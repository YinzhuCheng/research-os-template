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
import { ProfilePanel } from "./components/ProfilePanel";
import { ProjectCenter } from "./components/ProjectCenter";
import { RuntimePanel } from "./components/RuntimePanel";
import { internalPhaseLabel, macroPhaseLabel, normalizeMacroPhase } from "./labels";
import { useAppStore } from "./store";
import { selectMaterialDirectory } from "./tauriDialog";
import type { MaterialManifestSummary } from "./types";

const roleLabels: Record<string, string> = {
  manuscript_draft: "Manuscript draft",
  bibliography: "Bibliography",
  venue_template: "Venue template",
  venue_instruction: "Submission instructions",
  example_paper: "Example paper",
  pdf_document: "PDF material",
  slide_deck: "Slides",
  proof_audit: "Proof audit",
  review_record: "Review or rebuttal record",
  note: "Notes",
  code_or_notebook: "Code or notebook",
  data_or_structured_record: "Structured data",
  figure_or_screenshot: "Figure or screenshot",
  other_material: "Other material",
};

function MaterialManifestCard({ manifest }: { manifest?: MaterialManifestSummary | null }) {
  if (!manifest) {
    return (
      <div className="empty-state compact-empty">
        No full material folder has been imported yet. Import the folder that contains drafts, templates, example papers, notes, and prior review material before generating a research plan.
      </div>
    );
  }
  const roleEntries = Object.entries(manifest.role_counts ?? {}).sort(([a], [b]) => a.localeCompare(b));
  const imports = manifest.imports ?? [];
  return (
    <div className="material-summary" aria-label="Material bundle summary">
      <div className="metric-row">
        <span>Material bundle</span>
        <strong>{manifest.source_name ?? "Unnamed bundle"}</strong>
      </div>
      <div className="metric-row">
        <span>Imported files</span>
        <strong>{manifest.file_count ?? 0}</strong>
      </div>
      <div className="metric-row">
        <span>Excluded files</span>
        <strong>{manifest.excluded_count ?? 0}</strong>
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
      {imports.length > 1 ? (
        <div className="import-list" aria-label="Imported material sources">
          <strong>Imported sources</strong>
          {imports.map((item) => (
            <div className="metric-row compact-metric" key={item.manifest_id ?? item.source_name}>
              <span>{item.source_name ?? item.manifest_id ?? "material source"}</span>
              <strong>{item.file_count ?? 0} files</strong>
            </div>
          ))}
        </div>
      ) : null}
      {(manifest.warnings ?? []).length > 0 ? (
        <div className="notice warning">
          <AlertTriangle size={16} aria-hidden="true" />
          <div>
            <strong>Material issues to confirm</strong>
            <ul>
              {manifest.warnings?.map((warning) => <li key={warning}>{warning}</li>)}
            </ul>
          </div>
        </div>
      ) : null}
    </div>
  );
}

