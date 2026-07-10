- 
- Features
- Automation
- Event Hooks

# Event Hooks

Hermes has three hook systems that run custom code at key lifecycle points:

| System | Registered via | Runs in | Use case |
| --- | --- | --- | --- |
| Gateway hooks | HOOK.yaml+handler.pyin~/.hermes/hooks/ | Gateway only | Logging, alerts, webhooks |
| Plugin hooks | ctx.register_hook()in aplugin | CLI + Gateway | Tool interception, metrics, guardrails |
| Shell hooks | hooks:block in~/.hermes/config.yamlpointing at shell scripts | CLI + Gateway | Drop-in scripts for blocking, auto-formatting, context injection |

`HOOK.yaml`
`handler.py`
`~/.hermes/hooks/`
`ctx.register_hook()`
`hooks:`
`~/.hermes/config.yaml`

All three systems are non-blocking — errors in any hook are caught and logged, never crashing the agent.

## Gateway Event Hooks​

Gateway hooks fire automatically during gateway operation (Telegram, Discord, Slack, WhatsApp, Teams) without blocking the main agent pipeline.

### Creating a Hook​

Each hook is a directory under~/.hermes/hooks/containing two files:

`~/.hermes/hooks/`

```
~/.hermes/hooks/└── my-hook/    ├── HOOK.yaml      # Declares which events to listen for    └── handler.py     # Python handler function
```

#### HOOK.yaml​

```
name: my-hookdescription: Log all agent activity to a fileevents:  - agent:start  - agent:end  - agent:step
```

Theeventslist determines which events trigger your handler. You can subscribe to any combination of events, including wildcards likecommand:*.

`events`
`command:*`

#### handler.py​

```
import jsonfrom datetime import datetimefrom pathlib import PathLOG_FILE = Path.home() / ".hermes" / "hooks" / "my-hook" / "activity.log"async def handle(event_type: str, context: dict):    """Called for each subscribed event. Must be named 'handle'."""    entry = {        "timestamp": datetime.now().isoformat(),        "event": event_type,        **context,    }    with open(LOG_FILE, "a") as f:        f.write(json.dumps(entry) + "\n")
```

Handler rules:

- Must be namedhandle
- Receivesevent_type(string) andcontext(dict)
- Can beasync defor regulardef— both work
- Errors are caught and logged, never crashing the agent

`handle`
`event_type`
`context`
`async def`
`def`

### Available Events​

| Event | When it fires | Context keys |
| --- | --- | --- |
| gateway:startup | Gateway process starts | platforms(list of active platform names) |
| session:start | New messaging session created | platform,user_id,session_id,session_key |
| session:end | Session ended (before reset) | platform,user_id,session_key |
| session:reset | User ran/newor/reset | platform,user_id,session_key |
| agent:start | Agent begins processing a message | platform,user_id,session_id,message |
| agent:step | Each iteration of the tool-calling loop | platform,user_id,session_id,iteration,tool_names |
| agent:end | Agent finishes processing | platform,user_id,session_id,message,response |
| command:* | Any slash command executed | platform,user_id,command,args |

`gateway:startup`
`platforms`
`session:start`
`platform`
`user_id`
`session_id`
`session_key`
`session:end`
`platform`
`user_id`
`session_key`
`session:reset`
`/new`
`/reset`
`platform`
`user_id`
`session_key`
`agent:start`
`platform`
`user_id`
`session_id`
`message`
`agent:step`
`platform`
`user_id`
`session_id`
`iteration`
`tool_names`
`agent:end`
`platform`
`user_id`
`session_id`
`message`
`response`
`command:*`
`platform`
`user_id`
`command`
`args`

#### Wildcard Matching​

Handlers registered forcommand:*fire for anycommand:event (command:model,command:reset, etc.). Monitor all slash commands with a single subscription.

`command:*`
`command:`
`command:model`
`command:reset`

### Examples​

#### Telegram Alert on Long Tasks​

Send yourself a message when the agent takes more than 10 steps:

```
# ~/.hermes/hooks/long-task-alert/HOOK.yamlname: long-task-alertdescription: Alert when agent is taking many stepsevents:  - agent:step
```

```
# ~/.hermes/hooks/long-task-alert/handler.pyimport osimport httpxTHRESHOLD = 10BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")CHAT_ID = os.getenv("TELEGRAM_HOME_CHANNEL")async def handle(event_type: str, context: dict):    iteration = context.get("iteration", 0)    if iteration == THRESHOLD and BOT_TOKEN and CHAT_ID:        tools = ", ".join(context.get("tool_names", []))        text = f"⚠️ Agent has been running for {iteration} steps. Last tools: {tools}"        async with httpx.AsyncClient() as client:            await client.post(                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",                json={"chat_id": CHAT_ID, "text": text},            )
```

#### Command Usage Logger​

Track which slash commands are used:

```
# ~/.hermes/hooks/command-logger/HOOK.yamlname: command-loggerdescription: Log slash command usageevents:  - command:*
```

```
# ~/.hermes/hooks/command-logger/handler.pyimport jsonfrom datetime import datetimefrom pathlib import PathLOG = Path.home() / ".hermes" / "logs" / "command_usage.jsonl"def handle(event_type: str, context: dict):    LOG.parent.mkdir(parents=True, exist_ok=True)    entry = {        "ts": datetime.now().isoformat(),        "command": context.get("command"),        "args": context.get("args"),        "platform": context.get("platform"),        "user": context.get("user_id"),    }    with open(LOG, "a") as f:        f.write(json.dumps(entry) + "\n")
```

#### Session Start Webhook​

POST to an external service on new sessions:

```
# ~/.hermes/hooks/session-webhook/HOOK.yamlname: session-webhookdescription: Notify external service on new sessionsevents:  - session:start  - session:reset
```

```
# ~/.hermes/hooks/session-webhook/handler.pyimport httpxWEBHOOK_URL = "https://your-service.example.com/hermes-events"async def handle(event_type: str, context: dict):    async with httpx.AsyncClient() as client:        await client.post(WEBHOOK_URL, json={            "event": event_type,            **context,        }, timeout=5)
```

### Tutorial: BOOT.md — Run a Startup Checklist on Every Gateway Boot​

A popular pattern from the community: drop a Markdown checklist at~/.hermes/BOOT.md, and have the agent run it once every time the gateway starts. Useful for "on every boot, check overnight cron failures and ping me on Discord if anything failed," or "summarize the last 24h of deploy.log and post it to Slack #ops."

`~/.hermes/BOOT.md`

This tutorial shows how to build it yourself as a user-defined hook. Hermes does not ship a built-in BOOT.md hook — you wire up exactly the behavior you want.

#### What we're building​

1. A file at~/.hermes/BOOT.mdwith natural-language startup instructions.
2. A gateway hook that fires ongateway:startup, spawns a one-shot agent with your gateway's resolved model/credentials, and runs the BOOT.md instructions.
3. A[SILENT]convention so the agent can opt out of sending a message when there's nothing to report.

`~/.hermes/BOOT.md`
`gateway:startup`
`[SILENT]`

#### Step 1: Write your checklist​

Create~/.hermes/BOOT.md. Write it as if you were giving instructions to a human assistant:

`~/.hermes/BOOT.md`

```
# Startup Checklist1. Run `hermes cron list` and check if any scheduled jobs failed overnight.2. If any failed, summarize them for Discord #ops (the hook delivers your final response to its configured target).3. Check if `/opt/app/deploy.log` has any ERROR lines from the last 24 hours. If yes, summarize them and include in the same report.4. If nothing went wrong, reply with only `[SILENT]` so no message is sent.
```

The agent sees this as part of its prompt, so anything you can describe in plain language works — tool calls, shell commands, sending messages, summarizing files.

#### Step 2: Create the hook​

```
~/.hermes/hooks/boot-md/├── HOOK.yaml└── handler.py
```

~/.hermes/hooks/boot-md/HOOK.yaml

