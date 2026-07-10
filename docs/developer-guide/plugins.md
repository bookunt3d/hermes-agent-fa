---
layout: docs
title: "پلاگین‌ها"
permalink: /docs/developer-guide/plugins/
---

- 
- Developer Guide
- Extending
- Plugins

# Build a Hermes Plugin

This guide walks through building a complete Hermes plugin from scratch. By the end you'll have a working plugin with multiple tools, lifecycle hooks, shipped data files, and a bundled skill — everything the plugin system supports.

Hermes has several distinct pluggable interfaces — some use Pythonregister_*APIs, others are config-driven or drop-in directories. Use this map first:

`register_*`
| If you want to add… | Read |
| --- | --- |
| Custom tools, hooks, slash commands, skills, or CLI subcommands | This guide(the general plugin surface) |
| AnLLM / inference backend(new provider) | Model Provider Plugins |
| Agateway channel(Discord/Telegram/IRC/Teams/etc.) | Adding Platform Adapters |
| Amemory backend(Honcho/Mem0/Supermemory/etc.) | Memory Provider Plugins |
| Acontext-compression engine | Context Engine Plugins |
| Animage-generation backend | Image Generation Provider Plugins |
| Avideo-generation backend | Video Generation Provider Plugins |
| Aweb-search / extract backend | Web Search Provider Plugins |
| Acloud browser backend(Browserbase-style CDP session provider) | Browser Provider Plugins |
| Asecret-manager backend(vault / password manager / OS keystore) | Secret Source Plugins |
| Adashboard OIDC/auth provider | Web Dashboard — custom providers—ctx.register_dashboard_auth_provider() |
| ATTS backend(any CLI — Piper, VoxCPM, Kokoro, voice cloning, …) | TTS custom command providers— config-driven, no Python needed |
| AnSTT backend(custom whisper / ASR CLI) | Voice Message Transcription— setHERMES_LOCAL_STT_COMMANDto a shell template |
| External tools via MCP(filesystem, GitHub, Linear, any MCP server) | MCP— declaremcp_servers.<name>inconfig.yaml |
| Gateway event hooks(fire on startup, session events, commands) | Event Hooks— dropHOOK.yaml+handler.pyinto~/.hermes/hooks/<name>/ |
| Shell hooks(run a shell command on events) | Shell Hooks— declare underhooks:inconfig.yaml |
| Additional skill sources(custom GitHub repos, private skill indexes) | Skills—hermes skills tap add <repo>·Publishing a tap |
| A first-classcoreinference provider (not a plugin) | Adding Providers |

`ctx.register_dashboard_auth_provider()`
`HERMES_LOCAL_STT_COMMAND`
`mcp_servers.<name>`
`config.yaml`
`HOOK.yaml`
`handler.py`
`~/.hermes/hooks/<name>/`
`hooks:`
`config.yaml`
`hermes skills tap add <repo>`

See the fullPluggable interfaces tablefor a consolidated view of every extension surface including config-driven (TTS, STT, MCP, shell hooks) and drop-in directory (gateway hooks) styles.

Plugins that integratesomeone else's product or project— observability/metrics backends, vendor SaaS connectors, analytics dashboards, paid-service tie-ins — are built and distributed asstandalone plugin repos, not merged intoNousResearch/hermes-agent. Users install them into~/.hermes/plugins/or via a pip entry point; everything in this guide works the same way from a standalone repo. This is a coupling-and-maintenance decision (the core moves fast and we don't own your backend), not a quality bar — a plugin can be excellent and still belong in its own repo. Promote it in the Nous Research Discord#plugins-skills-and-skinschannel. SeeCONTRIBUTING.mdfor the policy.

`NousResearch/hermes-agent`
`~/.hermes/plugins/`
`#plugins-skills-and-skins`

## What you're building​

Acalculatorplugin with two tools:

- calculate— evaluate math expressions (2**16,sqrt(144),pi * 5**2)
- unit_convert— convert between units (100 F → 37.78 C,5 km → 3.11 mi)

`calculate`
`2**16`
`sqrt(144)`
`pi * 5**2`
`unit_convert`
`100 F → 37.78 C`
`5 km → 3.11 mi`

Plus a hook that logs every tool call, and a bundled skill file.

## Step 1: Create the plugin directory​

```
mkdir -p ~/.hermes/plugins/calculatorcd ~/.hermes/plugins/calculator
```

## Step 2: Write the manifest​

Createplugin.yaml:

`plugin.yaml`

```
name: calculatorversion: 1.0.0description: Math calculator — evaluate expressions and convert unitsprovides_tools:  - calculate  - unit_convertprovides_hooks:  - post_tool_call
```

This tells Hermes: "I'm a plugin called calculator, I provide tools and hooks." Theprovides_toolsandprovides_hooksfields are lists of what the plugin registers.

`provides_tools`
`provides_hooks`

Optional fields you could add:

```
author: Your Namerequires_env:          # gate loading on env vars; prompted during install  - SOME_API_KEY       # simple format — plugin disabled if missing  - name: OTHER_KEY    # rich format — shows description/url during install    description: "Key for the Other service"    url: "https://other.com/keys"    secret: true
```

## Step 3: Write the tool schemas​

Createschemas.py— this is what the LLM reads to decide when to call your tools:

`schemas.py`

```
"""Tool schemas — what the LLM sees."""CALCULATE = {    "name": "calculate",    "description": (        "Evaluate a mathematical expression and return the result. "        "Supports arithmetic (+, -, *, /, **), functions (sqrt, sin, cos, "        "log, abs, round, floor, ceil), and constants (pi, e). "        "Use this for any math the user asks about."    ),    "parameters": {        "type": "object",        "properties": {            "expression": {                "type": "string",                "description": "Math expression to evaluate (e.g., '2**10', 'sqrt(144)')",            },        },        "required": ["expression"],    },}UNIT_CONVERT = {    "name": "unit_convert",    "description": (        "Convert a value between units. Supports length (m, km, mi, ft, in), "        "weight (kg, lb, oz, g), temperature (C, F, K), data (B, KB, MB, GB, TB), "        "and time (s, min, hr, day)."    ),    "parameters": {        "type": "object",        "properties": {            "value": {                "type": "number",                "description": "The numeric value to convert",            },            "from_unit": {                "type": "string",                "description": "Source unit (e.g., 'km', 'lb', 'F', 'GB')",            },            "to_unit": {                "type": "string",                "description": "Target unit (e.g., 'mi', 'kg', 'C', 'MB')",            },        },        "required": ["value", "from_unit", "to_unit"],    },}
```

Why schemas matter:Thedescriptionfield is how the LLM decides when to use your tool. Be specific about what it does and when to use it. Theparametersdefine what arguments the LLM passes.

`description`
`parameters`

## Step 4: Write the tool handlers​

Createtools.py— this is the code that actually executes when the LLM calls your tools:

`tools.py`

