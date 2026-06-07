import { ShieldCheck, ShieldX } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../api";
import type { Approval } from "../types";

function riskLevel(approval: Approval) {
  return typeof approval.risk === "string" ? approval.risk : approval.risk?.risk ?? "medium";
}

function riskReason(approval: Approval) {
  return typeof approval.risk === "string" ? "需要研究者确认后才能继续。" : approval.risk?.reason ?? "需要研究者确认后才能继续。";
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
  return "项目沙箱或受控权限范围";
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
          <h2>审批队列</h2>
          <p>Codex 的命令、文件和权限请求必须在这里确认；超时默认拒绝。</p>
        </div>
      </div>
      {approvals.isLoading ? <p className="muted">正在读取审批队列...</p> : null}
      {(approvals.data?.approvals ?? []).length === 0 ? <p className="empty-state">当前没有待确认请求。高风险命令、外部写回和凭据访问会出现在这里。</p> : null}
      <div className="approval-list">
        {(approvals.data?.approvals ?? []).map((approval) => (
          <article className="approval-row" key={approval.approval_id}>
            <div className="approval-copy">
              <div className="approval-title-row">
                <strong>{approval.method || "权限请求"}</strong>
                <span className={`risk-badge risk-${riskLevel(approval)}`}>{riskLevel(approval)}</span>
              </div>
              <p>{riskReason(approval)}</p>
              <code>{approvalSummary(approval)}</code>
              <small>作用范围：{approvalScope(approval)}</small>
            </div>
            <div className="approval-actions">
              <button type="button" className="secondary-action" onClick={() => decide.mutate({ approvalId: approval.approval_id, decision: "decline" })}>
                <ShieldX size={14} aria-hidden="true" />
                拒绝本次
              </button>
              <button type="button" className="primary-action" onClick={() => decide.mutate({ approvalId: approval.approval_id, decision: "accept" })}>
                <ShieldCheck size={14} aria-hidden="true" />
                允许一次
              </button>
              <button type="button" className="secondary-action" onClick={() => decide.mutate({ approvalId: approval.approval_id, decision: "cancel" })}>
                取消队列
              </button>
            </div>
          </article>
        ))}
      </div>
      {decide.error ? <p className="error-text">{decide.error.message}</p> : null}
    </section>
  );
}
