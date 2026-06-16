# Project Summary

Research OS Desktop is a local researcher-copilot application. It is not a starter repository and no longer uses the old browser bridge or static HTML dashboard as a product surface.

## Current State

- Product line: `Tauri + React + Python sidecar`.
- User entry: `.rosproj` project files and sibling sandbox directories.
- Runtime: optional official Codex SDK/app-server integration, mediated by the sidecar.
- Default UI language: Chinese.
- Repository documentation language: English.
- Main controls: `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, `config/research_flow.yaml`, and `config/research_project.yaml`.

## Principles

- Align researcher intent before executing experiments or generating reports.
- Record budgets, stop conditions, allowed paths, and privacy boundaries before mutating work.
- Keep raw private material out of `PUBLIC/`, `docs/`, and git history.
- Route every risky command, external write, credential access, release, public export, or real resource use through explicit approval.
- Preserve negative, partial, failed, and inconclusive results as auditable artifacts.

## Durable Surfaces

- Desktop app: `apps/research-os-desktop/`.
- Python sidecar: `apps/research-os-sidecar/`.
- App seed and process docs: `docs/`, `config/`, `skills/`, `templates/`, `domain_profiles/`, and `adapters/`.
- Sanitized public state: `PUBLIC/research_state.json`, `PUBLIC/dashboard_data.json`, `PUBLIC/evidence_board.json`, and `PUBLIC/run_monitor.json`.
- Audit: `PROVENANCE/run_manifest.jsonl` and `PROVENANCE/resource_ledger.jsonl`.

## Research OS Flow

User-facing macro phases:

1. Initialization.
2. Semi-automated research loop.
3. Final product.

Internal stages:

`initialization_intake -> loop_acceptance_gate -> loop_plan_alignment -> loop_user_decision -> loop_execute_analyze -> final_product_selection -> final_product_production -> export_release_gate`

All choice prompts require a recommendation, concrete options, and free-form natural-language input.
