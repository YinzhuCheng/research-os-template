from __future__ import annotations

import json
import os
import queue
import shutil
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from research_os_sidecar.approval_service import ApprovalService
from research_os_sidecar.archive_service import ArchiveService
from research_os_sidecar.paper_artifact_service import PaperArtifactService
from research_os_sidecar.profile_service import ProfileService
from research_os_sidecar.project_service import ProjectService
from research_os_sidecar.research_loop_artifact_service import ResearchLoopArtifactService
from research_os_sidecar.runtime_config_service import RuntimeConfigService
from research_os_sidecar.runtime_service import RuntimeService
from research_os_sidecar.security import SecurityError, import_directory_to_project, resolve_under
from research_os_sidecar.state_service import ResearchStateService


def make_template(root: Path) -> None:
    legacy = "copilot"
    for directory in ["CONTROL", "config", "docs", "PUBLIC", "scripts", "skills", "templates"]:
        (root / directory).mkdir(parents=True, exist_ok=True)
        (root / directory / "README.md").write_text(f"# {directory}\n", encoding="utf-8")
    (root / "PUBLIC" / "research_state.json").write_text('{"schema_version":"research-state-v1"}\n', encoding="utf-8")
    (root / "PUBLIC" / f"{legacy}.html").write_text("old browser ui\n", encoding="utf-8")
    (root / "PUBLIC" / f"{legacy}_state.json").write_text("{}\n", encoding="utf-8")
    (root / "scripts" / f"check_{legacy}_bridge.ps1").write_text("old check\n", encoding="utf-8")
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
            self.assertTrue((project_root / "CONTROL" / "intake_queue").exists())
            self.assertTrue((project_root / "PRIVATE").exists())
            self.assertTrue((project_root / "PUBLIC" / "research_state.json").exists())
            legacy = "copilot"
            self.assertFalse((project_root / "PUBLIC" / f"{legacy}.html").exists())
            self.assertFalse((project_root / "PUBLIC" / f"{legacy}_state.json").exists())
            self.assertFalse((project_root / "scripts" / f"check_{legacy}_bridge.ps1").exists())
            self.assertFalse((project_root / "PRIVATE" / "secret.txt").exists())
            generated_agents = (project_root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("whole-folder material manifest", generated_agents)
            self.assertIn("Do not invent citations", generated_agents)
            self.assertIn("research-os-execution-harness", generated_agents)
            self.assertTrue((project_root / "CONTROL" / "project_context.md").exists())
            (project_root / "AGENTS.md").write_text("legacy context\n", encoding="utf-8")
            reopened = service.open_project(project_file)
            self.assertEqual(reopened["schema_version"], "research-os-project-v1")
            refreshed_agents = (project_root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Structured Research Plan", refreshed_agents)
            self.assertIn("Do not invent citations", refreshed_agents)
            self.assertNotIn("api_key", json.dumps(reopened).lower())

    def test_desktop_intake_and_choice_response_use_new_state_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            state = ResearchStateService(projects.require_project_root)

            intake = state.submit_intake({"free_text": "private research plan"})
            self.assertTrue((root / "PUBLIC" / "research_state.json").exists())
            self.assertTrue((root / "CONTROL" / "intake_queue" / f"{intake['packet']['session_id']}.intake.json").exists())
            self.assertTrue((root / "PRIVATE" / "intake" / intake["packet"]["session_id"] / "free_text.md").exists())
            self.assertFalse((root / "CONTROL" / ("copilot" + "_inbox")).exists())

            response = state.submit_choice_response({"prompt_id": "CP-1", "option_id": "balanced", "free_form": "keep software"})
            self.assertTrue((root / "CONTROL" / "choice_responses" / f"{response['response_id']}.json").exists())
            readback = state.read_state()
            self.assertIn("research_state", readback)
            self.assertIn("submission_workflow", readback)
            self.assertNotIn("copilot" + "_state", readback)

    def test_choice_response_ids_are_unique_inside_one_second(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            state = ResearchStateService(projects.require_project_root)

            responses = [
                state.submit_choice_response({"prompt_id": f"CP-{index}", "option_id": "balanced", "free_form": ""})
                for index in range(3)
            ]
            ids = [item["response_id"] for item in responses]
            self.assertEqual(len(ids), len(set(ids)))
            for response_id in ids:
                self.assertTrue((root / "CONTROL" / "choice_responses" / f"{response_id}.json").exists())

    def test_workflow_gap_is_recorded_in_provenance_and_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            state = ResearchStateService(projects.require_project_root)

            gap = state.record_workflow_gap({"description": "source verification table needs per-reference acceptance"})
            self.assertEqual(gap["status"], "recorded")
            self.assertTrue((root / "PROVENANCE" / "app_workflow_gaps.jsonl").exists())
            readback = state.read_state()
            gaps = readback["submission_workflow"]["workflow_gaps"]
            self.assertEqual(gaps[-1]["description"], "source verification table needs per-reference acceptance")

    def test_research_plan_write_moves_to_acceptance_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            state = ResearchStateService(projects.require_project_root, projects.update_project)

            result = state.write_research_plan(
                {
                    "summary": "folder-wide plan",
                    "content": "# Research Plan\n\nUse the full material manifest before writing.",
                    "next_actions": ["verify sources", "audit proof"],
                }
            )

            self.assertEqual(result["state"]["internal_phase"], "loop_acceptance_gate")
            self.assertTrue((root / "PUBLIC" / "research_plan.md").exists())
            self.assertTrue((root / "PUBLIC" / "research_plan.json").exists())
            prompts = result["state"]["choice_prompts"]
            self.assertEqual(prompts[0]["prompt_id"], "CP-RESEARCH-PLAN-ACCEPTANCE")
            readback = json.loads(Path(project["project_file"]).read_text(encoding="utf-8"))
            self.assertEqual(readback["current_macro_phase"], "research_loop")
            self.assertEqual(readback["current_phase"], "loop_acceptance_gate")

            with self.assertRaises(SecurityError):
                state.write_research_plan({"content": "api_key=secret"})

            state.submit_choice_response(
                {
                    "prompt_id": "CP-RESEARCH-PLAN-ACCEPTANCE",
                    "option_id": "accept_with_audit",
                    "free_form": "Accept the plan and start with source/proof/novelty audit.",
                }
            )
            accepted = state.read_state()["research_state"]
            self.assertEqual(accepted["internal_phase"], "loop_plan_alignment")
            self.assertEqual(accepted["choice_prompts"][0]["prompt_id"], "CP-FIRST-RESEARCH-LOOP")
            readback = json.loads(Path(project["project_file"]).read_text(encoding="utf-8"))
            self.assertEqual(readback["current_phase"], "loop_plan_alignment")

    def test_final_product_selection_syncs_project_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            state = ResearchStateService(projects.require_project_root, projects.update_project)

            state.select_final_products(["paper"], "prepare a submission package")

            project_file = Path(project["project_file"])
            readback = json.loads(project_file.read_text(encoding="utf-8"))
            self.assertEqual(readback["current_macro_phase"], "final_product")
            self.assertEqual(readback["current_phase"], "final_product_selection")
            mirror = json.loads((Path(project["project_root"]) / ".research-os" / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(mirror["current_macro_phase"], "final_product")

    def test_paper_artifact_service_writes_public_submission_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            service = PaperArtifactService(projects.require_project_root)

            result = service.write_artifacts(
                {
                    "summary": "draft paper package",
                    "workflow_updates": {
                        "status": "submission_package_draft_written",
                        "source_verification": [
                            {"id": "SRC-GUIDE", "label": "Guide", "status": "verified"},
                        ],
                        "proof_audit": [
                            {"id": "PROOF-MODEL", "label": "Model", "status": "accepted"},
                        ],
                    },
                    "files": [
                        {"path": "PUBLIC/paper/main.tex", "content": "\\section{Test}\n", "role": "manuscript"},
                        {"path": "PUBLIC/submission/highlights.txt", "content": "Highlight one\n", "role": "submission"},
                    ],
                }
            )
            self.assertEqual(len(result["written"]), 2)
            self.assertTrue((root / "PUBLIC" / "paper" / "main.tex").exists())
            self.assertTrue((root / "PUBLIC" / "submission" / "highlights.txt").exists())
            readback = json.loads((root / "PUBLIC" / "research_state.json").read_text(encoding="utf-8"))
            artifacts = readback["submission_workflow"]["artifact_status"]
            self.assertIn("PUBLIC/paper/main.tex", {item["path"] for item in artifacts})
            self.assertEqual(readback["submission_workflow"]["status"], "submission_package_draft_written")
            self.assertEqual(readback["submission_workflow"]["source_verification"][0]["status"], "verified")
            self.assertEqual(readback["submission_workflow"]["proof_audit"][0]["status"], "accepted")

    def test_paper_artifact_service_syncs_project_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            service = PaperArtifactService(projects.require_project_root, projects.update_project)

            service.write_artifacts(
                {
                    "summary": "paper iteration",
                    "files": [{"path": "PUBLIC/paper/main.tex", "content": "\\section{Test}\n", "role": "manuscript"}],
                }
            )

            readback = json.loads(Path(project["project_file"]).read_text(encoding="utf-8"))
            self.assertEqual(readback["current_macro_phase"], "final_product")
            self.assertEqual(readback["current_phase"], "final_product_production")

    def test_research_loop_artifact_service_preserves_loop_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            loop_artifacts = ResearchLoopArtifactService(projects.require_project_root, projects.update_project)

            result = loop_artifacts.write_artifacts(
                {
                    "summary": "source and proof audit",
                    "workflow_updates": {
                        "status": "source_proof_audit_ready",
                        "venue_requirements": [{"id": "VENUE-1", "label": "Guide", "status": "verified"}],
                        "source_verification": [{"id": "SRC-1", "label": "Reference", "status": "verified"}],
                        "proof_audit": [{"id": "PROOF-1", "label": "Model", "status": "needs_revision"}],
                        "claim_evidence": [{"id": "CLAIM-1", "label": "Main theorem", "status": "supported"}],
                        "novelty_positioning": [{"id": "NOVELTY-1", "label": "Exact representation", "status": "positioned"}],
                    },
                    "files": [
                        {
                            "path": "PUBLIC/research_loop/source_verification.md",
                            "content": "# Source verification\n\nVerified official venue page.\n",
                            "role": "source_verification",
                        }
                    ],
                }
            )

            self.assertEqual(len(result["written"]), 1)
            self.assertTrue((root / "PUBLIC" / "research_loop" / "source_verification.md").exists())
            state = json.loads((root / "PUBLIC" / "research_state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["macro_phase"], "research_loop")
            self.assertEqual(state["internal_phase"], "loop_acceptance_gate")
            self.assertEqual(state["choice_prompts"][0]["prompt_id"], "CP-RESEARCH-LOOP-ARTIFACT-ACCEPTANCE")
            workflow = state["submission_workflow"]
            self.assertEqual(workflow["venue_requirements"][0]["status"], "verified")
            self.assertIn("PUBLIC/research_loop/source_verification.md", {item["path"] for item in workflow["research_loop_artifacts"]})
            project_readback = json.loads(Path(project["project_file"]).read_text(encoding="utf-8"))
            self.assertEqual(project_readback["current_macro_phase"], "research_loop")
            self.assertEqual(project_readback["current_phase"], "loop_acceptance_gate")

    def test_research_loop_artifact_acceptance_returns_to_alignment(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            state = ResearchStateService(projects.require_project_root, projects.update_project)
            ResearchLoopArtifactService(projects.require_project_root, projects.update_project).write_artifacts(
                {
                    "summary": "audit",
                    "files": [{"path": "PUBLIC/research_loop/audit.md", "content": "audit\n", "role": "audit"}],
                }
            )

            state.submit_choice_response(
                {
                    "prompt_id": "CP-RESEARCH-LOOP-ARTIFACT-ACCEPTANCE",
                    "option_id": "accept_and_plan_next",
                    "free_form": "Accept the audit and prepare final paper production.",
                }
            )

            readback = state.read_state()["research_state"]
            self.assertEqual(readback["internal_phase"], "loop_plan_alignment")
            self.assertEqual(readback["choice_prompts"][0]["prompt_id"], "CP-NEXT-RESEARCH-LOOP")
            self.assertEqual(readback["choice_prompts"][0]["recommended_option"], "repair_blocking_gaps")
            project_readback = json.loads(Path(project["project_file"]).read_text(encoding="utf-8"))
            self.assertEqual(project_readback["current_phase"], "loop_plan_alignment")

    def test_research_loop_acceptance_recommends_repair_when_audit_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            projects.create_project("Demo", base / "demo.rosproj")
            state = ResearchStateService(projects.require_project_root, projects.update_project)
            ResearchLoopArtifactService(projects.require_project_root, projects.update_project).write_artifacts(
                {
                    "summary": "blocking proof audit",
                    "workflow_updates": {
                        "proof_audit": [{"id": "PROOF-1", "label": "Gate reuse", "status": "needs_revision"}]
                    },
                    "files": [{"path": "PUBLIC/research_loop/audit.md", "content": "audit\n", "role": "audit"}],
                }
            )

            state.submit_choice_response(
                {
                    "prompt_id": "CP-RESEARCH-LOOP-ARTIFACT-ACCEPTANCE",
                    "option_id": "accept_and_plan_next",
                    "free_form": "Accept the audit diagnosis, then repair proof gaps.",
                }
            )

            prompt = state.read_state()["research_state"]["choice_prompts"][0]
            self.assertEqual(prompt["recommended_option"], "repair_blocking_gaps")

    def test_research_loop_decision_moves_to_execute_analyze(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            state = ResearchStateService(projects.require_project_root, projects.update_project)

            state.submit_choice_response(
                {
                    "prompt_id": "CP-NEXT-RESEARCH-LOOP",
                    "option_id": "repair_blocking_gaps",
                    "free_form": "Repair proof and source blockers.",
                }
            )

            readback = state.read_state()["research_state"]
            self.assertEqual(readback["internal_phase"], "loop_execute_analyze")
            self.assertEqual(readback["choice_prompts"], [])
            project_readback = json.loads(Path(project["project_file"]).read_text(encoding="utf-8"))
            self.assertEqual(project_readback["current_phase"], "loop_execute_analyze")

    def test_paper_artifact_service_rejects_private_escape_and_secret_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            projects.create_project("Demo", base / "demo.rosproj")
            service = PaperArtifactService(projects.require_project_root)

            with self.assertRaises(SecurityError):
                service.write_artifacts({"files": [{"path": "../outside.tex", "content": "x"}]})
            with self.assertRaises(SecurityError):
                service.write_artifacts({"files": [{"path": "PRIVATE/paper/main.tex", "content": "x"}]})
            with self.assertRaises(SecurityError):
                service.write_artifacts({"files": [{"path": "PUBLIC/paper/main.tex", "content": "api_key=secret"}]})
            with self.assertRaises(SecurityError):
                service.write_artifacts({"files": [{"path": "PUBLIC/paper/main.tex", "content": "x\x08eta"}]})

    def test_project_path_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(SecurityError):
                resolve_under(root, root.parent / "outside.txt")

    def test_directory_import_preserves_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source"
            source.mkdir()
            (source / "draft.tex").write_text("draft", encoding="utf-8")
            (source / "nested").mkdir()
            (source / "nested" / "refs.bib").write_text("@article{x}", encoding="utf-8")
            project = base / "project"
            project.mkdir()

            result = import_directory_to_project(source, project, "PRIVATE/intake/source_materials")
            targets = {item["target"] for item in result["imported_files"]}
            self.assertIn("PRIVATE/intake/source_materials/draft.tex", targets)
            self.assertIn("PRIVATE/intake/source_materials/nested/refs.bib", targets)
            self.assertTrue((project / "CONTROL" / "intake_queue" / f"{result['manifest_id']}.material_manifest.json").exists())
            self.assertTrue((project / "PUBLIC" / "material_manifest_summary.json").exists())

    def test_directory_import_handles_long_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source"
            long_dir = source / "target_journal_templates_and_reference_papers" / "reference_papers"
            long_dir.mkdir(parents=True)
            long_name = "02_Embedding_and_approximation_theorems_for_echo_state_networks__Hart_Hook_Dawes_2020_arXiv.pdf"
            (long_dir / long_name).write_bytes(b"%PDF-1.4 test")
            project = base / "project"
            project.mkdir()

            result = import_directory_to_project(source, project, "PRIVATE/intake/source_materials_structured")
            self.assertEqual(len(result["imported_files"]), 1)
            self.assertTrue((project / result["imported_files"][0]["target"]).exists())

    def test_directory_import_handles_long_nested_target_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source"
            source.mkdir()
            (source / "reference_material.pdf").write_bytes(b"%PDF-1.4")
            project = base / ("project_" + "d" * 40)
            project.mkdir()
            target_subdir = (
                "PRIVATE/intake/"
                + ("prior_draft_project_" + "a" * 40)
                + "/"
                + ("source_materials_structured_" + "b" * 40)
                + "/"
                + ("target_journal_templates_" + "c" * 40)
            )

            result = import_directory_to_project(source, project, target_subdir)

            self.assertEqual(len(result["imported_files"]), 1)
            target = (project / result["imported_files"][0]["target"]).resolve()
            self.assertTrue(os.path.exists("\\\\?\\" + str(target)))
            shutil.rmtree("\\\\?\\" + str(project.resolve()))

    def test_directory_import_builds_folder_manifest_roles_and_state_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            source = base / "source"
            (source / "templates").mkdir(parents=True)
            (source / "reference_papers").mkdir(parents=True)
            (source / "notes").mkdir(parents=True)
            (source / "main.tex").write_text("\\section{Draft}", encoding="utf-8")
            (source / "references.bib").write_text("@article{x}", encoding="utf-8")
            (source / "templates" / "elsarticle.cls").write_text("class", encoding="utf-8")
            (source / "reference_papers" / "example.pdf").write_bytes(b"%PDF-1.4")
            (source / "slides.pptx").write_bytes(b"ppt")
            (source / "notes" / "proof_audit.md").write_text("proof notes", encoding="utf-8")
            (source / "secrets").mkdir()
            (source / "secrets" / "key.txt").write_text("api_key=secret", encoding="utf-8")
            (source / ".git" / "objects").mkdir(parents=True)
            (source / ".git" / "objects" / "noise").write_text("git object", encoding="utf-8")

            result = import_directory_to_project(source, root, "PRIVATE/intake/source_materials")
            roles = {item["role"] for item in result["imported_files"]}

            self.assertIn("manuscript_draft", roles)
            self.assertIn("bibliography", roles)
            self.assertIn("venue_template", roles)
            self.assertIn("example_paper", roles)
            self.assertIn("slide_deck", roles)
            self.assertIn("proof_audit", roles)
            self.assertEqual(result["excluded_count"], 2)
            self.assertIn("sensitive or secret-like", " ".join(result["warnings"]))
            self.assertIn("operational or build", json.dumps(result["excluded_files"], ensure_ascii=False))

            state = ResearchStateService(projects.require_project_root).read_state()
            manifest = state["material_manifest"]
            self.assertEqual(manifest["file_count"], 6)
            self.assertEqual(manifest["excluded_count"], 2)
            self.assertEqual(manifest["role_counts"]["manuscript_draft"], 1)
            self.assertNotIn("api_key", json.dumps(manifest, ensure_ascii=False).lower())

    def test_directory_import_aggregates_multiple_material_manifests(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            source_a = base / "source-a"
            source_b = base / "source-b"
            source_a.mkdir()
            source_b.mkdir()
            (source_a / "main.tex").write_text("\\section{Draft}", encoding="utf-8")
            (source_b / "slides.pptx").write_bytes(b"ppt")

            import_directory_to_project(source_a, root, "PRIVATE/intake/source_a")
            import_directory_to_project(source_b, root, "PRIVATE/intake/source_b")

            state = ResearchStateService(projects.require_project_root).read_state()
            manifest = state["material_manifest"]
            self.assertEqual(manifest["source_name"], "2 material imports")
            self.assertEqual(manifest["file_count"], 2)
            self.assertEqual(len(manifest["imports"]), 2)
            self.assertEqual(manifest["role_counts"]["manuscript_draft"], 1)
            self.assertEqual(manifest["role_counts"]["slide_deck"], 1)

    def test_profile_rejects_secret_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            profiles = ProfileService(Path(temp) / "profiles.json")
            seeded = profiles.list_profiles()["profiles"]
            yunwu = next(item for item in seeded if item["profile_id"] == "yunwu-gpt-55-xhigh")
            self.assertEqual(yunwu["provider_id"], "yunwu")
            self.assertEqual(yunwu["secret_ref"], "env:YUNWU_API_KEY")
            with self.assertRaises(ValueError):
                profiles.upsert_profile(
                    {
                        "profile_id": "bad",
                        "label": "Bad",
                        "type": "openai_api_key",
                        "api_key": "sk-test",
                    }
                )
            saved = profiles.upsert_profile(
                {
                    "profile_id": "yunwu-test",
                    "label": "Yunwu Test",
                    "type": "custom_provider",
                    "provider_id": "yunwu",
                    "model": "gpt-5.5",
                    "base_url": "https://yunwu.ai/v1",
                    "wire_api": "responses",
                    "reasoning_effort": "xhigh",
                    "env_key": "YUNWU_API_KEY",
                    "secret_ref": "env:YUNWU_API_KEY",
                }
            )
            self.assertEqual(saved["secret_ref"], "env:YUNWU_API_KEY")
            with self.assertRaises(ValueError):
                profiles.upsert_profile(
                    {
                        "profile_id": "bad-ref",
                        "label": "Bad ref",
                        "type": "custom_provider",
                        "provider_id": "yunwu",
                        "secret_ref": "sk-not-a-reference",
                    }
                )

    def test_profile_seeds_missing_yunwu_profile_for_existing_store(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            store = Path(temp) / "profiles.json"
            store.write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "openai-account",
                                "label": "OpenAI Account",
                                "type": "openai_account",
                                "provider_id": "openai",
                                "model": None,
                                "secret_ref": "codex_managed_auth",
                                "created_at": "2026-01-01T00:00:00+00:00",
                                "updated_at": "2026-01-01T00:00:00+00:00",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            listed = ProfileService(store).list_profiles()["profiles"]

            profile_ids = {item["profile_id"] for item in listed}
            self.assertIn("openai-account", profile_ids)
            self.assertIn("yunwu-gpt-55-xhigh", profile_ids)
            yunwu = next(item for item in listed if item["profile_id"] == "yunwu-gpt-55-xhigh")
            self.assertEqual(yunwu["model"], "gpt-5.5")
            self.assertEqual(yunwu["reasoning_effort"], "xhigh")
            self.assertEqual(yunwu["secret_ref"], "env:YUNWU_API_KEY")

    def test_runtime_config_writes_isolated_codex_home_without_secret(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            codex_home = Path(temp) / "codex_home"
            service = RuntimeConfigService(codex_home)
            profile = {
                "profile_id": "yunwu-test",
                "label": "Yunwu Test",
                "type": "custom_provider",
                "provider_id": "yunwu",
                "model": "gpt-5.5",
                "base_url": "https://yunwu.ai/v1",
                "wire_api": "responses",
                "reasoning_effort": "xhigh",
                "env_key": "YUNWU_API_KEY",
                "secret_ref": "env:YUNWU_API_KEY",
            }

            status = service.prepare_profile(profile, require_secret=False)

            config_text = (codex_home / "config.toml").read_text(encoding="utf-8")
            profile_text = (codex_home / "yunwu.config.toml").read_text(encoding="utf-8")
            self.assertIn('model_provider = "yunwu"', config_text)
            self.assertIn('model_reasoning_effort = "xhigh"', config_text)
            self.assertIn('wire_api = "responses"', config_text)
            self.assertIn('env_key = "YUNWU_API_KEY"', config_text)
            self.assertIn('model = "gpt-5.5"', profile_text)
            self.assertNotIn("sk-", config_text)
            self.assertEqual(status["codex_home"], str(codex_home))
            self.assertFalse(status["secret_loaded"])

    def test_runtime_config_loads_secret_only_to_environment(self) -> None:
        old_value = os.environ.pop("YUNWU_API_KEY", None)
        try:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                key_file = root / "gptimg2.txt"
                key_file.write_text("test-yunwu-value-12345\n", encoding="utf-8")
                service = RuntimeConfigService(root / "codex_home")
                profile = {
                    "profile_id": "yunwu-test",
                    "label": "Yunwu Test",
                    "type": "custom_provider",
                    "provider_id": "yunwu",
                    "model": "gpt-5.5",
                    "base_url": "https://yunwu.ai/v1",
                    "wire_api": "responses",
                    "reasoning_effort": "xhigh",
                    "env_key": "YUNWU_API_KEY",
                    "secret_ref": "env:YUNWU_API_KEY",
                }

                status = service.load_secret_from_file(profile, str(key_file))

                self.assertTrue(status["secret_loaded"])
                self.assertEqual(os.environ["YUNWU_API_KEY"], "test-yunwu-value-12345")
                config_text = (root / "codex_home" / "config.toml").read_text(encoding="utf-8")
                self.assertNotIn("test-yunwu-value-12345", config_text)
        finally:
            if old_value is not None:
                os.environ["YUNWU_API_KEY"] = old_value
            else:
                os.environ.pop("YUNWU_API_KEY", None)

    def test_runtime_service_passes_yunwu_provider_to_turn(self) -> None:
        old_value = os.environ.get("YUNWU_API_KEY")
        os.environ["YUNWU_API_KEY"] = "test-yunwu-value-12345"
        try:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                approvals = ApprovalService(timeout_seconds=0.01)
                service = RuntimeService(lambda: root, approvals)
                calls: list[dict[str, object]] = []

                class FakeClient:
                    def thread_start(self, params: dict[str, object]) -> dict[str, object]:
                        calls.append({"method": "thread_start", "params": params})
                        return {"thread": {"id": "thread_test"}}

                    def turn_start(self, thread_id: str, text: str, params: dict[str, object]) -> dict[str, object]:
                        calls.append({"method": "turn_start", "thread_id": thread_id, "text": text, "params": params})
                        return {"turn": {"id": "turn_test"}}

                    def register_turn_notifications(self, turn_id: str) -> None:
                        return None

                    def next_turn_notification(self, turn_id: str):
                        raise RuntimeError("stop fake drain")

                    def unregister_turn_notifications(self, turn_id: str) -> None:
                        return None

                service._client = FakeClient()  # type: ignore[attr-defined]
                profile = {
                    "profile_id": "yunwu-test",
                    "label": "Yunwu Test",
                    "type": "custom_provider",
                    "provider_id": "yunwu",
                    "model": "gpt-5.5",
                    "base_url": "https://yunwu.ai/v1",
                    "wire_api": "responses",
                    "reasoning_effort": "xhigh",
                    "env_key": "YUNWU_API_KEY",
                    "secret_ref": "env:YUNWU_API_KEY",
                }

                thread = service.start_thread(profile, ephemeral=True)
                result = service.start_turn("thread_test", "Return a JSON status artifact.", profile)

                self.assertEqual(thread["thread"]["id"], "thread_test")
                self.assertEqual(result["turn"]["id"], "turn_test")
                thread_params = calls[0]["params"]
                turn_params = calls[1]["params"]
                self.assertEqual(thread_params["sandbox"], "workspace-write")
                self.assertEqual(thread_params["approvalPolicy"], "on-request")
                self.assertEqual(thread_params["model"], "gpt-5.5")
                self.assertEqual(thread_params["modelProvider"], "yunwu")
                self.assertEqual(turn_params["approvalPolicy"], "on-request")
                self.assertEqual(turn_params["sandboxPolicy"], {"type": "workspace-write", "writableRoots": [str(root)], "networkAccess": True})
                self.assertEqual(turn_params["model"], "gpt-5.5")
                self.assertEqual(turn_params["modelProvider"], "yunwu")
        finally:
            if old_value is None:
                os.environ.pop("YUNWU_API_KEY", None)
            else:
                os.environ["YUNWU_API_KEY"] = old_value

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

    def test_archive_service_creates_snapshot_and_rejects_private_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            project = projects.create_project("Demo", base / "demo.rosproj")
            root = Path(project["project_root"])
            archives = ArchiveService(projects.require_project_root)
            (root / "PUBLIC" / "note.md").write_text("accepted artifact summary\n", encoding="utf-8")

            preview = archives.preview()
            self.assertTrue(preview["dirty"])
            self.assertIn("PUBLIC/note.md", preview["changed_paths"])

            record = archives.create("accepted loop artifact", "", "research_loop")
            self.assertEqual(record["status"], "created")
            self.assertIn("PUBLIC/note.md", record["changed_paths"])
            public_index = json.loads((root / "PUBLIC" / "archive_index.json").read_text(encoding="utf-8"))
            self.assertEqual(len(public_index["archives"]), 1)
            self.assertNotIn("PRIVATE", json.dumps(public_index, ensure_ascii=False))

            (root / "PRIVATE" / "secret.txt").write_text("private note\n", encoding="utf-8")
            record = archives.create("private ignored by git", "", "research_loop")
            self.assertNotIn("PRIVATE", json.dumps(record, ensure_ascii=False))

    def test_archive_preview_uses_runtime_project_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            template = base / "template"
            template.mkdir()
            make_template(template)
            projects = ProjectService(template)
            projects.create_project("Demo", base / "demo.rosproj")
            state = ResearchStateService(projects.require_project_root, projects.update_project)
            state.write_research_plan({"summary": "plan", "content": "# Research Plan\n"})
            state.submit_choice_response({"prompt_id": "CP-RESEARCH-PLAN-ACCEPTANCE", "option_id": "accept_with_audit"})
            archives = ArchiveService(projects.require_project_root)

            preview = archives.preview()

            self.assertEqual(preview["macro_phase"], "research_loop")
            self.assertEqual(preview["phase"], "loop_plan_alignment")


if __name__ == "__main__":
    unittest.main()
