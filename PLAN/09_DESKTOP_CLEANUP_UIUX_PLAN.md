# Research OS v4.1 Desktop Cleanup And UI/UX Plan

## Status

| Step | Area | Status |
| --- | --- | --- |
| 1 | Commit and push v4.0 desktop package result | completed |
| 2 | Delete old browser bridge and plugin double track | completed |
| 3 | Rename state surfaces to desktop naming | completed |
| 4 | Normalize desktop-first docs and repository checks | completed |
| 5 | Risk audit and targeted fixes | completed |
| 6 | UI/UX pass with click-path tests | completed |
| 7 | Full validation, package build, provenance | completed |

## Executed Changes

- Removed the old browser Copilot plugin, bridge server, public cockpit HTML, old bridge schemas/templates, old checks, and old bridge privacy tests.
- Migrated runtime state from `PUBLIC/copilot_state.json` and `CONTROL/copilot_inbox/` to `PUBLIC/research_state.json`, `CONTROL/intake_queue/`, and `CONTROL/choice_responses/`.
- Rewrote desktop docs around Tauri + React + Python sidecar, `.rosproj` sandbox projects, profile boundaries, approvals, archives, packaging, and migration.
- Strengthened `ProjectService` seed allowlist and denylist so old bridge UI and private material do not enter new projects.
- Hardened CORS, runtime event redaction, approval/state handling, and environment checks.
- Improved Project Center, workspace, runtime, approval, archive, profile, choice prompt, and final-product modal UX.
- Added Playwright click-path tests for project creation, final product modal close/select/free-form, archive preview, and empty approval queue across desktop and narrow viewports.

## Risk Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| Old browser bridge remains reachable | addressed | Deleted old entry files and added `check_desktop_app.ps1` assertions. Exact old names are only allowed in migration notes. |
| State naming split between old and desktop flows | addressed | `ResearchStateService` now reads/writes desktop state and intake queue paths. |
| Seed accidentally copies old UI or PRIVATE data | addressed | Added explicit denylist and tests for seed exclusion. |
| CORS wildcard exposes sidecar endpoints | addressed | Sidecar now uses explicit localhost/Tauri origin allowlist. |
| Runtime event stream leaks secrets/private content | addressed | Added recursive sensitive-value redaction before UI/log persistence. |
| Tauri package depends on global npm | addressed | `beforeBuildCommand` now calls local TypeScript and Vite CLIs through `node`. |
| Codex/Yunwu paid test cost overrun | avoided | Optional Yunwu UI review skipped; cost for this v4.1 pass is USD 0. |
| UI mojibake and unclear main path | addressed | Rewrote Chinese UI copy, added empty/error/loading states, and verified click paths. |

## Validation

- `git diff --check`
- old bridge exact-name scan, allowing only `docs/migration.md`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_desktop_app.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_schemas.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_docs_links.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_privacy.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_dashboard.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_environment_docs.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_governance_text.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_research_flow.ps1`
- Static HTML documentation check retired in v4.2; use `scripts/check_dashboard.ps1` and `scripts/check_docs_links.ps1`.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_archives.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_environment.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_private_intake_synthetic.ps1`
- `python -m unittest discover -s apps/research-os-sidecar/tests -v`
- `node ./node_modules/vitest/vitest.mjs run`
- `node ./node_modules/typescript/bin/tsc`
- `node ./node_modules/vite/bin/vite.js build`
- `node ./node_modules/@playwright/test/cli.js test`
- `node ./node_modules/@tauri-apps/cli/tauri.js build`
