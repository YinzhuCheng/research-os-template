import { Play, Square } from "lucide-react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";

function eventTitle(event: Record<string, unknown>) {
  const type = String(event.type ?? "runtime_event");
  const method = event.method ? ` · ${String(event.method)}` : "";
  if (type === "assistant_message") return "Codex 输出";
  if (type === "runtime_error") return "运行时需要修复";
  if (type === "thread_started") return "Thread 已启动";
  if (type === "turn_started") return "Turn 已开始";
  if (type === "codex_notification") return `Codex 事件${method}`;
  return type.replace(/_/g, " ");
}

function eventSummary(event: Record<string, unknown>) {
  if (typeof event.message === "string") return event.message;
  if (typeof event.error === "string") return event.error;
  const payload = event.payload as Record<string, unknown> | undefined;
  if (payload && typeof payload.message === "string") return payload.message;
  if (payload && typeof payload.status === "string") return `状态：${payload.status}`;
  return "已记录结构化事件，可展开查看详情。";
}

export function RuntimePanel() {
  const project = useAppStore((store) => store.project);
  const activeProfileId = useAppStore((store) => store.activeProfileId);
  const [turnText, setTurnText] = useState("读取 Research OS 状态，提出下一步对齐问题；不要绕过验收门。");
  const events = useQuery({ queryKey: ["runtime-events"], queryFn: () => api.runtimeEvents(0), refetchInterval: 2500 });
  const environment = useQuery({ queryKey: ["runtime-environment"], queryFn: api.environment, retry: false });
  const runtimeReady = Boolean(environment.data?.codex_sdk_available);
  const startThread = useMutation({ mutationFn: () => api.startThread(activeProfileId) });
  const startTurn = useMutation({
    mutationFn: () => {
      const threadId = project?.codex.thread_id ?? String((startThread.data as any)?.thread?.thread?.id ?? "");
      return api.startTurn(threadId, turnText, activeProfileId);
    },
  });
  const interrupt = useMutation({
    mutationFn: () => api.interrupt(project?.codex.thread_id ?? "", project?.codex.last_turn_id ?? ""),
  });
  const canStartTurn = Boolean(project?.codex.thread_id || startThread.data);

  return (
    <section className="panel runtime-panel">
      <div className="section-heading">
        <Play size={18} aria-hidden="true" />
        <div>
          <h2>Codex 执行流</h2>
          <p>{runtimeReady ? "Codex SDK 可用，所有执行仍经过 Research OS 审批。" : "Codex SDK 未安装或不可用；先配置运行时，再启动真实执行。"}</p>
        </div>
      </div>
      {!runtimeReady ? <p className="empty-state">当前只能查看项目状态和准备下一轮指令。安装或配置 Codex runtime 后，Thread/Turn 按钮会用于真实执行。</p> : null}
      <label className="field">
        <span>下一轮指令</span>
        <textarea value={turnText} onChange={(event) => setTurnText(event.target.value)} rows={4} />
      </label>
      <div className="inline-actions">
        <button className="secondary-action" type="button" onClick={() => startThread.mutate()} disabled={!runtimeReady || startThread.isPending}>
          <Play size={16} aria-hidden="true" />
          {startThread.isPending ? "正在启动" : "启动 Thread"}
        </button>
        <button className="primary-action" type="button" onClick={() => startTurn.mutate()} disabled={!runtimeReady || !canStartTurn || !turnText.trim() || startTurn.isPending}>
          <Play size={16} aria-hidden="true" />
          {startTurn.isPending ? "正在执行" : "执行/继续"}
        </button>
        <button className="secondary-action" type="button" onClick={() => interrupt.mutate()} disabled={!project?.codex.last_turn_id || interrupt.isPending}>
          <Square size={16} aria-hidden="true" />
          中断
        </button>
      </div>
      {runtimeReady && !canStartTurn ? <p className="hint-text">先启动 thread，或打开包含 thread_id 的项目。</p> : null}
      {[startThread.error, startTurn.error, interrupt.error].filter(Boolean).map((error, index) => (
        <p className="error-text" key={index}>{(error as Error).message}</p>
      ))}
      <div className="event-log" aria-label="Runtime events">
        {(events.data?.events ?? []).length === 0 ? <p>暂无执行事件。Codex 输出、工具调用、错误和恢复状态会显示在这里。</p> : null}
        {(events.data?.events ?? []).slice(-8).map((event, index) => (
          <article className="event-card" key={index}>
            <strong>{eventTitle(event)}</strong>
            <p>{eventSummary(event)}</p>
            <details>
              <summary>结构化详情</summary>
              <pre>{JSON.stringify(event, null, 2)}</pre>
            </details>
          </article>
        ))}
      </div>
    </section>
  );
}
