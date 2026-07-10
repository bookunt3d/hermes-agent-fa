---
layout: docs
title: "Features_Delegation"
permalink: /docs/user-guide/features/delegation/
---

- 
- Features
- Automation
- Subagent Delegation

# Subagent Delegation

Thedelegate_tasktool spawns child AIAgent instances with isolated context, restricted toolsets, and their own terminal sessions. Each child gets a fresh conversation and works independently — only its final summary enters the parent's context.

`delegate_task`

## Single Task​

```
delegate_task(    goal="Debug why tests fail",    context="Error: assertion in test_foo.py line 42",    toolsets=["terminal", "file"])
```

## Parallel Batch​

Up to 3 concurrent subagents by default (configurable, no hard ceiling):

```
delegate_task(tasks=[    {"goal": "Research topic A", "toolsets": ["web"]},    {"goal": "Research topic B", "toolsets": ["web"]},    {"goal": "Fix the build", "toolsets": ["terminal", "file"]}])
```

## How Subagent Context Works​

Subagents start with acompletely fresh conversation. They have zero knowledge of the parent's conversation history, prior tool calls, or anything discussed before delegation. The subagent's only context comes from thegoalandcontextfields the parent agent populates when it callsdelegate_task.

`goal`
`context`
`delegate_task`

This means the parent agent must passeverythingthe subagent needs in the call:

```
# BAD - subagent has no idea what "the error" isdelegate_task(goal="Fix the error")# GOOD - subagent has all context it needsdelegate_task(    goal="Fix the TypeError in api/handlers.py",    context="""The file api/handlers.py has a TypeError on line 47:    'NoneType' object has no attribute 'get'.    The function process_request() receives a dict from parse_body(),    but parse_body() returns None when Content-Type is missing.    The project is at /home/user/myproject and uses Python 3.11.""")
```

The subagent receives a focused system prompt built from your goal and context, instructing it to complete the task and provide a structured summary of what it did, what it found, any files modified, and any issues encountered.

## Practical Examples​

### Parallel Research​

Research multiple topics simultaneously and collect summaries:

```
delegate_task(tasks=[    {        "goal": "Research the current state of WebAssembly in 2025",        "context": "Focus on: browser support, non-browser runtimes, language support",        "toolsets": ["web"]    },    {        "goal": "Research the current state of RISC-V adoption in 2025",        "context": "Focus on: server chips, embedded systems, software ecosystem",        "toolsets": ["web"]    },    {        "goal": "Research quantum computing progress in 2025",        "context": "Focus on: error correction breakthroughs, practical applications, key players",        "toolsets": ["web"]    }])
```

### Code Review + Fix​

Delegate a review-and-fix workflow to a fresh context:

```
delegate_task(    goal="Review the authentication module for security issues and fix any found",    context="""Project at /home/user/webapp.    Auth module files: src/auth/login.py, src/auth/jwt.py, src/auth/middleware.py.    The project uses Flask, PyJWT, and bcrypt.    Focus on: SQL injection, JWT validation, password handling, session management.    Fix any issues found and run the test suite (pytest tests/auth/).""",    toolsets=["terminal", "file"])
```

### Multi-File Refactoring​

Delegate a large refactoring task that would flood the parent's context:

```
delegate_task(    goal="Refactor all Python files in src/ to replace print() with proper logging",    context="""Project at /home/user/myproject.    Use the 'logging' module with logger = logging.getLogger(__name__).    Replace print() calls with appropriate log levels:    - print(f"Error: ...") -> logger.error(...)    - print(f"Warning: ...") -> logger.warning(...)    - print(f"Debug: ...") -> logger.debug(...)    - Other prints -> logger.info(...)    Don't change print() in test files or CLI output.    Run pytest after to verify nothing broke.""",    toolsets=["terminal", "file"])
```

## Batch Mode Details​

When you provide atasksarray, subagents run inparallelusing a thread pool:

`tasks`
- Maximum concurrency:3 tasks by default (configurable viadelegation.max_concurrent_childrenor theDELEGATION_MAX_CONCURRENT_CHILDRENenv var; floor of 1, no hard ceiling). Batches larger than the limit return a tool error rather than being silently truncated.
- Thread pool:UsesThreadPoolExecutorwith the configured concurrency limit as max workers
- Progress display:In CLI mode, a tree-view shows tool calls from each subagent in real-time with per-task completion lines. In gateway mode, progress is batched and relayed to the parent's progress callback
- Result ordering:Results are sorted by task index to match input order regardless of completion order
- Interrupt propagation:Interrupting the parent (e.g., sending a new message) interrupts all active children

`delegation.max_concurrent_children`
`DELEGATION_MAX_CONCURRENT_CHILDREN`
`ThreadPoolExecutor`

Single-task delegation runs directly without thread pool overhead.

## Model Override​

You can configure a different model for subagents viaconfig.yaml— useful for delegating simple tasks to cheaper/faster models:

