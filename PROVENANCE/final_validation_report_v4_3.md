# Research OS v4.3 Final Validation Report

Timestamp: 2026-06-07T23:58:30.3077965+08:00

## Summary

Research OS Desktop v4.3 completed a researcher-perspective QA cycle, local screenshot review, Yunwu-assisted UI review, and targeted UI/UX fixes. The desktop app remains the primary user interface, with Chinese-first app copy and English-first durable repository documentation.

## Product Changes Validated

- Project Center now keeps create/open project as the primary path and collapses profile/model controls under advanced settings.
- Workspace now shows a clear current-action guide above the panels.
- Macro phases are normalized and rendered as researcher-facing Chinese labels, including legacy values such as `loop`.
- Runtime unavailable state now gives recovery copy and a retry action.
- Runtime events render readable cards with expandable structured details.
- Approval cards show method, risk, reason, command/scope, and clearer one-shot action labels.
- Archive panel frames snapshots as recovery/compare/continue protection.
- Final product modal keeps report as a recommendation but does not silently preselect it.
- Native Tauri dialog support is registered through `tauri-plugin-dialog`, with browser-preview fallback copy.
- Desktop validation now fails on known mojibake markers in source/tests.

## Screenshot QA

Local ignored screenshot directories:

- `apps/research-os-desktop/test-results/researcher-qa/baseline/`
- `apps/research-os-desktop/test-results/researcher-qa/after-ui-fix/`
- `apps/research-os-desktop/test-results/researcher-qa/after-yunwu-fix/`

All screenshot scripts reported no browser console errors and no Unicode replacement character in rendered HTML.

## Yunwu Cost

- Model: `gpt-5.4`
- Reasoning: `low`
- Calls: 3
- Token-log quota: 23,985
- Query-service exchange rate: `$1 = 500,000 tokens`
- Estimated cost: USD 0.04797
- Budget cap: USD 3
- Raw sanitized record: `PROVENANCE/yunwu_ui_review_v4_3.json`

## Validation Passed

- `git diff --check`
- `scripts/validate_schemas.ps1`
- `scripts/check_desktop_app.ps1`
- `scripts/scan_privacy.ps1`
- `scripts/check_docs_links.ps1`
- `scripts/check_dashboard.ps1`
- `scripts/check_environment_docs.ps1`
- `scripts/check_governance_text.ps1`
- `scripts/check_research_flow.ps1`
- `scripts/check_harness.ps1`
- `scripts/check_resource_guard.ps1`
- `scripts/check_no_orphan_skills.ps1`
- `scripts/check_archives.ps1`
- `scripts/check_environment.ps1`
- `scripts/check_private_intake_synthetic.ps1`
- `scripts/check_public_summaries.ps1`
- `scripts/check_package_artifacts.ps1`
- `scripts/check_integrations.ps1`
- `scripts/check_domain_profiles.ps1`
- `scripts/check_domain_templates.ps1`
- `scripts/check_domain_router.ps1`
- `scripts/check_research_kernel.ps1`
- `scripts/check_skill_mirror.ps1`
- `scripts/check_agent_capabilities.ps1`
- Sidecar unit tests: 7 passed
- Vitest: 1 passed
- TypeScript `tsc --noEmit`
- Playwright: 2 passed across desktop and narrow viewports
- Vite production build
- Tauri Windows package build

## Package Outputs

Local ignored package outputs were produced:

- `apps/research-os-desktop/src-tauri/target/release/research-os-desktop.exe`
- `apps/research-os-desktop/src-tauri/target/release/bundle/msi/Research OS_0.1.0_x64_en-US.msi`
- `apps/research-os-desktop/src-tauri/target/release/bundle/nsis/Research OS_0.1.0_x64-setup.exe`

## Residual Risk

The app has improved mocked researcher workflows, but the next meaningful risk is live Codex runtime dogfooding: interrupted-session recovery, post-approval execution result cards, and restore/compare archive actions still need validation against real Codex turns.
