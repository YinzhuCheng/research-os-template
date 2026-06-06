# Copilot Templates

This directory contains material-first Browser Copilot templates.

- `../yaml/copilot_intake.template.yaml`: sanitized intake packet.
- `../yaml/copilot_questions.template.yaml`: exactly three targeted questions.
- `../yaml/copilot_initialization_report.template.yaml`: structured initialization report.

Runtime raw uploads are expected under `PRIVATE/intake/<session_id>/` and are not committed. Public pages should render only sanitized state, hashes, filenames, and human-approved summaries.
