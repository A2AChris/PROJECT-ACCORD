#!/usr/bin/env python3
"""Fail-closed guard for public semantic claim dependencies.

The guard consumes only public claim-state, dependency, and adjudication artifacts. It
does not decide whether a challenge is true and performs no private reference verification.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "accord_adjudication", ROOT / "challenge" / "adjudication.py"
)
_adjudication = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_adjudication)

CONFIRMED_NEGATIVE_DISPOSITIONS = {
    "CONFIRMED_FALSIFICATION",
    "CONFIRMED_CONTRACT_GAP",
}
DEPENDENCY_RELATION = "SEMANTIC_INTERPRETATION"


class DependencyGuardError(ValueError):
    pass


def _claim_key(value: dict[str, Any]) -> tuple[str, str]:
    return value["id"], value["revision"]


def _reject_dependency_cycles(
    bindings: list[tuple[tuple[str, str], tuple[tuple[str, str], ...]]],
) -> None:
    graph = {dependent: set(requirements) for dependent, requirements in bindings}
    visiting: set[tuple[str, str]] = set()
    visited: set[tuple[str, str]] = set()

    def visit(node: tuple[str, str]) -> None:
        if node in visiting:
            raise DependencyGuardError("cyclic semantic dependency graph")
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph.get(node, set()):
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def validate_dependency_registry(
    registry: dict[str, Any],
    claim_index: dict[str, Any],
    entries: dict[tuple[str, str], dict[str, Any]],
) -> list[tuple[tuple[str, str], tuple[tuple[str, str], ...]]]:
    if registry.get("schema") != "accord.public-semantic-dependency-registry.v0.1":
        raise DependencyGuardError("unsupported semantic dependency registry schema")
    if registry.get("contract_revision") != "v0.1":
        raise DependencyGuardError("unsupported semantic dependency contract revision")

    normalized = []
    seen_dependents: set[tuple[str, str]] = set()
    for binding in registry["bindings"]:
        dependent = _claim_key(binding["dependent_claim"])
        if dependent in seen_dependents:
            raise DependencyGuardError(
                f"duplicate semantic dependency binding: {dependent[0]} {dependent[1]}"
            )
        seen_dependents.add(dependent)
        if dependent not in entries:
            raise DependencyGuardError(
                f"dependent claim revision is not registered: {dependent[0]} {dependent[1]}"
            )
        current = claim_index["claims"].get(dependent[0])
        if current is None or current["revision"] != dependent[1]:
            raise DependencyGuardError(
                "semantic dependency registry must bind the current dependent revision: "
                f"{dependent[0]} {dependent[1]}"
            )

        requirements: list[tuple[str, str]] = []
        seen_requirements: set[tuple[str, str]] = set()
        for requirement in binding["dependency_claims"]:
            if requirement["relation"] != DEPENDENCY_RELATION:
                raise DependencyGuardError(
                    f"unsupported semantic dependency relation: {requirement['relation']}"
                )
            required = _claim_key(requirement)
            if required == dependent:
                raise DependencyGuardError("claim revision cannot depend on itself")
            if required in seen_requirements:
                raise DependencyGuardError(
                    f"duplicate semantic dependency: {required[0]} {required[1]}"
                )
            seen_requirements.add(required)
            if required not in entries:
                raise DependencyGuardError(
                    f"dependency claim revision is not registered: {required[0]} {required[1]}"
                )
            requirements.append(required)
        if not requirements:
            raise DependencyGuardError(
                f"semantic dependency binding has no dependencies: {dependent[0]} {dependent[1]}"
            )
        normalized.append((dependent, tuple(requirements)))

    _reject_dependency_cycles(normalized)
    return normalized


def active_adjudications(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    superseded = {
        record["supersedes"]
        for record in records
        if isinstance(record.get("supersedes"), str)
    }
    return [
        record
        for record in records
        if record["adjudication_id"] not in superseded
    ]


def validate_failure_propagation(
    bindings: list[tuple[tuple[str, str], tuple[tuple[str, str], ...]]],
    records: list[dict[str, Any]],
    entries: dict[tuple[str, str], dict[str, Any]],
) -> int:
    adverse_targets = {
        _claim_key(record["claim"])
        for record in active_adjudications(records)
        if record["disposition"] in CONFIRMED_NEGATIVE_DISPOSITIONS
    }

    active_dependency_findings = 0
    for dependent, requirements in bindings:
        triggered = sorted(set(requirements) & adverse_targets)
        if not triggered:
            continue
        active_dependency_findings += len(triggered)
        state = entries[dependent]["publication_state"]
        if state == "PUBLISHED":
            rendered = ", ".join(f"{claim_id} {revision}" for claim_id, revision in triggered)
            raise DependencyGuardError(
                "dependent claim must not remain PUBLISHED while an active confirmed "
                f"negative finding targets semantic dependency {rendered}: "
                f"dependent={dependent[0]} {dependent[1]}"
            )
    return active_dependency_findings


def _load_adjudication_records(root: Path) -> list[dict[str, Any]]:
    index = _adjudication.load_json(root / "challenge" / "adjudications" / "index.json")
    records_root = (root / "challenge" / "adjudications" / "records").resolve()
    records: list[dict[str, Any]] = []
    for rel in index["records"]:
        path = (root / rel).resolve()
        try:
            path.relative_to(records_root)
        except ValueError as exc:
            raise DependencyGuardError(
                f"adjudication record escapes records directory: {rel}"
            ) from exc
        records.append(_adjudication.load_json(path))
    return records


def validate_repository(root: Path = ROOT) -> tuple[int, int]:
    # First require the existing adjudication governance to be internally valid.
    _adjudication.validate_repository(root)

    claim_index = _adjudication.load_json(root / "claims" / "public-claim-index.json")
    state_registry = _adjudication.load_json(root / "claims" / "public-claim-state.json")
    dependency_registry = _adjudication.load_json(
        root / "claims" / "public-semantic-dependencies.json"
    )
    entries = _adjudication.validate_state_registry(claim_index, state_registry)
    bindings = validate_dependency_registry(
        dependency_registry,
        claim_index,
        entries,
    )
    records = _load_adjudication_records(root)
    active_dependency_findings = validate_failure_propagation(
        bindings,
        records,
        entries,
    )
    edge_count = sum(len(requirements) for _, requirements in bindings)
    return edge_count, active_dependency_findings


def main() -> int:
    try:
        edge_count, active_dependency_findings = validate_repository()
    except (
        DependencyGuardError,
        _adjudication.AdjudicationError,
        KeyError,
        TypeError,
    ) as exc:
        print("SEMANTIC_DEPENDENCY_GUARD=FAIL")
        print(f"REASON={exc}")
        print("PRIVATE_REFERENCE_VERIFICATION=NOT_PERFORMED")
        return 1

    print("SEMANTIC_DEPENDENCY_GUARD=PASS")
    print(f"SEMANTIC_DEPENDENCY_EDGES={edge_count}")
    print(f"ACTIVE_DEPENDENCY_FINDINGS={active_dependency_findings}")
    print("PRIVATE_REFERENCE_VERIFICATION=NOT_PERFORMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
