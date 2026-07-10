- 
- Integrations
- AI Providers

# AI Providers

This page covers setting up inference providers for Hermes Agent — from cloud APIs like OpenRouter and Anthropic, to self-hosted endpoints like Ollama and vLLM, to advanced routing and fallback configurations. You need at least one provider configured to use Hermes.

## Inference Providers​

You need at least one way to connect to an LLM. Usehermes modelto switch providers and models interactively, or configure directly:

`hermes model`
| Provider | Setup |
| --- | --- |
| Nous Portal | hermes model(OAuth, subscription-based) |
| OpenAI Codex | hermes model(ChatGPT OAuth, uses Codex models) |
| GitHub Copilot | hermes model(OAuth device code flow,COPILOT_GITHUB_TOKEN,GH_TOKEN, orgh auth token) |
| GitHub Copilot ACP | hermes model(spawns localcopilot --acp --stdio) |
| Anthropic | hermes model(Claude Max + extra usage credits via OAuth; also supports Anthropic API key or manual setup-token — see note below) |
| OpenRouter | OPENROUTER_API_KEYin~/.hermes/.env |
| NovitaAI | NOVITA_API_KEYin~/.hermes/.env(provider:novita, 200+ models, Model API, Agent Sandbox, GPU Cloud) |
| z.ai / GLM | GLM_API_KEYin~/.hermes/.env(provider:zai) |
| Kimi / Moonshot | KIMI_API_KEYin~/.hermes/.env(provider:kimi-coding) |
| Kimi / Moonshot (China) | KIMI_CN_API_KEYin~/.hermes/.env(provider:kimi-coding-cn; aliases:kimi-cn,moonshot-cn) |
| Arcee AI | ARCEEAI_API_KEYin~/.hermes/.env(provider:arcee; aliases:arcee-ai,arceeai) |
| GMI Cloud | GMI_API_KEYin~/.hermes/.env(provider:gmi; aliases:gmi-cloud,gmicloud) |
| MiniMax | MINIMAX_API_KEYin~/.hermes/.env(provider:minimax) |
| MiniMax China | MINIMAX_CN_API_KEYin~/.hermes/.env(provider:minimax-cn) |
| xAI (Grok) — Responses API | XAI_API_KEYin~/.hermes/.env(provider:xai) |
| xAI Grok OAuth (SuperGrok) | hermes model→ "xAI Grok OAuth (SuperGrok / Premium+)" — browser login, no API key. Seeguide |
| Qwen Cloud (Alibaba DashScope) | DASHSCOPE_API_KEYin~/.hermes/.env(provider:alibaba) |
| Alibaba Cloud (Coding Plan) | DASHSCOPE_API_KEY(provider:alibaba-coding-plan, alias:alibaba_coding) — separate billing SKU, different endpoint |
| Kilo Code | KILOCODE_API_KEYin~/.hermes/.env(provider:kilocode) |
| Xiaomi MiMo | XIAOMI_API_KEYin~/.hermes/.env(provider:xiaomi, aliases:mimo,xiaomi-mimo) |
| Tencent TokenHub | TOKENHUB_API_KEYin~/.hermes/.env(provider:tencent-tokenhub, aliases:tencent,tokenhub,tencentmaas) |
| OpenCode Zen | OPENCODE_ZEN_API_KEYin~/.hermes/.env(provider:opencode-zen) |
| OpenCode Go | OPENCODE_GO_API_KEYin~/.hermes/.env(provider:opencode-go) |
| DeepSeek | DEEPSEEK_API_KEYin~/.hermes/.env(provider:deepseek) |
| Hugging Face | HF_TOKENin~/.hermes/.env(provider:huggingface, aliases:hf) |
| Google / Gemini | GOOGLE_API_KEY(orGEMINI_API_KEY) in~/.hermes/.env(provider:gemini) |
| Google Vertex AI | hermes model→ "Google Vertex AI" (provider:vertex; OAuth2 via service-account JSON or ADC, GCP billing) |
| OpenAI API (direct) | OPENAI_API_KEYin~/.hermes/.env(provider:openai-api, optionalOPENAI_BASE_URL) |
| Azure AI Foundry | hermes model→ "Azure AI Foundry" (provider:azure-foundry; uses Azure OpenAI / Foundry endpoint and key) |
| AWS Bedrock | hermes model→ "AWS Bedrock" (provider:bedrock; standard AWS credentials chain via boto3) |
| NVIDIA Build | NVIDIA_API_KEYin~/.hermes/.env(provider:nvidia; NIM-hosted models on build.nvidia.com) |
| Ollama Cloud | hermes model→ "Ollama Cloud" (provider:ollama-cloud; cloud-hosted Ollama API) |
| Qwen OAuth | hermes model→ "Qwen OAuth" (provider:qwen-oauth; browser PKCE login) |
| MiniMax OAuth | hermes model→ "MiniMax (OAuth)" (provider:minimax-oauth; browser PKCE login) |
| StepFun | STEPFUN_API_KEYin~/.hermes/.env(provider:stepfun) |
| LM Studio | hermes model→ "LM Studio" (provider:lmstudio, optionalLM_API_KEY) |
| Custom Endpoint | hermes model→ choose "Custom endpoint" (saved inconfig.yaml) |

`hermes model`
`hermes model`
`hermes model`
`COPILOT_GITHUB_TOKEN`
`GH_TOKEN`
`gh auth token`
`hermes model`
`copilot --acp --stdio`
`hermes model`
`OPENROUTER_API_KEY`
`~/.hermes/.env`
`NOVITA_API_KEY`
`~/.hermes/.env`
`novita`
`GLM_API_KEY`
`~/.hermes/.env`
`zai`
`KIMI_API_KEY`
`~/.hermes/.env`
`kimi-coding`
`KIMI_CN_API_KEY`
`~/.hermes/.env`
`kimi-coding-cn`
`kimi-cn`
`moonshot-cn`
`ARCEEAI_API_KEY`
`~/.hermes/.env`
`arcee`
`arcee-ai`
`arceeai`
`GMI_API_KEY`
`~/.hermes/.env`
`gmi`
`gmi-cloud`
`gmicloud`
`MINIMAX_API_KEY`
`~/.hermes/.env`
`minimax`
`MINIMAX_CN_API_KEY`
`~/.hermes/.env`
`minimax-cn`
`XAI_API_KEY`
`~/.hermes/.env`
`xai`
`hermes model`
`DASHSCOPE_API_KEY`
`~/.hermes/.env`
`alibaba`
`DASHSCOPE_API_KEY`
`alibaba-coding-plan`
`alibaba_coding`
`KILOCODE_API_KEY`
`~/.hermes/.env`
`kilocode`
`XIAOMI_API_KEY`
`~/.hermes/.env`
`xiaomi`
`mimo`
`xiaomi-mimo`
`TOKENHUB_API_KEY`
`~/.hermes/.env`
`tencent-tokenhub`
`tencent`
`tokenhub`
`tencentmaas`
`OPENCODE_ZEN_API_KEY`
`~/.hermes/.env`
`opencode-zen`
`OPENCODE_GO_API_KEY`
`~/.hermes/.env`
`opencode-go`
`DEEPSEEK_API_KEY`
`~/.hermes/.env`
`deepseek`
`HF_TOKEN`
`~/.hermes/.env`
`huggingface`
`hf`
`GOOGLE_API_KEY`
`GEMINI_API_KEY`
`~/.hermes/.env`
`gemini`
`hermes model`
`vertex`
`OPENAI_API_KEY`
`~/.hermes/.env`
`openai-api`
`OPENAI_BASE_URL`
`hermes model`
`azure-foundry`
`hermes model`
`bedrock`
`NVIDIA_API_KEY`
`~/.hermes/.env`
`nvidia`
`hermes model`
`ollama-cloud`
`hermes model`
`qwen-oauth`
`hermes model`
`minimax-oauth`
`STEPFUN_API_KEY`
`~/.hermes/.env`
`stepfun`
`hermes model`
`lmstudio`
`LM_API_KEY`
`hermes model`
`config.yaml`

For the official API-key path, see the dedicatedGoogle Gemini guide.

In themodel:config section, you can use eitherdefault:ormodel:as the key name for your model ID. Bothmodel: { default: my-model }andmodel: { model: my-model }work identically.

`model:`
`default:`
`model:`
`model: { default: my-model }`
`model: { model: my-model }`

### Nous Portal​

Nous Portalis Nous Research's unified subscription gateway andthe recommended way to run Hermes Agent. One OAuth login covers 300+ frontier agentic models (Claude, GPT, Gemini, DeepSeek, Qwen, Kimi, GLM, MiniMax, Grok, ...) plus theTool Gateway(web search, image generation, TTS, browser automation) plusNous Chat— billed against your Nous subscription instead of separate per-provider accounts.

```
hermes setup --portal     # fresh install — OAuth + provider + gateway in one commandhermes model              # existing install — pick "Nous Portal" from the listhermes portal info        # inspect login + routing at any time
```

Don't have a subscription yet? Get one atportal.nousresearch.com/manage-subscription.

