#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / ".agents" / "plugins" / "plugins" / "research-os-copilot" / "scripts" / "research_os_copilot_server.py"


def load_server_module():
    spec = importlib.util.spec_from_file_location("research_os_copilot_server", SERVER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CopilotPrivacyTests(unittest.TestCase):
    def test_raw_free_text_only_goes_to_private_runtime_path(self) -> None:
        module = load_server_module()
        sentinel = "RAW_SENTINEL_DO_NOT_LEAK_123456"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONTROL").mkdir()
            (root / "CONTROL" / "work_order.yaml").write_text("work_order_id: WO-TEST\n", encoding="utf-8")
            (root / "PUBLIC").mkdir()
            (root / "PUBLIC" / "copilot_state.json").write_text("{}", encoding="utf-8")
            (root / "PROVENANCE").mkdir()
            store = module.CopilotStore(root)

            packet = store.save_intake({"session_id": "INTAKE-test-001", "free_text": f"{sentinel} https://example.org/note"}, [])

            self.assertNotIn("free_text", packet)
            self.assertNotIn(sentinel, json.dumps(packet, ensure_ascii=False))
            self.assertIn("free_text_sha256", packet)
            self.assertTrue((root / "PRIVATE" / "intake" / "INTAKE-test-001" / "free_text.md").exists())

            control_text = (root / "CONTROL" / "copilot_inbox" / "INTAKE-test-001.intake.json").read_text(encoding="utf-8")
            public_text = (root / "PUBLIC" / "copilot_state.json").read_text(encoding="utf-8")
            self.assertNotIn(sentinel, control_text)
            self.assertNotIn(sentinel, public_text)
            self.assertIn('"fetch_authorized": false', control_text)

    def test_answers_confirmation_and_session_state_are_sanitized(self) -> None:
        module = load_server_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONTROL").mkdir()
            (root / "CONTROL" / "work_order.yaml").write_text("work_order_id: WO-TEST\n", encoding="utf-8")
            (root / "PUBLIC").mkdir()
            (root / "PUBLIC" / "copilot_state.json").write_text('{"active_session_id":"INTAKE-test-002"}', encoding="utf-8")
            (root / "PUBLIC" / "run_monitor.json").write_text('{"runs":[]}', encoding="utf-8")
            (root / "PROVENANCE").mkdir()
            store = module.CopilotStore(root)

            answers = store.save_answers(
                {
                    "session_id": "INTAKE-test-002",
                    "question_packet_id": "QPACK-test",
                    "answers": [
                        {"question_id": "Q-01", "selected_option": "A", "free_text_other": ""},
                        {"question_id": "Q-02", "selected_option": "B", "free_text_other": "custom"},
                        {"question_id": "Q-03", "selected_option": "C", "free_text_other": ""},
                    ],
                }
            )
            confirmation = store.save_confirmation(
                {
                    "session_id": "INTAKE-test-002",
                    "confirmed": True,
                    "requires_work_order": True,
                    "next_action": "Generate initialization report after Codex review.",
                    "notes": "ok",
                }
            )
            session = store.session_state("INTAKE-test-002")

            self.assertEqual(answers["status"], "answers_received")
            self.assertEqual(confirmation["status"], "confirmed")
            self.assertTrue(session["packets"]["answers"])
            self.assertTrue(session["packets"]["confirmation"])
            serialized = json.dumps(session, ensure_ascii=False)
            self.assertNotIn("PRIVATE", serialized)


if __name__ == "__main__":
    unittest.main()
