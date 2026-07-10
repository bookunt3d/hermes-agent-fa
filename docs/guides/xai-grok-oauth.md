---
layout: docs
title: "OAuth xAI Grok"
permalink: /docs/guides/xai-grok-oauth/
---

- 
- Guides & Tutorials
- xAI Grok OAuth (SuperGrok / X Premium+)

# xAI Grok OAuth (SuperGrok / X Premium+)

Hermes Agent supports xAI Grok through a browser-based OAuth device-code login flow againstaccounts.x.ai, using either aSuperGrok subscription(grok.com) or anX Premium+ subscription(linked X account). NoXAI_API_KEYis required — log in once and Hermes automatically refreshes your session in the background.

`XAI_API_KEY`

When you sign in with an X account that has Premium+, xAI automatically links the subscription status to your xAI session, so the OAuth flow works the same as it does for direct SuperGrok subscribers.

The transport reuses thecodex_responsesadapter (xAI exposes a Responses-style endpoint), so reasoning, tool-calling, streaming, and prompt caching work without any adapter changes.

`codex_responses`

The same OAuth bearer token is also reused by every direct-to-xAI surface in Hermes — TTS, image generation, video generation, and transcription — so a single login covers all four.

## Overview​

| Item | Value |
| --- | --- |
| Provider ID | xai-oauth |
| Display name | xAI Grok OAuth (SuperGrok / X Premium+) |
| Auth type | Browser OAuth 2.0 device code |
| Transport | xAI Responses API (codex_responses) |
| Default model | grok-build-0.1 |
| Endpoint | https://api.x.ai/v1 |
| Auth server | https://accounts.x.ai |
| Requires env var | No (XAI_API_KEYisnotused for this provider) |
| Subscription | SuperGrokorX Premium+— see note below |

`xai-oauth`
`codex_responses`
`grok-build-0.1`
`https://api.x.ai/v1`
`https://accounts.x.ai`
`XAI_API_KEY`

## Prerequisites​

- Python 3.9+
- Hermes Agent installed
- An activeSuperGroksubscription on your xAI account,oranX Premium+subscription on the X account you sign in with (xAI links the subscription automatically)
- A browser available anywhere you can open the printed verification URL

xAI's backend enforces its own allowlist on the OAuth API surface and has been seen to reject standard SuperGrok subscribers withHTTP 403(see issue#26847) even though the in-app subscription is active. If OAuth login succeeds in the browser but inference returns 403, setXAI_API_KEYand switch to the API-key path (provider: xai) — that surface is not subject to the same gating today.

`HTTP 403`
`XAI_API_KEY`
`provider: xai`

## Quick Start​

```
# Launch the provider and model pickerhermes model# → Select "xAI Grok OAuth (SuperGrok / X Premium+)" from the provider list# → Hermes opens or prints an accounts.x.ai verification URL# → Enter the displayed code if prompted, then approve access in the browser# → Pick a model (grok-build-0.1 is at the top)# → Start chattinghermes
```

After the first login, credentials are stored under~/.hermes/auth.jsonand refreshed automatically before they expire.

`~/.hermes/auth.json`

## Logging In Manually​

You can trigger a login without going through the model picker:

```
hermes auth add xai-oauth
```

### Remote / headless sessions​

On servers, containers, browser-only consoles (Cloud Shell, Codespaces, EC2 Instance Connect), or SSH sessions where Hermes cannot open a browser locally, Hermes prints the xAI verification URL and user code. Open the URL in any browser on your laptop or in the cloud console, enter the code if prompted, and Hermes will keep polling until xAI approves the login. No SSH tunnel or local callback listener is required.

```
hermes auth add xai-oauth --no-browser# Open the printed verification URL in your browser.
```

The same device-code flow applies when you sign in from the web dashboard or the desktop app: Hermes shows the verification URL and user code, then polls in the background until you approve access.

## How the Login Works​

1. Hermes requests a device code fromauth.x.ai.
2. You open the verification URL, sign in, enter the displayed code if prompted, and approve access.
3. Hermes polls xAI until approval, then saves tokens to~/.hermes/auth.json.
4. From then on, Hermes refreshes the access token in the background — you stay signed in until youhermes auth logout xai-oauthor revoke access from your xAI account settings.

