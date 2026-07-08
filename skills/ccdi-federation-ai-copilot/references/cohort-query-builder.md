# Cohort Query Builder

## Purpose

Turn a natural-language cohort question into a metadata-only CCDI Federation cohort query, validate the route and supported parameters against `references/openapi.yml`, execute the live metadata API only when explicitly requested, summarize the fetched response, and report the API endpoint and parameters used. Keep semantic permissible-value mapping inside this workflow as a required normalization phase when the request involves controlled values.

## API configuration

- API base URL: `https://federation-stage.ccdi.cancer.gov/api/v1/`
- API route and parameter source of truth: `references/openapi.yml`
- Live execution: use the environment's web/API fetching capability for read-only GET calls.
- **Request metadata** — append these query parameters to every live API request:
  - `request_source=agent_skill` — always include; identifies requests originating from this skill for attribution and analytics.
  - `summarized_query=<sanitized_summary>` — include a short, high-level, sanitized description of the user's intent (see [Summarized query rules](#summarized-query-rules) below).
- Use `references/openapi.yml` to confirm:
  - available endpoints
  - supported HTTP methods
  - supported query parameters
  - pagination parameter names
  - documented page-size limits
  - response shape when available
- use the following metadata files as the source of truth for semantic PV mapping and normalization:
  - file endpoints' supported permissible-values reference: `references/pv/file-pv-metadata.json`
  - sample endpoints' supported permissible-values reference: `references/pv/sample-pv-metadata.json`
  - subject endpoints' supported permissible-values reference: `references/pv/subject-pv-metadata.json`

## Default behavior

This workflow inherits shared defaults from the top-level skill file
`SKILL.md`.

Cohort-query-builder-specific defaults:

- Default to building and validating a metadata-only cohort query plan.
- Use 10 results per page unless `references/openapi.yml` documents a different limit.
- Default max pages: 3 unless the user requests more.
- Stop pagination on empty page, fewer-than-page-size page, no next page/token, repeated token, API error, user limit, or max-page cap.

## Workflow

1. Interpret the user's cohort question.
2. Identify relevant CCDI entity or endpoint: `subject`, `sample`, `file`, or cross-entity.
3. Extract user-facing cohort terms.
4. Run semantic PV mapping when controlled-value normalization is needed, specifically for the file, sample, and subject endpoints.
   - Use the PV metadata files directly when they are available in context.
5. Build the cohort API plan, including endpoint, method, normalized filters, and pagination settings.
6. Validate the route, endpoint, HTTP method, supported parameters, and pagination settings against `references/openapi.yml`.
7. Execute the live metadata API call when endpoint and parameter details are sufficient:

- Use the environment's web/API fetching capability for metadata-only GET requests.
- Use metadata-only `GET` requests unless `openapi.yml` documents another read-only metadata method.
- Append `request_source=agent_skill` to every request.
- Append `summarized_query=<sanitized_summary>` to every request; derive the value from the user's cohort intent following the rules in [Summarized query rules](#summarized-query-rules).
- Request 10 results per page unless `openapi.yml` documents a smaller maximum.
- Default max pages: 3 unless the user explicitly asks for more.
  - Stop pagination when:
    - the response has no records,
    - the response has fewer than the requested page size,
    - the API returns no next page or next token,
    - a page token repeats,
    - an API error occurs,
    - the user-requested limit is reached,
    - or the max-page safety cap is reached.
- Preserve page-level, node-level, and API-level errors.
- If the API call cannot be executed due to missing or unsupported endpoint or parameter information, return the planned API call and clearly indicate what is missing instead of inventing details.
- If fetching exceeds the default page cap or becomes slow, stop with partial results and explain what was fetched.

1. Summarize the fetched metadata before responding.
2. Return the cohort interpretation, semantic PV mappings, API used, parameters used, summary of fetched data, assumptions, ambiguities, errors, and limitations.

Do not return the full raw API payload by default. Provide a concise summary, with a small representative sample only if useful.

## Ambiguity handling

If a user term could map to several PVs, show alternatives rather than guessing silently. For example, "glioma" can map to multiple diagnosis-category PVs, including Low-Grade Gliomas, High-Grade Glioma, Other Gliomas, and Other Brain Tumors depending on context.

If the API route or parameter surface cannot be validated, do not execute a guessed API call. Return the planned call and the missing route or parameter information.

## Semantic PV mapping flow

```text
user term
  -> candidate fields/PVs from PV metadata files
  -> LLM semantic selection from valid candidates
  -> OpenAPI route and parameter validation
  -> API query filters
  -> live metadata API execution
  -> summarized response
```

### Semantic PV mapping  Examples

- "female subjects" -> subject.sex = F
- "RNA sequencing" -> sample.library_strategy = RNA-Seq
- "relapsed disease" -> sample.disease_phase = Relapse
- "tumor samples" -> sample.tissue_type = Tumor
- "variant files" -> file.type = VCF, if the user means variant call files

## Summarized query rules

Every live API request must include `summarized_query` as a short, sanitized, entity- and filter-focused description of the user's intent.  The value is used for analytics and usage tracking.

### What to include

- Entity type (subject, sample, or file).
- Key clinical or metadata filters (e.g. diagnosis, sex, disease phase, library strategy, file type).
- Pagination intent when relevant (e.g. "first page" vs "all pages").

### What to exclude

- Patient names, participant IDs, study IDs, or any personally identifiable information (PII).
- Verbatim user messages or chat history.
- Free-text fields that may contain sensitive data.
- Internal tool names, session IDs, or implementation details.

### Format

Produce a plain-English phrase of no more than 100 characters.  Do not JSON-encode or URL-encode the value; the client library handles encoding.

### Examples

| User intent | summarized_query value |
| --- | --- |
| "Show me female subjects with osteosarcoma" | `female subjects with osteosarcoma` |
| "Find RNA-seq samples from tumor tissue" | `RNA-seq samples tumor tissue` |
| "List VCF files for pediatric patients in relapse" | `VCF files pediatric relapse` |
| "How many subjects have neuroblastoma?" | `subjects with neuroblastoma count` |
| "Get all samples from study XYZ-001" | `samples by study` |

> **Note:** If the user's request cannot be summarized without including PII or sensitive details, omit `summarized_query` from the request rather than risk exposing sensitive data.

### When using `scripts/ccdi_client.py`

Pass the sanitized summary as the `summarized_query` keyword argument to `read_only_get`:

```python
read_only_get(
    base_url,
    path,
    params=filters,
    summarized_query='female subjects with osteosarcoma',
)
```

The function automatically appends both `request_source=agent_skill` and `summarized_query=<value>` to the outgoing URL.
