---
layout: docs
title: "Features_Code Execution"
permalink: /docs/user-guide/features_code-execution/
---

- 
- Features
- Automation
- Code Execution

# Code Execution (Programmatic Tool Calling)

Theexecute_codetool lets the agent write Python scripts that call Hermes tools programmatically, collapsing multi-step workflows into a single LLM turn. The script runs in a child process on the agent host, communicating with Hermes over a Unix domain socket RPC.

`execute_code`

## How It Works​

1. The agent writes a Python script usingfrom hermes_tools import ...
2. Hermes generates ahermes_tools.pystub module with RPC functions
3. Hermes opens a Unix domain socket and starts an RPC listener thread
4. The script runs in a child process — tool calls travel over the socket back to Hermes
5. Only the script'sprint()output is returned to the LLM; intermediate tool results never enter the context window

`from hermes_tools import ...`
`hermes_tools.py`
`print()`

```
# The agent can write scripts like:from hermes_tools import web_search, web_extractresults = web_search("Python 3.13 features", limit=5)for r in results["data"]["web"]:    content = web_extract([r["url"]])    # ... filter and process ...print(summary)
```

Available tools inside scripts:web_search,web_extract,read_file,write_file,search_files,patch,terminal(foreground only).

`web_search`
`web_extract`
`read_file`
`write_file`
`search_files`
`patch`
`terminal`

## When the Agent Uses This​

The agent usesexecute_codewhen there are:

`execute_code`
- 3+ tool callswith processing logic between them
- Bulk data filtering or conditional branching
- Loops over results

The key benefit: intermediate tool results never enter the context window — only the finalprint()output comes back, dramatically reducing token usage.

`print()`

## Practical Examples​

### Data Processing Pipeline​

```
from hermes_tools import search_files, read_fileimport json# Find all config files and extract database settingsmatches = search_files("database", path=".", file_glob="*.yaml", limit=20)configs = []for match in matches.get("matches", []):    content = read_file(match["path"])    configs.append({"file": match["path"], "preview": content["content"][:200]})print(json.dumps(configs, indent=2))
```

### Multi-Step Web Research​

```
from hermes_tools import web_search, web_extractimport json# Search, extract, and summarize in one turnresults = web_search("Rust async runtime comparison 2025", limit=5)summaries = []for r in results["data"]["web"]:    page = web_extract([r["url"]])    for p in page.get("results", []):        if p.get("content"):            summaries.append({                "title": r["title"],                "url": r["url"],                "excerpt": p["content"][:500]            })print(json.dumps(summaries, indent=2))
```

### Bulk File Refactoring​

```
from hermes_tools import search_files, read_file, patch# Find all Python files using deprecated API and fix themmatches = search_files("old_api_call", path="src/", file_glob="*.py")fixed = 0for match in matches.get("matches", []):    result = patch(        path=match["path"],        old_string="old_api_call(",        new_string="new_api_call(",        replace_all=True    )    if "error" not in str(result):        fixed += 1print(f"Fixed {fixed} files out of {len(matches.get('matches', []))} matches")
```

### Build and Test Pipeline​

```
from hermes_tools import terminal, read_fileimport json# Run tests, parse results, and reportresult = terminal("cd /project && python -m pytest --tb=short -q 2>&1", timeout=120)output = result.get("output", "")# Parse test outputpassed = output.count(" passed")failed = output.count(" failed")errors = output.count(" error")report = {    "passed": passed,    "failed": failed,    "errors": errors,    "exit_code": result.get("exit_code", -1),    "summary": output[-500:] if len(output) > 500 else output}print(json.dumps(report, indent=2))
```

## Execution Mode​

execute_codehas two execution modes controlled bycode_execution.modein~/.hermes/config.yaml:

`execute_code`
`code_execution.mode`
`~/.hermes/config.yaml`
| Mode | Working directory | Python interpreter |
| --- | --- | --- |
| project(default) | The session's working directory (same asterminal()) | ActiveVIRTUAL_ENV/CONDA_PREFIXpython, falling back to Hermes's own python |
| strict | A temp staging directory isolated from the user's project | sys.executable(Hermes's own python) |

`project`
`terminal()`
`VIRTUAL_ENV`
`CONDA_PREFIX`
`strict`
`sys.executable`

When to leave it onproject:you wantimport pandas,from my_project import foo, or relative paths likeopen(".env")to work the same way they do interminal(). This is almost always what you want.

