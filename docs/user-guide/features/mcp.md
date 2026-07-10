---
layout: docs
title: "MCP"
permalink: /user-guide/features/mcp/
---

- 
- Integrations
- MCP (Model Context Protocol)

# MCP (Model Context Protocol)

MCP lets Hermes Agent connect to external tool servers so the agent can use tools that live outside Hermes itself — GitHub, databases, file systems, browser stacks, internal APIs, and more.

If you have ever wanted Hermes to use a tool that already exists somewhere else, MCP is usually the cleanest way to do it.

## What MCP gives you​

- Access to external tool ecosystems without writing a native Hermes tool first
- Local stdio servers and remote HTTP MCP servers in the same config
- Automatic tool discovery and registration at startup
- Utility wrappers for MCP resources and prompts when supported by the server
- Per-server filtering so you can expose only the MCP tools you actually want Hermes to see

## Quick start​

1. MCP support ships with the standard install — no extra step needed.
2. Add an MCP server to~/.hermes/config.yaml:

MCP support ships with the standard install — no extra step needed.

Add an MCP server to~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
mcp_servers:  filesystem:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```

1. Start Hermes:

```
hermes chat
```

1. Ask Hermes to use the MCP-backed capability.

For example:

```
List the files in /home/user/projects and summarize the repo structure.
```

Hermes will discover the MCP server's tools and use them like any other tool.

## Catalog: one-click install for Nous-approved MCPs​

Hermes ships a curated catalog of MCP servers that Nous staff has reviewed
and merged. They're disabled by default — install only what you actually
want.

```
hermes mcp                # interactive picker (default)hermes mcp catalog        # plain-text list, scriptablehermes mcp install n8n    # install a catalog entry by name
```

The picker shows each entry with its current status:

```
n8n          available              Manage and inspect n8n workflows from Hermeslinear       enabled                Linear issue/project management (remote OAuth)github       installed (disabled)   GitHub repo + PR tools
```

HitEnteron a row to install (and walk through any required credentials),
enable, disable, or uninstall. Catalog entries are stored underoptional-mcps/in the hermes-agent repo — presence in that directory means
Nous approval. There is no community submission tier; entries are added by
merging a PR.

`Enter`
`optional-mcps/`

Catalog entries can require:

- API key— Hermes prompts at install time and writes the value to~/.hermes/.env. Non-secret values (base URLs) go to the same file.
- OAuth(remote MCP) — written asauth: oauthin your config; the MCP
client opens a browser on first connection.
- OAuth(third-party provider like Google/GitHub) — Hermes points you athermes auth <provider>if you haven't authenticated already.

`~/.hermes/.env`
`auth: oauth`
`hermes auth <provider>`

### Tool selection at install time​

After credentials are configured, Hermes probes the MCP server to list every
tool it exposes and presents a checklist:

```
Select tools for 'linear' (SPACE toggle, ENTER confirm)  [x] find_issues       Find issues matching a query  [x] get_issue         Get a single issue  [x] create_issue      Create a new issue  [ ] delete_workspace  Delete a Linear workspace  ...
```

The pre-checked rows come from:

1. Your prior selectionif you've installed this entry before (reinstalls
preserve what you had — the manifest's defaults don't override it)
2. The manifest'stools.default_enabledif the entry declares one (some
catalog entries pre-prune mutating or rarely-useful tools)
3. Everythingif neither applies

`tools.default_enabled`

Submit the checklist with ENTER. Only the checked tools end up inmcp_servers.<name>.tools.include. If you select everything, no filter is
written (cleanest config shape, identical behavior).

`mcp_servers.<name>.tools.include`

If the probe fails(server unreachable, OAuth not yet completed,
backing service not running), the install still succeeds: the manifest'stools.default_enabledis applied directly (if declared), or no filter is
written (if not). Re-runhermes mcp configure <name>once the server is
reachable to refine.

`tools.default_enabled`
`hermes mcp configure <name>`

### Trust model​

Installing a catalog entry runs whatever the manifest specifies —git clone,
the entry'sbootstrapcommands (pip install,npm install, etc.), and
ultimately the MCP server's own code. Manifests are gated by PR review into
the hermes-agent repo, so Nous has reviewed each entry before it shipped —but you should still read the manifest before installing, especially thesource:field's repository, theinstall.bootstrap:commands, and anytransport.command:invocation.

`git clone`
`bootstrap`
`pip install`
`npm install`
`source:`
`install.bootstrap:`
`transport.command:`

Manifests live atoptional-mcps/<name>/manifest.yamlon GitHub. The picker also prints the manifest'ssource:URL at install
time so you can quickly verify the upstream repo. The web dashboard's MCP
page surfaces the same detail per catalog entry — transport, auth type, the
endpoint URL (HTTP) or command + args (stdio), the git install source/ref and
bootstrap commands, and setup notes — with thesource:rendered as a
clickable link, so you can inspect exactly what an entry connects to or runs
before clicking Install.

[optional-mcps/<name>/manifest.yaml](https://github.com/NousResearch/hermes-agent/tree/main/optional-mcps)
`optional-mcps/<name>/manifest.yaml`
`source:`
`source:`

### Manifest version compatibility​

Manifests pin amanifest_version. The catalog is forward-compatible: if a
PR adds an entry with a newermanifest_versionthan your installed Hermes
understands, the picker will surface a warning (⚠ '<name>' requires a newer Hermes) for that entry instead of silently hiding it. Runhermes updateto install the latest Hermes when you see that.

`manifest_version`
`manifest_version`
`⚠ '<name>' requires a newer Hermes`
`hermes update`

### Runtime${ENV_VAR}substitution​

`${ENV_VAR}`

Inside an entry'stransport.command,transport.args,transport.url,
andheaders,${VAR}placeholders are resolved at server-connect time
from environment variables (which include everything in~/.hermes/.env).
This is useful when a catalog entry wants to reference a value the user
configured elsewhere — e.g.${HOME}/fooor${MY_PROVIDER_TOKEN}.

`transport.command`
`transport.args`
`transport.url`
`headers`
`${VAR}`
`~/.hermes/.env`
`${HOME}/foo`
`${MY_PROVIDER_TOKEN}`

Note this is distinct from${INSTALL_DIR}in catalog manifests, which is
substituted at install-time with the path the catalog cloned the entry's
repo into.

`${INSTALL_DIR}`

### Updating tool selection later​

```
hermes mcp configure linear
```

Reopens the same checklist with your current selection pre-checked. Use this
when you want more tools enabled, or when the server has added new tools that
you want to opt into.

### Updating the catalog manifest​

MCPs are never auto-updated. Re-runhermes mcp install <name>to refresh
after a Hermes update if a manifest version changed.

`hermes mcp install <name>`

To add an MCP to the catalog, open a PR againstoptional-mcps/.

[optional-mcps/](https://github.com/NousResearch/hermes-agent/tree/main/optional-mcps)
`optional-mcps/`

## Two kinds of MCP servers​

### Stdio servers​

Stdio servers run as local subprocesses and talk over stdin/stdout.

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

Use stdio servers when:

- the server is installed locally
- you want low-latency access to local resources
- you are following MCP server docs that showcommand,args, andenv

`command`
`args`
`env`

### HTTP servers​

HTTP MCP servers are remote endpoints Hermes connects to directly.

```
mcp_servers:  remote_api:    url: "https://mcp.example.com/mcp"    headers:      Authorization: "Bearer ***"
```

Use HTTP servers when:

- the MCP server is hosted elsewhere
- your organization exposes internal MCP endpoints
- you do not want Hermes spawning a local subprocess for that integration

### OAuth-authenticated HTTP servers​

Most hosted MCP servers (Linear, Sentry, Atlassian, Asana, Figma, Stripe, …) require OAuth 2.1 instead of a static bearer token. Setauth: oauthand Hermes handles discovery, dynamic client registration, PKCE, token exchange, refresh, and step-up auth via the MCP Python SDK.

`auth: oauth`

```
mcp_servers:  linear:    url: "https://mcp.linear.app/mcp"    auth: oauth
```

On first connect, Hermes prints an authorize URL, opens your browser when possible, and waits for the OAuth callback on a local loopback port. Tokens are cached at~/.hermes/mcp-tokens/<server>.jsonwith 0o600 perms; subsequent runs reuse them silently until refresh fails.

`~/.hermes/mcp-tokens/<server>.json`

Remote / headless hosts.When Hermes runs on a different machine than your browser, the loopback callback can't reach your laptop. Two ways to complete the flow:

- Paste-back (no setup):on an interactive terminal Hermes prints "Or paste the redirect URL here…" alongside the authorize URL. Open the URL in your browser, approve, copy the full URL the browser ends up on (the redirect will show a connection error — that's expected), paste it at the prompt. Bare?code=…&state=…query strings work too.
- SSH port forward:ssh -N -L <port>:127.0.0.1:<port> user@hostin a separate terminal, then let the redirect flow normally.

`?code=…&state=…`
`ssh -N -L <port>:127.0.0.1:<port> user@host`

SeeOAuth over SSH / Remote Hostsfor the full walkthrough, including DCR-less servers (e.g. Slack), pre-registeredclient_id/client_secret, scope customization, and re-auth viahermes mcp login <server>.

[OAuth over SSH / Remote Hosts](/docs/guides/oauth-over-ssh#mcp-servers)
`client_id`
`client_secret`
`hermes mcp login <server>`

Pitfall — providers that don't support automatic registration (Google Drive, Atlassian).Some servers reject the dynamic client registration step (RFC 7591) that bareauth: oauthrelies on — Google's official Drive server (https://drivemcp.googleapis.com/mcp/v1) returns a400 Bad Request, so no OAuth client is created and no token is acquired. The symptom is subtle: these servers also servetools/listwithoutauth, sohermes mcp logincan list the tools and look like it worked, but every real tool call later times out.hermes mcp loginnow detects this (it checks that a token actually landed on disk) and tells you to supply your own OAuth client. Create one in the provider's console and add it to config:

`auth: oauth`
`https://drivemcp.googleapis.com/mcp/v1`
`400 Bad Request`
`tools/list`
`hermes mcp login`
`hermes mcp login`

