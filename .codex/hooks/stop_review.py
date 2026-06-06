#!/usr/bin/env python3
"""Example Research OS Stop hook."""

from pathlib import Path
import sys


required = [
    Path("AGENTS.md"),
    Path("CONTROL/work_order.yaml"),
    Path("CONTROL/phase_gate.yaml"),
    Path("PROVENANCE/run_manifest.jsonl"),
    Path("PROVENANCE/resource_ledger.jsonl"),
]

missing = [str(path) for path in required if not path.exists()]
if missing:
    print("Research OS stop check: missing required audit files: " + ", ".join(missing))
    sys.exit(1)

print("Research OS stop check passed. Review git status, gap audit, and phase gate before final response.")
sys.exit(0)
