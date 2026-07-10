- 
- Developer Guide
- Architecture
- Gateway Internals

# Gateway Internals

The messaging gateway is the long-running process that connects Hermes to 20+ external messaging platforms through a unified architecture.

## Key Files​

| File | Purpose |
| --- | --- |
| gateway/run.py | GatewayRunner— main loop, slash commands, message dispatch (large file; check git for current LOC) |
| gateway/session.py | SessionStore— conversation persistence and session key construction |
| gateway/delivery.py | Outbound message delivery to target platforms/channels |
| gateway/pairing.py | DM pairing flow for user authorization |
| gateway/channel_directory.py | Maps chat IDs to human-readable names for cron delivery |
| gateway/hooks.py | Hook discovery, loading, and lifecycle event dispatch |
| gateway/mirror.py | Cross-session message mirroring forsend_message |
| gateway/status.py | Token lock management for profile-scoped gateway instances |
| gateway/builtin_hooks/ | Extension point for always-registered hooks (none shipped) |
| gateway/platforms/ | Platform adapters (one per messaging platform) |

`gateway/run.py`
`GatewayRunner`
`gateway/session.py`
`SessionStore`
`gateway/delivery.py`
`gateway/pairing.py`
`gateway/channel_directory.py`
`gateway/hooks.py`
`gateway/mirror.py`
`send_message`
`gateway/status.py`
`gateway/builtin_hooks/`
`gateway/platforms/`

## Architecture Overview​

```
┌─────────────────────────────────────────────────┐│                  GatewayRunner                  ││                                                 ││  ┌──────────┐  ┌──────────┐  ┌──────────┐       ││  │ Telegram │  │ Discord  │  │  Slack   │       ││  │ Adapter  │  │ Adapter  │  │ Adapter  │       ││  └────┬─────┘  └────┬─────┘  └────┬─────┘       ││       │             │             │             ││       └─────────────┼─────────────┘             ││                     ▼                           ││              _handle_message()                  ││                     │                           ││         ┌───────────┼───────────┐               ││         ▼           ▼           ▼               ││  Slash command   AIAgent    Queue/BG            ││    dispatch      creation   sessions            ││                     │                           ││                     ▼                           ││                 SessionStore                    ││              (SQLite persistence)               │└───────┴─────────────┴─────────────┴─────────────┘
```

## Message Flow​

When a message arrives from any platform:

1. Platform adapterreceives raw event, normalizes it into aMessageEvent
2. Base adapterchecks active session guard:If agent is running for this session → queue message, set interrupt eventIf/approve,/deny,/stop→ bypass guard (dispatched inline)
3. GatewayRunner._handle_message()receives the event:Resolve session key via_session_key_for_source()(format:agent:main:{platform}:{chat_type}:{chat_id})Check authorization (see Authorization below)Check if it's a slash command → dispatch to command handlerCheck if agent is already running → intercept commands like/stop,/statusOtherwise → createAIAgentinstance and run conversation
4. Responseis sent back through the platform adapter

`MessageEvent`
- If agent is running for this session → queue message, set interrupt event
- If/approve,/deny,/stop→ bypass guard (dispatched inline)

`/approve`
`/deny`
`/stop`
- Resolve session key via_session_key_for_source()(format:agent:main:{platform}:{chat_type}:{chat_id})
- Check authorization (see Authorization below)
- Check if it's a slash command → dispatch to command handler
- Check if agent is already running → intercept commands like/stop,/status
- Otherwise → createAIAgentinstance and run conversation

`_session_key_for_source()`
`agent:main:{platform}:{chat_type}:{chat_id}`
`/stop`
`/status`
`AIAgent`

### Session Key Format​

Session keys encode the full routing context:

```
agent:main:{platform}:{chat_type}:{chat_id}
```

For example:agent:main:telegram:private:123456789

`agent:main:telegram:private:123456789`

