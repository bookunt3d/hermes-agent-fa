---
layout: docs
title: "Features_Plugins"
permalink: /docs/user-guide/features_plugins/
---

- 
- Features
- Core
- Plugins

# Plugins

Hermes has a plugin system for adding custom tools, hooks, and integrations without modifying core code.

If you want to create a custom tool for yourself, your team, or one project,
this is usually the right path. The developer guide'sAdding Toolspage is for built-in Hermes
core tools that live intools/andtoolsets.py.

`tools/`
`toolsets.py`

→Build a Hermes Plugin— step-by-step guide with a complete working example.

## Quick overview​

Drop a directory into~/.hermes/plugins/with aplugin.yamland Python code:

`~/.hermes/plugins/`
`plugin.yaml`

```
~/.hermes/plugins/my-plugin/├── plugin.yaml      # manifest├── __init__.py      # register() — wires schemas to handlers├── schemas.py       # tool schemas (what the LLM sees)└── tools.py         # tool handlers (what runs when called)
```

Start Hermes — your tools appear alongside built-in tools. The model can call them immediately.

### Minimal working example​

Here is a complete plugin that adds ahello_worldtool and logs every tool call via a hook.

`hello_world`

~/.hermes/plugins/hello-world/plugin.yaml

`~/.hermes/plugins/hello-world/plugin.yaml`

```
name: hello-worldversion: "1.0"description: A minimal example plugin
```

~/.hermes/plugins/hello-world/__init__.py

`~/.hermes/plugins/hello-world/__init__.py`

```
"""Minimal Hermes plugin — registers a tool and a hook."""import jsondef register(ctx):    # --- Tool: hello_world ---    schema = {        "name": "hello_world",        "description": "Returns a friendly greeting for the given name.",        "parameters": {            "type": "object",            "properties": {                "name": {                    "type": "string",                    "description": "Name to greet",                }            },            "required": ["name"],        },    }    def handle_hello(params, **kwargs):        del kwargs        name = params.get("name", "World")        return json.dumps({"success": True, "greeting": f"Hello, {name}!"})    ctx.register_tool(        name="hello_world",        toolset="hello_world",        schema=schema,        handler=handle_hello,        description="Return a friendly greeting for the given name.",    )    # --- Hook: log every tool call ---    def on_tool_call(tool_name, params, result):        print(f"[hello-world] tool called: {tool_name}")    ctx.register_hook("post_tool_call", on_tool_call)
```

Drop both files into~/.hermes/plugins/hello-world/, restart Hermes, and the model can immediately callhello_world. The hook prints a log line after every tool invocation.

`~/.hermes/plugins/hello-world/`
`hello_world`

Project-local plugins under./.hermes/plugins/are disabled by default. Enable them only for trusted repositories by settingHERMES_ENABLE_PROJECT_PLUGINS=truebefore starting Hermes.

`./.hermes/plugins/`
`HERMES_ENABLE_PROJECT_PLUGINS=true`

## What plugins can do​

Everyctx.*API below is available inside a plugin'sregister(ctx)function.

`ctx.*`
`register(ctx)`
| Capability | How |
| --- | --- |
| Add tools | ctx.register_tool(name=..., toolset=..., schema=..., handler=...) |
| Add hooks | ctx.register_hook("post_tool_call", callback) |
| Add slash commands | ctx.register_command(name, handler, description)— adds/namein CLI and gateway sessions |
| Dispatch tools from commands | ctx.dispatch_tool(name, args)— invokes a registered tool with parent-agent context auto-wired |
| Add CLI commands | ctx.register_cli_command(name, help, setup_fn, handler_fn)— addshermes <plugin> <subcommand> |
| Inject messages | ctx.inject_message(content, role="user")— seeInjecting Messages |
| Ship data files | Path(__file__).parent / "data" / "file.yaml" |
| Bundle skills | ctx.register_skill(name, path)— namespaced asplugin:skill, loaded viaskill_view("plugin:skill") |
| Gate on env vars | requires_env: [API_KEY]in plugin.yaml — prompted duringhermes plugins install |
| Distribute via pip | [project.entry-points."hermes_agent.plugins"] |
| Register a gateway platform (Discord, Telegram, IRC, …) | ctx.register_platform(name, label, adapter_factory, check_fn, ...)— seeAdding Platform Adapters |
| Register an image-generation backend | ctx.register_image_gen_provider(provider)— seeImage Generation Provider Plugins |
| Register a video-generation backend | ctx.register_video_gen_provider(provider)— seeVideo Generation Provider Plugins |
| Register a context-compression engine | ctx.register_context_engine(engine)— seeContext Engine Plugins |
| Register a memory backend | SubclassMemoryProviderinplugins/memory/<name>/__init__.py— seeMemory Provider Plugins(uses a separate discovery system) |
| Run a host-owned LLM call | ctx.llm.complete(...)/ctx.llm.complete_structured(...)— borrow the user's active model + auth for a one-shot completion with optional JSON schema validation. SeePlugin LLM Access |
| Register an inference backend (LLM provider) | register_provider(ProviderProfile(...))inplugins/model-providers/<name>/__init__.py— seeModel Provider Plugins(uses a separate discovery system) |