```
mcp_servers:  googledrive:    url: "https://drivemcp.googleapis.com/mcp/v1"    auth: oauth    oauth:      client_id: "<your-oauth-client-id>"      client_secret: "<your-oauth-client-secret>"
```

Then runhermes mcp login googledrive— with the pre-registered client, Hermes skips registration and runs the normal browser authorization flow.

`hermes mcp login googledrive`

Pitfall — config auto-reload race.When you edit~/.hermes/config.yamlfrom inside a running Hermes session, the CLI auto-reloads MCP connections with a 30s timeout. That's not enough for an interactive OAuth flow. Add the entry, then runhermes mcp login <server>from a fresh terminal — it waits the full 5 minutes for you to complete auth.

`~/.hermes/config.yaml`
`hermes mcp login <server>`

## mTLS / client certificates​

Remote HTTP MCP servers that require mutual TLS (client-certificate authentication) are supported viaclient_cert/client_key. Hermes passes the resolved certificate to the underlying HTTP client for the TLS handshake.

`client_cert`
`client_key`

client_certaccepts three shapes:

`client_cert`
- A single combined PEM path— one file holding both the certificate and the private key:

```
mcp_servers:  internal_api:    url: "https://mcp.internal.example.com/mcp"    client_cert: "~/.certs/mcp-client.pem"
```

