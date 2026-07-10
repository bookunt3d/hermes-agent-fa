---
layout: docs
title: "جزئیات داخلی Cron"
permalink: /docs/developer-guide/cron-internals/
---

- 
- Developer Guide
- Internals
- Cron Internals

# Cron Internals

The cron subsystem provides scheduled task execution — from simple one-shot delays to recurring cron-expression jobs with skill injection and cross-platform delivery.

## Key Files​

| File | Purpose |
| --- | --- |
| cron/jobs.py | Job model, storage, atomic read/write tojobs.json |
| cron/scheduler.py | Scheduler loop — due-job detection, execution, repeat tracking |
| tools/cronjob_tools.py | Model-facingcronjobtool registration and handler |
| gateway/run.py | Gateway integration — cron ticking in the long-running loop |
| hermes_cli/cron.py | CLIhermes cronsubcommands |

`cron/jobs.py`
`jobs.json`
`cron/scheduler.py`
`tools/cronjob_tools.py`
`cronjob`
`gateway/run.py`
`hermes_cli/cron.py`
`hermes cron`

## Scheduling Model​

Four schedule formats are supported:

| Format | Example | Behavior |
| --- | --- | --- |
| Relative delay | 30m,2h,1d | One-shot, fires after the specified duration |
| Interval | every 2h,every 30m | Recurring, fires at regular intervals |
| Cron expression | 0 9 * * * | Standard 5-field cron syntax (minute, hour, day, month, weekday) |
| ISO timestamp | 2025-01-15T09:00:00 | One-shot, fires at the exact time |

`30m`
`2h`
`1d`
`every 2h`
`every 30m`
`0 9 * * *`
`2025-01-15T09:00:00`

The model-facing surface is a singlecronjobtool with action-style operations:create,list,update,pause,resume,run,remove.

`cronjob`
`create`
`list`
`update`
`pause`
`resume`
`run`
`remove`

## Job Storage​

Jobs are stored in~/.hermes/cron/jobs.jsonwith atomic write semantics (write to temp file, then rename). Each job record contains:

`~/.hermes/cron/jobs.json`

```
{  "id": "a1b2c3d4e5f6",  "name": "Daily briefing",  "prompt": "Summarize today's AI news and funding rounds",  "schedule": {    "kind": "cron",    "expr": "0 9 * * *",    "display": "0 9 * * *"  },  "skills": ["ai-funding-daily-report"],  "deliver": "telegram:-1001234567890",  "repeat": {    "times": null,    "completed": 42  },  "state": "scheduled",  "enabled": true,  "next_run_at": "2025-01-16T09:00:00Z",  "last_run_at": "2025-01-15T09:00:00Z",  "last_status": "ok",  "created_at": "2025-01-01T00:00:00Z",  "model": null,  "provider": null,  "script": null}
```

### Job Lifecycle States​

| State | Meaning |
| --- | --- |
| scheduled | Active, will fire at next scheduled time |
| paused | Suspended — won't fire until resumed |
| completed | Repeat count exhausted or one-shot that has fired |
| running | Currently executing (transient state) |

`scheduled`
`paused`
`completed`
`running`

### Backward Compatibility​

Older jobs may have a singleskillfield instead of theskillsarray. The scheduler normalizes this at load time — singleskillis promoted toskills: [skill].

`skill`
`skills`
`skill`
`skills: [skill]`

## Scheduler Runtime​

### Tick Cycle​

The scheduler runs on a periodic tick (default: every 60 seconds):

```
tick()  1. Acquire scheduler lock (prevents overlapping ticks)  2. Load all jobs from jobs.json  3. Filter to due jobs (next_run <= now AND state == "scheduled")  4. For each due job:     a. Set state to "running"     b. Create fresh AIAgent session (no conversation history)     c. Load attached skills in order (injected as user messages)     d. Run the job prompt through the agent     e. Deliver the response to the configured target     f. Update run_count, compute next_run     g. If repeat count exhausted → state = "completed"     h. Otherwise → state = "scheduled"  5. Write updated jobs back to jobs.json  6. Release scheduler lock
```

### Gateway Integration​

In gateway mode, the crontrigger(the part that decideswhena due job
fires — "Axis B") is selected through a pluggableCronSchedulerprovider. The
gateway callsresolve_cron_scheduler()(cron/scheduler_provider.py) and runs
the resolved provider'sstart()in a dedicated background thread, alongside a
separate gateway-housekeeping thread.

`CronScheduler`
`resolve_cron_scheduler()`
`cron/scheduler_provider.py`
`start()`

The active provider is chosen by thecron.providerconfig key:

