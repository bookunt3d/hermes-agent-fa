---
layout: docs
title: "اپلیکیشن دسکتاپ"
permalink: /user-guide/desktop/
---

- 
- Using Hermes
- Desktop App

# Desktop App

The Hermes desktop app is a native app built around thesameagent you get from the CLI and the gateway — same config, same API keys, same sessions, same skills, same memory. It is not a separate product or a lightweight clone; it uses the same Hermes Agent core and settings, and drives it through a modern & thoughtfully designed UI. If you have usedhermesin a terminal, everything you set up there is already here, and anything you do here shows up there.

`hermes`

It runs onmacOS, Windows, and Linux.

Hermes has several front ends that all talk to the same agent:

- Desktop App(this page) — a native application with a purpose-built UI for chat, configuration, and management.
- CLI(hermes) andTUI(hermes --tui) — terminal interfaces.
- Web Dashboard(hermes dashboard) — a browser admin panel; its optionalChattab embeds the TUI through a pseudo-terminal.

`hermes`
[TUI](/docs/user-guide/tui)
`hermes --tui`
[Web Dashboard](/docs/user-guide/features/web-dashboard)
`hermes dashboard`

Pick whichever fits the moment. They share state, so you can start a session in one and resume it in another.

## Install​

Follow theinstallation instructions for Hermes Desktop.

[installation instructions for Hermes Desktop](/docs/getting-started/installation)

If you already have Hermes installed, simply run

```
hermes desktop
```

That uses your current config, keys, sessions, and skills.

## What's in the app​

The desktop app is organized as a chat-first window with a left sidebar for navigation. It's built to allow managing multiple simultaneous agent conversations, configuring messaging providers, creating artifacts, browsing projects' folder structures, and working on multiple projects at once.

### Chat​

The center of the app. You get:

- Streaming responseswith live tool activity and structured tool-call summaries as the agent works.
- The same conversation historyas every other Hermes surface — sessions started here resume in the CLI/TUI and vice versa.
- Drag-and-drop filesanywhere in the chat area to attach them to your next message.
- A right-hand preview rail— render web pages, files, and tool outputs side by side while you keep chatting.
- Composer history and queue editing— press the up/down arrow keys in an empty composer to recall and reuse previous prompts, and edit messages you've queued up before they're sent.

#### Status bar​

The bar along the bottom of the chat shows live session state and exposes quick controls without opening Settings:

- Per-session YOLO toggle— flip YOLO on or off for just this session (matching the TUI). YOLO bypasses the dangerous-command approval prompts, so know what you're turning off — seeSecurity → YOLO Mode.

