# LCR Magic Tower Dogfood Release Plan

Last revised: 2026-06-16 04:20 +08:00

## Objective

Use Local Codex Router (LCR) itself to drive a three-model dogfood loop until both outcomes are true:

1. The magical-girl tower game reaches a publishable local-release standard.
2. The LCR app reaches a publishable standard for this workflow: robust provider handoff, stable WSL runtime, reliable built-in tools, save/load checkpoints, visual/model health checks, evidence capture, and no conflict with official Codex.

The operator should maintain LCR and supervise evidence. Game design, asset planning, implementation, visual review, and playtest critique should be delegated through LCR whenever the app can support it.

## Product Semantics

- Project: a workspace and durable app state container.
- Task/Chat: the user-visible workstream for one objective.
- Provider Thread: an internal Codex app-server thread for a provider/model inside the same task.
- Provider Switch: default behavior is multi-provider handoff, not a new user-visible chat.
- Fork: official Codex fork semantics for branch exploration.
- Save/Load: heavier project checkpoint; not a replacement for fork.
- Built-in Tools: LCR-owned tools exposed through Codex app-server dynamicTools. External MCP servers remain a separate category.

## Current Evidence Snapshot

- Magic tower project: `D:\workflow\magical-girl-tower-dogfood\magical-girl-tower.lcrproj`.
- Workspace: `D:\workflow\magical-girl-tower-dogfood\workspace`.
- Latest successful LCR dynamic tool smoke: DeepSeek triggered `yunwu_image_transparent_asset` through Codex `dynamicTools` and generated `yunwu-1781544007-9f1a5f3d`.
- Latest successful direct MCP tool smoke: source sidecar recovered a stale DeepSeek source thread into a fresh Yunwu provider thread, then generated `yunwu-1781547151-bb6a4fa9`.
- Latest direct MCP transparent assets:
  - `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781549746-21117331.png` (`terrain`, `RGBA`, `actual_n=1`, `transparent_pixel_ratio=0.5158`, no validation warnings).
  - `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781550294-ee592d0b.png` (`door`, `RGBA`, `actual_n=1`, `transparent_pixel_ratio=0.6533`, no validation warnings).
  - `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781554341-b98d2203.png` (`stair/portal candidate`, generated through real `/api/runtime/mcp/tool-call`, `RGBA`, `actual_n=1`, `transparent_pixel_ratio=0.7380`, no validation warnings).
- Latest visual evidence: `D:\workflow\magical-girl-tower-dogfood\captures\20260616-yunwu-mcp-retry-contact-sheet.png`.
- Latest Yunwu MCP checker preview: `D:\workflow\magical-girl-tower-dogfood\captures\20260616-yunwu-mcp-retry-transparent-stair-checker.png`.
- Latest game smoke after the retry:
  - Title screenshot: `D:\workflow\magical-girl-tower-dogfood\captures\20260616-yunwu-door-after-registry-fix.png`.
  - Map screenshot: `D:\workflow\magical-girl-tower-dogfood\captures\20260616-yunwu-door-map-after-registry-fix.png`.
  - Browser console errors: `0`.
- Latest DS visual implementation:
  - DS used `yunwu-1781549746-21117331` and copied it into `assets/images/sprites/tile_floor_grass_lcr.png`.
  - DS updated `js/sprites.js` and `css/style.css`.
  - Screenshot: `D:\workflow\magical-girl-tower-dogfood\captures\20260616-ds-grass-asset-map.png`.
  - `node --check js/*.js` passed and browser console errors were `0`.
- Latest Kimi visual micro-check:
  - Kimi successfully consumed the real game screenshot through `localImage`.
  - Verdict: `pass` for the visual chain, but content quality still needs retry-level improvement.
  - Kimi's next visual step: create a seamless grass tile variant or add a semi-transparent edge-blend overlay to hide grid seams and repetitive dark blotches.
