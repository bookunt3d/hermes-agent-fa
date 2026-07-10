- 
- Developer Guide
- Extending
- Adding Providers

# Adding Providers

Hermes can already talk to any OpenAI-compatible endpoint through the custom provider path. Do not add a built-in provider unless you want first-class UX for that service:

- provider-specific auth or token refresh
- a curated model catalog
- setup /hermes modelmenu entries
- provider aliases forprovider:modelsyntax
- a non-OpenAI API shape that needs an adapter

`hermes model`
`provider:model`

If the provider is just "another OpenAI-compatible base URL and API key", a named custom provider may be enough.

## The mental model​

A built-in provider has to line up across a few layers:

1. hermes_cli/auth.pydecides how credentials are found.
2. hermes_cli/runtime_provider.pyturns that into runtime data:providerapi_modebase_urlapi_keysource
3. run_agent.pyusesapi_modeto decide how requests are built and sent.
4. hermes_cli/models.pyandhermes_cli/main.pymake the provider show up in the CLI. (hermes_cli/setup.pydelegates tomain.pyautomatically — no changes needed there.)
5. agent/auxiliary_client.pyandagent/model_metadata.pykeep side tasks and token budgeting working.

`hermes_cli/auth.py`
`hermes_cli/runtime_provider.py`
- provider
- api_mode
- base_url
- api_key
- source

`provider`
`api_mode`
`base_url`
`api_key`
`source`
`run_agent.py`
`api_mode`
`hermes_cli/models.py`
`hermes_cli/main.py`
`hermes_cli/setup.py`
`main.py`
`agent/auxiliary_client.py`
`agent/model_metadata.py`

The important abstraction isapi_mode.

`api_mode`
- Most providers usechat_completions.
- Codex usescodex_responses.
- Anthropic usesanthropic_messages.
- A new non-OpenAI protocol usually means adding a new adapter and a newapi_modebranch.

`chat_completions`
`codex_responses`
`anthropic_messages`
`api_mode`

## Choose the implementation path first​

### Path A — OpenAI-compatible provider​

Use this when the provider accepts standard chat-completions style requests.

Typical work:

- add auth metadata
- add model catalog / aliases
- add runtime resolution
- add CLI menu wiring
- add aux-model defaults
- add tests and user docs

You usually do not need a new adapter or a newapi_mode.

`api_mode`

### Path B — Native provider​

Use this when the provider does not behave like OpenAI chat completions.

Examples in-tree today:

- codex_responses
- anthropic_messages

`codex_responses`
`anthropic_messages`

This path includes everything from Path A plus:

- a provider adapter inagent/
- run_agent.pybranches for request building, dispatch, usage extraction, interrupt handling, and response normalization
- adapter tests

`agent/`
`run_agent.py`

## File checklist​

### Required for every built-in provider​

1. hermes_cli/auth.py
2. hermes_cli/models.py
3. hermes_cli/runtime_provider.py
4. hermes_cli/main.py
5. agent/auxiliary_client.py
6. agent/model_metadata.py
7. tests
8. user-facing docs underwebsite/docs/

`hermes_cli/auth.py`
`hermes_cli/models.py`
`hermes_cli/runtime_provider.py`
`hermes_cli/main.py`
`agent/auxiliary_client.py`
`agent/model_metadata.py`
`website/docs/`

hermes_cli/setup.pydoesnotneed changes. The setup wizard delegates provider/model selection toselect_provider_and_model()inmain.py— any provider added there is automatically available inhermes setup.

`hermes_cli/setup.py`
`select_provider_and_model()`
`main.py`
`hermes setup`

### Additional for native / non-OpenAI providers​

1. agent/<provider>_adapter.py
2. run_agent.py
3. pyproject.tomlif a provider SDK is required

`agent/<provider>_adapter.py`
`run_agent.py`
`pyproject.toml`

## Fast path: Simple API-key providers​

If your provider is just an OpenAI-compatible endpoint that authenticates with a single API key, you do not need to touchauth.py,runtime_provider.py,main.py, or any of the other files in the full checklist below.

