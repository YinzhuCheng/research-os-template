#!/usr/bin/env python3
"""Example Research OS PostToolUse hook."""

import json
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

sys.exit(0)
