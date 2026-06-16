# Privacy And Audit Plan

## Privacy Zones

- `PUBLIC/`: public or sanitized material only.
- `PRIVATE/`: raw conversations, sensitive data, raw model/API calls, private audit records, and secret-reference procedures.
- `PROVENANCE/`: sanitized source records, hashes, resource use, manifests, live-evidence records, and public audit summaries.

## Forbidden Public Content

- API keys, tokens, cookies, authorization headers, SSH private keys, cloud passwords, and direct-login connection strings.
- Unsanitized user conversations, private data, unauthorized datasets, or sensitive model responses.
- Unlicensed images, PDFs, or data sources.

## Audit Requirements

- Every work order records inputs, outputs, allowed paths, forbidden paths, budget, stop conditions, and acceptance criteria.
- Every substantive run appends `PROVENANCE/run_manifest.jsonl`.
- Resource use is recorded in `PROVENANCE/resource_ledger.jsonl`.
- Public export requires privacy scanning.
- Generated images must record prompt, model, parameters, source image when relevant, and review notes.

## Failure Policy

If a scan finds sensitive material, public export fails. Codex should not delete raw material automatically; it should produce a sanitized copy or ask for human correction.
