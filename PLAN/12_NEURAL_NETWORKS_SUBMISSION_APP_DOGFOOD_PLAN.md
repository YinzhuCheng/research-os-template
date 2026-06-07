# Research OS v4.4 Neural Networks Submission App Dogfooding Plan

## Status

| Step | Area | Status |
| --- | --- | --- |
| 1 | Land submission work order, phase gate, budget, and executable plan | completed |
| 2 | Fix app blockers for real paper workflow dogfooding | completed |
| 3 | Create `.rosproj` sandbox and import the neural-network materials through the app/sidecar path | completed |
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

- Desktop UI/test mojibake is fixed in app source and Playwright/Vitest mocks; `check_desktop_app.ps1` now blocks the known mojibake code points.
- The sidecar now exposes a submission workflow state object and app/workflow gap logging route, enough for the neural-network paper dogfooding pass.
- The runtime adapter now instructs Codex to inspect relevant skills, verify venue rules and citations online, and record app/workflow gaps before bypassing them.
- The manuscript draft currently proves exact polynomial representation for quadratic-activation networks, but venue fit, novelty framing, proof obligations, learning-theory context, and citation authenticity still need verification.
- Real project intake exposed four reusable app gaps and fixes: directory-level source import, Windows long-path copy support, collision-free IDs for rapid choice responses, and single-sidecar port protection.
- The private `.rosproj` sandbox was created under `PRIVATE/projects/neural-network-submission/`; raw inputs remain outside git and were imported through the app/sidecar path.
- The initialization path now returns exactly three paper-oriented choice prompts, matching the Research OS rule for material analysis.

## Step 1 Validation

- `git diff --check` passed.
- `scripts/validate_schemas.ps1` passed after correcting `privacy_level` to `mixed`.
- `scripts/check_resource_guard.ps1` passed.
- Commit pushed: `ff95bac v4.4: start Neural Networks submission dogfooding`.

## Step 2 Validation

- TypeScript `tsc --noEmit` passed with bundled Node.
- `scripts/check_desktop_app.ps1` passed with expanded mojibake guard.
- Sidecar unit tests passed: 8 tests.
- Vitest passed: 1 test.
- Playwright passed: 2 tests across desktop and narrow viewports.
- Vite production build passed.

## Step 3 Validation

- Created `neural-network-submission.rosproj` and initialized the private project sandbox through the sidecar.
- Imported 32 source files from the local `neural network/` directory through app/sidecar import paths; the final directory import preserved relative paths.
- Submitted the initialization intake and recorded three unique choice responses for research-claim framing, strict source verification, and full submission package scope.
- `git diff --check` passed.
- `scripts/validate_schemas.ps1` passed.
- `scripts/scan_privacy.ps1` passed.
- `scripts/check_desktop_app.ps1` passed.
- Sidecar unit tests passed: 11 tests.
- TypeScript `tsc --noEmit` passed with bundled Node.
- Vitest passed: 1 test.
- Playwright passed: 2 tests across desktop and narrow viewports.
- Vite production build passed.

## Deliverables

- A Research OS project sandbox for this paper with preserved raw inputs, interaction records, screenshots, archives, run manifests, and resource ledger entries.
- A submission-ready English LaTeX package for *Neural Networks*: main manuscript, appendix/supplement if needed, references, highlights, cover letter, checklist, source-verification report, proof-audit report, and AI/funding/COI/CRediT statements.
- App improvements that generalize to future paper projects: readable Chinese UI, paper-track workflow, import/source verification/proof audit/rebuttal records, and tests.
