---
layout: docs
title: "Features_Web Dashboard"
permalink: /docs/user-guide/features/web-dashboard/
---

- 
- Features
- Management
- Web Dashboard

# Web Dashboard

The web dashboard is a browser-based UI for managing your Hermes Agent installation. Instead of editing YAML files or running CLI commands, you can configure settings, manage API keys, and monitor sessions from a clean web interface.

Hosted-mode auth uses Nous Portal OAuth; if you also want the dashboard to talk to a real backend,hermes setup --portalwires up the model and tool gateway too. SeeNous Portal.

`hermes setup --portal`

## Quick Start​

```
hermes dashboard
```

This starts a local web server and openshttp://127.0.0.1:9119in your browser. The dashboard runs entirely on your machine — no data leaves localhost.

`http://127.0.0.1:9119`

### Options​

| Flag | Default | Description |
| --- | --- | --- |
| --port | 9119 | Port to run the web server on |
| --host | 127.0.0.1 | Bind address |
| --no-open | — | Don't auto-open the browser |
| --insecure | off | Allow binding to non-localhost hosts (DANGEROUS— exposes API keys on the network; pair with a firewall and strong auth) |
| --isolated | off | When launched from a named profile (worker dashboard), run a dedicated per-profile server instead of routing to the machine dashboard |

`--port`
`9119`
`--host`
`127.0.0.1`
`--no-open`
`--insecure`
`--isolated`
`worker dashboard`

```
# Custom porthermes dashboard --port 8080# Bind to all interfaces (use with caution on shared networks)hermes dashboard --host 0.0.0.0# Start without opening browserhermes dashboard --no-open
```

## Managing multiple profiles​

The dashboard is amachine-levelmanagement surface: one server manages
everyprofileon the machine. A profile switcher in the
sidebar (visible whenever more than one profile exists) decides which
profile the management pages read and write — Config, API Keys, Skills,
MCP, Models, and the Chat tab all follow it. While a profile other than
the dashboard's own is selected, an amber banner names the managed profile
so the write target is never ambiguous.

The selection lives in the URL (?profile=<name>), so deep links likehttp://127.0.0.1:9119/skills?profile=workerland with the switcher
preselected and survive refresh.

`?profile=<name>`
`http://127.0.0.1:9119/skills?profile=worker`

Launching the dashboard from a profile alias routes to the machine
dashboard instead of starting a second server:

```
worker dashboard# → already running: opens the browser at ?profile=worker# → not running:     starts the machine dashboard with "worker" preselected
```

