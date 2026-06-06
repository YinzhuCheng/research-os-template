# Copilot Workflow Reference

## State Machine

`material_input -> save_intake -> pending_intake_analysis -> questions_ready -> answers_received -> initialization_pending_confirmation -> initializing -> review_ready -> loop_alignment -> plan_pending_confirmation -> executing -> acceptance`

The browser can move data into `save_intake` and `answers_received`. Codex is responsible for analysis, planning, execution, and acceptance.

## Material-first Intake

The first screen accepts free text and uploads. It should recommend uploading material, but it must not force a long questionnaire. If the material is sparse, Codex still asks only three targeted questions before initialization.

## Three-question Protocol

The three questions should be generated from the material. Prefer questions that decide:

- contribution boundary;
- research type and theory/experiment balance;
- budget or resource boundary;
- target audience or output;
- minimum validation standard;
- which uploaded material is authoritative.

Each question must reduce planning ambiguity and must include a recommended answer to reduce researcher burden.

## Initialization Report

The report is a startup package, not a finished paper. It must include:

- motivation;
- expected goals;
- contribution claims;
- related work map;
- references with links;
- download script path and legal policy;
- theory track when applicable;
- experiment track when applicable;
- minimum validation when applicable;
- repository resource links.

## Browser-to-Codex Bridge

The local browser cockpit writes sanitized packets and state. Codex reads the queue through the MCP/server bridge, then asks for human confirmation before execution. Runtime raw files belong under `PRIVATE/intake/<session_id>/` and remain outside git.
