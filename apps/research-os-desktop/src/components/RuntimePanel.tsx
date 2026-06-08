import { AlertTriangle, Play, RefreshCw, Square, Wrench } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";

const DEFAULT_PAPER_TURN = `Continue this project through the Research OS app-first workflow.

1. First read and follow the project AGENTS.md, CONTROL/project_context.md, CONTROL/work_order.yaml, CONTROL/phase_gate.yaml, and the relevant repo skills: research-os-orchestrator, research-os-execution-harness, research-os-resource-guard, research-os-live-evidence-refresh, research-os-paper-authoring, research-os-review-rebuttal, and research-os-visual-communication when needed.
2. Treat the current manuscript, PDF, PPT, templates, example papers, notes, proof-audit files, and prior review records as initialization material. Do not treat an old draft as a final product.
3. Use the material manifest to generate or update the structured research plan: problem, motivation, expected contributions, related literature, theoretical setup, proof route, optional computational checks, source verification, risks, and acceptance criteria.
4. Use PUBLIC/material_manifest_summary.json first. Do not print or echo full material manifests, full file lists, or raw private paths into the runtime stream; if more detail is needed, read only targeted representative files.
5. Verify Neural Networks submission rules, Elsevier template requirements, every citation, DOI, arXiv page, and publisher source online. Do not cite from memory and do not invent sources.
6. If the app or workflow blocks reusable progress, record the gap and propose or implement the app fix before bypassing it manually.
7. Produce only the next acceptance-ready artifact and structured records for this turn; do not bypass Research OS stage gates.`;

function eventTitle(event: Record<string, unknown>) {
  const type = String(event.type ?? "runtime_event");
  const method = event.method ? ` / ${String(event.method)}` : "";
  if (type === "assistant_message") return "Codex output";
  if (type === "runtime_error") return "Runtime needs repair";
  if (type === "thread_started") return "Thread started";
  if (type === "turn_started") return "Turn started";
  if (type === "codex_notification") return `Codex event${method}`;
  return type.replace(/_/g, " ");
}

function eventSummary(event: Record<string, unknown>) {
  if (typeof event.message === "string") return event.message;
  if (typeof event.error === "string") return event.error;
  const payload = event.payload as Record<string, unknown> | undefined;
  if (payload && typeof payload.message === "string") return payload.message;
  if (payload && typeof payload.status === "string") return `Status: ${payload.status}`;
  if (payload && typeof payload.reason === "string") return payload.reason;
  if (event.type === "runtime_turn_marked_needs_repair") return "The turn was marked for bounded retry from saved state.";
  if (event.type === "codex_notification" && event.method === "thread/tokenUsage/updated") {
    const usage = payload?.tokenUsage as Record<string, unknown> | undefined;
    const last = usage?.last as Record<string, unknown> | undefined;
    if (last?.totalTokens) return `Last usage update: ${String(last.totalTokens)} tokens.`;
  }
  if (event.type === "codex_notification" && typeof event.method === "string" && event.method.includes("commandExecution")) {
    const item = payload?.item as Record<string, unknown> | undefined;
    if (item?.command) return String(item.command);
    if (payload?.delta) return String(payload.delta);
  }
  return "Structured event recorded. Expand to inspect details.";
}

