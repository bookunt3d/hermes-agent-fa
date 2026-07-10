- 
- Developer Guide
- Internals
- Tools Runtime

# Tools Runtime

Hermes tools are self-registering functions grouped into toolsets and executed through a central registry/dispatch system.

Primary files:

- tools/registry.py
- model_tools.py
- toolsets.py
- tools/terminal_tool.py
- tools/environments/*

`tools/registry.py`
`model_tools.py`
`toolsets.py`
`tools/terminal_tool.py`
`tools/environments/*`

## Tool registration model​

Each tool module callsregistry.register(...)at import time.

`registry.register(...)`

model_tools.pyis responsible for importing/discovering tool modules and building the schema list used by the model.

`model_tools.py`

### Howregistry.register()works​

`registry.register()`

Every tool file intools/callsregistry.register()at module level to declare itself. The function signature is:

`tools/`
`registry.register()`

```
registry.register(    name="terminal",               # Unique tool name (used in API schemas)    toolset="terminal",            # Toolset this tool belongs to    schema={...},                  # OpenAI function-calling schema (description, parameters)    handler=handle_terminal,       # The function that executes when the tool is called    check_fn=check_terminal,       # Optional: returns True/False for availability    requires_env=["SOME_VAR"],     # Optional: env vars needed (for UI display)    is_async=False,                # Whether the handler is an async coroutine    description="Run commands",    # Human-readable description    emoji="💻",                    # Emoji for spinner/progress display)
```

Each call creates aToolEntrystored in the singletonToolRegistry._toolsdict keyed by tool name. If a name collision occurs across toolsets, a warning is logged and the later registration wins.

`ToolEntry`
`ToolRegistry._tools`

### Discovery:discover_builtin_tools()​

`discover_builtin_tools()`

Whenmodel_tools.pyis imported, it callsdiscover_builtin_tools()fromtools/registry.py. This function scans everytools/*.pyfile using AST parsing to find modules that contain top-levelregistry.register()calls, then imports them:

`model_tools.py`
`discover_builtin_tools()`
`tools/registry.py`
`tools/*.py`
`registry.register()`

```
# tools/registry.py (simplified)def discover_builtin_tools(tools_dir=None):    tools_path = Path(tools_dir) if tools_dir else Path(__file__).parent    for path in sorted(tools_path.glob("*.py")):        if path.name in {"__init__.py", "registry.py", "mcp_tool.py"}:            continue        if _module_registers_tools(path):  # AST check for top-level registry.register()            importlib.import_module(f"tools.{path.stem}")
```

This auto-discovery means new tool files are picked up automatically — no manual list to maintain. The AST check only matches top-levelregistry.register()calls (not calls inside functions), so helper modules intools/are not imported.

`registry.register()`
`tools/`

Each import triggers the module'sregistry.register()calls. Errors in optional tools (e.g., missingfal_clientfor image generation) are caught and logged — they don't prevent other tools from loading.

`registry.register()`
`fal_client`

After core tool discovery, MCP tools and plugin tools are also discovered:

1. MCP tools—tools.mcp_tool.discover_mcp_tools()reads MCP server config and registers tools from external servers.
2. Plugin tools—hermes_cli.plugins.discover_plugins()loads user/project/pip plugins that may register additional tools.

`tools.mcp_tool.discover_mcp_tools()`
`hermes_cli.plugins.discover_plugins()`

## Tool availability checking (check_fn)​

`check_fn`

Each tool can optionally provide acheck_fn— a callable that returnsTruewhen the tool is available andFalseotherwise. Typical checks include:

`check_fn`
`True`
`False`
- API key present— e.g.,lambda: bool(os.environ.get("SERP_API_KEY"))for web search
- Service running— e.g., checking if the Honcho server is configured
- Binary installed— e.g., verifyingplaywrightis available for browser tools

`lambda: bool(os.environ.get("SERP_API_KEY"))`
`playwright`

Whenregistry.get_definitions()builds the schema list for the model, it runs each tool'scheck_fn():

`registry.get_definitions()`
`check_fn()`

```
# Simplified from registry.pyif entry.check_fn:    try:        available = bool(entry.check_fn())    except Exception:        available = False   # Exceptions = unavailable    if not available:        continue            # Skip this tool entirely
```

Key behaviors:

- Check results arecached per-call— if multiple tools share the samecheck_fn, it only runs once.
- Exceptions incheck_fn()are treated as "unavailable" (fail-safe).
- Theis_toolset_available()method checks whether a toolset'scheck_fnpasses, used for UI display and toolset resolution.

`check_fn`
`check_fn()`
`is_toolset_available()`
`check_fn`

## Toolset resolution​

Toolsets are named bundles of tools. Hermes resolves them through:

- explicit enabled/disabled toolset lists
- platform presets (hermes-cli,hermes-telegram, etc.)
- dynamic MCP toolsets
- curated special-purpose sets likehermes-acp

`hermes-cli`
`hermes-telegram`
`hermes-acp`

### Howget_tool_definitions()filters tools​

`get_tool_definitions()`

The main entry point ismodel_tools.get_tool_definitions(enabled_toolsets, disabled_toolsets, quiet_mode):

`model_tools.get_tool_definitions(enabled_toolsets, disabled_toolsets, quiet_mode)`
1. Ifenabled_toolsetsis provided— only tools from those toolsets are included. Each toolset name is resolved viaresolve_toolset()which expands composite toolsets into individual tool names.
2. Ifdisabled_toolsetsis provided— start with ALL toolsets, then subtract the disabled ones.
3. If neither— include all known toolsets.
4. Registry filtering— the resolved tool name set is passed toregistry.get_definitions(), which appliescheck_fnfiltering and returns OpenAI-format schemas.
5. Dynamic schema patching— after filtering,execute_codeandbrowser_navigateschemas are dynamically adjusted to only reference tools that actually passed filtering (prevents model hallucination of unavailable tools).

Ifenabled_toolsetsis provided— only tools from those toolsets are included. Each toolset name is resolved viaresolve_toolset()which expands composite toolsets into individual tool names.

`enabled_toolsets`
`resolve_toolset()`

Ifdisabled_toolsetsis provided— start with ALL toolsets, then subtract the disabled ones.

`disabled_toolsets`

If neither— include all known toolsets.

Registry filtering— the resolved tool name set is passed toregistry.get_definitions(), which appliescheck_fnfiltering and returns OpenAI-format schemas.

`registry.get_definitions()`
`check_fn`

Dynamic schema patching— after filtering,execute_codeandbrowser_navigateschemas are dynamically adjusted to only reference tools that actually passed filtering (prevents model hallucination of unavailable tools).

`execute_code`
`browser_navigate`

### Legacy toolset names​

Old toolset names with_toolssuffixes (e.g.,web_tools,terminal_tools) are mapped to their modern tool names via_LEGACY_TOOLSET_MAPfor backward compatibility.

`_tools`
`web_tools`
`terminal_tools`
`_LEGACY_TOOLSET_MAP`

## Dispatch​

At runtime, tools are dispatched through the central registry, with agent-loop exceptions for some agent-level tools such as memory/todo/session-search handling.

### Dispatch flow: model tool_call → handler execution​

When the model returns atool_call, the flow is:

`tool_call`

```
Model response with tool_call    ↓run_agent.py agent loop    ↓model_tools.handle_function_call(name, args, task_id, user_task)    ↓[Agent-loop tools?] → handled directly by agent loop (todo, memory, session_search, delegate_task)    ↓[Plugin pre-hook] → invoke_hook("pre_tool_call", ...)    ↓registry.dispatch(name, args, **kwargs)    ↓Look up ToolEntry by name    ↓[Async handler?] → bridge via _run_async()[Sync handler?]  → call directly    ↓Return result string (or JSON error)    ↓[Plugin post-hook] → invoke_hook("post_tool_call", ...)
```

### Error wrapping​

All tool execution is wrapped in error handling at two levels:

1. registry.dispatch()— catches any exception from the handler and returns{"error": "Tool execution failed: ExceptionType: message"}as JSON.
2. handle_function_call()— wraps the entire dispatch in a secondary try/except that returns{"error": "Error executing tool_name: message"}.

registry.dispatch()— catches any exception from the handler and returns{"error": "Tool execution failed: ExceptionType: message"}as JSON.

`registry.dispatch()`
`{"error": "Tool execution failed: ExceptionType: message"}`

handle_function_call()— wraps the entire dispatch in a secondary try/except that returns{"error": "Error executing tool_name: message"}.

`handle_function_call()`
`{"error": "Error executing tool_name: message"}`

This ensures the model always receives a well-formed JSON string, never an unhandled exception.

### Agent-loop tools​

Four tools are intercepted before registry dispatch because they need agent-level state (TodoStore, MemoryStore, etc.):

- todo— planning/task tracking
- memory— persistent memory writes
- session_search— cross-session recall
- delegate_task— spawns subagent sessions

`todo`
`memory`
`session_search`
`delegate_task`

These tools' schemas are still registered in the registry (forget_tool_definitions), but their handlers return a stub error if dispatch somehow reaches them directly.

`get_tool_definitions`

### Async bridging​

When a tool handler is async,_run_async()bridges it to the sync dispatch path:

`_run_async()`
- CLI path (no running loop)— uses a persistent event loop to keep cached async clients alive
- Gateway path (running loop)— spins up a disposable thread withasyncio.run()
- Worker threads (parallel tools)— uses per-thread persistent loops stored in thread-local storage

`asyncio.run()`

## The DANGEROUS_PATTERNS approval flow​

The terminal tool integrates a dangerous-command approval system defined intools/approval.py:

`tools/approval.py`
1. Pattern detection—DANGEROUS_PATTERNSis a list of(regex, description)tuples covering destructive operations:Recursive deletes (rm -rf)Filesystem formatting (mkfs,dd)SQL destructive operations (DROP TABLE,DELETE FROMwithoutWHERE)System config overwrites (> /etc/)Service manipulation (systemctl stop)Remote code execution (curl | sh)Fork bombs, process kills, etc.
2. Detection— before executing any terminal command,detect_dangerous_command(command)checks against all patterns.
3. Approval prompt— if a match is found:CLI mode— an interactive prompt asks the user to approve, deny, or allow permanentlyGateway mode— an async approval callback sends the request to the messaging platformSmart approval— optionally, an auxiliary LLM can auto-approve low-risk commands that match patterns (e.g.,rm -rf node_modules/is safe but matches "recursive delete")
4. Session state— approvals are tracked per-session. Once you approve "recursive delete" for a session, subsequentrm -rfcommands don't re-prompt.
5. Permanent allowlist— the "allow permanently" option writes the pattern toconfig.yaml'scommand_allowlist, persisting across sessions.

Pattern detection—DANGEROUS_PATTERNSis a list of(regex, description)tuples covering destructive operations:

`DANGEROUS_PATTERNS`
`(regex, description)`
- Recursive deletes (rm -rf)
- Filesystem formatting (mkfs,dd)
- SQL destructive operations (DROP TABLE,DELETE FROMwithoutWHERE)
- System config overwrites (> /etc/)
- Service manipulation (systemctl stop)
- Remote code execution (curl | sh)
- Fork bombs, process kills, etc.

`rm -rf`
`mkfs`
`dd`
`DROP TABLE`
`DELETE FROM`
`WHERE`
`> /etc/`
`systemctl stop`
`curl | sh`

Detection— before executing any terminal command,detect_dangerous_command(command)checks against all patterns.

`detect_dangerous_command(command)`

Approval prompt— if a match is found:

- CLI mode— an interactive prompt asks the user to approve, deny, or allow permanently
- Gateway mode— an async approval callback sends the request to the messaging platform
- Smart approval— optionally, an auxiliary LLM can auto-approve low-risk commands that match patterns (e.g.,rm -rf node_modules/is safe but matches "recursive delete")

`rm -rf node_modules/`

Session state— approvals are tracked per-session. Once you approve "recursive delete" for a session, subsequentrm -rfcommands don't re-prompt.

`rm -rf`

Permanent allowlist— the "allow permanently" option writes the pattern toconfig.yaml'scommand_allowlist, persisting across sessions.

`config.yaml`
`command_allowlist`

## Terminal/runtime environments​

The terminal system supports multiple backends:

- local
- docker
- ssh
- singularity
- modal
- daytona

It also supports:

- per-task cwd overrides
- background process management
- PTY mode
- approval callbacks for dangerous commands

## Concurrency​

Tool calls may execute sequentially or concurrently depending on the tool mix and interaction requirements.

## Related docs​

- Toolsets Reference
- Built-in Tools Reference
- Agent Loop Internals
- ACP Internals