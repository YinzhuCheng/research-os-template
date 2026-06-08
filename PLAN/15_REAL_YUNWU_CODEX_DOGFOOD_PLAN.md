# Research OS v4.7 Real Yunwu-Codex Dogfood Plan

## Summary

This plan supersedes the unfinished Step 5/6 path in `PLAN/14_ENGLISH_APP_SUBMISSION_DOGFOOD_PLAN.md`.

The current operator-assisted paper package is no longer treated as a valid final result. It is reclassified as entry material, together with the original `neural network/` folder, prior private draft project, txt/PPT notes, templates, example papers, venue instructions, screenshots, and QA reports.

The next valid route is a real Research OS Desktop dogfood run:

`Research OS Desktop UI -> Python sidecar -> Codex app-server/SDK -> Yunwu gpt-5.5 xhigh -> app artifact routes -> compile/review/acceptance gates`.

Codex must do the intelligent research and manuscript repair work through the app runtime. The human operator may only act as a realistic researcher with short instructions and as an app maintainer who fixes the workflow when the app blocks reusable progress.

## Hard Rules

- Re-read this plan, `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml` before each work step.
- After each completed implementation or workflow step: update this plan's status/gap audit, validate the touched surface, inspect `git status`, commit, and push.
- Do not call Yunwu before the app has an isolated Codex provider/profile path and redacted cost/provenance logging.
- Read `C:\Users\cyz19\Desktop\gptimg2.txt` only into process memory for authorized runtime use. Never write the key, Authorization header, token, cookie, or raw credential to repo, `.rosproj`, logs, screenshots, or raw request records.
- Do not commit raw `neural network/` material or `PRIVATE/` project contents.
- If Yunwu `gpt-5.5` with `model_reasoning_effort = "xhigh"` is unavailable or not OpenAI Responses-compatible through Codex, stop and report instead of silently falling back.
- Spend policy: target USD 90-105 if useful review/rebuttal signal continues, hard cap USD 200. Stop early if signal saturates or cost measurement becomes unsafe.
- Every paper change after this plan must be produced by app-driven Codex turns and written through legal app/sidecar artifact routes, except emergency diagnostics.
- Every discovered app/workflow gap must be recorded and fixed before bypassing it.

## Workflow

### Step 1 - Land Real Yunwu-Codex Governance

Status: completed

- Add this plan and mark v4.7 / `WO-0018` as the active route.
- Update work order, phase gate, and project metadata so the baseline paper package is entry material.
- Record that no new Yunwu call has happened in this step.
- Validate and commit/push.

### Step 2 - Implement Isolated Yunwu Codex Runtime

Status: completed

- Add sidecar support for app-owned isolated `CODEX_HOME` and profile files.
- Add a Yunwu provider profile with model `gpt-5.5`, provider `yunwu`, `model_reasoning_effort = "xhigh"`, `wire_api = "responses"`, and environment auth through `YUNWU_API_KEY`.
- Ensure provider/auth settings are never written to project `.codex/config.toml`.
- Surface runtime proof in the UI: provider, model, reasoning effort, isolated Codex home, and redacted cost state.
- Add tests for profile creation, secret rejection, config generation without key leakage, and runtime parameter propagation.
- Validate and commit/push.

### Step 3 - Prove Real Yunwu-Codex Turn

Status: pending

- Use the app runtime endpoint to start a Codex thread with Yunwu provider.
- Run one small proof turn that returns a structured status artifact through the app route.
- Confirm usage/cost using the documented Yunwu query service or another reliable measurement.
- Record redacted runtime events, cost, and screenshots.
- If the app-server/SDK cannot drive the provider, fix the app or stop with a precise blocker.
- Validate and commit/push.

### Step 4 - Fresh App Project Re-run

Status: pending

- Create a fresh private `.rosproj` sandbox.
- Import the original `neural network/` folder, prior private draft project, and current operator-assisted paper package as initialization material.
- Mark the current package as `operator_assisted_baseline_material`.
- Start initialization through real app/Codex runtime and answer exactly three targeted questions as a researcher with short answers.
- Accept or reject generated artifacts through app gates only.
- Capture screenshots and interaction records.
- Validate and commit/push public app/provenance changes only.

### Step 5 - App-Driven Research Loops

Status: pending

- Run Codex-driven source verification, proof audit, novelty positioning, theorem repair, citation audit, and venue-fit loops.
- Require online source verification for venue rules, AI policies, DOI/proceedings metadata, and cited claims.
- Record negative findings, uncertainty, and app gaps.
- Fix app/workflow gaps discovered during the loops.
- Validate and commit/push after meaningful checkpoints.

