# 公开审计摘要

当前模板已完成第一版实现，并正在加入 Research OS v2 的研究无关性与 Codex harness 补强。

- 隐私策略：`PUBLIC/` 与 `PRIVATE/` 双目录强隔离。
- 公开导出：已实现 `scripts/export_public.ps1`。
- 运行 manifest：已实现 `PROVENANCE/run_manifest.jsonl`。
- 资源账本：已加入 `PROVENANCE/resource_ledger.jsonl`。
- 实时证据：已加入 `PROVENANCE/live_evidence_snapshot.yaml`。
- Skill 套件：已实现入口、初始化、对齐、执行、证据、分析、论文、视觉、润色、review、公开导出，以及 v2 的 feasibility、resource guard、live evidence、harness audit。
- Codex harness：已加入根 `AGENTS.md`、`.codex/config.toml.example`、hook 策略样例和 harness requirements。
- 最终验证：[final_validation_report.md](final_validation_report.md)。

v2 约束：

- 不默认 LLM、机器学习、数据集、baseline、论文、投稿目标或固定预算。
- 最小可行性验证的预算、工具、样本量、设备、模型和人工步骤必须来自入口材料或研究者确认。
- 真实凭据不得落盘，只能记录环境变量名、secret store 路径、IAM 角色或短期凭据获取流程。