```
"""Tool handlers — the code that runs when the LLM calls each tool."""import jsonimport math# Safe globals for expression evaluation — no file/network access_SAFE_MATH = {    "abs": abs, "round": round, "min": min, "max": max,    "pow": pow, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,    "tan": math.tan, "log": math.log, "log2": math.log2, "log10": math.log10,    "floor": math.floor, "ceil": math.ceil,    "pi": math.pi, "e": math.e,    "factorial": math.factorial,}def calculate(args: dict, **kwargs) -> str:    """Evaluate a math expression safely.    Rules for handlers:    1. Receive args (dict) — the parameters the LLM passed    2. Do the work    3. Return a JSON string — ALWAYS, even on error    4. Accept **kwargs for forward compatibility    """    expression = args.get("expression", "").strip()    if not expression:        return json.dumps({"error": "No expression provided"})    try:        result = eval(expression, {"__builtins__": {}}, _SAFE_MATH)        return json.dumps({"expression": expression, "result": result})    except ZeroDivisionError:        return json.dumps({"expression": expression, "error": "Division by zero"})    except Exception as e:        return json.dumps({"expression": expression, "error": f"Invalid: {e}"})# Conversion tables — values are in base units_LENGTH = {"m": 1, "km": 1000, "mi": 1609.34, "ft": 0.3048, "in": 0.0254, "cm": 0.01}_WEIGHT = {"kg": 1, "g": 0.001, "lb": 0.453592, "oz": 0.0283495}_DATA = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}_TIME = {"s": 1, "ms": 0.001, "min": 60, "hr": 3600, "day": 86400}def _convert_temp(value, from_u, to_u):    # Normalize to Celsius    c = {"F": (value - 32) * 5/9, "K": value - 273.15}.get(from_u, value)    # Convert to target    return {"F": c * 9/5 + 32, "K": c + 273.15}.get(to_u, c)def unit_convert(args: dict, **kwargs) -> str:    """Convert between units."""    value = args.get("value")    from_unit = args.get("from_unit", "").strip()    to_unit = args.get("to_unit", "").strip()    if value is None or not from_unit or not to_unit:        return json.dumps({"error": "Need value, from_unit, and to_unit"})    try:        # Temperature        if from_unit.upper() in {"C","F","K"} and to_unit.upper() in {"C","F","K"}:            result = _convert_temp(float(value), from_unit.upper(), to_unit.upper())            return json.dumps({"input": f"{value} {from_unit}", "result": round(result, 4),                             "output": f"{round(result, 4)} {to_unit}"})        # Ratio-based conversions        for table in (_LENGTH, _WEIGHT, _DATA, _TIME):            lc = {k.lower(): v for k, v in table.items()}            if from_unit.lower() in lc and to_unit.lower() in lc:                result = float(value) * lc[from_unit.lower()] / lc[to_unit.lower()]                return json.dumps({"input": f"{value} {from_unit}",                                 "result": round(result, 6),                                 "output": f"{round(result, 6)} {to_unit}"})        return json.dumps({"error": f"Cannot convert {from_unit} → {to_unit}"})    except Exception as e:        return json.dumps({"error": f"Conversion failed: {e}"})
```

Key rules for handlers:

1. Signature:def my_handler(args: dict, **kwargs) -> str
2. Return:Always a JSON string. Success and errors alike.
3. Never raise:Catch all exceptions, return error JSON instead.
4. Accept**kwargs:Hermes may pass additional context in the future.

`def my_handler(args: dict, **kwargs) -> str`
`**kwargs`

## Step 5: Write the registration​

Create__init__.py— this wires schemas to handlers:

`__init__.py`

```
"""Calculator plugin — registration."""import loggingfrom . import schemas, toolslogger = logging.getLogger(__name__)# Track tool usage via hooks_call_log = []def _on_post_tool_call(tool_name, args, result, task_id, **kwargs):    """Hook: runs after every tool call (not just ours)."""    _call_log.append({"tool": tool_name, "session": task_id})    if len(_call_log) > 100:        _call_log.pop(0)    logger.debug("Tool called: %s (session %s)", tool_name, task_id)def register(ctx):    """Wire schemas to handlers and register hooks."""    ctx.register_tool(name="calculate",    toolset="calculator",                      schema=schemas.CALCULATE,    handler=tools.calculate)    ctx.register_tool(name="unit_convert", toolset="calculator",                      schema=schemas.UNIT_CONVERT, handler=tools.unit_convert)    # This hook fires for ALL tool calls, not just ours    ctx.register_hook("post_tool_call", _on_post_tool_call)
```

Whatregister()does:

`register()`
- Called exactly once at startup
- ctx.register_tool()puts your tool in the registry — the model sees it immediately
- ctx.register_hook()subscribes to lifecycle events
- ctx.register_cli_command()registers a CLI subcommand (e.g.hermes my-plugin <subcommand>)
- ctx.register_command()registers an in-session slash command (e.g./myplugin <args>inside CLI / gateway chat) — seeRegister slash commandsbelow
- ctx.dispatch_tool(name, arguments)— call any other tool (built-in or from another plugin) with the parent agent's context (approvals, credentials, task_id) wired up automatically. Useful from slash-command handlers that need to invoketerminal,read_file, or any other tool as if the model had called it directly.
- If this function crashes, the plugin is disabled but Hermes continues fine

`ctx.register_tool()`
`ctx.register_hook()`
`ctx.register_cli_command()`
`hermes my-plugin <subcommand>`
`ctx.register_command()`
`/myplugin <args>`
`ctx.dispatch_tool(name, arguments)`
`terminal`
`read_file`

dispatch_toolexample — a slash command that runs a tool:

`dispatch_tool`

```
def handle_scan(ctx, raw_args: str):    """Implement /scan by invoking the terminal tool through the registry."""    result = ctx.dispatch_tool("terminal", {"command": f"find . -name '{raw_args}'"})    return result  # returned to the caller's chat UIdef register(ctx):    # Handlers receive a single raw_args string; close over ctx via a lambda.    ctx.register_command(        "scan",        lambda raw: handle_scan(ctx, raw),        description="Find files matching a glob",    )
```

The dispatched tool goes through the normal approval, redaction, and budget pipelines — it's a real tool invocation, not a shortcut around them.

## Step 6: Test it​

Start Hermes:

```
hermes
```

You should seecalculator: calculate, unit_convertin the banner's tool list.

`calculator: calculate, unit_convert`

Try these prompts:

```
What's 2 to the power of 16?Convert 100 fahrenheit to celsiusWhat's the square root of 2 times pi?How many gigabytes is 1.5 terabytes?
```

Check plugin status:

```
/plugins
```

Output:

```
Plugins (1):  ✓ calculator v1.0.0 (2 tools, 1 hooks)
```

### Debugging plugin discovery​

If your plugin doesn't show up — or shows up but isn't loading — setHERMES_PLUGINS_DEBUG=1to get verbose discovery logs on stderr:

`HERMES_PLUGINS_DEBUG=1`

```
HERMES_PLUGINS_DEBUG=1 hermes plugins list
```

You'll see, for every plugin source (bundled, user, project, entry-points):