`ctx.register_tool(name=..., toolset=..., schema=..., handler=...)`
`ctx.register_hook("post_tool_call", callback)`
`ctx.register_command(name, handler, description)`
`/name`
`ctx.dispatch_tool(name, args)`
`ctx.register_cli_command(name, help, setup_fn, handler_fn)`
`hermes <plugin> <subcommand>`
`ctx.inject_message(content, role="user")`
`Path(__file__).parent / "data" / "file.yaml"`
`ctx.register_skill(name, path)`
`plugin:skill`
`skill_view("plugin:skill")`
`requires_env: [API_KEY]`
`hermes plugins install`
`[project.entry-points."hermes_agent.plugins"]`
`ctx.register_platform(name, label, adapter_factory, check_fn, ...)`
`ctx.register_image_gen_provider(provider)`
`ctx.register_video_gen_provider(provider)`
`ctx.register_context_engine(engine)`
`MemoryProvider`
`plugins/memory/<name>/__init__.py`
`ctx.llm.complete(...)`
`ctx.llm.complete_structured(...)`
`register_provider(ProviderProfile(...))`
`plugins/model-providers/<name>/__init__.py`

## Plugin discovery​

| Source | Path | Use case |
| --- | --- | --- |
| Bundled | <repo>/plugins/ | Ships with Hermes — seeBuilt-in Plugins |
| User | ~/.hermes/plugins/ | Personal plugins |
| Project | .hermes/plugins/ | Project-specific plugins (requiresHERMES_ENABLE_PROJECT_PLUGINS=true) |
| pip | hermes_agent.pluginsentry_points | Distributed packages |
| Nix | services.hermes-agent.extraPlugins/extraPythonPackages | NixOS declarative installs — seeNix Setup |

`<repo>/plugins/`
`~/.hermes/plugins/`
`.hermes/plugins/`
`HERMES_ENABLE_PROJECT_PLUGINS=true`
`hermes_agent.plugins`
`services.hermes-agent.extraPlugins`
`extraPythonPackages`

Later sources override earlier ones on name collision, so a user plugin with the same name as a bundled plugin replaces it.

### Plugin sub-categories​

Within each source, Hermes also recognizes sub-category directories that route plugins to specialized discovery systems:

| Sub-directory | What it holds | Discovery system |
| --- | --- | --- |
| plugins/(root) | General plugins — tools, hooks, slash commands, CLI commands, bundled skills | PluginManager(kind:standaloneorbackend) |
| plugins/platforms/<name>/ | Gateway channel adapters (ctx.register_platform()) | PluginManager(kind:platform, one level deeper) |
| plugins/image_gen/<name>/ | Image-generation backends (ctx.register_image_gen_provider()) | PluginManager(kind:backend, one level deeper) |
| plugins/memory/<name>/ | Memory providers (subclassMemoryProvider) | Own loaderinplugins/memory/__init__.py(kind:exclusive— one active at a time) |
| plugins/context_engine/<name>/ | Context-compression engines (ctx.register_context_engine()) | Own loaderinplugins/context_engine/__init__.py(one active at a time) |
| plugins/model-providers/<name>/ | LLM provider profiles (register_provider(ProviderProfile(...))) | Own loaderinproviders/__init__.py(lazily scanned on firstget_provider_profile()call) |

