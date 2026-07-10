- 
- Integrations
- ACP Editor Integration

# ACP Editor Integration

Hermes Agent can run as an ACP server, letting ACP-compatible editors talk to Hermes over stdio and render:

- chat messages
- tool activity
- file diffs
- terminal commands
- approval prompts
- streamed thinking / response chunks

ACP is a good fit when you want Hermes to behave like an editor-native coding agent instead of a standalone CLI or messaging bot.

## What Hermes exposes in ACP mode​

Hermes runs with a curatedhermes-acptoolset designed for editor workflows. It includes:

`hermes-acp`
- file tools:read_file,write_file,patch,search_files
- terminal tools:terminal,process
- web/browser tools
- memory, todo, session search
- skills
- execute_code and delegate_task
- vision

`read_file`
`write_file`
`patch`
`search_files`
`terminal`
`process`

It intentionally excludes things that do not fit typical editor UX, such as messaging delivery and cronjob management.

## Installation​

Install Hermes normally, then add the ACP extra:

```
pip install -e '.[acp]'
```

This installs theagent-client-protocoldependency and enables:

`agent-client-protocol`
- hermes acp
- hermes-acp
- python -m acp_adapter

`hermes acp`
`hermes-acp`
`python -m acp_adapter`

For Zed registry installs, Zed launches Hermes through the official ACP Registry entry. That entry uses auvxdistribution that runs:

`uvx`

```
uvx --from 'hermes-agent[acp]==<version>' hermes-acp
```

Make sureuvis available onPATHbefore using the registry install path.

`uv`
`PATH`

## Launching the ACP server​

Any of the following starts Hermes in ACP mode:

```
hermes acp
```

```
hermes-acp
```

```
python -m acp_adapter
```

Hermes logs to stderr so stdout remains reserved for ACP JSON-RPC traffic.

For non-interactive checks:

```
hermes acp --versionhermes acp --check
```

### Browser tools (optional)​

Browser tools (browser_navigate,browser_click, etc.) depend on theagent-browsernpm package and Chromium, which aren't part of the Python
wheel. Install them with:

`browser_navigate`
`browser_click`
`agent-browser`

```
hermes acp --setup-browser           # interactive (prompts before ~400 MB download)hermes acp --setup-browser --yes     # accept the download non-interactively
```

This is the standalone command. The Zed registry's terminal-auth flow (hermes acp --setup) also offers the browser bootstrap as a follow-up question after model selection, so most users never need to run--setup-browserdirectly.

`hermes acp --setup`
`--setup-browser`

What it does:

- Installs Node.js 22 LTS into~/.hermes/node/if missing
- npm install -g agent-browser @askjo/camofox-browserinto that prefix (no sudo needed —npm's--prefixpoints at the user-writable Hermes-managed Node)
- Installs Playwright Chromium, or uses a detected system Chrome/Chromium when available

`~/.hermes/node/`
`npm install -g agent-browser @askjo/camofox-browser`
`npm`
`--prefix`

The bootstrap is idempotent — re-running it is fast and skips work that's already done.

## Editor setup​

### VS Code​

Install theACP Clientextension.

To connect:

1. Open the ACP Client panel from the Activity Bar.
2. SelectHermes Agentfrom the built-in agent list.
3. Connect and start chatting.

If you want to define Hermes manually, add it through VS Code settings underacp.agents:

`acp.agents`

```
{  "acp.agents": {    "Hermes Agent": {      "command": "hermes",      "args": ["acp"]    }  }}
```

### Zed​

Zed v0.221.x and newer installs external agents through the official ACP Registry.

1. Open the Agent Panel.
2. ClickAdd Agent, or run thezed: acp registrycommand.
3. Search forHermes Agent.
4. Install it and start a new Hermes external-agent thread.

`zed: acp registry`

Prerequisites:

- Configure Hermes provider credentials first withhermes model, or set them in~/.hermes/.env/~/.hermes/config.yaml.
- Installuvso the registry launcher can runuvx --from 'hermes-agent[acp]==<version>' hermes-acp.

`hermes model`
`~/.hermes/.env`
`~/.hermes/config.yaml`
`uv`
`uvx --from 'hermes-agent[acp]==<version>' hermes-acp`

For local development before the registry entry is available, use a custom agent server in Zed settings:

```
{  "agent_servers": {    "hermes-agent": {      "type": "custom",      "command": "hermes",      "args": ["acp"]    }  }}
```

### JetBrains​

Use an ACP-compatible plugin and point it at:

```
/path/to/hermes-agent/acp_registry
```

## Registry manifest​

The source copy of Hermes' official ACP Registry metadata lives at:

```
acp_registry/agent.jsonacp_registry/icon.svg
```

The upstream registry PR copies those files into the top-levelhermes-agent/directory inagentclientprotocol/registry.

`hermes-agent/`
`agentclientprotocol/registry`

The registry entry uses auvxdistribution that points directly at thehermes-agentPyPI release:

`uvx`
`hermes-agent`

```
uvx --from 'hermes-agent[acp]==<version>' hermes-acp
```

The registry CI verifies that the pinned version exists on PyPI, so the manifest'sversionand uvxpackagepin must always matchpyproject.toml.scripts/release.pykeeps them in lockstep automatically.

`version`
`package`
`pyproject.toml`
`scripts/release.py`

## Configuration and credentials​

ACP mode uses the same Hermes configuration as the CLI:

- ~/.hermes/.env
- ~/.hermes/config.yaml
- ~/.hermes/skills/
- ~/.hermes/state.db

`~/.hermes/.env`
`~/.hermes/config.yaml`
`~/.hermes/skills/`
`~/.hermes/state.db`

Provider resolution uses Hermes' normal runtime resolver, so ACP inherits the currently configured provider and credentials. Hermes also advertises a terminal auth method (--setup) for first-run registry clients; this opens Hermes' interactive model/provider setup.

`--setup`

## Session behavior​

ACP sessions are tracked by the ACP adapter's in-memory session manager while the server is running.

Each session stores:

- session ID
- working directory
- selected model
- current conversation history
- cancel event

The underlyingAIAgentstill uses Hermes' normal persistence/logging paths, but ACPlist/load/resume/forkare scoped to the currently running ACP server process.

`AIAgent`
`list/load/resume/fork`

## Working directory behavior​

ACP sessions bind the editor's cwd to the Hermes task ID so file and terminal tools run relative to the editor workspace, not the server process cwd.

## Approvals​

Dangerous terminal commands can be routed back to the editor as approval prompts. ACP approval options are simpler than the CLI flow:

- allow once
- allow always
- deny

On timeout or error, the approval bridge denies the request.

### Session-scoped edit auto-approval​

ACP exposes a third tier betweenallow onceandallow always:Allow for session. Picking it from the editor's permission prompt records the approval inside the current ACP session only — every subsequent matching command in that session goes through without prompting, but a new ACP session (or restarting the editor) resets the slate and re-prompts the first time.

| Option | Editor label | Scope | Persisted across restarts |
| --- | --- | --- | --- |
| allow_once | Allow once | This one tool call | No |
| allow_session | Allow for session | All matching calls in this ACP session | No — cleared when the session ends |
| allow_always | Allow always | All future sessions | Yes (written to the Hermes permanent allowlist) |
| deny | Deny | This one tool call | No |

`allow_once`
`allow_session`
`allow_always`
`deny`

allow_sessionis the right default for an editor workflow where you trust an agent for the duration of a task but don't want to grant a long-lived allowlist entry. The safety trade-off is straightforward: the broader the scope, the less the editor will interrupt you, and the more damage a misbehaving agent (or prompt injection) can do before you notice. Start withallow_oncefor unfamiliar commands; promote toallow_sessiononce you've seen the agent run the same pattern correctly a few times; reserveallow_alwaysfor truly idempotent commands you trust forever (e.g.git status).

`allow_session`
`allow_once`
`allow_session`
`allow_always`
`git status`

The ACP bridge maps these options onto Hermes' internal approval semantics —allow_alwayswrites a permanent allowlist entry the same way the CLI does, whileallow_sessiononly affects the in-process approval cache for the current ACP session.

`allow_always`
`allow_session`

## Troubleshooting​

### ACP agent does not appear in the editor​

Check:

- In Zed, open the ACP Registry withzed: acp registryand search forHermes Agent.
- For manual/local development, verify the customagent_serverscommand points tohermes acp.
- Hermes is installed and on your PATH.
- The ACP extra is installed (pip install -e '.[acp]').
- uvis installed if launching from the official Zed registry entry.

`zed: acp registry`
`agent_servers`
`hermes acp`
`pip install -e '.[acp]'`
`uv`

### ACP starts but immediately errors​

Try these checks:

```
hermes acp --versionhermes acp --checkhermes doctorhermes status
```

### Missing credentials​

ACP mode uses Hermes' existing provider setup. Configure credentials with:

```
hermes model
```

or by editing~/.hermes/.env. Registry clients can also trigger Hermes' terminal auth flow, which runs the same interactive provider/model setup.

`~/.hermes/.env`

### Zed registry launcher cannot find uv​

Installuvfrom the official uv installation docs, then retry the Hermes Agent thread from Zed.

`uv`

## See also​

- ACP Internals
- Provider Runtime Resolution
- Tools Runtime