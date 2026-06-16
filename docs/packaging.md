# Packaging Guide

The Windows desktop package is built from `apps/research-os-desktop`.

```powershell
cd apps/research-os-desktop
npm install
npm run tauri -- build
```

Expected local artifacts:

- `apps/research-os-desktop/src-tauri/target/release/research-os-desktop.exe`
- `apps/research-os-desktop/src-tauri/target/release/bundle/msi/*.msi`
- `apps/research-os-desktop/src-tauri/target/release/bundle/nsis/*setup.exe`

Do not commit `node_modules/`, `dist/`, `src-tauri/target/`, or `src-tauri/gen/`.
