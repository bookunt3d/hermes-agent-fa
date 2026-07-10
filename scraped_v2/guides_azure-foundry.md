- 
- Guides & Tutorials
- Microsoft Foundry

# Microsoft Foundry

Hermes Agent'sazure-foundryprovider supports Microsoft Foundry (formerly Azure AI Foundry) and Azure OpenAI. A single Foundry resource can host models with two different wire formats:

`azure-foundry`
- OpenAI-style—POST /v1/chat/completionson endpoints likehttps://<resource>.openai.azure.com/openai/v1. Used for GPT-4.x, GPT-5.x, Llama, Mistral, and most open-weight models.
- Anthropic-style—POST /v1/messageson endpoints likehttps://<resource>.services.ai.azure.com/anthropic. Used when Microsoft Foundry serves Claude models via the Anthropic Messages API format.

`POST /v1/chat/completions`
`https://<resource>.openai.azure.com/openai/v1`
`POST /v1/messages`
`https://<resource>.services.ai.azure.com/anthropic`

The setup wizard probes your endpoint and auto-detects which transport it uses, which deployments are available, and each model's context length.

## Prerequisites​

- A Microsoft Foundry or Azure OpenAI resource with at least one deployment
- The deployment's endpoint URL
- Eitheran API key (from the Azure Portal under "Keys and Endpoint")ortheAzure AI UserRBAC role on the Foundry resource if you plan to use Microsoft Entra ID (the keyless path Microsoft recommends). Some tenants may show the role asFoundry Userduring Microsoft's rename rollout.

## Quick Start​

```
hermes model# → Select "Azure Foundry"# → Enter your endpoint URL# → Choose Authentication:#     1. API key#     2. Microsoft Entra ID  (managed identity / workload identity / az login)# → (Entra) Hermes probes DefaultAzureCredential; on success it never asks for a key# → (API key) Enter your API key# Hermes probes the endpoint and auto-detects transport + models# → Pick a model from the list (or type a deployment name manually)
```

The wizard will:

1. Sniff the URL path— URLs ending in/anthropicare recognised as Microsoft Foundry Claude routes.
2. ProbeGET <base>/models— if the endpoint returns an OpenAI-shaped model list, Hermes switches tochat_completionsand prefills a picker with the returned deployment IDs.
3. Probe Anthropic Messages shape— fallback for endpoints that do not expose/modelsbut do accept the Anthropic Messages format.
4. Fall back to manual entry— private/gated endpoints that reject every probe still work; you pick the API mode and type a deployment name by hand.

`/anthropic`
`GET <base>/models`
`chat_completions`
`/models`

Context length for the chosen model is resolved via Hermes' standard metadata chain (models.dev, provider metadata, and hardcoded family fallbacks) and stored inconfig.yamlso the model can size its own context window correctly.

`models.dev`
`config.yaml`

## Microsoft Entra ID (keyless, RBAC) — recommended​

Microsoft recommendskeyless authentication with Microsoft Entra IDfor production Foundry workloads. Hermes supports Entra ID forbothAPI surfaces:

- OpenAI-style(api_mode: chat_completions/codex_responses) — GPT-4/5, Llama, Mistral, DeepSeek, etc.
- Anthropic-style(api_mode: anthropic_messages) — Claude models on Microsoft Foundry.

`api_mode: chat_completions`
`codex_responses`
`api_mode: anthropic_messages`

Foundry's RBAC is per-resource (Azure AI Usergrants both surfaces; some tenants may displayFoundry User) and Microsoft documents the same inference scope (https://ai.azure.com/.default) for both. Under the hood:

`Azure AI User`
`Foundry User`
`https://ai.azure.com/.default`
- OpenAI-style uses the OpenAI Python SDK's native callableapi_key=contract — the SDK mints a fresh JWT per request automatically.
- Anthropic-style uses anhttpx.Clientwith a request event hook installed byagent.azure_identity_adapter.build_bearer_http_client, because the Anthropic SDK does not accept callableauth_tokennatively. The hook rewritesAuthorization: Bearer <fresh-jwt>per outbound request. Same Microsoft RBAC, same Foundry scope — the SDK contract is the only difference.

`api_key=`
`httpx.Client`
`agent.azure_identity_adapter.build_bearer_http_client`
`auth_token`
`Authorization: Bearer <fresh-jwt>`

