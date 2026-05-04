---
name: api-explainer
description: explain ccdi federation api endpoints, parameters, response fields, permissible values, metadata relationships, example requests, and errors using openapi.yml, pv metadata references, and the ccdi federation api wiki. use this skill when the user asks what an endpoint does, how to call an endpoint, what parameters are supported, what a response field or permissible value means, how subject/sample/file metadata relate, why an api response looks a certain way, or how to interpret pagination, harmonized fields, unharmonized fields, node-level responses, or api errors. keep explanations metadata-only and use api documentation as the source of truth.
---

# API Explainer

## Purpose

Explain CCDI Federation API endpoints, parameters, response shapes, metadata fields, permissible values, relationships, pagination, and errors in clear user-facing language.

Use `references/openapi.yml` as the source of truth for route, method, parameter, pagination, and response validation. Use the local PV metadata files and the CCDI Federation API wiki for permissible-value explanation.

This skill is for explanation and onboarding. It helps users understand how the API works before or after they run metadata queries.

## API configuration

- API host: `https://federation.ccdi.cancer.gov/`
- API version base path: `/api/v1/`
- Route and parameter source of truth: `references/openapi.yml`
- Permissible-value explanation reference: `https://github.com/CBIIT/ccdi-federation-api/wiki`
- Explain only metadata-level API behavior.
- Do not claim raw data access.

Use `openapi.yml` to confirm:

- available endpoints
- supported HTTP methods
- required and optional parameters
- parameter names and types
- pagination behavior
- response schema or response examples when available
- documented errors and status codes

Use the following PV metadata files when available:

- `references/subject-pv-metadata.json`
- `references/sample-pv-metadata.json`
- `references/file-pv-metadata.json`

## Default behavior

- Default to explanation mode.
- Do not execute live API calls unless the user explicitly asks to test, fetch, or inspect live metadata.
- When the user asks how an endpoint works, explain the endpoint purpose, method, path, parameters, pagination, response shape, and common use cases.
- When the user provides an API response, summarize and explain the response rather than dumping it back.
- When the user asks about a field, explain the field meaning, entity context, expected value type, controlled-value status, and relationship to other metadata when known.
- When the user asks about a permissible value, explain the exact PV, field, entity, meaning, description, caDSR reference when available, and similar alternatives when relevant.
- If route, field, or PV details are not present in `openapi.yml`, bundled PV metadata, or the referenced CCDI Federation API wiki, clearly say what is missing instead of inventing details.
- Preserve and explain node-level, page-level, and API-level errors.

## Workflow

1. Identify the user's explanation target:
   - endpoint
   - parameter
   - response field
   - permissible value
   - full API response
   - error message
   - pagination behavior
   - subject/sample/file relationship
   - harmonized vs unharmonized metadata

2. Consult `references/openapi.yml` when endpoint, method, route, parameter, pagination, or response-shape details are needed.

3. If the user asks about metadata fields or permissible values, use the relevant PV metadata references when available:
   - `references/pv/subject-pv-metadata.json`
   - `references/pv/sample-pv-metadata.json`
   - `references/pv/file-pv-metadata.json`

4. For broader permissible-value background, refer to the CCDI Federation API wiki:
   - `https://github.com/CBIIT/ccdi-federation-api/wiki`

5. Explain the API behavior in user-facing language:
   - what the endpoint is for
   - what kind of metadata it returns
   - what filters or query parameters it supports
   - how pagination works
   - what the key response fields mean
   - what permissible values mean in context
   - what assumptions or limitations apply

6. If the user provided a response payload:
   - identify the endpoint if possible
   - summarize record counts and key fields
   - explain nested structures
   - identify missing or null fields
   - explain controlled-value fields when relevant
   - explain per-node or per-page errors
   - distinguish empty results from API errors

7. If the user asks for an example request:
   - build a documented request using the base path and supported parameters
   - include method, endpoint, query parameters, and a short explanation
   - do not invent unsupported parameters

8. If the user asks to run or test the API:
   - prefer the environment’s internal web/API fetching tool when available
   - use metadata-only read requests
   - summarize the returned metadata
   - report endpoint, method, parameters, pagination, returned records, and errors
   - avoid long-running or full-export behavior unless explicitly requested

## Explanation rules

- Use `openapi.yml` as the source of truth for routes and parameters.
- Use PV metadata and the CCDI Federation API wiki as the source of truth for controlled-value explanation.
- Do not invent routes, parameters, fields, response schemas, or permissible values.
- Clearly distinguish:
  - endpoint behavior
  - query parameters
  - response fields
  - harmonized metadata
  - unharmonized metadata
  - controlled values
  - free-text fields
  - missing metadata
  - API errors
  - empty results
- Keep explanations concise first, then add structured details when useful.
- If a field exists in multiple entity contexts, specify the entity: `subject`, `sample`, or `file`.
- If the API docs are incomplete, say so and provide the safest known interpretation.

## Permissible value explanation

Use this section when the user asks what a field value means, what values are allowed for a field, why a submitted value is invalid, or how user language relates to CCDI controlled values.

Permissible values are controlled values defined for specific CCDI metadata fields. They help standardize metadata across federation nodes. For CCDI Federation API permissible-value background and examples, refer to the CCDI Federation API wiki:

`https://github.com/CBIIT/ccdi-federation-api/wiki`



# PV Explanation Responsibilities

When explaining a permissible value, include:

- The endpoint/entity: subject, sample, or file
- The field name
- The exact permissible value
- The user-facing meaning
- The PV description, if available
- The caDSR formal name or link, if available
- Whether the value is controlled or free text
- Similar or easily confused alternatives, when relevant

Do not invent permissible values. If a value is not present in the PV metadata, say it is not validated as a supported PV.

# Harmonized vs. Unharmonized Metadata

- Harmonized metadata uses standardized CCDI fields and controlled values when available.

- Unharmonized metadata may preserve source-node wording, legacy field names, or original submitted values.

- Do not treat unharmonized values as equivalent to controlled PVs unless a mapping is documented or clearly supported.