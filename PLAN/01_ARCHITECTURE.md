# 架构设计

## 项目边界

`research-os-template/` 是一个可复制模板仓库。用它初始化新研究项目时，模板应保留高可控、可追踪、可审计的 harness engineer 特征。

## 目录职责

- `PUBLIC/`：可上传内容，包含研究简报、公开文献索引、脱敏结果、论文、图表、仪表盘。
- `PRIVATE/`：原始对话、敏感数据、原始模型调用、私有审计日志、密钥占位说明。默认不进 git。
- `CONTROL/`：阶段闸门、work order、人工确认、决策记录。
- `PROVENANCE/`：来源、hash、成本、运行 manifest、公开可审计摘要。
- `config/`：项目配置和 schema 约束。
- `skills/`：入口 skill 与子 skill。
- `scripts/`：确定性工具脚本。
- `templates/`：Markdown、YAML、LaTeX、BibTeX、review/rebuttal 模板。
- `PLAN/`：模板自身实施计划和缺口审计。

## 研究对象 ID

- `RQ-*`：研究问题。
- `HYP-*`：可证伪假设。
- `CLAIM-*`：论文论断。
- `EXP-*`：实验协议。
- `RUN-*`：运行记录。
- `RES-*`：结果。
- `DEC-*`：决策。
- `REV-*`：审稿问题。

## 生命周期

1. 输入对话、草稿或 demo。
2. 生成 research brief 和需求对齐清单。
3. 建立假设注册表和文献证据矩阵。
4. 先写实验协议，再生成 work order。
5. Codex 执行并写入 manifest。
6. 汇总结果、失败案例和威胁分析。
7. 生成英文 LaTeX 论文与附录。
8. 自 review、rebuttal、修稿循环。
9. 公开导出脱敏包。

## 阶段闸门

- `low`：阶段切换、预算超限、外部写入、公开导出、投稿前确认。
- `medium`：主要实验协议、核心 claim、论文结构、重要图表前确认。
- `high`：每个 mutating work order 前确认。
