- 
- Messaging Platforms
- Other
- LINE

# LINE Setup

Run Hermes Agent as aLINEbot via the official LINE Messaging API. The adapter lives as a bundled platform plugin underplugins/platforms/line/— no core edits, just enable it like any other platform.

`plugins/platforms/line/`

LINE is the dominant messaging app in Japan, Taiwan, and Thailand. If your users live there, this is how they reach you.

> Runhermes gateway setupand pickLINEfor a guided walk-through.

Runhermes gateway setupand pickLINEfor a guided walk-through.

`hermes gateway setup`

## How the bot responds​

| Context | Behavior |
| --- | --- |
| 1:1 chat(UIDs) | Responds to every message |
| Group chat(CIDs) | Responds when the group is on the allowlist |
| Multi-user room(RIDs) | Responds when the room is on the allowlist |

`U`
`C`
`R`

Inbound text, images, audio, video, files, stickers, and locations are all handled. Outbound text uses thefree reply token first(single-use, ~60s window) and falls back to the metered Push API when the token has expired.

## Step 1: Create a LINE Messaging API channel​

1. Go to theLINE Developers Console.
2. Create a Provider, then under it aMessaging APIchannel.
3. From the channel'sBasic settingstab, copy theChannel secret.
4. From theMessaging APItab, scroll toChannel access token (long-lived)and clickIssue. Copy the token.
5. In theMessaging APItab, also disableAuto-reply messagesandGreeting messagesso they don't fight your bot's replies.

## Step 2: Expose the webhook port​

LINE delivers webhooks over public HTTPS. The default port is8646— override withLINE_PORTif needed.

`8646`
`LINE_PORT`

```
# Cloudflare Tunnel (recommended for production — fixed hostname)cloudflared tunnel --url http://localhost:8646# ngrok (good for dev)ngrok http 8646# devtunneldevtunnel create hermes-line --allow-anonymousdevtunnel port create hermes-line -p 8646 --protocol httpsdevtunnel host hermes-line
```

Copy thehttps://...URL — you'll set it as the webhook URL below.Leave the tunnel runningwhile testing. For production, set up a fixed Cloudflare named tunnel so the webhook URL doesn't change on restart.

`https://...`

## Step 3: Configure Hermes​

Add to~/.hermes/.env:

`~/.hermes/.env`

```
LINE_CHANNEL_ACCESS_TOKEN=YOUR_LONG_LIVED_TOKENLINE_CHANNEL_SECRET=YOUR_CHANNEL_SECRET# Allowlist — at least one of these (or LINE_ALLOW_ALL_USERS=true for dev)LINE_ALLOWED_USERS=U1234567890abcdef...           # comma-separated U-prefixed IDsLINE_ALLOWED_GROUPS=C1234567890abcdef...          # optional group IDsLINE_ALLOWED_ROOMS=R1234567890abcdef...           # optional room IDs# Required for image / audio / video sends — the public HTTPS base URL# the tunnel resolves to.  Without it, send_image/voice/video will refuse.LINE_PUBLIC_URL=https://my-tunnel.example.com
```

Then in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
gateway:  platforms:    line:      enabled: true
```

That's enough — the bundled-plugin scan ingateway/config.pyautomatically picks upplugins/platforms/line/. NoPlatform.LINEenum edit, no_create_adapterregistration.

`gateway/config.py`
`plugins/platforms/line/`
`Platform.LINE`
`_create_adapter`

## Step 4: Set the webhook URL​

Back in the LINE console:

1. Open your channel →Messaging APItab.
2. UnderWebhook settings→Webhook URL, pastehttps://<your-tunnel>/line/webhook(note the/line/webhookpath — the adapter listens there).
3. ClickVerify. LINE pings the URL; you should see a 200.
4. ToggleUse webhooktoOn.

`https://<your-tunnel>/line/webhook`
`/line/webhook`

## Step 5: Run the gateway​

```
hermes gateway
```

The agent log shows:

```
LINE: webhook listening on 0.0.0.0:8646/line/webhook (public: https://my-tunnel.example.com)
```

