#!/usr/bin/env python3
"""Validate PROJECT ACCORD public challenge lifecycle and adjudication governance.

This module validates public bindings and governance invariants only. It does not decide
truth, scope, evidence authenticity, claim correctness, or the private reference.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

FINAL_DISPOSITIONS = {
    "CONFIRMED_FALSIFICATION",
    "CONFIRMED_CONTRACT_GAP",
    "REJECTED_OUT_OF_SCOPE",
    "INSUFFICIENT_EVIDENCE",
    "NOT_CONFIRMED",
}
REVIEW_CLASSES = {
    "PROJECT_ADJUDICATED",
    "EXTERNAL_INDEPENDENT",
    "MULTI_PARTY_REVIEWED",
}
CHALLENGE_TYPES = {
    "REGISTERED_FALSIFICATION",
    "NOVEL_FALSIFICATION_HYPOTHESIS",
}
RECEIPT_STATES = {
    "RECEIVED",
    "MECHANICALLY_VALID",
    "UNDER_REVIEW",
    "COMPLETED",
    "INVALID_SUBMISSION",
}
STATE_BY_ACTION = {
    "CLAIM_SUSPENDED": "SUSPENDED",
    "CLAIM_WITHDRAWN": "WITHDRAWN",
    "CLAIM_SUPERSEDED": "SUPERSEDED",
}
DECISION_AUTHORITY_BASIS = (
    "challenge/ADJUDICATION-CONTRACT.md#decision-authority-versus-review-provenance"
)


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


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise AdjudicationError(f"{field} must be an RFC3339 UTC timestamp ending in Z")
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise AdjudicationError(f"{field} is not a valid RFC3339 timestamp") from exc


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
                f"current claim index points to non-current state: "
                f"{claim_id} {current['revision']}={state['publication_state']}"
            )
        if state["falsification_ids"] != current["falsification_ids"]:
            raise AdjudicationError(
                f"falsification registry drift: {claim_id} {current['revision']}"
            )
    return entries


def validate_receipts(
    receipt_index: dict[str, Any],
    entries: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    if receipt_index.get("schema") != "accord.challenge-receipt-index.v0.1":
        raise AdjudicationError("unsupported challenge receipt index schema")
    receipts: dict[str, dict[str, Any]] = {}
    digests: dict[str, str] = {}
    for receipt in receipt_index["records"]:
        receipt_id = receipt["receipt_id"]
        if receipt_id in receipts:
            raise AdjudicationError(f"duplicate receipt id: {receipt_id}")
        digest = receipt["canonical_sha256"]
        prior = digests.get(digest)
        if prior is not None and prior != receipt_id:
            raise AdjudicationError(
                f"duplicate canonical challenge content across receipts: {prior}, {receipt_id}"
            )
        digests[digest] = receipt_id

        claim = receipt["claim"]
        key = (claim["id"], claim["revision"])
        state = entries.get(key)
        if state is None:
            raise AdjudicationError(
                f"receipt targets unregistered claim revision: {key[0]} {key[1]}"
            )
        challenge_type = receipt["challenge_type"]
        if challenge_type not in CHALLENGE_TYPES:
            raise AdjudicationError(f"unsupported receipt challenge type: {challenge_type}")
        falsification_id = claim.get("falsification_id")
        novel = receipt.get("novel_hypothesis")
        if challenge_type == "REGISTERED_FALSIFICATION":
            if falsification_id not in state["falsification_ids"]:
                raise AdjudicationError(
                    f"registered challenge requires published falsification id for {key[0]}"
                )
            if novel is not None:
                raise AdjudicationError(
                    "registered falsification receipt must not carry novel_hypothesis"
                )
        else:
            if falsification_id is not None:
                raise AdjudicationError(
                    "novel falsification hypothesis must not pretend to use a registered id"
                )
            if not isinstance(novel, dict):
                raise AdjudicationError(
                    "novel falsification hypothesis requires novel_hypothesis detail"
                )
            for field in (
                "alleged_claim_contradiction",
                "reason_no_registered_falsification_id_applies",
            ):
                if not isinstance(novel.get(field), str) or not novel[field].strip():
                    raise AdjudicationError(
                        f"novel falsification hypothesis requires {field}"
                    )

        if receipt["status"] not in RECEIPT_STATES:
            raise AdjudicationError(f"unsupported receipt state: {receipt['status']}")
        received_at = _parse_timestamp(receipt["received_at"], "received_at")
        changed_at = _parse_timestamp(
            receipt["last_status_change_at"], "last_status_change_at"
        )
        if changed_at < received_at:
            raise AdjudicationError(
                f"receipt {receipt_id} last status change predates receipt"
            )
        if not isinstance(receipt.get("public_locator"), str) or not receipt["public_locator"].strip():
            raise AdjudicationError(f"receipt {receipt_id} requires public_locator")
        receipts[receipt_id] = receipt
    return receipts


def _require_nonempty_list(detail: dict[str, Any], field: str, message: str) -> None:
    value = detail.get(field)
    if not isinstance(value, list) or not value:
        raise AdjudicationError(message)


def _require_nonempty_string(detail: dict[str, Any], field: str, message: str) -> None:
    value = detail.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AdjudicationError(message)


def _binding(record: dict[str, Any]) -> tuple[str, str, str, str, str | None]:
    challenge = record["challenge"]
    claim = record["claim"]
    return (
        challenge["canonical_sha256"],
        claim["id"],
        claim["revision"],
        challenge["challenge_type"],
        claim.get("falsification_id"),
    )


def validate_record(
    record: dict[str, Any],
    entries: dict[tuple[str, str], dict[str, Any]],
    receipts: dict[str, dict[str, Any]],
) -> None:
    if record.get("schema") != "accord.challenge-adjudication-record.v0.2":
        raise AdjudicationError("unsupported adjudication record schema")

    challenge = record["challenge"]
    claim = record["claim"]
    key = (claim["id"], claim["revision"])
    state = entries.get(key)
    if state is None:
        raise AdjudicationError(
            f"adjudication targets unregistered claim revision: {key[0]} {key[1]}"
        )

    challenge_type = challenge["challenge_type"]
    if challenge_type not in CHALLENGE_TYPES:
        raise AdjudicationError(f"unsupported challenge type: {challenge_type}")
    falsification_id = claim.get("falsification_id")
    if challenge_type == "REGISTERED_FALSIFICATION":
        if falsification_id not in state["falsification_ids"]:
            raise AdjudicationError(
                f"unregistered falsification id for {key[0]} {key[1]}: {falsification_id}"
            )
    elif falsification_id is not None:
        raise AdjudicationError(
            "novel falsification adjudication must not carry registered falsification_id"
        )

    visibility = challenge["visibility"]
    if visibility == "PUBLIC":
        receipt_id = challenge.get("receipt_id")
        locator = challenge.get("public_locator")
        if not receipt_id or not locator:
            raise AdjudicationError(
                "public adjudication requires receipt_id and public_locator"
            )
        receipt = receipts.get(receipt_id)
        if receipt is None:
            raise AdjudicationError(f"public adjudication references unknown receipt: {receipt_id}")
        if receipt["status"] != "COMPLETED":
            raise AdjudicationError(
                f"public adjudication receipt must be COMPLETED: {receipt_id}"
            )
        if receipt["canonical_sha256"] != challenge["canonical_sha256"]:
            raise AdjudicationError("public adjudication digest does not match receipt")
        if receipt["public_locator"] != locator:
            raise AdjudicationError("public adjudication locator does not match receipt")
        if receipt["challenge_type"] != challenge_type:
            raise AdjudicationError("public adjudication challenge type does not match receipt")
        receipt_claim = receipt["claim"]
        if receipt_claim["id"] != claim["id"] or receipt_claim["revision"] != claim["revision"]:
            raise AdjudicationError("public adjudication claim binding does not match receipt")
        if receipt_claim.get("falsification_id") != falsification_id:
            raise AdjudicationError(
                "public adjudication falsification binding does not match receipt"
            )
    elif visibility == "CONFIDENTIAL_SECURITY":
        if "receipt_id" in challenge or "public_locator" in challenge:
            raise AdjudicationError(
                "confidential adjudication must not expose public receipt or locator"
            )
    else:
        raise AdjudicationError(f"unsupported challenge visibility: {visibility}")

    provenance = record["review_provenance"]
    review_class = provenance["review_class"]
    reviewers = provenance["reviewers"]
    if review_class not in REVIEW_CLASSES:
        raise AdjudicationError(f"unsupported review class: {review_class}")
    identifiers = [r["identifier"] for r in reviewers]
    if not identifiers or len(identifiers) != len(set(identifiers)):
        raise AdjudicationError("reviewers must be non-empty and uniquely identified")
    if review_class == "EXTERNAL_INDEPENDENT":
        if not any(r["relationship"] == "EXTERNAL" for r in reviewers):
            raise AdjudicationError(
                "EXTERNAL_INDEPENDENT requires at least one external reviewer"
            )
        _require_nonempty_string(
            provenance,
            "independence_basis",
            "EXTERNAL_INDEPENDENT requires independence_basis",
        )
    if review_class == "MULTI_PARTY_REVIEWED" and len(reviewers) < 2:
        raise AdjudicationError("MULTI_PARTY_REVIEWED requires at least two reviewers")

    authority = record["decision_authority"]
    if authority["class"] != "PROJECT_MAINTAINER":
        raise AdjudicationError("unsupported decision authority class")
    _require_nonempty_string(authority, "actor", "decision authority actor is required")
    if authority.get("authority_basis") != DECISION_AUTHORITY_BASIS:
        raise AdjudicationError(
            "decision authority basis must bind to the current public adjudication contract"
        )
    _parse_timestamp(authority["decided_at"], "decision_authority.decided_at")

    disposition = record["disposition"]
    if disposition not in FINAL_DISPOSITIONS:
        raise AdjudicationError(f"unsupported completed disposition: {disposition}")
    if disposition == "CONFIRMED_FALSIFICATION" and challenge_type != "REGISTERED_FALSIFICATION":
        raise AdjudicationError(
            "CONFIRMED_FALSIFICATION requires REGISTERED_FALSIFICATION challenge type"
        )
    if disposition == "CONFIRMED_CONTRACT_GAP" and challenge_type != "NOVEL_FALSIFICATION_HYPOTHESIS":
        raise AdjudicationError(
            "CONFIRMED_CONTRACT_GAP requires NOVEL_FALSIFICATION_HYPOTHESIS"
        )

    detail = record["decision_detail"]
    _require_nonempty_string(detail, "basis", "adjudication basis must be non-empty")
    consequence = record.get("consequence")

    if disposition in {"CONFIRMED_FALSIFICATION", "CONFIRMED_CONTRACT_GAP"}:
        _require_nonempty_list(
            detail,
            "evidence_references",
            "confirmed disposition requires public evidence references",
        )
        if disposition == "CONFIRMED_FALSIFICATION":
            _require_nonempty_string(
                detail,
                "falsification_analysis",
                "confirmed falsification requires falsification_analysis",
            )
        else:
            _require_nonempty_string(
                detail,
                "contract_gap_analysis",
                "confirmed contract gap requires contract_gap_analysis",
            )
        if not isinstance(consequence, dict):
            raise AdjudicationError("confirmed disposition requires a claim consequence")
        if (
            consequence["claim_id"] != claim["id"]
            or consequence["claim_revision"] != claim["revision"]
        ):
            raise AdjudicationError("claim consequence must bind to adjudicated revision")
        action = consequence["action"]
        expected_state = STATE_BY_ACTION.get(action)
        if expected_state is None:
            raise AdjudicationError(f"unsupported claim consequence action: {action}")
        if state["publication_state"] != expected_state:
            raise AdjudicationError(
                "confirmed disposition consequence/state mismatch: "
                f"{action} requires {expected_state}, found {state['publication_state']}"
            )
        replacement = consequence.get("replacement_revision")
        if action == "CLAIM_SUPERSEDED":
            if not replacement:
                raise AdjudicationError("CLAIM_SUPERSEDED requires replacement_revision")
            replacement_state = entries.get((claim["id"], replacement))
            if replacement_state is None or replacement_state["publication_state"] != "PUBLISHED":
                raise AdjudicationError("replacement revision must exist and be PUBLISHED")
        elif replacement is not None:
            raise AdjudicationError(
                "replacement_revision is valid only for CLAIM_SUPERSEDED"
            )
        return

    if consequence is not None:
        raise AdjudicationError("non-confirmed disposition must not carry claim consequence")
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


def validate_adjudication_set(
    records: list[dict[str, Any]],
    entries: dict[tuple[str, str], dict[str, Any]],
    receipts: dict[str, dict[str, Any]],
) -> tuple[int, int]:
    by_id: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = record["adjudication_id"]
        if record_id in by_id:
            raise AdjudicationError(f"duplicate adjudication id: {record_id}")
        validate_record(record, entries, receipts)
        by_id[record_id] = record

    superseded_by: dict[str, str] = {}
    for record_id, record in by_id.items():
        prior_id = record.get("supersedes")
        if prior_id is None:
            continue
        if prior_id == record_id:
            raise AdjudicationError("adjudication cannot supersede itself")
        prior = by_id.get(prior_id)
        if prior is None:
            raise AdjudicationError(
                f"adjudication {record_id} supersedes unknown adjudication {prior_id}"
            )
        if prior_id in superseded_by:
            raise AdjudicationError(
                f"forked adjudication supersession from {prior_id}"
            )
        if _binding(prior) != _binding(record):
            raise AdjudicationError(
                "supersession must preserve exact challenge and claim binding"
            )
        superseded_by[prior_id] = record_id

    for start in by_id:
        seen: set[str] = set()
        current = start
        while current in superseded_by:
            if current in seen:
                raise AdjudicationError("cyclic adjudication supersession")
            seen.add(current)
            current = superseded_by[current]

    active_by_binding: dict[tuple[str, str, str, str, str | None], str] = {}
    active_records = 0
    confirmed_active = 0
    for record_id, record in by_id.items():
        if record_id in superseded_by:
            continue
        binding = _binding(record)
        prior_active = active_by_binding.get(binding)
        if prior_active is not None:
            raise AdjudicationError(
                "multiple active final adjudications for one exact binding: "
                f"{prior_active}, {record_id}"
            )
        active_by_binding[binding] = record_id
        active_records += 1
        if record["disposition"] in {"CONFIRMED_FALSIFICATION", "CONFIRMED_CONTRACT_GAP"}:
            confirmed_active += 1

    completed_receipts = {
        receipt_id
        for receipt_id, receipt in receipts.items()
        if receipt["status"] == "COMPLETED"
    }
    final_receipts = {
        record["challenge"]["receipt_id"]
        for record in by_id.values()
        if record["challenge"]["visibility"] == "PUBLIC"
        and record["adjudication_id"] not in superseded_by
    }
    missing = completed_receipts - final_receipts
    if missing:
        raise AdjudicationError(
            f"completed receipt lacks active final adjudication: {sorted(missing)}"
        )
    return active_records, confirmed_active


def validate_repository(root: Path = ROOT) -> tuple[int, int, int]:
    claim_index = load_json(root / "claims" / "public-claim-index.json")
    state_registry = load_json(root / "claims" / "public-claim-state.json")
    receipt_index = load_json(root / "challenge" / "receipts" / "index.json")
    adjudication_index = load_json(root / "challenge" / "adjudications" / "index.json")

    entries = validate_state_registry(claim_index, state_registry)
    receipts = validate_receipts(receipt_index, entries)

    if adjudication_index.get("schema") != "accord.challenge-adjudication-index.v0.2":
        raise AdjudicationError("unsupported adjudication index schema")

    records: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for rel in adjudication_index["records"]:
        if rel in seen_paths:
            raise AdjudicationError(f"duplicate adjudication record path: {rel}")
        seen_paths.add(rel)
        path = root / rel
        records_root = (root / "challenge" / "adjudications" / "records").resolve()
        try:
            path.resolve().relative_to(records_root)
        except (OSError, ValueError) as exc:
            raise AdjudicationError(
                f"adjudication record escapes records directory: {rel}"
            ) from exc
        if not path.is_file():
            raise AdjudicationError(f"adjudication record not found: {rel}")
        records.append(load_json(path))

    active, confirmed = validate_adjudication_set(records, entries, receipts)
    return len(receipts), active, confirmed


def main() -> int:
    try:
        receipt_count, active_count, confirmed_count = validate_repository()
    except (AdjudicationError, KeyError, TypeError) as exc:
        print("ADJUDICATION_GOVERNANCE_CHECK=FAIL")
        print(f"REASON={exc}")
        print("PRIVATE_REFERENCE_VERIFICATION=NOT_PERFORMED")
        return 1

    print("ADJUDICATION_GOVERNANCE_CHECK=PASS")
    print(f"PUBLIC_CHALLENGE_RECEIPTS={receipt_count}")
    print(f"ACTIVE_FINAL_ADJUDICATIONS={active_count}")
    print(f"CONFIRMED_ACTIVE_FINDINGS={confirmed_count}")
    print("PRIVATE_REFERENCE_VERIFICATION=NOT_PERFORMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
