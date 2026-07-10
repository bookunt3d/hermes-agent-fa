- 
- Messaging Platforms
- Other
- Matrix

# Matrix Setup

Hermes Agent integrates with Matrix, the open, federated messaging protocol. Matrix lets you run your own homeserver or use a public one like matrix.org — either way, you keep control of your communications. The bot connects via themautrixPython SDK, processes messages through the Hermes Agent pipeline (including tool use, memory, and reasoning), and responds in real time. It supports text, file attachments, images, audio, video, and optional end-to-end encryption (E2EE).

`mautrix`

Hermes works with any Matrix homeserver — Synapse, Conduit, Dendrite, or matrix.org.

Before setup, here's the part most people want to know: how Hermes behaves once it's connected.

## How Hermes Behaves​

| Context | Behavior |
| --- | --- |
| DMs | Hermes responds to every message. No@mentionneeded. Each DM has its own session. SetMATRIX_DM_MENTION_THREADS=trueto start a thread when the bot is@mentionedin a DM. |
| Rooms | By default, Hermes requires an@mentionto respond. SetMATRIX_REQUIRE_MENTION=falseor add room IDs toMATRIX_FREE_RESPONSE_ROOMSfor free-response rooms. Room invites are auto-accepted. |
| Threads | Hermes supports Matrix threads (MSC3440). If you reply in a thread, Hermes keeps the thread context isolated from the main room timeline. Threads where the bot has already participated do not require a mention. |
| Auto-threading | By default, Hermes auto-creates a thread for each message it responds to in a room. This keeps conversations isolated. SetMATRIX_AUTO_THREAD=falseto disable. SetMATRIX_DM_AUTO_THREAD=true(default false) to also auto-create threads for DM messages — this is distinct fromMATRIX_DM_MENTION_THREADS, which only starts a thread when the bot is@mentionedin a DM. |
| Commands | Hermes accepts normal/commandswhen your Matrix client sends them. If your client reserves/for local commands, use!commandsinstead; Hermes normalizes known!commandaliases to/command. |
| Interactive controls | Dangerous-command approval and/modelselection can use Matrix reactions. Approval reactions can be limited to the user who requested the action. |
| Thinking and tool activity | Matrix uses threaded, editable thinking/tool-activity panes when gateway progress is enabled, so updates do not flood the main room timeline. |
| Shared rooms with multiple users | By default, Hermes isolates session history per user inside the room. Two people talking in the same room do not share one transcript unless you explicitly disable that. |

`@mention`
`MATRIX_DM_MENTION_THREADS=true`
`@mentioned`
`@mention`
`MATRIX_REQUIRE_MENTION=false`
`MATRIX_FREE_RESPONSE_ROOMS`
`MATRIX_AUTO_THREAD=false`
`MATRIX_DM_AUTO_THREAD=true`
`MATRIX_DM_MENTION_THREADS`
`@mentioned`
`/commands`
`/`
`!commands`
`!command`
`/command`
`/model`

The bot automatically joins rooms when invited. Just invite the bot's Matrix user to any room and it will join and start responding.

## Capability Matrix​

This table is backed by the Matrix adapter capability declaration and Matrix test
coverage. E2EE is mode-based because deployments choose whether encrypted rooms
are disabled, opportunistic, or required.

| Capability | Matrix |
| --- | --- |
| text | yes |
| threads | yes |
| reactions | yes |
| approvals | yes |
| model picker | yes |
| thinking panes | yes |
| images | yes |
| multiple images | yes |
| files | yes |
| voice/audio | yes |
| video | yes |
| E2EE | off / optional / required |
| diagnostics | yes |

### Session Model in Matrix​

By default:

- each DM gets its own session
- each thread gets its own session namespace
- each user in a shared room gets their own session inside that room

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

### Mention and Threading Configuration​

You can configure mention and auto-threading behavior via environment variables orconfig.yaml:

`config.yaml`

```
matrix:  require_mention: true           # Require @mention in rooms (default: true)  allowed_users:                  # Matrix users allowed to trigger agent turns    - "@alice:matrix.org"  allowed_rooms:                  # Matrix rooms allowed to trigger agent turns    - "!abc123:matrix.org"  free_response_rooms:            # Rooms exempt from mention requirement    - "!abc123:matrix.org"  ignore_user_patterns:           # Bridge/appservice ghost users to ignore    - "^@telegram_"    - "^@whatsapp_"  process_notices: false          # Ignore m.notice by default  session_scope: room             # auto|room|thread; room is recommended for project rooms  auto_thread: true               # Auto-create threads for responses (default: true)  dm_mention_threads: false       # Create thread when @mentioned in DM (default: false)
```

Or via environment variables:

```
MATRIX_REQUIRE_MENTION=trueMATRIX_ALLOWED_USERS=@alice:matrix.orgMATRIX_ALLOWED_ROOMS=!abc123:matrix.orgMATRIX_FREE_RESPONSE_ROOMS=!abc123:matrix.org,!def456:matrix.orgMATRIX_IGNORE_USER_PATTERNS='^@telegram_,^@whatsapp_'MATRIX_PROCESS_NOTICES=falseMATRIX_SESSION_SCOPE=room       # recommended for stable project-room contextMATRIX_AUTO_THREAD=trueMATRIX_DM_MENTION_THREADS=falseMATRIX_REACTIONS=true          # default: true — emoji reactions during processingMATRIX_ALLOW_ROOM_MENTIONS=false
```

MATRIX_REACTIONS=falseturns off the processing-lifecycle emoji reactions (👀/✅/❌) the bot posts on inbound messages. Useful for rooms where reaction events are noisy or aren't supported by all participating clients.

`MATRIX_REACTIONS=false`