`auth.py`
`runtime_provider.py`
`main.py`

All you need is:

1. A plugin directory underplugins/model-providers/<your-provider>/containing:__init__.py— callsregister_provider(profile)at module-levelplugin.yaml— manifest (name, kind: model-provider, version, description)
2. That's it. Provider plugins auto-load the first time anything callsget_provider_profile()orlist_providers()— bundled plugins (this repo) and user plugins at$HERMES_HOME/plugins/model-providers/both get picked up.

`plugins/model-providers/<your-provider>/`
- __init__.py— callsregister_provider(profile)at module-level
- plugin.yaml— manifest (name, kind: model-provider, version, description)

`__init__.py`
`register_provider(profile)`
`plugin.yaml`
`get_provider_profile()`
`list_providers()`
`$HERMES_HOME/plugins/model-providers/`

When you add a plugin and it callsregister_provider(), the following wire up automatically:

`register_provider()`
1. PROVIDER_REGISTRYentry inauth.py(credential resolution, env-var lookup)
2. api_modeset tochat_completions
3. base_urlsourced from the config or the declared env var
4. env_varschecked in priority order for the API key
5. fallback_modelslist registered for the provider
6. --providerCLI flag accepts the provider id
7. hermes modelmenu includes the provider
8. hermes setupwizard delegates tomain.pyautomatically
9. provider:modelalias syntax works
10. Runtime resolver returns the correctbase_urlandapi_key
11. --provider <name>CLI flag accepts the provider id
12. Fallback model activation can switch into the provider cleanly

`PROVIDER_REGISTRY`
`auth.py`
`api_mode`
`chat_completions`
`base_url`
`env_vars`
`fallback_models`
`--provider`
`hermes model`
`hermes setup`
`main.py`
`provider:model`
`base_url`
`api_key`
`--provider <name>`

User plugins at$HERMES_HOME/plugins/model-providers/<name>/override bundled plugins of the same name (last-writer-wins inregister_provider()) — so third parties can monkey-patch or replace any built-in profile without editing the repo.

`$HERMES_HOME/plugins/model-providers/<name>/`
`register_provider()`

Seeplugins/model-providers/nvidia/orplugins/model-providers/gmi/as a template, and the fullModel Provider Plugin guidefor field reference, hook idioms, and end-to-end examples.

`plugins/model-providers/nvidia/`
`plugins/model-providers/gmi/`

## Full path: OAuth and complex providers​

Use the full checklist below when your provider needs any of the following:

- OAuth or token refresh (Nous Portal, Codex, Qwen Portal, Copilot)
- A non-OpenAI API shape that requires a new adapter (Anthropic Messages, Codex Responses)
- Custom endpoint detection or multi-region probing (z.ai, Kimi)
- A curated static model catalog or live/modelsfetch
- Provider-specifichermes modelmenu entries with bespoke auth flows

`/models`
`hermes model`

## Step 1: Pick one canonical provider id​

Choose a single provider id and use it everywhere.

Examples from the repo:

- openai-codex
- kimi-coding
- minimax-cn

`openai-codex`
`kimi-coding`
`minimax-cn`

That same id should appear in:

- PROVIDER_REGISTRYinhermes_cli/auth.py
- _PROVIDER_LABELSinhermes_cli/models.py
- _PROVIDER_ALIASESin bothhermes_cli/auth.pyandhermes_cli/models.py
- CLI--providerchoices inhermes_cli/main.py
- setup / model selection branches
- auxiliary-model defaults
- tests

`PROVIDER_REGISTRY`
`hermes_cli/auth.py`
`_PROVIDER_LABELS`
`hermes_cli/models.py`
`_PROVIDER_ALIASES`
`hermes_cli/auth.py`
`hermes_cli/models.py`
`--provider`
`hermes_cli/main.py`

If the id differs between those files, the provider will feel half-wired: auth may work while/model, setup, or runtime resolution silently misses it.

`/model`

## Step 2: Add auth metadata inhermes_cli/auth.py​

