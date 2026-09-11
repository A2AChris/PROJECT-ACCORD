from pathlib import Path
import hashlib
import unittest


ROOT = Path(__file__).resolve().parent.parent
SECURITY = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
CONTRIBUTING = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
LICENSE_SCOPE = (ROOT / "LICENSE-SCOPE.md").read_text(encoding="utf-8")

APACHE_2_0_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"


class ReleaseSurfaceTests(unittest.TestCase):
    def test_confidential_security_contact_is_declared(self):
        self.assertIn("project_accord@proton.me", SECURITY)
        self.assertIn("project_accord@proton.me", README)

    def test_security_policy_no_longer_claims_channel_is_undeclared(self):
        self.assertNotIn("has not\nyet been declared", SECURITY)
        self.assertNotIn("Until that gate is closed", SECURITY)

    def test_security_reporting_is_not_listed_as_remaining_prerequisite(self):
        marker = "The following remain publication prerequisites"
        tail = CONTRIBUTING.split(marker, 1)[1]
        self.assertNotIn("verified confidential security-reporting channel", tail)

    def test_private_vulnerability_reporting_is_additional_not_required_for_email_channel(self):
        self.assertIn("additional\nchannel once the repository is public", SECURITY)
        self.assertIn("email channel above remains valid independently", SECURITY)

    def test_license_is_canonical_apache_2_0_text(self):
        license_bytes = (ROOT / "LICENSE").read_bytes()
        self.assertEqual(hashlib.sha256(license_bytes).hexdigest(), APACHE_2_0_SHA256)
        self.assertIn(b"Apache License", license_bytes)
        self.assertIn(b"Version 2.0, January 2004", license_bytes)

    def test_readme_declares_apache_2_0_and_scope_file(self):
        self.assertIn("Apache License 2.0 (`Apache-2.0`)", README)
        self.assertIn("[`LICENSE-SCOPE.md`](LICENSE-SCOPE.md)", README)
        self.assertNotIn("A `LICENSE` has not yet been selected", README)
        self.assertNotIn("Eine `LICENSE` wurde noch nicht gewählt", README)

    def test_license_scope_excludes_separate_private_unpublished_material(self):
        self.assertIn("files contained in this", LICENSE_SCOPE)
        self.assertIn("public-surface repository", LICENSE_SCOPE)
        self.assertIn("does **not** place any separate private or unpublished material", LICENSE_SCOPE)
        self.assertIn("private reference implementations", LICENSE_SCOPE)
        self.assertIn("private tests and internal assurance material", LICENSE_SCOPE)
        self.assertIn("unpublished architecture", LICENSE_SCOPE)

    def test_contribution_intake_remains_closed(self):
        self.assertIn("General external code and documentation contributions are still closed", CONTRIBUTING)
        self.assertIn("designated **Not a Contribution**", CONTRIBUTING)
        self.assertIn("explicitly submits the material for inclusion in the Work", CONTRIBUTING)
        self.assertIn("Apache-2.0 Section 5", CONTRIBUTING)

    def test_license_is_no_longer_a_remaining_publication_prerequisite(self):
        marker = "The following remain publication prerequisites"
        tail = CONTRIBUTING.split(marker, 1)[1]
        self.assertNotIn("final contribution/licensing terms", tail)
        self.assertIn("IP red-team review", tail)
        self.assertIn("claim red-team review", tail)


if __name__ == "__main__":
    unittest.main()
