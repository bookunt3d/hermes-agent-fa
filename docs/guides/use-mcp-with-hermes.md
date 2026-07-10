---
layout: docs
title: "استفاده از MCP"
permalink: /guides/use-mcp-with-hermes/
---

- 
- Guides & Tutorials
- Use MCP with Hermes

# Use MCP with Hermes

This guide shows how to actually use MCP with Hermes Agent in day-to-day workflows.

If the feature page explains what MCP is, this guide is about how to get value from it quickly and safely.

## When should you use MCP?​

Use MCP when:

- a tool already exists in MCP form and you do not want to build a native Hermes tool
- you want Hermes to operate against a local or remote system through a clean RPC layer
- you want fine-grained per-server exposure control
- you want to connect Hermes to internal APIs, databases, or company systems without modifying Hermes core

Do not use MCP when:

- a built-in Hermes tool already solves the job well
- the server exposes a huge dangerous tool surface and you are not prepared to filter it
- you only need one very narrow integration and a native tool would be simpler and safer

## Mental model​

Think of MCP as an adapter layer:

- Hermes remains the agent
- MCP servers contribute tools
- Hermes discovers those tools at startup or reload time
- the model can use them like normal tools
- you control how much of each server is visible

That last part matters. Good MCP usage is not just “connect everything.” It is “connect the right thing, with the smallest useful surface.”

## Step 1: install MCP support​

If you installed Hermes with the standard install script, MCP support is already included (the installer runsuv pip install -e ".[all]").

`uv pip install -e ".[all]"`

If you installed without extras and need to add MCP separately:

```
cd ~/.hermes/hermes-agentuv pip install -e ".[mcp]"
```

For npm-based servers, make sure Node.js andnpxare available.

`npx`

For many Python MCP servers,uvxis a nice default.

`uvx`

## Step 2: add one server first​

Start with a single, safe server.

Example: filesystem access to one project directory only.

```
mcp_servers:  project_fs:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]
```

Then start Hermes:

```
hermes chat
```

Now ask something concrete:

```
Inspect this project and summarize the repo layout.
```

## Step 3: verify MCP loaded​

You can verify MCP in a few ways:

- Hermes banner/status should show MCP integration when configured
- ask Hermes what tools it has available
- use/reload-mcpafter config changes
- check logs if the server failed to connect

`/reload-mcp`

A practical test prompt:

```
Tell me which MCP-backed tools are available right now.
```

## Step 4: start filtering immediately​

Do not wait until later if the server exposes a lot of tools.

### Example: whitelist only what you want​

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, search_code]
```

This is usually the best default for sensitive systems.

## WSL2: bridge Hermes in WSL to Windows Chrome​

This is the practical setup when:

- Hermes runs inside WSL2
- the browser you want to control is your normal signed-in Chrome on Windows
- /browser connectis awkward or unreliable from WSL

`/browser connect`

In this setup, Hermes doesnotconnect to Chrome directly. Instead:

- Hermes runs in WSL
- Hermes starts a local stdio MCP server
- that MCP server is launched through Windows interop (cmd.exeorpowershell.exe)
- the MCP server attaches to your live Windows Chrome session

`cmd.exe`
`powershell.exe`

Mental model:

```
Hermes (WSL) -> MCP stdio bridge -> Windows Chrome
```

### Why this mode is useful​

- you keep your real Windows browser profile, cookies, and logins
- Hermes stays in its supported Unix environment (WSL2)
- browser control is exposed as MCP tools instead of relying on Hermes core browser transport

### Recommended server​

Usechrome-devtools-mcp.

`chrome-devtools-mcp`

If your Windows Chrome already has live remote debugging enabled fromchrome://inspect/#remote-debugging, add it like this from WSL:

`chrome://inspect/#remote-debugging`

```
hermes mcp add chrome-devtools-win --command cmd.exe --args /c npx -y chrome-devtools-mcp@latest --autoConnect --no-usage-statistics
```

After saving the server:

```
hermes mcp test chrome-devtools-win
```

Then start a fresh Hermes session or run:

```
/reload-mcp
```

### Typical prompt​

Once loaded, Hermes can use the MCP-prefixed browser tools directly. For example:

```
调用 MCP 工具 mcp_chrome_devtools_win_list_pages，列出当前浏览器标签页。
```

### When/browser connectis the wrong tool​

`/browser connect`

