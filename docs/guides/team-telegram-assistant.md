---
layout: docs
title: "دستیار تلگرام تیمی"
permalink: /docs/guides/team-telegram-assistant/
---

- 
- Guides & Tutorials
- Tutorial: Team Telegram Assistant

# Set Up a Team Telegram Assistant

This tutorial walks you through setting up a Telegram bot powered by Hermes Agent that multiple team members can use. By the end, your team will have a shared AI assistant they can message for help with code, research, system administration, and anything else — secured with per-user authorization.

## What We're Building​

A Telegram bot that:

- Any authorized team membercan DM for help — code reviews, research, shell commands, debugging
- Runs on your serverwith full tool access — terminal, file editing, web search, code execution
- Per-user sessions— each person gets their own conversation context
- Secure by default— only approved users can interact, with two authorization methods
- Scheduled tasks— daily standups, health checks, and reminders delivered to a team channel

## Prerequisites​

Before starting, make sure you have:

- Hermes Agent installedon a server or VPS (not your laptop — the bot needs to stay running). Follow theinstallation guideif you haven't yet.
- A Telegram accountfor yourself (the bot owner)
- An LLM provider configured— at minimum, an API key for OpenAI, Anthropic, or another supported provider in~/.hermes/.env

`~/.hermes/.env`

A $5/month VPS is plenty for running the gateway. Hermes itself is lightweight — the LLM API calls are what cost money, and those happen remotely.

## Step 1: Create a Telegram Bot​

Every Telegram bot starts with@BotFather— Telegram's official bot for creating bots.

1. Open Telegramand search for@BotFather, or go tot.me/BotFather
2. Send/newbot— BotFather will ask you two things:Display name— what users see (e.g.,Team Hermes Assistant)Username— must end inbot(e.g.,myteam_hermes_bot)
3. Copy the bot token— BotFather replies with something like:Use this token to access the HTTP API:7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...Save this token — you'll need it in the next step.
4. Set a description(optional but recommended):/setdescriptionChoose your bot, then enter something like:Team AI assistant powered by Hermes Agent. DM me for help with code, research, debugging, and more.
5. Set bot commands(optional — gives users a command menu):/setcommandsChoose your bot, then paste:new - Start a fresh conversationmodel - Show or change the AI modelstatus - Show session infohelp - Show available commandsstop - Stop the current task

Open Telegramand search for@BotFather, or go tot.me/BotFather

`@BotFather`

Send/newbot— BotFather will ask you two things:

`/newbot`
- Display name— what users see (e.g.,Team Hermes Assistant)
- Username— must end inbot(e.g.,myteam_hermes_bot)

`Team Hermes Assistant`
`bot`
`myteam_hermes_bot`

Copy the bot token— BotFather replies with something like:

```
Use this token to access the HTTP API:7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...
```

Save this token — you'll need it in the next step.

Set a description(optional but recommended):

```
/setdescription
```

Choose your bot, then enter something like:

```
Team AI assistant powered by Hermes Agent. DM me for help with code, research, debugging, and more.
```

Set bot commands(optional — gives users a command menu):

```
/setcommands
```

Choose your bot, then paste:

```
new - Start a fresh conversationmodel - Show or change the AI modelstatus - Show session infohelp - Show available commandsstop - Stop the current task
```

Keep your bot token secret. Anyone with the token can control the bot. If it leaks, use/revokein BotFather to generate a new one.

`/revoke`

## Step 2: Configure the Gateway​

You have two options: the interactive setup wizard (recommended) or manual configuration.

### Option A: Interactive Setup (Recommended)​

```
hermes gateway setup
```

This walks you through everything with arrow-key selection. PickTelegram, paste your bot token, and enter your user ID when prompted.

### Option B: Manual Configuration​

Add these lines to~/.hermes/.env:

`~/.hermes/.env`

```
# Telegram bot token from BotFatherTELEGRAM_BOT_TOKEN=7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...# Your Telegram user ID (numeric)TELEGRAM_ALLOWED_USERS=123456789
```

### Finding Your User ID​

Your Telegram user ID is a numeric value (not your username). To find it:

1. Message@userinfoboton Telegram
2. It instantly replies with your numeric user ID
3. Copy that number intoTELEGRAM_ALLOWED_USERS

`TELEGRAM_ALLOWED_USERS`

Telegram user IDs are permanent numbers like123456789. They're different from your@username, which can change. Always use the numeric ID for allowlists.

`123456789`
`@username`

## Step 3: Start the Gateway​

### Quick Test​

