- 
- Messaging Platforms
- Popular
- WhatsApp

# WhatsApp Setup

Hermes connects to WhatsApp through a built-in bridge based onBaileys. This works by emulating a WhatsApp Web session —notthrough the official WhatsApp Business API. No Meta developer account or Business verification is required.

> Runhermes gateway setupand pickWhatsAppfor a guided walk-through.

Runhermes gateway setupand pickWhatsAppfor a guided walk-through.

`hermes gateway setup`

This page is for theBaileys bridge— quick to set up, personal accounts, no public URL needed, ban risk.

If you're running a real business bot and want stability, see theWhatsApp Business Cloud API guideinstead. It's the official Meta-supported path: no account ban risk, but requires a Meta Business account and a public webhook URL.

The two adapters can also run in parallel against different phone numbers if you have a reason to.

WhatsApp doesnotofficially support third-party bots outside the Business API. Using a third-party bridge carries a small risk of account restrictions. To minimize risk:

- Use a dedicated phone numberfor the bot (not your personal number)
- Don't send bulk/spam messages— keep usage conversational
- Don't automate outbound messagingto people who haven't messaged first

WhatsApp periodically updates their Web protocol, which can temporarily break compatibility
with third-party bridges. When this happens, Hermes will update the bridge dependency. If the
bot stops working after a WhatsApp update, pull the latest Hermes version and re-pair.

## Two Modes​

| Mode | How it works | Best for |
| --- | --- | --- |
| Separate bot number(recommended) | Dedicate a phone number to the bot. People message that number directly. | Clean UX, multiple users, lower ban risk |
| Personal self-chat | Use your own WhatsApp. You message yourself to talk to the agent. | Quick setup, single user, testing |

## Prerequisites​

- Node.js v18+andnpm— the WhatsApp bridge runs as a Node.js process
- A phone with WhatsAppinstalled (for scanning the QR code)

Unlike older browser-driven bridges, the current Baileys-based bridge doesnotrequire a local Chromium or Puppeteer dependency stack.

## Step 1: Run the Setup Wizard​

```
hermes whatsapp
```

The wizard will:

1. Ask which mode you want (botorself-chat)
2. Install bridge dependencies if needed
3. Display aQR codein your terminal
4. Wait for you to scan it

To scan the QR code:

1. Open WhatsApp on your phone
2. Go toSettings → Linked Devices
3. TapLink a Device
4. Point your camera at the terminal QR code

Once paired, the wizard confirms the connection and exits. Your session is saved automatically.

If the QR code looks garbled, make sure your terminal is at least 60 columns wide and supports
Unicode. You can also try a different terminal emulator.

## Step 2: Getting a Second Phone Number (Bot Mode)​

For bot mode, you need a phone number that isn't already registered with WhatsApp. Three options:

| Option | Cost | Notes |
| --- | --- | --- |
| Google Voice | Free | US only. Get a number atvoice.google.com. Verify WhatsApp via SMS through the Google Voice app. |
| Prepaid SIM | $5–15 one-time | Any carrier. Activate, verify WhatsApp, then the SIM can sit in a drawer. Number must stay active (make a call every 90 days). |
| VoIP services | Free–$5/month | TextNow, TextFree, or similar. Some VoIP numbers are blocked by WhatsApp — try a few if the first doesn't work. |

After getting the number:

1. Install WhatsApp on a phone (or use WhatsApp Business app with dual-SIM)
2. Register the new number with WhatsApp
3. Runhermes whatsappand scan the QR code from that WhatsApp account

`hermes whatsapp`

## Step 3: Configure Hermes​

Add the following to your~/.hermes/.envfile:

`~/.hermes/.env`

```
# RequiredWHATSAPP_ENABLED=trueWHATSAPP_MODE=bot                          # "bot" or "self-chat"# Access control — pick ONE of these options:WHATSAPP_ALLOWED_USERS=15551234567         # Comma-separated phone numbers (with country code, no +)# WHATSAPP_ALLOWED_USERS=*                 # OR use * to allow everyone# WHATSAPP_ALLOW_ALL_USERS=true            # OR set this flag instead (same effect as *)
```

