---
layout: docs
title: "Messaging_Mattermost"
permalink: /docs/user-guide/messaging_mattermost/
---

- 
- Messaging Platforms
- Other
- Mattermost

# Mattermost Setup

Hermes Agent integrates with Mattermost as a bot, letting you chat with your AI assistant through direct messages or team channels. Mattermost is a self-hosted, open-source Slack alternative — you run it on your own infrastructure, keeping full control of your data. The bot connects via Mattermost's REST API (v4) and WebSocket for real-time events, processes messages through the Hermes Agent pipeline (including tool use, memory, and reasoning), and responds in real time. It supports text, file attachments, images, and slash commands.

No external Mattermost library is required — the adapter usesaiohttp, which is already a Hermes dependency.

`aiohttp`

Before setup, here's the part most people want to know: how Hermes behaves once it's in your Mattermost instance.

## How Hermes Behaves​

| Context | Behavior |
| --- | --- |
| DMs | Hermes responds to every message. No@mentionneeded. Each DM has its own session. |
| Public/private channels | Hermes responds when you@mentionit. Without a mention, Hermes ignores the message. |
| Threads | IfMATTERMOST_REPLY_MODE=thread, Hermes replies in a thread under your message. Thread context stays isolated from the parent channel. |
| Shared channels with multiple users | By default, Hermes isolates session history per user inside the channel. Two people talking in the same channel do not share one transcript unless you explicitly disable that. |

`@mention`
`@mention`
`MATTERMOST_REPLY_MODE=thread`

If you want Hermes to reply as threaded conversations (nested under your original message), setMATTERMOST_REPLY_MODE=thread. The default isoff, which sends flat messages in the channel.

`MATTERMOST_REPLY_MODE=thread`
`off`

### Session Model in Mattermost​

By default:

- each DM gets its own session
- each thread gets its own session namespace
- each user in a shared channel gets their own session inside that channel

This is controlled byconfig.yaml:

`config.yaml`

```
group_sessions_per_user: true
```

Set it tofalseonly if you explicitly want one shared conversation for the entire channel:

`false`

```
group_sessions_per_user: false
```

Shared sessions can be useful for a collaborative channel, but they also mean:

- users share context growth and token costs
- one person's long tool-heavy task can bloat everyone else's context
- one person's in-flight run can interrupt another person's follow-up in the same channel

This guide walks you through the full setup process — from creating your bot on Mattermost to sending your first message.

## Step 1: Enable Bot Accounts​

Bot accounts must be enabled on your Mattermost server before you can create one.

1. Log in to Mattermost as aSystem Admin.
2. Go toSystem Console→Integrations→Bot Accounts.
3. SetEnable Bot Account Creationtotrue.
4. ClickSave.

If you don't have System Admin access, ask your Mattermost administrator to enable bot accounts and create one for you.

## Step 2: Create a Bot Account​

1. In Mattermost, click the☰menu (top-left) →Integrations→Bot Accounts.
2. ClickAdd Bot Account.
3. Fill in the details:Username: e.g.,hermesDisplay Name: e.g.,Hermes AgentDescription: optionalRole:Memberis sufficient
4. ClickCreate Bot Account.
5. Mattermost will display thebot token.Copy it immediately.

- Username: e.g.,hermes
- Display Name: e.g.,Hermes Agent
- Description: optional
- Role:Memberis sufficient

`hermes`
`Hermes Agent`
`Member`

The bot token is only displayed once when you create the bot account. If you lose it, you'll need to regenerate it from the bot account settings. Never share your token publicly or commit it to Git — anyone with this token has full control of the bot.

Store the token somewhere safe (a password manager, for example). You'll need it in Step 5.

You can also use apersonal access tokeninstead of a bot account. Go toProfile→Security→Personal Access Tokens→Create Token. This is useful if you want Hermes to post as your own user rather than a separate bot user.

## Step 3: Add the Bot to Channels​

The bot needs to be a member of any channel where you want it to respond:

1. Open the channel where you want the bot.
2. Click the channel name →Add Members.
3. Search for your bot username (e.g.,hermes) and add it.

`hermes`

For DMs, simply open a direct message with the bot — it will be able to respond immediately.

## Step 4: Find Your Mattermost User ID​

Hermes Agent uses your Mattermost User ID to control who can interact with the bot. To find it:

1. Click youravatar(top-left corner) →Profile.
2. Your User ID is displayed in the profile dialog — click it to copy.

Your User ID is a 26-character alphanumeric string like3uo8dkh1p7g1mfk49ear5fzs5c.

`3uo8dkh1p7g1mfk49ear5fzs5c`

