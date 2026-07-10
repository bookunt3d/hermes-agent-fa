---
layout: docs
title: "ویندوز (بومی)"
permalink: /user-guide/windows-native/
---

- 
- Using Hermes
- Windows (Native)

# Windows (Native) Guide

Hermes runs natively on Windows 10 and Windows 11 — no WSL, no Cygwin, no Docker. This page is the deep dive: what works natively, what's WSL-only, what the installer actually does, and the Windows-specific knobs you might need to touch.

If you just want to install, the one-liner on thelanding pageorInstallation pageis all you need. Come back here when something surprises you.

[landing page](/docs/)
[Installation page](/docs/getting-started/installation#windows-native-powershell)

If you prefer a real POSIX environment (for the dashboard's embedded terminal,forksemantics, Linux-style file watchers, etc.), see theWindows (WSL2) Guide. Both coexist cleanly: native data lives under%LOCALAPPDATA%\hermes, WSL data lives under~/.hermes.

`fork`
[Windows (WSL2) Guide](/docs/user-guide/windows-wsl-quickstart)
`%LOCALAPPDATA%\hermes`
`~/.hermes`

## Quick install​

OpenPowerShell(or Windows Terminal) and run:

```
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

No admin rights required. The installer goes to%LOCALAPPDATA%\hermes\and addshermesto yourUser PATH— open a new terminal after it finishes.

`%LOCALAPPDATA%\hermes\`
`hermes`

Installer options(requires the scriptblock form to pass parameters):

```
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1))) -NoVenv -SkipSetup -Branch main
```

| Parameter | Default | Purpose |
| --- | --- | --- |
| -Branch | main | Clone a specific branch (useful for testing PRs) |
| -Commit | unset | Pin install to a specific commit SHA (overrides-Branch) |
| -Tag | unset | Pin install to a specific git tag (e.g.v0.14.0) |
| -NoVenv | off | Skip venv creation (advanced — you manage Python yourself) |
| -SkipSetup | off | Skip the post-installhermes setupwizard |
| -HermesHome | %LOCALAPPDATA%\hermes | Override data directory |
| -InstallDir | %LOCALAPPDATA%\hermes\hermes-agent | Override code location |

`-Branch`
`main`
`-Commit`
`-Branch`
`-Tag`
`v0.14.0`
`-NoVenv`
`-SkipSetup`
`hermes setup`
`-HermesHome`
`%LOCALAPPDATA%\hermes`
`-InstallDir`
`%LOCALAPPDATA%\hermes\hermes-agent`

The installer auto-retries flaky git fetches and strips BOM from any downloadedinstall.ps1payload, so a UTF-8 BOM picked up during HTTP transit no longer breaks the[scriptblock]::Create((irm ...))form.

`install.ps1`
`[scriptblock]::Create((irm ...))`

### Desktop installer (alternative)​

A thin GUI installer is also available — useful if you'd rather double-click an.exethan open PowerShell. Download Hermes Desktop, run the installer, and on first launch the GUI callsinstall.ps1under the hood to provision Python (viauv), Node, PortableGit, and the rest of the dependency bootstrap described below. After the first run, the desktop app and the PowerShell-installedhermesCLI share the same%LOCALAPPDATA%\hermes\hermes-agentinstall and%LOCALAPPDATA%\hermesdata directory — switch between the GUI and the CLI freely.

`.exe`
`install.ps1`
`uv`
`hermes`
`%LOCALAPPDATA%\hermes\hermes-agent`
`%LOCALAPPDATA%\hermes`

Use the desktop installer when you want a familiar Windows install experience or you're handing Hermes to a non-developer; use the PowerShell one-liner when you're already in a terminal.

### Dependency bootstrap (dep_ensure)​

`dep_ensure`

On first launch (and on demand when a missing tool is detected), Hermes runs a small Python bootstrapper —hermes_cli/dep_ensure.py— that checks for and lazily installs the non-Python dependencies it needs. On Windows, the relevant ones are:

`hermes_cli/dep_ensure.py`

| Dependency | Why Hermes needs it |
| --- | --- |
| PortableGit | Providesbash.exefor the terminal tool andgitfor in-session clones. Provisioned at install time, not bydep_ensure. |
| Node.js 22 | Required for the browser tool (agent-browser), the TUI's web bridge, and the WhatsApp bridge. |
| ffmpeg | Audio format conversion for TTS / voice messages. |
| ripgrep | Fast file search — falls back togrepif unavailable. |
| npm packages | agent-browser, Playwright Chromium, and any per-toolset Node deps are installed once at first browser-tool use. |

`bash.exe`
`git`
`dep_ensure`
`agent-browser`
`grep`
`agent-browser`

Each dep has ashutil.which(...)-style check; if a binary is missing and the run is interactive,dep_ensureoffers to install it (deferring toscripts\install.ps1 -ensure <dep>for the actual install logic). Non-interactive runs (gateway, cron, headless desktop launches) skip the prompt and surface a clearthis feature needs <dep>error instead.

`shutil.which(...)`
`dep_ensure`
`scripts\install.ps1 -ensure <dep>`
`this feature needs <dep>`

## What the installer actually does​

Top-to-bottom, in order:

1. Bootstrapsuv— Astral's fast Python manager. Installed to%USERPROFILE%\.local\bin.
2. Installs Python 3.11viauv. No existing Python needed.
3. Installs Node.js 22(winget if available, else a portable Node tarball unpacked under%LOCALAPPDATA%\hermes\node). Used for the browser tool and the WhatsApp bridge.
4. Installs portable Git— ifgitis already on PATH the installer uses it; otherwise it downloads a trimmed, self-containedPortableGit(~45 MB, from the officialgit-for-windowsrelease) to%LOCALAPPDATA%\hermes\git. No admin, no Windows installer registry, no interference with anything else on the box.
5. Clones the repoto%LOCALAPPDATA%\hermes\hermes-agentand creates a virtualenv inside it.
6. Tiereduv pip install— tries.[all]first, falls back to progressively smaller sets ([messaging,dashboard,ext]→[messaging]→.) if agit+httpsdep flakes on rate-limited GitHub. Prevents "single flake drops you to a bare install" failure mode.
7. Auto-installs messaging SDKskeyed off.env— ifTELEGRAM_BOT_TOKEN/DISCORD_BOT_TOKEN/SLACK_BOT_TOKEN/SLACK_APP_TOKEN/WHATSAPP_ENABLEDare present, runspython -m ensurepip --upgradeand targetedpip installcalls so each platform's SDK is actually importable.
8. SetsHERMES_GIT_BASH_PATHto the resolvedbash.exeso Hermes finds it deterministically in fresh shells.
9. Adds%LOCALAPPDATA%\hermes\hermes-agent\venv\Scriptsto User PATH and setsHERMES_HOME=%LOCALAPPDATA%\hermes— exposes thehermescommand (and points it at your data dir) after you open a new terminal.
10. Runshermes setup— the normal first-run wizard (model, provider, toolsets). Skip with-SkipSetup.

`uv`
`%USERPROFILE%\.local\bin`
`uv`
`%LOCALAPPDATA%\hermes\node`
`git`
`git-for-windows`
`%LOCALAPPDATA%\hermes\git`
`%LOCALAPPDATA%\hermes\hermes-agent`
`uv pip install`
`.[all]`
`[messaging,dashboard,ext]`
`[messaging]`
`.`
`git+https`
`.env`
`TELEGRAM_BOT_TOKEN`
`DISCORD_BOT_TOKEN`
`SLACK_BOT_TOKEN`
`SLACK_APP_TOKEN`
`WHATSAPP_ENABLED`
`python -m ensurepip --upgrade`
`pip install`
`HERMES_GIT_BASH_PATH`
`bash.exe`
`%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts`
`HERMES_HOME=%LOCALAPPDATA%\hermes`
`hermes`
`hermes setup`
`-SkipSetup`

On Windows, per-tool API key setup (Firecrawl, FAL, Browser Use, OpenAI TTS) is the highest-friction part of getting a useful agent. ANous Portalsubscription covers the modelandall of those tools through one OAuth login. After the installer finishes, runhermes setup --portalto wire everything up.

[Nous Portal](/docs/user-guide/features/tool-gateway)
`hermes setup --portal`

## Feature matrix​

Everything except the dashboard's embedded terminal pane runs natively on Windows.

| Feature | Native Windows | WSL2 |
| --- | --- | --- |
| CLI (hermes chat,hermes setup,hermes gateway, …) | ✓ | ✓ |
| Interactive TUI (hermes --tui) | ✓ | ✓ |
| Messaging gateway (Telegram, Discord, Slack, WhatsApp, 15+ platforms) | ✓ | ✓ |
| Cron scheduler | ✓ | ✓ |
| Browser tool (Chromium via Node) | ✓ | ✓ |
| MCP servers (stdio and HTTP) | ✓ | ✓ |
| Local Ollama / LM Studio / llama-server | ✓ | ✓ (via WSL networking) |
| Web dashboard (sessions, jobs, metrics, config) | ✓ | ✓ |
| Dashboard/chatembedded terminal pane | ✗ (needs POSIX PTY) | ✓ |
| Auto-start at login | ✓ (schtasks) | ✓ (systemd) |

`hermes chat`
`hermes setup`
`hermes gateway`
`hermes --tui`
`/chat`

The dashboard's/chattab embeds a real terminal via a POSIX PTY (ptyprocess). Native Windows has no equivalent primitive; Python'spywinpty/ Windows ConPTY would work but is a separate implementation — treat as future work.The rest of the dashboard works natively— only that one tab shows a "use WSL2 for this" banner.

`/chat`
`ptyprocess`
`pywinpty`

## How Hermes runs shell commands on Windows​

Hermes's terminal tool runs commands throughGit Bash, same strategy Claude Code uses. This sidesteps the POSIX-vs-Windows gap without rewriting every tool.

Resolution order forbash.exe:

`bash.exe`
1. HERMES_GIT_BASH_PATHenvironment variable if set.
2. %LOCALAPPDATA%\hermes\git\usr\bin\bash.exe(installer-managed PortableGit).
3. %LOCALAPPDATA%\hermes\git\bin\bash.exe(older Git-for-Windows layout).
4. System Git-for-Windows install (%ProgramFiles%\Git\bin\bash.exe, etc.).
5. MSYS2, Cygwin, or anybash.exeon PATH as a last resort.

`HERMES_GIT_BASH_PATH`
`%LOCALAPPDATA%\hermes\git\usr\bin\bash.exe`
`%LOCALAPPDATA%\hermes\git\bin\bash.exe`
`%ProgramFiles%\Git\bin\bash.exe`
`bash.exe`

The installer setsHERMES_GIT_BASH_PATHexplicitly so fresh PowerShell sessions don't have to re-discover. Override it if you want Hermes to use a specific bash — for example, your system Git Bash or a WSL-hosted bash via a symlink.

`HERMES_GIT_BASH_PATH`

Pitfall:MinGit's layout is different from the full Git-for-Windows installer — bash lives underusr\bin\bash.exe, notbin\bash.exe. Hermes checks both. If you're manually unpacking a MinGit zip, make sure you pick thenon-busyboxvariant (MinGit-*-64-bit.zip, notMinGit-*-busybox*.zip) — busybox builds shipashinstead ofbashand most coreutils are missing.

`usr\bin\bash.exe`
`bin\bash.exe`
`MinGit-*-64-bit.zip`
`MinGit-*-busybox*.zip`
`ash`
`bash`

## UTF-8 console on Windows​

Python's default stdio on Windows uses the console's active code page (usually cp1252 or cp437). Hermes's banner, slash-command list, tool feed, Rich panels, and skill descriptions all contain Unicode. Without intervention, any of that crashes withUnicodeEncodeError: 'charmap' codec can't encode character….

`UnicodeEncodeError: 'charmap' codec can't encode character…`

