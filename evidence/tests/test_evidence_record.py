import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EV = HERE.parent
spec = importlib.util.spec_from_file_location("verify_record", EV / "verify_record.py")
vr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vr)

RECORD = json.loads((EV / "ACCORD-RM01-REFERENCE-EVIDENCE-v0.3.json").read_text(encoding="utf-8"))


def resign(obj):
    obj = copy.deepcopy(obj)
    obj["integrity"]["record_sha256"] = None
    obj["integrity"]["record_sha256"] = vr.canonical_digest(obj)
    return obj


class EvidenceRecordP8Tests(unittest.TestCase):
    def test_baseline_valid(self):
        vr.validate_record(RECORD)

    def test_digest_recomputes(self):
        self.assertEqual(vr.canonical_digest(RECORD), RECORD["integrity"]["record_sha256"])

    def test_public_reference_uses_commitment_only(self):
        ref = RECORD["public_reference"]
        self.assertEqual(set(ref), {"alias", "status", "private_reference_commitment"})
        commitment = ref["private_reference_commitment"]
        self.assertEqual(commitment["algorithm"], "SHA-256")
        self.assertEqual(len(commitment["commitment"]), 64)

    def test_evidence_binds_only_c05(self):
        self.assertEqual(
            RECORD["claim_binding"]["evidenced_public_claim"],
            {"id": "ACCORD-C05", "revision": "v0.2"},
        )

    def test_c03_c04_are_dependencies_not_evidenced_claims(self):
        deps = RECORD["claim_binding"]["semantic_dependencies_not_independently_evidenced"]
        self.assertEqual(
            {(d["id"], d["revision"]) for d in deps},
            {("ACCORD-C03", "v0.2"), ("ACCORD-C04", "v0.2")},
        )
        self.assertIn(
            "This record independently evidences ACCORD-C03 or ACCORD-C04 as general claims.",
            RECORD["forbidden_inferences"],
        )

    def test_r2_claim_rejected(self):
        r = resign(RECORD)
        r["evidence_classification"]["public_reproduction_level"] = "R2_PUBLICLY_REPRODUCIBLE"
        r = resign(r)
        with self.assertRaises(vr.RecordError):
            vr.validate_record(r)

    def test_partial_profile_rejected(self):
        r = resign(RECORD)
        r["ci_summary"]["profiles"][0]["passed"] -= 1
        r = resign(r)
        with self.assertRaises(vr.RecordError):
            vr.validate_record(r)

    def test_tampered_digest_rejected(self):
        r = copy.deepcopy(RECORD)
        r["record_id"] += "-tampered"
        with self.assertRaises(vr.RecordError):
            vr.validate_record(r)

    def test_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "dup.json"
            p.write_text('{"schema":"a","schema":"b"}', encoding="utf-8")
            with self.assertRaises(vr.RecordError):
                vr.load_record(p)


if __name__ == "__main__":
    unittest.main()
