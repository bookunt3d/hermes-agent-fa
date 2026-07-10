---
layout: docs
title: "Messaging_Wecom Callback"
permalink: /docs/user-guide/messaging_wecom-callback/
---

- 
- Messaging Platforms
- Chinese platforms
- WeCom Callback (Self-Built App)

# WeCom Callback (Self-Built App)

Connect Hermes to WeCom (Enterprise WeChat) as a self-built enterprise application using the callback/webhook model.

Hermes supports two WeCom integration modes:

- WeCom Bot— bot-style, connects via WebSocket. Simpler setup, works in group chats.
- WeCom Callback(this page) — self-built app, receives encrypted XML callbacks. Shows as a first-class app in users' WeCom sidebar. Supports multi-corp routing.

See also:WeCom Botfor the bot-style integration.

> Runhermes gateway setupand pickWeCom Callbackfor a guided walk-through.

Runhermes gateway setupand pickWeCom Callbackfor a guided walk-through.

`hermes gateway setup`

## How It Works​

1. You register a self-built application in the WeCom Admin Console
2. WeCom pushes encrypted XML to your HTTP callback endpoint
3. Hermes decrypts the message, queues it for the agent
4. Immediately acknowledges (silent — nothing displayed to the user)
5. The agent processes the request (typically 3–30 minutes)
6. The reply is delivered proactively via the WeCommessage/sendAPI

`message/send`

## Prerequisites​

- A WeCom enterprise account with admin access
- aiohttpandhttpxPython packages (included in the default install)
- A publicly reachable server for the callback URL (or a tunnel like ngrok)

`aiohttp`
`httpx`

## Setup​

### 1. Create a Self-Built App in WeCom​

1. Go toWeCom Admin Console→Applications→Create App
2. Note yourCorp ID(shown at the top of the admin console)
3. In the app settings, create aCorp Secret
4. Note theAgent IDfrom the app's overview page
5. UnderReceive Messages, configure the callback URL:URL:http://YOUR_PUBLIC_IP:8645/wecom/callbackToken: Generate a random token (WeCom provides one)EncodingAESKey: Generate a key (WeCom provides one)

- URL:http://YOUR_PUBLIC_IP:8645/wecom/callback
- Token: Generate a random token (WeCom provides one)
- EncodingAESKey: Generate a key (WeCom provides one)

`http://YOUR_PUBLIC_IP:8645/wecom/callback`

### 2. Configure Environment Variables​

Add to your.envfile:

`.env`

```
WECOM_CALLBACK_CORP_ID=your-corp-idWECOM_CALLBACK_CORP_SECRET=your-corp-secretWECOM_CALLBACK_AGENT_ID=1000002WECOM_CALLBACK_TOKEN=your-callback-tokenWECOM_CALLBACK_ENCODING_AES_KEY=your-43-char-aes-key# OptionalWECOM_CALLBACK_HOST=0.0.0.0WECOM_CALLBACK_PORT=8645WECOM_CALLBACK_ALLOWED_USERS=user1,user2
```

### 3. Start the Gateway​

```
hermes gateway
```

(Usehermes gateway startonly afterhermes gateway installhas registered the systemd/launchd service.)

`hermes gateway start`
`hermes gateway install`

The callback adapter starts an HTTP server on the configured port. WeCom will verify the callback URL via a GET request, then begin sending messages via POST.

## Configuration Reference​

Set these inconfig.yamlunderplatforms.wecom_callback.extra, or use environment variables:

`config.yaml`
`platforms.wecom_callback.extra`
| Setting | Default | Description |
| --- | --- | --- |
| corp_id | — | WeCom enterprise Corp ID (required) |
| corp_secret | — | Corp secret for the self-built app (required) |
| agent_id | — | Agent ID of the self-built app (required) |
| token | — | Callback verification token (required) |
| encoding_aes_key | — | 43-character AES key for callback encryption (required) |
| host | 0.0.0.0 | Bind address for the HTTP callback server |
| port | 8645 | Port for the HTTP callback server |
| path | /wecom/callback | URL path for the callback endpoint |

