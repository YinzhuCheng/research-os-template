# Research OS Process Contract

This document is the human-readable companion to `config/research_flow.yaml`. The YAML file is the machine-readable source of truth.

## Canonical Flow

`material_intake -> targeted_questions -> initialization -> research_kernel -> domain_or_general_route -> feasibility_or_evidence -> execution_harness -> analysis -> acceptance_gate -> next_loop_or_export`

## Stage Contract

| Stage | Required skill | Output | Human gate |
| --- | --- | --- | --- |
| `material_intake` | `research-os-copilot` | intake packet and sanitized state | Reading private raw uploads or following external links. |
| `targeted_questions` | `research-os-copilot` | exactly three targeted questions | Researcher answers all three questions. |
| `initialization` | `research-os-init` | startup package and repository links | Budget, paper target, public export, or external resource assumptions. |
| `research_kernel` | `research-os-research-kernel` | candidate, evaluator contract, belief, trace, next action, human gate | Public claims, real resources, external writeback, phase changes. |
| `domain_or_general_route` | `research-os-orchestrator` | domain artifact plan and quality gates | Ambiguous domain or material plan change. |
| `feasibility_or_evidence` | `research-os-orchestrator` | feasibility probe, evidence map, live evidence refresh | Budget, real resource choices, time-sensitive unverified claims. |
| `execution_harness` | `research-os-execution-harness` | manifest, ledger, result artifacts | Credentials, paid resources, external writeback, unsafe code, budget overrun. |
| `analysis` | `research-os-analysis` | result interpretation and claim updates | Upgrading claims or changing next action policy. |
| `acceptance_gate` | `research-os-alignment` | accepted next action or revised plan | Scope, budget, privacy, dissemination, or external behavior changes. |
| `next_loop_or_export` | `research-os-orchestrator` | next loop or sanitized export | Public export, submission, external upload, paper route. |

## Skill Boundaries

- `research-os-orchestrator` routes and coordinates. It does not produce domain conclusions by itself.
- `research-os-copilot` manages material-first intake, the three-question protocol, and browser state. It does not authorize execution.
- `research-os-research-kernel` owns the shared generate/evaluate/update/human-gate state machine.
- Domain skills provide field-specific taste, artifacts, and quality gates only after a kernel candidate and evaluator exist.
- `research-os-experiment-manager` plans and supervises experiment loops; `research-os-execution-harness` enforces execution boundaries; `research-os-replay-eval-harness` handles reproducibility and post-run checks.
- `research-os-evidence` manages claim-evidence records; `research-os-live-evidence-refresh` handles current external evidence only when freshness matters.
- Paper, visual, polish, review, and export skills run only when the corresponding report, paper, or public export route is explicitly enabled.

## Anti-Spaghetti Rules

- Do not add a main-route skill unless it has schema/template support, validator coverage, doc-map presence, and skill mirror consistency.
- Do not let a domain skill bypass `research-os-research-kernel`.
- Do not let feasibility or experiment planning bypass `research-os-resource-guard` and `research-os-execution-harness`.
- Do not discard failed, null, partial, or inconclusive outcomes; preserve them as `search_trace` or `negative_result`.
- Do not use old fixed five-question intake. The current flow is material-first plus exactly three targeted questions.

## Phase Semantics

`CONTROL/phase_gate.yaml` records the current template/work-order phase. `config/research_project.yaml.current_phase` records the default project runtime phase for a new instantiated project. The process contract links them by defining which stage should handle the next action.
