import { Check, MessageSquareText } from "lucide-react";
import { useState } from "react";
import type { ChoicePrompt as ChoicePromptType } from "../types";

interface Props {
  prompt: ChoicePromptType;
  pending?: boolean;
  onSubmit?: (selection: { optionId: string; freeForm: string }) => void;
}

export function ChoicePrompt({ prompt, pending = false, onSubmit }: Props) {
  const recommended = prompt.options.find((option) => option.id === prompt.recommended_option) ?? prompt.options[0];
  const [optionId, setOptionId] = useState(recommended.id);
  const [freeForm, setFreeForm] = useState("");

  return (
    <section className="choice-prompt" aria-labelledby={`${prompt.prompt_id}-title`}>
      <div className="section-heading compact-heading">
        <MessageSquareText size={18} aria-hidden="true" />
        <div>
          <h3 id={`${prompt.prompt_id}-title`}>{prompt.question}</h3>
          <p>{prompt.why_recommended}</p>
        </div>
      </div>
      <div className="choice-list" role="radiogroup" aria-label={prompt.question}>
        {prompt.options.map((option) => (
          <label className={`choice-row ${option.id === optionId ? "selected" : ""}`} key={option.id}>
            <input
              type="radio"
              name={prompt.prompt_id}
              checked={option.id === optionId}
              onChange={() => setOptionId(option.id)}
            />
            <span>
              <strong>
                {option.label}
                {option.id === prompt.recommended_option ? <em>推荐</em> : null}
              </strong>
              <small>{option.description}</small>
            </span>
          </label>
        ))}
      </div>
      <label className="field">
        <span>{prompt.free_form_label}</span>
        <textarea
          value={freeForm}
          onChange={(event) => setFreeForm(event.target.value)}
          placeholder={prompt.free_form_placeholder ?? "用自然语言补充你的偏好、限制或修改意见。"}
          rows={3}
        />
      </label>
      <button className="primary-action" type="button" onClick={() => onSubmit?.({ optionId, freeForm })} disabled={pending}>
        <Check size={16} aria-hidden="true" />
        {pending ? "正在保存" : "保存选择"}
      </button>
    </section>
  );
}
