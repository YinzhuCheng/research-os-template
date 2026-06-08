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

Status: completed

- Use the app runtime endpoint to start a Codex thread with Yunwu provider.
- Run one small proof turn that returns a structured status artifact through the app route.
- Confirm usage/cost using the documented Yunwu query service or another reliable measurement.
- Record redacted runtime events, cost, and screenshots.
- If the app-server/SDK cannot drive the provider, fix the app or stop with a precise blocker.
- Validate and commit/push.

### Step 4 - Fresh App Project Re-run

Status: completed

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
- Step 3 further found that Codex app-server uses different sandbox enum shapes for thread start versus turn start: `thread_start.sandbox` expects `workspace-write`, while `turn_start.sandboxPolicy.type` expects `workspaceWrite`. The adapter now handles this split explicitly.
- Step 3 proved the real app-driven route with a completed Codex turn through `modelProvider=yunwu`, `model=gpt-5.5`, `reasoningEffort=xhigh`; measured Yunwu cost was approximately USD `0.0000114232`.
- Step 3 found and fixed a telemetry redaction gap: numeric `tokenUsage` was being redacted because its field name contains `token`. Runtime redaction now preserves numeric usage telemetry while still redacting real Authorization headers, API keys, cookies, passwords, secrets, and token strings.
- Step 4 created the fresh private neural-network `.rosproj`, imported the original source folder, prior private draft project, and operator-assisted baseline as entry material, answered exactly three initialization questions through app routes, ran a real Yunwu-backed Codex initialization turn, wrote the research plan through `/api/research-plan/write`, and accepted the plan through the app gate.
- Step 4 found and fixed a runtime event scaling gap: one initialization turn persisted 8573 events, so the UI now requests a bounded tail through `/api/runtime/events?limit=...` while preserving full redacted JSONL history in the project.
- Step 4 found and fixed a status recovery gap: completed turns could leave `.rosproj` showing `last_status=turn_started`, especially after sidecar restart. Runtime drain callbacks now update turn status, and project open recovers completed/repair status from persisted runtime events.
- Step 4 found and fixed a runtime proof UX gap: after sidecar restart the UI showed `not configured` even though an isolated Codex config existed. Runtime status now recovers provider/model/reasoning from app-owned `CODEX_HOME/config.toml`, and the UI distinguishes "configured but key not loaded" from "not configured".
- Step 4 recorded an open import-classification gap: the privacy scanner safely excluded many prior-project files containing secret-like text, but this may over-exclude sanitized provenance. A later loop should add a classified exclusion report before final paper production.
- Step 5 first encountered a sidecar restart recovery gap before any new model turn: `.rosproj` retained the prior thread id, but the new app-server session returned `thread not found`. `RuntimeService.start_turn()` now automatically resumes the saved thread and retries once when Codex app-server reports this condition.
- Step 5 then exposed a terminal-status mapping gap: after a network-disconnected turn was interrupted, Codex emitted `turn/completed` with payload status `interrupted`, but the sidecar stored `turn_completed`. Runtime drain and project-open recovery now map `interrupted` to `turn_interrupted` and failed/error terminal states to `needs_repair`.
- Step 5 terminal-status recovery now also corrects stale projects that were already miswritten as `turn_completed` when persisted runtime events show the terminal payload was actually `interrupted`.
- Step 5 retry exposed a researcher-facing recovery gap: after a provider reconnect, the turn produced token usage and command output but no app-readable artifact or terminal state for several minutes, so the operator had to interrupt it. The sidecar now exposes a formal `mark-turn-needs-repair` route and the UI has a `Prepare retry` action so the next turn can continue from saved state instead of recreating the project.
- Step 5 retry also exposed an event-usability gap: Codex printed a full material manifest into the runtime stream, creating more than 11,000 persisted events and overwhelming the UI. Runtime API responses now summarize long strings and long lists while preserving full redacted JSONL in the private project, and the default UI turn prompt tells Codex not to echo full manifests or raw private paths.
- Step 5 source/proof/novelty audit succeeded after the runtime recovery fix. A fresh app-driven Codex/Yunwu thread verified venue facts online, produced a compact audit JSON, and the artifact was written through `/api/research-loop-artifacts/write` to the private project `PUBLIC/research_loop/source_proof_novelty_audit.md`. The researcher accepted the artifact through the app gate. Remaining blockers before paper production are baseline manuscript selection, theorem-bound harmonization, final citation metadata, submission declarations, and optional symbolic checks.
- Step 5 blocker-repair exposed a network-route gap: Yunwu direct streaming could disconnect, but Research OS Desktop had no app-level way to force only the Codex/Yunwu runtime through a local VPN/proxy while keeping the app and localhost traffic direct. Profiles now support `proxy_mode` (`direct`, `system`, `custom`) and a validated local-only `proxy_url`; sidecar applies proxy environment variables only to the app-owned runtime, restarts Codex client when route or secret state changes, and the UI exposes the setting in both project center and workspace. `http://127.0.0.1:7897` was verified against Yunwu `/v1/models` with HTTP 200 and no model inference.
- Step 5 blocker-repair and Step 6 entry succeeded after the proxy route fix. A real app-driven Yunwu/Codex turn produced a blocker-repair package and paper-production gate, written through `/api/research-loop-artifacts/write` and accepted through the app gate; the paper final-product track was selected through `/api/final-products`.
- Step 6 first paper-production turn produced a complete private paper package through `/api/paper-artifacts/write` and `latexmk` compiled `PUBLIC/paper/main.pdf` to 9 pages. Remaining paper blockers are theorem-bound/proof-accounting adversarial review, citation/venue final verification, overfull/underfull LaTeX cleanup, and final declarations/cover-letter polish.
- Step 6 first paper-production turn exposed an app artifact protocol gap: large LaTeX/BibTeX strings can contain invalid JSON escape sequences when Codex returns raw `content`. Artifact writers now accept exactly one of `content` or `content_base64`; `content_base64` is decoded as UTF-8 and still passes path-boundary, secret, and control-character validation. The desktop runtime prompt now instructs Codex to use `content_base64` for LaTeX, BibTeX, and backslash-heavy artifacts.

