---
layout: docs
title: "Features_Memory Providers"
permalink: /docs/user-guide/features/memory-providers/
---

- 
- Features
- Core
- Memory Providers

# Memory Providers

Hermes Agent ships with 8 external memory provider plugins that give the agent persistent, cross-session knowledge beyond the built-in MEMORY.md and USER.md. Onlyoneexternal provider can be active at a time — the built-in memory is always active alongside it.

## Quick Start​

```
hermes memory setup      # interactive picker + configurationhermes memory status     # check what's activehermes memory off        # disable external provider
```

You can also select the active memory provider viahermes plugins→ Provider Plugins → Memory Provider.

`hermes plugins`

Or set manually in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
memory:  provider: openviking   # or honcho, mem0, hindsight, holographic, retaindb, byterover, supermemory
```

## How It Works​

When a memory provider is active, Hermes automatically:

1. Injects provider contextinto the system prompt (what the provider knows)
2. Prefetches relevant memoriesbefore each turn (background, non-blocking)
3. Syncs conversation turnsto the provider after each response
4. Extracts memories on session end(for providers that support it)
5. Mirrors built-in memory writesto the external provider
6. Adds provider-specific toolsso the agent can search, store, and manage memories

The built-in memory (MEMORY.md / USER.md) continues to work exactly as before. The external provider is additive.

## Available Providers​

### Honcho​

AI-native cross-session user modeling with dialectic reasoning, session-scoped context injection, semantic search, and persistent conclusions. Base context now includes the session summary alongside user representation and peer cards, giving the agent awareness of what has already been discussed.

|  |  |
| --- | --- |
| Best for | Multi-agent systems with cross-session context, user-agent alignment |
| Requires | pip install honcho-ai+API keyor self-hosted instance |
| Data storage | Honcho Cloud or self-hosted |
| Cost | Honcho pricing (cloud) / free (self-hosted) |

`pip install honcho-ai`

Tools (5):honcho_profile(read/update peer card),honcho_search(semantic search),honcho_context(session context — summary, representation, card, messages),honcho_reasoning(LLM-synthesized),honcho_conclude(create/delete conclusions)

`honcho_profile`
`honcho_search`
`honcho_context`
`honcho_reasoning`
`honcho_conclude`

Architecture:Two-layer context injection — a base layer (session summary + representation + peer card, refreshed oncontextCadence) plus a dialectic supplement (LLM reasoning, refreshed ondialecticCadence). The dialectic automatically selects cold-start prompts (general user facts) vs. warm prompts (session-scoped context) based on whether base context exists.

`contextCadence`
`dialecticCadence`

Three orthogonal config knobscontrol cost and depth independently:

- contextCadence— how often the base layer refreshes (API call frequency)
- dialecticCadence— how often the dialectic LLM fires (LLM call frequency)
- dialecticDepth— how many.chat()passes per dialectic invocation (1–3, depth of reasoning)

`contextCadence`
`dialecticCadence`
`dialecticDepth`
`.chat()`

The auto-injected dialectic also scales its reasoning level by query length (longer query → deeper reasoning, capped atreasoningLevelCap); seeQuery-Adaptive Reasoning Level.

`reasoningLevelCap`

Setup Wizard:

```
hermes memory setup        # select "honcho" — runs the Honcho-specific post-setup
```

The legacyhermes honcho setupcommand still works (it now redirects tohermes memory setup), but is only registered after Honcho is selected as the active memory provider.

`hermes honcho setup`
`hermes memory setup`

Config:$HERMES_HOME/honcho.json(profile-local) or~/.honcho/config.json(global). Resolution order:$HERMES_HOME/honcho.json>~/.hermes/honcho.json>~/.honcho/config.json. See theconfig referenceand theHoncho integration guide.

`$HERMES_HOME/honcho.json`
`~/.honcho/config.json`
`$HERMES_HOME/honcho.json`
`~/.hermes/honcho.json`
`~/.honcho/config.json`
| Key | Default | Description |
| --- | --- | --- |
| apiKey | -- | API key fromapp.honcho.dev |
| baseUrl | -- | Base URL for self-hosted Honcho |
| peerName | -- | User peer identity |
| aiPeer | host key | AI peer identity (one per profile) |
| workspace | host key | Shared workspace ID |
| contextTokens | null(uncapped) | Token budget for auto-injected context per turn. Truncates at word boundaries |
| contextCadence | 1 | Minimum turns betweencontext()API calls (base layer refresh) |
| dialecticCadence | 2 | Minimum turns betweenpeer.chat()LLM calls. Recommended 1–5. Only applies tohybrid/contextmodes |
| dialecticDepth | 1 | Number of.chat()passes per dialectic invocation. Clamped 1–3. Pass 0: cold/warm prompt, pass 1: self-audit, pass 2: reconciliation |
| dialecticDepthLevels | null | Optional array of reasoning levels per pass, e.g.["minimal", "low", "medium"]. Overrides proportional defaults |
| dialecticReasoningLevel | 'low' | Base reasoning level:minimal,low,medium,high,max |
| dialecticDynamic | true | Whentrue, model can override reasoning level per-call via tool param |
| dialecticMaxChars | 600 | Max chars of dialectic result injected into system prompt |
| recallMode | 'hybrid' | hybrid(auto-inject + tools),context(inject only),tools(tools only) |
| writeFrequency | 'async' | When to flush messages:async(background thread),turn(sync),session(batch on end), or integer N |
| saveMessages | true | Whether to persist messages to Honcho API |
| observationMode | 'directional' | directional(all on) orunified(shared pool). Override withobservationobject |
| messageMaxChars | 25000 | Max chars per message (chunked if exceeded) |
| dialecticMaxInputChars | 10000 | Max chars for dialectic query input topeer.chat() |
| sessionStrategy | 'per-directory' | per-directory,per-repo,per-session,global |
| pinUserPeer | false | Gateway only. Whentrue, every non-agent gateway user collapses topeerName; the pin overrides all aliases |
| userPeerAliases | {} | Gateway only. Maps runtime IDs to peers ({"7654321": "alice"}). Many-to-one |
| runtimePeerPrefix | "" | Gateway only. Namespaces unknown runtime IDs (telegram_7654321) when no alias matches |

`apiKey`
`baseUrl`
`peerName`
`aiPeer`
`workspace`
`contextTokens`
`null`
`contextCadence`
`1`
`context()`
`dialecticCadence`
`2`
`peer.chat()`
`hybrid`
`context`
`dialecticDepth`
`1`
`.chat()`
`dialecticDepthLevels`
`null`
`["minimal", "low", "medium"]`
`dialecticReasoningLevel`
`'low'`
`minimal`
`low`
`medium`
`high`
`max`
`dialecticDynamic`
`true`
`true`
`dialecticMaxChars`
`600`
`recallMode`
`'hybrid'`
`hybrid`
`context`
`tools`
`writeFrequency`
`'async'`
`async`
`turn`
`session`
`saveMessages`
`true`
`observationMode`
`'directional'`
`directional`
`unified`
`observation`
`messageMaxChars`
`25000`
`dialecticMaxInputChars`
`10000`
`peer.chat()`
`sessionStrategy`
`'per-directory'`
`per-directory`
`per-repo`
`per-session`
`global`
`pinUserPeer`
`false`
`true`
`peerName`
`userPeerAliases`
`{}`
`{"7654321": "alice"}`
`runtimePeerPrefix`
`""`
`telegram_7654321`

```
{  "apiKey": "your-key-from-app.honcho.dev",  "hosts": {    "hermes": {      "enabled": true,      "aiPeer": "hermes",      "peerName": "your-name",      "workspace": "hermes"    }  }}
```

```
{  "baseUrl": "http://localhost:8000",  "hosts": {    "hermes": {      "enabled": true,      "aiPeer": "hermes",      "peerName": "your-name",      "workspace": "hermes"    }  }}
```

`hermes honcho`

If you previously usedhermes honcho setup, your config and all server-side data are intact. Just re-enable through the setup wizard again or manually setmemory.provider: honchoto reactivate via the new system.

`hermes honcho setup`
`memory.provider: honcho`

Multi-peer setup:

Honcho models conversations as peers exchanging messages — one user peer plus one AI peer per Hermes profile, all sharing a workspace. The workspace is the shared environment: the user peer is global across profiles, each AI peer is its own identity. Every AI peer builds an independent representation / card from its own observations, so acoderprofile stays code-oriented while awriterprofile stays editorial against the same user.

`coder`
`writer`

The mapping:

| Concept | What it is |
| --- | --- |
| Workspace | Shared environment. All Hermes profiles under one workspace see the same user identity. |
| User peer(peerName) | The human. Shared across profiles in the workspace. |
| AI peer(aiPeer) | One per Hermes profile. Host keyhermes→ default;hermes.<profile>for others. |
| Observation | Per-peer toggles controlling what Honcho models from whose messages.directional(default, all four on) orunified(single-observer pool). |

`peerName`
`aiPeer`
`hermes`
`hermes.<profile>`
`directional`
`unified`

### New profile, fresh Honcho peer​

```
hermes profile create coder --clone
```

--clonecreates ahermes.coderhost block inhoncho.jsonwithaiPeer: "coder", sharedworkspace, inheritedpeerName,recallMode,writeFrequency,observation, etc. The AI peer is eagerly created in Honcho so it exists before the first message.

`--clone`
`hermes.coder`
`honcho.json`
`aiPeer: "coder"`
`workspace`
`peerName`
`recallMode`
`writeFrequency`
`observation`

### Existing profiles, backfill Honcho peers​

```
hermes honcho sync
```

Scans every Hermes profile, creates host blocks for any profile without one, inherits settings from the defaulthermesblock, and creates the new AI peers eagerly. Idempotent — skips profiles that already have a host block.

`hermes`

### Per-profile observation​

Each host block can override the observation config independently. Example: a code-focused profile where the AI peer observes the user but doesn't self-model:

```
"hermes.coder": {  "aiPeer": "coder",  "observation": {    "user": { "observeMe": true, "observeOthers": true },    "ai":   { "observeMe": false, "observeOthers": true }  }}
```

Observation toggles (one set per peer):

| Toggle | Effect |
| --- | --- |
| observeMe | Honcho builds a representation of this peer from its own messages |
| observeOthers | This peer observes the other peer's messages (feeds cross-peer reasoning) |

`observeMe`
`observeOthers`

Presets viaobservationMode:

`observationMode`
- "directional"(default) — all four flags on. Full mutual observation; enables cross-peer dialectic.
- "unified"— userobserveMe: true, AIobserveOthers: true, rest false. Single-observer pool; AI models the user but not itself, user peer only self-models.

`"directional"`
`"unified"`
`observeMe: true`
`observeOthers: true`

Server-side toggles set via theHoncho dashboardwin over local defaults — synced back at session init.

See theHoncho pagefor the full observation reference.

### Gateway identity mapping​

The peer model above covers CLI, TUI, and desktop sessions, where every conversation resolves topeerName. Thegatewayadds a second axis: users arrive with platform-native runtime IDs (Telegram UID, Discord snowflake, Slack user), and three keys decide which peer each ID resolves to.

`peerName`
| Key | Effect |
| --- | --- |
| pinUserPeer: true | Every non-agent gateway user collapses topeerName. The pin is checked first, so it overrides all aliases — pick it only when no user-side identity needs its own peer |
| userPeerAliases | Maps specific runtime IDs to peers ({"7654321": "alice"}). The home for routing distinct identities — including agents that each carry their own peer |
| runtimePeerPrefix | Namespaces any unmapped runtime ID (telegram_7654321) so platforms with same-shaped IDs don't collide |

`pinUserPeer: true`
`peerName`
`userPeerAliases`
`{"7654321": "alice"}`
`runtimePeerPrefix`
`telegram_7654321`

Off-gateway these keys do nothing.hermes memory setuponly prompts for them when it detects a connected gateway platform. See theHoncho pagefor the resolver ladder and the setup flow.

`hermes memory setup`

```
{  "apiKey": "your-key",  "workspace": "hermes",  "peerName": "eri",  "hosts": {    "hermes": {      "enabled": true,      "aiPeer": "hermes",      "workspace": "hermes",      "peerName": "eri",      "recallMode": "hybrid",      "writeFrequency": "async",      "sessionStrategy": "per-directory",      "observation": {        "user": { "observeMe": true, "observeOthers": true },        "ai": { "observeMe": true, "observeOthers": true }      },      "dialecticReasoningLevel": "low",      "dialecticDynamic": true,      "dialecticCadence": 2,      "dialecticDepth": 1,      "dialecticMaxChars": 600,      "contextCadence": 1,      "messageMaxChars": 25000,      "saveMessages": true    },    "hermes.coder": {      "enabled": true,      "aiPeer": "coder",      "workspace": "hermes",      "peerName": "eri",      "recallMode": "tools",      "observation": {        "user": { "observeMe": true, "observeOthers": false },        "ai": { "observeMe": true, "observeOthers": true }      }    },    "hermes.writer": {      "enabled": true,      "aiPeer": "writer",      "workspace": "hermes",      "peerName": "eri"    }  },  "sessions": {    "/home/user/myproject": "myproject-main"  }}
```

See theconfig referenceandHoncho integration guide.

### OpenViking​

Context database by Volcengine (ByteDance) with filesystem-style knowledge hierarchy, tiered retrieval, and automatic memory extraction into 6 categories.

|  |  |
| --- | --- |
| Best for | Self-hosted knowledge management with structured browsing |
| Requires | pip install openviking+ running server |
| Data storage | Self-hosted (local or cloud) |
| Cost | Free (open-source, AGPL-3.0) |

`pip install openviking`

Tools:viking_search(semantic search),viking_read(tiered: abstract/overview/full),viking_browse(filesystem navigation),viking_remember(store facts),viking_add_resource(ingest URLs/docs)

`viking_search`
`viking_read`
`viking_browse`
`viking_remember`
`viking_add_resource`

Setup:

```
# Start the OpenViking server firstpip install openvikingopenviking-server# Then configure Hermeshermes memory setup    # select "openviking"# Or manually:hermes config set memory.provider openvikingecho "OPENVIKING_ENDPOINT=http://localhost:1933" >> ~/.hermes/.env# Authenticated servers should use a user/admin API key:echo "OPENVIKING_API_KEY=..." >> ~/.hermes/.env
```

Key features:

- Tiered context loading: L0 (~100 tokens) → L1 (~2k) → L2 (full)
- Automatic memory extraction on session commit (profile, preferences, entities, events, cases, patterns)
- viking://URI scheme for hierarchical knowledge browsing

`viking://`

