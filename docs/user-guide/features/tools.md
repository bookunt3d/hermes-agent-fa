---
layout: docs
title: "ابزارها"
permalink: /user-guide/features/tools/
---

- 
- Features
- Core
- Tools & Toolsets

# Tools & Toolsets

Tools are functions that extend the agent's capabilities. They're organized into logicaltoolsetsthat can be enabled or disabled per platform.

## Available Tools​

Hermes ships with a broad built-in tool registry covering web search, browser automation, terminal execution, file editing, memory, delegation, scheduled tasks, Home Assistant, and more.

Honcho cross-session memoryis available as a memory provider plugin (plugins/memory/honcho/), not as a built-in toolset. SeePluginsfor installation.

`plugins/memory/honcho/`
[Plugins](/docs/user-guide/features/plugins)

High-level categories:

| Category | Examples | Description |
| --- | --- | --- |
| Web | web_search,web_extract | Search the web and extract page content. |
| X Search | x_search | Search X (Twitter) posts and threads via xAI's built-inx_searchResponses tool — gated on xAI credentials (SuperGrok OAuth orXAI_API_KEY); off by default, opt in viahermes tools→ 🐦 X (Twitter) Search. |
| Terminal & Files | terminal,process,read_file,patch | Execute commands and manipulate files. |
| Browser | browser_navigate,browser_snapshot,browser_vision | Interactive browser automation with text and vision support. |
| Media | vision_analyze,image_generate,text_to_speech | Multimodal analysis and generation. |
| Agent orchestration | todo,clarify,execute_code,delegate_task | Planning, clarification, code execution, and subagent delegation. |
| Memory & recall | memory,session_search | Persistent memory and session search. |
| Automation | cronjob | Scheduled tasks with create/list/update/pause/resume/run/remove actions. Outbound delivery is handled by cron's own delivery, thehermes sendCLI, and the gateway notifier — not by an agent-callable tool. |
| Integrations | ha_*, MCP server tools | Home Assistant, MCP, and other integrations. |

`web_search`
`web_extract`
`x_search`
`x_search`
`XAI_API_KEY`
`hermes tools`
`terminal`
`process`
`read_file`
`patch`
`browser_navigate`
`browser_snapshot`
`browser_vision`
`vision_analyze`
`image_generate`
`text_to_speech`
`todo`
`clarify`
`execute_code`
`delegate_task`
`memory`
`session_search`
`cronjob`
`hermes send`
`ha_*`

For the authoritative code-derived registry, seeBuilt-in Tools ReferenceandToolsets Reference.

[Built-in Tools Reference](/docs/reference/tools-reference)
[Toolsets Reference](/docs/reference/toolsets-reference)

PaidNous Portalsubscribers can use web search, image generation, TTS, and browser automation through theTool Gateway— no separate API keys needed. Runhermes modelto enable it, or configure individual tools withhermes tools.

