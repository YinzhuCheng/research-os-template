from __future__ import annotations

import datetime as dt
import json
import os
import re
import time
import uuid
from pathlib import Path
from typing import Any


APP_NAME = "LocalCodexRouter"
PROJECT_SCHEMA_VERSION = "local-codex-router-project-v1"
LEGACY_PROJECT_SCHEMA_VERSION = "codex-shell-project-v1"
DEFAULT_PORT = 8790
DEFAULT_CODEX_HOME_NAME = "embedded_codex_home"
SHORT_CODEX_HOME_DIR = ("LCR", "cx")
PROJECT_FILE_SUFFIX = ".lcrproj"
LEGACY_PROJECT_FILE_SUFFIX = ".codexproj"
WORKSPACE_STATE_DIRNAME = ".lcr"
LEGACY_WORKSPACE_STATE_DIRNAME = ".codex-shell"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat()


def new_id(prefix: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).astimezone().strftime("%Y%m%dT%H%M%S%f")
    return f"{prefix}-{stamp}-{uuid.uuid4().hex[:6]}"


def app_data_dir() -> Path:
    root = os.environ.get("LOCAL_CODEX_ROUTER_APPDATA") or os.environ.get("CODEX_SHELL_APPDATA")
    if root:
        return Path(root).expanduser().resolve()
    if os.name == "nt":
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(base) / APP_NAME
    return Path.home() / ".local-codex-router"


def default_codex_home() -> Path:
    override = os.environ.get("LOCAL_CODEX_ROUTER_CODEX_HOME") or os.environ.get("CODEX_SHELL_CODEX_HOME")
    if override:
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base).joinpath(*SHORT_CODEX_HOME_DIR)
    return app_data_dir() / DEFAULT_CODEX_HOME_NAME


def slugify(value: str, default: str = "codex-project") -> str:
    cleaned = re.sub(r"[^0-9A-Za-z._-]+", "-", value.strip()).strip("-._")
    return cleaned[:80] or default


def ensure_suffix(path: Path, suffix: str) -> Path:
    return path if path.suffix.lower() == suffix.lower() else path.with_suffix(suffix)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    last_error: Exception | None = None
    for attempt in range(5):
        temp_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
        try:
            temp_path.write_text(text, encoding="utf-8")
            os.replace(temp_path, path)
            return
        except PermissionError as exc:
            # Windows file watchers and concurrent readers can briefly hold the
            # destination after another atomic write. Use a fresh temp file on
            # each retry so failed replacements never leak into later attempts.
            last_error = exc
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
            time.sleep(0.05 * (attempt + 1))
    if last_error is not None:
        raise last_error


def append_jsonl(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


def public_error(exc: Exception) -> dict[str, Any]:
    return {"ok": False, "error": str(exc), "error_type": exc.__class__.__name__}
