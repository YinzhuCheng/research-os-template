# Routing Reference

## Language Mode

- `zh-first`: internal planning, logs, analysis, and audit are Chinese; formal paper follows venue language only when a paper target is explicitly enabled.
- `en-only`: all project materials should be English unless a source quote or data field requires another language.

## Intervention Level

- `low`: Codex proceeds within a phase, but pauses at phase gates and high-risk actions.
- `medium`: Codex also pauses for major protocols, core claims, dissemination structure, and important figures.
- `high`: Codex proposes every mutating work order and waits for approval before execution.

## Stage Routing

- `copilot_intake`: process material-first browser intake through `research-os-copilot`; do not use the retired fixed five-question intake.
- `initialization`: create config, research brief, alignment dossier, first work order.
- `research_kernel`: normalize substantive work into candidate, evaluator contract, evaluation result, belief state, search trace, negative result, next-action policy, and human judgment gate.
- `literature`: build literature matrix and evidence map.
- `protocol`: write experiments and stop conditions.
- `execution`: run work orders and record manifests.
- `analysis`: interpret results and update claim-evidence.
- `feasibility`: define and run a researcher-budgeted minimal feasibility probe.
- `evidence_refresh`: refresh time-sensitive literature, tool, policy, price, resource, or venue evidence.
- `paper`: build LaTeX paper, figures, appendix, and submission checklist only when requested.
- `review`: run adversarial review and rebuttal loops.
- `export`: sanitize and package public materials.

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
