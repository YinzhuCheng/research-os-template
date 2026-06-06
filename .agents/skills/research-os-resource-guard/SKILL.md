---
name: research-os-resource-guard
description: Guard researcher-defined budgets and real resources for any research domain, including time, compute, cloud, lab materials, API calls, model usage, human annotation, equipment, and other costs. Use before spending, scaling, external calls, or reviewing cost anomalies.
---

# Research OS Resource Guard

Use this skill before any action that can consume money, quota, human time, instrument time, cloud resources, paid APIs, or scarce materials.

## Workflow

1. Read `config/research_project.yaml`, `CONTROL/work_order.yaml`, and `PROVENANCE/resource_ledger.jsonl`.
2. Determine whether the action uses real resources.
3. Compare planned use with:
   - total limit,
   - category limit,
   - stage limit,
   - daily limit,
   - warning threshold,
   - hard stop policy.
4. If limits are missing for real resources, stop for alignment.
5. If planned use exceeds warning threshold, ask for confirmation.
6. If planned use exceeds hard stop, block until the decision maker changes the budget.
7. After execution, record actual or estimated use in the resource ledger.

## Quick Checks

- Read `references/resource_guard_rules.md` before judging a budget.
- Do not assume LLM/API spending is the only cost.
- Prefer smaller probes, cached artifacts, dry runs, local/offline checks, and staged expansion.
