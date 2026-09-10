#!/usr/bin/env python3
"""Cross-platform validation of the PROJECT ACCORD public candidate.

This script validates only public artifacts. It does not access, open, or verify
the private reference implementation.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIRS = {"__pycache__", ".pytest_cache", ".git"}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def repository_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in GENERATED_DIRS for part in rel.parts):
            continue
        files.append(path)
    return sorted(files)


def parse_manifest(base: Path, manifest: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line_no, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if "  " not in line:
            fail(f"{manifest}: malformed line {line_no}")
        digest, rel = line.split("  ", 1)
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            fail(f"{manifest}: invalid SHA-256 at line {line_no}")
        if not rel or rel in result:
            fail(f"{manifest}: empty or duplicate path at line {line_no}")
        result[rel] = digest
    return result


def verify_manifest(base: Path, manifest: Path, expected_paths: set[str]) -> None:
    entries = parse_manifest(base, manifest)
    if set(entries) != expected_paths:
        missing = sorted(expected_paths - set(entries))
        extra = sorted(set(entries) - expected_paths)
        fail(f"{manifest}: coverage mismatch missing={missing} extra={extra}")
    for rel, expected in entries.items():
        path = base / rel
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            fail(f"{manifest}: hash mismatch for {rel}")


def reject_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            fail(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def verify_text_and_json() -> None:
    for path in repository_files():
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            fail(f"non-UTF-8 public file: {rel}: {exc}")
        if "\r" in text:
            fail(f"CR byte found in canonical public text: {rel}")
        if text and not text.endswith("\n"):
            fail(f"missing final newline: {rel}")
        for line_no, line in enumerate(text.splitlines(), 1):
            if line.rstrip(" \t") != line:
                fail(f"trailing whitespace: {rel}:{line_no}")
        if path.suffix.lower() == ".json":
            try:
                json.loads(text, object_pairs_hook=reject_duplicate_keys)
            except json.JSONDecodeError as exc:
                fail(f"invalid JSON: {rel}: {exc}")


def run_command(args: list[str], cwd: Path = ROOT) -> str:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode != 0:
        print(output, end="")
        fail(f"command failed: {' '.join(args)}")
    return output


def run_unittest_suite(path: str) -> int:
    output = run_command(
        [sys.executable, "-B", "-S", "-m", "unittest", "discover", "-s", path, "-v"]
    )
    print(output, end="")
    matches = re.findall(r"Ran (\d+) tests?", output)
    if len(matches) != 1:
        fail(f"could not determine test count for {path}")
    return int(matches[0])


def verify_challenge_examples() -> int:
    count = 0
    for fixture in sorted((ROOT / "challenge" / "fixtures" / "examples").glob("*.json")):
        output = run_command(
            [sys.executable, "-B", "-S", "challenge/harness.py", fixture.relative_to(ROOT).as_posix()]
        )
        if "status = WELL_FORMED_CHALLENGE_SUBMISSION" not in output:
            fail(f"unexpected challenge status for {fixture.name}")
        if "judgment = NOT_PERFORMED" not in output:
            fail(f"challenge harness adjudicated {fixture.name}")
        count += 1
    if count == 0:
        fail("no challenge examples found")
    return count


def main() -> int:
    all_files = repository_files()

    root_manifest = ROOT / "PUBLICATION-CANDIDATE.sha256"
    root_expected = {
        p.relative_to(ROOT).as_posix()
        for p in all_files
        if p != root_manifest
    }
    verify_manifest(ROOT, root_manifest, root_expected)

    evidence_base = ROOT / "evidence"
    evidence_manifest = evidence_base / "MANIFEST.sha256"
    evidence_expected = {
        p.relative_to(evidence_base).as_posix()
        for p in all_files
        if evidence_base in p.parents and p != evidence_manifest
    }
    verify_manifest(evidence_base, evidence_manifest, evidence_expected)

    verify_text_and_json()

    claim_tests = run_unittest_suite("tests")
    challenge_tests = run_unittest_suite("challenge/tests")
    evidence_tests = run_unittest_suite("evidence/tests")
    example_count = verify_challenge_examples()

    self_check = run_command(
        [sys.executable, "-B", "-S", "evidence/verify_record.py"]
    )
    print(self_check, end="")
    if "PUBLIC_RECORD_SELF_CHECK=PASS" not in self_check:
        fail("public evidence self-check did not pass")
    if "REFERENCE_VERIFICATION=NOT_PERFORMED" not in self_check:
        fail("public evidence self-check exceeded its declared boundary")

    total_tests = claim_tests + challenge_tests + evidence_tests
    print(f"PUBLIC_VALIDATION=PASS")
    print(f"PYTHON={platform.python_version()}")
    print(f"PLATFORM={platform.system()}")
    print(f"CLAIM_TESTS={claim_tests}")
    print(f"CHALLENGE_TESTS={challenge_tests}")
    print(f"EVIDENCE_TESTS={evidence_tests}")
    print(f"TOTAL_UNIT_TESTS={total_tests}")
    print(f"CHALLENGE_EXAMPLES={example_count}")
    print("PRIVATE_REFERENCE_VERIFICATION=NOT_PERFORMED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print("PUBLIC_VALIDATION=FAIL")
        print(f"REASON={exc}")
        print("PRIVATE_REFERENCE_VERIFICATION=NOT_PERFORMED")
        raise SystemExit(1)
