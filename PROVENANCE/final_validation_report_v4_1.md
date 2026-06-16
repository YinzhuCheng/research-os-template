# Research OS v4.1 Desktop Cleanup And UI/UX Validation

Timestamp: 2026-06-07T22:19:40+08:00

## Scope

This validation covers the v4.1 cleanup after the v4.0 desktop app package commit. The product route is now desktop-first: Tauri + React UI, Python sidecar, `.rosproj` project sandbox, and Research OS state as the source of truth.

## Main Changes

- Removed the old browser Copilot/bridge plugin, bridge server, HTML cockpit, old schemas/templates, and old check scripts.
- Migrated public runtime state to `PUBLIC/research_state.json` and intake commands to `CONTROL/intake_queue/`.
- Rewrote desktop docs, migration notes, dashboard data, process contract, environment docs, testing docs, architecture docs, packaging docs, and script docs.
- Improved desktop UI/UX around project creation, sidecar status, material intake, choice prompts, runtime events, approvals, archives, and final product selection.
- Added Playwright click-path coverage for desktop and narrow viewports.
- Hardened CORS, runtime event redaction, project seed filtering, and Tauri packaging.

## Validation Commands

Passed:

- `git diff --check`
- old bridge exact-name scan; only `docs/migration.md` contains retired names
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_desktop_app.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_schemas.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_docs_links.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_privacy.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_dashboard.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_environment_docs.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_governance_text.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_research_flow.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_html_docs.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_archives.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_environment.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_private_intake_synthetic.ps1`
- `python -m unittest discover -s apps/research-os-sidecar/tests -v`
- `node ./node_modules/vitest/vitest.mjs run`
- `node ./node_modules/typescript/bin/tsc`
- `node ./node_modules/vite/bin/vite.js build`
- `node ./node_modules/@playwright/test/cli.js test`
- `node ./node_modules/@tauri-apps/cli/tauri.js build`

## Package Outputs

Generated locally under ignored build paths:

- `apps/research-os-desktop/src-tauri/target/release/research-os-desktop.exe`
- `apps/research-os-desktop/src-tauri/target/release/bundle/msi/Research OS_0.1.0_x64_en-US.msi`
- `apps/research-os-desktop/src-tauri/target/release/bundle/nsis/Research OS_0.1.0_x64-setup.exe`

## Resource Use

- Yunwu UI heuristic review was skipped because local unit, static, package, and Playwright QA were sufficient for this pass.
- Additional paid API cost for v4.1: USD 0.

## Residual Risks

- Full Codex app-server integration remains dependent on the user's installed official Codex runtime and profile configuration.
- v1 packaging still detects or uses local runtime dependencies; bundling an official Codex binary is intentionally out of scope.
- Playwright verifies mocked sidecar UI flows, not a real long-running Codex turn.