`~/.hermes/hooks/boot-md/HOOK.yaml`

```
name: boot-mddescription: Run ~/.hermes/BOOT.md on gateway startupevents:  - gateway:startup
```

~/.hermes/hooks/boot-md/handler.py

`~/.hermes/hooks/boot-md/handler.py`

```
"""Run ~/.hermes/BOOT.md on every gateway startup."""import loggingimport threadingfrom pathlib import Pathlogger = logging.getLogger("hooks.boot-md")BOOT_FILE = Path.home() / ".hermes" / "BOOT.md"def _build_prompt(content: str) -> str:    return (        "You are running a startup boot checklist. Follow the instructions "        "below exactly.\n\n"        "---\n"        f"{content}\n"        "---\n\n"        "Execute each instruction. Put any user-facing summary in your "        "final response — the hook delivers it to the configured channel "        "(e.g. Discord or Slack); you do not send messages yourself.\n"        "If nothing needs attention and there is nothing to report, reply "        "with ONLY: [SILENT]"    )def _run_boot_agent(content: str) -> None:    """Spawn a one-shot agent and execute the checklist.    Uses the gateway's resolved model and runtime credentials so this works    against custom endpoints, aggregators, and OAuth-based providers alike.    """    try:        from gateway.run import _resolve_gateway_model, _resolve_runtime_agent_kwargs        from run_agent import AIAgent        agent = AIAgent(            model=_resolve_gateway_model(),            **_resolve_runtime_agent_kwargs(),            platform="gateway",            quiet_mode=True,            skip_context_files=True,            skip_memory=True,            max_iterations=20,        )        result = agent.run_conversation(_build_prompt(content))        response = (result.get("final_response", "") or "").strip()        if response.upper() not in {"[SILENT]", "SILENT", "NO_REPLY", "NO REPLY"}:            logger.info("boot-md completed: %s", response[:200])        else:            logger.info("boot-md completed (nothing to report)")    except Exception as e:        logger.error("boot-md agent failed: %s", e)async def handle(event_type: str, context: dict) -> None:    if not BOOT_FILE.exists():        return    content = BOOT_FILE.read_text(encoding="utf-8").strip()    if not content:        return    logger.info("Running BOOT.md (%d chars)", len(content))    # Background thread so gateway startup isn't blocked on a full agent turn.    thread = threading.Thread(        target=_run_boot_agent,        args=(content,),        name="boot-md",        daemon=True,    )    thread.start()
```

The two key lines:

- _resolve_gateway_model()reads the gateway's currently-configured model.
- _resolve_runtime_agent_kwargs()resolves provider credentials the same way a normal gateway turn does — including API keys, base URLs, OAuth tokens, and credential pools.

`_resolve_gateway_model()`
`_resolve_runtime_agent_kwargs()`

Without these, a bareAIAgent()falls back to built-in defaults and will 401 against any non-default endpoint.

`AIAgent()`

#### Step 3: Test it​

Restart the gateway:

```
hermes gateway restart
```

Watch the logs:

```
hermes logs --follow --level INFO | grep boot-md
```

You should seeRunning BOOT.md (N chars)followed by eitherboot-md completed: ...(summary of what the agent did) orboot-md completed (nothing to report)when the agent replied with an exact silence token such as[SILENT].

`Running BOOT.md (N chars)`
`boot-md completed: ...`
`boot-md completed (nothing to report)`
`[SILENT]`

Delete~/.hermes/BOOT.mdto disable the checklist — the hook stays loaded but silently skips when the file isn't there.

`~/.hermes/BOOT.md`

#### Extending the pattern​

- Schedule-aware checklists:key offdatetime.now().weekday()inside BOOT.md's instructions ("if it's Monday, also check the weekly deploy log"). The instructions are free-form text, so anything the agent can reason about is fair game.
- Multiple checklists:point the hook at a different file (STARTUP.md,MORNING.md, etc.) and register separate hook directories for each.
- Non-agent variant:if you don't need a full agent loop, skipAIAgententirely and have the handler post a fixed notification directly viahttpx. Cheaper, faster, and has no provider dependency.

`datetime.now().weekday()`
`STARTUP.md`
`MORNING.md`
`AIAgent`
`httpx`

#### Why this isn't a built-in​

An earlier version of Hermes shipped this as a built-in hook and silently spawned an agent with bare defaults on every gateway boot. That surprised users with custom endpoints and made the feature invisible to users who didn't know it was running. Keeping it as a documented pattern — built by you, in your hooks directory — means you see exactly what it does and opt in by writing the files.

### How It Works​

1. On gateway startup,HookRegistry.discover_and_load()scans~/.hermes/hooks/
2. Each subdirectory withHOOK.yaml+handler.pyis loaded dynamically
3. Handlers are registered for their declared events
4. At each lifecycle point,hooks.emit()fires all matching handlers
5. Errors in any handler are caught and logged — a broken hook never crashes the agent

`HookRegistry.discover_and_load()`
`~/.hermes/hooks/`
`HOOK.yaml`
`handler.py`
`hooks.emit()`

Gateway hooks only fire in thegateway(Telegram, Discord, Slack, WhatsApp, Teams). The CLI does not load gateway hooks. For hooks that work everywhere, useplugin hooks.

## Plugin Hooks​

Pluginscan register hooks that fire inboth CLI and gatewaysessions. These are registered programmatically viactx.register_hook()in your plugin'sregister()function.

`ctx.register_hook()`
`register()`

For plugin packaging and registration details, see
thePlugins guide.

```
def register(ctx):    ctx.register_hook("pre_tool_call", my_tool_observer)    ctx.register_hook("post_tool_call", my_tool_logger)    ctx.register_hook("pre_llm_call", my_memory_callback)    ctx.register_hook("post_llm_call", my_sync_callback)    ctx.register_hook("on_session_start", my_init_callback)    ctx.register_hook("on_session_end", my_cleanup_callback)
```

General rules for all hooks:

- Callbacks receivekeyword arguments. Always accept**kwargsfor forward compatibility — new parameters may be added in future versions without breaking your plugin.
- If a callbackcrashes, it's logged and skipped. Other hooks and the agent continue normally. A misbehaving plugin can never break the agent.
- Two hooks' return values affect behavior:pre_tool_callcanblockthe tool, andpre_llm_callcaninject contextinto the LLM call. All other hooks are fire-and-forget observers.
- Observer callbacks receivetelemetry_schema_versionautomatically. When present,turn_id,api_request_id,task_id,session_id, andapi_call_countare separate correlation fields. Treatapi_request_idas an opaque identifier; do not parse its string format.

`**kwargs`
`pre_tool_call`
`pre_llm_call`
`telemetry_schema_version`
`turn_id`
`api_request_id`
`task_id`
`session_id`
`api_call_count`
`api_request_id`

### Quick reference​

| Hook | Fires when | Returns |
| --- | --- | --- |
| pre_tool_call | Before any tool executes | {"action": "block", "message": str}to veto the call |
| post_tool_call | After any tool returns | ignored |
| pre_llm_call | Once per turn, before the tool-calling loop | {"context": str}to prepend context to the user message |
| post_llm_call | Once per turn, after the tool-calling loop | ignored |
| pre_verify | Once per turn when the agent edited code, before it verifies/finishes | {"action": "continue", "message": str}to keep going |
| on_session_start | New session created (first turn only) | ignored |
| on_session_end | Session ends | ignored |
| on_session_finalize | CLI/gateway tears down an active session (flush, save, stats) | ignored |
| on_session_reset | Gateway swaps in a fresh session key (e.g./new,/reset) | ignored |
| subagent_start | Adelegate_taskchild has been constructed and is about to run | ignored |
| subagent_stop | Adelegate_taskchild has exited | ignored |
| pre_gateway_dispatch | Gateway received a user message, before auth + dispatch | {"action": "skip" | "rewrite" | "allow", ...}to influence flow |
| pre_approval_request | Dangerous command needs user approval, before the prompt/notification is sent | ignored |
| post_approval_response | User responded to an approval prompt (or it timed out) | ignored |
| transform_tool_result | After any tool returns, before the result is handed back to the model | strto replace the result,Noneto leave unchanged |
| transform_terminal_output | Inside theterminaltool, before truncation/ANSI-strip/redact | strto replace the raw output,Noneto leave unchanged |
| transform_llm_output | After the tool-calling loop completes, before the final response is delivered | strto replace the response text,None/empty to leave unchanged |

