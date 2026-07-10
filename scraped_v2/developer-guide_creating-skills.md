- 
- Developer Guide
- Extending
- Creating Skills

# Creating Skills

Skills are the preferred way to add new capabilities to Hermes Agent. They're easier to create than tools, require no code changes to the agent, and can be shared with the community.

## Should it be a Skill or a Tool?​

Make it aSkillwhen:

- The capability can be expressed as instructions + shell commands + existing tools
- It wraps an external CLI or API that the agent can call viaterminalorweb_extract
- It doesn't need custom Python integration or API key management baked into the agent
- Examples: arXiv search, git workflows, Docker management, PDF processing, email via CLI tools

`terminal`
`web_extract`

Make it aToolwhen:

- It requires end-to-end integration with API keys, auth flows, or multi-component configuration
- It needs custom processing logic that must execute precisely every time
- It handles binary data, streaming, or real-time events
- Examples: browser automation, TTS, vision analysis

## Skill Directory Structure​

Bundled skills live inskills/organized by category. Official optional skills use the same structure inoptional-skills/:

`skills/`
`optional-skills/`

```
skills/├── research/│   └── arxiv/│       ├── SKILL.md              # Required: main instructions│       └── scripts/              # Optional: helper scripts│           └── search_arxiv.py├── productivity/│   └── ocr-and-documents/│       ├── SKILL.md│       ├── scripts/│       └── references/└── ...
```

## SKILL.md Format​

```
---name: my-skilldescription: Brief description (shown in skill search results)version: 1.0.0author: Your Namelicense: MITplatforms: [macos, linux]          # Optional — restrict to specific OS platforms                                   #   Valid: macos, linux, windows                                   #   Omit to load on all platforms (default)metadata:  hermes:    tags: [Category, Subcategory, Keywords]    related_skills: [other-skill-name]    requires_toolsets: [web]            # Optional — only show when these toolsets are active    requires_tools: [web_search]        # Optional — only show when these tools are available    fallback_for_toolsets: [browser]    # Optional — hide when these toolsets are active    fallback_for_tools: [browser_navigate]  # Optional — hide when these tools exist    config:                              # Optional — config.yaml settings the skill needs      - key: my.setting        description: "What this setting controls"        default: "sensible-default"        prompt: "Display prompt for setup"    blueprint:                              # Optional — marks this skill a runnable automation      schedule: "0 9 * * *"              #   cron expr / "every 2h" / ISO timestamp      deliver: origin                    #   optional (default origin)      prompt: "Task instruction for each run"  # optional      no_agent: false                    # optionalrequired_environment_variables:          # Optional — env vars the skill needs  - name: MY_API_KEY    prompt: "Enter your API key"    help: "Get one at https://example.com"    required_for: "API access"---# Skill TitleBrief intro.## When to UseTrigger conditions — when should the agent load this skill?## Quick ReferenceTable of common commands or API calls.## ProcedureStep-by-step instructions the agent follows.## PitfallsKnown failure modes and how to handle them.## VerificationHow the agent confirms it worked.
```

### Platform-Specific Skills​

Skills can restrict themselves to specific operating systems using theplatformsfield:

`platforms`

```
platforms: [macos]            # macOS only (e.g., iMessage, Apple Reminders)platforms: [macos, linux]     # macOS and Linuxplatforms: [windows]          # Windows only
```

When set, the skill is automatically hidden from the system prompt,skills_list(), and slash commands on incompatible platforms. If omitted or empty, the skill loads on all platforms (backward compatible).

`skills_list()`

### Conditional Skill Activation​

Skills can declare dependencies on specific tools or toolsets. This controls whether the skill appears in the system prompt for a given session.

```
metadata:  hermes:    requires_toolsets: [web]           # Hide if the web toolset is NOT active    requires_tools: [web_search]       # Hide if web_search tool is NOT available    fallback_for_toolsets: [browser]   # Hide if the browser toolset IS active    fallback_for_tools: [browser_navigate]  # Hide if browser_navigate IS available
```

