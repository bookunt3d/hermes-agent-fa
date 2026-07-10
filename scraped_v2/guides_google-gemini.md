# Google Gemini

Hermes Agent supports Google Gemini as a native provider using theGoogle AI Studio / Gemini API— not the OpenAI-compatible endpoint. This lets Hermes translate its internal OpenAI-shaped message and tool loop into Gemini's nativegenerateContentAPI while preserving tool calling, streaming, multimodal inputs, and Gemini-specific response metadata.

`generateContent`

## Prerequisites​

- Google AI Studio API key— create one ataistudio.google.com/apikey
- Billing-enabled Google Cloud project— recommended for agent use. Gemini's free tier is too small for long-running agent sessions because Hermes may make several model calls per user turn.
- Hermes installed— no extra Python package is required for the native Gemini provider.

SetGOOGLE_API_KEYorGEMINI_API_KEY. Hermes checks both names for thegeminiprovider.

`GOOGLE_API_KEY`
`GEMINI_API_KEY`
`gemini`

## Quick Start​

```
# Add your Gemini API keyecho "GOOGLE_API_KEY=..." >> ~/.hermes/.env# Select Gemini as your providerhermes model# → Choose "More providers..." → "Google AI Studio"# → Hermes checks your key tier and shows Gemini models# → Select a model# Start chattinghermes chat
```

If you prefer direct config editing, use the native Gemini API base URL:

```
model:  default: gemini-3-flash-preview  provider: gemini  base_url: https://generativelanguage.googleapis.com/v1beta
```

## Configuration​

After runninghermes model, your~/.hermes/config.yamlwill contain:

`hermes model`
`~/.hermes/config.yaml`

```
model:  default: gemini-3-flash-preview  provider: gemini  base_url: https://generativelanguage.googleapis.com/v1beta
```

And in~/.hermes/.env:

`~/.hermes/.env`

```
GOOGLE_API_KEY=...
```

### Native Gemini API​

The recommended endpoint is:

```
https://generativelanguage.googleapis.com/v1beta
```

Hermes detects this endpoint and creates its native Gemini adapter. Internally, Hermes still keeps the agent loop in OpenAI-shaped messages, then translates each request to Gemini's native schema:

- messages[]→ Geminicontents[]
- system prompts → GeminisystemInstruction
- tool schemas → GeminifunctionDeclarations
- tool results → GeminifunctionResponseparts
- streaming responses → OpenAI-shaped stream chunks for the Hermes loop

`messages[]`
`contents[]`
`systemInstruction`
`functionDeclarations`
`functionResponse`

For Gemini 3 tool use, Hermes preserves thethoughtSignaturevalues attached to function-call parts and replays them on the next tool turn. That covers the validation-critical path for multi-step agent workflows.

`thoughtSignature`

Gemini 3 may also attach thought signatures to other response parts. Hermes' native adapter is optimized for agent tool loops today, so it does not yet replay every non-tool-call signature with full part-level fidelity.

### Prefer the Native Endpoint​

Google also exposes an OpenAI-compatible endpoint:

```
https://generativelanguage.googleapis.com/v1beta/openai/
```

For Hermes agent sessions, prefer the native Gemini endpoint above. Hermes includes a native Gemini adapter so it can map multi-turn tool use, tool-call results, streaming, multimodal inputs, and Gemini response metadata directly onto Gemini'sgenerateContentAPI. The OpenAI-compatible endpoint is still useful when you specifically need OpenAI API compatibility.

`generateContent`

If you previously setGEMINI_BASE_URLto the/openaiURL, remove it or change it:

`GEMINI_BASE_URL`
`/openai`

