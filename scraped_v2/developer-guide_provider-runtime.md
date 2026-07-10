- 
- Developer Guide
- Architecture
- Provider Runtime Resolution

# Provider Runtime Resolution

Hermes has a shared provider runtime resolver used across:

- CLI
- gateway
- cron jobs
- ACP
- auxiliary model calls

Primary implementation:

- hermes_cli/runtime_provider.py— credential resolution,_resolve_custom_runtime()
- hermes_cli/auth.py— provider registry,resolve_provider()
- hermes_cli/model_switch.py— shared/modelswitch pipeline (CLI + gateway)
- agent/auxiliary_client.py— auxiliary model routing
- providers/— ABC + registry entry points (ProviderProfile,register_provider,get_provider_profile,list_providers)
- plugins/model-providers/<name>/— per-provider plugins (bundled) that declareapi_mode,base_url,env_vars,fallback_modelsand register themselves into the registry on first access. User plugins at$HERMES_HOME/plugins/model-providers/<name>/override bundled ones of the same name.

`hermes_cli/runtime_provider.py`
`_resolve_custom_runtime()`
`hermes_cli/auth.py`
`resolve_provider()`
`hermes_cli/model_switch.py`
`/model`
`agent/auxiliary_client.py`
`providers/`
`ProviderProfile`
`register_provider`
`get_provider_profile`
`list_providers`
`plugins/model-providers/<name>/`
`api_mode`
`base_url`
`env_vars`
`fallback_models`
`$HERMES_HOME/plugins/model-providers/<name>/`

get_provider_profile()inproviders/returns aProviderProfilefor a given provider id.runtime_provider.pycalls this at resolution time to get the canonicalbase_url,env_varspriority list,api_mode, andfallback_modelswithout needing to duplicate that data in multiple files. Adding a new plugin underplugins/model-providers/<your-provider>/(or$HERMES_HOME/plugins/model-providers/<your-provider>/) that callsregister_provider()is enough forruntime_provider.pyto pick it up — no branch needed in the resolver itself.

`get_provider_profile()`
`providers/`
`ProviderProfile`
`runtime_provider.py`
`base_url`
`env_vars`
`api_mode`
`fallback_models`
`plugins/model-providers/<your-provider>/`
`$HERMES_HOME/plugins/model-providers/<your-provider>/`
`register_provider()`
`runtime_provider.py`

If you are trying to add a new first-class inference provider, readAdding Providersand theModel Provider Plugin guidealongside this page.

## Resolution precedence​

At a high level, provider resolution uses:

1. explicit CLI/runtime request
2. config.yamlmodel/provider config
3. environment variables
4. provider-specific defaults or auto resolution

`config.yaml`

That ordering matters because Hermes treats the saved model/provider choice as the source of truth for normal runs. This prevents a stale shell export from silently overriding the endpoint a user last selected inhermes model.

`hermes model`

## Providers​

Current provider families include (seeplugins/model-providers/for the complete bundled set):

`plugins/model-providers/`
- OpenRouter
- Nous Portal
- OpenAI Codex
- Copilot / Copilot ACP
- Anthropic (native)
- Google / Gemini (gemini)
- Alibaba / DashScope (alibaba,alibaba-coding-plan)
- DeepSeek
- Z.AI
- Kimi / Moonshot (kimi-coding,kimi-coding-cn)
- MiniMax (minimax,minimax-cn,minimax-oauth)
- Kilo Code
- Hugging Face
- OpenCode Zen / OpenCode Go
- AWS Bedrock
- Azure Foundry
- NVIDIA NIM
- xAI (Grok)
- Arcee
- GMI Cloud
- StepFun
- Qwen OAuth
- Xiaomi
- Ollama Cloud
- LM Studio
- Tencent TokenHub
- Custom (provider: custom) — first-class provider for any OpenAI-compatible endpoint
- Named custom providers (custom_providerslist in config.yaml)

`gemini`
`alibaba`
`alibaba-coding-plan`
`kimi-coding`
`kimi-coding-cn`
`minimax`
`minimax-cn`
`minimax-oauth`
`provider: custom`
`custom_providers`

