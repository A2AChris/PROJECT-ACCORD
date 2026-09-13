import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CH = HERE.parent
spec = importlib.util.spec_from_file_location("harness", CH / "harness.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

EXAMPLES = CH / "fixtures" / "examples"


def load(name):
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


class PublicChallengeHarnessP8Tests(unittest.TestCase):
    def test_all_examples_well_formed(self):
        paths = sorted(EXAMPLES.glob("*.json"))
        self.assertEqual(len(paths), 5)
        for path in paths:
            result = h.validate_fixture(json.loads(path.read_text(encoding="utf-8")))
            self.assertEqual(result["status"], "WELL_FORMED_CHALLENGE_SUBMISSION")
            self.assertEqual(result["judgment"], "NOT_PERFORMED")

    def test_claim_revision_and_falsification_id_are_registry_bound(self):
        doc = load("ACCORD-C05-lineage-ambiguity.json")
        self.assertEqual(doc["claim"]["revision"], "v0.3")
        self.assertEqual(doc["claim"]["falsification_id"], "C05-F4")
        self.assertEqual(h.validate_fixture(doc)["falsification_id"], "C05-F4")

    def test_stale_claim_revision_rejected(self):
        doc = load("ACCORD-C05-lineage-ambiguity.json")
        doc["claim"]["revision"] = "v0.2"
        with self.assertRaises(h.ValidationError):
            h.validate_fixture(doc)

    def test_unknown_falsification_id_rejected(self):
        doc = load("ACCORD-C05-lineage-ambiguity.json")
        doc["claim"]["falsification_id"] = "C05-F99"
        with self.assertRaises(h.ValidationError):
            h.validate_fixture(doc)

    def test_attack_tags_are_not_claim_specific_permissions(self):
        doc = load("ACCORD-C01-self-legitimation.json")
        doc["attack"]["class"] = "EVIDENCE_INCONSISTENCY"
        self.assertEqual(
            h.validate_fixture(doc)["status"],
            "WELL_FORMED_CHALLENGE_SUBMISSION",
        )

    def test_other_preserves_unanticipated_attack_path(self):
        doc = load("ACCORD-C05-lineage-ambiguity.json")
        doc["attack"] = {
            "class": "OTHER",
            "summary": "Previously unclassified public failure mechanism.",
            "other_class": "novel mechanism",
        }
        self.assertEqual(
            h.validate_fixture(doc)["status"],
            "WELL_FORMED_CHALLENGE_SUBMISSION",
        )

    def test_scope_is_echoed_not_adjudicated(self):
        doc = load("ACCORD-C04-result-dependent-admission.json")
        for position in [
            "SUBMITTER_ASSERTED_IN_SCOPE",
            "SUBMITTER_UNCERTAIN",
            "SUBMITTER_ASSERTED_OUT_OF_SCOPE",
        ]:
            mutated = copy.deepcopy(doc)
            mutated["scope_position"]["position"] = position
            result = h.validate_fixture(mutated)
            self.assertEqual(result["scope_position"], position)
            self.assertEqual(result["judgment"], "NOT_PERFORMED")

    def test_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "dup.json"
            p.write_text('{"schema_version":"a","schema_version":"b"}', encoding="utf-8")
            with self.assertRaises(h.ValidationError):
                h.load_fixture(p)

    def test_nonfinite_number_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "nan.json"
            p.write_text('{"x":NaN}', encoding="utf-8")
            with self.assertRaises(h.ValidationError):
                h.load_fixture(p)

    def test_unknown_evidence_reference_rejected(self):
        doc = load("ACCORD-C03-observation-to-cause.json")
        doc["observations"][0]["evidence_refs"] = ["missing"]
        with self.assertRaises(h.ValidationError):
            h.validate_fixture(doc)

    def test_duplicate_evidence_id_rejected(self):
        doc = load("ACCORD-C03-observation-to-cause.json")
        doc["evidence"].append(copy.deepcopy(doc["evidence"][0]))
        with self.assertRaises(h.ValidationError):
            h.validate_fixture(doc)

    def test_c05_subject_is_public_abstract_selector(self):
        doc = load("ACCORD-C05-lineage-ambiguity.json")
        self.assertEqual(
            set(doc["subject"]),
            {"historical_subject", "historical_cutoff"},
        )


if __name__ == "__main__":
    unittest.main()
