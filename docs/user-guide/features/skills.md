---
layout: docs
title: "مهارت‌ها"
permalink: /user-guide/features/skills/
---

- 
- Features
- Core
- Skills System

# Skills System

Skills are on-demand knowledge documents the agent can load when needed. They follow aprogressive disclosurepattern to minimize token usage and are compatible with theagentskills.ioopen standard.

[agentskills.io](https://agentskills.io/specification)

All skills live in~/.hermes/skills/— the primary directory and source of truth. On fresh install, bundled skills are copied from the repo. Hub-installed and agent-created skills also go here. The agent can modify or delete any skill.

`~/.hermes/skills/`

You can also point Hermes atexternal skill directories— additional folders scanned alongside the local one. SeeExternal Skill Directoriesbelow.

See also:

- Bundled Skills Catalog
- Official Optional Skills Catalog

[Bundled Skills Catalog](/docs/reference/skills-catalog)
[Official Optional Skills Catalog](/docs/reference/optional-skills-catalog)

## Starting with a blank slate​

By default every profile is seeded with the bundled skill catalog, and eachhermes updateadds any newly bundled skills. If you want a profile withno bundled skills— and that stays empty across updates — you have two paths:

`hermes update`

At install time(applies to the default~/.hermesprofile):

`~/.hermes`

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --no-skills
```

At profile-create time(named profiles):

```
hermes profile create research --no-skills
```

On an already-installed profile(default or named), toggle it at runtime:

```
hermes skills opt-out            # stop future seeding — nothing on disk is touchedhermes skills opt-out --remove   # also delete UNMODIFIED bundled skills (confirms first)hermes skills opt-in --sync      # undo: remove the marker and re-seed now
```

All three paths write a.no-bundled-skillsmarker into the profile directory. While the marker is present, the installer,hermes update, and any skill sync all skip bundled-skill seeding for that profile. Delete the marker (or runhermes skills opt-in) to re-enable.

`.no-bundled-skills`
`hermes update`
`hermes skills opt-in`

hermes skills opt-outonly stopsfutureseeding — it never deletes anything already on disk. The optional--removeflag deletes bundled skillsonlywhen they are unmodified (byte-identical to the version Hermes installed). Skills you have edited, skills installed from the hub, and skills you wrote yourself are always kept.

`hermes skills opt-out`
`--remove`

## Using Skills​

Every installed skill is automatically available as a slash command:

```
# In the CLI or any messaging platform:/gif-search funny cats/axolotl help me fine-tune Llama 3 on my dataset/github-pr-workflow create a PR for the auth refactor/plan design a rollout for migrating our auth provider# Just the skill name loads it and lets the agent ask what you need:/excalidraw
```

### Stacking multiple skills in one command​

You can invoke several skills in a single message by chaining slash commands
at the start — every leading/skilltoken (up to 5) is loaded, and the rest
becomes your instruction:

`/skill`

```
/github-pr-workflow /test-driven-development fix issue #123 and open a PR
```

Parsing stops at the first token that isn't an installed skill, so arguments
that happen to start with/(like file paths) are never swallowed:

`/`

```
/ocr-and-documents /tmp/scan.pdf extract the tables   # loads one skill; /tmp/scan.pdf is the argument
```

For combinations you use repeatedly, prefer askill bundle—
same effect under one short command.

The bundledplanskill is a good example. Running/plan [request]loads the skill's instructions, telling Hermes to inspect context if needed, write a markdown implementation plan instead of executing the task, and save the result under.hermes/plans/relative to the active workspace/backend working directory.

`plan`
`/plan [request]`
`.hermes/plans/`

You can also interact with skills through natural conversation:

```
hermes chat --toolsets skills -q "What skills do you have?"hermes chat --toolsets skills -q "Show me the axolotl skill"
```

## Learning a skill from sources (/learn)​

`/learn`

/learnis the fast way to turn something you already know — or a pile of
reference material — into a reusable skill, without hand-writing theSKILL.md. It is open-ended: point it atanything you can describeand the
agent gathers the material with the tools it already has, then authors a skill
that follows thehouse authoring standards(≤60-char
description, the standard section order, Hermes-tool framing, no invented
commands).

`/learn`
`SKILL.md`

```
# A local SDK or doc directory — read with read_file / search_files/learn the REST client in ~/projects/acme-sdk, focus on auth + pagination# An online doc page — fetched with web_extract/learn https://docs.example.com/api/quickstart# The workflow you just walked the agent through in this conversation/learn how I just deployed the staging server# Pasted notes / a described procedure/learn filing an expense: open the portal, New > Expense, attach the receipt, submit
```

Because the live agent does the sourcing,/learnworks the same in the CLI,
the messaging gateway, the TUI, and the dashboard — and on any terminal backend
(local, Docker, remote), since there is no separate ingestion engine. In thedashboard, the Skills page has aLearn a skillbutton that opens a panel
with a directory field, a URL field, and an open-ended text box; it composes a/learnrequest and runs it in chat.

`/learn`
`/learn`

There is no model-tool footprint:/learnbuilds a standards-guided prompt and
hands it to the agent as a normal turn. The agent saves the result with theskill_managetool, so thewrite-approval gateapplies if you have it on.

`/learn`
`skill_manage`

## Progressive Disclosure​

Skills use a token-efficient loading pattern:

```
Level 0: skills_list()           → [{name, description, category}, ...]   (~3k tokens)Level 1: skill_view(name)        → Full content + metadata       (varies)Level 2: skill_view(name, path)  → Specific reference file       (varies)
```

The agent only loads the full skill content when it actually needs it.

## SKILL.md Format​

```
---name: my-skilldescription: Brief description of what this skill doesversion: 1.0.0platforms: [macos, linux]     # Optional — restrict to specific OS platformsmetadata:  hermes:    tags: [python, automation]    category: devops    fallback_for_toolsets: [web]    # Optional — conditional activation (see below)    requires_toolsets: [terminal]   # Optional — conditional activation (see below)    config:                          # Optional — config.yaml settings      - key: my.setting        description: "What this controls"        default: "value"        prompt: "Prompt for setup"---# Skill Title## When to UseTrigger conditions for this skill.## Procedure1. Step one2. Step two## Pitfalls- Known failure modes and fixes## VerificationHow to confirm it worked.
```

### Platform-Specific Skills​

Skills can restrict themselves to specific operating systems using theplatformsfield:

`platforms`

| Value | Matches |
| --- | --- |
| macos | macOS (Darwin) |
| linux | Linux |
| windows | Windows |

`macos`
`linux`
`windows`

```
platforms: [macos]            # macOS only (e.g., iMessage, Apple Reminders, FindMy)platforms: [macos, linux]     # macOS and Linux
```

When set, the skill is automatically hidden from the system prompt,skills_list(), and slash commands on incompatible platforms. If omitted, the skill loads on all platforms.

`skills_list()`

## Skill output and media delivery​

When a skill response (or any agent response) includes a bare absolute path to a media file — for example/home/user/screenshots/diagram.png— the gateway auto-detects it, strips it from the visible text, and delivers the file natively to the user's chat (Telegram photo, Discord attachment, etc.) instead of leaving the raw path in the message.

`/home/user/screenshots/diagram.png`

For audio specifically, the[[audio_as_voice]]directive promotes audio files to native voice-message bubbles on platforms that support them (Telegram, WhatsApp).

`[[audio_as_voice]]`

### Forcing document-style delivery:[[as_document]]​

`[[as_document]]`

Sometimes you want theoppositeof inline preview: you want the file delivered as a downloadable attachment, not a re-compressed image bubble. The classic example is a high-resolution screenshot or chart — Telegram'ssendPhotorecompresses it to ~200 KB at 1280 px, destroying readability. A 1-2 MB PNG sent viasendDocumentkeeps the original bytes intact.

`sendPhoto`
`sendDocument`

If a response (or any text inside it — typically the last line) contains the literal directive[[as_document]], every media path extracted from that response is delivered as a document/file attachment rather than an image bubble:

`[[as_document]]`

```
Here is your rendered chart:/home/user/.hermes/cache/chart-q4-2025.png[[as_document]]
```

The directive is stripped before delivery, so users never see it. Granularity is intentionally all-or-nothing per response: emit[[as_document]]once and every image path in the same response is delivered as a document. This mirrors the scope of[[audio_as_voice]].

`[[as_document]]`
`[[audio_as_voice]]`

Use it from a skill when:

- You produce screenshots or charts the user needs as files (for editing in another tool, archiving, sharing intact).
- The default lossy preview would obscure detail (small text, pixel-accurate diagrams, color-sensitive renders).

Platforms without a separate document path (e.g. SMS) fall back to whatever attachment mechanism they have.

### Conditional Activation (Fallback Skills)​

Skills can automatically show or hide themselves based on which tools are available in the current session. This is most useful forfallback skills— free or local alternatives that should only appear when a premium tool is unavailable.

```
metadata:  hermes:    fallback_for_toolsets: [web]      # Show ONLY when these toolsets are unavailable    requires_toolsets: [terminal]     # Show ONLY when these toolsets are available    fallback_for_tools: [web_search]  # Show ONLY when these specific tools are unavailable    requires_tools: [terminal]        # Show ONLY when these specific tools are available
```

| Field | Behavior |
| --- | --- |
| fallback_for_toolsets | Skill ishiddenwhen the listed toolsets are available. Shown when they're missing. |
| fallback_for_tools | Same, but checks individual tools instead of toolsets. |
| requires_toolsets | Skill ishiddenwhen the listed toolsets are unavailable. Shown when they're present. |
| requires_tools | Same, but checks individual tools. |

`fallback_for_toolsets`
`fallback_for_tools`
`requires_toolsets`
`requires_tools`

Example:The built-induckduckgo-searchskill usesfallback_for_toolsets: [web]. When you haveFIRECRAWL_API_KEYset, the web toolset is available and the agent usesweb_search— the DuckDuckGo skill stays hidden. If the API key is missing, the web toolset is unavailable and the DuckDuckGo skill automatically appears as a fallback.

`duckduckgo-search`
`fallback_for_toolsets: [web]`
`FIRECRAWL_API_KEY`
`web_search`

Skills without any conditional fields behave exactly as before — they're always shown.

## Secure Setup on Load​

Skills can declare required environment variables without disappearing from discovery:

```
required_environment_variables:  - name: TENOR_API_KEY    prompt: Tenor API key    help: Get a key from https://developers.google.com/tenor    required_for: full functionality
```

When a missing value is encountered, Hermes asks for it securely only when the skill is actually loaded in the local CLI. You can skip setup and keep using the skill. Messaging surfaces never ask for secrets in chat — they tell you to usehermes setupor~/.hermes/.envlocally instead.

`hermes setup`
`~/.hermes/.env`

Once set, declared env vars areautomatically passed throughtoexecute_codeandterminalsandboxes — the skill's scripts can use$TENOR_API_KEYdirectly. For non-skill env vars, use theterminal.env_passthroughconfig option. SeeEnvironment Variable Passthroughfor details.

`execute_code`
`terminal`
`$TENOR_API_KEY`
`terminal.env_passthrough`
[Environment Variable Passthrough](/docs/user-guide/security#environment-variable-passthrough)

### Skill Config Settings​

Skills can also declare non-secret config settings (paths, preferences) stored inconfig.yaml:

`config.yaml`

```
metadata:  hermes:    config:      - key: myplugin.path        description: Path to the plugin data directory        default: "~/myplugin-data"        prompt: Plugin data directory path
```

Settings are stored underskills.configin your config.yaml.hermes config migrateprompts for unconfigured settings, andhermes config showdisplays them. When a skill loads, its resolved config values are injected into the context so the agent knows the configured values automatically.

`skills.config`
`hermes config migrate`
`hermes config show`

SeeSkill SettingsandCreating Skills — Config Settingsfor details.

[Skill Settings](/docs/user-guide/configuration#skill-settings)
[Creating Skills — Config Settings](/docs/developer-guide/creating-skills#config-settings-configyaml)

## Skill Directory Structure​

```
~/.hermes/skills/                  # Single source of truth├── mlops/                         # Category directory│   ├── axolotl/│   │   ├── SKILL.md               # Main instructions (required)│   │   ├── references/            # Additional docs│   │   ├── templates/             # Output formats│   │   ├── scripts/               # Helper scripts callable from the skill│   │   └── assets/                # Supplementary files│   └── vllm/│       └── SKILL.md├── devops/│   └── deploy-k8s/                # Agent-created skill│       ├── SKILL.md│       └── references/├── .hub/                          # Skills Hub state│   ├── lock.json│   ├── quarantine/│   └── audit.log└── .bundled_manifest              # Tracks seeded bundled skills
```

## External Skill Directories​

If you maintain skills outside of Hermes — for example, a shared~/.agents/skills/directory used by multiple AI tools — you can tell Hermes to scan those directories too.

`~/.agents/skills/`

Addexternal_dirsunder theskillssection in~/.hermes/config.yaml:

`external_dirs`
`skills`
`~/.hermes/config.yaml`

```
skills:  external_dirs:    - ~/.agents/skills    - /home/shared/team-skills    - ${SKILLS_REPO}/skills
```

Paths support~expansion and${VAR}environment variable substitution.

`~`
`${VAR}`

### How it works​

- Create locally, update in place: New agent-created skills are written to~/.hermes/skills/. Existing skills are modified where they are found, including skills underexternal_dirs, when the agent usesskill_manageactions such aspatch,edit,write_file,remove_file, ordelete.
- External dirs are not a write-protection boundary: If an external skill directory is writable by the Hermes process, agent-managed skill updates can change files in that directory. Use filesystem permissions or a separate profile/toolset setup if shared external skills must stay read-only.
- Local precedence: If the same skill name exists in both the local dir and an external dir, the local version wins.
- Full integration: External skills appear in the system prompt index,skills_list,skill_view, and as/skill-nameslash commands — no different from local skills.
- Non-existent paths are silently skipped: If a configured directory doesn't exist, Hermes ignores it without errors. Useful for optional shared directories that may not be present on every machine.

`~/.hermes/skills/`
`external_dirs`
`skill_manage`
`patch`
`edit`
`write_file`
`remove_file`
`delete`
`skills_list`
`skill_view`
`/skill-name`

### Example​

```
~/.hermes/skills/               # Local (primary, read-write)├── devops/deploy-k8s/│   └── SKILL.md└── mlops/axolotl/    └── SKILL.md~/.agents/skills/               # External (shared, mutable if writable)├── my-custom-workflow/│   └── SKILL.md└── team-conventions/    └── SKILL.md
```

All four skills appear in your skill index. If you create a new skill calledmy-custom-workflowlocally, it shadows the external version.

`my-custom-workflow`

## Skill Bundles​

Skill bundles are tiny YAML files that group several skills under a single slash command. When you run/<bundle-name>, every skill listed in the bundle loads at once — useful when a particular task always benefits from the same set of skills together.

`/<bundle-name>`

### Quick example​

```
# Create a bundle for backend feature workhermes bundles create backend-dev \  --skill github-code-review \  --skill test-driven-development \  --skill github-pr-workflow \  -d "Backend feature work — review, test, PR workflow"
```

Then in the CLI or any gateway platform:

```
/backend-dev refactor the auth middleware
```

The agent receives all three skills loaded into one user message, with any text after the slash command attached as a user instruction.

### YAML schema​

Bundles live in~/.hermes/skill-bundles/<slug>.yamland look like this:

`~/.hermes/skill-bundles/<slug>.yaml`

```
name: backend-devdescription: Backend feature work — review, test, PR workflow.skills:  - github-code-review  - test-driven-development  - github-pr-workflowinstruction: |  Always start by writing failing tests, then implement.  Open the PR through the standard workflow with co-author tags.
```

Fields:

- name(optional — defaults to the filename stem) — the bundle's display name. Normalized to a hyphen slug for the slash command (Backend Dev→/backend-dev).
- description(optional) — short text shown in/bundlesandhermes bundles list.
- skills(required, non-empty list) — skill names or paths relative to your skills directory. Use the same identifier you'd pass to/<skill-name>.
- instruction(optional) — extra guidance prepended to the loaded skill content. Useful for codifying "how we always use these together."

`name`
`Backend Dev`
`/backend-dev`
`description`
`/bundles`
`hermes bundles list`
`skills`
`/<skill-name>`
`instruction`

### Managing bundles​

```
# List all installed bundleshermes bundles list# Inspect one bundlehermes bundles show backend-dev# Create a bundle interactively (omit --skill flags to enter them one per line)hermes bundles create research# Overwrite an existing bundlehermes bundles create backend-dev --skill ... --force# Delete a bundlehermes bundles delete backend-dev# Re-scan ~/.hermes/skill-bundles/ and report changeshermes bundles reload
```

From inside a chat session,/bundleslists every installed bundle and its skills.

`/bundles`

### Behavior​

- Bundles take precedence over individual skillswhen slugs collide. If you name a bundleresearchand you also have a skill calledresearch,/researchinvokes the bundle. This is intentional — you opted into the bundle by naming it.
- Missing skills are skipped, not fatal.If a bundle listsskill-fooand you haven't installed it, the bundle still loads the skills that do resolve, and the agent gets a note listing what was skipped.
- Bundles work in every surface— interactive CLI, TUI, dashboard chat, and every gateway platform (Telegram, Discord, Slack, …) — because dispatch is centralized in the same place as individual skill commands.
- Bundles do not invalidate the prompt cache.They generate a fresh user message at invocation time, the same way/<skill-name>does — no system prompt mutation.

`research`
`research`
`/research`
`skill-foo`
`/<skill-name>`

### When bundles beat installing each skill manually​

Use a bundle when:

- You always pair the same skills for a recurring task (/backend-dev,/release-prep,/incident-response).
- You want a one-character-shorter mental model than typing several/skillinvocations in a row.
- You want to ship a team-wide "task profile" by checking the bundle YAML into a shared dotfiles repo and symlinking it into~/.hermes/skill-bundles/.

`/backend-dev`
`/release-prep`
`/incident-response`
`/skill`
`~/.hermes/skill-bundles/`

A bundle is just a YAML alias — it doesn't install skills for you. The skills themselves must already be present (in~/.hermes/skills/or an external skill directory). Otherwise the bundle invocation just skips the missing ones.

`~/.hermes/skills/`

## Agent-Managed Skills (skill_manage tool)​

The agent can create, update, and delete its own skills via theskill_managetool. This is the agent'sprocedural memory— when it figures out a non-trivial workflow, it saves the approach as a skill for future reuse.

`skill_manage`

Skills and memory work together in the self-improvement loop: memory stores
small durable facts that should always be in context, while skills store longer
procedures that should load only when relevant. The background review can
suggest or stage skill changes after a session, but the write-approval gate
below lets you require human review before those changes land.

### When the Agent Creates Skills​

- After completing a complex task (5+ tool calls) successfully
- When it hit errors or dead ends and found the working path
- When the user corrected its approach
- When it discovered a non-trivial workflow

### Actions​

| Action | Use for | Key params |
| --- | --- | --- |
| create | New skill from scratch | name,content(full SKILL.md), optionalcategory |
| patch | Targeted fixes (preferred) | name,old_string,new_string |
| edit | Major structural rewrites | name,content(full SKILL.md replacement) |
| delete | Remove a skill entirely | name |
| write_file | Add/update supporting files | name,file_path,file_content |
| remove_file | Remove a supporting file | name,file_path |

`create`
`name`
`content`
`category`
`patch`
`name`
`old_string`
`new_string`
`edit`
`name`
`content`
`delete`
`name`
`write_file`
`name`
`file_path`
`file_content`
`remove_file`
`name`
`file_path`

Thepatchaction is preferred for updates — it's more token-efficient thaneditbecause only the changed text appears in the tool call.

`patch`
`edit`

### Gating agent skill writes (skills.write_approval)​

`skills.write_approval`

By default the agent writes skills freely — including from thebackground
self-improvement reviewthat runs after a turn. If you'd rather approve every skill write first
(small models that misjudge what they learned, secure environments, or just
wanting eyes on the self-improvement loop), turn on the write-approval gate:

[background
self-improvement review](/docs/user-guide/features/memory#controlling-memory-writes-write_approval)

```
skills:  write_approval: false     # false = write freely (default) | true = require approval
```

Whenwrite_approval: true, everyskill_managewrite (create / edit /
patch / delete / write_file / remove_file) isstagedinstead of committed —
a SKILL.md is too large to review inline, so staging applies regardless of
whether the write came from a foreground turn or the background review.
Staged writes survive restarts under~/.hermes/pending/skills/and are
reviewed with the same familiar approve/deny flow as dangerous commands:

`write_approval: true`
`skill_manage`
`~/.hermes/pending/skills/`

```
/skills pending             # list staged skill writes + a one-line gist each/skills diff <id>           # full unified diff (best viewed in CLI or dashboard)/skills approve <id>        # apply it (or 'all')/skills reject <id>         # drop it (or 'all')/skills approval on         # turn the gate on (or 'off') and persist it
```

The review surface works in the interactive CLI and on messaging platforms
(diff output is truncated for chat bubbles — read the full diff on the CLI or
in the pending JSON file). Memory writes have the same gate undermemory.write_approval— seeControlling memory writes.

`memory.write_approval`
[Controlling memory writes](/docs/user-guide/features/memory#controlling-memory-writes-write_approval)

> The separateskills.guard_agent_createdsetting is a content scanner
(dangerous-pattern heuristics), not an approval gate — the two are
independent. SeeGuard on agent-created skill writes.

The separateskills.guard_agent_createdsetting is a content scanner
(dangerous-pattern heuristics), not an approval gate — the two are
independent. SeeGuard on agent-created skill writes.

`skills.guard_agent_created`
[Guard on agent-created skill writes](/docs/user-guide/configuration#guard-on-agent-created-skill-writes)

## Skills Hub​

Browse, search, install, and manage skills from online registries,skills.sh, direct well-known skill endpoints, and official optional skills.

`skills.sh`

### Common commands​

```
hermes skills browse                              # Browse all hub skills (official first)hermes skills browse --source official            # Browse only official optional skillshermes skills search kubernetes                   # Search all sourceshermes skills search react --source skills-sh     # Search the skills.sh directoryhermes skills search https://mintlify.com/docs --source well-knownhermes skills inspect openai/skills/k8s           # Preview before installinghermes skills install openai/skills/k8s           # Install with security scanhermes skills install official/security/1passwordhermes skills install skills-sh/vercel-labs/json-render/json-render-react --forcehermes skills install well-known:https://mintlify.com/docs/.well-known/skills/mintlifyhermes skills install https://sharethis.chat/SKILL.md              # Direct URL (single-file SKILL.md)hermes skills install https://example.com/SKILL.md --name my-skill # Override name when frontmatter has nonehermes skills list --source hub                   # List hub-installed skillshermes skills check                               # Check installed hub skills for upstream updateshermes skills update                              # Reinstall hub skills with upstream changes when neededhermes skills audit                               # Re-scan all hub skills for securityhermes skills uninstall k8s                       # Remove a hub skillhermes skills reset google-workspace              # Un-stick a bundled skill from "user-modified" (see below)hermes skills reset google-workspace --restore    # Also restore the bundled version, deleting your local editshermes skills publish skills/my-skill --to github --repo owner/repohermes skills snapshot export setup.json          # Export skill confighermes skills tap add myorg/skills-repo           # Add a custom GitHub source
```

### Supported hub sources​

| Source | Example | Notes |
| --- | --- | --- |
| official | official/security/1password | Optional skills shipped with Hermes. |
| skills-sh | skills-sh/vercel-labs/agent-skills/vercel-react-best-practices | Searchable viahermes skills search <query> --source skills-sh. Hermes resolves alias-style skills when the skills.sh slug differs from the repo folder. |
| well-known | well-known:https://mintlify.com/docs/.well-known/skills/mintlify | Skills served directly from/.well-known/skills/index.jsonon a website. Search using the site or docs URL. |
| url | https://sharethis.chat/SKILL.md | Direct HTTP(S) URL to a single-fileSKILL.md. Name resolution: frontmatter → URL slug → interactive prompt →--nameflag. |
| github | openai/skills/k8s | Direct GitHub repo/path installs and custom taps. |
| clawhub,lobehub,browse-sh | Source-specific identifiers | Community or marketplace integrations. |

`official`
`official/security/1password`
`skills-sh`
`skills-sh/vercel-labs/agent-skills/vercel-react-best-practices`
`hermes skills search <query> --source skills-sh`
`well-known`
`well-known:https://mintlify.com/docs/.well-known/skills/mintlify`
`/.well-known/skills/index.json`
`url`
`https://sharethis.chat/SKILL.md`
`SKILL.md`
`--name`
`github`
`openai/skills/k8s`
`clawhub`
`lobehub`
`browse-sh`

### Integrated hubs and registries​

Hermes currently integrates with these skills ecosystems and discovery sources:

#### 1. Official optional skills (official)​

`official`

These are maintained in the Hermes repository itself and install with built-in trust.

- Catalog:Official Optional Skills Catalog
- Source in repo:optional-skills/
- Example:

[Official Optional Skills Catalog](/docs/reference/optional-skills-catalog)
`optional-skills/`

```
hermes skills browse --source officialhermes skills install official/security/1password
```

#### 2. skills.sh (skills-sh)​

`skills-sh`

This is Vercel's public skills directory. Hermes can search it directly, inspect skill detail pages, resolve alias-style slugs, and install from the underlying source repo.

- Directory:skills.sh
- CLI/tooling repo:vercel-labs/skills
- Official Vercel skills repo:vercel-labs/agent-skills
- Example:

[skills.sh](https://skills.sh/)
[vercel-labs/skills](https://github.com/vercel-labs/skills)
[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```
hermes skills search react --source skills-shhermes skills inspect skills-sh/vercel-labs/json-render/json-render-reacthermes skills install skills-sh/vercel-labs/json-render/json-render-react --force
```

#### 3. Well-known skill endpoints (well-known)​

`well-known`

This is URL-based discovery from sites that publish/.well-known/skills/index.json. It is not a single centralized hub — it is a web discovery convention.

`/.well-known/skills/index.json`
- Example live endpoint:Mintlify docs skills index
- Reference server implementation:vercel-labs/skills-handler
- Example:

[Mintlify docs skills index](https://mintlify.com/docs/.well-known/skills/index.json)
[vercel-labs/skills-handler](https://github.com/vercel-labs/skills-handler)

```
hermes skills search https://mintlify.com/docs --source well-knownhermes skills inspect well-known:https://mintlify.com/docs/.well-known/skills/mintlifyhermes skills install well-known:https://mintlify.com/docs/.well-known/skills/mintlify
```

#### 4. Direct GitHub skills (github)​

`github`

Hermes can install directly from GitHub repositories and GitHub-based taps. This is useful when you already know the repo/path or want to add your own custom source repo.

Default taps (browsable without any setup):

- openai/skills
- anthropics/skills
- huggingface/skills
- NVIDIA/skills— NVIDIA-verified skills (signedskill.oms.sig+ governanceskill-card.md)
- garrytan/gstack
- Example:

openai/skills

[openai/skills](https://github.com/openai/skills)

anthropics/skills

[anthropics/skills](https://github.com/anthropics/skills)

huggingface/skills

[huggingface/skills](https://github.com/huggingface/skills)

NVIDIA/skills— NVIDIA-verified skills (signedskill.oms.sig+ governanceskill-card.md)

[NVIDIA/skills](https://github.com/NVIDIA/skills)
`skill.oms.sig`
`skill-card.md`

garrytan/gstack

[garrytan/gstack](https://github.com/garrytan/gstack)

Example:

```
hermes skills install openai/skills/k8shermes skills tap add myorg/skills-repo
```

Category groupings (skills.sh.json).A GitHub tap may ship askills.sh.jsonfile at its repo root following theskills.sh schema. Itsgroupings(each with atitleand a list of skill names) are read at index
time and become the category labels shown in theSkills Hubpage — instead of a
tag-derived guess. This is generic: any tap that ships the file gets real
categorization, no Hermes-side changes required.

`skills.sh.json`
`skills.sh.json`
[skills.sh schema](https://skills.sh/schemas/skills.sh.schema.json)
`groupings`
`title`
[Skills Hub](https://hermes-agent.nousresearch.com/docs)

```
{  "$schema": "https://skills.sh/schemas/skills.sh.schema.json",  "groupings": [    { "title": "Inference AI", "skills": ["dynamo-recipe-runner", "dynamo-router-sla"] },    { "title": "Decision Optimization", "skills": ["cuopt-developer", "cuopt-install"] }  ]}
```

#### 5. ClawHub (clawhub)​

`clawhub`

A third-party skills marketplace integrated as a community source.

- Site:clawhub.ai
- Hermes source id:clawhub

[clawhub.ai](https://clawhub.ai/)
`clawhub`

#### 6. Claude marketplace-style repos (claude-marketplace)​

`claude-marketplace`

Hermes supports marketplace repos that publish Claude-compatible plugin/marketplace manifests.

Known integrated sources include:

- anthropics/skills
- aiskillstore/marketplace

[anthropics/skills](https://github.com/anthropics/skills)
[aiskillstore/marketplace](https://github.com/aiskillstore/marketplace)

Hermes source id:claude-marketplace

`claude-marketplace`

#### 7. LobeHub (lobehub)​

`lobehub`

Hermes can search and convert agent entries from LobeHub's public catalog into installable Hermes skills.

- Site:LobeHub
- Public agents index:chat-agents.lobehub.com
- Backing repo:lobehub/lobe-chat-agents
- Hermes source id:lobehub

[LobeHub](https://lobehub.com/)
[chat-agents.lobehub.com](https://chat-agents.lobehub.com/)
[lobehub/lobe-chat-agents](https://github.com/lobehub/lobe-chat-agents)
`lobehub`

#### 8. browse.sh (browse-sh)​

`browse-sh`

Hermes integrates withbrowse.sh, Browserbase's catalog of 200+ site-specific browser-automation SKILL.md files (Airbnb, Amazon, arXiv, 12306.cn, Etsy, Xero, and many more). Each skill describes how to drive one website end-to-end and is suitable for use with Hermes' browser tools and any browser-automation skills you already have installed.

[browse.sh](https://browse.sh)
- Site:browse.sh
- Catalog API:https://browse.sh/api/skills
- Hermes source id:browse-sh
- Trust level:community

[browse.sh](https://browse.sh/)
`https://browse.sh/api/skills`
`browse-sh`
`community`

```
hermes skills search airbnb --source browse-shhermes skills inspect browse-sh/airbnb.com/search-listings-ddgioahermes skills install browse-sh/airbnb.com/search-listings-ddgioa
```

Identifiers use the formbrowse-sh/<hostname>/<task-id>and match the slug exposed by the browse.sh catalog. Content is resolved through the per-skill detail endpoint (/api/skills/<slug>→skillMdUrl), not through the catalog's GitHubsourceUrl.

`browse-sh/<hostname>/<task-id>`
`/api/skills/<slug>`
`skillMdUrl`
`sourceUrl`

#### 9. Direct URL (url)​

`url`

Install a single-fileSKILL.mddirectly from any HTTP(S) URL — useful when an author hosts a skill on their own site (no hub listing, no GitHub path to type). Hermes fetches the URL, parses the YAML frontmatter, security-scans it, and installs.

`SKILL.md`
- Hermes source id:url
- Identifier: the URL itself (no prefix needed)
- Scope:single-fileSKILL.mdonly. Multi-file skills withreferences/orscripts/need a manifest and should be published via one of the other sources above.

`url`
`SKILL.md`
`references/`
`scripts/`

```
hermes skills install https://sharethis.chat/SKILL.mdhermes skills install https://example.com/my-skill/SKILL.md --category productivity
```

Name resolution, in order:

1. name:field in the SKILL.md YAML frontmatter (recommended — every well-formed skill has one).
2. Parent directory name from the URL path (e.g..../my-skill/SKILL.md→my-skill, or.../my-skill.md→my-skill), when it's a valid identifier (^[a-z][a-z0-9_-]*$).
3. Interactive prompt on a terminal with a TTY.
4. On non-interactive surfaces (the/skills installslash command inside the TUI, gateway platforms, scripts), a clean error pointing at the--nameoverride.

`name:`
`.../my-skill/SKILL.md`
`my-skill`
`.../my-skill.md`
`my-skill`
`^[a-z][a-z0-9_-]*$`
`/skills install`
`--name`

```
# Frontmatter has no name and the URL slug is unhelpful — supply one:hermes skills install https://example.com/SKILL.md --name sharethis-chat# Or inside a chat session:/skills install https://example.com/SKILL.md --name sharethis-chat
```

Trust level is alwayscommunity— the same security scan runs as for every other source. The URL is stored as the install identifier, sohermes skills updatere-fetches from the same URL automatically when you want to refresh.

`community`
`hermes skills update`

### Security scanning and--force​

`--force`

All hub-installed skills go through asecurity scannerthat checks for data exfiltration, prompt injection, destructive commands, supply-chain signals, and other threats.

hermes skills inspect ...now also surfaces upstream metadata when available:

`hermes skills inspect ...`
- repo URL
- skills.sh detail page URL
- install command
- weekly installs
- upstream security audit statuses
- well-known index/endpoint URLs

Use--forcewhen you have reviewed a third-party skill and want to override a non-dangerous policy block:

`--force`

```
hermes skills install skills-sh/anthropics/skills/pdf --force
```

Important behavior:

- --forcecan override policy blocks for caution/warn-style findings.
- --forcedoesnotoverride adangerousscan verdict.
- Official optional skills (official/...) are treated as built-in trust and do not show the third-party warning panel.

`--force`
`--force`
`dangerous`
`official/...`

### Trust levels​

| Level | Source | Policy |
| --- | --- | --- |
| builtin | Ships with Hermes | Always trusted |
| official | optional-skills/in the repo | Built-in trust, no third-party warning |
| trusted | Trusted registries/repos such asopenai/skills,anthropics/skills,huggingface/skills,NVIDIA/skills | More permissive policy than community sources |
| community | Everything else (skills.sh, well-known endpoints, custom GitHub repos, most marketplaces) | Non-dangerous findings can be overridden with--force;dangerousverdicts stay blocked |

`builtin`
`official`
`optional-skills/`
`trusted`
`openai/skills`
`anthropics/skills`
`huggingface/skills`
`NVIDIA/skills`
`community`
`skills.sh`
`--force`
`dangerous`

### Update lifecycle​

The hub now tracks enough provenance to re-check upstream copies of installed skills:

```
hermes skills check          # Report which installed hub skills changed upstreamhermes skills update         # Reinstall only the skills with updates availablehermes skills update react   # Update one specific installed hub skill
```

This uses the stored source identifier plus the current upstream bundle content hash to detect drift.

Skills hub operations use the GitHub API, which has a rate limit of 60 requests/hour for unauthenticated users. If you see rate-limit errors during install or search, setGITHUB_TOKENin your.envfile to increase the limit to 5,000 requests/hour. The error message includes an actionable hint when this happens.

`GITHUB_TOKEN`
`.env`

### Publishing a custom skill tap​

If you want to share a curated set of skills — for your team, your org, or publicly — you can publish them as atap: a GitHub repository other Hermes users add withhermes skills tap add <owner/repo>. No server, no registry sign-up, no release pipeline. Just a directory ofSKILL.mdfiles.

`hermes skills tap add <owner/repo>`
`SKILL.md`

#### Repo layout​

A tap is any GitHub repo (public or private — private needsGITHUB_TOKEN) laid out like this:

`GITHUB_TOKEN`

```
owner/repo├── skills/                       # default path; configurable per-tap│   ├── my-workflow/│   │   ├── SKILL.md              # required│   │   ├── references/           # optional supporting files│   │   ├── templates/│   │   └── scripts/│   ├── another-skill/│   │   └── SKILL.md│   └── third-skill/│       └── SKILL.md└── README.md                     # optional but helpful
```

Rules:

- Each skill lives in its own directory under the tap's root path (defaultskills/).
- The directory name becomes the skill's install slug.
- Each skill directory must contain aSKILL.mdwith standardSKILL.md frontmatter(name,description, plus optionalmetadata.hermes.tags,version,author,platforms,metadata.hermes.config).
- Subdirectories likereferences/,templates/,scripts/,assets/are downloaded alongsideSKILL.mdat install time.
- Skills whose directory name starts with.or_are ignored.

`skills/`
`SKILL.md`
`name`
`description`
`metadata.hermes.tags`
`version`
`author`
`platforms`
`metadata.hermes.config`
`references/`
`templates/`
`scripts/`
`assets/`
`SKILL.md`
`.`
`_`

Hermes discovers skills by listing every subdirectory of the tap path and probing each forSKILL.md.

`SKILL.md`

#### Minimal tap example​

```
my-org/hermes-skills└── skills/    └── deploy-runbook/        └── SKILL.md
```

skills/deploy-runbook/SKILL.md:

`skills/deploy-runbook/SKILL.md`

```
---name: deploy-runbookdescription: Our deployment runbook — services, rollback, Slack channelsversion: 1.0.0author: My Org Platform Teammetadata:  hermes:    tags: [deployment, runbook, internal]---# Deploy RunbookStep 1: ...
```

After pushing that to GitHub, any Hermes user can subscribe and install:

```
hermes skills tap add my-org/hermes-skillshermes skills search deployhermes skills install my-org/hermes-skills/deploy-runbook
```

#### Non-default paths​

If your skills don't live underskills/(common when you're adding askills/subtree to an existing project), edit the tap entry in~/.hermes/.hub/taps.json:

`skills/`
`skills/`
`~/.hermes/.hub/taps.json`

```
{  "taps": [    {"repo": "my-org/platform-docs", "path": "internal/skills/"}  ]}
```

Thehermes skills tap addCLI defaults new taps topath: "skills/"; edit the file directly if you need a different path.hermes skills tap listshows the effective path per tap.

`hermes skills tap add`
`path: "skills/"`
`hermes skills tap list`

#### Installing individual skills directly (without adding a tap)​

Users can also install a single skill from any public GitHub repo without adding the whole repo as a tap:

```
hermes skills install owner/repo/skills/my-workflow
```

Useful when you want to share one skill without asking the user to subscribe to your whole registry.

#### Trust levels for taps​

New taps are assignedcommunitytrust by default. Skills installed from them run through the standard security scan and show the third-party warning panel on first install. If your org or a widely-trusted source should get higher trust, add its repo toTRUSTED_REPOSintools/skills_hub.py(requires a Hermes core PR).

`community`
`TRUSTED_REPOS`
`tools/skills_hub.py`

#### Tap management​

```
hermes skills tap list                                # show all configured tapshermes skills tap add myorg/skills-repo               # add (default path: skills/)hermes skills tap remove myorg/skills-repo            # remove
```

Inside a running session:

```
/skills tap list/skills tap add myorg/skills-repo/skills tap remove myorg/skills-repo
```

Taps are stored in~/.hermes/.hub/taps.json(created on demand).

`~/.hermes/.hub/taps.json`

## Bundled skill updates (hermes skills reset)​

`hermes skills reset`

Hermes ships with a set of bundled skills inskills/inside the repo. On install and on everyhermes update, a sync pass copies those into~/.hermes/skills/and records a manifest at~/.hermes/skills/.bundled_manifestmapping each skill name to the content hash at the time it was synced (theorigin hash).

`skills/`
`hermes update`
`~/.hermes/skills/`
`~/.hermes/skills/.bundled_manifest`

On each sync, Hermes recomputes the hash of your local copy and compares it to the origin hash:

- Unchanged→ safe to pull upstream changes, copy the new bundled version in, record the new origin hash.
- Changed→ treated asuser-modifiedand skipped forever, so your edits never get stomped.

The protection is good, but it has one sharp edge. If you edit a bundled skill and then later want to abandon your changes and go back to the bundled version by just copy-pasting from~/.hermes/hermes-agent/skills/, the manifest still holds theoldorigin hash from whenever the last successful sync ran. Your fresh copy-paste contents (current bundled hash) won't match that stale origin hash, so sync keeps flagging it as user-modified.

`~/.hermes/hermes-agent/skills/`

hermes skills resetis the escape hatch:

`hermes skills reset`

```
# Safe: clears the manifest entry for this skill. Your current copy is preserved,# but the next sync re-baselines against it so future updates work normally.hermes skills reset google-workspace# Full restore: also deletes your local copy and re-copies the current bundled# version. Use this when you want the pristine upstream skill back.hermes skills reset google-workspace --restore# Non-interactive (e.g. in scripts or TUI mode) — skip the --restore confirmation.hermes skills reset google-workspace --restore --yes
```

The same command works in chat as a slash command:

```
/skills reset google-workspace/skills reset google-workspace --restore
```

Each profile has its own.bundled_manifestunder its ownHERMES_HOME, sohermes -p coder skills reset <name>only affects that profile.

`.bundled_manifest`
`HERMES_HOME`
`hermes -p coder skills reset <name>`

### Slash commands (inside chat)​

All the same commands work with/skills:

`/skills`

```
/skills browse/skills search react --source skills-sh/skills search https://mintlify.com/docs --source well-known/skills inspect skills-sh/vercel-labs/json-render/json-render-react/skills install openai/skills/skill-creator --force/skills check/skills update/skills reset google-workspace/skills list
```

Official optional skills still use identifiers likeofficial/security/1passwordandofficial/migration/openclaw-migration.

`official/security/1password`
`official/migration/openclaw-migration`
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/skills.md)