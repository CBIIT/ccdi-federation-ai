# CCDI Federation MCP server design

- **Status:** MCP server implemented under `mcp/`; public deployment still requires a DNS name, TLS gateway, and distributed traffic controls.
- **Source skill:** `skills/ccdi-federation-ai-copilot/`, version `1.0.1`
- **Scope:** Remote, public, read-only metadata MCP server. Client implementation is out of scope.
- **Transport:** Streamable HTTP over HTTPS at `/mcp`.
- **Authentication:** None.

## 1. Source analysis and responsibility split

The agent skill provides natural-language cohort planning, API explanation,
OpenAPI-based request checks, optional live metadata requests, and exact
permissible-value (PV) reference data. Its bundled OpenAPI describes 23 GET
operations. The PV JSON files cover fields for `subject`, `sample`, and `file`
only. The `mcp/` directory now contains the Python server package and tests. The older
`docs/agentskill-design.md` describes an MCP implementation that is not present
in this checkout, so it is historical context rather than an implementation
source.

| Asset | Server use |
| --- | --- |
| `references/openapi.yml` | Authority for GET routes, operation IDs, path and query parameters, and documented responses. |
| `references/pv/subject-pv-metadata.json` | Exact subject PVs and field metadata. |
| `references/pv/sample-pv-metadata.json` | Exact sample PVs and field metadata. |
| `references/pv/file-pv-metadata.json` | Exact file PVs and field metadata. |
| `scripts/pv_mapper.py` | Candidate logic for loading bundled PVs; server behavior must remain exact-value listing. |
| `scripts/ccdi_client.py` | Candidate fixed-host GET logic; the server still needs OpenAPI-derived validation and response limits. |

The MCP server supplies deterministic reference and execution tools. The agent
skill or MCP host interprets natural language, decides when to call a live
tool, handles clarification, plans multi-operation or multi-page workflows,
and presents results to the user. `plan_cohort` and `explain_api` remain at the
agent skill level. The server registers neither as a tool or prompt, and it
does not expose their workflow documents as resources.

## 2. Remote architecture

The public endpoint is an unauthenticated Streamable HTTP service behind a TLS
gateway. The gateway assigns the deployment hostname, terminates HTTPS,
validates allowed browser origins, caps inbound request size, and enforces
distributed traffic limits. Backend instances remain private and stateless.
The server makes outbound requests only to the fixed CCDI Federation API origin
`https://federation.ccdi.cancer.gov/api/v1`. It accepts no caller-supplied
base URL, host, port, or arbitrary HTTP target.

The server packages the checked-in OpenAPI and PV files as read-only,
versioned assets. It fails startup if they are missing or malformed. It never
replaces bundled PVs with wiki content, a live API response, web search, or an
external OpenAPI document. Asset hashes and OpenAPI version appear in service
diagnostics and tool provenance so a deployed version can be identified.

No OAuth, login, API key, bearer token, per-user scope, or client
registration is required. With no caller identity, network controls must use
the source IP observed at the trusted gateway and a global request budget.
The backend must not trust arbitrary forwarding headers from callers.

## 3. MCP tools and resources

The server exposes six tools. The first five require no CCDI API request.

| Tool | Input | Output and rule |
| --- | --- | --- |
| `list_operations` | Optional `entity` and `kind` | Bounded operation IDs, GET paths, descriptions, and pagination status from the bundled OpenAPI. |
| `describe_operation` | `operation_id` | Exact method, route, path/query parameters, required fields, documented responses, and pagination rules. |
| `get_field_metadata` | `entity`, `field` | Bundled formal name, description, caDSR link, controlled status, and PV count. An unknown field and a field with no PV list are distinct states. |
| `list_permissible_values` | `entity`, optional `field`, `offset`, `limit` | Exact field-labelled bundled PV entries with `total` and `next_offset`. No user-term lookup or inferred mapping. |
| `validate_query` | `operation_id`, `path_params`, `query_params` | Valid/executable status, normalized GET request or specific validation errors, warnings, and source provenance. No network call. |
| `query_metadata` | Same query arguments | Revalidates, makes one bounded API GET, and returns the full parsed upstream JSON payload with HTTP status and provenance. |

`list_permissible_values` accepts only `subject`, `sample`, or `file`.
Omitting `field` enumerates all controlled fields for that entity in stable
field-name order, preserving each field's bundled PV order. Pagination must
allow the entire exact list to be retrieved. A field with
`permissible_values: null` is reported as having no bundled PV list. The
server cannot provide a bundled PV for an arbitrary unmatched user term. It
does not claim that a guessed synonym is a validated PV. Whether to show the
exact list, infer a semantic mapping from its values and descriptions, or ask
the user to choose belongs to the agent skill or host.

The server may expose an immutable operation-index resource at
`ccdi://reference/operations` and a field-scoped PV resource template at
`ccdi://reference/pv/{entity}/{field}`. Targeted tools remain the primary
interface because clients may not surface resources. Raw OpenAPI and complete
PV bundles need not be placed in model context by default.

The service returns machine-readable structured content. In particular,
`query_metadata` carries its potentially large API payload once, without a
duplicate text copy. The server generates no summary and selects no example
records. Count and summary API operations, when documented, remain ordinary
upstream routes rather than server-generated calculations.

## 4. Query validation contract

