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