### Why use Entra ID?​

- No long-lived API keys to rotate or revoke.
- RBAC-driven access — grant or removeAzure AI Useron the Foundry resource, no config rewrite needed.
- Access and audit logs are segmented by assignee instead of all callers sharing one static key.
- Single auth surface for Azure VMs, AKS pods, App Service, Functions, Container Apps, and Foundry Agent Service via managed identity.
- Workload identity and service-principal flows for CI/CD pipelines.

`Azure AI User`

### One-time setup (Azure side)​

1. In the Azure Portal, open your Foundry resource →Access control (IAM)→Add → Add role assignment.
2. Pick theAzure AI Userrole (orFoundry Userif your tenant has the renamed role).
3. Assign it to:Your user accountfor local development withaz login.A managed identity or workload identityfor Azure-hosted compute (recommended for production).A Foundry Agent Service hosted agent's agent identitywhen Hermes runs inside a hosted agent.A service principalfor CI/CD pipelines when workload identity is not available.
4. Wait ~5 minutes for the role to propagate.

- Your user accountfor local development withaz login.
- A managed identity or workload identityfor Azure-hosted compute (recommended for production).
- A Foundry Agent Service hosted agent's agent identitywhen Hermes runs inside a hosted agent.
- A service principalfor CI/CD pipelines when workload identity is not available.

`az login`

Azure CLI equivalent:

```
az role assignment create \  --assignee <principal-or-agent-identity-client-id> \  --role "Azure AI User" \  --scope <foundry-resource-id>
```

### One-time setup (Hermes side)​

```
hermes model# → Select "Azure Foundry"# → Enter your endpoint URL# → Authentication: 2 (Microsoft Entra ID)# → (optional) user-assigned managed identity client ID# → (optional) Azure tenant ID# → Hermes probes DefaultAzureCredential() and reports which inner#    credential succeeded (e.g. AzureCliCredential, ManagedIdentityCredential)
```

The wizard runs a bounded preflight probe (10 s timeout). On failure it offers to "save anyway, validate later" — useful when configuring on a machine that doesn't yet have credentials but will at runtime (e.g. preparing config for a managed-identity deployment).

azure-identityis installed automatically on first use via Hermes' lazy-install path. To pre-install:

`azure-identity`

```
pip install azure-identity
```

### Configuration written toconfig.yaml​

`config.yaml`

```
model:  provider: azure-foundry  base_url: https://my-resource.openai.azure.com/openai/v1  api_mode: chat_completions  auth_mode: entra_id  default: gpt-4o  context_length: 128000  entra:    scope: https://ai.azure.com/.default        # only when overriding the default
```

Hermes only manages one Entra-specific knob inconfig.yaml:

`config.yaml`
- scope— the OAuth resource scope. Defaults to Microsoft's documented inference scope (https://ai.azure.com/.default). Override only if your resource was provisioned against a non-standard audience.

`scope`
`https://ai.azure.com/.default`

Everything else (tenant, service principal secret, federated token file, sovereign cloud authority, broker preferences) is read byazure-identitydirectly from the standardAZURE_*environment variables — see thecredential resolution orderbelow. Set those in~/.hermes/.envor your deployment environment, exactly as Microsoft's SDK reference describes.

`azure-identity`
`AZURE_*`
`~/.hermes/.env`

No secrets land in~/.hermes/.envfor Entra mode —azure-identitycaches tokens in-process (and where available, in your OS keychain /~/.IdentityService).

`~/.hermes/.env`
`azure-identity`
`~/.IdentityService`

### Credential resolution order​

azure-identity'sDefaultAzureCredentialwalks this chain on each token request, stopping at the first credential that returns a token:

`azure-identity`
`DefaultAzureCredential`
1. Environment credential—AZURE_TENANT_ID+AZURE_CLIENT_ID+AZURE_CLIENT_SECRET(orAZURE_CLIENT_CERTIFICATE_PATH/AZURE_FEDERATED_TOKEN_FILE).
2. Workload Identity—AZURE_FEDERATED_TOKEN_FILE(AKS federated tokens / OIDC).
3. Managed Identity— IMDS endpoint (169.254.169.254) for virtual machines;IDENTITY_ENDPOINTfor App Service / Functions / Container Apps. Foundry Agent Service hosted agents use the hosted agent's agent identity.
4. Visual Studio Code— Azure account extension.
5. Azure CLI—az loginsession.
6. Azure Developer CLI—azd auth login.
7. Azure PowerShell—Connect-AzAccount.
8. Broker(Windows / WSL only) — Web Account Manager.

