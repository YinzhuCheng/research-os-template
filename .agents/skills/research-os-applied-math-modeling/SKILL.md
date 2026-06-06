---
name: research-os-applied-math-modeling
description: Run applied mathematics research workflows in Research OS, including problem-to-model translation, assumption ledgers, variable dictionaries, nondimensionalization, stability and error checks, numerical validation planning, sensitivity analysis, and interpretation limits.
---

# Research OS Applied Math Modeling

Use this skill for applied mathematics, modeling, simulation design, differential equations, optimization, stability analysis, approximation, or sensitivity studies.

## Workflow

1. Read `domain_profiles/applied-mathematics/profile.yaml` and `domain_profiles/applied-mathematics/agents.yaml`.
2. Read control files and use `research-os-execution-harness` before any mutation, simulation, code execution, or resource use.
3. Route the model through `research-os-research-kernel`: model candidate is the candidate; stability, error, validation, and sensitivity checks are evaluator contracts.
4. Translate the application question into variables, parameters, units, equations, objectives, and constraints.
5. Create a `model_assumption_ledger`; mark missing mechanisms and validity regimes.
6. Perform scale checks and nondimensionalization before interpreting numerical output.
7. Record a stability, well-posedness, approximation, or error-check path.
8. Define minimal numerical validation, sanity checks, baselines, and sensitivity probes.
9. Preserve unstable, dimensionally inconsistent, or invalid-regime models as `negative_result` or `search_trace`.
10. Separate mathematical conclusions from application recommendations.

## Boundaries

- No simulation run is implied by this skill. Execution requires an approved work order and resource guard.
- Do not publish application conclusions without assumptions, regimes, stability/error context, and sensitivity limits.
- Use `templates/domain/applied-mathematics/applied_math_model_case.template.yaml` for durable artifacts.

## References

- Read `references/applied_math_modeling_workflow.md` for the modeling loop and quality gates.
