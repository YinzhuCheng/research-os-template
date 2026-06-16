#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "build_public_summaries.py"


def load_summary_tool():
    tools_dir = str(ROOT / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    spec = importlib.util.spec_from_file_location("build_public_summaries", TOOL_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicSummaryTests(unittest.TestCase):
    def test_generated_public_summaries_are_sanitized_and_nonempty(self) -> None:
        tool = load_summary_tool()
        evidence = tool.build_evidence_board(ROOT)
        monitor = tool.build_run_monitor(ROOT)

        self.assertGreaterEqual(evidence["summary"]["total_claims"], 1)
        self.assertGreaterEqual(len(evidence["rows"]), 1)
        self.assertGreaterEqual(len(monitor["runs"]), 1)
        self.assertIn("audit_runs", monitor)
        self.assertIn("resource_summary", monitor)
        tool.validate_no_sensitive_text("evidence", evidence)
        tool.validate_no_sensitive_text("monitor", monitor)

    def test_sensitive_text_is_rejected(self) -> None:
        tool = load_summary_tool()
        with self.assertRaises(ValueError):
            tool.validate_no_sensitive_text("bad", {"path": "PRIVATE/intake/raw.txt"})
        with self.assertRaises(ValueError):
            tool.validate_no_sensitive_text("bad", {"header": "Authorization: Bearer abcdefghijk"})

    def test_existing_public_summary_files_validate(self) -> None:
        tool = load_summary_tool()
        messages = tool.validate_summary_files(ROOT)
        self.assertIn("Public summary OK: PUBLIC/evidence_board.json", messages)
        self.assertIn("Public summary OK: PUBLIC/run_monitor.json", messages)


if __name__ == "__main__":
    unittest.main()