If Hermes runs in WSL and Chrome runs on Windows,/browser connectmay fail even though Chrome is open and debuggable.

`/browser connect`

Common reasons:

- WSL cannot reach the same host-local endpoint Chrome exposes to Windows tools
- newer Chrome live-debugging flows are not the same as a classicws://localhost:9222
- the browser is easier to attach to from a Windows-side helper likechrome-devtools-mcp

`ws://localhost:9222`
`chrome-devtools-mcp`

In those cases, keep/browser connectfor same-environment setups and use MCP for WSL-to-Windows browser bridging.

`/browser connect`

### Known pitfalls​

- Start Hermes from a Windows-mounted path like/mnt/c/Users/<you>or/mnt/c/workspace/...when using Windows stdio executables through MCP.
- If you start Hermes from/rootor/home/..., Windows may emit aUNCcurrent-directory warning before the MCP server starts.
- Ifchrome-devtools-mcp --autoConnecttimes out while enumerating pages, reduce background/frozen tabs in Chrome and retry.

`/mnt/c/Users/<you>`
`/mnt/c/workspace/...`
`/root`
`/home/...`
`UNC`
`chrome-devtools-mcp --autoConnect`

### Example: blacklist dangerous actions​

```
mcp_servers:  stripe:    url: "https://mcp.stripe.com"    headers:      Authorization: "Bearer ***"    tools:      exclude: [delete_customer, refund_payment]
```

### Example: disable utility wrappers too​

```
mcp_servers:  docs:    url: "https://mcp.docs.example.com"    tools:      prompts: false      resources: false
```

## What does filtering actually affect?​

There are two categories of MCP-exposed functionality in Hermes:

1. Server-native MCP tools

- filtered with:tools.includetools.exclude

- tools.include
- tools.exclude

`tools.include`
`tools.exclude`
1. Hermes-added utility wrappers

- filtered with:tools.resourcestools.prompts

- tools.resources
- tools.prompts

`tools.resources`
`tools.prompts`

### Utility wrappers you may see​

Resources:

- list_resources
- read_resource

`list_resources`
`read_resource`

Prompts:

- list_prompts
- get_prompt

`list_prompts`
`get_prompt`

These wrappers only appear if:

- your config allows them, and
- the MCP server session actually supports those capabilities

So Hermes will not pretend a server has resources/prompts if it does not.

## Common patterns​

### Pattern 1: local project assistant​

Use MCP for a repo-local filesystem or git server when you want Hermes to reason over a bounded workspace.

```
mcp_servers:  fs:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"]  git:    command: "uvx"    args: ["mcp-server-git", "--repository", "/home/user/project"]
```

Good prompts:

```
Review the project structure and identify where configuration lives.
```

```
Check the local git state and summarize what changed recently.
```

### Pattern 2: repo-native work record with Open Scaffold​

UseOpen Scaffoldwhen you want Hermes to read a repository's durable AI-work record: mission, plans, evidence notes, handoff packets, and review/gate results. Hermes remains the agent; Open Scaffold remains the repo-local record.

