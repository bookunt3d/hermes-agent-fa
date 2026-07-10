---
layout: docs
title: "پروفایل‌ها"
permalink: /user-guide/profiles/
---

- 
- Using Hermes
- Profiles: Running Multiple Agents

# Profiles: Running Multiple Agents

Run multiple independent Hermes agents on the same machine — each with its own config, API keys, memory, sessions, skills, and gateway state.

## What are profiles?​

A profile is a separate Hermes home directory. Each profile gets its own directory containing its ownconfig.yaml,.env,SOUL.md, memories, sessions, skills, cron jobs, and state database. Profiles let you run separate agents for different purposes — a coding assistant, a personal bot, a research agent — without mixing up Hermes state.

`config.yaml`
`.env`
`SOUL.md`

When you create a profile, it automatically becomes its own command. Create a profile calledcoderand you immediately havecoder chat,coder setup,coder gateway start, etc.

`coder`
`coder chat`
`coder setup`
`coder gateway start`

## Quick start​

```
hermes profile create coder       # creates profile + "coder" command aliascoder setup                       # configure API keys and modelcoder chat                        # start chatting
```

That's it.coderis now its own Hermes profile with its own config, memory, and state.

`coder`

## Creating a profile​

Quickest setup: runhermes setup --portalinside the new profile to wire up models + tools at once. SeeNous Portal.

`hermes setup --portal`
[Nous Portal](/docs/integrations/nous-portal)

### Blank profile​

```
hermes profile create mybot
```

Creates a fresh profile with bundled skills seeded. Runmybot setupto configure API keys, model, and gateway tokens.

`mybot setup`

If you plan to use this profile as a kanban worker (or want the kanban orchestrator to route work to it), pass--description "<role>"at create time so the orchestrator knows what it's good at:

`--description "<role>"`

```
hermes profile create researcher --description "Reads source code and external docs, writes findings."
```

You can also set or auto-generate the description later withhermes profile describe— see theKanban guidefor the full routing model.

