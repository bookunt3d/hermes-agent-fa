---
layout: docs
title: "Messaging_Webhooks"
permalink: /docs/user-guide/messaging_webhooks/
---

- 
- Messaging Platforms
- Other
- Webhooks

# Webhooks

Receive events from external services (GitHub, GitLab, JIRA, Stripe, etc.) and trigger Hermes agent runs automatically. The webhook adapter runs an HTTP server that accepts POST requests, validates HMAC signatures, transforms payloads into agent prompts, and routes responses back to the source or to another configured platform.

The agent processes the event and can respond by posting comments on PRs, sending messages to Telegram/Discord, or logging the result.

## Video Tutorial​

## Quick Start​

1. Enable viahermes gateway setupor environment variables
2. Define routes inconfig.yamlorcreate them dynamically withhermes webhook subscribe
3. Point your service athttp://your-server:8644/webhooks/<route-name>

`hermes gateway setup`
`config.yaml`
`hermes webhook subscribe`
`http://your-server:8644/webhooks/<route-name>`

## Setup​

There are two ways to enable the webhook adapter.

### Via setup wizard​

```
hermes gateway setup
```

Follow the prompts to enable webhooks, set the port, and set a global HMAC secret.

### Via environment variables​

Add to~/.hermes/.env:

`~/.hermes/.env`

```
WEBHOOK_ENABLED=trueWEBHOOK_PORT=8644        # defaultWEBHOOK_SECRET=your-global-secret
```

### Verify the server​

Once the gateway is running:

```
curl http://localhost:8644/health
```

Expected response:

```
{"status": "ok", "platform": "webhook"}
```

## Configuring Routes​

Routes define how different webhook sources are handled. Each route is a named entry underplatforms.webhook.extra.routesin yourconfig.yaml.

`platforms.webhook.extra.routes`
`config.yaml`

### Route properties​

| Property | Required | Description |
| --- | --- | --- |
| events | No | List of event types to accept (e.g.["pull_request"]). If empty, all events are accepted. Event type is read fromX-GitHub-Event,X-GitLab-Event, orevent_typein the payload. |
| secret | Yes | HMAC secret for signature validation. Falls back to the globalsecretif not set on the route. Set to"INSECURE_NO_AUTH"for testing only (skips validation). |
| prompt | No | Template string with dot-notation payload access (e.g.{pull_request.title}). If omitted, the full JSON payload is dumped into the prompt. Payload fields are untrusted — seeAuthenticated does not mean trusted. |
| filters | No | Declarative payload filters evaluated after auth/body/event filtering and before agent or direct delivery work. Non-matches return{"status":"ignored","reason":"filter"}with HTTP 200. |
| script | No | Filter/transform script under~/.hermes/scripts/. The webhook payload is passed as JSON on stdin. JSON object stdout replaces the payload before templating; text stdout is exposed asscript_output; empty stdout,[SILENT], or a nonzero exit code ignores the webhook. |
| skills | No | List of skill names to load for the agent run. |
| deliver | No | Where to send the response:github_comment,telegram,discord,slack,signal,sms,whatsapp,matrix,mattermost,homeassistant,email,dingtalk,feishu,wecom,weixin,bluebubbles,qqbot, orlog(default). |
| deliver_extra | No | Additional delivery config — keys depend ondelivertype (e.g.repo,pr_number,chat_id). Values support the same{dot.notation}templates asprompt. |
| deliver_only | No | Iftrue, skip the agent entirely — the renderedprompttemplate becomes the literal message that gets delivered. Zero LLM cost, sub-second delivery. SeeDirect Delivery Modefor use cases. Requiresdeliverto be a real target (notlog). |

