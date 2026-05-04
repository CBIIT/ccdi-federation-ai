# CCDI Federation API AgentSkill Design (Implemented State)

## Goal

Provide a reusable metadata-only AgentSkill for CCDI Federation tasks:

- Cohort query planning and optional execution guidance
- Endpoint and response explanation
- Controlled-value (PV) normalization support
- Safe routing with explicit assumptions and guardrails

The skill is intentionally lightweight: prompt-driven orchestration first, helper scripts second.

## Current Implementation Snapshot

This document reflects what is currently implemented in `skills/ccdi-federation-helper`.

### Implemented skill package structure

```text
skills/ccdi-federation-helper/
├── SKILL.md
├── README.md
├── assets/
├── schemas/
├── references/
│   ├── api-explainer.md
│   ├── cohort-query-builder.md
│   ├── openapi.yml
│   └── pv/
│       ├── file-pv-metadata.json
│       ├── sample-pv-metadata.json
│       └── subject-pv-metadata.json
└── scripts/
    ├── ccdi_client.py
    └── pv_mapper.py
```

## Architecture Overview

### Runtime model

```text
User Request
  ↓
AI Assistant
  ↓
CCDI Federation Helper (router policy in SKILL.md)
  ↓
Reference workflow docs (cohort-query-builder / api-explainer)
  ↓
Optional helper scripts (pv_mapper.py, ccdi_client.py)
  ↓
CCDI Federation metadata API (only when explicitly requested)
  ↓
User-facing explanation/plan/summary
```

### Design principle

```text
SKILL.md + references = reasoning, routing, policy
scripts                = minimal deterministic helpers
```

## Router Behavior (Implemented)

`SKILL.md` currently routes to two reference workflows:

- Cohort Query Builder -> `references/cohort-query-builder.md`
- Endpoint or Response Explainer -> `references/api-explainer.md`

Routing behavior is policy-centric, not code-centric. Most behavior is encoded in markdown instructions.

## Implemented Policies

The following are already defined and active in `SKILL.md` and the workflow docs.

### Response style

- Conversational asks: prose-first summary with optional structured detail
- Planning/validation asks: structured-first output with explicit assumptions and warnings

### Execution policy

- Default mode is planning/explanation
- Live API execution happens only on explicit user request
- Live execution is read-only and metadata-only

### Mapping policy

- Use permissible-value references when available
- Do not invent unsupported mappings
- Surface ambiguities and assumptions explicitly

### Guardrails

- Metadata-only scope
- No raw data claims
- Preserve node/page/API errors when discussing execution results

## Reference Workflow Contracts

### Cohort Query Builder (`references/cohort-query-builder.md`)

Implemented contract includes:

1. Interpret cohort intent in natural language
2. Identify entity scope (`subject`, `sample`, `file`, or cross-entity)
3. Normalize controlled values using PV metadata
4. Validate route/parameters against `references/openapi.yml`
5. Optionally execute read-only metadata API calls on explicit request
6. Return summary with assumptions, ambiguities, and limitations

Important current defaults documented in the workflow:

- `GET` read-only metadata execution
- Default `10` results per page
- Default max `3` pages unless user asks for more

### API Explainer (`references/api-explainer.md`)

Implemented contract includes:

1. Explain endpoint purpose, methods, parameters, pagination, and response shape
2. Use `references/openapi.yml` as route/parameter source of truth
3. Use PV metadata for controlled-value interpretation
4. Explain harmonized vs unharmonized metadata distinctions
5. Avoid inventing undocumented routes/fields/PVs

## Script Layer (Implemented)

### `scripts/ccdi_client.py`

Current implemented capabilities:

- Build URL with encoded query parameters
- Execute read-only GET requests
- Parse JSON responses
- Return structured success/error envelopes
- Support configurable timeout and retry count

### `scripts/pv_mapper.py`

Current implemented capabilities:

- Load PV metadata by endpoint type (`file`, `sample`, `subject`)
- List controlled fields
- Retrieve permissible values for a field
- Validate field/value pair existence
- Return field-level metadata

## Scope Clarification

The package README references additional workflows (for example, sanity checking and QA helpers), but those script modules are not present in the current skill directory.

Design implication:

- Current implementation is a minimal metadata planning/explainer skill with two concrete helper scripts.
- Additional QA/sanity modules remain extension work rather than active implementation in this folder.

## Future Extension Points

If expanded, keep current policies unchanged and add modules incrementally:

- Query-plan validation helper
- Response summarization helper
- Sanity-check and QA runner helpers
- Snapshot comparison utilities

Each added module should preserve the same constraints:

- metadata-only behavior
- explicit assumption reporting
- per-node/per-page error preservation
- OpenAPI-driven validation