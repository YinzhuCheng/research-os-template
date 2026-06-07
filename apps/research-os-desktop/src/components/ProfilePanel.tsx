import { KeyRound, Save } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../api";
import { useAppStore } from "../store";
import type { Profile } from "../types";

export function ProfilePanel() {
  const queryClient = useQueryClient();
  const activeProfileId = useAppStore((state) => state.activeProfileId);
  const setActiveProfileId = useAppStore((state) => state.setActiveProfileId);
  const profiles = useQuery({ queryKey: ["profiles"], queryFn: api.profiles });
  const [draft, setDraft] = useState<Profile>({
    profile_id: "custom-openai-compatible",
    label: "OpenAI Compatible",
    type: "custom_provider",
    provider_id: "custom",
    model: "",
    base_url: "",
    secret_ref: "env:OPENAI_API_KEY"
  });
  const save = useMutation({
    mutationFn: () => api.saveProfile(draft),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["profiles"] })
  });

  return (
    <section className="panel profile-panel">
      <div className="section-heading">
        <KeyRound size={18} aria-hidden="true" />
        <div>
          <h2>Profile 与模型</h2>
          <p>Profile 只保存 provider 和模型偏好，不保存 API key、token 或密码。</p>
        </div>
      </div>
      <div className="profile-list">
        {(profiles.data?.profiles ?? []).map((profile) => (
          <button
            className={`profile-button ${profile.profile_id === activeProfileId ? "active" : ""}`}
            key={profile.profile_id}
            type="button"
            onClick={() => setActiveProfileId(profile.profile_id)}
          >
            <strong>{profile.label}</strong>
            <small>{profile.provider_id ?? profile.type}</small>
          </button>
        ))}
      </div>
      <div className="profile-form">
        <label className="field">
          <span>Profile ID</span>
          <input value={draft.profile_id} onChange={(event) => setDraft({ ...draft, profile_id: event.target.value })} />
        </label>
        <label className="field">
          <span>显示名称</span>
          <input value={draft.label} onChange={(event) => setDraft({ ...draft, label: event.target.value })} />
        </label>
        <label className="field">
          <span>Provider ID</span>
          <input value={draft.provider_id ?? ""} onChange={(event) => setDraft({ ...draft, provider_id: event.target.value })} />
        </label>
        <label className="field">
          <span>默认模型</span>
          <input value={draft.model ?? ""} onChange={(event) => setDraft({ ...draft, model: event.target.value })} />
        </label>
        <label className="field">
          <span>Secret 引用</span>
          <input value={draft.secret_ref ?? ""} onChange={(event) => setDraft({ ...draft, secret_ref: event.target.value })} placeholder="env:OPENAI_API_KEY" />
        </label>
      </div>
      <button className="secondary-action" type="button" onClick={() => save.mutate()}>
        <Save size={16} aria-hidden="true" />
        保存 Profile
      </button>
      {save.error ? <p className="error-text">{save.error.message}</p> : null}
    </section>
  );
}
