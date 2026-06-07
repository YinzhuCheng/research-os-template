# Scripts

Primary desktop checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_desktop_app.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_docs_links.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1
```

Sidecar privacy and archive checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_private_intake_synthetic.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_archives.ps1
```

The retired browser bridge and static HTML dashboard scripts have been removed. Desktop app state now uses `PUBLIC/research_state.json` and `CONTROL/intake_queue/`.
