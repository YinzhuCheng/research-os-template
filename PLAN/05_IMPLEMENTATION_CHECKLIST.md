# 实施检查清单

## Commit 1: 计划文档

- [x] 创建 `research-os-template/`。
- [x] 初始化独立 git 仓库。
- [x] 写入 `PLAN/` 文档。
- [x] 提交 `docs: add research os implementation plan`。

## Commit 2: 目录骨架

- [x] 创建 `PUBLIC/`、`PRIVATE/`、`CONTROL/`、`PROVENANCE/`、`config/`、`skills/`、`scripts/`、`templates/`。
- [x] 创建 `.gitignore`，忽略 `PRIVATE/**`，保留 `PRIVATE/README.md` 和 `.gitkeep`。
- [x] 写入隐私边界说明和基础配置。

## Commit 3: Schema 与模板

- [x] 实现 `research_project.yaml`。
- [x] 实现 work order、run manifest、claim-evidence、research brief 模板。
- [x] 写入样例对象。

## Commit 4: 入口、初始化、对齐 skill

- [x] 创建 orchestrator/init/alignment skill。
- [x] 每个 skill 含 `SKILL.md`、`references/`、必要 `assets/`。
- [x] 创建安装脚本。

## Commit 5: Harness 与审计脚本

- [x] 实现 schema 校验。
- [x] 实现隐私扫描。
- [x] 实现公开导出。
- [x] 实现 manifest/hash 工具。

## Commit 6: 静态仪表盘

- [x] 创建 `PUBLIC/index.html`。
- [x] 渲染 Markdown 和 JSON。
- [x] 显示阶段、claim、实验、结果、审计状态。

## Commit 7: 论文与 review skill

- [x] 创建 paper/visual/polish/review/export skill。
- [x] 增加 LaTeX、BibTeX、图表、附录模板。
- [x] 增加 review/rebuttal 模板。

## Commit 8: 验证与补缺

- [x] 运行全部脚本验证。
- [x] 运行 skill frontmatter 校验。
- [x] 运行隐私扫描测试。
- [x] 运行 dashboard 静态检查。
- [x] 更新最终审计说明。

## Commit 9: Research OS v2 研究无关性与 Codex Harness

- [x] 移除固定 `model_budget: 100`、`target_venue`、默认 LaTeX/投稿目标等方向绑定。
- [x] 将预算改为研究者入口定义的 `resource_budget`，覆盖时间、算力、云、实验耗材、API、模型、人工、仪器等资源。
- [x] 将 pilot 改为 `research-os-feasibility-probe`，不限定 LLM/ML/软件/数据集研究。
- [x] 将论文链路改为可选，仅在 `dissemination` 明确启用时运行。
- [x] 新增根 `AGENTS.md`、`.codex/config.toml.example`、hooks 示例和 harness requirements。
- [x] 新增 `research-os-harness-audit`、`research-os-resource-guard`、`research-os-live-evidence-refresh` skill。
- [x] 增加 `PRIVATE/secrets/README.md`，只允许凭据占位、环境变量名和 secret store 路径。
- [x] 更新 dashboard，显示 research type、feasibility、resource guard、live evidence、harness audit。
- [x] 运行 v2 通用性、harness、resource guard、live evidence、隐私和回归验证。
- [x] 更新 v2 最终审计说明。
- [x] 提交 `feat: add research neutral harness v2`。

## Commit 10: Research OS v3 治理授权

- [x] 将当前本地历史 bootstrap 到远端 `main`。
- [x] 创建并推送 `codex/research-os-v3` 分支。
- [x] 将 work order 更新为 `WO-0002`，授权 v3 文档、skill、adapter、schema 和脚本改动。
- [x] 刷新 live evidence 与 claim-evidence，补充自动科研和 Codex harness 依据。
- [x] 记录 v3 governance run manifest 和 resource ledger。
- [x] 提交 `chore: authorize research os v3 documentation work`。

## Commit 11: Human-in-loop 文档站

- [x] 新增 `docs/start-here.html`，面向一般研究者和 Codex 新手。
- [x] 新增 `docs/technical-report.html`，面向后续 agent 和维护者。
- [x] 新增 `docs/README.md`、`docs/doc_map.yaml`、`docs/PROJECT_SUMMARY.md`、`docs/PROJECT_LOG.md` 和 `docs/ASSET_SOURCES.md`。
- [x] 更新根 `README.md` 与 `PUBLIC/index.html` 导航。
- [x] 提交 `docs: add human loop research os guide`。

## Commit 12: Skill 与开源组件集成层

- [x] 新增 `.agents/skills/` 仓库级 skill 镜像。
- [x] 新增 skill 镜像同步/检查脚本。
- [x] 新增 `research-os-doc-site`、`research-os-integration-scout`、`research-os-experiment-manager`、`research-os-replay-eval-harness`。
- [x] 新增 `docs/integrations/components.yaml` 和 adapter 模板。
- [x] 提交 `feat: add auto research skill and integration layer`。

## Commit 13: v3 harness 验证

- [x] 新增 doc map、harness run、integration component schema。
- [x] 新增 HTML、链接、integration、skill mirror 检查脚本。
- [x] 运行 schema、skill、harness、dashboard、privacy、HTML、link、integration、skill mirror 验证。
- [x] 完成浏览器 QA。
- [x] 提交 `test: validate research os v3 governance`。
- [x] 推送分支并创建 draft PR：[PR #1](https://github.com/YinzhuCheng/research-os-template/pull/1)。

## Commit 14: Research OS v3.1 五大领域深度研究范式

- [x] 新增 `domain_profiles/`，覆盖基础数学、应用数学、机器学习、计算机科学和统计学。
- [x] 新增五个领域 skill：`research-os-math-discovery`、`research-os-applied-math-modeling`、`research-os-ml-research-protocol`、`research-os-cs-research-artifact`、`research-os-statistical-inference`。
- [x] 新增 `templates/domain/` 领域产物模板和 `domain_profile` / `agent_capability` schema。
- [x] 新增 `docs/domain-modes.html`，并接入快速上手、技术报告、dashboard 和 doc map。
- [x] 新增领域 profile、agent capability、domain templates 和 router 检查脚本。
- [x] 运行 v3.1 全量验证并提交推送。
