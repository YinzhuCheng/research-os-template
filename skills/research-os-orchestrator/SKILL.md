---
name: research-os-orchestrator
description: Entry skill for converting research conversations, draft plans, or experiment demos into Codex Research OS projects. Use when the user asks to initialize, route, continue, audit, or coordinate a structured research project with language mode, human intervention level, privacy boundaries, and stage gates.
---

# Research OS Orchestrator

Use this as the entry skill. Keep orchestration short; load sub-skill references only when needed.

## Workflow

1. Inspect `config/research_flow.yaml`, `config/research_project.yaml`, `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, `PLAN/05_IMPLEMENTATION_CHECKLIST.md`, and `PLAN/06_GAP_AUDIT.md` if present.
2. Determine:
   - source type: dialogue, draft plan, demo code, existing project, or continuation;
   - language mode: `zh-first` by default, or `en-only` if requested;
   - intervention level: `low` by default, with stage gates;
   - privacy boundary: always `PUBLIC/` vs `PRIVATE/`.
3. Route:
   - process contract: use `config/research_flow.yaml` as the canonical stage sequence and skill handoff contract;
   - material-first browser intake: use `research-os-copilot` for pending `CONTROL/copilot_inbox/` packets, `PUBLIC/copilot.html` interactions, exactly three targeted questions, and initialization reports;
   - research kernel: normalize any substantive research loop through `research-os-research-kernel` first, producing or updating `candidate`, `evaluator_contract`, `belief_state`, `search_trace`, `negative_result`, `next_action_policy`, and `human_judgment_gate`;
   - domain-specific research mode: inspect the active domain profile in `domain_profiles/` first, then route to one of:
     `research-os-math-discovery`, `research-os-applied-math-modeling`,
     `research-os-ml-research-protocol`, `research-os-cs-research-artifact`, or
     `research-os-statistical-inference`;
   - initialization or import: use `research-os-init`;
   - intent confirmation: use `research-os-alignment`;
   - feasibility check: use `research-os-feasibility-probe`;
   - resource budgeting and spend control: use `research-os-resource-guard`;
   - live or time-sensitive evidence: use `research-os-live-evidence-refresh`;
   - harness audit: use `research-os-harness-audit`;
   - execution and audit: use `research-os-execution-harness`;
   - evidence and literature: use `research-os-evidence`;
   - final product phase: use `research-os-final-product` when the researcher chooses paper, research report, software, or a multi-track final product;
   - paper writing: use `research-os-paper-authoring` only when `dissemination.paper_enabled` is true, the researcher explicitly asks for a paper, or the final product plan selects paper;
   - report writing: use `research-os-report-authoring` when the final product plan selects a process-rich research report;
   - software productization: use `research-os-software-productization` when the final product plan selects software;
   - figures and visual polish: use `research-os-visual-communication` when a report, paper, software document, dashboard, or public artifact needs visual communication;
   - prose/fact polish: use `research-os-polish-factcheck`;
   - review/rebuttal: use `research-os-review-rebuttal` only for papers or formal reports;
   - public package: use `research-os-public-export`.
4. Before any mutating work, require or skip confirmation according to `intervention_level`.
5. Never move raw private material into `PUBLIC/`. Create a sanitized summary instead.
6. After substantive work, update the relevant checklist, gap audit, manifest, and decision records.

## Quick Checks

- Read `references/routing.md` and `config/research_flow.yaml` before changing routing or stage-gate behavior.
- If a requested action touches external writeback, submission, public export, budget overrun, real resources, credentials, or privacy policy changes, stop for human confirmation.
- If the user asks for implementation, create or reuse a work order before editing project artifacts.