Add the bot as a friend from the LINE app (scan the QR in the channel'sMessaging APItab) and send it a message.

## Slow LLM responses​

LINE's reply token is single-use and expires roughly 60 seconds after the inbound event. Slow LLMs can't reply in time, which would normally force a paid Push API call.

When the LLM is still running pastLINE_SLOW_RESPONSE_THRESHOLDseconds (default45), the adapter consumes the original reply token to send aTemplate Buttonsbubble:

`LINE_SLOW_RESPONSE_THRESHOLD`
`45`

> 🤔 Still thinking. Tap below to fetch the answer when it's ready.[ Get answer ]

🤔 Still thinking. Tap below to fetch the answer when it's ready.

[ Get answer ]

The user tapsGet answerwhen convenient — that postback delivers afreshreply token, which the adapter uses to send the cached answer (still free).

State machine:PENDING → READY → DELIVERED, plusERRORfor cancelled runs (the orphan PENDING resolves to "Run was interrupted before completion." after/stopso the persistent button doesn't loop).

`PENDING → READY → DELIVERED`
`ERROR`
`/stop`

To disable the postback button and always Push-fallback instead:

```
LINE_SLOW_RESPONSE_THRESHOLD=0
```

For the postback flow to fire reliably, suppress chatter that would consume the reply token before the threshold:

```
# ~/.hermes/config.yamldisplay:  interim_assistant_messages: false  platforms:    line:      tool_progress: off
```

## Cron / notification delivery​

```
LINE_HOME_CHANNEL=Uxxxxxxxxxxxxxxxxxxxx     # default delivery target
```

Cron jobs withdeliver: lineroute toLINE_HOME_CHANNEL. The adapter ships a standalone Push-only sender so cron jobs work even when cron runs in a separate process from the gateway.

`deliver: line`
`LINE_HOME_CHANNEL`

## Environment variable reference​

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| LINE_CHANNEL_ACCESS_TOKEN | yes | — | Long-lived channel access token |
| LINE_CHANNEL_SECRET | yes | — | Channel secret (HMAC-SHA256 webhook verification) |
| LINE_HOST | no | 0.0.0.0 | Webhook bind host |
| LINE_PORT | no | 8646 | Webhook bind port |
| LINE_PUBLIC_URL | for media | — | Public HTTPS base URL; required for image/voice/video sends |
| LINE_ALLOWED_USERS | one of | — | Comma-separated user IDs (U-prefixed) |
| LINE_ALLOWED_GROUPS | one of | — | Comma-separated group IDs (C-prefixed) |
| LINE_ALLOWED_ROOMS | one of | — | Comma-separated room IDs (R-prefixed) |
| LINE_ALLOW_ALL_USERS | dev only | false | Skip allowlist entirely |
| LINE_HOME_CHANNEL | no | — | Default cron / notification delivery target |
| LINE_SLOW_RESPONSE_THRESHOLD | no | 45 | Seconds before the postback button fires (0= disabled) |
| LINE_PENDING_TEXT | no | "🤔 Still thinking…" | Bubble text shown alongside the postback button |
| LINE_BUTTON_LABEL | no | "Get answer" | Button label |
| LINE_DELIVERED_TEXT | no | "Already replied ✅" | Reply when an already-delivered button is tapped again |
| LINE_INTERRUPTED_TEXT | no | "Run was interrupted before completion." | Reply when a/stoporphan button is tapped |

`LINE_CHANNEL_ACCESS_TOKEN`
`LINE_CHANNEL_SECRET`
`LINE_HOST`
`0.0.0.0`
`LINE_PORT`
`8646`
`LINE_PUBLIC_URL`
`LINE_ALLOWED_USERS`
`LINE_ALLOWED_GROUPS`
`LINE_ALLOWED_ROOMS`
`LINE_ALLOW_ALL_USERS`
`false`
`LINE_HOME_CHANNEL`
`LINE_SLOW_RESPONSE_THRESHOLD`
`45`
`0`
`LINE_PENDING_TEXT`
`LINE_BUTTON_LABEL`
`LINE_DELIVERED_TEXT`
`LINE_INTERRUPTED_TEXT`
`/stop`

## Troubleshooting​

"invalid signature" on webhook verify.TheChannel secretwas copied wrong, or your tunnel rewrote the request body. Verify withcurl -i https://<tunnel>/line/webhook/healthfirst — that should return{"status":"ok","platform":"line"}.

`Channel secret`
`curl -i https://<tunnel>/line/webhook/health`
`{"status":"ok","platform":"line"}`

Bot receives nothing in groups.CheckLINE_ALLOWED_GROUPSincludes theC...group ID. To find a group ID, send a test message and grep~/.hermes/logs/gateway.logforLINE: rejecting unauthorized source— the rejected source dict has the IDs.

`LINE_ALLOWED_GROUPS`
`C...`
`~/.hermes/logs/gateway.log`
`LINE: rejecting unauthorized source`

send_imagefails with "LINE_PUBLIC_URL must be set".LINE's Messaging API does not accept binary uploads — images, audio, and video must be reachable HTTPS URLs. SetLINE_PUBLIC_URLto the tunnel's public hostname and the adapter will serve files from/line/media/<token>/<filename>automatically.

`send_image`
`LINE_PUBLIC_URL`
`/line/media/<token>/<filename>`

Postback button never appears.Either the LLM responded faster thanLINE_SLOW_RESPONSE_THRESHOLD, or another bubble (tool-progress, streaming) consumed the reply token first. See the suppression block under "Slow LLM responses".

`LINE_SLOW_RESPONSE_THRESHOLD`

"already in use by another profile".The same channel access token is bound to another running Hermes profile. Stop the other gateway or use a separate channel.

## Limitations​

- Bubble and length caps.Each LINE text bubble is capped at 5000 characters. Longer responses are smart-chunked at ~4500 characters across up to 5 bubbles per Reply/Push call, splitting on natural boundaries where possible.
- No native message editing.LINE has no edit-message API — streaming responses always send fresh bubbles, never edit prior ones.
- No Markdown rendering.Bold (**), italics (*), code fences, and headings render as literal characters. The adapter strips them before sending; URLs are preserved ([label](url)becomeslabel (url)).
- Loading indicator is DM-only.LINE rejects the chat/loading API for groups and rooms, so the typing indicator only shows in 1:1 chats.

`**`
`*`
`[label](url)`
`label (url)`