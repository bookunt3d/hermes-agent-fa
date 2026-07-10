---
layout: docs
title: "پیکربندی مدل‌ها"
permalink: /user-guide/configuring-models/
---

- 
- Using Hermes
- Configuring Models

# Configuring Models

Hermes uses two kinds of model slots:

- Main model— what the agent thinks with. Every user message, every tool-call loop, every streamed response goes through this model.
- Auxiliary models— smaller side-jobs the agent offloads. Context compression, vision (image analysis), web-page summarization, approval scoring, MCP tool routing, session-title generation, and skill search. Each has its own slot and can be overridden independently.

This page covers configuring both from the dashboard. If you prefer config files or the CLI, jump toAlternative methodsat the bottom.

Nous Portalprovides 300+ models under one subscription. On a fresh install, runhermes setup --portalto log in and set Nous as your provider in one command. Inspect what's wired up withhermes portal info.

[Nous Portal](/docs/user-guide/features/tool-gateway)
`hermes setup --portal`
`hermes portal info`
- Portal subscribers also get10% off token-billed providers.

`model:`

On a brand-new install the bundled default config hasmodel: ""(an empty string sentinel meaning "not configured yet"). The first time you runhermes setuporhermes model, that key is upgraded in-place to a mapping withprovider,default,base_url, andapi_modesub-keys — the shape shown throughout this page and inprofiles.md/configuration.md. If you ever see an empty string inconfig.yaml, runhermes model(or clickChangein the dashboard) and Hermes will write the dict form for you.

`model: ""`
`hermes setup`
`hermes model`
`provider`
`default`
`base_url`
`api_mode`
[profiles.md](/docs/user-guide/profiles)
`profiles.md`
[configuration.md](/docs/user-guide/configuration)
`configuration.md`
`config.yaml`
`hermes model`

## The Models page​

Open the dashboard and clickModelsin the sidebar. You get two sections:

1. Model Settings— the top panel, where you assign models to slots.
2. Usage analytics— ranked cards showing every model that ran a session in the selected period, with token counts, cost, and capability badges.

The top card is theModel Settingspanel. The main row always shows what the agent will spin up for new sessions. ClickChangeto open the picker.

## Setting the main model​

ClickChangeon the Main model row:

The picker has two columns:

- Left— authenticated providers. Only providers you've set up (API key set, OAuth'd, or defined as a custom endpoint) show up here. If a provider is missing, head toKeysand add its credential.
- Right— the curated model list for the selected provider. These are the agentic models Hermes recommends for that provider, not the raw/modelsdump (which on OpenRouter includes 400+ models including TTS, image generators, and rerankers).

`/models`

Type in the filter box to narrow by provider name, slug, or model ID.

Pick a model, hitSwitch, and Hermes writes it to~/.hermes/config.yamlunder themodelsection.This applies to new sessions only— any chat tab you already have open keeps running whatever model it started with. To hot-swap the current chat, use the/modelslash command inside it.

`~/.hermes/config.yaml`
`model`
`/model`

### Mid-session switches and context warnings​

When you switch modelsinside an active session(Herm TUI model picker,hermesCLI, or/modelon Telegram/Discord), Hermes estimates whether yournext messagewill runpreflight context compressionagainst the new model's window. If the session is already near or above that model's compression threshold (seeContext Compression), the switch reply includes a warning — the samewarning_messagepath used for expensive-model notices. The switch still applies immediately; compression runs on thefirst user message after the switch, before the model answers.

