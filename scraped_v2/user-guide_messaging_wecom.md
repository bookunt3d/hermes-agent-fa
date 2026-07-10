- 
- Messaging Platforms
- Chinese platforms
- WeCom (Enterprise WeChat)

# WeCom (Enterprise WeChat)

Connect Hermes toWeCom(企业微信), Tencent's enterprise messaging platform. The adapter uses WeCom's AI Bot WebSocket gateway for real-time bidirectional communication — no public endpoint or webhook needed.

See also:WeCom Callbackfor inbound webhook setup.

## Prerequisites​

- A WeCom organization account
- An AI Bot created in the WeCom Admin Console
- The Bot ID and Secret from the bot's credentials page
- Python packages:aiohttpandhttpx

`aiohttp`
`httpx`

## Setup​

### Step 1: Create an AI Bot​

#### Recommended: Scan-to-Create (one command)​

```
hermes gateway setup
```

SelectWeComand scan the QR code with your WeCom mobile app. Hermes will automatically create a bot application with the correct permissions and save the credentials.

The setup wizard will:

1. Display a QR code in your terminal
2. Wait for you to scan it with the WeCom mobile app
3. Automatically retrieve the Bot ID and Secret
4. Guide you through access control configuration

#### Alternative: Manual Setup​

If scan-to-create is not available, the wizard falls back to manual input:

1. Log in to theWeCom Admin Console
2. Navigate toApplications→Create Application→AI Bot
3. Configure the bot name and description
4. Copy theBot IDandSecretfrom the credentials page
5. Runhermes gateway setup, selectWeCom, and enter the credentials when prompted

`hermes gateway setup`

Keep the Bot Secret private. Anyone with it can impersonate your bot.

### Step 2: Configure Hermes​

#### Option A: Interactive Setup (Recommended)​

```
hermes gateway setup
```

SelectWeComand follow the prompts. The wizard will guide you through:

- Bot credentials (via QR scan or manual entry)
- Access control settings (allowlist, pairing mode, or open access)
- Home channel for notifications

#### Option B: Manual Configuration​

Add the following to~/.hermes/.env:

`~/.hermes/.env`

```
WECOM_BOT_ID=your-bot-idWECOM_SECRET=your-secret# Optional: restrict accessWECOM_ALLOWED_USERS=user_id_1,user_id_2# Optional: home channel for cron/notificationsWECOM_HOME_CHANNEL=chat_id
```

### Step 3: Start the gateway​

```
hermes gateway
```

## Features​

- WebSocket transport— persistent connection, no public endpoint needed
- DM and group messaging— configurable access policies
- Per-group sender allowlists— fine-grained control over who can interact in each group
- Media support— images, files, voice, video upload and download
- AES-encrypted media— automatic decryption for inbound attachments
- Quote context— preserves reply threading
- Markdown rendering— rich text responses
- Reply correlation— responses are correlated to the inbound message context
- Auto-reconnect— exponential backoff on connection drops

The WeCom adapter delivers each response as a single complete message — it doesnotstream responses token-by-token, and it doesnotshow a typing
indicator. "Reply correlation" (below) only threads a response to its inbound
request; it is not live streaming.

## Configuration Options​

Set these inconfig.yamlunderplatforms.wecom.extra:

`config.yaml`
`platforms.wecom.extra`
| Key | Default | Description |
| --- | --- | --- |
| bot_id | — | WeCom AI Bot ID (required) |
| secret | — | WeCom AI Bot Secret (required) |
| websocket_url | wss://openws.work.weixin.qq.com | WebSocket gateway URL |
| dm_policy | open | DM access:open,allowlist,disabled,pairing |
| group_policy | open | Group access:open,allowlist,disabled |
| allow_from | [] | User IDs allowed for DMs (when dm_policy=allowlist) |
| group_allow_from | [] | Group IDs allowed (when group_policy=allowlist) |
| groups | {} | Per-group configuration (see below) |

`bot_id`
`secret`
`websocket_url`
`wss://openws.work.weixin.qq.com`
`dm_policy`
`open`
`open`
`allowlist`
`disabled`
`pairing`
`group_policy`
`open`
`open`
`allowlist`
`disabled`
`allow_from`
`[]`
`group_allow_from`
`[]`
`groups`
`{}`

## Access Policies​

### DM Policy​

Controls who can send direct messages to the bot:

| Value | Behavior |
| --- | --- |
| open | Anyone can DM the bot (default) |
| allowlist | Only user IDs inallow_fromcan DM |
| disabled | All DMs are ignored |
| pairing | Pairing mode (for initial setup) |

