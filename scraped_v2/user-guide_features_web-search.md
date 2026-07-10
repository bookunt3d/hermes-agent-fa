- 
- Features
- Media & Web
- Web Search

# Web Search & Extract

Hermes Agent includes two model-callable web tools backed by multiple providers:

- web_search— search the web and return ranked results
- web_extract— fetch and extract readable content from one or more URLs

`web_search`
`web_extract`

Both are configured through a single backend selection. Providers are chosen viahermes toolsor set directly inconfig.yaml.

`hermes tools`
`config.yaml`

## Backends​

| Provider | Env Var | Search | Extract | Free tier |
| --- | --- | --- | --- | --- |
| Firecrawl(default) | FIRECRAWL_API_KEY | ✔ | ✔ | 500 credits/mo |
| SearXNG | SEARXNG_URL | ✔ | — | ✔ Free (self-hosted) |
| Brave Search (free tier) | BRAVE_SEARCH_API_KEY | ✔ | — | 2 000 queries/mo |
| DDGS (DuckDuckGo) | — (no key) | ✔ | — | ✔ Free |
| Tavily | TAVILY_API_KEY | ✔ | ✔ | 1 000 searches/mo |
| Exa | EXA_API_KEY | ✔ | ✔ | 1 000 searches/mo |
| Parallel | PARALLEL_API_KEY | ✔ | ✔ | Paid |
| xAI (Grok) | XAI_API_KEYorhermes auth login xai-oauth | ✔ | — | Paid (SuperGrok or per-token) |

`FIRECRAWL_API_KEY`
`SEARXNG_URL`
`BRAVE_SEARCH_API_KEY`
`TAVILY_API_KEY`
`EXA_API_KEY`
`PARALLEL_API_KEY`
`XAI_API_KEY`
`hermes auth login xai-oauth`

Brave Search, DDGS, and xAI aresearch-only— pair any of them with Firecrawl/Tavily/Exa/Parallel when you also needweb_extract. DDGS uses theddgsPython packageunder the hood; if it isn't already installed, runpip install ddgs(or let Hermes lazy-install it on first use). xAI runs Grok's server-sideweb_searchtool on the Responses API — results are LLM-generated rather than index-backed, so titles, descriptions, and URL choice are all model output (see thetrust-model caveatbelow).

`web_extract`
`ddgs`
`pip install ddgs`
`web_search`

Per-capability split:you can use different providers for search and extract independently — for example SearXNG (free) for search and Firecrawl for extract. SeePer-capability configurationbelow.

If you have a paidNous Portalsubscription, web search and extract are available through theTool Gatewayvia managed Firecrawl — no API key needed. New installs can runhermes setup --portalto log in and turn on all gateway tools at once; existing installs can flip just web viahermes tools.

`hermes setup --portal`
`hermes tools`

## Howweb_extracthandles long pages​

`web_extract`

Backends return raw page markdown, which can be huge (forum threads, docs sites, news articles with embedded comments). To keep your context window usable and your costs down,web_extractruns returned content through theweb_extractauxiliary modelbefore handing it to the agent. Behavior is purely size-driven:

`web_extract`
`web_extract`
| Page size (characters) | What happens |
| --- | --- |
| Under 5 000 | Returned as-is — no LLM call, full markdown reaches the agent |
| 5 000 – 500 000 | Single-pass summary via theweb_extractauxiliary model, capped at ~5 000 chars of output |
| 500 000 – 2 000 000 | Chunked: split into 100 k-char chunks, summarize each in parallel, then synthesize a final summary (~5 000 chars) |
| Over 2 000 000 | Refused with a hint to use a more focused source URL |

`web_extract`

The summary keeps quotes, code blocks, and key facts in their original formatting — it's a content compressor, not a paraphraser. If summarization fails or times out, Hermes falls back to the first ~5 000 chars of raw content rather than a useless error.

### Which model does the summarizing?​

Theweb_extractauxiliary task. By default (auxiliary.web_extract.provider: "auto"), this is yourmain chat model— same provider, same model ashermes model. That's fine for most setups, but on expensive reasoning models (Opus, MiniMax M2.7, etc.) every long-page extract adds meaningful cost.

