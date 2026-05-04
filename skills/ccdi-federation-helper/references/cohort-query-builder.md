---
name: cohort-query-builder
description: build and execute metadata-only ccdi federation cohort queries from natural-language cohort requests. use this skill when the user asks to find, define, review, run, or plan a cohort query; map cohort terms to ccdi fields or permissible values; normalize terms like rna sequencing, female, relapse, tumor samples, or vcf files into valid subject, sample, or file metadata filters; fetch cohort metadata from the api; summarize returned metadata; or explain what api endpoint and parameters were used. includes semantic permissible-value mapping inside the cohort query builder workflow, uses openapi.yml for route and parameter validation, and uses 100 results per page for live metadata api execution.
---

# Cohort Query Builder

## Purpose

Turn a natural-language cohort question into a metadata-only CCDI Federation cohort query, validate the route and supported parameters against `references/openapi.yml`, execute the live metadata API when enough API information is available, summarize the fetched response, and report the API endpoint and parameters used. Keep semantic permissible-value mapping inside this workflow as a required normalization phase when the request involves controlled values.

## API configuration

- API base URL: `https://federation.ccdi.cancer.gov/api/v1/`
- API route and parameter source of truth: `references/openapi.yml`
- Preferred live execution path: the MCP server named `ccdi-federation` when it is available in the environment.
- Local MCP availability check:
  - First check whether an MCP server named `ccdi-federation` is already available in the active tool environment.
  - In this repository, a local MCP registration is also defined in `.mcp.json` under `mcpServers.ccdi-federation`.
  - That server is implemented by `mcp/ccdi_mcp_server.js` and exposes read-only GET helpers over the CCDI Federation OpenAPI spec.
- MCP tools exposed by `ccdi-federation`:
  - `list_operations`: enumerate available GET endpoints extracted from `openapi.yml`
  - `get_operation_schema`: inspect required and optional parameters for a specific API path
  - `call_operation`: execute a validated OpenAPI-backed GET call by API path
  - `call_raw_get`: execute a raw GET against the configured base URL when a validated path-based call is not sufficient
- Use `openapi.yml` to confirm:
  - available endpoints
  - supported HTTP methods
  - supported query parameters
  - pagination parameter names
  - documented page-size limits
  - response shape when available
- use the following metadata files as the source of truth for semantic PV mapping and normalization:
  - file endpoints' supported permissible-values reference to `references/pv/file-pv-metadata.json`
  - sample endpoints' supported permissible-values reference to `references/pv/sample-pv-metadata.json`
  - subject endpoints' supported permissible-values reference to `references/pv/subject-pv-metadata.json`

## Default behavior

- Default to building and validating a metadata-only cohort query plan.
- Execute the live CCDI Federation metadata API only when the user explicitly asks to run, fetch, retrieve, or summarize API results.
- Prefer the `ccdi-federation` MCP server for live API calls when it is available.
- If `ccdi-federation` is available:
  - use `list_operations` to discover valid GET routes when needed
  - use `get_operation_schema` to confirm required path and query parameters for the target route
  - use `call_operation` for normal validated metadata fetches by path
  - use `call_raw_get` only as a fallback for read-only GET requests that still need custom handling after route validation
- If `ccdi-federation` is not available, fall back to the environment’s internal web/API fetching tool.
- Use bundled Python scripts only as optional helpers for deterministic PV lookup/validation or as fallback execution tools when no internal API tool is available.
- Do not run Python for every semantic PV mapping step when the relevant PV metadata is already available.
- Keep execution metadata-only.
- Use 10 results per page unless `openapi.yml` documents a different limit.
- Default max pages: 3 unless the user requests more.
- Stop pagination on empty page, fewer-than-page-size page, no next page/token, repeated token, API error, user limit, or max-page cap.
- Summarize fetched API data before responding; do not dump raw full responses unless the user asks.

## Workflow


