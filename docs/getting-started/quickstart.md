---
layout: docs
title: "راهنمای شروع سریع"
permalink: /getting-started/quickstart/
---

- 
- Getting Started
- Quickstart

# Quickstart

This guide gets you from zero to a working Hermes setup that survives real use. Install, choose a provider, verify a working chat, and know exactly what to do when something breaks.

## Prefer to watch?​

Onchain AI Garageput together a Masterclass walkthrough of installation, setup, and basic commands — a good companion to this page if you'd rather follow along on video. For more, see the fullHermes Agent Tutorials & Use Casesplaylist.

[Hermes Agent Tutorials & Use Cases](https://www.youtube.com/playlist?list=PLmpUb_PWAkDxewld5ZYyKifuHxgIbiq2d)

## Who this is for​

- Brand new and want the shortest path to a working setup
- Switching providers and don't want to lose time to config mistakes
- Setting up Hermes for a team, bot, or always-on workflow
- Tired of "it installed, but it still does nothing"

## The fastest path​

Pick the row that matches your goal:

| Goal | Do this first | Then do this |
| --- | --- | --- |
| I just want Hermes working on my machine | hermes setup | Run a real chat and verify it responds |
| I already know my provider | hermes model | Save the config, then start chatting |
| I want a bot or always-on setup | hermes gateway setupafter CLI works | Connect Telegram, Discord, Slack, or another platform |
| I want a local or self-hosted model | hermes model→ custom endpoint | Verify the endpoint, model name, and context length |
| I want multi-provider fallback | hermes modelfirst | Add routing and fallback only after the base chat works |

`hermes setup`
`hermes model`
`hermes gateway setup`
`hermes model`
`hermes model`

Rule of thumb:if Hermes cannot complete a normal chat, do not add more features yet. Get one clean conversation working first, then layer on gateway, cron, skills, voice, or routing.

## 1. Install Hermes Agent​

### With the Hermes Desktop installer on macOS or Windows (recommended)​

To easily install the command-line and desktop applications,download the Hermes Desktop installerfrom our website and run it.

[download the Hermes Desktop installer](https://hermes-agent.nousresearch.com/)

### Without Hermes Desktop:​

For a command-line only install without Hermes Desktop, run:

#### Linux / macOS / WSL2 / Android (Termux)​

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

#### Windows (native)​

Run in powershell:

```
iex (irm https://hermes-agent.nousresearch.com/install.ps1) 
```

If you're installing on a phone, see the dedicatedTermux guidefor the tested manual path, supported extras, and current Android-specific limitations.

[Termux guide](/docs/getting-started/termux)

After it finishes, reload your shell:

```
source ~/.bashrc   # or source ~/.zshrc
```

For detailed installation options, prerequisites, and troubleshooting, see theInstallation guide.

[Installation guide](/docs/getting-started/installation)

## 2. Choose a Provider​

The single most important setup step. Usehermes modelto walk through the choice interactively:

`hermes model`

```
hermes model
```

One subscription covers 300+ models plus theTool Gateway(web search, image generation, TTS, cloud browser). On a fresh install:

[Tool Gateway](/docs/user-guide/features/tool-gateway)

```
hermes setup --portal
```

That logs you in, sets Nous as your provider, and turns on the Tool Gateway in one command.

On a fresh install,hermes setupoffers three modes:

`hermes setup`
- Quick Setup (Nous Portal)— free OAuth login, no API keys; sets up a model plus the Tool Gateway tools. The recommended fast path.
- Full Setup— walk through every provider, tool, and option yourself (bring your own keys).
- Blank Slate— everything startsoffexcept the bare minimum needed to run an agent:provider & model, the File Operations toolset, and the Terminal toolset. No web, browser, code execution, vision, memory, delegation, cron, skills, plugins, or MCP servers — and compression, checkpoints, smart routing, and memory capture are all disabled. After the minimal baseline is applied, you choose one of two paths:start with everything disabled(finish now with the minimal agent), orwalk through all configurations(opt in to tools, skills, plugins, MCP, and messaging). Pick this when you want a minimal, fully-controlled agent and intend to enable only exactly what you need.

Blank Slate writes an explicitplatform_toolsets.clilist plusagent.disabled_toolsets, so nothing you didn't choose ever loads — not even afterhermes update. Re-enable anything later withhermes tools, seed skills withhermes skills opt-in --sync, or tune settings withhermes setup agent.

`platform_toolsets.cli`
`agent.disabled_toolsets`
`hermes update`
`hermes tools`
`hermes skills opt-in --sync`
`hermes setup agent`

Good defaults:

| Provider | What it is | How to set up |
| --- | --- | --- |
| Nous Portal | Subscription-based, zero-config | OAuth login viahermes model |
| OpenAI Codex | ChatGPT OAuth, uses Codex models | Device code auth viahermes model |
| Anthropic | Claude models directly — Max plan + extra usage credits (OAuth), or API key for pay-per-token | hermes model→ OAuth login (requires Max + extra credits), or an Anthropic API key |
| OpenRouter | Multi-provider routing across many models | Enter your API key |
| Z.AI | GLM / Zhipu-hosted models | SetGLM_API_KEY/ZAI_API_KEY(also acceptsZ_AI_API_KEY) |
| Kimi / Moonshot | Moonshot-hosted coding and chat models | SetKIMI_API_KEY(or the Kimi-Coding-specificKIMI_CODING_API_KEY) |
| Kimi / Moonshot China | China-region Moonshot endpoint | SetKIMI_CN_API_KEY |
| Arcee AI | Trinity models | SetARCEEAI_API_KEY |
| GMI Cloud | Multi-model direct API | SetGMI_API_KEY |
| MiniMax (OAuth) | MiniMax frontier model via browser OAuth — no API key needed (model name inhermes_cli/models.pymay change between releases) | hermes model→ MiniMax (OAuth) |
| MiniMax | International MiniMax endpoint | SetMINIMAX_API_KEY |
| MiniMax China | China-region MiniMax endpoint | SetMINIMAX_CN_API_KEY |
| Alibaba Cloud | Qwen models via DashScope | SetDASHSCOPE_API_KEY(Qwen Coding Plan also acceptsALIBABA_CODING_PLAN_API_KEY) |
| Hugging Face | 20+ open models via unified router (Qwen, DeepSeek, Kimi, etc.) | SetHF_TOKEN |
| AWS Bedrock | Claude, Nova, Llama, DeepSeek via native Converse API | IAM role oraws configure(guide) |
| Azure Foundry | Azure AI Foundry-hosted models | SetAZURE_FOUNDRY_API_KEY+AZURE_FOUNDRY_BASE_URL |
| Google AI Studio | Gemini models via direct API | SetGOOGLE_API_KEY/GEMINI_API_KEY |
| xAI | Grok models via direct API | SetXAI_API_KEY |
| xAI Grok OAuth | SuperGrok / Premium+ subscription, no API key needed | hermes model→ xAI Grok OAuth |
| NovitaAI | Multi-model API gateway | SetNOVITA_API_KEY |
| StepFun | Step Plan models | SetSTEPFUN_API_KEY |
| Xiaomi MiMo | Xiaomi-hosted models | SetXIAOMI_API_KEY |
| Tencent TokenHub | Tencent-hosted models | SetTOKENHUB_API_KEY |
| Ollama Cloud | Managed Ollama-hosted models | SetOLLAMA_API_KEY |
| LM Studio | Local desktop app exposing an OpenAI-compatible API | SetLM_API_KEY(andLM_BASE_URLif non-default) |
| Qwen OAuth | Qwen Portal browser OAuth — no API key needed | hermes model→ Qwen OAuth |
| Kilo Code | KiloCode-hosted models | SetKILOCODE_API_KEY |
| OpenCode Zen | Pay-as-you-go access to curated models | SetOPENCODE_ZEN_API_KEY |
| OpenCode Go | $10/month subscription for open models | SetOPENCODE_GO_API_KEY |
| DeepSeek | Direct DeepSeek API access | SetDEEPSEEK_API_KEY |
| NVIDIA NIM | Nemotron models via build.nvidia.com or local NIM | SetNVIDIA_API_KEY(optional:NVIDIA_BASE_URL) |
| GitHub Copilot | GitHub Copilot subscription (GPT-5.x, Claude, Gemini, etc.) | OAuth viahermes model, orCOPILOT_GITHUB_TOKEN/GH_TOKEN |
| GitHub Copilot ACP | Copilot ACP agent backend (spawns localcopilotCLI) | hermes model(requirescopilotCLI +copilot login) |
| Custom Endpoint | VLLM, SGLang, Ollama, or any OpenAI-compatible API | Set base URL + API key |

`hermes model`
`hermes model`
`hermes model`
`GLM_API_KEY`
`ZAI_API_KEY`
`Z_AI_API_KEY`
`KIMI_API_KEY`
`KIMI_CODING_API_KEY`
`KIMI_CN_API_KEY`
`ARCEEAI_API_KEY`
`GMI_API_KEY`
`hermes_cli/models.py`
`hermes model`
`MINIMAX_API_KEY`
`MINIMAX_CN_API_KEY`
`DASHSCOPE_API_KEY`
`ALIBABA_CODING_PLAN_API_KEY`
`HF_TOKEN`
`aws configure`
[guide](/docs/guides/aws-bedrock)
`AZURE_FOUNDRY_API_KEY`
`AZURE_FOUNDRY_BASE_URL`
`GOOGLE_API_KEY`
`GEMINI_API_KEY`
`XAI_API_KEY`
`hermes model`
`NOVITA_API_KEY`
`STEPFUN_API_KEY`
`XIAOMI_API_KEY`
`TOKENHUB_API_KEY`
`OLLAMA_API_KEY`
`LM_API_KEY`
`LM_BASE_URL`
`hermes model`
`KILOCODE_API_KEY`
`OPENCODE_ZEN_API_KEY`
`OPENCODE_GO_API_KEY`
`DEEPSEEK_API_KEY`
`NVIDIA_API_KEY`
`NVIDIA_BASE_URL`
`hermes model`
`COPILOT_GITHUB_TOKEN`
`GH_TOKEN`
`copilot`
`hermes model`
`copilot`
`copilot login`

For most first-time users: choose a provider, accept the defaults unless you know why you're changing them. The full provider catalog with env vars and setup steps lives on theProviderspage.

[Providers](/docs/integrations/providers)

Hermes Agent requires a model with at least64,000 tokensof context. Models with smaller windows cannot maintain enough working memory for multi-step tool-calling workflows and will be rejected at startup. Most hosted models (Claude, GPT, Gemini, Qwen, DeepSeek) meet this easily. If you're running a local model, set its context size to at least 64K (e.g.--ctx-size 65536for llama.cpp or-c 65536for Ollama).

`--ctx-size 65536`
`-c 65536`

You can switch providers at any time withhermes model— no lock-in. For a full list of all supported providers and setup details, seeAI Providers.

`hermes model`
[AI Providers](/docs/integrations/providers)

### How settings are stored​

Hermes separates secrets from normal config:

- Secrets and tokens→~/.hermes/.env
- Non-secret settings→~/.hermes/config.yaml

`~/.hermes/.env`
`~/.hermes/config.yaml`

The easiest way to set values correctly is through the CLI:

```
hermes config set model anthropic/claude-opus-4.6hermes config set terminal.backend dockerhermes config set OPENROUTER_API_KEY sk-or-...
```

The right value goes to the right file automatically.

## 3. Run Your First Chat​

```
hermes            # classic CLIhermes --tui      # modern TUI (recommended)
```

You'll see a welcome banner with your model, available tools, and skills. Use a prompt that's specific and easy to verify:

Hermes ships with two terminal interfaces: the classicprompt_toolkitCLI and a newerTUIwith modal overlays, mouse selection, and non-blocking input. Both share the same sessions, slash commands, and config — try each withhermesvshermes --tui.

`prompt_toolkit`
[TUI](/docs/user-guide/tui)
`hermes`
`hermes --tui`

```
Summarize this repo in 5 bullets and tell me what the main entrypoint is.
```

```
Check my current directory and tell me what looks like the main project file.
```

```
Help me set up a clean GitHub PR workflow for this codebase.
```

What success looks like:

- The banner shows your chosen model/provider
- Hermes replies without error
- It can use a tool if needed (terminal, file read, web search)
- The conversation continues normally for more than one turn

If that works, you're past the hardest part.

## 4. Verify Sessions Work​

Before moving on, make sure resume works:

```
hermes --continue    # Resume the most recent sessionhermes -c            # Short form
```

That should bring you back to the session you just had. If it doesn't, check whether you're in the same profile and whether the session actually saved. This matters later when you're juggling multiple setups or machines.

## 5. Try Key Features​

### Use the terminal​

```
❯ What's my disk usage? Show the top 5 largest directories.
```

The agent runs terminal commands on your behalf and shows results.

### Slash commands​

Type/to see an autocomplete dropdown of all commands:

`/`

| Command | What it does |
| --- | --- |
| /help | Show all available commands |
| /tools | List available tools |
| /model | Switch models interactively |
| /personality pirate | Try a fun personality |
| /save | Save the conversation |

`/help`
`/tools`
`/model`
`/personality pirate`
`/save`

### Multi-line input​

PressAlt+Enter,Ctrl+J, orShift+Enterto add a new line.Shift+Enterrequires a terminal that sends it as a distinct sequence (Kitty / foot / WezTerm / Ghostty by default; iTerm2 / Alacritty / VS Code terminal once the Kitty keyboard protocol is enabled).Alt+EnterandCtrl+Jwork in every terminal.

`Alt+Enter`
`Ctrl+J`
`Shift+Enter`
`Shift+Enter`
`Alt+Enter`
`Ctrl+J`

### Interrupt the agent​

If the agent is taking too long, type a new message and press Enter — it interrupts the current task and switches to your new instructions.Ctrl+Calso works.

`Ctrl+C`

## 6. Add the Next Layer​

Only after the base chat works. Pick what you need:

### Bot or shared assistant​

```
hermes gateway setup    # Interactive platform configuration
```

ConnectTelegram,Discord,Slack,WhatsApp,Signal,Email, orHome Assistant, orMicrosoft Teams.

[Telegram](/docs/user-guide/messaging/telegram)
[Discord](/docs/user-guide/messaging/discord)
[Slack](/docs/user-guide/messaging/slack)
[WhatsApp](/docs/user-guide/messaging/whatsapp)
[Signal](/docs/user-guide/messaging/signal)
[Email](/docs/user-guide/messaging/email)
[Home Assistant](/docs/user-guide/messaging/homeassistant)
[Microsoft Teams](/docs/user-guide/messaging/teams)

### Automation and tools​

- hermes tools— tune tool access per platform
- hermes skills— browse and install reusable workflows
- Cron — only after your bot or CLI setup is stable

`hermes tools`
`hermes skills`

### Sandboxed terminal​

For safety, run the agent in a Docker container or on a remote server:

```
hermes config set terminal.backend docker    # Docker isolationhermes config set terminal.backend ssh       # Remote server
```

### Voice mode​

```
# From the Hermes install directory (the curl installer placed it at# ~/.hermes/hermes-agent on Linux/macOS or %LOCALAPPDATA%\hermes\hermes-agent on Windows):cd ~/.hermes/hermes-agentuv pip install -e ".[voice]"# Includes faster-whisper for free local speech-to-text
```

Then in the CLI:/voice on. PressCtrl+Bto record. SeeVoice Mode.

`/voice on`
`Ctrl+B`
[Voice Mode](/docs/user-guide/features/voice-mode)

### Skills​

Skills are on-demand instruction documents that teach Hermes how to do a specific task — deploy to Kubernetes, open a GitHub PR, fine-tune a model, search for GIFs. Each is aSKILL.mdfile with a name, a description, and a step-by-step procedure. The agent reads the short descriptions for free and only loads a skill's full content when a task actually calls for it, so adding skills doesn't bloat every request.

`SKILL.md`

Hermes ships with a catalog of bundled skills already installed in~/.hermes/skills/. You can add more from the Skills Hub, or write your own.

`~/.hermes/skills/`

Browse and install from the hub:

```
hermes skills browse                      # list everything availablehermes skills search kubernetes           # find skills by keywordhermes skills install openai/skills/k8s   # install one (runs a security scan first)
```

The install argument is asource/pathslug from the hub —openai/skills/k8smeans thek8sskill from OpenAI's catalog.hermes skills browseshows the exact slugs to use.

`source/path`
`openai/skills/k8s`
`k8s`
`hermes skills browse`

Use a skill— every installed skill becomes a slash command automatically:

```
/k8s deploy the staging manifest          # run the skill with a request/k8s                                       # load it and let Hermes ask what you need
```

This works in the CLI and in any connected messaging platform. You don't have to install everything up front — the agent picks the right bundled skill on its own during normal conversation when a task matches one.

SeeSkills Systemfor writing your own, external skill directories, and the full hub source list.

[Skills System](/docs/user-guide/features/skills)

### MCP servers​

```
# Add to ~/.hermes/config.yamlmcp_servers:  github:    command: npx    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
```

### Editor integration (ACP)​

ACP support ships with the standard[all]extras, so the curl installer already includes it. Just run:

`[all]`

```
hermes acp
```

(If you installed without[all], runcd ~/.hermes/hermes-agent && uv pip install -e ".[acp]"first.)

`[all]`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[acp]"`

SeeACP Editor Integration.

[ACP Editor Integration](/docs/user-guide/features/acp)

## Common Failure Modes​

These are the problems that waste the most time:

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Hermes opens but gives empty or broken replies | Provider auth or model selection is wrong | Runhermes modelagain and confirm provider, model, and auth |
| Custom endpoint "works" but returns garbage | Wrong base URL, model name, or not actually OpenAI-compatible | Verify the endpoint in a separate client first |
| Gateway starts but nobody can message it | Bot token, allowlist, or platform setup is incomplete | Re-runhermes gateway setupand checkhermes gateway status |
| hermes --continuecan't find old session | Switched profiles or session never saved | Checkhermes sessions listand confirm you're in the right profile |
| Model unavailable or odd fallback behavior | Provider routing or fallback settings are too aggressive | Keep routing off until the base provider is stable |
| hermes doctorflags config problems | Config values are missing or stale | Fix the config, retest a plain chat before adding features |

`hermes model`
`hermes gateway setup`
`hermes gateway status`
`hermes --continue`
`hermes sessions list`
`hermes doctor`

## Recovery Toolkit​

When something feels off, use this order:

1. hermes doctor
2. hermes model
3. hermes setup
4. hermes sessions list
5. hermes --continue
6. hermes gateway status

`hermes doctor`
`hermes model`
`hermes setup`
`hermes sessions list`
`hermes --continue`
`hermes gateway status`

That sequence gets you from "broken vibes" back to a known state fast.

## Quick Reference​

| Command | Description |
| --- | --- |
| hermes | Start chatting |
| hermes model | Choose your LLM provider and model |
| hermes tools | Configure which tools are enabled per platform |
| hermes setup | Full setup wizard (configures everything at once) |
| hermes doctor | Diagnose issues |
| hermes update | Update to latest version |
| hermes gateway | Start the messaging gateway |
| hermes --continue | Resume last session |

`hermes`
`hermes model`
`hermes tools`
`hermes setup`
`hermes doctor`
`hermes update`
`hermes gateway`
`hermes --continue`

## Next Steps​

- CLI Guide— Master the terminal interface
- Configuration— Customize your setup
- Messaging Gateway— Connect Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant, Teams, and more
- Tools & Toolsets— Explore available capabilities
- AI Providers— Full provider list and setup details
- Skills System— Reusable workflows and knowledge
- Tips & Best Practices— Power user tips

[CLI Guide](/docs/user-guide/cli)
[Configuration](/docs/user-guide/configuration)
[Messaging Gateway](/docs/user-guide/messaging/)
[Tools & Toolsets](/docs/user-guide/features/tools)
[AI Providers](/docs/integrations/providers)
[Skills System](/docs/user-guide/features/skills)
[Tips & Best Practices](/docs/guides/tips)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/quickstart.md)