---
layout: docs
title: "افزودن تطبیق‌دهنده‌های پلتفرم"
permalink: /docs/developer-guide/adding-platform-adapters/
---

- 
- Developer Guide
- Extending
- Adding a Platform Adapter

# Adding a Platform Adapter

This guide covers adding a new messaging platform to the Hermes gateway. A platform adapter connects Hermes to an external messaging service (Telegram, Discord, WeCom, etc.) so users can interact with the agent through that service.

There are two ways to add a platform:

- Plugin(recommended for community/third-party): Drop a plugin directory into~/.hermes/plugins/— zero core code changes needed. SeePlugin Pathbelow.
- Built-in: Modify 20+ files across code, config, and docs. Use theBuilt-in Checklistbelow.

`~/.hermes/plugins/`

## Architecture Overview​

```
User ↔ Messaging Platform ↔ Platform Adapter ↔ Gateway Runner ↔ AIAgent
```

Every adapter extendsBasePlatformAdapterfromgateway/platforms/base.pyand implements:

`BasePlatformAdapter`
`gateway/platforms/base.py`
- connect()— Establish connection (WebSocket, long-poll, HTTP server, etc.)(abstract)
- disconnect()— Clean shutdown(abstract)
- send()— Send a text message to a chat(abstract)
- send_typing()— Show typing indicator (optional override)
- get_chat_info()— Return chat metadata (optional override)

`connect()`
`disconnect()`
`send()`
`send_typing()`
`get_chat_info()`

Inbound messages are received by the adapter and forwarded viaself.handle_message(event), which the base class routes to the gateway runner.

`self.handle_message(event)`

## Plugin Path (Recommended)​

The plugin system lets you add a platform adapter without modifying any core Hermes code. Your plugin is a directory with two files:

```
~/.hermes/plugins/my-platform/  plugin.yaml      # Plugin metadata  adapter.py       # Adapter class + register() entry point
```

### plugin.yaml​

Plugin metadata. Therequires_envandoptional_envblocks auto-populatehermes configUI entries (seeSurfacing Env Varsbelow).

`requires_env`
`optional_env`
`hermes config`

```
name: my-platformlabel: My Platformkind: platformversion: 1.0.0description: My custom messaging platform adapterauthor: Your Namerequires_env:  - MY_PLATFORM_TOKEN          # bare string works  - name: MY_PLATFORM_CHANNEL  # or rich dict for better UX    description: "Channel to join"    prompt: "Channel"    password: falseoptional_env:  - name: MY_PLATFORM_HOME_CHANNEL    description: "Default channel for cron delivery"    password: false
```

### adapter.py​

```
import osfrom gateway.platforms.base import (    BasePlatformAdapter, SendResult, MessageEvent, MessageType,)from gateway.config import Platform, PlatformConfigclass MyPlatformAdapter(BasePlatformAdapter):    def __init__(self, config: PlatformConfig):        super().__init__(config, Platform("my_platform"))        extra = config.extra or {}        self.token = os.getenv("MY_PLATFORM_TOKEN") or extra.get("token", "")    async def connect(self) -> bool:        # Connect to the platform API, start listeners        self._mark_connected()        return True    async def disconnect(self) -> None:        self._mark_disconnected()    async def send(self, chat_id, content, reply_to=None, metadata=None):        # Send message via platform API        return SendResult(success=True, message_id="...")    async def get_chat_info(self, chat_id):        return {"name": chat_id, "type": "dm"}def check_requirements() -> bool:    return bool(os.getenv("MY_PLATFORM_TOKEN"))def validate_config(config) -> bool:    extra = getattr(config, "extra", {}) or {}    return bool(os.getenv("MY_PLATFORM_TOKEN") or extra.get("token"))def _env_enablement() -> dict | None:    token = os.getenv("MY_PLATFORM_TOKEN", "").strip()    channel = os.getenv("MY_PLATFORM_CHANNEL", "").strip()    if not (token and channel):        return None    seed = {"token": token, "channel": channel}    home = os.getenv("MY_PLATFORM_HOME_CHANNEL")    if home:        seed["home_channel"] = {"chat_id": home, "name": "Home"}    return seeddef register(ctx):    """Plugin entry point — called by the Hermes plugin system."""    ctx.register_platform(        name="my_platform",        label="My Platform",        adapter_factory=lambda cfg: MyPlatformAdapter(cfg),        check_fn=check_requirements,        validate_config=validate_config,        required_env=["MY_PLATFORM_TOKEN"],        install_hint="pip install my-platform-sdk",        # Env-driven auto-configuration — seeds PlatformConfig.extra from        # env vars before adapter construction. See "Env-Driven Auto-        # Configuration" section below.        env_enablement_fn=_env_enablement,        # Cron home-channel delivery support. Lets deliver=my_platform cron        # jobs route without editing cron/scheduler.py. See "Cron Delivery"        # section below.        cron_deliver_env_var="MY_PLATFORM_HOME_CHANNEL",        # Per-platform user authorization env vars        allowed_users_env="MY_PLATFORM_ALLOWED_USERS",        allow_all_env="MY_PLATFORM_ALLOW_ALL_USERS",        # Message length limit for smart chunking (0 = no limit)        max_message_length=4000,        # LLM guidance injected into system prompt        platform_hint=(            "You are chatting via My Platform. "            "It supports markdown formatting."        ),        # Display        emoji="💬",    )    # Optional: register platform-specific tools    ctx.register_tool(        name="my_platform_search",        toolset="my_platform",        schema={...},        handler=my_search_handler,    )
```