`hermes_cli/auth.py`

For API-key providers, add aProviderConfigentry toPROVIDER_REGISTRYwith:

`ProviderConfig`
`PROVIDER_REGISTRY`
- id
- name
- auth_type="api_key"
- inference_base_url
- api_key_env_vars
- optionalbase_url_env_var

`id`
`name`
`auth_type="api_key"`
`inference_base_url`
`api_key_env_vars`
`base_url_env_var`

Also add aliases to_PROVIDER_ALIASES.

`_PROVIDER_ALIASES`

Use the existing providers as templates:

- simple API-key path: Z.AI, MiniMax
- API-key path with endpoint detection: Kimi, Z.AI
- native token resolution: Anthropic
- OAuth / auth-store path: Nous, OpenAI Codex

Questions to answer here:

- What env vars should Hermes check, and in what priority order?
- Does the provider need base-URL overrides?
- Does it need endpoint probing or token refresh?
- What should the auth error say when credentials are missing?

If the provider needs something more than "look up an API key", add a dedicated credential resolver instead of shoving logic into unrelated branches.

## Step 3: Add model catalog and aliases inhermes_cli/models.py​

`hermes_cli/models.py`

Update the provider catalog so the provider works in menus and inprovider:modelsyntax.

`provider:model`

Typical edits:

- _PROVIDER_MODELS
- _PROVIDER_LABELS
- _PROVIDER_ALIASES
- provider display order insidelist_available_providers()
- provider_model_ids()if the provider supports a live/modelsfetch

`_PROVIDER_MODELS`
`_PROVIDER_LABELS`
`_PROVIDER_ALIASES`
`list_available_providers()`
`provider_model_ids()`
`/models`

If the provider exposes a live model list, prefer that first and keep_PROVIDER_MODELSas the static fallback.

`_PROVIDER_MODELS`

This file is also what makes inputs like these work:

```
anthropic:claude-sonnet-4-6kimi:model-name
```

If aliases are missing here, the provider may authenticate correctly but still fail in/modelparsing.

`/model`

## Step 4: Resolve runtime data inhermes_cli/runtime_provider.py​

`hermes_cli/runtime_provider.py`

resolve_runtime_provider()is the shared path used by CLI, gateway, cron, ACP, and helper clients.

`resolve_runtime_provider()`

Add a branch that returns a dict with at least:

```
{    "provider": "your-provider",    "api_mode": "chat_completions",  # or your native mode    "base_url": "https://...",    "api_key": "...",    "source": "env|portal|auth-store|explicit",    "requested_provider": requested_provider,}
```

If the provider is OpenAI-compatible,api_modeshould usually staychat_completions.

`api_mode`
`chat_completions`

Be careful with API-key precedence. Hermes already contains logic to avoid leaking an OpenRouter key to unrelated endpoints. A new provider should be equally explicit about which key goes to which base URL.

## Step 5: Wire the CLI inhermes_cli/main.py​

`hermes_cli/main.py`

A provider is not discoverable until it shows up in the interactivehermes modelflow.

`hermes model`

Update these inhermes_cli/main.py:

`hermes_cli/main.py`
- provider_labelsdict
- providerslist inselect_provider_and_model()
- provider dispatch (if selected_provider == ...)
- --providerargument choices
- login/logout choices if the provider supports those flows
- a_model_flow_<provider>()function, or reuse_model_flow_api_key_provider()if it fits

`provider_labels`
`providers`
`select_provider_and_model()`
`if selected_provider == ...`
`--provider`
`_model_flow_<provider>()`
`_model_flow_api_key_provider()`

hermes_cli/setup.pydoes not need changes — it callsselect_provider_and_model()frommain.py, so your new provider appears in bothhermes modelandhermes setupautomatically.

`hermes_cli/setup.py`
`select_provider_and_model()`
`main.py`
`hermes model`
`hermes setup`

## Step 6: Keep auxiliary calls working​

Two files matter here:

### agent/auxiliary_client.py​

`agent/auxiliary_client.py`

