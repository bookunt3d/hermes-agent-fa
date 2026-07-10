- 
- Developer Guide
- Extending
- Plugins
- Model Provider Plugins

# Building a Model Provider Plugin

Model provider plugins declare an inference backend — an OpenAI-compatible endpoint, an Anthropic Messages server, a Codex-style Responses API, or a Bedrock-native surface — that Hermes can routeAIAgentcalls through. Every built-in provider (OpenRouter, Anthropic, GMI, DeepSeek, Nvidia, …) ships as one of these plugins. Third parties can add their own by dropping a directory under$HERMES_HOME/plugins/model-providers/with zero changes to the repo.

`AIAgent`
`$HERMES_HOME/plugins/model-providers/`

Model provider plugins are the third kind ofprovider plugin. The others areMemory Provider Plugins(cross-session knowledge) andContext Engine Plugins(context compression strategies). All three follow the same "drop a directory, declare a profile, no repo edits" pattern.

## How discovery works​

providers/__init__.py._discover_providers()runs lazily the first time any code callsget_provider_profile()orlist_providers(). Discovery order:

`providers/__init__.py._discover_providers()`
`get_provider_profile()`
`list_providers()`
1. Bundled plugins—<repo>/plugins/model-providers/<name>/— ship with Hermes
2. User plugins—$HERMES_HOME/plugins/model-providers/<name>/— drop in any directory; no restart required for subsequent sessions
3. Legacy single-file—<repo>/providers/<name>.py— back-compat for out-of-tree editable installs

`<repo>/plugins/model-providers/<name>/`
`$HERMES_HOME/plugins/model-providers/<name>/`
`<repo>/providers/<name>.py`

User plugins override bundled plugins of the same namebecauseregister_provider()is last-writer-wins. Drop a$HERMES_HOME/plugins/model-providers/gmi/directory to replace the built-in GMI profile without touching the repo.

`register_provider()`
`$HERMES_HOME/plugins/model-providers/gmi/`

## Directory structure​

```
plugins/model-providers/my-provider/├── __init__.py       # Calls register_provider(profile) at module-level├── plugin.yaml       # kind: model-provider + metadata (optional but recommended)└── README.md         # Setup instructions (optional)
```

The only required file is__init__.py.plugin.yamlis used byhermes pluginsfor introspection and by the general PluginManager to route the plugin to the right loader; without it, the general loader falls back to a source-text heuristic.

`__init__.py`
`plugin.yaml`
`hermes plugins`

## Minimal example — a simple API-key provider​

```
# plugins/model-providers/acme-inference/__init__.pyfrom providers import register_providerfrom providers.base import ProviderProfileacme = ProviderProfile(    name="acme-inference",    aliases=("acme",),    display_name="Acme Inference",    description="Acme — OpenAI-compatible direct API",    signup_url="https://acme.example.com/keys",    env_vars=("ACME_API_KEY", "ACME_BASE_URL"),    base_url="https://api.acme.example.com/v1",    auth_type="api_key",    default_aux_model="acme-small-fast",    fallback_models=(        "acme-large-v3",        "acme-medium-v3",        "acme-small-fast",    ),)register_provider(acme)
```

```
# plugins/model-providers/acme-inference/plugin.yamlname: acme-inferencekind: model-providerversion: 1.0.0description: Acme Inference — OpenAI-compatible direct APIauthor: Your Name
```

That's it. After dropping these two files, the followingauto-wirewith no other edits:

| Integration | Where | What it gets |
| --- | --- | --- |
| Credential resolution | hermes_cli/auth.py | PROVIDER_REGISTRY["acme-inference"]populated from profile |
| --providerCLI flag | hermes_cli/main.py | Acceptsacme-inference |
| hermes modelpicker | hermes_cli/models.py | Appears inCANONICAL_PROVIDERS, model list fetched from{base_url}/models |
| hermes doctor | hermes_cli/doctor.py | Health check forACME_API_KEY+{base_url}/modelsprobe |
| hermes setup | hermes_cli/config.py | ACME_API_KEYappears inOPTIONAL_ENV_VARSand the setup wizard |
| URL reverse-mapping | agent/model_metadata.py | Hostname → provider name for auto-detection |
| Auxiliary model | agent/auxiliary_client.py | Usesdefault_aux_modelfor compression / summarization |
| Runtime resolution | hermes_cli/runtime_provider.py | Returns correctbase_url,api_key,api_mode |
| Transport | agent/transports/chat_completions.py | Profile path generates kwargs viaprepare_messages/build_extra_body/build_api_kwargs_extras |