`pre_tool_call`
`{"action": "block", "message": str}`
`post_tool_call`
`pre_llm_call`
`{"context": str}`
`post_llm_call`
`pre_verify`
`{"action": "continue", "message": str}`
`on_session_start`
`on_session_end`
`on_session_finalize`
`on_session_reset`
`/new`
`/reset`
`subagent_start`
`delegate_task`
`subagent_stop`
`delegate_task`
`pre_gateway_dispatch`
`{"action": "skip" | "rewrite" | "allow", ...}`
`pre_approval_request`
`post_approval_response`
`transform_tool_result`
`str`
`None`
`transform_terminal_output`
`terminal`
`str`
`None`
`transform_llm_output`
`str`
`None`

### pre_tool_call​

`pre_tool_call`

Firesimmediately beforeevery tool execution — built-in tools and plugin tools alike.

Callback signature:

```
def my_callback(tool_name: str, args: dict, task_id: str, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| tool_name | str | Name of the tool about to execute (e.g."terminal","web_search","read_file") |
| args | dict | The arguments the model passed to the tool |
| task_id | str | Session/task identifier. Empty string if not set. |

`tool_name`
`str`
`"terminal"`
`"web_search"`
`"read_file"`
`args`
`dict`
`task_id`
`str`

Fires:Inmodel_tools.py, insidehandle_function_call(), before the tool's handler runs. Fires once per tool call — if the model calls 3 tools in parallel, this fires 3 times.

`model_tools.py`
`handle_function_call()`

Return value — veto the call:

```
return {"action": "block", "message": "Reason the tool call was blocked"}
```

The agent short-circuits the tool withmessageas the error returned to the model. The first matching block directive wins (Python plugins registered first, then shell hooks). Any other return value is ignored, so existing observer-only callbacks keep working unchanged.

`message`

Use cases:Logging, audit trails, tool call counters, blocking dangerous operations, rate limiting, per-user policy enforcement.

Example — tool call audit log:

```
import json, loggingfrom datetime import datetimelogger = logging.getLogger(__name__)def audit_tool_call(tool_name, args, task_id, **kwargs):    logger.info("TOOL_CALL session=%s tool=%s args=%s",                task_id, tool_name, json.dumps(args)[:200])def register(ctx):    ctx.register_hook("pre_tool_call", audit_tool_call)
```

Example — warn on dangerous tools:

```
DANGEROUS = {"terminal", "write_file", "patch"}def warn_dangerous(tool_name, **kwargs):    if tool_name in DANGEROUS:        print(f"⚠ Executing potentially dangerous tool: {tool_name}")def register(ctx):    ctx.register_hook("pre_tool_call", warn_dangerous)
```

### post_tool_call​

`post_tool_call`

Firesimmediately afterevery tool execution returns.

Callback signature:

```
def my_callback(tool_name: str, args: dict, result: str, task_id: str,                duration_ms: int, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| tool_name | str | Name of the tool that just executed |
| args | dict | The arguments the model passed to the tool |
| result | str | The tool's return value (always a JSON string) |
| task_id | str | Session/task identifier. Empty string if not set. |
| duration_ms | int | How long the tool's dispatch took, in milliseconds (measured withtime.monotonic()aroundregistry.dispatch()). |

`tool_name`
`str`
`args`
`dict`
`result`
`str`
`task_id`
`str`
`duration_ms`
`int`
`time.monotonic()`
`registry.dispatch()`

Fires:Inmodel_tools.py, insidehandle_function_call(), after the tool's handler returns. Fires once per tool call. Doesnotfire if the tool raised an unhandled exception (the error is caught and returned as an error JSON string instead, andpost_tool_callfires with that error string asresult).

`model_tools.py`
`handle_function_call()`
`post_tool_call`
`result`

Return value:Ignored.

Use cases:Logging tool results, metrics collection, tracking tool success/failure rates, latency dashboards, per-tool budget alerts, sending notifications when specific tools complete.

Example — track tool usage metrics:

```
from collections import Counter, defaultdictimport json_tool_counts = Counter()_error_counts = Counter()_latency_ms = defaultdict(list)def track_metrics(tool_name, result, duration_ms=0, **kwargs):    _tool_counts[tool_name] += 1    _latency_ms[tool_name].append(duration_ms)    try:        parsed = json.loads(result)        if "error" in parsed:            _error_counts[tool_name] += 1    except (json.JSONDecodeError, TypeError):        passdef register(ctx):    ctx.register_hook("post_tool_call", track_metrics)
```

### pre_llm_call​

`pre_llm_call`

Firesonce per turn, before the tool-calling loop begins. This is theonly hook whose return value is used— it can inject context into the current turn's user message.

Callback signature:

```
def my_callback(session_id: str, user_message: str, conversation_history: list,                is_first_turn: bool, model: str, platform: str, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| session_id | str | Unique identifier for the current session |
| user_message | str | The user's original message for this turn (before any skill injection) |
| conversation_history | list | Copy of the full message list (OpenAI format:[{"role": "user", "content": "..."}]) |
| is_first_turn | bool | Trueif this is the first turn of a new session,Falseon subsequent turns |
| model | str | The model identifier (e.g."anthropic/claude-sonnet-4.6") |
| platform | str | Where the session is running:"cli","telegram","discord", etc. |

`session_id`
`str`
`user_message`
`str`
`conversation_history`
`list`
`[{"role": "user", "content": "..."}]`
`is_first_turn`
`bool`
`True`
`False`
`model`
`str`
`"anthropic/claude-sonnet-4.6"`
`platform`
`str`
`"cli"`
`"telegram"`
`"discord"`

Fires:Inrun_agent.py, insiderun_conversation(), after context compression but before the mainwhileloop. Fires once perrun_conversation()call (i.e. once per user turn), not once per API call within the tool loop.

`run_agent.py`
`run_conversation()`
`while`
`run_conversation()`

Return value:If the callback returns a dict with a"context"key, or a plain non-empty string, the text is appended to the current turn's user message. ReturnNonefor no injection.

`"context"`
`None`

```
# Inject contextreturn {"context": "Recalled memories:\n- User likes Python\n- Working on hermes-agent"}# Plain string (equivalent)return "Recalled memories:\n- User likes Python"# No injectionreturn None
```

Where context is injected:Always theuser message, never the system prompt. This preserves the prompt cache — the system prompt stays identical across turns, so cached tokens are reused. The system prompt is Hermes's territory (model guidance, tool enforcement, personality, skills). Plugins contribute context alongside the user's input.

All injected context isephemeral— added at API call time only. The original user message in the conversation history is never mutated, and nothing is persisted to the session database.

Whenmultiple pluginsreturn context, their outputs are joined with double newlines in plugin discovery order (alphabetical by directory name).

Use cases:Memory recall, RAG context injection, guardrails, per-turn analytics.

Example — memory recall:

```
import httpxMEMORY_API = "https://your-memory-api.example.com"def recall(session_id, user_message, is_first_turn, **kwargs):    try:        resp = httpx.post(f"{MEMORY_API}/recall", json={            "session_id": session_id,            "query": user_message,        }, timeout=3)        memories = resp.json().get("results", [])        if not memories:            return None        text = "Recalled context:\n" + "\n".join(f"- {m['text']}" for m in memories)        return {"context": text}    except Exception:        return Nonedef register(ctx):    ctx.register_hook("pre_llm_call", recall)
```

Example — guardrails:

```
POLICY = "Never execute commands that delete files without explicit user confirmation."def guardrails(**kwargs):    return {"context": POLICY}def register(ctx):    ctx.register_hook("pre_llm_call", guardrails)
```

### post_llm_call​

`post_llm_call`

Firesonce per turn, after the tool-calling loop completes and the agent has produced a final response. Only fires onsuccessfulturns — does not fire if the turn was interrupted.

Callback signature:

```
def my_callback(session_id: str, user_message: str, assistant_response: str,                conversation_history: list, model: str, platform: str, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| session_id | str | Unique identifier for the current session |
| user_message | str | The user's original message for this turn |
| assistant_response | str | The agent's final text response for this turn |
| conversation_history | list | Copy of the full message list after the turn completed |
| model | str | The model identifier |
| platform | str | Where the session is running |

`session_id`
`str`
`user_message`
`str`
`assistant_response`
`str`
`conversation_history`
`list`
`model`
`str`
`platform`
`str`

Fires:Inrun_agent.py, insiderun_conversation(), after the tool loop exits with a final response. Guarded byif final_response and not interrupted— so it doesnotfire when the user interrupts mid-turn or the agent hits the iteration limit without producing a response.

`run_agent.py`
`run_conversation()`
`if final_response and not interrupted`

Return value:Ignored.

Use cases:Syncing conversation data to an external memory system, computing response quality metrics, logging turn summaries, triggering follow-up actions.

Example — sync to external memory:

```
import httpxMEMORY_API = "https://your-memory-api.example.com"def sync_memory(session_id, user_message, assistant_response, **kwargs):    try:        httpx.post(f"{MEMORY_API}/store", json={            "session_id": session_id,            "user": user_message,            "assistant": assistant_response,        }, timeout=5)    except Exception:        pass  # best-effortdef register(ctx):    ctx.register_hook("post_llm_call", sync_memory)
```

Example — track response lengths:

```
import logginglogger = logging.getLogger(__name__)def log_response_length(session_id, assistant_response, model, **kwargs):    logger.info("RESPONSE session=%s model=%s chars=%d",                session_id, model, len(assistant_response or ""))def register(ctx):    ctx.register_hook("post_llm_call", log_response_length)
```

### pre_verify​

`pre_verify`

Firesonce per turn when the agent edited code, just before it finishes (after the built-in verify-on-stop guard). This is a user/plugin policy gate: a callback can keep the agent going — run a check, defer it, tidy the diff — instead of letting it stop.

Hermes' shipped verification guidance is not a defaultpre_verifyhook. It is appended to the evidence-based verify-on-stop nudge when edited code lacks fresh verification evidence, so it does not create a second default continuation path. Setagent.verify_guidance: falseto keep that built-in evidence nudge terse.

`pre_verify`
`agent.verify_guidance: false`

Callback signature:

```
def my_callback(session_id: str, platform: str, model: str, coding: bool,                attempt: int, final_response: str, changed_paths: list, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| session_id | str | Unique identifier for the current session |
| platform | str | Where the session is running ("cli","telegram", …) |
| model | str | The model identifier |
| coding | bool | Whether the turn is in the coding posture (in a code workspace) — scope your hook on this |
| attempt | int | How many times this turn has already been nudged (0 on the first) — self-throttle on this |
| final_response | str | The answer the agent is about to deliver |
| changed_paths | list | Files the agent edited this turn (sorted, always non-empty here) |

`session_id`
`str`
`platform`
`str`
`"cli"`
`"telegram"`
`model`
`str`
`coding`
`bool`
`attempt`
`int`
`final_response`
`str`
`changed_paths`
`list`

Scope a hook to the coding context by checkingcodingand make it one-shot withattempt(shell hooks read both from.extra), the same way apre_tool_callhook scopes ontool_name— so you can register severalpre_verifyhooks, each firing only where it should.

`coding`
`attempt`
`.extra`
`pre_tool_call`
`tool_name`
`pre_verify`

Fires:Inagent/conversation_loop.py, at the point the agent would accept a final answer, immediately after the verify-on-stop check — but only when the agent edited code this turn and at least onepre_verifyhook is registered.

`agent/conversation_loop.py`
`pre_verify`

Return value — keep the agent going:

```
return {"action": "continue", "message": "Run the formatter on your changes, then finish."}
```

Themessageis appended as a synthetic user turn and the loop runs again. The Claude-Code Stop shape ({"decision": "block", "reason": "..."}, where blocking the stop meanskeep going) is accepted too. A directive with no message — or any other return — lets the turn finish.

`message`
`{"decision": "block", "reason": "..."}`

Bounded:consecutive continue directives in one turn are capped byagent.max_verify_nudges(default 3), so a hook that always says continue can never trap the loop. The attempted answer is kept in history but not surfaced to the user while the agent is being nudged.

`agent.max_verify_nudges`

Make it idempotent:the hook re-fires after each nudge, so gate onattempt(if attempt: return None) — otherwise it just nudges until the bound is hit.

`attempt`
`if attempt: return None`

Use cases:defer tests/lints during creative iteration, require green checks for certain paths, block "done" until a changelog entry exists, run a project-specific verification checklist.

Example — defer checks on creative UI work, scoped + one-shot:

```
UI = (".tsx", ".jsx", ".css", ".scss")def defer_ui_checks(coding, attempt, changed_paths, **kwargs):    if attempt or not coding:        return None  # one-shot, coding only    if not all(p.endswith(UI) for p in changed_paths):        return None  # only pure-UI edits    return {        "action": "continue",        "message": "This is UI work — don't run tests/lints yet; ask the user to "                   "eyeball it first, and clean the diff before any commit.",    }def register(ctx):    ctx.register_hook("pre_verify", defer_ui_checks)
```

For standing guidance that should shape the built-in missing-evidence nudge, useagent.verify_guidance. For broader coding posture rules that don't need togateverification, preferagent.coding_instructionsinconfig.yaml— it rides the coding brief and costs no extra turn.

`agent.verify_guidance`
`agent.coding_instructions`
`config.yaml`

### on_session_start​

`on_session_start`

Firesoncewhen a brand-new session is created. Doesnotfire on session continuation (when the user sends a second message in an existing session).

Callback signature:

```
def my_callback(session_id: str, model: str, platform: str, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| session_id | str | Unique identifier for the new session |
| model | str | The model identifier |
| platform | str | Where the session is running |

`session_id`
`str`
`model`
`str`
`platform`
`str`

Fires:Inrun_agent.py, insiderun_conversation(), during the first turn of a new session — specifically after the system prompt is built but before the tool loop starts. The check isif not conversation_history(no prior messages = new session).

`run_agent.py`
`run_conversation()`
`if not conversation_history`

Return value:Ignored.

Use cases:Initializing session-scoped state, warming caches, registering the session with an external service, logging session starts.

Example — initialize a session cache:

```
_session_caches = {}def init_session(session_id, model, platform, **kwargs):    _session_caches[session_id] = {        "model": model,        "platform": platform,        "tool_calls": 0,        "started": __import__("datetime").datetime.now().isoformat(),    }def register(ctx):    ctx.register_hook("on_session_start", init_session)
```

### on_session_end​

`on_session_end`

Fires at thevery endof everyrun_conversation()call, regardless of outcome. Also fires from the CLI's exit handler if the agent was mid-turn when the user quit.

`run_conversation()`

Callback signature:

```
def my_callback(session_id: str, completed: bool, interrupted: bool,                model: str, platform: str, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| session_id | str | Unique identifier for the session |
| completed | bool | Trueif the agent produced a final response,Falseotherwise |
| interrupted | bool | Trueif the turn was interrupted (user sent new message,/stop, or quit) |
| model | str | The model identifier |
| platform | str | Where the session is running |

`session_id`
`str`
`completed`
`bool`
`True`
`False`
`interrupted`
`bool`
`True`
`/stop`
`model`
`str`
`platform`
`str`

Fires:In two places:

1. run_agent.py— at the end of everyrun_conversation()call, after all cleanup. Always fires, even if the turn errored.
2. cli.py— in the CLI's atexit handler, butonlyif the agent was mid-turn (_agent_running=True) when the exit occurred. This catches Ctrl+C and/exitduring processing. In this case,completed=Falseandinterrupted=True.

`run_agent.py`
`run_conversation()`
`cli.py`
`_agent_running=True`
`/exit`
`completed=False`
`interrupted=True`

Return value:Ignored.

Use cases:Flushing buffers, closing connections, persisting session state, logging session duration, cleanup of resources initialized inon_session_start.

`on_session_start`

Example — flush and cleanup:

```
_session_caches = {}def cleanup_session(session_id, completed, interrupted, **kwargs):    cache = _session_caches.pop(session_id, None)    if cache:        # Flush accumulated data to disk or external service        status = "completed" if completed else ("interrupted" if interrupted else "failed")        print(f"Session {session_id} ended: {status}, {cache['tool_calls']} tool calls")def register(ctx):    ctx.register_hook("on_session_end", cleanup_session)
```

Example — session duration tracking:

```
import time, logginglogger = logging.getLogger(__name__)_start_times = {}def on_start(session_id, **kwargs):    _start_times[session_id] = time.time()def on_end(session_id, completed, interrupted, **kwargs):    start = _start_times.pop(session_id, None)    if start:        duration = time.time() - start        logger.info("SESSION_DURATION session=%s seconds=%.1f completed=%s interrupted=%s",                     session_id, duration, completed, interrupted)def register(ctx):    ctx.register_hook("on_session_start", on_start)    ctx.register_hook("on_session_end", on_end)
```

### on_session_finalize​

`on_session_finalize`

Fires when the CLI or gatewaytears downan active session — for example, when the user runs/new, the gateway GC'd an idle session, or the CLI quit with an active agent. This is the last chance to flush state tied to the outgoing session before its identity is gone.

`/new`

Callback signature:

```
def my_callback(session_id: str | None, platform: str, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| session_id | strorNone | The outgoing session ID. May beNoneif no active session existed. |
| platform | str | "cli"or the messaging platform name ("telegram","discord", etc.). |

`session_id`
`str`
`None`
`None`
`platform`
`str`
`"cli"`
`"telegram"`
`"discord"`

Fires:Incli.py(on/new/ CLI exit) andgateway/run.py(when a session is reset or GC'd). Always paired withon_session_reseton the gateway side.

`cli.py`
`/new`
`gateway/run.py`
`on_session_reset`

Return value:Ignored.

Use cases:Persist final session metrics before the session ID is discarded, close per-session resources, emit a final telemetry event, drain queued writes.

### on_session_reset​

`on_session_reset`

Fires when the gatewayswaps in a new session keyfor an active chat — the user invoked/new,/reset,/clear, or the adapter picked a fresh session after an idle window. This lets plugins react to the fact that conversation state has been wiped without waiting for the nexton_session_start.

`/new`
`/reset`
`/clear`
`on_session_start`

Callback signature:

```
def my_callback(session_id: str, platform: str, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| session_id | str | The new session's ID (already rotated to the fresh value). |
| platform | str | The messaging platform name. |

`session_id`
`str`
`platform`
`str`

Fires:Ingateway/run.py, immediately after the new session key is allocated but before the next inbound message is processed. On the gateway, the order is:on_session_finalize(old_id)→ swap →on_session_reset(new_id)→on_session_start(new_id)on the first inbound turn.

`gateway/run.py`
`on_session_finalize(old_id)`
`on_session_reset(new_id)`
`on_session_start(new_id)`

Return value:Ignored.

Use cases:Reset per-session caches keyed bysession_id, emit "session rotated" analytics, prime a fresh state bucket.

`session_id`

See theBuild a Plugin guidefor the full walkthrough including tool schemas, handlers, and advanced hook patterns.

### subagent_start​

`subagent_start`

Firesonce per child agentafterdelegate_taskhas constructed the childAIAgentand before that child is run. Whether you delegate a single task or a batch of three, this hook fires once for each child.

`delegate_task`
`AIAgent`

This hook is specific to delegation/subagent lifecycle. It is not a universal "before any agent invocation" gate for gateway, CLI, cron, batch, MoA, or other runner-originated agent executions.

Callback signature:

```
def my_callback(parent_session_id: str | None,                parent_turn_id: str,                parent_subagent_id: str | None,                child_session_id: str | None,                child_subagent_id: str,                child_role: str,                child_goal: str,                **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| parent_session_id | str | None | Session ID of the delegating parent agent. |
| parent_turn_id | str | Turn ID of the parent agent turn that requested delegation, if available. |
| parent_subagent_id | str | None | Parent subagent ID when this child was spawned by another subagent;Nonefor top-level parent agents. |
| child_session_id | str | None | Session ID allocated for the child agent. |
| child_subagent_id | str | Stable subagent ID used by delegation observability and controls. |
| child_role | str | Effective child role after delegation policy is applied, for example"leaf"or"orchestrator". |
| child_goal | str | Delegated goal/prompt that the child agent will execute. |

`parent_session_id`
`str | None`
`parent_turn_id`
`str`
`parent_subagent_id`
`str | None`
`None`
`child_session_id`
`str | None`
`child_subagent_id`
`str`
`child_role`
`str`
`"leaf"`
`"orchestrator"`
`child_goal`
`str`

Fires:Intools/delegate_tool.py, inside_build_child_agent(), after the childAIAgenthas been constructed and annotated with subagent identity metadata, and before_run_single_child()runs the child.

`tools/delegate_tool.py`
`_build_child_agent()`
`AIAgent`
`_run_single_child()`

Return value:Ignored. This is an observer hook only; returning a value does not block or mutate the child agent run.

Use cases:Logging subagent creation, mapping parent/child session relationships, tracking nested delegation trees, emitting pre-run audit records, pre-allocating per-child observability resources.

Example — log subagent creation:

```
import logginglogger = logging.getLogger(__name__)def log_subagent_start(    parent_session_id,    parent_turn_id,    child_session_id,    child_subagent_id,    child_role,    child_goal,    **kwargs,):    logger.info(        "SUBAGENT_START parent=%s turn=%s child_session=%s child=%s role=%s goal=%r",        parent_session_id,        parent_turn_id,        child_session_id,        child_subagent_id,        child_role,        child_goal[:200],    )def register(ctx):    ctx.register_hook("subagent_start", log_subagent_start)
```

subagent_startis useful for delegation observability, but it is not a blocking policy hook. To block delegation before a child is built, usepre_tool_callto block thedelegate_tasktool call.

`subagent_start`
`pre_tool_call`
`delegate_task`

### subagent_stop​

`subagent_stop`

Firesonce per child agentafterdelegate_taskfinishes. Whether you delegated a single task or a batch of three, this hook fires once for each child, serialised on the parent thread.

`delegate_task`

Callback signature:

```
def my_callback(parent_session_id: str, child_role: str | None,                child_summary: str | None, child_status: str,                duration_ms: int, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| parent_session_id | str | Session ID of the delegating parent agent |
| child_role | str | None | Orchestrator role tag set on the child (Noneif the feature isn't enabled) |
| child_summary | str | None | The final response the child returned to the parent |
| child_status | str | "completed","failed","interrupted", or"error" |
| duration_ms | int | Wall-clock time spent running the child, in milliseconds |

`parent_session_id`
`str`
`child_role`
`str | None`
`None`
`child_summary`
`str | None`
`child_status`
`str`
`"completed"`
`"failed"`
`"interrupted"`
`"error"`
`duration_ms`
`int`

Fires:Intools/delegate_tool.py, afterThreadPoolExecutor.as_completed()drains all child futures. Firing is marshalled to the parent thread so hook authors don't have to reason about concurrent callback execution.

`tools/delegate_tool.py`
`ThreadPoolExecutor.as_completed()`

Return value:Ignored.

Use cases:Logging orchestration activity, accumulating child durations for billing, writing post-delegation audit records.

Example — log orchestrator activity:

```
import logginglogger = logging.getLogger(__name__)def log_subagent(parent_session_id, child_role, child_status, duration_ms, **kwargs):    logger.info(        "SUBAGENT parent=%s role=%s status=%s duration_ms=%d",        parent_session_id, child_role, child_status, duration_ms,    )def register(ctx):    ctx.register_hook("subagent_stop", log_subagent)
```

With heavy delegation (e.g. orchestrator roles × 5 leaves × nested depth),subagent_stopfires many times per turn. Keep your callback fast; push expensive work to a background queue.

`subagent_stop`

### pre_gateway_dispatch​

`pre_gateway_dispatch`

Firesonce per incomingMessageEventin the gateway, after the internal-event guard butbeforeauth/pairing and agent dispatch. This is the interception point for gateway-level message-flow policies (listen-only windows, human handover, per-chat routing, etc.) that don't fit cleanly into any single platform adapter.

`MessageEvent`

Callback signature:

```
def my_callback(event, gateway, session_store, **kwargs):
```

| Parameter | Type | Description |
| --- | --- | --- |
| event | MessageEvent | The normalized inbound message (has.text,.source,.message_id,.internal, etc.). |
| gateway | GatewayRunner | The active gateway runner, so plugins can callgateway.adapters[platform].send(...)for side-channel replies (owner notifications, etc.). |
| session_store | SessionStore | For silent transcript ingestion viasession_store.append_to_transcript(...). |

`event`
`MessageEvent`
`.text`
`.source`
`.message_id`
`.internal`
`gateway`
`GatewayRunner`
`gateway.adapters[platform].send(...)`
`session_store`
`SessionStore`
`session_store.append_to_transcript(...)`

Fires:Ingateway/run.py, insideGatewayRunner._handle_message(), immediately afteris_internalis computed.Internal events skip the hook entirely(they are system-generated — background-process completions, etc. — and must not be gate-kept by user-facing policy).

`gateway/run.py`
`GatewayRunner._handle_message()`
`is_internal`

Return value:Noneor a dict. The first recognized action dict wins; remaining plugin results are ignored. Exceptions in plugin callbacks are caught and logged; the gateway always falls through to normal dispatch on error.

`None`
| Return | Effect |
| --- | --- |
| {"action": "skip", "reason": "..."} | Drop the message — no agent reply, no pairing flow, no auth. Plugin is assumed to have handled it (e.g. silent-ingested into the transcript). |
| {"action": "rewrite", "text": "new text"} | Replaceevent.text, then continue normal dispatch with the modified event. Useful for collapsing buffered ambient messages into a single prompt. |
| {"action": "allow"}/None | Normal dispatch — runs the full auth / pairing / agent-loop chain. |

`{"action": "skip", "reason": "..."}`
`{"action": "rewrite", "text": "new text"}`
`event.text`
`{"action": "allow"}`
`None`

Use cases:Listen-only group chats (only respond when tagged; buffer ambient messages into context); human handover (silent-ingest customer messages while owner handles the chat manually); per-profile rate limiting; policy-driven routing.

Example — drop unauthorized DMs silently without triggering the pairing code:

```
def deny_unauthorized_dms(event, **kwargs):    src = event.source    if src.chat_type == "dm" and not _is_approved_user(src.user_id):        return {"action": "skip", "reason": "unauthorized-dm"}    return Nonedef register(ctx):    ctx.register_hook("pre_gateway_dispatch", deny_unauthorized_dms)
```

Example — rewrite an ambient-message buffer into a single prompt on mention:

```
_buffers = {}def buffer_or_rewrite(event, **kwargs):    key = (event.source.platform, event.source.chat_id)    buf = _buffers.setdefault(key, [])    if _bot_mentioned(event.text):        combined = "\n".join(buf + [event.text])        buf.clear()        return {"action": "rewrite", "text": combined}    buf.append(event.text)    return {"action": "skip", "reason": "ambient-buffered"}def register(ctx):    ctx.register_hook("pre_gateway_dispatch", buffer_or_rewrite)
```

### pre_approval_request​

`pre_approval_request`

Firesimmediately beforean approval request is shown to the user — covers every surface: interactive CLI, the Ink TUI, gateway platforms (Telegram, Discord, Slack, WhatsApp, Matrix, etc.), and ACP clients (VS Code, Zed, JetBrains).

This is the right place to wire a custom notifier — for example, a macOS menu-bar app that pops an allow/deny notification, or an audit log that records every approval request with context.

Callback signature:

```
def my_callback(    command: str,    description: str,    pattern_key: str,    pattern_keys: list[str],    session_key: str,    surface: str,    **kwargs,):
```

| Parameter | Type | Description |
| --- | --- | --- |
| command | str | The shell command awaiting approval |
| description | str | Human-readable reason(s) the command is flagged (combined when multiple patterns match) |
| pattern_key | str | Primary pattern key that triggered the approval (e.g."rm_rf","sudo") |
| pattern_keys | list[str] | All pattern keys that matched |
| session_key | str | Session identifier, useful for scoping notifications per-chat |
| surface | str | "cli"for interactive CLI/TUI prompts,"gateway"for async platform approvals |

`command`
`str`
`description`
`str`
`pattern_key`
`str`
`"rm_rf"`
`"sudo"`
`pattern_keys`
`list[str]`
`session_key`
`str`
`surface`
`str`
`"cli"`
`"gateway"`

Return value:ignored. Hooks here are observer-only; they cannot veto or pre-answer the approval. Usepre_tool_callto block a tool before it reaches the approval system.

`pre_tool_call`

Use cases:Desktop notifications, push alerts, audit logging, Slack webhooks, escalation routing, metrics.

Example — desktop notification on macOS:

```
import subprocessdef notify_approval(command, description, session_key, **kwargs):    title = "Hermes needs approval"    body = f"{description}: {command[:80]}"    subprocess.Popen([        "osascript", "-e",        f'display notification "{body}" with title "{title}"',    ])def register(ctx):    ctx.register_hook("pre_approval_request", notify_approval)
```

### post_approval_response​

`post_approval_response`

Firesafterthe user responds to an approval prompt (or the prompt times out).

Callback signature:

```
def my_callback(    command: str,    description: str,    pattern_key: str,    pattern_keys: list[str],    session_key: str,    surface: str,    choice: str,    **kwargs,):
```

Same kwargs aspre_approval_request, plus:

`pre_approval_request`
| Parameter | Type | Description |
| --- | --- | --- |
| choice | str | One of"once","session","always","deny", or"timeout" |

`choice`
`str`
`"once"`
`"session"`
`"always"`
`"deny"`
`"timeout"`

Return value:ignored.

Use cases:Close the matching desktop notification, record the final decision in an audit log, update metrics, roll forward a rate limiter.

```
def log_decision(command, choice, session_key, **kwargs):    logger.info("approval %s: %s for session %s", choice, command[:60], session_key)def register(ctx):    ctx.register_hook("post_approval_response", log_decision)
```

### transform_tool_result​

`transform_tool_result`

Firesaftera tool returns andbeforethe result is appended to the conversation. Lets a plugin rewrite ANY tool's result string — not just terminal output — before the model sees it.

Callback signature:

```
def my_callback(    tool_name: str,    arguments: dict,    result: str,    task_id: str | None,    **kwargs,) -> str | None:
```

| Parameter | Type | Description |
| --- | --- | --- |
| tool_name | str | Tool that produced the result (read_file,web_extract,delegate_task, …). |
| arguments | dict | Arguments the model called the tool with. |
| result | str | The tool's raw result string, post-truncation and post-ANSI-strip. |
| task_id | str | None | Task/session ID when running inside RL/benchmark environments. |

`tool_name`
`str`
`read_file`
`web_extract`
`delegate_task`
`arguments`
`dict`
`result`
`str`
`task_id`
`str | None`

Return value:strto replace the result (the returned string is what the model sees),Noneto leave it unchanged.

`str`
`None`

Use cases:Redact organization-specific PII fromweb_extractoutput, wrap long JSON tool responses in a summary header, inject retrieval-augmented hints intoread_fileresults, rewritedelegate_tasksubagent reports into a project-specific schema.

`web_extract`
`read_file`
`delegate_task`

```
import reSECRET = re.compile(r"sk-[A-Za-z0-9]{32,}")def redact_secrets(tool_name, result, **kwargs):    if SECRET.search(result):        return SECRET.sub("[REDACTED]", result)    return Nonedef register(ctx):    ctx.register_hook("transform_tool_result", redact_secrets)
```

Applies to every tool. For terminal-only rewriting seetransform_terminal_outputbelow — it's narrower and runs earlier in the pipeline (pre-truncation, pre-redaction).

`transform_terminal_output`

### transform_terminal_output​

`transform_terminal_output`

Fires inside theterminaltool's foreground-output pipeline,beforethe default 50 KB truncation, ANSI strip, and secret redaction. Lets plugins rewrite the raw stdout/stderr of a shell command before any downstream processing touches it.

`terminal`

Callback signature:

```
def my_callback(    command: str,    output: str,    exit_code: int,    cwd: str,    task_id: str | None,    **kwargs,) -> str | None:
```

| Parameter | Type | Description |
| --- | --- | --- |
| command | str | The shell command that produced the output. |
| output | str | Raw combined stdout/stderr (may be very large — truncation happens after the hook). |
| exit_code | int | Process exit code. |
| cwd | str | Working directory the command ran in. |

`command`
`str`
`output`
`str`
`exit_code`
`int`
`cwd`
`str`

Return value:strto replace the output,Noneto leave it unchanged.

`str`
`None`

Use cases:Inject summaries for commands that produce massive output (du -ah,find,tree), tag output with a project-specific marker so downstream hooks know how to handle it, strip timing noise that flaps between runs and defeats prompt caching.

`du -ah`
`find`
`tree`

```
def summarize_find(command, output, **kwargs):    if command.startswith("find ") and len(output) > 50_000:        lines = output.count("\n")        head = "\n".join(output.splitlines()[:40])        return f"{head}\n\n[summary: {lines} paths total, showing first 40]"    return Nonedef register(ctx):    ctx.register_hook("transform_terminal_output", summarize_find)
```

Pairs well withtransform_tool_result(which covers every other tool).

`transform_tool_result`

### transform_llm_output​

`transform_llm_output`

Firesonce per turnafter the tool-calling loop completes and the model has produced a final response,beforethat response is delivered to the user (CLI, gateway, or programmatic caller). Lets a plugin rewrite the assistant's final text using classical-programming methods — no extra inference tokens burned on SOUL flavor text or a skill-driven transform.

Callback signature:

```
def my_callback(    response_text: str,    session_id: str,    model: str,    platform: str,    **kwargs,) -> str | None:
```

| Parameter | Type | Description |
| --- | --- | --- |
| response_text | str | The assistant's final response text for this turn. |
| session_id | str | Session ID for this conversation (may be empty for one-shot runs). |
| model | str | Model name that produced the response (e.g.anthropic/claude-sonnet-4.6). |
| platform | str | Delivery platform (cli,telegram,discord, …; empty when unset). |

`response_text`
`str`
`session_id`
`str`
`model`
`str`
`anthropic/claude-sonnet-4.6`
`platform`
`str`
`cli`
`telegram`
`discord`

Return value:Non-emptystrto replace the response text,Noneor empty string to leave it unchanged.First non-empty string winswhen multiple plugins register — mirroringtransform_tool_result.

`str`
`None`
`transform_tool_result`

Use cases:Apply a personality/vocabulary transform (pirate-speak, Spongebob), redact user-specific identifiers from the final text, append a project-specific signature footer, enforce a house style guide without burning tokens on SOUL instructions.

```
import os, redef spongebob(response_text, **kwargs):    if os.environ.get("SPONGEBOB_MODE") != "on":        return None  # pass through unchanged    return re.sub(r"!", "!! Tartar sauce!", response_text)def register(ctx):    ctx.register_hook("transform_llm_output", spongebob)
```

The hook is guarded on a non-empty, non-interrupted response — it will not fire on stop-button interrupts or empty turns. Exceptions are logged as warnings and do not break agent execution.

## Shell Hooks​

Declare shell-script hooks in yourcli-config.yamland Hermes will run them as subprocesses whenever the corresponding plugin-hook event fires — in both CLI and gateway sessions. No Python plugin authoring required.

`cli-config.yaml`

Use shell hooks when you want a drop-in, single-file script (Bash, Python, anything with a shebang) to:

- Block a tool call— reject dangerousterminalcommands, enforce per-directory policies, require approval for destructivewrite_file/patchoperations.
- Run after a tool call— auto-format Python or TypeScript files that the agent just wrote, log API calls, trigger a CI workflow.
- Inject context into the next LLM turn— prependgit statusoutput, the current weekday, or retrieved documents to the user message (seepre_llm_call).
- Observe lifecycle events— write a log line when a subagent completes (subagent_stop) or a session starts (on_session_start).

`terminal`
`write_file`
`patch`
`git status`
`pre_llm_call`
`subagent_stop`
`on_session_start`

Shell hooks are registered by callingagent.shell_hooks.register_from_config(cfg)at both CLI startup (hermes_cli/main.py) and gateway startup (gateway/run.py). They compose naturally with Python plugin hooks — both flow through the same dispatcher.

`agent.shell_hooks.register_from_config(cfg)`
`hermes_cli/main.py`
`gateway/run.py`

### Comparison at a glance​

| Dimension | Shell hooks | Plugin hooks | Gateway hooks |
| --- | --- | --- | --- |
| Declared in | hooks:block in~/.hermes/config.yaml | register()in aplugin.yamlplugin | HOOK.yaml+handler.pydirectory |
| Lives under | ~/.hermes/agent-hooks/(by convention) | ~/.hermes/plugins/<name>/ | ~/.hermes/hooks/<name>/ |
| Language | Any (Bash, Python, Go binary, …) | Python only | Python only |
| Runs in | CLI + Gateway | CLI + Gateway | Gateway only |
| Events | VALID_HOOKS(incl.subagent_stop) | VALID_HOOKS | Gateway lifecycle (gateway:startup,agent:*,command:*) |
| Can block a tool call | Yes (pre_tool_call) | Yes (pre_tool_call) | No |
| Can inject LLM context | Yes (pre_llm_call) | Yes (pre_llm_call) | No |
| Consent | First-use prompt per(event, command)pair | Implicit (Python plugin trust) | Implicit (dir trust) |
| Inter-process isolation | Yes (subprocess) | No (in-process) | No (in-process) |

`hooks:`
`~/.hermes/config.yaml`
`register()`
`plugin.yaml`
`HOOK.yaml`
`handler.py`
`~/.hermes/agent-hooks/`
`~/.hermes/plugins/<name>/`
`~/.hermes/hooks/<name>/`
`VALID_HOOKS`
`subagent_stop`
`VALID_HOOKS`
`gateway:startup`
`agent:*`
`command:*`
`pre_tool_call`
`pre_tool_call`
`pre_llm_call`
`pre_llm_call`
`(event, command)`

### Configuration schema​

```
hooks:  <event_name>:                  # Must be in VALID_HOOKS    - matcher: "<regex>"         # Optional; used for pre/post_tool_call only      command: "<shell command>" # Required; runs via shlex.split, shell=False      timeout: <seconds>         # Optional; default 60, capped at 300hooks_auto_accept: false         # See "Consent model" below
```

Event names must be one of theplugin hook events; typos produce a "Did you mean X?" warning and are skipped. Unknown keys inside a single entry are ignored; missingcommandis a skip-with-warning.timeout > 300is clamped with a warning.

`command`
`timeout > 300`

### JSON wire protocol​

Each time the event fires, Hermes spawns a subprocess for every matching hook (matcher permitting), pipes a JSON payload tostdin, and readsstdoutback as JSON.

stdin — payload the script receives:

```
{  "hook_event_name": "pre_tool_call",  "tool_name":       "terminal",  "tool_input":      {"command": "rm -rf /"},  "session_id":      "sess_abc123",  "cwd":             "/home/user/project",  "extra":           {"task_id": "...", "tool_call_id": "..."}}
```

tool_nameandtool_inputarenullfor non-tool events (pre_llm_call,subagent_stop, session lifecycle). Theextradict carries all event-specific kwargs (user_message,conversation_history,child_role,duration_ms, …). Unserialisable values are stringified rather than omitted.

`tool_name`
`tool_input`
`null`
`pre_llm_call`
`subagent_stop`
`extra`
`user_message`
`conversation_history`
`child_role`
`duration_ms`

stdout — optional response:

```
// Block a pre_tool_call (both shapes accepted; normalised internally):{"decision": "block", "reason":  "Forbidden: rm -rf"}   // Claude-Code style{"action":   "block", "message": "Forbidden: rm -rf"}   // Hermes-canonical// Inject context for pre_llm_call:{"context": "Today is Friday, 2026-04-17"}// Keep the agent going at the verify gate (pre_verify); both shapes accepted:{"action": "continue", "message": "Run the formatter, then finish."}{"decision": "block",  "reason":  "Run the formatter, then finish."}// Silent no-op — any empty / non-matching output is fine:
```

Malformed JSON, non-zero exit codes, and timeouts log a warning but never abort the agent loop.

### Worked examples​

#### 1. Auto-format Python files after every write​

```
# ~/.hermes/config.yamlhooks:  post_tool_call:    - matcher: "write_file|patch"      command: "~/.hermes/agent-hooks/auto-format.sh"
```

```
#!/usr/bin/env bash# ~/.hermes/agent-hooks/auto-format.shpayload="$(cat -)"path=$(echo "$payload" | jq -r '.tool_input.path // empty')[[ "$path" == *.py ]] && command -v black >/dev/null && black "$path" 2>/dev/nullprintf '{}\n'
```

The agent's in-context view of the file isnotre-read automatically — the reformat only affects the file on disk. Subsequentread_filecalls pick up the formatted version.

`read_file`

#### 2. Block destructiveterminalcommands​

`terminal`

```
hooks:  pre_tool_call:    - matcher: "terminal"      command: "~/.hermes/agent-hooks/block-rm-rf.sh"      timeout: 5
```

```
#!/usr/bin/env bash# ~/.hermes/agent-hooks/block-rm-rf.shpayload="$(cat -)"cmd=$(echo "$payload" | jq -r '.tool_input.command // empty')if echo "$cmd" | grep -qE 'rm[[:space:]]+-rf?[[:space:]]+/'; then  printf '{"decision": "block", "reason": "blocked: rm -rf / is not permitted"}\n'else  printf '{}\n'fi
```

#### 3. Injectgit statusinto every turn (Claude-CodeUserPromptSubmitequivalent)​

`git status`
`UserPromptSubmit`

```
hooks:  pre_llm_call:    - command: "~/.hermes/agent-hooks/inject-cwd-context.sh"
```

```
#!/usr/bin/env bash# ~/.hermes/agent-hooks/inject-cwd-context.shcat - >/dev/null   # discard stdin payloadif status=$(git status --porcelain 2>/dev/null) && [[ -n "$status" ]]; then  jq --null-input --arg s "$status" \     '{context: ("Uncommitted changes in cwd:\n" + $s)}'else  printf '{}\n'fi
```

Claude Code'sUserPromptSubmitevent is intentionally not a separate Hermes event —pre_llm_callfires at the same place and already supports context injection. Use it here.

`UserPromptSubmit`
`pre_llm_call`

#### 4. Log every subagent completion​

```
hooks:  subagent_stop:    - command: "~/.hermes/agent-hooks/log-orchestration.sh"
```

```
#!/usr/bin/env bash# ~/.hermes/agent-hooks/log-orchestration.shlog=~/.hermes/logs/orchestration.logjq -c '{ts: now, parent: .session_id, extra: .extra}' < /dev/stdin >> "$log"printf '{}\n'
```

### Consent model​

Each unique(event, command)pair prompts the user for approval the first time Hermes sees it, then persists the decision to~/.hermes/shell-hooks-allowlist.json. Subsequent runs (CLI or gateway) skip the prompt.

`(event, command)`
`~/.hermes/shell-hooks-allowlist.json`

Three escape hatches bypass the interactive prompt — any one is sufficient:

1. --accept-hooksflag on the CLI (e.g.hermes --accept-hooks chat)
2. HERMES_ACCEPT_HOOKS=1environment variable
3. hooks_auto_accept: trueincli-config.yaml

`--accept-hooks`
`hermes --accept-hooks chat`
`HERMES_ACCEPT_HOOKS=1`
`hooks_auto_accept: true`
`cli-config.yaml`

Non-TTY runs (gateway, cron, CI) need one of these three — otherwise any newly-added hook silently stays un-registered and logs a warning.

Script edits are silently trusted.The allowlist keys on the exact command string, not the script's hash, so editing the script on disk does not invalidate consent.hermes hooks doctorflags mtime drift so you can spot edits and decide whether to re-approve.

`hermes hooks doctor`

#### Manual allowlisting​

Manual allowlisting is useful for non-TTY or service-account deployments where an operator cannot answer the first-use prompt interactively. The allowlist file is~/.hermes/shell-hooks-allowlist.json, and the expected format is anapprovalsarray. Each approval records the hookeventand the exactcommandstring:

`~/.hermes/shell-hooks-allowlist.json`
`approvals`
`event`
`command`

```
{  "approvals": [    {      "event": "post_llm_call",      "command": "/home/hermes/.hermes/hooks/my-hook.py"    }  ]}
```

The command string must match the configured hook command exactly. A path-keyed object with asha256field is not the expected format and will not approve the hook. Verify manual entries withhermes hooks list.

`sha256`
`hermes hooks list`

### Thehermes hooksCLI​

`hermes hooks`
| Command | What it does |
| --- | --- |
| hermes hooks list | Dump configured hooks with matcher, timeout, and consent status |
| hermes hooks test <event> [--for-tool X] [--payload-file F] | Fire every matching hook against a synthetic payload and print the parsed response |
| hermes hooks revoke <command> | Remove every allowlist entry matching<command>(takes effect on next restart) |
| hermes hooks doctor | For every configured hook: check exec bit, allowlist status, mtime drift, JSON output validity, and rough execution time |

`hermes hooks list`
`hermes hooks test <event> [--for-tool X] [--payload-file F]`
`hermes hooks revoke <command>`
`<command>`
`hermes hooks doctor`

### Security​

Shell hooks run withyour full user credentials— same trust boundary as a cron entry or a shell alias. Treat thehooks:block inconfig.yamlas privileged configuration:

`hooks:`
`config.yaml`
- Only reference scripts you wrote or fully reviewed.
- Keep scripts inside~/.hermes/agent-hooks/so the path is easy to audit.
- Re-runhermes hooks doctorafter you pull a shared config to spot newly-added hooks before they register.
- If your config.yaml is version-controlled across a team, review PRs that change thehooks:section the same way you'd review CI config.

`~/.hermes/agent-hooks/`
`hermes hooks doctor`
`hooks:`

### Ordering and precedence​

Both Python plugin hooks and shell hooks flow through the sameinvoke_hook()dispatcher. Python plugins are registered first (discover_and_load()), shell hooks second (register_from_config()), so Pythonpre_tool_callblock decisions take precedence in tie cases. The first valid block wins — the aggregator returns as soon as any callback produces{"action": "block", "message": str}with a non-empty message.

`invoke_hook()`
`discover_and_load()`
`register_from_config()`
`pre_tool_call`
`{"action": "block", "message": str}`