The caller supplies a documented `operation_id` and named path and query
parameters, not a URL string. The server resolves only bundled GET operations,
requires documented path parameters, rejects extra or missing parameters,
and percent-encodes validated path segments. It rejects slash injection,
encoded traversal, query fragments in path segments, unknown query keys, and
wrong parameter types.

The symbolic `metadata.unharmonized.<field>` OpenAPI parameter is permitted
only on operations that document it, with a concrete nonempty field suffix.
The literal placeholder is never sent upstream. Experimental `search` is
accepted only on the diagnosis routes that document it. Bundled PV presence
does not make a field a valid API filter; the OpenAPI parameter list controls
filter availability. Count-route `{field}` values should be constrained to
fields established by bundled metadata. An unsupported field is reported as
a validation gap rather than guessed.

**Filter values pass through exactly as supplied.** The MCP server does not
reject, rewrite, or prevalidate them against the PV bundle. The CCDI
Federation API owns exact matching and upstream error behavior. The PV listing
tool is informational and independent of query execution. The agent skill may
use that listing to infer a mapping to an exact bundled value or help a user
choose one, but the MCP server does not perform semantic mapping or user-facing
clarification.

`validate_query` makes no network call. `query_metadata` performs the same
validation again on every invocation; a prior validation result cannot bypass
it. Unsupported routes or parameters fail before any upstream request.

## 5. Live execution and response limits

Each `query_metadata` invocation fetches one API response. For paginated
operations, default to `page=1` and `per_page=20`. Require positive integers;
reject `per_page>200` instead of clamping it. The server never loops through
pages. Multi-page decisions remain with the agent skill or host.

| Control | Requirement |
| --- | --- |
| Upstream execution timeout | 10 minutes for the call, including any retry. |
| Upstream decoded response body | Maximum 24,000,000 bytes (24 MB); reject rather than truncate. |
| Retry | At most one bounded backoff retry for an upstream 429 or 5xx GET response. |
| Redirects | Do not follow them. |
| Network concurrency | Enforce a global upstream budget and per-source-IP limits at the gateway; at most two concurrent upstream requests per source IP. |

The result contains only the validated request, HTTP status, complete parsed
JSON payload, and source provenance. Federated node-level errors inside an
HTTP 200 payload remain intact. Non-2xx upstream JSON errors retain their
status and payload with an MCP tool error flag. Timeout, invalid JSON,
oversized response, and transport failures return explicit error codes and
must not invent a CCDI payload. The server does not extract records, calculate
counts, choose examples, or write a narrative summary.

The host or skill should make a live call only when the user asks to run,
fetch, test, inspect, or summarize live metadata. A public MCP server cannot
verify the original user request, so its enforceable boundary is one bounded,
metadata-only GET per tool call. It must expose no raw-file download, data
transfer, manifest export, arbitrary URL fetch, or filesystem-write tool.

## 6. Security and deployment requirements

- Validate `Origin` when present and reject disallowed browser origins. Allow
  standard non-browser requests without an `Origin` header. Match CORS policy
  to the allowed browser origins.
- Validate MCP protocol/method headers and JSON-RPC body consistency, and cap
  inbound request size before parsing.
- Keep backend instances unreachable from the public internet except through
  the gateway. Apply distributed rate and in-flight limits by source IP plus
  a global upstream budget. Return 429 with `Retry-After` when overloaded.
- Set gateway timeouts above the 10-minute upstream limit. Support request
  cancellation so abandoned calls stop upstream work.
- Do not cache live query results across callers. Cache only immutable bundled
  catalog/PV data by asset hash. Avoid logging full filters and payloads.
- Restrict outbound network access to the approved CCDI API host and necessary
  deployment infrastructure. Use fixed HTTPS, no redirects, and no ambient
  caller credentials.
- Deploy versioned immutable artifacts. Review OpenAPI/PV diffs and rerun
  contract tests before updating bundled assets.

## 7. Server implementation and acceptance

The Python server package under `mcp/` uses MCP Python SDK `2.3.0` and
separates OpenAPI/PV loading (`catalog.py`), query validation
(`validation.py`), upstream GET execution (`upstream.py`), and MCP transport
registration (`server.py`). The Dockerfile copies the checked-in reference
assets into the service image. The server exposes `/healthz` and `/readyz`,
configurable host and origin allowlists, a 65,536-byte MCP request-body cap,
and a 16-request per-process upstream concurrency budget. The deployment
gateway remains responsible for public TLS, distributed traffic controls,
and outbound egress policy. No MCP client code is included. The agent skill
now routes live metadata fetches to `query_metadata` by default when the
server is connected.

The server unit tests verify all 23 operation IDs, parameter registration,
exact paged enumeration of the three PV bundles, unsupported entities,
unknown fields versus fields without PVs, absence of semantic mapping,
and preservation of unmatched filter values during query validation. They
also verify route injection rejection, documented unharmonized filters,
pagination defaults and bounds, one-page execution, complete node-level
payload preservation, upstream errors, redirects, timeout, invalid JSON,
response-size rejection, and no generated summaries or examples. Tests also
exercise MCP tool discovery and origin rejection through the ASGI app.
Deployment tests still need to verify public unauthenticated discovery over HTTPS, origin
rejection, quotas across replicas, cancellation, and gateway timeout behavior.

## References

- Local skill: `skills/ccdi-federation-ai-copilot/SKILL.md` and its referenced OpenAPI/PV assets.
- [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
