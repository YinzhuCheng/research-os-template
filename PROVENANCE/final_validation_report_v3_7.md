# Research OS v3.7 Validation Report

## Scope

v3.7 lands lightweight Copilot usability improvements only:

- generated `PUBLIC/evidence_board.json` from public claim/evidence records;
- generated `PUBLIC/run_monitor.json` from public experiment, manifest, and resource-ledger summaries;
- lightweight JSON/JSONL/YAML resource rendering in `PUBLIC/index.html`;
- Evidence Board, audit run summary, resource summary, and bridge command copy affordance in `PUBLIC/copilot.html`;
- synthetic private-intake privacy check using temporary fixture roots only.

Deferred P2 items remain out of scope: hypothesis backlog, critic/evolution loops, knowledge graph, real experiment queues, broad AI4Science expansion, and real external adapter execution.

## Validation Commands

Passed locally on 2026-06-07:

- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_public_summaries.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_public_summaries.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_dashboard.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_copilot_state.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_copilot_resource_rendering.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_private_intake_synthetic.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_schemas.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_html_docs.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_eval_fixtures.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_package_artifacts.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_privacy.ps1 -Paths PUBLIC,PROVENANCE`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_harness.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/package_template.ps1 -DryRun`
- runtime Python:
  - `tests/test_schema_instances.py`
  - `tests/test_copilot_privacy.py`
  - `tests/test_hooks.py`
  - `tests/test_public_summaries.py`
- runtime Python: `.codex/hooks/stop_review.py`

## Browser QA

Temporary local HTTP server:

- URL: `http://127.0.0.1:8765/`
- Server stopped after QA.

Chrome headless checks passed:

- `PUBLIC/index.html` rendered `Evidence Board`, `Sanitized Evidence Board`, structured JSON source controls, and the document reader.
- `PUBLIC/copilot.html` rendered `Evidence Board`, `CLAIM-001`, `Latest Audit Runs`, `Resource Summary`, `Copy Start Command`, and the deferred-scope note.
- Nonblank screenshots were generated in the user temp directory:
  - `C:\Users\cyz19\AppData\Local\Temp\research-os-v37-dashboard.png`
  - `C:\Users\cyz19\AppData\Local\Temp\research-os-v37-copilot.png`

## Notes

- The local `python` command resolves to the WindowsApps placeholder and returns exit code `9009`; local tests used the Codex runtime Python path. Repository PowerShell wrappers already resolve that runtime automatically.
- No real `PRIVATE/` material was read. Synthetic privacy tests used temporary directories.
- No paid API, cloud, GPU, lab resource, external download, or external writeback was used.
