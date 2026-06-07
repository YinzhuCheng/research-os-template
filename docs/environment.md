# Environment

Research OS Desktop needs Git, Python 3.10+, Node/npm for frontend development, and Rust/Cargo for Tauri packaging.

Minimum runtime:

- Git for project archives and initial commits.
- Python 3.10+ for the sidecar.
- A Windows WebView2-capable environment for the Tauri app.

Development and packaging:

- Node.js with npm for `apps/research-os-desktop`.
- Rust/Cargo for `npm run tauri -- build`.
- Optional Codex SDK/app-server for runtime execution.

Check the environment:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1
```

The old browser bridge is retired. The desktop app starts the Python sidecar automatically.
