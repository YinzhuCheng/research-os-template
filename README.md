# Codex Research OS Template

This repository is a research-neutral Codex Research OS template. It turns research notes, draft plans, conversations, papers, zips, or demos into an auditable human-in-loop research workspace.

It does not assume an LLM, machine learning task, dataset, baseline, paper, venue, or budget by default. Those decisions must come from researcher material or explicit human confirmation.

## Main Entrypoints

- [Desktop App](docs/desktop-app.md): Tauri + React + Python sidecar app for `.rosproj` projects.
- [Material-first Copilot](PUBLIC/copilot.html): browser cockpit for initial material intake.
- [Public Dashboard](PUBLIC/index.html): project navigation and document reader.
- [Quick Start](docs/start-here.html): onboarding for general researchers and Codex beginners.
- [Technical Report](docs/technical-report.html): repository route for future agents and maintainers.
- [Process Contract](docs/process-contract.md): canonical automation flow and skill handoff rules.
- [Environment Guide](docs/environment.md): required runtime, optional tools, and OS-specific install notes.
- [Copilot Bridge Doc](docs/codex-browser-copilot.html): browser-to-Codex bridge details.
- [Domain Modes](docs/domain-modes.html): five domain-specific research paradigms.
- [Research Kernel Template](templates/research_kernel/research_cycle.template.yaml): shared feedback computation loop.
- [Final Product Plan Template](templates/yaml/final_product_plan.template.yaml): paper/report/software output planning.
- [Archive Record Template](templates/yaml/archive_record.template.yaml): git-backed archive metadata.
- [Document Map](docs/doc_map.yaml): structured navigation.

## Research OS v4.0 Desktop App

v4.0 introduces an independent Windows-oriented desktop shell:

- `apps/research-os-desktop/`: Tauri + React + TypeScript UI.
- `apps/research-os-sidecar/`: Python sidecar that owns project files, profile metadata, permissions, archives, and guarded Codex app-server/SDK mediation.
- `.rosproj` is the project entrypoint; the sibling directory is the default writable sandbox.
- The UI does not talk directly to Codex app-server. It only talks to the sidecar.
- Profile metadata stores provider/model preferences and secret references only; it must not store API keys, tokens, cookies, passwords, or authorization headers.

Development commands:

```powershell
python .\apps\research-os-sidecar\sidecar_server.py --serve --template-root .
cd .\apps\research-os-desktop
npm install
npm run dev
```

## Research OS v3.9

v3.9 presents the system to researchers as three macro phases:

`initialization -> semi-automated loop research -> final product`

Internally, the process is governed by eight clearer stages:

`initialization_intake -> loop_acceptance_gate -> loop_plan_alignment -> loop_user_decision -> loop_execute_analyze -> final_product_selection -> final_product_production -> export_release_gate`

Key changes:

- The loop phase blocks progression until the researcher accepts the previous artifact.
- Every user-facing choice prompt has a recommended option, default options, and a natural-language free-form path.
- Final product selection supports paper, research report, software, or multiple tracks.
- Paper output uses venue/template/comparable-paper inputs when provided and defaults to English LaTeX/PDF.
- Research reports emphasize process, initial data, negative results, and reproducibility; supported targets are HTML, LaTeX/PDF, and PPT.
- Software output defaults to stable, engineered, polished, user-friendly productization with documentation and preserved research artifacts.
- Git-backed archives record timestamp, phase, commit, and user description while excluding `PRIVATE/` and secrets.
- Dashboard and Copilot now expose a three-phase phase bar, structured action groups, final product entry, archive entry, and natural-language UI expectations.

## Research OS v3.5

v3.5 hardens the process contract and skill governance:

- `config/research_flow.yaml` defines the canonical machine-readable flow.
- `docs/process-contract.md` explains the human-readable flow and skill handoffs.
- `skills/README.md` is now a trigger matrix instead of a flat skill list.
- Governance text in `AGENTS.md`, `.codex/requirements.md`, and `CONTROL/README.md` is readable and validator-checked.
- New validators check process flow and governance text quality.

## Research OS v3.4

v3.4 makes the runtime environment and repository structure explicit:

- `docs/environment.md` lists the required and optional tools.
- `scripts/install_environment.ps1` checks the environment and can optionally try to install Git/Python on Windows with `winget`.
- `scripts/check_environment.ps1` verifies Git, Python, PowerShell, core files, and optional Codex bridge/LaTeX tools.
- Generated paper output under `PUBLIC/paper/` is no longer tracked by default. Use `templates/latex/` as the authoritative paper scaffold, and generate public paper artifacts only after a paper-oriented work order or explicit researcher decision.
- Old validation snapshots were removed from the current tree; durable audit continues through `PROVENANCE/run_manifest.jsonl`, `PROVENANCE/resource_ledger.jsonl`, and the latest validation report.

Installation commands may need small adjustments by OS version, enterprise image, proxy, and package manager.

## Research OS v3.3

v3.3 adds a material-first Codex Browser Copilot:

- The first screen asks for free text or uploaded material, not a fixed questionnaire.
- Codex profiles the material and asks exactly three targeted questions.
- Every question has a recommended answer, selectable options, and an Other/free-form path.
- Initialization reports include motivation, goals, contribution claims, related work and gaps, reference links, conditional theory track, conditional experiment track, minimum validation, and repository links.
- Browser submissions enqueue structured packets; Codex confirms before analysis or execution.

## Research Kernel

All substantive research loops pass through:

`candidate -> evaluator_contract -> evaluation_result -> belief_state -> search_trace/negative_result -> next_action_policy -> human_judgment_gate`

Every evaluator must list the computation or check: metric, procedure, inputs, scale, threshold, resource estimate, failure mode, and replay note. This keeps skills from becoming a loose toolbox.

## Privacy And Resources

- `PUBLIC/` contains public or sanitized material only.
- `PRIVATE/` is ignored by git and holds raw private material at runtime.
- Real API keys, tokens, cookies, SSH keys, authorization headers, and cloud credentials must never be written to the repository.
- Paid resources, external writeback, public export, and submission require human confirmation.
- Reference download scripts only attempt open-access URLs or landing pages and do not bypass paywalls.

## Useful Commands

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_environment.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment_docs.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_research_flow.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_governance_text.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_strict_schema_instances.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_bridge.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_intake_schema.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_state.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_resource_rendering.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_desktop_app.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_archives.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1
```

To run the local browser bridge:

```powershell
python .agents/plugins/plugins/research-os-copilot/scripts/research_os_copilot_server.py --serve
```
