# Research OS v4.5 App-First Reinitialization Dogfooding Plan

## Summary

This plan supersedes the active assumptions in `PLAN/12_NEURAL_NETWORKS_SUBMISSION_APP_DOGFOOD_PLAN.md`.

The existing neural-network manuscript package is now treated as an initial draft material bundle, not as an accepted final-product artifact. Research OS Desktop must ingest the whole `neural network/` folder and the prior private paper project artifacts as source material, profile the folder, ask exactly three targeted initialization questions, produce a research plan, run acceptance-gated research loops, and only then enter the final paper-production track.

Two outcomes are required:

1. Bring the neural-network paper to a submission-ready level for *Neural Networks*.
2. Improve Research OS Desktop so a researcher with ordinary prompts can reproduce this workflow through app affordances, generated project context, skills, harness rules, source verification, review/rebuttal loops, screenshots, and audit records.

## Hard Rules

- Re-read this plan, `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml` before every implementation step.
- After every completed step, update this plan's status/gap audit, validate the changed surface, inspect `git status`, commit, and push.
- Treat previous manuscript, PDF, PPT, notes, BibTeX, templates, venue instructions, screenshots, reviews, and proof-audit files as initialization inputs until the app explicitly advances through the stage gates.
- The app must consider whole folders, not only the obvious manuscript draft. Intake must preserve a folder manifest, file roles, provenance, and missing/ambiguous-file warnings.
- Do not hand-edit the paper as the normal path. If paper content must change, use or improve the app/sidecar artifact route first.
- Any prompt that future researchers will routinely need must be encoded in app-generated project context, `AGENTS.md`, skills, work orders, or system/developer instructions, not left as user prompt burden.
- Every generated `.rosproj` project must include durable context rules telling Codex to use repo skills first, verify online sources, avoid hallucinated citations, preserve folder-wide evidence, and record app/workflow gaps.
- Use online verification for venue rules, citation metadata, source authenticity, and AI-use disclosure requirements before finalizing the paper.
- Yunwu API use is authorized up to USD 200 for this work order. Use `gpt-5.5` with `reasoning_effort: xhigh` for high-value review/rebuttal and paper-improvement loops, but do not burn budget without useful signal.
- Store only redacted API call records. Never store API keys, Authorization headers, cookies, or real credentials.
- Keep screenshots and app interaction records in ignored/private artifact paths unless they are sanitized and intentionally moved to public provenance.
- Do not commit raw `neural network/` materials or `PRIVATE/` project contents.

## Revised Workflow

### Step 1 - Land Revised Rules And Control Plane

Status: completed

- Create this plan.
- Update `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml` to v4.5.
- Update `AGENTS.md` with durable app-first dogfooding and generated-context rules.
- Fix obvious process-contract mojibake that could leak into app context.
- Validate schemas/resource guard/privacy where practical.
- Commit and push.

### Step 2 - App Intake Must Understand Whole Folders

Status: completed

- Inspect current sidecar import/intake/project seed services.
- Add or improve a folder manifest service that records all files, relative paths, roles, sizes, hashes, provenance, and excluded private/sensitive paths.
- Make initialization summarize the whole material bundle: manuscript draft, PDF/PPT/notes, templates, venue instructions, example papers, references, proof audits, screenshots, and prior app logs.
- Surface the manifest and missing/ambiguous-file warnings in the app UI.
- Add tests showing the app does not choose only `main.tex` when multiple relevant files exist.
- Commit and push.

### Step 3 - Generate Strong Project Context Automatically

Status: completed

- Improve project creation so each `.rosproj` sandbox receives an app-generated `AGENTS.md` or equivalent context pack.
- Include mandatory skill routing, source verification, whole-folder intake, stage gates, privacy, resource guard, hallucinated-citation prevention, reviewer-loop expectations, and app-gap logging.
- Add sidecar tests confirming the generated context exists and contains the required rules.
- Commit and push.

### Step 4 - Reinitialize The Neural-Network Project Through The App

Status: pending

- Treat the current private paper package and original `neural network/` folder as intake material.
- Use the app/sidecar path to import or re-index the full material bundle.
- Generate exactly three targeted initialization questions, each with a recommended option, defaults, and free-form input.
- Answer them as the researcher/operator according to the user's objective.
- Produce a research plan before any final-product writing.
- Record screenshots and app interaction logs.
- Commit and push only public/app/provenance updates; do not commit raw private material.

