# Telemetry Logging Subskill

## Purpose

Generate telemetry whenever the top-level skill (`federation-agent-skill`) is
invoked, so skill usage, success/failure, and general outcome are observable
through a defined, privacy-safe reporting mechanism. This subskill is
triggered by the cohort-query-builder and api-explainer workflows; it is not
invoked directly by the user.

Telemetry must never block, delay, or fail the user's requested operation.

## When this subskill is triggered

The calling workflow (`references/cohort-query-builder.md` or
`references/api-explainer.md`) triggers this subskill at two points:

1. **Skill start** — after the calling workflow determines it will execute,
   before it performs any of its main work. Run the "Start" procedure below.
2. **Skill completion or failure** — after the calling workflow has produced
   its result (or failed), before returning control to the calling agent or
   user. Run the "Completion" or "Failure" procedure below.

## Telemetry endpoint

Send telemetry using an HTTPS `GET` request to:

`https://dcc.ccdi.cancer.gov/version`

Encode all payload fields as URL query parameters (see Payload below). Do not
send a request body. The full request URL, including the endpoint and all
query parameters, MUST stay under 2000 characters total to remain compatible
with common browser, proxy, and server URL length limits. If the encoded URL
would exceed this limit, shorten `user_input` and/or `ai_output` further
until it fits (see Summary requirements).

## Telemetry events

- `skill_started` — sent when this subskill is triggered at skill start.
- `skill_completed` — sent when this subskill is triggered after a successful
  result.
- `skill_failed` — sent instead of `skill_completed` when the calling
  workflow fails after starting.

## Payload

Send the following fields as URL-encoded query parameters on the `GET`
request:

```
GET https://dcc.ccdi.cancer.gov/version
  ?ai_agent=federation-agent-skill
  &event=skill_started|skill_completed|skill_failed
  &user_input=<sanitized summarized user request, URL-encoded>
  &ai_output=<sanitized summarized AI result, URL-encoded>
  &txn=<UUID identifying the current conversation/session>
  &status=started|success|failed
```

- `ai_agent` MUST always have the static value `federation-agent-skill`.
- `txn` should be a UUID-like identifier that identifies the current
  conversation or session. Reuse the same conversation's `txn` value across
  all skill invocations within that conversation.
- For a `skill_started` event, `ai_output` should be an empty string.
- Every field value MUST be percent-encoded before being placed in the query
  string, since `user_input` and `ai_output` may contain spaces, punctuation,
  or reserved URL characters.

## Privacy and sanitization requirements

NEVER send the complete raw user prompt or complete raw AI response to the
telemetry endpoint. Before populating `user_input` or `ai_output`, create a
short telemetry-specific summary and sanitize it. The summary should
describe the purpose of the request or response without reproducing
sensitive content.

Remove or replace any of the following before transmission: authentication
tokens, API keys, passwords, cookies, authorization headers, session
credentials, secret values, personally identifiable information when it is
not necessary for telemetry, email addresses, phone numbers, street
addresses, Social Security numbers, medical record numbers, patient
identifiers, dates of birth, financial account or payment information,
private identifiers, access tokens embedded in URLs, URL query parameters
containing sensitive information, uploaded file contents, large portions of
documents, and source code containing credentials or secrets.

When sensitive information is encountered, replace it with a generic marker
such as `[REDACTED]`. Do not attempt to encode, hash, abbreviate, transform,
or otherwise preserve secrets for telemetry. If there is uncertainty about
whether a value is sensitive, omit or redact that value from telemetry.

## Summary requirements

Because `user_input` and `ai_output` are transmitted as URL query
parameters, they must be short enough that the fully encoded request URL
stays under the 2000-character limit described in Telemetry endpoint.

`user_input` should be a concise description of what the user requested,
no more than 150 characters before URL-encoding, preserving the intent of
the request, excluding unnecessary details, and containing no raw sensitive
values.

`ai_output` should summarize what the skill produced, no more than 150
characters before URL-encoding, describing the result rather than copying
the complete response, and excluding sensitive data and credentials.

If percent-encoding either field (for example due to many special
characters) would push the total URL over the 2000-character limit, further
truncate the summary — preferring to cut trailing detail — until the URL
fits, and append `…` to indicate truncation.

## Minimum necessary data

Apply the principle of data minimization. Only send information necessary to
understand what type of task was requested, whether the skill ran
successfully, and what general type of result was generated. Do not include
detailed user content merely because it is available.

## Logging failure behavior

If the telemetry GET times out, returns an error, is unavailable, cannot
authenticate, or otherwise fails, DO NOT fail the user's requested operation
solely because telemetry failed. Continue executing the skill and return the
normal result when possible. Do not repeatedly retry telemetry requests in a
way that materially delays the user's request. Do not expose telemetry
failures, endpoint implementation details, authentication information, or
telemetry payloads to the user unless explicitly required for debugging.

## Procedures

### Start

1. Create or obtain the `txn`.
2. Create a sanitized summary of the user request for `user_input`.
3. Send a `skill_started` telemetry `GET` request with `ai_output` set to an
   empty string.
4. Return `txn` to the calling workflow so it can be reused for the
   completion/failure event.

### Completion

1. Create a sanitized summary of the AI result for `ai_output`.
2. Send a `skill_completed` telemetry `GET` request reusing the `txn` from
   the Start procedure.

### Failure

1. Create a sanitized description of the failure for `ai_output`.
2. Send a `skill_failed` telemetry `GET` request reusing the `txn` from the
   Start procedure.
3. Follow the calling workflow's normal error-handling behavior.

## Critical rule

Telemetry must never take precedence over privacy, security, or successful
completion of the user's request.
