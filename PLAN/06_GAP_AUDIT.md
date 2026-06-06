# 缺口审计

## 当前状态

Commit 9 已补强 Research OS v2：研究无关性、Codex harness、研究者定义资源预算、可行性探针、资源守护、实时证据刷新和安全凭据方案，并完成验证。

## 已知缺口

- 已实现目录骨架。
- 已实现 `PUBLIC/` 与 `PRIVATE/` 强隔离的基础 `.gitignore`。
- 已实现 schema 和样例对象。
- 已实现入口、初始化、对齐、执行、证据、分析、论文、视觉、润色、review、公开导出 skill。
- 已实现基础审计脚本。
- 已实现静态仪表盘。
- 已实现 LaTeX 投稿包和图表模板。
- 已运行验证。
- 已新增 `AGENTS.md`、`.codex/config.toml.example` 和 hooks 示例。
- 已新增 `research-os-feasibility-probe`、`research-os-resource-guard`、`research-os-live-evidence-refresh`、`research-os-harness-audit`。
- 已将论文链路改为可选传播目标。
- 已将固定预算改为研究者定义的 `resource_budget`。

## 残余风险

- LaTeX 完整编译在本机 MiKTeX 环境中超时，已保留 `build/latex/main.log`；源码静态检查已通过。
- Dashboard v2 静态检查已通过；仍缺浏览器截图级 QA。
- Schema 校验为 smoke validation，后续可升级为完整 JSON Schema/YAML 校验。
- hooks 示例是策略样例，真正生效取决于研究者复制/启用 `.codex/config.toml.example` 并在受信任项目中运行。
- resource guard 当前是模板级账本和检查脚本，不直接控制云厂商账单；云预算上限仍需在云平台侧设置。
- live evidence refresh 记录来源和访问日期，但不能替代人工阅读全文或目标领域专家审查。
- `scripts/write_manifest.ps1` 在 `powershell -File` 入口下对多值数组参数不够直观；后续应补一个列表文件或 JSON 输入接口，避免命令行参数折叠。

## 下一步

已提交 `feat: add research neutral harness v2`。后续优先补 Browser 截图 QA、完整 JSON Schema/YAML 语义校验和云平台侧预算硬上限模板。