`AZURE_TENANT_ID`
`AZURE_CLIENT_ID`
`AZURE_CLIENT_SECRET`
`AZURE_CLIENT_CERTIFICATE_PATH`
`AZURE_FEDERATED_TOKEN_FILE`
`AZURE_FEDERATED_TOKEN_FILE`
`169.254.169.254`
`IDENTITY_ENDPOINT`
`az login`
`azd auth login`
`Connect-AzAccount`

Interactive browser credential is excluded by default for unattended Hermes runs; use Azure CLI, Azure Developer CLI, managed identity, workload identity, or service principal credentials instead.

### Deployment patterns​

Local development:

```
az loginhermes model   # pick Azure Foundry → Entra IDhermes         # uses your az login token
```

Azure VM / Functions / App Service / Container Apps (system-assigned managed identity):

1. Enable system-assigned identity on the compute resource.
2. Grant the identityAzure AI User(orFoundry User) on the Foundry resource.
3. Setmodel.auth_mode: entra_idin config.yaml — no env vars needed.

`Azure AI User`
`Foundry User`
`model.auth_mode: entra_id`

Azure VM / Functions / App Service / Container Apps (user-assigned managed identity):

- SetAZURE_CLIENT_IDto the user-assigned identity's client ID soDefaultAzureCredentialpicks the right one.

`AZURE_CLIENT_ID`
`DefaultAzureCredential`

Foundry Agent Service hosted agent:

- Create the hosted agent and grant that agent's identityAzure AI User(orFoundry User) on the Foundry resource. Hermes usesManagedIdentityCredentialfrom inside the hosted agent; role assignment belongs on the agent identity, not just the parent project or your user.

`Azure AI User`
`Foundry User`
`ManagedIdentityCredential`

AKS Workload Identity (replaces AAD Pod Identity):

- Annotate the pod's service account with the workload identity client ID.
- The pod's federated token file is auto-detected viaAZURE_FEDERATED_TOKEN_FILE.
- model.auth_mode: entra_idworks without further config changes.

`AZURE_FEDERATED_TOKEN_FILE`
`model.auth_mode: entra_id`

Service principal in CI:

- SetAZURE_TENANT_ID,AZURE_CLIENT_ID,AZURE_CLIENT_SECRETin the runner env.

`AZURE_TENANT_ID`
`AZURE_CLIENT_ID`
`AZURE_CLIENT_SECRET`

#### Sovereign clouds (Government, China)​

