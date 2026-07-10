---
layout: docs
title: "گیت‌وی‌های چند پروفایلی"
permalink: /user-guide/multi-profile-gateways/
---

- 
- Using Hermes
- Running Many Gateways at Once

# Running Many Gateways at Once

Operate multipleprofiles— each with its own bot tokens,
sessions, and memory — as managed services on a single machine. This page
covers the operational concerns: starting them all together, viewing logs
across profiles, preventing the host from sleeping, and recovering from common
launchd/systemd quirks.

[profiles](/docs/user-guide/profiles)

If you only run one Hermes agent, you don't need this page — seeProfilesfor the basics.

[Profiles](/docs/user-guide/profiles)

## When to use this​

You want this setup when you have two or more Hermes agents that should all
be online at the same time. Common reasons:

- A personal assistant on one Telegram bot and a coding agent on another
- One agent per family member or one per Slack workspace
- Sandbox + production instances of the same configuration
- A research agent + a writing agent + a cron-driven bot — each with isolated
memory and skills

Every profile already gets its own per-platform LaunchAgent
(ai.hermes.gateway-<name>.plist) or systemd user service
(hermes-gateway-<name>.service). This guide adds the patterns for managing
them collectively.

`ai.hermes.gateway-<name>.plist`
`hermes-gateway-<name>.service`

## Quick start​

```
# Create profiles (once)hermes profile create coderhermes profile create personal-bothermes profile create research# Configure eachcoder setuppersonal-bot setupresearch setup# Install each gateway as a managed servicecoder gateway installpersonal-bot gateway installresearch gateway install# Start them allcoder gateway startpersonal-bot gateway startresearch gateway start
```

That's it — three independent agents, each on its own process, restarting
automatically on crash and on user login.

## Alternative: one gateway for all profiles (multiplexing)​

The model above runsone process per profile. That is the default and is
the right choice for most setups. But on a host with many profiles — or a
container deployment where one process per profile is operationally heavy — you
can instead run asingle multiplexing gateway: the default profile's gateway
becomes the sole inbound process and serves messages foreveryprofile on the
box.

This isopt-inandoff by default. When it's off, nothing on this page
changes — every behavior below is inert.

### When to prefer multiplexing​

- A container/VPS deployment where N supervisor units, N ports, and N PID files
are a burden.
- Many low-traffic profiles that don't each justify a full process.
- You want a single thing to start, monitor, and restart.

Stick with one-process-per-profile when you want hard process-level isolation
between profiles (separate memory footprints, independent crash domains, the
ability to restart one profile without touching the others).

### How to opt in​

Set the flag on thedefault profile(it owns the multiplexer) and restart
its gateway:

```
hermes config set gateway.multiplex_profiles truehermes gateway restart
```

