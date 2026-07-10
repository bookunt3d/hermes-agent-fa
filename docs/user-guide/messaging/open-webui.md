---
layout: docs
title: "Messaging_Open Webui"
permalink: /docs/user-guide/messaging_open-webui/
---

- 
- Messaging Platforms
- Other
- Open WebUI

# Open WebUI Integration

Open WebUI(126k★) is the most popular self-hosted chat interface for AI. With Hermes Agent's built-in API server, you can use Open WebUI as a polished web frontend for your agent — complete with conversation management, user accounts, and a modern chat interface.

## Architecture​

Open WebUI connects to Hermes Agent's API server just like it would connect to OpenAI. Hermes handles the requests with its full toolset — terminal, file operations, web search, memory, skills — and returns the final response.

The API server is aHermes agent runtime, not a pure LLM proxy. For each request, Hermes creates a server-sideAIAgenton the API-server host. Tool calls run where that API server is running.

`AIAgent`

For example, if a laptop points Open WebUI or another OpenAI-compatible client at a Hermes API server on a remote machine,pwd, file tools, browser tools, local MCP tools, and other workspace tools run on the remote API-server host, not on the laptop.

`pwd`

Open WebUI talks to Hermes server-to-server, so you do not needAPI_SERVER_CORS_ORIGINSfor this integration.

`API_SERVER_CORS_ORIGINS`

## Quick Setup​

### 1. Enable the API server​

```
hermes config set API_SERVER_ENABLED truehermes config set API_SERVER_KEY your-secret-key
```

hermes config setauto-routes the flag toconfig.yamland the secret to~/.hermes/.env. If the gateway is already running, restart it so the change takes effect:

`hermes config set`
`config.yaml`
`~/.hermes/.env`

```
hermes gateway stop && hermes gateway
```

### 2. Start Hermes Agent gateway​

```
hermes gateway
```

You should see:

```
[API Server] API server listening on http://127.0.0.1:8642
```

### 3. Verify the API server is reachable​

```
curl -s http://127.0.0.1:8642/health# {"status": "ok", ...}curl -s -H "Authorization: Bearer your-secret-key" http://127.0.0.1:8642/v1/models# {"object":"list","data":[{"id":"hermes-agent", ...}]}
```

If/healthfails, the gateway didn't pick upAPI_SERVER_ENABLED=true— restart it. If/v1/modelsreturns401, yourAuthorizationheader doesn't matchAPI_SERVER_KEY.

`/health`
`API_SERVER_ENABLED=true`
`/v1/models`
`401`
`Authorization`
`API_SERVER_KEY`

### 4. Start Open WebUI​

```
docker run -d -p 3000:8080 \  -e OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1 \  -e OPENAI_API_KEY=your-secret-key \  -e ENABLE_OLLAMA_API=false \  --add-host=host.docker.internal:host-gateway \  -v open-webui:/app/backend/data \  --name open-webui \  --restart always \  ghcr.io/open-webui/open-webui:main
```

ENABLE_OLLAMA_API=falsesuppresses the default Ollama backend, which would otherwise show up empty and clutter the model picker. Omit it if you actually have Ollama running alongside.

`ENABLE_OLLAMA_API=false`

First launch takes 15–30 seconds: Open WebUI downloads sentence-transformer embedding models (~150MB) the first time it starts. Wait fordocker logs open-webuito settle before opening the UI.

`docker logs open-webui`

### 5. Open the UI​

Go tohttp://localhost:3000. Create your admin account (the first user becomes admin). You should see your agent in the model dropdown (named after your profile, orhermes-agentfor the default profile). Start chatting!

## Docker Compose Setup​

For a more permanent setup, create adocker-compose.yml:

`docker-compose.yml`

```
services:  open-webui:    image: ghcr.io/open-webui/open-webui:main    ports:      - "3000:8080"    volumes:      - open-webui:/app/backend/data    environment:      - OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1      - OPENAI_API_KEY=your-secret-key      - ENABLE_OLLAMA_API=false    extra_hosts:      - "host.docker.internal:host-gateway"    restart: alwaysvolumes:  open-webui:
```

Then:

```
docker compose up -d
```

## Configuring via the Admin UI​

If you prefer to configure the connection through the UI instead of environment variables:

1. Log in to Open WebUI athttp://localhost:3000
2. Click yourprofile avatar→Admin Settings
3. Go toConnections
4. UnderOpenAI API, click thewrench icon(Manage)
5. Click+ Add New Connection
6. Enter:URL:http://host.docker.internal:8642/v1API Key: the exact same value asAPI_SERVER_KEYin Hermes
7. Click thecheckmarkto verify the connection
8. Save