`open`
`allowlist`
`allow_from`
`disabled`
`pairing`

```
WECOM_DM_POLICY=allowlist
```

### Group Policy​

Controls which groups the bot responds in:

| Value | Behavior |
| --- | --- |
| open | Bot responds in all groups (default) |
| allowlist | Bot only responds in group IDs listed ingroup_allow_from |
| disabled | All group messages are ignored |

`open`
`allowlist`
`group_allow_from`
`disabled`

```
WECOM_GROUP_POLICY=allowlist
```

### Per-Group Sender Allowlists​

For fine-grained control, you can restrict which users are allowed to interact with the bot within specific groups. This is configured inconfig.yaml:

`config.yaml`

```
platforms:  wecom:    enabled: true    extra:      bot_id: "your-bot-id"      secret: "your-secret"      group_policy: "allowlist"      group_allow_from:        - "group_id_1"        - "group_id_2"      groups:        group_id_1:          allow_from:            - "user_alice"            - "user_bob"        group_id_2:          allow_from:            - "user_charlie"        "*":          allow_from:            - "user_admin"
```

How it works:

1. Thegroup_policyandgroup_allow_fromcontrols determine whether a group is allowed at all.
2. If a group passes the top-level check, thegroups.<group_id>.allow_fromlist (if present) further restricts which senders within that group can interact with the bot.
3. A wildcard"*"group entry serves as a default for groups not explicitly listed.
4. Allowlist entries support the*wildcard to allow all users, and entries are case-insensitive.
5. Entries can optionally use thewecom:user:orwecom:group:prefix format — the prefix is stripped automatically.

`group_policy`
`group_allow_from`
`groups.<group_id>.allow_from`
`"*"`
`*`
`wecom:user:`
`wecom:group:`

If noallow_fromis configured for a group, all users in that group are allowed (assuming the group itself passes the top-level policy check).

`allow_from`

## Media Support​

### Inbound (receiving)​

The adapter receives media attachments from users and caches them locally for agent processing:

| Type | How it's handled |
| --- | --- |
| Images | Downloaded and cached locally. Supports both URL-based and base64-encoded images. |
| Files | Downloaded and cached. Filename is preserved from the original message. |
| Voice | Voice message text transcription is extracted if available. |
| Mixed messages | WeCom mixed-type messages (text + images) are parsed and all components extracted. |

Quoted messages:Media from quoted (replied-to) messages is also extracted, so the agent has context about what the user is replying to.

### AES-Encrypted Media Decryption​

WeCom encrypts some inbound media attachments with AES-256-CBC. The adapter handles this automatically:

- When an inbound media item includes anaeskeyfield, the adapter downloads the encrypted bytes and decrypts them using AES-256-CBC with PKCS#7 padding.
- The AES key is the base64-decoded value of theaeskeyfield (must be exactly 32 bytes).
- The IV is derived from the first 16 bytes of the key.
- This requires thecryptographyPython package (pip install cryptography).

`aeskey`
`aeskey`
`cryptography`
`pip install cryptography`

No configuration is needed — decryption happens transparently when encrypted media is received.

### Outbound (sending)​

| Method | What it sends | Size limit |
| --- | --- | --- |
| send | Markdown text messages | 4000 chars |
| send_image/send_image_file | Native image messages | 10 MB |
| send_document | File attachments | 20 MB |
| send_voice | Voice messages (AMR format only for native voice) | 2 MB |
| send_video | Video messages | 10 MB |

`send`
`send_image`
`send_image_file`
`send_document`
`send_voice`
`send_video`

Chunked upload:Files are uploaded in 512 KB chunks through a three-step protocol (init → chunks → finish). The adapter handles this automatically.

Automatic downgrade:When media exceeds the native type's size limit but is under the absolute 20 MB file limit, it is automatically sent as a generic file attachment instead:

- Images > 10 MB → sent as file
- Videos > 10 MB → sent as file
- Voice > 2 MB → sent as file
- Non-AMR audio → sent as file (WeCom only supports AMR for native voice)

Files exceeding the absolute 20 MB limit are rejected with an informational message sent to the chat.

## Reply-Mode Responses​

When the bot receives a message via the WeCom callback, the adapter remembers the inbound request ID. If a response is sent while the request context is still active, the adapter uses WeCom's reply-mode (aibot_respond_msg) to correlate the response directly to the inbound message. This provides a more natural conversation experience in the WeCom client.

`aibot_respond_msg`

