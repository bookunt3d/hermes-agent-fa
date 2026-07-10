---
layout: docs
title: "عیب‌یابی Cron"
permalink: /docs/guides/cron-troubleshooting/
---

- 
- Guides & Tutorials
- Cron Troubleshooting

# Cron Troubleshooting

When a cron job isn't behaving as expected, work through these checks in order. Most issues fall into one of four categories: timing, delivery, permissions, or skill loading.

## Jobs Not Firing​

### Check 1: Verify the job exists and is active​

```
hermes cron list
```

Look for the job and confirm its state is[active](not[paused]or[completed]). If it shows[completed], the repeat count may be exhausted — edit the job to reset it.

`[active]`
`[paused]`
`[completed]`
`[completed]`

### Check 2: Confirm the schedule is correct​

A misformatted schedule silently defaults to one-shot or is rejected entirely. Test your expression:

| Your expression | Should evaluate to |
| --- | --- |
| 0 9 * * * | 9:00 AM every day |
| 0 9 * * 1 | 9:00 AM every Monday |
| every 2h | Every 2 hours from now |
| 30m | 30 minutes from now |
| 2025-06-01T09:00:00 | June 1, 2025 at 9:00 AM UTC |

`0 9 * * *`
`0 9 * * 1`
`every 2h`
`30m`
`2025-06-01T09:00:00`

If the job fires once and then disappears from the list, it's a one-shot schedule (30m,1d, or an ISO timestamp) — expected behavior.

`30m`
`1d`

### Check 3: Is the gateway running?​

Cron jobs are fired by the gateway's background ticker thread, which ticks every 60 seconds. A regular CLI chat session doesnotautomatically fire cron jobs.

If you're expecting jobs to fire automatically, you need a running gateway (hermes gatewayfor foreground, orhermes gateway startfor the installed service). For one-off debugging, you can manually trigger a tick withhermes cron tick.

`hermes gateway`
`hermes gateway start`
`hermes cron tick`

### Check 4: Check the system clock and timezone​

Jobs use the local timezone. If your machine's clock is wrong or in a different timezone than expected, jobs will fire at the wrong times. Verify:

```
datehermes cron list   # Compare next_run times with local time
```

## Delivery Failures​

### Check 1: Verify the deliver target is correct​

Delivery targets are case-sensitive and require the correct platform to be configured. A misconfigured target silently drops the response.

| Target | Requires |
| --- | --- |
| telegram | TELEGRAM_BOT_TOKENin~/.hermes/.env |
| discord | DISCORD_BOT_TOKENin~/.hermes/.env |
| slack | SLACK_BOT_TOKENin~/.hermes/.env |
| whatsapp | WhatsApp gateway configured |
| signal | Signal gateway configured |
| matrix | Matrix homeserver configured |
| email | SMTP configured inconfig.yaml |
| sms | SMS provider configured |
| local | Write access to~/.hermes/cron/output/ |
| origin | Delivers to the chat where the job was created |

`telegram`
`TELEGRAM_BOT_TOKEN`
`~/.hermes/.env`
`discord`
`DISCORD_BOT_TOKEN`
`~/.hermes/.env`
`slack`
`SLACK_BOT_TOKEN`
`~/.hermes/.env`
`whatsapp`
`signal`
`matrix`
`email`
`config.yaml`
`sms`
`local`
`~/.hermes/cron/output/`
`origin`

Other supported platforms includemattermost,homeassistant,dingtalk,feishu,wecom,weixin,bluebubbles,qqbot, andwebhook. You can also target a specific chat withplatform:chat_idsyntax (e.g.,telegram:-1001234567890).

`mattermost`
`homeassistant`
`dingtalk`
`feishu`
`wecom`
`weixin`
`bluebubbles`
`qqbot`
`webhook`
`platform:chat_id`
`telegram:-1001234567890`

If delivery fails, the job still runs — it just won't send anywhere. Checkhermes cron listfor updatedlast_errorfield (if available).

`hermes cron list`
`last_error`

### Check 2: Check[SILENT]usage​

`[SILENT]`

If your cron job produces no output, delivery is suppressed. If the agent response includes the cron quiet marker[SILENT], delivery is also suppressed. This is intentional for monitoring jobs — but make sure your prompt is not accidentally suppressing everything.

`[SILENT]`

Use prompts like "respond with only [SILENT] if nothing changed." Avoid asking the agent to include[SILENT]inside a longer explanation, because cron treats that marker as a suppression signal.

`[SILENT]`

### Check 3: Platform token permissions​

Each messaging platform bot needs specific permissions to receive messages. If delivery silently fails:

- Telegram: Bot must be an admin in the target group/channel
- Discord: Bot must have permission to send in the target channel
- Slack: Bot must be added to the workspace and havechat:writescope

`chat:write`

### Check 4: Response wrapping​

By default, cron responses are wrapped with a header and footer (cron.wrap_response: trueinconfig.yaml). Some platforms or integrations may not handle this well. To disable:

`cron.wrap_response: true`
`config.yaml`

```
cron:  wrap_response: false
```

## Skill Loading Failures​

### Check 1: Verify skills are installed​

```
hermes skills list
```

