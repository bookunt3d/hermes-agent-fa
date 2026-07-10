---
layout: docs
title: "حلقه Agent"
permalink: /docs/developer-guide/agent-loop/
---

- 
- Developer Guide
- Architecture
- Agent Loop Internals

# Agent Loop Internals

The core orchestration engine isrun_agent.py'sAIAgentclass — a large file that handles everything from prompt assembly to tool dispatch to provider failover.

`run_agent.py`
`AIAgent`

## Core Responsibilities​

AIAgentis responsible for:

`AIAgent`
- Assembling the effective system prompt and tool schemas viaprompt_builder.py
- Selecting the correct provider/API mode (chat_completions, codex_responses, anthropic_messages)
- Making interruptible model calls with cancellation support
- Executing tool calls (sequentially or concurrently via thread pool)
- Maintaining conversation history in OpenAI message format
- Handling compression, retries, and fallback model switching
- Tracking iteration budgets across parent and child agents
- Flushing persistent memory before context is lost

`prompt_builder.py`

## Two Entry Points​

```
# Simple interface — returns final response stringresponse = agent.chat("Fix the bug in main.py")# Full interface — returns dict with messages, metadata, usage statsresult = agent.run_conversation(    user_message="Fix the bug in main.py",    system_message=None,           # auto-built if omitted    conversation_history=None,      # auto-loaded from session if omitted    task_id="task_abc123")
```

chat()is a thin wrapper aroundrun_conversation()that extracts thefinal_responsefield from the result dict.

`chat()`
`run_conversation()`
`final_response`

## API Modes​

Hermes supports three API execution modes, resolved from provider selection, explicit args, and base URL heuristics:

| API mode | Used for | Client type |
| --- | --- | --- |
| chat_completions | OpenAI-compatible endpoints (OpenRouter, custom, most providers) | openai.OpenAI |
| codex_responses | OpenAI Codex / Responses API | openai.OpenAIwith Responses format |
| anthropic_messages | Native Anthropic Messages API | anthropic.Anthropicvia adapter |

`chat_completions`
`openai.OpenAI`
`codex_responses`
`openai.OpenAI`
`anthropic_messages`
`anthropic.Anthropic`

The mode determines how messages are formatted, how tool calls are structured, how responses are parsed, and how caching/streaming works. All three converge on the same internal message format (OpenAI-stylerole/content/tool_callsdicts) before and after API calls.

`role`
`content`
`tool_calls`

Mode resolution order:

1. Explicitapi_modeconstructor arg (highest priority)
2. Provider-specific detection (e.g.,anthropicprovider →anthropic_messages)
3. Base URL heuristics (e.g.,api.anthropic.com→anthropic_messages)
4. Default:chat_completions

`api_mode`
`anthropic`
`anthropic_messages`
`api.anthropic.com`
`anthropic_messages`
`chat_completions`

## Turn Lifecycle​

Each iteration of the agent loop follows this sequence:

```
run_conversation()  1. Generate task_id if not provided  2. Append user message to conversation history  3. Build or reuse cached system prompt (prompt_builder.py)  4. Check if preflight compression is needed (>50% context)  5. Build API messages from conversation history     - chat_completions: OpenAI format as-is     - codex_responses: convert to Responses API input items     - anthropic_messages: convert via anthropic_adapter.py  6. Inject ephemeral prompt layers (budget warnings, context pressure)  7. Apply prompt caching markers if on Anthropic  8. Make interruptible API call (_interruptible_api_call)  9. Parse response:     - If tool_calls: execute them, append results, loop back to step 5     - If text response: persist session, flush memory if needed, return
```

### Message Format​

All messages use OpenAI-compatible format internally:

```
{"role": "system", "content": "..."}{"role": "user", "content": "..."}{"role": "assistant", "content": "...", "tool_calls": [...]}{"role": "tool", "tool_call_id": "...", "content": "..."}
```

Reasoning content (from models that support extended thinking) is stored inassistant_msg["reasoning"]and optionally displayed via thereasoning_callback.

`assistant_msg["reasoning"]`
`reasoning_callback`

### Message Alternation Rules​

The agent loop enforces strict message role alternation:

- After the system message:User → Assistant → User → Assistant → ...
- During tool calling:Assistant (with tool_calls) → Tool → Tool → ... → Assistant
- Nevertwo assistant messages in a row
- Nevertwo user messages in a row
- Onlytoolrole can have consecutive entries (parallel tool results)

`User → Assistant → User → Assistant → ...`
`Assistant (with tool_calls) → Tool → Tool → ... → Assistant`
`tool`

Providers validate these sequences and will reject malformed histories.

## Interruptible API Calls​

API requests are wrapped in_interruptible_api_call()which runs the actual HTTP call in a background thread while monitoring an interrupt event:

`_interruptible_api_call()`

```
┌────────────────────────────────────────────────────┐│  Main thread                  API thread           ││                                                    ││   wait on:                     HTTP POST           ││    - response ready     ───▶   to provider         ││    - interrupt event                               ││    - timeout                                       │└────────────────────────────────────────────────────┘
```

When interrupted (user sends new message,/stopcommand, or signal):

`/stop`
- The API thread is abandoned (response discarded)
- The agent can process the new input or shut down cleanly
- No partial response is injected into conversation history

## Tool Execution​

### Sequential vs Concurrent​

