---
name: research-os-math-discovery
description: Run fundamental mathematics discovery workflows in Research OS without default formalization, including definition normalization, example banks, conjecture generation, counterexample search, lemma decomposition, proof strategy, proof-gap review, and human-in-loop theorem notes.
---

# Research OS Math Discovery

Use this skill for basic mathematics, proof-oriented research, conjecture work, counterexample search, or theorem-note drafting.

## Workflow

1. Read `domain_profiles/fundamental-mathematics/profile.yaml` and `domain_profiles/fundamental-mathematics/agents.yaml`.
2. Read `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml`; route any mutation or experiment through `research-os-execution-harness`.
3. Route the conjecture or theorem note through `research-os-research-kernel`: `conjecture_card` is the candidate; counterexample search and proof-gap review are evaluator contracts.
4. Start with definitions: normalize objects, assumptions, notation, quantifiers, and excluded cases.
5. Build examples before proof attempts: canonical, small, degenerate, and boundary cases.
6. Generate conjectures only after examples or literature cues are recorded.
7. Search for counterexamples before proof strategy. If a counterexample is found, revise or retire the conjecture and preserve it as `negative_result` or `search_trace`.
8. Decompose the proof route into lemmas and dependencies; label every unresolved step.
9. Run proof-referee review and emit `proof_gap_report` before any public theorem claim.

## Boundaries

- Do not default to Lean, Coq, Isabelle, or other formalization tools. Use `formalization_future_slot` only as a future status.
- Do not present a `proof_sketch` as a proof. Public theorem notes require `human_checked`.
- Do not write outside work order `allowed_paths`; never move raw private notes into `PUBLIC/`.
- Use `templates/domain/fundamental-mathematics/math_discovery_case.template.yaml` for durable artifacts.

## References

- Read `references/math_discovery_workflow.md` for the role sequence, artifact statuses, and failure modes.
