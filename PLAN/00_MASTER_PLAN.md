# Codex Research OS 实施总计划

## 目标

在本目录实现一个可复用的 Codex 科研项目模板。模板用于把 GPT 对话、研究计划草稿或简单实验 demo 规范成可执行、可审计、可追溯的研究仓库。模板必须与具体研究方向无关，不默认 LLM、机器学习、数据集实验、baseline、论文或投稿目标。

## 默认策略

- 语言：`zh-first`，计划、实验记录、分析和内部审计默认中文；入口允许设置 `en-only`。
- 可选语言：入口允许设置 `en-only`，此时项目计划、审计、网页和论文均使用英文。
- 人类介入：默认 `low`，阶段内自动推进，阶段切换必须给决策者确认清单。
- 隐私：严格区分 `PUBLIC/` 和 `PRIVATE/`。真实密钥、token、cookie、SSH 私钥、云账号密码不得落盘。
- 资源：预算由研究者定义为 `resource_budget`，覆盖时间、算力、云、实验耗材、API、模型、人工、仪器等资源。
- 可行性：每个项目都先定义 `feasibility_probe`，预算、工具、样本量、设备、模型和人工步骤均来自入口材料或对齐确认。
- 论文：论文是可选传播产物。仅当 `dissemination.paper_enabled: true` 或研究者明确要求论文/投稿时启用 LaTeX、视觉和 review/rebuttal 链路。
- Harness：模板根提供 `AGENTS.md`、`.codex/config.toml.example`、hooks 示例和 harness audit，强调 sandbox、approval、manifest、预算、隐私和外部写入控制。
- Git：本模板是独立子仓库，只提交模板自身，不推送远程。

## 八个提交

1. `docs: add research os implementation plan`
2. `chore: scaffold research os template`
3. `feat: add research object schemas`
4. `feat: add research os orchestration skills`
5. `feat: add audit and export harness`
6. `feat: add static research dashboard`
7. `feat: add paper and review skill suite`
8. `test: validate research os template`

每次提交后必须重读 `PLAN/05_IMPLEMENTATION_CHECKLIST.md` 和 `PLAN/06_GAP_AUDIT.md`，确认下一步。

## 核心产物

- 项目模板目录骨架。
- 可安装的多级 skill 套件。
- 研究对象 schema 与模板。
- Codex harness 文件、审计、隐私扫描、资源守护、公开导出脚本。
- 静态研究仪表盘。
- 可选 LaTeX 论文、视觉表达、润色、事实校验、review/rebuttal 工作流。

## 不做

- 不自动投稿。
- 不自动上传公开平台。
- 不把当前具体研究项目改造成模板。
- 不默认任何模型、provider、数据集、baseline、预算金额或实验范式。
- 不承诺规避 AI 检测器；“去 AI 化”只表示去模板腔、空泛句和不自然结构。

## v2 依据

- OpenAI Codex 文档：AGENTS.md、Skills、Hooks、Sandbox、MCP。
- 自动科研参考：Agent Laboratory、AI co-scientist、AI Scientist-v2、agent 成本研究。
- 设计原则：阶段化、人类反馈、证据链、实验经理、成本/资源控制、实时证据刷新。