- A[cert, key]2-tuple— certificate and key in separate files (equivalent to settingclient_cert+client_key):

`[cert, key]`
`client_cert`
`client_key`

```
mcp_servers:  internal_api:    url: "https://mcp.internal.example.com/mcp"    client_cert: ["~/.certs/mcp-client.crt", "~/.certs/mcp-client.key"]
```

- A[cert, key, password]3-tuple— when the private key is encrypted, the third element is the key passphrase:

`[cert, key, password]`

```
mcp_servers:  internal_api:    url: "https://mcp.internal.example.com/mcp"    client_cert: ["~/.certs/mcp-client.crt", "~/.certs/mcp-client.key", "${MCP_KEY_PASSWORD}"]
```

You can also keep the cert and key fully separate viaclient_cert(combined PEM) plus an explicitclient_key. Paths support~expansion; a missing file raises a clear, server-scoped error rather than an opaque TLS handshake failure.

`client_cert`
`client_key`
`~`

## Basic configuration reference​

Hermes reads MCP config from~/.hermes/config.yamlundermcp_servers.

`~/.hermes/config.yaml`
`mcp_servers`

### Common keys​

| Key | Type | Meaning |
| --- | --- | --- |
| command | string | Executable for a stdio MCP server |
| args | list | Arguments for the stdio server |
| env | mapping | Environment variables passed to the stdio server |
| url | string | HTTP MCP endpoint |
| headers | mapping | HTTP headers for remote servers |
| client_cert | string | list | Client certificate for mTLS — a combined PEM path, or[cert, key]/[cert, key, password] |
| client_key | string | Client private-key PEM path (when separate fromclient_cert) |
| timeout | number | Tool call timeout |
| connect_timeout | number | Initial connection timeout (also bounds the MCPinitializehandshake) |
| idle_timeout_seconds | number | Recycle a stdio server after this many seconds without a tool call (0= never, default). The server restarts transparently on the next tool call. |
| max_lifetime_seconds | number | Recycle a stdio server after this total age (0= never, default). Restarts transparently on next use. |
| enabled | bool | Iffalse, Hermes skips the server entirely |
| supports_parallel_tool_calls | bool | Iftrue, tools from this server may run concurrently |
| tools | mapping | Per-server tool filtering and utility policy |

