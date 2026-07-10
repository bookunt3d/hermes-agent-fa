- 
- Features
- Tool Gateway

# Nous Tool Gateway

One subscription. Every tool built in.

The Tool Gateway is included with every paidNous Portalsubscription. It routes Hermes' tool calls — web search, image generation, text-to-speech, and cloud browser automation — through infrastructure Nous already runs, so you don't have to sign up with Firecrawl, FAL, OpenAI, Browser Use, or anyone else just to make your agent useful.

## What's included​

|  | Tool | What you get |
| --- | --- | --- |
| 🔍 | Web search & extract | Agent-grade web search and full-page extraction via Firecrawl. No rate limits to worry about — the gateway handles scaling. |
| 🎨 | Image generation | Nine models under one endpoint:FLUX 2 Klein 9B,FLUX 2 Pro,Z-Image Turbo,Nano Banana Pro(Gemini 3 Pro Image),GPT Image 1.5,GPT Image 2,Ideogram V3,Recraft V4 Pro,Qwen Image. Pick per-generation with a flag, or let Hermes default to FLUX 2 Klein. |
| 🔊 | Text-to-speech | OpenAI TTS voices wired into thetext_to_speechtool. Drop voice notes into Telegram, generate audio for pipelines, narrate anything. |
| 🌐 | Cloud browser automation | Headless Chromium sessions via Browser Use.browser_navigate,browser_click,browser_type,browser_vision— all the agent-driving primitives, no Browserbase account required. |

`text_to_speech`
`browser_navigate`
`browser_click`
`browser_type`
`browser_vision`

All four are pay-as-you-use billed against your Nous subscription. Use any combination — run the gateway for web and images while keeping your own ElevenLabs key for TTS, or route everything through Nous.

## Why it's here​

Building an agent that can actuallydo thingsmeans stitching together 5+ API subscriptions — each with their own signup, rate limits, billing, and quirks. The gateway collapses that into one account:

- One bill.Pay Nous; we handle the rest.
- One signup.No Firecrawl, FAL, Browser Use, or OpenAI audio accounts to manage.
- One key.Your Nous Portal OAuth covers every tool.
- Same quality.Same backends the direct-key route uses — just fronted by us.

Bring your own keys anytime — per-tool, whenever you want to. The gateway isn't a lock-in, it's a shortcut.

## Get started​

There are three ways in — pick whichever fits where you are:

```
hermes setup --portal     # Fresh install: Nous OAuth + set Nous as provider + turn on the Tool Gateway in one go
```

```
hermes model              # Switch your inference provider to Nous Portal — Hermes then offers to turn on the gateway for all tools
```

```
hermes tools              # Enable the gateway per-tool — pick "Nous Subscription" for any tool you want
```

hermes setup --portalandhermes modelare the all-at-once paths: log in once, optionally flip every tool to the gateway.hermes toolsis the à la carte path — turn on just the tools you want, one at a time.

`hermes setup --portal`
`hermes model`
`hermes tools`

You don't have to log in first.Withhermes tools, the Nous-managed backends (Web search, Image, Video, TTS, Browser) are always listed, even if you've never signed into Nous Portal. Select one and Hermes runs the Portal login right there if you aren't already authenticated — no need to runhermes modelbeforehand. If your Nous OAuth is already active, selecting the backend enables it immediately with no extra prompt. This path only logs you in and turns on the one tool you picked — it doesnotswitch your inference provider, and it doesnotprompt you to enable the gateway for every other tool.

`hermes tools`
`hermes model`

Check what's active at any time:

```
hermes portal info        # Portal auth + Tool Gateway routing summaryhermes portal tools       # Gateway catalog with current routing per toolhermes status             # Full system status (Tool Gateway is one section)
```

hermes portal infoshows a section like:

`hermes portal info`

```
◆ Nous Tool Gateway  Nous Portal     ✓ managed tools available  Web tools       ✓ active via Nous subscription  Image gen       ✓ active via Nous subscription  TTS             ✓ active via Nous subscription  Browser         ○ active via Browser Use key
```

Tools marked "active via Nous subscription" are going through the gateway. Anything else is using your own keys.

## Eligibility​

The Tool Gateway is apaid-subscriptionfeature. Free-tier Nous accounts can use Portal for inference but don't include managed tools —upgrade your planto unlock the gateway.

Some accounts are also entitled to afree tool pool— a small managed-tool allowance that covers gateway tool calls without a paid subscription. When a free pool is available, the gateway surfaces it and shows a setup prompt on first use, so you can opt in and start using managed tools right away.

## Mix and match​

The gateway is per-tool. Turn it on for just what you want:

- All tools through Nous— easiest; one subscription, done.
- Gateway for web + images, bring your own TTS— keep your ElevenLabs voice, let Nous handle the rest.
- Gateway only for things you don't have keys for— "I already pay for Browserbase, but I don't want a Firecrawl account" works fine.

