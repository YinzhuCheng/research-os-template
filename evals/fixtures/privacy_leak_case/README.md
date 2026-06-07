# Privacy Leak Fixture

Tests should use a temporary synthetic repository root and a sentinel string.

Expected result: the sentinel raw free text appears only in temporary
`PRIVATE/intake/<session_id>/free_text.md`, never in generated `CONTROL/`,
`PUBLIC/`, or HTTP API response payloads.
