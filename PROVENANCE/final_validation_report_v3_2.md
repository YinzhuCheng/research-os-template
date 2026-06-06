# Research OS v3.2 Validation Report

Date: 2026-06-06

## Scope

Validated the Research OS v3.2 research kernel and feedback computation layer:

- `research-os-research-kernel`
- `config/schemas/research_kernel.schema.json`
- `templates/research_kernel/research_cycle.template.yaml`
- `kernel_bindings` for five domain profiles
- domain templates with evaluator computation checklists
- anti-spaghetti no-orphan skill validation

## Checks

Passed:

- `scripts/validate_schemas.ps1`
- `scripts/validate_skills.ps1`
- `scripts/check_research_kernel.ps1`
- `scripts/check_domain_kernel_bindings.ps1`
- `scripts/check_no_orphan_skills.ps1`
- `scripts/check_domain_profiles.ps1`
- `scripts/check_agent_capabilities.ps1`
- `scripts/check_domain_templates.ps1`
- `scripts/check_domain_router.ps1`
- `scripts/check_skill_mirror.ps1`
- `scripts/check_integrations.ps1`
- `scripts/check_html_docs.ps1`
- `scripts/check_docs_links.ps1`
- `scripts/check_dashboard.ps1`
- `scripts/check_harness.ps1`
- `scripts/check_harness.ps1 -PythonPath "C:\Users\cyz19\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"`
- `scripts/check_resource_guard.ps1`
- `scripts/check_research_neutrality.ps1`
- `scripts/check_live_evidence.ps1`
- `scripts/scan_privacy.ps1`

Browser QA passed for desktop and mobile viewports:

- `docs/start-here.html`
- `docs/domain-modes.html`
- `docs/technical-report.html`
- `PUBLIC/index.html`

Report and screenshots:

- `build/browser-qa/v3.2/report.json`
- `build/browser-qa/v3.2/start-here-desktop.png`
- `build/browser-qa/v3.2/start-here-mobile.png`
- `build/browser-qa/v3.2/domain-modes-desktop.png`
- `build/browser-qa/v3.2/domain-modes-mobile.png`
- `build/browser-qa/v3.2/technical-report-desktop.png`
- `build/browser-qa/v3.2/technical-report-mobile.png`
- `build/browser-qa/v3.2/dashboard-desktop.png`
- `build/browser-qa/v3.2/dashboard-mobile.png`

## Residual Risk

- YAML semantic validation remains lightweight; future work can add full instance validation against JSON Schema.
- The research kernel is a template-level contract, not a persistent database or independent runtime.
- Evaluator contracts require calculations to be listed, but expert review remains necessary for scientific adequacy.