Thread-aware platforms (Telegram forum topics, Discord threads, Slack threads) may include thread IDs in the chat_id portion.Never construct session keys manually— always usebuild_session_key()fromgateway/session.py.

`build_session_key()`
`gateway/session.py`

### Two-Level Message Guard​

When an agent is actively running, incoming messages pass through two sequential guards:

1. Level 1 — Base adapter(gateway/platforms/base.py): Checks_active_sessions. If the session is active, queues the message in_pending_messagesand sets an interrupt event. This catches messagesbeforethey reach the gateway runner.
2. Level 2 — Gateway runner(gateway/run.py): Checks_running_agents. Intercepts specific commands (/stop,/new,/queue,/status,/approve,/deny) and routes them appropriately. Everything else triggersrunning_agent.interrupt().

Level 1 — Base adapter(gateway/platforms/base.py): Checks_active_sessions. If the session is active, queues the message in_pending_messagesand sets an interrupt event. This catches messagesbeforethey reach the gateway runner.

`gateway/platforms/base.py`
`_active_sessions`
`_pending_messages`

Level 2 — Gateway runner(gateway/run.py): Checks_running_agents. Intercepts specific commands (/stop,/new,/queue,/status,/approve,/deny) and routes them appropriately. Everything else triggersrunning_agent.interrupt().

`gateway/run.py`
`_running_agents`
`/stop`
`/new`
`/queue`
`/status`
`/approve`
`/deny`
`running_agent.interrupt()`

Commands that must reach the runner while the agent is blocked (like/approve) are dispatchedinlineviaawait self._message_handler(event)— they bypass the background task system to avoid race conditions.

`/approve`
`await self._message_handler(event)`

## Authorization​

The gateway uses a multi-layer authorization check, evaluated in order:

1. Per-platform allow-all flag(e.g.,TELEGRAM_ALLOW_ALL_USERS) — if set, all users on that platform are authorized
2. Platform allowlist(e.g.,TELEGRAM_ALLOWED_USERS) — comma-separated user IDs
3. DM pairing— authenticated users can pair new users via a pairing code
4. Global allow-all(GATEWAY_ALLOW_ALL_USERS) — if set, all users across all platforms are authorized
5. Default: deny— unauthorized users are rejected

`TELEGRAM_ALLOW_ALL_USERS`
`TELEGRAM_ALLOWED_USERS`
`GATEWAY_ALLOW_ALL_USERS`

### DM Pairing Flow​

```
Admin: /pairGateway: "Pairing code: ABC123. Share with the user."New user: ABC123Gateway: "Paired! You're now authorized."
```

Pairing state is persisted ingateway/pairing.pyand survives restarts.

`gateway/pairing.py`

## Slash Command Dispatch​

All slash commands in the gateway flow through the same resolution pipeline:

1. resolve_command()fromhermes_cli/commands.pymaps input to canonical name (handles aliases, prefix matching)
2. The canonical name is checked againstGATEWAY_KNOWN_COMMANDS
3. Handler in_handle_message()dispatches based on canonical name
4. Some commands are gated on config (gateway_config_gateonCommandDef)

`resolve_command()`
`hermes_cli/commands.py`
`GATEWAY_KNOWN_COMMANDS`
`_handle_message()`
`gateway_config_gate`
`CommandDef`

### Running-Agent Guard​

Commands that must NOT execute while the agent is processing are rejected early:

```
if _quick_key in self._running_agents:    if canonical == "model":        return "⏳ Agent is running — wait for it to finish or /stop first."
```

Bypass commands (/stop,/new,/approve,/deny,/queue,/status) have special handling.

`/stop`
`/new`
`/approve`
`/deny`
`/queue`
`/status`

## Config Sources​

The gateway reads configuration from multiple sources:

| Source | What it provides |
| --- | --- |
| ~/.hermes/.env | API keys, bot tokens, platform credentials |
| ~/.hermes/config.yaml | Model settings, tool configuration, display options |
| Environment variables | Override any of the above |

