import { BookOpenCheck, Bug, ExternalLink, FileSearch, ShieldQuestion } from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import type { SubmissionWorkflow, SubmissionWorkflowItem } from "../types";

function statusLabel(status?: string) {
  if (!status) return "待记录";
  if (status.includes("needs_online")) return "待联网核查";
  if (status.includes("needs_doi")) return "待逐条核查";
  if (status.includes("needs_review")) return "待审计";
  if (status === "verified") return "已核查";
  if (status === "resolved") return "已解决";
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
      {(items ?? []).length === 0 ? <p className="empty-state">暂无条目。Codex 完成分析后会把核查项写回这里。</p> : null}
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
          <h2>论文投稿工作流</h2>
          <p>把目标期刊、来源真实性、证明审计、rebuttal 攻防和 app 缺口放在同一个验收面板中。</p>
        </div>
      </div>

      <div className="workflow-summary">
        <div>
          <span>目标期刊</span>
          <strong>{workflow?.target_venue ?? "待选择"}</strong>
        </div>
        <div>
          <span>文章类型</span>
          <strong>{workflow?.article_type ?? "待确认"}</strong>
        </div>
        <div>
          <span>栏目</span>
          <strong>{workflow?.target_section ?? "待确认"}</strong>
        </div>
      </div>

      <div className="notice info">
        <ExternalLink size={16} aria-hidden="true" />
        <span>每轮论文任务都必须要求 Codex 联网核查官方投稿规则和引用来源；未核查来源不得进入最终正文。</span>
      </div>

      <WorkflowList title="来源真实性核查" items={workflow?.source_verification} icon="source" />
      <WorkflowList title="数学证明审计" items={workflow?.proof_audit} icon="proof" />

      <div className="workflow-block">
        <div className="workflow-block-title">
          <Bug size={16} aria-hidden="true" />
          <strong>App / 工作流缺口</strong>
        </div>
        {gaps.length === 0 ? <p className="empty-state">暂未记录缺口。只要 app 让论文流程不顺，就先记录并修 app。</p> : null}
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
          <span>记录新的 app 或工作流不足</span>
          <textarea
            rows={3}
            value={gap}
            onChange={(event) => setGap(event.target.value)}
            placeholder="例如：来源核查结果不能在 UI 中逐条验收，导致论文引用审计无法复用。"
          />
        </label>
        <button className="secondary-action" type="button" disabled={!gap.trim() || recordGap.isPending} onClick={() => recordGap.mutate()}>
          <Bug size={16} aria-hidden="true" />
          {recordGap.isPending ? "正在记录" : "记录缺口"}
        </button>
        {recordGap.error ? <p className="error-text">{recordGap.error.message}</p> : null}
      </div>
    </section>
  );
}
