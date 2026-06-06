---
name: research-os-copilot
description: Use the Research OS browser cockpit and MCP bridge to collect material-first intake, generate three targeted questions, confirm execution with Codex, and update sanitized project state.
---

# Research OS Copilot Plugin Skill

Use this plugin skill to open or process the material-first Research OS cockpit.

## Commands

- Start the local cockpit server with `.agents/plugins/plugins/research-os-copilot/scripts/research_os_copilot_server.py --serve`.
- Open `http://127.0.0.1:8765/` in the Codex in-app browser.
- Process queued packets from `CONTROL/copilot_inbox/`.

## Rules

- Browser submissions enqueue work; Codex confirms before executing.
- Raw uploads are private runtime files, not public documentation.
- Generate exactly three targeted questions before initialization.
- Use the repository `research-os-copilot` skill for full workflow policy.
