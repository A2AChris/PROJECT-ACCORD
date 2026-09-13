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

DEPENDENCIES = json.loads(
    (ROOT / "claims" / "public-semantic-dependencies.json").read_text(encoding="utf-8")
)
STATE_REGISTRY = json.loads(
    (ROOT / "claims" / "public-claim-state.json").read_text(encoding="utf-8")
)


def set_state(registry, claim_id, revision, state):
    for entry in registry["entries"]:
        if entry["id"] == claim_id and entry["revision"] == revision:
            entry["publication_state"] = state
            return
    raise AssertionError(f"missing claim state: {claim_id} {revision}")


class SemanticDependencyGuardTests(unittest.TestCase):
    def test_current_dependency_registry_is_consistent(self):
        guard.validate_dependencies(
            copy.deepcopy(DEPENDENCIES), copy.deepcopy(STATE_REGISTRY)
        )

    def test_dependency_leaving_published_rejects_unchanged_published_dependent(self):
        states = copy.deepcopy(STATE_REGISTRY)
        set_state(states, "ACCORD-C03", "v0.2", "SUSPENDED")
        with self.assertRaises(guard.DependencyGuardError):
            guard.validate_dependencies(copy.deepcopy(DEPENDENCIES), states)

    def test_explicitly_suspended_dependent_is_fail_closed_not_auto_falsified(self):
        states = copy.deepcopy(STATE_REGISTRY)
        set_state(states, "ACCORD-C04", "v0.2", "SUSPENDED")
        set_state(states, "ACCORD-C05", "v0.3", "SUSPENDED")
        guard.validate_dependencies(copy.deepcopy(DEPENDENCIES), states)


if __name__ == "__main__":
    unittest.main()
