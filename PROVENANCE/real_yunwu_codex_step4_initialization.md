# Real Yunwu-Codex Dogfood Step 4 Initialization Report

Timestamp: 2026-06-08T12:30:26+08:00

Work order: `WO-0018`

## Scope

This checkpoint created and initialized a fresh private Research OS Desktop project for the neural-network submission workflow. The prior operator-assisted paper package was imported as entry material only, not as an accepted final product.

The valid execution route used in this checkpoint was:

`Research OS Desktop UI/API -> Python sidecar -> Codex app-server/SDK -> Yunwu gpt-5.5 xhigh -> app artifact route`

## Private Project

- Project id: `neural-network-real-yunwu-codex-20260608-120431`
- Project file: `PRIVATE/projects/neural-network-submission/neural-network-real-yunwu-codex-20260608-120431.rosproj`
- Project root: `PRIVATE/projects/neural-network-submission/neural-network-real-yunwu-codex-20260608-120431/`
- Current macro phase after this checkpoint: `research_loop`
- Current internal phase after this checkpoint: `loop_plan_alignment`
- Codex thread id: `019ea569-4fbe-7db1-bf2e-16f2318d9eed`
- Codex initialization turn id: `019ea569-c41f-77b1-818d-9591810902d1`
- Recovered turn status after sidecar restart: `turn_completed`

## Imported Material Summary

The app imported three material sources through sidecar import routes.

- Aggregate imported files: 1346
- Aggregate excluded files: 833
- Role counts:
  - notes: 445
  - slide decks: 8
  - PDF material: 12
  - example papers: 10
  - bibliography files: 17
  - venue templates: 338
  - manuscript drafts: 11
  - proof audits: 31
  - venue instructions: 38
  - review records: 37
  - structured records: 155
  - figures/screenshots: 33

Import roles:

- `original_neural_network_folder`: original source folder.
- `prior_private_draft_project`: prior private draft project.
- `operator_assisted_baseline_material`: current compiled PDF/LaTeX/QA package used only as baseline entry material.

## Researcher Choices

The app asked exactly three initialization questions and the researcher answered through `/api/choice-response`:

- Material scope: `whole_folder_research_plan`
- Source verification: `strict_online`
- Research plan priority: `proof_and_submission_plan`

The generated research plan was written through `/api/research-plan/write`:

- Research plan id: `RP-20260608T121233039076-99ff79`
- App artifact: `PUBLIC/research_plan.md` inside the private project

The plan was accepted through the app gate:

- Acceptance prompt: `CP-RESEARCH-PLAN-ACCEPTANCE`
- Acceptance option: `accept_with_audit`
- Response id: `CR-20260608T121308281439-e53193`

## Cost

Yunwu usage was measured before and after the initialization planning turn.

- Before: `280737.8366`
- After: `280816.0452`
- Delta quota: `78.2086`
- Estimated USD: `0.0001564172`
- Model/provider: `modelProvider=yunwu`, `model=gpt-5.5`, `reasoningEffort=xhigh`

The key was loaded into sidecar process memory only and was not written to the repository, project files, screenshots, logs, or raw call records.

## App Gaps Found And Fixed

- The runtime event stream produced 8573 persisted events for one initialization turn. Fetching all events on every UI refresh is not usable. Fixed by adding `limit` support to `/api/runtime/events` and making the React runtime panel request only the latest events by default while preserving the full redacted JSONL history in the project.
- `.rosproj` kept `codex.last_status=turn_started` after a completed turn. Fixed by adding runtime turn-status callbacks and restart-time recovery from `.research-os/runtime_events.jsonl`.
- After sidecar restart, the runtime panel showed `not configured` despite a valid app-owned Codex config. Fixed by recovering provider/model/reasoning from the existing isolated `CODEX_HOME/config.toml` and updating the UI copy to distinguish "configured but key not loaded" from "not configured".

## Open Gaps For Later Loops

- The import privacy scanner excluded many prior-project files because they contained secret-like text. This is safer than under-filtering, but may over-exclude useful sanitized provenance and should be refined with a classified exclusion report before final paper production.
- Runtime event history is persisted on disk, but after a sidecar restart only live in-memory events appear in the event panel. A future UI should show a tail of persisted history with explicit privacy redaction guarantees.
- The `.rosproj` default profile remains `openai-account`; runtime calls can explicitly use the Yunwu profile, but the project default should eventually reflect the selected runtime profile for less confusing UI behavior.

## Validation

- Sidecar unittest: 33 tests passed.
- Python `py_compile`: passed for modified sidecar modules and tests.
- TypeScript `tsc --noEmit`: passed.
- Vitest: 1 test passed.
- Playwright screenshots captured under ignored `apps/research-os-desktop/test-results/researcher-qa/real-yunwu-codex-step4/`.
- Runtime environment after restart recovered `provider_id=yunwu`, `model=gpt-5.5`, `reasoning_effort=xhigh`, and `secret_loaded=false`.

No raw private material was committed. No public export, manuscript submission, external writeback, or credential persistence was performed.
