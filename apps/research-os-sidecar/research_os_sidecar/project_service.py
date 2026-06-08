from __future__ import annotations

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .common import PROJECT_SCHEMA_VERSION, now_iso, read_json, slugify, write_json
from .security import SecurityError, resolve_under


SEED_FILES = ["AGENTS.md", "README.md", ".gitattributes"]
SEED_DIRS = ["CONTROL", "config", "docs", "PUBLIC", "scripts", "skills", "templates", "domain_profiles", "adapters"]


def _legacy_name(*parts: str) -> str:
    return "".join(parts)


BLOCKED_SEED_NAMES = {
    _legacy_name("copilot", ".html"),
    _legacy_name("copilot", "_state.json"),
    _legacy_name("codex-browser-", "copilot", ".html"),
    _legacy_name("check_", "copilot_bridge.ps1"),
    _legacy_name("check_", "copilot", "_intake_schema.ps1"),
    _legacy_name("check_", "copilot_resource_rendering.ps1"),
    _legacy_name("check_", "copilot", "_state.ps1"),
    _legacy_name("research_os_", "copilot_server.py"),
}


def _codex_terminal_status(status: str) -> str:
    if status == "interrupted":
        return "turn_interrupted"
    if status in {"failed", "error"}:
        return "needs_repair"
    if status and status != "completed":
        return f"turn_{status}"
    return "turn_completed"


