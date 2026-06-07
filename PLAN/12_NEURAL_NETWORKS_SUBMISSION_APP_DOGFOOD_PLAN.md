# Research OS v4.4 Neural Networks Submission App Dogfooding Plan

## Status

| Step | Area | Status |
| --- | --- | --- |
| 1 | Land submission work order, phase gate, budget, and executable plan | in_progress |
| 2 | Fix app blockers for real paper workflow dogfooding | pending |
| 3 | Create `.rosproj` sandbox and import the neural-network materials through the app/sidecar path | pending |
| 4 | Run initialization, evidence refresh, proof audit, and acceptance-gated research loops | pending |
| 5 | Produce the Neural Networks Full Article package through the paper final-product track | pending |
| 6 | Run paid Yunwu `gpt-5.5` `xhigh` review/rebuttal rounds within USD 90-105 target range | pending |
| 7 | Validate, archive, package, record screenshots/provenance, commit, and push | pending |

## Operating Rule

Before each implementation step, reread this plan, inspect the current worktree, execute only the current step, update status and gap notes, validate the changed surface, inspect `git status`, then commit and push.

The implementation must stay app-first. If the paper cannot be improved comfortably through Research OS Desktop, fix the app or sidecar workflow first, then return to the manuscript. Direct hand edits to the manuscript are allowed only when they are performed as app/Codex outputs or when a small repair is needed to keep the app-driven flow moving.

## Target

- Source materials: local untracked `neural network/` directory.
- Target venue: *Neural Networks* Full Article.
- Target section: `Mathematical and Computational Analysis`.
- Author and corresponding author: Cheng Yinzhu.
- Affiliations: Renmin University of China; Beijing Institute of Mathematical Sciences and Applications (BIMSA).
- Funding: none.
- Competing interests: none.
- AI declaration: include only if required by the current official guide; verify online before final package.

## Budget And Resource Guard

- Yunwu budget is authorized for this work order with hard ceiling USD 105.
- Intended paid-review target spend is USD 90-105, using `gpt-5.5` with reasoning effort `xhigh`.
- Before any paid call, verify model availability, endpoint behavior, and usage/balance measurement with a small probe.
- If `gpt-5.5` or `xhigh` is unavailable, stop paid escalation and record the blocker rather than silently substituting a model.
- Store only redacted request/response records. Never persist API keys, Authorization headers, cookies, or platform tokens.

## Gap Audit

- The current desktop UI and tests still appear to contain Chinese mojibake in app-facing strings; fix before using screenshots or app-driven choices as evidence.
- The sidecar has intake and final-product primitives but lacks a first-class paper submission workflow view, source verification ledger, proof-audit ledger, and app bug/workflow-gap log.
- The runtime adapter can launch Codex SDK turns but the app does not yet provide enough structured prompts for literature verification, proof audit, and Neural Networks submission packaging.
- The manuscript draft currently proves exact polynomial representation for quadratic-activation networks, but venue fit, novelty framing, proof obligations, learning-theory context, and citation authenticity still need verification.

## Deliverables

- A Research OS project sandbox for this paper with preserved raw inputs, interaction records, screenshots, archives, run manifests, and resource ledger entries.
- A submission-ready English LaTeX package for *Neural Networks*: main manuscript, appendix/supplement if needed, references, highlights, cover letter, checklist, source-verification report, proof-audit report, and AI/funding/COI/CRediT statements.
- App improvements that generalize to future paper projects: readable Chinese UI, paper-track workflow, import/source verification/proof audit/rebuttal records, and tests.