- URL:http://host.docker.internal:8642/v1
- API Key: the exact same value asAPI_SERVER_KEYin Hermes

`http://host.docker.internal:8642/v1`
`API_SERVER_KEY`

Your agent model should now appear in the model dropdown (named after your profile, orhermes-agentfor the default profile).

Environment variables only take effect on Open WebUI'sfirst launch. After that, connection settings are stored in its internal database. To change them later, use the Admin UI or delete the Docker volume and start fresh.

## API Type: Chat Completions vs Responses​

Open WebUI supports two API modes when connecting to a backend:

| Mode | Format | When to use |
| --- | --- | --- |
| Chat Completions(default) | /v1/chat/completions | Recommended. Works out of the box. |
| Responses(experimental) | /v1/responses | For server-side conversation state viaprevious_response_id. |

`/v1/chat/completions`
`/v1/responses`
`previous_response_id`

### Using Chat Completions (recommended)​

This is the default and requires no extra configuration. Open WebUI sends standard OpenAI-format requests and Hermes Agent responds accordingly. Each request includes the full conversation history.

### Using Responses API​

To use the Responses API mode:

1. Go toAdmin Settings→Connections→OpenAI→Manage
2. Edit your hermes-agent connection
3. ChangeAPI Typefrom "Chat Completions" to"Responses (Experimental)"
4. Save

With the Responses API, Open WebUI sends requests in the Responses format (inputarray +instructions), and Hermes Agent can preserve full tool call history across turns viaprevious_response_id. Whenstream: true, Hermes also streams spec-nativefunction_callandfunction_call_outputitems, which enables custom structured tool-call UI in clients that render Responses events.

`input`
`instructions`
`previous_response_id`
`stream: true`
`function_call`
`function_call_output`

Open WebUI currently manages conversation history client-side even in Responses mode — it sends the full message history in each request rather than usingprevious_response_id. The main advantage of Responses mode today is the structured event stream: text deltas,function_call, andfunction_call_outputitems arrive as OpenAI Responses SSE events instead of Chat Completions chunks.

`previous_response_id`
`function_call`
`function_call_output`

## How It Works​

When you send a message in Open WebUI:

1. Open WebUI sends aPOST /v1/chat/completionsrequest with your message and conversation history
2. Hermes Agent creates a server-sideAIAgentinstance using the API server's profile, model/provider config, memory, skills, and configured API-server toolsets
3. The agent processes your request — it may call tools (terminal, file operations, web search, etc.) on the API-server host
4. As tools execute,inline progress messages stream to the UIso you can see what the agent is doing (e.g.`💻 ls -la`,`🔍 Python 3.12 release`)
5. The agent's final text response streams back to Open WebUI
6. Open WebUI displays the response in its chat interface

`POST /v1/chat/completions`
`AIAgent`
``💻 ls -la``
``🔍 Python 3.12 release``

Your agent has access to the same tools and capabilities as that API-server Hermes instance. If the API server is remote, those tools are remote too.

If you need tools to run against yourlocalworkspace today, run Hermes locally and point it at a pure LLM provider or pure OpenAI-compatible model proxy (for example vLLM, LiteLLM, Ollama, llama.cpp, OpenAI, OpenRouter, etc.). A future split-runtime mode for "remote brain, local hands" is being tracked in#18715; it is not the behavior of the current API server.

With streaming enabled (the default), you'll see brief inline indicators as tools run — the tool emoji and its key argument. These appear in the response stream before the agent's final answer, giving you visibility into what's happening behind the scenes.

## Configuration Reference​

### Hermes Agent (API server)​

| Variable | Default | Description |
| --- | --- | --- |
| API_SERVER_ENABLED | false | Enable the API server |
| API_SERVER_PORT | 8642 | HTTP server port |
| API_SERVER_HOST | 127.0.0.1 | Bind address |
| API_SERVER_KEY | (required) | Bearer token for auth. MatchOPENAI_API_KEY. |

`API_SERVER_ENABLED`
`false`
`API_SERVER_PORT`
`8642`
`API_SERVER_HOST`
`127.0.0.1`
`API_SERVER_KEY`
`OPENAI_API_KEY`

### Open WebUI​

| Variable | Description |
| --- | --- |
| OPENAI_API_BASE_URL | Hermes Agent's API URL (include/v1) |
| OPENAI_API_KEY | Must be non-empty. Match yourAPI_SERVER_KEY. |

`OPENAI_API_BASE_URL`
`/v1`
`OPENAI_API_KEY`
`API_SERVER_KEY`

