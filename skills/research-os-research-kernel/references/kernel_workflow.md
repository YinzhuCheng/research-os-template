# Research Kernel Workflow

The kernel is the shared program underneath domain-specific research taste:

`generate candidate -> evaluate candidate -> update belief state -> human gate -> next action`

## Core Objects

- `candidate`: the object under consideration, such as conjecture, model, method, algorithm, system, estimand, design, or protocol.
- `evaluator_contract`: the explicit check that can judge the candidate.
- `evaluation_result`: the outcome of an evaluator contract.
- `belief_state`: assumptions, uncertainty, evidence links, and confidence after an update.
- `search_trace`: durable trace of attempts, revisions, failed attacks, and explored branches.
- `negative_result`: a failed, disproven, unstable, leaking, unidentified, or otherwise unusable candidate retained for reuse.
- `next_action_policy`: continue, revise, change evaluator, ask human, stop, or export.
- `human_judgment_gate`: human review required by risk, claim strength, resource use, privacy, or phase change.

## Computation Checklist

Every evaluator contract must include:

- `metric_or_check`
- `formula_or_procedure`
- `inputs`
- `units_or_scale`
- `acceptance_threshold`
- `resource_estimate`
- `failure_mode`
- `replay_note`

Mathematics may use non-numeric checks such as example enumeration, counterexample search, lemma dependency checking, or proof-gap scoring.
Other domains use the same fields for stability, error, benchmark, leakage, ablation, diagnostics, uncertainty, sensitivity, complexity, or artifact evaluation.

## Anti-Spaghetti Rules

- A skill is not part of the main route unless it is represented in routing, docs, validation, and skill mirror checks.
- Domain knowledge enters through `domain_profiles/`, `templates/domain/`, schemas, rubrics, and source registries.
- External components remain adapters or registry entries; they do not become the core architecture.
- Failed and inconclusive work stays visible in `negative_result` or `search_trace`.
