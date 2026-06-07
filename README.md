# Research OS Desktop

Research OS is now a desktop-first researcher copilot framework built with `Tauri + React + Python sidecar`. The app creates or opens `.rosproj` project files, treats the sibling directory as the project sandbox, and uses the sidecar to govern state, permissions, archives, and optional Codex runtime execution.

## Main Entry

- Desktop app source: [apps/research-os-desktop](apps/research-os-desktop)
- Python sidecar: [apps/research-os-sidecar](apps/research-os-sidecar)
- Desktop guide: [docs/desktop-app.md](docs/desktop-app.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- Security and risk register: [docs/security-risk.md](docs/security-risk.md)
- Environment: [docs/environment.md](docs/environment.md)
- Public dashboard: [PUBLIC/index.html](PUBLIC/index.html)

## Project Model

- `.rosproj` stores non-sensitive metadata only.
- The sibling project directory is the only default writable sandbox.
- Raw intake material belongs under project-local `PRIVATE/`.
- Sanitized UI state is stored in `PUBLIC/research_state.json`.
- User choices are written to `CONTROL/choice_responses/`; intake packets are written to `CONTROL/intake_queue/`.
- API keys, tokens, cookies, passwords, and authorization headers must not be written to project files.

## Development

```powershell
cd apps/research-os-desktop
npm install
npm run test
npm run build
npm run tauri -- build
```

Sidecar tests:

```powershell
python -m unittest discover -s apps/research-os-sidecar/tests -v
```

Repository checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_desktop_app.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_docs_links.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1
```

## Runtime Boundary

React UI calls only the local Python sidecar. The sidecar owns project file I/O, profile metadata, archive creation, permission classification, approval queues, and optional Codex SDK/app-server mediation. Codex runs inside the project sandbox and cannot bypass Research OS approval policy.
