# CCDI Federation API AgentSkill Design (Implemented State)

## Goal

Provide a reusable metadata-only AgentSkill for CCDI Federation tasks:

- Cohort query planning and optional execution guidance
- Endpoint and response explanation
- Controlled-value (PV) normalization support
- Safe routing with explicit assumptions and guardrails

The skill is intentionally lightweight: prompt-driven orchestration first, helper scripts second.

## Current Implementation Snapshot

This document reflects what is currently implemented in `skills/ccdi-federation-helper` and `mcp/`.

### Implemented project structure

```text
ccdi-federation-agentskill/
├── mcp/
│   ├── ccdi_mcp_server.js        (Node.js stdio MCP server)
│   ├── package.json
│   └── package-lock.json
├── .mcp.json                      (MCP server registration: ccdi-federation)
└── skills/ccdi-federation-helper/
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
MCP Server (ccdi-federation) [PREFERRED]    OR    Optional helper scripts [FALLBACK]
├─ list_operations                               (pv_mapper.py, ccdi_client.py)
├─ get_operation_schema
├─ call_operation (validated GET)
└─ call_raw_get (raw GET)
  ↓
CCDI Federation metadata API (only when explicitly requested)
  ↓
User-facing explanation/plan/summary
```

### Design principle

```text
SKILL.md + references = reasoning, routing, policy
MCP server            = validated API execution (preferred path)
scripts               = minimal deterministic helpers (fallback)
```

### Execution layering

1. **Prompt layer**: SKILL.md routes based on user intent
2. **Planning layer**: Reference docs define cohort and API planning workflows
3. **Execution layer** (MCP-first):
   - If `ccdi-federation` MCP server is available, use its tools:
     - `list_operations`: discover valid endpoints from OpenAPI spec
     - `get_operation_schema`: inspect required/optional parameters for a path
     - `call_operation`: execute validated OpenAPI-backed GET calls by path
     - `call_raw_get`: fallback for raw GET requests that bypass OpenAPI validation
   - If MCP server is unavailable, fall back to Python helper scripts or direct API fetching
4. **Response layer**: Summarize and explain execution results with assumptions and errors

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
5. Optionally execute read-only metadata API calls on explicit request via MCP server:
   - Checks whether `ccdi-federation` MCP server is available
   - Uses `call_operation` for validated OpenAPI-backed calls
   - Falls back to direct API fetching if MCP is unavailable
6. Return summary with assumptions, ambiguities, and limitations

Important current defaults documented in the workflow:

- `GET` read-only metadata execution (always read-only, never write)
- Preferred: MCP server (`ccdi-federation`) for execution when available
- Fallback: direct HTTP fetch or Python helpers if MCP unavailable
- Default `10` results per page
- Default max `3` pages unless user asks for more

### API Explainer (`references/api-explainer.md`)

Implemented contract includes:

1. Explain endpoint purpose, methods, parameters, pagination, and response shape
2. MCP Server Layer (Implemented)

### `mcp/ccdi_mcp_server.js`

Implemented Node.js stdio MCP server exposing four tools:

1. **`list_operations`**: Enumerate available GET endpoints extracted from OpenAPI spec
2. **`get_operation_schema`**: Inspect required and optional parameters for a specific API path
3. **`call_operation`**: Execute validated OpenAPI-backed GET call by path
   - Input: `path`, `path_params` (optional), `query_params` (optional), `base_url` (optional), `timeout_seconds`, `max_retries`, `strict_query_validation`
   - Output: Structured response with `ok`, `status`, `headers`, `payload`, `resolved_path`, `base_url`, and `warnings`
4. **`call_raw_get`**: Execute raw read-only GET against configured base URL (fallback)
   - Input: `path`, `query_params` (optional), `base_url` (optional), `timeout_seconds`, `max_retries`
   - Output: Same structured envelope as `call_operation`

### MCP Registration

- Server registered in `.mcp.json` as `ccdi-federation`
- Entry command: `node /path/to/mcp/ccdi_mcp_server.js`
- Transport: stdio

## Helper Script Layer (Fallback)

### `scripts/ccdi_client.py`

Fallback capabilities (used only when MCP server is unavailable)
## Script Layer (Implemented)
Execution Path Preference (MCP-First Strategy)

Current implementation now prioritizes the MCP server for live API execution:

1. **Preferred path**: Check if `ccdi-federation` MCP server is available in the environment
   - If available, use `call_operation` or `list_operations` for API interaction
   - This provides validated, schema-aware execution with proper error handling
2. **Fallback path**: If MCP is unavailable, use Python helper scripts or direct HTTP fetch
   - Maintains backward compatibility with environments that don't have MCP infrastructure

This MCP-first strategy is documented in `references/cohort-query-builder.md` and enforced by the workflow.

## Scope Clarification

The package README references additional workflows (for example, sanity checking and QA helpers), but those script modules are not present in the current skill directory.

Design implication:

- Current implementation is a metadata planning/explainer skill with an MCP server for validated API execution.
- Python helper scripts remain as optional fallback
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