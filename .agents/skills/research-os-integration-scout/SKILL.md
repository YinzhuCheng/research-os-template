---
name: research-os-integration-scout
description: Evaluate and register open-source auto-research components for Research OS, recording source URLs, licenses, install commands, environment-variable names, output mappings, safety risks, and adapter boundaries without vendoring large third-party code.
---

# Research OS Integration Scout

Use this skill when adding or updating entries in `docs/integrations/components.yaml` or adapter templates.

## Workflow

1. Read `CONTROL/work_order.yaml`, `PROVENANCE/live_evidence_snapshot.yaml`, and `docs/integrations/components.yaml`.
2. Verify each component from primary sources where possible:
   - project repository;
   - paper or project page;
   - license file;
   - official installation instructions.
3. Record only integration metadata by default:
   - source URL and access date;
   - license name and license risk;
   - install command or documentation URL;
   - environment variable names, never secret values;
   - Research OS phases where the component can attach;
   - input and output artifact mapping;
   - sandbox, cost, privacy, and external write risks.
4. Use `templates/yaml/integration_component.template.yaml` for new entries.
5. Run `scripts/check_integrations.ps1`.

## Boundaries

- Do not vendor large third-party code unless the work order explicitly authorizes a license review and maintenance plan.
- Do not install dependencies or run paid API calls during scouting.
- Mark a component `adapter_status: planned` unless a deterministic local adapter and validation check exist.
