# Replay Eval Rules

- Prefer append-only records.
- Record the command or tool, inputs, outputs, hashes when available, cost, privacy level, and errors.
- Treat missing logs, missing terminal states, and unverifiable artifacts as audit risks.
- Keep raw private traces in `PRIVATE/`; publish only sanitized summaries.
