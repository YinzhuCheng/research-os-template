from __future__ import annotations

import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any


APP_NAME = "ResearchOS"
PROJECT_SCHEMA_VERSION = "research-os-project-v1"
DEFAULT_PORT = 8789


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat()


def app_data_dir() -> Path:
    root = os.environ.get("RESEARCH_OS_APPDATA")
    if root:
        return Path(root).expanduser().resolve()
    if os.name == "nt":
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(base) / APP_NAME
    return Path.home() / ".research-os"


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z._-]+", "-", value.strip()).strip("-._")
    return cleaned[:80] or "research-project"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


def public_error(exc: Exception) -> dict[str, Any]:
    return {"ok": False, "error": str(exc), "error_type": exc.__class__.__name__}