- which directories were scanned and how many manifests each yielded
- per manifest: resolved key, name, kind, source, on-disk path
- skip reasons:disabled via config,not enabled in config,exclusive plugin,no plugin.yaml, depth cap reached
- on load: the plugin being imported, plus a one-line summary of whatregister(ctx)registered (tools, hooks, slash commands, CLI commands)
- on parse failure: a full traceback for the exception (YAML scanner errors, etc.)
- onregister()failure: a full traceback pointing at the line in your__init__.pythat raised

`disabled via config`
`not enabled in config`
`exclusive plugin`
`no plugin.yaml, depth cap reached`
`register(ctx)`
`register()`
`__init__.py`

The same logs are always written to~/.hermes/logs/agent.logat WARNING level (failures only) and DEBUG level (everything) when the env var is set. So if you can't run with the env var (e.g. from inside the gateway), tail the log file instead:

`~/.hermes/logs/agent.log`

```
hermes logs --level WARNING | grep -i plugin
```

Common reasons a plugin doesn't appear:

- Not enabled in config— plugins are opt-in. Runhermes plugins enable <name>(the name comes from theplugins listoutput, which can be<category>/<plugin>for nested layouts).
- Wrong directory layout— must be~/.hermes/plugins/<plugin-name>/plugin.yaml(flat) or~/.hermes/plugins/<category>/<plugin-name>/plugin.yaml(one level of category nesting, max). Anything deeper is ignored.
- Missing__init__.py— the plugin directory needs bothplugin.yamland__init__.pywith aregister(ctx)function.
- Wrongkind— gateway adapters needkind: platformin their manifest. Memory providers are auto-detected askind: exclusiveand routed through thememory.providerconfig instead ofplugins.enabled.

`hermes plugins enable <name>`
`plugins list`
`<category>/<plugin>`
`~/.hermes/plugins/<plugin-name>/plugin.yaml`
`~/.hermes/plugins/<category>/<plugin-name>/plugin.yaml`
`__init__.py`
`plugin.yaml`
`__init__.py`
`register(ctx)`
`kind`
`kind: platform`
`kind: exclusive`
`memory.provider`
`plugins.enabled`

## Your plugin's final structure​

```
~/.hermes/plugins/calculator/├── plugin.yaml      # "I'm calculator, I provide tools and hooks"├── __init__.py      # Wiring: schemas → handlers, register hooks├── schemas.py       # What the LLM reads (descriptions + parameter specs)└── tools.py         # What runs (calculate, unit_convert functions)
```

Four files, clear separation:

- Manifestdeclares what the plugin is
- Schemasdescribe tools for the LLM
- Handlersimplement the actual logic
- Registrationconnects everything

## What else can plugins do?​

### Ship data files​

Put any files in your plugin directory and read them at import time:

```
# In tools.py or __init__.pyfrom pathlib import Path_PLUGIN_DIR = Path(__file__).parent_DATA_FILE = _PLUGIN_DIR / "data" / "languages.yaml"with open(_DATA_FILE) as f:    _DATA = yaml.safe_load(f)
```

### Bundle skills​

Plugins can ship skill files that the agent loads viaskill_view("plugin:skill"). Register them in your__init__.py:

`skill_view("plugin:skill")`
`__init__.py`

```
~/.hermes/plugins/my-plugin/├── __init__.py├── plugin.yaml└── skills/    ├── my-workflow/    │   └── SKILL.md    └── my-checklist/        └── SKILL.md
```

```
from pathlib import Pathdef register(ctx):    skills_dir = Path(__file__).parent / "skills"    for child in sorted(skills_dir.iterdir()):        skill_md = child / "SKILL.md"        if child.is_dir() and skill_md.exists():            ctx.register_skill(child.name, skill_md)
```

The agent can now load your skills with their namespaced name:

```
skill_view("my-plugin:my-workflow")   # → plugin's versionskill_view("my-workflow")              # → built-in version (unchanged)
```

Key properties:

- Plugin skills areread-only— they don't enter~/.hermes/skills/and can't be edited viaskill_manage.
- Plugin skills arenotlisted in the system prompt's<available_skills>index — they're opt-in explicit loads.
- Bare skill names are unaffected — the namespace prevents collisions with built-in skills.
- When the agent loads a plugin skill, a bundle context banner is prepended listing sibling skills from the same plugin.

`~/.hermes/skills/`
`skill_manage`
`<available_skills>`

The oldshutil.copy2pattern (copying a skill into~/.hermes/skills/) still works but creates name collision risk with built-in skills. Preferctx.register_skill()for new plugins.

`shutil.copy2`
`~/.hermes/skills/`
`ctx.register_skill()`

### Gate on environment variables​

If your plugin needs an API key:

```
# plugin.yaml — simple format (backwards-compatible)requires_env:  - WEATHER_API_KEY
```

IfWEATHER_API_KEYisn't set, the plugin is disabled with a clear message. No crash, no error in the agent — just "Plugin weather disabled (missing: WEATHER_API_KEY)".

`WEATHER_API_KEY`

When users runhermes plugins install, they'reprompted interactivelyfor any missingrequires_envvariables. Values are saved to.envautomatically.

`hermes plugins install`
`requires_env`
`.env`

For a better install experience, use the rich format with descriptions and signup URLs:

```
# plugin.yaml — rich formatrequires_env:  - name: WEATHER_API_KEY    description: "API key for OpenWeather"    url: "https://openweathermap.org/api"    secret: true
```

| Field | Required | Description |
| --- | --- | --- |
| name | Yes | Environment variable name |
| description | No | Shown to user during install prompt |
| url | No | Where to get the credential |
| secret | No | Iftrue, input is hidden (like a password field) |

`name`
`description`
`url`
`secret`
`true`

Both formats can be mixed in the same list. Already-set variables are skipped silently.

### Lazy-install optional Python dependencies​

If your plugin wraps an SDK that not every user will have installed (a vendor SDK, a heavy ML lib, a platform-specific package), don'timportit at the top of the module. Use thetools.lazy_deps.ensure(...)helper inside the tool handler — Hermes will install the package on first use, gated by the user'ssecurity.allow_lazy_installsconfig.

`import`
`tools.lazy_deps.ensure(...)`
`security.allow_lazy_installs`

```
# tools.pyfrom tools.lazy_deps import ensure, FeatureUnavailabledef my_tool_handler(args, **kwargs):    try:        ensure("my-plugin.my-backend")   # key must be in LAZY_DEPS    except FeatureUnavailable as exc:        return {"error": str(exc)}    import my_backend_sdk   # safe now    ...
```

Two rules from the security model intools/lazy_deps.py:

`tools/lazy_deps.py`
| Rule | Why |
| --- | --- |
| Your feature key must appear in the in-treeLAZY_DEPSallowlist | Prevents a malicious config from coaxing Hermes into installing arbitrary packages — only specs Hermes itself ships are eligible |
| Specs are PyPI-by-name only | No--index-url,git+https://, or file: paths. Pin versions with PEP 440 ("my-sdk>=1.2,<2") inside the allowlist entry |

`LAZY_DEPS`
`--index-url`
`git+https://`
`"my-sdk>=1.2,<2"`

