#!/usr/bin/env python3
"""Validate PROJECT ACCORD public challenge-adjudication governance.

This module validates public bindings and consequence invariants only. It does not decide
truth, scope, evidence authenticity, claim correctness, or the private reference.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

FINAL_DISPOSITIONS = {
    "CONFIRMED_FALSIFICATION",
    "REJECTED_OUT_OF_SCOPE",
    "INSUFFICIENT_EVIDENCE",
    "NOT_CONFIRMED",
}
REVIEW_CLASSES = {
    "PROJECT_ADJUDICATED",
    "EXTERNAL_INDEPENDENT",
    "MULTI_PARTY_REVIEWED",
}
STATE_BY_ACTION = {
    "CLAIM_SUSPENDED": "SUSPENDED",
    "CLAIM_WITHDRAWN": "WITHDRAWN",
    "CLAIM_SUPERSEDED": "SUPERSEDED",
}


class AdjudicationError(ValueError):
    pass


def _reject_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise AdjudicationError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, AdjudicationError) as exc:
        raise AdjudicationError(f"{path}: {exc}") from exc



def canonical_json_sha256(path: Path) -> str:
    document = load_json(path)
    canonical = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _state_entries(state_registry: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    entries: dict[tuple[str, str], dict[str, Any]] = {}
    for entry in state_registry["entries"]:
        key = (entry["id"], entry["revision"])
        if key in entries:
            raise AdjudicationError(f"duplicate claim state entry: {key[0]} {key[1]}")
        entries[key] = entry
    return entries


def validate_state_registry(
    claim_index: dict[str, Any],
    state_registry: dict[str, Any],
) -> dict[tuple[str, str], dict[str, Any]]:
    entries = _state_entries(state_registry)

    for claim_id, current in claim_index["claims"].items():
        key = (claim_id, current["revision"])
        if key not in entries:
            raise AdjudicationError(
                f"current claim missing from state registry: {claim_id} {current['revision']}"
            )
        state = entries[key]
        if state["publication_state"] in {"WITHDRAWN", "SUPERSEDED"}:
            raise AdjudicationError(
                f"current claim index points to non-current state: {claim_id} "
                f"{current['revision']}={state['publication_state']}"
            )
        if state["falsification_ids"] != current["falsification_ids"]:
            raise AdjudicationError(
                f"falsification registry drift: {claim_id} {current['revision']}"
            )

    return entries


def _require_nonempty_list(detail: dict[str, Any], field: str, message: str) -> None:
    value = detail.get(field)
    if not isinstance(value, list) or not value:
        raise AdjudicationError(message)


def _require_nonempty_string(detail: dict[str, Any], field: str, message: str) -> None:
    value = detail.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AdjudicationError(message)


def validate_record(
    record: dict[str, Any],
    entries: dict[tuple[str, str], dict[str, Any]],
    root: Path | None = None,
) -> None:
    challenge = record["challenge"]
    public_artifact_path = challenge.get("public_artifact_path")
    if public_artifact_path is not None:
        if root is None:
            raise AdjudicationError(
                "public_artifact_path validation requires repository root"
            )
        artifact = root / public_artifact_path
        submissions_root = (root / "challenge" / "submissions").resolve()
        try:
            resolved = artifact.resolve()
            resolved.relative_to(submissions_root)
        except (OSError, ValueError) as exc:
            raise AdjudicationError(
                "public challenge artifact escapes challenge/submissions"
            ) from exc
        if not artifact.is_file():
            raise AdjudicationError(
                f"public challenge artifact not found: {public_artifact_path}"
            )
        actual = canonical_json_sha256(artifact)
        if actual != challenge["canonical_sha256"]:
            raise AdjudicationError(
                "public challenge artifact canonical SHA-256 mismatch"
            )

    claim = record["claim"]
    key = (claim["id"], claim["revision"])
    state = entries.get(key)
    if state is None:
        raise AdjudicationError(
            f"adjudication targets unregistered claim revision: {key[0]} {key[1]}"
        )
    if claim["falsification_id"] not in state["falsification_ids"]:
        raise AdjudicationError(
            f"unregistered falsification id for {key[0]} {key[1]}: "
            f"{claim['falsification_id']}"
        )

    disposition = record["disposition"]
    if disposition not in FINAL_DISPOSITIONS:
        raise AdjudicationError(f"unsupported completed disposition: {disposition}")
    if record["review_class"] not in REVIEW_CLASSES:
        raise AdjudicationError(f"unsupported review class: {record['review_class']}")

    detail = record["decision_detail"]
    _require_nonempty_string(detail, "basis", "adjudication basis must be non-empty")

    consequence = record.get("consequence")

    if disposition == "CONFIRMED_FALSIFICATION":
        _require_nonempty_list(
            detail,
            "evidence_references",
            "confirmed falsification requires public evidence references",
        )
        _require_nonempty_string(
            detail,
            "falsification_analysis",
            "confirmed falsification requires a falsification analysis",
        )
        if not isinstance(consequence, dict):
            raise AdjudicationError("confirmed falsification requires a claim consequence")
        if (
            consequence["claim_id"] != claim["id"]
            or consequence["claim_revision"] != claim["revision"]
        ):
            raise AdjudicationError("claim consequence must bind to the adjudicated revision")
        action = consequence["action"]
        expected_state = STATE_BY_ACTION.get(action)
        if expected_state is None:
            raise AdjudicationError(f"unsupported claim consequence action: {action}")
        if state["publication_state"] != expected_state:
            raise AdjudicationError(
                "confirmed falsification consequence/state mismatch: "
                f"{action} requires {expected_state}, found {state['publication_state']}"
            )
        if state["publication_state"] == "PUBLISHED":
            raise AdjudicationError(
                "confirmed falsification cannot coexist with affected revision PUBLISHED"
            )

        replacement = consequence.get("replacement_revision")
        if action == "CLAIM_SUPERSEDED":
            if not replacement:
                raise AdjudicationError(
                    "CLAIM_SUPERSEDED requires replacement_revision"
                )
            replacement_state = entries.get((claim["id"], replacement))
            if replacement_state is None:
                raise AdjudicationError(
                    "replacement revision is not registered in public claim state"
                )
            if replacement_state["publication_state"] != "PUBLISHED":
                raise AdjudicationError(
                    "replacement revision must be PUBLISHED"
                )
        elif replacement is not None:
            raise AdjudicationError(
                "replacement_revision is only valid for CLAIM_SUPERSEDED"
            )
        return

    if consequence is not None:
        raise AdjudicationError(
            "non-confirmed disposition must not carry a claim consequence"
        )

    if disposition == "REJECTED_OUT_OF_SCOPE":
        _require_nonempty_list(
            detail,
            "public_rule_references",
            "out-of-scope rejection requires public rule references",
        )
    elif disposition == "INSUFFICIENT_EVIDENCE":
        _require_nonempty_string(
            detail,
            "missing_evidence_statement",
            "insufficient-evidence disposition requires missing_evidence_statement",
        )
    elif disposition == "NOT_CONFIRMED":
        _require_nonempty_string(
            detail,
            "falsification_analysis",
            "not-confirmed disposition requires falsification_analysis",
        )


def validate_repository(root: Path = ROOT) -> tuple[int, int]:
    claim_index = load_json(root / "claims" / "public-claim-index.json")
    state_registry = load_json(root / "claims" / "public-claim-state.json")
    adjudication_index = load_json(root / "challenge" / "adjudications" / "index.json")

    entries = validate_state_registry(claim_index, state_registry)
    record_count = 0
    confirmed_count = 0
    seen_paths: set[str] = set()

    for rel in adjudication_index["records"]:
        if rel in seen_paths:
            raise AdjudicationError(f"duplicate adjudication record path: {rel}")
        seen_paths.add(rel)

        path = root / rel
        records_root = (root / "challenge" / "adjudications" / "records").resolve()
        try:
            resolved = path.resolve()
            resolved.relative_to(records_root)
        except (OSError, ValueError) as exc:
            raise AdjudicationError(
                f"adjudication record escapes records directory: {rel}"
            ) from exc

        if not path.is_file():
            raise AdjudicationError(f"adjudication record not found: {rel}")

        record = load_json(path)
        validate_record(record, entries, root=root)
        record_count += 1
        if record["disposition"] == "CONFIRMED_FALSIFICATION":
            confirmed_count += 1

    return record_count, confirmed_count


def main() -> int:
    try:
        record_count, confirmed_count = validate_repository()
    except (AdjudicationError, KeyError, TypeError) as exc:
        print("ADJUDICATION_GOVERNANCE_CHECK=FAIL")
        print(f"REASON={exc}")
        print("PRIVATE_REFERENCE_VERIFICATION=NOT_PERFORMED")
        return 1

    print("ADJUDICATION_GOVERNANCE_CHECK=PASS")
    print(f"ADJUDICATION_RECORDS={record_count}")
    print(f"CONFIRMED_FALSIFICATIONS={confirmed_count}")
    print("PRIVATE_REFERENCE_VERIFICATION=NOT_PERFORMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
