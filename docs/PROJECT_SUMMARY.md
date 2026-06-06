# Project Summary

Research OS v3 是一个通用的 human-in-loop auto researcher 仓库模板。它的默认目标不是替研究者自动完成某个具体学科任务，而是把研究想法、草稿、demo 或实验过程组织成可执行、可审计、可复现、可交接的工作空间。

## 当前状态

- 当前阶段：`research-os-v3`
- 控制文件：`CONTROL/work_order.yaml` 已更新为 `WO-0002`
- 默认语言：`zh-first`
- 默认边界：研究无关、低介入但阶段闸门、真实资源调用和外部写入需人工确认
- 主要产物：普通研究者上手文档、技术路线 HTML、skill 镜像、开源组件 registry、harness 检查脚本

## 核心原则

- 先对齐研究者意图，再执行实验或报告生成。
- 先记录预算、停止条件和允许路径，再进行 mutating 工作。
- 先刷新时效性证据，再把外部结论写进公开文档。
- 默认不 vendoring 大段第三方源码，优先记录来源、许可证、安装方式、环境变量名和 adapter 产物映射。
- 原始敏感材料、密钥、cookie、authorization header 和私有审计不得进入 `PUBLIC/` 或 git 历史。

## 重要入口

- 新手入口：`docs/start-here.html`
- 技术报告：`docs/technical-report.html`
- 文档地图：`docs/doc_map.yaml`
- 开源组件 registry：`docs/integrations/components.yaml`
- 仓库规则：`AGENTS.md`
- Codex harness 示例：`.codex/requirements.md`
