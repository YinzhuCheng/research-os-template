# 最终验证报告

验证日期：2026-06-06

## 验证结果

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| Schema 轻校验 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1` | 通过 |
| Skill 结构校验 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1` | 通过，15 个 skill |
| 隐私扫描 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\scan_privacy.ps1` | 通过 |
| Dashboard 静态检查 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1` | 通过 |
| 研究中立性 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_research_neutrality.ps1` | 通过，覆盖 4 类 dry-run 研究 |
| Harness 审计 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_harness.ps1 -PythonPath <bundled-python>` | 通过 |
| Resource guard | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_resource_guard.ps1` | 通过 |
| Live evidence | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_live_evidence.ps1` | 通过 |
| LaTeX 源码静态检查 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_latex_sources.ps1` | `paper_enabled: false` 时跳过；`-Force` 时通过 |
| LaTeX 编译 | `pdflatex -interaction=nonstopmode -halt-on-error -output-directory ..\..\build\latex main.tex` | 超时，已终止进程并保留 `build/latex/main.log` |
| Hash 清单 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\hash_paths.ps1` | 通过，写入 `PROVENANCE/hashes.json` |
| 公开导出 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export_public.ps1 -Name v2_validation_export` | 通过，写入 `exports/v2_validation_export.zip` |

## 说明

- MiKTeX/pdflatex 已安装，但本次最小论文编译在 120 秒内未完成，可能卡在首次包解析或依赖安装。源码静态检查已确认主稿、附录、BibTeX、TikZ 与 PGFPlots 样例文件齐全。
- `tool_search` 未暴露 Browser 控制工具，因此前端只做了静态检查和 JSON 解析；未做截图级视觉 QA。
- 当前系统 `python` 是 Windows Store 占位程序；harness 验证使用 Codex bundled Python 完成 hook 编译和外部写入阻断样例。
- 公开导出脚本已实现并通过测试，导出产物保留在 `exports/`。

## Skill 清单

- `research-os-orchestrator`
- `research-os-init`
- `research-os-alignment`
- `research-os-execution-harness`
- `research-os-evidence`
- `research-os-analysis`
- `research-os-feasibility-probe`
- `research-os-resource-guard`
- `research-os-live-evidence-refresh`
- `research-os-harness-audit`
- `research-os-paper-authoring`
- `research-os-visual-communication`
- `research-os-polish-factcheck`
- `research-os-review-rebuttal`
- `research-os-public-export`

## 残余风险

- LaTeX 完整编译需要后续确认 MiKTeX 包安装策略或改用固定 TeX Live 环境。
- 当前 schema 校验是 smoke validation，不是完整 JSON Schema/YAML 语义校验。
- 静态 dashboard 未做真实浏览器截图验证。
- Hooks 示例需要研究者在受信任项目中启用 `.codex/config.toml.example` 才会成为运行期控制。
