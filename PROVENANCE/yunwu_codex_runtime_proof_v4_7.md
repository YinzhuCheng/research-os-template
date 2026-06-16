# Research OS v4.7 Yunwu-Codex Runtime Proof

Generated at: 2026-06-08T11:59:00+08:00  
Work order: WO-0018

## Result

Research OS Desktop successfully drove a real Codex app-server/SDK thread and turn through the Yunwu provider profile.

Observed runtime route:

`Research OS Desktop UI/API -> Python sidecar -> Codex SDK/app-server -> isolated CODEX_HOME -> Yunwu provider -> gpt-5.5 xhigh -> sidecar runtime events -> app artifact route`

The proof thread response reported:

- `modelProvider`: `yunwu`
- `model`: `gpt-5.5`
- `reasoningEffort`: `xhigh`
- thread id: `019ea55d-1417-7863-afea-48d05483a641`
- turn id: `019ea55d-5de9-7502-88e1-59b5de0d28a9`
- turn status: `completed`

The proof turn returned a compact JSON object stating that it was a Research OS Desktop app-driven Codex proof turn, with `provider_expected=yunwu`, `model_expected=gpt-5.5`, `reasoning_expected=xhigh`, `modified_files=[]`, and `next_action=stop_after_proof`.

The Codex output was then written through the Research OS app artifact route to the private proof project under `PROVENANCE/research_loop/yunwu_codex_runtime_proof.json`.

## Cost

Yunwu usage was measured through the documented free usage query endpoint.

- usage before: `280732.125`
- usage after: `280737.8366`
- quota delta: `5.7116`
- estimated USD delta: `0.0000114232`

No API key, Authorization header, cookie, token, or raw credential was written to this report, the repository, `.rosproj`, screenshots, or committed logs.

## Screenshots

Local screenshots were captured under ignored test artifacts:

- `apps/research-os-desktop/test-results/researcher-qa/real-yunwu-codex-proof/runtime-proof-desktop.png`
- `apps/research-os-desktop/test-results/researcher-qa/real-yunwu-codex-proof/runtime-proof-narrow.png`

The screenshots are intentionally not committed.

## App Gaps Fixed During Proof

- Existing profile stores did not automatically receive the new built-in Yunwu profile.
- `thread_start.sandbox` needed `workspace-write` instead of `workspaceWrite`.
- `approvalPolicy` needed `on-request` instead of `unlessTrusted`.
- `turn_start.sandboxPolicy.type` needed `workspaceWrite` even though `thread_start.sandbox` needs `workspace-write`.
- Runtime event redaction was over-broad and hid numeric `tokenUsage`; redaction now preserves numeric usage telemetry while still redacting Authorization, cookies, API keys, passwords, secrets, and real token strings.

## Residual Notes

- `thread_start` currently reports a read-only sandbox in the returned thread metadata even when later turns use explicit workspace-write sandbox policy. This did not block the no-file proof turn, but should be watched during write-producing turns.
- The proof used a private throwaway `.rosproj` project and did not import the neural-network source material.
