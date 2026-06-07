from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any


SECRET_RE = re.compile(
    r"(?i)(authorization\s*:|bearer\s+[a-z0-9._-]{12,}|api[_-]?key|secret[_-]?key|cookie\s*:|token\s*[:=]|ssh-rsa|BEGIN\s+(RSA|OPENSSH|EC|DSA)\s+PRIVATE\s+KEY)"
)
SECRET_PATH_PARTS = {
    ".aws",
    ".azure",
    ".docker",
    ".gnupg",
    ".kube",
    ".ssh",
    "credentials",
    "secrets",
}
SAFE_GIT_COMMANDS = {
    "status",
    "diff",
    "log",
    "branch",
    "show",
    "add",
    "commit",
}


class SecurityError(ValueError):
    pass


def resolve_under(root: Path, value: str | Path) -> Path:
    root = root.resolve()
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    if resolved != root and root not in resolved.parents:
        raise SecurityError(f"Path escapes project sandbox: {value}")
    return resolved


def relative_to_root(root: Path, value: str | Path) -> str:
    resolved = resolve_under(root, value)
    return resolved.relative_to(root.resolve()).as_posix()


def assert_no_secret_path(path: Path) -> None:
    lowered = {part.lower() for part in path.parts}
    if lowered.intersection(SECRET_PATH_PARTS):
        raise SecurityError(f"Refusing secret-bearing path: {path}")


def scan_text_for_secrets(path: Path) -> None:
    if not path.is_file():
        return
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    if SECRET_RE.search(text):
        raise SecurityError(f"Secret-like content detected in {path}")


def import_file_to_project(source: Path, project_root: Path, target_subdir: str = "INBOX/imports") -> dict[str, Any]:
    source = source.expanduser().resolve()
    if not source.exists() or not source.is_file():
        raise SecurityError(f"Import source is not a file: {source}")
    assert_no_secret_path(source)
    scan_text_for_secrets(source)
    target_dir = resolve_under(project_root, target_subdir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    shutil.copy2(source, target)
    return {"source_name": source.name, "target": relative_to_root(project_root, target)}


def classify_command(command: str, cwd: str | None = None) -> dict[str, Any]:
    stripped = command.strip()
    lowered = stripped.lower()
    risky_markers = [
        " --global",
        "npm install -g",
        "pip install --user",
        "setx ",
        "reg add",
        "sc.exe ",
        "schtasks ",
        "format ",
        "del /s",
        "remove-item -recurse",
        "git push",
        "gh release",
        "curl -x",
    ]
    if any(marker in lowered for marker in risky_markers):
        return {"risk": "high", "decision": "requires_confirmation", "reason": "External, global, or destructive command pattern."}
    if lowered.startswith("git "):
        parts = lowered.split()
        subcommand = parts[1] if len(parts) > 1 else ""
        if subcommand in SAFE_GIT_COMMANDS:
            return {"risk": "low", "decision": "allowed_in_sandbox", "reason": "Safe git operation inside project sandbox."}
        return {"risk": "medium", "decision": "requires_confirmation", "reason": "Git command can affect remotes or history."}
    return {"risk": "medium", "decision": "requires_confirmation", "reason": "Command requires Research OS approval."}


def validate_changed_paths(project_root: Path, paths: list[str]) -> None:
    for path in paths:
        normalized = path.replace("\\", "/")
        if normalized.startswith("PRIVATE/") or "/PRIVATE/" in normalized:
            raise SecurityError(f"Archive refuses PRIVATE path: {path}")
        resolved = resolve_under(project_root, normalized)
        assert_no_secret_path(resolved)
        scan_text_for_secrets(resolved)


def redact_sensitive(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            lowered = str(key).lower()
            if any(marker in lowered for marker in ("api_key", "apikey", "authorization", "cookie", "password", "secret", "token")):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = redact_sensitive(item)
        return redacted
    if isinstance(value, list):
        return [redact_sensitive(item) for item in value]
    if isinstance(value, str) and SECRET_RE.search(value):
        return "[REDACTED]"
    return value