`config.yaml`

```
# In ~/.hermes/config.yamldelegation:  model: "google/gemini-flash-2.0"    # Cheaper model for subagents  provider: "openrouter"              # Optional: route subagents to a different provider
```

If omitted, subagents use the same model as the parent.

## Toolset Selection Tips​

Thetoolsetsparameter controls what tools the subagent has access to. Choose based on the task:

`toolsets`
| Toolset Pattern | Use Case |
| --- | --- |
| ["terminal", "file"] | Code work, debugging, file editing, builds |
| ["web"] | Research, fact-checking, documentation lookup |
| ["terminal", "file", "web"] | Full-stack tasks (default) |
| ["file"] | Read-only analysis, code review without execution |
| ["terminal"] | System administration, process management |

`["terminal", "file"]`
`["web"]`
`["terminal", "file", "web"]`
`["file"]`
`["terminal"]`

Certain toolsets are blocked for subagents regardless of what you specify:

- delegation— blocked for leaf subagents (the default). Retained forrole="orchestrator"children, bounded bymax_spawn_depth— seeDepth Limit and Nested Orchestrationbelow.
- clarify— subagents cannot interact with the user
- memory— no writes to shared persistent memory
- code_execution— children should reason step-by-step

`delegation`
`role="orchestrator"`
`max_spawn_depth`
`clarify`
`memory`
`code_execution`

## Max Iterations​

Each subagent has an iteration limit (default: 50) that controls how many tool-calling turns it can take:

```
delegate_task(    goal="Quick file check",    context="Check if /etc/nginx/nginx.conf exists and print its first 10 lines",    max_iterations=10  # Simple task, don't need many turns)
```

## Child Timeout​

By default there isno wall-clock timeouton subagents. Children fail only from what they're actually doing — API errors, tool errors, or hitting their iteration budget — never from a delegation-level stopwatch. Earlier releases shipped a hard cap (300s, later 600s), which kept killing legitimately busy children mid-task: deep code reviews, large research fan-outs, and slow reasoning models routinely need more than 10 minutes while making steady progress the whole time.

Genuinely stuck children are still detected: the heartbeat staleness monitor stops refreshing the parent's activity when a child makes no progress (no API calls, no tool starts), letting the gateway inactivity timeout fire on a truly wedged worker.

If you want a hard cap anyway (e.g. cost control on unattended cron-driven delegation), opt in per-install:

```
delegation:  child_timeout_seconds: 0     # default: 0 = no timeout  # child_timeout_seconds: 1800  # opt-in hard cap (floor 30s)
```

A positive value enforces a hard wall-clock limit on each child;0or a negative value disables it.

`0`

With a hard cap configured, if a subagent times out having madezeroAPI calls (usually: provider unreachable, auth failure, or tool-schema rejection),delegate_taskwrites a structured diagnostic to~/.hermes/logs/subagent-timeout-<session>-<timestamp>.logcontaining the subagent's config snapshot, credential-resolution trace, and any early error messages. Much easier to root-cause than the previous silent-timeout behavior.

`delegate_task`
`~/.hermes/logs/subagent-timeout-<session>-<timestamp>.log`

## Monitoring Running Subagents (/agents)​

`/agents`

The TUI ships a/agentsoverlay (alias/tasks) that turns recursivedelegate_taskfan-out into a first-class audit surface:

`/agents`
`/tasks`
`delegate_task`
- Live tree view of running and recently-finished subagents, grouped by parent
- Per-branch cost, token, and file-touched rollups
- Kill and pause controls — cancel a specific subagent mid-flight without interrupting its siblings
- Post-hoc review: step through each subagent's turn-by-turn history even after they've returned to the parent

The classic CLI just prints/agentsas a text summary; the TUI is where the overlay shines. SeeTUI — Slash commands.

`/agents`

## Depth Limit and Nested Orchestration​

By default, delegation isflat: a parent (depth 0) spawns children (depth 1), and those children cannot delegate further. This prevents runaway recursive delegation.

For multi-stage workflows (research → synthesis, or parallel orchestration over sub-problems), a parent can spawnorchestratorchildren thatcandelegate their own workers:

```
delegate_task(    goal="Survey three code review approaches and recommend one",    role="orchestrator",  # Allows this child to spawn its own workers    context="...",)
```

- role="leaf"(default): child cannot delegate further — identical to the flat-delegation behavior.
- role="orchestrator": child retains thedelegationtoolset. Gated bydelegation.max_spawn_depth(default1= flat, sorole="orchestrator"is a no-op at defaults). Raisemax_spawn_depthto 2 to allow orchestrator children to spawn leaf grandchildren; 3+ for deeper trees. There is no upper ceiling — cost is the practical limit.
- delegation.orchestrator_enabled: false: global kill switch that forces every child toleafregardless of theroleparameter.

`role="leaf"`
`role="orchestrator"`
`delegation`
`delegation.max_spawn_depth`
`role="orchestrator"`
`max_spawn_depth`
`delegation.orchestrator_enabled: false`
`leaf`
`role`

