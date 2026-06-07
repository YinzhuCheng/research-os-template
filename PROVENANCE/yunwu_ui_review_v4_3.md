# Research OS v4.3 Yunwu UI Review Summary

Timestamp: 2026-06-07T23:51:13.3447179+08:00

## Scope

- Model: `gpt-5.4`
- Reasoning: `low`
- Calls: 3 sanitized UI review prompts
- Inputs: local screenshot summaries, UI state descriptions, and previously recorded UX findings
- Excluded data: API key, authorization headers, private research material, raw project secrets
- Raw sanitized record: `PROVENANCE/yunwu_ui_review_v4_3.json`

## Cost

- Query service documented exchange rate: `$1 = 500,000 tokens`
- Token log quota for this pass:
  - researcher workflow: 4,002
  - desktop UX/accessibility: 8,648
  - safety/runtime recovery: 11,335
- Total quota: 23,985
- Estimated cost: USD 0.04797
- Budget: USD 3 hard cap

## Findings Used

- First-run project center still felt too technical because profile/model settings competed with create/open project.
- Runtime unavailable state needed direct recovery actions instead of passive explanatory copy.
- Approval actions needed clearer one-shot semantics and better risk language.
- Archive panel needed stronger recovery framing, not only snapshot creation.
- Final product modal should not silently preselect a product type when confidence is not high.
- Workspace needed a persistent "current action" guide to reduce competing panel noise.

## Fixes Applied After Review

- Collapsed profile/model controls under `高级设置：AI 模型与密钥引用`.
- Added a top-of-workspace current action guide.
- Reworked runtime unavailable state with `重试检测` and expandable configuration guidance.
- Renamed approval actions to `拒绝本次`, `允许一次`, and `取消队列`.
- Added archive recovery framing for future compare/restore/continue entries.
- Removed automatic final-product preselection while keeping report visibly recommended.

## Post-Fix QA

- Final screenshots were saved locally under ignored `apps/research-os-desktop/test-results/researcher-qa/after-yunwu-fix/`.
- Screenshot script reported no browser console errors and no Unicode replacement character.
- TypeScript, desktop check, Playwright, and Vite build passed after the Yunwu-driven fixes.
