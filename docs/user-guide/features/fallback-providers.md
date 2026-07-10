---
layout: docs
title: "Features_Fallback Providers"
permalink: /docs/user-guide/features/fallback-providers/
---

- 
- Integrations
- Fallback Providers

# Fallback Providers

Hermes Agent has three layers of resilience that keep your sessions running when providers hit issues:

1. Credential pools— rotate across multiple API keys for thesameprovider (tried first)
2. Primary model fallback— automatically switches to adifferentprovider:modelwhen your main model fails
3. Auxiliary task fallback— independent provider resolution for side tasks like vision, compression, and web extraction

Credential pools handle same-provider rotation (e.g., multiple OpenRouter keys). This page covers cross-provider fallback. Both are optional and work independently.

## Primary Model Fallback​

When your main LLM provider encounters errors — rate limits, server overload, auth failures, connection drops — Hermes can automatically switch to a backup provider:modelpair mid-session without losing your conversation.

### Configuration​

The easiest path is the interactive manager:

```
hermes fallback
```

hermes fallbackreuses the provider picker fromhermes model— same provider list, same credential prompts, same validation. Use the subcommandsadd,list(aliasls),remove(aliasrm), andclearto manage the chain. Changes persist under the top-levelfallback_providers:list inconfig.yaml.

`hermes fallback`
`hermes model`
`add`
`list`
`ls`
`remove`
`rm`
`clear`
`fallback_providers:`
`config.yaml`

If you'd rather edit the YAML directly, add a top-levelfallback_providerslist to~/.hermes/config.yaml:

`fallback_providers`
`~/.hermes/config.yaml`

```
fallback_providers:  - provider: openrouter    model: anthropic/claude-sonnet-4
```

Each entry requires bothproviderandmodel. Entries missing either field are ignored.

`provider`
`model`
`fallback_model`
`fallback_providers`

fallback_providers(plural, list) is the current config shape and supports multiple fallbacks tried in order.fallback_model(singular) is the legacy single-fallback key — Hermes still honors it for back-compat, buthermes fallbackwrites the currentfallback_providerskey and migrates legacy config on write. When both are set,fallback_providerstakes priority.

`fallback_providers`
`fallback_model`
`hermes fallback`
`fallback_providers`
`fallback_providers`

### Supported Providers​

