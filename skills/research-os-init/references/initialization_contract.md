# Initialization Contract

## Required Inputs

At least one of:

- GPT or Codex conversation transcript.
- Research plan draft.
- Simple experiment demo or code.
- Dataset description.
- Target venue or publication goal.

## Required Outputs

- `research_project.yaml` with language, intervention, venue, phase, and budget.
- Research brief with question, motivation, hypotheses, minimal experiment, and success criteria.
- First work order with allowed paths and forbidden paths.
- Alignment dossier request for the decision maker.

## Extraction Rules

- Convert vague ideas into falsifiable hypotheses.
- Preserve user uncertainty as open questions.
- Separate user preference from evidence.
- Keep private raw material out of `PUBLIC/`.
