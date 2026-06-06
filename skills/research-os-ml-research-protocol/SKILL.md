---
name: research-os-ml-research-protocol
description: Run machine learning research protocol workflows in Research OS across classical ML, reinforcement learning, transfer learning, computational learning theory, computer vision, NLP, and generative AI, including task cards, data cards, baseline matrices, ablation plans, leakage audits, evaluation harness specs, and reproducibility packs.
---

# Research OS ML Research Protocol

Use this skill for ML research design, benchmark planning, evaluation protocol, data/license audit, baseline selection, ablation planning, or reproducibility review.

## Workflow

1. Read `domain_profiles/machine-learning/profile.yaml` and `domain_profiles/machine-learning/agents.yaml`.
2. Read control files and route mutation, code execution, or experiment runs through `research-os-execution-harness`.
3. Create a task card: subfield, inputs, outputs, metric, target claim, and failure modes.
4. Create a data card: source, license, split policy, privacy, and benchmark contamination risk.
5. Define baselines before proposing performance claims.
6. Define ablations, negative controls, seed policy, and cost-performance checks.
7. Write an `eval_harness_spec` with environment capture, replay command, and manifest links.
8. Run result-referee review for leakage, statistical validity, ablation sufficiency, and reproducibility.

## Boundaries

- Do not claim SOTA or benchmark superiority without current evidence refresh and baseline context.
- Do not assume data use rights; licenses and privacy notes must be explicit.
- Do not run training or evaluation unless the work order and resource guard allow it.
- Use `templates/domain/machine-learning/ml_research_case.template.yaml` for durable artifacts.

## References

- Read `references/ml_research_protocol_workflow.md` for subfield routing and quality gates.