Hermes sends structured Matrix user mentions for explicit Matrix IDs such as@alice:example.org. Room-wide@roomnotifications are disabled by default; setMATRIX_ALLOW_ROOM_MENTIONS=trueonly in rooms where the bot is allowed to notify everyone.

`@alice:example.org`
`@room`
`MATRIX_ALLOW_ROOM_MENTIONS=true`

If you are upgrading from a version that did not haveMATRIX_REQUIRE_MENTION, the bot previously responded to all messages in rooms. To preserve that behavior, setMATRIX_REQUIRE_MENTION=false.

`MATRIX_REQUIRE_MENTION`
`MATRIX_REQUIRE_MENTION=false`

### Project Room Isolation​

If you use the same Matrix bot in multiple project rooms, configure stable
room-scoped sessions:

```
MATRIX_SESSION_SCOPE=roomMATRIX_AUTO_THREAD=false
```

MATRIX_SESSION_SCOPEaccepts:

`MATRIX_SESSION_SCOPE`
| Scope | Behavior |
| --- | --- |
| auto | Backward-compatible default. ExistingMATRIX_AUTO_THREADbehavior controls synthetic threads. |
| room | Unthreaded room messages stay in one stable room session. Real Matrix threads still use their thread root. |
| thread | Unthreaded room messages synthesize a thread/session from the triggering event ID. |

`auto`
`MATRIX_AUTO_THREAD`
`room`
`thread`

Hermes now includes the current Matrix room name, room ID, topic, message ID,
and a Matrix room-boundary note in the agent prompt./statusalso shows the
current Matrix room/session scope, and/resumewill not silently resume a
named session from another Matrix room unless you explicitly use/resume --cross-room <session name>.

`/status`
`/resume`
`/resume --cross-room <session name>`

MATRIX_SESSION_SCOPE=roomcontrols the room/thread lane. The existinggroup_sessions_per_usersetting still controls whether users inside that room
share the lane. Withgroup_sessions_per_user: true(default), Alice and Bob get
separate Project B sessions. Withgroup_sessions_per_user: false, the room has
one shared Project B transcript.

`MATRIX_SESSION_SCOPE=room`
`group_sessions_per_user`
`group_sessions_per_user: true`
`group_sessions_per_user: false`

This guide walks you through the full setup process — from creating your bot account to sending your first message.

## Step 1: Create a Bot Account​

You need a Matrix user account for the bot. There are several ways to do this:

### Option A: Register on Your Homeserver (Recommended)​

If you run your own homeserver (Synapse, Conduit, Dendrite):

1. Use the admin API or registration tool to create a new user:

```
# Synapse exampleregister_new_matrix_user -c /etc/synapse/homeserver.yaml http://localhost:8008
```

1. Choose a username likehermes— the full user ID will be@hermes:your-server.org.

`hermes`
`@hermes:your-server.org`

### Option B: Use matrix.org or Another Public Homeserver​

1. Go toElement Weband create a new account.
2. Pick a username for your bot (e.g.,hermes-bot).

`hermes-bot`

### Option C: Use Your Own Account​

You can also run Hermes as your own user. This means the bot posts as you — useful for personal assistants.

## Step 2: Get an Access Token​

Hermes needs an access token to authenticate with the homeserver. You have two options:

### Option A: Access Token (Recommended)​

The most reliable way to get a token:

Via Element:

1. Log in toElementwith the bot account.
2. Go toSettings→Help & About.
3. Scroll down and expandAdvanced— the access token is displayed there.
4. Copy it immediately.

Via the API:

```
curl -X POST https://your-server/_matrix/client/v3/login \  -H "Content-Type: application/json" \  -d '{    "type": "m.login.password",    "user": "@hermes:your-server.org",    "password": "your-password"  }'
```

The response includes anaccess_tokenfield — copy it.

`access_token`

The access token gives full access to the bot's Matrix account. Never share it publicly or commit it to Git. If compromised, revoke it by logging out all sessions for that user.

### Option B: Password Login​

Instead of providing an access token, you can give Hermes the bot's user ID and password. Hermes will log in automatically on startup. This is simpler but means the password is stored in your.envfile.

`.env`

```
MATRIX_USER_ID=@hermes:your-server.orgMATRIX_PASSWORD=your-password
```

## Step 3: Find Your Matrix User ID​

Hermes Agent uses your Matrix User ID to control who can interact with the bot. Matrix User IDs follow the format@username:server.

`@username:server`

To find yours:

1. OpenElement(or your preferred Matrix client).
2. Click your avatar →Settings.
3. Your User ID is displayed at the top of the profile (e.g.,@alice:matrix.org).

`@alice:matrix.org`

Matrix User IDs always start with@and contain a:followed by the server name. For example:@alice:matrix.org,@bob:your-server.com.

`@`
`:`
`@alice:matrix.org`
`@bob:your-server.com`

## Step 4: Configure Hermes Agent​

### Option A: Interactive Setup (Recommended)​

Run the guided setup command:

```
hermes gateway setup
```

SelectMatrixwhen prompted, then provide your homeserver URL, access token (or user ID + password), and allowed user IDs when asked.

### Option B: Manual Configuration​

Add the following to your~/.hermes/.envfile:

`~/.hermes/.env`

Using an access token:

```
# RequiredMATRIX_HOMESERVER=https://matrix.example.orgMATRIX_ACCESS_TOKEN=***# Optional: user ID (auto-detected from token if omitted)# MATRIX_USER_ID=@hermes:matrix.example.org# Security: restrict who can interact with the botMATRIX_ALLOWED_USERS=@alice:matrix.example.org# Optional: restrict which rooms can trigger the botMATRIX_ALLOWED_ROOMS=!abc123:matrix.example.org# Multiple allowed users (comma-separated)# MATRIX_ALLOWED_USERS=@alice:matrix.example.org,@bob:matrix.example.org
```

