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
          <h2>存档</h2>
          <p>创建 git-backed snapshot，并写入脱敏索引；适合长任务前、阶段切换前和风险操作前。中断后可用最近存档对比、恢复或继续。</p>
        </div>
      </div>
      <div className="metric-row">
        <span>宏观阶段</span>
        <strong>{macroPhaseLabel(asString(preview.data?.macro_phase))}</strong>
      </div>
      <div className="metric-row">
        <span>内部阶段</span>
        <strong>{internalPhaseLabel(asString(preview.data?.phase))}</strong>
      </div>
      <div className="metric-row">
        <span>Git 状态</span>
        <strong>{dirty ? `${changed.length} 个待存档变更` : "干净，无待存档变更"}</strong>
      </div>
      {changed.length > 0 ? (
        <ul className="changed-paths" aria-label="待存档变更">
          {changed.slice(0, 5).map((item) => <li key={item}>{item}</li>)}
          {changed.length > 5 ? <li>还有 {changed.length - 5} 个路径...</li> : null}
        </ul>
      ) : null}
      <p className="hint-text">隐私检查：{String(preview.data?.secrets_scan ?? "待刷新")}；PRIVATE 路径不会进入公开索引。</p>
      <label className="field">
        <span>存档描述</span>
        <textarea value={description} onChange={(event) => setDescription(event.target.value)} rows={3} placeholder="说明这个存档的研究状态、风险或下一步意图。" />
      </label>
      <div className="inline-actions">
        <button className="secondary-action" type="button" onClick={() => preview.refetch()}>
          <RefreshCw size={16} aria-hidden="true" />
          刷新预览
        </button>
        <button className="primary-action" type="button" onClick={() => create.mutate()} disabled={!description.trim() || create.isPending}>
          <Archive size={16} aria-hidden="true" />
          {create.isPending ? "正在创建" : "创建存档"}
        </button>
      </div>
      {create.error ? <p className="error-text">{create.error.message}</p> : null}
      <p className="muted">已有存档：{archives.data?.archives.length ?? 0}。后续会在这里提供恢复、对比和继续入口。</p>
    </section>
  );
}
