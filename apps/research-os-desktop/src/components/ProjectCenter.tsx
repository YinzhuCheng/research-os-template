import { FolderOpen, Plus, RefreshCw, Server } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";
import { chooseRosprojSavePath, selectExistingRosproj } from "../tauriDialog";
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
  const [name, setName] = useState("Neural Networks Submission");
  const [projectFile, setProjectFile] = useState("D:/ResearchOSProjects/neural-network-submission.rosproj");
  const [openPath, setOpenPath] = useState("");
  const [dialogNotice, setDialogNotice] = useState("");
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

  async function chooseCreatePath() {
    setDialogNotice("");
    try {
      const selected = await chooseRosprojSavePath(projectFile);
      if (selected) setProjectFile(selected);
    } catch {
      setDialogNotice("This is not the Tauri desktop runtime, so the system file picker is unavailable. Enter the .rosproj path manually.");
    }
  }

  async function chooseOpenPath() {
    setDialogNotice("");
    try {
      const selected = await selectExistingRosproj();
      if (selected) setOpenPath(selected);
    } catch {
      setDialogNotice("This is not the Tauri desktop runtime, so the system file picker is unavailable. Enter an existing .rosproj path manually.");
    }
  }

  return (
    <main className="project-center">
      <section className="hero-panel">
        <div className="header-copy">
          <p className="eyebrow">Research OS Desktop</p>
          <h1>Research Project Workbench</h1>
          <p className="hero-copy">Create or open a `.rosproj` file. The app creates a sibling project directory as the sandbox and lets the sidecar govern Codex, permissions, archives, and final products.</p>
        </div>
        <div className="status-card" role="status">
          <Server size={18} aria-hidden="true" />
          <div>
            <strong>{health.isSuccess ? "Sidecar connected" : "Waiting for sidecar"}</strong>
            <small>{health.isSuccess ? "Local runtime is available" : "If this persists, restart the app or check the Python sidecar environment."}</small>
          </div>
          <button className="icon-button" type="button" aria-label="Refresh sidecar status" onClick={() => health.refetch()}>
            <RefreshCw size={16} />
          </button>
        </div>
      </section>

      <div className="center-grid">
        <section className="panel">
          <div className="section-heading">
            <Plus size={18} aria-hidden="true" />
            <div>
              <h2>Create Project</h2>
              <p>The app initializes the Research OS directory structure, generated project context, and the first git commit.</p>
            </div>
          </div>
          <label className="field">
            <span>Project name</span>
            <input value={name} onChange={(event) => setName(event.target.value)} />
          </label>
          <label className="field">
            <span>.rosproj path</span>
            <input value={projectFile} onChange={(event) => setProjectFile(event.target.value)} aria-invalid={!createPathValid} />
          </label>
          <button className="secondary-action" type="button" onClick={chooseCreatePath}>
            <FolderOpen size={16} aria-hidden="true" />
            Choose save location
          </button>
          {!createPathValid ? <p className="hint-text">The path should end with `.rosproj`; the project directory will use the same base name.</p> : null}
          <button className="primary-action" type="button" onClick={() => create.mutate()} disabled={create.isPending || !createPathValid || !name.trim()}>
            <Plus size={16} aria-hidden="true" />
            {create.isPending ? "Creating" : "Create project"}
          </button>
          {create.error ? <p className="error-text">{create.error.message}</p> : null}
        </section>

        <section className="panel">
          <div className="section-heading">
            <FolderOpen size={18} aria-hidden="true" />
            <div>
              <h2>Open Project</h2>
              <p>Open an existing `.rosproj` to resume Research OS state and the most recent Codex thread.</p>
            </div>
          </div>
          <label className="field">
            <span>.rosproj path</span>
            <input value={openPath} onChange={(event) => setOpenPath(event.target.value)} placeholder="D:/ResearchOSProjects/demo.rosproj" aria-invalid={Boolean(openPath) && !openPathValid} />
          </label>
          <div className="inline-actions">
            <button className="secondary-action" type="button" onClick={chooseOpenPath}>
              <FolderOpen size={16} aria-hidden="true" />
              Choose project file
            </button>
            <button className="secondary-action" type="button" onClick={() => open.mutate()} disabled={open.isPending || !openPathValid}>
              <FolderOpen size={16} aria-hidden="true" />
              {open.isPending ? "Opening" : "Open project"}
            </button>
          </div>
          {dialogNotice ? <p className="hint-text">{dialogNotice}</p> : null}
          {open.error ? <p className="error-text">{open.error.message}</p> : null}
          <div className="recent-list" aria-label="Recent projects">
            <strong>Recent projects</strong>
            {recent.length === 0 ? <p className="muted">No recent projects yet.</p> : null}
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
