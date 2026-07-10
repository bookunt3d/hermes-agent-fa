- 
- Guides & Tutorials
- Run Hermes Agent with Nous Portal

# Run Hermes Agent with Nous Portal

This guide walks you through running Hermes Agent on aNous Portalsubscription end to end — from signing up to verifying that every tool routes correctly. If you just want the overview of what the Portal is and what's in the subscription, see theNous Portal integration page. This page is the task script.

## Prerequisites​

- Hermes Agent installed (Quickstart)
- A web browser on the machine you're setting up (or SSH port forwarding — seeOAuth over SSH)
- About 5 minutes

You donotneed: an OpenAI key, an Anthropic key, a Firecrawl account, a FAL account, a Browser Use account, or any other per-vendor credential. That's the whole point.

## 1. Get a subscription​

Openportal.nousresearch.com/manage-subscription, sign up, and pick a plan.

Already subscribed? Skip to step 2.

## 2. Run the one-shot setup​

```
hermes setup --portal
```

This single command does five things:

1. Opens your browser to portal.nousresearch.com for OAuth login
2. Stores the refresh token at~/.hermes/auth.json
3. Setsmodel.provider: nousin~/.hermes/config.yaml
4. Picks a default agentic model (anthropic/claude-sonnet-4.6or similar)
5. Turns on the Tool Gateway for web search, image generation, TTS, and browser automation

`~/.hermes/auth.json`
`model.provider: nous`
`~/.hermes/config.yaml`
`anthropic/claude-sonnet-4.6`

When it finishes, you're back at your terminal ready to chat.

### What if I'm SSH'd into a server?​

OAuth needs a browser, but the loopback callback runs on the machine where Hermes is running. Two options:

```
# Option A: SSH port forwarding (preferred)ssh -N -L 8642:127.0.0.1:8642 user@remote-host    # in a local terminalhermes setup --portal                              # on the remote, open the printed URL in your local browser# Option B: device-code login (works from Cloud Shell, Codespaces, EC2 Instance Connect)hermes auth add nous --type oauth# Then re-run `hermes setup --portal` to wire the provider + gateway
```

SeeOAuth over SSH / Remote Hostsfor the full walkthrough including ProxyJump chains, mosh/tmux, and ControlMaster gotchas.

## 3. Verify it worked​

```
hermes portal info
```

You should see:

```
  Nous Portal  ───────────  Auth:    ✓ logged in  Portal:  https://portal.nousresearch.com  Model:   ✓ using Nous as inference provider  Tool Gateway  ────────────  Web search & extract  via Nous Portal  Image generation      via Nous Portal  Text-to-speech        via Nous Portal  Browser automation    via Nous Portal
```

If any line shows something other than "via Nous Portal" or the auth line says "not logged in", jump toTroubleshootingbelow.

## 4. Run your first conversation​

```
hermes chat
```

Try something that exercises both the model and the Tool Gateway:

```
Hey, search the web for "Hermes Agent release notes" and summarize the top 3 hits.
```

You should see Hermes callweb_search(Firecrawl-backed, through the gateway) and respond with a summary. If the search runs and the response makes sense, you're done — the Portal is wired up end to end.

`web_search`

## 5. Pick the model you actually want​

hermes setup --portallets you pick a model during setup, but the whole point of the subscription is access to the full catalog — switch any time with/modelmid-session:

`hermes setup --portal`
`/model`

```
/model anthropic/claude-sonnet-4.6     # best general-purpose agentic/model openai/gpt-5.4                  # strong reasoning + tool calling/model google/gemini-2.5-pro           # huge context window/model deepseek/deepseek-v3.2          # cost-effective coder/model anthropic/claude-opus-4.6       # heavyweight for hard problems
```

Or pop the picker to browse:

```
/model
```

Pick a different default permanently:

```
# in your terminal, outside any sessionhermes config set model.default anthropic/claude-sonnet-4.6
```

### Don't pick Hermes-4 for agent work​

Hermes-4-70B and Hermes-4-405B are available on the Portal at deep discounts, but they'rechat/reasoning models, not tool-call-tuned. They will struggle with multi-step agent loops. Use them viaNous Chatfor conversation/research work, or through thesubscription proxyfrom non-agent tools. For Hermes Agent itself, stick to the frontier agentic models above.

The Portal's owninfo pagecarries this warning too — it's the official Nous guidance, not just a Hermes-side opinion.

## 6. (Optional) Customize Tool Gateway routing​

The gateway is opt-in per tool, not all-or-nothing. If you already have a Browserbase account and want to keep using it while routing web search and image generation through Nous, that's supported:

```
hermes tools# → Web search       → "Nous Subscription"     (recommended)# → Image generation → "Nous Subscription"     (recommended)# → Browser          → "Browserbase"           (your existing key)# → TTS              → "Nous Subscription"     (recommended)
```

These rows appear inhermes toolseven before you've logged into Nous Portal — if you pick "Nous Subscription" without an active session, Hermes runs the Portal login inline (without changing your inference provider or your other tools).

`hermes tools`

