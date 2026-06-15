from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import WORKSPACE_STATE_DIRNAME, new_id, now_iso, read_json, write_json
from .security import SECRET_RE, SecurityError, redact_sensitive


TASK_STATE_SCHEMA_VERSION = "lcr-task-state-v1"
DEFAULT_HANDOFF_POLICY = "multi_provider_handoff"


class TaskService:
    """User-facing task state over internal provider-specific Codex threads.

    A task is what the user perceives as one conversation or objective. Each
    task may use multiple internal Codex threads, one per provider/model route.
    Provider switching should therefore preserve the task and only change the
    active provider thread.
    """

    def __init__(self, project_service) -> None:
        self._projects = project_service

    def snapshot(self) -> dict[str, Any]:
        state = self._state()
        current = self.current_task()
        return {
            "schema_version": TASK_STATE_SCHEMA_VERSION,
            "current_task": current,
            "tasks": list(state.get("tasks") or []),
            "updated_at": state.get("updated_at"),
        }

    def ensure_default_task(self, *, thread_id: str | None = None, title: str | None = None, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        project = self._project()
        state = self._state()
        tasks = list(state.get("tasks") or [])
        current_task_id = str(project.get("current_task_id") or state.get("current_task_id") or "")
        task = self._find_task(tasks, current_task_id)
        if not task:
            task = self._new_task(title or project.get("name") or "New task")
            tasks.insert(0, task)
            current_task_id = str(task["task_id"])
        if thread_id:
            task = self._bind_thread_to_task(task, thread_id=thread_id, settings=settings or {}, role="provider", make_active=True)
        state["tasks"] = self._replace_task(tasks, task)
        state["current_task_id"] = current_task_id
        state["updated_at"] = now_iso()
        self._write_state(state)
        self._sync_project_current_task(task)
        return task

    def create_task(self, title: str | None = None, *, thread_id: str | None = None, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        task = self._new_task(title or "New task")
        if thread_id:
            task = self._bind_thread_to_task(task, thread_id=thread_id, settings=settings or {}, role="provider", make_active=True)
        state = self._state()
        tasks = [item for item in list(state.get("tasks") or []) if item.get("task_id") != task.get("task_id")]
        tasks.insert(0, task)
        state["tasks"] = tasks[:100]
        state["current_task_id"] = task["task_id"]
        state["updated_at"] = now_iso()
        self._write_state(state)
        self._sync_project_current_task(task)
        return task

    def switch_task(self, task_id: str) -> dict[str, Any]:
        state = self._state()
        tasks = list(state.get("tasks") or [])
        task = self._find_task(tasks, task_id)
        if not task:
            raise ValueError("Task not found.")
        task["updated_at"] = now_iso()
        state["tasks"] = self._replace_task(tasks, task)
        state["current_task_id"] = task["task_id"]
        state["updated_at"] = now_iso()
        self._write_state(state)
        self._sync_project_current_task(task)
        return task

    def update_current_task_title(self, title: str) -> dict[str, Any]:
        task = self.current_task()
        if not task:
            raise ValueError("No current task.")
        clean_title = str(title or "").strip()
        if not clean_title:
            raise ValueError("Task title cannot be empty.")
        redacted_title = str(redact_sensitive(clean_title)).strip()
        if SECRET_RE.search(redacted_title):
            raise SecurityError("Secret-like content is not allowed in task titles.")
        task["title"] = redacted_title[:160]
        task["updated_at"] = now_iso()
        self._save_task(task)
        return task

    def current_task(self) -> dict[str, Any] | None:
        project = self._project()
        state = self._state()
        task_id = str(project.get("current_task_id") or state.get("current_task_id") or "")
        task = self._find_task(list(state.get("tasks") or []), task_id)
        if task:
            return task
        return None

    def bind_thread(
        self,
        *,
        thread_id: str,
        settings: dict[str, Any] | None = None,
        role: str = "provider",
        title: str | None = None,
        make_active: bool = True,
    ) -> dict[str, Any]:
        task = self.ensure_default_task(title=title, settings=settings)
        task = self._bind_thread_to_task(task, thread_id=thread_id, settings=settings or {}, role=role, make_active=make_active)
        state = self._state()
        state["tasks"] = self._replace_task(list(state.get("tasks") or []), task)
        state["current_task_id"] = task["task_id"]
        state["updated_at"] = now_iso()
        self._write_state(state)
        self._sync_project_current_task(task)
        return task

    def find_provider_thread(
        self,
        *,
        profile_id: str | None,
        provider_id: str | None = None,
        model: str | None,
        effort: str | None,
    ) -> dict[str, Any] | None:
        task = self.current_task()
        if not task:
            return None
        desired_profile = str(profile_id or "")
        desired_provider = str(provider_id or "").strip().lower()
        desired_model = _canonical_model_key(model)
        desired_effort = _canonical_effort_key(effort)
        matches: list[dict[str, Any]] = []
        for item in list(task.get("provider_threads") or []):
            if item.get("missing_at"):
                continue
            item_profile = str(item.get("profile_id") or "")
            item_provider = str(item.get("provider_id") or "").strip().lower()
            if desired_profile and item_profile != desired_profile:
                if not desired_provider or item_provider != desired_provider:
                    continue
            elif not desired_profile and desired_provider and item_provider != desired_provider:
                continue
            if desired_model and _canonical_model_key(item.get("model")) != desired_model:
                continue
            if desired_effort and _canonical_effort_key(item.get("reasoning_effort")) != desired_effort:
                continue
            matches.append(dict(item))
        if not matches:
            return None
        matches.sort(key=lambda item: str(item.get("updated_at") or ""), reverse=True)
        return matches[0]

    def active_provider_thread(self) -> dict[str, Any] | None:
        task = self.current_task()
        if not task:
            return None
        active_thread_id = str(task.get("active_provider_thread_id") or "")
        for item in list(task.get("provider_threads") or []):
            if str(item.get("thread_id") or "") == active_thread_id:
                return dict(item)
        return None

    def needs_provider_handoff(self, *, thread_id: str | None, profile_id: str | None, model: str | None, effort: str | None) -> bool:
        if not thread_id:
            return False
        task = self.ensure_default_task(thread_id=thread_id)
        current = None
        for item in list(task.get("provider_threads") or []):
            if str(item.get("thread_id") or "") == str(thread_id):
                current = item
                break
        if not current:
            return False
        if not current.get("profile_id") and not current.get("model") and not current.get("reasoning_effort"):
            return False
        if profile_id and str(current.get("profile_id") or "") != str(profile_id):
            return True
        if model and _canonical_model_key(current.get("model")) != _canonical_model_key(model):
            return True
        if effort and _canonical_effort_key(current.get("reasoning_effort")) != _canonical_effort_key(effort):
            return True
        return False

    def record_provider_handoff(
        self,
        *,
        from_thread_id: str | None,
        to_thread_id: str,
        settings: dict[str, Any],
        reused_existing: bool,
    ) -> dict[str, Any]:
        task = self.bind_thread(thread_id=to_thread_id, settings=settings, role="provider", make_active=True)
        event = {
            "event_id": new_id("handoff"),
            "type": "provider_handoff",
            "handoff_policy": DEFAULT_HANDOFF_POLICY,
            "from_thread_id": from_thread_id,
            "to_thread_id": to_thread_id,
            "profile_id": settings.get("profile_id"),
            "provider_id": settings.get("provider_id"),
            "model": settings.get("model"),
            "reasoning_effort": settings.get("reasoning_effort"),
            "permission_mode": settings.get("permission_mode"),
            "reused_existing": reused_existing,
            "created_at": now_iso(),
        }
        handoff_events = list(task.get("handoff_events") or [])
        handoff_events.append(event)
        task["handoff_events"] = handoff_events[-80:]
        task["updated_at"] = now_iso()
        state = self._state()
        state["tasks"] = self._replace_task(list(state.get("tasks") or []), task)
        state["current_task_id"] = task["task_id"]
        state["updated_at"] = now_iso()
        self._write_state(state)
        self._sync_project_current_task(task)
        return event

    def mark_provider_thread_missing(self, thread_id: str, *, reason: str | None = None) -> None:
        clean_thread_id = str(thread_id or "").strip()
        if not clean_thread_id:
            return
        task = self.current_task()
        if not task:
            return
        updated = False
        provider_threads: list[dict[str, Any]] = []
        for item in list(task.get("provider_threads") or []):
            entry = dict(item)
            if str(entry.get("thread_id") or "") == clean_thread_id:
                entry["missing_at"] = now_iso()
                entry["missing_reason"] = str(reason or "app_server_thread_not_found")
                updated = True
            provider_threads.append(entry)
        if not updated:
            return
        task["provider_threads"] = self._prune_provider_threads(provider_threads)
        if str(task.get("active_provider_thread_id") or "") == clean_thread_id:
            task["active_provider_thread_id"] = None
        task["updated_at"] = now_iso()
        self._save_task(task)

    def record_goal(self, thread_id: str, goal: Any) -> None:
        task = self.ensure_default_task(thread_id=thread_id)
        task["goal"] = redact_sensitive(goal)
        task["updated_at"] = now_iso()
        self._save_task(task)

    def record_plan(self, thread_id: str, plan: dict[str, Any]) -> None:
        task = self.ensure_default_task(thread_id=thread_id)
        task["plan"] = redact_sensitive(plan)
        task["updated_at"] = now_iso()
        self._save_task(task)

    def record_checkpoint(self, checkpoint: dict[str, Any]) -> None:
        task = self.current_task()
        if not task:
            return
        refs = list(task.get("checkpoint_refs") or [])
        refs.insert(
            0,
            {
                "save_id": checkpoint.get("save_id"),
                "description": checkpoint.get("description") or checkpoint.get("default_description"),
                "created_at": checkpoint.get("created_at") or now_iso(),
            },
        )
        task["checkpoint_refs"] = refs[:40]
        task["updated_at"] = now_iso()
        self._save_task(task)

    def _new_task(self, title: str) -> dict[str, Any]:
        project = self._project()
        task_id = new_id("task")
        now = now_iso()
        return {
            "schema_version": TASK_STATE_SCHEMA_VERSION,
            "task_id": task_id,
            "project_id": project.get("project_id"),
            "title": str(title or "New task").strip() or "New task",
            "status": "active",
            "handoff_policy": DEFAULT_HANDOFF_POLICY,
            "active_provider_thread_id": None,
            "provider_threads": [],
            "fork_threads": [],
            "handoff_events": [],
            "goal": None,
            "plan": None,
            "checkpoint_refs": [],
            "asset_context_refs": [],
            "created_at": now,
            "updated_at": now,
        }

    def _bind_thread_to_task(
        self,
        task: dict[str, Any],
        *,
        thread_id: str,
        settings: dict[str, Any],
        role: str,
        make_active: bool,
    ) -> dict[str, Any]:
        clean_thread_id = str(thread_id or "").strip()
        if not clean_thread_id:
            return task
        now = now_iso()
        hint = self._thread_context_hint(clean_thread_id)
        prior_entry: dict[str, Any] = {}
        for item in list(task.get("provider_threads") or []):
            if str(item.get("thread_id") or "") == clean_thread_id:
                prior_entry = dict(item)
                break
        merged_settings = {
            **{key: value for key, value in prior_entry.items() if value is not None},
            **{key: value for key, value in hint.items() if value is not None},
            **{key: value for key, value in dict(settings or {}).items() if value is not None},
        }
        thread_entry = {
            "thread_id": clean_thread_id,
            "role": role or "provider",
            "profile_id": merged_settings.get("profile_id"),
            "provider_id": merged_settings.get("provider_id"),
            "model": merged_settings.get("model"),
            "reasoning_effort": merged_settings.get("reasoning_effort"),
            "permission_mode": merged_settings.get("permission_mode"),
            "collaboration_mode": merged_settings.get("collaboration_mode"),
            "name": merged_settings.get("name"),
            "updated_at": now,
        }
        existing = []
        created_at = now
        for item in list(task.get("provider_threads") or []):
            if str(item.get("thread_id") or "") == clean_thread_id:
                created_at = str(item.get("created_at") or now)
                continue
            existing.append(item)
        thread_entry["created_at"] = created_at
        existing.insert(0, thread_entry)
        task["provider_threads"] = self._prune_provider_threads(existing)
        if role == "fork":
            fork_threads = [item for item in list(task.get("fork_threads") or []) if str(item.get("thread_id") or "") != clean_thread_id]
            fork_threads.insert(0, thread_entry)
            task["fork_threads"] = fork_threads[:40]
        if make_active:
            task["active_provider_thread_id"] = clean_thread_id
        if task.get("goal") is None and hint.get("goal") is not None:
            task["goal"] = redact_sensitive(hint.get("goal"))
        if task.get("plan") is None and hint.get("latest_plan") is not None:
            task["plan"] = redact_sensitive(hint.get("latest_plan"))
        task["updated_at"] = now
        return task

    def _prune_provider_threads(self, provider_threads: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Keep task continuity records useful without accumulating stale missing threads."""
        active_missing_by_route: dict[tuple[str, str, str, str], int] = {}
        pruned: list[dict[str, Any]] = []
        for item in provider_threads:
            entry = dict(item)
            if entry.get("missing_at"):
                route_key = (
                    str(entry.get("profile_id") or ""),
                    str(entry.get("provider_id") or "").strip().lower(),
                    _canonical_model_key(entry.get("model")),
                    _canonical_effort_key(entry.get("reasoning_effort")),
                )
                count = active_missing_by_route.get(route_key, 0)
                if count >= 2:
                    continue
                active_missing_by_route[route_key] = count + 1
            pruned.append(entry)
        return pruned[:40]

    def _thread_context_hint(self, thread_id: str) -> dict[str, Any]:
        """Return secret-free task continuity hints for a known Codex thread."""
        if not thread_id:
            return {}
        shell_root = self._projects.require_workspace_root() / WORKSPACE_STATE_DIRNAME
        merged: dict[str, Any] = {}
        context_state = read_json(shell_root / "project_context_state.json", {})
        context_threads = context_state.get("threads") if isinstance(context_state, dict) else None
        if isinstance(context_threads, dict):
            context_entry = context_threads.get(thread_id)
            if isinstance(context_entry, dict):
                merged.update(context_entry)
        thread_cache = read_json(shell_root / "thread_cache.json", {})
        cache_entry = (thread_cache.get("by_id") or {}).get(thread_id) if isinstance(thread_cache, dict) else None
        if isinstance(cache_entry, dict):
            merged.update({key: value for key, value in cache_entry.items() if value is not None})
        provider_id = merged.get("provider_id")
        if not provider_id:
            model_text = str(merged.get("model") or "")
            if "/" in model_text:
                provider_id = model_text.split("/", 1)[0]
        return redact_sensitive(
            {
                "profile_id": merged.get("profile_id"),
                "provider_id": provider_id,
                "model": merged.get("model"),
                "reasoning_effort": merged.get("reasoning_effort"),
                "permission_mode": merged.get("permission_mode"),
                "collaboration_mode": merged.get("collaboration_mode"),
                "name": merged.get("name"),
                "goal": merged.get("goal"),
                "latest_plan": merged.get("latest_plan"),
            }
        )

    def _save_task(self, task: dict[str, Any]) -> None:
        state = self._state()
        state["tasks"] = self._replace_task(list(state.get("tasks") or []), task)
        state["current_task_id"] = task["task_id"]
        state["updated_at"] = now_iso()
        self._write_state(state)
        self._sync_project_current_task(task)

    def _sync_project_current_task(self, task: dict[str, Any]) -> None:
        active_thread = task.get("active_provider_thread_id")
        project = self._project()
        recent_tasks = [item for item in list(project.get("recent_tasks") or []) if isinstance(item, str) and item != task.get("task_id")]
        recent_tasks.insert(0, str(task.get("task_id")))
        patch = {
            "current_task_id": task.get("task_id"),
            "recent_tasks": recent_tasks[:50],
            "current_thread_id": active_thread,
        }
        recent_threads = [item for item in list(project.get("recent_threads") or []) if isinstance(item, str) and item != active_thread]
        if active_thread:
            recent_threads.insert(0, str(active_thread))
        patch["recent_threads"] = recent_threads[:20]
        self._projects.update_project(patch)

    def _replace_task(self, tasks: list[dict[str, Any]], task: dict[str, Any]) -> list[dict[str, Any]]:
        return [task, *[item for item in tasks if item.get("task_id") != task.get("task_id")]][:100]

    def _find_task(self, tasks: list[dict[str, Any]], task_id: str) -> dict[str, Any] | None:
        if not task_id:
            return None
        for task in tasks:
            if str(task.get("task_id") or "") == task_id:
                return dict(task)
        return None

    def _state(self) -> dict[str, Any]:
        state = dict(read_json(self._path(), {"schema_version": TASK_STATE_SCHEMA_VERSION, "current_task_id": None, "tasks": []}))
        state.setdefault("schema_version", TASK_STATE_SCHEMA_VERSION)
        state.setdefault("tasks", [])
        return state

    def _write_state(self, state: dict[str, Any]) -> None:
        self._reject_secret_like(state)
        write_json(self._path(), state)

    def _path(self) -> Path:
        return self._projects.require_workspace_root() / WORKSPACE_STATE_DIRNAME / "tasks.json"

    def _project(self) -> dict[str, Any]:
        project = self._projects.current_project
        if not project:
            raise ValueError("No project is open.")
        return dict(project)

    def _reject_secret_like(self, payload: dict[str, Any]) -> None:
        serialized = str(redact_sensitive(payload))
        if SECRET_RE.search(serialized):
            raise SecurityError("Secret-like content is not allowed in task records.")


def _canonical_model_key(model: Any) -> str:
    """Normalize display/provider-prefixed model ids for provider-thread reuse only."""
    text = str(model or "").strip().lower()
    if "/" in text:
        text = text.rsplit("/", 1)[-1]
    return text


def _canonical_effort_key(effort: Any) -> str:
    text = str(effort or "").strip().lower()
    if text == "max":
        return "xhigh"
    return text
