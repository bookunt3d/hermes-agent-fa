---
layout: docs
title: "Features_Subscription Proxy"
permalink: /docs/user-guide/features_subscription-proxy/
---

- 
- Features
- Management
- Subscription Proxy

# Subscription Proxy

The subscription proxy is a local HTTP server that lets external apps —
OpenViking, Karakeep, Open WebUI, anything that speaks OpenAI-compatible
chat completions — use your Hermes-managed provider subscription as their
LLM endpoint. The proxy attaches the right credentials (refreshing them
automatically) so the app never needs a static API key.

This is different from theAPI server:

|  | API server | Subscription proxy |
| --- | --- | --- |
| What it serves | Your agent (full toolset, memory, skills) | Raw model inference |
| Use case | "Use Hermes as a chat backend" | "Use my Portal sub from another app" |
| Auth | YourAPI_SERVER_KEY | Any bearer (proxy attaches the real one) |
| Tool calls | Yes — the agent runs tools | No — passthrough only |

`API_SERVER_KEY`

Use the API server when you want theagentas a backend. Use the
proxy when you just wantthe modelthrough your subscription.

## Quick Start​

### 1. Log into your provider (one-time)​

```
hermes portal
```

This opens your browser for the Nous Portal OAuth flow. Hermes stores
the refresh token in~/.hermes/auth.json— the same place all Hermes
provider logins live.

`~/.hermes/auth.json`

### 2. Start the proxy​

```
hermes proxy start
```

```
Starting Hermes proxy for Nous Portal  Listening on:  http://127.0.0.1:8645/v1  Forwarding to: (resolved per-request from your subscription)  Use any bearer token in the client — the proxy attaches your real credential.
```

Leave this running in the foreground. Usetmux,nohup, or a systemd
unit if you want it to survive logout.

`tmux`
`nohup`

### 3. Point your app at it​

Any OpenAI-compatible app config takes the same triple:

```
Base URL:   http://127.0.0.1:8645/v1API key:    anything (e.g. "sk-unused")Model:      Hermes-4-70B    # or Hermes-4.3-36B, Hermes-4-405B
```

The proxy ignores theAuthorizationheader from your app and attaches
your real Portal credential to the upstream request. Refreshes happen
automatically when the bearer approaches expiry.

`Authorization`

## Available providers​

```
hermes proxy providers
```

Currently shipped:nous(Nous Portal) andxai(xAI / Grok). More
OAuth providers can be added by implementing theUpstreamAdapterinterface inhermes_cli/proxy/adapters/.

`nous`
`xai`
`UpstreamAdapter`
`hermes_cli/proxy/adapters/`

## Check status​

```
hermes proxy status
```

```
Hermes proxy upstream adapters  [nous    ] Nous Portal — ready (bearer expires 2026-05-15T06:43:21Z)
```

If you seenot logged in, runhermes portal. If you seecredentials need attention, your refresh token was revoked (rare —
happens if you signed out from the Portal web UI) — just re-runhermes portal.

`not logged in`
`hermes portal`
`credentials need attention`
`hermes portal`

## Allowed paths​

The proxy only forwards paths the upstream actually serves. For Nous
Portal:

| Path | Purpose |
| --- | --- |
| /v1/chat/completions | Chat completions (streaming + non-streaming) |
| /v1/completions | Legacy text completions |
| /v1/embeddings | Embeddings |
| /v1/models | Model list |

`/v1/chat/completions`
`/v1/completions`
`/v1/embeddings`
`/v1/models`

Other paths (/v1/images/generations,/v1/audio/speech, etc.) return
404 with a clear error pointing at the allowed paths. This keeps stray
clients from leaking weird requests to the upstream.

`/v1/images/generations`
`/v1/audio/speech`

## Configuring OpenViking to use Portal​

OpenVikingis a context
database that needs an LLM provider for its VLM (vision/language model
used to extract memories) and embedding model. With the proxy, you can
point itsvlm.api_baseat your local proxy:

`vlm.api_base`

Edit~/.openviking/ov.conf:

`~/.openviking/ov.conf`

```
{  "vlm": {    "provider": "openai",    "model": "Hermes-4-70B",    "api_base": "http://127.0.0.1:8645/v1",    "api_key": "unused-proxy-attaches-real-creds"  }}
```

Then start your proxy in a terminal alongsideopenviking-server:

`openviking-server`

```
# Terminal 1hermes proxy start# Terminal 2openviking-server
```

OpenViking's VLM calls now flow through your Portal subscription. The
embedding model side still needs its own provider — Portal does serve/v1/embeddingsbut the model selection depends on what your tier
supports; checkportal.nousresearch.com/models.

`/v1/embeddings`
`portal.nousresearch.com/models`

## Configuring Karakeep (or any bookmark/summarizer app)​

Karakeeptakes an OpenAI-compatible API for
bookmark summarization. In its config:

```
# Karakeep .envOPENAI_API_BASE_URL=http://127.0.0.1:8645/v1OPENAI_API_KEY=any-non-empty-stringINFERENCE_TEXT_MODEL=Hermes-4-70B
```

Same pattern works for Open WebUI, LobeChat, NextChat, or any other
OpenAI-compatible client.

## Exposing on LAN​

By default the proxy binds127.0.0.1(localhost only). To let other
machines on your network use it:

`127.0.0.1`

```
hermes proxy start --host 0.0.0.0 --port 8645
```

⚠Be aware:anyone on your network can now use your Portal
subscription. The proxy has no auth of its own — it accepts any bearer.
Use a firewall, VPN, or reverse proxy with proper auth if you expose
this beyond your trusted network.

## Rate limits​

Your Portal tier's RPM/TPM limits apply across the whole proxy. The
proxy doesn't fan out or pool — it's a single bearer with your full
subscription quota. Monitor usage atportal.nousresearch.com.

## Architecture​

The proxy is intentionally minimal. Per request:

1. ReceivePOST /v1/chat/completionsfrom your app
2. Look up the adapter's current credential (refresh if expiring)
3. Forward the request body verbatim, withAuthorization: Bearer <minted-key>
4. Stream the response back unchanged (SSE preserved)

`POST /v1/chat/completions`
`Authorization: Bearer <minted-key>`

No transformation. No logging of request bodies. No agent loop. The
proxy is a credential-attaching pass-through.

## Future: more OAuth providers​

The adapter system is pluggable. Adding a new provider (e.g.
HuggingFace, GitHub Copilot's chat endpoint, Anthropic via OAuth)
requires implementingUpstreamAdapterinhermes_cli/proxy/adapters/<provider>.pyand registering it inadapters/__init__.py. Providers that aren't OpenAI-compatible at the
protocol level (Anthropic Messages API, for example) would need a
transformation layer, which is out of scope for the current shape.

`UpstreamAdapter`
`hermes_cli/proxy/adapters/<provider>.py`
`adapters/__init__.py`