## Troubleshooting​

### No models appear in the dropdown​

- Check the URL has/v1suffix:http://host.docker.internal:8642/v1(not just:8642)
- Verify the gateway is running:curl http://localhost:8642/healthshould return{"status": "ok"}
- Check model listing:curl -H "Authorization: Bearer your-secret-key" http://localhost:8642/v1/modelsshould return a list withhermes-agent
- Docker networking: From inside Docker,localhostmeans the container, not your host. Usehost.docker.internalor--network=host.
- Empty Ollama backend shadowing the picker: If you omittedENABLE_OLLAMA_API=false, Open WebUI shows an empty Ollama section above your Hermes models. Restart the container with-e ENABLE_OLLAMA_API=falseor disable Ollama inAdmin Settings → Connections.

`/v1`
`http://host.docker.internal:8642/v1`
`:8642`
`curl http://localhost:8642/health`
`{"status": "ok"}`
`curl -H "Authorization: Bearer your-secret-key" http://localhost:8642/v1/models`
`hermes-agent`
`localhost`
`host.docker.internal`
`--network=host`
`ENABLE_OLLAMA_API=false`
`-e ENABLE_OLLAMA_API=false`

### Connection test passes but no models load​

This is almost always the missing/v1suffix. Open WebUI's connection test is a basic connectivity check — it doesn't verify model listing works.

`/v1`

### Response takes a long time​

Hermes Agent may be executing multiple tool calls (reading files, running commands, searching the web) before producing its final response. This is normal for complex queries. The response appears all at once when the agent finishes.

### "Invalid API key" errors​

Make sure yourOPENAI_API_KEYin Open WebUI matches theAPI_SERVER_KEYin Hermes Agent.

`OPENAI_API_KEY`
`API_SERVER_KEY`

Open WebUI persists OpenAI-compatible connection settings in its own database after first launch. If you accidentally saved a wrong key in the Admin UI, fixing the environment variables alone is not enough — update or delete the saved connection inAdmin Settings → Connections, or reset the Open WebUI data directory / database.

## Multi-User Setup with Profiles​

To run separate Hermes instances per user — each with their own config, memory, and skills — useprofiles. Each profile runs its own API server on a different port and automatically advertises the profile name as the model in Open WebUI.

### 1. Create profiles and configure API servers​

API_SERVER_*are env vars, not YAML config keys, so write them to each profile's.env. Pick ports outside the default-platform range (8644is the webhook adapter,8645is wecom-callback,8646is msgraph-webhook), e.g.8650+:

`API_SERVER_*`
`.env`
`8644`
`8645`
`8646`
`8650+`

```
hermes profile create alicecat >> ~/.hermes/profiles/alice/.env <<EOFAPI_SERVER_ENABLED=trueAPI_SERVER_PORT=8650API_SERVER_KEY=alice-secretEOFhermes profile create bobcat >> ~/.hermes/profiles/bob/.env <<EOFAPI_SERVER_ENABLED=trueAPI_SERVER_PORT=8651API_SERVER_KEY=bob-secretEOF
```

### 2. Start each gateway​

```
hermes -p alice gateway &hermes -p bob gateway &
```

### 3. Add connections in Open WebUI​

InAdmin Settings→Connections→OpenAI API→Manage, add one connection per profile:

| Connection | URL | API Key |
| --- | --- | --- |
| Alice | http://host.docker.internal:8650/v1 | alice-secret |
| Bob | http://host.docker.internal:8651/v1 | bob-secret |

`http://host.docker.internal:8650/v1`
`alice-secret`
`http://host.docker.internal:8651/v1`
`bob-secret`

The model dropdown will showaliceandbobas distinct models. You can assign models to Open WebUI users via the admin panel, giving each user their own isolated Hermes agent.

`alice`
`bob`

The model name defaults to the profile name. To override it, setAPI_SERVER_MODEL_NAMEin the profile's.env:

`API_SERVER_MODEL_NAME`
`.env`

```
hermes -p alice config set API_SERVER_MODEL_NAME "Alice's Agent"
```

## Linux Docker (no Docker Desktop)​

On Linux without Docker Desktop,host.docker.internaldoesn't resolve by default. Options:

`host.docker.internal`

```
# Option 1: Add host mappingdocker run --add-host=host.docker.internal:host-gateway ...# Option 2: Use host networkingdocker run --network=host -e OPENAI_API_BASE_URL=http://localhost:8642/v1 ...# Option 3: Use Docker bridge IPdocker run -e OPENAI_API_BASE_URL=http://172.17.0.1:8642/v1 ...
```