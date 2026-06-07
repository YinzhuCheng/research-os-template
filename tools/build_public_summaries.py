#!/usr/bin/env python3
"""Build lightweight sanitized PUBLIC summaries for desktop/public dashboards."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from validate_repo import YamlDate, YamlDateTime, load_instance


PRIVATE_PATH_RE = re.compile(r"PRIVATE[\\/]", re.IGNORECASE)
CREDENTIAL_RE = re.compile(
    r"(authorization\s*:|bearer\s+[a-z0-9._-]{8,}|api[_-]?key\s*[:=]|token\s*[:=]|password\s*[:=])",
    re.IGNORECASE,
)


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def json_safe(value: Any) -> Any:
    if isinstance(value, YamlDate | YamlDateTime):
        return value.value
    if isinstance(value, dict):
        return {str(key): json_safe(child) for key, child in value.items()}
    if isinstance(value, list):
        return [json_safe(child) for child in value]
    return value


def sanitize_text(value: Any) -> str:
    text = str(json_safe(value) if value is not None else "")
    text = PRIVATE_PATH_RE.sub("[private-path-redacted]", text)
    text = CREDENTIAL_RE.sub("[credential-redacted]", text)
    return text


def classify_ref(ref: str) -> str:
    if ref.startswith(("http://", "https://")):
        return "url"
    return "repo_path"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def build_evidence_board(root: Path) -> dict[str, Any]:
    source_path = root / "PUBLIC" / "claim_evidence_matrix.yaml"
    matrix = load_instance(source_path)
    claims = matrix.get("claims", []) if isinstance(matrix, dict) else []

    rows: list[dict[str, Any]] = []
    status_counts: dict[str, int] = {}
    repo_refs = 0
    url_refs = 0
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        evidence = [sanitize_text(item) for item in claim.get("evidence", [])]
        counterevidence = [sanitize_text(item) for item in claim.get("counterevidence", [])]
        public_evidence = [{"kind": classify_ref(item), "ref": item} for item in evidence]
        repo_refs += sum(1 for item in public_evidence if item["kind"] == "repo_path")
        url_refs += sum(1 for item in public_evidence if item["kind"] == "url")
        status = sanitize_text(claim.get("status", "draft"))
        status_counts[status] = status_counts.get(status, 0) + 1
        rows.append(
            {
                "claim_id": sanitize_text(claim.get("id", "")),
                "status": status,
                "claim": sanitize_text(claim.get("claim", "")),
                "evidence_count": len(evidence),
                "evidence": public_evidence,
                "counterevidence_count": len(counterevidence),
                "counterevidence": counterevidence,
                "dissemination_targets": [
                    sanitize_text(item) for item in claim.get("dissemination_targets", [])
                ],
                "privacy_level": sanitize_text(claim.get("privacy_level", "public")),
            }
        )

    return {
        "schema_version": "v1.0",
        "updated_at": now_iso(),
        "source_policy": "sanitized_public_summary_only",
        "source": "PUBLIC/claim_evidence_matrix.yaml",
        "summary": {
            "total_claims": len(rows),
            "status_counts": status_counts,
            "repository_evidence_refs": repo_refs,
            "external_evidence_refs": url_refs,
        },
        "rows": rows,
        "deferred_scope_note": "This is a readable claim/evidence board, not a knowledge graph or autonomous hypothesis backlog.",
    }


def summarize_resource_ledger(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = 0.0
    latest_entry = rows[-1] if rows else {}
    for row in rows:
        amount = row.get("amount", 0)
        if isinstance(amount, int | float):
            total += float(amount)
    return {
        "ledger_entries": len(rows),
        "total_recorded_amount": total,
        "currency_or_unit": sanitize_text(latest_entry.get("currency_or_unit", "CNY") if rows else "CNY"),
        "latest_entry_id": sanitize_text(latest_entry.get("entry_id", "") if rows else ""),
        "resource_policy": "local zero-cost validation unless a researcher-approved work order says otherwise",
    }


def summarize_manifest(rows: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for row in rows[-limit:]:
        errors = row.get("errors", [])
        summaries.append(
            {
                "run_id": sanitize_text(row.get("run_id", "")),
                "timestamp": sanitize_text(row.get("timestamp", "")),
                "work_order_id": sanitize_text(row.get("work_order_id", "")),
                "status": sanitize_text(row.get("status", "")),
                "command_or_tool": sanitize_text(row.get("command_or_tool", "")),
                "outputs_count": len(row.get("outputs", []) or []),
                "privacy_level": sanitize_text(row.get("privacy_level", "public")),
                "error_count": len(errors or []),
            }
        )
    return summaries


def summarize_experiment_run(path: Path) -> dict[str, Any] | None:
    try:
        run = load_instance(path)
    except Exception:
        return None
    if not isinstance(run, dict):
        return None
    replay = run.get("replay", {}) if isinstance(run.get("replay"), dict) else {}
    failure = run.get("failure", {}) if isinstance(run.get("failure"), dict) else {}
    environment = run.get("environment", {}) if isinstance(run.get("environment"), dict) else {}
    return {
        "experiment_id": sanitize_text(run.get("experiment_id", path.parent.name)),
        "status": sanitize_text(run.get("status", "planned")),
        "command_or_adapter": sanitize_text(environment.get("kind", "local-static-fixture")),
        "inputs": [sanitize_text(item) for item in replay.get("inputs", [])],
        "outputs": [sanitize_text(item) for item in run.get("artifacts", [])],
        "metrics": [sanitize_text(item) for item in run.get("measurements", [])],
        "resource_use": sanitize_text(environment.get("resource_policy", "0 CNY; local validation only")),
        "failure_class": sanitize_text(failure.get("class", "not_run")),
        "replay_command": sanitize_text(replay.get("command", "")),
        "human_decision_required": run.get("status") in {"approved", "queued", "running", "needs_human_review"},
    }


def build_run_monitor(root: Path) -> dict[str, Any]:
    manifest_rows = load_jsonl(root / "PROVENANCE" / "run_manifest.jsonl")
    ledger_rows = load_jsonl(root / "PROVENANCE" / "resource_ledger.jsonl")
    experiment_rows: list[dict[str, Any]] = []
    experiments_root = root / "RUNS" / "experiments"
    if experiments_root.exists():
        for path in sorted(experiments_root.glob("*/run.yaml")):
            summary = summarize_experiment_run(path)
            if summary:
                experiment_rows.append(summary)

    return {
        "schema_version": "v1.1",
        "updated_at": now_iso(),
        "source_policy": "sanitized_public_summary_only",
        "runs": experiment_rows,
        "audit_runs": summarize_manifest(manifest_rows),
        "resource_summary": summarize_resource_ledger(ledger_rows),
        "deferred_p2": [
            "hypothesis backlog",
            "critic/evolution loops",
            "knowledge graph",
            "real experiment queue",
            "external adapter execution",
        ],
    }


def validate_no_sensitive_text(path: str, payload: Any) -> None:
    text = json.dumps(payload, ensure_ascii=False)
    if PRIVATE_PATH_RE.search(text):
        raise ValueError(f"{path} contains a PRIVATE path")
    if CREDENTIAL_RE.search(text):
        raise ValueError(f"{path} contains credential-like text")


def validate_summary_files(root: Path) -> list[str]:
    checks = [
        ("PUBLIC/evidence_board.json", ["schema_version", "summary", "rows"]),
        ("PUBLIC/run_monitor.json", ["schema_version", "runs", "audit_runs", "resource_summary"]),
    ]
    messages: list[str] = []
    for rel, required_keys in checks:
        path = root / rel
        if not path.exists():
            raise ValueError(f"Missing public summary: {rel}")
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        for key in required_keys:
            if key not in payload:
                raise ValueError(f"{rel} missing required key: {key}")
        validate_no_sensitive_text(rel, payload)
        messages.append(f"Public summary OK: {rel}")

    evidence = json.loads((root / "PUBLIC" / "evidence_board.json").read_text(encoding="utf-8-sig"))
    if not evidence.get("rows"):
        raise ValueError("PUBLIC/evidence_board.json must contain at least one row")
    monitor = json.loads((root / "PUBLIC" / "run_monitor.json").read_text(encoding="utf-8-sig"))
    if not monitor.get("runs"):
        raise ValueError("PUBLIC/run_monitor.json must contain at least one run summary")
    return messages


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_summaries(root: Path) -> list[str]:
    evidence = build_evidence_board(root)
    monitor = build_run_monitor(root)
    validate_no_sensitive_text("PUBLIC/evidence_board.json", evidence)
    validate_no_sensitive_text("PUBLIC/run_monitor.json", monitor)
    write_json(root / "PUBLIC" / "evidence_board.json", evidence)
    write_json(root / "PUBLIC" / "run_monitor.json", monitor)
    return [
        "Wrote PUBLIC/evidence_board.json",
        "Wrote PUBLIC/run_monitor.json",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Research OS repository root")
    parser.add_argument("--write", action="store_true", help="Write sanitized public summaries")
    parser.add_argument("--check", action="store_true", help="Validate existing sanitized public summaries")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        messages: list[str] = []
        if args.write or not args.check:
            messages.extend(write_summaries(root))
        if args.check:
            messages.extend(validate_summary_files(root))
    except Exception as exc:  # noqa: BLE001 - CLI should return clear validation errors.
        print(f"Public summary build/check failed: {exc}", file=sys.stderr)
        return 1
    for message in messages:
        print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
