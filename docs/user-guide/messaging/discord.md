---
layout: docs
title: "Messaging_Discord"
permalink: /docs/user-guide/messaging_discord/
---

- 
- Messaging Platforms
- Popular
- Discord

# Discord Setup

Hermes Agent integrates with Discord as a bot, letting you chat with your AI assistant through direct messages or server channels. The bot receives your messages, processes them through the Hermes Agent pipeline (including tool use, memory, and reasoning), and responds in real time. It supports text, voice messages, file attachments, and slash commands.

Before setup, here's the part most people want to know: how Hermes behaves once it's in your server.

## How Hermes Behaves​

| Context | Behavior |
| --- | --- |
| DMs | Hermes responds to every message. No@mentionneeded. Each DM has its own session. |
| Server channels | By default, Hermes only responds when you@mentionit. If you post in a channel without mentioning it, Hermes ignores the message. |
| Free-response channels | You can make specific channels mention-free withDISCORD_FREE_RESPONSE_CHANNELS, or disable mentions globally withDISCORD_REQUIRE_MENTION=false. Messages in these channels are answered inline — auto-threading is skipped so the channel stays a lightweight chat. |
| Threads | Hermes replies in the same thread. Mention rules still apply unless that thread or its parent channel is configured as free-response. Threads stay isolated from the parent channel for session history. |
| Shared channels with multiple users | By default, Hermes isolates session history per user inside the channel for safety and clarity. Two people talking in the same channel do not share one transcript unless you explicitly disable that. |
| Messages mentioning other users | WhenDISCORD_IGNORE_NO_MENTIONistrue(the default), Hermes stays silent if a message @mentions other users but doesnotmention the bot. This prevents the bot from jumping into conversations directed at other people. Set tofalseif you want the bot to respond to all messages regardless of who is mentioned. This only applies in server channels, not DMs. |

`@mention`
`@mention`
`DISCORD_FREE_RESPONSE_CHANNELS`
`DISCORD_REQUIRE_MENTION=false`
`DISCORD_IGNORE_NO_MENTION`
`true`
`false`

If you want a normal bot-help channel where people can talk to Hermes without tagging it every time, add that channel toDISCORD_FREE_RESPONSE_CHANNELS.

`DISCORD_FREE_RESPONSE_CHANNELS`

### Discord Gateway Model​

Hermes on Discord is not a webhook that replies statelessly. It runs through the full messaging gateway, which means each incoming message goes through:

1. authorization (DISCORD_ALLOWED_USERS)
2. mention / free-response checks
3. session lookup
4. session transcript loading
5. normal Hermes agent execution, including tools, memory, and slash commands
6. response delivery back to Discord

`DISCORD_ALLOWED_USERS`

That matters because behavior in a busy server depends on both Discord routing and Hermes session policy.

### Session Model in Discord​

By default:

- each DM gets its own session
- each server thread gets its own session namespace
- each user in a shared channel gets their own session inside that channel

So if Alice and Bob both talk to Hermes in#research, Hermes treats those as separate conversations by default even though they are using the same visible Discord channel.

`#research`

This is controlled byconfig.yaml:

`config.yaml`

```
group_sessions_per_user: true
```

Set it tofalseonly if you explicitly want one shared conversation for the entire room:

`false`

```
group_sessions_per_user: false
```

Shared sessions can be useful for a collaborative room, but they also mean:

- users share context growth and token costs
- one person's long tool-heavy task can bloat everyone else's context
- one person's in-flight run can interrupt another person's follow-up in the same room

### Interrupts and Concurrency​

Hermes tracks running agents by session key.

With the defaultgroup_sessions_per_user: true:

`group_sessions_per_user: true`
- Alice interrupting her own in-flight request only affects Alice's session in that channel
- Bob can keep talking in the same channel without inheriting Alice's history or interrupting Alice's run

Withgroup_sessions_per_user: false:

`group_sessions_per_user: false`
- the whole room shares one running-agent slot for that channel/thread
- follow-up messages from different people can interrupt or queue behind each other

This guide walks you through the full setup process — from creating your bot on Discord's Developer Portal to sending your first message.

## Step 1: Create a Discord Application​

1. Go to theDiscord Developer Portaland sign in with your Discord account.
2. ClickNew Applicationin the top-right corner.
3. Enter a name for your application (e.g., "Hermes Agent") and accept the Developer Terms of Service.
4. ClickCreate.

You'll land on theGeneral Informationpage. Note theApplication ID— you'll need it later to build the invite URL.

## Step 2: Create the Bot​

1. In the left sidebar, clickBot.
2. Discord automatically creates a bot user for your application. You'll see the bot's username, which you can customize.
3. UnderAuthorization Flow:SetPublic BottoON— required to use the Discord-provided invite link (recommended). This allows the Installation tab to generate a default authorization URL.LeaveRequire OAuth2 Code Grantset toOFF.

- SetPublic BottoON— required to use the Discord-provided invite link (recommended). This allows the Installation tab to generate a default authorization URL.
- LeaveRequire OAuth2 Code Grantset toOFF.

You can set a custom avatar and banner for your bot on this page. This is what users will see in Discord.

If you prefer to keep your bot private (Public Bot = OFF), youmustuse theManual URLmethod in Step 5 instead of the Installation tab. The Discord-provided link requires Public Bot to be enabled.

## Step 3: Enable Privileged Gateway Intents​

This is the most critical step in the entire setup. Without the correct intents enabled, your bot will connect to Discord butwill not be able to read message content.

On theBotpage, scroll down toPrivileged Gateway Intents. You'll see three toggles:

| Intent | Purpose | Required? |
| --- | --- | --- |
| Presence Intent | See user online/offline status | Optional |
| Server Members Intent | Access the member list, resolve usernames | Required |
| Message Content Intent | Read the text content of messages | Required |

Enable both Server Members Intent and Message Content Intentby toggling themON.

- WithoutMessage Content Intent, your bot receives message events but the message text is empty — the bot literally cannot see what you typed.
- WithoutServer Members Intent, the bot cannot resolve usernames for the allowed users list and may fail to identify who is messaging it.

