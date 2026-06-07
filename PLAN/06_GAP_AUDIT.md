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
- Process contract: v3.5 adds a machine-readable canonical flow and skill trigger matrix.
- Governance readability: v3.5 rewrites key control documents and adds a validator for unreadable governance text.
- P0/P1 audit hardening: v3.6 adds strict schema-instance validation, HTML trailing-content checks, manifest write-path guard, sanitized Copilot intake packets, answer/confirmation APIs, stronger hooks, local eval fixtures, run monitor, adapter contract, release package allowlist, tests, and CI skeleton.
- Lightweight Copilot usability: v3.7 adds generated public Evidence Board and Run Monitor summaries, readable JSON/JSONL/YAML dashboard rendering, Copilot Evidence Board/resource summaries, and synthetic private-intake validation without touching real `PRIVATE/`.
- UI personalization: v3.8 adds five local visual styles and Chinese/English interface settings to Dashboard and Copilot, with Chinese as the default UI language and English as the default final-paper language.
- Three-phase flow: v3.9 exposes initialization, semi-automated loop research, and final product as the user-facing macro phases while consolidating internal governance into eight controlled stages.
- Loop acceptance: v3.9 makes acceptance of the previous artifact a blocking gate before next-step planning.
- Choice prompts: v3.9 requires recommended options, default options, and natural-language free-form input for every user-facing choice.
- Final products: v3.9 adds paper, research report, and software tracks with dedicated skills and schema/template support.
- Archives: v3.9 adds git-backed snapshot APIs, schema/template support, public sanitized archive index, archive validation, and UI entry points.
- UI structure: v3.9 adds phase bars, grouped actions, final product modal, archive modal, local natural-language UI expectations, and inline icon provenance.

## Remaining Risks

- Strict YAML validation covers this repository's current YAML subset, but it is not a full YAML 1.2 parser.
- The browser cockpit can enqueue intake, answers, and next-action confirmations, but Codex still needs to confirm and execute work from the conversation/app side.
- Runtime uploads are designed for `PRIVATE/`; v3.7 tests only synthetic temporary private-intake fixtures and still cannot test real private upload handling while `PRIVATE/` remains forbidden for commits.
- The repo-scoped plugin scaffold may need Codex app trust, marketplace, or MCP-install adjustments by environment.
- `PUBLIC/index.html` has lightweight JSON/JSONL/YAML rendering for selected resources, but it is intentionally not a rich control console or editing UI.
- UI preferences are browser-local and static-page friendly. A future project instance may want schema-backed defaults if teams need shared UI policy.
- Final product generation is now planned and routed, but actual paper/report/software outputs still require project-specific material and researcher selection.
- Git-backed archives are local repository snapshots. Whether project instances should push archive commits by default remains an explicit post-v3.9 product decision.
- Archive privacy checks block obvious secret/private paths, but they do not replace a human review before public export or submission.
- External component integrations are adapter registrations only. License/security review is required before vendoring or executing third-party research systems.
- Mathematical formalization remains a future slot. Lean/Coq/Isabelle integration needs a dedicated work order, toolchain review, and false-proof handling policy.
- Paper generation is optional. `templates/latex/` is checked statically, but generated `PUBLIC/paper/` output is only created after paper enablement.
- The process contract is template-level. Real project instances may still need a project-specific work order before running private intake or experiments.
- The v3.6/v3.7 experiment monitor and adapter layer are schema/template/sanitized-summary scaffolds only. They do not execute real experiments or integrate external systems.

## Next Improvement Slots

- Replace the dependency-free YAML subset parser with a full parser when the runtime dependency policy is decided.
- Add OS-specific installer variants once the target deployment platforms are known.
- Add optional formal proof adapters after the mathematical discovery loop is stable.
- Move P2 discovery-layer work into a new opt-in work order only if it still serves the copilot product boundary: hypothesis backlog, critic, evolution trace, evidence graph, and additional AI4Science domain profiles remain deferred.