```
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

## Available Models​

Thehermes modelpicker shows Gemini models maintained in Hermes' provider registry. Common choices include:

`hermes model`
| Model | ID | Notes |
| --- | --- | --- |
| Gemini 3.1 Pro Preview | gemini-3.1-pro-preview | Most capable preview model when available |
| Gemini 3 Pro Preview | gemini-3-pro-preview | Strong reasoning and coding model |
| Gemini 3 Flash Preview | gemini-3-flash-preview | Recommended default balance of speed and capability |
| Gemini 3.1 Flash Lite Preview | gemini-3.1-flash-lite-preview | Fastest / lowest-cost option when available |

`gemini-3.1-pro-preview`
`gemini-3-pro-preview`
`gemini-3-flash-preview`
`gemini-3.1-flash-lite-preview`

Model availability changes over time. If a model disappears or is not enabled for your key, runhermes modelagain and pick one from the current list.

`hermes model`

Use Gemini's native model IDs such asgemini-3-flash-preview, not OpenRouter-style IDs likegoogle/gemini-3-flash-preview, whenprovider: gemini.

`gemini-3-flash-preview`
`google/gemini-3-flash-preview`
`provider: gemini`

### Latest Aliases​

Google publishes moving aliases for the Pro and Flash Gemini families.gemini-pro-latestandgemini-flash-latestare useful when you want Google to advance the model automatically without changing your Hermes config.

`gemini-pro-latest`
`gemini-flash-latest`
| Alias | Currently tracks | Notes |
| --- | --- | --- |
| gemini-pro-latest | Latest Gemini Pro model | Best when you want Google's current Pro default |
| gemini-flash-latest | Latest Gemini Flash model | Best when you want Google's current Flash default |

`gemini-pro-latest`
`gemini-flash-latest`

```
model:  default: gemini-pro-latest  provider: gemini  base_url: https://generativelanguage.googleapis.com/v1beta
```

If you need strict reproducibility, prefer explicit model IDs such asgemini-3.1-pro-previeworgemini-3-flash-preview.

`gemini-3.1-pro-preview`
`gemini-3-flash-preview`

### Gemma via the Gemini API​

Google also exposes Gemma models through the Gemini API. Hermes recognizes these as Google models, but hides very low-throughput Gemma entries from the default model picker so new users do not accidentally select an evaluation-tier model for a long-running agent session.

Useful evaluation IDs include:

| Model | ID | Notes |
| --- | --- | --- |
| Gemma 4 31B IT | gemma-4-31b-it | Larger Gemma model; useful for compatibility and quality evaluation |
| Gemma 4 26B A4B IT | gemma-4-26b-a4b-it | Smaller active-parameter variant when available |

`gemma-4-31b-it`
`gemma-4-26b-a4b-it`

These models are best treated as evaluation options on Gemini API keys. Google's Gemma API pricing is free-tier-only and the usage caps are low compared with production Gemini models, so sustained Hermes agent use should normally move to a paid Gemini model, a self-hosted deployment, or another provider with appropriate quota.

To use a Gemma model that is hidden from the picker, set it directly:

```
model:  default: gemma-4-31b-it  provider: gemini  base_url: https://generativelanguage.googleapis.com/v1beta
```

## Switching Models Mid-Session​

Use the/modelcommand during a conversation:

`/model`

```
/model gemini-3-flash-preview/model gemini-flash-latest/model gemini-3-pro-preview/model gemini-pro-latest/model gemma-4-31b-it/model gemini-3.1-flash-lite-preview
```

If you have not configured Gemini yet, exit the session and runhermes modelfirst./modelswitches among already-configured providers and models; it does not collect new API keys.

`hermes model`
`/model`

## Diagnostics​

```
hermes doctor
```

The doctor checks:

- WhetherGOOGLE_API_KEYorGEMINI_API_KEYis available
- Whether configured provider credentials can be resolved

`GOOGLE_API_KEY`
`GEMINI_API_KEY`

## Gateway (Messaging Platforms)​

Gemini works with all Hermes gateway platforms (Telegram, Discord, Slack, WhatsApp, LINE, Feishu, etc.). Configure Gemini as your provider, then start the gateway normally:

```
hermes gateway setuphermes gateway start
```

The gateway readsconfig.yamland uses the same Gemini provider configuration.

`config.yaml`

## Troubleshooting​

### "Gemini native client requires an API key"​

Hermes could not find a usable API key. Add one of these to~/.hermes/.env:

`~/.hermes/.env`

```
GOOGLE_API_KEY=...# orGEMINI_API_KEY=...
```

Then runhermes modelagain.

`hermes model`

### "This Google API key is on the free tier"​

Hermes probes Gemini API keys during setup. Free-tier quotas can be exhausted after a handful of agent turns because tool use, retries, compression, and auxiliary tasks may require multiple model calls.

Enable billing on the Google Cloud project attached to your key, regenerate the key if needed, then run:

```
hermes model
```

### "404 model not found"​

The selected model is not available for your account, region, or key. Runhermes modelagain and pick another Gemini model from the current list.

`hermes model`

### Gemma model is not shown inhermes model​

`hermes model`

Hermes may hide low-throughput Gemma models from the picker by default. If you intentionally want to evaluate one, set the model ID directly in~/.hermes/config.yaml.

`~/.hermes/config.yaml`

### "429 quota exceeded" on Gemma​

Gemma models exposed through the Gemini API are useful for evaluation, but their Gemini API free-tier caps are low. Use them for compatibility testing, then switch to a paid Gemini model or another provider for sustained agent sessions.

### OpenAI-compatible endpoint is configured​

Check~/.hermes/.envfor:

`~/.hermes/.env`

```
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

Change it to the native endpoint or remove the override:

```
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

### Tool calling fails with schema errors​

Upgrade Hermes and rerunhermes model. The native Gemini adapter sanitizes tool schemas for Gemini's stricter function-declaration format; older builds or custom endpoints may not.

`hermes model`

## Related​

- AI Providers
- Configuration
- Fallback Providers
- AWS Bedrock— native cloud-provider integration using AWS credentials