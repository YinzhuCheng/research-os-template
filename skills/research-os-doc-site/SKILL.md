---
name: research-os-doc-site
description: Build and maintain Research OS public documentation pages, including offline HTML guides, technical reports, dashboard navigation, document maps, link checks, and asset provenance.
---

# Research OS Doc Site

Use this skill when changing `docs/`, `PUBLIC/index.html`, or any user-facing Research OS documentation.

## Workflow

1. Read `docs/doc_map.yaml`, `docs/PROJECT_SUMMARY.md`, `CONTROL/work_order.yaml`, and `CONTROL/phase_gate.yaml`.
2. Keep two audience layers distinct:
   - `docs/start-here.html` for general researchers and Codex beginners;
   - `docs/technical-report.html` for maintainers and future agents.
3. Use offline HTML, inline CSS, and repository-relative links. Do not rely on CDN scripts, remote fonts, or external images.
4. Keep diagrams inspectable and accessible:
   - use inline SVG or semantic HTML;
   - include `aria-label` or nearby text explaining the diagram;
   - avoid text overlap at mobile and desktop widths.
5. Update `docs/doc_map.yaml` and `PUBLIC/dashboard_data.json` whenever a new durable entrypoint is added.
6. Update `docs/ASSET_SOURCES.md` if any external asset, screenshot, generated bitmap, icon pack, or template is introduced.
7. Run:
   - `scripts/check_html_docs.ps1`
   - `scripts/check_docs_links.ps1`
   - `scripts/check_dashboard.ps1`

## Boundaries

- Do not place private research material in `docs/` or `PUBLIC/`.
- Do not add tracking scripts or analytics.
- Do not make the HTML depend on a build step unless the work order explicitly authorizes it.
