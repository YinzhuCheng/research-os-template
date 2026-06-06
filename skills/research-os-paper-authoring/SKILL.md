---
name: research-os-paper-authoring
description: Write formal submission-ready papers from Codex Research OS results, target venue templates, submission requirements, example manuscripts, claim-evidence matrices, figures, tables, and appendices. Default output is English LaTeX even when internal project notes are Chinese.
---

# Research OS Paper Authoring

Use this skill when turning research outputs into a manuscript and `dissemination.paper_enabled` is true or the researcher explicitly asks for paper writing.

## Workflow

1. Read dissemination target, venue or journal rules if provided, claim-evidence matrix, result analysis, figure plan, and appendix plan.
2. Write English LaTeX by default unless `language_mode: en-only` already applies to all materials.
3. Use claims only if they have evidence links.
4. Keep abstract, introduction, method, experiments, results, limitations, and appendix aligned.
5. Use `templates/latex/` as the source scaffold, then generate or update:
   - `PUBLIC/paper/main.tex`,
   - `PUBLIC/paper/appendix.tex`,
   - `PUBLIC/paper/references.bib`,
   - `PUBLIC/paper/submission_checklist.md`.
6. Hand off layout and figure concerns to `research-os-visual-communication`.
7. If no paper target is enabled, stop and create a report or decision memo work order instead.

## Quick Checks

- Read `references/latex_authoring.md` before writing manuscript text.
- `PUBLIC/paper/` is not a default tracked scaffold. Create it only after `dissemination.paper_enabled: true` or an explicit paper work order.
- Avoid final bullet lists in manuscript prose unless the venue style explicitly accepts them.
- Never invent citations or results.
