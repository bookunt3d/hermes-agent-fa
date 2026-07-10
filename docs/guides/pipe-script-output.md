---
layout: docs
title: "خروجی اسکریپت لوله‌ای"
permalink: /docs/guides/pipe-script-output/
---

# Pipe Script Output to Messaging Platforms

hermes sendis a small, scriptable CLI that pushes a message to any
messaging platform Hermes is already configured for. Think of it as a
cross-platformcurlfor notifications — you don't need a running
gateway, you don't need an LLM, and you don't need to re-paste bot tokens
into each of your scripts.

`hermes send`
`curl`

Use it for:

- System monitoring (memory, disk, GPU temp, long-running job finished)
- CI/CD notifications (deploy done, test failure)
- Cron scripts that need to ping you with results
- Quick one-shot messages from a terminal
- Piping any tool's output anywhere (make | hermes send --to slack:#builds)

`make | hermes send --to slack:#builds`

The command reuses the same credentials and platform adapters thathermes gatewayalready uses, so there's no second configuration surface to
maintain.

`hermes gateway`

## Quick Start​

```
# Plain text to the home channel for a platformhermes send --to telegram "deploy finished"# Pipe in stdout from anythingecho "RAM 92%" | hermes send --to telegram:-1001234567890# Send a filehermes send --to discord:#ops --file /tmp/report.md# Attach a subject/header linehermes send --to slack:#eng --subject "[CI] build.log" --file build.log# Thread target (Telegram topic, Discord thread)hermes send --to telegram:-1001234567890:17585 "threaded reply"# List every configured targethermes send --list# Filter by platformhermes send --list telegram
```

## Argument Reference​

| Flag | Description |
| --- | --- |
| -t, --to TARGET | Destination. Seetarget formats. |
| message(positional) | Message text. Omit to read from--fileor stdin. |
| -f, --file PATH | Read the body from a file.--file -forces stdin. |
| -s, --subject LINE | Prepend a header/subject line before the body. |
| -l, --list | List available targets. Optional positional platform filter. |
| -q, --quiet | No stdout on success (exit code only — ideal for scripts). |
| --json | Emit the raw JSON result of the send. |
| -h, --help | Show the built-in help text. |

`-t, --to TARGET`
`message`
`--file`
`-f, --file PATH`
`--file -`
`-s, --subject LINE`
`-l, --list`
`-q, --quiet`
`--json`
`-h, --help`

### Target Formats​

| Format | Example | Meaning |
| --- | --- | --- |
| platform | telegram | Send to the platform's configured home channel |
| platform:chat_id | telegram:-1001234567890 | Specific numeric chat / group / user |
| platform:chat_id:thread_id | telegram:-1001234567890:17585 | Specific thread or Telegram forum topic |
| platform:#channel | discord:#ops | Human-friendly channel name (resolved against the channel directory) |
| platform:+E164 | signal:+15551234567 | Phone-addressed platforms: Signal, SMS, WhatsApp |

`platform`
`telegram`
`platform:chat_id`
`telegram:-1001234567890`
`platform:chat_id:thread_id`
`telegram:-1001234567890:17585`
`platform:#channel`
`discord:#ops`
`platform:+E164`
`signal:+15551234567`

Any platform Hermes ships adapters for works as a target:telegram,discord,slack,signal,sms,whatsapp,matrix,mattermost,feishu,dingtalk,wecom,weixin,email, and
others.

`telegram`
`discord`
`slack`
`signal`
`sms`
`whatsapp`
`matrix`
`mattermost`
`feishu`
`dingtalk`
`wecom`
`weixin`
`email`

### Exit Codes​

| Code | Meaning |
| --- | --- |
| 0 | Send (or list) succeeded |
| 1 | Delivery failed at the platform level (auth, permissions, network) |
| 2 | Usage / argument / config error |

`0`
`1`
`2`

Exit codes follow the standard Unix convention so your scripts can
branch on them the same way they would oncurlorgrep.

`curl`
`grep`

## Message Body Resolution​

hermes sendresolves the message body in this order:

`hermes send`
1. Positional argument—hermes send --to telegram "hi"
2. --file PATH—hermes send --to telegram --file msg.txt
3. Piped stdin—echo hi | hermes send --to telegram

`hermes send --to telegram "hi"`
`--file PATH`
`hermes send --to telegram --file msg.txt`
`echo hi | hermes send --to telegram`

When stdin is a TTY (no pipe), Hermes doesnotwait for input — you'll
get a clear usage error instead. This keeps scripts from hanging if they
accidentally omit the body.

## Real-World Examples​

### Monitoring: Memory / Disk Alerts​

Replace ad-hoccurl https://api.telegram.org/...calls in your watchdogs
with a single portable line:

