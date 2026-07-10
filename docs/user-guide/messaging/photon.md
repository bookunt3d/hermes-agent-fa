---
layout: docs
title: "Messaging_Photon"
permalink: /docs/user-guide/messaging/photon/
---

- 
- Messaging Platforms
- Other
- Photon iMessage

# Photon iMessage

Connect Hermes toiMessagethroughPhoton, a managed
service that handles the Apple line allocation and abuse-prevention
layer so you don't have to run your own Mac relay.

The free tier uses Photon's shared iMessage line pool — different
recipients may see different sending numbers, but each conversation
stays stable. The paid Business tier gives every user the same
dedicated number; the plugin supports both, and the free tier is the
recommended starting point.

Photon's shared-line pool is free. No subscription is required to send
your first iMessage from Hermes — just a phone number we can bind to
your account.

## Architecture​

Photon is apersistent-connectionchannel, like Discord or Slack —no webhook, no public URL, no signing secret to manage.

Thespectrum-tsSDK holds a long-livedgRPC streamto Photon for
both directions. Because the SDK is TypeScript-only, Hermes runs it in a
small supervisedNode sidecarand talks to it over loopback:

`spectrum-ts`
- Inbound— the sidecar consumes the SDK'sapp.messagesgRPC
stream and forwards each message to the Python adapter over a loopbackGET /inbound(NDJSON). The adapter dedupes and dispatches it to the
agent, reconnecting automatically if the stream drops.
- Outbound— replies are loopback POSTs to the sidecar, which callsspace.send(...)on the SDK.

`app.messages`
`GET /inbound`
`space.send(...)`

The Python plugin starts, supervises, and shuts down the sidecar
automatically.

## Prerequisites​

- A Photon account — sign up atapp.photon.codes
- Node.js 18.17 or neweron PATH (node --version)
- A phone number that can receive iMessage (used to bind your account)

`node --version`

That's it — there is no public URL or tunnel to set up.

## First-time setup​

Either run the unified gateway wizard and pickPhoton iMessage:

```
hermes gateway setup
```

…or run the Photon setup directly (the wizard calls the same flow):

```
# Device-code login + project + user + sidecar deps, all in onehermes photon setup --phone +15551234567
```

The setup, in order:

1. Device login(client_id=photon-cli) — openshttps://app.photon.codes/for approval and stores the bearer token.
2. Finds or createstheHermes Agentproject on your account.
3. Enables Spectrum, reads the project's Spectrum id, and rotates
the project secret.
4. Registers your phone numberas a Spectrum user — skipped if a
user with that number already exists, so re-running is safe.
5. Prints your assigned iMessage line— the number you text to reach
your agent.
6. Runsnpm installinside the plugin's sidecar directory.

`client_id=photon-cli`
`https://app.photon.codes/`
`Hermes Agent`
`npm install`

Runtime credentials are written to~/.hermes/.env(PHOTON_PROJECT_ID= the Spectrum project id,PHOTON_PROJECT_SECRET),
the same place every other channel keeps its token. Management metadata
(device token, dashboard project id) lives in~/.hermes/auth.jsonundercredential_pool.photon/credential_pool.photon_project.

`~/.hermes/.env`
`PHOTON_PROJECT_ID`
`PHOTON_PROJECT_SECRET`
`~/.hermes/auth.json`
`credential_pool.photon`
`credential_pool.photon_project`

## Authorizing users​

Photon uses the same authorization model as every other Hermes
channel. Choose one approach:

DM pairing (default).When an unknown number messages your Photon
line, Hermes replies with a pairing code. Approve it with:

```
hermes pairing approve photon <CODE>
```

Usehermes pairing listto see pending codes and approved users.

`hermes pairing list`

Pre-authorize specific numbers(in~/.hermes/.env):

`~/.hermes/.env`

```
PHOTON_ALLOWED_USERS=+15551234567,+15559876543
```

Open access(dev only, in~/.hermes/.env):

`~/.hermes/.env`

```
PHOTON_ALLOW_ALL_USERS=true
```

WhenPHOTON_ALLOWED_USERSis set, unknown senders are silently
ignored rather than offered a pairing code (the allowlist signals you
deliberately restricted access).

`PHOTON_ALLOWED_USERS`

### Require mentions in group chats​

By default Hermes responds to every authorized DM and group message.
To make group chats opt-in, enable mention gating (DMs still always
work):

```
gateway:  platforms:    photon:      enabled: true      require_mention: true
```

Withrequire_mention: true, group-chat messages are ignored unless
they match a wake-word pattern. The defaults matchHermesand@Hermes agentvariants. For a custom agent name, set regex patterns:

`require_mention: true`
`Hermes`
`@Hermes agent`

```
gateway:  platforms:    photon:      require_mention: true      mention_patterns:        - '(?<![\w@])@?amos\b[,:\-]?'
```