Your User ID isnotyour username. The username is what appears after@(e.g.,@alice). The User ID is a long alphanumeric identifier that Mattermost uses internally.

`@`
`@alice`

Alternative: You can also get your User ID via the API:

```
curl -H "Authorization: Bearer YOUR_TOKEN" \  https://your-mattermost-server/api/v4/users/me | jq .id
```

To get aChannel ID: click the channel name →View Info. The Channel ID is shown in the info panel. You'll need this if you want to set a home channel manually.

## Step 5: Configure Hermes Agent​

### Option A: Interactive Setup (Recommended)​

Run the guided setup command:

```
hermes gateway setup
```

SelectMattermostwhen prompted, then paste your server URL, bot token, and user ID when asked.

### Option B: Manual Configuration​

Add the following to your~/.hermes/.envfile:

`~/.hermes/.env`

```
# RequiredMATTERMOST_URL=https://mm.example.comMATTERMOST_TOKEN=***MATTERMOST_ALLOWED_USERS=3uo8dkh1p7g1mfk49ear5fzs5c# Multiple allowed users (comma-separated)# MATTERMOST_ALLOWED_USERS=3uo8dkh1p7g1mfk49ear5fzs5c,8fk2jd9s0a7bncm1xqw4tp6r3e# Optional: reply mode (thread or off, default: off)# MATTERMOST_REPLY_MODE=thread# Optional: respond without @mention (default: true = require mention)# MATTERMOST_REQUIRE_MENTION=false# Optional: channels where bot responds without @mention (comma-separated channel IDs)# MATTERMOST_FREE_RESPONSE_CHANNELS=channel_id_1,channel_id_2
```