`plugins/`
`PluginManager`
`standalone`
`backend`
`plugins/platforms/<name>/`
`ctx.register_platform()`
`PluginManager`
`platform`
`plugins/image_gen/<name>/`
`ctx.register_image_gen_provider()`
`PluginManager`
`backend`
`plugins/memory/<name>/`
`MemoryProvider`
`plugins/memory/__init__.py`
`exclusive`
`plugins/context_engine/<name>/`
`ctx.register_context_engine()`
`plugins/context_engine/__init__.py`
`plugins/model-providers/<name>/`
`register_provider(ProviderProfile(...))`
`providers/__init__.py`
`get_provider_profile()`

User plugins at~/.hermes/plugins/model-providers/<name>/and~/.hermes/plugins/memory/<name>/override bundled plugins of the same name — last-writer-wins inregister_provider()/register_memory_provider(). Drop a directory in, and it replaces the built-in without any repo edits.

`~/.hermes/plugins/model-providers/<name>/`
`~/.hermes/plugins/memory/<name>/`
`register_provider()`
`register_memory_provider()`

## Plugins are opt-in (with a few exceptions)​

General plugins and user-installed backends are disabled by default— discovery finds them (so they show up inhermes pluginsand/plugins), but nothing with hooks or tools loads until you add the plugin's name toplugins.enabledin~/.hermes/config.yaml. This stops third-party code from running without your explicit consent.

`hermes plugins`
`/plugins`
`plugins.enabled`
`~/.hermes/config.yaml`

```
plugins:  enabled:    - my-tool-plugin    - disk-cleanup  disabled:       # optional deny-list — always wins if a name appears in both    - noisy-plugin
```

Three ways to flip state:

```
hermes plugins                    # interactive toggle (space to check/uncheck)hermes plugins enable <name>      # add to allow-listhermes plugins disable <name>     # remove from allow-list + add to disabled
```

Afterhermes plugins install owner/repo, you're askedEnable 'name' now? [y/N]— defaults to no. Skip the prompt for scripted installs with--enableor--no-enable.

`hermes plugins install owner/repo`
`Enable 'name' now? [y/N]`
`--enable`
`--no-enable`

### What the allow-list does NOT gate​

Several categories of plugin bypassplugins.enabled— they're part of Hermes' built-in surface and would break basic functionality if gated off by default:

`plugins.enabled`
| Plugin kind | How it's activated instead |
| --- | --- |
| Bundled platform plugins(IRC, Teams, etc. underplugins/platforms/) | Auto-loaded so every shipped gateway channel is available. The actual channel turns on viagateway.platforms.<name>.enabledinconfig.yaml. |
| Bundled backends(image-gen providers underplugins/image_gen/, etc.) | Auto-loaded so the default backend "just works". Selection happens via<category>.providerinconfig.yaml(e.g.image_gen.provider: openai). |
| Memory providers(plugins/memory/) | All discovered; exactly one is active, chosen bymemory.providerinconfig.yaml. |
| Context engines(plugins/context_engine/) | All discovered; one is active, chosen bycontext.engineinconfig.yaml. |
| Model providers(plugins/model-providers/) | All bundled providers underplugins/model-providers/discover and register at the firstget_provider_profile()call. The user picks one at a time via--providerorconfig.yaml. |
| Pip-installedbackendplugins | Opt-in viaplugins.enabled(same as general plugins). |
| User-installed platforms(under~/.hermes/plugins/platforms/) | Opt-in viaplugins.enabled— third-party gateway adapters need explicit consent. |

`plugins/platforms/`
`gateway.platforms.<name>.enabled`
`config.yaml`
`plugins/image_gen/`
`<category>.provider`
`config.yaml`
`image_gen.provider: openai`
`plugins/memory/`
`memory.provider`
`config.yaml`
`plugins/context_engine/`
`context.engine`
`config.yaml`
`plugins/model-providers/`
`plugins/model-providers/`
`get_provider_profile()`
`--provider`
`config.yaml`
`backend`
`plugins.enabled`
`~/.hermes/plugins/platforms/`
`plugins.enabled`