`cron.provider`
- empty (default)→ the built-inInProcessCronScheduler, which runs the
historical in-process loop callingscheduler.tick()every 60 seconds. This
is byte-identical to the pre-provider behavior.
- a named provider(e.g.chronos, a managed-cron provider for
scale-to-zero deployments) → discovered fromplugins/cron/<name>/or$HERMES_HOME/plugins/<name>/.

`InProcessCronScheduler`
`scheduler.tick()`
`chronos`
`plugins/cron/<name>/`
`$HERMES_HOME/plugins/<name>/`

If a named provider is missing, fails to load, or reportsis_available() == False, the resolver falls back to the built-in with a warning —cron is
never left without a trigger.The built-in provider lives in core
(cron/scheduler_provider.py), not inplugins/, so the fallback can't be
accidentally removed.

`is_available() == False`
`cron/scheduler_provider.py`
`plugins/`

What "firing"means(job execution + delivery) is unchanged and shared by all
providers — it stays inscheduler.run_job()/scheduler._deliver_result().
A provider only controls the trigger, never execution.

`scheduler.run_job()`
`scheduler._deliver_result()`

In CLI mode, cron jobs only fire whenhermes croncommands are run or during active CLI sessions.

`hermes cron`

### Managed cron (Chronos) for scale-to-zero​

Hosted gateways can run theChronosprovider (cron.provider: chronos)
instead of the built-in ticker. Chronos lets an idle gatewayscale to zeroand still fire cron jobs: rather than a 60-second in-process loop (which would
keep the process awake), it asks Nous infrastructure to arm exactlyone
managed one-shot per job at that job's real next-fire time. At fire time Nous
calls the gateway back over an authenticated webhook (POST /api/cron/fire);
the gateway runs the job through the samerun_one_jobpath as the built-in,
then re-arms the next one-shot. Between fires the process can be fully stopped —
it wakes only on a genuine fire, never on a periodic timer.

`cron.provider: chronos`
`POST /api/cron/fire`
`run_one_job`

The flow (the managed scheduler is provided by Nous; the agent holds no
scheduler credentials):

```
create/update a cron job  → Chronos asks Nous to arm a one-shot at the job's next_run_at      (authenticated with the agent's existing Nous token)  → at fire time Nous calls the gateway: POST {callback_url}/api/cron/fire      (authenticated with a short-lived, purpose-scoped Nous-minted JWT)  → the gateway verifies the token, claims the job (store compare-and-set so    multi-replica deployments fire at-most-once), runs it, and re-arms the next    one-shot
```

Config (all non-secret; on hosted agents Nous sets these at provision time):

| key | meaning |
| --- | --- |
| cron.provider | chronosto activate (empty = built-in ticker) |
| cron.chronos.portal_url | Nous base URL (arming + the fire-token issuer) |
| cron.chronos.callback_url | the gateway's own public base URL for inbound fires |
| cron.chronos.expected_audience | this agent's fire-token audience |
| cron.chronos.nas_jwks_url | key set for verifying the inbound fire token |

`cron.provider`
`chronos`
`cron.chronos.portal_url`
`cron.chronos.callback_url`
`cron.chronos.expected_audience`
`cron.chronos.nas_jwks_url`

If Chronos is misconfigured or the agent isn't logged into Nous,resolve_cron_scheduler()falls back to the built-in ticker (logged warning) —
cron never loses its trigger. Recurring jobs re-arm after each fire;repeat-N
jobs stop cleanly when the count is exhausted (no orphaned one-shot). The full
agent↔Nous wire contract lives indocs/chronos-managed-cron-contract.md.

`resolve_cron_scheduler()`
`repeat`
`docs/chronos-managed-cron-contract.md`

### Fresh Session Isolation​

Each cron job runs in a completely fresh agent session:

- No conversation history from previous runs
- No memory of previous cron executions (unless persisted to memory/files)
- The prompt must be self-contained — cron jobs cannot ask clarifying questions
- Thecronjobtoolset is disabled (recursion guard)

`cronjob`

## Skill-Backed Jobs​

A cron job can attach one or more skills via theskillsfield. At execution time:

`skills`
1. Skills are loaded in the specified order
2. Each skill's SKILL.md content is injected as context
3. The job's prompt is appended as the task instruction
4. The agent processes the combined skill context + prompt

This enables reusable, tested workflows without pasting full instructions into cron prompts. For example:

```
Create a daily funding report → attach "ai-funding-daily-report" skill
```

### Script-Backed Jobs​

Jobs can also attach a Python script via thescriptfield. The script runsbeforeeach agent turn, and its stdout is injected into the prompt as context. This enables data collection and change detection patterns:

`script`

```
# ~/.hermes/scripts/check_competitors.pyimport requests, json# Fetch competitor release notes, diff against last run# Print summary to stdout — agent analyzes and reports
```

The script timeout defaults to 3600 seconds (1 hour)._get_script_timeout()resolves the limit through a three-layer chain:

`_get_script_timeout()`
1. Module-level override—_SCRIPT_TIMEOUT(for tests/monkeypatching). Only used when it differs from the default.
2. Environment variable—HERMES_CRON_SCRIPT_TIMEOUT
3. Config—cron.script_timeout_secondsinconfig.yaml(read viaload_config())
4. Default— 3600 seconds (1 hour)

`_SCRIPT_TIMEOUT`
`HERMES_CRON_SCRIPT_TIMEOUT`
`cron.script_timeout_seconds`
`config.yaml`
`load_config()`

This timeout bounds thepre-run script only, not the agent. Skill-based / LLM-driven jobs run on a separateinactivity-based budget (HERMES_CRON_TIMEOUT, default 600s of idle time,0= unlimited) — they can run for hours as long as they keep calling tools or streaming tokens, and are only killed after the configured idle period with no activity. Scripts are dispatched to a persistent thread pool (not held under the tick lock), so a long-running script does not block other due jobs from firing.

`HERMES_CRON_TIMEOUT`
`0`

### Provider Recovery​

run_job()passes the user's configured fallback providers and credential pool into theAIAgentinstance:

`run_job()`
`AIAgent`
- Fallback providers— readsfallback_providers(list) orfallback_model(legacy dict) fromconfig.yaml, matching the gateway's_load_fallback_model()pattern. Passed asfallback_model=toAIAgent.__init__, which normalizes both formats into a fallback chain.
- Credential pool— loads viaload_pool(provider)fromagent.credential_poolusing the resolved runtime provider name. Only passed when the pool has credentials (pool.has_credentials()). Enables same-provider key rotation on 429/rate-limit errors.

`fallback_providers`
`fallback_model`
`config.yaml`
`_load_fallback_model()`
`fallback_model=`
`AIAgent.__init__`
`load_pool(provider)`
`agent.credential_pool`
`pool.has_credentials()`

This mirrors the gateway's behavior — without it, cron agents would fail on rate limits without attempting recovery.

## Delivery Model​

Cron job results can be delivered to any supported platform.

A bare platform name (slack,telegram, …) delivers to that platform's configuredhome channel. To target aspecificdestination instead, append a target after a colon:platform:<target>. The target is resolved at fire time (not when the job is created), so a job can name a destination on a platform that isn't connected yet and start delivering once it comes online.

`slack`
`telegram`
`platform:<target>`

Most platforms also accept an optional thread/topic as a third segment:platform:<chat_id>:<thread_id>.

`platform:<chat_id>:<thread_id>`
| Target | Syntax | Example |
| --- | --- | --- |
| Origin chat | origin | Deliver to the chat where the job was created |
| Local file | local | Save to~/.hermes/cron/output/ |
| Telegram | telegram,telegram:<chat_id>,telegram:<chat_id>:<thread_id>,telegram:@username | telegram:-1001234567890:17585 |
| Discord | discord,discord:#channel,discord:<channel_id>,discord:<channel_id>:<thread_id> | discord:#engineering |
| Slack | slack,slack:#channel,slack:<channel_id>,slack:<channel_id>:<thread_ts> | slack:#engineering |
| Matrix | matrix,matrix:<!room_id:server>,matrix:<@user:server> | matrix:!abc123:example.org |
| Feishu | feishu,feishu:<chat_id>,feishu:<chat_id>:<thread_id> | feishu:oc_abc123def |
| WhatsApp | whatsapp,whatsapp:<jid>,whatsapp:+<E.164> | whatsapp:123456@g.us |
| Signal | signal,signal:group:<id>,signal:+<E.164> | signal:group:aBcD== |
| SMS | sms,sms:+<E.164> | sms:+<E.164 number> |
| Email | email,email:<address> | email:alerts@example.com |
| Weixin | weixin,weixin:<wxid> | weixin:wxid_abc123 |
| Mattermost | mattermostormattermost:<channel_id> | Bare name delivers to Mattermost home |
| Home Assistant | homeassistantorhomeassistant:<conversation> | Bare name delivers to HA conversation |
| DingTalk | dingtalkordingtalk:<chat_id> | Bare name delivers to DingTalk |
| WeCom | wecomorwecom:<chat_id> | Bare name delivers to WeCom |
| BlueBubbles | bluebubblesorbluebubbles:<chat_guid> | Bare name delivers to iMessage via BlueBubbles |
| QQ Bot | qqbotorqqbot:<chat_id> | Bare name delivers to QQ (Tencent) via Official API v2 |

