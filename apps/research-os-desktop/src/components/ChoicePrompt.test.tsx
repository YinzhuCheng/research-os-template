import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import type { ChoicePrompt as ChoicePromptType } from "../types";
import { ChoicePrompt } from "./ChoicePrompt";

const prompt: ChoicePromptType = {
  prompt_id: "CP-TEST",
  question: "下一步选择什么？",
  recommended_option: "balanced",
  why_recommended: "默认均衡路径风险较低。",
  options: [
    { id: "balanced", label: "均衡路径", description: "同时处理目标和证据。", is_recommended: true },
    { id: "fast", label: "快速路径", description: "先跑通最小验证。" },
  ],
  free_form_enabled: true,
  free_form_label: "自然语言补充",
  free_form_placeholder: "补充约束",
};

describe("ChoicePrompt", () => {
  it("renders recommendation, options, and free-form input", async () => {
    const onSubmit = vi.fn();
    render(<ChoicePrompt prompt={prompt} onSubmit={onSubmit} />);

    expect(screen.getByText("推荐")).toBeInTheDocument();
    expect(screen.getByLabelText("自然语言补充")).toBeInTheDocument();
    expect(screen.getByText("快速路径")).toBeInTheDocument();

    await userEvent.type(screen.getByLabelText("自然语言补充"), "需要保留软件目标");
    await userEvent.click(screen.getByRole("button", { name: /保存选择/ }));

    expect(onSubmit).toHaveBeenCalledWith({ optionId: "balanced", freeForm: "需要保留软件目标" });
  });
});