| Provider | Value | Requirements |
| --- | --- | --- |
| OpenRouter | openrouter | OPENROUTER_API_KEY |
| Nous Portal | nous | hermes setup --portal(fresh) orhermes auth add nous(OAuth) |
| OpenAI Codex | openai-codex | hermes model(ChatGPT OAuth) |
| GitHub Copilot | copilot | COPILOT_GITHUB_TOKEN,GH_TOKEN, orGITHUB_TOKEN |
| GitHub Copilot ACP | copilot-acp | External process (editor integration) |
| Anthropic | anthropic | ANTHROPIC_API_KEYor Claude Code credentials |
| z.ai / GLM | zai | GLM_API_KEY |
| Kimi / Moonshot | kimi-coding | KIMI_API_KEY |
| MiniMax | minimax | MINIMAX_API_KEY |
| MiniMax (China) | minimax-cn | MINIMAX_CN_API_KEY |
| DeepSeek | deepseek | DEEPSEEK_API_KEY |
| NVIDIA NIM | nvidia | NVIDIA_API_KEY(optional:NVIDIA_BASE_URL) |
| GMI Cloud | gmi | GMI_API_KEY(optional:GMI_BASE_URL) |
| StepFun | stepfun | STEPFUN_API_KEY(optional:STEPFUN_BASE_URL) |
| Ollama Cloud | ollama-cloud | OLLAMA_API_KEY |
| Google AI Studio | gemini | GOOGLE_API_KEY(alias:GEMINI_API_KEY) |
| xAI (Grok) | xai(aliasgrok) | XAI_API_KEY(optional:XAI_BASE_URL) |
| xAI Grok OAuth (SuperGrok) | xai-oauth(aliasgrok-oauth) | hermes model→ xAI Grok OAuth (browser login; SuperGrok subscription) |
| AWS Bedrock | bedrock | Standard boto3 auth (AWS_REGION+AWS_PROFILEorAWS_ACCESS_KEY_ID) |
| Qwen Portal (OAuth) | qwen-oauth | hermes model(Qwen Portal OAuth; optional:HERMES_QWEN_BASE_URL) |
| MiniMax (OAuth) | minimax-oauth | hermes model(MiniMax portal OAuth) |
| OpenCode Zen | opencode-zen | OPENCODE_ZEN_API_KEY |
| OpenCode Go | opencode-go | OPENCODE_GO_API_KEY |
| Kilo Code | kilocode | KILOCODE_API_KEY |
| Xiaomi MiMo | xiaomi | XIAOMI_API_KEY |
| Arcee AI | arcee | ARCEEAI_API_KEY |
| GMI Cloud | gmi | GMI_API_KEY |
| Alibaba / DashScope | alibaba | DASHSCOPE_API_KEY |
| Alibaba Coding Plan | alibaba-coding-plan | ALIBABA_CODING_PLAN_API_KEY(falls back toDASHSCOPE_API_KEY) |
| Kimi / Moonshot (China) | kimi-coding-cn | KIMI_CN_API_KEY |
| StepFun | stepfun | STEPFUN_API_KEY |
| Tencent TokenHub | tencent-tokenhub | TOKENHUB_API_KEY |
| Microsoft Foundry | azure-foundry | AZURE_FOUNDRY_API_KEY+AZURE_FOUNDRY_BASE_URL |
| LM Studio (local) | lmstudio | LM_API_KEY(or none for local) +LM_BASE_URL |
| Hugging Face | huggingface | HF_TOKEN |
| Custom endpoint | custom | base_url+key_env(see below) |

`openrouter`
`OPENROUTER_API_KEY`
`nous`
`hermes setup --portal`
`hermes auth add nous`
`openai-codex`
`hermes model`
`copilot`
`COPILOT_GITHUB_TOKEN`
`GH_TOKEN`
`GITHUB_TOKEN`
`copilot-acp`
`anthropic`
`ANTHROPIC_API_KEY`
`zai`
`GLM_API_KEY`
`kimi-coding`
`KIMI_API_KEY`
`minimax`
`MINIMAX_API_KEY`
`minimax-cn`
`MINIMAX_CN_API_KEY`
`deepseek`
`DEEPSEEK_API_KEY`
`nvidia`
`NVIDIA_API_KEY`
`NVIDIA_BASE_URL`
`gmi`
`GMI_API_KEY`
`GMI_BASE_URL`
`stepfun`
`STEPFUN_API_KEY`
`STEPFUN_BASE_URL`
`ollama-cloud`
`OLLAMA_API_KEY`
`gemini`
`GOOGLE_API_KEY`
`GEMINI_API_KEY`
`xai`
`grok`
`XAI_API_KEY`
`XAI_BASE_URL`
`xai-oauth`
`grok-oauth`
`hermes model`
`bedrock`
`AWS_REGION`
`AWS_PROFILE`
`AWS_ACCESS_KEY_ID`
`qwen-oauth`
`hermes model`
`HERMES_QWEN_BASE_URL`
`minimax-oauth`
`hermes model`
`opencode-zen`
`OPENCODE_ZEN_API_KEY`
`opencode-go`
`OPENCODE_GO_API_KEY`
`kilocode`
`KILOCODE_API_KEY`
`xiaomi`
`XIAOMI_API_KEY`
`arcee`
`ARCEEAI_API_KEY`
`gmi`
`GMI_API_KEY`
`alibaba`
`DASHSCOPE_API_KEY`
`alibaba-coding-plan`
`ALIBABA_CODING_PLAN_API_KEY`
`DASHSCOPE_API_KEY`
`kimi-coding-cn`
`KIMI_CN_API_KEY`
`stepfun`
`STEPFUN_API_KEY`
`tencent-tokenhub`
`TOKENHUB_API_KEY`
`azure-foundry`
`AZURE_FOUNDRY_API_KEY`
`AZURE_FOUNDRY_BASE_URL`
`lmstudio`
`LM_API_KEY`
`LM_BASE_URL`
`huggingface`
`HF_TOKEN`
`custom`
`base_url`
`key_env`