Run the gateway in the foreground first to make sure everything works:

```
hermes gateway
```

You should see output like:

```
[Gateway] Starting Hermes Gateway...[Gateway] Telegram adapter connected[Gateway] Cron scheduler started (tick every 60s)
```

Open Telegram, find your bot, and send it a message. If it replies, you're in business. PressCtrl+Cto stop.

`Ctrl+C`

### Production: Install as a Service​

For a persistent deployment that survives reboots:

```
hermes gateway installsudo hermes gateway install --system   # Linux only: boot-time system service
```

This creates a background service: a user-levelsystemdservice on Linux by default, alaunchdservice on macOS, or a boot-time Linux system service if you pass--system.

`--system`

```
# Linux — manage the default user servicehermes gateway starthermes gateway stophermes gateway status# View live logsjournalctl --user -u hermes-gateway -f# Keep running after SSH logoutsudo loginctl enable-linger $USER# Linux servers — explicit system-service commandssudo hermes gateway start --systemsudo hermes gateway status --systemjournalctl -u hermes-gateway -f
```

```
# macOS — manage the servicehermes gateway starthermes gateway stoptail -f ~/.hermes/logs/gateway.log
```

The launchd plist captures your shell PATH at install time so gateway subprocesses can find tools like Node.js and ffmpeg. If you install new tools later, re-runhermes gateway installto update the plist.

`hermes gateway install`

### Verify It's Running​

```
hermes gateway status
```

Then send a test message to your bot on Telegram. You should get a response within a few seconds.

## Step 4: Set Up Team Access​

Now let's give your teammates access. There are two approaches.

### Approach A: Static Allowlist​

Collect each team member's Telegram user ID (have them message@userinfobot) and add them as a comma-separated list:

```
# In ~/.hermes/.envTELEGRAM_ALLOWED_USERS=123456789,987654321,555555555
```

Restart the gateway after changes:

```
hermes gateway stop && hermes gateway start
```

### Approach B: DM Pairing (Recommended for Teams)​

DM pairing is more flexible — you don't need to collect user IDs upfront. Here's how it works:

1. Teammate DMs the bot— since they're not on the allowlist, the bot replies with a one-time pairing code:🔐 Pairing code: XKGH5N7PSend this code to the bot owner for approval.
2. Teammate sends you the code(via any channel — Slack, email, in person)
3. You approve iton the server:hermes pairing approve telegram XKGH5N7P
4. They're in— the bot immediately starts responding to their messages

Teammate DMs the bot— since they're not on the allowlist, the bot replies with a one-time pairing code:

```
🔐 Pairing code: XKGH5N7PSend this code to the bot owner for approval.
```

Teammate sends you the code(via any channel — Slack, email, in person)

You approve iton the server:

```
hermes pairing approve telegram XKGH5N7P
```

They're in— the bot immediately starts responding to their messages

Managing paired users:

```
# See all pending and approved usershermes pairing list# Revoke someone's accesshermes pairing revoke telegram 987654321# Clear expired pending codeshermes pairing clear-pending
```

DM pairing is ideal for teams because you don't need to restart the gateway when adding new users. Approvals take effect immediately.

### Security Considerations​

- Never setGATEWAY_ALLOW_ALL_USERS=trueon a bot with terminal access — anyone who finds your bot could run commands on your server
- Pairing codes expire after1 hourand use cryptographic randomness
- Rate limiting prevents brute-force attacks: 1 request per user per 10 minutes, max 3 pending codes per platform
- After 5 failed approval attempts, the platform enters a 1-hour lockout
- All pairing data is stored withchmod 0600permissions

`GATEWAY_ALLOW_ALL_USERS=true`
`chmod 0600`

## Step 5: Configure the Bot​

### Set a Home Channel​

Ahome channelis where the bot delivers cron job results and proactive messages. Without one, scheduled tasks have nowhere to send output.

Option 1:Use the/sethomecommand in any Telegram group or chat where the bot is a member.

`/sethome`

Option 2:Set it manually in~/.hermes/.env:

`~/.hermes/.env`

```
TELEGRAM_HOME_CHANNEL=-1001234567890TELEGRAM_HOME_CHANNEL_NAME="Team Updates"
```

To find a channel ID, add@userinfobotto the group — it will report the group's chat ID.

### Configure Tool Progress Display​

