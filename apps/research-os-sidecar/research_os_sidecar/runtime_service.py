from __future__ import annotations

import shutil
import threading
from pathlib import Path
from typing import Any, Callable

from .approval_service import ApprovalService
from .common import append_jsonl, now_iso
from .runtime_config_service import RuntimeConfigService
from .security import redact_sensitive


RESEARCH_OS_DEVELOPER_INSTRUCTIONS = """You are running inside a Research OS desktop project sandbox.
Before acting, read AGENTS.md and CONTROL/project_context.md when present.
Use the project root as the only default writable workspace.
Do not read or write outside the project unless the Research OS UI explicitly grants a path import or approval.
Preserve CONTROL, PUBLIC, PRIVATE, PROVENANCE, resource ledgers, run manifests, negative results, and intermediate artifacts.
Follow the three macro phases: initialization, semi-automated research loop, final product.
Every user-facing choice must include a recommended option, concrete defaults, and natural-language free-form input.
Treat existing manuscripts, PDFs, PPT files, notes, templates, and reviews as initialization material until Research OS gates accept them.
Inspect whole-folder material manifests before planning or writing, and do not focus only on the obvious draft file.
Before research or paper work, inspect and follow the relevant repository SKILL.md files.
For manuscript work, verify venue rules and every cited source online; do not invent citations, DOIs, theorems, experiments, or results.
When a Research OS Desktop or workflow gap blocks reusable progress, record the gap and prefer fixing the app/workflow before bypassing it.
"""


