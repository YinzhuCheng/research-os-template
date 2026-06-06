# Templates

This directory stores reusable Research OS scaffolds. Templates describe artifact structure; they are not evidence and they are not runtime-private material.

Main groups:

- `markdown/`: research briefs, evidence notes, feasibility reports, paper sections, review/rebuttal, and public export summaries.
- `yaml/`: structured packets, component registries, resource budgets, live-evidence refreshes, copilot intake/questions/initialization reports, and research-kernel objects.
- `domain/`: field-specific artifact templates for mathematics, applied mathematics, machine learning, computer science, and statistics.
- `research_kernel/`: the shared `candidate -> evaluator_contract -> evaluation_result -> belief_state -> search_trace/negative_result -> next_action_policy -> human_judgment_gate` loop.
- `latex/`: optional paper scaffold used only after a paper-oriented work order or explicit researcher decision.

`PUBLIC/paper/` should be generated from `templates/latex/` when needed; the default repository should not carry stale generated paper output.
