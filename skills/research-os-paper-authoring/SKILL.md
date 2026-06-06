---
name: research-os-paper-authoring
description: Write formal submission-ready papers from Codex Research OS results, target venue templates, submission requirements, example manuscripts, claim-evidence matrices, figures, tables, and appendices. Default output is English LaTeX even when internal project notes are Chinese.
---

# Research OS Paper Authoring

Use this skill when turning research outputs into a manuscript.

## Workflow

1. Read target venue, submission rules, claim-evidence matrix, result analysis, figure plan, and appendix plan.
2. Write English LaTeX by default unless `language_mode: en-only` already applies to all materials.
3. Use claims only if they have evidence links.
4. Keep abstract, introduction, method, experiments, results, limitations, and appendix aligned.
5. Generate or update:
   - `PUBLIC/paper/main.tex`,
   - `PUBLIC/paper/appendix.tex`,
   - `PUBLIC/paper/references.bib`,
   - `PUBLIC/paper/submission_checklist.md`.
6. Hand off layout and figure concerns to `research-os-visual-communication`.

## Quick Checks

- Read `references/latex_authoring.md` before writing manuscript text.
- Avoid final bullet lists in manuscript prose unless the venue style explicitly accepts them.
- Never invent citations or results.
