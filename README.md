# Codex Research OS Template

这是一个研究方向无关的 Codex 科研项目模板，用于把对话、研究计划草稿或实验 demo 转成可执行、可追溯、可审计的研究仓库。它不默认 LLM、机器学习、数据集、baseline、论文或投稿目标；这些内容只能在入口材料中出现，或由研究者在对齐阶段确认。

## 默认行为

- 内部计划、实验记录、分析和审计默认中文；入口可设 `language_mode: en-only`。
- 论文是可选传播产物。只有明确设置论文、报告、投稿等 `dissemination` 目标后，才启用对应写作链路。
- 预算由研究者定义为 `resource_budget`，可覆盖时间、算力、云资源、实验耗材、API、模型、人工、仪器机时等资源。
- 默认低介入，但预算、真实资源调用、凭据使用、外部写入、公开导出和投稿必须人工确认。
- `PUBLIC/` 可公开；`PRIVATE/` 默认不进 git；真实密钥、token、cookie、SSH 私钥和云账号密码不得落盘。

## 主要入口

- 快速上手 HTML：[docs/start-here.html](docs/start-here.html)
- 五大领域模式 HTML：[docs/domain-modes.html](docs/domain-modes.html)
- 完整技术路线 HTML：[docs/technical-report.html](docs/technical-report.html)
- 研究内核模板：[templates/research_kernel/research_cycle.template.yaml](templates/research_kernel/research_cycle.template.yaml)
- 文档中心：[docs/README.md](docs/README.md)
- 文档地图：[docs/doc_map.yaml](docs/doc_map.yaml)
- 开源组件 registry：[docs/integrations/components.yaml](docs/integrations/components.yaml)
- 计划：[PLAN/00_MASTER_PLAN.md](PLAN/00_MASTER_PLAN.md)
- Codex 仓库规则：[AGENTS.md](AGENTS.md)
- Codex harness 示例：[.codex/requirements.md](.codex/requirements.md)
- 静态 dashboard：[PUBLIC/index.html](PUBLIC/index.html)
- 公开区：[PUBLIC/README.md](PUBLIC/README.md)
- 私有区：[PRIVATE/README.md](PRIVATE/README.md)
- 控制区：[CONTROL/README.md](CONTROL/README.md)
- 来源与审计：[PROVENANCE/README.md](PROVENANCE/README.md)
- Skill 套件：[skills/README.md](skills/README.md)
- 领域 profiles：[domain_profiles/README.md](domain_profiles/README.md)

## Research OS v3

v3 将模板定位为通用的 human-in-loop auto researcher 仓库。默认不假设研究方向、模型、provider、数据集、baseline、论文或预算；这些内容只来自研究者入口材料或明确决策记录。

新增重点：

- 面向普通研究者的 HTML 快速上手页。
- 面向后续 agent 和维护者的 HTML 技术路线。
- `.agents/skills/` 仓库级 skill 发现镜像。
- 开源自动研究组件 registry 和 adapter 模板。
- HTML 链接、skill 镜像、integration registry 和 harness run 检查。

## 使用原则

## Research OS v3.2

v3.2 新增统一研究内核与反馈计算层：所有领域研究循环都先表达为 `candidate -> evaluator_contract -> evaluation_result -> belief_state -> search_trace/negative_result -> next_action_policy -> human_judgment_gate`。每个 evaluator 必须列出计算或检查，包括指标、过程、输入、尺度、阈值、资源估计、失败模式和复现记录。这样领域 skill 是结构化程序的一部分，而不是松散工具箱。

## Research OS v3.1

v3.1 新增五大领域深度研究范式层：基础数学、应用数学、机器学习、计算机科学和统计学。每个领域都有 `domain_profiles/` 中的 profile、agent registry、`templates/domain/` 中的产物模板，以及对应的领域 skill。数学领域默认不启用形式化证明，先强化猜想、例子、反例、证明策略和 proof-gap review。

先对齐研究者真实意图，再定义最小可行性验证；先登记资源预算和停止条件，再执行 work order；先刷新时效性证据，再依赖外部信息；公开导出前必须通过隐私扫描。