## Validation Log

- 2026-06-08T11:15:00+08:00: Step 1 completed. Added v4.7 / `WO-0018` governance and reclassified the current operator-assisted paper package as entry material. Validation passed: `git diff --check`, schema validation, resource guard, privacy scan, and desktop app checks. No Yunwu call, paid API, key read, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:20:00+08:00: Step 2 completed. Implemented isolated Research OS owned Codex runtime configuration, seeded Yunwu provider profile metadata, sidecar local-key loading into process memory, runtime parameter propagation, and UI runtime proof display. Validation passed: sidecar unittest (27 tests), Python `py_compile`, desktop app check, TypeScript, Vitest, and Vite build. No Yunwu call, paid API, key read, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:28:00+08:00: Step 3 checkpoint. Fixed the profile-store upgrade gap that prevented the app from exposing the Yunwu `gpt-5.5` xhigh profile when a user already had an older local profile store. Validation passed: sidecar unittest (28 tests), Python `py_compile`, and `git diff --check`. No Yunwu call, paid API, key read, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:41:00+08:00: Step 3 checkpoint. Fixed the Codex app-server sandbox enum mismatch by switching sidecar runtime parameters from `workspaceWrite` to `workspace-write`. Validation passed: sidecar unittest (28 tests), Python `py_compile`, and `git diff --check`. The failed `thread_start` was rejected during app-server request validation; no model turn, paid API usage, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:46:00+08:00: Step 3 checkpoint. Fixed the Codex app-server approval-policy enum mismatch by switching runtime parameters from `unlessTrusted` to `on-request`. Validation passed: sidecar unittest (28 tests), Python `py_compile`, and `git diff --check`. The failed `thread_start` was rejected during app-server request validation; no model turn, paid API usage, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:50:00+08:00: Step 3 checkpoint. Fixed the Codex app-server turn sandboxPolicy enum mismatch by using `workspaceWrite` for `turn_start.sandboxPolicy.type` while retaining `workspace-write` for `thread_start.sandbox`. Validation passed: sidecar unittest (28 tests), Python `py_compile`, and `git diff --check`. The failed `turn_start` was rejected during app-server request validation; no model turn, paid API usage, raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T11:59:00+08:00: Step 3 completed. Started a Research OS Desktop private proof project, loaded the Yunwu key into sidecar process memory only, created a Codex thread with `modelProvider=yunwu`, `model=gpt-5.5`, `reasoningEffort=xhigh`, completed one proof turn, wrote the Codex JSON result through the app research-loop artifact route, measured Yunwu usage delta as `5.7116` quota / estimated USD `0.0000114232`, and captured local screenshots. Also fixed numeric usage telemetry redaction. Validation passed: sidecar unittest (29 tests), Python `py_compile`, Playwright screenshot smoke check, and `git diff --check`. No raw private material commit, public export, submission, or external writeback was used.
- 2026-06-08T12:30:26+08:00: Step 4 completed. Created a fresh private neural-network `.rosproj`, imported three material bundles through app routes, answered exactly three initialization questions, ran a real Codex initialization turn through Yunwu `gpt-5.5` xhigh, wrote the structured research plan through `/api/research-plan/write`, accepted it through the app gate, and advanced to `research_loop / loop_plan_alignment`. Measured Yunwu usage delta was `78.2086` quota / estimated USD `0.0001564172`. App fixes in this checkpoint added runtime event tail limiting, completed-turn status sync/recovery, and runtime-config recovery after sidecar restart. Validation passed: sidecar unittest (33 tests), Python `py_compile`, TypeScript `tsc --noEmit`, Vitest, Playwright screenshots, runtime restart proof, and pending final privacy/resource/schema checks before commit. No raw private material commit, public export, submission, external writeback, or credential persistence was used.
- 2026-06-08T12:38:10+08:00: Step 5 checkpoint. The first source/proof/novelty loop attempt was blocked before model execution because a restarted sidecar/app-server process did not recognize the saved thread id and returned `thread not found`. Fixed `RuntimeService.start_turn()` to resume the thread and retry once on that exact error. Validation passed: sidecar unittest (34 tests), Python `py_compile`, `git diff --check`, privacy scan, resource guard, schema validation, and desktop app checks. No model turn, paid usage, raw private material commit, public export, submission, external writeback, or credential persistence was used.
- 2026-06-08T12:57:03+08:00: Step 5 checkpoint. A source/proof/novelty turn started through Yunwu but the stream disconnected before completion and was interrupted after no progress; Yunwu usage remained unchanged at `280816.0452`. Fixed terminal status mapping so interrupted turns are no longer shown as completed, both live and after project reopen. Validation passed: sidecar unittest (36 tests), Python `py_compile`, `git diff --check`, privacy scan, resource guard, schema validation, and desktop app checks. No successful model artifact, raw private material commit, public export, submission, external writeback, or credential persistence was used.
- 2026-06-08T13:01:43+08:00: Step 5 checkpoint. Extended project-open terminal-status recovery so stale `.rosproj` files already miswritten as `turn_completed` can still be corrected to `turn_interrupted` when persisted runtime events show an interrupted terminal payload. Validation passed: sidecar unittest (36 tests), Python `py_compile`, and `git diff --check`. No model turn, paid usage, raw private material commit, public export, submission, external writeback, or credential persistence was used.
- 2026-06-08T13:36:00+08:00: Step 5 checkpoint. A bounded source/proof/novelty retry reached Yunwu usage but produced no app-readable artifact after a reconnect and over-large manifest output; the turn was interrupted and the private project was marked `needs_repair` through the new app route. Fixed runtime recovery UX, added response-side runtime event summarization, and tightened the default turn prompt to avoid echoing full manifests. Measured Yunwu usage delta was `22.7640` quota / estimated USD `0.000045528`. Validation passed: sidecar unittest (38 tests), Python `py_compile`, TypeScript `tsc --noEmit`, Vitest, and Vite build; final privacy/resource/schema/desktop checks pending before commit. No raw private material commit, public export, submission, external writeback, or credential persistence was used.
- 2026-06-08T13:55:00+08:00: Step 5 checkpoint. Yunwu recovered and a fresh app-driven Codex thread completed the source/proof/novelty audit using `modelProvider=yunwu`, `model=gpt-5.5`, and `reasoningEffort=xhigh`. The JSON final answer was extracted from the private runtime log and written through `/api/research-loop-artifacts/write`; the researcher accepted the audit through the app gate, returning the project to `loop_plan_alignment`. Measured Yunwu usage delta was `81.7918` quota / estimated USD `0.0001635836`. Pending validation/commit before continuing to blocker-repair loop. No raw private material commit, public export, submission, external writeback, or credential persistence was used.
- 2026-06-08T15:00:47+08:00: Step 5 network-route checkpoint. Verified local proxy port `127.0.0.1:7897`, verified Yunwu `/v1/models` through `http://127.0.0.1:7897` with HTTP 200, and added Research OS Desktop profile/runtime/UI support for routing only the app-owned Codex/Yunwu runtime through a custom local proxy. Validation passed: sidecar unittest (40 tests), Python `py_compile`, TypeScript `tsc --noEmit`, Vitest, Vite build, `git diff --check`, and manual Playwright screenshot check of the proxy UI. The Playwright test runner itself timed out without output, so the focused proxy UI check was run through a direct Playwright script. No model inference, paid API usage, raw private material commit, public export, submission, external writeback, or credential persistence was used.
- 2026-06-08T15:52:16+08:00: Step 5/6 checkpoint. Continued through the app-controlled Yunwu/Codex route using `modelProvider=yunwu`, `model=gpt-5.5`, `reasoningEffort=xhigh`, and `proxy_url=http://127.0.0.1:7897`. A blocker-repair artifact batch was written through `/api/research-loop-artifacts/write` and accepted through the app gate; the paper final-product track was selected; a first submission package was written through `/api/paper-artifacts/write`; `latexmk` compiled `PUBLIC/paper/main.pdf` to 9 pages. Measured Yunwu cost was approximately USD `0.00020206` for blocker repair and USD `0.000325628` for first paper production. App gap fixed: artifact routes now accept `content_base64` to avoid JSON escape corruption for LaTeX/BibTeX while preserving privacy validation. Validation passed: sidecar unittest (42 tests), Python `compileall`, desktop app check, TypeScript `tsc --noEmit`, Vitest, Vite build, and `git diff --check`. Pending before final submission: adversarial proof review, citation/venue final source refresh, LaTeX warning cleanup, and final submission artifacts.
