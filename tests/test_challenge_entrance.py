from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent
CHALLENGE_ENTRY = (ROOT / "CHALLENGE.md").read_text(encoding="utf-8")
ISSUE_TEMPLATE = (
    ROOT / ".github" / "ISSUE_TEMPLATE" / "accord-challenge.yml"
).read_text(encoding="utf-8")


class ChallengeEntranceVisibilityTests(unittest.TestCase):
    def test_root_challenge_entry_preserves_canonical_public_intake(self):
        normalized = " ".join(CHALLENGE_ENTRY.split())
        self.assertIn(
            "canonical public intake remains a GitHub Issue in this repository whose title begins with:",
            normalized,
        )
        self.assertIn("[ACCORD CHALLENGE]", CHALLENGE_ENTRY)
        self.assertIn("NOVEL_FALSIFICATION_HYPOTHESIS", CHALLENGE_ENTRY)
        self.assertIn("challenge/README.md", CHALLENGE_ENTRY)
        self.assertIn("challenge/LIFECYCLE-CONTRACT.md", CHALLENGE_ENTRY)
        self.assertIn("challenge/ADJUDICATION-CONTRACT.md", CHALLENGE_ENTRY)

    def test_public_and_confidential_intake_remain_separate(self):
        self.assertIn("public research challenge != confidential security report", CHALLENGE_ENTRY)
        self.assertIn("project_accord@proton.me", CHALLENGE_ENTRY)
        self.assertIn("Security-sensitive material must not be posted here.", ISSUE_TEMPLATE)
        self.assertIn("SECURITY.md", ISSUE_TEMPLATE)

    def test_issue_template_prefills_canonical_title_prefix(self):
        self.assertIn('title: "[ACCORD CHALLENGE] "', ISSUE_TEMPLATE)
        self.assertIn("REGISTERED_FALSIFICATION", ISSUE_TEMPLATE)
        self.assertIn("NOVEL_FALSIFICATION_HYPOTHESIS", ISSUE_TEMPLATE)
        self.assertIn("mechanical acceptance or receipt does not mean", ISSUE_TEMPLATE)


if __name__ == "__main__":
    unittest.main()
