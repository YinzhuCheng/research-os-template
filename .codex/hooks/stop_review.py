#!/usr/bin/env python3
"""Example Research OS Stop hook."""

from pathlib import Path
import shutil
import subprocess
import sys


def repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current, *current.parents]:
        if (parent / "CONTROL" / "work_order.yaml").exists():
            return parent
    return Path.cwd().resolve()


def run_check(root: Path, script: str, *args: str) -> None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if shell is None:
        raise SystemExit("Research OS stop check failed: neither pwsh nor powershell is available.")
    command = [
        shell,
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(root / script),
        *args,
    ]
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        print(result.stdout.strip())
        print(result.stderr.strip())
        raise SystemExit(f"Research OS stop check failed: {script}")


ROOT = repo_root()
required = [
    ROOT / "AGENTS.md",
    ROOT / "CONTROL" / "work_order.yaml",
    ROOT / "CONTROL" / "phase_gate.yaml",
    ROOT / "PROVENANCE" / "run_manifest.jsonl",
    ROOT / "PROVENANCE" / "resource_ledger.jsonl",
]

missing = [str(path) for path in required if not path.exists()]
if missing:
    print("Research OS stop check: missing required audit files: " + ", ".join(missing))
    sys.exit(1)

for script, args in [
    ("scripts/check_strict_schema_instances.ps1", []),
    ("scripts/check_public_summaries.ps1", []),
    ("scripts/check_private_intake_synthetic.ps1", []),
    ("scripts/check_html_docs.ps1", []),
    ("scripts/scan_privacy.ps1", ["-Paths", "PUBLIC", "PROVENANCE"]),
    ("scripts/check_package_artifacts.ps1", []),
    ("scripts/check_harness.ps1", []),
]:
    run_check(ROOT, script, *args)

phase_text = (ROOT / "CONTROL" / "phase_gate.yaml").read_text(encoding="utf-8")
work_text = (ROOT / "CONTROL" / "work_order.yaml").read_text(encoding="utf-8")
if "current_phase:" not in phase_text or "work_order_id:" not in work_text:
    print("Research OS stop check: phase gate or work order is missing canonical fields.")
    sys.exit(1)

print("Research OS stop check passed. Review git status, gap audit, and phase gate before final response.")
sys.exit(0)