Using password login:

```
# RequiredMATRIX_HOMESERVER=https://matrix.example.orgMATRIX_USER_ID=@hermes:matrix.example.orgMATRIX_PASSWORD=***# SecurityMATRIX_ALLOWED_USERS=@alice:matrix.example.org
```

## Private Deployment Hardening​

For private Matrix deployments, set both user and room allowlists. IfMATRIX_ALLOWED_USERSis unset, any sender who can reach the bot in a joined
room can trigger an agent turn. IfMATRIX_ALLOWED_ROOMSis unset, any room the
bot joins can trigger an agent turn. A locked-down deployment should set both:

`MATRIX_ALLOWED_USERS`
`MATRIX_ALLOWED_ROOMS`

```
MATRIX_ALLOWED_USERS=@alice:matrix.example.org,@bob:matrix.example.orgMATRIX_ALLOWED_ROOMS=!ops:matrix.example.org,!dmroom:matrix.example.org
```

Bridge and appservice deployments need extra loop protection. Hermes always
ignores its own events, Matrix appservice-style users whose localpart starts
with_, duplicate event IDs, old startup events, edit replacement events, andm.noticeevents by default. Add deployment-specific bridge ghost patterns when
your bridge uses a different naming convention:

`_`
`m.notice`

```
MATRIX_IGNORE_USER_PATTERNS='^@telegram_,^@slack_,^@whatsapp_'
```

Only enable notices when a trusted human workflow really sendsm.notice:

`m.notice`

```
MATRIX_PROCESS_NOTICES=true
```

Outbound whole-room notifications are disabled by default. KeepMATRIX_ALLOW_ROOM_MENTIONS=falseunless the bot is explicitly allowed to wake
the whole room with@room.

`MATRIX_ALLOW_ROOM_MENTIONS=false`
`@room`

Diagnostics and debug payloads redact Matrix access tokens, recovery keys,
device identifiers, and message bodies. Media downloads are limited to Matrixmxc://content URIs and rejected when they exceedMATRIX_MAX_MEDIA_BYTES.
Treat federated rooms and untrusted homeservers as untrusted input: keep room
allowlists tight, prefer DMs or private rooms for tool-heavy work, and avoid
authorizing bridge ghosts or appservice puppets as allowed users.

`mxc://`
`MATRIX_MAX_MEDIA_BYTES`

Optional behavior settings in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
group_sessions_per_user: true
```

- group_sessions_per_user: truekeeps each participant's context isolated inside shared rooms

`group_sessions_per_user: true`

### Start the Gateway​

Once configured, start the Matrix gateway:

```
hermes gateway
```

The bot should connect to your homeserver and start syncing within a few seconds. Send it a message — either a DM or in a room it has joined — to test.

You can runhermes gatewayin the background or as a systemd service for persistent operation. See the deployment docs for details.

`hermes gateway`

## End-to-End Encryption (E2EE)​

Hermes supports Matrix end-to-end encryption, so you can chat with your bot in encrypted rooms.

### Requirements​

E2EE requires themautrixlibrary with encryption extras and thelibolmC library:

`mautrix`
`libolm`

```
# Install mautrix with E2EE supportpip install 'mautrix[encryption]'# Or install with hermes extrascd ~/.hermes/hermes-agent && uv pip install -e ".[matrix]"
```

You also needlibolminstalled on your system:

`libolm`

```
# Debian/Ubuntusudo apt install libolm-dev# macOSbrew install libolm# Fedorasudo dnf install libolm-devel
```

### Enable E2EE​

Add to your~/.hermes/.env:

`~/.hermes/.env`

```
MATRIX_E2EE_MODE=required
```

MATRIX_E2EE_MODEaccepts:

`MATRIX_E2EE_MODE`
| Mode | Behavior |
| --- | --- |
| off | Do not initialize Matrix E2EE. |
| optional | Try E2EE when dependencies are available, but keep unencrypted rooms working if crypto cannot initialize. |
| required | Fail closed if E2EE dependencies or crypto setup are not available. |

`off`
`optional`
`required`

Optional mode may fall back to non-E2EE operation when crypto setup is unavailable. Required mode fails closed instead of silently downgrading.

For backwards compatibility,MATRIX_ENCRYPTION=truestill enables required E2EE behavior.

`MATRIX_ENCRYPTION=true`

When E2EE is enabled, Hermes:

- Stores encryption keys in~/.hermes/platforms/matrix/store/(legacy installs:~/.hermes/matrix/store/)
- Uploads device keys on first connection
- Decrypts incoming messages and encrypts outgoing messages automatically
- Auto-joins encrypted rooms when invited

`~/.hermes/platforms/matrix/store/`
`~/.hermes/matrix/store/`

### Matrix Tools and Controls​

In Matrix conversations, Hermes exposes Matrix-specific tools to the agent:

- matrix_send_reaction
- matrix_redact_message
- matrix_create_room
- matrix_invite_user
- matrix_fetch_history
- matrix_set_presence

`matrix_send_reaction`
`matrix_redact_message`
`matrix_create_room`
`matrix_invite_user`
`matrix_fetch_history`
`matrix_set_presence`

These tools are scoped to Matrix contexts and are not available in non-Matrix toolsets. Admin-style tools are disabled by default: redaction requiresMATRIX_TOOLS_ALLOW_REDACTION=true, invites requireMATRIX_TOOLS_ALLOW_INVITES=true, and room creation requiresMATRIX_TOOLS_ALLOW_ROOM_CREATE=true. Public room creation also requiresMATRIX_ALLOW_PUBLIC_ROOMS=true.
Matrix tools are limited to the current Matrix room by default. Explicit
cross-room targets requireMATRIX_TOOLS_ALLOW_CROSS_ROOM=true; redaction and
invite-like cross-room actions additionally requireMATRIX_TOOLS_ALLOW_CROSS_ROOM_DESTRUCTIVE=true. IfMATRIX_ALLOWED_ROOMSis
set, Matrix tools may only target those rooms.

`MATRIX_TOOLS_ALLOW_REDACTION=true`
`MATRIX_TOOLS_ALLOW_INVITES=true`
`MATRIX_TOOLS_ALLOW_ROOM_CREATE=true`
`MATRIX_ALLOW_PUBLIC_ROOMS=true`
`MATRIX_TOOLS_ALLOW_CROSS_ROOM=true`
`MATRIX_TOOLS_ALLOW_CROSS_ROOM_DESTRUCTIVE=true`
`MATRIX_ALLOWED_ROOMS`

Reaction controls use:

- ✅ approve once
- ♾️ approve always
- ❌ deny
- number reactions for/modelchoices

`/model`

SetMATRIX_APPROVAL_REQUIRE_SENDER=falseif you intentionally want any authorized Matrix user in the room to operate an approval/model picker prompt. The default is requester-bound when Hermes knows who requested the action.

`MATRIX_APPROVAL_REQUIRE_SENDER=false`

### Media Limits​

Hermes uploads and downloads Matrix images, files, audio, and video through Matrix media APIs. Multiple generated images are sent as one ordered logical batch, preserving captions and thread context across the batch.

By default, Matrix media over 100 MB is rejected before upload/download. Override with:

```
MATRIX_MAX_MEDIA_BYTES=104857600
```

Inbound media must use Matrixmxc://content URIs. Hermes rejects arbitrary
HTTP(S) media URLs in Matrix events to avoid turning a federated room into an
unrestricted downloader.

`mxc://`

