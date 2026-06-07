#!/usr/bin/env python3
"""Run local Research OS regression evals without external resources."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(root: Path, command: list[str]) -> None:
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    scripts = [
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "scripts/check_strict_schema_instances.ps1"],
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "scripts/check_html_docs.ps1"],
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "scripts/check_eval_fixtures.ps1"],
    ]
    for command in scripts:
        run(root, command)
    print("Research OS local evals passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