`command`
`args`
`env`
`url`
`headers`
`client_cert`
`[cert, key]`
`[cert, key, password]`
`client_key`
`client_cert`
`timeout`
`connect_timeout`
`initialize`
`idle_timeout_seconds`
`0`
`max_lifetime_seconds`
`0`
`enabled`
`false`
`supports_parallel_tool_calls`
`true`
`tools`

### Minimal stdio example​

```
mcp_servers:  filesystem:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
```

### Recycling memory-heavy stdio servers​

Browser-based MCP servers (e.g.@playwright/mcp) keep a full Chromium
resident after their first tool call — hundreds of MB that never get
released. Opt in to automatic recycling and the server is torn down after
the idle/lifetime limit, then restarted transparently the next time one of
its tools is called (its tools stay registered the whole time):

`@playwright/mcp`

```
mcp_servers:  playwright:    command: "npx"    args: ["-y", "@playwright/mcp@latest", "--headless"]    idle_timeout_seconds: 900     # recycle after 15 min without a tool call    max_lifetime_seconds: 86400   # and at least once a day regardless
```

### Minimal HTTP example​

```
mcp_servers:  company_api:    url: "https://mcp.internal.example.com"    headers:      Authorization: "Bearer ***"
```

## Built-in presets​

For well-known MCP servers,hermes mcp addaccepts a--presetflag that fills in the transport details so you don't have to look up the command and args. The preset only supplies defaults — anything else (env vars, headers, filtering) you pass on the same command line still wins.

`hermes mcp add`
`--preset`

| Preset | What it wires up |
| --- | --- |
| codex | The Codex CLI's MCP server (codex mcp-serverover stdio). Requires thecodexCLI on PATH. |

`codex`
`codex mcp-server`
`codex`

```
# Add Codex CLI as an MCP server in one linehermes mcp add codex --preset codex
```

That writes the equivalent of:

```
mcp_servers:  codex:    command: "codex"    args: ["mcp-server"]
```

You can pick any local name (hermes mcp add my-codex --preset codexis fine); the preset only provides thecommand/argsdefaults.

`hermes mcp add my-codex --preset codex`
`command`
`args`

## How Hermes registers MCP tools​

Hermes prefixes MCP tools so they do not collide with built-in names:

```
mcp_<server_name>_<tool_name>
```

Examples:

| Server | MCP tool | Registered name |
| --- | --- | --- |
| filesystem | read_file | mcp_filesystem_read_file |
| github | create-issue | mcp_github_create_issue |
| my-api | query.data | mcp_my_api_query_data |