## Synapse Integration Tests​

Hermes includes an opt-in Synapse harness for local validation:

```
docker compose -f tests/e2e/matrix_synapse_gateway/docker-compose.yml up -dHERMES_MATRIX_SYNAPSE_INTEGRATION=1 \  scripts/run_tests.sh -m "integration and matrix_synapse" \  tests/e2e/matrix_synapse_gateway/test_gateway.pydocker compose -f tests/e2e/matrix_synapse_gateway/docker-compose.yml down -v
```

The harness creates temporary users through Synapse shared-secret registration
and covers private-room send/receive, named-room invite/join, media
upload/download, bot response delivery, and startup old-event filtering. E2EE
smoke coverage is separately marked withmatrix_e2eeso it can stay opt-in on
developer machines.

`matrix_e2ee`

### Cross-Signing Verification (Recommended)​

If your Matrix account has cross-signing enabled (the default in Element), set the recovery key so the bot can self-sign its device on startup. Without this, other Matrix clients may refuse to share encryption sessions with the bot after a device key rotation.

```
MATRIX_RECOVERY_KEY=EsT... your recovery key here
```

Where to find it:In Element, go toSettings→Security & Privacy→Encryption→ your recovery key (also called the "Security Key"). This is the key you were asked to save when you first set up cross-signing.

On each startup, ifMATRIX_RECOVERY_KEYis set, Hermes imports cross-signing keys from the homeserver's secure secret storage and signs the current device. This is idempotent and safe to leave enabled permanently.

`MATRIX_RECOVERY_KEY`

If Hermes bootstraps a new Matrix recovery key, it never logs the raw key. SetMATRIX_RECOVERY_KEY_OUTPUT_FILE=/secure/path/matrix-recovery-key.txtbefore
startup to write a generated key once with file mode0600; the file is not
overwritten if it already exists.

`MATRIX_RECOVERY_KEY_OUTPUT_FILE=/secure/path/matrix-recovery-key.txt`
`0600`

If you delete~/.hermes/platforms/matrix/store/crypto.db, the bot loses its encryption identity. Simply restarting with the same device ID willnotfully recover — the homeserver still holds one-time keys signed with the old identity key, and peers cannot establish new Olm sessions.

`~/.hermes/platforms/matrix/store/crypto.db`

Hermes detects this condition on startup and refuses to enable E2EE, logging:device XXXX has stale one-time keys on the server signed with a previous identity key.

`device XXXX has stale one-time keys on the server signed with a previous identity key`

Easiest recovery: generate a new access token(which gets a fresh device ID with no stale key history). See the "Upgrading from a previous version with E2EE" section below. This is the most reliable path and avoids touching the homeserver database.

Manual recovery(advanced — keeps the same device ID):

1. Stop Synapse and delete the old device from its database:sudosystemctl stop matrix-synapsesudosqlite3 /var/lib/matrix-synapse/homeserver.db"DELETE FROM e2e_device_keys_json WHERE device_id = 'DEVICE_ID' AND user_id = '@hermes:your-server';DELETE FROM e2e_one_time_keys_json WHERE device_id = 'DEVICE_ID' AND user_id = '@hermes:your-server';DELETE FROM e2e_fallback_keys_json WHERE device_id = 'DEVICE_ID' AND user_id = '@hermes:your-server';DELETE FROM devices WHERE device_id = 'DEVICE_ID' AND user_id = '@hermes:your-server';"sudosystemctl start matrix-synapseOr via the Synapse admin API (note the URL-encoded user ID):curl-XDELETE-H"Authorization: Bearer ADMIN_TOKEN"\'https://your-server/_synapse/admin/v2/users/%40hermes%3Ayour-server/devices/DEVICE_ID'Note: deleting a device via the admin API may also invalidate the associated access token. You may need to generate a new token afterward.
2. Delete the local crypto store and restart Hermes:rm-f~/.hermes/platforms/matrix/store/crypto.db*# restart hermes

