from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent
README = (ROOT / "README.md").read_text(encoding="utf-8")


class ReadmeSecurityChannelStatusTests(unittest.TestCase):
    def test_private_reporting_is_repository_setting_not_release_gate(self):
        normalized = " ".join(README.split())

        self.assertIn(
            "repository-native private vulnerability reporting may be used as an additional channel",
            normalized.lower(),
        )
        self.assertIn(
            "availability is a repository setting, not a condition of repository public status",
            normalized.lower(),
        )
        self.assertIn(
            "repository-natives private vulnerability reporting kann als zusätzlicher kanal genutzt werden",
            normalized.lower(),
        )
        self.assertIn(
            "repository-einstellung und keine bedingung für den öffentlichen status des repositories",
            normalized.lower(),
        )

        self.assertNotIn(
            "private vulnerability reporting is intended as an additional channel after public release",
            normalized.lower(),
        )
        self.assertNotIn(
            "private vulnerability reporting ist nach dem public release als zusätzlicher kanal vorgesehen",
            normalized.lower(),
        )


if __name__ == "__main__":
    unittest.main()
