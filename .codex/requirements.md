# Research OS Harness Requirements

This file documents the Codex control surface expected by the template. It is not an active session policy by itself. Copy or adapt `.codex/config.toml.example` only inside a trusted project.

## Minimum Expectations

- Keep `AGENTS.md` in the repository root.
- Prefer `sandbox_mode = "workspace-write"` and `approval_policy = "on-request"` for normal Research OS projects.
- Require human confirmation for external writeback, public export, real resource use, credentials, budget overrun, and submission.
- Use `config/research_flow.yaml` as the canonical process contract.
- Use repo skills before generic execution; keep `.agents/skills/` synchronized from `skills/`.

## Hook Coverage

Hooks are examples, not complete security boundaries.

- `PreToolUse`: reject clearly dangerous commands, credential leakage, unconfirmed real resource calls, and external writeback.
- `PostToolUse`: remind agents to record manifests, resource ledger entries, privacy scans, and failed/partial states.
- `Stop`: run strict schema validation, HTML trailing-content checks, privacy scan, package-artifact policy checks, harness checks, and phase-gate consistency checks before final handoff.

## MCP And External Tools

Any MCP server or connector must document:

- permissions and data boundary,
- rate limits and cost risks,
- whether external writeback is possible,
- whether private material may leave the workspace,
- what artifacts are safe to store in `PUBLIC/` or `PROVENANCE/`.

## Skill Discovery

- `skills/` is the authoritative template skill source.
- `.agents/skills/` is the repo-scoped Codex discovery mirror.
- After editing `skills/`, run `scripts/sync_skill_mirror.ps1` and `scripts/check_skill_mirror.ps1`.
- Before copying ideas from an external skill or plugin, record source, license, install path, risks, and adapter boundary in `docs/integrations/components.yaml`.
