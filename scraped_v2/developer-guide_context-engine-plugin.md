- 
- Developer Guide
- Extending
- Plugins
- Context Engine Plugins

# Building a Context Engine Plugin

Context engine plugins replace the built-inContextCompressorwith an alternative strategy for managing conversation context. For example, a Lossless Context Management (LCM) engine that builds a knowledge DAG instead of lossy summarization.

`ContextCompressor`

## How it works​

The agent's context management is built on theContextEngineABC (agent/context_engine.py). The built-inContextCompressoris the default implementation. Plugin engines must implement the same interface.

`ContextEngine`
`agent/context_engine.py`
`ContextCompressor`

Onlyonecontext engine can be active at a time. Selection is config-driven:

```
# config.yamlcontext:  engine: "compressor"    # default built-in  engine: "lcm"           # activates a plugin engine named "lcm"
```

Plugin engines arenever auto-activated— the user must explicitly setcontext.engineto the plugin's name.

`context.engine`

## Directory structure​

Each context engine lives inplugins/context_engine/<name>/:

`plugins/context_engine/<name>/`

```
plugins/context_engine/lcm/├── __init__.py      # exports the ContextEngine subclass├── plugin.yaml      # metadata (name, description, version)└── ...              # any other modules your engine needs
```

## The ContextEngine ABC​

Your engine must implement theserequiredmethods:

```
from agent.context_engine import ContextEngineclass LCMEngine(ContextEngine):    @property    def name(self) -> str:        """Short identifier, e.g. 'lcm'. Must match config.yaml value."""        return "lcm"    def update_from_response(self, usage: dict) -> None:        """Called after every LLM call with the usage dict.        Update self.last_prompt_tokens, self.last_completion_tokens,        self.last_total_tokens from the response.        """    def should_compress(self, prompt_tokens: int = None) -> bool:        """Return True if compaction should fire this turn."""    def compress(self, messages: list, current_tokens: int = None,                 focus_topic: str = None) -> list:        """Compact the message list and return a new (possibly shorter) list.        The returned list must be a valid OpenAI-format message sequence.        ``focus_topic`` is an optional topic string from manual        ``/compress <focus>``; engines that support guided compression should        prioritise preserving information related to it, others may ignore it.        """
```

### Class attributes your engine must maintain​

The agent reads these directly for display and logging:

```
last_prompt_tokens: int = 0last_completion_tokens: int = 0last_total_tokens: int = 0threshold_tokens: int = 0        # when compression triggerscontext_length: int = 0          # model's full context windowcompression_count: int = 0       # how many times compress() has run
```

### Optional methods​

These have sensible defaults in the ABC. Override as needed:

| Method | Default | Override when |
| --- | --- | --- |
| on_session_start(session_id, **kwargs) | No-op | You need to load persisted state (DAG, DB) |
| on_session_end(session_id, messages) | No-op | You need to flush state, close connections |
| on_session_reset() | Resets token counters | You have per-session state to clear |
| update_model(model, context_length, ...) | Updates context_length + threshold | You need to recalculate budgets on model switch |
| get_tool_schemas() | Returns[] | Your engine provides agent-callable tools (e.g.,lcm_grep) |
| handle_tool_call(name, args, **kwargs) | Returns error JSON | You implement tool handlers |
| should_compress_preflight(messages) | ReturnsFalse | You can do a cheap pre-API-call estimate |
| get_status() | Standard token/threshold dict | You have custom metrics to expose |

`on_session_start(session_id, **kwargs)`
`on_session_end(session_id, messages)`
`on_session_reset()`
`update_model(model, context_length, ...)`
`get_tool_schemas()`
`[]`
`lcm_grep`
`handle_tool_call(name, args, **kwargs)`
`should_compress_preflight(messages)`
`False`
`get_status()`

## Engine tools​

Context engines can expose tools the agent calls directly. Return schemas fromget_tool_schemas()and handle calls inhandle_tool_call():

`get_tool_schemas()`
`handle_tool_call()`

```
def get_tool_schemas(self):    return [{        "name": "lcm_grep",        "description": "Search the context knowledge graph",        "parameters": {            "type": "object",            "properties": {                "query": {"type": "string", "description": "Search query"}            },            "required": ["query"],        },    }]def handle_tool_call(self, name, args, **kwargs):    if name == "lcm_grep":        results = self._search_dag(args["query"])        return json.dumps({"results": results})    return json.dumps({"error": f"Unknown tool: {name}"})
```

Engine tools are injected into the agent's tool list at startup and dispatched automatically — no registry registration needed.

## Registration​

### Via directory (recommended)​

Place your engine inplugins/context_engine/<name>/. The__init__.pymust export aContextEnginesubclass. The discovery system finds and instantiates it automatically.

`plugins/context_engine/<name>/`
`__init__.py`
`ContextEngine`

### Via general plugin system​

A general plugin can also register a context engine:

```
def register(ctx):    engine = LCMEngine(context_length=200000)    ctx.register_context_engine(engine)
```

Only one engine can be registered. A second plugin attempting to register is rejected with a warning.

## Lifecycle​

```
1. Engine instantiated (plugin load or directory discovery)2. on_session_start() — conversation begins3. update_from_response() — after each API call4. should_compress() — checked each turn5. compress() — called when should_compress() returns True6. on_session_end() — session boundary (CLI exit, /reset, gateway expiry)
```

on_session_reset()is called on/newor/resetto clear per-session state without a full shutdown.

`on_session_reset()`
`/new`
`/reset`

## Configuration​

Users select your engine viahermes plugins→ Provider Plugins → Context Engine, or by editingconfig.yaml:

`hermes plugins`
`config.yaml`

```
context:  engine: "lcm"   # must match your engine's name property
```

Thecompressionconfig block (compression.threshold,compression.protect_last_n, etc.) is specific to the built-inContextCompressor. Your engine should define its own config format if needed, reading fromconfig.yamlduring initialization.

`compression`
`compression.threshold`
`compression.protect_last_n`
`ContextCompressor`
`config.yaml`

## Testing​

```
from agent.context_engine import ContextEnginedef test_engine_satisfies_abc():    engine = YourEngine(context_length=200000)    assert isinstance(engine, ContextEngine)    assert engine.name == "your-name"def test_compress_returns_valid_messages():    engine = YourEngine(context_length=200000)    msgs = [{"role": "user", "content": "hello"}]    result = engine.compress(msgs)    assert isinstance(result, list)    assert all("role" in m for m in result)
```

Seetests/agent/test_context_engine.pyfor the full ABC contract test suite.

`tests/agent/test_context_engine.py`

## See also​

- Context Compression and Caching— how the built-in compressor works
- Memory Provider Plugins— analogous single-select plugin system for memory
- Plugins— general plugin system overview