Switch any tool at any time via:

```
hermes tools          # Interactive picker for each tool category
```

Select the tool, pickNous Subscriptionas the provider (or any direct provider you prefer). No config editing required. If you aren't logged into Nous Portal yet, pickingNous Subscriptionkicks off the Portal login inline — you don't need to authenticate throughhermes modelfirst.

`hermes model`

## Using individual image models​

Image generation defaults to FLUX 2 Klein 9B for speed. Override per-call by passing the model ID to theimage_generatetool:

`image_generate`
| Model | ID | Best for |
| --- | --- | --- |
| FLUX 2 Klein 9B | fal-ai/flux-2/klein/9b | Fast, good default |
| FLUX 2 Pro | fal-ai/flux-2-pro | Higher fidelity FLUX |
| Z-Image Turbo | fal-ai/z-image/turbo | Stylized, fast |
| Nano Banana Pro | fal-ai/nano-banana-pro | Google Gemini 3 Pro Image |
| GPT Image 1.5 | fal-ai/gpt-image-1.5 | OpenAI image gen, text+image |
| GPT Image 2 | fal-ai/gpt-image-2 | OpenAI latest |
| Ideogram V3 | fal-ai/ideogram/v3 | Strong prompt adherence + typography |
| Recraft V4 Pro | fal-ai/recraft/v4/pro/text-to-image | Vector-style, graphic design |
| Qwen Image | fal-ai/qwen-image | Alibaba multimodal |

`fal-ai/flux-2/klein/9b`
`fal-ai/flux-2-pro`
`fal-ai/z-image/turbo`
`fal-ai/nano-banana-pro`
`fal-ai/gpt-image-1.5`
`fal-ai/gpt-image-2`
`fal-ai/ideogram/v3`
`fal-ai/recraft/v4/pro/text-to-image`
`fal-ai/qwen-image`

The set evolves —hermes tools→ Image Generation shows the current live list.

`hermes tools`

## Configuration reference​

Most users never need to touch this —hermes modelandhermes toolscover every workflow interactively. This section is for writing config.yaml directly or scripting setups.

`hermes model`
`hermes tools`

### Per-tooluse_gatewayflag​

`use_gateway`

Each tool's config block takes ause_gatewayboolean:

`use_gateway`

```
web:  backend: firecrawl  use_gateway: trueimage_gen:  use_gateway: truetts:  provider: openai  use_gateway: truebrowser:  cloud_provider: browser-use  use_gateway: true
```

Precedence:use_gateway: trueroutes through Nous regardless of any direct keys in.env.use_gateway: false(or absent) uses direct keys if available and only falls back to the gateway when none exist.

`use_gateway: true`
`.env`
`use_gateway: false`

### Disabling the gateway​

```
web:  use_gateway: false   # Hermes now uses FIRECRAWL_API_KEY from .env
```

hermes toolsautomatically clears the flag when you pick a non-gateway provider, so this usually happens for you.

`hermes tools`

### Self-hosted gateway (advanced)​

Running your own Nous-compatible gateway? Override endpoints in~/.hermes/.env:

`~/.hermes/.env`

```
TOOL_GATEWAY_DOMAIN=your-domain.example.comTOOL_GATEWAY_SCHEME=httpsTOOL_GATEWAY_USER_TOKEN=your-token        # normally auto-populated from Portal loginFIRECRAWL_GATEWAY_URL=https://...         # override one endpoint specifically
```

These knobs exist for custom infrastructure setups (enterprise deployments, dev environments). Regular subscribers never set them.

## FAQ​

### Does it work with Telegram / Discord / the other messaging gateways?​

Yes. Tool Gateway operates at the tool-execution layer, not the CLI. Every interface that can call a tool — CLI, Telegram, Discord, Slack, IRC, Teams, the API server, anything — benefits from it transparently.

### What happens if my subscription expires?​

Tools routed through the gateway stop working until you renew or swap in direct API keys viahermes tools. Hermes shows a clear error pointing at the portal.

`hermes tools`

### Can I see usage or costs per tool?​

Yes — theNous Portal dashboardbreaks usage down by tool so you can see what's driving your bill.

### Is Modal (serverless terminal) included?​

Modal is available as anoptional add-onthrough the Nous subscription, not part of the default Tool Gateway bundle. Configure it viahermes setup terminalor directly inconfig.yamlwhen you want a remote sandbox for shell execution.

`hermes setup terminal`
`config.yaml`

### Do I need to delete my existing API keys when I enable the gateway?​

No — keep them in.env. Whenuse_gateway: true, Hermes skips direct keys and uses the gateway. Flip the flag back tofalseand your keys become the source again. The gateway isn't a lock-in.

`.env`
`use_gateway: true`
`false`