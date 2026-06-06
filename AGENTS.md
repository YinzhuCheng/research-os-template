# Codex Research OS 模板规则

## 研究中立性

- 不默认任何研究方向。不要把项目默认成 LLM、机器学习、软件工程、数据集实验、论文或投稿任务。
- 入口材料不足时，生成对齐问题和待决策项，不擅自补默认模型、provider、baseline、dataset、样本量或预算。
- `feasibility_probe` 表示最小可行性验证，预算和工具必须来自研究者输入或确认后的决策记录。

## 语言与产物

- 默认 `zh-first`：计划、实验记录、分析、内部审计和 dashboard 使用中文。
- 只有 `dissemination.paper_enabled: true` 或研究者明确指定论文/投稿目标时，才进入论文写作、LaTeX、视觉和 review/rebuttal 流程。
- 未指定论文目标时，默认产物是研究简报、实验/验证报告、审计包、复现包或决策备忘。

## 控制与审计

- 执行前先读取 `CONTROL/work_order.yaml`、`CONTROL/phase_gate.yaml` 和 `config/research_project.yaml`。
- 只在 work order 的 `allowed_paths` 内写入；禁止路径必须视为硬边界。
- 每次实质运行后写入 `PROVENANCE/run_manifest.jsonl`，资源消耗写入 `PROVENANCE/resource_ledger.jsonl`。
- 预算、真实资源调用、凭据使用、外部写入、公开导出和投稿必须人工确认。
- 不自动清理 build、cache、log、raw output、validation report 或中间实验产物。

## 隐私与凭据

- `PUBLIC/` 只放可公开或已脱敏内容。
- `PRIVATE/` 默认不进入 git，原始对话、敏感数据和私有审计留在这里。
- 真实 API key、云账号密码、SSH 私钥、cookie、authorization header 不得写入仓库任何文件。
- 需要资源凭据时，只记录环境变量名、secret store 路径、IAM 角色名或短期凭据获取方式；真实值由运行环境提供。

## 实时证据

- 对时效性信息必须联网刷新并记录来源：文献状态、工具/API、价格、会议规则、数据许可、法律/伦理要求和外部资源可用性。
- 如果不能联网，必须把相关 claim 标成 `unverified` 或 `freshness_risk: high`。

## Git

- 本目录是独立 git 仓库。只提交模板自身，不推送远程。
- 不回滚用户或其他进程产生的无关改动。
- 提交前运行相关验证脚本，并在最终说明中报告未能运行的检查。
