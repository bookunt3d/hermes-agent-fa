- 
- Messaging Platforms
- Microsoft 365
- Teams Meetings

# Microsoft Teams Meetings

Use the Teams meeting pipeline when you want Hermes to ingest Microsoft Graph meeting events, fetch transcripts first, fall back to recordings plus STT when needed, and deliver a structured summary to downstream sinks.

Prerequisites: seeMicrosoft Teamsfor the underlying bot/credential setup.

> Runhermes gateway setupand pickTeams Meetingsfor a guided walk-through.

Runhermes gateway setupand pickTeams Meetingsfor a guided walk-through.

`hermes gateway setup`

This page focuses on setup and enablement:

- Graph credentials
- webhook listener configuration
- Teams delivery modes
- pipeline config shape

For day-2 operations, go-live checks, and the operator worksheet, use the dedicated guide:Operate the Teams Meeting Pipeline.

## What This Feature Does​

The pipeline:

1. receives Microsoft Graph webhook events
2. resolves the meeting and prefers transcript artifacts first
3. falls back to recording download plus STT when no usable transcript is available
4. stores durable job state and sink records locally
5. can write summaries to Notion, Linear, and Microsoft Teams

Operator actions stay in the CLI (theteams-pipelinesubcommand is registered by theteams_pipelineplugin — enable it viahermes plugins enable teams_pipelineor setplugins.enabled: [teams_pipeline]inconfig.yaml):

`teams-pipeline`
`teams_pipeline`
`hermes plugins enable teams_pipeline`
`plugins.enabled: [teams_pipeline]`
`config.yaml`

```
hermes teams-pipeline validatehermes teams-pipeline listhermes teams-pipeline maintain-subscriptions
```

## Prerequisites​

Before enabling the meetings pipeline, make sure you have:

- a working Hermes install
- the existingMicrosoft Teams bot setupif you want Teams outbound delivery
- Microsoft Graph application credentials with the permissions required for the meeting resources you plan to subscribe to
- a public HTTPS URL that Microsoft Graph can call for webhook delivery
- ffmpeginstalled if you want recording-plus-STT fallback

`ffmpeg`

## Step 1: Add Microsoft Graph Credentials​

Add Graph app-only credentials to~/.hermes/.env:

`~/.hermes/.env`

```
MSGRAPH_TENANT_ID=<tenant-id>MSGRAPH_CLIENT_ID=<client-id>MSGRAPH_CLIENT_SECRET=<client-secret>
```

These credentials are used by:

- the Graph client foundation
- subscription maintenance commands
- meeting resolution and artifact fetches
- Graph-based Teams outbound delivery when you do not provide a dedicated Teams access token

## Step 2: Enable the Graph Webhook Listener​

The webhook listener is a gateway platform namedmsgraph_webhook. At minimum, enable it and set a client state value:

`msgraph_webhook`

```
MSGRAPH_WEBHOOK_ENABLED=trueMSGRAPH_WEBHOOK_HOST=127.0.0.1MSGRAPH_WEBHOOK_PORT=8646MSGRAPH_WEBHOOK_CLIENT_STATE=<random-shared-secret>MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES=communications/onlineMeetings
```

The listener exposes:

- /msgraph/webhookfor Graph notifications
- /healthfor a simple health check

`/msgraph/webhook`
`/health`

You need to route your public HTTPS endpoint to that listener. For example, if your public domain ishttps://ops.example.com, your Graph notification URL would typically be:

`https://ops.example.com`

```
https://ops.example.com/msgraph/webhook
```

## Step 3: Configure Teams Delivery and Pipeline Behavior​

The meeting pipeline reads its runtime config from the existingteamsplatform entry. Pipeline-specific knobs live underteams.extra.meeting_pipeline. Teams outbound delivery stays on the normal Teams platform config surface.

`teams`
`teams.extra.meeting_pipeline`

