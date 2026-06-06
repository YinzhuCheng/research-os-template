# Documentation Center

Research OS documentation is layered so a researcher can start quickly while later agents can audit every path.

- [Material-first Copilot](../PUBLIC/copilot.html): browser cockpit for free text, links, and uploaded research material.
- [Process Contract](process-contract.md): canonical Research OS flow and skill handoff rules.
- [Environment Guide](environment.md): runtime requirements, optional tools, and installation notes.
- [Copilot Bridge Technical Doc](codex-browser-copilot.html): browser-to-Codex state machine, schemas, plugin bridge, and safety rules.
- [Start Here](start-here.html): quick start for general researchers and Codex beginners.
- [Technical Report](technical-report.html): full repository route for maintainers and future agents.
- [Domain Modes](domain-modes.html): five deep domain paradigms for mathematics, applied mathematics, machine learning, computer science, and statistics.
- [Research Kernel Template](../templates/research_kernel/research_cycle.template.yaml): shared generate-evaluate-update-human gate program.
- [Document Map](doc_map.yaml): authoritative navigation map.

Core controls:

- [Work order](../CONTROL/work_order.yaml)
- [Phase gate](../CONTROL/phase_gate.yaml)
- [Project config](../config/research_project.yaml)
- [Research flow](../config/research_flow.yaml)
- [Repository rules](../AGENTS.md)
- [Public dashboard](../PUBLIC/index.html)
- [Environment check](../scripts/check_environment.ps1)
- [Environment installer](../scripts/install_environment.ps1)
- [Skills](../skills/README.md)
- [Domain profiles](../domain_profiles/README.md)
- [Live evidence](../PROVENANCE/live_evidence_snapshot.yaml)

Maintenance rules:

- Keep raw private material out of `docs/` and `PUBLIC/`.
- Add every durable entrypoint to `doc_map.yaml` and `PUBLIC/dashboard_data.json`.
- Main-route skills need schema/template/validator/doc coverage.
- Offline HTML must use inline CSS/SVG and local repository links.
