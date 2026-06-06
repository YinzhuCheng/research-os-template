---
name: research-os-harness-audit
description: Audit Codex Research OS control surfaces, including AGENTS.md, work orders, allowed and forbidden paths, phase gates, hooks, sandbox assumptions, MCP/tool boundaries, manifests, resource ledgers, privacy scans, and uncommitted changes.
---

# Research OS Harness Audit

Use this skill before real execution, public export, submission, or handoff.

## Workflow

1. Read `AGENTS.md`, `.codex/requirements.md`, `.codex/config.toml.example`, `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml`.
2. Check control surfaces:
   - project instructions exist,
   - allowed and forbidden paths are explicit,
   - real resources and credentials require confirmation,
   - run manifest and resource ledger exist,
   - public export has privacy scan,
   - hooks are examples unless explicitly enabled,
   - MCP usage has permission, cost, and data boundary notes.
3. Check git state and ignored artifacts without deleting anything.
4. Produce a harness audit report with pass/fail/warn items and next required decisions.

## Quick Checks

- Read `references/harness_audit_rules.md` before audit reporting.
- Treat hooks as guardrails, not as complete security boundaries.
- Prefer sandbox and approval settings over ad hoc broad access.
