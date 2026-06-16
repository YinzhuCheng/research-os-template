# Desktop Copilot Workflow

The desktop workflow is the only active Research OS copilot route:

`desktop_intake -> pending_intake_analysis -> three_targeted_questions -> initialization_report -> loop_acceptance_gate -> loop_plan_alignment -> loop_user_decision -> loop_execute_analyze -> final_product_selection`

The Tauri UI sends material and choices to the Python sidecar. The sidecar writes sanitized packets under `CONTROL/intake_queue/`, public state under `PUBLIC/research_state.json`, and raw user material under `PRIVATE/intake/<session_id>/`.

Codex reads only sanitized control packets unless a work order explicitly grants private intake access. Every user-facing choice must include a recommended option, concrete defaults, and natural-language free-form input.

The loop is acceptance-gated. If the researcher rejects an artifact, Codex revises the current artifact and does not advance to the next internal phase.
