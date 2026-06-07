from __future__ import annotations

import json
import queue
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from research_os_sidecar.approval_service import ApprovalService
from research_os_sidecar.profile_service import ProfileService
from research_os_sidecar.project_service import ProjectService
from research_os_sidecar.security import SecurityError, resolve_under


def make_template(root: Path) -> None:
    for directory in ["CONTROL", "config", "docs", "PUBLIC", "scripts", "skills", "templates"]:
        (root / directory).mkdir(parents=True, exist_ok=True)
        (root / directory / "README.md").write_text(f"# {directory}\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("rules\n", encoding="utf-8")
    (root / "README.md").write_text("# template\n", encoding="utf-8")
    (root / "config" / "research_project.yaml").write_text(
        'current_macro_phase: initialization\ncurrent_phase: initialization_intake\n',
        encoding="utf-8",
    )
    (root / "PRIVATE").mkdir()
    (root / "PRIVATE" / "secret.txt").write_text("token=SHOULD_NOT_COPY\n", encoding="utf-8")


class SidecarServiceTests(unittest.TestCase):
    def test_project_create_open_and_seed_excludes_private(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            service = ProjectService(template)
            project = service.create_project("Demo", base / "demo.rosproj")

            project_file = Path(project["project_file"])
            project_root = Path(project["project_root"])
            self.assertTrue(project_file.exists())
            self.assertTrue((project_root / "CONTROL").exists())
            self.assertTrue((project_root / "PRIVATE").exists())
            self.assertFalse((project_root / "PRIVATE" / "secret.txt").exists())
            reopened = service.open_project(project_file)
            self.assertEqual(reopened["schema_version"], "research-os-project-v1")
            self.assertNotIn("api_key", json.dumps(reopened).lower())

    def test_project_path_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(SecurityError):
                resolve_under(root, root.parent / "outside.txt")

    def test_profile_rejects_secret_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            profiles = ProfileService(Path(temp) / "profiles.json")
            with self.assertRaises(ValueError):
                profiles.upsert_profile(
                    {
                        "profile_id": "bad",
                        "label": "Bad",
                        "type": "openai_api_key",
                        "api_key": "sk-test",
                    }
                )

    def test_approval_times_out_to_decline(self) -> None:
        approvals = ApprovalService(timeout_seconds=0.01)
        result = approvals.request_approval(None, "item/commandExecution/requestApproval", {"command": "git push"})
        self.assertEqual(result["decision"], "decline")

    def test_approval_can_be_accepted_by_ui_decision(self) -> None:
        approvals = ApprovalService(timeout_seconds=1.0)
        results: "queue.Queue[dict]" = queue.Queue()

        def worker() -> None:
            results.put(approvals.request_approval(None, "item/commandExecution/requestApproval", {"command": "git status"}))

        thread = threading.Thread(target=worker)
        thread.start()
        pending = approvals.list_pending()["approvals"]
        self.assertEqual(len(pending), 1)
        approvals.decide(pending[0]["approval_id"], "accept")
        thread.join(timeout=2)
        self.assertEqual(results.get_nowait()["decision"], "accept")


if __name__ == "__main__":
    unittest.main()
