#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.validate_repo import ValidationError, parse_yaml_text, run  # noqa: E402


class SchemaInstanceTests(unittest.TestCase):
    def test_repo_instances_validate(self) -> None:
        messages = run(ROOT)
        self.assertIn("Strict Research OS schema validation passed.", messages[-1])

    def test_unquoted_yaml_date_is_not_a_string(self) -> None:
        parsed = parse_yaml_text("created_at: 2026-06-06\n")
        with self.assertRaises(ValidationError):
            from tools.validate_repo import validate_value

            validate_value(parsed["created_at"], {"type": "string"}, {"type": "string"}, "created_at")


if __name__ == "__main__":
    unittest.main()
