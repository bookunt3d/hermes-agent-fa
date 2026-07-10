- 
- Guides & Tutorials
- Operate the Teams Meeting Pipeline

# Operate the Teams Meeting Pipeline

Use this guide after you have already enabled the feature fromTeams Meetings.

This page covers:

- operator CLI flows
- routine subscription maintenance
- failure triage
- go-live checks
- rollout worksheet

## Core Operator Commands​

### Validate the config snapshot​

```
hermes teams-pipeline validate
```

Use this first after any config change.

### Inspect token health​

```
hermes teams-pipeline token-healthhermes teams-pipeline token-health --force-refresh
```

Use--force-refreshwhen you suspect stale auth state.

`--force-refresh`

### Inspect subscriptions​

```
hermes teams-pipeline subscriptions
```

### Renew near-expiry subscriptions​

```
hermes teams-pipeline maintain-subscriptionshermes teams-pipeline maintain-subscriptions --dry-run
```

### Automating subscription renewal (REQUIRED for production)​

Microsoft Graph subscriptions expire in at most 72 hours.If nothing renews them, meeting notifications silently stop after 3 days and the pipeline looks "broken." This is the #1 operational failure mode for any Graph-backed integration.

You MUST runmaintain-subscriptionson a schedule. Pick one of these three options:

`maintain-subscriptions`

#### Option 1: Hermes cron (recommended if you already run the Hermes gateway)​

Hermes ships a built-in cron scheduler. The--no-agentmode runs a script as the job (rather than using an LLM), and--scriptmust point at a file under~/.hermes/scripts/. First create the script:

`--no-agent`
`--script`
`~/.hermes/scripts/`

```
mkdir -p ~/.hermes/scriptscat > ~/.hermes/scripts/maintain-teams-subscriptions.sh <<'EOF'#!/usr/bin/env bashexec hermes teams-pipeline maintain-subscriptionsEOFchmod +x ~/.hermes/scripts/maintain-teams-subscriptions.sh
```

Then register a script-only cron job that runs every 12 hours (gives 6x headroom against the 72h expiry window):

```
hermes cron create "0 */12 * * *" \  --name "teams-pipeline-maintain-subscriptions" \  --no-agent \  --script maintain-teams-subscriptions.sh \  --deliver local
```

Verify it was registered and inspect the next run time:

```
hermes cron listhermes cron status        # scheduler status
```

#### Option 2: systemd timer (recommended for Linux production deployments)​

Create/etc/systemd/system/hermes-teams-pipeline-maintain.service:

`/etc/systemd/system/hermes-teams-pipeline-maintain.service`

```
[Unit]Description=Hermes Teams pipeline subscription maintenanceAfter=network-online.target[Service]Type=oneshotUser=hermesEnvironmentFile=/etc/hermes/envExecStart=/usr/local/bin/hermes teams-pipeline maintain-subscriptions
```

And/etc/systemd/system/hermes-teams-pipeline-maintain.timer:

`/etc/systemd/system/hermes-teams-pipeline-maintain.timer`

```
[Unit]Description=Run Hermes Teams pipeline subscription maintenance every 12 hours[Timer]OnBootSec=5minOnUnitActiveSec=12hPersistent=true[Install]WantedBy=timers.target
```

Enable:

```
sudo systemctl daemon-reloadsudo systemctl enable --now hermes-teams-pipeline-maintain.timersystemctl list-timers hermes-teams-pipeline-maintain.timer
```

#### Option 3: Plain crontab​

```
0 */12 * * * /usr/local/bin/hermes teams-pipeline maintain-subscriptions >> /var/log/hermes/teams-pipeline-maintain.log 2>&1
```

Make sure the cron environment has theMSGRAPH_*credentials. Simplest fix: source~/.hermes/.envat the top of a wrapper script that crontab calls.

`MSGRAPH_*`
`~/.hermes/.env`

#### Verifying renewal is working​

After you've set up the schedule, check renewal activity after the first scheduled run:

```
hermes teams-pipeline subscriptions   # should show expirationDateTime advancedhermes teams-pipeline maintain-subscriptions --dry-run   # should show "0 expiring soon" most of the time
```

If you ever see your Graph webhook mysteriously "stop working" after exactly ~72 hours, this is the first thing to check: did the renewal job actually run?

### Inspect recent jobs​

```
hermes teams-pipeline listhermes teams-pipeline list --status failedhermes teams-pipeline show <job-id>
```

### Replay a stored job​

```
hermes teams-pipeline run <job-id>
```

### Dry-run meeting artifact fetches​

