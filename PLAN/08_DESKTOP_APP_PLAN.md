# Research OS v4.0 Desktop App Plan

## Status

| Step | Area | Status |
| --- | --- | --- |
| 1 | Tauri + React desktop shell | implemented |
| 2 | Python sidecar service layer | implemented |
| 3 | `.rosproj` project sandbox model | implemented |
| 4 | Profile, approval, archive, state services | implemented |
| 5 | Optional Codex app-server/SDK adapter | implemented |
| 6 | Docs, dashboard, validation script | implemented |
| 7 | Validation | completed |

## Decisions

- Product route: Tauri + React + Python sidecar.
- Project route: `.rosproj` file plus sibling sandbox directory.
- Runtime route: official Codex app-server/SDK, optional at import time and safe-failing when unavailable.
- Security route: project-root writes are normal; sandbox-external access, credentials, external writeback, git push, release, public export, and real resources require explicit confirmation.

## Validation Targets

- `python -m unittest discover -s apps/research-os-sidecar/tests`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_desktop_app.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1`
- Frontend build/tests when Node dependencies are installed.

## Validation Result

Completed in v4.0/v4.1 follow-up:

- Tauri build produced local MSI and NSIS bundles under ignored `apps/research-os-desktop/src-tauri/target/`.
- Sidecar unit tests, frontend Vitest, Playwright desktop/narrow click paths, schema checks, dashboard checks, docs link checks, privacy scan, and desktop app checks passed.
- Tauri packaging was hardened by changing `beforeBuildCommand` from `npm run build` to direct local `node` calls for TypeScript and Vite.