Verify your mix with:

```
hermes portal tools
```

You'll see per-tool routing —via Nous Portalfor the ones routed through the subscription, and the partner name (browserbase,firecrawl, etc.) for the ones using your own keys.

`via Nous Portal`
`browserbase`
`firecrawl`

## 7. (Optional) Enable voice mode​

Because the Tool Gateway includes OpenAI TTS,voice modeworks without a separate OpenAI key:

```
hermes setup voice# → pick "Nous Subscription" for TTS# → pick a speech-to-text backend (local faster-whisper is free, no setup)
```

Then in any messaging-platform session (Telegram, Discord, Signal, etc.), send a voice message and Hermes will transcribe it, respond, and reply with synthesized voice — all on your Portal subscription.

## 8. (Optional) Cron + always-on workflows​

The Portal subscription works forcron jobsandbatch processingthe same way it works for interactive chat — the OAuth refresh token is reused automatically. No additional setup; just schedule cron jobs and they'll bill against your subscription.

```
hermes cron create "every day at 9am" \  "Search the web for top AI news and summarize the 5 most important stories" \  --name "Daily AI news"
```

The cron job runs unattended, calls the model + web search + summarization all through your Portal subscription.

## Profiles and multi-user setups​

If you useHermes profiles(e.g. a separate config per project), the Portal refresh token is automatically shared across all profiles via a shared token store. Sign in once on any profile, and the rest pick it up automatically.

For team setups where multiple humans share a machine, each human has their own Portal account → each home directory holds its own~/.hermes/auth.json→ no token sharing across users. This is the right boundary.

`~/.hermes/auth.json`

## Troubleshooting​

### hermes portal infoshows "not logged in" afterhermes setup --portal​

`hermes portal info`
`hermes setup --portal`

The OAuth flow didn't complete. Re-run it:

```
hermes portal
```

If your browser doesn't open or the callback fails, you're likely on a remote/headless host — seeOAuth over SSHfor the port-forwarding workarounds.

### "Model: currently openrouter" (or some other provider) instead of "using Nous as inference provider"​

Your local config drifted. The OAuth worked butmodel.provideris still pointing at a different provider. Fix:

`model.provider`

```
hermes config set model.provider nous
```

Or interactively:

```
hermes model# pick Nous Portal
```

Re-verify withhermes portal info.

`hermes portal info`

### Tool Gateway tools showing partner names instead of "via Nous Portal"​

Per-tool config is overriding the gateway. Run:

```
hermes tools# pick "Nous Subscription" for any tool you want gateway-routed
```

Some users intentionally mix — e.g. routing web through Nous but using their own Browserbase key for browser. If that's intentional, leave it alone. If not, this command fixes it.

### "Re-authentication required" mid-session​

Your Portal refresh token was invalidated (password change, manual revoke, session expiry). The token is now quarantined locally so Hermes doesn't replay it endlessly. Just log in again:

```
hermes auth add nous
```

The quarantine clears automatically on successful re-login.

### Model I want isn't in the/modelpicker​

`/model`

The Portal catalog mirrors OpenRouter's model list (300+). If a model is missing, try typing the OpenRouter-style slug directly:

```
/model anthropic/claude-opus-4.6/model openai/o1-2025-12-17
```

If a model is genuinely unavailable,open an issue— most gaps are routing config we can update.

### Billing not appearing on my Portal account​

hermes portal infowill tell you whether you're actually routing through the Portal or some other provider. Common causes:

`hermes portal info`
- model.providerset toopenrouter/anthropic/etc. instead ofnous
- An OAuth refresh failure that fell back to a different configured provider
- Multiple Hermes profiles where you're using the wrong one (checkhermes profile list)

`model.provider`
`openrouter`
`anthropic`
`nous`
`hermes profile list`

### Want to revoke and start clean​

```
hermes auth logout nous       # wipes the local refresh token# Then re-run setup or remove the subscription from the Portal web UI
```

## What this gets you, in plain numbers​

| Without Portal | With Portal |
| --- | --- |
| 1× OpenRouter / Anthropic / OpenAI key in.env | 1× OAuth refresh token, no.envkeys |
| 1× Firecrawl key for web | Web routed through gateway |
| 1× FAL key for image gen | Image gen routed through gateway |
| 1× Browser Use / Browserbase key for browser | Browser routed through gateway |
| 1× OpenAI key for TTS / voice mode | TTS routed through gateway |
| 5 separate dashboards, top-ups, invoices | 1 subscription, 1 invoice |
| Cross-machine: replicate all 5 keys | Cross-machine: re-OAuth once |

`.env`
`.env`

That's the deal. If you're using more than two of those backends anyway, the subscription pays for itself.

## See also​

- Nous Portal integration page— Overview of what's in the subscription
- Tool Gateway— Full details on every gateway-routed tool
- Subscription proxy— Use your Portal subscription from non-Hermes tools
- Voice mode— Set up voice conversations on the Portal subscription
- OAuth over SSH— Remote / headless login patterns
- Profiles— Share one Portal login across multiple Hermes configurations