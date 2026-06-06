---
name: research-os-copilot
description: Run the material-first Codex Browser Copilot workflow for Research OS, including intake packets, exactly three targeted questions, initialization reports, sanitized dashboard state, and browser-to-Codex confirmation queues.
---

# Research OS Copilot

Use this skill when the researcher wants to start or continue a Research OS project through the browser cockpit at `PUBLIC/copilot.html`, or when a pending copilot intake packet appears in `CONTROL/copilot_inbox/`.

## Workflow

1. Read `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, `config/research_project.yaml`, and `docs/doc_map.yaml`.
2. Read the latest sanitized intake packet from `CONTROL/copilot_inbox/`. Do not read `PRIVATE/intake/` unless the active work order explicitly permits it.
3. Classify the material as one of: `theory`, `experiment`, `theory_and_experiment`, `engineering_system`, `survey`, or `unclear`.
4. Generate exactly three targeted questions. Every question must include:
   - `reason_for_asking`
   - `recommended_answer`
   - selectable `options`
   - a free-form `Other` answer path
   - `plan_impact`
5. After the researcher answers, produce a `copilot_initialization_report` with:
   - research motivation
   - expected goals
   - contribution claims
   - related work, shortcomings, and relationship to this research
   - reference links and legal download policy
   - theory track when the project is theory-heavy
   - experiment track and minimum validation when the project has experiments
   - repository resource links
6. Bind the initialization report to `research-os-research-kernel` before any substantive execution. Candidate claims, evaluation contracts, search traces, negative results, and human gates must remain first-class objects.
7. Update only sanitized public state in `PUBLIC/copilot_state.json`; raw uploaded material remains private at runtime.

## Guardrails

- Do not ask the old fixed five intake questions.
- Do not silently ask more than three pre-initialization questions.
- Do not initialize an experiment plan with concrete spending until the researcher provides a budget.
- Do not bypass paywalls or download restricted paper full text.
- Do not external-write, publish, submit, or call paid resources without explicit confirmation.
- Do not move raw upload content into `PUBLIC/`, `docs/`, or git-tracked provenance.

## Outputs

- Intake packet: `config/schemas/copilot_intake.schema.json`
- Question packet: `config/schemas/copilot_questions.schema.json`
- Initialization report: `config/schemas/copilot_initialization_report.schema.json`
- Browser state: `PUBLIC/copilot_state.json`
- Runtime queue: `CONTROL/copilot_inbox/*.json`

See `references/copilot_workflow.md` for the full state machine and browser bridge contract.