function ResearchPlanStatus({ state }: { state?: Record<string, unknown> }) {
  const plan = state?.research_plan as Record<string, unknown> | undefined;
  if (!plan) return null;
  const internalPhase = String(state?.internal_phase ?? "");
  const status = String(state?.status ?? "");
  let message = "The plan is available as the current research baseline.";
  if (internalPhase === "loop_acceptance_gate" && status.includes("research_plan_ready")) {
    message = "The project should remain at the acceptance gate until this plan is accepted or revised.";
  } else if (status.includes("research_plan_accepted") || internalPhase === "loop_plan_alignment") {
    message = "The plan has been accepted; use the current loop prompt to repair blockers or plan the next artifact.";
  } else if (status.includes("revision")) {
    message = "The plan needs revision before the project can move forward.";
  }
  return (
    <div className="notice info">
      <ClipboardCheck size={16} aria-hidden="true" />
      <span>Research plan generated: {String(plan.summary ?? "awaiting researcher acceptance")}. {message}</span>
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
      setDialogNotice("This is not the Tauri desktop runtime, so the system folder picker is unavailable. Enter the material folder path manually.");
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
          <p className="eyebrow">Current project</p>
          <h1>{project?.name}</h1>
          <p className="path-text">{project?.project_root}</p>
        </div>
        <div className="header-actions">
          <span className="status-pill">Phase: {activePhaseLabel}</span>
          <span className="status-pill subtle">Internal: {internalLabel}</span>
          <button className="primary-action" type="button" onClick={() => setFinalOpen(true)}>
            <FileStack size={16} aria-hidden="true" />
            Enter Final Product
          </button>
        </div>
      </header>

      <PhaseBar active={activePhase} />

      <section className="current-action" aria-label="Current research action">
        <strong>Current task: treat the full neural-network manuscript bundle as initialization material.</strong>
        <span>Import the whole folder, generate a structured research plan, pass the acceptance gate, verify sources, and only then enter final paper production.</span>
      </section>

      {state.error ? (
        <div className="notice danger" role="alert">
          <AlertTriangle size={16} aria-hidden="true" />
          <span>Could not read Research OS state: {state.error.message}</span>
        </div>
      ) : null}

      <div className="workspace-grid">
        <section className="panel primary-panel">
          <div className="section-heading">
            <Upload size={18} aria-hidden="true" />
            <div>
              <h2>Materials and Goal</h2>
              <p>Import the complete folder, then add the research objective in natural language. Raw files stay private; the UI shows only sanitized summaries and warnings.</p>
            </div>
          </div>

          <label className="field">
            <span>Research material folder</span>
            <input
              value={materialDirectory}
              onChange={(event) => setMaterialDirectory(event.target.value)}
              placeholder="D:/Google One/research-os-template/neural network"
            />
          </label>
          <div className="inline-actions split-actions">
            <button className="secondary-action" type="button" onClick={chooseMaterialDirectory}>
              <FolderOpen size={16} aria-hidden="true" />
              Choose folder
            </button>
            <button
              className="primary-action"
              type="button"
              onClick={() => importDirectory.mutate()}
              disabled={!materialDirectory.trim() || importDirectory.isPending}
            >
              <Upload size={16} aria-hidden="true" />
              {importDirectory.isPending ? "Importing" : "Import full material bundle"}
            </button>
          </div>
          {dialogNotice ? <p className="hint-text">{dialogNotice}</p> : null}
          {importDirectory.error ? <p className="error-text">{importDirectory.error.message}</p> : null}
          <MaterialManifestCard manifest={state.data?.material_manifest} />

          <label className="field">
            <span>Research objective, constraints, venue rules, or free-form notes</span>
            <textarea
              value={material}
              onChange={(event) => setMaterial(event.target.value)}
              rows={7}
              placeholder="Example: Treat the old paper, PDF, PPT, template, and example papers as initial materials. First generate a research plan. Verify every citation and submission rule online before final writing."
            />
          </label>
          <div className="inline-actions split-actions">
            <button className="primary-action" type="button" onClick={() => submitIntake.mutate()} disabled={!material.trim() || submitIntake.isPending}>
              <Upload size={16} aria-hidden="true" />
              {submitIntake.isPending ? "Saving" : "Save goal and initialize"}
            </button>
            <span className="muted">Saving creates exactly three targeted questions and does not bypass researcher acceptance.</span>
          </div>
          {submitIntake.error ? <p className="error-text">{submitIntake.error.message}</p> : null}
        </section>

        <section className="panel">
          <div className="section-heading">
            <ClipboardCheck size={18} aria-hidden="true" />
            <div>
              <h2>Acceptance and Next Step</h2>
              <p>Each loop starts by accepting or revising the previous artifact, then answering one to three high-impact alignment questions.</p>
            </div>
          </div>
          {state.isLoading ? <p className="muted">Loading current phase questions...</p> : null}
          <ResearchPlanStatus state={state.data?.research_state} />
          {!state.isLoading && prompts.length === 0 ? <p className="empty-state">No pending questions. Import materials or continue Codex execution to create the next alignment prompt.</p> : null}
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
        <ProfilePanel />
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