Add a cheap / fast default aux model to_API_KEY_PROVIDER_AUX_MODELSif this is a direct API-key provider.

`_API_KEY_PROVIDER_AUX_MODELS`

Auxiliary tasks include things like:

- vision summarization
- web extraction summarization
- context compression summaries
- session-search summaries
- memory flushes

If the provider has no sensible aux default, side tasks may fall back badly or use an expensive main model unexpectedly.

### agent/model_metadata.py​

`agent/model_metadata.py`

Add context lengths for the provider's models so token budgeting, compression thresholds, and limits stay sane.

## Step 7: If the provider is native, add an adapter andrun_agent.pysupport​

`run_agent.py`

If the provider is not plain chat completions, isolate the provider-specific logic inagent/<provider>_adapter.py.

`agent/<provider>_adapter.py`

Keeprun_agent.pyfocused on orchestration. It should call adapter helpers, not hand-build provider payloads inline all over the file.

`run_agent.py`

A native provider usually needs work in these places:

### New adapter file​

Typical responsibilities:

- build the SDK / HTTP client
- resolve tokens
- convert OpenAI-style conversation messages to the provider's request format
- convert tool schemas if needed
- normalize provider responses back into whatrun_agent.pyexpects
- extract usage and finish-reason data

`run_agent.py`

### run_agent.py​

`run_agent.py`

Search forapi_modeand audit every switch point. At minimum, verify:

`api_mode`
- __init__chooses the newapi_mode
- client construction works for the provider
- _build_api_kwargs()knows how to format requests
- _interruptible_api_call()dispatches to the right client call
- interrupt / client rebuild paths work
- response validation accepts the provider's shape
- finish-reason extraction is correct
- token-usage extraction is correct
- fallback-model activation can switch into the new provider cleanly
- summary-generation and memory-flush paths still work

`__init__`
`api_mode`
`_build_api_kwargs()`
`_interruptible_api_call()`

Also searchrun_agent.pyforself.client.. Any code path that assumes the standard OpenAI client exists can break when a native provider uses a different client object orself.client = None.

`run_agent.py`
`self.client.`
`self.client = None`

### Prompt caching and provider-specific request fields​

Prompt caching and provider-specific knobs are easy to regress.

Examples already in-tree:

- Anthropic has a native prompt-caching path
- OpenRouter gets provider-routing fields
- not every provider should receive every request-side option

When you add a native provider, double-check that Hermes is only sending fields that provider actually understands.

## Step 8: Tests​

At minimum, touch the tests that guard provider wiring.

Common places:

- tests/hermes_cli/test_runtime_provider_resolution.py
- tests/cli/test_cli_provider_resolution.py
- tests/hermes_cli/test_model_switch_custom_providers.py(and adjacenttests/hermes_cli/test_model_switch_*.py)
- tests/hermes_cli/test_setup_model_provider.py
- tests/run_agent/test_provider_parity.py
- tests/run_agent/test_run_agent.py
- tests/test_<provider>_adapter.pyfor a native provider

`tests/hermes_cli/test_runtime_provider_resolution.py`
`tests/cli/test_cli_provider_resolution.py`
`tests/hermes_cli/test_model_switch_custom_providers.py`
`tests/hermes_cli/test_model_switch_*.py`
`tests/hermes_cli/test_setup_model_provider.py`
`tests/run_agent/test_provider_parity.py`
`tests/run_agent/test_run_agent.py`
`tests/test_<provider>_adapter.py`

For docs-only examples, the exact file set may differ. The point is to cover:

- auth resolution
- CLI menu / provider selection
- runtime provider resolution
- agent execution path
- provider:modelparsing
- any adapter-specific message conversion

Run tests with xdist disabled:

```
source venv/bin/activatepython -m pytest tests/hermes_cli/test_runtime_provider_resolution.py tests/cli/test_cli_provider_resolution.py tests/hermes_cli/test_setup_model_provider.py tests/run_agent/test_provider_parity.py -n0 -q
```

For deeper changes, run the full suite before pushing:

