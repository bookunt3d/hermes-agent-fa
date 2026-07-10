- 
- Developer Guide
- Extending
- Plugins
- Browser Provider Plugins

# Building a Browser Provider Plugin

Browser provider plugins register acloud browser backendthat services cloud-modebrowser_*tool calls (navigate, click, screenshot, …). Built-in providers — Browserbase, Browser Use, and Firecrawl — all ship as plugins underplugins/browser/<name>/. You can add a new one, or override a bundled one, by dropping a directory next to them.

`browser_*`
`plugins/browser/<name>/`

Browser backends are one of severalbackend pluginsHermes supports. The others (with their own ABCs) areWeb Search Provider Plugins(which this ABC deliberately mirrors),Image Generation,Video Generation,Memory Providers,Context Engines,Secret Sources, andModel Providers. General tool/hook/CLI plugins live inBuild a Hermes Plugin.

## How it fits together​

A browser provider doesnotimplement browsing. It implementssession lifecycle: create a remote browser session, hand back a CDP websocket URL, and tear the session down. Hermes' own browser stack (agent-browser+tools/browser_tool.py) connects to whatever CDP URL you return and drives the page from there — every provider gets the fullbrowser_*toolset for free.

`agent-browser`
`tools/browser_tool.py`
`browser_*`

The active provider is selected bybrowser.cloud_providerinconfig.yaml; the dispatcher intools/browser_tool.pyis a pure registry lookup with no per-provider conditionals.

`browser.cloud_provider`
`config.yaml`
`tools/browser_tool.py`

## Discovery​

Hermes scans for browser backends in three places:

1. Bundled—<repo>/plugins/browser/<name>/(auto-loaded withkind: backend)
2. User—~/.hermes/plugins/browser/<name>/(opt-in viaplugins.enabledorhermes plugins enable <name>)
3. Pip— packages declaring ahermes_agent.pluginsentry point

`<repo>/plugins/browser/<name>/`
`kind: backend`
`~/.hermes/plugins/browser/<name>/`
`plugins.enabled`
`hermes plugins enable <name>`
`hermes_agent.plugins`

Each plugin'sregister(ctx)callsctx.register_browser_provider(...), which puts the instance into the registry inagent/browser_registry.py.

`register(ctx)`
`ctx.register_browser_provider(...)`
`agent/browser_registry.py`

## Directory structure​

```
plugins/browser/my-backend/├── __init__.py     # register() entry point├── provider.py     # BrowserProvider subclass└── plugin.yaml     # Manifest with kind: backend and provides_browser_providers
```

plugin.yaml:

`plugin.yaml`

```
name: browser-my-backendversion: 1.0.0description: "My cloud browser backend. Requires MY_BACKEND_API_KEY."author: youkind: backendprovides_browser_providers:  - my-backend
```

__init__.py:

`__init__.py`

```
from plugins.browser.my_backend.provider import MyBackendProviderdef register(ctx) -> None:    ctx.register_browser_provider(MyBackendProvider())
```

## The BrowserProvider ABC​

Implementagent.browser_provider.BrowserProvider. Three lifecycle methods plus identity:

`agent.browser_provider.BrowserProvider`

```
from agent.browser_provider import BrowserProviderclass MyBackendProvider(BrowserProvider):    @property    def name(self) -> str:        return "my-backend"          # the browser.cloud_provider config value    @property    def display_name(self) -> str:        return "My Backend"          # shown in `hermes tools`    def is_available(self) -> bool:        """Cheap check only — env var present, dep importable.        NO network calls: runs at tool-registration time and on every        `hermes tools` paint."""        return bool(os.environ.get("MY_BACKEND_API_KEY"))    def create_session(self, task_id: str) -> dict:        """Create a remote browser session; return the session-metadata contract."""        session = my_api.create_browser(...)        return {            "session_name": f"my-backend-{task_id}",  # unique agent-browser session name            "bb_session_id": session.id,              # provider session ID (for cleanup)            "cdp_url": session.cdp_ws_url,            # CDP websocket URL            "features": {"stealth": True},            # feature flags you enabled        }    def close_session(self, session_id: str) -> bool:        """Terminate by provider session ID. Log-and-return-False on error —        never raise, so the dispatcher's cleanup loop keeps moving."""        ...    def emergency_cleanup(self, session_id: str) -> None:        """Best-effort teardown from atexit/signal handlers. Must not raise."""        ...
```

### The session-metadata contract​

create_session()must return at leastsession_name,bb_session_id,cdp_url, andfeatures. Two quirks worth knowing:

`create_session()`
`session_name`
`bb_session_id`
`cdp_url`
`features`
- bb_session_idis a legacy key namekept verbatim for backward compatibility withtools/browser_tool.py— it holdsyourprovider's session ID regardless of vendor. Don't rename it.
- create_session()may raise—ValueErrorfor missing credentials,RuntimeErrorfor network/API failures. The dispatcher surfaces these to the user. This differs fromclose_session/emergency_cleanup, which must never raise.

`bb_session_id`
`tools/browser_tool.py`
`create_session()`
`ValueError`
`RuntimeError`
`close_session`
`emergency_cleanup`

An optionalexternal_call_idkey supports managed-gateway billing.

`external_call_id`

### get_setup_schema()— thehermes toolspicker row​

`get_setup_schema()`
`hermes tools`

Override this to appear as a first-class option in the Browser Automation picker with API-key prompts and an install hook:

```
def get_setup_schema(self) -> dict:    return {        "name": "My Backend",        "badge": "paid",        "tag": "Cloud browser with stealth and proxies",        "env_vars": [            {"key": "MY_BACKEND_API_KEY",             "prompt": "My Backend API key",             "url": "https://mybackend.example"},        ],        "post_setup": "agent_browser",   # auto-installs the agent-browser npm dep    }
```

Per the project standard for tool backends: if a backend can't be selected and configured throughhermes tools, it isn't done — "set this env var manually" is not an integration.

`hermes tools`

## Users configure it​

```
browser:  cloud_provider: my-backend
```

## Reference implementations​

The three bundled providers underplugins/browser/are the canonical examples, in ascending complexity:firecrawl(simplest),browser_use, andbrowserbase(stealth/proxy/keep-alive feature flags with graceful fallback when paid features are unavailable). Copy the closest one.

`plugins/browser/`
`firecrawl`
`browser_use`
`browserbase`

## Checklist​

- nameis lowercase and stable (it's a config value users write)
- is_available()makes zero network calls
- create_session()returns the full metadata contract (bb_session_idkey name intact)
- close_session()/emergency_cleanup()never raise
- get_setup_schema()exposes your env vars sohermes toolscan configure the backend
- plugin.yamldeclareskind: backend+provides_browser_providers

`name`
`is_available()`
`create_session()`
`bb_session_id`
`close_session()`
`emergency_cleanup()`
`get_setup_schema()`
`hermes tools`
`plugin.yaml`
`kind: backend`
`provides_browser_providers`