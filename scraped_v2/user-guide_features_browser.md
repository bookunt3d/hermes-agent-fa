- 
- Features
- Media & Web
- Browser

# Browser Automation

Hermes Agent includes a full browser automation toolset with multiple backend options:

- Browserbase cloud modeviaBrowserbasefor managed cloud browsers and anti-bot tooling
- Browser Use cloud modeviaBrowser Useas an alternative cloud browser provider
- Firecrawl cloud modeviaFirecrawlfor cloud browsers with built-in scraping
- Camofox local modeviaCamofoxfor local anti-detection browsing (Firefox-based fingerprint spoofing)
- Local Chromium-family CDP— connect browser tools to your own Chrome, Brave, Chromium, or Edge instance using/browser connect
- Local browser modevia theagent-browserCLI and a local Chromium installation

`/browser connect`
`agent-browser`

In all modes, the agent can navigate websites, interact with page elements, fill forms, and extract information.

## Overview​

Pages are represented asaccessibility trees(text-based snapshots), making them ideal for LLM agents. Interactive elements get ref IDs (like@e1,@e2) that the agent uses for clicking and typing.

`@e1`
`@e2`

Key capabilities:

- Multi-provider cloud execution— Browserbase, Browser Use, or Firecrawl — no local browser needed
- Local Chromium-family integration— attach to your running Chrome, Brave, Chromium, or Edge browser via CDP for hands-on browsing
- Built-in stealth— random fingerprints, CAPTCHA solving, residential proxies (Browserbase)
- Session isolation— each task gets its own browser session
- Automatic cleanup— inactive sessions are closed after a timeout
- Vision analysis— screenshot + AI analysis for visual understanding

## Setup​

If you have a paidNous Portalsubscription, you can use browser automation through theTool Gatewaywithout any separate API keys. New installs can runhermes setup --portalto log in and turn on every gateway tool at once; existing installs can pickNous Subscriptionas the browser provider viahermes modelorhermes tools.

`hermes setup --portal`
`hermes model`
`hermes tools`

### Browserbase cloud mode​

To use Browserbase-managed cloud browsers, add:

```
# Add to ~/.hermes/.envBROWSERBASE_API_KEY=***BROWSERBASE_PROJECT_ID=your-project-id-here
```

Get your credentials atbrowserbase.com.

### Browser Use cloud mode​

To use Browser Use as your cloud browser provider, add:

```
# Add to ~/.hermes/.envBROWSER_USE_API_KEY=***
```

Get your API key atbrowser-use.com. Browser Use provides a cloud browser via its REST API. If both Browserbase and Browser Use credentials are set, Browserbase takes priority.

### Firecrawl cloud mode​

To use Firecrawl as your cloud browser provider, add:

```
# Add to ~/.hermes/.envFIRECRAWL_API_KEY=fc-***
```

Get your API key atfirecrawl.dev. Then select Firecrawl as your browser provider:

```
hermes setup tools# → Browser Automation → Firecrawl
```

Optional settings:

```
# Self-hosted Firecrawl instance (default: https://api.firecrawl.dev)FIRECRAWL_API_URL=http://localhost:3002# Session TTL in seconds (default: 300)FIRECRAWL_BROWSER_TTL=600
```

### Hybrid routing: cloud for public URLs, local for LAN/localhost​

When a cloud provider is configured, Hermes auto-spawns alocal Chromium sidecarfor URLs that resolve to a private/loopback/LAN address (localhost,127.0.0.1,192.168.x.x,10.x.x.x,172.16-31.x.x,*.local,*.lan,*.internal,
IPv6 loopback::1, link-local169.254.x.x). Public URLs continue to use the
cloud provider in the same conversation.

`localhost`
`127.0.0.1`
`192.168.x.x`
`10.x.x.x`
`172.16-31.x.x`
`*.local`
`*.lan`
`*.internal`
`::1`
`169.254.x.x`

This solves the common "I'm developing locally but using Browserbase" workflow —
the agent can screenshot your dashboard athttp://localhost:3000AND scrapehttps://github.comwithout you switching providers or disabling the SSRF guard.
The cloud provider never sees the private URL.

