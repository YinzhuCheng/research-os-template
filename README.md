# Codex Research OS Template

This repository is a research-neutral Codex Research OS template. It turns research notes, draft plans, conversations, papers, zips, or demos into an auditable human-in-loop research workspace.

It does not assume an LLM, machine learning task, dataset, baseline, paper, venue, or budget by default. Those decisions must come from researcher material or explicit human confirmation.

## Main Entrypoints

- [Material-first Copilot](PUBLIC/copilot.html): browser cockpit for initial material intake.
- [Public Dashboard](PUBLIC/index.html): project navigation and document reader.
- [Quick Start](docs/start-here.html): onboarding for general researchers and Codex beginners.
- [Technical Report](docs/technical-report.html): repository route for future agents and maintainers.
- [Copilot Bridge Doc](docs/codex-browser-copilot.html): browser-to-Codex bridge details.
- [Domain Modes](docs/domain-modes.html): five domain-specific research paradigms.
- [Research Kernel Template](templates/research_kernel/research_cycle.template.yaml): shared feedback computation loop.
- [Document Map](docs/doc_map.yaml): structured navigation.

## Research OS v3.3

v3.3 adds a material-first Codex Browser Copilot:

- The first screen asks for free text or uploaded material, not a fixed questionnaire.
- Codex profiles the material and asks exactly three targeted questions.
- Every question has a recommended answer, selectable options, and an Other/free-form path.
- Initialization reports include motivation, goals, contribution claims, related work and gaps, reference links, conditional theory track, conditional experiment track, minimum validation, and repository links.
- Browser submissions enqueue structured packets; Codex confirms before analysis or execution.

## Research Kernel

All substantive research loops pass through:

`candidate -> evaluator_contract -> evaluation_result -> belief_state -> search_trace/negative_result -> next_action_policy -> human_judgment_gate`

Every evaluator must list the computation or check: metric, procedure, inputs, scale, threshold, resource estimate, failure mode, and replay note. This keeps skills from becoming a loose toolbox.

## Privacy And Resources

- `PUBLIC/` contains public or sanitized material only.
- `PRIVATE/` is ignored by git and holds raw private material at runtime.
- Real API keys, tokens, cookies, SSH keys, authorization headers, and cloud credentials must never be written to the repository.
- Paid resources, external writeback, public export, and submission require human confirmation.
- Reference download scripts only attempt open-access URLs or landing pages and do not bypass paywalls.

## Useful Commands

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_bridge.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_intake_schema.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_state.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1
```

To run the local browser bridge:

```powershell
python .agents/plugins/plugins/research-os-copilot/scripts/research_os_copilot_server.py --serve
```
