---
name: research-os-replay-eval-harness
description: Design replayable evaluation and audit harnesses for Research OS runs, including manifest replay, artifact integrity checks, low-cost monitoring, terminal-state truthfulness, and regression validation.
---

# Research OS Replay Eval Harness

Use this skill when a Research OS task needs reproducibility checks, replay records, monitoring, or post-run evaluation.

## Workflow

1. Read `PROVENANCE/run_manifest.jsonl`, `PROVENANCE/resource_ledger.jsonl`, and any active harness run record.
2. Identify replay inputs:
   - code or template versions;
   - source files and hashes;
   - configuration;
   - environment assumptions;
   - artifacts and terminal state.
3. Define low-cost monitoring first:
   - process status;
   - log tail;
   - output file existence;
   - timestamp progress;
   - resource counters.
4. Record truthful outcomes: succeeded, failed, timed out, cancelled, partial, blocked, or unverified.
5. Add regression checks that can run locally without paid resources whenever possible.
6. Run `scripts/check_harness.ps1` and any task-specific validation script.

## Boundaries

- Do not infer success from the existence of an output file alone.
- Do not rewrite historical manifests to hide failures.
- Do not call paid external APIs for replay unless explicitly authorized.