[Nous Portal](https://portal.nousresearch.com)
[Tool Gateway](/docs/user-guide/features/tool-gateway)
`hermes model`
`hermes tools`

## Using Toolsets​

```
# Use specific toolsetshermes chat --toolsets "web,terminal"# See all available toolshermes tools# Configure tools per platform (interactive)hermes tools
```

Common toolsets includeweb,search,terminal,file,browser,vision,image_gen,skills,tts,todo,memory,session_search,cronjob,code_execution,delegation,clarify,homeassistant,messaging,spotify,discord,discord_admin,debugging, andsafe.

`web`
`search`
`terminal`
`file`
`browser`
`vision`
`image_gen`
`skills`
`tts`
`todo`
`memory`
`session_search`
`cronjob`
`code_execution`
`delegation`
`clarify`
`homeassistant`
`messaging`
`spotify`
`discord`
`discord_admin`
`debugging`
`safe`

SeeToolsets Referencefor the full set, including platform presets such ashermes-cli,hermes-telegram, and dynamic MCP toolsets likemcp-<server>.

[Toolsets Reference](/docs/reference/toolsets-reference)
`hermes-cli`
`hermes-telegram`
`mcp-<server>`

## Terminal Backends​

The terminal tool can execute commands in different environments:

| Backend | Description | Use Case |
| --- | --- | --- |
| local | Run on your machine (default) | Development, trusted tasks |
| docker | Isolated containers | Security, reproducibility |
| ssh | Remote server | Sandboxing, keep agent away from its own code |
| singularity | HPC containers | Cluster computing, rootless |
| modal | Cloud execution | Serverless, scale |
| daytona | Cloud sandbox workspace | Persistent remote dev environments |

`local`
`docker`
`ssh`
`singularity`
`modal`
`daytona`

### Configuration​

```
# In ~/.hermes/config.yamlterminal:  backend: local    # or: docker, ssh, singularity, modal, daytona  cwd: "."          # Working directory  timeout: 180      # Command timeout in seconds
```

### Docker Backend​

```
terminal:  backend: docker  docker_image: python:3.11-slim
```

One persistent container, shared across the whole process.Hermes starts a single long-lived container on first use (docker run -d ... sleep 2h) and routes every terminal, file, andexecute_codecall throughdocker execinto that same container. Working-directory changes, installed packages, environment tweaks, and files written to/workspaceall carry over from one tool call to the next, across/new,/reset, anddelegate_tasksubagents, for the lifetime of the Hermes process. The container is stopped and removed on shutdown.

`docker run -d ... sleep 2h`
`execute_code`
`docker exec`
`/workspace`
`/new`
`/reset`
`delegate_task`

This means the Docker backend behaves like a persistent sandbox VM, not a fresh container per command. If youpip install fooonce, it's there for the rest of the session. If youcd /workspace/project, subsequentlscalls see that directory. SeeConfiguration → Docker Backendfor the full lifecycle details and thecontainer_persistentflag that controls whether/workspaceand/rootsurvive across Hermes restarts.

`pip install foo`
`cd /workspace/project`
`ls`
[Configuration → Docker Backend](/docs/user-guide/configuration#docker-backend)
`container_persistent`
`/workspace`
`/root`

### SSH Backend​

Recommended for security — agent can't modify its own code:

```
terminal:  backend: ssh
```

```
# Set credentials in ~/.hermes/.envTERMINAL_SSH_HOST=my-server.example.comTERMINAL_SSH_USER=myuserTERMINAL_SSH_KEY=~/.ssh/id_rsa
```

### Singularity/Apptainer​

```
# Pre-build SIF for parallel workersapptainer build ~/python.sif docker://python:3.11-slim# Configurehermes config set terminal.backend singularityhermes config set terminal.singularity_image ~/python.sif
```

### Modal (Serverless Cloud)​

```
uv pip install modalmodal setuphermes config set terminal.backend modal
```

### Container Resources​

Configure CPU, memory, disk, and persistence for all container backends:

```
terminal:  backend: docker  # or singularity, modal, daytona  container_cpu: 1              # CPU cores (default: 1)  container_memory: 5120        # Memory in MB (default: 5GB)  container_disk: 51200         # Disk in MB (default: 50GB)  container_persistent: true    # Persist filesystem across sessions (default: true)
```

Whencontainer_persistent: true, installed packages, files, and config survive across sessions.

`container_persistent: true`

### Container Security​

All container backends run with security hardening:

- Read-only root filesystem (Docker)
- All Linux capabilities dropped
- No privilege escalation
- PID limits (256 processes)
- Full namespace isolation
- Persistent workspace via volumes, not writable root layer

Docker can optionally receive an explicit env allowlist viaterminal.docker_forward_env, but forwarded variables are visible to commands inside the container and should be treated as exposed to that session.

`terminal.docker_forward_env`

## Background Process Management​

Start background processes and manage them:

```
terminal(command="pytest -v tests/", background=true)# Returns: {"session_id": "proc_abc123", "pid": 12345}# Then manage with the process tool:process(action="list")       # Show all running processesprocess(action="poll", session_id="proc_abc123")   # Check statusprocess(action="wait", session_id="proc_abc123")   # Block until doneprocess(action="log", session_id="proc_abc123")    # Full outputprocess(action="kill", session_id="proc_abc123")   # Terminateprocess(action="write", session_id="proc_abc123", data="y")  # Send input
```

PTY mode (pty=true) enables interactive CLI tools like Codex and Claude Code.

`pty=true`

## Sudo Support​

If a command needs sudo, you'll be prompted for your password (cached for the session). Or setSUDO_PASSWORDin~/.hermes/.env.

`SUDO_PASSWORD`
`~/.hermes/.env`

On messaging platforms, if sudo fails, the output includes a tip to addSUDO_PASSWORDto~/.hermes/.env.

`SUDO_PASSWORD`
`~/.hermes/.env`
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/tools.md)