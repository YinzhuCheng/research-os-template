import { FolderOpen, Plus, Server } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";
import { ProfilePanel } from "./ProfilePanel";

export function ProjectCenter() {
  const queryClient = useQueryClient();
  const setProject = useAppStore((state) => state.setProject);
  const [name, setName] = useState("Untitled Research Project");
  const [projectFile, setProjectFile] = useState("D:/ResearchOSProjects/untitled.rosproj");
  const [openPath, setOpenPath] = useState("");
  const health = useQuery({ queryKey: ["health"], queryFn: api.health, retry: false });
  const create = useMutation({
    mutationFn: () => api.createProject(name, projectFile),
    onSuccess: (data) => {
      setProject(data.project);
      queryClient.invalidateQueries({ queryKey: ["project"] });
    }
  });
  const open = useMutation({
    mutationFn: () => api.openProject(openPath),
    onSuccess: (data) => {
      setProject(data.project);
      queryClient.invalidateQueries({ queryKey: ["project"] });
    }
  });

  return (
    <main className="project-center">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Research OS Desktop</p>
          <h1>研究项目工作台</h1>
          <p className="hero-copy">创建一个 `.rosproj` 项目，Research OS 会把项目目录作为沙箱，并由 sidecar 统一治理 Codex、归档、权限和最终产物。</p>
        </div>
        <div className="status-pill" role="status">
          <Server size={16} aria-hidden="true" />
          {health.isSuccess ? "Sidecar 已连接" : "等待 sidecar"}
        </div>
      </section>

      <div className="center-grid">
        <section className="panel">
          <div className="section-heading">
            <Plus size={18} aria-hidden="true" />
            <div>
              <h2>新建项目</h2>
              <p>项目目录会自动生成 Research OS 标准结构和初始 git commit。</p>
            </div>
          </div>
          <label className="field">
            <span>项目名称</span>
            <input value={name} onChange={(event) => setName(event.target.value)} />
          </label>
          <label className="field">
            <span>.rosproj 路径</span>
            <input value={projectFile} onChange={(event) => setProjectFile(event.target.value)} />
          </label>
          <button className="primary-action" type="button" onClick={() => create.mutate()} disabled={create.isPending}>
            <Plus size={16} aria-hidden="true" />
            创建项目
          </button>
          {create.error ? <p className="error-text">{create.error.message}</p> : null}
        </section>

        <section className="panel">
          <div className="section-heading">
            <FolderOpen size={18} aria-hidden="true" />
            <div>
              <h2>打开项目</h2>
              <p>打开已有 `.rosproj` 后继续上次 Codex thread 和 Research OS 状态。</p>
            </div>
          </div>
          <label className="field">
            <span>.rosproj 路径</span>
            <input value={openPath} onChange={(event) => setOpenPath(event.target.value)} placeholder="D:/ResearchOSProjects/demo.rosproj" />
          </label>
          <button className="secondary-action" type="button" onClick={() => open.mutate()} disabled={open.isPending || !openPath}>
            <FolderOpen size={16} aria-hidden="true" />
            打开项目
          </button>
          {open.error ? <p className="error-text">{open.error.message}</p> : null}
        </section>
      </div>
      <ProfilePanel />
    </main>
  );
}