If your bot is online but never responds to messages, theMessage Content Intentis almost certainly disabled. Go back to theDeveloper Portal, select your application → Bot → Privileged Gateway Intents, and make sureMessage Content Intentis toggled ON. ClickSave Changes.

Regarding server count:

- If your bot is infewer than 100 servers, you can simply toggle intents on and off freely.
- If your bot is in100 or more servers, Discord requires you to submit a verification application to use privileged intents. For personal use, this is not a concern.

ClickSave Changesat the bottom of the page.

## Step 4: Get the Bot Token​

The bot token is the credential Hermes Agent uses to log in as your bot. Still on theBotpage:

1. Under theTokensection, clickReset Token.
2. If you have two-factor authentication enabled on your Discord account, enter your 2FA code.
3. Discord will display your new token.Copy it immediately.

The token is only displayed once. If you lose it, you'll need to reset it and generate a new one. Never share your token publicly or commit it to Git — anyone with this token has full control of your bot.

Store the token somewhere safe (a password manager, for example). You'll need it in Step 8.

## Step 5: Generate the Invite URL​

You need an OAuth2 URL to invite the bot to your server. There are two ways to do this:

### Option A: Using the Installation Tab (Recommended)​

This method requiresPublic Botto be set toONin Step 2. If you set Public Bot to OFF, use the Manual URL method below instead.

1. In the left sidebar, clickInstallation.
2. UnderInstallation Contexts, enableGuild Install.
3. ForInstall Link, selectDiscord Provided Link.
4. UnderDefault Install Settingsfor Guild Install:Scopes: selectbotandapplications.commandsPermissions: select the permissions listed below.

- Scopes: selectbotandapplications.commands
- Permissions: select the permissions listed below.

`bot`
`applications.commands`

### Option B: Manual URL​

You can construct the invite URL directly using this format:

```
https://discord.com/oauth2/authorize?client_id=YOUR_APP_ID&scope=bot+applications.commands&permissions=274878286912
```

ReplaceYOUR_APP_IDwith the Application ID from Step 1.

`YOUR_APP_ID`

### Required Permissions​

These are the minimum permissions your bot needs:

- View Channels— see the channels it has access to
- Send Messages— respond to your messages
- Embed Links— format rich responses
- Attach Files— send images, audio, and file outputs
- Read Message History— maintain conversation context

### Recommended Additional Permissions​

- Send Messages in Threads— respond in thread conversations
- Add Reactions— react to messages for acknowledgment

### Permission Integers​

| Level | Permissions Integer | What's Included |
| --- | --- | --- |
| Minimal | 117760 | View Channels, Send Messages, Read Message History, Attach Files |
| Recommended | 274878286912 | All of the above plus Embed Links, Send Messages in Threads, Add Reactions |

`117760`
`274878286912`

## Step 6: Invite to Your Server​

1. Open the invite URL in your browser (from the Installation tab or the manual URL you constructed).
2. In theAdd to Serverdropdown, select your server.
3. ClickContinue, thenAuthorize.
4. Complete the CAPTCHA if prompted.

You need theManage Serverpermission on the Discord server to invite a bot. If you don't see your server in the dropdown, ask a server admin to use the invite link instead.

After authorizing, the bot will appear in your server's member list (it will show as offline until you start the Hermes gateway).

## Step 7: Find Your Discord User ID​

Hermes Agent uses your Discord User ID to control who can interact with the bot. To find it:

1. Open Discord (desktop or web app).
2. Go toSettings→Advanced→ toggleDeveloper ModetoON.
3. Close settings.
4. Right-click your own username (in a message, the member list, or your profile) →Copy User ID.

Your User ID is a long number like284102345871466496.

`284102345871466496`

Developer Mode also lets you copyChannel IDsandServer IDsthe same way — right-click the channel or server name and select Copy ID. You'll need a Channel ID if you want to set a home channel manually.

## Step 8: Configure Hermes Agent​

### Option A: Interactive Setup (Recommended)​

Run the guided setup command:

```
hermes gateway setup
```

SelectDiscordwhen prompted, then paste your bot token and user ID when asked.

### Option B: Manual Configuration​

Add the following to your~/.hermes/.envfile:

`~/.hermes/.env`

```
# RequiredDISCORD_BOT_TOKEN=your-bot-tokenDISCORD_ALLOWED_USERS=284102345871466496# Multiple allowed users (comma-separated)# DISCORD_ALLOWED_USERS=284102345871466496,198765432109876543
```

Then start the gateway:

```
hermes gateway
```

The bot should come online in Discord within a few seconds. Send it a message — either a DM or in a channel it can see — to test.

You can runhermes gatewayin the background or as a systemd service for persistent operation. See the deployment docs for details.

`hermes gateway`

## Configuration Reference​

Discord behavior is controlled through two files:~/.hermes/.envfor credentials and env-level toggles, and~/.hermes/config.yamlfor structured settings. Environment variables always take precedence over config.yaml values when both are set.

`~/.hermes/.env`
`~/.hermes/config.yaml`

### Environment Variables (.env)​

