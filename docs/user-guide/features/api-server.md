---
layout: docs
title: "Features_Api Server"
permalink: /docs/user-guide/features/api-server/
---

- 
- Features
- Management
- API Server

# API Server

The API server exposes hermes-agent as an OpenAI-compatible HTTP endpoint. Any frontend that speaks the OpenAI format — Open WebUI, LobeChat, LibreChat, NextChat, ChatBox, and hundreds more — can connect to hermes-agent and use it as a backend.

Your agent handles requests with its full toolset (terminal, file operations, web search, memory, skills) and returns the final response. When streaming, tool progress indicators appear inline so frontends can show what the agent is doing.

Hermes itself needs a configured provider and tool backends for the API server to be useful. ANous Portalsubscription handles both — 300+ models plus web/image/TTS/browser via the Tool Gateway. Runhermes setup --portalonce before starting the API server and frontends like Open WebUI or LobeChat get a fully tool-equipped backend.

`hermes setup --portal`

## Quick Start​

### 1. Enable the API server​

Add to~/.hermes/.env:

`~/.hermes/.env`

```
API_SERVER_ENABLED=trueAPI_SERVER_KEY=change-me-local-dev# Optional: only if a browser must call Hermes directly# API_SERVER_CORS_ORIGINS=http://localhost:3000
```

### 2. Start the gateway​

```
hermes gateway
```

You'll see:

```
[API Server] API server listening on http://127.0.0.1:8642
```

### 3. Connect a frontend​

Point any OpenAI-compatible client athttp://localhost:8642/v1:

`http://localhost:8642/v1`

```
# Test with curlcurl http://localhost:8642/v1/chat/completions \  -H "Authorization: Bearer change-me-local-dev" \  -H "Content-Type: application/json" \  -d '{"model": "hermes-agent", "messages": [{"role": "user", "content": "Hello!"}]}'
```

Or connect Open WebUI, LobeChat, or any other frontend — see theOpen WebUI integration guidefor step-by-step instructions.

## Endpoints​

### POST /v1/chat/completions​

Standard OpenAI Chat Completions format. Stateless — the full conversation is included in each request via themessagesarray.

`messages`

Request:

```
{  "model": "hermes-agent",  "messages": [    {"role": "system", "content": "You are a Python expert."},    {"role": "user", "content": "Write a fibonacci function"}  ],  "stream": false}
```

Response:

```
{  "id": "chatcmpl-abc123",  "object": "chat.completion",  "created": 1710000000,  "model": "hermes-agent",  "choices": [{    "index": 0,    "message": {"role": "assistant", "content": "Here's a fibonacci function..."},    "finish_reason": "stop"  }],  "usage": {"prompt_tokens": 50, "completion_tokens": 200, "total_tokens": 250}}
```

Inline image input:user messages may sendcontentas an array oftextandimage_urlparts. Both remotehttp(s)URLs anddata:image/...URLs are supported:

`content`
`text`
`image_url`
`http(s)`
`data:image/...`

```
{  "model": "hermes-agent",  "messages": [    {      "role": "user",      "content": [        {"type": "text", "text": "What is in this image?"},        {"type": "image_url", "image_url": {"url": "https://example.com/cat.png", "detail": "high"}}      ]    }  ]}
```

Uploaded files (file/input_file/file_id) and non-imagedata:URLs return400 unsupported_content_type.

`file`
`input_file`
`file_id`
`data:`
`400 unsupported_content_type`

Streaming("stream": true): Returns Server-Sent Events (SSE) with token-by-token response chunks. ForChat Completions, the stream uses standardchat.completion.chunkevents plus Hermes' customhermes.tool.progressevent for tool-start UX. ForResponses, the stream uses OpenAI Responses event types such asresponse.created,response.output_text.delta,response.output_item.added,response.output_item.done, andresponse.completed.

`"stream": true`
`chat.completion.chunk`
`hermes.tool.progress`
`response.created`
`response.output_text.delta`
`response.output_item.added`
`response.output_item.done`
`response.completed`

Tool progress in streams:

- Chat Completions: Hermes emitsevent: hermes.tool.progressfor tool-start visibility without polluting persisted assistant text.
- Responses: Hermes emits spec-nativefunction_callandfunction_call_outputoutput items during the SSE stream, so clients can render structured tool UI in real time.

`event: hermes.tool.progress`
`function_call`
`function_call_output`

### POST /v1/responses​