`events`
`["pull_request"]`
`X-GitHub-Event`
`X-GitLab-Event`
`event_type`
`secret`
`secret`
`"INSECURE_NO_AUTH"`
`prompt`
`{pull_request.title}`
`filters`
`{"status":"ignored","reason":"filter"}`
`script`
`~/.hermes/scripts/`
`script_output`
`[SILENT]`
`skills`
`deliver`
`github_comment`
`telegram`
`discord`
`slack`
`signal`
`sms`
`whatsapp`
`matrix`
`mattermost`
`homeassistant`
`email`
`dingtalk`
`feishu`
`wecom`
`weixin`
`bluebubbles`
`qqbot`
`log`
`deliver_extra`
`deliver`
`repo`
`pr_number`
`chat_id`
`{dot.notation}`
`prompt`
`deliver_only`
`true`
`prompt`
`deliver`
`log`

### Full example​

```
platforms:  webhook:    enabled: true    extra:      port: 8644      secret: "global-fallback-secret"      routes:        github-pr:          events: ["pull_request"]          secret: "github-webhook-secret"          prompt: |            Review this pull request:            Repository: {repository.full_name}            PR #{number}: {pull_request.title}            Author: {pull_request.user.login}            URL: {pull_request.html_url}            Diff URL: {pull_request.diff_url}            Action: {action}          skills: ["github-code-review"]          deliver: "github_comment"          deliver_extra:            repo: "{repository.full_name}"            pr_number: "{number}"        deploy-notify:          events: ["push"]          secret: "deploy-secret"          prompt: "New push to {repository.full_name} branch {ref}: {head_commit.message}"          filters:            - field: "ref"              equals: "refs/heads/main"          deliver: "telegram"
```

### Payload Filters​

Usefilterswhen a provider sends a broad event stream but only some payloads should wake the agent or triggerdeliver_onlydelivery. Filters run after signature validation, body parsing, andevents, but before prompt rendering, idempotency, agent dispatch, or direct delivery.

`filters`
`deliver_only`
`events`

```
platforms:  webhook:    extra:      routes:        todoist:          events: ["item:updated"]          secret: "todoist-secret"          filters:            - field: "payload.labels"              contains: "hermes"            - any:                - field: "payload.priority"                  equals: 4                - field: "payload.project_id"                  in_file: "~/.hermes/data/todoist/watchlist.json"          prompt: "Todoist task changed: {payload.content}"
```

Supported operators:

- exists: true|false
- missing: true
- equals/not_equals
- containsfor strings, lists, and dict keys
- infor inline lists
- in_filefor JSON arrays, JSON objects (keys are used), or newline-delimited text files
- regex
- all,any, andnotgroups

`exists: true|false`
`missing: true`
`equals`
`not_equals`
`contains`
`in`
`in_file`
`regex`
`all`
`any`
`not`

Field paths use dot notation.payload.fooreads from a top-levelpayloadobject when one exists, or from the root webhook body for flat payloads.event/event_typematch the resolved event type, andheaders.<Name>reads request headers.

`payload.foo`
`payload`
`event`
`event_type`
`headers.<Name>`

### Script Filters and Transforms​

Usescriptwhen declarative filters are not enough. Scripts must live under~/.hermes/scripts/for the active profile; relative paths resolve there, and path traversal outside that directory is blocked..shand.bashscripts run with bash, and all other extensions run with the current Python interpreter.

`script`
`~/.hermes/scripts/`
`.sh`
`.bash`

The route payload is sent to stdin as JSON:

```
# ~/.hermes/scripts/todoist-hermes-label.pyimport jsonimport syspayload = json.load(sys.stdin)labels = payload.get("payload", {}).get("labels", [])if "hermes" not in labels:    print("[SILENT]")    raise SystemExit(0)payload["body"] = payload["payload"]["content"]print(json.dumps(payload))
```

Script outcomes:

- JSON object stdout replaces the payload used bypromptanddeliver_extra.
- Non-JSON text stdout is added to the payload asscript_output.
- Empty stdout, exact[SILENT],{"__hermes_ignore__": true}, timeout, missing script, or nonzero exit code returns HTTP 200 with{"status":"ignored","reason":"script"}.

