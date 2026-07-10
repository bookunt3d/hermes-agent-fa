---
layout: docs
title: "Messaging_Feishu"
permalink: /docs/user-guide/messaging_feishu/
---

- 
- Messaging Platforms
- Chinese platforms
- Feishu / Lark

# Feishu / Lark Setup

Hermes Agent integrates with Feishu and Lark as a full-featured bot. Once connected, you can chat with the agent in direct messages or group chats, receive cron job results in a home chat, and send text, images, audio, and file attachments through the normal gateway flow.

The integration supports both connection modes:

- websocket— recommended; Hermes opens the outbound connection and you do not need a public webhook endpoint
- webhook— useful when you want Feishu/Lark to push events into your gateway over HTTP

`websocket`
`webhook`

## How Hermes Behaves​

| Context | Behavior |
| --- | --- |
| Direct messages | Hermes responds to every message. |
| Group chats | Hermes responds only when the bot is @mentioned in the chat. |
| Shared group chats | By default, session history is isolated per user inside a shared chat. |

This shared-chat behavior is controlled byconfig.yaml:

`config.yaml`

```
group_sessions_per_user: true
```

Set it tofalseonly if you explicitly want one shared conversation per chat.

`false`

## Step 1: Create a Feishu / Lark App​

### Recommended: Scan-to-Create (one command)​

```
hermes gateway setup
```

SelectFeishu / Larkand scan the QR code with your Feishu or Lark mobile app. Hermes will automatically create a bot application with the correct permissions and save the credentials.

### Alternative: Manual Setup​

If scan-to-create is not available, the wizard falls back to manual input:

1. Open the Feishu or Lark developer console:Feishu:https://open.feishu.cn/Lark:https://open.larksuite.com/
2. Create a new app.
3. InCredentials & Basic Info, copy theApp IDandApp Secret.
4. Enable theBotcapability for the app.
5. Runhermes gateway setup, selectFeishu / Lark, and enter the credentials when prompted.

- Feishu:https://open.feishu.cn/
- Lark:https://open.larksuite.com/

`hermes gateway setup`

Keep the App Secret private. Anyone with it can impersonate your app.

### Configure Permissions​

In the Feishu developer console, go toPermission Managementand add the following scopes. You can bulk-import them in the permissions page.

Required permissions:

| Scope | Purpose |
| --- | --- |
| im:message | Receive and read messages |
| im:message:send_as_bot | Send messages as the bot |
| im:resource | Access images, files, and audio sent by users |
| im:chat | Access chat/group metadata |
| im:chat:readonly | Read chat list and membership |

`im:message`
`im:message:send_as_bot`
`im:resource`
`im:chat`
`im:chat:readonly`

Recommended permissions (for full functionality):

| Scope | Purpose |
| --- | --- |
| im:message.reactions:readonly | Receive emoji reaction events |
| admin:app.info:readonly | Auto-detect bot identity for @mention gating |
| contact:user.id:readonly | Resolve user IDs for allowlist matching |

`im:message.reactions:readonly`
`admin:app.info:readonly`
`contact:user.id:readonly`

### Configure Events​

InEvents and Callbacks:

1. Set the connection mode toLong Connection (WebSocket)(recommended) or configure a webhook URL
2. In theEvent Configurationsection, subscribe to:im.message.receive_v1— required for receiving messages

- im.message.receive_v1— required for receiving messages

`im.message.receive_v1`

### Publish the App​

After configuring permissions and events, go toVersion Managementand publish a new version of the app. The permissions won't take effect until a version is published and approved (for enterprise apps, this may require admin approval).

## Step 2: Choose a Connection Mode​

### Recommended: WebSocket mode​

Use WebSocket mode when Hermes runs on your laptop, workstation, or a private server. No public URL is required. The official Lark SDK opens and maintains a persistent outbound WebSocket connection with automatic reconnection.

```
FEISHU_CONNECTION_MODE=websocket
```

Requirements:ThewebsocketsPython package must be installed. The SDK handles connection lifecycle, heartbeats, and auto-reconnection internally.

