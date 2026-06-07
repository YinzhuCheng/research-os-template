import { Play, Square } from "lucide-react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";

export function RuntimePanel() {
  const project = useAppStore((store) => store.project);
  const activeProfileId = useAppStore((store) => store.activeProfileId);
  const [turnText, setTurnText] = useState("读取 Research OS 状态，提出下一步对齐问题；不要绕过验收门。");
  const events = useQuery({ queryKey: ["runtime-events"], queryFn: () => api.runtimeEvents(0), refetchInterval: 2500 });
  const environment = useQuery({ queryKey: ["runtime-environment"], queryFn: api.environment, retry: false });
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
          <p>{environment.data?.codex_sdk_available ? "Codex SDK 可用，所有执行仍经过 Research OS 审批。" : "Codex SDK 未安装或不可用；执行接口会安全失败。"}</p>
        </div>
      </div>
      <label className="field">
        <span>下一轮指令</span>
        <textarea value={turnText} onChange={(event) => setTurnText(event.target.value)} rows={4} />
      </label>
      <div className="inline-actions">
        <button className="secondary-action" type="button" onClick={() => startThread.mutate()} disabled={startThread.isPending}>
          <Play size={16} aria-hidden="true" />
          {startThread.isPending ? "正在启动" : "启动 Thread"}
        </button>
        <button className="primary-action" type="button" onClick={() => startTurn.mutate()} disabled={!canStartTurn || !turnText.trim() || startTurn.isPending}>
          <Play size={16} aria-hidden="true" />
          {startTurn.isPending ? "正在执行" : "执行/继续"}
        </button>
        <button className="secondary-action" type="button" onClick={() => interrupt.mutate()} disabled={!project?.codex.last_turn_id || interrupt.isPending}>
          <Square size={16} aria-hidden="true" />
          中断
        </button>
      </div>
      {!canStartTurn ? <p className="hint-text">先启动 thread，或打开包含 thread_id 的项目。</p> : null}
      {[startThread.error, startTurn.error, interrupt.error].filter(Boolean).map((error, index) => (
        <p className="error-text" key={index}>{(error as Error).message}</p>
      ))}
      <div className="event-log" aria-label="Runtime events">
        {(events.data?.events ?? []).length === 0 ? <p>暂无 runtime events。</p> : null}
        {(events.data?.events ?? []).slice(-8).map((event, index) => (
          <pre key={index}>{JSON.stringify(event, null, 2)}</pre>
        ))}
      </div>
    </section>
  );
}
