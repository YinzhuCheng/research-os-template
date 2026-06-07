# PUBLIC

This directory contains material that is public, shareable, or explicitly sanitized.

Allowed content:

- Public research briefs, plans, feasibility summaries, decision memos, and dashboards.
- Public-source evidence summaries with links.
- Sanitized experiment, interview, reasoning, engineering, or validation outputs.
- Generated public paper/report/software documentation artifacts only after the researcher enables that final product track.
- Sanitized archive indexes such as `archive_index.json`.

Forbidden content:

- API keys, tokens, cookies, authorization headers, SSH private keys, cloud passwords, or real credentials.
- Raw private conversations, uploaded intake material, private data, or sensitive experimental logs.
- Unauthorized datasets, third-party assets, restricted full text, or copyrighted material copied beyond fair use.
- Raw model/API requests and responses unless they are sanitized summaries approved for public export.

`PUBLIC/paper/` is no longer a tracked default scaffold. Use `templates/latex/` as the source template and generate public paper output only when `dissemination.paper_enabled: true` or a work order explicitly authorizes it.

Final product outputs remain opt-in. Paper, research report, and software release artifacts must pass the same privacy scan and human export/release gate before becoming public.

`PUBLIC/archive_index.json` is a sanitized index. The durable archive ledger is written to `PROVENANCE/archive_index.jsonl` after the first real archive is created; neither file may include `PRIVATE/` content, real credentials, authorization headers, cookies, tokens, or raw private intake material.