`hermes`
`/model`
[Context Compression](/docs/user-guide/configuration#context-compression)
`warning_message`

Prompt caches are keyed to the model serving the request, so any mid-conversation model change — an explicit/modelswitch, anautomatic fallback, or acredential-poolrotation onto a different account — means the next message re-reads the entire conversation at full input-token price instead of the cached (~75–90% discounted) rate. On a long session this one-time re-read can dwarf the per-token difference between the two models. Switch when you need to, but prefer doing it early in a conversation or right after starting a fresh session.

`/model`
[automatic fallback](/docs/user-guide/features/fallback-providers)
[credential-pool](/docs/user-guide/features/credential-pools)

## Setting auxiliary models​

ClickShow auxiliaryto reveal the 11 task slots:

Every auxiliary task defaults toauto— meaning Hermes tries your main model for that job too. If that route is unavailable or hits a capacity-style failure,autofollows any task-specificauxiliary.<task>.fallback_chain, then the mainfallback_providers/fallback_modelchain, then Hermes' built-in auxiliary discovery chain. Override a specific task when you want a cheaper or faster model for a side-job.

`auto`
`auto`
`auxiliary.<task>.fallback_chain`
`fallback_providers`
`fallback_model`

### Common override patterns​

| Task | When to override |
| --- | --- |
| Title Gen | Almost always. A $0.10/M flash model writes session titles as well as Opus. Default config sets this togoogle/gemini-3-flash-previewon OpenRouter. |
| Vision | When your main model lacks vision support. Point it atgoogle/gemini-2.5-flashorgpt-4o-mini. |
| Compression | When you're burning reasoning tokens on Opus/M2.7 just to summarize context. A fast chat model does the job at 1/50th the cost. |
| Approval | Forapproval_mode: smart— a fast/cheap model (haiku, flash, gpt-5-mini) decides whether to auto-approve low-risk commands. Expensive models here are waste. |
| Web Extract | When you useweb_extractheavily. Same logic as compression — summarization doesn't need reasoning. |
| Skills Hub | hermes skills searchuses this. Usually fine atauto. |
| MCP | MCP tool routing. Usually fine atauto. |
| Triage Specifier | Routes the Kanban triage specifier (hermes kanban specify) that expands a rough one-liner into a concrete spec. A cheap, capable model works well. |
| Kanban Decomposer | Routes Kanban task decomposition — splits a triage task into a graph of child tasks for specialist profiles. |
| Profile Describer | Routes profile-description generation (hermes profile describe --auto/ the dashboard auto-generate button). Short, cheap call. |
| Curator | Routes the curator skill-usage review pass. Can run for minutes on reasoning models, so a cheaper aux model is often worthwhile. |

`google/gemini-3-flash-preview`
`google/gemini-2.5-flash`
`gpt-4o-mini`
`approval_mode: smart`
`web_extract`
`hermes skills search`
`auto`
`auto`
`hermes kanban specify`
`hermes profile describe --auto`

### Per-task override​

ClickChangeon any auxiliary row. Same picker opens, same behavior — pick provider + model, hit Switch. The row updates to showprovider · modelinstead ofauto (use main model).

`provider · model`
`auto (use main model)`

### Reset all to auto​

If you've over-tuned and want to start over, clickReset all to autoat the top of the auxiliary section. Every slot goes back to using your main model.

## The "Use as" shortcut​

Every model card on the page has aUse asdropdown. This is the fast path — pick a model you see in your analytics, clickUse as, and assign it to the main slot or any specific auxiliary task in one click:

The dropdown has:

- Main model— same as clicking Change on the main row.
- All auxiliary tasks— assigns this model to all 11 aux slots at once. Useful when you just want every side-job on a cheap flash model.
- Individual task options— Vision, Web Extract, Compression, etc. The currently-assigned model for each task is markedcurrent.

`current`

Cards are badged withmainoraux · <task>when they're currently assigned to something — so you can see at a glance which of your historical models are wired in where.

`main`
`aux · <task>`

## What gets written toconfig.yaml​

`config.yaml`

When you save via the dashboard, Hermes writes to~/.hermes/config.yaml:

`~/.hermes/config.yaml`

Main model:

```
model:  provider: openrouter  default: anthropic/claude-opus-4.7  base_url: ''        # cleared on provider switch  api_mode: chat_completions
```

Auxiliary override (example — vision on gemini-flash):

```
auxiliary:  vision:    provider: openrouter    model: google/gemini-2.5-flash    base_url: ''    api_key: ''    timeout: 120    extra_body: {}    download_timeout: 30
```

Auxiliary on auto (default):

```
auxiliary:  compression:    provider: auto    model: ''    base_url: ''    # ... other fields unchanged
```

provider: autowithmodel: ''tells Hermes to use the main model for that task, while still honoring fallback policy if the main route cannot serve the auxiliary call.

`provider: auto`
`model: ''`

Optional task-specific fallback chains live under the same auxiliary task:

```
auxiliary:  title_generation:    provider: auto    model: ''    fallback_chain:      - provider: openrouter        model: inclusionai/ring-2.6-1t:free
```

Whenfallback_chainis absent,autouses the top-levelfallback_providerschain before the built-in auxiliary discovery chain.

`fallback_chain`
`auto`
`fallback_providers`

## When does it take effect?​

- CLI(hermes chat): nexthermes chatinvocation.
- Gateway(Telegram, Discord, Slack, etc.): nextnewsession. Existing sessions keep their model. Restart the gateway (hermes gateway restart) if you want to force all sessions to pick up the change.
- Dashboard chat tab(/chat): next new PTY. The currently-open chat keeps its model — use/modelinside it to hot-swap.

`hermes chat`
`hermes chat`
`hermes gateway restart`
`/chat`
`/model`

Changes never invalidate prompt caches on running sessions. That's deliberate: swapping the main model inside a session requires a cache reset (the system prompt contains model-specific content), and we reserve that for the explicit/modelslash command inside chat.

`/model`

## Troubleshooting​

### "No authenticated providers" in the picker​

Hermes lists a provider only if it has a working credential. CheckKeysin the sidebar — you should see one of: an API key, a successful OAuth, or a custom endpoint URL. If the provider you want isn't there, runhermes setupto wire it up, or go toKeysand add the env var.

`hermes setup`

### Main model didn't change in my running chat​

Expected. The dashboard writesconfig.yaml, which new sessions read. The currently-open chat is a live agent process — it keeps whatever model it was spawned with. Use/model <name>inside the chat to hot-swap that specific session.

`config.yaml`
`/model <name>`

### Auxiliary override "didn't take effect"​

Three things to check:

1. Did you start a new session?Existing chats don't re-read config.
2. Isproviderset to something other thanauto?If the field showsauto, the task is still using your main model. ClickChangeand pick a real provider.
3. Is the provider authenticated?If you assignedminimaxto a task but don't have a MiniMax API key, that task falls back to the openrouter default and logs a warning inagent.log.

`provider`
`auto`
`auto`
`minimax`
`agent.log`

### I picked a model but Hermes switched providers on me​

On OpenRouter (or any aggregator), bare model names resolvewithinthe aggregator first. Soclaude-sonnet-4on OpenRouter becomesanthropic/claude-sonnet-4.6, staying on your OpenRouter auth. But if you typedclaude-sonnet-4on a native Anthropic auth, it would stay asclaude-sonnet-4-6. If you see an unexpected provider switch, check that your current provider is what you expect — the picker always shows the current main at the top of the dialog.

`claude-sonnet-4`
`anthropic/claude-sonnet-4.6`
`claude-sonnet-4`
`claude-sonnet-4-6`

## Alternative methods​

### CLI slash command​

Inside anyhermes chatsession:

`hermes chat`

```
/model gpt-5.4 --provider openrouter             # session-only/model gpt-5.4 --provider openrouter --global    # also persists to config.yaml
```

--globaldoes the same thing the dashboard'sChangebutton does, plus it switches the running session in-place.

`--global`

### Custom aliases​

Define your own short names for models you reach for often, then use/model <alias>in the CLI or any messaging platform. There are two equivalent formats — pick whichever fits your workflow.

`/model <alias>`

Canonical (top-levelmodel_aliases:)— full control over provider + base_url:

`model_aliases:`

```
# ~/.hermes/config.yamlmodel_aliases:  fav:    model: claude-sonnet-4.6    provider: anthropic  grok:    model: grok-4    provider: x-ai
```

Short string form (model.aliases.<name>: provider/model)— convenient from the shell becausehermes config setonly writes scalar values, but it can't carry a custombase_url:

`model.aliases.<name>: provider/model`
`hermes config set`
`base_url`

```
hermes config set model.aliases.fav anthropic/claude-opus-4.6hermes config set model.aliases.grok x-ai/grok-4
```

Both paths feed the same loader (hermes_cli/model_switch.py). Entries declared inmodel_aliases:take precedence overmodel.aliases:entries with the same name.

`hermes_cli/model_switch.py`
`model_aliases:`
`model.aliases:`

Then/model favor/model grokin chat. User aliases shadow built-in short names (sonnet,kimi,opus, etc.). SeeCustom model aliasesfor the full reference.

`/model fav`
`/model grok`
`sonnet`
`kimi`
`opus`
[Custom model aliases](/docs/reference/slash-commands#custom-model-aliases)

### hermes modelsubcommand​

`hermes model`

```
hermes model            # Interactive provider + model picker (the canonical way to switch defaults)
```

hermes modelwalks you through picking a provider, authenticating (OAuth flows open a browser; API-key providers prompt for the key), and then choosing a specific model from that provider's curated catalog. The choice is written tomodel.providerandmodel.modelin~/.hermes/config.yaml.

`hermes model`
`model.provider`
`model.model`
`~/.hermes/config.yaml`

To list providers/models without launching the picker, use the dashboard or the REST endpoints below. To inspect what the CLI will actually use right now:hermes config show | grep '^model\.'andhermes status.

`hermes config show | grep '^model\.'`
`hermes status`

### Direct config edit​

Edit~/.hermes/config.yamland restart whatever reads it. See theConfiguration referencefor the full schema.

`~/.hermes/config.yaml`
[Configuration reference](/docs/user-guide/configuration)

### REST API​

The dashboard uses three endpoints. Useful for scripting:

```
# List authenticated providers + curated model listscurl -H "X-Hermes-Session-Token: $TOKEN" http://localhost:PORT/api/model/options# Read current main + auxiliary assignmentscurl -H "X-Hermes-Session-Token: $TOKEN" http://localhost:PORT/api/model/auxiliary# Set the main modelcurl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \  -d '{"scope":"main","provider":"openrouter","model":"anthropic/claude-opus-4.7"}' \  http://localhost:PORT/api/model/set# Override a single auxiliary taskcurl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \  -d '{"scope":"auxiliary","task":"vision","provider":"openrouter","model":"google/gemini-2.5-flash"}' \  http://localhost:PORT/api/model/set# Assign one model to every auxiliary taskcurl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \  -d '{"scope":"auxiliary","task":"","provider":"openrouter","model":"google/gemini-2.5-flash"}' \  http://localhost:PORT/api/model/set# Reset all auxiliary tasks to autocurl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \  -d '{"scope":"auxiliary","task":"__reset__","provider":"","model":""}' \  http://localhost:PORT/api/model/set
```

The session token is injected into the dashboard HTML at startup and rotates on every server restart. Grab it from the browser devtools (window.__HERMES_SESSION_TOKEN__) if you're scripting against a running dashboard.

`window.__HERMES_SESSION_TOKEN__`
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/configuring-models.md)