### Custom Endpoint Fallback​

For a custom OpenAI-compatible endpoint, addbase_urland optionallykey_env:

`base_url`
`key_env`

```
fallback_providers:  - provider: custom    model: my-local-model    base_url: http://localhost:8000/v1    key_env: MY_LOCAL_KEY            # env var name containing the API key
```

### When Fallback Triggers​

The fallback activates automatically when the primary model fails with:

- Rate limits(HTTP 429) — after exhausting retry attempts
- Server errors(HTTP 500, 502, 503) — after exhausting retry attempts
- Auth failures(HTTP 401, 403) — immediately (no point retrying)
- Not found(HTTP 404) — immediately
- Invalid responses— when the API returns malformed or empty responses repeatedly

When triggered, Hermes:

1. Resolves credentials for the fallback provider
2. Builds a new API client
3. Swaps the model, provider, and client in-place
4. Resets the retry counter and continues the conversation

The switch is seamless — your conversation history, tool calls, and context are preserved. The agent continues from exactly where it left off, just using a different model.

Prompt caches are keyed to the model (and on most providers, the account) serving the request. When fallback fires, the new provider:modelhas no cached prefix for your conversation, so the next request re-reads the entire history at full input-token price instead of the ~75–90% discounted cached rate. The same applies when the turn ends and the primary is restored — that first request back on the primary is a full re-read too (unless the primary's cache TTL hasn't expired). This is unavoidable — it's the cost of staying alive through an outage — but it's why a long session that bounces between providers can cost noticeably more than one that stays put.

Fallback isturn-scoped: each new user message starts with the primary model restored. If the primary fails mid-turn, fallback activates for that turn only. On the next message, Hermes tries the primary again. Within a single turn, fallback activates at most once — if the fallback also fails, normal error handling takes over (retries, then error message). This prevents cascading failover loops within a turn while giving the primary model a fresh chance every turn.

### Examples​

OpenRouter as fallback for Anthropic native:

```
model:  provider: anthropic  default: claude-sonnet-4-6fallback_providers:  - provider: openrouter    model: anthropic/claude-sonnet-4
```

Nous Portal as fallback for OpenRouter:

```
model:  provider: openrouter  default: anthropic/claude-opus-4fallback_providers:  - provider: nous    model: nous-hermes-3
```

Local model as fallback for cloud:

```
fallback_providers:  - provider: custom    model: llama-3.1-70b    base_url: http://localhost:8000/v1    key_env: LOCAL_API_KEY
```

Codex OAuth as fallback:

```
fallback_providers:  - provider: openai-codex    model: gpt-5.3-codex
```

### Where Fallback Works​

| Context | Fallback Supported |
| --- | --- |
| CLI sessions | ✔ |
| Messaging gateway (Telegram, Discord, etc.) | ✔ |
| Subagent delegation | ✔ (subagents inherit the parent fallback chain) |
| Cron jobs | ✔ (cron agents inherit configured fallback providers) |
| Auxiliary tasks onprovider: auto | ✔ (try per-task fallback, then the main fallback chain before built-in aux discovery) |

`provider: auto`

There are no environment variables for the primary fallback chain — configure it exclusively throughconfig.yamlorhermes fallback. This is intentional: fallback configuration is a deliberate choice, not something a stale shell export should override.

`config.yaml`
`hermes fallback`

## Auxiliary Task Fallback​

Hermes uses separate lightweight models for side tasks. Each task has its own provider resolution chain that acts as a built-in fallback system.

### Tasks with Independent Provider Resolution​

