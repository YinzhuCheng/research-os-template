---
name: research-os-visual-communication
description: Improve research paper visual communication, including LaTeX typography, color palettes, TikZ/PGFPlots/SVG vector figures, tables, figure diversity, appendix visuals, graphical abstracts, and AIGC image review.
---

# Research OS Visual Communication

Use this skill for the visual and presentation layer of research outputs.

## Workflow

1. Prefer vector-native figures: TikZ, PGFPlots, SVG, Graphviz, or Mermaid exported to vector.
2. Use bitmap or AIGC images only for graphical abstracts or concept illustrations, never for experimental data.
3. Maintain a figure plan with purpose, evidence source, rendering toolchain, and paper section.
4. Check figure diversity:
   - main result,
   - ablation,
   - cost-performance,
   - failure cases,
   - method structure,
   - experiment flow,
   - qualitative examples or appendix expansions.
5. After visual changes, compile or statically inspect LaTeX sources and render pages when tooling exists.

## Quick Checks

- Read `references/visual_rules.md` before creating figures or changing style.
- Save AIGC prompts, model, parameters, raw output, and review notes.
