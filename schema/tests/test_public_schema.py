import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "public_schema", ROOT / "tools" / "public_schema.py"
)
ps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ps)


class PublicSchemaContractTests(unittest.TestCase):
    def test_current_public_artifacts_conform_to_published_schemas(self):
        targets = [
            (
                ROOT / "claims" / "public-claim-index.json",
                ROOT / "claims" / "public-claim-index.schema.json",
            ),
            (
                ROOT / "challenge" / "fixtures" / "template.json",
                ROOT / "challenge" / "fixtures" / "fixture.schema.json",
            ),
            (
                ROOT / "evidence" / "ACCORD-RM01-REFERENCE-EVIDENCE-v0.4.json",
                ROOT / "evidence" / "evidence-record.schema.json",
            ),
        ]
        targets.extend(
            (path, ROOT / "challenge" / "fixtures" / "fixture.schema.json")
            for path in sorted((ROOT / "challenge" / "fixtures" / "examples").glob("*.json"))
        )
        for instance_path, schema_path in targets:
            with self.subTest(instance=instance_path.name):
                ps.validate_paths(instance_path, schema_path)

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