`filesystem`
`read_file`
`mcp_filesystem_read_file`
`github`
`create-issue`
`mcp_github_create_issue`
`my-api`
`query.data`
`mcp_my_api_query_data`

In practice, you usually do not need to call the prefixed name manually — Hermes sees the tool and chooses it during normal reasoning.

## MCP utility tools​

When supported, Hermes also registers utility tools around MCP resources and prompts:

- list_resources
- read_resource
- list_prompts
- get_prompt

`list_resources`
`read_resource`
`list_prompts`
`get_prompt`

These are registered per server with the same prefix pattern, for example:

- mcp_github_list_resources
- mcp_github_get_prompt

`mcp_github_list_resources`
`mcp_github_get_prompt`

### Important​

These utility tools are now capability-aware:

- Hermes only registers resource utilities if the MCP session actually supports resource operations
- Hermes only registers prompt utilities if the MCP session actually supports prompt operations

So a server that exposes callable tools but no resources/prompts will not get those extra wrappers.

## Per-server filtering​

You can control which tools each MCP server contributes to Hermes, allowing fine-grained management of your tool namespace.

### Disable a server entirely​

```
mcp_servers:  legacy:    url: "https://mcp.legacy.internal"    enabled: false
```

Ifenabled: false, Hermes skips the server completely and does not even attempt a connection.

`enabled: false`

### Whitelist server tools​

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [create_issue, list_issues]
```

Only those MCP server tools are registered.

### Blacklist server tools​

```
mcp_servers:  stripe:    url: "https://mcp.stripe.com"    tools:      exclude: [delete_customer]
```

All server tools are registered except the excluded ones.

### Precedence rule​

If both are present:

```
tools:  include: [create_issue]  exclude: [create_issue, delete_issue]
```

includewins.

`include`

### Filter utility tools too​

You can also separately disable Hermes-added utility wrappers:

```
mcp_servers:  docs:    url: "https://mcp.docs.example.com"    tools:      prompts: false      resources: false
```

That means:

- tools.resources: falsedisableslist_resourcesandread_resource
- tools.prompts: falsedisableslist_promptsandget_prompt

`tools.resources: false`
`list_resources`
`read_resource`
`tools.prompts: false`
`list_prompts`
`get_prompt`

### Full example​

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [create_issue, list_issues, search_code]      prompts: false  stripe:    url: "https://mcp.stripe.com"    headers:      Authorization: "Bearer ***"    tools:      exclude: [delete_customer]      resources: false  legacy:    url: "https://mcp.legacy.internal"    enabled: false
```

## What happens if everything is filtered out?​

If your config filters out all callable tools and disables or omits all supported utilities, Hermes does not create an empty runtime MCP toolset for that server.

That keeps the tool list clean.

## Runtime behavior​

### Discovery time​

Hermes discovers MCP servers at startup and registers their tools into the normal tool registry.

### Dynamic Tool Discovery​

MCP servers can notify Hermes when their available tools change at runtime by sending anotifications/tools/list_changednotification. When Hermes receives this notification, it automatically re-fetches the server's tool list and updates the registry — no manual/reload-mcprequired.

`notifications/tools/list_changed`
`/reload-mcp`

This is useful for MCP servers whose capabilities change dynamically (e.g. a server that adds tools when a new database schema is loaded, or removes tools when a service goes offline).

The refresh is lock-protected so rapid-fire notifications from the same server don't cause overlapping refreshes. Prompt and resource change notifications (prompts/list_changed,resources/list_changed) are received but not yet acted on.

`prompts/list_changed`
`resources/list_changed`

### Reloading​

If you change MCP config, use:

```
/reload-mcp
```

This reloads MCP servers from config and refreshes the available tool list. For runtime tool changes pushed by the server itself, seeDynamic Tool Discoveryabove.

### Toolsets​

Each configured MCP server also creates a runtime toolset when it contributes at least one registered tool:

```
mcp-<server>
```

That makes MCP servers easier to reason about at the toolset level.

## Security model​

### Stdio env filtering​

For stdio servers, Hermes does not blindly pass your full shell environment.

Only explicitly configuredenvplus a safe baseline are passed through. This reduces accidental secret leakage.

`env`

### Config-level exposure control​

