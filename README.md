# Research OS Desktop

Research OS Desktop is a local researcher-copilot application. It is no longer a starter repository or a browser-copilot shell. The product route is:

`Tauri + React UI -> Python sidecar -> optional official Codex SDK/app-server -> .rosproj project sandbox`

The desktop app creates or opens `.rosproj` files. Each project gets a sibling directory that acts as the default sandbox. The sidecar owns project state, permissions, archive snapshots, profile metadata, and optional Codex runtime mediation.

## Main Entry Points

- Desktop app source: [apps/research-os-desktop](apps/research-os-desktop)
- Python sidecar: [apps/research-os-sidecar](apps/research-os-sidecar)
- Desktop app guide: [docs/desktop-app.md](docs/desktop-app.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- Security and risk: [docs/security-risk.md](docs/security-risk.md)
- Environment: [docs/environment.md](docs/environment.md)
- Testing: [docs/testing.md](docs/testing.md)
- Packaging: [docs/packaging.md](docs/packaging.md)
- Migration notes: [docs/migration.md](docs/migration.md)

## Project Model

- `.rosproj` stores non-sensitive metadata only.
- The sibling project directory is the only default writable sandbox.
- Raw intake material belongs under project-local `PRIVATE/`.
- Sanitized UI state is stored in `PUBLIC/research_state.json`.
- Intake packets are written to `CONTROL/intake_queue/`.
- Choice responses are written to `CONTROL/choice_responses/`.
- API keys, account tokens, cookies, passwords, and authorization headers must not be written to project files.

## Desktop Development

```powershell
cd apps/research-os-desktop
npm install
npm run test
npm run test:ui
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

React calls only the local Python sidecar. The sidecar owns filesystem writes, profile metadata, archive creation, permission classification, approval queues, and optional Codex SDK/app-server mediation. Codex runs inside the project sandbox and cannot bypass Research OS approval policy.
