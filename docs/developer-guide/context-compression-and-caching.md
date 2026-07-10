---
layout: docs
title: "فشرده‌سازی و کش زمینه"
permalink: /docs/developer-guide/context-compression-and-caching/
---

- 
- Developer Guide
- Architecture
- Context Compression and Caching

# Context Compression and Caching

Hermes Agent uses a dual compression system and Anthropic prompt caching to
manage context window usage efficiently across long conversations.

Source files:agent/context_engine.py(ABC),agent/context_compressor.py(default engine),agent/prompt_caching.py,gateway/run.py(session hygiene),run_agent.py(search for_compress_context)

`agent/context_engine.py`
`agent/context_compressor.py`
`agent/prompt_caching.py`
`gateway/run.py`
`run_agent.py`
`_compress_context`

## Pluggable Context Engine​

Context management is built on theContextEngineABC (agent/context_engine.py). The built-inContextCompressoris the default implementation, but plugins can replace it with alternative engines (e.g., Lossless Context Management).

`ContextEngine`
`agent/context_engine.py`
`ContextCompressor`

```
context:  engine: "compressor"    # default — built-in lossy summarization  engine: "lcm"           # example — plugin providing lossless context
```

The engine is responsible for:

- Deciding when compaction should fire (should_compress())
- Performing compaction (compress())
- Optionally exposing tools the agent can call (e.g.,lcm_grep)
- Tracking token usage from API responses

`should_compress()`
`compress()`
`lcm_grep`

Selection is config-driven viacontext.engineinconfig.yaml. The resolution order:

`context.engine`
`config.yaml`
1. Checkplugins/context_engine/<name>/directory
2. Check general plugin system (register_context_engine())
3. Fall back to built-inContextCompressor

`plugins/context_engine/<name>/`
`register_context_engine()`
`ContextCompressor`

Plugin engines arenever auto-activated— the user must explicitly setcontext.engineto the plugin's name. The default"compressor"always uses the built-in.

`context.engine`
`"compressor"`

Configure viahermes plugins→ Provider Plugins → Context Engine, or editconfig.yamldirectly.

`hermes plugins`
`config.yaml`

For building a context engine plugin, seeContext Engine Plugins.

## Dual Compression System​

Hermes has two separate compression layers that operate independently:

```
                     ┌──────────────────────────┐  Incoming message   │   Gateway Session Hygiene │  Fires at 85% of context  ─────────────────► │   (pre-agent, rough est.) │  Safety net for large sessions                     └─────────────┬────────────┘                                   │                                   ▼                     ┌──────────────────────────┐                     │   Agent ContextCompressor │  Fires at 50% of context (default)                     │   (in-loop, real tokens)  │  Normal context management                     └──────────────────────────┘
```

### 1. Gateway Session Hygiene (85% threshold)​

Located ingateway/run.py(search forSession hygiene: auto-compress). This is asafety netthat
runs before the agent processes a message. It prevents API failures when sessions
grow too large between turns (e.g., overnight accumulation in Telegram/Discord).

`gateway/run.py`
`Session hygiene: auto-compress`
- Threshold: Fixed at 85% of model context length
- Token source: Prefers actual API-reported tokens from last turn; falls back
to rough character-based estimate (estimate_messages_tokens_rough)
- Fires: Only whenlen(history) >= 4and compression is enabled
- Purpose: Catch sessions that escaped the agent's own compressor

`estimate_messages_tokens_rough`
`len(history) >= 4`

The gateway hygiene threshold is intentionally higher than the agent's compressor.
Setting it at 50% (same as the agent) caused premature compression on every turn
in long gateway sessions.

### 2. Agent ContextCompressor (50% threshold, configurable)​

Located inagent/context_compressor.py. This is theprimary compression
systemthat runs inside the agent's tool loop with access to accurate,
API-reported token counts.

`agent/context_compressor.py`

## Configuration​

All compression settings are read fromconfig.yamlunder thecompressionkey:

`config.yaml`
`compression`

```
compression:  enabled: true              # Enable/disable compression (default: true)  threshold: 0.50            # Fraction of context window (default: 0.50 = 50%)  target_ratio: 0.20         # How much of threshold to keep as tail (default: 0.20)  protect_last_n: 20         # Minimum protected tail messages (default: 20)  codex_gpt55_autoraise: true  # gpt-5.5 on Codex OAuth: raise trigger to 85% (default: true)  codex_gpt55_autoraise_notice: true  # Show the one-time autoraise notice (default: true)  codex_app_server_auto: native  # native|hermes|off for Codex app-server thread compaction# Summarization model/provider configured under auxiliary:auxiliary:  compression:    model: null              # Override model for summaries (default: auto-detect)    provider: auto           # Provider: "auto", "openrouter", "nous", "main", etc.    base_url: null           # Custom OpenAI-compatible endpoint
```

### Parameter Details​

| Parameter | Default | Range | Description |
| --- | --- | --- | --- |
| threshold | 0.50 | 0.0-1.0 | Compression triggers when prompt tokens ≥threshold × context_length |
| target_ratio | 0.20 | 0.10-0.80 | Controls tail protection token budget:threshold_tokens × target_ratio |
| protect_last_n | 20 | ≥1 | Minimum number of recent messages always preserved |
| protect_first_n | 3 | (hardcoded) | System prompt + first exchange always preserved |
| codex_gpt55_autoraise | true | bool | Raise the trigger to 85% for gpt-5.5 on the ChatGPT Codex OAuth route (see below). Setfalseto keep the globalthreshold |
| codex_gpt55_autoraise_notice | true | bool | Show the one-time Codex gpt-5.5 autoraise notice. Setfalseto keep the 85% autoraise but suppress the banner |
| codex_app_server_auto | native | native,hermes,off | Thread-compaction mode for Codex app-server sessions (see below) |

`threshold`
`0.50`
`threshold × context_length`
`target_ratio`
`0.20`
`threshold_tokens × target_ratio`
`protect_last_n`
`20`
`protect_first_n`
`3`
`codex_gpt55_autoraise`
`true`
`false`
`threshold`
`codex_gpt55_autoraise_notice`
`true`
`false`
`codex_app_server_auto`
`native`
`native`
`hermes`
`off`

### Codex gpt-5.5 threshold autoraise​

The ChatGPT Codex OAuth backend hard-caps gpt-5.5 at a272Kcontext window
(the same slug exposes 1.05M on OpenAI's direct API and OpenRouter, and 400K on
GitHub Copilot). At the default 50% trigger, compaction would fire at ~136K —
half the window the model can actually use. When the active route is Codex
OAuth (provider: openai-codex) and the model is gpt-5.5, Hermes raises the
trigger to85%(~231K) and shows a notice with the opt-out command. The
notice is shown once per profile — a marker under$HERMES_HOME(.codex_gpt55_autoraise_notice) records that it ran, so repeated agent/session
inits (e.g. every inbound gateway message) don't re-emit it; if the raised
threshold later changes it re-notifies once. Only this exact route is affected;
gpt-5.5 on any other provider keeps your globalthreshold. To opt back down to
the global value:

`provider: openai-codex`
`$HERMES_HOME`
`.codex_gpt55_autoraise_notice`
`threshold`

```
hermes config set compression.codex_gpt55_autoraise false
```

To keep the 85% autoraise but hide only the one-time notice:

```
hermes config set compression.codex_gpt55_autoraise_notice false
```

### Codex app-server thread compaction​

Codex app-server sessions (api_mode: codex_app_server— the codex CLI/agent
runtime) are different from every other route: the codex agent owns the backing
thread context, so Hermes' auxiliary summarizer cannot shrink it — rewriting the
local transcript mirror leaves the real thread growing unbounded until a hard
context reset. For this runtime, compaction goes through the app-server's own
mechanism instead:

`api_mode: codex_app_server`
- Manual compaction (/compress) asks the app-server to compact the thread
(thread/compact/start) and waits for the compaction turn to complete.
- Automatic compaction is controlled bycompression.codex_app_server_auto:
the defaultnativelets the app-server decide when to compact and Hermes
records the resulting compaction events (compression counters, session
events). Sethermesto let Hermes' compression threshold initiate
app-server compaction, oroffto disable Hermes-initiated automatic
compaction entirely (codex may still compact natively).

`/compress`
`thread/compact/start`
`compression.codex_app_server_auto`
`native`
`hermes`
`off`

Hermes' local transcript is never rewritten on this runtime — state.db records
the compaction boundary while the visible transcript stays intact. All other
routes (including Codex OAuth chat sessions) keep Hermes' summary compressor.

### Computed Values (for a 200K context model at defaults)​

```
context_length       = 200,000threshold_tokens     = 200,000 × 0.50 = 100,000tail_token_budget    = 100,000 × 0.20 = 20,000max_summary_tokens   = min(200,000 × 0.05, 12,000) = 10,000
```

threshold_tokensis alwaysthreshold × context_length, wherecontext_lengthis themain agent model'scontext window — never the auxiliary/summary
model's. On a 262,144-token model at the default0.50, the threshold is262,144 × 0.50 = 131,072. That number being close to a common "128K context"
is a coincidence of the percentage, not a sign that the auxiliary model's window
is the trigger. The auxiliary model's context window is a separate concern — see
the "Summary model context length" warning below for how it affects whether a
summary can be produced, not when compression fires.

`threshold_tokens`
`threshold × context_length`
`context_length`
`0.50`
`262,144 × 0.50 = 131,072`

## Compression Algorithm​

TheContextCompressor.compress()method follows a 4-phase algorithm:

`ContextCompressor.compress()`

### Phase 1: Prune Old Tool Results (cheap, no LLM call)​

Old tool results (>200 chars) outside the protected tail are replaced with:

```
[Old tool output cleared to save context space]
```

This is a cheap pre-pass that saves significant tokens from verbose tool
outputs (file contents, terminal output, search results).

### Phase 2: Determine Boundaries​

```
┌─────────────────────────────────────────────────────────────┐│  Message list                                               ││                                                             ││  [0..2]  ← protect_first_n (system + first exchange)        ││  [3..N]  ← middle turns → SUMMARIZED                        ││  [N..end] ← tail (by token budget OR protect_last_n)        ││                                                             │└─────────────────────────────────────────────────────────────┘
```

Tail protection istoken-budget based: walks backward from the end,
accumulating tokens until the budget is exhausted. Falls back to the fixedprotect_last_ncount if the budget would protect fewer messages.

`protect_last_n`

Boundaries are aligned to avoid splitting tool_call/tool_result groups.
The_align_boundary_backward()method walks past consecutive tool results
to find the parent assistant message, keeping groups intact.

`_align_boundary_backward()`

### Phase 3: Generate Structured Summary​

The summary model must have a context windowat least as largeas the main agent model's. The entire middle section is sent to the summary model in a singlecall_llm(task="compression")call. If the summary model's context is smaller, the API returns a context-length error —_generate_summary()catches it, logs a warning, and returnsNone. The compressor then drops the middle turnswithout a summary, silently losing conversation context. This is the most common cause of degraded compaction quality.

`call_llm(task="compression")`
`_generate_summary()`
`None`

The middle turns are summarized using the auxiliary LLM with a structured
template:

```
## Goal[What the user is trying to accomplish]## Constraints & Preferences[User preferences, coding style, constraints, important decisions]## Progress### Done[Completed work — specific file paths, commands run, results]### In Progress[Work currently underway]### Blocked[Any blockers or issues encountered]## Key Decisions[Important technical decisions and why]## Relevant Files[Files read, modified, or created — with brief note on each]## Next Steps[What needs to happen next]## Critical Context[Specific values, error messages, configuration details]
```

