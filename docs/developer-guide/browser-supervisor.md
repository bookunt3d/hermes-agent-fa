---
layout: docs
title: "نظارت‌گر مرورگر"
permalink: /docs/developer-guide/browser-supervisor/
---

- 
- Developer Guide
- Internals
- Browser CDP Supervisor

# Browser CDP Supervisor

The CDP supervisor closes two long-standing gaps in Hermes' browser tooling:

1. Native JS dialogs(alert/confirm/prompt/beforeunload) block the
page's JS thread. Without supervision, the agent has no way to know a
dialog is open — subsequent tool calls hang or throw opaque errors.
2. Cross-origin iframes (OOPIFs)are invisible to top-levelRuntime.evaluate. The agent can see iframe nodes in the DOM snapshot but
can't click, type, or eval inside them without a CDP session attached to
the child target.

`alert`
`confirm`
`prompt`
`beforeunload`
`Runtime.evaluate`

The supervisor solves both by holding a persistent WebSocket to the backend's
CDP endpoint per browser task, surfacing pending dialogs and frame structure
intobrowser_snapshot, and exposing abrowser_dialogtool for explicit
responses.

`browser_snapshot`
`browser_dialog`

## Backend support​

| Backend | Dialog detect | Dialog respond | Frame tree | OOPIFRuntime.evaluateviabrowser_cdp(frame_id=...) |
| --- | --- | --- | --- | --- |
| Local Chrome (--remote-debugging-port) //browser connect | ✓ | ✓ full workflow | ✓ | ✓ |
| Browserbase | ✓ (via bridge) | ✓ full workflow (via bridge) | ✓ | ✓ |
| Camofox | ✗ no CDP (REST-only) | ✗ | partial via DOM snapshot | ✗ |

`Runtime.evaluate`
`browser_cdp(frame_id=...)`
`--remote-debugging-port`
`/browser connect`

Browserbase quirk.Browserbase's CDP proxy uses Playwright internally and
auto-dismisses native dialogs within ~10ms, soPage.handleJavaScriptDialogcan't keep up. The supervisor injects a bridge script viaPage.addScriptToEvaluateOnNewDocumentthat overrideswindow.alert/confirm/promptwith a synchronous XHR to a magic host
(hermes-dialog-bridge.invalid).Fetch.enableintercepts those XHRs before
they touch the network — the dialog becomes aFetch.requestPausedevent the
supervisor captures, andrespond_to_dialogfulfills viaFetch.fulfillRequestwith a JSON body the injected script decodes.

`Page.handleJavaScriptDialog`
`Page.addScriptToEvaluateOnNewDocument`
`window.alert`
`confirm`
`prompt`
`hermes-dialog-bridge.invalid`
`Fetch.enable`
`Fetch.requestPaused`
`respond_to_dialog`
`Fetch.fulfillRequest`

From the page's perspective,prompt()still returns the agent-supplied
string. From the agent's perspective, it's the samebrowser_dialog(action=...)API either way.

`prompt()`
`browser_dialog(action=...)`

Camofox is unsupported — no CDP surface, REST-only.

## Architecture​

### CDPSupervisor​

Oneasyncio.Taskrunning in a background daemon thread per Hermestask_id.
Holds a persistent WebSocket to the backend's CDP endpoint. Maintains:

`asyncio.Task`
`task_id`
- Dialog queue—List[PendingDialog]with{id, type, message, default_prompt, session_id, opened_at}
- Frame tree—Dict[frame_id, FrameInfo]with parent relationships, URL, origin, whether cross-origin child session
- Session map—Dict[session_id, SessionInfo]so interaction tools can route to the right attached session for OOPIF operations
- Recent console errors— ring buffer of the last 50 for diagnostics

`List[PendingDialog]`
`{id, type, message, default_prompt, session_id, opened_at}`
`Dict[frame_id, FrameInfo]`
`Dict[session_id, SessionInfo]`

Subscribes on attach:

- Page.enable—javascriptDialogOpening,frameAttached,frameNavigated,frameDetached
- Runtime.enable—executionContextCreated,consoleAPICalled,exceptionThrown
- Target.setAutoAttach {autoAttach: true, flatten: true}— surfaces child OOPIF targets; supervisor enablesPage+Runtimeon each