The fix is inhermes_cli/stdio.py::configure_windows_stdio(), called early in every entry point (cli.py::main,hermes_cli/main.py::main,gateway/run.py::main). It:

`hermes_cli/stdio.py::configure_windows_stdio()`
`cli.py::main`
`hermes_cli/main.py::main`
`gateway/run.py::main`
1. Flips the console code page to CP_UTF8 (65001) viakernel32.SetConsoleCP/SetConsoleOutputCP.
2. Reconfiguressys.stdout/sys.stderr/sys.stdinto UTF-8 witherrors='replace'.
3. SetsPYTHONIOENCODING=utf-8andPYTHONUTF8=1(viasetdefault, so explicit user values win) so child Python subprocesses inherit UTF-8.
4. SetsEDITOR=notepadif neitherEDITORnorVISUALis set (see the Editor section below).

`kernel32.SetConsoleCP`
`SetConsoleOutputCP`
`sys.stdout`
`sys.stderr`
`sys.stdin`
`errors='replace'`
`PYTHONIOENCODING=utf-8`
`PYTHONUTF8=1`
`setdefault`
`EDITOR=notepad`
`EDITOR`
`VISUAL`

Idempotent. No-op on non-Windows.

Opt out:HERMES_DISABLE_WINDOWS_UTF8=1in the environment falls back to the legacy cp1252 stdio path. Useful for bisecting an encoding bug; unlikely to be the right setting in normal operation.

