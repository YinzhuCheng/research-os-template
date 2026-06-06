#!/usr/bin/env python3
"""Example Research OS PreToolUse hook.

The script is conservative and intended as a template. It exits non-zero for
obvious policy violations and prints actionable guidance for confirmation cases.
"""

import json
import re
import sys


def read_payload() -> str:
    try:
        return sys.stdin.read()
    except Exception:
        return ""


payload_text = read_payload()
try:
    payload = json.loads(payload_text) if payload_text.strip() else {}
except json.JSONDecodeError:
    payload = {"raw": payload_text}

haystack = json.dumps(payload, ensure_ascii=False).lower()

hard_denies = {
    "external writeback": r"\b(git\s+push|gh\s+pr\s+create|gh\s+release|curl\s+.*\b(upload|post)\b|scp\s+|rsync\s+.*:)",
    "destructive reset": r"\b(git\s+reset\s+--hard|git\s+checkout\s+--|remove-item\s+.*-recurse|rm\s+-rf)\b",
    "credential literal": r"(authorization:\s*bearer|api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}|password\s*[:=]\s*['\"][^'\"]{8,})",
    "private secret write": r"private[\\/]+secrets[\\/]+(?!readme\.md|\.gitkeep)",
}

for label, pattern in hard_denies.items():
    if re.search(pattern, haystack, flags=re.IGNORECASE):
        print(f"Research OS policy blocked tool use: {label}. Require explicit human approval and a work order update.")
        sys.exit(2)

confirmation_patterns = {
    "cloud or remote shell": r"\b(aws|gcloud|az|ssh|kubectl|terraform|docker\s+push)\b",
    "public export": r"\b(export_public|zip|tar)\b",
    "resource spending": r"\b(openai|anthropic|deepseek|kimi|api call|gpu|cloud instance)\b",
}

for label, pattern in confirmation_patterns.items():
    if re.search(pattern, haystack, flags=re.IGNORECASE):
        print(f"Research OS policy notice: {label} may require confirmation, resource ledger, and manifest entry.")

sys.exit(0)
