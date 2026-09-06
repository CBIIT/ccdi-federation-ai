# CCDI Federation AI

[![Install via npx skills](https://img.shields.io/badge/npx%20skills-install-blue)](https://www.skills.sh/cbiit/ccdi-federation-ai/ccdi-federation-ai-copilot)
[![snyk-security-scan](https://img.shields.io/github/actions/workflow/status/CBIIT/ccdi-federation-ai/snyk-security-scan.yml)](https://github.com/CBIIT/ccdi-federation-ai/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Last Update](https://img.shields.io/github/last-commit/CBIIT/ccdi-federation-ai?label=Last%20update&style=classic)](https://github.com/CBIIT/ccdi-federation-ai)
[![Snyk Check](https://github.com/CBIIT/ccdi-federation-ai/actions/workflows/snyk-security-scan.yml/badge.svg)](https://github.com/CBIIT/ccdi-federation-ai/actions)

An AI agent skill for the [CCDI Data Federation API](https://ccdi.cancer.gov/data-federation-resource). This repository provides components for AI-ready CCDI Federation metadata, including an AgentSkill that standardizes AI interactions through workflows and routing.

## Skill Structure

Each skill directory contains:

- **SKILL.md** — Main instruction file with YAML frontmatter, routing rules, guardrails, and response style guidelines
- **scripts/** — Helper scripts and utilities (PV mapper, fallback API client)
- **references/** — OpenAPI spec, permissible-value metadata, and workflow references
- **agents/** — Agent-specific configuration

Repository layout:

- `skills/ccdi-federation-ai-copilot/` — AgentSkill docs, routing, and fallback scripts
- `skills/skill-usage-reporter/` — CloudWatch telemetry analysis and interactive HTML usage reporting
- `docs/instructions/` — End-user and developer setup guides

## Getting Started

### Install Skill from GUI

Follow the step-by-step guide to install and use the skill on Chatgpt:

- [docs/instructions/chatgpt-instruction.md](./docs/instructions/chatgpt-instruction.md)

![Using the skill in chatgpt](./docs/instructions/images/9-codex-use-skill2.png)

### Use NPX to install a skill

Install the skill bundle via [npx](https://docs.npmjs.com/cli/commands/npx):

```bash
npx skills add CBIIT/ccdi-federation-ai
```

## Use the Skill Usage Reporter

The `skill-usage-reporter` analyzes telemetry events in exported CloudWatch
logs and creates a self-contained, interactive HTML dashboard. The report
includes invocation counts, success and failure rates, incomplete events,
session counts, duration, usage trends, skill breakdowns, and user-intent
summaries.

### Use it with Codex

Provide one or more CloudWatch log files, or place the files in a folder, and
ask Codex to run the skill. For example:

```text
Use $skill-usage-reporter to analyze the CloudWatch logs in ./logs and create
an interactive usage report in ./reports.
```

Supported inputs include `.json`, `.jsonl`, and `.ndjson` files. Input folders
are scanned recursively.

### Run the report generator directly

From the repository root, analyze a folder and write a timestamped report:

```bash
python3 skills/skill-usage-reporter/scripts/generate_usage_report.py \
  ./logs \
  --output-dir ./reports
```

Analyze multiple files or folders in one report:

```bash
python3 skills/skill-usage-reporter/scripts/generate_usage_report.py \
  ./logs/week-1.json \
  ./logs/week-2 \
  --output-dir ./reports \
  --title "CCDI Skill Usage Report"
```

To try the included sample log:

```bash
python3 skills/skill-usage-reporter/scripts/generate_usage_report.py \
  skills/ccdi-federation-ai-copilot/assets/log-analytics-results-2026-09-06.json \
  --output-dir ./reports
```

The generated filename uses the pattern
`skill-usage-report-YYYYMMDDTHHMMSSffffffZ.html`, preventing reports from
overwriting one another. Open the HTML file in a browser to filter by date,
skill, status, or text; sort invocation details; and export filtered rows to
CSV. The report is fully offline and makes no external network requests.

Run the following command for all available options:

```bash
python3 skills/skill-usage-reporter/scripts/generate_usage_report.py --help
```

## Links

- [CCDI Data Federation](https://ccdi.cancer.gov/data-federation-resource)
- [CCDI Data Federation API documentation](https://cbiit.github.io/ccdi-federation-api/overview.html)
- [Childhood Cancer Data Initiative (CCDI)](https://ccdi.cancer.gov/)

## Disclaimer

This software is provided as-is for research and data exploration purposes. It is maintained by the [Center for Biomedical Informatics and Information Technology (CBIIT)](https://www.cancer.gov/about-nci/organization/cbiit) at the National Cancer Institute. All API calls made through this skill are read-only and access only publicly available CCDI Federation metadata.
