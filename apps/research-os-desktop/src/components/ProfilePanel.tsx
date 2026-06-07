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
    profile_id: "custom-openai-compatible",
    label: "OpenAI Compatible",
    type: "custom_provider",
    provider_id: "custom",
    model: "",
    base_url: "",
    secret_ref: "env:OPENAI_API_KEY",
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
            <strong>高级设置：AI 模型与密钥引用</strong>
          </span>
          <small>{activeProfile ? `${activeProfile.label}${activeProfile.model ? ` · ${activeProfile.model}` : ""}` : "未选择 profile"}</small>
        </summary>
        <p className="hint-text">普通研究流程不需要先改这里。Profile 只保存 provider、模型和 secret 引用；不要把 API key、token 或密码粘贴进项目。</p>
        <div className="profile-list">
          {(profiles.data?.profiles ?? []).length === 0 ? <p className="empty-state">暂无 profile。可以先使用环境变量引用创建一个 OpenAI-compatible profile。</p> : null}
          {(profiles.data?.profiles ?? []).map((profile) => (
            <button
              className={`profile-button ${profile.profile_id === activeProfileId ? "active" : ""}`}
              key={profile.profile_id}
              type="button"
              onClick={() => setActiveProfileId(profile.profile_id)}
            >
              <strong>{profile.label}</strong>
              <small>{profile.provider_id ?? profile.type}{profile.model ? ` · ${profile.model}` : ""}</small>
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
            <input value={draft.model ?? ""} onChange={(event) => setDraft({ ...draft, model: event.target.value })} placeholder="gpt-5.4" />
          </label>
          <label className="field">
            <span>Secret 引用</span>
            <input value={draft.secret_ref ?? ""} onChange={(event) => setDraft({ ...draft, secret_ref: event.target.value })} placeholder="env:OPENAI_API_KEY" />
          </label>
        </div>
        <button className="secondary-action" type="button" onClick={() => save.mutate()} disabled={save.isPending}>
          <Save size={16} aria-hidden="true" />
          {save.isPending ? "正在保存" : "保存 Profile"}
        </button>
        {save.error ? <p className="error-text">{save.error.message}</p> : null}
      </details>
    </section>
  );
}
