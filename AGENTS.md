# Codex Research OS Desktop Rules

These rules apply to this repository. They are written for Codex and later agents working on Research OS Desktop.

## Priority Order

When instructions conflict, use this order:

1. Latest user instruction in the current thread.
2. `CONTROL/work_order.yaml` and `CONTROL/phase_gate.yaml`.
3. This `AGENTS.md`.
4. `config/research_flow.yaml` process contract.
5. `config/research_project.yaml` and schemas.
6. Current docs and dashboard data.
7. Historical `PLAN/` and `PROVENANCE/` records.

## Use Repo Skills First

- Before a research task, identify the relevant repo skill under `skills/` or `.agents/skills/`.
- Read the selected `SKILL.md` before using it.
- Use `research-os-orchestrator` as the default entry skill for routing.
- Use `research-os-research-kernel` before domain-specific research work.
- Use domain skills only after the kernel has a candidate and evaluator contract.
- Use `research-os-execution-harness` before mutating research artifacts or running experiments.
- If no skill applies, continue with general Codex behavior and record the gap if the task should become a durable Research OS route.

## Canonical Flow

The canonical flow is defined in `config/research_flow.yaml`.

User-facing macro phases:

`initialization -> semi_automated_research_loop -> final_product`

Internal controlled stages:

`initialization_intake -> loop_acceptance_gate -> loop_plan_alignment -> loop_user_decision -> loop_execute_analyze -> final_product_selection -> final_product_production -> export_release_gate`

The main product surface is the Research OS Desktop app. The first workflow is desktop material intake in a `.rosproj` project. Do not ask the retired fixed five-question intake. After material profiling, ask exactly three targeted questions, each with a recommended answer, options, and an Other/free-form path.

During the loop phase, do not advance past `loop_acceptance_gate` unless the researcher accepts the previous artifact. If the researcher rejects it or gives revision instructions, keep the loop in revision mode and update the current artifact before planning the next step.

Every user-facing choice prompt, including final product selection and archive descriptions, must provide a recommended option, concrete defaults, and a natural-language free-form path.

## Research Neutrality

- Do not assume an LLM, machine learning task, software project, dataset, baseline, paper, venue, or budget by default.
- If input material is insufficient, create alignment questions and pending decisions instead of inventing tools, providers, baselines, datasets, sample sizes, or budgets.
- `feasibility_probe` means the smallest useful validation path. Its budget and tools must come from researcher material or confirmed decisions.

## Language And Outputs

- Repository documentation is English-first.
- The desktop app UI may default to Chinese.
- Final product flows run only after `final_product_selection` or an explicit researcher request.
- Paper writing, LaTeX, visual paper polish, review/rebuttal, and submission flows run only when `dissemination.paper_enabled: true`, the paper track is selected, or the researcher explicitly asks for a paper/submission.
- Report output may include more process, initial data, negative results, and reproducibility detail than a paper. Supported report targets are HTML, LaTeX/PDF, and PPT when enabled.
- Software output defaults to stable, engineered, polished, user-friendly productization with documentation and preserved intermediate research artifacts unless the researcher adjusts the target in natural language.
- Without a final product target, default outputs are research briefs, validation reports, audit packs, reproducibility packs, or decision memos.

## Control And Audit

- Before mutating work, read `CONTROL/work_order.yaml`, `CONTROL/phase_gate.yaml`, and `config/research_project.yaml`.
- Write only inside `allowed_paths`; treat `forbidden_paths` as hard boundaries.
- After substantive work, append `PROVENANCE/run_manifest.jsonl`.
- Record resource use in `PROVENANCE/resource_ledger.jsonl`.
- Human confirmation is required for real resource use, credentials, budget overrun, external writeback, public export, and submission.
- Do not clean build files, caches, logs, raw outputs, validation reports, or intermediate experiment artifacts unless the user explicitly asks for cleanup and names the target paths.

## Privacy And Credentials

- `PUBLIC/` contains public or sanitized material only.
- `PRIVATE/` is ignored by git and is the default location for raw intake material, private conversations, sensitive data, and private audit material.
- Never write real API keys, platform tokens, cookies, auth headers, SSH private keys, cloud passwords, or real credentials to the repository.
- If credentials are needed, record only environment variable names, secret-store paths, IAM role names, or short-lived credential retrieval procedures.

## Evidence And Freshness

- Refresh time-sensitive information online and record sources when decisions depend on literature status, tools/APIs, prices, venue rules, dataset licenses, legal/ethics requirements, or external resource availability.
- If freshness cannot be verified, mark the claim as `unverified` or `freshness_risk: high`.

## Git

- This is an independent git repository for Research OS Desktop.
- Do not revert unrelated user or external changes.
- Run relevant validation scripts before committing.
- Report checks that could not be run.
