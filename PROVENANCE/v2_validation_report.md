# Research OS v2 验证报告

验证日期：2026-06-06

## 通过项

- 研究中立性：通过 `check_research_neutrality.ps1`，覆盖 LLM 方法、湿实验机制、社会科学访谈、理论/综述四类 dry-run 输入；未默认模型、provider、budget、论文或投稿目标。
- Harness：通过 `check_harness.ps1 -PythonPath <bundled-python>`，检查 `AGENTS.md`、`.codex/config.toml.example`、hooks、work order、phase gate、manifest、resource ledger、secrets README，并验证 `git push` 样例被 PreToolUse hook 阻断。
- Resource guard：通过 `check_resource_guard.ps1`，确认 `resource_budget` 和 `resource_ledger.jsonl` 存在并覆盖多资源类别。
- Live evidence：通过 `check_live_evidence.ps1`，确认实时证据快照记录 URL、访问日期、风险等级和影响对象。
- 回归：schema、15 个 skill、隐私扫描、dashboard 静态检查、LaTeX 强制静态检查、公开导出均通过。

## 关键结论

- `pilot` 已被替换为 `research-os-feasibility-probe`，不再固定 100 元，也不限定 LLM、机器学习或软件实验。
- 预算改为研究者定义的 `resource_budget`，支持时间、算力、云、实验耗材、API、模型、人工、仪器和其他资源。
- 论文链路为可选传播目标；默认不生成论文、LaTeX 投稿包或 review/rebuttal。
- 凭据方案只允许记录环境变量名、secret store 路径、IAM 角色或短期凭据流程；真实密钥不得落盘。

## 残余风险

- hooks 是模板策略样例，只有研究者启用 `.codex/config.toml.example` 后才在 Codex 运行期生效。
- resource guard 不能替代云平台账单硬上限，真实云预算仍需在云厂商侧设置。
- Browser 控制工具本轮未暴露，dashboard 未做截图级 QA。
