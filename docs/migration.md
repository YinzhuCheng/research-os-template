# Migration Notes

Research OS v4.1 removes the legacy browser bridge as an active product surface. The desktop app is now the only primary UI.

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

Current replacements:

- Desktop UI: `apps/research-os-desktop/`.
- Sidecar API: `apps/research-os-sidecar/research_os_sidecar/server.py`.
- Public state: `PUBLIC/research_state.json`.
- Intake queue: `CONTROL/intake_queue/`.
- Choice responses: `CONTROL/choice_responses/`.

Historical plans and provenance may still mention the retired bridge for audit continuity.
