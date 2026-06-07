from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .common import PROJECT_SCHEMA_VERSION, now_iso, read_json, slugify, write_json
from .security import SecurityError, resolve_under


SEED_FILES = ["AGENTS.md", "README.md", ".gitattributes"]
SEED_DIRS = ["CONTROL", "config", "docs", "PUBLIC", "scripts", "skills", "templates", "domain_profiles", "adapters"]


class ProjectService:
    def __init__(self, template_root: Path) -> None:
        self.template_root = template_root.resolve()
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

    def _seed_project(self, project_root: Path) -> None:
        for file_name in SEED_FILES:
            source = self.template_root / file_name
            if source.exists():
                shutil.copy2(source, project_root / file_name)
        for dir_name in SEED_DIRS:
            source = self.template_root / dir_name
            target = project_root / dir_name
            if source.exists():
                shutil.copytree(source, target, ignore=self._ignore_seed_items)
        agents_skills = self.template_root / ".agents" / "skills"
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
        return {name for name in names if name in blocked or name.endswith((".pyc", ".pyo"))}

    def _write_project_scaffold(self, project_root: Path) -> None:
        for path in [
            "PRIVATE/.gitkeep",
            "PROVENANCE/run_manifest.jsonl",
            "PROVENANCE/resource_ledger.jsonl",
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