For third-party plugins distributed via pip, declare the optional deps as[project.optional-dependencies]extras in your ownpyproject.tomland tell users topip install your-plugin[backend]— that path doesn't go throughlazy_deps. The lazy-install dance is most useful forbundledplugins where shipping a hard dependency on every install would bloat the base Hermes footprint.

`[project.optional-dependencies]`
`pyproject.toml`
`pip install your-plugin[backend]`
`lazy_deps`

Whensecurity.allow_lazy_installs: falseis set globally,ensure()raisesFeatureUnavailableimmediately with a remediation hint — your plugin should catch it and degrade gracefully (return an error result, not crash the tool loop).

`security.allow_lazy_installs: false`
`ensure()`
`FeatureUnavailable`

### Thread-safe lazy singletons​

Plugins often cache an expensive object — an SDK client, an HTTP session, a connection pool — in a module-level variable built on first use:

```
_client = Nonedef get_client():    global _client    if _client is not None:        return _client    _client = ExpensiveClient(...)   # ← TOCTOU race    return _client
```

This is a footgun. Hermes runs multiple threads in one process (delegated tool calls, background workers, the self-improvement fork), so two threads can hitget_client()before_clientis set,bothpass theis not Nonecheck,bothrun the expensive build, and the second write clobbers the first — leaking whatever resource the loser opened (connection, file handle, background thread).

`get_client()`
`_client`
`is not None`

Don't hand-roll the lock. Use the helpers inplugins/plugin_utils.py:

`plugins/plugin_utils.py`

```
from plugins.plugin_utils import lazy_singleton, SingletonSlot# Zero-arg accessor → decorate it:@lazy_singletondef get_client():    return ExpensiveClient(load_config())   # runs exactly onceclient = get_client()    # safe across threadsget_client.reset()       # drop the instance (tests / teardown)# Accessor that takes a build argument → use a slot:_slot: SingletonSlot = SingletonSlot()def get_client(config=None):    return _slot.get(lambda: ExpensiveClient(resolve(config)))def reset_client():    _slot.reset()
```

Both serialize concurrent first calls with double-checked locking and run the factory at most once. If the factory raises, nothing is cached and the next call retries. The honcho memory plugin (plugins/memory/honcho/client.py) is the reference consumer.

`plugins/memory/honcho/client.py`

> Rule of thumb: any time you writeglobal _somethingfollowed by ais Nonecheck and a build, reach for one of these instead.

Rule of thumb: any time you writeglobal _somethingfollowed by ais Nonecheck and a build, reach for one of these instead.

`global _something`
`is None`

### Conditional tool availability​

For tools that depend on optional libraries:

```
ctx.register_tool(    name="my_tool",    schema={...},    handler=my_handler,    check_fn=lambda: _has_optional_lib(),  # False = tool hidden from model)
```

### Overriding a built-in tool​

To replace a built-in tool with your own implementation (e.g. swap the
default browser tool for a headed-Chrome CDP backend, or replaceweb_searchwith a custom corporate index), passoverride=True:

`web_search`
`override=True`

```
def register(ctx):    ctx.register_tool(        name="browser_navigate",             # same name as the built-in        toolset="plugin_my_browser",         # your own toolset namespace        schema={...},        handler=my_custom_navigate,        override=True,                       # explicit opt-in    )
```

Withoutoverride=True, the registry rejects any registration that would
shadow an existing tool from a different toolset — this prevents
accidental overwrites. The override is logged at INFO level so it's
auditable in~/.hermes/logs/agent.log. Plugins load after built-in
tools, so the registration order is correct: your handler replaces the
built-in one.

`override=True`
`~/.hermes/logs/agent.log`

### Register multiple hooks​

```
def register(ctx):    ctx.register_hook("pre_tool_call", before_any_tool)    ctx.register_hook("post_tool_call", after_any_tool)    ctx.register_hook("pre_llm_call", inject_memory)    ctx.register_hook("on_session_start", on_new_session)    ctx.register_hook("on_session_end", on_session_end)
```

### Hook reference​

Each hook is documented in full on theEvent Hooks reference— callback signatures, parameter tables, exactly when each fires, and examples. Here's the summary:

| Hook | Fires when | Callback signature | Returns |
| --- | --- | --- | --- |
| pre_tool_call | Before any tool executes | tool_name: str, args: dict, task_id: str | ignored |
| post_tool_call | After any tool returns | tool_name: str, args: dict, result: str, task_id: str, duration_ms: int | ignored |
| pre_llm_call | Once per turn, before the tool-calling loop | session_id: str, user_message: str, conversation_history: list, is_first_turn: bool, model: str, platform: str | context injection |
| post_llm_call | Once per turn, after the tool-calling loop (successful turns only) | session_id: str, user_message: str, assistant_response: str, conversation_history: list, model: str, platform: str | ignored |
| on_session_start | New session created (first turn only) | session_id: str, model: str, platform: str | ignored |
| on_session_end | End of everyrun_conversationcall + CLI exit | session_id: str, completed: bool, interrupted: bool, model: str, platform: str | ignored |
| on_session_finalize | CLI/gateway tears down an active session | session_id: str | None, platform: str | ignored |
| on_session_reset | Gateway swaps in a new session key (/new,/reset) | session_id: str, platform: str | ignored |
| kanban_task_claimed | A kanban task is claimed (dispatcher process, before the worker spawns) | task_id: str, board: str | None, assignee: str | None, run_id: int | None, profile_name: str | ignored |
| kanban_task_completed | A kanban task completes (worker process) | task_id, board, assignee, run_id, profile_name, summary: str | None | ignored |
| kanban_task_blocked | A kanban task is blocked (worker process) | task_id, board, assignee, run_id, profile_name, reason: str | None | ignored |

`pre_tool_call`
`tool_name: str, args: dict, task_id: str`
`post_tool_call`
`tool_name: str, args: dict, result: str, task_id: str, duration_ms: int`
`pre_llm_call`
`session_id: str, user_message: str, conversation_history: list, is_first_turn: bool, model: str, platform: str`
`post_llm_call`
`session_id: str, user_message: str, assistant_response: str, conversation_history: list, model: str, platform: str`
`on_session_start`
`session_id: str, model: str, platform: str`
`on_session_end`
`run_conversation`
`session_id: str, completed: bool, interrupted: bool, model: str, platform: str`
`on_session_finalize`
`session_id: str | None, platform: str`
`on_session_reset`
`/new`
`/reset`
`session_id: str, platform: str`
`kanban_task_claimed`
`task_id: str, board: str | None, assignee: str | None, run_id: int | None, profile_name: str`
`kanban_task_completed`
`task_id, board, assignee, run_id, profile_name, summary: str | None`
`kanban_task_blocked`
`task_id, board, assignee, run_id, profile_name, reason: str | None`

Most hooks are fire-and-forget observers — their return values are ignored. The exception ispre_llm_call, which can inject context into the conversation.

`pre_llm_call`

All callbacks should accept**kwargsfor forward compatibility. If a hook callback crashes, it's logged and skipped. Other hooks and the agent continue normally.

`**kwargs`