| Field | Behavior |
| --- | --- |
| requires_toolsets | Skill ishiddenwhen ANY listed toolset isnotavailable |
| requires_tools | Skill ishiddenwhen ANY listed tool isnotavailable |
| fallback_for_toolsets | Skill ishiddenwhen ANY listed toolsetisavailable |
| fallback_for_tools | Skill ishiddenwhen ANY listed toolisavailable |

`requires_toolsets`
`requires_tools`
`fallback_for_toolsets`
`fallback_for_tools`

Use case forfallback_for_*:Create a skill that serves as a workaround when a primary tool isn't available. For example, aduckduckgo-searchskill withfallback_for_tools: [web_search]only shows when the web search tool (which requires an API key) is not configured.

`fallback_for_*`
`duckduckgo-search`
`fallback_for_tools: [web_search]`

Use case forrequires_*:Create a skill that only makes sense when certain tools are present. For example, a web scraping workflow skill withrequires_toolsets: [web]won't clutter the prompt when web tools are disabled.

`requires_*`
`requires_toolsets: [web]`

### Environment Variable Requirements​

Skills can declare environment variables they need. When a skill is loaded viaskill_view, its required vars are automatically registered for passthrough into sandboxed execution environments (terminal, execute_code).

`skill_view`

```
required_environment_variables:  - name: TENOR_API_KEY    prompt: "Tenor API key"               # Shown when prompting user    help: "Get your key at https://tenor.com"  # Help text or URL    required_for: "GIF search functionality"   # What needs this var
```

Each entry supports:

- name(required) — the environment variable name
- prompt(optional) — prompt text when asking the user for the value
- help(optional) — help text or URL for obtaining the value
- required_for(optional) — describes which feature needs this variable

`name`
`prompt`
`help`
`required_for`

Users can also manually configure passthrough variables inconfig.yaml:

`config.yaml`

```
terminal:  env_passthrough:    - MY_CUSTOM_VAR    - ANOTHER_VAR
```

Seeskills/apple/for examples of macOS-only skills.

`skills/apple/`

## Secure Setup on Load​

Userequired_environment_variableswhen a skill needs an API key or token. Missing values donothide the skill from discovery. Instead, Hermes prompts for them securely when the skill is loaded in the local CLI.

`required_environment_variables`

```
required_environment_variables:  - name: TENOR_API_KEY    prompt: Tenor API key    help: Get a key from https://developers.google.com/tenor    required_for: full functionality
```

The user can skip setup and keep loading the skill. Hermes never exposes the raw secret value to the model. Gateway and messaging sessions show local setup guidance instead of collecting secrets in-band.

When your skill is loaded, any declaredrequired_environment_variablesthat are set areautomatically passed throughtoexecute_codeandterminalsandboxes — including remote backends like Docker and Modal. Your skill's scripts can access$TENOR_API_KEY(oros.environ["TENOR_API_KEY"]in Python) without the user needing to configure anything extra. SeeEnvironment Variable Passthroughfor details.

`required_environment_variables`
`execute_code`
`terminal`
`$TENOR_API_KEY`
`os.environ["TENOR_API_KEY"]`

Legacyprerequisites.env_varsremains supported as a backward-compatible alias.

`prerequisites.env_vars`

### Config Settings (config.yaml)​

Skills can declare non-secret settings that are stored inconfig.yamlunder theskills.confignamespace. Unlike environment variables (which are secrets stored in.env), config settings are for paths, preferences, and other non-sensitive values.

`config.yaml`
`skills.config`
`.env`

```
metadata:  hermes:    config:      - key: myplugin.path        description: Path to the plugin data directory        default: "~/myplugin-data"        prompt: Plugin data directory path      - key: myplugin.domain        description: Domain the plugin operates on        default: ""        prompt: Plugin domain (e.g., AI/ML research)
```

Each entry supports:

