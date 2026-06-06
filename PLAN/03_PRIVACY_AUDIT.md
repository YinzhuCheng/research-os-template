# 隐私与审计计划

## 隐私分区

- `PUBLIC/`：默认可上传。所有文件必须可公开或已脱敏。
- `PRIVATE/`：默认 `.gitignore`。保存原始对话、未脱敏数据、密钥占位、原始模型响应和私有审计。
- `PROVENANCE/`：允许保存脱敏来源、hash、成本、manifest。原始 payload 只能在 `PRIVATE/`。

## 禁止公开的内容

- API key、platform token、cookie、authorization header。
- 未脱敏的用户对话、隐私数据、未授权数据集。
- 私有模型响应中的敏感字段。
- 未确认授权的图片、PDF、数据源。

## 审计要求

- 每个 work order 必须记录输入、输出、允许路径、禁止路径、预算、验收标准。
- 每次运行写入 `PROVENANCE/run_manifest.jsonl`。
- 公开导出前运行隐私扫描。
- 所有 AIGC 图像必须保存 prompt、模型、参数、原图、审核记录。

## 默认失败策略

扫描发现敏感信息时，公开导出失败并输出具体路径和命中规则。Codex 不应自动删除原始材料，只能提示修复或生成脱敏副本。
