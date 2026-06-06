# 架构设计

## 项目边界

`research-os-template/` 是一个可复制模板仓库。用它初始化新研究项目时，模板应保留高可控、可追踪、可审计的 harness engineer 特征，并保持研究方向无关。

## 目录职责

- `PUBLIC/`：可上传内容，包含研究简报、公开文献索引、脱敏结果、论文、图表、仪表盘。
- `PRIVATE/`：原始对话、敏感数据、原始模型/API 调用、私有审计日志、凭据占位说明。真实密钥不得落盘，默认不进 git。
- `CONTROL/`：阶段闸门、work order、人工确认、决策记录。
- `PROVENANCE/`：来源、hash、资源消耗、运行 manifest、实时证据刷新、公开可审计摘要。
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
- `FEAS-*`：最小可行性验证。
- `BUD-*`：资源预算或资源消耗记录。
- `EVID-*`：实时证据刷新项。

## 生命周期

1. 输入对话、草稿或 demo。
2. 生成 research brief 和需求对齐清单。
3. 明确研究类型、验证对象、资源预算、传播目标和隐私边界。
4. 建立假设注册表、证据矩阵和实时证据刷新任务。
5. 定义最小可行性验证，写入成功、失败和不确定结果三种调整路径。
6. 先写协议和 work order，再由 resource guard 与 harness audit 检查。
7. Codex 执行并写入 manifest、资源账本、hash 和审计摘要。
8. 汇总结果、失败案例、统计/定性分析和威胁分析。
9. 如果研究者指定论文/投稿目标，再生成英文 LaTeX 论文、附录、自 review 和 rebuttal。
10. 公开导出脱敏包。

## 阶段闸门

- `low`：阶段切换、预算超限、外部写入、公开导出、投稿前确认。
- `medium`：主要实验协议、核心 claim、论文结构、重要图表前确认。
- `high`：每个 mutating work order 前确认。

## Codex Harness

- `AGENTS.md` 提供仓库级指令，靠近研究项目根目录，约束语言、隐私、预算、外部写入和审计。
- `.codex/config.toml.example` 推荐 `workspace-write` 与 `on-request`，避免默认 `danger-full-access` 和 `never`。
- Hooks 示例覆盖 `PreToolUse`、`PostToolUse`、`Stop`：执行前阻断高风险命令，执行后提醒补 manifest，停止前检查未提交变更和审计缺口。
- MCP 配置只记录环境变量名和工具策略，不保存 bearer token 或账号密码。
