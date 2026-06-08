import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, ClipboardCheck, FileStack, FolderOpen, Upload } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "./api";
import { ApprovalPanel } from "./components/ApprovalPanel";
import { ArchivePanel } from "./components/ArchivePanel";
import { ChoicePrompt } from "./components/ChoicePrompt";
import { FinalProductModal } from "./components/FinalProductModal";
import { PaperWorkflowPanel } from "./components/PaperWorkflowPanel";
import { PhaseBar } from "./components/PhaseBar";
import { ProjectCenter } from "./components/ProjectCenter";
import { RuntimePanel } from "./components/RuntimePanel";
import { internalPhaseLabel, macroPhaseLabel, normalizeMacroPhase } from "./labels";
import { useAppStore } from "./store";
import { selectMaterialDirectory } from "./tauriDialog";
import type { MaterialManifestSummary } from "./types";

const roleLabels: Record<string, string> = {
  manuscript_draft: "论文草稿",
  bibliography: "参考文献",
  venue_template: "期刊模板",
  venue_instruction: "投稿要求",
  example_paper: "示例论文",
  pdf_document: "PDF 材料",
  slide_deck: "PPT/演示",
  proof_audit: "证明审计",
  review_record: "审稿/反驳记录",
  note: "笔记",
  code_or_notebook: "代码/Notebook",
  data_or_structured_record: "结构化数据",
  figure_or_screenshot: "图片/截图",
  other_material: "其他材料",
};

function MaterialManifestCard({ manifest }: { manifest?: MaterialManifestSummary | null }) {
  if (!manifest) {
    return (
      <div className="empty-state compact-empty">
        尚未导入完整材料文件夹。先导入包含草稿、模板、示例论文和笔记的文件夹，Research OS 才能基于全量上下文生成计划。
      </div>
    );
  }
  const roleEntries = Object.entries(manifest.role_counts ?? {}).sort(([a], [b]) => a.localeCompare(b));
  return (
    <div className="material-summary" aria-label="材料包概览">
      <div className="metric-row">
        <span>材料包</span>
        <strong>{manifest.source_name ?? "未命名材料包"}</strong>
      </div>
      <div className="metric-row">
        <span>已导入文件</span>
        <strong>{manifest.file_count ?? 0} 个</strong>
      </div>
      <div className="metric-row">
        <span>排除文件</span>
        <strong>{manifest.excluded_count ?? 0} 个</strong>
      </div>
      {roleEntries.length > 0 ? (
        <div className="role-grid">
          {roleEntries.map(([role, count]) => (
            <span className="role-chip" key={role}>
              {roleLabels[role] ?? role}: {count}
            </span>
          ))}
        </div>
      ) : null}
      {(manifest.warnings ?? []).length > 0 ? (
        <div className="notice warning">
          <AlertTriangle size={16} aria-hidden="true" />
          <div>
            <strong>需要确认的材料问题</strong>
            <ul>
              {manifest.warnings?.map((warning) => <li key={warning}>{warning}</li>)}
            </ul>
          </div>
        </div>
      ) : null}
    </div>
  );
}

