---
layout: docs
title: "نکات و ترفندها"
permalink: /guides/tips/
---

- 
- Guides & Tutorials
- Tips & Best Practices

# Tips & Best Practices

A quick-wins collection of practical tips that make you immediately more effective with Hermes Agent. Each section targets a different aspect — scan the headers and jump to what's relevant.

Runhermes setup --portal— you get 300+ models including Claude, GPT-5, and Gemini under one subscription. SeeNous Portal.

`hermes setup --portal`
[Nous Portal](/docs/integrations/nous-portal)

## Getting the Best Results​

### Be Specific About What You Want​

Vague prompts produce vague results. Instead of "fix the code," say "fix the TypeError inapi/handlers.pyon line 47 — theprocess_request()function receivesNonefromparse_body()." The more context you give, the fewer iterations you need.

`api/handlers.py`
`process_request()`
`None`
`parse_body()`

### Provide Context Up Front​

Front-load your request with the relevant details: file paths, error messages, expected behavior. One well-crafted message beats three rounds of clarification. Paste error tracebacks directly — the agent can parse them.

### Use Context Files for Recurring Instructions​

If you find yourself repeating the same instructions ("use tabs not spaces," "we use pytest," "the API is at/api/v2"), put them in anAGENTS.mdfile. The agent reads it automatically every session — zero effort after setup.

`/api/v2`
`AGENTS.md`

### Let the Agent Use Its Tools​

Don't try to hand-hold every step. Say "find and fix the failing test" rather than "opentests/test_foo.py, look at line 42, then..." The agent has file search, terminal access, and code execution — let it explore and iterate.

`tests/test_foo.py`

### Use Skills for Complex Workflows​

Before writing a long prompt explaining how to do something, check if there's already a skill for it. Type/skillsto browse available skills, or just invoke one directly like/axolotlor/github-pr-workflow.

`/skills`
`/axolotl`
`/github-pr-workflow`

## CLI Power User Tips​

### Multi-Line Input​

PressAlt+Enter,Ctrl+J, orShift+Enterto insert a newline without sending.Shift+Enteronly works when the terminal sends it as a distinct keystroke (Kitty / foot / WezTerm / Ghostty by default; iTerm2 / Alacritty / VS Code terminal once the Kitty keyboard protocol is enabled). The other two work in every terminal.

`Shift+Enter`

### Paste Detection​

The CLI auto-detects multi-line pastes. Just paste a code block or error traceback directly — it won't send each line as a separate message. The paste is buffered and sent as one message.

### Interrupt and Redirect​

PressCtrl+Conce to interrupt the agent mid-response. You can then type a new message to redirect it. Double-press Ctrl+C within 2 seconds to force exit. This is invaluable when the agent starts going down the wrong path.

### Resume Sessions with-c​

`-c`

Forgot something from your last session? Runhermes -cto resume exactly where you left off, with full conversation history restored. You can also resume by title:hermes -r "my research project".

`hermes -c`
`hermes -r "my research project"`

### Clipboard Image Paste​

PressCtrl+Vto paste an image from your clipboard directly into the chat. The agent uses vision to analyze screenshots, diagrams, error popups, or UI mockups — no need to save to a file first.

### Slash Command Autocomplete​

Type/and pressTabto see all available commands. This includes built-in commands (/compress,/model,/title) and every installed skill. You don't need to memorize anything — Tab completion has you covered.

`/`
`/compress`
`/model`
`/title`

Use/verboseto cycle through tool output display modes:off → new → all → verbose. The "all" mode is great for watching what the agent does; "off" is cleanest for simple Q&A.

`/verbose`

## Context Files​

### AGENTS.md: Your Project's Brain​

Create anAGENTS.mdin your project root with architecture decisions, coding conventions, and project-specific instructions. This is automatically injected into every session, so the agent always knows your project's rules.

`AGENTS.md`

```
# Project Context- This is a FastAPI backend with SQLAlchemy ORM- Always use async/await for database operations- Tests go in tests/ and use pytest-asyncio- Never commit .env files
```

### SOUL.md: Customize Personality​

Want Hermes to have a stable default voice? Edit~/.hermes/SOUL.md(or$HERMES_HOME/SOUL.mdif you use a custom Hermes home). Hermes now seeds a starter SOUL automatically and uses that global file as the instance-wide personality source.

