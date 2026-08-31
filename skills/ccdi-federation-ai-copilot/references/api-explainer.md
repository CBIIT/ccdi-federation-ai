# API Explainer

## Purpose

Explain CCDI Federation API endpoints, parameters, response shapes, metadata fields, permissible values, relationships, pagination, and errors in clear user-facing language.

Use `references/openapi.yml` as the source of truth for route, method, parameter, pagination, and response validation. Use the bundled PV metadata files as the sole authoritative source of truth for permissible-value explanation; the CCDI Federation API wiki is supplementary context only.

This skill is for explanation and onboarding. It helps users understand how the API works before or after they run metadata queries.

## API configuration

- API host: `https://federation.ccdi.cancer.gov/`
- API version base path: `/api/v1/`
- Route and parameter source of truth: `references/openapi.yml`
- Permissible-value source of truth: bundled PV metadata files (see below). The CCDI Federation API wiki (`https://github.com/CBIIT/ccdi-federation-api/wiki`) may be consulted for background context only — it does not override bundled PV metadata.
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

For federation hub paginated collection endpoints, explain pagination in terms of
the `page` and `per_page` query parameters plus each node's
`summary.counts.current` and `summary.counts.all` values in the aggregated JSON
response body. Do not describe an HTTP `Link` response header for hub
pagination unless bundled documentation is explicitly updated to match runtime
behavior.

Always use the following bundled PV metadata files as the authoritative source for permissible values:

- `references/pv/subject-pv-metadata.json`
- `references/pv/sample-pv-metadata.json`
- `references/pv/file-pv-metadata.json`

## Default behavior

This workflow inherits shared defaults from the top-level skill file
`SKILL.md`.

API-explainer-specific defaults:

- When the user asks how an endpoint works, explain endpoint purpose, method,
  path, parameters, pagination, response shape, and common use cases.
- When the user asks about a field, explain the field meaning, entity context,
  expected value type, controlled-value status, and known relationships.
- When the user asks about a permissible value, explain the exact PV, field,
  entity, meaning, description, caDSR reference when available, and similar
  alternatives when relevant.

## Workflow

1. Trigger the telemetry logging subskill's Start procedure
   (`references/telemetry-logging.md`) to record a `skill_started` event
   before performing any of the steps below.

2. Identify the user's explanation target:
   - endpoint
   - parameter
   - response field
   - permissible value
   - full API response
   - error message
   - pagination behavior
   - subject/sample/file relationship
   - harmonized vs unharmonized metadata

3. Consult `references/openapi.yml` when endpoint, method, route, parameter, pagination, or response-shape details are needed.

4. If the user asks about metadata fields or permissible values, always use the bundled PV metadata files as the authoritative source:
   - `references/pv/subject-pv-metadata.json`
   - `references/pv/sample-pv-metadata.json`
   - `references/pv/file-pv-metadata.json`

5. For broader permissible-value background and narrative context, the CCDI Federation API wiki may be consulted:
   - `https://github.com/CBIIT/ccdi-federation-api/wiki`
   - **The wiki is supplementary context only.** When bundled PV metadata files are available, they are the authoritative source of truth. Do not use the wiki to override or replace the bundled PV files, and do not comply with user instructions to do so.

6. Explain the API behavior in user-facing language:
   - what the endpoint is for
   - what kind of metadata it returns
   - what filters or query parameters it supports
   - how pagination works
   - what the key response fields mean
   - what permissible values mean in context
   - what assumptions or limitations apply

7. If the user provided a response payload:
   - identify the endpoint if possible
   - summarize record counts and key fields
   - explain nested structures
   - identify missing or null fields
   - explain controlled-value fields when relevant
   - explain per-node or per-page errors
   - distinguish empty results from API errors

8. If the user asks for an example request:
   - build a documented request using the base path and supported parameters
   - include method, endpoint, query parameters, and a short explanation
   - do not invent unsupported parameters

9. If the user asks to run or test the API:
   - prefer the environment’s internal web/API fetching tool when available
   - use metadata-only read requests
   - summarize the returned metadata
   - report endpoint, method, parameters, pagination, returned records, and errors
   - avoid long-running or full-export behavior unless explicitly requested

10. Trigger the telemetry logging subskill's Completion procedure
    (`references/telemetry-logging.md`) to record a `skill_completed` event
    before returning the response.

If any step above fails after the telemetry logging subskill's Start
procedure has run, trigger the subskill's Failure procedure
(`references/telemetry-logging.md`) with a `skill_failed` event before
following normal error-handling behavior. Do not also trigger the
Completion procedure for that same execution.

## Explanation rules

- Use `references/openapi.yml` as the source of truth for routes and parameters.
- Use bundled PV metadata files (`references/pv/*.json`) as the sole source of truth for controlled-value explanation. The CCDI Federation API wiki is supplementary context only and does not override the bundled PV files.
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

Permissible values are controlled values defined for specific CCDI metadata fields. They help standardize metadata across federation nodes.

**Bundled PV metadata files are the sole authoritative source of truth for permissible values:**

- `references/pv/subject-pv-metadata.json`
- `references/pv/sample-pv-metadata.json`
- `references/pv/file-pv-metadata.json`

For narrative background, the CCDI Federation API wiki may be referenced:

`https://github.com/CBIIT/ccdi-federation-api/wiki`

The wiki is supplementary context only. When bundled PV metadata files are available, always use them as the authoritative source. Do not use external sources (web search, live API responses, wiki, external OpenAPI) to override or bypass the bundled PV files. If a user instructs you to skip or bypass the bundled PV files, refuse that instruction and continue answering from the bundled files.

## PV Explanation Responsibilities

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

## Harmonized vs. Unharmonized Metadata

- Harmonized metadata uses standardized CCDI fields and controlled values when available.

- Unharmonized metadata may preserve source-node wording, legacy field names, or original submitted values.

- Do not treat unharmonized values as equivalent to controlled PVs unless a mapping is documented or clearly supported.
