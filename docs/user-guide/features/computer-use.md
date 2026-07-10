---
layout: docs
title: "Features_Computer Use"
permalink: /docs/user-guide/features_computer-use/
---

- 
- Features
- Media & Web
- Computer Use

# Computer Use

Hermes Agent can drive your desktop — clicking, typing, scrolling,
dragging — in thebackgroundonmacOS, Windows, and Linux. Your
cursor doesn't move, keyboard focus doesn't change, and your virtual
desktops / Spaces don't switch on you. You and the agent co-work on the
same machine.

Unlike most computer-use integrations, this works withany tool-capable
model— Claude, GPT, Gemini, or an open model on a local
OpenAI-compatible endpoint. There's no Anthropic-native schema to worry
about.

## How it works​

Thecomputer_usetoolset speaks MCP over stdio tocua-driver, an open-source background
computer-use driver. Each platform uses the appropriate accessibility +
input stack under the hood:

`computer_use`
`cua-driver`
| Platform | Accessibility tree | Input dispatch |
| --- | --- | --- |
| macOS | AX (private SkyLight SPIs) | SLPSPostEventRecordTo— pid-scoped, no cursor warp |
| Windows | UIAutomation | SendInput+PostMessage— no focus steal |
| Linux | AT-SPI (X11 + Wayland) | XTest (X11) / virtual-keyboard (Wayland) |

`SLPSPostEventRecordTo`
`SendInput`
`PostMessage`

The result is the same on every platform: the agent can read the
accessibility tree of any visible window AND post synthesized events
without bringing it to front, switching virtual desktops, or moving the
real OS cursor.

For the underlying contract —whybackground mode matters, the
no-foreground invariant, click-dispatch internals — seecua.ai/docs/explanation/the-no-foreground-contract.

## Enabling​

Pick whichever path is most convenient — both run the same upstream
installer:

Option 1: dedicated CLI command (most direct).

```
hermes computer-use install
```

This fetches and runs the upstream cua-driver installer —install.shon macOS/Linux,install.ps1on Windows. Usehermes computer-use statusto verify the install.

`install.sh`
`install.ps1`
`hermes computer-use status`

Option 2: enable the toolset interactively.

1. Runhermes tools, pick🖱️  Computer Use (macOS/Windows/Linux).
2. The setup runs the upstream installer (same as Option 1).

`hermes tools`
`🖱️  Computer Use (macOS/Windows/Linux)`

After installing, regardless of which path you took, grant the
platform-appropriate prereqs:

| Platform | Prereqs |
| --- | --- |
| macOS | System Settings → Privacy & Security →Accessibility+Screen Recording→ allow your terminal (or Hermes app).hermes computer-use doctorwill tell you which permission is missing. |
| Windows | None at install time. If you're driving over SSH (not RDP / console), you need the autostart pattern — seecua.ai/docs/how-to-guides/driver/windows-sshfor the Session 0 ↔ Session 1+ proxy. |
| Linux | A reachable display server:DISPLAYset for X11, orXDG_SESSION_TYPE=wayland. Wayland sessions need an XWayland bridge for capture. AT-SPI must be on (default on GNOME/KDE/Xfce). |

`hermes computer-use doctor`
`DISPLAY`
`XDG_SESSION_TYPE=wayland`

Then start a session with the toolset enabled:

```
hermes -t computer_use chat
```

or addcomputer_useto your enabled toolsets in~/.hermes/config.yaml.

`computer_use`
`~/.hermes/config.yaml`

## hermes computer-use doctor— your first triage stop​

`hermes computer-use doctor`

hermes computer-use doctorruns cua-driver's structuredhealth_reportMCP tool and prints a per-check matrix. It's the single
fastest way to find outwhyan action isn't working.

`hermes computer-use doctor`
`health_report`

```
$ hermes computer-use doctor⚠️  cua-driver 0.5.8 on darwin — degraded  ✅ binary_version: cua-driver 0.5.8  ✅ platform_supported: macOS 26.4.1 (arm64)  ✅ session_active: MCP session is active.  ❌ bundle_identity: Process has no CFBundleIdentifier.      → Run the binary inside CuaDriver.app so TCC grants attribute correctly.  ✅ tcc_accessibility: Accessibility is granted.  ✅ tcc_screen_recording: Screen Recording is granted.  ✅ ax_capability: AX is trusted and reachable.  ✅ screen_capture_capability: ScreenCaptureKit reachable; 1 display(s) shareable.
```

- Exit code 0when overall isok— everything's wired up.
- Exit code 1whendegradedorfailed— at least one check failed; the hint on each failure tells you what to fix.
- Exit code 2when the cua-driver binary itself isn't reachable.

`ok`
`degraded`
`failed`

Useful flags:

- --include CHECK— run only the listed checks (repeat for multiple)
- --skip CHECK— skip a check (wins over--include)
- --json— emit the raw structured payload, same shape as thetools/call health_reportMCP response

`--include CHECK`
`--skip CHECK`
`--include`
`--json`
`tools/call health_report`

The check matrix is platform-aware:bundle_identity/tcc_*areskipon Windows + Linux because those concepts don't apply.ax_capabilitychecks AX on macOS, UIA on Windows, AT-SPI on Linux —
each with the right diagnostic hint when it can't reach.

`bundle_identity`
`tcc_*`
`skip`
`ax_capability`

## The agent cursor and sessions​

When the agent acts, you'll see atinted overlay cursorglide
across the screen to where each click / type / scroll lands. The real
OS cursor never moves — the overlay is a visual cue that says "the
agent is acting here." Each Hermes run declares its own cua-driversession id(something likehermes-3a7b9c14d2e8); the cursor's
identity is keyed to that session, so concurrent runs / subagents each
get their own cursor without stepping on each other.

`hermes-3a7b9c14d2e8`

Tune the cursor withcua-driver's CLI flags or the runtimeset_agent_cursor_styleMCP tool — seecua.ai/docs/how-to-guides/driver/personalize-cursorfor the full menu (built-inarrowvsteardropsilhouette, custom
SVG / PNG / ICO via--cursor-icon, runtime gradient colors, bloom
halo).

`cua-driver`
`set_agent_cursor_style`
`arrow`
`teardrop`
`--cursor-icon`

## Going deeper — the cua-driver skill pack​

Hermes intentionally keeps its skill (skills/computer-use/SKILL.md)
focused on the Hermes-sidecomputer_useaction vocabulary — the
single source of truth the agent loads. For the deeper material —
platform-specific deep dives, recording semantics, browser page
interaction — point your agent harness at the cua-driver skill pack
the cua-driver team ships and maintains directly:

`skills/computer-use/SKILL.md`
`computer_use`

```
cua-driver skills install
```

This symlinks the pack into your agent harness' skill directory. After
running it, an agent gets access to:

| File | Topic |
| --- | --- |
| SKILL.md | The cross-platform core (snapshot invariant, no-foreground contract, click dispatch, AX-tree mechanics) |
| MACOS.md | macOS specifics: no-foreground contract, AXMenuBar navigation, SkyLight click dispatch, Apple Events JS bridge |
| WINDOWS.md | Windows specifics: UIA tree, UWP /ApplicationFrameHosthosting, Session 0 isolation, autostart pattern |
| LINUX.md | Linux specifics: AT-SPI tree, X11 / Wayland, terminal-emulator detection |
| RECORDING.md | Trajectory + video recording semantics |
| WEB_APPS.md | Browser-page interaction tips |
| TESTS.md | Replay-by-trajectory workflow |

`SKILL.md`
`MACOS.md`
`WINDOWS.md`
`ApplicationFrameHost`
`LINUX.md`
`RECORDING.md`
`WEB_APPS.md`
`TESTS.md`

These areplatform deep dives, not duplicates of the Hermes skill—
when an agent reports "on Windows, my click landed on the wrong
element," it readsWINDOWS.mdfor the UIA / UWP context that
explains why and what to do differently.

`WINDOWS.md`

cua-driver skills statusshows what's installed and which agent
harnesses it's linked into. Today the autodetect list covers Claude
Code, Codex, OpenCode, OpenClaw, and Antigravity;Hermes
autodetection is planned as a follow-up intrycua/cua— until
then, runcua-driver skills installonce and point your harness at
the resulting~/.cua-driver/skills/cua-driverdirectory (or symlink
it into your usual skill space).