The full response is delivered as a single message — the adapter does not stream tokens incrementally. If the inbound request context has expired or is unavailable, the adapter falls back to proactive message sending viaaibot_send_msg.

`aibot_send_msg`

Reply-mode also works for media: uploaded media can be sent as a reply to the originating message.

## Connection and Reconnection​

The adapter maintains a persistent WebSocket connection to WeCom's gateway atwss://openws.work.weixin.qq.com.

`wss://openws.work.weixin.qq.com`

### Connection Lifecycle​

1. Connect:Opens a WebSocket connection and sends anaibot_subscribeauthentication frame with the bot_id and secret.
2. Heartbeat:Sends application-level ping frames every 30 seconds to keep the connection alive.
3. Listen:Continuously reads inbound frames and dispatches message callbacks.

`aibot_subscribe`

### Reconnection Behavior​

On connection loss, the adapter uses exponential backoff to reconnect:

| Attempt | Delay |
| --- | --- |
| 1st retry | 2 seconds |
| 2nd retry | 5 seconds |
| 3rd retry | 10 seconds |
| 4th retry | 30 seconds |
| 5th+ retry | 60 seconds |

After each successful reconnection, the backoff counter resets to zero. All pending request futures are failed on disconnect so callers don't hang indefinitely.

### Deduplication​

Inbound messages are deduplicated using message IDs with a 5-minute window and a maximum cache of 1000 entries. This prevents double-processing of messages during reconnection or network hiccups.

## All Environment Variables​

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| WECOM_BOT_ID | ✅ | — | WeCom AI Bot ID |
| WECOM_SECRET | ✅ | — | WeCom AI Bot Secret |
| WECOM_ALLOWED_USERS | — | (empty) | Comma-separated user IDs for the gateway-level allowlist |
| WECOM_HOME_CHANNEL | — | — | Chat ID for cron/notification output |
| WECOM_WEBSOCKET_URL | — | wss://openws.work.weixin.qq.com | WebSocket gateway URL |
| WECOM_DM_POLICY | — | open | DM access policy |
| WECOM_GROUP_POLICY | — | open | Group access policy |

`WECOM_BOT_ID`
`WECOM_SECRET`
`WECOM_ALLOWED_USERS`
`WECOM_HOME_CHANNEL`
`WECOM_WEBSOCKET_URL`
`wss://openws.work.weixin.qq.com`
`WECOM_DM_POLICY`
`open`
`WECOM_GROUP_POLICY`
`open`

## Troubleshooting​

| Problem | Fix |
| --- | --- |
| WECOM_BOT_ID and WECOM_SECRET are required | Set both env vars or configure in setup wizard |
| WeCom startup failed: aiohttp not installed | Install aiohttp:pip install aiohttp |
| WeCom startup failed: httpx not installed | Install httpx:pip install httpx |
| invalid secret (errcode=40013) | Verify the secret matches your bot's credentials |
| Timed out waiting for subscribe acknowledgement | Check network connectivity toopenws.work.weixin.qq.com |
| Bot doesn't respond in groups | Checkgroup_policysetting and ensure the group ID is ingroup_allow_from |
| Bot ignores certain users in a group | Check per-groupallow_fromlists in thegroupsconfig section |
| Media decryption fails | Installcryptography:pip install cryptography |
| cryptography is required for WeCom media decryption | The inbound media is AES-encrypted. Install:pip install cryptography |
| Voice messages sent as files | WeCom only supports AMR format for native voice. Other formats are auto-downgraded to file. |
| File too largeerror | WeCom has a 20 MB absolute limit on all file uploads. Compress or split the file. |
| Images sent as files | Images > 10 MB exceed the native image limit and are auto-downgraded to file attachments. |
| Timeout sending message to WeCom | The WebSocket may have disconnected. Check logs for reconnection messages. |
| WeCom websocket closed during authentication | Network issue or incorrect credentials. Verify bot_id and secret. |

`WECOM_BOT_ID and WECOM_SECRET are required`
`WeCom startup failed: aiohttp not installed`
`pip install aiohttp`
`WeCom startup failed: httpx not installed`
`pip install httpx`
`invalid secret (errcode=40013)`
`Timed out waiting for subscribe acknowledgement`
`openws.work.weixin.qq.com`
`group_policy`
`group_allow_from`
`allow_from`
`groups`
`cryptography`
`pip install cryptography`
`cryptography is required for WeCom media decryption`
`pip install cryptography`
`File too large`
`Timeout sending message to WeCom`
`WeCom websocket closed during authentication`