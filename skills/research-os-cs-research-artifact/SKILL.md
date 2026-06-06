---
name: research-os-cs-research-artifact
description: Run computer science research artifact workflows in Research OS across algorithms, systems, software engineering, security, databases, programming languages, HCI, and artifact evaluation, including problem specs, invariants, complexity arguments, system design records, benchmark protocols, threat models, and artifact evaluation packs.
---

# Research OS CS Research Artifact

Use this skill for computer science research design, algorithm analysis, system artifact planning, benchmark protocol, threat modeling, or artifact evaluation.

## Workflow

1. Read `domain_profiles/computer-science/profile.yaml` and `domain_profiles/computer-science/agents.yaml`.
2. Read control files and route code execution, benchmark runs, or artifact mutation through `research-os-execution-harness`.
3. Route the algorithm, system, protocol, or artifact through `research-os-research-kernel`: the artifact is the candidate; correctness, complexity, benchmark, threat, and artifact-eval checks are evaluator contracts.
4. Write a problem spec: interface, inputs, outputs, constraints, workloads, and success criteria.
5. If algorithmic, record invariants, edge cases, proof obligations, and complexity assumptions.
6. If systems-oriented, record architecture, dependency boundaries, environment, observability, and artifact inventory.
7. If security-relevant, record assets, adversaries, trust boundaries, and misuse risks.
8. Define benchmark protocol and replay plan before performance claims.
9. Preserve failed invariants, benchmark regressions, and artifact failures as `negative_result` or `search_trace`.
10. Produce an artifact evaluation pack with documentation, consistency, completeness, exercisability, and reuse notes.

## Boundaries

- Do not publish exploit-enabling detail or private infrastructure notes without human review.
- Do not claim reproducibility without artifact inventory and manifest-linked replay steps.
- Use `templates/domain/computer-science/cs_research_case.template.yaml` for durable artifacts.

## References

- Read `references/cs_research_artifact_workflow.md` for algorithm/system/security/artifact routes.