`auth.x.ai`
`~/.hermes/auth.json`
`hermes auth logout xai-oauth`

## Checking Login Status​

```
hermes doctor
```

The◆ Auth Providerssection will show the current state of every provider, includingxai-oauth.

`◆ Auth Providers`
`xai-oauth`

## Switching Models​

```
hermes model# → Select "xAI Grok OAuth (SuperGrok / X Premium+)"# → Pick from the model list (grok-build-0.1 is pinned to the top)
```

Or set the model directly:

```
hermes config set model.default grok-build-0.1hermes config set model.provider xai-oauth
```

## Configuration Reference​

After login,~/.hermes/config.yamlwill contain:

`~/.hermes/config.yaml`

```
model:  default: grok-build-0.1  provider: xai-oauth  base_url: https://api.x.ai/v1
```

### Provider aliases​

All of the following resolve toxai-oauth:

`xai-oauth`

```
hermes --provider xai-oauth        # canonicalhermes --provider grok-oauth       # aliashermes --provider x-ai-oauth       # aliashermes --provider xai-grok-oauth   # alias
```

## Direct-to-xAI Tools (TTS / Image / Video / Transcription / X Search)​

Once you're logged in via OAuth, every direct-to-xAI tool reuses the same bearer token automatically — there isno separate setupunless you'd rather use an API key.

To pick a backend for each tool:

```
hermes tools# → Text-to-Speech       → "xAI TTS"# → Image Generation     → "xAI Grok Imagine (image)"# → Video Generation     → "xAI Grok Imagine"# → X (Twitter) Search   → "xAI Grok OAuth (SuperGrok / X Premium+)"
```

If OAuth tokens are already stored, the picker confirms it and skips the credential prompt. If neither OAuth norXAI_API_KEYis set, the picker offers a 3-choice menu: OAuth login, paste API key, or skip.

`XAI_API_KEY`

Thevideo_gentoolset is disabled by default. Enable it inhermes tools→🎬 Video Generation(press space) before the agent can callvideo_generate. Otherwise the agent may fall back to the bundled ComfyUI skill, which is also tagged for video generation.

`video_gen`
`hermes tools`
`🎬 Video Generation`
`video_generate`

Thex_searchtoolset auto-enables whenever xAI credentials (a SuperGrok / X Premium+ OAuth token orXAI_API_KEY) are configured. Disable explicitly viahermes tools→🐦 X (Twitter) Search(press space) if you don't want this. The tool routes through xAI's built-inx_searchResponses API — it works witheitheryour SuperGrok / X Premium+ OAuth login or a paidXAI_API_KEY, and prefers OAuth when both are configured (uses your subscription quota instead of API spend). The tool schema is hidden from the model when no xAI credentials are configured, regardless of whether the toolset is enabled.

`x_search`
`XAI_API_KEY`
`hermes tools`
`🐦 X (Twitter) Search`
`x_search`
`XAI_API_KEY`

### Models​

| Tool | Model | Notes |
| --- | --- | --- |
| Chat | grok-build-0.1 | Default; auto-selected when you log in via OAuth |
| Chat | grok-4.3 | Previous default |
| Chat | grok-4.20-0309-reasoning | Reasoning variant |
| Chat | grok-4.20-0309-non-reasoning | Non-reasoning variant |
| Chat | grok-4.20-multi-agent-0309 | Multi-agent variant |
| Image | grok-imagine-image | Default; ~5–10 s |
| Image | grok-imagine-image-quality | Higher fidelity; ~10–20 s |
| Video | grok-imagine-video | Text-to-video |
| Video | grok-imagine-video-1.5-preview | Image-to-video; dated aliasgrok-imagine-video-1.5-2026-05-30 |
| TTS | (default voice) | xAI/v1/ttsendpoint |

`grok-build-0.1`
`grok-4.3`
`grok-4.20-0309-reasoning`
`grok-4.20-0309-non-reasoning`
`grok-4.20-multi-agent-0309`
`grok-imagine-image`
`grok-imagine-image-quality`
`grok-imagine-video`
`grok-imagine-video-1.5-preview`
`grok-imagine-video-1.5-2026-05-30`
`/v1/tts`

