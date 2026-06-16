# LCR Magic Tower Dogfood Release Plan

Last revised: 2026-06-16 20:46 +08:00

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
- Latest prompt/background retry evidence from the live source sidecar:
  - transparent door candidate: `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781613388-4c26c59b.png` (`RGBA`, `actual_n=1`, transparency passed, visually stronger than the older door batch but still more concept-prop than strict map tile).
  - transparent stair candidate through real MCP tool-call: `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781613489-e8fd42f7.png` (`RGBA`, `actual_n=1`, transparency passed, materially usable as a forest-ruin stair entrance prop).
  - continuous forest background plate through real MCP tool-call: `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781613600-f8537f8d.png` (`RGB`, `requested_background=auto`, `actual_n=1`, visually much closer to the desired “background plate + transparent props” route).
  - transparent key candidate through the HTTP image route: `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781613742-8f6e65bb.png` (`RGBA`, `actual_n=1`, transparency passed, still glow-heavy for map pickup use but a valid proof that the HTTP write route works when called correctly).
- Latest asset-registry compatibility hardening:
  - `asset_registry.json` rebuild now emits compatibility aliases `manifest_key` and `in_use` alongside canonical `manifest_keys` and `integration_status`.
  - Live magical-tower registry after rebuild: `135` assets total, `44` promoted or in-use, `20` approved-unpromoted, `71` needs review.
  - This closed a real dogfood diagnosis gap where generated/promoted assets were already in use but higher-level context readers misread the registry and treated them as forgotten.
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

Latest evidence from the 2026-06-16 prompt/background protocol repair:

- `yunwu_image_generate` must no longer be treated as “transparent by default”. The latest successful background plate (`yunwu-1781611452-52109ed5.png`) proves the game should use a non-transparent continuous backdrop route for the map base.
- `yunwu_image_transparent_asset` remains the right route for true cutout sprites and props; the transparent forest-canopy retry stayed alpha-clean and materially usable.
- The previous grass-plate retry (`yunwu-1781610678-d2c38ac6.png`) is now a useful negative control: it succeeded transport-wise but visually failed because the old protocol forced scene art through a transparent contract.
- The next DS step should explicitly use the newest background-plate asset plus transparent props as the rendering baseline, not continue stacking transparent overlays on the older blocky map.

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

Latest evidence from the 2026-06-16 13:00 Yunwu MCP retry and DS tool-drift check:

- A DeepSeek bounded visual-refinement turn successfully used the LCR dynamic `lcr_browser_smoke` tool twice, but then drifted into requesting ad-hoc WSL `python3 -m http.server` approvals after file-URL smoke did not satisfy it.
- The manual supervisor declined the first server approval and interrupted the turn after DS requested a second server on another port. This prevented budget waste and records a tool-selection recovery gap rather than a game-design failure.
- LCR observation: `thread/read` shows `dynamicToolCall` items as completed but does not expose the human-readable tool result enough for quick UI/debug review. Tool evidence should be easier to inspect as `tool-event verified`.
- Yunwu image MCP was retried directly through `/api/runtime/mcp/tool-call` with `yunwu_image_transparent_asset`.
- New asset:
  - `yunwu-1781586042-ef792b2d`, purpose `retry_transparent_forest_overlay_small_cluster`, PNG/RGBA, `has_alpha=true`, transparent ratio about `0.837`, actual count `1/1`, transparency status `passed`.
  - Local path: `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\assets\generated\yunwu-1781586042-ef792b2d.png`.
- Visual assessment: the asset is materially better than earlier RGB terrain sheets and works as a small Japanese-anime/JRPG forest-edge overlay candidate, but it still has a soft glow/haze and should be Kimi/DS-reviewed before promotion.
- Dogfood milestone recorded: `Yunwu MCP transparent forest overlay retry after DS tool drift`.
- New LCR bug/risk from the same run: DS's `file:///mnt/d/...` browser-smoke call failed in Playwright with `ERR_FILE_NOT_FOUND`, so future browser-smoke tool result text should explain the host-path normalization requirement and recommend local app URLs or LCR-normalized paths instead of ad-hoc HTTP servers.

Latest fix from the 2026-06-16 13:10 browser-smoke recovery pass:

- Fixed the root cause of the DS server drift: `DogfoodRunService.browser_smoke` now converts WSL-style file URLs such as `file:///mnt/d/...` into host-browser URLs such as `file:///D:/...` before calling Playwright, not only for preflight.
- Browser-smoke records now include `navigation_url` when the browser-visible URL differs from the user/model supplied URL. This gives DS/Kimi a concrete clue that LCR normalized the path and they should not start a temporary HTTP server.
- The `lcr_browser_smoke` dynamic tool description now explicitly says WSL-style file URLs are supported and instructs agents not to start ad-hoc HTTP servers just to capture screenshots.
- Regression coverage:
  - targeted browser-smoke URL tests passed: 2 tests;
  - full sidecar unittest suite passed: 130 tests.
- Live source-sidecar verification on port 8795:
  - project `Magical Girl Tower Dogfood` reopened successfully;
  - `/api/dogfood/browser-smoke` with `url=file:///mnt/d/workflow/magical-girl-tower-dogfood/workspace/index.html` passed;
  - screenshot captured at `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\wsl-file-url-normalization-live-regression-2026-06-16T131106-922485+0800.png`;
  - recorded `navigation_url=file:///D:/workflow/magical-girl-tower-dogfood/workspace/index.html`.
- Remaining operational wrinkle: PowerShell `Start-Process -ArgumentList @(..., "D:\Google One\...")` still splits paths with spaces; the manual restart used a quoted argument string. A dedicated restart helper should be implemented later.

Latest fix from the 2026-06-16 13:25 browser-smoke failure-evidence pass:

- LCR browser smoke now attempts to capture a screenshot even when a Playwright action fails after the page has loaded. This matters for dogfood supervision because DS/Kimi need to see the failed state instead of receiving only a timeout string.
- Failed action captures are recorded with `screenshot_status=captured_after_failure` and a short `screenshot_error`.
- Live source-sidecar verification:
  - intentionally clicking a missing `Enter` text now failed the smoke as expected but still saved `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\browser-smoke-failure-screenshot-regression-2026-06-16T131841-206767+0800.png`;
  - the screenshot showed the game was on a story dialog with a `Next` button, proving the failure screenshot is actionable.
- A corrected keyboard-driven smoke reached the map and passed:
  - screenshot: `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\post-browser-smoke-fix-enter-key-map-reached-2026-06-16T132012-820069+0800.png`;
  - no console errors were recorded.

Latest Yunwu image MCP retry from 2026-06-16 13:30:

- Three direct `/api/runtime/mcp/tool-call` calls to `yunwu_image_transparent_asset` succeeded through the LCR MCP/tool path, not through an out-of-band image generator.
- New transparent candidates:
  - `yunwu-1781587477-af8a12d8`, purpose `dogfood_retry_yunwu_transparent_yellow_key`, PNG/RGBA, transparent ratio about `0.906`, alpha passed; visually too much glow, should be redrawn as a smaller icon before promotion.
  - `yunwu-1781587576-9dcab144`, purpose `dogfood_retry_yunwu_transparent_yellow_door`, PNG/RGBA, transparent ratio about `0.618`, alpha passed; visually usable as a yellow-door candidate.
  - `yunwu-1781587652-490539d0`, purpose `dogfood_retry_yunwu_transparent_forest_sprite_monster`, PNG/RGBA, transparent ratio about `0.760`, alpha passed; visually usable as a forest-monster candidate.
- Checker preview: `D:\workflow\magical-girl-tower-dogfood\captures\yunwu-mcp-retry-transparent-checker-20260616.png`.
- Dogfood milestone recorded: `Yunwu image MCP transparent retry`.
- Next DS/Kimi step: classify and promote only the door/monster after visual micro-check; redraw the key with stricter icon constraints.

Latest LCR context-injection fix from 2026-06-16 14:05:

- Dogfood exposed that auto-injected `asset_registry.json`, `asset_context_pack.json`, and `project_context_pack.json` mentions were being interpreted by Codex app-server as `local-codex-router` MCP resource reads.
- Because LCR does not yet expose a real `local-codex-router` resource server, DS hit `resources/read failed: unknown MCP server 'local-codex-router'` and could not continue from the asset context.
- Fixed by making project and asset context injection text-only for now, with explicit guidance that JSON paths are orientation references and should not be read through MCP resources unless LCR exposes that server.
- Regression coverage:
  - targeted project/asset context injection tests passed: 4 tests;
  - full sidecar unittest suite passed: 130 tests.
