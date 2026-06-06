---
name: research-os-feasibility-probe
description: Define or evaluate minimal feasibility probes for any research domain, without defaulting to LLMs, machine learning, datasets, papers, fixed budgets, or specific tools. Use when Codex must turn a research idea into the smallest researcher-budgeted validation path and decide how to continue after success, failure, or unclear results.
---

# Research OS Feasibility Probe

Use this skill before large experiments or expensive resource use.

## Workflow

1. Read `config/research_project.yaml`, `PUBLIC/research_brief.md`, `CONTROL/work_order.yaml`, and the latest alignment dossier if present.
2. Identify the validation object: claim, mechanism, prototype, dataset, intervention, theory, artifact, observation, or other project-specific target.
3. Use only researcher-provided or aligned resources:
   - budget amount,
   - time,
   - compute,
   - lab/material resources,
   - cloud/API/model resources,
   - human participation or annotation,
   - equipment or external services.
4. Draft the smallest probe that can change the decision:
   - what evidence is sufficient to continue,
   - what evidence is sufficient to stop,
   - what uncertainty means and how to reduce it.
5. Create a next-action policy:
   - success: expand, replicate, or formalize;
   - failure: narrow, change method, change assumption, or stop;
   - unclear: collect missing evidence, improve measurement, or ask decision maker.
6. Update claim status conservatively.

## Quick Checks

- Read `references/probe_rules.md` before writing a probe.
- Do not assume an LLM, model provider, ML benchmark, dataset, baseline, or paper target.
- Do not spend real resources without `research-os-resource-guard` and required confirmation.