`websockets`

How it works:The adapter runs the Lark SDK's WebSocket client in a background executor thread. Inbound events (messages, reactions, card actions) are dispatched to the main asyncio loop. On disconnect, the SDK will attempt to reconnect automatically.

### Optional: Webhook mode​

Use webhook mode only when you already run Hermes behind a reachable HTTP endpoint.

```
FEISHU_CONNECTION_MODE=webhook
```

In webhook mode, Hermes starts an HTTP server (viaaiohttp) and serves a Feishu endpoint at:

`aiohttp`

```
/feishu/webhook
```

Requirements:TheaiohttpPython package must be installed.

`aiohttp`

You can customize the webhook server bind address and path:

```
FEISHU_WEBHOOK_HOST=127.0.0.1   # default: 127.0.0.1FEISHU_WEBHOOK_PORT=8765         # default: 8765FEISHU_WEBHOOK_PATH=/feishu/webhook  # default: /feishu/webhook
```

When Feishu sends a URL verification challenge (type: url_verification), the webhook responds automatically so you can complete the subscription setup in the Feishu developer console. The challenge response is gated onFEISHU_VERIFICATION_TOKENwhen set — challenge requests with a missing or mismatched token are rejected so an unauthenticated remote cannot prove endpoint control by echoing attacker-controlled challenge data.

`type: url_verification`
`FEISHU_VERIFICATION_TOKEN`

## Step 3: Configure Hermes​

### Option A: Interactive Setup​

```
hermes gateway setup
```

SelectFeishu / Larkand fill in the prompts.

### Option B: Manual Configuration​

Add the following to~/.hermes/.env:

`~/.hermes/.env`

```
FEISHU_APP_ID=cli_xxxFEISHU_APP_SECRET=secret_xxxFEISHU_DOMAIN=feishuFEISHU_CONNECTION_MODE=websocket# Optional but strongly recommendedFEISHU_ALLOWED_USERS=ou_xxx,ou_yyyFEISHU_HOME_CHANNEL=oc_xxx
```

FEISHU_DOMAINaccepts:

`FEISHU_DOMAIN`
- feishufor Feishu China
- larkfor Lark international

`feishu`
`lark`

## Step 4: Start the Gateway​

```
hermes gateway
```

Then message the bot from Feishu/Lark to confirm that the connection is live.

## Home Chat​

Use/set-homein a Feishu/Lark chat to mark it as the home channel for cron job results and cross-platform notifications.

`/set-home`

You can also preconfigure it:

```
FEISHU_HOME_CHANNEL=oc_xxx
```

## Security​

### User Allowlist​

For production use, set an allowlist of Feishu Open IDs:

```
FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy
```

If you leave the allowlist empty, anyone who can reach the bot may be able to use it. In group chats, the allowlist is checked against the sender's open_id before the message is processed.

### Webhook Encryption Key​

When running in webhook mode, set an encryption key to enable signature verification of inbound webhook payloads:

```
FEISHU_ENCRYPT_KEY=your-encrypt-key
```

This key is found in theEvent Subscriptionssection of your Feishu app configuration. When set, the adapter verifies every webhook request using the signature algorithm:

```
SHA256(timestamp + nonce + encrypt_key + body)
```

The computed hash is compared against thex-lark-signatureheader using timing-safe comparison. Requests with invalid or missing signatures are rejected with HTTP 401.

`x-lark-signature`

In WebSocket mode, signature verification is handled by the SDK itself, soFEISHU_ENCRYPT_KEYis optional. In webhook mode, it is strongly recommended for production.

`FEISHU_ENCRYPT_KEY`

### Verification Token​

An additional layer of authentication that checks thetokenfield inside webhook payloads:

`token`

```
FEISHU_VERIFICATION_TOKEN=your-verification-token
```

This token is also found in theEvent Subscriptionssection of your Feishu app. When set, every inbound webhook payload must contain a matchingtokenin itsheaderobject. Mismatched tokens are rejected with HTTP 401.

`token`
`header`

