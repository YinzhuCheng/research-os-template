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
  initialization: "初始化阶段",
  research_loop: "半自动循环研究阶段",
  final_product: "最终产物阶段",
};

const internalPhaseLabels: Record<string, string> = {
  initialization_intake: "材料与目标 intake",
  loop_acceptance_gate: "验收门",
  loop_plan_alignment: "下一步规划对齐",
  loop_user_decision: "用户决策记录",
  loop_execute_analyze: "执行与分析",
  final_product_selection: "最终产物选择",
  final_product_production: "最终产物生产",
  export_release_gate: "导出发布确认",
};

export function normalizeMacroPhase(value?: string | null): MacroPhase {
  if (!value) return "initialization";
  return macroAliases[value] ?? "initialization";
}

export function macroPhaseLabel(value?: string | null): string {
  return macroLabels[normalizeMacroPhase(value)];
}

export function internalPhaseLabel(value?: string | null): string {
  if (!value) return "未记录内部阶段";
  return internalPhaseLabels[value] ?? value;
}
