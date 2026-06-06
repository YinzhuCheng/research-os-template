# PRIVATE/secrets

DO_NOT_STORE_REAL_SECRETS

此目录只保存凭据使用说明和占位信息，不保存真实密钥。

允许记录：

- 环境变量名，例如 `OPENAI_API_KEY`、`AWS_PROFILE`。
- OS secret store、云 secret manager 或 vault 的路径。
- IAM 角色、服务账号名、SSH key 文件的外部路径说明。
- 短期凭据获取步骤和过期时间。

禁止记录：

- 真实 API key、token、cookie、authorization header。
- 云服务器账号密码、root 密码、SSH 私钥内容。
- 可直接登录或扣费的完整凭据。

使用原则：

- 优先只读权限、最小权限和短期凭据。
- 真实资源调用前必须确认预算和 work order。
- 使用后只在 `PROVENANCE/resource_ledger.jsonl` 中记录脱敏资源类型、金额或用量、状态和时间。
