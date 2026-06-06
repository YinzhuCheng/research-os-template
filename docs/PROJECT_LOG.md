# Project Log

## 2026-06-06

用户要求将 Research OS 模板升级为通用 human-in-loop auto researcher 仓库，并结合最新自动科研研究补齐治理、文档、skill 发现、开源组件集成和 harness engineering。

已完成：

- 将本地 v2 历史 bootstrap 到 `YinzhuCheng/research-os-template` 的远端 `main`。
- 创建并推送 `codex/research-os-v3` 分支。
- 将 `CONTROL/work_order.yaml` 更新为 `WO-0002`，授权本轮写入 `docs/`、`.agents/`、`.codex/`、`skills/`、`scripts/`、`config/`、`PUBLIC/`、`PROVENANCE/`、`PLAN/`。
- 刷新 `PUBLIC/claim_evidence_matrix.yaml` 和 `PROVENANCE/live_evidence_snapshot.yaml`，补充 Agent Laboratory、AI co-scientist、AI Scientist-v2、Agentic Science survey、Deep Researcher Agent、Claw AI Lab 和 OpenAI Codex 控制面的来源。
- 新增文档中心、项目摘要、项目日志和资产来源记录。
- 新增 `research-os-doc-site`、`research-os-integration-scout`、`research-os-experiment-manager`、`research-os-replay-eval-harness`。
- 新增 `.agents/skills/` 仓库级 skill 镜像，并通过镜像一致性检查。
- 新增 `docs/integrations/components.yaml`，记录 Agent Laboratory/AgentRxiv、AI Scientist-v2、AI co-scientist、Deep Researcher Agent、Claw AI Lab、AG2 和 OpenAI skills catalog 的适配边界。
- 新增 doc map、harness run、integration component schema 和 HTML/link/integration/skill mirror 检查脚本。
- 完成完整脚本验证和 Browser QA，截图与报告保留在 `build/browser-qa/`。

待完成：

- 审查 draft PR：[YinzhuCheng/research-os-template#1](https://github.com/YinzhuCheng/research-os-template/pull/1)。

## 2026-06-06 v3.1

用户要求将五个领域都深化，而不是只做数学重点和其他领域骨架。已新增：

- `domain_profiles/` 五大领域 profile 与 agent registry。
- 五个领域 skill 和对应 reference workflow。
- `templates/domain/` 五大领域 artifact 模板。
- `docs/domain-modes.html` 领域模式入口。
- 领域 schema、校验脚本、dashboard/doc map/技术报告链接。
- AlphaGeometry、FunSearch、AlphaEvolve 的 registry 记录，用作数学与算法发现范式来源。

## 2026-06-06 v3.2

用户要求按照“研究内核与反馈计算层”方案实施，并强调仓库要成为结构化程序，而不是意大利面式杂货工具箱。已新增：

- `research-os-research-kernel` skill，把候选对象、评价器契约、计算清单、评价结果、belief state、search trace、negative result、next action 和 human gate 统一建模。
- `config/schemas/research_kernel.schema.json`、`templates/yaml/research_kernel.template.yaml` 和 `templates/research_kernel/research_cycle.template.yaml`。
- 五大领域 profile 的 `kernel_bindings`，以及领域模板中的 evaluator 计算清单。
- `check_research_kernel.ps1`、`check_domain_kernel_bindings.ps1` 和 `check_no_orphan_skills.ps1`。
- 文档、dashboard、claim-evidence 和 doc map 的 research kernel 链接。