class ProjectService:
    def __init__(self, seed_root: Path) -> None:
        self.seed_root = seed_root.resolve()
        self.current_project: dict[str, Any] | None = None

    def create_project(self, name: str, project_file: str | Path) -> dict[str, Any]:
        project_file = Path(project_file).expanduser().resolve()
        if project_file.suffix.lower() != ".rosproj":
            project_file = project_file.with_suffix(".rosproj")
        project_id = slugify(project_file.stem or name)
        project_root = project_file.with_suffix("")
        if project_root.exists() and any(project_root.iterdir()):
            raise ValueError(f"Project directory is not empty: {project_root}")
        project_root.mkdir(parents=True, exist_ok=True)

        self._seed_project(project_root)
        self._write_project_scaffold(project_root)

        data = {
            "schema_version": PROJECT_SCHEMA_VERSION,
            "project_id": project_id,
            "name": name.strip() or project_id,
            "project_file": str(project_file),
            "project_root": str(project_root),
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "current_macro_phase": "initialization",
            "current_phase": "initialization_intake",
            "default_profile_id": "openai-account",
            "codex": {"thread_id": None, "last_turn_id": None, "last_status": "not_started"},
            "permissions": {
                "sandbox_root": str(project_root),
                "default_sandbox": "workspace_write",
                "outside_root_policy": "explicit_import_only",
                "download_root": "INBOX/downloads",
            },
        }
        self._write_generated_context(project_root, data)
        write_json(project_file, data)
        write_json(project_root / ".research-os" / "project.json", data)
        self._init_git(project_root)
        self.current_project = data
        return data

    def open_project(self, project_file: str | Path) -> dict[str, Any]:
        data = read_json(Path(project_file).expanduser().resolve(), {})
        if data.get("schema_version") != PROJECT_SCHEMA_VERSION:
            raise ValueError("Unsupported or missing .rosproj schema_version.")
        project_root = Path(str(data.get("project_root", ""))).expanduser().resolve()
        if not project_root.exists():
            raise ValueError(f"Project root does not exist: {project_root}")
        data["project_root"] = str(project_root)
        data = self._recover_codex_status_from_runtime_events(project_root, data)
        self._write_generated_context(project_root, data)
        write_json(project_root / ".research-os" / "project.json", data)
        self.current_project = data
        return data

    def close_project(self) -> dict[str, Any]:
        self.current_project = None
        return {"closed": True}

    def require_project_root(self) -> Path:
        if not self.current_project:
            raise ValueError("No project is open.")
        return Path(str(self.current_project["project_root"])).resolve()

    def update_project(self, patch: dict[str, Any]) -> dict[str, Any]:
        if not self.current_project:
            raise ValueError("No project is open.")
        disallowed = {"project_file", "project_root", "schema_version"}
        for key in disallowed:
            patch.pop(key, None)
        self.current_project.update(patch)
        self.current_project["updated_at"] = now_iso()
        project_file = Path(str(self.current_project["project_file"]))
        write_json(project_file, self.current_project)
        write_json(self.require_project_root() / ".research-os" / "project.json", self.current_project)
        return self.current_project

    def safe_project_path(self, value: str | Path) -> Path:
        return resolve_under(self.require_project_root(), value)

    def _recover_codex_status_from_runtime_events(self, project_root: Path, data: dict[str, Any]) -> dict[str, Any]:
        codex = dict(data.get("codex") or {})
        turn_id = codex.get("last_turn_id")
        if not turn_id or codex.get("last_status") not in {"turn_started", "turn_completed"}:
            return data
        runtime_events = project_root / ".research-os" / "runtime_events.jsonl"
        if not runtime_events.exists():
            return data
        recovered_status: str | None = None
        try:
            for line in runtime_events.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                event = json.loads(line)
                if event.get("type") == "runtime_error" and event.get("turn_id") == turn_id:
                    recovered_status = "needs_repair"
                elif event.get("type") == "codex_notification" and event.get("method") == "turn/completed":
                    payload_turn = ((event.get("payload") or {}).get("turn") or {})
                    if payload_turn.get("id") == turn_id:
                        terminal_status = str(payload_turn.get("status") or "").strip().lower()
                        recovered_status = _codex_terminal_status(terminal_status)
        except (OSError, json.JSONDecodeError):
            return data
        if recovered_status:
            codex["last_status"] = recovered_status
            data["codex"] = codex
            data["updated_at"] = now_iso()
        return data

    def _seed_project(self, project_root: Path) -> None:
        for file_name in SEED_FILES:
            source = self.seed_root / file_name
            if source.exists():
                shutil.copy2(source, project_root / file_name)
        for dir_name in SEED_DIRS:
            source = self.seed_root / dir_name
            target = project_root / dir_name
            if source.exists():
                shutil.copytree(source, target, ignore=self._ignore_seed_items)
        agents_skills = self.seed_root / ".agents" / "skills"
        if agents_skills.exists():
            shutil.copytree(agents_skills, project_root / ".agents" / "skills", ignore=self._ignore_seed_items)

    def _ignore_seed_items(self, _dir: str, names: list[str]) -> set[str]:
        blocked = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            "node_modules",
            "target",
            "PRIVATE",
            "external_repos",
            "archive_index.jsonl",
        }
        return {
            name
            for name in names
            if name in blocked
            or name in BLOCKED_SEED_NAMES
            or name.startswith("copilot_")
            or name.endswith((".pyc", ".pyo"))
        }

    def _write_project_scaffold(self, project_root: Path) -> None:
        for path in [
            "PRIVATE/.gitkeep",
            "PROVENANCE/run_manifest.jsonl",
            "PROVENANCE/resource_ledger.jsonl",
            "CONTROL/intake_queue/.gitkeep",
            "INBOX/downloads/.gitkeep",
            "INBOX/imports/.gitkeep",
            "outputs/.gitkeep",
            ".research-os/runtime_events.jsonl",
            ".research-os/approvals.jsonl",
        ]:
            target = project_root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_text("", encoding="utf-8")
        gitignore = project_root / ".gitignore"
        existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
        needed = "\nPRIVATE/**\n.research-os/runtime_events.jsonl\n*.secret\n*.key\n"
        if "PRIVATE/**" not in existing:
            gitignore.write_text(existing.rstrip() + needed, encoding="utf-8")

    def _write_generated_context(self, project_root: Path, project: dict[str, Any]) -> None:
        project_name = str(project.get("name") or project.get("project_id") or "Research OS project")
        context = f"""# Research OS Project Context

This file was generated by Research OS Desktop for `{project_name}`. It is the first context file Codex should read inside this project sandbox.

## Non-Negotiable Workflow

- Treat manuscript drafts, PDFs, PPT files, notes, venue templates, example papers, proof audits, screenshots, and previous review records as initialization material until the Research OS stage gates accept them.
- Before planning or writing, inspect the whole-folder material manifest in `CONTROL/intake_queue/*.material_manifest.json` and the public summary in `PUBLIC/material_manifest_summary.json`.
- Do not silently choose only `main.tex`, a PDF, or the most obvious draft when other source files are present.
- After material profiling, ask exactly three targeted initialization questions, each with a recommended option, concrete defaults, and a natural-language free-form path.
- Do not advance from the research loop acceptance gate unless the researcher accepts the previous artifact or gives revision instructions that have been handled.

## Skill And Harness Routing

- Use repository skills before generic execution. Start with `research-os-orchestrator` for routing and `research-os-execution-harness` before mutating artifacts or running experiments.
- Use `research-os-resource-guard` before paid APIs, cloud compute, real resource use, credentials, external writeback, public export, or budget changes.
- Use `research-os-live-evidence-refresh` before relying on venue rules, API/tool behavior, literature status, dataset/license facts, legal/ethics requirements, prices, or other time-sensitive claims.
- Use `research-os-paper-authoring` only after the paper track is selected or explicitly requested. Use `research-os-review-rebuttal` for adversarial review and rebuttal-style improvement rounds.

## Structured Research Plan

Before any final paper production, produce a researcher-visible plan with these sections:

1. Research content and problem statement.
2. Research motivation and venue fit.
3. Expected results and contributions.
4. Related literature and how the planned result differs from each source.
5. Theoretical setup, definitions, assumptions, and conventions.
6. Proof route for each main theoretical claim.
7. Experiment or computational design if applicable, including expected small-scale preliminary results.
8. Evidence and source-verification plan.
9. Risk register covering proof gaps, novelty risk, citation risk, venue-fit risk, and app/workflow risk.
10. Acceptance criteria for entering the final paper track.

## Source And Citation Integrity

- Verify target venue instructions and every cited source online before finalizing a paper.
- Do not invent citations, DOIs, arXiv IDs, URLs, theorems, experiments, results, author metadata, venue rules, or AI-use declarations.
- Record source verification status, access dates, unresolved access risks, and uncertain findings instead of hiding them.

## Privacy, Artifacts, And Gaps

- `PRIVATE/` is for raw intake and sensitive material; do not move raw private material into `PUBLIC/`.
- Preserve intermediate artifacts, failed attempts, negative results, raw redacted LLM calls, screenshots, logs, manifests, and resource ledger entries.
- Record reusable app or workflow gaps in `PROVENANCE/app_workflow_gaps.jsonl` and prefer fixing the app/workflow before bypassing it manually.
- Use `PUBLIC/paper/`, `PUBLIC/submission/`, and `PROVENANCE/paper/` for controlled paper artifacts after final-product gates are satisfied.
"""
        (project_root / "AGENTS.md").write_text(context, encoding="utf-8")
        project_context = project_root / "CONTROL" / "project_context.md"
        project_context.parent.mkdir(parents=True, exist_ok=True)
        project_context.write_text(context, encoding="utf-8")

    def _init_git(self, project_root: Path) -> None:
        if (project_root / ".git").exists():
            return
        def run(args: list[str]) -> None:
            subprocess.run(["git", *args], cwd=project_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            run(["init"])
            run(["add", "--all"])
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Research OS Desktop",
                    "-c",
                    "user.email=research-os-desktop@example.invalid",
                    "commit",
                    "-m",
                    "initialize Research OS project",
                ],
                cwd=project_root,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            raise SecurityError(f"Could not initialize project git repository: {exc}") from exc