`curl https://api.telegram.org/...`

```
#!/usr/bin/env bashram_pct=$(free | awk '/^Mem:/ {printf "%d", $3 * 100 / $2}')if [ "$ram_pct" -ge 85 ]; then  hermes send --to telegram --subject "⚠ MEMORY WARNING" \    "RAM ${ram_pct}% on $(hostname)"fi
```

Becausehermes sendreuses your Hermes config, the same script works on
any host where Hermes is installed — no need to export bot tokens into
each machine's environment manually.

`hermes send`

For watchdogs that might fire when the gateway itself is struggling (OOM
alerts, disk-full alerts), keep using a minimalcurlcall instead ofhermes send. If the Python interpreter can't load because the box is
thrashing, you still want that alert to go out.

`curl`
`hermes send`

### CI / CD: Build and Test Results​

```
# In .github/workflows/deploy.yml or any CI scriptif ./scripts/deploy.sh; then  hermes send --to slack:#deploys "✅ ${CI_COMMIT_SHA:0:7} deployed"else  tail -n 100 deploy.log | hermes send \    --to slack:#deploys --subject "❌ deploy failed"  exit 1fi
```

### Cron: Daily Report​

```
# Crontab entry0 9 * * * /usr/local/bin/generate-metrics.sh \  | /home/me/.hermes/bin/hermes send \      --to telegram --subject "Daily metrics $(date +%Y-%m-%d)"
```

### Long-Running Tasks: Ping When Done​

```
./train.py --epochs 200 && \  hermes send --to telegram "training done" || \  hermes send --to telegram "training failed (exit $?)"
```

### Scripting with--jsonand--quiet​

`--json`
`--quiet`

```
# Hard-fail a script if delivery fails; don't clutter logs on successhermes send --to telegram --quiet "keepalive" || {  echo "Telegram delivery failed" >&2  exit 1}# Capture the message ID for later editing / threadingmsg_id=$(hermes send --to discord:#ops --json "build started" \  | jq -r .message_id)
```

## Doeshermes sendNeed the Gateway Running?​

`hermes send`

Usually no.For any bot-token platform — Telegram, Discord, Slack,
Signal, SMS, WhatsApp Cloud API, and most others —hermes sendcalls
the platform's REST endpoint directly using credentials from~/.hermes/.envand~/.hermes/config.yaml. It's a standalone subprocess
that exits as soon as the message is delivered.

`hermes send`
`~/.hermes/.env`
`~/.hermes/config.yaml`

A live gateway is only required forplugin platformsthat rely on a
persistent adapter connection (for example, a custom plugin that keeps
a long-lived WebSocket open). In that case you'll get a clear error
pointing at the gateway; start it withhermes gateway startand retry.

`hermes gateway start`

## Listing and Discovering Targets​

Before sending to a specific channel, you can inspect what's available:

```
# Every target across every configured platformhermes send --list# Just Telegram targetshermes send --list telegram# Machine-readablehermes send --list --json
```

The listing is built from~/.hermes/channel_directory.json, which the
gateway refreshes every few minutes while it's running. If you see
"no channels discovered yet", start the gateway once (hermes gateway start) so it can populate the cache.

`~/.hermes/channel_directory.json`
`hermes gateway start`

Human-friendly names (discord:#ops,slack:#engineering) are resolved
against this cache at send time, so you don't need to memorize numeric
IDs.

`discord:#ops`
`slack:#engineering`

## Comparison with Other Approaches​

| Approach | Multi-platform | Reuses Hermes creds | Needs gateway | Best for |
| --- | --- | --- | --- | --- |
| hermes send | ✅ | ✅ | No (bot-token) | Everything below |
| Rawcurlto each platform | Each scripted separately | Manual | No | Critical watchdogs |
| cronjob with--deliver | ✅ | ✅ | No | Scheduled agent tasks |

`hermes send`
`curl`
`cron`
`--deliver`

hermes sendis intentionally the simplest possible surface. If you need
an agent to decide what to say, schedule a cron job — the agent's final
response is auto-delivered to the configureddeliver:target (the agent
no longer fires messages itself). If you need a scheduled run with LLM-generated content,
usecronjob(action='create', prompt=...)withdeliver='telegram:...'.
If you just need to pipe a raw string, reach forhermes send.

`hermes send`
`deliver:`
`cronjob(action='create', prompt=...)`
`deliver='telegram:...'`
`hermes send`

## Related​

- Automate Anything with Cron—
scheduled jobs whose output auto-delivers to any platform.
- Gateway Internals—
the delivery router thathermes sendshares with cron delivery.
- Messaging Platform Setup—
one-time configuration for each platform.

`hermes send`