Pass--isolatedto opt out and run a dedicated server scoped to that
profile (the pre-unification behavior — useful if you deliberately expose
different profiles' dashboards with different auth).

`--isolated`

TheChattab follows the switcher too: a scoped chat spawns its PTY
child with the selected profile'sHERMES_HOME, so the conversation runs
with that profile's model, skills, memory, and session history. Switching
profiles starts a fresh terminal session.

`HERMES_HOME`

What stays per-profile and isnotabsorbed by the switcher: gateway
processes (manage them viahermes -p <name> gateway …), each profile's
session database, and cron schedulers (the Cron page already aggregates
across profiles with its own filter).

`hermes -p <name> gateway …`

## Prerequisites​

The defaulthermes-agentinstall does not ship the HTTP stack or PTY helper — those are optional extras. Theweb dashboardneeds FastAPI and Uvicorn (webextra). TheChattab also needsptyprocessto spawn the embedded TUI behind a pseudo-terminal (ptyextra on POSIX). Install both with:

`hermes-agent`
`web`
`ptyprocess`
`pty`

```
cd ~/.hermes/hermes-agent && uv pip install -e ".[web,pty]"
```

Thewebextra pulls in FastAPI/Uvicorn;ptypulls inptyprocess(POSIX) orpywinpty(native Windows — note that the embedded TUI itself still requires WSL).cd ~/.hermes/hermes-agent && uv pip install -e ".[all]"includes both extras and is the easiest path if you also want messaging/voice/etc.

`web`
`pty`
`ptyprocess`
`pywinpty`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[all]"`

When you runhermes dashboardwithout the dependencies, it will tell you what to install. If the frontend hasn't been built yet andnpmis available, it builds automatically on first launch.

`hermes dashboard`
`npm`

The Chat tab is part of everyhermes dashboardlaunch — the embedded browser chat pane (running the TUI over PTY/WebSocket) is always available, with no extra flag required.

`hermes dashboard`

## Pages​

### Status​

The landing page shows a live overview of your installation:

- Agent versionand release date
- Gateway status— running/stopped, PID, connected platforms and their state
- Active sessions— count of sessions active in the last 5 minutes
- Recent sessions— list of the 20 most recent sessions with model, message count, token usage, and a preview of the conversation

The status page auto-refreshes every 5 seconds.

### Chat​

TheChattab embeds the full Hermes TUI (the same interface you get fromhermes --tui) directly in the browser. Everything you can do in the terminal TUI — slash commands, model picker, tool-call cards, markdown streaming, clarify/sudo/approval prompts, skin theming — works identically here, because the dashboard is running the real TUI binary and rendering its ANSI output throughxterm.jswith its WebGL renderer for pixel-perfect cell layout.

`hermes --tui`

How it works:

- /api/ptyopens a WebSocket authenticated with the dashboard's session token
- The server spawnshermes --tuibehind a POSIX pseudo-terminal
- Keystrokes travel to the PTY; ANSI output streams back to the browser
- xterm.js's WebGL renderer paints each cell to an integer-pixel grid; mouse tracking (SGR 1006), wide characters (Unicode 11), and box-drawing glyphs all render natively
- Resizing the browser window resizes the TUI via the@xterm/addon-fitaddon

`/api/pty`
`hermes --tui`
`@xterm/addon-fit`

Resume an existing session:from theSessionstab, click the play icon (▶) next to any session. That jumps to/chat?resume=<id>and launches the TUI with--resume, loading the full history.

`/chat?resume=<id>`
`--resume`

Session switcher (right rail):the Chat tab carries its own ChatGPT-style conversation list in a thin right rail beside the terminal, so you can swap conversations without leaving the page. The rail stacks the model picker on top and the session list directly below it; the terminal takes up most of the screen. The list shows your most recent sessions for the active profile — title (falling back to a message preview), relative last-active time, message count, and the source channel for non-CLI sessions. Click any row to resume it in place (the terminal respawns with that conversation's history); the active session is highlighted.New chatstarts a fresh session, and a refresh control re-pulls the list. The rail is read-only for switching — delete, rename, export, and bulk cleanup still live on theSessionstab. On narrow screens it folds into a slide-over panel.

Prerequisites:

- Node.js (same requirement ashermes --tui; the TUI bundle is built on first launch)
- ptyprocess— installed by theptyextra (cd ~/.hermes/hermes-agent && uv pip install -e ".[web,pty]", or[all]covers both)
- POSIX kernel (Linux, macOS, or WSL2).  The/chatterminal pane specifically needs a POSIX PTY — native Windows Python has no equivalent, so on a native Windows install the rest of the dashboard (sessions, jobs, metrics, config editor) works but the/chattab will show a banner telling you to use WSL2 for that feature.

`hermes --tui`
`ptyprocess`
`pty`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[web,pty]"`
`[all]`
`/chat`
`/chat`

Close the browser tab and the PTY is reaped cleanly on the server. Re-opening spawns a fresh session.

To pointHermes Desktopat a dashboard running on another machine instead of its own bundled backend, see the remote-backend section below.

### Connecting Hermes Desktop to a remote backend​

Hermes Desktop normally launches its own local backend, but it can also attach to a dashboard running on a remote machine (a VM, a homelab box, etc.) viaSettings → Gateway → Remote gateway. This is the most common source of "Desktop says the backend is ready but chat never works" reports, because Desktop's readiness check verifies less than the live chat connection actually needs.

`hermes dashboard`

The "remote backend" Desktop connects toisahermes dashboardprocess running on the remote machine — the same server this page documents. It has to be up and reachable before any of the steps below matter; Desktop attaches to it, it doesn't start it for you. Keep it running undersystemd/tmux/etc. so it survives logout and reboots. Thegateway(Telegram/Discord/Slack/etc.) is aseparatelong-running process — start it independently if you rely on messaging channels; it is not the thing the desktop app connects to.

`hermes dashboard`
`systemd`
`tmux`

Desktop's "remote backend is ready" probe only hitsGET /api/status, which is a public endpoint — it answers as soon asanydashboard is running on the host. The live chat connection is aseparateWebSocket to/api/ws(and/api/pty), and that socket is gated by two more checks the status probe never touches:

`GET /api/status`
`/api/ws`
`/api/pty`
1. You must be authenticated.When the dashboard is bound to a non-loopback address it engages its auth gate. Protect it with a username and password (the bundledusername/password provider); Desktop signs in once and reuses the resulting session for the WebSocket via a single-use ticket. Without a configured provider, a non-loopback dashboardfails closed at startup.
2. The bind host must allow the client and match the Host header.A loopback bind (127.0.0.1) only accepts loopback clients, so a remote machine is rejected at the socket layer regardless of credentials. Bind to a non-loopback address (--host 0.0.0.0) so the peer-IP guard lets the remote client through. The remote URL you enter in Desktop must reach the dashboard by the same host it bound to — the DNS-rebinding guard requires the Host header to match.

`127.0.0.1`
`--host 0.0.0.0`

#### Remote dashboard setup​

Set a username and password, then run the dashboard bound to a reachable address. For asystemdservice:

`systemd`

```
[Service]EnvironmentFile=%h/.hermes/.envExecStart=/path/to/venv/bin/python -m hermes_cli.main dashboard \    --host 0.0.0.0 --port 9119 --no-open
```

with~/.hermes/.envcontaining:

`~/.hermes/.env`

```
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=adminHERMES_DASHBOARD_BASIC_AUTH_PASSWORD=choose-a-strong-passwordHERMES_DASHBOARD_BASIC_AUTH_SECRET=<32+ random bytes; openssl rand -base64 32>
```

Then in Desktop enter theRemote URL(e.g.http://VM_IP:9119) andSign inwith that username and password. See theusername/password providersection for the full configuration surface.

`http://VM_IP:9119`

From any machine, check that the dashboard advertises the username/password provider:

```
curl -s http://VM_IP:9119/api/status | jq '.auth_required, .auth_providers'# true# ["basic"]
```

- auth_required: trueand"basic"in the providers list → Desktop'sSign inflow will work.
- auth_required: false→ the bind is loopback, or the gate didn't engage. Bind to a non-loopback address.
- auth_required: truebut no"basic"provider → the username/password env vars aren't loaded. Fix those first.

`auth_required: true`
`"basic"`
`auth_required: false`
`auth_required: true`
`"basic"`

If/api/statusshows the gate is on with the"basic"provider and Desktopstillfails to connect after signing in, the issue is past basic setup — grab a freshdesktop.log(Settings → Gateway → Open logs) plus the dashboard's logs from the same retry window and look for the/api/wsclose code (4403 = chat WS rejected by the request guard, e.g. Host/peer mismatch; 4401 = the WS ticket didn't authenticate).

`/api/status`
`"basic"`
`desktop.log`
`/api/ws`

### Config​

A form-based editor forconfig.yaml. All 150+ configuration fields are auto-discovered fromDEFAULT_CONFIGand organized into tabbed categories:

`config.yaml`
`DEFAULT_CONFIG`
- model— default model, provider, base URL, reasoning settings
- terminal— backend (local/docker/ssh/modal), timeout, shell preferences
- display— skin, tool progress, resume display, spinner settings
- agent— max iterations, gateway timeout, service tier
- delegation— subagent limits, reasoning effort
- memory— provider selection, context injection settings
- approvals— dangerous command approval mode (ask/yolo/deny)
- And more — every section of config.yaml has corresponding form fields

Fields with known valid values (terminal backend, skin, approval mode, etc.) render as dropdowns. Booleans render as toggles. Everything else is a text input.

Actions:

- Save— writes changes toconfig.yamlimmediately
- Reset to defaults— reverts all fields to their default values (doesn't save until you click Save)
- Export— downloads the current config as JSON
- Import— uploads a JSON config file to replace the current values

`config.yaml`

Config changes take effect on the next agent session or gateway restart. The web dashboard edits the sameconfig.yamlfile thathermes config setand the gateway read from.

`config.yaml`
`hermes config set`

### API Keys​

Manage the.envfile where API keys and credentials are stored. Keys are grouped by category:

`.env`
- LLM Providers— OpenRouter, Anthropic, OpenAI, DeepSeek, etc.
- Tool API Keys— Browserbase, Firecrawl, Tavily, ElevenLabs, etc.
- Messaging Platforms— Telegram, Discord, Slack bot tokens, etc.
- Agent Settings— non-secret env vars likeAPI_SERVER_ENABLED

`API_SERVER_ENABLED`

Each key shows:

- Whether it's currently set (with a redacted preview of the value)
- A description of what it's for
- A link to the provider's signup/key page
- An input field to set or update the value
- A delete button to remove it

Advanced/rarely-used keys are hidden by default behind a toggle.

### Sessions​

Browse and inspect all agent sessions. Each row shows the session title, source platform icon (CLI, Telegram, Discord, Slack, cron), model name, message count, tool call count, and how long ago it was active. Live sessions are marked with a pulsing badge.

- Search— full-text search across all message content using FTS5. Results show highlighted snippets and auto-scroll to the first matching message when expanded.
- Stats— a summary bar shows total sessions, how many are active in the store, archived count, total messages, and a per-source breakdown.
- Expand— click a session to load its full message history. Messages are color-coded by role (user, assistant, system, tool) and rendered as Markdown with syntax highlighting.
- Tool calls— assistant messages with tool calls show collapsible blocks with the function name and JSON arguments.
- Rename— set or clear a session's title inline (pencil icon).
- Export— download a session (metadata + full message history) as JSON (download icon).
- Prune— the header "Prune old sessions" button deletes ended sessions older than N days.
- Delete— remove a session and its message history with the trash icon.

### Logs​

View agent, gateway, and error log files with filtering and live tailing.

- File— switch betweenagent,errors, andgatewaylog files
- Level— filter by log level: ALL, DEBUG, INFO, WARNING, or ERROR
- Component— filter by source component: all, gateway, agent, tools, cli, or cron
- Lines— choose how many lines to display (50, 100, 200, or 500)
- Auto-refresh— toggle live tailing that polls for new log lines every 5 seconds
- Color-coded— log lines are colored by severity (red for errors, yellow for warnings, dim for debug)

`agent`
`errors`
`gateway`

### Analytics​

Usage and cost analytics computed from session history. Select a time period (7, 30, or 90 days) to see:

- Summary cards— total tokens (input/output), cache hit percentage, total estimated or actual cost, and total session count with daily average
- Daily token chart— stacked bar chart showing input and output token usage per day, with hover tooltips showing breakdowns and cost
- Daily breakdown table— date, session count, input tokens, output tokens, cache hit rate, and cost for each day
- Per-model breakdown— table showing each model used, its session count, token usage, and estimated cost

### Cron​

Create and manage scheduled cron jobs that run agent prompts on a recurring schedule.

- Create— fill in a name (optional), prompt, cron expression (e.g.0 9 * * *), and delivery target (local, Telegram, Discord, Slack, or email)
- Job list— each job shows its name, prompt preview, schedule expression, state badge (enabled/paused/error), delivery target, last run time, and next run time
- Pause / Resume— toggle a job between active and paused states
- Edit— open a pre-filled modal to change a job's prompt, schedule, name, or delivery target
- Trigger now— immediately execute a job outside its normal schedule
- Delete— permanently remove a cron job

`0 9 * * *`

### Profiles​

Create and manageprofiles— isolated Hermes instances with their own config, skills, and sessions.

- Profile cards— each shows its model/provider, skill count, gateway state, description, and badges (active, default, alias)
- Create— name + optional clone-from-default / clone-everything / no-bundled-skills, description, and model; the dedicated Profile Builder page (/profiles/new) offers the full flow (model, MCPs, skills)
- Manage skills & tools— jumps to the Skills page scoped to that profile (sets the sidebar profile switcher)
- Set as active— flips the sticky default thatfuture CLI/gateway runspick up (same ashermes profile use). This doesnotchange what the dashboard manages — that's the profile switcher's job
- Edit model / description / SOUL— inline editors writing into that profile
- Rename / Delete— named profiles only

`/profiles/new`
`hermes profile use`

### Skills​

Browse, search, and toggle installed skills and toolsets, and install new ones from the hub. Skills are loaded from~/.hermes/skills/and grouped by category.

`~/.hermes/skills/`
- Search— filter installed skills and toolsets by name, description, or category
- Category filter— click category pills to narrow the list (e.g. MLOps, MCP, Red Teaming, AI)
- Toggle— enable or disable individual skills with a switch. Changes take effect on the next session.
- Toolsets— a separate view shows built-in toolsets (file operations, web browsing, etc.) with their active/inactive status, setup requirements, and list of included tools
- Browse hub— a third view searches the skill hub across all sources (the same ashermes skills search), installs any result by identifier with a live install log, and offers an "Update all" button to refresh installed skills.

`hermes skills search`

### MCP​

ManageMCPservers without the CLI. The samemcp_serversblock inconfig.yamlthathermes mcpreads from.

`mcp_servers`
`config.yaml`
`hermes mcp`

Your MCP servers:

- Add— register an HTTP/SSE server (URL) or a stdio server (command + args), with optionalKEY=VALUEenvironment variables for stdio servers
- Enable / disable— toggle a server on or off without deleting it. A disabled server stays in config so you can re-enable it later. Takes effect on the next gateway restart.
- Test— connect to a server, list its tools, and disconnect — verifies the connection before the agent depends on it
- Remove— delete a server from the config
- Secret-shaped env values are redacted in the list view

`KEY=VALUE`

Catalog:browse the Nous-approved MCP servers (the bundledoptional-mcps/catalog) and install any of them with one click. Entries that need API keys
prompt for them inline; the values go to.env. This is the same cataloghermes mcp catalog/hermes mcp installuse.

`optional-mcps/`
`.env`
`hermes mcp catalog`
`hermes mcp install`

### Webhooks​

Manage dynamicwebhook subscriptions. The
webhook platform must be enabled in messaging settings first; the page shows a
hint when it isn't.

- Create— name, description, event filter, delivery target, optional direct-delivery mode, and an agent prompt. On creation the page surfaces the route URL and the one-time HMAC secret to copy.
- Enable / disable— toggle a subscription on or off. Disabled routes stay in the subscriptions file but the gateway rejects their incoming events (403). The gateway hot-reloads the file, so the change takes effect on the next event — no restart needed.
- List— each subscription shows its URL, events, and delivery target
- Delete— remove a subscription

### Pairing​

Approve and revoke messaging users without the CLI — how a remote admin
onboards Telegram/Discord/etc. users to a paired gateway. Full parity withhermes pairing.

`hermes pairing`
- Pending requests— each shows platform, code, user, and age, with an Approve button
- Approved users— each shows platform and user, with a Revoke button
- Clear pending— drop all outstanding pairing codes

### Channels​

Connect Hermes to any messaging platform from the browser — full parity withhermes setup gateway. The page lists every supported channel (Telegram,
Discord, Slack, Matrix, Mattermost, WhatsApp, Signal, BlueBubbles/iMessage,
Email, SMS/Twilio, DingTalk, Feishu/Lark, WeCom, WeChat, QQ Bot, Yuanbao, plus
the API server and webhook endpoints) with its live connection status.

`hermes setup gateway`
- Configure— open a per-platform form with exactly the fields that channel needs (bot token, app token, server URL, allowlist, etc.). Secrets render as password inputs and are stored redacted; leaving a field blank keeps the existing value. Required fields are marked and validated. A "Setup guide" link points to the platform's credential docs.
- Enable / disable— toggle a channel on or off. The credential stays on disk; only the active state changes.
- Test— check whether the channel is configured, enabled, and reporting a live connection from the gateway.
- Restart gateway— credentials are written to~/.hermes/.envand the enabled flag toconfig.yaml; the gateway connects each enabled channel on its next restart, which you can trigger right from the page.

`~/.hermes/.env`
`config.yaml`

### System​

A consolidated administration panel for installation-wide operations:

- Host— live system stats: OS / kernel, architecture, hostname, Python and Hermes versions, CPU core count + utilization, memory, disk usage of the Hermes home, uptime, and load average. (CPU/memory/disk come frompsutilwhen installed; identity fields are always shown.) The Hermes version shows anupdate-status badge(up to date / N commits behind) and aCheck for updatesbutton. When an update is available on a git or pip install, anUpdate nowbutton opens a confirmation dialog — showing how many commits you'll pull — before runninghermes updatein the background. On Docker/Nix/Homebrew installs the dashboard can't apply the update in place, so it shows the correct out-of-band command instead.
- Nous Portal— login status, the active inference provider, and the Tool Gateway routing table (which tools run via the Portal vs. locally), with a link to manage your subscription. Read-only mirror ofhermes portal.
- Skill curator— the background skill-maintenance status (active / paused, interval, last run) with pause/resume and a run-now button. Mirrorshermes curator.
- Gateway— start, stop, and restart the messaging gateway, with live status (running/stopped, PID, state)
- Memory— pick the external memory provider (or built-in only), and reset the built-inMEMORY.md/USER.mdstores
- Credential pool— add and remove the rotating API keys the agent round-robins through (per provider). Keys are redacted in the list; the raw value only ever reaches the agent.
- Operations— rundoctor, a security audit, create a backup, restore from a backup archive, update skills, show the system-prompt size breakdown, generate a support dump, or migrate config for retired settings. Each spawns a background action whose live log streams into the page.
- Checkpoints— see the/rollbackshadow store size and prune it
- Shell hooks— list configured hooks with their consent + executable status,createa hook (event, command, matcher, timeout, with an opt-in consent grant), and remove one. Hooks run arbitrary commands, so the create form carries a security warning and the hook only fires after consent is granted.

`psutil`
`hermes update`
`hermes portal`
`hermes curator`
`MEMORY.md`
`USER.md`
`doctor`
`/rollback`

Creating a shell hook (note the consent checkbox and the run-arbitrary-commands warning):

The web dashboard reads and writes your.envfile, which contains API keys and secrets. It binds to127.0.0.1by default — only accessible from your local machine. If you bind to0.0.0.0, anyone on your network can view and modify your credentials. The dashboard has no authentication of its own.

`.env`
`127.0.0.1`
`0.0.0.0`

## /reloadSlash Command​

`/reload`

The dashboard PR also adds a/reloadslash command to the interactive CLI. After changing API keys via the web dashboard (or by editing.envdirectly), use/reloadin an active CLI session to pick up the changes without restarting:

`/reload`
`.env`
`/reload`

```
You → /reload  Reloaded .env (3 var(s) updated)
```

This re-reads~/.hermes/.envinto the running process's environment. Useful when you've added a new provider key via the dashboard and want to use it immediately.

`~/.hermes/.env`

## REST API​

The web dashboard exposes a REST API that the frontend consumes. You can also call these endpoints directly for automation:

The management endpoint families —/api/config,/api/env,/api/skills,/api/tools/toolsets,/api/mcp, and/api/model/{info,options,auxiliary,set}—
accept an optional?profile=<name>query parameter (or"profile"in the
JSON body for writes) that scopes the read/write to that profile'sHERMES_HOME. Omitted = the dashboard's own profile. Unknown profile names
return404. The/api/ptyWebSocket accepts the same parameter to spawn
a chat under the selected profile.

`/api/config`
`/api/env`
`/api/skills`
`/api/tools/toolsets`
`/api/mcp`
`/api/model/{info,options,auxiliary,set}`
`?profile=<name>`
`"profile"`
`HERMES_HOME`
`404`
`/api/pty`

### GET /api/status​

Returns agent version, gateway status, platform states, and active session count.

### GET /api/sessions​

Returns the 20 most recent sessions with metadata (model, token counts, timestamps, preview).

### GET /api/config​

Returns the currentconfig.yamlcontents as JSON.

`config.yaml`

### GET /api/config/defaults​

Returns the default configuration values.

### GET /api/config/schema​

Returns a schema describing every config field — type, description, category, and select options where applicable. The frontend uses this to render the correct input widget for each field.

### PUT /api/config​

Saves a new configuration. Body:{"config": {...}}.

`{"config": {...}}`

### GET /api/env​

Returns all known environment variables with their set/unset status, redacted values, descriptions, and categories.

### PUT /api/env​

Sets an environment variable. Body:{"key": "VAR_NAME", "value": "secret"}.

`{"key": "VAR_NAME", "value": "secret"}`

### DELETE /api/env​

Removes an environment variable. Body:{"key": "VAR_NAME"}.

`{"key": "VAR_NAME"}`

### GET /api/sessions/{session_id}​

Returns metadata for a single session.

### GET /api/sessions/{session_id}/messages​

Returns the full message history for a session, including tool calls and timestamps.

### GET /api/sessions/search​

Full-text search across message content. Query parameter:q. Returns matching session IDs with highlighted snippets.

`q`

### DELETE /api/sessions/{session_id}​

Deletes a session and its message history.

### GET /api/logs​

Returns log lines. Query parameters:file(agent/errors/gateway),lines(count),level,component.

`file`
`lines`
`level`
`component`

### GET /api/analytics/usage​

Returns token usage, cost, and session analytics. Query parameter:days(default 30). Response includes daily breakdowns and per-model aggregates.

`days`

### GET /api/cron/jobs​

Returns all configured cron jobs with their state, schedule, and run history.

### POST /api/cron/jobs​

Creates a new cron job. Body:{"prompt": "...", "schedule": "0 9 * * *", "name": "...", "deliver": "local"}.

`{"prompt": "...", "schedule": "0 9 * * *", "name": "...", "deliver": "local"}`

### POST /api/cron/jobs/{job_id}/pause​

Pauses a cron job.

### POST /api/cron/jobs/{job_id}/resume​

Resumes a paused cron job.

### POST /api/cron/jobs/{job_id}/trigger​

Immediately triggers a cron job outside its schedule.

### DELETE /api/cron/jobs/{job_id}​

Deletes a cron job.

### GET /api/skills​

Returns all skills with their name, description, category, and enabled status.

### PUT /api/skills/toggle​

Enables or disables a skill. Body:{"name": "skill-name", "enabled": true}.

`{"name": "skill-name", "enabled": true}`

### GET /api/tools/toolsets​

Returns all toolsets with their label, description, tools list, and active/configured status.

### Admin endpoints​

These power the MCP, Channels, Webhooks, Pairing, and System pages. All sit behind the
same auth gate as the rest of/api/.

`/api/`
| Method & path | Purpose |
| --- | --- |
| GET /api/mcp/servers | List configured MCP servers (env values redacted) |
| POST /api/mcp/servers | Add a server. Body:{name, url?, command?, args?, env?, auth?} |
| POST /api/mcp/servers/{name}/test | Connect, list tools, disconnect |
| PUT /api/mcp/servers/{name}/enabled | Enable / disable a server |
| DELETE /api/mcp/servers/{name} | Remove a server |
| GET /api/mcp/catalog | Browse the Nous-approved MCP catalog |
| POST /api/mcp/catalog/install | Install a catalog entry (with required env) |
| GET /api/messaging/platforms | List every messaging channel with status + per-platform setup fields |
| PUT /api/messaging/platforms/{id} | Configure a channel. Body:{enabled?, env?, clear_env?}(env writes to.env, enabled toconfig.yaml) |
| POST /api/messaging/platforms/{id}/test | Report whether a channel is configured, enabled, and connected |
| GET /api/pairing | List pending + approved messaging users |
| POST /api/pairing/approve | Approve a code. Body:{platform, code} |
| POST /api/pairing/revoke | Revoke a user. Body:{platform, user_id} |
| POST /api/pairing/clear-pending | Drop all pending codes |
| GET /api/webhooks | List subscriptions + platform-enabled status |
| POST /api/webhooks | Create a subscription (returns one-time secret) |
| DELETE /api/webhooks/{name} | Remove a subscription |
| GET /api/credentials/pool | List pooled rotation keys (redacted) |
| POST /api/credentials/pool | Add a key. Body:{provider, api_key, label?} |
| DELETE /api/credentials/pool/{provider}/{index} | Remove a key (1-based index) |
| GET /api/memory | Active provider + available providers + built-in file sizes |
| PUT /api/memory/provider | Select a provider (empty = built-in only) |
| POST /api/memory/reset | Reset built-in memory. Body:{target: all|memory|user} |
| POST /api/gateway/start·/stop·/restart | Gateway lifecycle (backgrounded) |
| POST /api/ops/doctor·/security-audit·/backup·/import | Diagnostics & maintenance (backgrounded; tail via/api/actions/{name}/status) |
| GET /api/ops/hooks | Configured shell hooks + allowlist status |
| GET /api/ops/checkpoints·POST .../prune | Inspect / prune the/rollbackstore |
| POST /api/ops/hooks·DELETE /api/ops/hooks | Create / remove a shell hook (consent-gated) |
| GET /api/system/stats | Host stats — OS, CPU, memory, disk, uptime |
| GET /api/hermes/update/check | Report update availability (commits behind, install method) without applying. For git/pip installs that are behind, also returns acommitslist (sha,summary,author,at) of what's changed.?force=1busts the 6h cache |
| GET /api/curator·PUT .../paused·POST .../run | Skill-curator status + pause/resume + run |
| GET /api/portal | Nous Portal auth + Tool Gateway routing (read-only) |
| POST /api/ops/prompt-size·/dump·/config-migrate | Diagnostics (backgrounded) |
| PUT /api/webhooks/{name}/enabled | Enable / disable a webhook route |
| POST /api/skills/hub/install·/uninstall·/update | Skills hub actions (backgrounded) |
| GET /api/skills/hub/search | Search the skill hub across all sources |
| GET /api/sessions/stats | Session-store statistics |
| PATCH /api/sessions/{id} | Rename / archive a session |
| GET /api/sessions/{id}/export | Export a session (metadata + messages) as JSON |
| POST /api/sessions/prune | Delete ended sessions older than N days |
| PUT /api/cron/jobs/{id} | Edit a cron job's prompt / schedule / name / deliver |

`GET /api/mcp/servers`
`POST /api/mcp/servers`
`{name, url?, command?, args?, env?, auth?}`
`POST /api/mcp/servers/{name}/test`
`PUT /api/mcp/servers/{name}/enabled`
`DELETE /api/mcp/servers/{name}`
`GET /api/mcp/catalog`
`POST /api/mcp/catalog/install`
`GET /api/messaging/platforms`
`PUT /api/messaging/platforms/{id}`
`{enabled?, env?, clear_env?}`
`.env`
`config.yaml`
`POST /api/messaging/platforms/{id}/test`
`GET /api/pairing`
`POST /api/pairing/approve`
`{platform, code}`
`POST /api/pairing/revoke`
`{platform, user_id}`
`POST /api/pairing/clear-pending`
`GET /api/webhooks`
`POST /api/webhooks`
`DELETE /api/webhooks/{name}`
`GET /api/credentials/pool`
`POST /api/credentials/pool`
`{provider, api_key, label?}`
`DELETE /api/credentials/pool/{provider}/{index}`
`GET /api/memory`
`PUT /api/memory/provider`
`POST /api/memory/reset`
`{target: all|memory|user}`
`POST /api/gateway/start`
`/stop`
`/restart`
`POST /api/ops/doctor`
`/security-audit`
`/backup`
`/import`
`/api/actions/{name}/status`
`GET /api/ops/hooks`
`GET /api/ops/checkpoints`
`POST .../prune`
`/rollback`
`POST /api/ops/hooks`
`DELETE /api/ops/hooks`
`GET /api/system/stats`
`GET /api/hermes/update/check`
`commits`
`sha`
`summary`
`author`
`at`
`?force=1`
`GET /api/curator`
`PUT .../paused`
`POST .../run`
`GET /api/portal`
`POST /api/ops/prompt-size`
`/dump`
`/config-migrate`
`PUT /api/webhooks/{name}/enabled`
`POST /api/skills/hub/install`
`/uninstall`
`/update`
`GET /api/skills/hub/search`
`GET /api/sessions/stats`
`PATCH /api/sessions/{id}`
`GET /api/sessions/{id}/export`
`POST /api/sessions/prune`
`PUT /api/cron/jobs/{id}`

## Authentication (gated mode)​

When the dashboard is bound to a public or non-loopback address — anything other than127.0.0.1/localhost— Hermes Agent engages an auth gate. Every request must carry a verified session cookie or it's bounced to the login page. Three providers ship in the box:

`127.0.0.1`
`localhost`
- Username/password— the simplest way to put auth on a self-hosted / on-prem / homelab dashboard. No external identity provider.Use it only on a trusted network or behind a VPN — not for public-internet exposure.
- OAuth (Nous Portal)— for hosted deployments and any dashboard reachable over the public internet, and the recommended path for aremote Hermes Desktop connection. Every login is verified against your Nous account, so this is the provider suitable for internet-facing use.
- Self-hosted OIDC— for bringing your own identity provider via standard OpenID Connect (Keycloak, Auth0, Okta, Google, GitHub via an OIDC bridge, etc.). No Nous Portal involved; suitable for public-internet exposure when fronted by a conformant OIDC server.

Operator-owned dashboards bound to loopback are unaffected — no auth, no login page.

### When the gate engages​

| Flags | Auth gate | Use case |
| --- | --- | --- |
| hermes dashboard(default — binds to127.0.0.1) | OFF | Local development |
| hermes dashboard --host 0.0.0.0 | ON | Remote / production — protect with the username/password provider or OAuth |

`hermes dashboard`
`127.0.0.1`
`hermes dashboard --host 0.0.0.0`

The gate is on if and only if:

1. The bind host is not127.0.0.1,::1,localhost, or0.0.0.0AND
2. The--insecureflag isnotset.

`127.0.0.1`
`::1`
`localhost`
`0.0.0.0`
`--insecure`
`--insecure`

--insecureskips the gate and serves an unauthenticated dashboard that reads/writes your.env(API keys, secrets) and can run agent commands.Do not use it for a remote connection.To expose the dashboard to another machine, configure theusername/password provider(or OAuth) and leave--insecureoff. The flag exists only as a last-resort escape hatch on a fully trusted, firewalled single-host network.

`--insecure`
`.env`
`--insecure`

### Fail-closed semantics​

If the gate would engage butnoDashboardAuthProvideris registered (no Nous plugin, no custom plugin),hermes dashboardrefuses to bind with an explicit error message. There is no "default-deny but accept everything" fallback — a misconfigured gated dashboard never starts.

`DashboardAuthProvider`
`hermes dashboard`

When you runhermes dashboard --host 0.0.0.0interactively(a real terminal) and no provider is configured yet, Hermes doesn't just fail — it offers to set one up on the spot: pickusername & password(writesdashboard.basic_authtoconfig.yamland you're running in seconds) orOAuth(points you athermes dashboard register). Non-interactive callers — Docker/s6, CI, piped runs — skip the prompt and hit the fail-closed error above, so an unattended deploy still never starts without auth.

`hermes dashboard --host 0.0.0.0`
`dashboard.basic_auth`
`config.yaml`
`hermes dashboard register`

### Default provider: Nous Research​

The bundledplugins/dashboard_auth/nousplugin isalways installedand auto-loaded. It auto-registers aDashboardAuthProvidernamednouswhen a client ID is configured.

`plugins/dashboard_auth/nous`
`DashboardAuthProvider`
`nous`

Because every login is verified against Nous Portal and protected by your Nous account,the Nous provider is the one suitable for exposing a dashboard to the public internet.

#### Registering a dashboard​

To use the Nous provider you need an OAuth client ID (shapeagent:{id}). There are two ways to get one:

`agent:{id}`
- CLI —hermes dashboard register.Run it on the host where the dashboard lives. It resolves your existing Nous login (runhermes setupfirst if you're not logged in), registers a self-hosted OAuth client with the Portal, and writesHERMES_DASHBOARD_OAUTH_CLIENT_IDinto~/.hermes/.envfor you. Optional flags:--name(a human-readable label, otherwise auto-generated) and--redirect-uri(a public HTTPS callback URL for an internet-facing host).hermes dashboard register# ✓ Registered dashboard "swift_falcon"# …writes HERMES_DASHBOARD_OAUTH_CLIENT_ID to ~/.hermes/.env
- GUI — the Local Dashboards page.Open/local-dashboardsin the Nous Portal to register, name, manage, and revoke self-hosted dashboards from the browser. Copy the resultingagent:{id}client ID intoHERMES_DASHBOARD_OAUTH_CLIENT_ID(env) ordashboard.oauth.client_id(config.yaml). This is also where you revoke a dashboard registered via the CLI.

CLI —hermes dashboard register.Run it on the host where the dashboard lives. It resolves your existing Nous login (runhermes setupfirst if you're not logged in), registers a self-hosted OAuth client with the Portal, and writesHERMES_DASHBOARD_OAUTH_CLIENT_IDinto~/.hermes/.envfor you. Optional flags:--name(a human-readable label, otherwise auto-generated) and--redirect-uri(a public HTTPS callback URL for an internet-facing host).

`hermes dashboard register`
`hermes setup`
`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`~/.hermes/.env`
`--name`
`--redirect-uri`

```
hermes dashboard register# ✓ Registered dashboard "swift_falcon"# …writes HERMES_DASHBOARD_OAUTH_CLIENT_ID to ~/.hermes/.env
```

GUI — the Local Dashboards page.Open/local-dashboardsin the Nous Portal to register, name, manage, and revoke self-hosted dashboards from the browser. Copy the resultingagent:{id}client ID intoHERMES_DASHBOARD_OAUTH_CLIENT_ID(env) ordashboard.oauth.client_id(config.yaml). This is also where you revoke a dashboard registered via the CLI.

`/local-dashboards`
`agent:{id}`
`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`dashboard.oauth.client_id`

#### Configuration​

The plugin reads from two surfaces, with the environment variable winning when set non-empty:

config.yaml— the canonical surface:

`config.yaml`

```
dashboard:  oauth:    client_id: agent:01HXYZ…             # required to engage the gate
```

Environment variables— operator overrides:

| Env var | Overrides | Format | Provisioned by |
| --- | --- | --- | --- |
| HERMES_DASHBOARD_OAUTH_CLIENT_ID | dashboard.oauth.client_id | agent:{instance_id} | hermes dashboard register |

`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`dashboard.oauth.client_id`
`agent:{instance_id}`
`hermes dashboard register`

Per the Hermes Agent convention (~/.hermes/.envis for API keys / secrets only),config.yamlis the recommended place to set these valuesfor local dev, on-prem, and any deployment you control directly. The environment-variable path exists so a hosting platform's secret injection can push per-deployclient_ids without anyone having to editconfig.yamlinside the image — that's its primary purpose.

`~/.hermes/.env`
`config.yaml`
`client_id`
`config.yaml`

Empty environment values are treated as unset, so a provisioned-but-not-populated platform secret can't accidentally shadow a validconfig.yamlentry.

`config.yaml`

If neither source provides a client_id, the plugin reports the specific reason and the dashboard's fail-closed bind error tells you exactly what to fix:

```
Refusing to bind dashboard to 0.0.0.0 — the OAuth auth gate engages onnon-loopback binds, but no auth providers are registered.Bundled providers reported these issues:  • nous: HERMES_DASHBOARD_OAUTH_CLIENT_ID is not set (and    dashboard.oauth.client_id in config.yaml is empty). The Nous Portal    provisions this env var (shape 'agent:{instance_id}') when it    deploys a Hermes Agent instance — set it to your provisioned    client id (either as an env var or under dashboard.oauth.client_id    in config.yaml), or pass --insecure to skip the OAuth gate entirely.Or pass --insecure to skip the auth gate (NOT recommended on untrustednetworks).
```

#### Worked example: Nous Research​

From a logged-in Hermes install to a Nous-gated dashboard in three steps.

1. Log in and register the dashboard.hermes dashboard registeruses your existing Nous login to provision an OAuth client and writesHERMES_DASHBOARD_OAUTH_CLIENT_IDinto~/.hermes/.envfor you:

`hermes dashboard register`
`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`~/.hermes/.env`

```
hermes setup            # if you're not already logged into Nous Portalhermes dashboard register# ✓ Registered dashboard "swift_falcon"# …writes HERMES_DASHBOARD_OAUTH_CLIENT_ID to ~/.hermes/.env
```

2. Run the dashboard on a reachable address.A non-loopback bind without--insecureengages the OAuth gate, and theclient_idjust written activates thenousprovider:

`--insecure`
`client_id`
`nous`

```
hermes dashboard --host 0.0.0.0 --port 9119 --no-open
```

3. Log in.Openhttp://<host>:9119/, you'll be bounced to/login. ClickSign in with Nous Research→ authenticate at the Portal → land back on the authenticated dashboard. Verify the gate from any machine:

`http://<host>:9119/`
`/login`

```
curl -s http://<host>:9119/api/status | jq '.auth_required, .auth_providers'# true# ["nous"]
```

GET /api/auth/methen returns the verified session (provider: nous). For an internet-facing host, register with--redirect-uri https://hermes.example.com/auth/callbackand setHERMES_DASHBOARD_PUBLIC_URLso the OAuth callback resolves to your public URL (seePublic URL override).

`GET /api/auth/me`
`provider: nous`
`--redirect-uri https://hermes.example.com/auth/callback`
`HERMES_DASHBOARD_PUBLIC_URL`

### Username/password provider (no OAuth IDP)​

If you don't want to wire up an OAuth identity provider — a self-hosted "just put a password on my dashboard" deployment — the bundledplugins/dashboard_auth/basicplugin registers aDashboardAuthProvidernamedbasicthat authenticates with ausername and passwordinstead of an OAuth redirect.

`plugins/dashboard_auth/basic`
`DashboardAuthProvider`
`basic`

It plugs into the same gate as the OAuth provider: the gate engages on a non-loopback bind without--insecure, the login page renders a credential form for this provider (instead of a "Log in with X" button), and everything downstream of login — session cookies, transparent refresh, WS tickets, logout, the audit log — is identical to the OAuth path. Sessions are stateless HMAC-signed tokens the provider mints itself, so there'sno database and no external IDP. Password hashing uses stdlibscrypt(no third-party dependency).

`--insecure`
`scrypt`

The username/password provider is intended for self-hosted / on-prem / homelab dashboards on atrusted network, or reachable only over aVPN. It protects a single shared credential with no external identity provider, MFA, or per-user accounts behind it, so it isnot suitable for exposing a dashboard directly to the public internet. For an internet-facing dashboard, use theNous Research provider(or your ownself-hosted OIDC/custom OAuthprovider) instead.

#### Configuration​

Like the Nous provider, it reads fromconfig.yaml(canonical) with environment variables winning when set non-empty. It activates only whenusernameplus eitherpassword_hash(preferred) orpasswordare configured — otherwise it's a no-op, so OAuth users and loopback/--insecureoperators are unaffected.

`config.yaml`
`username`
`password_hash`
`password`
`--insecure`

config.yaml:

`config.yaml`

```
dashboard:  basic_auth:    username: admin    # Preferred — no plaintext at rest. Compute with:    #   python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('PW'))"    password_hash: "scrypt$16384$8$1$…$…"    # ...or a plaintext password (hashed in-memory at load; less safe at rest):    # password: "s3cret"    secret: "<32+ random bytes, base64 or hex>"  # token-signing key    session_ttl_seconds: 43200                    # optional; access-token lifetime (default 12h)
```

Environment overrides:

| Env var | Overrides | Notes |
| --- | --- | --- |
| HERMES_DASHBOARD_BASIC_AUTH_USERNAME | dashboard.basic_auth.username | required to activate |
| HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH | dashboard.basic_auth.password_hash | preferred (no plaintext at rest) |
| HERMES_DASHBOARD_BASIC_AUTH_PASSWORD | dashboard.basic_auth.password | plaintext;wins over a configpassword_hashso you can rotate via env |
| HERMES_DASHBOARD_BASIC_AUTH_SECRET | dashboard.basic_auth.secret | token-signing key |
| HERMES_DASHBOARD_BASIC_AUTH_TTL_SECONDS | dashboard.basic_auth.session_ttl_seconds | access-token lifetime |

`HERMES_DASHBOARD_BASIC_AUTH_USERNAME`
`dashboard.basic_auth.username`
`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH`
`dashboard.basic_auth.password_hash`
`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`
`dashboard.basic_auth.password`
`password_hash`
`HERMES_DASHBOARD_BASIC_AUTH_SECRET`
`dashboard.basic_auth.secret`
`HERMES_DASHBOARD_BASIC_AUTH_TTL_SECONDS`
`dashboard.basic_auth.session_ttl_seconds`
`secret`

Whensecretis empty, a random per-process signing key is generated. That's fine for a single process, but it meansevery session is invalidated on restartand sessionsdon't span multiple workers. Set an explicitsecretfor restart-surviving / multi-worker deployments.

`secret`
`secret`

The/auth/password-loginendpoint is rate-limited per client IP (default 10 attempts/minute → HTTP 429) and returns a single generic401 Invalid credentialsfor both unknown users and wrong passwords, so it can't be used as a username-enumeration oracle.

`/auth/password-login`
`401 Invalid credentials`

#### Worked example: username/password​

From nothing to a password-gated dashboard on a trusted network in three steps.

1. Set credentials in~/.hermes/.env.Hash the password so no plaintext sits at rest, and set a stable signing secret so sessions survive restarts:

`~/.hermes/.env`

```
# Compute a scrypt hash of your chosen password:HASH=$(python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('choose-a-strong-password'))")cat >> ~/.hermes/.env <<EOFHERMES_DASHBOARD_BASIC_AUTH_USERNAME=adminHERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH=$HASHHERMES_DASHBOARD_BASIC_AUTH_SECRET=$(openssl rand -base64 32)EOFchmod 600 ~/.hermes/.env
```

2. Run the dashboard on a reachable address.A non-loopback bind without--insecureengages the gate, and the username + hash activate thebasicprovider:

`--insecure`
`basic`

```
hermes dashboard --host 0.0.0.0 --port 9119 --no-open
```

3. Log in.Openhttp://<host>:9119/, you'll be bounced to/login— acredential form(not a "Sign in with X" button). Enteradmin/ your password → land on the authenticated dashboard. Verify the gate from any machine:

`http://<host>:9119/`
`/login`
`admin`

```
curl -s http://<host>:9119/api/status | jq '.auth_required, .auth_providers'# true# ["basic"]
```

GET /api/auth/methen returns the verified session (provider: basic). Keep this behind a VPN — see the warning above; for a public host use theNous Researchorself-hosted OIDCprovider instead.

`GET /api/auth/me`
`provider: basic`

#### Writing your own password provider​

basicis just one implementation of an extension point. Any plugin can register a password provider: setsupports_password = Trueon yourDashboardAuthProvidersubclass and implementcomplete_password_login(*, username, password) -> Session(raiseInvalidCredentialsErroron rejection,ProviderErrorif your backing store is down). The OAuthstart_login/complete_loginmethods can be left asNotImplementedErrorstubs for a pure-password provider. This is the path for LDAP-bind, a credentials database, or any other non-redirect auth scheme — the framework handles the form, the route, the cookies, and refresh for you.

`basic`
`supports_password = True`
`DashboardAuthProvider`
`complete_password_login(*, username, password) -> Session`
`InvalidCredentialsError`
`ProviderError`
`start_login`
`complete_login`
`NotImplementedError`

### Self-hosted OIDC provider​

If you run your own identity provider, the bundledplugins/dashboard_auth/self_hostedplugin authenticates the dashboard against it usingstandard OpenID Connect— no per-IDP code, no Nous Portal involved. It's verified against and works with any conformant OIDC server:

`plugins/dashboard_auth/self_hosted`

> Authentik · Keycloak · Zitadel · Authelia · Auth0 · Okta · Google · …

Authentik · Keycloak · Zitadel · Authelia · Auth0 · Okta · Google · …

Like the Nous provider, it auto-loads and only registers itself once it's configured, so it's a no-op for loopback /--insecuredashboards.

`--insecure`

#### Configuration​

Configure anissuerand aclient_id(a public PKCE client — no client secret). The plugin fetches the IDP'sauthorization_endpoint,token_endpoint, andjwks_urifrom{issuer}/.well-known/openid-configuration, so you never hardcode endpoint URLs.

`authorization_endpoint`
`token_endpoint`
`jwks_uri`
`{issuer}/.well-known/openid-configuration`

config.yaml— the canonical surface:

`config.yaml`

```
dashboard:  oauth:    provider: self-hosted    self_hosted:      issuer: https://auth.example.com/application/o/hermes/   # required      client_id: hermes-dashboard                              # required      scopes: "openid profile email"                           # optional (this is the default)
```

Environment variables— operator overrides (env wins overconfig.yamlwhen set non-empty; an empty value is treated as unset):

`config.yaml`
| Env var | Overrides | Notes |
| --- | --- | --- |
| HERMES_DASHBOARD_OIDC_ISSUER | dashboard.oauth.self_hosted.issuer | OIDC issuer URL — required |
| HERMES_DASHBOARD_OIDC_CLIENT_ID | dashboard.oauth.self_hosted.client_id | Public client id — required |
| HERMES_DASHBOARD_OIDC_SCOPES | dashboard.oauth.self_hosted.scopes | Defaults toopenid profile email |

`HERMES_DASHBOARD_OIDC_ISSUER`
`dashboard.oauth.self_hosted.issuer`
`HERMES_DASHBOARD_OIDC_CLIENT_ID`
`dashboard.oauth.self_hosted.client_id`
`HERMES_DASHBOARD_OIDC_SCOPES`
`dashboard.oauth.self_hosted.scopes`
`openid profile email`

In your IDP, register apublicapplication/client with the authorization-code + PKCE (S256) grant and add the dashboard's callback as an allowed redirect URI. The callback is<dashboard public URL>/auth/callback(seePublic URL overridefor how the dashboard derives its public URL behind a proxy).

`<dashboard public URL>/auth/callback`

#### What it verifies​

The provider verifies the OpenID ConnectID token(RS256/ES256) against the discoveredjwks_uri, with theissandaudclaims pinned to your configuredissuerandclient_id. Standard OIDC claims map onto the dashboard session:

`jwks_uri`
`iss`
`aud`
`issuer`
`client_id`
| Session field | Claim(s) |
| --- | --- |
| user_id | sub(required) |
| email | email |
| display_name | name→preferred_username→nickname→email |
| org_id | org_id/organization, else joinedgroups |

`user_id`
`sub`
`email`
`email`
`display_name`
`name`
`preferred_username`
`nickname`
`email`
`org_id`
`org_id`
`organization`
`groups`

The ID token is what establishes identity — the access token is treated as opaque (the OIDC spec does not require it to be a JWT). Endpoint URLs are required to be HTTPS (loopbackhttp://is allowed for local-dev IDPs), and the discovery document's advertisedissuermust match your configured one (a trailing-slash difference is tolerated). Refresh tokens, when the IDP issues them, are used for silent re-auth via the standardrefresh_tokengrant; logout calls the IDP's RFC 7009revocation_endpointwhen advertised.

`http://`
`issuer`
`refresh_token`
`revocation_endpoint`

> Confidential clients(those with aclient_secret) are not supported yet — configure a public + PKCE client, which is the typical choice for a browser-facing dashboard.

Confidential clients(those with aclient_secret) are not supported yet — configure a public + PKCE client, which is the typical choice for a browser-facing dashboard.

`client_secret`

#### Worked example: Keycloak​

Keycloakis one of the easiest self-hosted OIDC servers to stand up for a local test — it runs as a single container in dev mode (in-memory DB) and exposes textbook OIDC discovery. This walkthrough gets you from nothing to a working dashboard login in a few minutes.

1. Run Keycloak with a pre-configured realm.Save this realm export asrealm-hermes.json— it defines ahermesrealm, apublic PKCE client(hermes-dashboard), and a test user, all imported on boot so there's nothing to click in the admin UI:

`realm-hermes.json`
`hermes`
`hermes-dashboard`

```
{  "realm": "hermes",  "enabled": true,  "clients": [    {      "clientId": "hermes-dashboard",      "name": "Hermes Agent Dashboard",      "enabled": true,      "publicClient": true,      "standardFlowEnabled": true,      "protocol": "openid-connect",      "redirectUris": ["http://localhost:9119/auth/callback"],      "webOrigins": ["http://localhost:9119"],      "attributes": { "pkce.code.challenge.method": "S256" }    }  ],  "users": [    {      "username": "testuser",      "enabled": true,      "emailVerified": true,      "email": "testuser@example.com",      "firstName": "Test",      "lastName": "User",      "credentials": [        { "type": "password", "value": "testpassword", "temporary": false }      ]    }  ]}
```

Start it (Keycloak 26+), mounting that file into the import directory:

```
docker run --rm -p 8080:8080 \  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \  -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \  -v "$PWD/realm-hermes.json:/opt/keycloak/data/import/realm-hermes.json:ro" \  quay.io/keycloak/keycloak:26.0 \  start-dev --import-realm
```

Once it's up, the realm advertises standard OIDC discovery athttp://localhost:8080/realms/hermes/.well-known/openid-configuration(issuerhttp://localhost:8080/realms/hermes). The admin console is athttp://localhost:8080/(admin/admin).

`http://localhost:8080/realms/hermes/.well-known/openid-configuration`
`http://localhost:8080/realms/hermes`
`http://localhost:8080/`
`admin`
`admin`

2. Point the dashboard at it.The self-hosted plugin permits a loopbackhttp://issuer (HTTPS is required for any non-loopback issuer), so the local Keycloak works as-is:

`http://`

```
export HERMES_DASHBOARD_OIDC_ISSUER="http://localhost:8080/realms/hermes"export HERMES_DASHBOARD_OIDC_CLIENT_ID="hermes-dashboard"export HERMES_DASHBOARD_PUBLIC_URL="http://localhost:9119"hermes dashboard --host 0.0.0.0 --port 9119 --no-open
```

HERMES_DASHBOARD_PUBLIC_URLtells the dashboard its OAuth callback ishttp://localhost:9119/auth/callback— the redirect URI the realm registered
above. Binding to0.0.0.0(a non-loopback bind) without--insecureis what
engages the OAuth gate.

`HERMES_DASHBOARD_PUBLIC_URL`
`http://localhost:9119/auth/callback`
`0.0.0.0`
`--insecure`

3. Log in.Openhttp://localhost:9119/, you'll be bounced to/login. ClickSign in with Self-Hosted OIDC→ authenticate at Keycloak astestuser/testpassword→ land back on the authenticated dashboard. The sidebar showsLogged in as Test User via self-hosted, andGET /api/auth/mereturns the verified session (provider: self-hosted,email: testuser@example.com).

`http://localhost:9119/`
`/login`
`testuser`
`testpassword`
`Logged in as Test User via self-hosted`
`GET /api/auth/me`
`provider: self-hosted`
`email: testuser@example.com`

> If you bind or browse on a different host/port, add that origin's…/auth/callbackto the client'sValid redirect URIsin the Keycloak
admin console (Clients → hermes-dashboard → Settings). The same pattern works
for Authentik, Zitadel, Authelia, and other OIDC servers — only the issuer
URL and client registration UI differ.

If you bind or browse on a different host/port, add that origin's…/auth/callbackto the client'sValid redirect URIsin the Keycloak
admin console (Clients → hermes-dashboard → Settings). The same pattern works
for Authentik, Zitadel, Authelia, and other OIDC servers — only the issuer
URL and client registration UI differ.

`…/auth/callback`

### Public URL override​

By default, the dashboard reconstructs the OAuth callback URL from the request —X-Forwarded-Host+X-Forwarded-Proto+X-Forwarded-Prefix(when uvicorn is configured withproxy_headers=True, whichstart_serverenables under the gate). This works out of the box behind a reverse proxy that sets all three headers correctly.

`X-Forwarded-Host`
`X-Forwarded-Proto`
`X-Forwarded-Prefix`
`proxy_headers=True`
`start_server`

For deploys behind reverse proxies that don't reliably forward those headers (manual nginx setups, on-prem ingresses, custom-domain deploys with partial proxy chains), setdashboard.public_url(orHERMES_DASHBOARD_PUBLIC_URL) to thecomplete public URLthe dashboard is reached at:

`dashboard.public_url`
`HERMES_DASHBOARD_PUBLIC_URL`

```
dashboard:  public_url: "https://dashboard.example.com/hermes"
```

When set, the OAuth callback URL becomes<public_url>/auth/callbackverbatim —X-Forwarded-Prefixis ignored on that code path because the operator has explicitly declared the public URL. This is intentional: stacking the prefix on top would double-prefix the common case where the prefix is already baked intopublic_url.

`<public_url>/auth/callback`
`X-Forwarded-Prefix`
`public_url`

Same precedence as the other dashboard settings — env wins overconfig.yaml:

`config.yaml`
| Surface | Override path | When to use |
| --- | --- | --- |
| dashboard.public_urlinconfig.yaml | HERMES_DASHBOARD_PUBLIC_URL | Local dev / on-prem (canonical) |
| HERMES_DASHBOARD_PUBLIC_URLenv var | — | Hosting-platform secrets / CI |
| (unset) | — | Default — reconstruct fromX-Forwarded-*headers |

`dashboard.public_url`
`config.yaml`
`HERMES_DASHBOARD_PUBLIC_URL`
`HERMES_DASHBOARD_PUBLIC_URL`
`X-Forwarded-*`

Validation rejects values withouthttp:///https://scheme, without a host, or containing quote / angle / whitespace / control characters. A malformed value silently falls through to header reconstruction so the login flow keeps working rather than dispatching the user to a hostile URL.

`http://`
`https://`

> Note:public_urloverrides the OAuth callback URL only. TheSecurecookie flag is still controlled byrequest.url.scheme(X-Forwarded-Proto under proxy_headers), so anhttp://public_urlon a TLS-terminated public deploy will produce non-Secure cookies. This is an operator footgun — pairpublic_urlwith proper TLS termination upstream.

Note:public_urloverrides the OAuth callback URL only. TheSecurecookie flag is still controlled byrequest.url.scheme(X-Forwarded-Proto under proxy_headers), so anhttp://public_urlon a TLS-terminated public deploy will produce non-Secure cookies. This is an operator footgun — pairpublic_urlwith proper TLS termination upstream.

`public_url`
`Secure`
`request.url.scheme`
`http://`
`public_url`
`public_url`

### OAuth flow​

The provider implements theNous Portal OAuth contract v1— authorization-code grant with PKCE (S256):

1. User hits/without a session cookie → gate redirects to/login.
2. Login page shows a "Continue with Nous Research" button →/auth/login?provider=nous.
3. Server stashes PKCE state in a short-lived cookie, redirects user tohttps://portal.nousresearch.com/oauth/authorize?….
4. User authenticates with Portal, lands at/auth/callback?code=…&state=….
5. Server exchanges the code for an access token atPOST /api/oauth/token, verifies the JWT signature against the Portal's JWKS (/.well-known/jwks.json), and sets thehermes_session_atcookie.
6. User is redirected to/(or to the original deep-link path via thenext=query parameter).

`/`
`/login`
`/auth/login?provider=nous`
`https://portal.nousresearch.com/oauth/authorize?…`
`/auth/callback?code=…&state=…`
`POST /api/oauth/token`
`/.well-known/jwks.json`
`hermes_session_at`
`/`
`next=`

Access tokens have a 15-minute TTL.There is no refresh token in contract v1— when the token expires, the SPA's fetch wrapper detects the 401 envelope and full-page-navigates back to/loginto re-run the flow.

`/login`

### Cookies set​

| Name | Lifetime | Notes |
| --- | --- | --- |
| hermes_session_at | Token TTL (15 min) | HttpOnly, SameSite=Lax, Secure-when-HTTPS |
| hermes_session_pkce | 10 min | HttpOnly; holds the PKCE verifier + provider hint during the round trip |
| hermes_session_rt | unused in v1 | Reserved for forward-compat; not written whenrefresh_tokenis empty |

`hermes_session_at`
`hermes_session_pkce`
`hermes_session_rt`
`refresh_token`

All three arePath=/andSameSite=Lax. TheSecureflag is set when the dashboard is reached over HTTPS (detected via the request URL scheme — honoursX-Forwarded-Protofrom an upstream TLS terminator underproxy_headers=True).

`Path=/`
`SameSite=Lax`
`Secure`
`X-Forwarded-Proto`
`proxy_headers=True`

### Logout​

The sidebar widget showsLogged in as <user_id…> via nouswith a logout icon. Clicking it POSTs/auth/logout, which clears all dashboard-auth cookies and redirects back to/login.

`Logged in as <user_id…> via nous`
`/auth/logout`
`/login`

### Audit log​

Every login start, success, failure, and session-verify failure is written as a JSON line to$HERMES_HOME/logs/dashboard-auth.log. Sensitive fields (access_token,refresh_token,code,code_verifier,state,Authorizationheader) are redacted before logging.

`$HERMES_HOME/logs/dashboard-auth.log`
`access_token`
`refresh_token`
`code`
`code_verifier`
`state`
`Authorization`

### Custom providers​

To plug a non-Nous OAuth provider (e.g. Google, GitHub, custom OIDC), create a plugin that registers aDashboardAuthProvider:

`DashboardAuthProvider`

```
# ~/.hermes/plugins/dashboard-auth-myidp/__init__.pyfrom hermes_cli.dashboard_auth import DashboardAuthProvider, Session, LoginStartclass MyIdPProvider(DashboardAuthProvider):    name = "myidp"    display_name = "My Identity Provider"    def start_login(self, *, redirect_uri): ...    def complete_login(self, *, code, state, code_verifier, redirect_uri): ...    def verify_session(self, *, access_token): ...    def refresh_session(self, *, refresh_token): ...    def revoke_session(self, *, refresh_token): ...def register(ctx):    ctx.register_dashboard_auth_provider(MyIdPProvider())
```

The login page lists all registered providers; multiple providers can be stacked and the user picks one at/login.

`/login`

### Non-interactive (bearer-token) auth​

Alongside interactive human login (session cookies + refresh), theDashboardAuthProviderABC supports anon-interactive, service-to-servicecapability viasupports_token = True+verify_token(token=...). When a provider opts in, an inboundAuthorization: Bearer <token>is verified and, on success, aTokenPrincipalis attached to the request (request.state.token_principal) for the endpoints that provider marks token-authable — no cookie, no redirect, no refresh.

`DashboardAuthProvider`
`supports_token = True`
`verify_token(token=...)`
`Authorization: Bearer <token>`
`TokenPrincipal`
`request.state.token_principal`

The bundled first consumer is thedrainprovider (plugins/dashboard_auth/drain):nous-account-serviceprovisions a per-agent secret viaHERMES_DASHBOARD_DRAIN_SECRET, and the provider verifies inbound bearer tokens against it with a constant-time compare, registering/api/gateway/drainas token-authable. Itfails closed— a weak/short secret (< 256 bits) is rejected at registration and the endpoint stays disabled; it's a no-op when the env var is unset. Behavioural knobs (scope,min_secret_chars) live underdashboard.drain_authinconfig.yaml.

`plugins/dashboard_auth/drain`
`nous-account-service`
`HERMES_DASHBOARD_DRAIN_SECRET`
`/api/gateway/drain`
`scope`
`min_secret_chars`
`dashboard.drain_auth`
`config.yaml`

Custom providers can implementsupports_token/verify_tokenthe same way to expose their own machine-authable endpoints.

`supports_token`
`verify_token`

### Verifying the gate is on​

```
# Quick env-var path.HERMES_DASHBOARD_OAUTH_CLIENT_ID=agent:test \  hermes dashboard --host 0.0.0.0# Or the equivalent via config.yaml (recommended for local dev / on-prem):##   dashboard:#     oauth:#       client_id: agent:test## then just:hermes dashboard --host 0.0.0.0# Hit /api/status to see the gate state:curl -s http://127.0.0.1:9119/api/status | jq '.auth_required, .auth_providers'# true# ["nous"]
```

The dashboard's React StatusPage shows the same fields under "Web server". A sidebar AuthWidget surfaces the current identity once you've signed in.

## Connecting Hermes Desktop to a remote backend​

Hermes Desktop can drive a Hermes backend running on another machine (a VPS, a home server, a Mini behind Tailscale). In the app this lives underSettings → Gateway → Remote gateway, which asks for aRemote URLand a way toSign in. (For the desktop app itself — install, settings, chat — see theHermes Desktoppage.)

You protect the remote dashboard with one of the bundled auth providers, and the desktop app signs in against whichever one the backend advertises. For a backend reachable beyond your own machine — a VPS, a public host, anything internet-facing — the recommended provider isOAuth (Nous Portal)(register it withhermes dashboard registerand sign in withSign in with Nous Research). The bundledusername/password provideris the quickest option when the backend is on a trusted LAN or reachable only over a VPN, but isnot suitable for direct public-internet exposure. Binding the dashboard to a non-loopback address engages its auth gate; once signed in, Desktop reuses the session for the chat WebSocket automatically — there is no token to copy or paste.

`hermes dashboard register`

The recipe below uses the username/password path because it's the quickest to stand up on a trusted network; for the OAuth path seeDefault provider: Nous Research.

### On the backend (the remote machine)​

```
# 1. Set the dashboard login credentials in ~/.hermes/.env (secrets file, 0600).cat >> ~/.hermes/.env <<'EOF'HERMES_DASHBOARD_BASIC_AUTH_USERNAME=adminHERMES_DASHBOARD_BASIC_AUTH_PASSWORD=choose-a-strong-password# Recommended: a stable signing secret so sessions survive restarts.HERMES_DASHBOARD_BASIC_AUTH_SECRET=$(openssl rand -base64 32)EOFchmod 600 ~/.hermes/.env# 2. Run the dashboard bound to a reachable address. The non-loopback bind#    engages the auth gate; the username/password provider handles login.hermes dashboard --no-open --host 0.0.0.0 --port 9119
```

Prefer no plaintext at rest? UseHERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASHwith a scrypt hash instead — seeUsername/password providerfor the full surface.

`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH`

If you run the dashboard as a systemd service,~/.hermes/.envis picked up automatically when the unit hasEnvironmentFile=%h/.hermes/.env, so the credentials are in the environment at boot.

`~/.hermes/.env`
`EnvironmentFile=%h/.hermes/.env`

The dashboard reads and writes your.env(API keys, secrets) and can run agent commands. Theusername/passwordsetup shown here is for a trusted network — never expose a password-protected dashboard directly to the open internet. Put it behind a VPN.Tailscaleis the clean option: bind to the machine's tailscale IP (--host <tailscale-ip>) and usehttp://<tailscale-ip>:9119as the Remote URL. Only devices on your tailnet can reach it. To reach a backend over the public internet, use theOAuth (Nous Portal)provider instead.

`.env`
`--host <tailscale-ip>`
`http://<tailscale-ip>:9119`

### In Hermes Desktop​

Settings → Gateway → Remote gateway:

- Remote URL—http://<backend-host>:9119(path prefixes like/hermesare supported if you front it with a reverse proxy)
- Sign in— the app detects the username/password gateway and shows aSign inbutton; click it and enter the credentials from step 1
- Save and reconnect— switches the desktop shell onto the remote backend

`http://<backend-host>:9119`
`/hermes`

The session refreshes automatically and survives restarts whenHERMES_DASHBOARD_BASIC_AUTH_SECRETis set on the backend.

`HERMES_DASHBOARD_BASIC_AUTH_SECRET`

### Environment-variable override​

Instead of the in-app setting, you can point the desktop at a backend with an env var before launching it. WhenHERMES_DESKTOP_REMOTE_URLis set, it overrides the saved in-app URL (the Gateway settings panel shows an "env override" badge and disables editing); you stillSign inwith your username and password from the panel.

`HERMES_DESKTOP_REMOTE_URL`
| Env var | Value |
| --- | --- |
| HERMES_DESKTOP_REMOTE_URL | http://<backend-host>:9119 |

`HERMES_DESKTOP_REMOTE_URL`
`http://<backend-host>:9119`

### Troubleshooting​

- "Remote gateway incomplete"— you haven't entered a remote URL.
- Sign-in fails with 401 / "Invalid credentials"— the username or password doesn't match the backend'sHERMES_DASHBOARD_BASIC_AUTH_USERNAME/HERMES_DASHBOARD_BASIC_AUTH_PASSWORD. The backend returns the same generic error for unknown user and wrong password, so check both. Confirm the gate withcurl -s http://<host>:9119/api/status | jq '.auth_required, .auth_providers'— it should reporttrueand include"basic".
- No "Sign in" button — it asks for a session token instead— the username/password provider isn't active (/api/statuswon't list"basic"). Make sure the username and a password (or password hash) are set and the dashboard process loaded them.
- Signed out on every restart— setHERMES_DASHBOARD_BASIC_AUTH_SECRETto a stable value; otherwise the signing key is regenerated per boot.
- Connection refused / times out— the backend bound to127.0.0.1(the default) instead of a reachable address, or a firewall/VPN is blocking the port. Bind to0.0.0.0or the tailscale IP and open the port to your trusted network.

`HERMES_DASHBOARD_BASIC_AUTH_USERNAME`
`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`
`curl -s http://<host>:9119/api/status | jq '.auth_required, .auth_providers'`
`true`
`"basic"`
`/api/status`
`"basic"`
`HERMES_DASHBOARD_BASIC_AUTH_SECRET`
`127.0.0.1`
`0.0.0.0`

## CORS​

The web server restricts CORS to localhost origins only:

- http://localhost:9119/http://127.0.0.1:9119(production)
- http://localhost:3000/http://127.0.0.1:3000
- http://localhost:5173/http://127.0.0.1:5173(Vite dev server)

`http://localhost:9119`
`http://127.0.0.1:9119`
`http://localhost:3000`
`http://127.0.0.1:3000`
`http://localhost:5173`
`http://127.0.0.1:5173`

If you run the server on a custom port, that origin is added automatically.

## Development​

If you're contributing to the web dashboard frontend:

```
# Terminal 1: start the backend APIhermes dashboard --no-open# Terminal 2: start the Vite dev server with HMRcd web/npm installnpm run dev
```

The Vite dev server athttp://localhost:5173proxies/apirequests to the FastAPI backend athttp://127.0.0.1:9119.

`http://localhost:5173`
`/api`
`http://127.0.0.1:9119`

The frontend is built with React 19, TypeScript, Tailwind CSS v4, and shadcn/ui-style components. Production builds output tohermes_cli/web_dist/which the FastAPI server serves as a static SPA.

`hermes_cli/web_dist/`

## Automatic Build on Update​

When you runhermes update, the web frontend is automatically rebuilt ifnpmis available. This keeps the dashboard in sync with code updates. Ifnpmisn't installed, the update skips the frontend build andhermes dashboardwill build it on first launch.

`hermes update`
`npm`
`npm`
`hermes dashboard`

## Themes & plugins​

The dashboard ships with six built-in themes and can be extended with user-defined themes, plugin tabs, and backend API routes — all drop-in, no repo clone needed.

Switch themes livefrom the header bar — click the palette icon next to the language switcher. Selection persists toconfig.yamlunderdashboard.themeand is restored on page load.

`config.yaml`
`dashboard.theme`

Change the font independentlyfrom the same picker — theFontsection below the theme list overrides the UI font of whatever theme is active. The choice persists across theme switches (config.yaml→dashboard.font); pickTheme defaultto clear it and return to the active theme's own font.

`config.yaml`
`dashboard.font`

Built-in themes:

| Theme | Character |
| --- | --- |
| Hermes Teal(default) | Dark teal + cream, system fonts, comfortable spacing |
| Hermes Teal (Large)(default-large) | Same as default with 18px text and roomier spacing |
| Midnight(midnight) | Deep blue-violet, Inter + JetBrains Mono |
| Ember(ember) | Warm crimson + bronze, Spectral serif + IBM Plex Mono |
| Mono(mono) | Grayscale, IBM Plex, compact |
| Cyberpunk(cyberpunk) | Neon green on black, Share Tech Mono |
| Rosé(rose) | Pink + ivory, Fraunces serif, spacious |

`default`
`default-large`
`midnight`
`ember`
`mono`
`cyberpunk`
`rose`

To build your own theme, add a plugin tab, inject into shell slots, or expose plugin-specific REST endpoints, seeExtending the Dashboard— the complete guide covers:

- Theme YAML schema — palette, typography, layout, assets, componentStyles, colorOverrides, customCSS
- Layout variants —standard,cockpit,tiled
- Plugin manifest, SDK, shell slots, page-scoped slots (inject widgets into built-in pages without overriding them), backend FastAPI routes
- A full combined theme-plus-plugin walkthrough (Strike Freedom cockpit demo)
- Discovery, reload, and troubleshooting

`standard`
`cockpit`
`tiled`