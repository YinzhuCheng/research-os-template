# Skills

`skills/` is the versioned source of Research OS repo skills. `.agents/skills/` is the repo-scoped Codex discovery mirror.

Use repo skills before generic Codex execution. The canonical process is defined in `config/research_flow.yaml`; this file is the human-readable trigger matrix.

## Main Trigger Matrix

| Situation | Required Skill | Inputs | Outputs | Boundary |
| --- | --- | --- | --- | --- |
| Route any Research OS task | `research-os-orchestrator` | work order, phase gate, project config, process contract | selected next skill and stage | Routes only; does not invent research conclusions. |
| Browser material intake or pending copilot packet | `research-os-copilot` | free text, source links, upload metadata, sanitized inbox packet | intake packet, exactly three targeted questions, initialization state | Does not execute uploads or approve work. |
| Import messy notes, plans, chats, PDFs, or demos | `research-os-init` | sanitized material summary and three answers | research brief, startup package, initial objects | Does not invent budget, venue, baseline, model, or dataset. |
| Align goals or resolve phase-gate ambiguity | `research-os-alignment` | brief, phase gate, work order, gap audit | alignment dossier and next decision | Clarifies intent; does not execute. |
| Normalize any substantive research loop | `research-os-research-kernel` | candidate idea or artifact, evidence, domain profile | candidate, evaluator contract, belief, trace, negative result, next action, human gate | Required before domain skill work. |
| Fundamental mathematics discovery | `research-os-math-discovery` | kernel candidate, math profile, examples/conjectures | conjecture cards, example banks, counterexample logs, proof-gap reports | Non-formal by default; no direct execution bypass. |
| Applied mathematics modeling | `research-os-applied-math-modeling` | kernel candidate, model assumptions, applied math profile | assumption ledgers, stability/error/sensitivity checks | Plans modeling; simulations need harness. |
| Machine learning protocol | `research-os-ml-research-protocol` | kernel candidate, ML profile, task/data context | task cards, data cards, baselines, ablations, leakage audits | No default dataset/model/budget. |
| Computer science artifact research | `research-os-cs-research-artifact` | kernel candidate, CS profile, artifact/system/algorithm context | specs, invariants, complexity, benchmarks, artifact-eval packs | Code execution and benchmarks need harness. |
| Statistical inference | `research-os-statistical-inference` | kernel candidate, estimand/design/model context | estimand cards, identification memos, diagnostics, uncertainty statements | Distinguish estimand, estimator, uncertainty, and sensitivity. |
| Define smallest useful validation | `research-os-feasibility-probe` | candidate, evaluator, resource boundary | feasibility probe and stop/continue policy | Requires researcher-provided resources. |
| Manage budgets and scarce resources | `research-os-resource-guard` | project budget, work order, planned action | resource guard decision | Required before spending, scaling, or real resource use. |
| Execute an approved work order | `research-os-execution-harness` | work order, phase gate, allowed paths, approved plan | manifest entry, ledger entry, result artifacts | Only execution boundary; must respect forbidden paths. |
| Plan or supervise experiment loops | `research-os-experiment-manager` | approved feasibility/experiment plan and budget | experiment cycle plan, checkpoints, stop rules | Supervises loops; actual execution still uses harness. |
| Replay or evaluate a run | `research-os-replay-eval-harness` | manifest, ledger, artifacts, logs | replay/eval notes and regression checks | Does not rewrite history or hide failures. |
| Link claims to evidence | `research-os-evidence` | claim matrix, literature/results, research brief | claim-evidence updates | Public claims need evidence links. |
| Refresh time-sensitive evidence | `research-os-live-evidence-refresh` | current-dependent claim or decision | source records and freshness risk | Uses current sources; does not replace expert review. |
| Analyze observed results | `research-os-analysis` | manifests, result files, claim matrix | result analysis, failure taxonomy, claim updates | Does not smooth away null or failed results. |
| Maintain docs/dashboard/doc map | `research-os-doc-site` | docs, dashboard, doc map, work order | updated offline docs and navigation | No private material, no remote assets by default. |
| Audit harness/control surfaces | `research-os-harness-audit` | AGENTS, Codex config, work order, phase gate, git state | audit report and required decisions | Audit only; no cleanup unless separately authorized. |
| Register external auto-research components | `research-os-integration-scout` | source URL, license, adapter intent | registry entry and risk boundary | Registry/adapters only; no vendoring by default. |
| Write a paper | `research-os-paper-authoring` | enabled dissemination target, claim matrix, results | LaTeX paper artifacts | Only when paper is explicitly enabled or requested. |
| Improve research visuals | `research-os-visual-communication` | figure/table/report/paper needs | figure plan or visual artifacts | Evidence figures must stay source-linked. |
| Polish/fact-check prose | `research-os-polish-factcheck` | manuscript/report and evidence matrix | polish report or edits | Only after a draft exists. |
| Review/rebuttal | `research-os-review-rebuttal` | paper/formal report draft and target venue | review matrix, rebuttal plan | Paper/formal report route only. |
| Public export | `research-os-public-export` | public export decision, PUBLIC/PROVENANCE | sanitized export package | Requires privacy scan and human approval. |

## Main-route Governance

A main-route skill must not be a loose prompt or isolated tool. Before it enters `research-os-orchestrator`, it needs:

- kernel binding or explicit kernel exemption;
- schema or template support;
- validator coverage;
- documentation or `docs/doc_map.yaml` presence;
- `.agents/skills/` mirror consistency.

## Install Or Mirror

```powershell
.\scripts\install_skills.ps1
.\scripts\sync_skill_mirror.ps1
.\scripts\check_skill_mirror.ps1
```
