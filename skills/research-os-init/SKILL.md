---
name: research-os-init
description: Initialize a Codex Research OS project from GPT conversations, research plan drafts, notes, PDFs, code snippets, or simple experiment demos. Use when Codex should normalize messy research inputs into config, research brief, hypotheses, privacy split, and first work orders.
---

# Research OS Init

Use this skill after `research-os-orchestrator` routes an initialization request.

## Workflow

1. Classify each source as public-safe, private raw material, or unknown.
2. Store raw or sensitive source descriptions in `PRIVATE/`; store sanitized summaries in `PUBLIC/`.
3. Create or update:
   - `config/research_project.yaml`,
   - `PUBLIC/research_brief.md`,
   - `PUBLIC/claim_evidence_matrix.yaml`,
   - `CONTROL/work_order.yaml`,
   - `CONTROL/phase_gate.yaml`,
   - `PROVENANCE/run_manifest.jsonl`.
4. Extract:
   - research question IDs,
   - falsifiable hypotheses,
   - candidate claims,
   - minimal experiment,
   - success and failure criteria,
   - unresolved decisions.
5. Hand off to `research-os-alignment` before execution begins.

## Output Requirements

- In `zh-first`, write internal docs in Chinese.
- In `en-only`, write all docs in English.
- Keep claims tentative until linked to evidence.
- Do not invent experimental results.

## Quick Checks

- Read `references/initialization_contract.md` before initializing a new project.
- If a source may contain private data, default it to `PRIVATE/` and create a sanitized summary.
