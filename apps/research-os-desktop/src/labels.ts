import type { MacroPhase } from "./types";

const macroAliases: Record<string, MacroPhase> = {
  initialization: "initialization",
  initialization_intake: "initialization",
  loop: "research_loop",
  research: "research_loop",
  research_loop: "research_loop",
  semi_auto_loop: "research_loop",
  semi_automated_research_loop: "research_loop",
  final: "final_product",
  final_product: "final_product",
  final_product_selection: "final_product",
  final_product_production: "final_product",
};

const macroLabels: Record<MacroPhase, string> = {
  initialization: "Initialization",
  research_loop: "Research Loop",
  final_product: "Final Product",
};

const internalPhaseLabels: Record<string, string> = {
  initialization_intake: "Material intake",
  loop_acceptance_gate: "Acceptance gate",
  loop_plan_alignment: "Plan alignment",
  loop_user_decision: "User decision",
  loop_execute_analyze: "Execution and analysis",
  final_product_selection: "Final product selection",
  final_product_production: "Final product production",
  export_release_gate: "Export and release gate",
};

export function normalizeMacroPhase(value?: string | null): MacroPhase {
  if (!value) return "initialization";
  return macroAliases[value] ?? "initialization";
}

export function macroPhaseLabel(value?: string | null): string {
  return macroLabels[normalizeMacroPhase(value)];
}

export function internalPhaseLabel(value?: string | null): string {
  if (!value) return "No internal phase recorded";
  return internalPhaseLabels[value] ?? value;
}