- Latest direct MCP alpha checks passed for both assets; both are registered in `asset_registry.json` and generated asset manifest.
- Sidecar unit tests at the last plan revision: 112 passed.
- Latest LCR stability hardening: desktop startup now attempts to stop stale LCR-owned sidecars on port 8790 before spawning, sidecar stdio pipes no longer risk unread-pipe stalls, and project JSON writes retry transient Windows `os.replace` permission failures.
- Latest LCR tool hardening: direct `mcpServer/tool/call` now honors the MCP server `tool_timeout_sec`; this fixed false timeouts for slower Yunwu image calls.
- Latest LCR asset-memory hardening: `asset_registry` rebuild now links agent-copied generated assets to game manifest refs by content hash. This fixed the `yunwu-1781550294-ee592d0b` yellow door after DS copied it to `assets/images/sprites/tile_door_new.png`; the registry now records `promoted_path=assets/images/sprites/tile_door_new.png` and `manifest_keys=tiles.door`.
- Latest LCR context-guard hardening: before blocking a hot thread at 90% context, `start_turn` now probes whether the provider thread still exists. If the thread is stale after restart, LCR marks it missing and lets provider handoff/recovery continue instead of forcing a failed compact first.
- Latest LCR image-return hardening: persisted Yunwu image responses now strip raw `b64_json` from returned data and keep only `b64_json_present`, local paths, and validation metadata, preventing UI/log b64 floods.
- Latest Yunwu image MCP dogfood:
  - DS used the real in-app Yunwu image tool from an app-server turn, not a manual side call.
  - First portal redraw attempt fell back from `gpt-image-2-all` HTTP 503 to `gpt-image-2` and generated `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781556230-3935bd95.png`.
  - Kimi visual micro-check rejected that candidate as `retry` because a baked gray oval ground shadow/platform would clash with grass, stone, and forest terrain.
  - DS used Kimi's stricter prompt for a second real Yunwu image tool call and generated `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781556517-68192932.png`.
  - Independent alpha check for the accepted candidate: PNG RGBA 1024x1024, transparent ratio about `0.579`, semi-transparent ratio about `0.034`.
  - Kimi final visual micro-check returned `pass`, usable role `portal`, and recommended crop-to-content, bottom-center pivot, and registering as a 96x96 portal.
  - Checker preview: `D:\workflow\magical-girl-tower-dogfood\captures\20260616-ds-yunwu-redraw-portal-no-shadow-checker.png`.
- Known game quality gap: Kimi visual micro-check still marked the map as `retry`; the map remains too grid/block-like.
- Known LCR risks:
  - Installed packages still need a fresh rebuild to carry the latest sidecar startup/tool-timeout/asset-registry/image-return fixes.
  - Provider-thread compact after runtime restart can still fail with `compact_thread_not_found`; in the latest run this left `current_thread_id=null` and required an explicit new provider thread.
  - `turn/start` may return a recovered/new provider thread id even when a caller supplied an older thread id; callers and UI must follow the returned `thread_id`.
  - DeepSeek output showed occasional mojibake (`กช`, `กม`) for symbols and PowerShell/GBK printing failed on emoji output; LCR should normalize/escape runtime output as UTF-8.
  - Asset registry usage must be proven by screenshots rather than claimed by model text.

## Standing Rules

- Before each major step, reread this plan and revise it if current evidence changes.
- Do not edit official Codex config unless the user explicitly asks. Specifically avoid mutating `C:\Users\cyz19\.codex\config.toml`.
- Do not create project-level `.codex*` state in the magic tower workspace.
- Do not store API keys, Authorization headers, cookies, admin tokens, or raw key files in repo, `.lcrproj`, `.lcr`, reports, screenshots, or generated manifests.
- Preserve artifacts by default. Do not clean logs, screenshots, generated assets, failed attempts, or validation records unless the user explicitly asks.
- Use WSL as the default execution host once available.
- Prefer DS for planning, research, coding, algorithms, and code review.
- Use Kimi for visual micro-checks and visual planning when image input matters.
- Use Yunwu GPT-5.4 high reasoning for milestone playtest critique.
- Use Yunwu image tools aggressively enough to improve quality, but batch by evidence: generate, inspect, promote, smoke, then scale.

## Budget Policy

- DeepSeek: 50 CNY cap.
- Kimi: 50 CNY cap.
- Yunwu GPT: 50 USD cap.
- Yunwu images: 200 images cap.
- Warn around 80%; hard stop at 100%.
- Product UI does not need detailed token accounting, but provenance should record approximate provider calls and image counts.

## LCR Release Criteria

LCR can be considered release-ready for this workflow only when these are proven:

- Provider switch keeps the same user-visible task and preserves goal, plan, asset context, checkpoint references, and recent milestones.
- DS can call LCR built-in web research and Yunwu image tools from inside a real app-server turn.
- Kimi can reliably receive real image attachments/screenshots for visual checks, or the metadata marks the limitation honestly.
- Yunwu image generate/edit/transparent tools record requested parameters, actual count, alpha/format/size validation, local path, and manifest path.
- Tool events record sanitized summaries, not large b64 payloads.
- Long turn watchdog distinguishes thinking/tool activity from silent stalls and allows interrupt/fork/compact.
- Save checkpoint is lightweight by default and excludes runtime logs, `.lcr/saves`, `node_modules`, caches, and unreferenced large assets.
- Browser smoke can capture screenshots and console summaries to `.lcr/captures`.
- Official Codex config and project `.codex*` isolation checks pass.
- Sidecar unit tests and desktop build pass before packaging.

## Game Release Criteria

The game can be considered publishable for this dogfood target only when these are proven:

- Three floors are playable from start to victory.
- The game communicates "magic tower" as deterministic resource-planning RPG, not just a dark tower interior.
- The visual style is Japanese-anime / JRPG / magical-girl inspired and avoids obvious square-block map feel.
- Floor themes are distinct, for example forest entrance, crystal ruin corridor, and star tower core or magical garden.
- Player movement works at 800x600, 1024x768, and 1920x1080.
- Player cannot walk through collision blockers.
- Keys, doors, monsters, stairs, pickups, battle forecast, victory, failure, and restart all work.
- Heroine has idle and walk_down/up/left/right with at least two visible frames per direction.
- Terrain uses a continuous background and/or autotile-style edge/corner/transition pieces rather than simple repeated square blocks.
- Asset use is real: `sprite_manifest` and browser screenshots must prove promoted assets are actually used.
- DS provides a deterministic route table with HP, keys, ATK/DEF, and required fights per floor.
- Yunwu GPT-5.4 high reasoning playtests at least one milestone and DS addresses the critique.
- Final output includes a local run command and a distributable package or static release folder.

## Execution Loop

1. Reread this plan.
2. Inspect current game/LCR evidence.
3. If LCR has a blocking bug, fix LCR first and run tests.
4. Create or update a lightweight checkpoint.
5. Ask DS for a bounded step:
   - research or plan when design is unclear,
   - one small code change when implementation is clear,
   - evidence-required report after each change.
6. Use Kimi only when visual evidence matters:
   - give 1-3 images,
   - ask for pass/retry/redraw plus concrete visual action,
   - allow Kimi to propose plan/goal changes when image evidence justifies it.
7. Use Yunwu image tool when an asset gap is explicit:
   - reference/edit route for consistent heroine frames,
   - transparent single-asset route for props/monsters/HUD,
   - same-category sheets only for tiles/icons/decor with large gutters.
8. Run browser smoke and syntax checks.
9. Let Yunwu GPT-5.4 high critique playable milestones.
10. Record screenshot, milestone, resource ledger, and provenance.
11. Revise this plan if the evidence changes.

## Immediate Next Actions

1. Let DS do one bounded promote step for accepted portal asset `yunwu-1781556517-68192932`: crop to content, set bottom-center pivot metadata, register as a 96x96 portal/stair transition candidate, and update registry/manifest without breaking current game rules.
2. Run `node --check js/*.js`, browser smoke, and screenshot after the portal promote step.
3. Ask DS for one bounded seamless/edge-blend step that directly addresses Kimi's screenshot critique: visible grid seams, repetitive dark blotches, and the solid green band below the map.
4. DS must preserve the current working game rules and run `node --check js/*.js`; if it edits CSS only, it must still run browser smoke and save a screenshot.
5. Ask Kimi to judge the new screenshot against the previous `20260616-ds-grass-asset-map.png` and decide whether the map still reads as blocky.
6. If the seamless/edge-blend step improves the screenshot, run Yunwu GPT-5.4 high playtest and send the critique back to DS for route/UI/value priorities.
7. If visual quality is still poor, let DS plan a redraw of a dedicated seamless grass/background asset through Yunwu image tools rather than overfitting CSS around a bad texture.
8. Keep treating ignored `asset_id`/manifest paths, stale provider threads, or unverified model claims as LCR context/evidence bugs and fix the app before continuing.

## Commit/Push Gate

Commit and push only after:

- relevant tests pass,
- provenance/resource ledger is updated,
- isolation checks pass,
- no secrets are detected in touched files,
- the commit groups a coherent LCR or game milestone.
