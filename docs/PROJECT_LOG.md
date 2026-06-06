# Project Log

## 2026-06-06

用户要求将 Research OS 模板升级为通用 human-in-loop auto researcher 仓库，并结合最新自动科研研究补齐治理、文档、skill 发现、开源组件集成和 harness engineering。

已完成：

- 将本地 v2 历史 bootstrap 到 `YinzhuCheng/research-os-template` 的远端 `main`。
- 创建并推送 `codex/research-os-v3` 分支。
- 将 `CONTROL/work_order.yaml` 更新为 `WO-0002`，授权本轮写入 `docs/`、`.agents/`、`.codex/`、`skills/`、`scripts/`、`config/`、`PUBLIC/`、`PROVENANCE/`、`PLAN/`。
- 刷新 `PUBLIC/claim_evidence_matrix.yaml` 和 `PROVENANCE/live_evidence_snapshot.yaml`，补充 Agent Laboratory、AI co-scientist、AI Scientist-v2、Agentic Science survey、Deep Researcher Agent、Claw AI Lab 和 OpenAI Codex 控制面的来源。
- 新增文档中心、项目摘要、项目日志和资产来源记录。

待完成：

- 新增 HTML 上手文档和技术报告。
- 新增 skill 镜像、开源组件 registry、adapter 模板、schema 和验证脚本。
- 运行完整验证和浏览器 QA。
- 创建 draft PR。
