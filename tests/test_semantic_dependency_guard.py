import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "accord_dependency_guard", ROOT / "claims" / "dependency_guard.py"
)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

CLAIM_INDEX = json.loads(
    (ROOT / "claims" / "public-claim-index.json").read_text(encoding="utf-8")
)
STATE_REGISTRY = json.loads(
    (ROOT / "claims" / "public-claim-state.json").read_text(encoding="utf-8")
)
DEPENDENCY_REGISTRY = json.loads(
    (ROOT / "claims" / "public-semantic-dependencies.json").read_text(encoding="utf-8")
)
CURRENT_RM01 = json.loads(
    (ROOT / "evidence" / "ACCORD-RM01-REFERENCE-EVIDENCE-v0.7.json").read_text(
        encoding="utf-8"
    )
)


def entries():
    return guard._adjudication.validate_state_registry(
        CLAIM_INDEX, copy.deepcopy(STATE_REGISTRY)
    )


def bindings(current_entries=None):
    if current_entries is None:
        current_entries = entries()
    return guard.validate_dependency_registry(
        DEPENDENCY_REGISTRY,
        CLAIM_INDEX,
        current_entries,
    )


def finding(
    adjudication_id,
    claim_id="ACCORD-C03",
    revision="v0.2",
    disposition="CONFIRMED_FALSIFICATION",
    supersedes=None,
):
    record = {
        "adjudication_id": adjudication_id,
        "claim": {"id": claim_id, "revision": revision},
        "disposition": disposition,
    }
    if supersedes is not None:
        record["supersedes"] = supersedes
    return record


class SemanticDependencyGuardTests(unittest.TestCase):
    def test_current_c05_binding_is_exactly_c03_and_c04(self):
        current_bindings = bindings()
        self.assertEqual(len(current_bindings), 1)
        dependent, requirements = current_bindings[0]
        self.assertEqual(dependent, ("ACCORD-C05", "v0.3"))
        self.assertEqual(
            set(requirements),
            {
                ("ACCORD-C03", "v0.2"),
                ("ACCORD-C04", "v0.2"),
            },
        )

    def test_registry_matches_current_rm01_semantic_dependencies(self):
        dependent, requirements = bindings()[0]
        evidenced = CURRENT_RM01["claim_binding"]["evidenced_public_claim"]
        rm01_dependencies = {
            (item["id"], item["revision"])
            for item in CURRENT_RM01["claim_binding"][
                "semantic_dependencies_not_independently_evidenced"
            ]
        }
        self.assertEqual(dependent, (evidenced["id"], evidenced["revision"]))
        self.assertEqual(set(requirements), rm01_dependencies)

    def test_confirmed_dependency_finding_blocks_published_dependent(self):
        current_entries = entries()
        with self.assertRaises(guard.DependencyGuardError):
            guard.validate_failure_propagation(
                bindings(current_entries),
                [finding("ACCORD-ADJ-DEP001")],
                current_entries,
            )

    def test_confirmed_dependency_finding_allows_suspended_dependent(self):
        current_entries = entries()
        current_entries[("ACCORD-C05", "v0.3")]["publication_state"] = "SUSPENDED"
        active = guard.validate_failure_propagation(
            bindings(current_entries),
            [finding("ACCORD-ADJ-DEP001")],
            current_entries,
        )
        self.assertEqual(active, 1)

    def test_nonconfirmed_dependency_review_does_not_propagate(self):
        current_entries = entries()
        active = guard.validate_failure_propagation(
            bindings(current_entries),
            [finding("ACCORD-ADJ-DEP001", disposition="NOT_CONFIRMED")],
            current_entries,
        )
        self.assertEqual(active, 0)
        self.assertEqual(
            current_entries[("ACCORD-C05", "v0.3")]["publication_state"],
            "PUBLISHED",
        )

    def test_superseded_confirmed_finding_is_not_active(self):
        current_entries = entries()
        records = [
            finding("ACCORD-ADJ-DEP001"),
            finding(
                "ACCORD-ADJ-DEP002",
                disposition="NOT_CONFIRMED",
                supersedes="ACCORD-ADJ-DEP001",
            ),
        ]
        active = guard.validate_failure_propagation(
            bindings(current_entries),
            records,
            current_entries,
        )
        self.assertEqual(active, 0)

    def test_plain_dependency_supersession_without_confirmed_finding_does_not_propagate(self):
        current_entries = entries()
        current_entries[("ACCORD-C03", "v0.2")]["publication_state"] = "SUPERSEDED"
        active = guard.validate_failure_propagation(
            bindings(current_entries),
            [],
            current_entries,
        )
        self.assertEqual(active, 0)


if __name__ == "__main__":
    unittest.main()
