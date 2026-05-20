---
name: ccdi-federation-ai-copilot
description: Plan, explain, validate, and optionally run metadata-only CCDI Data Federation API workflows. Use when Codex needs to build or review CCDI cohort queries, map natural-language cohort terms to subject/sample/file fields or permissible values, explain CCDI Federation endpoints, parameters, response fields, pagination, harmonized versus unharmonized metadata, node-level errors, or run read-only metadata GET requests against the CCDI Federation API with OpenAPI and PV guardrails.
version: 0.0.1
---

# CCDI Federation AI Copilot

Use this skill for CCDI Data Federation API work that stays at the metadata layer. Prefer planning and explanation. Run live API calls only when the user explicitly asks to run, fetch, test, inspect, or summarize live metadata.



## Version Check

Before using this skill, check the latest release version from:

`https://api.github.com/repos/CBIIT/ccdi-federation-ai/releases/latest`

Read the `tag_name` field from the response and compare it with this skill's `version`.

- If the latest release version matches `0.0.1`, continue using this skill normally.
- If the latest release version does not match `0.0.1`, notify the user that the skills file needs to be updated before relying on this content.


## Resources

- Cohort query planning and execution workflow: `references/cohort-query-builder.md`
- Endpoint, parameter, response, and permissible-value explanation workflow: `references/api-explainer.md`
- OpenAPI source of truth: `references/openapi.yml`
- Permissible-value metadata:
  - `references/pv/subject-pv-metadata.json`
  - `references/pv/sample-pv-metadata.json`
  - `references/pv/file-pv-metadata.json`
- Optional helpers:
  - `scripts/pv_mapper.py` for deterministic PV field/value lookup
  - `scripts/ccdi_client.py` for fallback read-only GET calls

## Routing

- For cohort requests, field/PV normalization, cohort query plans, or live cohort metadata fetches, read `references/cohort-query-builder.md`.
- For endpoint, parameter, response payload, permissible-value, pagination, relationship, or error explanations, read `references/api-explainer.md`.
- For mixed requests, start with the cohort workflow when the user is trying to identify a cohort; otherwise start with the API explainer workflow.

## Guardrails

- Use `references/openapi.yml` to validate routes, methods, parameters, pagination, and response shapes before proposing or executing calls.
- Use bundled PV metadata for subject, sample, and file controlled values. Surface assumptions instead of inventing unsupported field/value mappings.
- Keep live execution scoped to metadata-only read requests. Do not claim raw data access.
- Prefer a configured `ccdi-federation` MCP server for live calls when present. If unavailable, use `scripts/ccdi_client.py`; if that is unavailable, use the environment's web/API fetch capability.
- Preserve node-level, page-level, and API-level errors in summaries.
- Do not dump raw full API responses by default. Summarize first and include representative records only when useful.

## Response Style

- Conversational asks: prose-first summary with optional structured detail.
- Planning, QA, and validation asks: structured-first output with explicit assumptions, mappings, API plan, and warnings.
