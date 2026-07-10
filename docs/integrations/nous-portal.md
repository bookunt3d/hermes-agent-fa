---
layout: docs
title: "Nous Portal"
permalink: /integrations/nous-portal/
---

- 
- Integrations
- Nous Portal

# Nous Portal

Nous Portalis Nous Research's unified subscription gateway andthe recommended way to run Hermes Agent. One OAuth login replaces the juggling act of separate accounts, API keys, and billing relationships across every model lab, search API, image generator, and browser provider you'd otherwise need to wire up by hand.

[Nous Portal](https://portal.nousresearch.com)

If you only have time to set up one thing, set up this. The fastest path:

```
hermes setup --portal
```

That single command runs the Portal OAuth, lets you pick a Nous model, sets Nous as your inference provider inconfig.yaml, and turns on the Tool Gateway. You're ready tohermes chatimmediately after.

`config.yaml`
`hermes chat`

Don't have a subscription yet?portal.nousresearch.com/manage-subscription— sign up, then come back and run the command above.

[portal.nousresearch.com/manage-subscription](https://portal.nousresearch.com/manage-subscription)

## What's in the subscription​

### 300+ frontier models, one bill​

The Portal proxies a curated catalog of agentic models from across the ecosystem — billed against your Nous subscription instead of one credit balance per lab.

| Family | Models |
| --- | --- |
| Anthropic Claude | Opus 4.7, Opus 4.6, Sonnet 4.6, Haiku 4.5 |
| OpenAI | GPT-5.5, GPT-5.5 Pro, GPT-5.4 Mini, GPT-5.4 Nano, GPT-5.3 Codex |
| Google Gemini | Gemini 3 Pro Preview, Gemini 3 Flash Preview, Gemini 3.1 Pro Preview, Gemini 3.1 Flash Lite Preview |
| DeepSeek | DeepSeek V4 Pro |
| Qwen | Qwen3.7-Max, Qwen3.6-35B-A3B |
| Kimi / Moonshot | Kimi K2.6 |
| GLM / Zhipu | GLM-5.1 |
| MiniMax | MiniMax M2.7 |
| xAI | Grok 4.3 |
| NVIDIA | Nemotron-3 Super 120B-A12B |
| Tencent | Hunyuan 3 Preview |
| Xiaomi | MiMo V2.5 Pro |
| StepFun | Step 3.5 Flash |
| Hermes | Hermes-4-70B, Hermes-4-405B (chat, seenote below) |
| + everything else | 280+ additional models — the full agentic frontier |

Routing happens through OpenRouter under the hood, so model availability and failover behavior matches what you'd get with an OpenRouter key — just billed against your Nous subscription instead. Switch between Claude Sonnet 4.6 for code and Gemini 3 Pro for long context with/modelmid-session — no new credentials, no top-ups, no surprise zero-balance errors.

`/model`

### The Nous Tool Gateway​

The same subscription unlocks theTool Gateway, which routes Hermes Agent's tool calls through Nous-managed infrastructure. Five backends, one login:

[Tool Gateway](/docs/user-guide/features/tool-gateway)

| Tool | Partner | What it does |
| --- | --- | --- |
| Web search & extract | Firecrawl | Agent-grade search and full-page extraction. No Firecrawl API key, no rate limit babysitting. |
| Image generation | FAL | Nine models under one endpoint: FLUX 2 Klein 9B, FLUX 2 Pro, Z-Image Turbo, Nano Banana Pro (Gemini 3 Pro Image), GPT Image 1.5, GPT Image 2, Ideogram V3, Recraft V4 Pro, Qwen Image. |
| Text-to-speech | OpenAI TTS | High-quality TTS without a separate OpenAI key. Enablesvoice modeacross messaging platforms. |
| Cloud browser automation | Browser Use | Headless Chromium sessions forbrowser_navigate,browser_click,browser_type,browser_vision. No Browserbase account needed. |
| Cloud terminal sandbox | Modal | Serverless terminal sandboxes for code execution (optional add-on). |

[voice mode](/docs/user-guide/features/voice-mode)
`browser_navigate`
`browser_click`
`browser_type`
`browser_vision`

Without the gateway, hooking each of those up means a Firecrawl account, a FAL account, a Browser Use account, an OpenAI key, and a Modal account — five separate signups, five separate dashboards, five separate top-up flows. With the gateway, all of it routes through one subscription.

You can also enable just specific gateway tools (e.g. web search but not image generation) — seeMixing the gateway with your own backendsbelow.

### Nous Chat​

Your Portal account also coverschat.nousresearch.com— Nous Research's web chat interface with the same model catalog. Useful when you're away from your terminal, or for non-agent conversation work.

[chat.nousresearch.com](https://chat.nousresearch.com)

### No credentials in your dotfiles​

Because everything routes through one OAuth-authenticated Portal session, you don't accumulate a.envfile with a dozen long-lived API keys. The refresh token at~/.hermes/auth.jsonis the only credential on disk, and Hermes mints short-lived JWTs from it per request — seeToken handlingbelow.

`.env`
`~/.hermes/auth.json`

### Cross-platform parity​

Native Windowsmakes per-tool API key setup its rough edge — installing a Firecrawl account, a FAL account, a Browser Use account, an OpenAI key from Windows is the highest-friction part of getting a useful agent. A Portal subscription smooths that out: one OAuth covers the model and every gateway tool, so Windows users get the same experience as macOS/Linux without manually configuring four backends.

[Native Windows](/docs/user-guide/windows-native)

## A note on Hermes 4​

Nous Research's ownHermes 4family (Hermes-4-70B, Hermes-4-405B) is available through the Portal at heavily discounted rates. These arefrontier hybrid-reasoning chat models— strong at math, science, instruction following, schema adherence, roleplay, and long-form writing.

They arenot recommended for use inside Hermes Agent, however. Hermes 4 is tuned for chat and reasoning, not the rapid-fire tool-calling loop the agent relies on. Use them forNous Chat, for research workflows, or via thesubscription proxyfrom other tooling — but for agent work, pick a frontier agentic model from the catalog instead:

[Nous Chat](https://chat.nousresearch.com)
[subscription proxy](/docs/user-guide/features/subscription-proxy)

```
/model anthropic/claude-sonnet-4.6     # best general-purpose agentic model/model openai/gpt-5.5-pro              # strong reasoning + tool calling/model google/gemini-3-pro-preview     # huge context window/model deepseek/deepseek-v4-pro        # cost-effective coder
```

The Portal's ownmodel info pagecarries the same warning, so this isn't a Hermes-side opinion — it's the official guidance from Nous Research.

[model info page](https://portal.nousresearch.com/info)

## Setup​

### Fresh install — one command​

```
hermes setup --portal
```

This runs the full setup in one shot:

1. Opens your browser to portal.nousresearch.com for OAuth login
2. Stores the refresh token at~/.hermes/auth.json
3. Lets you pick a Nous model from the curated list (or skip to keep your current one)
4. Sets Nous as your inference provider in~/.hermes/config.yaml(when you pick a model)
5. Turns on the Tool Gateway (web, image, TTS, browser routing)
6. Returns you to your terminal ready tohermes chat

`~/.hermes/auth.json`
`~/.hermes/config.yaml`
`hermes chat`

If you don't have a subscription yet, sign up atportal.nousresearch.com/manage-subscriptionfirst.

[portal.nousresearch.com/manage-subscription](https://portal.nousresearch.com/manage-subscription)

### Existing install — add Portal alongside other providers​

If you already have Hermes configured with OpenRouter, Anthropic, or any other provider and you want to add the Portal alongside them:

```
hermes model# pick "Nous Portal" from the provider list# browser opens, sign in, done
```

Your existing providers stay configured. You can switch between them with/modelmid-session orhermes modelbetween sessions — the Portal becomes one of your available providers, not your only one.

`/model`
`hermes model`

### Headless / SSH / remote setup​

OAuth needs a browser, but the loopback callback runs on the machine where Hermes is running. For remote hosts, seeOAuth over SSH / Remote Hosts— the same patterns work for the Portal as for any other OAuth-based provider (ssh -Lport forwarding).

[OAuth over SSH / Remote Hosts](/docs/guides/oauth-over-ssh)
`ssh -L`

### Profile setup​

If you useHermes profiles, the Portal refresh token is automatically shared across all profiles via a shared token store. Sign in once on any profile, and the rest pick it up automatically — no need to repeat the OAuth flow per profile.

[Hermes profiles](/docs/user-guide/profiles)

## Using the Portal day-to-day​

### Inspecting what's wired up​

```
hermes portal            # log in to Nous Portal + set it up (one-shot onboarding)hermes portal info       # login status, subscription info, model + gateway routinghermes portal status     # alias for `portal info`hermes portal tools      # detailed Tool Gateway catalog with per-tool routinghermes portal open       # open the subscription management page in your browser
```

hermes portal(with no subcommand) is the human-readable alias forhermes auth add nous --type oauth— it logs you in, lets you pick a Nous model, sets Nous as your inference provider, and offers the Tool Gateway opt-in (identical tohermes setup --portal, and the same Nous flow as the first-time quick setup).

`hermes portal`
`hermes auth add nous --type oauth`
`hermes setup --portal`

hermes portal infogives you the high-level overview:

`hermes portal info`

```
  Nous Portal  ───────────  Auth:    ✓ logged in  Portal:  https://portal.nousresearch.com  Model:   ✓ using Nous as inference provider  Tool Gateway  ────────────  Web search & extract  via Nous Portal  Image generation      via Nous Portal  Text-to-speech        via Nous Portal  Browser automation    via Nous Portal  Cloud terminal        not configured
```

### Switching models​

Inside a session:

```
/model anthropic/claude-sonnet-4.6/model openai/gpt-5.5-pro/model google/gemini-3-pro-preview
```

Or open the picker:

```
/model# arrow keys, enter to select
```

Outside a session (the full setup wizard, useful when adding a new provider):

```
hermes model
```

### Mixing the gateway with your own backends​

If you already have, say, a Browserbase account and want to keep using it while routing web search and image generation through Nous, that's supported. Usehermes toolsto pick backends per tool:

`hermes tools`

```
hermes tools# → Web search       → "Nous Subscription"# → Image generation → "Nous Subscription"# → Browser          → "Browserbase"  (your existing key)# → TTS              → "Nous Subscription"
```

The Tool Gateway is opt-in per tool, not all-or-nothing. The managed backends show up inhermes toolswhether or not you're logged into Nous Portal — if you pick "Nous Subscription" before authenticating, Hermes runs the Portal login inline (it won't change your inference provider or touch your other tools). See theTool Gateway docsfor the full per-tool configuration matrix.

`hermes tools`
[Tool Gateway docs](/docs/user-guide/features/tool-gateway)

### Subscription management​

Manage your plan, view usage, or upgrade/cancel at any time:

- Web:portal.nousresearch.com/manage-subscription
- CLI shortcut:hermes portal open(opens the same page in your default browser)

[portal.nousresearch.com/manage-subscription](https://portal.nousresearch.com/manage-subscription)
`hermes portal open`

## Configuration reference​

Afterhermes setup --portal,~/.hermes/config.yamlwill look like:

`hermes setup --portal`
`~/.hermes/config.yaml`

```
model:  provider: nous  default: anthropic/claude-sonnet-4.6     # or whatever model you picked  base_url: https://inference-api.nousresearch.com/v1
```

The Tool Gateway settings live under their respective tool sections:

```
web:  backend: nous       # web search/extract routes through Tool Gatewayimage_gen:  provider: noustts:  provider: nousbrowser:  backend: nous
```

The OAuth refresh token is stored separately at~/.hermes/auth.json(not inconfig.yaml— credentials and configuration are kept separate by design).

`~/.hermes/auth.json`
`config.yaml`

## Token handling​

Hermes mints a short-lived JWT from your stored Portal refresh token on each inference call rather than reusing a long-lived API key. The token lifecycle is fully automatic — refresh, mint, retry on transient 401 — and you never see it.

If the Portal invalidates the refresh token (password change, manual revoke, session expiry), the invalid refresh token isquarantined locallyso Hermes stops replaying it and you don't see a stream of identical 401s. The next call surfaces a clear "re-authentication required" message. Runhermes auth add nousto log in again; the quarantine clears on the next successful login.

`hermes auth add nous`

## Troubleshooting​

### hermes portal infoshows "not logged in"​

`hermes portal info`

You haven't completed the OAuth flow, or your refresh token was wiped. Run:

```
hermes portal
```

or usehermes modeland re-select Nous Portal.

`hermes model`

### Got a "re-authentication required" message mid-session​

Your Portal refresh token was invalidated (password change, manual revoke, or session expiry). Runhermes auth add nousand your next request will use the new credentials. Any quarantine on the old token clears automatically on successful re-login.

`hermes auth add nous`

### Want to use a specific provider model that the Portal doesn't expose​

The Portal proxies through OpenRouter, so any model that OpenRouter supports is generally available. If a specific model isn't appearing in/model, try the OpenRouter-style slug directly:

`/model`

```
/model anthropic/claude-opus-4.6
```

If a model is genuinely missing,open an issue— we surface the Portal's catalog to Hermes and gaps usually mean a routing config we can update.

[open an issue](https://github.com/NousResearch/hermes-agent/issues)

### Bills not appearing on my Portal account​

Checkhermes portal infofirst — if it shows you're using a different provider (Model: currently openrouterinstead ofusing Nous as inference provider), your local config has drifted. Runhermes model, pick Nous Portal, and the next request will route through your subscription.

`hermes portal info`
`Model: currently openrouter`
`using Nous as inference provider`
`hermes model`

## See also​

- Tool Gateway— Full details on every gateway tool, per-tool config, and pricing
- Subscription proxy— Use your Portal subscription from non-Hermes tools (other agents, scripts, third-party clients)
- Voice mode— Voice conversations using the Portal's OpenAI TTS
- AI Providers— Full provider catalog if you want to compare alternatives
- OAuth over SSH— Login from remote hosts or browser-only environments
- Profiles— Multiple Hermes configurations sharing one Portal login

[Tool Gateway](/docs/user-guide/features/tool-gateway)
[Subscription proxy](/docs/user-guide/features/subscription-proxy)
[Voice mode](/docs/user-guide/features/voice-mode)
[AI Providers](/docs/integrations/providers)
[OAuth over SSH](/docs/guides/oauth-over-ssh)
[Profiles](/docs/user-guide/profiles)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/integrations/nous-portal.md)