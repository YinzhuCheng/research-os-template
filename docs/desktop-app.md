# Research OS Desktop App

Research OS Desktop is the primary product surface. It uses `Tauri + React + Python sidecar` and opens local `.rosproj` projects.

## User Flow

1. Create or open a `.rosproj` file.
2. The app creates or uses the sibling project directory as the sandbox.
3. Submit material in the desktop intake panel.
4. Answer choice prompts with a recommended option, default options, and natural-language free-form input.
5. Approve or reject Codex commands in the approval queue.
6. Create git-backed archives before risky transitions.
7. Enter final product mode for paper, report, software, or multiple tracks.

## Project Layout

- `CONTROL/intake_queue/`: sanitized desktop intake packets.
- `CONTROL/choice_responses/`: user choices and natural-language supplements.
- `PUBLIC/research_state.json`: sanitized UI state.
- `PRIVATE/intake/`: raw material captured at runtime.
- `PROVENANCE/`: run manifests, ledgers, and archive records.
- `outputs/`: generated final products.

## Runtime Boundary

The React UI calls only the Python sidecar. The sidecar owns filesystem writes, approval decisions, state files, archives, and Codex SDK/app-server mediation.

Codex execution is optional. If Codex is unavailable, the runtime panel fails safely without changing project state.

## Removed Legacy Surface

The browser bridge and static browser cockpit are retired. Use [migration.md](migration.md) for the replacement map.
