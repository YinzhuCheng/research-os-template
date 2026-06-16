# LCR Magic Tower Dogfood Release Plan

Last revised: 2026-06-16 06:03 +08:00

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
- Latest LCR MCP preset fix:
  - `yunwu_image_transparent_asset` now appears in the source `yunwu_image` MCP preset tools policy with `approval_mode=prompt`.
  - The current running app data MCP config was also updated through `/api/router/mcp/config/save`, and `/api/runtime/mcp/reload` returned `reloaded=true`.
  - Sidecar unit tests after this fix: `113` tests passed.
- Latest Yunwu transparent asset retry:
  - Real `/api/runtime/mcp/tool-call` to `yunwu_image.yunwu_image_transparent_asset` generated `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781558270-bd96583d.png`.
  - Result: PNG RGBA 1024x1024, `actual_n=1`, `count_mismatch=false`, transparent pixel ratio about `0.911`, corner alpha all zero.
  - Checker preview: `D:\workflow\magical-girl-tower-dogfood\captures\20260616-yunwu-mcp-retry-key-checker.png`.
  - Human visual judgment: good transparent cutout for HUD/reward art, but too glow-heavy/concept-art-like for a 64x64 map pickup.
- Latest DS bounded asset step:
  - Provider handoff from Yunwu to DeepSeek stayed inside the same task and created provider thread `019ecd2b-e987-70f2-8c2f-419f35cb0c44`.
  - DS promoted `yunwu-1781558270-bd96583d` as HUD/reward key art, not as the map pickup key.
  - New game asset: `D:\workflow\magical-girl-tower-dogfood\workspace\assets\images\sprites\hud_key_yellow.png`.
  - Updated game manifest: `sprites.hud.key_yellow` and `promoted_assets.yunwu-1781558270-bd96583d`.
  - Updated registry: `integration_status=promoted_as_hud_reward`, `manifest_keys=["hud.key_yellow"]`, `in_use=true`.
  - Validation: WSL `node --check js/*.js` passed; `sprite_manifest.json` parsed successfully; browser smoke at `http://127.0.0.1:8123/` passed with HTTP 200 and zero supplied console errors.
  - Browser screenshot: `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\after-ds-hud-key-promotion-2026-06-16T052723-597271+0800.png`.
- Latest context/health-check hardening:
  - Source now accepts `context_mode=project`, `project_context`, and `with_context` as default project-context aliases.
  - Source now maps `context_mode=health`, `health_check`, `light`, and `lightweight` to `minimal_text`, so post-compact health checks do not inject the full Project/Asset Context Pack.
  - `_task_thread_settings` now preserves an existing task/provider-thread `collaboration_mode` when a short health check omits that field, instead of silently resetting it to `default`.
  - Real DeepSeek compact completed on thread `019ecd2b-e987-70f2-8c2f-419f35cb0c44`, and a post-compact turn replied exactly `LCR_COMPACT_OK`.
  - Running sidecar still needs restart/repackage before these source fixes affect the installed/runtime app; do not restart without preserving runtime-loaded provider secrets.
- Latest Kimi visual evidence:
  - Kimi visual micro-check recovered from a stale missing provider thread into `019ecd40-d30c-7b43-955a-c11945ccca4a`.
  - First check used an old title-screen screenshot and correctly returned `retry` because the overworld map was not visible.
  - A real in-app browser screenshot was captured at `D:\workflow\magical-girl-tower-dogfood\captures\20260616-current-real-map-browser.png` for future Kimi/DS review.
- Latest Yunwu image MCP transparent asset retry:
  - Real `/api/runtime/mcp/tool-call` to `yunwu_image.yunwu_image_transparent_asset` succeeded twice through the MCP path.
  - First retry generated `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781560517-2adfd05d.png`: PNG RGBA, `actual_n=1`, transparent ratio about `0.832`, visually too realistic for map/HUD icon use.
  - Second retry used a stricter 2D/JRPG prompt and generated `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781560636-992a50eb.png`: PNG RGBA, `actual_n=1`, transparent ratio about `0.886`, semi-transparent ratio about `0.005`, visually much closer to a usable game key icon.
  - Checker comparison: `D:\workflow\magical-girl-tower-dogfood\captures\yunwu-key-retry-comparison-checkerboard.png`.
  - Evidence judgment: the transparent/edit route is working; remaining quality risk is prompt/style/specification, not the MCP transport or alpha validation.
- Latest Dogfood evidence hardening:
  - Source now promotes capture paths attached directly to a dogfood milestone into the run-level `captures` list, so `run_summary.latest_capture` follows the newest milestone evidence instead of staying pinned to an older browser smoke screenshot.
  - Sidecar unit tests after the latest source fixes: `116` tests passed.