## Output of runtime resolution​

The runtime resolver returns data such as:

- provider
- api_mode
- base_url
- api_key
- source
- provider-specific metadata like expiry/refresh info

`provider`
`api_mode`
`base_url`
`api_key`
`source`

## Why this matters​

This resolver is the main reason Hermes can share auth/runtime logic between:

- hermes chat
- gateway message handling
- cron jobs running in fresh sessions
- ACP editor sessions
- auxiliary model tasks

`hermes chat`

## OpenRouter and custom OpenAI-compatible base URLs​

Hermes contains logic to avoid leaking the wrong API key to a custom endpoint when multiple provider keys exist (e.g.OPENROUTER_API_KEYandOPENAI_API_KEY).

`OPENROUTER_API_KEY`
`OPENAI_API_KEY`

Each provider's API key is scoped to its own base URL:

- OPENROUTER_API_KEYis only sent toopenrouter.aiendpoints
- OPENAI_API_KEYis used for custom endpoints and as a fallback

`OPENROUTER_API_KEY`
`openrouter.ai`
`OPENAI_API_KEY`

Hermes also distinguishes between:

- a real custom endpoint selected by the user
- the OpenRouter fallback path used when no custom endpoint is configured

That distinction is especially important for:

- local model servers
- non-OpenRouter OpenAI-compatible APIs
- switching providers without re-running setup
- config-saved custom endpoints that should keep working even whenOPENAI_BASE_URLis not exported in the current shell

`OPENAI_BASE_URL`

## Native Anthropic path​

Anthropic is not just "via OpenRouter" anymore.

When provider resolution selectsanthropic, Hermes uses:

`anthropic`
- api_mode = anthropic_messages
- the native Anthropic Messages API
- agent/anthropic_adapter.pyfor translation

`api_mode = anthropic_messages`
`agent/anthropic_adapter.py`

Credential resolution for native Anthropic now prefers refreshable Claude Code credentials over copied env tokens when both are present. In practice that means:

- Claude Code credential files are treated as the preferred source when they include refreshable auth
- manualANTHROPIC_TOKEN/CLAUDE_CODE_OAUTH_TOKENvalues still work as explicit overrides
- Hermes preflights Anthropic credential refresh before native Messages API calls
- Hermes still retries once on a 401 after rebuilding the Anthropic client, as a fallback path

`ANTHROPIC_TOKEN`
`CLAUDE_CODE_OAUTH_TOKEN`

## OpenAI Codex path​

Codex uses a separate Responses API path:

- api_mode = codex_responses
- dedicated credential resolution and auth store support

`api_mode = codex_responses`

## Auxiliary model routing​

Auxiliary tasks such as:

- vision
- web extraction summarization
- context compression summaries
- skills hub operations
- MCP helper operations
- memory flushes

can use their own provider/model routing rather than the main conversational model.

When an auxiliary task is configured with providermain, Hermes resolves that through the same shared runtime path as normal chat. In practice that means:

`main`
- env-driven custom endpoints still work
- custom endpoints saved viahermes model/config.yamlalso work
- auxiliary routing can tell the difference between a real saved custom endpoint and the OpenRouter fallback

`hermes model`
`config.yaml`

## Fallback models​

Hermes supports a configured fallback provider chain — a list of(provider, model)entries tried in order when the primary model encounters errors. The legacy single-pairfallback_modeldict is still accepted for back-compat (and migrated on first write).

`(provider, model)`
`fallback_model`

### How it works internally​

