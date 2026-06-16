---
name: research-os-software-productization
description: Turn accepted Research OS research assets into stable, engineered, polished, user-friendly software artifacts with documentation, tests, usability checks, and preserved intermediate research records.
---

# Research OS Software Productization

Use this skill when the final product track includes software.

## Workflow

1. Read the `final_product_plan`, accepted research artifact, evidence links, current codebase state, and user free-form expectations.
2. Confirm the product target with a choice prompt that includes a recommended engineering scope, alternatives, and natural-language input.
3. Define target user, primary workflow, supported platform or runtime, input/output behavior, documentation, tests, and release expectation.
4. Build to the default quality target unless the researcher changes it: stable, engineered, polished, user-friendly, and aligned with software engineering norms.
5. Preserve intermediate research artifacts, logs, prompts, validation reports, and decision records.
6. Run tests, lint/static checks when available, and browser or CLI QA when relevant.
7. Stop for human confirmation before external deployment, publication, package release, credentials, paid resources, or external writeback.

## Boundaries

- Do not treat a research demo as production software without explicit scope.
- Do not invent platform, package manager, user workflow, or release target when the researcher has not supplied one.
- Do not remove experiment artifacts while productizing.

## References

- Productization workflow: `references/software_productization_workflow.md`
- Product brief template: `assets/software_product_brief.template.md`
