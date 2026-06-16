# PROVENANCE

This directory stores auditable, sanitized records for Research OS runs.

Keep:

- `run_manifest.jsonl`: append-only records for substantive runs.
- `resource_ledger.jsonl`: resource and budget records.
- `live_evidence_snapshot.yaml`: current source basis for time-sensitive claims.
- Validation reports and public audit summaries.

Do not store raw private uploads, secrets, credentials, cookies, authorization headers, or unsanitized API/model payloads here. Raw private materials belong under `PRIVATE/`, which is intentionally not tracked by git.

Older validation snapshots can be recovered from git history. The current tree keeps the latest relevant reports plus the durable manifest and ledger.
