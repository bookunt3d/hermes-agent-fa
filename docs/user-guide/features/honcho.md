---
layout: docs
title: "Features_Honcho"
permalink: /docs/user-guide/features/honcho/
---

- 
- Features
- Core
- Honcho Memory

# Honcho Memory

Honchois an AI-native memory backend that adds dialectic reasoning and deep user modeling on top of Hermes's built-in memory system. Instead of simple key-value storage, Honcho maintains a running model of who the user is — their preferences, communication style, goals, and patterns — by reasoning about conversations after they happen.

Honcho is integrated into theMemory Providerssystem. All features below are available through the unified memory provider interface.

## What Honcho Adds​

| Capability | Built-in Memory | Honcho |
| --- | --- | --- |
| Cross-session persistence | ✔ File-based MEMORY.md/USER.md | ✔ Server-side with API |
| User profile | ✔ Manual agent curation | ✔ Automatic dialectic reasoning |
| Session summary | — | ✔ Session-scoped context injection |
| Multi-agent isolation | — | ✔ Per-peer profile separation |
| Observation modes | — | ✔ Unified or directional observation |
| Conclusions (derived insights) | — | ✔ Server-side reasoning about patterns |
| Search across history | ✔ FTS5 session search | ✔ Semantic search over conclusions |

Dialectic reasoning: After each conversation turn (gated bydialecticCadence), Honcho analyzes the exchange and derives insights about the user's preferences, habits, and goals. These accumulate over time, giving the agent a deepening understanding that goes beyond what the user explicitly stated. The dialectic supports multi-pass depth (1–3 passes) with automatic cold/warm prompt selection — cold start queries focus on general user facts while warm queries prioritize session-scoped context.

`dialecticCadence`

Session-scoped context: Base context now includes the session summary alongside the user representation and peer card. This gives the agent awareness of what has already been discussed in the current session, reducing repetition and enabling continuity.

Multi-agent profiles: When multiple Hermes instances talk to the same user (e.g., a coding assistant and a personal assistant), Honcho maintains separate "peer" profiles. Each peer sees only its own observations and conclusions, preventing cross-contamination of context.

## Setup​

```
hermes memory setup    # select "honcho" from the provider list
```

Or configure manually:

```
# ~/.hermes/config.yamlmemory:  provider: honcho
```

```
echo 'HONCHO_API_KEY=***' >> ~/.hermes/.env
```

Get an API key athoncho.dev.

## Architecture​

### Two-Layer Context Injection​

Every turn (inhybridorcontextmode), Honcho assembles two layers of context injected into the system prompt:

`hybrid`
`context`
1. Base context— session summary, user representation, user peer card, AI self-representation, and AI identity card. Refreshed oncontextCadence. This is the "who is this user" layer.
2. Dialectic supplement— LLM-synthesized reasoning about the user's current state and needs. Refreshed ondialecticCadence. This is the "what matters right now" layer.

`contextCadence`
`dialecticCadence`

Both layers are concatenated and truncated to thecontextTokensbudget (if set).

`contextTokens`

### Cold/Warm Prompt Selection​

The dialectic automatically selects between two prompt strategies:

- Cold start(no base context yet): General query — "Who is this person? What are their preferences, goals, and working style?"
- Warm session(base context exists): Session-scoped query — "Given what's been discussed in this session so far, what context about this user is most relevant?"

This happens automatically based on whether base context has been populated.

### Three Orthogonal Config Knobs​

Cost and depth are controlled by three independent knobs:

| Knob | Controls | Default |
| --- | --- | --- |
| contextCadence | Turns betweencontext()API calls (base layer refresh) | 1 |
| dialecticCadence | Turns betweenpeer.chat()LLM calls (dialectic layer refresh) | 2(recommended 1–5) |
| dialecticDepth | Number of.chat()passes per dialectic invocation (1–3) | 1 |

`contextCadence`
`context()`
`1`
`dialecticCadence`
`peer.chat()`
`2`
`dialecticDepth`
`.chat()`
`1`

These are orthogonal — you can have frequent context refreshes with infrequent dialectic, or deep multi-pass dialectic at low frequency. Example:contextCadence: 1, dialecticCadence: 5, dialecticDepth: 2refreshes base context every turn, runs dialectic every 5 turns, and each dialectic run makes 2 passes.

`contextCadence: 1, dialecticCadence: 5, dialecticDepth: 2`

### Dialectic Depth (Multi-Pass)​

WhendialecticDepth> 1, each dialectic invocation runs multiple.chat()passes:

`dialecticDepth`
`.chat()`
- Pass 0: Cold or warm prompt (see above)
- Pass 1: Self-audit — identifies gaps in the initial assessment and synthesizes evidence from recent sessions
- Pass 2: Reconciliation — checks for contradictions between prior passes and produces a final synthesis

Each pass uses a proportional reasoning level (lighter early passes, base level for the main pass). Override per-pass levels withdialecticDepthLevels— e.g.,["minimal", "medium", "high"]for a depth-3 run.

`dialecticDepthLevels`
`["minimal", "medium", "high"]`

Passes bail out early if the prior pass returned strong signal (long, structured output), so depth 3 doesn't always mean 3 LLM calls.

### Session-Start Prewarm​

On session init, Honcho fires a dialectic call in the background at the full configureddialecticDepthand hands the result directly to turn 1's context assembly. A single-pass prewarm on a cold peer often returns thin output — multi-pass depth runs the audit/reconcile cycle before the user ever speaks. If prewarm hasn't landed by turn 1, turn 1 falls back to a synchronous call with a bounded timeout.

`dialecticDepth`

### Query-Adaptive Reasoning Level​

The auto-injected dialectic scalesdialecticReasoningLevelby query length: +1 level at ≥120 chars, +2 at ≥400, clamped atreasoningLevelCap(default"high"). Disable withreasoningHeuristic: falseto pin every auto call todialecticReasoningLevel. Available levels:minimal,low,medium,high,max.

`dialecticReasoningLevel`
`reasoningLevelCap`
`"high"`
`reasoningHeuristic: false`
`dialecticReasoningLevel`
`minimal`
`low`
`medium`
`high`
`max`

## Configuration Options​

Honcho is configured in~/.honcho/config.json(global) or$HERMES_HOME/honcho.json(profile-local). The setup wizard handles this for you.

`~/.honcho/config.json`
`$HERMES_HOME/honcho.json`

### Self-Hosted Honcho with Authentication​

When pointing Hermes at a self-hosted Honcho server,hermes honcho setup(andhermes memory setup) ask for alocal JWT / bearer tokenafter the base URL. Paste a JWT signed with the server'sAUTH_JWT_SECRET(the Honcho compose env var) to enable authenticated access; leave it blank for servers running withAUTH_USE_AUTH=false. The local token is stored under the host block (hosts.<host>.apiKeyinhoncho.json), separate from any cloudapiKey, so you can flip theCloud or local?prompt back tocloudlater without losing either credential.

`hermes honcho setup`
`hermes memory setup`
`AUTH_JWT_SECRET`
`AUTH_USE_AUTH=false`
`hosts.<host>.apiKey`
`honcho.json`
`apiKey`
`Cloud or local?`
`cloud`

### Full Config Reference​

| Key | Default | Description |
| --- | --- | --- |
| contextTokens | null(uncapped) | Token budget for auto-injected context per turn. Set to an integer (e.g. 1200) to cap. Truncates at word boundaries |
| contextCadence | 1 | Minimum turns betweencontext()API calls (base layer refresh) |
| dialecticCadence | 2 | Minimum turns betweenpeer.chat()LLM calls (dialectic layer). Recommended 1–5. Intoolsmode, irrelevant — model calls explicitly |
| dialecticDepth | 1 | Number of.chat()passes per dialectic invocation. Clamped to 1–3 |
| dialecticDepthLevels | null | Optional array of reasoning levels per pass, e.g.["minimal", "low", "medium"]. Overrides proportional defaults |
| dialecticReasoningLevel | 'low' | Base reasoning level:minimal,low,medium,high,max |
| dialecticDynamic | true | Whentrue, model can override reasoning level per-call via tool param |
| dialecticMaxChars | 600 | Max chars of dialectic result injected into system prompt |
| recallMode | 'hybrid' | hybrid(auto-inject + tools),context(inject only),tools(tools only) |
| writeFrequency | 'async' | When to flush messages:async(background thread),turn(sync),session(batch on end), or integer N |
| saveMessages | true | Whether to persist messages to Honcho API |
| observationMode | 'directional' | directional(all on) orunified(shared pool). Override withobservationobject for granular control |
| messageMaxChars | 25000 | Max chars per message sent viaadd_messages(). Chunked if exceeded |
| dialecticMaxInputChars | 10000 | Max chars for dialectic query input topeer.chat() |
| sessionStrategy | 'per-directory' | per-directory,per-repo,per-session, orglobal |
| pinUserPeer | false | Gateway only. Whentrue, every platform user collapses topeerName |
| userPeerAliases | {} | Gateway only. Map of runtime IDs to peers ({"7654321": "alice"}). Many-to-one |
| runtimePeerPrefix | "" | Gateway only. Namespaces unknown runtime IDs (telegram_7654321) when no alias matches |

