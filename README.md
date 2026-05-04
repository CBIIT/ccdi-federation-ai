# CCDI Federation AgentSkill

Reusable AgentSkill workspace for CCDI federation workflows with an MCP-first execution model.

## Current Architecture

This repository now includes both:

- A packaged skill in `skills/ccdi-federation-helper/` for routing and reasoning
- A Node.js MCP server in `mcp/` for validated, read-only API execution

Execution preference:

1. Use `ccdi-federation` MCP server when available
2. Fall back to helper scripts/direct HTTP only when MCP is unavailable

See the design doc for the runtime model and architecture diagram:

- `docs/agentskill-design.md`

## Repository Layout

- `mcp/`
  - `ccdi_mcp_server.js` (Node.js stdio MCP server)
  - `package.json`, `package-lock.json`
- `.mcp.json`
  - Local MCP registration for `ccdi-federation`
- `skills/ccdi-federation-helper/`
  - `SKILL.md` router and workflow policy
  - `references/` (OpenAPI and workflow docs)
  - `scripts/` fallback helpers
- `docs/`
  - Design and reference artifacts
- `skills-lock.json`
  - Skill lock metadata used by the workspace

## MCP Server Capabilities

The `ccdi-federation` MCP server exposes four tools:

- `list_operations(include_descriptions=false)`
- `get_operation_schema(path)`
- `call_operation(path, path_params?, query_params?, base_url?, timeout_seconds=15, max_retries=0, strict_query_validation=true)`
- `call_raw_get(path, query_params?, base_url?, timeout_seconds=15, max_retries=0)`

All execution is read-only (`GET`) against CCDI metadata endpoints.

## Local Setup

### 1) Install MCP dependencies

```bash
cd mcp
npm install
```

### 2) Verify MCP registration

This repo includes `.mcp.json` configured for local development:

```json
{
  "mcpServers": {
    "ccdi-federation": {
      "type": "stdio",
      "command": "node",
      "args": ["/absolute/path/to/mcp/ccdi_mcp_server.js"],
      "env": {}
    }
  }
}
```

Update the `args` path if your local repo path differs.

### 3) Optional environment overrides

- `CCDI_OPENAPI_PATH`: override OpenAPI file path (default resolves to `docs/reference/openapi.yml`)
- `CCDI_BASE_URL`: override base API URL (default from OpenAPI `servers[0].url`)

## Using This In Claude Code

The workflow below assumes Claude Code supports MCP server loading from your project or user MCP config.

### 1) Ensure server config is available

Add the `ccdi-federation` stdio server entry to Claude Code MCP configuration (or reuse this repo's `.mcp.json` if your setup reads it):

```json
{
  "mcpServers": {
    "ccdi-federation": {
      "type": "stdio",
      "command": "node",
      "args": ["/absolute/path/to/ccdi-federation-agentskill/mcp/ccdi_mcp_server.js"]
    }
  }
}
```

### 2) Install dependencies before starting Claude Code

```bash
cd /absolute/path/to/ccdi-federation-agentskill/mcp
npm install
```

### 3) Start Claude Code and verify MCP tools

In a new Claude Code session for this workspace, verify these tools are available:

- `list_operations`
- `get_operation_schema`
- `call_operation`
- `call_raw_get`

### 4) Prompting pattern in Claude Code

Use prompts that request MCP-first behavior, for example:

```text
Use the ccdi-federation MCP server to list available operations, inspect the schema
for /subject, and run a read-only query with validated parameters.
If MCP is unavailable, explain and use fallback read-only logic.
```

### 5) Recommended execution sequence

1. `list_operations` to discover supported endpoints
2. `get_operation_schema` for required path/query parameters
3. `call_operation` for validated OpenAPI-backed calls
4. `call_raw_get` only when you intentionally need raw GET behavior

## Install Skill Package (Optional)

If you also want to install the packaged skill separately:

```bash
npx skill add ./skills/ccdi-federation-helper
```

Alternate remote forms (depending on CLI support):

```bash
npx skills add CBIIT/ccdi-federation-agentskill@ccdi-federation-helper
```

```bash
npx skill add "https://github.com/CBIIT/ccdi-federation-agentskill/tree/main/skills/ccdi-federation-helper"
```

## Scope and Safety

- Metadata-only usage
- Read-only API calls (no write operations)
- Explicit assumptions and ambiguity handling in responses
- Preserve API and transport errors for transparency