### Step 5 - Research Loop Before Final Product

Status: pending

- Build or improve app support for an acceptance-gated loop: artifact acceptance, next plan, user decision, execution, analysis.
- Run the neural-network manuscript through source verification, proof audit, novelty/venue-fit analysis, and claim-evidence matrix updates.
- Use live web verification for references and venue rules.
- Record negative or uncertain findings instead of hiding them.
- Commit and push app/workflow improvements and public provenance.

### Step 6 - Final Paper Production

Status: pending

- Only after accepted research-plan and analysis gates, enter final product paper track.
- Generate or revise the English LaTeX manuscript, appendix, references, highlights, cover letter, declarations, checklist, source verification report, and proof audit report through sidecar artifact routes.
- Compile PDF, inspect logs, render screenshots, and run visual QA.
- Record final app interaction screenshots and archive records.
- Commit and push public/app/provenance updates.

### Step 7 - Yunwu High-Reasoning Review And Rebuttal Loops

Status: pending

- Use Yunwu `gpt-5.5` with `xhigh` reasoning for proof review, novelty/venue fit, adversarial reviewer simulation, rebuttal planning, editorial polish, and final submission gate.
- Measure cost before and after batches using the best available Yunwu usage tool.
- Keep calls redacted and focused on sanitized manuscript/review text.
- Stop when feedback saturates or hard budget risk appears; do not spend just to spend.
- Apply justified revisions through the app/sidecar artifact route.
- Commit and push records and app fixes after meaningful rounds.

### Step 8 - Final Validation, Archive, And Handoff

Status: pending

- Run sidecar tests, desktop tests, schema checks, privacy scan, resource guard, LaTeX compile, citation/source verification, and UI walkthrough screenshots.
- Create a final private git-backed archive through the app.
- Produce a concise handoff report identifying:
  - final paper files,
  - remaining non-technical submission gates,
  - verified sources,
  - Yunwu spend,
  - app bugs fixed,
  - workflow gaps still open.
- Commit and push final public/app/provenance updates.

## Current Gap Audit

- The previous v4.4 workflow incorrectly treated an improved manuscript package as if it were already a final-product artifact.
- The app now has a folder manifest path: directory import records roles, hashes, target paths, exclusions, role counts, and warnings; `/api/state` exposes a public summary and the UI renders it in the materials panel.
- New projects now receive generated `AGENTS.md` and `CONTROL/project_context.md` context packs that instruct Codex to use skills, inspect whole-folder manifests, verify sources, avoid hallucinated citations, preserve provenance, respect gates, and record app/workflow gaps.
- The app must expose a clearer distinction between "draft material", "accepted research artifact", and "final product".
- The app and governance should keep the successful v4.4 fixes: controlled paper artifact writes, control-character guard, phase synchronization, profile UI text guard, screenshots, private archives, and redacted Yunwu records.

## Validation Log

- 2026-06-08T08:26:41+08:00: Step 1 completed. `git diff --check`, `scripts/validate_schemas.ps1`, `scripts/check_resource_guard.ps1`, `scripts/scan_privacy.ps1`, `scripts/check_desktop_app.ps1`, and `scripts/check_research_flow.ps1` passed. No raw private paper material, API key, Authorization header, cookie, or external writeback was introduced.
- 2026-06-08T08:47:51+08:00: Step 2 completed. Added sidecar whole-folder material manifests, public manifest summaries, state exposure, app material-import UI, readable Chinese app copy, manifest role/warning UI, and regression checks. Validation passed: `git diff --check`, `scripts/validate_schemas.ps1`, `scripts/scan_privacy.ps1`, `scripts/check_desktop_app.ps1`, sidecar unittest (16 tests), TypeScript `tsc --noEmit`, Vitest, Vite production build, and an HTTP sidecar endpoint smoke test that created a temporary project, imported a multi-file material folder, and read manifest roles through `/api/state`.
- 2026-06-08T08:54:51+08:00: Step 3 completed. Project creation now overwrites generated project `AGENTS.md` and writes `CONTROL/project_context.md`; runtime developer instructions now tell Codex to read both context files and inspect whole-folder material manifests. Validation passed: sidecar unittest (16 tests), `scripts/check_desktop_app.ps1`, `scripts/validate_schemas.ps1`, `scripts/scan_privacy.ps1`, `py_compile`, and `git diff --check`.