`http://localhost:3000`
`https://github.com`

The feature ison by default. To disable it (all URLs go to the configured
cloud provider, as before):

```
# ~/.hermes/config.yamlbrowser:  cloud_provider: browserbase  auto_local_for_private_urls: false
```

With auto-routing disabled, private URLs are rejected with"Blocked: URL targets a private or internal address"unless you also setbrowser.allow_private_urls: true(which lets the cloud provider attempt them —
usually won't work since Browserbase etc. can't reach your LAN).

`"Blocked: URL targets a private or internal address"`
`browser.allow_private_urls: true`

Requirements: the local sidecar uses the sameagent-browserCLI as pure local
mode, so you need it installed (hermes setup tools → Browser Automationauto-installs it). Post-navigation redirects from a public URL onto a private
address are still blocked (you can't use a redirect-to-internal trick to reach
your LAN through the public path).

`agent-browser`
`hermes setup tools → Browser Automation`

### Camofox local mode​

Camofoxis a self-hosted Node.js server wrapping Camoufox (a Firefox fork with C++ fingerprint spoofing). It provides local anti-detection browsing without cloud dependencies.

```
# Clone the Camofox browser server firstgit clone https://github.com/jo-inc/camofox-browsercd camofox-browser# Build and start with Docker using the default container settings# (auto-detects arch: aarch64 on M1/M2, x86_64 on Intel)make up# Stop and remove the default containermake down# Force a clean rebuild (for example, after upgrading VERSION/RELEASE)make reset# Just download binaries without buildingmake fetch# Override arch or version explicitlymake up ARCH=x86_64make up VERSION=135.0.1 RELEASE=beta.24
```

make upstarts the default container immediately. If you want custom runtime settings such as a larger Node heap, VNC, or a persistent profile directory, build the image first and then run it yourself:

`make up`

```
# Build the image without starting the default containermake build# Start with persistence, VNC live view, and a larger Node heapmkdir -p ~/.camofox-dockerdocker run -d \  --name camofox-browser \  --restart unless-stopped \  -p 9377:9377 \  -p 6080:6080 \  -p 5901:5900 \  -e CAMOFOX_PORT=9377 \  -e ENABLE_VNC=1 \  -e VNC_BIND=0.0.0.0 \  -e VNC_RESOLUTION=1920x1080 \  -e MAX_OLD_SPACE_SIZE=2048 \  -v ~/.camofox-docker:/root/.camofox \  camofox-browser:135.0.1-aarch64
```

With VNC enabled, the browser runs in headed mode and can be watched live in your browser athttp://localhost:6080(noVNC). You can also connect a native VNC client tolocalhost:5901.

`http://localhost:6080`
`localhost:5901`

If you already ranmake up, stop and remove that default container before starting the custom one:

`make up`

```
make down# then run the custom docker run command above
```

Then set in~/.hermes/.env:

`~/.hermes/.env`

```
CAMOFOX_URL=http://localhost:9377
```

If Camofox is running in Docker and you want it to open web apps served from the host machine, enable loopback rewriting.CAMOFOX_URLshould still point at the host-published control API, but page URLs such ashttp://127.0.0.1:3000must be opened from inside the container ashttp://host.docker.internal:3000:

`CAMOFOX_URL`
`http://127.0.0.1:3000`
`http://host.docker.internal:3000`

```
# ~/.hermes/config.yamlbrowser:  camofox:    rewrite_loopback_urls: true    loopback_host_alias: host.docker.internal  # default; use a LAN IP if needed
```

Equivalent env vars:

```
CAMOFOX_REWRITE_LOOPBACK_URLS=trueCAMOFOX_LOOPBACK_HOST_ALIAS=host.docker.internal
```

The rewrite only applies to page navigation URLs with loopback hosts (localhost,127.0.0.1,::1). It does not changeCAMOFOX_URL. Leave it disabled for non-Docker Camofox installs, where the browser already runs on the host and loopback URLs are correct.

`localhost`
`127.0.0.1`
`::1`
`CAMOFOX_URL`