- key(required) — dotpath for the setting (e.g.,myplugin.path)
- description(required) — explains what the setting controls
- default(optional) — default value if the user doesn't configure it
- prompt(optional) — prompt text shown duringhermes config migrate; falls back todescription

`key`
`myplugin.path`
`description`
`default`
`prompt`
`hermes config migrate`
`description`

How it works:

1. Storage:Values are written toconfig.yamlunderskills.config.<key>:skills:config:myplugin:path:~/my-data
2. Discovery:hermes config migratescans all enabled skills, finds unconfigured settings, and prompts the user. Settings also appear inhermes config showunder "Skill Settings."
3. Runtime injection:When a skill loads, its config values are resolved and appended to the skill message:[Skill config (from ~/.hermes/config.yaml):myplugin.path = /home/user/my-data]The agent sees the configured values without needing to readconfig.yamlitself.
4. Manual setup:Users can also set values directly:hermes configsetskills.config.myplugin.path ~/my-data

Storage:Values are written toconfig.yamlunderskills.config.<key>:

`config.yaml`
`skills.config.<key>`

```
skills:  config:    myplugin:      path: ~/my-data
```

Discovery:hermes config migratescans all enabled skills, finds unconfigured settings, and prompts the user. Settings also appear inhermes config showunder "Skill Settings."

`hermes config migrate`
`hermes config show`

Runtime injection:When a skill loads, its config values are resolved and appended to the skill message:

```
[Skill config (from ~/.hermes/config.yaml):  myplugin.path = /home/user/my-data]
```

The agent sees the configured values without needing to readconfig.yamlitself.

`config.yaml`

Manual setup:Users can also set values directly:

```
hermes config set skills.config.myplugin.path ~/my-data
```

Userequired_environment_variablesfor API keys, tokens, and othersecrets(stored in~/.hermes/.env, never shown to the model). Useconfigforpaths, preferences, and non-sensitive settings(stored inconfig.yaml, visible in config show).

`required_environment_variables`
`~/.hermes/.env`
`config`
`config.yaml`

### Credential File Requirements (OAuth tokens, etc.)​

Skills that use OAuth or file-based credentials can declare files that need to be mounted into remote sandboxes. This is for credentials stored asfiles(not env vars) — typically OAuth token files produced by a setup script.

```
required_credential_files:  - path: google_token.json    description: Google OAuth2 token (created by setup script)  - path: google_client_secret.json    description: Google OAuth2 client credentials
```

Each entry supports:

- path(required) — file path relative to~/.hermes/
- description(optional) — explains what the file is and how it's created

`path`
`~/.hermes/`
`description`

When loaded, Hermes checks if these files exist. Missing files triggersetup_needed. Existing files are automatically:

`setup_needed`
- Mounted into Dockercontainers as read-only bind mounts
- Synced into Modalsandboxes (at creation + before each command, so mid-session OAuth works)
- Available onlocalbackend without any special handling

Userequired_environment_variablesfor simple API keys and tokens (strings stored in~/.hermes/.env). Userequired_credential_filesfor OAuth token files, client secrets, service account JSON, certificates, or any credential that's a file on disk.

`required_environment_variables`
`~/.hermes/.env`
`required_credential_files`

See theskills/productivity/google-workspace/SKILL.mdfor a complete example using both.

`skills/productivity/google-workspace/SKILL.md`

## Skill Guidelines​

### No External Dependencies​

Prefer stdlib Python, curl, and existing Hermes tools (web_extract,terminal,read_file). If a dependency is needed, document installation steps in the skill.

`web_extract`
`terminal`
`read_file`

### Progressive Disclosure​

Put the most common workflow first. Edge cases and advanced usage go at the bottom. This keeps token usage low for common tasks.

### Include Helper Scripts​

For XML/JSON parsing or complex logic, include helper scripts inscripts/— don't expect the LLM to write parsers inline every time.

`scripts/`

### Deliver media as documents ([[as_document]])​

`[[as_document]]`