`Page.enable`
`javascriptDialogOpening`
`frameAttached`
`frameNavigated`
`frameDetached`
`Runtime.enable`
`executionContextCreated`
`consoleAPICalled`
`exceptionThrown`
`Target.setAutoAttach {autoAttach: true, flatten: true}`
`Page`
`Runtime`

Thread-safe state access via a snapshot lock; tool handlers (sync) read the
frozen snapshot without awaiting.

### Lifecycle​

- Start:SupervisorRegistry.get_or_start(task_id, cdp_url)— called bybrowser_navigate, Browserbase session create,/browser connect.
Idempotent.
- Stop:session teardown or/browser disconnect. Cancels the asyncio
task, closes the WebSocket, discards state.
- Rebind:if the CDP URL changes (user reconnects to a new Chrome), the
old supervisor is stopped and a fresh one started — state is never reused
across endpoints.

`SupervisorRegistry.get_or_start(task_id, cdp_url)`
`browser_navigate`
`/browser connect`
`/browser disconnect`

### Dialog policy​

Configurable viaconfig.yamlunderbrowser.dialog_policy:

`config.yaml`
`browser.dialog_policy`
- must_respond(default) — capture, surface inbrowser_snapshot, wait
for explicitbrowser_dialog(action=...)call. After a 300s safety timeout
with no response, auto-dismiss and log. Prevents a buggy agent from stalling
forever.
- auto_dismiss— record and dismiss immediately; agent sees it after the
fact viabrowser_stateinsidebrowser_snapshot.
- auto_accept— record and accept (useful forbeforeunloadwhere the
workflow wants to navigate away cleanly).

`must_respond`
`browser_snapshot`
`browser_dialog(action=...)`
`auto_dismiss`
`browser_state`
`browser_snapshot`
`auto_accept`
`beforeunload`

Policy is per-task; no per-dialog overrides.

## Agent surface​

### browser_dialogtool​

`browser_dialog`

```
browser_dialog(action, prompt_text=None, dialog_id=None)
```

- action="accept"/"dismiss"→ responds to the specified or sole pending dialog (required)
- prompt_text=...→ text to supply to aprompt()dialog
- dialog_id=...→ disambiguate when multiple dialogs are queued (rare)

`action="accept"`
`"dismiss"`
`prompt_text=...`
`prompt()`
`dialog_id=...`

Tool is response-only. The agent reads pending dialogs frombrowser_snapshotoutput before calling.

`browser_snapshot`

### browser_snapshotextension​

`browser_snapshot`

Adds three optional fields to the existing snapshot output when a supervisor
is attached:

```
{  "pending_dialogs": [    {"id": "d-1", "type": "alert", "message": "Hello", "opened_at": 1650000000.0}  ],  "recent_dialogs": [    {"id": "d-1", "type": "alert", "message": "...", "opened_at": 1650000000.0,     "closed_at": 1650000000.1, "closed_by": "remote"}  ],  "frame_tree": {    "top": {"frame_id": "FRAME_A", "url": "https://example.com/", "origin": "https://example.com"},    "children": [      {"frame_id": "FRAME_B", "url": "about:srcdoc", "is_oopif": false},      {"frame_id": "FRAME_C", "url": "https://ads.example.net/", "is_oopif": true, "session_id": "SID_C"}    ],    "truncated": false  }}
```

- pending_dialogs— dialogs currently blocking the page's JS thread.
The agent must callbrowser_dialog(action=...)to respond. Empty on
Browserbase because their CDP proxy auto-dismisses within ~10ms.
- recent_dialogs— ring buffer of up to 20 recently-closed dialogs with
aclosed_bytag:"agent"(we responded),"auto_policy"(local
auto_dismiss/auto_accept),"watchdog"(must_respond timeout hit), or"remote"(browser/backend closed it on us, e.g. Browserbase). This is
how agents on Browserbase still get visibility into what happened.
- frame_tree— frame structure including cross-origin (OOPIF) children.
Capped at 30 entries + OOPIF depth 2 to bound snapshot size on ad-heavy
pages.truncated: truesurfaces when limits were hit; agents needing
the full tree can usebrowser_cdpwithPage.getFrameTree.

pending_dialogs— dialogs currently blocking the page's JS thread.
The agent must callbrowser_dialog(action=...)to respond. Empty on
Browserbase because their CDP proxy auto-dismisses within ~10ms.

`pending_dialogs`
`browser_dialog(action=...)`

