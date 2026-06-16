# LCR Release Execution Loop

Last revised: 2026-06-16 23:05 +08:00

## Objective

Drive the magical-tower dogfood project to a publishable local-release standard while, in parallel, hardening Local Codex Router (LCR) itself to a publishable standard for multi-provider agent work.

This plan is the operator loop for the current phase. It does not replace the broader release plan in `PLAN/16_LCR_MAGIC_TOWER_DOGFOOD_RELEASE_PLAN.md`; it narrows the next execution slices so each slice can be verified, recorded, committed, and pushed.

## Roles

- LCR maintainer (Codex operator): fix runtime, task continuity, tool reliability, UI/UX truthfulness, evidence capture, isolation, and packaging blockers.
- DeepSeek: primary research/design/coding agent inside LCR. Prefer DS for non-visual work and bounded implementation turns.
- Kimi: visual micro-checks, visual planning, and image-grounded executable suggestions. Do not give Kimi long open-ended coding turns unless its current multimodal path is healthy.
- Yunwu GPT-5.4 high: milestone playtest critic. Use after a meaningful playable improvement, not as the first mover.
- Yunwu image tools: asset generation/edit route. Use aggressively but in evidence-backed batches.

## Current High-Signal Blocking Issues

1. Task continuity can still degrade after restarts or stale-thread recovery.
   - Symptom: live provider threads exist, but `active_provider_thread_id` and project `current_thread_id` can fall to `null`.
   - Release impact: provider switch no longer feels like one continuous task; direct MCP/tool actions may attach to stale or missing threads.

2. Yunwu image transport and prompt routing need to be treated as partly recovered, not simply “down”.
   - Latest evidence: multiple live `yunwu_image_transparent_asset` MCP calls succeeded again on 2026-06-16 22:41-22:52 and returned real RGBA transparent PNG cutouts, but upstream/TLS instability was also observed earlier the same evening.
   - Release impact: LCR must report a truthful mixed health state: usable when healthy, retry/degraded when upstream transport regresses, and avoid silently misclassifying prompts that lower asset quality.

3. Asset memory is better than before but still not strong enough.
   - Registry, manifest, and in-use truth have improved, but agent loops still need stronger forced references to concrete `asset_id`, manifest keys, and promoted paths.
   - Release impact: agents can still appear to “forget” existing assets even when the state is present.

4. Game visual route is still not at publishable quality.
   - Current critique: the map still reads as block/grid based with layered decals instead of a unified JRPG overworld.
   - Release impact: the dogfood target is not yet a good release-quality test case.

5. The active magical-tower task is currently focused on a recovered DeepSeek provider thread whose latest turn is interrupted after real web research.
   - Latest evidence: active thread `019ed0dc-6c17-75f3-9499-c7cf7b963777` contains verified `lcr_web_research_brief`, `lcr_web_search_batch`, and `lcr_web_fetch` items, but its last turn is `interrupted`.
   - Release impact: before asking DS to continue, LCR must treat this as resumable task continuity rather than a fresh blank chat or an excuse to lose asset/context state.

## Execution Loop

### Slice A: LCR self-healing and continuity

Goals:
- Repair task/project active-thread self-healing.
- Keep provider switching inside one visible task.
- Preserve WSL-first execution and live source-sidecar authority.

Required evidence:
- `tasks.current_task()` can restore `active_provider_thread_id` to a valid live thread when stale or missing.
- project `current_thread_id` follows the repaired active thread.
- targeted sidecar tests pass.

### Slice B: Tool health and degraded-mode truthfulness

Goals:
- Keep Yunwu image path usable when upstream is healthy.
- When upstream is unhealthy, show truthful retry/degraded state and avoid fake success.
- Keep Kimi visual path and DS built-in tool path measurable.

Required evidence:
- Yunwu retry/backoff behavior covered by tests.
- current health state recorded in provenance and metadata.
- no raw secrets or large raw payloads leak into repo state.

### Slice C: Asset-context enforcement

Goals:
- Every DS implementation step must reference concrete asset evidence.
- Promoted assets must be provably used by the game, not only claimed.

Required evidence:
- prompts or context packs require concrete `asset_id` / manifest refs / promoted paths.
- browser smoke screenshot proves new assets are actually visible in the game.

### Slice D: Game quality loop

Goals:
- Use DS to research “what makes a good magic tower” and choose a better visual route.
- Use Kimi for image-grounded judgments.
- Use Yunwu GPT-5.4 high to critique only after a real playable improvement.

Required evidence:
- DS performs verified web/tool research before major visual/route changes.
- Kimi receives real screenshots or contact sheets and returns executable visual guidance.
- Yunwu GPT critique feeds into a bounded next DS implementation step.

## Immediate Ordered Tasks

1. Fix task self-healing so a stale or empty active provider thread resolves to the best live thread.
2. Validate the fix with targeted tests and live task-state inspection.
3. Record the Yunwu mixed-health findings and keep both retry hardening and prompt-mode fixes in place.
4. Re-open the magical-tower task through the repaired continuity path and keep the current DeepSeek research thread as the visible task focus unless stronger evidence says it is unusable.
5. Ask DS for one bounded research-or-implementation step that:
   - references concrete assets,
   - uses real built-in tools when research is requested,
   - runs WSL-safe validation,
   - stops after reporting exact changed files and screenshots.
6. Prefer the recovered Yunwu transparent assets and the fixed `single_transparent_asset` prompt route for the next map-prop and pickup generation batch; do not continue using prompts whose metadata shows `animation_frame_set` for single keys/doors/stairs.
7. Use Kimi for a strict visual micro-check on the resulting screenshot(s).
8. If the screenshot materially improves, run Yunwu GPT-5.4 high as a critique loop and convert the feedback into the next DS step.
9. After each meaningful slice:
   - reread this plan,
   - revise it if evidence changed,
   - append provenance/resource entries,
   - commit and push a coherent slice if tests and isolation checks pass.

## Validation Checklist

- Sidecar targeted tests pass for every runtime/task fix.
- Full relevant sidecar suite passes before pushing a larger slice.
- `C:\Users\cyz19\.codex\config.toml` remains untouched.
- Workspace root does not gain new `.codex*` state.
- No API key, Authorization header, cookie, admin token, or raw base64 is written to tracked artifacts.
- WSL remains the default execution host for actual game-agent work.

## Commit Policy

Commit only coherent slices:
- one continuity/runtime fix slice,
- one tool/health reporting slice,
- one game dogfood improvement slice.

Do not mix broad unrelated cleanup into the same commit.
