# Research OS v4.2 Repository Cleanup Plan

## Status

| Step | Area | Status |
| --- | --- | --- |
| 1 | Audit remaining seed-name, HTML, and non-English documentation references | completed |
| 2 | Rename product seed and app-facing names away from old branding | completed |
| 3 | Delete static HTML documentation and dashboard legacy | completed |
| 4 | Rewrite durable documentation in English | completed |
| 5 | Update scripts, doc map, public evidence data, and validation contracts | completed |
| 6 | Run validation, record provenance, commit, and push | completed |

## Scope

This pass makes Research OS Desktop the clear repository identity. The desktop app remains Chinese-first by default, while repository documentation is English-first.

## Boundaries

- Keep `templates/` as an artifact-scaffold directory.
- Keep historical `PROVENANCE/` records immutable except for appending new entries.
- Do not read or commit `PRIVATE/`.
- Do not use paid API calls.

## Validation

- Schema validation passed.
- Desktop app checks passed.
- Dashboard data check passed.
- Documentation links passed.
- Environment docs passed.
- Privacy scan passed.
- Governance, research flow, harness, domain router, no-orphan skills, package artifact checks passed.
- Sidecar unit tests passed.
- Frontend unit tests passed.
- Playwright desktop/narrow click-path tests passed.
- Frontend production build passed.
- Tauri Windows package build passed.
- Durable docs have no Chinese characters; app UI remains Chinese-first.
