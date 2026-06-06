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
- `research-os-paper-authoring`：目标会议/期刊模板驱动的英文 LaTeX 投稿稿。
- `research-os-visual-communication`：排版、配色、矢量图、图表美化、附录图表。
- `research-os-polish-factcheck`：逻辑润色、结构优化、专业化、事实校验、去模板腔。
- `research-os-review-rebuttal`：自 review、攻击性审稿、rebuttal、修稿循环。
- `research-os-public-export`：只从 `PUBLIC/` 和脱敏 `PROVENANCE/` 生成可上传包。

## 触发关系

`research-os-orchestrator` 可以调用其他子 skill。论文阶段优先调用 `paper-authoring`，再调用 `visual-communication`，再调用 `polish-factcheck`，最后调用 `review-rebuttal`。

## 外部参考

设计参考 OpenAI Skills 小模块组合原则、AI Scientist 的端到端闭环、Agent Laboratory 的分阶段人类反馈、Co-Scientist 的生成/反思/排序/演化、多 agent 透明性要求。