Both keys also accept env vars (PHOTON_REQUIRE_MENTION,PHOTON_MENTION_PATTERNS). This is the same mention-gating model the
BlueBubbles iMessage channel uses.

`PHOTON_REQUIRE_MENTION`
`PHOTON_MENTION_PATTERNS`

## Start the gateway​

```
hermes gateway start
```

You'll see something like:

```
[photon] connected — sidecar on 127.0.0.1:8789, streaming inbound over gRPC
```

Send an iMessage to your assigned number and Hermes will reply.

## Status & troubleshooting​

```
hermes photon status
```

Prints saved credentials, sidecar health, your registered number, and the
assigned iMessage line Hermes uses. When a Photon token and dashboard project
are available,statusrefreshes missing number rows from the dashboard
without provisioning new lines.

`status`

```
Photon iMessage status──────────────────────  device token        : ✓ stored  dashboard project   : 3c90c3cc-0d44-4b50-...  spectrum project id : sp-...  project secret      : ✓ stored  my number           : +15551234567  assigned number     : +16282679185  node binary         : /usr/bin/node  sidecar deps        : ✓ installed
```

Common issues:

- sidecar deps : ✗ run hermes photon install-sidecar— Node is
installed butspectrum-tsisn't. Run the suggested command.
- device token : ✗ missing— runhermes photon setupto log in.
- No iMessage line assigned yet— Spectrum is enabled but no line
has been provisioned; re-runhermes photon setupor check thedashboard.
- Sidecar won't start— confirmnode --versionis 18.17+ and thathermes photon install-sidecarcompleted without errors.

`sidecar deps : ✗ run hermes photon install-sidecar`
`spectrum-ts`
`device token : ✗ missing`
`hermes photon setup`
`No iMessage line assigned yet`
`hermes photon setup`
`node --version`
`hermes photon install-sidecar`

## Limits today​

- Inbound attachments are metadata-only.Inbound events carry the
filename + MIME type; the agent sees a marker but can't yet read the
bytes. The SDK exposes attachment bytes viacontent.read(), so this
is a sidecar follow-up.
- Outbound attachments are supported.Hermes sends images, voice
notes, video, and documents through spectrum-ts'attachment()/voice()content builders via the sidecar's/send-attachmentendpoint. Captions arrive as a separate iMessage bubble after the
media.
- Photon's free quotas:5,000 messages per server per day,
50 new-conversation initiations per shared line per day. Increases
available — emailhelp@photon.codes.

`content.read()`
`attachment()`
`voice()`
`/send-attachment`
`help@photon.codes`

## Env vars​

| Variable | Default | Notes |
| --- | --- | --- |
| PHOTON_PROJECT_ID | from.env | Spectrum project id (the SDK'sprojectId); set by setup |
| PHOTON_PROJECT_SECRET | from.env | Project secret; set by setup |
| PHOTON_SIDECAR_PORT | 8789 | Loopback port for the sidecar control + inbound channel |
| PHOTON_SIDECAR_AUTOSTART | true | Whether the adapter spawns the sidecar |
| PHOTON_NODE_BIN | which node | Override the Node binary path |
| PHOTON_HOME_CHANNEL | (unset) | Default space id for cron / notifications |
| PHOTON_HOME_CHANNEL_NAME | (unset) | Human label for the home channel |
| PHOTON_ALLOWED_USERS | (unset) | Comma-separated E.164 allowlist |
| PHOTON_ALLOW_ALL_USERS | false | Dev only — accept any sender |
| PHOTON_REQUIRE_MENTION | false | Require a wake word before responding in groups |
| PHOTON_MENTION_PATTERNS | Hermes wake words | JSON list / comma / newline regex patterns for group mentions |
| PHOTON_DASHBOARD_HOST | app.photon.codes | Override the dashboard / device-login host |
| PHOTON_SPECTRUM_HOST | spectrum.photon.codes | Override the Spectrum API host |

`PHOTON_PROJECT_ID`
`.env`
`projectId`
`PHOTON_PROJECT_SECRET`
`.env`
`PHOTON_SIDECAR_PORT`
`8789`
`PHOTON_SIDECAR_AUTOSTART`
`true`
`PHOTON_NODE_BIN`
`which node`
`PHOTON_HOME_CHANNEL`
`PHOTON_HOME_CHANNEL_NAME`
`PHOTON_ALLOWED_USERS`
`PHOTON_ALLOW_ALL_USERS`
`false`
`PHOTON_REQUIRE_MENTION`
`false`
`PHOTON_MENTION_PATTERNS`
`PHOTON_DASHBOARD_HOST`
`app.photon.codes`
`PHOTON_SPECTRUM_HOST`
`spectrum.photon.codes`