- Post-fix dogfood verification:
  - Kimi visual micro-check on the real Yunwu transparent preview, door, and forest monster succeeded, but took about 232 seconds; this is usable but should be recorded as high-latency multimodal behavior.
  - DS completed a bounded follow-up turn, synchronized registry state, added a `forest_spirit` enemy definition, and ran `node --check` on 9 game JS files successfully.
  - Browser smoke reached the map after the story sequence and captured `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\post-promote-map-after-full-story-smoke-2026-06-16T140014-647127+0800.png`, but exposed a resource timeout and the need for smarter story/map smoke actions.
- Remaining LCR risks from the same pass: sidecar restarts still need automatic provider-key re-presentation, provider thread cleanup/normalization is still noisy, and browser smoke needs richer actions such as click-until-gone or wait-for-text-absent.

Latest browser-smoke action fix from 2026-06-16 14:15:

- Added `click_text_until_absent` and `wait_for_text_absent` to LCR browser smoke actions so DS/Kimi can pass story/tutorial/dialog screens without guessing a fixed number of clicks.
- Dynamic `lcr_browser_smoke` tool schema now exposes these actions and recommends `click_text_until_absent` for story/tutorial screens.
- Regression coverage:
  - targeted browser-smoke dynamic-tool/action tests passed: 2 tests;
  - full sidecar unittest suite passed: 130 tests.
- Live magic-tower verification on the source sidecar:
  - restarted source sidecar on port `8795` after confirming the old process did not know the new action;
  - reopened `D:\workflow\magical-girl-tower-dogfood\magical-girl-tower.lcrproj`;
  - `/api/dogfood/browser-smoke` with `click_text_until_absent("Next")` clicked through 8 story steps, found `#grid-container`, found `Floor`, and passed with no console errors;
  - screenshot captured at `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\click-until-absent-story-to-map-regression-2026-06-16T141304-537290+0800.png`.
- New operational finding: source sidecar restarts still do not automatically reopen the last `.lcrproj`; this should become a startup restore improvement later.

Latest browser-smoke timeout-budget fix from 2026-06-16 14:30:

- DS started the next bounded free-map visual step after context guard correctly blocked the stale 90%+ thread and LCR recovered to a fresh DeepSeek provider thread.
- DS updated the game visual layer in `css/style.css` and `js/ui.js`, then attempted `lcr_browser_smoke` with `click_text_until_absent("Next")`.
- The smoke failed because LCR allowed a `timeout_ms=30000` browser action but the outer Python subprocess still killed the Playwright runner after 25 seconds.
- Fixed `DogfoodRunService` to compute the subprocess timeout from the browser action budget, capped at 240 seconds, so legitimate long story/tutorial transitions can record screenshot evidence.
- Regression coverage:
  - targeted browser-smoke action-budget test passed;
  - full sidecar unittest suite passed: 130 tests.
- Live verification:
  - source sidecar restarted on port `8795` with the latest code and the magic tower project reopened;
  - `/api/dogfood/browser-smoke` with `click_text_until_absent("Next", timeout_ms=30000)` passed in about 38 seconds, clicked through 8 story steps, found `#grid-container`, found `Floor`, and captured `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\dynamic-timeout-story-to-map-after-ds-visual-step-2026-06-16T142624-685628+0800.png`.
- Visual assessment of DS's step: the game remains playable and the smoke passed with no console errors, but the map still reads as a grid with a large forest sticker. Next loop should ask Kimi for a visual plan and then DS should either replace the background strategy or redraw a dedicated seamless field/background asset.

Latest Kimi visual critique from 2026-06-16 14:35:

- Kimi visual micro-check completed in about 78 seconds on the latest DS map screenshot.
- Verdict: `retry`.
- Kimi's core critique: the central circular foliage patch looks like a flat decal pasted on top of an obvious square tile grid, not a unified grass field.
- Kimi's executable plan for DS:
  - break the uniform square grass grid with irregular, interlocking ground patches;
  - remove the hard-edged circular foliage decal and scatter individual clumps/bushes/flowers organically;
  - add subtle dirt patches, local shading, and color variation for depth;
  - align wall and character perspective scale;
  - add soft transitions where grass meets stone walls.
- Kimi recommends both new image generation and code/layout changes. Next DS step should generate or select reusable transparent grass/bush/wall assets before another visual code pass.

Latest Yunwu transparent MCP retry from 2026-06-16 14:50:

- DS retried the LCR/Yunwu `yunwu_image_transparent_asset` dynamic tool from inside the magic-tower task, limited to 4 images and no game-code edits.
- All 4 image tool calls completed through the LCR tool path with `requested_n=1`, `actual_n=1`, PNG/RGBA output, `has_alpha=true`, and `transparency_status=passed`.
- Generated assets:
  - `yunwu-1781591838-6b49808b`, purpose `irregular_grass_patch`, transparent ratio about `0.699`, visually usable as an irregular grass overlay.
  - `yunwu-1781591902-dee9f76c`, purpose `bush_flower_clump`, transparent ratio about `0.731`, visually usable as a bush/flower decoration.
  - `yunwu-1781591955-77ddba36`, purpose `dirt_grass_transition_patch`, transparent ratio about `0.598`, visually usable as a dirt/grass transition decal.
  - `yunwu-1781592018-40500807`, purpose `stone_wall_grass_edge`, transparent ratio about `0.805`, alpha-correct but visually mismatched.
- Contact sheet saved at `D:\workflow\magical-girl-tower-dogfood\captures\yunwu-transparent-mcp-retry-contact-sheet-20260616.png`.
- Kimi visual micro-check completed in about 117 seconds on the contact sheet:
  - verdict: `retry`;
  - usable now: `grass`, `bush_flowers`, `dirt_grass`;
  - needs redraw: `wall_grass`;
  - reason: `wall_grass` uses a pronounced side-view/isometric block perspective while the other three assets are soft top-down/aerial, so it will clash when composited.
- LCR dogfood findings:
  - the transparent edit route is materially better than earlier RGB/non-alpha terrain generations;
  - image generation still needs clearer per-call progress in the UI because 4 sequential image calls took about 329 seconds and can look stalled;
  - Kimi visual turns work with real attached images, but remain high-latency;
  - `/api/turn/start` callers must consistently include the admin session token, otherwise the API returns `Missing or invalid admin session token`.
- Next DS step: promote/use the first three assets only as map overlay candidates, and redraw `wall_grass` with direct top-down aerial perspective before attempting wall/grass transitions.

Latest LCR guard/tool-progress and visual retry round from 2026-06-16 15:30:

- Fixed a real dogfood regression in `RuntimeSupervisorService`: the 90% context guard must not automatically interrupt an active turn in the middle of file edits. It now warns/marks the active turn and lets the next turn boundary enforce compact/fork/continue decisions, avoiding half-written game changes.
- Updated Yunwu image MCP tool descriptions so DS/Kimi know each image call can take 45-90 seconds and should report per-asset progress (`actual_n`, local path, alpha status) instead of claiming a whole batch is complete.
- Added local stylesheet sanity checks to dogfood browser smoke for `file://` pages. The first implementation had a self-inflicted Unicode marker bug, so the final detector uses ASCII Unicode escapes and unit tests cover broken braces and mojibake markers.
- Source sidecar restart findings:
  - restarting source sidecar still loses current project/runtime state until the `.lcrproj` is reopened;
  - manually restarted source sidecar also needs provider keys re-presented through process environment or vault, otherwise compact/turn calls fail with `runtime_secret_missing`;
  - old provider threads can become `thread_missing` after app-server restart, and LCR recovered through `multi_provider_handoff` into a new DeepSeek/Kimi provider thread under the same user-visible task.
- DS completed the bounded organic overlay integration after recovery:
  - copied/used `overlay_grass_wisp.png`, `overlay_bush_clump.png`, and `overlay_dirt_edge.png`;
  - updated `js/sprites.js`, `js/ui.js`, and `css/style.css`;
  - ran `node --check js/*.js`;
  - ran LCR browser smoke with `click_text_until_absent("Next")`;
  - screenshot captured at `D:\workflow\magical-girl-tower-dogfood\workspace\.lcr\captures\organic-ground-overlay-smoke-2026-06-16T151302-363534+0800.png`.
