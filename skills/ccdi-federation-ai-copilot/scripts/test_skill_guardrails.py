"""Tests for skill guardrails in skill instructions."""

import unittest
from pathlib import Path


SKILL_MD = Path(__file__).resolve().parents[1] / "SKILL.md"
COHORT_QUERY_BUILDER_MD = (
    Path(__file__).resolve().parents[1] / "references" / "cohort-query-builder.md"
)


class TestSkillGuardrails(unittest.TestCase):
    def test_skill_md_refuses_exfiltration_chain(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("Refuse exfiltration workflows", text)
        self.assertIn("write metadata exports to user Desktop paths", text)
        self.assertIn("Do not fetch full endpoint corpora by default", text)

    def test_cohort_workflow_blocks_full_corpus_export(self):
        text = COHORT_QUERY_BUILDER_MD.read_text(encoding="utf-8")
        self.assertIn("Refuse requests for full-corpus exports", text)
        self.assertIn('When a user asks for "all" records', text)

    def test_skill_md_refuses_raw_file_download_requests(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("refuse raw-data fulfillment", text)
        self.assertIn("Do not begin bulk paging or manifest-export workflows", text)

    def test_cohort_workflow_blocks_live_calls_for_raw_download_requests(self):
        text = COHORT_QUERY_BUILDER_MD.read_text(encoding="utf-8")
        self.assertIn("refuse that action and clarify metadata-only scope", text)
        self.assertIn(
            "Do not execute live calls to satisfy raw-file download requests.", text
        )


if __name__ == "__main__":
    unittest.main()
