import { Play, Square } from "lucide-react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";

export function RuntimePanel() {
  const project = useAppStore((state) => state.project);
  const activeProfileId = useAppStore((state) => state.activeProfileId);
  const [turnText, setTurnText] = useState("读取 Research OS 状态，提出下一步对齐问题，但不要绕过验收门。");
  const events = useQuery({ queryKey: ["runtime-events"], queryFn: () => api.runtimeEvents(0), refetchInterval: 2500 });
  const environment = useQuery({ queryKey: ["runtime-environment"], queryFn: api.environment, retry: false });
  const startThread = useMutation({ mutationFn: () => api.startThread(activeProfileId) });
  const startTurn = useMutation({
    mutationFn: () => {
      const threadId = project?.codex.thread_id ?? String((startThread.data as any)?.thread?.thread?.id ?? "");
      return api.startTurn(threadId, turnText, activeProfileId);
    }
  });
  const interrupt = useMutation({
    mutationFn: () => api.interrupt(project?.codex.thread_id ?? "", project?.codex.last_turn_id ?? "")
  });

  return (
    <section className="panel runtime-panel">
      <div className="section-heading">
        <Play size={18} aria-hidden="true" />
        <div>
          <h2>Codex Runtime</h2>
          <p>{environment.data?.codex_sdk_available ? "Codex SDK 可用" : "Codex SDK 未安装，执行接口会安全失败"}</p>
        </div>
      </div>
      <label className="field">
        <span>下一轮指令</span>
        <textarea value={turnText} onChange={(event) => setTurnText(event.target.value)} rows={4} />
      </label>
      <div className="inline-actions">
        <button className="secondary-action" type="button" onClick={() => startThread.mutate()}>
          <Play size={16} aria-hidden="true" />
          启动 Thread
        </button>
        <button className="primary-action" type="button" onClick={() => startTurn.mutate()} disabled={!project?.codex.thread_id && !startThread.data}>
          <Play size={16} aria-hidden="true" />
          执行/继续
        </button>
        <button className="secondary-action" type="button" onClick={() => interrupt.mutate()} disabled={!project?.codex.last_turn_id}>
          <Square size={16} aria-hidden="true" />
          中断
        </button>
      </div>
      {[startThread.error, startTurn.error, interrupt.error].filter(Boolean).map((error, index) => (
        <p className="error-text" key={index}>{(error as Error).message}</p>
      ))}
      <div className="event-log" aria-label="Runtime events">
        {(events.data?.events ?? []).slice(-8).map((event, index) => (
          <pre key={index}>{JSON.stringify(event, null, 2)}</pre>
        ))}
      </div>
    </section>
  );
}
