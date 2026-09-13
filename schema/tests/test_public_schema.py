import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "public_schema", ROOT / "tools" / "public_schema.py"
)
ps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ps)

LEGACY_SCHEMA_PATHS = {
    "challenge/adjudications/adjudication-record.schema.json",
    "challenge/adjudications/adjudication-record.v0.2.schema.json",
    "challenge/adjudications/index.schema.json",
    "challenge/adjudications/index.v0.2.schema.json",
    "challenge/receipts/index.schema.json",
    "claims/public-claim-state.schema.json",
    "claims/public-semantic-dependencies.schema.json",
}
LEGACY_ID_PREFIX = "https://project-accord.example/schema/"
NEW_ID_PREFIX = "urn:project-accord:schema:"


class PublicSchemaContractTests(unittest.TestCase):
    def test_current_public_artifacts_conform_to_published_schemas(self):
        targets = [
            (
                ROOT / "claims" / "public-claim-index.json",
                ROOT / "claims" / "public-claim-index.schema.json",
            ),
            (
                ROOT / "claims" / "public-claim-state.json",
                ROOT / "claims" / "public-claim-state.schema.json",
            ),
            (
                ROOT / "claims" / "public-semantic-dependencies.json",
                ROOT / "claims" / "public-semantic-dependencies.schema.json",
            ),
            (
                ROOT / "challenge" / "fixtures" / "template.json",
                ROOT / "challenge" / "fixtures" / "fixture.schema.json",
            ),
            (
                ROOT / "challenge" / "receipts" / "index.json",
                ROOT / "challenge" / "receipts" / "index.schema.json",
            ),
            (
                ROOT / "challenge" / "adjudications" / "index.json",
                ROOT / "challenge" / "adjudications" / "index.schema.json",
            ),
            (
                ROOT / "evidence" / "ACCORD-RM01-REFERENCE-EVIDENCE-v0.6.json",
                ROOT / "evidence" / "evidence-record.schema.json",
            ),
        ]
        targets.extend(
            (path, ROOT / "challenge" / "fixtures" / "fixture.schema.json")
            for path in sorted((ROOT / "challenge" / "fixtures" / "examples").glob("*.json"))
        )
        targets.extend(
            (
                path,
                ROOT
                / "challenge"
                / "adjudications"
                / "adjudication-record.schema.json",
            )
            for path in sorted(
                (ROOT / "challenge" / "adjudications" / "records").glob("*.json")
            )
        )
        for instance_path, schema_path in targets:
            with self.subTest(instance=instance_path.name):
                ps.validate_paths(instance_path, schema_path)

    def test_schema_ids_are_unique_and_follow_identifier_policy(self):
        registry = json.loads(
            (ROOT / "schema" / "schema-id-registry.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registry["new_identifier_prefix"], NEW_ID_PREFIX)
        self.assertEqual(
            registry["canonical_access"],
            "REPOSITORY_PATH_AT_EXACT_GIT_REVISION",
        )

        legacy_entries = registry["legacy_non_dereferenceable_identifiers"]
        self.assertEqual(
            {entry["path"] for entry in legacy_entries},
            LEGACY_SCHEMA_PATHS,
        )
        for entry in legacy_entries:
            self.assertEqual(
                entry["classification"],
                "NON_DEREFERENCEABLE_LEGACY_IDENTIFIER",
            )
            self.assertIs(entry["dereferenceable"], False)
            self.assertTrue(entry["id"].startswith(LEGACY_ID_PREFIX))

        registered_legacy = {
            entry["path"]: entry["id"] for entry in legacy_entries
        }
        seen_ids = {}
        schema_paths = sorted(ROOT.rglob("*.schema.json"))
        self.assertTrue(schema_paths)
        for path in schema_paths:
            rel = path.relative_to(ROOT).as_posix()
            document = json.loads(path.read_text(encoding="utf-8"))
            schema_id = document.get("$id")
            self.assertIsInstance(schema_id, str, rel)
            self.assertTrue(schema_id, rel)
            self.assertNotIn(schema_id, seen_ids, rel)
            seen_ids[schema_id] = rel

            if schema_id.startswith(LEGACY_ID_PREFIX):
                self.assertIn(rel, registered_legacy)
                self.assertEqual(registered_legacy[rel], schema_id)
            else:
                self.assertTrue(
                    schema_id.startswith(NEW_ID_PREFIX),
                    f"{rel}: new/non-legacy schema id must use {NEW_ID_PREFIX}",
                )

    def test_schema_identifier_policy_denies_network_registry_claim_for_legacy_ids(self):
        text = (ROOT / "schema" / "SCHEMA-IDENTIFIER-POLICY.md").read_text(
            encoding="utf-8"
        )
        required = (
            "NON_DEREFERENCEABLE_LEGACY_IDENTIFIER",
            "does **not** claim that every",
            "repository path at an exact Git revision",
            "urn:project-accord:schema:",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_unknown_schema_keyword_fails_closed(self):
        schema = {"type": "object", "futureKeyword": True}
        with self.assertRaises(ps.SchemaContractError):
            ps.check_supported_schema(schema)

    def test_additional_properties_false_is_enforced(self):
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {"known": {"type": "string"}},
        }
        ps.check_supported_schema(schema)
        with self.assertRaises(ps.SchemaContractError):
            ps.validate_instance({"known": "ok", "extra": "no"}, schema)

    def test_unique_items_is_enforced_for_objects(self):
        schema = {
            "type": "array",
            "uniqueItems": True,
            "items": {"type": "object"},
        }
        ps.check_supported_schema(schema)
        with self.assertRaises(ps.SchemaContractError):
            ps.validate_instance([{"a": 1}, {"a": 1}], schema)

    def test_integer_does_not_accept_boolean(self):
        schema = {"type": "integer", "minimum": 0}
        ps.check_supported_schema(schema)
        with self.assertRaises(ps.SchemaContractError):
            ps.validate_instance(True, schema)

    def test_pattern_and_bounds_are_enforced(self):
        schema = {
            "type": "string",
            "minLength": 3,
            "maxLength": 6,
            "pattern": "^[A-Z]+$",
        }
        ps.check_supported_schema(schema)
        ps.validate_instance("ABC", schema)
        for invalid in ("AB", "ABCDEFG", "AbC"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ps.SchemaContractError):
                    ps.validate_instance(invalid, schema)


if __name__ == "__main__":
    unittest.main()