The chat catalog is derived live from the on-diskmodels.devcache; new xAI releases appear automatically once that cache refreshes.grok-build-0.1is always pinned to the top of the list.

`models.dev`
`grok-build-0.1`

## Environment Variables​

| Variable | Effect |
| --- | --- |
| XAI_BASE_URL | Override the defaulthttps://api.x.ai/v1endpoint (rarely needed). |

`XAI_BASE_URL`
`https://api.x.ai/v1`

To select xAI as the active provider, setmodel.provider: xai-oauthinconfig.yaml(usehermes setupfor the guided flow) or pass--provider xai-oauthfor a single invocation.

`model.provider: xai-oauth`
`config.yaml`
`hermes setup`
`--provider xai-oauth`

## Troubleshooting​

### Token expired — not re-logging in automatically​

Hermes refreshes the token before each session and again reactively on a 401. If refresh fails withinvalid_grant(the refresh token was revoked, or the account was rotated), Hermes surfaces a typed re-auth message instead of crashing.

`invalid_grant`

When the refresh failure is terminal (HTTP 4xx,invalid_grant, revoked grant, etc.), Hermes marks the refresh token as dead and quarantines it locally — subsequent calls skip the doomed refresh attempt instead of replaying the same 401 over and over. The agent surfaces a single "re-authentication required" message and stays out of the way until you log in again.

`invalid_grant`

Fix:runhermes auth add xai-oauthagain to start a fresh login. The quarantine clears on the next successful exchange.

`hermes auth add xai-oauth`

### Authorization timed out​

Device-code approval has a finite expiry window (xAI setsexpires_inon the device-code response, typically on the order of tens of minutes). If you do not approve the login in time, Hermes raises a timeout error.

`expires_in`

Fix:re-runhermes auth add xai-oauth(orhermes model). The flow starts fresh.

`hermes auth add xai-oauth`
`hermes model`

### Logging in from a remote server​

On SSH or container sessions Hermes prints the verification URL and user code instead of opening a browser. Open that URL in a browser on your laptop or in a cloud console — no SSH port forward is needed for xAI Grok OAuth.

```
hermes auth add xai-oauth --no-browser
```

For loopback-redirect providers (Spotify, MCP servers), seeOAuth over SSH / Remote Hosts.

### HTTP 403 after a successful login (tier / entitlement)​

OAuth completed in the browser, tokens are saved, but inference or token refresh returnsHTTP 403with a message similar to"The caller does not have permission to execute the specified operation".

`HTTP 403`

This isnota stale-token problem — re-runninghermes modelwon't change it. xAI's backend has been seen to restrict OAuth API access to specific SuperGrok tiers despite the in-app subscription being active (issue#26847).

`hermes model`

Fix:setXAI_API_KEYand switch to the API-key path:

`XAI_API_KEY`

```
export XAI_API_KEY=xai-...hermes config set model.provider xai
```

Or upgrade your subscription atx.ai/grokif the OAuth route is required.

### "No xAI credentials found" error at runtime​

The auth store has noxai-oauthentry and noXAI_API_KEYis set. You haven't logged in yet, or the credential file was deleted.

`xai-oauth`
`XAI_API_KEY`

Fix:runhermes modeland pick the xAI Grok OAuth provider, or runhermes auth add xai-oauth.

`hermes model`
`hermes auth add xai-oauth`

## Logging Out​

To remove all stored xAI Grok OAuth credentials:

```
hermes auth logout xai-oauth
```

This clears both the singleton OAuth entry inauth.jsonand any credential-pool rows forxai-oauth. Usehermes auth remove xai-oauth <index|id|label>if you only want to drop a single pool entry (runhermes auth list xai-oauthto see them).

`auth.json`
`xai-oauth`
`hermes auth remove xai-oauth <index|id|label>`
`hermes auth list xai-oauth`

## See Also​

- OAuth over SSH / Remote Hosts— SSH tunnels for loopback-redirect providers (Spotify, MCP); xAI uses device code and does not need a tunnel
- AI Providers reference
- Environment Variables
- Configuration
- Voice & TTS