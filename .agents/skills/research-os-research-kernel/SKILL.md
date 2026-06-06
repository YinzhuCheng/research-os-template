---
name: research-os-research-kernel
description: Maintain the Research OS v3.2 generate-evaluate-update-human gate kernel, including candidates, evaluator contracts, evaluation results, belief state, search trace, negative results, next-action policy, and explicit computation checklists.
---

# Research OS Research Kernel

Use this skill whenever a research task should move from an idea, domain artifact, or external component into the unified Research OS loop.

## Workflow

1. Read `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, `config/research_project.yaml`, and `config/schemas/research_kernel.schema.json`.
2. Identify or create the active kernel cycle using `templates/research_kernel/research_cycle.template.yaml`.
3. Normalize the current proposal into `candidate`: conjecture, model, method, algorithm, system, estimand, design, protocol, or other research object.
4. Define at least one `evaluator_contract` before treating the candidate as actionable.
5. For each evaluator, list the calculation or check explicitly: `metric_or_check`, `formula_or_procedure`, `inputs`, `units_or_scale`, `acceptance_threshold`, `resource_estimate`, `failure_mode`, and `replay_note`.
6. Record evaluation outcomes as `evaluation_result`; inconclusive and failed outcomes must enter `negative_result` or `search_trace`.
7. Update `belief_state` with assumptions, uncertainty, evidence links, and confidence level.
8. Use `next_action_policy` to decide whether to continue, revise, change evaluator, ask a human, stop, or export.
9. Apply `human_judgment_gate` before public claims, real resources, external writeback, privacy boundary changes, or phase changes.

## Boundaries

- Do not bypass domain profiles; the kernel provides the shared state machine, while domain skills provide field-specific taste.
- Do not execute code, spend resources, or write external systems unless `research-os-execution-harness` and `research-os-resource-guard` allow it.
- Do not discard failed candidates. Negative and inconclusive results are reusable research assets.
- Do not add a new main-route skill unless it has kernel binding, schema/template support, validator coverage, doc-map presence, and mirror validation.

## References

- Read `references/kernel_workflow.md` for the canonical loop and anti-spaghetti rules.
- Use `assets/kernel_cycle_notes.template.md` for human-readable kernel cycle notes.
