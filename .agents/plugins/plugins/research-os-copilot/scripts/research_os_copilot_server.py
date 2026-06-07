#!/usr/bin/env python3
"""Local Research OS Copilot bridge.

This script intentionally uses only the Python standard library. It provides:

- a local HTTP cockpit bridge for PUBLIC/copilot.html;
- a sanitized intake queue under CONTROL/copilot_inbox/;
- runtime private upload storage under PRIVATE/intake/<session_id>/;
- a lightweight JSON-line tool mode for MCP-adjacent smoke tests.

The browser never executes research work directly. It saves packets; Codex reads
them and asks the researcher for confirmation before mutating project artifacts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import mimetypes
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


DEFAULT_PORT = 8765
STATIC_ALLOWLIST = {
    "PUBLIC",
    "docs",
    "config",
    "templates",
    "CONTROL",
    "PROVENANCE",
    "domain_profiles",
    "skills",
    "scripts",
}
STATE_NAMES = {
    "material_input",
    "save_intake",
    "pending_intake_analysis",
    "questions_ready",
    "answers_received",
    "initialization_pending_confirmation",
    "initializing",
    "review_ready",
    "loop_alignment",
    "plan_pending_confirmation",
    "executing",
    "acceptance",
}
SESSION_ID_RE = re.compile(r"^INTAKE-[0-9A-Za-z_-]+$")
ARCHIVE_ID_RE = re.compile(r"^ARCH-[0-9A-Za-z_-]+$")
SECRET_RE = re.compile(r"(?i)(authorization\s*:|bearer\s+[a-z0-9._-]{12,}|api[_-]?key|secret[_-]?key|cookie\s*:|token\s*[:=])")


def utcish_now() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat()


def find_repo_root() -> Path:
    env_root = os.environ.get("RESEARCH_OS_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if (candidate / "CONTROL" / "work_order.yaml").exists():
            return candidate

    start_points = [Path.cwd().resolve(), Path(__file__).resolve()]
    for start in start_points:
        for parent in [start, *start.parents]:
            if (parent / "CONTROL" / "work_order.yaml").exists():
                return parent
    raise RuntimeError("Could not locate Research OS repository root.")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(name: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|\x00-\x1f]+', "_", name).strip()
    return cleaned[:140] or "upload.bin"


def safe_session_id(value: str) -> str:
    session_id = value.strip()
    if not SESSION_ID_RE.match(session_id):
        raise ValueError("Invalid session_id.")
    return session_id


def safe_archive_id(value: str) -> str:
    archive_id = value.strip()
    if not ARCHIVE_ID_RE.match(archive_id):
        raise ValueError("Invalid archive_id.")
    return archive_id


def run_git(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result


def private_text_summary(text: str) -> str:
    if not text.strip():
        return "No free text submitted."
    return "Raw free text is stored only under PRIVATE/intake/<session_id>/free_text.md when the local bridge is active."


def extract_links(text: str) -> list[dict[str, Any]]:
    links: list[dict[str, Any]] = []
    for url in sorted(set(re.findall(r"https?://[^\s<>'\"]+", text))):
        declared = "other"
        lowered = url.lower()
        if "chat.openai.com" in lowered or "chatgpt.com" in lowered:
            declared = "chat_link"
        elif "arxiv.org" in lowered or "doi.org" in lowered:
            declared = "paper_link"
        elif "github.com" in lowered or "gitlab.com" in lowered:
            declared = "repo_link"
        links.append(
            {
                "url": url.rstrip(").,;"),
                "declared_type": declared,
                "fetch_authorized": False,
                "notes": "Recorded from intake text; fetching requires explicit authorization.",
            }
        )
    return links


def parse_multipart(body: bytes, content_type: str) -> tuple[dict[str, str], list[dict[str, Any]]]:
    boundary_match = re.search(r"boundary=([^;]+)", content_type)
    if not boundary_match:
        return {}, []
    boundary = boundary_match.group(1).strip().strip('"').encode("utf-8")
    delimiter = b"--" + boundary
    fields: dict[str, str] = {}
    files: list[dict[str, Any]] = []

    for raw_part in body.split(delimiter):
        part = raw_part.strip()
        if not part or part == b"--":
            continue
        if part.endswith(b"--"):
            part = part[:-2].strip()
        if b"\r\n\r\n" not in part:
            continue
        raw_headers, data = part.split(b"\r\n\r\n", 1)
        headers = raw_headers.decode("utf-8", errors="replace")
        disposition = re.search(r'Content-Disposition: form-data;\s*name="([^"]+)"(?:;\s*filename="([^"]*)")?', headers, re.I)
        if not disposition:
            continue
        name = disposition.group(1)
        filename = disposition.group(2)
        data = data.rstrip(b"\r\n")
        if filename:
            files.append({"field": name, "filename": filename, "data": data})
        else:
            fields[name] = data.decode("utf-8", errors="replace")
    return fields, files


class CopilotStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    @property
    def public_state_path(self) -> Path:
        return self.root / "PUBLIC" / "copilot_state.json"

    @property
    def inbox_dir(self) -> Path:
        return self.root / "CONTROL" / "copilot_inbox"

    @property
    def event_log(self) -> Path:
        return self.root / "PROVENANCE" / "copilot_events.jsonl"

    @property
    def run_monitor_path(self) -> Path:
        return self.root / "PUBLIC" / "run_monitor.json"

    @property
    def archive_log_path(self) -> Path:
        return self.root / "PROVENANCE" / "archive_index.jsonl"

    @property
    def public_archive_path(self) -> Path:
        return self.root / "PUBLIC" / "archive_index.json"

    def session_id(self) -> str:
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"INTAKE-{stamp}"

    def save_intake(self, fields: dict[str, str], files: list[dict[str, Any]]) -> dict[str, Any]:
        session_id = safe_session_id(fields.get("session_id") or self.session_id())
        free_text = fields.get("free_text", "")
        upload_dir = self.root / "PRIVATE" / "intake" / session_id
        upload_dir.mkdir(parents=True, exist_ok=True)

        uploaded_files: list[dict[str, Any]] = []
        material_hashes: list[str] = []
        for index, item in enumerate(files, start=1):
            original_name = item["filename"] or f"upload-{index}.bin"
            data = item["data"]
            digest = sha256_bytes(data)
            material_hashes.append(digest)
            private_name = f"{index:03d}-{safe_name(original_name)}"
            private_path = upload_dir / private_name
            private_path.write_bytes(data)
            uploaded_files.append(
                {
                    "file_id": f"file-{index:03d}",
                    "original_name": original_name,
                    "mime_type": mimetypes.guess_type(original_name)[0],
                    "size_bytes": len(data),
                    "sha256": digest,
                    "storage_policy": "private_runtime_only",
                    "public_summary": "Private upload registered; raw content is not public.",
                }
            )

        text_digest: str | None = None
        text_size = len(free_text.encode("utf-8"))
        if free_text.strip():
            (upload_dir / "free_text.md").write_text(free_text, encoding="utf-8")
            text_digest = sha256_bytes(free_text.encode("utf-8"))
            material_hashes.append(text_digest)
        source_links = extract_links(free_text)

        packet = {
            "schema_version": "v1.1",
            "session_id": session_id,
            "created_at": utcish_now(),
            "free_text_present": bool(free_text.strip()),
            "free_text_sha256": text_digest,
            "free_text_size_bytes": text_size,
            "free_text_summary": private_text_summary(free_text),
            "uploaded_files": uploaded_files,
            "source_links": source_links,
            "privacy_default": "private",
            "material_hashes": material_hashes,
            "status": "pending_intake_analysis",
        }

        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        write_json(self.inbox_dir / f"{session_id}.intake.json", packet)
        append_jsonl(
            self.event_log,
            {
                "event": "intake_saved",
                "timestamp": utcish_now(),
                "session_id": session_id,
                "uploaded_file_count": len(uploaded_files),
                "source_link_count": len(source_links),
                "status": "pending_intake_analysis",
            },
        )
        self.update_public_state_from_intake(packet)
        return self.sanitize_packet(packet)

    def sanitize_packet(self, packet: dict[str, Any]) -> dict[str, Any]:
        clean = dict(packet)
        clean.pop("free_text", None)
        clean["uploaded_files"] = [
            {k: v for k, v in item.items() if k != "private_runtime_path"}
            for item in packet.get("uploaded_files", [])
        ]
        return clean

    def update_public_state_from_intake(self, packet: dict[str, Any]) -> None:
        state = read_json(self.public_state_path, {})
        state.update(
            {
                "schema_version": "v1.0",
                "updated_at": utcish_now(),
                "state": "pending_intake_analysis",
                "active_session_id": packet["session_id"],
                "research_type": "unclear",
                "pending_confirmation": True,
                "intake_summary": {
                    "free_text_present": bool(packet.get("free_text_present")),
                    "free_text_sha256": packet.get("free_text_sha256"),
                    "free_text_size_bytes": packet.get("free_text_size_bytes", 0),
                    "free_text_summary": packet.get("free_text_summary", ""),
                    "uploaded_file_count": len(packet.get("uploaded_files", [])),
                    "source_link_count": len(packet.get("source_links", [])),
                    "material_hashes": packet.get("material_hashes", []),
                },
            }
        )
        write_json(self.public_state_path, state)

    def save_answers(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = read_json(self.public_state_path, {})
        session_id = safe_session_id(str(payload.get("session_id") or state.get("active_session_id") or ""))
        answers = payload.get("answers", [])
        if not isinstance(answers, list) or len(answers) != 3:
            raise ValueError("Exactly three question answers are required.")

        clean_answers = []
        for index, answer in enumerate(answers, start=1):
            if not isinstance(answer, dict):
                raise ValueError("Each answer must be an object.")
            question_id = str(answer.get("question_id") or f"Q-{index:02d}")
            if not re.match(r"^Q-[0-9]{2}$", question_id):
                raise ValueError(f"Invalid question_id: {question_id}")
            clean_answers.append(
                {
                    "question_id": question_id,
                    "selected_option": str(answer.get("selected_option") or ""),
                    "free_text_other": str(answer.get("free_text_other") or ""),
                }
            )

        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        packet = {
            "schema_version": "v1.0",
            "answers_packet_id": f"ANS-{stamp}",
            "session_id": session_id,
            "question_packet_id": payload.get("question_packet_id") or state.get("question_packet_id"),
            "created_at": utcish_now(),
            "answers": clean_answers,
            "status": "answers_received",
        }
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        write_json(self.inbox_dir / f"{session_id}.answers.json", packet)
        state.update(
            {
                "updated_at": utcish_now(),
                "state": "answers_received",
                "active_session_id": session_id,
                "pending_confirmation": True,
                "answer_summary": {
                    "answers_packet_id": packet["answers_packet_id"],
                    "answer_count": len(clean_answers),
                    "status": packet["status"],
                },
            }
        )
        write_json(self.public_state_path, state)
        append_jsonl(
            self.event_log,
            {
                "event": "answers_saved",
                "timestamp": utcish_now(),
                "session_id": session_id,
                "answer_count": len(clean_answers),
                "status": "answers_received",
            },
        )
        return packet

    def save_confirmation(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = read_json(self.public_state_path, {})
        session_id = safe_session_id(str(payload.get("session_id") or state.get("active_session_id") or ""))
        confirmed = bool(payload.get("confirmed", False))
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        packet = {
            "schema_version": "v1.0",
            "confirmation_id": f"CONF-{stamp}",
            "session_id": session_id,
            "created_at": utcish_now(),
            "next_action": str(payload.get("next_action") or "Generate initialization report after Codex review."),
            "confirmed": confirmed,
            "requires_work_order": bool(payload.get("requires_work_order", True)),
            "notes": str(payload.get("notes") or ""),
            "status": "confirmed" if confirmed else "changes_requested",
        }
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        write_json(self.inbox_dir / f"{session_id}.confirmation.json", packet)
        state.update(
            {
                "updated_at": utcish_now(),
                "state": "initialization_pending_confirmation" if confirmed else "plan_pending_confirmation",
                "active_session_id": session_id,
                "pending_confirmation": not confirmed,
                "next_action": {
                    "label": packet["next_action"],
                    "requires_work_order": packet["requires_work_order"],
                    "status": packet["status"],
                },
            }
        )
        write_json(self.public_state_path, state)
        append_jsonl(
            self.event_log,
            {
                "event": "next_action_confirmation_saved",
                "timestamp": utcish_now(),
                "session_id": session_id,
                "confirmed": confirmed,
                "status": packet["status"],
            },
        )
        return packet

    def session_state(self, session_id: str) -> dict[str, Any]:
        safe_id = safe_session_id(session_id)
        return {
            "session_id": safe_id,
            "public_state": read_json(self.public_state_path, {}),
            "packets": {
                "intake": (self.inbox_dir / f"{safe_id}.intake.json").exists(),
                "answers": (self.inbox_dir / f"{safe_id}.answers.json").exists(),
                "confirmation": (self.inbox_dir / f"{safe_id}.confirmation.json").exists(),
            },
            "run_monitor": read_json(self.run_monitor_path, {"runs": []}),
        }

    def list_pending(self) -> list[dict[str, Any]]:
        if not self.inbox_dir.exists():
            return []
        packets = []
        for path in sorted(self.inbox_dir.glob("*.json")):
            try:
                payload = read_json(path, {})
                packets.append(
                    {
                        "path": str(path.relative_to(self.root)),
                        "session_id": payload.get("session_id"),
                        "status": payload.get("status"),
                        "created_at": payload.get("created_at"),
                    }
                )
            except Exception as exc:  # noqa: BLE001 - report malformed queue items.
                packets.append({"path": str(path.relative_to(self.root)), "error": str(exc)})
        return packets

    def download_references(self) -> dict[str, Any]:
        state = read_json(self.public_state_path, {})
        refs = state.get("literature", {}).get("reference_links", [])
        output_dir = self.root / "PRIVATE" / "references" / (state.get("active_session_id") or "default")
        output_dir.mkdir(parents=True, exist_ok=True)
        results = []
        for ref in refs:
            url = str(ref.get("url", ""))
            policy = str(ref.get("download_policy", "human_download_required"))
            title = safe_name(str(ref.get("title", "reference")))
            target_url = open_reference_url(url, policy)
            if not target_url:
                results.append({"title": title, "status": "skipped", "message": "Policy requires human download."})
                continue
            ext = ".pdf" if ".pdf" in target_url.lower() else ".html"
            target = output_dir / f"{title}{ext}"
            try:
                urllib.request.urlretrieve(target_url, target)
                results.append({"title": title, "status": "downloaded", "path": str(target.relative_to(self.root))})
            except Exception as exc:  # noqa: BLE001 - preserve failure for human handling.
                results.append({"title": title, "status": "failed", "message": str(exc)})
        write_json(output_dir / "download_report.json", results)
        return {"output_dir": str(output_dir.relative_to(self.root)), "results": results}

    def git_changed_paths(self) -> list[str]:
        result = run_git(self.root, ["status", "--porcelain"], check=True)
        paths: list[str] = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            path = line[3:].strip()
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            paths.append(path.replace("\\", "/"))
        return paths

    def git_head(self) -> str:
        return run_git(self.root, ["rev-parse", "HEAD"], check=True).stdout.strip()

    def git_branch(self) -> str:
        return run_git(self.root, ["rev-parse", "--abbrev-ref", "HEAD"], check=True).stdout.strip()

    def current_phase_info(self) -> tuple[str, str]:
        project_text = (self.root / "config" / "research_project.yaml").read_text(encoding="utf-8")
        phase_text = (self.root / "CONTROL" / "phase_gate.yaml").read_text(encoding="utf-8")
        phase = "unknown"
        macro_phase = "unknown"
        for line in project_text.splitlines():
            if line.startswith("current_phase:"):
                phase = line.split(":", 1)[1].strip().strip('"')
            if line.startswith("current_macro_phase:"):
                macro_phase = line.split(":", 1)[1].strip().strip('"')
        if phase == "unknown":
            for line in phase_text.splitlines():
                if line.startswith("current_phase:"):
                    phase = line.split(":", 1)[1].strip().strip('"')
        return phase, macro_phase

    def scan_archive_paths(self, paths: list[str]) -> None:
        for path in paths:
            parts = Path(path).parts
            if path.startswith("PRIVATE/") or "PRIVATE" in parts:
                raise ValueError(f"Archive refuses PRIVATE path: {path}")
            target = (self.root / path).resolve()
            if not str(target).startswith(str(self.root.resolve())):
                raise ValueError(f"Archive path escapes repository: {path}")
            if target.is_file():
                try:
                    text = target.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                if SECRET_RE.search(text):
                    raise ValueError(f"Archive secrets scan failed for changed path: {path}")

    def archive_preview(self) -> dict[str, Any]:
        phase, macro_phase = self.current_phase_info()
        changed_paths = self.git_changed_paths()
        self.scan_archive_paths(changed_paths)
        return {
            "ok": True,
            "phase": phase,
            "macro_phase": macro_phase,
            "git_branch": self.git_branch(),
            "git_commit": self.git_head(),
            "dirty": bool(changed_paths),
            "changed_paths": changed_paths,
            "private_paths_included": False,
            "secrets_scan": "passed",
            "status": "preview",
        }

    def list_archives(self) -> dict[str, Any]:
        archives = []
        if self.archive_log_path.exists():
            for line in self.archive_log_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    archives.append(json.loads(line))
        return {"archives": archives}

    def write_public_archive_index(self) -> None:
        archives = self.list_archives()["archives"]
        public_archives = [
            {
                "archive_id": item.get("archive_id"),
                "created_at": item.get("created_at"),
                "phase": item.get("phase"),
                "macro_phase": item.get("macro_phase"),
                "git_commit": item.get("git_commit"),
                "git_branch": item.get("git_branch"),
                "description": item.get("description"),
                "changed_path_count": len(item.get("changed_paths", [])),
                "status": item.get("status"),
            }
            for item in archives
        ]
        write_json(self.public_archive_path, {"archives": public_archives})

    def create_archive(self, payload: dict[str, Any]) -> dict[str, Any]:
        description = str(payload.get("description") or "").strip()
        if not description:
            raise ValueError("Archive description is required.")
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        archive_id = safe_archive_id(str(payload.get("archive_id") or f"ARCH-{stamp}"))
        phase, default_macro_phase = self.current_phase_info()
        macro_phase = str(payload.get("macro_phase") or default_macro_phase or "unknown")
        if macro_phase not in {"initialization", "research_loop", "final_product", "unknown"}:
            macro_phase = "unknown"

        changed_paths = self.git_changed_paths()
        self.scan_archive_paths(changed_paths)
        if changed_paths:
            run_git(self.root, ["add", "--all", "--", "."])
            run_git(
                self.root,
                [
                    "-c",
                    "user.name=Research OS Archive",
                    "-c",
                    "user.email=research-os-archive@example.invalid",
                    "commit",
                    "-m",
                    f"archive snapshot: {description[:72]}",
                ],
            )
        snapshot_commit = self.git_head()
        record = {
            "archive_id": archive_id,
            "created_at": utcish_now(),
            "phase": phase,
            "macro_phase": macro_phase,
            "git_commit": snapshot_commit,
            "git_branch": self.git_branch(),
            "description": description,
            "user_free_form": str(payload.get("user_free_form") or ""),
            "changed_paths": changed_paths,
            "public_index_path": "PUBLIC/archive_index.json",
            "private_paths_included": False,
            "secrets_scan": "passed",
            "status": "created",
        }
        append_jsonl(self.archive_log_path, record)
        self.write_public_archive_index()
        run_git(self.root, ["add", "--", "PROVENANCE/archive_index.jsonl", "PUBLIC/archive_index.json"])
        run_git(
            self.root,
            [
                "-c",
                "user.name=Research OS Archive",
                "-c",
                "user.email=research-os-archive@example.invalid",
                "commit",
                "-m",
                f"archive index: {archive_id}",
            ],
        )
        record["index_commit"] = self.git_head()
        return record


def open_reference_url(url: str, policy: str) -> str | None:
    if policy == "human_download_required":
        return None
    match = re.match(r"^https://arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5}(v[0-9]+)?)", url)
    if match:
        return f"https://arxiv.org/pdf/{match.group(1)}.pdf"
    if url.startswith("https://arxiv.org/pdf/"):
        return url
    if policy == "landing_page_only" and url.startswith("https://"):
        return url
    if policy == "open_access_attempt" and url.startswith("https://"):
        return url
    return None


class Handler(BaseHTTPRequestHandler):
    store: CopilotStore

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:8765")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload: Any, status: int = 200) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"), "application/json; charset=utf-8")

    def send_static(self, request_path: str) -> bool:
        clean = urllib.parse.unquote(request_path).lstrip("/")
        if not clean:
            return False
        if clean in {"README.md", "AGENTS.md"}:
            target = self.store.root / clean
        else:
            first = clean.split("/", 1)[0]
            if first not in STATIC_ALLOWLIST:
                return False
            target = self.store.root / clean
        resolved = target.resolve()
        root = self.store.root.resolve()
        if not str(resolved).startswith(str(root)):
            return False
        if "PRIVATE" in resolved.parts:
            return False
        if not resolved.is_file():
            return False
        mime = mimetypes.guess_type(str(resolved))[0] or "text/plain"
        if resolved.suffix.lower() in {".md", ".yaml", ".yml", ".json", ".jsonl", ".ps1", ".py"}:
            mime = "text/plain"
        if resolved.suffix.lower() == ".html":
            mime = "text/html"
        self._send(200, resolved.read_bytes(), f"{mime}; charset=utf-8")
        return True

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:8765")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in {"/", "/copilot", "/copilot.html"}:
            path = self.store.root / "PUBLIC" / "copilot.html"
            self._send(200, path.read_bytes(), "text/html; charset=utf-8")
            return
        if parsed.path == "/index.html":
            path = self.store.root / "PUBLIC" / "index.html"
            self._send(200, path.read_bytes(), "text/html; charset=utf-8")
            return
        if parsed.path in {"/api/state", "/copilot_state.json"}:
            self.send_json(read_json(self.store.public_state_path, {}))
            return
        if parsed.path == "/dashboard_data.json":
            self.send_json(read_json(self.store.root / "PUBLIC" / "dashboard_data.json", {}))
            return
        if parsed.path == "/run_monitor.json":
            self.send_json(read_json(self.store.run_monitor_path, {"runs": []}))
            return
        if parsed.path == "/api/archive-preview":
            try:
                self.send_json(self.store.archive_preview())
            except Exception as exc:  # noqa: BLE001
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return
        if parsed.path in {"/api/archives", "/archive_index.json"}:
            self.send_json(self.store.list_archives())
            return
        session_match = re.match(r"^/api/session/([^/]+)/state$", parsed.path)
        if session_match:
            try:
                self.send_json(self.store.session_state(urllib.parse.unquote(session_match.group(1))))
            except Exception as exc:  # noqa: BLE001 - API returns validation failure.
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return
        if parsed.path == "/api/pending":
            self.send_json({"pending": self.store.list_pending()})
            return
        if self.send_static(parsed.path):
            return
        self.send_error(404, "Not found")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        if parsed.path == "/api/intake":
            try:
                content_type = self.headers.get("Content-Type", "")
                if content_type.startswith("multipart/form-data"):
                    fields, files = parse_multipart(body, content_type)
                else:
                    payload = json.loads(body.decode("utf-8") or "{}")
                    fields = {key: str(value) for key, value in payload.items() if isinstance(value, (str, int, float, bool))}
                    files = []
                packet = self.store.save_intake(fields, files)
                self.send_json({"ok": True, "packet": packet})
            except Exception as exc:  # noqa: BLE001 - API returns validation failure.
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return
        if parsed.path == "/api/question-answers":
            try:
                payload = json.loads(body.decode("utf-8") or "{}")
                packet = self.store.save_answers(payload)
                self.send_json({"ok": True, "answers": packet})
            except Exception as exc:  # noqa: BLE001
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return
        if parsed.path == "/api/confirm-next-action":
            try:
                payload = json.loads(body.decode("utf-8") or "{}")
                packet = self.store.save_confirmation(payload)
                self.send_json({"ok": True, "confirmation": packet})
            except Exception as exc:  # noqa: BLE001
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return
        if parsed.path == "/api/download-references":
            self.send_json({"ok": True, "download": self.store.download_references()})
            return
        if parsed.path == "/api/archive-snapshot":
            try:
                payload = json.loads(body.decode("utf-8") or "{}")
                self.send_json({"ok": True, "archive": self.store.create_archive(payload)})
            except Exception as exc:  # noqa: BLE001
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return
        self.send_error(404, "Not found")

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        sys.stderr.write("research-os-copilot: " + (format % args) + "\n")


def serve(port: int) -> None:
    root = find_repo_root()
    Handler.store = CopilotStore(root)
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Research OS Copilot running at http://127.0.0.1:{port}/")
    print(f"Repository root: {root}")
    server.serve_forever()


def mcp_stdio() -> None:
    """Lightweight JSON-line tool shim.

    This keeps the repo self-contained for bridge smoke tests. A production MCP
    transport can wrap the same store methods.
    """
    store = CopilotStore(find_repo_root())
    tools = {
        "list_pending_intake": lambda _: {"pending": store.list_pending()},
        "read_public_state": lambda _: read_json(store.public_state_path, {}),
        "read_session_state": lambda args: store.session_state(str(args.get("session_id", ""))),
        "save_question_answers": lambda args: store.save_answers(args),
        "confirm_next_action": lambda args: store.save_confirmation(args),
        "download_references": lambda _: store.download_references(),
        "archive_preview": lambda _: store.archive_preview(),
        "create_archive": lambda args: store.create_archive(args),
        "list_archives": lambda _: store.list_archives(),
    }
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            tool = request.get("tool")
            args = request.get("arguments", {})
            if tool == "tools/list":
                response = {"tools": sorted(tools)}
            elif tool in tools:
                response = tools[tool](args)
            else:
                response = {"error": f"Unknown tool: {tool}"}
        except Exception as exc:  # noqa: BLE001
            response = {"error": str(exc)}
        print(json.dumps(response, ensure_ascii=False), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Run local HTTP cockpit bridge.")
    parser.add_argument("--mcp-stdio", action="store_true", help="Run JSON-line MCP-adjacent tool shim.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    if args.serve:
        serve(args.port)
    elif args.mcp_stdio:
        mcp_stdio()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