- Kimi visual micro-check completed in about 107 seconds on the latest screenshot plus the reference image:
  - verdict: `retry`;
  - main issue: the map still reads as a pasted circular transparent overlay over visible square grid cells;
  - executable next strategy: generate/use a seamless full grass/background image, break the circular tree border into irregular clusters, tint the outer background to match the play area, add small entity shadows, and use individual obstacle sprites instead of a continuous pasted perimeter.
- Next DS step should not keep stacking transparent stickers. It should plan a better rendering route: seamless background or larger map art layer first, then place transparent sprites for characters, doors, stairs, monsters, trees, walls, and props on top.

Latest LCR evidence-display hardening from 2026-06-16 15:40:

- Fixed the next visible app gap before continuing the game loop: `thread/read` now decorates Codex `dynamicToolCall` and `commandExecution` items with compact `lcrVerifiedEvidence` metadata.
- The new metadata gives the UI a stable way to show `tool-event verified` or `command-event verified` without making users parse long JSON or trust model claims.
- Dynamic tool evidence includes tool name, server (`lcr_web`, `lcr_browser`, `yunwu_image`, etc.), status, verified flag, short summary lines, paths, and URLs when available.
- Command evidence includes shell command, status, exit code, and short output summary.
- Regression coverage now proves both cases:
  - app-server already returns a `dynamicToolCall`;
  - LCR overlays a missing `dynamicToolCall` from runtime events;
  - Codex `commandExecution` receives the same UI-ready evidence shape.
- Full sidecar unit tests after the fix: `134` passed.
- Isolation check after the fix: official `C:\Users\cyz19\.codex\config.toml` timestamp remained `2026-06-15 09:42:47`; the magic-tower workspace still contains the pre-existing empty `.codex` audit artifact from `2026-06-16 12:16:09`, but this pass did not create or modify it.

Latest DS planning failure and completion-quality fix from 2026-06-16 16:05:

- After the evidence-display fix, LCR started a new DeepSeek planning turn for the seamless/free-map route.
- A lightweight checkpoint was created first: `2026-06-16T154410-220618-0800-before-DS-seamless-map-planning-after-verified-evi`.
- DeepSeek successfully used LCR web tools:
  - `lcr_web_research_brief` record `research-brief-20260616T154649631896-113e85`;
  - `lcr_web_search_batch` record `search-batch-20260616T154707516285-0eaf66`.
- DeepSeek also triggered a structured `request_user_input` modal about the technical route. The selected answer was the recommended hybrid route: keep the invisible grid/DOM/collision architecture, render a seamless per-floor background art layer, and place transparent sprites/props above it.
- The turn still failed as a useful planning artifact: it completed after about `893937 ms`, but the final agent message only said it would produce the plan and did not include the plan.
- Dogfood milestone recorded this as `retry` in `.lcr/dogfood_run.json`; do not treat the turn as a successful design round.
- LCR now flags this pattern in `thread/read`: completed turns with verified tool/command activity but only short progress-note final messages get `lcrCompletionQuality.status=suspect` and `recommended_action=continue_or_retry_final_answer`.
- Full sidecar unit tests after the fix: `136` passed.
- The LCR web-search health result is mixed: the tools were callable and verified, but search result quality was weak for specialized game-dev queries. DS or the API manager should improve query templates and source prioritization before relying on the brief.

Latest live Yunwu retry recovery and startup-restore fix from 2026-06-16 18:36:

- Re-ran the real Yunwu transparent-asset retry through the source sidecar and confirmed the quality result is mixed but improved:
  - `yunwu-1781603540-512dd67e.png` yellow magical door: alpha-clean and isolated, but still too concept-art/portal-like for a strict top-down tile prop.
  - `yunwu-1781603573-7cffb5a4.png` stone stair entrance: alpha-clean and materially closer to a usable top-down map prop.
  - `yunwu-1781605126-6d5dc979.png` small grass tuft overlay: alpha-clean and usable as a small organic ground-decoration candidate.
