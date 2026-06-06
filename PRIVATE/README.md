# PRIVATE 区

此目录用于保存私有研究材料，默认被 `.gitignore` 排除。

典型内容：

- 原始 GPT/Codex 对话。
- 私有研究想法和未公开决策笔记。
- 原始模型请求、响应、实验日志。
- 敏感数据、授权受限数据、密钥占位说明。

规则：

- 不保存真实 API key、token、cookie 或 authorization header。
- 如需公开，先生成脱敏副本到 `PUBLIC/` 或 `PROVENANCE/`。
- Codex 不应自动删除本目录中的原始材料。
