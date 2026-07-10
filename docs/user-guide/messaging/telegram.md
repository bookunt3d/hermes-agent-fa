---
layout: docs
title: "Messaging_Telegram"
permalink: /docs/user-guide/messaging/telegram/
---

- 
- Messaging Platforms
- Popular
- Telegram

# Telegram Setup

Hermes Agent integrates with Telegram as a full-featured conversational bot. Once connected, you can chat with your agent from any device, send voice memos that get auto-transcribed, receive scheduled task results, and use the agent in group chats. The integration is built onpython-telegram-botand supports text, voice, images, and file attachments.

## Step 1: Create a Bot via BotFather​

Every Telegram bot requires an API token issued by@BotFather, Telegram's official bot management tool.

1. Open Telegram and search for@BotFather, or visitt.me/BotFather
2. Send/newbot
3. Choose adisplay name(e.g., "Hermes Agent") — this can be anything
4. Choose ausername— this must be unique and end inbot(e.g.,my_hermes_bot)
5. BotFather replies with yourAPI token. It looks like this:

`/newbot`
`bot`
`my_hermes_bot`

```
123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

Keep your bot token secret. Anyone with this token can control your bot. If it leaks, revoke it immediately via/revokein BotFather.

`/revoke`

## Step 2: Customize Your Bot (Optional)​

These BotFather commands improve the user experience. Message @BotFather and use:

| Command | Purpose |
| --- | --- |
| /setdescription | The "What can this bot do?" text shown before a user starts chatting |
| /setabouttext | Short text on the bot's profile page |
| /setuserpic | Upload an avatar for your bot |
| /setcommands | Define the command menu (the/button in chat) |
| /setprivacy | Control whether the bot sees all group messages (see Step 3) |

`/setdescription`
`/setabouttext`
`/setuserpic`
`/setcommands`
`/`
`/setprivacy`

For/setcommands, a useful starting set:

`/setcommands`

```
help - Show help informationnew - Start a new conversationsethome - Set this chat as the home channel
```

### Online/Offline status indicator (Optional)​

Telegram bots have no real online/offline presence dot — that green dot is auser-accountfeature, not something the Bot API exposes for bots. The closest
surface is the bot'sshort description(the line shown under its name in the
bot's profile).

Enablestatus_indicatorand Hermes sets that short description toOnlinewhen the gateway connects andOfflineon a clean shutdown:

`status_indicator`

```
gateway:  platforms:    telegram:      extra:        status_indicator: true        # Optional custom strings (defaults: "Online" / "Offline"):        status_online: "🟢 Online"        status_offline: "🔴 Offline"
```

Notes:

- The short description isglobalto the bot (visible to all users), not
per-chat. Users see it on the bot's profile page, not as a live badge inside
an open chat.
- Only acleangateway shutdown (/stop,disconnect) writes "Offline".
A hard crash leaves the last-known status — the inherent limitation of a
profile-text indicator.
- Off by default, since it mutates the bot's global profile.

`/stop`
`disconnect`

### Command menu priority and cap (Optional)​

Hermes registers its command menu automatically when the Telegram gateway starts. The menu is built from the central slash-command registry plus eligible plugin/skill commands, then capped so Telegram accepts the payload reliably. The default cap is 60 commands — enough to keep all built-in commands plus common skill commands visible.

If you have local or plugin commands that should stay visible in Telegram's/picker, prioritize them in~/.hermes/config.yaml:

`/`
`~/.hermes/config.yaml`

```
platforms:  telegram:    extra:      command_menu:        max_commands: 60        priority_mode: prepend  # prepend | append | replace        priority:          - my_plugin_command
```

priority_modecontrols how your list combines with Hermes' built-in priority list:

`priority_mode`
- prepend: put your commands first, then Hermes defaults
- append: keep Hermes defaults first, then your commands
- replace: use only your list for priority ordering

`prepend`
`append`
`replace`

Telegram allows up to 100 BotCommands, but large command payloads can fail. Hermes defaults to 60 for reliability and clamps configured values to1..100; use/commandsfor the full command list.

`1..100`
`/commands`

## Step 3: Privacy Mode (Critical for Groups)​

Telegram bots have aprivacy modethat isenabled by default. This is the single most common source of confusion when using bots in groups.

With privacy mode ON, your bot can only see:

- Messages that start with a/command
- Replies directly to the bot's own messages
- Service messages (member joins/leaves, pinned messages, etc.)
- Messages in channels where the bot is an admin

`/`

With privacy mode OFF, the bot receives every message in the group.

### How to disable privacy mode​

1. Message@BotFather
2. Send/mybots
3. Select your bot
4. Go toBot Settings → Group Privacy → Turn off

`/mybots`

You must remove and re-add the bot to any groupafter changing the privacy setting. Telegram caches the privacy state when a bot joins a group, and it will not update until the bot is removed and re-added.

An alternative to disabling privacy mode: promote the bot togroup admin. Admin bots always receive all messages regardless of the privacy setting, and this avoids needing to toggle the global privacy mode.

### Observe group chatter without auto-replying​

For OpenClaw/Yuanbao-style group behavior, configure Telegram so the bot canseeordinary group messages but onlyrespondswhen directly triggered:

```
telegram:  allowed_chats:    - "-1001234567890"  group_allowed_chats:    - "-1001234567890"  require_mention: true  observe_unmentioned_group_messages: true
```

With this mode enabled, unmentioned group messages from explicitly allowlisted chats/topics are appended to the shared chat/topic session transcript as observed context, but they do not dispatch the agent.allowed_chatsgates where the bot responds;group_allowed_chatsauthorizes the shared group session used for observed context, so use the same chat IDs for this mode. A later@botnamemention, reply to the bot, or configured mention pattern in that same allowlisted chat/topic can use that observed context. The triggered message is also tagged with[nickname|user_id]and gets a per-turn safety prompt so the model treats prior observed lines as context, not instructions addressed to the bot.

`allowed_chats`
`group_allowed_chats`
`@botname`
`[nickname|user_id]`

Equivalent environment variable:

```
TELEGRAM_ALLOWED_CHATS=-1001234567890TELEGRAM_GROUP_ALLOWED_CHATS=-1001234567890TELEGRAM_OBSERVE_UNMENTIONED_GROUP_MESSAGES=true
```

This requires Telegram to deliver ordinary group messages to the gateway, so disable BotFather privacy mode or promote the bot to group admin as described above.

## Step 4: Find Your User ID​

Hermes Agent uses numeric Telegram user IDs to control access. Your user ID isnotyour username — it's a number like123456789.

`123456789`

Method 1 (recommended):Message@userinfobot— it instantly replies with your user ID.

Method 2:Message@get_id_bot— another reliable option.

Save this number; you'll need it for the next step.

## Step 5: Configure Hermes​

### Option A: Interactive Setup (Recommended)​

```
hermes gateway setup
```

SelectTelegramwhen prompted. The wizard asks for your bot token and allowed user IDs, then writes the configuration for you.

### Option B: Manual Configuration​

Add the following to~/.hermes/.env:

`~/.hermes/.env`

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZTELEGRAM_ALLOWED_USERS=123456789    # Comma-separated for multiple users
```

### Start the Gateway​

```
hermes gateway
```

The bot should come online within seconds. Send it a message on Telegram to verify.

## Sending Generated Files from Docker-backed Terminals​

If your terminal backend isdocker, keep in mind that Telegram attachments are
sent by thegateway process, not from inside the container. That means the
finalMEDIA:/...path must be readable on the host where the gateway is
running.

`docker`
`MEDIA:/...`

Common pitfall:

- the agent writes a file inside Docker to/workspace/report.txt
- the model emitsMEDIA:/workspace/report.txt
- Telegram delivery fails because/workspace/report.txtonly exists inside the
container, not on the host

`/workspace/report.txt`
`MEDIA:/workspace/report.txt`
`/workspace/report.txt`

Recommended pattern:

```
terminal:  backend: docker  docker_volumes:    - "/home/user/.hermes/cache/documents:/output"
```

Then:

- write files inside Docker to/output/...
- emit thehost-visiblepath inMEDIA:, for example:MEDIA:/home/user/.hermes/cache/documents/report.txt

`/output/...`
`MEDIA:`
`MEDIA:/home/user/.hermes/cache/documents/report.txt`

If you already have adocker_volumes:section, add the new mount to the same
list. YAML duplicate keys silently override earlier ones.

`docker_volumes:`

### SupportedMEDIA:file extensions​

`MEDIA:`

The gateway extractsMEDIA:/path/to/filetags from agent replies and ships the referenced file as a platform-native attachment. Supported extensions across all gateway platforms:

`MEDIA:/path/to/file`
| Category | Extensions |
| --- | --- |
| Images | png,jpg,jpeg,gif,webp,bmp,tiff,svg |
| Audio | mp3,wav,ogg,m4a,opus,flac,aac |
| Video | mp4,mov,webm,mkv,avi |
| Documents | pdf,txt,md,csv,json,xml,html,yaml,yml,log |
| Office | docx,xlsx,pptx,odt,ods,odp |
| Archives | zip,rar,7z,tar,gz,bz2 |
| Books / packages | epub,apk,ipa |

`png`
`jpg`
`jpeg`
`gif`
`webp`
`bmp`
`tiff`
`svg`
`mp3`
`wav`
`ogg`
`m4a`
`opus`
`flac`
`aac`
`mp4`
`mov`
`webm`
`mkv`
`avi`
`pdf`
`txt`
`md`
`csv`
`json`
`xml`
`html`
`yaml`
`yml`
`log`
`docx`
`xlsx`
`pptx`
`odt`
`ods`
`odp`
`zip`
`rar`
`7z`
`tar`
`gz`
`bz2`
`epub`
`apk`
`ipa`

Anything on this list delivered as a native attachment on platforms that support it (Telegram, Discord, Signal, Slack, WhatsApp, Feishu, Matrix, etc.); on platforms without native support it falls back to a link or plain-text indicator. Theboldcategories were added in the last few releases — if you were relying on the model sayinghere is the file: /path/to/report.docxinstead, swap toMEDIA:/path/to/report.docxfor native delivery.

`here is the file: /path/to/report.docx`
`MEDIA:/path/to/report.docx`

## Webhook Mode​

By default, Hermes connects to Telegram usinglong polling— the gateway makes outbound requests to Telegram's servers to fetch new updates. This works well for local and always-on deployments.

Forcloud deployments(Fly.io, Railway, Render, etc.),webhook modeis more cost-effective. These platforms can auto-wake suspended machines on inbound HTTP traffic, but not on outbound connections. Since polling is outbound, a polling bot can never sleep. Webhook mode flips the direction — Telegram pushes updates to your bot's HTTPS URL, enabling sleep-when-idle deployments.

|  | Polling (default) | Webhook |
| --- | --- | --- |
| Direction | Gateway → Telegram (outbound) | Telegram → Gateway (inbound) |
| Best for | Local, always-on servers | Cloud platforms with auto-wake |
| Setup | No extra config | SetTELEGRAM_WEBHOOK_URL |
| Idle cost | Machine must stay running | Machine can sleep between messages |

`TELEGRAM_WEBHOOK_URL`

### Configuration​

Add the following to~/.hermes/.env:

`~/.hermes/.env`

```
TELEGRAM_WEBHOOK_URL=https://my-app.fly.dev/telegramTELEGRAM_WEBHOOK_SECRET="$(openssl rand -hex 32)"  # required# TELEGRAM_WEBHOOK_PORT=8443        # optional, default 8443
```

| Variable | Required | Description |
| --- | --- | --- |
| TELEGRAM_WEBHOOK_URL | Yes | Public HTTPS URL where Telegram will send updates. The URL path is auto-extracted (e.g.,/telegramfrom the example above). |
| TELEGRAM_WEBHOOK_SECRET | Yes(whenTELEGRAM_WEBHOOK_URLis set) | Secret token that Telegram echoes in every webhook request for verification. The gateway refuses to start without it — seeGHSA-3vpc-7q5r-276h. Generate withopenssl rand -hex 32. |
| TELEGRAM_WEBHOOK_PORT | No | Local port the webhook server listens on (default:8443). |

`TELEGRAM_WEBHOOK_URL`
`/telegram`
`TELEGRAM_WEBHOOK_SECRET`
`TELEGRAM_WEBHOOK_URL`
`openssl rand -hex 32`
`TELEGRAM_WEBHOOK_PORT`
`8443`

WhenTELEGRAM_WEBHOOK_URLis set, the gateway starts an HTTP webhook server instead of polling. When unset, polling mode is used — no behavior change from previous versions.

`TELEGRAM_WEBHOOK_URL`

### Cloud deployment example (Fly.io)​

1. Add the env vars to your Fly.io app secrets:

```
fly secrets set TELEGRAM_WEBHOOK_URL=https://my-app.fly.dev/telegramfly secrets set TELEGRAM_WEBHOOK_SECRET=$(openssl rand -hex 32)
```

1. Expose the webhook port in yourfly.toml:

`fly.toml`

```
[[services]]  internal_port = 8443  protocol = "tcp"  [[services.ports]]    handlers = ["tls", "http"]    port = 443
```

1. Deploy:

```
fly deploy
```

The gateway log should show:[telegram] Connected to Telegram (webhook mode).

`[telegram] Connected to Telegram (webhook mode)`

## Proxy Support​

If Telegram's API is blocked or you need to route traffic through a proxy, set a Telegram-specific proxy URL. This takes priority over the genericHTTPS_PROXY/HTTP_PROXYenv vars.

`HTTPS_PROXY`
`HTTP_PROXY`

Option 1: config.yaml (recommended)

```
telegram:  proxy_url: "socks5://127.0.0.1:1080"
```

Option 2: environment variable

```
TELEGRAM_PROXY=socks5://127.0.0.1:1080
```

Supported schemes:http://,https://,socks5://.

`http://`
`https://`
`socks5://`

The proxy applies to both the main Telegram connection and the fallback IP transport. If no Telegram-specific proxy is set, the gateway falls back toHTTPS_PROXY/HTTP_PROXY/ALL_PROXY(or macOS system proxy auto-detection).

`HTTPS_PROXY`
`HTTP_PROXY`
`ALL_PROXY`

## Home Channel​

Use the/sethomecommand in any Telegram chat (DM or group) to designate it as thehome channel. Scheduled tasks (cron jobs) deliver their results to this channel.

`/sethome`

You can also set it manually in~/.hermes/.env:

`~/.hermes/.env`

```
TELEGRAM_HOME_CHANNEL=-1001234567890TELEGRAM_HOME_CHANNEL_NAME="My Notes"
```

Group chat IDs are negative numbers (e.g.,-1001234567890). Your personal DM chat ID is the same as your user ID.

`-1001234567890`

### Cron deliveries in topic mode​

If you have topic mode enabled in your bot DM, cron messages delivered to the root chat land in the system-only lobby — replying there opens no session and you see the "main chat is reserved for system commands" notice. Create a dedicated forum topic (e.g.Cron) and set:

`Cron`

```
TELEGRAM_CRON_THREAD_ID=<topic_thread_id>
```

TELEGRAM_CRON_THREAD_IDoverridesTELEGRAM_HOME_CHANNEL_THREAD_IDfor cron deliveries only. Replies in that topic continue the topic's existing session.

`TELEGRAM_CRON_THREAD_ID`
`TELEGRAM_HOME_CHANNEL_THREAD_ID`

## Voice Messages​

### Incoming Voice (Speech-to-Text)​

Voice messages you send on Telegram are automatically transcribed by Hermes's configured STT provider and injected as text into the conversation.

- localusesfaster-whisperon the machine running Hermes — no API key required
- groquses Groq Whisper and requiresGROQ_API_KEY
- openaiuses OpenAI Whisper and requiresVOICE_TOOLS_OPENAI_KEY

`local`
`faster-whisper`
`groq`
`GROQ_API_KEY`
`openai`
`VOICE_TOOLS_OPENAI_KEY`

#### Skipping STT: pass the raw audio file to the agent​

If you'd rather have theagent itselfhandle audio — for diarization, a custom transcription tool, or just archiving the recording — setstt.enabled: falsein~/.hermes/config.yaml:

`stt.enabled: false`
`~/.hermes/config.yaml`

```
stt:  enabled: false
```

With STT disabled, the gateway still downloads the voice/audio attachment into Hermes's audio cache, butdoes not transcribe it. The agent receives the message with a marker like:

```
[The user sent a voice message: /home/<user>/.hermes/cache/audio/<hash>.ogg]
```

Your tools or skills can then read that path directly (e.g., hand it off to a local diarization pipeline, a richer transcription model, or upload it to long-term storage). The file extension reflects the original format Telegram delivered (.oggfor voice notes,.mp3/.m4a/etc. for audio attachments).

`.ogg`
`.mp3`
`.m4a`

This pairs naturally with thelocal Bot API serversection below, which lifts Telegram's 20MB getFile ceiling to 2GB — useful when the recordings you want to process are longer than a couple of minutes.

