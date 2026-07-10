---
layout: docs
title: "Messaging_Msgraph Webhook"
permalink: /docs/user-guide/messaging/msgraph-webhook/
---

- 
- Messaging Platforms
- Microsoft 365
- Microsoft Graph Webhook Listener

# Microsoft Graph Webhook Listener

Themsgraph_webhookgateway platform is an inbound event listener. It's how Hermes receiveschange notificationsfrom Microsoft Graph — "a Teams meeting ended," "a new message landed in this chat," "this calendar event was updated." Different from theteamsplatform (which is a chat bot users type to) — this one is M365 telling Hermes something happened, not a person.

`msgraph_webhook`
`teams`

Right now the primary consumer is the Teams meeting summary pipeline: Graph notifies when a meeting produces a transcript, the pipeline fetches it, and Hermes posts a summary back into Teams. Other Graph resources (/chats/.../messages,/users/.../events) use the same listener — the pipeline consumers land with their own PRs.

`/chats/.../messages`
`/users/.../events`

## Prerequisites​

- Microsoft Graph application credentials —Register a Microsoft Graph Application
- Apublic HTTPS URLthat Microsoft Graph can reach (Graph does not call private endpoints). A dev tunnel works for testing; production needs a real domain with a valid certificate.
- A strong shared secret to use as theclientStatevalue. Generate withopenssl rand -hex 32and put it in~/.hermes/.envasMSGRAPH_WEBHOOK_CLIENT_STATE.

`clientState`
`openssl rand -hex 32`
`~/.hermes/.env`
`MSGRAPH_WEBHOOK_CLIENT_STATE`

## Quick Start​

