import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


REFERENCE_DIR = Path(__file__).resolve().parent
PPTX_PATH = REFERENCE_DIR / "qag-copilot.pptx"


class TestReferenceAssets(unittest.TestCase):
    def test_qag_copilot_pptx_scrubs_creator_metadata(self):
        with ZipFile(PPTX_PATH) as zf:
            root = ET.fromstring(zf.read("docProps/core.xml"))

        namespaces = {
            "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        self.assertIsNone(root.find("dc:creator", namespaces))
        self.assertIsNone(root.find("cp:lastModifiedBy", namespaces))

    def test_qag_copilot_pptx_external_links_match_documented_allowlist(self):
        expected = {
            "https://qag.m3aicommons.org",
            "https://www.biorxiv.org/content/10.1101/2025.09.02.673797v1.full.pdf",
        }
        found = set()

        with ZipFile(PPTX_PATH) as zf:
            for name in zf.namelist():
                if not name.endswith(".rels"):
                    continue
                root = ET.fromstring(zf.read(name))
                for rel in root.findall("{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
                    if rel.attrib.get("TargetMode") == "External":
                        found.add(rel.attrib["Target"])

        self.assertEqual(found, expected)


if __name__ == "__main__":
    unittest.main()
