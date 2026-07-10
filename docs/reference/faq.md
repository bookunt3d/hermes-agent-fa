---
layout: docs
title: "سؤالات متداول"
permalink: /reference/faq/
---

- 
- Reference
- FAQ & Troubleshooting

# FAQ & Troubleshooting

Quick answers and fixes for the most common questions and issues.

## Frequently Asked Questions​

### What LLM providers work with Hermes?​

Hermes Agent works with any OpenAI-compatible API. Supported providers include:

- OpenRouter— access hundreds of models through one API key (recommended for flexibility)
- Nous Portal— Nous Research's subscription gateway — 300+ models plus web/image/TTS/browser through one OAuth login (recommended for newcomers)
- OpenAI— GPT-5.4, GPT-5-codex, GPT-4.1, GPT-4o, etc.
- Anthropic— Claude models (direct API, OAuth viahermes auth add anthropic, OpenRouter, or any compatible proxy)
- Google— Gemini models (direct API viageminiprovider, OpenRouter, or compatible proxy)
- z.ai / ZhipuAI— GLM models
- Kimi / Moonshot AI— Kimi models
- MiniMax— global and China endpoints
- Local models— viaOllama,vLLM,llama.cpp,SGLang, or any OpenAI-compatible server

[OpenRouter](https://openrouter.ai/)
[Nous Portal](/docs/integrations/nous-portal)
`hermes auth add anthropic`
`gemini`
[Ollama](https://ollama.com/)
[vLLM](https://docs.vllm.ai/)
[llama.cpp](https://github.com/ggerganov/llama.cpp)
[SGLang](https://github.com/sgl-project/sglang)

Set your provider withhermes modelor by editing~/.hermes/.env. See theEnvironment Variablesreference for all provider keys.

`hermes model`
`~/.hermes/.env`
[Environment Variables](/docs/reference/environment-variables)

### Does it work on Windows/Android/Termux/my plataform??​

SeePlatform Supportfor the full platform availability matrix.

[Platform Support](/docs/getting-started/platform-support)

### I run Hermes in WSL2. What's the best way to control my normal Windows Chrome?​

Prefer an MCP bridge over/browser connect.

`/browser connect`

Recommended pattern:

- run Hermes inside WSL2
- keep using your normal signed-in Chrome on Windows
- addchrome-devtools-mcpas an MCP server throughcmd.exeorpowershell.exe
- let Hermes use the resulting MCP browser tools

`chrome-devtools-mcp`
`cmd.exe`
`powershell.exe`

This is more reliable than trying to force Hermes core browser transport to attach directly across the WSL2/Windows boundary.

See:

- Use MCP with Hermes
- Browser Automation

[Use MCP with Hermes](/docs/guides/use-mcp-with-hermes#wsl2-bridge-hermes-in-wsl-to-windows-chrome)
[Browser Automation](/docs/user-guide/features/browser#wsl2--windows-chrome-prefer-mcp-over-browser-connect)

### Is my data sent anywhere?​

API calls goonly to the LLM provider you configure(e.g., OpenRouter, your local Ollama instance). Hermes Agent does not collect telemetry, usage data, or analytics. Your conversations, memory, and skills are stored locally in~/.hermes/.

`~/.hermes/`

### Can I use it offline / with local models?​

Yes. Runhermes model, selectCustom endpoint, and enter your server's URL:

`hermes model`

```
hermes model# Select: Custom endpoint (enter URL manually)# API base URL: http://localhost:11434/v1# API key: ollama# Model name: qwen3.5:27b# Context length: 64000   ← Hermes minimum; set this to match your server's actual context window
```

Or configure it directly inconfig.yaml:

`config.yaml`

```
model:  default: qwen3.5:27b  provider: custom  base_url: http://localhost:11434/v1
```

Hermes persists the endpoint, provider, and base URL inconfig.yamlso it survives restarts. If your local server has exactly one model loaded,/model customauto-detects it. You can also setprovider: customin config.yaml — it's a first-class provider, not an alias for anything else.

`config.yaml`
`/model custom`
`provider: custom`

This works with Ollama, vLLM, llama.cpp server, SGLang, LocalAI, and others. See theConfiguration guidefor details.

[Configuration guide](/docs/user-guide/configuration)

If you set a customnum_ctxin Ollama (e.g.,ollama run --num_ctx 64000), make sure to set the matching context length in Hermes — Ollama's/api/showreports the model'smaximumcontext, not the effectivenum_ctxyou configured.

`num_ctx`
`ollama run --num_ctx 64000`
`/api/show`
`num_ctx`

Hermes auto-detects local endpoints and relaxes streaming timeouts (read timeout raised from 120s to 1800s, stale stream detection disabled). If you still hit timeouts on very large contexts, setHERMES_STREAM_READ_TIMEOUT=1800in your.env. See theLocal LLM guidefor details.

`HERMES_STREAM_READ_TIMEOUT=1800`
`.env`
[Local LLM guide](/docs/guides/local-llm-on-mac#timeouts)

### How much does it cost?​

Hermes Agent itself isfree and open-source(MIT license). You pay only for the LLM API usage from your chosen provider. Local models are completely free to run.

### Can multiple people use one instance?​

Yes. Themessaging gatewaylets multiple users interact with the same Hermes Agent instance via Telegram, Discord, Slack, WhatsApp, or Home Assistant. Access is controlled through allowlists (specific user IDs) and DM pairing (first user to message claims access).

[messaging gateway](/docs/user-guide/messaging/)

### What's the difference between memory and skills?​

- Memorystoresfacts— things the agent knows about you, your projects, and preferences. Memories are retrieved automatically based on relevance.
- Skillsstoreprocedures— step-by-step instructions for how to do things. Skills are recalled when the agent encounters a similar task.

Both persist across sessions. SeeMemoryandSkillsfor details.

[Memory](/docs/user-guide/features/memory)
[Skills](/docs/user-guide/features/skills)

### Can I use it in my own Python project?​

Yes. Import theAIAgentclass and use Hermes programmatically:

`AIAgent`

```
from run_agent import AIAgentagent = AIAgent(model="anthropic/claude-opus-4.7")response = agent.chat("Explain quantum computing briefly")
```

See thePython Library guidefor full API usage.

[Python Library guide](/docs/user-guide/features/code-execution)

## Troubleshooting​

### Installation Issues​

#### hermes: command not foundafter installation​

`hermes: command not found`

Cause:Your shell hasn't reloaded the updated PATH.

Solution:

```
# Reload your shell profilesource ~/.bashrc    # bashsource ~/.zshrc     # zsh# Or start a new terminal session
```

If it still doesn't work, verify the install location:

```
which hermesls ~/.local/bin/hermes
```

The installer adds~/.local/binto your PATH. If you use a non-standard shell config, addexport PATH="$HOME/.local/bin:$PATH"manually.

`~/.local/bin`
`export PATH="$HOME/.local/bin:$PATH"`

#### Python version too old​

Cause:Hermes requires Python 3.11 or newer.

Solution:

```
python3 --version   # Check current version# Install a newer Pythonsudo apt install python3.12   # Ubuntu/Debianbrew install python@3.12      # macOS
```

The installer handles this automatically — if you see this error during manual installation, upgrade Python first.

#### Terminal commands saynode: command not found(ornvm,pyenv,asdf, …)​

`node: command not found`
`nvm`
`pyenv`
`asdf`

Cause:Hermes builds a per-session environment snapshot by runningbash -lonce at startup. A bash login shell reads/etc/profile,~/.bash_profile, and~/.profile, butdoes not source~/.bashrc— so tools that install themselves there (nvm,asdf,pyenv,cargo, customPATHexports) stay invisible to the snapshot. This most commonly happens when Hermes runs under systemd or in a minimal shell where nothing has pre-loaded the interactive shell profile.

`bash -l`
`/etc/profile`
`~/.bash_profile`
`~/.profile`
`~/.bashrc`
`nvm`
`asdf`
`pyenv`
`cargo`
`PATH`

Solution:Hermes auto-sources~/.bashrcby default. If that's not enough — e.g. you're a zsh user whose PATH lives in~/.zshrc, or you initnvmfrom a standalone file — list the extra files to source in~/.hermes/config.yaml:

`~/.bashrc`
`~/.zshrc`
`nvm`
`~/.hermes/config.yaml`

```
terminal:  shell_init_files:    - ~/.zshrc                     # zsh users: pulls zsh-managed PATH into the bash snapshot    - ~/.nvm/nvm.sh                # direct nvm init (works regardless of shell)    - /etc/profile.d/cargo.sh      # system-wide rc files  # When this list is set, the default ~/.bashrc auto-source is NOT added —  # include it explicitly if you want both:  #   - ~/.bashrc  #   - ~/.zshrc
```

Missing files are skipped silently. Sourcing happens in bash, so files that rely on zsh-only syntax may error — if that's a concern, source just the PATH-setting portion (e.g. nvm'snvm.shdirectly) rather than the whole rc file.

`nvm.sh`

To disable the auto-source behaviour (strict login-shell semantics only):

```
terminal:  auto_source_bashrc: false
```

#### uv: command not found​

`uv: command not found`

Cause:Theuvpackage manager isn't installed or not in PATH.

`uv`

Solution:

```
curl -LsSf https://astral.sh/uv/install.sh | shsource ~/.bashrc
```

#### Permission denied errors during install​

Cause:Insufficient permissions to write to the install directory.

Solution:

```
# Don't use sudo with the installer — it installs to ~/.local/bin# If you previously installed with sudo, clean up:sudo rm /usr/local/bin/hermes# Then re-run the standard installercurl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

### Provider & Model Issues​

#### /modelonly shows one provider / can't switch providers​

`/model`

Cause:/model(inside a chat session) can only switch between providers you'vealready configured. If you've only set up OpenRouter, that's all/modelwill show.

`/model`
`/model`

Solution:Exit your session and usehermes modelfrom your terminal to add new providers:

`hermes model`

```
# Exit the Hermes chat session first (Ctrl+C or /quit)# Run the full provider setup wizardhermes model# This lets you: add providers, run OAuth, enter API keys, configure endpoints
```

After adding a new provider viahermes model, start a new chat session —/modelwill now show all your configured providers.

`hermes model`
`/model`

| Want to... | Use |
| --- | --- |
| Add a new provider | hermes model(from terminal) |
| Enter/change API keys | hermes model(from terminal) |
| Switch model mid-session | /model <name>(inside session) |
| Switch to different configured provider | /model provider:model(inside session) |

`hermes model`
`hermes model`
`/model <name>`
`/model provider:model`

#### API key not working​

Cause:Key is missing, expired, incorrectly set, or for the wrong provider.

Solution:

```
# Check your configurationhermes config show# Re-configure your providerhermes model# Or set directlyhermes config set OPENROUTER_API_KEY sk-or-v1-xxxxxxxxxxxx
```

Make sure the key matches the provider. An OpenAI key won't work with OpenRouter and vice versa. Check~/.hermes/.envfor conflicting entries.

`~/.hermes/.env`

#### Model not available / model not found​

Cause:The model identifier is incorrect or not available on your provider.

Solution:

```
# List available models for your providerhermes model# Set a valid modelhermes config set HERMES_MODEL anthropic/claude-opus-4.7# Or specify per-sessionhermes chat --model openrouter/meta-llama/llama-3.1-70b-instruct
```

#### Rate limiting (429 errors)​

Cause:You've exceeded your provider's rate limits.

Solution:Wait a moment and retry. For sustained usage, consider:

- Upgrading your provider plan
- Switching to a different model or provider
- Usinghermes chat --provider <alternative>to route to a different backend

`hermes chat --provider <alternative>`

#### Context length exceeded​

Cause:The conversation has grown too long for the model's context window, or Hermes detected the wrong context length for your model.

Solution:

```
# Compress the current session/compress# Or start a fresh sessionhermes chat# Use a model with a larger context windowhermes chat --model openrouter/google/gemini-3-flash-preview
```

If this happens on the first long conversation, Hermes may have the wrong context length for your model. Check what it detected:

Look at the CLI startup line — it shows the detected context length (e.g.,📊 Context limit: 128000 tokens). You can also check with/usageduring a session.

`📊 Context limit: 128000 tokens`
`/usage`

To fix context detection, set it explicitly:

```
# In ~/.hermes/config.yamlmodel:  default: your-model-name  context_length: 131072  # your model's actual context window
```

Or for custom endpoints, add it per-model:

```
custom_providers:  - name: "My Server"    base_url: "http://localhost:11434/v1"    models:      qwen3.5:27b:        context_length: 64000
```

SeeContext Length Detectionfor how auto-detection works and all override options.

[Context Length Detection](/docs/integrations/providers#context-length-detection)

### Terminal Issues​

#### Command blocked as dangerous​

Cause:Hermes detected a potentially destructive command (e.g.,rm -rf,DROP TABLE). This is a safety feature.

`rm -rf`
`DROP TABLE`

Solution:When prompted, review the command and typeyto approve it. You can also:

`y`
- Ask the agent to use a safer alternative
- See the full list of dangerous patterns in theSecurity docs

[Security docs](/docs/user-guide/security)

This is working as intended — Hermes never silently runs destructive commands. The approval prompt shows you exactly what will execute.

#### sudonot working via messaging gateway​

`sudo`

Cause:The messaging gateway runs without an interactive terminal, sosudocannot prompt for a password.

`sudo`

Solution:

- Avoidsudoin messaging — ask the agent to find alternatives
- If you must usesudo, configure passwordless sudo for specific commands in/etc/sudoers
- Or switch to the terminal interface for administrative tasks:hermes chat

`sudo`
`sudo`
`/etc/sudoers`
`hermes chat`

#### Docker backend not connecting​

Cause:Docker daemon isn't running or the user lacks permissions.

Solution:

```
# Check Docker is runningdocker info# Add your user to the docker groupsudo usermod -aG docker $USERnewgrp docker# Verifydocker run hello-world
```

### Messaging Issues​

#### Bot not responding to messages​

Cause:The bot isn't running, isn't authorized, or your user isn't in the allowlist.

Solution:

```
# Check if the gateway is runninghermes gateway status# Start the gatewayhermes gateway start# Check logs for errorscat ~/.hermes/logs/gateway.log | tail -50
```

#### Messages not delivering​

Cause:Network issues, bot token expired, or platform webhook misconfiguration.

Solution:

- Verify your bot token is valid withhermes gateway setup
- Check gateway logs:cat ~/.hermes/logs/gateway.log | tail -50
- For webhook-based platforms (Slack, WhatsApp), ensure your server is publicly accessible

`hermes gateway setup`
`cat ~/.hermes/logs/gateway.log | tail -50`

#### Allowlist confusion — who can talk to the bot?​

Cause:Authorization mode determines who gets access.

Solution:

| Mode | How it works |
| --- | --- |
| Allowlist | Only user IDs listed in config can interact |
| DM pairing | First user to message in DM claims exclusive access |
| Open | Anyone can interact (not recommended for production) |

Configure in~/.hermes/config.yamlunder your gateway's settings. See theMessaging docs.

`~/.hermes/config.yaml`
[Messaging docs](/docs/user-guide/messaging/)

#### Gateway won't start​

Cause:Missing dependencies, port conflicts, or misconfigured tokens.

Solution:

```
# Install core messaging gateway dependenciescd ~/.hermes/hermes-agent && uv pip install -e ".[messaging]"  # Telegram, Discord, Slack, and shared gateway deps# Check for port conflictslsof -i :8080# Verify configurationhermes config show
```

#### WSL: Gateway keeps disconnecting orhermes gateway startfails​

`hermes gateway start`

Cause:WSL's systemd support is unreliable. Many WSL2 installations don't have systemd enabled, and even when enabled, services may not survive WSL restarts or Windows idle shutdowns.

Solution:Use foreground mode instead of the systemd service:

```
# Option 1: Direct foreground (simplest)hermes gateway run# Option 2: Persistent via tmux (survives terminal close)tmux new -s hermes 'hermes gateway run'# Reattach later: tmux attach -t hermes# Option 3: Background via nohupnohup hermes gateway run > ~/.hermes/logs/gateway.log 2>&1 &
```

If you want to try systemd anyway, make sure it's enabled:

1. Open/etc/wsl.conf(create it if it doesn't exist)
2. Add:[boot]systemd=true
3. From PowerShell:wsl --shutdown
4. Reopen your WSL terminal
5. Verify:systemctl is-system-runningshould say "running" or "degraded"

`/etc/wsl.conf`

```
[boot]systemd=true
```

`wsl --shutdown`
`systemctl is-system-running`

For reliable auto-start, use Windows Task Scheduler to launch WSL + the gateway on login:

1. Create a task that runswsl -d Ubuntu -- bash -lc 'hermes gateway run'
2. Set it to trigger on user logon

`wsl -d Ubuntu -- bash -lc 'hermes gateway run'`

#### macOS: Node.js / ffmpeg / other tools not found by gateway​

Cause:launchd services inherit a minimal PATH (/usr/bin:/bin:/usr/sbin:/sbin) that doesn't include Homebrew, nvm, cargo, or other user-installed tool directories. This commonly breaks the WhatsApp bridge (node not found) or voice transcription (ffmpeg not found).

`/usr/bin:/bin:/usr/sbin:/sbin`
`node not found`
`ffmpeg not found`

Solution:The gateway captures your shell PATH when you runhermes gateway install. If you installed tools after setting up the gateway, re-run the install to capture the updated PATH:

`hermes gateway install`

```
hermes gateway install    # Re-snapshots your current PATHhermes gateway start      # Detects the updated plist and reloads
```

You can verify the plist has the correct PATH:

```
/usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:PATH" \  ~/Library/LaunchAgents/ai.hermes.gateway.plist
```

### Performance Issues​

#### Slow responses​

Cause:Large model, distant API server, or heavy system prompt with many tools.

Solution:

- Try a faster/smaller model:hermes chat --model openrouter/meta-llama/llama-3.1-8b-instruct
- Reduce active toolsets:hermes chat -t "terminal"
- Check your network latency to the provider
- For local models, ensure you have enough GPU VRAM

`hermes chat --model openrouter/meta-llama/llama-3.1-8b-instruct`
`hermes chat -t "terminal"`

#### High token usage​

Cause:Long conversations, verbose system prompts, or many tool calls accumulating context.

Solution:

```
# Compress the conversation to reduce tokens/compress# Check session token usage/usage
```

Use/compressregularly during long sessions. It summarizes the conversation history and reduces token usage significantly while preserving context.

`/compress`

#### Session getting too long​

Cause:Extended conversations accumulate messages and tool outputs, approaching context limits.

Solution:

```
# Compress current session (preserves key context)/compress# Start a new session with a reference to the old onehermes chat# Resume a specific session later if neededhermes chat --continue
```

### MCP Issues​

#### MCP server not connecting​

Cause:Server binary not found, wrong command path, or missing runtime.

Solution:

```
# Ensure MCP dependencies are installed (already included in standard install)cd ~/.hermes/hermes-agent && uv pip install -e ".[mcp]"# For npm-based servers, ensure Node.js is availablenode --versionnpx --version# Test the server manuallynpx -y @modelcontextprotocol/server-filesystem /tmp
```

Verify your~/.hermes/config.yamlMCP configuration:

`~/.hermes/config.yaml`

```
mcp_servers:  filesystem:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/docs"]
```

#### Tools not showing up from MCP server​

Cause:Server started but tool discovery failed, tools were filtered out by config, or the server does not support the MCP capability you expected.

Solution:

- Check gateway/agent logs for MCP connection errors
- Ensure the server responds to thetools/listRPC method
- Review anytools.include,tools.exclude,tools.resources,tools.prompts, orenabledsettings under that server
- Remember that resource/prompt utility tools are only registered when the session actually supports those capabilities
- Use/reload-mcpafter changing config

`tools/list`
`tools.include`
`tools.exclude`
`tools.resources`
`tools.prompts`
`enabled`
`/reload-mcp`

```
# Verify MCP servers are configuredhermes config show | grep -A 12 mcp_servers# Restart Hermes or reload MCP after config changeshermes chat
```

See also:

- MCP (Model Context Protocol)
- Use MCP with Hermes
- MCP Config Reference

[MCP (Model Context Protocol)](/docs/user-guide/features/mcp)
[Use MCP with Hermes](/docs/guides/use-mcp-with-hermes)
[MCP Config Reference](/docs/reference/mcp-config-reference)

#### MCP timeout errors​

Cause:The MCP server is taking too long to respond, or it crashed during execution.

Solution:

- Increase the timeout in your MCP server config if supported
- Check if the MCP server process is still running
- For remote HTTP MCP servers, check network connectivity

If an MCP server crashes mid-request, Hermes will report a timeout. Check the server's own logs (not just Hermes logs) to diagnose the root cause.

## Profiles​

### How do profiles differ from just setting HERMES_HOME?​

Profiles are a managed layer on top ofHERMES_HOME. Youcouldmanually setHERMES_HOME=/some/pathbefore every command, but profiles handle all the plumbing for you: creating the directory structure, generating shell aliases (hermes-work), tracking the active profile in~/.hermes/active_profile, and syncing skill updates across all profiles automatically. They also integrate with tab completion so you don't have to remember paths.

`HERMES_HOME`
`HERMES_HOME=/some/path`
`hermes-work`
`~/.hermes/active_profile`

### Can two profiles share the same bot token?​

No. Each messaging platform (Telegram, Discord, etc.) requires exclusive access to a bot token. If two profiles try to use the same token simultaneously, the second gateway will fail to connect. Create a separate bot per profile — for Telegram, talk to@BotFatherto make additional bots.

[@BotFather](https://t.me/BotFather)

### Do profiles share memory or sessions?​

No. Each profile has its own memory store, session database, and skills directory. They are completely isolated. If you want to start a new profile with existing memories and sessions, usehermes profile create newname --clone-allto copy everything from the current profile, or add--clone-from <profile>to copy from a specific source profile.

`hermes profile create newname --clone-all`
`--clone-from <profile>`

### What happens when I runhermes update?​

`hermes update`

hermes updatepulls the latest code and reinstalls dependenciesonce(not per-profile). It then syncs updated skills to all profiles automatically. You only need to runhermes updateonce — it covers every profile on the machine.

`hermes update`
`hermes update`

### How many profiles can I run?​

There is no hard limit. Each profile is just a directory under~/.hermes/profiles/. The practical limit depends on your disk space and how many concurrent gateways your system can handle (each gateway is a lightweight Python process). Running dozens of profiles is fine; each idle profile uses no resources.

`~/.hermes/profiles/`

## Workflows & Patterns​

### Using different models for different tasks (multi-model workflows)​

Scenario:You use GPT-5.4 as your daily driver, but Gemini or Grok writes better social media content. Manually switching models every time is tedious.

Solution: Delegation config.Hermes can route subagents to a different model automatically. Set this in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
delegation:  model: "google/gemini-3-flash-preview"   # subagents use this model  provider: "openrouter"                    # provider for subagents
```

Now when you tell Hermes "write me a Twitter thread about X" and it spawns adelegate_tasksubagent, that subagent runs on Gemini instead of your main model. Your primary conversation stays on GPT-5.4.

`delegate_task`

You can also be explicit in your prompt:"Delegate a task to write social media posts about our product launch. Use your subagent for the actual writing."The agent will usedelegate_task, which automatically picks up the delegation config.

`delegate_task`

For one-off model switches without delegation, use/modelin the CLI:

`/model`

```
/model google/gemini-3-flash-preview    # switch for this session# ... write your content .../model openai/gpt-5.4                   # switch back
```

Each/modelswitch resets the prompt cache — the cache key includes the model, so the first message after every switch re-reads the whole conversation at full input price. On long sessions, prefer delegation (subagents get their own fresh context) or a new session over repeated back-and-forth switching.

`/model`

SeeSubagent Delegationfor more on how delegation works.

[Subagent Delegation](/docs/user-guide/features/delegation)

### Running multiple agents on one WhatsApp number (per-chat binding)​

Scenario:In OpenClaw, you had multiple independent agents bound to specific WhatsApp chats — one for a family shopping list group, another for your private chat. Can Hermes do this?

Current limitation:Hermes profiles each require their own WhatsApp number/session. You cannot bind multiple profiles to different chats on the same WhatsApp number — the WhatsApp bridge (Baileys) uses one authenticated session per number.

Workarounds:

1. Use a single profile with personality switching.Create differentAGENTS.mdcontext files or use the/personalitycommand to change behavior per chat. The agent sees which chat it's in and can adapt.
2. Use cron jobs for specialized tasks.For a shopping list tracker, set up a cron job that monitors a specific chat and manages the list — no separate agent needed.
3. Use separate numbers.If you need truly independent agents, pair each profile with its own WhatsApp number. Virtual numbers from services like Google Voice work for this.
4. Use Telegram or Discord instead.These platforms support per-chat binding more naturally — each Telegram group or Discord channel gets its own session, and you can run multiple bot tokens (one per profile) on the same account.

Use a single profile with personality switching.Create differentAGENTS.mdcontext files or use the/personalitycommand to change behavior per chat. The agent sees which chat it's in and can adapt.

`AGENTS.md`
`/personality`

Use cron jobs for specialized tasks.For a shopping list tracker, set up a cron job that monitors a specific chat and manages the list — no separate agent needed.

Use separate numbers.If you need truly independent agents, pair each profile with its own WhatsApp number. Virtual numbers from services like Google Voice work for this.

Use Telegram or Discord instead.These platforms support per-chat binding more naturally — each Telegram group or Discord channel gets its own session, and you can run multiple bot tokens (one per profile) on the same account.

SeeProfilesandWhatsApp setupfor more details.

[Profiles](/docs/user-guide/profiles)
[WhatsApp setup](/docs/user-guide/messaging/whatsapp)

### Controlling what shows up in Telegram (hiding logs and reasoning)​

Scenario:You see gateway exec logs, Hermes reasoning, and tool call details in Telegram instead of just the final output.

Solution:Thedisplay.tool_progresssetting inconfig.yamlcontrols how much tool activity is shown:

`display.tool_progress`
`config.yaml`

```
display:  tool_progress: "off"   # options: off, new, all, verbose
```

- off— Only the final response. No tool calls, no reasoning, no logs.
- new— Shows new tool calls as they happen (brief one-liners).
- all— Shows all tool activity including results.
- verbose— Full detail including tool arguments and outputs.

`off`
`new`
`all`
`verbose`

For messaging platforms,offornewis usually what you want. After editingconfig.yaml, restart the gateway for changes to take effect.

`off`
`new`
`config.yaml`

You can also toggle this per-session with the/verbosecommand (if enabled):

`/verbose`

```
display:  tool_progress_command: true   # enables /verbose in the gateway
```

### Managing skills on Telegram (slash command limit)​

Scenario:Telegram has a 100 slash command limit, and your skills are pushing past it. You want to disable skills you don't need on Telegram, buthermes skills configsettings don't seem to take effect.

`hermes skills config`

Solution:Usehermes skills configto disable skills per-platform. This writes toconfig.yaml:

`hermes skills config`
`config.yaml`

```
skills:  disabled: []                    # globally disabled skills  platform_disabled:    telegram: [skill-a, skill-b]  # disabled only on telegram
```

After changing this,restart the gateway(hermes gateway restartor kill and relaunch). The Telegram bot command menu rebuilds on startup.

`hermes gateway restart`

Skills with very long descriptions are truncated to 40 characters in the Telegram menu to stay within payload size limits. If skills aren't appearing, it may be a total payload size issue rather than the 100 command count limit — disabling unused skills helps with both.

### Shared thread sessions (multiple users, one conversation)​

Scenario:You have a Telegram or Discord thread where multiple people mention the bot. You want all mentions in that thread to be part of one shared conversation, not separate per-user sessions.

Current behavior:Hermes creates sessions keyed by user ID on most platforms, so each person gets their own conversation context. This is by design for privacy and context isolation.

Workarounds:

1. Use Slack.Slack sessions are keyed by thread, not by user. Multiple users in the same thread share one conversation — exactly the behavior you're describing. This is the most natural fit.
2. Use a group chat with a single user.If one person is the designated "operator" who relays questions, the session stays unified. Others can read along.
3. Use a Discord channel.Discord sessions are keyed by channel, so all users in the same channel share context. Use a dedicated channel for the shared conversation.

Use Slack.Slack sessions are keyed by thread, not by user. Multiple users in the same thread share one conversation — exactly the behavior you're describing. This is the most natural fit.

Use a group chat with a single user.If one person is the designated "operator" who relays questions, the session stays unified. Others can read along.

Use a Discord channel.Discord sessions are keyed by channel, so all users in the same channel share context. Use a dedicated channel for the shared conversation.

### Exporting Hermes to another machine​

Scenario:You've built up skills, cron jobs, and memories on one machine and want to move everything to a new dedicated Linux box.

Solution:

1. Install Hermes Agent on the new machine:curl-fsSLhttps://hermes-agent.nousresearch.com/install.sh|bash
2. On thesource machine, create a full backup:hermes backupThis creates a zip of your entire~/.hermes/directory — config, API keys, memories, skills, sessions, and profiles — saved to your home directory as~/hermes-backup-<timestamp>.zip.
3. Copy the zip to the new machine and import it:# On the source machinescp~/hermes-backup-<timestamp>.zip newmachine:~/# On the new machinehermesimport~/hermes-backup-<timestamp>.zip
4. On the new machine, runhermes setupto verify API keys and provider config are working.

Install Hermes Agent on the new machine:

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

On thesource machine, create a full backup:

```
hermes backup
```

This creates a zip of your entire~/.hermes/directory — config, API keys, memories, skills, sessions, and profiles — saved to your home directory as~/hermes-backup-<timestamp>.zip.

`~/.hermes/`
`~/hermes-backup-<timestamp>.zip`

Copy the zip to the new machine and import it:

```
# On the source machinescp ~/hermes-backup-<timestamp>.zip newmachine:~/# On the new machinehermes import ~/hermes-backup-<timestamp>.zip
```

On the new machine, runhermes setupto verify API keys and provider config are working.

`hermes setup`

### Moving a single profile to another machine​

Scenario:You want to move or share one specific profile — not your full installation.

```
# On the source machinehermes profile export work ./work-backup.tar.gz# Copy the file to the target machine, then:hermes profile import ./work-backup.tar.gz work
```

The imported profile will have all config, memories, sessions, and skills from the export. You may need to update paths or re-authenticate with providers if the new machine has a different setup.

### hermes backupvshermes profile export​

`hermes backup`
`hermes profile export`

| Feature | hermes backup | hermes profile export |
| --- | --- | --- |
| Use Case | Full machine migration | Porting/sharing a specific profile |
| Scope | Global (entire~/.hermesdirectory) | Local (single profile directory) |
| Includes | All profiles, global config, API keys, sessions | Single profile: SOUL.md, memories, sessions, skills |
| Credentials | Included(.envandauth.json) | Excluded(stripped for safe sharing) |
| Format | .zip | .tar.gz |

`hermes backup`
`hermes profile export`
`~/.hermes`
`.env`
`auth.json`
`.zip`
`.tar.gz`

Manual fallback (rsync):If you prefer to copy files directly, exclude the code repo:

```
rsync -av --exclude='hermes-agent' ~/.hermes/ newmachine:~/.hermes/
```

hermes backupproduces a consistent snapshot even while Hermes is actively running. The restored archive excludes machine-local runtime files likegateway.pidandcron.pid.

`hermes backup`
`gateway.pid`
`cron.pid`

### Permission denied when reloading shell after install​

Scenario:After running the Hermes installer,source ~/.zshrcgives a permission denied error.

`source ~/.zshrc`

Cause:This usually happens when~/.zshrc(or~/.bashrc) has incorrect file permissions, or when the installer couldn't write to it cleanly. It's not a Hermes-specific issue — it's a shell config permissions problem.

`~/.zshrc`
`~/.bashrc`

Solution:

```
# Check permissionsls -la ~/.zshrc# Fix if needed (should be -rw-r--r-- or 644)chmod 644 ~/.zshrc# Then reloadsource ~/.zshrc# Or just open a new terminal window — it picks up PATH changes automatically
```

If the installer added the PATH line but permissions are wrong, you can add it manually:

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

### Error 400 on first agent run​

Scenario:Setup completes fine, but the first chat attempt fails with HTTP 400.

Cause:Usually a model name mismatch — the configured model doesn't exist on your provider, or the API key doesn't have access to it.

Solution:

```
# Check what model and provider are configuredhermes config show | head -20# Re-run model selectionhermes model# Or test with a known-good modelhermes chat -q "hello" --model anthropic/claude-opus-4.7
```

If using OpenRouter, make sure your API key has credits. A 400 from OpenRouter often means the model requires a paid plan or the model ID has a typo.

## Still Stuck?​

If your issue isn't covered here:

1. Search existing issues:GitHub Issues
2. Ask the community:Nous Research Discord
3. File a bug report:Include your OS, Python version (python3 --version), Hermes version (hermes --version), and the full error message

[GitHub Issues](https://github.com/NousResearch/hermes-agent/issues)
[Nous Research Discord](https://discord.gg/nousresearch)
`python3 --version`
`hermes --version`
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/reference/faq.md)