`hermes profile describe`
[Kanban guide](/docs/user-guide/features/kanban#auto-vs-manual-orchestration)

### Clone config only (--clone)​

`--clone`

```
hermes profile create work --clone
```

Copies your current profile'sconfig.yaml,.env,SOUL.md, and skills into the new profile. Same API keys, model, and capabilities, but fresh sessions and memory. Edit~/.hermes/profiles/work/.envfor different API keys, or~/.hermes/profiles/work/SOUL.mdfor a different personality.

`config.yaml`
`.env`
`SOUL.md`
`~/.hermes/profiles/work/.env`
`~/.hermes/profiles/work/SOUL.md`

### Clone everything (--clone-all)​

`--clone-all`

```
hermes profile create backup --clone-all
```

Copieseverything— config, API keys, personality, all memories, skills, cron jobs, plugins. A complete working snapshot. Per-profile history is excluded (session history,state.db,backups/,state-snapshots/,checkpoints/) — these belong to the source profile and can reach tens of GB. For a full backup including history, usehermes profile exportorhermes backupinstead.

`state.db`
`backups/`
`state-snapshots/`
`checkpoints/`
`hermes profile export`
`hermes backup`

### Clone from a specific profile​

```
hermes profile create work --clone-from coder
```

--clone-from <source>selects the source profile directly and implies a config/skills/SOUL clone. Combine it with--clone-allwhen you want a full copy of that source profile:

`--clone-from <source>`
`--clone-all`

```
hermes profile create work-backup --clone-from coder --clone-all
```

When Honcho is enabled, clone operations automatically create a dedicated AI peer for the new profile while sharing the same user workspace. Each profile builds its own observations and identity. SeeHoncho -- Multi-agent / Profilesfor details.

[Honcho -- Multi-agent / Profiles](/docs/user-guide/features/memory-providers#honcho)

## Using profiles​

### Command aliases​

Every profile automatically gets a command alias at~/.local/bin/<name>:

`~/.local/bin/<name>`

```
coder chat                    # chat with the coder agentcoder setup                   # configure coder's settingscoder gateway start           # start coder's gatewaycoder doctor                  # check coder's healthcoder skills list             # list coder's skillscoder config set model.default anthropic/claude-sonnet-4
```

The alias works with every hermes subcommand — it's justhermes -p <name>under the hood.

`hermes -p <name>`

### The-pflag​

`-p`

You can also target a profile explicitly with any command:

```
hermes -p coder chathermes --profile=coder doctorhermes chat -p coder -q "hello"    # works in any position
```

### Sticky default (hermes profile use)​

`hermes profile use`

```
hermes profile use coderhermes chat                   # now targets coderhermes tools                  # configures coder's toolshermes profile use default    # switch back
```

Sets a default so plainhermescommands target that profile. Likekubectl config use-context.

`hermes`
`kubectl config use-context`

### Knowing where you are​

The CLI always shows which profile is active:

- Prompt:coder ❯instead of❯
- Banner: ShowsProfile: coderon startup
- hermes profile: Shows current profile name, path, model, gateway status

`coder ❯`
`❯`
`Profile: coder`
`hermes profile`

## Profiles vs workspaces vs sandboxing​

Profiles are often confused with workspaces or sandboxes, but they are different things:

- Aprofilegives Hermes its own state directory:config.yaml,.env,SOUL.md, sessions, memory, logs, cron jobs, and gateway state.
- Aworkspaceorworking directoryis where terminal commands start. That is controlled separately byterminal.cwd.
- Asandboxis what limits filesystem access. Profiles donotsandbox the agent.

`config.yaml`
`.env`
`SOUL.md`
`terminal.cwd`

On the defaultlocalterminal backend, the agent still has the same filesystem access as your user account. A profile does not stop it from accessing folders outside the profile directory.

`local`

If you want a profile to start in a specific project folder, set an explicit absoluteterminal.cwdin that profile'sconfig.yaml:

`terminal.cwd`
`config.yaml`

```
terminal:  backend: local  cwd: /absolute/path/to/project
```

Usingcwd: "."on the local backend means "the directory Hermes was launched from", not "the profile directory".

`cwd: "."`

Also note:

- SOUL.mdcan guide the model, but it does not enforce a workspace boundary.
- Changes toSOUL.mdtake effect cleanly on a new session. Existing sessions may still be using the old prompt state.
- Asking the model "what directory are you in?" is not a reliable isolation test. If you need a predictable starting directory for tools, setterminal.cwdexplicitly.

`SOUL.md`
`SOUL.md`
`terminal.cwd`

## Running gateways​

Each profile runs its own gateway as a separate process with its own bot token:

```
coder gateway start           # starts coder's gatewayassistant gateway start       # starts assistant's gateway (separate process)
```

### Different bot tokens​

Each profile has its own.envfile. Configure a different Telegram/Discord/Slack bot token in each:

`.env`

```
# Edit coder's tokensnano ~/.hermes/profiles/coder/.env# Edit assistant's tokensnano ~/.hermes/profiles/assistant/.env
```

### Safety: token locks​

If two profiles accidentally use the same bot token, the second gateway will be blocked with a clear error naming the conflicting profile. Supported for Telegram, Discord, Slack, WhatsApp, and Signal.

### Persistent services​

```
coder gateway install         # creates hermes-gateway-coder systemd/launchd serviceassistant gateway install     # creates hermes-gateway-assistant service
```

Each profile gets its own service name. They run independently.

Per-profile gateways are supervised bys6-overlay(PID 1 in the container), sohermes profile create <name>automatically registers an s6 service slot at/run/service/gateway-<name>/.hermes -p <name> gateway start/stop/restartdispatches tos6-svcinstead of spawning a bare process — crashes are auto-restarted anddocker restartpreserves the previously-running set of gateways. SeePer-profile gateway supervisionfor details.

[s6-overlay](https://github.com/just-containers/s6-overlay)
`hermes profile create <name>`
`/run/service/gateway-<name>/`
`hermes -p <name> gateway start/stop/restart`
`s6-svc`
`docker restart`
[Per-profile gateway supervision](/docs/user-guide/docker#per-profile-gateway-supervision)

## Configuring profiles​

Each profile has its own:

- config.yaml— model, provider, toolsets, all settings
- .env— API keys, bot tokens
- SOUL.md— personality and instructions

`config.yaml`
`.env`
`SOUL.md`

```
coder config set model.default anthropic/claude-sonnet-4echo "You are a focused coding assistant." > ~/.hermes/profiles/coder/SOUL.md
```

If you want this profile to work in a specific project by default, also set its ownterminal.cwd:

`terminal.cwd`

```
coder config set terminal.cwd /absolute/path/to/project
```

### From the dashboard​

Theweb dashboardis a machine-level surface that can manageanyprofile's config, API
keys, skills, MCPs, and model via the profile switcher in its sidebar — no
per-profile dashboard needed.coder dashboardroutes to the machine
dashboard with thecoderprofile preselected. The dashboard's Chat tab
also follows the switcher, spawning a conversation under the selected
profile's home.

[web dashboard](/docs/user-guide/features/web-dashboard#managing-multiple-profiles)
`coder dashboard`
`coder`

Note: "Set as active" on the dashboard's Profiles page is the sticky
default forfuture CLI/gateway runs(same ashermes profile use) —
to edit a profile from the dashboard, use the switcher instead.

`hermes profile use`

## Updating​

hermes updatepulls code once (shared) and syncs new bundled skills toallprofiles automatically:

`hermes update`

```
hermes update# → Code updated (12 commits)# → Skills synced: default (up to date), coder (+2 new), assistant (+2 new)
```

User-modified skills are never overwritten.

## Managing profiles​

```
hermes profile list           # show all profiles with statushermes profile show coder     # detailed info for one profilehermes profile rename coder dev-bot   # rename (updates alias + service)hermes profile export coder   # export to coder.tar.gzhermes profile import coder.tar.gz   # import from archive
```

## Deleting a profile​

```
hermes profile delete coder
```

This stops the gateway, removes the systemd/launchd service, removes the command alias, and deletes all profile data. You'll be asked to type the profile name to confirm.

Use--yesto skip confirmation:hermes profile delete coder --yes

`--yes`
`hermes profile delete coder --yes`

You cannot delete the default profile (~/.hermes). To remove everything, usehermes uninstall.

`~/.hermes`
`hermes uninstall`

## Tab completion​

```
# Basheval "$(hermes completion bash)"# Zsheval "$(hermes completion zsh)"
```

Add the line to your~/.bashrcor~/.zshrcfor persistent completion. Completes profile names after-p, profile subcommands, and top-level commands.

`~/.bashrc`
`~/.zshrc`
`-p`

## How it works​

Profiles use theHERMES_HOMEenvironment variable. When you runcoder chat, the wrapper script setsHERMES_HOME=~/.hermes/profiles/coderbefore launching hermes. Since 119+ files in the codebase resolve paths viaget_hermes_home(), Hermes state automatically scopes to the profile's directory — config, sessions, memory, skills, state database, gateway PID, logs, and cron jobs.

`HERMES_HOME`
`coder chat`
`HERMES_HOME=~/.hermes/profiles/coder`
`get_hermes_home()`

This is separate from terminal working directory. Tool execution starts fromterminal.cwd(or the launch directory whencwd: "."on the local backend), not automatically fromHERMES_HOME.

`terminal.cwd`
`cwd: "."`
`HERMES_HOME`

On host installs, tool subprocesses keep your real OS-userHOMEby default so
existing CLI credentials under~keep working across profiles. Profile data is
isolated byHERMES_HOME, not by changingHOME. Container backends still use{HERMES_HOME}/homefor persistent tool state, and host users who need strict
per-profile tool config can opt in withterminal.home_mode: profile.

`HOME`
`~`
`HERMES_HOME`
`HOME`
`{HERMES_HOME}/home`
`terminal.home_mode: profile`

This means two things that are easy to mix up:

- HERMES_HOMEis the profile boundary. It controls Hermes config,.env,
memory, sessions, skills, logs, cron jobs, gateway state, and other Hermes
data.
- HOMEis the operating-system/user home that external CLIs expect. On host
installs, Hermes keeps it as the real user home by default so tools likegit,ssh,gh,az,npm, Claude Code, and Codex find the same
credentials they use in your normal shell.

`HERMES_HOME`
`.env`
`HOME`
`git`
`ssh`
`gh`
`az`
`npm`

The tradeoff is that host profiles share normal user-level CLI state by default.
If you need separate CLI identities per profile, setterminal.home_mode: profilein that profile'sconfig.yaml. In that mode Hermes launches tool
subprocesses withHOME={HERMES_HOME}/home; you then need to initialize or link
the profile-specific~/.ssh,~/.gitconfig,~/.config/gh, cloud CLI auth,
Claude/Codex auth, npm state, and similar files inside that profile home.

`terminal.home_mode: profile`
`config.yaml`
`HOME={HERMES_HOME}/home`
`~/.ssh`
`~/.gitconfig`
`~/.config/gh`

Hermes also exposesHERMES_REAL_HOMEto subprocesses so scripts can still find
the actual account home whenhome_mode: profileis active.

`HERMES_REAL_HOME`
`home_mode: profile`

The default profile is simply~/.hermesitself. No migration needed — existing installs work identically.

`~/.hermes`

## Sharing profiles as distributions​

A profile you built on one machine can be packaged as agit repositoryand installed with one command on another machine — your own workstation, a teammate's laptop, or a community user's environment. The shared package includes the SOUL, config, skills, cron jobs, and MCP connections. Credentials, memories, and sessions stay per-machine.

```
# Install a whole agent from a git repohermes profile install github.com/you/research-bot --alias# Update later when the author ships a new version (keeps your memories + .env)hermes profile update research-bot
```

SeeProfile Distributions: Share a Whole Agentfor the full guide — authoring, publishing, update semantics, security model, and use cases.

[Profile Distributions: Share a Whole Agent](/docs/user-guide/profile-distributions)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/profiles.md)