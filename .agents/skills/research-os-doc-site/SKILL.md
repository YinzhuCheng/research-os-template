---
name: research-os-doc-site
description: Maintain Research OS Desktop repository documentation, document maps, dashboard data, link checks, and asset provenance after the static HTML documentation surface was retired.
---

# Research OS Documentation

Use this skill when changing `docs/`, `README.md`, `PUBLIC/dashboard_data.json`, or user-facing Research OS Desktop documentation.

## Workflow

1. Read `docs/doc_map.yaml`, `docs/PROJECT_SUMMARY.md`, `CONTROL/work_order.yaml`, and `CONTROL/phase_gate.yaml`.
2. Keep documentation English-first. The desktop app UI may remain Chinese.
3. Keep `docs/desktop-app.md` as the user entry and `docs/architecture.md` as the maintainer/agent entry.
4. Update `docs/doc_map.yaml` and `PUBLIC/dashboard_data.json` whenever a durable entrypoint changes.
5. Update `docs/ASSET_SOURCES.md` if any external asset, screenshot, generated bitmap, icon pack, or third-party template is introduced.
6. Run:
   - `scripts/check_docs_links.ps1`
   - `scripts/check_dashboard.ps1`
   - `scripts/check_desktop_app.ps1`

## Boundaries

- Do not place private research material in `docs/` or `PUBLIC/`.
- Do not add tracking scripts or analytics.
- Do not reintroduce static HTML documentation or the old browser dashboard.
