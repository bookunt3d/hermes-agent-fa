- 
- Developer Guide
- Extending
- Adding Tools

# Adding Tools

Before writing a tool, ask yourself:should this be askillinstead?

This page is for adding abuilt-in Hermes toolto the repository itself.
If you want a personal, project-local, or otherwise custom tool without
modifying Hermes core, use the plugin route instead:

- Plugins
- Build a Hermes Plugin

Default to plugins for most custom tool creation. Only follow this page when
you explicitly want to ship a new built-in tool intools/andtoolsets.py.

`tools/`
`toolsets.py`

Make it aSkillwhen the capability can be expressed as instructions + shell commands + existing tools (arXiv search, git workflows, Docker management, PDF processing).

Make it aToolwhen it requires end-to-end integration with API keys, custom processing logic, binary data handling, or streaming (browser automation, TTS, vision analysis).

## Overview​

Adding a tool touches2 files:

1. tools/your_tool.py— handler, schema, check function,registry.register()call
2. toolsets.py— add tool name to_HERMES_CORE_TOOLS(or a specific toolset)

`tools/your_tool.py`
`registry.register()`
`toolsets.py`
`_HERMES_CORE_TOOLS`

Anytools/*.pyfile with a top-levelregistry.register()call is auto-discovered at startup — no manual import list required.

`tools/*.py`
`registry.register()`

## Step 1: Create the Built-in Tool File​

Every tool file follows the same structure:

```
# tools/weather_tool.py"""Weather Tool -- look up current weather for a location."""import jsonimport osimport logginglogger = logging.getLogger(__name__)# --- Availability check ---def check_weather_requirements() -> bool:    """Return True if the tool's dependencies are available."""    return bool(os.getenv("WEATHER_API_KEY"))# --- Handler ---def weather_tool(location: str, units: str = "metric") -> str:    """Fetch weather for a location. Returns JSON string."""    api_key = os.getenv("WEATHER_API_KEY")    if not api_key:        return json.dumps({"error": "WEATHER_API_KEY not configured"})    try:        # ... call weather API ...        return json.dumps({"location": location, "temp": 22, "units": units})    except Exception as e:        return json.dumps({"error": str(e)})# --- Schema ---WEATHER_SCHEMA = {    "name": "weather",    "description": "Get current weather for a location.",    "parameters": {        "type": "object",        "properties": {            "location": {                "type": "string",                "description": "City name or coordinates (e.g. 'London' or '51.5,-0.1')"            },            "units": {                "type": "string",                "enum": ["metric", "imperial"],                "description": "Temperature units (default: metric)",                "default": "metric"            }        },        "required": ["location"]    }}# --- Registration ---from tools.registry import registryregistry.register(    name="weather",    toolset="weather",    schema=WEATHER_SCHEMA,    handler=lambda args, **kw: weather_tool(        location=args.get("location", ""),        units=args.get("units", "metric")),    check_fn=check_weather_requirements,    requires_env=["WEATHER_API_KEY"],)
```

### Key Rules​

- HandlersMUSTreturn a JSON string (viajson.dumps()), never raw dicts
- ErrorsMUSTbe returned as{"error": "message"}, never raised as exceptions
- Thecheck_fnis called when building tool definitions — if it returnsFalse, the tool is silently excluded
- Thehandlerreceives(args: dict, **kwargs)whereargsis the LLM's tool call arguments

`json.dumps()`
`{"error": "message"}`
`check_fn`
`False`
`handler`
`(args: dict, **kwargs)`
`args`

## Step 2: Add the Built-in Tool to a Toolset​

Intoolsets.py, add the tool name:

`toolsets.py`

```
# If it should be available on all platforms (CLI + messaging):_HERMES_CORE_TOOLS = [    ...    "weather",  # <-- add here]# Or create a new standalone toolset:"weather": {    "description": "Weather lookup tools",    "tools": ["weather"],    "includes": []},
```

## Step 3: Add Discovery Import(No longer needed)​

Tool modules with a top-levelregistry.register()call are auto-discovered bydiscover_builtin_tools()intools/registry.py. No manual import list to maintain — just create your file intools/and it's picked up at startup.

`registry.register()`
`discover_builtin_tools()`
`tools/registry.py`
`tools/`

## Async Handlers​

If your handler needs async code, mark it withis_async=True:

`is_async=True`

```
async def weather_tool_async(location: str) -> str:    async with aiohttp.ClientSession() as session:        ...    return json.dumps(result)registry.register(    name="weather",    toolset="weather",    schema=WEATHER_SCHEMA,    handler=lambda args, **kw: weather_tool_async(args.get("location", "")),    check_fn=check_weather_requirements,    is_async=True,  # registry calls _run_async() automatically)
```

The registry handles async bridging transparently — you never callasyncio.run()yourself.

`asyncio.run()`

## Handlers That Need task_id​

Tools that manage per-session state receivetask_idvia**kwargs:

`task_id`
`**kwargs`

```
def _handle_weather(args, **kw):    task_id = kw.get("task_id")    return weather_tool(args.get("location", ""), task_id=task_id)registry.register(    name="weather",    ...    handler=_handle_weather,)
```

## Agent-Loop Intercepted Tools​

Some tools (todo,memory,session_search,delegate_task) need access to per-session agent state. These are intercepted byrun_agent.pybefore reaching the registry. The registry still holds their schemas, butdispatch()returns a fallback error if the intercept is bypassed.

`todo`
`memory`
`session_search`
`delegate_task`
`run_agent.py`
`dispatch()`

## Optional: Setup Wizard Integration​

If your tool requires an API key, add it tohermes_cli/config.py:

`hermes_cli/config.py`

```
OPTIONAL_ENV_VARS = {    ...    "WEATHER_API_KEY": {        "description": "Weather API key for weather lookup",        "prompt": "Weather API key",        "url": "https://weatherapi.com/",        "tools": ["weather"],        "password": True,    },}
```

## Checklist​

- Tool file created with handler, schema, check function, and registration
- Added to appropriate toolset intoolsets.py
- Confirmed this really should be a built-in/core tool and not a plugin
- Handler returns JSON strings, errors returned as{"error": "..."}
- Optional: API key added toOPTIONAL_ENV_VARSinhermes_cli/config.py
- Optional: Added totoolset_distributions.pyfor batch processing
- Tested withhermes chat -q "Use the weather tool for London"

`toolsets.py`
`{"error": "..."}`
`OPTIONAL_ENV_VARS`
`hermes_cli/config.py`
`toolset_distributions.py`
`hermes chat -q "Use the weather tool for London"`