# CONTROL

This directory stores the Research OS control plane.

Key files:

- `work_order.yaml`: what this run may read/write, expected outputs, budget, stop conditions, and acceptance criteria.
- `phase_gate.yaml`: current phase, intervention level, and decisions requiring human confirmation.
- `copilot_inbox/` when present: sanitized browser copilot packets waiting for Codex review.

Rules:

- Read `work_order.yaml`, `phase_gate.yaml`, and `config/research_project.yaml` before mutating work.
- Use `config/research_flow.yaml` to decide which skill should handle each process stage.
- Do not move raw private material into `CONTROL/`; raw intake belongs in `PRIVATE/`.
- Do not treat the browser queue as execution approval. Codex must still apply work order, phase gate, harness, privacy, and resource checks.