Summary budget scales with the amount of content being compressed:

- Formula:content_tokens × 0.20(the_SUMMARY_RATIOconstant)
- Minimum: 2,000 tokens
- Maximum:min(context_length × 0.05, 12,000)tokens

`content_tokens × 0.20`
`_SUMMARY_RATIO`
`min(context_length × 0.05, 12,000)`

### Phase 4: Assemble Compressed Messages​

The compressed message list is:

1. Head messages (with a note appended to system prompt on first compression)
2. Summary message (role chosen to avoid consecutive same-role violations)
3. Tail messages (unmodified)

Orphaned tool_call/tool_result pairs are cleaned up by_sanitize_tool_pairs():

`_sanitize_tool_pairs()`
- Tool results referencing removed calls → removed
- Tool calls whose results were removed → stub result injected

### Iterative Re-compression​

On subsequent compressions, the previous summary is passed to the LLM with
instructions toupdateit rather than summarize from scratch. This preserves
information across multiple compactions — items move from "In Progress" to "Done",
new progress is added, and obsolete information is removed.

The_previous_summaryfield on the compressor instance stores the last summary
text for this purpose.

`_previous_summary`

## Before/After Example​

### Before Compression (45 messages, ~95K tokens)​

```
[0] system:    "You are a helpful assistant..." (system prompt)[1] user:      "Help me set up a FastAPI project"[2] assistant: <tool_call> terminal: mkdir project </tool_call>[3] tool:      "directory created"[4] assistant: <tool_call> write_file: main.py </tool_call>[5] tool:      "file written (2.3KB)"    ... 30 more turns of file editing, testing, debugging ...[38] assistant: <tool_call> terminal: pytest </tool_call>[39] tool:      "8 passed, 2 failed\n..."  (5KB output)[40] user:      "Fix the failing tests"[41] assistant: <tool_call> read_file: tests/test_api.py </tool_call>[42] tool:      "import pytest\n..."  (3KB)[43] assistant: "I see the issue with the test fixtures..."[44] user:      "Great, also add error handling"
```

### After Compression (25 messages, ~45K tokens)​

```
[0] system:    "You are a helpful assistant...               [Note: Some earlier conversation turns have been compacted...]"[1] user:      "Help me set up a FastAPI project"[2] assistant: "[CONTEXT COMPACTION] Earlier turns were compacted...               ## Goal               Set up a FastAPI project with tests and error handling               ## Progress               ### Done               - Created project structure: main.py, tests/, requirements.txt               - Implemented 5 API endpoints in main.py               - Wrote 10 test cases in tests/test_api.py               - 8/10 tests passing               ### In Progress               - Fixing 2 failing tests (test_create_user, test_delete_user)               ## Relevant Files               - main.py — FastAPI app with 5 endpoints               - tests/test_api.py — 10 test cases               - requirements.txt — fastapi, pytest, httpx               ## Next Steps               - Fix failing test fixtures               - Add error handling"[3] user:      "Fix the failing tests"[4] assistant: <tool_call> read_file: tests/test_api.py </tool_call>[5] tool:      "import pytest\n..."[6] assistant: "I see the issue with the test fixtures..."[7] user:      "Great, also add error handling"
```

## Prompt Caching (Anthropic)​

Source:agent/prompt_caching.py

`agent/prompt_caching.py`

Reduces input token costs by ~75% on multi-turn conversations by caching the
conversation prefix. Uses Anthropic'scache_controlbreakpoints.

`cache_control`

### Strategy: system_and_3​

Anthropic allows a maximum of 4cache_controlbreakpoints per request. Hermes
uses the "system_and_3" strategy:

`cache_control`

```
Breakpoint 1: System prompt           (stable across all turns)Breakpoint 2: 3rd-to-last non-system message  ─┐Breakpoint 3: 2nd-to-last non-system message   ├─ Rolling windowBreakpoint 4: Last non-system message          ─┘
```