`prompt`
`deliver_extra`
`script_output`
`[SILENT]`
`{"__hermes_ignore__": true}`
`{"status":"ignored","reason":"script"}`

### Prompt Templates​

Prompts use dot-notation to access nested fields in the webhook payload:

- {pull_request.title}resolves topayload["pull_request"]["title"]
- {repository.full_name}resolves topayload["repository"]["full_name"]
- {__raw__}— special token that dumps theentire payloadas indented JSON (truncated at 4000 characters). Useful for monitoring alerts or generic webhooks where the agent needs the full context.
- Missing keys are left as the literal{key}string (no error)
- Nested dicts and lists are JSON-serialized and truncated at 2000 characters

`{pull_request.title}`
`payload["pull_request"]["title"]`
`{repository.full_name}`
`payload["repository"]["full_name"]`
`{__raw__}`
`{key}`

You can mix{__raw__}with regular template variables:

`{__raw__}`

```
prompt: "PR #{pull_request.number} by {pull_request.user.login}: {__raw__}"
```

If noprompttemplate is configured for a route, the entire payload is dumped as indented JSON (truncated at 4000 characters).

`prompt`

The same dot-notation templates work indeliver_extravalues.

`deliver_extra`

### Forum Topic Delivery​

When delivering webhook responses to Telegram, you can target a specific forum topic by includingmessage_thread_id(orthread_id) indeliver_extra:

`message_thread_id`
`thread_id`
`deliver_extra`

```
webhooks:  routes:    alerts:      events: ["alert"]      prompt: "Alert: {__raw__}"      deliver: "telegram"      deliver_extra:        chat_id: "-1001234567890"        message_thread_id: "42"
```

Ifchat_idis not provided indeliver_extra, the delivery falls back to the home channel configured for the target platform.

`chat_id`
`deliver_extra`

## GitHub PR Review (Step by Step)​

This walkthrough sets up automatic code review on every pull request.

### 1. Create the webhook in GitHub​

1. Go to your repository →Settings→Webhooks→Add webhook
2. SetPayload URLtohttp://your-server:8644/webhooks/github-pr
3. SetContent typetoapplication/json
4. SetSecretto match your route config (e.g.github-webhook-secret)
5. UnderWhich events?, selectLet me select individual eventsand checkPull requests
6. ClickAdd webhook

`http://your-server:8644/webhooks/github-pr`
`application/json`
`github-webhook-secret`

### 2. Add the route config​

Add thegithub-prroute to your~/.hermes/config.yamlas shown in the example above.

`github-pr`
`~/.hermes/config.yaml`

### 3. EnsureghCLI is authenticated​

`gh`

Thegithub_commentdelivery type uses the GitHub CLI to post comments:

`github_comment`

```
gh auth login
```

### 4. Test it​

Open a pull request on the repository. The webhook fires, Hermes processes the event, and posts a review comment on the PR.

## GitLab Webhook Setup​

GitLab webhooks work similarly but use a different authentication mechanism. GitLab sends the secret as a plainX-Gitlab-Tokenheader (exact string match, not HMAC).

`X-Gitlab-Token`

### 1. Create the webhook in GitLab​

1. Go to your project →Settings→Webhooks
2. Set theURLtohttp://your-server:8644/webhooks/gitlab-mr
3. Enter yourSecret token
4. SelectMerge request events(and any other events you want)
5. ClickAdd webhook

`http://your-server:8644/webhooks/gitlab-mr`

### 2. Add the route config​

```
platforms:  webhook:    enabled: true    extra:      routes:        gitlab-mr:          events: ["merge_request"]          secret: "your-gitlab-secret-token"          prompt: |            Review this merge request:            Project: {project.path_with_namespace}            MR !{object_attributes.iid}: {object_attributes.title}            Author: {object_attributes.last_commit.author.name}            URL: {object_attributes.url}            Action: {object_attributes.action}          deliver: "log"
```