When the model returns tool calls:

- Single tool call→ executed directly in the main thread
- Multiple tool calls→ executed concurrently viaThreadPoolExecutorException: tools marked as interactive (e.g.,clarify) force sequential executionResults are reinserted in the original tool call order regardless of completion order

`ThreadPoolExecutor`
- Exception: tools marked as interactive (e.g.,clarify) force sequential execution
- Results are reinserted in the original tool call order regardless of completion order

`clarify`

### Execution Flow​

```
for each tool_call in response.tool_calls:    1. Resolve handler from tools/registry.py    2. Fire pre_tool_call plugin hook    3. Check if dangerous command (tools/approval.py)       - If dangerous: invoke approval_callback, wait for user    4. Execute handler with args + task_id    5. Fire post_tool_call plugin hook    6. Append {"role": "tool", "content": result} to history
```

### Agent-Level Tools​

Some tools are intercepted byrun_agent.pybeforereachinghandle_function_call():

`run_agent.py`
`handle_function_call()`
| Tool | Why intercepted |
| --- | --- |
| todo | Reads/writes agent-local task state |
| memory | Writes to persistent memory files with character limits |
| session_search | Queries session history via the agent's session DB |
| delegate_task | Spawns subagent(s) with isolated context |

`todo`
`memory`
`session_search`
`delegate_task`

These tools modify agent state directly and return synthetic tool results without going through the registry.

## Callback Surfaces​

AIAgentsupports platform-specific callbacks that enable real-time progress in the CLI, gateway, and ACP integrations:

`AIAgent`
| Callback | When fired | Used by |
| --- | --- | --- |
| tool_progress_callback | Before/after each tool execution | CLI spinner, gateway progress messages |
| thinking_callback | When model starts/stops thinking | CLI "thinking..." indicator |
| reasoning_callback | When model returns reasoning content | CLI reasoning display, gateway reasoning blocks |
| clarify_callback | Whenclarifytool is called | CLI input prompt, gateway interactive message |
| step_callback | After each complete agent turn | Gateway step tracking, ACP progress |
| stream_delta_callback | Each streaming token (when enabled) | CLI streaming display |
| tool_gen_callback | When tool call is parsed from stream | CLI tool preview in spinner |
| status_callback | State changes (thinking, executing, etc.) | ACP status updates |

`tool_progress_callback`
`thinking_callback`
`reasoning_callback`
`clarify_callback`
`clarify`
`step_callback`
`stream_delta_callback`
`tool_gen_callback`
`status_callback`

## Budget and Fallback Behavior​

### Iteration Budget​

The agent tracks iterations viaIterationBudget:

`IterationBudget`
- Default: 90 iterations (configurable viaagent.max_turns)
- Each agent gets its own budget. Subagents get independent budgets capped atdelegation.max_iterations(default 50) — total iterations across parent + subagents can exceed the parent's cap
- At 100%, the agent stops and returns a summary of work done

`agent.max_turns`
`delegation.max_iterations`

### Fallback Model​

When the primary model fails (429 rate limit, 5xx server error, 401/403 auth error):

1. Checkfallback_providerslist in config
2. Try each fallback in order
3. On success, continue the conversation with the new provider
4. On 401/403, attempt credential refresh before failing over

`fallback_providers`

The fallback system also covers auxiliary tasks independently — vision, compression, and web extraction each have their own fallback chain configurable via theauxiliary.*config section.

`auxiliary.*`

## Compression and Persistence​

### When Compression Triggers​

- Preflight(before API call): If conversation exceeds 50% of model's context window
- Gateway auto-compression: If conversation exceeds 85% (more aggressive, runs between turns)

### What Happens During Compression​

1. Memory is flushed to disk first (preventing data loss)
2. Middle conversation turns are summarized into a compact summary
3. The last N messages are preserved intact (compression.protect_last_n, default: 20)
4. Tool call/result message pairs are kept together (never split)
5. A new session lineage ID is generated (compression creates a "child" session)

`compression.protect_last_n`

### Session Persistence​

After each turn:

- Messages are saved to the session store (SQLite viahermes_state.py)
- Memory changes are flushed toMEMORY.md/USER.md
- The session can be resumed later via/resumeorhermes chat --resume

`hermes_state.py`
`MEMORY.md`
`USER.md`
`/resume`
`hermes chat --resume`

## Key Source Files​

| File | Purpose |
| --- | --- |
| run_agent.py | AIAgent class — the complete agent loop |
| agent/prompt_builder.py | System prompt assembly from memory, skills, context files, personality |
| agent/context_engine.py | ContextEngine ABC — pluggable context management |
| agent/context_compressor.py | Default engine — lossy summarization algorithm |
| agent/prompt_caching.py | Anthropic prompt caching markers and cache metrics |
| agent/auxiliary_client.py | Auxiliary LLM client for side tasks (vision, summarization) |
| model_tools.py | Tool schema collection,handle_function_call()dispatch |

`run_agent.py`
`agent/prompt_builder.py`
`agent/context_engine.py`
`agent/context_compressor.py`
`agent/prompt_caching.py`
`agent/auxiliary_client.py`
`model_tools.py`
`handle_function_call()`

## Related Docs​

- Provider Runtime Resolution
- Prompt Assembly
- Context Compression & Prompt Caching
- Tools Runtime
- Architecture Overview