The kanban lifecycle hooks fireafterthe board DB change commits, so a callback always sees durable state and can never hold the SQLite write lock. Because kanban workers run as separatehermes -p <profile> chat -qsubprocesses,kanban_task_claimedfires in thedispatcherprocess whilekanban_task_completed/kanban_task_blockedfire in theworkerprocess — hook in the dispatcher to observe every transition centrally, or in the worker for per-task in-session context.

`hermes -p <profile> chat -q`
`kanban_task_claimed`
`kanban_task_completed`
`kanban_task_blocked`

### pre_llm_callcontext injection​

`pre_llm_call`

This is the only hook whose return value matters. When apre_llm_callcallback returns a dict with a"context"key (or a plain string), Hermes injects that text into thecurrent turn's user message. This is the mechanism for memory plugins, RAG integrations, guardrails, and any plugin that needs to provide the model with additional context.

`pre_llm_call`
`"context"`

#### Return format​

```
# Dict with context keyreturn {"context": "Recalled memories:\n- User prefers dark mode\n- Last project: hermes-agent"}# Plain string (equivalent to the dict form above)return "Recalled memories:\n- User prefers dark mode"# Return None or don't return → no injection (observer-only)return None
```

Any non-None, non-empty return with a"context"key (or a plain non-empty string) is collected and appended to the user message for the current turn.

`"context"`

#### Oversized-context spill​

Per-hook context is capped at10,000characters by default. Anything above the cap is written to$HERMES_HOME/hook_outputs/<session_id>/<uuid>.txtand replaced with a head/tail preview plus the saved path. The model can read the full content viaread_fileorterminalif it genuinely needs it. This keeps a runaway plugin from inflating every subsequent turn's prompt and blowing out the prompt cache prefix. Tune inconfig.yaml:

`10,000`
`$HERMES_HOME/hook_outputs/<session_id>/<uuid>.txt`
`read_file`
`terminal`
`config.yaml`

```
hooks:  output_spill:    enabled: true          # default: true    max_chars: 10000       # default; set higher to opt out of spilling    preview_head: 500      # chars shown at the top of the preview    preview_tail: 500      # chars shown at the bottom of the preview    # directory: null      # default: $HERMES_HOME/hook_outputs
```

#### How injection works​

Injected context is appended to theuser message, not the system prompt. This is a deliberate design choice:

- Prompt cache preservation— the system prompt stays identical across turns. Anthropic and OpenRouter cache the system prompt prefix, so keeping it stable saves 75%+ on input tokens in multi-turn conversations. If plugins modified the system prompt, every turn would be a cache miss.
- Ephemeral— the injection happens at API call time only. The original user message in the conversation history is never mutated, and nothing is persisted to the session database.
- The system prompt is Hermes's territory— it contains model-specific guidance, tool enforcement rules, personality instructions, and cached skill content. Plugins contribute context alongside the user's input, not by altering the agent's core instructions.

#### Example: Memory recall plugin​

```
"""Memory plugin — recalls relevant context from a vector store."""import httpxMEMORY_API = "https://your-memory-api.example.com"def recall_context(session_id, user_message, is_first_turn, **kwargs):    """Called before each LLM turn. Returns recalled memories."""    try:        resp = httpx.post(f"{MEMORY_API}/recall", json={            "session_id": session_id,            "query": user_message,        }, timeout=3)        memories = resp.json().get("results", [])        if not memories:            return None  # nothing to inject        text = "Recalled context from previous sessions:\n"        text += "\n".join(f"- {m['text']}" for m in memories)        return {"context": text}    except Exception:        return None  # fail silently, don't break the agentdef register(ctx):    ctx.register_hook("pre_llm_call", recall_context)
```

#### Example: Guardrails plugin​

```
"""Guardrails plugin — enforces content policies."""POLICY = """You MUST follow these content policies for this session:- Never generate code that accesses the filesystem outside the working directory- Always warn before executing destructive operations- Refuse requests involving personal data extraction"""def inject_guardrails(**kwargs):    """Injects policy text into every turn."""    return {"context": POLICY}def register(ctx):    ctx.register_hook("pre_llm_call", inject_guardrails)
```

#### Example: Observer-only hook (no injection)​

```
"""Analytics plugin — tracks turn metadata without injecting context."""import logginglogger = logging.getLogger(__name__)def log_turn(session_id, user_message, model, is_first_turn, **kwargs):    """Fires before each LLM call. Returns None — no context injected."""    logger.info("Turn: session=%s model=%s first=%s msg_len=%d",                session_id, model, is_first_turn, len(user_message or ""))    # No return → no injectiondef register(ctx):    ctx.register_hook("pre_llm_call", log_turn)
```

#### Multiple plugins returning context​

When multiple plugins return context frompre_llm_call, their outputs are joined with double newlines and appended to the user message together. The order follows plugin discovery order (alphabetical by plugin directory name).

`pre_llm_call`

### Register CLI commands​

Plugins can add their ownhermes <plugin>subcommand tree:

`hermes <plugin>`

```
def _my_command(args):    """Handler for hermes my-plugin <subcommand>."""    sub = getattr(args, "my_command", None)    if sub == "status":        print("All good!")    elif sub == "config":        print("Current config: ...")    else:        print("Usage: hermes my-plugin <status|config>")def _setup_argparse(subparser):    """Build the argparse tree for hermes my-plugin."""    subs = subparser.add_subparsers(dest="my_command")    subs.add_parser("status", help="Show plugin status")    subs.add_parser("config", help="Show plugin config")    subparser.set_defaults(func=_my_command)def register(ctx):    ctx.register_tool(...)    ctx.register_cli_command(        name="my-plugin",        help="Manage my plugin",        setup_fn=_setup_argparse,        handler_fn=_my_command,    )
```

After registration, users can runhermes my-plugin status,hermes my-plugin config, etc.

`hermes my-plugin status`
`hermes my-plugin config`

Memory provider pluginsuse a convention-based approach instead: add aregister_cli(subparser)function to your plugin'scli.pyfile. The memory plugin discovery system finds it automatically — noctx.register_cli_command()call needed. See theMemory Provider Plugin guidefor details.

`register_cli(subparser)`
`cli.py`
`ctx.register_cli_command()`

Active-provider gating:Memory plugin CLI commands only appear when their provider is the activememory.providerin config. If a user hasn't set up your provider, your CLI commands won't clutter the help output.

`memory.provider`

### Register slash commands​

Plugins can register in-session slash commands — commands users type during a conversation (like/lcm statusor/ping). These work in both CLI and gateway (Telegram, Discord, etc.).

`/lcm status`
`/ping`

```
def _handle_status(raw_args: str) -> str:    """Handler for /mystatus — called with everything after the command name."""    if raw_args.strip() == "help":        return "Usage: /mystatus [help|check]"    return "Plugin status: all systems nominal"def register(ctx):    ctx.register_command(        "mystatus",        handler=_handle_status,        description="Show plugin status",    )
```

After registration, users can type/mystatusin any session. The command appears in autocomplete,/helpoutput, and the Telegram bot menu.

`/mystatus`
`/help`

Signature:ctx.register_command(name: str, handler: Callable, description: str = "", args_hint: str = "")

