# Project Summary

Research OS v3 是一个通用的 human-in-loop auto researcher 仓库模板。它的默认目标不是替研究者自动完成某个具体学科任务，而是把研究想法、草稿、demo 或实验过程组织成可执行、可审计、可复现、可交接的工作空间。

## 当前状态

- 当前阶段：`research-os-v3.9`
- 控制文件：`CONTROL/work_order.yaml` 已更新为 `WO-0010`
- 默认语言：`zh-first`
- 默认边界：研究无关、低介入但阶段闸门、真实资源调用和外部写入需人工确认
- 主要产物：普通研究者上手文档、技术路线 HTML、三阶段 Research OS 流程、循环验收 gate、最终产物 workflow、git-backed archive、research kernel、领域 profile、skill 镜像、开源组件 registry、harness 检查脚本

## 核心原则

- 先对齐研究者意图，再执行实验或报告生成。
- 先记录预算、停止条件和允许路径，再进行 mutating 工作。
- 先刷新时效性证据，再把外部结论写进公开文档。
- 默认不 vendoring 大段第三方源码，优先记录来源、许可证、安装方式、环境变量名和 adapter 产物映射。
- 原始敏感材料、密钥、cookie、authorization header 和私有审计不得进入 `PUBLIC/` 或 git 历史。

## 重要入口

- 新手入口：`docs/start-here.html`
- 技术报告：`docs/technical-report.html`
- 文档地图：`docs/doc_map.yaml`
- 开源组件 registry：`docs/integrations/components.yaml`
- 仓库规则：`AGENTS.md`
- Codex harness 示例：`.codex/requirements.md`

## v3.1 领域层

- `docs/domain-modes.html`：五大领域入口。
- `domain_profiles/`：五大领域 profile 和 agent capability registry。
- `templates/domain/`：五大领域产物模板。
- `skills/research-os-math-discovery`、`research-os-applied-math-modeling`、`research-os-ml-research-protocol`、`research-os-cs-research-artifact`、`research-os-statistical-inference`：领域执行入口。
- `scripts/check_domain_profiles.ps1`、`check_agent_capabilities.ps1`、`check_domain_templates.ps1`、`check_domain_router.ps1`：领域层 harness 检查。

## v3.2 研究内核层

- `skills/research-os-research-kernel`：统一 generate-evaluate-update-human gate 程序。
- `config/schemas/research_kernel.schema.json`：候选、评价器、计算清单、belief、trace、negative result、next action 和 human gate schema。
- `templates/research_kernel/research_cycle.template.yaml`：跨领域研究循环模板。
- `domain_profiles/*/profile.yaml`：通过 `kernel_bindings` 把领域产物挂接到统一内核。
- `scripts/check_research_kernel.ps1`、`check_domain_kernel_bindings.ps1`、`check_no_orphan_skills.ps1`：防止 skill 体系退化为松散工具箱。

## v3.9 三阶段与最终产物层

- 用户视角宏观阶段：初始化阶段、半自动循环研究阶段、最终产物阶段。
- 内部阶段：`initialization_intake`、`loop_acceptance_gate`、`loop_plan_alignment`、`loop_user_decision`、`loop_execute_analyze`、`final_product_selection`、`final_product_production`、`export_release_gate`。
- 第二阶段循环必须先验收当前产物；未验收通过时不得进入下一步计划。
- 所有用户选择必须包含推荐选项、默认选项和自然语言 free-form 路径。
- 新增最终产物技能：`research-os-final-product`、`research-os-report-authoring`、`research-os-software-productization`。
- 新增 git-backed archive：bridge API、`scripts/create_archive_snapshot.ps1`、`scripts/check_archives.ps1`、`PUBLIC/archive_index.json`、`PROVENANCE/archive_index.jsonl`。
- Dashboard/Copilot 已加入三阶段 phase bar、分组主操作、最终产物弹窗、存档弹窗和自然语言 UI 目标输入。
