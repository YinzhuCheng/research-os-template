# Architecture

Research OS Desktop is a governed local application:

`Tauri shell -> React workbench -> Python sidecar -> optional official Codex SDK/app-server -> project sandbox`

The React UI never talks directly to Codex. It calls the sidecar over localhost for project creation, state, approvals, archives, runtime events, profile metadata, and final-product selection.

## Project Seed

The packaged application carries a `research-os-core` seed. When a user creates a `.rosproj` file, the sidecar copies the seed into the sibling project directory, initializes the Research OS control structure, and creates the first local git commit.

The seed is not branded as a starter repository. The `templates/` directory remains because it contains reusable artifact scaffolds for papers, reports, domain records, adapter contracts, and Research OS state objects.

## State

- `.rosproj`: non-sensitive project metadata.
- `CONTROL/intake_queue/`: sanitized material-intake packets.
- `CONTROL/choice_responses/`: user selections and natural-language supplements.
- `PUBLIC/research_state.json`: sanitized state rendered by the desktop UI.
- `PRIVATE/intake/`: raw material captured at runtime.
- `PROVENANCE/`: manifests, ledgers, and archive records.

## Research Flow

The machine-readable process contract is `config/research_flow.yaml`. The user-facing macro phases are initialization, semi-automated research loop, and final product.

Internal stages are `initialization_intake`, `loop_acceptance_gate`, `loop_plan_alignment`, `loop_user_decision`, `loop_execute_analyze`, `final_product_selection`, `final_product_production`, and `export_release_gate`.

Final Product Tracks support paper, research report, software, or a multi-track combination. Git-backed archives are local snapshots used before risky transitions, long-running work, or release gates.

## Artifact Routes

The sidecar owns app-readable artifact writes. Research-loop outputs use `/api/research-loop-artifacts/write`; paper and submission outputs use `/api/paper-artifacts/write`. Each file entry may provide either `content` or `content_base64`, never both. `content_base64` is preferred for LaTeX, BibTeX, and other backslash-heavy text because it avoids JSON escape corruption while preserving the same UTF-8 decode, path-boundary, secret-scan, and control-character checks.

## Skills And Domains

`research-os-orchestrator` routes the work. `research-os-research-kernel` owns generate/evaluate/update/human-gate state. Domain routes stay under `domain_profiles/` and the domain skills:

- `research-os-math-discovery`
- `research-os-applied-math-modeling`
- `research-os-ml-research-protocol`
- `research-os-cs-research-artifact`
- `research-os-statistical-inference`

No domain skill may bypass the research kernel, resource guard, execution harness, privacy policy, or approval gates.
