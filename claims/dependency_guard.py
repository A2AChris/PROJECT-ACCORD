#!/usr/bin/env python3
"""Validate fail-closed publication state for declared semantic claim dependencies."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


class DependencyGuardError(ValueError):
    pass


def _reject_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise DependencyGuardError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, DependencyGuardError) as exc:
        raise DependencyGuardError(f"{path}: {exc}") from exc


def _state_entries(state_registry: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    entries: dict[tuple[str, str], dict[str, Any]] = {}
    for entry in state_registry["entries"]:
        key = (entry["id"], entry["revision"])
        if key in entries:
            raise DependencyGuardError(f"duplicate claim state entry: {key[0]} {key[1]}")
        entries[key] = entry
    return entries


def validate_dependencies(
    dependency_registry: dict[str, Any],
    state_registry: dict[str, Any],
) -> None:
    if dependency_registry.get("schema") != "accord.public-semantic-dependencies.v0.1":
        raise DependencyGuardError("unsupported semantic dependency registry schema")
    if dependency_registry.get("contract_revision") != "v0.1":
        raise DependencyGuardError("unsupported semantic dependency contract revision")

    entries = _state_entries(state_registry)
    seen: set[tuple[str, str, str, str, str]] = set()

    for relation in dependency_registry["dependencies"]:
        dependent = relation["dependent"]
        dependency = relation["dependency"]
        kind = relation["kind"]
        dependent_key = (dependent["id"], dependent["revision"])
        dependency_key = (dependency["id"], dependency["revision"])

        if kind != "SEMANTIC_INTERPRETATION":
            raise DependencyGuardError(f"unsupported semantic dependency kind: {kind}")
        if dependent_key == dependency_key:
            raise DependencyGuardError("claim revision cannot semantically depend on itself")
        if dependent_key not in entries:
            raise DependencyGuardError(
                f"dependent claim revision missing from state registry: {dependent_key[0]} {dependent_key[1]}"
            )
        if dependency_key not in entries:
            raise DependencyGuardError(
                f"semantic dependency missing from state registry: {dependency_key[0]} {dependency_key[1]}"
            )

        identity = (
            dependent_key[0],
            dependent_key[1],
            dependency_key[0],
            dependency_key[1],
            kind,
        )
        if identity in seen:
            raise DependencyGuardError("duplicate semantic dependency relation")
        seen.add(identity)

        dependent_state = entries[dependent_key]["publication_state"]
        dependency_state = entries[dependency_key]["publication_state"]

        if dependency_state != "PUBLISHED" and dependent_state == "PUBLISHED":
            raise DependencyGuardError(
                "published dependent claim requires explicit re-evaluation after semantic dependency "
                f"leaves PUBLISHED: {dependent_key[0]} {dependent_key[1]} depends on "
                f"{dependency_key[0]} {dependency_key[1]}={dependency_state}"
            )


def validate_repository(root: Path = ROOT) -> None:
    dependencies = load_json(root / "claims" / "public-semantic-dependencies.json")
    state_registry = load_json(root / "claims" / "public-claim-state.json")
    validate_dependencies(dependencies, state_registry)


def main() -> int:
    try:
        validate_repository()
    except (DependencyGuardError, KeyError, TypeError) as exc:
        print("SEMANTIC_DEPENDENCY_GUARD=FAIL")
        print(f"REASON={exc}")
        return 1
    print("SEMANTIC_DEPENDENCY_GUARD=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
