---
layout: docs
title: "رابط متنی (TUI)"
permalink: /user-guide/tui/
---

- 
- Using Hermes
- TUI

# TUI

The TUI is the modern front-end for Hermes — a terminal UI backed by the same Python runtime as theClassic CLI. Same agent, same sessions, same slash commands; a cleaner, more responsive surface for interacting with them.

[Classic CLI](/docs/user-guide/cli)

It's the recommended way to run Hermes interactively.

## Launch​

```
# Launch the TUIhermes --tui# Resume the latest TUI session (falls back to the latest classic session)hermes --tui -chermes --tui --continue# Resume a specific session by ID or titlehermes --tui -r 20260409_000000_aa11bbhermes --tui --resume "my t0p session"# Run source directly — skips the prebuild step (for TUI contributors)hermes --tui --dev
```

You can also enable it via env var:

```
export HERMES_TUI=1hermes          # now uses the TUIhermes chat     # same
```

Or make it the persistent default in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
display:  interface: tui   # "cli" (default) or "tui"
```

Withdisplay.interface: tui, a barehermes(andhermes chat) launches the TUI. Explicit flags always win — runhermes --clito drop back to the classic REPL for a single invocation, orhermes --tui/HERMES_TUI=1to force the TUI when the config default iscli.

`display.interface: tui`
`hermes`
`hermes chat`
`hermes --cli`
`hermes --tui`
`HERMES_TUI=1`
`cli`

The classic CLI remains the shipped default. Anything documented inCLI Interface— slash commands, quick commands, skill preloading, personalities, multi-line input, interrupts — works in the TUI identically.

[CLI Interface](/docs/user-guide/cli)

## Why the TUI​

- Instant first frame— the banner paints before the app finishes loading, so the terminal never feels frozen while Hermes is starting.
- Non-blocking input— type and queue messages before the session is ready. Your first prompt sends the moment the agent comes online.
- Rich overlays— model picker, session picker, approval and clarification prompts all render as modal panels rather than inline flows.
- Live session panel— tools and skills fill in progressively as they initialize.
- Mouse-friendly selection— drag to highlight with a uniform background instead of SGR inverse. Copy with your terminal's normal copy gesture.
- Alternate-screen rendering— differential updates mean no flicker when streaming, no scrollback clutter after you quit.
- Composer affordances— inline paste-collapse for long snippets,Cmd+V/Ctrl+Vtext paste with clipboard-image fallback, bracketed-paste safety, and image/file-path attachment normalization.

`Cmd+V`
`Ctrl+V`

Sameskinsandpersonalitiesapply. Switch mid-session with/skin ares,/personality pirate, and the UI repaints live. SeeSkins & Themesfor the full list of customizable keys and which ones apply to classic vs TUI — the TUI honors the banner palette, UI colors, prompt glyph/color, session display, completion menu, selection bg,tool_prefix, andhelp_header.

[skins](/docs/user-guide/features/skins)
[personalities](/docs/user-guide/features/personality)
`/skin ares`
`/personality pirate`
[Skins & Themes](/docs/user-guide/features/skins)
`tool_prefix`
`help_header`

### Collapsible banner sections​

The TUI startup banner groups runtime info into four collapsible sections, each rendered with a▸/▾chevron next to the section title:

`▸`
`▾`

| Section | Default state |
| --- | --- |
| Tools | Open |
| Skills | Collapsed |
| System Prompt | Collapsed |
| MCP Servers | Collapsed |

Click anywhere on a section header (or its chevron) to toggle it. The Tools list opens by default because it's the most-checked section at session start; Skills, System Prompt, and MCP Servers collapse by default so the banner stays compact even when you've installed dozens of skills or wired up many MCP servers. State is local to the banner instance, so the next launch resets to the defaults.

## Requirements​

- Node.js≥ 20 — the TUI runs as a subprocess launched from the Python CLI.hermes doctorverifies this.
- TTY— like the classic CLI, piping stdin or running in non-interactive environments falls back to single-query mode.

`hermes doctor`

On first launch Hermes installs the TUI's Node dependencies intoui-tui/node_modules(one-time, a few seconds). Subsequent launches are fast. If you pull a new Hermes version, the TUI bundle is rebuilt automatically when sources are newer than the dist.

`ui-tui/node_modules`

### External prebuild​

Distributions that ship a prebuilt bundle (Nix, system packages) can point Hermes at it:

```
export HERMES_TUI_DIR=/path/to/prebuilt/ui-tuihermes --tui
```

The directory must containdist/entry.js.

`dist/entry.js`

## Keybindings​

Keybindings match theClassic CLIexactly. The only behavioral differences:

[Classic CLI](/docs/user-guide/cli#keybindings)
- Mouse draghighlights text with a uniform selection background.
- Cmd+V/Ctrl+Vfirst tries normal text paste, then falls back to OSC52/native clipboard reads, and finally image attach when the clipboard or pasted payload resolves to an image.
- /terminal-setupinstalls local VS Code / Cursor / Windsurf terminal bindings for betterCmd+Enterand undo/redo parity on macOS.
- Slash autocompletionopens as a floating panel with descriptions, not an inline dropdown.
- Ctrl+Xopens the live session switcher. When a queued message is highlighted (sent while the agent was still running), it still deletes that queued message instead.Esccancels editing and unhighlights without deleting.
- Ctrl+G/Ctrl+X Ctrl+E— open the current input buffer in$EDITORfor multi-line / long-prompt composition; save-and-exit sends the contents back as the prompt.

`Cmd+V`
`Ctrl+V`
`/terminal-setup`
`Cmd+Enter`
`Ctrl+X`
`Esc`
`Ctrl+G`
`Ctrl+X Ctrl+E`
`$EDITOR`

## Slash commands​

All slash commands work unchanged. A few are TUI-owned — they produce richer output or render as overlays rather than inline panels:

| Command | TUI behavior |
| --- | --- |
| /help | Overlay with categorized commands, arrow-key navigable |
| /sessions(alias/switch) | Live session switcher — list open TUI sessions, switch between them, close them, or start another one |
| /model | Modal model picker grouped by provider, with cost hints |
| /skin | Live preview — theme change applies as you browse |
| /details | Toggle verbose tool-call details (global or per-section) |
| /usage | Rich token / cost / context panel |
| /agents(alias/tasks) | Observability overlay — live subagent tree with kill/pause controls, per-branch cost / token / file rollups, turn-by-turn history |
| /reload | Re-reads~/.hermes/.envinto the running TUI process so newly added API keys take effect without a restart |
| /mouse [on|off|toggle|wheel|buttons|all] | Pick a mouse tracking preset at runtime (also persists todisplay.mouse_trackinginconfig.yaml).wheel(1000+1006) keeps scroll-wheel scrolling without the hover events that make tmux spam "No image in clipboard" over the prompt row;buttonsadds drag-to-select;allis the default with hover-driven UI. |

`/help`
`/sessions`
`/switch`
`/model`
`/skin`
`/details`
`/usage`
`/agents`
`/tasks`
`/reload`
`~/.hermes/.env`
`/mouse [on|off|toggle|wheel|buttons|all]`
`display.mouse_tracking`
`config.yaml`
`wheel`
`buttons`
`all`

Every other slash command (including installed skills, quick commands, and personality toggles) works identically to the classic CLI. SeeSlash Commands Reference.

[Slash Commands Reference](/docs/reference/slash-commands)

## Live session switcher​

Use the live session switcher when you want one terminal to act as a dispatcher for several TUI sessions. It lists only sessions that are currently live in this TUI process; closed sessions remain saved transcripts and can still be reopened with/resumeorhermes --tui --resume <id-or-title>.

`/resume`
`hermes --tui --resume <id-or-title>`

Open it with any of these:

- Ctrl+Xfrom the TUI.
- /sessionsor/switch.
- /sessions newto create a fresh live session immediately.
- Click theN live sessionscount in the status line.

`Ctrl+X`
`/sessions`
`/switch`
`/sessions new`
`N live sessions`

Inside the switcher:

- ↑/↓move the selection; mouse clicks select rows too.
- Enterswitches to the selected live session.
- Ctrl+Dcloses the selected live session.
- Ctrl+Nstarts a blank live session.
- Ctrl+Rrefreshes the live-session list.
- Esccloses the switcher.
- Select+new, type a prompt, and pressEnterto dispatch a new live session. PressTabfirst if you want to choose a model just for that new session.

`↑`
`↓`
`Enter`
`Ctrl+D`
`Ctrl+N`
`Ctrl+R`
`Esc`
`+new`
`Enter`
`Tab`

## LaTeX math rendering​

The TUI's markdown pipeline renders LaTeX math inline:$E = mc^2$and$$\frac{a}{b}$$render as Unicode-formatted math instead of the raw TeX source. Works for inline and block math; unsupported syntax falls back to showing the literal TeX wrapped in a code span so it remains copyable.

`$E = mc^2$`
`$$\frac{a}{b}$$`

This is always-on — nothing to configure. Classic CLI keeps the raw TeX.

## Light-terminal detection​

The TUI auto-detects light terminals and swaps to the light theme accordingly. Detection works in three layers:

1. HERMES_TUI_THEMEenv var — highest priority. Values:light,dark, or a raw 6-char background hex (e.g.ffffff,1a1a2e).
2. COLORFGBGenv var — the classic "what's my background color?" hint used by xterm-derived terminals.
3. Terminal background probe via OSC 11 — works on modern terminals (Ghostty, Warp, iTerm2, WezTerm, Kitty) that don't setCOLORFGBG.

`HERMES_TUI_THEME`
`light`
`dark`
`ffffff`
`1a1a2e`
`COLORFGBG`
`COLORFGBG`

If you want the light theme permanently regardless of terminal:

```
export HERMES_TUI_THEME=light
```

## Busy indicator styles​

The status-bar busy indicator is pluggable — the default rotates Hermes' kawaii face palette every 2.5 seconds during agent work. Pick a different style via config or the/indicatorslash command:

`/indicator`

```
display:  tui_status_indicator: kaomoji   # kaomoji | emoji | unicode | ascii
```

Or in-session:/indicator emoji(etc.). Styles ship with matched glyph widths so the rest of the status bar doesn't jitter on rotation.

`/indicator emoji`

## Auto-resume​

By default,hermes --tuistarts a fresh session each launch. To re-attach to the most recent TUI session automatically (useful when your terminal or SSH connection drops unexpectedly), opt in:

`hermes --tui`

```
export HERMES_TUI_RESUME=1          # most-recent TUI session# or:export HERMES_TUI_RESUME=<session-id>   # specific session
```

Unset the variable or pass--resume <id>explicitly to override on a per-launch basis.

`--resume <id>`

## Status line​

The TUI's status line tracks agent state in real time:

| Status | Meaning |
| --- | --- |
| starting agent… | Session ID is live; tools and skills still coming online. You can type — messages queue and send when ready. |
| ready | Agent is idle, accepting input. |
| thinking…/running… | Agent is reasoning or running a tool. |
| interrupted | Current turn was cancelled; press Enter to send again. |
| forging session…/resuming… | Initial connect or--resumehandshake. |

`starting agent…`
`ready`
`thinking…`
`running…`
`interrupted`
`forging session…`
`resuming…`
`--resume`

The per-skin status-bar colors and thresholds are shared with the classic CLI — seeSkinsfor customization.

[Skins](/docs/user-guide/features/skins)

The status line also shows:

- Working directory with git branch—~/projects/hermes-agent (docs/two-week-gap-sweep). The branch suffix updates when yougit checkoutin a side terminal (mtime-cached) so the TUI reflects your actual active branch, not whatever it was at launch.
- Per-prompt elapsed time—⏱ 12s/3m 45swhile the turn is running (live), frozen to⏲ 32s / 3m 45safter the turn completes. First number is time since last user message; second is total session duration. Resets on every new prompt.
- 🗜️ N— number of times the running session has been auto-compressed. Appears once the first compression fires.
- ▶ N— number of/backgroundtasks currently running in this session. Appears whenever at least one task is in flight.
- ⚠ YOLO— visible warning whenever YOLO mode is on (hermes --yolo,/yolo, orHERMES_YOLO_MODE=1). The same badge also appears in the startup banner so you cannot launch an auto-approving session without noticing.

`~/projects/hermes-agent (docs/two-week-gap-sweep)`
`git checkout`
`⏱ 12s/3m 45s`
`⏲ 32s / 3m 45s`
`🗜️ N`
`▶ N`
`/background`
`⚠ YOLO`
`hermes --yolo`
`/yolo`
`HERMES_YOLO_MODE=1`

## Configuration​

The TUI respects all standard Hermes config:~/.hermes/config.yaml, profiles, personalities, skins, quick commands, credential pools, memory providers, tool/skill enablement. No TUI-specific config file exists.

`~/.hermes/config.yaml`

A handful of keys tune the TUI surface specifically:

```
display:  skin: default              # any built-in or custom skin  personality: helpful  details_mode: collapsed    # hidden | collapsed | expanded — global accordion default  sections:                  # optional: per-section overrides (any subset)    thinking: expanded       # always open    tools: expanded          # always open    activity: collapsed      # opt back IN to the activity panel (hidden by default)  mouse_tracking: all        # off | wheel | buttons | all (or true/false for back-compat).                             #   wheel   — 1000+1006 (scroll + click; no drag, no hover —                             #             recommended inside tmux to silence the prompt-row                             #             "No image in clipboard" spam from hover events)                             #   buttons — adds 1002 for terminal-side drag selection                             #   all     — adds 1003 for hover (scrollbar paginate-on-hover,                             #             link mouseenter, etc.)
```

Runtime toggles:

- /details [hidden|collapsed|expanded|cycle]— set the global mode
- /details <section> [hidden|collapsed|expanded|reset]— override one section
(sections:thinking,tools,subagents,activity)

`/details [hidden|collapsed|expanded|cycle]`
`/details <section> [hidden|collapsed|expanded|reset]`
`thinking`
`tools`
`subagents`
`activity`

Default visibility

The TUI ships with opinionated per-section defaults that stream the turn as
a live transcript instead of a wall of chevrons:

- thinking—expanded. Reasoning streams inline as the model emits it.
- tools—expanded. Tool calls and their results render open.
- subagents— falls through to the globaldetails_mode(collapsed under
chevron by default — stays quiet until a delegation actually happens).
- activity—hidden. Ambient meta (gateway hints, terminal-parity
nudges, background notifications) is noise for most day-to-day use. Tool
failures still render inline on the failing tool row; ambient
errors/warnings surface via a floating-alert backstop when every panel
is hidden.

`thinking`
`tools`
`subagents`
`details_mode`
`activity`

Per-section overrides take precedence over both the section default and the
globaldetails_mode. To reshape the layout:

`details_mode`
- display.sections.thinking: collapsed— put thinking back under a chevron
- display.sections.tools: collapsed— put tool calls back under a chevron
- display.sections.activity: collapsed— opt the activity panel back in
- /details <section> <mode>at runtime

`display.sections.thinking: collapsed`
`display.sections.tools: collapsed`
`display.sections.activity: collapsed`
`/details <section> <mode>`

Anything set explicitly indisplay.sectionswins over the defaults, so
existing configs keep working unchanged.

`display.sections`

## Sessions​

Sessions are shared between the TUI and the classic CLI — both write to the same~/.hermes/state.db. You can start a session in one, resume in the other. The session picker surfaces sessions from both sources, with a source tag.

`~/.hermes/state.db`

SeeSessionsfor lifecycle, search, compression, and export.

[Sessions](/docs/user-guide/sessions)

## How the TUI talks to its gateway​

By default the TUI spawns its own in-process gateway, so each TUI instance is self-contained — there's nothing to configure.

You may see aHERMES_TUI_GATEWAY_URLenv var referenced in the codebase or logs. This is aninternal wiring detail of the web dashboard, not a user-facing remote-attach knob. When you open the dashboard's "Chat" tab (hermes dashboard→/chat), the dashboard's web server spawns an embedded TUI child process and injectsHERMES_TUI_GATEWAY_URLso that child attaches to the dashboard's own in-processtui_gatewayover a loopback WebSocket (/api/ws). The/api/wsendpoint exists only inside the dashboard server (hermes_cli/web_server.py) and is bound to that process's lifetime and auth.

`HERMES_TUI_GATEWAY_URL`
`hermes dashboard`
`/chat`
`HERMES_TUI_GATEWAY_URL`
`tui_gateway`
`/api/ws`
`/api/ws`
`hermes_cli/web_server.py`

There is no general "point any TUI at any standalone gateway port" mode. In particular, the OpenAI-compatible API server (hermes gateway/ theapi_serverplatform) doesnotserve/api/ws— it's the model-backend surface (/v1/chat/completions,/v1/models, …) and deliberately does not expose the TUI's JSON-RPC control channel. SettingHERMES_TUI_GATEWAY_URLto that port will 404.

`hermes gateway`
`api_server`
`/api/ws`
`/v1/chat/completions`
`/v1/models`
`HERMES_TUI_GATEWAY_URL`

If you want multiple surfaces to share one set of sessions, use the shared~/.hermes/state.db(seeSessions) or the web dashboard's embedded chat (seeWeb Dashboard) — not a hand-set gateway URL.

`~/.hermes/state.db`
[Sessions](/docs/user-guide/sessions)
[Web Dashboard](/docs/user-guide/features/web-dashboard#chat)

## Reverting to the classic CLI​

Launchinghermes(without--tui) stays on the classic CLI by default. To make a machine prefer the TUI, setdisplay.interface: tuiin~/.hermes/config.yaml(persistent) orHERMES_TUI=1in your shell profile (per-shell). To go back, setinterface: cli/ unset the env var, or passhermes --clifor a one-off.

`hermes`
`--tui`
`display.interface: tui`
`~/.hermes/config.yaml`
`HERMES_TUI=1`
`interface: cli`
`hermes --cli`

If the TUI fails to launch (no Node, missing bundle, TTY issue), Hermes prints a diagnostic and falls back — rather than leaving you stuck.

## See also​

- CLI Interface— full slash command and keybinding reference (shared)
- Sessions— resume, branch, and history
- Skins & Themes— theme the banner, status bar, and overlays
- Voice Mode— works in both interfaces
- Configuration— all config keys

[CLI Interface](/docs/user-guide/cli)
[Sessions](/docs/user-guide/sessions)
[Skins & Themes](/docs/user-guide/features/skins)
[Voice Mode](/docs/user-guide/features/voice-mode)
[Configuration](/docs/user-guide/configuration)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/tui.md)