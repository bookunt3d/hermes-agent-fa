- 
- Messaging Platforms
- Other
- SimpleX Chat

# SimpleX Chat

SimpleX Chatis a private, decentralised messaging platform where users own their contacts and groups. Unlike other platforms, SimpleX assigns no persistent user IDs — every contact is identified by an opaque internal ID generated at connection time, which makes it one of the most private messengers available.

> Runhermes gateway setupand pickSimpleXfor a guided walk-through.

Runhermes gateway setupand pickSimpleXfor a guided walk-through.

`hermes gateway setup`

## Prerequisites​

- Thesimplex-chatCLI installed and running as a daemon
- Python packagewebsockets(pip install websockets)

`pip install websockets`

## Install simplex-chat​

Download the latest release from thesimplex-chat GitHub releasespage:

```
# Linux / macOS binarycurl -L https://github.com/simplex-chat/simplex-chat/releases/latest/download/simplex-chat-ubuntu-22_04-x86_64 -o simplex-chatchmod +x simplex-chat
```

The SimpleX Chat project does not publish a prebuilt Docker image for the chat client; to run it under Docker, build from source from thesimplex-chat repository.

## Start the daemon​

```
simplex-chat -p 5225
```

The daemon listens on WebSocket atws://127.0.0.1:5225by default.

`ws://127.0.0.1:5225`

## Configure Hermes​

### Via setup wizard​

```
hermes gateway setup
```

SelectSimpleX Chatand follow the prompts.

### Via environment variables​

Add these to~/.hermes/.env:

`~/.hermes/.env`

```
SIMPLEX_WS_URL=ws://127.0.0.1:5225SIMPLEX_ALLOWED_USERS=<contact-id-1>,<contact-id-2>SIMPLEX_HOME_CHANNEL=<contact-id>
```

| Variable | Required | Description |
| --- | --- | --- |
| SIMPLEX_WS_URL | Yes | WebSocket URL of the simplex-chat daemon |
| SIMPLEX_ALLOWED_USERS | Recommended | Comma-separated allowlist. Each entry can be a numericcontactIdora display name — both forms work. |
| SIMPLEX_ALLOW_ALL_USERS | Optional | Settrueto allow every contact (use carefully) |
| SIMPLEX_AUTO_ACCEPT | Optional | Auto-accept incoming contact requests (default:true) |
| SIMPLEX_GROUP_ALLOWED | Optional | Comma-separated group IDs the bot participates in, or*for any group. Omit to ignore group messages entirely |
| SIMPLEX_HOME_CHANNEL | Optional | Default contact/group ID for cron job delivery |
| SIMPLEX_HOME_CHANNEL_NAME | Optional | Human label for the home channel |
| HERMES_SIMPLEX_TEXT_BATCH_DELAY | Optional | Quiet-period seconds (default:0.8) used to concatenate rapid-fire inbound text messages into one event |

`SIMPLEX_WS_URL`
`SIMPLEX_ALLOWED_USERS`
`contactId`
`SIMPLEX_ALLOW_ALL_USERS`
`true`
`SIMPLEX_AUTO_ACCEPT`
`true`
`SIMPLEX_GROUP_ALLOWED`
`*`
`SIMPLEX_HOME_CHANNEL`
`SIMPLEX_HOME_CHANNEL_NAME`
`HERMES_SIMPLEX_TEXT_BATCH_DELAY`
`0.8`

## Find your contact ID or display name​

After starting the daemon, open a conversation with your agent contact. The numericcontactIdappears in session logs. If you'd rather use the display name shown in the SimpleX UI, that works too —SIMPLEX_ALLOWED_USERSaccepts either form.

`contactId`
`SIMPLEX_ALLOWED_USERS`

## Authorization​

By defaultall contacts are denied. You must either:

1. SetSIMPLEX_ALLOWED_USERSto a comma-separated list ofcontactIds and/or display names (e.g.SIMPLEX_ALLOWED_USERS=4,alicematches either contactId 4 or the contact whose display name is "alice"), or
2. UseDM pairing— send any message to the bot and it will reply with a pairing code. Enter that code viahermes pairing approve simplex <CODE>.

`SIMPLEX_ALLOWED_USERS`
`contactId`
`SIMPLEX_ALLOWED_USERS=4,alice`
`hermes pairing approve simplex <CODE>`

## Group chats​

By default the adapter ignores group messages — a bot in a group otherwise
processes every member's traffic. Opt-in explicitly:

```
SIMPLEX_GROUP_ALLOWED=12,34          # specific group IDs# orSIMPLEX_GROUP_ALLOWED=*              # any group the bot is in
```

Address groups by prefixing the chat ID withgroup:, e.g.simplex:group:12as a crondeliver=target or in ahermes sendcall.

`group:`
`simplex:group:12`
`deliver=`
`hermes send`

## Attachments​

The adapter supports native SimpleX attachments in both directions:

- Inbound— incoming images, voice notes, and files are accepted via
the daemon's XFTP flow (rcvFileDescrReady→/freceive→ wait forrcvFileComplete) and surfaced asMessageEvent.media_urlswith the
appropriateMessageType(PHOTO,VOICE,TEXT+ document).
- Outbound—send_image_file,send_voice,send_document, andsend_videoall use the structured/_sendform withfilePath, so
the receiving SimpleX client renders images inline and plays voice
notes inline rather than offering them as downloads.

`rcvFileDescrReady`
`/freceive`
`rcvFileComplete`
`MessageEvent.media_urls`
`MessageType`
`PHOTO`
`VOICE`
`TEXT`
`send_image_file`
`send_voice`
`send_document`
`send_video`
`/_send`
`filePath`

Agent replies can also embedMEDIA:/path/to/filetags in plain text —
the adapter strips the tag from the body and sends the file as either a
voice note (audio extensions) or a document.

`MEDIA:/path/to/file`

## Using SimpleX with cron jobs​

```
cronjob(    action="create",    schedule="every 1h",    deliver="simplex",          # uses SIMPLEX_HOME_CHANNEL    prompt="Check for alerts and summarise.")
```

Or target a specific contact via the cron job'sdeliver:field, or from a shell script with thehermes sendCLI:

`deliver:`
`hermes send`

```
hermes send simplex:<contact-id> "Done!"
```

## Privacy notes​

- SimpleX never reveals phone numbers or email addresses — contacts use opaque IDs
- The connection between Hermes and the daemon is local WebSocket (ws://127.0.0.1:5225) — no data leaves your machine
- Messages are end-to-end encrypted by the SimpleX protocol before reaching the daemon

`ws://127.0.0.1:5225`

## Troubleshooting​

"Cannot reach daemon"— Ensuresimplex-chat -p 5225is running and the port matchesSIMPLEX_WS_URL.

`simplex-chat -p 5225`
`SIMPLEX_WS_URL`

"websockets not installed"— Runpip install websockets.

`pip install websockets`

Messages not received— Check that the contact's ID is inSIMPLEX_ALLOWED_USERSor approve them via DM pairing.

`SIMPLEX_ALLOWED_USERS`