Stop Synapse and delete the old device from its database:

```
sudo systemctl stop matrix-synapsesudo sqlite3 /var/lib/matrix-synapse/homeserver.db "  DELETE FROM e2e_device_keys_json WHERE device_id = 'DEVICE_ID' AND user_id = '@hermes:your-server';  DELETE FROM e2e_one_time_keys_json WHERE device_id = 'DEVICE_ID' AND user_id = '@hermes:your-server';  DELETE FROM e2e_fallback_keys_json WHERE device_id = 'DEVICE_ID' AND user_id = '@hermes:your-server';  DELETE FROM devices WHERE device_id = 'DEVICE_ID' AND user_id = '@hermes:your-server';"sudo systemctl start matrix-synapse
```

Or via the Synapse admin API (note the URL-encoded user ID):

```
curl -X DELETE -H "Authorization: Bearer ADMIN_TOKEN" \  'https://your-server/_synapse/admin/v2/users/%40hermes%3Ayour-server/devices/DEVICE_ID'
```

Note: deleting a device via the admin API may also invalidate the associated access token. You may need to generate a new token afterward.

Delete the local crypto store and restart Hermes:

```
rm -f ~/.hermes/platforms/matrix/store/crypto.db*# restart hermes
```

Other Matrix clients (Element, matrix-commander) may cache the old device keys. After recovery, type/discardsessionin Element to force a new encryption session with the bot.

`/discardsession`

Ifmautrix[encryption]is not installed orlibolmis missing, the bot falls back to a plain (unencrypted) client automatically. You'll see a warning in the logs.

`mautrix[encryption]`
`libolm`

## Home Room​

You can designate a "home room" where the bot sends proactive messages (such as cron job output, reminders, and notifications). There are two ways to set it:

### Using the Slash Command​

Type/sethomein any Matrix room where the bot is present. That room becomes the home room.
If your Matrix client intercepts slash commands, type!sethomeinstead.

`/sethome`
`!sethome`

### Manual Configuration​

Add this to your~/.hermes/.env:

`~/.hermes/.env`

```
MATRIX_HOME_ROOM=!abc123def456:matrix.example.org
```

## Room allowlist (allowed_rooms)​

`allowed_rooms`

Restrict the bot to a fixed set of Matrix rooms. When set, the botonlyresponds in rooms whose ID appears in the list — messages from any other room are silently ignored, even if the bot is mentioned.

DMs (direct chat rooms) are exemptfrom this filter, so authorized users can always reach the bot one-on-one.

```
matrix:  allowed_rooms:    - "!abc123def456:matrix.example.org"    - "!opsroom789:matrix.example.org"
```

Or via env var (comma-separated):

```
MATRIX_ALLOWED_ROOMS="!abc123def456:matrix.example.org,!opsroom789:matrix.example.org"
```

Behavior:

- Empty / unset → no restriction (default).
- Non-empty → room ID must be on the list. The check runsbeforeany other gating (mention requirement, sender allowlist, etc.).
- Use the room'sinternal ID(!abc...:server), not its alias (#room:server). You can find a room's internal ID in Element via Room → Settings → Advanced.

`!abc...:server`
`#room:server`

See also:admin/user slash command split.

To find a Room ID: in Element, go to the room →Settings→Advanced→ theInternal room IDis shown there (starts with!).

`!`

## Commands in Matrix​

Hermes supports the same gateway commands in Matrix that it supports on other
messaging platforms, including/commands,/model,/stop,/queue,/steer,/goal,/subgoal,/background,/bg,/btw,/tasks, and/yolo.

`/commands`
`/model`
`/stop`
`/queue`
`/steer`
`/goal`
`/subgoal`
`/background`
`/bg`
`/btw`
`/tasks`
`/yolo`

Some Matrix clients reserve leading/for local client commands and may not
send unknown slash commands to the room. In that case, use!as a Matrix-safe
alias:

`/`
`!`

```
!commands!model!model gpt-5.5 --provider openrouter!queue continue with the next task!stop
```

Hermes only normalizes!commandwhen the command is known to the gateway, a
registered plugin command, or an installed skill command. Ordinary exclamations
such as!importantremain normal chat messages.

`!command`
`!important`

## Troubleshooting​

### Bot is not responding to messages​

Cause: The bot hasn't joined the room,MATRIX_ALLOWED_USERSdoesn't include your User ID,MATRIX_ALLOWED_ROOMSdoesn't include the room, or a room message did not mention the bot.

`MATRIX_ALLOWED_USERS`
`MATRIX_ALLOWED_ROOMS`

Fix: Invite the bot to the room — it auto-joins on invite. Verify your User ID is inMATRIX_ALLOWED_USERS(use the full@user:serverformat) and the room ID is inMATRIX_ALLOWED_ROOMSif that allowlist is configured. In rooms, mention the bot or add the room toMATRIX_FREE_RESPONSE_ROOMS. Restart the gateway.

`MATRIX_ALLOWED_USERS`
`@user:server`
`MATRIX_ALLOWED_ROOMS`
`MATRIX_FREE_RESPONSE_ROOMS`

### Bot joins rooms but silently drops every message (clock skew)​

Cause: The host's system clock is set ahead of real time. The Matrix adapter applies a 5-second startup-grace filter (event_ts < startup_ts - 5) to ignore events replayed from initial sync. When the wall clock is ahead, every incoming event looks "older than startup" and is dropped before reaching the message handler — the bot appears connected but never replies. See#12614.