### Configuration​

Users configure the platform inconfig.yaml:

`config.yaml`

```
gateway:  platforms:    my_platform:      enabled: true      extra:        token: "..."        channel: "#general"
```

Or via environment variables (which the adapter reads in__init__).

`__init__`

### What the Plugin System Handles Automatically​

When you callctx.register_platform(), the following integration points are handled for you — no core code changes needed:

`ctx.register_platform()`
| Integration point | How it works |
| --- | --- |
| Gateway adapter creation | Registry checked before built-in if/elif chain |
| Config parsing | Platform._missing_()accepts any platform name |
| Connected platform validation | Registryvalidate_config()called |
| User authorization | allowed_users_env/allow_all_envchecked |
| Env-only auto-enable | env_enablement_fnseedsPlatformConfig.extra+home_channel |
| YAML config bridge | apply_yaml_config_fntranslatesconfig.yamlkeys into env vars / extras |
| Cron delivery | cron_deliver_env_varmakesdeliver=<name>work |
| hermes configUI entries | requires_env/optional_envinplugin.yamlauto-populate |
| send engine (tools/send_message_tool.py) | Routes through live gateway adapter |
| Webhook cross-platform delivery | Registry checked for known platforms |
| /updatecommand access | allow_update_commandflag |
| Channel directory | Plugin platforms included in enumeration |
| System prompt hints | platform_hintinjected into LLM context |
| Message chunking | max_message_lengthfor smart splitting |
| PII redaction | pii_safeflag |
| hermes status | Shows plugin platforms with(plugin)tag |
| hermes gateway setup | Plugin platforms appear in setup menu |
| hermes tools/hermes skills | Plugin platforms in per-platform config |
| Token lock (multi-profile) | Useacquire_scoped_lock()in yourconnect() |
| Orphaned config warning | Descriptive log when plugin is missing |

`Platform._missing_()`
`validate_config()`
`allowed_users_env`
`allow_all_env`
`env_enablement_fn`
`PlatformConfig.extra`
`home_channel`
`apply_yaml_config_fn`
`config.yaml`
`cron_deliver_env_var`
`deliver=<name>`
`hermes config`
`requires_env`
`optional_env`
`plugin.yaml`
`tools/send_message_tool.py`
`/update`
`allow_update_command`
`platform_hint`
`max_message_length`
`pii_safe`
`hermes status`
`(plugin)`
`hermes gateway setup`
`hermes tools`
`hermes skills`
`acquire_scoped_lock()`
`connect()`

## Env-Driven Auto-Configuration​

Most users set up a platform by dropping env vars into~/.hermes/.envrather than editingconfig.yaml. Theenv_enablement_fnhook lets your plugin pick those env vars upbeforethe adapter is constructed, sohermes gateway status,get_connected_platforms(), and cron delivery see the correct state without instantiating the platform SDK.

`~/.hermes/.env`
`config.yaml`
`env_enablement_fn`
`hermes gateway status`
`get_connected_platforms()`

