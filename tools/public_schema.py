#!/usr/bin/env python3
"""Fail-closed JSON Schema subset validator for PROJECT ACCORD public artifacts.

The public schemas use a deliberately small Draft 2020-12 subset. This module
implements exactly that subset with the Python standard library. If a schema is
extended with an unsupported validation keyword, validation fails closed rather
than silently ignoring the new constraint.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"
SUPPORTED_KEYWORDS = {
    "$schema",
    "$id",
    "title",
    "type",
    "additionalProperties",
    "required",
    "properties",
    "const",
    "enum",
    "minLength",
    "maxLength",
    "pattern",
    "minItems",
    "maxItems",
    "uniqueItems",
    "items",
    "minProperties",
    "maxProperties",
    "minimum",
}
SUPPORTED_TYPES = {"object", "array", "string", "integer"}


class SchemaContractError(ValueError):
    pass


def _reject_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise SchemaContractError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, SchemaContractError) as exc:
        raise SchemaContractError(f"{path}: {exc}") from exc


def _schema_error(path: str, message: str) -> None:
    raise SchemaContractError(f"schema {path}: {message}")


def check_supported_schema(schema: Any, path: str = "$") -> None:
    if not isinstance(schema, dict):
        _schema_error(path, "schema node must be an object")

    unknown = sorted(set(schema) - SUPPORTED_KEYWORDS)
    if unknown:
        _schema_error(path, f"unsupported keyword(s): {unknown}")

    if "$schema" in schema and schema["$schema"] != DRAFT_2020_12:
        _schema_error(path, "only JSON Schema Draft 2020-12 is supported")

    for annotation in ("$id", "title"):
        if annotation in schema and not isinstance(schema[annotation], str):
            _schema_error(path, f"{annotation} must be a string")

    if "type" in schema:
        type_name = schema["type"]
        if type_name not in SUPPORTED_TYPES:
            _schema_error(path, f"unsupported type: {type_name!r}")

    if "required" in schema:
        required = schema["required"]
        if (
            not isinstance(required, list)
            or any(not isinstance(item, str) for item in required)
            or len(required) != len(set(required))
        ):
            _schema_error(path, "required must be an array of unique strings")

    if "properties" in schema:
        properties = schema["properties"]
        if not isinstance(properties, dict):
            _schema_error(path, "properties must be an object")
        for name, child in properties.items():
            if not isinstance(name, str):
                _schema_error(path, "property names must be strings")
            check_supported_schema(child, f"{path}.properties[{name!r}]")

    if "additionalProperties" in schema:
        additional = schema["additionalProperties"]
        if not isinstance(additional, (bool, dict)):
            _schema_error(path, "additionalProperties must be boolean or schema object")
        if isinstance(additional, dict):
            check_supported_schema(additional, f"{path}.additionalProperties")

    if "items" in schema:
        check_supported_schema(schema["items"], f"{path}.items")

    if "enum" in schema:
        enum = schema["enum"]
        if not isinstance(enum, list) or not enum:
            _schema_error(path, "enum must be a non-empty array")

    if "pattern" in schema:
        pattern = schema["pattern"]
        if not isinstance(pattern, str):
            _schema_error(path, "pattern must be a string")
        try:
            re.compile(pattern)
        except re.error as exc:
            _schema_error(path, f"invalid pattern: {exc}")

    for keyword in ("minLength", "maxLength", "minItems", "maxItems", "minProperties", "maxProperties", "minimum"):
        if keyword in schema:
            value = schema[keyword]
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                _schema_error(path, f"{keyword} must be a non-negative integer")

    if "uniqueItems" in schema and not isinstance(schema["uniqueItems"], bool):
        _schema_error(path, "uniqueItems must be boolean")


def _instance_error(path: str, message: str) -> None:
    raise SchemaContractError(f"instance {path}: {message}")


def _matches_type(instance: Any, type_name: str) -> bool:
    if type_name == "object":
        return isinstance(instance, dict)
    if type_name == "array":
        return isinstance(instance, list)
    if type_name == "string":
        return isinstance(instance, str)
    if type_name == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    raise AssertionError(type_name)


def _canonical_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def validate_instance(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    if "const" in schema and instance != schema["const"]:
        _instance_error(path, f"must equal const {schema['const']!r}")

    if "enum" in schema and instance not in schema["enum"]:
        _instance_error(path, "value is not in enum")

    if "type" in schema:
        type_name = schema["type"]
        if not _matches_type(instance, type_name):
            _instance_error(path, f"must be of type {type_name}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            _instance_error(path, f"length is below minLength={schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            _instance_error(path, f"length exceeds maxLength={schema['maxLength']}")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            _instance_error(path, f"does not match pattern {schema['pattern']!r}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            _instance_error(path, f"item count is below minItems={schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            _instance_error(path, f"item count exceeds maxItems={schema['maxItems']}")
        if schema.get("uniqueItems"):
            keys = [_canonical_key(item) for item in instance]
            if len(keys) != len(set(keys)):
                _instance_error(path, "items must be unique")
        if "items" in schema:
            for index, item in enumerate(instance):
                validate_instance(item, schema["items"], f"{path}[{index}]")

    if isinstance(instance, dict):
        if "minProperties" in schema and len(instance) < schema["minProperties"]:
            _instance_error(path, f"property count is below minProperties={schema['minProperties']}")
        if "maxProperties" in schema and len(instance) > schema["maxProperties"]:
            _instance_error(path, f"property count exceeds maxProperties={schema['maxProperties']}")

        required = schema.get("required", [])
        missing = [name for name in required if name not in instance]
        if missing:
            _instance_error(path, f"missing required properties: {missing}")

        properties = schema.get("properties", {})
        for name, value in instance.items():
            if name in properties:
                validate_instance(value, properties[name], f"{path}.{name}")
                continue
            additional = schema.get("additionalProperties", True)
            if additional is False:
                _instance_error(path, f"unexpected property: {name}")
            if isinstance(additional, dict):
                validate_instance(value, additional, f"{path}.{name}")

    if isinstance(instance, int) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            _instance_error(path, f"must be >= {schema['minimum']}")


def validate_paths(instance_path: Path, schema_path: Path) -> None:
    schema = load_json(schema_path)
    check_supported_schema(schema)
    instance = load_json(instance_path)
    validate_instance(instance, schema)
