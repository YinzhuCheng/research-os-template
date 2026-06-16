import { BookOpenCheck, Bug, ExternalLink, FileSearch, ShieldQuestion } from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import type { SubmissionWorkflow, SubmissionWorkflowItem } from "../types";

function statusLabel(status?: string) {
  if (!status) return "Not recorded";
  if (status.includes("needs_online")) return "Needs online verification";
  if (status.includes("needs_doi")) return "Needs per-source check";
  if (status.includes("needs_review")) return "Needs audit";
  if (status === "verified") return "Verified";
  if (status === "resolved") return "Resolved";
  return status;
}

function WorkflowList({ title, items, icon }: { title: string; items?: SubmissionWorkflowItem[]; icon: "source" | "proof" }) {
  const Icon = icon === "source" ? FileSearch : ShieldQuestion;
  return (
    <div className="workflow-block">
      <div className="workflow-block-title">
        <Icon size={16} aria-hidden="true" />
        <strong>{title}</strong>
      </div>
      {(items ?? []).length === 0 ? <p className="empty-state">No items yet. Codex analysis should write reusable check items back here.</p> : null}
      {(items ?? []).map((item) => (
        <article className="workflow-item" key={item.id}>
          <div>
            <strong>{item.label}</strong>
            {item.required_evidence ? <small>{item.required_evidence}</small> : null}
          </div>
          <span>{statusLabel(item.status)}</span>
        </article>
      ))}
    </div>
  );
}

export function PaperWorkflowPanel({ workflow }: { workflow?: SubmissionWorkflow }) {
  const queryClient = useQueryClient();
  const [gap, setGap] = useState("");
  const recordGap = useMutation({
    mutationFn: () => api.recordWorkflowGap(gap, "medium"),
    onSuccess: () => {
      setGap("");
      queryClient.invalidateQueries({ queryKey: ["state"] });
    },
  });
  const gaps = workflow?.workflow_gaps ?? [];

  return (
    <section className="panel paper-workflow-panel">
      <div className="section-heading">
        <BookOpenCheck size={18} aria-hidden="true" />
        <div>
          <h2>Paper Submission Workflow</h2>
          <p>Track venue rules, source authenticity, proof audit, rebuttal-style review, and reusable app gaps in one acceptance panel.</p>
        </div>
      </div>

      <div className="workflow-summary">
        <div>
          <span>Target venue</span>
          <strong>{workflow?.target_venue ?? "Not selected"}</strong>
        </div>
        <div>
          <span>Article type</span>
          <strong>{workflow?.article_type ?? "Not confirmed"}</strong>
        </div>
        <div>
          <span>Section</span>
          <strong>{workflow?.target_section ?? "Not confirmed"}</strong>
        </div>
      </div>

      <div className="notice info">
        <ExternalLink size={16} aria-hidden="true" />
        <span>Every paper turn must require Codex to verify official submission rules and citation sources online. Unverified sources cannot enter final manuscript claims.</span>
      </div>

      <WorkflowList title="Venue Requirements" items={workflow?.venue_requirements} icon="source" />
      <WorkflowList title="Source Authenticity" items={workflow?.source_verification} icon="source" />
      <WorkflowList title="Mathematical Proof Audit" items={workflow?.proof_audit} icon="proof" />
      <WorkflowList title="Claim-Evidence Matrix" items={workflow?.claim_evidence} icon="proof" />
      <WorkflowList title="Novelty Positioning" items={workflow?.novelty_positioning} icon="source" />

      <div className="workflow-block">
        <div className="workflow-block-title">
          <BookOpenCheck size={16} aria-hidden="true" />
          <strong>Accepted Research Loop Artifacts</strong>
        </div>
        {(workflow?.research_loop_artifacts ?? []).length === 0 ? (
          <p className="empty-state">No accepted loop artifacts yet. Source verification, proof audit, novelty map, and claim-evidence records should appear here before final paper production.</p>
        ) : null}
        {(workflow?.research_loop_artifacts ?? []).map((item) => (
          <article className="workflow-item" key={item.path}>
            <div>
              <strong>{item.path}</strong>
              <small>{item.role ?? "research_loop_artifact"}</small>
            </div>
            <span>{item.bytes ? `${Math.round(item.bytes / 1024)} KB` : "Written"}</span>
          </article>
        ))}
      </div>

      <div className="workflow-block">
        <div className="workflow-block-title">
          <BookOpenCheck size={16} aria-hidden="true" />
          <strong>Submission Package Files</strong>
        </div>
        {(workflow?.artifact_status ?? []).length === 0 ? (
          <p className="empty-state">No paper files yet. After controlled sidecar writes, main.tex, references.bib, audit reports, and submission materials appear here.</p>
        ) : null}
        {(workflow?.artifact_status ?? []).map((item) => (
          <article className="workflow-item" key={item.path}>
            <div>
              <strong>{item.path}</strong>
              <small>{item.role ?? "paper_artifact"}</small>
            </div>
            <span>{item.bytes ? `${Math.round(item.bytes / 1024)} KB` : "Written"}</span>
          </article>
        ))}
      </div>

      <div className="workflow-block">
        <div className="workflow-block-title">
          <Bug size={16} aria-hidden="true" />
          <strong>App / Workflow Gaps</strong>
        </div>
        {gaps.length === 0 ? <p className="empty-state">No gaps recorded yet. If the app makes the paper workflow awkward, record the gap and fix the app first.</p> : null}
        {gaps.slice(-4).map((item, index) => (
          <article className="workflow-item" key={String(item.gap_id ?? index)}>
            <div>
              <strong>{String(item.severity ?? "medium")}</strong>
              <small>{String(item.description ?? "")}</small>
            </div>
            <span>{String(item.status ?? "recorded")}</span>
          </article>
        ))}
        <label className="field">
          <span>Record a new app or workflow gap</span>
          <textarea
            rows={3}
            value={gap}
            onChange={(event) => setGap(event.target.value)}
            placeholder="Example: source-verification results cannot be accepted per reference, so citation audit cannot be reused."
          />
        </label>
        <button className="secondary-action" type="button" disabled={!gap.trim() || recordGap.isPending} onClick={() => recordGap.mutate()}>
          <Bug size={16} aria-hidden="true" />
          {recordGap.isPending ? "Recording" : "Record gap"}
        </button>
        {recordGap.error ? <p className="error-text">{recordGap.error.message}</p> : null}
      </div>
    </section>
  );
}
