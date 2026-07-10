---
layout: docs
title: "جزئیات داخلی ACP"
permalink: /docs/developer-guide/acp-internals/
---

- 
- Developer Guide
- Internals
- ACP Internals

# ACP Internals

The ACP adapter wraps Hermes' synchronousAIAgentin an async JSON-RPC stdio server.

`AIAgent`

Key implementation files:

- acp_adapter/entry.py
- acp_adapter/server.py
- acp_adapter/session.py
- acp_adapter/events.py
- acp_adapter/permissions.py
- acp_adapter/tools.py
- acp_adapter/auth.py
- acp_registry/agent.json

`acp_adapter/entry.py`
`acp_adapter/server.py`
`acp_adapter/session.py`
`acp_adapter/events.py`
`acp_adapter/permissions.py`
`acp_adapter/tools.py`
`acp_adapter/auth.py`
`acp_registry/agent.json`

## Boot flow​

```
hermes acp / hermes-acp / python -m acp_adapter  -> acp_adapter.entry.main()  -> parse --version / --check / --setup before server startup  -> load ~/.hermes/.env  -> configure stderr logging  -> construct HermesACPAgent  -> acp.run_agent(agent, use_unstable_protocol=True)
```

The Zed ACP Registry path launches the same adapter throughuvx --from 'hermes-agent[acp]==<version>' hermes-acp, pointed at thehermes-agentPyPI release.

`uvx --from 'hermes-agent[acp]==<version>' hermes-acp`
`hermes-agent`

Stdout is reserved for ACP JSON-RPC transport. Human-readable logs go to stderr.

## Major components​

### HermesACPAgent​

`HermesACPAgent`

acp_adapter/server.pyimplements the ACP agent protocol.

`acp_adapter/server.py`

Responsibilities:

- initialize / authenticate
- new/load/resume/fork/list/cancel session methods
- prompt execution
- session model switching
- wiring sync AIAgent callbacks into ACP async notifications

### SessionManager​

`SessionManager`

acp_adapter/session.pytracks live ACP sessions.

`acp_adapter/session.py`

Each session stores:

- session_id
- agent
- cwd
- model
- history
- cancel_event

`session_id`
`agent`
`cwd`
`model`
`history`
`cancel_event`

The manager is thread-safe and supports:

- create
- get
- remove
- fork
- list
- cleanup
- cwd updates

### Event bridge​

acp_adapter/events.pyconverts AIAgent callbacks into ACPsession_updateevents.

`acp_adapter/events.py`
`session_update`

Bridged callbacks:

- tool_progress_callback
- thinking_callback(currently set toNonein the ACP bridge — reasoning is forwarded throughstep_callbackinstead)
- step_callback

`tool_progress_callback`
`thinking_callback`
`None`
`step_callback`
`step_callback`

BecauseAIAgentruns in a worker thread while ACP I/O lives on the main event loop, the bridge uses:

`AIAgent`

```
asyncio.run_coroutine_threadsafe(...)
```

### Permission bridge​

acp_adapter/permissions.pyadapts dangerous terminal approval prompts into ACP permission requests.

`acp_adapter/permissions.py`

Mapping:

- allow_once-> Hermesonce
- allow_always-> Hermesalways
- reject options -> Hermesdeny

`allow_once`
`once`
`allow_always`
`always`
`deny`

Timeouts and bridge failures deny by default.

### Tool rendering helpers​

acp_adapter/tools.pymaps Hermes tools to ACP tool kinds and builds editor-facing content.

`acp_adapter/tools.py`

Examples:

- patch/write_file-> file diffs
- terminal-> shell command text
- read_file/search_files-> text previews
- large results -> truncated text blocks for UI safety

`patch`
`write_file`
`terminal`
`read_file`
`search_files`

## Session lifecycle​

```
new_session(cwd)  -> create SessionState  -> create AIAgent(platform="acp", enabled_toolsets=["hermes-acp"])  -> bind task_id/session_id to cwd overrideprompt(..., session_id)  -> extract text from ACP content blocks  -> reset cancel event  -> install callbacks + approval bridge  -> run AIAgent in ThreadPoolExecutor  -> update session history  -> emit final agent message chunk
```

### Cancelation​

cancel(session_id):

`cancel(session_id)`
- sets the session cancel event
- callsagent.interrupt()when available
- causes the prompt response to returnstop_reason="cancelled"

`agent.interrupt()`
`stop_reason="cancelled"`

### Forking​

fork_session()deep-copies message history into a new live session, preserving conversation state while giving the fork its own session ID and cwd.

`fork_session()`

## Provider/auth behavior​

ACP does not implement its own auth store.

Instead it reuses Hermes' runtime resolver:

- acp_adapter/auth.py
- hermes_cli/runtime_provider.py

`acp_adapter/auth.py`
`hermes_cli/runtime_provider.py`

So ACP advertises and uses the currently configured Hermes provider/credentials. It also always advertises a terminal setup auth method (hermes-setup, args--setup) so first-run registry clients can open Hermes' interactive model/provider configuration before starting a normal ACP session.

`hermes-setup`
`--setup`

## Working directory binding​

ACP sessions carry an editor cwd.

The session manager binds that cwd to the ACP session ID via task-scoped terminal/file overrides, so file and terminal tools operate relative to the editor workspace.

## Duplicate same-name tool calls​

The event bridge tracks tool IDs FIFO per tool name, not just one ID per name. This is important for:

- parallel same-name calls
- repeated same-name calls in one step

Without FIFO queues, completion events would attach to the wrong tool invocation.

## Approval callback restoration​

ACP temporarily installs an approval callback on the terminal tool during prompt execution, then restores the previous callback afterward. This avoids leaving ACP session-specific approval handlers installed globally forever.

## Current limitations​

- ACP sessions are persisted to the shared~/.hermes/state.db(SessionDB) and transparently restored across process restarts; they appear insession_search
- non-text prompt blocks are currently ignored for request text extraction
- editor-specific UX varies by ACP client implementation

`~/.hermes/state.db`
`session_search`

## Related files​

- tests/acp/— ACP test suite
- toolsets.py—hermes-acptoolset definition
- hermes_cli/main.py—hermes acpCLI subcommand
- pyproject.toml—[acp]optional dependency +hermes-acpscript

`tests/acp/`
`toolsets.py`
`hermes-acp`
`hermes_cli/main.py`
`hermes acp`
`pyproject.toml`
`[acp]`
`hermes-acp`