`project`
`import pandas`
`from my_project import foo`
`open(".env")`
`terminal()`

When to flip tostrict:you need maximum reproducibility — you want the same interpreter every session regardless of which venv the user activated, and you want scripts quarantined from the project tree (no risk of accidentally reading project files through a relative path).

`strict`

```
# ~/.hermes/config.yamlcode_execution:  mode: project   # or "strict"
```

Fallback behavior inprojectmode: ifVIRTUAL_ENV/CONDA_PREFIXis unset, broken, or points at a Python older than 3.8, the resolver falls back cleanly tosys.executable— it never leaves the agent without a working interpreter.

`project`
`VIRTUAL_ENV`
`CONDA_PREFIX`
`sys.executable`

Security-critical invariants are identical across both modes:

- environment scrubbing (API keys, tokens, credentials stripped)
- tool whitelist (scripts cannot callexecute_coderecursively,delegate_task, or MCP tools)
- resource limits (timeout, stdout cap, tool-call cap)

`execute_code`
`delegate_task`

Switching mode changes where scripts run and which interpreter runs them, not what credentials they can see or which tools they can call.

## Resource Limits​

| Resource | Limit | Notes |
| --- | --- | --- |
| Timeout | 5 minutes (300s) | Script is killed with SIGTERM, then SIGKILL after 5s grace |
| Stdout | 50 KB | Output truncated with[output truncated at 50KB]notice |
| Stderr | 10 KB | Included in output on non-zero exit for debugging |
| Tool calls | 50 per execution | Error returned when limit reached |

`[output truncated at 50KB]`

All limits are configurable viaconfig.yaml:

`config.yaml`

```
# In ~/.hermes/config.yamlcode_execution:  mode: project      # project (default) | strict  timeout: 300       # Max seconds per script (default: 300)  max_tool_calls: 50 # Max tool calls per execution (default: 50)
```

## How Tool Calls Work Inside Scripts​

When your script calls a function likeweb_search("query"):

`web_search("query")`
1. The call is serialized to JSON and sent over a Unix domain socket to the parent process
2. The parent dispatches through the standardhandle_function_callhandler
3. The result is sent back over the socket
4. The function returns the parsed result

`handle_function_call`

This means tool calls inside scripts behave identically to normal tool calls — same rate limits, same error handling, same capabilities. The only restriction is thatterminal()is foreground-only (nobackgroundorptyparameters).

`terminal()`
`background`
`pty`

## Error Handling​

When a script fails, the agent receives structured error information:

- Non-zero exit code: stderr is included in the output so the agent sees the full traceback
- Timeout: Script is killed and the agent sees"Script timed out after 300s and was killed."
- Interruption: If the user sends a new message during execution, the script is terminated and the agent sees[execution interrupted — user sent a new message]
- Tool call limit: When the 50-call limit is hit, subsequent tool calls return an error message

`"Script timed out after 300s and was killed."`
`[execution interrupted — user sent a new message]`

The response always includesstatus(success/error/timeout/interrupted),output,tool_calls_made, andduration_seconds.

`status`
`output`
`tool_calls_made`
`duration_seconds`

## Security​

The child process runs with aminimal environment. API keys, tokens, and credentials are stripped by default. The script accesses tools exclusively via the RPC channel — it cannot read secrets from environment variables unless explicitly allowed.

Environment variables containingKEY,TOKEN,SECRET,PASSWORD,CREDENTIAL,PASSWD, orAUTHin their names are excluded. Only safe system variables (PATH,HOME,LANG,SHELL,PYTHONPATH,VIRTUAL_ENV, etc.) are passed through.

`KEY`
`TOKEN`
`SECRET`
`PASSWORD`
`CREDENTIAL`
`PASSWD`
`AUTH`
`PATH`
`HOME`
`LANG`
`SHELL`
`PYTHONPATH`
`VIRTUAL_ENV`

### Skill Environment Variable Passthrough​

When a skill declaresrequired_environment_variablesin its frontmatter, those variables areautomatically passed throughto bothexecute_codeandterminalchild processes after the skill is loaded. This lets skills use their declared API keys without weakening the security posture for arbitrary code.

`required_environment_variables`
`execute_code`
`terminal`

For non-skill use cases, you can explicitly allowlist variables inconfig.yaml:

`config.yaml`

```
terminal:  env_passthrough:    - MY_CUSTOM_KEY    - ANOTHER_TOKEN
```