OPENVIKING_ACCOUNTandOPENVIKING_USERare used for local/trusted mode.OPENVIKING_AGENTis Hermes' peer ID in OpenViking for peer-scoped memories.

`OPENVIKING_ACCOUNT`
`OPENVIKING_USER`
`OPENVIKING_AGENT`

### Mem0​

Server-side LLM fact extraction with semantic search, reranking, and automatic deduplication. Three connection modes:Platform(Mem0 Cloud),self-hosted dashboard(a Mem0 server you run via Docker), andOSS(Mem0 in-process with your own LLM + vector store).

|  |  |
| --- | --- |
| Best for | Hands-off memory management — Mem0 handles extraction automatically |
| Requires | pip install mem0ai+ API key (platform), a running Mem0 server (self-hosted dashboard), or an LLM + vector store (OSS) |
| Data storage | Mem0 Cloud (platform), your own Mem0 server (self-hosted dashboard), or in-process (OSS) |
| Cost | Mem0 pricing (platform) / free (self-hosted or OSS) |

`pip install mem0ai`

Tools (4):mem0_search(semantic search; optional reranking in platform mode, off by default),mem0_add(store verbatim facts),mem0_update(update by ID),mem0_delete(delete by ID)

`mem0_search`
`mem0_add`
`mem0_update`
`mem0_delete`

