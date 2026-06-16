---
name: research-os-alignment
description: Generate decision-maker alignment dossiers for Codex Research OS projects. Use when a research project has been initialized or a phase gate needs clarification of the researcher's real intent, assumptions, constraints, tradeoffs, and recommended next decisions.
---

# Research OS Alignment

Use this skill to keep automated research aligned with the researcher's real intent.

## Workflow

1. Read the research brief, project config, phase gate, latest work order, and gap audit.
2. Infer:
   - likely true motivation,
   - hidden assumptions,
   - conflicting goals,
   - underspecified constraints,
   - high-risk shortcuts,
   - next irreversible decisions.
3. Generate an alignment dossier:
   - concise summary,
   - what Codex thinks the researcher wants,
   - recommended decisions,
   - questions by priority,
   - assumptions Codex will use if unanswered.
4. Adjust question count by intervention level:
   - `low`: only highest-impact questions and recommended defaults;
   - `medium`: include methodological and writing tradeoffs;
   - `high`: include every material work-order decision.
5. Write confirmed decisions to `CONTROL/decision_records/`.

## Quick Checks

- Read `references/alignment_checklist.md` before writing a dossier.
- Do not ask questions answerable from repository files.
- Do not proceed past a phase gate if a required high-risk decision is unresolved.