`ctx.register_command(name: str, handler: Callable, description: str = "", args_hint: str = "")`
| Parameter | Type | Description |
| --- | --- | --- |
| name | str | Command name without the leading slash (e.g."lcm","mystatus") |
| handler | Callable[[str], str | None] | Called with the raw argument string. May also beasync. |
| description | str | Shown in/help, autocomplete, and Telegram bot menu |

`name`
`str`
`"lcm"`
`"mystatus"`
`handler`
`Callable[[str], str | None]`
`async`
`description`
`str`
`/help`

Key differences fromregister_cli_command():

`register_cli_command()`
|  | register_command() | register_cli_command() |
| --- | --- | --- |
| Invoked as | /namein a session | hermes namein a terminal |
| Where it works | CLI sessions, Telegram, Discord, etc. | Terminal only |
| Handler receives | Raw args string | argparseNamespace |
| Use case | Diagnostics, status, quick actions | Complex subcommand trees, setup wizards |

`register_command()`
`register_cli_command()`
`/name`
`hermes name`
`Namespace`

Conflict protection:If a plugin tries to register a name that conflicts with a built-in command (help,model,new, etc.), the registration is silently rejected with a log warning. Built-in commands always take precedence.

`help`
`model`
`new`

Async handlers:The gateway dispatch automatically detects and awaits async handlers, so you can use either sync or async functions:

```
async def _handle_check(raw_args: str) -> str:    result = await some_async_operation()    return f"Check result: {result}"def register(ctx):    ctx.register_command("check", handler=_handle_check, description="Run async check")
```

### Dispatch tools from slash commands​

Slash command handlers that need to orchestrate tools (spawn a subagent viadelegate_task, callfile_edit, etc.) should usectx.dispatch_tool()instead of reaching into framework internals. The parent-agent context (workspace hints, spinner, model inheritance) is wired up automatically.

`delegate_task`
`file_edit`
`ctx.dispatch_tool()`

```
def register(ctx):    def _handle_deliver(raw_args: str):        result = ctx.dispatch_tool(            "delegate_task",            {                "goal": raw_args,                "toolsets": ["terminal", "file", "web"],            },        )        return result    ctx.register_command(        "deliver",        handler=_handle_deliver,        description="Delegate a goal to a subagent",    )
```

Signature:ctx.dispatch_tool(name: str, args: dict, *, parent_agent=None) -> str

`ctx.dispatch_tool(name: str, args: dict, *, parent_agent=None) -> str`
| Parameter | Type | Description |
| --- | --- | --- |
| name | str | Tool name as registered in the tool registry (e.g."delegate_task","file_edit") |
| args | dict | Tool arguments, same shape the model would send |
| parent_agent | Agent | None | Optional override. When omitted, resolves from the current CLI agent (or degrades gracefully in gateway mode) |

`name`
`str`
`"delegate_task"`
`"file_edit"`
`args`
`dict`
`parent_agent`
`Agent | None`

Runtime behavior:

- CLI mode:parent_agentis resolved from the active CLI agent so workspace hints, spinner, and model selection inherit as expected.
- Gateway mode:There is no CLI agent, so tools degrade gracefully — workspace is read from the configured terminal working directory and no spinner is shown.
- Explicit override:If the caller passesparent_agent=explicitly, it is respected and not overwritten.

`parent_agent`
`parent_agent=`

This is the public, stable interface for tool dispatch from plugin commands. Plugins should not reach intoctx._cli_ref.agentor similar private state.

`ctx._cli_ref.agent`

### Act from inside a hook (profile + tools)​

ctx._cli_refis only populated in aninteractive CLIsession. It isNonein the gateway, in non-interactivehermes chat -qruns, and inkanban-spawned worker sessions— so any plugin logic that reaches through_cli_refsilently no-ops in exactly those contexts. Two stable, session-agnostic APIs cover what hooks actually need:

`ctx._cli_ref`
`None`
`hermes chat -q`
`_cli_ref`
- ctx.profile_name— the active profile name (e.g."default", or the assignee profile in a kanban worker). Derived fromHERMES_HOME, so it works everywhere with no_cli_refdependency.
- ctx.dispatch_tool(name, args)— invoke any registered tool (built-in or plugin), including thekanban_*tools,delegate_task,terminal,read_file, etc. Works from hook callbacks regardless of which process the hook fires in.

`ctx.profile_name`
`"default"`
`HERMES_HOME`
`_cli_ref`
`ctx.dispatch_tool(name, args)`
`kanban_*`
`delegate_task`
`terminal`
`read_file`

Together these let a kanban lifecycle hook observe a transition and act on the board without touching framework internals:

```
def register(ctx):    def on_blocked(*, task_id, reason=None, **kw):        # Runs in the worker process; ctx._cli_ref is None here.        ctx.dispatch_tool("kanban_comment", {            "task_id": task_id,            "comment": f"[{ctx.profile_name}] auto-noted block: {reason}",        })    ctx.register_hook("kanban_task_blocked", on_blocked)
```

For running a fullhermes <subcommand>(e.g.hermes kanban show), shell out with theterminaltool viactx.dispatch_tool("terminal", {"command": "hermes kanban show ..."})— there is no in-process slash-command bridge for headless worker sessions, and tools are the supported way to drive Hermes from a hook.

`hermes <subcommand>`
`hermes kanban show`
`terminal`
`ctx.dispatch_tool("terminal", {"command": "hermes kanban show ..."})`

### Handle Slack Block Kit button clicks​

Plugins that post Block Kit messages with interactive elements (buttons, overflow menus, datepickers, etc.) can register the click handlers directly with the Slack adapter — no monkey-patching ofslack_bolt.AsyncApprequired.

`slack_bolt.AsyncApp`

```
def register(ctx):    async def _on_approve(ack, body, action):        # ack within 3 seconds — slack_bolt requirement.        await ack()        # body["channel"]["id"], body["user"]["id"], body["message"]["ts"]        # action["action_id"], action["value"]        sweep_id = (action.get("value") or "").split("|", 1)[-1]        # ...do the deterministic work, then post a follow-up.    ctx.register_slack_action_handler("inbox_sweep_approve", _on_approve)
```

Signature:ctx.register_slack_action_handler(action_id, callback) -> None

`ctx.register_slack_action_handler(action_id, callback) -> None`
| Parameter | Type | Description |
| --- | --- | --- |
| action_id | str | re.Pattern | dict | Whateverslack_bolt.App.action()accepts: a literalaction_id, a compiled regex matching multiple ids, or a constraint dict like{"action_id": "...", "block_id": "..."} |
| callback | async callable | Receives(ack, body, action)per the slack_bolt convention |

`action_id`
`str | re.Pattern | dict`
`slack_bolt.App.action()`
`action_id`
`{"action_id": "...", "block_id": "..."}`
`callback`
`(ack, body, action)`

Runtime behavior:

- The handler is queued at plugin-load time and wired into the adapter'sslack_bolt.AsyncAppwhen the Slack platform connects.
- Each callback is wrapped defensively: if your handler raises, the gateway logs the error and best-effort-acks the click so Slack stops retrying.
- Standard slack_bolt rules apply —await ack()within 3 seconds, then do longer work.
- For multi-workspace deployments the handler fires for clicks from any connected workspace; usebody["team"]["id"]if you need to scope behaviour.

`slack_bolt.AsyncApp`
`await ack()`
`body["team"]["id"]`

This is the public way for plugins to participate in Slack interactivity. Older plugins may patchSlackAdapter.connect; prefer this API instead.

`SlackAdapter.connect`

This guide coversgeneral plugins(tools, hooks, slash commands, CLI commands). The sections below sketch the authoring pattern for each specialized plugin type; each links to its full guide for field reference and examples.

## Specialized plugin types​

Hermes has five specialized plugin types beyond the general surface. Each ships as a directory underplugins/<category>/<name>/(bundled) or~/.hermes/plugins/<category>/<name>/(user). The contract differs by category — pick the one you need, then read its full guide.

`plugins/<category>/<name>/`
`~/.hermes/plugins/<category>/<name>/`

### Model provider plugins — add an LLM backend​

Drop a profile intoplugins/model-providers/<name>/:

`plugins/model-providers/<name>/`

```
# plugins/model-providers/acme/__init__.pyfrom providers import register_providerfrom providers.base import ProviderProfileregister_provider(ProviderProfile(    name="acme",    aliases=("acme-inference",),    display_name="Acme Inference",    env_vars=("ACME_API_KEY", "ACME_BASE_URL"),    base_url="https://api.acme.example.com/v1",    auth_type="api_key",    default_aux_model="acme-small-fast",    fallback_models=("acme-large-v3", "acme-medium-v3"),))
```

```
# plugins/model-providers/acme/plugin.yamlname: acme-providerkind: model-providerversion: 1.0.0description: Acme Inference — OpenAI-compatible direct API
```

Lazy-discovered the first time anything callsget_provider_profile()orlist_providers()—auth.py,config.py,doctor.py,models.py,runtime_provider.py, and the chat_completions transport auto-wire to it. User plugins override bundled ones by name.

`get_provider_profile()`
`list_providers()`
`auth.py`
`config.py`
`doctor.py`
`models.py`
`runtime_provider.py`

Full guide:Model Provider Plugins— field reference, overridable hooks (prepare_messages,build_extra_body,build_api_kwargs_extras,fetch_models), api_mode selection, auth types, testing.

`prepare_messages`
`build_extra_body`
`build_api_kwargs_extras`
`fetch_models`

### Platform plugins — add a gateway channel​

Drop an adapter intoplugins/platforms/<name>/:

`plugins/platforms/<name>/`

```
# plugins/platforms/myplatform/adapter.pyfrom gateway.platforms.base import BasePlatformAdapterclass MyPlatformAdapter(BasePlatformAdapter):    async def connect(self): ...    async def send(self, chat_id, text): ...    async def disconnect(self): ...def check_requirements():    import os    return bool(os.environ.get("MYPLATFORM_TOKEN"))def _env_enablement():    import os    tok = os.getenv("MYPLATFORM_TOKEN", "").strip()    if not tok:        return None    return {"token": tok}def register(ctx):    ctx.register_platform(        name="myplatform",        label="MyPlatform",        adapter_factory=lambda cfg: MyPlatformAdapter(cfg),        check_fn=check_requirements,        required_env=["MYPLATFORM_TOKEN"],        # Auto-populate PlatformConfig.extra from env so env-only setups        # show up in `hermes gateway status` without SDK instantiation.        env_enablement_fn=_env_enablement,        # Opt in to cron delivery: `deliver=myplatform` routes to this var.        cron_deliver_env_var="MYPLATFORM_HOME_CHANNEL",        emoji="💬",        platform_hint="You are chatting via MyPlatform. Keep responses concise.",    )
```

```
# plugins/platforms/myplatform/plugin.yamlname: myplatform-platformlabel: MyPlatformkind: platformversion: 1.0.0description: MyPlatform gateway adapterrequires_env:  - name: MYPLATFORM_TOKEN    description: "Bot token from the MyPlatform console"    password: trueoptional_env:  - name: MYPLATFORM_HOME_CHANNEL    description: "Default channel for cron delivery"    password: false
```

Full guide:Adding Platform Adapters— completeBasePlatformAdaptercontract, message routing, auth gating, setup wizard integration. Look atplugins/platforms/irc/for a stdlib-only working example.

`BasePlatformAdapter`
`plugins/platforms/irc/`

### Memory provider plugins — add a cross-session knowledge backend​

Drop an implementation ofMemoryProviderintoplugins/memory/<name>/:

`MemoryProvider`
`plugins/memory/<name>/`

```
# plugins/memory/my-memory/__init__.pyfrom agent.memory_provider import MemoryProviderclass MyMemoryProvider(MemoryProvider):    @property    def name(self) -> str:        return "my-memory"    def is_available(self) -> bool:        import os        return bool(os.environ.get("MY_MEMORY_API_KEY"))    def initialize(self, session_id: str, **kwargs) -> None:        self._session_id = session_id    def sync_turn(self, user_content, assistant_content, *,                  session_id="", messages=None) -> None:        ...    def prefetch(self, query, *, session_id="") -> str:        ...    def get_tool_schemas(self) -> list[dict]:        return []   # required @abstractmethod — see full guidedef register(ctx):    ctx.register_memory_provider(MyMemoryProvider())
```

Memory providers are single-select — only one is active at a time, chosen viamemory.providerinconfig.yaml.

`memory.provider`
`config.yaml`

Full guide:Memory Provider Plugins— fullMemoryProviderABC, threading contract, profile isolation, CLI command registration viacli.py.

`MemoryProvider`
`cli.py`

### Context engine plugins — replace the context compressor​

```
# plugins/context_engine/my-engine/__init__.pyfrom agent.context_engine import ContextEngineclass MyContextEngine(ContextEngine):    @property    def name(self) -> str:        return "my-engine"    def update_from_response(self, usage) -> None: ...    def should_compress(self, prompt_tokens: int = None) -> bool: ...    def compress(self, messages, current_tokens=None, focus_topic=None) -> list: ...def register(ctx):    ctx.register_context_engine(MyContextEngine())
```

Context engines are single-select — chosen viacontext.engineinconfig.yaml.

`context.engine`
`config.yaml`

Full guide:Context Engine Plugins.

### Image-generation backends​

Drop a provider intoplugins/image_gen/<name>/:

`plugins/image_gen/<name>/`

```
# plugins/image_gen/my-imggen/__init__.pyfrom agent.image_gen_provider import ImageGenProviderclass MyImageGenProvider(ImageGenProvider):    @property    def name(self) -> str:        return "my-imggen"    def is_available(self) -> bool: ...    def generate(self, prompt: str, aspect_ratio="landscape", **kwargs) -> dict:        # returns success_response(...) / error_response(...)        ...def register(ctx):    ctx.register_image_gen_provider(MyImageGenProvider())
```

```
# plugins/image_gen/my-imggen/plugin.yamlname: my-imggenkind: backendversion: 1.0.0description: Custom image generation backend
```

