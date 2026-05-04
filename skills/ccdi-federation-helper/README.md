# CCDI Federation Helper

This package rebuilds the minimal AgentSkill scaffold for CCDI federation workflows.

## Implemented Workflows

- Cohort Query Builder: `scripts/build_query.py`, `scripts/pv_mapper.py`, `scripts/validate_plan.py`
- Endpoint or Response Explainer: `scripts/explain_endpoint.py`
- Cohort Sanity Checker: `scripts/summarize_response.py`, `scripts/sanity_check.py`
- Metadata QA Assistant: `scripts/qa_runner.py`, `scripts/compare_snapshot.py`, `scripts/ccdi_client.py`

## Included In The Skill Package

- Parent skill router in `SKILL.md`
- Workflow reference docs under `references/`
- Local copy of the CCDI OpenAPI spec at `references/openapi.yml`
- Example payloads and schemas under `assets/` and `schemas/`

## Current Scope

- Cohort query planning
- Endpoint and payload explanation
- Cohort sanity-check guidance
- Node-level metadata QA guidance

This scaffold is metadata-only and defaults to planning or explanation unless live execution is explicitly requested.

## Response Style

- Conversational asks: prose-first summary with optional structured detail.
- Planning, QA, and validation asks: structured-first output with explicit assumptions and warnings.

## Execution Policy

- Default to planning or explanation mode.
- Only use live read-only metadata calls when the user explicitly asks.
- Treat live execution as a minimal helper surface for MVP, not a full orchestration layer.

## Mapping Policy

- Use Permissible Value mappings when available.
- Surface labeled assumptions instead of inventing unsupported mappings.
- Preserve per-node errors and coverage changes in QA-oriented responses.

## Validation

- `python3 .agents/skills/ccdi-federation-helper/scripts/validate_examples.py`
- `python3 -m unittest tests.ccdi_skill.test_scaffold tests.ccdi_skill.test_examples tests.ccdi_skill.test_pv_mapper tests.ccdi_skill.test_validate_plan tests.ccdi_skill.test_build_query tests.ccdi_skill.test_explain_endpoint tests.ccdi_skill.test_summary_and_qa tests.ccdi_skill.test_skill_routing`