OpenAI Responses API format. Supports server-side conversation state viaprevious_response_id— the server stores full conversation history (including tool calls and results) so multi-turn context is preserved without the client managing it.

`previous_response_id`

Request:

```
{  "model": "hermes-agent",  "input": "What files are in my project?",  "instructions": "You are a helpful coding assistant.",  "store": true}
```

Response:

```
{  "id": "resp_abc123",  "object": "response",  "status": "completed",  "model": "hermes-agent",  "output": [    {"type": "function_call", "name": "terminal", "arguments": "{\"command\": \"ls\"}", "call_id": "call_1"},    {"type": "function_call_output", "call_id": "call_1", "output": "README.md src/ tests/"},    {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "Your project has..."}]}  ],  "usage": {"input_tokens": 50, "output_tokens": 200, "total_tokens": 250}}
```

Inline image input:input[].contentcan containinput_textandinput_imageparts. Both remote URLs anddata:image/...URLs are supported:

`input[].content`
`input_text`
`input_image`
`data:image/...`

```
{  "model": "hermes-agent",  "input": [    {      "role": "user",      "content": [        {"type": "input_text", "text": "Describe this screenshot."},        {"type": "input_image", "image_url": "data:image/png;base64,iVBORw0K..."}      ]    }  ]}
```

Uploaded files (input_file/file_id) and non-imagedata:URLs return400 unsupported_content_type.

`input_file`
`file_id`
`data:`
`400 unsupported_content_type`

#### Multi-turn with previous_response_id​

Chain responses to maintain full context (including tool calls) across turns:

```
{  "input": "Now show me the README",  "previous_response_id": "resp_abc123"}
```

The server reconstructs the full conversation from the stored response chain — all previous tool calls and results are preserved. Chained requests also share the same session, so multi-turn conversations appear as a single entry in the dashboard and session history.

#### Named conversations​

Use theconversationparameter instead of tracking response IDs:

`conversation`

```
{"input": "Hello", "conversation": "my-project"}{"input": "What's in src/?", "conversation": "my-project"}{"input": "Run the tests", "conversation": "my-project"}
```

The server automatically chains to the latest response in that conversation. Like the/titlecommand for gateway sessions.

`/title`

### GET /v1/responses/{id}​

Retrieve a previously stored response by ID.

### DELETE /v1/responses/{id}​

Delete a stored response.

### GET /v1/models​

Lists the agent as an available model. The advertised model name defaults to theprofilename (orhermes-agentfor the default profile). Required by most frontends for model discovery.

`hermes-agent`

### GET /v1/capabilities​

Returns a machine-readable description of the API server's stable surface for external UIs, orchestrators, and plugin bridges.

```
{  "object": "hermes.api_server.capabilities",  "platform": "hermes-agent",  "model": "hermes-agent",  "auth": {"type": "bearer", "required": true},  "features": {    "chat_completions": true,    "responses_api": true,    "run_submission": true,    "run_status": true,    "run_events_sse": true,    "run_stop": true  }}
```

Use this endpoint when integrating dashboards, browser UIs, or control planes so they can discover whether the running Hermes version supports runs, streaming, cancellation, and session continuity without depending on private Python internals.

### GET /health​

Health check. Returns{"status": "ok"}. Also available atGET /v1/healthfor OpenAI-compatible clients that expect the/v1/prefix.

`{"status": "ok"}`
`/v1/`

### GET /health/detailed​

Extended health check that also reports active sessions, running agents, and resource usage. Useful for monitoring/observability tooling.

## Runs API (streaming-friendly alternative)​

In addition to/v1/chat/completionsand/v1/responses, the server exposes arunsAPI for long-form sessions where the client wants to subscribe to progress events instead of managing streaming themselves.

`/v1/chat/completions`
`/v1/responses`

### POST /v1/runs​

Create a new agent run. Returns arun_idthat can be used to subscribe to progress events.

`run_id`

```
{  "run_id": "run_abc123",  "status": "started"}
```

Runs accept a simpleinputstring and optionalsession_id,instructions,conversation_history, orprevious_response_id. Whensession_idis provided, Hermes surfaces it in the run status so external UIs can correlate runs with their own conversation IDs.

`input`
`session_id`
`instructions`
`conversation_history`
`previous_response_id`
`session_id`

### GET /v1/runs/{run_id}​

Poll the current run state. This is useful for dashboards that need status without holding an SSE connection open, or for UIs that reconnect after navigation.