```
def _env_enablement() -> dict | None:    """Seed PlatformConfig.extra from env vars.    Called by the platform registry during load_gateway_config().    Return None when the platform isn't minimally configured — the    caller then skips auto-enabling. Return a dict to seed extras.    The special 'home_channel' key is extracted and becomes a proper    HomeChannel dataclass on the PlatformConfig; every other key is    merged into PlatformConfig.extra.    """    token = os.getenv("MY_PLATFORM_TOKEN", "").strip()    channel = os.getenv("MY_PLATFORM_CHANNEL", "").strip()    if not (token and channel):        return None    seed = {"token": token, "channel": channel}    home = os.getenv("MY_PLATFORM_HOME_CHANNEL")    if home:        seed["home_channel"] = {            "chat_id": home,            "name": os.getenv("MY_PLATFORM_HOME_CHANNEL_NAME", "Home"),        }    return seeddef register(ctx):    ctx.register_platform(        name="my_platform",        label="My Platform",        adapter_factory=lambda cfg: MyPlatformAdapter(cfg),        check_fn=check_requirements,        validate_config=validate_config,        env_enablement_fn=_env_enablement,        # ... other fields    )
```

## YAML→env Config Bridge​

Some users prefer settingconfig.yamlkeys (my_platform.require_mention,my_platform.allowed_channels, etc.) over env vars. Theapply_yaml_config_fnhook lets your plugin own this translation instead of forcing coregateway/config.pyto know your platform's YAML schema.

`config.yaml`
`my_platform.require_mention`
`my_platform.allowed_channels`
`apply_yaml_config_fn`
`gateway/config.py`

```
import osdef _apply_yaml_config(yaml_cfg: dict, platform_cfg: dict) -> dict | None:    """Translate config.yaml `my_platform:` keys into env vars / extras.    yaml_cfg     — the full top-level parsed config.yaml dict    platform_cfg — the platform's own sub-dict (yaml_cfg.get("my_platform", {}))    May mutate os.environ directly (use `not os.getenv(...)` guards to    preserve env > YAML precedence) and/or return a dict to merge into    PlatformConfig.extra. Return None or {} for no extras.    """    if "require_mention" in platform_cfg and not os.getenv("MY_PLATFORM_REQUIRE_MENTION"):        os.environ["MY_PLATFORM_REQUIRE_MENTION"] = str(platform_cfg["require_mention"]).lower()    allowed = platform_cfg.get("allowed_channels")    if allowed is not None and not os.getenv("MY_PLATFORM_ALLOWED_CHANNELS"):        if isinstance(allowed, list):            allowed = ",".join(str(v) for v in allowed)        os.environ["MY_PLATFORM_ALLOWED_CHANNELS"] = str(allowed)    return None  # nothing extra to merge into PlatformConfig.extradef register(ctx):    ctx.register_platform(        name="my_platform",        ...,        apply_yaml_config_fn=_apply_yaml_config,    )
```

The hook is invoked duringload_gateway_config()after the generic shared-key loop (which handles common keys likeunauthorized_dm_behavior,notice_delivery,reply_prefix,require_mention, etc.) and before_apply_env_overrides(), so your plugin only needs to bridgeplatform-specifickeys.

`load_gateway_config()`
`unauthorized_dm_behavior`
`notice_delivery`
`reply_prefix`
`require_mention`
`_apply_env_overrides()`

Exceptions raised by the hook are swallowed and logged at debug level — a misbehaving plugin never aborts gateway config load.

## Cron Delivery​

To letdeliver=my_platformcron jobs route to a configured home channel, setcron_deliver_env_varto the env var name that holds the default chat/room/channel ID:

`deliver=my_platform`
`cron_deliver_env_var`

```
ctx.register_platform(    name="my_platform",    ...    cron_deliver_env_var="MY_PLATFORM_HOME_CHANNEL",)
```

The scheduler reads this env var when resolving the home target fordeliver=my_platformjobs, and also treats the platform as a valid cron target in_KNOWN_DELIVERY_PLATFORMS-style checks. If yourenv_enablement_fnseeds ahome_channeldict (see above), that takes precedence —cron_deliver_env_varis the fallback for cron jobs that run before env seeding.

`deliver=my_platform`
`_KNOWN_DELIVERY_PLATFORMS`
`env_enablement_fn`
`home_channel`
`cron_deliver_env_var`

### Out-of-process cron delivery​