Full guide:Image Generation Provider Plugins— fullImageGenProviderABC,list_models()/get_setup_schema()metadata,success_response()/error_response()helpers, base64 vs URL output, user overrides, pip distribution.

`ImageGenProvider`
`list_models()`
`get_setup_schema()`
`success_response()`
`error_response()`

Reference examples:plugins/image_gen/openai/(DALL-E / GPT-Image via OpenAI SDK),plugins/image_gen/openai-codex/,plugins/image_gen/xai/(Grok image gen).

`plugins/image_gen/openai/`
`plugins/image_gen/openai-codex/`
`plugins/image_gen/xai/`

## Non-Python extension surfaces​

Hermes also accepts extensions that aren't Python plugins at all. These are shown in thePluggable interfaces table; the sections below sketch each authoring style briefly.

### MCP servers — register external tools​

Model Context Protocol (MCP) servers register their own tools into Hermes without any Python plugin. Declare them in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
mcp_servers:  filesystem:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]    timeout: 120  linear:    url: "https://mcp.linear.app/sse"    auth:      type: "oauth"
```

Hermes connects to each server at startup, lists its tools, and registers them alongside built-ins. The LLM sees them exactly like any other tool.Full guide:MCP.

### Gateway event hooks — fire on lifecycle events​

Drop a manifest + handler into~/.hermes/hooks/<name>/:

`~/.hermes/hooks/<name>/`

```
# ~/.hermes/hooks/long-task-alert/HOOK.yamlname: long-task-alertdescription: Send a push notification when a long task finishesevents:  - agent:end
```

```
# ~/.hermes/hooks/long-task-alert/handler.pyasync def handle(event_type: str, context: dict) -> None:    if context.get("duration_seconds", 0) > 120:        # send notification …        pass
```

Events includegateway:startup,session:start,session:end,session:reset,agent:start,agent:step,agent:end, and wildcardcommand:*. Errors in hooks are caught and logged — they never block the main pipeline.

`gateway:startup`
`session:start`
`session:end`
`session:reset`
`agent:start`
`agent:step`
`agent:end`
`command:*`

Full guide:Gateway Event Hooks.

### Shell hooks — run a shell command on tool calls​

If you just want to run a script when a tool fires (notifications, audit logs, desktop alerts, auto-formatters), use shell hooks inconfig.yaml— no Python required:

`config.yaml`

```
hooks:  - event: post_tool_call    command: "notify-send 'Tool ran: {tool_name}'"    when:      tools: [terminal, patch, write_file]
```

Supports all the same events as Python plugin hooks (pre_tool_call,post_tool_call,pre_llm_call,post_llm_call,on_session_start,on_session_end,pre_gateway_dispatch) plus structured JSON output forpre_tool_callblocking decisions.

`pre_tool_call`
`post_tool_call`
`pre_llm_call`
`post_llm_call`
`on_session_start`
`on_session_end`
`pre_gateway_dispatch`
`pre_tool_call`

Full guide:Shell Hooks.

### Skill sources — add a custom skill registry​

If you maintain a GitHub repo of skills (or want to pull from a community index beyond the built-in sources), add it as atap:

```
hermes skills tap add myorg/skills-repohermes skills search my-workflow --source myorg/skills-repohermes skills install myorg/skills-repo/my-workflow
```

Publishing your own tap is just a GitHub repo withskills/<skill-name>/SKILL.mddirectories — no server or registry signup needed.

`skills/<skill-name>/SKILL.md`

Full guides:Skills Hub·Publishing a custom tap(repo layout, minimal example, non-default paths, trust levels).

### TTS / STT via command templates​

Any CLI that reads/writes audio or text can be plugged in throughconfig.yaml— no Python code:

`config.yaml`

```
tts:  provider: voxcpm  providers:    voxcpm:      type: command      command: "voxcpm --ref ~/voice.wav --text-file {input_path} --out {output_path}"      output_format: mp3      voice_compatible: true
```

For STT, pointHERMES_LOCAL_STT_COMMANDat a shell template. Supported placeholders:{input_path},{output_path},{format},{voice},{model},{speed}(TTS);{input_path},{output_dir},{language},{model}(STT). Any path-interacting CLI is automatically a plugin.

`HERMES_LOCAL_STT_COMMAND`
`{input_path}`
`{output_path}`
`{format}`
`{voice}`
`{model}`
`{speed}`
`{input_path}`
`{output_dir}`
`{language}`
`{model}`

Full guides:TTS custom command providers·STT.

## Distribute via pip​

For sharing plugins publicly, add an entry point to your Python package:

```
# pyproject.toml[project.entry-points."hermes_agent.plugins"]my-plugin = "my_plugin_package"
```

```
pip install hermes-plugin-calculator# Plugin auto-discovered on next hermes startup
```

## Distribute for NixOS​

Nix/NixOS is no longer an explicitly supported install path (best-effort only) — seeNix Setup. This section is kept for users already deploying on NixOS.

NixOS users can install your plugin declaratively if you provide apyproject.tomlwith entry points:

`pyproject.toml`

Entry-point plugins(recommended for distribution):

```
# User's configuration.nixservices.hermes-agent.extraPythonPackages = [  (pkgs.python312Packages.buildPythonPackage {    pname = "my-plugin";    version = "1.0.0";    src = pkgs.fetchFromGitHub {      owner = "you";      repo = "hermes-my-plugin";      rev = "v1.0.0";      hash = "sha256-...";  # nix-prefetch-url --unpack    };    format = "pyproject";    build-system = [ pkgs.python312Packages.setuptools ];  })];
```

Directory plugins(nopyproject.tomlneeded):

`pyproject.toml`

```
services.hermes-agent.extraPlugins = [  (pkgs.fetchFromGitHub {    owner = "you";    repo = "hermes-my-plugin";    rev = "v1.0.0";    hash = "sha256-...";  })];
```

See theNix Setup guidefor complete documentation including overlay usage and collision checking.

## Common mistakes​

Handler doesn't return JSON string:

```
# Wrong — returns a dictdef handler(args, **kwargs):    return {"result": 42}# Right — returns a JSON stringdef handler(args, **kwargs):    return json.dumps({"result": 42})
```

Missing**kwargsin handler signature:

`**kwargs`

```
# Wrong — will break if Hermes passes extra contextdef handler(args):    ...# Rightdef handler(args, **kwargs):    ...
```

Handler raises exceptions:

```
# Wrong — exception propagates, tool call failsdef handler(args, **kwargs):    result = 1 / int(args["value"])  # ZeroDivisionError!    return json.dumps({"result": result})# Right — catch and return error JSONdef handler(args, **kwargs):    try:        result = 1 / int(args.get("value", 0))        return json.dumps({"result": result})    except Exception as e:        return json.dumps({"error": str(e)})
```

Schema description too vague:

```
# Bad — model doesn't know when to use it"description": "Does stuff"# Good — model knows exactly when and how"description": "Evaluate a mathematical expression. Use for arithmetic, trig, logarithms. Supports: +, -, *, /, **, sqrt, sin, cos, log, pi, e."
```