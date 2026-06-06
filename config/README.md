# Config

This directory stores project configuration and JSON schemas.

Key files:

- `research_project.yaml`: project profile, language mode, privacy posture, dissemination settings, resource guard, and feasibility-probe defaults.
- `schemas/`: structured contracts for project config, skills, domain profiles, agent capabilities, research-kernel objects, integrations, and copilot packets.

Configuration rules:

- Do not fill in a model, dataset, baseline, budget, provider, venue, or paper goal unless it is present in researcher material or a confirmed decision.
- Keep real secrets out of config files. Store only environment variable names or secret-store references.
- If a new durable object enters the main route, add a schema, template, validator, and doc-map entry.