Equivalently, in the default profile's~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
gateway:  multiplex_profiles: true
```

(The flag is also accepted as a top-levelmultiplex_profiles: truefor
convenience.) On the next start the default gateway enumerates every profile,
brings up each profile's enabled platforms under that profile's own
credentials, and routes each inbound message to the profile it belongs to. Each
turn resolves the routed profile's config, skills, memory, SOUL,and provider
keys— credentials are never shared across profiles.

`multiplex_profiles: true`

You donotrunhermes gateway startfor the secondary profiles — the
default gateway serves them. See the contract changes below.

`hermes gateway start`

### What changes when multiplexing is on​

Enabling the flag changes how a few things behave. All of these revert the
moment the flag is off.

#### 1. Secondary profiles must not start their own gateway​

With a multiplexer running, a named-profilehermes gateway start/runis ahard error, pointing you back at the multiplexer:

`hermes gateway start`
`run`

```
The default gateway is running as a profile multiplexer and already servesprofile 'coder'. ...
```

The multiplexer is the single inbound process; a second profile gateway would
double-bind that profile's platforms. Pass--forceonly if you deliberately
want a separate process for that profile (not recommended while the multiplexer
is running). The cross-profile lifecycle wrapper script earlier on this page is
thereforenotused in multiplex mode — you only manage the default gateway.

`--force`

#### 2. HTTP-inbound platforms are reached via a/p/<profile>/URL prefix​

`/p/<profile>/`

Webhook (and other HTTP-inbound) traffic for a secondary profile arrives on the
default listener under a profile prefix,nota second port:

```
# default profilePOST http://host:8644/webhooks/<route># the "coder" profile, same listenerPOST http://host:8644/p/coder/webhooks/<route>
```

An unknown or unconfigured profile in the prefix returns404. Because the one
shared listener already serves every profile this way, asecondary profile
must not enable a port-binding platform itself— doing so is a config error
and the gateway refuses to start, naming the profile and platform:

`404`

```
Profile 'coder' enables the port-binding platform 'webhook', butgateway.multiplex_profiles is on. ... Remove platforms.webhook from profile'coder's config.yaml (configure it only on the default profile).
```

Port-binding platforms covered by this rule:webhook,api_server,msgraph_webhook,feishu,wecom_callback,bluebubbles,sms. Configure
any of theseonly on the default profile; every profile is reachable through
its/p/<profile>/prefix.

`webhook`
`api_server`
`msgraph_webhook`
`feishu`
`wecom_callback`
`bluebubbles`
`sms`
`/p/<profile>/`

#### 3. Per-credential platforms still need their own token per profile​

Polling/connection platforms (Telegram, Discord, Slack, Matrix, Signal, …) work
fine multiplexed, but each profile that enables one must supply itsownbot
token — the same token cannot be polled by two profiles at once. If two profiles
configure the same(platform, token), startup fails fast naming both profiles
(seeToken-conflict safety— the rule is unchanged,
it's just enforced inside the one process now).

`(platform, token)`

#### 4. Session keys are namespaced by profile​

Each profile's sessions live under anagent:<profile>:…namespace so two
profiles on the same platform/chat never collide in the shared session store.
Thedefaultprofile keeps the historicalagent:main:…namespace
byte-for-byte, so existing default-profile sessions are unaffected — no
migration, no orphaned history.

`agent:<profile>:…`
`agent:main:…`

#### 5. One PID/lock and one status surface​

There is a single process-level PID and lock (the multiplexer, under the default
home).hermes statusreports the multiplexer and the profiles it serves;hermes status -p <name>slices to one profile. Each profile still writes its
ownruntime_status.jsonunder its own home, so existing per-profile readers
keep working.

`hermes status`
`hermes status -p <name>`
`runtime_status.json`

#### What doesnotchange​

Per-profile.envcredential isolation is preserved and, if anything,
stricter: a profile's keys are resolved from its own scope and are never unioned
into a shared environment (this also means subprocesses like MCP servers and
Kanban workers only ever see their own profile's secrets). Kanban,
profile-scoped skills/memory/SOUL, and model routing all behave per-profile
exactly as they do with separate gateways.

`.env`

## Start, stop, or restart all gateways at once​

The CLI ships with single-profile lifecycle commands. To act across every
profile, wrap them in a shell loop. Put the snippet below in~/.local/bin/hermes-gatewaysandchmod +xit:

`~/.local/bin/hermes-gateways`
`chmod +x`

```
#!/bin/shset -eu# Add or remove profile names here as you create / delete profiles.profiles="default coder personal-bot research"usage() {  echo "Usage: hermes-gateways {start|stop|restart|status|list}"}run_for_profile() {  profile="$1"  action="$2"  if [ "$profile" = "default" ]; then    hermes gateway "$action"  else    hermes -p "$profile" gateway "$action"  fi}action="${1:-}"case "$action" in  start|stop|restart|status)    for profile in $profiles; do      echo "==> $action $profile"      run_for_profile "$profile" "$action"    done    ;;  list)    hermes gateway list    ;;  *)    usage    exit 2    ;;esac
```

Then:

```
hermes-gateways start      # start every configured profilehermes-gateways stop       # stop every configured profilehermes-gateways restart    # restart allhermes-gateways status     # status across allhermes-gateways list       # delegates to `hermes gateway list`
```

Thedefaultprofile is targeted withhermes gateway <action>(no-p),
nothermes -p default gateway <action>. The wrapper above handles both forms.

`default`
`hermes gateway <action>`
`-p`
`hermes -p default gateway <action>`

## Manage one profile​

The shortcut commands every profile installs:

```
coder gateway run        # foreground (Ctrl-C to stop)coder gateway start      # start the managed servicecoder gateway stop       # stop the managed servicecoder gateway restart    # restartcoder gateway status     # statuscoder gateway install    # create the LaunchAgent / systemd unitcoder gateway uninstall  # remove the service file
```

These are equivalent tohermes -p coder gateway <action>— useful if a
profile alias is not onPATHor if you target profiles dynamically from a
script.

`hermes -p coder gateway <action>`
`PATH`

## Service files​

Each profile installs its own service with a unique name, so installations
never clash:

| Platform | Path |
| --- | --- |
| macOS | ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist |
| Linux | ~/.config/systemd/user/hermes-gateway-<profile>.service |

`~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist`
`~/.config/systemd/user/hermes-gateway-<profile>.service`

The default profile keeps the historical names:ai.hermes.gateway.plist/hermes-gateway.service.

`ai.hermes.gateway.plist`
`hermes-gateway.service`

## Viewing logs​

Each profile writes to its own log files:

```
# Default profiletail -f ~/.hermes/logs/gateway.logtail -f ~/.hermes/logs/gateway.error.log# Named profiletail -f ~/.hermes/profiles/<name>/logs/gateway.logtail -f ~/.hermes/profiles/<name>/logs/gateway.error.log
```

Stream every profile's log simultaneously:

```
tail -f ~/.hermes/logs/gateway.log ~/.hermes/profiles/*/logs/gateway.log
```

The CLI also has a structured log viewer:

```
hermes logs -f                  # follow default profilehermes -p coder logs -f         # follow one profilehermes logs --help              # filters, levels, JSON output
```

## Identify what's actually running​

```
hermes profile list             # profiles + model + gateway statehermes-gateways status          # full status across every profilelaunchctl list | grep hermes    # macOS — PIDs and labelssystemctl --user list-units 'hermes-gateway-*'   # Linux — units
```

## Editing configuration​

Every profile keeps its config inside its own directory:

```
~/.hermes/profiles/<name>/├── .env              # API keys, bot tokens (chmod 600)├── config.yaml       # model, provider, toolsets, gateway settings└── SOUL.md           # personality / system prompt
```

The default profile uses~/.hermes/directly with the same three files.

`~/.hermes/`

Edit them with any editor or via the CLI:

```
hermes config set model.model anthropic/claude-sonnet-4    # default profilecoder config set model.model openai/gpt-5                  # named profile
```

After editing.envorconfig.yaml, restart the affected gateway:

`.env`
`config.yaml`

```
coder gateway restart# or, for everything:hermes-gateways restart
```

## Keeping the host awake​

The gateway process can run all day, but the operating system will still try
to sleep when idle. Two patterns:

### macOS —caffeinate​

`caffeinate`

caffeinateis built into macOS and prevents sleep while it runs. No install.

`caffeinate`

```
caffeinate -dis                    # block display, idle, and system sleepcaffeinate -dis -t 28800           # same, auto-exit after 8 hourscaffeinate -i -w $(cat ~/.hermes/gateway.pid) &   # awake while default gateway runs# Persistent: run in background and forgetnohup caffeinate -dis >/dev/null 2>&1 &disown# Inspect / stoppmset -g assertions | grep -iE 'caffeinate|prevent|user is active'pkill caffeinate
```

| Flag | Effect |
| --- | --- |
| -d | block display sleep |
| -i | block idle system sleep (default) |
| -m | block disk sleep |
| -s | block system sleep (AC-powered Macs only) |
| -u | simulate user activity (prevents screen lock) |
| -t N | auto-exit afterNseconds |
| -w P | exit when PIDPexits |

`-d`
`-i`
`-m`
`-s`
`-u`
`-t N`
`N`
`-w P`
`P`

caffeinatecannot override the hardware-driven lid-close sleep on MacBooks.
For lid-closed operation, change your Energy Saver / Battery preferences or
use a third-party tool.

`caffeinate`

### Linux —systemd-inhibitorloginctl​

`systemd-inhibit`
`loginctl`

```
# Inhibit suspend while a command runssystemd-inhibit --what=idle:sleep --who=hermes --why="gateways running" \  sleep infinity &# Allow user services to keep running after logout (recommended)sudo loginctl enable-linger "$USER"
```

After enabling lingering, your systemd user units (includinghermes-gateway-<profile>.service) continue running across SSH disconnects
and reboots.

`hermes-gateway-<profile>.service`

## Token-conflict safety​

Each profile must use unique bot tokens for each platform. If two profiles
share a Telegram, Discord, Slack, WhatsApp, or Signal token, the second
gateway refuses to start with an error naming the conflicting profile.

To audit:

```
grep -H 'TELEGRAM_BOT_TOKEN\|DISCORD_BOT_TOKEN' \     ~/.hermes/.env ~/.hermes/profiles/*/.env
```

## Updating the code​

hermes updatepulls the latest code once and syncs new bundled skills into
every profile:

`hermes update`

```
hermes updatehermes-gateways restart
```

User-modified skills are never overwritten.

## Troubleshooting​

### "Could not find service in domain for user gui: 501"​

You ranhermes gateway startafter a previoushermes gateway stop. The
CLI'sstopdoes a fulllaunchctl unload, which removes the service from
launchd's registry. The CLI catches this specific error onstartand
automatically re-loads the plist (↻ launchd job was unloaded; reloading service definition). The service starts normally. Nothing to fix.

`hermes gateway start`
`hermes gateway stop`
`stop`
`launchctl unload`
`start`
`↻ launchd job was unloaded; reloading service definition`

### Stale PID after a crash​

If a profile's gateway showsnot runningbut a process is still alive:

`not running`

```
ps -ef | grep "hermes_cli.*-p <profile>"cat ~/.hermes/profiles/<profile>/gateway.pidkill -TERM <pid>          # gracefulkill -KILL <pid>          # if that fails after a few seconds<profile> gateway start
```

### Forcing a hard reset of one service​

```
# macOSlaunchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plistlaunchctl load   ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist# Linuxsystemctl --user restart hermes-gateway-<profile>.service
```

### Health check​

```
hermes doctor                  # default profilehermes -p <profile> doctor     # one profile
```

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/multi-profile-gateways.md)