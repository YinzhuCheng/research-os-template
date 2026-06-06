# Public Audit Summary

The current template is in Research OS v3.4. It provides a material-first browser copilot, a shared research kernel, five deep domain modes, and explicit environment setup.

Current public controls:

- Privacy split: `PUBLIC/` contains public or sanitized material; raw intake and sensitive material stay under `PRIVATE/`.
- Write control: writes are governed by `CONTROL/work_order.yaml` and `CONTROL/phase_gate.yaml`.
- Audit trail: substantive runs append to `PROVENANCE/run_manifest.jsonl`.
- Resource trail: costs and real-resource boundaries append to `PROVENANCE/resource_ledger.jsonl`.
- Environment contract: `docs/environment.md`, `scripts/install_environment.ps1`, and `scripts/check_environment.ps1`.
- Paper track: `templates/latex/` is the source scaffold; generated `PUBLIC/paper/` output is created only after explicit paper enablement.

Core constraints:

- Do not assume LLM, machine learning, dataset, baseline, paper, venue, or budget by default.
- Minimum validation budgets, tools, sample sizes, equipment, and models must come from researcher material or explicit confirmation.
- Real credentials must never be written to the repository. Record only environment variable names, secret-store paths, IAM role names, or short-lived credential retrieval procedures.
- Reference downloads must use open-access URLs, DOI/arXiv landing pages, or user-authorized URLs and must not bypass paywalls.

Latest validation report: `PROVENANCE/final_validation_report_v3_4.md` after the v3.4 checks are run.
