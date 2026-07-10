---
layout: docs
title: "مسیر یادگیری"
permalink: /getting-started/learning-path/
---

- 
- Getting Started
- Learning Path

# Learning Path

Hermes Agent can do a lot — CLI assistant, Telegram/Discord bot, task automation, RL training, and more. This page helps you figure out where to start and what to read based on your experience level and what you're trying to accomplish.

If you haven't installed Hermes Agent yet, begin with theInstallation guideand then run through theQuickstart. Everything below assumes you have a working installation.

[Installation guide](/docs/getting-started/installation)
[Quickstart](/docs/getting-started/quickstart)

First-time users almost always wanthermes setup --portal— one OAuth covers a model plus the four Tool Gateway tools (search/image/TTS/browser). SeeNous Portal.

`hermes setup --portal`
[Nous Portal](/docs/integrations/nous-portal)

## How to Use This Page​

- Know your level?Jump to theexperience-level tableand follow the reading order for your tier.
- Have a specific goal?Skip toBy Use Caseand find the scenario that matches.
- Just browsing?Check theKey Featurestable for a quick overview of everything Hermes Agent can do.

## By Experience Level​

| Level | Goal | Recommended Reading | Time Estimate |
| --- | --- | --- | --- |
| Beginner | Get up and running, have basic conversations, use built-in tools | Installation→Quickstart→CLI Usage→Configuration | ~1 hour |
| Intermediate | Set up messaging bots, use advanced features like memory, cron jobs, and skills | Sessions→Messaging→Tools→Skills→Memory→Cron | ~2–3 hours |
| Advanced | Build custom tools, create skills, train models with RL, contribute to the project | Architecture→Adding Tools→Creating Skills→Contributing | ~4–6 hours |

[Installation](/docs/getting-started/installation)
[Quickstart](/docs/getting-started/quickstart)
[CLI Usage](/docs/user-guide/cli)
[Configuration](/docs/user-guide/configuration)
[Sessions](/docs/user-guide/sessions)
[Messaging](/docs/user-guide/messaging)
[Tools](/docs/user-guide/features/tools)
[Skills](/docs/user-guide/features/skills)
[Memory](/docs/user-guide/features/memory)
[Cron](/docs/user-guide/features/cron)
[Architecture](/docs/developer-guide/architecture)
[Adding Tools](/docs/developer-guide/adding-tools)
[Creating Skills](/docs/developer-guide/creating-skills)
[Contributing](/docs/developer-guide/contributing)

## By Use Case​

Pick the scenario that matches what you want to do. Each one links you to the relevant docs in the order you should read them.

### "I want a CLI coding assistant"​

Use Hermes Agent as an interactive terminal assistant for writing, reviewing, and running code.

1. Installation
2. Quickstart
3. CLI Usage
4. Code Execution
5. Context Files
6. Tips & Tricks

[Installation](/docs/getting-started/installation)
[Quickstart](/docs/getting-started/quickstart)
[CLI Usage](/docs/user-guide/cli)
[Code Execution](/docs/user-guide/features/code-execution)
[Context Files](/docs/user-guide/features/context-files)
[Tips & Tricks](/docs/guides/tips)

Pass files directly into your conversation with context files. Hermes Agent can read, edit, and run code in your projects.

### "I want a Telegram/Discord bot"​

Deploy Hermes Agent as a bot on your favorite messaging platform.

1. Installation
2. Configuration
3. Messaging Overview
4. Telegram Setup
5. Discord Setup
6. Voice Mode
7. Use Voice Mode with Hermes
8. Security

[Installation](/docs/getting-started/installation)
[Configuration](/docs/user-guide/configuration)
[Messaging Overview](/docs/user-guide/messaging)
[Telegram Setup](/docs/user-guide/messaging/telegram)
[Discord Setup](/docs/user-guide/messaging/discord)
[Voice Mode](/docs/user-guide/features/voice-mode)
[Use Voice Mode with Hermes](/docs/guides/use-voice-mode-with-hermes)
[Security](/docs/user-guide/security)

For full project examples, see:

- Daily Briefing Bot
- Team Telegram Assistant

[Daily Briefing Bot](/docs/guides/daily-briefing-bot)
[Team Telegram Assistant](/docs/guides/team-telegram-assistant)

### "I want to automate tasks"​

Schedule recurring tasks, run batch jobs, or chain agent actions together.

1. Quickstart
2. Cron Scheduling
3. Batch Processing
4. Delegation
5. Hooks

[Quickstart](/docs/getting-started/quickstart)
[Cron Scheduling](/docs/user-guide/features/cron)
[Batch Processing](/docs/user-guide/features/batch-processing)
[Delegation](/docs/user-guide/features/delegation)
[Hooks](/docs/user-guide/features/hooks)

Cron jobs let Hermes Agent run tasks on a schedule — daily summaries, periodic checks, automated reports — without you being present.

### "I want to build custom tools/skills"​

Extend Hermes Agent with your own tools and reusable skill packages.

