---
layout: docs
title: "دستورات CLI"
permalink: /reference/cli-commands/
---

- 
- Reference
- Command Reference
- CLI Commands Reference

# CLI Commands Reference

This page covers theterminal commandsyou run from your shell.

For in-chat slash commands, seeSlash Commands Reference.

[Slash Commands Reference](/docs/reference/slash-commands)

## Global entrypoint​

```
hermes [global-options] <command> [subcommand/options]
```

### Global options​

| Option | Description |
| --- | --- |
| --version,-V | Show version and exit. |
| --profile <name>,-p <name> | Select which Hermes profile to use for this invocation. Overrides the sticky default set byhermes profile use. |
| --resume <session>,-r <session> | Resume a previous session by ID or title. |
| --continue [name],-c [name] | Resume the most recent session, or the most recent session matching a title. |
| --worktree,-w | Start in an isolated git worktree for parallel-agent workflows. |
| --yolo | Bypass dangerous-command approval prompts. |
| --pass-session-id | Include the session ID in the agent's system prompt. |
| --ignore-user-config | Ignore~/.hermes/config.yamland fall back to built-in defaults. Credentials in.envare still loaded. |
| --ignore-rules | Skip auto-injection ofAGENTS.md,SOUL.md,.cursorrules, memory, and preloaded skills. |
| --tui | Launch theTUIinstead of the classic CLI. Equivalent toHERMES_TUI=1. Always wins overdisplay.interface. |
| --cli | Force the classic prompt_toolkit REPL. Use this to overridedisplay.interface: tuifor a single invocation. |
| --dev | With--tui: run the TypeScript sources directly viatsxinstead of the prebuilt bundle (for TUI contributors). |

`--version`
`-V`
`--profile <name>`
`-p <name>`
`hermes profile use`
`--resume <session>`
`-r <session>`
`--continue [name]`
`-c [name]`
`--worktree`
`-w`
`--yolo`
`--pass-session-id`
`--ignore-user-config`
`~/.hermes/config.yaml`
`.env`
`--ignore-rules`
`AGENTS.md`
`SOUL.md`
`.cursorrules`
`--tui`
[TUI](/docs/user-guide/tui)
`HERMES_TUI=1`
`display.interface`
`--cli`
`display.interface: tui`
`--dev`
`--tui`
`tsx`

## Top-level commands​

| Command | Purpose |
| --- | --- |
| hermes chat | Interactive or one-shot chat with the agent. |
| hermes model | Interactively choose the default provider and model. |
| hermes moa | Configure named Mixture of Agents presets selectable from the model picker. |
| hermes fallback | Manage fallback providers tried when the primary model errors. |
| hermes gateway | Run or manage the messaging gateway service. |
| hermes proxy | Local OpenAI-compatible proxy that attaches OAuth provider credentials. SeeSubscription Proxy. |
| hermes lsp | Manage Language Server Protocol integration (semantic diagnostics for write_file/patch). |
| hermes setup | Interactive setup wizard for all or part of the configuration. |
| hermes whatsapp | Configure and pair the WhatsApp bridge. |
| hermes whatsapp-cloud | Configure the official Meta WhatsApp Business Cloud API adapter (Business account + public webhook required). Distinct fromhermes whatsapp(Baileys personal-account bridge). |
| hermes slack | Slack helpers (currently: generate the app manifest with every command as a native slash). |
| hermes auth | Manage credentials — add, list, remove, reset, status, logout. Handles OAuth flows for Codex/Nous/Anthropic. |
| hermes login/logout | Deprecated— usehermes authinstead. |
| hermes send | Send a one-shot message to a configured messaging platform (Telegram, Discord, Slack, Signal, SMS, …). Useful from shell scripts, cron jobs, CI hooks, and monitoring daemons — no agent loop, no LLM. |
| hermes secrets | Manage external secret sources (currently Bitwarden Secrets Manager) for pulling API keys at process startup instead of from~/.hermes/.env. |
| hermes migrate | Diagnose and (optionally) rewriteconfig.yamlto replace references to retired models or deprecated settings (e.g.migrate xai). |
| hermes status | Show agent, auth, and platform status. |
| hermes cron | Inspect and tick the cron scheduler. |
| hermes kanban | Multi-profile collaboration board (tasks, links, dispatcher). |
| hermes project | Manage named, multi-folder workspaces (projects). Anchors desktop session grouping and, when bound to a kanban board, gives tasks a deterministic worktree + branch convention. State is per-profile. |
| hermes webhook | Manage dynamic webhook subscriptions for event-driven activation. |
| hermes hooks | Inspect, approve, or remove shell-script hooks declared inconfig.yaml. |
| hermes doctor | Diagnose config and dependency issues. |
| hermes security audit | On-demand supply-chain audit (OSV.dev) for the venv, plugin requirements, and pinned MCP servers. |
| hermes dump | Copy-pasteable setup summary for support/debugging. |
| hermes prompt-size | Show a byte breakdown of the system prompt + tool schemas (skills index, memory, profile). Runs offline. |
| hermes debug | Debug tools — upload logs and system info for support. |
| hermes backup | Back up Hermes home directory to a zip file. |
| hermes checkpoints | Inspect / prune / clear~/.hermes/checkpoints/(the shadow store used by/rollback). Run with no args for a status overview. |
| hermes import | Restore a Hermes backup from a zip file. |
| hermes logs | View, tail, and filter agent/gateway/error log files. |
| hermes config | Show, edit, migrate, and query configuration files. |
| hermes pairing | Approve or revoke messaging pairing codes. |
| hermes skills | Browse, install, publish, audit, and configure skills. |
| hermes bundles | Group several skills under a single/<name>slash command. SeeSkill Bundles. |
| hermes curator | Background skill maintenance — status, run, pause, pin. SeeCurator. |
| hermes memory | Configure external memory provider. Plugin-specific subcommands (e.g.hermes honcho) register automatically when their provider is active. |
| hermes acp | Run Hermes as an ACP server for editor integration. |
| hermes mcp | Manage MCP server configurations and run Hermes as an MCP server. |
| hermes plugins | Manage Hermes Agent plugins (install, enable, disable, remove). |
| hermes portal | Nous Portal status, subscription link, and Tool Gateway routing. SeeTool Gateway. |
| hermes tools | Configure enabled tools per platform. |
| hermes computer-use | Install or check the cua-driver backend (macOS Computer Use). |
| hermes pets | Browse, install, and selectpetdexanimated pets shown across the CLI, TUI, and desktop app. Subcommands:list,install,select,show,off,scale,remove,doctor. |
| hermes sessions | Browse, export, prune, rename, and delete sessions. |
| hermes insights | Show token/cost/activity analytics. |
| hermes claw | OpenClaw migration helpers. |
| hermes dashboard | Launch the web dashboard for managing config, API keys, and sessions. |
| hermes desktop(aliasgui) | Build and launch the native Electron desktop app. |
| hermes profile | Manage profiles — multiple isolated Hermes instances. |
| hermes completion | Print shell completion scripts (bash/zsh/fish). |
| hermes version | Show version information. |
| hermes update | Pull latest code and reinstall dependencies.--checkpreviews without installing;--backuptakes a pre-pullHERMES_HOMEsnapshot. |
| hermes uninstall | Remove Hermes from the system. |

