#!/usr/bin/env python3
"""Example Research OS PostToolUse hook."""

import json
from pathlib import Path
import sys


payload_text = sys.stdin.read()
try:
    payload = json.loads(payload_text) if payload_text.strip() else {}
except json.JSONDecodeError:
    payload = {"raw": payload_text}

text = json.dumps(payload, ensure_ascii=False).lower()
if "failed" in text or "error" in text or "exception" in text:
    print("Research OS notice: tool output indicates failure. Record status, errors, and next action in PROVENANCE/run_manifest.jsonl.")

if "public" in text or "export" in text:
    print("Research OS notice: run scripts/scan_privacy.ps1 before any public export.")

if "cost" in text or "budget" in text or "resource" in text:
    print("Research OS notice: update PROVENANCE/resource_ledger.jsonl if real resources were consumed.")

root = Path(__file__).resolve()
for parent in [root, *root.parents]:
    if (parent / "CONTROL" / "work_order.yaml").exists():
        root = parent
        break
if isinstance(root, Path) and (root / "PUBLIC" / "copilot.html").exists():
    html = (root / "PUBLIC" / "copilot.html").read_text(encoding="utf-8")
    close = html.lower().rfind("</html>")
    if close >= 0 and html[close + 7 :].strip():
        print("Research OS notice: PUBLIC/copilot.html has content after </html>; run scripts/check_html_docs.ps1.")

sys.exit(0)