- Fixed a live LCR evidence bug in `RuntimeService.read_thread`:
  - when `thread/read` returned stale `dynamicToolCall` items, LCR previously only inserted missing event items and did not refresh existing items from newer `item/completed` notifications;
  - this caused successful Yunwu image tool calls to remain stuck as `tool-event unverified` in the UI even though `.lcr/runtime_events.jsonl` contained the full completed result;
  - LCR now overlays the latest completed dynamic-tool event over an existing stale thread item before decorating evidence.
- Fixed a cold-start restore gap in `ProjectService`:
  - if `current_project.json` is missing, LCR now falls back to the most recent project from `projects.json`;
  - if `current_project.json` exists but is explicitly empty after `close_project()`, LCR still respects that and does not silently reopen a project.
- Live cold-start validation after a real source-sidecar restart on port `8795`:
  - `Magical Girl Tower Dogfood` reopened automatically;
  - `execution_host=wsl` and `wsl_distro=Ubuntu-24.04` were restored;
  - successful Yunwu image tool items on the recovered thread now read back as `tool-event verified`.
- Sidecar unit tests after this pass: `141` passed.
- Remaining runtime nuance:
  - cold-start restore intentionally does not persist provider secrets, so `secret_loaded=false` after restart until keys are re-presented through env or vault;
  - this is acceptable for isolation, but the UI should make the “runtime restored, secret needs re-presenting” state readable.

Latest provider-thread normalization fix from 2026-06-16 19:10:

Latest Yunwu image prompt/background protocol hardening from 2026-06-16 20:09:

- Fixed a real LCR protocol bug rather than only retrying image draws:
  - `game_asset_japanese_anime` now distinguishes `background_plate` from transparent cutout asset modes.
  - `yunwu_image_generate` no longer defaults to `background=transparent` in the MCP/runtime path.
  - prompt enhancement for background plates now asks for a continuous readable backdrop instead of repeating the alpha=0 transparent cutout contract.
- Real MCP verification after the fix:
  - transparent forest-canopy prop `yunwu-1781610570-32a5f267.png`: PNG RGBA, `has_alpha=true`, transparent ratio about `0.450`, usable as a large forest overlay/cluster candidate.
  - pre-fix grass plate `yunwu-1781610678-d2c38ac6.png`: PNG RGB, visually fake-transparent / checkerboard-adjacent, useful as a negative control proving the old protocol was wrong for scene plates.
  - final post-default-fix grass plate `yunwu-1781611452-52109ed5.png`: PNG RGB, `requested_background=auto`, `transparency_status=not_requested`, visually much closer to the intended route of “continuous grassy background plate + transparent props on top”.
- New routing rule from evidence:
  - use `yunwu_image_transparent_asset` for doors, stairs, keys, gems, monsters, HUD icons, heroine cutouts, and other true alpha sprites.
  - use `yunwu_image_generate` with `background=auto` or `opaque` for full-scene background plates or larger overworld/room backdrops.
  - do not use `has_alpha=true` as a quality proxy for background plates.
- Validation after the protocol fix:
  - targeted Yunwu prompt-guide/unit tests passed.
  - full sidecar unit test suite passed again: `143` tests.
  - live source sidecar on `8795` served the patched MCP tool path and wrote the new manifest fields `prompt_category`, `prompt_strategy_metadata.asset_mode`, and the correct `requested_background`.

Latest Yunwu retry and asset-context compatibility pass from 2026-06-16 20:46:

- Real MCP and HTTP retries confirmed the transport and protocol are both healthy:
  - `yunwu_image_transparent_asset` through `/api/runtime/mcp/tool-call` produced `yunwu-1781613489-e8fd42f7.png` with `RGBA`, `has_alpha=true`, and a transparency ratio about `0.709`.
  - `yunwu_image_generate` through `/api/runtime/mcp/tool-call` produced `yunwu-1781613600-f8537f8d.png` as a non-transparent forest background plate (`RGB`, `requested_background=auto`, `transparency_status=not_requested`).
  - the admin-token-protected HTTP image route also succeeded when called correctly and produced `yunwu-1781613742-8f6e65bb.png`, proving the earlier 400 was a caller issue rather than a Yunwu/LCR image-service failure.
