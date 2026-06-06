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

The stage sequence is:

`material_intake -> targeted_questions -> initialization -> research_kernel -> domain_or_general_route -> feasibility_or_evidence -> execution_harness -> analysis -> acceptance_gate -> next_loop_or_export`

- `material_intake`: use `research-os-copilot`; raw uploads stay private.
- `targeted_questions`: use `research-os-copilot`; ask exactly three targeted questions with recommended answer, options, and Other/free-form path.
- `initialization`: use `research-os-init`, with `research-os-alignment` and `research-os-evidence` as needed.
- `research_kernel`: use `research-os-research-kernel`; define candidate and evaluator contract before field routing.
- `domain_or_general_route`: inspect `domain_profiles/`; only then route to a domain skill.
- `feasibility_or_evidence`: use `research-os-feasibility-probe`, `research-os-evidence`, `research-os-live-evidence-refresh`, and `research-os-resource-guard` as needed.
- `execution_harness`: use `research-os-execution-harness`; experiment loops may be planned with `research-os-experiment-manager`, but execution still uses the harness.
- `analysis`: use `research-os-analysis`; preserve failures and negative results.
- `acceptance_gate`: use `research-os-alignment`; require human confirmation for scope, budget, privacy, dissemination, or external behavior changes.
- `next_loop_or_export`: loop through orchestrator again, or use public/paper/export skills only when enabled.

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

Use `research-os-copilot` when a researcher starts from `PUBLIC/copilot.html`, uploads material, pastes source links, or when `CONTROL/copilot_inbox/` contains a pending packet.

The route is:

`material_input -> save_intake -> pending_intake_analysis -> three targeted questions -> initialization report -> research-os-research-kernel -> domain profile -> execution harness`

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