`.env`
| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| DISCORD_BOT_TOKEN | Yes | — | Bot token from theDiscord Developer Portal. |
| DISCORD_ALLOWED_USERS | Conditional | — | Comma-separated Discord user IDs allowed to interact with the bot. Without thisorDISCORD_ALLOWED_ROLES, the gateway denies all users unlessDISCORD_ALLOW_ALL_USERS=true,GATEWAY_ALLOW_ALL_USERS=true, orDISCORD_ALLOWED_CHANNELSexplicitly scopes guild access. |
| DISCORD_ALLOWED_ROLES | No | — | Comma-separated Discord role IDs. Any member with one of these roles is authorized — OR semantics withDISCORD_ALLOWED_USERS. Auto-enables theServer Members Intenton connect. Useful when moderation teams churn: new mods get access as soon as the role is granted, no config push needed. |
| DISCORD_ALLOW_ALL_USERS | No | false | Explicit opt-in to allow every Discord user who can reach the bot. This restores the pre-0.18 open behavior for Discord only; use only for trusted/private guilds or development. |
| GATEWAY_ALLOW_ALL_USERS | No | false | Global allow-all opt-in for every gateway platform. Prefer the platform-specificDISCORD_ALLOW_ALL_USERSunless you intentionally want all connected platforms open. |
| DISCORD_HOME_CHANNEL | No | — | Channel ID where the bot sends proactive messages (cron output, reminders, notifications). |
| DISCORD_HOME_CHANNEL_NAME | No | "Home" | Display name for the home channel in logs and status output. |
| DISCORD_COMMAND_SYNC_POLICY | No | "safe" | Controls native slash-command startup sync."safe"diffs existing global commands and only updates what changed, recreating commands when Discord metadata changes cannot be applied via patch."bulk"preserves the oldtree.sync()behavior."off"skips startup sync entirely. |
| DISCORD_REQUIRE_MENTION | No | true | Whentrue, the bot only responds in server channels when@mentioned. Set tofalseto respond to all messages in every channel. |
| DISCORD_THREAD_REQUIRE_MENTION | No | false | Whentrue, the in-thread mention shortcut is disabled — threads are gated the same as channels, requiring@mentioneven after the bot has already participated. Use this when multiple bots share a thread and you want each to fire only on explicit@mention. |
| DISCORD_FREE_RESPONSE_CHANNELS | No | — | Comma-separated channel IDs where the bot responds without requiring an@mention, even whenDISCORD_REQUIRE_MENTIONistrue. |
| DISCORD_IGNORE_NO_MENTION | No | true | Whentrue, the bot stays silent if a message@mentionsother users but doesnotmention the bot. Prevents the bot from jumping into conversations directed at other people. Only applies in server channels, not DMs. |
| DISCORD_AUTO_THREAD | No | true | Whentrue, automatically creates a new thread for every@mentionin a text channel, so each conversation is isolated (similar to Slack behavior). Messages already inside threads or DMs are unaffected. |
| DISCORD_ALLOW_BOTS | No | "none" | Controls how the bot handles messages from other Discord bots."none"— ignore all other bots."mentions"— only accept bot messages that@mentionHermes."all"— accept all bot messages. |
| DISCORD_REACTIONS | No | true | Whentrue, the bot adds emoji reactions to messages during processing (👀 when starting, ✅ on success, ❌ on error). Set tofalseto disable reactions entirely. |
| DISCORD_IGNORED_CHANNELS | No | — | Comma-separated channel IDs where the botneverresponds, even when@mentioned. Takes priority over all other channel settings. |
| DISCORD_ALLOWED_CHANNELS | No | — | Comma-separated channel IDs. When set, the botonlyresponds in these channels (plus DMs if allowed). Overridesconfig.yamldiscord.allowed_channels. Combine withDISCORD_IGNORED_CHANNELSto express allow/deny rules. |
| DISCORD_NO_THREAD_CHANNELS | No | — | Comma-separated channel IDs where the bot responds directly in the channel instead of creating a thread. Only relevant whenDISCORD_AUTO_THREADistrue. |
| DISCORD_HISTORY_BACKFILL | No | true | Whentrue, prepend recent channel scrollback (since the bot's last response) to the user message when the bot is mentioned. Recovers context the bot would otherwise miss withrequire_mention. Skipped in DMs and free-response channels. Set tofalseto disable. |
| DISCORD_HISTORY_BACKFILL_LIMIT | No | 50 | Maximum number of messages to scan backwards when assembling the backfill block. In practice the scan usually stops earlier — at the bot's own last message in the channel. |
| DISCORD_REPLY_TO_MODE | No | "first" | Controls reply-reference behavior:"off"— never reply to the original message,"first"— reply-reference on the first message chunk only (default),"all"— reply-reference on every chunk. |
| DISCORD_ALLOW_MENTION_EVERYONE | No | false | Whenfalse(default), the bot cannot ping@everyoneor@hereeven if its response contains those tokens. Set totrueto opt back in. SeeMention Controlbelow. |
| DISCORD_ALLOW_MENTION_ROLES | No | false | Whenfalse(default), the bot cannot ping@rolementions. Set totrueto allow. |
| DISCORD_ALLOW_MENTION_USERS | No | true | Whentrue(default), the bot can ping individual users by ID. |
| DISCORD_ALLOW_MENTION_REPLIED_USER | No | true | Whentrue(default), replying to a message pings the original author. |
| DISCORD_PROXY | No | — | Proxy URL for Discord connections (HTTP, WebSocket, REST). OverridesHTTPS_PROXY/ALL_PROXY. Supportshttp://,https://, andsocks5://schemes. |
| DISCORD_ALLOW_ANY_ATTACHMENT | No | false | Whentrue, the bot accepts attachments of any file type (not just the built-in PDF/text/zip/office allowlist). Unknown types are cached to disk and surfaced to the agent as a local path withapplication/octet-streamMIME so it can inspect them withterminal/read_file/ffprobe/ etc. |
| DISCORD_MAX_ATTACHMENT_BYTES | No | 33554432 | Maximum bytes per attachment the gateway will download and cache. Default 32 MiB. Set to0for no cap (attachments are held in memory while being written, so unlimited carries a real memory cost). |
| HERMES_DISCORD_TEXT_BATCH_DELAY_SECONDS | No | 0.6 | Grace window the adapter waits before flushing a queued text chunk. Useful for smoothing streamed output. |
| HERMES_DISCORD_TEXT_BATCH_SPLIT_DELAY_SECONDS | No | 2.0 | Delay between split chunks when a single message exceeds Discord's length limit. |

`DISCORD_BOT_TOKEN`
`DISCORD_ALLOWED_USERS`
`DISCORD_ALLOWED_ROLES`
`DISCORD_ALLOW_ALL_USERS=true`
`GATEWAY_ALLOW_ALL_USERS=true`
`DISCORD_ALLOWED_CHANNELS`
`DISCORD_ALLOWED_ROLES`
`DISCORD_ALLOWED_USERS`
`DISCORD_ALLOW_ALL_USERS`
`false`
`GATEWAY_ALLOW_ALL_USERS`
`false`
`DISCORD_ALLOW_ALL_USERS`
`DISCORD_HOME_CHANNEL`
`DISCORD_HOME_CHANNEL_NAME`
`"Home"`
`DISCORD_COMMAND_SYNC_POLICY`
`"safe"`
`"safe"`
`"bulk"`
`tree.sync()`
`"off"`
`DISCORD_REQUIRE_MENTION`
`true`
`true`
`@mentioned`
`false`
`DISCORD_THREAD_REQUIRE_MENTION`
`false`
`true`
`@mention`
`@mention`
`DISCORD_FREE_RESPONSE_CHANNELS`
`@mention`
`DISCORD_REQUIRE_MENTION`
`true`
`DISCORD_IGNORE_NO_MENTION`
`true`
`true`
`@mentions`
`DISCORD_AUTO_THREAD`
`true`
`true`
`@mention`
`DISCORD_ALLOW_BOTS`
`"none"`
`"none"`
`"mentions"`
`@mention`
`"all"`
`DISCORD_REACTIONS`
`true`
`true`
`false`
`DISCORD_IGNORED_CHANNELS`
`@mentioned`
`DISCORD_ALLOWED_CHANNELS`
`config.yaml`
`discord.allowed_channels`
`DISCORD_IGNORED_CHANNELS`
`DISCORD_NO_THREAD_CHANNELS`
`DISCORD_AUTO_THREAD`
`true`
`DISCORD_HISTORY_BACKFILL`
`true`
`true`
`require_mention`
`false`
`DISCORD_HISTORY_BACKFILL_LIMIT`
`50`
`DISCORD_REPLY_TO_MODE`
`"first"`
`"off"`
`"first"`
`"all"`
`DISCORD_ALLOW_MENTION_EVERYONE`
`false`
`false`
`@everyone`
`@here`
`true`
`DISCORD_ALLOW_MENTION_ROLES`
`false`
`false`
`@role`
`true`
`DISCORD_ALLOW_MENTION_USERS`
`true`
`true`
`DISCORD_ALLOW_MENTION_REPLIED_USER`
`true`
`true`
`DISCORD_PROXY`
`HTTPS_PROXY`
`ALL_PROXY`
`http://`
`https://`
`socks5://`
`DISCORD_ALLOW_ANY_ATTACHMENT`
`false`
`true`
`application/octet-stream`
`terminal`
`read_file`
`ffprobe`
`DISCORD_MAX_ATTACHMENT_BYTES`
`33554432`
`0`
`HERMES_DISCORD_TEXT_BATCH_DELAY_SECONDS`
`0.6`
`HERMES_DISCORD_TEXT_BATCH_SPLIT_DELAY_SECONDS`
`2.0`

DISCORD_ALLOW_BOTSexists to accept input from a specific trusted bot (e.g. a relay or webhook bot), not to let two Hermes profiles talk to each other. The default,"none", ignores all other bots and is the safe setting.

`DISCORD_ALLOW_BOTS`
`"none"`

Wiring multiple Hermes profiles to reply to one another in a shared channel — by setting"mentions"or"all"across several profiles — is an unsupported topology. Discord auto-@mentionsthe replied-to author on every reply, so under"mentions"two bots will satisfy each other's mention gate indefinitely and ack-loop. There is no circuit breaker for this because the supported configuration is simply to leaveDISCORD_ALLOW_BOTSat"none". If you must accept a particular bot, scope the acceptance narrowly and never to another auto-replying agent.

`"mentions"`
`"all"`
`@mentions`
`"mentions"`
`DISCORD_ALLOW_BOTS`
`"none"`

### Config File (config.yaml)​

`config.yaml`

Thediscordsection in~/.hermes/config.yamlmirrors the env vars above. Config.yaml settings are applied as defaults — if the equivalent env var is already set, the env var wins.

`discord`
`~/.hermes/config.yaml`

```
# Discord-specific settingsdiscord:  require_mention: true           # Require @mention in server channels  thread_require_mention: false   # If true, require @mention in threads too (multi-bot threads)  free_response_channels: ""      # Comma-separated channel IDs (or YAML list)  auto_thread: true               # Auto-create threads on @mention  reactions: true                 # Add emoji reactions during processing  ignored_channels: []            # Channel IDs where bot never responds  no_thread_channels: []          # Channel IDs where bot responds without threading  history_backfill: true          # Prepend recent channel scrollback on mention (default: true)  history_backfill_limit: 50      # Max messages to scan backwards (default: 50)  channel_prompts: {}             # Per-channel ephemeral system prompts  allow_mentions:                 # What the bot is allowed to ping (safe defaults)    everyone: false               # @everyone / @here pings (default: false)    roles: false                  # @role pings (default: false)    users: true                   # @user pings (default: true)    replied_user: true            # reply-reference pings the author (default: true)# Session isolation (applies to all gateway platforms, not just Discord)group_sessions_per_user: true     # Isolate sessions per user in shared channels
```

#### discord.require_mention​

`discord.require_mention`

Type:boolean —Default:true

`true`

When enabled, the bot only responds in server channels when directly@mentioned. DMs always get a response regardless of this setting.

`@mentioned`

#### discord.thread_require_mention​

`discord.thread_require_mention`

Type:boolean —Default:false

`false`

By default, once the bot has participated in a thread (auto-created on@mentionor replied in once), it keeps responding to every subsequent message in that thread without needing to be@mentionedagain. That's the right default for one-on-one conversations.

`@mention`
`@mentioned`

Inmulti-bot threadswhere users address one bot per turn, this default becomes a footgun — every other bot in the thread also fires on every message, burning credits and spamming the channel. Setthread_require_mention: trueto disable the in-thread shortcut and gate threads the same way channels are gated. Explicit@mentionsstill work as before.

`thread_require_mention: true`
`@mentions`

```
discord:  require_mention: true  thread_require_mention: true    # multi-bot setup
```

#### discord.free_response_channels​

`discord.free_response_channels`

Type:string or list —Default:""

`""`

Channel IDs where the bot responds to all messages without needing an@mention. Accepts either a comma-separated string or a YAML list:

`@mention`

```
# String formatdiscord:  free_response_channels: "1234567890,9876543210"# List formatdiscord:  free_response_channels:    - 1234567890    - 9876543210
```

If a thread's parent channel is in this list, the thread also becomes mention-free.

Free-response channels alsoskip auto-threading— the bot replies inline rather than spinning off a new thread per message. This keeps the channel usable as a lightweight chat surface. If you want threading behavior, don't list the channel as free-response (use normal@mentionflow instead).

`@mention`

#### discord.auto_thread​

`discord.auto_thread`

Type:boolean —Default:true

`true`

When enabled, every@mentionin a regular text channel automatically creates a new thread for the conversation. This keeps the main channel clean and gives each conversation its own isolated session history. Once a thread is created, subsequent messages in that thread don't require@mention— the bot knows it's already participating. Setthread_require_mentiontotrueto disable this in-thread shortcut for multi-bot setups.

`@mention`
`@mention`
`thread_require_mention`
`true`

Messages sent in existing threads or DMs are unaffected by this setting. Channels listed indiscord.free_response_channelsordiscord.no_thread_channelsalso bypass auto-threading and get inline replies instead.

`discord.free_response_channels`
`discord.no_thread_channels`

#### discord.reactions​

`discord.reactions`

Type:boolean —Default:true

`true`

Controls whether the bot adds emoji reactions to messages as visual feedback:

- 👀 added when the bot starts processing your message
- ✅ added when the response is delivered successfully
- ❌ added if an error occurs during processing

Disable this if you find the reactions distracting or if the bot's role doesn't have theAdd Reactionspermission.

#### discord.ignored_channels​

`discord.ignored_channels`

Type:string or list —Default:[]

`[]`

Channel IDs where the botneverresponds, even when directly@mentioned. This takes the highest priority — if a channel is in this list, the bot silently ignores all messages there, regardless ofrequire_mention,free_response_channels, or any other setting.

`@mentioned`
`require_mention`
`free_response_channels`

```
# String formatdiscord:  ignored_channels: "1234567890,9876543210"# List formatdiscord:  ignored_channels:    - 1234567890    - 9876543210
```

If a thread's parent channel is in this list, messages in that thread are also ignored.

#### discord.no_thread_channels​

`discord.no_thread_channels`

Type:string or list —Default:[]

`[]`

Channel IDs where the bot responds directly in the channel instead of auto-creating a thread. This only has an effect whenauto_threadistrue(the default). In these channels, the bot responds inline like a normal message rather than spawning a new thread.

`auto_thread`
`true`

```
discord:  no_thread_channels:    - 1234567890  # Bot responds inline here
```

Useful for channels dedicated to bot interaction where threads would add unnecessary noise.

#### discord.channel_prompts​

`discord.channel_prompts`

Type:mapping —Default:{}

`{}`

Per-channel ephemeral system prompts that are injected on every turn in the matching Discord channel or thread without being persisted to transcript history.

```
discord:  channel_prompts:    "1234567890": |      This channel is for research tasks. Prefer deep comparisons,      citations, and concise synthesis.    "9876543210": |      This forum is for therapy-style support. Be warm, grounded,      and non-judgmental.
```

Behavior:

- Exact thread/channel ID matches win.
- If a message arrives inside a thread or forum post and that thread has no explicit entry, Hermes falls back to the parent channel/forum ID.
- Prompts are applied ephemerally at runtime, so changing them affects future turns immediately without rewriting past session history.

#### discord.history_backfill​

`discord.history_backfill`

Type:boolean —Default:true

`true`

When enabled, the bot recovers missed channel messages on each@mention. Withrequire_mention: true, the bot only processes messages that tag it directly — everything else in the channel is invisible to the session transcript. History backfill scans backwards through recent channel history when triggered, collecting messages between the bot's last response and the current mention, and includes them as context.

`@mention`
`require_mention: true`

Behavior by surface:

- Server channels(withrequire_mention: true): backfill scans the channel since the bot's last response. Useful when other participants posted while the bot wasn't addressed.
- Threads: backfill scans the thread only — Discord'schannel.history()on a thread returns only that thread's messages, not the parent channel. This is the right scope because threads are usually self-contained conversations.
- DMs: skipped. Every DM message triggers the bot, so the session transcript is already complete — there's no mention gap to fill.
- Free-response channelsandbot's own auto-created threads: skipped for the same reason — no mention gating means no gap.

`require_mention: true`
`channel.history()`

Per-user sessions (group_sessions_per_user: true, the default) also benefit: a user's session is missing the context posted by other channel participants and the user's own messages from before they tagged the bot. Backfill fills both gaps.

`group_sessions_per_user: true`

```
discord:  history_backfill: true   # default
```

To turn it off:

```
discord:  history_backfill: false
```

> Note:Messages that arrivewhilethe bot is processing (between a trigger and its response) are not captured. This is an accepted simplification — the user can re-send or tag again.

Note:Messages that arrivewhilethe bot is processing (between a trigger and its response) are not captured. This is an accepted simplification — the user can re-send or tag again.

#### discord.history_backfill_limit​

`discord.history_backfill_limit`

Type:integer —Default:50

`50`

Maximum number of messages to scan backwards when recovering channel context. In practice the scan usually stops much earlier — at the bot's own last message in the channel, which is the natural boundary between turns. This limit is a safety cap for cold starts and long gaps where no prior bot message exists in recent history.

```
discord:  history_backfill: true  history_backfill_limit: 50
```

#### group_sessions_per_user​

`group_sessions_per_user`

Type:boolean —Default:true

`true`

This is a global gateway setting (not Discord-specific) that controls whether users in the same channel get isolated session histories.

Whentrue: Alice and Bob talking in#researcheach have their own separate conversation with Hermes. Whenfalse: the entire channel shares one conversation transcript and one running-agent slot.

`true`
`#research`
`false`

```
group_sessions_per_user: true
```

See theSession Modelsection above for the full implications of each mode.

#### display.tool_progress​

`display.tool_progress`

Type:string —Default:"all"—Values:off,new,all,verbose

`"all"`
`off`
`new`
`all`
`verbose`

Controls whether the bot sends progress messages in the chat while processing (e.g., "Reading file...", "Running terminal command..."). This is a global gateway setting that applies to all platforms.

```
display:  tool_progress: "all"    # off | new | all | verbose
```

- off— no progress messages
- new— only show the first tool call per turn
- all— show all tool calls (truncated to 40 characters in gateway messages)
- verbose— show full tool call details (can produce long messages)

`off`
`new`
`all`
`verbose`

#### display.tool_progress_command​

`display.tool_progress_command`

Type:boolean —Default:false

`false`

When enabled, makes the/verboseslash command available in the gateway, letting you cycle through tool progress modes (off → new → all → verbose → off) without editing config.yaml.

`/verbose`
`off → new → all → verbose → off`

```
display:  tool_progress_command: true
```

## Slash Command Access Control​

By default, every allowed user can run every slash command. To split your allowlist intoadmins(full slash command access) andregular users(only commands you explicitly enable), addallow_admin_fromanduser_allowed_commandsto the Discord platform'sextrablock:

`allow_admin_from`
`user_allowed_commands`
`extra`

```
gateway:  platforms:    discord:      extra:        # Existing user allowlist (unchanged)        allow_from:          - "123456789012345678"  # admin user ID          - "999888777666555444"  # regular user ID        # NEW — admins get all slash commands (built-in + plugin)        allow_admin_from:          - "123456789012345678"        # NEW — non-admin allowed users can only run these slash commands.        # /help and /whoami are always allowed so users can see their access.        user_allowed_commands:          - status          - model          - history        # Optional: separate admin / command lists for server channels        group_allow_admin_from:          - "123456789012345678"        group_user_allowed_commands:          - status
```

Behavior:

- A user inallow_admin_fromfor a scope (DM or server channel) can runeveryregistered slash command — built-in AND plugin-registered — through the live command registry.
- A user not inallow_admin_fromcan only run commands listed inuser_allowed_commands, plus the always-allowed floor:/helpand/whoami.
- Plain chat (non-slash messages) is unaffected. Non-admin users can still talk to the agent normally; they just can't trigger arbitrary commands.
- Backward compat:ifallow_admin_fromis not set for a scope, slash command gating is disabled for that scope. Existing installs keep working with no changes.
- DM admin status does not imply server-channel admin status. Each scope has its own admin list.

`allow_admin_from`
`allow_admin_from`
`user_allowed_commands`
`/help`
`/whoami`
`allow_admin_from`

Use/whoamito see the active scope, your tier (admin / user / unrestricted), and which slash commands you can run.

`/whoami`

## Interactive Model Picker​

Send/modelwith no arguments in a Discord channel to open a dropdown-based model picker:

`/model`
1. Provider selection— a Select dropdown showing available providers (up to 25).
2. Model selection— a second dropdown with models for the chosen provider (up to 25).

The picker times out after 120 seconds. Only authorized users (those inDISCORD_ALLOWED_USERS) can interact with it. If you know the model name, type/model <name>directly.

`DISCORD_ALLOWED_USERS`
`/model <name>`

## Native Slash Commands for Skills​

Hermes automatically registers installed skills asnative Discord Application Commands. This means skills appear in Discord's autocomplete/menu alongside built-in commands.

`/`
- Each skill becomes a Discord slash command (e.g.,/code-review,/ascii-art)
- Skills accept an optionalargsstring parameter
- Discord has a limit of 100 application commands per bot — if you have more skills than available slots, extra skills are skipped with a warning in the logs
- Skills are registered during bot startup alongside built-in commands like/model,/reset, and/background

`/code-review`
`/ascii-art`
`args`
`/model`
`/reset`
`/background`

No extra configuration is needed — any skill installed viahermes skills installis automatically registered as a Discord slash command on the next gateway restart.

`hermes skills install`

### Disabling Slash Command Registration​

If you run multiple Hermes gateways against the same Discord application (e.g. staging + production), only one of them should own the global slash-command registration — otherwise the last startup wins and the registrations flap. Turn slash registration off on the "follower" gateway:

```
gateway:  platforms:    discord:      extra:        slash_commands: false   # default: true
```

Leaving this attrueon the "primary" gateway keeps the normal behavior — global/-menu commands for built-ins and installed skills.

`true`
`/`

## Sending Media (inlineMEDIA:tags)​

`MEDIA:`

The Discord adapter supports native file uploads for every common media type via inlineMEDIA:/path/to/filetags emitted in the agent's response — the adapter strips the tag and auto-uploads the file:

`MEDIA:/path/to/file`
| Type | How it's delivered |
| --- | --- |
| Images (PNG/JPG/WebP) | Native Discord image attachment with inline preview |
| Animated GIFs | send_animationuploads asanimation.gifso Discord plays it inline (not as a static thumbnail) |
| Video (MP4/MOV) | send_video— native video player |
| Audio / Voice | send_voice— native voice message when possible, file attachment otherwise |
| Documents (PDF/ZIP/docx/etc.) | send_document— native attachment with download button |

`send_animation`
`animation.gif`
`send_video`
`send_voice`
`send_document`

Discord's per-upload size limit depends on the server's boost tier (25 MB free, up to 500 MB). If Hermes gets an HTTP 413, the adapter falls back to a link pointing at the local cache path rather than failing silently.

## Receiving Arbitrary File Types​

Any file type a user uploads is accepted. Authorization to message the agent is the gate — not the file extension. Every upload is downloaded, cached under~/.hermes/cache/documents/, and surfaced to the agent as aDOCUMENT-typed message event so it can inspect the file withterminal(ffprobe,unzip,file,strings, etc.) orread_file.

`~/.hermes/cache/documents/`
`DOCUMENT`
`terminal`
`ffprobe`
`unzip`
`file`
`strings`
`read_file`
- Known types (PDF, docx/xlsx/pptx, zip, images/audio/video, etc.) keep their precise MIME.
- Unknown types fall back to the upload's reported content type, orapplication/octet-streamwhen none is given.
- Small UTF-8-decodable files (text, code, config, HTML, CSS, JSON, YAML, ...) have their contents auto-injected into the prompt up to 100 KiB. Binary files that can't be decoded are surfaced as a path-pointing context note only (auto-translated for Docker/Modal sandboxed terminals viato_agent_visible_cache_path), so they don't blow up the context window.

`application/octet-stream`
`to_agent_visible_cache_path`

The only inbound limit is the per-file size cap (default 32 MiB):

```
discord:  # Optional — raise/disable the per-file size cap. Default is 32 MiB.  # The whole file is held in memory while being cached, so unlimited  # uploads carry a real memory cost.  max_attachment_bytes: 33554432   # bytes; 0 = unlimited
```

Equivalent env var:DISCORD_MAX_ATTACHMENT_BYTES=33554432(or0for no cap).

`DISCORD_MAX_ATTACHMENT_BYTES=33554432`
`0`

The legacydiscord.allow_any_attachmentflag is now a no-op — any file type is always accepted — and is kept only so existing configs don't error.

`discord.allow_any_attachment`

Disabling the size cap (max_attachment_bytes: 0) means a user can drop a multi-GB file on the bot and the gateway will dutifully buffer it through memory while caching to disk. Only set this in trusted single-user installs. For shared bots, keep the default 32 MiB or raise it conservatively.

`max_attachment_bytes: 0`

## Interactive Prompts (clarify)​

When the agent calls theclarifytool — to ask which approach you prefer, get post-task feedback, or check before a non-trivial decision — Discord renders the question withone button per choice:

`clarify`

> Which framework should I use for the dashboard?[1. Next.js] [2. Remix] [3. Astro] [Other (type answer)]

Which framework should I use for the dashboard?

[1. Next.js] [2. Remix] [3. Astro] [Other (type answer)]

Click a numbered button to answer, or clickOtherto type a free-form response (the next message you send in that channel becomes the answer). Open-endedclarifycalls (no preset choices) skip the buttons and just capture your next message.

`clarify`

The buttons disable themselves once a choice is made so duplicate clicks don't double-resolve the prompt. Configure the response timeout viaagent.clarify_timeoutin~/.hermes/config.yaml(default600seconds). If you don't respond within the timeout, the agent unblocks with a sentinel message and adapts rather than hanging.

`agent.clarify_timeout`
`~/.hermes/config.yaml`
`600`

## Home Channel​

You can designate a "home channel" where the bot sends proactive messages (such as cron job output, reminders, and notifications). There are two ways to set it:

### Using the Slash Command​

Type/sethomein any Discord channel where the bot is present. That channel becomes the home channel.

`/sethome`

### Manual Configuration​

Add these to your~/.hermes/.env:

`~/.hermes/.env`

```
DISCORD_HOME_CHANNEL=123456789012345678DISCORD_HOME_CHANNEL_NAME="#bot-updates"
```

Replace the ID with the actual channel ID (right-click → Copy Channel ID with Developer Mode on).

## Voice Messages​

Hermes Agent supports Discord voice messages:

- Incoming voice messagesare automatically transcribed using the configured STT provider: localfaster-whisper(no key), Groq Whisper (GROQ_API_KEY), or OpenAI Whisper (VOICE_TOOLS_OPENAI_KEY).
- Text-to-speech: Use/voice ttsto have the bot send spoken audio responses alongside text replies.
- Discord voice channels: Hermes can also join a voice channel, listen to users speaking, and talk back in the channel.

`faster-whisper`
`GROQ_API_KEY`
`VOICE_TOOLS_OPENAI_KEY`
`/voice tts`

For the full setup and operational guide, see:

- Voice Mode
- Use Voice Mode with Hermes

### Voice Channel Audio Effects (ambient + verbal acks)​

When the bot is in a voice channel, you can give it a more conversational feel: a short verbal acknowledgement ("let me look into that") before it starts working, and a subtle ambient "thinking" bed that plays underneath while tools run — the speech ducks the ambient down and swells it back when finished, similar to Grok voice mode.

discord.py plays only one audio stream per connection, so Hermes installs a software mixer on the outgoing stream that sums an ambient loop, acknowledgements, and TTS replies into that single stream — they overlap instead of cutting each other off.

This isoff by default. Enable it inconfig.yaml:

`config.yaml`

```
discord:  voice_fx:    enabled: true          # master switch    ambient_enabled: true  # idle "thinking" bed while tools run    ambient_path: ""       # custom loop file (any audio format); "" = built-in synthesised pad    ambient_gain: 0.18     # idle bed loudness (0.0–1.0)    duck_gain: 0.06        # ambient loudness while the bot is speaking    speech_gain: 1.0       # TTS / acknowledgement loudness    ack_enabled: true      # speak a short phrase before the first tool call of a turn    ack_phrases:           # picked at random; set to [] to disable the spoken ack      - "Let me look into that."      - "One moment."      - "Checking on that now."
```

Notes:

- The acknowledgement fires at most once per turn, only when the bot is in a voice channel and the mixer is active. It uses your configured TTS provider.
- ambient_pathaccepts any fileffmpegcan decode; it's looped seamlessly. Leave it empty to use the built-in synthesised pad (no asset needed).
- All settings live inconfig.yaml(not.env) — they're behavioral, not secrets.
- Whenvoice_fx.enabledisfalse, voice playback uses the original one-shot path and nothing changes.

`ambient_path`
`ffmpeg`
`config.yaml`
`.env`
`voice_fx.enabled`
`false`

## Forum Channels​

Discord forum channels (type 15) don't accept direct messages — every post in a forum must be a thread. Hermes auto-detects forum channels and creates a new thread post whenever it needs to send there, so text replies, TTS, images, voice messages, and file attachments all work without special handling from the agent.

- Thread nameis derived from the first line of the message (markdown heading prefix stripped, capped at 100 chars). When the message is attachment-only, the filename is used as the fallback thread name.
- Attachmentsride along on the starter message of the new thread — no separate upload step, no partial sends.
- One call, one thread: each forum send creates a new thread. Successive sends to the same forum will therefore produce separate threads.
- Detection is three-layered: the channel directory cache first, a process-local probe cache second, and a liveGET /channels/{id}probe as a last resort (whose result is then memoized for the life of the process).

`GET /channels/{id}`

Refreshing the directory (/channels refreshon platforms that expose it, or a gateway restart) populates the cache with any forum channels created after the bot started.

`/channels refresh`

## Troubleshooting​

### Bot is online but not responding to messages​

Cause: Either Message Content Intent is disabled, or Discord auth is failing closed because no access policy is configured.

Fix:

1. Go toDeveloper Portal→ your app → Bot → Privileged Gateway Intents → enableMessage Content Intent→ Save Changes.
2. Verify that at least one Discord access policy is configured:# recommended: allow specific usersDISCORD_ALLOWED_USERS=284102345871466496# or allow a trusted guild/dev bot to behave like pre-0.18 DiscordDISCORD_ALLOW_ALL_USERS=true
3. Restart the gateway:hermes gateway restart

Go toDeveloper Portal→ your app → Bot → Privileged Gateway Intents → enableMessage Content Intent→ Save Changes.

Verify that at least one Discord access policy is configured:

```
# recommended: allow specific usersDISCORD_ALLOWED_USERS=284102345871466496# or allow a trusted guild/dev bot to behave like pre-0.18 DiscordDISCORD_ALLOW_ALL_USERS=true
```

Restart the gateway:

```
hermes gateway restart
```

If the gateway log says Discord is connected and REST API checks work, but every inbound message is silent, look for this warning in~/.hermes/logs/gateway.log:

`~/.hermes/logs/gateway.log`

```
No Discord access policy configured; inbound Discord messages will be denied by default.
```

Hermes 0.18 intentionally fails closed on externally reachable adapters. A Discord bot with noDISCORD_ALLOWED_USERS, noDISCORD_ALLOWED_ROLES, noDISCORD_ALLOWED_CHANNELS, and no explicit allow-all flag will connect successfully but deny inbound users before normal message handling.

`DISCORD_ALLOWED_USERS`
`DISCORD_ALLOWED_ROLES`
`DISCORD_ALLOWED_CHANNELS`

### "Disallowed Intents" error on startup​

Cause: Your code requests intents that aren't enabled in the Developer Portal.

Fix: Enable all three Privileged Gateway Intents (Presence, Server Members, Message Content) in the Bot settings, then restart.

### Bot can't see messages in a specific channel​

Cause: The bot's role doesn't have permission to view that channel.

Fix: In Discord, go to the channel's settings → Permissions → add the bot's role withView ChannelandRead Message Historyenabled.

### 403 Forbidden errors​

Cause: The bot is missing required permissions.

Fix: Re-invite the bot with the correct permissions using the URL from Step 5, or manually adjust the bot's role permissions in Server Settings → Roles.

### Bot is offline​

Cause: The Hermes gateway isn't running, or the token is incorrect.

Fix: Check thathermes gatewayis running. VerifyDISCORD_BOT_TOKENin your.envfile. If you recently reset the token, update it.

`hermes gateway`
`DISCORD_BOT_TOKEN`
`.env`

### "User not allowed" / Bot ignores you​

Cause: Your User ID isn't inDISCORD_ALLOWED_USERS.

`DISCORD_ALLOWED_USERS`

Fix: Add your User ID toDISCORD_ALLOWED_USERSin~/.hermes/.envand restart the gateway.

`DISCORD_ALLOWED_USERS`
`~/.hermes/.env`

### People in the same channel are sharing context unexpectedly​

Cause:group_sessions_per_useris disabled, or the platform cannot provide a user ID for the messages in that context.

`group_sessions_per_user`

Fix: Set this in~/.hermes/config.yamland restart the gateway:

`~/.hermes/config.yaml`

```
group_sessions_per_user: true
```

If you intentionally want a shared room conversation, leave it off — just expect shared transcript history and shared interrupt behavior.

## Security​

Always setDISCORD_ALLOWED_USERS(orDISCORD_ALLOWED_ROLES) to restrict who can interact with the bot. Without either, the gateway denies all users by default as a safety measure. Only authorize people you trust — authorized users have full access to the agent's capabilities, including tool use and system access.

`DISCORD_ALLOWED_USERS`
`DISCORD_ALLOWED_ROLES`

### Role-Based Access Control​

For servers where access is managed by roles instead of individual user lists (moderator teams, support staff, internal tooling), useDISCORD_ALLOWED_ROLES— a comma-separated list of role IDs. Any member with one of those roles is authorized.

`DISCORD_ALLOWED_ROLES`

```
# ~/.hermes/.env — works alongside or instead of DISCORD_ALLOWED_USERSDISCORD_ALLOWED_ROLES=987654321098765432,876543210987654321
```

Semantics:

- OR with user allowlist.A user is authorized if their ID is inDISCORD_ALLOWED_USERSorthey have any role inDISCORD_ALLOWED_ROLES.
- Server Members Intent auto-enabled.WhenDISCORD_ALLOWED_ROLESis set, the bot enables the Members intent on connect — required for Discord to send role information with member records.
- Role IDs, not names.Grab them from Discord:User Settings → Advanced → Developer Mode ON, then right-click any role →Copy Role ID.
- DM fallback.In DMs the role check scans mutual guilds; a user with an allowed role in any shared server is authorized in DMs too.

`DISCORD_ALLOWED_USERS`
`DISCORD_ALLOWED_ROLES`
`DISCORD_ALLOWED_ROLES`

This is the preferred pattern when the moderation team churns — new moderators get access the moment the role is granted, with no.envedit or gateway restart.

`.env`

### Mention Control​

By default, Hermes blocks the bot from pinging@everyone,@here, and role mentions, even if its reply contains those tokens. This prevents a poorly-worded prompt or echoed user content from spamming a whole server. Individual@userpings and reply-reference pings (the little "replying to…" chip) stay enabled so normal conversation still works.

`@everyone`
`@here`
`@user`

You can relax these defaults via either env vars orconfig.yaml:

`config.yaml`

```
# ~/.hermes/config.yamldiscord:  allow_mentions:    everyone: false      # allow the bot to ping @everyone / @here    roles: false         # allow the bot to ping @role mentions    users: true          # allow the bot to ping individual @users    replied_user: true   # ping the author when replying to their message
```

```
# ~/.hermes/.env — env vars win over config.yamlDISCORD_ALLOW_MENTION_EVERYONE=falseDISCORD_ALLOW_MENTION_ROLES=falseDISCORD_ALLOW_MENTION_USERS=trueDISCORD_ALLOW_MENTION_REPLIED_USER=true
```

Leaveeveryoneandrolesatfalseunless you know exactly why you need them. It is very easy for an LLM to produce the string@everyoneinside a normal-looking response; without this protection, that would notify every member of your server.

`everyone`
`roles`
`false`
`@everyone`

For more information on securing your Hermes Agent deployment, see theSecurity Guide.