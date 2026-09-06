#!/usr/bin/env python3
"""Tests for the skill usage report generator."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("generate_usage_report.py")
SPEC = importlib.util.spec_from_file_location("generate_usage_report", MODULE_PATH)
REPORTER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(REPORTER)


def access_event(timestamp, event, status, request="", output="", txn="session-1"):
    target = (
        "/version?ai_agent=test-skill"
        f"&event={event}&user_input={request}&ai_output={output}"
        f"&txn={txn}&status={status}"
    )
    return {
        "@timestamp": timestamp,
        "@message": f'INFO: 10.0.0.1:123 - "GET {target} HTTP/1.1" 200 OK',
    }


class ReporterTests(unittest.TestCase):
    def test_pairs_reused_transaction_and_generates_private_html(self):
        records = [
            access_event("2026-09-06T10:00:00Z", "skill_started", "started", "Count+subjects"),
            {"@timestamp": "2026-09-06T10:00:02Z", "@message": "secret unrelated raw log"},
            access_event("2026-09-06T10:00:05Z", "skill_completed", "success", "Count+subjects", "Returned+counts"),
            access_event("2026-09-06T10:01:00Z", "skill_started", "started", "Find+samples"),
            access_event("2026-09-06T10:01:08Z", "skill_failed", "failed", "Find+samples", "API+failed"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "logs.json"
            source.write_text(json.dumps(records), encoding="utf-8")
            args = REPORTER.parse_args([str(source), "--output-dir", str(root)])
            output, data = REPORTER.generate(args)
            self.assertRegex(output.name, r"^skill-usage-report-\d{8}T\d{12}Z\.html$")
            self.assertEqual([x["result"] for x in data["invocations"]], ["success", "failed"])
            self.assertEqual([x["duration_seconds"] for x in data["invocations"]], [5.0, 8.0])
            html = output.read_text(encoding="utf-8")
            self.assertIn("Count subjects", html)
            self.assertNotIn("secret unrelated raw log", html)
            self.assertNotIn("10.0.0.1", html)
            self.assertIn("Export filtered CSV", html)
            self.assertIn('lines.join("\\n")', html)

    def test_reads_cloudwatch_results_and_tracks_orphan(self):
        event = access_event("2026-09-06T10:00:05Z", "skill_completed", "success")
        row = [{"field": key, "value": value} for key, value in event.items()]
        records = REPORTER.records_from_json({"results": [row]})
        telemetry = REPORTER.extract_telemetry(records[0], Path("query.json"))
        invocations, orphans = REPORTER.pair_invocations([telemetry])
        self.assertEqual(invocations, [])
        self.assertEqual(len(orphans), 1)

    def test_reads_json_lines_and_reports_incomplete(self):
        record = access_event("2026-09-06T10:00:00Z", "skill_started", "started")
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "events.jsonl"
            source.write_text(json.dumps(record) + "\nnot-json\n", encoding="utf-8")
            records, warnings = REPORTER.load_records(source)
            self.assertEqual(len(records), 1)
            self.assertEqual(len(warnings), 1)
            telemetry = REPORTER.extract_telemetry(records[0], source)
            invocations, _ = REPORTER.pair_invocations([telemetry])
            self.assertEqual(invocations[0]["result"], "incomplete")


if __name__ == "__main__":
    unittest.main()