| Task | What It Does | Config Key |
| --- | --- | --- |
| Vision | Image analysis, browser screenshots | auxiliary.vision |
| Web Extract | Web page summarization | auxiliary.web_extract |
| Compression | Context compression summaries | auxiliary.compression |
| Skills Hub | Skill search and discovery | auxiliary.skills_hub |
| MCP | MCP helper operations | auxiliary.mcp |
| Approval | Smart command-approval classification | auxiliary.approval |
| Title Generation | Session title summaries | auxiliary.title_generation |
| Triage Specifier | hermes kanban specify/ dashboard ✨ button — fleshes out a one-liner triage task into a real spec | auxiliary.triage_specifier |

`auxiliary.vision`
`auxiliary.web_extract`
`auxiliary.compression`
`auxiliary.skills_hub`
`auxiliary.mcp`
`auxiliary.approval`
`auxiliary.title_generation`
`hermes kanban specify`
`auxiliary.triage_specifier`

### Auto-Detection Chain​

When a task's provider is set to"auto"(the default), Hermes first tries the main provider + main model for that auxiliary task. If that route is unavailable or later fails with a capacity-style error, Hermes now honors user-configured fallback policy before using the built-in discovery chain:

`"auto"`

```
Main provider + main model → auxiliary.<task>.fallback_chain →fallback_providers / fallback_model → built-in auxiliary discovery chain
```

The task-specific chain is most precise and wins when present. The top-levelfallback_providerschain is the same policy the main agent uses, so free-only or same-provider fallback rules apply to auxiliary tasks onautoas well.

`fallback_providers`
`auto`

Built-in text discovery chain (compression, web extract, title generation, etc.):

```
OpenRouter → Nous Portal → Custom endpoint → Codex OAuth →API-key providers (z.ai, Kimi, MiniMax, Xiaomi MiMo, Hugging Face, Anthropic) → give up
```

Built-in vision discovery chain:

```
Main provider (if vision-capable) → OpenRouter → Nous Portal →Codex OAuth → Anthropic → Custom endpoint → give up
```

Those built-in chains are a convenience fallback for users who have not declared a task-specific or main fallback policy.

### Configuring Auxiliary Providers​

Each task can be configured independently inconfig.yaml:

`config.yaml`

```
auxiliary:  vision:    provider: "auto"              # auto | openrouter | nous | codex | main | anthropic    model: ""                     # e.g. "openai/gpt-4o"    base_url: ""                  # direct endpoint (takes precedence over provider)    api_key: ""                   # API key for base_url  web_extract:    provider: "auto"    model: ""  compression:    provider: "auto"    model: ""    fallback_chain:              # optional, task-specific fallback policy      - provider: openrouter        model: inclusionai/ring-2.6-1t:free  skills_hub:    provider: "auto"    model: ""  mcp:    provider: "auto"    model: ""
```

Every task above follows the sameprovider / model / base_urlpattern. Each task can also declare its ownfallback_chain; if omitted,provider: autouses the top-levelfallback_providerschain before Hermes' built-in auxiliary discovery chain.

`fallback_chain`
`provider: auto`
`fallback_providers`

Context compression is configured underauxiliary.compression:

`auxiliary.compression`

```
auxiliary:  compression:    provider: main                                    # Same provider options as other auxiliary tasks    model: google/gemini-3-flash-preview    base_url: null                                    # Custom OpenAI-compatible endpoint
```

And the primary fallback chain uses:

```
fallback_providers:  - provider: openrouter    model: anthropic/claude-sonnet-4    # base_url: http://localhost:8000/v1             # Optional custom endpoint
```

All three — auxiliary, compression, fallback — work the same way: setproviderto pick who handles the request,modelto pick which model, andbase_urlto point at a custom endpoint (overrides provider).

`provider`
`model`
`base_url`

### Provider Options for Auxiliary Tasks​

These options apply toauxiliary:,compression:, andfallback_providers:entries only —"main"isnota valid value for your top-levelmodel.provider. For custom endpoints, useprovider: customin yourmodel:section (seeAI Providers).