`~/.hermes/.env`
`~/.hermes/config.yaml`

Unlike the CLI (which usesload_cli_config()with hardcoded defaults), the gateway readsconfig.yamldirectly via YAML loader. This means config keys that exist in the CLI's defaults dict but not in the user's config file may behave differently between CLI and gateway.

`load_cli_config()`
`config.yaml`

## Platform Adapters​

Most messaging platforms ship as plugin adapters underplugins/platforms/<name>/adapter.py; a few legacy adapters still live directly ingateway/platforms/. All extendBasePlatformAdapterfromgateway/platforms/base.py:

`plugins/platforms/<name>/adapter.py`
`gateway/platforms/`
`BasePlatformAdapter`
`gateway/platforms/base.py`

```
plugins/platforms/                  # plugin-packaged adapters (one dir each)├── telegram/adapter.py     # Telegram Bot API (long polling or webhook)├── discord/adapter.py      # Discord bot via discord.py├── slack/adapter.py        # Slack Socket Mode├── whatsapp/adapter.py     # WhatsApp Business Cloud API├── matrix/adapter.py       # Matrix via mautrix (optional E2EE)├── mattermost/adapter.py   # Mattermost WebSocket API├── email/adapter.py        # Email via IMAP/SMTP├── sms/adapter.py          # SMS via Twilio├── dingtalk/adapter.py     # DingTalk WebSocket├── feishu/adapter.py       # Feishu/Lark WebSocket or webhook├── wecom/adapter.py        # WeCom (WeChat Work) callback├── line/adapter.py         # LINE Messaging API├── teams/adapter.py        # Microsoft Teams├── irc/adapter.py          # IRC (canonical scoped-lock example)├── homeassistant/adapter.py # Home Assistant conversation integration└── …                       # google_chat, ntfy, photon, raft, simplex, …gateway/platforms/                  # core base + legacy direct adapters├── base.py              # BasePlatformAdapter — shared logic for all platforms├── signal.py            # Signal via signal-cli REST API├── weixin.py            # Weixin (personal WeChat) via iLink Bot API├── bluebubbles.py       # Apple iMessage via BlueBubbles macOS server├── qqbot/               # QQ Bot (Tencent QQ) via Official API v2 (sub-package)├── yuanbao.py           # Yuanbao (Tencent) DM/group adapter├── msgraph_webhook.py   # Microsoft Graph change-notification webhook (Teams, Outlook, etc.)├── webhook.py           # Inbound/outbound webhook adapter└── api_server.py        # REST API server adapter
```

Experimental connector-backed platforms use the generic relay adapter ingateway/relay/instead of a direct platform module. WhenGATEWAY_RELAY_URLorgateway.relay_urlis configured, the gateway registers therelayplatform, dials the connector over an outbound WebSocket, and receivesdescriptor,inbound, andinterrupt_inboundframes on that same socket. The connector advertises aCapabilityDescriptor; Hermes can send normal outbound replies, token-lessfollow_upoperations, and interrupt frames back through the relay. The source-grounded wire contract lives indocs/relay-connector-contract.md.

`gateway/relay/`
`GATEWAY_RELAY_URL`
`gateway.relay_url`
`relay`
`descriptor`
`inbound`
`interrupt_inbound`
`CapabilityDescriptor`
`follow_up`
`docs/relay-connector-contract.md`

Adapters implement a common interface:

- connect()/disconnect()— lifecycle management
- send_message()— outbound message delivery
- on_message()— inbound message normalization →MessageEvent

`connect()`
`disconnect()`
`send_message()`
`on_message()`
`MessageEvent`

### Token Locks​

Adapters that connect with unique credentials callacquire_scoped_lock()inconnect()andrelease_scoped_lock()indisconnect(). This prevents two profiles from using the same bot token simultaneously.

