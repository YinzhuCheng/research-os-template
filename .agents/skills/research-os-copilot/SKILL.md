---
name: research-os-copilot
description: Run the desktop Research OS copilot workflow, including .rosproj intake, exactly three targeted initialization questions, sanitized research_state, choice prompts, and Codex confirmation queues.
---

# Research OS Copilot

Use this skill when the researcher starts or continues a `.rosproj` desktop project through the Tauri app, or when `CONTROL/intake_queue/` contains a pending desktop intake packet.

## Workflow

1. Read `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, `config/research_project.yaml`, and the latest sanitized packet from `CONTROL/intake_queue/`.
2. Do not read `PRIVATE/intake/` unless the active work order explicitly permits it.
3. Build a material profile from public metadata and any user-provided summary.
4. Ask exactly three targeted initialization questions. Each question must include a recommended option, concrete options, why it is recommended, and an Other/free-form path.
5. After the researcher answers, produce an initialization report with research goals, assumptions, candidate directions, minimum validation path, risks, and the next acceptance gate.
6. Update only sanitized state in `PUBLIC/research_state.json`; raw free text and uploaded material remain private at runtime.
7. Keep the loop strict: if the researcher rejects the previous artifact, revise the current artifact instead of advancing.

## Output Boundaries

- `PUBLIC/research_state.json`: sanitized app state for the desktop UI.
- `CONTROL/intake_queue/*.json`: sanitized intake packets waiting for Codex review.
- `CONTROL/choice_responses/*.json`: user choices and natural-language supplements.
- `PRIVATE/intake/<session_id>/`: raw runtime intake, never read unless permitted.

See `references/copilot_workflow.md` for the desktop state machine and UI-to-Codex contract.