`hermes_cli/auth.py`
`PROVIDER_REGISTRY["acme-inference"]`
`--provider`
`hermes_cli/main.py`
`acme-inference`
`hermes model`
`hermes_cli/models.py`
`CANONICAL_PROVIDERS`
`{base_url}/models`
`hermes doctor`
`hermes_cli/doctor.py`
`ACME_API_KEY`
`{base_url}/models`
`hermes setup`
`hermes_cli/config.py`
`ACME_API_KEY`
`OPTIONAL_ENV_VARS`
`agent/model_metadata.py`
`agent/auxiliary_client.py`
`default_aux_model`
`hermes_cli/runtime_provider.py`
`base_url`
`api_key`
`api_mode`
`agent/transports/chat_completions.py`
`prepare_messages`
`build_extra_body`
`build_api_kwargs_extras`

## ProviderProfile fields​

Full definition inproviders/base.py. The most useful ones:

`providers/base.py`
| Field | Type | Purpose |
| --- | --- | --- |
| name | str | Canonical id — matchesmodel.providerinconfig.yamland the--providerflag |
| aliases | tuple[str, ...] | Alternative names resolved byget_provider_profile()(e.g.grok→xai) |
| api_mode | str | chat_completions|codex_responses|anthropic_messages|bedrock_converse |
| display_name | str | Human label shown inhermes modelpicker |
| description | str | Picker subtitle |
| signup_url | str | Shown during first-run setup ("get an API key here") |
| env_vars | tuple[str, ...] | API-key env vars in priority order; a final*_BASE_URLentry is used as the user base-URL override |
| base_url | str | Default inference endpoint |
| models_url | str | Explicit catalog URL (falls back to{base_url}/models) |
| auth_type | str | api_key|oauth_device_code|oauth_external|copilot|aws_sdk|external_process |
| fallback_models | tuple[str, ...] | Curated list shown when live catalog fetch fails |
| default_headers | dict[str, str] | Sent on every request (e.g. Copilot'sEditor-Version) |
| fixed_temperature | Any | None= use caller's value;OMIT_TEMPERATUREsentinel = don't send temperature at all (Kimi) |
| default_max_tokens | int | None | Provider-level max_tokens cap (Nvidia: 16384) |
| default_aux_model | str | Cheap model for auxiliary tasks (compression, vision, summarization) |

`name`
`model.provider`
`config.yaml`
`--provider`
`aliases`
`tuple[str, ...]`
`get_provider_profile()`
`grok`
`xai`
`api_mode`
`chat_completions`
`codex_responses`
`anthropic_messages`
`bedrock_converse`
`display_name`
`hermes model`
`description`
`signup_url`
`env_vars`
`tuple[str, ...]`
`*_BASE_URL`
`base_url`
`models_url`
`{base_url}/models`
`auth_type`
`api_key`
`oauth_device_code`
`oauth_external`
`copilot`
`aws_sdk`
`external_process`
`fallback_models`
`tuple[str, ...]`
`default_headers`
`dict[str, str]`
`Editor-Version`
`fixed_temperature`
`None`
`OMIT_TEMPERATURE`
`default_max_tokens`
`int | None`
`default_aux_model`

## Overridable hooks​

SubclassProviderProfilefor non-trivial quirks:

`ProviderProfile`

```
from typing import Anyfrom providers.base import ProviderProfileclass AcmeProfile(ProviderProfile):    def prepare_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:        """Provider-specific message preprocessing. Runs after codex        sanitization, before developer-role swap. Default: pass-through."""        # Example: Qwen normalizes plain-text content to a list-of-parts        # array and injects cache_control; Kimi rewrites tool-call JSON        return messages    def build_extra_body(self, *, session_id=None, **context) -> dict:        """Provider-specific extra_body fields merged into the API call.        Context includes: session_id, provider_preferences, model, base_url,        reasoning_config. Default: empty dict."""        # Example: OpenRouter's provider-preferences block,        # Gemini's thinking_config translation.        return {}    def build_api_kwargs_extras(self, *, reasoning_config=None, **context):        """Returns (extra_body_additions, top_level_kwargs). Needed when some        fields go top-level (Kimi's reasoning_effort, OpenRouter's verbosity for        adaptive Anthropic models) and some go in extra_body (OpenRouter's        reasoning dict). Default: ({}, {})."""        return {}, {}    def fetch_models(self, *, api_key=None, timeout=8.0) -> list[str] | None:        """Live catalog fetch. Default hits {models_url or base_url}/models with        Bearer auth. Override for: custom auth (Anthropic), no REST endpoint        (Bedrock → None), or public/unauthenticated catalogs (OpenRouter)."""        return super().fetch_models(api_key=api_key, timeout=timeout)
```

## Hook reference examples​

Look at these bundled plugins for idioms:

| Plugin | Why look |
| --- | --- |
| plugins/model-providers/openrouter/ | Aggregator with provider preferences, public model catalog |
| plugins/model-providers/gemini/ | thinking_configtranslation (native + OpenAI-compat nested forms) |
| plugins/model-providers/kimi-coding/ | OMIT_TEMPERATURE,extra_body.thinking, top-levelreasoning_effort |
| plugins/model-providers/qwen-oauth/ | Message normalization,cache_controlinjection, VL high-res |
| plugins/model-providers/nous/ | Attribution tags, "omit reasoning when disabled" |
| plugins/model-providers/custom/ | Ollamanum_ctx+think: falsequirks |
| plugins/model-providers/bedrock/ | api_mode="bedrock_converse",fetch_modelsreturns None (no REST endpoint) |

`plugins/model-providers/openrouter/`
`plugins/model-providers/gemini/`
`thinking_config`
`plugins/model-providers/kimi-coding/`
`OMIT_TEMPERATURE`
`extra_body.thinking`
`reasoning_effort`
`plugins/model-providers/qwen-oauth/`
`cache_control`
`plugins/model-providers/nous/`
`plugins/model-providers/custom/`
`num_ctx`
`think: false`
`plugins/model-providers/bedrock/`
`api_mode="bedrock_converse"`
`fetch_models`

## User overrides — replace a built-in without editing the repo​

Say you want to pointgmiat your private staging endpoint for testing. Create~/.hermes/plugins/model-providers/gmi/__init__.py:

`gmi`
`~/.hermes/plugins/model-providers/gmi/__init__.py`

```
from providers import register_providerfrom providers.base import ProviderProfileregister_provider(ProviderProfile(    name="gmi",    aliases=("gmi-cloud", "gmicloud"),    env_vars=("GMI_API_KEY",),    base_url="https://gmi-staging.internal.example.com/v1",    auth_type="api_key",    default_aux_model="google/gemini-3.1-flash-lite-preview",))
```

Next session,get_provider_profile("gmi").base_urlreturns the staging URL. No repo patch, no rebuild. Because user plugins are discovered after bundled ones, the userregister_provider()call wins.

`get_provider_profile("gmi").base_url`
`register_provider()`

## api_mode selection​

Four values are recognized. Hermes picks one based on:

1. User explicit override (config.yamlmodel.api_modewhen set)
2. OpenCode's per-model dispatch (opencode_model_api_modefor Zen and Go)
3. URL auto-detection —/anthropicsuffix →anthropic_messages,api.openai.com→codex_responses,api.x.ai→codex_responses,/codingon Kimi domains →chat_completions
4. Profileapi_modeas a fallback when URL detection finds nothing
5. Defaultchat_completions

`config.yaml`
`model.api_mode`
`opencode_model_api_mode`
`/anthropic`
`anthropic_messages`
`api.openai.com`
`codex_responses`
`api.x.ai`
`codex_responses`
`/coding`
`chat_completions`
`api_mode`
`chat_completions`

Setprofile.api_modeto match the default your provider ships — it acts as a hint. User URL overrides still win.

`profile.api_mode`

## Auth types​

| auth_type | Meaning | Who uses it |
| --- | --- | --- |
| api_key | Single env var carries a static API key | Most providers |
| oauth_device_code | Device-code OAuth flow | — |
| oauth_external | User signs in elsewhere, tokens land inauth.json | Anthropic OAuth, MiniMax OAuth, Qwen Portal, Nous Portal |
| copilot | GitHub Copilot token refresh cycle | copilotplugin only |
| aws_sdk | AWS SDK credential chain (IAM role, profile, env) | bedrockplugin only |
| external_process | Auth handled by a subprocess the agent spawns | copilot-acpplugin only |

`auth_type`
`api_key`
`oauth_device_code`
`oauth_external`
`auth.json`
`copilot`
`copilot`
`aws_sdk`
`bedrock`
`external_process`
`copilot-acp`

auth_typegates which codepaths treat your provider as a "simple api-key provider" — if it's notapi_key, the PluginManager still records the manifest but Hermes' CLI-level automation (doctor checks,--providerflag, setup wizard delegation) may skip over it.

`auth_type`
`api_key`
`--provider`

## Discovery timing​

Provider discovery islazy— triggered by the firstget_provider_profile()orlist_providers()call in the process. In practice this happens early at startup (auth.pymodule load extendsPROVIDER_REGISTRYeagerly). If you need to verify your plugin loaded, run:

`get_provider_profile()`
`list_providers()`
`auth.py`
`PROVIDER_REGISTRY`

```
hermes doctor
```

— a successfulauth_type="api_key"profile appears under the Provider Connectivity section with a/modelsprobe.

`auth_type="api_key"`
`/models`

For programmatic inspection:

```
from providers import list_providersfor p in list_providers():    print(p.name, p.base_url, p.api_mode)
```

## Testing your plugin​

PointHERMES_HOMEat a temp directory so you don't pollute your real config:

`HERMES_HOME`

```
export HERMES_HOME=/tmp/hermes-plugin-testmkdir -p $HERMES_HOME/plugins/model-providers/my-providercat > $HERMES_HOME/plugins/model-providers/my-provider/__init__.py <<'EOF'from providers import register_providerfrom providers.base import ProviderProfileregister_provider(ProviderProfile(    name="my-provider",    env_vars=("MY_API_KEY",),    base_url="https://api.my-provider.example.com/v1",    auth_type="api_key",))EOFexport MY_API_KEY=your-test-keyhermes -z "hello" --provider my-provider -m some-model
```

## General PluginManager integration​

The generalPluginManager(the thinghermes pluginsoperates on)seesmodel-provider plugins but does not import them —providers/__init__.pyowns their lifecycle. The manager records the manifest for introspection and categorizes bykind: model-provider. When you drop an unlabeled user plugin into$HERMES_HOME/plugins/that happens to callregister_providerwith aProviderProfile, the manager auto-coerces it tokind: model-providervia a source-text heuristic — so the plugin still routes correctly even withoutplugin.yaml.

`PluginManager`
`hermes plugins`
`providers/__init__.py`
`kind: model-provider`
`$HERMES_HOME/plugins/`
`register_provider`
`ProviderProfile`
`kind: model-provider`
`plugin.yaml`

## Distribute via pip​

Like any Hermes plugin, model providers can ship as a pip package. Add an entry point to yourpyproject.toml:

`pyproject.toml`

```
[project.entry-points."hermes_agent.plugins"]acme-inference = "acme_hermes_plugin:register"
```

…whereacme_hermes_plugin:registeris a function that callsregister_provider(profile). The general PluginManager picks up entry-point plugins duringdiscover_and_load(). Forkind: model-providerpip plugins, you still need to declare the kind in your manifest (or rely on the source-text heuristic).

`acme_hermes_plugin:register`
`register_provider(profile)`
`discover_and_load()`
`kind: model-provider`

SeeBuilding a Hermes Pluginfor the full entry-points setup.

## Related pages​

- Provider Runtime— resolution precedence + where each layer reads the profile
- Adding Providers— end-to-end checklist for new inference backends (covers both the fast plugin path and the full CLI/auth integration)
- Memory Provider Plugins
- Context Engine Plugins
- Building a Hermes Plugin— general plugin authoring