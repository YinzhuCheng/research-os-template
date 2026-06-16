# Research OS v4.2 Repository Cleanup Validation

Timestamp: 2026-06-07T22:54:33+08:00

## Scope

This validation covers the v4.2 repository cleanup. Research OS Desktop is now the clear repository identity. The old static HTML documentation and dashboard surfaces have been removed, while the Tauri app keeps its required `index.html` as a Vite application shell.

## Changes

- Removed `PUBLIC/index.html`, `docs/start-here.html`, `docs/domain-modes.html`, `docs/technical-report.html`, and `scripts/check_html_docs.ps1`.
- Renamed the packaged project seed resource from `research-os-template` to `research-os-core`.
- Replaced sidecar `--template-root` with `--seed-root`.
- Renamed `scripts/package_template.ps1` to `scripts/package_seed.ps1`.
- Rewrote durable repository documentation in English.
- Updated `docs/doc_map.yaml`, `PUBLIC/dashboard_data.json`, `PUBLIC/claim_evidence_matrix.yaml`, public summaries, and validation scripts.
- Updated `research-os-doc-site` skill instructions to forbid reintroducing static HTML documentation as the primary surface.

## Validation

Passed:

- `git diff --check`
- durable documentation Chinese-character scan
- retired HTML/template-name residual scan, allowing only `docs/migration.md` to list removed files
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_schemas.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_desktop_app.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_dashboard.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_docs_links.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_environment_docs.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_privacy.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_governance_text.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_research_flow.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_harness.ps1 -PythonPath <bundled Python>`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_domain_router.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_no_orphan_skills.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_package_artifacts.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_public_summaries.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_environment.ps1 -PythonPath <bundled Python>`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_private_intake_synthetic.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_archives.ps1`
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

## Cost

No paid API, Yunwu call, cloud compute, or external writeback was used. Additional cost: USD 0.

## Residual Note

The remote GitHub repository name still includes the old name until the owner renames it on GitHub. This is outside ordinary git commit/push.
