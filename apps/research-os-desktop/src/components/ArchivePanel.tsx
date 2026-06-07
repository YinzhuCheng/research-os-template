import { Archive, RefreshCw } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";

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
    }
  });

  return (
    <section className="panel">
      <div className="section-heading">
        <Archive size={18} aria-hidden="true" />
        <div>
          <h2>存档</h2>
          <p>存档会创建 git-backed snapshot，并写入脱敏索引。</p>
        </div>
      </div>
      <div className="metric-row">
        <span>阶段</span>
        <strong>{String(preview.data?.phase ?? "unknown")}</strong>
      </div>
      <div className="metric-row">
        <span>未提交变更</span>
        <strong>{preview.data?.dirty ? "有" : "无"}</strong>
      </div>
      <label className="field">
        <span>存档描述</span>
        <textarea value={description} onChange={(event) => setDescription(event.target.value)} rows={3} placeholder="说明这个存档的研究状态、风险或下一步意图" />
      </label>
      <div className="inline-actions">
        <button className="secondary-action" type="button" onClick={() => preview.refetch()}>
          <RefreshCw size={16} aria-hidden="true" />
          刷新预览
        </button>
        <button className="primary-action" type="button" onClick={() => create.mutate()} disabled={!description.trim()}>
          <Archive size={16} aria-hidden="true" />
          创建存档
        </button>
      </div>
      {create.error ? <p className="error-text">{create.error.message}</p> : null}
      <p className="muted">已有存档：{archives.data?.archives.length ?? 0}</p>
    </section>
  );
}