Optional behavior settings in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
group_sessions_per_user: true
```

- group_sessions_per_user: truekeeps each participant's context isolated inside shared channels and threads

`group_sessions_per_user: true`

### Start the Gateway​

Once configured, start the Mattermost gateway:

```
hermes gateway
```

The bot should connect to your Mattermost server within a few seconds. Send it a message — either a DM or in a channel where it's been added — to test.

You can runhermes gatewayin the background or as a systemd service for persistent operation. See the deployment docs for details.

`hermes gateway`

## Home Channel​

You can designate a "home channel" where the bot sends proactive messages (such as cron job output, reminders, and notifications). There are two ways to set it:

### Using the Slash Command​

Type/sethomein any Mattermost channel where the bot is present. That channel becomes the home channel.

`/sethome`

### Manual Configuration​

Add this to your~/.hermes/.env:

`~/.hermes/.env`

```
MATTERMOST_HOME_CHANNEL=abc123def456ghi789jkl012mn
```

Replace the ID with the actual channel ID (click the channel name → View Info → copy the ID).

## Reply Mode​

TheMATTERMOST_REPLY_MODEsetting controls how Hermes posts responses:

`MATTERMOST_REPLY_MODE`
| Mode | Behavior |
| --- | --- |
| off(default) | Hermes posts flat messages in the channel, like a normal user. |
| thread | Hermes replies in a thread under your original message. Keeps channels clean when there's lots of back-and-forth. |

`off`
`thread`

Set it in your~/.hermes/.env:

`~/.hermes/.env`

```
MATTERMOST_REPLY_MODE=thread
```

## Mention Behavior​

By default, the bot only responds in channels when@mentioned. You can change this:

`@mentioned`
| Variable | Default | Description |
| --- | --- | --- |
| MATTERMOST_REQUIRE_MENTION | true | Set tofalseto respond to all messages in channels (DMs always work). |
| MATTERMOST_FREE_RESPONSE_CHANNELS | (none) | Comma-separated channel IDs where the bot responds without@mention, even when require_mention is true. |

`MATTERMOST_REQUIRE_MENTION`
`true`
`false`
`MATTERMOST_FREE_RESPONSE_CHANNELS`
`@mention`

To find a channel ID in Mattermost: open the channel, click the channel name header, and look for the ID in the URL or channel details.

When the bot is@mentioned, the mention is automatically stripped from the message before processing.

`@mentioned`

## Channel allowlist (allowed_channels)​

`allowed_channels`

Restrict the bot to a fixed set of Mattermost channels. When set, the botonlyresponds in channels whose ID appears in the list — messages from any other channel are silently ignored, even if the bot is@mentioned.

`@mentioned`

DMs are exemptfrom this filter, so authorized users can always reach the bot in a direct message.

```
mattermost:  allowed_channels:    - "abc123def456ghi789jkl012mno"   # #ops    - "xyz987uvw654rst321opq098nml"   # #incident-response
```

Or via env var (comma-separated):

```
MATTERMOST_ALLOWED_CHANNELS="abc123def456ghi789jkl012mno,xyz987uvw654rst321opq098nml"
```

Behavior:

- Empty / unset → no restriction (fully backward compatible).
- Non-empty → channel ID must be on the list, or the message is dropped before any other gating (mention requirement,MATTERMOST_FREE_RESPONSE_CHANNELS, etc.) runs.
- Find a channel ID via the Mattermost UI → channel header → "View Info", or read it from the channel URL.

`MATTERMOST_FREE_RESPONSE_CHANNELS`

See also:admin/user slash command split.

## Troubleshooting​

### Bot is not responding to messages​

Cause: The bot is not a member of the channel, orMATTERMOST_ALLOWED_USERSdoesn't include your User ID.

`MATTERMOST_ALLOWED_USERS`

Fix: Add the bot to the channel (channel name → Add Members → search for the bot). Verify your User ID is inMATTERMOST_ALLOWED_USERS. Restart the gateway.

`MATTERMOST_ALLOWED_USERS`

### 403 Forbidden errors​

Cause: The bot token is invalid, or the bot doesn't have permission to post in the channel.

Fix: Check thatMATTERMOST_TOKENin your.envfile is correct. Make sure the bot account hasn't been deactivated. Verify the bot has been added to the channel. If using a personal access token, ensure your account has the required permissions.

`MATTERMOST_TOKEN`
`.env`

### WebSocket disconnects / reconnection loops​

Cause: Network instability, Mattermost server restarts, or firewall/proxy issues with WebSocket connections.

Fix: The adapter automatically reconnects with exponential backoff (2s → 60s). Check your server's WebSocket configuration — reverse proxies (nginx, Apache) need WebSocket upgrade headers configured. Verify no firewall is blocking WebSocket connections on your Mattermost server.

For nginx, ensure your config includes:

```
location /api/v4/websocket {    proxy_pass http://mattermost-backend;    proxy_set_header Upgrade $http_upgrade;    proxy_set_header Connection "upgrade";    proxy_read_timeout 600s;}
```

### "Failed to authenticate" on startup​

Cause: The token or server URL is incorrect.

Fix: VerifyMATTERMOST_URLpoints to your Mattermost server (includehttps://, no trailing slash). Check thatMATTERMOST_TOKENis valid — try it with curl:

`MATTERMOST_URL`
`https://`
`MATTERMOST_TOKEN`

```
curl -H "Authorization: Bearer YOUR_TOKEN" \  https://your-server/api/v4/users/me
```

If this returns your bot's user info, the token is valid. If it returns an error, regenerate the token.

### Bot is offline​

Cause: The Hermes gateway isn't running, or it failed to connect.

Fix: Check thathermes gatewayis running. Look at the terminal output for error messages. Common issues: wrong URL, expired token, Mattermost server unreachable.

`hermes gateway`

### "User not allowed" / Bot ignores you​

Cause: Your User ID isn't inMATTERMOST_ALLOWED_USERS.

`MATTERMOST_ALLOWED_USERS`

Fix: Add your User ID toMATTERMOST_ALLOWED_USERSin~/.hermes/.envand restart the gateway. Remember: the User ID is a 26-character alphanumeric string, not your@username.

`MATTERMOST_ALLOWED_USERS`
`~/.hermes/.env`
`@username`

## Per-Channel Prompts​

Assign ephemeral system prompts to specific Mattermost channels. The prompt is injected at runtime on every turn — never persisted to transcript history — so changes take effect immediately.

```
mattermost:  channel_prompts:    "channel_id_abc123": |      You are a research assistant. Focus on academic sources,      citations, and concise synthesis.    "channel_id_def456": |      Code review mode. Be precise about edge cases and      performance implications.
```

Keys are Mattermost channel IDs (find them in the channel URL or via the API). All messages in the matching channel get the prompt injected as an ephemeral system instruction.

## Security​

Always setMATTERMOST_ALLOWED_USERSto restrict who can interact with the bot. Without it, the gateway denies all users by default as a safety measure. Only add User IDs of people you trust — authorized users have full access to the agent's capabilities, including tool use and system access.

`MATTERMOST_ALLOWED_USERS`

For more information on securing your Hermes Agent deployment, see theSecurity Guide.

## Notes​

- Self-hosted friendly: Works with any self-hosted Mattermost instance. No Mattermost Cloud account or subscription required.
- No extra dependencies: The adapter usesaiohttpfor HTTP and WebSocket, which is already included with Hermes Agent.
- Team Edition compatible: Works with both Mattermost Team Edition (free) and Enterprise Edition.

`aiohttp`