`cua-driver skills status`
`trycua/cua`
`cua-driver skills install`
`~/.cua-driver/skills/cua-driver`

## Quick example​

User prompt:"Find my latest email from Stripe and summarise what they want me to do."

The agent's plan (this is the same shape on macOS / Windows / Linux —
the model substitutes the platform's idiomatic shortcut and app name):

1. computer_use(action="capture", mode="som", app="Mail")— gets a
screenshot of the email app with every sidebar item, toolbar button,
and message row numbered.
2. computer_use(action="click", element=14)— clicks the search field.
3. computer_use(action="type", text="from:stripe")
4. computer_use(action="key", keys="return", capture_after=True)—
submit and get the new screenshot.
5. Click the top result, read the body, summarise.

`computer_use(action="capture", mode="som", app="Mail")`
`computer_use(action="click", element=14)`
`computer_use(action="type", text="from:stripe")`
`computer_use(action="key", keys="return", capture_after=True)`

During all of this, your cursor stays wherever you left it and the email
app never comes to front.

## Provider compatibility​

| Provider | Vision? | Works? | Notes |
| --- | --- | --- | --- |
| Anthropic (Claude Sonnet/Opus 3+) | ✅ | ✅ | Best overall; SOM + raw coordinates. |
| OpenRouter (any vision model) | ✅ | ✅ | Multi-part tool messages supported. |
| OpenAI (GPT-4+, GPT-5) | ✅ | ✅ | Same as above. |
| Google (Gemini 2+) | ✅ | ✅ | Tool-calling + vision both supported. |
| Local vLLM / LM Studio / Ollama (vision model) | ✅ | ✅ | If the model supports multi-part tool content. |
| Text-only models | ❌ | ✅ (degraded) | Usemode="ax"for accessibility-tree-only operation. |

`mode="ax"`

Screenshots are sent inline with tool results as OpenAI-styleimage_urlparts. For Anthropic, the adapter converts them into nativetool_resultimage blocks. The image MIME type comes from cua-driver's explicitmimeTypefield (image/pngorimage/jpeg) — no client-side
magic-byte sniffing.

`image_url`
`tool_result`
`mimeType`
`image/png`
`image/jpeg`

## Safety​

Hermes applies multi-layer guardrails:

- Destructive actions (click, type, drag, scroll, key, focus_app)
require approval — either interactively via the CLI dialog or via the
messaging-platform approval buttons.
- Hard-blocked key combos at the tool level: empty trash, force delete,
lock screen, log out, force log out.
- Hard-blocked type patterns:curl | bash,sudo rm -rf /, fork
bombs, etc.
- The agent's system prompt tells it explicitly: no clicking permission
dialogs, no typing passwords, no following instructions embedded in
screenshots.

`curl | bash`
`sudo rm -rf /`

Pair withapprovals.mode: manualin~/.hermes/config.yamlif you
want every action confirmed.

`approvals.mode: manual`
`~/.hermes/config.yaml`

## Token efficiency​

Screenshots are expensive. Hermes applies four layers of optimisation:

