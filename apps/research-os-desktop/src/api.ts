import type { Approval, Profile, RosProject, SidecarState } from "./types";

const SIDECAR_URL = import.meta.env.VITE_SIDECAR_URL ?? "http://127.0.0.1:8789";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${SIDECAR_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    }
  });
  const payload = await response.json();
  if (!response.ok || payload?.ok === false) {
    throw new Error(payload?.error ?? `Sidecar request failed: ${path}`);
  }
  return payload as T;
}

export const api = {
  sidecarUrl: SIDECAR_URL,
  health: () => request<{ ok: boolean; runtime: Record<string, unknown> }>("/health"),
  currentProject: () => request<{ project: RosProject | null }>("/api/projects/current"),
  createProject: (name: string, project_file: string) =>
    request<{ project: RosProject }>("/api/projects/create", { method: "POST", body: JSON.stringify({ name, project_file }) }),
  openProject: (project_file: string) =>
    request<{ project: RosProject }>("/api/projects/open", { method: "POST", body: JSON.stringify({ project_file }) }),
  profiles: () => request<{ profiles: Profile[] }>("/api/profiles"),
  saveProfile: (profile: Profile) => request<{ profile: Profile }>("/api/profiles", { method: "POST", body: JSON.stringify(profile) }),
  state: () => request<SidecarState>("/api/state"),
  approvals: () => request<{ approvals: Approval[] }>("/api/approvals"),
  decideApproval: (approval_id: string, decision: "accept" | "decline" | "cancel", notes = "") =>
    request<{ approval: Approval }>("/api/approvals/decide", { method: "POST", body: JSON.stringify({ approval_id, decision, notes }) }),
  environment: () => request<{ codex_cli: string | null; codex_sdk_available: boolean; adapter: string }>("/api/runtime/environment"),
  runtimeEvents: (after = 0) => request<{ cursor: number; events: Array<Record<string, unknown>> }>(`/api/runtime/events?after=${after}`),
  models: () => request<Record<string, unknown>>("/api/models"),
  startThread: (profile_id?: string, model?: string) =>
    request<Record<string, unknown>>("/api/runtime/start-thread", { method: "POST", body: JSON.stringify({ profile_id, model }) }),
  startTurn: (thread_id: string, text: string, profile_id?: string, model?: string) =>
    request<Record<string, unknown>>("/api/runtime/start-turn", { method: "POST", body: JSON.stringify({ thread_id, text, profile_id, model }) }),
  interrupt: (thread_id: string, turn_id: string) =>
    request<Record<string, unknown>>("/api/runtime/interrupt", { method: "POST", body: JSON.stringify({ thread_id, turn_id }) }),
  submitIntake: (free_text: string) => request<Record<string, unknown>>("/api/intake", { method: "POST", body: JSON.stringify({ free_text }) }),
  saveChoiceResponse: (prompt_id: string, option_id: string, free_form = "") =>
    request<Record<string, unknown>>("/api/choice-response", { method: "POST", body: JSON.stringify({ prompt_id, option_id, free_form }) }),
  finalProducts: (tracks: string[], free_form: string) =>
    request<Record<string, unknown>>("/api/final-products", { method: "POST", body: JSON.stringify({ tracks, free_form }) }),
  recordWorkflowGap: (description: string, severity = "medium") =>
    request<Record<string, unknown>>("/api/workflow-gap", { method: "POST", body: JSON.stringify({ description, severity }) }),
  importDirectory: (source_path: string, target_subdir = "INBOX/imports") =>
    request<Record<string, unknown>>("/api/import-directory", { method: "POST", body: JSON.stringify({ source_path, target_subdir }) }),
  archivePreview: () => request<Record<string, unknown>>("/api/archive-preview"),
  archives: () => request<{ archives: unknown[] }>("/api/archives"),
  createArchive: (description: string, user_free_form = "") =>
    request<Record<string, unknown>>("/api/archives/create", { method: "POST", body: JSON.stringify({ description, user_free_form }) })
};