1. Interpret the user's cohort question.
2. Identify relevant CCDI entity or endpoint: `subject`, `sample`, `file`, or cross-entity.
3. Extract user-facing cohort terms.
4. Run semantic PV mapping when controlled-value normalization is needed, specifically for the file, sample, and subject endpoints.
   - Use the PV metadata files directly when they are available in context.
   - Use `pv_mapper.py` only as an optional helper for deterministic candidate lookup or validation when needed.
   - Do not run Python for every mapping step if the relevant PV metadata is already available.
      - Use `pv_mapper.get_controlled_fields(endpoint_type)` to retrieve candidate controlled fields from metadata files.
        - Supported endpoint types: `'file'`, `'sample'`, `'subject'`
        - Returns list of fields with defined permissible values
      - Use `pv_mapper.get_permissible_values(endpoint_type, field)` to retrieve candidate permissible values for a specific field.
        - Returns list of valid values or `None` if field has no controlled values
      - Use LLM semantic reasoning to select the best valid candidate from the retrieved PVs.
      - Use `pv_mapper.field_value_pair_exists(endpoint_type, field, value)` to confirm selected field/value pairs exist in the source metadata.
        - Returns `True` if the field/value pair is valid, `False` otherwise
      - Optionally use `pv_mapper.get_field_metadata(endpoint_type, field)` to access complete field metadata including formal name, caDSR link, and descriptions.
5. Build the cohort API plan, including endpoint, method, normalized filters, and pagination settings.
6. Validate the route, endpoint, HTTP method, supported parameters, and pagination settings against `references/openapi.yml`.
7. Execute the live metadata API call when endpoint and parameter details are sufficient:
  - First check whether the MCP server named `ccdi-federation` is available.
  - If `ccdi-federation` is available, fetch through that MCP server instead of making a direct HTTP call.
    - Use `list_operations` if the correct path still needs to be identified.
    - Use `get_operation_schema` with the selected API path before execution when parameter requirements are unclear.
    - Use `call_operation` with:
      - `path`: the validated OpenAPI path such as `/subject`, `/sample`, or `/file`
      - `path_params`: only when the selected path template includes required path placeholders
      - `query_params`: the normalized cohort filters and pagination parameters
      - `base_url`: optional override only when the user explicitly needs a non-default CCDI base URL
      - `timeout_seconds`, `max_retries`, and `strict_query_validation` as needed
    - Use `call_raw_get` only when a read-only GET call still cannot be expressed cleanly through `call_operation` after OpenAPI validation.
  - If `ccdi-federation` is not available, use the environment's direct web/API fetching capability as the fallback execution path.
   - Use metadata-only `GET` requests unless `openapi.yml` documents another read-only metadata method.
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
   - Avoid long-running script execution during chat.
   - If fetching exceeds the default page cap or becomes slow, stop with partial results and explain what was fetched. 
8. Summarize the fetched metadata before responding.
9. Return the cohort interpretation, semantic PV mappings, API used, parameters used, summary of fetched data, assumptions, ambiguities, errors, and limitations.

Do not return the full raw API payload by default. Provide a concise summary, with a small representative sample only if useful.


## Ambiguity handling

If a user term could map to several PVs, show alternatives rather than guessing silently. For example, "glioma" can map to multiple diagnosis-category PVs, including Low-Grade Gliomas, High-Grade Glioma, Other Gliomas, and Other Brain Tumors depending on context.

If the API route or parameter surface cannot be validated, do not execute a guessed API call. Return the planned call and the missing route or parameter information.

## Semantic PV mapping flow
```text
user term
  -> candidate fields/PVs from pv_mapper.py
  -> LLM semantic selection from valid candidates
  -> script validation of selected PVs
  -> OpenAPI route and parameter validation
  -> API query filters
  -> live metadata API execution
  -> summarized response
```

###  Semantic PV mapping  Examples

- "female subjects" -> subject.sex = F
- "RNA sequencing" -> sample.library_strategy = RNA-Seq
- "relapsed disease" -> sample.disease_phase = Relapse
- "tumor samples" -> sample.tissue_type = Tumor
- "variant files" -> file.type = VCF, if the user means variant call files
The intended mapping flow is:
