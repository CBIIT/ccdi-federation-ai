# CCDI Data Federation Resource API

This directory contains documentation and reference materials for the CCDI Data Federation Resource API service.

- **about.md**: Provides a detailed description and overview of the project.
- **openapi.yml**: The official OpenAPI/Swagger specification for the API.
- **[endpoint]-api-response.json**: Example JSON responses for specific API endpoints to assist with integration and testing.
- **qag-copilot.pptx**: Slide deck demonstrating the Query Augmented Generation (QAG) tool.

## Reference Asset Notes

- The `qag-copilot.pptx` file has its embedded creator and last-modifier metadata removed.
- The presentation contains two intentional public external hyperlinks:
  - `https://www.biorxiv.org/content/10.1101/2025.09.02.673797v1.full.pdf`
  - `https://qag.m3aicommons.org`
- Some example API payloads intentionally include both `Site_ID` and `site_id` because the upstream CCDI Federation responses expose both spellings. PowerShell JSON cmdlets can treat keys case-insensitively, so prefer a case-sensitive parser or access the raw JSON text when working with these examples in PowerShell.

## Permissible Values (PV) Metadata

The `pv/` directory includes both human-readable Markdown references and machine-consumable JSON files for metadata permissible values.

- `pv/subject-pv-metadata.md`: Subject-level field definitions and permissible values.
- `pv/sample-pv-metadata.md`: Sample-level field definitions and permissible values.
- `pv/file-pv-metadata.md`: File-level field definitions and permissible values.
- `pv/subject-pv-metadata.json`: Structured subject-level mappings (field name -> permissible values).
- `pv/sample-pv-metadata.json`: Structured sample-level mappings (field name -> permissible values).
- `pv/file-pv-metadata.json`: Structured file-level mappings (field name -> permissible values).

Each JSON entry is designed for programmatic and agent consumption and includes:

- field name
- permissible value
- description
- VM long name

## Agent Skill Scaffold

A reusable CCDI Federation skill scaffold is available at:

- `.agents/skills/ccdi-federation-helper/`

This scaffold includes:

- A parent skill router in `SKILL.md`.
- Sub-workflow references for cohort query planning, endpoint explanation, sanity checks, and node QA.
- A local copy of the CCDI OpenAPI document at `references/openapi.yml`.
- Python helper modules for planning, explanation, summarization, QA, and read-only client access under `scripts/`.

The scaffold is metadata-only and defaults to planning or explanation unless live execution is explicitly requested.
