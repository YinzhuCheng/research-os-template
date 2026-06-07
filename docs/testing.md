# Testing Guide

Run sidecar tests:

```powershell
python -m unittest discover -s apps/research-os-sidecar/tests -v
```

Run frontend tests and package build:

```powershell
cd apps/research-os-desktop
npm run test
npm run test:ui
npm run build
npm run tauri -- build
```

Run repository checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_desktop_app.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_docs_links.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1
```

Yunwu or other paid-model UI review is optional. If used, record only the cost delta and never persist the key or authorization header.
