from __future__ import annotations

from typing import Any

from .common import append_jsonl, new_id, now_iso, read_json, write_json


DEFAULT_CHOICE_PROMPTS = [
    {
        "prompt_id": "CP-INITIALIZATION-RESEARCH-CLAIM",
        "stage": "initialization_intake",
        "question": "本轮初始化优先把研究主张定位成什么？",
        "recommended_option": "theorem_first",
        "why_recommended": "当前材料是理论初稿，先锁定可证明主张能降低后续写作和引用幻觉风险。",
        "options": [
            {
                "id": "theorem_first",
                "label": "定理主张优先",
                "description": "先明确模型、定理、证明义务和反例风险。",
                "is_recommended": True,
            },
            {
                "id": "venue_first",
                "label": "期刊适配优先",
                "description": "先判断 Neural Networks 的栏目、篇幅和写法是否匹配。",
            },
            {
                "id": "context_first",
                "label": "相关工作优先",
                "description": "先补算术电路、polynomial networks 和 approximation theory 语境。",
            },
        ],
        "free_form_enabled": True,
        "free_form_label": "自然语言补充",
        "free_form_placeholder": "补充你认为最重要的理论主张、风险或目标读者。",
        "requires_human_response": True,
    },
    {
        "prompt_id": "CP-INITIALIZATION-EVIDENCE",
        "stage": "initialization_intake",
        "question": "来源真实性核查应采用哪种严格度？",
        "recommended_option": "strict_online",
        "why_recommended": "投稿论文不能依赖记忆引用；每条引用都应有 DOI、arXiv、publisher 或官方页面。",
        "options": [
            {
                "id": "strict_online",
                "label": "逐条联网核查",
                "description": "所有投稿规则和引用都记录 URL、访问日期和可信来源。",
                "is_recommended": True,
            },
            {
                "id": "core_only",
                "label": "先核核心来源",
                "description": "先核期刊规则、模板和核心参考文献，次要文献后补。",
            },
            {
                "id": "local_first",
                "label": "先用本地材料",
                "description": "先整理本地 PDF/BibTeX，再统一联网补证据。",
            },
        ],
        "free_form_enabled": True,
        "free_form_label": "自然语言补充",
        "free_form_placeholder": "补充必须核查的网站、文献范围或不可接受来源。",
        "requires_human_response": True,
    },
    {
        "prompt_id": "CP-INITIALIZATION-FINAL-PACKAGE",
        "stage": "initialization_intake",
        "question": "最终投稿包默认应包含哪些交付物？",
        "recommended_option": "full_submission",
        "why_recommended": "Full Article 投稿需要正文、参考文献、声明、highlights、cover letter 和检查清单一起推进。",
        "options": [
            {
                "id": "full_submission",
                "label": "完整投稿包",
                "description": "LaTeX/PDF、appendix、bib、highlights、cover letter、source/proof audit。",
                "is_recommended": True,
            },
            {
                "id": "manuscript_first",
                "label": "正文优先",
                "description": "先把 main.tex 和 references.bib 做到可读可编译。",
            },
            {
                "id": "audit_first",
                "label": "审计优先",
                "description": "先完成证明审计和引用核查，再写完整正文。",
            },
        ],
        "free_form_enabled": True,
        "free_form_label": "自然语言补充",
        "free_form_placeholder": "补充你对投稿包、附录、图表或 rebuttal 记录的要求。",
        "requires_human_response": True,
    },
]


DEFAULT_SUBMISSION_WORKFLOW = {
    "target_venue": "Neural Networks",
    "article_type": "Full Article",
    "target_section": "Mathematical and Computational Analysis",
    "status": "paper_workflow_ready",
    "author_metadata": {
        "author": "Cheng Yinzhu",
        "corresponding_author": "Cheng Yinzhu",
        "affiliations": [
            "Renmin University of China",
            "Beijing Institute of Mathematical Sciences and Applications (BIMSA)",
        ],
        "funding": "none",
        "competing_interests": "none",
        "ai_declaration": "verify_current_elsevier_policy_before_finalizing",
    },
    "source_verification": [
        {
            "id": "SRC-GUIDE",
            "label": "Neural Networks Guide for Authors",
            "status": "needs_online_refresh",
            "required_evidence": "official guide URL, access date, article type, abstract/highlights/AI declaration rules",
        },
        {
            "id": "SRC-TEMPLATE",
            "label": "Elsevier LaTeX template and bibliography style",
            "status": "needs_online_refresh",
            "required_evidence": "official template URL, template package version or access date",
        },
        {
            "id": "SRC-REFERENCES",
            "label": "All manuscript references",
            "status": "needs_doi_arxiv_publisher_check",
            "required_evidence": "DOI, arXiv, publisher page, or other reliable source for every cited item",
        },
    ],
    "proof_audit": [
        {
            "id": "PROOF-MODEL",
            "label": "Quadratic network model and output-layer assumptions",
            "status": "needs_review",
        },
        {
            "id": "PROOF-GATES",
            "label": "Identity, addition, and multiplication gate validity under hidden-layer activation rules",
            "status": "needs_review",
        },
        {
            "id": "PROOF-BOUNDS",
            "label": "Depth and width bounds for monomials and full polynomials",
            "status": "needs_review",
        },
        {
            "id": "PROOF-NOVELTY",
            "label": "Novelty framing against arithmetic circuits, polynomial networks, and approximation theory",
            "status": "needs_review",
        },
    ],
    "review_rounds": [],
    "workflow_gaps": [],
}


