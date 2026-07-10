---
layout: docs
title: "متغیرهای محیطی"
permalink: /docs/reference/environment-variables/
---

- 
- Reference
- Configuration Reference
- Environment Variables

# Environment Variables Reference

Hermes reads environment variables from the process environment and, for user-managed secrets, from~/.hermes/.env. Keep API keys, bot tokens, OAuth secrets, and other credentials in.env; preferconfig.yamlfor non-secret behaviour settings when a config key exists. Some variables below are process-only overrides or internal bridge variables and should not be committed to.envjust because they are documented here.

`~/.hermes/.env`
`.env`
`config.yaml`
`.env`

## LLM Providers​

| Variable | Description |
| --- | --- |
| OPENROUTER_API_KEY | OpenRouter API key (recommended for flexibility) |
| OPENROUTER_BASE_URL | Override the OpenRouter-compatible base URL |
| HERMES_OPENROUTER_CACHE | Enable OpenRouter response caching (1/true/yes/on). Overridesopenrouter.response_cachein config.yaml. SeeResponse Caching. |
| HERMES_OPENROUTER_CACHE_TTL | Cache TTL in seconds (1-86400). Overridesopenrouter.response_cache_ttlin config.yaml. |
| NOUS_BASE_URL | Override Nous Portal base URL (rarely needed; development/testing only) |
| NOUS_INFERENCE_BASE_URL | Override Nous inference endpoint directly |
| OPENAI_API_KEY | API key for custom OpenAI-compatible endpoints (used withOPENAI_BASE_URL) |
| OPENAI_BASE_URL | Base URL for custom endpoint (VLLM, SGLang, etc.) |
| LM_API_KEY | API key for LM Studio (lmstudioprovider). Often a placeholder for local servers |
| LM_BASE_URL | LM Studio base URL (default:http://localhost:1234/v1) |
| COPILOT_GITHUB_TOKEN | GitHub token for Copilot API — first priority (OAuthgho_*or fine-grained PATgithub_pat_*; classic PATsghp_*arenot supported) |
| GH_TOKEN | GitHub token — second priority for Copilot (also used byghCLI) |
| GITHUB_TOKEN | GitHub token — third priority for Copilot |
| HERMES_COPILOT_ACP_COMMAND | Override Copilot ACP CLI binary path (default:copilot) |
| COPILOT_CLI_PATH | Alias forHERMES_COPILOT_ACP_COMMAND |
| HERMES_COPILOT_ACP_ARGS | Override Copilot ACP arguments (default:--acp --stdio) |
| COPILOT_ACP_BASE_URL | Override Copilot ACP base URL |
| COPILOT_API_BASE_URL | Override the Copilot API base URL (copilotprovider) |
| GLM_API_KEY | z.ai / ZhipuAI GLM API key (z.ai) |
| ZAI_API_KEY | Alias forGLM_API_KEY |
| Z_AI_API_KEY | Alias forGLM_API_KEY |
| GLM_BASE_URL | Override z.ai base URL (default:https://api.z.ai/api/paas/v4) |
| KIMI_API_KEY | Kimi / Moonshot AI API key (moonshot.ai) |
| KIMI_CODING_API_KEY | Alias key for thekimi-codingprovider (accepted alongsideKIMI_API_KEY) |
| KIMI_BASE_URL | Override Kimi base URL (default:https://api.moonshot.ai/v1) |
| KIMI_CN_API_KEY | Kimi / Moonshot China API key (moonshot.cn) |
| ARCEEAI_API_KEY | Arcee AI API key (chat.arcee.ai) |
| ARCEE_BASE_URL | Override Arcee base URL (default:https://api.arcee.ai/api/v1) |
| GMI_API_KEY | GMI Cloud API key (gmicloud.ai) |
| GMI_BASE_URL | Override GMI Cloud base URL (default:https://api.gmi-serving.com/v1) |
| MINIMAX_API_KEY | MiniMax API key — global endpoint (minimax.io).Not used byminimax-oauth(OAuth path uses browser login instead). |
| MINIMAX_BASE_URL | Override MiniMax base URL (default:https://api.minimax.io/anthropic— Hermes uses MiniMax's Anthropic Messages-compatible endpoint).Not used byminimax-oauth. |
| MINIMAX_CN_API_KEY | MiniMax API key — China endpoint (minimaxi.com).Not used byminimax-oauth(OAuth path uses browser login instead). |
| MINIMAX_CN_BASE_URL | Override MiniMax China base URL (default:https://api.minimaxi.com/anthropic).Not used byminimax-oauth. |
| KILOCODE_API_KEY | Kilo Code API key (kilo.ai) |
| KILOCODE_BASE_URL | Override Kilo Code base URL (default:https://api.kilo.ai/api/gateway) |
| XIAOMI_API_KEY | Xiaomi MiMo API key (platform.xiaomimimo.com) |
| XIAOMI_BASE_URL | Override Xiaomi MiMo base URL (default:https://api.xiaomimimo.com/v1) |
| TOKENHUB_API_KEY | Tencent TokenHub API key (tokenhub.tencentmaas.com) |
| TOKENHUB_BASE_URL | Override Tencent TokenHub base URL (default:https://tokenhub.tencentmaas.com/v1) |
| AZURE_FOUNDRY_API_KEY | Microsoft Foundry / Azure OpenAI API key (ai.azure.com). Not needed whenmodel.auth_mode: entra_id |
| AZURE_FOUNDRY_BASE_URL | Microsoft Foundry endpoint URL (e.g.https://<resource>.openai.azure.com/openai/v1for OpenAI-style, orhttps://<resource>.services.ai.azure.com/anthropicfor Anthropic-style) |
| AZURE_ANTHROPIC_KEY | Azure Anthropic API key forprovider: anthropic+base_urlpointing at a Microsoft Foundry Claude deployment (alternative toANTHROPIC_API_KEYwhen both Anthropic and Azure Anthropic are configured) |
| AZURE_TENANT_ID | Entra ID tenant ID (service-principal flows; honored byazure-identitywhenmodel.auth_mode: entra_id) |
| AZURE_CLIENT_ID | Entra ID client ID (service principal, workload identity, or user-assigned managed identity) |
| AZURE_CLIENT_SECRET | Service principal secret used byEnvironmentCredential |
| AZURE_CLIENT_CERTIFICATE_PATH | Service principal certificate (alternative toAZURE_CLIENT_SECRET) |
| AZURE_FEDERATED_TOKEN_FILE | Federated token file path for AKS Workload Identity / OIDC flows |
| AZURE_AUTHORITY_HOST | Sovereign-cloud authority override (e.g.https://login.microsoftonline.usfor Azure Government). SeeAzure Foundry guide |
| IDENTITY_ENDPOINT/MSI_ENDPOINT | Managed Identity endpoint for App Service, Functions, and Container Apps; VMs usually use IMDS instead and do not set these |
| HF_TOKEN | Hugging Face token for Inference Providers (huggingface.co/settings/tokens) |
| HF_BASE_URL | Override Hugging Face base URL (default:https://router.huggingface.co/v1) |
| GOOGLE_API_KEY | Google AI Studio API key (aistudio.google.com/app/apikey) |
| GEMINI_API_KEY | Alias forGOOGLE_API_KEY |
| GEMINI_BASE_URL | Override Google AI Studio base URL |
| ANTHROPIC_API_KEY | Anthropic Console API key (console.anthropic.com) |
| ANTHROPIC_BASE_URL | Override the Anthropic API base URL |
| ANTHROPIC_TOKEN | Manual or legacy Anthropic OAuth/setup-token override |
| DASHSCOPE_API_KEY | Qwen Cloud (Alibaba DashScope) API key for Qwen models (modelstudio.console.alibabacloud.com) |
| DASHSCOPE_BASE_URL | Custom DashScope base URL (default:https://dashscope-intl.aliyuncs.com/compatible-mode/v1; usehttps://dashscope.aliyuncs.com/compatible-mode/v1for mainland-China region) |
| ALIBABA_CODING_PLAN_API_KEY | Qwen Coding Plan API key (alibaba-coding-planprovider) |
| ALIBABA_CODING_PLAN_BASE_URL | Override the Qwen Coding Plan base URL |
| DEEPSEEK_API_KEY | DeepSeek API key for direct DeepSeek access (platform.deepseek.com) |
| DEEPSEEK_BASE_URL | Custom DeepSeek API base URL |
| NOVITA_API_KEY | NovitaAI API key — AI-native cloud for Model API, Agent Sandbox, and GPU Cloud (novita.ai/settings/key-management) |
| NOVITA_BASE_URL | Override NovitaAI base URL (default:https://api.novita.ai/openai/v1) |
| NVIDIA_API_KEY | NVIDIA NIM API key — Nemotron and open models (build.nvidia.com) |
| NVIDIA_BASE_URL | Override NVIDIA base URL (default:https://integrate.api.nvidia.com/v1; set tohttp://localhost:8000/v1for a local NIM endpoint) |
| STEPFUN_API_KEY | StepFun API key — Step-series models (platform.stepfun.com) |
| STEPFUN_BASE_URL | Override StepFun base URL (default:https://api.stepfun.com/v1) |
| OLLAMA_API_KEY | Ollama Cloud API key — managed Ollama catalog without local GPU (ollama.com/settings/keys) |
| OLLAMA_BASE_URL | Override Ollama Cloud base URL (default:https://ollama.com/v1) |
| XAI_API_KEY | xAI (Grok) API key for chat + TTS + web search (console.x.ai) |
| XAI_BASE_URL | Override xAI base URL (default:https://api.x.ai/v1) |
| MISTRAL_API_KEY | Mistral API key for Voxtral TTS and Voxtral STT (console.mistral.ai) |
| AWS_REGION | AWS region for Bedrock inference (e.g.us-east-1,eu-central-1). Read by boto3. |
| AWS_PROFILE | AWS named profile for Bedrock authentication (reads~/.aws/credentials). Leave unset to use default boto3 credential chain. |
| BEDROCK_BASE_URL | Override Bedrock runtime base URL (default:https://bedrock-runtime.us-east-1.amazonaws.com; usually leave unset and useAWS_REGIONinstead) |
| HERMES_QWEN_BASE_URL | Qwen Portal base URL override (default:https://portal.qwen.ai/v1) |
| OPENCODE_ZEN_API_KEY | OpenCode Zen API key — pay-as-you-go access to curated models (opencode.ai) |
| OPENCODE_ZEN_BASE_URL | Override OpenCode Zen base URL |
| OPENCODE_GO_API_KEY | OpenCode Go API key — $10/month subscription for open models (opencode.ai) |
| OPENCODE_GO_BASE_URL | Override OpenCode Go base URL |
| CLAUDE_CODE_OAUTH_TOKEN | Explicit Claude Code token override if you export one manually |
| HERMES_MODEL | Override model name at process level (used by cron scheduler; preferconfig.yamlfor normal use) |
| VOICE_TOOLS_OPENAI_KEY | Preferred OpenAI key for OpenAI speech-to-text and text-to-speech providers |
| HERMES_LOCAL_STT_COMMAND | Optional local speech-to-text command template. Supports{input_path},{output_dir},{language}, and{model}placeholders |
| HERMES_LOCAL_STT_LANGUAGE | Default language passed toHERMES_LOCAL_STT_COMMANDor auto-detected localwhisperCLI fallback (default:en) |
| HERMES_HOME | Override Hermes config directory (default:~/.hermes). Also scopes the gateway PID file and systemd service name, so multiple installations can run concurrently |
| HERMES_GIT_BASH_PATH | Windows only.Overridebash.exediscovery for the terminal tool. Points at any bash — full Git-for-Windows install, WSL bash via symlink, MSYS2, Cygwin. The installer sets this automatically to the PortableGit it provisioned. See theWindows (Native) Guide |
| HERMES_DISABLE_WINDOWS_UTF8 | Windows only.Set to1to disable the UTF-8 stdio shim (configure_windows_stdio()) and fall back to the console's locale code page. Useful for bisecting encoding bugs; rarely the right setting in normal operation |
| HERMES_KANBAN_HOME | Override the shared Hermes root that anchors the kanban board (db + workspaces + worker logs). Falls back toget_default_hermes_root()(the parent of any active profile). Useful for tests and unusual deployments |
| HERMES_KANBAN_BOARD | Pin the active kanban board for this process. Takes precedence over~/.hermes/kanban/current; the dispatcher injects this into worker subprocess env so workers physically cannot see tasks on other boards. Defaults todefault. Slug validation: lowercase alphanumerics + hyphens + underscores, 1-64 chars |
| HERMES_KANBAN_DB | Pin the kanban database file path directly (highest precedence; beatsHERMES_KANBAN_BOARDandHERMES_KANBAN_HOME). The dispatcher injects this into worker subprocess env so profile workers converge on the dispatcher's board |
| HERMES_KANBAN_WORKSPACES_ROOT | Pin the kanban workspaces root directly (highest precedence for workspaces; beatsHERMES_KANBAN_HOME). The dispatcher injects this into worker subprocess env |
| HERMES_KANBAN_DISPATCH_IN_GATEWAY | Runtime override forkanban.dispatch_in_gateway. Set to0,false,no, oroffto keep the gateway from starting the embedded Kanban dispatcher; any other non-empty value enables it. Useful when a separate dispatcher process owns the board. |

`OPENROUTER_API_KEY`
`OPENROUTER_BASE_URL`
`HERMES_OPENROUTER_CACHE`
`1`
`true`
`yes`
`on`
`openrouter.response_cache`
`HERMES_OPENROUTER_CACHE_TTL`
`openrouter.response_cache_ttl`
`NOUS_BASE_URL`
`NOUS_INFERENCE_BASE_URL`
`OPENAI_API_KEY`
`OPENAI_BASE_URL`
`OPENAI_BASE_URL`
`LM_API_KEY`
`lmstudio`
`LM_BASE_URL`
`http://localhost:1234/v1`
`COPILOT_GITHUB_TOKEN`
`gho_*`
`github_pat_*`
`ghp_*`
`GH_TOKEN`
`gh`
`GITHUB_TOKEN`
`HERMES_COPILOT_ACP_COMMAND`
`copilot`
`COPILOT_CLI_PATH`
`HERMES_COPILOT_ACP_COMMAND`
`HERMES_COPILOT_ACP_ARGS`
`--acp --stdio`
`COPILOT_ACP_BASE_URL`
`COPILOT_API_BASE_URL`
`copilot`
`GLM_API_KEY`
`ZAI_API_KEY`
`GLM_API_KEY`
`Z_AI_API_KEY`
`GLM_API_KEY`
`GLM_BASE_URL`
`https://api.z.ai/api/paas/v4`
`KIMI_API_KEY`
`KIMI_CODING_API_KEY`
`kimi-coding`
`KIMI_API_KEY`
`KIMI_BASE_URL`
`https://api.moonshot.ai/v1`
`KIMI_CN_API_KEY`
`ARCEEAI_API_KEY`
`ARCEE_BASE_URL`
`https://api.arcee.ai/api/v1`
`GMI_API_KEY`
`GMI_BASE_URL`
`https://api.gmi-serving.com/v1`
`MINIMAX_API_KEY`
`minimax-oauth`
`MINIMAX_BASE_URL`
`https://api.minimax.io/anthropic`
`minimax-oauth`
`MINIMAX_CN_API_KEY`
`minimax-oauth`
`MINIMAX_CN_BASE_URL`
`https://api.minimaxi.com/anthropic`
`minimax-oauth`
`KILOCODE_API_KEY`
`KILOCODE_BASE_URL`
`https://api.kilo.ai/api/gateway`
`XIAOMI_API_KEY`
`XIAOMI_BASE_URL`
`https://api.xiaomimimo.com/v1`
`TOKENHUB_API_KEY`
`TOKENHUB_BASE_URL`
`https://tokenhub.tencentmaas.com/v1`
`AZURE_FOUNDRY_API_KEY`
`model.auth_mode: entra_id`
`AZURE_FOUNDRY_BASE_URL`
`https://<resource>.openai.azure.com/openai/v1`
`https://<resource>.services.ai.azure.com/anthropic`
`AZURE_ANTHROPIC_KEY`
`provider: anthropic`
`base_url`
`ANTHROPIC_API_KEY`
`AZURE_TENANT_ID`
`azure-identity`
`model.auth_mode: entra_id`
`AZURE_CLIENT_ID`
`AZURE_CLIENT_SECRET`
`EnvironmentCredential`
`AZURE_CLIENT_CERTIFICATE_PATH`
`AZURE_CLIENT_SECRET`
`AZURE_FEDERATED_TOKEN_FILE`
`AZURE_AUTHORITY_HOST`
`https://login.microsoftonline.us`
`IDENTITY_ENDPOINT`
`MSI_ENDPOINT`
`HF_TOKEN`
`HF_BASE_URL`
`https://router.huggingface.co/v1`
`GOOGLE_API_KEY`
`GEMINI_API_KEY`
`GOOGLE_API_KEY`
`GEMINI_BASE_URL`
`ANTHROPIC_API_KEY`
`ANTHROPIC_BASE_URL`
`ANTHROPIC_TOKEN`
`DASHSCOPE_API_KEY`
`DASHSCOPE_BASE_URL`
`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
`https://dashscope.aliyuncs.com/compatible-mode/v1`
`ALIBABA_CODING_PLAN_API_KEY`
`alibaba-coding-plan`
`ALIBABA_CODING_PLAN_BASE_URL`
`DEEPSEEK_API_KEY`
`DEEPSEEK_BASE_URL`
`NOVITA_API_KEY`
`NOVITA_BASE_URL`
`https://api.novita.ai/openai/v1`
`NVIDIA_API_KEY`
`NVIDIA_BASE_URL`
`https://integrate.api.nvidia.com/v1`
`http://localhost:8000/v1`
`STEPFUN_API_KEY`
`STEPFUN_BASE_URL`
`https://api.stepfun.com/v1`
`OLLAMA_API_KEY`
`OLLAMA_BASE_URL`
`https://ollama.com/v1`
`XAI_API_KEY`
`XAI_BASE_URL`
`https://api.x.ai/v1`
`MISTRAL_API_KEY`
`AWS_REGION`
`us-east-1`
`eu-central-1`
`AWS_PROFILE`
`~/.aws/credentials`
`BEDROCK_BASE_URL`
`https://bedrock-runtime.us-east-1.amazonaws.com`
`AWS_REGION`
`HERMES_QWEN_BASE_URL`
`https://portal.qwen.ai/v1`
`OPENCODE_ZEN_API_KEY`
`OPENCODE_ZEN_BASE_URL`
`OPENCODE_GO_API_KEY`
`OPENCODE_GO_BASE_URL`
`CLAUDE_CODE_OAUTH_TOKEN`
`HERMES_MODEL`
`config.yaml`
`VOICE_TOOLS_OPENAI_KEY`
`HERMES_LOCAL_STT_COMMAND`
`{input_path}`
`{output_dir}`
`{language}`
`{model}`
`HERMES_LOCAL_STT_LANGUAGE`
`HERMES_LOCAL_STT_COMMAND`
`whisper`
`en`
`HERMES_HOME`
`~/.hermes`
`HERMES_GIT_BASH_PATH`
`bash.exe`
`HERMES_DISABLE_WINDOWS_UTF8`
`1`
`configure_windows_stdio()`
`HERMES_KANBAN_HOME`
`get_default_hermes_root()`
`HERMES_KANBAN_BOARD`
`~/.hermes/kanban/current`
`default`
`HERMES_KANBAN_DB`
`HERMES_KANBAN_BOARD`
`HERMES_KANBAN_HOME`
`HERMES_KANBAN_WORKSPACES_ROOT`
`HERMES_KANBAN_HOME`
`HERMES_KANBAN_DISPATCH_IN_GATEWAY`
`kanban.dispatch_in_gateway`
`0`
`false`
`no`
`off`

## Provider Auth (OAuth)​

For native Anthropic auth, Hermes prefers Claude Code's own credential files when they exist because those credentials can refresh automatically.OAuth against Anthropic requires a Claude Max plan with purchased extra usage credits— Hermes routes as Claude Code, which only draws from the Max plan's extra/overage credits, not the base Max allowance, and does not work on Claude Pro. Without Max + extra credits, use an API key instead. Environment variables such asANTHROPIC_TOKENremain useful as manual overrides, but they are no longer the preferred path for Claude Max login.

`ANTHROPIC_TOKEN`
| Variable | Description |
| --- | --- |
| HERMES_PORTAL_BASE_URL | Override Nous Portal URL (for development/testing) |
| NOUS_INFERENCE_BASE_URL | Override Nous inference API URL |
| HERMES_NOUS_MIN_KEY_TTL_SECONDS | Min agent key TTL before re-mint (default: 1800 = 30min) |
| HERMES_NOUS_TIMEOUT_SECONDS | HTTP timeout for Nous credential / token flows |
| HERMES_DUMP_REQUESTS | Dump API request payloads to log files (true/false) |
| HERMES_PREFILL_MESSAGES_FILE | Path to a JSON file of ephemeral prefill messages injected at API-call time |
| HERMES_TIMEZONE | IANA timezone override (for exampleAmerica/New_York) |

`HERMES_PORTAL_BASE_URL`
`NOUS_INFERENCE_BASE_URL`
`HERMES_NOUS_MIN_KEY_TTL_SECONDS`
`HERMES_NOUS_TIMEOUT_SECONDS`
`HERMES_DUMP_REQUESTS`
`true`
`false`
`HERMES_PREFILL_MESSAGES_FILE`
`HERMES_TIMEZONE`
`America/New_York`

## Tool APIs​

| Variable | Description |
| --- | --- |
| PARALLEL_API_KEY | AI-native web search (parallel.ai) |
| FIRECRAWL_API_KEY | Web scraping and cloud browser (firecrawl.dev) |
| FIRECRAWL_API_URL | Custom Firecrawl API endpoint for self-hosted instances (optional) |
| TAVILY_API_KEY | Tavily API key for AI-native web search, extract, and crawl (app.tavily.com) |
| SEARXNG_URL | SearXNG instance URL for free self-hosted web search — no API key required (searxng.github.io) |
| TAVILY_BASE_URL | Override the Tavily API endpoint. Useful for corporate proxies and self-hosted Tavily-compatible search backends. Same pattern asGROQ_BASE_URL. |
| EXA_API_KEY | Exa API key for AI-native web search and contents (exa.ai) |
| BRAVE_SEARCH_API_KEY | Brave Search API subscription token for web search (free tier available) (brave.com/search/api) |
| BROWSERBASE_API_KEY | Browser automation (browserbase.com) |
| BROWSERBASE_PROJECT_ID | Browserbase project ID |
| BROWSER_USE_API_KEY | Browser Use cloud browser API key (browser-use.com) |
| FIRECRAWL_BROWSER_TTL | Firecrawl browser session TTL in seconds (default: 300) |
| BROWSER_CDP_URL | Chrome DevTools Protocol URL for local browser (set via/browser connect, e.g.ws://localhost:9222) |
| CAMOFOX_URL | Camofox local anti-detection browser URL (default:http://localhost:9377) |
| CAMOFOX_USER_ID | Optional externally managed Camofox user ID for shared visible sessions |
| CAMOFOX_SESSION_KEY | Optional Camofox session key used when creating tabs forCAMOFOX_USER_ID |
| CAMOFOX_ADOPT_EXISTING_TAB | Set totrueto reuse an existing Camofox tab before creating a new one |
| BROWSER_INACTIVITY_TIMEOUT | Browser session inactivity timeout in seconds |
| AGENT_BROWSER_ARGS | Extra Chromium launch flags (comma- or newline-separated). Hermes auto-injects--no-sandbox,--disable-dev-shm-usagewhen running as root or on AppArmor-restricted unprivileged user namespaces (Ubuntu 23.10+, DGX Spark, many container images); set this manually only to override or add other flags. |
| AGENT_BROWSER_ENGINE | Browser engine for local mode:auto(default — Chromium-family via CDP), or a specific engine override. |
| FAL_KEY | Image generation (fal.ai) |
| KREA_API_KEY | Krea API key for Krea 2 image generation (krea.ai) |
| GROQ_API_KEY | Groq Whisper STT API key (groq.com) |
| ELEVENLABS_API_KEY | ElevenLabs premium TTS voices (elevenlabs.io) |
| STT_GROQ_MODEL | Override the Groq STT model (default:whisper-large-v3-turbo) |
| GROQ_BASE_URL | Override the Groq OpenAI-compatible STT endpoint |
| STT_OPENAI_MODEL | Override the OpenAI STT model (default:whisper-1) |
| STT_OPENAI_BASE_URL | Override the OpenAI-compatible STT endpoint |
| GITHUB_TOKEN | GitHub token for Skills Hub (higher API rate limits, skill publish) |
| HONCHO_API_KEY | Cross-session user modeling (honcho.dev) |
| HONCHO_BASE_URL | Base URL for self-hosted Honcho instances (default: Honcho cloud). No API key required for local instances |
| HINDSIGHT_TIMEOUT | Timeout in seconds for Hindsight memory-provider API calls (default:60). Bump this if your Hindsight instance is slow to respond during/syncoron_session_switchand you're seeing timeouts inerrors.log. |
| SUPERMEMORY_API_KEY | Semantic long-term memory with profile recall and session ingest (supermemory.ai) |
| DAYTONA_API_KEY | Daytona cloud sandboxes (daytona.io) |

`PARALLEL_API_KEY`
`FIRECRAWL_API_KEY`
`FIRECRAWL_API_URL`
`TAVILY_API_KEY`
`SEARXNG_URL`
`TAVILY_BASE_URL`
`GROQ_BASE_URL`
`EXA_API_KEY`
`BRAVE_SEARCH_API_KEY`
`BROWSERBASE_API_KEY`
`BROWSERBASE_PROJECT_ID`
`BROWSER_USE_API_KEY`
`FIRECRAWL_BROWSER_TTL`
`BROWSER_CDP_URL`
`/browser connect`
`ws://localhost:9222`
`CAMOFOX_URL`
`http://localhost:9377`
`CAMOFOX_USER_ID`
`CAMOFOX_SESSION_KEY`
`CAMOFOX_USER_ID`
`CAMOFOX_ADOPT_EXISTING_TAB`
`true`
`BROWSER_INACTIVITY_TIMEOUT`
`AGENT_BROWSER_ARGS`
`--no-sandbox,--disable-dev-shm-usage`
`AGENT_BROWSER_ENGINE`
`auto`
`FAL_KEY`
`KREA_API_KEY`
`GROQ_API_KEY`
`ELEVENLABS_API_KEY`
`STT_GROQ_MODEL`
`whisper-large-v3-turbo`
`GROQ_BASE_URL`
`STT_OPENAI_MODEL`
`whisper-1`
`STT_OPENAI_BASE_URL`
`GITHUB_TOKEN`
`HONCHO_API_KEY`
`HONCHO_BASE_URL`
`HINDSIGHT_TIMEOUT`
`60`
`/sync`
`on_session_switch`
`errors.log`
`SUPERMEMORY_API_KEY`
`DAYTONA_API_KEY`

### Skill API Keys​

Secrets consumed by specific bundled / optional skills. Each is only needed if you use the corresponding skill.

| Variable | Used by skill | Description |
| --- | --- | --- |
| NOTION_API_KEY | notion | Notion integration token. |
| LINEAR_API_KEY | linear | Linear personal API key. |
| AIRTABLE_API_KEY | airtable | Airtable personal access token. |
| TENOR_API_KEY | gif-search | Tenor API key for GIF search. |

`NOTION_API_KEY`
`notion`
`LINEAR_API_KEY`
`linear`
`AIRTABLE_API_KEY`
`airtable`
`TENOR_API_KEY`
`gif-search`

### Langfuse Observability​

Environment variables for the bundledobservability/langfuseplugin. Set these in~/.hermes/.env. The plugin must also be enabled (hermes plugins enable observability/langfuse, or check the box inhermes plugins) before any of these take effect.

`observability/langfuse`
`~/.hermes/.env`
`hermes plugins enable observability/langfuse`
`hermes plugins`
| Variable | Description |
| --- | --- |
| HERMES_LANGFUSE_PUBLIC_KEY | Langfuse project public key (pk-lf-...). Required. |
| HERMES_LANGFUSE_SECRET_KEY | Langfuse project secret key (sk-lf-...). Required. |
| HERMES_LANGFUSE_BASE_URL | Langfuse server URL (default:https://cloud.langfuse.com). Set for self-hosted. |
| HERMES_LANGFUSE_ENV | Environment tag on traces (production,staging, …) |
| HERMES_LANGFUSE_RELEASE | Release/version tag on traces |
| HERMES_LANGFUSE_SAMPLE_RATE | SDK sampling rate 0.0–1.0 (default:1.0) |
| HERMES_LANGFUSE_MAX_CHARS | Per-field truncation for serialized payloads (default:12000) |
| HERMES_LANGFUSE_DEBUG | trueenables verbose plugin logging toagent.log |
| LANGFUSE_PUBLIC_KEY/LANGFUSE_SECRET_KEY/LANGFUSE_BASE_URL | Standard Langfuse SDK names. Accepted as fallbacks when theHERMES_LANGFUSE_*equivalents are unset. |

`HERMES_LANGFUSE_PUBLIC_KEY`
`pk-lf-...`
`HERMES_LANGFUSE_SECRET_KEY`
`sk-lf-...`
`HERMES_LANGFUSE_BASE_URL`
`https://cloud.langfuse.com`
`HERMES_LANGFUSE_ENV`
`production`
`staging`
`HERMES_LANGFUSE_RELEASE`
`HERMES_LANGFUSE_SAMPLE_RATE`
`1.0`
`HERMES_LANGFUSE_MAX_CHARS`
`12000`
`HERMES_LANGFUSE_DEBUG`
`true`
`agent.log`
`LANGFUSE_PUBLIC_KEY`
`LANGFUSE_SECRET_KEY`
`LANGFUSE_BASE_URL`
`HERMES_LANGFUSE_*`

### Nous Tool Gateway​

These variables configure theTool Gatewayfor paid Nous subscribers or self-hosted gateway deployments. Most users don't need to set these — the gateway is configured automatically viahermes modelorhermes tools.

`hermes model`
`hermes tools`
| Variable | Description |
| --- | --- |
| TOOL_GATEWAY_DOMAIN | Base domain for Tool Gateway routing (default:nousresearch.com) |
| TOOL_GATEWAY_SCHEME | HTTP or HTTPS scheme for gateway URLs (default:https) |
| TOOL_GATEWAY_USER_TOKEN | Auth token for the Tool Gateway (normally auto-populated from Nous auth) |
| FIRECRAWL_GATEWAY_URL | Override URL for the Firecrawl gateway endpoint specifically |

`TOOL_GATEWAY_DOMAIN`
`nousresearch.com`
`TOOL_GATEWAY_SCHEME`
`https`
`TOOL_GATEWAY_USER_TOKEN`
`FIRECRAWL_GATEWAY_URL`

## Terminal Backend​

| Variable | Description |
| --- | --- |
| TERMINAL_ENV | Backend:local,docker,ssh,singularity,modal,daytona |
| HERMES_DOCKER_BINARY | Override the container binary Hermes shells out to (e.g.podman,/usr/local/bin/docker). When unset, Hermes auto-discoversdockerorpodmanonPATH. Needed when both are installed and you want the non-default, or when the binary lives outsidePATH. |
| TERMINAL_DOCKER_IMAGE | Docker image (default:nikolaik/python-nodejs:python3.11-nodejs20) |
| TERMINAL_DOCKER_FORWARD_ENV | JSON array of env var names to explicitly forward into Docker terminal sessions. Note: skill-declaredrequired_environment_variablesare forwarded automatically — you only need this for vars not declared by any skill. |
| TERMINAL_DOCKER_VOLUMES | Additional Docker volume mounts (comma-separatedhost:containerpairs) |
| TERMINAL_DOCKER_MOUNT_CWD_TO_WORKSPACE | Advanced opt-in: mount the launch cwd into Docker/workspace(true/false, default:false) |
| TERMINAL_SINGULARITY_IMAGE | Singularity image or.sifpath |
| TERMINAL_MODAL_IMAGE | Modal container image |
| TERMINAL_DAYTONA_IMAGE | Daytona sandbox image |
| TERMINAL_TIMEOUT | Command timeout in seconds |
| TERMINAL_LIFETIME_SECONDS | Max lifetime for terminal sessions in seconds |
| TERMINAL_CWD | Deprecated direct override for gateway/cron terminal sessions. Preferterminal.cwdinconfig.yaml; CLI still uses the launch directory. |
| SUDO_PASSWORD | Enable sudo without interactive prompt |

`TERMINAL_ENV`
`local`
`docker`
`ssh`
`singularity`
`modal`
`daytona`
`HERMES_DOCKER_BINARY`
`podman`
`/usr/local/bin/docker`
`docker`
`podman`
`PATH`
`PATH`
`TERMINAL_DOCKER_IMAGE`
`nikolaik/python-nodejs:python3.11-nodejs20`
`TERMINAL_DOCKER_FORWARD_ENV`
`required_environment_variables`
`TERMINAL_DOCKER_VOLUMES`
`host:container`
`TERMINAL_DOCKER_MOUNT_CWD_TO_WORKSPACE`
`/workspace`
`true`
`false`
`false`
`TERMINAL_SINGULARITY_IMAGE`
`.sif`
`TERMINAL_MODAL_IMAGE`
`TERMINAL_DAYTONA_IMAGE`
`TERMINAL_TIMEOUT`
`TERMINAL_LIFETIME_SECONDS`
`TERMINAL_CWD`
`terminal.cwd`
`config.yaml`
`SUDO_PASSWORD`

For cloud sandbox backends, persistence is filesystem-oriented.TERMINAL_LIFETIME_SECONDScontrols when Hermes cleans up an idle terminal session, and later resumes may recreate the sandbox rather than keep the same live processes running.

`TERMINAL_LIFETIME_SECONDS`

## SSH Backend​

| Variable | Description |
| --- | --- |
| TERMINAL_SSH_HOST | Remote server hostname |
| TERMINAL_SSH_USER | SSH username |
| TERMINAL_SSH_PORT | SSH port (default: 22) |
| TERMINAL_SSH_KEY | Path to private key |
| TERMINAL_SSH_PERSISTENT | Override persistent shell for SSH (default: followsTERMINAL_PERSISTENT_SHELL) |

`TERMINAL_SSH_HOST`
`TERMINAL_SSH_USER`
`TERMINAL_SSH_PORT`
`TERMINAL_SSH_KEY`
`TERMINAL_SSH_PERSISTENT`
`TERMINAL_PERSISTENT_SHELL`

## Container Resources (Docker, Singularity, Modal, Daytona)​

| Variable | Description |
| --- | --- |
| TERMINAL_CONTAINER_CPU | CPU cores (default: 1) |
| TERMINAL_CONTAINER_MEMORY | Memory in MB (default: 5120) |
| TERMINAL_CONTAINER_DISK | Disk in MB (default: 51200) |
| TERMINAL_CONTAINER_PERSISTENT | Persist container filesystem across sessions (default:true) |
| TERMINAL_SANDBOX_DIR | Host directory for workspaces and overlays (default:~/.hermes/sandboxes/) |

`TERMINAL_CONTAINER_CPU`
`TERMINAL_CONTAINER_MEMORY`
`TERMINAL_CONTAINER_DISK`
`TERMINAL_CONTAINER_PERSISTENT`
`true`
`TERMINAL_SANDBOX_DIR`
`~/.hermes/sandboxes/`

## Persistent Shell​

| Variable | Description |
| --- | --- |
| TERMINAL_PERSISTENT_SHELL | Enable persistent shell for non-local backends (default:true). Also settable viaterminal.persistent_shellin config.yaml |
| TERMINAL_LOCAL_PERSISTENT | Enable persistent shell for local backend (default:false) |
| TERMINAL_SSH_PERSISTENT | Override persistent shell for SSH backend (default: followsTERMINAL_PERSISTENT_SHELL) |

`TERMINAL_PERSISTENT_SHELL`
`true`
`terminal.persistent_shell`
`TERMINAL_LOCAL_PERSISTENT`
`false`
`TERMINAL_SSH_PERSISTENT`
`TERMINAL_PERSISTENT_SHELL`

## Messaging​

| Variable | Description |
| --- | --- |
| TELEGRAM_BOT_TOKEN | Telegram bot token (from @BotFather) |
| TELEGRAM_ALLOWED_USERS | Comma-separated user IDs allowed to use the bot (applies to DMs, groups, and forums) |
| TELEGRAM_ALLOW_ALL_USERS | Allow any Telegram user to trigger the bot (dev only). |
| TELEGRAM_GROUP_ALLOWED_USERS | Comma-separated sender user IDs authorized in groups/forums only (does NOT grant DM access). Chat-ID-shaped values (starting with-) are still honored as chat IDs for backward compat with pre-#17686 configs, with a deprecation warning. |
| TELEGRAM_GROUP_ALLOWED_CHATS | Comma-separated group/forum chat IDs; any member is authorized |
| TELEGRAM_HOME_CHANNEL | Default Telegram chat/channel for cron delivery |
| TELEGRAM_HOME_CHANNEL_NAME | Display name for the Telegram home channel |
| TELEGRAM_CRON_THREAD_ID | Forum topic ID to receive cron deliveries; overridesTELEGRAM_HOME_CHANNEL_THREAD_IDfor cron only. Use in topic mode so replies to cron messages open a new session instead of hitting the system lobby (#24409). |
| TELEGRAM_WEBHOOK_URL | Public HTTPS URL for webhook mode (enables webhook instead of polling) |
| TELEGRAM_WEBHOOK_PORT | Local listen port for webhook server (default:8443) |
| TELEGRAM_WEBHOOK_SECRET | Secret token Telegram echoes back in each update for verification.Required wheneverTELEGRAM_WEBHOOK_URLis set— the gateway refuses to start without it (GHSA-3vpc-7q5r-276h). Generate withopenssl rand -hex 32. |
| TELEGRAM_REACTIONS | Enable emoji reactions on messages during processing (default:false) |
| TELEGRAM_REQUIRE_MENTION | Require an explicit trigger before responding in Telegram groups. Equivalent totelegram.require_mentioninconfig.yaml. |
| TELEGRAM_MENTION_PATTERNS | JSON array, newline-separated list, or comma-separated list of regex wake-word patterns accepted when Telegram group mention gating is enabled. Equivalent totelegram.mention_patterns. |
| TELEGRAM_EXCLUSIVE_BOT_MENTIONS | When enabled, explicit@...botmentions in Telegram groups route only to the mentioned bot usernames before reply or wake-word fallbacks run. Default:true. Equivalent totelegram.exclusive_bot_mentions. |
| TELEGRAM_REPLY_TO_MODE | Reply-reference behavior:off,first(default), orall. Matches the Discord pattern. |
| TELEGRAM_IGNORED_THREADS | Comma-separated Telegram forum topic/thread IDs where the bot never responds |
| TELEGRAM_PROXY | Proxy URL for Telegram connections — overridesHTTPS_PROXY. Supportshttp://,https://,socks5:// |
| DISCORD_BOT_TOKEN | Discord bot token |
| DISCORD_ALLOWED_USERS | Comma-separated Discord user IDs allowed to use the bot |
| DISCORD_ALLOW_ALL_USERS | Allow any Discord user to trigger the bot (dev only). |
| DISCORD_ALLOWED_ROLES | Comma-separated Discord role IDs allowed to use the bot (OR withDISCORD_ALLOWED_USERS). Auto-enables the Members intent. Useful when moderation teams churn — role grants propagate automatically. |
| DISCORD_ALLOWED_CHANNELS | Comma-separated Discord channel IDs. When set, the bot only responds in these channels (plus DMs if allowed). Overridesconfig.yamldiscord.allowed_channels. |
| DISCORD_PROXY | Proxy URL for Discord connections — overridesHTTPS_PROXY. Supportshttp://,https://,socks5:// |
| DISCORD_HOME_CHANNEL | Default Discord channel for cron delivery |
| DISCORD_HOME_CHANNEL_NAME | Display name for the Discord home channel |
| DISCORD_COMMAND_SYNC_POLICY | Discord slash-command startup sync policy:safe(diff and reconcile),bulk(legacytree.sync()), oroff |
| DISCORD_REQUIRE_MENTION | Require an @mention before responding in server channels |
| DISCORD_FREE_RESPONSE_CHANNELS | Comma-separated channel IDs where mention is not required |
| DISCORD_AUTO_THREAD | Auto-thread long replies when supported |
| DISCORD_ALLOW_ANY_ATTACHMENT | Whentrue, accept attachments of any file type (not just the built-in PDF/text/zip/office allowlist). Unknown types are cached and surfaced to the agent as a local path so it can inspect them viaterminal/read_file/ffprobe. Defaultfalse. |
| DISCORD_MAX_ATTACHMENT_BYTES | Maximum bytes per attachment the gateway will cache. Default33554432(32 MiB). Set to0for no cap (attachments are held in memory while being written). |
| DISCORD_REACTIONS | Enable emoji reactions on messages during processing (default:true) |
| DISCORD_IGNORED_CHANNELS | Comma-separated channel IDs where the bot never responds |
| DISCORD_NO_THREAD_CHANNELS | Comma-separated channel IDs where bot responds without auto-threading |
| DISCORD_REPLY_TO_MODE | Reply-reference behavior:off,first(default), orall |
| DISCORD_ALLOW_MENTION_EVERYONE | Allow the bot to ping@everyone/@here(default:false). SeeMention Control. |
| DISCORD_ALLOW_MENTION_ROLES | Allow the bot to ping@rolementions (default:false). |
| DISCORD_ALLOW_MENTION_USERS | Allow the bot to ping individual@usermentions (default:true). |
| DISCORD_ALLOW_MENTION_REPLIED_USER | Ping the author when replying to their message (default:true). |
| SLACK_BOT_TOKEN | Slack bot token (xoxb-...) |
| SLACK_APP_TOKEN | Slack app-level token (xapp-..., required for Socket Mode) |
| SLACK_ALLOWED_USERS | Comma-separated Slack user IDs |
| SLACK_ALLOW_ALL_USERS | Allow any Slack user to trigger the bot (dev only). |
| SLACK_HOME_CHANNEL | Default Slack channel for cron delivery |
| SLACK_HOME_CHANNEL_NAME | Display name for the Slack home channel |
| GOOGLE_CHAT_PROJECT_ID | GCP project hosting the Pub/Sub topic (falls back toGOOGLE_CLOUD_PROJECT) |
| GOOGLE_CHAT_SUBSCRIPTION_NAME | Full Pub/Sub subscription path,projects/{proj}/subscriptions/{sub}(legacy alias:GOOGLE_CHAT_SUBSCRIPTION) |
| GOOGLE_CHAT_SERVICE_ACCOUNT_JSON | Path to Service Account JSON, or the JSON inline (falls back toGOOGLE_APPLICATION_CREDENTIALS) |
| GOOGLE_CHAT_ALLOWED_USERS | Comma-separated user emails allowed to chat with the bot |
| GOOGLE_CHAT_ALLOW_ALL_USERS | Allow any Google Chat user to trigger the bot (dev only) |
| GOOGLE_CHAT_HOME_CHANNEL | Default space (e.g.spaces/AAAA...) for cron delivery |
| GOOGLE_CHAT_HOME_CHANNEL_NAME | Display name for the Google Chat home space |
| GOOGLE_CHAT_MAX_MESSAGES | Pub/Sub FlowControl max in-flight messages (default:1) |
| GOOGLE_CHAT_MAX_BYTES | Pub/Sub FlowControl max in-flight bytes (default:16777216, 16 MiB) |
| GOOGLE_CHAT_BOOTSTRAP_SPACES | Comma-separated extra space IDs to probe at startup when resolving the bot's ownusers/{id} |
| GOOGLE_CHAT_DEBUG_RAW | Set to any value to log redacted Pub/Sub envelopes at DEBUG level (debugging only) |
| WHATSAPP_ENABLED | Enable the WhatsApp bridge (true/false) |
| WHATSAPP_MODE | bot(separate number) orself-chat(message yourself) |
| WHATSAPP_ALLOWED_USERS | Comma-separated phone numbers (with country code, no+), or*to allow all senders |
| WHATSAPP_ALLOW_ALL_USERS | Allow all WhatsApp senders without an allowlist (true/false) |
| WHATSAPP_HOME_CHANNEL | Default chat ID for cron / notification delivery. |
| WHATSAPP_HOME_CHANNEL_NAME | Display name for the WhatsApp home channel. |
| WHATSAPP_DEBUG | Log raw message events in the bridge for troubleshooting (true/false) |
| WHATSAPP_CLOUD_PHONE_NUMBER_ID | Meta Phone Number ID from the WhatsApp Business Cloud API (15–17 digits;notthe phone number itself) |
| WHATSAPP_CLOUD_ACCESS_TOKEN | Meta access token (starts withEAA); temporary tokens expire after 24h, System User tokens are permanent |
| WHATSAPP_CLOUD_APP_SECRET | 32-char hex app secret used to verify inbound webhook signatures |
| WHATSAPP_CLOUD_VERIFY_TOKEN | Shared secret for Meta's webhook verification handshake (auto-generated by the setup wizard) |
| WHATSAPP_CLOUD_ALLOWED_USERS | Comma-separatedwa_ids (phone numbers with country code, no+) allowed to message the bot |
| WHATSAPP_CLOUD_ALLOW_ALL_USERS | Allow all WhatsApp Cloud senders without an allowlist (true/false) |
| WHATSAPP_CLOUD_APP_ID | Optional Meta App ID (for future analytics integration) |
| WHATSAPP_CLOUD_WABA_ID | Optional WhatsApp Business Account ID (for future analytics integration) |
| WHATSAPP_CLOUD_WEBHOOK_HOST | Interface the inbound webhook server binds to (default0.0.0.0) |
| WHATSAPP_CLOUD_WEBHOOK_PORT | Port the inbound webhook server binds to (default8090) |
| WHATSAPP_CLOUD_WEBHOOK_PATH | URL path Meta posts inbound messages to (default/whatsapp/webhook) |
| WHATSAPP_CLOUD_API_VERSION | Meta Graph API version to call (defaultv20.0) |
| WHATSAPP_CLOUD_HOME_CHANNEL | wa_idto use as the bot's home channel (for cron jobs etc.) |
| WHATSAPP_CLOUD_DM_POLICY | DM gating for the Cloud adapter (open/allowlist/disabled); falls back toWHATSAPP_DM_POLICYwhen unset |
| WHATSAPP_CLOUD_ALLOW_FROM | Comma-separated senders allowed whendm_policy: allowlist(barewa_ids; Baileys-style JIDs are normalized) |
| WHATSAPP_CLOUD_GROUP_POLICY | Group gating for the Cloud adapter (open/allowlist/disabled); falls back toWHATSAPP_GROUP_POLICYwhen unset |
| WHATSAPP_CLOUD_GROUP_ALLOW_FROM | Comma-separated group chat IDs allowed whengroup_policy: allowlist |
| SIGNAL_HTTP_URL | signal-cli daemon HTTP endpoint (for examplehttp://127.0.0.1:8080) |
| SIGNAL_ACCOUNT | Bot phone number in E.164 format |
| SIGNAL_ALLOWED_USERS | Comma-separated E.164 phone numbers or UUIDs |
| SIGNAL_GROUP_ALLOWED_USERS | Comma-separated group IDs, or*for all groups |
| SIGNAL_HOME_CHANNEL_NAME | Display name for the Signal home channel |
| SIGNAL_IGNORE_STORIES | Ignore Signal stories/status updates |
| SIGNAL_ALLOW_ALL_USERS | Allow all Signal users without an allowlist |
| TWILIO_ACCOUNT_SID | Twilio Account SID (shared with telephony skill) |
| TWILIO_AUTH_TOKEN | Twilio Auth Token (shared with telephony skill; also used for webhook signature validation) |
| TWILIO_PHONE_NUMBER | Twilio phone number in E.164 format (shared with telephony skill) |
| SMS_WEBHOOK_URL | Public URL for Twilio signature validation — must match the webhook URL in Twilio Console (required) |
| SMS_WEBHOOK_PORT | Webhook listener port for inbound SMS (default:8080) |
| SMS_WEBHOOK_HOST | Webhook bind address (default:0.0.0.0) |
| SMS_INSECURE_NO_SIGNATURE | Set totrueto disable Twilio signature validation (local dev only — not for production) |
| SMS_ALLOWED_USERS | Comma-separated E.164 phone numbers allowed to chat |
| SMS_ALLOW_ALL_USERS | Allow all SMS senders without an allowlist |
| SMS_HOME_CHANNEL | Phone number for cron job / notification delivery |
| SMS_HOME_CHANNEL_NAME | Display name for the SMS home channel |
| EMAIL_ADDRESS | Email address for the Email gateway adapter |
| EMAIL_PASSWORD | Password or app password for the email account |
| EMAIL_IMAP_HOST | IMAP hostname for the email adapter |
| EMAIL_IMAP_PORT | IMAP port |
| EMAIL_SMTP_HOST | SMTP hostname for the email adapter |
| EMAIL_SMTP_PORT | SMTP port |
| EMAIL_ALLOWED_USERS | Comma-separated email addresses allowed to message the bot |
| EMAIL_HOME_ADDRESS | Default recipient for proactive email delivery |
| EMAIL_HOME_ADDRESS_NAME | Display name for the email home target |
| EMAIL_POLL_INTERVAL | Email polling interval in seconds |
| EMAIL_ALLOW_ALL_USERS | Allow all inbound email senders |
| DINGTALK_CLIENT_ID | DingTalk bot AppKey from developer portal (open.dingtalk.com) |
| DINGTALK_CLIENT_SECRET | DingTalk bot AppSecret from developer portal |
| DINGTALK_ALLOWED_USERS | Comma-separated DingTalk user IDs allowed to message the bot |
| DINGTALK_WEBHOOK_URL | Static robot webhook URL for cross-platform / cron delivery. |
| DINGTALK_HOME_CHANNEL | Default conversation ID for cron / notification delivery. |
| DINGTALK_HOME_CHANNEL_NAME | Display name for the DingTalk home channel. |
| FEISHU_APP_ID | Feishu/Lark bot App ID fromopen.feishu.cn |
| FEISHU_APP_SECRET | Feishu/Lark bot App Secret |
| FEISHU_DOMAIN | feishu(China) orlark(international). Default:feishu |
| FEISHU_CONNECTION_MODE | websocket(recommended) orwebhook. Default:websocket |
| FEISHU_ENCRYPT_KEY | Optional encryption key for webhook mode |
| FEISHU_VERIFICATION_TOKEN | Optional verification token for webhook mode |
| FEISHU_ALLOWED_USERS | Comma-separated Feishu user IDs allowed to message the bot |
| FEISHU_ALLOW_BOTS | none(default) /mentions/all— accept inbound messages from other bots. Seebot-to-bot messaging |
| FEISHU_REQUIRE_MENTION | true(default) /false— whether group messages must @mention the bot. Override per-chat viagroup_rules.<chat_id>.require_mention. |
| FEISHU_HOME_CHANNEL | Feishu chat ID for cron delivery and notifications |
| FEISHU_HOME_CHANNEL_NAME | Display name for the Feishu home channel. |
| FEISHU_ALLOW_ALL_USERS | Allow any Feishu user to trigger the bot (dev only). |
| WECOM_BOT_ID | WeCom AI Bot ID from admin console |
| WECOM_SECRET | WeCom AI Bot secret |
| WECOM_WEBSOCKET_URL | Custom WebSocket URL (default:wss://openws.work.weixin.qq.com) |
| WECOM_ALLOWED_USERS | Comma-separated WeCom user IDs allowed to message the bot |
| WECOM_HOME_CHANNEL | WeCom chat ID for cron delivery and notifications |
| WECOM_CALLBACK_CORP_ID | WeCom enterprise Corp ID for callback self-built app |
| WECOM_CALLBACK_CORP_SECRET | Corp secret for the self-built app |
| WECOM_CALLBACK_AGENT_ID | Agent ID of the self-built app |
| WECOM_CALLBACK_TOKEN | Callback verification token |
| WECOM_CALLBACK_ENCODING_AES_KEY | AES key for callback encryption |
| WECOM_CALLBACK_HOST | Callback server bind address (default:0.0.0.0) |
| WECOM_CALLBACK_PORT | Callback server port (default:8645) |
| WECOM_CALLBACK_ALLOWED_USERS | Comma-separated user IDs for allowlist |
| WECOM_CALLBACK_ALLOW_ALL_USERS | Settrueto allow all users without an allowlist |
| WEIXIN_ACCOUNT_ID | Weixin account ID obtained via QR login through iLink Bot API |
| WEIXIN_TOKEN | Weixin authentication token obtained via QR login through iLink Bot API |
| WEIXIN_BASE_URL | Override Weixin iLink Bot API base URL (default:https://ilinkai.weixin.qq.com) |
| WEIXIN_CDN_BASE_URL | Override Weixin CDN base URL for media (default:https://novac2c.cdn.weixin.qq.com/c2c) |
| WEIXIN_DM_POLICY | Direct message policy:open,allowlist,pairing,disabled(default:open) |
| WEIXIN_GROUP_POLICY | Group message policy:open,allowlist,disabled(default:disabled) |
| WEIXIN_ALLOWED_USERS | Comma-separated Weixin user IDs allowed to DM the bot |
| WEIXIN_GROUP_ALLOWED_USERS | Comma-separated Weixingroup chat IDs(not member user IDs) allowed to interact with the bot. The variable name is legacy — it expects group IDs. Only takes effect when iLink actually delivers group events; QR-login iLink bot identities (...@im.bot) typically don't receive ordinary WeChat group messages. |
| WEIXIN_HOME_CHANNEL | Weixin chat ID for cron delivery and notifications |
| WEIXIN_HOME_CHANNEL_NAME | Display name for the Weixin home channel |
| WEIXIN_ALLOW_ALL_USERS | Allow all Weixin users without an allowlist (true/false) |
| BLUEBUBBLES_SERVER_URL | BlueBubbles server URL (e.g.http://192.168.1.10:1234) |
| BLUEBUBBLES_PASSWORD | BlueBubbles server password |
| BLUEBUBBLES_WEBHOOK_HOST | Webhook listener bind address (default:127.0.0.1) |
| BLUEBUBBLES_WEBHOOK_PORT | Webhook listener port (default:8645) |
| BLUEBUBBLES_HOME_CHANNEL | Phone/email for cron/notification delivery |
| BLUEBUBBLES_ALLOWED_USERS | Comma-separated authorized users |
| BLUEBUBBLES_ALLOW_ALL_USERS | Allow all users (true/false) |
| QQ_APP_ID | QQ Bot App ID fromq.qq.com |
| QQ_CLIENT_SECRET | QQ Bot App Secret fromq.qq.com |
| QQ_STT_API_KEY | API key for external STT fallback provider (optional, used when QQ built-in ASR returns no text) |
| QQ_STT_BASE_URL | Base URL for external STT provider (optional) |
| QQ_STT_MODEL | Model name for external STT provider (optional) |
| QQ_ALLOWED_USERS | Comma-separated QQ user openIDs allowed to message the bot |
| QQ_GROUP_ALLOWED_USERS | Comma-separated QQ group IDs for group @-message access |
| QQ_ALLOW_ALL_USERS | Allow all users (true/false, overridesQQ_ALLOWED_USERS) |
| QQBOT_HOME_CHANNEL | QQ user/group openID for cron delivery and notifications |
| QQBOT_HOME_CHANNEL_NAME | Display name for the QQ home channel |
| QQ_PORTAL_HOST | Override the QQ portal host (set tosandbox.q.qq.comto route through the sandbox gateway; default:q.qq.com). |
| QQ_SANDBOX | Enable QQ sandbox mode for development testing (true/false) |
| MATTERMOST_URL | Mattermost server URL (e.g.https://mm.example.com) |
| MATTERMOST_TOKEN | Bot token or personal access token for Mattermost |
| MATTERMOST_ALLOWED_USERS | Comma-separated Mattermost user IDs allowed to message the bot |
| MATTERMOST_ALLOW_ALL_USERS | Allow any Mattermost user to trigger the bot (dev only). |
| MATTERMOST_ALLOWED_CHANNELS | If set, the bot only responds in these channels (whitelist). |
| MATTERMOST_HOME_CHANNEL | Channel ID for proactive message delivery (cron, notifications) |
| MATTERMOST_REQUIRE_MENTION | Require@mentionin channels (default:true). Set tofalseto respond to all messages. |
| MATTERMOST_FREE_RESPONSE_CHANNELS | Comma-separated channel IDs where bot responds without@mention |
| MATTERMOST_REPLY_MODE | Reply style:thread(threaded replies) oroff(flat messages, default) |
| MATRIX_HOMESERVER | Matrix homeserver URL (e.g.https://matrix.org) |
| MATRIX_ACCESS_TOKEN | Matrix access token for bot authentication |
| MATRIX_USER_ID | Matrix user ID (e.g.@hermes:matrix.org) — required for password login, optional with access token |
| MATRIX_PASSWORD | Matrix password (alternative to access token) |
| MATRIX_ALLOWED_USERS | Comma-separated Matrix user IDs allowed to message the bot (e.g.@alice:matrix.org) |
| MATRIX_ALLOW_ALL_USERS | Allow any Matrix user to trigger the bot (dev only). |
| MATRIX_HOME_CHANNEL | Default room ID for cron / notification delivery. |
| MATRIX_HOME_CHANNEL_NAME | Display name for the Matrix home room. |
| MATRIX_ALLOWED_ROOMS | Comma-separated Matrix room IDs allowed to trigger bot responses |
| MATRIX_HOME_ROOM | Room ID for proactive message delivery (e.g.!abc123:matrix.org) |
| MATRIX_ENCRYPTION | Enable end-to-end encryption (true/false, default:false) |
| MATRIX_E2EE_MODE | Matrix E2EE behavior:off,optional, orrequired. OverridesMATRIX_ENCRYPTIONwhen set. |
| MATRIX_DEVICE_ID | Stable Matrix device ID for E2EE persistence across restarts (e.g.HERMES_BOT). Without this, E2EE keys rotate every startup and historic-room decrypt breaks. |
| MATRIX_REACTIONS | Enable processing-lifecycle emoji reactions on inbound messages (default:true). Set tofalseto disable. |
| MATRIX_REQUIRE_MENTION | Require@mentionin rooms (default:true). Set tofalseto respond to all messages. |
| MATRIX_FREE_RESPONSE_ROOMS | Comma-separated room IDs where bot responds without@mention |
| MATRIX_IGNORE_USER_PATTERNS | Comma-separated regular expressions for Matrix bridge/appservice ghost user IDs to ignore |
| MATRIX_PROCESS_NOTICES | Process inbound Matrixm.noticeevents (default:false) |
| MATRIX_SESSION_SCOPE | Matrix session scope for project rooms:auto,room, orthread(default:auto) |
| MATRIX_TOOLS_ALLOW_CROSS_ROOM | Allow Matrix tools to target explicit rooms other than the current room (default:false) |
| MATRIX_TOOLS_ALLOW_CROSS_ROOM_DESTRUCTIVE | Allow cross-room Matrix redaction/invite-like tools; requiresMATRIX_TOOLS_ALLOW_CROSS_ROOM=true(default:false) |
| MATRIX_TOOLS_ALLOW_REDACTION | Allow Matrix message redaction tool execution (default:false) |
| MATRIX_TOOLS_ALLOW_INVITES | Allow Matrix invite tool execution (default:false) |
| MATRIX_TOOLS_ALLOW_ROOM_CREATE | Allow Matrix room creation tool execution (default:false) |
| MATRIX_ALLOW_ROOM_MENTIONS | Allow outbound@roommentions to notify all room members (default:false) |
| MATRIX_AUTO_THREAD | Auto-create threads for room messages (default:true) |
| MATRIX_DM_AUTO_THREAD | Auto-create threads for DM messages in Matrix (default:false) |
| MATRIX_DM_MENTION_THREADS | Create a thread when bot is@mentionedin a DM (default:false) |
| MATRIX_APPROVAL_REQUIRE_SENDER | Require approval/model-picker reactions to come from the original requester when known (default:true) |
| MATRIX_APPROVAL_TIMEOUT_SECONDS | Timeout for Matrix reaction approval/model-picker prompts (default:300) |
| MATRIX_ALLOW_PUBLIC_ROOMS | Allow Matrix room-creation tools to create public rooms (default:false) |
| MATRIX_MAX_MEDIA_BYTES | Maximum Matrix media upload/download size in bytes (default:104857600) |
| MATRIX_RECOVERY_KEY | Recovery key for cross-signing verification after device key rotation. Recommended for E2EE setups with cross-signing enabled. |
| MATRIX_RECOVERY_KEY_OUTPUT_FILE | Optional one-time path for a generated Matrix recovery key. Created with mode0600and never overwritten. |
| HASS_TOKEN | Home Assistant Long-Lived Access Token (enables HA platform + tools) |
| HASS_URL | Home Assistant URL (default:http://homeassistant.local:8123) |
| WEBHOOK_ENABLED | Enable the webhook platform adapter (true/false) |
| WEBHOOK_PORT | HTTP server port for receiving webhooks (default:8644) |
| WEBHOOK_SECRET | Global HMAC secret for webhook signature validation (used as fallback when routes don't specify their own) |
| API_SERVER_ENABLED | Enable the OpenAI-compatible API server (true/false). Runs alongside other platforms. |
| API_SERVER_KEY | Bearer token for API server authentication. Required whenever the API server is enabled. |
| API_SERVER_CORS_ORIGINS | Comma-separated browser origins allowed to call the API server directly (for examplehttp://localhost:3000,http://127.0.0.1:3000). Default: disabled. |
| API_SERVER_PORT | Port for the API server (default:8642) |
| API_SERVER_HOST | Host/bind address for the API server (default:127.0.0.1).API_SERVER_KEYis still required on loopback; use a narrowAPI_SERVER_CORS_ORIGINSallowlist for browser access. |
| API_SERVER_MODEL_NAME | Model name advertised on/v1/models. Defaults to the profile name (orhermes-agentfor the default profile). Useful for multi-user setups where frontends like Open WebUI need distinct model names per connection. |
| GATEWAY_PROXY_URL | URL of a remote Hermes API server to forward messages to (proxy mode). When set, the gateway handles platform I/O only — all agent work is delegated to the remote server. Also configurable viagateway.proxy_urlinconfig.yaml. |
| GATEWAY_PROXY_KEY | Bearer token for authenticating with the remote API server in proxy mode. Must matchAPI_SERVER_KEYon the remote host. |
| MESSAGING_CWD | Deprecated compatibility fallback for gateway working directory. Preferterminal.cwdinconfig.yaml. |
| GATEWAY_ALLOWED_USERS | Comma-separated user IDs allowed across all platforms |
| GATEWAY_ALLOW_ALL_USERS | Allow all users without allowlists (true/false, default:false) |

`TELEGRAM_BOT_TOKEN`
`TELEGRAM_ALLOWED_USERS`
`TELEGRAM_ALLOW_ALL_USERS`
`TELEGRAM_GROUP_ALLOWED_USERS`
`-`
`TELEGRAM_GROUP_ALLOWED_CHATS`
`TELEGRAM_HOME_CHANNEL`
`TELEGRAM_HOME_CHANNEL_NAME`
`TELEGRAM_CRON_THREAD_ID`
`TELEGRAM_HOME_CHANNEL_THREAD_ID`
`TELEGRAM_WEBHOOK_URL`
`TELEGRAM_WEBHOOK_PORT`
`8443`
`TELEGRAM_WEBHOOK_SECRET`
`TELEGRAM_WEBHOOK_URL`
`openssl rand -hex 32`
`TELEGRAM_REACTIONS`
`false`
`TELEGRAM_REQUIRE_MENTION`
`telegram.require_mention`
`config.yaml`
`TELEGRAM_MENTION_PATTERNS`
`telegram.mention_patterns`
`TELEGRAM_EXCLUSIVE_BOT_MENTIONS`
`@...bot`
`true`
`telegram.exclusive_bot_mentions`
`TELEGRAM_REPLY_TO_MODE`
`off`
`first`
`all`
`TELEGRAM_IGNORED_THREADS`
`TELEGRAM_PROXY`
`HTTPS_PROXY`
`http://`
`https://`
`socks5://`
`DISCORD_BOT_TOKEN`
`DISCORD_ALLOWED_USERS`
`DISCORD_ALLOW_ALL_USERS`
`DISCORD_ALLOWED_ROLES`
`DISCORD_ALLOWED_USERS`
`DISCORD_ALLOWED_CHANNELS`
`config.yaml`
`discord.allowed_channels`
`DISCORD_PROXY`
`HTTPS_PROXY`
`http://`
`https://`
`socks5://`
`DISCORD_HOME_CHANNEL`
`DISCORD_HOME_CHANNEL_NAME`
`DISCORD_COMMAND_SYNC_POLICY`
`safe`
`bulk`
`tree.sync()`
`off`
`DISCORD_REQUIRE_MENTION`
`DISCORD_FREE_RESPONSE_CHANNELS`
`DISCORD_AUTO_THREAD`
`DISCORD_ALLOW_ANY_ATTACHMENT`
`true`
`terminal`
`read_file`
`ffprobe`
`false`
`DISCORD_MAX_ATTACHMENT_BYTES`
`33554432`
`0`
`DISCORD_REACTIONS`
`true`
`DISCORD_IGNORED_CHANNELS`
`DISCORD_NO_THREAD_CHANNELS`
`DISCORD_REPLY_TO_MODE`
`off`
`first`
`all`
`DISCORD_ALLOW_MENTION_EVERYONE`
`@everyone`
`@here`
`false`
`DISCORD_ALLOW_MENTION_ROLES`
`@role`
`false`
`DISCORD_ALLOW_MENTION_USERS`
`@user`
`true`
`DISCORD_ALLOW_MENTION_REPLIED_USER`
`true`
`SLACK_BOT_TOKEN`
`xoxb-...`
`SLACK_APP_TOKEN`
`xapp-...`
`SLACK_ALLOWED_USERS`
`SLACK_ALLOW_ALL_USERS`
`SLACK_HOME_CHANNEL`
`SLACK_HOME_CHANNEL_NAME`
`GOOGLE_CHAT_PROJECT_ID`
`GOOGLE_CLOUD_PROJECT`
`GOOGLE_CHAT_SUBSCRIPTION_NAME`
`projects/{proj}/subscriptions/{sub}`
`GOOGLE_CHAT_SUBSCRIPTION`
`GOOGLE_CHAT_SERVICE_ACCOUNT_JSON`
`GOOGLE_APPLICATION_CREDENTIALS`
`GOOGLE_CHAT_ALLOWED_USERS`
`GOOGLE_CHAT_ALLOW_ALL_USERS`
`GOOGLE_CHAT_HOME_CHANNEL`
`spaces/AAAA...`
`GOOGLE_CHAT_HOME_CHANNEL_NAME`
`GOOGLE_CHAT_MAX_MESSAGES`
`1`
`GOOGLE_CHAT_MAX_BYTES`
`16777216`
`GOOGLE_CHAT_BOOTSTRAP_SPACES`
`users/{id}`
`GOOGLE_CHAT_DEBUG_RAW`
`WHATSAPP_ENABLED`
`true`
`false`
`WHATSAPP_MODE`
`bot`
`self-chat`
`WHATSAPP_ALLOWED_USERS`
`+`
`*`
`WHATSAPP_ALLOW_ALL_USERS`
`true`
`false`
`WHATSAPP_HOME_CHANNEL`
`WHATSAPP_HOME_CHANNEL_NAME`
`WHATSAPP_DEBUG`
`true`
`false`
`WHATSAPP_CLOUD_PHONE_NUMBER_ID`
`WHATSAPP_CLOUD_ACCESS_TOKEN`
`EAA`
`WHATSAPP_CLOUD_APP_SECRET`
`WHATSAPP_CLOUD_VERIFY_TOKEN`
`WHATSAPP_CLOUD_ALLOWED_USERS`
`wa_id`
`+`
`WHATSAPP_CLOUD_ALLOW_ALL_USERS`
`true`
`false`
`WHATSAPP_CLOUD_APP_ID`
`WHATSAPP_CLOUD_WABA_ID`
`WHATSAPP_CLOUD_WEBHOOK_HOST`
`0.0.0.0`
`WHATSAPP_CLOUD_WEBHOOK_PORT`
`8090`
`WHATSAPP_CLOUD_WEBHOOK_PATH`
`/whatsapp/webhook`
`WHATSAPP_CLOUD_API_VERSION`
`v20.0`
`WHATSAPP_CLOUD_HOME_CHANNEL`
`wa_id`
`WHATSAPP_CLOUD_DM_POLICY`
`open`
`allowlist`
`disabled`
`WHATSAPP_DM_POLICY`
`WHATSAPP_CLOUD_ALLOW_FROM`
`dm_policy: allowlist`
`wa_id`
`WHATSAPP_CLOUD_GROUP_POLICY`
`open`
`allowlist`
`disabled`
`WHATSAPP_GROUP_POLICY`
`WHATSAPP_CLOUD_GROUP_ALLOW_FROM`
`group_policy: allowlist`
`SIGNAL_HTTP_URL`
`http://127.0.0.1:8080`
`SIGNAL_ACCOUNT`
`SIGNAL_ALLOWED_USERS`
`SIGNAL_GROUP_ALLOWED_USERS`
`*`
`SIGNAL_HOME_CHANNEL_NAME`
`SIGNAL_IGNORE_STORIES`
`SIGNAL_ALLOW_ALL_USERS`
`TWILIO_ACCOUNT_SID`
`TWILIO_AUTH_TOKEN`
`TWILIO_PHONE_NUMBER`
`SMS_WEBHOOK_URL`
`SMS_WEBHOOK_PORT`
`8080`
`SMS_WEBHOOK_HOST`
`0.0.0.0`
`SMS_INSECURE_NO_SIGNATURE`
`true`
`SMS_ALLOWED_USERS`
`SMS_ALLOW_ALL_USERS`
`SMS_HOME_CHANNEL`
`SMS_HOME_CHANNEL_NAME`
`EMAIL_ADDRESS`
`EMAIL_PASSWORD`
`EMAIL_IMAP_HOST`
`EMAIL_IMAP_PORT`
`EMAIL_SMTP_HOST`
`EMAIL_SMTP_PORT`
`EMAIL_ALLOWED_USERS`
`EMAIL_HOME_ADDRESS`
`EMAIL_HOME_ADDRESS_NAME`
`EMAIL_POLL_INTERVAL`
`EMAIL_ALLOW_ALL_USERS`
`DINGTALK_CLIENT_ID`
`DINGTALK_CLIENT_SECRET`
`DINGTALK_ALLOWED_USERS`
`DINGTALK_WEBHOOK_URL`
`DINGTALK_HOME_CHANNEL`
`DINGTALK_HOME_CHANNEL_NAME`
`FEISHU_APP_ID`
`FEISHU_APP_SECRET`
`FEISHU_DOMAIN`
`feishu`
`lark`
`feishu`
`FEISHU_CONNECTION_MODE`
`websocket`
`webhook`
`websocket`
`FEISHU_ENCRYPT_KEY`
`FEISHU_VERIFICATION_TOKEN`
`FEISHU_ALLOWED_USERS`
`FEISHU_ALLOW_BOTS`
`none`
`mentions`
`all`
`FEISHU_REQUIRE_MENTION`
`true`
`false`
`group_rules.<chat_id>.require_mention`
`FEISHU_HOME_CHANNEL`
`FEISHU_HOME_CHANNEL_NAME`
`FEISHU_ALLOW_ALL_USERS`
`WECOM_BOT_ID`
`WECOM_SECRET`
`WECOM_WEBSOCKET_URL`
`wss://openws.work.weixin.qq.com`
`WECOM_ALLOWED_USERS`
`WECOM_HOME_CHANNEL`
`WECOM_CALLBACK_CORP_ID`
`WECOM_CALLBACK_CORP_SECRET`
`WECOM_CALLBACK_AGENT_ID`
`WECOM_CALLBACK_TOKEN`
`WECOM_CALLBACK_ENCODING_AES_KEY`
`WECOM_CALLBACK_HOST`
`0.0.0.0`
`WECOM_CALLBACK_PORT`
`8645`
`WECOM_CALLBACK_ALLOWED_USERS`
`WECOM_CALLBACK_ALLOW_ALL_USERS`
`true`
`WEIXIN_ACCOUNT_ID`
`WEIXIN_TOKEN`
`WEIXIN_BASE_URL`
`https://ilinkai.weixin.qq.com`
`WEIXIN_CDN_BASE_URL`
`https://novac2c.cdn.weixin.qq.com/c2c`
`WEIXIN_DM_POLICY`
`open`
`allowlist`
`pairing`
`disabled`
`open`
`WEIXIN_GROUP_POLICY`
`open`
`allowlist`
`disabled`
`disabled`
`WEIXIN_ALLOWED_USERS`
`WEIXIN_GROUP_ALLOWED_USERS`
`...@im.bot`
`WEIXIN_HOME_CHANNEL`
`WEIXIN_HOME_CHANNEL_NAME`
`WEIXIN_ALLOW_ALL_USERS`
`true`
`false`
`BLUEBUBBLES_SERVER_URL`
`http://192.168.1.10:1234`
`BLUEBUBBLES_PASSWORD`
`BLUEBUBBLES_WEBHOOK_HOST`
`127.0.0.1`
`BLUEBUBBLES_WEBHOOK_PORT`
`8645`
`BLUEBUBBLES_HOME_CHANNEL`
`BLUEBUBBLES_ALLOWED_USERS`
`BLUEBUBBLES_ALLOW_ALL_USERS`
`true`
`false`
`QQ_APP_ID`
`QQ_CLIENT_SECRET`
`QQ_STT_API_KEY`
`QQ_STT_BASE_URL`
`QQ_STT_MODEL`
`QQ_ALLOWED_USERS`
`QQ_GROUP_ALLOWED_USERS`
`QQ_ALLOW_ALL_USERS`
`true`
`false`
`QQ_ALLOWED_USERS`
`QQBOT_HOME_CHANNEL`
`QQBOT_HOME_CHANNEL_NAME`
`QQ_PORTAL_HOST`
`sandbox.q.qq.com`
`q.qq.com`
`QQ_SANDBOX`
`true`
`false`
`MATTERMOST_URL`
`https://mm.example.com`
`MATTERMOST_TOKEN`
`MATTERMOST_ALLOWED_USERS`
`MATTERMOST_ALLOW_ALL_USERS`
`MATTERMOST_ALLOWED_CHANNELS`
`MATTERMOST_HOME_CHANNEL`
`MATTERMOST_REQUIRE_MENTION`
`@mention`
`true`
`false`
`MATTERMOST_FREE_RESPONSE_CHANNELS`
`@mention`
`MATTERMOST_REPLY_MODE`
`thread`
`off`
`MATRIX_HOMESERVER`
`https://matrix.org`
`MATRIX_ACCESS_TOKEN`
`MATRIX_USER_ID`
`@hermes:matrix.org`
`MATRIX_PASSWORD`
`MATRIX_ALLOWED_USERS`
`@alice:matrix.org`
`MATRIX_ALLOW_ALL_USERS`
`MATRIX_HOME_CHANNEL`
`MATRIX_HOME_CHANNEL_NAME`
`MATRIX_ALLOWED_ROOMS`
`MATRIX_HOME_ROOM`
`!abc123:matrix.org`
`MATRIX_ENCRYPTION`
`true`
`false`
`false`
`MATRIX_E2EE_MODE`
`off`
`optional`
`required`
`MATRIX_ENCRYPTION`
`MATRIX_DEVICE_ID`
`HERMES_BOT`
`MATRIX_REACTIONS`
`true`
`false`
`MATRIX_REQUIRE_MENTION`
`@mention`
`true`
`false`
`MATRIX_FREE_RESPONSE_ROOMS`
`@mention`
`MATRIX_IGNORE_USER_PATTERNS`
`MATRIX_PROCESS_NOTICES`
`m.notice`
`false`
`MATRIX_SESSION_SCOPE`
`auto`
`room`
`thread`
`auto`
`MATRIX_TOOLS_ALLOW_CROSS_ROOM`
`false`
`MATRIX_TOOLS_ALLOW_CROSS_ROOM_DESTRUCTIVE`
`MATRIX_TOOLS_ALLOW_CROSS_ROOM=true`
`false`
`MATRIX_TOOLS_ALLOW_REDACTION`
`false`
`MATRIX_TOOLS_ALLOW_INVITES`
`false`
`MATRIX_TOOLS_ALLOW_ROOM_CREATE`
`false`
`MATRIX_ALLOW_ROOM_MENTIONS`
`@room`
`false`
`MATRIX_AUTO_THREAD`
`true`
`MATRIX_DM_AUTO_THREAD`
`false`
`MATRIX_DM_MENTION_THREADS`
`@mentioned`
`false`
`MATRIX_APPROVAL_REQUIRE_SENDER`
`true`
`MATRIX_APPROVAL_TIMEOUT_SECONDS`
`300`
`MATRIX_ALLOW_PUBLIC_ROOMS`
`false`
`MATRIX_MAX_MEDIA_BYTES`
`104857600`
`MATRIX_RECOVERY_KEY`
`MATRIX_RECOVERY_KEY_OUTPUT_FILE`
`0600`
`HASS_TOKEN`
`HASS_URL`
`http://homeassistant.local:8123`
`WEBHOOK_ENABLED`
`true`
`false`
`WEBHOOK_PORT`
`8644`
`WEBHOOK_SECRET`
`API_SERVER_ENABLED`
`true`
`false`
`API_SERVER_KEY`
`API_SERVER_CORS_ORIGINS`
`http://localhost:3000,http://127.0.0.1:3000`
`API_SERVER_PORT`
`8642`
`API_SERVER_HOST`
`127.0.0.1`
`API_SERVER_KEY`
`API_SERVER_CORS_ORIGINS`
`API_SERVER_MODEL_NAME`
`/v1/models`
`hermes-agent`
`GATEWAY_PROXY_URL`
`gateway.proxy_url`
`config.yaml`
`GATEWAY_PROXY_KEY`
`API_SERVER_KEY`
`MESSAGING_CWD`
`terminal.cwd`
`config.yaml`
`GATEWAY_ALLOWED_USERS`
`GATEWAY_ALLOW_ALL_USERS`
`true`
`false`
`false`

### Web Dashboard & Hermes Desktop​

Auth for theweb dashboardand for connectingHermes Desktop to a remote backend. Per the secrets-only convention, credentials belong in~/.hermes/.env; the OAuthclient_idis better set underdashboard.oauthinconfig.yaml(env wins when set).

`~/.hermes/.env`
`client_id`
`dashboard.oauth`
`config.yaml`

Three dashboard-auth providers ship in the box. For a remote Hermes Desktop connection or any internet-facing dashboard, the recommended provider isOAuth (Nous Portal)— setHERMES_DASHBOARD_OAUTH_CLIENT_ID(provision it withhermes dashboard register). The bundledusername/passwordprovider (HERMES_DASHBOARD_BASIC_AUTH_*) is the quickest option for a backend on a trusted LAN or behind a VPN, but is not suitable for direct public-internet exposure. To authenticate against your own identity provider, use theself-hosted OIDCprovider (HERMES_DASHBOARD_OIDC_*). Either way, a non-loopback bind (hermes dashboard --host 0.0.0.0) engages the auth gate. SeeWeb Dashboard → Authenticationfor the full picture.

`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`hermes dashboard register`
`HERMES_DASHBOARD_BASIC_AUTH_*`
`HERMES_DASHBOARD_OIDC_*`
`hermes dashboard --host 0.0.0.0`
| Variable | Description |
| --- | --- |
| HERMES_DASHBOARD_BASIC_AUTH_USERNAME | Username for the bundled username/password dashboard-auth provider (plugins/dashboard_auth/basic). Activates the provider when set together with a password. Overridesdashboard.basic_auth.username. |
| HERMES_DASHBOARD_BASIC_AUTH_PASSWORD | Plaintext password for the basic provider (hashed in-memory at load). Wins over a configpassword_hashso you can rotate via env. Overridesdashboard.basic_auth.password. |
| HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH | scrypt password hash for the basic provider (preferred — no plaintext at rest). Compute withpython -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('PW'))". Overridesdashboard.basic_auth.password_hash. |
| HERMES_DASHBOARD_BASIC_AUTH_SECRET | HMAC key (32+ bytes, base64/hex/raw) signing the basic provider's stateless session tokens. Set explicitly so sessions survive restarts / span multiple workers; blank → random per-process (you'll be logged out on every restart). Overridesdashboard.basic_auth.secret. |
| HERMES_DASHBOARD_BASIC_AUTH_TTL_SECONDS | Access-token lifetime for the basic provider (default 12h). Overridesdashboard.basic_auth.session_ttl_seconds. |
| HERMES_DASHBOARD_OAUTH_CLIENT_ID | OAuth client id (agent:{instance_id}) for the gated/public dashboard, activating the Nous (plugins/dashboard_auth/nous) provider. Overridesdashboard.oauth.client_id. Provision it withhermes dashboard register. |
| HERMES_DASHBOARD_PUBLIC_URL | Complete public URL the dashboard is reached at, for OAuth callback construction behind reverse proxies. Overridesdashboard.public_url. |
| HERMES_DASHBOARD_OIDC_ISSUER | OIDC issuer URL for the bundled self-hosted OIDC provider (plugins/dashboard_auth/self_hosted). Required to activate it. Overridesdashboard.oauth.self_hosted.issuer. |
| HERMES_DASHBOARD_OIDC_CLIENT_ID | Public OIDC client id (authorization-code + PKCE) for the self-hosted OIDC provider. Required to activate it. Overridesdashboard.oauth.self_hosted.client_id. |
| HERMES_DASHBOARD_OIDC_SCOPES | Requested OIDC scopes for the self-hosted OIDC provider (defaultopenid profile email). Overridesdashboard.oauth.self_hosted.scopes. |
| HERMES_DESKTOP_REMOTE_URL | (Desktop side) Base URL of the remote backend, e.g.http://host:9119. When set, overrides the in-app Gateway URL; you still sign in from the Gateway settings panel (OAuth redirect or username/password, whichever the backend advertises). |
| HERMES_DESKTOP_HERMES | Desktop backend command override. Used by packagers/Nix or troubleshooting to point Electron at a specifichermesexecutable after backend probing. |
| HERMES_DESKTOP_HERMES_ROOT | Desktop source-checkout override used byhermes desktop --hermes-root; checked before the packaged first-launch install or an existinghermesonPATH. |
| HERMES_DESKTOP_IGNORE_EXISTING | Set to1to make Desktop ignore an existinghermesonPATHduring backend resolution. Equivalent tohermes desktop --ignore-existing. |
| HERMES_DESKTOP_CWD | Initial project directory for Desktop chat sessions. Set byhermes desktop --cwd. |

`HERMES_DASHBOARD_BASIC_AUTH_USERNAME`
`plugins/dashboard_auth/basic`
`dashboard.basic_auth.username`
`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`
`password_hash`
`dashboard.basic_auth.password`
`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH`
`python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('PW'))"`
`dashboard.basic_auth.password_hash`
`HERMES_DASHBOARD_BASIC_AUTH_SECRET`
`dashboard.basic_auth.secret`
`HERMES_DASHBOARD_BASIC_AUTH_TTL_SECONDS`
`dashboard.basic_auth.session_ttl_seconds`
`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`agent:{instance_id}`
`plugins/dashboard_auth/nous`
`dashboard.oauth.client_id`
`hermes dashboard register`
`HERMES_DASHBOARD_PUBLIC_URL`
`dashboard.public_url`
`HERMES_DASHBOARD_OIDC_ISSUER`
`plugins/dashboard_auth/self_hosted`
`dashboard.oauth.self_hosted.issuer`
`HERMES_DASHBOARD_OIDC_CLIENT_ID`
`dashboard.oauth.self_hosted.client_id`
`HERMES_DASHBOARD_OIDC_SCOPES`
`openid profile email`
`dashboard.oauth.self_hosted.scopes`
`HERMES_DESKTOP_REMOTE_URL`
`http://host:9119`
`HERMES_DESKTOP_HERMES`
`hermes`
`HERMES_DESKTOP_HERMES_ROOT`
`hermes desktop --hermes-root`
`hermes`
`PATH`
`HERMES_DESKTOP_IGNORE_EXISTING`
`1`
`hermes`
`PATH`
`hermes desktop --ignore-existing`
`HERMES_DESKTOP_CWD`
`hermes desktop --cwd`

### Microsoft Graph (Teams Meetings)​

App-only credentials for the Microsoft Graph REST client used by the upcoming Teams meeting summary pipeline. SeeRegister a Microsoft Graph applicationfor the Azure portal walkthrough and the exact API permissions required.

| Variable | Description |
| --- | --- |
| MSGRAPH_TENANT_ID | Azure AD tenant ID (directory GUID) for the Graph app registration. |
| MSGRAPH_CLIENT_ID | Application (client) ID of the Azure app registration. |
| MSGRAPH_CLIENT_SECRET | Client secret value for the app registration. Store in~/.hermes/.envwithchmod 600; rotate periodically via the Azure portal. |
| MSGRAPH_SCOPE | OAuth2 scope for the client-credentials token request (default:https://graph.microsoft.com/.default). |
| MSGRAPH_AUTHORITY_URL | Microsoft identity platform authority (default:https://login.microsoftonline.com). Override only for national/sovereign clouds (e.g.https://login.microsoftonline.usfor GCC High). |

`MSGRAPH_TENANT_ID`
`MSGRAPH_CLIENT_ID`
`MSGRAPH_CLIENT_SECRET`
`~/.hermes/.env`
`chmod 600`
`MSGRAPH_SCOPE`
`https://graph.microsoft.com/.default`
`MSGRAPH_AUTHORITY_URL`
`https://login.microsoftonline.com`
`https://login.microsoftonline.us`

### Microsoft Graph Webhook Listener​

Inbound change-notification listener for Graph events (Teams meetings, calendar, chat, etc.). SeeMicrosoft Graph Webhook Listenerfor setup and security hardening.

| Variable | Description |
| --- | --- |
| MSGRAPH_WEBHOOK_ENABLED | Enable themsgraph_webhookgateway platform (true/1/yes). |
| MSGRAPH_WEBHOOK_PORT | Port the listener binds to (default:8646). |
| MSGRAPH_WEBHOOK_CLIENT_STATE | Shared secret Graph echoes in every notification; compared withhmac.compare_digest. Generate withopenssl rand -hex 32. |
| MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES | Comma-separated allowlist of Graph resource paths/patterns (e.g.communications/onlineMeetings,chats/*/messages). Trailing*is prefix-matching. Empty = accept all. |
| MSGRAPH_WEBHOOK_ALLOWED_SOURCE_CIDRS | Comma-separated CIDR ranges allowed to POST to the listener (e.g.52.96.0.0/14,52.104.0.0/14). Empty = allow all (default). Restrict to Microsoft Graph's published egress ranges in production. |

`MSGRAPH_WEBHOOK_ENABLED`
`msgraph_webhook`
`true`
`1`
`yes`
`MSGRAPH_WEBHOOK_PORT`
`8646`
`MSGRAPH_WEBHOOK_CLIENT_STATE`
`hmac.compare_digest`
`openssl rand -hex 32`
`MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES`
`communications/onlineMeetings,chats/*/messages`
`*`
`MSGRAPH_WEBHOOK_ALLOWED_SOURCE_CIDRS`
`52.96.0.0/14,52.104.0.0/14`

### Teams Meeting Summary Delivery​

Only used when theteams_pipelinepluginis enabled. Settings are also configurable underplatforms.teams.extrainconfig.yaml— env vars take priority when both are set. SeeMicrosoft Teams → Meeting Summary Delivery.

`teams_pipeline`
`platforms.teams.extra`
`config.yaml`
| Variable | Description |
| --- | --- |
| TEAMS_DELIVERY_MODE | graphorincoming_webhook. |
| TEAMS_INCOMING_WEBHOOK_URL | Teams-generated webhook URL; required whenTEAMS_DELIVERY_MODE=incoming_webhook. |
| TEAMS_GRAPH_ACCESS_TOKEN | Pre-acquired delegated access token for Graph delivery. Rarely needed — the writer falls back to theMSGRAPH_*app credentials when unset. |
| TEAMS_TEAM_ID | Target Team ID for channel delivery (graphmode). |
| TEAMS_CHANNEL_ID | Target channel ID (paired withTEAMS_TEAM_ID). |
| TEAMS_CHAT_ID | Target 1:1 or group chat ID (alternative to team+channel forgraphmode). |

`TEAMS_DELIVERY_MODE`
`graph`
`incoming_webhook`
`TEAMS_INCOMING_WEBHOOK_URL`
`TEAMS_DELIVERY_MODE=incoming_webhook`
`TEAMS_GRAPH_ACCESS_TOKEN`
`MSGRAPH_*`
`TEAMS_TEAM_ID`
`graph`
`TEAMS_CHANNEL_ID`
`TEAMS_TEAM_ID`
`TEAMS_CHAT_ID`
`graph`

### LINE Messaging API​

Used by the bundled LINE platform plugin (plugins/platforms/line/). SeeMessaging Gateway → LINEfor full setup.

`plugins/platforms/line/`
| Variable | Description |
| --- | --- |
| LINE_CHANNEL_ACCESS_TOKEN | Long-lived channel access token from the LINE Developers Console (Messaging API tab). Required. |
| LINE_CHANNEL_SECRET | Channel secret (Basic settings tab); used for HMAC-SHA256 webhook signature verification. Required. |
| LINE_HOST | Webhook bind host (default:0.0.0.0). |
| LINE_PORT | Webhook bind port (default:8646). |
| LINE_PUBLIC_URL | Public HTTPS base URL (e.g.https://my-tunnel.example.com). Required for image / audio / video sends — LINE only accepts HTTPS-reachable URLs. |
| LINE_ALLOWED_USERS | Comma-separated user IDs allowed to DM the bot (U-prefixed). |
| LINE_ALLOWED_GROUPS | Comma-separated group IDs the bot will respond in (C-prefixed). |
| LINE_ALLOWED_ROOMS | Comma-separated room IDs the bot will respond in (R-prefixed). |
| LINE_ALLOW_ALL_USERS | Dev-only escape hatch — accepts any source. Default:false. |
| LINE_HOME_CHANNEL | Default delivery target for cron jobs withdeliver: line. |
| LINE_SLOW_RESPONSE_THRESHOLD | Seconds before the slow-LLM Template Buttons postback fires (default:45). Set0to disable and always Push-fallback. |
| LINE_PENDING_TEXT | Bubble text shown alongside the postback button. |
| LINE_BUTTON_LABEL | Postback button label (default:Get answer). |
| LINE_DELIVERED_TEXT | Reply when an already-delivered postback is tapped again (default:Already replied ✅). |
| LINE_INTERRUPTED_TEXT | Reply when a/stop-orphaned postback button is tapped (default:Run was interrupted before completion.). |

`LINE_CHANNEL_ACCESS_TOKEN`
`LINE_CHANNEL_SECRET`
`LINE_HOST`
`0.0.0.0`
`LINE_PORT`
`8646`
`LINE_PUBLIC_URL`
`https://my-tunnel.example.com`
`LINE_ALLOWED_USERS`
`U`
`LINE_ALLOWED_GROUPS`
`C`
`LINE_ALLOWED_ROOMS`
`R`
`LINE_ALLOW_ALL_USERS`
`false`
`LINE_HOME_CHANNEL`
`deliver: line`
`LINE_SLOW_RESPONSE_THRESHOLD`
`45`
`0`
`LINE_PENDING_TEXT`
`LINE_BUTTON_LABEL`
`Get answer`
`LINE_DELIVERED_TEXT`
`Already replied ✅`
`LINE_INTERRUPTED_TEXT`
`/stop`
`Run was interrupted before completion.`

### ntfy (push notifications)​

ntfyis a lightweight HTTP-based push notification service. Subscribe to a topic from thentfy mobile app, publish to that topic to talk to the agent.

| Variable | Description |
| --- | --- |
| NTFY_TOPIC | Topic to subscribe to (incoming messages). Required. |
| NTFY_SERVER_URL | Server URL (default:https://ntfy.sh). Point at a self-hosted ntfy for privacy. |
| NTFY_TOKEN | Optional auth token. Bearer token (e.g.tk_xyz) oruser:passfor Basic auth. |
| NTFY_PUBLISH_TOPIC | Topic for outgoing replies (defaults toNTFY_TOPIC). |
| NTFY_MARKDOWN | Settrueto send replies withX-Markdown: trueheader. Default:false. |
| NTFY_ALLOWED_USERS | Allowlist (treated as user IDs; on ntfy these are topic names). Typically set to the same value asNTFY_TOPIC. |
| NTFY_ALLOW_ALL_USERS | Dev-only escape hatch — only safe on access-controlled private topics. Default:false. |
| NTFY_HOME_CHANNEL | Default delivery target for cron jobs withdeliver: ntfy. |
| NTFY_HOME_CHANNEL_NAME | Human label for the home channel (defaults to the topic name). |

`NTFY_TOPIC`
`NTFY_SERVER_URL`
`https://ntfy.sh`
`NTFY_TOKEN`
`tk_xyz`
`user:pass`
`NTFY_PUBLISH_TOPIC`
`NTFY_TOPIC`
`NTFY_MARKDOWN`
`true`
`X-Markdown: true`
`false`
`NTFY_ALLOWED_USERS`
`NTFY_TOPIC`
`NTFY_ALLOW_ALL_USERS`
`false`
`NTFY_HOME_CHANNEL`
`deliver: ntfy`
`NTFY_HOME_CHANNEL_NAME`

Seethe ntfy messaging guide— particularly theidentity modelsection — before deploying with untrusted topics.

### IRC​

Connect Hermes to an IRC server. No external dependencies. Seethe IRC messaging guide.

| Variable | Description |
| --- | --- |
| IRC_SERVER | IRC server hostname (e.g.irc.libera.chat). Required. |
| IRC_CHANNEL | Channel(s) to join (e.g.#hermes); comma-separate for multiple. Required. |
| IRC_NICKNAME | Bot nickname (default:hermes-bot). Required. |
| IRC_PORT | Server port (default:6697with TLS,6667without). |
| IRC_USE_TLS | Use TLS (true/false; defaulttrueon port 6697). |
| IRC_SERVER_PASSWORD | Server password for thePASScommand (optional). |
| IRC_NICKSERV_PASSWORD | NickServ password for automatic IDENTIFY on connect (optional). |
| IRC_ALLOWED_USERS | Comma-separated nicks allowed to talk to the bot. |
| IRC_ALLOW_ALL_USERS | Allow anyone in the channel to talk to the bot (dev only). |
| IRC_HOME_CHANNEL | Channel for cron / notification delivery (defaults toIRC_CHANNEL). |

`IRC_SERVER`
`irc.libera.chat`
`IRC_CHANNEL`
`#hermes`
`IRC_NICKNAME`
`hermes-bot`
`IRC_PORT`
`6697`
`6667`
`IRC_USE_TLS`
`true`
`false`
`true`
`IRC_SERVER_PASSWORD`
`PASS`
`IRC_NICKSERV_PASSWORD`
`IRC_ALLOWED_USERS`
`IRC_ALLOW_ALL_USERS`
`IRC_HOME_CHANNEL`
`IRC_CHANNEL`

### SimpleX​

Connect Hermes to aSimpleX Chatnetwork via a localsimplex-chatdaemon. Seethe SimpleX messaging guide.

`simplex-chat`
| Variable | Description |
| --- | --- |
| SIMPLEX_WS_URL | WebSocket URL of the simplex-chat daemon (e.g.ws://127.0.0.1:5225). |
| SIMPLEX_ALLOWED_USERS | Comma-separated SimpleX contact IDs allowed to talk to the bot. |
| SIMPLEX_ALLOW_ALL_USERS | Allow any contact to talk to the bot (dev only — disables allowlist). |
| SIMPLEX_AUTO_ACCEPT | Auto-accept incoming contact requests (default:true). |
| SIMPLEX_GROUP_ALLOWED | Comma-separated SimpleX group IDs the bot should participate in, or*to allow any group. Omit to ignore group messages entirely (safer default — a bot in a group otherwise processes every member's traffic). |
| SIMPLEX_HOME_CHANNEL | Default contact/group ID for cron / notification delivery. |
| SIMPLEX_HOME_CHANNEL_NAME | Human label for the home channel (defaults to the ID). |

`SIMPLEX_WS_URL`
`ws://127.0.0.1:5225`
`SIMPLEX_ALLOWED_USERS`
`SIMPLEX_ALLOW_ALL_USERS`
`SIMPLEX_AUTO_ACCEPT`
`true`
`SIMPLEX_GROUP_ALLOWED`
`*`
`SIMPLEX_HOME_CHANNEL`
`SIMPLEX_HOME_CHANNEL_NAME`

### Photon​

Connect Hermes toPhoton/ Spectrum (iMessage and other Spectrum platforms) via the Node sidecar. Seethe Photon messaging guide.

| Variable | Description |
| --- | --- |
| PHOTON_PROJECT_ID | Spectrum project id (the project'sspectrumProjectId; set byhermes photon setup). |
| PHOTON_PROJECT_SECRET | Project secret paired with the Spectrum project id (set byhermes photon setup). |
| PHOTON_ALLOWED_USERS | Comma-separated E.164 phone numbers allowed to talk to the bot. |
| PHOTON_ALLOW_ALL_USERS | Allow any sender to trigger the bot (dev only — disables allowlist). |
| PHOTON_REQUIRE_MENTION | Ignore group-chat messages unless they match a mention wake word (true/false, defaultfalse). |
| PHOTON_MENTION_PATTERNS | Mention wake-word regexes for group chats (JSON list or comma/newline-separated; defaults to Hermes wake words). |
| PHOTON_HOME_CHANNEL | Default Photon target for cron / notification delivery: Spectrum space id, DM GUID, or bare E.164 phone number. |
| PHOTON_HOME_CHANNEL_NAME | Human label for the home channel. |
| PHOTON_MARKDOWN | Send agent replies as markdown — iMessage renders it natively, other Spectrum platforms degrade to plain text (true/false, defaulttrue). |
| PHOTON_REACTIONS | Tapback 👀/👍/👎 on messages as processing status and route tapbacks on bot messages to the agent (true/false, defaultfalse). |
| PHOTON_TELEMETRY | Enable Spectrum SDK telemetry in the sidecar (true/false, defaultfalse; toggle with `hermes photon telemetry on |
| PHOTON_SIDECAR_PORT | Loopback port for the Node sidecar control + inbound channel (default8789). |
| PHOTON_SIDECAR_AUTOSTART | Spawn the Node sidecar on connect (true/false, defaulttrue). |
| PHOTON_NODE_BIN | Path to the node binary (default:shutil.which('node')). |
| PHOTON_DASHBOARD_HOST | Photon Dashboard API host (defaulthttps://app.photon.codes). |
| PHOTON_SPECTRUM_HOST | Photon Spectrum API host (defaulthttps://spectrum.photon.codes). |

`PHOTON_PROJECT_ID`
`spectrumProjectId`
`hermes photon setup`
`PHOTON_PROJECT_SECRET`
`hermes photon setup`
`PHOTON_ALLOWED_USERS`
`PHOTON_ALLOW_ALL_USERS`
`PHOTON_REQUIRE_MENTION`
`true`
`false`
`false`
`PHOTON_MENTION_PATTERNS`
`PHOTON_HOME_CHANNEL`
`PHOTON_HOME_CHANNEL_NAME`
`PHOTON_MARKDOWN`
`true`
`false`
`true`
`PHOTON_REACTIONS`
`true`
`false`
`false`
`PHOTON_TELEMETRY`
`true`
`false`
`false`
`PHOTON_SIDECAR_PORT`
`8789`
`PHOTON_SIDECAR_AUTOSTART`
`true`
`false`
`true`
`PHOTON_NODE_BIN`
`shutil.which('node')`
`PHOTON_DASHBOARD_HOST`
`https://app.photon.codes`
`PHOTON_SPECTRUM_HOST`
`https://spectrum.photon.codes`

### Microsoft Teams (adapter)​

The Microsoft Teams platform adapter (Bot Framework / Azure AD), distinct from theMicrosoft Graph (Teams Meetings)integration above. Seethe Teams messaging guide.

| Variable | Description |
| --- | --- |
| TEAMS_CLIENT_ID | Azure AD application (Bot Framework) client ID. |
| TEAMS_CLIENT_SECRET | Azure AD application client secret. |
| TEAMS_TENANT_ID | Azure AD tenant ID hosting the bot application. |
| TEAMS_PORT | Webhook listen port (Bot Framework default:3978). |
| TEAMS_ALLOWED_USERS | Comma-separated Teams user IDs / UPNs allowed to talk to the bot. |
| TEAMS_ALLOW_ALL_USERS | Allow any Teams user to trigger the bot (dev only). |
| TEAMS_HOME_CHANNEL | Default chat/channel ID for cron / notification delivery. |
| TEAMS_HOME_CHANNEL_NAME | Display name for the Teams home channel. |

`TEAMS_CLIENT_ID`
`TEAMS_CLIENT_SECRET`
`TEAMS_TENANT_ID`
`TEAMS_PORT`
`3978`
`TEAMS_ALLOWED_USERS`
`TEAMS_ALLOW_ALL_USERS`
`TEAMS_HOME_CHANNEL`
`TEAMS_HOME_CHANNEL_NAME`

### Raft​

| Variable | Description |
| --- | --- |
| RAFT_PROFILE | Raft agent profile slug — auto-enables the adapter when set. |

`RAFT_PROFILE`

### Advanced Messaging Tuning​

Advanced per-platform knobs for throttling the outbound message batcher. Most users never need to touch these; defaults are set to respect each platform's rate limits without feeling sluggish.

| Variable | Description |
| --- | --- |
| HERMES_TELEGRAM_TEXT_BATCH_DELAY_SECONDS | Grace window before flushing a queued Telegram text chunk (default:0.6). |
| HERMES_TELEGRAM_TEXT_BATCH_SPLIT_DELAY_SECONDS | Delay between split chunks when a single Telegram message exceeds the length limit (default:2.0). |
| HERMES_SIMPLEX_TEXT_BATCH_DELAY | Quiet-period seconds (default:0.8) used to concatenate rapid-fire inbound text messages into a single MessageEvent — same pattern as Telegram's text batching. |
| HERMES_TELEGRAM_MEDIA_BATCH_DELAY_SECONDS | Grace window before flushing queued Telegram media (default:0.6). |
| HERMES_TELEGRAM_FOLLOWUP_GRACE_SECONDS | Delay before sending a follow-up after the agent finishes, to avoid racing the last stream chunk. |
| HERMES_TELEGRAM_HTTP_CONNECT_TIMEOUT/_READ_TIMEOUT/_WRITE_TIMEOUT/_POOL_TIMEOUT | Override the underlyingpython-telegram-botHTTP timeouts (seconds). |
| HERMES_TELEGRAM_INIT_TIMEOUT | Per-attempt cap (seconds) on the Telegraminitialize()connect chain during gateway startup, so an unreachable fallback-IP chain can't block startup indefinitely (default:30). |
| HERMES_TELEGRAM_HTTP_POOL_SIZE | Max concurrent HTTP connections to the Telegram API. |
| HERMES_TELEGRAM_DISABLE_FALLBACK_IPS | Disable the hard-coded Cloudflare fallback IPs used when DNS fails (true/false). |
| HERMES_DISCORD_TEXT_BATCH_DELAY_SECONDS | Grace window before flushing a queued Discord text chunk (default:0.6). |
| HERMES_DISCORD_TEXT_BATCH_SPLIT_DELAY_SECONDS | Delay between split chunks when a Discord message exceeds the length limit (default:2.0). |
| HERMES_DISCORD_LIVENESS_INTERVAL_SECONDS | Internal bridge fordiscord.liveness_interval_seconds(config.yaml). Interval for the Discord REST liveness probe that detects zombie clients behind dead proxies/NATs (default:60; set to0to disable). Prefer settingdiscord.liveness_interval_secondsinconfig.yaml. |
| HERMES_DISCORD_LIVENESS_FAILURE_THRESHOLD | Internal bridge fordiscord.liveness_failure_threshold(config.yaml). Consecutive probe failures before forcing a Discord reconnect (default:3). Prefer settingdiscord.liveness_failure_thresholdinconfig.yaml. |
| HERMES_MATRIX_TEXT_BATCH_DELAY_SECONDS/_SPLIT_DELAY_SECONDS | Matrix equivalents of the Telegram batch knobs. |
| HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS/_SPLIT_DELAY_SECONDS/_MAX_CHARS/_MAX_MESSAGES | Feishu batcher tuning — delay, split delay, max chars per message, max messages per batch. |
| HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS | Feishu media flush delay. |
| HERMES_FEISHU_DEDUP_CACHE_SIZE | Size of the Feishu webhook dedup cache (default:1024). |
| HERMES_WECOM_TEXT_BATCH_DELAY_SECONDS/_SPLIT_DELAY_SECONDS | WeCom batcher tuning. |
| HERMES_VISION_DOWNLOAD_TIMEOUT | Timeout in seconds for downloading an image before handing it to vision models (default:30). |
| HERMES_VISION_MAX_CONCURRENCY | Max concurrent imageencode/resizebursts across the whole process (override forauxiliary.vision.max_concurrency; default: host CPU core count, no ceiling). Bounds only the CPU-bound encode step so a video-frame fan-out can't saturate every core and starve the event loop — the LLM calls stay fully concurrent. Values< 1are ignored. |
| HERMES_RESTART_DRAIN_TIMEOUT | Gateway: seconds to wait for active runs to drain on/restartbefore forcing the restart (default:900). |
| HERMES_GATEWAY_PLATFORM_CONNECT_TIMEOUT | Per-platform connect timeout during gateway startup and reconnect (seconds;0/negative waits indefinitely). Applies to the connect attemptandthe Discord adapter's ready-wait, so accounts with many slash commands to sync don't get killed mid-startup. Bridged fromgateway.platform_connect_timeoutinconfig.yaml(default30); this env var is the manual override and wins if set explicitly. |
| HERMES_GATEWAY_BUSY_INPUT_MODE | Default gateway busy-input behavior:queue,steer, orinterrupt. Can be overridden per chat with/busy. |
| HERMES_GATEWAY_BUSY_ACK_ENABLED | Whether the gateway sends an acknowledgment message (⚡/⏳/⏩) when a user sends input while the agent is busy (default:true). Set tofalseto suppress these messages entirely — the input is still queued/steered/interrupts as normal, only the chat reply is silenced. Bridged fromdisplay.busy_ack_enabledinconfig.yaml. |
| HERMES_GATEWAY_NO_SUPERVISE | Inside the s6-overlay Docker image, opt out of auto-supervision when runninghermes gateway runand use pre-s6 foreground semantics (no auto-restart, gateway is the container's main process). Truthy values:1,true,yes. Equivalent to the--no-superviseCLI flag. No-op outside the s6 image. |
| HERMES_GATEWAY_BOOTSTRAP_STATE | Inside the s6-overlay Docker image, declare the gateway'sinitialsupervised state on a fresh volume. On a blank volume there is no persistedgateway_state.json, so the boot reconciler registers thegateway-defaultslot but leaves itdown(it only auto-starts when the last recorded state wasrunning). Set this torunningand the first-boot setup hook seedsgateway_state.jsonbeforethe reconciler runs, so the gateway comes up on the very first boot. Only the literal valuerunningis honoured. First-boot-only: an existinggateway_state.jsonis never overwritten, so a deliberately-stopped gateway stays stopped across restarts. No-op outside the s6 image. |
| GATEWAY_RELAY_URL | Experimental relay connector WebSocket base URL. When set, the gateway registers the genericrelayadapter and dials the connector outbound. Mirrorsgateway.relay_urlinconfig.yaml. |
| GATEWAY_RELAY_ID | Relay gateway identifier assigned byhermes gateway enrollor managed self-provisioning. Mirrorsgateway.relay_id. |
| GATEWAY_RELAY_SECRET | Per-gateway relay secret used to authenticate the WebSocket. If this is already configured, managed self-provisioning is skipped. Mirrorsgateway.relay_secret. |
| GATEWAY_RELAY_DELIVERY_KEY | Connector-issued delivery key retained for relay/passthrough authentication compatibility. Current relay inbound messages arrive on the outbound WebSocket rather than a gateway-side HTTP receiver. |
| GATEWAY_RELAY_ENROLL_TOKEN | Enrollment token consumed byhermes gateway enrollwhen--tokenis not passed explicitly. |
| GATEWAY_RELAY_PLATFORM | Optional platform name advertised in the relay capability descriptor. |
| GATEWAY_RELAY_BOT_ID | Optional bot identifier advertised in the relay capability descriptor. |
| GATEWAY_RELAY_ENDPOINT | Optional gateway endpoint advertised for connector modes that need a callback/passthrough URL; not required for the default WS-only inbound relay path. Mirrorsgateway.relay_endpoint. |
| GATEWAY_RELAY_ROUTE_KEYS | Comma-separated relay route keys advertised to the connector. Mirrorsgateway.relay_route_keys. |
| HERMES_FILE_MUTATION_VERIFIER | Enable the per-turn file-mutation verifier footer (default:true). When enabled, Hermes appends an advisory listing anywrite_file/patchcalls that failed during the turn and were not superseded by a successful write. Set to0,false,no, oroffto suppress. Mirrorsdisplay.file_mutation_verifierinconfig.yaml; the env var wins when set. |
| HERMES_CRON_TIMEOUT | Inactivity timeout for cron job agent runs in seconds (default:600). The agent can run indefinitely while actively calling tools or receiving stream tokens — this only triggers when idle. Set to0for unlimited. |
| HERMES_CRON_SCRIPT_TIMEOUT | Timeout for pre-run scripts attached to cron jobs in seconds (default:3600). Bounds the script only — skill/agent jobs use the separateHERMES_CRON_TIMEOUTinactivity budget. Also configurable viacron.script_timeout_secondsinconfig.yaml. |
| HERMES_CRON_MAX_PARALLEL | Max cron jobs run in parallel per tick (default:4). |

`HERMES_TELEGRAM_TEXT_BATCH_DELAY_SECONDS`
`0.6`
`HERMES_TELEGRAM_TEXT_BATCH_SPLIT_DELAY_SECONDS`
`2.0`
`HERMES_SIMPLEX_TEXT_BATCH_DELAY`
`0.8`
`HERMES_TELEGRAM_MEDIA_BATCH_DELAY_SECONDS`
`0.6`
`HERMES_TELEGRAM_FOLLOWUP_GRACE_SECONDS`
`HERMES_TELEGRAM_HTTP_CONNECT_TIMEOUT`
`_READ_TIMEOUT`
`_WRITE_TIMEOUT`
`_POOL_TIMEOUT`
`python-telegram-bot`
`HERMES_TELEGRAM_INIT_TIMEOUT`
`initialize()`
`30`
`HERMES_TELEGRAM_HTTP_POOL_SIZE`
`HERMES_TELEGRAM_DISABLE_FALLBACK_IPS`
`true`
`false`
`HERMES_DISCORD_TEXT_BATCH_DELAY_SECONDS`
`0.6`
`HERMES_DISCORD_TEXT_BATCH_SPLIT_DELAY_SECONDS`
`2.0`
`HERMES_DISCORD_LIVENESS_INTERVAL_SECONDS`
`discord.liveness_interval_seconds`
`60`
`0`
`discord.liveness_interval_seconds`
`config.yaml`
`HERMES_DISCORD_LIVENESS_FAILURE_THRESHOLD`
`discord.liveness_failure_threshold`
`3`
`discord.liveness_failure_threshold`
`config.yaml`
`HERMES_MATRIX_TEXT_BATCH_DELAY_SECONDS`
`_SPLIT_DELAY_SECONDS`
`HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS`
`_SPLIT_DELAY_SECONDS`
`_MAX_CHARS`
`_MAX_MESSAGES`
`HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS`
`HERMES_FEISHU_DEDUP_CACHE_SIZE`
`1024`
`HERMES_WECOM_TEXT_BATCH_DELAY_SECONDS`
`_SPLIT_DELAY_SECONDS`
`HERMES_VISION_DOWNLOAD_TIMEOUT`
`30`
`HERMES_VISION_MAX_CONCURRENCY`
`auxiliary.vision.max_concurrency`
`< 1`
`HERMES_RESTART_DRAIN_TIMEOUT`
`/restart`
`900`
`HERMES_GATEWAY_PLATFORM_CONNECT_TIMEOUT`
`0`
`gateway.platform_connect_timeout`
`config.yaml`
`30`
`HERMES_GATEWAY_BUSY_INPUT_MODE`
`queue`
`steer`
`interrupt`
`/busy`
`HERMES_GATEWAY_BUSY_ACK_ENABLED`
`true`
`false`
`display.busy_ack_enabled`
`config.yaml`
`HERMES_GATEWAY_NO_SUPERVISE`
`hermes gateway run`
`1`
`true`
`yes`
`--no-supervise`
`HERMES_GATEWAY_BOOTSTRAP_STATE`
`gateway_state.json`
`gateway-default`
`running`
`running`
`gateway_state.json`
`running`
`gateway_state.json`
`GATEWAY_RELAY_URL`
`relay`
`gateway.relay_url`
`config.yaml`
`GATEWAY_RELAY_ID`
`hermes gateway enroll`
`gateway.relay_id`
`GATEWAY_RELAY_SECRET`
`gateway.relay_secret`
`GATEWAY_RELAY_DELIVERY_KEY`
`GATEWAY_RELAY_ENROLL_TOKEN`
`hermes gateway enroll`
`--token`
`GATEWAY_RELAY_PLATFORM`
`GATEWAY_RELAY_BOT_ID`
`GATEWAY_RELAY_ENDPOINT`
`gateway.relay_endpoint`
`GATEWAY_RELAY_ROUTE_KEYS`
`gateway.relay_route_keys`
`HERMES_FILE_MUTATION_VERIFIER`
`true`
`write_file`
`patch`
`0`
`false`
`no`
`off`
`display.file_mutation_verifier`
`config.yaml`
`HERMES_CRON_TIMEOUT`
`600`
`0`
`HERMES_CRON_SCRIPT_TIMEOUT`
`3600`
`HERMES_CRON_TIMEOUT`
`cron.script_timeout_seconds`
`config.yaml`
`HERMES_CRON_MAX_PARALLEL`
`4`

## Agent Behavior​

| Variable | Description |
| --- | --- |
| HERMES_MAX_ITERATIONS | Max tool-calling iterations per conversation (default: 90) |
| HERMES_INFERENCE_MODEL | Override model name at process level (takes priority overconfig.yamlfor the session). Also settable via-m/--modelflag. |
| HERMES_YOLO_MODE | Set to1to bypass dangerous-command approval prompts. Equivalent to--yolo. |
| HERMES_ACCEPT_HOOKS | Auto-approve any unseen shell hooks declared inconfig.yamlwithout a TTY prompt. Equivalent to--accept-hooksorhooks_auto_accept: true. |
| HERMES_IGNORE_USER_CONFIG | Skip~/.hermes/config.yamland use built-in defaults (credentials in.envstill load). Equivalent to--ignore-user-config. |
| HERMES_IGNORE_RULES | Skip auto-injection ofAGENTS.md,SOUL.md,.cursorrules, memory, and preloaded skills. Equivalent to--ignore-rules. |
| HERMES_SAFE_MODE | Troubleshooting mode: disable ALL customizations — skips plugin discovery, MCP server loading, and shell-hook registration. Set automatically by--safe-mode(which also sets the two flags above). |
| HERMES_MD_NAMES | Comma-separated list of rules-file names to auto-inject (default:AGENTS.md,CLAUDE.md,.cursorrules,SOUL.md). |
| HERMES_TOOL_PROGRESS | Deprecated compatibility variable for tool progress display. Preferdisplay.tool_progressinconfig.yaml. |
| HERMES_TOOL_PROGRESS_MODE | Deprecated compatibility variable for tool progress mode. Preferdisplay.tool_progressinconfig.yaml. |
| HERMES_HUMAN_DELAY_MODE | Response pacing:off/natural/custom |
| HERMES_HUMAN_DELAY_MIN_MS | Custom delay range minimum (ms) |
| HERMES_HUMAN_DELAY_MAX_MS | Custom delay range maximum (ms) |
| HERMES_QUIET | Suppress non-essential output (true/false) |
| CODEX_HOME | WhenCodex app-server runtimeis enabled, override the directory Codex CLI reads its config + auth from (default:~/.codex). Hermes' migration writes the managed block to<CODEX_HOME>/config.toml. |
| HERMES_KANBAN_TASK | Set by the kanban dispatcher when spawning a worker (task UUID). Workers and the spawnedhermes-toolsMCP subprocess inherit it so kanban tools gate correctly. Don't set manually. |
| HERMES_API_TIMEOUT | LLM API call timeout in seconds (default:1800) |
| HERMES_API_CALL_STALE_TIMEOUT | Non-streaming stale-call timeout in seconds (default:90). Auto-disabled for local providers when left unset, and may scale upward for very large contexts. Also configurable viaproviders.<id>.stale_timeout_secondsorproviders.<id>.models.<model>.stale_timeout_secondsinconfig.yaml. |
| HERMES_STREAM_READ_TIMEOUT | Streaming socket read timeout in seconds (default:120). Auto-increased toHERMES_API_TIMEOUTfor local providers. Increase if local LLMs time out during long code generation. |
| HERMES_STREAM_STALE_TIMEOUT | Stale stream detection timeout in seconds (default:180). Auto-disabled for local providers. Triggers connection kill if no chunks arrive within this window. |
| HERMES_STREAM_RETRIES | Number of mid-stream reconnect attempts on transient network errors (default:3). |
| HERMES_STREAM_STALE_GIVEUP | Cross-turn circuit breaker: after this many consecutive stale kills (streaming or non-streaming) with no completed response, abort each call immediately with an actionable error instead of re-waiting out the stale timeout (default:5,0disables). Resets on any completed response,/modelswitch, fallback activation, or turn-start primary restore. |
| HERMES_AGENT_TIMEOUT | Gateway inactivity timeout for a running agent in seconds (default:1800, 30 minutes). Resets on every tool call and streamed token. Set to0to disable. |
| HERMES_AGENT_TIMEOUT_WARNING | Gateway: send a warning message after this many seconds of inactivity (default: 75% ofHERMES_AGENT_TIMEOUT). |
| HERMES_AGENT_NOTIFY_INTERVAL | Gateway: interval in seconds between progress notifications on long-running agent turns. |
| HERMES_CHECKPOINT_TIMEOUT | Timeout for filesystem checkpoint creation in seconds (default:30). |
| HERMES_EXEC_ASK | Enable execution approval prompts in gateway mode (true/false) |
| HERMES_ENABLE_PROJECT_PLUGINS | Enable auto-discovery of repo-local plugins from./.hermes/plugins/for both the agent loader and the dashboard web server. Accepts the standard truthy set:1/true/yes/on(case-insensitive). Everything else — including0,false,no,off, and the empty string — is treated asdisabled(default). Note: as of GHSA-5qr3-c538-wm9j (#29156) the dashboard web server refuses to auto-import a project plugin's Pythonapifile even when this var is enabled — project plugins may extend the UI via static JS/CSS but their backend routes are only loaded when moved under~/.hermes/plugins/. |
| HERMES_PLUGINS_DEBUG | 1/trueto surface verbose plugin-discovery logs on stderr — directories scanned, manifests parsed, skip reasons, and full tracebacks on parse orregister()failure. Aimed at plugin authors. |
| HERMES_BACKGROUND_NOTIFICATIONS | Background process notification mode in gateway:all(default),result,error,off |
| HERMES_EPHEMERAL_SYSTEM_PROMPT | Ephemeral system prompt injected at API-call time (never persisted to sessions) |
| HERMES_PREFILL_MESSAGES_FILE | Path to a JSON file of ephemeral prefill messages injected at API-call time. |
| HERMES_ALLOW_PRIVATE_URLS | true/false— allow tools to fetch localhost/private-network URLs. Off by default in gateway mode. |
| HERMES_REDACT_SECRETS | true/false— control secret redaction in tool output, logs, and chat responses (default:true). |
| HERMES_WRITE_SAFE_ROOT | Optional directory prefix that restrictswrite_file/patchwrites; paths outside require approval. Supports multiple directories separated byos.pathsep(:on Unix,;on Windows). |
| HERMES_DISABLE_LAZY_INSTALLS | Internal bridge var set automatically in the official Docker image to prevent runtime dependency installs into the immutable/opt/hermestree. The user-facing equivalent issecurity.allow_lazy_installs: falseinconfig.yaml; do not set this in.env. |
| HERMES_DISABLE_FILE_STATE_GUARD | Set to1to turn off the "file changed since you read it" guard onpatch/write_file. |
| HERMES_CORE_TOOLS | Comma-separated override for the canonical core tool list (advanced; rarely needed). |
| HERMES_BUNDLED_SKILLS | Comma-separated override for the list of bundled skills loaded at startup. |
| HERMES_OPTIONAL_SKILLS | Comma-separated list of optional-skill names to auto-install on first run. |
| HERMES_DEBUG_INTERRUPT | Set to1to log detailed interrupt/cancel tracing toagent.log. |
| HERMES_DUMP_REQUESTS | Dump API request payloads to log files (true/false) |
| HERMES_DUMP_REQUEST_STDOUT | Dump API request payloads to stdout instead of log files. |
| HERMES_OAUTH_TRACE | Set to1to log OAuth token exchange and refresh attempts. Includes redacted timing info. |
| HERMES_OAUTH_FILE | Override the path used for OAuth credential storage (default:~/.hermes/auth.json). |
| HERMES_AGENT_HELP_GUIDANCE | Append additional guidance text to the system prompt for custom deployments. |
| HERMES_AGENT_LOGO | Override the ASCII banner logo at CLI startup. |
| DELEGATION_MAX_CONCURRENT_CHILDREN | Max parallel subagents perdelegate_taskbatch (default:3, floor of 1, no ceiling). Also configurable viadelegation.max_concurrent_childreninconfig.yaml— the config value takes priority. |

`HERMES_MAX_ITERATIONS`
`HERMES_INFERENCE_MODEL`
`config.yaml`
`-m`
`--model`
`HERMES_YOLO_MODE`
`1`
`--yolo`
`HERMES_ACCEPT_HOOKS`
`config.yaml`
`--accept-hooks`
`hooks_auto_accept: true`
`HERMES_IGNORE_USER_CONFIG`
`~/.hermes/config.yaml`
`.env`
`--ignore-user-config`
`HERMES_IGNORE_RULES`
`AGENTS.md`
`SOUL.md`
`.cursorrules`
`--ignore-rules`
`HERMES_SAFE_MODE`
`--safe-mode`
`HERMES_MD_NAMES`
`AGENTS.md,CLAUDE.md,.cursorrules,SOUL.md`
`HERMES_TOOL_PROGRESS`
`display.tool_progress`
`config.yaml`
`HERMES_TOOL_PROGRESS_MODE`
`display.tool_progress`
`config.yaml`
`HERMES_HUMAN_DELAY_MODE`
`off`
`natural`
`custom`
`HERMES_HUMAN_DELAY_MIN_MS`
`HERMES_HUMAN_DELAY_MAX_MS`
`HERMES_QUIET`
`true`
`false`
`CODEX_HOME`
`~/.codex`
`<CODEX_HOME>/config.toml`
`HERMES_KANBAN_TASK`
`hermes-tools`
`HERMES_API_TIMEOUT`
`1800`
`HERMES_API_CALL_STALE_TIMEOUT`
`90`
`providers.<id>.stale_timeout_seconds`
`providers.<id>.models.<model>.stale_timeout_seconds`
`config.yaml`
`HERMES_STREAM_READ_TIMEOUT`
`120`
`HERMES_API_TIMEOUT`
`HERMES_STREAM_STALE_TIMEOUT`
`180`
`HERMES_STREAM_RETRIES`
`3`
`HERMES_STREAM_STALE_GIVEUP`
`5`
`0`
`/model`
`HERMES_AGENT_TIMEOUT`
`1800`
`0`
`HERMES_AGENT_TIMEOUT_WARNING`
`HERMES_AGENT_TIMEOUT`
`HERMES_AGENT_NOTIFY_INTERVAL`
`HERMES_CHECKPOINT_TIMEOUT`
`30`
`HERMES_EXEC_ASK`
`true`
`false`
`HERMES_ENABLE_PROJECT_PLUGINS`
`./.hermes/plugins/`
`1`
`true`
`yes`
`on`
`0`
`false`
`no`
`off`
`api`
`~/.hermes/plugins/`
`HERMES_PLUGINS_DEBUG`
`1`
`true`
`register()`
`HERMES_BACKGROUND_NOTIFICATIONS`
`all`
`result`
`error`
`off`
`HERMES_EPHEMERAL_SYSTEM_PROMPT`
`HERMES_PREFILL_MESSAGES_FILE`
`HERMES_ALLOW_PRIVATE_URLS`
`true`
`false`
`HERMES_REDACT_SECRETS`
`true`
`false`
`true`
`HERMES_WRITE_SAFE_ROOT`
`write_file`
`patch`
`os.pathsep`
`:`
`;`
`HERMES_DISABLE_LAZY_INSTALLS`
`/opt/hermes`
`security.allow_lazy_installs: false`
`config.yaml`
`.env`
`HERMES_DISABLE_FILE_STATE_GUARD`
`1`
`patch`
`write_file`
`HERMES_CORE_TOOLS`
`HERMES_BUNDLED_SKILLS`
`HERMES_OPTIONAL_SKILLS`
`HERMES_DEBUG_INTERRUPT`
`1`
`agent.log`
`HERMES_DUMP_REQUESTS`
`true`
`false`
`HERMES_DUMP_REQUEST_STDOUT`
`HERMES_OAUTH_TRACE`
`1`
`HERMES_OAUTH_FILE`
`~/.hermes/auth.json`
`HERMES_AGENT_HELP_GUIDANCE`
`HERMES_AGENT_LOGO`
`DELEGATION_MAX_CONCURRENT_CHILDREN`
`delegate_task`
`3`
`delegation.max_concurrent_children`
`config.yaml`

## Interface​

| Variable | Description |
| --- | --- |
| HERMES_TUI | Launch theTUIinstead of the classic CLI when set to1. Equivalent to passing--tui. |
| HERMES_TUI_DIR | Path to a prebuiltui-tui/directory (must containdist/entry.jsand populatednode_modules). Used by distros and Nix to skip the first-launchnpm install. |
| HERMES_TUI_RESUME | Resume a specific TUI session by ID on launch. When set,hermes --tuiskips forging a fresh session and picks up the named session instead — useful for re-attaching after a disconnect or terminal crash. |
| HERMES_TUI_THEME | Force the TUI color theme:light,dark, or a raw 6-character background hex (e.g.ffffffor1a1a2e). When unset, Hermes auto-detects usingCOLORFGBGand terminal background queries; this variable overrides detection on terminals (Ghostty, Warp, iTerm2, etc.) that don't setCOLORFGBG. |
| HERMES_INFERENCE_MODEL | Force the model forhermes -z/hermes chatwithout mutatingconfig.yaml. Pairs with the--providerflag. Useful for scripted callers (sweeper, CI, batch runners) that need to override the default model per run. |

`HERMES_TUI`
`1`
`--tui`
`HERMES_TUI_DIR`
`ui-tui/`
`dist/entry.js`
`node_modules`
`npm install`
`HERMES_TUI_RESUME`
`hermes --tui`
`HERMES_TUI_THEME`
`light`
`dark`
`ffffff`
`1a1a2e`
`COLORFGBG`
`COLORFGBG`
`HERMES_INFERENCE_MODEL`
`hermes -z`
`hermes chat`
`config.yaml`
`--provider`

## Session Settings​

| Variable | Description |
| --- | --- |
| SESSION_IDLE_MINUTES | Reset sessions after N minutes of inactivity (default: 1440) |
| SESSION_RESET_HOUR | Daily reset hour in 24h format (default: 4 = 4am) |
| HERMES_SESSION_ID | Exported automatically into every tool subprocessHermes spawns (terminal,execute_code, persistent shell, Docker/Singularity backends, delegated subagent runs). Set by the agent to the current session ID; user scripts called from tools can read it to correlate their output, telemetry, or side effects with the originating Hermes session.You should not set this manually— overriding it from a parent shell only takes effect outside an agent run, and is overwritten the moment the agent starts a session. |

`SESSION_IDLE_MINUTES`
`SESSION_RESET_HOUR`
`HERMES_SESSION_ID`
`terminal`
`execute_code`

## Context Compression (config.yaml only)​

Context compression is configured exclusively throughconfig.yaml— there are no environment variables for it. Threshold settings live in thecompression:block, while the summarization model/provider lives underauxiliary.compression:.

`config.yaml`
`compression:`
`auxiliary.compression:`

```
compression:  enabled: true  threshold: 0.50  target_ratio: 0.20         # fraction of threshold to preserve as recent tail  protect_last_n: 20         # minimum recent messages to keep uncompressed
```

Older configs withcompression.summary_model,compression.summary_provider, andcompression.summary_base_urlare automatically migrated toauxiliary.compression.*on first load.

`compression.summary_model`
`compression.summary_provider`
`compression.summary_base_url`
`auxiliary.compression.*`

## Auxiliary Task Overrides​

| Variable | Description |
| --- | --- |
| AUXILIARY_VISION_PROVIDER | Override provider for vision tasks |
| AUXILIARY_VISION_MODEL | Override model for vision tasks |
| AUXILIARY_VISION_BASE_URL | Direct OpenAI-compatible endpoint for vision tasks |
| AUXILIARY_VISION_API_KEY | API key paired withAUXILIARY_VISION_BASE_URL |
| AUXILIARY_WEB_EXTRACT_PROVIDER | Override provider for web extraction/summarization |
| AUXILIARY_WEB_EXTRACT_MODEL | Override model for web extraction/summarization |
| AUXILIARY_WEB_EXTRACT_BASE_URL | Direct OpenAI-compatible endpoint for web extraction/summarization |
| AUXILIARY_WEB_EXTRACT_API_KEY | API key paired withAUXILIARY_WEB_EXTRACT_BASE_URL |

`AUXILIARY_VISION_PROVIDER`
`AUXILIARY_VISION_MODEL`
`AUXILIARY_VISION_BASE_URL`
`AUXILIARY_VISION_API_KEY`
`AUXILIARY_VISION_BASE_URL`
`AUXILIARY_WEB_EXTRACT_PROVIDER`
`AUXILIARY_WEB_EXTRACT_MODEL`
`AUXILIARY_WEB_EXTRACT_BASE_URL`
`AUXILIARY_WEB_EXTRACT_API_KEY`
`AUXILIARY_WEB_EXTRACT_BASE_URL`

For task-specific direct endpoints, Hermes uses the task's configured API key orOPENAI_API_KEY. It does not reuseOPENROUTER_API_KEYfor those custom endpoints.

`OPENAI_API_KEY`
`OPENROUTER_API_KEY`

## Fallback Providers (config.yaml only)​

The primary model fallback chain is configured exclusively throughconfig.yaml— there are no environment variables for it. Add a top-levelfallback_providerslist withproviderandmodelkeys to enable automatic failover when your main model encounters errors. Auxiliary tasks whose provider isautoalso consult this chain before Hermes' built-in auxiliary discovery chain.

`config.yaml`
`fallback_providers`
`provider`
`model`
`auto`

```
fallback_providers:  - provider: openrouter    model: anthropic/claude-sonnet-4
```

The older top-levelfallback_modelsingle-provider shape is still read for backward compatibility, but new configuration should usefallback_providers. For task-specific auxiliary policy, useauxiliary.<task>.fallback_chaininconfig.yaml; there is no environment variable equivalent.

`fallback_model`
`fallback_providers`
`auxiliary.<task>.fallback_chain`
`config.yaml`

SeeFallback Providersfor full details.

## Provider Routing (config.yaml only)​

These go in~/.hermes/config.yamlunder theprovider_routingsection:

`~/.hermes/config.yaml`
`provider_routing`
| Key | Description |
| --- | --- |
| sort | Sort providers:"price"(default),"throughput", or"latency" |
| only | List of provider slugs to allow (e.g.,["anthropic", "google"]) |
| ignore | List of provider slugs to skip |
| order | List of provider slugs to try in order |
| require_parameters | Only use providers supporting all request params (true/false) |
| data_collection | "allow"(default) or"deny"to exclude data-storing providers |

`sort`
`"price"`
`"throughput"`
`"latency"`
`only`
`["anthropic", "google"]`
`ignore`
`order`
`require_parameters`
`true`
`false`
`data_collection`
`"allow"`
`"deny"`

Usehermes config setto set environment variables — it automatically saves them to the right file (.envfor secrets,config.yamlfor everything else).

`hermes config set`
`.env`
`config.yaml`