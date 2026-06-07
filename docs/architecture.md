# Desktop Architecture

Research OS Desktop uses a governed local runtime:

`React UI -> Python sidecar -> optional Codex SDK/app-server -> project sandbox`

The React UI never talks directly to Codex. It calls the sidecar over localhost for project management, state, approvals, archives, runtime events, and final product selection.

The sidecar owns `.rosproj` files and creates a sibling project directory as the only default writable sandbox. It writes sanitized state to `PUBLIC/research_state.json`, intake packets to `CONTROL/intake_queue/`, and raw runtime intake under project-local `PRIVATE/intake/`.

Codex integration is optional. When available, Codex runs with project-root `cwd`, workspace-write sandboxing, and a Research OS approval handler.