If your skill produces a high-resolution screenshot, chart, or any image where lossy preview compression would hurt — emit the literal directive[[as_document]]somewhere in the response (commonly the last line). The gateway strips the directive and delivers every extracted media path in that response as a downloadable file attachment instead of an inline image bubble. SeeSkill output and media deliveryfor the full semantics.

`[[as_document]]`

#### Referencing bundled scripts from SKILL.md​

When a skill is loaded, the activation message exposes the absolute skill directory as[Skill directory: /abs/path]and also substitutes two template tokens anywhere in the SKILL.md body:

`[Skill directory: /abs/path]`
| Token | Replaced with |
| --- | --- |
| ${HERMES_SKILL_DIR} | Absolute path to the skill's directory |
| ${HERMES_SESSION_ID} | The active session id (left in place if there is no session) |

`${HERMES_SKILL_DIR}`
`${HERMES_SESSION_ID}`

So a SKILL.md can tell the agent to run a bundled script directly with:

```
To analyse the input, run:    node ${HERMES_SKILL_DIR}/scripts/analyse.js <input>
```

The agent sees the substituted absolute path and invokes theterminaltool with a ready-to-run command — no path math, no extraskill_viewround-trip. Disable substitution globally withskills.template_vars: falseinconfig.yaml.

`terminal`
`skill_view`
`skills.template_vars: false`
`config.yaml`

#### Inline shell snippets (opt-in)​

Skills can also embed inline shell snippets written as!`cmd`in the SKILL.md body. When enabled, each snippet's stdout is inlined into the message before the agent reads it, so skills can inject dynamic context:

`!`cmd``

```
Current date: !`date -u +%Y-%m-%d`Git branch: !`git -C ${HERMES_SKILL_DIR} rev-parse --abbrev-ref HEAD`
```

This isoff by default— any snippet in a SKILL.md runs on the host without approval, so only enable it for skill sources you trust:

```
# config.yamlskills:  inline_shell: true  inline_shell_timeout: 10   # seconds per snippet
```

Snippets run with the skill directory as their working directory, and output is capped at 4000 characters. Failures (timeouts, non-zero exits) show up as a short[inline-shell error: ...]marker instead of breaking the whole skill.

`[inline-shell error: ...]`

### Test It​

Run the skill and verify the agent follows the instructions correctly:

```
hermes chat --toolsets skills -q "Use the X skill to do Y"
```

## Where Should the Skill Live?​

Bundled skills (inskills/) ship with every Hermes install. They should bebroadly useful to most users:

`skills/`
- Document handling, web research, common dev workflows, system administration
- Used regularly by a wide range of people

If your skill is official and useful but not universally needed (e.g., a paid service integration, a heavyweight dependency), put it inoptional-skills/— it ships with the repo, is discoverable viahermes skills browse(labeled "official"), and installs with built-in trust.

`optional-skills/`
`hermes skills browse`

If your skill is specialized, community-contributed, or niche, it's better suited for aSkills Hub— upload it to a registry and share it viahermes skills install.

`hermes skills install`

## Blueprints: skills that are also automations​

Ablueprintis an ordinary skill that additionally declares a schedule in its frontmatter. Add ametadata.hermes.blueprintblock and the skill becomes a shareable, runnable automation:

`metadata.hermes.blueprint`

```
metadata:  hermes:    tags: [blueprint, email]    blueprint:      schedule: "0 8 * * *"     # presence of `blueprint:` marks it runnable      deliver: telegram          # optional (default: origin)      prompt: "Summarize my unread email and today's calendar."  # optional      no_agent: false            # optional
```

Because a blueprintisa skill, it flows through the entire skills pipeline unchanged — search, inspect, install, security scan, provenance, taps, the centralized index, andhermes skills publishfor sharing. Nothing new to learn.

`hermes skills publish`

Installing a blueprint.When you install a skill that carries ablueprint:block, Hermes registers it as asuggested cron jobrather than scheduling it. Scheduling isopt-in— installing never silently creates a recurring job. You review and accept it via/suggestions:

`blueprint:`
`/suggestions`

```
hermes skills install owner/morning-brief# → Blueprint: 'morning-brief' is an automation (schedule 0 8 * * *).#   Added to your suggestions — run /suggestions to schedule or dismiss it.# then, in a session:/suggestions             # lists pending suggestions, numbered/suggestions accept 1    # creates the cron job/suggestions dismiss 1   # never offer it again
```

Blueprints are onesourceof the unified Suggested Cron Jobs surface — the same place curated starter automations and (later) usage-pattern and integration suggestions appear. SeeSuggested Cron Jobsbelow.

Sharing an automation you built.A blueprint loaded by a cron job (hermes cron create --skill <name> ...) can be exported back to a SKILL.md and published like any other skill, so an automation you tuned for yourself becomes a one-command install for someone else.

`hermes cron create --skill <name> ...`

The blueprint layer adds no new object type, store, or transport — the blueprint is a skill, the schedule is a cron job, and sharing is the existing publish/tap/index path.

## Suggested Cron Jobs​

Hermes canproposeautomations and let you accept them with one tap, instead of making you assemble cron jobs by hand. Every proposal flows through one surface — the/suggestionscommand — regardless of where it came from:

`/suggestions`
| Source | Trigger |
| --- | --- |
| catalog | Curated starter automations (/suggestions catalog) — daily briefing, important-mail monitor, weekly review, workday-start reminder |
| blueprint | You installed a skill carrying ablueprint:block |
| usage | The background review noticed a recurring ask a schedule would serve |
| integration | You connected an account (Gmail, GitHub, ...) and the obvious automations are offered |

`catalog`
`/suggestions catalog`
`blueprint`
`blueprint:`
`usage`
`integration`

```
/suggestions             # list pending/suggestions accept N    # schedule suggestion N (creates the cron job)/suggestions dismiss N   # dismiss it — latched, never re-offered/suggestions catalog     # add the curated starter automations
```

Accepting a suggestion calls the samecron.jobs.create_jobthecronjobtool uses — there is no second job engine. Suggestionsneverauto-create jobs; acceptance is always explicit. Dismissed suggestions latch by a stable key so the same proposal is never re-offered. The pending list is capped so it never becomes a nag wall.

`cron.jobs.create_job`
`cronjob`

Theimportant-mail monitorcatalog entry is the poll→classify→surface pattern: it scores inbox items with a cheap classifier model (auxiliary.monitorinconfig.yaml) and delivers only the ones above an urgency threshold, staying silent otherwise.

`auxiliary.monitor`
`config.yaml`

## Publishing Skills​

### To the Skills Hub​

```
hermes skills publish skills/my-skill --to github --repo owner/repo
```

### To a Custom Repository​

Add your repo as a tap:

```
hermes skills tap add owner/repo
```

Users can then search and install from your repository.

## Security Scanning​

All hub-installed skills go through a security scanner that checks for:

- Data exfiltration patterns
- Prompt injection attempts
- Destructive commands
- Shell injection

Trust levels:

- builtin— ships with Hermes (always trusted)
- official— fromoptional-skills/in the repo (built-in trust, no third-party warning)
- trusted— from openai/skills, anthropics/skills, huggingface/skills
- community— non-dangerous findings can be overridden with--force;dangerousverdicts remain blocked

`builtin`
`official`
`optional-skills/`
`trusted`
`community`
`--force`
`dangerous`

Hermes can now consume third-party skills from multiple external discovery models:

- direct GitHub identifiers (for exampleopenai/skills/k8s)
- skills.shidentifiers (for exampleskills-sh/vercel-labs/json-render/json-render-react)
- well-known endpoints served from/.well-known/skills/index.json

`openai/skills/k8s`
`skills.sh`
`skills-sh/vercel-labs/json-render/json-render-react`
`/.well-known/skills/index.json`

If you want your skills to be discoverable without a GitHub-specific installer, consider serving them from a well-known endpoint in addition to publishing them in a repo or marketplace.