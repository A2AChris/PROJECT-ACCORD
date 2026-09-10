import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAIMS_MD = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
INDEX = json.loads((ROOT / "claims" / "public-claim-index.json").read_text(encoding="utf-8"))


class PublicClaimContractTests(unittest.TestCase):
    def test_exact_claim_set(self):
        self.assertEqual(
            set(INDEX["claims"]),
            {"ACCORD-C01","ACCORD-C02","ACCORD-C03","ACCORD-C04","ACCORD-C05"},
        )

    def test_contract_revision_matches(self):
        self.assertEqual(INDEX["contract_revision"], "v0.2")
        self.assertIn("**Public contract revision:** `v0.2`", CLAIMS_MD)

    def test_each_claim_and_revision_appear_in_prose_contract(self):
        for claim_id, entry in INDEX["claims"].items():
            self.assertIn(claim_id, CLAIMS_MD)
            section_match = re.search(
                rf"# {re.escape(claim_id)}\b.*?(?=\n# ACCORD-C|\n# Cross-claim|\Z)",
                CLAIMS_MD,
                flags=re.S,
            )
            self.assertIsNotNone(section_match, claim_id)
            self.assertIn(f"**Revision:** `{entry['revision']}`", section_match.group(0))

    def test_every_registered_falsification_id_exists_in_prose(self):
        for claim_id, entry in INDEX["claims"].items():
            for fid in entry["falsification_ids"]:
                self.assertIn(f"**{fid} —", CLAIMS_MD, (claim_id, fid))

    def test_no_unregistered_falsification_ids_in_prose(self):
        registered = {
            fid for entry in INDEX["claims"].values()
            for fid in entry["falsification_ids"]
        }
        found = set(re.findall(r"\*\*(C0[1-5]-F[1-9][0-9]*) —", CLAIMS_MD))
        self.assertEqual(found, registered)

    def test_c05_does_not_assume_evidence_sufficiency(self):
        c05 = re.search(r"# ACCORD-C05\b.*?(?=\n# Cross-claim|\Z)", CLAIMS_MD, re.S).group(0)
        self.assertIn("sufficiency", c05)
        self.assertIn("is not assumed", c05)
        self.assertIn("Those are conditions the positive assertion", c05)

    def test_c04_is_profile_bounded_not_universal_future_claim(self):
        c04 = re.search(r"# ACCORD-C04\b.*?(?=\n# ACCORD-C05|\Z)", CLAIMS_MD, re.S).group(0)
        self.assertIn("applies only to a reconstruction profile explicitly bound to C04", c04)
        self.assertIn("not a universal assertion", c04)

    def test_cross_claim_evidence_non_generalization_is_explicit(self):
        self.assertIn("A dependency relation among claims is not an evidence relation.", CLAIMS_MD)


if __name__ == "__main__":
    unittest.main()