[Open Scaffold](https://github.com/graphanov/open-scaffold)

Add the server for one scaffolded repository:

```
hermes mcp add open_scaffold --command npx --args -y open-scaffold@latest mcp serve --repo /absolute/path/to/repohermes mcp test open_scaffold
```

Then keep the exposed surface read-oriented. Chooseselectin thehermes mcp addprompt, or editconfig.yamlafterward:

`select`
`hermes mcp add`
`config.yaml`

```
mcp_servers:  open_scaffold:    command: "npx"    args: ["-y", "open-scaffold@latest", "mcp", "serve", "--repo", "/absolute/path/to/repo"]    tools:      include:        - list_plans        - get_plan        - get_mission        - list_evidence        - get_evidence        - get_status        - search_plans        - list_amendments        - get_handoff        - analyze_loop        - gate_loop      prompts: false
```

Good prompts:

```
Use the Open Scaffold MCP tools to compile the current handoff packet and tell me the next legal action.
```

```
Inspect the active plans and evidence notes, then say whether this repo is ready for human review or needs another attempt.
```

Boundary notes:

- Open Scaffold MCP is local-first and read-only by default.
- Its write tools require the server to be started with--allow-write; do not enable that until you explicitly want Hermes to mutate.oscfiles.
- Open Scaffold records and gates work; it does not authorize Hermes to merge, publish, deploy, or spawn runtimes.
- Pinopen-scaffold@<version>instead of@latestif you need reproducible tool schemas.

`--allow-write`
`.osc`
`open-scaffold@<version>`
`@latest`

### Pattern 3: GitHub triage assistant​

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, update_issue, search_code]      prompts: false      resources: false
```

Good prompts:

```
List open issues about MCP, cluster them by theme, and draft a high-quality issue for the most common bug.
```

```
Search the repo for uses of _discover_and_register_server and explain how MCP tools are registered.
```

### Pattern 4: internal API assistant​

```
mcp_servers:  internal_api:    url: "https://mcp.internal.example.com"    headers:      Authorization: "Bearer ***"    tools:      include: [list_customers, get_customer, list_invoices]      resources: false      prompts: false
```

Good prompts:

```
Look up customer ACME Corp and summarize recent invoice activity.
```

This is the sort of place where a strict whitelist is far better than an exclude list.

### Pattern 4: documentation / knowledge servers​

Some MCP servers expose prompts or resources that are more like shared knowledge assets than direct actions.

```
mcp_servers:  docs:    url: "https://mcp.docs.example.com"    tools:      prompts: true      resources: true
```

Good prompts:

```
List available MCP resources from the docs server, then read the onboarding guide and summarize it.
```

```
List prompts exposed by the docs server and tell me which ones would help with incident response.
```

## Tutorial: end-to-end setup with filtering​

Here is a practical progression.

### Phase 1: add GitHub MCP with a tight whitelist​

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, search_code]      prompts: false      resources: false
```

Start Hermes and ask:

```
Search the codebase for references to MCP and summarize the main integration points.
```

### Phase 2: expand only when needed​

If you later need issue updates too:

```
tools:  include: [list_issues, create_issue, update_issue, search_code]
```

Then reload:

```
/reload-mcp
```

### Phase 3: add a second server with different policy​

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, update_issue, search_code]      prompts: false      resources: false  filesystem:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"]
```

Now Hermes can combine them:

```
Inspect the local project files, then create a GitHub issue summarizing the bug you find.
```

That is where MCP gets powerful: multi-system workflows without changing Hermes core.

## Safe usage recommendations​

### Prefer allowlists for dangerous systems​

For anything financial, customer-facing, or destructive:

- usetools.include
- start with the smallest set possible

`tools.include`

### Disable unused utilities​

If you do not want the model browsing server-provided resources/prompts, turn them off:

```
tools:  resources: false  prompts: false
```

### Keep servers scoped narrowly​

Examples:

- filesystem server rooted to one project dir, not your whole home directory
- git server pointed at one repo
- internal API server with read-heavy tool exposure by default

### Reload after config changes​

```
/reload-mcp
```

Do this after changing:

- include/exclude lists
- enabled flags
- resources/prompts toggles
- auth headers / env

## Troubleshooting by symptom​

### "The server connects but the tools I expected are missing"​

Possible causes:

- filtered bytools.include
- excluded bytools.exclude
- utility wrappers disabled viaresources: falseorprompts: false
- server does not actually support resources/prompts

`tools.include`
`tools.exclude`
`resources: false`
`prompts: false`

### "The server is configured but nothing loads"​

Check:

- enabled: falsewas not left in config
- command/runtime exists (npx,uvx, etc.)
- HTTP endpoint is reachable
- auth env or headers are correct

`enabled: false`
`npx`
`uvx`

### "Why do I see fewer tools than the MCP server advertises?"​

Because Hermes now respects your per-server policy and capability-aware registration. That is expected, and usually desirable.

### "How do I remove an MCP server without deleting the config?"​

Use:

```
enabled: false
```

That keeps the config around but prevents connection and registration.

## Recommended first MCP setups​

Good first servers for most users:

- filesystem
- git
- GitHub
- fetch / documentation MCP servers
- one narrow internal API

Not-great first servers:

- giant business systems with lots of destructive actions and no filtering
- anything you do not understand well enough to constrain

## Related docs​

- MCP (Model Context Protocol)
- FAQ
- Slash Commands

[MCP (Model Context Protocol)](/docs/user-guide/features/mcp)
[FAQ](/docs/reference/faq)
[Slash Commands](/docs/reference/slash-commands)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/guides/use-mcp-with-hermes.md)