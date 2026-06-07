#!/usr/bin/env python3
"""Strict local validators for Research OS repository instances.

This tool intentionally has no third-party dependencies. It implements the
small YAML and JSON Schema subset used by this repository so CI and hooks can
catch known governance regressions without installing PyYAML/jsonschema.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class YamlDate:
    value: str


@dataclass(frozen=True)
class YamlDateTime:
    value: str


class ValidationError(Exception):
    pass


def strip_inline_comment(text: str) -> str:
    in_quote: str | None = None
    escaped = False
    for index, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_quote == '"':
            escaped = True
            continue
        if char in {"'", '"'}:
            if in_quote == char:
                in_quote = None
            elif in_quote is None:
                in_quote = char
            continue
        if char == "#" and in_quote is None and (index == 0 or text[index - 1].isspace()):
            return text[:index].rstrip()
    return text.rstrip()


def split_inline_list(value: str) -> list[str]:
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    parts: list[str] = []
    current: list[str] = []
    in_quote: str | None = None
    escaped = False
    for char in inner:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\" and in_quote == '"':
            current.append(char)
            escaped = True
            continue
        if char in {"'", '"'}:
            current.append(char)
            if in_quote == char:
                in_quote = None
            elif in_quote is None:
                in_quote = char
            continue
        if char == "," and in_quote is None:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    parts.append("".join(current).strip())
    return parts


def parse_scalar(raw: str) -> Any:
    value = strip_inline_comment(raw).strip()
    if value == "":
        return ""
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith("[") and value.endswith("]"):
        return [parse_scalar(part) for part in split_inline_list(value)]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        if value.startswith('"'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"null", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}t[0-9:.+-]+", lowered):
        return YamlDateTime(value)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return YamlDate(value)
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def prepared_yaml_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise ValidationError("YAML indentation must not use tabs")
        stripped = strip_inline_comment(raw)
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        lines.append((indent, stripped.strip()))
    return lines


def split_key_value(text: str) -> tuple[str, str]:
    if ":" not in text:
        raise ValidationError(f"Expected key/value YAML line, got: {text}")
    key, value = text.split(":", 1)
    return key.strip(), value.strip()


def parse_yaml_text(text: str) -> Any:
    lines = prepared_yaml_lines(text)
    if not lines:
        return None

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(lines):
            return {}, index
        line_indent, content = lines[index]
        if line_indent < indent:
            return {}, index
        if line_indent == indent and content.startswith("- "):
            return parse_list(index, indent)
        return parse_map(index, indent)

    def parse_map(index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(lines):
            line_indent, content = lines[index]
            if line_indent < indent or content.startswith("- "):
                break
            if line_indent > indent:
                raise ValidationError(f"Unexpected indentation at line: {content}")
            key, raw_value = split_key_value(content)
            index += 1
            if raw_value == "":
                if index < len(lines) and lines[index][0] > line_indent:
                    child, index = parse_block(index, lines[index][0])
                    result[key] = child
                else:
                    result[key] = {}
            else:
                result[key] = parse_scalar(raw_value)
        return result, index

    def parse_list(index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(lines):
            line_indent, content = lines[index]
            if line_indent < indent:
                break
            if line_indent != indent or not content.startswith("- "):
                break
            rest = content[2:].strip()
            index += 1
            if not rest:
                if index < len(lines) and lines[index][0] > line_indent:
                    child, index = parse_block(index, lines[index][0])
                else:
                    child = None
                result.append(child)
                continue
            if ":" in rest and not rest.startswith(("http://", "https://", '"', "'")):
                key, raw_value = split_key_value(rest)
                item: dict[str, Any] = {}
                item[key] = parse_scalar(raw_value) if raw_value else {}
                if index < len(lines) and lines[index][0] > line_indent:
                    child, index = parse_map(index, lines[index][0])
                    item.update(child)
                result.append(item)
            else:
                result.append(parse_scalar(rest))
        return result, index

    parsed, end = parse_block(0, lines[0][0])
    if end != len(lines):
        raise ValidationError(f"Could not parse all YAML content; stopped at {lines[end]}")
    return parsed


def load_instance(path: Path) -> Any:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    return parse_yaml_text(text)


def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def resolve_ref(schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValidationError(f"Unsupported external $ref: {ref}")
    node: Any = schema
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, YamlDate):
        return "yaml-date"
    if isinstance(value, YamlDateTime):
        return "yaml-datetime"
    return type(value).__name__


def matches_type(value: Any, expected: str) -> bool:
    actual = type_name(value)
    if expected == "number":
        return actual in {"number", "integer"}
    return actual == expected


def validate_value(value: Any, node: dict[str, Any], root_schema: dict[str, Any], path: str) -> None:
    if "$ref" in node:
        validate_value(value, resolve_ref(root_schema, str(node["$ref"])), root_schema, path)
        return

    expected_type = node.get("type")
    if expected_type is not None:
        expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(matches_type(value, item) for item in expected_types):
            raise ValidationError(f"{path}: {value!r} is {type_name(value)}, expected {expected_types}")

    if "const" in node and value != node["const"]:
        raise ValidationError(f"{path}: {value!r} does not equal const {node['const']!r}")
    if "enum" in node and value not in node["enum"]:
        raise ValidationError(f"{path}: {value!r} is not one of {node['enum']!r}")
    if value is None:
        return

    if isinstance(value, str):
        if "minLength" in node and len(value) < int(node["minLength"]):
            raise ValidationError(f"{path}: string shorter than minLength {node['minLength']}")
        if "pattern" in node and not re.search(str(node["pattern"]), value):
            raise ValidationError(f"{path}: {value!r} does not match pattern {node['pattern']!r}")
        if node.get("format") == "uri" and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
            raise ValidationError(f"{path}: {value!r} is not a URI")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in node and value < int(node["minimum"]):
            raise ValidationError(f"{path}: {value} is below minimum {node['minimum']}")

    if isinstance(value, list):
        if "minItems" in node and len(value) < int(node["minItems"]):
            raise ValidationError(f"{path}: array has fewer than {node['minItems']} items")
        if "maxItems" in node and len(value) > int(node["maxItems"]):
            raise ValidationError(f"{path}: array has more than {node['maxItems']} items")
        if "items" in node:
            for index, item in enumerate(value):
                validate_value(item, node["items"], root_schema, f"{path}[{index}]")

    if isinstance(value, dict):
        for key in node.get("required", []):
            if key not in value:
                raise ValidationError(f"{path}: missing required property {key!r}")
        properties = node.get("properties", {})
        for key, child_schema in properties.items():
            if key in value:
                validate_value(value[key], child_schema, root_schema, f"{path}.{key}")
        if node.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                raise ValidationError(f"{path}: unexpected properties {sorted(extra)}")


def validate_instance(instance_path: Path, schema_path: Path, root: Path) -> None:
    instance = load_instance(instance_path)
    schema = load_schema(schema_path)
    validate_value(instance, schema, schema, str(instance_path.relative_to(root)))


def validate_json_schema_files(root: Path) -> list[str]:
    messages: list[str] = []
    for path in sorted((root / "config" / "schemas").glob("*.json")):
        load_schema(path)
        messages.append(f"JSON schema OK: {path.relative_to(root)}")
    return messages


def instance_pairs(root: Path) -> list[tuple[str, str]]:
    return [
        ("config/research_flow.yaml", "config/schemas/research_flow.schema.json"),
        ("config/research_project.yaml", "config/schemas/research_project.schema.json"),
        ("CONTROL/work_order.yaml", "config/schemas/work_order.schema.json"),
        ("PUBLIC/claim_evidence_matrix.yaml", "config/schemas/claim_evidence.schema.json"),
        ("PROVENANCE/live_evidence_snapshot.yaml", "config/schemas/live_evidence_snapshot.schema.json"),
        ("docs/doc_map.yaml", "config/schemas/doc_map.schema.json"),
        ("docs/integrations/components.yaml", "config/schemas/integration_registry.schema.json"),
        ("templates/research_kernel/research_cycle.template.yaml", "config/schemas/research_kernel.schema.json"),
        ("templates/yaml/harness_run.template.yaml", "config/schemas/harness_run.schema.json"),
        ("templates/yaml/copilot_intake.template.yaml", "config/schemas/copilot_intake.schema.json"),
        ("templates/yaml/copilot_questions.template.yaml", "config/schemas/copilot_questions.schema.json"),
        (
            "templates/yaml/copilot_initialization_report.template.yaml",
            "config/schemas/copilot_initialization_report.schema.json",
        ),
        ("templates/adapters/adapter_contract.template.yaml", "config/schemas/adapter_contract.schema.json"),
        ("RUNS/experiments/EXP-0001/run.yaml", "config/schemas/experiment_run.schema.json"),
    ]


def validate_component_items(root: Path) -> list[str]:
    registry_path = root / "docs" / "integrations" / "components.yaml"
    schema_path = root / "config" / "schemas" / "integration_component.schema.json"
    registry = load_instance(registry_path)
    schema = load_schema(schema_path)
    components = registry.get("components", []) if isinstance(registry, dict) else []
    for index, component in enumerate(components):
        validate_value(component, schema, schema, f"docs/integrations/components.yaml.components[{index}]")
    return [f"Integration component instances OK: {len(components)}"]


def validate_jsonl(root: Path) -> list[str]:
    messages: list[str] = []
    for rel in ["PROVENANCE/run_manifest.jsonl", "PROVENANCE/resource_ledger.jsonl"]:
        path = root / rel
        if not path.exists():
            raise ValidationError(f"Missing JSONL file: {rel}")
        load_instance(path)
        messages.append(f"JSONL parse OK: {rel}")
    return messages


def run(root: Path) -> list[str]:
    messages = validate_json_schema_files(root)
    for instance_rel, schema_rel in instance_pairs(root):
        instance_path = root / instance_rel
        schema_path = root / schema_rel
        if not instance_path.exists():
            raise ValidationError(f"Missing instance file: {instance_rel}")
        validate_instance(instance_path, schema_path, root)
        messages.append(f"Schema instance OK: {instance_rel} -> {schema_rel}")
    messages.extend(validate_component_items(root))
    messages.extend(validate_jsonl(root))
    messages.append("Strict Research OS schema validation passed.")
    return messages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Research OS repository root")
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        messages = run(root)
    except Exception as exc:  # noqa: BLE001 - CLI should report validation path.
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"Strict validation failed: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"ok": True, "messages": messages}, ensure_ascii=False, indent=2))
    else:
        for message in messages:
            print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
