---
layout: docs
title: "Docker"
permalink: /user-guide/docker/
---

- 
- Using Hermes
- Docker

# Hermes Agent — Docker

There are two distinct ways Docker intersects with Hermes Agent:

1. Running Hermes IN Docker— the agent itself runs inside a container (this page's primary focus)
2. Docker as a terminal backend— the agent runs on your host but executes every command inside a single, persistent Docker sandbox container that survives across tool calls,/new, and subagents for the life of the Hermes process (seeConfiguration → Docker Backend)

`/new`
[Configuration → Docker Backend](/docs/user-guide/configuration#docker-backend)

This page covers option 1. The container stores all user data (config, API keys, sessions, skills, memories) in a single directory mounted from the host at/opt/data. The image itself is stateless and can be upgraded by pulling a new version without losing any configuration.

`/opt/data`

## Quick start​

If this is your first time running Hermes Agent, create a data directory on the host and start the container interactively to run the setup wizard:

Some VPS providers (Hetzner Cloud, and several others) offer a browser-based
console for managing hosts. These consoles transmit special characters
incorrectly —:may arrive as;,@may be mis-rendered, and non-English
keyboard layouts fare worse — which silently corruptsdocker runarguments
like-v ~/.hermes:/opt/data,-e KEY=value, and pasted API keys / tokens.

`:`
`;`
`@`
`docker run`
`-v ~/.hermes:/opt/data`
`-e KEY=value`

Connect over SSH instead(ssh root@<host>) for copy-paste-safe command
entry. If you must use the browser console, type the commands manually
instead of pasting, and double-check every:,@,=, and/in the
result before hitting Enter.

`ssh root@<host>`
`:`
`@`
`=`
`/`

```
mkdir -p ~/.hermesdocker run -it --rm \  -v ~/.hermes:/opt/data \  nousresearch/hermes-agent setup
```

This drops you into the setup wizard, which will prompt you for your API keys and write them to~/.hermes/.env. You only need to do this once. It is highly recommended to set up a chat system for the gateway to work with at this point.

`~/.hermes/.env`

Inside the container, runhermes setup --portalonce — the refresh token persists in the mounted~/.hermesvolume. SeeNous Portal.

`hermes setup --portal`
`~/.hermes`
[Nous Portal](/docs/integrations/nous-portal)

## Running in gateway mode​

Once configured, run the container in the background as a persistent gateway (Telegram, Discord, Slack, WhatsApp, etc.):

```
docker run -d \  --name hermes \  --restart unless-stopped \  -v ~/.hermes:/opt/data \  -p 8642:8642 \  nousresearch/hermes-agent gateway run
```

Port 8642 exposes the gateway'sOpenAI-compatible API serverand health endpoint. It's optional if you only use chat platforms (Telegram, Discord, etc.), but required if you want the dashboard or external tools to reach the gateway.

[OpenAI-compatible API server](/docs/user-guide/features/api-server)

Inside the official Docker image,gateway runisautomatically supervised by s6-overlay: if the gateway process crashes it's restarted within a couple of seconds without losing the container, and the dashboard (whenHERMES_DASHBOARD=1is set) is supervised alongside it. Thegateway runCMD process itself is asleep infinityheartbeat that keeps the container alive while s6 manages the actual gateway process — sodocker stopstill shuts everything down cleanly, butdocker logsshows the supervised gateway's output.

`gateway run`
`HERMES_DASHBOARD=1`
`gateway run`
`sleep infinity`
`docker stop`
`docker logs`

You'll see a one-line breadcrumb indocker logsconfirming the upgrade. To opt out — and get the historical "gateway is the container's main process, container exit = gateway exit" semantics — pass--no-superviseor setHERMES_GATEWAY_NO_SUPERVISE=1. The opt-out is useful for CI smoke tests that want the container to exit with the gateway's status code; for production deployments the supervised default is strictly better.

`docker logs`
`--no-supervise`
`HERMES_GATEWAY_NO_SUPERVISE=1`

This behavior applies to the s6-based image only. Earlier (tini-based) images still rungateway runas the foreground main process.

`gateway run`

See theWhere the logs gosection below for the full routing map (per-profile gateways, dashboard, boot reconciler, container-widedocker logs).

`docker logs`

Thetool_loop_guardrails.hard_stop_enabledsetting defaults tofalse, which is reasonable for interactive CLI and TUI sessions where a person can see repeated tool-call warnings. In unattended gateway or server deployments, warnings alone may not stop an agent that gets stuck in a repeated tool-call loop. Operators who want circuit-breaker behavior should explicitly enable hard stops in the profile'sconfig.yaml:

`tool_loop_guardrails.hard_stop_enabled`
`false`
`config.yaml`

```
tool_loop_guardrails:  hard_stop_enabled: true  hard_stop_after:    exact_failure: 5    idempotent_no_progress: 5
```

Note: the API server is gated onAPI_SERVER_ENABLED=true. To expose it beyond127.0.0.1inside the container, also setAPI_SERVER_HOST=0.0.0.0and anAPI_SERVER_KEY(minimum 8 characters — generate one withopenssl rand -hex 32). Example:

`API_SERVER_ENABLED=true`
`127.0.0.1`
`API_SERVER_HOST=0.0.0.0`
`API_SERVER_KEY`
`openssl rand -hex 32`

```
docker run -d \  --name hermes \  --restart unless-stopped \  -v ~/.hermes:/opt/data \  -p 8642:8642 \  -e API_SERVER_ENABLED=true \  -e API_SERVER_HOST=0.0.0.0 \  -e API_SERVER_KEY="$(openssl rand -hex 32)" \  -e API_SERVER_CORS_ORIGINS='*' \  nousresearch/hermes-agent gateway run
```

Opening any port on an internet facing machine is a security risk. You should not do it unless you understand the risks.

## Running the dashboard​

The built-in web dashboard runs as a supervised s6-rc service alongside the gateway in the same container. SetHERMES_DASHBOARD=1to bring it up:

`HERMES_DASHBOARD=1`

```
docker run -d \  --name hermes \  --restart unless-stopped \  -v ~/.hermes:/opt/data \  -p 8642:8642 \  -p 9119:9119 \  -e HERMES_DASHBOARD=1 \  nousresearch/hermes-agent gateway run
```

The dashboard is supervised by s6 — if it crashes,s6-superviserestarts it automatically after a short backoff. Dashboard stdout/stderr is forwarded todocker logs <container>(no prefix; the gateway's own output now lives in a per-profile s6-log file — seeWhere the logs gobelow — so the two streams don't clash).

`s6-supervise`
`docker logs <container>`

| Environment variable | Description | Default |
| --- | --- | --- |
| HERMES_DASHBOARD | Set to1(ortrue/yes) to enable the supervised dashboard service | (unset — service is registered but stays down) |
| HERMES_DASHBOARD_HOST | Bind address for the dashboard HTTP server | 0.0.0.0 |
| HERMES_DASHBOARD_PORT | Port for the dashboard HTTP server | 9119 |
| HERMES_DASHBOARD_INSECURE | Deprecated / no-op.Formerly bypassed the auth gate; as of the June 2026 hardening it no longer disables authentication. A non-loopback bind always requires an auth provider | (ignored — configure a provider instead) |

`HERMES_DASHBOARD`
`1`
`true`
`yes`
`HERMES_DASHBOARD_HOST`
`0.0.0.0`
`HERMES_DASHBOARD_PORT`
`9119`
`HERMES_DASHBOARD_INSECURE`

The dashboard inside the container defaults to binding0.0.0.0— without it, the published-p 9119:9119port would not be reachable from the host. To restrict the bind to container loopback (for sidecar / reverse-proxy setups), setHERMES_DASHBOARD_HOST=127.0.0.1.

`0.0.0.0`
`-p 9119:9119`
`HERMES_DASHBOARD_HOST=127.0.0.1`

The dashboard's auth gate engages automatically when both of the following are true:

1. The bind host is non-loopback (e.g. the default0.0.0.0inside the container),and
2. ADashboardAuthProviderplugin is registered.

`0.0.0.0`
`DashboardAuthProvider`

There are three bundled ways to satisfy the second condition:

- Username/password— the simplest for a self-hosted / on-prem / homelab container on a trusted network or behind a VPN: setHERMES_DASHBOARD_BASIC_AUTH_USERNAME+HERMES_DASHBOARD_BASIC_AUTH_PASSWORD(andHERMES_DASHBOARD_BASIC_AUTH_SECRETfor restart-stable sessions). Not suitable for direct public-internet exposure.
- OAuth (Nous Portal)— for hosted/public deploys: thedashboard_auth/nousprovider activates wheneverHERMES_DASHBOARD_OAUTH_CLIENT_IDis set.
- Self-hosted OIDC— to authenticate against your own identity provider via standard OpenID Connect: thedashboard_auth/self_hostedprovider activates whenHERMES_DASHBOARD_OIDC_ISSUER+HERMES_DASHBOARD_OIDC_CLIENT_IDare set.

`HERMES_DASHBOARD_BASIC_AUTH_USERNAME`
`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`
`HERMES_DASHBOARD_BASIC_AUTH_SECRET`
`dashboard_auth/nous`
`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`dashboard_auth/self_hosted`
`HERMES_DASHBOARD_OIDC_ISSUER`
`HERMES_DASHBOARD_OIDC_CLIENT_ID`

Whichever you choose, the gate redirects callers to a login page before they can reach any protected route. SeeWeb Dashboard → Authenticationfor all three providers.

[Web Dashboard → Authentication](/docs/user-guide/features/web-dashboard#authentication-gated-mode)

If no provider is registered and the bind is non-loopback, the dashboardfails closed at startupwith a specific error pointing at the missing env var. There is no longer an escape hatch that serves the dashboard unauthenticated on a public bind:HERMES_DASHBOARD_INSECURE=1is now a deprecated no-op (it logs a warning and is ignored). Configure a provider, or bindHERMES_DASHBOARD_HOST=127.0.0.1and reach the dashboard over an SSH tunnel / Tailscale instead.

`HERMES_DASHBOARD_INSECURE=1`
`HERMES_DASHBOARD_HOST=127.0.0.1`
`--insecure`

An unauthenticated public dashboard was the entry point for the June 2026 MCP-config persistence campaign: internet scanners reached exposed dashboards (and OpenAI API servers) and drove the agent into planting an SSH-key backdoor. The auth gate is now mandatory on every non-loopback bind. For a trusted-LAN / homelab box, the bundled username/password provider (HERMES_DASHBOARD_BASIC_AUTH_USERNAME+_PASSWORD) is the zero-infra way to satisfy it.

`HERMES_DASHBOARD_BASIC_AUTH_USERNAME`
`_PASSWORD`

Running the dashboard as a separate containerissupported when that container shares the host PID and network namespace (e.g.network_mode: host, as the repo's owndocker-compose.ymldoes — see itsdashboardservice). Its gateway-liveness detection requires a shared PID namespace with the gateway process, so the limitation only applies to dashboards run in isolated bridge-network containers without a shared PID namespace.

`network_mode: host`
`docker-compose.yml`
`dashboard`

## Running interactively (CLI chat)​

To open an interactive chat session against a running data directory:

```
docker run -it --rm \  -v ~/.hermes:/opt/data \  nousresearch/hermes-agent
```

Or if you have already opened a terminal in your running container (via Docker Desktop for instance), just run:

```
/opt/hermes/.venv/bin/hermes
```

## Persistent volumes​

The/opt/datavolume is the single source of truth for all Hermes state. It maps to your host's~/.hermes/directory and contains:

`/opt/data`
`~/.hermes/`

| Path | Contents |
| --- | --- |
| .env | API keys and secrets |
| config.yaml | All Hermes configuration |
| SOUL.md | Agent personality/identity |
| sessions/ | Conversation history |
| memories/ | Persistent memory store |
| skills/ | Installed skills |
| home/ | Per-profile HOME for Hermes tool subprocesses (git,ssh,gh,npm, and skill CLIs) |
| cron/ | Scheduled job definitions |
| hooks/ | Event hooks |
| logs/ | Runtime logs |
| skins/ | Custom CLI skins |

`.env`
`config.yaml`
`SOUL.md`
`sessions/`
`memories/`
`skills/`
`home/`
`git`
`ssh`
`gh`
`npm`
`cron/`
`hooks/`
`logs/`
`skins/`

### Immutable install tree​

In hosted and published Docker images,/opt/hermesis the installed application tree. It is root-owned and read-only to the runtimehermesuser, so agent turns, gateway sessions, dashboard actions, and normaldocker exec hermes hermes ...commands cannot edit the core source, bundled.venv,node_modules, or TUI bundle in place.

`/opt/hermes`
`hermes`
`docker exec hermes hermes ...`
`.venv`
`node_modules`

All mutable Hermes state belongs under/opt/data: config,.env, profiles, skills, memories, sessions, logs, dashboard uploads, plugins, and other user-managed files. The image also disables runtime.pycwrites and Hermes lazy dependency installs into/opt/hermes; optional platform dependencies needed by the published image should be baked into the image or installed through a new image build.

`/opt/data`
`.env`
`.pyc`
`/opt/hermes`

On hosted/published images, agent self-improvement is scoped to skills, memory, plugins, and config under/opt/data. The installed core source under/opt/hermesis immutable; core changes are made via PRs to the repo and shipped by updating the image, not by live-editing the running install.

`/opt/data`
`/opt/hermes`

If an operator needs to repair or inspect files outside/opt/data, use a root shell intentionally. Thehermesshim normally dropsdocker exec hermes hermes ...back to the runtime user; setHERMES_DOCKER_EXEC_AS_ROOT=1for a one-off root invocation when you explicitly need root semantics.

`/opt/data`
`hermes`
`docker exec hermes hermes ...`
`HERMES_DOCKER_EXEC_AS_ROOT=1`

Skill CLIs that store credentials under~must be initialized against the subprocess HOME, not just the data-volume root. For example, thexurl skillstores OAuth state in~/.xurl; in the official Docker layout, Hermes tool calls read that as/opt/data/home/.xurl, so run manual xurl auth withHOME=/opt/data/homeand verify withHOME=/opt/data/home xurl auth status.

`~`
[xurl skill](/docs/user-guide/skills/bundled/social-media/social-media-xurl)
`~/.xurl`
`/opt/data/home/.xurl`
`HOME=/opt/data/home`
`HOME=/opt/data/home xurl auth status`

Never run two Hermesgatewaycontainers against the same data directory simultaneously — session files and memory stores are not designed for concurrent write access.

## Multi-profile support​

Hermes supportsmultiple profiles— separate~/.hermes/subdirectories that let you run independent agents (different SOUL, skills, memory, sessions, credentials) from a single installation.Inside the official Docker image, the s6 supervision tree treats each profile as a first-class supervised service, so the recommended deployment isone container hosting all profiles.

[multiple profiles](/docs/reference/profile-commands)
`~/.hermes/`

Each profile created withhermes profile create <name>gets:

`hermes profile create <name>`
- A dedicated s6 service slot at/run/service/gateway-<name>/, registered dynamically by the runtime — no container rebuild required.
- Auto-restart on crash, backoff-managed bys6-supervise.
- Per-profile rotated logs at${HERMES_HOME}/logs/gateways/<name>/current(10 archives × 1 MB each).
- State persistence across container restarts: the boot-time reconciler readsgateway_state.jsonfrom each profile directory and brings the slot back up only for profiles whose last recorded state wasrunning. Only a gateway you explicitly stopped (hermes gateway stop) stays down across a restart — a container restart, image upgrade, or unexpected exit leaves the recorded state asrunning, so the gateway auto-starts on the next boot.

`/run/service/gateway-<name>/`
`s6-supervise`
`${HERMES_HOME}/logs/gateways/<name>/current`
`gateway_state.json`
`running`
`hermes gateway stop`
`running`

The lifecycle commands you'd run on the host work the same way from inside the container:

```
# Create a profile — registers the gateway-<name> s6 slot.docker exec hermes hermes profile create coder# Start / stop / restart — dispatches s6-svc; the gateway lifecycle survives docker restart.docker exec hermes hermes -p coder gateway startdocker exec hermes hermes -p coder gateway stopdocker exec hermes hermes -p coder gateway restart# Status — reports `Manager: s6 (container supervisor)` inside the container.docker exec hermes hermes -p coder gateway status# Remove a profile — tears down the s6 slot too.docker exec hermes hermes profile delete coder
```

Under the hood,hermes gateway start/stop/restartinside the container is intercepted and routed tos6-svcagainst the right service directory; you don't need to learn the s6 commands directly. For raw supervisor state, use/command/s6-svstat /run/service/gateway-<name>(note/command/is on PATH only for processes spawned by the supervision tree — when calling fromdocker exec, pass the absolute path).

`hermes gateway start/stop/restart`
`s6-svc`
`/command/s6-svstat /run/service/gateway-<name>`
`/command/`
`docker exec`

### Reaching more than one profile from outside the container​

Two different surfaces reach a profile's gateway from outside, and they behave differently — don't conflate them:

Hermes Desktop (and the web dashboard).The Desktop app'sRemote Gatewayconnection talks to ahermes dashboardbackend (defaultport 9119, enabled byHERMES_DASHBOARD=1) —notthe OpenAI API server. One dashboard backend serveseveryco-located profile: the app's profile switcher sends the target profile with each request and the backend opens that profile'sHERMES_HOMEon disk. So you donotneed a second port — or a second connection — per profile for Desktop; one:9119connection covers them all through the switcher.

`hermes dashboard`
`HERMES_DASHBOARD=1`
`HERMES_HOME`
`:9119`

OpenAI-compatible API clients (Open WebUI, LobeChat,/v1/...).These talk to each profile'sAPI server, which bindsport 8642 for every profile(resolved fromAPI_SERVER_PORT/platforms.api_server.extra.port— there is no auto-allocation and noconfig.yaml/gateway.portkey). If you want a client to reach aspecificsecond profile, give that profile a distinctAPI_SERVER_PORTinits own.env, otherwise its gateway tries to bind 8642 too and conflicts with the default profile:

`/v1/...`
`API_SERVER_PORT`
`platforms.api_server.extra.port`
`config.yaml`
`gateway.port`
`API_SERVER_PORT`
`.env`

```
# Create the profile (registers its gateway-<name> s6 slot)docker exec hermes hermes profile create work# Point its API server at a free port (write to the profile's own .env)cat >> /opt/data/profiles/work/.env <<'EOF'API_SERVER_ENABLED=trueAPI_SERVER_PORT=8643EOFdocker exec hermes hermes -p work gateway restart
```

KeepAPI_SERVER_PORTin each profile'sown.env, never in the container-wideenvironment:block — a global value would force every profile onto the same port and they would collide. With bridge networking, publish the extra port indocker-compose.yml(- "8643:8643"); withnetwork_mode: hostit is already reachable on the host. The default profile's 8642 connection is untouched.

`API_SERVER_PORT`
`.env`
`environment:`
`docker-compose.yml`
`- "8643:8643"`
`network_mode: host`

### Why one container with many profiles, not many containers​

Before the s6 migration, "one container per profile" was the recommended pattern because there was no in-container supervisor to manage multiple gateways. With s6 as PID 1, that's no longer necessary, and the single-container layout is simpler in almost every dimension:

|  | One container, many profiles | One container per profile |
| --- | --- | --- |
| Disk overhead | One image, one bundled venv, one Playwright cache | N images / N caches |
| Memory overhead | Shared Python interpreter cache, shared node_modules | Duplicated per container |
| Profile creation | docker exec ... hermes profile create <name>(seconds) | Newdocker runinvocation + port allocation + bind-mount config |
| Per-profile crash recovery | s6-superviseauto-restart | Docker's--restart unless-stopped(slower, kills sibling work) |
| Logs | Per-profile rotated file vias6-log, plus container-boot audit log | docker logs <name>per container — no built-in rotation |
| Backup | One~/.hermesdirectory | N directories to coordinate |

`docker exec ... hermes profile create <name>`
`docker run`
`s6-supervise`
`--restart unless-stopped`
`s6-log`
`docker logs <name>`
`~/.hermes`

The default profile (default) is always registered on first boot, so a fresh container ships with one supervised gateway out of the box. Additional profiles are pure runtime adds.

`default`

### When you DO want a separate container​

Profile-in-container is the default. Run a separate container per profile only when you have a specific reason:

- Resource isolation per workload— e.g. a runaway browser-tool session in profile A shouldn't be able to OOM profile B. Containers give you--memory/--cpusper profile.
- Independent image pinning— different upstream image tags per workload.
- Network segmentation— distinct Docker networks per profile (e.g. one customer-facing, one internal).
- Compliance / blast radius— distinct credentials never share an OS-level process tree.

`--memory`
`--cpus`

In those cases, declare one service per profile with distinctcontainer_name,volumes, andports:

`container_name`
`volumes`
`ports`

```
services:  hermes-work:    image: nousresearch/hermes-agent:latest    container_name: hermes-work    restart: unless-stopped    command: gateway run    ports:      - "8642:8642"    volumes:      - ~/.hermes-work:/opt/data  hermes-personal:    image: nousresearch/hermes-agent:latest    container_name: hermes-personal    restart: unless-stopped    command: gateway run    ports:      - "8643:8642"    volumes:      - ~/.hermes-personal:/opt/data
```

The warning fromPersistent volumesstill applies: never point two containers at the same~/.hermesdirectory simultaneously. The s6 supervisor inside each container manages its own profile set; cross-container sharing of a data volume corrupts session files and memory stores.

`~/.hermes`

## Where the logs go​

The s6 container has four distinct log surfaces, and "why isn't my gateway showing anything indocker logs" is a common surprise. Cheatsheet:

`docker logs`

| Source | Where it lands | How to read it |
| --- | --- | --- |
| Per-profile gateway(hermes gateway runand per-profile gateways under s6) | Tee'd to two places:docker logs <container>(real time, no extra prefix)and${HERMES_HOME}/logs/gateways/<profile>/current(rotated, ISO-8601 timestamped, 10 archives × 1 MB each) | docker logs -f hermesortail -F ~/.hermes/logs/gateways/default/currenton the host |
| Dashboard(whenHERMES_DASHBOARD=1) | docker logs <container>(no prefix) | docker logs -f hermes— interleaved with gateway lines |
| Boot reconciler(records which profile gateways were restored on each container start) | ${HERMES_HOME}/logs/container-boot.log(append-only audit log) | tail -F ~/.hermes/logs/container-boot.log |
| Generic Hermes logs(agent.log,errors.log) | ${HERMES_HOME}/logs/(profile-aware) | docker exec hermes hermes logs --follow [--level WARNING] [--session <id>] |

`hermes gateway run`
`docker logs <container>`
`${HERMES_HOME}/logs/gateways/<profile>/current`
`docker logs -f hermes`
`tail -F ~/.hermes/logs/gateways/default/current`
`HERMES_DASHBOARD=1`
`docker logs <container>`
`docker logs -f hermes`
`${HERMES_HOME}/logs/container-boot.log`
`tail -F ~/.hermes/logs/container-boot.log`
`agent.log`
`errors.log`
`${HERMES_HOME}/logs/`
`docker exec hermes hermes logs --follow [--level WARNING] [--session <id>]`

Two practical consequences worth knowing:

- The file copy atlogs/gateways/<profile>/currentis what survives container restarts.docker logsonly retains output from the current container's lifetime (and is wiped ondocker rm); the rotated files persist on the bind-mounted volume.
- The boot reconciler's audit line shape is<iso-timestamp> profile=<name> prior_state=<state> action=<registered|started>, so a quickgrep profile=coder ~/.hermes/logs/container-boot.logreveals when a given profile was last restored and whether s6 auto-started it.

`logs/gateways/<profile>/current`
`docker logs`
`docker rm`
`<iso-timestamp> profile=<name> prior_state=<state> action=<registered|started>`
`grep profile=coder ~/.hermes/logs/container-boot.log`

## Environment variable forwarding​

API keys are read from/opt/data/.envinside the container. You can also pass environment variables directly:

`/opt/data/.env`

```
docker run -it --rm \  -v ~/.hermes:/opt/data \  -e ANTHROPIC_API_KEY="sk-ant-..." \  -e OPENAI_API_KEY="sk-..." \  nousresearch/hermes-agent
```

Direct-eflags override values from.env. This is useful for CI/CD or secrets-manager integrations where you don't want keys on disk.

`-e`
`.env`

This page covers running Hermes itself inside Docker. If you want Hermes to execute the agent'sterminal/execute_codecalls inside a Docker sandbox container (one long-lived container shared across Hermes processes — see issue #20561), that's a separate config block —terminal.backend: dockerplusterminal.docker_image,terminal.docker_volumes,terminal.docker_forward_env,terminal.docker_env,terminal.docker_run_as_host_user,terminal.docker_extra_args,terminal.docker_persist_across_processes, andterminal.docker_orphan_reaper. SeeConfiguration → Docker Backendfor the full set including container-lifecycle rules.

`terminal`
`execute_code`
`terminal.backend: docker`
`terminal.docker_image`
`terminal.docker_volumes`
`terminal.docker_forward_env`
`terminal.docker_env`
`terminal.docker_run_as_host_user`
`terminal.docker_extra_args`
`terminal.docker_persist_across_processes`
`terminal.docker_orphan_reaper`
[Configuration → Docker Backend](/docs/user-guide/configuration#docker-backend)

## Docker Compose example​

For persistent deployment with both the gateway and dashboard, adocker-compose.yamlis convenient:

`docker-compose.yaml`

```
services:  hermes:    image: nousresearch/hermes-agent:latest    container_name: hermes    restart: unless-stopped    command: gateway run    ports:      - "8642:8642"   # gateway API      - "9119:9119"   # dashboard (only reached when HERMES_DASHBOARD=1)    volumes:      - ~/.hermes:/opt/data    environment:      - HERMES_DASHBOARD=1      # Uncomment to forward specific env vars instead of using .env file:      # - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}      # - OPENAI_API_KEY=${OPENAI_API_KEY}      # - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}    deploy:      resources:        limits:          memory: 4G          cpus: "2.0"
```

Start withdocker compose up -dand view logs withdocker compose logs -f. The supervised gateway's stdout is also tee'd to${HERMES_HOME}/logs/gateways/<profile>/currenton the volume — seeWhere the logs gofor the full routing map.

`docker compose up -d`
`docker compose logs -f`
`${HERMES_HOME}/logs/gateways/<profile>/current`

## Optional: Linux desktop audio bridge​

Voice mode in Docker needs two separate things to work: Hermes must be allowed to probe audio devices inside the container, and the container must be able to reach your host audio server. The setup below covers the host audio plumbing for Linux desktops that expose a PulseAudio-compatible socket, including many PipeWire setups.

This is a Linux desktop workaround, not a general Docker Desktop feature. It is useful when you already have host audio working and want CLI voice mode inside the Hermes container. If Hermes still reportsRunning inside Docker container -- no audio devices, use a build that includes Docker audio probing support forPULSE_SERVER/PIPEWIRE_REMOTE.

`Running inside Docker container -- no audio devices`
`PULSE_SERVER`
`PIPEWIRE_REMOTE`

First, create an ALSA config next to your Compose file:

```
pcm.!default {    type pulse    hint {        show on        description "Default ALSA Output (PulseAudio)"    }}pcm.pulse {    type pulse}ctl.!default {    type pulse}
```

Then build a small derived image with the ALSA PulseAudio plugin installed:

```
FROM nousresearch/hermes-agent:latestUSER rootRUN apt-get update \    && apt-get install -y --no-install-recommends libasound2-plugins \    && rm -rf /var/lib/apt/lists/*
```

Use that image in Compose and pass through the host user's PulseAudio socket and cookie:

```
services:  hermes:    build:      context: .      dockerfile: Dockerfile.audio    image: hermes-agent-audio    container_name: hermes    restart: unless-stopped    command: gateway run    volumes:      - ~/.hermes:/opt/data      - /run/user/${HERMES_UID}/pulse:/run/user/${HERMES_UID}/pulse      - ~/.config/pulse/cookie:/tmp/pulse-cookie:ro      - ./asound.conf:/etc/asound.conf:ro    environment:      - HERMES_UID=${HERMES_UID}      - HERMES_GID=${HERMES_GID}      - XDG_RUNTIME_DIR=/run/user/${HERMES_UID}      - PULSE_SERVER=unix:/run/user/${HERMES_UID}/pulse/native      - PULSE_COOKIE=/tmp/pulse-cookie
```

Start it with your host UID/GID so the container process can access the per-user audio socket:

```
export HERMES_UID="$(id -u)"export HERMES_GID="$(id -g)"docker compose up -d --build
```

To verify what PortAudio sees inside the container:

```
docker exec hermes /opt/hermes/.venv/bin/python -c "import sounddevice as sd; print(sd.query_devices())"
```

## Resource limits​

The Hermes container needs moderate resources. Recommended minimums:

| Resource | Minimum | Recommended |
| --- | --- | --- |
| Memory | 1 GB | 2–4 GB |
| CPU | 1 core | 2 cores |
| Disk (data volume) | 500 MB | 2+ GB (grows with sessions/skills) |

Browser automation (Playwright/Chromium) is the most memory-hungry feature. If you don't need browser tools, 1 GB is sufficient. With browser tools active, allocate at least 2 GB.

Set limits in Docker:

```
docker run -d \  --name hermes \  --restart unless-stopped \  --memory=4g --cpus=2 \  -v ~/.hermes:/opt/data \  nousresearch/hermes-agent gateway run
```

## What the Dockerfile does​

The official image is based ondebian:13.4and includes:

`debian:13.4`
- Python 3.13 with dependencies synced from the lockfile viauv sync --frozen --no-install-projectfor the baked extras (all,messaging, Anthropic/Bedrock/Azure identity, Hindsight, Matrix), followed by a no-dependency editable install of Hermes itself.
- Node.js 22 + npm (for browser automation, WhatsApp bridge, TUI/Desktop bundles, and workspace build tooling)
- Playwright with Chromium (npx playwright install --with-deps chromium --only-shell)
- ripgrep, ffmpeg, git, andxz-utilsas system utilities
- docker-cli— so agents running inside the container can drive the host's Docker daemon (bind-mount/var/run/docker.sockto opt in) fordocker build,docker run, container inspection, etc.
- openssh-client— enables theSSH terminal backendfrom inside the container. The SSH backend shells out to the systemsshbinary; without this, it failed silently in containerized installs.
- The WhatsApp bridge (scripts/whatsapp-bridge/)
- s6-overlayv3as PID 1 (replaces the oldertini) — supervises the dashboard and per-profile gateways with auto-restart on crash, reaps zombie subprocesses, and forwards signals.

`uv sync --frozen --no-install-project`
`all`
`messaging`
`npx playwright install --with-deps chromium --only-shell`
`xz-utils`
`docker-cli`
`/var/run/docker.sock`
`docker build`
`docker run`
`openssh-client`
[SSH terminal backend](/docs/user-guide/configuration#ssh-backend)
`ssh`
`scripts/whatsapp-bridge/`
[s6-overlay](https://github.com/just-containers/s6-overlay)
`s6-overlay`
`tini`

The image treats/opt/hermesas an immutable install tree at runtime. Optional Python extras, Node workspaces, and TUI assets that must be available inside Docker need to be baked during the image build; runtime lazy installs are disabled so supervised gateways anddocker exec hermes …commands do not try to write dependency artifacts back into the read-only source tree.

`/opt/hermes`
`docker exec hermes …`

The container'sENTRYPOINTis s6-overlay's/init. On boot it:

`ENTRYPOINT`
`/init`
1. Runs/etc/cont-init.d/01-hermes-setup(=docker/stage2-hook.sh) as root: optional UID/GID remap, fixes volume ownership, seeds.env/config.yaml/SOUL.mdon first boot, runs non-interactive config-schema migrations unlessHERMES_SKIP_CONFIG_MIGRATION=1, syncs bundled skills.
2. Runs/etc/cont-init.d/02-reconcile-profiles(=hermes_cli.container_boot): walks$HERMES_HOME/profiles/<name>/, recreates the per-profile gateway s6 service slot under/run/service/gateway-<profile>/, and auto-starts only those whose last recorded state wasrunning(seePer-profile gateway supervision).
3. Starts the staticmain-hermesanddashboards6-rc services.
4. Exec's the container's CMD as the main program (/opt/hermes/docker/main-wrapper.sh), which routes the arguments the user passed todocker run:no args →hermes(the default)first arg is an executable on PATH (e.g.sleep,bash) → exec it directlyanything else →hermes <args>(subcommand passthrough)
The container exits when this main program exits, with its exit code.

`/etc/cont-init.d/01-hermes-setup`
`docker/stage2-hook.sh`
`.env`
`config.yaml`
`SOUL.md`
`HERMES_SKIP_CONFIG_MIGRATION=1`
`/etc/cont-init.d/02-reconcile-profiles`
`hermes_cli.container_boot`
`$HERMES_HOME/profiles/<name>/`
`/run/service/gateway-<profile>/`
`running`
`main-hermes`
`dashboard`
`/opt/hermes/docker/main-wrapper.sh`
`docker run`
- no args →hermes(the default)
- first arg is an executable on PATH (e.g.sleep,bash) → exec it directly
- anything else →hermes <args>(subcommand passthrough)
The container exits when this main program exits, with its exit code.

`hermes`
`sleep`
`bash`
`hermes <args>`

The container ENTRYPOINT is now/init(s6-overlay), not/usr/bin/tini. All five documenteddocker runinvocation patterns (no args,chat -q "…",sleep infinity,bash,--tui) behave identically to the tini-based image. If you have a downstream wrapper that depended on tini-specific signal behavior or hard-coded/usr/bin/tini --invocation, pin to the previous image tag.

`/init`
`/usr/bin/tini`
`docker run`
`chat -q "…"`
`sleep infinity`
`bash`
`--tui`
`/usr/bin/tini --`

Do not override the image entrypoint unless you keep/init(or, equivalently, the legacydocker/entrypoint.shshim that forwards to the stage2 hook) in the command chain. s6-overlay's/initruns as root so it can chown the volume on first boot, then drops to thehermesuser vias6-setuidgidfor every supervised service AND for the main program. Startinghermes gateway runas root inside the official image is refused by default because it can leave root-owned files in/opt/dataand break later dashboard or gateway starts. SetHERMES_ALLOW_ROOT_GATEWAY=1only when you intentionally accept that risk.

`/init`
`docker/entrypoint.sh`
`/init`
`hermes`
`s6-setuidgid`
`hermes gateway run`
`/opt/data`
`HERMES_ALLOW_ROOT_GATEWAY=1`

### docker execautomatically drops to thehermesuser​

`docker exec`
`hermes`

docker exec hermes <cmd>defaults to running as root inside the container, but the image ships a thin shim at/opt/hermes/bin/hermes(earliest on PATH) that detects root callers and transparently re-execs throughs6-setuidgid hermes. Sodocker exec hermes login,docker exec hermes profile create …,docker exec hermes setup, etc. all write files owned by UID 10000 — i.e. readable by the supervised gateway — with no extra--userflag needed. Non-root callers (the supervised processes themselves,docker exec --user hermes, kanban subagents inside the container) hit a short-circuit that exec's the venv binary directly, so there's no overhead on the hot paths.

`docker exec hermes <cmd>`
`/opt/hermes/bin/hermes`
`s6-setuidgid hermes`
`docker exec hermes login`
`docker exec hermes profile create …`
`docker exec hermes setup`
`--user`
`docker exec --user hermes`

If you specifically need adocker execthat retains root semantics (diagnostic sessions, inspecting root-only state, files outside/opt/datathat root happens to own), opt out per invocation:

`docker exec`
`/opt/data`

```
docker exec -e HERMES_DOCKER_EXEC_AS_ROOT=1 hermes <cmd>
```

The shim accepts1/true/yes(case-insensitive). Anything else — including typos like=0— falls through to the drop, so silent opt-outs aren't possible. Ifs6-setuidgidisn't available (custom builds that stripped s6-overlay), the shim refuses to run as root and exits 126 instead, surfacing the broken privilege model loudly rather than regressing to the historical footgun wheredocker exec hermes loginwould writeauth.jsonasroot:rootand break the supervised gateway's auth on every chat platform message.

`1`
`true`
`yes`
`=0`
`s6-setuidgid`
`docker exec hermes login`
`auth.json`
`root:root`

### Per-profile gateway supervision​

Each profile created withhermes profile create <name>automatically gets an s6-supervised gateway service registered at/run/service/gateway-<name>/, with state-persistent auto-restart across container restarts. SeeMulti-profile supportabove for the user-facing workflow and the lifecycle commands.

`hermes profile create <name>`
`/run/service/gateway-<name>/`

Supervision benefits over the pre-s6 image:

- Gateway crashes are auto-restarted bys6-superviseafter a ~1s backoff.
- Dashboard, when enabled withHERMES_DASHBOARD=1, is supervised on the same supervision tree and gets the same auto-restart treatment.
- docker restart, image upgrades (docker compose up -d --force-recreate), and unexpected exits preserve running gateways: the cont-init reconciler reads$HERMES_HOME/profiles/<name>/gateway_state.jsonand brings the slot back up if the last recorded state wasrunning. Only an explicithermes gateway stoprecordsstoppedand keeps the gateway down across the restart; the container/s6 SIGTERM sent on a restart or upgrade is treated as "still running" and auto-starts.
- Per-profile gateway logs persist under$HERMES_HOME/logs/gateways/<profile>/current(rotated bys6-log), and the reconciler's actions are appended to$HERMES_HOME/logs/container-boot.logper boot. SeeWhere the logs gofor the full routing map.

`s6-supervise`
`HERMES_DASHBOARD=1`
`docker restart`
`docker compose up -d --force-recreate`
`$HERMES_HOME/profiles/<name>/gateway_state.json`
`running`
`hermes gateway stop`
`stopped`
`$HERMES_HOME/logs/gateways/<profile>/current`
`s6-log`
`$HERMES_HOME/logs/container-boot.log`

hermes statusinside the container reportsManager: s6 (container supervisor). Use/command/s6-svstat /run/service/gateway-<name>for the raw supervisor view (note/command/is on PATH for supervision-tree processes only; pass the absolute path when calling fromdocker exec).

`hermes status`
`Manager: s6 (container supervisor)`
`/command/s6-svstat /run/service/gateway-<name>`
`/command/`
`docker exec`

## Upgrading​

Pull the latest image and recreate the container. Your data directory is
preserved, and the container runs non-interactive config-schema migrations
against the mounted$HERMES_HOME/config.yamlbefore starting the gateway.
When a migration is needed, Hermes writes timestamped backups next toconfig.yamland.envfirst.

`$HERMES_HOME/config.yaml`
`config.yaml`
`.env`

```
docker pull nousresearch/hermes-agent:latestdocker rm -f hermesdocker run -d \  --name hermes \  --restart unless-stopped \  -v ~/.hermes:/opt/data \  nousresearch/hermes-agent gateway run
```

Or with Docker Compose:

```
docker compose pulldocker compose up -d
```

SetHERMES_SKIP_CONFIG_MIGRATION=1only if you need to inspect or migrate the
persisted config manually before letting the new image rewrite it.

`HERMES_SKIP_CONFIG_MIGRATION=1`

## Skills and credential files​

When using Docker as the execution environment (not the methods above, but when the agent runs commands inside a Docker sandbox — seeConfiguration → Docker Backend), Hermes reuses a single long-lived container for all tool calls and automatically bind-mounts the skills directory (~/.hermes/skills/) and any credential files declared by skills into that container as read-only volumes. Skill scripts, templates, and references are available inside the sandbox without manual configuration, and because the container persists for the life of the Hermes process, any dependencies you install or files you write stay around for the next tool call.

[Configuration → Docker Backend](/docs/user-guide/configuration#docker-backend)
`~/.hermes/skills/`

The same syncing happens for SSH and Modal backends — skills and credential files are uploaded via rsync or the Modal mount API before each command.

## Installing more tools in the container​

The official image ships with a curated set of utilities (seeWhat the Dockerfile does), but not every tool an agent might want is preinstalled. There are five recommended approaches, in increasing order of effort and durability.

### npm or Python tools — usenpxoruvx​

`npx`
`uvx`

For any tool published to npm or PyPI, instruct Hermes to run it vianpx(npm) oruvx(Python) and to remember that command in its persistent memory. If the tool needs a config file or credentials, instruct it to drop those under/opt/data(e.g./opt/data/<tool>/config.yaml).

`npx`
`uvx`
`/opt/data`
`/opt/data/<tool>/config.yaml`

Dependencies are fetched on demand and cached for the life of the container. Configuration written under/opt/datasurvives container restarts because it lives on the bind-mounted host directory. The package cache itself is rebuilt after adocker rm, butnpxanduvxre-fetch transparently the next time the tool runs.

`/opt/data`
`docker rm`
`npx`
`uvx`

### Other tools (apt packages, binaries) — install and remember​

For anything outside npm or PyPI —aptpackages, prebuilt binaries, language runtimes not already in the image — instruct Hermes how to install it (e.g.apt-get update && apt-get install -y <package>) and tell it to remember the install command. The tool persists for the rest of the container's lifetime, and Hermes will re-run the install command after a container restart when it next needs the tool.

`apt`
`apt-get update && apt-get install -y <package>`

This is a good fit for tools that are quick to install and used occasionally. For tools used constantly, prefer the next approach.

### Durable installs — build a derived image​

When a tool must be available immediately on every container start with no re-install delay, build a new image that inherits fromnousresearch/hermes-agentand installs the tool in a layer:

`nousresearch/hermes-agent`

```
FROM nousresearch/hermes-agent:latestUSER rootRUN apt-get update \    && apt-get install -y --no-install-recommends <your-package> \    && rm -rf /var/lib/apt/lists/*USER hermes
```

Build it and use it in place of the official image:

```
docker build -t my-hermes:latest .docker run -d \  --name hermes \  --restart unless-stopped \  -v ~/.hermes:/opt/data \  -p 8642:8642 \  my-hermes:latest gateway run
```

The entrypoint script and/opt/datasemantics are inherited unchanged, so the rest of this page still applies. Remember to rebuild the image when pulling a newer upstreamnousresearch/hermes-agent.

`/opt/data`
`nousresearch/hermes-agent`

### Complex tools or multi-service stacks — run a sidecar container​

For tools that bring their own service (a database, a web server, a queue, a headless browser farm) or that are too heavy to live inside the Hermes container, run them as a separate container on a shared Docker network. Hermes reaches the sidecar by container name, the same way it reaches a local inference server (seeConnecting to local inference servers).

```
services:  hermes:    image: nousresearch/hermes-agent:latest    container_name: hermes    restart: unless-stopped    command: gateway run    ports:      - "8642:8642"    volumes:      - ~/.hermes:/opt/data    networks:      - hermes-net  my-tool:    image: example/my-tool:latest    container_name: my-tool    restart: unless-stopped    networks:      - hermes-netnetworks:  hermes-net:    driver: bridge
```

From inside the Hermes container, the sidecar is reachable athttp://my-tool:<port>(or whatever protocol it serves). This pattern keeps each service's lifecycle, resource limits, and upgrade cadence independent, and avoids bloating the Hermes image with dependencies that are only needed by one tool.

`http://my-tool:<port>`

### Broadly useful tools — open an issue or pull request​

If a tool is likely to be useful to most Hermes Agent users, consider contributing it upstream rather than carrying it in a private derived image. Open an issue or pull request on thehermes-agent repositorydescribing the tool and its use case. Tools that get bundled into the official image benefit every user and avoid the maintenance overhead of a downstream fork.

[hermes-agent repository](https://github.com/NousResearch/hermes-agent)

## Connecting to local inference servers (vLLM, Ollama, etc.)​

When running Hermes in Docker and your inference server (vLLM, Ollama, text-generation-inference, etc.) is also running on the host or in another container, networking requires extra attention.

### Docker Compose (recommended)​

Put both services on the same Docker network. This is the most reliable approach:

```
services:  vllm:    image: vllm/vllm-openai:latest    container_name: vllm    command: >      --model Qwen/Qwen2.5-7B-Instruct      --served-model-name my-model      --host 0.0.0.0      --port 8000    ports:      - "8000:8000"    networks:      - hermes-net    deploy:      resources:        reservations:          devices:            - capabilities: [gpu]  hermes:    image: nousresearch/hermes-agent:latest    container_name: hermes    restart: unless-stopped    command: gateway run    ports:      - "8642:8642"    volumes:      - ~/.hermes:/opt/data    networks:      - hermes-netnetworks:  hermes-net:    driver: bridge
```

Then in your~/.hermes/config.yaml, use thecontainer nameas the hostname:

`~/.hermes/config.yaml`

```
model:  provider: custom  model: my-model  base_url: http://vllm:8000/v1  api_key: "none"
```

- Use thecontainer name(vllm) as the hostname — notlocalhostor127.0.0.1, which refer to the Hermes container itself.
- Themodelvalue must match the--served-model-nameyou passed to vLLM.
- Setapi_keyto any non-empty string (vLLM requires the header but doesn't validate it by default).
- Donotinclude a trailing slash inbase_url.

`vllm`
`localhost`
`127.0.0.1`
`model`
`--served-model-name`
`api_key`
`base_url`

### Standalone Docker run (no Compose)​

If your inference server runs directly on the host (not in Docker), usehost.docker.internalon macOS/Windows, or--network hoston Linux:

`host.docker.internal`
`--network host`

macOS / Windows:

```
docker run -d \  --name hermes \  -v ~/.hermes:/opt/data \  -p 8642:8642 \  nousresearch/hermes-agent gateway run
```

```
# config.yamlmodel:  provider: custom  model: my-model  base_url: http://host.docker.internal:8000/v1  api_key: "none"
```

Linux (host networking):

```
docker run -d \  --name hermes \  --network host \  -v ~/.hermes:/opt/data \  nousresearch/hermes-agent gateway run
```

```
# config.yamlmodel:  provider: custom  model: my-model  base_url: http://127.0.0.1:8000/v1  api_key: "none"
```

`--network host`
`-p`

### Verifying connectivity​

From inside the Hermes container, confirm the inference server is reachable:

```
docker exec hermes curl -s http://vllm:8000/v1/models
```

You should see a JSON response listing your served model. If this fails, check:

1. Both containers are on the same Docker network (docker network inspect hermes-net)
2. The inference server is listening on0.0.0.0, not127.0.0.1
3. The port number matches

`docker network inspect hermes-net`
`0.0.0.0`
`127.0.0.1`

### Ollama​

Ollama works the same way. If Ollama runs on the host, usehost.docker.internal:11434(macOS/Windows) or127.0.0.1:11434(Linux with--network host). If Ollama runs in its own container on the same Docker network:

`host.docker.internal:11434`
`127.0.0.1:11434`
`--network host`

```
model:  provider: custom  model: llama3  base_url: http://ollama:11434/v1  api_key: "none"
```

## Troubleshooting​

### Container exits immediately​

Check logs:docker logs hermes. Common causes:

`docker logs hermes`
- Missing or invalid.envfile — run interactively first to complete setup
- Port conflicts if running with exposed ports

`.env`

### "Permission denied" errors​

The container's stage2 hook drops privileges to the non-roothermesuser (UID 10000) vias6-setuidgidinside each supervised service. If your host~/.hermes/is owned by a different UID, setHERMES_UID/HERMES_GID— or theirPUID/PGIDaliases, for parity with LinuxServer.io and NAS images — to match your host user, or ensure the data directory is writable:

`hermes`
`s6-setuidgid`
`~/.hermes/`
`HERMES_UID`
`HERMES_GID`
`PUID`
`PGID`

```
chmod -R 755 ~/.hermes
```

On a NAS (UGOS, Synology, unRAID) the data directory is typically abind mountowned by a host UID the container cannotchown. SetPUID/PGID(orHERMES_UID/HERMES_GID) to that host user so the runtime runs as the owner of the mount rather than UID 10000:

`chown`
`PUID`
`PGID`
`HERMES_UID`
`HERMES_GID`

```
docker run -d \  --name hermes \  -e PUID=1000 -e PGID=10 \  -v /volume1/docker/hermes:/opt/data \  nousresearch/hermes-agent gateway run
```

docker exec hermes <cmd>automatically drops to UID 10000 too — seedocker execautomatically drops to thehermesuserfor details and the per-invocation opt-out.

`docker exec hermes <cmd>`
`docker exec`
`hermes`

### Browser tools not working​

Playwright needs shared memory. Add--shm-size=1gto your Docker run command:

`--shm-size=1g`

```
docker run -d \  --name hermes \  --shm-size=1g \  -v ~/.hermes:/opt/data \  nousresearch/hermes-agent gateway run
```

### Gateway not reconnecting after network issues​

The--restart unless-stoppedflag handles most transient failures. If the gateway is stuck, restart the container:

`--restart unless-stopped`

```
docker restart hermes
```

### Checking container health​

```
docker logs --tail 50 hermes          # Recent logsdocker run -it --rm nousresearch/hermes-agent:latest version     # Verify versiondocker stats hermes                    # Resource usage
```

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/docker.md)