`hermes chat`
`hermes model`
`hermes moa`
`hermes fallback`
`hermes gateway`
`hermes proxy`
[Subscription Proxy](/docs/user-guide/features/subscription-proxy)
`hermes lsp`
`hermes setup`
`hermes whatsapp`
`hermes whatsapp-cloud`
`hermes whatsapp`
`hermes slack`
`hermes auth`
`hermes login`
`logout`
`hermes auth`
`hermes send`
`hermes secrets`
`~/.hermes/.env`
`hermes migrate`
`config.yaml`
`migrate xai`
`hermes status`
`hermes cron`
`hermes kanban`
`hermes project`
`hermes webhook`
`hermes hooks`
`config.yaml`
`hermes doctor`
`hermes security audit`
`hermes dump`
`hermes prompt-size`
`hermes debug`
`hermes backup`
`hermes checkpoints`
`~/.hermes/checkpoints/`
`/rollback`
`hermes import`
`hermes logs`
`hermes config`
`hermes pairing`
`hermes skills`
`hermes bundles`
`/<name>`
[Skill Bundles](/docs/user-guide/features/skills#skill-bundles)
`hermes curator`
[Curator](/docs/user-guide/features/curator)
`hermes memory`
`hermes honcho`
`hermes acp`
`hermes mcp`
`hermes plugins`
`hermes portal`
[Tool Gateway](/docs/user-guide/features/tool-gateway)
`hermes tools`
`hermes computer-use`
`hermes pets`
[petdex](/docs/user-guide/features/pets)
`list`
`install`
`select`
`show`
`off`
`scale`
`remove`
`doctor`
`hermes sessions`
`hermes insights`
`hermes claw`
`hermes dashboard`
`hermes desktop`
`gui`
`hermes profile`
`hermes completion`
`hermes version`
`hermes update`
`--check`
`--backup`
`HERMES_HOME`
`hermes uninstall`

## hermes chat​

`hermes chat`

```
hermes chat [options]
```

Common options:

| Option | Description |
| --- | --- |
| -q,--query "..." | One-shot, non-interactive prompt. |
| -m,--model <model> | Override the model for this run. |
| -t,--toolsets <csv> | Enable a comma-separated set of toolsets. |
| --provider <provider> | Force a provider:auto,openrouter,nous,openai-codex,copilot-acp,copilot,anthropic,gemini,huggingface,novita(aliasesnovita-ai,novitaai),openai-api,zai,kimi-coding,kimi-coding-cn,minimax,minimax-cn,minimax-oauth,kilocode,xiaomi,arcee,gmi,alibaba,alibaba-coding-plan(aliasalibaba_coding),deepseek,nvidia,ollama-cloud,xai(aliasgrok),xai-oauth(aliasgrok-oauth),qwen-oauth,bedrock,opencode-zen,opencode-go,azure-foundry,lmstudio,stepfun,tencent-tokenhub(aliastencent,tokenhub). |
| -s,--skills <name> | Preload one or more skills for the session (can be repeated or comma-separated). |
| -v,--verbose | Verbose output. |
| -Q,--quiet | Programmatic mode: suppress banner/spinner/tool previews. |
| --image <path> | Attach a local image to a single query. |
| --resume <session>/--continue [name] | Resume a session directly fromchat. |
| --worktree | Create an isolated git worktree for this run. |
| --checkpoints | Enable filesystem checkpoints before destructive file changes. |
| --yolo | Skip approval prompts. |
| --pass-session-id | Pass the session ID into the system prompt. |
| --ignore-user-config | Ignore~/.hermes/config.yamland use built-in defaults. Credentials in.envare still loaded. Useful for isolated CI runs, reproducible bug reports, and third-party integrations. |
| --ignore-rules | Skip auto-injection ofAGENTS.md,SOUL.md,.cursorrules, persistent memory, and preloaded skills. Combine with--ignore-user-configfor a fully isolated run. |
| --safe-mode | Troubleshooting mode: disable ALL customizations — user config, rules/memory injection, plugins, shell hooks, and MCP servers (implies--ignore-user-configand--ignore-rules). Use to isolate whether a problem comes from your setup or from Hermes itself. |
| --source <tag> | Session source tag for filtering (default:cli). Usetoolfor third-party integrations that should not appear in user session lists. |
| --max-turns <N> | Maximum tool-calling iterations per conversation turn (default: 90, oragent.max_turnsin config). |

`-q`
`--query "..."`
`-m`
`--model <model>`
`-t`
`--toolsets <csv>`
`--provider <provider>`
`auto`
`openrouter`
`nous`
`openai-codex`
`copilot-acp`
`copilot`
`anthropic`
`gemini`
`huggingface`
`novita`
`novita-ai`
`novitaai`
`openai-api`
`zai`
`kimi-coding`
`kimi-coding-cn`
`minimax`
`minimax-cn`
`minimax-oauth`
`kilocode`
`xiaomi`
`arcee`
`gmi`
`alibaba`
`alibaba-coding-plan`
`alibaba_coding`
`deepseek`
`nvidia`
`ollama-cloud`
`xai`
`grok`
`xai-oauth`
`grok-oauth`
`qwen-oauth`
`bedrock`
`opencode-zen`
`opencode-go`
`azure-foundry`
`lmstudio`
`stepfun`
`tencent-tokenhub`
`tencent`
`tokenhub`
`-s`
`--skills <name>`
`-v`
`--verbose`
`-Q`
`--quiet`
`--image <path>`
`--resume <session>`
`--continue [name]`
`chat`
`--worktree`
`--checkpoints`
`--yolo`
`--pass-session-id`
`--ignore-user-config`
`~/.hermes/config.yaml`
`.env`
`--ignore-rules`
`AGENTS.md`
`SOUL.md`
`.cursorrules`
`--ignore-user-config`
`--safe-mode`
`--ignore-user-config`
`--ignore-rules`
`--source <tag>`
`cli`
`tool`
`--max-turns <N>`
`agent.max_turns`

Examples:

```
hermeshermes chat -q "Summarize the latest PRs"hermes chat --provider openrouter --model anthropic/claude-sonnet-4.6hermes chat --toolsets web,terminal,skillshermes chat --quiet -q "Return only JSON"hermes chat --worktree -q "Review this repo and open a PR"hermes chat --ignore-user-config --ignore-rules -q "Repro without my personal setup"hermes chat --safe-mode -q "Is this bug mine or Hermes'?"
```

### hermes -z <prompt>— scripted one-shot​

`hermes -z <prompt>`

For programmatic callers (shell scripts, CI, cron, parent processes piping in a prompt),hermes -zis the purest one-shot entry point:single prompt in, final response text out, nothing else on stdout or stderr.No banner, no spinner, no tool previews, noSession:line — just the agent's final reply as plain text.

`hermes -z`
`Session:`

```
hermes -z "What's the capital of France?"# → Paris.# Parent scripts can cleanly capture the response:answer=$(hermes -z "summarize this" < /path/to/file.txt)
```

Per-run overrides (no mutation to~/.hermes/config.yaml):

`~/.hermes/config.yaml`

| Flag | Equivalent env var | Purpose |
| --- | --- | --- |
| -m/--model <model> | HERMES_INFERENCE_MODEL | Override the model for this run |
| --provider <provider> | (none) | Override the provider for this run |

`-m`
`--model <model>`
`HERMES_INFERENCE_MODEL`
`--provider <provider>`

```
hermes -z "…" --provider openrouter --model openai/gpt-5.5# or:HERMES_INFERENCE_MODEL=anthropic/claude-sonnet-4.6 hermes -z "…"
```

Same agent, same tools, same skills — just strips every interactive / cosmetic layer. If you need tool output in the transcript too, usehermes chat -qinstead;-zis explicitly for "I only want the final answer".

`hermes chat -q`
`-z`

## hermes model​

`hermes model`

Interactive provider + model selector.This is the command for adding new providers, setting up API keys, and running OAuth flows.Run it from your terminal — not from inside an active Hermes chat session.

```
hermes model
```

Use this when you want to:

- add a new provider(OpenRouter, Anthropic, Copilot, DeepSeek, custom, etc.)
- log into OAuth-backed providers (Anthropic, Copilot, Codex, Nous Portal)
- enter or update API keys
- pick from provider-specific model lists
- configure a custom/self-hosted endpoint
- save the new default into config

hermes model(run from your terminal, outside any Hermes session) is thefull provider setup wizard. It can add new providers, run OAuth flows, prompt for API keys, and configure endpoints.

`hermes model`

/model(typed inside an active Hermes chat session) can onlyswitch between providers and models you've already set up. It cannot add new providers, run OAuth, or prompt for API keys.

`/model`

If you need to add a new provider:Exit your Hermes session first (Ctrl+Cor/quit), then runhermes modelfrom your terminal prompt.

`Ctrl+C`
`/quit`
`hermes model`

### /modelslash command (mid-session)​

`/model`

Switch between already-configured models without leaving a session:

```
/model                              # Show current model and available options/model claude-sonnet-4              # Switch model (auto-detects provider)/model zai:glm-5                    # Switch provider and model/model custom:qwen-2.5              # Use model on your custom endpoint/model custom                       # Auto-detect model from custom endpoint/model custom:local:qwen-2.5        # Use a named custom provider/model openrouter:anthropic/claude-sonnet-4  # Switch back to cloud
```

By default,/modelchanges applyto the current session only. Add--globalto persist the change toconfig.yaml:

`/model`
`--global`
`config.yaml`

```
/model claude-sonnet-4 --global     # Switch and save as new default
```

If you've only configured OpenRouter,/modelwill only show OpenRouter models. To add another provider (Anthropic, DeepSeek, Copilot, etc.), exit your session and runhermes modelfrom the terminal.

`/model`
`hermes model`

Provider and base URL changes are persisted toconfig.yamlautomatically. When switching away from a custom endpoint, the stale base URL is cleared to prevent it leaking into other providers.

`config.yaml`

## hermes gateway​

`hermes gateway`

```
hermes gateway <subcommand>
```

Subcommands:

| Subcommand | Description |
| --- | --- |
| run | Run the gateway in the foreground. Recommended for WSL, Docker, and Termux. |
| start | Start the installed systemd/launchd background service. |
| stop | Stop the service (or foreground process). |
| restart | Restart the service. |
| status | Show service status. |
| list | Listall profilesand whether each profile's gateway is currently running (with PID where available). Handy when you run multiple profiles side-by-side and want a single overview. |
| install | Install as a systemd (Linux) or launchd (macOS) background service. |
| uninstall | Remove the installed service. |
| setup | Interactive messaging-platform setup. |
| migrate-legacy | Remove legacyhermes.serviceunits left over from pre-rename installs. Profile units (hermes-gateway-<profile>.service) and unrelated services are never touched. Flags:--dry-run,-y/--yes. |
| enroll | Experimental: enroll this gateway with a relay connector and save relay credentials for connector-backed platforms. |

`run`
`start`
`stop`
`restart`
`status`
`list`
`install`
`uninstall`
`setup`
`migrate-legacy`
`hermes.service`
`hermes-gateway-<profile>.service`
`--dry-run`
`-y`
`--yes`
`enroll`

Options:

| Option | Description |
| --- | --- |
| --all | Onstart/restart/stop: act onevery profile'sgateway, not just the activeHERMES_HOME. Useful if you run multiple profiles side-by-side and want to restart them all afterhermes update. |
| --no-supervise | Onrun: inside the s6-overlay Docker image, opt out of auto-supervision and use pre-s6 foreground semantics — gateway runs as the container's main process with no auto-restart. No-op outside the s6 image. Equivalent to settingHERMES_GATEWAY_NO_SUPERVISE=1. |

`--all`
`start`
`restart`
`stop`
`HERMES_HOME`
`hermes update`
`--no-supervise`
`run`
`HERMES_GATEWAY_NO_SUPERVISE=1`

hermes gateway enrollaccepts--token,--connector-url,--gateway-id, and--wake-url. It exchanges the enrollment token with the connector and writes the resultingGATEWAY_RELAY_ID,GATEWAY_RELAY_SECRET,GATEWAY_RELAY_DELIVERY_KEY, optionalGATEWAY_RELAY_URL, and (when--wake-urlis given)GATEWAY_RELAY_WAKE_URLvalues to the active profile's.env.

`hermes gateway enroll`
`--token`
`--connector-url`
`--gateway-id`
`--wake-url`
`GATEWAY_RELAY_ID`
`GATEWAY_RELAY_SECRET`
`GATEWAY_RELAY_DELIVERY_KEY`
`GATEWAY_RELAY_URL`
`--wake-url`
`GATEWAY_RELAY_WAKE_URL`
`.env`

Usehermes gateway runinstead ofhermes gateway start— WSL's systemd support is unreliable. Wrap it in tmux for persistence:tmux new -s hermes 'hermes gateway run'. SeeWSL FAQfor details.

`hermes gateway run`
`hermes gateway start`
`tmux new -s hermes 'hermes gateway run'`
[WSL FAQ](/docs/reference/faq#wsl-gateway-keeps-disconnecting-or-hermes-gateway-start-fails)

## hermes lsp​

`hermes lsp`

```
hermes lsp <subcommand>
```

Manage the Language Server Protocol integration. LSP runs real
language servers (pyright, gopls, rust-analyzer, …) in the
background and feeds their diagnostics into the post-write check
used bywrite_fileandpatch. Gated on git workspace detection
— LSP only runs when the cwd or edited file is inside a git
worktree.

`write_file`
`patch`

Subcommands:

| Subcommand | Description |
| --- | --- |
| status | Show service state, configured servers, install status. |
| list | Print the registry of supported servers. Pass--installed-onlyto skip missing ones. |
| install <id> | Eagerly install one server's binary. |
| install-all | Install every server with a known auto-install recipe. |
| restart | Tear down running clients so the next edit re-spawns. |
| which <id> | Print the resolved binary path for one server. |

`status`
`list`
`--installed-only`
`install <id>`
`install-all`
`restart`
`which <id>`

SeeLSP — Semantic Diagnosticsfor
the full guide, supported languages, and configuration knobs.

[LSP — Semantic Diagnostics](/docs/user-guide/features/lsp)

## hermes setup​

`hermes setup`

```
hermes setup [model|tts|terminal|gateway|tools|agent] [--non-interactive] [--reset] [--quick] [--reconfigure] [--portal]
```

Easiest path:hermes setup --portal— OAuth into Nous Portal and opt into theTool Gatewayin one shot.

`hermes setup --portal`
[Tool Gateway](/docs/user-guide/features/tool-gateway)

First run:launches the first-time wizard.

Returning user (already configured):drops straight into the full reconfigure wizard — every prompt shows your current value as its default, press Enter to keep or type a new value. No menu.

Jump into one section instead of the full wizard:

| Section | Description |
| --- | --- |
| model | Provider and model setup. |
| terminal | Terminal backend and sandbox setup. |
| gateway | Messaging platform setup. |
| tools | Enable/disable tools per platform. |
| agent | Agent behavior settings. |

`model`
`terminal`
`gateway`
`tools`
`agent`

Options:

| Option | Description |
| --- | --- |
| --quick | On returning-user runs: only prompt for items that are missing or unset. Skip items you already have configured. |
| --non-interactive | Use defaults / environment values without prompts. |
| --reset | Reset configuration to defaults before setup. |
| --reconfigure | Backwards-compat alias — barehermes setupon an existing install now does this by default. |
| --portal | One-shot Nous Portal setup: log in via OAuth, set Nous as the inference provider, and opt into theTool Gateway. Skips the rest of the wizard. |

`--quick`
`--non-interactive`
`--reset`
`--reconfigure`
`hermes setup`
`--portal`
[Tool Gateway](/docs/user-guide/features/tool-gateway)

## hermes portal​

`hermes portal`

```
hermes portal [status|open|tools]
```

Inspect Nous Portal auth, Tool Gateway routing, and reach the subscription page. Subcommand-less invocation runsstatus.

`status`

| Subcommand | Description |
| --- | --- |
| status(default) | Portal auth state + per-tool Tool Gateway routing summary. Also shown when no subcommand is given. |
| open | Openportal.nousresearch.com/manage-subscriptionin your default browser. |
| tools | List every Tool Gateway partner (Firecrawl, FAL, OpenAI TTS, Browser Use, Modal) and which are routed via Nous. |

`status`
`open`
`portal.nousresearch.com/manage-subscription`
`tools`

For configuration of the gateway itself, seeTool Gateway. For the one-shot setup path, seehermes setup --portalabove.

[Tool Gateway](/docs/user-guide/features/tool-gateway)
`hermes setup --portal`

## hermes whatsapp​

`hermes whatsapp`

```
hermes whatsapp
```

Runs the WhatsApp pairing/setup flow, including mode selection and QR-code pairing.

## hermes slack​

`hermes slack`

```
hermes slack manifest              # print manifest to stdouthermes slack manifest --write      # write to ~/.hermes/slack-manifest.jsonhermes slack manifest --slashes-only  # just the features.slash_commands array
```

Generates a Slack app manifest that registers every gateway command inCOMMAND_REGISTRY(/btw,/stop,/model, …) as a first-class
Slack slash command — matching Discord and Telegram parity. Paste the
output into your Slack app config athttps://api.slack.com/apps→ your app →Features → App Manifest → Edit, thenSave. Slack prompts for
reinstall if scopes or slash commands changed.

`COMMAND_REGISTRY`
`/btw`
`/stop`
`/model`
[https://api.slack.com/apps](https://api.slack.com/apps)

| Flag | Default | Purpose |
| --- | --- | --- |
| --write [PATH] | stdout | Write to a file instead of stdout. Bare--writewrites$HERMES_HOME/slack-manifest.json. |
| --name NAME | Hermes | Bot display name in Slack. |
| --description DESC | default blurb | Bot description shown in the Slack app directory. |
| --slashes-only | off | Emit onlyfeatures.slash_commandsfor merging into a manually-maintained manifest. |

`--write [PATH]`
`--write`
`$HERMES_HOME/slack-manifest.json`
`--name NAME`
`Hermes`
`--description DESC`
`--slashes-only`
`features.slash_commands`

Runhermes slack manifest --writeagain afterhermes updateto pick
up any new commands.

`hermes slack manifest --write`
`hermes update`

## hermes send​

`hermes send`

```
hermes send --to <target> "message text"hermes send --to <target> --file <path>echo "message" | hermes send --to <target>hermes send --list [platform]
```

Send a one-shot message to a configured messaging platform without spinning up an agent or gateway loop. Reuses the gateway's already-configured credentials (~/.hermes/.env+~/.hermes/config.yaml) so ops scripts, cron jobs, CI hooks, and monitoring daemons can post status updates without reimplementing each platform's REST client.

`~/.hermes/.env`
`~/.hermes/config.yaml`

For bot-token platforms (Telegram, Discord, Slack, Signal, SMS, WhatsApp-CloudAPI) no running gateway is required —hermes sendtalks directly to the platform's REST endpoint. Plugin platforms that need a persistent adapter still require a live gateway.

`hermes send`

| Option | Description |
| --- | --- |
| -t,--to <TARGET> | Delivery target. Formats:platform(uses home channel),platform:chat_id,platform:chat_id:thread_id, orplatform:#channel-name. Examples:telegram,telegram:-1001234567890,discord:#ops,slack:C0123ABCD,signal:+15551234567. |
| -f,--file <PATH> | Read the message body fromPATH(text files only — logs, reports, markdown). Pass-to force reading from stdin. To send an image or other binary file, useMEDIA:<path>(see below). |
| -s,--subject <LINE> | Prepend a subject/header line before the message body. |
| -l,--list [platform] | List configured targets across all platforms (or only the given platform). |
| -q,--quiet | Suppress stdout on success — useful in scripts (rely on exit code only). |
| --json | Emit raw JSON result instead of human-readable output. |

`-t`
`--to <TARGET>`
`platform`
`platform:chat_id`
`platform:chat_id:thread_id`
`platform:#channel-name`
`telegram`
`telegram:-1001234567890`
`discord:#ops`
`slack:C0123ABCD`
`signal:+15551234567`
`-f`
`--file <PATH>`
`PATH`
`-`
`MEDIA:<path>`
`-s`
`--subject <LINE>`
`-l`
`--list [platform]`
`-q`
`--quiet`
`--json`

If neither a positionalmessageargument nor--fileis provided,hermes sendreads from stdin when it is not a TTY. Exit codes:0on success,1on delivery/backend failure,2on usage errors.

`message`
`--file`
`hermes send`
`0`
`1`
`2`

### Sending images and other media​

--fileis fortextbodies only. To deliver an image, document, video, or audio file as a native platform attachment, reference it inside the message text with theMEDIA:<local_path>directive:

`--file`
`MEDIA:<local_path>`

```
hermes send --to telegram "MEDIA:/tmp/screenshot.png"hermes send --to telegram "Build chart for today MEDIA:/tmp/chart.png"   # with captionhermes send --to discord:#ops "MEDIA:/tmp/report.pdf"
```

By default, image files are sent as photos (platforms like Telegram recompress these). Add[[as_document]]to the message to deliver them as uncompressed file attachments instead:

`[[as_document]]`

```
hermes send --to telegram "[[as_document]] MEDIA:/tmp/screenshot.png"
```

Examples:

```
hermes send --to telegram "deploy finished"echo "RAM 92%" | hermes send --to telegram:-1001234567890hermes send --to discord:#ops --file /tmp/report.mdhermes send --to slack:#eng --subject "[CI]" --file build.loghermes send --list                  # all platformshermes send --list telegram         # filter by platform
```

## hermes secrets​

`hermes secrets`

```
hermes secrets bitwarden <subcommand>hermes secrets bw <subcommand>          # short alias
```

Pull API keys from an external secret manager at process startup instead of storing them in~/.hermes/.env. Currently supportsBitwarden Secrets Manager. See the full guide:Bitwarden integration.

`~/.hermes/.env`
[Bitwarden integration](/docs/user-guide/secrets/bitwarden)

bitwarden(aliasbw) subcommands:

`bitwarden`
`bw`

| Subcommand | Description |
| --- | --- |
| setup | Interactive wizard: install the pinnedbwsbinary, store an access token, and pick a project. Accepts--project-id,--access-token, and--server-urlfor non-interactive use. |
| status | Show current config, binary path/version, and last fetch info. |
| sync | Fetch secrets now and report what changed. Add--applyto actually export the secrets into the current shell's environment (default is dry-run). |
| install | Download and verify the pinnedbwsbinary.--forcere-downloads even if a managed copy already exists. |
| disable | Turn off the Bitwarden integration. |

`setup`
`bws`
`--project-id`
`--access-token`
`--server-url`
`status`
`sync`
`--apply`
`install`
`bws`
`--force`
`disable`

## hermes migrate​

`hermes migrate`

```
hermes migrate <type>
```

Diagnose and (optionally) rewrite the activeconfig.yamlto replace references to retired models or deprecated settings. A timestamped backup of the originalconfig.yamlis taken before any rewrite (skip with--no-backup).

`config.yaml`
`config.yaml`
`--no-backup`

| Subcommand | Description |
| --- | --- |
| xai | Scanconfig.yamlfor references to xAI models scheduled for retirement on May 15, 2026 and (with--apply) rewrite them in-place to the official replacements per the xAI migration guide. Defaults to dry-run. |

`xai`
`config.yaml`
`--apply`

Common flags for migration subcommands:

| Flag | Description |
| --- | --- |
| --apply | Rewriteconfig.yamlin-place (default: dry-run, no writes). |
| --no-backup | Skip the timestamped backup ofconfig.yamlwhen applying. |

`--apply`
`config.yaml`
`--no-backup`
`config.yaml`

> Not to be confused withhermes claw migrate(one-shot import of OpenClaw configuration into Hermes) —hermes migrateis the top-level config-rewrite command.

Not to be confused withhermes claw migrate(one-shot import of OpenClaw configuration into Hermes) —hermes migrateis the top-level config-rewrite command.

`hermes claw migrate`
`hermes migrate`

## hermes proxy​

`hermes proxy`

```
hermes proxy <subcommand>
```

Run a local OpenAI-compatible HTTP server that forwards requests to an OAuth-authenticated upstream provider (e.g. Nous Portal, xAI). External apps can point at the proxy with any bearer token; the proxy attaches your real OAuth credentials on the way out. SeeSubscription Proxyfor the full guide.

[Subscription Proxy](/docs/user-guide/features/subscription-proxy)

| Subcommand | Description |
| --- | --- |
| start | Run the proxy in the foreground. Flags:--provider <nous|xai>(defaultnous),--host <addr>(default127.0.0.1; use0.0.0.0to expose on LAN),--port <int>(default8645). |
| status | Show which proxy upstreams are ready (credentials present, OAuth valid). |
| providers | List available proxy upstream providers. |

`start`
`--provider <nous|xai>`
`nous`
`--host <addr>`
`127.0.0.1`
`0.0.0.0`
`--port <int>`
`8645`
`status`
`providers`

## hermes security​

`hermes security`

```
hermes security <subcommand>
```

On-demand vulnerability scan againstOSV.dev. Covers the Hermes venv (installed PyPI distributions), Python dependencies declared by plugins under~/.hermes/plugins/, and pinnednpx/uvxMCP servers inconfig.yaml. Does NOT scan globally-installed packages or editor/browser extensions.

[OSV.dev](https://osv.dev)
`~/.hermes/plugins/`
`npx`
`uvx`
`config.yaml`

| Subcommand | Description |
| --- | --- |
| audit | Run a one-shot supply-chain audit. |

`audit`

auditflags:

`audit`

| Flag | Default | Description |
| --- | --- | --- |
| --json | off | Emit machine-readable JSON instead of human-readable text. |
| --fail-on <level> | critical | Exit non-zero when any finding meets this severity (low,moderate,high,critical). |
| --skip-venv | off | Skip scanning the Hermes Python venv. |
| --skip-plugins | off | Skip scanning plugin requirements files. |
| --skip-mcp | off | Skip scanning pinned MCP servers inconfig.yaml. |

`--json`
`--fail-on <level>`
`critical`
`low`
`moderate`
`high`
`critical`
`--skip-venv`
`--skip-plugins`
`--skip-mcp`
`config.yaml`

## hermes login/hermes logout(Deprecated)​

`hermes login`
`hermes logout`

hermes loginhas been removed. Usehermes authto manage OAuth credentials,hermes modelto select a provider, orhermes setupfor full interactive setup.

`hermes login`
`hermes auth`
`hermes model`
`hermes setup`

## hermes auth​

`hermes auth`

Manage credential pools for same-provider key rotation. SeeCredential Poolsfor full documentation.

[Credential Pools](/docs/user-guide/features/credential-pools)

```
hermes auth                                              # Interactive wizardhermes auth list                                         # Show all poolshermes auth list openrouter                              # Show specific providerhermes auth add openrouter --api-key sk-or-v1-xxx        # Add API keyhermes auth add anthropic --type oauth                   # Add OAuth credentialhermes auth remove openrouter 2                          # Remove by indexhermes auth reset openrouter                             # Clear cooldownshermes auth status anthropic                             # Show auth status for a providerhermes auth logout anthropic                             # Log out and clear stored auth statehermes auth spotify                                      # Authenticate Hermes with Spotify via PKCE
```

Subcommands:add,list,remove,reset,status,logout,spotify. When called with no subcommand, launches the interactive management wizard.

`add`
`list`
`remove`
`reset`
`status`
`logout`
`spotify`

## hermes status​

`hermes status`

```
hermes status [--all] [--deep]
```

| Option | Description |
| --- | --- |
| --all | Show all details in a shareable redacted format. |
| --deep | Run deeper checks that may take longer. |

`--all`
`--deep`

## hermes cron​

`hermes cron`

```
hermes cron <list|create|edit|pause|resume|run|remove|status|tick>
```

| Subcommand | Description |
| --- | --- |
| list | Show scheduled jobs. |
| create/add | Create a scheduled job from a prompt, optionally attaching one or more skills via repeated--skill. |
| edit | Update a job's schedule, prompt, name, delivery, repeat count, or attached skills. Supports--clear-skills,--add-skill, and--remove-skill. |
| pause | Pause a job without deleting it. |
| resume | Resume a paused job and compute its next future run. |
| run | Trigger a job on the next scheduler tick. |
| remove | Delete a scheduled job. |
| status | Check whether the cron scheduler is running. |
| tick | Run due jobs once and exit. |

`list`
`create`
`add`
`--skill`
`edit`
`--clear-skills`
`--add-skill`
`--remove-skill`
`pause`
`resume`
`run`
`remove`
`status`
`tick`

The crontriggeris pluggable via thecron.providerconfig key. Empty
(the default) uses the built-in in-process ticker. Set it tochronos(the
NAS-managed provider for scale-to-zero hosted gateways) — configured via thecron.chronos.*keys (portal_url,callback_url,expected_audience,nas_jwks_url) — or name a custom provider underplugins/cron/<name>/or$HERMES_HOME/plugins/<name>/. An unknown or unavailable provider falls back to
the built-in, so cron is never left without a trigger. See thecron internalsdoc.

`cron.provider`
`chronos`
`cron.chronos.*`
`portal_url`
`callback_url`
`expected_audience`
`nas_jwks_url`
`plugins/cron/<name>/`
`$HERMES_HOME/plugins/<name>/`
[cron internals](/docs/developer-guide/cron-internals#gateway-integration)

## hermes kanban​

`hermes kanban`

```
hermes kanban [--board <slug>] <action> [options]
```

Multi-profile, multi-project collaboration board. Each install can host many boards (one per project, repo, or domain); each board is a standalone queue with its own SQLite DB and dispatcher scope. New installs start with one board calleddefault, whose DB is~/.hermes/kanban.dbfor back-compat; additional boards live at~/.hermes/kanban/boards/<slug>/kanban.db. The gateway-embedded dispatcher sweeps every board per tick.

`default`
`~/.hermes/kanban.db`
`~/.hermes/kanban/boards/<slug>/kanban.db`

Global flags (apply to every action below):

| Flag | Purpose |
| --- | --- |
| --board <slug> | Operate on a specific board. Defaults to the current board (set viahermes kanban boards switch, theHERMES_KANBAN_BOARDenv var, ordefault). |

`--board <slug>`
`hermes kanban boards switch`
`HERMES_KANBAN_BOARD`
`default`

This is the human / scripting surface.Agent workers spawned by the dispatcher drive the board through a dedicatedkanban_*toolset(kanban_show,kanban_complete,kanban_block,kanban_create,kanban_link,kanban_comment,kanban_heartbeat; orchestrator profiles also getkanban_listandkanban_unblock) instead of shelling tohermes kanban. Workers haveHERMES_KANBAN_BOARDpinned in their env so they physically cannot see other boards.

`kanban_*`
[toolset](/docs/user-guide/features/kanban#how-workers-interact-with-the-board)
`kanban_show`
`kanban_complete`
`kanban_block`
`kanban_create`
`kanban_link`
`kanban_comment`
`kanban_heartbeat`
`kanban_list`
`kanban_unblock`
`hermes kanban`
`HERMES_KANBAN_BOARD`

| Action | Purpose |
| --- | --- |
| init | Createkanban.dbif missing. Idempotent. |
| boards list/boards ls | List all boards with task counts.--json,--all(include archived). |
| boards create <slug> | Create a new board. Flags:--name,--description,--icon,--color,--switch(make active). Slug is kebab-case, auto-downcased. |
| boards switch <slug>/boards use | Persist<slug>as the active board (writes~/.hermes/kanban/current). |
| boards show/boards current | Print the currently-active board's name, DB path, and task counts. |
| boards rename <slug> "<name>" | Change a board's display name. Slug is immutable. |
| boards rm <slug> | Archive (default) or hard-delete a board.--deleteskips the archive step. Archived boards move toboards/_archived/<slug>-<ts>/. Refused fordefault. |
| create "<title>" | Create a new task on the active board. Flags:--body,--assignee,--parent(repeatable),--workspace scratch|worktree|dir:<path>,--tenant,--priority,--triage,--idempotency-key,--max-runtime,--max-retries,--skill(repeatable). |
| list/ls | List tasks on the active board. Filter with--mine,--assignee,--status,--tenant,--archived,--json. |
| show <id> | Show a task with comments and events.--jsonfor machine output. |
| assign <id> <profile> | Assign or reassign. Usenoneto unassign. Refused while task is running. |
| link <parent> <child> | Add a dependency. Cycle-detected. Both tasks must be on the same board. |
| unlink <parent> <child> | Remove a dependency. |
| claim <id> | Atomically claim a ready task. Prints resolved workspace path. |
| comment <id> "<text>" | Append a comment. The next worker that claims the task reads it as part of itskanban_show()response. |
| complete <id> | Mark task done. Flags:--result,--summary,--metadata. |
| block <id> "<reason>" | Mark task blocked for human input. Also appends the reason as a comment. |
| schedule <id> "<reason>" | Park time-delay/follow-up work inscheduledso it is not shown as a human blocker. |
| unblock <id> | Return a blocked or scheduled task to ready (ortodoif dependencies are still open). |
| archive <id> | Hide from default list.gcwill remove scratch workspaces. |
| tail <id> | Follow a task's event stream. |
| dispatch | One dispatcher pass on the active board. Flags:--dry-run,--max N,--failure-limit N,--json. |
| context <id> | Print the full context a worker would see (title + body + parent results + comments). |
| specify <id>/specify --all | Flesh out a triage-column task into a concrete spec (title + body with goal, approach, acceptance criteria) via the auxiliary LLM, then promote it totodo. Flags:--tenant(scope--allto one tenant),--author,--json. Configure the model underauxiliary.triage_specifierinconfig.yaml. |
| decompose <id>/decompose --all | Fan a triage-column task out into a graph of child tasks routed to specialist profiles by description. Falls back to specify-style single-task promotion when the LLM decides the task doesn't benefit from fan-out. Same flags asspecify. Configure the decomposer model underauxiliary.kanban_decomposerinconfig.yaml;kanban.orchestrator_profileonly controls who owns the root/orchestration task after fan-out. Also runs automatically every dispatcher tick whenkanban.auto_decompose: true(the default). SeeAuto vs Manual orchestration. |
| gc | Remove scratch workspaces for archived tasks. |

`init`
`kanban.db`
`boards list`
`boards ls`
`--json`
`--all`
`boards create <slug>`
`--name`
`--description`
`--icon`
`--color`
`--switch`
`boards switch <slug>`
`boards use`
`<slug>`
`~/.hermes/kanban/current`
`boards show`
`boards current`
`boards rename <slug> "<name>"`
`boards rm <slug>`
`--delete`
`boards/_archived/<slug>-<ts>/`
`default`
`create "<title>"`
`--body`
`--assignee`
`--parent`
`--workspace scratch|worktree|dir:<path>`
`--tenant`
`--priority`
`--triage`
`--idempotency-key`
`--max-runtime`
`--max-retries`
`--skill`
`list`
`ls`
`--mine`
`--assignee`
`--status`
`--tenant`
`--archived`
`--json`
`show <id>`
`--json`
`assign <id> <profile>`
`none`
`link <parent> <child>`
`unlink <parent> <child>`
`claim <id>`
`comment <id> "<text>"`
`kanban_show()`
`complete <id>`
`--result`
`--summary`
`--metadata`
`block <id> "<reason>"`
`schedule <id> "<reason>"`
`scheduled`
`unblock <id>`
`todo`
`archive <id>`
`gc`
`tail <id>`
`dispatch`
`--dry-run`
`--max N`
`--failure-limit N`
`--json`
`context <id>`
`specify <id>`
`specify --all`
`todo`
`--tenant`
`--all`
`--author`
`--json`
`auxiliary.triage_specifier`
`config.yaml`
`decompose <id>`
`decompose --all`
`specify`
`auxiliary.kanban_decomposer`
`config.yaml`
`kanban.orchestrator_profile`
`kanban.auto_decompose: true`
[Auto vs Manual orchestration](/docs/user-guide/features/kanban#auto-vs-manual-orchestration)
`gc`

Examples:

```
# Create a second board and put a task on it without switching away.hermes kanban boards create atm10-server --name "ATM10 Server" --icon 🎮hermes kanban --board atm10-server create "Restart server" --assignee ops# Switch the active board for subsequent calls.hermes kanban boards switch atm10-serverhermes kanban list                  # shows atm10-server tasks# Archive a board (recoverable) or hard-delete it.hermes kanban boards rm atm10-serverhermes kanban boards rm atm10-server --delete
```

Board resolution order (highest precedence first):--board <slug>flag →HERMES_KANBAN_BOARDenv var →~/.hermes/kanban/currentfile →default.

`--board <slug>`
`HERMES_KANBAN_BOARD`
`~/.hermes/kanban/current`
`default`

All actions are also available as a slash command in the gateway (/kanban …), with the same argument surface — includingboardssubcommands and the--boardflag.

`/kanban …`
`boards`
`--board`

For the full design — comparison with Cline Kanban / Paperclip / NanoClaw / Gemini Enterprise, eight collaboration patterns, four user stories, concurrency correctness proof — seedocs/hermes-kanban-v1-spec.pdfin the repository or theKanban user guide.

`docs/hermes-kanban-v1-spec.pdf`
[Kanban user guide](/docs/user-guide/features/kanban)

## hermes project​

`hermes project`

```
hermes project <create|list|show|add-folder|remove-folder|rename|set-primary|use|archive|restore|bind-board>
```

Projects are human-named workspaces that can span multiple folders / repos. They anchor desktop session grouping and, when bound to a kanban board, give tasks a deterministic worktree + branch convention. State is per-profile.

| Subcommand | Description |
| --- | --- |
| create | Create a new project. |
| list(aliasls) | List projects. |
| show | Show a project's details. |
| add-folder | Add a folder / repo to a project. |
| remove-folder | Remove a folder from a project. |
| rename | Rename a project. |
| set-primary | Set the primary folder. |
| use | Set the active project. |
| archive | Archive a project (recoverable). |
| restore | Restore an archived project. |
| bind-board | Bind a kanban board to this project. |

`create`
`list`
`ls`
`show`
`add-folder`
`remove-folder`
`rename`
`set-primary`
`use`
`archive`
`restore`
`bind-board`

## hermes webhook​

`hermes webhook`

```
hermes webhook <subscribe|list|remove|test>
```

Manage dynamic webhook subscriptions for event-driven agent activation. Requires the webhook platform to be enabled in config — if not configured, prints setup instructions.

| Subcommand | Description |
| --- | --- |
| subscribe/add | Create a webhook route. Returns the URL and HMAC secret to configure on your service. |
| list/ls | Show all agent-created subscriptions. |
| remove/rm | Delete a dynamic subscription. Static routes from config.yaml are not affected. |
| test | Send a test POST to verify a subscription is working. |

`subscribe`
`add`
`list`
`ls`
`remove`
`rm`
`test`

### hermes webhook subscribe​

`hermes webhook subscribe`

```
hermes webhook subscribe <name> [options]
```

| Option | Description |
| --- | --- |
| --prompt | Prompt template with{dot.notation}payload references. |
| --events | Comma-separated event types to accept (e.g.issues,pull_request). Empty = all. |
| --description | Human-readable description. |
| --skills | Comma-separated skill names to load for the agent run. |
| --deliver | Delivery target:log(default),telegram,discord,slack,github_comment. |
| --deliver-chat-id | Target chat/channel ID for cross-platform delivery. |
| --secret | Custom HMAC secret. Auto-generated if omitted. |
| --deliver-only | Skip the agent — deliver the rendered--promptas the literal message. Zero LLM cost, sub-second delivery. Requires--deliverto be a real target (notlog). |
| --script | Filter/transform script under~/.hermes/scripts/. The webhook payload is passed as JSON on stdin; JSON stdout replaces the payload, and empty stdout,[SILENT], or a nonzero exit code ignores the webhook. SeeScript Filters and Transforms. |

`--prompt`
`{dot.notation}`
`--events`
`issues,pull_request`
`--description`
`--skills`
`--deliver`
`log`
`telegram`
`discord`
`slack`
`github_comment`
`--deliver-chat-id`
`--secret`
`--deliver-only`
`--prompt`
`--deliver`
`log`
`--script`
`~/.hermes/scripts/`
`[SILENT]`
[Script Filters and Transforms](/docs/user-guide/messaging/webhooks#script-filters-and-transforms)

Subscriptions persist to~/.hermes/webhook_subscriptions.jsonand are hot-reloaded by the webhook adapter without a gateway restart.

`~/.hermes/webhook_subscriptions.json`

## hermes doctor​

`hermes doctor`

```
hermes doctor [--fix]
```

| Option | Description |
| --- | --- |
| --fix | Attempt automatic repairs where possible. |

`--fix`

## hermes dump​

`hermes dump`

```
hermes dump [--show-keys]
```

Outputs a compact, plain-text summary of your entire Hermes setup. Designed to be copy-pasted into Discord, GitHub issues, or Telegram when asking for support — no ANSI colors, no special formatting, just data.

| Option | Description |
| --- | --- |
| --show-keys | Show redacted API key prefixes (first and last 4 characters) instead of justset/not set. |

`--show-keys`
`set`
`not set`

### What it includes​

| Section | Details |
| --- | --- |
| Header | Hermes version, release date, git commit hash |
| Environment | OS, Python version, OpenAI SDK version |
| Identity | Active profile name, HERMES_HOME path |
| Model | Configured default model and provider |
| Terminal | Backend type (local, docker, ssh, etc.) |
| API keys | Presence check for all 22 provider/tool API keys |
| Features | Enabled toolsets, MCP server count, memory provider |
| Services | Gateway status, configured messaging platforms |
| Workload | Cron job counts, installed skill count |
| Config overrides | Any config values that differ from defaults |

### Example output​

```
--- hermes dump ---version:          0.8.0 (2026.4.8) [af4abd2f]os:               Linux 6.14.0-37-generic x86_64python:           3.11.14openai_sdk:       2.24.0profile:          defaulthermes_home:      ~/.hermesmodel:            anthropic/claude-opus-4.6provider:         openrouterterminal:         localapi_keys:  openrouter           set  openai               not set  anthropic            set  nous                 not set  firecrawl            set  ...features:  toolsets:           all  mcp_servers:        0  memory_provider:    built-in  gateway:            running (systemd)  platforms:          telegram, discord  cron_jobs:          3 active / 5 total  skills:             42config_overrides:  agent.max_turns: 250  compression.threshold: 0.85  display.streaming: True--- end dump ---
```

### When to use​

- Reporting a bug on GitHub — paste the dump into your issue
- Asking for help in Discord — share it in a code block
- Comparing your setup to someone else's
- Quick sanity check when something isn't working

hermes dumpis specifically designed for sharing. For interactive diagnostics, usehermes doctor. For a visual overview, usehermes status.

`hermes dump`
`hermes doctor`
`hermes status`

## hermes debug​

`hermes debug`

```
hermes debug share [options]
```

Upload a debug report (system info + recent logs) to a paste service and get a shareable URL. Useful for quick support requests — includes everything a helper needs to diagnose your issue.

| Option | Description |
| --- | --- |
| --lines <N> | Number of log lines to include per log file (default: 200). |
| --expire <days> | Paste expiry in days (default: 7). |
| --nous | Upload to Nous-internal diagnostics storage instead of a public paste service. Use this when Nous support asks for a private diagnostic bundle. |
| --local | Print the report locally instead of uploading. |
| --no-redact | Disable upload-time secret redaction. By default, uploads are redacted. |

`--lines <N>`
`--expire <days>`
`--nous`
`--local`
`--no-redact`

The report includes system info (OS, Python version, Hermes version), recent agent, gateway, GUI/dashboard, and desktop logs (512 KB limit per file), and redacted API key status. By default, uploads are redacted so secrets are not included.

Default uploads use public paste services tried in order: paste.rs, dpaste.com.--nousuploads the same debug bundle to private Nous diagnostics storage instead; the returned viewer link is for the Nous team and auto-deletes after 14 days.

`--nous`

### Examples​

```
hermes debug share              # Upload debug report, print URLhermes debug share --lines 500  # Include more log lineshermes debug share --expire 30  # Keep paste for 30 dayshermes debug share --nous       # Upload a private diagnostics bundle for Nous supporthermes debug share --local      # Print report to terminal (no upload)
```

## hermes backup​

`hermes backup`

```
hermes backup [options]
```

Create a zip archive of your Hermes configuration, skills, sessions, and data. The backup excludes the hermes-agent codebase itself.

| Option | Description |
| --- | --- |
| -o,--output <path> | Output path for the zip file (default:~/hermes-backup-<timestamp>.zip). |
| -q,--quick | Quick snapshot: only critical state files (config.yaml, state.db, .env, auth, cron jobs). Much faster than a full backup. |
| -l,--label <name> | Label for the snapshot (only used with--quick). |

`-o`
`--output <path>`
`~/hermes-backup-<timestamp>.zip`
`-q`
`--quick`
`-l`
`--label <name>`
`--quick`

The backup uses SQLite'sbackup()API for safe copying, so it works correctly even when Hermes is running (WAL-mode safe).

`backup()`

What's excluded from the zip:

- *.db-wal,*.db-shm,*.db-journal— SQLite's WAL / shared-memory / journal sidecars. The*.dbfile already got a consistent snapshot viasqlite3.backup(); shipping the live sidecars alongside it would let a restore see a half-committed state.
- checkpoints/— per-session trajectory caches. Hash-keyed and regenerated per session; wouldn't port cleanly to another install anyway.
- Thehermes-agentcode itself (this is a user-data backup, not a repo snapshot).

`*.db-wal`
`*.db-shm`
`*.db-journal`
`*.db`
`sqlite3.backup()`
`checkpoints/`
`hermes-agent`

### Examples​

```
hermes backup                           # Full backup to ~/hermes-backup-*.ziphermes backup -o /tmp/hermes.zip        # Full backup to specific pathhermes backup --quick                   # Quick state-only snapshothermes backup --quick --label "pre-upgrade"  # Quick snapshot with label
```

## hermes checkpoints​

`hermes checkpoints`

```
hermes checkpoints [COMMAND]
```

Inspect and manage the shadow git store at~/.hermes/checkpoints/— the storage layer behind the in-session/rollbackcommand. Safe to run any time; does not require the agent to be running.

`~/.hermes/checkpoints/`
`/rollback`

| Subcommand | Description |
| --- | --- |
| status(default) | Show total size, project count, and per-project breakdown. Barehermes checkpointsis equivalent. |
| list | Alias forstatus. |
| prune | Force a cleanup sweep — delete orphan and stale projects, GC the store, enforce the size cap. Ignores the 24h idempotency marker. |
| clear | Delete the entire checkpoint base. Irreversible; asks for confirmation unless-f. |
| clear-legacy | Delete only thelegacy-<timestamp>/archives produced by the v1→v2 migration. |

`status`
`hermes checkpoints`
`list`
`status`
`prune`
`clear`
`-f`
`clear-legacy`
`legacy-<timestamp>/`

### Options​

| Option | Subcommand | Description |
| --- | --- | --- |
| --limit N | status,list | Max projects to list (default 20). |
| --retention-days N | prune | Drop projects whoselast_touchis older than N days (default 7). |
| --max-size-mb N | prune | After the orphan/stale pass, drop the oldest commit per project until total store size ≤ N MB (default 500). |
| --keep-orphans | prune | Skip deleting projects whose working directory no longer exists. |
| -f,--force | clear,clear-legacy | Skip the confirmation prompt. |

`--limit N`
`status`
`list`
`--retention-days N`
`prune`
`last_touch`
`--max-size-mb N`
`prune`
`--keep-orphans`
`prune`
`-f`
`--force`
`clear`
`clear-legacy`

### Examples​

```
hermes checkpoints                                  # status overviewhermes checkpoints prune --retention-days 3         # aggressive cleanuphermes checkpoints prune --max-size-mb 200          # tighten size cap oncehermes checkpoints clear-legacy -f                  # drop v1 archive dirshermes checkpoints clear -f                         # wipe everything
```

SeeCheckpoints and/rollbackfor the full architecture and the in-session commands.

[Checkpoints and/rollback](/docs/user-guide/checkpoints-and-rollback)
`/rollback`

## hermes import​

`hermes import`

```
hermes import <zipfile> [options]
```

Restore a previously created Hermes backup into your Hermes home directory. All files in the archive overwrite existing files in your Hermes home;--forceonly skips the confirmation prompt that fires when the target already has a Hermes installation.

`--force`

| Option | Description |
| --- | --- |
| -f,--force | Skip the existing-installation confirmation prompt. |

`-f`
`--force`

Stop the gateway before importing to avoid conflicts with running processes.

### Examples​

```
hermes import ~/hermes-backup-20260423.zip           # Prompts before overwriting existing confighermes import ~/hermes-backup-20260423.zip --force   # Overwrite without prompting
```

## hermes logs​

`hermes logs`

```
hermes logs [log_name] [options]
```

View, tail, and filter Hermes log files. All logs are stored in~/.hermes/logs/(or<profile>/logs/for non-default profiles).

`~/.hermes/logs/`
`<profile>/logs/`

### Log files​

| Name | File | What it captures |
| --- | --- | --- |
| agent(default) | agent.log | All agent activity — API calls, tool dispatch, session lifecycle (INFO and above) |
| errors | errors.log | Warnings and errors only — a filtered subset of agent.log |
| gateway | gateway.log | Messaging gateway activity — platform connections, message dispatch, webhook events |
| gui | gui.log | Dashboard / TUI-gateway / PTY-bridge / websocket events |
| desktop | desktop.log | Electron desktop app — boot, backend spawn output, and recent Python tracebacks |

`agent`
`agent.log`
`errors`
`errors.log`
`gateway`
`gateway.log`
`gui`
`gui.log`
`desktop`
`desktop.log`

### Options​

| Option | Description |
| --- | --- |
| log_name | Which log to view:agent(default),errors,gateway, orlistto show available files with sizes. |
| -n,--lines <N> | Number of lines to show (default: 50). |
| -f,--follow | Follow the log in real time, liketail -f. Press Ctrl+C to stop. |
| --level <LEVEL> | Minimum log level to show:DEBUG,INFO,WARNING,ERROR,CRITICAL. |
| --session <ID> | Filter lines containing a session ID substring. |
| --since <TIME> | Show lines from a relative time ago:30m,1h,2d, etc. Supportss(seconds),m(minutes),h(hours),d(days). |
| --component <NAME> | Filter by component:gateway,agent,tools,cli,cron. |

`log_name`
`agent`
`errors`
`gateway`
`list`
`-n`
`--lines <N>`
`-f`
`--follow`
`tail -f`
`--level <LEVEL>`
`DEBUG`
`INFO`
`WARNING`
`ERROR`
`CRITICAL`
`--session <ID>`
`--since <TIME>`
`30m`
`1h`
`2d`
`s`
`m`
`h`
`d`
`--component <NAME>`
`gateway`
`agent`
`tools`
`cli`
`cron`

### Examples​

```
# View the last 50 lines of agent.log (default)hermes logs# Follow agent.log in real timehermes logs -f# View the last 100 lines of gateway.loghermes logs gateway -n 100# Show only warnings and errors from the last hourhermes logs --level WARNING --since 1h# Filter by a specific sessionhermes logs --session abc123# Follow errors.log, starting from 30 minutes agohermes logs errors --since 30m -f# List all log files with their sizeshermes logs list
```

### Filtering​

Filters can be combined. When multiple filters are active, a log line must passallof them to be shown:

```
# WARNING+ lines from the last 2 hours containing session "tg-12345"hermes logs --level WARNING --since 2h --session tg-12345
```

Lines without a parseable timestamp are included when--sinceis active (they may be continuation lines from a multi-line log entry). Lines without a detectable level are included when--levelis active.

`--since`
`--level`

### Log rotation​

Hermes uses Python'sRotatingFileHandler. Old logs are rotated automatically — look foragent.log.1,agent.log.2, etc. Thehermes logs listsubcommand shows all log files including rotated ones.

`RotatingFileHandler`
`agent.log.1`
`agent.log.2`
`hermes logs list`

## hermes prompt-size​

`hermes prompt-size`

```
hermes prompt-size [--platform <name>] [--json]
```

Reports the fixed prompt budget for a fresh session — what gets sent on every
API callbeforeany conversation content. Useful when a downstream adapter or
proxy has a tighter prompt budget than the model's context window, or when you
want to see which block (skills index, memory, profile) dominates.

It builds the same system prompt the agent would, then breaks it down:

- System prompt total— full assembled prompt (identity, guidance, skills
index, context files, memory, profile, timestamp).
- Skills index— the<available_skills>block. This is often the largest
single block when many skills are installed.
- Memoryanduser profile— yourMEMORY.md/USER.mdsnapshots.
- Prompt tiers— stable / context / volatile, matching how Hermes layers
the prompt for cache-friendliness.
- Tool schemas— the JSON for all enabled tools (the other half of the
fixed per-call payload).

`<available_skills>`
`MEMORY.md`
`USER.md`

Runs entirely offline — no API call, works with no credentials configured.

```
# Human-readable breakdown for the CLI platform (default)hermes prompt-size# Simulate a messaging platform's prompt (different platform hint)hermes prompt-size --platform telegram# Machine-readable output for scriptshermes prompt-size --json
```

The skills index and tool schemas scale with how many skills and tools you have
enabled. To shrink the prompt, disable unused toolsets (hermes tools) or
uninstall skills you don't need (hermes skills). Context files (AGENTS.md,
.cursorrules) in your current directory also count toward the total.

`hermes tools`
`hermes skills`

## hermes config​

`hermes config`

```
hermes config <subcommand>
```

Subcommands:

| Subcommand | Description |
| --- | --- |
| show | Show current config values. |
| edit | Openconfig.yamlin your editor. |
| set <key> <value> | Set a config value. |
| path | Print the config file path. |
| env-path | Print the.envfile path. |
| check | Check for missing or stale config. |
| migrate | Add newly introduced options interactively. |

`show`
`edit`
`config.yaml`
`set <key> <value>`
`path`
`env-path`
`.env`
`check`
`migrate`

## hermes pairing​

`hermes pairing`

```
hermes pairing <list|approve|revoke|clear-pending>
```

| Subcommand | Description |
| --- | --- |
| list | Show pending and approved users. |
| approve <platform> <code> | Approve a pairing code. |
| revoke <platform> <user-id> | Revoke a user's access. |
| clear-pending | Clear pending pairing codes. |

`list`
`approve <platform> <code>`
`revoke <platform> <user-id>`
`clear-pending`

## hermes skills​

`hermes skills`

```
hermes skills <subcommand>
```

Subcommands:

| Subcommand | Description |
| --- | --- |
| browse | Paginated browser for skill registries. |
| search | Search skill registries. |
| install | Install a skill. |
| inspect | Preview a skill without installing it. |
| list | List installed skills. |
| check | Check installed hub skills for upstream updates. |
| update | Reinstall hub skills with upstream changes when available. |
| audit | Re-scan installed hub skills. |
| uninstall | Remove a hub-installed skill. |
| reset | Un-stick a bundled skill flagged asuser_modifiedby clearing its manifest entry. With--restore, also replaces the user copy with the bundled version. |
| opt-out | Stop bundled skills from being seeded into the active profile. Writes a.no-bundled-skillsmarker so the installer,hermes update, and any sync skip bundled-skill seeding. Safe by default — nothing on disk is touched. With--remove, also deletes already-present bundled skills that areunmodified(user-edited, hub-installed, and hand-written skills are never removed; previews and confirms first,--yesto skip). |
| opt-in | Undoopt-outby removing the.no-bundled-skillsmarker so bundled skills are seeded again on the nexthermes update. With--sync, re-seed immediately. |
| publish | Publish a skill to a registry. |
| snapshot | Export/import skill configurations. |
| tap | Manage custom skill sources. |
| config | Interactive enable/disable configuration for skills by platform. |

`browse`
`search`
`install`
`inspect`
`list`
`check`
`update`
`audit`
`uninstall`
`reset`
`user_modified`
`--restore`
`opt-out`
`.no-bundled-skills`
`hermes update`
`--remove`
`--yes`
`opt-in`
`opt-out`
`.no-bundled-skills`
`hermes update`
`--sync`
`publish`
`snapshot`
`tap`
`config`

Common examples:

```
hermes skills browsehermes skills browse --source officialhermes skills search react --source skills-shhermes skills search https://mintlify.com/docs --source well-knownhermes skills inspect official/security/1passwordhermes skills inspect skills-sh/vercel-labs/json-render/json-render-reacthermes skills install official/migration/openclaw-migrationhermes skills install skills-sh/anthropics/skills/pdf --forcehermes skills install https://sharethis.chat/SKILL.md                     # Direct URL (single-file SKILL.md)hermes skills install https://example.com/SKILL.md --name my-skill        # Override name when frontmatter has nonehermes skills checkhermes skills updatehermes skills confighermes skills reset google-workspacehermes skills reset google-workspace --restore --yeshermes skills opt-out                  # stop future bundled-skill seeding (nothing deleted)hermes skills opt-out --remove --yes   # also delete UNMODIFIED bundled skillshermes skills opt-in --sync            # undo: remove marker and re-seed now
```

Notes:

- --forcecan override non-dangerous policy blocks for third-party/community skills.
- --forcedoes not override adangerousscan verdict.
- --source skills-shsearches the publicskills.shdirectory.
- --source well-knownlets you point Hermes at a site exposing/.well-known/skills/index.json.
- --source browse-shsearchesbrowse.sh's catalog of 200+ site-specific browser-automation skills. Identifiers look likebrowse-sh/airbnb.com/search-listings-ddgioa.
- Passing anhttp(s)://…/*.mdURL installs a single-file SKILL.md directly. When frontmatter has noname:and the URL slug isn't a valid identifier, an interactive terminal prompts for a name; non-interactive surfaces (/skills installinside the TUI, gateway platforms) require--name <x>instead.

`--force`
`--force`
`dangerous`
`--source skills-sh`
`skills.sh`
`--source well-known`
`/.well-known/skills/index.json`
`--source browse-sh`
[browse.sh](https://browse.sh)
`browse-sh/airbnb.com/search-listings-ddgioa`
`http(s)://…/*.md`
`name:`
`/skills install`
`--name <x>`

## hermes bundles​

`hermes bundles`

```
hermes bundles <subcommand>
```

Skill bundles group several skills under one/<bundle-name>slash command. Invoking the bundle loads every referenced skill into a single combined user message. Storage:~/.hermes/skill-bundles/<slug>.yaml. SeeSkill Bundlesfor the YAML schema and behavior.

`/<bundle-name>`
`~/.hermes/skill-bundles/<slug>.yaml`
[Skill Bundles](/docs/user-guide/features/skills#skill-bundles)

Subcommands:

| Subcommand | Description |
| --- | --- |
| list | List installed bundles (default when no subcommand given) |
| show <name> | Show one bundle's name, description, skills, and file path |
| create <name> | Create a new bundle. Pass--skill <id>(repeat) or omit for interactive entry.--description,--instruction,--forceavailable. |
| delete <name> | Remove a bundle file |
| reload | Re-scan~/.hermes/skill-bundles/and report added/removed bundles |

`list`
`show <name>`
`create <name>`
`--skill <id>`
`--description`
`--instruction`
`--force`
`delete <name>`
`reload`
`~/.hermes/skill-bundles/`

Examples:

```
hermes bundles create backend-dev \  --skill github-code-review \  --skill test-driven-development \  --skill github-pr-workflow \  -d "Backend feature work"hermes bundles listhermes bundles show backend-devhermes bundles delete backend-dev
```

In a chat session,/bundleslists installed bundles and/<bundle-name>loads one.

`/bundles`
`/<bundle-name>`

## hermes curator​

`hermes curator`

```
hermes curator <subcommand>
```

The curator is an auxiliary-model background task that periodically reviews agent-created skills, prunes stale ones, consolidates overlaps, and archives obsolete skills. Bundled and hub-installed skills are never touched. Archives are recoverable; auto-deletion never happens.

| Subcommand | Description |
| --- | --- |
| status | Show curator status and skill stats |
| run | Trigger a curator review now (blocks until the LLM pass finishes) |
| run --background | Start the LLM pass in a background thread and return immediately |
| run --dry-run | Preview only — produce the review report with no mutations |
| backup | Take a manual tar.gz snapshot of~/.hermes/skills/(curator also snapshots automatically before every real run) |
| rollback | Restore~/.hermes/skills/from a snapshot (defaults to newest) |
| rollback --list | List available snapshots |
| rollback --id <ts> | Restore a specific snapshot by id |
| rollback -y | Skip the confirmation prompt |
| pause | Pause the curator until resumed |
| resume | Resume a paused curator |
| pin <skill> | Pin a skill so the curator never auto-transitions it |
| unpin <skill> | Unpin a skill |
| restore <skill> | Restore an archived skill |
| archive <skill> | Archive a skill manually |
| prune | Manually prune skills the curator would normally clean up |
| list-archived | List archived skills (recoverable viarestore) |

`status`
`run`
`run --background`
`run --dry-run`
`backup`
`~/.hermes/skills/`
`rollback`
`~/.hermes/skills/`
`rollback --list`
`rollback --id <ts>`
`rollback -y`
`pause`
`resume`
`pin <skill>`
`unpin <skill>`
`restore <skill>`
`archive <skill>`
`prune`
`list-archived`
`restore`

On a fresh install the first scheduled pass is deferred by one fullinterval_hours(7 days by default) — the gateway will not curate immediately on the first tick afterhermes update. Usehermes curator run --dry-runto preview before that happens.

`interval_hours`
`hermes update`
`hermes curator run --dry-run`

SeeCuratorfor behavior and config.

[Curator](/docs/user-guide/features/curator)

## hermes moa​

`hermes moa`

Configure named Mixture of Agents presets. Presets appear as selectable models under aMixture of Agentsprovider in every model picker;/moa <prompt>runs one prompt through the default preset.

`Mixture of Agents`
`/moa <prompt>`

```
hermes moa listhermes moa configure [name]hermes moa delete <name>
```

hermes moa configurereuses Hermes' provider → model picker for each reference model and the aggregator. A preset is an execution-mode configuration, not a primary model or provider.

`hermes moa configure`

## hermes fallback​

`hermes fallback`

```
hermes fallback <subcommand>
```

Manage the fallback provider chain. Fallback providers are tried in order when the primary model fails with rate-limit, overload, or connection errors.

| Subcommand | Description |
| --- | --- |
| list(alias:ls) | Show the current fallback chain (default when no subcommand) |
| add | Pick a provider + model (same picker ashermes model) and append to the chain |
| remove(alias:rm) | Pick an entry to delete from the chain |
| clear | Remove all fallback entries |

`list`
`ls`
`add`
`hermes model`
`remove`
`rm`
`clear`

SeeFallback Providers.

[Fallback Providers](/docs/user-guide/features/fallback-providers)

## hermes hooks​

`hermes hooks`

```
hermes hooks <subcommand>
```

Inspect shell-script hooks declared in~/.hermes/config.yaml, test them against synthetic payloads, and manage the first-use consent allowlist at~/.hermes/shell-hooks-allowlist.json.

`~/.hermes/config.yaml`
`~/.hermes/shell-hooks-allowlist.json`

| Subcommand | Description |
| --- | --- |
| list(alias:ls) | List configured hooks with matcher, timeout, and consent status |
| test <event> | Fire every hook matching<event>against a synthetic payload |
| revoke(aliases:remove,rm) | Remove a command's allowlist entries (takes effect on next restart) |
| doctor | Check each configured hook: exec bit, allowlist, mtime drift, JSON validity, and synthetic run timing |

`list`
`ls`
`test <event>`
`<event>`
`revoke`
`remove`
`rm`
`doctor`

SeeHooksfor event signatures and payload shapes.

[Hooks](/docs/user-guide/features/hooks)

## hermes memory​

`hermes memory`

```
hermes memory <subcommand>
```

Set up and manage external memory provider plugins. Available providers: honcho, openviking, mem0, hindsight, holographic, retaindb, byterover, supermemory. Only one external provider can be active at a time. Built-in memory (MEMORY.md/USER.md) is always active.

Subcommands:

| Subcommand | Description |
| --- | --- |
| setup | Interactive provider selection and configuration. |
| status | Show current memory provider config. |
| off | Disable external provider (built-in only). |

`setup`
`status`
`off`

When an external memory provider is active, it may register its own top-levelhermes <provider>command for provider-specific management (e.g.hermes honchowhen Honcho is active). Inactive providers do not expose their subcommands. Runhermes --helpto see what's currently wired in.

`hermes <provider>`
`hermes honcho`
`hermes --help`

## hermes acp​

`hermes acp`

```
hermes acp
```

Starts Hermes as an ACP (Agent Client Protocol) stdio server for editor integration.

Related entrypoints:

```
hermes-acppython -m acp_adapter
```

Install support first:

```
cd ~/.hermes/hermes-agent && uv pip install -e '.[acp]'
```

SeeACP Editor IntegrationandACP Internals.

[ACP Editor Integration](/docs/user-guide/features/acp)
[ACP Internals](/docs/developer-guide/acp-internals)

## hermes mcp​

`hermes mcp`

```
hermes mcp <subcommand>
```

Manage MCP (Model Context Protocol) server configurations and run Hermes as an MCP server.

| Subcommand | Description |
| --- | --- |
| (none)orpicker | Interactive catalog picker — browse Nous-approved MCPs and install/enable/disable. |
| catalog | List Nous-approved MCPs (plain text, scriptable). |
| install <name> | Install a catalog entry (e.g.hermes mcp install n8n). |
| serve [-v|--verbose] | Run Hermes as an MCP server — expose conversations to other agents. |
| add <name> [--url URL] [--command CMD] [--auth oauth|header] [--args ...] | Add a custom MCP server with automatic tool discovery.--argspasses the remaining argv to the stdio command, so put it last. |
| remove <name>(alias:rm) | Remove an MCP server from config. |
| list(alias:ls) | List configured MCP servers. |
| test <name> | Test connection to an MCP server. |
| configure <name>(alias:config) | Toggle tool selection for a server. |
| login <name> | Force re-authentication for an OAuth-based MCP server. |

`picker`
`catalog`
`install <name>`
`hermes mcp install n8n`
`serve [-v|--verbose]`
`add <name> [--url URL] [--command CMD] [--auth oauth|header] [--args ...]`
`--args`
`remove <name>`
`rm`
`list`
`ls`
`test <name>`
`configure <name>`
`config`
`login <name>`

SeeMCP Config Reference,Use MCP with Hermes, andMCP Server Mode.

[MCP Config Reference](/docs/reference/mcp-config-reference)
[Use MCP with Hermes](/docs/guides/use-mcp-with-hermes)
[MCP Server Mode](/docs/user-guide/features/mcp#running-hermes-as-an-mcp-server)

## hermes plugins​

`hermes plugins`

```
hermes plugins [subcommand]
```

Unified plugin management — general plugins, memory providers, and context engines in one place. Runninghermes pluginswith no subcommand opens a composite interactive screen with two sections:

`hermes plugins`
- General Plugins— multi-select checkboxes to enable/disable installed plugins
- Provider Plugins— single-select configuration for Memory Provider and Context Engine. Press ENTER on a category to open a radio picker.

| Subcommand | Description |
| --- | --- |
| (none) | Composite interactive UI — general plugin toggles + provider plugin configuration. |
| install <identifier> [--force] | Install a plugin from a Git URL orowner/repo. |
| update <name> | Pull latest changes for an installed plugin. |
| remove <name>(aliases:rm,uninstall) | Remove an installed plugin. |
| enable <name> | Enable a disabled plugin. |
| disable <name> | Disable a plugin without removing it. |
| list(alias:ls) | List installed plugins with enabled/disabled status. |

`install <identifier> [--force]`
`owner/repo`
`update <name>`
`remove <name>`
`rm`
`uninstall`
`enable <name>`
`disable <name>`
`list`
`ls`

Provider plugin selections are saved toconfig.yaml:

`config.yaml`
- memory.provider— active memory provider (empty = built-in only)
- context.engine— active context engine ("compressor"= built-in default)

`memory.provider`
`context.engine`
`"compressor"`

General plugin disabled list is stored inconfig.yamlunderplugins.disabled.

`config.yaml`
`plugins.disabled`

SeePluginsandBuild a Hermes Plugin.

[Plugins](/docs/user-guide/features/plugins)
[Build a Hermes Plugin](/docs/developer-guide/plugins)

## hermes tools​

`hermes tools`

```
hermes tools [--summary]
```

| Option | Description |
| --- | --- |
| --summary | Print the current enabled-tools summary and exit. |

`--summary`

Without--summary, this launches the interactive per-platform tool configuration UI.

`--summary`

## hermes computer-use​

`hermes computer-use`

```
hermes computer-use <subcommand>
```

Subcommands:

| Subcommand | Description |
| --- | --- |
| install | Run the upstream cua-driver installer (macOS, Windows, and Linux). |
| install --upgrade | Re-run the installer even if cua-driver is already on PATH. The upstream script always pulls the latest release, so this performs an in-place upgrade. |
| status | Print whethercua-driveris on$PATHand which version is installed. |

`install`
`install --upgrade`
`status`
`cua-driver`
`$PATH`

hermes computer-use installis the stable entry point for installing thecua-driverbinary used by thecomputer_usetoolset. It runs the same upstream installer thathermes toolsinvokes when you first enable Computer Use, so it's safe
to use for re-running the install if the toolset toggle didn't trigger
it (for example, on returning-user setups).

`hermes computer-use install`
[cua-driver](https://github.com/trycua/cua)
`computer_use`
`hermes tools`

hermes updateautomatically re-runs the upstream installer at the end
of the update if cua-driver is on PATH, so most users will not need to
call--upgrademanually. Use it when upstream ships a fix you want
right now without waiting for the next Hermes update.

`hermes update`
`--upgrade`

## hermes pets​

`hermes pets`

```
hermes pets <list|install|select|show|off|scale|remove|doctor>
```

Petdexis a public gallery of animated sprite pets for coding agents. Install one and Hermes shows it reacting to agent activity across the CLI, TUI, and desktop app.

[Petdex](https://github.com/crafter-station/petdex)

| Subcommand | Description |
| --- | --- |
| list | Browse the petdex gallery. |
| install | Install a pet from the gallery. |
| select | Set the active pet (writesdisplay.pet.*). |
| show | Animate the active pet in the terminal. |
| off | Disable the pet display. |
| scale | Resize the pet everywhere (display.pet.scale). |
| remove | Delete an installed pet. |
| doctor | Check pet setup + terminal graphics support. |

`list`
`install`
`select`
`display.pet.*`
`show`
`off`
`scale`
`display.pet.scale`
`remove`
`doctor`

You can also generate a brand-new pet from a text description with the/hatchslash command. SeePets.

`/hatch`
[Pets](/docs/user-guide/features/pets)

## hermes sessions​

`hermes sessions`

```
hermes sessions <subcommand>
```

Subcommands:

| Subcommand | Description |
| --- | --- |
| list | List recent sessions. |
| browse | Interactive session picker with search and resume. |
| export <output> [--session-id ID] | Export sessions to JSONL. |
| delete <session-id> | Delete one session. |
| prune | Delete sessions matching filters: time bounds--older-than/--newer-than/--before/--after(durations like5h/2d, bare days, or ISO timestamps); attributes--source,--title,--model,--provider,--branch,--end-reason,--user,--chat-id,--chat-type,--cwd; numeric bounds--min/--max-messages,--min/--max-tokens,--min/--max-cost,--min/--max-tool-calls; plus--include-archived,--dry-run,--yes. Default: older than 90 days. |
| archive | Bulk-archive (soft-hide, no deletion) sessions matching the same filters asprune. Requires at least one filter. |
| stats | Show session-store statistics. |
| rename <session-id> <title> | Set or change a session title. |

`list`
`browse`
`export <output> [--session-id ID]`
`delete <session-id>`
`prune`
`--older-than`
`--newer-than`
`--before`
`--after`
`5h`
`2d`
`--source`
`--title`
`--model`
`--provider`
`--branch`
`--end-reason`
`--user`
`--chat-id`
`--chat-type`
`--cwd`
`--min/--max-messages`
`--min/--max-tokens`
`--min/--max-cost`
`--min/--max-tool-calls`
`--include-archived`
`--dry-run`
`--yes`
`archive`
`prune`
`stats`
`rename <session-id> <title>`

## hermes insights​

`hermes insights`

```
hermes insights [--days N] [--source platform]
```

| Option | Description |
| --- | --- |
| --days <n> | Analyze the lastndays (default: 30). |
| --source <platform> | Filter by source such ascli,telegram, ordiscord. |

`--days <n>`
`n`
`--source <platform>`
`cli`
`telegram`
`discord`

## hermes claw​

`hermes claw`

```
hermes claw migrate [options]
```

Migrate your OpenClaw setup to Hermes. Reads from~/.openclaw(or a custom path) and writes to~/.hermes. Automatically detects legacy directory names (~/.clawdbot,~/.moltbot) and config filenames (clawdbot.json,moltbot.json).

`~/.openclaw`
`~/.hermes`
`~/.clawdbot`
`~/.moltbot`
`clawdbot.json`
`moltbot.json`

| Option | Description |
| --- | --- |
| --dry-run | Preview what would be migrated without writing anything. |
| --preset <name> | Migration preset:full(all compatible settings) oruser-data(excludes infrastructure config). Neither preset imports secrets — pass--migrate-secretsexplicitly. |
| --overwrite | Overwrite existing Hermes files on conflicts (default: refuse to apply when the plan has conflicts). |
| --migrate-secrets | Include API keys in migration. Required even under--preset full. |
| --no-backup | Skip the pre-migration zip snapshot of~/.hermes/(by default a single restore-point archive is written to~/.hermes/backups/pre-migration-*.zipbefore apply; restorable withhermes import). |
| --source <path> | Custom OpenClaw directory (default:~/.openclaw). |
| --workspace-target <path> | Target directory for workspace instructions (AGENTS.md). |
| --skill-conflict <mode> | Handle skill name collisions:skip(default),overwrite, orrename. |
| --yes | Skip the confirmation prompt. |

`--dry-run`
`--preset <name>`
`full`
`user-data`
`--migrate-secrets`
`--overwrite`
`--migrate-secrets`
`--preset full`
`--no-backup`
`~/.hermes/`
`~/.hermes/backups/pre-migration-*.zip`
`hermes import`
`--source <path>`
`~/.openclaw`
`--workspace-target <path>`
`--skill-conflict <mode>`
`skip`
`overwrite`
`rename`
`--yes`

### What gets migrated​

The migration covers 30+ categories across persona, memory, skills, model providers, messaging platforms, agent behavior, session policies, MCP servers, TTS, and more. Items are eitherdirectly importedinto Hermes equivalents orarchivedfor manual review.

Directly imported:SOUL.md, MEMORY.md, USER.md, AGENTS.md, skills (4 source directories), default model, custom providers, MCP servers, messaging platform tokens and allowlists (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost), agent defaults (reasoning effort, compression, human delay, timezone, sandbox), session reset policies, approval rules, TTS config, browser settings, tool settings, exec timeout, command allowlist, gateway config, and API keys from 3 sources.

Archived for manual review:Cron jobs, plugins, hooks/webhooks, memory backend (QMD), skills registry config, UI/identity, logging, multi-agent setup, channel bindings, IDENTITY.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md.

API key resolutionchecks three sources in priority order: config values →~/.openclaw/.env→auth-profiles.json. All token fields handle plain strings, env templates (${VAR}), and SecretRef objects.

`~/.openclaw/.env`
`auth-profiles.json`
`${VAR}`

For the complete config key mapping, SecretRef handling details, and post-migration checklist, see thefull migration guide.

[full migration guide](/docs/guides/migrate-from-openclaw)

### Examples​

```
# Preview what would be migratedhermes claw migrate --dry-run# Full migration (all compatible settings, no secrets)hermes claw migrate --preset full# Full migration including API keyshermes claw migrate --preset full --migrate-secrets# Migrate user data only (no secrets), overwrite conflictshermes claw migrate --preset user-data --overwrite# Migrate from a custom OpenClaw pathhermes claw migrate --source /home/user/old-openclaw
```

## hermes serve​

`hermes serve`

```
hermes serve [options]
```

Start the Hermesbackend server— the JSON-RPC/WebSocket gateway thedesktop appand remote clients connect to. It is the same serverhermes dashboardruns, butheadless: it never opens a browser UI. The desktop app launches its ownhermes servebackend; use this command directly when you want a headless backend on a remote host. Accepts the same--host/--port/--insecure/--skip-build/--stop/--statusoptions ashermes dashboardbelow (a non-loopback bind engages the same auth gate). Requires the[web]extra; the embedded Chat socket additionally needs[pty]on a POSIX host.

[desktop app](/docs/user-guide/desktop)
`hermes dashboard`
`hermes serve`
`--host`
`--port`
`--insecure`
`--skip-build`
`--stop`
`--status`
`hermes dashboard`
`[web]`
`[pty]`

## hermes dashboard​

`hermes dashboard`

```
hermes dashboard [options]
```

Launch the web dashboard — a browser-based UI for managing configuration, API keys, and monitoring sessions. (For a headless backend with no browser UI — e.g. what the desktop app spawns — usehermes serveabove.) Requirescd ~/.hermes/hermes-agent && uv pip install -e ".[web]"(FastAPI + Uvicorn). The embedded browser Chat tab is always available and additionally needs theptyextra (cd ~/.hermes/hermes-agent && uv pip install -e ".[web,pty]") plus a POSIX PTY environment such as Linux, macOS, or WSL2. SeeWeb Dashboardfor full documentation.

`hermes serve`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[web]"`
`pty`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[web,pty]"`
[Web Dashboard](/docs/user-guide/features/web-dashboard)

| Option | Default | Description |
| --- | --- | --- |
| --port | 9119 | Port to run the web server on |
| --host | 127.0.0.1 | Bind address |
| --no-open | — | Don't auto-open the browser |
| --insecure | off | Deprecated / no-op.Formerly bypassed auth on a non-loopback bind. Since the June 2026 hardening a public bindalwaysrequires an auth provider (password or OAuth). Bind127.0.0.1and tunnel to keep it local. |
| --skip-build | off | Skip the web UI build step and serve the existingdistdirectly. Useful for non-interactive contexts (Windows Scheduled Tasks, CI) where npm isn't available. Pre-build withcd web && npm run build. |
| --isolated | off | When launched from a named profile (worker dashboard), run a dedicated per-profile server instead of routing to the machine dashboard. |
| --stop | — | Stop runninghermes dashboardprocesses and exit. |
| --status | — | List runninghermes dashboardprocesses and exit. |

`--port`
`9119`
`--host`
`127.0.0.1`
`--no-open`
`--insecure`
`127.0.0.1`
`--skip-build`
`dist`
`cd web && npm run build`
`--isolated`
`worker dashboard`
`--stop`
`hermes dashboard`
`--status`
`hermes dashboard`

### hermes dashboard register​

`hermes dashboard register`

Register this install as a self-hosted dashboard with your Nous Portal account. Creates an OAuth client, writesHERMES_DASHBOARD_OAUTH_CLIENT_IDinto~/.hermes/.env, and prints how to engage the login gate. Requires being logged in (hermes setup).

`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`~/.hermes/.env`
`hermes setup`

| Option | Description |
| --- | --- |
| --name | Human-readable label for the dashboard (default: auto-generated). |
| --redirect-uri | Public HTTPS OAuth redirect URI (e.g.https://hermes.example.com/auth/callback). Omit for localhost-only use. |
| --portal-url | Override the Nous Portal base URL for registration (default: the portal you logged into). Also settable viaHERMES_DASHBOARD_PORTAL_URL. |

`--name`
`--redirect-uri`
`https://hermes.example.com/auth/callback`
`--portal-url`
`HERMES_DASHBOARD_PORTAL_URL`

```
# Default — opens browser to http://127.0.0.1:9119hermes dashboard# Custom port, no browserhermes dashboard --port 8080 --no-open# From a profile alias — routes to the machine dashboard with the# profile preselected in the sidebar switcher (attach if running)worker dashboard
```

## hermes profile​

`hermes profile`

```
hermes profile <subcommand>
```

Manage profiles — multiple isolated Hermes instances, each with its own config, sessions, skills, and home directory.

| Subcommand | Description |
| --- | --- |
| list | List all profiles. |
| use <name> | Set a sticky default profile. |
| create <name> [--clone] [--clone-all] [--clone-from <source>] [--no-alias] | Create a new profile.--clonecopies config,.env,SOUL.md, and skills from the active profile.--clone-allcopies all state.--clone-fromspecifies a source profile and implies config clone unless paired with--clone-all. |
| delete <name> [-y] | Delete a profile. |
| show <name> | Show profile details (home directory, config, etc.). |
| alias <name> [--remove] [--name NAME] | Manage wrapper scripts for quick profile access. |
| rename <old> <new> | Rename a profile. |
| export <name> [-o FILE] | Export a profile to a.tar.gzarchive (local backup). |
| import <archive> [--name NAME] | Import a profile from a.tar.gzarchive (local restore). |
| install <source> [--name N] [--alias] [--force] [-y] | Install a profile distribution from a git URL or local directory. |
| update <name> [--force-config] [-y] | Re-pull a distribution; preserves user data (memories, sessions, auth). |
| info <name> | Show a profile's distribution manifest (version, requirements, source). |

`list`
`use <name>`
`create <name> [--clone] [--clone-all] [--clone-from <source>] [--no-alias]`
`--clone`
`.env`
`SOUL.md`
`--clone-all`
`--clone-from`
`--clone-all`
`delete <name> [-y]`
`show <name>`
`alias <name> [--remove] [--name NAME]`
`rename <old> <new>`
`export <name> [-o FILE]`
`.tar.gz`
`import <archive> [--name NAME]`
`.tar.gz`
`install <source> [--name N] [--alias] [--force] [-y]`
`update <name> [--force-config] [-y]`
`info <name>`

Examples:

```
hermes profile listhermes profile create work --clonehermes profile use workhermes profile alias work --name h-workhermes profile export work -o work-backup.tar.gzhermes profile import work-backup.tar.gz --name restoredhermes profile install github.com/user/my-distro --aliashermes profile update workhermes -p work chat -q "Hello from work profile"
```

## hermes completion​

`hermes completion`

```
hermes completion [bash|zsh|fish]
```

Print a shell completion script to stdout. Source the output in your shell profile for tab-completion of Hermes commands, subcommands, and profile names.

Examples:

```
# Bashhermes completion bash >> ~/.bashrc# Zshhermes completion zsh >> ~/.zshrc# Fishhermes completion fish > ~/.config/fish/completions/hermes.fish
```

## hermes update​

`hermes update`

```
hermes update [--gateway] [--check] [--no-backup] [--backup] [--yes]
```

Pulls the latesthermes-agentcode and reinstalls dependencies in the managed venv, then re-runs the post-install hooks (MCP servers, skills sync, completion install). Safe to run on a live install. Use--checkto see whether your checkout is behindorigin/mainwithout installing.

`hermes-agent`
`--check`
`origin/main`

hermes updatepulls the configured update branch (default:main). If your checkout is on another branch, Hermes may check out the update branch before pulling. Commit branch work before updating when you want to keep it outside the update autostash flow.

`hermes update`
`main`

| Option | Description |
| --- | --- |
| --gateway | Internal mode used by the messaging/updatecommand. Uses file-based IPC for prompts and progress streaming instead of reading from terminal stdin. Not a gateway restart flag. |
| --check | Check whether an update is available without pulling, installing dependencies, or restarting anything. |
| --no-backup | Skip the pre-update backup for this run, even ifupdates.pre_update_backupis enabled inconfig.yaml. |
| --backup | Create a labeled pre-update snapshot ofHERMES_HOME(config, auth, sessions, skills, pairing data) before pulling. Default isoff— the previous always-backup behavior was adding minutes to every update on large homes. Flip it on permanently viaupdates.pre_update_backup: trueinconfig.yaml. |
| --yes,-y | Assume yes for interactive prompts such as config migration and stash restore. API-key entry is skipped; runhermes config migrateseparately for those. |

`--gateway`
`/update`
`--check`
`--no-backup`
`updates.pre_update_backup`
`config.yaml`
`--backup`
`HERMES_HOME`
`updates.pre_update_backup: true`
`config.yaml`
`--yes`
`-y`
`hermes config migrate`

Additional behavior:

- Gateway restart.After a successful update, Hermes attempts to restart all running gateway profiles automatically so they pick up the new code. Usehermes gateway restartwhen you want to restart a gateway without applying an update.
- Local source changes.For git installs, dirty tracked files and untracked files are auto-stashed before branch checkout or pull (git stash push --include-untracked). Interactive terminal updates ask before restoring the stash. Non-interactive updates restore it by default; setupdates.non_interactive_local_changes: discardonly on managed installs where local source edits should be thrown away after a successful pull. If stash restore conflicts or the pull fails, the stash is left in place for manual recovery.
- npm lockfile churn.Before stashing or switching branches, Hermes makes a best-effort cleanup of trackedpackage-lock.jsondiffs produced by npm install/build steps. Commit or manually stash intentional lockfile edits before runninghermes update.
- Pairing data snapshot.Even when--backupis off,hermes updatetakes a lightweight snapshot of~/.hermes/pairing/and the Feishu comment rules beforegit pull. You can roll it back withhermes backup restore --state pre-updateif a pull rewrites a file you were editing.
- Legacyhermes.servicewarning.If Hermes detects a pre-renamehermes.servicesystemd unit (instead of the currenthermes-gateway.service), it prints a one-time migration hint so you can avoid flap-loop issues.
- Exit codes.0on success,1on pull/install/post-install errors,2on unexpected working-tree changes that blockgit pull.

`hermes gateway restart`
`git stash push --include-untracked`
`updates.non_interactive_local_changes: discard`
`package-lock.json`
`hermes update`
`--backup`
`hermes update`
`~/.hermes/pairing/`
`git pull`
`hermes backup restore --state pre-update`
`hermes.service`
`hermes.service`
`hermes-gateway.service`
`0`
`1`
`2`
`git pull`

## Maintenance commands​

| Command | Description |
| --- | --- |
| hermes version | Print version information. |
| hermes update | Pull latest changes and reinstall dependencies. |
| hermes postinstall | Internal bootstrap. Runs once after the install script provisions Hermes (or afterhermes update) to install non-Python dependencies that pip cannot provide — Node.js runtime, headless browser, ripgrep, ffmpeg — and then triggerhermes setupif the profile has not been configured yet. Safe to re-run idempotently. |
| hermes uninstall [--full] [--gui] [--yes] | Remove Hermes, optionally deleting all config/data.--guiremoves only the desktop Chat GUI, leaving the agent intact;--fullalso deletes config/data;--yesskips prompts. |

`hermes version`
`hermes update`
`hermes postinstall`
`hermes update`
`hermes setup`
`hermes uninstall [--full] [--gui] [--yes]`
`--gui`
`--full`
`--yes`

## See also​

- Slash Commands Reference
- CLI Interface
- Sessions
- Skills System
- Skins & Themes

[Slash Commands Reference](/docs/reference/slash-commands)
[CLI Interface](/docs/user-guide/cli)
[Sessions](/docs/user-guide/sessions)
[Skills System](/docs/user-guide/features/skills)
[Skins & Themes](/docs/user-guide/features/skins)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/reference/cli-commands.md)