## Delivery Options​

Thedeliverfield controls where the agent's response goes after processing the webhook event.

`deliver`
| Deliver Type | Description |
| --- | --- |
| log | Logs the response to the gateway log output. This is the default and is useful for testing. |
| github_comment | Posts the response as a PR/issue comment via theghCLI. Requiresdeliver_extra.repoanddeliver_extra.pr_number. TheghCLI must be installed and authenticated on the gateway host (gh auth login). |
| telegram | Routes the response to Telegram. Uses the home channel, or specifychat_idindeliver_extra. |
| discord | Routes the response to Discord. Uses the home channel, or specifychat_idindeliver_extra. |
| slack | Routes the response to Slack. Uses the home channel, or specifychat_idindeliver_extra. |
| signal | Routes the response to Signal. Uses the home channel, or specifychat_idindeliver_extra. |
| sms | Routes the response to SMS via Twilio. Uses the home channel, or specifychat_idindeliver_extra. |
| whatsapp | Routes the response to WhatsApp. Uses the home channel, or specifychat_idindeliver_extra. |
| matrix | Routes the response to Matrix. Uses the home channel, or specifychat_idindeliver_extra. |
| mattermost | Routes the response to Mattermost. Uses the home channel, or specifychat_idindeliver_extra. |
| homeassistant | Routes the response to Home Assistant. Uses the home channel, or specifychat_idindeliver_extra. |
| email | Routes the response to Email. Uses the home channel, or specifychat_idindeliver_extra. |
| dingtalk | Routes the response to DingTalk. Uses the home channel, or specifychat_idindeliver_extra. |
| feishu | Routes the response to Feishu/Lark. Uses the home channel, or specifychat_idindeliver_extra. |
| wecom | Routes the response to WeCom. Uses the home channel, or specifychat_idindeliver_extra. |
| weixin | Routes the response to Weixin (WeChat). Uses the home channel, or specifychat_idindeliver_extra. |
| bluebubbles | Routes the response to BlueBubbles (iMessage). Uses the home channel, or specifychat_idindeliver_extra. |

`log`
`github_comment`
`gh`
`deliver_extra.repo`
`deliver_extra.pr_number`
`gh`
`gh auth login`
`telegram`
`chat_id`
`deliver_extra`
`discord`
`chat_id`
`deliver_extra`
`slack`
`chat_id`
`deliver_extra`
`signal`
`chat_id`
`deliver_extra`
`sms`
`chat_id`
`deliver_extra`
`whatsapp`
`chat_id`
`deliver_extra`
`matrix`
`chat_id`
`deliver_extra`
`mattermost`
`chat_id`
`deliver_extra`
`homeassistant`
`chat_id`
`deliver_extra`
`email`
`chat_id`
`deliver_extra`
`dingtalk`
`chat_id`
`deliver_extra`
`feishu`
`chat_id`
`deliver_extra`
`wecom`
`chat_id`
`deliver_extra`
`weixin`
`chat_id`
`deliver_extra`
`bluebubbles`
`chat_id`
`deliver_extra`

For cross-platform delivery, the target platform must also be enabled and connected in the gateway. If nochat_idis provided indeliver_extra, the response is sent to that platform's configured home channel.

`chat_id`
`deliver_extra`

## Direct Delivery Mode​

By default, every webhook POST triggers an agent run — the payload becomes a prompt, the agent processes it, and the agent's response is delivered. This costs LLM tokens on every event.

For use cases where you just want topush a plain notification— no reasoning, no agent loop, just deliver the message — setdeliver_only: trueon the route. The renderedprompttemplate becomes the literal message body, and the adapter dispatches it directly to the configured delivery target.

`deliver_only: true`
`prompt`

### When to use direct delivery​

- External service push— Supabase/Firebase webhook fires on a database change → notify a user in Telegram instantly
- Monitoring alerts— Datadog/Grafana alert webhook → push to a Discord channel
- Inter-agent pings— Agent A notifies Agent B's user that a long-running task finished
- Background job completion— Cron job finishes → post result to Slack