Control how much detail the bot shows when using tools. In~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
display:  tool_progress: new    # off | new | all | verbose
```

| Mode | What You See |
| --- | --- |
| off | Clean responses only — no tool activity |
| new | Brief status for each new tool call (recommended for messaging) |
| all | Every tool call with details |
| verbose | Full tool output including command results |

`off`
`new`
`all`
`verbose`

Users can also change this per-session with the/verbosecommand in chat.

`/verbose`

### Set Up a Personality with SOUL.md​

Customize how the bot communicates by editing~/.hermes/SOUL.md:

`~/.hermes/SOUL.md`

For a full guide, seeUse SOUL.md with Hermes.

```
# SoulYou are a helpful team assistant. Be concise and technical.Use code blocks for any code. Skip pleasantries — the teamvalues directness. When debugging, always ask for error logsbefore guessing at solutions.
```

### Add Project Context​

If your team works on specific projects, create context files so the bot knows your stack:

```
<!-- ~/.hermes/AGENTS.md --># Team Context- We use Python 3.12 with FastAPI and SQLAlchemy- Frontend is React with TypeScript- CI/CD runs on GitHub Actions- Production deploys to AWS ECS- Always suggest writing tests for new code
```

Context files are injected into every session's system prompt. Keep them concise — every character counts against your token budget.

## Step 6: Set Up Scheduled Tasks​

With the gateway running, you can schedule recurring tasks that deliver results to your team channel.

### Daily Standup Summary​

Message the bot on Telegram:

```
Every weekday at 9am, check the GitHub repository atgithub.com/myorg/myproject for:1. Pull requests opened/merged in the last 24 hours2. Issues created or closed3. Any CI/CD failures on the main branchFormat as a brief standup-style summary.
```

The agent creates a cron job automatically and delivers results to the chat where you asked (or the home channel).

### Server Health Check​

```
Every 6 hours, check disk usage with 'df -h', memory with 'free -h',and Docker container status with 'docker ps'. Report anything unusual —partitions above 80%, containers that have restarted, or high memory usage.
```

### Managing Scheduled Tasks​

```
# From the CLIhermes cron list          # View all scheduled jobshermes cron status        # Check if scheduler is running# From Telegram chat/cron list                # View jobs/cron remove <job_id>     # Remove a job
```

Cron job prompts run in completely fresh sessions with no memory of prior conversations. Make sure each prompt containsallthe context the agent needs — file paths, URLs, server addresses, and clear instructions.

## Production Tips​

### Use Docker for Safety​

On a shared team bot, use Docker as the terminal backend so agent commands run in a container instead of on your host:

```
# In ~/.hermes/.envTERMINAL_BACKEND=dockerTERMINAL_DOCKER_IMAGE=nikolaik/python-nodejs:python3.11-nodejs20
```

Or in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
terminal:  backend: docker  container_cpu: 1  container_memory: 5120  container_persistent: true
```

This way, even if someone asks the bot to run something destructive, your host system is protected.

### Monitor the Gateway​

```
# Check if the gateway is runninghermes gateway status# Watch live logs (Linux)journalctl --user -u hermes-gateway -f# Watch live logs (macOS)tail -f ~/.hermes/logs/gateway.log
```

### Keep Hermes Updated​

From Telegram, send/updateto the bot — it will pull the latest version and restart. Or from the server:

`/update`

```
hermes updatehermes gateway stop && hermes gateway start
```

### Log Locations​

| What | Location |
| --- | --- |
| Gateway logs | journalctl --user -u hermes-gateway(Linux) or~/.hermes/logs/gateway.log(macOS) |
| Cron job output | ~/.hermes/cron/output/{job_id}/{timestamp}.md |
| Cron job definitions | ~/.hermes/cron/jobs.json |
| Pairing data | ~/.hermes/pairing/ |
| Session history | ~/.hermes/sessions/ |

`journalctl --user -u hermes-gateway`
`~/.hermes/logs/gateway.log`
`~/.hermes/cron/output/{job_id}/{timestamp}.md`
`~/.hermes/cron/jobs.json`
`~/.hermes/pairing/`
`~/.hermes/sessions/`

## Going Further​

You've got a working team Telegram assistant. Here are some next steps:

- Security Guide— deep dive into authorization, container isolation, and command approval
- Messaging Gateway— full reference for gateway architecture, session management, and chat commands
- Telegram Setup— platform-specific details including voice messages and TTS
- Scheduled Tasks— advanced cron scheduling with delivery options and cron expressions
- Context Files— AGENTS.md, SOUL.md, and .cursorrules for project knowledge
- Personality— built-in personality presets and custom persona definitions
- Add more platforms— the same gateway can simultaneously runDiscord,Slack, andWhatsApp

Questions or issues? Open an issue on GitHub — contributions are welcome.