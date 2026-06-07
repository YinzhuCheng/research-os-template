# Research OS Process Contract

This document is the human-readable companion to `config/research_flow.yaml`. The YAML file is the machine-readable source of truth.

## Canonical Flow

User-facing macro phases:

`initialization -> semi_automated_research_loop -> final_product`

Internal controlled stages:

`initialization_intake -> loop_acceptance_gate -> loop_plan_alignment -> loop_user_decision -> loop_execute_analyze -> final_product_selection -> final_product_production -> export_release_gate`

The macro phases are for the researcher and UI. The internal stages are for governance, audit, skill routing, and validators.

## Stage Contract

| Stage | Required skill | Output | Human gate |
| --- | --- | --- | --- |
| `initialization_intake` | `research-os-copilot` | intake packet, exactly three targeted questions, startup package | Reading private raw uploads, following external links, assuming budget, or assuming product targets. |
| `loop_acceptance_gate` | `research-os-alignment` | accepted artifact or revision request | The researcher must accept the previous artifact before the next step. Rejection blocks progression. |
| `loop_plan_alignment` | `research-os-orchestrator` | next-stage action proposal plus 1-3 high-impact choice prompts | Scope, budget, privacy, dissemination, or resource assumptions. |
| `loop_user_decision` | `research-os-alignment` | selected options, free-form notes, updated work order/phase gate | Ambiguous or conflicting researcher instructions. |
| `loop_execute_analyze` | `research-os-research-kernel` and `research-os-execution-harness` | candidate, evaluator, resources, audit, results, analysis, claim updates | Credentials, paid resources, unsafe code, external writeback, budget overrun, or public claims. |
| `final_product_selection` | `research-os-final-product` | multi-track final product plan | Selecting paper/report/software targets and any natural-language quality expectations. |
| `final_product_production` | `research-os-final-product` | paper, report, software package, or selected combination | Venue submission, public export, software release, or external upload. |
| `export_release_gate` | `research-os-public-export` | sanitized release/export decision and package | Public export, submission, external writeback, or release. |

`loop_execute_analyze` consolidates older `research_kernel`, `domain_or_general_route`, `feasibility_or_evidence`, `execution_harness`, and `analysis` UI stages. The old objects still exist inside candidate, evaluator, resource, and audit subrecords.

## Choice Prompt Contract

Every user-facing choice must include `recommended_option`, `options[]`, `free_form_enabled: true`, `free_form_label`, and `why_recommended`.
Initialization still asks exactly three targeted questions after material profiling.
Loop planning asks 1-3 high-impact alignment questions.
Final product selection supports paper, research report, software, or a multi-track combination.

## Skill Boundaries

- `research-os-orchestrator` routes and coordinates. It does not produce domain conclusions by itself.
- `research-os-copilot` manages material-first intake, the three-question protocol, and browser state. It does not authorize execution or final product release.
- `research-os-research-kernel` owns the shared generate/evaluate/update/human-gate state machine.
- Domain skills provide field-specific taste, artifacts, and quality gates only after a kernel candidate and evaluator exist.
- `research-os-experiment-manager` plans and supervises experiment loops; `research-os-execution-harness` enforces execution boundaries; `research-os-replay-eval-harness` handles reproducibility and post-run checks.
- `research-os-evidence` manages claim-evidence records; `research-os-live-evidence-refresh` handles current external evidence only when freshness matters.
- `research-os-final-product` selects and coordinates paper, report, and software tracks.
- `research-os-report-authoring` writes process-rich research reports with HTML, LaTeX/PDF, and PPT targets.
- `research-os-software-productization` turns a research result into stable, documented, user-friendly software while preserving intermediate artifacts.
- Paper, visual, polish, review/rebuttal, and export skills run only when the corresponding final product or public export route is explicitly enabled.

## Anti-Spaghetti Rules

- Do not add a main-route skill unless it has schema/template support, validator coverage, doc-map presence, and skill mirror consistency.
- Do not let a domain skill bypass `research-os-research-kernel`.
- Do not let feasibility or experiment planning bypass `research-os-resource-guard` and `research-os-execution-harness`.
- Do not discard failed, null, partial, or inconclusive outcomes; preserve them as `search_trace` or `negative_result`.
- Do not use old fixed five-question intake. The current flow is material-first plus exactly three targeted questions.
- Do not expose the retired `domain_or_general_route`, `feasibility_or_evidence`, `acceptance_gate`, or `next_loop_or_export` names as user-facing UI stages.
- Do not bypass `loop_acceptance_gate`: rejection means revise the current artifact, not plan the next step.
- Do not offer fixed-only choices. Recommended defaults must always be paired with natural-language Other/free-form input.

## Archive Contract

Git-backed archives are local project snapshots. The UI must collect a researcher description and show the current phase plus git status before creation.
Archive creation first commits the current snapshot when needed, then writes or appends `PROVENANCE/archive_index.jsonl` and refreshes the sanitized public index at `PUBLIC/archive_index.json`.
Archives must not include `PRIVATE/`, real credentials, cookies, tokens, authorization headers, or unsanitized raw material.

## Phase Semantics

`CONTROL/phase_gate.yaml` records the current template/work-order phase. `config/research_project.yaml.current_phase` records the default project runtime phase for a new instantiated project. The process contract links them by defining which stage should handle the next action.
