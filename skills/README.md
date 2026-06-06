# skills 区

此目录保存模板内版本化的 Codex skill 套件。

已包含：

- `research-os-orchestrator`
- `research-os-research-kernel`
- `research-os-init`
- `research-os-alignment`
- `research-os-execution-harness`
- `research-os-feasibility-probe`
- `research-os-harness-audit`
- `research-os-doc-site`
- `research-os-integration-scout`
- `research-os-experiment-manager`
- `research-os-replay-eval-harness`
- `research-os-resource-guard`
- `research-os-live-evidence-refresh`
- `research-os-evidence`
- `research-os-analysis`
- `research-os-paper-authoring`
- `research-os-visual-communication`
- `research-os-polish-factcheck`
- `research-os-review-rebuttal`
- `research-os-public-export`
- `research-os-math-discovery`
- `research-os-applied-math-modeling`
- `research-os-ml-research-protocol`
- `research-os-cs-research-artifact`
- `research-os-statistical-inference`

安装方式：

```powershell
.\scripts\install_skills.ps1
```

默认复制到 `~/.codex/skills`，但模板内版本仍是权威来源。

仓库级 Codex 自动发现镜像位于 `.agents/skills/`。更新 `skills/` 后运行：

```powershell
.\scripts\sync_skill_mirror.ps1
.\scripts\check_skill_mirror.ps1
```

## v3.2 skill 治理

主路由 skill 不能只是一个松散工具。进入 `research-os-orchestrator` 主链路前，必须满足：

- 在 `skills/README.md`、`docs/doc_map.yaml` 或技术报告中可发现。
- 有 schema、template、validator 或明确 kernel exemption。
- 能通过 `.agents/skills/` 镜像一致性检查。
- 对研究对象必须说明如何进入 `research-os-research-kernel` 的 candidate、evaluator、belief、trace、negative result 和 human gate。