export function RuntimePanel() {
  const queryClient = useQueryClient();
  const project = useAppStore((store) => store.project);
  const setProject = useAppStore((store) => store.setProject);
  const activeProfileId = useAppStore((store) => store.activeProfileId);
  const [turnText, setTurnText] = useState(DEFAULT_PAPER_TURN);
  const [keyFilePath, setKeyFilePath] = useState("");
  const events = useQuery({ queryKey: ["runtime-events"], queryFn: () => api.runtimeEvents(0), refetchInterval: 2500 });
  const environment = useQuery({ queryKey: ["runtime-environment"], queryFn: api.environment, retry: false });
  const runtimeConfig = environment.data?.runtime_config;
  const runtimeConfigured = Boolean(runtimeConfig?.provider_id || runtimeConfig?.model);
  const runtimeReady = Boolean(environment.data?.codex_sdk_available && runtimeConfig?.secret_loaded);
  const loadSecret = useMutation({
    mutationFn: () => api.loadRuntimeSecret(activeProfileId, keyFilePath),
    onSuccess: () => environment.refetch(),
  });
  const startThread = useMutation({ mutationFn: () => api.startThread(activeProfileId) });
  const startTurn = useMutation({
    mutationFn: () => {
      const threadId = project?.codex.thread_id ?? String((startThread.data as any)?.thread?.thread?.id ?? "");
      return api.startTurn(threadId, turnText, activeProfileId);
    },
  });
  const interrupt = useMutation({
    mutationFn: () => api.interrupt(project?.codex.thread_id ?? "", project?.codex.last_turn_id ?? ""),
    onSuccess: async () => {
      events.refetch();
      const current = await api.currentProject();
      setProject(current.project);
    },
  });
  const markNeedsRepair = useMutation({
    mutationFn: () =>
      api.markTurnNeedsRepair(
        project?.codex.thread_id ?? "",
        project?.codex.last_turn_id ?? "",
        "Researcher marked this turn as stale, interrupted, or not app-readable; continue from saved project state with a bounded retry."
      ),
    onSuccess: async () => {
      await events.refetch();
      const current = await api.currentProject();
      setProject(current.project);
      queryClient.invalidateQueries({ queryKey: ["project"] });
    },
  });
  const canStartTurn = Boolean(project?.codex.thread_id || startThread.data);
  const turnStatus = project?.codex.last_status ?? "not_started";
  const showRecovery = Boolean(project?.codex.last_turn_id && ["turn_started", "turn_interrupted", "needs_repair"].includes(turnStatus));

  return (
    <section className="panel runtime-panel">
      <div className="section-heading">
        <Play size={18} aria-hidden="true" />
        <div>
          <h2>Codex Execution Stream</h2>
          <p>
            {runtimeReady
              ? "Codex SDK is available. Execution still goes through Research OS approvals."
              : runtimeConfigured
                ? "Provider settings are detected. Reload the local key into sidecar memory before the next paid Codex turn."
                : "Codex SDK is missing or unavailable. Configure the runtime before starting real execution."}
          </p>
        </div>
      </div>
      <div className="runtime-proof">
        <span>Provider: <strong>{runtimeConfig?.provider_id ?? "not configured"}</strong></span>
        <span>Model: <strong>{runtimeConfig?.model ?? "not configured"}</strong></span>
        <span>Reasoning: <strong>{runtimeConfig?.reasoning_effort ?? "not configured"}</strong></span>
        <span>Secret: <strong>{runtimeConfig?.secret_loaded ? "loaded in sidecar memory" : "not loaded"}</strong></span>
        <span>Route: <strong>{runtimeConfig?.proxy_mode === "custom" ? runtimeConfig.proxy_url : runtimeConfig?.proxy_mode ?? "direct"}</strong></span>
        <span>Turn: <strong>{turnStatus}</strong></span>
      </div>
      {showRecovery ? (
        <div className="notice warning runtime-recovery">
          <AlertTriangle size={16} aria-hidden="true" />
          <div>
            <strong>{turnStatus === "turn_started" ? "A turn is still marked as running" : "This turn needs a continuation decision"}</strong>
            <p>
              If the stream stopped, the provider disconnected, or the output was not app-readable, prepare a bounded retry from the saved project state instead of recreating the project.
            </p>
          </div>
        </div>
      ) : null}
      {!runtimeReady ? (
        <div className="empty-state action-state">
          <strong>{runtimeConfigured ? "Provider profile is detected; key is not loaded" : "Research engine is not ready"}</strong>
          <p>
            {runtimeConfigured
              ? "This is expected after a sidecar restart. Keys stay in process memory only, so reload the local key file before continuing a real Yunwu/Codex turn."
              : "You can still organize materials, answer alignment questions, and create archives. Real Codex execution needs the Codex SDK plus a loaded provider key."}
          </p>
          <label className="field">
            <span>Local key file path (not saved)</span>
            <input value={keyFilePath} onChange={(event) => setKeyFilePath(event.target.value)} placeholder="Select or paste a local key file path" />
          </label>
          <div className="inline-actions">
            <button className="secondary-action" type="button" onClick={() => loadSecret.mutate()} disabled={!keyFilePath.trim() || loadSecret.isPending}>
              <RefreshCw size={16} aria-hidden="true" />
              {loadSecret.isPending ? "Loading key" : "Load key into sidecar"}
            </button>
            <button className="secondary-action" type="button" onClick={() => environment.refetch()} disabled={environment.isFetching}>
              <RefreshCw size={16} aria-hidden="true" />
              {environment.isFetching ? "Checking" : "Retry check"}
            </button>
          </div>
          {loadSecret.error ? <p className="error-text">{loadSecret.error.message}</p> : null}
          <details>
            <summary>Configuration notes</summary>
            <p>Research OS writes provider settings to an isolated app-owned CODEX_HOME. Keys are loaded into the sidecar process environment only and are not saved to the project.</p>
          </details>
        </div>
      ) : null}
      <label className="field">
        <span>Next turn instruction</span>
        <textarea value={turnText} onChange={(event) => setTurnText(event.target.value)} rows={8} />
      </label>
      <div className="inline-actions">
        <button className="secondary-action" type="button" onClick={() => startThread.mutate()} disabled={!runtimeReady || startThread.isPending}>
          <Play size={16} aria-hidden="true" />
          {startThread.isPending ? "Starting" : "Start thread"}
        </button>
        <button className="primary-action" type="button" onClick={() => startTurn.mutate()} disabled={!runtimeReady || !canStartTurn || !turnText.trim() || startTurn.isPending}>
          <Play size={16} aria-hidden="true" />
          {startTurn.isPending ? "Running" : "Run or continue"}
        </button>
        <button className="secondary-action" type="button" onClick={() => interrupt.mutate()} disabled={!project?.codex.last_turn_id || interrupt.isPending}>
          <Square size={16} aria-hidden="true" />
          Interrupt
        </button>
        <button
          className="secondary-action"
          type="button"
          onClick={() => markNeedsRepair.mutate()}
          disabled={!showRecovery || markNeedsRepair.isPending}
          title="Marks the current turn as needing repair so the next turn can continue from saved state."
        >
          <Wrench size={16} aria-hidden="true" />
          {markNeedsRepair.isPending ? "Preparing retry" : "Prepare retry"}
        </button>
      </div>
      {runtimeReady && !canStartTurn ? <p className="hint-text">Start a thread first, or open a project that already has a thread_id.</p> : null}
      {[startThread.error, startTurn.error, interrupt.error, markNeedsRepair.error].filter(Boolean).map((error, index) => (
        <p className="error-text" key={index}>{(error as Error).message}</p>
      ))}
      <div className="event-log" aria-label="Runtime events">
        {(events.data?.events ?? []).length === 0 ? <p>No runtime events yet. Codex output, tool calls, errors, and recovery state will appear here.</p> : <p className="hint-text">Showing the latest runtime events. Full redacted event history is preserved inside the project.</p>}
        {(events.data?.events ?? []).slice(-8).map((event, index) => (
          <article className="event-card" key={index}>
            <strong>{eventTitle(event)}</strong>
            <p>{eventSummary(event)}</p>
            <details>
              <summary>Structured details</summary>
              <pre>{JSON.stringify(event, null, 2)}</pre>
            </details>
          </article>
        ))}
      </div>
    </section>
  );
}