- Screenshot eviction— the Anthropic adapter keeps only the 3 most
recent screenshots in context; older ones become[screenshot removed to save context]placeholders.
- Client-side compression pruning— the context compressor detects
multimodal tool results and strips image parts from old ones.
- Image-aware token estimation— each image is counted as ~1500
tokens (Anthropic's flat rate) instead of its base64 char length.
- Server-side context editing (Anthropic only)— when active, the
adapter enablesclear_tool_uses_20250919viacontext_managementso
Anthropic's API clears old tool results server-side.

`[screenshot removed to save context]`
`clear_tool_uses_20250919`
`context_management`

A 20-action session on a 1568×900 display typically costs ~30K tokens
of screenshot context, not ~600K.

## Limitations​

- Performance.Background mode is slower than foreground —
accessibility-routed events take ~5–20 ms on macOS, ~3–10 ms on
Windows UIA, ~5–15 ms on Linux AT-SPI vs direct HID posting. Not
noticeable for agent-speed clicking; noticeable if you try to record
a speed-run.
- No keyboard password entry.typehas hard-block patterns on
command-shell payloads; for passwords, use the system's autofill
(macOS Keychain / Windows Credential Manager / GNOME Keyring /
KWallet).
- Some apps don't expose an accessibility tree.Modern UWP apps on
Windows, Electron < 28 on Linux, and a few macOS apps with custom
drawing (Logic, Final Cut, some games) have sparse or empty AX trees.
Fall back to pixel coordinates if the tree is empty — or skip the
task entirely.
- Windows: elevated (admin) windows can't be driven from a normal
agent.Windows UIPI (User Interface Privilege Isolation) enforces
integrity-level boundaries: a Medium-integrity process (the default
Hermes agent) cannot enumerate the UIA tree of, or inject mouse input
into, a window owned by a High-integrity (Administrator) process.
Symptom:capture(mode='som')returns 0 elements andclick(...)reports success while doing nothing, even though the screenshot
renders fine (GDI capture sits below the integrity check). Keyboard
events partially bypass UIPI, so Tab / Enter can still navigate an
elevated dialog. This is an OS constraint, not a cua-driver bug — it
affects every Windows automation stack. To drive elevated windows,
run the Hermes agent itself at High integrity (launch from an
elevated terminal); otherwise target non-elevated windows.
- Platform-specific deployment gotchas:macOSuses private SkyLight SPIs. Apple can change them in any
OS update. Hermes warns when the installed cua-driver is older than
the version it was tested against.WindowsSSH sessions run inSession 0, which has no
interactive desktop. Drive Hermes from inside the RDP / console
session, or set up cua-driver's autostart Scheduled Task —windows-sshhas the recipe.Linuxrequires a reachable display server. Headless servers
need Xvfb (Xvfb :99 -screen 0 1920x1080x24) beforecomputer_usecan capture or inject events. Pure Wayland sessions
need an XWayland bridge for screen capture (cua-driver's Wayland
inject path handles input independently).

`type`
`capture(mode='som')`
`click(...)`
- macOSuses private SkyLight SPIs. Apple can change them in any
OS update. Hermes warns when the installed cua-driver is older than
the version it was tested against.
- WindowsSSH sessions run inSession 0, which has no
interactive desktop. Drive Hermes from inside the RDP / console
session, or set up cua-driver's autostart Scheduled Task —windows-sshhas the recipe.
- Linuxrequires a reachable display server. Headless servers
need Xvfb (Xvfb :99 -screen 0 1920x1080x24) beforecomputer_usecan capture or inject events. Pure Wayland sessions
need an XWayland bridge for screen capture (cua-driver's Wayland
inject path handles input independently).

`Xvfb :99 -screen 0 1920x1080x24`
`computer_use`

For cross-platform GUI automation without the desktop overhead (and
without TCC / Session 0 / X11 setup), thebrowsertoolset uses a
real headless Chromium and is the right answer for web-only tasks.

`browser`

## Configuration​

Override the driver binary path (tests / CI / local builds):

```
HERMES_CUA_DRIVER_CMD=/path/to/your/cua-driver
```

Swap the backend entirely (for testing):

```
HERMES_COMPUTER_USE_BACKEND=noop   # records calls, no side effects
```

### Telemetry​

cua-driver ships with anonymous usage telemetry (PostHog) enabled by default
upstream.Hermes disables it for you— on every cua-driver invocation
(the MCP backend,status,doctor, and install) Hermes setsCUA_DRIVER_RS_TELEMETRY_ENABLED=0in the driver's environment.

`status`
`doctor`
`CUA_DRIVER_RS_TELEMETRY_ENABLED=0`

To opt back in (let cua-driver use its own default and send telemetry), set
this inconfig.yaml:

`config.yaml`

```
computer_use:  cua_telemetry: true   # default: false (telemetry off)
```

When it's on,hermes computer-use doctorreportstelemetry: enabled;
when off (the default), it reportstelemetry: disabled via CUA_DRIVER_RS_TELEMETRY_ENABLED.

`hermes computer-use doctor`
`telemetry: enabled`
`telemetry: disabled via CUA_DRIVER_RS_TELEMETRY_ENABLED`

## Testing against a local cua-driver build​

When you're developing cua-driver itself — or want to test an
unreleased fix — point Hermes at a binary you built from source instead
of the published release. Hermes resolves the driver withshutil.which("cua-driver")anddoes not enforceHERMES_CUA_DRIVER_VERSION, so a local build (reported as0.0.0-local-*) is accepted as-is. Two approaches:

`shutil.which("cua-driver")`
`HERMES_CUA_DRIVER_VERSION`
`0.0.0-local-*`

### Option A —install-local(build + put it on PATH)​

`install-local`

From yourtrycua/cuacheckout, run the upstream local installer. It
builds the Rust backend in release mode and dropscua-driverinto the
same install layout the production installer uses, adding its bin dir
to your PATH:

`trycua/cua`
`cua-driver`

```
# Windows (PowerShell), from the cua repo root./libs/cua-driver/scripts/install-local.ps1 -NoAutoStart
```

```
# macOS / Linux, from the cua repo root  (defaults to a debug build without --release)./libs/cua-driver/scripts/install-local.sh --release
```

- Windows stages the build under%USERPROFILE%\.cua-driver\packages\…and junctions%LOCALAPPDATA%\Programs\Cua\cua-driver\bin(added to your User
PATH) to it. macOS/Linux symlinkscua-driverinto~/.local/bin(override with--bin-dir <path>).
- -NoAutoStartskips registering thecua-driver-servelogon daemon
— you don't need it for Hermes testing (see notes).

`%USERPROFILE%\.cua-driver\packages\…`
`%LOCALAPPDATA%\Programs\Cua\cua-driver\bin`
`cua-driver`
`~/.local/bin`
`--bin-dir <path>`
`-NoAutoStart`
`cua-driver-serve`

Then open a fresh shell (so the PATH change is visible) and confirm:

```
cua-driver --version                 # local builds report 0.0.0-local-release# Windows:      (Get-Command cua-driver).Source# macOS/Linux:  which cua-driver
```

### Option B — point Hermes straight at the built binary (fastest loop)​

Skip the install ceremony entirely:cargo buildand setHERMES_CUA_DRIVER_CMDto the resulting binary. Best for rapid
edit/build/test.

`cargo build`
`HERMES_CUA_DRIVER_CMD`

```
cargo build -p cua-driver            # add --release for a release build; run from libs/cua-driver/rust
```

```
# Windows (.env)HERMES_CUA_DRIVER_CMD=C:\path\to\cua\libs\cua-driver\rust\target\debug\cua-driver.exe# macOS / Linux (.env)HERMES_CUA_DRIVER_CMD=/path/to/cua/libs/cua-driver/rust/target/debug/cua-driver
```

### Confirm Hermes is using your build​

- hermes computer-use statusprints the resolved binary path and
version.
- hermes computer-use doctorconfirms the binary is reachable and
exercises the full MCP path end-to-end.
- In a session,computer_use(action="capture")exercises the spawnedcua-driver mcpchild process.

`hermes computer-use status`
`hermes computer-use doctor`
`computer_use(action="capture")`
`cua-driver mcp`

### Notes & gotchas​

- Hermes spawns its owncua-driver mcpchild over stdio— it doesnotattach to the long-runningcua-driver serveautostart daemon
or its named pipe. So the scheduled task / LaunchAgent is unnecessary
for testing (-NoAutoStartis fine). The autostart daemon and the
Windows UIAccess worker (cua-driver-uia.exe) only matter for
foreground-safe input on some apps (e.g. WPF); the standard tool
surface works through the stdio child. On Windows SSH sessions, the
autostart pattern IS needed — see the Limitations section.
- Locked binary on Windows.A runningcua-driver-servedaemon can
holdcua-driver.exeand block an overwrite on rebuild.install-local.ps1renames the locked binary out of the way
automatically; if youcargo buildmanually (Option B), stop it
first withcua-driver autostart disable(orschtasks /End /TN cua-driver-serve).
- Rebuild loop.After editing cua-driver source, re-runinstall-local(rebuilds, restages, flips thecurrentjunction)
for Option A, or just re-cargo buildfor Option B — no Hermes
change needed either way.
- Local builds skip the version check.Hermes warns when the
installed cua-driver is older than its per-OS tested baseline, but
exempts0.0.0-local-*dev builds — so your local build never
triggers that warning.

`cua-driver mcp`
`cua-driver serve`
`-NoAutoStart`
`cua-driver-uia.exe`
`cua-driver-serve`
`cua-driver.exe`
`install-local.ps1`
`cargo build`
`cua-driver autostart disable`
`schtasks /End /TN cua-driver-serve`
`install-local`
`current`
`cargo build`
`0.0.0-local-*`

## Troubleshooting​

First action when anything's off: runhermes computer-use doctor.The structured per-check matrix tells you (and any agent helping you
debug) exactly what's wrong.