Benefits:

- Zero LLM tokens— the agent is never invoked
- Sub-second delivery— a single adapter call, no reasoning loop
- Same security as agent mode— HMAC auth, rate limits, idempotency, and body-size limits all still apply
- Synchronous response— the POST returns200 OKonce delivery succeeds, or502if the target rejects it, so your upstream service can retry intelligently

`200 OK`
`502`

### Example: Telegram push from Supabase​

```
platforms:  webhook:    enabled: true    extra:      port: 8644      secret: "global-secret"      routes:        antenna-matches:          secret: "antenna-webhook-secret"          deliver: "telegram"          deliver_only: true          prompt: "🎉 New match: {match.user_name} matched with you!"          deliver_extra:            chat_id: "{match.telegram_chat_id}"
```

Your Supabase edge function signs the payload with HMAC-SHA256 and POSTs tohttps://your-server:8644/webhooks/antenna-matches. The webhook adapter validates the signature, renders the template from the payload, delivers to Telegram, and returns200 OK.

`https://your-server:8644/webhooks/antenna-matches`
`200 OK`

### Example: Dynamic subscription via CLI​

```
hermes webhook subscribe antenna-matches \  --deliver telegram \  --deliver-chat-id "123456789" \  --deliver-only \  --prompt "🎉 New match: {match.user_name} matched with you!" \  --description "Antenna match notifications"
```

### Response codes​

| Status | Meaning |
| --- | --- |
| 200 OK | Delivered successfully. Body:{"status": "delivered", "route": "...", "target": "...", "delivery_id": "..."} |
| 200 OK(status=duplicate) | DuplicateX-GitHub-DeliveryID within the idempotency TTL (1 hour). Not re-delivered. |
| 401 Unauthorized | HMAC signature invalid or missing. |
| 400 Bad Request | Malformed JSON body. |
| 404 Not Found | Unknown route name. |
| 413 Payload Too Large | Body exceededmax_body_bytes. |
| 429 Too Many Requests | Route rate limit exceeded. |
| 502 Bad Gateway | Target adapter rejected the message or raised. The error is logged server-side; the response body is a genericDelivery failedto avoid leaking adapter internals. |

`200 OK`
`{"status": "delivered", "route": "...", "target": "...", "delivery_id": "..."}`
`200 OK`
`X-GitHub-Delivery`
`401 Unauthorized`
`400 Bad Request`
`404 Not Found`
`413 Payload Too Large`
`max_body_bytes`
`429 Too Many Requests`
`502 Bad Gateway`
`Delivery failed`

### Configuration gotchas​

