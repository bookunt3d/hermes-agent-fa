- 
- Messaging Platforms
- Microsoft 365
- Microsoft Teams

# Microsoft Teams Setup

Connect Hermes Agent to Microsoft Teams as a bot. Unlike Slack's Socket Mode, Teams delivers messages by calling apublic HTTPS webhook, so your instance needs a publicly reachable endpoint — either a dev tunnel (local dev) or a real domain (production).

Need meeting summaries from Microsoft Graph events rather than normal bot conversations? Use the dedicated setup page:Teams Meetings.

> Runhermes gateway setupand pickMicrosoft Teamsfor a guided walk-through.

Runhermes gateway setupand pickMicrosoft Teamsfor a guided walk-through.

`hermes gateway setup`

## How the Bot Responds​

| Context | Behavior |
| --- | --- |
| Personal chat (DM) | Bot responds to every message. No @mention needed. |
| Group chat | Bot only responds when @mentioned. |
| Channel | Bot only responds when @mentioned. |

Teams delivers @mentions as regular messages with<at>BotName</at>tags, which Hermes strips automatically before processing.

`<at>BotName</at>`

For source or local installs, include the Teams extra so the bundled adapter can
import the Microsoft Teams SDK:

```
uv sync --extra teams# or, for editable installs:uv pip install -e ".[teams]"
```

## Step 1: Install the Teams CLI​

The@microsoft/teams.cliautomates bot registration — no Azure portal needed.

`@microsoft/teams.cli`

```
npm install -g @microsoft/teams.cli@previewteams login
```

To verify your login and find your own AAD object ID (needed forTEAMS_ALLOWED_USERS):

`TEAMS_ALLOWED_USERS`

```
teams status --verbose
```

## Step 2: Expose the Webhook Port​

Teams cannot deliver messages tolocalhost. For local development, use any tunnel tool to get a public HTTPS URL. The default port is3978— change it withTEAMS_PORTif needed.

`localhost`
`3978`
`TEAMS_PORT`

```
# devtunnel (Microsoft)devtunnel create hermes-bot --allow-anonymousdevtunnel port create hermes-bot -p 3978 --protocol https  # replace 3978 with TEAMS_PORT if changeddevtunnel host hermes-bot# ngrokngrok http 3978  # replace 3978 with TEAMS_PORT if changed# cloudflaredcloudflared tunnel --url http://localhost:3978  # replace 3978 with TEAMS_PORT if changed
```

Copy thehttps://URL from the output — you'll use it in the next step. Leave the tunnel running while developing.

`https://`

For production, point your bot's endpoint at your server's public domain instead (seeProduction Deployment).

## Step 3: Create the Bot​

```
teams app create \  --name "Hermes" \  --endpoint "https://<your-tunnel-url>/api/messages"
```

The CLI outputs yourCLIENT_ID,CLIENT_SECRET, andTENANT_ID, plus an install link for Step 6. Save the client secret — it won't be shown again.

`CLIENT_ID`
`CLIENT_SECRET`
`TENANT_ID`

## Step 4: Configure Environment Variables​

Add to~/.hermes/.env:

`~/.hermes/.env`

```
# RequiredTEAMS_CLIENT_ID=<your-client-id>TEAMS_CLIENT_SECRET=<your-client-secret>TEAMS_TENANT_ID=<your-tenant-id># Restrict access to specific users (recommended)# Use AAD object IDs from `teams status --verbose`TEAMS_ALLOWED_USERS=<your-aad-object-id>
```

## Step 5: Start the Gateway​

```
HERMES_UID=$(id -u) HERMES_GID=$(id -g) docker compose up -d gateway
```

This starts the gateway. The default webhook port is3978(override withTEAMS_PORT). Check that it's running:

`3978`
`TEAMS_PORT`

```
curl http://localhost:3978/health   # should return: okdocker logs -f hermes
```

Look for:

```
[teams] Webhook server listening on 0.0.0.0:3978/api/messages
```

## Step 6: Install the App in Teams​

```
teams app get <teamsAppId> --install-link
```

Open the printed link in your browser — it opens directly in the Teams client. After installing, send a direct message to your bot — it's ready.

## Configuration Reference​

### Environment Variables​

| Variable | Description |
| --- | --- |
| TEAMS_CLIENT_ID | Azure AD App (client) ID |
| TEAMS_CLIENT_SECRET | Azure AD client secret |
| TEAMS_TENANT_ID | Azure AD tenant ID |
| TEAMS_ALLOWED_USERS | Comma-separated AAD object IDs allowed to use the bot |
| TEAMS_ALLOW_ALL_USERS | Settrueto skip the allowlist and allow anyone |
| TEAMS_HOME_CHANNEL | Conversation ID for cron/proactive message delivery |
| TEAMS_HOME_CHANNEL_NAME | Display name for the home channel |
| TEAMS_PORT | Webhook port (default:3978) |

`TEAMS_CLIENT_ID`
`TEAMS_CLIENT_SECRET`
`TEAMS_TENANT_ID`
`TEAMS_ALLOWED_USERS`
`TEAMS_ALLOW_ALL_USERS`
`true`
`TEAMS_HOME_CHANNEL`
`TEAMS_HOME_CHANNEL_NAME`
`TEAMS_PORT`
`3978`

### config.yaml​