For full details:see the dedicatedNous Portal integration page(what's in the subscription, model catalog, troubleshooting) and the step-by-stepRun Hermes Agent with Nous Portal guide.

Client identification.Every Portal request from Hermes Agent carries aclient=hermes-client-v<version>tag (e.g.client=hermes-client-v0.13.0) auto-aligned to your installed release. This is sent on all Portal pathways — main chat loop, auxiliary calls, compression summarizer, web extraction — and lets Portal-side telemetry distinguish Hermes traffic from other clients. No config required; the tag updates automatically when youhermes update.

`client=hermes-client-v<version>`
`client=hermes-client-v0.13.0`
`hermes update`

JWT auth (automatic).Hermes prefers scopedinference:invokeJWTs for Portal requests with the legacy opaque session-key path as a fallback. No configuration is required — credentials are managed by the OAuth flow and rotate transparently. Revoked refresh tokens are quarantined to avoid replay loops.

`inference:invoke`

The OpenAI Codex provider authenticates via device code (open a URL, enter a code). Hermes stores the resulting credentials in its own auth store under~/.hermes/auth.jsonand can import existing Codex CLI credentials from~/.codex/auth.jsonwhen present. No Codex CLI installation is required.

`~/.hermes/auth.json`
`~/.codex/auth.json`

If a token refresh fails with a terminal error (HTTP 4xx,invalid_grant, revoked grant, etc.), Hermes marks the refresh token as dead and stops replaying it so you don't see a flood of identical auth failures. The next request surfaces a typed re-auth message instead. Runhermes auth add codex-oauth(orhermes model→ OpenAI Codex) to start a fresh device-code login; the quarantine clears on the next successful exchange.

`invalid_grant`
`hermes auth add codex-oauth`
`hermes model`

Even when using Nous Portal, Codex, or a custom endpoint, some tools (vision, web summarization, MoA) use a separate "auxiliary" model. By default (auxiliary.*.provider: "auto"), Hermes routes these tasks to yourmain chat model— the same model you picked inhermes model. You can override each task individually to route it to a cheaper/faster model (e.g. Gemini Flash on OpenRouter) — seeAuxiliary Models.

`auxiliary.*.provider: "auto"`
`hermes model`

Paid Nous Portal subscribers also get access to theTool Gateway— web search, image generation, TTS, and browser automation routed through your subscription. No extra API keys needed. On a fresh install,hermes setup --portallogs you in, sets Nous as your provider, and turns the gateway on in one command. Existing users can enable it fromhermes modelor per-tool fromhermes tools. Inspect routing at any time withhermes portal info.

`hermes setup --portal`
`hermes model`
`hermes tools`
`hermes portal info`

### Two Commands for Model Management​

Hermes hastwomodel commands that serve different purposes:

| Command | Where to run | What it does |
| --- | --- | --- |
| hermes model | Your terminal (outside any session) | Full setup wizard — add providers, run OAuth, enter API keys, configure endpoints |
| /model | Inside a Hermes chat session | Quick switch betweenalready-configuredproviders and models |

`hermes model`
`/model`

If you're trying to switch to a provider you haven't set up yet (e.g. you only have OpenRouter configured and want to use Anthropic), you needhermes model, not/model. Exit your session first (Ctrl+Cor/quit), runhermes model, complete the provider setup, then start a new session.

`hermes model`
`/model`
`Ctrl+C`
`/quit`
`hermes model`

### Anthropic (Native)​

Use Claude models directly through the Anthropic API — no OpenRouter proxy needed. Supports three auth methods:

When you authenticate viahermes model→ Anthropic OAuth (or viahermes auth add anthropic --type oauth), Hermes routes as Claude Code against your Anthropic account.It only works if you're on a Claude Max plan and have purchased extra usage credits.The base Max plan allowance (the usage included in Claude Code by default) is not consumed by Hermes — only the extra/overage credits you've added on top are. Claude Pro subscribers cannot use this path.

`hermes model`
`hermes auth add anthropic --type oauth`

If you don't have Max + extra credits, use anANTHROPIC_API_KEYinstead — requests are billed pay-per-token against that key's organization (standard API pricing, independent of any Claude subscription).

`ANTHROPIC_API_KEY`

```
# With an API key (pay-per-token)export ANTHROPIC_API_KEY=***hermes chat --provider anthropic --model claude-sonnet-4-6# Preferred: authenticate through `hermes model`# Hermes will use Claude Code's credential store directly when availablehermes model# Manual override with a setup-token (fallback / legacy)export ANTHROPIC_TOKEN=***  # setup-token or manual OAuth tokenhermes chat --provider anthropic# Auto-detect Claude Code credentials (if you already use Claude Code)hermes chat --provider anthropic  # reads Claude Code credential files automatically
```

When you choose Anthropic OAuth throughhermes model, Hermes prefers Claude Code's own credential store over copying the token into~/.hermes/.env. That keeps refreshable Claude credentials refreshable.

`hermes model`
`~/.hermes/.env`

Or set it permanently:

```
model:  provider: "anthropic"  default: "claude-sonnet-4-6"
```

--provider claudeand--provider claude-codealso work as shorthand for--provider anthropic.

`--provider claude`
`--provider claude-code`
`--provider anthropic`

### GitHub Copilot​

Hermes supports GitHub Copilot as a first-class provider with two modes:

copilot— Direct Copilot API(recommended). Uses your GitHub Copilot subscription to access GPT-5.x, Claude, Gemini, and other models through the Copilot API.

`copilot`

```
hermes chat --provider copilot --model gpt-5.4
```

Authentication options(checked in this order):

1. COPILOT_GITHUB_TOKENenvironment variable
2. GH_TOKENenvironment variable
3. GITHUB_TOKENenvironment variable
4. gh auth tokenCLI fallback

`COPILOT_GITHUB_TOKEN`
`GH_TOKEN`
`GITHUB_TOKEN`
`gh auth token`

If no token is found,hermes modeloffers anOAuth device code login— the same flow used by the Copilot CLI and opencode.

`hermes model`

The Copilot API doesnotsupport classic Personal Access Tokens (ghp_*). Supported token types:

`ghp_*`
| Type | Prefix | How to get |
| --- | --- | --- |
| OAuth token | gho_ | hermes model→ GitHub Copilot → Login with GitHub |
| Fine-grained PAT | github_pat_ | GitHub Settings → Developer settings → Fine-grained tokens (needsCopilot Requestspermission) |
| GitHub App token | ghu_ | Via GitHub App installation |

`gho_`
`hermes model`
`github_pat_`
`ghu_`

If yourgh auth tokenreturns aghp_*token, usehermes modelto authenticate via OAuth instead.

`gh auth token`
`ghp_*`
`hermes model`

Hermes sends a supported GitHub token (gho_*,github_pat_*, orghu_*) directly toapi.githubcopilot.comand includes Copilot-specific headers (Editor-Version,Copilot-Integration-Id,Openai-Intent,x-initiator).

`gho_*`
`github_pat_*`
`ghu_*`
`api.githubcopilot.com`
`Editor-Version`
`Copilot-Integration-Id`
`Openai-Intent`
`x-initiator`

On HTTP 401, Hermes now performs a one-shot credential recovery before fallback:

1. Re-resolve token via the normal priority chain (COPILOT_GITHUB_TOKEN→GH_TOKEN→GITHUB_TOKEN→gh auth token)
2. Rebuild the shared OpenAI client with refreshed headers
3. Retry the request once

`COPILOT_GITHUB_TOKEN`
`GH_TOKEN`
`GITHUB_TOKEN`
`gh auth token`

Some older community proxies useapi.github.com/copilot_internal/v2/tokenexchange flows. That endpoint can be unavailable for some account types (returns 404). Hermes therefore keeps direct-token auth as the primary path and relies on runtime credential refresh + retry for robustness.

`api.github.com/copilot_internal/v2/token`

API routing: GPT-5+ models (exceptgpt-5-mini) automatically use the Responses API. All other models (GPT-4o, Claude, Gemini, etc.) use Chat Completions. Models are auto-detected from the live Copilot catalog.

`gpt-5-mini`

copilot-acp— Copilot ACP agent backend. Spawns the local Copilot CLI as a subprocess:

`copilot-acp`

```
hermes chat --provider copilot-acp --model copilot-acp# Requires the GitHub Copilot CLI in PATH and an existing `copilot login` session
```

Permanent config:

```
model:  provider: "copilot"  default: "gpt-5.4"
```

| Environment variable | Description |
| --- | --- |
| COPILOT_GITHUB_TOKEN | GitHub token for Copilot API (first priority) |
| HERMES_COPILOT_ACP_COMMAND | Override the Copilot CLI binary path (default:copilot) |
| HERMES_COPILOT_ACP_ARGS | Override ACP args (default:--acp --stdio) |

`COPILOT_GITHUB_TOKEN`
`HERMES_COPILOT_ACP_COMMAND`
`copilot`
`HERMES_COPILOT_ACP_ARGS`
`--acp --stdio`

### First-Class API-Key Providers​

These providers have built-in support with dedicated provider IDs. Set the API key and use--providerto select:

`--provider`

```
# NovitaAI Model APIhermes chat --provider novita --model moonshotai/kimi-k2.5# Requires: NOVITA_API_KEY in ~/.hermes/.env# z.ai / ZhipuAI GLMhermes chat --provider zai --model glm-5# Requires: GLM_API_KEY in ~/.hermes/.env# Kimi / Moonshot AI (international: api.moonshot.ai)hermes chat --provider kimi-coding --model kimi-for-coding# Requires: KIMI_API_KEY in ~/.hermes/.env# Kimi / Moonshot AI (China: api.moonshot.cn)hermes chat --provider kimi-coding-cn --model kimi-k2.5# Requires: KIMI_CN_API_KEY in ~/.hermes/.env# MiniMax (global endpoint)hermes chat --provider minimax --model MiniMax-M2.7# Requires: MINIMAX_API_KEY in ~/.hermes/.env# MiniMax (China endpoint)hermes chat --provider minimax-cn --model MiniMax-M2.7# Requires: MINIMAX_CN_API_KEY in ~/.hermes/.env# Qwen Cloud / DashScope (Qwen models)hermes chat --provider alibaba --model qwen3.5-plus# Requires: DASHSCOPE_API_KEY in ~/.hermes/.env# Xiaomi MiMohermes chat --provider xiaomi --model mimo-v2-pro# Requires: XIAOMI_API_KEY in ~/.hermes/.env# Tencent TokenHub (Hy3 Preview)hermes chat --provider tencent-tokenhub --model hy3-preview# Requires: TOKENHUB_API_KEY in ~/.hermes/.env# Arcee AI (Trinity models)hermes chat --provider arcee --model trinity-large-thinking# Requires: ARCEEAI_API_KEY in ~/.hermes/.env# GMI Cloud# Use the exact model ID returned by GMI's /v1/models endpoint.hermes chat --provider gmi --model zai-org/GLM-5.1-FP8# Requires: GMI_API_KEY in ~/.hermes/.env
```

Or set the provider permanently inconfig.yaml:

`config.yaml`

```
model:  provider: "gmi"  default: "zai-org/GLM-5.1-FP8"
```

Base URLs can be overridden withNOVITA_BASE_URL,GLM_BASE_URL,KIMI_BASE_URL,MINIMAX_BASE_URL,MINIMAX_CN_BASE_URL,DASHSCOPE_BASE_URL,XIAOMI_BASE_URL,GMI_BASE_URL, orTOKENHUB_BASE_URLenvironment variables.

`NOVITA_BASE_URL`
`GLM_BASE_URL`
`KIMI_BASE_URL`
`MINIMAX_BASE_URL`
`MINIMAX_CN_BASE_URL`
`DASHSCOPE_BASE_URL`
`XIAOMI_BASE_URL`
`GMI_BASE_URL`
`TOKENHUB_BASE_URL`

When using the Z.AI / GLM provider, Hermes automatically probes multiple endpoints (global, China, coding variants) to find one that accepts your API key. You don't need to setGLM_BASE_URLmanually — the working endpoint is detected and cached automatically.

`GLM_BASE_URL`

### xAI (Grok) — Responses API + Prompt Caching​

xAI is wired through the Responses API (codex_responsestransport) for automatic reasoning support on Grok 4 models — noreasoning_effortparameter needed, the server reasons by default. SetXAI_API_KEYin~/.hermes/.envand pick xAI inhermes model, or dropgrokas a shortcut into/model grok-4-fast-reasoning.

`codex_responses`
`reasoning_effort`
`XAI_API_KEY`
`~/.hermes/.env`
`hermes model`
`grok`
`/model grok-4-fast-reasoning`

SuperGrok and X Premium+ subscribers can sign in with browser OAuth instead of using an API key — pickxAI Grok OAuth (SuperGrok / Premium+)inhermes model, or runhermes auth add xai-oauth. The same OAuth bearer token is automatically reused by direct-to-xAI tools (TTS, image gen, video gen, transcription). See thexAI Grok OAuth guidefor the full flow — and if Hermes runs on a remote host, also seeOAuth over SSH / Remote Hostsfor the requiredssh -Ltunnel.

`hermes model`
`hermes auth add xai-oauth`
`ssh -L`

When using xAI as a provider (any base URL containingx.ai), Hermes automatically enables prompt caching by sending thex-grok-conv-idheader with every API request. This routes requests to the same server within a conversation session, allowing xAI's infrastructure to reuse cached system prompts and conversation history.

`x.ai`
`x-grok-conv-id`

No configuration is needed — caching activates automatically when an xAI endpoint is detected and a session ID is available. This reduces latency and cost for multi-turn conversations.

xAI also ships a dedicated TTS endpoint (/v1/tts). SelectxAI TTSinhermes tools→ Voice & TTS, or see theVoice & TTSpage for config.

`/v1/tts`
`hermes tools`

Retired xAI model migration (May 15, 2026):xAI is retiringgrok-4*,grok-3,grok-code-fast-1, andgrok-imagine-image-proon 2026-05-15.hermes doctorandhermes chatstartup both detect any config still pointing at a retired ref and print the recommended replacement. Usehermes migrate xaifor a one-shot config rewrite — dry-run by default, add--applyto write changes (a timestampedconfig.yaml.bak-pre-migrate-xai-*backup is created automatically).

`grok-4*`
`grok-3`
`grok-code-fast-1`
`grok-imagine-image-pro`
`hermes doctor`
`hermes chat`
`hermes migrate xai`
`--apply`
`config.yaml.bak-pre-migrate-xai-*`

```
hermes migrate xai          # preview replacementshermes migrate xai --apply  # rewrite ~/.hermes/config.yaml in place
```

xAI Web Search backend.When theWeb Searchtoolset is enabled,web.backend: xairoutes search through xAI's hosted search endpoint using the sameXAI_API_KEY/ OAuth credentials. No additional setup required if xAI is already configured as a provider.

`web.backend: xai`
`XAI_API_KEY`

### NovitaAI​

NovitaAIis the AI-native cloud for builders and agents. Its three product lines are Model API for 200+ models, Agent Sandbox for building and running AI agents, and GPU Cloud for scalable compute, all available from one platform.

```
# Use any available modelhermes chat --provider novita --model moonshotai/kimi-k2.5# Requires: NOVITA_API_KEY in ~/.hermes/.env# Short aliashermes chat --provider novita-ai --model deepseek/deepseek-v3-0324
```

Or set it permanently inconfig.yaml:

`config.yaml`

```
model:  provider: "novita"  default: "moonshotai/kimi-k2.5"  base_url: "https://api.novita.ai/openai/v1"
```

Get your API key atnovita.ai/settings/key-management. The base URL can be overridden withNOVITA_BASE_URL.

`NOVITA_BASE_URL`

### Ollama Cloud — Managed Ollama Models, OAuth + API Key​

Ollama Cloudhosts the same open-weight catalog as local Ollama but without the GPU requirement. Pick it inhermes modelasOllama Cloud, paste your API key fromollama.com/settings/keys, and Hermes auto-discovers the available models.

`hermes model`

```
hermes model# → pick "Ollama Cloud"# → paste your OLLAMA_API_KEY# → select from discovered models (gpt-oss:120b, glm-4.6:cloud, qwen3-coder:480b-cloud, etc.)
```

Orconfig.yamldirectly:

`config.yaml`

```
model:  provider: "ollama-cloud"  default: "gpt-oss:120b"
```

The model catalog is fetched dynamically fromollama.com/v1/modelsand cached for one hour.model:tagnotation (e.g.qwen3-coder:480b-cloud) is preserved through normalization — don't use dashes.

`ollama.com/v1/models`
`model:tag`
`qwen3-coder:480b-cloud`

Both speak the same OpenAI-compatible API. Cloud is a first-class provider (--provider ollama-cloud,OLLAMA_API_KEY); local Ollama is reached via the Custom Endpoint flow (base URLhttp://localhost:11434/v1, no key). Use cloud for large models you can't run locally; use local for privacy or offline work.

`--provider ollama-cloud`
`OLLAMA_API_KEY`
`http://localhost:11434/v1`

### AWS Bedrock​

Anthropic Claude, Amazon Nova, DeepSeek v3.2, Meta Llama 4, and other models via AWS Bedrock. Uses the AWS SDK (boto3) credential chain — no API key, just standard AWS auth.

`boto3`

```
# Simplest — named profile in ~/.aws/credentialshermes chat --provider bedrock --model us.anthropic.claude-sonnet-4-6# Or with explicit env varsAWS_PROFILE=myprofile AWS_REGION=us-east-1 hermes chat --provider bedrock --model us.anthropic.claude-sonnet-4-6
```

Or permanently inconfig.yaml:

`config.yaml`

```
model:  provider: "bedrock"  default: "us.anthropic.claude-sonnet-4-6"bedrock:  region: "us-east-1"          # or set AWS_REGION  # profile: "myprofile"       # or set AWS_PROFILE  # discovery: true            # auto-discover region from IAM  # guardrail:                 # optional Bedrock Guardrails  #   guardrail_identifier: "your-guardrail-id"  #   guardrail_version: "DRAFT"
```

Authentication uses the standard boto3 chain: explicitAWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY,AWS_PROFILEfrom~/.aws/credentials, IAM role on EC2/ECS/Lambda, IMDS, or SSO. No env var is required if you're already authenticated with the AWS CLI.

`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`
`AWS_PROFILE`
`~/.aws/credentials`

Bedrock uses theConverse APIunder the hood — requests are translated to Bedrock's model-agnostic shape, so the same config works for Claude, Nova, DeepSeek, and Llama models. SetBEDROCK_BASE_URLonly if you're calling a non-default regional endpoint.

`BEDROCK_BASE_URL`

See theAWS Bedrock guidefor a walkthrough of IAM setup, region selection, and cross-region inference.

### Google Vertex AI​

Gemini models on Google Cloud Vertex AI via Vertex's OpenAI-compatible endpoint. Authentication isOAuth2— a short-lived access token (~1 hour) minted from a service-account JSON or Application Default Credentials (ADC). There isno static API key; Hermes mints and auto-refreshes the token for you, including re-minting on a mid-session401.

`401`

```
# Service account JSON (recommended for servers / gateways)echo "VERTEX_CREDENTIALS_PATH=/path/to/service-account.json" >> ~/.hermes/.env# or Application Default Credentialsgcloud auth application-default loginhermes model   # → "Google Vertex AI" → project → region → model
```

Or inconfig.yaml(project/region are non-secret and live here; the credential path stays in.env):

`config.yaml`
`.env`

```
model:  provider: "vertex"  default: "google/gemini-3-flash-preview"   # Vertex requires the google/ prefixvertex:  project_id: "my-gcp-project"   # blank → use the project embedded in the credentials  region: "global"               # required for the Gemini 3.x previews
```

VERTEX_PROJECT_ID/VERTEX_REGIONenv vars override theconfig.yamlvalues. Install withpip install 'hermes-agent[vertex]'(or let Hermes lazy-installgoogle-authon first use). See theGoogle Vertex AI guidefor the full walkthrough, and theGoogle Gemini guidefor the static-API-key AI Studio path instead.

`VERTEX_PROJECT_ID`
`VERTEX_REGION`
`config.yaml`
`pip install 'hermes-agent[vertex]'`
`google-auth`

### Qwen Portal (OAuth)​

Alibaba's Qwen Portal with browser-based OAuth login. PickQwen OAuth (Portal)inhermes model, sign in through the browser, and Hermes persists the refresh token.

`hermes model`

```
hermes model# → pick "Qwen OAuth (Portal)"# → browser opens; sign in with your Alibaba account# → confirm — credentials are saved to ~/.hermes/auth.jsonhermes chat   # uses portal.qwen.ai/v1 endpoint
```

Or configureconfig.yaml:

`config.yaml`

```
model:  provider: "qwen-oauth"  default: "qwen3-coder-plus"
```

SetHERMES_QWEN_BASE_URLonly if the portal endpoint relocates (default:https://portal.qwen.ai/v1).

`HERMES_QWEN_BASE_URL`
`https://portal.qwen.ai/v1`

qwen-oauthuses the consumer-facing Qwen Portal with OAuth login — ideal for individual users. Thealibabaprovider uses Qwen Cloud (Alibaba DashScope) with aDASHSCOPE_API_KEY— ideal for programmatic / production workloads. Both route to Qwen-family models but live at different endpoints.

`qwen-oauth`
`alibaba`
`DASHSCOPE_API_KEY`

### Alibaba Cloud (Coding Plan)​

If you're subscribed to Alibaba'sCoding Plan(a pricing SKU separate from standard DashScope API access), Hermes exposes it as its own first-class provider:alibaba-coding-plan. Endpoint:https://coding-intl.dashscope.aliyuncs.com/v1. It's OpenAI-compatible like the regularalibabaprovider but with a different base URL and billing surface.

`alibaba-coding-plan`
`https://coding-intl.dashscope.aliyuncs.com/v1`
`alibaba`

```
model:  provider: alibaba_coding     # alias for alibaba-coding-plan  model: qwen3-coder-plus
```

Or from the CLI:

```
hermes chat --provider alibaba_coding --model qwen3-coder-plus
```

alibaba_codinguses the sameDASHSCOPE_API_KEYyouralibabaentry already uses — no separate key needed, just a different routing target. Before this provider was registered, users who setprovider: alibaba_codinginconfig.yamlsilently fell through to OpenRouter routing.

`alibaba_coding`
`DASHSCOPE_API_KEY`
`alibaba`
`provider: alibaba_coding`
`config.yaml`

### MiniMax (OAuth)​

MiniMax-M2.7 via browser OAuth login — no API key needed. PickMiniMax (OAuth)inhermes model, sign in through the browser, and Hermes persists the access + refresh tokens. Uses the Anthropic Messages-compatible endpoint (/anthropic) under the hood.

`hermes model`
`/anthropic`

```
hermes model# → pick "MiniMax (OAuth)"# → browser opens; sign in with your MiniMax account (global or CN region)# → confirm — credentials are saved to ~/.hermes/auth.jsonhermes chat   # uses api.minimax.io/anthropic endpoint
```

Or configureconfig.yaml:

`config.yaml`

```
model:  provider: "minimax-oauth"  default: "MiniMax-M2.7"
```

Supported models:MiniMax-M2.7(main) andMiniMax-M2.7-highspeed(wired as the default auxiliary model). The OAuth path ignoresMINIMAX_API_KEY/MINIMAX_BASE_URL.

`MiniMax-M2.7`
`MiniMax-M2.7-highspeed`
`MINIMAX_API_KEY`
`MINIMAX_BASE_URL`

minimax-oauthuses MiniMax's consumer-facing portal with OAuth login — no billing setup required. Theminimaxandminimax-cnproviders useMINIMAX_API_KEY/MINIMAX_CN_API_KEY— for programmatic access. See theMiniMax OAuth guidefor a full walkthrough.

`minimax-oauth`
`minimax`
`minimax-cn`
`MINIMAX_API_KEY`
`MINIMAX_CN_API_KEY`

### NVIDIA NIM​

Nemotron and other open source models viabuild.nvidia.com(free API key) or a local NIM endpoint.

```
# Cloud (build.nvidia.com)hermes chat --provider nvidia --model nvidia/nemotron-3-super-120b-a12b# Requires: NVIDIA_API_KEY in ~/.hermes/.env# Local NIM endpoint — override base URLNVIDIA_BASE_URL=http://localhost:8000/v1 hermes chat --provider nvidia --model nvidia/nemotron-3-super-120b-a12b
```

Or set it permanently inconfig.yaml:

`config.yaml`

```
model:  provider: "nvidia"  default: "nvidia/nemotron-3-super-120b-a12b"
```

For on-prem deployments (DGX Spark, local GPU), setNVIDIA_BASE_URL=http://localhost:8000/v1. NIM exposes the same OpenAI-compatible chat completions API as build.nvidia.com, so switching between cloud and local is a one-line env-var change.

`NVIDIA_BASE_URL=http://localhost:8000/v1`

Hermes automatically attaches the NIM billing-origin header on every request tobuild.nvidia.com— no configuration needed. This routes consumption against the correct origin in NVIDIA's billing dashboard.

`build.nvidia.com`

### GMI Cloud​

Open and reasoning models viaGMI Cloud— OpenAI-compatible API, API key authentication.

```
# GMI Cloudhermes chat --provider gmi --model deepseek-ai/DeepSeek-V3.2# Requires: GMI_API_KEY in ~/.hermes/.env
```

Or set it permanently inconfig.yaml:

`config.yaml`

```
model:  provider: "gmi"  default: "deepseek-ai/DeepSeek-V3.2"
```

The base URL can be overridden withGMI_BASE_URL(default:https://api.gmi-serving.com/v1).

`GMI_BASE_URL`
`https://api.gmi-serving.com/v1`

### StepFun​

Step-series models viaStepFun— OpenAI-compatible API, API key authentication.

```
# StepFunhermes chat --provider stepfun --model step-3.5-flash# Requires: STEPFUN_API_KEY in ~/.hermes/.env
```

Or set it permanently inconfig.yaml:

`config.yaml`

```
model:  provider: "stepfun"  default: "step-3.5-flash"
```

The base URL can be overridden withSTEPFUN_BASE_URL(default:https://api.stepfun.com/v1).

`STEPFUN_BASE_URL`
`https://api.stepfun.com/v1`

### Hugging Face Inference Providers​

Hugging Face Inference Providersroutes to 20+ open models through a unified OpenAI-compatible endpoint (router.huggingface.co/v1). Requests are automatically routed to the fastest available backend (Groq, Together, SambaNova, etc.) with automatic failover.

`router.huggingface.co/v1`

```
# Use any available modelhermes chat --provider huggingface --model Qwen/Qwen3.5-397B-A17B# Requires: HF_TOKEN in ~/.hermes/.env# Short aliashermes chat --provider hf --model deepseek-ai/DeepSeek-V3.2
```

Or set it permanently inconfig.yaml:

`config.yaml`

```
model:  provider: "huggingface"  default: "Qwen/Qwen3.5-397B-A17B"
```

Get your token athuggingface.co/settings/tokens— make sure to enable the "Make calls to Inference Providers" permission. Free tier included ($0.10/month credit, no markup on provider rates).

You can append routing suffixes to model names::fastest(default),:cheapest, or:provider_nameto force a specific backend.

`:fastest`
`:cheapest`
`:provider_name`

The base URL can be overridden withHF_BASE_URL.

`HF_BASE_URL`

## Custom & Self-Hosted LLM Providers​

Hermes Agent works withany OpenAI-compatible API endpoint. If a server implements/v1/chat/completions, you can point Hermes at it. This means you can use local models, GPU inference servers, multi-provider routers, or any third-party API.

`/v1/chat/completions`

### General Setup​

Three ways to configure a custom endpoint:

Interactive setup (recommended):

```
hermes model# Select "Custom endpoint (self-hosted / VLLM / etc.)"# Enter: API base URL, API key, Model name
```

Manual config (config.yaml):

`config.yaml`

```
# In ~/.hermes/config.yamlmodel:  default: your-model-name  provider: custom  base_url: http://localhost:8000/v1  api_key: your-key-or-leave-empty-for-local
```

LLM_MODELin.envisremoved—config.yamlis the single source of truth for model and endpoint configuration.OPENAI_BASE_URLis still honored, butonlyfor theopenai-apiprovider (it overrides the OpenAI endpoint for direct API-key access). For other providers and custom endpoints, usehermes modelor setmodel.base_urlinconfig.yamldirectly. If you have stale entries in your.env, they are automatically cleared on the nexthermes setupor config migration.

`LLM_MODEL`
`.env`
`config.yaml`
`OPENAI_BASE_URL`
`openai-api`
`hermes model`
`model.base_url`
`config.yaml`
`.env`
`hermes setup`

Both approaches persist toconfig.yaml, which is the source of truth for model, provider, and base URL.

`config.yaml`

### Switching Models with/model​

`/model`

hermes model(run from your terminal, outside any chat session) is thefull provider setup wizard. Use it to add new providers, run OAuth flows, enter API keys, and configure custom endpoints.

`hermes model`

/model(typed inside an active Hermes chat session) can onlyswitch between providers and models you've already set up. It cannot add new providers, run OAuth, or prompt for API keys. If you've only configured one provider (e.g. OpenRouter),/modelwill only show models for that provider.

`/model`
`/model`

To add a new provider:Exit your session (Ctrl+Cor/quit), runhermes model, set up the new provider, then start a new session.

`Ctrl+C`
`/quit`
`hermes model`

Once you have at least one custom endpoint configured, you can switch models mid-session:

```
/model custom:qwen-2.5          # Switch to a model on your custom endpoint/model custom                    # Auto-detect the model from the endpoint/model openrouter:claude-sonnet-4 # Switch back to a cloud provider
```

If you havenamed custom providersconfigured (see below), use the triple syntax:

```
/model custom:local:qwen-2.5    # Use the "local" custom provider with model qwen-2.5/model custom:work:llama3       # Use the "work" custom provider with llama3
```

When switching providers, Hermes persists the base URL and provider to config so the change survives restarts. When switching away from a custom endpoint to a built-in provider, the stale base URL is automatically cleared.

/model custom(bare, no model name) queries your endpoint's/modelsAPI and auto-selects the model if exactly one is loaded. Useful for local servers running a single model.

`/model custom`
`/models`

Everything below follows this same pattern — just change the URL, key, and model name.

### Ollama — Local Models, Zero Config​

Ollamaruns open-weight models locally with one command. Best for: quick local experimentation, privacy-sensitive work, offline use. Supports tool calling via the OpenAI-compatible API.

```
# Install and run a modelollama pull qwen2.5-coder:32bollama serve   # Starts on port 11434
```

Then configure Hermes:

```
hermes model# Select "Custom endpoint (self-hosted / VLLM / etc.)"# Enter URL: http://localhost:11434/v1# Skip API key (Ollama doesn't need one)# Enter model name (e.g. qwen2.5-coder:32b)
```

Or configureconfig.yamldirectly:

`config.yaml`

```
model:  default: qwen2.5-coder:32b  provider: custom  base_url: http://localhost:11434/v1  context_length: 64000   # See warning below
```

Ollama doesnotuse your model's full context window by default. Depending on your VRAM, the default is:

| Available VRAM | Default context |
| --- | --- |
| Less than 24 GB | 4,096 tokens |
| 24–48 GB | 32,768 tokens |
| 48+ GB | 256,000 tokens |

Hermes Agent requires at least64,000 tokensof context for agent use with tools. Smaller windows are rejected at startup because the system prompt, tool schemas, and working conversation state need enough room for reliable multi-step workflows.

How to increase it(pick one):

```
# Option 1: Set server-wide via environment variable (recommended)OLLAMA_CONTEXT_LENGTH=64000 ollama serve# Option 2: For systemd-managed Ollamasudo systemctl edit ollama.service# Add: Environment="OLLAMA_CONTEXT_LENGTH=64000"# Then: sudo systemctl daemon-reload && sudo systemctl restart ollama# Option 3: Bake it into a custom model (persistent per-model)echo -e "FROM qwen2.5-coder:32b\nPARAMETER num_ctx 64000" > Modelfileollama create qwen2.5-coder-64k -f Modelfile
```

You cannot set context length through the OpenAI-compatible API(/v1/chat/completions). It must be configured server-side or via a Modelfile. This is the #1 source of confusion when integrating Ollama with tools like Hermes.

`/v1/chat/completions`

Verify your context is set correctly:

```
ollama ps# Look at the CONTEXT column — it should show your configured value
```

List available models withollama list. Pull any model from theOllama librarywithollama pull <model>. Ollama handles GPU offloading automatically — no configuration needed for most setups.

`ollama list`
`ollama pull <model>`

### vLLM — High-Performance GPU Inference​

vLLMis the standard for production LLM serving. Best for: maximum throughput on GPU hardware, serving large models, continuous batching.

```
pip install vllmvllm serve meta-llama/Llama-3.1-70B-Instruct \  --port 8000 \  --max-model-len 65536 \  --tensor-parallel-size 2 \  --enable-auto-tool-choice \  --tool-call-parser hermes
```

Then configure Hermes:

```
hermes model# Select "Custom endpoint (self-hosted / VLLM / etc.)"# Enter URL: http://localhost:8000/v1# Skip API key (or enter one if you configured vLLM with --api-key)# Enter model name: meta-llama/Llama-3.1-70B-Instruct
```

Context length:vLLM reads the model'smax_position_embeddingsby default. If that exceeds your GPU memory, it errors and asks you to set--max-model-lenlower. You can also use--max-model-len autoto automatically find the maximum that fits. Set--gpu-memory-utilization 0.95(default 0.9) to squeeze more context into VRAM.

`max_position_embeddings`
`--max-model-len`
`--max-model-len auto`
`--gpu-memory-utilization 0.95`

Tool calling requires explicit flags:

| Flag | Purpose |
| --- | --- |
| --enable-auto-tool-choice | Required fortool_choice: "auto"(the default in Hermes) |
| --tool-call-parser <name> | Parser for the model's tool call format |

`--enable-auto-tool-choice`
`tool_choice: "auto"`
`--tool-call-parser <name>`

Supported parsers:hermes(Qwen 2.5, Hermes 2/3),llama3_json(Llama 3.x),mistral,deepseek_v3,deepseek_v31,xlam,pythonic. Without these flags, tool calls won't work — the model will output tool calls as text.

`hermes`
`llama3_json`
`mistral`
`deepseek_v3`
`deepseek_v31`
`xlam`
`pythonic`

Qwen reasoning parsers:Hermes preserves structured reasoning metadata such asreasoning,reasoning_content, and streamed reasoning deltas when OpenAI-compatible servers return them. That metadata is treated as reasoning/thinking trace data, not as a replacement for the assistant's visible answer. For Qwen reasoning models served by vLLM, make sure the final user-visible response still appears incontent. If--reasoning-parser qwen3leavescontentempty in your deployment, either disable that parser or pass a server-supported request option such aschat_template_kwargs.enable_thinking: falsethroughextra_body.

`reasoning`
`reasoning_content`
`content`
`--reasoning-parser qwen3`
`content`
`chat_template_kwargs.enable_thinking: false`
`extra_body`

vLLM supports human-readable sizes:--max-model-len 64k(lowercase k = 1000, uppercase K = 1024).

`--max-model-len 64k`

### SGLang — Fast Serving with RadixAttention​

SGLangis an alternative to vLLM with RadixAttention for KV cache reuse. Best for: multi-turn conversations (prefix caching), constrained decoding, structured output.

```
pip install "sglang[all]"python -m sglang.launch_server \  --model meta-llama/Llama-3.1-70B-Instruct \  --port 30000 \  --context-length 65536 \  --tp 2 \  --tool-call-parser qwen
```

Then configure Hermes:

```
hermes model# Select "Custom endpoint (self-hosted / VLLM / etc.)"# Enter URL: http://localhost:30000/v1# Enter model name: meta-llama/Llama-3.1-70B-Instruct
```

Context length:SGLang reads from the model's config by default. Use--context-lengthto override. If you need to exceed the model's declared maximum, setSGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1.

`--context-length`
`SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1`

Tool calling:Use--tool-call-parserwith the appropriate parser for your model family:qwen(Qwen 2.5),llama3,llama4,deepseekv3,mistral,glm. Without this flag, tool calls come back as plain text.

`--tool-call-parser`
`qwen`
`llama3`
`llama4`
`deepseekv3`
`mistral`
`glm`

If responses seem truncated, addmax_tokensto your requests or set--default-max-tokenson the server. SGLang's default is only 128 tokens per response if not specified in the request.

`max_tokens`
`--default-max-tokens`

### llama.cpp / llama-server — CPU & Metal Inference​

llama.cppruns quantized models on CPU, Apple Silicon (Metal), and consumer GPUs. Best for: running models without a datacenter GPU, Mac users, edge deployment.

```
# Build and start llama-servercmake -B build && cmake --build build --config Release./build/bin/llama-server \  --jinja -fa \  -c 64000 \  -ngl 99 \  -m models/qwen2.5-coder-32b-instruct-Q4_K_M.gguf \  --port 8080 --host 0.0.0.0
```

Context length (-c):Recent builds default to0which reads the model's training context from the GGUF metadata. For models with 128k+ training context, this can OOM trying to allocate the full KV cache. Set-cexplicitly to at least 64,000 tokens for Hermes. If using parallel slots (-np), the total context is divided among slots — with-c 64000 -np 4, each slot only gets 16k, which is below Hermes' minimum per active session.

`-c`
`0`
`-c`
`-np`
`-c 64000 -np 4`

Then configure Hermes to point at it:

```
hermes model# Select "Custom endpoint (self-hosted / VLLM / etc.)"# Enter URL: http://localhost:8080/v1# Skip API key (local servers don't need one)# Enter model name — or leave blank to auto-detect if only one model is loaded
```

This saves the endpoint toconfig.yamlso it persists across sessions.

`config.yaml`
`--jinja`

Without--jinja, llama-server ignores thetoolsparameter entirely. The model will try to call tools by writing JSON in its response text, but Hermes won't recognize it as a tool call — you'll see raw JSON like{"name": "web_search", ...}printed as a message instead of an actual search.

`--jinja`
`tools`
`{"name": "web_search", ...}`

Native tool calling support (best performance): Llama 3.x, Qwen 2.5 (including Coder), Hermes 2/3, Mistral, DeepSeek, Functionary. All other models use a generic handler that works but may be less efficient. See thellama.cpp function calling docsfor the full list.

You can verify tool support is active by checkinghttp://localhost:8080/props— thechat_templatefield should be present.

`http://localhost:8080/props`
`chat_template`

Download GGUF models fromHugging Face. Q4_K_M quantization offers the best balance of quality vs. memory usage.

### LM Studio — Desktop App with Local Models​

LM Studiois a desktop app for running local models with a GUI. Best for: users who prefer a visual interface, quick model testing, developers on macOS/Windows/Linux.

Start the server from the LM Studio app (Developer tab → Start Server), or use the CLI:

```
lms server start                        # Starts on port 1234lms load qwen2.5-coder --context-length 64000
```

Then configure Hermes:

```
hermes model# Select "LM Studio"# Press Enter to use http://localhost:1234/v1# Pick one of the discovered models# If LM Studio server auth is enabled, enter LM_API_KEY when prompted
```

Hermes will automatically load a LM Studio model with 64K context length

To change context length in LM Studio:

1. Click the gear icon next to the model picker
2. Set "Context Length" to at least 64000 for a smooth experience
3. Reload the model for the change to take effect
4. If your machine cannot fit 64000, consider using a smaller model with larger context lengths.

Alternatively, use the CLI:lms load model-name --context-length 64000

`lms load model-name --context-length 64000`

You can use the CLI to estimate if the model will fit:lms load model-name --context-length 64000 --estimate-only

`lms load model-name --context-length 64000 --estimate-only`

To set persistent per-model defaults: My Models tab → gear icon on the model → set context size.
:::

Tool calling:Supported since LM Studio 0.3.6. Models with native tool-calling training (Qwen 2.5, Llama 3.x, Mistral, Hermes) are auto-detected and shown with a tool badge. Other models use a generic fallback that may be less reliable.

### WSL2 Networking (Windows Users)​

Since Hermes Agent requires a Unix environment, Windows users run it inside WSL2. If your model server (Ollama, LM Studio, etc.) runs on theWindows host, you need to bridge the network gap — WSL2 uses a virtual network adapter with its own subnet, solocalhostinside WSL2 refers to the Linux VM,notthe Windows host.

`localhost`

If your model server also runs inside WSL2 (common for vLLM, SGLang, and llama-server),localhostworks as expected — they share the same network namespace. Skip this section.

`localhost`

#### Option 1: Mirrored Networking Mode (Recommended)​

Available onWindows 11 22H2+, mirrored mode makeslocalhostwork bidirectionally between Windows and WSL2 — the simplest fix.

`localhost`
1. Create or edit%USERPROFILE%\.wslconfig(e.g.,C:\Users\YourName\.wslconfig):[wsl2]networkingMode=mirrored
2. Restart WSL from PowerShell:wsl --shutdown
3. Reopen your WSL2 terminal.localhostnow reaches Windows services:curlhttp://localhost:11434/v1/models# Ollama on Windows — works

Create or edit%USERPROFILE%\.wslconfig(e.g.,C:\Users\YourName\.wslconfig):

`%USERPROFILE%\.wslconfig`
`C:\Users\YourName\.wslconfig`

```
[wsl2]networkingMode=mirrored
```

Restart WSL from PowerShell:

```
wsl --shutdown
```

Reopen your WSL2 terminal.localhostnow reaches Windows services:

`localhost`

```
curl http://localhost:11434/v1/models   # Ollama on Windows — works
```

On some Windows 11 builds, the Hyper-V firewall blocks mirrored connections by default. Iflocalhoststill doesn't work after enabling mirrored mode, run this in anAdmin PowerShell:

`localhost`

```
Set-NetFirewallHyperVVMSetting -Name '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -DefaultInboundAction Allow
```

#### Option 2: Use the Windows Host IP (Windows 10 / older builds)​

If you can't use mirrored mode, find the Windows host IP from inside WSL2 and use that instead oflocalhost:

`localhost`

```
# Get the Windows host IP (the default gateway of WSL2's virtual network)ip route show | grep -i default | awk '{ print $3 }'# Example output: 172.29.192.1
```

Use that IP in your Hermes config:

```
model:  default: qwen2.5-coder:32b  provider: custom  base_url: http://172.29.192.1:11434/v1   # Windows host IP, not localhost
```

The host IP can change on WSL2 restart. You can grab it dynamically in your shell:

```
export WSL_HOST=$(ip route show | grep -i default | awk '{ print $3 }')echo "Windows host at: $WSL_HOST"curl http://$WSL_HOST:11434/v1/models   # Test Ollama
```

Or use your machine's mDNS name (requireslibnss-mdnsin WSL2):

`libnss-mdns`

```
sudo apt install libnss-mdnscurl http://$(hostname).local:11434/v1/models
```

#### Server Bind Address (Required for NAT Mode)​

If you're usingOption 2(NAT mode with the host IP), the model server on Windows must accept connections from outside127.0.0.1. By default, most servers only listen on localhost — WSL2 connections in NAT mode come from a different virtual subnet and will be refused. In mirrored mode,localhostmaps directly so the default127.0.0.1binding works fine.

`127.0.0.1`
`localhost`
`127.0.0.1`
| Server | Default bind | How to fix |
| --- | --- | --- |
| Ollama | 127.0.0.1 | SetOLLAMA_HOST=0.0.0.0environment variable before starting Ollama (System Settings → Environment Variables on Windows, or edit the Ollama service) |
| LM Studio | 127.0.0.1 | Enable"Serve on Network"in the Developer tab → Server settings |
| llama-server | 127.0.0.1 | Add--host 0.0.0.0to the startup command |
| vLLM | 0.0.0.0 | Already binds to all interfaces by default |
| SGLang | 127.0.0.1 | Add--host 0.0.0.0to the startup command |

`127.0.0.1`
`OLLAMA_HOST=0.0.0.0`
`127.0.0.1`
`127.0.0.1`
`--host 0.0.0.0`
`0.0.0.0`
`127.0.0.1`
`--host 0.0.0.0`

Ollama on Windows (detailed):Ollama runs as a Windows service. To setOLLAMA_HOST:

`OLLAMA_HOST`
1. OpenSystem Properties→Environment Variables
2. Add a newSystem variable:OLLAMA_HOST=0.0.0.0
3. Restart the Ollama service (or reboot)

`OLLAMA_HOST`
`0.0.0.0`

#### Windows Firewall​

Windows Firewall treats WSL2 as a separate network (in both NAT and mirrored mode). If connections still fail after the steps above, add a firewall rule for your model server's port:

```
# Run in Admin PowerShell — replace PORT with your server's portNew-NetFirewallRule -DisplayName "Allow WSL2 to Model Server" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 11434
```

Common ports: Ollama11434, vLLM8000, SGLang30000, llama-server8080, LM Studio1234.

`11434`
`8000`
`30000`
`8080`
`1234`

#### Quick Verification​

From inside WSL2, test that you can reach your model server:

```
# Replace URL with your server's address and portcurl http://localhost:11434/v1/models          # Mirrored modecurl http://172.29.192.1:11434/v1/models       # NAT mode (use your actual host IP)
```

If you get a JSON response listing your models, you're good. Use that same URL as thebase_urlin your Hermes config.

`base_url`

### Troubleshooting Local Models​

These issues affectalllocal inference servers when used with Hermes.

#### "Connection refused" from WSL2 to a Windows-hosted model server​

If you're running Hermes inside WSL2 and your model server on the Windows host,http://localhost:<port>won't work in WSL2's default NAT networking mode. SeeWSL2 Networkingabove for the fix.

`http://localhost:<port>`

#### Tool calls appear as text instead of executing​

The model outputs something like{"name": "web_search", "arguments": {...}}as a message instead of actually calling the tool.

`{"name": "web_search", "arguments": {...}}`

Cause:Your server doesn't have tool calling enabled, or the model doesn't support it through the server's tool calling implementation.

| Server | Fix |
| --- | --- |
| llama.cpp | Add--jinjato the startup command |
| vLLM | Add--enable-auto-tool-choice --tool-call-parser hermes |
| SGLang | Add--tool-call-parser qwen(or appropriate parser) |
| Ollama | Tool calling is enabled by default — make sure your model supports it (check withollama show model-name) |
| LM Studio | Update to 0.3.6+ and use a model with native tool support |

`--jinja`
`--enable-auto-tool-choice --tool-call-parser hermes`
`--tool-call-parser qwen`
`ollama show model-name`

#### Model seems to forget context or give incoherent responses​

Cause:Context window is too small. When the conversation exceeds the context limit, most servers silently drop older messages. Hermes's system prompt + tool schemas alone can use 4k–8k tokens.

Diagnosis:

```
# Check what Hermes thinks the context is# Look at startup line: "Context limit: X tokens"# Check your server's actual context# Ollama: ollama ps (CONTEXT column)# llama.cpp: curl http://localhost:8080/props | jq '.default_generation_settings.n_ctx'# vLLM: check --max-model-len in startup args
```

Fix:Set context to at least64,000 tokensfor agent use. See each server's section above for the specific flag.

#### "Context limit: 2048 tokens" at startup​

Hermes auto-detects context length from your server's/v1/modelsendpoint. If the server reports a low value (or doesn't report one at all), Hermes uses the model's declared limit which may be wrong.

`/v1/models`

Fix:Set it explicitly inconfig.yaml:

`config.yaml`

```
model:  default: your-model  provider: custom  base_url: http://localhost:11434/v1  context_length: 64000
```

#### Responses get cut off mid-sentence​

Possible causes:

1. Low output cap (max_tokens) on the server— SGLang defaults to 128 tokens per response. Set--default-max-tokenson the server or configure Hermes withmodel.max_tokensin config.yaml. Note:max_tokenscontrols response length only — it is unrelated to how long your conversation history can be (that iscontext_length).
2. Context exhaustion— The model filled its context window. Increasemodel.context_lengthor enablecontext compressionin Hermes.

`max_tokens`
`--default-max-tokens`
`model.max_tokens`
`max_tokens`
`context_length`
`model.context_length`

### LiteLLM Proxy — Multi-Provider Gateway​

LiteLLMis an OpenAI-compatible proxy that unifies 100+ LLM providers behind a single API. Best for: switching between providers without config changes, load balancing, fallback chains, budget controls.

```
# Install and startpip install "litellm[proxy]"litellm --model anthropic/claude-sonnet-4 --port 4000# Or with a config file for multiple models:litellm --config litellm_config.yaml --port 4000
```

Then configure Hermes withhermes model→ Custom endpoint →http://localhost:4000/v1.

`hermes model`
`http://localhost:4000/v1`

Examplelitellm_config.yamlwith fallback:

`litellm_config.yaml`

```
model_list:  - model_name: "best"    litellm_params:      model: anthropic/claude-sonnet-4      api_key: sk-ant-...  - model_name: "best"    litellm_params:      model: openai/gpt-4o      api_key: sk-...router_settings:  routing_strategy: "latency-based-routing"
```

### ClawRouter — Cost-Optimized Routing​

ClawRouterby BlockRunAI is a local routing proxy that auto-selects models based on query complexity. It classifies requests across 14 dimensions and routes to the cheapest model that can handle the task. Payment is via USDC cryptocurrency (no API keys).

```
# Install and startnpx @blockrun/clawrouter    # Starts on port 8402
```

Then configure Hermes withhermes model→ Custom endpoint →http://localhost:8402/v1→ model nameblockrun/auto.

`hermes model`
`http://localhost:8402/v1`
`blockrun/auto`

Routing profiles:

| Profile | Strategy | Savings |
| --- | --- | --- |
| blockrun/auto | Balanced quality/cost | 74-100% |
| blockrun/eco | Cheapest possible | 95-100% |
| blockrun/premium | Best quality models | 0% |
| blockrun/free | Free models only | 100% |
| blockrun/agentic | Optimized for tool use | varies |

`blockrun/auto`
`blockrun/eco`
`blockrun/premium`
`blockrun/free`
`blockrun/agentic`

ClawRouter requires a USDC-funded wallet on Base or Solana for payment. All requests route through BlockRun's backend API. Runnpx @blockrun/clawrouter doctorto check wallet status.

`npx @blockrun/clawrouter doctor`

### Other Compatible Providers​

Any service with an OpenAI-compatible API works. Some popular options:

| Provider | Base URL | Notes |
| --- | --- | --- |
| Together AI | https://api.together.xyz/v1 | Cloud-hosted open models |
| Groq | https://api.groq.com/openai/v1 | Ultra-fast inference |
| DeepSeek | https://api.deepseek.com/v1 | DeepSeek models |
| Fireworks AI | https://api.fireworks.ai/inference/v1 | Fast open model hosting |
| GMI Cloud | https://api.gmi-serving.com/v1 | Managed OpenAI-compatible inference |
| Cerebras | https://api.cerebras.ai/v1 | Wafer-scale chip inference |
| Mistral AI | https://api.mistral.ai/v1 | Mistral models |
| OpenAI | https://api.openai.com/v1 | Direct OpenAI access |
| Azure OpenAI | https://YOUR.openai.azure.com/ | Enterprise OpenAI |
| LocalAI | http://localhost:8080/v1 | Self-hosted, multi-model |
| Jan | http://localhost:1337/v1 | Desktop app with local models |

`https://api.together.xyz/v1`
`https://api.groq.com/openai/v1`
`https://api.deepseek.com/v1`
`https://api.fireworks.ai/inference/v1`
`https://api.gmi-serving.com/v1`
`https://api.cerebras.ai/v1`
`https://api.mistral.ai/v1`
`https://api.openai.com/v1`
`https://YOUR.openai.azure.com/`
`http://localhost:8080/v1`
`http://localhost:1337/v1`

Configure any of these withhermes model→ Custom endpoint, or inconfig.yaml:

`hermes model`
`config.yaml`

```
model:  default: meta-llama/Llama-3.1-70B-Instruct-Turbo  provider: custom  base_url: https://api.together.xyz/v1  api_key: your-together-key
```

### Context Length Detection​

context_lengthis thetotal context window— the combined budget for inputandoutput tokens (e.g. 200,000 for Claude Opus 4.6). Hermes uses this to decide when to compress history and to validate API requests.

`context_length`

model.max_tokensis theoutput cap— the maximum number of tokens the model may generate in asingle response. It has nothing to do with how long your conversation history can be. The industry-standard namemax_tokensis a common source of confusion; Anthropic's native API has since renamed itmax_output_tokensfor clarity.

`model.max_tokens`
`max_tokens`
`max_output_tokens`

Setcontext_lengthwhen auto-detection gets the window size wrong.
Setmodel.max_tokensonly when you need to limit how long individual responses can be.

`context_length`
`model.max_tokens`

Hermes uses a multi-source resolution chain to detect the correct context window for your model and provider:

1. Config override—model.context_lengthin config.yaml (highest priority)
2. Custom provider per-model—custom_providers[].models.<id>.context_length
3. Persistent cache— previously discovered values (survives restarts)
4. Endpoint/models— queries your server's API (local/custom endpoints)
5. Anthropic/v1/models— queries Anthropic's API formax_input_tokens(API-key users only)
6. OpenRouter API— live model metadata from OpenRouter
7. Nous Portal— suffix-matches Nous model IDs against OpenRouter metadata
8. models.dev— community-maintained registry with provider-specific context lengths for 3800+ models across 100+ providers
9. Fallback defaults— broad model family patterns (128K default)

`model.context_length`
`custom_providers[].models.<id>.context_length`
`/models`
`/v1/models`
`max_input_tokens`

For most setups this works out of the box. The system is provider-aware — the same model can have different context limits depending on who serves it (e.g.,claude-opus-4.6is 1M on Anthropic direct but 128K on GitHub Copilot).

`claude-opus-4.6`

To set the context length explicitly, addcontext_lengthto your model config:

`context_length`

```
model:  default: "qwen3.5:9b"  base_url: "http://localhost:8080/v1"  context_length: 131072  # tokens
```

For custom endpoints, you can also set context length per model:

```
custom_providers:  - name: "My Local LLM"    base_url: "http://localhost:11434/v1"    models:      qwen3.5:27b:        context_length: 64000      deepseek-r1:70b:        context_length: 65536
```

hermes modelwill prompt for context length when configuring a custom endpoint. Leave it blank for auto-detection.

`hermes model`
- You're using Ollama with a customnum_ctxthat's lower than the model's maximum
- You want to limit context below the model's maximum (e.g., 8k on a 128k model to save VRAM)
- You're running behind a proxy that doesn't expose/v1/models

`num_ctx`
`/v1/models`

### Named Custom Providers​

If you work with multiple custom endpoints (e.g., a local dev server and a remote GPU server), you can define them as named custom providers inconfig.yaml:

`config.yaml`

```
custom_providers:  - name: local    base_url: http://localhost:8080/v1    # api_key omitted — Hermes uses "no-key-required" for keyless local servers  - name: work    base_url: https://gpu-server.internal.corp/v1    key_env: CORP_API_KEY    api_mode: chat_completions   # set explicitly by `hermes model` → Custom Endpoint wizard; auto-detection still happens as a fallback  - name: anthropic-proxy    base_url: https://proxy.example.com/anthropic    key_env: ANTHROPIC_PROXY_KEY    api_mode: anthropic_messages  # for Anthropic-compatible proxies
```

Some OpenAI-compatible endpoints need provider-specific request body fields. Add anextra_bodymap to the matching custom provider and Hermes will merge it into each chat-completions request for that endpoint:

`extra_body`

```
custom_providers:  - name: gemma-local    base_url: http://localhost:8080/v1    model: google/gemma-4-31b-it    extra_body:      enable_thinking: true      reasoning_effort: high
```

Use the shape your server documents. For example, vLLM Gemma deployments and some NVIDIA NIM endpoints expectenable_thinkingunderchat_template_kwargsinstead of as a top-levelextra_bodyfield:

`enable_thinking`
`chat_template_kwargs`
`extra_body`

```
extra_body:  chat_template_kwargs:    enable_thinking: true
```

For Qwen reasoning models served by vLLM, this same shape can be used to disable thinking when a reasoning parser separates all generated text into reasoning fields and leaves the assistantcontentempty:

`content`

```
extra_body:  chat_template_kwargs:    enable_thinking: false
```

Thehermes model→ Custom Endpoint wizard now prompts forapi_modeexplicitly and persists your answer toconfig.yaml. URL-based auto-detection (e.g./anthropicpaths →anthropic_messages) still happens as a fallback when the field is left blank.

`hermes model`
`api_mode`
`config.yaml`
`/anthropic`
`anthropic_messages`

Native vision for custom-provider models.If your custom endpoint serves a vision-capable model that isn't in models.dev, setmodel.supports_vision: trueso Hermes routes attached images natively (asimage_urlparts) instead of pre-processing them throughvision_analyze. Single knob — no need to also setagent.image_input_mode: native.

`model.supports_vision: true`
`image_url`
`vision_analyze`
`agent.image_input_mode: native`

```
model:  provider: custom  base_url: http://localhost:8080/v1  default: qwen3.6-35b-a3b  supports_vision: true   # send images natively; otherwise vision_analyze pre-describes them
```

The same key is honored on per-named-provider models (custom_providers[*].models[*].supports_vision) and accepts standard YAML booleans (true/false/yes/no/on/off/1/0).

`custom_providers[*].models[*].supports_vision`
`true/false/yes/no/on/off/1/0`

Switch between them mid-session with the triple syntax:

```
/model custom:local:qwen-2.5       # Use the "local" endpoint with qwen-2.5/model custom:work:llama3-70b      # Use the "work" endpoint with llama3-70b/model custom:anthropic-proxy:claude-sonnet-4  # Use the proxy
```

You can also select named custom providers from the interactivehermes modelmenu.

`hermes model`

### Cookbook: Together AI, Groq, Perplexity​

The cloud providers listed inOther Compatible Providersall speak OpenAI's REST dialect, so they wire up the same way undercustom_providers:. Three worked recipes follow. Each drops into~/.hermes/config.yamland the matching API key goes in~/.hermes/.env.

`custom_providers:`
`~/.hermes/config.yaml`
`~/.hermes/.env`

#### Together AI​

Hosts open-weight models (Llama, MiniMax, Gemma, DeepSeek, Qwen) at prices significantly below first-party APIs. Good default for multi-model fleets.

```
# ~/.hermes/config.yamlcustom_providers:  - name: together    base_url: https://api.together.xyz/v1    key_env: TOGETHER_API_KEY    # api_mode: chat_completions  # default — no need to setmodel:  default: MiniMaxAI/MiniMax-M2.7   # or any model from together.ai/models  provider: custom:together
```

```
# ~/.hermes/.envTOGETHER_API_KEY=your-together-key
```

Switch models mid-session:

```
/model custom:together:meta-llama/Llama-3.3-70B-Instruct-Turbo/model custom:together:google/gemma-4-31b-it/model custom:together:deepseek-ai/DeepSeek-V3
```

Together's/v1/modelsendpoint works, sohermes modelcan auto-discover available models.

`/v1/models`
`hermes model`

#### Groq​

Ultra-fast inference (~500 tok/s on Llama-3.3-70B). Small catalog but strong for latency-sensitive interactive use.

```
# ~/.hermes/config.yamlcustom_providers:  - name: groq    base_url: https://api.groq.com/openai/v1    key_env: GROQ_API_KEYmodel:  default: llama-3.3-70b-versatile  provider: custom:groq
```

```
# ~/.hermes/.envGROQ_API_KEY=your-groq-key
```

#### Perplexity​

Useful when you want a model that does live web search and citation automatically. Strict about which models are available — checkperplexity.ai/settings/apifor the current list.

```
# ~/.hermes/config.yamlcustom_providers:  - name: perplexity    base_url: https://api.perplexity.ai    key_env: PERPLEXITY_API_KEYmodel:  default: sonar  provider: custom:perplexity
```

```
# ~/.hermes/.envPERPLEXITY_API_KEY=your-perplexity-key
```

#### Multiple providers in one config​

The three recipes compose — use all of them together and switch per turn with/model custom:<name>:<model>:

`/model custom:<name>:<model>`

```
custom_providers:  - name: together    base_url: https://api.together.xyz/v1    key_env: TOGETHER_API_KEY  - name: groq    base_url: https://api.groq.com/openai/v1    key_env: GROQ_API_KEY  - name: perplexity    base_url: https://api.perplexity.ai    key_env: PERPLEXITY_API_KEYmodel:  default: MiniMaxAI/MiniMax-M2.7  provider: custom:together      # boot to Together; switch freely after
```

- hermes doctorshould print noUnknown providerwarnings for any of these names after the CLI validator fixes in #15083.
- If a provider's/v1/modelsendpoint is unreachable (Perplexity is the common one),hermes modelwill persist the model with a warning rather than hard-reject — see #15136.
- To skipcustom_providers:entirely and use bareprovider: customwithCUSTOM_BASE_URLenv var, see #15103.

`hermes doctor`
`Unknown provider`
`/v1/models`
`hermes model`
`custom_providers:`
`provider: custom`
`CUSTOM_BASE_URL`

### Choosing the Right Setup​

| Use Case | Recommended |
| --- | --- |
| Just want it to work | OpenRouter (default) or Nous Portal |
| Local models, easy setup | Ollama |
| Production GPU serving | vLLM or SGLang |
| Mac / no GPU | Ollama or llama.cpp |
| Multi-provider routing | LiteLLM Proxy or OpenRouter |
| Cost optimization | ClawRouter or OpenRouter withsort: "price" |
| Maximum privacy | Ollama, vLLM, or llama.cpp (fully local) |
| Enterprise / Azure | Azure OpenAI with custom endpoint |
| Chinese AI models | z.ai (GLM), Kimi/Moonshot (kimi-codingorkimi-coding-cn), MiniMax, Xiaomi MiMo, or Tencent TokenHub (first-class providers) |

`sort: "price"`
`kimi-coding`
`kimi-coding-cn`

You can switch between providers at any time withhermes model— no restart required. Your conversation history, memory, and skills carry over regardless of which provider you use.

`hermes model`

## Optional API Keys​

| Feature | Provider | Env Variable |
| --- | --- | --- |
| Web scraping | Firecrawl | FIRECRAWL_API_KEY,FIRECRAWL_API_URL |
| Browser automation | Browserbase | BROWSERBASE_API_KEY,BROWSERBASE_PROJECT_ID |
| Image generation | FAL | FAL_KEY |
| Premium TTS voices | ElevenLabs | ELEVENLABS_API_KEY |
| OpenAI TTS + voice transcription | OpenAI | VOICE_TOOLS_OPENAI_KEY |
| Mistral TTS + voice transcription | Mistral | MISTRAL_API_KEY |
| Cross-session user modeling | Honcho | HONCHO_API_KEY |
| Semantic long-term memory | Supermemory | SUPERMEMORY_API_KEY |

`FIRECRAWL_API_KEY`
`FIRECRAWL_API_URL`
`BROWSERBASE_API_KEY`
`BROWSERBASE_PROJECT_ID`
`FAL_KEY`
`ELEVENLABS_API_KEY`
`VOICE_TOOLS_OPENAI_KEY`
`MISTRAL_API_KEY`
`HONCHO_API_KEY`
`SUPERMEMORY_API_KEY`

### Self-Hosting Firecrawl​

By default, Hermes uses theFirecrawl cloud APIfor web search and scraping. If you prefer to run Firecrawl locally, you can point Hermes at a self-hosted instance instead. See Firecrawl'sSELF_HOST.mdfor complete setup instructions.

What you get:No API key required, no rate limits, no per-page costs, full data sovereignty.

What you lose:The cloud version uses Firecrawl's proprietary "Fire-engine" for advanced anti-bot bypassing (Cloudflare, CAPTCHAs, IP rotation). Self-hosted uses basic fetch + Playwright, so some protected sites may fail. Search uses DuckDuckGo instead of Google.

Setup:

1. Clone and start the Firecrawl Docker stack (5 containers: API, Playwright, Redis, RabbitMQ, PostgreSQL — requires ~4-8 GB RAM):gitclone https://github.com/firecrawl/firecrawlcdfirecrawl# In .env, set: USE_DB_AUTHENTICATION=false, HOST=0.0.0.0, PORT=3002dockercompose up-d
2. Point Hermes at your instance (no API key needed):hermes configsetFIRECRAWL_API_URL http://localhost:3002

Clone and start the Firecrawl Docker stack (5 containers: API, Playwright, Redis, RabbitMQ, PostgreSQL — requires ~4-8 GB RAM):

```
git clone https://github.com/firecrawl/firecrawlcd firecrawl# In .env, set: USE_DB_AUTHENTICATION=false, HOST=0.0.0.0, PORT=3002docker compose up -d
```

Point Hermes at your instance (no API key needed):

```
hermes config set FIRECRAWL_API_URL http://localhost:3002
```

You can also set bothFIRECRAWL_API_KEYandFIRECRAWL_API_URLif your self-hosted instance has authentication enabled.

`FIRECRAWL_API_KEY`
`FIRECRAWL_API_URL`

## OpenRouter Provider Routing​

When using OpenRouter, you can control how requests are routed across providers. Add aprovider_routingsection to~/.hermes/config.yaml:

`provider_routing`
`~/.hermes/config.yaml`

```
provider_routing:  sort: "throughput"          # "price" (default), "throughput", or "latency"  # only: ["anthropic"]      # Only use these providers  # ignore: ["deepinfra"]    # Skip these providers  # order: ["anthropic", "google"]  # Try providers in this order  # require_parameters: true  # Only use providers that support all request params  # data_collection: "deny"   # Exclude providers that may store/train on data
```

Shortcuts:Append:nitroto any model name for throughput sorting (e.g.,anthropic/claude-sonnet-4:nitro), or:floorfor price sorting.

`:nitro`
`anthropic/claude-sonnet-4:nitro`
`:floor`

## OpenRouter Pareto Code Router​

OpenRouter ships an experimental coding-model router atopenrouter/pareto-codethat auto-routes requests to the cheapest model meeting a coding-quality bar (ranked byArtificial Analysis). Pick this model and tune themin_coding_scoreknob in~/.hermes/config.yaml:

`openrouter/pareto-code`
`min_coding_score`
`~/.hermes/config.yaml`

```
model:  provider: openrouter  model: openrouter/pareto-codeopenrouter:  min_coding_score: 0.65   # 0.0–1.0; higher = stronger (more expensive) coders. Default 0.65.
```

Notes:

- min_coding_scoreisonlysent whenmodel.modelisopenrouter/pareto-code. On any other model the value is a no-op.
- Set to empty string (or remove the line) to let OpenRouter pick the strongest available coder — its documented behavior when the plugins block is omitted.
- Selection is deterministic per score on a given day, but the actual model chosen can shift as the Pareto frontier moves (new models, benchmark updates).
- See OpenRouter'sPareto Router docsfor the full router behavior.
- To use the Pareto Code router for a specificauxiliary task(compression, vision, etc.) instead of the main agent, setextra_body.pluginsunder that task — seeAuxiliary Models → OpenRouter routing & Pareto Code for auxiliary tasks.

`min_coding_score`
`model.model`
`openrouter/pareto-code`
`extra_body.plugins`

## Fallback Providers​

Configure a chain of backup providers Hermes tries in order when the primary model fails (rate limits, server errors, auth failures). The canonical format is a top-levelfallback_providers:list:

`fallback_providers:`

```
fallback_providers:  - provider: openrouter    model: anthropic/claude-sonnet-4  - provider: anthropic    model: claude-sonnet-4    # base_url: http://localhost:8000/v1    # optional, for custom endpoints    # api_mode: chat_completions           # optional override
```

The legacy single-pairfallback_model:dict is still accepted for back-compat:

`fallback_model:`

```
fallback_model:  provider: openrouter  model: anthropic/claude-sonnet-4
```

When activated, the fallback swaps the model and provider mid-session without losing your conversation. The chain is tried entry-by-entry; activation is one-shot per session.

Supported providers:openrouter,nous,novita,openai-codex,copilot,copilot-acp,anthropic,gemini,qwen-oauth,huggingface,zai,kimi-coding,kimi-coding-cn,minimax,minimax-cn,minimax-oauth,deepseek,nvidia,xai,xai-oauth,ollama-cloud,bedrock,azure-foundry,opencode-zen,opencode-go,kilocode,xiaomi,arcee,gmi,stepfun,lmstudio,alibaba,alibaba-coding-plan,tencent-tokenhub,custom.

`openrouter`
`nous`
`novita`
`openai-codex`
`copilot`
`copilot-acp`
`anthropic`
`gemini`
`qwen-oauth`
`huggingface`
`zai`
`kimi-coding`
`kimi-coding-cn`
`minimax`
`minimax-cn`
`minimax-oauth`
`deepseek`
`nvidia`
`xai`
`xai-oauth`
`ollama-cloud`
`bedrock`
`azure-foundry`
`opencode-zen`
`opencode-go`
`kilocode`
`xiaomi`
`arcee`
`gmi`
`stepfun`
`lmstudio`
`alibaba`
`alibaba-coding-plan`
`tencent-tokenhub`
`custom`

Fallback is configured exclusively throughconfig.yaml— or interactively viahermes fallback. For full details on when it triggers, how the chain advances, and how it interacts with auxiliary tasks and delegation, seeFallback Providers.

`config.yaml`
`hermes fallback`

## See Also​

- Configuration— General configuration (directory structure, config precedence, terminal backends, memory, compression, and more)
- Environment Variables— Complete reference of all environment variables