`HERMES_DISABLE_WINDOWS_UTF8=1`

## The editor (Ctrl-X Ctrl-E,/edit)​

`Ctrl-X Ctrl-E`
`/edit`

Pre-#21561, pressingCtrl-X Ctrl-Eor typing/editsilently did nothing on Windows. prompt_toolkit has a hardcoded POSIX-absolute fallback list (/usr/bin/nano,/usr/bin/pico,/usr/bin/vi, …) that never resolves on Windows — even with full Git for Windows installed.

`Ctrl-X Ctrl-E`
`/edit`
`/usr/bin/nano`
`/usr/bin/pico`
`/usr/bin/vi`

Hermes's Windows stdio shim now setsEDITOR=notepadas a default. Notepad ships with every Windows install and works as a blocking editor —subprocess.call(["notepad", file])blocks until the window closes.

`EDITOR=notepad`
`subprocess.call(["notepad", file])`

User overrides still win(they're checked before the setdefault):

| Editor | PowerShell command |
| --- | --- |
| VS Code | $env:EDITOR = "code --wait" |
| Notepad++ | $env:EDITOR = "'C:\Program Files\Notepad++\notepad++.exe' -multiInst -nosession" |
| Neovim | $env:EDITOR = "nvim" |
| Helix | $env:EDITOR = "hx" |

`$env:EDITOR = "code --wait"`
`$env:EDITOR = "'C:\Program Files\Notepad++\notepad++.exe' -multiInst -nosession"`
`$env:EDITOR = "nvim"`
`$env:EDITOR = "hx"`

The--waitflag on VS Code is critical — without it the editor returns immediately and Hermes gets a blank buffer back.

`--wait`

Set it permanently in your PowerShell profile:

```
# In $PROFILE$env:EDITOR = "code --wait"
```

Or as a User environment variable in System Settings so every new shell picks it up.

## Ctrl+Enterfor newline in the CLI​

`Ctrl+Enter`

Windows Terminal passesCtrl+Enterthrough as a dedicated key sequence. Hermes binds it to "insert newline" so you can compose multi-line prompts in the CLI without falling back toEsc-then-Enter. Works in Windows Terminal, VS Code integrated terminal, and any modern Windows console host that honors VT escape sequences.

`Ctrl+Enter`
`Esc`
`Enter`

On legacycmd.execonsolesCtrl+Entercollapses to plainEnter— useEsc Enterinstead, or upgrade to Windows Terminal (it's free and installed by default on Windows 11).

`cmd.exe`
`Ctrl+Enter`
`Enter`
`Esc Enter`

## Running the gateway at Windows login​

hermes gateway installon Windows usesScheduled Taskswith a Startup-folder fallback — no admin required.

`hermes gateway install`

### Install​

```
hermes gateway install
```

What happens under the hood:

1. schtasks /Create /SC ONLOGON /RL LIMITED /TN HermesGateway— registers a task that runs at your login with standard (non-elevated) permissions. No UAC prompt.
2. If schtasks is blocked by group policy, falls back to writing astart /min cmd.exe /d /c <wrapper>shortcut into%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup. Same effect, slightly cruder.
3. Spawns the gatewaydetached viapythonw.exe— notpython.exe.pythonw.exehas no console attached, which immunizes it againstCTRL_C_EVENTbroadcasts from sibling processes (a real issue that used to kill the gateway when you Ctrl+C'd anything in the same process group).

`schtasks /Create /SC ONLOGON /RL LIMITED /TN HermesGateway`
`start /min cmd.exe /d /c <wrapper>`
`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`
`pythonw.exe`
`python.exe`
`pythonw.exe`
`CTRL_C_EVENT`

Flags used when spawning:DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW | CREATE_BREAKAWAY_FROM_JOB.

`DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW | CREATE_BREAKAWAY_FROM_JOB`

### Manage​

```
hermes gateway status      # Merged view: schtasks + Startup folder + running PIDhermes gateway start       # Starts the scheduled task nowhermes gateway stop        # Graceful SIGTERM equivalent (TerminateProcess via psutil)hermes gateway restarthermes gateway uninstall   # Removes schtasks entry, Startup shortcut, pid file
```

hermes gateway statusis idempotent — call it a thousand times in a row and it will never accidentally kill the gateway. (Pre-PR #21561 it silently did, viaos.kill(pid, 0)colliding withCTRL_C_EVENTat the C level — see "process management internals" below if you care about the story.)

`hermes gateway status`
`os.kill(pid, 0)`
`CTRL_C_EVENT`

### Why not a Windows Service?​

Services require admin rights to install and tie the gateway's lifecycle to machine boot, not user login. The typical Hermes user wants: log in → gateway available, log out → gateway gone. Scheduled Tasks do exactly that without elevation. If you genuinely want a service, usenssmorsc createmanually — but you probably don't.

`nssm`
`sc create`

## Data layout​

| Path | Contents |
| --- | --- |
| %LOCALAPPDATA%\hermes\hermes-agent\ | Git checkout + venv.venv\Scripts\hermes.exeis the command added to User PATH. Safe toRemove-Item -Recurseand reinstall. |
| %LOCALAPPDATA%\hermes\git\ | PortableGit (only if the installer provisioned it). |
| %LOCALAPPDATA%\hermes\node\ | Portable Node.js (only if the installer provisioned it). |
| %LOCALAPPDATA%\hermes\bin\ | Hermes's manageduv.exe(the Python manager it uses for updates). |
| %LOCALAPPDATA%\hermes\(root) | Your config, auth, skills, sessions, logs (config.yaml,.env,skills\,sessions\,logs\, …).Survives reinstalls. |

`%LOCALAPPDATA%\hermes\hermes-agent\`
`venv\Scripts\hermes.exe`
`Remove-Item -Recurse`
`%LOCALAPPDATA%\hermes\git\`
`%LOCALAPPDATA%\hermes\node\`
`%LOCALAPPDATA%\hermes\bin\`
`uv.exe`
`%LOCALAPPDATA%\hermes\`
`config.yaml`
`.env`
`skills\`
`sessions\`
`logs\`

On native Windows the installer setsHERMES_HOME=%LOCALAPPDATA%\hermes, so your data and the disposable install live under thesame%LOCALAPPDATA%\hermesroot: the install/runtime is thehermes-agent\,git\,node\, andbin\subdirectories, while your data files sit directly in%LOCALAPPDATA%\hermes. Reinstalling only replaces thehermes-agent\checkout, so your data survives — but because the two share a root,don'tRemove-Item -Recurse %LOCALAPPDATA%\hermesif you want to keep your data; delete thehermes-agent\subdirectory instead. Your data directory is identical in shape to a Linux~/.hermes, so you can mirror it between machines.

`HERMES_HOME=%LOCALAPPDATA%\hermes`
`%LOCALAPPDATA%\hermes`
`hermes-agent\`
`git\`
`node\`
`bin\`
`%LOCALAPPDATA%\hermes`
`hermes-agent\`
`Remove-Item -Recurse %LOCALAPPDATA%\hermes`
`hermes-agent\`
`~/.hermes`

OverrideHERMES_HOME:set the environment variable to point at a different data dir (e.g.%USERPROFILE%\.hermesto match a Linux/WSL layout). Works the same as on Linux.

`HERMES_HOME`
`%USERPROFILE%\.hermes`

## Browser tool​

The browser tool usesagent-browser(a Node helper) to drive Chromium. On Windows:

`agent-browser`
- The installer putsagent-browseron PATH via npm.
- shutil.which("agent-browser", path=...)picks up the.cmdshim automatically —CreateProcessWcan't execute an extensionless shebang, so Hermes always resolves to the.CMDwrapper. Don't manually invoke the shebang script; always go through the.cmd.
- Playwright Chromium is auto-installed on first run (npx playwright install chromium). If installation fails,hermes doctorsurfaces it with a fix-it hint.

`agent-browser`
`shutil.which("agent-browser", path=...)`
`.cmd`
`CreateProcessW`
`.CMD`
`.cmd`
`npx playwright install chromium`
`hermes doctor`

## Running Hermes on Windows — practical notes​

### PATH after install​

The installer adds%LOCALAPPDATA%\hermes\hermes-agent\venv\Scriptsto yourUser PATHvia[Environment]::SetEnvironmentVariable. Existing terminals don't pick this up — open a new PowerShell window (or Windows Terminal tab) after installation. Close-and-reopen, don't$env:PATH += …by hand unless you know what you're doing.

`%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts`
`[Environment]::SetEnvironmentVariable`
`$env:PATH += …`

Verify:

```
Get-Command hermes        # should print C:\Users\<you>\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exehermes --version
```

### Environment variables​

Hermes honors both$env:X(process-scope) and User environment variables (permanent, set in System Properties → Environment Variables). Setting API keys in%LOCALAPPDATA%\hermes\.env(yourHERMES_HOME) is the normal path — same as Linux:

`$env:X`
`%LOCALAPPDATA%\hermes\.env`
`HERMES_HOME`

```
OPENROUTER_API_KEY=sk-or-...TELEGRAM_BOT_TOKEN=...
```

Don't put secrets in User environment variables unless you specifically want every Windows process to see them (it isn't what you want).

### Windows-specific env vars​

These only affect native Windows installs:

| Variable | Effect |
| --- | --- |
| HERMES_GIT_BASH_PATH | Override bash.exe discovery. Point at any bash — full Git-for-Windows, WSL bash via symlink, MSYS2, Cygwin. The installer sets this automatically. |
| HERMES_DISABLE_WINDOWS_UTF8 | Set to1to disable the UTF-8 stdio shim and fall back to the locale code page. Useful for bisecting an encoding bug. |
| EDITOR/VISUAL | Your editor for/editandCtrl-X Ctrl-E. Hermes defaults tonotepadif both are unset. |

`HERMES_GIT_BASH_PATH`
`HERMES_DISABLE_WINDOWS_UTF8`
`1`
`EDITOR`
`VISUAL`
`/edit`
`Ctrl-X Ctrl-E`
`notepad`

## Uninstall​

From PowerShell:

```
hermes uninstall
```

That's the clean path — removes the schtasks entry, Startup folder shortcut,hermes.cmdshim, deletes%LOCALAPPDATA%\hermes\hermes-agent\, and trims the User PATH. It leaves the rest of%LOCALAPPDATA%\hermes\alone (your config, auth, skills, sessions, logs) in case you're reinstalling.

`hermes.cmd`
`%LOCALAPPDATA%\hermes\hermes-agent\`
`%LOCALAPPDATA%\hermes\`

To nuke everything:

```
hermes uninstallRemove-Item -Recurse -Force "$env:LOCALAPPDATA\hermes"# Also remove a legacy CLI/WSL data dir if you ever used one:Remove-Item -Recurse -Force "$env:USERPROFILE\.hermes"
```

Thehermes uninstallCLI subcommand also handles the case where the schtasks entry was registered under a different task name (older installs) — it searches by install path rather than by hardcoded task name.

`hermes uninstall`

## Process management internals​

This is background material — skip unless you're debugging an "it's killing itself" weirdness.

On Linux and macOS, the POSIX idiomos.kill(pid, 0)is a no-op permission check: "is this PID alive and can I signal it?" On Windows, Python'sos.killmapssig=0toCTRL_C_EVENT— they collide at integer value 0 — and routes it throughGenerateConsoleCtrlEvent(0, pid), which broadcasts Ctrl+C to theentire console process groupcontaining the target PID. That'sbpo-14484, open since 2012. It won't be fixed because changing it would break scripts that depend on the current behavior.

`os.kill(pid, 0)`
`os.kill`
`sig=0`
`CTRL_C_EVENT`
`GenerateConsoleCtrlEvent(0, pid)`
[bpo-14484](https://bugs.python.org/issue14484)

Consequence: any codepath that said "check if this PID is alive" viaos.kill(pid, 0)on Windows was silently killing the target. Hermes migrated every such site (14 across 11 files) togateway.status._pid_exists(), which usespsutil.pid_exists()(which in turn usesOpenProcess + GetExitCodeProcesson Windows — no signals). If you're writing a plugin or patch, usepsutil.pid_exists()directly orgateway.status._pid_exists()— neveros.kill(pid, 0).

`os.kill(pid, 0)`
`gateway.status._pid_exists()`
`psutil.pid_exists()`
`OpenProcess + GetExitCodeProcess`
`psutil.pid_exists()`
`gateway.status._pid_exists()`
`os.kill(pid, 0)`

scripts/check-windows-footguns.pyenforces this in CI: any newos.kill(pid, 0)call fails theWindows footguns (blocking)check unless the line carries a# windows-footgun: ok — <reason>marker.

`scripts/check-windows-footguns.py`
`os.kill(pid, 0)`
`Windows footguns (blocking)`
`# windows-footgun: ok — <reason>`

## Common pitfalls​

hermes: command not foundright after install.Open a new PowerShell window. The installer added%LOCALAPPDATA%\hermes\binto User PATH, but existing shells need to be restarted to pick it up. In the meantime you can run& "$env:LOCALAPPDATA\hermes\bin\hermes.cmd".

`hermes: command not found`
`%LOCALAPPDATA%\hermes\bin`
`& "$env:LOCALAPPDATA\hermes\bin\hermes.cmd"`

WinError 193: %1 is not a valid Win32 applicationwhen running a tool.You hit a shebang-script invocation that bypassed the.cmdshim. Hermes resolves commands throughshutil.which(cmd, path=local_bin)so PATHEXT picks up.CMD— if you're invoking the tool via a hardcoded path instead, switch to the.cmdvariant (e.g.,npx.cmd, notnpx).

`WinError 193: %1 is not a valid Win32 application`
`.cmd`
`shutil.which(cmd, path=local_bin)`
`.CMD`
`.cmd`
`npx.cmd`
`npx`

[scriptblock]::Create(...)fails withThe assignment expression is not valid.Your download ofinstall.ps1picked up a UTF-8 BOM. Theirm | iexform strips BOMs automatically;[scriptblock]::Create((irm ...))does not. Re-run with the simpleirm | iexform, or download the script manually and save it without a BOM via[IO.File]::WriteAllText($path, $text, (New-Object Text.UTF8Encoding $false)).

`[scriptblock]::Create(...)`
`The assignment expression is not valid`
`install.ps1`
`irm | iex`
`[scriptblock]::Create((irm ...))`
`irm | iex`
`[IO.File]::WriteAllText($path, $text, (New-Object Text.UTF8Encoding $false))`

Gateway won't stay running after restart.Checkhermes gateway status— it merges the schtasks entry, the Startup-folder shortcut (if used), and the live PID. If schtasks is registered but not running, group policy may be blockingONLOGONtriggers. Runschtasks /Query /TN HermesGateway /V /FO LISTto see the task's failure reason, or fall back to the Startup-folder path by uninstalling and reinstalling withHERMES_GATEWAY_FORCE_STARTUP=1.

`hermes gateway status`
`ONLOGON`
`schtasks /Query /TN HermesGateway /V /FO LIST`
`HERMES_GATEWAY_FORCE_STARTUP=1`

/editstill does nothing after setting$env:EDITOR.You set it in the current process only; close and reopen the shell, or set it at User scope in System Properties → Environment Variables. Verify withecho $env:EDITORin a new PowerShell window.

`/edit`
`$env:EDITOR`
`echo $env:EDITOR`

Browser tool launches but tools time out.Chromium is auto-installed on first run. If the install failed (rate-limited GitHub, Playwright CDN hiccup), runhermes doctor— it will surface the missing Chromium and print the exactnpx playwright install chromiumcommand to fix it.

`hermes doctor`
`npx playwright install chromium`

agent-browserfails with a weird Node version error.The installer provisions Node 22 at%LOCALAPPDATA%\hermes\nodebut your PATH may have an older system Node 18 first. Either move Hermes's node dir earlier on PATH, or delete the system install if you don't use Node elsewhere.

`agent-browser`
`%LOCALAPPDATA%\hermes\node`

Chinese / Japanese / Arabic characters show as?in the CLI.The UTF-8 stdio shim didn't activate. Check thatHERMES_DISABLE_WINDOWS_UTF8is NOT set (Get-ChildItem env:HERMES_DISABLE_WINDOWS_UTF8). If it's empty and you still see?, the console host (very oldcmd.exe) may not support UTF-8 at all — switch to Windows Terminal.

`?`
`HERMES_DISABLE_WINDOWS_UTF8`
`Get-ChildItem env:HERMES_DISABLE_WINDOWS_UTF8`
`?`
`cmd.exe`

Gateway can't send Telegram photos — "BadRequest: payload contains invalid characters".This is unrelated to Windows but sometimes surfaces first there. Usually it means your file path contains unescaped backslashes in a JSON body. Telegram should be receiving paths Hermes normalizes, not raw Windows paths — if you're seeing this inside a custom plugin, make sure you're passing the Hermes-provided path, notstr(Path(...))from user input.

`BadRequest: payload contains invalid characters`
`str(Path(...))`

"Works on my other machine" encoding weirdness aftergit pull.If you edited Hermes config or a skill on Windows using a non-UTF-8 editor (Notepad on older Windows versions, some Chinese IMEs), the file may have been saved with a BOM. Hermes toleratesutf-8-sigon most config reads, but a BOM inside a folded YAML scalar (description: >) silently breaks YAML parsing. Re-save the file as plain UTF-8 without BOM.

`git pull`
`utf-8-sig`
`description: >`

## Where to go next​

- Installation— the full install page, including Linux/macOS/WSL2/Termux.
- Windows (WSL2) Guide— if you want POSIX semantics or the dashboard terminal pane.
- CLI Reference— everyhermessubcommand.
- FAQ— common non-Windows-specific questions.
- Messaging Gateway— running Telegram/Discord/Slack on Windows.

[Installation](/docs/getting-started/installation)
[Windows (WSL2) Guide](/docs/user-guide/windows-wsl-quickstart)
[CLI Reference](/docs/reference/cli-commands)
`hermes`
[FAQ](/docs/reference/faq)
[Messaging Gateway](/docs/user-guide/messaging/)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/windows-native.md)