BothFEISHU_ENCRYPT_KEYandFEISHU_VERIFICATION_TOKENcan be used together for defense in depth.

`FEISHU_ENCRYPT_KEY`
`FEISHU_VERIFICATION_TOKEN`

## Group Message Policy​

TheFEISHU_GROUP_POLICYenvironment variable controls whether and how Hermes responds in group chats:

`FEISHU_GROUP_POLICY`

```
FEISHU_GROUP_POLICY=allowlist   # default
```

| Value | Behavior |
| --- | --- |
| open | Hermes responds to @mentions from any user in any group. |
| allowlist | Hermes only responds to @mentions from users listed inFEISHU_ALLOWED_USERS. |
| disabled | Hermes ignores all group messages entirely. |

`open`
`allowlist`
`FEISHU_ALLOWED_USERS`
`disabled`

In all modes, the bot must be explicitly @mentioned (or @all) in the group before the message is processed. Direct messages always bypass this gate.

SetFEISHU_REQUIRE_MENTION=falseto let Hermes read all group traffic without requiring an @mention:

`FEISHU_REQUIRE_MENTION=false`

```
FEISHU_REQUIRE_MENTION=false
```

For per-chat control, setrequire_mentionon agroup_rulesentry — seePer-Group Access Controlbelow.

`require_mention`
`group_rules`

### Bot Identity​

Hermes auto-detects the bot'sopen_idand display name on startup. You only need to set these manually when auto-detection cannot reach the Feishu API, or when your app uses tenant-scoped user IDs:

`open_id`

```
FEISHU_BOT_OPEN_ID=ou_xxx     # only when auto-detection failsFEISHU_BOT_USER_ID=xxx        # required if your app uses sender_id_type=user_idFEISHU_BOT_NAME=MyBot         # only when auto-detection fails
```

## Bot-to-Bot Messaging​

By default Hermes ignores messages sent by other bots. Enable bot-to-bot messaging when you want Hermes to participate in A2A orchestration or receive notifications from other bots in the same group.

```
FEISHU_ALLOW_BOTS=mentions   # default: none
```

| Value | Behavior |
| --- | --- |
| none | Ignore all messages from other bots (default). |
| mentions | Accept only when the peer bot @mentions Hermes. |
| all | Accept every peer bot message. |

`none`
`mentions`
`all`

Also configurable asfeishu.allow_botsinconfig.yaml(env wins when both are set).

`feishu.allow_bots`
`config.yaml`

Peer bots do not need to be added toFEISHU_ALLOWED_USERS— that allowlist applies to human senders only.

`FEISHU_ALLOWED_USERS`

Grant theapplication:bot.basic_info:readscope to display peer bot names; without it, peer bots still route correctly but appear as theiropen_id.

`application:bot.basic_info:read`
`open_id`

## Interactive Card Actions​

When users click buttons or interact with interactive cards sent by the bot, the adapter routes these as synthetic/cardcommand events:

`/card`
- Button clicks become:/card button {"key": "value", ...}
- The action'svaluepayload from the card definition is included as JSON.
- Card actions are deduplicated with a 15-minute window to prevent double processing.

`/card button {"key": "value", ...}`
`value`

Gateway-driven update prompts use a native FeishuYes/Nocard instead of falling back to plain text replies. Whenhermes update --gatewayneeds confirmation, the adapter records the selected answer in Hermes's.update_responsefile and replaces the card inline with a resolved state.

`Yes`
`No`
`hermes update --gateway`
`.update_response`

Card action events are dispatched withMessageType.COMMAND, so they flow through the normal command processing pipeline.

`MessageType.COMMAND`

This is also howcommand approvalworks — when the agent needs to run a dangerous command, it sends an interactive card with Allow Once / Session / Always / Deny buttons. The user clicks a button, and the card action callback delivers the approval decision back to the agent.

### Required Feishu App Configuration​

Interactive cards requirethreeconfiguration steps in the Feishu Developer Console. Missing any of them causes error200340when users click card buttons.

