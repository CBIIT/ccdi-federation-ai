# CCDI OpenAPI MCP Server

This folder contains a Node.js MCP server generated from `docs/reference/openapi.yml`.

## What It Provides

- Loads CCDI OpenAPI paths and GET operation metadata.
- Exposes MCP tools for operation discovery and execution.
- Executes read-only GET requests with optional query and path parameters.
- Validates required path/query parameters before sending requests.

## Files

- `ccdi_mcp_server.js`: MCP server implementation.
- `package.json`: Node.js dependencies and run scripts.

## Setup

```bash
cd mcp
npm install
```

## Run

```bash
cd mcp
npm start
```

The server uses MCP stdio transport, so it does not listen on an HTTP port.

## Optional Environment Variables

- `CCDI_OPENAPI_PATH`: override OpenAPI path (default: `docs/reference/openapi.yml`).
- `CCDI_BASE_URL`: override API base URL (default from OpenAPI server URL).

## Exposed MCP Tools

- `list_operations(include_descriptions=False)`
- `get_operation_schema(path)`
- `call_operation(path, path_params=None, query_params=None, base_url=None, timeout_seconds=15, max_retries=0, strict_query_validation=True)`
- `call_raw_get(path, query_params=None, base_url=None, timeout_seconds=15, max_retries=0)`
