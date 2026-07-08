import importlib.util
import pathlib
import tempfile
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parent / "parse_pv_to_json.py"
_SPEC = importlib.util.spec_from_file_location("parse_pv_to_json", MODULE_PATH)
parser = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(parser)


class TestParsePvToJson(unittest.TestCase):
    def test_parse_pv_table_returns_none_without_header(self):
        self.assertIsNone(parser.parse_pv_table(["# no table", "value"]))

    def test_parse_pv_table_parses_rows(self):
        lines = [
            "| Permissible Value | Description | VM Long Name | VM Public ID | Concept Code | Begin Date |",
            "| --- | --- | --- | --- | --- | --- |",
            "| `F` | Female | Female long | 1 | C1 | 2020-01-01 |",
            "| `M` | Male | Male long | 2 | C2 | 2020-01-01 |",
            "",
        ]
        rows = parser.parse_pv_table(lines)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["value"], "F")
        self.assertEqual(rows[1]["description"], "Male")

    def test_parse_pv_md_extracts_field_metadata(self):
        content = """### **`sex`**

**Formal Name: `Sex`** [Link](https://example.org/cde)

This metadata element is defined by the caDSR as "Biological sex at birth".

| Permissible Value | Description | VM Long Name | VM Public ID | Concept Code | Begin Date |
| --- | --- | --- | --- | --- | --- |
| `F` | Female | Female long | 1 | C1 | 2020-01-01 |
| `M` | Male | Male long | 2 | C2 | 2020-01-01 |
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = pathlib.Path(tmpdir) / "subject-pv-metadata.md"
            md_path.write_text(content, encoding="utf-8")

            parsed = parser.parse_pv_md(md_path)
            self.assertIn("sex", parsed)
            field = parsed["sex"]
            self.assertEqual(field["formal_name"], "Sex")
            self.assertEqual(field["cadsr_link"], "https://example.org/cde")
            self.assertEqual(field["cde_description"], "Biological sex at birth")
            self.assertEqual([pv["value"] for pv in field["permissible_values"]], ["F", "M"])


if __name__ == "__main__":
    unittest.main()
