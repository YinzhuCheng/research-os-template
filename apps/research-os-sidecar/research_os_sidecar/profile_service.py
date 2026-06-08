from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .common import app_data_dir, now_iso, read_json, write_json


PROFILE_TYPES = {"openai_account", "openai_api_key", "custom_provider"}
SECRET_FIELDS = {"api_key", "token", "secret", "password", "authorization"}
REFERENCE_FIELDS = {"secret_ref", "env_key", "env_key_instructions"}
ENV_KEY_RE = re.compile(r"^[A-Z_][A-Z0-9_]*$")


class ProfileService:
    def __init__(self, store_path: Path | None = None) -> None:
        self.store_path = store_path or (app_data_dir() / "profiles.json")

    def list_profiles(self) -> dict[str, Any]:
        payload = read_json(self.store_path, {"profiles": []})
        profiles = [item for item in payload.get("profiles") or [] if isinstance(item, dict)]
        existing = {str(item.get("profile_id")): item for item in profiles}
        changed = False
        for profile in self._default_profiles():
            profile_id = str(profile["profile_id"])
            if profile_id not in existing:
                existing[profile_id] = profile
                changed = True
        if changed or profiles != list(existing.values()):
            payload["profiles"] = sorted(existing.values(), key=lambda item: str(item.get("profile_id")))
            write_json(self.store_path, payload)
        return payload

    def upsert_profile(self, profile: dict[str, Any]) -> dict[str, Any]:
        self._assert_no_secret(profile)
        profile_type = profile.get("type")
        if profile_type not in PROFILE_TYPES:
            raise ValueError(f"Unsupported profile type: {profile_type}")
        profile_id = str(profile.get("profile_id") or "").strip()
        if not profile_id:
            raise ValueError("profile_id is required.")
        payload = self.list_profiles()
        existing = {item["profile_id"]: item for item in payload["profiles"]}
        current = existing.get(profile_id, {})
        merged = {
            **current,
            **profile,
            "profile_id": profile_id,
            "updated_at": now_iso(),
        }
        merged.setdefault("created_at", now_iso())
        existing[profile_id] = merged
        payload["profiles"] = sorted(existing.values(), key=lambda item: item["profile_id"])
        write_json(self.store_path, payload)
        return merged

    def delete_profile(self, profile_id: str) -> dict[str, Any]:
        payload = self.list_profiles()
        payload["profiles"] = [item for item in payload["profiles"] if item.get("profile_id") != profile_id]
        write_json(self.store_path, payload)
        return {"deleted": profile_id}

    def get_profile(self, profile_id: str | None) -> dict[str, Any]:
        profiles = self.list_profiles()["profiles"]
        if profile_id:
            for item in profiles:
                if item.get("profile_id") == profile_id:
                    return item
            raise ValueError(f"Unknown profile: {profile_id}")
        return profiles[0]

    def _assert_no_secret(self, value: Any) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                lowered = str(key).lower()
                if lowered in REFERENCE_FIELDS:
                    self._assert_safe_reference(lowered, nested)
                    continue
                if lowered in SECRET_FIELDS or any(part in lowered for part in SECRET_FIELDS):
                    raise ValueError(f"Profile metadata must not store secret field: {key}")
                self._assert_no_secret(nested)
        elif isinstance(value, list):
            for item in value:
                self._assert_no_secret(item)

    def _assert_safe_reference(self, key: str, value: Any) -> None:
        text = str(value or "")
        if key == "env_key" and text and not ENV_KEY_RE.match(text):
            raise ValueError("env_key must be an environment variable name, not a secret value.")
        if key == "secret_ref" and text and not (text.startswith("env:") or text == "codex_managed_auth"):
            raise ValueError("secret_ref must be an environment-variable reference or codex_managed_auth.")

    def _default_profiles(self) -> list[dict[str, Any]]:
        created_at = now_iso()
        return [
            {
                "profile_id": "openai-account",
                "label": "OpenAI Account",
                "type": "openai_account",
                "provider_id": "openai",
                "model": None,
                "secret_ref": "codex_managed_auth",
                "created_at": created_at,
                "updated_at": created_at,
            },
            {
                "profile_id": "yunwu-gpt-55-xhigh",
                "label": "Yunwu GPT-5.5 xhigh",
                "type": "custom_provider",
                "provider_id": "yunwu",
                "model": "gpt-5.5",
                "base_url": "https://yunwu.ai/v1",
                "wire_api": "responses",
                "reasoning_effort": "xhigh",
                "env_key": "YUNWU_API_KEY",
                "secret_ref": "env:YUNWU_API_KEY",
                "created_at": created_at,
                "updated_at": created_at,
            },
        ]
