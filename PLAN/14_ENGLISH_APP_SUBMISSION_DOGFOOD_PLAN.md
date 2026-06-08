# Research OS v4.6 English-App Neural Networks Submission Plan

## Summary

This plan supersedes `PLAN/13_APP_FIRST_REINITIALIZATION_DOGFOOD_PLAN.md` for the active neural-network paper workflow.

The current manuscript package is treated as an initial draft material bundle, not as an accepted final product. Research OS Desktop must run in English mode for this work so Chinese UI mojibake does not block the paper. The app must ingest the complete `neural network/` folder and the prior private draft-project artifacts, generate a structured research plan, run acceptance-gated research loops, and then produce a submission-ready paper package for *Neural Networks*.

The work has two equally important outcomes:

1. Bring the paper to a submission-ready state.
2. Improve Research OS Desktop so ordinary researchers can reproduce this path through app affordances, generated context, harness rules, structured research planning, source verification, screenshot/audit capture, and review/rebuttal loops instead of expert prompt craft.

## Hard Rules

- Re-read this plan, `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml` before each work step.
- After each completed step: update this plan's status/gap audit, validate the touched surface, inspect `git status`, commit, and push.
- Use English-mode app UI and English generated project context for this workflow. Chinese UI restoration is deferred unless a narrow issue blocks the English workflow.
- Treat previous manuscript, PDF, PPT, notes, BibTeX, templates, venue instructions, screenshots, reviews, and proof-audit files as initialization inputs until the app advances through gates.
- The app must reason over whole folders and preserve material manifests with file roles, hashes, exclusions, warnings, and provenance.
- Do not hand-edit the paper as the normal path. If paper content must change, improve or use the app/sidecar artifact route first.
- Common high-value prompts must be encoded in generated `AGENTS.md`, `CONTROL/project_context.md`, work orders, skills, or harness rules.
- Verify venue rules, AI disclosure requirements, source authenticity, and citation metadata online before finalizing.
- Do not invent citations, DOIs, theorem dependencies, proof claims, experiments, or venue policies.
- Yunwu API use is authorized up to USD 200 for this work order. Use `gpt-5.5` with `reasoning_effort: xhigh` for high-value proof review, novelty review, venue-fit review, rebuttal simulation, and polishing. Spend for signal; do not spend just to spend.
- Store only redacted API call records. Never store API keys, Authorization headers, cookies, account tokens, or real credentials.
- Keep screenshots and app interaction records in ignored/private artifact paths unless sanitized for public provenance.
- Do not commit raw `neural network/` materials or `PRIVATE/` project contents.

## Structured Research Plan Contract

The app-generated research plan must be visible to the researcher and include these sections:

- Research content and problem statement.
- Research motivation and venue fit.
- Expected results and contributions.
- Related literature and how the planned result differs from each source.
- Theoretical setup, definitions, assumptions, and conventions.
- Proof route for each main theoretical claim.
- Experiment or computational design if applicable, including expected small-scale preliminary results.
- Evidence and source-verification plan.
- Risk register covering proof gaps, novelty risk, citation risk, venue-fit risk, and app/workflow risk.
- Acceptance criteria for entering the final paper track.

Every plan question must use the Research OS choice-prompt contract: recommended option, concrete defaults, why recommended, and free-form input.

## Workflow

### Step 1 - Land v4.6 English-App Rules

Status: completed

