# Research OS Desktop App

Research OS Desktop is the primary product path for v4.0. It wraps the Research
OS workflow in a Windows desktop app built with Tauri, React, and a Python
sidecar. Codex remains the execution kernel through the official Codex
app-server/SDK; the app owns project state, permissions, archives, provenance,
and user-facing workflow.

## Architecture

```text
Tauri + React UI
  -> Python sidecar on 127.0.0.1:8789
  -> Research OS project sandbox
  -> optional official Codex app-server/SDK
```

The React UI never talks directly to Codex app-server. It talks to the sidecar,
which validates paths, profile metadata, approval requests, archives, and
Research OS state before any agent work can proceed.

## Project Model

- A `.rosproj` file is the project entrypoint.
- The sibling directory without the extension is the project sandbox.
- The project sandbox contains `CONTROL/`, `PUBLIC/`, `PRIVATE/`,
  `PROVENANCE/`, `config/`, `INBOX/downloads/`, and `outputs/`.
- `.rosproj` stores non-sensitive metadata only: project path, active phase,
  default profile id, and Codex thread ids.
- API keys, cookies, tokens, passwords, authorization headers, SSH keys, and
  provider secrets must not be written to `.rosproj` or project git.

## Development

Run the sidecar:

```powershell
python .\apps\research-os-sidecar\sidecar_server.py --serve --template-root .
```

Run the React UI:

```powershell
cd .\apps\research-os-desktop
npm install
npm run dev
```

Run the Tauri shell after installing Rust and Tauri prerequisites:

```powershell
cd .\apps\research-os-desktop
npm run tauri dev
```

## Safety Defaults

- Project-root writes are allowed only inside the project sandbox.
- External files must be explicitly imported into `INBOX/` or `PRIVATE/intake/`.
- Downloads must land inside `INBOX/downloads/` or another project path.
- Git `status`, `diff`, `log`, `branch`, `add`, and `commit` are low risk
  inside the sandbox.
- Git push, release, external writeback, credential access, public export,
  submission, and real resource use require explicit confirmation.
- If Codex SDK is missing, runtime endpoints return `codex_unavailable` instead
  of simulating execution.