`acquire_scoped_lock()`
`connect()`
`release_scoped_lock()`
`disconnect()`

## Delivery Path​

Outgoing deliveries (gateway/delivery.py) handle:

`gateway/delivery.py`
- Direct reply— send response back to the originating chat
- Home channel delivery— route cron job outputs and background results to a configured home channel
- Explicit target delivery— the send engine specifyingtelegram:-1001234567890, exposed via thehermes sendCLIfor shell scripts and via crondeliver:targets
- Cross-platform delivery— deliver to a different platform than the originating message

`telegram:-1001234567890`
`hermes send`
`deliver:`

Cron job deliveries are NOT mirrored into gateway session history — they live in their own cron session only. This is a deliberate design choice to avoid message alternation violations.

## Hooks​

Gateway hooks are Python modules that respond to lifecycle events:

### Gateway Hook Events​

| Event | When fired |
| --- | --- |
| gateway:startup | Gateway process starts |
| session:start | New conversation session begins |
| session:end | Session completes or times out |
| session:reset | User resets session with/new |
| agent:start | Agent begins processing a message |
| agent:step | Agent completes one tool-calling iteration |
| agent:end | Agent finishes and returns response |
| command:* | Any slash command is executed |

`gateway:startup`
`session:start`
`session:end`
`session:reset`
`/new`
`agent:start`
`agent:step`
`agent:end`
`command:*`

Hooks are discovered fromgateway/builtin_hooks/(an extension point — currently empty in the shipped distribution;_register_builtin_hooks()is a no-op stub) and~/.hermes/hooks/(user-installed). Each hook is a directory with aHOOK.yamlmanifest andhandler.py.

`gateway/builtin_hooks/`
`_register_builtin_hooks()`
`~/.hermes/hooks/`
`HOOK.yaml`
`handler.py`

## Memory Provider Integration​

When a memory provider plugin (e.g., Honcho) is enabled:

1. Gateway creates anAIAgentper message with the session ID
2. TheMemoryManagerinitializes the provider with the session context
3. Provider tools (e.g.,honcho_profile,viking_search) are routed through:

`AIAgent`
`MemoryManager`
`honcho_profile`
`viking_search`

```
AIAgent._invoke_tool()  → self._memory_manager.handle_tool_call(name, args)    → provider.handle_tool_call(name, args)
```

1. On session end/reset,on_session_end()fires for cleanup and final data flush

`on_session_end()`

### Memory Flush Lifecycle​

When a session is reset, resumed, or expires:

1. Built-in memories are flushed to disk
2. Memory provider'son_session_end()hook fires
3. A temporaryAIAgentruns a memory-only conversation turn
4. Context is then discarded or archived

`on_session_end()`
`AIAgent`

## Background Maintenance​

The gateway runs periodic maintenance alongside message handling:

- Cron ticking— checks job schedules and fires due jobs
- Session expiry— cleans up abandoned sessions after timeout
- Memory flush— proactively flushes memory before session expiry
- Cache refresh— refreshes model lists and provider status

## Process Management​

The gateway runs as a long-lived process, managed via:

- hermes gateway start/hermes gateway stop— manual control
- systemctl(Linux) orlaunchctl(macOS) — service management
- PID file at~/.hermes/gateway.pid— profile-scoped process tracking

`hermes gateway start`
`hermes gateway stop`
`systemctl`
`launchctl`
`~/.hermes/gateway.pid`

Profile-scoped vs global:start_gateway()uses profile-scoped PID files.hermes gateway stopstops only the current profile's gateway.hermes gateway stop --alluses globalps auxscanning to kill all gateway processes (used during updates).

`start_gateway()`
`hermes gateway stop`
`hermes gateway stop --all`
`ps aux`

## Related Docs​

- Session Storage
- Cron Internals
- ACP Internals
- Agent Loop Internals
- Messaging Gateway (User Guide)