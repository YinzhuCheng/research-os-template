# Skills

`skills/` is the versioned source of Research OS repo skills. `.agents/skills/` is the repo-scoped Codex discovery mirror.

Included skills:

- `research-os-orchestrator`
- `research-os-copilot`
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

Install or mirror:

```powershell
.\scripts\install_skills.ps1
.\scripts\sync_skill_mirror.ps1
.\scripts\check_skill_mirror.ps1
```

## Main-route Governance

A main-route skill must not be a loose prompt or isolated tool. Before it enters `research-os-orchestrator`, it needs:

- kernel binding or explicit kernel exemption;
- schema or template support;
- validator coverage;
- documentation or `docs/doc_map.yaml` presence;
- `.agents/skills/` mirror consistency.

`research-os-copilot` is governed by the copilot schemas, templates, validators, browser page, plugin bridge, and research-kernel handoff.
