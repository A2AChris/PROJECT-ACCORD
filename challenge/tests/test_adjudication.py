import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "accord_adjudication", ROOT / "challenge" / "adjudication.py"
)
adj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adj)

CLAIM_INDEX = json.loads(
    (ROOT / "claims" / "public-claim-index.json").read_text(encoding="utf-8")
)
STATE_REGISTRY = json.loads(
    (ROOT / "claims" / "public-claim-state.json").read_text(encoding="utf-8")
)


def base_record(disposition="NOT_CONFIRMED"):
    return {
        "schema": "accord.challenge-adjudication-record.v0.1",
        "adjudication_id": "ACCORD-ADJ-TEST001",
        "challenge": {"canonical_sha256": "a" * 64},
        "claim": {
            "id": "ACCORD-C05",
            "revision": "v0.2",
            "falsification_id": "C05-F1",
        },
        "review_class": "PROJECT_ADJUDICATED",
        "disposition": disposition,
        "decision_detail": {
            "basis": "Public test rationale.",
            "public_rule_references": ["CLAIMS.md#accord-c05"],
            "evidence_references": [],
            "falsification_analysis": "The test record does not establish C05-F1.",
        },
    }


class AdjudicationGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.state = copy.deepcopy(STATE_REGISTRY)
        self.entries = adj.validate_state_registry(CLAIM_INDEX, self.state)

    def test_current_claim_index_is_bound_to_revision_state_registry(self):
        self.assertEqual(len(self.entries), len(CLAIM_INDEX["claims"]))
        for claim_id, current in CLAIM_INDEX["claims"].items():
            self.assertIn((claim_id, current["revision"]), self.entries)

    def test_unknown_falsification_id_is_rejected(self):
        record = base_record()
        record["claim"]["falsification_id"] = "C05-F99"
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries)

    def test_confirmed_falsification_requires_consequence(self):
        record = base_record("CONFIRMED_FALSIFICATION")
        record["decision_detail"]["evidence_references"] = ["public:evidence:test"]
        record["decision_detail"]["falsification_analysis"] = "C05-F1 is satisfied."
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries)

    def test_confirmed_falsification_cannot_leave_revision_published(self):
        record = base_record("CONFIRMED_FALSIFICATION")
        record["decision_detail"]["evidence_references"] = ["public:evidence:test"]
        record["decision_detail"]["falsification_analysis"] = "C05-F1 is satisfied."
        record["consequence"] = {
            "action": "CLAIM_SUSPENDED",
            "claim_id": "ACCORD-C05",
            "claim_revision": "v0.2",
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries)

    def test_confirmed_falsification_accepts_matching_suspension(self):
        state = copy.deepcopy(STATE_REGISTRY)
        for entry in state["entries"]:
            if entry["id"] == "ACCORD-C05" and entry["revision"] == "v0.2":
                entry["publication_state"] = "SUSPENDED"
        entries = adj.validate_state_registry(CLAIM_INDEX, state)
        record = base_record("CONFIRMED_FALSIFICATION")
        record["decision_detail"]["evidence_references"] = ["public:evidence:test"]
        record["decision_detail"]["falsification_analysis"] = "C05-F1 is satisfied."
        record["consequence"] = {
            "action": "CLAIM_SUSPENDED",
            "claim_id": "ACCORD-C05",
            "claim_revision": "v0.2",
        }
        adj.validate_record(record, entries)

    def test_non_confirmed_disposition_rejects_claim_consequence(self):
        record = base_record()
        record["consequence"] = {
            "action": "CLAIM_SUSPENDED",
            "claim_id": "ACCORD-C05",
            "claim_revision": "v0.2",
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries)

    def test_out_of_scope_rejection_requires_public_rule_reference(self):
        record = base_record("REJECTED_OUT_OF_SCOPE")
        record["decision_detail"]["public_rule_references"] = []
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries)

    def test_insufficient_evidence_requires_missing_evidence_statement(self):
        record = base_record("INSUFFICIENT_EVIDENCE")
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries)

    def test_not_confirmed_requires_falsification_analysis(self):
        record = base_record("NOT_CONFIRMED")
        del record["decision_detail"]["falsification_analysis"]
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries)

    def test_repository_registry_is_currently_empty_and_valid(self):
        records, confirmed = adj.validate_repository(ROOT)
        self.assertEqual(records, 0)
        self.assertEqual(confirmed, 0)


if __name__ == "__main__":
    unittest.main()