1. Plugins
2. Build a Hermes Plugin
3. Tools Overview
4. Skills Overview
5. MCP (Model Context Protocol)
6. Architecture
7. Adding Tools
8. Creating Skills

[Plugins](/docs/user-guide/features/plugins)
[Build a Hermes Plugin](/docs/developer-guide/plugins)
[Tools Overview](/docs/user-guide/features/tools)
[Skills Overview](/docs/user-guide/features/skills)
[MCP (Model Context Protocol)](/docs/user-guide/features/mcp)
[Architecture](/docs/developer-guide/architecture)
[Adding Tools](/docs/developer-guide/adding-tools)
[Creating Skills](/docs/developer-guide/creating-skills)

For most custom tool creation, start with plugins. TheAdding Toolspage is for built-in Hermes core development, not the usual user/custom-tool path.

[Adding Tools](/docs/developer-guide/adding-tools)

### "I want to train models"​

Use reinforcement learning to fine-tune model behavior with Hermes Agent's RL training pipeline (powered byAtropos).

[Atropos](https://github.com/NousResearch/atropos)
1. Quickstart
2. Configuration
3. Atropos RL Environments(external)
4. Provider Routing
5. Architecture

[Quickstart](/docs/getting-started/quickstart)
[Configuration](/docs/user-guide/configuration)
[Atropos RL Environments](https://github.com/NousResearch/atropos)
[Provider Routing](/docs/user-guide/features/provider-routing)
[Architecture](/docs/developer-guide/architecture)

RL training works best when you already understand the basics of how Hermes Agent handles conversations and tool calls. Run through the Beginner path first if you're new.

### "I want to use it as a Python library"​

Integrate Hermes Agent into your own Python applications programmatically.

1. Installation
2. Quickstart
3. Python Library Guide
4. Architecture
5. Tools
6. Sessions

[Installation](/docs/getting-started/installation)
[Quickstart](/docs/getting-started/quickstart)
[Python Library Guide](/docs/guides/python-library)
[Architecture](/docs/developer-guide/architecture)
[Tools](/docs/user-guide/features/tools)
[Sessions](/docs/user-guide/sessions)

## Key Features at a Glance​

Not sure what's available? Here's a quick directory of major features:

| Feature | What It Does | Link |
| --- | --- | --- |
| Tools | Built-in tools the agent can call (file I/O, search, shell, etc.) | Tools |
| Skills | Installable plugin packages that add new capabilities | Skills |
| Memory | Persistent memory across sessions | Memory |
| Context Files | Feed files and directories into conversations | Context Files |
| MCP | Connect to external tool servers via Model Context Protocol | MCP |
| Cron | Schedule recurring agent tasks | Cron |
| Delegation | Spawn sub-agents for parallel work | Delegation |
| Code Execution | Run Python scripts that call Hermes tools programmatically | Code Execution |
| Browser | Web browsing and scraping | Browser |
| Hooks | Event-driven callbacks and middleware | Hooks |
| Batch Processing | Process multiple inputs in bulk | Batch Processing |
| Provider Routing | Route requests across multiple LLM providers | Provider Routing |

[Tools](/docs/user-guide/features/tools)
[Skills](/docs/user-guide/features/skills)
[Memory](/docs/user-guide/features/memory)
[Context Files](/docs/user-guide/features/context-files)
[MCP](/docs/user-guide/features/mcp)
[Cron](/docs/user-guide/features/cron)
[Delegation](/docs/user-guide/features/delegation)
[Code Execution](/docs/user-guide/features/code-execution)
[Browser](/docs/user-guide/features/browser)
[Hooks](/docs/user-guide/features/hooks)
[Batch Processing](/docs/user-guide/features/batch-processing)
[Provider Routing](/docs/user-guide/features/provider-routing)

## What to Read Next​

Based on where you are right now:

- Just finished installing?→ Head to theQuickstartto run your first conversation.
- Completed the Quickstart?→ ReadCLI UsageandConfigurationto customize your setup.
- Comfortable with the basics?→ ExploreTools,Skills, andMemoryto unlock the full power of the agent.
- Setting up for a team?→ ReadSecurityandSessionsto understand access control and conversation management.
- Ready to build?→ Jump into theDeveloper Guideto understand the internals and start contributing.
- Want practical examples?→ Check out theGuidessection for real-world projects and tips.

[Quickstart](/docs/getting-started/quickstart)
[CLI Usage](/docs/user-guide/cli)
[Configuration](/docs/user-guide/configuration)
[Tools](/docs/user-guide/features/tools)
[Skills](/docs/user-guide/features/skills)
[Memory](/docs/user-guide/features/memory)
[Security](/docs/user-guide/security)
[Sessions](/docs/user-guide/sessions)
[Developer Guide](/docs/developer-guide/architecture)
[Guides](/docs/guides/tips)

You don't need to read everything. Pick the path that matches your goal, follow the links in order, and you'll be productive quickly. You can always come back to this page to find your next step.

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/learning-path.md)