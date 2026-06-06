---
name: research-os-analysis
description: Analyze experiment results in Codex Research OS projects, including main results, ablations, cost-performance tradeoffs, failure cases, statistics, threats to validity, and claim-evidence updates.
---

# Research OS Analysis

Use this skill after experiment runs produce results.

## Workflow

1. Read run manifests, result files, work orders, and claim-evidence matrix.
2. Separate observed results from interpretation.
3. Produce:
   - main result summary,
   - ablation analysis,
   - resource-performance analysis,
   - failure taxonomy,
   - threats to validity,
   - claim updates.
4. Retire or narrow unsupported claims.
5. If feasibility results contradict expectations, hand off to `research-os-feasibility-probe` for adjustment policy before expanding scope.
6. Hand off figure needs to `research-os-visual-communication`.

## Quick Checks

- Read `references/analysis_rules.md` before writing final analysis.
- Do not smooth away failed or null results.
