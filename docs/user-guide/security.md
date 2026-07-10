---
layout: docs
title: "امنیت"
permalink: /user-guide/security/
---

- 
- Using Hermes
- Security

# Security

Hermes Agent is designed with a defense-in-depth security model. This page covers every security boundary — from command approval to container isolation to user authorization on messaging platforms.

## Overview​

The security model has seven layers:

1. User authorization— who can talk to the agent (allowlists, DM pairing)
2. Dangerous command approval— human-in-the-loop for destructive operations
3. Container isolation— Docker/Singularity/Modal sandboxing with hardened settings
4. MCP credential filtering— environment variable isolation for MCP subprocesses
5. Context file scanning— prompt injection detection in project files
6. Cross-session isolation— sessions cannot access each other's data or state; cron job storage paths are hardened against path traversal attacks
7. Input sanitization— working directory parameters in terminal tool backends are validated against an allowlist to prevent shell injection

## Dangerous Command Approval​

Before executing any command, Hermes checks it against a curated list of dangerous patterns. If a match is found, the user must explicitly approve it.

### Approval Modes​

The approval system supports three modes, configured viaapprovals.modein~/.hermes/config.yaml:

`approvals.mode`
`~/.hermes/config.yaml`

```
approvals:  mode: manual                    # manual | smart | off  timeout: 60                     # seconds to wait for user response (default: 60)  cron_mode: deny                 # deny | approve — what cron jobs do when they hit a dangerous command  mcp_reload_confirm: true        # /reload-mcp asks before invalidating the MCP tool cache  destructive_slash_confirm: true # /clear, /new, /reset, /undo prompt before discarding state
```

The full set of keys:

| Key | Default | What it controls |
| --- | --- | --- |
| mode | manual | Approval policy for dangerous shell commands — see the table below. |
| timeout | 60 | Seconds Hermes waits for an approval reply before timing out. |
| cron_mode | deny | Howcron jobsbehave headlessly when they trigger a dangerous-command prompt.denyblocks the command (the agent must find another path);approveauto-approves everything in cron context. |
| mcp_reload_confirm | true | When true,/reload-mcpasks before rebuilding the MCP tool set. Rebuilding invalidates the provider prompt cache (tool schemas live in the system prompt), so the next message re-sends full input tokens. Users who clickAlways Approveflip this key tofalse. |
| destructive_slash_confirm | true | When true, destructive session slash commands (/clear,/new,/reset,/undo) prompt before discarding conversation state. Three-option dialog (Approve Once / Always Approve / Cancel) routed through native yes/no buttons on Telegram, Discord, and Slack; text fallback elsewhere. Users who clickAlways Approveflip this key tofalse. TUI uses its own modal overlay (setHERMES_TUI_NO_CONFIRM=1to opt out there). |

`mode`
`manual`
`timeout`
`60`
`cron_mode`
`deny`
[cron jobs](/docs/user-guide/features/cron)
`deny`
`approve`
`mcp_reload_confirm`
`true`
`/reload-mcp`
`false`
`destructive_slash_confirm`
`true`
`/clear`
`/new`
`/reset`
`/undo`
`false`
`HERMES_TUI_NO_CONFIRM=1`

| Mode | Behavior |
| --- | --- |
| manual(default) | Always prompt the user for approval on dangerous commands |
| smart | Use an auxiliary LLM to assess risk. Low-risk commands (e.g.,python -c "print('hello')") are auto-approved. Genuinely dangerous commands are auto-denied. Uncertain cases escalate to a manual prompt. |
| off | Disable all approval checks — equivalent to running with--yolo. All commands execute without prompts. |

`python -c "print('hello')"`
`--yolo`

Settingapprovals.mode: offdisables all safety prompts. Use only in trusted environments (CI/CD, containers, etc.).

`approvals.mode: off`

### YOLO Mode​

YOLO mode bypassesalldangerous command approval prompts for the current session. It can be activated three ways:

1. CLI flag: Start a session withhermes --yoloorhermes chat --yolo
2. Slash command: Type/yoloduring a session to toggle it on/off
3. Environment variable: SetHERMES_YOLO_MODE=1

`hermes --yolo`
`hermes chat --yolo`
`/yolo`
`HERMES_YOLO_MODE=1`

The/yolocommand is atoggle— each use flips the mode on or off:

`/yolo`

```
> /yolo  ⚡ YOLO mode ON — all commands auto-approved. Use with caution.> /yolo  ⚠ YOLO mode OFF — dangerous commands will require approval.
```

YOLO mode is available in both CLI and gateway sessions. Internally, it sets theHERMES_YOLO_MODEenvironment variable which is checked before every command execution.

`HERMES_YOLO_MODE`

When YOLO is active, Hermes shows two persistent visual reminders so it's hard to forget that approval prompts are bypassed:

- A red banner line at session start when YOLO is already active:⚠ YOLO mode — all approval prompts bypassed. Hidden when YOLO is off so the default banner stays uncluttered.
- A⚠ YOLOfragment in the status bar across all width tiers, updated live as you toggle YOLO on or off (rich-text renderer and plain-text fallback).

`⚠ YOLO mode — all approval prompts bypassed`
`⚠ YOLO`

YOLO mode disablesalldangerous command safety checks for the session —exceptthe hardline blocklist (see below). Use only when you fully trust the commands being generated (e.g., well-tested automation scripts in disposable environments).

For destructive session slash commands (/clear,/new//reset,/undo,/quit --delete—/exit --deleteis an alias), the CLI also prompts for confirmation before running them. SeeSlash Commands — Confirmation prompts for destructive commands.

`/clear`
`/new`
`/reset`
`/undo`
`/quit --delete`
`/exit --delete`
[Slash Commands — Confirmation prompts for destructive commands](/docs/reference/slash-commands#confirmation-prompts-for-destructive-commands)

### Hardline Blocklist (Always-On Floor)​

Some commands are so catastrophic — irreversible filesystem wipes, fork bombs, direct block-device writes — that Hermes refuses to run themregardlessof:

- --yolo//yolotoggled on
- approvals.mode: off
- Cron jobs running in headlessapprovemode
- User explicitly clicking "allow always"

`--yolo`
`/yolo`
`approvals.mode: off`
`approve`

The blocklist is the floor below--yolo. It tripsbeforethe approval layer even sees the command, and there's no override flag. Patterns currently covered (not exhaustive; kept in sync withtools/approval.py::UNRECOVERABLE_BLOCKLIST):

`--yolo`
`tools/approval.py::UNRECOVERABLE_BLOCKLIST`

| Pattern | Why it's hardline |
| --- | --- |
| rm -rf /and obvious variants | Wipes the filesystem root |
| rm -rf --no-preserve-root / | The explicit "yes I mean root" variant |
| :(){ :|:& };:(bash fork bomb) | Pegs the host until reboot |
| mkfs.*on a mounted root device | Formats the live system |
| dd if=/dev/zero of=/dev/sd* | Zeroes a physical disk |
| Piping untrusted URLs toshat the rootfs top level | Remote-code-execution attack vector too broad to approve |

`rm -rf /`
`rm -rf --no-preserve-root /`
`:(){ :|:& };:`
`mkfs.*`
`dd if=/dev/zero of=/dev/sd*`
`sh`

If you hit the blocklist, the tool call returns an explanatory error to the agent and nothing runs. If a legitimate workflow needs one of these commands (you're the operator of a wipe-and-reinstall pipeline, for example), run it outside the agent.

### User-Defined Deny Rules (approvals.deny)​

`approvals.deny`

The hardline blocklist is fixed and code-shipped.approvals.denyis its user-editable counterpart: a list of glob patterns that block matching terminal commands unconditionally —before--yolo,/yolo, andapprovals.mode: offare consulted. Use it to run yolo-with-exceptions: "let the agent do everything, except these specific things, ever."

`approvals.deny`
`--yolo`
`/yolo`
`approvals.mode: off`

```
approvals:  deny:    - "git push --force*"    - "*curl*|*sh*"    - "dd if=* of=/dev/*"
```

Details:

- Patterns arefnmatchglobs (*,?,[...]) matchedcase-insensitivelyagainst the whole command text.git push --force*matchesgit push --force origin mainbut notgit push origin main.
- Matching runs over the same normalized/deobfuscated command variants the dangerous-pattern detector uses, so simple quoting tricks (git pu""sh --force) don't slip past a rule.
- YAML quoting:always quote patterns. A bare leading*is a YAML alias and fails to parse;{,!, and:have their own YAML meanings. Single quotes are safest for shell-ish content.
- Deny rules apply to host-reaching backends (local, SSH, host-mounted Docker). Isolated container backends skip the guard stack entirely, as they always have — nothing they run can touch the host.
- A denied command returns a BLOCKED error to the agent telling it not to retry or rephrase. Nothing runs.

[fnmatch](https://docs.python.org/3/library/fnmatch.html)
`*`
`?`
`[...]`
`git push --force*`
`git push --force origin main`
`git push origin main`
`git pu""sh --force`
`*`
`{`
`!`
`: `

Like the rest of the approval config, changes take effect immediately (the config cache is mtime-keyed) — no session restart needed.

Deny rules are a guardrail against an honest-but-wrong agent, the same threat model as the dangerous-pattern detector. They are not a sandbox against a deliberately adversarial process — for that, use an isolated backend (Docker, Modal) or an egress-restricted environment.

### Approval Timeout​

When a dangerous command prompt appears, the user has a configurable amount of time to respond. If no response is given within the timeout, the command isdeniedby default (fail-closed).

Configure the timeout in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
approvals:  timeout: 60  # seconds (default: 60)
```

### What Triggers Approval​

The following patterns trigger approval prompts (defined intools/approval.py):

`tools/approval.py`

| Pattern | Description |
| --- | --- |
| rm -r/rm --recursive | Recursive delete |
| rm ... / | Delete in root path |
| chmod 777/666/o+w/a+w | World/other-writable permissions |
| chmod --recursivewith unsafe perms | Recursive world/other-writable (long flag) |
| chown -R root/chown --recursive root | Recursive chown to root |
| mkfs | Format filesystem |
| dd if= | Disk copy |
| > /dev/sd | Write to block device |
| DROP TABLE/DATABASE | SQL DROP |
| DELETE FROM(without WHERE) | SQL DELETE without WHERE |
| TRUNCATE TABLE | SQL TRUNCATE |
| > /etc/ | Overwrite system config |
| systemctl stop/restart/disable/mask | Stop/restart/disable system services |
| kill -9 -1 | Kill all processes |
| pkill -9 | Force kill processes |
| Fork bomb patterns | Fork bombs |
| bash -c/sh -c/zsh -c/ksh -c | Shell command execution via-cflag (including combined flags like-lc) |
| python -e/perl -e/ruby -e/node -c | Script execution via-e/-cflag |
| curl ... | sh/wget ... | sh | Pipe remote content to shell |
| bash <(curl ...)/sh <(wget ...) | Execute remote script via process substitution |
| teeto/etc/,~/.ssh/,~/.hermes/.env | Overwrite sensitive file via tee |
| >/>>to/etc/,~/.ssh/,~/.hermes/.env | Overwrite sensitive file via redirection |
| xargs rm | xargs with rm |
| find -exec rm/find -delete | Find with destructive actions |
| cp/mv/installto/etc/ | Copy/move file into system config |
| sed -i/sed --in-placeon/etc/ | In-place edit of system config |
| pkill/killallhermes/gateway | Self-termination prevention |
| gateway runwith&/disown/nohup/setsid | Prevents starting gateway outside service manager |

`rm -r`
`rm --recursive`
`rm ... /`
`chmod 777/666`
`o+w`
`a+w`
`chmod --recursive`
`chown -R root`
`chown --recursive root`
`mkfs`
`dd if=`
`> /dev/sd`
`DROP TABLE/DATABASE`
`DELETE FROM`
`TRUNCATE TABLE`
`> /etc/`
`systemctl stop/restart/disable/mask`
`kill -9 -1`
`pkill -9`
`bash -c`
`sh -c`
`zsh -c`
`ksh -c`
`-c`
`-lc`
`python -e`
`perl -e`
`ruby -e`
`node -c`
`-e`
`-c`
`curl ... | sh`
`wget ... | sh`
`bash <(curl ...)`
`sh <(wget ...)`
`tee`
`/etc/`
`~/.ssh/`
`~/.hermes/.env`
`>`
`>>`
`/etc/`
`~/.ssh/`
`~/.hermes/.env`
`xargs rm`
`find -exec rm`
`find -delete`
`cp`
`mv`
`install`
`/etc/`
`sed -i`
`sed --in-place`
`/etc/`
`pkill`
`killall`
`gateway run`
`&`
`disown`
`nohup`
`setsid`

Container bypass: When running indocker,singularity,modal, ordaytonabackends, dangerous command checks areskippedbecause the container itself is the security boundary. Destructive commands inside a container can't harm the host.

`docker`
`singularity`
`modal`
`daytona`

### Approval Flow (CLI)​

In the interactive CLI, dangerous commands show an inline approval prompt:

```
  ⚠️  DANGEROUS COMMAND: recursive delete      rm -rf /tmp/old-project      [o]nce  |  [s]ession  |  [a]lways  |  [d]eny      Choice [o/s/a/D]:
```

The four options:

- once— allow this single execution
- session— allow this pattern for the rest of the session
- always— add to permanent allowlist (saved toconfig.yaml)
- deny(default) — block the command

`config.yaml`

### Approval Flow (Gateway/Messaging)​

On messaging platforms, the agent sends the dangerous command details to the chat and waits for the user to reply:

- Replyyes,y,approve,ok, orgoto approve
- Replyno,n,deny, orcancelto deny

TheHERMES_EXEC_ASK=1environment variable is automatically set when running the gateway.

`HERMES_EXEC_ASK=1`

### Permanent Allowlist​

Commands approved with "always" are saved to~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
# Permanently allowed dangerous command patternscommand_allowlist:  - rm  - systemctl
```

These patterns are loaded at startup and silently approved in all future sessions.

Usehermes config editto review or remove patterns from your permanent allowlist.

`hermes config edit`

## User Authorization (Gateway)​

When running the messaging gateway, Hermes controls who can interact with the bot through a layered authorization system.

### Authorization Check Order​

The_is_user_authorized()method checks in this order:

`_is_user_authorized()`
1. Per-platform allow-all flag(e.g.,DISCORD_ALLOW_ALL_USERS=true)
2. DM pairing approved list(users approved via pairing codes)
3. Platform-specific allowlists(e.g.,TELEGRAM_ALLOWED_USERS=12345,67890)
4. Global allowlist(GATEWAY_ALLOWED_USERS=12345,67890)
5. Global allow-all(GATEWAY_ALLOW_ALL_USERS=true)
6. Default: deny

`DISCORD_ALLOW_ALL_USERS=true`
`TELEGRAM_ALLOWED_USERS=12345,67890`
`GATEWAY_ALLOWED_USERS=12345,67890`
`GATEWAY_ALLOW_ALL_USERS=true`

### Platform Allowlists​

Set allowed user IDs as comma-separated values in~/.hermes/.env:

`~/.hermes/.env`

```
# Platform-specific allowlistsTELEGRAM_ALLOWED_USERS=123456789,987654321DISCORD_ALLOWED_USERS=111222333444555666WHATSAPP_ALLOWED_USERS=15551234567SLACK_ALLOWED_USERS=U01ABC123# Cross-platform allowlist (checked for all platforms)GATEWAY_ALLOWED_USERS=123456789# Per-platform allow-all (use with caution)DISCORD_ALLOW_ALL_USERS=true# Global allow-all (use with extreme caution)GATEWAY_ALLOW_ALL_USERS=true
```

Ifno allowlists are configuredandGATEWAY_ALLOW_ALL_USERSis not set,all users are denied. The gateway logs a warning at startup:

`GATEWAY_ALLOW_ALL_USERS`

```
No user allowlists configured. All unauthorized users will be denied.Set GATEWAY_ALLOW_ALL_USERS=true in ~/.hermes/.env to allow open access,or configure platform allowlists (e.g., TELEGRAM_ALLOWED_USERS=your_id).
```

### DM Pairing System​

For more flexible authorization, Hermes includes a code-based pairing system. Instead of requiring user IDs upfront, unknown users receive a one-time pairing code that the bot owner approves via the CLI.

How it works:

1. An unknown user sends a DM to the bot
2. The bot replies with an 8-character pairing code
3. The bot owner runshermes pairing approve <platform> <code>on the CLI
4. The user is permanently approved for that platform

`hermes pairing approve <platform> <code>`

Control how unauthorized direct messages are handled in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
unauthorized_dm_behavior: pairwhatsapp:  unauthorized_dm_behavior: ignore
```

- pairis the default for chat-style DM platforms. Unauthorized DMs get a pairing code reply.
- ignoresilently drops unauthorized DMs.
- Email defaults toignoreunlessplatforms.email.unauthorized_dm_behavior: pairis set, because inboxes can contain unrelated unread mail.
- Platform sections override the global default, so you can keep pairing on Telegram while keeping WhatsApp silent.

`pair`
`ignore`
`ignore`
`platforms.email.unauthorized_dm_behavior: pair`

Security features(based on OWASP + NIST SP 800-63-4 guidance):

| Feature | Details |
| --- | --- |
| Code format | 8-char from 32-char unambiguous alphabet (no 0/O/1/I) |
| Randomness | Cryptographic (secrets.choice()) |
| Code TTL | 1 hour expiry |
| Rate limiting | 1 request per user per 10 minutes |
| Pending limit | Max 3 pending codes per platform |
| Lockout | 5 failed approval attempts → 1-hour lockout |
| File security | chmod 0600on all pairing data files |
| Logging | Codes are never logged to stdout |

`secrets.choice()`
`chmod 0600`

Pairing CLI commands:

```
# List pending and approved usershermes pairing list# Approve a pairing codehermes pairing approve telegram ABC12DEF# Revoke a user's accesshermes pairing revoke telegram 123456789# Clear all pending codeshermes pairing clear-pending
```

`hermes`

The official Docker image runs the gateway as the unprivilegedhermesuser
(uid 10000) viagosu, butdocker execdefaults to root. Approval files
created by root are written with mode0600 root:rootand the gateway
cannot read them — the approval is silently ignored (#10270).

`hermes`
`gosu`
`docker exec`
`0600 root:root`
[#10270](https://github.com/NousResearch/hermes-agent/issues/10270)

Always pass-u hermes:

`-u hermes`

```
docker exec -u hermes hermes-agent hermes pairing approve telegram ABC12DEF
```

If you already ran the command as root and the user is still unauthorized,
restart the container — the entrypoint will fix ownership on the next start.

Storage:Pairing data is stored in~/.hermes/pairing/with per-platform JSON files:

`~/.hermes/pairing/`
- {platform}-pending.json— pending pairing requests
- {platform}-approved.json— approved users
- _rate_limits.json— rate limit and lockout tracking

`{platform}-pending.json`
`{platform}-approved.json`
`_rate_limits.json`

## Container Isolation​

When using thedockerterminal backend, Hermes applies strict security hardening to every container.

`docker`

### Docker Security Flags​

Every container runs with these flags (defined intools/environments/docker.py):

`tools/environments/docker.py`

```
_BASE_SECURITY_ARGS = [    "--cap-drop", "ALL",                          # Drop ALL Linux capabilities    "--cap-add", "DAC_OVERRIDE",                  # Root can write to bind-mounted dirs    "--cap-add", "CHOWN",                         # Package managers need file ownership    "--cap-add", "FOWNER",                        # Package managers need file ownership    "--security-opt", "no-new-privileges",         # Block privilege escalation    "--pids-limit", "256",                         # Limit process count    "--tmpfs", "/tmp:rw,nosuid,size=512m",         # Size-limited /tmp    "--tmpfs", "/var/tmp:rw,noexec,nosuid,size=256m",  # No-exec /var/tmp]
```

SETUID/SETGIDarenotin the base list — they're added conditionally when the container starts as root and an init/entrypoint must drop privileges (the s6 privilege-drop path). They're skipped when the container already runs as a non-root--user. The/runtmpfs is also split out from the base list and mounted per-image (hardenednoexecby default,execonly for s6-overlay images that exec from/run).

`SETUID`
`SETGID`
`--user`
`/run`
`noexec`
`exec`
`/run`

### Resource Limits​

Container resources are configurable in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
terminal:  backend: docker  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"  docker_forward_env: []  # Explicit allowlist only; empty keeps secrets out of the container  container_cpu: 1        # CPU cores  container_memory: 5120  # MB (default 5GB)  container_disk: 51200   # MB (default 50GB, requires overlay2 on XFS)  container_persistent: true  # Persist filesystem across sessions
```

### Filesystem Persistence​

- Persistent mode(container_persistent: true): Bind-mounts/workspaceand/rootfrom~/.hermes/sandboxes/docker/<task_id>/
- Ephemeral mode(container_persistent: false): Uses tmpfs for workspace — everything is lost on cleanup

`container_persistent: true`
`/workspace`
`/root`
`~/.hermes/sandboxes/docker/<task_id>/`
`container_persistent: false`

For production gateway deployments, usedocker,modal, ordaytonabackend to isolate agent commands from your host system. This eliminates the need for dangerous command approval entirely.

`docker`
`modal`
`daytona`

If you add names toterminal.docker_forward_env, those variables are intentionally injected into the container for terminal commands. This is useful for task-specific credentials likeGITHUB_TOKEN, but it also means code running in the container can read and exfiltrate them.

`terminal.docker_forward_env`
`GITHUB_TOKEN`

## Terminal Backend Security Comparison​

| Backend | Isolation | Dangerous Cmd Check | Best For |
| --- | --- | --- | --- |
| local | None — runs on host | ✅ Yes | Development, trusted users |
| ssh | Remote machine | ✅ Yes | Running on a separate server |
| docker | Container | ❌ Skipped (container is boundary) | Production gateway |
| singularity | Container | ❌ Skipped | HPC environments |
| modal | Cloud sandbox | ❌ Skipped | Scalable cloud isolation |
| daytona | Cloud sandbox | ❌ Skipped | Persistent cloud workspaces |

## Environment Variable Passthrough​

Bothexecute_codeandterminalstrip sensitive environment variables from child processes to prevent credential exfiltration by LLM-generated code. However, skills that declarerequired_environment_variableslegitimately need access to those vars.

`execute_code`
`terminal`
`required_environment_variables`

### How It Works​

Two mechanisms allow specific variables through the sandbox filters:

1. Skill-scoped passthrough (automatic)

When a skill is loaded (viaskill_viewor the/skillcommand) and declaresrequired_environment_variables, any of those vars that are actually set in the environment are automatically registered as passthrough. Missing vars (still in setup-needed state) arenotregistered.

`skill_view`
`/skill`
`required_environment_variables`

```
# In a skill's SKILL.md frontmatterrequired_environment_variables:  - name: TENOR_API_KEY    prompt: Tenor API key    help: Get a key from https://developers.google.com/tenor
```

After loading this skill,TENOR_API_KEYpasses through toexecute_code,terminal(local),and remote backends (Docker, Modal)— no manual configuration needed.

`TENOR_API_KEY`
`execute_code`
`terminal`

Prior to v0.5.1, Docker'sforward_envwas a separate system from the skill passthrough. They are now merged — skill-declared env vars are automatically forwarded into Docker containers and Modal sandboxes without needing to add them todocker_forward_envmanually.

`forward_env`
`docker_forward_env`

2. Config-based passthrough (manual)

For env vars not declared by any skill, add them toterminal.env_passthroughinconfig.yaml:

`terminal.env_passthrough`
`config.yaml`

```
terminal:  env_passthrough:    - MY_CUSTOM_KEY    - ANOTHER_TOKEN
```

### Credential File Passthrough (OAuth tokens, etc.)​

Some skills needfiles(not just env vars) in the sandbox — for example, Google Workspace stores OAuth tokens asgoogle_token.jsonunder the active profile'sHERMES_HOME. Skills declare these in frontmatter:

`google_token.json`
`HERMES_HOME`

```
required_credential_files:  - path: google_token.json    description: Google OAuth2 token (created by setup script)  - path: google_client_secret.json    description: Google OAuth2 client credentials
```

When loaded, Hermes checks if these files exist in the active profile'sHERMES_HOMEand registers them for mounting:

`HERMES_HOME`
- Docker: Read-only bind mounts (-v host:container:ro)
- Modal: Mounted at sandbox creation + synced before each command (handles mid-session OAuth setup)
- Local: No action needed (files already accessible)

`-v host:container:ro`

You can also list credential files manually inconfig.yaml:

`config.yaml`

```
terminal:  credential_files:    - google_token.json    - my_custom_oauth_token.json
```

Paths are relative to~/.hermes/. Files are mounted to/root/.hermes/inside the container. This list is read bytools/credential_files.py(terminal.credential_files) — it lives under theterminal:block but is loaded by the credential-files module, not the core terminal backend, so it isn't part of the bundledDEFAULT_CONFIGsnapshot.

`~/.hermes/`
`/root/.hermes/`
`tools/credential_files.py`
`terminal.credential_files`
`terminal:`
`DEFAULT_CONFIG`

### What Each Sandbox Filters​

| Sandbox | Default Filter | Passthrough Override |
| --- | --- | --- |
| execute_code | Blocks vars containingKEY,TOKEN,SECRET,PASSWORD,CREDENTIAL,PASSWD,AUTHin name; only allows safe-prefix vars through | ✅ Passthrough vars bypass both checks |
| terminal(local) | Blocks explicit Hermes infrastructure vars (provider keys, gateway tokens, tool API keys) | ✅ Passthrough vars bypass the blocklist |
| terminal(Docker) | No host env vars by default | ✅ Passthrough vars +docker_forward_envforwarded via-e |
| terminal(Modal) | No host env/files by default | ✅ Credential files mounted; env passthrough via sync |
| MCP | Blocks everything except safe system vars + explicitly configuredenv | ❌ Not affected by passthrough (use MCPenvconfig instead) |

`KEY`
`TOKEN`
`SECRET`
`PASSWORD`
`CREDENTIAL`
`PASSWD`
`AUTH`
`docker_forward_env`
`-e`
`env`
`env`

### Security Considerations​

- The passthrough only affects vars you or your skills explicitly declare — the default security posture is unchanged for arbitrary LLM-generated code
- Credential files are mountedread-onlyinto Docker containers
- Skills Guard scans skill content for suspicious env access patterns before installation
- Missing/unset vars are never registered (you can't leak what doesn't exist)
- Hermes infrastructure secrets (provider API keys, gateway tokens) should never be added toenv_passthrough— they have dedicated mechanisms

`env_passthrough`

## MCP Credential Handling​

MCP (Model Context Protocol) server subprocesses receive afiltered environmentto prevent accidental credential leakage.

### Safe Environment Variables​

Only these variables are passed through from the host to MCP stdio subprocesses:

```
PATH, HOME, USER, LANG, LC_ALL, TERM, SHELL, TMPDIR
```

Plus anyXDG_*variables. All other environment variables (API keys, tokens, secrets) arestripped.

`XDG_*`

Variables explicitly defined in the MCP server'senvconfig are passed through:

`env`

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."  # Only this is passed
```

### Credential Redaction​

Error messages from MCP tools are sanitized before being returned to the LLM. The following patterns are replaced with[REDACTED]:

`[REDACTED]`
- GitHub PATs (ghp_...)
- OpenAI-style keys (sk-...)
- Bearer tokens
- token=,key=,API_KEY=,password=,secret=parameters

`ghp_...`
`sk-...`
`token=`
`key=`
`API_KEY=`
`password=`
`secret=`

### Website Access Policy​

You can restrict which websites the agent can access through its web and browser tools. This is useful for preventing the agent from accessing internal services, admin panels, or other sensitive URLs.

```
# In ~/.hermes/config.yamlsecurity:  website_blocklist:    enabled: true    domains:      - "*.internal.company.com"      - "admin.example.com"    shared_files:      - "/etc/hermes/blocked-sites.txt"
```

When a blocked URL is requested, the tool returns an error explaining the domain is blocked by policy. The blocklist is enforced acrossweb_search,web_extract,browser_navigate, and all URL-capable tools.

`web_search`
`web_extract`
`browser_navigate`

SeeWebsite Blocklistin the configuration guide for full details.

[Website Blocklist](/docs/user-guide/configuration#website-blocklist)

### SSRF Protection​

All URL-capable tools (web search, web extract, vision, browser) validate URLs before fetching them to prevent Server-Side Request Forgery (SSRF) attacks. Blocked addresses include:

- Private networks(RFC 1918):10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
- Loopback:127.0.0.0/8,::1
- Link-local:169.254.0.0/16(includes cloud metadata at169.254.169.254)
- CGNAT / shared address space(RFC 6598):100.64.0.0/10(Tailscale, WireGuard VPNs)
- Cloud metadata hostnames:metadata.google.internal,metadata.goog
- Reserved, multicast, and unspecified addresses

`10.0.0.0/8`
`172.16.0.0/12`
`192.168.0.0/16`
`127.0.0.0/8`
`::1`
`169.254.0.0/16`
`169.254.169.254`
`100.64.0.0/10`
`metadata.google.internal`
`metadata.goog`

SSRF protection is always active for internet-facing use and DNS failures are treated as blocked (fail-closed). Redirect chains are re-validated at each hop to prevent redirect-based bypasses.

#### Intentionally allowing private URLs​

Some setups legitimately need private/internal URL access — home networks that resolvehome.arpato RFC 1918 space, LAN-only Ollama/llama.cpp endpoints, internal wikis, cloud metadata debugging, and the like. For those cases there's a global opt-out:

`home.arpa`

```
security:  allow_private_urls: true   # default: false
```

When on, web tools, the browser, vision URL fetches, and gateway media downloads no longer reject RFC 1918 / loopback / link-local / CGNAT / cloud-metadata destinations.This is a deliberate trust boundary— only enable it on machines where the agent running arbitrary prompt-injected URLs against the local network is an acceptable risk. Public-facing gateways should leave it off.

The host-substring guard (which blocks lookalike Unicode domain tricks even when the underlying IP is public) stays on regardless of this setting.

### Tirith Pre-Exec Security Scanning​

Hermes integratestirithfor content-level command scanning before execution. Tirith detects threats that pattern matching alone misses:

[tirith](https://github.com/sheeki03/tirith)
- Homograph URL spoofing (internationalized domain attacks)
- Pipe-to-interpreter patterns (curl | bash,wget | sh)
- Terminal injection attacks

`curl | bash`
`wget | sh`

Tirith auto-installs from GitHub releases on first use with SHA-256 checksum verification (and cosign provenance verification if cosign is available).

```
# In ~/.hermes/config.yamlsecurity:  tirith_enabled: true       # Enable/disable tirith scanning (default: true)  tirith_path: "tirith"      # Path to tirith binary (default: PATH lookup)  tirith_timeout: 5          # Subprocess timeout in seconds  tirith_fail_open: true     # Allow execution when tirith is unavailable (default: true)
```

Whentirith_fail_openistrue(default), commands proceed if tirith is not installed or times out. Set tofalsein high-security environments to block commands when tirith is unavailable.

`tirith_fail_open`
`true`
`false`

Tirith ships prebuilt binaries for Linux (x86_64 / aarch64) and macOS (x86_64 / arm64). On platforms with no prebuilt binary (Windows, etc.), tirith is silently skipped — pattern-matching guards still run, and the CLI does not surface an "unavailable" banner. To use tirith on Windows, run Hermes under WSL.

Tirith's verdict integrates with the approval flow: safe commands pass through, while both suspicious and blocked commands trigger user approval with the full tirith findings (severity, title, description, safer alternatives). Users can approve or deny — the default choice is deny to keep unattended scenarios secure.

### Context File Injection Protection​

Context files (AGENTS.md, .cursorrules, SOUL.md) are scanned for prompt injection before being included in the system prompt. The scanner checks for:

- Instructions to ignore/disregard prior instructions
- Hidden HTML comments with suspicious keywords
- Attempts to read secrets (.env,credentials,.netrc)
- Credential exfiltration viacurl
- Invisible Unicode characters (zero-width spaces, bidirectional overrides)

`.env`
`credentials`
`.netrc`
`curl`

Blocked files show a warning:

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

## Best Practices for Production Deployment​

### Gateway Deployment Checklist​

1. Set explicit allowlists— never useGATEWAY_ALLOW_ALL_USERS=truein production
2. Use container backend— setterminal.backend: dockerin config.yaml
3. Restrict resource limits— set appropriate CPU, memory, and disk limits
4. Store secrets securely— keep API keys in~/.hermes/.envwith proper file permissions
5. Enable DM pairing— use pairing codes instead of hardcoding user IDs when possible
6. Review command allowlist— periodically auditcommand_allowlistin config.yaml
7. Setterminal.cwd— don't let the agent operate from sensitive directories
8. Run as non-root— never run the gateway as root
9. Monitor logs— check~/.hermes/logs/for unauthorized access attempts
10. Keep updated— runhermes updateregularly for security patches

`GATEWAY_ALLOW_ALL_USERS=true`
`terminal.backend: docker`
`~/.hermes/.env`
`command_allowlist`
`terminal.cwd`
`~/.hermes/logs/`
`hermes update`

### Securing API Keys​

```
# Set proper permissions on the .env filechmod 600 ~/.hermes/.env# Keep separate keys for different services# Never commit .env files to version control
```

### Network Isolation​

For maximum security, run the gateway on a separate machine or VM. Setterminal.backend: sshinconfig.yaml, then provide host details via environment variables in~/.hermes/.env:

`terminal.backend: ssh`
`config.yaml`
`~/.hermes/.env`

```
# ~/.hermes/config.yamlterminal:  backend: ssh
```

```
# ~/.hermes/.envTERMINAL_SSH_HOST=agent-worker.localTERMINAL_SSH_USER=hermesTERMINAL_SSH_KEY=~/.ssh/hermes_agent_key
```

The SSH connection details live in.env(notconfig.yaml) so they aren't checked in or shared along with profile exports. This keeps the gateway's messaging connections separate from the agent's command execution.

`.env`
`config.yaml`

## Supply-chain advisory checking​

Hermes ships with a built-in advisory scanner that flags Python packages in the active venv that match a curated catalog of known-compromised versions (supply-chain worms like the May 2026mistralai 2.4.6poisoning). Implementation lives inhermes_cli/security_advisories.py.

`mistralai 2.4.6`
`hermes_cli/security_advisories.py`

How it runs:

- CLI startup banner.A one-line warning is printed if any advisory matches, with a pointer tohermes doctorfor the full remediation.
- hermes doctor.Surfaces every active advisory with version specifics and 2-4 step remediation instructions.
- Gateway startup.Logged togateway.log; the first interactive message gets a short operator banner.

`hermes doctor`
`hermes doctor`
`gateway.log`

Each advisory carries a stable id. Once you have read and acted on it you can dismiss it for good:

```
hermes doctor --ack <advisory-id>
```

The ack is persisted toconfig.security.acked_advisoriesand survives restart. Old advisories are intentionallynotremoved from the catalog — leaving them in place keeps fresh installs warned about historically poisoned versions that might still be cached in a private mirror.

`config.security.acked_advisories`

The check itself is stdlib-only and runs from oneimportlib.metadata.version()lookup per advisory, so it's safe to run on every startup.

`importlib.metadata.version()`

### Lazy install of optional dependencies​

Many features (Mistral TTS, ElevenLabs, Honcho memory, Bedrock, Slack, Matrix, …) depend on Python packages that not every user needs. Hermes installs theselazilyon first use rather than eagerly underhermes-agent[all]. The implementation lives intools/lazy_deps.py.

`hermes-agent[all]`
`tools/lazy_deps.py`

The trade-off this fixes:

- Fragility.When one extra's transitive dependency becomes unavailable on PyPI (quarantined for malware, yanked, broken upload), the entire[all]resolve would fail and fresh installs would silently fall back to a stripped tier — losing 10+ unrelated extras at once. Lazy install isolates each backend so one poisoned dep can't break unrelated features.
- Bloat.A user who only ever talks to one provider no longer pulls hundreds of packages they will never import.

`[all]`

How it works:

1. A backend module callsensure("feature.name")at the top of its first-import path.
2. If the deps are missing,ensurecheckssecurity.allow_lazy_installsinconfig.yaml(defaulttrue) and runs a venv-scopedpip installfor the allowlisted specs.
3. If the install fails or the user has disabled lazy installs, the call raisesFeatureUnavailablewith the actual pip stderr and a pointer athermes tools.

`ensure("feature.name")`
`ensure`
`security.allow_lazy_installs`
`config.yaml`
`true`
`pip install`
`FeatureUnavailable`
`hermes tools`

Security guarantees enforced bytools/lazy_deps.py:

`tools/lazy_deps.py`

| Guarantee | What it means |
| --- | --- |
| Venv-scoped only | Installs targetsys.executablein the active venv — never the system Python |
| PyPI by name only | Specs accept"package>=1.0,<2"syntax. No--index-url,git+https://, or file: paths — a maliciousconfig.yamlcannot redirect the install |
| Allowlist | Only specs that appear in the in-treeLAZY_DEPSmap can be installed via this path. A typo in a feature name does NOT get install-anything semantics |
| Opt-out | Setsecurity.allow_lazy_installs: falseto disable runtime installs entirely. Useful for restricted networks or strict security postures |
| No silent retries | Failures surface asFeatureUnavailable— no caching of bad state, no retry storms |

`sys.executable`
`"package>=1.0,<2"`
`--index-url`
`git+https://`
`config.yaml`
`LAZY_DEPS`
`security.allow_lazy_installs: false`
`FeatureUnavailable`

To disable runtime installs:

```
# ~/.hermes/config.yamlsecurity:  allow_lazy_installs: false
```

When disabled, backends that need optional deps will tell the user to run the install manually (pip install …) or pick a different backend viahermes tools.

`pip install …`
`hermes tools`
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/security.md)