# Implementation Checklist

This checklist tracks the current durable Research OS Desktop state. Historical implementation details are preserved in git and provenance.

## Product

- [x] Tauri + React desktop app.
- [x] Python sidecar.
- [x] `.rosproj` project model.
- [x] Sibling project sandbox.
- [x] `research-os-core` seed in packaged app resources.
- [x] Optional official Codex SDK/app-server adapter.
- [x] UI-mediated approvals and timeout-deny behavior.
- [x] Git-backed local archive service.

## Research OS Flow

- [x] Three user-facing macro phases.
- [x] Consolidated internal stage sequence.
- [x] Acceptance-gated semi-automated loop.
- [x] Choice prompt contract with recommended options and free-form input.
- [x] Paper, report, and software final-product tracks.

## State And Privacy

- [x] `PUBLIC/research_state.json`.
- [x] `CONTROL/intake_queue/`.
- [x] `CONTROL/choice_responses/`.
- [x] `PRIVATE/` excluded from git.
- [x] Runtime event redaction.
- [x] Privacy scan and archive validation.

## Documentation

- [x] English-first repository docs.
- [x] Desktop app guide.
- [x] Architecture guide.
- [x] Security and risk register.
- [x] Testing guide.
- [x] Packaging guide.
- [x] Migration notes for retired browser and HTML surfaces.
- [x] Static HTML dashboard and docs removed.

## Validation

- [x] Sidecar unit tests.
- [x] Frontend unit tests.
- [x] Playwright desktop/narrow click paths.
- [x] Tauri package build.
- [x] Schema validation.
- [x] Dashboard data check.
- [x] Docs link check.
- [x] Privacy scan.
