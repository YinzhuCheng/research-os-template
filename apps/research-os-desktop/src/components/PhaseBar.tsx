import { CheckCircle2, Circle, FileStack, FlaskConical, Rocket } from "lucide-react";
import { normalizeMacroPhase } from "../labels";
import type { MacroPhase } from "../types";

const phases: Array<{ id: MacroPhase; label: string; detail: string; Icon: typeof Rocket }> = [
  { id: "initialization", label: "初始化阶段", detail: "材料、问题、项目启动包", Icon: Rocket },
  { id: "research_loop", label: "半自动循环研究阶段", detail: "验收、对齐、执行、分析", Icon: FlaskConical },
  { id: "final_product", label: "最终产物阶段", detail: "论文、报告、软件", Icon: FileStack },
];

export function PhaseBar({ active }: { active: MacroPhase | string }) {
  const normalizedActive = normalizeMacroPhase(active);
  const activeIndex = phases.findIndex((phase) => phase.id === normalizedActive);
  return (
    <ol className="phase-bar" aria-label="Research OS 三阶段">
      {phases.map((phase, index) => {
        const complete = index < activeIndex;
        const selected = phase.id === normalizedActive;
        const Icon = phase.Icon;
        return (
          <li className={`phase-item ${selected ? "active" : ""} ${complete ? "complete" : ""}`} key={phase.id}>
            <span className="phase-icon" aria-hidden="true">
              {complete ? <CheckCircle2 size={18} /> : selected ? <Icon size={18} /> : <Circle size={18} />}
            </span>
            <span>
              <strong>{phase.label}</strong>
              <small>{phase.detail}</small>
            </span>
          </li>
        );
      })}
    </ol>
  );
}