[Security → YOLO Mode](/docs/user-guide/security#yolo-mode)

Chatting against a Hermes instance on another machine instead of the bundled local backend? SeeConnecting to a remote backendbelow — and for the full picture of how the remote-hosted dashboard connection works (the auth gate, the/api/wschat socket, and WebSocket close-code triage), seeWeb Dashboard → Connecting Hermes Desktop to a remote backend.

`/api/ws`
[Web Dashboard → Connecting Hermes Desktop to a remote backend](/docs/user-guide/features/web-dashboard#connecting-hermes-desktop-to-a-remote-backend)

#### Choosing a model​

The model picker lives in thecomposer, just left of the microphone. Click it to switch the model, reasoning effort, and fast mode from one dropdown.

- The composer picker is sticky UI state and never touches your default.It's remembered locally (per device) andfollowsacross new chats and restarts instead of snapping back to the default — pick a model once and the nextCmd/Ctrl+Nopens on it. With a live chat, switching models scopes the change to thatcurrent chat; either way the selection rides along when the session is created/switched and isneverwritten to the profile default. (Switchingprofilesreseeds to that profile's own default.)
- Set the default in Settings → Model.That "main" model is yourper-profile global default— it's what new chats, crons, subagents, and auxiliary tasks start from, and it's the only place that writes it. Eachprofilekeeps its own default.
- Per-model effort/fast presets.Each model remembers its own reasoning effort and fast-mode choice in the desktop app, re-applied to the session whenever you pick that model. These presets are a desktop convenience and don't change crons or subagents.
- Mid-chat switches reset the prompt cache.Switching the model inside a live chat means the next message re-reads the whole conversation at full input price (provider prompt caches are keyed to the model). Fine occasionally; on a long chat, a fresh chat on the new model is often cheaper than bouncing back and forth.

`Cmd/Ctrl+N`

### File browser​

Explore and preview the working directory without leaving the app — useful for following along as the agent reads, writes, and edits files. Set the initial project directory withhermes desktop --cwd <path>(or theHERMES_DESKTOP_CWDenvironment variable).

`hermes desktop --cwd <path>`
`HERMES_DESKTOP_CWD`

### Voice​

Talk to Hermes and hear it back, the samevoice modeavailable elsewhere. On macOS the OS will prompt once for microphone access.

[voice mode](/docs/user-guide/features/voice-mode)

### Settings & onboarding​

Manage providers, models, tools, and credentials from a real UI instead of editing YAML. First-run onboarding gets you to your first message in seconds. The settings panes cover providers/keys, model selection, toolset configuration, MCP servers, the gateway, and session management.

- Providers settings pane— a dedicated place to manage inference providers, with an Accounts / API-keys UX for signing in and storing credentials per provider.
- Every provider and model in the menus— the GUI surfaces the full provider list and every model thathermes modelknows about, so you pick from the same catalog the CLI sees rather than a curated subset.
- xAI Grok OAuth— Grok is a first-class OAuth provider in the launcher; sign in through the browser flow like the other OAuth providers.
- Tool-backend installs from the GUI— run a tool backend's post-setup install steps directly from the app instead of dropping to a terminal.
- Auxiliary-model warning— if you switch the main model to a new provider while auxiliary tasks (titling, summarization, and similar helpers) are still pinned to another provider, the app warns you so you don't unknowingly split work across two providers.

`hermes model`

First-run onboarding has been redesigned on a unified overlay design system, and you can pickChoose provider laterto skip provider setup and get into the app first.

### Management panes​

The app also surfaces the broader Hermes management surface so you don't have to drop to a terminal:

- Skills— browse, install, and manageskills.
- Cron— view and managescheduled jobs.
- Profiles— switch betweenHermes profiles(isolated config/skills/sessions).
- Messaging— set up gateway channels.
- AgentsandCommand Center— orchestration surfaces for multi-agent work.

[skills](/docs/user-guide/features/skills)
[scheduled jobs](/docs/reference/cli-commands#hermes-cron)
[Hermes profiles](/docs/user-guide/profiles)

### Keyboard & navigation​

- Command palette— pressCmd+K(Ctrl+K on Windows/Linux) to jump to actions and navigate the app from the keyboard.
- Rebindable shortcuts— a shortcuts panel in Settings lets you remap the app's keyboard shortcuts to your own keys.
- Custom zoom shortcuts— zoom the interface in half-step increments for finer control over text size.
- UI language switcher— change the app's interface language in-app, including Simplified Chinese (zh-Hans).

### Sessions & profiles​

- Session-list overhaul— a reworked session list with archiving and general session hygiene to keep the list manageable as it grows.
- Search sessions by id— find a specific session directly by its id.
- Concurrent multi-profile sessions— run sessions across multipleprofilesat the same time, and reference a session in another profile with cross-profile@sessionlinks.

[profiles](/docs/user-guide/profiles)
`@session`

## Updating​

The app checks for updates in the background and offers a one-click update when one is ready.

Themanual update processalso works with the GUI.

[manual update process](https://hermes-agent.nousresearch.com/docs/getting-started/updating)

## Uninstalling​

OpenSettings → About → Danger zoneand pick how much to remove:

- Uninstall Chat GUI only— removes the desktop app and its data; the Hermes agent, your config, and your chats stay. (Same ashermes uninstall --gui.)
- Uninstall GUI + agent, keep my data— removes the app and the agent but keeps config, chats, and secrets for a future reinstall. (Same ashermes uninstall.)
- Uninstall everything— removes the app, the agent, and all user data. (Same ashermes uninstall --full.)

`hermes uninstall --gui`
`hermes uninstall`
`hermes uninstall --full`

The app closes to finish the job (the cleanup runs after it exits so it can remove the running app bundle and its own venv). The agent-removing options are hidden automatically when no local agent is installed (for example, a GUI-only "lite" client connected to a remote backend).

You can do the same from the terminal —hermes uninstall --guifor the GUI alone, orhermes uninstall/hermes uninstall --fullfor the agent too.

`hermes uninstall --gui`
`hermes uninstall`
`hermes uninstall --full`

Runninghermes uninstall --guifrom asource checkout(ahermes desktopdev build) also removes the workspacenode_modulesandapps/desktop/{dist,release}build output, since those are GUI build artifacts. They're recoverable withhermes desktop(ornpm install+ a rebuild) — but if you're actively hacking on the desktop app, expect to reinstall dependencies afterward.

`hermes uninstall --gui`
`hermes desktop`
`node_modules`
`apps/desktop/{dist,release}`
`hermes desktop`
`npm install`

## CLI reference:hermes desktop​

`hermes desktop`

To launch via the CLI, simply runhermes desktop. By default it installs workspace Node dependencies, builds the current OS's unpacked Electron app, then launches that packaged artifact.

`hermes desktop`

| Flag | Description |
| --- | --- |
| --skip-build | Skip npm install/package and launch the existing unpacked app fromapps/desktop/release |
| --force-build | Force a full rebuild even if the content stamp matches |
| --build-only | Build the desktop app but do not launch it (used byhermes update) |
| --source | Launch viaelectron .againstapps/desktop/distinstead of the packaged app |
| --cwd PATH | Initial project directory for desktop chat sessions (setsHERMES_DESKTOP_CWD) |
| --hermes-root PATH | Override the Hermes source root the app uses (setsHERMES_DESKTOP_HERMES_ROOT) |
| --ignore-existing | Force the app to ignore anyhermesCLI already onPATHduring backend resolution |
| --fake-boot | Enable deterministic boot delays for validating the startup UI |

`--skip-build`
`apps/desktop/release`
`--force-build`
`--build-only`
`hermes update`
`--source`
`electron .`
`apps/desktop/dist`
`--cwd PATH`
`HERMES_DESKTOP_CWD`
`--hermes-root PATH`
`HERMES_DESKTOP_HERMES_ROOT`
`--ignore-existing`
`hermes`
`PATH`
`--fake-boot`

## How it works​

The packaged app ships the Electron shell and a native React chat surface. On first launch it can install the Hermes Agent runtime intoHERMES_HOME(~/.hermes, or%LOCALAPPDATA%\hermeson Windows) —the same layout a CLI install uses, which is why the two are interchangeable. Backend resolution first honoursHERMES_DESKTOP_HERMES_ROOT, then a completed managed install, then a probedhermesonPATH(unless--ignore-existing/HERMES_DESKTOP_IGNORE_EXISTING=1is set), and finally an explicitHERMES_DESKTOP_HERMEScommand override for packagers such as Nix. The React renderer talks to a headless backend the app launches for you — ahermes serveprocess that serves thetui_gatewayJSON-RPC/WebSocket API — and reuses the agent runtime rather than embeddinghermes --tui. The desktop app isself-contained: it runs its ownhermes servebackend and never opens or requires theweb dashboard. (Runtimes older than theservecommand fall back to a headlessdashboard --no-openautomatically, so an app update never outruns its backend.) Install, backend-resolution, and self-update logic live in the Electron main process.

`HERMES_HOME`
`~/.hermes`
`%LOCALAPPDATA%\hermes`
`HERMES_DESKTOP_HERMES_ROOT`
`hermes`
`PATH`
`--ignore-existing`
`HERMES_DESKTOP_IGNORE_EXISTING=1`
`HERMES_DESKTOP_HERMES`
`hermes serve`
`tui_gateway`
`hermes --tui`
`hermes serve`
[web dashboard](/docs/user-guide/features/web-dashboard)
`serve`
`dashboard --no-open`

## Connecting to a remote backend​

By default the app starts and manages its ownlocalbackend. You can instead point it at a Hermes backend running on another machine — a VPS, a home server, or a Mini behind Tailscale.

`hermes serve`

"Remote backend" means ahermes serveserver running on the remote machine — that is the process the desktop app connects to. Nothing in this section works unless that backend is actually up and reachable. The desktop app does not start it for you; you (or asystemdservice) keephermes serverunning on the remote host, and the app attaches to it. If you also use messaging channels (Telegram, Discord, etc.), thegatewayis aseparatelong-running process you start independently — see the note after the setup steps.

`hermes serve`
`systemd`
`hermes serve`

The connection has two halves: on the backend you protect it with anauth provider, and in the app you enter the backend's URL and sign in. Binding the backend to a non-loopback address automatically engages its auth gate, and the provider you configure is what lets the desktop app through.

Pick a provider based on where the backend lives:

- OAuth (Nous Portal) — preferred for anything reachable beyond your own machine.Logins are verified against your Nous account, so this is the option suitable for a VPS, a public host, or any remote backend. Register the dashboard withhermes dashboard register(or the Portal/local-dashboardspage) to provision its OAuth client, then sign in from the app withSign in with Nous Research. A self-hosted OIDC provider works the same way if you run your own identity provider.
- Username/password — local / trusted-network use only.The simplest option when the backend is on the same trusted LAN or reachable only over a VPN (e.g. Tailscale). It protects a single shared credential with no external identity provider, sodo not use it for a dashboard exposed to the public internet— reach for OAuth there instead.

`hermes dashboard register`
[/local-dashboards](https://portal.nousresearch.com/local-dashboards)
`/local-dashboards`

The rest of this section shows the username/password path because it's the quickest to stand up on a trusted network; for the OAuth path seeWeb Dashboard → Default provider: Nous Research.

[Web Dashboard → Default provider: Nous Research](/docs/user-guide/features/web-dashboard#default-provider-nous-research)

### On the backend (the remote machine)​

Set a username and password, then start the backend bound to a reachable address. The credentials live in~/.hermes/.env(the secrets file, mode 0600):

`~/.hermes/.env`

```
# 1. Set the dashboard login credentials.cat >> ~/.hermes/.env <<'EOF'HERMES_DASHBOARD_BASIC_AUTH_USERNAME=adminHERMES_DASHBOARD_BASIC_AUTH_PASSWORD=choose-a-strong-password# Recommended: a stable signing secret so sessions survive restarts.# Without it a random key is generated per boot and you'll be logged out# on every restart.HERMES_DASHBOARD_BASIC_AUTH_SECRET=$(openssl rand -base64 32)EOFchmod 600 ~/.hermes/.env# 2. Run the backend bound to a reachable address. The non-loopback bind#    engages the auth gate; the username/password provider handles login.hermes serve --host 0.0.0.0 --port 9119
```

Keep thathermes serveprocess running for as long as you want the desktop app to be able to connect — if it stops, the app can no longer reach the backend. Run it undersystemd,tmux, or your process manager of choice so it survives logout and reboots.

`hermes serve`
`systemd`
`tmux`

Separately, make sure thegateway is runningon the remote host if you rely on messaging channels — thehermes servebackend is what the desktop app talks to, but your Telegram/Discord/Slack gateway sessions are a different process that you start and keep running on their own. SeeMessagingfor gateway setup.

`hermes serve`
[Messaging](/docs/user-guide/messaging/)

Prefer not to keep a plaintext password at rest? SetHERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASHto a scrypt hash instead — compute it withpython -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('PW'))". Full configuration surface (config.yaml keys, every env var, the rate limiter):Web Dashboard → Username/password provider.

`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH`
`python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('PW'))"`
[Web Dashboard → Username/password provider](/docs/user-guide/features/web-dashboard#usernamepassword-provider-no-oauth-idp)

Running the backend as a systemd service? Give the unitEnvironmentFile=%h/.hermes/.envso the credentials are in the environment at boot.

`EnvironmentFile=%h/.hermes/.env`

The backend reads and writes your.env(API keys, secrets) and can run agent commands. Theusername/passwordsetup shown above is for a trusted network — never expose a password-protected backend directly to the open internet; put it behind a VPN.Tailscaleis the clean option: bind to the machine's tailscale IP (--host <tailscale-ip>) and usehttp://<tailscale-ip>:9119as the Remote URL so only your tailnet can reach it. To reach a backend over the public internet, use theOAuth (Nous Portal)provider instead.

`.env`
[Tailscale](https://tailscale.com/)
`--host <tailscale-ip>`
`http://<tailscale-ip>:9119`

### In the app​

Settings → Gateway → Remote gateway:

1. Remote URL—http://<backend-host>:9119(path prefixes like/hermeswork if you front it with a reverse proxy)
2. Sign in— the app detects which provider the backend advertises and adapts the button. For a username/password backend it shows aSign inbutton that opens a credential form (enter the credentials from step 1). For an OAuth backend it showsSign in with<provider>(e.g.Sign in with Nous Research), which runs the provider's browser sign-in. Either way the app ends up with an authenticated session against the backend.
3. Save and reconnect— switches the desktop shell onto the remote backend. The session refreshes automatically; you stay signed in across restarts whenHERMES_DASHBOARD_BASIC_AUTH_SECRETis set.

`http://<backend-host>:9119`
`/hermes`
`<provider>`
`HERMES_DASHBOARD_BASIC_AUTH_SECRET`

You can also set the backend URL without the UI via theHERMES_DESKTOP_REMOTE_URLenvironment variable before launching the app (it overrides the in-app setting); you still sign in from the Gateway settings panel.

`HERMES_DESKTOP_REMOTE_URL`

The remote gateway host is configured perprofile, so each profile can point at its own remote backend (or stay on its local one). Switching profiles switches which remote host the app connects to.

[profile](/docs/user-guide/profiles)

### Troubleshooting​

- Sign-in fails with 401 / "Invalid credentials"— the username or password doesn't match the backend'sHERMES_DASHBOARD_BASIC_AUTH_USERNAME/HERMES_DASHBOARD_BASIC_AUTH_PASSWORD. The backend returns the same generic error for an unknown user and a wrong password (no enumeration oracle), so double-check both. Confirm the gate is on withcurl -s http://<host>:9119/api/status | jq '.auth_required, .auth_providers'— it should reporttrueand include"basic".
- No "Sign in" button — it asks for a session token instead— the backend's username/password provider isn't active./api/statuswon't list"basic"inauth_providers. Make sure both the username and a password (or password hash) are set in~/.hermes/.envand that the dashboard process actually loaded them.
- Signed out on every restart— setHERMES_DASHBOARD_BASIC_AUTH_SECRETto a stable value. Without it the token-signing key is regenerated per boot, invalidating all sessions.
- Connection refused / times out— the backend bound to127.0.0.1(the default) or a firewall/VPN is blocking the port. Bind to0.0.0.0or the tailscale IP and open the port to your trusted network.

`HERMES_DASHBOARD_BASIC_AUTH_USERNAME`
`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`
`curl -s http://<host>:9119/api/status | jq '.auth_required, .auth_providers'`
`true`
`"basic"`
`/api/status`
`"basic"`
`auth_providers`
`~/.hermes/.env`
`HERMES_DASHBOARD_BASIC_AUTH_SECRET`
`127.0.0.1`
`0.0.0.0`

For the same setup from the web-dashboard angle, seeWeb Dashboard → Connecting Hermes Desktop to a remote backend; the env vars are catalogued underEnvironment Variables → Web Dashboard & Hermes Desktop.

[Web Dashboard → Connecting Hermes Desktop to a remote backend](/docs/user-guide/features/web-dashboard#connecting-hermes-desktop-to-a-remote-backend)
[Environment Variables → Web Dashboard & Hermes Desktop](/docs/reference/environment-variables#web-dashboard--hermes-desktop)

## Troubleshooting​

Boot logs land inHERMES_HOME/logs/desktop.log(it includes backend output and recent Python tracebacks) — check it first if the app reports a boot failure. You can also tail it from the CLI:

`HERMES_HOME/logs/desktop.log`

```
hermes logs gui -f
```

Common resets:

```
# Force a clean first-launch setup (macOS/Linux)rm "$HOME/.hermes/hermes-agent/.hermes-bootstrap-complete"# Rebuild a broken Python venv (macOS/Linux)rm -rf "$HOME/.hermes/hermes-agent/venv"# Reset a stuck macOS microphone prompttccutil reset Microphone com.nousresearch.hermes
```

### "Build desktop app" stuck on Electron download​

The build downloads the Electron runtime (~114 MB) fromgithub.com/electron/electron/releases. If the installer hangs on theBuild desktop appstep with the live output repeatingretrying attempt=…, GitHub is being blocked or throttled on your network (firewall, proxy, or region).

`github.com/electron/electron/releases`
`retrying attempt=…`

The installer self-heals this automatically: on a failed build it (1) clears a corrupt cached Electron zip and retries, then (2) if it still fails and you haven't setELECTRON_MIRROR, retries once more throughnpmmirror.com, the de-facto Electron community mirror.@electron/getSHASUM-checks the download, but the checksums come from the same mirror — that catches a corrupt or partial download, not a compromised mirror. If you'd rather not trust a third-party host, pin your ownELECTRON_MIRROR(below); the build never overrides one you've set.

`ELECTRON_MIRROR`
`npmmirror.com`
`@electron/get`
`ELECTRON_MIRROR`

Tochoose your own mirror(e.g. a corporate/trusted one), setELECTRON_MIRRORbefore installing or rebuild manually — the build honors it and won't override it:

`ELECTRON_MIRROR`

```
ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/ \  bash -c 'cd "$HOME/.hermes/hermes-agent/apps/desktop" && CSC_IDENTITY_AUTO_DISCOVERY=false npm run pack'
```

To clear a corrupt cached zip by hand:

```
rm -f "$HOME/Library/Caches/electron"/electron-*.zip   # macOSrm -f "$HOME/.cache/electron"/electron-*.zip            # Linux
```

## Building from source​

If you want to hack on the app itself, install workspace deps from the repo root once, then run the dev server fromapps/desktop:

`apps/desktop`

```
npm install          # from repo root — links apps/desktop, web, apps/sharedcd apps/desktopnpm run dev          # Vite renderer + Electron, which boots the Python backend
```

Point the app at a specific checkout, or sandbox it from your real config:

```
HERMES_DESKTOP_HERMES_ROOT=/path/to/clone npm run devHERMES_HOME=/tmp/throwaway npm run devnpm run dev:fake-boot   # exercise the startup overlay with deterministic delays
```

Build installers:

```
npm run dist:mac     # DMG + zipnpm run dist:win     # NSIS + MSInpm run dist:linux   # AppImage + deb + rpmnpm run pack         # unpacked app under release/ (no installer)
```

macOS/Windows signing and notarization run automatically when the relevant credentials are present in the environment (CSC_LINK/CSC_KEY_PASSWORD/APPLE_*for macOS,WIN_CSC_*for Windows).

`CSC_LINK`
`CSC_KEY_PASSWORD`
`APPLE_*`
`WIN_CSC_*`

## See also​

- CLI Guide— the terminal interface
- TUI— the modern terminal UI used byhermes --tuiand the dashboard chat tab
- Web Dashboard— browser admin panel with an embedded chat tab
- Configuration— config that the desktop app reads and writes
- Windows (Native)— native Windows install path

[CLI Guide](/docs/user-guide/cli)
[TUI](/docs/user-guide/tui)
`hermes --tui`
[Web Dashboard](/docs/user-guide/features/web-dashboard)
[Configuration](/docs/user-guide/configuration)
[Windows (Native)](/docs/user-guide/windows-native)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/desktop.md)