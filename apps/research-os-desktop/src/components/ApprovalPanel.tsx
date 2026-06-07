import { ShieldCheck, ShieldX } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../api";

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
            <div>
              <strong>{approval.method}</strong>
              <small>{approval.risk.reason}</small>
            </div>
            <div className="approval-actions">
              <button type="button" className="secondary-action" onClick={() => decide.mutate({ approvalId: approval.approval_id, decision: "decline" })}>
                <ShieldX size={14} aria-hidden="true" />
                拒绝
              </button>
              <button type="button" className="primary-action" onClick={() => decide.mutate({ approvalId: approval.approval_id, decision: "accept" })}>
                <ShieldCheck size={14} aria-hidden="true" />
                允许
              </button>
            </div>
          </article>
        ))}
      </div>
      {decide.error ? <p className="error-text">{decide.error.message}</p> : null}
    </section>
  );
}