- Known game quality gap: Kimi visual micro-check still marked the map as `retry`; the map remains too grid/block-like.
- Known LCR risks:
  - Installed packages still need a fresh rebuild to carry the latest sidecar startup/tool-timeout/asset-registry/image-return fixes.
  - Provider-thread compact after runtime restart can still fail with `compact_thread_not_found`; in the latest run this left `current_thread_id=null` and required an explicit new provider thread.
  - `turn/start` may return a recovered/new provider thread id even when a caller supplied an older thread id; callers and UI must follow the returned `thread_id`.
  - `context_mode=project` currently returns `Unsupported context mode: project`; UI/API should expose valid context mode choices instead of letting users or automation guess.
  - Some DS file mutations were reflected in project files and context pack plan state, but the thread item view only exposed a final `agentMessage` rather than fine-grained command/tool/file-change events. Release UI should distinguish model claims from tool-event verified changes more explicitly.
  - DeepSeek output showed occasional mojibake (`กช`, `กม`) for symbols and PowerShell/GBK printing failed on emoji output; LCR should normalize/escape runtime output as UTF-8.
  - Asset registry usage must be proven by screenshots rather than claimed by model text.
  - DS did not use verified web research tools during the latest design/route turn despite being asked to research; release metadata should mark that as a tool-use health gap until a true `lcr_web_*` tool event is observed.

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

Latest evidence from the 2026-06-16 Yunwu MCP retry:

- `yunwu_image_transparent_asset` is callable through LCR MCP when the request includes the local admin session token.
- `n=2` remained unstable: the request returned `actual_n=1`, so production draws should still prefer concurrent repeated `n=1` calls.
- The transparent edit route now reliably produced PNG RGBA assets with alpha, but visual usability still needs a separate gate.
- `yunwu-1781561870-18ebb71e.png` is a better heroine walk-pose candidate than the earlier portrait-like image, but it still has an oval ground shadow/halo.
- `yunwu-1781561922-7e785d75.png` is semantically a good yellow-key sprite, but still has gold glow and should be cropped/cleaned or redrawn before promotion.
- Next DS/Kimi asset steps must treat `has_alpha=true` as necessary but not sufficient; contact-sheet and in-game scale review remain required before promote.

Latest LCR tool-chain fix from the same checkpoint:

- Source now injects `lcr_web_search_batch`, `lcr_web_research_brief`, `lcr_web_search`, and `lcr_web_fetch` as app-server `dynamicTools` whenever the LCR built-in web server is enabled.
- Dynamic tool events now record `server=lcr_web` or `server=yunwu_image`, so dogfood evidence can distinguish web research from image generation and avoid charging web calls as image usage.
- Sidecar unit tests passed: 118 tests, including new coverage for lcr_web dynamic tool registration and a fake research brief dynamic call.
- The running sidecar must still be restarted/repackaged before this source change affects active app-server turns.

Latest evidence from the 2026-06-16 post-restart Yunwu image MCP retry:

- The source sidecar was restarted on port 8795 and the magic tower project was reopened; health shows WSL `Ubuntu-24.04`, project runtime configured, and provider secret loaded.
- MCP status exposes `lcr_web` plus `yunwu_image` with `yunwu_image_transparent_asset`, `yunwu_image_edit`, and `yunwu_image_generate`.
- Two `yunwu_image_transparent_asset` calls with stricter Japanese-anime sprite prompts produced PNG RGBA assets:
  - `yunwu-1781563030-1cb35bb5.png` heroine candidate, `has_alpha=true`, transparent ratio about `0.663`.
  - `yunwu-1781563084-6efc6537.png` yellow-door candidate, `has_alpha=true`, transparent ratio about `0.613`.
- A stricter direct `yunwu_image_generate` call with `background=transparent`, `format=png`, and no-glow/no-backdrop prompt produced `yunwu-1781563564-d1ef0f96.png`, `has_alpha=true`, transparent ratio about `0.877`; this is cleaner than the edit-route samples but still has a gold aura.
- A parallel `yunwu_image_transparent_asset` strict key call timed out after 240 seconds; treat edit-route transparency as useful but currently less stable than direct generation for small props.
- Contact-sheet evidence was saved at `D:\workflow\magical-girl-tower-dogfood\captures\yunwu_mcp_retry_contact_sheet_20260616.png`.
- Asset registry now records the latest assets with inferred types `heroine`, `door`, and `key`, all `not_promoted/unreviewed`; alpha correctness is better, but visual usability still needs Kimi/DS review before promotion.

Latest LCR evidence-display fix from the same morning:

- A DeepSeek `no_context` tool-compliance turn successfully called the LCR built-in web dynamic tool `lcr_web_search_batch`.
- Verified event: `dynamic_tool_called server=lcr_web tool=lcr_web_search_batch`, record `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\research\search-batch-20260616T065707169673-4e2f12.json`.
- The first DS web prompt claimed `lcr_web_research_brief`, but the important evidence distinction is now clear: only runtime `dynamicToolCall` / `dynamic_tool_called` records count as verified tool use.
- LCR now overlays `dynamicToolCall` events back into `thread/read` when app-server omits them; live verification on thread `019ecd80-9dce-7233-8509-5b3c64fac8e9` returned item order `userMessage,dynamicToolCall,agentMessage`.
- Sidecar unit tests passed: 119 tests.
- Remaining LCR issues exposed:
  - `profile_id=deepseek` returns `Unknown profile` even though provider `deepseek` exists; UI/API should suggest profile ids or resolve provider ids safely.
  - `context_mode=health_check` was still blocked by the 90% context guard; short health checks should either bypass with a safe minimal thread or expose a clear continue-once decision path.
  - Basic web search returned low-quality/off-topic results for autotile queries; use the research layer or better source-targeted queries for real design work.

Latest LCR runtime profile / health-check fix from the same morning:

- Runtime profile resolution now accepts provider ids such as `deepseek` for runtime calls and resolves them to a safe default profile when available, while profile CRUD and secret-loading endpoints remain strict about concrete `profile_id`.
- `context_mode=health_check` / `lightweight` maps to `minimal_text` and now starts a fresh minimal provider thread, so short provider/tool smoke checks are not blocked by a hot user task thread at 90%+ context.
- Sidecar unit tests passed: 121 tests, including new coverage for provider-id runtime profile resolution and fresh-thread health-check behavior.
- Live verification after restarting the source sidecar on port 8795:
  - posting `/api/runtime/turns/start` with `profile_id=deepseek` and `context_mode=health_check` succeeded,
  - the handoff resolved to `profile_id=deepseek-default`,
  - the runtime event recorded `reason=minimal_text_fresh_thread`,
  - DeepSeek returned `ok` in about 2 seconds.
- The live restart exposed two Windows-side operational footguns to harden later:
  - selecting the first `Get-NetTCPConnection` row can hit `TimeWait` instead of the real listener,
  - `Start-Process -ArgumentList` needs explicit quoting for paths with spaces such as `D:\Google One\research-os-template`.
- The project was switched back to the previous DS dogfood thread after smoke so the app does not visually stay on the disposable health-check thread.

Latest evidence from the 2026-06-16 Yunwu MCP retry after the network interruption:

- Direct Yunwu Images API connectivity is healthy: `gpt-image-2` returned a smoke image URL in about 56 seconds.
- The actual LCR MCP path is also healthy: `mcpServer/tool/call` for `yunwu_image_transparent_asset` completed twice through `/api/runtime/mcp/tool-call`.
- Generated assets:
  - `yunwu-1781566023-f48a6585.png`, key candidate, PNG/RGBA, `has_alpha=true`, transparent ratio about `0.826`.
  - `yunwu-1781566680-32b6cc3a.png`, yellow-door candidate, PNG/RGBA, `has_alpha=true`, transparent ratio about `0.598`.
- Contact-sheet evidence was saved at `D:\workflow\magical-girl-tower-dogfood\captures\yunwu_mcp_retry_after_fix_contact_sheet_20260616.png`.
- Visual gate: the door is game-usable as a single transparent sprite candidate; the key is semantically usable but still has gold particles/glow, so future prompts should continue saying `no aura`, `no particles`, `no glow ring`, and `tight silhouette`.
- LCR bug exposed and fixed: direct MCP tool calls used to create/reuse an internal tool thread and then steal the project/task active thread. `RuntimeService.call_mcp_tool` now restores the prior project current thread and task active provider thread by default, while still returning the internal tool thread id for audit. `/api/runtime/threads/switch` now also synchronizes task active thread state.
- LCR dogfood milestone API bug exposed and fixed: old `dogfood_run.json` records can contain string capture refs, and `add_milestone` previously assumed all existing captures were objects. It now ignores legacy non-object captures during merge instead of returning 400.
- Sidecar unit tests passed: 121 tests. Live verification after source sidecar restart confirmed project `current_thread_id` and task `active_provider_thread_id` remained on `019ecd80-9dce-7233-8509-5b3c64fac8e9` after the second Yunwu MCP image call.
- Dogfood milestone was recorded as `Yunwu MCP transparent assets verified after active-thread fix`.
- Operational footgun confirmed: `Stop-Process` did not terminate one old 8795 listener, while `taskkill /F /PID` did. Windows restart scripts should identify the `Listen` owner process robustly and verify the restarted process really serves the patched source.

Latest evidence from the 2026-06-16 noon transparent-asset and verification pass:

- Yunwu image MCP is materially healthier for transparent game assets: three `yunwu_image_transparent_asset` calls produced PNG/RGBA assets with alpha metadata recorded:
  - `yunwu-1781582083-5faeecc3`, heroine walk-down candidate, transparent ratio about `0.658`.
  - `yunwu-1781582151-00d0b82a`, forest cluster overlay, transparent ratio about `0.684`.
  - `yunwu-1781582208-605a21d0`, crystal stair/portal candidate, transparent ratio about `0.571`.
- Contact-sheet evidence was saved at `D:\workflow\magical-girl-tower-dogfood\captures\yunwu_mcp_retry_three_assets_checker_20260616.png`.
- Kimi visual micro-check succeeded on a real generated asset sheet. Kimi judged:
  - heroine: pass as `walk_down_f1`;
  - forest: pass as overlay decoration, not base/autotile;
  - crystal stair: pass as a special portal, not ordinary stairs.
- DeepSeek implemented the next bounded game step:
  - copied `heroine_walk_down_f1.png` and `forest_cluster_overlay.png` into `assets/images/sprites/`;
  - updated `js/sprites.js` and `js/ui.js`;
  - reported 9 `node --check` validations passed.
- Browser smoke after DS's step produced a verified map screenshot at `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\post-ds-walk-forest-map-verified-2026-06-16T122218-836618+0800.png`.
- Visual assessment: the map is less purely square/blocky, but the forest overlay currently reads as a large sticker; next DS/Kimi loop should refine overlay scale/placement and complete heroine multi-frame animation before expanding assets.
- LCR direct MCP tool-call bug fixed: direct image/web/browser MCP calls now use internal app-server tool threads without adding provider threads or handoff events to the user-visible task.
- LCR browser smoke bug fixed:
  - WSL-style `file:///mnt/d/...` URLs normalize to Windows host paths before preflight.
  - successful Playwright screenshots can override stale file preflight failures.
  - `domcontentloaded` replaces `networkidle` to avoid hanging on local games.
  - action lists now allow up to 80 actions and record `action_warning` if truncated.
- LCR workspace isolation bug found and patched:
  - magic tower workspace root contains an empty `.codex` directory, first observed in runtime logs before this checkpoint and timestamped around the app-server/dogfood turns.
  - The likely cause is launching Codex app-server from the workspace root (`cd workspace && codex app-server`), even though `CODEX_HOME` is isolated.
  - Runtime launch now starts app-server from `workspace/.lcr/runtime-cwd` while keeping thread `cwd` and writable roots pointed at the real workspace, so process-local Codex startup files should no longer be created at workspace root.
  - Existing empty `.codex` was not deleted automatically; preserve it as audit evidence until the user explicitly approves cleanup.
- Live regression smoke preserved 30 actions with no truncation warning, no console errors, and a screenshot at `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\long-action-limit-regression-smoke-2026-06-16T123217-671054+0800.png`.
- Sidecar unit tests passed: 129 tests.
- Remaining LCR/product risks:
  - historical task state still contains earlier direct-MCP provider-thread pollution; the fix prevents future pollution but does not automatically rewrite old audit history.
  - `Start-Process -ArgumentList` must quote seed-root paths with spaces; otherwise source sidecar startup silently exits.
  - browser smoke can now support longer flows, but DS/Kimi must still use meaningful actions that reach the actual gameplay state, not just title/dialog screens.

1. Rebuild/restart the installed LCR package so the running app carries the MCP preset, asset promotion crop/resize, image-return, context-guard, and timeout fixes.
2. Ask DS for one bounded seamless/free-map step that directly addresses Kimi's screenshot critique: visible grid seams, repetitive dark blotches, and the solid green band below the map.
3. DS must preserve the current working game rules and run `node --check js/*.js`; if it edits CSS only, it must still run browser smoke and save a screenshot.
4. Ask Kimi to judge the new screenshot against the previous `20260616-ds-grass-asset-map.png` and decide whether the map still reads as blocky. Kimi may propose an executable visual plan, not only pass/fail.
5. If the visual step improves the screenshot, run Yunwu GPT-5.4 high playtest and send the critique back to DS for route/UI/value priorities.
6. If visual quality is still poor, let DS plan a redraw of a dedicated seamless grass/background asset through Yunwu image tools rather than overfitting CSS around a bad texture.
7. Fix the LCR event/evidence display gap so command/tool/file-change evidence is visible as `tool-event verified`, not only inferred from model text.
8. Keep treating ignored `asset_id`/manifest paths, stale provider threads, unsupported context-mode values, or unverified model claims as LCR context/evidence bugs and fix the app before continuing.

## Commit/Push Gate

Commit and push only after:

- relevant tests pass,
- provenance/resource ledger is updated,
- isolation checks pass,
- no secrets are detected in touched files,
- the commit groups a coherent LCR or game milestone.