`origin`
`local`
`~/.hermes/cron/output/`
`telegram`
`telegram:<chat_id>`
`telegram:<chat_id>:<thread_id>`
`telegram:@username`
`telegram:-1001234567890:17585`
`discord`
`discord:#channel`
`discord:<channel_id>`
`discord:<channel_id>:<thread_id>`
`discord:#engineering`
`slack`
`slack:#channel`
`slack:<channel_id>`
`slack:<channel_id>:<thread_ts>`
`slack:#engineering`
`matrix`
`matrix:<!room_id:server>`
`matrix:<@user:server>`
`matrix:!abc123:example.org`
`feishu`
`feishu:<chat_id>`
`feishu:<chat_id>:<thread_id>`
`feishu:oc_abc123def`
`whatsapp`
`whatsapp:<jid>`
`whatsapp:+<E.164>`
`whatsapp:123456@g.us`
`signal`
`signal:group:<id>`
`signal:+<E.164>`
`signal:group:aBcD==`
`sms`
`sms:+<E.164>`
`sms:+<E.164 number>`
`email`
`email:<address>`
`email:alerts@example.com`
`weixin`
`weixin:<wxid>`
`weixin:wxid_abc123`
`mattermost`
`mattermost:<channel_id>`
`homeassistant`
`homeassistant:<conversation>`
`dingtalk`
`dingtalk:<chat_id>`
`wecom`
`wecom:<chat_id>`
`bluebubbles`
`bluebubbles:<chat_guid>`
`qqbot`
`qqbot:<chat_id>`

Platforms in the first group have explicit, validated target syntax — named channels (#channel), topics/threads, room/user IDs, group IDs, or phone numbers. The remaining platforms accept the genericplatform:<chat_id>form (the value after the colon is used verbatim as the destination ID); a bare platform name always delivers to the home channel.

`#channel`
`platform:<chat_id>`

Named channels(slack:#engineering,discord:#engineering, or a friendly name likeslack:engineering) are resolved against the channel directory the gateway builds from connected adapters, so the gateway must have discovered the channel for name resolution to succeed; raw IDs (slack:C0123ABCD45) always work.

`slack:#engineering`
`discord:#engineering`
`slack:engineering`
`slack:C0123ABCD45`

ForTelegram topics, usetelegram:<chat_id>:<thread_id>(e.g.,telegram:-1001234567890:17585). ForSlack threads, the third segment is the parent message'sthread_ts(e.g.,slack:C0123ABCD45:1700000000.000100), so it only applies when replying under an existing message.

`telegram:<chat_id>:<thread_id>`
`telegram:-1001234567890:17585`
`thread_ts`
`slack:C0123ABCD45:1700000000.000100`

### Response Wrapping​

By default (cron.wrap_response: true), cron deliveries are wrapped with:

`cron.wrap_response: true`
- A header identifying the cron job name and task
- A footer noting the agent cannot see the delivered message in conversation

The[SILENT]prefix in a cron response suppresses delivery entirely — useful for jobs that only need to write to files or perform side effects.

`[SILENT]`

### Session Isolation​

Cron deliveries are NOT mirrored into gateway session conversation history. They exist only in the cron job's own session. This prevents message alternation violations in the target chat's conversation.

## Recursion Guard​

Cron-run sessions have thecronjobtoolset disabled. This prevents:

`cronjob`
- A scheduled job from creating new cron jobs
- Recursive scheduling that could explode token usage
- Accidental mutation of the job schedule from within a job

## Locking​

The scheduler uses cross-process file-based locking (fcntl.flockon Unix,msvcrt.lockingon Windows) to prevent overlapping ticks from executing the same due-job batch twice — even between the gateway's in-process ticker and a standalonehermes cron/ manualtick()call. If the lock cannot be acquired,tick()returns 0 immediately.

`fcntl.flock`
`msvcrt.locking`
`hermes cron`
`tick()`
`tick()`

## CLI Interface​

Thehermes cronCLI provides direct job management:

`hermes cron`

```
hermes cron list                    # Show all jobshermes cron create                  # Interactive job creation (alias: add)hermes cron edit <job_id>           # Edit job configurationhermes cron pause <job_id>          # Pause a running jobhermes cron resume <job_id>         # Resume a paused jobhermes cron run <job_id>            # Trigger immediate executionhermes cron remove <job_id>         # Delete a job
```

## Related Docs​

- Cron Feature Guide
- Gateway Internals
- Agent Loop Internals