function Workspace() {
  const queryClient = useQueryClient();
  const project = useAppStore((store) => store.project);
  const [material, setMaterial] = useState("");
  const [materialDirectory, setMaterialDirectory] = useState("");
  const [dialogNotice, setDialogNotice] = useState("");
  const [finalOpen, setFinalOpen] = useState(false);
  const state = useQuery({ queryKey: ["state"], queryFn: api.state, refetchInterval: 5000 });
  const submitIntake = useMutation({
    mutationFn: () => api.submitIntake(material),
    onSuccess: () => {
      setMaterial("");
      queryClient.invalidateQueries({ queryKey: ["state"] });
    },
  });
  const importDirectory = useMutation({
    mutationFn: () => api.importDirectory(materialDirectory, "PRIVATE/intake/source_materials"),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["state"] });
    },
  });
  const saveChoice = useMutation({
    mutationFn: ({ promptId, optionId, freeForm }: { promptId: string; optionId: string; freeForm: string }) =>
      api.saveChoiceResponse(promptId, optionId, freeForm),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["state"] }),
  });
  const finalProducts = useMutation({
    mutationFn: ({ tracks, freeForm }: { tracks: string[]; freeForm: string }) => api.finalProducts(tracks, freeForm),
    onSuccess: () => {
      setFinalOpen(false);
      queryClient.invalidateQueries({ queryKey: ["state"] });
    },
  });

  async function chooseMaterialDirectory() {
    setDialogNotice("");
    try {
      const selected = await selectMaterialDirectory();
      if (selected) setMaterialDirectory(selected);
    } catch {
      setDialogNotice("当前不是 Tauri 桌面运行环境，无法打开系统目录选择器；请手动输入材料文件夹路径。");
    }
  }

  const activePhase = normalizeMacroPhase(project?.current_macro_phase);
  const activePhaseLabel = macroPhaseLabel(project?.current_macro_phase);
  const internalLabel = internalPhaseLabel(project?.current_phase);
  const prompts = state.data?.choice_prompts ?? [];

  return (
    <main className="workspace">
      <header className="workspace-header">
        <div className="header-copy">
          <p className="eyebrow">当前项目</p>
          <h1>{project?.name}</h1>
          <p className="path-text">{project?.project_root}</p>
        </div>
        <div className="header-actions">
          <span className="status-pill">阶段：{activePhaseLabel}</span>
          <span className="status-pill subtle">内部：{internalLabel}</span>
          <button className="primary-action" type="button" onClick={() => setFinalOpen(true)}>
            <FileStack size={16} aria-hidden="true" />
            进入最终产物阶段
          </button>
        </div>
      </header>

      <PhaseBar active={activePhase} />

      <section className="current-action" aria-label="当前研究行动">
        <strong>当前任务：把整份神经网络论文材料包作为初始化输入。</strong>
        <span>先导入文件夹、生成研究计划、完成验收门和来源核查，再进入最终论文产物；不要把旧草稿直接当成最终稿。</span>
      </section>

      {state.error ? (
        <div className="notice danger" role="alert">
          <AlertTriangle size={16} aria-hidden="true" />
          <span>无法读取 Research OS 状态：{state.error.message}</span>
        </div>
      ) : null}

      <div className="workspace-grid">
        <section className="panel primary-panel">
          <div className="section-heading">
            <Upload size={18} aria-hidden="true" />
            <div>
              <h2>材料与目标</h2>
              <p>导入完整文件夹，再补充自然语言目标。原始文件进入项目私有 intake；公开状态只显示摘要和警告。</p>
            </div>
          </div>

          <label className="field">
            <span>研究材料文件夹</span>
            <input
              value={materialDirectory}
              onChange={(event) => setMaterialDirectory(event.target.value)}
              placeholder="D:/Google One/research-os-template/neural network"
            />
          </label>
          <div className="inline-actions split-actions">
            <button className="secondary-action" type="button" onClick={chooseMaterialDirectory}>
              <FolderOpen size={16} aria-hidden="true" />
              选择文件夹
            </button>
            <button
              className="primary-action"
              type="button"
              onClick={() => importDirectory.mutate()}
              disabled={!materialDirectory.trim() || importDirectory.isPending}
            >
              <Upload size={16} aria-hidden="true" />
              {importDirectory.isPending ? "正在导入" : "导入完整材料包"}
            </button>
          </div>
          {dialogNotice ? <p className="hint-text">{dialogNotice}</p> : null}
          {importDirectory.error ? <p className="error-text">{importDirectory.error.message}</p> : null}
          <MaterialManifestCard manifest={state.data?.material_manifest} />

          <label className="field">
            <span>研究目标、限制、期刊要求或自然语言补充</span>
            <textarea
              value={material}
              onChange={(event) => setMaterial(event.target.value)}
              rows={7}
              placeholder="例如：请把旧论文、PDF、PPT、投稿模板和示例论文都视为初始材料，先生成研究计划；所有引用和投稿规则必须联网核查。"
            />
          </label>
          <div className="inline-actions split-actions">
            <button className="primary-action" type="button" onClick={() => submitIntake.mutate()} disabled={!material.trim() || submitIntake.isPending}>
              <Upload size={16} aria-hidden="true" />
              {submitIntake.isPending ? "正在保存" : "保存目标并初始化"}
            </button>
            <span className="muted">保存后生成三个定向问题；不会绕过用户验收。</span>
          </div>
          {submitIntake.error ? <p className="error-text">{submitIntake.error.message}</p> : null}
        </section>

        <section className="panel">
          <div className="section-heading">
            <ClipboardCheck size={18} aria-hidden="true" />
            <div>
              <h2>验收与下一步</h2>
              <p>每轮先确认上一阶段产物，再回答 1-3 个高影响问题，最后交给 Codex 执行。</p>
            </div>
          </div>
          {state.isLoading ? <p className="muted">正在读取当前阶段问题...</p> : null}
          {!state.isLoading && prompts.length === 0 ? <p className="empty-state">当前没有待回答问题。导入材料或继续 Codex 执行后会在这里出现对齐问题。</p> : null}
          {prompts.slice(0, 3).map((prompt) => (
            <ChoicePrompt
              key={prompt.prompt_id}
              prompt={prompt}
              pending={saveChoice.isPending}
              onSubmit={({ optionId, freeForm }) => saveChoice.mutate({ promptId: prompt.prompt_id, optionId, freeForm })}
            />
          ))}
          {saveChoice.error ? <p className="error-text">{saveChoice.error.message}</p> : null}
        </section>

        <PaperWorkflowPanel workflow={state.data?.submission_workflow} />
        <RuntimePanel />
        <ApprovalPanel />
        <ArchivePanel />
      </div>

      <FinalProductModal
        open={finalOpen}
        onClose={() => setFinalOpen(false)}
        onSubmit={(tracks, freeForm) => finalProducts.mutate({ tracks, freeForm })}
        pending={finalProducts.isPending}
        error={finalProducts.error?.message}
      />
    </main>
  );
}

export default function App() {
  const setProject = useAppStore((store) => store.setProject);
  const project = useAppStore((store) => store.project);
  const current = useQuery({ queryKey: ["project"], queryFn: api.currentProject, retry: false });

  useEffect(() => {
    if (current.data?.project) {
      setProject(current.data.project);
    }
  }, [current.data?.project, setProject]);

  return project ? <Workspace /> : <ProjectCenter />;
}