`web_extract`
`auxiliary.web_extract.provider: "auto"`
`hermes model`

To route extraction summaries to a cheap, fast model regardless of your main:

```
# ~/.hermes/config.yamlauxiliary:  web_extract:    provider: openrouter    model: google/gemini-3-flash-preview    timeout: 360       # seconds; raise if you hit summarization timeouts
```

Or pick interactively:hermes model→Configure auxiliary models→web_extract.

`hermes model`
`web_extract`

SeeAuxiliary Modelsfor the full reference and per-task override patterns.

### When summarization gets in the way​

If you specifically need raw, unsummarized page content — for example, you're scraping a structured page where the LLM summary would drop important fields — usebrowser_navigate+browser_snapshotinstead. The browser tool returns the live accessibility tree without auxiliary-model rewriting (subject to its own 8 000-char snapshot cap on huge pages).

`browser_navigate`
`browser_snapshot`

## Setup​

### Quick setup viahermes tools​

`hermes tools`

Runhermes tools, navigate toWeb Search & Extract, and pick a provider. The wizard prompts for the required URL or API key and writes it to your config.

`hermes tools`

```
hermes tools
```

### Firecrawl (default)​

Full-featured search and extract. Recommended for most users.

```
# ~/.hermes/.envFIRECRAWL_API_KEY=fc-your-key-here
```

Get a key atfirecrawl.dev. The free tier includes 500 credits/month.

Self-hosted Firecrawl:Point at your own instance instead of the cloud API:

```
# ~/.hermes/.envFIRECRAWL_API_URL=http://localhost:3002
```

WhenFIRECRAWL_API_URLis set, the API key is optional (disable server auth withUSE_DB_AUTHENTICATION=false).

`FIRECRAWL_API_URL`
`USE_DB_AUTHENTICATION=false`

### SearXNG (free, self-hosted)​

SearXNG is a privacy-respecting, open-source metasearch engine that aggregates results from 70+ search engines.No API key required— just point Hermes at a running SearXNG instance.

SearXNG issearch-only—web_extractrequires a separate extract provider.

`web_extract`

#### Option A — Self-host with Docker (recommended)​

This gives you a private instance with no rate limits.

1. Create a working directory:

```
mkdir -p ~/searxng/searxngcd ~/searxng
```

2. Write adocker-compose.yml:

`docker-compose.yml`

```
# ~/searxng/docker-compose.ymlservices:  searxng:    image: searxng/searxng:latest    container_name: searxng    ports:      - "8888:8080"    volumes:      - ./searxng:/etc/searxng:rw    environment:      - SEARXNG_BASE_URL=http://localhost:8888/    restart: unless-stopped
```

3. Start the container:

```
docker compose up -d
```

4. Enable the JSON API format:

SearXNG ships with JSON output disabled by default. Copy the generated config and enable it:

```
# Copy the auto-generated config out of the containerdocker cp searxng:/etc/searxng/settings.yml ~/searxng/searxng/settings.yml
```

Open~/searxng/searxng/settings.yml.
Ifuse_default_settings: trueis present, the file only contains your overrides. All other settings are inherited from the built-in defaults.
To enable JSON responses for Hermes, add the following override:

`~/searxng/searxng/settings.yml`
`use_default_settings: true`

```
search:  formats:    - html    - json
```

Yoursettings.ymlshould look similar to:

`settings.yml`

```
# Read the documentation before extending the defaults:# https://docs.searxng.org/admin/settings/use_default_settings: trueserver:  secret_key: "abcdef12345678"  image_proxy: truesearch:  formats:    - html    - json
```

5. Restart to apply:

```
docker cp ~/searxng/searxng/settings.yml searxng:/etc/searxng/settings.ymldocker restart searxng
```

6. Verify it works:

```
curl -s "http://localhost:8888/search?q=test&format=json" | python3 -c \  "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"results\"])} results')"
```

You should see something like10 results. If you get a403 Forbidden, JSON format is still disabled — recheck step 4.

