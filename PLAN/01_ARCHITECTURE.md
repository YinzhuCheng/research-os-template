# Architecture Plan

## Product Boundary

Research OS Desktop is a local app, not a starter repository. It ships a `research-os-core` seed that can initialize governed `.rosproj` project sandboxes.

## Directory Responsibilities

- `apps/research-os-desktop/`: Tauri + React + TypeScript UI.
- `apps/research-os-sidecar/`: Python sidecar services.
- `PUBLIC/`: sanitized public state and summaries.
- `PRIVATE/`: raw intake, sensitive data, private audit, and secret references; real secrets must never be committed.
- `CONTROL/`: work orders, phase gates, intake queue, choice responses, and human confirmations.
- `PROVENANCE/`: run manifests, ledgers, live-evidence records, and audit summaries.
- `config/`: project configuration and schemas.
- `skills/` and `.agents/skills/`: skill sources and repo-scoped mirror.
- `scripts/`: deterministic validation and packaging scripts.
- `templates/`: reusable artifact scaffolds for reports, papers, schemas, adapters, and domain records.
- `PLAN/`: implementation plans and gap audits.

## Lifecycle

1. Create or open a `.rosproj` file.
2. Seed a sibling project sandbox.
3. Capture material through desktop intake.
4. Ask exactly three targeted initialization questions.
5. Run the acceptance-gated research loop.
6. Select final product tracks when accepted artifacts exist.
7. Export or release only after human confirmation.

## Codex Boundary

Codex is an optional execution kernel. The sidecar controls `cwd`, state persistence, approvals, archive snapshots, runtime event redaction, and sandbox boundaries.
