---
layout: docs
title: "مهاجرت از OpenClaw"
permalink: /docs/guides/migrate-from-openclaw/
---

- 
- Guides & Tutorials
- Migrate from OpenClaw

# Migrate from OpenClaw

hermes claw migrateimports your OpenClaw (or legacy Clawdbot/Moldbot) setup into Hermes. This guide covers exactly what gets migrated, the config key mappings, and what to verify after migration.

`hermes claw migrate`

If your OpenClaw setup was multi-provider,hermes setup --portalcollapses it to one OAuth — 300+ models plus the Tool Gateway in a single login. SeeNous Portal.

`hermes setup --portal`

## Quick start​

```
# Preview then migrate (always shows a preview first, then asks to confirm)hermes claw migrate# Preview only, no changeshermes claw migrate --dry-run# Full migration including API keys, skip confirmationhermes claw migrate --preset full --migrate-secrets --yes
```

The migration always shows a full preview of what will be imported before making any changes. Review the list, then confirm to proceed.

Reads from~/.openclaw/by default. Legacy~/.clawdbot/or~/.moltbot/directories are detected automatically. Same for legacy config filenames (clawdbot.json,moltbot.json).

`~/.openclaw/`
`~/.clawdbot/`
`~/.moltbot/`
`clawdbot.json`
`moltbot.json`

## Options​

| Option | Description |
| --- | --- |
| --dry-run | Preview only — stop after showing what would be migrated. |
| --preset <name> | full(all compatible settings) oruser-data(excludes infrastructure config). Neither preset imports secrets by default — pass--migrate-secretsexplicitly. |
| --overwrite | Overwrite existing Hermes files on conflicts (default: refuse to apply when the plan has conflicts). |
| --migrate-secrets | Include API keys. Required even under--preset full— no preset imports secrets silently. |
| --no-backup | Skip the pre-migration zip snapshot of~/.hermes/(by default a single restore-point archive is written before apply, under~/.hermes/backups/pre-migration-*.zip; restorable withhermes import). |
| --source <path> | Custom OpenClaw directory. |
| --workspace-target <path> | Where to placeAGENTS.md. |
| --skill-conflict <mode> | skip(default),overwrite, orrename. |
| --yes | Skip the confirmation prompt after preview. |

`--dry-run`
`--preset <name>`
`full`
`user-data`
`--migrate-secrets`
`--overwrite`
`--migrate-secrets`
`--preset full`
`--no-backup`
`~/.hermes/`
`~/.hermes/backups/pre-migration-*.zip`
`hermes import`
`--source <path>`
`--workspace-target <path>`
`AGENTS.md`
`--skill-conflict <mode>`
`skip`
`overwrite`
`rename`
`--yes`

## What gets migrated​

### Persona, memory, and instructions​

