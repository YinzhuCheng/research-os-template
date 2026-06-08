import { KeyRound, Save } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";
import type { Profile } from "../types";

export function ProfilePanel() {
  const queryClient = useQueryClient();
  const activeProfileId = useAppStore((store) => store.activeProfileId);
  const setActiveProfileId = useAppStore((store) => store.setActiveProfileId);
  const profiles = useQuery({ queryKey: ["profiles"], queryFn: api.profiles });
  const [draft, setDraft] = useState<Profile>({
    profile_id: "yunwu-gpt-55-xhigh",
    label: "Yunwu GPT-5.5 xhigh",
    type: "custom_provider",
    provider_id: "yunwu",
    model: "gpt-5.5",
    base_url: "https://yunwu.ai/v1",
    wire_api: "responses",
    reasoning_effort: "xhigh",
    env_key: "YUNWU_API_KEY",
    secret_ref: "env:YUNWU_API_KEY",
  });
  const save = useMutation({
    mutationFn: () => api.saveProfile(draft),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["profiles"] }),
  });
  const activeProfile = (profiles.data?.profiles ?? []).find((profile) => profile.profile_id === activeProfileId);

  return (
    <section className="panel profile-panel compact-panel">
      <details>
        <summary className="advanced-summary">
          <span>
            <KeyRound size={18} aria-hidden="true" />
            <strong>Advanced Settings: model and secret reference</strong>
          </span>
          <small>{activeProfile ? `${activeProfile.label}${activeProfile.model ? ` / ${activeProfile.model}` : ""}` : "No profile selected"}</small>
        </summary>
        <p className="hint-text">
          Normal research flow does not require editing this first. Profiles store provider, model, and secret references only. Do not paste API keys, tokens, or passwords into a project.
        </p>
        <div className="profile-list">
          {(profiles.data?.profiles ?? []).length === 0 ? (
            <p className="empty-state">No profiles yet. Create an OpenAI-compatible profile that references a local environment variable.</p>
          ) : null}
          {(profiles.data?.profiles ?? []).map((profile) => (
            <button
              className={`profile-button ${profile.profile_id === activeProfileId ? "active" : ""}`}
              key={profile.profile_id}
              type="button"
              onClick={() => setActiveProfileId(profile.profile_id)}
            >
              <strong>{profile.label}</strong>
              <small>
                {profile.provider_id ?? profile.type}
                {profile.model ? ` / ${profile.model}` : ""}
              </small>
            </button>
          ))}
        </div>
        <div className="profile-form">
          <label className="field">
            <span>Profile ID</span>
            <input value={draft.profile_id} onChange={(event) => setDraft({ ...draft, profile_id: event.target.value })} />
          </label>
          <label className="field">
            <span>Display name</span>
            <input value={draft.label} onChange={(event) => setDraft({ ...draft, label: event.target.value })} />
          </label>
          <label className="field">
            <span>Provider ID</span>
            <input value={draft.provider_id ?? ""} onChange={(event) => setDraft({ ...draft, provider_id: event.target.value })} />
          </label>
          <label className="field">
            <span>Default model</span>
            <input value={draft.model ?? ""} onChange={(event) => setDraft({ ...draft, model: event.target.value })} placeholder="gpt-5.5" />
          </label>
          <label className="field">
            <span>Base URL</span>
            <input value={draft.base_url ?? ""} onChange={(event) => setDraft({ ...draft, base_url: event.target.value })} placeholder="https://yunwu.ai/v1" />
          </label>
          <label className="field">
            <span>Wire API</span>
            <input value={draft.wire_api ?? ""} onChange={(event) => setDraft({ ...draft, wire_api: event.target.value })} placeholder="responses" />
          </label>
          <label className="field">
            <span>Reasoning effort</span>
            <input value={draft.reasoning_effort ?? ""} onChange={(event) => setDraft({ ...draft, reasoning_effort: event.target.value })} placeholder="xhigh" />
          </label>
          <label className="field">
            <span>Environment variable</span>
            <input value={draft.env_key ?? ""} onChange={(event) => setDraft({ ...draft, env_key: event.target.value })} placeholder="YUNWU_API_KEY" />
          </label>
          <label className="field">
            <span>Secret reference</span>
            <input value={draft.secret_ref ?? ""} onChange={(event) => setDraft({ ...draft, secret_ref: event.target.value })} placeholder="env:YUNWU_API_KEY" />
          </label>
        </div>
        <button className="secondary-action" type="button" onClick={() => save.mutate()} disabled={save.isPending}>
          <Save size={16} aria-hidden="true" />
          {save.isPending ? "Saving" : "Save profile"}
        </button>
        {save.error ? <p className="error-text">{save.error.message}</p> : null}
      </details>
    </section>
  );
}