`auxiliary:`
`compression:`
`fallback_providers:`
`"main"`
`model.provider`
`provider: custom`
`model:`
| Provider | Description | Requirements |
| --- | --- | --- |
| "auto" | Try providers in order until one works (default) | At least one provider configured |
| "openrouter" | Force OpenRouter | OPENROUTER_API_KEY |
| "nous" | Force Nous Portal | hermes auth |
| "codex" | Force Codex OAuth | hermes model→ Codex |
| "main" | Use whatever provider the main agent uses (auxiliary tasks only) | Active main provider configured |
| "anthropic" | Force Anthropic native | ANTHROPIC_API_KEYor Claude Code credentials |

`"auto"`
`"openrouter"`
`OPENROUTER_API_KEY`
`"nous"`
`hermes auth`
`"codex"`
`hermes model`
`"main"`
`"anthropic"`
`ANTHROPIC_API_KEY`

### Direct Endpoint Override​

For any auxiliary task, settingbase_urlbypasses provider resolution entirely and sends requests directly to that endpoint:

`base_url`

```
auxiliary:  vision:    base_url: "http://localhost:1234/v1"    api_key: "local-key"    model: "qwen2.5-vl"
```

base_urltakes precedence overprovider. Hermes uses the configuredapi_keyfor authentication, falling back toOPENAI_API_KEYif not set. It doesnotreuseOPENROUTER_API_KEYfor custom endpoints.

`base_url`
`provider`
`api_key`
`OPENAI_API_KEY`
`OPENROUTER_API_KEY`

## Auxiliary Capacity-Error Fallback​

When you set an explicit auxiliary provider (e.g.auxiliary.vision.provider: glm), Hermes treats that as your preferred choice — but if the provider literally cannot serve the request because of acapacity error(HTTP 402 payment required, HTTP 429 daily-quota exhaustion, connection failure), Hermes falls back through a layered chain instead of failing silently:

