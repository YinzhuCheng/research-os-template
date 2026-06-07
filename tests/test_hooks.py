#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".codex" / "hooks" / "pre_tool_use_policy.py"


class HookPolicyTests(unittest.TestCase):
    def run_hook(self, payload: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )

    def test_blocks_external_writeback(self) -> None:
        result = self.run_hook({"tool": "shell_command", "command": "git push origin main"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("external writeback", result.stdout.lower())

    def test_blocks_credential_literal(self) -> None:
        result = self.run_hook({"tool": "shell_command", "command": "curl -H 'Authorization: Bearer abcdefghijklmnopqrs'"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("credential", result.stdout.lower())

    def test_allows_read_command(self) -> None:
        result = self.run_hook({"tool": "shell_command", "command": "Get-Content CONTROL/work_order.yaml"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
