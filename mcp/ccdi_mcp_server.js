import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import yaml from "js-yaml";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dir = dirname(__filename);

function defaultOpenApiPath() {
  return process.env.CCDI_OPENAPI_PATH
    ? resolve(process.env.CCDI_OPENAPI_PATH)
    : resolve(__dir, "..", "docs", "reference", "openapi.yml");
}

function loadOpenApiSpec(specPath) {
  const raw = readFileSync(specPath, "utf-8");
  const doc = yaml.load(raw);
  if (typeof doc !== "object" || doc === null) {
    throw new Error(`OpenAPI document at ${specPath} did not parse into an object`);
  }
  return doc;
}

function defaultBaseUrl(spec) {
  if (process.env.CCDI_BASE_URL) return process.env.CCDI_BASE_URL.replace(/\/$/, "");
  const servers = spec.servers;
  if (Array.isArray(servers) && servers.length > 0) {
    const url = servers[0]?.url;
    if (typeof url === "string" && url) return url.replace(/\/$/, "");
  }
  throw new Error("No default server URL found in OpenAPI spec and CCDI_BASE_URL is not set");
}

function extractOperations(spec) {
  const result = {};
  const paths = spec.paths ?? {};

  for (const [route, routeItem] of Object.entries(paths)) {
    if (typeof routeItem !== "object" || routeItem === null) continue;

    for (const [method, operation] of Object.entries(routeItem)) {
      if (typeof operation !== "object" || operation === null) continue;
      if (method.toLowerCase() !== "get") continue;

      const operationId =
        operation.operationId ??
        `${method}_${route.replace(/^\//, "").replace(/\//g, "_")}`;

      const params = Array.isArray(operation.parameters) ? operation.parameters : [];
      const pathParams = [];
      const requiredPathParams = [];
      const queryParams = [];
      const requiredQueryParams = [];

      for (const p of params) {
        if (typeof p !== "object" || p === null) continue;
        const { name, in: location, required } = p;
        if (typeof name !== "string" || typeof location !== "string") continue;
        if (location === "path") {
          pathParams.push(name);
          if (required) requiredPathParams.push(name);
        } else if (location === "query") {
          queryParams.push(name);
          if (required) requiredQueryParams.push(name);
        }
      }

      result[operationId] = {
        operationId,
        method: method.toUpperCase(),
        path: route,
        summary: operation.summary ?? "",
        description: operation.description ?? "",
        pathParams,
        requiredPathParams,
        queryParams,
        requiredQueryParams,
      };
    }
  }

  return Object.fromEntries(Object.entries(result).sort(([a], [b]) => a.localeCompare(b)));
}

function pathParamNamesFromRoute(route) {
  return [...route.matchAll(/\{([^}]+)\}/g)].map((m) => m[1]);
}

function resolvePath(routeTemplate, pathParams) {
  const values = pathParams ?? {};
  const missing = [];
  let resolved = routeTemplate;
  for (const key of pathParamNamesFromRoute(routeTemplate)) {
    if (!(key in values)) {
      missing.push(key);
      continue;
    }
    resolved = resolved.replace(`{${key}}`, String(values[key]));
  }
  return missing.length > 0 ? { resolved: null, missing } : { resolved, missing: [] };
}

function isAllowedQueryParam(name, allowed) {
  if (allowed.includes(name)) return true;
  for (const candidate of allowed) {
    if (candidate.includes("<field>")) {
      const prefix = candidate.replace("<field>", "");
      if (name.startsWith(prefix)) return true;
    }
  }
  return false;
}

function validateQueryParams(queryParams, operation) {
  const provided = queryParams ?? {};
  const missingRequired = operation.requiredQueryParams.filter((r) => !(r in provided));
  const unknown = Object.keys(provided).filter(
    (k) => !isAllowedQueryParam(k, operation.queryParams)
  );
  return { missingRequired, unknown };
}

function buildUrl(baseUrl, path, params) {
  const route = path.startsWith("/") ? path : `/${path}`;
  const base = `${baseUrl.replace(/\/$/, "")}${route}`;
  if (!params || Object.keys(params).length === 0) return base;
  const qs = new URLSearchParams(
    Object.entries(params).flatMap(([k, v]) =>
      Array.isArray(v) ? v.map((vi) => [k, String(vi)]) : [[k, String(v)]]
    )
  ).toString();
  return `${base}?${qs}`;
}

async function httpGetJson(baseUrl, path, params, timeoutSeconds = 15) {
  const url = buildUrl(baseUrl, path, params);
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutSeconds * 1000);

  try {
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timer);
    const text = await res.text();
    let payload;
    try {
      payload = JSON.parse(text);
    } catch {
      payload = text;
    }
    const headers = Object.fromEntries(res.headers.entries());
    return {
      ok: res.ok,
      url,
      status: res.status,
      headers,
      payload,
      errors: res.ok ? [] : [`HTTP ${res.status}`],
    };
  } catch (err) {
    clearTimeout(timer);
    return { ok: false, url, status: null, headers: {}, payload: null, errors: [String(err)] };
  }
}

// ---------------------------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------------------------

const SPEC_PATH = defaultOpenApiPath();
const SPEC = loadOpenApiSpec(SPEC_PATH);
const OPERATIONS = extractOperations(SPEC);
const OPERATIONS_BY_PATH = Object.fromEntries(
  Object.values(OPERATIONS).map((op) => [op.path, op])
);
const DEFAULT_BASE_URL = defaultBaseUrl(SPEC);