Minimum~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
platforms:  msgraph_webhook:    enabled: true    extra:      host: 127.0.0.1      port: 8646      client_state: "replace-with-a-strong-secret"      accepted_resources:        - "communications/onlineMeetings"
```

Or via env vars in~/.hermes/.env(auto-merged on startup):

`~/.hermes/.env`

```
MSGRAPH_WEBHOOK_ENABLED=trueMSGRAPH_WEBHOOK_PORT=8646MSGRAPH_WEBHOOK_CLIENT_STATE=<generate-with-openssl-rand-hex-32>MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES=communications/onlineMeetings
```

Note: the bind host is read fromextra.hostinconfig.yaml(see the example above); there is noMSGRAPH_WEBHOOK_HOSTenv-var override.

`extra.host`
`config.yaml`
`MSGRAPH_WEBHOOK_HOST`

Start the gateway:hermes gateway run. The listener exposes:

`hermes gateway run`
- POST /msgraph/webhook— change notifications from Graph
- GET /msgraph/webhook?validationToken=...— Graph subscription validation handshake
- GET /health— readiness probe with accepted/duplicate counters

`POST /msgraph/webhook`
`GET /msgraph/webhook?validationToken=...`
`GET /health`

Expose the listener publicly (reverse proxy, dev tunnel, ingress). Your notification URL for Graph subscriptions is your public HTTPS origin followed by/msgraph/webhook:

`/msgraph/webhook`

```
https://ops.example.com/msgraph/webhook
```

## Configuration​

All settings go underplatforms.msgraph_webhook.extra:

`platforms.msgraph_webhook.extra`
| Setting | Default | Description |
| --- | --- | --- |
| host | 0.0.0.0 | Bind address for the HTTP listener. Non-loopback binds requireallowed_source_cidrs; loopback (127.0.0.1/::1) is the easiest dev-tunnel / reverse-proxy setup. |
| port | 8646 | Bind port. |
| webhook_path | /msgraph/webhook | URL path Graph POSTs to. |
| health_path | /health | Readiness endpoint. |
| client_state | — | Shared secret Graph echoes in every notification. Compared withhmac.compare_digest— generate withopenssl rand -hex 32. |
| accepted_resources | [](accept all) | Allowlist of Graph resource paths/patterns. Trailing*acts as prefix match. Leading/is tolerated. Example:["communications/onlineMeetings", "chats/*/messages"]. |
| max_seen_receipts | 5000 | Dedupe cache size for notification IDs. Oldest entries evicted when the cap is hit. |
| allowed_source_cidrs | [] | Required for non-loopback binds. Leave empty only when the listener is bound to loopback and fronted by a local tunnel / reverse proxy. |

`host`
`0.0.0.0`
`allowed_source_cidrs`
`127.0.0.1`
`::1`
`port`
`8646`
`webhook_path`
`/msgraph/webhook`
`health_path`
`/health`
`client_state`
`hmac.compare_digest`
`openssl rand -hex 32`
`accepted_resources`
`[]`
`*`
`/`
`["communications/onlineMeetings", "chats/*/messages"]`
`max_seen_receipts`
`5000`
`allowed_source_cidrs`
`[]`

Most settings also have an equivalent env var (MSGRAPH_WEBHOOK_*) that merges into the config at gateway startup (the exception ishost, which is config-only — see the note above) — see theenvironment variables reference.

`MSGRAPH_WEBHOOK_*`
`host`

## Security Hardening​

### clientState is the primary auth check​

Every Graph notification includes theclientStatestring your subscription registered with. The listener rejects any notification whoseclientStatedoesn't match, using timing-safe comparison. This is Microsoft's documented mechanism — treat the value as a strong shared secret.

`clientState`
`clientState`

Ifclient_stateis unset, the listener refuses to start.

`client_state`

### Source-IP allowlisting (production deployments)​

For production, restrict the listener to Microsoft's published Graph webhook source IP ranges. Microsoft documents the egress ranges under theOffice 365 IP Address and URL Web service. Configure them as:

```
platforms:  msgraph_webhook:    enabled: true    extra:      host: 0.0.0.0      client_state: "..."      allowed_source_cidrs:        - "52.96.0.0/14"        - "52.104.0.0/14"        # ...add the current Microsoft 365 "Common" + "Teams" category egress ranges
```

Or as an env var:

```
MSGRAPH_WEBHOOK_ALLOWED_SOURCE_CIDRS="52.96.0.0/14,52.104.0.0/14"
```

Binding a non-loopback host such as0.0.0.0,::, or a LAN IP withoutallowed_source_cidrsis refused at startup. If you're using a dev tunnel or reverse proxy on the same machine, bind Hermes to127.0.0.1or::1and leave the allowlist empty there. Invalid CIDR strings log a warning and are ignored.Review the Microsoft IP list quarterly— it changes.

`0.0.0.0`
`::`
`allowed_source_cidrs`
`127.0.0.1`
`::1`

### HTTPS termination​

The listener speaks plain HTTP. Terminate TLS at your reverse proxy (Caddy, Nginx, Cloudflare Tunnel, AWS ALB) and proxy to the listener over the local network. Graph refuses to deliver to non-HTTPS endpoints, so there's no path for unencrypted traffic to reach you from Graph itself.

### Response hygiene​

On success the listener returns202 Acceptedwith an empty body — internal counters stay out of the wire response. Operators can observe counts via/health, which is guarded by the same source-IP rules as the webhook path.

`202 Accepted`
`/health`

Status code table:

| Outcome | Status |
| --- | --- |
| Notification(s) accepted or deduped | 202 |
| Validation handshake (GET withvalidationToken) | 200 (echoes the token) |
| Every item in batch failed clientState | 403 |
| Malformed JSON / missingvaluearray / unknown resource | 400 |
| Source IP not in allowlist | 403 |
| Bare GET withoutvalidationToken | 400 |

`validationToken`
`value`
`validationToken`

## Troubleshooting​

| Problem | What to check |
| --- | --- |
| Graph subscription validation fails | Public URL is reachable,/msgraph/webhookpath matches, GET withvalidationTokenechoes the token verbatim astext/plainwithin 10 seconds. |
| Notifications POST but nothing ingests | client_statematches what you registered the subscription with. Re-runopenssl rand -hex 32and create a new subscription if the value drifted. Checkaccepted_resourcesincludes the resource path Graph is sending. |
| Every notification 403s | clientStatemismatch (forged, or subscription registered with a different value). Re-create the subscription withhermes teams-pipeline subscribe --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE" ...(ships with the pipeline runtime PR). |
| Listener refuses to start on0.0.0.0 | Setallowed_source_cidrsto Microsoft's current webhook egress ranges, or bind Hermes to127.0.0.1/::1behind your tunnel or reverse proxy. |
| Listener starts butcurl http://localhost:8646/healthhangs | Port binding collision. Checkss -tlnp | grep 8646and changeport:if needed. |
| Real Graph requests from Microsoft get 403'd | Source IP allowlist is too narrow. Widen the list to include the current Microsoft egress ranges. If you're still validating the tunnel path, bind Hermes to loopback and let the tunnel handle public exposure. |

`/msgraph/webhook`
`validationToken`
`text/plain`
`client_state`
`openssl rand -hex 32`
`accepted_resources`
`clientState`
`hermes teams-pipeline subscribe --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE" ...`
`0.0.0.0`
`allowed_source_cidrs`
`127.0.0.1`
`::1`
`curl http://localhost:8646/health`
`ss -tlnp | grep 8646`
`port:`

## Related Docs​

- Register a Microsoft Graph Application— Azure app registration prereq
- Environment Variables → Microsoft Graph— full env var list
- Microsoft Teams bot setup— the different platform that lets users chat with Hermes in Teams