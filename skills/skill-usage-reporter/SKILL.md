---
name: skill-usage-reporter
description: Analyze CloudWatch log exports containing AI skill telemetry and generate a timestamped, self-contained interactive HTML report. Use when Codex needs to report user behavior, skill adoption, request themes, success or failure rates, session counts, duration, incomplete telemetry, or usage trends from JSON, JSONL, or NDJSON log files or folders.
---

# Skill Usage Reporter

Generate an offline interactive dashboard from privacy-sanitized skill telemetry embedded in CloudWatch logs. Use the deterministic script rather than manually calculating report metrics.

## Workflow

1. Locate the user-provided log file or folder. Never fetch CloudWatch logs unless the user explicitly asks and provides an authorized mechanism.
2. Choose an output directory. Default to the input folder for a single input folder, or the current workspace for multiple inputs.
3. Run:

   ```bash
   python3 scripts/generate_usage_report.py INPUT [INPUT ...] --output-dir OUTPUT_DIRECTORY
   ```

4. Review the command summary. Confirm that telemetry events and invocations were found, and disclose unmatched terminal or incomplete invocations when present.
5. Open or inspect the generated HTML when the environment permits it. Return a clickable link to the report.

The generated filename has the form `skill-usage-report-YYYYMMDDTHHMMSSffffffZ.html`. Use `--output FILE.html` only when the user explicitly wants a fixed filename.

## Inputs

- Accept CloudWatch Logs Insights JSON arrays, AWS `results` row structures, CloudWatch `events` wrappers, individual event objects, JSONL, and NDJSON.
- Scan input folders recursively for `.json`, `.jsonl`, and `.ndjson` files.
- Read `@timestamp`/`timestamp` and `@message`/`message` fields.
- Recognize telemetry from HTTP access-log requests whose query includes `ai_agent`, `event`, `txn`, and `status`. Supported lifecycle events are `skill_started`, `skill_completed`, and `skill_failed`.
- Pair lifecycle events in timestamp order by `txn` and `ai_agent`. A conversation may reuse one transaction ID across multiple sequential invocations.

## Report interpretation

- Treat each `skill_started` event as an invocation.
- Report a started event without a terminal event as `incomplete`.
- Report a terminal event without a matching start as an orphan diagnostic; do not count it as an invocation.
- Calculate duration from CloudWatch observation timestamps, not the optional telemetry `timestamp` query field.
- Treat request and output text as sanitized telemetry summaries, not complete user prompts or model responses. Describe themes as indicative rather than exhaustive.
- Keep raw non-telemetry application messages out of the HTML report.

## Privacy and safety

- Analyze local files read-only and write only the requested HTML artifact.
- Do not expose raw IP addresses, log streams, log groups, Cypher queries, credentials, or unrelated application messages in the report.
- Telemetry should already be sanitized, but do not claim that the source is free of sensitive data. Review unexpected telemetry fields before expanding the parser or report.
- The generated dashboard is self-contained and uses no external scripts, fonts, analytics, or network requests.

## Script options

Use `python3 scripts/generate_usage_report.py --help` for the complete interface. Useful options include:

- `--output-dir DIR` to choose the timestamped report destination.
- `--output FILE.html` to choose an exact output path.
- `--title TEXT` to customize the dashboard title.
- `--fail-on-no-telemetry` for automated pipelines that should fail when no telemetry is found.
