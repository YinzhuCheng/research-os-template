---
name: research-os-statistical-inference
description: Run statistics research workflows in Research OS, including estimand-first framing, identification assumptions, sampling and power planning, model diagnostics, uncertainty statements, sensitivity analysis, p-value and interval interpretation, Bayesian reporting, and statistical ethics checks.
---

# Research OS Statistical Inference

Use this skill for statistical research design, causal or predictive inference, sampling, diagnostics, uncertainty reporting, or sensitivity analysis.

## Workflow

1. Read `domain_profiles/statistics/profile.yaml` and `domain_profiles/statistics/agents.yaml`.
2. Read control files and use `research-os-execution-harness` before computation, mutation, or public export.
3. Route the estimand, design, or model through `research-os-research-kernel`: estimand/design is the candidate; identification, power, diagnostics, uncertainty, and sensitivity are evaluator contracts.
4. Define the estimand before choosing a model: population, target quantity, exposure/intervention, outcome, contrast, and time horizon.
5. Record identification assumptions, confounding, measurement, and missingness risks.
6. Plan sampling, power or precision, multiplicity, and analysis decisions.
7. Define diagnostics, model checks, convergence checks, priors, or calibration checks as appropriate.
8. Preserve unidentified estimands, diagnostic failures, and sensitivity reversals as `negative_result` or `search_trace`.
9. Write uncertainty statements with effect size, intervals or posterior summaries, practical significance, and limitations.
10. Run sensitivity and ethics review before public statistical conclusions.

## Boundaries

- Do not reduce evidence to binary p-value significance.
- Do not publish statistical conclusions without estimand, method, uncertainty, diagnostics, and sensitivity limits.
- Do not expose private data or subgroup-sensitive details in `PUBLIC/`.
- Use `templates/domain/statistics/statistical_inference_case.template.yaml` for durable artifacts.

## References

- Read `references/statistical_inference_workflow.md` for estimand, diagnostics, uncertainty, and ethics gates.