The new filtering support is also a security control:

- disable dangerous tools you do not want the model to see
- expose only a minimal whitelist for a sensitive server
- disable resource/prompt wrappers when you do not want that surface exposed

## Example use cases​

### GitHub server with a minimal issue-management surface​

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, update_issue]      prompts: false      resources: false
```

Use it like:

```
Show me open issues labeled bug, then draft a new issue for the flaky MCP reconnection behavior.
```

### Stripe server with dangerous actions removed​

```
mcp_servers:  stripe:    url: "https://mcp.stripe.com"    headers:      Authorization: "Bearer ***"    tools:      exclude: [delete_customer, refund_payment]
```

Use it like:

```
Look up the last 10 failed payments and summarize common failure reasons.
```

### Filesystem server for a single project root​

```
mcp_servers:  project_fs:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]
```

Use it like:

```
Inspect the project root and explain the directory layout.
```

## Troubleshooting​

### MCP server not connecting​

Check:

```
# Verify MCP deps are installed (already included in standard install)cd ~/.hermes/hermes-agent && uv pip install -e ".[mcp]"node --versionnpx --version
```

Then verify your config and restart Hermes.

### Tools not appearing​

Possible causes:

- the server failed to connect
- discovery failed
- your filter config excluded the tools
- the utility capability does not exist on that server
- the server is disabled withenabled: false

`enabled: false`

If you are intentionally filtering, this is expected.

### Why didn't resource or prompt utilities appear?​

Because Hermes now only registers those wrappers when both are true:

1. your config allows them
2. the server session actually supports the capability

This is intentional and keeps the tool list honest.

## Parallel Tool Calls​

By default, MCP tools run sequentially — one at a time. If your MCP server exposes tools that are safe to run concurrently (e.g. read-only queries, independent API calls), you can opt-in to parallel execution:

```
mcp_servers:  docs:    command: "docs-server"    supports_parallel_tool_calls: true
```

Whensupports_parallel_tool_callsistrue, Hermes may execute multiple tools from that server at the same time within a single tool-call batch, just like it does for built-in read-only tools (web_search, read_file, etc.).

`supports_parallel_tool_calls`
`true`

Only enable parallel calls for MCP servers whose tools are safe to run at the same time. If tools read and write shared state, files, databases, or external resources, review the read/write race conditions before enabling this setting.

## MCP Sampling Support​

MCP servers can request LLM inference from Hermes via thesampling/createMessageprotocol. This allows an MCP server to ask Hermes to generate text on its behalf — useful for servers that need LLM capabilities but don't have their own model access.

`sampling/createMessage`

Sampling isenabled by defaultfor all MCP servers (when the MCP SDK supports it). Configure it per-server under thesamplingkey:

`sampling`

```
mcp_servers:  my_server:    command: "my-mcp-server"    sampling:      enabled: true            # Enable sampling (default: true)      model: "openai/gpt-4o"  # Override model for sampling requests (optional)      max_tokens_cap: 4096     # Max tokens per sampling response (default: 4096)      timeout: 30              # Timeout in seconds per request (default: 30)      max_rpm: 10              # Rate limit: max requests per minute (default: 10)      max_tool_rounds: 5       # Max tool-use rounds in sampling loops (default: 5)      allowed_models: []       # Allowlist of model names the server may request (empty = any)      log_level: "info"        # Audit log level: debug, info, or warning (default: info)
```

The sampling handler includes a sliding-window rate limiter, per-request timeouts, and tool-loop depth limits to prevent runaway usage. Metrics (request count, errors, tokens used) are tracked per server instance.

To disable sampling for a specific server:

```
mcp_servers:  untrusted_server:    url: "https://mcp.example.com"    sampling:      enabled: false
```

## Running Hermes as an MCP server​

In addition to connectingtoMCP servers, Hermes can alsobean MCP server. This lets other MCP-capable agents (Claude Code, Cursor, Codex, or any MCP client) use Hermes's messaging capabilities — list conversations, read message history, and send messages across all your connected platforms.

### When to use this​

- You want Claude Code, Cursor, or another coding agent to send and read Telegram/Discord/Slack messages through Hermes
- You want a single MCP server that bridges to all of Hermes's connected messaging platforms at once
- You already have a running Hermes gateway with connected platforms

### Quick start​

```
hermes mcp serve
```

This starts a stdio MCP server. The MCP client (not you) manages the process lifecycle.

### MCP client configuration​

Add Hermes to your MCP client config. For example, in Claude Code's~/.claude/claude_desktop_config.json:

`~/.claude/claude_desktop_config.json`

```
{  "mcpServers": {    "hermes": {      "command": "hermes",      "args": ["mcp", "serve"]    }  }}
```

Or if you installed Hermes in a specific location:

```
{  "mcpServers": {    "hermes": {      "command": "/home/user/.hermes/hermes-agent/venv/bin/hermes",      "args": ["mcp", "serve"]    }  }}
```

### Available tools​

The MCP server exposes 10 tools, matching OpenClaw's channel bridge surface plus a Hermes-specific channel browser:

| Tool | Description |
| --- | --- |
| conversations_list | List active messaging conversations. Filter by platform or search by name. |
| conversation_get | Get detailed info about one conversation by session key. |
| messages_read | Read recent message history for a conversation. |
| attachments_fetch | Extract non-text attachments (images, media) from a specific message. |
| events_poll | Poll for new conversation events since a cursor position. |
| events_wait | Long-poll / block until the next event arrives (near-real-time). |
| messages_send | Send a message through a platform (e.g.telegram:123456,discord:#general). |
| channels_list | List available messaging targets across all platforms. |
| permissions_list_open | List pending approval requests observed during this bridge session. |
| permissions_respond | Allow or deny a pending approval request. |

`conversations_list`
`conversation_get`
`messages_read`
`attachments_fetch`
`events_poll`
`events_wait`
`messages_send`
`telegram:123456`
`discord:#general`
`channels_list`
`permissions_list_open`
`permissions_respond`