```
source venv/bin/activatepython -m pytest tests/ -n0 -q
```

## Step 9: Live verification​

After tests, run a real smoke test.

```
source venv/bin/activatepython -m hermes_cli.main chat -q "Say hello" --provider your-provider --model your-model
```

Also test the interactive flows if you changed menus:

```
source venv/bin/activatepython -m hermes_cli.main modelpython -m hermes_cli.main setup
```

For native providers, verify at least one tool call too, not just a plain text response.

## Step 10: Update user-facing docs​

If the provider is meant to ship as a first-class option, update the user docs too:

- website/docs/getting-started/quickstart.md
- website/docs/user-guide/configuration.md
- website/docs/reference/environment-variables.md

`website/docs/getting-started/quickstart.md`
`website/docs/user-guide/configuration.md`
`website/docs/reference/environment-variables.md`

A developer can wire the provider perfectly and still leave users unable to discover the required env vars or setup flow.

## OpenAI-compatible provider checklist​

Use this if the provider is standard chat completions.

- ProviderConfigadded inhermes_cli/auth.py
- aliases added inhermes_cli/auth.pyandhermes_cli/models.py
- model catalog added inhermes_cli/models.py
- runtime branch added inhermes_cli/runtime_provider.py
- CLI wiring added inhermes_cli/main.py(setup.py inherits automatically)
- aux model added inagent/auxiliary_client.py
- context lengths added inagent/model_metadata.py
- runtime / CLI tests updated
- user docs updated

`ProviderConfig`
`hermes_cli/auth.py`
`hermes_cli/auth.py`
`hermes_cli/models.py`
`hermes_cli/models.py`
`hermes_cli/runtime_provider.py`
`hermes_cli/main.py`
`agent/auxiliary_client.py`
`agent/model_metadata.py`

## Native provider checklist​

Use this when the provider needs a new protocol path.

- everything in the OpenAI-compatible checklist
- adapter added inagent/<provider>_adapter.py
- newapi_modesupported inrun_agent.py
- interrupt / rebuild path works
- usage and finish-reason extraction works
- fallback path works
- adapter tests added
- live smoke test passes

`agent/<provider>_adapter.py`
`api_mode`
`run_agent.py`

## Common pitfalls​

### 1. Adding the provider to auth but not to model parsing​

That makes credentials resolve correctly while/modelandprovider:modelinputs fail.

`/model`
`provider:model`

### 2. Forgetting thatconfig["model"]can be a string or a dict​

`config["model"]`

A lot of provider-selection code has to normalize both forms.

### 3. Assuming a built-in provider is required​

If the service is just OpenAI-compatible, a custom provider may already solve the user problem with less maintenance.

### 4. Forgetting auxiliary paths​

The main chat path can work while summarization, memory flushes, or vision helpers fail because aux routing was never updated.

### 5. Native-provider branches hiding inrun_agent.py​

`run_agent.py`

Search forapi_modeandself.client.. Do not assume the obvious request path is the only one.

`api_mode`
`self.client.`

### 6. Sending OpenRouter-only knobs to other providers​

Fields like provider routing belong only on the providers that support them.

### 7. Updatinghermes modelbut nothermes setup​

`hermes model`
`hermes setup`

Both flows need to know about the provider.

## Good search targets while implementing​

If you are hunting for all the places a provider touches, search these symbols:

- PROVIDER_REGISTRY
- _PROVIDER_ALIASES
- _PROVIDER_MODELS
- resolve_runtime_provider
- _model_flow_
- select_provider_and_model
- api_mode
- _API_KEY_PROVIDER_AUX_MODELS
- self.client.

`PROVIDER_REGISTRY`
`_PROVIDER_ALIASES`
`_PROVIDER_MODELS`
`resolve_runtime_provider`
`_model_flow_`
`select_provider_and_model`
`api_mode`
`_API_KEY_PROVIDER_AUX_MODELS`
`self.client.`

## Related docs​

- Provider Runtime Resolution
- Architecture
- Contributing