`event_ts < startup_ts - 5`

Symptom: Gateway log showsMatrix: dropped N live events as 'too old' more than 30s after startup.

`Matrix: dropped N live events as 'too old' more than 30s after startup`

Fix: Sync the host clock with NTP and restart the bot:

```
# Debian/Ubuntusudo timedatectl set-ntp truetimedatectl status   # confirm "System clock synchronized: yes"# macOSsudo sntp -sS time.apple.com
```

### "Failed to authenticate" / "whoami failed" on startup​

Cause: The access token or homeserver URL is incorrect.

Fix: VerifyMATRIX_HOMESERVERpoints to your homeserver (includehttps://, no trailing slash). Check thatMATRIX_ACCESS_TOKENis valid — try it with curl:

`MATRIX_HOMESERVER`
`https://`
`MATRIX_ACCESS_TOKEN`

```
curl -H "Authorization: Bearer YOUR_TOKEN" \  https://your-server/_matrix/client/v3/account/whoami
```

If this returns your user info, the token is valid. If it returns an error, generate a new token.

### "mautrix not installed" error​

Cause: ThemautrixPython package is not installed.

`mautrix`

Fix: Install it:

```
pip install 'mautrix[encryption]'
```

Or with Hermes extras:

```
cd ~/.hermes/hermes-agent && uv pip install -e ".[matrix]"
```

### Encryption errors / "could not decrypt event"​

Cause: Missing encryption keys,libolmnot installed, or the bot's device isn't trusted.

`libolm`

Fix:

1. Verifylibolmis installed on your system (see the E2EE section above).
2. Make sureMATRIX_ENCRYPTION=trueis set in your.env.
3. In your Matrix client (Element), go to the bot's profile -> Sessions -> verify/trust the bot's device.
4. If the bot just joined an encrypted room, it can only decrypt messages sentafterit joined. Older messages are inaccessible.

`libolm`
`MATRIX_ENCRYPTION=true`
`.env`

### Upgrading from a previous version with E2EE​

If you also manually deletedcrypto.db, see the "Deleting the crypto store" warning in the E2EE section above — there are additional steps to clear stale one-time keys from the homeserver.

`crypto.db`

If you previously used Hermes withMATRIX_ENCRYPTION=trueand are upgrading to
a version that uses the new SQLite-based crypto store, the bot's encryption
identity has changed. Your Matrix client (Element) may cache the old device keys
and refuse to share encryption sessions with the bot.

`MATRIX_ENCRYPTION=true`

Symptoms: The bot connects and shows "E2EE enabled" in the logs, but all
messages show "could not decrypt event" and the bot never responds.

What's happening: The old encryption state (from the previousmatrix-nioor
serialization-basedmautrixbackend) is incompatible with the new SQLite crypto
store. The bot creates a fresh encryption identity, but your Matrix client still
has the old keys cached and won't share the room's encryption session with a
device whose keys changed. This is a Matrix security feature -- clients treat
changed identity keys for the same device as suspicious.

`matrix-nio`
`mautrix`

Fix(one-time migration):

1. Generate a new access tokento get a fresh device ID. The simplest way:curl-XPOST https://your-server/_matrix/client/v3/login\-H"Content-Type: application/json"\-d'{"type": "m.login.password","identifier": {"type": "m.id.user", "user": "@hermes:your-server.org"},"password": "***","initial_device_display_name": "Hermes Agent"}'Copy the newaccess_tokenand updateMATRIX_ACCESS_TOKENin~/.hermes/.env.
2. Delete old encryption state:rm-f~/.hermes/platforms/matrix/store/crypto.dbrm-f~/.hermes/platforms/matrix/store/crypto_store.*
3. Set your recovery key(if you use cross-signing — most Element users do). Add to~/.hermes/.env:MATRIX_RECOVERY_KEY=EsT... your recovery key hereThis lets the bot self-sign with cross-signing keys on startup, so Element trusts the new device immediately. Without this, Element may see the new device as unverified and refuse to share encryption sessions. Find your recovery key in Element underSettings→Security & Privacy→Encryption.
4. Force your Matrix client to rotate the encryption session. In Element,
open the DM room with the bot and type/discardsession. This forces Element
to create a new encryption session and share it with the bot's new device.
5. Restart the gateway:hermes gateway runIfMATRIX_RECOVERY_KEYis set, you should seeMatrix: cross-signing verified via recovery keyin the logs.
6. Send a new message. The bot should decrypt and respond normally.

Generate a new access tokento get a fresh device ID. The simplest way:

```
curl -X POST https://your-server/_matrix/client/v3/login \  -H "Content-Type: application/json" \  -d '{    "type": "m.login.password",    "identifier": {"type": "m.id.user", "user": "@hermes:your-server.org"},    "password": "***",    "initial_device_display_name": "Hermes Agent"  }'
```

Copy the newaccess_tokenand updateMATRIX_ACCESS_TOKENin~/.hermes/.env.

`access_token`
`MATRIX_ACCESS_TOKEN`
`~/.hermes/.env`

Delete old encryption state:

```
rm -f ~/.hermes/platforms/matrix/store/crypto.dbrm -f ~/.hermes/platforms/matrix/store/crypto_store.*
```

Set your recovery key(if you use cross-signing — most Element users do). Add to~/.hermes/.env:

`~/.hermes/.env`

```
MATRIX_RECOVERY_KEY=EsT... your recovery key here
```

This lets the bot self-sign with cross-signing keys on startup, so Element trusts the new device immediately. Without this, Element may see the new device as unverified and refuse to share encryption sessions. Find your recovery key in Element underSettings→Security & Privacy→Encryption.