Setup (Platform):

```
hermes memory setup    # select "mem0" → "Platform"# Or manually:hermes config set memory.provider mem0echo "MEM0_API_KEY=your-key" >> ~/.hermes/.env
```

Setup (OSS):

```
hermes memory setup    # select "mem0" → "Open Source (self-hosted)"# Or via flags:hermes memory setup mem0 --mode oss --oss-llm openai --oss-llm-key sk-... --oss-vector qdrant
```

Preview without writing files:

```
hermes memory setup mem0 --mode oss --oss-llm-key sk-... --dry-run
```

Setup (Self-Hosted Dashboard):connect to a Mem0 server you run via Docker (the dashboard's REST API):

```
hermes memory setup    # select "mem0" → "Self-hosted server"# Or via flags:hermes memory setup mem0 --mode selfhosted --host http://localhost:8888 --api-key your-admin-api-key
```

Or configure manually — either as env vars:

```
echo "MEM0_HOST=http://localhost:8888" >> ~/.hermes/.envecho "MEM0_API_KEY=your-admin-api-key" >> ~/.hermes/.env
```

or inmem0.json:

`mem0.json`

```
{ "host": "http://localhost:8888", "api_key": "your-admin-api-key" }
```

The plugin authenticates withX-API-Keyand uses the server's/search//memoriesroutes.api_keyis optional (omit only forAUTH_DISABLEDservers). Don't setmode: oss— it takes precedence overhost.

`X-API-Key`
`/search`
`/memories`
`api_key`
`AUTH_DISABLED`
`mode: oss`
`host`

Config:$HERMES_HOME/mem0.json(behavioral settings). Only the secretMEM0_API_KEYbelongs in~/.hermes/.env.

`$HERMES_HOME/mem0.json`
`MEM0_API_KEY`
`~/.hermes/.env`
| Key | Default | Description |
| --- | --- | --- |
| mode | platform | platform(Mem0 Cloud) oross(self-managed, in-process) |
| host | — | Self-hosted Mem0 server URL (Docker dashboard). Routes over HTTP withX-API-Key; don't combine withmode: oss |
| user_id | hermes-user | User identifier |
| agent_id | hermes | Agent identifier |
| rerank | false | Rerank search results for relevance (platform mode only) |

`mode`
`platform`
`platform`
`oss`
`host`
`X-API-Key`
`mode: oss`
`user_id`
`hermes-user`
`agent_id`
`hermes`
`rerank`
`false`

OSS supported providers:

| Component | Providers |
| --- | --- |
| LLM | openai, ollama |
| Embedder | openai, ollama |
| Vector Store | qdrant (local/server), pgvector |

Switching modes:Re-runhermes memory setup mem0 --mode <platform|selfhosted|oss>or editmem0.jsondirectly.

`hermes memory setup mem0 --mode <platform|selfhosted|oss>`
`mem0.json`

### Hindsight​

Long-term memory with knowledge graph, entity resolution, and multi-strategy retrieval. Thehindsight_reflecttool provides cross-memory synthesis that no other provider offers. Automatically retains full conversation turns (including tool calls) with session-level document tracking.

`hindsight_reflect`
|  |  |
| --- | --- |
| Best for | Knowledge graph-based recall with entity relationships |
| Requires | Cloud: API key fromui.hindsight.vectorize.io. Local: LLM API key (OpenAI, Groq, OpenRouter, etc.) |
| Data storage | Hindsight Cloud or local embedded PostgreSQL |
| Cost | Hindsight pricing (cloud) or free (local) |

Tools:hindsight_retain(store with entity extraction),hindsight_recall(multi-strategy search),hindsight_reflect(cross-memory synthesis)

`hindsight_retain`
`hindsight_recall`
`hindsight_reflect`

Setup:

```
hermes memory setup    # select "hindsight"# Or manually:hermes config set memory.provider hindsightecho "HINDSIGHT_API_KEY=your-key" >> ~/.hermes/.env
```

The setup wizard installs dependencies automatically and only installs what's needed for the selected mode (hindsight-clientfor cloud,hindsight-allfor local). Requireshindsight-client >= 0.4.22(auto-upgraded on session start if outdated).

`hindsight-client`
`hindsight-all`
`hindsight-client >= 0.4.22`

Local mode UI:hindsight-embed -p hermes ui start

`hindsight-embed -p hermes ui start`

Config:$HERMES_HOME/hindsight/config.json

`$HERMES_HOME/hindsight/config.json`
| Key | Default | Description |
| --- | --- | --- |
| mode | cloud | cloudorlocal |
| bank_id | hermes | Memory bank identifier |
| recall_budget | mid | Recall thoroughness:low/mid/high |
| memory_mode | hybrid | hybrid(context + tools),context(auto-inject only),tools(tools only) |
| auto_retain | true | Automatically retain conversation turns |
| auto_recall | true | Automatically recall memories before each turn |
| retain_async | true | Process retain asynchronously on the server |
| retain_context | conversation between Hermes Agent and the User | Context label for retained memories |
| retain_tags | — | Default tags applied to retained memories; merged with per-call tool tags |
| retain_source | — | Optionalmetadata.sourceattached to retained memories |
| retain_user_prefix | User | Label used before user turns in auto-retained transcripts |
| retain_assistant_prefix | Assistant | Label used before assistant turns in auto-retained transcripts |
| recall_tags | — | Tags to filter on recall |

`mode`
`cloud`
`cloud`
`local`
`bank_id`
`hermes`
`recall_budget`
`mid`
`low`
`mid`
`high`
`memory_mode`
`hybrid`
`hybrid`
`context`
`tools`
`auto_retain`
`true`
`auto_recall`
`true`
`retain_async`
`true`
`retain_context`
`conversation between Hermes Agent and the User`
`retain_tags`
`retain_source`
`metadata.source`
`retain_user_prefix`
`User`
`retain_assistant_prefix`
`Assistant`
`recall_tags`

Seeplugin READMEfor the full configuration reference.

### Holographic​

Local SQLite fact store with FTS5 full-text search, trust scoring, and HRR (Holographic Reduced Representations) for compositional algebraic queries.

|  |  |
| --- | --- |
| Best for | Local-only memory with advanced retrieval, no external dependencies |
| Requires | Nothing (SQLite is always available). NumPy optional for HRR algebra. |
| Data storage | Local SQLite |
| Cost | Free |

Tools:fact_store(9 actions: add, search, probe, related, reason, contradict, update, remove, list),fact_feedback(helpful/unhelpful rating that trains trust scores)

`fact_store`
`fact_feedback`

Setup:

```
hermes memory setup    # select "holographic"# Or manually:hermes config set memory.provider holographic
```

Config:config.yamlunderplugins.hermes-memory-store

`config.yaml`
`plugins.hermes-memory-store`
| Key | Default | Description |
| --- | --- | --- |
| db_path | $HERMES_HOME/memory_store.db | SQLite database path |
| auto_extract | false | Auto-extract facts at session end |
| default_trust | 0.5 | Default trust score (0.0–1.0) |

`db_path`
`$HERMES_HOME/memory_store.db`
`auto_extract`
`false`
`default_trust`
`0.5`

Unique capabilities:

- probe— entity-specific algebraic recall (all facts about a person/thing)
- reason— compositional AND queries across multiple entities
- contradict— automated detection of conflicting facts
- Trust scoring with asymmetric feedback (+0.05 helpful / -0.10 unhelpful)

`probe`
`reason`
`contradict`

### RetainDB​

Cloud memory API with hybrid search (Vector + BM25 + Reranking), 7 memory types, and delta compression.

|  |  |
| --- | --- |
| Best for | Teams already using RetainDB's infrastructure |
| Requires | RetainDB account + API key |
| Data storage | RetainDB Cloud |
| Cost | $20/month |

Tools:retaindb_profile(user profile),retaindb_search(semantic search),retaindb_context(task-relevant context),retaindb_remember(store with type + importance),retaindb_forget(delete memories)

`retaindb_profile`
`retaindb_search`
`retaindb_context`
`retaindb_remember`
`retaindb_forget`

Setup:

```
hermes memory setup    # select "retaindb"# Or manually:hermes config set memory.provider retaindbecho "RETAINDB_API_KEY=your-key" >> ~/.hermes/.env
```

### ByteRover​

Persistent memory via thebrvCLI — hierarchical knowledge tree with tiered retrieval (fuzzy text → LLM-driven search). Local-first with optional cloud sync.

`brv`
|  |  |
| --- | --- |
| Best for | Developers who want portable, local-first memory with a CLI |
| Requires | ByteRover CLI (npm install -g byterover-cliorinstall script) |
| Data storage | Local (default) or ByteRover Cloud (optional sync) |
| Cost | Free (local) or ByteRover pricing (cloud) |

`npm install -g byterover-cli`

Tools:brv_query(search knowledge tree),brv_curate(store facts/decisions/patterns),brv_status(CLI version + tree stats)

`brv_query`
`brv_curate`
`brv_status`

Setup:

```
# Install the CLI firstcurl -fsSL https://byterover.dev/install.sh | sh# Then configure Hermeshermes memory setup    # select "byterover"# Or manually:hermes config set memory.provider byterover
```

Key features:

- Automatic pre-compression extraction (saves insights before context compression discards them)
- Knowledge tree stored at$HERMES_HOME/byterover/(profile-scoped)
- SOC2 Type II certified cloud sync (optional)

`$HERMES_HOME/byterover/`

### Supermemory​

Semantic long-term memory with profile recall, semantic search, explicit memory tools, and session-end conversation ingest via the Supermemory graph API.

|  |  |
| --- | --- |
| Best for | Semantic recall with user profiling and session-level graph building |
| Requires | pip install supermemory+API key |
| Data storage | Supermemory Cloud |
| Cost | Supermemory pricing |

`pip install supermemory`

Tools:supermemory_store(save explicit memories),supermemory_search(semantic similarity search),supermemory_forget(forget by ID or best-match query),supermemory_profile(persistent profile + recent context)

`supermemory_store`
`supermemory_search`
`supermemory_forget`
`supermemory_profile`

Setup:

```
hermes memory setup    # select "supermemory"# Or manually:hermes config set memory.provider supermemoryecho 'SUPERMEMORY_API_KEY=***' >> ~/.hermes/.env
```

Config:$HERMES_HOME/supermemory.json

`$HERMES_HOME/supermemory.json`
| Key | Default | Description |
| --- | --- | --- |
| container_tag | hermes | Container tag used for search and writes. Supports{identity}template for profile-scoped tags. |
| auto_recall | true | Inject relevant memory context before turns |
| auto_capture | true | Store cleaned user-assistant turns after each response |
| max_recall_results | 10 | Max recalled items to format into context |
| profile_frequency | 50 | Include profile facts on first turn and every N turns |
| capture_mode | all | Skip tiny or trivial turns by default |
| search_mode | hybrid | Search mode:hybrid,memories, ordocuments |
| api_timeout | 5.0 | Timeout for SDK and ingest requests |

`container_tag`
`hermes`
`{identity}`
`auto_recall`
`true`
`auto_capture`
`true`
`max_recall_results`
`10`
`profile_frequency`
`50`
`capture_mode`
`all`
`search_mode`
`hybrid`
`hybrid`
`memories`
`documents`
`api_timeout`
`5.0`

Environment variables:SUPERMEMORY_API_KEY(required),SUPERMEMORY_CONTAINER_TAG(overrides config).

`SUPERMEMORY_API_KEY`
`SUPERMEMORY_CONTAINER_TAG`

Key features:

- Automatic context fencing — strips recalled memories from captured turns to prevent recursive memory pollution
- Full-session ingest — the entire conversation is sent once at session boundaries
- Session-end conversation ingest (to/v4/conversations) for richer profile + graph building in Supermemory
- Profile facts injected on first turn and at configurable intervals
- Profile-scoped containers— use{identity}incontainer_tag(e.g.hermes-{identity}→hermes-coder) to isolate memories per Hermes profile
- Multi-container mode— enableenable_custom_container_tagswith acustom_containerslist to let the agent read/write across named containers. Automatic operations stay on the primary container.

`/v4/conversations`
`{identity}`
`container_tag`
`hermes-{identity}`
`hermes-coder`
`enable_custom_container_tags`
`custom_containers`

```
{  "container_tag": "hermes",  "enable_custom_container_tags": true,  "custom_containers": ["project-alpha", "shared-knowledge"],  "custom_container_instructions": "Use project-alpha for coding context."}
```

Support:Discord·support@supermemory.com

### Memori​

Structured long-term memory using Memori Cloud, with background completed-turn capture, tool-aware turn context, and explicit recall tools for facts, summaries, quota, signup, and feedback.

|  |  |
| --- | --- |
| Best for | Agent-controlled recall with structured project and session attribution |
| Requires | pip install hermes-memori+hermes-memori install+Memori API key |
| Data storage | Memori Cloud |
| Cost | Memori pricing |

`pip install hermes-memori`
`hermes-memori install`

Tools:memori_recall(search long-term memory),memori_recall_summary(summarized context),memori_quota(usage/quota),memori_signup(request signup email),memori_feedback(send integration feedback)

`memori_recall`
`memori_recall_summary`
`memori_quota`
`memori_signup`
`memori_feedback`

Setup:

```
pip install hermes-memorihermes-memori installhermes config set memory.provider memorihermes memory setup
```

## Provider Comparison​

| Provider | Storage | Cost | Tools | Dependencies | Unique Feature |
| --- | --- | --- | --- | --- | --- |
| Honcho | Cloud | Paid | 5 | honcho-ai | Dialectic user modeling + session-scoped context |
| OpenViking | Self-hosted | Free | 5 | openviking+ server | Filesystem hierarchy + tiered loading |
| Mem0 | Cloud/Self-hosted | Free/Paid | 4 | mem0ai | Server-side LLM extraction + self-hosted/OSS modes |
| Hindsight | Cloud/Local | Free/Paid | 3 | hindsight-client | Knowledge graph + reflect synthesis |
| Holographic | Local | Free | 2 | None | HRR algebra + trust scoring |
| RetainDB | Cloud | $20/mo | 5 | requests | Delta compression |
| ByteRover | Local/Cloud | Free/Paid | 3 | brvCLI | Pre-compression extraction |
| Supermemory | Cloud | Paid | 4 | supermemory | Context fencing + session graph ingest + multi-container |
| Memori | Cloud | Free/Paid | 5 | hermes-memori | Tool-aware memory + structured recall |

`honcho-ai`
`openviking`
`mem0ai`
`hindsight-client`
`requests`
`brv`
`supermemory`
`hermes-memori`

## Profile Isolation​

Each provider's data is isolated perprofile:

- Local storage providers(Holographic, ByteRover) use$HERMES_HOME/paths which differ per profile
- Config file providers(Honcho, Mem0, Hindsight, Supermemory) store config in$HERMES_HOME/so each profile has its own credentials
- Cloud providers(RetainDB) auto-derive profile-scoped project names
- Env var providers(OpenViking) are configured via each profile's.envfile

`$HERMES_HOME/`
`$HERMES_HOME/`
`.env`

## Building a Memory Provider​

See theDeveloper Guide: Memory Provider Pluginsfor how to create your own.