- deliver_only: truerequiresdeliverto be a real target.deliver: log(or omittingdeliver) is rejected at startup — the adapter refuses to start if it finds a misconfigured route.
- Theskillsfield is ignored in direct delivery mode (no agent runs, so there's nothing to inject skills into).
- Template rendering uses the same{dot.notation}syntax as agent mode, including the{__raw__}token.
- Idempotency uses the sameX-GitHub-Delivery/X-Request-IDheader — retries with the same ID returnstatus=duplicateand do NOT re-deliver.

`deliver_only: true`
`deliver`
`deliver: log`
`deliver`
`skills`
`{dot.notation}`
`{__raw__}`
`X-GitHub-Delivery`
`X-Request-ID`
`status=duplicate`

## Dynamic Subscriptions (CLI)​

In addition to static routes inconfig.yaml, you can create webhook subscriptions dynamically using thehermes webhookCLI command. This is especially useful when the agent itself needs to set up event-driven triggers.

`config.yaml`
`hermes webhook`

### Create a subscription​

```
hermes webhook subscribe github-issues \  --events "issues" \  --prompt "New issue #{issue.number}: {issue.title}\nBy: {issue.user.login}\n\n{issue.body}" \  --deliver telegram \  --deliver-chat-id "-100123456789" \  --description "Triage new GitHub issues"
```

This returns the webhook URL and an auto-generated HMAC secret. Configure your service to POST to that URL.

### List subscriptions​

```
hermes webhook list
```

### Remove a subscription​

```
hermes webhook remove github-issues
```

### Test a subscription​

```
hermes webhook test github-issueshermes webhook test github-issues --payload '{"issue": {"number": 42, "title": "Test"}}'
```

### How dynamic subscriptions work​

- Subscriptions are stored in~/.hermes/webhook_subscriptions.json
- The webhook adapter hot-reloads this file on each incoming request (mtime-gated, negligible overhead)
- Static routes fromconfig.yamlalways take precedence over dynamic ones with the same name
- Dynamic subscriptions use the same route format and capabilities as static routes (events, prompt templates, skills, delivery)
- No gateway restart required — subscribe and it's immediately live

`~/.hermes/webhook_subscriptions.json`
`config.yaml`

### Agent-driven subscriptions​

The agent can create subscriptions via the terminal tool when guided by thewebhook-subscriptionsskill. Ask the agent to "set up a webhook for GitHub issues" and it will run the appropriatehermes webhook subscribecommand.

`webhook-subscriptions`
`hermes webhook subscribe`

## Security​

The webhook adapter includes multiple layers of security:

### HMAC signature validation​

The adapter validates incoming webhook signatures using the appropriate method for each source:

- GitHub:X-Hub-Signature-256header — HMAC-SHA256 hex digest prefixed withsha256=
- GitLab:X-Gitlab-Tokenheader — plain secret string match
- Generic (V2, recommended):X-Webhook-Signature-V2+X-Webhook-Timestampheaders — HMAC-SHA256 hex digest of<timestamp>.<body>. The timestamp (Unix seconds) must be within ±300 seconds of the server clock, which prevents captured requests from being replayed later.
- Generic (V1, legacy):X-Webhook-Signatureheader — raw HMAC-SHA256 hex digest of the body only. Still accepted for backward compatibility, but it has no replay protection (a captured request replays indefinitely); the gateway logs a deprecation warning once per route. Switch senders to V2.

`X-Hub-Signature-256`
`sha256=`
`X-Gitlab-Token`
`X-Webhook-Signature-V2`
`X-Webhook-Timestamp`
`<timestamp>.<body>`
`X-Webhook-Signature`

If a secret is configured but no recognized signature header is present, the request is rejected.

### Secret is required​

Every route must have a secret — either set directly on the route or inherited from the globalsecret. Routes without a secret cause the adapter to fail at startup with an error. For development/testing only, you can set the secret to"INSECURE_NO_AUTH"to skip validation entirely.

`secret`
`"INSECURE_NO_AUTH"`

INSECURE_NO_AUTHis only accepted when the gateway is bound to a loopback host (127.0.0.1,localhost,::1). If it is combined with a non-loopback bind such as0.0.0.0or a LAN IP, the adapter refuses to start — this prevents accidentally exposing an unauthenticated endpoint on a public interface.

`INSECURE_NO_AUTH`
`127.0.0.1`
`localhost`
`::1`
`0.0.0.0`

### Rate limiting​

Each route is rate-limited to30 requests per minuteby default (fixed-window). Configure this globally:

```
platforms:  webhook:    extra:      rate_limit: 60  # requests per minute
```

Requests exceeding the limit receive a429 Too Many Requestsresponse.

`429 Too Many Requests`

### Idempotency​

Delivery IDs (fromX-GitHub-Delivery,X-Request-ID, or a timestamp fallback) are cached for1 hour. Duplicate deliveries (e.g. webhook retries) are silently skipped with a200response, preventing duplicate agent runs.

`X-GitHub-Delivery`
`X-Request-ID`
`200`

### Body size limits​

Payloads exceeding1 MBare rejected before the body is read. Configure this:

```
platforms:  webhook:    extra:      max_body_bytes: 2097152  # 2 MB
```

### Authenticated does not mean trusted​

HMAC validation authenticates thesender, not thecontent.A valid signature only proves the request came from a party holding the route's secret (e.g. GitHub). It says nothing about who wrote thebusiness fieldsinside the payload — PR titles, commit messages, issue descriptions, and any other upstream text are authored by arbitrary third parties and must be treated as untrusted.

This is the same trust model that applies to everything the agent reads: web pages, files, and tool output are all untrusted input. Hermes does not — and cannot reliably — sanitize untrusted text with a blocklist; phrasing, encoding, and translation make that trivially bypassable.The trust boundary is the agent's capability surface, not the input channel.Harden there:

- Sandbox the runtime.Run the gateway with the Docker or SSH terminal backend (or in a VM) when exposed to the internet, so a hijacked turn cannot touch the host.
- Scope the toolset.Disableterminal,file, and outbound-action tools on webhook-triggered sessions if the route only needs to read and summarize. Fewer capabilities means a smaller blast radius if a payload field carries injected instructions.
- Keep approvals onfor any destructive or outbound operation, so an injected instruction cannot act unattended.
- Template narrowly.Prefer a specificpromptwith named fields ({pull_request.title}) over{__raw__}or an empty template that dumps the whole payload, so only the fields you intend reach the prompt.

`terminal`
`file`
`prompt`
`{pull_request.title}`
`{__raw__}`

## Troubleshooting​

### Webhook not arriving​

- Verify the port is exposed and accessible from the webhook source
- Check firewall rules — port8644(or your configured port) must be open
- Verify the URL path matches:http://your-server:8644/webhooks/<route-name>
- Use the/healthendpoint to confirm the server is running

`8644`
`http://your-server:8644/webhooks/<route-name>`
`/health`

### Signature validation failing​

- Ensure the secret in your route config exactly matches the secret configured in the webhook source
- For GitHub, the secret is HMAC-based — checkX-Hub-Signature-256
- For GitLab, the secret is a plain token match — checkX-Gitlab-Token
- Check gateway logs forInvalid signaturewarnings

`X-Hub-Signature-256`
`X-Gitlab-Token`
`Invalid signature`

### Event being ignored​

- Check that the event type is in your route'seventslist
- GitHub events use values likepull_request,push,issues(theX-GitHub-Eventheader value)
- GitLab events use values likemerge_request,push(theX-GitLab-Eventheader value)
- Ifeventsis empty or not set, all events are accepted

`events`
`pull_request`
`push`
`issues`
`X-GitHub-Event`
`merge_request`
`push`
`X-GitLab-Event`
`events`

### Agent not responding​

- Run the gateway in foreground to see logs:hermes gateway run
- Check that the prompt template is rendering correctly
- Verify the delivery target is configured and connected

`hermes gateway run`

### Duplicate responses​

- The idempotency cache should prevent this — check that the webhook source is sending a delivery ID header (X-GitHub-DeliveryorX-Request-ID)
- Delivery IDs are cached for 1 hour

`X-GitHub-Delivery`
`X-Request-ID`

### ghCLI errors (GitHub comment delivery)​

`gh`
- Rungh auth loginon the gateway host
- Ensure the authenticated GitHub user has write access to the repository
- Check thatghis installed and on the PATH

`gh auth login`
`gh`

## Environment Variables​

| Variable | Description | Default |
| --- | --- | --- |
| WEBHOOK_ENABLED | Enable the webhook platform adapter | false |
| WEBHOOK_PORT | HTTP server port for receiving webhooks | 8644 |
| WEBHOOK_SECRET | Global HMAC secret (used as fallback when routes don't specify their own) | (none) |

`WEBHOOK_ENABLED`
`false`
`WEBHOOK_PORT`
`8644`
`WEBHOOK_SECRET`