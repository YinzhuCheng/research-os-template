# Research OS v3.9 三阶段、循环验收与最终产物工作流计划

## 执行规则

- 每个大步骤开始前必须重读本文件、`CONTROL/work_order.yaml`、`CONTROL/phase_gate.yaml`、`config/research_project.yaml`。
- 每个大步骤结束前必须更新本文件的步骤状态，按需要更新 `PLAN/05_IMPLEMENTATION_CHECKLIST.md` 和 `PLAN/06_GAP_AUDIT.md`。
- 每个大步骤必须运行相关验证，检查 `git status --short`，确认不包含 `PRIVATE/`、真实密钥、授权头或无关文件。
- 每个大步骤完成后创建一次 git commit 并 push 当前分支。
- 如果遇到真实资源、凭证、外部平台写回、公开提交、预算超限、`PRIVATE/` 读取/提交需求，必须停止并要求人工确认。

## 目标

把用户视角重构为三阶段：

1. 初始化阶段
2. 半自动循环研究阶段
3. 最终产物阶段

底层 Research OS 细分阶段保留治理能力，但允许合并和删除冗余阶段，形成职责更清晰的内部状态机。第二阶段固定循环为：

`用户验收上阶段产物 -> 系统提出下一阶段行动规划和对齐问题 -> 用户选择或自然语言回复 -> 系统执行并产出下一阶段结果`

未验收通过时不得进入下一步，只能按用户反馈继续修订当前阶段产物。

所有用户选项控件都必须提供推荐选项、多个默认选项、自然语言 Other/free-form 输入。

## 内部阶段重整

- `initialization_intake`: 合并 `material_intake`、`targeted_questions`、`initialization`。
- `loop_acceptance_gate`: 用户验收上一阶段产物；未通过则阻塞进入下一步。
- `loop_plan_alignment`: 系统提出下一阶段行动规划、推荐选项和对齐问题。
- `loop_user_decision`: 记录用户选择和自然语言补充，更新 work order/phase gate。
- `loop_execute_analyze`: 合并 research kernel、domain routing、feasibility/evidence、execution harness、analysis；保留 candidate/evaluator/resource/audit 子对象。
- `final_product_selection`: 用户选择一个或多个最终产物类型。
- `final_product_production`: 按 paper/report/software track 执行产物生成和迭代。
- `export_release_gate`: 公开导出、提交、外部写入前的人类确认。

## 步骤状态

| Step | 内容 | 状态 | 验证 | Commit/Push |
| --- | --- | --- | --- | --- |
| 1 | 落盘计划与 v3.9 工作单 | completed | passed: `scripts/validate_schemas.ps1`; `scripts/check_harness.ps1` | pushed: `78bc54b` |
| 2 | 流程契约与 schema | completed | passed: schema, strict instance, flow checks | ready for step commit |
| 3 | 最终产物 workflows 与 skills | pending | skill/mirror/integration checks | pending |
| 4 | git-backed 存档功能 | pending | archive tests/privacy checks | pending |
| 5 | UI/UX 重整 | pending | dashboard/copilot/html/link checks | pending |
| 6 | 文档、dashboard 数据与检查脚本 | pending | docs/governance checks | pending |
| 7 | 完整验证与浏览器 QA | pending | full validation and browser QA | pending |

## 产物轨道

- Paper track: 目标期刊/会议、模板、可选同类论文、英文 LaTeX/PDF、review/rebuttal 迭代。
- Report track: 强调研究过程、初始数据、负结果、复现细节；支持 HTML、LaTeX/PDF、PPT 输出。
- Software track: 默认接近正式产品，稳定、规范、美观、用户友好；用户可用自然语言调整目标。

## 存档要求

- UI 收集描述，显示当前阶段和 git 状态。
- 后端创建 git snapshot commit，并写入 `PROVENANCE/archive_index.jsonl`。
- 生成脱敏公开索引 `PUBLIC/archive_index.json`。
- 禁止包含 `PRIVATE/`、真实密钥、authorization headers、cookies、tokens。

## 开源资源策略

只登记和参考开源资源，不 vendoring、不安装、不执行第三方系统，除非后续工作单明确授权。候选资源包括 Quarto、Typst、Marp、MkDocs Material、Lucide、Hatch、PyInstaller、FastAPI。
