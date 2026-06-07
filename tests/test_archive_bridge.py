#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
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


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return result.stdout.strip()


def seed_repo(root: Path) -> None:
    (root / "CONTROL").mkdir()
    (root / "CONTROL" / "work_order.yaml").write_text("work_order_id: WO-TEST\n", encoding="utf-8")
    (root / "CONTROL" / "phase_gate.yaml").write_text("current_phase: research-os-v3.9\n", encoding="utf-8")
    (root / "config").mkdir()
    (root / "config" / "research_project.yaml").write_text(
        "current_macro_phase: research_loop\ncurrent_phase: loop_acceptance_gate\n",
        encoding="utf-8",
    )
    (root / "PUBLIC").mkdir()
    (root / "PUBLIC" / "copilot_state.json").write_text("{}", encoding="utf-8")
    (root / "PUBLIC" / "archive_index.json").write_text('{"archives":[]}\n', encoding="utf-8")
    (root / "PROVENANCE").mkdir()
    git(root, "init")
    git(root, "add", ".")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "seed")


class ArchiveBridgeTests(unittest.TestCase):
    def test_create_archive_commits_snapshot_and_public_index(self) -> None:
        module = load_server_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_repo(root)
            store = module.CopilotStore(root)
            (root / "PUBLIC" / "note.md").write_text("accepted artifact summary\n", encoding="utf-8")

            preview = store.archive_preview()
            self.assertTrue(preview["dirty"])
            self.assertIn("PUBLIC/note.md", preview["changed_paths"])

            record = store.create_archive({"description": "accepted loop artifact", "macro_phase": "research_loop"})
            self.assertEqual(record["status"], "created")
            self.assertEqual(record["phase"], "loop_acceptance_gate")
            self.assertIn("PUBLIC/note.md", record["changed_paths"])
            self.assertIn("index_commit", record)

            public_index = json.loads((root / "PUBLIC" / "archive_index.json").read_text(encoding="utf-8"))
            self.assertEqual(len(public_index["archives"]), 1)
            self.assertEqual(public_index["archives"][0]["description"], "accepted loop artifact")
            self.assertNotIn("PRIVATE", json.dumps(public_index, ensure_ascii=False))
            self.assertEqual(git(root, "status", "--porcelain"), "")

    def test_archive_rejects_private_path(self) -> None:
        module = load_server_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_repo(root)
            (root / "PRIVATE").mkdir()
            (root / "PRIVATE" / "secret.txt").write_text("private note\n", encoding="utf-8")
            store = module.CopilotStore(root)

            with self.assertRaises(ValueError):
                store.create_archive({"description": "should fail"})


if __name__ == "__main__":
    unittest.main()
