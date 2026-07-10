- 
- Messaging Platforms
- Popular
- Slack

# Slack Setup

Connect Hermes Agent to Slack as a bot using Socket Mode. Socket Mode uses WebSockets instead of
public HTTP endpoints, so your Hermes instance doesn't need to be publicly accessible — it works
behind firewalls, on your laptop, or on a private server.

Classic Slack apps (using RTM API) werefully deprecated in March 2025. Hermes uses the modern
Bolt SDK with Socket Mode. If you have an old classic app, you must create a new one following
the steps below.

## Overview​

| Component | Value |
| --- | --- |
| Library | slack-bolt/slack_sdkfor Python (Socket Mode) |
| Connection | WebSocket — no public URL required |
| Auth tokens needed | Bot Token (xoxb-) + App-Level Token (xapp-) |
| User identification | Slack Member IDs (e.g.,U01ABC2DEF3) |

`slack-bolt`
`slack_sdk`
`xoxb-`
`xapp-`
`U01ABC2DEF3`

## Step 1: Create a Slack App​

The fastest path is to paste a manifest Hermes generates for you. It
declares every built-in slash command (/btw,/stop,/model, …),
every required OAuth scope, every event subscription, and enables Socket
Mode — all at once.

`/btw`
`/stop`
`/model`

### Option A: From a Hermes-generated manifest (recommended)​

1. Generate the manifest:hermes slack manifest--writeThis writes~/.hermes/slack-manifest.jsonand prints paste-in
instructions.
2. Go tohttps://api.slack.com/apps→Create New App→From an app manifest
3. Pick your workspace, paste the JSON contents, review, clickNext→Create
4. Skip ahead toStep 6: Install App to Workspace. The manifest
handled scopes, events, and slash commands for you.

```
hermes slack manifest --write
```

`~/.hermes/slack-manifest.json`

### Option B: From scratch (manual)​

1. Go tohttps://api.slack.com/apps
2. ClickCreate New App
3. ChooseFrom scratch
4. Enter an app name (e.g., "Hermes Agent") and select your workspace
5. ClickCreate App

You'll land on the app'sBasic Informationpage. Continue with
Steps 2–6 below.

## Step 2: Configure Bot Token Scopes​

Navigate toFeatures → OAuth & Permissionsin the sidebar. Scroll toScopes → Bot Token Scopesand add the following:

| Scope | Purpose |
| --- | --- |
| chat:write | Send messages as the bot |
| app_mentions:read | Detect when @mentioned in channels |
| channels:history | Read messages in public channels the bot is in |
| channels:read | List and get info about public channels |
| groups:history | Read messages in private channels the bot is invited to |
| im:history | Read direct message history |
| im:read | View basic DM info |
| im:write | Open and manage DMs |
| mpim:history | Read group direct message (multi-person DM) history |
| mpim:read | View basic group DM info |
| users:read | Look up user information |
| files:read | Read and download attached files, including voice notes/audio |
| files:write | Upload files (images, audio, documents) |

`chat:write`
`app_mentions:read`
`channels:history`
`channels:read`
`groups:history`
`im:history`
`im:read`
`im:write`
`mpim:history`
`mpim:read`
`users:read`
`files:read`
`files:write`

Withoutchannels:historyandgroups:history, the botwill not receive messages in channels—
it will only work in DMs. Withoutfiles:read, Hermes can chat butcannot reliably read user-uploaded attachments.
These are the most commonly missed scopes.

`channels:history`
`groups:history`
`files:read`

Optional scopes:

| Scope | Purpose |
| --- | --- |
| groups:read | List and get info about private channels |

`groups:read`

## Step 3: Enable Socket Mode​

Socket Mode lets the bot connect via WebSocket instead of requiring a public URL.

1. In the sidebar, go toSettings → Socket Mode
2. ToggleEnable Socket Modeto ON
3. You'll be prompted to create anApp-Level Token:Name it something likehermes-socket(the name doesn't matter)Add theconnections:writescopeClickGenerate
4. Copy the token— it starts withxapp-. This is yourSLACK_APP_TOKEN