cron_deliver_env_varmakes your platform a recognizeddeliver=target. To make the actual send succeed when the cron job runs in a separate process from the gateway (i.e.,hermes cron runseparate fromhermes gateway), register astandalone_sender_fn:

`cron_deliver_env_var`
`deliver=`
`hermes cron run`
`hermes gateway`
`standalone_sender_fn`

```
async def _standalone_send(    pconfig,    chat_id,    message,    *,    thread_id=None,    media_files=None,    force_document=False,):    """Open an ephemeral connection / acquire a fresh token, send, and close."""    # ... open connection, send message, return result ...    return {"success": True, "message_id": "..."}    # or {"error": "..."}ctx.register_platform(    name="my_platform",    ...    cron_deliver_env_var="MY_PLATFORM_HOME_CHANNEL",    standalone_sender_fn=_standalone_send,)
```

Why this hook is necessary: built-in platforms (Telegram, Discord, Slack, etc.) ship direct REST helpers intools/send_message_tool.pyso cron can deliver without holding the gateway in the same process. Plugin platforms historically depended on_gateway_runner_ref(), which returnsNoneoutside the gateway process, so withoutstandalone_sender_fnthe cron-side send fails withNo live adapter for platform '<name>'.

`tools/send_message_tool.py`
`_gateway_runner_ref()`
`None`
`standalone_sender_fn`
`No live adapter for platform '<name>'`

The function receives the samepconfigandchat_idthat the live adapter would, plus optionalthread_id,media_files, andforce_documentkeyword arguments. Returning{"success": True, "message_id": ...}is treated as a successful delivery; returning{"error": "..."}surfaces the message in cron'sdelivery_errors. Exceptions raised inside the function are caught by the dispatcher and reported asPlugin standalone send failed: <reason>. Reference implementations live inplugins/platforms/{irc,teams,google_chat}/adapter.py.

`pconfig`
`chat_id`
`thread_id`
`media_files`
`force_document`
`{"success": True, "message_id": ...}`
`{"error": "..."}`
`delivery_errors`
`Plugin standalone send failed: <reason>`
`plugins/platforms/{irc,teams,google_chat}/adapter.py`

## Surfacing Env Vars inhermes config​

`hermes config`