`corp_id`
`corp_secret`
`agent_id`
`token`
`encoding_aes_key`
`host`
`0.0.0.0`
`port`
`8645`
`path`
`/wecom/callback`

## Multi-App Routing​

For enterprises running multiple self-built apps (e.g., across different departments or subsidiaries), configure theappslist inconfig.yaml:

`apps`
`config.yaml`

```
platforms:  wecom_callback:    enabled: true    extra:      host: "0.0.0.0"      port: 8645      apps:        - name: "dept-a"          corp_id: "ww_corp_a"          corp_secret: "secret-a"          agent_id: "1000002"          token: "token-a"          encoding_aes_key: "key-a-43-chars..."        - name: "dept-b"          corp_id: "ww_corp_b"          corp_secret: "secret-b"          agent_id: "1000003"          token: "token-b"          encoding_aes_key: "key-b-43-chars..."
```

Users are scoped bycorp_id:user_idto prevent cross-corp collisions. When a user sends a message, the adapter records which app (corp) they belong to and routes replies through the correct app's access token.

`corp_id:user_id`

## Access Control​

Restrict which users can interact with the app:

```
# Allowlist specific usersWECOM_CALLBACK_ALLOWED_USERS=zhangsan,lisi,wangwu# Or allow all usersWECOM_CALLBACK_ALLOW_ALL_USERS=true
```

## Endpoints​

The adapter exposes:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | /wecom/callback | URL verification handshake (WeCom sends this during setup) |
| POST | /wecom/callback | Encrypted message callback (WeCom sends user messages here) |
| GET | /health | Health check — returns{"status": "ok"} |

`/wecom/callback`
`/wecom/callback`
`/health`
`{"status": "ok"}`

## Encryption​

All callback payloads are encrypted with AES-CBC using the EncodingAESKey. The adapter handles:

- Inbound: Decrypt XML payload, verify SHA1 signature
- Outbound: Replies sent via proactive API (not encrypted callback response)

The crypto implementation is compatible with Tencent's official WXBizMsgCrypt SDK.

## Limitations​

- No streaming— replies arrive as complete messages after the agent finishes
- No typing indicators— the callback model doesn't support typing status
- Text only— currently supports text messages for input; image/file/voice input not yet implemented. The agent is aware of outbound media capabilities via the WeCom platform hint (images, documents, video, voice).
- Response latency— agent sessions take 3–30 minutes; users see the reply when processing completes

## Troubleshooting​

Signature verification failing.WeCom signs every request with theTokenyou registered in the admin
console. A mismatch between the token configured in Hermes and the token the
admin console expects is the most common cause. Re-copy both theTokenandEncodingAESKeyfrom the admin console — they're easy to truncate. Whitespace
in~/.hermes/.envvalues around=will also break signature checks. After
fixing, restarthermes gateway run.

`~/.hermes/.env`
`=`
`hermes gateway run`

Callback URL not reachable / verification step fails.WeCom hits the public URL you registered. Confirm:

1. Your reverse proxy / tunnel forwards/wecom/callbackto the gateway's port.
2. The URL in the admin console is HTTPS (WeCom rejects plain HTTP).
3. From outside your network,curl -i https://<your-domain>/wecom/callbackreturns something other than a timeout (a 4xx without query params is fine —
it just means the listener is reachable).

`/wecom/callback`
`curl -i https://<your-domain>/wecom/callback`

Port not reachable / listener not bound.Checkhermes gateway runlogs for the bound host/port. If the adapter bound to127.0.0.1you must front it with a reverse proxy or tunnel — WeCom's servers
can't reach loopback. Setextra.host: 0.0.0.0inconfig.yaml(plusallowed_source_cidrsif exposing directly) or keep loopback and use a tunnel
such as Cloudflare Tunnel / nginx.

`hermes gateway run`
`127.0.0.1`
`extra.host: 0.0.0.0`
`config.yaml`
`allowed_source_cidrs`