Force your Matrix client to rotate the encryption session. In Element,
open the DM room with the bot and type/discardsession. This forces Element
to create a new encryption session and share it with the bot's new device.

`/discardsession`

Restart the gateway:

```
hermes gateway run
```

IfMATRIX_RECOVERY_KEYis set, you should seeMatrix: cross-signing verified via recovery keyin the logs.

`MATRIX_RECOVERY_KEY`
`Matrix: cross-signing verified via recovery key`

Send a new message. The bot should decrypt and respond normally.

After migration, messages sentbeforethe upgrade cannot be decrypted -- the old
encryption keys are gone. This only affects the transition; new messages work
normally.

New installations are not affected.This migration is only needed if you had
a working E2EE setup with a previous version of Hermes and are upgrading.

Why a new access token?Each Matrix access token is bound to a specific device
ID. Reusing the same device ID with new encryption keys causes other Matrix
clients to distrust the device (they see changed identity keys as a potential
security breach). A new access token gets a new device ID with no stale key
history, so other clients trust it immediately.

## Proxy Mode (E2EE on macOS)​

Matrix E2EE requireslibolm, which doesn't compile on macOS ARM64 (Apple Silicon). Thehermes-agent[matrix]extra is gated to Linux only. If you're on macOS, proxy mode lets you run E2EE in a Docker container on a Linux VM while the actual agent runs natively on macOS with full access to your local files, memory, and skills.

`libolm`
`hermes-agent[matrix]`

### How It Works​

```
macOS (Host):  └─ hermes gateway       ├─ api_server adapter ← listens on 0.0.0.0:8642       ├─ AIAgent ← single source of truth       ├─ Sessions, memory, skills       └─ Local file access (Obsidian, projects, etc.)Linux VM (Docker):  └─ hermes gateway (proxy mode)       ├─ Matrix adapter ← E2EE decryption/encryption       └─ HTTP forward → macOS:8642/v1/chat/completions           (no LLM API keys, no agent, no inference)
```

The Docker container only handles Matrix protocol + E2EE. When a message arrives, it decrypts it and forwards the text to the host via a standard HTTP request. The host runs the agent, calls tools, generates a response, and streams it back. The container encrypts and sends the response to Matrix. All sessions are unified — CLI, Matrix, Telegram, and any other platform share the same memory and conversation history.

### Step 1: Configure the Host (macOS)​

Enable the API server so the host accepts incoming requests from the Docker container.

Add to~/.hermes/.env:

`~/.hermes/.env`

```
API_SERVER_ENABLED=trueAPI_SERVER_KEY=your-secret-key-hereAPI_SERVER_HOST=0.0.0.0
```

- API_SERVER_HOST=0.0.0.0binds to all interfaces so the Docker container can reach it.
- API_SERVER_KEYis required for non-loopback binding. Pick a strong random string.
- The API server runs on port 8642 by default (change withAPI_SERVER_PORTif needed).

`API_SERVER_HOST=0.0.0.0`
`API_SERVER_KEY`
`API_SERVER_PORT`

Start the gateway:

```
hermes gateway
```

You should see the API server start alongside any other platforms you have configured. Verify it's reachable from the VM:

```
# From the Linux VMcurl http://<mac-ip>:8642/health
```

### Step 2: Configure the Docker Container (Linux VM)​

The container needs Matrix credentials and the proxy URL. It does NOT need LLM API keys.

docker-compose.yml:

`docker-compose.yml`

```
services:  hermes-matrix:    build: .    environment:      # Matrix credentials      MATRIX_HOMESERVER: "https://matrix.example.org"      MATRIX_ACCESS_TOKEN: "syt_..."      MATRIX_ALLOWED_USERS: "@you:matrix.example.org"      MATRIX_ENCRYPTION: "true"      MATRIX_DEVICE_ID: "HERMES_BOT"      # Proxy mode — forward to host agent      GATEWAY_PROXY_URL: "http://192.168.1.100:8642"      GATEWAY_PROXY_KEY: "your-secret-key-here"    volumes:      - ./matrix-store:/root/.hermes/platforms/matrix/store
```

Dockerfile:

`Dockerfile`

```
FROM python:3.11-slimRUN apt-get update && apt-get install -y libolm-dev && rm -rf /var/lib/apt/lists/*RUN cd ~/.hermes/hermes-agent && uv pip install -e ".[matrix]"CMD ["hermes", "gateway"]
```

That's the entire container. No API keys for OpenRouter, Anthropic, or any inference provider.

### Step 3: Start Both​

1. Start the host gateway first:hermes gateway
2. Start the Docker container:dockercompose up-d
3. Send a message in an encrypted Matrix room. The container decrypts it, forwards it to the host, and streams the response back.

Start the host gateway first:

```
hermes gateway
```

Start the Docker container:

```
docker compose up -d
```

Send a message in an encrypted Matrix room. The container decrypts it, forwards it to the host, and streams the response back.

### Configuration Reference​

Proxy mode is configured on thecontainer side(the thin gateway):

