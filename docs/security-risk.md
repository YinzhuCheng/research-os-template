# Security and Risk Register

| Risk | Status | Control |
|---|---|---|
| API key or token persistence | mitigated | Profile metadata stores only secret references; runtime events are recursively redacted. |
| Sidecar exposed to arbitrary web pages | mitigated | CORS is limited to Tauri and local development origins. |
| Project root escape | mitigated | Sidecar path resolution rejects paths outside the project sandbox. |
| Raw intake leaks to public state | mitigated | Raw material is stored under `PRIVATE/intake/`; `PUBLIC/research_state.json` stores metadata only. |
| Old browser bridge drift | mitigated | Browser bridge files and checks are removed; desktop state paths are canonical. |
| Fixed localhost port conflict | open | v1 uses `127.0.0.1:8789`; future work should add negotiated ports. |
| Packaged app depends on system Python | open | v1 detects system Python; future packaging should bundle a sidecar runtime. |
| Codex SDK unavailable | accepted | Runtime adapter fails safely with `codex_unavailable`. |