```
hermes teams-pipeline fetch --meeting-id <meeting-id>hermes teams-pipeline fetch --join-web-url "<join-url>"
```

## Routine Runbook​

### After first setup​

Run these in order:

```
hermes teams-pipeline validatehermes teams-pipeline token-health --force-refreshhermes teams-pipeline subscriptions
```

Then trigger or wait for a real meeting event and confirm:

```
hermes teams-pipeline listhermes teams-pipeline show <job-id>
```

### Daily or periodic checks​

- runhermes teams-pipeline maintain-subscriptions --dry-run
- inspecthermes teams-pipeline list --status failed
- verify the Teams delivery target is still the correct chat or channel

`hermes teams-pipeline maintain-subscriptions --dry-run`
`hermes teams-pipeline list --status failed`

### Before changing webhook URLs or delivery targets​

- update the public notification URL or Teams target config
- runhermes teams-pipeline validate
- renew or recreate affected subscriptions
- confirm new events land in the expected sink

`hermes teams-pipeline validate`

## Failure Triage​

### No jobs are being created​

Check:

- msgraph_webhookis enabled
- the public notification URL points to/msgraph/webhook
- the client state in the subscription matchesMSGRAPH_WEBHOOK_CLIENT_STATE
- subscriptions still exist remotely and are not expired

`msgraph_webhook`
`/msgraph/webhook`
`MSGRAPH_WEBHOOK_CLIENT_STATE`

### Jobs stay in retry or fail before summarization​

Check:

- transcript permissions and availability
- recording permissions and artifact availability
- ffmpegavailability if recording fallback is enabled
- Graph token health

`ffmpeg`

### Summaries are produced but not delivered to Teams​

Check:

- platforms.teams.enabled: true
- delivery_mode
- incoming_webhook_urlfor webhook mode
- chat_idorteam_idpluschannel_idfor Graph mode
- Teams auth config if Graph posting is used

`platforms.teams.enabled: true`
`delivery_mode`
`incoming_webhook_url`
`chat_id`
`team_id`
`channel_id`

### Duplicate or unexpected replays​

Check:

- whether you manually replayed a job withhermes teams-pipeline run
- whether the sink record already exists for that meeting
- whether you intentionally enabled a resend path in your local config

`hermes teams-pipeline run`

## Go-Live Checklist​

- Graph credentials are present and correct
- msgraph_webhookis enabled and reachable from the public internet
- MSGRAPH_WEBHOOK_CLIENT_STATEis set and matches subscriptions
- transcript subscription is created
- recording subscription is created if STT fallback is required
- ffmpegis installed if recording fallback is enabled
- Teams outbound delivery target is configured and verified
- Notion and Linear sinks are configured only if actually needed
- hermes teams-pipeline validatereturns an OK snapshot
- hermes teams-pipeline token-health --force-refreshsucceeds
- maintain-subscriptionsis scheduled(Hermes cron, systemd timer, or crontab — seeAutomating subscription renewal). Without this, Graph subscriptions silently expire within 72 hours.
- a real end-to-end meeting event has produced a stored job
- at least one summary has reached the intended delivery sink

`msgraph_webhook`
`MSGRAPH_WEBHOOK_CLIENT_STATE`
`ffmpeg`
`hermes teams-pipeline validate`
`hermes teams-pipeline token-health --force-refresh`
`maintain-subscriptions`

## Delivery-Mode Decision Guide​

| Mode | Use when | Tradeoff |
| --- | --- | --- |
| incoming_webhook | you only need simple posting into Teams | simplest setup, less control |
| graph | you need channel or chat posting through Graph | more control, more auth and target config |

`incoming_webhook`
`graph`

## Operator Worksheet​

Fill this out before rollout:

| Item | Value |
| --- | --- |
| Public notification URL |  |
| Graph tenant ID |  |
| Graph client ID |  |
| Webhook client state |  |
| Transcript resource subscription |  |
| Recording resource subscription |  |
| Teams delivery mode |  |
| Teams chat ID or team/channel |  |
| Notion database ID |  |
| Linear team ID |  |
| Store path override, if any |  |
| Owner for daily checks |  |

## Change Review Worksheet​

Use this before changing the deployment:

| Question | Answer |
| --- | --- |
| Are we changing the public webhook URL? |  |
| Are we rotating Graph credentials? |  |
| Are we changing Teams delivery mode? |  |
| Are we moving to a new Teams chat or channel? |  |
| Do subscriptions need to be recreated or renewed? |  |
| Do we need a fresh end-to-end verification run? |  |

## Related Docs​

- Teams Meetings setup
- Microsoft Teams bot setup