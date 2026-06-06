# Research OS Harness Requirements

本文件描述模板期望的 Codex 控制面。它不是当前会话的强制配置，复制模板初始化新项目后再由研究者决定是否启用。

## 最低要求

- 项目根目录保留 `AGENTS.md`。
- 推荐权限为 `sandbox_mode = "workspace-write"` 与 `approval_policy = "on-request"`。
- 外部写入、公开导出、真实资源调用、凭据使用、预算超限和投稿必须人工确认。
- 使用 hook 时，先本地审查脚本，再复制 `.codex/config.toml.example` 为 `.codex/config.toml`。

## Hook 覆盖

- `PreToolUse`：拒绝明显危险命令、外部写回、凭据泄漏和未确认的真实资源调用。
- `PostToolUse`：提醒记录 manifest、资源 ledger、隐私扫描和失败状态。
- `Stop`：提醒检查 `git status`、缺口审计和下一步阶段闸门。

## MCP 与实时信息

MCP 用于连接文献库、内部文档、浏览器、云账单或项目管理系统。任何 MCP 服务器都应在说明中写清楚权限、速率限制、成本和数据边界。

## Skill 发现

- `skills/` 是模板内权威 skill 源。
- `.agents/skills/` 是 Codex 仓库级发现镜像，供支持 Agent Skills 标准的客户端自动发现。
- 更新 `skills/` 后运行 `scripts/sync_skill_mirror.ps1` 和 `scripts/check_skill_mirror.ps1`。
- 从外部 skill 或插件借鉴内容前，先在 `docs/integrations/components.yaml` 记录来源、许可证和风险。
