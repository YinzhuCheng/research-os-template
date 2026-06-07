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

## v3.6 P0/P1 Audit Hardening

- [x] Add strict schema-instance validation with a dependency-free local validator.
- [x] Fix YAML date/string and null/string template mismatches caught by strict validation.
- [x] Remove `PUBLIC/copilot.html` trailing manifest JSON and reject trailing non-whitespace after `</html>`.
- [x] Guard `scripts/write_manifest.ps1` so default writes target `PROVENANCE/run_manifest.jsonl`.
- [x] Keep raw Copilot `free_text` out of `CONTROL/`, `PUBLIC/`, and API responses.
- [x] Add Copilot answer and next-action confirmation APIs plus browser controls.
- [x] Add cross-platform hook commands and stronger Stop-hook checks.
- [x] Add local experiment/run monitor, eval fixtures, adapter contract, package allowlist, tests, and CI skeleton.

## v3.7 Lightweight Copilot Usability

- [x] Keep the initial product boundary as researcher copilot, not fully autonomous research agent.
- [x] Generate `PUBLIC/evidence_board.json` from the public claim/evidence matrix for readable claim review.
- [x] Generate `PUBLIC/run_monitor.json` from public experiment skeleton, manifest, and resource ledger summaries.
- [x] Add lightweight JSON/JSONL/YAML rendering to `PUBLIC/index.html`.
- [x] Add Evidence Board, audit run summary, resource summary, and bridge command copy affordance to `PUBLIC/copilot.html`.
- [x] Add public summary checks and synthetic private-intake privacy checks to local validation, Stop hook, and CI skeleton.
- [x] Keep P2 hypothesis backlog, critic/evolution loops, knowledge graph, real experiment queues, and external adapter execution deferred.

## v3.8 UI Style And Language Settings

- [x] Add a user settings button to `PUBLIC/index.html` and `PUBLIC/copilot.html`.
- [x] Provide five suitable UI styles: clean SaaS, compact enterprise, soft system, developer dark, and editorial report.
- [x] Default the interface language to Chinese.
- [x] Provide a full English interface option.
- [x] Show that final paper output defaults to English regardless of interface language.
- [x] Persist UI style/language locally and support URL overrides for QA or direct links.
- [x] Add responsive wrapping and narrow-screen constraints to avoid text overflow after language switching.

## v3.9 Three-Phase Flow, Final Products, And Archives

- [x] Persist the v3.9 execution plan in `PLAN/07_THREE_PHASE_FINAL_PRODUCT_PLAN.md`.
- [x] Replace the user-facing process model with three macro phases: initialization, semi-automated loop research, and final product.
- [x] Consolidate the internal process into eight controlled stages while preserving work order, phase gate, kernel, resource, audit, manifest, and ledger controls.
- [x] Add the universal `choice_prompt` contract with recommended option, defaults, and natural-language free-form input.
- [x] Add final product plan schema/template and paper, report, and software product tracks.
- [x] Add `research-os-final-product`, `research-os-report-authoring`, and `research-os-software-productization` skills and mirror them under `.agents/skills/`.
- [x] Register metadata-only open-source resources for final product tooling without vendoring or executing third-party systems.
- [x] Add git-backed archive preview/create/list bridge APIs, archive schema/template, public archive index, validator, and unit test.
- [x] Add Dashboard/Copilot three-phase phase bars, structured action groups, final product modal, archive modal, and natural-language UI expectation fields.
- [x] Update docs, dashboard data, doc map, asset provenance, checklist, and gap audit for v3.9.
- [ ] Complete full validation and browser QA for desktop and mobile.
