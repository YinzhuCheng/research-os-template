# Research OS v3.3 Validation Report

Date: 2026-06-06
Work order: `WO-0004`
Branch: `codex/research-os-v3`

## Scope

Validated the material-first Codex Browser Copilot implementation:

- `PUBLIC/copilot.html`
- `PUBLIC/copilot_state.json`
- copilot schemas and templates
- `research-os-copilot` skill and `.agents/skills` mirror
- repo-scoped plugin scaffold under `.agents/plugins/`
- local bridge server
- dashboard and documentation links
- Research OS kernel/domain/harness regression checks

## Checks Passed

- `validate_schemas.ps1`
- `validate_skills.ps1`
- `check_skill_mirror.ps1`
- `check_no_orphan_skills.ps1`
- `check_copilot_bridge.ps1`
- `check_copilot_intake_schema.ps1`
- `check_copilot_state.ps1`
- `check_copilot_resource_rendering.ps1`
- `check_dashboard.ps1`
- `check_html_docs.ps1`
- `check_docs_links.ps1`
- `check_research_kernel.ps1`
- `check_domain_kernel_bindings.ps1`
- `check_domain_profiles.ps1`
- `check_agent_capabilities.ps1`
- `check_domain_templates.ps1`
- `check_domain_router.ps1`
- `check_integrations.ps1`
- `check_harness.ps1`
- `scan_privacy.ps1`

## Browser QA

Local bridge was started at `http://127.0.0.1:8765/` and checked with the Codex in-app Browser.

- `PUBLIC/copilot.html`: form, three-question area, Overview, Literature, Theory, Experiment, and Repository Links were visible.
- `PUBLIC/index.html`: Copilot entry, material-first dashboard data, and document reader were visible.
- Console errors: 0 for the checked pages.
- No form submission with real uploads was performed, because the current work order forbids writing runtime private intake material.

## Known Environment Limitation

The plugin-creator `validate_plugin.py` helper could not run in the bundled Python environment because `yaml` / PyYAML is not installed. The repository-specific `check_copilot_bridge.ps1` covered plugin JSON parsing, marketplace JSON parsing, MCP config presence, skill presence, server script presence, routing, and documentation bindings.

## Residual Risks

- The browser cannot force Codex execution; it writes structured queue packets and Codex must confirm.
- Runtime upload handling is implemented in the local bridge but was not exercised with real files under this work order.
- Full production MCP transport may require environment-specific trust and installation review.
- Reference downloads are best-effort and limited to open URLs or landing pages; failures remain human-handled.