`contextTokens`
`null`
`contextCadence`
`1`
`context()`
`dialecticCadence`
`2`
`peer.chat()`
`tools`
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
`add_messages()`
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

Session strategycontrols how Honcho sessions map to your work:

- per-session— eachhermesrun gets a fresh session. Clean starts, memory via tools. Recommended for new users.
- per-directory— one Honcho session per working directory. Context accumulates across runs.
- per-repo— one session per git repository.
- global— single session across all directories.

`per-session`
`hermes`
`per-directory`
`per-repo`
`global`

Recall modecontrols how memory flows into conversations:

- hybrid— context auto-injected into system prompt AND tools available (model decides when to query).
- context— auto-injection only, tools hidden.
- tools— tools only, no auto-injection. Agent must explicitly callhoncho_reasoning,honcho_search, etc.

`hybrid`
`context`
`tools`
`honcho_reasoning`
`honcho_search`

Settings per recall mode:

| Setting | hybrid | context | tools |
| --- | --- | --- | --- |
| writeFrequency | flushes messages | flushes messages | flushes messages |
| contextCadence | gates base context refresh | gates base context refresh | irrelevant — no injection |
| dialecticCadence | gates auto LLM calls | gates auto LLM calls | irrelevant — model calls explicitly |
| dialecticDepth | multi-pass per invocation | multi-pass per invocation | irrelevant — model calls explicitly |
| contextTokens | caps injection | caps injection | irrelevant — no injection |
| dialecticDynamic | gates model override | N/A (no tools) | gates model override |

`hybrid`
`context`
`tools`
`writeFrequency`
`contextCadence`
`dialecticCadence`
`dialecticDepth`
`contextTokens`
`dialecticDynamic`

Intoolsmode, the model is fully in control — it callshoncho_reasoningwhen it wants, at whateverreasoning_levelit picks. Cadence and budget settings only apply to modes with auto-injection (hybridandcontext).

`tools`
`honcho_reasoning`
`reasoning_level`
`hybrid`
`context`

## Gateway Identity Mapping​

These settings only matter when you run theHermes gateway— the one entrypoint where users arrive with platform-native runtime IDs (Telegram UID, Discord snowflake, Slack user). CLI, TUI, and desktop sessions have no runtime ID and always resolve topeerName, so off-gateway these keys do nothing.

`peerName`

The setup wizard detects whether a gateway platform is connected and skips this step entirely if not. When it runs, it asks one question —who talks to this gateway?— and derives the keys:

| Answer | Result |
| --- | --- |
| just me | pinUserPeer: true— every non-agent gateway user collapses to your peer. Pin overrides all aliases, so pick this only when no user-side identity needs its own peer. If separate agents reach the gateway and each needs a distinct peer, donotpin — leavepinUserPeer: falseand map them viauserPeerAliases(the[e]editor) instead |
| me + other people(pooled) | pinUserPeer: false+userPeerAliasesmapping your runtime IDs topeerName— you stay on your shared history, others get their own peers |
| only other people | pinUserPeer: false, optionalruntimePeerPrefix— each user gets their own peer |

`pinUserPeer: true`
`pinUserPeer: false`
`userPeerAliases`
`[e]`
`pinUserPeer: false`
`userPeerAliases`
`peerName`
`pinUserPeer: false`
`runtimePeerPrefix`

Pick[e]at the prompt to set the three keys directly instead.

`[e]`

The resolver tries the keys top-down, first match wins:pinUserPeer→userPeerAliases[id]→runtimePeerPrefix + id→ raw runtime ID →peerName→ session-key fallback.

`pinUserPeer`
`userPeerAliases[id]`
`runtimePeerPrefix + id`
`peerName`

FlippingpinUserPeerfromtruetofalsedoes not migrate data — memory accumulated underpeerNamestays there, and platform users resolve to fresh, empty peers. To keep your own continuity, choose thepooledpath so your runtime IDs alias back topeerName. The wizard offers this steer automatically when it detects the transition.

`pinUserPeer`
`true`
`false`
`peerName`
`peerName`

pinPeerNameis a legacy alias forpinUserPeer— still read for back-compat (pinUserPeerwins where both are set), never written. Re-running setup migrates it onto the canonical key.

`pinPeerName`
`pinUserPeer`
`pinUserPeer`

## Observation (Directional vs. Unified)​

