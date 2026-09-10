#!/usr/bin/env python3
"""PROJECT ACCORD public challenge-submission validator.

This validator checks only public mechanical structure. It does not adjudicate
truth, scope, evidence authenticity, impact, or claim falsification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "accord-challenge-v0.3"
MAX_BYTES = 256 * 1024
MAX_DEPTH = 12
MAX_LIST_ITEMS = 100
MAX_STRING = 8000

ATTACK_CLASSES = {
    "EPISTEMIC_PROMOTION",
    "AUTHORITY_EXPANSION",
    "BOUNDARY_COLLAPSE",
    "LINEAGE_AMBIGUITY",
    "EVIDENCE_INCONSISTENCY",
    "SCOPE_ESCAPE",
    "SEMANTIC_OVERCLAIM",
    "OTHER",
}

SCOPE_POSITIONS = {
    "SUBMITTER_ASSERTED_IN_SCOPE",
    "SUBMITTER_UNCERTAIN",
    "SUBMITTER_ASSERTED_OUT_OF_SCOPE",
}

REQUIRED_SUBJECT_KEYS = {
    "ACCORD-C01": {"boundary"},
    "ACCORD-C02": {"boundary"},
    "ACCORD-C03": {"subject"},
    "ACCORD-C04": {"historical_subject", "historical_boundary"},
    "ACCORD-C05": {"historical_subject", "historical_cutoff"},
}

TOP_LEVEL_KEYS = {
    "schema_version", "challenge_id", "claim", "attack", "scope_position",
    "subject", "observations", "evidence", "counterexample", "notes"
}
REQUIRED_TOP_LEVEL = {
    "schema_version", "challenge_id", "claim", "attack", "scope_position",
    "subject", "observations", "evidence", "counterexample"
}

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class ValidationError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def _reject_duplicate_object_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValidationError(f"duplicate JSON object key: {key}")
        out[key] = value
    return out


def _reject_nonfinite(value: str) -> None:
    raise ValidationError(f"non-finite JSON number is not permitted: {value}")


def _nonempty_string(value: Any, path: str) -> str:
    _require(isinstance(value, str), f"{path} must be a string")
    _require(bool(value.strip()), f"{path} must not be empty")
    _require(len(value) <= MAX_STRING, f"{path} exceeds {MAX_STRING} characters")
    return value


def _walk_limits(value: Any, depth: int = 0, path: str = "$") -> None:
    _require(depth <= MAX_DEPTH, f"{path} exceeds maximum nesting depth {MAX_DEPTH}")
    if isinstance(value, str):
        _require(len(value) <= MAX_STRING, f"{path} exceeds {MAX_STRING} characters")
    elif isinstance(value, list):
        _require(len(value) <= MAX_LIST_ITEMS, f"{path} exceeds {MAX_LIST_ITEMS} items")
        for i, item in enumerate(value):
            _walk_limits(item, depth + 1, f"{path}[{i}]")
    elif isinstance(value, dict):
        _require(len(value) <= MAX_LIST_ITEMS, f"{path} contains too many keys")
        for key, item in value.items():
            _require(isinstance(key, str), f"{path} contains a non-string key")
            _walk_limits(item, depth + 1, f"{path}.{key}")
    else:
        _require(value is None or isinstance(value, (bool, int, float)),
                 f"{path} contains unsupported JSON type")


def canonical_bytes(document: dict[str, Any]) -> bytes:
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def load_json_file(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValidationError(str(exc)) from exc
    _require(len(raw) <= MAX_BYTES, f"{path.name} exceeds {MAX_BYTES} bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{path.name} is not valid UTF-8") from exc
    try:
        doc = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_object_keys,
            parse_constant=_reject_nonfinite,
        )
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValidationError(str(exc)) from exc
    _require(isinstance(doc, dict), f"{path.name} root must be an object")
    _walk_limits(doc)
    return doc, raw


def claim_index_path() -> Path:
    return Path(__file__).resolve().parent.parent / "claims" / "public-claim-index.json"


def load_claim_index() -> dict[str, Any]:
    doc, _ = load_json_file(claim_index_path())
    _require(doc.get("schema") == "accord.public-claim-index.v0.2",
             "unsupported public claim index schema")
    _require(doc.get("contract_revision") == "v0.2",
             "unexpected public claim contract revision")
    claims = doc.get("claims")
    _require(isinstance(claims, dict) and claims, "public claim index has no claims")
    return claims


def load_fixture(path: Path) -> tuple[dict[str, Any], bytes]:
    return load_json_file(path)


def _validate_claim(claim: Any, claims: dict[str, Any]) -> tuple[str, str]:
    _require(isinstance(claim, dict), "claim must be an object")
    _require(set(claim) == {"id", "revision", "falsification_id"},
             "claim must contain exactly id, revision and falsification_id")
    claim_id = _nonempty_string(claim.get("id"), "claim.id")
    revision = _nonempty_string(claim.get("revision"), "claim.revision")
    falsification_id = _nonempty_string(claim.get("falsification_id"), "claim.falsification_id")
    _require(claim_id in claims, f"unknown public claim: {claim_id}")
    entry = claims[claim_id]
    _require(isinstance(entry, dict), f"invalid claim-index entry for {claim_id}")
    _require(revision == entry.get("revision"),
             f"claim.revision must be {entry.get('revision')} for {claim_id}")
    ids = entry.get("falsification_ids")
    _require(isinstance(ids, list), f"missing falsification registry for {claim_id}")
    _require(falsification_id in ids,
             f"unknown falsification_id {falsification_id} for {claim_id}")
    return claim_id, falsification_id


def _validate_attack(attack: Any) -> None:
    _require(isinstance(attack, dict), "attack must be an object")
    required = {"class", "summary"}
    allowed = required | {"other_class"}
    _require(required.issubset(attack), "attack is missing required keys")
    _require(set(attack).issubset(allowed), "attack contains unknown keys")
    attack_class = _nonempty_string(attack.get("class"), "attack.class")
    _require(attack_class in ATTACK_CLASSES, f"unknown public attack tag: {attack_class}")
    _nonempty_string(attack.get("summary"), "attack.summary")
    if attack_class == "OTHER":
        _nonempty_string(attack.get("other_class"), "attack.other_class")
    else:
        _require("other_class" not in attack,
                 "attack.other_class is permitted only with OTHER")


def _validate_scope_position(scope: Any) -> str:
    _require(isinstance(scope, dict), "scope_position must be an object")
    _require(set(scope) == {"position", "justification"},
             "scope_position must contain exactly position and justification")
    position = _nonempty_string(scope.get("position"), "scope_position.position")
    _require(position in SCOPE_POSITIONS, f"invalid submitter scope position: {position}")
    _nonempty_string(scope.get("justification"), "scope_position.justification")
    return position


def _validate_subject(subject: Any, claim_id: str) -> None:
    _require(isinstance(subject, dict), "subject must be an object")
    _require(bool(subject), "subject must not be empty")
    _require(len(subject) <= 16, "subject has too many public fields")
    for key, value in subject.items():
        _nonempty_string(key, "subject key")
        _nonempty_string(value, f"subject.{key}")
    missing = REQUIRED_SUBJECT_KEYS[claim_id] - set(subject)
    _require(not missing, f"subject is missing claim-required keys: {sorted(missing)}")


def _validate_evidence(evidence: Any) -> set[str]:
    _require(isinstance(evidence, list) and evidence,
             "evidence must be a non-empty array")
    _require(len(evidence) <= MAX_LIST_ITEMS, "too many evidence entries")
    ids: set[str] = set()
    allowed_kinds = {"SELF_CONTAINED", "EXTERNAL_REFERENCE", "ATTACHED_ARTIFACT"}
    for i, item in enumerate(evidence):
        path = f"evidence[{i}]"
        _require(isinstance(item, dict), f"{path} must be an object")
        required = {"id", "kind", "description"}
        allowed = required | {"locator", "sha256"}
        _require(required.issubset(item), f"{path} is missing required keys")
        _require(set(item).issubset(allowed), f"{path} contains unknown keys")
        evidence_id = _nonempty_string(item.get("id"), f"{path}.id")
        _require(ID_RE.match(evidence_id) is not None, f"{path}.id has invalid format")
        _require(evidence_id not in ids, f"duplicate evidence id: {evidence_id}")
        ids.add(evidence_id)
        kind = _nonempty_string(item.get("kind"), f"{path}.kind")
        _require(kind in allowed_kinds, f"{path}.kind is invalid")
        _nonempty_string(item.get("description"), f"{path}.description")
        if kind in {"EXTERNAL_REFERENCE", "ATTACHED_ARTIFACT"}:
            _nonempty_string(item.get("locator"), f"{path}.locator")
        if "sha256" in item:
            digest = _nonempty_string(item.get("sha256"), f"{path}.sha256")
            _require(SHA256_RE.match(digest) is not None,
                     f"{path}.sha256 must be 64 hexadecimal characters")
    return ids


def _validate_observations(observations: Any, evidence_ids: set[str]) -> None:
    _require(isinstance(observations, list) and observations,
             "observations must be a non-empty array")
    _require(len(observations) <= MAX_LIST_ITEMS, "too many observations")
    ids: set[str] = set()
    for i, item in enumerate(observations):
        path = f"observations[{i}]"
        _require(isinstance(item, dict), f"{path} must be an object")
        _require(set(item) == {"id", "statement", "evidence_refs"},
                 f"{path} has invalid keys")
        obs_id = _nonempty_string(item.get("id"), f"{path}.id")
        _require(ID_RE.match(obs_id) is not None, f"{path}.id has invalid format")
        _require(obs_id not in ids, f"duplicate observation id: {obs_id}")
        ids.add(obs_id)
        _nonempty_string(item.get("statement"), f"{path}.statement")
        refs = item.get("evidence_refs")
        _require(isinstance(refs, list) and refs,
                 f"{path}.evidence_refs must be non-empty")
        _require(len(refs) == len(set(refs)),
                 f"{path}.evidence_refs contains duplicates")
        for ref in refs:
            ref = _nonempty_string(ref, f"{path}.evidence_refs[]")
            _require(ref in evidence_ids,
                     f"{path} references unknown evidence id: {ref}")


def _validate_counterexample(counterexample: Any) -> None:
    _require(isinstance(counterexample, dict), "counterexample must be an object")
    _require(set(counterexample) == {"reasoning"}, "counterexample has invalid keys")
    _nonempty_string(counterexample.get("reasoning"), "counterexample.reasoning")


def validate_fixture(document: dict[str, Any]) -> dict[str, Any]:
    _require(set(document).issubset(TOP_LEVEL_KEYS),
             f"unknown top-level keys: {sorted(set(document) - TOP_LEVEL_KEYS)}")
    _require(REQUIRED_TOP_LEVEL.issubset(document),
             f"missing top-level keys: {sorted(REQUIRED_TOP_LEVEL - set(document))}")
    _require(document.get("schema_version") == SCHEMA_VERSION,
             f"schema_version must be {SCHEMA_VERSION}")
    _nonempty_string(document.get("challenge_id"), "challenge_id")

    claims = load_claim_index()
    claim_id, falsification_id = _validate_claim(document.get("claim"), claims)
    _validate_attack(document.get("attack"))
    scope_position = _validate_scope_position(document.get("scope_position"))
    _validate_subject(document.get("subject"), claim_id)
    evidence_ids = _validate_evidence(document.get("evidence"))
    _validate_observations(document.get("observations"), evidence_ids)
    _validate_counterexample(document.get("counterexample"))
    if "notes" in document:
        _nonempty_string(document.get("notes"), "notes")

    return {
        "status": "WELL_FORMED_CHALLENGE_SUBMISSION",
        "scope_position": scope_position,
        "judgment": "NOT_PERFORMED",
        "claim": claim_id,
        "falsification_id": falsification_id,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args(argv)
    try:
        document, raw = load_fixture(args.fixture)
        result = validate_fixture(document)
        result["input_sha256"] = hashlib.sha256(raw).hexdigest()
        result["canonical_sha256"] = hashlib.sha256(canonical_bytes(document)).hexdigest()
    except ValidationError as exc:
        print("status = INVALID_CHALLENGE_SUBMISSION")
        print("judgment = NOT_PERFORMED")
        print(f"reason = {exc}")
        return 1

    for key in [
        "status", "scope_position", "judgment", "claim",
        "falsification_id", "input_sha256", "canonical_sha256"
    ]:
        print(f"{key} = {result[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
