import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "public_schema", ROOT / "tools" / "public_schema.py"
)
ps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ps)


class SemanticDependencySchemaTests(unittest.TestCase):
    def test_dependency_registry_conforms_to_published_schema(self):
        ps.validate_paths(
            ROOT / "claims" / "public-semantic-dependencies.json",
            ROOT / "claims" / "public-semantic-dependencies.schema.json",
        )


if __name__ == "__main__":
    unittest.main()
