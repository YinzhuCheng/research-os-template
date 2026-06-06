# Implementation Checklist

This checklist tracks the durable Research OS template state. Detailed historical snapshots can be recovered from git history; the current tree keeps the operational checklist concise.

## Core Repository

- [x] Maintain a research-neutral template that does not assume LLM, ML, dataset, baseline, paper, venue, or budget by default.
- [x] Keep public/private separation with `PUBLIC/` for sanitized output and `PRIVATE/` ignored by git.
- [x] Gate execution through `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml`.
- [x] Record substantive runs in `PROVENANCE/run_manifest.jsonl`.
- [x] Record resource boundaries and usage in `PROVENANCE/resource_ledger.jsonl`.

## v3 Documentation And Skills

- [x] Provide researcher-facing onboarding in `docs/start-here.html`.
- [x] Provide agent-facing technical routing in `docs/technical-report.html`.
- [x] Maintain a public dashboard in `PUBLIC/index.html` backed by `PUBLIC/dashboard_data.json`.
- [x] Maintain a structured document map in `docs/doc_map.yaml`.
- [x] Mirror skills from `skills/` to `.agents/skills/` and validate the mirror.
- [x] Register open-source auto-research components as adapters/registry entries instead of vendoring large projects.

## v3.1 Domain Layer

- [x] Add five deep domain profiles: fundamental mathematics, applied mathematics, machine learning, computer science, and statistics.
- [x] Add field-specific skills, agent-role registries, artifact templates, and validation scripts.
- [x] Keep mathematical proof workflows non-formal by default while supporting conjectures, examples, counterexamples, proof strategies, and proof-gap reports.

## v3.2 Research Kernel

- [x] Introduce the shared `candidate -> evaluator_contract -> evaluation_result -> belief_state -> search_trace/negative_result -> next_action_policy -> human_judgment_gate` loop.
- [x] Require evaluator computation checklists: metric/check, procedure, inputs, scale, threshold, resource estimate, failure mode, and replay note.
- [x] Bind domain templates and skills to kernel objects to prevent toolbox sprawl.
- [x] Validate orphan skills so main-route skills need schema/template/validator/doc coverage.

## v3.3 Material-first Copilot

- [x] Replace fixed first-round questions with free text, links, and material upload intake.
- [x] Generate exactly three targeted questions after Codex profiles the material.
- [x] Provide recommended answers, options, and an Other/free-form path for each targeted question.
- [x] Render sanitized initialization state in the browser cockpit.
- [x] Add a repo-scoped plugin scaffold and local bridge server.

## v3.4 Environment And Cleanup

- [x] Document required and optional runtime tools in `docs/environment.md`.
- [x] Add `scripts/install_environment.ps1` with OS-version caveats and conservative Windows `winget` support.
- [x] Add `scripts/check_environment.ps1` and `scripts/check_environment_docs.ps1`.
- [x] Treat `templates/latex/` as the authoritative optional paper scaffold.
- [x] Remove stale generated `PUBLIC/paper/` output from the current tree.
- [x] Remove old validation snapshots while preserving durable manifest and ledger files.
- [x] Run the full v3.4 validation set and record `PROVENANCE/final_validation_report_v3_4.md`.

## v3.5 Process Contract And Skill Governance

- [x] Plan the v3.5 hardening pass around a single canonical Research OS process.
- [x] Rewrite unreadable governance entrypoints: `AGENTS.md`, `.codex/requirements.md`, and `CONTROL/README.md`.
- [x] Add `config/research_flow.yaml` and `config/schemas/research_flow.schema.json`.
- [x] Upgrade `skills/README.md` into a trigger matrix with responsibilities and boundaries.
- [x] Update orchestrator routing to reference the process contract.
- [x] Add `docs/process-contract.md`.
- [x] Add `scripts/check_research_flow.ps1` and `scripts/check_governance_text.ps1`.
- [x] Run the full v3.5 validation set and record `PROVENANCE/final_validation_report_v3_5.md`.
