# Migration Notes

Research OS v4.2 removes the remaining static HTML documentation and dashboard legacy. The desktop app is now the only primary UI.

Removed active surfaces:

- `PUBLIC/copilot.html`
- `.agents/plugins/plugins/research-os-copilot/`
- `scripts/check_copilot_bridge.ps1`
- `scripts/check_copilot_intake_schema.ps1`
- `scripts/check_copilot_resource_rendering.ps1`
- `scripts/check_copilot_state.ps1`
- `PUBLIC/copilot_state.json`
- `docs/codex-browser-copilot.html`
- `CONTROL/copilot_inbox/`
- `PUBLIC/index.html`
- `docs/start-here.html`
- `docs/domain-modes.html`
- `docs/technical-report.html`
- `scripts/check_html_docs.ps1`

Current replacements:

- Desktop UI: `apps/research-os-desktop/`.
- Sidecar API: `apps/research-os-sidecar/research_os_sidecar/server.py`.
- Public state: `PUBLIC/research_state.json`.
- Intake queue: `CONTROL/intake_queue/`.
- Choice responses: `CONTROL/choice_responses/`.
- Documentation entry: `docs/desktop-app.md`, `docs/architecture.md`, and `docs/doc_map.yaml`.

Historical plans and provenance may still mention the retired bridge for audit continuity.
