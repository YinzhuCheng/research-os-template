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

## v3 当前补强方向

- 已启动 `WO-0002`，将仓库升级为通用 human-in-loop auto researcher。
- 已补普通研究者快速上手 HTML 与后续 agent 技术路线 HTML。
- 已新增文档地图、项目摘要、项目日志和资产来源记录。
- 已将 Research OS 文档入口接入根 README 和公开 dashboard。
- 已补 `.agents/skills/` 仓库级 skill 镜像、开源组件 registry、adapter 模板和 v3 验证脚本。
- 已完成浏览器 QA，覆盖 `docs/start-here.html`、`docs/technical-report.html` 和 `PUBLIC/index.html` 的 desktop/mobile 视口。

## v3 剩余风险

- 当前 dashboard 能链接到 HTML，但内置 reader 对 HTML/YAML 仍以源码方式展示；直接打开页面是主要使用路径。
- 开源组件 registry 只应记录适配和来源，不得绕过许可证、密钥、预算或 sandbox 控制。
- `gh` CLI 未登录，PR 创建将优先使用 GitHub connector；本地 git push 已通过现有凭据成功。
- YAML 语义校验仍是轻量检查，后续可接入完整 YAML schema validator。

## v3.1 当前补强方向

- 已新增五大领域深度研究范式层，通过 `domain_profiles/`、`templates/domain/`、领域 skill 和校验脚本表达学科口味。
- 基础数学默认不做形式化证明；先通过猜想、例子、反例、证明策略、proof-gap 和 human review 降低错误证明风险。
- 应用数学、机器学习、计算机科学和统计学均拥有独立产物模板与质量闸门。

## v3.1 剩余风险

- 当前领域 YAML 仍以轻量结构检查为主，后续可引入完整 YAML parser 和 JSON Schema 语义校验。
- 领域 agent 目前是 skill 内部角色和 capability registry，不是独立 agent runtime；后续如接入外部 runtime，必须新增 adapter、权限和回放验证。

## v3.2 当前补强方向

- 已新增统一 research kernel，把 candidate、evaluator contract、evaluation result、belief state、search trace、negative result、next-action policy 和 human gate 变成一等对象。
- 已把“列出计算”固化为 evaluator contract 必填清单：metric/check、formula/procedure、inputs、scale、threshold、resource estimate、failure mode 和 replay note。
- 已为五大领域 profile 和模板新增 kernel bindings，避免领域 skill 只是一组互不相干的提示词或工具。
- 已新增 no-orphan-skill 检查：主路由 skill 必须有 schema/template、validator、doc map 或明确治理位置。

## v3.2 剩余风险

- 目前 YAML 语义验证仍以结构和关键字段检查为主；后续可接入严格 YAML parser 与 JSON Schema 实例校验。
- research kernel 是模板级程序契约，不是持久数据库或独立运行时；如果未来需要长期跨项目记忆，需要新增存储、迁移和隐私策略。
- evaluator contract 先约束“必须列出计算”，但不自动判断计算是否科学合理；高风险领域仍需要专家人工闸门。
- 数学形式化仅保留 future slot；未来启用 Lean/Coq/Isabelle 前需要单独 work order、工具链安全审查和误报处理规范。
