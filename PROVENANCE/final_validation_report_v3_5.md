# Final Validation Report v3.5

Date: 2026-06-06

Scope:

- Process contract and skill governance hardening.
- Governance text repair for `AGENTS.md`, `.codex/requirements.md`, and `CONTROL/README.md`.
- Machine-readable `config/research_flow.yaml` and schema.
- Skill trigger matrix and orchestrator routing update.
- Dashboard, technical report, doc map, and validator wiring.

## Passed Checks

- `scripts/validate_schemas.ps1`
- `scripts/validate_skills.ps1`
- `scripts/check_skill_mirror.ps1`
- `scripts/check_no_orphan_skills.ps1`
- `scripts/check_research_kernel.ps1`
- `scripts/check_domain_router.ps1`
- `scripts/check_dashboard.ps1`
- `scripts/check_docs_links.ps1`
- `scripts/check_html_docs.ps1`
- `scripts/check_harness.ps1 -PythonPath <bundled-python>`
- `scripts/scan_privacy.ps1`
- `scripts/check_research_flow.ps1`
- `scripts/check_governance_text.ps1`
- `scripts/check_domain_profiles.ps1`
- `scripts/check_agent_capabilities.ps1`
- `scripts/check_domain_templates.ps1`
- `scripts/check_domain_kernel_bindings.ps1`
- `scripts/check_integrations.ps1`
- `scripts/check_copilot_intake_schema.ps1`
- `scripts/check_copilot_state.ps1`
- `scripts/check_copilot_resource_rendering.ps1`
- `scripts/check_copilot_bridge.ps1`
- `scripts/check_environment_docs.ps1`

## Browser QA

Opened the local dashboard and technical report through a temporary local HTTP server at `127.0.0.1:8766`.

- `PUBLIC/index.html`: v3.5 phase, Process Contract toolbar link, Process Contract document entry, and Research Flow YAML entry were visible.
- `docs/technical-report.html`: v3.5 title, Process Contract section, `config/research_flow.yaml` link, and `skills/README.md` trigger matrix link were visible.

The temporary HTTP server was stopped after QA.

## Governance Decisions

- `config/research_flow.yaml` is the canonical machine-readable process contract.
- `docs/process-contract.md` is the human-readable companion.
- `skills/README.md` is the skill trigger matrix.
- `AGENTS.md` explicitly requires repo skill selection before generic Codex execution.
- Existing skills were not split or merged in v3.5; responsibilities and handoff boundaries were clarified instead.

## Residual Risks

- `config/research_flow.yaml` is validated by smoke/regex checks rather than full YAML schema-instance validation.
- Real private intake handling remains untested because `PRIVATE/` is forbidden for this governance pass.
- The process contract is template-level; instantiated projects still need project-specific work orders before running experiments or private intake.
