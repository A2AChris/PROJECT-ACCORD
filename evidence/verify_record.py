#!/usr/bin/env python3
"""Self-check a sanitized PROJECT ACCORD public evidence record.

This validates only the public record's deterministic integrity and public
cross-field invariants. It does not open the private reference commitment and
does not verify the private implementation or private CI.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


class RecordError(ValueError):
    pass


def _reject_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise RecordError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_record(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError, RecordError) as exc:
        raise RecordError(str(exc)) from exc


def canonical_digest(record: dict) -> str:
    clone = json.loads(json.dumps(record, ensure_ascii=False))
    integrity = clone.get("integrity")
    if not isinstance(integrity, dict):
        raise RecordError("missing integrity object")
    integrity["record_sha256"] = None
    raw = json.dumps(clone, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_record(record: dict) -> None:
    if record.get("schema") != "accord.public-evidence-record.v0.5":
        raise RecordError("unsupported schema")
    if record.get("project") != "PROJECT ACCORD":
        raise RecordError("unexpected project")

    ref = record.get("public_reference")
    classification = record.get("evidence_classification")
    ci = record.get("ci_summary")
    integrity = record.get("integrity")
    if not all(isinstance(x, dict) for x in (ref, classification, ci, integrity)):
        raise RecordError("missing required object")

    if ref.get("alias") != "ACCORD-RM01":
        raise RecordError("unexpected public reference alias")
    if ref.get("status") != "PROVISIONALLY_FROZEN":
        raise RecordError("unexpected current public reference lifecycle status")
    commitment = ref.get("private_reference_commitment")
    if not isinstance(commitment, dict):
        raise RecordError("missing private reference commitment")
    if commitment.get("algorithm") != "SHA-256":
        raise RecordError("unexpected commitment algorithm")
    digest = commitment.get("commitment")
    if not isinstance(digest, str) or len(digest) != 64:
        raise RecordError("invalid private reference commitment")

    if classification.get("reference_evidence_level") != "R0_PROJECT_ATTESTED":
        raise RecordError("unexpected reference evidence level")
    if classification.get("public_challenge_contract") != "STRUCTURED_COUNTEREXAMPLE_SURFACE_PRESENT":
        raise RecordError("unexpected public challenge contract classification")
    if classification.get("public_reproduction_level") != "NOT_CLAIMED":
        raise RecordError("public reproduction must not be implied")
    qualification = classification.get("qualification", "")
    if "This provisionally frozen public evidence record" not in qualification:
        raise RecordError("current record lifecycle qualification is missing")
    if "public_reference.status value is record-lifecycle metadata" not in qualification:
        raise RecordError("record-lifecycle semantic separation is missing")
    if "does not classify the historical execution lineage as provisional, committed, executed, effective, or final" not in qualification:
        raise RecordError("record status is not separated from historical-lineage semantics")
    if "R1 means structured public challengeability" not in qualification:
        raise RecordError("R1 challengeability qualification is missing")
    if "External empirical generation of private-reference traces is not currently claimed." not in qualification:
        raise RecordError("private-reference trace-generation limitation is missing")

    binding = record.get("claim_binding")
    if not isinstance(binding, dict):
        raise RecordError("missing claim binding")
    evidenced = binding.get("evidenced_public_claim")
    if evidenced != {"id": "ACCORD-C05", "revision": "v0.3"}:
        raise RecordError("evidence record must bind only to ACCORD-C05 v0.3")
    dependencies = binding.get("semantic_dependencies_not_independently_evidenced")
    if not isinstance(dependencies, list):
        raise RecordError("missing semantic dependency classification")
    dep_ids = {(d.get("id"), d.get("revision")) for d in dependencies if isinstance(d, dict)}
    if dep_ids != {("ACCORD-C03", "v0.2"), ("ACCORD-C04", "v0.2")}:
        raise RecordError("unexpected semantic dependency classification")

    profiles = ci.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise RecordError("missing project-attested CI profiles")
    for profile in profiles:
        if not isinstance(profile, dict):
            raise RecordError("invalid CI profile")
        passed, total = profile.get("passed"), profile.get("total")
        if not isinstance(passed, int) or not isinstance(total, int) or total <= 0:
            raise RecordError("invalid test-count attestation")
        if passed != total:
            raise RecordError("record does not attest a fully passing profile")

    forbidden = record.get("forbidden_inferences")
    if not isinstance(forbidden, list):
        raise RecordError("missing forbidden inference registry")
    if "PROVISIONALLY_FROZEN public-reference status means that the historical execution lineage is provisional or uncommitted." not in forbidden:
        raise RecordError("provisional-status lineage inference is not forbidden")
    if "FROZEN public-reference status is required for the C05 term 'committed' to apply to the historical execution lineage." not in forbidden:
        raise RecordError("frozen-status committed-lineage inference is not forbidden")

    stored = integrity.get("record_sha256")
    if not isinstance(stored, str) or len(stored) != 64:
        raise RecordError("invalid record digest")
    if canonical_digest(record) != stored:
        raise RecordError("record digest mismatch")


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    path = Path(argv[0]) if argv else Path(__file__).with_name("ACCORD-RM01-REFERENCE-EVIDENCE-v0.7.json")
    try:
        record = load_record(path)
        validate_record(record)
    except RecordError as exc:
        print("PUBLIC_RECORD_SELF_CHECK=FAIL")
        print(f"REASON={exc}")
        print("PRIVATE_REFERENCE_OPENING=NOT_PERFORMED")
        print("REFERENCE_VERIFICATION=NOT_PERFORMED")
        return 1

    print("PUBLIC_RECORD_SELF_CHECK=PASS")
    print(f"RECORD_ID={record['record_id']}")
    print(f"PUBLIC_REFERENCE={record['public_reference']['alias']}")
    print(f"PUBLIC_REFERENCE_STATUS={record['public_reference']['status']}")
    print(f"PRIVATE_REFERENCE_COMMITMENT={record['public_reference']['private_reference_commitment']['commitment']}")
    print(f"RECORD_SHA256={record['integrity']['record_sha256']}")
    print("PRIVATE_REFERENCE_OPENING=NOT_PERFORMED")
    print("REFERENCE_VERIFICATION=NOT_PERFORMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