Cost warning:Withmax_spawn_depth: 3andmax_concurrent_children: 3, the tree can reach 3×3×3 = 27 concurrent leaf agents. Each extra level multiplies spend — raisemax_spawn_depthintentionally.

`max_spawn_depth: 3`
`max_concurrent_children: 3`
`max_spawn_depth`

## Lifetime and Durability​

delegate_taskrunsinside the parent's current turn. It blocks the parent until every child finishes (or is cancelled). It isnota background job queue:

`delegate_task`
- If the parent is interrupted (user sends a new message,/stop,/new), all active children are cancelled and returnstatus="interrupted". Their in-progress work is discarded.
- Children donotcontinue running after the parent turn ends.
- Cancelled children return a structured result (status="interrupted",exit_reason="interrupted"), but because the parent was interrupted too, that result often never makes it into a user-visible reply.

`/stop`
`/new`
`status="interrupted"`
`status="interrupted"`
`exit_reason="interrupted"`

Fordurable long-running workthat must survive interrupts or outlive the current turn, use:

- cronjob(action=create) — schedules a separate agent run; immune to parent-turn interrupts.
- terminal(background=True, notify_on_complete=True)— long-running shell commands that keep running while the agent does other things.

`cronjob`
`create`
`terminal(background=True, notify_on_complete=True)`

## Key Properties​

- Each subagent gets itsown terminal session(separate from the parent)
- Nested delegation is opt-in— onlyrole="orchestrator"children can delegate further, and only whenmax_spawn_depthis raised from its default of 1 (flat). Disable globally withorchestrator_enabled: false.
- Leaf subagentscannotcall:delegate_task,clarify,memory,execute_code. Orchestrator subagents retaindelegate_taskbut still cannot use the other three.
- Interrupt propagation— interrupting the parent interrupts all active children (including grandchildren under orchestrators)
- Only the final summary enters the parent's context, keeping token usage efficient
- Subagents inherit the parent'sAPI key, provider configuration, and credential pool(enabling key rotation on rate limits)

`role="orchestrator"`
`max_spawn_depth`
`orchestrator_enabled: false`
`delegate_task`
`clarify`
`memory`
`execute_code`
`delegate_task`

## Delegation vs execute_code​

| Factor | delegate_task | execute_code |
| --- | --- | --- |
| Reasoning | Full LLM reasoning loop | Just Python code execution |
| Context | Fresh isolated conversation | No conversation, just script |
| Tool access | All non-blocked tools with reasoning | 7 tools via RPC, no reasoning |
| Parallelism | 3 concurrent subagents by default (configurable) | Single script |
| Best for | Complex tasks needing judgment | Mechanical multi-step pipelines |
| Token cost | Higher (full LLM loop) | Lower (only stdout returned) |
| User interaction | None (subagents can't clarify) | None |

Rule of thumb:Usedelegate_taskwhen the subtask requires reasoning, judgment, or multi-step problem solving. Useexecute_codewhen you need mechanical data processing or scripted workflows.

`delegate_task`
`execute_code`

## Configuration​

```
# In ~/.hermes/config.yamldelegation:  max_iterations: 50                        # Max turns per child (default: 50)  # max_concurrent_children: 3              # Parallel children per batch (default: 3)  # max_spawn_depth: 1                      # Tree depth (floor 1, no ceiling, default 1 = flat). Raise to 2 to allow orchestrator children to spawn leaves; 3+ for deeper trees.  # orchestrator_enabled: true              # Disable to force all children to leaf role.  model: "google/gemini-3-flash-preview"             # Optional provider/model override  provider: "openrouter"                             # Optional built-in provider  api_mode: anthropic_messages                       # optional; auto-detected from base_url for anthropic_messages endpoints# Or use a direct custom endpoint instead of provider:delegation:  model: "qwen2.5-coder"  base_url: "http://localhost:1234/v1"  api_key: "local-key"  # api_mode: "anthropic_messages"  # Optional. Wire protocol override for base_url ("chat_completions", "codex_responses", or "anthropic_messages"). Empty = auto-detect from URL (e.g. /anthropic suffix). Set explicitly for endpoints the heuristic can't classify (Azure AI Foundry, MiniMax, Zhipu GLM, LiteLLM proxies, …).
```

Whenbase_urlpoints at an Anthropic-compatible endpoint — for example a path ending in/anthropic, an Azure Foundry Claude route, or a MiniMax/anthropicproxy —api_modeis auto-detected asanthropic_messagesso the subagent uses the right wire format without you setting anything. Setapi_modeexplicitly when the auto-detection guess is wrong (rare).

`base_url`
`/anthropic`
`/anthropic`
`api_mode`
`anthropic_messages`
`api_mode`

The agent handles delegation automatically based on the task complexity. You don't need to explicitly ask it to delegate — it will do so when it makes sense.