In short:bundled "always-works" infrastructure loads automatically; third-party general plugins are opt-in.Theplugins.enabledallow-list is the gate specifically for arbitrary code a user drops into~/.hermes/plugins/.

`plugins.enabled`
`~/.hermes/plugins/`

### Migration for existing users​

When you upgrade to a version of Hermes that has opt-in plugins (config schema v21+), any user plugins already installed under~/.hermes/plugins/that weren't already inplugins.disabledareautomatically grandfatheredintoplugins.enabled. Your existing setup keeps working. Bundled standalone plugins are NOT grandfathered — even existing users have to opt in explicitly. (Bundled platform/backend plugins never needed grandfathering because they were never gated.)

`~/.hermes/plugins/`
`plugins.disabled`
`plugins.enabled`

## Available hooks​

Plugins can register callbacks for these lifecycle events. See theEvent Hooks pagefor full details, callback signatures, and examples.

| Hook | Fires when |
| --- | --- |
| pre_tool_call | Before any tool executes |
| post_tool_call | After any tool returns |
| pre_llm_call | Once per turn, before the LLM loop — can return{"context": "..."}toinject context into the user message |
| post_llm_call | Once per turn, after the LLM loop (successful turns only) |
| on_session_start | New session created (first turn only) |
| on_session_end | End of everyrun_conversationcall + CLI exit handler |
| on_session_finalize | CLI/gateway tears down an active session (/new, GC, CLI quit) |
| on_session_reset | Gateway swaps in a new session key (/new,/reset,/clear, idle rotation) |
| subagent_stop | Once per child afterdelegate_taskfinishes |
| pre_gateway_dispatch | Gateway received a user message, before auth + dispatch. Return{"action": "skip" | "rewrite" | "allow", ...}to influence flow. |

`pre_tool_call`
`post_tool_call`
`pre_llm_call`
`{"context": "..."}`
`post_llm_call`
`on_session_start`
`on_session_end`
`run_conversation`
`on_session_finalize`
`/new`
`on_session_reset`
`/new`
`/reset`
`/clear`
`subagent_stop`
`delegate_task`
`pre_gateway_dispatch`
`{"action": "skip" | "rewrite" | "allow", ...}`

## Plugin types​

Hermes has four kinds of plugins:

| Type | What it does | Selection | Location |
| --- | --- | --- | --- |
| General plugins | Add tools, hooks, slash commands, CLI commands | Multi-select (enable/disable) | ~/.hermes/plugins/ |
| Memory providers | Replace or augment built-in memory | Single-select (one active) | plugins/memory/ |
| Context engines | Replace the built-in context compressor | Single-select (one active) | plugins/context_engine/ |
| Model providers | Declare an inference backend (OpenRouter, Anthropic, …) | Multi-register, picked by--provider/config.yaml | plugins/model-providers/ |

`~/.hermes/plugins/`
`plugins/memory/`
`plugins/context_engine/`
`--provider`
`config.yaml`
`plugins/model-providers/`

Memory providers and context engines areprovider plugins— only one of each type can be active at a time. Model providers are also plugins, but many load simultaneously; the user picks one at a time via--providerorconfig.yaml. General plugins can be enabled in any combination.

`--provider`
`config.yaml`

## Pluggable interfaces — where to go for each​

The table above shows the four plugin categories, but within "General plugins" thePluginContextexposes several distinct extension points — and Hermes also accepts extensions outside the Python plugin system (config-driven backends, shell-hooked commands, external servers, etc.). Use this table to find the right doc for what you want to build:

`PluginContext`
| Want to add… | How | Authoring guide |
| --- | --- | --- |
| Atoolthe LLM can call | Python plugin —ctx.register_tool() | Build a Hermes Plugin·Adding Tools |
| Alifecycle hook(pre/post LLM, session start/end, tool filter) | Python plugin —ctx.register_hook() | Hooks reference·Build a Hermes Plugin |
| Aslash commandfor the CLI / gateway | Python plugin —ctx.register_command() | Build a Hermes Plugin·Extending the CLI |
| Asubcommandforhermes <thing> | Python plugin —ctx.register_cli_command() | Extending the CLI |
| A bundledskillthat your plugin ships | Python plugin —ctx.register_skill() | Creating Skills |
| Aninference backend(LLM provider: OpenAI-compat, Codex, Anthropic-Messages, Bedrock) | Provider plugin —register_provider(ProviderProfile(...))inplugins/model-providers/<name>/ | Model Provider Plugins·Adding Providers |
| Agateway channel(Discord / Telegram / IRC / Teams / etc.) | Platform plugin —ctx.register_platform()inplugins/platforms/<name>/ | Adding Platform Adapters |
| Amemory backend(Honcho, Mem0, Supermemory, …) | Memory plugin — subclassMemoryProviderinplugins/memory/<name>/ | Memory Provider Plugins |
| Acontext-compression strategy | Context-engine plugin —ctx.register_context_engine() | Context Engine Plugins |
| Animage-generation backend(DALL·E, SDXL, …) | Backend plugin —ctx.register_image_gen_provider() | Image Generation Provider Plugins |
| Avideo-generation backend(Veo, Kling, Pixverse, Grok-Imagine, Runway, …) | Backend plugin —ctx.register_video_gen_provider() | Video Generation Provider Plugins |
| ATTS backend(any CLI — Piper, VoxCPM, Kokoro, xtts, voice-cloning scripts, …) | Config-driven (recommended) — declare undertts.providers.<name>withtype: commandinconfig.yaml. OR Python backend plugin —ctx.register_tts_provider()for Python-SDK / streaming engines that need more than a shell template. | TTS Setup·Python plugin guide |
| AnSTT backend(any CLI — whisper.cpp, custom whisper binary, local ASR CLI) | Config-driven (recommended) — declare understt.providers.<name>withtype: commandinconfig.yaml, or setHERMES_LOCAL_STT_COMMANDfor the legacy single-command escape hatch. OR Python backend plugin —ctx.register_transcription_provider()for Python-SDK engines (OpenRouter, SenseAudio, Gemini-STT, etc.). | STT Setup·Python plugin guide |
| External tools via MCP(filesystem, GitHub, Linear, Notion, any MCP server) | Config-driven — declaremcp_servers.<name>withcommand:/url:inconfig.yaml. Hermes auto-discovers the server's tools and registers them alongside built-ins. | MCP |
| Additional skill sources(custom GitHub repos, private skill indexes) | CLI —hermes skills tap add <repo> | Skills Hub·Publishing a custom tap |
| Gateway event hooks(fire ongateway:startup,session:start,agent:end,command:*) | DropHOOK.yaml+handler.pyinto~/.hermes/hooks/<name>/ | Event Hooks |
| Shell hooks(run a shell command on events — notifications, audit logs, desktop alerts) | Config-driven — declare underhooks:inconfig.yaml | Shell Hooks |

`ctx.register_tool()`
`ctx.register_hook()`
`ctx.register_command()`
`hermes <thing>`
`ctx.register_cli_command()`
`ctx.register_skill()`
`register_provider(ProviderProfile(...))`
`plugins/model-providers/<name>/`
`ctx.register_platform()`
`plugins/platforms/<name>/`
`MemoryProvider`
`plugins/memory/<name>/`
`ctx.register_context_engine()`
`ctx.register_image_gen_provider()`
`ctx.register_video_gen_provider()`
`tts.providers.<name>`
`type: command`
`config.yaml`
`ctx.register_tts_provider()`
`stt.providers.<name>`
`type: command`
`config.yaml`
`HERMES_LOCAL_STT_COMMAND`
`ctx.register_transcription_provider()`
`mcp_servers.<name>`
`command:`
`url:`
`config.yaml`
`hermes skills tap add <repo>`
`gateway:startup`
`session:start`
`agent:end`
`command:*`
`HOOK.yaml`
`handler.py`
`~/.hermes/hooks/<name>/`
`hooks:`
`config.yaml`

Not everything is a Python plugin. Some extension surfaces intentionally useconfig-driven shell commands(TTS, STT, shell hooks) so any CLI you already have becomes a plugin without writing Python. Others areexternal servers(MCP) the agent connects to and auto-registers tools from. And some aredrop-in directories(gateway hooks) with their own manifest format. Pick the right surface for the integration style that fits your use case; the authoring guides in the table above each cover placeholders, discovery, and examples.

## NixOS declarative plugins​

On NixOS, plugins can be installed declaratively via the module options — nohermes plugins installneeded. See theNix Setup guidefor full details.