- Name it something likehermes-socket(the name doesn't matter)
- Add theconnections:writescope
- ClickGenerate

`hermes-socket`
`connections:write`
`xapp-`
`SLACK_APP_TOKEN`

You can always find or regenerate app-level tokens underSettings → Basic Information → App-Level Tokens.

## Step 4: Subscribe to Events​

This step is critical — it controls what messages the bot can see.

1. In the sidebar, go toFeatures → Event Subscriptions
2. ToggleEnable Eventsto ON
3. ExpandSubscribe to bot eventsand add:

| Event | Required? | Purpose |
| --- | --- | --- |
| message.im | Yes | Bot receives direct messages |
| message.mpim | Yes | Bot receives messages ingroup DMs(multi-person DMs) it's added to |
| message.channels | Yes | Bot receives messages inpublicchannels it's added to |
| message.groups | Recommended | Bot receives messages inprivatechannels it's invited to |
| app_mention | Yes | Prevents Bolt SDK errors when bot is @mentioned |

`message.im`
`message.mpim`
`message.channels`
`message.groups`
`app_mention`
1. ClickSave Changesat the bottom of the page

If the bot works in DMs butnot in channels, you almost certainly forgot to addmessage.channels(for public channels) and/ormessage.groups(for private channels).
Without these events, Slack simply never delivers channel messages to the bot.

`message.channels`
`message.groups`

## Step 5: Enable the Messages Tab​

This step enables direct messages to the bot. Without it, users see"Sending messages to this app has been turned off"when trying to DM the bot.

1. In the sidebar, go toFeatures → App Home
2. Scroll toShow Tabs
3. ToggleMessages Tabto ON
4. Check"Allow users to send Slash commands and messages from the messages tab"

Even with all the correct scopes and event subscriptions, Slack will not allow users to send direct messages to the bot unless the Messages Tab is enabled. This is a Slack platform requirement, not a Hermes configuration issue.

## Step 6: Install App to Workspace​

1. In the sidebar, go toSettings → Install App
2. ClickInstall to Workspace
3. Review the permissions and clickAllow
4. After authorization, you'll see aBot User OAuth Tokenstarting withxoxb-
5. Copy this token— this is yourSLACK_BOT_TOKEN

`xoxb-`
`SLACK_BOT_TOKEN`

If you change scopes or event subscriptions later, youmust reinstall the appfor the changes
to take effect. The Install App page will show a banner prompting you to do so.

## Step 7: Find User IDs for the Allowlist​

Hermes uses SlackMember IDs(not usernames or display names) for the allowlist.

To find a Member ID:

1. In Slack, click on the user's name or avatar
2. ClickView full profile
3. Click the⋮(more) button
4. SelectCopy member ID

Member IDs look likeU01ABC2DEF3. You need your own Member ID at minimum.

`U01ABC2DEF3`

## Step 8: Configure Hermes​

Add the following to your~/.hermes/.envfile:

`~/.hermes/.env`

```
# RequiredSLACK_BOT_TOKEN=xoxb-your-bot-token-hereSLACK_APP_TOKEN=xapp-your-app-token-hereSLACK_ALLOWED_USERS=U01ABC2DEF3              # Comma-separated Member IDs# OptionalSLACK_HOME_CHANNEL=C01234567890              # Default channel for cron/scheduled messagesSLACK_HOME_CHANNEL_NAME=general              # Human-readable name for the home channel (optional)
```

Or run the interactive setup:

```
hermes gateway setup    # Select Slack when prompted
```

Then start the gateway:

```
hermes gateway              # Foregroundhermes gateway install      # Install as a user servicesudo hermes gateway install --system   # Linux only: boot-time system service
```

## Step 9: Invite the Bot to Channels​

After starting the gateway, you need toinvite the botto any channel where you want it to respond:

```
/invite @Hermes Agent
```

The bot willnotautomatically join channels. You must invite it to each channel individually.

## Slash Commands​

Every Hermes command (/btw,/stop,/new,/model,/help, ...)
is a native Slack slash command — exactly the way they work on Telegram
and Discord. Type/in Slack and the autocomplete picker lists every
Hermes command with its description.

`/btw`
`/stop`
`/new`
`/model`
`/help`
`/`

Under the hood: Hermes ships with a generated Slack app manifest (see
Step 1, Option A) that declares every command inCOMMAND_REGISTRYas a slash command. In Socket Mode, Slack routes the command event
through the WebSocket regardless of the manifest'surlfield.

`COMMAND_REGISTRY`
`url`

### Refreshing slash commands after updates​

When Hermes adds new commands (e.g. afterhermes update), regenerate
the manifest and update your Slack app:

`hermes update`

```
hermes slack manifest --write
```

Then in Slack:

1. Openhttps://api.slack.com/apps→
your Hermes app
2. Features → App Manifest → Edit
3. Paste the new contents of~/.hermes/slack-manifest.json
4. Save. Slack will prompt to reinstall the app if scopes or slash
commands changed.

`~/.hermes/slack-manifest.json`

### Legacy/hermes <subcommand>still works​

`/hermes <subcommand>`

For backward compatibility with older manifests, you can still type/hermes btw run the tests— Hermes routes it the same way as/btw run the tests. Free-form questions also work:/hermes what's the weather?is treated as a regular message.

`/hermes btw run the tests`
`/btw run the tests`
`/hermes what's the weather?`

### Using commands inside threads (the!cmdprefix)​

`!cmd`

Slack itself blocks native slash commands inside thread replies — try/queuein a thread and Slack responds with"/queue is not supported
in threads. Sorry!"There is no app-side setting that re-enables them;
Slack never delivers them to Hermes.

`/queue`

As a workaround, Hermes recognises a leading!as an alternate
command prefix that works in threads (and anywhere else). Type!queue,!stop,!model gpt-5.4, etc. as a regular thread reply —
Hermes treats it identically to the slash form and replies in the same
thread.

`!`
`!queue`
`!stop`
`!model gpt-5.4`

Only the first token is checked against the known command list, so
casual messages like!nice workpass through to the agent unchanged.

`!nice work`

Approval prompts (dangerous command /execute_codeapproval) normally
render as interactive buttons. When buttons can't be delivered and
Hermes falls back to a text prompt, the prompt instructs you to reply
with!approve/!deny— the form that works inside threads.

`execute_code`
`!approve`
`!deny`

### Advanced: emit only the slash-commands array​

If you maintain your Slack manifest by hand and just want the slash
command list:

```
hermes slack manifest --slashes-only > /tmp/slashes.json
```

Paste that array into thefeatures.slash_commandskey of your
existing manifest.

`features.slash_commands`

## How the Bot Responds​

Understanding how Hermes behaves in different contexts:

| Context | Behavior |
| --- | --- |
| DMs | Bot responds to every message — no @mention needed |
| Channels | Botonly responds when @mentioned(e.g.,@Hermes Agent what time is it?). In channels, Hermes replies in a thread attached to that message. |
| Threads | If you @mention Hermes inside an existing thread, it replies in that same thread. Once the bot has an active session in a thread,subsequent replies in that thread do not require @mention— the bot follows the conversation naturally. |

`@Hermes Agent what time is it?`

In channels, always @mention the bot to start a conversation. Once the bot is active in a thread, you can reply in that thread without mentioning it. Outside of threads, messages without @mention are ignored to prevent noise in busy channels.

## Configuration Options​

Beyond the required environment variables from Step 8, you can customize Slack bot behavior through~/.hermes/config.yaml.

`~/.hermes/config.yaml`

### Thread & Reply Behavior​

```
platforms:  slack:    # Controls how multi-part responses are threaded    # "off"   — never thread replies to the original message    # "first" — first chunk threads to user's message (default)    # "all"   — all chunks thread to user's message    reply_to_mode: "first"    extra:      # Whether to reply in a thread (default: true).      # When false, channel messages get direct channel replies instead      # of threads. Messages inside existing threads still reply in-thread.      reply_in_thread: true      # Also post thread replies to the main channel      # (Slack's "Also send to channel" feature).      # Only the first chunk of the first reply is broadcast.      reply_broadcast: false      # Render agent messages as Slack Block Kit blocks (default: false).      # When true, the final agent message is sent with structured blocks —      # section headers, dividers, true nested lists (via rich_text), and      # native Block Kit tables — instead of flat mrkdwn text. A plain-text      # fallback is always sent alongside for notifications/accessibility.      # Tables exceeding Slack's limits (100 rows / 20 cols / 10k chars)      # gracefully fall back to aligned monospace.      rich_blocks: false      # Continuable-cron delivery surface (default: "thread").      # "in_channel" delivers a continuable cron job FLAT into the channel      # (no dedicated thread); pair with reply_in_thread: false (and      # require_mention: false) so a plain reply continues the job.      # See the cron guide → "Flat, in-channel continuation".      cron_continuable_surface: thread
```

| Key | Default | Description |
| --- | --- | --- |
| platforms.slack.reply_to_mode | "first" | Threading mode for multi-part messages:"off","first", or"all" |
| platforms.slack.extra.reply_in_thread | true | Whenfalse, channel messages get direct replies instead of threads. Messages inside existing threads still reply in-thread. |
| platforms.slack.extra.reply_broadcast | false | Whentrue, thread replies are also posted to the main channel. Only the first chunk is broadcast. |
| platforms.slack.extra.rich_blocks | false | Whentrue, agent messages are rendered asBlock Kitblocks (headers, dividers, true nested lists, and native tables). A plain-text fallback is always sent. Tables over Slack's limits fall back to aligned monospace. No app reinstall required — it's a send-side change only. |
| platforms.slack.extra.cron_continuable_surface | "thread" | Delivery surface forcontinuable cron jobs."thread"opens a dedicated thread per delivery (default);"in_channel"delivers flat into the channel timeline. Pairin_channelwithreply_in_thread: false(andrequire_mention: false) so a plain channel reply continues the job. |

`platforms.slack.reply_to_mode`
`"first"`
`"off"`
`"first"`
`"all"`
`platforms.slack.extra.reply_in_thread`
`true`
`false`
`platforms.slack.extra.reply_broadcast`
`false`
`true`
`platforms.slack.extra.rich_blocks`
`false`
`true`
`platforms.slack.extra.cron_continuable_surface`
`"thread"`
`"thread"`
`"in_channel"`
`in_channel`
`reply_in_thread: false`
`require_mention: false`

### Session Isolation​

```
# Global setting — applies to Slack and all other platformsgroup_sessions_per_user: true
```

Whentrue(the default), each user in a shared channel gets their own isolated conversation session. Two people talking to Hermes in#generalwill have separate histories and contexts.

`true`
`#general`

Set tofalseif you want a collaborative mode where the entire channel shares one conversation session. Be aware this means users share context growth and token costs, and one user's/resetclears the session for everyone.

`false`
`/reset`

### Mention & Trigger Behavior​

```
slack:  # Require @mention in channels (this is the default behavior;  # the Slack adapter enforces @mention gating in channels regardless,  # but you can set this explicitly for consistency with other platforms)  require_mention: true  # Prevent thread auto-engagement: only reply to channel messages that  # contain an explicit @mention. With this OFF (default), Slack can  # "auto-engage" — remembering past mentions in a thread and following  # up on bot-message replies, and resuming active sessions without a  # fresh mention. With strict_mention ON, every new channel message  # must @mention the bot before Hermes will respond.  strict_mention: false  # Custom mention patterns that trigger the bot  # (in addition to the default @mention detection)  mention_patterns:    - "hey hermes"    - "hermes,"  # Text prepended to every outgoing message  reply_prefix: ""
```

`strict_mention`

Set this totruein busy workspaces where Slack's default "the bot remembers this thread" behavior surprises users — for example, a long tech-support thread where the bot helped at the start and you'd rather it stay silent unless explicitly pinged again. DMs and active interactive sessions are unaffected.

`true`

Slack supports both patterns:@mentionrequired to start a conversation by default, but you can opt specific channels out viaSLACK_FREE_RESPONSE_CHANNELS(comma-separated channel IDs) orslack.free_response_channelsinconfig.yaml. Once the bot has an active session in a thread, subsequent thread replies do not require a mention. In1:1 DMsthe bot always responds without needing a mention.

`@mention`
`SLACK_FREE_RESPONSE_CHANNELS`
`slack.free_response_channels`
`config.yaml`

A1:1 direct messageis a private conversation with one person, so it is mention-exempt. Agroup DM (MPIM / multi-person DM)is ashared surface— multiple people can see and trigger the bot — so it obeys the same operator controls as a channel:require_mention,strict_mention,free_response_channels, andallowed_channelsall apply, and the bot only adds:eyes:/:white_check_mark:reactions when it is actually@mentioned. To let the bot respond freely in a specific group DM, add its channel ID (starts withG) tofree_response_channels.

`require_mention`
`strict_mention`
`free_response_channels`
`allowed_channels`
`:eyes:`
`:white_check_mark:`
`@mentioned`
`G`
`free_response_channels`

### Channel allowlist (allowed_channels)​

`allowed_channels`

Restrict the bot to a fixed set of Slack channels — useful when the bot is invited to many channels but should only respond in a few. When set, messages from channels NOT in this list aresilently ignored, even if the bot is@mentioned.

`@mentioned`

1:1 DMs are exemptfrom this filter, so authorized users can always reach the bot in a direct message.Group DMs (MPIMs) are not exempt— like channels, an MPIM must be on the allowlist (its ID starts withG) or its messages are dropped.

`G`

```
slack:  allowed_channels:    - "C0123456789"   # #ops    - "C0987654321"   # #incident-response
```

Or via env var (comma-separated):

```
SLACK_ALLOWED_CHANNELS="C0123456789,C0987654321"
```

Behavior:

- Empty / unset → no restriction (fully backward compatible).
- Non-empty → channel ID must be on the list, or the message is dropped before any other gating (mention requirement,free_response_channels, etc.) runs.
- Slack channel IDs start withC(public),G(private), orD(DM). Look them up via the Slack UI's "Open channel details" → "About" panel, or via the API.

`free_response_channels`
`C`
`G`
`D`

See also:admin/user slash command split.

### Unauthorized User Handling​

```
slack:  # What happens when an unauthorized user (not in SLACK_ALLOWED_USERS) DMs the bot  # "pair"   — prompt them for a pairing code (default)  # "ignore" — silently drop the message  unauthorized_dm_behavior: "pair"
```

You can also set this globally for all platforms:

```
unauthorized_dm_behavior: "pair"
```

The platform-specific setting underslack:takes precedence over the global setting.

`slack:`

### Voice Transcription​

```
# Global setting — enable/disable automatic transcription of incoming voice messagesstt_enabled: true
```

Whentrue(the default), incoming audio messages are automatically transcribed using the configured STT provider before being processed by the agent.

`true`

### Full Example​

```
# Global gateway settingsgroup_sessions_per_user: trueunauthorized_dm_behavior: "pair"stt_enabled: true# Slack-specific settingsslack:  require_mention: true  unauthorized_dm_behavior: "pair"# Platform configplatforms:  slack:    reply_to_mode: "first"    extra:      reply_in_thread: true      reply_broadcast: false
```

## Home Channel​

SetSLACK_HOME_CHANNELto a channel ID where Hermes will deliver scheduled messages,
cron job results, and other proactive notifications. To find a channel ID:

`SLACK_HOME_CHANNEL`
1. Right-click the channel name in Slack
2. ClickView channel details
3. Scroll to the bottom — the Channel ID is shown there

```
SLACK_HOME_CHANNEL=C01234567890
```

Make sure the bot has beeninvited to the channel(/invite @Hermes Agent).

`/invite @Hermes Agent`

## Multi-Workspace Support​

Hermes can connect tomultiple Slack workspacessimultaneously using a single gateway instance. Each workspace is authenticated independently with its own bot user ID.

### Configuration​

Provide multiple bot tokens as acomma-separated listinSLACK_BOT_TOKEN:

`SLACK_BOT_TOKEN`

```
# Multiple bot tokens — one per workspaceSLACK_BOT_TOKEN=xoxb-workspace1-token,xoxb-workspace2-token,xoxb-workspace3-token# A single app-level token is still used for Socket ModeSLACK_APP_TOKEN=xapp-your-app-token
```

Or in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
platforms:  slack:    token: "xoxb-workspace1-token,xoxb-workspace2-token"
```

### OAuth Token File​

In addition to tokens in the environment or config, Hermes also loads tokens from anOAuth token fileat:

```
~/.hermes/slack_tokens.json
```

This file is a JSON object mapping team IDs to token entries:

```
{  "T01ABC2DEF3": {    "token": "xoxb-workspace-token-here",    "team_name": "My Workspace"  }}
```

Tokens from this file are merged with any tokens specified viaSLACK_BOT_TOKEN. Duplicate tokens are automatically deduplicated.

`SLACK_BOT_TOKEN`

### How it works​

- Thefirst tokenin the list is the primary token, used for the Socket Mode connection (AsyncApp).
- Each token is authenticated viaauth.teston startup. The gateway maps eachteam_idto its ownWebClientandbot_user_id.
- When a message arrives, Hermes uses the correct workspace-specific client to respond.
- The primarybot_user_id(from the first token) is used for backward compatibility with features that expect a single bot identity.

`auth.test`
`team_id`
`WebClient`
`bot_user_id`
`bot_user_id`

## Voice Messages​

Hermes supports voice on Slack:

- Incoming:Voice/audio messages are automatically transcribed using the configured STT provider: localfaster-whisper, Groq Whisper (GROQ_API_KEY), or OpenAI Whisper (VOICE_TOOLS_OPENAI_KEY)
- Outgoing:TTS responses are sent as audio file attachments

`faster-whisper`
`GROQ_API_KEY`
`VOICE_TOOLS_OPENAI_KEY`

## Per-Channel Prompts​

Assign ephemeral system prompts to specific Slack channels. The prompt is injected at runtime on every turn — never persisted to transcript history — so changes take effect immediately.

```
slack:  channel_prompts:    "C01RESEARCH": |      You are a research assistant. Focus on academic sources,      citations, and concise synthesis.    "C02ENGINEERING": |      Code review mode. Be precise about edge cases and      performance implications.
```

Keys are Slack channel IDs (find them via channel details → "About" → scroll to bottom). All messages in the matching channel get the prompt injected as an ephemeral system instruction.

## Per-Channel Skill Bindings​

Auto-load a skill whenever a new session starts in a specific channel or DM. Unlike per-channel prompts (which are injected on every turn), skill bindings inject the skill content as a user message atsession start— it becomes part of the conversation history and does not need to be reloaded on subsequent turns.

This is ideal for DMs or channels with a dedicated purpose (flashcards, a domain-specific Q&A bot, a support triage channel, etc.) where you don't want the model's own skill selector to decide whether to load on every short reply.

```
slack:  channel_skill_bindings:    # DM channel — always runs in "german-flashcards" mode    - id: "D0ATH9TQ0G6"      skills:        - german-flashcards    # Research channel — preload multiple skills in order    - id: "C01RESEARCH"      skills:        - arxiv        - writing-plans    # Short form: single skill as a string    - id: "C02SUPPORT"      skill: hubspot-on-demand
```

Notes:

- The binding matches by channel ID. For threaded messages in a bound channel, the thread inherits the parent channel's binding.
- The skill is loaded only at session start (new session or after auto-reset). If you change the binding, run/newor wait for the session to auto-reset for it to take effect.
- Combine withchannel_promptsfor per-channel tone/constraints on top of the skill's instructions.

`/new`
`channel_prompts`

## Troubleshooting​

| Problem | Solution |
| --- | --- |
| Bot doesn't respond to DMs | Verifymessage.imis in your event subscriptions and the app is reinstalled |
| Bot works in DMs but not in channels | Most common issue.Addmessage.channelsandmessage.groupsto event subscriptions, reinstall the app, and invite the bot to the channel with/invite @Hermes Agent |
| Bot doesn't respond to @mentions in channels | 1) Checkmessage.channelsevent is subscribed. 2) Bot must be invited to the channel. 3) Ensurechannels:historyscope is added. 4) Reinstall the app after scope/event changes |
| Bot ignores messages in private channels | Add both themessage.groupsevent subscription andgroups:historyscope, then reinstall the app and/invitethe bot |
| Bot doesn't respond in group DMs (multi-person DMs) | Add themessage.mpimevent subscription and thempim:historyscope (plusmpim:read), thenreinstallthe app. Withoutmessage.mpim, Slack never delivers group-DM messages to the bot — even though 1:1 DMs work. |
| "Sending messages to this app has been turned off" in DMs | Enable theMessages Tabin App Home settings (see Step 5) |
| "not_authed" or "invalid_auth" errors | Regenerate your Bot Token and App Token, update.env |
| Bot responds but can't post in a channel | Invite the bot to the channel with/invite @Hermes Agent |
| Bot can chat but can't read uploaded images/files | Addfiles:read, thenreinstallthe app. Hermes now surfaces attachment access diagnostics in-chat when Slack returns scope/auth/permission failures. |
| missing_scopeerror | Add the required scope in OAuth & Permissions, thenreinstallthe app |
| Socket disconnects frequently | Check your network; Bolt auto-reconnects but unstable connections cause lag |
| Changed scopes/events but nothing changed | Youmust reinstallthe app to your workspace after any scope or event subscription change |

`message.im`
`message.channels`
`message.groups`
`/invite @Hermes Agent`
`message.channels`
`channels:history`
`message.groups`
`groups:history`
`/invite`
`message.mpim`
`mpim:history`
`mpim:read`
`message.mpim`
`.env`
`/invite @Hermes Agent`
`files:read`
`missing_scope`

### Quick Checklist​

If the bot isn't working in channels, verifyallof the following:

1. ✅message.channelsevent is subscribed (for public channels)
2. ✅message.groupsevent is subscribed (for private channels)
3. ✅app_mentionevent is subscribed
4. ✅channels:historyscope is added (for public channels)
5. ✅groups:historyscope is added (for private channels)
6. ✅ App wasreinstalledafter adding scopes/events
7. ✅ Bot wasinvitedto the channel (/invite @Hermes Agent)
8. ✅ You are@mentioningthe bot in your message

`message.channels`
`message.groups`
`app_mention`
`channels:history`
`groups:history`
`/invite @Hermes Agent`

## Security​

Always setSLACK_ALLOWED_USERSwith the Member IDs of authorized users. Without this setting,
the gateway willdeny all messagesby default as a safety measure. Never share your bot tokens —
treat them like passwords.

`SLACK_ALLOWED_USERS`
- Tokens should be stored in~/.hermes/.env(file permissions600)
- Rotate tokens periodically via the Slack app settings
- Audit who has access to your Hermes config directory
- Socket Mode means no public endpoint is exposed — one less attack surface

`~/.hermes/.env`
`600`