### Step 6 - App-Driven Paper Production And Yunwu Review

Status: pending

- Select the paper final-product track through the app.
- Use Codex/Yunwu turns for paper production, proof review, adversarial reviewer simulation, rebuttal planning, and editorial polish.
- Write manuscript, appendix, references, cover letter, highlights, declarations, checklist, source verification, and proof audit through app artifact routes.
- Compile and visually QA PDF after each substantial paper update.
- Continue review rounds while useful signal remains and measured cost remains below the hard cap.
- Validate and commit/push public app/provenance changes.

### Step 7 - Final Validation And Handoff

Status: pending

- Run local sidecar, frontend, schema, privacy, resource, desktop, LaTeX, citation, and source-verification checks.
- Create a private archive through the app.
- Produce a handoff report with final artifact paths, remaining human submission gates, cost summary, app fixes, and residual risks.
- Commit and push final public app/provenance updates.

## Current Gap Audit

- Current v4.6 paper artifacts are useful baseline material but were not produced by app-driven Codex runtime.
- Existing runtime code has a Codex SDK/app-server adapter shell, but it lacks isolated `CODEX_HOME`, durable provider config generation, Yunwu env-key injection, xhigh reasoning propagation, and reliable cost instrumentation.
- Existing profile metadata supports `custom_provider` but not enough validated fields for safe provider config generation.
- Previous Yunwu spending records include direct model calls, not proof that Research OS Desktop drove Codex through Yunwu.
- Step 2 added isolated app-owned `CODEX_HOME` config generation, a seeded Yunwu `gpt-5.5` xhigh profile, `wire_api = "responses"`, `env_key = "YUNWU_API_KEY"`, in-memory local key loading, runtime proof status in the UI, and tests proving no key is written to config files.
- Runtime can now prepare and display the intended Yunwu/Codex configuration, but the real paid app-server turn is still unproven until Step 3.
- Step 3 found an upgrade-path gap before any paid call: existing app profile stores that already contained `openai-account` did not receive the newly introduced `yunwu-gpt-55-xhigh` default profile. The sidecar now seeds missing built-in profiles idempotently while preserving user-defined profiles.
- Step 3 then found a runtime adapter compatibility gap: Codex app-server rejects the old camelCase sandbox enum `workspaceWrite` and expects `workspace-write`. The sidecar now uses app-server enum values for both thread and turn sandbox configuration, with regression coverage.
- Step 3 also found the matching approval-policy enum gap: Codex app-server rejects `unlessTrusted` and expects values such as `on-request`. The sidecar now uses `on-request` so approval requests still flow through the Research OS UI.

## Validation Log

- 2026-06-08T11:15:00+08:00: Step 1 completed. Added v4.7 / `WO-0018` governance and reclassified the current operator-assisted paper package as entry material. Validation passed: `git diff --check`, schema validation, resource guard, privacy scan, and desktop app checks. No Yunwu call, paid API, key read, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:20:00+08:00: Step 2 completed. Implemented isolated Research OS owned Codex runtime configuration, seeded Yunwu provider profile metadata, sidecar local-key loading into process memory, runtime parameter propagation, and UI runtime proof display. Validation passed: sidecar unittest (27 tests), Python `py_compile`, desktop app check, TypeScript, Vitest, and Vite build. No Yunwu call, paid API, key read, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:28:00+08:00: Step 3 checkpoint. Fixed the profile-store upgrade gap that prevented the app from exposing the Yunwu `gpt-5.5` xhigh profile when a user already had an older local profile store. Validation passed: sidecar unittest (28 tests), Python `py_compile`, and `git diff --check`. No Yunwu call, paid API, key read, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:41:00+08:00: Step 3 checkpoint. Fixed the Codex app-server sandbox enum mismatch by switching sidecar runtime parameters from `workspaceWrite` to `workspace-write`. Validation passed: sidecar unittest (28 tests), Python `py_compile`, and `git diff --check`. The failed `thread_start` was rejected during app-server request validation; no model turn, paid API usage, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:46:00+08:00: Step 3 checkpoint. Fixed the Codex app-server approval-policy enum mismatch by switching runtime parameters from `unlessTrusted` to `on-request`. Validation passed: sidecar unittest (28 tests), Python `py_compile`, and `git diff --check`. The failed `thread_start` was rejected during app-server request validation; no model turn, paid API usage, raw private material commit, public export, submission, or external writeback was used.
