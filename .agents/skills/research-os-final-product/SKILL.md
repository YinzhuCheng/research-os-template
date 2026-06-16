---
name: research-os-final-product
description: Coordinate the final product phase for Research OS, including user selection of paper, research report, software, or multiple tracks, with evidence gates, free-form expectations, and handoff to track-specific authoring or productization skills.
---

# Research OS Final Product

Use this skill when the researcher chooses to leave the semi-automated research loop and turn accepted research assets into final products.

## Workflow

1. Read `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, `config/research_project.yaml`, `config/research_flow.yaml`, and `templates/yaml/final_product_plan.template.yaml`.
2. Confirm the previous research-loop artifact has passed `loop_acceptance_gate`.
3. Present product choices with a recommended option, concrete options, and a free-form natural-language path: paper, research report, software, or any combination.
4. Create or update a `final_product_plan` with selected tracks, target expectations, evidence requirements, intermediate-artifact policy, and human gates.
5. Route selected tracks to `research-os-paper-authoring`, `research-os-report-authoring`, or `research-os-software-productization`.
6. Preserve intermediate artifacts, logs, validation reports, prompts, raw outputs, and reproducibility records unless the researcher explicitly names cleanup targets.
7. Stop for human confirmation before public export, submission, software release, external upload, external writeback, credentials, or real resource use.

## Boundaries

- Do not invent target venues, templates, comparable papers, citations, datasets, results, or software requirements.
- Do not proceed from rejected research-loop artifacts.
- Do not publish, submit, upload, or write back externally without explicit approval.
- Do not move raw private material into `PUBLIC/`.

## References

- Workflow reference: `references/final_product_workflow.md`
- Product plan notes: `assets/final_product_plan_notes.template.md`
