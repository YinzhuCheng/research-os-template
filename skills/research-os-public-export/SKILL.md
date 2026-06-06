---
name: research-os-public-export
description: Prepare public export packages for Codex Research OS projects with strict PUBLIC/PRIVATE separation, privacy scanning, provenance summaries, and no external upload. Use when Codex should package or audit shareable research materials.
---

# Research OS Public Export

Use this skill only when the user wants a public package or shareable snapshot.

## Workflow

1. Confirm public export is allowed by the current phase gate.
2. Run `scripts/scan_privacy.ps1` against `PUBLIC/` and `PROVENANCE/`.
3. If the scan fails, stop and report the offending paths.
4. Run `scripts/export_public.ps1`.
5. Record the export in `PROVENANCE/run_manifest.jsonl`.
6. Do not upload or push anywhere unless the user explicitly asks.

## Quick Checks

- Read `references/export_policy.md` before changing export behavior.
- Never include raw `PRIVATE/` files in export bundles.
