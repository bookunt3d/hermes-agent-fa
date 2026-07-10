---
layout: docs
title: "رابط خط فرمان (CLI)"
permalink: /user-guide/cli/
---

- 
- Using Hermes
- CLI Interface

# CLI Interface

Hermes Agent's CLI is a full terminal user interface (TUI) — not a web UI. It features multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output. Built for people who live in the terminal.

One command —hermes setup --portal— and you're ready tohermes chat. SeeNous Portal.

`hermes setup --portal`
`hermes chat`
[Nous Portal](/docs/integrations/nous-portal)

Hermes also ships a modern TUI with modal overlays, mouse selection, and non-blocking input. Launch it withhermes --tui— see theTUIguide.

`hermes --tui`
[TUI](/docs/user-guide/tui)

## Running the CLI​

```
# Start an interactive session (default)hermes# Single query mode (non-interactive)hermes chat -q "Hello"# With a specific modelhermes chat --model "anthropic/claude-sonnet-4"# With a specific providerhermes chat --provider nous        # Use Nous Portalhermes chat --provider openrouter  # Force OpenRouter# With specific toolsetshermes chat --toolsets "web,terminal,skills"# Start with one or more skills preloadedhermes -s hermes-agent-dev,github-authhermes chat -s github-pr-workflow -q "open a draft PR"# Resume previous sessionshermes --continue             # Resume the most recent CLI session (-c)hermes --resume <session_id>  # Resume a specific session by ID (-r)# Verbose mode (debug output)hermes chat --verbose# Isolated git worktree (for running multiple agents in parallel)hermes -w                         # Interactive mode in worktreehermes -w -z "Fix issue #123"     # Single query in worktree
```

## Interface Layout​

The Hermes CLI banner, conversation stream, and fixed input prompt rendered as a stable docs figure instead of fragile text art.

The welcome banner shows your model, terminal backend, working directory, available tools, and installed skills at a glance.

### Status Bar​

A persistent status bar sits above the input area, updating in real time:

```
 ⚕ claude-sonnet-4-20250514 │ 12.4K/200K │ [██████░░░░] 6% │ $0.06 │ 15m
```

| Element | Description |
| --- | --- |
| Model name | Current model (truncated if longer than 26 chars) |
| Token count | Context tokens used / max context window |
| Context bar | Visual fill indicator with color-coded thresholds |
| Cost | Estimated session cost (orn/afor unknown/zero-priced models) |
| 🗜️ N | Context compression count— how many times the running session has been auto-compressed. Appears once the first compression fires. |
| ▶ N | Active background tasks— how many/backgroundprompts are still running in the current session. Appears whenever at least one task is in flight. |
| Duration | Elapsed session time |
| ⚠ YOLO | YOLO mode warning— shown wheneverHERMES_YOLO_MODEis on (eitherhermes --yoloat launch or/yolotoggled mid-session). Mirrors the banner-line warning so you can't forget you're in auto-approve mode. |

`n/a`
`/background`
`HERMES_YOLO_MODE`
`hermes --yolo`
`/yolo`

The bar adapts to terminal width — full layout at ≥ 76 columns, compact at 52–75, minimal (model + duration, plus the YOLO badge when active) below 52.

Context color coding:

| Color | Threshold | Meaning |
| --- | --- | --- |
| Green | < 50% | Plenty of room |
| Yellow | 50–80% | Getting full |
| Orange | 80–95% | Approaching limit |
| Red | ≥ 95% | Near overflow — consider/compress |

`/compress`

Use/usagefor a detailed breakdown including per-category costs (input vs output tokens).

`/usage`

### Session Resume Display​

When resuming a previous session (hermes -corhermes --resume <id>), a "Previous Conversation" panel appears between the banner and the input prompt, showing a compact recap of the conversation history. SeeSessions — Conversation Recap on Resumefor details and configuration.

