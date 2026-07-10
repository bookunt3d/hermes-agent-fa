- 
- Developer Guide
- Extending
- Plugins
- Web Search Provider Plugins

# Building a Web Search Provider Plugin

Web-search provider plugins register a backend that servicesweb_search,web_extract, and (optionally) deep-crawl tool calls. Built-in providers — Firecrawl, SearXNG, Tavily, Exa, Parallel, Brave Search (free tier), xAI, and DDGS — all ship as plugins underplugins/web/<name>/. You can add a new one, or override a bundled one, by dropping a directory next to them.

`web_search`
`web_extract`
`plugins/web/<name>/`

Web search is one of severalbackend pluginsHermes supports. The others (with their own ABCs) areImage Generation Provider Plugins,Video Generation Provider Plugins,Memory Provider Plugins,Context Engine Plugins, andModel Provider Plugins. General tool/hook/CLI plugins live inBuild a Hermes Plugin.

## How discovery works​

Hermes scans for web-search backends in three places:

1. Bundled—<repo>/plugins/web/<name>/(auto-loaded withkind: backend, always available)
2. User—~/.hermes/plugins/web/<name>/(opt-in viaplugins.enabledorhermes plugins enable <name>)
3. Pip— packages declaring ahermes_agent.pluginsentry point

`<repo>/plugins/web/<name>/`
`kind: backend`
`~/.hermes/plugins/web/<name>/`
`plugins.enabled`
`hermes plugins enable <name>`
`hermes_agent.plugins`

Each plugin'sregister(ctx)function callsctx.register_web_search_provider(...)— that puts the instance into the registry inagent/web_search_registry.py. The active provider for each capability is picked by config:

`register(ctx)`
`ctx.register_web_search_provider(...)`
`agent/web_search_registry.py`
| Capability | Config key | Falls back to |
| --- | --- | --- |
| web_search | web.search_backend | web.backend |
| web_extract | web.extract_backend | web.backend |
| Deep crawl modes insideweb_extract | web.extract_backend | web.backend |

`web_search`
`web.search_backend`
`web.backend`
`web_extract`
`web.extract_backend`
`web.backend`
`web_extract`
`web.extract_backend`
`web.backend`

When neither key is set, Hermes auto-detects the backend from whichever API key/URL is present in the environment.hermes toolswalks users through selection.

`hermes tools`

## Directory structure​

```
plugins/web/my-backend/├── __init__.py     # register() entry point├── provider.py     # WebSearchProvider subclass└── plugin.yaml     # Manifest with kind: backend and provides_web_providers
```

brave_free/andddgs/are the smallest in-tree references —brave_freefor an API-key-gated search-only provider,ddgsfor a no-key provider that lazy-installs its SDK.

`brave_free/`
`ddgs/`
`brave_free`
`ddgs`

## The WebSearchProvider ABC​

