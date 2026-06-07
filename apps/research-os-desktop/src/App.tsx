import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, ClipboardCheck, FileStack, Upload } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "./api";
import { ApprovalPanel } from "./components/ApprovalPanel";
import { ArchivePanel } from "./components/ArchivePanel";
import { ChoicePrompt } from "./components/ChoicePrompt";
import { FinalProductModal } from "./components/FinalProductModal";
import { PhaseBar } from "./components/PhaseBar";
import { ProjectCenter } from "./components/ProjectCenter";
import { RuntimePanel } from "./components/RuntimePanel";
import { internalPhaseLabel, macroPhaseLabel, normalizeMacroPhase } from "./labels";
import { useAppStore } from "./store";

function Workspace() {
  const queryClient = useQueryClient();
  const project = useAppStore((store) => store.project);
  const [material, setMaterial] = useState("");
  const [finalOpen, setFinalOpen] = useState(false);
  const state = useQuery({ queryKey: ["state"], queryFn: api.state, refetchInterval: 5000 });
  const submitIntake = useMutation({
    mutationFn: () => api.submitIntake(material),
    onSuccess: () => {
      setMaterial("");
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
            进入最终产物
          </button>
        </div>
      </header>

      <PhaseBar active={activePhase} />

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
              <p>把研究想法、计划草稿、链接或 demo 说明交给项目沙箱。原始内容只进入项目内私有 intake。</p>
            </div>
          </div>
          <label className="field">
            <span>研究材料、目标、草稿或链接</span>
            <textarea
              value={material}
              onChange={(event) => setMaterial(event.target.value)}
              rows={8}
              placeholder="粘贴研究计划、ChatGPT 链接、论文线索、软件 demo 说明或实验想法。"
            />
          </label>
          <div className="inline-actions split-actions">
            <button className="primary-action" type="button" onClick={() => submitIntake.mutate()} disabled={!material.trim() || submitIntake.isPending}>
              <Upload size={16} aria-hidden="true" />
              {submitIntake.isPending ? "正在保存" : "保存材料并初始化"}
            </button>
            <span className="muted">保存后会生成对齐问题，不会绕过用户验收。</span>
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
          {!state.isLoading && prompts.length === 0 ? <p className="empty-state">当前没有待回答问题。保存材料或继续 Codex 执行后会在这里出现对齐问题。</p> : null}
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