Honcho models a conversation as peers exchanging messages. Each peer has two observation toggles that map 1:1 to Honcho'sSessionPeerConfig:

`SessionPeerConfig`
| Toggle | Effect |
| --- | --- |
| observeMe | Honcho builds a representation of this peer from its own messages |
| observeOthers | This peer observes the other peer's messages (feeds cross-peer reasoning) |

`observeMe`
`observeOthers`

Two peers × two toggles = four flags.observationModeis a shorthand preset:

`observationMode`
| Preset | User flags | AI flags | Semantics |
| --- | --- | --- | --- |
| "directional"(default) | me: on, others: on | me: on, others: on | Full mutual observation. Enables cross-peer dialectic — "what does the AI know about the user, based on what the user said and the AI replied." |
| "unified" | me: on, others: off | me: off, others: on | Shared-pool semantics — the AI observes the user's messages only, the user peer only self-models. Single-observer pool. |

`"directional"`
`"unified"`

Override the preset with an explicitobservationblock for per-peer control:

`observation`

```
"observation": {  "user": { "observeMe": true,  "observeOthers": true },  "ai":   { "observeMe": true,  "observeOthers": false }}
```

Common patterns:

| Intent | Config |
| --- | --- |
| Full observation (most users) | "observationMode": "directional" |
| AI shouldn't re-model the user from its own replies | "ai": {"observeMe": true, "observeOthers": false} |
| Strong persona the AI peer shouldn't update from self-observation | "ai": {"observeMe": false, "observeOthers": true} |

`"observationMode": "directional"`
`"ai": {"observeMe": true, "observeOthers": false}`
`"ai": {"observeMe": false, "observeOthers": true}`

Server-side toggles set via theHoncho dashboardwin over local defaults — Hermes syncs them back at session init.

## Tools​

When Honcho is active as the memory provider, five tools become available:

| Tool | Purpose |
| --- | --- |
| honcho_profile | Read or update peer card — passcard(list of facts) to update, omit to read |
| honcho_search | Semantic search over context — raw excerpts, no LLM synthesis |
| honcho_context | Full session context — summary, representation, card, recent messages |
| honcho_reasoning | Synthesized answer from Honcho's LLM — passreasoning_level(minimal/low/medium/high/max) to control depth |
| honcho_conclude | Create or delete conclusions — passconclusionto create,delete_idto remove (PII only) |

`honcho_profile`
`card`
`honcho_search`
`honcho_context`
`honcho_reasoning`
`reasoning_level`
`honcho_conclude`
`conclusion`
`delete_id`

## CLI Commands​

Thehermes honchosubcommand isonly registered when Honcho is the active memory provider(memory.provider: honchoinconfig.yaml). On a fresh install, configure Honcho directly withhermes memory setup honcho(or runhermes memory setupand pick it from the list); thehermes honchosubcommand then appears on the next invocation.

`hermes honcho`
`memory.provider: honcho`
`config.yaml`
`hermes memory setup honcho`
`hermes memory setup`
`hermes honcho`

```
hermes memory setup honcho    # Configure Honcho directly (works before activation)hermes honcho status          # Connection status, config, and key settingshermes honcho setup           # Redirects to `hermes memory setup` (post-activation alias)hermes honcho strategy        # Show or set session strategy (per-session/per-directory/per-repo/global)hermes honcho peer            # Show or update peer names + dialectic reasoning levelhermes honcho mode            # Show or set recall mode (hybrid/context/tools)hermes honcho tokens          # Show or set token budget for context and dialectichermes honcho identity        # Seed or show the AI peer's Honcho identityhermes honcho sync            # Sync Honcho config to all existing profileshermes honcho peers           # Show peer identities across all profileshermes honcho sessions        # List known Honcho session mappingshermes honcho map             # Map current directory to a Honcho session namehermes honcho enable          # Enable Honcho for the active profilehermes honcho disable         # Disable Honcho for the active profilehermes honcho migrate         # Step-by-step migration guide from openclaw-honcho
```

## Migrating fromhermes honcho​

`hermes honcho`

If you previously used the standalonehermes honcho setup:

`hermes honcho setup`
1. Your existing configuration (honcho.jsonor~/.honcho/config.json) is preserved
2. Your server-side data (memories, conclusions, user profiles) is intact
3. Setmemory.provider: honchoin config.yaml to reactivate

`honcho.json`
`~/.honcho/config.json`
`memory.provider: honcho`

No re-login or re-setup needed. Runhermes memory setupand select "honcho" — the wizard detects your existing config.

`hermes memory setup`

## Full Documentation​

SeeMemory Providers — Honchofor the complete reference.