class RuntimeService:
    def __init__(
        self,
        project_root_provider,
        approval_service: ApprovalService,
        on_turn_status: Callable[[str, str], None] | None = None,
    ) -> None:
        self._project_root_provider = project_root_provider
        self._approval_service = approval_service
        self._on_turn_status = on_turn_status
        self._runtime_config = RuntimeConfigService()
        self._client: Any | None = None
        self._events: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def environment(self) -> dict[str, Any]:
        return {
            "codex_cli": shutil.which("codex"),
            "codex_sdk_available": self._sdk_available(),
            "adapter": "openai_codex.client.CodexClient",
            "runtime_config": self._runtime_config.status(),
        }

    def load_provider_secret(self, profile: dict[str, Any], key_file_path: str) -> dict[str, Any]:
        status = self._runtime_config.load_secret_from_file(profile, key_file_path)
        self._record_event({"type": "runtime_secret_loaded", "payload": status})
        return status

    def account(self) -> dict[str, Any]:
        client = self._ensure_client()
        response = client.account_read({"refreshToken": False})
        return self._model_to_dict(response)

    def login_api_key(self, api_key: str) -> dict[str, Any]:
        if not api_key.strip():
            raise ValueError("api_key is required for API-key login and is never saved by Research OS.")
        client = self._ensure_client()
        response = client.account_login_start({"type": "apiKey", "apiKey": api_key})
        return self._model_to_dict(response)

    def login_chatgpt(self, device_code: bool = False) -> dict[str, Any]:
        client = self._ensure_client()
        response = client.account_login_start({"type": "chatgptDeviceCode" if device_code else "chatgpt"})
        return self._model_to_dict(response)

    def logout(self) -> dict[str, Any]:
        client = self._ensure_client()
        response = client.account_logout()
        return self._model_to_dict(response)

    def models(self) -> dict[str, Any]:
        client = self._ensure_client()
        return self._model_to_dict(client.model_list(include_hidden=False))

    def start_thread(self, profile: dict[str, Any], model: str | None = None, ephemeral: bool = False) -> dict[str, Any]:
        root = self._project_root_provider()
        runtime_status = self._runtime_config.prepare_profile(profile, require_secret=profile.get("provider_id") == "yunwu")
        client = self._ensure_client()
        params: dict[str, Any] = {
            "cwd": str(root),
            "sandbox": "workspace-write",
            "approvalPolicy": "on-request",
            "approvalsReviewer": "user",
            "developerInstructions": RESEARCH_OS_DEVELOPER_INSTRUCTIONS,
            "ephemeral": ephemeral,
            "serviceName": "research_os_desktop",
        }
        chosen_model = model or profile.get("model")
        if chosen_model:
            params["model"] = chosen_model
        if profile.get("provider_id"):
            params["modelProvider"] = profile["provider_id"]
        started = client.thread_start(params)
        payload = self._model_to_dict(started)
        self._record_event({"type": "thread_started", "payload": payload, "runtime_config": runtime_status})
        return payload

    def resume_thread(self, thread_id: str, profile: dict[str, Any], model: str | None = None) -> dict[str, Any]:
        root = self._project_root_provider()
        runtime_status = self._runtime_config.prepare_profile(profile, require_secret=profile.get("provider_id") == "yunwu")
        client = self._ensure_client()
        params: dict[str, Any] = {
            "cwd": str(root),
            "sandbox": "workspace-write",
            "approvalPolicy": "on-request",
            "approvalsReviewer": "user",
            "developerInstructions": RESEARCH_OS_DEVELOPER_INSTRUCTIONS,
        }
        chosen_model = model or profile.get("model")
        if chosen_model:
            params["model"] = chosen_model
        if profile.get("provider_id"):
            params["modelProvider"] = profile["provider_id"]
        resumed = client.thread_resume(thread_id, params)
        payload = self._model_to_dict(resumed)
        self._record_event({"type": "thread_resumed", "payload": payload, "runtime_config": runtime_status})
        return payload

    def start_turn(self, thread_id: str, text: str, profile: dict[str, Any], model: str | None = None) -> dict[str, Any]:
        if not text.strip():
            raise ValueError("Turn text is required.")
        root = self._project_root_provider()
        runtime_status = self._runtime_config.prepare_profile(profile, require_secret=profile.get("provider_id") == "yunwu")
        client = self._ensure_client()
        params: dict[str, Any] = {
            "cwd": str(root),
            "approvalPolicy": "on-request",
            "approvalsReviewer": "user",
            "sandboxPolicy": {"type": "workspaceWrite", "writableRoots": [str(root)], "networkAccess": True},
            "serviceName": "research_os_desktop",
        }
        chosen_model = model or profile.get("model")
        if chosen_model:
            params["model"] = chosen_model
        if profile.get("provider_id"):
            params["modelProvider"] = profile["provider_id"]
        started = client.turn_start(thread_id, text, params)
        payload = self._model_to_dict(started)
        turn_id = payload.get("turn", {}).get("id")
        if turn_id:
            threading.Thread(target=self._drain_turn, args=(turn_id,), daemon=True).start()
        self._record_event({"type": "turn_started", "payload": payload, "runtime_config": runtime_status})
        return payload

    def steer(self, thread_id: str, turn_id: str, text: str) -> dict[str, Any]:
        client = self._ensure_client()
        response = client.turn_steer(thread_id, turn_id, text)
        payload = self._model_to_dict(response)
        self._record_event({"type": "turn_steered", "payload": payload})
        return payload

    def interrupt(self, thread_id: str, turn_id: str) -> dict[str, Any]:
        client = self._ensure_client()
        response = client.turn_interrupt(thread_id, turn_id)
        payload = self._model_to_dict(response)
        self._record_event({"type": "turn_interrupted", "payload": payload})
        return payload

    def list_events(self, after: int = 0, limit: int | None = None) -> dict[str, Any]:
        with self._lock:
            if limit is not None and limit > 0 and after <= 0:
                start = max(0, len(self._events) - limit)
                events = self._events[start:]
            else:
                events = self._events[after:]
                if limit is not None and limit > 0:
                    events = events[:limit]
            cursor = len(self._events)
        return {"cursor": cursor, "events": events}

    def _drain_turn(self, turn_id: str) -> None:
        client = self._ensure_client()
        client.register_turn_notifications(turn_id)
        try:
            while True:
                notification = client.next_turn_notification(turn_id)
                payload = self._model_to_dict(notification.payload)
                self._record_event({"type": "codex_notification", "method": notification.method, "payload": payload})
                if notification.method == "turn/completed":
                    self._update_turn_status(turn_id, "turn_completed")
                    break
        except Exception as exc:  # noqa: BLE001
            self._record_event({"type": "runtime_error", "error": str(exc), "turn_id": turn_id, "status": "needs_repair"})
            self._update_turn_status(turn_id, "needs_repair")
        finally:
            client.unregister_turn_notifications(turn_id)

    def _ensure_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            from openai_codex.client import CodexClient, CodexConfig
        except ImportError as exc:
            raise RuntimeError("codex_unavailable: install the OpenAI Codex Python SDK or configure a Codex CLI runtime.") from exc
        root = self._project_root_provider()
        config = CodexConfig(
            cwd=str(root),
            client_name="research_os_desktop",
            client_title="Research OS Desktop",
            client_version="0.1.0",
            experimental_api=True,
        )
        self._client = CodexClient(
            config=config,
            approval_handler=lambda method, params: self._approval_service.request_approval(root, method, params),
        )
        self._client.start()
        self._client.initialize()
        self._record_event({"type": "codex_initialized", "payload": self.environment()})
        return self._client

    def _record_event(self, event: dict[str, Any]) -> None:
        event = redact_sensitive({"index": None, "timestamp": now_iso(), **event})
        with self._lock:
            event["index"] = len(self._events)
            self._events.append(event)
        try:
            append_jsonl(self._project_root_provider() / ".research-os" / "runtime_events.jsonl", event)
        except Exception:
            pass

    def _update_turn_status(self, turn_id: str, status: str) -> None:
        if self._on_turn_status is None:
            return
        try:
            self._on_turn_status(turn_id, status)
        except Exception as exc:  # noqa: BLE001
            self._record_event(
                {
                    "type": "runtime_status_sync_error",
                    "turn_id": turn_id,
                    "status": status,
                    "error": str(exc),
                }
            )

    def _sdk_available(self) -> bool:
        try:
            import openai_codex.client  # noqa: F401
            return True
        except ImportError:
            return False

    def _model_to_dict(self, value: Any) -> Any:
        if hasattr(value, "model_dump"):
            return value.model_dump(by_alias=True, mode="json", exclude_none=True)
        if hasattr(value, "dict"):
            return value.dict()
        if isinstance(value, dict):
            return {key: self._model_to_dict(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._model_to_dict(item) for item in value]
        if hasattr(value, "__dict__"):
            return {key: self._model_to_dict(item) for key, item in value.__dict__.items() if not key.startswith("_")}
        return value
