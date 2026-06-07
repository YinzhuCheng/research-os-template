import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ClipboardCheck, FileStack, Upload } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "./api";
import { ApprovalPanel } from "./components/ApprovalPanel";
import { ArchivePanel } from "./components/ArchivePanel";
import { ChoicePrompt } from "./components/ChoicePrompt";
import { FinalProductModal } from "./components/FinalProductModal";
import { PhaseBar } from "./components/PhaseBar";
import { ProjectCenter } from "./components/ProjectCenter";
import { RuntimePanel } from "./components/RuntimePanel";
import { useAppStore } from "./store";

function Workspace() {
  const queryClient = useQueryClient();
  const project = useAppStore((state) => state.project);
  const [material, setMaterial] = useState("");
  const [finalOpen, setFinalOpen] = useState(false);
  const state = useQuery({ queryKey: ["state"], queryFn: api.state, refetchInterval: 5000 });
  const submitIntake = useMutation({ mutationFn: () => api.submitIntake(material), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["state"] }) });
  const finalProducts = useMutation({
    mutationFn: ({ tracks, freeForm }: { tracks: string[]; freeForm: string }) => api.finalProducts(tracks, freeForm),
    onSuccess: () => {
      setFinalOpen(false);
      queryClient.invalidateQueries({ queryKey: ["state"] });
    }
  });
  const activePhase = project?.current_macro_phase ?? "initialization";

  return (
    <main className="workspace">
      <header className="workspace-header">
        <div>
          <p className="eyebrow">当前项目</p>
          <h1>{project?.name}</h1>
          <p>{project?.project_root}</p>
        </div>
        <button className="primary-action" type="button" onClick={() => setFinalOpen(true)}>
          <FileStack size={16} aria-hidden="true" />
          进入最终产物阶段
        </button>
      </header>
      <PhaseBar active={activePhase} />

      <div className="workspace-grid">
        <section className="panel primary-panel">
          <div className="section-heading">
            <Upload size={18} aria-hidden="true" />
            <div>
              <h2>材料与目标</h2>
              <p>输入会先进入项目沙箱内的私有 intake，再由 Codex 生成三个定向问题。</p>
            </div>
          </div>
          <label className="field">
            <span>研究材料、目标、草稿或链接</span>
            <textarea value={material} onChange={(event) => setMaterial(event.target.value)} rows={7} placeholder="粘贴研究计划、ChatGPT 链接、论文线索、软件 demo 说明或实验想法。" />
          </label>
          <button className="primary-action" type="button" onClick={() => submitIntake.mutate()} disabled={!material.trim()}>
            <Upload size={16} aria-hidden="true" />
            保存材料并进入初始化
          </button>
          {submitIntake.error ? <p className="error-text">{submitIntake.error.message}</p> : null}
        </section>

        <section className="panel">
          <div className="section-heading">
            <ClipboardCheck size={18} aria-hidden="true" />
            <div>
              <h2>验收与下一步</h2>
              <p>未验收通过时不会进入下一步；自然语言修改会作为当前阶段修订指令。</p>
            </div>
          </div>
          {(state.data?.choice_prompts ?? []).slice(0, 1).map((prompt) => (
            <ChoicePrompt key={prompt.prompt_id} prompt={prompt} />
          ))}
        </section>

        <RuntimePanel />
        <ApprovalPanel />
        <ArchivePanel />
      </div>
      <FinalProductModal
        open={finalOpen}
        onClose={() => setFinalOpen(false)}
        onSubmit={(tracks, freeForm) => finalProducts.mutate({ tracks, freeForm })}
      />
    </main>
  );
}

export default function App() {
  const setProject = useAppStore((state) => state.setProject);
  const project = useAppStore((state) => state.project);
  const current = useQuery({ queryKey: ["project"], queryFn: api.currentProject, retry: false });

  useEffect(() => {
    if (current.data?.project) {
      setProject(current.data.project);
    }
  }, [current.data?.project, setProject]);

  return project ? <Workspace /> : <ProjectCenter />;
}