- Prompt-mode diagnosis from the same pass:
  - the transparent stair retry still showed that a phrase such as `forest-ruin stair entrance` could be misclassified as `terrain_tileset` when it should be a `single_transparent_asset`.
  - `image_prompt_strategy.infer_asset_mode()` now prioritizes door/stair/key/monster/gem/pickup-like nouns before terrain keywords so single props are not accidentally rewritten as tilesets.
  - targeted prompt-guide regression coverage now proves that a `yellow rune-sealed door sprite for a forest ruin map` stays in `single_transparent_asset` mode.
- Asset-memory diagnosis from the same pass:
  - the live magical-tower registry already contained real `integration_status=in_use` and `manifest_keys=[...]` links, but some LCR context/dogfood logic still expected flat `manifest_key` and `in_use` fields.
  - the registry compatibility aliases now make those older readers truthful again without replacing the canonical richer schema.
- Updated routing rule from evidence:
  - use `yunwu_image_generate` for seamless/background plates and other opaque scene layers;
  - use `yunwu_image_transparent_asset` for cutout props and sprites;
  - do not treat `has_alpha=true` as sufficient evidence of in-game usability; Kimi or later screenshot review must still gate promotion.

- Dogfood inspection on the current magic-tower task showed that the same effective DeepSeek/Kimi route could accumulate many live provider-thread records after restarts and recoveries.
- This weakens the product goal that provider switching should feel like one continuous task with internal model handoff rather than a stack of unrelated chats.
- `TaskService` now normalizes task state on read and prunes duplicate live provider threads by canonical route:
  - canonical route key = provider id + canonical model id + canonical effort + permission mode + collaboration mode + role;
  - keep the newest live thread per route;
  - keep at most one recent missing-thread diagnostic per route.
- The normalization is alias-tolerant for model ids such as `deepseek-v4-pro` vs `deepseek/deepseek-v4-pro`.
- Regression coverage after the fix:
  - targeted pruning tests passed;
  - full sidecar unittest suite passed: `142` tests.
- Operational next step: restart the source sidecar so the live magic-tower task on port `8795` picks up the normalized task state before the next DS/Kimi/Yunwu loop.

1. Keep the current source sidecar on port `8795` as the authoritative runtime and preserve its loaded provider secrets while continuing this loop.
2. Ask DS for one bounded deep-research + implementation step that directly addresses the "still too blocky / still too much pasted overlay" critique while preserving current gameplay rules.
3. DS must explicitly reference `asset_id`, `manifest_key`/`manifest_keys`, or concrete promoted asset paths from the Asset Context Pack; vague mentions like “use grass assets” do not count as successful context use.
4. DS must use real LCR web tools for current map/autotile/background research and produce tool-event verified evidence, not only claimed research.
5. DS should treat `yunwu-1781613600-f8537f8d.png` or a successor background plate as the preferred base-map route, with transparent props layered above it; do not continue stacking transparent overlays on the old square-grid base.
6. DS must preserve working rules, run `node --check js/*.js`, and run browser smoke with a saved screenshot after the bounded change.
7. Ask Kimi to judge the new screenshot or contact sheet against the previous map screenshots and answer with either an executable visual plan or a strict `pass/retry/redraw` style verdict.
8. If the screenshot meaningfully improves, run Yunwu GPT-5.4 high as a playtest critic and feed the critique back to DS for route/UI/value priorities.
9. If the map is still blocky, have DS plan and then use Yunwu image tools for a dedicated seamless background / autotile-supporting redraw route instead of piling more overlays on a bad base.
10. Continue treating ignored `asset_id`/manifest paths, stale provider threads, unsupported context-mode values, missing tool evidence, misclassified prompt modes, or silently dropped visual assets as LCR bugs and fix the app before continuing.
11. Keep task continuity compact: if the same effective provider/model/effort route reappears after restart or alias variation, prefer the newest live provider thread and keep only one missing diagnostic for that route.

## Commit/Push Gate

Commit and push only after:

- relevant tests pass,
- provenance/resource ledger is updated,
- isolation checks pass,
- no secrets are detected in touched files,
- the commit groups a coherent LCR or game milestone.