`10 results`
`403 Forbidden`

7. Configure Hermes:

```
# ~/.hermes/.envSEARXNG_URL=http://localhost:8888
```

Then select SearXNG as the search backend in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
web:  search_backend: "searxng"
```

Or set viahermes tools→ Web Search & Extract → SearXNG.

`hermes tools`

#### Option B — Use a public instance​

Public SearXNG instances are listed atsearx.space. Filter by instances that haveJSON format enabled(shown in the table).

```
# ~/.hermes/.envSEARXNG_URL=https://searx.example.com
```

Public instances have rate limits, variable uptime, and may disable JSON format at any time. For production use, self-hosting is strongly recommended.

#### Pair SearXNG with an extract provider​

SearXNG handles search; you need a separate provider forweb_extract. Use the per-capability keys:

`web_extract`

```
# ~/.hermes/config.yamlweb:  search_backend: "searxng"  extract_backend: "firecrawl"   # or tavily, exa, parallel
```

With this config, Hermes uses SearXNG for all search queries and Firecrawl for URL extraction — combining free search with high-quality extraction.

### Tavily​

AI-optimised search and extract with a generous free tier.

```
# ~/.hermes/.envTAVILY_API_KEY=tvly-your-key-here
```

Get a key atapp.tavily.com. The free tier includes 1 000 searches/month.

### Exa​

Neural search with semantic understanding. Good for research and finding conceptually related content.

```
# ~/.hermes/.envEXA_API_KEY=your-exa-key-here
```

Get a key atexa.ai. The free tier includes 1 000 searches/month.

### Parallel​

AI-native search and extraction with deep research capabilities.

```
# ~/.hermes/.envPARALLEL_API_KEY=your-parallel-key-here
```

Get access atparallel.ai.

### xAI (Grok)​

Routesweb_searchthrough Grok's server-sideweb_search toolon the Responses API. Grok runs the actual searching and returns the top results as structured JSON.

`web_search`

Works with either credential path — no new env vars, no new setup wizard:

```
# ~/.hermes/.env (env-var path)XAI_API_KEY=sk-xai-your-key-here
```

or for SuperGrok subscribers:

```
hermes auth login xai-oauth
```

Then select xAI as the search backend:

```
# ~/.hermes/config.yamlweb:  backend: "xai"
```

Optional knobs:

```
web:  backend: "xai"  xai:    model: grok-build-0.1        # reasoning model required by web_search (default)    allowed_domains:             # optional, max 5 — mutex with excluded_domains      - arxiv.org    excluded_domains:            # optional, max 5      - example-spam.com    timeout: 90                  # seconds (default)
```

Search-only— pair with Firecrawl / Tavily / Exa / Parallel if you also needweb_extract. On 401 the provider performs a single forced OAuth-token refresh and retries (covers mid-window revocation and opaque tokens the proactive expiry check can't decode); env-var credentials skip the retry.

`web_extract`

Unlike index-backed providers (Brave, Tavily, Exa) which return verbatim search-engine results, xAI is an LLM choosing which URLs to surface and writing the titles and descriptions itself. Thecontentof the query influences the output, so a maliciously crafted query (e.g. injected via untrusted upstream input the agent picked up) can in principle steer Grok into emitting attacker-chosen URLs. Treat returned URLs the same way you'd treat any model-generated link — validate before fetching, especially if the query came from untrusted input.

## Configuration​

### Single backend​

Set one provider for all web capabilities:

```
# ~/.hermes/config.yamlweb:  backend: "searxng"   # firecrawl | searxng | brave-free | ddgs | tavily | exa | parallel | xai
```

### Per-capability configuration​

Use different providers for search vs extract. This lets you combine free search (SearXNG) with a paid extract provider, or vice versa:

```
# ~/.hermes/config.yamlweb:  search_backend: "searxng"     # used by web_search  extract_backend: "firecrawl"  # used by web_extract
```

When per-capability keys are empty, both fall through toweb.backend. Whenweb.backendis also empty, the backend is auto-detected from whichever API key/URL is present.

`web.backend`
`web.backend`

Priority order (per capability):

1. web.search_backend/web.extract_backend(explicit per-capability)
2. web.backend(shared fallback)
3. Auto-detect from environment variables

`web.search_backend`
`web.extract_backend`
`web.backend`

### Auto-detection​

If no backend is explicitly configured, Hermes picks the first available one based on which credentials are set:

| Credential present | Auto-selected backend |
| --- | --- |
| FIRECRAWL_API_KEYorFIRECRAWL_API_URL | firecrawl |
| PARALLEL_API_KEY | parallel |
| TAVILY_API_KEY | tavily |
| EXA_API_KEY | exa |
| SEARXNG_URL | searxng |

`FIRECRAWL_API_KEY`
`FIRECRAWL_API_URL`
`PARALLEL_API_KEY`
`TAVILY_API_KEY`
`EXA_API_KEY`
`SEARXNG_URL`

xAI Web Search isnotin the auto-detection chain — havingXAI_API_KEYset (or being signed in via xAI Grok OAuth) does not automatically route web traffic through xAI, since those credentials are also used for inference / TTS / image gen and the user may want a different backend for web. Opt in explicitly withweb.backend: "xai".

`XAI_API_KEY`
`web.backend: "xai"`

## Verify your setup​

Runhermes setupto see which web backend is detected:

`hermes setup`

```
✅ Web Search & Extract (searxng)
```

Or check via the CLI:

```
# Activate the venv and run the web tools module directlysource ~/.hermes/hermes-agent/.venv/bin/activatepython -m tools.web_tools
```

This prints the active backend and its status:

```
✅ Web backend: searxng   Using SearXNG (search only): http://localhost:8888
```

## Troubleshooting​

### web_searchreturns{"success": false}​

`web_search`
`{"success": false}`
- CheckSEARXNG_URLis reachable:curl -s "http://localhost:8888/search?q=test&format=json"
- If you get HTTP 403, JSON format is disabled — addjsonto theformatslist insettings.ymland restart
- If you get a connection error, the container may not be running:docker ps | grep searxng

`SEARXNG_URL`
`curl -s "http://localhost:8888/search?q=test&format=json"`
`json`
`formats`
`settings.yml`
`docker ps | grep searxng`

### web_extractsays "search-only backend"​

`web_extract`

SearXNG cannot extract URL content. Setweb.extract_backendto a provider that supports extraction:

`web.extract_backend`

```
web:  search_backend: "searxng"  extract_backend: "firecrawl"  # or tavily / exa / parallel
```

### SearXNG returns 0 results​

Some public instances disable certain search engines or categories. Try:

- A different query
- A different public instance fromsearx.space
- Self-hosting your own instance for reliable results

### Rate limited on a public instance​

Switch to a self-hosted instance (seeOption Aabove). With Docker, your own instance has no rate limits.

### web_extractreturns truncated content with a "summarization timed out" note​

`web_extract`

The auxiliary model didn't finish summarizing within the configured timeout. Either:

- Raiseauxiliary.web_extract.timeoutinconfig.yaml(default 360s on fresh installs, 30s if the key is missing)
- Switch theweb_extractauxiliary task to a faster model (e.g.google/gemini-3-flash-preview) — seeHowweb_extracthandles long pages
- For pages where summarization is the wrong tool, usebrowser_navigateinstead

`auxiliary.web_extract.timeout`
`config.yaml`
`web_extract`
`google/gemini-3-flash-preview`
`web_extract`
`browser_navigate`

## Optional skill:searxng-search​

`searxng-search`

For agents that need to use SearXNG viacurldirectly (e.g. as a fallback when the web toolset isn't available), install thesearxng-searchoptional skill:

`curl`
`searxng-search`

```
hermes skills install official/research/searxng-search
```

This adds a skill that teaches the agent how to:

- Call the SearXNG JSON API viacurlor Python
- Filter by category (general,news,science, etc.)
- Handle pagination and error cases
- Fall back gracefully when SearXNG is unreachable

`curl`
`general`
`news`
`science`