`auxiliary.vision.provider: glm`
1. Primary aux provider— the one you configured (tried first, always)
2. auxiliary.<task>.fallback_chain— your per-task override list, if you wrote one
3. Main agent provider + model— last-resort safety net (always tried, even if you didn't write a chain)
4. Warn + re-raise— if every layer fails, Hermes logsAuxiliary <task>: ... all fallbacks exhaustedat WARNING level and re-raises the original error

`auxiliary.<task>.fallback_chain`
`Auxiliary <task>: ... all fallbacks exhausted`

Transient HTTP 429 rate limits (Retry-After: ...) are treated as request constraints, not capacity problems — they respect your explicit provider choice and donottrigger the fallback ladder. Only daily/monthly quota exhaustion, payment errors, and connection failures bypass the explicit-provider gate.

`Retry-After: ...`

For users onprovider: auto(no explicit aux provider), the existing auto-detection chain runs in place of steps 2–3. Its first step is already the main agent model, soautousers get the same outcome with zero config.

`provider: auto`
`auto`

### Optional: per-task fallback chain​

If you want a different fallback ordering than "main agent model first", configurefallback_chainexplicitly. Each entry needs at leastprovider;model,base_url, andapi_keyare optional.

`fallback_chain`
`provider`
`model`
`base_url`
`api_key`

```
auxiliary:  vision:    provider: glm    model: glm-4v-flash    fallback_chain:      - provider: openrouter        model: google/gemini-3-flash-preview      - provider: nous        model: anthropic/claude-sonnet-4  compression:    provider: openrouter    fallback_chain:      - provider: openai        model: gpt-4o-mini
```

You donotneed to configurefallback_chainto get fallback — the main-agent safety net runs regardless. Use it only when you specifically want a different order than the default.

`fallback_chain`

### Provider quota errors that trigger fallback​

Hermes recognizes these as capacity-equivalent to 402 credit exhaustion (not transient rate limits):

- Bedrock / LiteLLM:Too many tokens per day,daily limit,tokens per day
- Vertex AI / GCP:quota exceeded,resource exhausted,RESOURCE_EXHAUSTED
- Generic:daily quota,quota_exceeded

`Too many tokens per day`
`daily limit`
`tokens per day`
`quota exceeded`
`resource exhausted`
`RESOURCE_EXHAUSTED`
`daily quota`
`quota_exceeded`

If your provider returns a different phrase for daily-quota exhaustion and Hermes doesn't trigger fallback, that's a bug — open an issue with the exact error string.

## Context Compression Fallback​

Context compression uses theauxiliary.compressionconfig block to control which model and provider handles summarization:

`auxiliary.compression`

```
auxiliary:  compression:    provider: "auto"                              # auto | openrouter | nous | main    model: "google/gemini-3-flash-preview"
```

Older configs withcompression.summary_model/compression.summary_provider/compression.summary_base_urlare automatically migrated toauxiliary.compression.*on first load (config version 17).

`compression.summary_model`
`compression.summary_provider`
`compression.summary_base_url`
`auxiliary.compression.*`

If no provider is available for compression, Hermes drops middle conversation turns without generating a summary rather than failing the session.

## Delegation Provider Override​

Subagents spawned bydelegate_taskinherit the parent agent's primary fallback chain. You can still route subagents to a different primary provider:modelpair for cost optimization:

`delegate_task`

```
delegation:  provider: "openrouter"                      # override provider for all subagents  model: "google/gemini-3-flash-preview"      # override model  # base_url: "http://localhost:1234/v1"      # or use a direct endpoint  # api_key: "local-key"
```

SeeSubagent Delegationfor full configuration details.

## Cron Job Providers​

Cron jobs inherit your configuredfallback_providerschain (or legacyfallback_model) when they create an agent. To use a different primary provider for a cron job, configureproviderandmodeloverrides on the cron job itself:

`fallback_providers`
`fallback_model`
`provider`
`model`

```
cronjob(    action="create",    schedule="every 2h",    prompt="Check server status",    provider="openrouter",    model="google/gemini-3-flash-preview")
```

SeeScheduled Tasks (Cron)for full configuration details.

## Summary​

| Feature | Fallback Mechanism | Config Location |
| --- | --- | --- |
| Main agent model | fallback_providersin config.yaml — per-turn failover on errors (primary restored each turn) | fallback_providers:(top-level list) |
| Auxiliary tasks (any) — auto users | Full auto-detection chain (main agent model first, then provider chain) on capacity errors | auxiliary.<task>.provider: auto |
| Auxiliary tasks (any) — explicit provider | fallback_chain(if set) → main agent model → warn + raise, on capacity errors only | auxiliary.<task>.fallback_chain |
| Vision | Layered (see above) + internal OpenRouter retry | auxiliary.vision |
| Web extraction | Layered (see above) + internal OpenRouter retry | auxiliary.web_extract |
| Context compression | Layered (see above); degrades to no-summary if all layers unavailable | auxiliary.compression |
| Skills hub | Layered (see above) | auxiliary.skills_hub |
| MCP helpers | Layered (see above) | auxiliary.mcp |
| Approval classification | Layered (see above) | auxiliary.approval |
| Title generation | Layered (see above) | auxiliary.title_generation |
| Triage specifier | Layered (see above) | auxiliary.triage_specifier |
| Delegation | Provider override only (no automatic fallback) | delegation.provider/delegation.model |
| Cron jobs | Per-job provider override only (no automatic fallback) | Per-jobprovider/model |

`fallback_providers`
`fallback_providers:`
`auxiliary.<task>.provider: auto`
`fallback_chain`
`auxiliary.<task>.fallback_chain`
`auxiliary.vision`
`auxiliary.web_extract`
`auxiliary.compression`
`auxiliary.skills_hub`
`auxiliary.mcp`
`auxiliary.approval`
`auxiliary.title_generation`
`auxiliary.triage_specifier`
`delegation.provider`
`delegation.model`
`provider`
`model`