import { FolderOpen, Plus, RefreshCw, Server } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";
import { ProfilePanel } from "./ProfilePanel";

const RECENT_KEY = "researchOS.recentProjects.v1";

function readRecentProjects(): string[] {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY) ?? "[]");
  } catch {
    return [];
  }
}

function rememberProject(path: string) {
  const next = [path, ...readRecentProjects().filter((item) => item !== path)].slice(0, 5);
  localStorage.setItem(RECENT_KEY, JSON.stringify(next));
}

export function ProjectCenter() {
  const queryClient = useQueryClient();
  const setProject = useAppStore((store) => store.setProject);
  const [name, setName] = useState("Untitled Research Project");
  const [projectFile, setProjectFile] = useState("D:/ResearchOSProjects/untitled.rosproj");
  const [openPath, setOpenPath] = useState("");
  const [recent, setRecent] = useState<string[]>(readRecentProjects);
  const health = useQuery({ queryKey: ["health"], queryFn: api.health, retry: false });
  const createPathValid = useMemo(() => projectFile.trim().toLowerCase().endsWith(".rosproj"), [projectFile]);
  const openPathValid = useMemo(() => openPath.trim().toLowerCase().endsWith(".rosproj"), [openPath]);
  const create = useMutation({
    mutationFn: () => api.createProject(name, projectFile),
    onSuccess: (data) => {
      rememberProject(data.project.project_file);
      setRecent(readRecentProjects());
      setProject(data.project);
      queryClient.invalidateQueries({ queryKey: ["project"] });
    },
  });
  const open = useMutation({
    mutationFn: () => api.openProject(openPath),
    onSuccess: (data) => {
      rememberProject(data.project.project_file);
      setRecent(readRecentProjects());
      setProject(data.project);
      queryClient.invalidateQueries({ queryKey: ["project"] });
    },
  });

  return (
    <main className="project-center">
      <section className="hero-panel">
        <div className="header-copy">
          <p className="eyebrow">Research OS Desktop</p>
          <h1>研究项目工作台</h1>
          <p className="hero-copy">创建或打开 `.rosproj` 项目文件。应用会把同名目录作为沙箱，并由 sidecar 统一治理 Codex、权限、归档和最终产物。</p>
        </div>
        <div className="status-card" role="status">
          <Server size={18} aria-hidden="true" />
          <div>
            <strong>{health.isSuccess ? "Sidecar 已连接" : "等待 sidecar"}</strong>
            <small>{health.isSuccess ? "本地运行时可用" : "如长时间未连接，请重启应用或检查 Python 环境。"}</small>
          </div>
          <button className="icon-button" type="button" aria-label="刷新 sidecar 状态" onClick={() => health.refetch()}>
            <RefreshCw size={16} />
          </button>
        </div>
      </section>

      <div className="center-grid">
        <section className="panel">
          <div className="section-heading">
            <Plus size={18} aria-hidden="true" />
            <div>
              <h2>新建项目</h2>
              <p>项目目录会自动生成 Research OS 结构和初始 git commit。</p>
            </div>
          </div>
          <label className="field">
            <span>项目名称</span>
            <input value={name} onChange={(event) => setName(event.target.value)} />
          </label>
          <label className="field">
            <span>.rosproj 路径</span>
            <input value={projectFile} onChange={(event) => setProjectFile(event.target.value)} aria-invalid={!createPathValid} />
          </label>
          {!createPathValid ? <p className="hint-text">路径应以 `.rosproj` 结尾，项目目录会使用同名文件夹。</p> : null}
          <button className="primary-action" type="button" onClick={() => create.mutate()} disabled={create.isPending || !createPathValid || !name.trim()}>
            <Plus size={16} aria-hidden="true" />
            {create.isPending ? "正在创建" : "创建项目"}
          </button>
          {create.error ? <p className="error-text">{create.error.message}</p> : null}
        </section>

        <section className="panel">
          <div className="section-heading">
            <FolderOpen size={18} aria-hidden="true" />
            <div>
              <h2>打开项目</h2>
              <p>打开已有 `.rosproj` 后恢复 Research OS 状态和最近 Codex thread。</p>
            </div>
          </div>
          <label className="field">
            <span>.rosproj 路径</span>
            <input value={openPath} onChange={(event) => setOpenPath(event.target.value)} placeholder="D:/ResearchOSProjects/demo.rosproj" aria-invalid={Boolean(openPath) && !openPathValid} />
          </label>
          <button className="secondary-action" type="button" onClick={() => open.mutate()} disabled={open.isPending || !openPathValid}>
            <FolderOpen size={16} aria-hidden="true" />
            {open.isPending ? "正在打开" : "打开项目"}
          </button>
          {open.error ? <p className="error-text">{open.error.message}</p> : null}
          <div className="recent-list" aria-label="最近项目">
            <strong>最近项目</strong>
            {recent.length === 0 ? <p className="muted">暂无最近项目。</p> : null}
            {recent.map((path) => (
              <button className="recent-item" type="button" key={path} onClick={() => setOpenPath(path)}>
                {path}
              </button>
            ))}
          </div>
        </section>
      </div>
      <ProfilePanel />
    </main>
  );
}
