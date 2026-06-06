# Math Discovery Workflow

Default loop:

1. `math-definition-normalizer`: scope objects, notation, assumptions, and excluded cases.
2. `math-example-builder`: produce canonical, small, degenerate, and boundary examples.
3. `math-conjecture-generator`: propose conjectures from observed patterns.
4. `math-counterexample-finder`: attack the conjecture before any proof attempt.
5. `math-proof-strategist`: propose lemmas, proof routes, and theorem dependencies.
6. `math-proof-referee`: identify gaps, hidden assumptions, circularity, and unsupported reductions.

Required statuses:

- `conjecture`: plausible but not proved.
- `counterexample_found`: disproved or needs revision.
- `proof_sketch`: strategy exists but gaps may remain.
- `proof_gap`: unresolved step is explicitly recorded.
- `human_checked`: a human mathematician has reviewed the argument.
- `formalization_future_slot`: formalization is deferred, not claimed.

Acceptance rule: a theorem-like public claim requires definition scope, examples, counterexample search, proof-gap review, and human review.
