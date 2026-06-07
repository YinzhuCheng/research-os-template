# Skill Suite Plan

## Principles

The skill system should stay modular. Entry skills route, domain skills contribute field-specific judgment, and execution skills enforce audit, resource, and privacy boundaries.

## Main Skills

- `research-os-orchestrator`: route work, read stage state, and coordinate the next action.
- `research-os-research-kernel`: structure candidates, evaluator contracts, computation checks, results, belief state, traces, negative results, and human gates.
- `research-os-copilot`: handle desktop intake, exactly three targeted questions, and sanitized `PUBLIC/research_state.json`.
- `research-os-alignment`: clarify intent, assumptions, tradeoffs, and phase gates.
- `research-os-execution-harness`: execute approved work orders and record audit data.
- `research-os-resource-guard`: protect real budgets and scarce resources.
- `research-os-evidence`: manage hypotheses, literature, evidence, counterevidence, and claim matrices.
- `research-os-analysis`: analyze results, ablations, failures, threats, and claim updates.
- `research-os-final-product`: coordinate paper, report, and software final-product tracks.
- `research-os-public-export`: prepare sanitized exports after explicit confirmation.

## Routing Rules

Substantive research goes through `research-os-research-kernel` before domain-specific execution. Real resource use goes through `research-os-resource-guard`. Mutating work goes through `research-os-execution-harness`. Time-sensitive external claims require `research-os-live-evidence-refresh`.