| Setting | Description |
| --- | --- |
| GATEWAY_PROXY_URL | URL of the remote Hermes API server (e.g.,http://192.168.1.100:8642) |
| GATEWAY_PROXY_KEY | Bearer token for authentication (must matchAPI_SERVER_KEYon the host) |
| gateway.proxy_url | Same asGATEWAY_PROXY_URLbut inconfig.yaml |

`GATEWAY_PROXY_URL`
`http://192.168.1.100:8642`
`GATEWAY_PROXY_KEY`
`API_SERVER_KEY`
`gateway.proxy_url`
`GATEWAY_PROXY_URL`
`config.yaml`

The host side needs:

| Setting | Description |
| --- | --- |
| API_SERVER_ENABLED | Set totrue |
| API_SERVER_KEY | Bearer token (shared with the container) |
| API_SERVER_HOST | Set to0.0.0.0for network access |
| API_SERVER_PORT | Port number (default:8642) |

`API_SERVER_ENABLED`
`true`
`API_SERVER_KEY`
`API_SERVER_HOST`
`0.0.0.0`
`API_SERVER_PORT`
`8642`

### Works for Any Platform​

Proxy mode is not limited to Matrix. Any platform adapter can use it — setGATEWAY_PROXY_URLon any gateway instance and it will forward to the remote agent instead of running one locally. This is useful for any deployment where the platform adapter needs to run in a different environment from the agent (network isolation, E2EE requirements, resource constraints).

`GATEWAY_PROXY_URL`

Session continuity is maintained via theX-Hermes-Session-Idheader. The host's API server tracks sessions by this ID, so conversations persist across messages just like they would with a local agent.

`X-Hermes-Session-Id`

Limitations (v1):Tool progress messages from the remote agent are not relayed back — the user sees the streamed final response only, not individual tool calls. Dangerous command approval prompts are handled on the host side, not relayed to the Matrix user. These can be addressed in future updates.

### Bot connects and sends, but ignores inbound messages​

Cause: Matrix event handlers only fire when sync payloads are dispatched through
mautrix'shandle_sync()machinery. A rawclient.sync()poll that never callshandle_sync()can leave the adapter connected (send works) while inbound
messages never reach_on_room_message.

`handle_sync()`
`client.sync()`
`handle_sync()`
`_on_room_message`

Fix: Hermes uses an explicit sync loop that callsclient.handle_sync()on
both the initial sync and every incremental sync response. This matches the
diagnosis in upstream issue #7914 and closed PR #37807, but keeps Hermes's own
background maintenance tasks (joined-room tracking, invite handling, E2EE key
share) instead of delegating the full lifecycle toclient.start(). If inbound
messages still fail after a gateway restart, verify handlers are registered before
the first sync and check logs forsync event dispatch error.

`client.handle_sync()`
`client.start()`
`sync event dispatch error`

### Sync issues / bot falls behind​

Cause: Long-running tool executions can delay the sync loop, or the homeserver is slow.

Fix: The sync loop automatically retries every 5 seconds on error. Check the Hermes logs for sync-related warnings. If the bot consistently falls behind, ensure your homeserver has adequate resources.

### Bot is offline​

Cause: The Hermes gateway isn't running, or it failed to connect.

Fix: Check thathermes gatewayis running. Look at the terminal output for error messages. Common issues: wrong homeserver URL, expired access token, homeserver unreachable.

`hermes gateway`

### "User not allowed" / Bot ignores you​

Cause: Your User ID isn't inMATRIX_ALLOWED_USERS.

`MATRIX_ALLOWED_USERS`

Fix: Add your User ID toMATRIX_ALLOWED_USERSin~/.hermes/.envand restart the gateway. Use the full@user:serverformat.

`MATRIX_ALLOWED_USERS`
`~/.hermes/.env`
`@user:server`

### Bot ignores an entire room​

Cause:MATRIX_ALLOWED_ROOMSis set and the current room ID is not listed, or the room requires a mention and the message did not mention the bot.

`MATRIX_ALLOWED_ROOMS`

Fix: Add the room ID toMATRIX_ALLOWED_ROOMS, or remove the room allowlist if this is a personal deployment. To find a Room ID in Element, open room settings and checkAdvanced.

`MATRIX_ALLOWED_ROOMS`

### Bridge messages loop or echo​

Cause: A bridge/appservice puppet is relaying bot output back as a new user message, or a bridge uses non-standard ghost user IDs.

Fix: Keep bridge ghosts out ofMATRIX_ALLOWED_USERS, add a matchingMATRIX_IGNORE_USER_PATTERNSentry, and leaveMATRIX_PROCESS_NOTICES=falseunless notices are part of a trusted workflow.

`MATRIX_ALLOWED_USERS`
`MATRIX_IGNORE_USER_PATTERNS`
`MATRIX_PROCESS_NOTICES=false`

## Security​

Always setMATRIX_ALLOWED_USERSand, for shared/private deployments,MATRIX_ALLOWED_ROOMS. Without them, anyone who can message the bot in a joined room may trigger the agent. Only authorize people and rooms you trust — authorized users have full access to the agent's capabilities, including tool use and system access.

`MATRIX_ALLOWED_USERS`
`MATRIX_ALLOWED_ROOMS`

For more information on securing your Hermes Agent deployment, see theSecurity Guide.

## Notes​

- Any homeserver: Works with Synapse, Conduit, Dendrite, matrix.org, or any spec-compliant Matrix homeserver. No specific homeserver software required.
- Federation: If you're on a federated homeserver, the bot can communicate with users from other servers — just add their full@user:serverIDs toMATRIX_ALLOWED_USERS.
- Auto-join: The bot automatically accepts room invites and joins. It starts responding immediately after joining.
- Media support: Hermes can send and receive images, audio, video, and file attachments. Media is uploaded to your homeserver using the Matrix content repository API.
- Native voice messages (MSC3245): The Matrix adapter automatically tags outgoing voice messages with theorg.matrix.msc3245.voiceflag. This means TTS responses and voice audio are rendered asnative voice bubblesin Element and other clients that support MSC3245, rather than as generic audio file attachments. Incoming voice messages with the MSC3245 flag are also correctly identified and routed to speech-to-text transcription. No configuration is needed — this works automatically.

`@user:server`
`MATRIX_ALLOWED_USERS`
`org.matrix.msc3245.voice`