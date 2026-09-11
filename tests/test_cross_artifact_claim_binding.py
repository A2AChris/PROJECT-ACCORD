import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = json.loads((ROOT / "claims" / "public-claim-index.json").read_text(encoding="utf-8"))
EVIDENCE = json.loads((ROOT / "evidence" / "ACCORD-RM01-REFERENCE-EVIDENCE-v0.4.json").read_text(encoding="utf-8"))
README = (ROOT / "README.md").read_text(encoding="utf-8")


class CrossArtifactClaimBindingTests(unittest.TestCase):
    def test_evidenced_claim_exists_at_same_revision(self):
        bound = EVIDENCE["claim_binding"]["evidenced_public_claim"]
        self.assertIn(bound["id"], INDEX["claims"])
        self.assertEqual(INDEX["claims"][bound["id"]]["revision"], bound["revision"])
        self.assertEqual(
            INDEX["claims"][bound["id"]]["public_evidence_status"],
            "R0_PROJECT_ATTESTED_VIA_ACCORD_RM01",
        )

    def test_semantic_dependencies_exist_but_are_not_marked_rm01_evidenced(self):
        for dep in EVIDENCE["claim_binding"]["semantic_dependencies_not_independently_evidenced"]:
            entry = INDEX["claims"][dep["id"]]
            self.assertEqual(entry["revision"], dep["revision"])
            self.assertIn("NOT_INDEPENDENTLY_EVIDENCED_BY_RM01", entry["public_evidence_status"])

    def test_readme_uses_current_claim_revision(self):
        for claim_id in INDEX["claims"]:
            self.assertIn(f"{claim_id} v0.2", README)


if __name__ == "__main__":
    unittest.main()
