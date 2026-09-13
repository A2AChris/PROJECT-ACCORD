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


def published_entries():
    return adj.validate_state_registry(
        CLAIM_INDEX, copy.deepcopy(STATE_REGISTRY)
    )


def base_receipt(
    receipt_id="ACCORD-RCP-TEST001",
    challenge_type="REGISTERED_FALSIFICATION",
    status="COMPLETED",
):
    claim = {"id": "ACCORD-C05", "revision": "v0.2"}
    record = {
        "receipt_id": receipt_id,
        "canonical_sha256": "a" * 64,
        "public_locator": "https://github.com/A2AChris/PROJECT-ACCORD/issues/999",
        "claim": claim,
        "challenge_type": challenge_type,
        "status": status,
        "received_at": "2026-09-13T17:00:00Z",
        "last_status_change_at": "2026-09-13T17:05:00Z",
    }
    if challenge_type == "REGISTERED_FALSIFICATION":
        claim["falsification_id"] = "C05-F1"
    else:
        record["novel_hypothesis"] = {
            "alleged_claim_contradiction": "The public claim appears contradicted.",
            "reason_no_registered_falsification_id_applies": (
                "No published falsification id faithfully expresses this mechanism."
            ),
        }
    return record


def base_record(
    adjudication_id="ACCORD-ADJ-TEST001",
    disposition="NOT_CONFIRMED",
    challenge_type="REGISTERED_FALSIFICATION",
    visibility="PUBLIC",
):
    claim = {"id": "ACCORD-C05", "revision": "v0.2"}
    challenge = {
        "canonical_sha256": "a" * 64,
        "challenge_type": challenge_type,
        "visibility": visibility,
    }
    if challenge_type == "REGISTERED_FALSIFICATION":
        claim["falsification_id"] = "C05-F1"
    if visibility == "PUBLIC":
        challenge["receipt_id"] = "ACCORD-RCP-TEST001"
        challenge["public_locator"] = (
            "https://github.com/A2AChris/PROJECT-ACCORD/issues/999"
        )
    return {
        "schema": "accord.challenge-adjudication-record.v0.2",
        "adjudication_id": adjudication_id,
        "challenge": challenge,
        "claim": claim,
        "review_provenance": {
            "review_class": "PROJECT_ADJUDICATED",
            "reviewers": [
                {"identifier": "A2AChris", "relationship": "PROJECT"}
            ],
        },
        "decision_authority": {
            "class": "PROJECT_MAINTAINER",
            "actor": "A2AChris",
            "authority_basis": adj.DECISION_AUTHORITY_BASIS,
            "decided_at": "2026-09-13T17:10:00Z",
        },
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
        self.entries = published_entries()
        receipt_index = {
            "schema": "accord.challenge-receipt-index.v0.1",
            "contract_revision": "v0.1",
            "records": [base_receipt()],
        }
        self.receipts = adj.validate_receipts(receipt_index, self.entries)

    def test_current_claim_index_is_bound_to_revision_state_registry(self):
        self.assertEqual(len(self.entries), len(CLAIM_INDEX["claims"]))

    def test_registered_receipt_requires_published_falsification_id(self):
        receipt = base_receipt()
        receipt["claim"]["falsification_id"] = "C05-F99"
        index = {
            "schema": "accord.challenge-receipt-index.v0.1",
            "contract_revision": "v0.1",
            "records": [receipt],
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_receipts(index, self.entries)

    def test_novel_receipt_must_not_carry_registered_id(self):
        receipt = base_receipt(challenge_type="NOVEL_FALSIFICATION_HYPOTHESIS")
        receipt["claim"]["falsification_id"] = "C05-F1"
        index = {
            "schema": "accord.challenge-receipt-index.v0.1",
            "contract_revision": "v0.1",
            "records": [receipt],
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_receipts(index, self.entries)

    def test_novel_receipt_requires_explanation(self):
        receipt = base_receipt(challenge_type="NOVEL_FALSIFICATION_HYPOTHESIS")
        del receipt["novel_hypothesis"]
        index = {
            "schema": "accord.challenge-receipt-index.v0.1",
            "contract_revision": "v0.1",
            "records": [receipt],
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_receipts(index, self.entries)

    def test_duplicate_receipt_content_is_rejected(self):
        first = base_receipt("ACCORD-RCP-TEST001")
        second = base_receipt("ACCORD-RCP-TEST002")
        index = {
            "schema": "accord.challenge-receipt-index.v0.1",
            "contract_revision": "v0.1",
            "records": [first, second],
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_receipts(index, self.entries)

    def test_receipt_time_cannot_move_backwards(self):
        receipt = base_receipt()
        receipt["last_status_change_at"] = "2026-09-13T16:59:59Z"
        index = {
            "schema": "accord.challenge-receipt-index.v0.1",
            "contract_revision": "v0.1",
            "records": [receipt],
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_receipts(index, self.entries)

    def test_public_final_requires_completed_receipt(self):
        receipt_index = {
            "schema": "accord.challenge-receipt-index.v0.1",
            "contract_revision": "v0.1",
            "records": [base_receipt(status="UNDER_REVIEW")],
        }
        receipts = adj.validate_receipts(receipt_index, self.entries)
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(base_record(), self.entries, receipts)

    def test_confidential_final_must_not_expose_public_locator(self):
        record = base_record(visibility="CONFIDENTIAL_SECURITY")
        record["challenge"]["public_locator"] = "https://example.invalid"
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries, {})

    def test_external_independent_requires_external_reviewer(self):
        record = base_record()
        record["review_provenance"]["review_class"] = "EXTERNAL_INDEPENDENT"
        record["review_provenance"]["independence_basis"] = "No project affiliation."
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries, self.receipts)

    def test_external_independent_requires_independence_basis(self):
        record = base_record()
        record["review_provenance"] = {
            "review_class": "EXTERNAL_INDEPENDENT",
            "reviewers": [
                {"identifier": "external-reviewer", "relationship": "EXTERNAL"}
            ],
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries, self.receipts)

    def test_multi_party_requires_two_reviewers(self):
        record = base_record()
        record["review_provenance"]["review_class"] = "MULTI_PARTY_REVIEWED"
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries, self.receipts)

    def test_unsupported_decision_authority_is_rejected(self):
        record = base_record()
        record["decision_authority"]["class"] = "EXTERNAL_TRIBUNAL"
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries, self.receipts)

    def test_decision_authority_basis_must_match_contract(self):
        record = base_record()
        record["decision_authority"]["authority_basis"] = "because-maintainer"
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries, self.receipts)

    def test_duplicate_adjudication_id_is_rejected(self):
        a = base_record()
        b = base_record()
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_adjudication_set([a, b], self.entries, self.receipts)

    def test_two_active_finals_for_same_binding_are_rejected(self):
        a = base_record("ACCORD-ADJ-TEST001")
        b = base_record("ACCORD-ADJ-TEST002")
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_adjudication_set([a, b], self.entries, self.receipts)

    def test_valid_supersession_leaves_one_active_final(self):
        a = base_record("ACCORD-ADJ-TEST001")
        b = base_record("ACCORD-ADJ-TEST002")
        b["supersedes"] = "ACCORD-ADJ-TEST001"
        active, confirmed = adj.validate_adjudication_set(
            [a, b], self.entries, self.receipts
        )
        self.assertEqual(active, 1)
        self.assertEqual(confirmed, 0)

    def test_supersession_must_preserve_binding(self):
        a = base_record("ACCORD-ADJ-TEST001")
        b = base_record("ACCORD-ADJ-TEST002")
        b["supersedes"] = "ACCORD-ADJ-TEST001"
        b["challenge"]["canonical_sha256"] = "b" * 64
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_adjudication_set([a, b], self.entries, self.receipts)

    def test_forked_supersession_is_rejected(self):
        a = base_record("ACCORD-ADJ-TEST001")
        b = base_record("ACCORD-ADJ-TEST002")
        c = base_record("ACCORD-ADJ-TEST003")
        b["supersedes"] = "ACCORD-ADJ-TEST001"
        c["supersedes"] = "ACCORD-ADJ-TEST001"
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_adjudication_set([a, b, c], self.entries, self.receipts)

    def test_confirmed_falsification_requires_matching_nonpublished_state(self):
        record = base_record(disposition="CONFIRMED_FALSIFICATION")
        record["decision_detail"]["evidence_references"] = ["public:evidence:test"]
        record["decision_detail"]["falsification_analysis"] = "C05-F1 is satisfied."
        record["consequence"] = {
            "action": "CLAIM_SUSPENDED",
            "claim_id": "ACCORD-C05",
            "claim_revision": "v0.2",
        }
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries, self.receipts)

    def test_confirmed_contract_gap_requires_novel_challenge(self):
        record = base_record(disposition="CONFIRMED_CONTRACT_GAP")
        record["decision_detail"]["evidence_references"] = ["public:evidence:test"]
        record["decision_detail"]["contract_gap_analysis"] = "The contract is incomplete."
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_record(record, self.entries, self.receipts)

    def test_completed_receipt_requires_active_final(self):
        with self.assertRaises(adj.AdjudicationError):
            adj.validate_adjudication_set([], self.entries, self.receipts)

    def test_repository_registries_are_currently_empty_and_valid(self):
        receipts, active, confirmed = adj.validate_repository(ROOT)
        self.assertEqual(receipts, 0)
        self.assertEqual(active, 0)
        self.assertEqual(confirmed, 0)


if __name__ == "__main__":
    unittest.main()