1. Subscribe to the card action event:InEvent Subscriptions, addcard.action.triggerto your subscribed events.
2. Enable the Interactive Card capability:InApp Features > Bot, ensure theInteractive Cardtoggle is enabled. This tells Feishu that your app can receive card action callbacks.
3. Configure the Card Request URL (webhook mode only):InApp Features > Bot > Message Card Request URL, set the URL to the same endpoint as your event webhook (e.g.https://your-server:8765/feishu/webhook). In WebSocket mode this is handled automatically by the SDK.

Subscribe to the card action event:InEvent Subscriptions, addcard.action.triggerto your subscribed events.

`card.action.trigger`

Enable the Interactive Card capability:InApp Features > Bot, ensure theInteractive Cardtoggle is enabled. This tells Feishu that your app can receive card action callbacks.

Configure the Card Request URL (webhook mode only):InApp Features > Bot > Message Card Request URL, set the URL to the same endpoint as your event webhook (e.g.https://your-server:8765/feishu/webhook). In WebSocket mode this is handled automatically by the SDK.

`https://your-server:8765/feishu/webhook`

Without all three steps, Feishu will successfullysendinteractive cards (sending only requiresim:message:sendpermission), but clicking any button will return error 200340. The card appears to work — the error only surfaces when a user interacts with it.

`im:message:send`

## Document Comment Intelligent Reply​

Beyond chat, the adapter can also answer@-mentions left onFeishu/Lark documents. When a user comments on a document (local text selection or whole-doc comment) and @-mentions the bot, Hermes reads the document plus the surrounding comment thread and posts an LLM reply inline on the thread.

`@`

Powered by thedrive.notice.comment_add_v1event, the handler:

`drive.notice.comment_add_v1`
- Fetches the document content and comment timeline in parallel (20 messages for whole-doc threads, 12 for local-selection threads).
- Runs the agent with thefeishu_doc+feishu_drivetoolsets scoped to that single comment session.
- Chunks replies at 4000 chars and posts them back as threaded replies.
- Caches per-document sessions for 1 hour with a 50-message cap so follow-up comments on the same doc keep context.

`feishu_doc`
`feishu_drive`

### 3-Tier Access Control​

Document-comment replies areexplicit-grant only— there is no implicit allow-all mode. Permissions resolve in this order (first match wins, per field):

1. Exact doc— rule scoped to a specific document token.
2. Wildcard— rule that matches a pattern of docs.
3. Top-level— default rule for the workspace.

Two policies are available per rule:

- allowlist— a static list of users / tenants.
- pairing— static list ∪ runtime-approved store. Useful for rollouts where moderators can grant access live.

`allowlist`
`pairing`

Rules live in~/.hermes/feishu_comment_rules.json(pairing grants in~/.hermes/feishu_comment_pairing.json) with mtime-cached hot-reload — edits take effect on the next comment event without restarting the gateway.

`~/.hermes/feishu_comment_rules.json`
`~/.hermes/feishu_comment_pairing.json`

CLI:

```
# Inspect current rules and pairing statepython -m gateway.platforms.feishu_comment_rules status# Simulate an access check for a specific doc + userpython -m gateway.platforms.feishu_comment_rules check <fileType:fileToken> <user_open_id># Manage pairing grants at runtimepython -m gateway.platforms.feishu_comment_rules pairing listpython -m gateway.platforms.feishu_comment_rules pairing add <user_open_id>python -m gateway.platforms.feishu_comment_rules pairing remove <user_open_id>
```

### Required Feishu App Configuration​

On top of the chat/card permissions already granted, add the drive comment event:

- Subscribe todrive.notice.comment_add_v1inEvent Subscriptions.
- Grant thedocs:doc:readonlyanddrive:drive:readonlyscopes so the handler can read document content.

`drive.notice.comment_add_v1`
`docs:doc:readonly`
`drive:drive:readonly`

## Meeting Invitation Events​

You can invite the Hermes Feishu/Lark bot into a video meeting the same way you invite a human participant. When the bot receives the meeting invitation event, Hermes can automatically start an agent turn that attempts to join the meeting.

Powered by thevc.bot.meeting_invited_v1event, the flow is:

`vc.bot.meeting_invited_v1`
- A user invites the bot to a Feishu/Lark video meeting.
- Feishu/Lark sends Hermes the meeting invitation event.
- Hermes extracts the inviter, meeting topic, and meeting number.
- If the inviter is authorized by the normal gateway allowlist or pairing policy, the agent receives the meeting number and tries to join automatically.
- If the invite is malformed, or the agent cannot join, Hermes drops the event or replies to the inviter with a concise explanation.

Malformed invitations that do not include both an inviter and ameeting_noare ignored.

`meeting_no`

### Required Feishu App Configuration​

On top of the chat/card permissions already granted, add the video-meeting invitation event:

- Subscribe tovc.bot.meeting_invited_v1inEvent Subscriptions.
- Enable the Video Conferencing permission scope prompted by the Feishu/Lark developer console for that event.
- Keepim:messageandim:message:send_as_botenabled so Hermes can reply to the inviter.
- Ensure the gateway user allowlist or pairing policy authorizes the inviter. Meeting invitations do not bypass normal gateway access checks.

`vc.bot.meeting_invited_v1`
`im:message`
`im:message:send_as_bot`

## Media Support​

### Inbound (receiving)​

The adapter receives and caches the following media types from users:

| Type | Extensions | How it's processed |
| --- | --- | --- |
| Images | .jpg, .jpeg, .png, .gif, .webp, .bmp | Downloaded via Feishu API and cached locally |
| Audio | .ogg, .mp3, .wav, .m4a, .aac, .flac, .opus, .webm | Downloaded and cached; small text files are auto-extracted |
| Video | .mp4, .mov, .avi, .mkv, .webm, .m4v, .3gp | Downloaded and cached as documents |
| Files | .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx, and more | Downloaded and cached as documents |

Media from rich-text (post) messages, including inline images and file attachments, is also extracted and cached.

For small text-based documents (.txt, .md), the file content is automatically injected into the message text so the agent can read it directly without needing tools.

### Outbound (sending)​

| Method | What it sends |
| --- | --- |
| send | Text or rich post messages (auto-detected based on markdown content) |
| send_image/send_image_file | Uploads image to Feishu, then sends as native image bubble (with optional caption) |
| send_document | Uploads file to Feishu API, then sends as file attachment |
| send_voice | Uploads audio file as a Feishu file attachment |
| send_video | Uploads video and sends as native media message |
| send_animation | GIFs are downgraded to file attachments (Feishu has no native GIF bubble) |

`send`
`send_image`
`send_image_file`
`send_document`
`send_voice`
`send_video`
`send_animation`

File upload routing is automatic based on extension:

- .ogg,.opus→ uploaded asopusaudio
- .mp4,.mov,.avi,.m4v→ uploaded asmp4media
- .pdf,.doc(x),.xls(x),.ppt(x)→ uploaded with their document type
- Everything else → uploaded as a generic stream file

`.ogg`
`.opus`
`opus`
`.mp4`
`.mov`
`.avi`
`.m4v`
`mp4`
`.pdf`
`.doc(x)`
`.xls(x)`
`.ppt(x)`

## Markdown Rendering and Post Fallback​

When outbound text contains markdown formatting (headings, bold, lists, code blocks, links, etc.), the adapter automatically sends it as a Feishupostmessage with an embeddedmdtag rather than as plain text. This enables rich rendering in the Feishu client.

`md`

If the Feishu API rejects the post payload (e.g., due to unsupported markdown constructs), the adapter automatically falls back to sending as plain text with markdown stripped. This two-stage fallback ensures messages are always delivered.

Plain text messages (no markdown detected) are sent as the simpletextmessage type.

`text`

## Processing Status Reactions​

While the agent is working, the bot shows aTypingreaction on your message. It's cleared when the reply arrives, or replaced withCrossMarkif processing failed.

`Typing`
`CrossMark`

SetFEISHU_REACTIONS=falseto turn it off.

`FEISHU_REACTIONS=false`

## Burst Protection and Batching​

The adapter includes debouncing for rapid message bursts to avoid overwhelming the agent:

### Text Batching​

When a user sends multiple text messages in quick succession, they are merged into a single event before being dispatched:

| Setting | Env Var | Default |
| --- | --- | --- |
| Quiet period | HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS | 0.6s |
| Max messages per batch | HERMES_FEISHU_TEXT_BATCH_MAX_MESSAGES | 8 |
| Max characters per batch | HERMES_FEISHU_TEXT_BATCH_MAX_CHARS | 4000 |

`HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS`
`HERMES_FEISHU_TEXT_BATCH_MAX_MESSAGES`
`HERMES_FEISHU_TEXT_BATCH_MAX_CHARS`

### Media Batching​

Multiple media attachments sent in quick succession (e.g., dragging several images) are merged into a single event:

| Setting | Env Var | Default |
| --- | --- | --- |
| Quiet period | HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS | 0.8s |

`HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS`

### Per-Chat Serialization​

Messages within the same chat are processed serially (one at a time) to maintain conversation coherence. Each chat has its own lock, so messages in different chats are processed concurrently.

## Rate Limiting (Webhook Mode)​

In webhook mode, the adapter enforces per-IP rate limiting to protect against abuse:

- Window:60-second sliding window
- Limit:120 requests per window per (app_id, path, IP) triple
- Tracking cap:Up to 4096 unique keys tracked (prevents unbounded memory growth)

Requests that exceed the limit receive HTTP 429 (Too Many Requests).

### Webhook Anomaly Tracking​

The adapter tracks consecutive error responses per IP address. After 25 consecutive errors from the same IP within a 6-hour window, a warning is logged. This helps detect misconfigured clients or probing attempts.

Additional webhook protections:

- Body size limit:1 MB maximum
- Body read timeout:30 seconds
- Content-Type enforcement:Onlyapplication/jsonis accepted

`application/json`

## WebSocket Tuning​

When usingwebsocketmode, you can customize reconnect and ping behavior:

`websocket`

```
platforms:  feishu:    extra:      ws_reconnect_interval: 120   # Seconds between reconnect attempts (default: 120)      ws_ping_interval: 30         # Seconds between WebSocket pings (optional; SDK default if unset)
```

| Setting | Config key | Default | Description |
| --- | --- | --- | --- |
| Reconnect interval | ws_reconnect_interval | 120s | How long to wait between reconnection attempts |
| Ping interval | ws_ping_interval | (SDK default) | Frequency of WebSocket keepalive pings |

`ws_reconnect_interval`
`ws_ping_interval`

## Per-Group Access Control​

Beyond the globalFEISHU_GROUP_POLICY, you can set fine-grained rules per group chat usinggroup_rulesin config.yaml:

`FEISHU_GROUP_POLICY`
`group_rules`

```
platforms:  feishu:    extra:      default_group_policy: "open"     # Default for groups not in group_rules      admins:                          # Users who can manage bot settings        - "ou_admin_open_id"      group_rules:        "oc_group_chat_id_1":          policy: "allowlist"          # open | allowlist | blacklist | admin_only | disabled          allowlist:            - "ou_user_open_id_1"            - "ou_user_open_id_2"        "oc_group_chat_id_2":          policy: "admin_only"        "oc_group_chat_id_3":          policy: "blacklist"          blacklist:            - "ou_blocked_user"        "oc_free_chat":          policy: "open"          require_mention: false       # overrides FEISHU_REQUIRE_MENTION for this chat
```

| Policy | Description |
| --- | --- |
| open | Anyone in the group can use the bot |
| allowlist | Only users in the group'sallowlistcan use the bot |
| blacklist | Everyone except users in the group'sblacklistcan use the bot |
| admin_only | Only users in the globaladminslist can use the bot in this group |
| disabled | Bot ignores all messages in this group |

`open`
`allowlist`
`allowlist`
`blacklist`
`blacklist`
`admin_only`
`admins`
`disabled`

Setrequire_mention: falseon agroup_rulesentry to skip the @-mention requirement for that specific chat. When omitted, the chat inherits the globalFEISHU_REQUIRE_MENTIONvalue.

`require_mention: false`
`group_rules`
`FEISHU_REQUIRE_MENTION`

Groups not listed ingroup_rulesfall back todefault_group_policy(defaults to the value ofFEISHU_GROUP_POLICY).

`group_rules`
`default_group_policy`
`FEISHU_GROUP_POLICY`

## Deduplication​

Inbound messages are deduplicated using message IDs with a 24-hour TTL. The dedup state is persisted across restarts to~/.hermes/feishu_seen_message_ids.json.

`~/.hermes/feishu_seen_message_ids.json`
| Setting | Env Var | Default |
| --- | --- | --- |
| Cache size | HERMES_FEISHU_DEDUP_CACHE_SIZE | 2048 entries |

`HERMES_FEISHU_DEDUP_CACHE_SIZE`

## All Environment Variables​

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| FEISHU_APP_ID | ✅ | — | Feishu/Lark App ID |
| FEISHU_APP_SECRET | ✅ | — | Feishu/Lark App Secret |
| FEISHU_DOMAIN | — | feishu | feishu(China) orlark(international) |
| FEISHU_CONNECTION_MODE | — | websocket | websocketorwebhook |
| FEISHU_ALLOWED_USERS | — | (empty) | Comma-separated open_id list for user allowlist |
| FEISHU_ALLOW_BOTS | — | none | Accept messages from other bots:none,mentions, orall |
| FEISHU_REQUIRE_MENTION | — | true | Whether group messages must @mention the bot |
| FEISHU_HOME_CHANNEL | — | — | Chat ID for cron/notification output |
| FEISHU_ENCRYPT_KEY | — | (empty) | Encrypt key for webhook signature verification |
| FEISHU_VERIFICATION_TOKEN | — | (empty) | Verification token for webhook payload auth |
| FEISHU_GROUP_POLICY | — | allowlist | Group message policy:open,allowlist,disabled |
| FEISHU_BOT_OPEN_ID | — | (empty) | Bot's open_id (for @mention detection) |
| FEISHU_BOT_USER_ID | — | (empty) | Bot's user_id (for @mention detection) |
| FEISHU_BOT_NAME | — | (empty) | Bot's display name (for @mention detection) |
| FEISHU_WEBHOOK_HOST | — | 127.0.0.1 | Webhook server bind address |
| FEISHU_WEBHOOK_PORT | — | 8765 | Webhook server port |
| FEISHU_WEBHOOK_PATH | — | /feishu/webhook | Webhook endpoint path |
| HERMES_FEISHU_DEDUP_CACHE_SIZE | — | 2048 | Max deduplicated message IDs to track |
| HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS | — | 0.6 | Text burst debounce quiet period |
| HERMES_FEISHU_TEXT_BATCH_MAX_MESSAGES | — | 8 | Max messages merged per text batch |
| HERMES_FEISHU_TEXT_BATCH_MAX_CHARS | — | 4000 | Max characters merged per text batch |
| HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS | — | 0.8 | Media burst debounce quiet period |

`FEISHU_APP_ID`
`FEISHU_APP_SECRET`
`FEISHU_DOMAIN`
`feishu`
`feishu`
`lark`
`FEISHU_CONNECTION_MODE`
`websocket`
`websocket`
`webhook`
`FEISHU_ALLOWED_USERS`
`FEISHU_ALLOW_BOTS`
`none`
`none`
`mentions`
`all`
`FEISHU_REQUIRE_MENTION`
`true`
`FEISHU_HOME_CHANNEL`
`FEISHU_ENCRYPT_KEY`
`FEISHU_VERIFICATION_TOKEN`
`FEISHU_GROUP_POLICY`
`allowlist`
`open`
`allowlist`
`disabled`
`FEISHU_BOT_OPEN_ID`
`FEISHU_BOT_USER_ID`
`FEISHU_BOT_NAME`
`FEISHU_WEBHOOK_HOST`
`127.0.0.1`
`FEISHU_WEBHOOK_PORT`
`8765`
`FEISHU_WEBHOOK_PATH`
`/feishu/webhook`
`HERMES_FEISHU_DEDUP_CACHE_SIZE`
`2048`
`HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS`
`0.6`
`HERMES_FEISHU_TEXT_BATCH_MAX_MESSAGES`
`8`
`HERMES_FEISHU_TEXT_BATCH_MAX_CHARS`
`4000`
`HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS`
`0.8`

WebSocket and per-group ACL settings are configured viaconfig.yamlunderplatforms.feishu.extra(seeWebSocket TuningandPer-Group Access Controlabove).

`config.yaml`
`platforms.feishu.extra`

## Troubleshooting​

| Problem | Fix |
| --- | --- |
| lark-oapi not installed | Install the SDK:pip install lark-oapi |
| websockets not installed; websocket mode unavailable | Install websockets:pip install websockets |
| aiohttp not installed; webhook mode unavailable | Install aiohttp:pip install aiohttp |
| FEISHU_APP_ID or FEISHU_APP_SECRET not set | Set both env vars or configure viahermes gateway setup |
| Another local Hermes gateway is already using this Feishu app_id | Only one Hermes instance can use the same app_id at a time. Stop the other gateway first. |
| Bot doesn't respond in groups | Ensure the bot is @mentioned, checkFEISHU_GROUP_POLICY, and verify the sender is inFEISHU_ALLOWED_USERSif policy isallowlist |
| Webhook rejected: invalid verification token | EnsureFEISHU_VERIFICATION_TOKENmatches the token in your Feishu app's Event Subscriptions config |
| Webhook rejected: invalid signature | EnsureFEISHU_ENCRYPT_KEYmatches the encrypt key in your Feishu app config |
| Post messages show as plain text | The Feishu API rejected the post payload; this is normal fallback behavior. Check logs for details. |
| Images/files not received by bot | Grantim:messageandim:resourcepermission scopes to your Feishu app |
| Bot identity not auto-detected | Usually a transient network issue reaching Feishu's bot info endpoint. SetFEISHU_BOT_OPEN_IDandFEISHU_BOT_NAMEmanually as a workaround. |
| Peer bot messages still ignored after enablingFEISHU_ALLOW_BOTS | Hermes can't identify itself yet — setFEISHU_BOT_OPEN_ID(andFEISHU_BOT_USER_IDif your app usessender_id_type=user_id). |
| Peer bots show asou_xxxxxxinstead of by name | Grant theapplication:bot.basic_info:readscope. |
| Error 200340 when clicking approval buttons | EnableInteractive Cardcapability and configureCard Request URLin the Feishu Developer Console. SeeRequired Feishu App Configurationabove. |
| Webhook rate limit exceeded | More than 120 requests/minute from the same IP. This is usually a misconfiguration or loop. |

`lark-oapi not installed`
`pip install lark-oapi`
`websockets not installed; websocket mode unavailable`
`pip install websockets`
`aiohttp not installed; webhook mode unavailable`
`pip install aiohttp`
`FEISHU_APP_ID or FEISHU_APP_SECRET not set`
`hermes gateway setup`
`Another local Hermes gateway is already using this Feishu app_id`
`FEISHU_GROUP_POLICY`
`FEISHU_ALLOWED_USERS`
`allowlist`
`Webhook rejected: invalid verification token`
`FEISHU_VERIFICATION_TOKEN`
`Webhook rejected: invalid signature`
`FEISHU_ENCRYPT_KEY`
`im:message`
`im:resource`
`FEISHU_BOT_OPEN_ID`
`FEISHU_BOT_NAME`
`FEISHU_ALLOW_BOTS`
`FEISHU_BOT_OPEN_ID`
`FEISHU_BOT_USER_ID`
`sender_id_type=user_id`
`ou_xxxxxx`
`application:bot.basic_info:read`
`Webhook rate limit exceeded`

## Toolset​

Feishu / Lark uses thehermes-feishuplatform preset, which includes the same core tools as Telegram and other gateway-based messaging platforms.

`hermes-feishu`