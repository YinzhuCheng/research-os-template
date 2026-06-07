# Gap Audit

## Addressed

- Browser bridge retired.
- Static HTML docs and dashboard removed.
- Product naming moved away from old seed branding.
- Documentation is English-first.
- Desktop state paths are canonical.
- Sidecar CORS and event redaction are hardened.
- Seed copying excludes private and retired browser artifacts.
- UI click paths are covered by Playwright.

## Remaining Risks

- The sidecar still uses a fixed default port, `127.0.0.1:8789`.
- The packaged app still depends on a system Python runtime in v1.
- Full Codex runtime behavior depends on the user's installed official Codex environment.
- Playwright tests mock sidecar responses; they do not validate a real long-running Codex turn.
- The remote GitHub repository name may still need owner-level renaming outside the codebase.

## Next Improvements

- Add negotiated sidecar ports.
- Bundle a Python sidecar runtime for Windows.
- Add real but harmless Codex app-server integration tests.
- Add an app-level documentation viewer if users need offline docs inside the desktop shell.
