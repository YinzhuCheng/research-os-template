# Research OS v4.3 UI/UX Fix Report

Timestamp: 2026-06-07T23:33:50.4620367+08:00

## Changes

- Replaced raw macro-phase display with stable Chinese macro-stage labels and secondary internal-stage labels.
- Added a macro-phase normalization layer so legacy or sidecar values such as `loop` still highlight the correct phase.
- Added native Tauri dialog support through the Rust dialog plugin and direct `invoke` calls, with browser-preview fallback copy.
- Reworked the runtime event log from raw JSON-first output to readable event cards with expandable structured details.
- Reworked approval rows to show method, risk, reason, command/scope, and explicit allow/decline/cancel actions.
- Reworked archive preview to show macro phase, internal phase, changed path count, changed paths, and privacy scan status.
- Added desktop validation guards for known mojibake markers in desktop source and tests.
- Updated Playwright coverage so researcher-visible labels, runtime events, approval details, archive state, final product modal, and dialog fallback behavior are exercised.

## Screenshot QA

Post-fix screenshots were saved locally under ignored:

`apps/research-os-desktop/test-results/researcher-qa/after-ui-fix/`

The screenshot script reported no browser console errors and no Unicode replacement character in rendered HTML.

## Validation

- TypeScript `tsc --noEmit` passed.
- `scripts/check_desktop_app.ps1` passed.
- Playwright workflow passed on desktop and narrow viewport.
- Vite production build passed.
- `cargo check` passed.
- Vitest passed.
- Tauri Windows build passed and produced local MSI and NSIS bundles.

## Remaining UX Risks For Yunwu Review

- The first-run profile form is still technical and may need clearer provider/model guidance.
- Disabled runtime buttons communicate safety, but a researcher may still need a clearer "install/configure Codex runtime" path.
- Final product modal is usable, but external review should check whether defaulting to report is still the best researcher-facing recommendation.