`hermes computer-use doctor`

Specific failure modes the doctor doesn't catch:

computer_use backend unavailable: cua-driver is not installed—
Runhermes computer-use installto fetch the cua-driver binary, or
runhermes toolsand enable the Computer Use toolset.

`computer_use backend unavailable: cua-driver is not installed`
`hermes computer-use install`
`hermes tools`

Clicks seem to have no effect— Capture and verify. A modal you
didn't see may be blocking input. Dismiss it withescapeor the close
button.

`escape`

Element indices are stale— SOM indices are only valid until the
nextcapture. Re-capture after any state-changing action. The
wrapper carries opaqueelement_tokens for stale detection — you'll
see an explicit error rather than a wrong click.

`capture`
`element_token`

"blocked pattern in type text"— The text you tried totypematches the dangerous-shell-pattern list. Break the command up or
reconsider.

`type`

Empty captures on Linux—DISPLAYnot set, or you're on pure
Wayland without an XWayland bridge.hermes computer-use doctorwill
flag this asax_capability: failwith aSet DISPLAY (X11)…hint.

`DISPLAY`
`hermes computer-use doctor`
`ax_capability: fail`
`Set DISPLAY (X11)…`

Empty captures on Windows over SSH— You're in Session 0 (the
services session). Drive from RDP / console directly, or set up the
autostart pattern — seecua.ai/docs/how-to-guides/driver/windows-ssh.

