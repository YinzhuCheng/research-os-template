# Three-Phase And Final Product Plan

## Execution Rules

- Read this plan, `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml` before major workflow changes.
- Update plan status and gap audits after substantive work.
- Run relevant validation before committing.
- Do not read, write, or commit `PRIVATE/` material.
- Stop for real resources, credentials, external writeback, public release, submission, or budget overrun.

## Goal

Research OS exposes three user-facing macro phases:

1. Initialization.
2. Semi-automated research loop.
3. Final product.

The research loop is acceptance-gated:

`accept or revise previous artifact -> align next plan -> record user choice and free-form input -> execute and analyze -> return to acceptance`

If the researcher rejects the previous artifact, the system must revise the current artifact instead of planning the next step.

## Internal Stages

- `initialization_intake`
- `loop_acceptance_gate`
- `loop_plan_alignment`
- `loop_user_decision`
- `loop_execute_analyze`
- `final_product_selection`
- `final_product_production`
- `export_release_gate`

## Final Product Tracks

- Paper: target venue, venue template, comparable papers, English LaTeX/PDF, review/rebuttal iteration.
- Report: process-rich output, initial data, negative results, reproduction details, HTML/LaTeX/PDF/PPT targets.
- Software: stable, engineered, polished, user-friendly productization with documentation and preserved research artifacts.

## Archive Requirements

The app collects an archive description, shows current phase and git status, creates a local git snapshot, appends `PROVENANCE/archive_index.jsonl`, and refreshes `PUBLIC/archive_index.json`. Archives must not include `PRIVATE/`, real credentials, cookies, tokens, or authorization headers.