Alternatively, configure via~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
platforms:  teams:    enabled: true    extra:      client_id: "your-client-id"      client_secret: "your-secret"      tenant_id: "your-tenant-id"      port: 3978
```

## Features​

### Interactive Approval Cards​

When the agent needs to run a potentially dangerous command, it sends an Adaptive Card with four buttons instead of asking you to type/approve:

`/approve`
- Allow Once— approve this specific command
- Allow Session— approve this pattern for the rest of the session
- Always Allow— permanently approve this pattern
- Deny— reject the command

Clicking a button resolves the approval inline and replaces the card with the decision.

### Meeting Summary Delivery (Teams Meeting Pipeline)​

When theTeams meeting pipeline pluginis enabled, this adapter also handles outbound delivery of meeting summaries — one Teams integration surface, not two. After a meeting's transcript is summarized, the writer posts the summary into your chosen Teams target.

Pipeline summary delivery is configured under theteamsplatform entry alongside the bot config:

`teams`

```
platforms:  teams:    enabled: true    extra:      # existing bot config (client_id, client_secret, tenant_id, port) ...      # Meeting summary delivery (only used when the teams_pipeline plugin is enabled)      delivery_mode: "graph"       # or "incoming_webhook"      # For delivery_mode: graph — pick ONE of:      chat_id: "19:meeting_..."    # post into a Teams chat      # team_id: "..."             # OR post into a channel      # channel_id: "..."      # access_token: "..."        # optional; falls back to MSGRAPH_* app credentials      # For delivery_mode: incoming_webhook:      # incoming_webhook_url: "https://outlook.office.com/webhook/..."
```

| Mode | Use when | Trade-off |
| --- | --- | --- |
| incoming_webhook | Simple "post a summary into this channel" with a static Teams-generated URL. | No reply threading, no reactions, shows as the webhook's configured identity. |
| graph | Threaded channel posts or 1:1/group chat posts under the bot's identity via Microsoft Graph. | Requires theGraph app registrationwithChannelMessage.Send(channel) orChat.ReadWrite.All(chat) application permissions. |

`incoming_webhook`
`graph`
`ChannelMessage.Send`
`Chat.ReadWrite.All`

If theteams_pipelineplugin isnotenabled, these settings are inert — they only wire up when the pipeline runtime binds to the Graph webhook ingress.

`teams_pipeline`

## Production Deployment​

For a permanent server, skip devtunnel and register your bot with your server's public HTTPS endpoint:

```
teams app create \  --name "Hermes" \  --endpoint "https://your-domain.com/api/messages"
```

If you've already created the bot and just need to update the endpoint:

```
teams app update --id <teamsAppId> --endpoint "https://your-domain.com/api/messages"
```

Make sure your configured port (TEAMS_PORT, default3978) is reachable from the internet and that your TLS certificate is valid — Teams rejects self-signed certificates.

`TEAMS_PORT`
`3978`

## Troubleshooting​

| Problem | Solution |
| --- | --- |
| healthendpoint works but bot doesn't respond | Check that your tunnel is still running and the bot's messaging endpoint matches the tunnel URL |
| KeyError: 'teams'in logs | Restart the container — this is fixed in the current version |
| Bot responds with auth errors | VerifyTEAMS_CLIENT_ID,TEAMS_CLIENT_SECRET, andTEAMS_TENANT_IDare all set correctly |
| No inference provider configured | Check thatANTHROPIC_API_KEY(or another provider key) is set in~/.hermes/.env |
| Bot receives messages but ignores them | Your AAD object ID may not be inTEAMS_ALLOWED_USERS. Runteams status --verboseto find it |
| Tunnel URL changes on restart | devtunnel URLs are persistent if you use a named tunnel (devtunnel create hermes-bot). ngrok and cloudflared generate a new URL each run unless you have a paid plan — update the bot endpoint withteams app updatewhen it changes |
| Teams shows "This bot is not responding" | The webhook returned an error. Checkdocker logs hermesfor tracebacks |
| [teams] Failed to connectin logs | The SDK failed to authenticate. Double-check your credentials and that the tenant ID matches the account you used inteams login |

`health`
`KeyError: 'teams'`
`TEAMS_CLIENT_ID`
`TEAMS_CLIENT_SECRET`
`TEAMS_TENANT_ID`
`No inference provider configured`
`ANTHROPIC_API_KEY`
`~/.hermes/.env`
`TEAMS_ALLOWED_USERS`
`teams status --verbose`
`devtunnel create hermes-bot`
`teams app update`
`docker logs hermes`
`[teams] Failed to connect`
`teams login`

## Security​

Always setTEAMS_ALLOWED_USERSwith the AAD object IDs of authorized users. Without this, anyone who can find or install your bot can interact with it.

`TEAMS_ALLOWED_USERS`

TreatTEAMS_CLIENT_SECRETlike a password — rotate it periodically via the Azure portal or Teams CLI.

`TEAMS_CLIENT_SECRET`
- Store credentials in~/.hermes/.envwith permissions600(chmod 600 ~/.hermes/.env)
- The bot only accepts messages from users inTEAMS_ALLOWED_USERS; unauthorized messages are silently dropped
- Your public endpoint (/api/messages) is authenticated by the Teams Bot Framework — requests without valid JWTs are rejected

`~/.hermes/.env`
`600`
`chmod 600 ~/.hermes/.env`
`TEAMS_ALLOWED_USERS`
`/api/messages`

## Related Docs​

- Teams Meetings
- Operate the Teams Meeting Pipeline