### How It Works​

apply_anthropic_cache_control()deep-copies the messages and injectscache_controlmarkers:

`apply_anthropic_cache_control()`
`cache_control`

```
# Cache marker formatmarker = {"type": "ephemeral"}# Or for 1-hour TTL:marker = {"type": "ephemeral", "ttl": "1h"}
```

The marker is applied differently based on content type:

| Content Type | Where Marker Goes |
| --- | --- |
| String content | Converted to[{"type": "text", "text": ..., "cache_control": ...}] |
| List content | Added to the last element's dict |
| None/empty | Added asmsg["cache_control"] |
| Tool messages | Added asmsg["cache_control"](native Anthropic only) |

`[{"type": "text", "text": ..., "cache_control": ...}]`
`msg["cache_control"]`
`msg["cache_control"]`

### Cache-Aware Design Patterns​

1. Stable system prompt: The system prompt is breakpoint 1 and cached across
all turns. Avoid mutating it mid-conversation (compression appends a note
only on the first compaction).
2. Message ordering matters: Cache hits require prefix matching. Adding or
removing messages in the middle invalidates the cache for everything after.
3. Compression cache interaction: After compression, the cache is invalidated
for the compressed region but the system prompt cache survives. The rolling
3-message window re-establishes caching within 1-2 turns.
4. TTL selection: Default is5m(5 minutes). Use1hfor long-running
sessions where the user takes breaks between turns.
5. Model identity is part of the cache key: Provider-side caches are scoped
to the model (and account/API key) serving the request. Any mid-conversation
model change — an explicit/modelswitch, primary-model fallback, or a
credential-pool rotation onto a different account — means the next request
gets zero cache hits and re-reads the full conversation at undiscounted
input price. This is inherent to how provider caches work, not something
Hermes can avoid; user-facing docs for/model, fallback providers, and
credential pools carry cost warnings for this reason. Don't add features
that silently swap the model or credentials mid-session.

Stable system prompt: The system prompt is breakpoint 1 and cached across
all turns. Avoid mutating it mid-conversation (compression appends a note
only on the first compaction).

Message ordering matters: Cache hits require prefix matching. Adding or
removing messages in the middle invalidates the cache for everything after.

Compression cache interaction: After compression, the cache is invalidated
for the compressed region but the system prompt cache survives. The rolling
3-message window re-establishes caching within 1-2 turns.

TTL selection: Default is5m(5 minutes). Use1hfor long-running
sessions where the user takes breaks between turns.

`5m`
`1h`

Model identity is part of the cache key: Provider-side caches are scoped
to the model (and account/API key) serving the request. Any mid-conversation
model change — an explicit/modelswitch, primary-model fallback, or a
credential-pool rotation onto a different account — means the next request
gets zero cache hits and re-reads the full conversation at undiscounted
input price. This is inherent to how provider caches work, not something
Hermes can avoid; user-facing docs for/model, fallback providers, and
credential pools carry cost warnings for this reason. Don't add features
that silently swap the model or credentials mid-session.

`/model`
`/model`

### Enabling Prompt Caching​

Prompt caching is automatically enabled when:

- The model is an Anthropic Claude model (detected by model name)
- The provider supportscache_control(native Anthropic API or OpenRouter)

`cache_control`

```
# config.yaml — TTL is configurable (must be "5m" or "1h")prompt_caching:  cache_ttl: "5m"
```

The CLI shows caching status at startup:

```
💾 Prompt caching: ENABLED (Claude via OpenRouter, 5m TTL)
```

## Context Pressure Warnings​

Intermediate context-pressure warnings have been removed (see the iteration-budget block inrun_agent.py, which notes: "No intermediate pressure warnings — they caused models to 'give up' prematurely on complex tasks"). Compression fires when prompt tokens reach the configuredcompression.threshold(default 50%) with no prior warning step; gateway session hygiene fires as the secondary safety net at 85% of the model's context window.

`run_agent.py`
`compression.threshold`