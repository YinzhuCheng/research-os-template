# skills 区

此目录保存模板内版本化的 Codex skill 套件。

已包含：

- `research-os-orchestrator`
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