// ---------------------------------------------------------------------------
// MCP Server
// ---------------------------------------------------------------------------

const server = new McpServer({
  name: "ccdi-federation-openapi",
  version: "1.0.0",
});

// list_operations ----------------------------------------------------------------
server.tool(
  "list_operations",
  "List available CCDI API GET operations extracted from the OpenAPI document.",
  { include_descriptions: z.boolean().optional().default(false) },
  async ({ include_descriptions }) => {
    const operations = Object.values(OPERATIONS).map((op) => {
      const item = {
        method: op.method,
        path: op.path,
        summary: op.summary,
        path_params: op.pathParams,
        query_params: op.queryParams,
      };
      if (include_descriptions) item.description = op.description;
      return item;
    });
    const result = {
      ok: true,
      openapi_path: SPEC_PATH,
      default_base_url: DEFAULT_BASE_URL,
      operation_count: operations.length,
      operations,
    };
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// get_operation_schema -----------------------------------------------------------
server.tool(
  "get_operation_schema",
  "Return parameter contract for a specific operation path.",
  { path: z.string() },
  async ({ path }) => {
    const op = OPERATIONS_BY_PATH[path];
    if (!op) {
      const result = {
        ok: false,
        errors: [`Unknown path: ${path}`],
        known_paths: Object.values(OPERATIONS).map((o) => o.path),
      };
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    }
    const result = {
      ok: true,
      operation: {
        method: op.method,
        path: op.path,
        summary: op.summary,
        description: op.description,
        path_params: op.pathParams,
        required_path_params: op.requiredPathParams,
        query_params: op.queryParams,
        required_query_params: op.requiredQueryParams,
      },
    };
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// call_operation -----------------------------------------------------------------
server.tool(
  "call_operation",
  "Execute a read-only GET operation by path.",
  {
    path: z.string(),
    path_params: z.record(z.unknown()).optional(),
    query_params: z.record(z.unknown()).optional(),
    base_url: z.string().optional(),
    timeout_seconds: z.number().int().positive().optional().default(15),
    max_retries: z.number().int().min(0).optional().default(0),
    strict_query_validation: z.boolean().optional().default(true),
  },
  async ({
    path,
    path_params,
    query_params,
    base_url,
    timeout_seconds,
    max_retries,
    strict_query_validation,
  }) => {
    const op = OPERATIONS_BY_PATH[path];
    if (!op) {
      const r = {
        ok: false,
        errors: [`Unknown path: ${path}`],
        known_paths: Object.values(OPERATIONS).map((o) => o.path),
      };
      return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
    }

    const { resolved, missing } = resolvePath(op.path, path_params ?? {});
    if (missing.length > 0) {
      const r = {
        ok: false,
        errors: [`Missing required path params: ${missing.join(", ")}`],
        operation_path: op.path,
        required_path_params: op.requiredPathParams,
      };
      return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
    }

    const { missingRequired, unknown } = validateQueryParams(query_params, op);
    if (missingRequired.length > 0) {
      const r = {
        ok: false,
        errors: [`Missing required query params: ${missingRequired.join(", ")}`],
        operation_path: op.path,
        required_query_params: op.requiredQueryParams,
      };
      return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
    }
    if (strict_query_validation && unknown.length > 0) {
      const r = {
        ok: false,
        errors: [`Unknown query params for path '${op.path}': ${unknown.join(", ")}`],
        allowed_query_params: op.queryParams,
      };
      return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
    }

    const requestBaseUrl = (base_url ?? DEFAULT_BASE_URL).replace(/\/$/, "");
    const attempts = (max_retries ?? 0) + 1;
    let response = {};
    for (let i = 0; i < attempts; i++) {
      response = await httpGetJson(requestBaseUrl, resolved, query_params, timeout_seconds);
      if (response.ok) break;
    }
    response.operation_path = op.path;
    response.resolved_path = resolved;
    response.base_url = requestBaseUrl;
    if (unknown.length > 0) {
      response.warnings = [
        `Ignored validation for unknown query params: ${unknown.join(", ")}`,
      ];
    }

    return { content: [{ type: "text", text: JSON.stringify(response, null, 2) }] };
  }
);

// call_raw_get -------------------------------------------------------------------
server.tool(
  "call_raw_get",
  "Execute a raw read-only GET request against the configured CCDI API base URL.",
  {
    path: z.string(),
    query_params: z.record(z.unknown()).optional(),
    base_url: z.string().optional(),
    timeout_seconds: z.number().int().positive().optional().default(15),
    max_retries: z.number().int().min(0).optional().default(0),
  },
  async ({ path, query_params, base_url, timeout_seconds, max_retries }) => {
    const requestBaseUrl = (base_url ?? DEFAULT_BASE_URL).replace(/\/$/, "");
    const attempts = (max_retries ?? 0) + 1;
    let response = {};
    for (let i = 0; i < attempts; i++) {
      response = await httpGetJson(requestBaseUrl, path, query_params, timeout_seconds);
      if (response.ok) break;
    }
    response.base_url = requestBaseUrl;
    return { content: [{ type: "text", text: JSON.stringify(response, null, 2) }] };
  }
);

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

const transport = new StdioServerTransport();
await server.connect(transport);
