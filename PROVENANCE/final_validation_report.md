# 最终验证报告

验证日期：2026-06-06

## v3 验证结果

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| Schema 轻校验 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1` | 通过，10 个 JSON schema 均可解析 |
| Skill 结构校验 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1` | 通过，19 个 skill |
| Harness 审计 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_harness.ps1 -PythonPath <bundled-python>` | 通过，hook 编译和外部写入阻断样例通过 |
| Dashboard 静态检查 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1` | 通过 |
| 隐私扫描 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1` | 通过 |
| HTML 文档检查 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_html_docs.ps1` | 通过 |
| 文档链接检查 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_docs_links.ps1` | 通过，12 个 markdown/html 文件 |
| Integration registry 检查 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_integrations.ps1` | 通过，8 个组件 |
| Skill 镜像检查 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_skill_mirror.ps1` | 通过，19 个镜像 skill |
| Git diff whitespace | `git diff --check` | 通过 |

## 浏览器 QA

使用 Codex in-app Browser 通过本地 HTTP 服务检查以下页面：

- `docs/start-here.html`
- `docs/technical-report.html`
- `PUBLIC/index.html`

视口：

- Desktop：1440 x 900
- Mobile：390 x 844

结果：

- 共检查 6 个页面/视口组合。
- 无缺失关键文案。
- 无控制台 error。
- 无水平溢出。
- 无可见元素越界。

截图和 JSON 报告保留在 `build/browser-qa/`：

- `build/browser-qa/start-here-desktop.png`
- `build/browser-qa/start-here-mobile.png`
- `build/browser-qa/technical-report-desktop.png`
- `build/browser-qa/technical-report-mobile.png`
- `build/browser-qa/dashboard-desktop.png`
- `build/browser-qa/dashboard-mobile.png`
- `build/browser-qa/report.json`

## v3 产物摘要

- 新增面向一般研究者的 `docs/start-here.html`。
- 新增面向后续 agent 和维护者的 `docs/technical-report.html`。
- 新增 `.agents/skills/` 仓库级 skill 镜像，`skills/` 仍为权威源。
- 新增 `docs/integrations/components.yaml`，记录 8 个开源自动研究组件的来源、许可证、安装入口、环境变量名、产物映射和风险。
- 新增 doc map、harness run、integration component schema 和对应模板。
- 新增 HTML、链接、integration、skill mirror 检查脚本。

## 残余风险

- LaTeX 完整编译在 v2 阶段曾因本机 MiKTeX 环境超时，v3 未改动论文链路，未重复运行完整 LaTeX 编译。
- 当前 YAML 语义校验仍以 smoke validation 和确定性文本检查为主，后续可引入完整 YAML schema validator。
- 开源组件 registry 是适配记录和设计入口，不代表第三方组件已安装、已授权运行或已通过安全审计。
- Hooks 示例需要研究者在受信任项目中启用 `.codex/config.toml.example` 才会成为运行期控制。
