# Research OS v3.8 Validation Report

## Scope

v3.8 adds browser-local UI personalization to the public Dashboard and Copilot pages:

- user settings button on `PUBLIC/index.html` and `PUBLIC/copilot.html`;
- five UI styles: clean SaaS, compact enterprise, soft system, developer dark, and editorial report;
- Chinese default interface language;
- full English interface option;
- visible note that final paper output defaults to English regardless of UI language;
- localStorage persistence plus optional `?lang=` and `?theme=` URL overrides for QA/direct links;
- responsive wrapping and narrow-screen constraints for Chinese/English labels.

No research workflow, automation boundary, raw intake handling, or `PRIVATE/` material was changed.

## Validation Commands

Passed locally on 2026-06-07:

- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_schemas.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_html_docs.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_dashboard.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_copilot_resource_rendering.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_privacy.ps1 -Paths PUBLIC,PROVENANCE`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/package_template.ps1 -DryRun`

## Browser QA

Temporary local HTTP server:

- URL: `http://127.0.0.1:8766/`
- Server stopped after QA.

Chrome headless DOM checks passed:

- Dashboard default Chinese rendered `用户设置`, `界面风格`, `中文（默认）`, `论文输出：最终完成论文时默认使用英文`, all five style options, and `UI 设置`.
- Copilot default Chinese rendered `用户设置`, `保存初始材料`, `证据板`, all five style options, and the final-paper English note.
- Dashboard English/dark rendered `User Settings`, `Interface Style`, `Chinese (default)`, `Paper output: final papers default to English`, `Developer Dark`, and `data-theme="dark"`.
- Copilot English/dark rendered `User Settings`, `Save Initial Material`, `Evidence Board`, `Developer Dark`, and `data-theme="dark"`.

Nonblank screenshots were generated in the user temp directory:

- `C:\Users\cyz19\AppData\Local\Temp\research-os-v38-dashboard-en-dark.png`
- `C:\Users\cyz19\AppData\Local\Temp\research-os-v38-copilot-en-dark.png`
- `C:\Users\cyz19\AppData\Local\Temp\research-os-v38-dashboard-mobile-zh.png`
- `C:\Users\cyz19\AppData\Local\Temp\research-os-v38-copilot-mobile-zh.png`

Manual screenshot review found no obvious layout collapse. Mobile Copilot title and state pills were adjusted after screenshot review to avoid clipping at 390px width.

## Notes

- No paid API, cloud, GPU, lab resource, external writeback, external download, or real private upload was used.
- Preferences are browser-local; schema-backed shared project preferences remain a future optional slot.
