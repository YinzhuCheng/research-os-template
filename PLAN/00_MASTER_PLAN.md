# Codex Research OS 实施总计划

## 目标

在本目录实现一个可复用的 Codex 科研项目模板。模板用于把 GPT 对话、研究计划草稿或简单实验 demo 规范成可执行、可审计、可写论文的研究仓库。

## 默认策略

- 语言：`zh-first`，计划、实验记录、分析和内部审计默认中文；正式论文按目标会议/期刊要求输出英文 LaTeX。
- 可选语言：入口允许设置 `en-only`，此时项目计划、审计、网页和论文均使用英文。
- 人类介入：默认 `low`，阶段内自动推进，阶段切换必须给决策者确认清单。
- 隐私：严格区分 `PUBLIC/` 和 `PRIVATE/`。公开导出只允许读取 `PUBLIC/` 和脱敏后的 `PROVENANCE/`。
- 论文：LaTeX 优先，强关注排版、配色、矢量图、图表多样性、附录和投稿包。
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
- 审计、隐私扫描、公开导出脚本。
- 静态研究仪表盘。
- LaTeX 论文、视觉表达、润色、事实校验、review/rebuttal 工作流。

## 不做

- 不自动投稿。
- 不自动上传公开平台。
- 不把当前具体研究项目改造成模板。
- 不承诺规避 AI 检测器；“去 AI 化”只表示去模板腔、空泛句和不自然结构。
