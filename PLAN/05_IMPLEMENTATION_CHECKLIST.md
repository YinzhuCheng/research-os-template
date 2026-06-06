# 实施检查清单

## Commit 1: 计划文档

- [x] 创建 `research-os-template/`。
- [x] 初始化独立 git 仓库。
- [x] 写入 `PLAN/` 文档。
- [x] 提交 `docs: add research os implementation plan`。

## Commit 2: 目录骨架

- [ ] 创建 `PUBLIC/`、`PRIVATE/`、`CONTROL/`、`PROVENANCE/`、`config/`、`skills/`、`scripts/`、`templates/`。
- [ ] 创建 `.gitignore`，忽略 `PRIVATE/**`，保留 `PRIVATE/README.md` 和 `.gitkeep`。
- [ ] 写入隐私边界说明和基础配置。

## Commit 3: Schema 与模板

- [ ] 实现 `research_project.yaml`。
- [ ] 实现 work order、run manifest、claim-evidence、research brief 模板。
- [ ] 写入样例对象。

## Commit 4: 入口、初始化、对齐 skill

- [ ] 创建 orchestrator/init/alignment skill。
- [ ] 每个 skill 含 `SKILL.md`、`references/`、必要 `assets/`。
- [ ] 创建安装脚本。

## Commit 5: Harness 与审计脚本

- [ ] 实现 schema 校验。
- [ ] 实现隐私扫描。
- [ ] 实现公开导出。
- [ ] 实现 manifest/hash 工具。

## Commit 6: 静态仪表盘

- [ ] 创建 `PUBLIC/index.html`。
- [ ] 渲染 Markdown 和 JSON。
- [ ] 显示阶段、claim、实验、结果、审计状态。

## Commit 7: 论文与 review skill

- [ ] 创建 paper/visual/polish/review/export skill。
- [ ] 增加 LaTeX、BibTeX、图表、附录模板。
- [ ] 增加 review/rebuttal 模板。

## Commit 8: 验证与补缺

- [ ] 运行全部脚本验证。
- [ ] 运行 skill frontmatter 校验。
- [ ] 运行隐私扫描测试。
- [ ] 运行 dashboard 静态检查。
- [ ] 更新最终审计说明。
