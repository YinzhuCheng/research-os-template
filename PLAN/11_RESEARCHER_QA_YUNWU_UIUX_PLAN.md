# Research OS v4.3 Researcher QA, Yunwu Review, And UI/UX Fix Plan

## Status

| Step | Area | Status |
| --- | --- | --- |
| 1 | Land v4.3 work order, phase gate, and executable plan | completed |
| 2 | Run researcher-perspective Playwright walkthroughs and local screenshots | completed |
| 3 | Fix desktop UI copy, mojibake guards, researcher workflow UX, and native dialogs | completed |
| 4 | Run signal-first Yunwu UX review within USD 3 and apply high-impact findings | pending |
| 5 | Run validation, record provenance/resource use, commit, and push each step | pending |

## Operating Rule

Before each implementation step, reread this plan, check for gaps, execute only the current step, update this status table and gap notes, validate the changed surface, inspect `git status`, then commit and push.

## Scope

- Simulate the app from a real researcher perspective with local mocked sidecar data.
- Save screenshots only under ignored test artifact directories.
- Use Yunwu API only for sanitized UI review signal, with a hard USD 3 cap and no persisted secrets.
- Keep app UI Chinese-first and durable repository documentation English-first.
- Treat the desktop app as the only primary UI; static HTML/browser legacy remains retired.

## Implementation Notes

- First known blocker: Chinese desktop UI strings and tests contain mojibake, and current tests assert the broken strings.
- Add a static guard so mojibake markers fail future desktop validation.
- Use native Tauri dialogs for create/open/import if compatible with the current Tauri version; otherwise leave a typed-path fallback with explicit validation.
- Preserve screenshots, local QA logs, redacted Yunwu request summaries, validation reports, and resource ledger entries.

## Gap Audit

- `apps/research-os-desktop/src/App.tsx`, `ProjectCenter.tsx`, `FinalProductModal.tsx`, and Playwright tests need a full readable-Chinese copy audit.
- Existing Playwright tests cover click paths but do not protect against mojibake.
- Researcher-facing first-run flow needs stronger sidecar/profile/project recovery states.
- Yunwu usage measurement must be verified against the current public API docs before paid review calls.

## Step 1 Validation

- `git diff --check` passed.
- `scripts/validate_schemas.ps1` passed.

## Step 2 Validation

- Existing Playwright workflow passed on desktop and narrow viewport.
- Researcher QA screenshots were captured locally under ignored `apps/research-os-desktop/test-results/researcher-qa/baseline/`.
- Rendered HTML had no Unicode replacement character and no browser console errors.
- Baseline issues were recorded in `PROVENANCE/researcher_qa_baseline_v4_3.md`.

## Step 3 Validation

- TypeScript `tsc --noEmit` passed.
- `scripts/check_desktop_app.ps1` passed, including the new mojibake guard.
- Playwright workflow passed on desktop and narrow viewport.
- Vite production build passed.
- `cargo check` passed after adding `tauri-plugin-dialog`.
- Vitest passed.
- Tauri Windows build passed and produced local MSI and NSIS bundles.
- Post-fix screenshots were captured locally under ignored `apps/research-os-desktop/test-results/researcher-qa/after-ui-fix/`.