Example~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
platforms:  msgraph_webhook:    enabled: true    extra:      host: 127.0.0.1      port: 8646      client_state: "replace-me"      accepted_resources:        - "communications/onlineMeetings"  teams:    enabled: true    extra:      client_id: "your-teams-client-id"      client_secret: "your-teams-client-secret"      tenant_id: "your-teams-tenant-id"      # outbound summary delivery      delivery_mode: "graph" # or incoming_webhook      team_id: "team-id"      channel_id: "channel-id"      # incoming_webhook_url: "https://..."      meeting_pipeline:        transcript_min_chars: 80        transcript_required: false        transcription_fallback: true        ffmpeg_extract_audio: true        notion:          enabled: false        linear:          enabled: false
```

If you bind the listener to a non-loopback host such as0.0.0.0, you must also setallowed_source_cidrsto Microsoft's webhook egress ranges. Loopback binds (127.0.0.1/::1) are the intended dev-tunnel and local reverse-proxy setup.

`0.0.0.0`
`allowed_source_cidrs`
`127.0.0.1`
`::1`

## Teams Delivery Modes​

The pipeline supports two Teams summary-delivery modes inside the existing Teams plugin.

### incoming_webhook​

`incoming_webhook`

Use this when you want a simple webhook post into Teams without channel-message creation through Graph.

Required config:

```
platforms:  teams:    enabled: true    extra:      delivery_mode: "incoming_webhook"      incoming_webhook_url: "https://..."
```

### graph​

`graph`

Use this when you want Hermes to post the summary through Microsoft Graph into a Teams chat or channel.

Supported targets:

- chat_id
- team_id+channel_id
- team_id+home_channelfallback for the existing Teams platform

`chat_id`
`team_id`
`channel_id`
`team_id`
`home_channel`

Example:

```
platforms:  teams:    enabled: true    extra:      delivery_mode: "graph"      team_id: "team-id"      channel_id: "channel-id"
```

## Step 4: Start the Gateway​

Start Hermes normally after updating config:

```
hermes gateway run
```

Or, if you run Hermes in Docker, start the gateway the same way you already do for your deployment.

Check the listener:

```
curl http://localhost:8646/health
```

## Step 5: Create Graph Subscriptions​

Use the plugin CLI to create and inspect subscriptions.

Examples:

```
hermes teams-pipeline subscribe \  --resource communications/onlineMeetings/getAllTranscripts \  --notification-url https://ops.example.com/msgraph/webhook \  --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"hermes teams-pipeline subscribe \  --resource communications/onlineMeetings/getAllRecordings \  --notification-url https://ops.example.com/msgraph/webhook \  --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"
```

Microsoft Graph caps webhook subscriptions at 72 hours and will not auto-renew them. You MUST schedulehermes teams-pipeline maintain-subscriptionsbefore going live, or notifications will silently stop three days after any manual subscription creation. SeeAutomating subscription renewalin the operator runbook — three options (Hermes cron, systemd timer, plain crontab).

`hermes teams-pipeline maintain-subscriptions`

For subscription maintenance and day-2 operator flows, continue with the guide:Operate the Teams Meeting Pipeline.

## Validation​

Run the built-in validation snapshot:

```
hermes teams-pipeline validate
```

Useful companion checks:

```
hermes teams-pipeline token-healthhermes teams-pipeline subscriptions
```

## Troubleshooting​

| Problem | What to check |
| --- | --- |
| Graph webhook validation fails | Confirm the public URL is correct and reachable, and that Graph is calling the exact/msgraph/webhookpath |
| Jobs do not appear inhermes teams-pipeline list | Confirmmsgraph_webhookis enabled and that subscriptions point at the right notification URL |
| Transcript-first never succeeds | Check Graph permissions for transcript resources and whether the transcript artifact exists for that meeting |
| Recording fallback fails | Confirmffmpegis installed and the Graph app can access recording artifacts |
| Teams summary delivery fails | Re-checkdelivery_mode, target IDs, and Teams auth config |

`/msgraph/webhook`
`hermes teams-pipeline list`
`msgraph_webhook`
`ffmpeg`
`delivery_mode`

## Related Docs​

- Microsoft Teams bot setup
- Operate the Teams Meeting Pipeline