`hermes -c`
`hermes --resume <id>`
[Sessions — Conversation Recap on Resume](/docs/user-guide/sessions#conversation-recap-on-resume)

## Keybindings​

| Key | Action |
| --- | --- |
| Enter | Send message |
| Alt+Enter,Ctrl+J, orShift+Enter | New line (multi-line input).Shift+Enterrequires a terminal that distinguishes it fromEnter— see below. On Windows Terminal,Alt+Enteris captured by the terminal (fullscreen toggle); useCtrl+EnterorCtrl+Jinstead. |
| Alt+V | Paste an image from the clipboard when supported by the terminal |
| Ctrl+V | Paste text and opportunistically attach clipboard images |
| Ctrl+B | Start/stop voice recording when voice mode is enabled (voice.record_key, default:ctrl+b) |
| Ctrl+G | Open the current input buffer in$EDITOR(vim/nvim/nano/VS Code/etc.). Save and quit to send the edited text as the next prompt — ideal for long, multi-paragraph prompts. |
| Ctrl+X Ctrl+E | Emacs-style alternate binding for the external editor (same behavior asCtrl+G). |
| Ctrl+C | Interrupt agent (double-press within 2s to force exit) |
| Ctrl+D | Exit |
| Ctrl+Z | Suspend Hermes to background (Unix only). Runfgin the shell to resume. |
| Tab | Accept auto-suggestion (ghost text) or autocomplete slash commands |

`Enter`
`Alt+Enter`
`Ctrl+J`
`Shift+Enter`
`Shift+Enter`
`Enter`
`Alt+Enter`
`Ctrl+Enter`
`Ctrl+J`
`Alt+V`
`Ctrl+V`
`Ctrl+B`
`voice.record_key`
`ctrl+b`
`Ctrl+G`
`$EDITOR`
`Ctrl+X Ctrl+E`
`Ctrl+G`
`Ctrl+C`
`Ctrl+D`
`Ctrl+Z`
`fg`
`Tab`

Multiline paste preview.When you paste a multi-line block, the CLI echoes a compact single-line preview ([pasted: 47 lines, 1,842 chars — press Enter to send]) instead of dumping the whole payload into the scrollback. The full content is still what gets sent; this is just display polish.

`[pasted: 47 lines, 1,842 chars — press Enter to send]`

Markdown stripping in final responses.The CLI strips the most verbose markdown fences and**bold**/*italic*wrappers fromfinalagent replies so they render as readable terminal prose rather than raw source. Code blocks and lists are preserved. This does not affect gateway platforms or tool results — they keep their markdown for native rendering.

`**bold**`
`*italic*`

## Slash Commands​

Type/to see the autocomplete dropdown. Hermes supports a large set of CLI slash commands, dynamic skill commands, and user-defined quick commands.

`/`

Common examples:

| Command | Description |
| --- | --- |
| /help | Show command help |
| /model | Show or change the current model |
| /tools | List currently available tools |
| /skills browse | Browse the skills hub and official optional skills |
| /background <prompt> | Run a prompt in a separate background session |
| /skin | Show or switch the active CLI skin |
| /voice on | Enable CLI voice mode (pressCtrl+Bto record) |
| /voice tts | Toggle spoken playback for Hermes replies |
| /reasoning high | Increase reasoning effort |
| /title My Session | Name the current session |
| /status | Show session info — model/profile/tokens/duration — followed by a localSession recapblock (recent turn counts, top tools used, files touched, latest user prompt + assistant reply). Pure local compute; no LLM call. |
| /sessions | Open an interactive session picker right inside the classic CLI (same surface the TUI uses). Type to filter, arrow keys to navigate, Enter to resume. |

`/help`
`/model`
`/tools`
`/skills browse`
`/background <prompt>`
`/skin`
`/voice on`
`Ctrl+B`
`/voice tts`
`/reasoning high`
`/title My Session`
`/status`
`/sessions`

For the full built-in CLI and messaging lists, seeSlash Commands Reference.

[Slash Commands Reference](/docs/reference/slash-commands)

For setup, providers, silence tuning, and messaging/Discord voice usage, seeVoice Mode.

[Voice Mode](/docs/user-guide/features/voice-mode)

Commands are case-insensitive —/HELPworks the same as/help. Installed skills also become slash commands automatically.

`/HELP`
`/help`

## Quick Commands​

You can define custom commands that run shell commands instantly without invoking the LLM. These work in both the CLI and messaging platforms (Telegram, Discord, etc.).

```
# ~/.hermes/config.yamlquick_commands:  status:    type: exec    command: systemctl status hermes-agent  gpu:    type: exec    command: nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader  restart:    type: alias    target: /gateway restart
```

Then type/status,/gpu, or/restartin any chat. See theConfiguration guidefor more examples.

`/status`
`/gpu`
`/restart`
[Configuration guide](/docs/user-guide/configuration#quick-commands)

## Preloading Skills at Launch​

If you already know which skills you want active for the session, pass them at launch time:

```
hermes -s hermes-agent-dev,github-authhermes chat -s github-pr-workflow -s github-auth
```

Hermes loads each named skill into the session prompt before the first turn. The same flag works in interactive mode and single-query mode.

## Skill Slash Commands​

Every installed skill in~/.hermes/skills/is automatically registered as a slash command. The skill name becomes the command:

`~/.hermes/skills/`

```
/gif-search funny cats/axolotl help me fine-tune Llama 3 on my dataset/github-pr-workflow create a PR for the auth refactor# Just the skill name loads it and lets the agent ask what you need:/excalidraw
```

## Personalities​

Set a predefined personality to change the agent's tone:

```
/personality pirate/personality kawaii/personality concise
```

Built-in personalities include:helpful,concise,technical,creative,teacher,kawaii,catgirl,pirate,shakespeare,surfer,noir,uwu,philosopher,hype.

`helpful`
`concise`
`technical`
`creative`
`teacher`
`kawaii`
`catgirl`
`pirate`
`shakespeare`
`surfer`
`noir`
`uwu`
`philosopher`
`hype`

You can also define custom personalities in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
personalities:  helpful: "You are a helpful, friendly AI assistant."  kawaii: "You are a kawaii assistant! Use cute expressions..."  pirate: "Arrr! Ye be talkin' to Captain Hermes..."  # Add your own!
```

## Multi-line Input​

There are two ways to enter multi-line messages:

1. Alt+Enter,Ctrl+J, orShift+Enter— inserts a new line
2. Backslash continuation— end a line with\to continue:

`Alt+Enter`
`Ctrl+J`
`Shift+Enter`
`\`

```
❯ Write a function that:\  1. Takes a list of numbers\  2. Returns the sum
```

Pasting multi-line text is supported — use any of the newline keys above, or simply paste content directly.

### Shift+Enter compatibility​

Most terminals send the same byte sequence forEnterandShift+Enterby default, so applications cannot distinguish them. Hermes recognisesShift+Enteronly when the terminal sends a distinct sequence via theKitty keyboard protocolor xterm'smodifyOtherKeysmode.

`Enter`
`Shift+Enter`
`Shift+Enter`
[Kitty keyboard protocol](https://sw.kovidgoyal.net/kitty/keyboard-protocol/)
`modifyOtherKeys`

| Terminal | Status |
| --- | --- |
| Kitty, foot, WezTerm, Ghostty | DistinctShift+Enterenabled by default |
| iTerm2 (recent), Alacritty, VS Code terminal, Warp | Supported once the Kitty protocol is enabled in settings |
| Windows Terminal Preview 1.25+ | Supported once the Kitty protocol is enabled in settings |
| macOS Terminal.app, stock Windows Terminal (stable) | Not supported —Shift+Enteris indistinguishable fromEnter |

`Shift+Enter`
`Shift+Enter`
`Enter`

Where the terminal cannot distinguish them,Alt+EnterandCtrl+Jcontinue to work everywhere.On Windows Terminal specifically,Alt+Enteris captured by the terminal (toggles fullscreen) and never reaches Hermes — useCtrl+Enter(delivered asCtrl+J) orCtrl+Jdirectly for a newline.

`Alt+Enter`
`Ctrl+J`
`Alt+Enter`
`Ctrl+Enter`
`Ctrl+J`
`Ctrl+J`

## Interrupting the Agent​

You can interrupt the agent at any point:

- Type a new message + Enterwhile the agent is working — it interrupts and processes your new instructions
- Ctrl+C— interrupt the current operation (press twice within 2s to force exit)
- In-progress terminal commands are killed immediately (SIGTERM, then SIGKILL after 1s)
- Multiple messages typed during interrupt are combined into one prompt

`Ctrl+C`

### Busy Input Mode​

Thedisplay.busy_input_modeconfig key controls what happens when you press Enter while the agent is working:

`display.busy_input_mode`

| Mode | Behavior |
| --- | --- |
| "interrupt"(default) | Your message interrupts the current operation and is processed immediately |
| "queue" | Your message is silently queued and sent as the next turn after the agent finishes |
| "steer" | Your message is injected into the current run via/steer, arriving at the agent after the next tool call — no interrupt, no new turn |

`"interrupt"`
`"queue"`
`"steer"`
`/steer`

```
# ~/.hermes/config.yamldisplay:  busy_input_mode: "steer"   # or "queue" or "interrupt" (default)
```

"queue"mode is useful when you want to prepare follow-up messages without accidentally canceling in-flight work."steer"mode is useful when you want to redirect the agent mid-task without interrupting — e.g. "actually, also check the tests" while it's still editing code. Unknown values fall back to"interrupt".

`"queue"`
`"steer"`
`"interrupt"`

"steer"has two automatic fallbacks: if the agent hasn't started yet, or if images are attached, the message falls back to"queue"behavior so nothing is lost.

`"steer"`
`"queue"`

You can also change it inside the CLI:

```
/busy queue/busy steer/busy interrupt/busy status
```

The very first time you press Enter while Hermes is working, Hermes prints a one-line reminder explaining the/busyknob ("(tip) Your message interrupted the current run…"). It only fires once per install — a flag inconfig.yamlunderonboarding.seen.busy_input_promptlatches it. Delete that key to see the tip again.

`/busy`
`"(tip) Your message interrupted the current run…"`
`config.yaml`
`onboarding.seen.busy_input_prompt`

### Suspending to Background​

On Unix systems, pressCtrl+Zto suspend Hermes to the background — just like any terminal process. The shell prints a confirmation:

`Ctrl+Z`

```
Hermes Agent has been suspended. Run `fg` to bring Hermes Agent back.
```

Typefgin your shell to resume the session exactly where you left off. This is not supported on Windows.

`fg`

## Tool Progress Display​

The CLI shows animated feedback as the agent works:

Thinking animation(during API calls):

```
  ◜ (｡•́︿•̀｡) pondering... (1.2s)  ◠ (⊙_⊙) contemplating... (2.4s)  ✧٩(ˊᗜˋ*)و✧ got it! (3.1s)
```

Tool execution feed:

```
  ┊ 💻 terminal `ls -la` (0.3s)  ┊ 🔍 web_search (1.2s)  ┊ 📄 web_extract (2.1s)
```

Cycle through display modes with/verbose:off → new → all → verbose. This command can also be enabled for messaging platforms — seeconfiguration.

`/verbose`
`off → new → all → verbose`
[configuration](/docs/user-guide/configuration#display-settings)

### Tool Preview Length​

Thedisplay.tool_preview_lengthconfig key controls the maximum number of characters shown in tool call preview lines (e.g. file paths, terminal commands). The default is0, which means no limit — full paths and commands are shown.

`display.tool_preview_length`
`0`

```
# ~/.hermes/config.yamldisplay:  tool_preview_length: 80   # Truncate tool previews to 80 chars (0 = no limit)
```

This is useful on narrow terminals or when tool arguments contain very long file paths.

## Session Management​

### Resuming Sessions​

When you exit a CLI session, a resume command is printed:

```
Resume this session with:  hermes --resume 20260225_143052_a1b2c3Session:        20260225_143052_a1b2c3Duration:       12m 34sMessages:       28 (5 user, 18 tool calls)
```

Resume options:

```
hermes --continue                          # Resume the most recent CLI sessionhermes -c                                  # Short formhermes -c "my project"                     # Resume a named session (latest in lineage)hermes --resume 20260225_143052_a1b2c3     # Resume a specific session by IDhermes --resume "refactoring auth"         # Resume by titlehermes -r 20260225_143052_a1b2c3           # Short form
```

Resuming restores the full conversation history from SQLite. The agent sees all previous messages, tool calls, and responses — just as if you never left.

Use/title My Session Nameinside a chat to name the current session, orhermes sessions rename <id> <title>from the command line. Usehermes sessions listto browse past sessions.

`/title My Session Name`
`hermes sessions rename <id> <title>`
`hermes sessions list`

### Session Storage​

CLI sessions are stored in Hermes's SQLite state database under~/.hermes/state.db. The database keeps:

`~/.hermes/state.db`
- session metadata (ID, title, timestamps, token counters)
- message history
- lineage across compressed/resumed sessions
- full-text search indexes used bysession_search

`session_search`

Some messaging adapters also keep per-platform transcript files alongside the database, but the CLI itself resumes from the SQLite session store.

### Context Compression​

Long conversations are automatically summarized when approaching context limits:

```
# In ~/.hermes/config.yamlcompression:  enabled: true  threshold: 0.50    # Compress at 50% of context limit by default# Summarization model configured under auxiliary:auxiliary:  compression:    model: ""  # Leave empty to use the main chat model (default). Or pin a cheap fast model, e.g. "google/gemini-3-flash-preview".
```

When compression triggers, middle turns are summarized while the first 3 and last 20 turns are always preserved.

## Background Sessions​

Run a prompt in a separate background session while continuing to use the CLI for other work:

```
/background Analyze the logs in /var/log and summarize any errors from today
```

Hermes immediately confirms the task and gives you back the prompt:

```
🔄 Background task #1 started: "Analyze the logs in /var/log and summarize..."   Task ID: bg_143022_a1b2c3
```

### How It Works​

Each/backgroundprompt spawns acompletely separate agent sessionin a daemon thread:

`/background`
- Isolated conversation— the background agent has no knowledge of your current session's history. It receives only the prompt you provide.
- Same configuration— the background agent inherits your model, provider, toolsets, reasoning settings, and fallback model from the current session.
- Non-blocking— your foreground session stays fully interactive. You can chat, run commands, or even start more background tasks.
- Multiple tasks— you can run several background tasks simultaneously. Each gets a numbered ID.

### Results​

When a background task finishes, the result appears as a panel in your terminal:

```
╭─ ⚕ Hermes (background #1) ──────────────────────────────────╮│ Found 3 errors in syslog from today:                         ││ 1. OOM killer invoked at 03:22 — killed process nginx        ││ 2. Disk I/O error on /dev/sda1 at 07:15                      ││ 3. Failed SSH login attempts from 192.168.1.50 at 14:30      │╰──────────────────────────────────────────────────────────────╯
```

If the task fails, you'll see an error notification instead. Ifdisplay.bell_on_completeis enabled in your config, the terminal bell rings when the task finishes.

`display.bell_on_complete`

### Use Cases​

- Long-running research— "/background research the latest developments in quantum error correction" while you work on code
- File processing— "/background analyze all Python files in this repo and list any security issues" while you continue a conversation
- Parallel investigations— start multiple background tasks to explore different angles simultaneously

Background sessions do not appear in your main conversation history. They are standalone sessions with their own task ID (e.g.,bg_143022_a1b2c3).

`bg_143022_a1b2c3`

## Quiet Mode​

By default, the CLI runs in quiet mode which:

- Suppresses verbose logging from tools
- Enables kawaii-style animated feedback
- Keeps output clean and user-friendly

For debug output:

```
hermes chat --verbose
```

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/cli.md)