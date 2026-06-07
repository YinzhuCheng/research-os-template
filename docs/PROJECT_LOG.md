# Project Log

## 2026-06-06

The project started as a general human-in-loop Research OS scaffold. The initial work created the control files, process contracts, schema layer, skill layer, domain profiles, public/private split, provenance ledger, and validation scripts.

## 2026-06-06 v3.1

Domain routes were expanded beyond mathematics. The repository gained five domain profile families, domain skills, domain templates, and validation scripts for profiles, agent capabilities, templates, routing, and kernel bindings.

## 2026-06-06 v3.2

The research kernel was introduced as the shared generate/evaluate/update/human-gate layer. It added candidate records, evaluator contracts, computation checklists, belief state, search trace, negative result handling, and next-action policy.

## 2026-06-07 v3.9

The user-facing flow was redefined as three macro phases: initialization, semi-automated research loop, and final product. The second phase became an acceptance-gated loop: accept or revise the previous artifact, align the next plan, record user choice plus free-form input, execute, analyze, and return to acceptance.

Final-product tracks were added for paper, research report, and software. Git-backed local archives were added for snapshots before risky transitions and long-running work.

## 2026-06-07 v4.0

Research OS moved from a browser-copilot concept to an independent desktop app route: Tauri + React + Python sidecar + optional official Codex SDK/app-server. The app creates `.rosproj` projects, initializes sibling sandbox directories, gates approvals, manages archives, and preserves Research OS state.

## 2026-06-07 v4.1

The retired browser bridge, browser cockpit, old bridge schemas, old checks, and old plugin entries were removed. Desktop state became `PUBLIC/research_state.json` and `CONTROL/intake_queue/`. The UI was improved with clearer project center, runtime, approval, archive, profile, choice prompt, and final-product flows. Playwright click-path tests were added.

## 2026-06-07 v4.2

This pass removes the remaining static HTML documentation/dashboard legacy, updates product naming away from old seed language, and makes repository documentation English-first while preserving the Chinese default app UI.
