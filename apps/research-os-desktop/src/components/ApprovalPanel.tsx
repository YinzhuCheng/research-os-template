import { ShieldCheck, ShieldX } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../api";
import type { Approval } from "../types";

function riskLevel(approval: Approval) {
  return typeof approval.risk === "string" ? approval.risk : approval.risk?.risk ?? "medium";
}

function riskReason(approval: Approval) {
  return typeof approval.risk === "string" ? "Researcher confirmation is required before continuing." : approval.risk?.reason ?? "Researcher confirmation is required before continuing.";
}

function approvalSummary(approval: Approval) {
  const params = approval.params ?? {};
  if (approval.summary) return approval.summary;
  if (approval.command) return approval.command;
  if (typeof params.command === "string") return params.command;
  if (typeof params.summary === "string") return params.summary;
  if (typeof params.path === "string") return params.path;
  return approval.method || approval.approval_id;
}

function approvalScope(approval: Approval) {
  const params = approval.params ?? {};
  if (typeof params.cwd === "string") return params.cwd;
  if (typeof params.path === "string") return params.path;
  if (typeof params.file === "string") return params.file;
  return "Project sandbox or controlled permission scope";
}

export function ApprovalPanel() {
  const queryClient = useQueryClient();
  const approvals = useQuery({ queryKey: ["approvals"], queryFn: api.approvals, refetchInterval: 2000 });
  const decide = useMutation({
    mutationFn: ({ approvalId, decision }: { approvalId: string; decision: "accept" | "decline" | "cancel" }) =>
      api.decideApproval(approvalId, decision),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["approvals"] }),
  });

  return (
    <section className="panel">
      <div className="section-heading">
        <ShieldCheck size={18} aria-hidden="true" />
        <div>
          <h2>Approval Queue</h2>
          <p>Codex command, file, and permission requests must be confirmed here. Timeouts default to decline.</p>
        </div>
      </div>
      {approvals.isLoading ? <p className="muted">Loading approval queue...</p> : null}
      {(approvals.data?.approvals ?? []).length === 0 ? <p className="empty-state">No pending approval requests. High-risk commands, external writeback, and credential access will appear here.</p> : null}
      <div className="approval-list">
        {(approvals.data?.approvals ?? []).map((approval) => (
          <article className="approval-row" key={approval.approval_id}>
            <div className="approval-copy">
              <div className="approval-title-row">
                <strong>{approval.method || "Permission request"}</strong>
                <span className={`risk-badge risk-${riskLevel(approval)}`}>{riskLevel(approval)}</span>
              </div>
              <p>{riskReason(approval)}</p>
              <code>{approvalSummary(approval)}</code>
              <small>Scope: {approvalScope(approval)}</small>
            </div>
            <div className="approval-actions">
              <button type="button" className="secondary-action" onClick={() => decide.mutate({ approvalId: approval.approval_id, decision: "decline" })}>
                <ShieldX size={14} aria-hidden="true" />
                Decline once
              </button>
              <button type="button" className="primary-action" onClick={() => decide.mutate({ approvalId: approval.approval_id, decision: "accept" })}>
                <ShieldCheck size={14} aria-hidden="true" />
                Allow once
              </button>
              <button type="button" className="secondary-action" onClick={() => decide.mutate({ approvalId: approval.approval_id, decision: "cancel" })}>
                Cancel queue
              </button>
            </div>
          </article>
        ))}
      </div>
      {decide.error ? <p className="error-text">{decide.error.message}</p> : null}
    </section>
  );
}