### Outgoing Voice (Text-to-Speech)​

When the agent generates audio via TTS, it's delivered as native Telegramvoice bubbles— the round, inline-playable kind.

- OpenAI and ElevenLabsproduce Opus natively — no extra setup needed
- Edge TTS(the default free provider) outputs MP3 and requiresffmpegto convert to Opus:

```
# Ubuntu/Debiansudo apt install ffmpeg# macOSbrew install ffmpeg
```

Without ffmpeg, Edge TTS audio is sent as a regular audio file (still playable, but uses the rectangular player instead of a voice bubble).

Configure the TTS provider in yourconfig.yamlunder thetts.providerkey.

`config.yaml`
`tts.provider`

## Large Files (>20MB) via Local Bot API Server​

Telegram'spublicBot API capsgetFiledownloads at20 MB, so any voice note, audio file, video, or document larger than that is silently rejected by Hermes with a "too large" reply. The documented way around this is to run alocaltelegram-bot-apidaemon — the same server software Telegram uses, but running on your network. A local server raises the file ceiling to2 GBand Hermes auto-lifts its own internal cap when it sees a custombase_urlconfigured.

`getFile`
`base_url`

This unlocks workflows like:

- Sending long voice memos (45-minute meetings, podcasts) to the bot
- Uploading large videos for vision-tool processing
- Archiving raw audio for offline pipelines like diarization, alignment, or training data

### Step 1: Obtain Telegram API credentials​

The local server talks directly to Telegram's MTProto layer (not the public Bot API), so it needsMTProto credentials:

1. Visitmy.telegram.org/appsand sign in with your Telegram account.
2. Create a new application (any name and short description will do).
3. Copy theapi_idandapi_hash— both are required.

`api_id`
`api_hash`

### Step 2: Run the telegram-bot-api server​

The community-maintainedaiogram/telegram-bot-apiDocker image is the easiest path. A minimaldocker-compose.yaml(use--localmode to enable the higher limits):

`aiogram/telegram-bot-api`
`docker-compose.yaml`
`--local`

```
services:  tg-bot-api:    image: aiogram/telegram-bot-api:latest    container_name: tg-bot-api    restart: unless-stopped    ports:      - "127.0.0.1:8081:8081"   # bind to loopback only; see security note    environment:      TELEGRAM_API_ID: "12345"           # your api_id from Step 1      TELEGRAM_API_HASH: "abcdef..."     # your api_hash from Step 1      TELEGRAM_LOCAL: "1"                # enable --local mode (raises 20MB → 2GB)    volumes:      - ./tg-bot-api-data:/var/lib/telegram-bot-api
```

Bring it up:

```
docker compose up -d tg-bot-apidocker logs --tail 20 tg-bot-api
```

The local Bot API server takes your bot token in the URL path (e.g./bot<TOKEN>/getMe) withno additional auth. Anyone who can reach the port can fully control your bot — read every message it can see, send messages as it, etc. Bind the container to127.0.0.1and/or front it with a reverse proxy on a private network.Never expose port 8081 to the public internet.

`/bot<TOKEN>/getMe`
`127.0.0.1`

### Step 3: Log the bot out of the public API (one-time)​

A bot can only be active ononeBot API server at a time. If your bot was already running againstapi.telegram.org(which it almost certainly was), you must explicitly log it out there before the local server will accept it:

`api.telegram.org`

```
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/logOut"# expected response: {"ok":true,"result":true}
```

This is a one-shot migration step — you don't repeat it on every restart. Telegram delivers any messages received afterlogOutthrough the new server instead.

`logOut`

Verify the local server can talk to Telegram on the bot's behalf:

```
curl "http://127.0.0.1:8081/bot<YOUR_BOT_TOKEN>/getMe"# expected response: {"ok":true,"result":{"id":...,"is_bot":true,...}}
```

### Step 4: Point Hermes at the local server​

Add the URLs underplatforms.telegram.extrain~/.hermes/config.yaml:

`platforms.telegram.extra`
`~/.hermes/config.yaml`

```
platforms:  telegram:    extra:      base_url: "http://127.0.0.1:8081/bot"      base_file_url: "http://127.0.0.1:8081/file/bot"      local_mode: true        # see Step 5 below — only set this if the bot's data                              # directory is readable by the Hermes process
```

`platforms.telegram.extra`
`telegram.extra`

At the moment only theplatforms.<name>.extraform is deep-merged into the platform config. Keys placed directly under a top-leveltelegram.extrablock are silently dropped.

`platforms.<name>.extra`
`telegram.extra`

Whenbase_urlis set, Hermes:

`base_url`
- Builds the python-telegram-bot client against the local server
- Auto-lifts its internal document/audio size cap from 20 MB → 2 GB
- Reports the active limit in the "too large" error message (Maximum: 2048 MB.) so it's obvious which mode you're in

`Maximum: 2048 MB.`

Restart the gateway and look for a confirmation log line:

```
hermes gateway restartgrep -E "Using custom Telegram base_url|Using Telegram local_mode" ~/.hermes/logs/gateway.log | tail
```

### Step 5:local_mode— file access on disk​

`local_mode`

The local server hastwo waysto deliver files:

1. Without--local(the default): files are served over HTTP at/file/bot<TOKEN>/<path>, same as the public Bot API. The 20MB ceiling stays in effect. Useful as a network-fix only (e.g. whenapi.telegram.orgis unreachable but you can self-host); not what you want for the size lift.
2. With--local(set viaTELEGRAM_LOCAL=1above): files are written to the server's filesystem and thegetFileresponse returns anabsolute pathinstead of an HTTP URL. The 20MB ceiling is lifted. Hermes must then read the bytesfrom disk, not over HTTP.

`--local`
`/file/bot<TOKEN>/<path>`
`api.telegram.org`
`--local`
`TELEGRAM_LOCAL=1`
`getFile`

To make the disk-read path work, setlocal_mode: truein the config aboveandmake sure the Hermes process can read the path the server returns. Two scenarios:

`local_mode: true`
- Same machine— telegram-bot-api and Hermes run on the same host. Bind-mount the data volume to a directory that Hermes can read (e.g.,/var/lib/telegram-bot-api), and make sure the file ownership matches. The container drops privileges to its internaltelegram-bot-apiuser (uid varies by image); the simplest fix is to adduser: "<UID>:<GID>"to the compose service so files are owned by a uid Hermes already runs as.
- Different machines— the bot server runs on one host (e.g., a NAS, a separate VM) and Hermes on another. The server's data directory must be shared with the Hermes machine at thesame absolute paththe server reports (typically/var/lib/telegram-bot-api). NFS works well for this; CIFS/SMB withuid=mount remapping is friendlier if you don't want to deal with uid mismatches at the filesystem level.

`/var/lib/telegram-bot-api`
`telegram-bot-api`
`user: "<UID>:<GID>"`
`/var/lib/telegram-bot-api`
`uid=`

Iflocal_mode: trueis set but Hermes can'tstatthe returned file path (permissions or wrong mount), python-telegram-bot silently falls back to an HTTPgetFileagainst the local server — which in--localmode responds with404 Not Found. The symptom shows up ingateway.logas:

`local_mode: true`
`stat`
`getFile`
`--local`
`404 Not Found`
`gateway.log`

```
[Telegram] Failed to cache voice: Not Foundtelegram.error.InvalidToken: Not Found
```

If you see that, the cap-lift is working but the file-share isn't. Verifyls -la /var/lib/telegram-bot-api/<TOKEN>/voice/from the Hermes host as the user the gateway runs as, and confirm a single file iscat-able without a permission error.

`ls -la /var/lib/telegram-bot-api/<TOKEN>/voice/`
`cat`

### Step 6: Test it​

Send the bot a voice note or audio file that's bigger than 20 MB. Tail the gateway log:

```
tail -f ~/.hermes/logs/gateway.log | grep -iE "telegram|cache"
```

You should see a[Telegram] Cached user voice at /home/<user>/.hermes/cache/audio/...line andno"too large" rejection. Combined withstt.enabled: false(above), the path to the original audio file then lands in the agent's inbound message for downstream processing.

`[Telegram] Cached user voice at /home/<user>/.hermes/cache/audio/...`
`stt.enabled: false`

## Group Chat Usage​

Hermes Agent works in Telegram group chats with a few considerations:

