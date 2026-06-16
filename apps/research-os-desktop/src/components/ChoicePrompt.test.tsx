import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import type { ChoicePrompt as ChoicePromptType } from "../types";
import { ChoicePrompt } from "./ChoicePrompt";

const prompt: ChoicePromptType = {
  prompt_id: "CP-TEST",
  question: "What should be selected next?",
  recommended_option: "balanced",
  why_recommended: "The balanced path has lower risk for early research planning.",
  options: [
    { id: "balanced", label: "Balanced path", description: "Handle goals and evidence together.", is_recommended: true },
    { id: "fast", label: "Fast path", description: "Run the smallest useful validation first." },
  ],
  free_form_enabled: true,
  free_form_label: "Natural-language additions",
  free_form_placeholder: "Add constraints",
};

describe("ChoicePrompt", () => {
  it("renders recommendation, options, and free-form input", async () => {
    const onSubmit = vi.fn();
    render(<ChoicePrompt prompt={prompt} onSubmit={onSubmit} />);

    expect(screen.getByText("Recommended")).toBeInTheDocument();
    expect(screen.getByLabelText("Natural-language additions")).toBeInTheDocument();
    expect(screen.getByText("Fast path")).toBeInTheDocument();

    await userEvent.type(screen.getByLabelText("Natural-language additions"), "Keep the software target visible");
    await userEvent.click(screen.getByRole("button", { name: /Save choice/ }));

    expect(onSubmit).toHaveBeenCalledWith({ optionId: "balanced", freeForm: "Keep the software target visible" });
  });
});
