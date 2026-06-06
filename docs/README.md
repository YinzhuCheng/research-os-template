# 文档中心

Research OS v3 的文档分成三层：

- 入门层：[start-here.html](start-here.html) 面向一般研究者和 Codex 新手，解释如何从一个研究想法进入可审计项目。
- 技术层：[technical-report.html](technical-report.html) 面向后续 agent、维护者和高级使用者，说明控制面、数据流、skill、harness 和集成方式。
- 治理层：`PROJECT_SUMMARY.md`、`PROJECT_LOG.md`、`doc_map.yaml` 和 `integrations/components.yaml` 记录仓库状态、变更历史、文档导航和外部组件来源。

## 快速入口

- 项目首页：[../README.md](../README.md)
- 控制平面：[../CONTROL/work_order.yaml](../CONTROL/work_order.yaml)
- 阶段闸门：[../CONTROL/phase_gate.yaml](../CONTROL/phase_gate.yaml)
- 公开 dashboard：[../PUBLIC/index.html](../PUBLIC/index.html)
- Skill 套件：[../skills/README.md](../skills/README.md)
- 来源证据：[../PROVENANCE/live_evidence_snapshot.yaml](../PROVENANCE/live_evidence_snapshot.yaml)

## 文档维护规则

- 对普通研究者可见的路线写进 `start-here.html`。
- 对 agent、harness、schema、skill、adapter 的细节写进 `technical-report.html`。
- 新增外部组件、图标、截图或视觉资产时，更新 `ASSET_SOURCES.md`。
- 新增或移动关键文档时，更新 `doc_map.yaml` 和 `PUBLIC/dashboard_data.json`。
