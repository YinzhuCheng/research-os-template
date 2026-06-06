# Gap Audit

This audit lists current residual risks after the v3.4 repository cleanup. Historical v2/v3/v3.1/v3.2/v3.3 notes are preserved in git history.

## Closed Gaps

- Research neutrality: no default model, provider, dataset, baseline, paper target, venue, or budget.
- Governance: work orders, phase gates, path boundaries, manifest, ledger, and privacy scan exist.
- Documentation: researcher quick start, technical route, domain modes, copilot bridge, environment guide, and document map exist.
- Domain depth: five initial domain profiles have skills, templates, agent roles, and validators.
- Research kernel: substantive domain work binds to shared kernel objects and computation checklists.
- Copilot intake: material-first browser cockpit, targeted three-question protocol, schemas, sanitized state, and bridge scaffold exist.
- Environment setup: runtime requirements and install/check scripts exist.
- Cleanup: generated paper output is no longer tracked by default; old validation snapshots were pruned from the current tree.

## Remaining Risks

- YAML validation is still lightweight. Future work can add strict JSON Schema validation for YAML instances.
- The browser cockpit can enqueue and render state, but Codex still needs to confirm and execute work from the conversation/app side.
- Runtime uploads are designed for `PRIVATE/`; this template cannot test real private upload handling while `PRIVATE/` remains forbidden for commits.
- The repo-scoped plugin scaffold may need Codex app trust, marketplace, or MCP-install adjustments by environment.
- `PUBLIC/index.html` renders many resources as source text. This keeps the asset weight low but is not a rich renderer for every file type.
- External component integrations are adapter registrations only. License/security review is required before vendoring or executing third-party research systems.
- Mathematical formalization remains a future slot. Lean/Coq/Isabelle integration needs a dedicated work order, toolchain review, and false-proof handling policy.
- Paper generation is optional. `templates/latex/` is checked statically, but generated `PUBLIC/paper/` output is only created after paper enablement.

## Next Improvement Slots

- Add a strict YAML parser and instance validator for domain profiles, copilot packets, component registry, and research-kernel cycles.
- Add richer browser-side rendering for selected YAML/JSON resources without turning the dashboard into a heavy app.
- Add a safe private-intake test harness that uses synthetic files only and never commits `PRIVATE/`.
- Add OS-specific installer variants once the target deployment platforms are known.
- Add optional formal proof adapters after the mathematical discovery loop is stable.