Skills must be installed before they can be attached to cron jobs. If a skill is missing, install it first withhermes skills install <skill-name>or via/skillsin the CLI.

`hermes skills install <skill-name>`
`/skills`

### Check 2: Check skill name vs. skill folder name​

Skill names are case-sensitive and must match the installed skill's folder name. If your job specifiesai-funding-daily-reportbut the skill folder isai-funding-daily-report, confirm the exact name fromhermes skills list.

`ai-funding-daily-report`
`ai-funding-daily-report`
`hermes skills list`

### Check 3: Skills that require interactive tools​

Cron jobs run with thecronjob,messaging, andclarifytoolsets disabled. This prevents recursive cron creation, direct message sending (delivery is handled by the scheduler), and interactive prompts. If a skill relies on these toolsets, it won't work in a cron context.

`cronjob`
`messaging`
`clarify`

Check the skill's documentation to confirm it works in non-interactive (headless) mode.

### Check 4: Multi-skill ordering​

When using multiple skills, they load in order. If Skill A depends on context from Skill B, make sure B loads first:

```
/cron add "0 9 * * *" "..." --skill context-skill --skill target-skill
```

In this example,context-skillloads beforetarget-skill.

`context-skill`
`target-skill`

## Job Errors and Failures​

### Check 1: Review recent job output​

If a job ran and failed, you may see error context in:

1. The chat where the job delivers (if delivery succeeded)
2. ~/.hermes/logs/agent.logfor scheduler messages (orerrors.logfor warnings)
3. The job'slast_runmetadata viahermes cron list

`~/.hermes/logs/agent.log`
`errors.log`
`last_run`
`hermes cron list`

### Check 2: Common error patterns​

"No such file or directory" for scriptsThescriptpath must be an absolute path (or relative to the Hermes config directory). Verify:

`script`

```
ls ~/.hermes/scripts/your-script.py   # Must existhermes cron edit <job_id> --script ~/.hermes/scripts/your-script.py
```

"Skill not found" at job executionThe skill must be installed on the machine running the scheduler. If you move between machines, skills don't automatically sync — reinstall them withhermes skills install <skill-name>.

`hermes skills install <skill-name>`

Job runs but delivers nothingLikely a delivery target issue (see Delivery Failures above), no output, or a response containing the cron quiet marker[SILENT].

`[SILENT]`

Job hangs or times outThe scheduler uses an inactivity-based timeout (default 600s, configurable viaHERMES_CRON_TIMEOUTenv var,0for unlimited). The agent can run as long as it's actively calling tools — the timer only fires after sustained inactivity. Long-running jobs should use scripts to handle data collection and deliver only the result.

`HERMES_CRON_TIMEOUT`
`0`

### Check 3: Lock contention​

The scheduler uses file-based locking to prevent overlapping ticks. If two gateway instances are running (or a CLI session conflicts with a gateway), jobs may be delayed or skipped.

Kill duplicate gateway processes:

```
ps aux | grep hermes# Kill duplicate processes, keep only one
```

### Check 4: Permissions on jobs.json​

Jobs are stored in~/.hermes/cron/jobs.json. If this file is not readable/writable by your user, the scheduler will fail silently:

`~/.hermes/cron/jobs.json`

```
ls -la ~/.hermes/cron/jobs.jsonchmod 600 ~/.hermes/cron/jobs.json   # Your user should own it
```

## Performance Issues​

### Slow job startup​

Each cron job creates a fresh AIAgent session, which may involve provider authentication and model loading. For time-sensitive schedules, add buffer time (e.g.,0 8 * * *instead of0 9 * * *).

`0 8 * * *`
`0 9 * * *`

### Too many overlapping jobs​

The scheduler executes jobs sequentially within each tick. If multiple jobs are due at the same time, they run one after another. Consider staggering schedules (e.g.,0 9 * * *and5 9 * * *instead of both at0 9 * * *) to avoid delays.

`0 9 * * *`
`5 9 * * *`
`0 9 * * *`

### Large script output​

Scripts that dump megabytes of output will slow down the agent and may hit token limits. Filter/summarize at the script level — emit only what the agent needs to reason about.

## Diagnostic Commands​

```
hermes cron list                    # Show all jobs, states, next_run timeshermes cron run <job_id>            # Schedule for next tick (for testing)hermes cron edit <job_id>           # Fix configuration issueshermes logs                         # View recent Hermes logshermes skills list                  # Verify installed skills
```

## Getting More Help​

If you've worked through this guide and the issue persists:

1. Run the job withhermes cron run <job_id>(fires on next gateway tick) and watch for errors in the chat output
2. Check~/.hermes/logs/agent.logfor scheduler messages and~/.hermes/logs/errors.logfor warnings
3. Open an issue atgithub.com/NousResearch/hermes-agentwith:The job ID and scheduleThe delivery targetWhat you expected vs. what happenedRelevant error messages from the logs

`hermes cron run <job_id>`
`~/.hermes/logs/agent.log`
`~/.hermes/logs/errors.log`
- The job ID and schedule
- The delivery target
- What you expected vs. what happened
- Relevant error messages from the logs

For the complete cron reference, seeAutomate Anything with CronandScheduled Tasks (Cron).