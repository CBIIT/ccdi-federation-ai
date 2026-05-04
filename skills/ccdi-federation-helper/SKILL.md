---
name: ccdi-federation-helper
description: Build CCDI cohort plans, explain metadata endpoints, run cohort sanity checks, and execute metadata QA using metadata-only guardrails.
---

## Routing

- Cohort Query Builder -> `references/cohort-query-builder.md`
- Endpoint or Response Explainer -> `references/api-explainer.md`

## Response Style

- Conversational asks: prose-first summary with optional structured detail.
- Planning, QA, and validation asks: structured-first output with explicit assumptions and warnings.

## Execution Policy

- Default to planning or explanation mode.
- Only call live read-only API workflows when the user explicitly asks.
- Keep live execution scoped to metadata-only GET requests.

## Mapping Policy

- Use Permissible Value mappings when available.
- Surface labeled assumptions instead of inventing unsupported mappings.
- Preserve per-node errors and coverage changes in QA-oriented responses.

## Guardrails

- Default to planning or explanation unless the user explicitly asks for live execution.
- Surface Permissible Value mapping decisions, assumptions, and per-node errors.