hermes_cli/config.pyscansplugins/platforms/*/plugin.yamlat import time and auto-populatesOPTIONAL_ENV_VARSfromrequires_envand (optional)optional_envblocks. Use the rich-dict form to contribute proper descriptions, prompts, password flags, and URLs — the CLI setup UI picks them up for free.

`hermes_cli/config.py`
`plugins/platforms/*/plugin.yaml`
`OPTIONAL_ENV_VARS`
`requires_env`
`optional_env`

```
# plugins/platforms/my_platform/plugin.yamlname: my_platform-platformlabel: My Platformkind: platformversion: 1.0.0description: >  My Platform gateway adapter for Hermes Agent.author: Your Namerequires_env:  - name: MY_PLATFORM_TOKEN    description: "Bot API token from the My Platform console"    prompt: "My Platform bot token"    url: "https://my-platform.example.com/bots"    password: true  - name: MY_PLATFORM_CHANNEL    description: "Channel to join (e.g. #hermes)"    prompt: "Channel"    password: falseoptional_env:  - name: MY_PLATFORM_HOME_CHANNEL    description: "Default channel for cron delivery (defaults to MY_PLATFORM_CHANNEL)"    prompt: "Home channel (or empty)"    password: false  - name: MY_PLATFORM_ALLOWED_USERS    description: "Comma-separated user IDs allowed to talk to the bot"    prompt: "Allowed users (comma-separated)"    password: false
```

Supported dict keys:name(required),description,prompt,url,password(bool; auto-detected from*_TOKEN/*_SECRET/*_KEY/*_PASSWORD/*_JSONsuffix when omitted),category(defaults to"messaging").

`name`
`description`
`prompt`
`url`
`password`
`*_TOKEN`
`*_SECRET`
`*_KEY`
`*_PASSWORD`
`*_JSON`
`category`
`"messaging"`

Bare-string entries (- MY_PLATFORM_TOKEN) still work — they get a generic description auto-derived from the plugin'slabel. If a hardcoded entry for the same var already exists inOPTIONAL_ENV_VARS, it wins (back-compat); the plugin.yaml form acts as the fallback.

`- MY_PLATFORM_TOKEN`
`label`
`OPTIONAL_ENV_VARS`

## Platform-Specific Slow-LLM UX​

Some platforms have constraints that change how a slow LLM response should be presented:

- LINEissues a single-usereply tokenthat expires roughly 60 seconds after the inbound event. Replying with that token is free; falling back to the metered Push API is not. If the LLM hasn't finished by the deadline, the choice is "burn paid Push quota" or "do something cleverer with the reply token before it expires."
- WhatsAppmarks a session inactive after 24h, after which only template messages are accepted.
- SMShas no concept of typing indicators or progressive updates — long responses just look like the bot is offline.

These are real constraints the baseBasePlatformAdaptercan't anticipate. The plugin surface intentionally leaves the room for an adapter to layer platform-specific UX on top of the base typing loop without expanding the kwarg list.

`BasePlatformAdapter`

### Pattern: subclass_keep_typingto layer mid-flight UX​

`_keep_typing`

BasePlatformAdapter._keep_typingis the typing-indicator heartbeat — it runs as a background task while the LLM is generating, and is cancelled when the response is delivered. To layer a platform-specific behavior at a threshold (e.g. send a "still thinking" bubble at 45s), override_keep_typingin your adapter, schedule your own task alongsidesuper()._keep_typing(), and tear it down infinally:

`BasePlatformAdapter._keep_typing`
`_keep_typing`
`super()._keep_typing()`
`finally`

```
class LineAdapter(BasePlatformAdapter):    async def _keep_typing(self, chat_id: str, *args, **kwargs) -> None:        if self.slow_response_threshold <= 0:            await super()._keep_typing(chat_id, *args, **kwargs)            return        async def _fire_at_threshold() -> None:            try:                await asyncio.sleep(self.slow_response_threshold)            except asyncio.CancelledError:                raise            # Platform-specific work here — for LINE, send a Template            # Buttons "Get answer" bubble using the cached reply token            # so the user can fetch the cached response later via a            # fresh (free) reply token from the postback callback.            await self._send_slow_response_button(chat_id)        side_task = asyncio.create_task(_fire_at_threshold())        try:            await super()._keep_typing(chat_id, *args, **kwargs)        finally:            if not side_task.done():                side_task.cancel()                try:                    await side_task                except (asyncio.CancelledError, Exception):                    pass
```

Key points:

- Alwaysawait super()._keep_typing(...).The typing heartbeat is independently useful — don't replace it, layer on top of it.
- Tear down the side task infinally.When the LLM finishes (or/stopcancels the run), the gateway cancels the typing task. Your side task must observe that cancellation too, otherwise it lingers and may fire after the response was already delivered.
- Pair withinterrupt_session_activityto resolve any orphan UX state when the user issues/stop. For LINE, this means transitioning the postback cache entry fromPENDINGtoERRORso the persistent "Get answer" button delivers a "Run was interrupted" message instead of looping.

`await super()._keep_typing(...)`
`finally`
`/stop`
`interrupt_session_activity`
`/stop`
`PENDING`
`ERROR`

### Pattern: subclasssendto route through a cache instead of sending immediately​

`send`

If your slow-response UX caches the response for later retrieval (LINE's postback flow), yoursendoverride needs to recognize three modes:

`send`
1. Pending postback active for this chat→ cache the response under the request_id, don't send anything visible.
2. System busy-ack(⚡ Interrupting,⏳ Queued,⏩ Steered) → bypass the cache and send visibly so the user sees the gateway's response to their input.
3. Normal response→ send via reply-token-or-push as usual.

`⚡ Interrupting`
`⏳ Queued`
`⏩ Steered`

```
async def send(self, chat_id: str, content: str, **kw) -> SendResult:    if _is_system_bypass(content):        return await self._send_text_chunks(chat_id, content, force_push=False)    pending_rid = self._pending_buttons.get(chat_id)    if pending_rid:        self._cache.set_ready(pending_rid, content)        return SendResult(success=True, message_id=pending_rid)    return await self._send_text_chunks(chat_id, content, force_push=False)
```

_SYSTEM_BYPASS_PREFIXESare the gateway's own busy-acknowledgment prefixes (⚡,⏳,⏩,💾). Always let those through visibly, regardless of cached UX state.

`_SYSTEM_BYPASS_PREFIXES`
`⚡`
`⏳`
`⏩`
`💾`

### When this pattern is appropriate​

Use the typing-loop override approach when:

- The platform's outbound API has a hard time-window constraint (single-use reply token, expiring sticky session, etc.) AND
- Avisible mid-flight bubbleis acceptable UX on that platform.

Use the simplerslow_response_threshold = 0always-Push path when:

`slow_response_threshold = 0`
- The platform doesn't have a meaningful free vs. paid distinction, OR
- The user community prefers "loading… loading… DONE" silence-then-response over an interactive intermediate bubble.

LINE supports both: the threshold defaults to 45s for free postback fetch, andLINE_SLOW_RESPONSE_THRESHOLD=0reverts to "always Push fallback."

`LINE_SLOW_RESPONSE_THRESHOLD=0`

### Reference Implementation​

Seeplugins/platforms/line/adapter.pyfor the full LINE postback implementation — aRequestCachestate machine (PENDING → READY → DELIVERED, plusERRORfor/stop), a_keep_typingoverride that fires the Template Buttons bubble at threshold, asendoverride that routes through the cache, and aninterrupt_session_activityoverride that resolves orphan PENDING entries.

`plugins/platforms/line/adapter.py`
`RequestCache`
`PENDING → READY → DELIVERED`
`ERROR`
`/stop`
`_keep_typing`
`send`
`interrupt_session_activity`

### Reference Implementations (Plugin Path)​

Seeplugins/platforms/irc/in the repo for a complete working example — a full async IRC adapter with zero external dependencies.plugins/platforms/teams/covers Bot Framework / Adaptive Cards,plugins/platforms/google_chat/covers OAuth-based REST APIs, andplugins/platforms/line/covers webhook-driven Messaging APIs with platform-specific slow-LLM UX.

`plugins/platforms/irc/`
`plugins/platforms/teams/`
`plugins/platforms/google_chat/`
`plugins/platforms/line/`

## Step-by-Step Checklist (Built-in Path)​

This checklist is for adding a platform directly to the Hermes core codebase — typically done by core contributors for officially supported platforms. Community/third-party platforms should use thePlugin Pathabove.

### 1. Platform Enum​

Add your platform to thePlatformenum ingateway/config.py:

`Platform`
`gateway/config.py`

```
class Platform(str, Enum):    # ... existing platforms ...    NEWPLAT = "newplat"
```

### 2. Adapter File​

Createplugins/platforms/newplat/adapter.py:

`plugins/platforms/newplat/adapter.py`

```
from gateway.config import Platform, PlatformConfigfrom gateway.platforms.base import (    BasePlatformAdapter, MessageEvent, MessageType, SendResult,)def check_newplat_requirements() -> bool:    """Return True if dependencies are available."""    return SOME_SDK_AVAILABLEclass NewPlatAdapter(BasePlatformAdapter):    def __init__(self, config: PlatformConfig):        super().__init__(config, Platform.NEWPLAT)        # Read config from config.extra dict        extra = config.extra or {}        self._api_key = extra.get("api_key") or os.getenv("NEWPLAT_API_KEY", "")    async def connect(self) -> bool:        # Set up connection, start polling/webhook        self._mark_connected()        return True    async def disconnect(self) -> None:        self._running = False        self._mark_disconnected()    async def send(self, chat_id, content, reply_to=None, metadata=None):        # Send message via platform API        return SendResult(success=True, message_id="...")    async def get_chat_info(self, chat_id):        return {"name": chat_id, "type": "dm"}
```

For inbound messages, build aMessageEventand callself.handle_message(event):

`MessageEvent`
`self.handle_message(event)`

```
source = self.build_source(    chat_id=chat_id,    chat_name=name,    chat_type="dm",  # or "group"    user_id=user_id,    user_name=user_name,)event = MessageEvent(    text=content,    message_type=MessageType.TEXT,    source=source,    message_id=msg_id,)await self.handle_message(event)
```

### 3. Gateway Config (gateway/config.py)​

`gateway/config.py`

Three touchpoints:

1. get_connected_platforms()— Add a check for your platform's required credentials
2. load_gateway_config()— Add token env map entry:Platform.NEWPLAT: "NEWPLAT_TOKEN"
3. _apply_env_overrides()— Map allNEWPLAT_*env vars to config

`get_connected_platforms()`
`load_gateway_config()`
`Platform.NEWPLAT: "NEWPLAT_TOKEN"`
`_apply_env_overrides()`
`NEWPLAT_*`

### 4. Gateway Runner (gateway/run.py)​

`gateway/run.py`

Five touchpoints:

1. _create_adapter()— Add anelif platform == Platform.NEWPLAT:branch
2. _is_user_authorized()allowed_users map—Platform.NEWPLAT: "NEWPLAT_ALLOWED_USERS"
3. _is_user_authorized()allow_all map—Platform.NEWPLAT: "NEWPLAT_ALLOW_ALL_USERS"
4. Early env check_any_allowlisttuple— Add"NEWPLAT_ALLOWED_USERS"
5. Early env check_allow_alltuple— Add"NEWPLAT_ALLOW_ALL_USERS"
6. _UPDATE_ALLOWED_PLATFORMSfrozenset— AddPlatform.NEWPLAT

`_create_adapter()`
`elif platform == Platform.NEWPLAT:`
`_is_user_authorized()`
`Platform.NEWPLAT: "NEWPLAT_ALLOWED_USERS"`
`_is_user_authorized()`
`Platform.NEWPLAT: "NEWPLAT_ALLOW_ALL_USERS"`
`_any_allowlist`
`"NEWPLAT_ALLOWED_USERS"`
`_allow_all`
`"NEWPLAT_ALLOW_ALL_USERS"`
`_UPDATE_ALLOWED_PLATFORMS`
`Platform.NEWPLAT`

### 5. Cross-Platform Delivery​

1. gateway/platforms/webhook.py— Add"newplat"to the delivery type tuple
2. cron/scheduler.py— Add to_KNOWN_DELIVERY_PLATFORMSfrozenset and_deliver_result()platform map

`gateway/platforms/webhook.py`
`"newplat"`
`cron/scheduler.py`
`_KNOWN_DELIVERY_PLATFORMS`
`_deliver_result()`

### 6. CLI Integration​

1. hermes_cli/config.py— Add allNEWPLAT_*vars to_EXTRA_ENV_KEYS
2. hermes_cli/gateway.py— Add entry to_PLATFORMSlist with key, label, emoji, token_var, setup_instructions, and vars
3. hermes_cli/platforms.py— AddPlatformInfoentry with label and default_toolset (used byskills_configandtools_configTUIs)
4. hermes_cli/setup.py— Add_setup_newplat()function (can delegate togateway.py) and add tuple to the messaging platforms list
5. hermes_cli/status.py— Add platform detection entry:"NewPlat": ("NEWPLAT_TOKEN", "NEWPLAT_HOME_CHANNEL")
6. hermes_cli/dump.py— Add"newplat": "NEWPLAT_TOKEN"to platform detection dict

`hermes_cli/config.py`
`NEWPLAT_*`
`_EXTRA_ENV_KEYS`
`hermes_cli/gateway.py`
`_PLATFORMS`
`hermes_cli/platforms.py`
`PlatformInfo`
`skills_config`
`tools_config`
`hermes_cli/setup.py`
`_setup_newplat()`
`gateway.py`
`hermes_cli/status.py`
`"NewPlat": ("NEWPLAT_TOKEN", "NEWPLAT_HOME_CHANNEL")`
`hermes_cli/dump.py`
`"newplat": "NEWPLAT_TOKEN"`

### 7. Tools​

1. tools/send_message_tool.py— Add"newplat": Platform.NEWPLATto platform map
2. tools/cronjob_tools.py— Addnewplatto the delivery target description string

`tools/send_message_tool.py`
`"newplat": Platform.NEWPLAT`
`tools/cronjob_tools.py`
`newplat`

### 8. Toolsets​

1. toolsets.py— Add"hermes-newplat"toolset definition with_HERMES_CORE_TOOLS
2. toolsets.py— Add"hermes-newplat"to the"hermes-gateway"includes list

`toolsets.py`
`"hermes-newplat"`
`_HERMES_CORE_TOOLS`
`toolsets.py`
`"hermes-newplat"`
`"hermes-gateway"`

### 9. Optional: Platform Hints​

agent/prompt_builder.py— If your platform has specific rendering limitations (no markdown, message length limits, etc.), add an entry to the_PLATFORM_HINTSdict. This injects platform-specific guidance into the system prompt:

`agent/prompt_builder.py`
`_PLATFORM_HINTS`

```
_PLATFORM_HINTS = {    # ...    "newplat": (        "You are chatting via NewPlat. It supports markdown formatting "        "but has a 4000-character message limit."    ),}
```

Not all platforms need hints — only add one if the agent's behavior should differ.

### 10. Tests​

Createtests/gateway/test_newplat.pycovering:

`tests/gateway/test_newplat.py`
- Adapter construction from config
- Message event building
- Send method (mock the external API)
- Platform-specific features (encryption, routing, etc.)

### 11. Documentation​

| File | What to add |
| --- | --- |
| website/docs/user-guide/messaging/newplat.md | Full platform setup page |
| website/docs/user-guide/messaging/index.md | Platform comparison table, architecture diagram, toolsets table, security section, next-steps link |
| website/docs/reference/environment-variables.md | All NEWPLAT_* env vars |
| website/docs/reference/toolsets-reference.md | hermes-newplat toolset |
| website/docs/integrations/index.md | Platform link |
| website/sidebars.ts | Sidebar entry for the docs page |
| website/docs/developer-guide/architecture.md | Adapter count + listing |
| website/docs/developer-guide/gateway-internals.md | Adapter file listing |

`website/docs/user-guide/messaging/newplat.md`
`website/docs/user-guide/messaging/index.md`
`website/docs/reference/environment-variables.md`
`website/docs/reference/toolsets-reference.md`
`website/docs/integrations/index.md`
`website/sidebars.ts`
`website/docs/developer-guide/architecture.md`
`website/docs/developer-guide/gateway-internals.md`

## Parity Audit​

Before marking a new platform PR as complete, run a parity audit against an established platform:

```
# Find every .py file mentioning the reference platformsearch_files "bluebubbles" output_mode="files_only" file_glob="*.py"# Find every .py file mentioning the new platformsearch_files "newplat" output_mode="files_only" file_glob="*.py"# Any file in the first set but not the second is a potential gap
```

Repeat for.mdand.tsfiles. Investigate each gap — is it a platform enumeration (needs updating) or a platform-specific reference (skip)?

`.md`
`.ts`

## Common Patterns​

### Long-Poll Adapters​

If your adapter uses long-polling (like Telegram or Weixin), use a polling loop task:

```
async def connect(self):    self._poll_task = asyncio.create_task(self._poll_loop())    self._mark_connected()async def _poll_loop(self):    while self._running:        messages = await self._fetch_updates()        for msg in messages:            await self.handle_message(self._build_event(msg))
```

### Callback/Webhook Adapters​

If the platform pushes messages to your endpoint (like WeCom Callback), run an HTTP server:

```
async def connect(self):    self._app = web.Application()    self._app.router.add_post("/callback", self._handle_callback)    # ... start aiohttp server    self._mark_connected()async def _handle_callback(self, request):    event = self._build_event(await request.text())    await self._message_queue.put(event)    return web.Response(text="success")  # Acknowledge immediately
```

For platforms with tight response deadlines (e.g., WeCom's 5-second limit), always acknowledge immediately and deliver the agent's reply proactively via API later. Agent sessions run 3–30 minutes — inline replies within a callback response window are not feasible.

### Token Locks​

If the adapter holds a persistent connection with a unique credential, add a scoped lock to prevent two profiles from using the same credential:

```
from gateway.status import acquire_scoped_lock, release_scoped_lockasync def connect(self):    if not acquire_scoped_lock("newplat", self._token):        logger.error("Token already in use by another profile")        return False    # ... connectasync def disconnect(self):    release_scoped_lock("newplat", self._token)
```

## Reference Implementations​

| Adapter | Pattern | Complexity | Good reference for |
| --- | --- | --- | --- |
| bluebubbles.py | REST + webhook | Medium | Simple REST API integration |
| weixin.py | Long-poll + CDN | High | Media handling, encryption |
| wecom_callback.py | Callback/webhook | Medium | HTTP server, AES crypto, multi-app |
| plugins/platforms/irc/adapter.py | Long-poll + IRC protocol | High | Full-featured plugin adapter with scoped token lock |

`bluebubbles.py`
`weixin.py`
`wecom_callback.py`
`plugins/platforms/irc/adapter.py`