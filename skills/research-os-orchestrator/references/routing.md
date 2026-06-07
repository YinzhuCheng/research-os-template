# Routing Reference

Use `config/research_flow.yaml` as the canonical process contract. This file explains how to interpret it.

## Specification Priority

When instructions conflict, apply:

1. Latest user instruction.
2. `CONTROL/work_order.yaml` and `CONTROL/phase_gate.yaml`.
3. `AGENTS.md`.
4. `config/research_flow.yaml`.
5. `config/research_project.yaml` and schemas.
6. Current docs and dashboard.
7. Historical `PLAN/` and `PROVENANCE/` records.

## Canonical Stage Routing

The user-facing macro sequence is:

`initialization -> semi_automated_research_loop -> final_product`

The internal stage sequence is:

`initialization_intake -> loop_acceptance_gate -> loop_plan_alignment -> loop_user_decision -> loop_execute_analyze -> final_product_selection -> final_product_production -> export_release_gate`

- `initialization_intake`: use `research-os-copilot` and `research-os-init`; raw uploads stay private; ask exactly three targeted questions with recommended option, concrete options, and Other/free-form path.
- `loop_acceptance_gate`: use `research-os-alignment`; the researcher must accept the previous artifact before the loop advances.
- `loop_plan_alignment`: use `research-os-alignment` and `research-os-orchestrator`; propose the next plan and ask one to three high-impact choice prompts.
- `loop_user_decision`: use `research-os-orchestrator`; record selected options and free-form notes before changing work orders, phase gates, or domain routes.
- `loop_execute_analyze`: use `research-os-research-kernel` with harness, evidence, feasibility, resource, domain, and analysis skills as needed; preserve kernel objects and failed results.
- `final_product_selection`: use `research-os-final-product`; select paper, research report, software, or a multi-track combination with natural-language expectations.
- `final_product_production`: use `research-os-final-product` to route to paper, report, software, review/rebuttal, visual, polish, and export skills.
- `export_release_gate`: use `research-os-public-export`; require human confirmation for public export, submission, software release, external upload, or writeback.

## Domain Profile Routing

Use `research-os-research-kernel` before choosing a field-specific workflow. The kernel keeps `generate -> evaluate -> update -> human_gate` as the shared program, and `domain_profiles/` provides field-specific artifacts, reviewer taste, and quality gates. A domain profile is active only when the researcher selects it or the source material clearly requires it and the phase gate records that decision.

- `domain_profiles/fundamental-mathematics/`: route to `research-os-math-discovery`.
- `domain_profiles/applied-mathematics/`: route to `research-os-applied-math-modeling`.
- `domain_profiles/machine-learning/`: route to `research-os-ml-research-protocol`.
- `domain_profiles/computer-science/`: route to `research-os-cs-research-artifact`.
- `domain_profiles/statistics/`: route to `research-os-statistical-inference`.

After a domain skill produces a plan or artifact, return to the general Research OS chain as needed:
`research-os-evidence`, `research-os-feasibility-probe`, `research-os-resource-guard`, `research-os-execution-harness`, `research-os-analysis`, and `research-os-public-export`.

Field routing never bypasses the work order, phase gate, allowed paths, forbidden paths, manifest, ledger, or privacy scan.

## Browser Copilot Routing

Use `research-os-copilot` when a researcher starts from the desktop app, uploads or imports material, pastes source links, or when `CONTROL/intake_queue/` contains a pending packet.

The route is:

`material_input -> save_intake -> pending_intake_analysis -> three targeted questions -> initialization report -> loop_acceptance_gate -> loop_plan_alignment`

Rules:

- The first screen is material-first; do not ask the old five fixed questions.
- Generate exactly three targeted questions before initialization.
- Every question must include `recommended_answer`, options, and a free-form Other path.
- Raw uploads stay runtime-private; public state is sanitized.
- Experiments require a researcher-provided budget before minimum validation runs.
- Theory tracks should include definitions, candidate theorems, and proof or validation notes.

## Anti-Spaghetti Skill Rule

Do not add a skill to the main route unless it has:

- a kernel binding or explicit kernel exemption;
- schema or template support;
- validator coverage;
- `docs/doc_map.yaml` or documentation presence;
- `.agents/skills/` mirror consistency.

Do not let a skill become a hidden sub-router. If it starts deciding broad process stages, move that logic to `research-os-orchestrator` and `config/research_flow.yaml`.
