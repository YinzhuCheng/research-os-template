from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from .common import app_data_dir
from .security import SECRET_RE, SecurityError


DEFAULT_YUNWU_PROFILE_ID = "yunwu-gpt-55-xhigh"
DEFAULT_YUNWU_ENV_KEY = "YUNWU_API_KEY"
DEFAULT_YUNWU_BASE_URL = "https://yunwu.ai/v1"
ALLOWED_WIRE_APIS = {"responses", "chat"}
ALLOWED_REASONING_EFFORTS = {"minimal", "low", "medium", "high", "xhigh"}
ENV_KEY_RE = re.compile(r"^[A-Z_][A-Z0-9_]*$")


class RuntimeConfigService:
    def __init__(self, codex_home: Path | None = None) -> None:
        self.codex_home = codex_home or (app_data_dir() / "codex_home")
        self._active_runtime: dict[str, Any] | None = None

    def prepare_profile(self, profile: dict[str, Any], require_secret: bool = False) -> dict[str, Any]:
        runtime = self._normalize_profile(profile)
        self.codex_home.mkdir(parents=True, exist_ok=True)
        (self.codex_home / "config.toml").write_text(self._base_config_toml(runtime), encoding="utf-8", newline="\n")
        (self.codex_home / f"{runtime['codex_profile']}.config.toml").write_text(
            self._profile_config_toml(runtime),
            encoding="utf-8",
            newline="\n",
        )
        os.environ["CODEX_HOME"] = str(self.codex_home)
        secret_loaded = bool(os.environ.get(runtime["env_key"]))
        if require_secret and not secret_loaded:
            raise RuntimeError(
                f"runtime_secret_missing: load a local key into {runtime['env_key']} before starting a Yunwu Codex turn."
            )
        runtime = {**runtime, "codex_home": str(self.codex_home), "secret_loaded": secret_loaded}
        self._active_runtime = runtime
        return self.redacted(runtime)

    def load_secret_from_file(self, profile: dict[str, Any], key_file_path: str) -> dict[str, Any]:
        runtime = self._normalize_profile(profile)
        path = Path(key_file_path).expanduser()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"Key file does not exist: {key_file_path}")
        value = path.read_text(encoding="utf-8-sig").strip()
        if not value:
            raise SecurityError("Key file is empty.")
        if "\n" in value or "\r" in value:
            value = value.splitlines()[0].strip()
        if len(value) < 8:
            raise SecurityError("Key file does not contain a plausible API key.")
        os.environ[runtime["env_key"]] = value
        prepared = self.prepare_profile(profile, require_secret=True)
        return {**prepared, "loaded_from": path.name}

    def status(self) -> dict[str, Any]:
        if self._active_runtime:
            runtime = {**self._active_runtime, "secret_loaded": bool(os.environ.get(self._active_runtime["env_key"]))}
            return self.redacted(runtime)
        recovered = self._status_from_existing_config()
        if recovered:
            return self.redacted(recovered)
        return {
            "codex_home": str(self.codex_home),
            "configured": (self.codex_home / "config.toml").exists(),
            "secret_loaded": False,
            "provider_id": None,
            "model": None,
            "reasoning_effort": None,
        }

    def redacted(self, runtime: dict[str, Any]) -> dict[str, Any]:
        return {
            "configured": True,
            "codex_home": str(runtime.get("codex_home") or self.codex_home),
            "codex_profile": runtime.get("codex_profile"),
            "provider_id": runtime.get("provider_id"),
            "provider_name": runtime.get("provider_name"),
            "base_url": runtime.get("base_url"),
            "wire_api": runtime.get("wire_api"),
            "env_key": runtime.get("env_key"),
            "model": runtime.get("model"),
            "reasoning_effort": runtime.get("reasoning_effort"),
            "secret_loaded": bool(runtime.get("secret_loaded")),
        }

    def _status_from_existing_config(self) -> dict[str, Any] | None:
        config = self.codex_home / "config.toml"
        if not config.exists():
            return None
        try:
            text = config.read_text(encoding="utf-8")
        except OSError:
            return None
        values: dict[str, str] = {}
        in_provider_section = False
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[model_providers.") and line.endswith("]"):
                in_provider_section = True
                continue
            if "=" not in line:
                continue
            key, value = [part.strip() for part in line.split("=", 1)]
            value = _toml_unescape(value.strip().strip('"'))
            if not in_provider_section and key in {"model", "model_provider", "model_reasoning_effort"}:
                values[key] = value
            elif in_provider_section and key in {"name", "base_url", "env_key", "wire_api"}:
                values[key] = value
        provider_id = values.get("model_provider")
        model = values.get("model")
        if not provider_id and not model:
            return None
        env_key = values.get("env_key") or DEFAULT_YUNWU_ENV_KEY
        return {
            "configured": True,
            "codex_home": str(self.codex_home),
            "codex_profile": provider_id,
            "provider_id": provider_id,
            "provider_name": values.get("name") or provider_id,
            "base_url": values.get("base_url"),
            "wire_api": values.get("wire_api"),
            "env_key": env_key,
            "model": model,
            "reasoning_effort": values.get("model_reasoning_effort"),
            "secret_loaded": bool(os.environ.get(env_key)),
        }

    def _normalize_profile(self, profile: dict[str, Any]) -> dict[str, Any]:
        provider_id = str(profile.get("provider_id") or "").strip() or "openai"
        if provider_id != "yunwu":
            return {
                "profile_id": str(profile.get("profile_id") or "openai-account"),
                "codex_profile": "openai",
                "provider_id": provider_id,
                "provider_name": str(profile.get("label") or "OpenAI"),
                "base_url": str(profile.get("base_url") or ""),
                "wire_api": str(profile.get("wire_api") or "responses"),
                "env_key": str(profile.get("env_key") or "OPENAI_API_KEY"),
                "model": str(profile.get("model") or "gpt-5.5"),
                "reasoning_effort": str(profile.get("reasoning_effort") or "high"),
            }

        env_key = str(profile.get("env_key") or "").strip()
        secret_ref = str(profile.get("secret_ref") or "").strip()
        if not env_key and secret_ref.startswith("env:"):
            env_key = secret_ref.removeprefix("env:").strip()
        env_key = env_key or DEFAULT_YUNWU_ENV_KEY
        if not ENV_KEY_RE.match(env_key):
            raise SecurityError(f"Invalid environment variable name for runtime secret: {env_key}")

        base_url = str(profile.get("base_url") or DEFAULT_YUNWU_BASE_URL).strip().rstrip("/")
        if not base_url.startswith(("https://", "http://")):
            raise SecurityError("Provider base_url must be an HTTP(S) URL.")
        if SECRET_RE.search(base_url):
            raise SecurityError("Provider base_url contains secret-like content.")

        wire_api = str(profile.get("wire_api") or "responses").strip().lower()
        if wire_api not in ALLOWED_WIRE_APIS:
            raise SecurityError(f"Unsupported provider wire_api: {wire_api}")

        reasoning_effort = str(profile.get("reasoning_effort") or "xhigh").strip().lower()
        if reasoning_effort not in ALLOWED_REASONING_EFFORTS:
            raise SecurityError(f"Unsupported reasoning effort: {reasoning_effort}")

        return {
            "profile_id": str(profile.get("profile_id") or DEFAULT_YUNWU_PROFILE_ID),
            "codex_profile": str(profile.get("codex_profile") or "yunwu"),
            "provider_id": "yunwu",
            "provider_name": str(profile.get("label") or "Yunwu GPT-5.5 xhigh"),
            "base_url": base_url,
            "wire_api": wire_api,
            "env_key": env_key,
            "model": str(profile.get("model") or "gpt-5.5").strip(),
            "reasoning_effort": reasoning_effort,
        }

    def _base_config_toml(self, runtime: dict[str, Any]) -> str:
        return "\n".join(
            [
                f'model = "{_toml_escape(runtime["model"])}"',
                f'model_provider = "{_toml_escape(runtime["provider_id"])}"',
                f'model_reasoning_effort = "{_toml_escape(runtime["reasoning_effort"])}"',
                'hide_agent_reasoning = true',
                "",
                f'[model_providers.{runtime["provider_id"]}]',
                f'name = "{_toml_escape(runtime["provider_name"])}"',
                f'base_url = "{_toml_escape(runtime["base_url"])}"',
                f'env_key = "{_toml_escape(runtime["env_key"])}"',
                f'wire_api = "{_toml_escape(runtime["wire_api"])}"',
                "",
            ]
        )

    def _profile_config_toml(self, runtime: dict[str, Any]) -> str:
        return "\n".join(
            [
                f'model = "{_toml_escape(runtime["model"])}"',
                f'model_provider = "{_toml_escape(runtime["provider_id"])}"',
                f'model_reasoning_effort = "{_toml_escape(runtime["reasoning_effort"])}"',
                "",
            ]
        )


def _toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _toml_unescape(value: str) -> str:
    return value.replace('\\"', '"').replace("\\\\", "\\")
