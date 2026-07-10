- 
- Messaging Platforms
- Popular
- Signal

# Signal Setup

Hermes connects to Signal through thesignal-clidaemon running in HTTP mode. The adapter streams messages in real-time via SSE (Server-Sent Events) and sends responses via JSON-RPC.

Signal is the most privacy-focused mainstream messenger — end-to-end encrypted by default, open-source protocol, minimal metadata collection. This makes it ideal for security-sensitive agent workflows.

The Signal adapter useshttpx(already a core Hermes dependency) for all communication. No additional Python packages are required. You just need signal-cli installed externally.

`httpx`

## Prerequisites​

- signal-cli— Java-based Signal client (GitHub)
- Java 17+runtime — required by signal-cli
- A phone numberwith Signal installed (for linking as a secondary device)

### Installing signal-cli​

```
# macOSbrew install signal-cli# Linux (download latest release)VERSION=$(curl -Ls -o /dev/null -w %{url_effective} \  https://github.com/AsamK/signal-cli/releases/latest | sed 's/^.*\/v//')curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}.tar.gz"sudo tar xf "signal-cli-${VERSION}.tar.gz" -C /optsudo ln -sf "/opt/signal-cli-${VERSION}/bin/signal-cli" /usr/local/bin/
```

signal-cli isnotin apt or snap repositories. The Linux install above downloads directly fromGitHub releases.

## Step 1: Link Your Signal Account​

Signal-cli works as alinked device— like WhatsApp Web, but for Signal. Your phone stays the primary device.

```
# Generate a linking URI (displays a QR code or link)signal-cli link -n "HermesAgent"
```

1. OpenSignalon your phone
2. Go toSettings → Linked Devices
3. TapLink New Device
4. Scan the QR code or enter the URI

## Step 2: Start the signal-cli Daemon​

```
# Replace +1234567890 with your Signal phone number (E.164 format)signal-cli --account +1234567890 daemon --http 127.0.0.1:8080
```

Keep this running in the background. You can usesystemd,tmux,screen, or run it as a service.

`systemd`
`tmux`
`screen`

Verify it's running:

```
curl http://127.0.0.1:8080/api/v1/check# Should return: {"versions":{"signal-cli":...}}
```

## Step 3: Configure Hermes​

The easiest way:

```
hermes gateway setup
```

SelectSignalfrom the platform menu. The wizard will:

1. Check if signal-cli is installed
2. Prompt for the HTTP URL (default:http://127.0.0.1:8080)
3. Test connectivity to the daemon
4. Ask for your account phone number
5. Configure allowed users and access policies

`http://127.0.0.1:8080`

### Manual Configuration​

Add to~/.hermes/.env:

`~/.hermes/.env`

```
# RequiredSIGNAL_HTTP_URL=http://127.0.0.1:8080SIGNAL_ACCOUNT=+1234567890# Security (recommended)SIGNAL_ALLOWED_USERS=+1234567890,+0987654321    # Comma-separated E.164 numbers or UUIDs# OptionalSIGNAL_GROUP_ALLOWED_USERS=groupId1,groupId2     # Enable groups (omit to disable, * for all)SIGNAL_HOME_CHANNEL=+1234567890                  # Default delivery target for cron jobs
```

Then start the gateway:

```
hermes gateway              # Foregroundhermes gateway install      # Install as a user servicesudo hermes gateway install --system   # Linux only: boot-time system service
```

## Access Control​

### DM Access​

DM access follows the same pattern as all other Hermes platforms:

1. SIGNAL_ALLOWED_USERSset→ only those users can message
2. No allowlist set→ unknown users get a DM pairing code (approve viahermes pairing approve signal CODE)
3. SIGNAL_ALLOW_ALL_USERS=true→ anyone can message (use with caution)

`SIGNAL_ALLOWED_USERS`
`hermes pairing approve signal CODE`
`SIGNAL_ALLOW_ALL_USERS=true`

### Group Access​

Group access is controlled by theSIGNAL_GROUP_ALLOWED_USERSenv var:

`SIGNAL_GROUP_ALLOWED_USERS`
| Configuration | Behavior |
| --- | --- |
| Not set (default) | All group messages are ignored. The bot only responds to DMs. |
| Set with group IDs | Only listed groups are monitored (e.g.,groupId1,groupId2). |
| Set to* | The bot responds in any group it's a member of. |

`groupId1,groupId2`
`*`

## Features​

### Attachments​

The adapter supports sending and receiving media in both directions.

Incoming(user → agent):

- Images— PNG, JPEG, GIF, WebP (auto-detected via magic bytes)
- Audio— MP3, OGG, WAV, M4A (voice messages transcribed if Whisper is configured)
- Documents— PDF, ZIP, and other file types

Outgoing(agent → user):

The agent can send media files viaMEDIA:tags in responses. The following delivery methods are supported:

`MEDIA:`
- Images—send_multiple_imagesandsend_image_filesend PNG, JPEG, GIF, WebP as native Signal attachments
- Voice—send_voicesends audio files (OGG, MP3, WAV, M4A, AAC) as attachments
- Video—send_videosends MP4 video files
- Documents—send_documentsends any file type (PDF, ZIP, etc.)

`send_multiple_images`
`send_image_file`
`send_voice`
`send_video`
`send_document`

All outgoing media goes through Signal's standard attachment API. Unlike some platforms, Signal does not distinguish between voice messages and file attachments at the protocol level.

Attachment size limit:100 MB(both directions).

Signal servers will rate-limit attachment uploads, the adapter uses a scheduler for multiple image sending that batches images in groups of 32 and throttles uploads to match the Signal server policy.

### Native Formatting, Reply Quotes, and Reactions​

Signal messages render withnative formattinginstead of literal markdown characters. The adapter converts markdown (**bold**,*italic*,`code`,~~strike~~,||spoiler||, headings) into SignalbodyRangesso the text shows up with real styling on the recipient's client rather than as visible**/`characters.

`**bold**`
`*italic*`
``code``
`~~strike~~`
`||spoiler||`
`bodyRanges`
`**`
```

Reply quotes.When Hermes replies to a specific message, it now posts a native reply that quotes the original — same UI affordance Signal users see when they use "Reply" themselves. This is automatic for replies generated in response to an inbound message.

Reactions.The agent can react to messages via the standard reaction API; reactions surface in Signal as emoji reactions on the referenced message rather than as extra text.

None of this requires additional config — it ships on by default in recent signal-cli builds. If yoursignal-cliversion is too old, Hermes falls back to plaintext delivery and logs a one-time warning.

`signal-cli`

### Typing Indicators​

The bot sends typing indicators while processing messages, refreshing every 8 seconds.

### Tool Progress Display​

Signal does not support editing already-sent messages. Hermes therefore suppresses gateway tool-progress bubbles on Signal, even when/verboseis enabled and saves a non-offmode for the platform.

`/verbose`
`off`

You can still see tool activity in the CLI, and final Signal replies can include normal assistant output. If you need live per-tool progress in chat, use a messaging platform with message editing support.

### Phone Number Redaction​

All phone numbers are automatically redacted in logs:

- +15551234567→+155****4567
- This applies to both Hermes gateway logs and the global redaction system

`+15551234567`
`+155****4567`

### Note to Self (Single-Number Setup)​

If you run signal-cli as alinked secondary deviceon your own phone number (rather than a separate bot number), you can interact with Hermes through Signal's "Note to Self" feature.

Just send a message to yourself from your phone — signal-cli picks it up and Hermes responds in the same conversation.

How it works:

- "Note to Self" messages arrive assyncMessage.sentMessageenvelopes
- The adapter detects when these are addressed to the bot's own account and processes them as regular inbound messages
- Echo-back protection (sent-timestamp tracking) prevents infinite loops — the bot's own replies are filtered out automatically

`syncMessage.sentMessage`

No extra configuration needed.This works automatically as long asSIGNAL_ACCOUNTmatches your phone number.

`SIGNAL_ACCOUNT`

### Health Monitoring​

The adapter monitors the SSE connection and automatically reconnects if:

- The connection drops (with exponential backoff: 2s → 60s)
- No activity is detected for 120 seconds (pings signal-cli to verify)

## Troubleshooting​

| Problem | Solution |
| --- | --- |
| "Cannot reach signal-cli"during setup | Ensure signal-cli daemon is running:signal-cli --account +YOUR_NUMBER daemon --http 127.0.0.1:8080 |
| Messages not received | Check thatSIGNAL_ALLOWED_USERSincludes the sender's number in E.164 format (with+prefix) |
| "signal-cli not found on PATH" | Install signal-cli and ensure it's in your PATH, or use Docker |
| Connection keeps dropping | Check signal-cli logs for errors. Ensure Java 17+ is installed. |
| Group messages ignored | ConfigureSIGNAL_GROUP_ALLOWED_USERSwith specific group IDs, or*to allow all groups. |
| Bot responds to no one | ConfigureSIGNAL_ALLOWED_USERS, use DM pairing, or explicitly allow all users through gateway policy if you want broader access. |
| Duplicate messages | Ensure only one signal-cli instance is listening on your phone number |

`signal-cli --account +YOUR_NUMBER daemon --http 127.0.0.1:8080`
`SIGNAL_ALLOWED_USERS`
`+`
`SIGNAL_GROUP_ALLOWED_USERS`
`*`
`SIGNAL_ALLOWED_USERS`

## Security​

Always configure access controls.The bot has terminal access by default. WithoutSIGNAL_ALLOWED_USERSor DM pairing, the gateway denies all incoming messages as a safety measure.

`SIGNAL_ALLOWED_USERS`
- Phone numbers are redacted in all log output
- Use DM pairing or explicit allowlists for safe onboarding of new users
- Keep groups disabled unless you specifically need group support, or allowlist only the groups you trust
- Signal's end-to-end encryption protects message content in transit
- The signal-cli session data in~/.local/share/signal-cli/contains account credentials — protect it like a password

`~/.local/share/signal-cli/`

## Environment Variables Reference​

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| SIGNAL_HTTP_URL | Yes | — | signal-cli HTTP endpoint |
| SIGNAL_ACCOUNT | Yes | — | Bot phone number (E.164) |
| SIGNAL_ALLOWED_USERS | No | — | Comma-separated phone numbers/UUIDs |
| SIGNAL_GROUP_ALLOWED_USERS | No | — | Group IDs to monitor, or*for all (omit to disable groups) |
| SIGNAL_ALLOW_ALL_USERS | No | false | Allow any user to interact (skip allowlist) |
| SIGNAL_HOME_CHANNEL | No | — | Default delivery target for cron jobs |

`SIGNAL_HTTP_URL`
`SIGNAL_ACCOUNT`
`SIGNAL_ALLOWED_USERS`
`SIGNAL_GROUP_ALLOWED_USERS`
`*`
`SIGNAL_ALLOW_ALL_USERS`
`false`
`SIGNAL_HOME_CHANNEL`