`~/.hermes/SOUL.md`
`$HERMES_HOME/SOUL.md`

For a full walkthrough, seeUse SOUL.md with Hermes.

[Use SOUL.md with Hermes](/docs/guides/use-soul-with-hermes)

```
# SoulYou are a senior backend engineer. Be terse and direct.Skip explanations unless asked. Prefer one-liners over verbose solutions.Always consider error handling and edge cases.
```

UseSOUL.mdfor durable personality. UseAGENTS.mdfor project-specific instructions.

`SOUL.md`
`AGENTS.md`

### .cursorrules Compatibility​

Already have a.cursorrulesor.cursor/rules/*.mdcfile? Hermes reads those too. No need to duplicate your coding conventions — they're loaded automatically from the working directory.

`.cursorrules`
`.cursor/rules/*.mdc`

### Discovery​

Hermes loads the top-levelAGENTS.mdfrom the current working directory at session start. SubdirectoryAGENTS.mdfiles are discovered lazily during tool calls (viasubdirectory_hints.py) and injected into tool results — they are not loaded upfront into the system prompt.

`AGENTS.md`
`AGENTS.md`
`subdirectory_hints.py`

Keep context files focused and concise. Every character counts against your token budget since they're injected into every single message.

## Memory & Skills​

### Memory vs. Skills: What Goes Where​

Memoryis for facts: your environment, preferences, project locations, and things the agent has learned about you.Skillsare for procedures: multi-step workflows, tool-specific instructions, and reusable recipes. Use memory for "what," skills for "how."

### When to Create Skills​

If you find a task that takes 5+ steps and you'll do it again, ask the agent to create a skill for it. Say "save what you just did as a skill calleddeploy-staging." Next time, just type/deploy-stagingand the agent loads the full procedure.

`deploy-staging`
`/deploy-staging`

### Managing Memory Capacity​

Memory is intentionally bounded (~2,200 chars for MEMORY.md, ~1,375 chars for USER.md). When it fills up, the agent consolidates entries. You can help by saying "clean up your memory" or "replace the old Python 3.9 note — we're on 3.12 now."

### Let the Agent Remember​

After a productive session, say "remember this for next time" and the agent will save the key takeaways. You can also be specific: "save to memory that our CI uses GitHub Actions with thedeploy.ymlworkflow."

`deploy.yml`

Memory is a frozen snapshot — changes made during a session don't appear in the system prompt until the next session starts. The agent writes to disk immediately, but the prompt cache isn't invalidated mid-session.

## Performance & Cost​

### Don't Break the Prompt Cache​

Most LLM providers cache the conversation prefix (system prompt + history). If you keep your system prompt stable (same context files, same memory), subsequent messages in a session getcache hitsthat are significantly cheaper. The cache is keyed to the model and account — so an explicit/modelswitch, anautomatic provider fallback, or acredential-pool rotationall force the next turn to re-read the entire conversation at full input price. Occasional switches are fine; frequent switching in a long session multiplies your cost.

`/model`
[automatic provider fallback](/docs/user-guide/features/fallback-providers)
[credential-pool rotation](/docs/user-guide/features/credential-pools)

### Use /compress Before Hitting Limits​

Long sessions accumulate tokens. When you notice responses slowing down or getting truncated, run/compress. This summarizes the conversation history, preserving key context while dramatically reducing token count. Use/usageto check where you stand.

`/compress`
`/usage`

### Delegate for Parallel Work​

Need to research three topics at once? Ask the agent to usedelegate_taskwith parallel subtasks. Each subagent runs independently with its own context, and only the final summaries come back — massively reducing your main conversation's token usage.

`delegate_task`

### Use execute_code for Batch Operations​

Instead of running terminal commands one at a time, ask the agent to write a script that does everything at once. "Write a Python script to rename all.jpegfiles to.jpgand run it" is cheaper and faster than renaming files individually.

`.jpeg`
`.jpg`

### Choose the Right Model​

Use/modelto switch models mid-session. Use a frontier model (Claude Sonnet/Opus, GPT-4o) for complex reasoning and architecture decisions. Switch to a faster model for simple tasks like formatting, renaming, or boilerplate generation. Keep in mind each switch resets the prompt cache (see above), so on long sessions it's often cheaper to start a fresh session on the other model than to bounce back and forth.

`/model`

Run/usageperiodically to see your token consumption. Run/insightsfor a broader view of usage patterns over the last 30 days.

`/usage`
`/insights`

## Messaging Tips​

### Set a Home Channel​

Use/sethomein your preferred Telegram or Discord chat to designate it as the home channel. Cron job results and scheduled task outputs are delivered here. Without it, the agent has nowhere to send proactive messages.

`/sethome`

### Use /title to Organize Sessions​

Name your sessions with/title auth-refactoror/title research-llm-quantization. Named sessions are easy to find withhermes sessions listand resume withhermes -r "auth-refactor". Unnamed sessions pile up and become impossible to distinguish.

`/title auth-refactor`
`/title research-llm-quantization`
`hermes sessions list`
`hermes -r "auth-refactor"`

### DM Pairing for Team Access​

Instead of manually collecting user IDs for allowlists, enable DM pairing. When a teammate DMs the bot, they get a one-time pairing code. You approve it withhermes pairing approve telegram XKGH5N7P— simple and secure.

`hermes pairing approve telegram XKGH5N7P`

### Tool Progress Display Modes​

Use/verboseto control how much tool activity you see. In messaging platforms, less is usually more — keep it on "new" to see just new tool calls. In the CLI, "all" gives you a satisfying live view of everything the agent does.

`/verbose`

By default, messaging sessions never auto-reset — context lives until you/resetor compression kicks in. If you want sessions to reset automatically (after idle time or daily at a fixed hour), opt in via thesession_resetsection in~/.hermes/config.yaml.

`/reset`
`session_reset`
`~/.hermes/config.yaml`

## Security​

### Use Docker for Untrusted Code​

When working with untrusted repositories or running unfamiliar code, use Docker or Daytona as your terminal backend. SetTERMINAL_BACKEND=dockerin your.env. Destructive commands inside a container can't harm your host system.

`TERMINAL_BACKEND=docker`
`.env`

```
# In your .env:TERMINAL_BACKEND=dockerTERMINAL_DOCKER_IMAGE=hermes-sandbox:latest
```

### Avoid Windows Encoding Pitfalls​

On Windows, some default encodings (such ascp125x) cannot represent all Unicode characters, which can causeUnicodeEncodeErrorwhen writing files in tests or scripts.

`cp125x`
`UnicodeEncodeError`
- Prefer opening files with an explicit UTF-8 encoding:

```
with open("results.txt", "w", encoding="utf-8") as f:    f.write("✓ All good\n")
```

- In PowerShell, you can also switch the current session to UTF-8 for console and native command output:

```
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
```

This keeps PowerShell and child processes on UTF-8 and helps avoid Windows-only failures.

### Review Before Choosing "Always"​

When the agent triggers a dangerous command approval (rm -rf,DROP TABLE, etc.), you get four options:once,session,always,deny. Think carefully before choosing "always" — it permanently allowlists that pattern. Start with "session" until you're comfortable.

`rm -rf`
`DROP TABLE`

### Command Approval Is Your Safety Net​

Hermes checks every command against a curated list of dangerous patterns before execution. This includes recursive deletes, SQL drops, piping curl to shell, and more. Don't disable this in production — it exists for good reasons.

When running in a container backend (Docker, Singularity, Modal, Daytona), dangerous command checks areskippedbecause the container is the security boundary. Make sure your container images are properly locked down.

### Use Allowlists for Messaging Bots​

Never setGATEWAY_ALLOW_ALL_USERS=trueon a bot with terminal access. Always use platform-specific allowlists (TELEGRAM_ALLOWED_USERS,DISCORD_ALLOWED_USERS) or DM pairing to control who can interact with your agent.

`GATEWAY_ALLOW_ALL_USERS=true`
`TELEGRAM_ALLOWED_USERS`
`DISCORD_ALLOWED_USERS`

```
# Recommended: explicit allowlists per platformTELEGRAM_ALLOWED_USERS=123456789,987654321DISCORD_ALLOWED_USERS=123456789012345678# Or use cross-platform allowlistGATEWAY_ALLOWED_USERS=123456789,987654321
```

Have a tip that should be on this page? Open an issue or PR — community contributions are welcome.

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/guides/tips.md)