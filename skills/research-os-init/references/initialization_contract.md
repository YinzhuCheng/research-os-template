# Initialization Contract

## Required Inputs

At least one of:

- GPT or Codex conversation transcript.
- Research plan draft.
- Simple experiment demo or code.
- Dataset description.
- Dissemination goal, if any.

## Required Outputs

- `research_project.yaml` with language, intervention, research profile, dissemination target, phase, and resource budget.
- Research brief with question, motivation, hypotheses, feasibility probe, success criteria, unclear-result policy, and public boundary.
- First work order with allowed paths and forbidden paths.
- Alignment dossier request for the decision maker.

## Extraction Rules

- Convert vague ideas into falsifiable hypotheses.
- Preserve user uncertainty as open questions.
- Separate user preference from evidence.
- Keep private raw material out of `PUBLIC/`.
- Treat budget, tools, model use, sample size, equipment, data source, comparison object, and paper target as researcher-specific variables.
- If a variable is not inferable from the source, mark it unresolved and ask through alignment.
