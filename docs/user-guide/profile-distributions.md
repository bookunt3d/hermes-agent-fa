---
layout: docs
title: "توزیع پروفایل‌ها"
permalink: /user-guide/profile-distributions/
---

- 
- Using Hermes
- Profile Distributions: Share a Whole Agent

# Profile Distributions: Share a Whole Agent

Aprofile distributionpackages a complete Hermes agent — personality, skills, cron jobs, MCP connections, config — as a git repository. Anyone with access to the repo can install the whole agent with one command, update it in place, and keep their own memories, sessions, and API keys untouched.

If aprofileis a local agent, a distribution is that agent made shareable.

[profile](/docs/user-guide/profiles)

## What this means​

Before distributions, sharing a Hermes agent meant sending someone:

1. Your SOUL.md
2. A list of skills to install
3. Your config.yaml, minus the secrets
4. A description of which MCP servers you wired up
5. Any cron jobs you scheduled
6. Instructions for which env vars to set

…and hoping they assembled it correctly. Every version bump or bug fix meant repeating the handoff.

With distributions, all of that lives in one git repo:

```
my-research-agent/├── distribution.yaml    # manifest: name, version, env-var requirements├── SOUL.md              # the agent's personality / system prompt├── config.yaml          # model, temperature, reasoning, tool defaults├── skills/              # bundled skills that come with the agent├── cron/                # scheduled tasks the agent runs└── mcp.json             # MCP servers the agent connects to
```

Recipients run:

```
hermes profile install github.com/you/my-research-agent --alias
```

…and they now have the whole agent. They fill in their own API keys (.env.EXAMPLE→.env), and they can runmy-research-agent chator address it through Telegram / Discord / Slack / any gateway platform. When you push a new version, they runhermes profile update my-research-agentand pull your changes — their memories and sessions stay put.

`.env.EXAMPLE`
`.env`
`my-research-agent chat`
`hermes profile update my-research-agent`

## Why git?​

We considered tarballs, HTTP archives, a custom format. None of them beat git:

- Zero build step for authors.Push to GitHub; consumers install. There's no "pack this, upload that, update the index" loop.
- Tags, branches, and commits are already the versioning system.A tag push does for us what "pack + upload a release" does for other tools.
- Updates are a fetch.Not a re-download of the whole archive.
- Transparent.Users can browse the repo, read diffs between versions, open issues against it, fork it to customize.
- Private repos work for free.SSH keys,git credentialhelpers, GitHub CLI stored credentials — whatever auth your terminal is already set up for applies transparently.
- Reproducibility is a commit SHA.The same thing pip and npm record.

`git credential`

The tradeoff: recipients need git installed. On any machine running Hermes in 2026, that's already true.

## When should you use a distribution?​

Good fits:

- You're sharing a specialized agent— a compliance monitor, a code reviewer, a research assistant, a customer-support bot — with a team or with the community.
- You're deploying the same agent to multiple machinesand don't want to copy files manually each time.
- You're iterating on an agentand want recipients to pick up new versions with one command.
- You're building an agent as a product— opinionated defaults, curated skills, tuned prompts — that other people should use as a starting point.

Not a fit:

- You just want to back up a profile on your own machine.Usehermes profile export/import— that's what those are for.
- You want to share API keys alongside the agent.auth.jsonand.envare deliberately excluded from distributions. Each installer brings their own credentials.
- You want to share memories / sessions / conversation history.Those are user data, not distribution content. Never shipped.

