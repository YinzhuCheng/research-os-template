from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import WORKSPACE_STATE_DIRNAME, now_iso, read_json, write_json
from .security import SECRET_RE, SecurityError, redact_sensitive


PROJECT_CONTEXT_SCHEMA_VERSION = "lcr-project-context-pack-v1"


class ProjectContextService:
    """Durable, lightweight project memory injected across thread switches.

    This is deliberately an index of project state, not a transcript archive.
    It keeps DS/Kimi/Yunwu oriented after switching threads, compacting, or
    restarting the sidecar without exposing raw runtime logs or secrets.
    """

    def __init__(self, project_service, dogfood_service=None, asset_registry_service=None, task_service=None) -> None:
        self._projects = project_service
        self._dogfood = dogfood_service
        self._assets = asset_registry_service
        self._tasks = task_service

    def snapshot(self, *, thread_id: str | None = None) -> dict[str, Any]:
        pack = self._build_pack(thread_id=thread_id)
        write_json(self._path(), pack)
        path = str(self._path())
        return {"context_pack": pack, "path": path, "context_pack_path": path}

    def context_inputs(self, *, thread_id: str | None = None) -> list[dict[str, Any]]:
        try:
            pack = self.snapshot(thread_id=thread_id)["context_pack"]
        except Exception:
            return []
        text = str(pack.get("text") or "").strip()
        if not text:
            return []
        return [{"type": "text", "text": text, "text_elements": []}]

    def record_runtime_notification(self, method: str, params: Any) -> None:
        if not isinstance(params, dict):
            return
        method = str(method or "")
        if method not in {
            "turn/plan/updated",
            "thread/goal/updated",
            "thread/goal/cleared",
            "thread/settings/updated",
            "thread/compacted",
            "thread/name/updated",
            "thread/started",
        }:
            return
        current = self._state()
        thread_id = self._thread_id_from_params(params)
        if not thread_id:
            return
        threads = dict(current.get("threads") or {})
        entry = dict(threads.get(thread_id) or {"thread_id": thread_id})
        if method == "turn/plan/updated":
            entry["latest_plan"] = {
                "turn_id": str(params.get("turnId") or ""),
                "explanation": params.get("explanation"),
                "steps": list(params.get("plan") or []),
                "updated_at": now_iso(),
            }
        elif method == "thread/goal/updated":
            entry["goal"] = params.get("goal") or {}
            entry["goal_updated_at"] = now_iso()
        elif method == "thread/goal/cleared":
            entry["goal"] = None
            entry["goal_updated_at"] = now_iso()
        elif method == "thread/settings/updated":
            entry["settings"] = dict(params.get("settings") or params)
            entry["settings_updated_at"] = now_iso()
        elif method == "thread/compacted":
            entry["last_compacted_at"] = now_iso()
            entry["compact"] = dict(params)
        elif method == "thread/name/updated":
            entry["name"] = params.get("threadName") or entry.get("name") or ""
        elif method == "thread/started":
            thread = dict(params.get("thread") or {})
            entry["name"] = thread.get("name") or entry.get("name") or ""
        entry["updated_at"] = now_iso()
        threads[thread_id] = entry
        current["threads"] = threads
        current["updated_at"] = now_iso()
        self._reject_secret_like(current)
        write_json(self._state_path(), current)

    def record_thread_hint(self, thread_id: str, patch: dict[str, Any]) -> None:
        if not str(thread_id or "").strip():
            return
        current = self._state()
        threads = dict(current.get("threads") or {})
        entry = dict(threads.get(thread_id) or {"thread_id": thread_id})
        allowed = {
            "name",
            "profile_id",
            "provider_id",
            "model",
            "reasoning_effort",
            "permission_mode",
            "collaboration_mode",
        }
        for key in allowed:
            if key in patch and patch.get(key) is not None:
                entry[key] = patch.get(key)
        entry["updated_at"] = now_iso()
        threads[thread_id] = entry
        current["threads"] = threads
        current["updated_at"] = now_iso()
        self._reject_secret_like(current)
        write_json(self._state_path(), current)

    def _build_pack(self, *, thread_id: str | None) -> dict[str, Any]:
        project = dict(self._projects.current_project or {})
        state = self._state()
        thread_cache = read_json(self._shell_root() / "thread_cache.json", {"by_id": {}})
        selected_thread_id = str(thread_id or project.get("current_thread_id") or "")
        thread_entry = self._thread_entry(selected_thread_id, state, thread_cache)
        recent_threads = self._recent_threads(project, state, thread_cache)
        task = self._task_summary()
        dogfood = self._dogfood_summary()
        assets = self._asset_summary()
        text = self._text(project, selected_thread_id, thread_entry, recent_threads, task, dogfood, assets)
        pack = {
            "schema_version": PROJECT_CONTEXT_SCHEMA_VERSION,
            "generated_at": now_iso(),
            "project": {
                "name": project.get("name") or "",
                "project_file": project.get("project_file") or "",
                "workspace_root": project.get("workspace_root") or "",
                "current_thread_id": selected_thread_id,
                "default_profile_id": project.get("default_profile_id") or "",
                "default_model": project.get("default_model") or "",
                "default_effort": project.get("default_effort") or "",
                "execution_host": dict(project.get("ui_preferences") or {}).get("execution_host") or "",
                "wsl_distro": dict(project.get("ui_preferences") or {}).get("wsl_distro") or "",
                "current_task_id": project.get("current_task_id") or "",
            },
            "task": task,
            "selected_thread": thread_entry,
            "recent_threads": recent_threads,
            "dogfood": dogfood,
            "assets": assets,
            "rules": [
                "Use this project context pack after thread switches, compact, fork, or sidecar restart.",
                "Do not read .lcr/runtime_events.jsonl or .lcr/approvals.jsonl unless the user explicitly asks.",
                "Use compact summaries, project_context_pack.json, asset_context_pack.json, screenshots, and manifests before raw logs.",
                "For public web research, prefer LCR built-in tools lcr_web_research_brief and lcr_web_search_batch; avoid raw curl, wget, or python urllib unless the LCR web tools fail or the user explicitly asks.",
                "When resuming another thread, verify the current thread id, goal, latest plan, and project files before editing.",
            ],
            "text": text[:8000],
        }
        self._reject_secret_like(pack)
        return pack

    def _text(
        self,
        project: dict[str, Any],
        thread_id: str,
        thread_entry: dict[str, Any],
        recent_threads: list[dict[str, Any]],
        task: dict[str, Any],
        dogfood: dict[str, Any],
        assets: dict[str, Any],
    ) -> str:
        lines = [
            "LCR Project Context Pack (auto-injected, secret-free)",
            "Freshness rule: this pack supersedes any older auto-injected LCR Project/Asset Context Pack text already present in the thread history.",
            "If counts, paths, goals, plans, or asset refs conflict, use this newest pack and the referenced JSON files.",
            f"Project: {project.get('name') or 'untitled'}",
            f"Workspace: {project.get('workspace_root') or ''}",
            f"Current task: {task.get('title') or task.get('task_id') or 'none'}",
            f"Current thread: {thread_id or 'none'}",
            f"Default runtime: profile={project.get('default_profile_id') or ''} model={project.get('default_model') or ''} effort={project.get('default_effort') or ''}",
        ]
        provider_threads = list(task.get("provider_threads") or [])
        if task:
            lines.append(
                "Task continuity: provider switches are internal handoffs within this same user-visible task; "
                "do not treat a provider-thread switch as a new objective."
            )
            if task.get("goal"):
                goal = task.get("goal")
                if isinstance(goal, dict) and goal.get("objective"):
                    lines.append(f"Task goal: {goal.get('objective')}")
                elif isinstance(goal, str):
                    lines.append(f"Task goal: {goal}")
            if task.get("plan"):
                plan = dict(task.get("plan") or {})
                steps = [str(item.get("step") or item) for item in list(plan.get("steps") or plan.get("plan") or [])[:6]]
                if steps:
                    lines.append("Task plan:")
                    lines.extend(f"- {step}" for step in steps)
            if provider_threads:
                lines.append("Provider threads for this task:")
                for item in provider_threads[:8]:
                    lines.append(
                        f"- {item.get('thread_id')} profile={item.get('profile_id') or ''} "
                        f"model={item.get('model') or ''} effort={item.get('reasoning_effort') or ''}"
                    )
            handoff_events = list(task.get("handoff_events") or [])
            if handoff_events:
                latest = dict(handoff_events[-1])
                lines.append(
                    f"Latest provider handoff: {latest.get('from_thread_id') or 'none'} -> {latest.get('to_thread_id') or ''} "
                    f"profile={latest.get('profile_id') or ''} model={latest.get('model') or ''} effort={latest.get('reasoning_effort') or ''}"
                )
        if thread_entry:
            lines.append(
                "Selected thread settings: "
                f"name={thread_entry.get('name') or ''} model={thread_entry.get('model') or ''} "
                f"effort={thread_entry.get('reasoning_effort') or ''} permission={thread_entry.get('permission_mode') or ''}"
            )
            goal = thread_entry.get("goal")
            if isinstance(goal, dict) and goal.get("objective"):
                lines.append(f"Selected thread goal: {goal.get('objective')}")
            latest_plan = thread_entry.get("latest_plan")
            if isinstance(latest_plan, dict):
                steps = [str(item.get("step") or item) for item in list(latest_plan.get("steps") or [])[:6]]
                if steps:
                    lines.append("Latest selected-thread plan:")
                    lines.extend(f"- {step}" for step in steps)
        if dogfood.get("enabled"):
            lines.append(
                f"Dogfood: phase={dogfood.get('phase')} status={dogfood.get('status')} provider={dogfood.get('current_provider')}"
            )
            if dogfood.get("goal"):
                lines.append(f"Dogfood goal: {dogfood.get('goal')}")
            if dogfood.get("next_step"):
                lines.append(f"Dogfood next step: {dogfood.get('next_step')}")
            if dogfood.get("latest_milestone"):
                milestone = dict(dogfood.get("latest_milestone") or {})
                lines.append(f"Latest milestone: {milestone.get('label')} status={milestone.get('status')}")
        if assets.get("total"):
            lines.append(
                f"Asset memory: total={assets.get('total')} promoted_or_in_use={assets.get('promoted_or_in_use')} "
                f"approved_unpromoted={assets.get('approved_unpromoted')} needs_review={assets.get('needs_review')}"
            )
            lines.append(f"Asset context: {assets.get('context_pack_path') or ''}")
        if recent_threads:
            lines.append("Recent threads:")
            for item in recent_threads[:8]:
                lines.append(
                    f"- {item.get('thread_id')} name={item.get('name') or ''} model={item.get('model') or ''} updated={item.get('updated_at') or ''}"
                )
        lines.extend(
            [
                "Rules:",
                "- Treat this pack as an orientation index, not as complete truth; inspect referenced project files before editing.",
                "- Context pack JSON paths are orientation references only; do not call MCP resources/read for them unless LCR explicitly exposes a matching MCP server.",
                "- Do not use generated/sliced assets in game code until they are promoted into the game manifest.",
                "- If context seems stale after thread switching, ask for or trigger a project-context refresh before continuing.",
                "- Ignore older auto-injected Project/Asset Context Pack blocks when this pack has a newer generated_at timestamp.",
                "- On provider handoff, continue the same task goal/plan/assets unless the user explicitly creates a new chat/task or fork branch.",
                "- For web research, use lcr_web_research_brief for multi-source briefs and lcr_web_search_batch for one or more search queries; do not run raw curl/wget/python HTTP loops unless those tools fail and you explain why.",
            ]
        )
        return "\n".join(lines)

    def _task_summary(self) -> dict[str, Any]:
        if self._tasks is None:
            return {}
        try:
            task = self._tasks.current_task()
        except Exception:
            return {}
        if not task:
            return {}
        keys = {
            "task_id",
            "title",
            "status",
            "handoff_policy",
            "active_provider_thread_id",
            "provider_threads",
            "handoff_events",
            "goal",
            "plan",
            "checkpoint_refs",
            "asset_context_refs",
            "updated_at",
        }
        compact = {key: task.get(key) for key in keys if key in task}
        compact["provider_threads"] = [self._compact_provider_thread(item) for item in list(compact.get("provider_threads") or [])[:10]]
        compact["handoff_events"] = [self._compact_handoff_event(item) for item in list(compact.get("handoff_events") or [])[-10:]]
        compact["checkpoint_refs"] = list(compact.get("checkpoint_refs") or [])[:10]
        return compact

    def _compact_provider_thread(self, item: Any) -> dict[str, Any]:
        if not isinstance(item, dict):
            return {}
        return {
            "thread_id": item.get("thread_id"),
            "profile_id": item.get("profile_id"),
            "provider_id": item.get("provider_id"),
            "model": item.get("model"),
            "reasoning_effort": item.get("reasoning_effort"),
            "permission_mode": item.get("permission_mode"),
            "role": item.get("role"),
            "updated_at": item.get("updated_at"),
        }

    def _compact_handoff_event(self, item: Any) -> dict[str, Any]:
        if not isinstance(item, dict):
            return {}
        return {
            "event_id": item.get("event_id"),
            "type": item.get("type"),
            "from_thread_id": item.get("from_thread_id"),
            "to_thread_id": item.get("to_thread_id"),
            "profile_id": item.get("profile_id"),
            "provider_id": item.get("provider_id"),
            "model": item.get("model"),
            "reasoning_effort": item.get("reasoning_effort"),
            "reused_existing": item.get("reused_existing"),
            "created_at": item.get("created_at"),
        }

    def _recent_threads(self, project: dict[str, Any], state: dict[str, Any], thread_cache: dict[str, Any]) -> list[dict[str, Any]]:
        by_id = {**dict(thread_cache.get("by_id") or {}), **dict(state.get("threads") or {})}
        ids = [str(item) for item in list(project.get("recent_threads") or []) if str(item).strip()]
        result = []
        for thread_id in ids:
            entry = dict(by_id.get(thread_id) or {"thread_id": thread_id})
            entry.setdefault("thread_id", thread_id)
            result.append(self._compact_thread_entry(entry))
        return result

    def _thread_entry(self, thread_id: str, state: dict[str, Any], thread_cache: dict[str, Any]) -> dict[str, Any]:
        if not thread_id:
            return {}
        entry = {
            **dict(thread_cache.get("by_id", {}).get(thread_id) or {}),
            **dict(state.get("threads", {}).get(thread_id) or {}),
        }
        entry.setdefault("thread_id", thread_id)
        return self._compact_thread_entry(entry)

    def _compact_thread_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        keys = {
            "thread_id",
            "name",
            "profile_id",
            "model",
            "reasoning_effort",
            "permission_mode",
            "collaboration_mode",
            "latest_plan",
            "goal",
            "last_compacted_at",
            "updated_at",
        }
        return {key: entry.get(key) for key in keys if key in entry}

    def _dogfood_summary(self) -> dict[str, Any]:
        if self._dogfood is None:
            return {"enabled": False}
        try:
            run = dict(self._dogfood.snapshot().get("run") or {})
        except Exception:
            return {"enabled": False, "status": "unavailable"}
        milestones = list(run.get("milestones") or [])
        captures = list(run.get("captures") or [])
        return {
            "enabled": bool(run.get("enabled")),
            "goal": str(run.get("goal") or "")[:1000],
            "phase": str(run.get("phase") or ""),
            "status": str(run.get("status") or ""),
            "current_provider": str(run.get("current_provider") or ""),
            "next_step": str(run.get("next_step") or "")[:1000],
            "budgets": run.get("budgets") or {},
            "usage": run.get("usage") or {},
            "latest_milestone": self._compact_milestone(milestones[-1]) if milestones else None,
            "latest_capture": self._compact_capture(captures[0]) if captures else None,
        }

    def _compact_milestone(self, milestone: Any) -> dict[str, Any] | None:
        if not isinstance(milestone, dict):
            return None
        return {
            "label": str(milestone.get("label") or "")[:240],
            "provider": str(milestone.get("provider") or "")[:80],
            "model": str(milestone.get("model") or "")[:120],
            "plan_step": str(milestone.get("plan_step") or "")[:240],
            "status": str(milestone.get("status") or "")[:80],
            "next_action": str(milestone.get("next_action") or milestone.get("next_step") or "")[:500],
            "created_at": str(milestone.get("created_at") or "")[:80],
        }

    def _compact_capture(self, capture: Any) -> dict[str, Any] | str | None:
        if isinstance(capture, str):
            return capture[:500]
        if not isinstance(capture, dict):
            return None
        return {
            "path": str(capture.get("path") or "")[:500],
            "label": str(capture.get("label") or "")[:160],
            "provider": str(capture.get("provider") or "")[:120],
            "created_at": str(capture.get("created_at") or "")[:80],
        }

    def _asset_summary(self) -> dict[str, Any]:
        if self._assets is None:
            return {}
        try:
            pack = self._assets.snapshot()
            context = pack.get("context_pack") or {}
            summary = dict((pack.get("registry") or {}).get("summary") or {})
            return {
                **summary,
                "summary": summary,
                "registry_path": pack.get("path"),
                "context_pack_path": context.get("context_pack_path"),
            }
        except Exception:
            return {"status": "unavailable"}

    def _thread_id_from_params(self, params: dict[str, Any]) -> str:
        thread_id = str(params.get("threadId") or params.get("thread_id") or "")
        if thread_id:
            return thread_id
        thread = params.get("thread")
        if isinstance(thread, dict):
            return str(thread.get("id") or thread.get("thread_id") or "")
        return ""

    def _state(self) -> dict[str, Any]:
        return dict(read_json(self._state_path(), {"schema_version": PROJECT_CONTEXT_SCHEMA_VERSION, "threads": {}}))

    def _path(self) -> Path:
        return self._shell_root() / "project_context_pack.json"

    def _state_path(self) -> Path:
        return self._shell_root() / "project_context_state.json"

    def _shell_root(self) -> Path:
        return self._projects.require_workspace_root() / WORKSPACE_STATE_DIRNAME

    def _reject_secret_like(self, payload: dict[str, Any]) -> None:
        serialized = str(redact_sensitive(payload))
        if SECRET_RE.search(serialized):
            raise SecurityError("Secret-like content is not allowed in project context pack records.")