- Add this plan and mark v4.6 as the active governance path.
- Update `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, `config/research_project.yaml`, and `AGENTS.md`.
- Keep existing v4.5 useful implementation work, but do not mix unfinished app-code changes into this governance commit.
- Validate schemas/resource guard/privacy where practical.
- Commit and push.

### Step 2 - Finish English-Mode Research Planning App Support

Status: completed

- Convert the active desktop paper workflow surfaces needed for this run to readable English.
- Finish the sidecar research-plan endpoint so the app can write `PUBLIC/research_plan.md/json` and move to `loop_acceptance_gate`.
- Ensure existing projects are upgraded with generated `AGENTS.md` and `CONTROL/project_context.md` on open, not only on creation.
- Ensure material import skips operational/build directories such as `.git`, `node_modules`, `dist`, `target`, and caches.
- Add tests and screenshots for the English research-plan workflow.
- Commit and push.

### Step 3 - Reinitialize The Neural-Network Project Through The App

Status: completed

- Create a fresh v4.6 `.rosproj` sandbox under `PRIVATE/projects/neural-network-submission/`.
- Import the full `neural network/` folder and the prior private draft project as initialization material.
- Submit intake through the app/sidecar path with the user's objective.
- Answer exactly three initialization questions as the researcher/operator.
- Generate and accept a structured research plan before paper rewriting.
- Capture app screenshots and interaction records.
- Commit and push only public app/provenance changes.

### Step 4 - Research Loop Before Final Product

Status: completed

- Use acceptance-gated loops for source verification, proof audit, novelty/venue-fit analysis, and claim-evidence matrix construction.
- Browse current official venue pages and source metadata where freshness matters.
- Record uncertain or negative findings rather than hiding them.
- Improve app/workflow gaps discovered during the run.
- Commit and push app/provenance changes.

### Step 4b - Repair Blocking Proof And Source Gaps

Status: completed

- Use the accepted Loop 1 audit as the governing diagnostic artifact.
- Repair the proof semantics by replacing ambiguous "available scalar" language with an affine-readable layer representation invariant.
- Reprove or weaken depth and width bounds before final-paper production.
- Expand direct novelty/source checks for polynomial neural networks, product-unit networks, quadratic activations, and arithmetic-circuit comparators.
- Extract the selected final manuscript citation set and verify every citation online.
- Commit and push app/provenance changes.

### Step 5 - Final Paper Production Through App Routes

Status: pending

- Enter final paper track only after the research plan, Loop 1 audit, and Step 4b repair artifacts are accepted.
- Produce the English LaTeX manuscript, appendix/supplement if needed, references, highlights, cover letter, declarations, checklist, source verification report, and proof audit report through sidecar artifact routes.
- Compile PDF, inspect logs, render screenshots, and run visual QA.
- Commit and push app/provenance changes, not private raw material.

### Step 6 - Yunwu High-Reasoning Review And Rebuttal Loops

Status: pending

- Measure available usage/cost before spending where possible.
- Use Yunwu `gpt-5.5` xhigh for proof review, venue novelty review, adversarial review, rebuttal planning, and editorial polish.
- Save redacted request/response records in private provenance.
- Apply justified changes through app/sidecar routes.
- Stop when feedback saturates or budget risk appears.
- Commit and push records and app fixes after meaningful rounds.

### Step 7 - Final Validation, Archive, And Handoff

Status: pending

- Run sidecar tests, desktop tests, schema checks, privacy scan, resource guard, LaTeX compile, citation/source verification, and UI screenshot walkthrough.
- Create a private git-backed archive through the app.
- Produce a handoff report listing final paper files, remaining non-technical submission gates, verified sources, Yunwu spend, app bugs fixed, and workflow gaps still open.
- Commit and push final public app/provenance updates.

## Current Gap Audit

- v4.5 correctly added whole-folder manifests and generated project context, and those should be kept.
- The active app workflow now uses readable English for the project center, material intake, acceptance gate, runtime stream, approval queue, archive panel, final-product modal, paper workflow panel, profile panel, and Playwright workflow tests.
- The sidecar now exposes a first-class research-plan write route that writes `PUBLIC/research_plan.md/json`, moves the project to `research_loop / loop_acceptance_gate`, and presents an English acceptance prompt.
- Existing projects are upgraded with generated `AGENTS.md` and `CONTROL/project_context.md` when opened, not only when created.
- Directory import now skips operational/build directories such as `.git`, `node_modules`, `dist`, `target`, and common caches.
- The generated project context now includes a structured theoretical-paper research-plan contract.
- English-mode screenshots were captured under ignored `apps/research-os-desktop/test-results/researcher-qa/v4.6-english/`.
- Step 3 created a fresh private project at `PRIVATE/projects/neural-network-submission/neural-network-v46-reinit-20260608-094813.rosproj`.
- The app/sidecar imported two material sources: the original `neural network/` folder and the prior private draft project. Aggregate manifest summary: 496 imported files, 445 excluded operational/secret-like files, two material imports.
- The app generated and accepted a structured research plan, then advanced to `research_loop / loop_plan_alignment` with prompt `CP-FIRST-RESEARCH-LOOP`.
- Real app screenshots for the private project were saved under `PRIVATE/projects/neural-network-submission/neural-network-v46-reinit-20260608-094813/PROVENANCE/app_screenshots/step3-reinitialization/`.
- Step 3 dogfooding found and fixed three app/workflow bugs: sidecar launcher could load stale installed code when using `python -m`, multiple material imports needed aggregate public summaries, and archive preview read stale seed config instead of runtime project phase. Windows long target paths in prior-project import also required long-path-safe directory creation.
- Step 4 added a first-class research-loop artifact route so source verification, proof audits, novelty positioning, and claim-evidence matrices can be written and accepted without prematurely moving the project to `final_product`.
- Step 4 Loop 1 verified official venue/policy pages and four starter references through DOI/Crossref, but recorded arXiv API 429 and full-reference extraction as unresolved checks.
- Step 4 Loop 1 found a blocking proof issue: the draft's gate language treats affine readouts as if they were hidden coordinates. The next loop must formalize affine-readable layer representation, repair gate lemmas, and rederive depth/width bounds before final-paper production.
- Step 4 dogfooding fixed the next-loop recommendation so accepted audit artifacts with blocking statuses recommend `repair_blocking_gaps`, not final paper production.
- Step 4 dogfooding also fixed stale research-plan messaging after plan acceptance; the UI now distinguishes pending acceptance from accepted-plan alignment.
- Step 4b repaired the proof route through an affine-readable layer representation invariant, closure lemmas for affine combinations/carry/product, a balanced product-tree construction, revised depth/width bounds, and vector-valued extension instructions.
- Step 4b expanded novelty positioning to direct polynomial/quadratic/product-unit comparators and added guardrails against optimality/lower-bound overclaims.
- Step 4b found and fixed a loop state-machine gap: after a researcher answers a next-loop planning prompt, the project now advances to `loop_execute_analyze` until artifacts are written back for acceptance.
- Step 4b accepted the repair artifact through the app; the current app recommendation is `enter_final_product_after_audit`.

## Validation Log

- 2026-06-08T09:08:01+08:00: Step 1 completed. Added the v4.6 English-app submission plan and updated AGENTS, work order, phase gate, and project metadata to use `en-only` for this workflow. Validation passed: `git diff --check` for touched governance files, `scripts/validate_schemas.ps1`, `scripts/check_resource_guard.ps1`, and `scripts/scan_privacy.ps1`. No Yunwu call, paid API, credential access, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T09:28:12+08:00: Step 2 completed. Converted the active desktop paper workflow surfaces to English, finished the research-plan endpoint and acceptance prompt, upgraded project-open context generation, skipped operational/build directories during material import, updated English tests and checks, and captured screenshots at `apps/research-os-desktop/test-results/researcher-qa/v4.6-english/`. Validation passed: `git diff --check`, `scripts/validate_schemas.ps1`, `scripts/scan_privacy.ps1`, `scripts/check_resource_guard.ps1`, `scripts/check_desktop_app.ps1`, sidecar unittest (17 tests), Python `py_compile`, TypeScript `tsc --noEmit`, Vitest, Playwright desktop/narrow workflow, and Vite production build. No Yunwu call, paid API, credential access, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T09:53:42+08:00: Step 3 completed. Used the current sidecar launcher to create and reopen a fresh private `.rosproj`, imported the full original material folder and prior draft project, submitted intake, answered exactly three initialization prompts, wrote the structured research plan through `/api/research-plan/write`, accepted it through the app gate, and captured real app screenshots. Dogfooding fixes added aggregate material-manifest summaries, long-path-safe import directory creation, acceptance-gate advancement to `loop_plan_alignment`, and archive-preview runtime phase reads. Validation passed: `git diff --check`, `scripts/validate_schemas.ps1`, `scripts/scan_privacy.ps1`, `scripts/check_resource_guard.ps1`, `scripts/check_desktop_app.ps1`, sidecar unittest (20 tests), Python `py_compile`, TypeScript `tsc --noEmit`, Vitest, Playwright desktop/narrow workflow, and Vite production build. No Yunwu call, paid API, credential access, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T10:23:52+08:00: Step 4 Loop 1 completed. Added `/api/research-loop-artifacts/write`, kept audit artifacts inside `research_loop`, displayed venue/source/proof/claim/novelty items in the paper workflow panel, and wrote accepted private loop artifacts for source verification, proof audit, claim-evidence, novelty positioning, and online-source records. Official online checks included the Neural Networks author guide, Elsevier LaTeX instructions, Elsevier generative-AI policy, Crossref DOI metadata for four starter references, and a recorded arXiv API 429 limitation. Validation passed: sidecar unittest (23 tests), Python `py_compile`, TypeScript `tsc --noEmit`, Vitest, Vite production build, `scripts/check_desktop_app.ps1`, and browser screenshot checks. No Yunwu call, paid API, credential access, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T10:38:10+08:00: Step 4b completed. Used the app choice prompt to select `repair_blocking_gaps`, fixed the sidecar state transition into `loop_execute_analyze`, wrote repaired proof/source/novelty artifacts through `/api/research-loop-artifacts/write`, accepted them through the loop artifact gate, and captured a private screenshot showing the final-product recommendation. Validation passed: sidecar unittest, Python `py_compile`, `scripts/check_desktop_app.ps1`, TypeScript `tsc --noEmit`, Vitest, Vite production build, privacy scan, resource guard, and schema validation. No Yunwu call, paid API, credential access, raw private material commit, public export, submission, or external writeback was used.