SettingWHATSAPP_ALLOWED_USERS=*allowsallsenders (equivalent toWHATSAPP_ALLOW_ALL_USERS=true).
This is consistent withSignal group allowlists.
To use the pairing flow instead, remove both variables and rely on theDM pairing system.

`WHATSAPP_ALLOWED_USERS=*`
`WHATSAPP_ALLOW_ALL_USERS=true`

Optional behavior settings in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
unauthorized_dm_behavior: pairwhatsapp:  unauthorized_dm_behavior: ignore
```

- unauthorized_dm_behavior: pairis the global default. Unknown DM senders get a pairing code.
- whatsapp.unauthorized_dm_behavior: ignoremakes WhatsApp stay silent for unauthorized DMs, which is usually the better choice for a private number.

`unauthorized_dm_behavior: pair`
`whatsapp.unauthorized_dm_behavior: ignore`

Then start the gateway:

```
hermes gateway              # Foregroundhermes gateway install      # Install as a user servicesudo hermes gateway install --system   # Linux only: boot-time system service
```

The gateway starts the WhatsApp bridge automatically using the saved session.

## Session Persistence​

The Baileys bridge saves its session under~/.hermes/platforms/whatsapp/session. This means:

`~/.hermes/platforms/whatsapp/session`
- Sessions survive restarts— you don't need to re-scan the QR code every time
- The session data includes encryption keys and device credentials
- Do not share or commit this session directory— it grants full access to the WhatsApp account

## Re-pairing​

If the session breaks (phone reset, WhatsApp update, manually unlinked), you'll see connection
errors in the gateway logs. To fix it:

```
hermes whatsapp
```

This generates a fresh QR code. Scan it again and the session is re-established. The gateway
handlestemporarydisconnections (network blips, phone going offline briefly) automatically
with reconnection logic.

## Voice Messages​

Hermes supports voice on WhatsApp:

- Incoming:Voice messages (.oggopus) are automatically transcribed using the configured STT provider: localfaster-whisper, Groq Whisper (GROQ_API_KEY), or OpenAI Whisper (VOICE_TOOLS_OPENAI_KEY)
- Outgoing:TTS responses are sent as MP3 audio file attachments
- Agent responses are prefixed with "⚕Hermes Agent" by default. You can customize or disable this inconfig.yaml:

`.ogg`
`faster-whisper`
`GROQ_API_KEY`
`VOICE_TOOLS_OPENAI_KEY`
`config.yaml`

```
# ~/.hermes/config.yamlwhatsapp:  reply_prefix: ""                          # Empty string disables the header  # reply_prefix: "🤖 *My Bot*\n──────\n"  # Custom prefix (supports \n for newlines)
```

## Message Formatting & Delivery​

WhatsApp supportsstreaming (progressive) responses— the bot edits its message in real-time as the AI generates text, just like Discord and Telegram. Internally, WhatsApp is classified as a TIER_MEDIUM platform for delivery capabilities.

### Chunking​

Long responses are automatically split into multiple messages at4,096 charactersper chunk (WhatsApp's practical display limit). You don't need to configure anything — the gateway handles splitting and sends chunks sequentially.

### WhatsApp-Compatible Markdown​

Standard Markdown in AI responses is automatically converted to WhatsApp's native formatting:

| Markdown | WhatsApp | Renders as |
| --- | --- | --- |
| **bold** | *bold* | bold |
| ~~strikethrough~~ | ~strikethrough~ | strikethrough |
| # Heading | *Heading* | Bold text (no native headings) |
| [link text](url) | link text (url) | Inline URL |

`**bold**`
`*bold*`
`~~strikethrough~~`
`~strikethrough~`
`# Heading`
`*Heading*`
`[link text](url)`
`link text (url)`

Code blocks and inline code are preserved as-is since WhatsApp supports triple-backtick formatting natively.

### Tool Progress​