## See also​

- Hermes-side skill—skills/computer-use/SKILL.md— teaches the
Hermescomputer_useaction vocabulary; this is what the agent loads.
- cua-driver skill pack— for platform-specific deep dives
(macOS no-foreground contract, Windows UIA + Session 0, Linux AT-SPIX11/Wayland, recording, browser pages), runcua-driver skills installand readMACOS.md/WINDOWS.md/LINUX.md/RECORDING.md/WEB_APPS.md. Oncecua-driver skills installautodetects Hermes (planned follow-up), this happens
automatically on install.
- cua.ai/docs— the cua-driver project's documentation:What is computer use?— concept introThe no-foreground contract—whybackground mode mattersInstall reference— cross-platform install detailsPersonalize the agent cursor— built-in shapes, custom assets, runtime overridesDrive Windows over SSH— the Session 0 → Session 1+ autostart patternKeep cua-driver running— autostart / daemon lifecycleConnect your agent— register cua-driver with various harnesses (Hermes among them)
- cua-driver source (trycua/cua)
- Browser automationfor cross-platform web tasks where you don't need to drive native apps.

`skills/computer-use/SKILL.md`
`computer_use`
- X11/Wayland, recording, browser pages), runcua-driver skills installand readMACOS.md/WINDOWS.md/LINUX.md/RECORDING.md/WEB_APPS.md. Oncecua-driver skills installautodetects Hermes (planned follow-up), this happens
automatically on install.

`cua-driver skills install`
`MACOS.md`
`WINDOWS.md`
`LINUX.md`
`RECORDING.md`
`WEB_APPS.md`
`cua-driver skills install`
- What is computer use?— concept intro
- The no-foreground contract—whybackground mode matters
- Install reference— cross-platform install details
- Personalize the agent cursor— built-in shapes, custom assets, runtime overrides
- Drive Windows over SSH— the Session 0 → Session 1+ autostart pattern
- Keep cua-driver running— autostart / daemon lifecycle
- Connect your agent— register cua-driver with various harnesses (Hermes among them)