`hermes plugins install`

```
services.hermes-agent = {  # Directory plugin (source tree with plugin.yaml)  extraPlugins = [ (pkgs.fetchFromGitHub { ... }) ];  # Entry-point plugin (pip package)  extraPythonPackages = [ (pkgs.python312Packages.buildPythonPackage { ... }) ];  # Enable in config  settings.plugins.enabled = [ "my-plugin" ];};
```

Declarative plugins are symlinked with anix-managed-prefix — they coexist with manually installed plugins and are cleaned up automatically when removed from the Nix config.

`nix-managed-`

## Managing plugins​

```
hermes plugins                               # unified interactive UIhermes plugins list                          # table: enabled / disabled / not enabledhermes plugins install user/repo             # install from Git, then prompt Enable? [y/N]hermes plugins install user/repo --enable    # install AND enable (no prompt)hermes plugins install user/repo --no-enable # install but leave disabled (no prompt)hermes plugins update my-plugin              # pull latesthermes plugins remove my-plugin              # uninstallhermes plugins enable my-plugin              # add to allow-listhermes plugins disable my-plugin             # remove from allow-list + add to disabled
```

### Interactive UI​

Runninghermes pluginswith no arguments opens a composite interactive screen:

`hermes plugins`

```
Plugins  ↑↓ navigate  SPACE toggle  ENTER configure/confirm  ESC done  General Plugins → [✓] my-tool-plugin — Custom search tool   [ ] webhook-notifier — Event hooks   [ ] disk-cleanup — Auto-cleanup of ephemeral files [bundled]  Provider Plugins     Memory Provider          ▸ honcho     Context Engine           ▸ compressor
```

- General Plugins section— checkboxes, toggle with SPACE. Checked = inplugins.enabled, unchecked = inplugins.disabled(explicit off).
- Provider Plugins section— shows current selection. Press ENTER to drill into a radio picker where you choose one active provider.
- Bundled plugins appear in the same list with a[bundled]tag.

`plugins.enabled`
`plugins.disabled`
`[bundled]`

Provider plugin selections are saved toconfig.yaml:

`config.yaml`

```
memory:  provider: "honcho"      # empty string = built-in onlycontext:  engine: "compressor"    # default built-in compressor
```

### Enabled vs. disabled vs. neither​

Plugins occupy one of three states:

| State | Meaning | Inplugins.enabled? | Inplugins.disabled? |
| --- | --- | --- | --- |
| enabled | Loaded on next session | Yes | No |
| disabled | Explicitly off — won't load even if also inenabled | (irrelevant) | Yes |
| not enabled | Discovered but never opted in | No | No |

`plugins.enabled`
`plugins.disabled`
`enabled`
`disabled`
`enabled`
`not enabled`

The default for a newly-installed or bundled plugin isnot enabled.hermes plugins listshows all three distinct states so you can tell what's been explicitly turned off vs. what's just waiting to be enabled.

`not enabled`
`hermes plugins list`

In a running session,/pluginsshows which plugins are currently loaded.

`/plugins`

## Injecting Messages​

Plugins can inject messages into the active conversation usingctx.inject_message():

`ctx.inject_message()`

```
ctx.inject_message("New data arrived from the webhook", role="user")
```

Signature:ctx.inject_message(content: str, role: str = "user") -> bool

`ctx.inject_message(content: str, role: str = "user") -> bool`

How it works:

- If the agent isidle(waiting for user input), the message is queued as the next input and starts a new turn.
- If the agent ismid-turn(actively running), the message interrupts the current operation — the same as a user typing a new message and pressing Enter.
- For non-"user"roles, the content is prefixed with[role](e.g.[system] ...).
- ReturnsTrueif the message was queued successfully,Falseif no CLI reference is available (e.g. in gateway mode).

`"user"`
`[role]`
`[system] ...`
`True`
`False`

This enables plugins like remote control viewers, messaging bridges, or webhook receivers to feed messages into the conversation from external sources.

inject_messageis only available in CLI mode. In gateway mode, there is no CLI reference and the method returnsFalse.

`inject_message`
`False`

See thefull guidefor handler contracts, schema format, hook behavior, error handling, and common mistakes.