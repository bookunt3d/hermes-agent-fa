---
layout: docs
title: "Features_Codex App Server Runtime"
permalink: /docs/user-guide/features_codex-app-server-runtime/
---

- 
- Features
- Automation
- Codex App-Server Runtime

# Codex App-Server Runtime

Hermes can optionally handopenai/*andopenai-codex/*turns to theCodex CLI app-serverinstead of running its own tool loop. When enabled, terminal commands, file edits, sandboxing, and MCP tool calls all execute inside Codex's runtime — Hermes becomes the shell around it (sessions DB, slash commands, gateway, memory and skill review).

`openai/*`
`openai-codex/*`

This isopt-in only. Default Hermes behavior is unchanged unless you flip the flag. Hermes never auto-routes you onto this runtime.

Not using OpenAI Codex?hermes setup --portalconfigures a non-Codex backend with Claude/Gemini/etc. in one step. SeeNous Portal.

`hermes setup --portal`

## Why​

- Run OpenAI agent turns against yourChatGPT subscription(no API key required) using the same auth flow Codex CLI uses.
- UseCodex's own toolset and sandbox—shellfor terminal/read/write/search,apply_patchfor structured edits,update_planfor planning, all running inside seatbelt/landlock sandboxing.
- Native Codex plugins— Linear, GitHub, Gmail, Calendar, Canva, etc. — installed viacodex pluginare auto-migrated and active in your Hermes session.
- Hermes' richer tools come along— web_search, web_extract, browser automation, vision, image generation, skills, and TTS work via an MCP callback. Codex calls back into Hermes for tools it doesn't have built in.
- Memory and skill nudges keep working— Codex's events are projected into Hermes' message shape so the self-improvement loop sees a normal-looking transcript.

`shell`
`apply_patch`
`update_plan`
`codex plugin`

## What tools the model actually has​

This is the part most users want to know up front. When this runtime is on, the model running your turn has three independent sources of tools:

### 1. Codex's built-in toolset (always on)​

These ship withcodex app-serveritself — no Hermes involvement, no MCP, no plugins. All five are available the moment the runtime starts:

`codex app-server`
- shell— runs arbitrary shell commands inside the sandbox. This is how the model reads files (cat,head,tail), writes them (echo > foo, heredocs), searches them (find,rg,grep), navigates directories (ls,cd), runs builds, manages processes, and anything else you'd do in bash.
- apply_patch— applies a structured multi-file diff in Codex's patch format. The model uses this for non-trivial code edits (adding a function, refactoring across files); shell heredocs are still available for one-off writes.
- update_plan— codex's internal todo / plan tracker. Equivalent of Hermes'todotool, but managed entirely inside codex's runtime.
- view_image— load a local image file into the conversation so the model can see it.
- web_search— codex has its own built-in web search when configured. Hermes also exposesweb_search(Firecrawl-backed) via the callback below; the model picks whichever it prefers.

`shell`
`cat`
`head`
`tail`
`echo > foo`
`find`
`rg`
`grep`
`ls`
`cd`
`apply_patch`
`update_plan`
`todo`
`view_image`
`web_search`
`web_search`

Soanything you'd do via terminal — read/write/search/find/run — codex does natively. The sandbox profile (:workspaceby default when you enable the runtime) controls what's writable.

`:workspace`

### 2. Native Codex plugins (auto-migrated from yourcodex plugininstall)​

`codex plugin`

When you enable the runtime, Hermes queries codex'splugin/listRPC and writes a[plugins."<name>@openai-curated"]entry for every plugin you have installed. The plugins themselves are managed by codex and authorized once via codex's own UI.

`plugin/list`
`[plugins."<name>@openai-curated"]`

Examples (the ones the OpenClaw thread highlighted as "YouTube-video-worthy"):

- Linear— find/update issues
- GitHub— search code, view PRs, comment
- Gmail— read/send mail
- Google Calendar— create/find events
- Outlook calendar/email— same shape via the Microsoft connector
- Canva— design generation
- ...whatever else you've installed viacodex plugin marketplace add openai-curated+codex plugin install ...

`codex plugin marketplace add openai-curated`
`codex plugin install ...`

What's NOT migrated:

- Plugins you haven't installed yet — install them in Codex first.
- ChatGPT app marketplace entries (app/list) — these are already enabled inside codex by virtue of your account auth.

`app/list`

### 3. Hermes tool callback (MCP server, registered in~/.codex/config.toml)​

`~/.codex/config.toml`

Hermes registers itself as an MCP server so codex can call back for tools codex doesn't ship with. Available via the callback:

- web_search/web_extract— Firecrawl-backed; tends to be cleaner than scraping for structured content.
- browser_navigate/browser_click/browser_type/browser_press/browser_snapshot/browser_scroll/browser_back/browser_get_images/browser_console/browser_vision— full browser automation via Camofox or Browserbase.
- vision_analyze— call a separate vision model to inspect an image (different from codex'sview_imagewhich loads it into the conversation).
- image_generate— image generation through Hermes' image_gen plugin chain.
- skill_view/skills_list— read from Hermes' skill library.
- text_to_speech— TTS through Hermes' configured provider.

`web_search`
`web_extract`
`browser_navigate`
`browser_click`
`browser_type`
`browser_press`
`browser_snapshot`
`browser_scroll`
`browser_back`
`browser_get_images`
`browser_console`
`browser_vision`
`vision_analyze`
`view_image`
`image_generate`
`skill_view`
`skills_list`
`text_to_speech`

When the model wants one of these, codex spawns thehermes_tools_mcp_serversubprocess via stdio MCP, the call is dispatched throughmodel_tools.handle_function_call()(same code path as Hermes' default runtime), and the result is returned to codex like any other MCP response.

`hermes_tools_mcp_server`
`model_tools.handle_function_call()`

### What's NOT available on this runtime​

These four Hermes tools require the running AIAgent context (mid-loop state) to dispatch, and a stateless MCP callback can't drive them. Switch back to the default runtime (/codex-runtime auto) when you need any of them:

`/codex-runtime auto`
- delegate_task— spawn subagents
- memory— Hermes' persistent memory store
- session_search— cross-session search
- todo— Hermes' todo store (codex'supdate_planis the in-runtime equivalent)

`delegate_task`
`memory`
`session_search`
`todo`
`update_plan`

## Workflow features (/goal, kanban, cron)​

`/goal`

### /goal(the Ralph loop)​

`/goal`

Works on this runtime.Goals persist instate_metakeyed by session id, the continuation prompt feeds back as a normal user message throughrun_conversation(), and codex executes the next turn natively. The goal judge runs via the auxiliary client (configured viaauxiliary.goal_judgein config.yaml), independent of which runtime is active. The judge's "blocked, needs user input" verdict is a clean escape if codex stalls on approvals.

`state_meta`
`run_conversation()`
`auxiliary.goal_judge`

One thing to be aware of:each continuation prompt is a fresh codex turn, which means codex re-evaluates command approval policy from scratch. If you're doing a long-running goal with lots of writes, expect more approval prompts than you'd see on a single in-session task. Setdefault_permissions = ":workspace"(which Hermes does automatically when you enable the runtime) so simple workspace writes don't require prompting.

`default_permissions = ":workspace"`

### Kanban (multi-agent worktree dispatch)​

Works on this runtime, with one subtle dependency.The kanban dispatcher spawns each worker as a separatehermes chat -qsubprocess that reads the user's config — which means ifmodel.openai_runtime: codex_app_serveris set globally, workers also come up on the codex runtime.

`hermes chat -q`
`model.openai_runtime: codex_app_server`

What works inside a codex-runtime worker:

- Codex's full toolset (shell, apply_patch, update_plan, view_image, web_search) — the worker does its actual task work natively
- The migrated codex plugins — Linear, GitHub, etc.
- The Hermes tool callback for browser_*, vision, image_gen, skills, TTS

What also works because the MCP callback exposes them:

- kanban_complete/kanban_block/kanban_comment/kanban_heartbeat— the worker handoff tools. These readHERMES_KANBAN_TASKfrom env (set by the dispatcher), gate access correctly, and write to the per-board SQLite DB pinned byHERMES_KANBAN_DB. Without these in the callback, a worker on this runtime could do its task but couldn't report back, hanging until the dispatcher's timeout.
- kanban_show/kanban_list— read-only board queries for the worker to check its own context.
- kanban_create/kanban_unblock/kanban_link— orchestrator-only operations. Available for orchestrator agents running on the codex runtime that need to dispatch new tasks.

`kanban_complete`
`kanban_block`
`kanban_comment`
`kanban_heartbeat`
`HERMES_KANBAN_TASK`
`HERMES_KANBAN_DB`
`kanban_show`
`kanban_list`
`kanban_create`
`kanban_unblock`
`kanban_link`

The kanban tools are gated byHERMES_KANBAN_TASKenv var the dispatcher sets — that var is propagated to the codex subprocess (codex inherits env) and from there to the spawnedhermes-toolsMCP server subprocess. So the tools see the right task id and gate correctly. For Codex app-server workers, Hermes also passes narrow app-server sandbox overrides whenHERMES_KANBAN_TASKis present: keepworkspace-writesandboxing, add theboard DB directory plus every Kanban path the dispatcher pinnedas extra writable roots (HERMES_KANBAN_WORKSPACES_ROOT,HERMES_KANBAN_WORKSPACE, legacyHERMES_KANBAN_ROOT— deduplicated, DB-dir first), and keep network disabled by default. This avoids the brittle:danger-no-sandboxworkaround while lettingkanban_complete/kanban_blockupdate the board DBandletting workers write reports/artifacts under workspace mounts that live outside the DB directory (e.g./media/.../kanban-workspaces/...on a separate drive —issue #27941).

`HERMES_KANBAN_TASK`
`hermes-tools`
`HERMES_KANBAN_TASK`
`workspace-write`
`HERMES_KANBAN_WORKSPACES_ROOT`
`HERMES_KANBAN_WORKSPACE`
`HERMES_KANBAN_ROOT`
`:danger-no-sandbox`
`kanban_complete`
`kanban_block`
`/media/.../kanban-workspaces/...`

### Cron jobs​

Not specifically tested.Cron jobs run viacronjob→AIAgent.run_conversation, the same code path as the CLI. If the cron job's config hasopenai_runtime: codex_app_serverit'll run on codex. The same tool-availability rules apply — codex built-ins + plugins + MCP callback work, agent-loop tools (delegate_task, memory, session_search, todo) don't. If your cron job relies on those, scope the cron to a profile that uses the default runtime.

`cronjob`
`AIAgent.run_conversation`
`openai_runtime: codex_app_server`

## Trade-offs​

|  | Hermes default runtime | Codex app-server (opt-in) |
| --- | --- | --- |
| delegate_tasksubagents | yes | not available — needs agent loop context |
| memory,session_search,todo | yes | not available — needs agent loop context |
| web_search,web_extract | yes | yes (via MCP callback) |
| Browser automation (Camofox/Browserbase) | yes | yes (via MCP callback) |
| vision_analyze,image_generate | yes | yes (via MCP callback) |
| skill_view,skills_list | yes | yes (via MCP callback) |
| text_to_speech | yes | yes (via MCP callback) |
| Codexshell(terminal/read/write/search/find/run) | — | yes (Codex built-in) |
| Codexapply_patch(structured multi-file edits) | — | yes (Codex built-in) |
| Codexupdate_plan(in-runtime todo) | — | yes (Codex built-in) |
| Codexview_image(load image into conversation) | — | yes (Codex built-in) |
| Codex sandbox (seatbelt/landlock, profiles) | — | yes (Codex built-in) |
| ChatGPT subscription auth | — | yes (viaopenai-codexprovider) |
| Native Codex plugins (Linear, GitHub, etc.) | — | yes (auto-migrated) |
| User MCP servers | yes | yes (auto-migrated to codex) |
| Memory + skill review (background) | yes | yes (via item projection) |
| Multi-turn conversations | yes | yes |
| /goal(Ralph loop) | yes | yes |
| Kanban worker dispatch | yes | yes (via callback) |
| Kanban orchestrator tools | yes | yes (via callback) |
| All gateway platforms | yes | yes |
| Non-OpenAI providers | yes | n/a — OpenAI/Codex-scoped |

`delegate_task`
`memory`
`session_search`
`todo`
`web_search`
`web_extract`
`vision_analyze`
`image_generate`
`skill_view`
`skills_list`
`text_to_speech`
`shell`
`apply_patch`
`update_plan`
`view_image`
`openai-codex`
`/goal`

## Prerequisites​

1. Codex CLI installed:npmi-g@openai/codexcodex--version# 0.130.0 or newer
2. Codex OAuth login.The codex subprocess reads~/.codex/auth.json. Two ways to populate it:codex login# writes tokens to ~/.codex/auth.jsonHermes' ownhermes auth login codexwrites to~/.hermes/auth.json— that's a separate session.Runcodex loginseparatelyif you haven't.
3. (Optional) Install the Codex plugins you want.When you enable the runtime, Hermes auto-migrates whichever curated plugins you've already installed via Codex CLI:codex plugin marketplaceaddopenai-curated# then via codex's TUI, install Linear / GitHub / Gmail / etc.Hermes will discover them and write[plugins."<name>@openai-curated"]entries to~/.codex/config.tomlautomatically.

Codex CLI installed:

```
npm i -g @openai/codexcodex --version   # 0.130.0 or newer
```

Codex OAuth login.The codex subprocess reads~/.codex/auth.json. Two ways to populate it:

`~/.codex/auth.json`

```
codex login                  # writes tokens to ~/.codex/auth.json
```

Hermes' ownhermes auth login codexwrites to~/.hermes/auth.json— that's a separate session.Runcodex loginseparatelyif you haven't.

`hermes auth login codex`
`~/.hermes/auth.json`
`codex login`

(Optional) Install the Codex plugins you want.When you enable the runtime, Hermes auto-migrates whichever curated plugins you've already installed via Codex CLI:

```
codex plugin marketplace add openai-curated# then via codex's TUI, install Linear / GitHub / Gmail / etc.
```

Hermes will discover them and write[plugins."<name>@openai-curated"]entries to~/.codex/config.tomlautomatically.

`[plugins."<name>@openai-curated"]`
`~/.codex/config.toml`

## Enabling​

In a Hermes session:

```
/codex-runtime codex_app_server
```

That command:

- Verifies thecodexCLI is installed (blocks with an install hint if not).
- Persistsmodel.openai_runtime: codex_app_serverto your config.yaml.
- Migrates user MCP servers from~/.hermes/config.yamlto~/.codex/config.toml.
- Discovers and migrates installed native Codex plugins(Linear, GitHub, Gmail, Calendar, Canva, etc.) by querying Codex'splugin/listRPC.
- Registers Hermes' own tools as an MCP serverso the codex subprocess can call back for tools codex doesn't ship with.
- Writesdefault_permissions = ":workspace"so the sandbox allows writes within the workspace without prompting for every operation.
- Tells you what was migrated. Takes effect on thenextsession — the current cached agent keeps the prior runtime so prompt caches stay valid.

`codex`
`model.openai_runtime: codex_app_server`
`~/.hermes/config.yaml`
`~/.codex/config.toml`
`plugin/list`
`default_permissions = ":workspace"`

Synonyms:/codex-runtime on,/codex-runtime off,/codex-runtime auto.

`/codex-runtime on`
`/codex-runtime off`
`/codex-runtime auto`

To check current state without changing anything:

```
/codex-runtime
```

You can also set it manually in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
model:  openai_runtime: codex_app_server   # default is "auto" (= Hermes runtime)
```

## Self-improvement loop (memory + skill nudges)​

Hermes' background self-improvement fires on counter thresholds:

- Every 10 user prompts → a forked review agent looks at the conversation and decides whether anything should be saved to memory.
- Every 10 tool iterations within a single turn → same idea but for skills (skill_managewrites).

`skill_manage`

Both keep working on the codex runtime.The codex path projects each completedcommandExecution/fileChange/mcpToolCall/dynamicToolCallitem into a syntheticassistant tool_call+toolresult message, so by the time the review runs it sees the same shape it sees on the default Hermes runtime.

`commandExecution`
`fileChange`
`mcpToolCall`
`dynamicToolCall`
`assistant tool_call`
`tool`

How the wiring stays equivalent:

|  | Default runtime | Codex runtime |
| --- | --- | --- |
| _turns_since_memoryincrements | per user prompt, in run_conversation pre-loop | same code path, before the early-return |
| _iters_since_skillincrements | per tool iteration in the chat-completions loop | byturn.tool_iterationsafter the codex turn returns |
| Memory trigger (_turns_since_memory >= _memory_nudge_interval) | computed in pre-loop, fires after response | computed in pre-loop, passed through to codex helper |
| Skill trigger (_iters_since_skill >= _skill_nudge_interval) | computed after the loop | computed after the codex turn |
| _spawn_background_review(messages_snapshot=..., review_memory=..., review_skills=...) | called when either trigger fires | called identically when either trigger fires |

`_turns_since_memory`
`_iters_since_skill`
`turn.tool_iterations`
`_turns_since_memory >= _memory_nudge_interval`
`_iters_since_skill >= _skill_nudge_interval`
`_spawn_background_review(messages_snapshot=..., review_memory=..., review_skills=...)`

One detail: the review fork itself needs to call Hermes' agent-loop tools (memory,skill_manage), which require Hermes' own dispatch. So when the parent agent is oncodex_app_server, the review fork isdowngraded tocodex_responses— same OAuth credentials, sameopenai-codexprovider, but talks to OpenAI's Responses API directly so Hermes owns the loop and the agent-loop tools work. This is invisible to the user.

`memory`
`skill_manage`
`codex_app_server`
`codex_responses`
`openai-codex`

Net effect: enable the codex runtime and your memory + skill nudges keep firing exactly as they would otherwise.

## How approvals work​

Codex requests approval before executing commands or applying patches. These get translated into Hermes' standard "Dangerous Command" prompt:

```
╭───────────────────────────────────────╮│ Dangerous Command                     ││                                       ││ /bin/bash -lc 'echo hello > foo.txt'  ││                                       ││ ❯ 1. Allow once                       ││   2. Allow for this session           ││   3. Deny                             ││                                       ││ Codex requests exec in /your/cwd      │╰───────────────────────────────────────╯
```

- Allow once→ approve this single command.
- Allow for this session→ Codex won't re-prompt for similar commands.
- Deny→ command is rejected; Codex continues in read-only mode.

Forapply_patch(file edit) approvals, Hermes shows a summary of what changed (1 add, 1 update: /tmp/new.py, /tmp/old.py) when codex provides the data via the correspondingfileChangeitem.

`apply_patch`
`1 add, 1 update: /tmp/new.py, /tmp/old.py`
`fileChange`

## Permission profiles​

Codex has three built-in permission profiles:

- :read-only— no writes; every shell command requires approval
- :workspace— writes within the current workspace allowed without prompts (Hermes' default when you enable the runtime)
- :danger-no-sandbox— no sandbox at all (don't use this unless you understand it)

`:read-only`
`:workspace`
`:danger-no-sandbox`

You can override the default in~/.codex/config.tomloutside Hermes' managed block:

`~/.codex/config.toml`

```
default_permissions = ":read-only"
```

(Hermes will preserve your override on re-migration as long as it lives outside the# managed by hermes-agentmarkers.)

`# managed by hermes-agent`

## Auxiliary tasks and ChatGPT subscription token cost​

When this runtime is on with theopenai-codexprovider,auxiliary tasks (title generation, context compression, vision auto-detect, the background self-improvement review fork) also flow through your ChatGPT subscription by default, because Hermes' auxiliary client uses the main provider/model when no per-task override is set.

`openai-codex`

This isn't specific tocodex_app_server— it's true for the existingcodex_responsespath too — but it's more visible here because you're explicitly opting in for the subscription billing.

`codex_app_server`
`codex_responses`

To route specific aux tasks to a cheaper / different model, set explicit overrides in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
auxiliary:  title_generation:    provider: openrouter    model: google/gemini-3-flash-preview  compression:    provider: openrouter    model: google/gemini-3-flash-preview  vision:    provider: openrouter    model: google/gemini-3-flash-preview  goal_judge:    provider: openrouter    model: google/gemini-3-flash-preview
```

The self-improvement review fork inherits the main runtime via_current_main_runtime()and Hermes downgrades it fromcodex_app_servertocodex_responsesautomatically (so the fork can actually callmemoryandskill_manage— Hermes' own agent-loop tools). That fork still uses your subscription auth unless you've routed aux tasks elsewhere.

`_current_main_runtime()`
`codex_app_server`
`codex_responses`
`memory`
`skill_manage`

## Editing~/.codex/config.tomlsafely​

`~/.codex/config.toml`

Hermes wraps everything it manages between two marker comments:

```
# managed by hermes-agent — `hermes codex-runtime migrate` regenerates this sectiondefault_permissions = ":workspace"[mcp_servers.filesystem]...[plugins."github@openai-curated"]...# end hermes-agent managed section
```

Anythingoutsidethat block is yours. Re-running migration (via/codex-runtime codex_app_serveror whenever you toggle the runtime on) replaces the managed block in place but preserves user content above and below it verbatim. This means you can:

`/codex-runtime codex_app_server`
- Add your own MCP servers Hermes doesn't know about
- Overridedefault_permissionsto:read-onlyif you prefer to be prompted
- Configure codex-only options (model, providers, otel, etc.)
- Add user-defined permission profiles in[permissions.<name>]tables

`default_permissions`
`:read-only`
`[permissions.<name>]`

Anything you addinsidethe managed block will get clobbered on the next migration. If you need a tweak that requires editing the managed block, file an issue and we'll add the knob.

## Multi-profile / multi-tenant setups​

By default, Hermes points the codex subprocess at~/.codex/regardless of which Hermes profile is active. This meanshermes -p workandhermes -p personalshare the same Codex auth, plugins, and config. For most users this is the right behavior — it matches what runningcodexCLI directly would do.

`~/.codex/`
`hermes -p work`
`hermes -p personal`
`codex`

If you want per-profile Codex isolation (separate auth, separate installed plugins, separate config), setCODEX_HOMEexplicitly per profile. The cleanest way is to point at a directory under yourHERMES_HOME:

`CODEX_HOME`
`HERMES_HOME`

```
# Inside the work profile, you might wrap hermes:CODEX_HOME=~/.hermes/profiles/work/codex hermes chat
```

You'll need to re-runcodex loginonce with thatCODEX_HOMEset so the OAuth tokens land in the profile-scoped location. After that,hermes -p workwill operate on isolated Codex state.

`codex login`
`CODEX_HOME`
`hermes -p work`

We don't auto-scope this because moving an existing user's~/.codex/would silently invalidate their Codex CLI auth — anyone who already rancodex loginwould have to re-authenticate. Opt-in feels safer than surprising users.

`~/.codex/`
`codex login`

## HOME environment variable passthrough​

Hermes does NOT rewriteHOMEwhen spawning the codex app-server subprocess (we useos.environ.copy()and only overlayCODEX_HOMEandRUST_LOG). This means:

`HOME`
`os.environ.copy()`
`CODEX_HOME`
`RUST_LOG`
- Commands codex runs via itsshelltool see the real userHOMEand find~/.gitconfig,~/.gh/,~/.aws/,~/.npmrc, etc. correctly.
- Codex's internal state stays isolated throughCODEX_HOME(which points at~/.codex/by default).

`shell`
`HOME`
`~/.gitconfig`
`~/.gh/`
`~/.aws/`
`~/.npmrc`
`CODEX_HOME`
`~/.codex/`

This matches the boundary OpenClaw arrived at after some early experimentation: isolate Codex's state, leave the user's home alone. (Cf. openclaw/openclaw#81562.)

## MCP server migration​

Hermes'mcp_serversconfig is auto-translated to the TOML format Codex expects. The migration runs every time you enable the runtime and is idempotent — re-runs replace the managed section but preserve any user-edited Codex config.

`mcp_servers`

What translates:

| Hermes (config.yaml) | Codex (config.toml) |
| --- | --- |
| command+args+env | stdio transport |
| url+headers | streamable_http transport |
| timeout | tool_timeout_sec |
| connect_timeout | startup_timeout_sec |
| enabled: false | enabled = false |

`config.yaml`
`config.toml`
`command`
`args`
`env`
`url`
`headers`
`timeout`
`tool_timeout_sec`
`connect_timeout`
`startup_timeout_sec`
`enabled: false`
`enabled = false`

What's not migrated:

- Hermes-specific keys likesampling(Codex's MCP client has no equivalent — these are dropped with a per-server warning).

`sampling`

## Native Codex plugin migration​

Plugins installed viacodex plugin(Linear, GitHub, Gmail, Calendar, Canva, etc.) are discovered through Codex'splugin/listRPC. For each plugin whereinstalled: true, Hermes writes a[plugins."<name>@openai-curated"]block enabling it in your Hermes session.

`codex plugin`
`plugin/list`
`installed: true`
`[plugins."<name>@openai-curated"]`

This means: when your friend says "I have Calendar and GitHub set up in my Codex CLI" and they enable Hermes' codex runtime, Hermes activates those automatically. No re-configuration needed.

What's NOT migrated:

- Plugins you haven't installed yet — install them in Codex first.
- Plugins where codex reportsavailability != AVAILABLE(broken install, expired OAuth, removed from marketplace, etc.). These are skipped to avoid writing config that would fail at activation time.
- ChatGPT app marketplace entries (the per-accountapp/listresults — these are already enabled inside codex by virtue of your account auth).
- Plugin OAuth — you authorize each plugin once in Codex itself; Hermes doesn't touch credentials.

`availability != AVAILABLE`
`app/list`

## Hermes tool callback (the new MCP server)​

Codex's built-in toolset covers shell/file ops/patches but doesn't have web search, browser automation, vision, image generation, etc. To keep those usable in a codex turn, Hermes registers itself as an MCP server in~/.codex/config.toml:

`~/.codex/config.toml`

```
[mcp_servers.hermes-tools]command = "/path/to/python"args = ["-m", "agent.transports.hermes_tools_mcp_server"]env = { HERMES_HOME = "/your/.hermes", PYTHONPATH = "...", HERMES_QUIET = "1" }startup_timeout_sec = 30.0tool_timeout_sec = 600.0
```

When the model callsweb_search(or another exposed Hermes tool), codex spawns thehermes_tools_mcp_serversubprocess via stdio, the request is dispatched throughmodel_tools.handle_function_call(), and the result is projected back to codex like any other MCP response.

`web_search`
`hermes_tools_mcp_server`
`model_tools.handle_function_call()`

Tools available via the callback:web_search,web_extract,browser_navigate,browser_click,browser_type,browser_press,browser_snapshot,browser_scroll,browser_back,browser_get_images,browser_console,browser_vision,vision_analyze,image_generate,skill_view,skills_list,text_to_speech.

`web_search`
`web_extract`
`browser_navigate`
`browser_click`
`browser_type`
`browser_press`
`browser_snapshot`
`browser_scroll`
`browser_back`
`browser_get_images`
`browser_console`
`browser_vision`
`vision_analyze`
`image_generate`
`skill_view`
`skills_list`
`text_to_speech`

Tools NOT available:delegate_task,memory,session_search,todo. These need the running AIAgent context to dispatch (mid-loop state) and a stateless MCP callback can't drive them. Use the default Hermes runtime (/codex-runtime auto) when you need these.

`delegate_task`
`memory`
`session_search`
`todo`
`/codex-runtime auto`

## Disabling​

Switch back at any time:

```
/codex-runtime auto
```

Effective on the next session. The Codex managed block stays in~/.codex/config.tomlso you can re-enable later without losing config — or remove it manually if you prefer.

`~/.codex/config.toml`

## Limitations​

This runtime isopt-in beta. Working as of Hermes Agent 2026.5 + Codex CLI 0.130.0:

- Multi-turn conversations
- commandExecutionandfileChange(apply_patch) approvals via Hermes UI
- MCP tool calls (verified against@modelcontextprotocol/server-filesystemand the newhermes-toolscallback)
- Native Codex plugin migration (verified against Linear / GitHub / Calendar inventory)
- Deny/cancel paths
- Toggle on/off cycle
- Memory and skill nudge counters (verified live via integration tests)
- Hermes web_search through codex (verified live: "OpenAI Codex CLI – Getting Started" returned end-to-end)

`commandExecution`
`fileChange`
`@modelcontextprotocol/server-filesystem`
`hermes-tools`

Known limitations:

- Hermes auth and codex auth are separate sessions.You need bothcodex loginANDhermes auth login codexfor the cleanest UX (the runtime uses codex's session for the LLM call). This is a deliberate design choice in Hermes'_import_codex_cli_tokens— Hermes won't share OAuth state with codex CLI to avoid clobbering each other on token refresh.
- delegate_task,memory,session_search,todoare unavailable on this runtime.They need the running AIAgent context which a stateless MCP callback can't provide. Use/codex-runtime autowhen you need these.
- No inline patch preview in approval prompts when codex doesn't track the changeset.Codex'sfileChangeapproval params don't always carry the changeset. Hermes caches the data from the correspondingitem/startednotification when possible, but if approval arrives before the item has streamed, the prompt falls back to whateverreasoncodex provides.
- Sub-second cancellation isn't guaranteed.Mid-stream interrupts (Ctrl+C while codex is responding) are sent viaturn/interrupt, but if codex has already flushed the final message, you get the response anyway.

`codex login`
`hermes auth login codex`
`_import_codex_cli_tokens`
`delegate_task`
`memory`
`session_search`
`todo`
`/codex-runtime auto`
`fileChange`
`item/started`
`reason`
`turn/interrupt`

If you find a bug,open an issuewith the output ofhermes logs --since 5m. Mentioncodex-runtimein the title so it's easy to triage.

`hermes logs --since 5m`
`codex-runtime`

## Architecture​

```
                ┌─── Hermes shell (CLI / TUI / gateway) ───┐                │  sessions DB · slash commands · memory   │                │  & skill review · cron · session pickers │                └──┬──────────────────────────────────────┬┘                   │ user_message               final     │                   ▼                            text +    │        ┌──────────────────────────────────┐   projected  │        │  AIAgent.run_conversation()       │   messages   │        │   if api_mode == codex_app_server │              │        │     → CodexAppServerSession       │              │        │   else: chat_completions / codex_responses (default)        └────┬─────────────────────────────┘              │             │ JSON-RPC over stdio                        │             ▼                                            │        ┌──────────────────────────────────┐              │        │  codex app-server (subprocess)    │──────────────┘        │   thread/start, turn/start        │        │   item/* notifications            │        │   shell + apply_patch + update_plan│        │   view_image + sandbox            │        │   ┌─────────────────────────┐     │        │   │  MCP client             │     │        │   │  ├─ user MCP servers    │     │        │   │  ├─ native plugins      │     │        │   │  │   (linear, github,   │     │        │   │  │    gmail, calendar,  │     │        │   │  │    canva, ...)       │     │        │   │  └─ hermes-tools ───────┼─────────────────┐        │   │       (callback to     │     │           │        │   │        Hermes' richer  │     │           │        │   │        tools)          │     │           │        │   └─────────────────────────┘     │           │        └──────────────────────────────────┘           │                                                        │                                                        ▼        ┌──────────────────────────────────────────────────────────┐        │  hermes_tools_mcp_server.py (subprocess on demand)        │        │   web_search, web_extract, browser_*, vision_analyze,    │        │   image_generate, skill_view, skills_list, text_to_speech│        └──────────────────────────────────────────────────────────┘
```

For implementation details, seePR #24182and theCodex app-server protocol README.