recent_dialogs— ring buffer of up to 20 recently-closed dialogs with
aclosed_bytag:"agent"(we responded),"auto_policy"(local
auto_dismiss/auto_accept),"watchdog"(must_respond timeout hit), or"remote"(browser/backend closed it on us, e.g. Browserbase). This is
how agents on Browserbase still get visibility into what happened.

`recent_dialogs`
`closed_by`
`"agent"`
`"auto_policy"`
`"watchdog"`
`"remote"`

frame_tree— frame structure including cross-origin (OOPIF) children.
Capped at 30 entries + OOPIF depth 2 to bound snapshot size on ad-heavy
pages.truncated: truesurfaces when limits were hit; agents needing
the full tree can usebrowser_cdpwithPage.getFrameTree.

`frame_tree`
`truncated: true`
`browser_cdp`
`Page.getFrameTree`

No new tool schema surface for any of these — the agent reads the snapshot it
already requests.

### Availability gating​

Both surfaces gate on_browser_cdp_check(supervisor can only run when a CDP
endpoint is reachable). On Camofox / no-backend sessions, the dialog tool is
hidden and the snapshot omits the new fields — no schema bloat.

`_browser_cdp_check`

## Cross-origin iframe interaction​

browser_cdp(frame_id=...)routes CDP calls (notablyRuntime.evaluate)
through the supervisor's already-connected WebSocket using the OOPIF's childsessionId. Agents pick frame_ids out ofbrowser_snapshot.frame_tree.children[]whereis_oopif=trueand pass them
tobrowser_cdp. For same-origin iframes (no dedicated CDP session), the
agent usescontentWindow/contentDocumentfrom a top-levelRuntime.evaluateinstead — the supervisor surfaces an error pointing at that
fallback whenframe_idbelongs to a non-OOPIF.

`browser_cdp(frame_id=...)`
`Runtime.evaluate`
`sessionId`
`browser_snapshot.frame_tree.children[]`
`is_oopif=true`
`browser_cdp`
`contentWindow`
`contentDocument`
`Runtime.evaluate`
`frame_id`

On Browserbase, this is the only reliable path for iframe interaction —
stateless CDP connections (opened perbrowser_cdpcall) hit signed-URL
expiry, while the supervisor's long-lived connection keeps a valid session.

`browser_cdp`

## File layout​

- tools/browser_supervisor.py—CDPSupervisor,SupervisorRegistry,PendingDialog,FrameInfo
- tools/browser_dialog_tool.py—browser_dialogtool handler
- tools/browser_tool.py—browser_navigatestart-hook,browser_snapshotmerge,/browser connectreattach,_cleanup_browser_sessionteardown
- toolsets.py— registersbrowser_dialoginbrowser,hermes-acp,hermes-api-server, and core toolsets (gated on CDP reachability)
- hermes_cli/config.py—browser.dialog_policyandbrowser.dialog_timeout_sdefaults

`tools/browser_supervisor.py`
`CDPSupervisor`
`SupervisorRegistry`
`PendingDialog`
`FrameInfo`
`tools/browser_dialog_tool.py`
`browser_dialog`
`tools/browser_tool.py`
`browser_navigate`
`browser_snapshot`
`/browser connect`
`_cleanup_browser_session`
`toolsets.py`
`browser_dialog`
`browser`
`hermes-acp`
`hermes-api-server`
`hermes_cli/config.py`
`browser.dialog_policy`
`browser.dialog_timeout_s`

## Non-goals​

- Detection/interaction for Camofox (upstream gap; tracked separately)
- Streaming dialog/frame events live to the user (would require gateway hooks)
- Persisting dialog history across sessions (in-memory only)
- Per-iframe dialog policies (agent can express this viadialog_id)
- Replacingbrowser_cdp— it stays as the escape hatch for the long tail (cookies, viewport, network throttling)

`dialog_id`
`browser_cdp`

## Testing​

Unit tests (tests/tools/test_browser_supervisor.py) use an asyncio mock CDP
server that speaks enough of the protocol to exercise all state transitions:
attach, enable, navigate, dialog fire, dialog dismiss, frame attach/detach,
child target attach, session teardown. Real-backend E2E (Browserbase + local
Chromium-family browser) is manual — exercise via/browser connectto a
live Chromium-family browser and run the dialog/frame test cases described
above.

`tests/tools/test_browser_supervisor.py`
`/browser connect`