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

HISTORICAL_RECORD_V05 = json.loads((EV / "ACCORD-RM01-REFERENCE-EVIDENCE-v0.5.json").read_text(encoding="utf-8"))
HISTORICAL_RECORD_V06 = json.loads((EV / "ACCORD-RM01-REFERENCE-EVIDENCE-v0.6.json").read_text(encoding="utf-8"))
RECORD = json.loads((EV / "ACCORD-RM01-REFERENCE-EVIDENCE-v0.7.json").read_text(encoding="utf-8"))


def resign(obj):
    obj = copy.deepcopy(obj)
    obj["integrity"]["record_sha256"] = None
    obj["integrity"]["record_sha256"] = vr.canonical_digest(obj)
    return obj


class EvidenceRecordP8Tests(unittest.TestCase):
    def test_baseline_valid(self):
        vr.validate_record(RECORD)

    def test_historical_v05_record_is_preserved(self):
        self.assertEqual(HISTORICAL_RECORD_V05["record_id"], "ACCORD-EVIDENCE-RM01-v0.5")
        self.assertEqual(
            HISTORICAL_RECORD_V05["claim_binding"]["evidenced_public_claim"],
            {"id": "ACCORD-C05", "revision": "v0.2"},
        )
        self.assertEqual(
            HISTORICAL_RECORD_V05["integrity"]["record_sha256"],
            "38ee75805375d1331b4988ddec8c63a65e678031e6bab268874335a42400f5c0",
        )

    def test_historical_v06_record_is_preserved(self):
        self.assertEqual(HISTORICAL_RECORD_V06["record_id"], "ACCORD-EVIDENCE-RM01-v0.6")
        self.assertEqual(
            HISTORICAL_RECORD_V06["claim_binding"]["evidenced_public_claim"],
            {"id": "ACCORD-C05", "revision": "v0.3"},
        )
        self.assertEqual(HISTORICAL_RECORD_V06["public_reference"]["status"], "PROVISIONALLY_FROZEN")
        self.assertEqual(
            HISTORICAL_RECORD_V06["integrity"]["record_sha256"],
            "c893bd644e9dd58c221c53ac92c8e8e82de218fe315f6aea8082572069dae258",
        )

    def test_current_record_is_v07(self):
        self.assertEqual(RECORD["record_id"], "ACCORD-EVIDENCE-RM01-v0.7")
        self.assertEqual(
            RECORD["integrity"]["record_sha256"],
            "a7dee3986896e98bc722747e8b9ab9e4bff1d65baf9c59391e69fec30354b297",
        )

    def test_digest_recomputes(self):
        self.assertEqual(vr.canonical_digest(RECORD), RECORD["integrity"]["record_sha256"])

    def test_public_reference_uses_commitment_only(self):
        ref = RECORD["public_reference"]
        self.assertEqual(set(ref), {"alias", "status", "private_reference_commitment"})
        commitment = ref["private_reference_commitment"]
        self.assertEqual(commitment["algorithm"], "SHA-256")
        self.assertEqual(len(commitment["commitment"]), 64)

    def test_public_reference_status_is_record_lifecycle_metadata(self):
        self.assertEqual(RECORD["public_reference"]["status"], "PROVISIONALLY_FROZEN")
        qualification = RECORD["evidence_classification"]["qualification"]
        self.assertIn("public_reference.status value is record-lifecycle metadata", qualification)
        self.assertIn(
            "does not classify the historical execution lineage as provisional, committed, executed, effective, or final",
            qualification,
        )
        self.assertIn(
            "PROVISIONALLY_FROZEN public-reference status means that the historical execution lineage is provisional or uncommitted.",
            RECORD["forbidden_inferences"],
        )
        self.assertIn(
            "FROZEN public-reference status is required for the C05 term 'committed' to apply to the historical execution lineage.",
            RECORD["forbidden_inferences"],
        )

    def test_missing_status_semantic_separation_is_rejected(self):
        r = copy.deepcopy(RECORD)
        r["evidence_classification"]["qualification"] = r["evidence_classification"]["qualification"].replace(
            "The public_reference.status value is record-lifecycle metadata; it does not classify the historical execution lineage as provisional, committed, executed, effective, or final. ",
            "",
        )
        r = resign(r)
        with self.assertRaises(vr.RecordError):
            vr.validate_record(r)

    def test_evidence_binds_only_c05(self):
        self.assertEqual(
            RECORD["claim_binding"]["evidenced_public_claim"],
            {"id": "ACCORD-C05", "revision": "v0.3"},
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

    def test_ci_profile_disclosure_is_explicitly_non_exhaustive(self):
        qualification = RECORD["ci_summary"]["qualification"]
        self.assertIn("not an exhaustive inventory", qualification)
        self.assertIn(
            "The listed CI profiles are a complete inventory of private CI coverage or map one-for-one to the public validation matrix.",
            RECORD["forbidden_inferences"],
        )

    def test_public_challenge_contract_does_not_attest_visibility(self):
        classification = RECORD["evidence_classification"]
        self.assertEqual(
            classification["public_challenge_contract"],
            "STRUCTURED_COUNTEREXAMPLE_SURFACE_PRESENT",
        )
        self.assertNotIn("public_challenge_level", classification)
        self.assertIn("does not itself attest current repository visibility", classification["qualification"])
        self.assertIn(
            "This record alone establishes that the repository is currently public or that R1 is presently in effect.",
            RECORD["forbidden_inferences"],
        )

    def test_r1_does_not_imply_private_reference_execution_access(self):
        qualification = RECORD["evidence_classification"]["qualification"]
        self.assertIn("R1 means structured public challengeability", qualification)
        self.assertIn("public trace generation", qualification)
        self.assertIn("External empirical generation of private-reference traces is not currently claimed.", qualification)
        self.assertIn(
            "R1 implies public execution access to, simulation of, or public trace generation from the private reference implementation.",
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