- Privacy modedetermines what messages the bot can see (seeStep 3)
- TELEGRAM_ALLOWED_USERSstill applies — only authorized users can trigger the bot, even in groups
- You can keep the bot from responding to ordinary group chatter withtelegram.require_mention: true
- Withtelegram.require_mention: true, group messages are accepted when they are:replies to one of the bot's messages@botusernamementions/command@botusername(Telegram's bot-menu command form that includes the bot name)matches for one of your configured regex wake words intelegram.mention_patterns
- In groups with multiple Hermes bots,telegram.exclusive_bot_mentionskeeps routing deterministic. When a message explicitly mentions one or more Telegram bot usernames, only the mentioned bot profiles process it; other Hermes bots ignore it before reply and wake-word fallbacks run. This is enabled by default.
- Usetelegram.ignored_threadsto keep Hermes silent in specific Telegram forum topics, even when the group would otherwise allow free responses or mention-triggered replies
- Iftelegram.require_mentionis left unset or false, Hermes keeps the previous open-group behavior and responds to normal group messages it can see

`TELEGRAM_ALLOWED_USERS`
`telegram.require_mention: true`
`telegram.require_mention: true`
- replies to one of the bot's messages
- @botusernamementions
- /command@botusername(Telegram's bot-menu command form that includes the bot name)
- matches for one of your configured regex wake words intelegram.mention_patterns

`@botusername`
`/command@botusername`
`telegram.mention_patterns`
`telegram.exclusive_bot_mentions`
`telegram.ignored_threads`
`telegram.require_mention`

### Multiple Hermes bots in one group​

If you run several Hermes profiles in the same Telegram group, create one Telegram bot token per profile and start one gateway per profile. Do not reuse the same bot token in multiple running gateways; Telegram will reject concurrent polling for the same token.

Recommended group config:

```
telegram:  require_mention: true  exclusive_bot_mentions: true  mention_patterns: []
```

With this setup, a group message like@research_bot @ops_bot summarize thisis processed byresearch_botandops_botonly. Other Hermes bots in the group stay silent, even if the message is a reply to one of their earlier messages or would otherwise match a shared wake word.

`@research_bot @ops_bot summarize this`
`research_bot`
`ops_bot`

Setexclusive_bot_mentions: falseonly for legacy groups where explicit mentions should not override reply and wake-word triggers.

`exclusive_bot_mentions: false`

To operate several profiles, run the gateway command once per profile. For example:

```
# default profilehermes gateway starthermes gateway statushermes gateway stop# named profileshermes -p research gateway starthermes -p research gateway statushermes -p research gateway stop
```

For a small fixed fleet, use a shell loop or script that callshermes gateway <action>for the default profile andhermes -p <profile> gateway <action>for each named profile. This is more reliable than assuming a single process-level command controls every named profile on every service manager.

`hermes gateway <action>`
`hermes -p <profile> gateway <action>`

### Troubleshooting: works in DMs but not groups​

If the bot responds in a private chat but stays silent in a group, check these
gates in order:

1. Telegram delivery:turn off BotFather privacy mode, promote the bot to
admin, or mention the bot directly. Hermes cannot respond to group messages
that Telegram never delivers to the bot.
2. Rejoin after changing privacy:remove the bot from the group and add it
again after changing BotFather privacy settings. Telegram may keep the old
delivery behavior for existing memberships.
3. Hermes authorization:make sure the sender is listed inTELEGRAM_ALLOWED_USERSorTELEGRAM_GROUP_ALLOWED_USERS, or allow the
group chat withTELEGRAM_GROUP_ALLOWED_CHATS.
4. Mention filters:iftelegram.require_mention: trueis set, normal
group chatter is ignored unless the message is a slash command, reply to the
bot,@botusernamemention, or configuredmention_patternsmatch.
5. Multi-bot routing:if a group contains several bots, make sure each
Hermes profile uses a unique bot token and keepexclusive_bot_mentionsenabled unless you intentionally want legacy shared-trigger behavior.

`TELEGRAM_ALLOWED_USERS`
`TELEGRAM_GROUP_ALLOWED_USERS`
`TELEGRAM_GROUP_ALLOWED_CHATS`
`telegram.require_mention: true`
`@botusername`
`mention_patterns`
`exclusive_bot_mentions`

Negative chat IDs are normal for Telegram groups and supergroups. If you use
chat-scoped authorization, put those IDs inTELEGRAM_GROUP_ALLOWED_CHATS, not
the sender-user allowlist.

`TELEGRAM_GROUP_ALLOWED_CHATS`

### Example group trigger configuration​

Add this to~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
telegram:  require_mention: true  exclusive_bot_mentions: true  mention_patterns:    - "^\\s*chompy\\b"  ignored_threads:    - 31    - "42"
```

This example allows all the usual direct triggers plus messages that begin withchompy, even if they do not use an@mention.
Messages in Telegram topics31and42are always ignored before the mention and free-response checks run.

`chompy`
`@mention`
`31`
`42`

### Notes onmention_patterns​

`mention_patterns`
- Patterns use Python regular expressions
- Matching is case-insensitive
- Patterns are checked against both text messages and media captions
- Invalid regex patterns are ignored with a warning in the gateway logs rather than crashing the bot
- If you want a pattern to match only at the start of a message, anchor it with^

`^`

## Private Chat Topics (Bot API 9.4)​

Telegram Bot API 9.4 (February 2026) introducedPrivate Chat Topics— bots can create forum-style topic threads directly in 1-on-1 DM chats, no supergroup needed. This lets you run multiple isolated workspaces within your existing DM with Hermes.

### Use case​

If you work on several long-running projects, topics keep their context separate:

- Topic "Website"— work on your production web service
- Topic "Research"— literature review and paper exploration
- Topic "General"— miscellaneous tasks and quick questions

Each topic gets its own conversation session, history, and context — completely isolated from the others.

### Configuration​

Before adding topics to your config, the user mustenable Topics modein the DM chat with the bot:

1. Open your private chat with the Hermes bot in Telegram
2. Tap the bot's name at the top to open chat info
3. EnableTopics(the toggle to turn the chat into a forum)

Without this, Hermes will logThe chat is not a forumon startup and skip topic creation. This is a Telegram client-side setting — the bot cannot enable it programmatically.

`The chat is not a forum`

Add topics underplatforms.telegram.extra.dm_topicsin~/.hermes/config.yaml:

`platforms.telegram.extra.dm_topics`
`~/.hermes/config.yaml`

```
platforms:  telegram:    extra:      dm_topics:      - chat_id: 123456789        # Your Telegram user ID        topics:        - name: General          icon_color: 7322096        - name: Website          icon_color: 9367192        - name: Research          icon_color: 16766590          skill: arxiv              # Auto-load a skill in this topic
```

Fields:

| Field | Required | Description |
| --- | --- | --- |
| name | Yes | Topic display name |
| icon_color | No | Telegram icon color code (integer) |
| icon_custom_emoji_id | No | Custom emoji ID for the topic icon |
| skill | No | Skill to auto-load on new sessions in this topic |
| thread_id | No | Auto-populated after topic creation — don't set manually |

`name`
`icon_color`
`icon_custom_emoji_id`
`skill`
`thread_id`

### How it works​

1. On gateway startup, Hermes callscreateForumTopicfor each topic that doesn't have athread_idyet
2. Thethread_idis saved back toconfig.yamlautomatically — subsequent restarts skip the API call
3. Each topic maps to an isolated session key:agent:main:telegram:dm:{chat_id}:{thread_id}
4. Messages in each topic have their own conversation history, memory flush, and context window

`createForumTopic`
`thread_id`
`thread_id`
`config.yaml`
`agent:main:telegram:dm:{chat_id}:{thread_id}`

### Root DM handling​

By default, messages sent to the root DM (outside any topic) are processed
normally. Setignore_root_dm: trueto turn the root DM into a lobby — normal
messages are silently ignored for users who have DM topics configured, while
system commands (/start,/help,/status, etc.) still work.

`ignore_root_dm: true`
`/start`
`/help`
`/status`

```
platforms:  telegram:    extra:      ignore_root_dm: true      dm_topics:        - chat_id: 123456789          topics:            - name: General
```

The check isper-chat: only users with at least one entry indm_topicswill have their root DM affected. Users without configured topics are
unaffected.

`dm_topics`

### Skill binding​

Topics with askillfield automatically load that skill when a new session starts in the topic. This works exactly like typing/skill-nameat the start of a conversation — the skill content is injected into the first message, and subsequent messages see it in the conversation history.

`skill`
`/skill-name`

For example, a topic withskill: arxivwill have the arxiv skill pre-loaded whenever its session resets (due to idle timeout, daily reset, or manual/reset).

`skill: arxiv`
`/reset`

Topics created outside of the config (e.g., by manually calling the Telegram API) are discovered automatically when aforum_topic_createdservice message arrives. You can also add topics to the config while the gateway is running — they'll be picked up on the next cache miss.

`forum_topic_created`

## Multi-session DM mode (/topic)​

`/topic`

A ChatGPT-style multi-session DM — one bot, many parallel conversations. Unlike the operator-curatedextra.dm_topicsabove, this mode isuser-driven: no config, no pre-declared topic names. The end user flips it on with/topic, then taps the Telegram+button to create as many topics as they want, each one a fully independent Hermes session.

`extra.dm_topics`
`/topic`

### /topicsubcommands​

`/topic`
| Form | Context | Effect |
| --- | --- | --- |
| /topic | Root DM, not yet enabled | Check BotFather capabilities, enable multi-session mode, create pinned System topic |
| /topic | Root DM, already enabled | Show status: unlinked sessions available for restore |
| /topic | Inside a topic | Show the current topic's session binding |
| /topic help | Any | Inline usage |
| /topic off | Root DM | Disable multi-session mode and clear all topic bindings for this chat |
| /topic <session-id> | Inside a topic | Restore a previous Telegram session into the current topic |

`/topic`
`/topic`
`/topic`
`/topic help`
`/topic off`
`/topic <session-id>`

Only authorized users (allowlist viaTELEGRAM_ALLOWED_USERS/ platform auth config) can run/topic. An unauthorized sender gets a refusal instead of activation.

`TELEGRAM_ALLOWED_USERS`
`/topic`

### DM Topics vs Multi-session DM mode​

|  | extra.dm_topics(config-driven) | /topic(user-driven) |
| --- | --- | --- |
| Who activates it | Operator, inconfig.yaml | End user, by sending/topic |
| Topic list | Fixed set declared in config | User creates/deletes topics freely |
| Topic names | Chosen by operator | Chosen by user; auto-renamed to match Hermes session title |
| Root DM behavior | Normal chat (lobby ifignore_root_dm: true) | Becomes a system lobby (non-command messages are rejected) |
| Primary use case | Permanent workspaces with optional skill binding | Ad-hoc parallel sessions |
| Persistence | extra.dm_topicsin config | telegram_dm_topic_mode+telegram_dm_topic_bindingsSQLite tables |

`extra.dm_topics`
`/topic`
`config.yaml`
`/topic`
`ignore_root_dm: true`
`extra.dm_topics`
`telegram_dm_topic_mode`
`telegram_dm_topic_bindings`

Both features can coexist on the same bot — you'd run/topicfrom a user's DM, andextra.dm_topicscontinues to manage operator-declared topics for other chats.

`/topic`
`extra.dm_topics`

### Prerequisites​

In@BotFather, open your bot →Bot Settings → Threads Settings:

1. Turn onThreaded Mode(enableshas_topics_enabled)
2. Donotdisable users creating topics (keepsallows_users_to_create_topicson)

`has_topics_enabled`
`allows_users_to_create_topics`

When the user first runs/topic, Hermes callsgetMeto verify both flags. If either is off, Hermes sends a screenshot of the BotFather Threads Settings page and explains what to toggle — no activation happens until prerequisites are met.

`/topic`
`getMe`

### Activation flow​

From the root DM, send:

```
/topic
```

Hermes will:

1. CheckgetMe().has_topics_enabledandallows_users_to_create_topics
2. If both are true, enable multi-session topic mode for this DM
3. Create and pin aSystemtopic for status/commands (best-effort)
4. Reply with a list of previous unlinked Telegram sessions the user can restore

`getMe().has_topics_enabled`
`allows_users_to_create_topics`

After activation, theroot DM is a lobby: normal prompts are rejected with guidance pointing atAll Messages. System commands (/status,/sessions,/usage,/help, etc.) still work in the root.

`/status`
`/sessions`
`/usage`
`/help`

### Creating a new topic (end-user flow)​

1. Open the bot DM in Telegram
2. TapAll Messagesat the top of the bot interface, then send any message
3. Telegram creates a new topic for that message
4. Hermes responds inside that topic — the topic is now a standalone session

Every topic gets its own conversation history, model state, tool execution, and session ID. The isolation key isagent:main:telegram:dm:{chat_id}:{thread_id}— identical to the config-driven DM topics isolation.

`agent:main:telegram:dm:{chat_id}:{thread_id}`

### Auto-renamed topics​

When Hermes generates a session title for a topic (via the auto-title pipeline, after the first exchange), the Telegram topic itself is renamed to match — e.g. "New Topic" becomes "Database migration plan". The rename is best-effort: failures are logged but don't break the session.

To disable this and keep your manually-chosen topic names untouched, set:

```
gateway:  platforms:    telegram:      extra:        disable_topic_auto_rename: true
```

When this flag is on, Hermes still generates an internal session title (used byhermes sessions, the TUI, etc.) but never edits the Telegram topic name. Useful when you organise topics by hand under BotFather Threaded Mode and don't want every first reply to overwrite the title.

`hermes sessions`

### /newinside a topic​

`/new`

Resets the current topic's session (new session ID, fresh history) without touching other topics. Hermes replies with a reminder that for parallel work, creating another topic (viaAll Messages) is usually what you want.

### Restoring a previous session​

Inside a topic, send:

```
/topic <session-id>
```

This binds the current topic to an existing Hermes session instead of starting fresh. Useful for continuing a conversation that started before topic mode was enabled. Restrictions:

- The target session must belong to the same Telegram user
- The target session must not already be bound to another topic

Hermes confirms with the session title and replays the last assistant message for context.

To discover session IDs, send/topic(no argument) in the root DM — Hermes lists the user's unlinked Telegram sessions.

`/topic`

### /topicinside a topic (no argument)​

`/topic`

Shows the current topic's binding: session title, session ID, and hints for/newvs creating another topic.

`/new`

### Under the hood​

- Activation persists totelegram_dm_topic_mode(chat_id, user_id, enabled, ...)instate.db
- Each topic binding persists totelegram_dm_topic_bindings(chat_id, thread_id, session_id, ...)withON DELETE CASCADEonsession_id— pruning a session automatically clears its topic binding
- The topic-mode SQLite migration isopt-in: it runs on the first/topiccall, never on gateway startup. Until a user runs/topicin this profile,state.dbis unchanged
- Each inbound DM message looks up its(chat_id, thread_id)binding. If present, the lookup routes the message to the bound session viaSessionStore.switch_session()so the session-key-to-session-id mapping stays consistent on disk
- /newinside a topic rewrites the binding row to point at the new session ID, so the next message stays on the fresh session
- Topics declared inextra.dm_topicsarenever auto-renamed— the operator-chosen name is preserved even when multi-session mode is enabled
- Setextra.disable_topic_auto_rename: trueto turn off auto-rename foralltopics in the chat (ad-hoc topics created via Threaded Mode included)
- The General (pinned top) topic in a forum-enabled DM is treated as the root lobby, regardless of whether Telegram delivers its messages withmessage_thread_id=1or with no thread_id
- Root-lobby reminders are rate-limited to one message per 30 seconds per chat — a user who forgets topic mode is on and types ten prompts in the root won't get ten replies
- BotFather setup screenshots are rate-limited to one send per 5 minutes per chat — repeated/topicattempts while Threads Settings are still disabled won't re-upload the same image
- /background <prompt>started inside a topic delivers its result back to the same topic; background sessions don't trigger auto-rename of the owning topic
- /topicitself is gated by the bot's user authorization check — unauthorized DMs get a refusal instead of activation

`telegram_dm_topic_mode(chat_id, user_id, enabled, ...)`
`state.db`
`telegram_dm_topic_bindings(chat_id, thread_id, session_id, ...)`
`ON DELETE CASCADE`
`session_id`
`/topic`
`/topic`
`state.db`
`(chat_id, thread_id)`
`SessionStore.switch_session()`
`/new`
`extra.dm_topics`
`extra.disable_topic_auto_rename: true`
`message_thread_id=1`
`/topic`
`/background <prompt>`
`/topic`

### Disabling multi-session mode​

Send/topic offin the root DM. Hermes flips the row off, clears the chat's(thread_id → session_id)bindings, and the root DM reverts to a normal Hermes chat. Existing topics in Telegram aren't deleted — they just stop being gated as independent sessions. Re-run/topiclater to turn it back on.

`/topic off`
`(thread_id → session_id)`
`/topic`

If you need to clean up by hand (e.g. a bulk reset across many chats), remove the rows directly:

```
sqlite3 ~/.hermes/state.db \  "UPDATE telegram_dm_topic_mode SET enabled = 0 WHERE chat_id = '<your_chat_id>'; \   DELETE FROM telegram_dm_topic_bindings WHERE chat_id = '<your_chat_id>';"
```

### Downgrading Hermes​

If you downgrade to a Hermes version that predates/topic, the feature simply stops working — thetelegram_dm_topic_modeandtelegram_dm_topic_bindingstables remain instate.dbbut are ignored by older code. DMs revert to the native per-thread isolation (eachmessage_thread_idstill gets its own session viabuild_session_key), so your existing Telegram topics keep working as parallel sessions. The root DM is no longer a lobby — messages there go into the agent like they used to. Re-upgrading reactivates multi-session mode exactly where it was.

`/topic`
`telegram_dm_topic_mode`
`telegram_dm_topic_bindings`
`state.db`
`message_thread_id`
`build_session_key`

## Group Forum Topic Skill Binding​

Supergroups withTopics modeenabled (also called "forum topics") already get session isolation per topic — eachthread_idmaps to its own conversation. But you may want toauto-load a skillwhen messages arrive in a specific group topic, just like DM topic skill binding works.

`thread_id`

### Use case​

A team supergroup with forum topics for different workstreams:

- Engineeringtopic → auto-loads thesoftware-developmentskill
- Researchtopic → auto-loads thearxivskill
- Generaltopic → no skill, general-purpose assistant

`software-development`
`arxiv`

### Configuration​

Add topic bindings underplatforms.telegram.extra.group_topicsin~/.hermes/config.yaml:

`platforms.telegram.extra.group_topics`
`~/.hermes/config.yaml`

```
platforms:  telegram:    extra:      group_topics:      - chat_id: -1001234567890       # Supergroup ID        topics:        - name: Engineering          thread_id: 5          skill: software-development        - name: Research          thread_id: 12          skill: arxiv        - name: General          thread_id: 1          # No skill — general purpose
```

Fields:

| Field | Required | Description |
| --- | --- | --- |
| chat_id | Yes | The supergroup's numeric ID (negative number starting with-100) |
| name | No | Human-readable label for the topic (informational only) |
| thread_id | Yes | Telegram forum topic ID — visible int.me/c/<group_id>/<thread_id>links |
| skill | No | Skill to auto-load on new sessions in this topic |

`chat_id`
`-100`
`name`
`thread_id`
`t.me/c/<group_id>/<thread_id>`
`skill`

### How it works​

1. When a message arrives in a mapped group topic, Hermes looks up thechat_idandthread_idingroup_topicsconfig
2. If a matching entry has askillfield, that skill is auto-loaded for the session — identical to DM topic skill binding
3. Topics without askillkey get session isolation only (existing behavior, unchanged)
4. Unmappedthread_idvalues orchat_idvalues fall through silently — no error, no skill

`chat_id`
`thread_id`
`group_topics`
`skill`
`skill`
`thread_id`
`chat_id`

### Differences from DM Topics​

|  | DM Topics | Group Topics |
| --- | --- | --- |
| Config key | extra.dm_topics | extra.group_topics |
| Topic creation | Hermes creates topics via API ifthread_idis missing | Admin creates topics in Telegram UI |
| thread_id | Auto-populated after creation | Must be set manually |
| icon_color/icon_custom_emoji_id | Supported | Not applicable (admin controls appearance) |
| Skill binding | ✓ | ✓ |
| Session isolation | ✓ | ✓ (already built-in for forum topics) |

`extra.dm_topics`
`extra.group_topics`
`thread_id`
`thread_id`
`icon_color`
`icon_custom_emoji_id`

To find a topic'sthread_id, open the topic in Telegram Web or Desktop and look at the URL:https://t.me/c/1234567890/5— the last number (5) is thethread_id. Thechat_idfor supergroups is the group ID prefixed with-100(e.g., group1234567890becomes-1001234567890).

`thread_id`
`https://t.me/c/1234567890/5`
`5`
`thread_id`
`chat_id`
`-100`
`1234567890`
`-1001234567890`

## Recent Bot API Features​

- Bot API 9.4 (Feb 2026):Private Chat Topics — bots can create forum topics in 1-on-1 DM chats viacreateForumTopic. Hermes uses this for two distinct features: operator-curatedPrivate Chat Topics(config-driven, fixed topic list) and user-drivenMulti-session DM mode(activated by/topic, unlimited user-created topics).
- Privacy policy:Telegram now requires bots to have a privacy policy. Set one via BotFather with/setprivacy_policy, or Telegram may auto-generate a placeholder. This is particularly important if your bot is public-facing.
- Bot API 9.5 (Mar 2026): Native streaming viasendMessageDraft.Hermes supports Telegram's native streaming-draft API as an opt-in transport for private chats. The default remains the legacyeditMessageTextpath because draft previews can visibly collapse and re-render on some Telegram clients.

`createForumTopic`
`/topic`
`/setprivacy_policy`
`sendMessageDraft`
`editMessageText`

### Streaming transport (gateway.streaming.transport)​

`gateway.streaming.transport`

When streaming is enabled (gateway.streaming.enabled: true), Hermes picks one of four transports:

`gateway.streaming.enabled: true`
| Value | Behaviour |
| --- | --- |
| auto(default) | Native draft streaming on supported chats (currently Telegram DMs); legacy edit-based path otherwise. Falls back gracefully if a draft frame fails. |
| draft | Force native drafts. Logs a downgrade and falls back to edit if the chat doesn't support drafts (e.g. groups/topics). |
| edit | Legacy progressiveeditMessageTextpolling for every chat type. |
| off | Disable streaming entirely (final reply only, no progressive updates). |

`auto`
`draft`
`edit`
`editMessageText`
`off`

In~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
gateway:  streaming:    enabled: true    transport: auto    # auto | draft | edit | off
```

What you'll see in DMs withedit(default)— the gateway sends a normal preview message and progressively updates it viaeditMessageText, avoiding Telegram's draft-preview collapse/rollback effect.

`edit`
`editMessageText`

What you'll see in DMs withautoordraft— Telegram shows an animated draft preview that updates token-by-token. When the reply finishes, it's delivered as a regular message and the draft preview clears naturally on the client. Drafts have no message id, so the final answer is what stays in your chat history.

`auto`
`draft`

What about groups, supergroups, forum topics?Telegram restrictssendMessageDraftto private chats (DMs). The gateway transparently falls back to the edit-based path for everything else — same UX as before.

`sendMessageDraft`

What if a draft frame fails?Any failure (transient network error, server-side rejection, older python-telegram-bot install) flips that response back to the edit-based path for the rest of the stream. The next response gets a fresh attempt.

## Rendering: Rich Messages, Tables and Link Previews​

Rich Messages (Bot API 10.1).Final replies that contain constructs the legacy MarkdownV2 path degrades — tables, task lists, collapsible<details>, and block math — are sent with Telegram's nativesendRichMessageusing the agent'sraw markdown, so they render natively with no client-side flattening. During streaming, the final answer is delivered byediting the existing preview in placeviaeditMessageText'srich_messageparameter — no second message, no delete, so there is no duplicate-delivery flicker at the end of a turn. In DMs the live streaming preview also usessendRichMessageDraft, so the animated draft matches the final rich message. Ordinary replies (plain prose, bold/italic, simple lists) stay on the MarkdownV2 path for consistent font weight and spacing across clients.

`<details>`
`sendRichMessage`
`editMessageText`
`rich_message`
`sendRichMessageDraft`

The rich path is skipped automatically when content exceeds the 32,768-character rich text limit, and any rejection from Telegram (unsupported endpoint on an olderpython-telegram-bot, parser error, oversized blocks/columns)transparently falls backto the MarkdownV2 path — your message is never lost. Transient/network errors arenotsilently re-sent (no duplicate final message).

`python-telegram-bot`

MarkdownV2 fallback.When the rich path is unavailable for a message, Hermes converts markdown to MarkdownV2. Since MarkdownV2 has no native table syntax, pipe tables are normalized:

- Small tablesare flattened intorow-group bullets— each row becomes a readable bulleted list under the column headings. Good for 2–4 columns and short cells.
- Larger or wider tablesfall back to afenced code blockwith aligned columns so nothing collapses.

Rich messages areopt-in. The default stays on the legacy MarkdownV2 path because current Telegram clients can make Bot API rich messages difficult to copy as plain text, which is especially painful for command snippets and mobile handoffs. To enable native rendering for tables/task lists/details/math:

```
gateway:  platforms:    telegram:      extra:        rich_messages: true        rich_drafts: false
```

This setting is for client-rendering/copy compatibility; Hermes already falls back automatically when Telegram rejects the rich API call.rich_draftscontrols the experimental rich draft preview path during Telegram DM streaming and stays off by default because Telegram Desktop/macOS can visually overlay rich draft frames until the chat redraws. If you only want the legacy "always code-block" table behavior while keeping rich messages enabled, disable table normalization by settingtelegram.pretty_tables: falseinconfig.yaml(default:true).

`rich_drafts`
`telegram.pretty_tables: false`
`config.yaml`
`true`

Link previews.Telegram auto-generates link previews for URLs in bot messages. If you'd rather suppress those (long/toolsoutput, agent reply that mentions ten links, etc.):

`/tools`

```
gateway:  platforms:    telegram:      extra:        disable_link_previews: true
```

When enabled, Hermes attaches Telegram'sLinkPreviewOptions(is_disabled=True)to every outgoing message and falls back to the legacydisable_web_page_previewparameter on olderpython-telegram-botversions.

`LinkPreviewOptions(is_disabled=True)`
`disable_web_page_preview`
`python-telegram-bot`

## Group Allowlisting​

Telegram groups and forum chats have two orthogonal gates you can configure:

- Sender user IDs(group_allow_from/TELEGRAM_GROUP_ALLOWED_USERS) — sender-scoped allowlist that applies only to group/forum messages. Use this when you want specific users to be able to invoke the bot in groups without adding them toTELEGRAM_ALLOWED_USERS(which would also give them DM access).
- Chat IDs(group_allowed_chats/TELEGRAM_GROUP_ALLOWED_CHATS) — chat-scoped allowlist. Any member of these groups/forums can interact with the bot. Useful for team/support bots where group membership itself is the access signal.

`group_allow_from`
`TELEGRAM_GROUP_ALLOWED_USERS`
`TELEGRAM_ALLOWED_USERS`
`group_allowed_chats`
`TELEGRAM_GROUP_ALLOWED_CHATS`

```
gateway:  platforms:    telegram:      extra:        # Global access (DMs + groups). Users here can always invoke the bot.        allow_from:          - "123456789"        # Sender IDs allowed in groups/forums only. Does NOT grant DM access.        group_allow_from:          - "987654321"        # Entire groups/forums — any member is authorized.        group_allowed_chats:          - "-1001234567890"
```

Equivalent env vars:

```
TELEGRAM_ALLOWED_USERS="123456789"TELEGRAM_GROUP_ALLOWED_USERS="987654321"TELEGRAM_GROUP_ALLOWED_CHATS="-1001234567890"
```

Behavior:

- TELEGRAM_ALLOWED_USERScovers all chat types (DMs, groups, forums).
- TELEGRAM_GROUP_ALLOWED_USERSonly authorizes the listed senders in groups/forums. They still can't DM the bot unless listed inTELEGRAM_ALLOWED_USERS.
- A chat inTELEGRAM_GROUP_ALLOWED_CHATSauthorizes every member of that chat, regardless of sender.
- Use*in any of these to allow any sender/chat.
- This layers on top of existing mention/pattern triggers and on top ofgroup_topics+ignored_threads.

`TELEGRAM_ALLOWED_USERS`
`TELEGRAM_GROUP_ALLOWED_USERS`
`TELEGRAM_ALLOWED_USERS`
`TELEGRAM_GROUP_ALLOWED_CHATS`
`*`
`group_topics`
`ignored_threads`

### Migration from before PR #17686​

Prior to this split,TELEGRAM_GROUP_ALLOWED_USERSwas the only knob and users putchat IDsin it. For backward compatibility, chat-ID-shaped values (starting with-) inTELEGRAM_GROUP_ALLOWED_USERSare still honored as chat IDs and a deprecation warning is logged once. Migration:

`TELEGRAM_GROUP_ALLOWED_USERS`
`-`
`TELEGRAM_GROUP_ALLOWED_USERS`

```
# Old (still works, but deprecated)TELEGRAM_GROUP_ALLOWED_USERS="-1001234567890"# NewTELEGRAM_GROUP_ALLOWED_CHATS="-1001234567890"
```

### Guest @mention bypass (guest_mode)​

`guest_mode`

In a typical setup,group_allowed_chatsis a hard gate: messages from groups outside the list are silently dropped, even if a member explicitly @mentions the bot. That's the right default for support / team bots.

`group_allowed_chats`

For more casual setups — friend group chats where you want the botmostly silentbutoccasionally available on explicit ping— enableguest_mode:

`guest_mode`

```
gateway:  platforms:    telegram:      extra:        group_allowed_chats:          - "-1001234567890"   # your main allowlisted group        guest_mode: true       # non-allowlisted groups: allow on @mention only
```

Env equivalent:

```
TELEGRAM_GUEST_MODE=true
```

Default:false.

`false`

Withguest_mode: true, a message from a non-allowlisted group is processedonlyif it explicitly @mentions the bot. The mention is required every turn — there's no session stickiness for guest interactions, so the bot never auto-engages in a friend group thread it isn't pinged into.

`guest_mode: true`

DMs and allowlisted groups behave exactly as before.

## Slash Command Access Control​

By default, every allowed user can run every slash command. To split your allowlist intoadmins(full slash command access) andregular users(only commands you explicitly enable), addallow_admin_fromanduser_allowed_commandsto the platform'sextrablock:

`allow_admin_from`
`user_allowed_commands`
`extra`

```
gateway:  platforms:    telegram:      extra:        # Existing allowlists (unchanged)        allow_from:          - "123456789"     # admin          - "555555555"     # regular user          - "777777777"     # regular user        # NEW — admins get all slash commands (built-in + plugin)        allow_admin_from:          - "123456789"        # NEW — non-admin allowed users can only run these slash commands.        # /help and /whoami are always allowed so users can see their access.        user_allowed_commands:          - status          - model          - history        # Optional: separate admin/command lists for groups        group_allow_admin_from:          - "123456789"        group_user_allowed_commands:          - status
```

Behavior:

- A user listed inallow_admin_fromfor a scope (DM or group) can runeveryregistered slash command — built-in commands AND plugin-registered ones — through the live registry.
- A user inallow_frombutnotinallow_admin_fromcan only run commands listed inuser_allowed_commands, plus the always-allowed floor:/helpand/whoami.
- Plain chat (non-slash messages) is unaffected. Non-admin users can still talk to the agent normally, they just can't trigger arbitrary commands.
- Backward compat:ifallow_admin_fromis not set for a scope, slash command gating is disabled for that scope. Existing installs keep working with no changes.
- DM admin status does not imply group admin status. Each scope has its own admin list.
- If onlygroup_allow_admin_fromis set, DM scope stays in unrestricted (backward-compat) mode.

`allow_admin_from`
`allow_from`
`allow_admin_from`
`user_allowed_commands`
`/help`
`/whoami`
`allow_admin_from`
`group_allow_admin_from`

Use/whoamito see the active scope, your tier (admin / user / unrestricted), and which slash commands you can run.

`/whoami`

## Interactive Model Picker​

When you send/modelwith no arguments in a Telegram chat, Hermes shows an interactive inline keyboard for switching models:

`/model`
1. Provider selection— buttons showing each available provider with model counts (e.g., "OpenAI (15)", "✓ Anthropic (12)" for the current provider).
2. Model selection— paginated model list withPrev/Nextnavigation, aBackbutton to return to providers, andCancel.

The current model and provider are displayed at the top. All navigation happens by editing the same message in-place (no chat clutter).

If you know the exact model name, type/model <name>directly to skip the picker. You can also type/model <name> --globalto persist the change across sessions.

`/model <name>`
`/model <name> --global`

## DNS-over-HTTPS Fallback IPs​

In some restricted networks,api.telegram.orgmay resolve to an IP that is unreachable. The Telegram adapter includes afallback IPmechanism that transparently retries connections against alternative IPs while preserving the correct TLS hostname and SNI.

`api.telegram.org`

### How it works​

1. IfTELEGRAM_FALLBACK_IPSis set, those IPs are used directly.
2. Otherwise, the adapter automatically queriesGoogle DNSandCloudflare DNSvia DNS-over-HTTPS (DoH) to discover alternative IPs forapi.telegram.org.
3. IPs returned by DoH that differ from the system DNS result are used as fallbacks.
4. If DoH is also blocked, a hardcoded seed IP (149.154.167.220) is used as a last resort.
5. Once a fallback IP succeeds, it becomes "sticky" — subsequent requests use it directly without retrying the primary path first.

`TELEGRAM_FALLBACK_IPS`
`api.telegram.org`
`149.154.167.220`

### Configuration​

```
# Explicit fallback IPs (comma-separated)TELEGRAM_FALLBACK_IPS=149.154.167.220,149.154.167.221
```

Or in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
platforms:  telegram:    extra:      fallback_ips:        - "149.154.167.220"
```

You usually don't need to configure this manually. The auto-discovery via DoH handles most restricted-network scenarios. TheTELEGRAM_FALLBACK_IPSenv var is only needed if DoH is also blocked on your network.

`TELEGRAM_FALLBACK_IPS`

## Proxy Support​

If your network requires an HTTP proxy to reach the internet (common in corporate environments), the Telegram adapter automatically reads standard proxy environment variables and routes all connections through the proxy.

### Supported variables​

The adapter checks these environment variables in order, using the first one that is set:

1. HTTPS_PROXY
2. HTTP_PROXY
3. ALL_PROXY
4. https_proxy/http_proxy/all_proxy(lowercase variants)

`HTTPS_PROXY`
`HTTP_PROXY`
`ALL_PROXY`
`https_proxy`
`http_proxy`
`all_proxy`

### Configuration​

Set the proxy in your environment before starting the gateway:

```
export HTTPS_PROXY=http://proxy.example.com:8080hermes gateway
```

Or add it to~/.hermes/.env:

`~/.hermes/.env`

```
HTTPS_PROXY=http://proxy.example.com:8080
```

The proxy applies to both the primary transport and all fallback IP transports. No additional Hermes configuration is needed — if the environment variable is set, it's used automatically.

This covers the custom fallback transport layer that Hermes uses for Telegram connections. The standardhttpxclient used elsewhere already respects proxy env vars natively.

`httpx`

## Message Reactions​

The bot can add emoji reactions to messages as visual processing feedback:

- 👀 when the bot starts processing your message
- ✅ when the response is delivered successfully
- ❌ if an error occurs during processing

Reactions aredisabled by default. Enable them inconfig.yaml:

`config.yaml`

```
telegram:  reactions: true
```

Or via environment variable:

```
TELEGRAM_REACTIONS=true
```

Unlike Discord (where reactions are additive), Telegram's Bot API replaces all bot reactions in a single call. The transition from 👀 to ✅/❌ happens atomically — you won't see both at once.

If the bot doesn't have permission to add reactions in a group, the reaction calls fail silently and message processing continues normally.

## Per-Channel Prompts​

Assign ephemeral system prompts to specific Telegram groups or forum topics. The prompt is injected at runtime on every turn — never persisted to transcript history — so changes take effect immediately.

```
telegram:  channel_prompts:    "-1001234567890": |      You are a research assistant. Focus on academic sources,      citations, and concise synthesis.    "42":  |      This topic is for creative writing feedback. Be warm and      constructive.
```

Keys are chat IDs (groups/supergroups) or forum topic IDs. For forum groups, topic-level prompts override the group-level prompt:

- Message in topic42inside group-1001234567890→ uses topic42's prompt
- Message in topic99(no explicit entry) → falls back to group-1001234567890's prompt
- Message in a group with no entry → no channel prompt applied

`42`
`-1001234567890`
`42`
`99`
`-1001234567890`

Numeric YAML keys are automatically normalized to strings.

## Troubleshooting​

| Problem | Solution |
| --- | --- |
| Bot not responding at all | VerifyTELEGRAM_BOT_TOKENis correct. Checkhermes gatewaylogs for errors. |
| Bot responds with "unauthorized" | Your user ID is not inTELEGRAM_ALLOWED_USERS. Double-check with @userinfobot. |
| Bot ignores group messages | Privacy mode is likely on. Disable it (Step 3) or make the bot a group admin.Remember to remove and re-add the bot after changing privacy. |
| Voice messages not transcribed | Verify STT is available: installfaster-whisperfor local transcription, or setGROQ_API_KEY/VOICE_TOOLS_OPENAI_KEYin~/.hermes/.env. |
| Voice replies are files, not bubbles | Installffmpeg(needed for Edge TTS Opus conversion). |
| Bot token revoked/invalid | Generate a new token via/revokethen/newbotor/tokenin BotFather. Update your.envfile. |
| Webhook not receiving updates | VerifyTELEGRAM_WEBHOOK_URLis publicly reachable (test withcurl). Ensure your platform/reverse proxy routes inbound HTTPS traffic from the URL's port to the local listen port configured byTELEGRAM_WEBHOOK_PORT(they do not need to be the same number). Ensure SSL/TLS is active — Telegram only sends to HTTPS URLs. Check firewall rules. |

`TELEGRAM_BOT_TOKEN`
`hermes gateway`
`TELEGRAM_ALLOWED_USERS`
`faster-whisper`
`GROQ_API_KEY`
`VOICE_TOOLS_OPENAI_KEY`
`~/.hermes/.env`
`ffmpeg`
`/revoke`
`/newbot`
`/token`
`.env`
`TELEGRAM_WEBHOOK_URL`
`curl`
`TELEGRAM_WEBHOOK_PORT`

## Exec Approval​

When the agent tries to run a potentially dangerous command, it asks you for approval in the chat:

> ⚠️ This command is potentially dangerous (recursive delete). Reply "yes" to approve.

⚠️ This command is potentially dangerous (recursive delete). Reply "yes" to approve.

Reply "yes"/"y" to approve or "no"/"n" to deny.

## Interactive Prompts (clarify)​

When the agent calls theclarifytool — to ask which approach you prefer, get post-task feedback, or check before a non-trivial decision — Telegram renders the question withinline keyboard buttons:

`clarify`

> ❓ Which framework should I use for the dashboard?[1. Next.js] [2. Remix] [3. Astro]
[✏️ Other (type answer)]

❓ Which framework should I use for the dashboard?

[1. Next.js] [2. Remix] [3. Astro]
[✏️ Other (type answer)]

Tap a button to answer, or tapOtherto type a free-form response (the next message you send becomes the answer). Open-endedclarifycalls (no preset choices) skip the buttons and just capture your next message.

`clarify`

Configure the response timeout viaagent.clarify_timeoutin~/.hermes/config.yaml(default600seconds). If you don't respond within the timeout, the agent unblocks with a sentinel message and adapts rather than hanging.

`agent.clarify_timeout`
`~/.hermes/config.yaml`
`600`

## Push notification volume​

Telegram fires a push notification on every message the bot sends. For long agent turns that emit tool-progress bubbles, streaming updates, and status callbacks, this gets noisy fast. The Telegram adapter has two notification modes:

| Mode | Behavior |
| --- | --- |
| important(default) | Onlyfinal responses,approval prompts, andslash-command confirmationsring. Tool progress, streaming chunks, and status messages are delivered withdisable_notification=true. |
| all | Every outgoing message fires a push notification. Legacy behavior; opt in if you genuinely want to hear about every tool call. |

`important`
`disable_notification=true`
`all`

Configure in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
display:  platforms:    telegram:      notifications: important   # or "all"
```

Env override (handy for quick A/B testing):

```
HERMES_TELEGRAM_NOTIFICATIONS=all
```

Unknown values log a warning and fall back toimportant.

`important`

## Status messages edited in place​

The Telegram adapter routes recurring agent status callbacks (e.g. "Compressing context…", "Calling tool…") throughsend_or_update_status(), which keeps a{(chat_id, status_key) → message_id}cache andedits the existing bubbleon subsequent emits instead of appending a new one each time. Distinctstatus_keyvalues get their own messages; distinct chats never collide. If the edit fails (e.g. the user deleted the message, or it's older than Telegram allows for edits), the cache entry is dropped and the next emit posts a fresh message and re-caches its ID. No config required — this is the default Telegram behavior. Other adapters that don't implementsend_or_update_statusfall through to plainsend()unchanged.

`send_or_update_status()`
`{(chat_id, status_key) → message_id}`
`status_key`
`send_or_update_status`
`send()`

## Pin incoming user message during agent turn​

When a user sends a message that triggers an agent turn, the Telegram adapter pins that incoming message for the duration of the turn and unpins it when the response is finished — a lightweight visual indicator that the bot is actively working on the message rather than ignoring it. The pin usesdisable_notification=trueto avoid extra pings. No config required.

`disable_notification=true`

## Security​

Always setTELEGRAM_ALLOWED_USERSto restrict who can interact with your bot. Without it, the gateway denies all users by default as a safety measure.

`TELEGRAM_ALLOWED_USERS`

Never share your bot token publicly. If compromised, revoke it immediately via BotFather's/revokecommand.

`/revoke`

For more details, see theSecurity documentation. You can also useDM pairingfor a more dynamic approach to user authorization.