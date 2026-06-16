# Final Validation Report v3.4

Date: 2026-06-06

Scope:

- Runtime environment documentation and install/check scripts.
- Repository structure cleanup.
- Removal of stale generated paper output and old validation snapshots.
- Preservation of durable manifest and resource ledger records.

## Passed Checks

- `scripts/check_environment.ps1 -PythonPath <bundled-python> -RequireCodexPluginFiles`
- `scripts/check_environment_docs.ps1`
- `scripts/install_environment.ps1 -PythonPath <bundled-python>`
- `scripts/validate_schemas.ps1`
- `scripts/validate_skills.ps1`
- `scripts/check_skill_mirror.ps1`
- `scripts/check_latex_sources.ps1`
- `scripts/check_latex_sources.ps1 -Generated`
- `scripts/check_dashboard.ps1`
- `scripts/check_html_docs.ps1`
- `scripts/check_docs_links.ps1`
- `scripts/check_research_kernel.ps1`
- `scripts/check_domain_kernel_bindings.ps1`
- `scripts/check_no_orphan_skills.ps1`
- `scripts/check_domain_profiles.ps1`
- `scripts/check_agent_capabilities.ps1`
- `scripts/check_domain_templates.ps1`
- `scripts/check_domain_router.ps1`
- `scripts/check_integrations.ps1`
- `scripts/check_copilot_intake_schema.ps1`
- `scripts/check_copilot_state.ps1`
- `scripts/check_copilot_resource_rendering.ps1`
- `scripts/check_copilot_bridge.ps1`
- `scripts/check_harness.ps1 -PythonPath <bundled-python>`
- `scripts/scan_privacy.ps1`

## Cleanup Decisions

- Removed default generated paper files under `PUBLIC/paper/`.
- Kept `templates/latex/` as the authoritative optional paper scaffold.
- Removed old validation snapshots from the current tree:
  - `PROVENANCE/final_validation_report.md`
  - `PROVENANCE/final_validation_report_v3_1.md`
  - `PROVENANCE/final_validation_report_v3_2.md`
  - `PROVENANCE/v2_validation_report.md`
  - `PROVENANCE/hashes.json`
- Preserved:
  - `PROVENANCE/final_validation_report_v3_3.md`
  - `PROVENANCE/run_manifest.jsonl`
  - `PROVENANCE/resource_ledger.jsonl`
  - `PROVENANCE/live_evidence_snapshot.yaml`

## Residual Risks

- Installer automation is conservative and Windows/winget-oriented for automatic installs. macOS/Linux users should adapt package-manager commands as documented in `docs/environment.md`.
- `PUBLIC/paper/` is intentionally absent until a paper track is enabled.
- Browser visual QA was not rerun in this cleanup pass because UI behavior changed only by adding environment links and dashboard text; static HTML and link checks passed.
