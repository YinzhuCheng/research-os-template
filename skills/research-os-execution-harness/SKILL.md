---
name: research-os-execution-harness
description: Execute Codex Research OS work orders with strict audit, path, privacy, cost, and stage-gate controls. Use when Codex should run experiments, mutate project artifacts, record run manifests, validate outputs, or continue a research task under a work order.
---

# Research OS Execution Harness

Use this skill before mutating research artifacts or running experiments.

## Workflow

1. Read `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml`.
2. Confirm the task stays within `allowed_paths` and avoids `forbidden_paths`.
3. If confirmation is required by the work order or intervention level, stop and ask.
4. Execute the task.
5. Record outputs and errors in `PROVENANCE/run_manifest.jsonl`.
6. Run privacy scan before any public export.
7. Update checklist and gap audit after substantive progress.

## Quick Checks

- Read `references/audit_contract.md` before changing execution rules.
- Use `scripts/validate_schemas.ps1` before relying on project objects.
- Use `scripts/write_manifest.ps1` after any substantial run.