When the agent calls tools (web search, file operations, etc.), WhatsApp displays real-time progress indicators showing which tool is running. This is enabled by default — no configuration needed.

### Message Batching (Debounce)​

WhatsApp delivers each message individually, so a rapid burst (forwarded batches, paste-splits, multi-line text) would otherwise trigger a separate agent invocation per fragment — wasting tokens and producing several disjointed replies. The adapter buffers successive text messages from the same chat and dispatches them as one combined request after a short quiet period (default5s, extended to10sfor very long fragments). Tune viaconfig.yaml:

`config.yaml`

```
# ~/.hermes/config.yamlgateway:  platforms:    whatsapp:      extra:        text_batch_delay_seconds: 5.0         # quiet period before flushing a batch        text_batch_split_delay_seconds: 10.0  # extended delay near the split threshold
```

Settext_batch_delay_seconds: 0to dispatch each message immediately (disables batching).

`text_batch_delay_seconds: 0`

## Troubleshooting​

| Problem | Solution |
| --- | --- |
| QR code not scanning | Ensure terminal is wide enough (60+ columns). Try a different terminal. Make sure you're scanning from the correct WhatsApp account (bot number, not personal). |
| QR code expires | QR codes refresh every ~20 seconds. If it times out, restarthermes whatsapp. |
| Session not persisting | Check that~/.hermes/platforms/whatsapp/sessionexists and is writable. If containerized, mount it as a persistent volume. |
| Logged out unexpectedly | WhatsApp unlinks devices after long inactivity. Keep the phone on and connected to the network, then re-pair withhermes whatsappif needed. |
| Bridge crashes or reconnect loops | Restart the gateway, update Hermes, and re-pair if the session was invalidated by a WhatsApp protocol change. |
| Bot stops working after WhatsApp update | Update Hermes to get the latest bridge version, then re-pair. |
| macOS: "Node.js not installed" but node works in terminal | launchd services don't inherit your shell PATH. Runhermes gateway installto re-snapshot your current PATH into the plist, thenhermes gateway start. See theGateway Service docsfor details. |
| Messages not being received | VerifyWHATSAPP_ALLOWED_USERSincludes the sender's number (with country code, no+or spaces), or set it to*to allow everyone. SetWHATSAPP_DEBUG=truein.envand restart the gateway to see raw message events inbridge.log. |
| Bot replies to strangers with a pairing code | Setwhatsapp.unauthorized_dm_behavior: ignorein~/.hermes/config.yamlif you want unauthorized DMs to be silently ignored instead. |

`hermes whatsapp`
`~/.hermes/platforms/whatsapp/session`
`hermes whatsapp`
`hermes gateway install`
`hermes gateway start`
`WHATSAPP_ALLOWED_USERS`
`+`
`*`
`WHATSAPP_DEBUG=true`
`.env`
`bridge.log`
`whatsapp.unauthorized_dm_behavior: ignore`
`~/.hermes/config.yaml`

## Security​

Configure access controlbefore going live. SetWHATSAPP_ALLOWED_USERSwith specific
phone numbers (including country code, without the+), use*to allow everyone, or setWHATSAPP_ALLOW_ALL_USERS=true. Without any of these, the gatewaydenies all incoming
messagesas a safety measure.

`WHATSAPP_ALLOWED_USERS`
`+`
`*`
`WHATSAPP_ALLOW_ALL_USERS=true`

By default, unauthorized DMs still receive a pairing code reply. If you want a private WhatsApp number to stay completely silent to strangers, set:

```
whatsapp:  unauthorized_dm_behavior: ignore
```

- The~/.hermes/platforms/whatsapp/sessiondirectory contains full session credentials — protect it like a password
- Set file permissions:chmod 700 ~/.hermes/platforms/whatsapp/session
- Use adedicated phone numberfor the bot to isolate risk from your personal account
- If you suspect compromise, unlink the device from WhatsApp → Settings → Linked Devices
- Phone numbers in logs are partially redacted, but review your log retention policy

`~/.hermes/platforms/whatsapp/session`
`chmod 700 ~/.hermes/platforms/whatsapp/session`