```
{  "object": "hermes.run",  "run_id": "run_abc123",  "status": "completed",  "session_id": "space-session",  "model": "hermes-agent",  "output": "Done.",  "usage": {"input_tokens": 50, "output_tokens": 200, "total_tokens": 250}}
```

Statuses are retained briefly after terminal states (completed,failed, orcancelled) for polling and UI reconciliation.

`completed`
`failed`
`cancelled`

### GET /v1/runs/{run_id}/events​

Server-Sent Events stream of the run's tool-call progress, token deltas, and lifecycle events. Designed for dashboards and thick clients that want to attach/detach without losing state.

### POST /v1/runs/{run_id}/stop​

Interrupt a running agent turn. The endpoint returns immediately with{"status": "stopping"}while Hermes asks the active agent to stop at the next safe interruption point.

`{"status": "stopping"}`

### POST /v1/runs/{run_id}/approval​

Resolve a pending approval for a run that is waiting on a human decision (for example, a tool call gated behind an approval policy). The body carries the approval decision; the run resumes once the decision is recorded. This endpoint is advertised in/v1/capabilitiesas therun_approvalfeature so external UIs can detect support before surfacing an approval prompt.

`/v1/capabilities`
`run_approval`

## Jobs API (background scheduled work)​

The server exposes a lightweight jobs CRUD surface for managing scheduled / background agent runs from a remote client. All endpoints are gated behind the same bearer auth.

### GET /api/jobs​

List all scheduled jobs.

### POST /api/jobs​

Create a new scheduled job. Body accepts the same shape ashermes cron— prompt, schedule, skills, provider override, delivery target.

`hermes cron`

### GET /api/jobs/{job_id}​

Fetch a single job's definition and last-run state.

### PATCH /api/jobs/{job_id}​

Update fields on an existing job (prompt, schedule, etc.). Partial updates are merged.

### DELETE /api/jobs/{job_id}​

Remove a job. Also cancels any in-flight run.

### POST /api/jobs/{job_id}/pause​

Pause a job without deleting it. Next-scheduled-run timestamps are suspended until resumed.

### POST /api/jobs/{job_id}/resume​

Resume a previously paused job.

### POST /api/jobs/{job_id}/run​

Trigger the job to run immediately, out of schedule.

## Sessions API (session control over REST)​

External UIs can manage Hermes sessions over REST without standing up the dashboard. All endpoints are gated byAPI_SERVER_KEYand live under/api/sessions/*.

`API_SERVER_KEY`
`/api/sessions/*`
| Method | Path | Description |
| --- | --- | --- |
| GET | /api/sessions | List sessions (paginated —limit,offset,source,include_children) |
| POST | /api/sessions | Create an empty session |
| GET | /api/sessions/{id} | Read session metadata |
| PATCH | /api/sessions/{id} | Update title orend_reason |
| DELETE | /api/sessions/{id} | Delete a session |
| GET | /api/sessions/{id}/messages | Message history for a session |
| POST | /api/sessions/{id}/fork | Branch the session viaSessionDBlineage (matches CLI/branchsemantics) |
| POST | /api/sessions/{id}/chat | Run one synchronous agent turn |
| POST | /api/sessions/{id}/chat/stream | SSE wrapper over a single turn — emitsassistant.delta,tool.started,tool.completed,run.completedevents |

`GET`
`/api/sessions`
`limit`
`offset`
`source`
`include_children`
`POST`
`/api/sessions`
`GET`
`/api/sessions/{id}`
`PATCH`
`/api/sessions/{id}`
`end_reason`
`DELETE`
`/api/sessions/{id}`
`GET`
`/api/sessions/{id}/messages`
`POST`
`/api/sessions/{id}/fork`
`SessionDB`
`/branch`
`POST`
`/api/sessions/{id}/chat`
`POST`
`/api/sessions/{id}/chat/stream`
`assistant.delta`
`tool.started`
`tool.completed`
`run.completed`

/v1/capabilitiesadvertises the full surface viasession_*feature flags andendpoints.session_*entries so external UIs can detect support and fall back safely. Inline images are supported inchatandchat/streampayloads (multimodal-aware path).

`/v1/capabilities`
`session_*`
`endpoints.session_*`
`chat`
`chat/stream`

```
# fork a session and run one turncurl -X POST http://localhost:8642/api/sessions/$ID/fork \  -H "Authorization: Bearer $API_SERVER_KEY" \  -d '{"title": "explore alt path"}'# stream a turn over SSEcurl -N -X POST http://localhost:8642/api/sessions/$ID/chat/stream \  -H "Authorization: Bearer $API_SERVER_KEY" \  -d '{"input": "what files changed in the last hour?"}'
```

## Skills and toolsets discovery​

GET /v1/skillsandGET /v1/toolsetslet external clients enumerate the agent's capabilities deterministically over REST instead of asking the model. Both are read-only and gated byAPI_SERVER_KEY.

`GET /v1/skills`
`GET /v1/toolsets`
`API_SERVER_KEY`

```
curl http://localhost:8642/v1/skills \  -H "Authorization: Bearer $API_SERVER_KEY"# → [{"name": "github-pr-workflow", "description": "...", "category": "..."}, ...]curl http://localhost:8642/v1/toolsets \  -H "Authorization: Bearer $API_SERVER_KEY"# → [{"name": "core", "label": "...", "description": "...", "enabled": true,#     "configured": true, "tools": ["read_file", "write_file", ...]}, ...]
```

/v1/skillsreturns the same metadata the skills hub uses internally./v1/toolsetsreturns toolsets resolved for theapi_serverplatform with the concretetoolslist each one expands to. Both are advertised underendpoints.*in/v1/capabilities.

`/v1/skills`
`/v1/toolsets`
`api_server`
`tools`
`endpoints.*`
`/v1/capabilities`

## Long-term memory scoping (X-Hermes-Session-Key)​

`X-Hermes-Session-Key`

Multi-user frontends like Open WebUI need a stable per-channel identifier for long-term memory (Honcho, etc.) that isindependentof the transcript-scopedX-Hermes-Session-Id(which rotates on/new). PassX-Hermes-Session-Keyon/v1/chat/completions,/v1/responses, or/v1/runsand Hermes threads it through toAIAgent(gateway_session_key=...), where the Honcho memory provider uses it to derive a stable scope.

`X-Hermes-Session-Id`
`/new`
`X-Hermes-Session-Key`
`/v1/chat/completions`
`/v1/responses`
`/v1/runs`
`AIAgent(gateway_session_key=...)`

```
POST /v1/chat/completions HTTP/1.1Authorization: Bearer ***X-Hermes-Session-Id: transcript-alphaX-Hermes-Session-Key: agent:main:webui:dm:user-42
```

Rules: max 256 chars, control characters (\r,\n,\x00) are rejected, and the value is echoed back on responses (JSON + SSE)./v1/capabilitiesadvertises support via"session_key_header": "X-Hermes-Session-Key". Without the key, Honcho'sper-sessionstrategy produces a different scope persession_id— exactly the behavior Hermes had before.

`\r`
`\n`
`\x00`
`/v1/capabilities`
`"session_key_header": "X-Hermes-Session-Key"`
`per-session`
`session_id`

## System Prompt Handling​

When a frontend sends asystemmessage (Chat Completions) orinstructionsfield (Responses API), hermes-agentlayers it on topof its core system prompt. Your agent keeps all its tools, memory, and skills — the frontend's system prompt adds extra instructions.

`system`
`instructions`

This means you can customize behavior per-frontend without losing capabilities:

- Open WebUI system prompt: "You are a Python expert. Always include type hints."
- The agent still has terminal, file tools, web search, memory, etc.

## Authentication​

Bearer token auth via theAuthorizationheader:

`Authorization`

```
Authorization: Bearer ***
```

Configure the key viaAPI_SERVER_KEYenv var. If you need a browser to call Hermes directly, also setAPI_SERVER_CORS_ORIGINSto an explicit allowlist.

`API_SERVER_KEY`
`API_SERVER_CORS_ORIGINS`

The API server gives full access to hermes-agent's toolset,including terminal commands.API_SERVER_KEYisrequired for every deployment, including the default loopback bind on127.0.0.1. KeepAPI_SERVER_CORS_ORIGINSnarrow to control browser access when you explicitly allow browser callers.

`API_SERVER_KEY`
`127.0.0.1`
`API_SERVER_CORS_ORIGINS`

## Configuration​

### Environment Variables​

| Variable | Default | Description |
| --- | --- | --- |
| API_SERVER_ENABLED | false | Enable the API server |
| API_SERVER_PORT | 8642 | HTTP server port |
| API_SERVER_HOST | 127.0.0.1 | Bind address (localhost only by default) |
| API_SERVER_KEY | (required) | Bearer token for auth |
| API_SERVER_CORS_ORIGINS | (none) | Comma-separated allowed browser origins |
| API_SERVER_MODEL_NAME | (profile name) | Model name on/v1/models. Defaults to profile name, orhermes-agentfor default profile. |

`API_SERVER_ENABLED`
`false`
`API_SERVER_PORT`
`8642`
`API_SERVER_HOST`
`127.0.0.1`
`API_SERVER_KEY`
`API_SERVER_CORS_ORIGINS`
`API_SERVER_MODEL_NAME`
`/v1/models`
`hermes-agent`

### config.yaml​

```
# Not yet supported — use environment variables.# config.yaml support coming in a future release.
```

## Security Headers​

All responses include security headers:

- X-Content-Type-Options: nosniff— prevents MIME type sniffing
- Referrer-Policy: no-referrer— prevents referrer leakage

`X-Content-Type-Options: nosniff`
`Referrer-Policy: no-referrer`

## CORS​

The API server doesnotenable browser CORS by default.

For direct browser access, set an explicit allowlist:

```
API_SERVER_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

When CORS is enabled:

- Preflight responsesincludeAccess-Control-Max-Age: 600(10 minute cache)
- SSE streaming responsesinclude CORS headers so browser EventSource clients work correctly
- Idempotency-Keyis an allowed request header — clients can send it for deduplication (responses are cached by key for 5 minutes)

`Access-Control-Max-Age: 600`
`Idempotency-Key`

Most documented frontends such as Open WebUI connect server-to-server and do not need CORS at all.

## Compatible Frontends​

Any frontend that supports the OpenAI API format works. Tested/documented integrations:

| Frontend | Stars | Connection |
| --- | --- | --- |
| Open WebUI | 126k | Full guide available |
| LobeChat | 73k | Custom provider endpoint |
| LibreChat | 34k | Custom endpoint in librechat.yaml |
| AnythingLLM | 56k | Generic OpenAI provider |
| NextChat | 87k | BASE_URL env var |
| ChatBox | 39k | API Host setting |
| Jan | 26k | Remote model config |
| HF Chat-UI | 8k | OPENAI_BASE_URL |
| big-AGI | 7k | Custom endpoint |
| OpenAI Python SDK | — | OpenAI(base_url="http://localhost:8642/v1") |
| curl | — | Direct HTTP requests |

`OpenAI(base_url="http://localhost:8642/v1")`

## Multi-User Setup with Profiles​

To give multiple users their own isolated Hermes instance (separate config, memory, skills), useprofiles:

```
# Create a profile per userhermes profile create alicehermes profile create bob# Configure each profile's API server on a different port. API_SERVER_* are env# vars (not config.yaml keys), so write them to each profile's .env:cat >> ~/.hermes/profiles/alice/.env <<EOFAPI_SERVER_ENABLED=trueAPI_SERVER_PORT=8643API_SERVER_KEY=alice-secretEOFcat >> ~/.hermes/profiles/bob/.env <<EOFAPI_SERVER_ENABLED=trueAPI_SERVER_PORT=8644API_SERVER_KEY=bob-secretEOF# Start each profile's gatewayhermes -p alice gateway &hermes -p bob gateway &
```

Each profile's API server automatically advertises the profile name as the model ID:

- http://localhost:8643/v1/models→ modelalice
- http://localhost:8644/v1/models→ modelbob

`http://localhost:8643/v1/models`
`alice`
`http://localhost:8644/v1/models`
`bob`

In Open WebUI, add each as a separate connection. The model dropdown showsaliceandbobas distinct models, each backed by a fully isolated Hermes instance. See theOpen WebUI guidefor details.

`alice`
`bob`

## Limitations​

- Response storage— stored responses (forprevious_response_id) are persisted in SQLite and survive gateway restarts. Max 100 stored responses (LRU eviction).
- No file upload— inline images are supported on both/v1/chat/completionsand/v1/responses, but uploaded files (file,input_file,file_id) and non-image document inputs are not supported through the API.
- Model field is cosmetic— themodelfield in requests is accepted but the actual LLM model used is configured server-side in config.yaml.

`previous_response_id`
`/v1/chat/completions`
`/v1/responses`
`file`
`input_file`
`file_id`
`model`

## Proxy Mode​

The API server also serves as the backend forgateway proxy mode. When another Hermes gateway instance is configured withGATEWAY_PROXY_URLpointing at this API server, it forwards all messages here instead of running its own agent. This enables split deployments — for example, a Docker container handling Matrix E2EE that relays to a host-side agent.

`GATEWAY_PROXY_URL`

SeeMatrix Proxy Modefor the full setup guide.