Or configure viahermes tools→ Browser Automation → Camofox.

`hermes tools`

WhenCAMOFOX_URLis set, all browser tools automatically route through Camofox instead of Browserbase or agent-browser.

`CAMOFOX_URL`

#### Persistent browser sessions​

By default, each Camofox session gets a random identity — cookies and logins don't survive across agent restarts. To enable persistent browser sessions, add the following to~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
browser:  camofox:    managed_persistence: true
```

Then fully restart Hermes so the new config is picked up.

Hermes readsbrowser.camofox.managed_persistence,nota top-levelmanaged_persistence. A common mistake is writing:

`browser.camofox.managed_persistence`
`managed_persistence`

```
# ❌ Wrong — Hermes ignores thismanaged_persistence: true
```

If the flag is placed at the wrong path, Hermes silently falls back to a random ephemeraluserIdand your login state will be lost on every session.

`userId`

##### What Hermes does​

- Sends a deterministic profile-scopeduserIdto Camofox so the server can reuse the same Firefox profile across sessions.
- Skips server-side context destruction on cleanup, so cookies and logins survive between agent tasks.
- Scopes theuserIdto the active Hermes profile, so different Hermes profiles get different browser profiles (profile isolation).

`userId`
`userId`

##### What Hermes does not do​

- It does not force persistence on the Camofox server. Hermes only sends a stableuserId; the server must honor it by mapping thatuserIdto a persistent Firefox profile directory.
- If your Camofox server build treats every request as ephemeral (e.g. always callsbrowser.newContext()without loading a stored profile), Hermes cannot make those sessions persist. Make sure you are running a Camofox build that implements userId-based profile persistence.

`userId`
`userId`
`browser.newContext()`

##### Verify it's working​

1. Start Hermes and your Camofox server.
2. Open Google (or any login site) in a browser task and sign in manually.
3. End the browser task normally.
4. Start a new browser task.
5. Open the same site again — you should still be signed in.

If step 5 logs you out, the Camofox server isn't honoring the stableuserId. Double-check your config path, confirm you fully restarted Hermes after editingconfig.yaml, and verify your Camofox server version supports persistent per-user profiles.

`userId`
`config.yaml`

##### Where state lives​

Hermes derives the stableuserIdfrom the profile-scoped directory~/.hermes/browser_auth/camofox/(or the equivalent under$HERMES_HOMEfor non-default profiles). The actual browser profile data lives on the Camofox server side, keyed by thatuserId. To fully reset a persistent profile, clear it on the Camofox server and remove the corresponding Hermes profile's state directory.

`userId`
`~/.hermes/browser_auth/camofox/`
`$HERMES_HOME`
`userId`

#### Externally managed Camofox sessions​

When another app drives the visible Camofox browser (a desktop assistant, a custom integration, another agent), configure Hermes to operate inside that same identity instead of spawning its own isolated profile.

Three knobs control the behavior:

| Setting | Env var | Effect |
| --- | --- | --- |
| browser.camofox.user_id | CAMOFOX_USER_ID | CamofoxuserIdHermes uses when creating tabs. Setting this opts the session into "externally managed" mode. |
| browser.camofox.session_key | CAMOFOX_SESSION_KEY | sessionKey(a.k.a.listItemId) sent on tab creation. Used to match an existing tab during adoption. Defaults to a per-task value if unset. |
| browser.camofox.adopt_existing_tab | CAMOFOX_ADOPT_EXISTING_TAB | When true, Hermes callsGET /tabs?userId=<user_id>on first use and reuses an existing tab before creating a new one. |

`browser.camofox.user_id`
`CAMOFOX_USER_ID`
`userId`
`browser.camofox.session_key`
`CAMOFOX_SESSION_KEY`
`sessionKey`
`listItemId`
`browser.camofox.adopt_existing_tab`
`CAMOFOX_ADOPT_EXISTING_TAB`
`GET /tabs?userId=<user_id>`

Env vars take precedence overconfig.yaml. Either form works:

`config.yaml`

```
browser:  camofox:    user_id: shared-camofox    session_key: visible-tab    adopt_existing_tab: true
```

```
CAMOFOX_USER_ID=shared-camofoxCAMOFOX_SESSION_KEY=visible-tabCAMOFOX_ADOPT_EXISTING_TAB=true
```

What changes whenuser_idis set:

`user_id`
- Hermes skips destructive cleanup at task end (same asmanaged_persistence: true). The other app's tab/cookies/profile survive.
- Hermes doesnotcallDELETE /sessions/<user_id>— that endpoint wipes all user data, so it would nuke the external app's session if it fired.

`managed_persistence: true`
`DELETE /sessions/<user_id>`

How tab adoption works (whenadopt_existing_tab: true):

`adopt_existing_tab: true`
1. On the first browser tool call after a process start, Hermes issuesGET /tabs?userId=<user_id>(5-second timeout).
2. If any tab in the response haslistItemId == session_key, Hermes adopts the most recently created one in that group.
3. Otherwise, Hermes adopts the most recently created tab for the user (anylistItemId).
4. If no tabs exist or the request fails, Hermes falls back to creating a new tab on the next operation.

`GET /tabs?userId=<user_id>`
`listItemId == session_key`
`listItemId`

Adoption only fires untiltab_idis populated for the session. If the external app closes the adopted tab mid-run, the next browser tool call will surface a Camofox error — Hermes does not re-poll for a fresh tab on every call.

`tab_id`

Pickingsession_key:if you want Hermes to reliably attach to aspecificexisting tab, setsession_keyto thelistItemIdthe external app used when creating it. If you leavesession_keyunset and only setuser_id, Hermes generates a per-tasksession_key(task_<id>) — Hermes will share cookies and the profile with the external app, but will open its own tab alongside instead of reusing one.

`session_key`
`session_key`
`listItemId`
`session_key`
`user_id`
`session_key`
`task_<id>`

Concurrency note:the external app and Hermes can drive the same CamofoxuserIdsimultaneously, but Camofox does not coordinate per-tab focus between clients. Coordinate ownership at the application layer (e.g. the external app pauses while Hermes runs).

`userId`

#### VNC live view​

When Camofox runs in headed mode (with a visible browser window), it exposes a VNC port in its health check response. Hermes automatically discovers this and includes the VNC URL in navigation responses, so the agent can share a link for you to watch the browser live.

### Local Chromium-family browser via CDP (/browser connect)​

`/browser connect`

Instead of a cloud provider, you can attach Hermes browser tools to your own running Chrome, Brave, Chromium, or Edge instance via the Chrome DevTools Protocol (CDP). This is useful when you want to see what the agent is doing in real-time, interact with pages that require your own cookies/sessions, or avoid cloud browser costs.

/browser connectis aninteractive-CLI slash command— it is not dispatched by the gateway. If you try to run it inside a WebUI, Telegram, Discord, or other gateway chat, the message will be sent to the agent as plain text and the command will not execute. Start Hermes from the terminal (hermesorhermes chat) and issue/browser connectthere.

`/browser connect`
`hermes`
`hermes chat`
`/browser connect`

In the CLI, use:

```
/browser connect                 # Auto-launch/connect to a local Chromium-family browser at http://127.0.0.1:9222/browser connect ws://host:port  # Connect to a specific CDP endpoint/browser status                  # Check current connection/browser disconnect              # Detach and return to cloud/local mode
```

If a browser isn't already running with remote debugging, Hermes will attempt to auto-launch a supported Chromium-family browser with--remote-debugging-port=9222. Detection includes Brave, Google Chrome, Chromium, and Microsoft Edge, with common Linux install paths such as/opt/brave-bin/braveand/snap/bin/brave.

`--remote-debugging-port=9222`
`/opt/brave-bin/brave`
`/snap/bin/brave`

To start a Chromium-family browser manually with CDP enabled, use a dedicated user-data-dir so the debug port actually comes up even if the browser is already running with your normal profile:

```
# Linux — Bravebrave-browser \  --remote-debugging-port=9222 \  --user-data-dir=$HOME/.hermes/chrome-debug \  --no-first-run \  --no-default-browser-check &# Linux — Google Chromegoogle-chrome \  --remote-debugging-port=9222 \  --user-data-dir=$HOME/.hermes/chrome-debug \  --no-first-run \  --no-default-browser-check &# macOS — Brave"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \  --remote-debugging-port=9222 \  --user-data-dir="$HOME/.hermes/chrome-debug" \  --no-first-run \  --no-default-browser-check &# macOS — Google Chrome"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \  --remote-debugging-port=9222 \  --user-data-dir="$HOME/.hermes/chrome-debug" \  --no-first-run \  --no-default-browser-check &
```

Then launch the Hermes CLI and run/browser connect.

`/browser connect`

Why--user-data-dir?Without it, launching a Chromium-family browser while a regular instance is already running typically opens a new window on the existing process — and that existing process was not started with--remote-debugging-port, so port 9222 never opens. A dedicated user-data-dir forces a fresh browser process where the debug port actually listens.--no-first-run --no-default-browser-checkskips the first-launch wizard for the fresh profile.

`--user-data-dir`
`--remote-debugging-port`
`--no-first-run --no-default-browser-check`

When connected via CDP, all browser tools (browser_navigate,browser_click, etc.) operate on your live browser instance instead of spinning up a cloud session.

`browser_navigate`
`browser_click`

### WSL2 + Windows Chrome: prefer MCP over/browser connect​

`/browser connect`

If Hermes runs inside WSL2 but the Chrome window you want to control runs on the Windows host,/browser connectis often not the best path.

`/browser connect`

Why:

- /browser connectexpects Hermes itself to reach a usable CDP endpoint
- modern Chrome live-debugging sessions often expose a host-local endpoint that is not directly reachable from WSL the same way a classic9222port is
- even when Windows Chrome is debuggable, the cleanest integration is often to let a Windows-side browser MCP server attach to Chrome and let Hermes talk to that MCP server

`/browser connect`
`9222`

For that setup, preferchrome-devtools-mcpthrough Hermes MCP support.

`chrome-devtools-mcp`

See the MCP guide for the practical setup:

- Use MCP with Hermes

### Local browser mode​

If you donotset any cloud credentials and don't use/browser connect, Hermes can still use the browser tools through a local Chromium install driven byagent-browser.

`/browser connect`
`agent-browser`

### Optional Environment Variables​

```
# Residential proxies for better CAPTCHA solving (default: "true")BROWSERBASE_PROXIES=true# Advanced stealth with custom Chromium — requires Scale Plan (default: "false")BROWSERBASE_ADVANCED_STEALTH=false# Session reconnection after disconnects — requires paid plan (default: "true")BROWSERBASE_KEEP_ALIVE=true# Custom session timeout in seconds (max 21600 = 6 hours) (default: project default)# Examples: 600 (10min), 1800 (30min), 21600 (6h max)BROWSERBASE_SESSION_TIMEOUT=1800# Inactivity timeout before auto-cleanup in seconds (default: 120)BROWSER_INACTIVITY_TIMEOUT=120# Extra Chromium launch flags (comma- or newline-separated). Hermes auto-injects# `--no-sandbox,--disable-dev-shm-usage` when it detects root or AppArmor-restricted# unprivileged user namespaces (Ubuntu 23.10+, DGX Spark, many container images),# so most users don't need to set this. Set it manually only if you need a flag# Hermes doesn't add automatically; setting it disables the auto-injection.AGENT_BROWSER_ARGS=--no-sandbox
```

### Install agent-browser CLI​

```
npm install -g agent-browser# Or install locally in the repo:npm install
```

Thebrowsertoolset must be included in your config'stoolsetslist or enabled viahermes config set toolsets '["hermes-cli", "browser"]'.

`browser`
`toolsets`
`hermes config set toolsets '["hermes-cli", "browser"]'`

## Available Tools​

### browser_navigate​

`browser_navigate`

Navigate to a URL. Must be called before any other browser tool. Initializes the Browserbase session.

```
Navigate to https://github.com/NousResearch
```

For simple information retrieval, preferweb_searchorweb_extract— they are faster and cheaper. Use browser tools when you need tointeractwith a page (click buttons, fill forms, handle dynamic content).

`web_search`
`web_extract`

### browser_snapshot​

`browser_snapshot`

Get a text-based snapshot of the current page's accessibility tree. Returns interactive elements with ref IDs like@e1,@e2for use withbrowser_clickandbrowser_type.

`@e1`
`@e2`
`browser_click`
`browser_type`
- full=false(default): Compact view showing only interactive elements
- full=true: Complete page content

`full=false`
`full=true`

Snapshots over 8000 characters are automatically summarized by an LLM.

### browser_click​

`browser_click`

Click an element identified by its ref ID from the snapshot.

```
Click @e5 to press the "Sign In" button
```

### browser_type​

`browser_type`

Type text into an input field. Clears the field first, then types the new text.

```
Type "hermes agent" into the search field @e3
```

### browser_scroll​

`browser_scroll`

Scroll the page up or down to reveal more content.

```
Scroll down to see more results
```

### browser_press​

`browser_press`

Press a keyboard key. Useful for submitting forms or navigation.

```
Press Enter to submit the form
```

Supported keys:Enter,Tab,Escape,ArrowDown,ArrowUp, and more.

`Enter`
`Tab`
`Escape`
`ArrowDown`
`ArrowUp`

### browser_back​

`browser_back`

Navigate back to the previous page in browser history.

### browser_get_images​

`browser_get_images`

List all images on the current page with their URLs and alt text. Useful for finding images to analyze.

### browser_vision​

`browser_vision`

Take a screenshot and analyze it with vision AI. Use this when text snapshots don't capture important visual information — especially useful for CAPTCHAs, complex layouts, or visual verification challenges.

The screenshot is saved persistently and the file path is returned alongside the AI analysis. On messaging platforms (Telegram, Discord, Slack, WhatsApp), you can ask the agent to share the screenshot — it will be sent as a native photo attachment via theMEDIA:mechanism.

`MEDIA:`

```
What does the chart on this page show?
```

Screenshots are stored in~/.hermes/cache/screenshots/and automatically cleaned up after 24 hours.

`~/.hermes/cache/screenshots/`

### browser_console​

`browser_console`

Get browser console output (log/warn/error messages) and uncaught JavaScript exceptions from the current page. Essential for detecting silent JS errors that don't appear in the accessibility tree.

```
Check the browser console for any JavaScript errors
```

Useclear=Trueto clear the console after reading, so subsequent calls only show new messages.

`clear=True`

browser_consolealso evaluates JavaScript when called with anexpressionargument — same shape as DevTools console, the result comes back parsed (JSON-serialized objects become dicts; primitive values stay primitive).

`browser_console`
`expression`

```
browser_console(expression="document.querySelector('h1').textContent")browser_console(expression="JSON.stringify(performance.timing)")
```

When a CDP supervisor is active for the current session (typical for any session that's runbrowser_navigateagainst a CDP-capable backend), evaluation runs over the supervisor's persistent WebSocket — no subprocess startup cost. Falls through to the standard agent-browser CLI path otherwise. Behaviour is identical either way; only latency changes.

`browser_navigate`

### browser_cdp​

`browser_cdp`

Raw Chrome DevTools Protocol passthrough — the escape hatch for browser operations not covered by the other tools. Use for native dialog handling, iframe-scoped evaluation, cookie/network control, or any CDP verb the agent needs.

Only available when a CDP endpoint is reachable at session start— meaning/browser connecthas attached to a running Chrome, Brave, Chromium, or Edge browser, orbrowser.cdp_urlis set inconfig.yaml. The default local agent-browser mode, Camofox, and cloud providers (Browserbase, Browser Use, Firecrawl) do not currently expose CDP to this tool — cloud providers have per-session CDP URLs but live-session routing is a follow-up.

`/browser connect`
`browser.cdp_url`
`config.yaml`

CDP method reference:https://chromedevtools.github.io/devtools-protocol/— the agent canweb_extracta specific method's page to look up parameters and return shape.

`web_extract`

Common patterns:

```
# List tabs (browser-level, no target_id)browser_cdp(method="Target.getTargets")# Handle a native JS dialog on a tabbrowser_cdp(method="Page.handleJavaScriptDialog",            params={"accept": true, "promptText": ""},            target_id="<tabId>")# Evaluate JS in a specific tabbrowser_cdp(method="Runtime.evaluate",            params={"expression": "document.title", "returnByValue": true},            target_id="<tabId>")# Get all cookiesbrowser_cdp(method="Network.getAllCookies")
```

Browser-level methods (Target.*,Browser.*,Storage.*) omittarget_id. Page-level methods (Page.*,Runtime.*,DOM.*,Emulation.*) require atarget_idfromTarget.getTargets. Each stateless call is independent — sessions do not persist between calls.

`Target.*`
`Browser.*`
`Storage.*`
`target_id`
`Page.*`
`Runtime.*`
`DOM.*`
`Emulation.*`
`target_id`
`Target.getTargets`

Cross-origin iframes:passframe_id(frombrowser_snapshot.frame_tree.children[]whereis_oopif=true) to route the CDP call through the supervisor's live session for that iframe. This is howRuntime.evaluateinside a cross-origin iframe works on Browserbase, where stateless CDP connections would hit signed-URL expiry. Example:

`frame_id`
`browser_snapshot.frame_tree.children[]`
`is_oopif=true`
`Runtime.evaluate`

```
browser_cdp(  method="Runtime.evaluate",  params={"expression": "document.title", "returnByValue": True},  frame_id="<frame_id from browser_snapshot>",)
```

Same-origin iframes don't needframe_id— usedocument.querySelector('iframe').contentDocumentfrom a top-levelRuntime.evaluateinstead.

`frame_id`
`document.querySelector('iframe').contentDocument`
`Runtime.evaluate`

### browser_dialog​

`browser_dialog`

Responds to a native JS dialog (alert/confirm/prompt/beforeunload). Before this tool existed, dialogs would silently block the page's JavaScript thread and subsequentbrowser_*calls would hang or throw; now the agent sees pending dialogs inbrowser_snapshotoutput and responds explicitly.

`alert`
`confirm`
`prompt`
`beforeunload`
`browser_*`
`browser_snapshot`

Workflow:

1. Callbrowser_snapshot. If a dialog is blocking the page, it shows up aspending_dialogs: [{"id": "d-1", "type": "alert", "message": "..."}].
2. Callbrowser_dialog(action="accept")orbrowser_dialog(action="dismiss"). Forprompt()dialogs, passprompt_text="..."to supply the response.
3. Re-snapshot —pending_dialogsis empty; the page's JS thread has resumed.

`browser_snapshot`
`pending_dialogs: [{"id": "d-1", "type": "alert", "message": "..."}]`
`browser_dialog(action="accept")`
`browser_dialog(action="dismiss")`
`prompt()`
`prompt_text="..."`
`pending_dialogs`

Detection happens automaticallyvia a persistent CDP supervisor — one WebSocket per task that subscribes to Page/Runtime/Target events. The supervisor also populates aframe_treefield in the snapshot so the agent can see the iframe structure of the current page, including cross-origin (OOPIF) iframes.

`frame_tree`

Availability matrix:

| Backend | Detection viapending_dialogs | Response (browser_dialogtool) |
| --- | --- | --- |
| Local Chrome via/browser connectorbrowser.cdp_url | ✓ | ✓ full workflow |
| Browserbase | ✓ | ✓ full workflow (via injected XHR bridge) |
| Camofox / default local agent-browser | ✗ | ✗ (no CDP endpoint) |

`pending_dialogs`
`browser_dialog`
`/browser connect`
`browser.cdp_url`

How it works on Browserbase.Browserbase's CDP proxy auto-dismisses real native dialogs server-side within ~10ms, so we can't usePage.handleJavaScriptDialog. The supervisor injects a small script viaPage.addScriptToEvaluateOnNewDocumentthat overrideswindow.alert/confirm/promptwith a synchronous XHR. We intercept those XHRs viaFetch.enable— the page's JS thread stays blocked on the XHR until we callFetch.fulfillRequestwith the agent's response.prompt()return values round-trip back into page JS unchanged.

`Page.handleJavaScriptDialog`
`Page.addScriptToEvaluateOnNewDocument`
`window.alert`
`confirm`
`prompt`
`Fetch.enable`
`Fetch.fulfillRequest`
`prompt()`

Dialog policyis configured inconfig.yamlunderbrowser.dialog_policy:

`config.yaml`
`browser.dialog_policy`
| Policy | Behavior |
| --- | --- |
| must_respond(default) | Capture, surface in snapshot, wait for explicitbrowser_dialog()call. Safety auto-dismiss afterbrowser.dialog_timeout_s(default 300s) so a buggy agent can't stall forever. |
| auto_dismiss | Capture, dismiss immediately. Agent still sees the dialog inbrowser_statehistory but doesn't have to act. |
| auto_accept | Capture, accept immediately. Useful when navigating pages with aggressivebeforeunloadprompts. |

`must_respond`
`browser_dialog()`
`browser.dialog_timeout_s`
`auto_dismiss`
`browser_state`
`auto_accept`
`beforeunload`

Frame treeinsidebrowser_snapshot.frame_treeis capped to 30 frames and OOPIF depth 2 to keep payloads bounded on ad-heavy pages. Atruncated: trueflag surfaces when limits were hit; agents needing the full tree can usebrowser_cdpwithPage.getFrameTree.

`browser_snapshot.frame_tree`
`truncated: true`
`browser_cdp`
`Page.getFrameTree`

## Practical Examples​

### Filling Out a Web Form​

```
User: Sign up for an account on example.com with my email john@example.comAgent workflow:1. browser_navigate("https://example.com/signup")2. browser_snapshot()  → sees form fields with refs3. browser_type(ref="@e3", text="john@example.com")4. browser_type(ref="@e5", text="SecurePass123")5. browser_click(ref="@e8")  → clicks "Create Account"6. browser_snapshot()  → confirms success
```

### Researching Dynamic Content​

```
User: What are the top trending repos on GitHub right now?Agent workflow:1. browser_navigate("https://github.com/trending")2. browser_snapshot(full=true)  → reads trending repo list3. Returns formatted results
```

## Session Recording​

Automatically record browser sessions as WebM video files:

```
browser:  record_sessions: true  # default: false
```

When enabled, recording starts automatically on the firstbrowser_navigateand saves to~/.hermes/browser_recordings/when the session closes. Works in both local and cloud (Browserbase) modes. Recordings older than 72 hours are automatically cleaned up.

`browser_navigate`
`~/.hermes/browser_recordings/`

## Stealth Features​

Browserbase provides automatic stealth capabilities:

| Feature | Default | Notes |
| --- | --- | --- |
| Basic Stealth | Always on | Random fingerprints, viewport randomization, CAPTCHA solving |
| Residential Proxies | On | Routes through residential IPs for better access |
| Advanced Stealth | Off | Custom Chromium build, requires Scale Plan |
| Keep Alive | On | Session reconnection after network hiccups |

If paid features aren't available on your plan, Hermes automatically falls back — first disablingkeepAlive, then proxies — so browsing still works on free plans.

`keepAlive`

## Session Management​

- Each task gets an isolated browser session via Browserbase
- Sessions are automatically cleaned up after inactivity (default: 2 minutes)
- A background thread checks every 30 seconds for stale sessions
- Emergency cleanup runs on process exit to prevent orphaned sessions
- Sessions are released via the Browserbase API (REQUEST_RELEASEstatus)

`REQUEST_RELEASE`

## Limitations​

- Text-based interaction— relies on accessibility tree, not pixel coordinates
- Snapshot size— large pages may be truncated or LLM-summarized at 8000 characters
- Session timeout— cloud sessions expire based on your provider's plan settings
- Cost— cloud sessions consume provider credits; sessions are automatically cleaned up when the conversation ends or after inactivity. Use/browser connectfor free local browsing.
- No file downloads— cannot download files from the browser

`/browser connect`