### Event system​

The MCP server includes a live event bridge that polls Hermes's session database for new messages. This gives MCP clients near-real-time awareness of incoming conversations:

```
# Poll for new events (non-blocking)events_poll(after_cursor=0)# Wait for next event (blocks up to timeout)events_wait(after_cursor=42, timeout_ms=30000)
```

Event types:message,approval_requested,approval_resolved

`message`
`approval_requested`
`approval_resolved`

The event queue is in-memory and starts when the bridge connects. Older messages are available throughmessages_read.

`messages_read`

### Options​

```
hermes mcp serve              # Normal modehermes mcp serve --verbose    # Debug logging on stderr
```

### How it works​

The MCP server reads conversation data directly from Hermes's session store (~/.hermes/sessions/sessions.jsonand the SQLite database). A background thread polls the database for new messages and maintains an in-memory event queue. For sending messages, it uses the same internal send engine (tools/send_message_tool.py) that powers cron delivery and thehermes sendCLI.

`~/.hermes/sessions/sessions.json`
`tools/send_message_tool.py`
`hermes send`

The gateway does NOT need to be running for read operations (listing conversations, reading history, polling events). It DOES need to be running for send operations, since the platform adapters need active connections.

### Current limits​

- The embeddedhermes mcp serveexposes astdio-onlyMCP server today. If you need an HTTP MCP server, run a separate adapter — or, much more commonly, use the MCPclientside of Hermes, which already speaks both stdio and HTTP (url+headersinmcp_servers.yaml/config.yaml; seeHTTP serversabove).
- Event polling at ~200ms intervals via mtime-optimized DB polling (skips work when files are unchanged)
- Noclaude/channelpush notification protocol yet
- Text-only sends (no media/attachment sending throughmessages_send)

`hermes mcp serve`
`url`
`headers`
`mcp_servers.yaml`
`config.yaml`
`claude/channel`
`messages_send`

## Related docs​

- Use MCP with Hermes
- CLI Commands
- Slash Commands
- FAQ

[Use MCP with Hermes](/docs/guides/use-mcp-with-hermes)
[CLI Commands](/docs/reference/cli-commands)
[Slash Commands](/docs/reference/slash-commands)
[FAQ](/docs/reference/faq)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/mcp.md)