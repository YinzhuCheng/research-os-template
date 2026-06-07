export type MacroPhase = "initialization" | "research_loop" | "final_product";

export interface RosProject {
  schema_version: string;
  project_id: string;
  name: string;
  project_file: string;
  project_root: string;
  current_macro_phase: MacroPhase;
  current_phase: string;
  default_profile_id: string;
  codex: {
    thread_id: string | null;
    last_turn_id: string | null;
    last_status: string;
  };
}

export interface Profile {
  profile_id: string;
  label: string;
  type: "openai_account" | "openai_api_key" | "custom_provider";
  provider_id?: string;
  model?: string | null;
  base_url?: string;
  secret_ref?: string;
}

export interface ChoicePrompt {
  prompt_id: string;
  stage?: string;
  question: string;
  recommended_option: string;
  why_recommended: string;
  options: Array<{
    id: string;
    label: string;
    description: string;
    is_recommended?: boolean;
  }>;
  free_form_enabled: true;
  free_form_label: string;
  free_form_placeholder?: string;
}

export interface Approval {
  approval_id: string;
  method: string;
  risk: { risk: string; decision: string; reason: string };
  created_at: string;
  status: "pending" | "resolved";
  params: Record<string, unknown>;
}

export interface SidecarState {
  project: RosProject | null;
  research_state: Record<string, unknown>;
  choice_prompts: ChoicePrompt[];
  run_monitor: Record<string, unknown>;
  archive_index: { archives: unknown[] };
}