1. Storage:AIAgent.__init__stores thefallback_modeldict and sets_fallback_activated = False.
2. Trigger points:_try_activate_fallback()is called from three places in the main retry loop inrun_agent.py:After max retries on invalid API responses (None choices, missing content)On non-retryable client errors (HTTP 401, 403, 404)After max retries on transient errors (HTTP 429, 500, 502, 503)
3. Activation flow(_try_activate_fallback):ReturnsFalseimmediately if already activated or not configuredCallsresolve_provider_client()fromauxiliary_client.pyto build a new client with proper authDeterminesapi_mode:codex_responsesfor openai-codex,anthropic_messagesfor anthropic,chat_completionsfor everything elseSwaps in-place:self.model,self.provider,self.base_url,self.api_mode,self.client,self._client_kwargsFor anthropic fallback: builds a native Anthropic client instead of OpenAI-compatibleRe-evaluates prompt caching (enabled for Claude models on OpenRouter)Sets_fallback_activated = True— prevents firing againResets retry count to 0 and continues the loop
4. Config flow:CLI:cli.pyreadsCLI_CONFIG["fallback_model"]→ passes toAIAgent(fallback_model=...)Gateway:gateway/run.py._load_fallback_model()readsconfig.yaml→ passes toAIAgentValidation: bothproviderandmodelkeys must be non-empty, or fallback is disabled

Storage:AIAgent.__init__stores thefallback_modeldict and sets_fallback_activated = False.

`AIAgent.__init__`
`fallback_model`
`_fallback_activated = False`

Trigger points:_try_activate_fallback()is called from three places in the main retry loop inrun_agent.py:

`_try_activate_fallback()`
`run_agent.py`
- After max retries on invalid API responses (None choices, missing content)
- On non-retryable client errors (HTTP 401, 403, 404)
- After max retries on transient errors (HTTP 429, 500, 502, 503)

Activation flow(_try_activate_fallback):

`_try_activate_fallback`
- ReturnsFalseimmediately if already activated or not configured
- Callsresolve_provider_client()fromauxiliary_client.pyto build a new client with proper auth
- Determinesapi_mode:codex_responsesfor openai-codex,anthropic_messagesfor anthropic,chat_completionsfor everything else
- Swaps in-place:self.model,self.provider,self.base_url,self.api_mode,self.client,self._client_kwargs
- For anthropic fallback: builds a native Anthropic client instead of OpenAI-compatible
- Re-evaluates prompt caching (enabled for Claude models on OpenRouter)
- Sets_fallback_activated = True— prevents firing again
- Resets retry count to 0 and continues the loop

`False`
`resolve_provider_client()`
`auxiliary_client.py`
`api_mode`
`codex_responses`
`anthropic_messages`
`chat_completions`
`self.model`
`self.provider`
`self.base_url`
`self.api_mode`
`self.client`
`self._client_kwargs`
`_fallback_activated = True`

Config flow:

- CLI:cli.pyreadsCLI_CONFIG["fallback_model"]→ passes toAIAgent(fallback_model=...)
- Gateway:gateway/run.py._load_fallback_model()readsconfig.yaml→ passes toAIAgent
- Validation: bothproviderandmodelkeys must be non-empty, or fallback is disabled

`cli.py`
`CLI_CONFIG["fallback_model"]`
`AIAgent(fallback_model=...)`
`gateway/run.py._load_fallback_model()`
`config.yaml`
`AIAgent`
`provider`
`model`

### What does NOT support fallback​

- Subagent delegation(tools/delegate_tool.py): subagents inherit the parent's provider but not the fallback config
- Auxiliary tasks: use their own independent provider auto-detection chain (see Auxiliary model routing above)

`tools/delegate_tool.py`

Cron jobsdosupport fallback:run_job()readsfallback_providers(or legacyfallback_model) fromconfig.yamland passes it toAIAgent(fallback_model=...), matching the gateway's_load_fallback_model()pattern. SeeCron Internals.

`run_job()`
`fallback_providers`
`fallback_model`
`config.yaml`
`AIAgent(fallback_model=...)`
`_load_fallback_model()`

### Test coverage​

Fallback behavior is exercised across several suites:

- tests/run_agent/test_fallback_credential_isolation.py— credential isolation between primary and fallback
- tests/hermes_cli/test_fallback_cmd.py— the/fallbackCLI command
- tests/gateway/test_fallback_eviction.py— gateway eviction of failed providers

`tests/run_agent/test_fallback_credential_isolation.py`
`tests/hermes_cli/test_fallback_cmd.py`
`/fallback`
`tests/gateway/test_fallback_eviction.py`

## Related docs​

- Agent Loop Internals
- ACP Internals
- Context Compression & Prompt Caching