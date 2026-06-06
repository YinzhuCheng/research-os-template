---
name: research-os-orchestrator
description: Entry skill for converting research conversations, draft plans, or experiment demos into Codex Research OS projects. Use when the user asks to initialize, route, continue, audit, or coordinate a structured research project with language mode, human intervention level, privacy boundaries, and stage gates.
---

# Research OS Orchestrator

Use this as the entry skill. Keep orchestration short; load sub-skill references only when needed.

## Workflow

1. Inspect `config/research_project.yaml`, `CONTROL/phase_gate.yaml`, `PLAN/05_IMPLEMENTATION_CHECKLIST.md`, and `PLAN/06_GAP_AUDIT.md` if present.
2. Determine:
   - source type: dialogue, draft plan, demo code, existing project, or continuation;
   - language mode: `zh-first` by default, or `en-only` if requested;
   - intervention level: `low` by default, with stage gates;
   - privacy boundary: always `PUBLIC/` vs `PRIVATE/`.
3. Route:
   - initialization or import: use `research-os-init`;
   - intent confirmation: use `research-os-alignment`;
   - execution and audit: use `research-os-execution-harness`;
   - evidence and literature: use `research-os-evidence`;
   - paper writing: use `research-os-paper-authoring`;
   - figures and visual polish: use `research-os-visual-communication`;
   - prose/fact polish: use `research-os-polish-factcheck`;
   - review/rebuttal: use `research-os-review-rebuttal`;
   - public package: use `research-os-public-export`.
4. Before any mutating work, require or skip confirmation according to `intervention_level`.
5. Never move raw private material into `PUBLIC/`. Create a sanitized summary instead.
6. After substantive work, update the relevant checklist, gap audit, manifest, and decision records.

## Quick Checks

- Read `references/routing.md` before changing routing or stage-gate behavior.
- If a requested action touches external writeback, submission, public export, budget overrun, or privacy policy changes, stop for human confirmation.
- If the user asks for implementation, create or reuse a work order before editing project artifacts.
