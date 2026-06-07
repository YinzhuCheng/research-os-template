# Research OS v3.6 P0/P1 Validation Report

Generated: 2026-06-06

Work order: `WO-0007`

## Scope

Implemented audit-package P0/P1 hardening only:

- strict schema-instance validation;
- HTML trailing-content detection and manifest write guard;
- sanitized Copilot intake packets and raw free-text privacy boundary;
- Copilot answer/confirmation API and cockpit controls;
- stronger example Codex hooks;
- local run monitor, experiment/eval scaffolds, adapter contract, package allowlist, tests, and CI skeleton.

P2 discovery-layer work remains out of scope.

## Validation Commands

Passed locally:

- `scripts/validate_schemas.ps1`
- `scripts/check_strict_schema_instances.ps1`
- `scripts/check_html_docs.ps1`
- `scripts/check_copilot_intake_schema.ps1`
- `scripts/check_copilot_state.ps1`
- `scripts/check_copilot_resource_rendering.ps1`
- `scripts/check_copilot_bridge.ps1`
- `scripts/check_dashboard.ps1`
- `scripts/check_docs_links.ps1`
- `scripts/check_integrations.ps1`
- `scripts/check_live_evidence.ps1`
- `scripts/scan_privacy.ps1 -Paths PUBLIC,PROVENANCE`
- `scripts/check_package_artifacts.ps1`
- `scripts/check_eval_fixtures.ps1`
- `scripts/check_harness.ps1`
- `scripts/check_governance_text.ps1`
- `scripts/check_research_flow.ps1`
- `scripts/check_research_neutrality.ps1`
- `scripts/check_resource_guard.ps1`
- `scripts/check_research_kernel.ps1`
- `scripts/check_domain_kernel_bindings.ps1`
- `scripts/check_no_orphan_skills.ps1`
- `scripts/check_environment_docs.ps1`
- `scripts/check_environment.ps1`
- `scripts/check_skill_mirror.ps1`
- `evals/run_eval.py`
- `tests/test_schema_instances.py`
- `tests/test_copilot_privacy.py`
- `tests/test_hooks.py`
- Python compile check for hooks, bridge server, validator, eval runner, and tests.
- `.codex/hooks/stop_review.py`
- `scripts/package_template.ps1 -DryRun`

Browser QA:

- Opened `http://127.0.0.1:8766/PUBLIC/copilot.html` through the in-app Browser via a temporary local static server.
- Confirmed title, main heading, stepper, Run Monitor, privacy preview, and zero console errors.
- Stopped the temporary server after verification.

## Resource And Privacy

- Cost: `0 CNY`.
- No paid API, cloud, GPU, lab, external writeback, public export, or real experiment execution.
- No real `PRIVATE/` material was read.
- Privacy tests used only a temporary synthetic repository root.
