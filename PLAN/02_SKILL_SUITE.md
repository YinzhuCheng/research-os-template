# Skill 套件设计

## 总原则

入口 skill 只负责判断上下文、加载必要参考、分发子 skill。子 skill 保持短小，复杂规则放入 `references/`，稳定操作放入 `scripts/`，模板放入 `assets/`。

## Skill 列表

- `research-os-orchestrator`：入口 skill，读取输入、语言模式、人类介入档位和当前阶段。
- `research-os-init`：从 GPT 对话、研究草稿、demo 代码生成规范项目。
- `research-os-alignment`：生成需求对齐清单、隐含假设、建议问题和阶段闸门。
- `research-os-execution-harness`：生成 work order，执行前后记录审计信息。
- `research-os-evidence`：文献、假设、claim-evidence matrix。
- `research-os-analysis`：结果分析、消融、失败案例、统计与威胁分析。
- `research-os-feasibility-probe`：生成研究者预算内的最小可行性验证，覆盖成功、失败、不确定结果后的调整路径，不限定研究范式。
- `research-os-resource-guard`：覆盖 LLM/API、云服务器、实验材料、人工标注、仪器机时等资源预算与异常增长。
- `research-os-live-evidence-refresh`：联网刷新文献、工具、API、价格、会议规则、数据许可、法律/伦理要求等时效性信息。
- `research-os-harness-audit`：检查 AGENTS、work order、allowed/forbidden paths、hooks、权限模式、MCP、外部写入、未提交变更和审计缺口。
- `research-os-paper-authoring`：仅在论文/投稿目标启用时，按会议/期刊模板驱动英文 LaTeX 投稿稿。
- `research-os-visual-communication`：仅在传播目标需要时，处理排版、配色、矢量图、图表美化、附录图表。
- `research-os-polish-factcheck`：逻辑润色、结构优化、专业化、事实校验、去模板腔。
- `research-os-review-rebuttal`：自 review、攻击性审稿、rebuttal、修稿循环。
- `research-os-public-export`：只从 `PUBLIC/` 和脱敏 `PROVENANCE/` 生成可上传包。

## 触发关系

`research-os-orchestrator` 可以调用其他子 skill。初始化阶段必须先判断研究类型、预算来源、验证对象和传播目标；缺信息时调用 `alignment`。任何真实资源调用前调用 `resource-guard`，任何时效性外部信息使用前调用 `live-evidence-refresh`，任何执行前后调用 `execution-harness` 和 `harness-audit`。论文阶段只在研究者明确启用时调用 `paper-authoring`、`visual-communication`、`polish-factcheck` 和 `review-rebuttal`。

## 外部参考

设计参考 OpenAI Skills 小模块组合原则、AI Scientist 的端到端闭环、Agent Laboratory 的分阶段人类反馈、Co-Scientist 的生成/反思/排序/演化、多 agent 透明性要求。