class ResearchStateService:
    def __init__(self, project_root_provider) -> None:
        self._project_root_provider = project_root_provider

    def read_state(self) -> dict[str, Any]:
        root = self._project_root_provider()
        research_state = read_json(root / "PUBLIC" / "research_state.json", self._default_research_state())
        project_state = read_json(root / ".research-os" / "project.json", {})
        prompts = research_state.get("choice_prompts") or research_state.get("questions") or DEFAULT_CHOICE_PROMPTS
        if "submission_workflow" not in research_state:
            research_state["submission_workflow"] = DEFAULT_SUBMISSION_WORKFLOW
        return {
            "project": project_state,
            "research_state": research_state,
            "choice_prompts": prompts,
            "submission_workflow": research_state.get("submission_workflow", DEFAULT_SUBMISSION_WORKFLOW),
            "run_monitor": read_json(root / "PUBLIC" / "run_monitor.json", {"runs": []}),
            "archive_index": read_json(root / "PUBLIC" / "archive_index.json", {"archives": []}),
        }

    def submit_intake(self, payload: dict[str, Any]) -> dict[str, Any]:
        root = self._project_root_provider()
        session_id = payload.get("session_id") or new_id("INTAKE")
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
                "submission_workflow": state.get("submission_workflow", DEFAULT_SUBMISSION_WORKFLOW),
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
            "product_plan_id": new_id("FP"),
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
        if "paper" in selected:
            plan["tracks"]["paper"].update(
                {
                    "target_venue": "Neural Networks",
                    "article_type": "Full Article",
                    "target_section": "Mathematical and Computational Analysis",
                    "source_verification_required": True,
                    "proof_audit_required": True,
                    "review_rebuttal_required": True,
                }
            )
        write_json(root / "PUBLIC" / "final_product_plan.json", plan)
        state = read_json(root / "PUBLIC" / "research_state.json", self._default_research_state())
        state["macro_phase"] = "final_product"
        state["internal_phase"] = "final_product_selection"
        state["submission_workflow"] = state.get("submission_workflow", DEFAULT_SUBMISSION_WORKFLOW)
        state["updated_at"] = now_iso()
        write_json(root / "PUBLIC" / "research_state.json", state)
        return plan

    def submit_choice_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        root = self._project_root_provider()
        prompt_id = str(payload.get("prompt_id") or "").strip()
        option_id = str(payload.get("option_id") or "").strip()
        free_form = str(payload.get("free_form") or "")
        if not prompt_id or not option_id:
            raise ValueError("prompt_id and option_id are required.")
        response = {
            "response_id": new_id("CR"),
            "created_at": now_iso(),
            "prompt_id": prompt_id,
            "option_id": option_id,
            "free_form": free_form,
            "source": "desktop_app",
        }
        target = root / "CONTROL" / "choice_responses" / f"{response['response_id']}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        write_json(target, response)
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

    def record_workflow_gap(self, payload: dict[str, Any]) -> dict[str, Any]:
        root = self._project_root_provider()
        description = str(payload.get("description") or "").strip()
        severity = str(payload.get("severity") or "medium").strip() or "medium"
        source = str(payload.get("source") or "desktop_app").strip() or "desktop_app"
        if not description:
            raise ValueError("Workflow gap description is required.")
        record = {
            "gap_id": new_id("GAP"),
            "created_at": now_iso(),
            "severity": severity,
            "source": source,
            "description": description,
            "status": "recorded",
            "policy": "Fix app/workflow first when the gap blocks reusable paper progress.",
        }
        append_jsonl(root / "PROVENANCE" / "app_workflow_gaps.jsonl", record)
        state = read_json(root / "PUBLIC" / "research_state.json", self._default_research_state())
        workflow = state.get("submission_workflow", DEFAULT_SUBMISSION_WORKFLOW)
        gaps = list(workflow.get("workflow_gaps", []))
        gaps.append(record)
        workflow["workflow_gaps"] = gaps[-20:]
        state["submission_workflow"] = workflow
        state["updated_at"] = now_iso()
        write_json(root / "PUBLIC" / "research_state.json", state)
        return record

    def _default_research_state(self) -> dict[str, Any]:
        return {
            "schema_version": "research-state-v1",
            "macro_phase": "initialization",
            "internal_phase": "initialization_intake",
            "status": "ready_for_intake",
            "pending_user_confirmation": False,
            "choice_prompts": DEFAULT_CHOICE_PROMPTS,
            "submission_workflow": DEFAULT_SUBMISSION_WORKFLOW,
        }