[hermes profile export/import](/docs/reference/profile-commands#hermes-profile-export)
`hermes profile export`
`import`
`auth.json`
`.env`

Hermes does not control git.The file exclusions described on this page are applied by theinstallerwhen someone runshermes profile installorhermes profile update. They arenotapplied when you rungit addorgit commit.

`hermes profile install`
`hermes profile update`
`git add`
`git commit`

## The lifecycle: author to installer to update​

Below is the full end-to-end flow. Pick the side you care about.

## For authors: publishing a distribution​

### Step 1 — Start from a working profile​

Build and refine the agent like any other profile:

```
hermes profile create research-botresearch-bot setup                    # configure model, API keys# Edit ~/.hermes/profiles/research-bot/SOUL.md# Install skills, wire up MCP servers, schedule cron jobs, etc.research-bot chat                     # dogfood until it feels right
```

### Step 2 — Add adistribution.yaml​

`distribution.yaml`

Create~/.hermes/profiles/research-bot/distribution.yaml:

`~/.hermes/profiles/research-bot/distribution.yaml`

```
name: research-botversion: 1.0.0description: "Autonomous research assistant with arXiv and web tools"hermes_requires: ">=0.12.0"author: "Your Name"license: "MIT"# Tell installers which env vars the agent needs. These are checked against# the installer's shell and existing .env file so they don't get nagged# about keys they already have configured.env_requires:  - name: OPENAI_API_KEY    description: "OpenAI API key (for model access)"    required: true  - name: SERPAPI_KEY    description: "SerpAPI key for web search"    required: false    default: ""
```

That's the whole manifest. Every field exceptnamehas a sensible default.

`name`

### Step 3 — Create a.gitignorebefore the first commit​

`.gitignore`

Do thisbeforerunninggit initorgit add. If you have already chatted with the profile, run setup, or otherwise used it, the directory now contains files you must not ship:.env,auth.json,memories/,sessions/,state.db*,logs/, and more.

`git init`
`git add`
`.env`
`auth.json`
`memories/`
`sessions/`
`state.db*`
`logs/`

Create~/.hermes/profiles/research-bot/.gitignorewith at minimum:

`~/.hermes/profiles/research-bot/.gitignore`

```
# Credentials & secrets — NEVER commitauth.json.env.env.EXAMPLE    # generated by install, not authorship domain# Runtime databases & statestate.dbstate.db-shmstate.db-walhermes_state.dbresponse_store.dbresponse_store.db-shmresponse_store.db-walgateway.pidgateway_state.jsonprocesses.jsonauth.lockactive_profile.update_check# User data — NEVER commitmemories/sessions/logs/plans/workspace/home/# Caches & generated artifactsimage_cache/audio_cache/document_cache/browser_screenshots/cache/# Infrastructure (should not be in profile dir, but safe to exclude)hermes-agent/.worktrees/profiles/bin/node_modules/# User customization namespace — your local overrideslocal/# Checkpoints & backups (can be huge)checkpoints/sandboxes/backups/# Logserrors.log.hermes_history
```

This mirrors thehard-excluded pathsthat the installer strips on its end. Anything else you want to keep out of the repo (scratch files, large assets, local-only skills) should also go in here.

### Step 4 — Push to a git repo​

```
cd ~/.hermes/profiles/research-botgit initgit add .git commit -m "v1.0.0"git remote add origin git@github.com:you/research-bot.gitgit tag v1.0.0git push -u origin main --tags
```

The repo is now a distribution. Anyone with access can install it.

The installer will additionally strip thehard-excluded pathseven if an author somehow ships them — but that only protects installers, not the author.

### Step 5 — Tag versioned releases​

Every time the agent reaches a stable point, bump the version and tag:

```
# Edit distribution.yaml: version: 1.1.0git add distribution.yaml SOUL.md skills/git commit -m "v1.1.0: tighter research SOUL, add arxiv skill"git tag v1.1.0git push --tags
```

Recipients who runhermes profile update research-botwill pull the latest.

`hermes profile update research-bot`

### What the repo looks like​

A complete authored distribution:

```
research-bot/├── .gitignore                   # excludes secrets & user data (see Step 3)├── distribution.yaml            # required├── SOUL.md                      # strongly recommended├── config.yaml                  # model, provider, tool defaults├── mcp.json                     # MCP server connections├── skills/│   ├── arxiv-search/SKILL.md│   ├── paper-summarization/SKILL.md│   └── citation-lookup/SKILL.md├── cron/│   └── weekly-digest.json       # scheduled tasks└── README.md                    # human-facing description (optional)
```

### Distribution-owned vs user-owned​

When an installer updates to a new version, some things get replaced (author's domain) and some things stay put (installer's domain). Defaults:

| Category | Paths | On update |
| --- | --- | --- |
| Distribution-owned | SOUL.md,config.yaml,mcp.json,skills/,cron/,distribution.yaml | Replaced from the new clone |
| Config override | config.yaml | Actually preserved by default — the installer may have tuned model or provider. Pass--force-configon update to reset. |
| User-owned | memories/,sessions/,state.db*,auth.json,.env,logs/,workspace/,plans/,home/,*_cache/,local/ | Never touched |

`SOUL.md`
`config.yaml`
`mcp.json`
`skills/`
`cron/`
`distribution.yaml`
`config.yaml`
`--force-config`
`memories/`
`sessions/`
`state.db*`
`auth.json`
`.env`
`logs/`
`workspace/`
`plans/`
`home/`
`*_cache/`
`local/`

You can override the distribution-owned list in the manifest:

```
distribution_owned:  - SOUL.md  - skills/research/            # only my research skills; other installed skills stay  - cron/digest.json
```

When omitted, the defaults above apply — which is what most distributions want.

## For installers: using a distribution​

### Install​

```
hermes profile install github.com/you/research-bot --alias
```

What happens:

1. Clones the repo into a temporary directory.
2. Readsdistribution.yaml, shows you the manifest (name, version, description, author, required env vars).
3. Checks each required env var against your shell environment and the target profile's existing.env. Marks each as✓ setorneeds settingso you know exactly what to configure.
4. Asks for confirmation. Pass-y/--yesto skip.
5. Copies distribution-owned files into~/.hermes/profiles/research-bot/(or wherever the manifest'snameresolves). Thehard-excluded pathsare stripped during this copy, even if the author accidentally left them in the repo.
6. Writes.env.EXAMPLEwith the required keys commented out — copy to.envand fill in.
7. With--alias, creates a wrapper so you can runresearch-bot chatdirectly.

`distribution.yaml`
`.env`
`✓ set`
`needs setting`
`-y`
`--yes`
`~/.hermes/profiles/research-bot/`
`name`
`.env.EXAMPLE`
`.env`
`--alias`
`research-bot chat`

### Source types​

Any git URL works:

```
# GitHub shorthandhermes profile install github.com/you/research-bot# Full HTTPShermes profile install https://github.com/you/research-bot.git# SSHhermes profile install git@github.com:you/research-bot.git# Self-hosted, GitLab, Gitea, Forgejo — any Git hosthermes profile install https://git.example.com/team/research-bot.git# Private repo using your configured git authhermes profile install git@github.com:your-org/internal-bot.git# Local directory during development (no git push needed)hermes profile install ~/my-profile-in-progress/
```

### Override the profile name​

Two users wanting the same distribution under different profile names:

```
# Alicehermes profile install github.com/acme/support-bot --name support-us --alias# Bob (same distribution, different local name)hermes profile install github.com/acme/support-bot --name support-eu --alias
```

### Fill in env vars​

After install, the agent's profile contains a.env.EXAMPLE:

`.env.EXAMPLE`

```
# Environment variables required by this Hermes distribution.# Copy to `.env` and fill in your own values before running.# OpenAI API key (for model access)# (required)OPENAI_API_KEY=# SerpAPI key for web search# (optional)# SERPAPI_KEY=
```

Copy it:

```
cp ~/.hermes/profiles/research-bot/.env.EXAMPLE ~/.hermes/profiles/research-bot/.env# Edit .env, paste your real keys
```

Required keys that were already in your shell environment (e.g.OPENAI_API_KEYexported in your~/.zshrc) are marked✓ setduring install — you don't need to duplicate them in.env.

`OPENAI_API_KEY`
`~/.zshrc`
`✓ set`
`.env`

### Check what you installed​

```
hermes profile info research-bot
```

Shows:

```
Distribution: research-botVersion:      1.0.0Description:  Autonomous research assistant with arXiv and web toolsAuthor:       Your NameRequires:     Hermes >=0.12.0Source:       https://github.com/you/research-botInstalled:    2026-05-08T17:04:32+00:00Environment variables:  OPENAI_API_KEY (required) — OpenAI API key (for model access)  SERPAPI_KEY (optional) — SerpAPI key for web search
```

hermes profile listalso shows aDistributioncolumn so at a glance you can see which of your profiles came from repos and which you hand-built:

`hermes profile list`
`Distribution`

```
 Profile          Model                        Gateway      Alias        Distribution ───────────────    ───────────────────────────    ───────────    ───────────    ──────────────────── ◆default         claude-sonnet-4              stopped      —            —  coder           gpt-5                        stopped      coder        —  research-bot    claude-opus-4                stopped      research-bot research-bot@1.0.0  telemetry       claude-sonnet-4              running      telemetry    telemetry@2.3.1
```

### Update​

```
hermes profile update research-bot
```

What happens:

1. Re-clones the repo from the recorded source URL.
2. Replaces distribution-owned files (SOUL, skills, cron, mcp.json).
3. Preservesyourconfig.yaml— you may have tuned the model, temperature, or other settings. Pass--force-configto overwrite.
4. Never touchesuser data: memories, sessions, auth,.env, logs, state.

`config.yaml`
`--force-config`
`.env`

No re-downloading the whole archive. No stomping your local changes to config. No deleting your conversation history.

### Remove​

```
hermes profile delete research-bot
```

The delete prompt surfaces distribution info before asking you to confirm:

```
Profile: research-botPath:    ~/.hermes/profiles/research-botModel:   claude-opus-4 (anthropic)Skills:  12Distribution: research-bot@1.0.0Installed from: https://github.com/you/research-botThis will permanently delete:  • All config, API keys, memories, sessions, skills, cron jobs  • Command alias (~/.local/bin/research-bot)Type 'research-bot' to confirm:
```

So you never accidentally delete an agent without knowing where it came from or being able to re-install it.

## Use cases and patterns​

### Personal: sync one agent across machines​

You built a research assistant on your laptop. You want the same agent on your workstation.

```
# Laptop — create .gitignore first (see "For authors" Step 3), then:cd ~/.hermes/profiles/research-botgit init && git add . && git status   # confirm no secrets stagedgit commit -m "initial"git remote add origin git@github.com:you/research-bot.gitgit push -u origin main# Workstationhermes profile install github.com/you/research-bot --alias# Fill in .env. Done.
```

Any iteration on the laptop (git commit && push) pulls onto the workstation withhermes profile update research-bot. Memories stay per-machine — the laptop remembers its own conversations, the workstation remembers its own, they don't collide.

`git commit && push`
`hermes profile update research-bot`

### Team: ship a reviewed internal agent​

Your engineering team wants a shared PR-review bot with a specific SOUL, specific skills, and a cron that runs every PR through it.

```
# Engineering lead — create .gitignore first (see "For authors" Step 3), then:cd ~/.hermes/profiles/pr-reviewer# ... build and tune ...git init && git add . && git status   # confirm no secrets stagedgit commit -m "v1.0 PR reviewer"git tag v1.0.0git push -u origin main --tags    # push to your company's internal Git host# Each engineerhermes profile install git@github.com:your-org/pr-reviewer.git --alias# Fill in .env with their own API key (billed to them), .env.EXAMPLE points at what's requiredpr-reviewer chat
```

When the lead ships v1.1 (better SOUL, new skill), engineers runhermes profile update pr-reviewerand everyone's on the new version within minutes.

`hermes profile update pr-reviewer`

### Community: publish a public agent​

You built something novel — maybe a "Polymarket trader" or an "academic paper summarizer" or a "Minecraft server ops assistant." You want to share it.

```
# You — create .gitignore first (see "For authors" Step 3), then:cd ~/.hermes/profiles/polymarket-trader# Write a solid README.md at the repo root — GitHub shows it on the repo pagegit init && git add . && git status   # confirm no secrets stagedgit commit -m "v1.0"git tag v1.0.0# Publish to a public GitHub repogit remote add origin https://github.com/you/hermes-polymarket-trader.gitgit push -u origin main --tags# Anyonehermes profile install github.com/you/hermes-polymarket-trader --alias
```

Tweet the install command. People who try it send you issues and PRs. If someone wants to customize, they fork — same git workflow everyone already knows.

### Product: ship an opinionated agent​

You built Hermes-on-top — maybe a compliance-monitoring harness, a customer-support stack, a domain-specific research platform. You want to distribute it as a product.

```
# distribution.yamlname: telemetry-harnessversion: 2.3.1description: "Compliance telemetry harness — monitors and reviews regulated workflows"hermes_requires: ">=0.13.0"author: "Acme Compliance Inc."license: "Commercial"env_requires:  - name: ACME_API_KEY    description: "Your Acme Compliance license key (email support@acme.com)"    required: true  - name: OPENAI_API_KEY    description: "OpenAI API key for model access"    required: true  - name: GRAPHITI_MCP_URL    description: "URL for your Graphiti knowledge graph instance"    required: false    default: "http://127.0.0.1:8000/sse"
```

Your customers install via a single command; the install preview tells them exactly which keys to have ready; updates roll out the moment you tag a new release; their compliance data (memories/,sessions/) never leaves their machine.

`memories/`
`sessions/`

### Ephemeral: one-off scripts on shared infra​

You're the ops lead. You want a temporary agent that diagnoses a production incident — a canned SOUL with the right tools and MCP connections — and runs on three on-call engineers' laptops for the next week.

```
# You — create .gitignore first (see "For authors" Step 3), then:# Build the profile, commit, push a private repogit push -u origin main# Each on-callhermes profile install git@github.com:your-org/incident-2026-q2.git --alias# Incident resolved — tear it downhermes profile delete incident-2026-q2
```

The install-delete cycle is cheap enough to be disposable.

## Recipes​

### Pin to a specific version​

Git ref pinning (#v1.2.0) is planned but not in the initial release — install currently tracks the default branch. Track your installed version viahermes profile info <name>and hold off on updates until you're ready.

`#v1.2.0`
`hermes profile info <name>`

### Check what version you're on vs. latest​

```
# Your installed versionhermes profile info research-bot | grep Version# Latest upstream (without installing)git ls-remote --tags https://github.com/you/research-bot | tail -5
```

### Keep local config customizations through updates​

The default update behavior already does this:config.yamlis preserved. To be safe, write your local tweaks to a file the distribution doesn't own:

`config.yaml`

```
# ~/.hermes/profiles/research-bot/local/my-overrides.yaml# (distribution never touches local/)
```

…and reference it fromconfig.yamlor your SOUL as needed.

`config.yaml`

### Force a clean re-install​

```
# Nuke and re-install from scratch (loses memories/sessions too)hermes profile delete research-bot --yeshermes profile install github.com/you/research-bot --alias# Update to current main but reset config.yaml to the distribution's defaulthermes profile update research-bot --force-config --yes
```

### Fork and customize​

The standard git workflow — distributions are just repos:

```
# Fork the repo on GitHub, then install your forkhermes profile install github.com/yourname/forked-research-bot --alias# Iterate locally in ~/.hermes/profiles/forked-research-bot/# Edit SOUL.md, commit, push to your fork# Upstream changes: pull them into your fork the usual way
```

### Test a distribution before pushing​

From the author's machine:

```
# Install from a local directory (no git push needed)hermes profile install ~/.hermes/profiles/research-bot --name research-bot-test --alias# Tweak, delete, re-install until it's righthermes profile delete research-bot-test --yeshermes profile install ~/.hermes/profiles/research-bot --name research-bot-test
```

## What's NOT in a distribution (ever)​

The installer hard-excludes these paths even if an author accidentally ships them. No config option lets you override this — the safety guard is a regression-tested invariant:

- auth.json— OAuth tokens, platform credentials
- .env— API keys, secrets
- memories/— conversation memory
- sessions/— conversation history
- state.db,state.db-shm,state.db-wal— session metadata
- logs/— agent and error logs
- workspace/— generated working files
- plans/— scratch plans
- home/— user's home mount in Docker backends
- *_cache/— image / audio / document caches
- local/— user-reserved customization namespace

`auth.json`
`.env`
`memories/`
`sessions/`
`state.db`
`state.db-shm`
`state.db-wal`
`logs/`
`workspace/`
`plans/`
`home/`
`*_cache/`
`local/`

When you clone a distribution as an installer, these simply aren't copied into your profile directory. When you update, your copies stay put. If you installed the same distribution on five machines, you have five isolated sets of this data — one per machine.

This exclusion runs atinstall / update time on the installer's machine. It doesnotprevent an author from commiting sensitive/unnecessary files. Authors must use a.gitignoreto keep secrets out of the repo.

`.gitignore`

## Security and trust​

Profile distributions are unsigned by default. You're trusting:

- The git host(GitHub / GitLab / wherever) to serve the bytes the author pushed.
- The authorto not ship a malicious SOUL, skills, or cron jobs.

Cron jobs from a distribution arenot auto-scheduled— the installer printshermes -p <name> cron listand you enable them explicitly. SOUL.md and skills ARE active as soon as you start chatting with the profile, so read them before your first run if you're installing from someone you don't know.

`hermes -p <name> cron list`

Rough analogy: installing a distribution is like installing a browser extension or a VS Code extension. Low friction, high power, trust the source. For internal company distributions, use a private repo and your normal git auth — nothing new to configure.

Future versions may add signing, a lockfile (.distribution-lock.yaml) with a resolved commit SHA, and a--dry-runflag that prints the diff before applying an update. None of those are shipping yet.

`.distribution-lock.yaml`
`--dry-run`

## Under the hood​

For implementation details, precise CLI behavior, and all flags, see theProfile Commands reference.

[Profile Commands reference](/docs/reference/profile-commands#distribution-commands)

The short version:

- install,update,infolive insidehermes profile— not a parallel command tree.
- The manifest format is YAML with a tiny required schema (nameonly).
- The installer uses your localgitbinary for cloning, so any auth your shell already handles (SSH keys, credential helpers) works transparently.
- After clone,.git/is stripped — the installed profile isn't itself a git checkout, avoiding "oh my, I accidentally committed my.envto the distribution's git history" traps.
- Reserved profile names (hermes,test,tmp,root,sudo) are rejected at install time to avoid collisions with common binaries.

`install`
`update`
`info`
`hermes profile`
`name`
`git`
`.git/`
`.env`
`hermes`
`test`
`tmp`
`root`
`sudo`

## See also​

- Profiles: Running Multiple Agents— the base concept
- Profile Commands reference— every flag, every option
- hermes profile export/import— local backup / restore (not distribution)
- Using SOUL with Hermes— authoring personalities
- Personality & SOUL— how SOUL fits into the agent
- Skills catalog— skills you can bundle

[Profiles: Running Multiple Agents](/docs/user-guide/profiles)
[Profile Commands reference](/docs/reference/profile-commands)
[hermes profile export/import](/docs/reference/profile-commands#hermes-profile-export)
`hermes profile export`
`import`
[Using SOUL with Hermes](/docs/guides/use-soul-with-hermes)
[Personality & SOUL](/docs/user-guide/features/personality)
[Skills catalog](/docs/reference/skills-catalog)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/profile-distributions.md)