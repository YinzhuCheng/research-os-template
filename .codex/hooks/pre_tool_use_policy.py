#!/usr/bin/env python3
"""Example Research OS PreToolUse hook.

The script is conservative and intended as a template. It exits non-zero for
obvious policy violations and prints actionable guidance for confirmation cases.
"""

import json
from pathlib import Path
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
command_text = str(payload.get("command") or payload.get("cmd") or payload.get("arguments", {}).get("command") or "")
tool_name = str(payload.get("tool") or payload.get("tool_name") or payload.get("name") or "")
cwd_text = str(payload.get("cwd") or payload.get("workdir") or payload.get("arguments", {}).get("workdir") or "")


def repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current, *current.parents]:
        if (parent / "CONTROL" / "work_order.yaml").exists():
            return parent
    return Path.cwd().resolve()


def normalized_payload_text() -> str:
    parts = [haystack, command_text.lower(), tool_name.lower(), cwd_text.lower()]
    return "\n".join(parts)


text = normalized_payload_text()

hard_denies = {
    "external writeback": r"\b(git\s+push|gh\s+pr\s+create|gh\s+release|curl\s+.*\b(upload|post)\b|scp\s+|rsync\s+.*:)",
    "destructive reset": r"\b(git\s+reset\s+--hard|git\s+checkout\s+--|remove-item\s+.*-recurse|rm\s+-rf)\b",
    "credential literal": r"(authorization:\s*bearer|api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}|password\s*[:=]\s*['\"][^'\"]{8,})",
    "private secret write": r"private[\\/]+secrets[\\/]+(?!readme\.md|\.gitkeep)",
}

for label, pattern in hard_denies.items():
    if re.search(pattern, text, flags=re.IGNORECASE):
        print(f"Research OS policy blocked tool use: {label}. Require explicit human approval and a work order update.")
        sys.exit(2)

confirmation_patterns = {
    "cloud or remote shell": r"\b(aws|gcloud|az|ssh|kubectl|terraform|docker\s+push)\b",
    "public export": r"\b(export_public|zip|tar)\b",
    "resource spending": r"\b(openai|anthropic|deepseek|kimi|api call|gpu|cloud instance)\b",
}

for label, pattern in confirmation_patterns.items():
    if re.search(pattern, text, flags=re.IGNORECASE):
        print(f"Research OS policy notice: {label} may require confirmation, resource ledger, and manifest entry.")

root = repo_root()
if command_text:
    if re.search(r"\b(PROVENANCE[\\/]+run_manifest\.jsonl)\b", command_text, flags=re.IGNORECASE):
        pass
    if re.search(r"\b(add-content|set-content|out-file)\b.*PUBLIC[\\/].*\.html", command_text, flags=re.IGNORECASE):
        print("Research OS policy notice: HTML writes must pass scripts/check_html_docs.ps1 to catch trailing content.")
    if "PRIVATE" in command_text and "PRIVATE\\secrets" not in command_text and "PRIVATE/secrets" not in command_text:
        print("Research OS policy notice: PRIVATE access requires an active work order and should not be committed.")

if not (root / "CONTROL" / "phase_gate.yaml").exists():
    print("Research OS policy blocked tool use: CONTROL/phase_gate.yaml is missing.")
    sys.exit(2)

sys.exit(0)
