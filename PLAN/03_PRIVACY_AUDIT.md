# 隐私与审计计划

## 隐私分区

- `PUBLIC/`：默认可上传。所有文件必须可公开或已脱敏。
- `PRIVATE/`：默认 `.gitignore`。保存原始对话、未脱敏数据、凭据占位、原始模型/API 响应和私有审计。
- `PROVENANCE/`：允许保存脱敏来源、hash、资源消耗、manifest、实时证据刷新。原始 payload 只能在 `PRIVATE/`。

## 禁止公开的内容

- API key、platform token、cookie、authorization header。
- 云账号密码、SSH 私钥、长期凭据、可直接登录的连接串。
- 未脱敏的用户对话、隐私数据、未授权数据集。
- 私有模型响应中的敏感字段。
- 未确认授权的图片、PDF、数据源。

## 审计要求

- 每个 work order 必须记录输入、输出、允许路径、禁止路径、资源预算、验收标准。
- 每次运行写入 `PROVENANCE/run_manifest.jsonl`。
- 资源消耗写入 `PROVENANCE/resource_ledger.jsonl`，覆盖 API、云、耗材、人工、仪器、模型等类别。
- 对时效性信息写入 `PROVENANCE/live_evidence_snapshot.yaml`，记录 URL、访问日期、可信等级和摘要。
- 公开导出前运行隐私扫描。
- 所有 AIGC 图像必须保存 prompt、模型、参数、原图、审核记录。

## 凭据方案

- `PRIVATE/secrets/README.md` 只保存环境变量名、secret store 路径、IAM 角色、短期凭据获取流程和最小权限说明。
- 真实值由操作系统环境、云 secret manager 或人工临时注入，不写入仓库文件。
- 使用凭据前必须有人工确认、资源上限和 manifest 记录；默认只读优先。

## 默认失败策略

扫描发现敏感信息时，公开导出失败并输出具体路径和命中规则。Codex 不应自动删除原始材料，只能提示修复或生成脱敏副本。