ExportAZURE_AUTHORITY_HOST(e.g.https://login.microsoftonline.usfor Azure Government,https://login.partner.microsoftonline.cnfor Azure China).azure-identityreads it directly.

`AZURE_AUTHORITY_HOST`
`https://login.microsoftonline.us`
`https://login.partner.microsoftonline.cn`
`azure-identity`

### Health checks​

hermes doctorruns a 10 s probe againstDefaultAzureCredentialwhenmodel.auth_mode: entra_id, reporting which inner credential won (env vars present, managed identity endpoint reachable, etc.).

`hermes doctor`
`DefaultAzureCredential`
`model.auth_mode: entra_id`

hermes authshows a structured status block:

`hermes auth`

```
azure-foundry (Microsoft Entra ID):  Endpoint: https://my-resource.openai.azure.com/openai/v1  Scope: https://ai.azure.com/.default  Status: configured; live token probe is skipped here
```

### Limitations​

- Anthropic-style endpoints use an httpx event hook.The Anthropic Python SDK does not accept a callableauth_tokennatively (≤ 0.86.0). Hermes installs a request event hook on a customhttpx.Clientthat mints a fresh JWT per outbound request and rewritesAuthorization: Bearer <jwt>. This is functionally equivalent to the OpenAI SDK's nativeCallable[[], str]contract but adds one indirection layer. If the Anthropic SDK adds first-class callable-auth support in a future release, Hermes will switch to it transparently.
- Batch jobs andmultiprocessing.Pool.The Entra token provider is a closure that cannot be pickled across process boundaries.batch_runner.pyautomatically drops the callable from the worker config and lets each worker process rebuild its own provider fromconfig.yaml— no user action required, but each worker pays one chain walk at startup.
- No bearer JWT persistence inauth.json.Hermes does not duplicateazure-identity's internal token cache; cold starts walk the credential chain on first inference.

`auth_token`
`httpx.Client`
`Authorization: Bearer <jwt>`
`Callable[[], str]`
`multiprocessing.Pool`
`batch_runner.py`
`config.yaml`
`auth.json`
`azure-identity`

## Configuration (written toconfig.yaml)​

`config.yaml`

After running the wizard you'll see something like this:

```
model:  provider: azure-foundry  base_url: https://my-resource.openai.azure.com/openai/v1  api_mode: chat_completions         # or "anthropic_messages"  default: gpt-5.4-mini              # your deployment / model name  context_length: 400000             # auto-detected
```

And in~/.hermes/.env:

`~/.hermes/.env`

```
AZURE_FOUNDRY_API_KEY=<your-azure-key>
```

## OpenAI-style endpoints (GPT, Llama, etc.)​

Azure OpenAI's v1 GA endpoint accepts the standardopenaiPython client with minimal changes:

`openai`

```
model:  provider: azure-foundry  base_url: https://my-resource.openai.azure.com/openai/v1  api_mode: chat_completions  default: gpt-5.4
```

Important behaviour:

- GPT-5.x, codex, and o-series auto-route to the Responses API.Microsoft Foundry deploys GPT-5 / codex / o1 / o3 / o4 models as Responses-API-only — calling/chat/completionsagainst them returns400 "The requested operation is unsupported.". Hermes detects these model families by name and upgradesapi_modetocodex_responsestransparently, even whenconfig.yamlstill readsapi_mode: chat_completions. GPT-4, GPT-4o, Llama, Mistral, and other deployments stay on/chat/completions.
- max_completion_tokensis used automatically.Azure OpenAI (like direct OpenAI) requiresmax_completion_tokensfor gpt-4o, o-series, and gpt-5.x models. Hermes sends the right parameter based on the endpoint.
- Pre-v1 endpoints that requireapi-version.If you have a legacy base URL likehttps://<resource>.openai.azure.com/openai?api-version=2025-04-01-preview, Hermes extracts the query string and forwards it viadefault_queryon every request (the OpenAI SDK otherwise drops it when joining paths).

`/chat/completions`
`400 "The requested operation is unsupported."`
`api_mode`
`codex_responses`
`config.yaml`
`api_mode: chat_completions`
`/chat/completions`
`max_completion_tokens`
`max_completion_tokens`
`api-version`
`https://<resource>.openai.azure.com/openai?api-version=2025-04-01-preview`
`default_query`

## Anthropic-style endpoints (Claude via Microsoft Foundry)​

For Claude deployments, use the Anthropic-style route:

```
model:  provider: azure-foundry  base_url: https://my-resource.services.ai.azure.com/anthropic  api_mode: anthropic_messages  default: claude-sonnet-4-6
```

Important behaviour:

- /v1is stripped from the base URL.The Anthropic SDK appends/v1/messagesto every request URL — Hermes removes any trailing/v1before handing the URL to the SDK to avoid double-/v1paths.
- api-versionis sent viadefault_query, not appended to the URL.Azure Anthropic requires anapi-versionquery string. Baking it into the base URL produces malformed paths like/anthropic?api-version=.../v1/messagesand returns 404. Hermes passesapi-version=2025-04-15via the Anthropic SDK'sdefault_queryinstead.
- Bearer auth is used instead ofx-api-key.Azure's Anthropic-compatible route requiresAuthorization: Bearer <key>rather than Anthropic's nativex-api-keyheader. Hermes detectsazure.comin the base URL and routes the API key through the SDK'sauth_tokenfield so the right header reaches the upstream.
- 1M context window beta header is kept.Azure still gates the 1M-token Claude context (Opus 4.6/4.7, Sonnet 4.6) behind theanthropic-beta: context-1m-2025-08-07header. Hermes keeps that beta header on Azure paths (it's stripped from native Anthropic OAuth requests because some subscriptions reject it, but Azure requires it).
- OAuth token refresh is disabled.Azure deployments use static API keys. The~/.claude/.credentials.jsonOAuth token refresh loop that applies to Anthropic Console is explicitly skipped for Azure endpoints to prevent the Claude Code OAuth token from overwriting your Azure key mid-session.

`/v1`
`/v1/messages`
`/v1`
`/v1`
`api-version`
`default_query`
`api-version`
`/anthropic?api-version=.../v1/messages`
`api-version=2025-04-15`
`default_query`
`x-api-key`
`Authorization: Bearer <key>`
`x-api-key`
`azure.com`
`auth_token`
`anthropic-beta: context-1m-2025-08-07`
`~/.claude/.credentials.json`

## Alternative:provider: anthropic+ Azure base URL​

`provider: anthropic`

If you already haveprovider: anthropicconfigured and just want to point it at Microsoft Foundry for Claude, you can skip theazure-foundryprovider entirely:

`provider: anthropic`
`azure-foundry`

```
model:  provider: anthropic  base_url: https://my-resource.services.ai.azure.com/anthropic  key_env: AZURE_ANTHROPIC_KEY  default: claude-sonnet-4-6
```

WithAZURE_ANTHROPIC_KEYset in~/.hermes/.env. Hermes detectsazure.comin the base URL and short-circuits around the Claude Code OAuth token chain so the Azure key is used directly withx-api-keyauth.

`AZURE_ANTHROPIC_KEY`
`~/.hermes/.env`
`azure.com`
`x-api-key`

key_envis the canonical snake_case field name;api_key_env(and the camelCasekeyEnv/apiKeyEnv) are accepted as aliases. If bothkey_envandAZURE_ANTHROPIC_KEY/ANTHROPIC_API_KEYare set, thekey_env-named env var wins.

`key_env`
`api_key_env`
`keyEnv`
`apiKeyEnv`
`key_env`
`AZURE_ANTHROPIC_KEY`
`ANTHROPIC_API_KEY`
`key_env`

## Model discovery​

Azure doesnotexpose a pure-API-key endpoint to list yourdeployedmodel deployments. Deployment enumeration requires Azure Resource Manager authentication (az cognitiveservices account deployment list) with an Azure AD principal, not the inference API key.

`az cognitiveservices account deployment list`

What Hermes can do:

- Azure OpenAI v1 endpoints (<resource>.openai.azure.com/openai/v1) exposeGET /modelswith the resource'savailablemodel catalog. Hermes uses this list to prefill the model picker.
- Microsoft Foundry/anthropicroutes: detected via URL path, model name entered manually.
- Private / firewalled endpoints: manual entry with a friendly "couldn't probe" message.

`<resource>.openai.azure.com/openai/v1`
`GET /models`
`/anthropic`

You can always type a deployment name directly — Hermes does not validate against the returned list.

## Environment variables​

| Variable | Purpose |
| --- | --- |
| AZURE_FOUNDRY_API_KEY | Primary API key for Microsoft Foundry / Azure OpenAI (api_key mode) |
| AZURE_FOUNDRY_BASE_URL | Endpoint URL (set viahermes model; env var is used as a fallback) |
| AZURE_ANTHROPIC_KEY | Used byprovider: anthropic+ Azure base URL (alternative toANTHROPIC_API_KEY) |
| AZURE_TENANT_ID | Entra ID tenant for service-principal flows |
| AZURE_CLIENT_ID | Entra ID client ID (service principal, workload identity, or user-assigned managed identity) |
| AZURE_CLIENT_SECRET | Service principal secret |
| AZURE_CLIENT_CERTIFICATE_PATH | Service principal cert (alternative to secret) |
| AZURE_FEDERATED_TOKEN_FILE | Workload Identity federated token path (AKS) |
| AZURE_AUTHORITY_HOST | Sovereign cloud authority host override |
| IDENTITY_ENDPOINT/MSI_ENDPOINT | Managed Identity endpoint for App Service, Functions, and Container Apps; VMs usually use IMDS instead |

`AZURE_FOUNDRY_API_KEY`
`AZURE_FOUNDRY_BASE_URL`
`hermes model`
`AZURE_ANTHROPIC_KEY`
`provider: anthropic`
`ANTHROPIC_API_KEY`
`AZURE_TENANT_ID`
`AZURE_CLIENT_ID`
`AZURE_CLIENT_SECRET`
`AZURE_CLIENT_CERTIFICATE_PATH`
`AZURE_FEDERATED_TOKEN_FILE`
`AZURE_AUTHORITY_HOST`
`IDENTITY_ENDPOINT`
`MSI_ENDPOINT`

The Azure SDK reads theAZURE_*env vars directly. Hermes never inspects them other than to report which sources are present inhermes doctoroutput.

`AZURE_*`
`hermes doctor`

## Troubleshooting​

401 Unauthorized on gpt-5.x deployments.Azure serves gpt-5.x on/chat/completions, not/responses. Hermes handles this automatically when the URL containsopenai.azure.com, but if you see a 401 with anInvalid API keybody, check thatapi_modein yourconfig.yamlischat_completions.

`/chat/completions`
`/responses`
`openai.azure.com`
`Invalid API key`
`api_mode`
`config.yaml`
`chat_completions`

404 on/v1/messages?api-version=.../v1/messages.This is the malformed-URL bug from pre-fix Azure Anthropic setups. Upgrade Hermes — theapi-versionparameter is now passed viadefault_queryrather than baked into the base URL, so the SDK can't corrupt it during URL joining.

`/v1/messages?api-version=.../v1/messages`
`api-version`
`default_query`

Wizard says "Auto-detection incomplete."The endpoint rejected both the/modelsprobe and the Anthropic Messages probe. This is normal for private endpoints behind a firewall or with an IP allow-list. Fall back to manual API mode selection and type your deployment name — everything still works, Hermes just can't prefill the picker.

`/models`

Wrong transport picked.Runhermes modelagain and the wizard will re-probe. If the probe still picks the wrong mode, you can editconfig.yamldirectly:

`hermes model`
`config.yaml`

```
model:  provider: azure-foundry  api_mode: anthropic_messages   # or chat_completions
```

Entra ID: "credential chain exhausted" or 401 Unauthorized after switching toauth_mode: entra_id.

`auth_mode: entra_id`
- Runaz loginto refresh your developer session (the cached token may have expired).
- Verify theAzure AI User(orFoundry User) role assignment took effect:az role assignment list --assignee <user-or-identity-id>should list it on your Foundry resource. Role propagation can take up to 5 minutes.
- For user-assigned managed identities, double-checkAZURE_CLIENT_IDmatches the identity attached to the compute resource.
- Runhermes doctor— the Azure Entra probe reports whether token acquisition succeeded and includes a remediation hint.

`az login`
`Azure AI User`
`Foundry User`
`az role assignment list --assignee <user-or-identity-id>`
`AZURE_CLIENT_ID`
`hermes doctor`

Entra ID: wizard preflight hangs or times out.The 10 s preflight is a soft check. Choose "Save anyway and validate later" and runhermes doctorafter deploying to the target environment. Common causes include an unreachable token service or stale local login state — prefer workload identity in CI, setAZURE_TENANT_ID+AZURE_CLIENT_ID+AZURE_CLIENT_SECRETwhen using a service principal, or runaz loginfor local development.

`hermes doctor`
`AZURE_TENANT_ID`
`AZURE_CLIENT_ID`
`AZURE_CLIENT_SECRET`
`az login`

401 on Anthropic-style endpoint with Entra ID.Verify the sameAzure AI User(orFoundry User) role is assigned on the Foundry resource (it covers both/openai/v1and/anthropicpaths). If the OpenAI-style probe works during the wizard butclaude-*requests fail at runtime, the most common cause is a stalemodel.entra.scopeleft over from an earlier wizard run — delete theentra.scopeline fromconfig.yamlso the runtime falls back to the defaulthttps://ai.azure.com/.defaultscope.

`Azure AI User`
`Foundry User`
`/openai/v1`
`/anthropic`
`claude-*`
`model.entra.scope`
`entra.scope`
`config.yaml`
`https://ai.azure.com/.default`

## Related​

- Environment variables
- Configuration
- AWS Bedrock— the other major cloud provider integration
- Microsoft: Configure Entra ID for Foundry— upstream documentation for the keyless path