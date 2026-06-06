# Research OS v3.1 Validation Report

Date: 2026-06-06

## Scope

Validated five deep domain modes for:

- fundamental mathematics
- applied mathematics
- machine learning
- computer science
- statistics

## Checks

Passed:

- `scripts/validate_schemas.ps1`
- `scripts/validate_skills.ps1`
- `scripts/check_skill_mirror.ps1`
- `scripts/check_integrations.ps1`
- `scripts/check_html_docs.ps1`
- `scripts/check_docs_links.ps1`
- `scripts/check_dashboard.ps1`
- `scripts/check_harness.ps1`
- `scripts/check_harness.ps1 -PythonPath "C:\Users\cyz19\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"`
- `scripts/scan_privacy.ps1`
- `scripts/check_domain_profiles.ps1`
- `scripts/check_agent_capabilities.ps1`
- `scripts/check_domain_templates.ps1`
- `scripts/check_domain_router.ps1`

Browser QA passed for desktop and mobile viewports:

- `docs/domain-modes.html`
- `docs/start-here.html`
- `docs/technical-report.html`
- `PUBLIC/index.html`

Report and screenshots:

- `build/browser-qa/v3.1/report.json`
- `build/browser-qa/v3.1/domain-modes-desktop.png`
- `build/browser-qa/v3.1/domain-modes-mobile.png`
- `build/browser-qa/v3.1/start-here-desktop.png`
- `build/browser-qa/v3.1/start-here-mobile.png`
- `build/browser-qa/v3.1/technical-report-desktop.png`
- `build/browser-qa/v3.1/technical-report-mobile.png`
- `build/browser-qa/v3.1/dashboard-desktop.png`
- `build/browser-qa/v3.1/dashboard-mobile.png`

## Residual Risk

- YAML validation remains a lightweight structural check, not full semantic JSON Schema validation.
- Domain agents are role definitions inside skills and registries, not a separate external agent runtime.
- Formal proof assistant integration remains disabled by default and is only a future slot.
