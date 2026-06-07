import { FileText, PackageCheck, Presentation, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

interface Props {
  open: boolean;
  onClose: () => void;
  onSubmit: (tracks: string[], freeForm: string) => void;
  pending?: boolean;
  error?: string;
}

const tracks = [
  { id: "paper", label: "论文", description: "目标 venue、模板、同类论文、LaTeX/PDF、review/rebuttal。", Icon: FileText },
  { id: "report", label: "研究报告", description: "更详细记录过程、初始数据、负结果和复现细节。", Icon: Presentation },
  { id: "software", label: "软件", description: "按正式、稳定、规范、美观、用户友好的工程标准推进。", Icon: PackageCheck },
];

export function FinalProductModal({ open, onClose, onSubmit, pending = false, error }: Props) {
  const [selected, setSelected] = useState<string[]>([]);
  const [freeForm, setFreeForm] = useState("");
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (open) {
      closeRef.current?.focus();
    }
  }, [open]);

  if (!open) return null;

  function toggle(track: string) {
    setSelected((current) => (current.includes(track) ? current.filter((item) => item !== track) : [...current, track]));
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <section className="modal" role="dialog" aria-modal="true" aria-labelledby="final-product-title">
        <button ref={closeRef} className="icon-button modal-close" type="button" aria-label="关闭最终产物选择" onClick={onClose}>
          <X size={18} />
        </button>
        <h2 id="final-product-title">进入最终产物阶段</h2>
        <p className="muted">选择你要产出的成果类型，可多选。报告是常见推荐，但不会自动替你勾选；关闭弹窗会继续停留在第二阶段。</p>
        <div className="track-list">
          {tracks.map(({ id, label, description, Icon }) => (
            <label className={`track-row ${selected.includes(id) ? "selected" : ""}`} key={id}>
              <input type="checkbox" checked={selected.includes(id)} onChange={() => toggle(id)} />
              <Icon size={18} aria-hidden="true" />
              <span>
                <strong>{label}{id === "report" ? <em>推荐</em> : null}</strong>
                <small>{description}</small>
              </span>
            </label>
          ))}
        </div>
        <label className="field">
          <span>自然语言目标调整</span>
          <textarea value={freeForm} onChange={(event) => setFreeForm(event.target.value)} rows={4} placeholder="例如：软件优先做成桌面工具；论文目标偏向 CHI；报告需要 PPT 和 HTML。" />
        </label>
        {error ? <p className="error-text">{error}</p> : null}
        <div className="modal-actions">
          <button className="secondary-action" type="button" onClick={onClose}>继续第二阶段</button>
          <button className="primary-action" type="button" onClick={() => onSubmit(selected, freeForm)} disabled={selected.length === 0 || pending}>
            {pending ? "正在确认" : "确认进入"}
          </button>
        </div>
      </section>
    </div>
  );
}
