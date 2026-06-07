from __future__ import annotations

from typing import Any

from .common import append_jsonl, now_iso, read_json, write_json


DEFAULT_CHOICE_PROMPTS = [
    {
        "prompt_id": "CP-INITIALIZATION-TRACK",
        "stage": "initialization_intake",
        "question": "初始化时优先建立哪类研究启动包？",
        "recommended_option": "balanced",
        "why_recommended": "默认同时保留目标、证据和最小验证路径，适合多数早期研究。",
        "options": [
            {
                "id": "balanced",
                "label": "均衡启动",
                "description": "目标、证据、风险、最小验证同时建立。",
                "is_recommended": True,
            },
            {
                "id": "evidence_first",
                "label": "证据优先",
                "description": "先梳理文献、数据和可验证事实。",
            },
            {
                "id": "prototype_first",
                "label": "原型优先",
                "description": "先让 demo 或实验 harness 跑起来。",
            },
        ],
        "free_form_enabled": True,
        "free_form_label": "自然语言补充",
        "free_form_placeholder": "描述你的研究偏好、领域约束或已有材料。",
        "requires_human_response": True,
    }
]


class ResearchStateService:
    def __init__(self, project_root_provider) -> None:
        self._project_root_provider = project_root_provider

    def read_state(self) -> dict[str, Any]:
        root = self._project_root_provider()
        research_state = read_json(root / "PUBLIC" / "research_state.json", self._default_research_state())
        project_state = read_json(root / ".research-os" / "project.json", {})
        prompts = research_state.get("choice_prompts") or research_state.get("questions") or DEFAULT_CHOICE_PROMPTS
        return {
            "project": project_state,
            "research_state": research_state,
            "choice_prompts": prompts,
            "run_monitor": read_json(root / "PUBLIC" / "run_monitor.json", {"runs": []}),
            "archive_index": read_json(root / "PUBLIC" / "archive_index.json", {"archives": []}),
        }

    def submit_intake(self, payload: dict[str, Any]) -> dict[str, Any]:
        root = self._project_root_provider()
        session_id = payload.get("session_id") or f"INTAKE-{now_iso().replace(':', '').replace('-', '').split('.')[0]}"
        free_text = str(payload.get("free_text") or "")
        private_intake = root / "PRIVATE" / "intake" / session_id
        private_intake.mkdir(parents=True, exist_ok=True)
        if free_text.strip():
            (private_intake / "free_text.md").write_text(free_text, encoding="utf-8")

        packet = {
            "schema_version": "desktop-intake-v1",
            "session_id": session_id,
            "created_at": now_iso(),
            "free_text_present": bool(free_text.strip()),
            "free_text_summary": "Raw free text is stored under PRIVATE/intake/<session_id>/free_text.md.",
            "source_links": payload.get("source_links", []),
            "uploaded_files": payload.get("uploaded_files", []),
            "privacy_default": "private",
            "status": "pending_intake_analysis",
            "source": "desktop_app",
        }
        write_json(root / "CONTROL" / "intake_queue" / f"{session_id}.intake.json", packet)

        state = read_json(root / "PUBLIC" / "research_state.json", self._default_research_state())
        state.update(
            {
                "schema_version": "research-state-v1",
                "updated_at": now_iso(),
                "macro_phase": "initialization",
                "internal_phase": "initialization_intake",
                "status": "pending_intake_analysis",
                "active_session_id": session_id,
                "pending_user_confirmation": True,
                "choice_prompts": DEFAULT_CHOICE_PROMPTS,
                "intake_summary": {
                    "free_text_present": bool(free_text.strip()),
                    "free_text_summary": "Raw free text is private; summarized metadata is safe to render.",
                    "uploaded_file_count": len(payload.get("uploaded_files", [])),
                    "source_link_count": len(payload.get("source_links", [])),
                },
            }
        )
        write_json(root / "PUBLIC" / "research_state.json", state)
        append_jsonl(
            root / "PROVENANCE" / "run_manifest.jsonl",
            {
                "run_id": f"RUN-{session_id}",
                "timestamp": now_iso(),
                "status": "intake_saved",
                "privacy_level": "private_metadata_only",
                "outputs": ["PUBLIC/research_state.json", f"CONTROL/intake_queue/{session_id}.intake.json"],
            },
        )
        return {"packet": packet, "state": state}

    def select_final_products(self, tracks: list[str], free_form: str = "") -> dict[str, Any]:
        root = self._project_root_provider()
        allowed = {"paper", "report", "software"}
        selected = [track for track in tracks if track in allowed]
        if not selected:
            raise ValueError("At least one final product track is required.")
        plan = {
            "product_plan_id": f"FP-{now_iso().replace(':', '').replace('-', '').split('.')[0]}",
            "created_at": now_iso(),
            "phase": "final_product_selection",
            "selected_tracks": selected,
            "choice_prompts": [
                {
                    "prompt_id": "CP-FINAL-PRODUCT",
                    "purpose": "Select final product tracks and natural-language expectations.",
                }
            ],
            "tracks": {track: {"status": "selected"} for track in selected},
            "intermediate_artifact_policy": "preserve",
            "human_gates": ["public_export", "submission", "external_writeback", "software_release"],
            "user_free_form_expectations": free_form,
            "status": "approved",
        }
        write_json(root / "PUBLIC" / "final_product_plan.json", plan)
        return plan

    def submit_choice_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        root = self._project_root_provider()
        prompt_id = str(payload.get("prompt_id") or "").strip()
        option_id = str(payload.get("option_id") or "").strip()
        free_form = str(payload.get("free_form") or "")
        if not prompt_id or not option_id:
            raise ValueError("prompt_id and option_id are required.")
        response = {
            "response_id": f"CR-{now_iso().replace(':', '').replace('-', '').split('.')[0]}",
            "created_at": now_iso(),
            "prompt_id": prompt_id,
            "option_id": option_id,
            "free_form": free_form,
            "source": "desktop_app",
        }
        write_json(root / "CONTROL" / "choice_responses" / f"{response['response_id']}.json", response)
        state = read_json(root / "PUBLIC" / "research_state.json", self._default_research_state())
        state["updated_at"] = now_iso()
        state["last_choice_response"] = {
            "prompt_id": prompt_id,
            "option_id": option_id,
            "free_form_present": bool(free_form.strip()),
        }
        state["pending_user_confirmation"] = False
        write_json(root / "PUBLIC" / "research_state.json", state)
        return response

    def _default_research_state(self) -> dict[str, Any]:
        return {
            "schema_version": "research-state-v1",
            "macro_phase": "initialization",
            "internal_phase": "initialization_intake",
            "status": "ready_for_intake",
            "pending_user_confirmation": False,
            "choice_prompts": DEFAULT_CHOICE_PROMPTS,
        }
