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
  { id: "paper", label: "Paper", description: "Venue, template, comparable papers, LaTeX/PDF, review and rebuttal loops.", Icon: FileText },
  { id: "report", label: "Research report", description: "Process-rich record with initial data, negative results, and reproducibility details.", Icon: Presentation },
  { id: "software", label: "Software", description: "Stable, engineered, polished, user-friendly productization with documentation.", Icon: PackageCheck },
];

export function FinalProductModal({ open, onClose, onSubmit, pending = false, error }: Props) {
  const [selected, setSelected] = useState<string[]>([]);
  const [freeForm, setFreeForm] = useState("");
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (open) closeRef.current?.focus();
  }, [open]);

  if (!open) return null;

  function toggle(track: string) {
    setSelected((current) => (current.includes(track) ? current.filter((item) => item !== track) : [...current, track]));
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <section className="modal" role="dialog" aria-modal="true" aria-labelledby="final-product-title">
        <button ref={closeRef} className="icon-button modal-close" type="button" aria-label="Close final product selection" onClick={onClose}>
          <X size={18} />
        </button>
        <h2 id="final-product-title">Enter Final Product Phase</h2>
        <p className="muted">Select one or more output tracks. For this submission project, Paper is recommended. Closing this dialog keeps the project in the research loop.</p>
        <div className="track-list">
          {tracks.map(({ id, label, description, Icon }) => (
            <label className={`track-row ${selected.includes(id) ? "selected" : ""}`} key={id}>
              <input type="checkbox" checked={selected.includes(id)} onChange={() => toggle(id)} />
              <Icon size={18} aria-hidden="true" />
              <span>
                <strong>{label}{id === "paper" ? <em>Recommended</em> : null}</strong>
                <small>{description}</small>
              </span>
            </label>
          ))}
        </div>
        <label className="field">
          <span>Natural-language target adjustment</span>
          <textarea value={freeForm} onChange={(event) => setFreeForm(event.target.value)} rows={4} placeholder="Example: Target Neural Networks Full Article, verify every citation online, and preserve rebuttal-style review records." />
        </label>
        {error ? <p className="error-text">{error}</p> : null}
        <div className="modal-actions">
          <button className="secondary-action" type="button" onClick={onClose}>Continue research loop</button>
          <button className="primary-action" type="button" onClick={() => onSubmit(selected, freeForm)} disabled={selected.length === 0 || pending}>
            {pending ? "Confirming" : "Confirm track"}
          </button>
        </div>
      </section>
    </div>
  );
}
