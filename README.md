# Codex Research OS Template

这是一个通用科研项目模板，用于把对话、研究计划草稿或实验 demo 转成可执行、可审计、可写论文的 Codex 研究仓库。

## 默认行为

- 内部研究过程默认中文。
- 正式论文默认英文 LaTeX。
- 入口允许设置 `language_mode: en-only`。
- 默认低介入，但阶段切换必须确认。
- `PUBLIC/` 可公开，`PRIVATE/` 默认不进 git。

## 主要入口

- 计划：[PLAN/00_MASTER_PLAN.md](PLAN/00_MASTER_PLAN.md)
- 公开区：[PUBLIC/README.md](PUBLIC/README.md)
- 私有区：[PRIVATE/README.md](PRIVATE/README.md)
- 控制区：[CONTROL/README.md](CONTROL/README.md)
- 来源与审计：[PROVENANCE/README.md](PROVENANCE/README.md)
- Skill 套件：[skills/README.md](skills/README.md)

## 使用原则

先写研究协议，再执行实验；先绑定 claim 和 evidence，再写论文；公开导出前必须通过隐私扫描。