Subclassagent.web_search_provider.WebSearchProvider. The only required members arename,is_available(), and whichever ofsearch()/extract()you implement. (Deep crawling is not a separate method — it's a mode ofextract().)

`agent.web_search_provider.WebSearchProvider`
`name`
`is_available()`
`search()`
`extract()`
`extract()`

```
# plugins/web/my-backend/provider.pyfrom __future__ import annotationsimport osfrom typing import Any, Dict, Listfrom agent.web_search_provider import WebSearchProviderclass MyBackendWebSearchProvider(WebSearchProvider):    """Minimal search-only provider against the My Backend HTTP API."""    @property    def name(self) -> str:        # Stable id used in web.search_backend / web.extract_backend / web.backend        # config keys. Lowercase, no spaces; hyphens permitted.        return "my-backend"    @property    def display_name(self) -> str:        # Human label shown in `hermes tools`. Defaults to `name`.        return "My Backend"    def is_available(self) -> bool:        # Cheap check — env var present, optional dep importable, etc.        # MUST NOT make network calls (runs on every `hermes tools` paint).        return bool(os.getenv("MY_BACKEND_API_KEY", "").strip())    def supports_search(self) -> bool:        return True    def supports_extract(self) -> bool:        return False    def search(self, query: str, limit: int = 5) -> Dict[str, Any]:        import httpx        api_key = os.environ["MY_BACKEND_API_KEY"]        try:            resp = httpx.get(                "https://api.example.com/search",                params={"q": query, "count": max(1, min(int(limit), 20))},                headers={"Authorization": f"Bearer {api_key}"},                timeout=15,            )            resp.raise_for_status()            data = resp.json()        except httpx.HTTPError as exc:            return {"success": False, "error": str(exc)}        # Response shape is fixed — see "Response shape" below.        return {            "success": True,            "data": {                "web": [                    {                        "title": item.get("title", ""),                        "url": item.get("url", ""),                        "description": item.get("snippet", ""),                        "position": idx + 1,                    }                    for idx, item in enumerate(data.get("results", []))                ],            },        }
```

```
# plugins/web/my-backend/__init__.pyfrom plugins.web.my_backend.provider import MyBackendWebSearchProviderdef register(ctx) -> None:    """Plugin entry point — called once at load time."""    ctx.register_web_search_provider(MyBackendWebSearchProvider())
```

## plugin.yaml​

```
name: web-my-backendversion: 1.0.0description: "My Backend web search — Bearer-auth REST API"author: Your Namekind: backendprovides_web_providers:  - my-backendrequires_env:  - MY_BACKEND_API_KEY
```

| Key | Purpose |
| --- | --- |
| kind: backend | Routes the plugin through the backend-loading path |
| provides_web_providers | List of providernames this plugin registers — used by the loader to advertise the plugin inhermes toolseven beforeregister()runs |
| requires_env | Interactive credential prompt duringhermes plugins install(seeBuild a Hermes Pluginfor the rich format) |

`kind: backend`
`provides_web_providers`
`name`
`hermes tools`
`register()`
`requires_env`
`hermes plugins install`

## ABC reference​

Full contract inagent/web_search_provider.py. Methods you may override:

`agent/web_search_provider.py`
| Member | Required | Default | Purpose |
| --- | --- | --- | --- |
| name | ✅ | — | Stable id used inweb.*_backendconfig |
| display_name | — | name | Label shown inhermes tools |
| is_available() | ✅ | — | Cheap availability gate — env vars, optional deps |
| supports_search() | — | True | Capability flag forweb_searchrouting |
| supports_extract() | — | False | Capability flag forweb_extractrouting |
| search(query, limit) | conditional | raises | Required whensupports_search()returnsTrue |
| extract(urls, **kwargs) | conditional | raises | Required whensupports_extract()returnsTrue |

`name`
`web.*_backend`
`display_name`
`name`
`hermes tools`
`is_available()`
`supports_search()`
`True`
`web_search`
`supports_extract()`
`False`
`web_extract`
`search(query, limit)`
`supports_search()`
`True`
`extract(urls, **kwargs)`
`supports_extract()`
`True`

Providers can advertise multiple capabilities from a single class — Firecrawl, Tavily, Exa, and Parallel all implement both search and extract. Brave Search and DDGS are search-only; SearXNG is search-only with a documented "pair me with an extract provider" workflow.

## Response shape​

The tool wrapper expects a fixed envelope so it doesn't have to translate between backends.

Search success:

```
{    "success": True,    "data": {        "web": [            {"title": str, "url": str, "description": str, "position": int},            ...        ],    },}
```

Extract success:

```
{    "success": True,    "data": [        {            "url": str,            "title": str,            "content": str,            "raw_content": str,            "metadata": dict,    # optional            "error": str,        # optional, only on per-URL failure        },        ...    ],}
```

Either capability, on failure:

```
{"success": False, "error": "human-readable message"}
```

Bothsearch()andextract()may beasync def— the dispatcher detects coroutine functions viainspect.iscoroutinefunctionand awaits accordingly. Sync implementations that do blocking I/O (HTTP, SDK calls) are fine for small backends; the dispatcher handles threading.

`search()`
`extract()`
`async def`
`inspect.iscoroutinefunction`

## Capability flags​

Hermes routes calls to the right provider based on thesupports_*flags. A common multi-provider setup:

`supports_*`

```
# ~/.hermes/config.yamlweb:  search_backend: "brave-free"     # search-only, fast, free 2k/mo  extract_backend: "firecrawl"     # extract + crawl, paid quota
```

Whenweb.search_backendorweb.extract_backendaren't set, both fall through toweb.backend. When that's also unset, Hermes picks the first available provider that supports the requested capability based on env-var presence.

`web.search_backend`
`web.extract_backend`
`web.backend`

If your provider only supports one capability, leave the other flags at their default (False) and the registry will skip it for that tool — users won't see misleading "provider X failed" errors when they're using X only for search and asking the agent to extract.

`False`

## How Hermes wires it into the tools​

Theweb_searchandweb_extracttools live intools/web_tools.py. At call time they:

`web_search`
`web_extract`
`tools/web_tools.py`
1. Read the relevant config key (web.search_backendforweb_search,web.extract_backendforweb_extract)
2. Ask the registry for the provider with thatname
3. Checkis_available()and the matchingsupports_*()flag
4. Dispatch tosearch()/extract()(deep crawl runs as a mode insideextract()), awaiting if the method is a coroutine
5. JSON-serialize the response envelope and hand it back to the LLM

`web.search_backend`
`web_search`
`web.extract_backend`
`web_extract`
`name`
`is_available()`
`supports_*()`
`search()`
`extract()`
`extract()`

Errors surface as the tool result; the LLM decides how to explain them. If no provider is registered (or every available one fails the capability gate), the tool returns a helpful error pointing athermes tools.

`hermes tools`

## Lazy-installing optional dependencies​

If your provider wraps a third-party SDK (like DDGS does with theddgspackage), don'timportit at module top level. Usetools.lazy_deps.ensure(...)insideis_available()orsearch()— Hermes will install the package on first use, gated bysecurity.allow_lazy_installs. SeeBuild a Hermes Plugin → Lazy-installfor the security model.

`ddgs`
`import`
`tools.lazy_deps.ensure(...)`
`is_available()`
`search()`
`security.allow_lazy_installs`

## Reference implementations​

- plugins/web/brave_free/— small, API-key-gated, search-only HTTP provider. Good starting template.
- plugins/web/ddgs/— no-key provider that lazy-installs its SDK. Useful pattern for backends that wrap a Python package.
- plugins/web/firecrawl/— full multi-capability provider (search + extract + crawl) with multiple format modes.
- plugins/web/searxng/— self-hosted, URL-configured backend with no auth.
- plugins/web/xai/— LLM-backed search via Grok's server-sideweb_searchtool. Shows how to reuse an existing OAuth/env-var credential surface (tools/xai_http.py) without adding new env vars, and how to write a cheapis_available()that honors the no-network contract.

`plugins/web/brave_free/`
`plugins/web/ddgs/`
`plugins/web/firecrawl/`
`plugins/web/searxng/`
`plugins/web/xai/`
`web_search`
`tools/xai_http.py`
`is_available()`

## Distribute via pip​

```
# pyproject.toml[project.entry-points."hermes_agent.plugins"]my-backend-web = "my_backend_web_package"
```

my_backend_web_packagemust expose a top-levelregisterfunction. SeeDistribute via pipin the general plugin guide for the full setup.

`my_backend_web_package`
`register`

## Related pages​

- Web Search— user-facing feature documentation and per-backend configuration
- Plugins overview— all plugin types at a glance
- Build a Hermes Plugin— general tools/hooks/slash commands guide