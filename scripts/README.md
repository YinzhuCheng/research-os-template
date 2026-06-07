# Scripts

This directory stores deterministic helper scripts for local Research OS operation. Scripts must be auditable, avoid writing secrets, and respect `CONTROL/work_order.yaml`.

## Environment

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_environment.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment_docs.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_research_flow.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_governance_text.ps1
```

`install_environment.ps1 -InstallMissing` can try Windows `winget` installs for Git and Python. Package names and install commands may need adjustment across Windows/macOS/Linux versions, enterprise images, proxies, and package managers.

If `python` is not on `PATH`, pass an explicit runtime:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1 -PythonPath "C:\path\to\python.exe"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_harness.ps1 -PythonPath "C:\path\to\python.exe"
```

## Core Validation

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_strict_schema_instances.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_harness.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_docs_links.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_html_docs.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build_public_summaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_public_summaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_private_intake_synthetic.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1
```

## Research Kernel And Domains

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_research_kernel.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_domain_kernel_bindings.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_no_orphan_skills.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_domain_profiles.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_agent_capabilities.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_domain_templates.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_domain_router.ps1
```

## Copilot And Integrations

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_bridge.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_intake_schema.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_state.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_resource_rendering.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_integrations.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_eval_fixtures.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_package_artifacts.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build_public_summaries.ps1
python .\evals\run_eval.py
```

Use `scripts/package_template.ps1 -DryRun` to inspect the release allowlist.
Actual packages reject `.git/`, `build/`, `exports/`, and `PRIVATE/`.

## Optional Paper Track

`templates/latex/` is the authoritative paper scaffold. `PUBLIC/paper/` is generated only after a paper-oriented work order or explicit researcher decision.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_latex_sources.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_latex_sources.ps1 -Generated -Force
```
