export type MacroPhase = "initialization" | "research_loop" | "final_product";

export interface RosProject {
  schema_version: string;
  project_id: string;
  name: string;
  project_file: string;
  project_root: string;
  current_macro_phase: MacroPhase | string;
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
  wire_api?: string;
  reasoning_effort?: string;
  env_key?: string;
  secret_ref?: string;
  proxy_mode?: "direct" | "system" | "custom";
  proxy_url?: string;
}

export interface RuntimeConfigStatus {
  configured?: boolean;
  codex_home?: string;
  codex_profile?: string;
  provider_id?: string | null;
  provider_name?: string | null;
  base_url?: string | null;
  wire_api?: string | null;
  env_key?: string | null;
  model?: string | null;
  reasoning_effort?: string | null;
  secret_loaded?: boolean;
  proxy_mode?: "direct" | "system" | "custom" | string | null;
  proxy_url?: string | null;
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
  risk?: { risk?: string; decision?: string; reason?: string } | string;
  created_at: string;
  status: "pending" | "resolved";
  params: Record<string, unknown>;
  summary?: string;
  command?: string;
}

export interface SubmissionWorkflowItem {
  id: string;
  label: string;
  status: string;
  required_evidence?: string;
}

export interface PaperArtifactStatus {
  path: string;
  role?: string;
  bytes?: number;
  updated_at?: string;
}

export interface SubmissionWorkflow {
  target_venue?: string;
  article_type?: string;
  target_section?: string;
  status?: string;
  venue_requirements?: SubmissionWorkflowItem[];
  source_verification?: SubmissionWorkflowItem[];
  proof_audit?: SubmissionWorkflowItem[];
  claim_evidence?: SubmissionWorkflowItem[];
  novelty_positioning?: SubmissionWorkflowItem[];
  artifact_status?: PaperArtifactStatus[];
  research_loop_artifacts?: PaperArtifactStatus[];
  review_rounds?: Array<Record<string, unknown>>;
  workflow_gaps?: Array<Record<string, unknown>>;
}

export interface MaterialManifestSummary {
  schema_version?: string;
  manifest_id?: string;
  created_at?: string;
  source_name?: string;
  target_root?: string;
  file_count?: number;
  excluded_count?: number;
  role_counts?: Record<string, number>;
  warnings?: string[];
  imports?: Array<{
    manifest_id?: string;
    source_name?: string;
    target_root?: string;
    file_count?: number;
    excluded_count?: number;
    role_counts?: Record<string, number>;
    warnings?: string[];
  }>;
}

export interface SidecarState {
  project: RosProject | null;
  research_state: Record<string, unknown>;
  choice_prompts: ChoicePrompt[];
  submission_workflow?: SubmissionWorkflow;
  material_manifest?: MaterialManifestSummary | null;
  run_monitor: Record<string, unknown>;
  archive_index: { archives: unknown[] };
}