| What | OpenClaw source | Hermes destination | Notes |
| --- | --- | --- | --- |
| Persona | workspace/SOUL.md | ~/.hermes/SOUL.md | Direct copy |
| Workspace instructions | workspace/AGENTS.md | AGENTS.mdin--workspace-target | Requires--workspace-targetflag |
| Long-term memory | workspace/MEMORY.md | ~/.hermes/memories/MEMORY.md | Parsed into entries, merged with existing, deduped. Uses§delimiter. |
| User profile | workspace/USER.md | ~/.hermes/memories/USER.md | Same entry-merge logic as memory. |
| Daily memory files | workspace/memory/*.md | ~/.hermes/memories/MEMORY.md | All daily files merged into main memory. |

`workspace/SOUL.md`
`~/.hermes/SOUL.md`
`workspace/AGENTS.md`
`AGENTS.md`
`--workspace-target`
`--workspace-target`
`workspace/MEMORY.md`
`~/.hermes/memories/MEMORY.md`
`§`
`workspace/USER.md`
`~/.hermes/memories/USER.md`
`workspace/memory/*.md`
`~/.hermes/memories/MEMORY.md`

Workspace files are also checked atworkspace.default/andworkspace-main/as fallback paths (OpenClaw renamedworkspace/toworkspace-main/in recent versions, and usesworkspace-{agentId}for multi-agent setups).

`workspace.default/`
`workspace-main/`
`workspace/`
`workspace-main/`
`workspace-{agentId}`

### Skills (4 sources)​

| Source | OpenClaw location | Hermes destination |
| --- | --- | --- |
| Workspace skills | workspace/skills/ | ~/.hermes/skills/openclaw-imports/ |
| Managed/shared skills | ~/.openclaw/skills/ | ~/.hermes/skills/openclaw-imports/ |
| Personal cross-project | ~/.agents/skills/ | ~/.hermes/skills/openclaw-imports/ |
| Project-level shared | workspace/.agents/skills/ | ~/.hermes/skills/openclaw-imports/ |

`workspace/skills/`
`~/.hermes/skills/openclaw-imports/`
`~/.openclaw/skills/`
`~/.hermes/skills/openclaw-imports/`
`~/.agents/skills/`
`~/.hermes/skills/openclaw-imports/`
`workspace/.agents/skills/`
`~/.hermes/skills/openclaw-imports/`

Skill conflicts are handled by--skill-conflict:skipleaves the existing Hermes skill,overwritereplaces it,renamecreates a-importedcopy.

`--skill-conflict`
`skip`
`overwrite`
`rename`
`-imported`

### Model and provider configuration​

| What | OpenClaw config path | Hermes destination | Notes |
| --- | --- | --- | --- |
| Default model | agents.defaults.model | config.yaml→model | Can be a string or{primary, fallbacks}object |
| Custom providers | models.providers.* | config.yaml→custom_providers | MapsbaseUrl,apiType/api— handles both short ("openai", "anthropic") and hyphenated ("openai-completions", "anthropic-messages", "google-generative-ai") values |
| Provider API keys | models.providers.*.apiKey | ~/.hermes/.env | Requires--migrate-secrets. SeeAPI key resolutionbelow. |

`agents.defaults.model`
`config.yaml`
`model`
`{primary, fallbacks}`
`models.providers.*`
`config.yaml`
`custom_providers`
`baseUrl`
`apiType`
`api`
`models.providers.*.apiKey`
`~/.hermes/.env`
`--migrate-secrets`

### Agent behavior​

| What | OpenClaw config path | Hermes config path | Mapping |
| --- | --- | --- | --- |
| Max turns | agents.defaults.timeoutSeconds | agent.max_turns | timeoutSeconds / 10, capped at 200 |
| Verbose mode | agents.defaults.verboseDefault | agent.verbose | "off" / "on" / "full" |
| Reasoning effort | agents.defaults.thinkingDefault | agent.reasoning_effort | "always"/"high"/"xhigh" → "high", "auto"/"medium"/"adaptive" → "medium", "off"/"low"/"none"/"minimal" → "low" |
| Compression | agents.defaults.compaction.mode | compression.enabled | "off" → false, anything else → true |
| Compression model | agents.defaults.compaction.model | compression.summary_model | Direct string copy |
| Human delay | agents.defaults.humanDelay.mode | human_delay.mode | "natural" / "custom" / "off" |
| Human delay timing | agents.defaults.humanDelay.minMs/.maxMs | human_delay.min_ms/.max_ms | Direct copy |
| Timezone | agents.defaults.userTimezone | timezone | Direct string copy |
| Exec timeout | tools.exec.timeoutSec | terminal.timeout | Direct copy (field istimeoutSec, nottimeout) |
| Docker sandbox | agents.defaults.sandbox.backend | terminal.backend | "docker" → "docker" |
| Docker image | agents.defaults.sandbox.docker.image | terminal.docker_image | Direct copy |

`agents.defaults.timeoutSeconds`
`agent.max_turns`
`timeoutSeconds / 10`
`agents.defaults.verboseDefault`
`agent.verbose`
`agents.defaults.thinkingDefault`
`agent.reasoning_effort`
`agents.defaults.compaction.mode`
`compression.enabled`
`agents.defaults.compaction.model`
`compression.summary_model`
`agents.defaults.humanDelay.mode`
`human_delay.mode`
`agents.defaults.humanDelay.minMs`
`.maxMs`
`human_delay.min_ms`
`.max_ms`
`agents.defaults.userTimezone`
`timezone`
`tools.exec.timeoutSec`
`terminal.timeout`
`timeoutSec`
`timeout`
`agents.defaults.sandbox.backend`
`terminal.backend`
`agents.defaults.sandbox.docker.image`
`terminal.docker_image`

### Session reset policies​

| OpenClaw config path | Hermes config path | Notes |
| --- | --- | --- |
| session.reset.mode | session_reset.mode | "daily", "idle", or both |
| session.reset.atHour | session_reset.at_hour | Hour (0–23) for daily reset |
| session.reset.idleMinutes | session_reset.idle_minutes | Minutes of inactivity |

`session.reset.mode`
`session_reset.mode`
`session.reset.atHour`
`session_reset.at_hour`
`session.reset.idleMinutes`
`session_reset.idle_minutes`

Note: OpenClaw also hassession.resetTriggers(a simple string array like["daily", "idle"]). If the structuredsession.resetisn't present, the migration falls back to inferring fromresetTriggers.

`session.resetTriggers`
`["daily", "idle"]`
`session.reset`
`resetTriggers`

### MCP servers​

| OpenClaw field | Hermes field | Notes |
| --- | --- | --- |
| mcp.servers.*.command | mcp_servers.*.command | Stdio transport |
| mcp.servers.*.args | mcp_servers.*.args |  |
| mcp.servers.*.env | mcp_servers.*.env |  |
| mcp.servers.*.cwd | mcp_servers.*.cwd |  |
| mcp.servers.*.url | mcp_servers.*.url | HTTP/SSE transport |
| mcp.servers.*.tools.include | mcp_servers.*.tools.include | Tool filtering |
| mcp.servers.*.tools.exclude | mcp_servers.*.tools.exclude |  |

`mcp.servers.*.command`
`mcp_servers.*.command`
`mcp.servers.*.args`
`mcp_servers.*.args`
`mcp.servers.*.env`
`mcp_servers.*.env`
`mcp.servers.*.cwd`
`mcp_servers.*.cwd`
`mcp.servers.*.url`
`mcp_servers.*.url`
`mcp.servers.*.tools.include`
`mcp_servers.*.tools.include`
`mcp.servers.*.tools.exclude`
`mcp_servers.*.tools.exclude`

### TTS (text-to-speech)​

TTS settings are read fromtwoOpenClaw config locations with this priority:

1. messages.tts.providers.{provider}.*(canonical location)
2. Top-leveltalk.providers.{provider}.*(fallback)
3. Legacy flat keysmessages.tts.{provider}.*(oldest format)

`messages.tts.providers.{provider}.*`
`talk.providers.{provider}.*`
`messages.tts.{provider}.*`
| What | Hermes destination |
| --- | --- |
| Provider name | config.yaml→tts.provider |
| ElevenLabs voice ID | config.yaml→tts.elevenlabs.voice_id |
| ElevenLabs model ID | config.yaml→tts.elevenlabs.model_id |
| OpenAI model | config.yaml→tts.openai.model |
| OpenAI voice | config.yaml→tts.openai.voice |
| Edge TTS voice | config.yaml→tts.edge.voice(OpenClaw renamed "edge" to "microsoft" — both are recognized) |
| TTS assets | ~/.hermes/tts/(file copy) |

`config.yaml`
`tts.provider`
`config.yaml`
`tts.elevenlabs.voice_id`
`config.yaml`
`tts.elevenlabs.model_id`
`config.yaml`
`tts.openai.model`
`config.yaml`
`tts.openai.voice`
`config.yaml`
`tts.edge.voice`
`~/.hermes/tts/`

### Messaging platforms​

| Platform | OpenClaw config path | Hermes.envvariable | Notes |
| --- | --- | --- | --- |
| Telegram | channels.telegram.botTokenor.accounts.default.botToken | TELEGRAM_BOT_TOKEN | Token can be string orSecretRef. Both flat and accounts layout supported. |
| Telegram | credentials/telegram-default-allowFrom.json | TELEGRAM_ALLOWED_USERS | Comma-joined fromallowFrom[]array |
| Discord | channels.discord.tokenor.accounts.default.token | DISCORD_BOT_TOKEN |  |
| Discord | channels.discord.allowFromor.accounts.default.allowFrom | DISCORD_ALLOWED_USERS |  |
| Slack | channels.slack.botTokenor.accounts.default.botToken | SLACK_BOT_TOKEN |  |
| Slack | channels.slack.appTokenor.accounts.default.appToken | SLACK_APP_TOKEN |  |
| Slack | channels.slack.allowFromor.accounts.default.allowFrom | SLACK_ALLOWED_USERS |  |
| WhatsApp | channels.whatsapp.allowFromor.accounts.default.allowFrom | WHATSAPP_ALLOWED_USERS | Auth via Baileys QR pairing — requires re-pairing after migration |
| Signal | channels.signal.accountor.accounts.default.account | SIGNAL_ACCOUNT |  |
| Signal | channels.signal.httpUrlor.accounts.default.httpUrl | SIGNAL_HTTP_URL |  |
| Signal | channels.signal.allowFromor.accounts.default.allowFrom | SIGNAL_ALLOWED_USERS |  |
| Matrix | channels.matrix.accessTokenor.accounts.default.accessToken | MATRIX_ACCESS_TOKEN | UsesaccessToken(notbotToken) |
| Mattermost | channels.mattermost.botTokenor.accounts.default.botToken | MATTERMOST_BOT_TOKEN |  |

`.env`
`channels.telegram.botToken`
`.accounts.default.botToken`
`TELEGRAM_BOT_TOKEN`
`credentials/telegram-default-allowFrom.json`
`TELEGRAM_ALLOWED_USERS`
`allowFrom[]`
`channels.discord.token`
`.accounts.default.token`
`DISCORD_BOT_TOKEN`
`channels.discord.allowFrom`
`.accounts.default.allowFrom`
`DISCORD_ALLOWED_USERS`
`channels.slack.botToken`
`.accounts.default.botToken`
`SLACK_BOT_TOKEN`
`channels.slack.appToken`
`.accounts.default.appToken`
`SLACK_APP_TOKEN`
`channels.slack.allowFrom`
`.accounts.default.allowFrom`
`SLACK_ALLOWED_USERS`
`channels.whatsapp.allowFrom`
`.accounts.default.allowFrom`
`WHATSAPP_ALLOWED_USERS`
`channels.signal.account`
`.accounts.default.account`
`SIGNAL_ACCOUNT`
`channels.signal.httpUrl`
`.accounts.default.httpUrl`
`SIGNAL_HTTP_URL`
`channels.signal.allowFrom`
`.accounts.default.allowFrom`
`SIGNAL_ALLOWED_USERS`
`channels.matrix.accessToken`
`.accounts.default.accessToken`
`MATRIX_ACCESS_TOKEN`
`accessToken`
`botToken`
`channels.mattermost.botToken`
`.accounts.default.botToken`
`MATTERMOST_BOT_TOKEN`

### Other config​

| What | OpenClaw path | Hermes path | Notes |
| --- | --- | --- | --- |
| Approval mode | approvals.exec.mode | config.yaml→approvals.mode | "auto"→"off", "always"→"manual", "smart"→"smart" |
| Command allowlist | exec-approvals.json | config.yaml→command_allowlist | Patterns merged and deduped |
| Browser CDP URL | browser.cdpUrl | config.yaml→browser.cdp_url |  |
| Browser headless | browser.headless | config.yaml→browser.headless |  |
| Brave search key | tools.web.search.brave.apiKey | .env→BRAVE_API_KEY | Requires--migrate-secrets |
| Gateway auth token | gateway.auth.token | .env→HERMES_GATEWAY_TOKEN | Requires--migrate-secrets |
| Working directory | agents.defaults.workspace | config.yaml→terminal.cwd | Legacy migrations may still emitMESSAGING_CWDas a compatibility fallback |

`approvals.exec.mode`
`config.yaml`
`approvals.mode`
`exec-approvals.json`
`config.yaml`
`command_allowlist`
`browser.cdpUrl`
`config.yaml`
`browser.cdp_url`
`browser.headless`
`config.yaml`
`browser.headless`
`tools.web.search.brave.apiKey`
`.env`
`BRAVE_API_KEY`
`--migrate-secrets`
`gateway.auth.token`
`.env`
`HERMES_GATEWAY_TOKEN`
`--migrate-secrets`
`agents.defaults.workspace`
`config.yaml`
`terminal.cwd`
`MESSAGING_CWD`

### Archived (no direct Hermes equivalent)​

These are saved to~/.hermes/migration/openclaw/<timestamp>/archive/for manual review:

`~/.hermes/migration/openclaw/<timestamp>/archive/`
| What | Archive file | How to recreate in Hermes |
| --- | --- | --- |
| IDENTITY.md | archive/workspace/IDENTITY.md | Merge intoSOUL.md |
| TOOLS.md | archive/workspace/TOOLS.md | Hermes has built-in tool instructions |
| HEARTBEAT.md | archive/workspace/HEARTBEAT.md | Use cron jobs for periodic tasks |
| BOOTSTRAP.md | archive/workspace/BOOTSTRAP.md | Use context files or skills |
| Cron jobs | archive/cron-config.json | Recreate withhermes cron create |
| Plugins | archive/plugins-config.json | Seeplugins guide |
| Hooks/webhooks | archive/hooks-config.json | Usehermes webhookor gateway hooks |
| Memory backend | archive/memory-backend-config.json | Configure viahermes honcho |
| Skills registry | archive/skills-registry-config.json | Usehermes skills config |
| UI/identity | archive/ui-identity-config.json | Use/skincommand |
| Logging | archive/logging-diagnostics-config.json | Set inconfig.yamllogging section |
| Multi-agent list | archive/agents-list.json | Use Hermes profiles |
| Channel bindings | archive/bindings.json | Manual setup per platform |
| Complex channels | archive/channels-deep-config.json | Manual platform config |

`IDENTITY.md`
`archive/workspace/IDENTITY.md`
`SOUL.md`
`TOOLS.md`
`archive/workspace/TOOLS.md`
`HEARTBEAT.md`
`archive/workspace/HEARTBEAT.md`
`BOOTSTRAP.md`
`archive/workspace/BOOTSTRAP.md`
`archive/cron-config.json`
`hermes cron create`
`archive/plugins-config.json`
`archive/hooks-config.json`
`hermes webhook`
`archive/memory-backend-config.json`
`hermes honcho`
`archive/skills-registry-config.json`
`hermes skills config`
`archive/ui-identity-config.json`
`/skin`
`archive/logging-diagnostics-config.json`
`config.yaml`
`archive/agents-list.json`
`archive/bindings.json`
`archive/channels-deep-config.json`

## API key resolution​

When--migrate-secretsis enabled, API keys are collected fromfour sourcesin priority order:

`--migrate-secrets`
1. Config values—models.providers.*.apiKeyand TTS provider keys inopenclaw.json
2. Environment file—~/.openclaw/.env(keys likeOPENROUTER_API_KEY,ANTHROPIC_API_KEY, etc.)
3. Config env sub-object—openclaw.json→"env"or"env"."vars"(some setups store keys here instead of a separate.envfile)
4. Auth profiles—~/.openclaw/agents/main/agent/auth-profiles.json(per-agent credentials)

`models.providers.*.apiKey`
`openclaw.json`
`~/.openclaw/.env`
`OPENROUTER_API_KEY`
`ANTHROPIC_API_KEY`
`openclaw.json`
`"env"`
`"env"."vars"`
`.env`
`~/.openclaw/agents/main/agent/auth-profiles.json`

Config values take priority. Each subsequent source fills any remaining gaps.

### Supported key targets​

OPENROUTER_API_KEY,OPENAI_API_KEY,ANTHROPIC_API_KEY,DEEPSEEK_API_KEY,GEMINI_API_KEY,ZAI_API_KEY,MINIMAX_API_KEY,ELEVENLABS_API_KEY,TELEGRAM_BOT_TOKEN,VOICE_TOOLS_OPENAI_KEY

`OPENROUTER_API_KEY`
`OPENAI_API_KEY`
`ANTHROPIC_API_KEY`
`DEEPSEEK_API_KEY`
`GEMINI_API_KEY`
`ZAI_API_KEY`
`MINIMAX_API_KEY`
`ELEVENLABS_API_KEY`
`TELEGRAM_BOT_TOKEN`
`VOICE_TOOLS_OPENAI_KEY`

Keys not in this allowlist are never copied.

## SecretRef handling​

OpenClaw config values for tokens and API keys can be in three formats:

```
// Plain string"channels": { "telegram": { "botToken": "123456:ABC-DEF..." } }// Environment template"channels": { "telegram": { "botToken": "${TELEGRAM_BOT_TOKEN}" } }// SecretRef object"channels": { "telegram": { "botToken": { "source": "env", "id": "TELEGRAM_BOT_TOKEN" } } }
```

The migration resolves all three formats. For env templates and SecretRef objects withsource: "env", it looks up the value in~/.openclaw/.envand theopenclaw.jsonenv sub-object. SecretRef objects withsource: "file"orsource: "exec"can't be resolved automatically — the migration warns about these, and those values must be added to Hermes manually viahermes config set.

`source: "env"`
`~/.openclaw/.env`
`openclaw.json`
`source: "file"`
`source: "exec"`
`hermes config set`

## After migration​

1. Check the migration report— printed on completion with counts of migrated, skipped, and conflicting items.
2. Review archived files— anything in~/.hermes/migration/openclaw/<timestamp>/archive/needs manual attention.
3. Start a new session— imported skills and memory entries take effect in new sessions, not the current one.
4. Verify API keys— runhermes statusto check provider authentication.
5. Test messaging— if you migrated platform tokens, restart the gateway:systemctl --user restart hermes-gateway
6. Check session policies— runhermes config showand verify thesession_resetvalue matches your expectations.
7. Re-pair WhatsApp— WhatsApp uses QR code pairing (Baileys), not token migration. Runhermes whatsappto pair.
8. Archive cleanup— after confirming everything works, runhermes claw cleanupto rename leftover OpenClaw directories to.pre-migration/(prevents state confusion).

Check the migration report— printed on completion with counts of migrated, skipped, and conflicting items.

Review archived files— anything in~/.hermes/migration/openclaw/<timestamp>/archive/needs manual attention.

`~/.hermes/migration/openclaw/<timestamp>/archive/`

Start a new session— imported skills and memory entries take effect in new sessions, not the current one.

Verify API keys— runhermes statusto check provider authentication.

`hermes status`

Test messaging— if you migrated platform tokens, restart the gateway:systemctl --user restart hermes-gateway

`systemctl --user restart hermes-gateway`

Check session policies— runhermes config showand verify thesession_resetvalue matches your expectations.

`hermes config show`
`session_reset`

Re-pair WhatsApp— WhatsApp uses QR code pairing (Baileys), not token migration. Runhermes whatsappto pair.

`hermes whatsapp`

Archive cleanup— after confirming everything works, runhermes claw cleanupto rename leftover OpenClaw directories to.pre-migration/(prevents state confusion).

`hermes claw cleanup`
`.pre-migration/`

## Troubleshooting​

### "OpenClaw directory not found"​

The migration checks~/.openclaw/, then~/.clawdbot/, then~/.moltbot/. If your installation is elsewhere, use--source /path/to/your/openclaw.

`~/.openclaw/`
`~/.clawdbot/`
`~/.moltbot/`
`--source /path/to/your/openclaw`

### "No provider API keys found"​

Keys might be stored in several places depending on your OpenClaw version: inline inopenclaw.jsonundermodels.providers.*.apiKey, in~/.openclaw/.env, in theopenclaw.json"env"sub-object, or inagents/main/agent/auth-profiles.json. The migration checks all four. If keys usesource: "file"orsource: "exec"SecretRefs, they can't be resolved automatically — add them viahermes config set.

`openclaw.json`
`models.providers.*.apiKey`
`~/.openclaw/.env`
`openclaw.json`
`"env"`
`agents/main/agent/auth-profiles.json`
`source: "file"`
`source: "exec"`
`hermes config set`

### Skills not appearing after migration​

Imported skills land in~/.hermes/skills/openclaw-imports/. Start a new session for them to take effect, or run/skillsto verify they're loaded.

`~/.hermes/skills/openclaw-imports/`
`/skills`

### TTS voice not migrated​

OpenClaw stores TTS settings in two places:messages.tts.providers.*and the top-leveltalkconfig. The migration checks both. If your voice ID was set via the OpenClaw UI (stored in a different path), you may need to set it manually:hermes config set tts.elevenlabs.voice_id YOUR_VOICE_ID.

`messages.tts.providers.*`
`talk`
`hermes config set tts.elevenlabs.voice_id YOUR_VOICE_ID`