See theSecurity guidefor full details.

### HERMES_*variables in the child​

`HERMES_*`

The child process receives only a small, fixed set of operationalHERMES_*variables by exact name:

`HERMES_*`
- HERMES_HOME
- HERMES_PROFILE
- HERMES_CONFIG
- HERMES_ENV

`HERMES_HOME`
`HERMES_PROFILE`
`HERMES_CONFIG`
`HERMES_ENV`

(plusHERMES_RPC_DIR/HERMES_RPC_SOCKET/TZ/HOME, which Hermes
injects explicitly so the RPC channel works).

`HERMES_RPC_DIR`
`HERMES_RPC_SOCKET`
`TZ`
`HOME`

Earlier versions passedanyvariable whose name began withHERMES_through to the child. That broad prefix was removed for security hardening: it
could leakHERMES_*-named configuration that doesn't match a secret substring
(for exampleHERMES_BASE_URL,HERMES_KANBAN_DB, or aHERMES_*_WEBHOOKendpoint) into arbitrary sandboxed code.

`HERMES_`
`HERMES_*`
`HERMES_BASE_URL`
`HERMES_KANBAN_DB`
`HERMES_*_WEBHOOK`

If anexecute_codescript — or a repo/plugin module it imports at import time
— relied on aHERMES_*variable outside the four operational names above, it
will now find that variableunsetin the child. The drop is intentional,
not a bug.

`execute_code`
`HERMES_*`

Workaround — opt the variable back in explicitly.Both routes pass the
variable throughexecute_codeandterminalchildren, and neither weakens
the secret-stripping guarantee (Hermes-managed provider credentials can never
be re-allowed this way):

`execute_code`
`terminal`
1. Per-machine, inconfig.yaml— add the exact variable name to the
passthrough allowlist:terminal:env_passthrough:-HERMES_KANBAN_DB-HERMES_BASE_URL
2. Per-skill, in the skill's frontmatter— declare it so it is registered
automatically whenever that skill is loaded:required_environment_variables:-HERMES_KANBAN_DB

Per-machine, inconfig.yaml— add the exact variable name to the
passthrough allowlist:

`config.yaml`

```
terminal:  env_passthrough:    - HERMES_KANBAN_DB    - HERMES_BASE_URL
```

Per-skill, in the skill's frontmatter— declare it so it is registered
automatically whenever that skill is loaded:

```
required_environment_variables:  - HERMES_KANBAN_DB
```

Diagnosing it.When the child drops one or more non-allowlistedHERMES_*variables, Hermes emits a one-linedebuglog naming them and pointing at theenv_passthroughescape hatch. Run with debug logging (hermes logs --level DEBUG, or check~/.hermes/logs/agent.log) and look forexecute_code: dropped N non-allowlisted HERMES_* var(s)if a script behaves
as though aHERMES_*variable is missing.

`HERMES_*`
`debug`
`env_passthrough`
`hermes logs --level DEBUG`
`~/.hermes/logs/agent.log`
`execute_code: dropped N non-allowlisted HERMES_* var(s)`
`HERMES_*`

Hermes always writes the script and the auto-generatedhermes_tools.pyRPC stub into a temp staging directory that is cleaned up after execution. Instrictmode the script alsorunsthere; inprojectmode it runs in the session's working directory (the staging directory stays onPYTHONPATHso imports still resolve). The child process runs in its own process group so it can be cleanly killed on timeout or interruption.

`hermes_tools.py`
`strict`
`project`
`PYTHONPATH`

## execute_code vs terminal​

| Use Case | execute_code | terminal |
| --- | --- | --- |
| Multi-step workflows with tool calls between | ✅ | ❌ |
| Simple shell command | ❌ | ✅ |
| Filtering/processing large tool outputs | ✅ | ❌ |
| Running a build or test suite | ❌ | ✅ |
| Looping over search results | ✅ | ❌ |
| Interactive/background processes | ❌ | ✅ |
| Needs API keys in environment | ⚠️ Only viapassthrough | ✅ (most pass through) |

Rule of thumb:Useexecute_codewhen you need to call Hermes tools programmatically with logic between calls. Useterminalfor running shell commands, builds, and processes.

`execute_code`
`terminal`

## Platform Support​

Code execution requires Unix domain sockets and is available onLinux and macOS only. It is automatically disabled on Windows — the agent falls back to regular sequential tool calls.