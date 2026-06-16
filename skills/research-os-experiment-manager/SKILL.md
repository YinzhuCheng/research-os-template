---
name: research-os-experiment-manager
description: Plan and supervise optional automated experiment loops in Research OS using human-approved hypotheses, feasibility probes, resource budgets, execution manifests, result ledgers, rollback/resume points, and stopping rules.
---

# Research OS Experiment Manager

Use this skill only after a work order authorizes experiment planning or execution.

## Workflow

1. Read `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, `config/research_project.yaml`, and the active feasibility probe.
2. Confirm the experiment is in scope and that budget, compute, tools, data access, and stop conditions are explicit.
3. Create a plan that separates:
   - hypothesis or task;
   - baseline or comparison, only if the researcher supplied or approved it;
   - execution environment;
   - measurements;
   - expected artifacts;
   - rollback/resume points.
4. Before execution, require confirmation for real resources, credentials, networked tools, external writeback, or budget overrun.
5. During execution, record:
   - `PROVENANCE/run_manifest.jsonl`;
   - `PROVENANCE/resource_ledger.jsonl`;
   - result files or reports under allowed paths;
   - failed, cancelled, timed out, and partial states.
6. Summarize outcomes without overstating success. Partial runs remain partial.

## Boundaries

- Research OS is research-neutral. Do not assume ML, GPU, datasets, baselines, or paper output.
- Long-running loops must have a human-approved cycle limit, wall-clock limit, and stop condition.
- Do not run LLM-written code outside an approved sandbox.
