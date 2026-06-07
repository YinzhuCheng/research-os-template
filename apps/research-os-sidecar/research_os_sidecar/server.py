from __future__ import annotations

import argparse
import json
import mimetypes
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .approval_service import ApprovalService
from .archive_service import ArchiveService
from .common import DEFAULT_PORT, public_error
from .profile_service import ProfileService
from .project_service import ProjectService
from .runtime_service import RuntimeService
from .security import import_file_to_project
from .state_service import ResearchStateService


class AppContext:
    def __init__(self, template_root: Path) -> None:
        self.projects = ProjectService(template_root)
        self.profiles = ProfileService()
        self.approvals = ApprovalService()
        self.runtime = RuntimeService(self.projects.require_project_root, self.approvals)
        self.state = ResearchStateService(self.projects.require_project_root)
        self.archives = ArchiveService(self.projects.require_project_root)


class Handler(BaseHTTPRequestHandler):
    context: AppContext

    def _send(self, status: int, body: bytes, content_type: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload: Any, status: int = 200) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"))

    def read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8") or "{}")

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send(204, b"")

    def do_GET(self) -> None:  # noqa: N802
        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            query = urllib.parse.parse_qs(parsed.query)
            if path == "/health":
                self.send_json({"ok": True, "service": "research-os-sidecar", "runtime": self.context.runtime.environment()})
            elif path == "/api/projects/current":
                self.send_json({"project": self.context.projects.current_project})
            elif path == "/api/profiles":
                self.send_json(self.context.profiles.list_profiles())
            elif path == "/api/runtime/environment":
                self.send_json(self.context.runtime.environment())
            elif path == "/api/runtime/events":
                after = int(query.get("after", ["0"])[0])
                self.send_json(self.context.runtime.list_events(after=after))
            elif path == "/api/account":
                self.send_json({"account": self.context.runtime.account()})
            elif path == "/api/models":
                self.send_json({"models": self.context.runtime.models()})
            elif path == "/api/state":
                self.send_json(self.context.state.read_state())
            elif path == "/api/approvals":
                self.send_json(self.context.approvals.list_pending())
            elif path == "/api/archive-preview":
                self.send_json(self.context.archives.preview())
            elif path == "/api/archives":
                self.send_json(self.context.archives.list_archives())
            elif path.startswith("/static/"):
                self._send_static(path.removeprefix("/static/"))
            else:
                self.send_json({"ok": False, "error": "Not found"}, status=404)
        except Exception as exc:  # noqa: BLE001
            self.send_json(public_error(exc), status=400)

    def do_POST(self) -> None:  # noqa: N802
        try:
            path = urllib.parse.urlparse(self.path).path
            payload = self.read_json_body()
            if path == "/api/projects/create":
                self.send_json({"project": self.context.projects.create_project(str(payload.get("name") or ""), str(payload.get("project_file") or ""))})
            elif path == "/api/projects/open":
                self.send_json({"project": self.context.projects.open_project(str(payload.get("project_file") or ""))})
            elif path == "/api/projects/close":
                self.send_json(self.context.projects.close_project())
            elif path == "/api/profiles":
                self.send_json({"profile": self.context.profiles.upsert_profile(payload)})
            elif path == "/api/profiles/delete":
                self.send_json(self.context.profiles.delete_profile(str(payload.get("profile_id") or "")))
            elif path == "/api/login/api-key":
                self.send_json({"login": self.context.runtime.login_api_key(str(payload.get("api_key") or ""))})
            elif path == "/api/login/chatgpt":
                self.send_json({"login": self.context.runtime.login_chatgpt(device_code=False)})
            elif path == "/api/login/device-code":
                self.send_json({"login": self.context.runtime.login_chatgpt(device_code=True)})
            elif path == "/api/logout":
                self.send_json({"logout": self.context.runtime.logout()})
            elif path == "/api/runtime/start-thread":
                profile = self.context.profiles.get_profile(payload.get("profile_id"))
                result = self.context.runtime.start_thread(profile, model=payload.get("model"), ephemeral=bool(payload.get("ephemeral", False)))
                thread_id = result.get("thread", {}).get("id")
                if thread_id:
                    self.context.projects.update_project({"codex": {"thread_id": thread_id, "last_turn_id": None, "last_status": "thread_started"}})
                self.send_json({"thread": result})
            elif path == "/api/runtime/resume-thread":
                profile = self.context.profiles.get_profile(payload.get("profile_id"))
                result = self.context.runtime.resume_thread(str(payload.get("thread_id") or ""), profile, model=payload.get("model"))
                self.send_json({"thread": result})
            elif path == "/api/runtime/start-turn":
                profile = self.context.profiles.get_profile(payload.get("profile_id"))
                result = self.context.runtime.start_turn(str(payload.get("thread_id") or ""), str(payload.get("text") or ""), profile, model=payload.get("model"))
                turn_id = result.get("turn", {}).get("id")
                if turn_id:
                    current = self.context.projects.current_project or {}
                    codex = dict(current.get("codex") or {})
                    codex.update({"last_turn_id": turn_id, "last_status": "turn_started"})
                    self.context.projects.update_project({"codex": codex})
                self.send_json({"turn": result})
            elif path == "/api/runtime/steer":
                self.send_json({"steer": self.context.runtime.steer(str(payload.get("thread_id") or ""), str(payload.get("turn_id") or ""), str(payload.get("text") or ""))})
            elif path == "/api/runtime/interrupt":
                self.send_json({"interrupt": self.context.runtime.interrupt(str(payload.get("thread_id") or ""), str(payload.get("turn_id") or ""))})
            elif path == "/api/approvals/decide":
                self.send_json({"approval": self.context.approvals.decide(str(payload.get("approval_id") or ""), str(payload.get("decision") or ""), str(payload.get("notes") or ""))})
            elif path == "/api/intake":
                self.send_json(self.context.state.submit_intake(payload))
            elif path == "/api/final-products":
                self.send_json({"plan": self.context.state.select_final_products(list(payload.get("tracks") or []), str(payload.get("free_form") or ""))})
            elif path == "/api/import-file":
                root = self.context.projects.require_project_root()
                self.send_json({"import": import_file_to_project(Path(str(payload.get("source_path") or "")), root, str(payload.get("target_subdir") or "INBOX/imports"))})
            elif path == "/api/archives/create":
                self.send_json({"archive": self.context.archives.create(str(payload.get("description") or ""), str(payload.get("user_free_form") or ""), payload.get("macro_phase"))})
            else:
                self.send_json({"ok": False, "error": "Not found"}, status=404)
        except Exception as exc:  # noqa: BLE001
            self.send_json(public_error(exc), status=400)

    def _send_static(self, relative_path: str) -> None:
        root = self.context.projects.require_project_root()
        target = (root / relative_path).resolve()
        if target != root and root not in target.parents:
            raise ValueError("Static path escapes project root.")
        if "PRIVATE" in target.parts or not target.is_file():
            raise ValueError("Static path is not public.")
        mime = mimetypes.guess_type(str(target))[0] or "text/plain"
        self._send(200, target.read_bytes(), f"{mime}; charset=utf-8")

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        print("research-os-sidecar: " + (format % args))


def serve(port: int, template_root: Path) -> None:
    Handler.context = AppContext(template_root)
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Research OS sidecar listening at http://127.0.0.1:{port}")
    print(f"Template root: {template_root.resolve()}")
    server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--template-root", default=str(Path.cwd()))
    args = parser.parse_args()
    if args.serve:
        serve(args.port, Path(args.template_root))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
