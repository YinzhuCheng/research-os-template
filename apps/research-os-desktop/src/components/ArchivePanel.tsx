import { Archive, RefreshCw } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import { internalPhaseLabel, macroPhaseLabel } from "../labels";

function asString(value: unknown, fallback = "unknown") {
  return typeof value === "string" && value ? value : fallback;
}

function changedPaths(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}

export function ArchivePanel() {
  const queryClient = useQueryClient();
  const [description, setDescription] = useState("");
  const preview = useQuery({ queryKey: ["archive-preview"], queryFn: api.archivePreview, retry: false });
  const archives = useQuery({ queryKey: ["archives"], queryFn: api.archives, retry: false });
  const create = useMutation({
    mutationFn: () => api.createArchive(description),
    onSuccess: () => {
      setDescription("");
      queryClient.invalidateQueries({ queryKey: ["archives"] });
      queryClient.invalidateQueries({ queryKey: ["archive-preview"] });
    },
  });
  const changed = changedPaths(preview.data?.changed_paths);
  const dirty = Boolean(preview.data?.dirty);

  return (
    <section className="panel">
      <div className="section-heading">
        <Archive size={18} aria-hidden="true" />
        <div>
          <h2>Archive</h2>
          <p>Create a git-backed snapshot and a redacted index before long runs, phase changes, paid review rounds, or risky operations.</p>
        </div>
      </div>
      <div className="metric-row">
        <span>Macro phase</span>
        <strong>{macroPhaseLabel(asString(preview.data?.macro_phase))}</strong>
      </div>
      <div className="metric-row">
        <span>Internal phase</span>
        <strong>{internalPhaseLabel(asString(preview.data?.phase))}</strong>
      </div>
      <div className="metric-row">
        <span>Git state</span>
        <strong>{dirty ? `${changed.length} changed paths` : "Clean, no pending archive changes"}</strong>
      </div>
      {changed.length > 0 ? (
        <ul className="changed-paths" aria-label="Changed paths">
          {changed.slice(0, 5).map((item) => <li key={item}>{item}</li>)}
          {changed.length > 5 ? <li>{changed.length - 5} more paths...</li> : null}
        </ul>
      ) : null}
      <p className="hint-text">Privacy check: {String(preview.data?.secrets_scan ?? "not refreshed")}; PRIVATE paths do not enter the public archive index.</p>
      <label className="field">
        <span>Archive description</span>
        <textarea value={description} onChange={(event) => setDescription(event.target.value)} rows={3} placeholder="Describe the research state, risk, or next action this archive should preserve." />
      </label>
      <div className="inline-actions">
        <button className="secondary-action" type="button" onClick={() => preview.refetch()}>
          <RefreshCw size={16} aria-hidden="true" />
          Refresh preview
        </button>
        <button className="primary-action" type="button" onClick={() => create.mutate()} disabled={!description.trim() || create.isPending}>
          <Archive size={16} aria-hidden="true" />
          {create.isPending ? "Creating" : "Create archive"}
        </button>
      </div>
      {create.error ? <p className="error-text">{create.error.message}</p> : null}
      <p className="muted">Existing archives: {archives.data?.archives.length ?? 0}. Restore, compare, and continue entry points will be added here after the archive model stabilizes.</p>
    </section>
  );
}
