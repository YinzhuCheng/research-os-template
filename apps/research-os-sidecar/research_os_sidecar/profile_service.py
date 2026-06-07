from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import app_data_dir, now_iso, read_json, write_json


PROFILE_TYPES = {"openai_account", "openai_api_key", "custom_provider"}
SECRET_FIELDS = {"api_key", "token", "secret", "password", "authorization"}


class ProfileService:
    def __init__(self, store_path: Path | None = None) -> None:
        self.store_path = store_path or (app_data_dir() / "profiles.json")

    def list_profiles(self) -> dict[str, Any]:
        payload = read_json(self.store_path, {"profiles": []})
        if not payload.get("profiles"):
            payload["profiles"] = [
                {
                    "profile_id": "openai-account",
                    "label": "OpenAI Account",
                    "type": "openai_account",
                    "provider_id": "openai",
                    "model": None,
                    "secret_ref": "codex_managed_auth",
                    "created_at": now_iso(),
                    "updated_at": now_iso(),
                }
            ]
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
                if lowered in SECRET_FIELDS or any(part in lowered for part in SECRET_FIELDS):
                    raise ValueError(f"Profile metadata must not store secret field: {key}")
                self._assert_no_secret(nested)
        elif isinstance(value, list):
            for item in value:
                self._assert_no_secret(item)
