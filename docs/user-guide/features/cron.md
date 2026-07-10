---
layout: docs
title: "Features_Cron"
permalink: /docs/user-guide/features/cron/
---

- 
- Features
- Automation
- Scheduled Tasks (Cron)

# Scheduled Tasks (Cron)

Schedule tasks to run automatically with natural language or cron expressions. Hermes exposes cron management through a singlecronjobtool with action-style operations instead of separate schedule/list/remove tools.

`cronjob`

## What cron can do now​

Cron jobs can:

- schedule one-shot or recurring tasks
- pause, resume, edit, trigger, and remove jobs
- attach zero, one, or multiple skills to a job
- deliver results back to the origin chat, local files, or configured platform targets
- run in fresh agent sessions with the normal static tool list
- run inno-agent mode— a script on a schedule, its stdout delivered verbatim, zero LLM involvement (see theno-agent modesection below)

All of this is available to Hermes itself through thecronjobtool, so you can create, pause, edit, and remove jobs by asking in plain language — no CLI required.

`cronjob`

At creation, an unpinned job (one you don't give an explicitprovider/model) follows the global default selected byhermes model— and Hermessnapshotsthat provider and model on the job. If the global default later changes, the jobfails closed: it skips the run, makes no inference call, and sends an alert telling you to pin the provider/model explicitly (cronjob action=update job_id=… provider=… model=…) to proceed. This prevents an unattended job from silently inheriting a switch to a paid provider/model and spending money you didn't intend (#44585). To make a job deliberately track your global default, pin it to the new values after changing them.hermes setup --portalis the lowest-friction option for unattended runs since OAuth refresh is automatic. SeeNous Portal.

`provider`
`model`
`hermes model`
`cronjob action=update job_id=… provider=… model=…`
`hermes setup --portal`

Cron-run sessions cannot recursively create more cron jobs. Hermes disables cron management tools inside cron executions to prevent runaway scheduling loops.

## Creating scheduled tasks​

### In chat with/cron​

`/cron`

```
/cron add 30m "Remind me to check the build"/cron add "every 2h" "Check server status"/cron add "every 1h" "Summarize new feed items" --skill blogwatcher/cron add "every 1h" "Use both skills and combine the result" --skill blogwatcher --skill maps
```

### From the standalone CLI​

```
hermes cron create "every 2h" "Check server status"hermes cron create "every 1h" "Summarize new feed items" --skill blogwatcherhermes cron create "every 1h" "Use both skills and combine the result" \  --skill blogwatcher \  --skill maps \  --name "Skill combo"
```

### Through natural conversation​

Ask Hermes normally:

```
Every morning at 9am, check Hacker News for AI news and send me a summary on Telegram.
```

Hermes will use the unifiedcronjobtool internally.

`cronjob`

## Skill-backed cron jobs​

A cron job can load one or more skills before it runs the prompt.

### Single skill​

```
cronjob(    action="create",    skill="blogwatcher",    prompt="Check the configured feeds and summarize anything new.",    schedule="0 9 * * *",    name="Morning feeds",)
```

### Multiple skills​

Skills are loaded in order. The prompt becomes the task instruction layered on top of those skills.

```
cronjob(    action="create",    skills=["blogwatcher", "maps"],    prompt="Look for new local events and interesting nearby places, then combine them into one short brief.",    schedule="every 6h",    name="Local brief",)
```

This is useful when you want a scheduled agent to inherit reusable workflows without stuffing the full skill text into the cron prompt itself.

## Running a job inside a project directory​

Cron jobs default to running detached from any repo — noAGENTS.md,CLAUDE.md, or.cursorrulesis loaded, and the terminal / file / code-exec tools run from whatever working directory the gateway started in. Pass--workdir(CLI) orworkdir=(tool call) to change that:

`AGENTS.md`
`CLAUDE.md`
`.cursorrules`
`--workdir`
`workdir=`

```
# Standalone CLI (schedule and prompt are positional)hermes cron create "every 1d at 09:00" \  "Audit open PRs, summarize CI health, and post to #eng" \  --workdir /home/me/projects/acme
```

```
# From a chat, via the cronjob toolcronjob(    action="create",    schedule="every 1d at 09:00",    workdir="/home/me/projects/acme",    prompt="Audit open PRs, summarize CI health, and post to #eng",)
```

Whenworkdiris set:

`workdir`
- AGENTS.md,CLAUDE.md, and.cursorrulesfrom that directory are injected into the system prompt (same discovery order as the interactive CLI)
- terminal,read_file,write_file,patch,search_files, andexecute_codeall use that directory as their working directory
- The path must be an absolute directory that exists — relative paths and missing directories are rejected at create / update time
- Pass--workdir ""(orworkdir=""via the tool) on edit to clear it and restore the old behaviour

`AGENTS.md`
`CLAUDE.md`
`.cursorrules`
`terminal`
`read_file`
`write_file`
`patch`
`search_files`
`execute_code`
`--workdir ""`
`workdir=""`

Jobs with aworkdirrun sequentially on the scheduler tick, not in the parallel pool. This is deliberate: the cron worker applies the job workdir through process-global terminal state, so two workdir jobs running at the same time would corrupt each other's cwd. Workdir-less jobs still run in parallel as before.

`workdir`

## Editing jobs​

You do not need to delete and recreate jobs just to change them.

The<job_id>placeholder below (and inLifecycle actions) also accepts the job's name (case-insensitive) — handy when you remembermorning-digestbut not the hex ID. An exact job ID takes precedence over name matches; if the reference is not an ID and a name matches more than one job, the command refuses and prints the candidate IDs so you can disambiguate.

`<job_id>`
`morning-digest`

### Chat​

```
/cron edit <job_id> --schedule "every 4h"/cron edit <job_id> --prompt "Use the revised task"/cron edit <job_id> --skill blogwatcher --skill maps/cron edit <job_id> --remove-skill blogwatcher/cron edit <job_id> --clear-skills
```

### Standalone CLI​

```
hermes cron edit <job_id> --schedule "every 4h"hermes cron edit <job_id> --prompt "Use the revised task"hermes cron edit <job_id> --skill blogwatcher --skill mapshermes cron edit <job_id> --add-skill mapshermes cron edit <job_id> --remove-skill blogwatcherhermes cron edit <job_id> --clear-skills
```

Notes:

- repeated--skillreplaces the job's attached skill list
- --add-skillappends to the existing list without replacing it
- --remove-skillremoves specific attached skills
- --clear-skillsremoves all attached skills

`--skill`
`--add-skill`
`--remove-skill`
`--clear-skills`

## Lifecycle actions​

Cron jobs now have a fuller lifecycle than just create/remove.

### Chat​

```
/cron list/cron pause <job_id>/cron resume <job_id>/cron run <job_id>/cron remove <job_id>
```

### Standalone CLI​

```
hermes cron listhermes cron pause <job_id_or_name>hermes cron resume <job_id_or_name>hermes cron run <job_id_or_name>hermes cron remove <job_id_or_name>hermes cron edit <job_id_or_name> [...flags]hermes cron statushermes cron tick
```

What they do:

- pause— keep the job but stop scheduling it
- resume— re-enable the job and compute the next future run
- run— trigger the job on the next scheduler tick
- remove— delete it entirely
- edit— modify schedule, prompt, delivery, etc.

`pause`
`resume`
`run`
`remove`
`edit`

Name-based lookup.All four mutating verbs (pause,resume,run,remove,edit) plus the agent'scronjobtool now accept a jobname(case-insensitive) in place of the hex ID. The agent and CLI both prefer an exact ID match if one exists; ambiguous name matches (multiple jobs sharing the same name) are refused with the full list of candidate IDs so you can pick one explicitly. Names are not unique, so this guard is load-bearing — it prevents silently mutating the wrong job when two share a name.

`pause`
`resume`
`run`
`remove`
`edit`
`cronjob`

## How it works​

Cron execution is handled by the gateway daemon.The gateway ticks the scheduler every 60 seconds, running any due jobs in isolated agent sessions.

```
hermes gateway install     # Install as a user servicesudo hermes gateway install --system   # Linux: boot-time system service for servershermes gateway             # Or run in foregroundhermes cron listhermes cron status
```

### Gateway scheduler behavior​

On each tick Hermes:

1. loads jobs from~/.hermes/cron/jobs.json
2. checksnext_run_atagainst the current time
3. starts a freshAIAgentsession for each due job
4. optionally injects one or more attached skills into that fresh session
5. runs the prompt to completion
6. delivers the final response
7. updates run metadata and the next scheduled time

`~/.hermes/cron/jobs.json`
`next_run_at`
`AIAgent`

A file lock at~/.hermes/cron/.tick.lockprevents overlapping scheduler ticks from double-running the same job batch.

`~/.hermes/cron/.tick.lock`

## Delivery options​

When scheduling jobs, you specify where the output goes:

| Option | Description | Example |
| --- | --- | --- |
| "origin" | Back to where the job was created | Default on messaging platforms |
| "local" | Save to local files only (~/.hermes/cron/output/) | Default on CLI |
| "telegram" | Telegram home channel | UsesTELEGRAM_HOME_CHANNEL |
| "telegram:123456" | Specific Telegram chat by ID | Direct delivery |
| "telegram:-100123:17585" | Specific Telegram topic | chat_id:thread_idformat |
| "discord" | Discord home channel | UsesDISCORD_HOME_CHANNEL |
| "discord:#engineering" | Specific Discord channel | By channel name |
| "slack" | Slack home channel |  |
| "whatsapp" | WhatsApp home |  |
| "signal" | Signal |  |
| "matrix" | Matrix home room |  |
| "mattermost" | Mattermost home channel |  |
| "email" | Email |  |
| "sms" | SMS via Twilio |  |
| "homeassistant" | Home Assistant |  |
| "dingtalk" | DingTalk |  |
| "feishu" | Feishu/Lark |  |
| "wecom" | WeCom |  |
| "weixin" | Weixin (WeChat) |  |
| "bluebubbles" | BlueBubbles (iMessage) |  |
| "qqbot" | QQ Bot (Tencent QQ) |  |
| "all" | Fan out to every connected home channel | Resolved at fire time |
| "telegram,discord" | Fan out to a specific set of channels | Comma-separated list |
| "origin,all" | Deliver to the originplusevery other connected channel | Combine any tokens |

`"origin"`
`"local"`
`~/.hermes/cron/output/`
`"telegram"`
`TELEGRAM_HOME_CHANNEL`
`"telegram:123456"`
`"telegram:-100123:17585"`
`chat_id:thread_id`
`"discord"`
`DISCORD_HOME_CHANNEL`
`"discord:#engineering"`
`"slack"`
`"whatsapp"`
`"signal"`
`"matrix"`
`"mattermost"`
`"email"`
`"sms"`
`"homeassistant"`
`"dingtalk"`
`"feishu"`
`"wecom"`
`"weixin"`
`"bluebubbles"`
`"qqbot"`
`"all"`
`"telegram,discord"`
`"origin,all"`

The agent's final response is automatically delivered to the configureddeliver:target — the agent does not send messages itself, so there is nothing to call in the cron prompt.

`deliver:`

### Routing intent (all)​

`all`

alllets you ship one cron job to every messaging channel you have configured, without having to enumerate them by name. It isresolved at fire time, so a job created before you wired up Telegram will pick up Telegram on the next tick after you setTELEGRAM_HOME_CHANNEL.

`all`
`TELEGRAM_HOME_CHANNEL`

Semantics:allexpands to every platform with a configured home channel. Zero is fine; the job simply produces no delivery targets and is recorded as a delivery failure upstream.

`all`

allcomposes with explicit targets.origin,alldelivers to the origin chatplusevery other connected home channel, de-duplicating by(platform, chat_id, thread_id).

`all`
`origin,all`
`(platform, chat_id, thread_id)`

### Telegram cron topic (TELEGRAM_CRON_THREAD_ID)​

`TELEGRAM_CRON_THREAD_ID`

When Telegram topic mode is enabled, the root DM is reserved as a system lobby — replies sent there are rebuffed with a lobby reminder andreply_to_message_idis dropped, so you cannot reply to a cron message that landed in the main chat.

`reply_to_message_id`

Point cron at a dedicated forum topic instead:

1. In Telegram, open the bot DM and create a topic named e.g.Cron. Long-press the topic header →Copy link; the trailing integer is the topic'smessage_thread_id.
2. SetTELEGRAM_CRON_THREAD_ID=<that id>in your.env.

`Cron`
`message_thread_id`
`TELEGRAM_CRON_THREAD_ID=<that id>`
`.env`

This applies only to cron deliveries.TELEGRAM_HOME_CHANNEL_THREAD_ID(used elsewhere, e.g. restart notifications) is unchanged. Explicitdeliver="telegram:chat_id:thread_id"targets continue to win over the env var. Replies to cron messages now arrive in the existing topic session, so you can act on them directly.

`TELEGRAM_HOME_CHANNEL_THREAD_ID`
`deliver="telegram:chat_id:thread_id"`

### Response wrapping​

By default, delivered cron output is wrapped with a header and footer so the recipient knows it came from a scheduled task:

```
Cronjob Response: Morning feeds-------------<agent output here>Note: The agent cannot see this message, and therefore cannot respond to it.
```

To deliver the raw agent output without the wrapper, setcron.wrap_responsetofalse:

`cron.wrap_response`
`false`

```
# ~/.hermes/config.yamlcron:  wrap_response: false
```

### Continuable jobs (reply to a cron delivery)​

By default a cron delivery is fire-and-forget: the message is sent, but it does
not live in the chat's conversation history, so if you reply to it the agent
has no record of what it said. Set a jobcontinuableand the delivered brief
becomes a conversation you can reply into — the agent has the brief in context
instead of asking "what is Task #2?".

Opt-in,default off. Enable globally in config, or per-job via thecronjobtool'sattach_to_session(which overrides the global setting for that one job):

`cronjob`
`attach_to_session`

```
# ~/.hermes/config.yamlcron:  mirror_delivery: false   # set true to make cron deliveries continuable
```

Behaviour isthread-preferred, scoped to the job's origin chat:

- Thread-capable platforms(Telegram topics, Discord/Slack threads): each
delivery opens its own dedicated thread and the brief is seeded into that
thread's session, so a reply in-thread continues with full context. A
recurring job (e.g. a daily brief) opens a fresh thread per run, keeping each
delivery's follow-up discussion isolated.
- DM-only platforms(WhatsApp, Signal, SMS): no threads exist, so the brief
is mirrored into the origin DM session instead — the DM itself is the
continuation surface.

Only the origin chat is ever touched: fan-out / broadcast targets (all,
explicit other-chat deliveries) are never made continuable. The mirror is
written as a labelled user turn ([Cron delivery: <task name>]), which keeps
the conversation history alternation-safe across all model providers.

`all`
`[Cron delivery: <task name>]`

#### Flat, in-channel continuation (Slack)​

The thread-preferred behaviour above mints a dedicated thread on every
delivery. If you'd rather have a continuable job landflat in the channel
timeline— no thread — set the Slackcontinuable surfacetoin_channel:

`in_channel`

```
# ~/.hermes/config.yamlslack:  cron_continuable_surface: in_channel   # default: thread  reply_in_thread: false                 # required pairing (see below)  require_mention: false                 # so a plain reply continues the job
```

Inin_channelmode the brief is delivered as an ordinary top-level channel
message (no thread is opened), and your reply continues the job via the
channel's shared session. Three settings work together:

`in_channel`
- cron_continuable_surface: in_channel— skips thread creation on delivery.
- reply_in_thread: false(required) — makes the bot answer your replyflatin the channel and key it to the same whole-channel session the brief
was seeded into. Without it the continuation still works but arrives in a
thread (it falls back safely to thread-style continuation, never a dropped
reply — the gateway logs a warning at startup so you can spot the mismatch).
- require_mention: false(or add the channel tofree_response_channels)
— so you can reply with a plain message; otherwise the bot only wakes when you@-mention it on each reply.

`cron_continuable_surface: in_channel`
`reply_in_thread: false`
`require_mention: false`
`free_response_channels`
`@`

Because the continuation is thewhole-channelsession, it is shared: other
chatter in the channel — and a second continuable in-channel job — join the same
rolling conversation. That is inherent to "flat in a channel" and is the same
tradeoffreply_in_thread: falseusers already accept; use the defaultthreadsurface when you want each delivery's follow-up isolated.

`reply_in_thread: false`
`thread`

This is a Slack capability today. Other platforms accept the key but fall back
to thethreadsurface (their continuation primitives differ); the choice is
per-platform, set under each platform's config. It's a gateway-side config flag
— a/restartpicks it up; no Slack app reinstall is needed.

`thread`
`/restart`

cron_continuable_surfaceis achannelsetting — a 1:1 DM has no
thread-vs-timeline split to choose between (the DM is already flat), so the key
has no effect there. What governs whether a DM cron delivery is continuable is
the separate, pre-existing knobslack.dm_top_level_threads_as_sessions:

`cron_continuable_surface`
`slack.dm_top_level_threads_as_sessions`
- false— all top-level DMs share one rolling DM session, so a continuable
cron brief and your reply land in thesamesession and the job continues in
context. This is what you want for continuable cron in a DM.
- true(default) — each top-level DM message is its own session, so a reply
to a delivered brief starts afreshsession that has no record of the brief.
Continuation does not work in this mode (for cron or any other flat delivery).

`false`
`true`

So for a continuable cron job delivered to a 1:1 DM, setslack.dm_top_level_threads_as_sessions: false.cron_continuable_surfaceis
not required (and is ignored) for DMs.

`slack.dm_top_level_threads_as_sessions: false`
`cron_continuable_surface`

### Silent suppression​

If the agent's final response contains[SILENT], delivery is suppressed entirely. The output is still saved locally for audit (in~/.hermes/cron/output/), but no message is sent to the delivery target.

`[SILENT]`
`~/.hermes/cron/output/`

This is useful for monitoring jobs that should only report when something is wrong:

```
Check if nginx is running. If everything is healthy, respond with only [SILENT].Otherwise, report the issue.
```

Failed jobs always deliver regardless of the[SILENT]marker — only successful runs can be silenced. For quiet monitoring jobs, prompt the agent to reply with only[SILENT]when there is nothing to report.

`[SILENT]`
`[SILENT]`

## Script timeout​

Pre-run scripts (attached via thescriptparameter) have a default timeout of 3600 seconds (1 hour). This bounds thescript only— skill-based / LLM-driven jobs run on a separate inactivity budget and are not capped by this value. If your scripts need a different limit, you can change it:

`script`

```
# ~/.hermes/config.yamlcron:  script_timeout_seconds: 1800   # 30 minutes
```

Or set theHERMES_CRON_SCRIPT_TIMEOUTenvironment variable. The resolution order is: env var → config.yaml → 3600s default.

`HERMES_CRON_SCRIPT_TIMEOUT`

## No-agent mode (script-only jobs)​

For recurring jobs that don't need LLM reasoning — classic watchdogs, disk/memory alerts, heartbeats, CI pings — passno_agent=Trueat creation time. The scheduler runs your script on schedule and delivers its stdout directly, skipping the agent entirely:

`no_agent=True`

```
hermes cron create "every 5m" \  --no-agent \  --script memory-watchdog.sh \  --deliver telegram \  --name "memory-watchdog"
```

Semantics:

- Script stdout (trimmed) → delivered verbatim as the message.
- Empty stdout → silent tick, no delivery. This is the watchdog pattern: "only say something when something is wrong".
- Non-zero exit or timeout → an error alert is delivered, so a broken watchdog can't fail silently.
- {"wakeAgent": false}on the last line → silent tick (same gate LLM jobs use).
- No tokens, no model, no provider fallback — the job never touches the inference layer.

`{"wakeAgent": false}`

.sh/.bashfiles run under/bin/bash; anything else under the current Python interpreter (sys.executable). Scripts must live in~/.hermes/scripts/(same sandboxing rule as the pre-run script gate).

`.sh`
`.bash`
`/bin/bash`
`sys.executable`
`~/.hermes/scripts/`

### The agent sets these up for you​

Thecronjobtool's schema exposesno_agentto Hermes directly, so you can describe a watchdog in chat and let the agent wire it up:

`cronjob`
`no_agent`

```
Ping me on Telegram if RAM is over 85%, every 5 minutes.
```

Hermes will write the check script to~/.hermes/scripts/viawrite_file, then call:

`~/.hermes/scripts/`
`write_file`

```
cronjob(action="create", schedule="every 5m",        script="memory-watchdog.sh", no_agent=True,        deliver="telegram", name="memory-watchdog")
```

It picksno_agent=Trueautomatically when the message content is fully determined by the script (watchdogs, threshold alerts, heartbeats). The same tool also lets the agent pause, resume, edit, and remove jobs — so the whole lifecycle is chat-driven without anyone touching the CLI.

`no_agent=True`

See theScript-Only Cron Jobs guidefor worked examples.

## Chaining jobs withcontext_from​

`context_from`

Cron jobs run in isolated sessions with no memory of previous runs. But sometimes one job's output is exactly what the next job needs. Thecontext_fromparameter wires that connection automatically — Job B's prompt gets Job A's most recent output prepended as context at runtime.

`context_from`

```
# Job 1: Collect raw datacronjob(    action="create",    prompt="Fetch the top 10 AI/ML stories from Hacker News. Save them to ~/.hermes/data/briefs/raw.md in markdown format with title, URL, and score.",    schedule="0 7 * * *",    name="AI News Collector",)# Job 2: Triage — receives Job 1's output as context# Get Job 1's ID from: cronjob(action="list")cronjob(    action="create",    prompt="Read ~/.hermes/data/briefs/raw.md. Score each story 1–10 for engagement potential and novelty. Output the top 5 to ~/.hermes/data/briefs/ranked.md.",    schedule="30 7 * * *",    context_from="<job1_id>",    name="AI News Triage",)# Job 3: Ship — receives Job 2's output as contextcronjob(    action="create",    prompt="Read ~/.hermes/data/briefs/ranked.md. Write 3 tweet drafts (hook + body + hashtags). Deliver to telegram:7976161601.",    schedule="0 8 * * *",    context_from="<job2_id>",    name="AI News Brief",)
```

How it works:

- When Job 2 fires, Hermes reads Job 1's most recent output from~/.hermes/cron/output/{job1_id}/*.md
- That output is prepended to Job 2's prompt automatically
- Job 2 doesn't need to hardcode "read this file" — it receives the content as context
- The chain can be any length: Job 1 → Job 2 → Job 3 → ...

`~/.hermes/cron/output/{job1_id}/*.md`

Whatcontext_fromaccepts:

`context_from`
| Format | Example |
| --- | --- |
| Single job ID (string) | context_from="a1b2c3d4" |
| Multiple job IDs (list) | context_from=["job_a", "job_b"] |

`context_from="a1b2c3d4"`
`context_from=["job_a", "job_b"]`

Outputs are concatenated in the order listed.

When to use it:

- Multi-stage pipelines (collect → filter → format → deliver)
- Dependent tasks where step N's work depends on step N−1's output
- Fan-out/fan-in patterns where one job aggregates results from several others

## Provider recovery​

Cron jobs inherit your configured fallback providers and credential pool rotation. If the primary API key is rate-limited or the provider returns an error, the cron agent can:

- Fall back to an alternate providerif you havefallback_providers(or the legacyfallback_model) configured inconfig.yaml
- Rotate to the next credentialin yourcredential poolfor the same provider

`fallback_providers`
`fallback_model`
`config.yaml`

This means cron jobs that run at high frequency or during peak hours are more resilient — a single rate-limited key won't fail the entire run.

## Schedule formats​

The agent's final response is automatically delivered to the job'sdeliver:target — the agent no longer fires messages itself, so the user-facing content simply goes in the final response. To deliver toadditional or differenttargets, list multipledeliver:targets on the cron job (comma-separated, e.g.deliver: "telegram,discord") rather than having the agent send them.

`deliver:`
`deliver:`
`deliver: "telegram,discord"`

### Relative delays (one-shot)​

```
30m     → Run once in 30 minutes2h      → Run once in 2 hours1d      → Run once in 1 day
```

### Intervals (recurring)​

```
every 30m    → Every 30 minutesevery 2h     → Every 2 hoursevery 1d     → Every day
```

### Cron expressions​

```
0 9 * * *       → Daily at 9:00 AM0 9 * * 1-5     → Weekdays at 9:00 AM0 */6 * * *     → Every 6 hours30 8 1 * *      → First of every month at 8:30 AM0 0 * * 0       → Every Sunday at midnight
```

### ISO timestamps​

```
2026-03-15T09:00:00    → One-time at March 15, 2026 9:00 AM
```

## Repeat behavior​

| Schedule type | Default repeat | Behavior |
| --- | --- | --- |
| One-shot (30m, timestamp) | 1 | Runs once |
| Interval (every 2h) | forever | Runs until removed |
| Cron expression | forever | Runs until removed |

`30m`
`every 2h`

You can override it:

```
cronjob(    action="create",    prompt="...",    schedule="every 2h",    repeat=5,)
```

## Managing jobs programmatically​

The agent-facing API is one tool:

```
cronjob(action="create", ...)cronjob(action="list")cronjob(action="update", job_id="...")cronjob(action="pause", job_id="...")cronjob(action="resume", job_id="...")cronjob(action="run", job_id="...")cronjob(action="remove", job_id="...")
```

Forupdate, passskills=[]to remove all attached skills.

`update`
`skills=[]`

## Toolsets available to cron jobs​

Cron runs each job in a fresh agent session with no chat platform attached. By default the cron agent getsthe toolset you configured for thecronplatform inhermes tools— not the CLI default, not everything under the sun.

`cron`
`hermes tools`

```
hermes tools# → pick the "cron" platform in the curses UI# → toggle toolsets on/off just like you would for Telegram/Discord/etc.
```

Tighter per-job control is available via theenabled_toolsetsfield oncronjob.create(or on an existing job viacronjob.update):

`enabled_toolsets`
`cronjob.create`
`cronjob.update`

```
cronjob(action="create", name="weekly-news-summary",        schedule="every sunday 9am",        enabled_toolsets=["web", "file"],      # just web + file, no terminal/browser/etc.        prompt="Summarize this week's AI news: ...")
```

Whenenabled_toolsetsis set on a job it wins; otherwise thehermes toolscron-platform config wins; otherwise Hermes falls back to the built-in defaults. This matters for cost control: carryingbrowser,delegationinto every tiny "fetch news" job bloats the tool-schema prompt on every LLM call.

`enabled_toolsets`
`hermes tools`
`browser`
`delegation`

### Skipping the agent entirely:wakeAgent​

`wakeAgent`

If your cron job attaches a pre-check script (viascript=), the script can decide at runtime whether Hermes should even invoke the agent. Emit a final stdout line of the form:

`script=`

```
{"wakeAgent": false}
```

…and cron skips the agent run entirely for this tick. Useful for frequent polls (every 1–5 min) that only need to wake the LLM when state actually changed — otherwise you pay for zero-content agent turns over and over.

```
# pre-check scriptimport json, syslatest = fetch_latest_issue_count()prev = read_state("issue_count")if latest == prev:    print(json.dumps({"wakeAgent": False}))   # skip this tick    sys.exit(0)write_state("issue_count", latest)print(json.dumps({"wakeAgent": True, "context": {"new_issues": latest - prev}}))
```

WhenwakeAgentis omitted, the default istrue(wake the agent as usual).

`wakeAgent`
`true`

#### Recipes: cheap pre-run gates​

ThewakeAgentgate gives you a $0 way to decide whether a scheduled job should spend any LLM tokens at all. Three patterns cover most use cases.

`wakeAgent`

File-change gate— only run when a watched file has new content since the last successful tick. The scheduler records each job'slast_run_at; compare it against the file's mtime.

`last_run_at`

```
#!/bin/bash# ~/.hermes/scripts/feed-changed.shFEED="$HOME/data/feed.json"STATE="$HOME/.hermes/scripts/.feed-changed.last"test -f "$FEED" || { echo '{"wakeAgent": false}'; exit 0; }mtime=$(stat -c %Y "$FEED")last=$(cat "$STATE" 2>/dev/null || echo 0)if [ "$mtime" -le "$last" ]; then  echo '{"wakeAgent": false}'else  echo "$mtime" > "$STATE"  echo '{"wakeAgent": true}'fi
```

```
cronjob(action="create", name="process-feed",        schedule="every 30m",        script="feed-changed.sh",        prompt="A new ~/data/feed.json has landed. Summarize what changed.")
```

External-flag gate— only run when some other process has signalled readiness (e.g. a deploy hook drops a file, a CI job sets a value in your state store).

```
#!/bin/bash# ~/.hermes/scripts/flag-ready.shif test -f /tmp/new-data-ready; then  rm -f /tmp/new-data-ready  echo '{"wakeAgent": true}'else  echo '{"wakeAgent": false}'fi
```

```
cronjob(action="create", name="nightly-analysis",        schedule="0 9 * * *",        script="flag-ready.sh",        prompt="Run the nightly analysis over today's batch.")
```

SQL-count gate— only run when there are new rows to process in your own database. The script can also pass the count through to the agent viacontext, so the agent knows how much it's looking at without re-querying.

`context`

```
#!/usr/bin/env python# ~/.hermes/scripts/new-rows.pyimport json, sqlite3conn = sqlite3.connect("/home/me/data/app.db")n = conn.execute(    "SELECT COUNT(*) FROM messages WHERE ts > strftime('%s','now','-2 hours')").fetchone()[0]if n < 1:    print(json.dumps({"wakeAgent": False}))else:    print(json.dumps({"wakeAgent": True, "context": {"new_rows": n}}))
```

```
cronjob(action="create", name="summarize-new-msgs",        schedule="every 2h",        script="new-rows.py",        prompt="Summarize the new messages from the last 2 hours.")
```

The same pattern works for any data source you can query from a script — Postgres, an HTTP API, your own state store — without baking a SQL evaluator into the cron subsystem.

Hermes's own~/.hermes/state.dbis an internal schema that changes between releases. Don't query it from a pre-run gate — point at your own database or feed instead.

`~/.hermes/state.db`

Credit: this recipe set was prompted by @iankar8's exploration in#2654, which proposed adding sql/file/command triggers as a parallel mechanism. Thescript+wakeAgentgate already covers all three cases at $0, so the work landed as documentation instead.

`script`
`wakeAgent`

### Chaining jobs:context_from​

`context_from`

A cron job can consume the most recent successful output of one or more other jobs by listing their names (or IDs) incontext_from:

`context_from`

```
cronjob(action="create", name="daily-digest",        schedule="every day 7am",        context_from=["ai-news-fetch", "github-prs-fetch"],        prompt="Write the daily digest using the outputs above.")
```

The referenced jobs' most recent completed outputs are injected above the prompt as context for this run. Each upstream entry must be a valid job ID or name (seecronjob action="list"). Note: chaining reads themost recent completedoutput — it does not wait for upstream jobs that are running in the same tick.

`cronjob action="list"`

## Job storage​

Jobs are stored in~/.hermes/cron/jobs.json. Output from job runs is saved to~/.hermes/cron/output/{job_id}/{timestamp}.md.

`~/.hermes/cron/jobs.json`
`~/.hermes/cron/output/{job_id}/{timestamp}.md`

Jobs may storemodelandproviderasnull. When those fields are omitted, Hermes resolves them at execution time from the global configuration. They only appear in the job record when a per-job override is set.

`model`
`provider`
`null`

The storage uses atomic file writes so interrupted writes do not leave a partially written job file behind.

## Self-contained prompts still matter​

Cron jobs run in a completely fresh agent session. The prompt must contain everything the agent needs that is not already provided by attached skills.

BAD:"Check on that server issue"

`"Check on that server issue"`

GOOD:"SSH into server 192.168.1.100 as user 'deploy', check if nginx is running with 'systemctl status nginx', and verify https://example.com returns HTTP 200."

`"SSH into server 192.168.1.100 as user 'deploy', check if nginx is running with 'systemctl status nginx', and verify https://example.com returns HTTP 200."`

## Security​

Scheduled task prompts are scanned for prompt-injection and credential-exfiltration patterns at creation and update time. Prompts containing invisible Unicode tricks, SSH backdoor attempts, or obvious secret-exfiltration payloads are blocked.