from __future__ import annotations

from pathlib import Path
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
            {"id": "balanced", "label": "均衡启动", "description": "目标、证据、风险、最小验证同时建立。", "is_recommended": True},
            {"id": "evidence_first", "label": "证据优先", "description": "先梳理文献、数据和可验证事实。"},
            {"id": "prototype_first", "label": "原型优先", "description": "先让 demo 或实验 harness 跑起来。"},
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
        public_state = read_json(root / "PUBLIC" / "copilot_state.json", {})
        project_state = read_json(root / ".research-os" / "project.json", {})
        return {
            "project": project_state,
            "copilot_state": public_state,
            "choice_prompts": public_state.get("questions") or DEFAULT_CHOICE_PROMPTS,
            "run_monitor": read_json(root / "PUBLIC" / "run_monitor.json", {"runs": []}),
            "archive_index": read_json(root / "PUBLIC" / "archive_index.json", {"archives": []}),
        }

    def submit_intake(self, payload: dict[str, Any]) -> dict[str, Any]:
        root = self._project_root_provider()
        session_id = payload.get("session_id") or f"INTAKE-{now_iso().replace(':', '').replace('-', '').split('.')[0]}"
        free_text = str(payload.get("free_text") or "")
        inbox = root / "PRIVATE" / "intake" / session_id
        inbox.mkdir(parents=True, exist_ok=True)
        if free_text.strip():
            (inbox / "free_text.md").write_text(free_text, encoding="utf-8")
        packet = {
            "schema_version": "v1.1",
            "session_id": session_id,
            "created_at": now_iso(),
            "free_text_present": bool(free_text.strip()),
            "free_text_summary": "Raw free text is stored under PRIVATE/intake/<session_id>/free_text.md.",
            "source_links": payload.get("source_links", []),
            "uploaded_files": payload.get("uploaded_files", []),
            "privacy_default": "private",
            "status": "pending_intake_analysis",
        }
        write_json(root / "CONTROL" / "copilot_inbox" / f"{session_id}.intake.json", packet)
        state = read_json(root / "PUBLIC" / "copilot_state.json", {})
        state.update(
            {
                "schema_version": "v1.1",
                "updated_at": now_iso(),
                "state": "pending_intake_analysis",
                "active_session_id": session_id,
                "pending_confirmation": True,
                "questions": DEFAULT_CHOICE_PROMPTS,
                "intake_summary": {
                    "free_text_present": bool(free_text.strip()),
                    "free_text_summary": "Raw free text is private; summarized metadata is safe to render.",
                    "uploaded_file_count": len(payload.get("uploaded_files", [])),
                    "source_link_count": len(payload.get("source_links", [])),
                },
            }
        )
        write_json(root / "PUBLIC" / "copilot_state.json", state)
        append_jsonl(root / "PROVENANCE" / "run_manifest.jsonl", {"run_id": f"RUN-{session_id}", "timestamp": now_iso(), "status": "intake_saved", "privacy_level": "private_metadata_only"})
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
            "choice_prompts": [{"prompt_id": "CP-FINAL-PRODUCT", "purpose": "Select final product tracks and natural-language expectations."}],
            "tracks": {track: {"status": "selected"} for track in selected},
            "intermediate_artifact_policy": "preserve",
            "human_gates": ["public_export", "submission", "external_writeback", "software_release"],
            "user_free_form_expectations": free_form,
            "status": "approved",
        }
        write_json(root / "PUBLIC" / "final_product_plan.json", plan)
        return plan
