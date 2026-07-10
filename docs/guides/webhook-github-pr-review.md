---
layout: docs
title: "Webhook بررسی PR گیتهاب"
permalink: /docs/guides/webhook-github-pr-review/
---

- 
- Guides & Tutorials
- GitHub PR Reviews via Webhook

# Automated GitHub PR Comments with Webhooks

This guide walks you through connecting Hermes Agent to GitHub so it automatically fetches a pull request's diff, analyzes the code changes, and posts a comment — triggered by a webhook event with no manual prompting.

When a PR is opened or updated, GitHub sends a webhook POST to your Hermes instance. Hermes runs the agent with a prompt that instructs it to retrieve the diff via theghCLI, and the response is posted back to the PR thread.

`gh`

If you don't have a public URL or just want to get started quickly, check outBuild a GitHub PR Review Agent— uses cron jobs to poll for PRs on a schedule, works behind NAT and firewalls.

For the full webhook platform reference (all config options, delivery types, dynamic subscriptions, security model) seeWebhooks.

Webhook payloads contain attacker-controlled data — PR titles, commit messages, and descriptions can contain malicious instructions. When your webhook endpoint is exposed to the internet, run the gateway in a sandboxed environment (Docker, SSH backend). See thesecurity sectionbelow.

## Prerequisites​

- Hermes Agent installed and running (hermes gateway)
- ghCLIinstalled and authenticated on the gateway host (gh auth login)
- A publicly reachable URL for your Hermes instance (seeLocal testing with ngrokif running locally)
- Admin access to the GitHub repository (required to manage webhooks)

`hermes gateway`
`gh`
`gh auth login`

## Step 1 — Enable the webhook platform​

Add the following to your~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
platforms:  webhook:    enabled: true    extra:      port: 8644          # default; change if another service occupies this port      rate_limit: 30      # max requests per minute per route (not a global cap)      routes:        github-pr-review:          secret: "your-webhook-secret-here"   # must match the GitHub webhook secret exactly          events:            - pull_request          # The agent is instructed to fetch the actual diff before reviewing.          # {number} and {repository.full_name} are resolved from the GitHub payload.          prompt: |            A pull request event was received (action: {action}).            PR #{number}: {pull_request.title}            Author: {pull_request.user.login}            Branch: {pull_request.head.ref} → {pull_request.base.ref}            Description: {pull_request.body}            URL: {pull_request.html_url}            If the action is "closed" or "labeled", stop here and do not post a comment.            Otherwise:            1. Run: gh pr diff {number} --repo {repository.full_name}            2. Review the code changes for correctness, security issues, and clarity.            3. Write a concise, actionable review comment and post it.          deliver: github_comment          deliver_extra:            repo: "{repository.full_name}"            pr_number: "{number}"
```

Key fields:

| Field | Description |
| --- | --- |
| secret(route-level) | HMAC secret for this route. Falls back toextra.secretglobal if omitted. |
| events | List ofX-GitHub-Eventheader values to accept. Empty list = accept all. |
| prompt | Template;{field}and{nested.field}resolve from the GitHub payload. |
| deliver | github_commentposts viagh pr comment.logjust writes to the gateway log. |
| deliver_extra.repo | Resolves to e.g.org/repofrom the payload. |
| deliver_extra.pr_number | Resolves to the PR number from the payload. |

`secret`
`extra.secret`
`events`
`X-GitHub-Event`
`prompt`
`{field}`
`{nested.field}`
`deliver`
`github_comment`
`gh pr comment`
`log`
`deliver_extra.repo`
`org/repo`
`deliver_extra.pr_number`

The GitHub webhook payload includes PR metadata (title, description, branch names, URLs) butnot the diff. The prompt above instructs the agent to rungh pr diffto fetch the actual changes. Theterminaltool is included in the defaulthermes-webhooktoolset, so no extra configuration is needed.

`gh pr diff`
`terminal`
`hermes-webhook`

## Step 2 — Start the gateway​

```
hermes gateway
```

You should see:

```
[webhook] Listening on 0.0.0.0:8644 — routes: github-pr-review
```

Verify it's running:

```
curl http://localhost:8644/health# {"status": "ok", "platform": "webhook"}
```

## Step 3 — Register the webhook on GitHub​

1. Go to your repository →Settings→Webhooks→Add webhook
2. Fill in:Payload URL:https://your-public-url.example.com/webhooks/github-pr-reviewContent type:application/jsonSecret:the same value you set forsecretin the route configWhich events?→ Select individual events → checkPull requests
3. ClickAdd webhook

- Payload URL:https://your-public-url.example.com/webhooks/github-pr-review
- Content type:application/json
- Secret:the same value you set forsecretin the route config
- Which events?→ Select individual events → checkPull requests

`https://your-public-url.example.com/webhooks/github-pr-review`
`application/json`
`secret`

GitHub will immediately send apingevent to confirm the connection. It is safely ignored —pingis not in youreventslist — and returns{"status": "ignored", "event": "ping"}. It is only logged at DEBUG level, so it won't appear in the console at the default log level.

`ping`
`ping`
`events`
`{"status": "ignored", "event": "ping"}`

## Step 4 — Open a test PR​

Create a branch, push a change, and open a PR. Within 30–90 seconds (depending on PR size and model), Hermes should post a review comment.

To follow the agent's progress in real time:

```
tail -f "${HERMES_HOME:-$HOME/.hermes}/logs/gateway.log"
```

## Local testing with ngrok​

If Hermes is running on your laptop, usengrokto expose it:

```
ngrok http 8644
```

Copy thehttps://...ngrok-free.appURL and use it as your GitHub Payload URL. On the free ngrok tier the URL changes each time ngrok restarts — update your GitHub webhook each session. Paid ngrok accounts get a static domain.

`https://...ngrok-free.app`

You can smoke-test a static route directly withcurl— no GitHub account or real PR needed.

`curl`
`deliver: log`

Changedeliver: github_commenttodeliver: login your config while testing. Otherwise the agent will attempt to post a comment to the fakeorg/repo#99repo in the test payload, which will fail. Switch back todeliver: github_commentonce you're satisfied with the prompt output.

`deliver: github_comment`
`deliver: log`
`org/repo#99`
`deliver: github_comment`

```
SECRET="your-webhook-secret-here"BODY='{"action":"opened","number":99,"pull_request":{"title":"Test PR","body":"Adds a feature.","user":{"login":"testuser"},"head":{"ref":"feat/x"},"base":{"ref":"main"},"html_url":"https://github.com/org/repo/pull/99"},"repository":{"full_name":"org/repo"}}'SIG=$(printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$SECRET" -hex | awk '{print "sha256="$2}')curl -s -X POST http://localhost:8644/webhooks/github-pr-review \  -H "Content-Type: application/json" \  -H "X-GitHub-Event: pull_request" \  -H "X-Hub-Signature-256: $SIG" \  -d "$BODY"# Expected: {"status":"accepted","route":"github-pr-review","event":"pull_request","delivery_id":"..."}
```

Then watch the agent run:

```
tail -f "${HERMES_HOME:-$HOME/.hermes}/logs/gateway.log"
```

hermes webhook test <name>only works fordynamic subscriptionscreated withhermes webhook subscribe. It does not read routes fromconfig.yaml.

`hermes webhook test <name>`
`hermes webhook subscribe`
`config.yaml`

## Filtering to specific actions​

GitHub sendspull_requestevents for many actions:opened,synchronize,reopened,closed,labeled, etc. Theeventslist filters by theX-GitHub-Eventheader value, and route-levelfilterscan narrow by payload fields such asaction.

`pull_request`
`opened`
`synchronize`
`reopened`
`closed`
`labeled`
`events`
`X-GitHub-Event`
`filters`
`action`

The prompt in Step 1 already handles this by instructing the agent to stop early forclosedandlabeledevents.

`closed`
`labeled`

The "stop here" instruction prevents a meaningful review, but the agent still runs to completion for everypull_requestevent regardless of action. Prefer filtering before the agent wakes:

`pull_request`

```
filters:  - field: "action"    in: ["opened", "synchronize", "reopened"]
```

For high-volume repositories, you can still filter upstream with a GitHub Actions workflow that calls your webhook URL conditionally.

> There is no Jinja2 or conditional template syntax.{field}and{nested.field}are the only substitutions supported. Anything else is passed verbatim to the agent.

There is no Jinja2 or conditional template syntax.{field}and{nested.field}are the only substitutions supported. Anything else is passed verbatim to the agent.

`{field}`
`{nested.field}`

## Using a skill for consistent review style​

Load aHermes skillto give the agent a consistent review persona. Addskillsto your route insideplatforms.webhook.extra.routesinconfig.yaml:

`skills`
`platforms.webhook.extra.routes`
`config.yaml`

```
platforms:  webhook:    enabled: true    extra:      routes:        github-pr-review:          secret: "your-webhook-secret-here"          events: [pull_request]          prompt: |            A pull request event was received (action: {action}).            PR #{number}: {pull_request.title} by {pull_request.user.login}            URL: {pull_request.html_url}            If the action is "closed" or "labeled", stop here and do not post a comment.            Otherwise:            1. Run: gh pr diff {number} --repo {repository.full_name}            2. Review the diff using your review guidelines.            3. Write a concise, actionable review comment and post it.          skills:            - review          deliver: github_comment          deliver_extra:            repo: "{repository.full_name}"            pr_number: "{number}"
```

> Note:Only the first skill in the list that is found is loaded. Hermes does not stack multiple skills — subsequent entries are ignored.

Note:Only the first skill in the list that is found is loaded. Hermes does not stack multiple skills — subsequent entries are ignored.

## Sending responses to Slack or Discord instead​

Replace thedeliveranddeliver_extrafields inside your route with your target platform:

`deliver`
`deliver_extra`

```
# Inside platforms.webhook.extra.routes.<route-name>:# Slackdeliver: slackdeliver_extra:  chat_id: "C0123456789"   # Slack channel ID (omit to use the configured home channel)# Discorddeliver: discorddeliver_extra:  chat_id: "987654321012345678"  # Discord channel ID (omit to use home channel)
```

The target platform must also be enabled and connected in the gateway. Ifchat_idis omitted, the response is sent to that platform's configured home channel.

`chat_id`

Validdelivervalues:log·github_comment·telegram·discord·slack·signal·sms

`deliver`
`log`
`github_comment`
`telegram`
`discord`
`slack`
`signal`
`sms`

## GitLab support​

The same adapter works with GitLab. GitLab usesX-Gitlab-Tokenfor authentication (plain string match, not HMAC) — Hermes handles both automatically.

`X-Gitlab-Token`

For event filtering, GitLab setsX-GitLab-Eventto values likeMerge Request Hook,Push Hook,Pipeline Hook. Use the exact header value inevents:

`X-GitLab-Event`
`Merge Request Hook`
`Push Hook`
`Pipeline Hook`
`events`

```
events:  - Merge Request Hook
```

GitLab payload fields differ from GitHub's — e.g.{object_attributes.title}for the MR title and{object_attributes.iid}for the MR number. The easiest way to discover the full payload structure is GitLab'sTestbutton in your webhook settings, combined with theRecent Deliverieslog. Alternatively, omitpromptfrom your route config — Hermes will then pass the full payload as formatted JSON directly to the agent, and the agent's response (visible in the gateway log withdeliver: log) will describe its structure.

`{object_attributes.title}`
`{object_attributes.iid}`
`prompt`
`deliver: log`

## Security notes​

- Never useINSECURE_NO_AUTHin production — it disables signature validation entirely. It is only for local development.
- Rotate your webhook secretperiodically and update it in both GitHub (webhook settings) and yourconfig.yaml.
- Rate limitingis 30 req/min per route by default (configurable viaextra.rate_limit). Exceeding it returns429.
- Duplicate deliveries(webhook retries) are deduplicated via a 1-hour idempotency cache. The cache key isX-GitHub-Deliveryif present, thenX-Request-ID, then a millisecond timestamp. When neither delivery ID header is set, retries arenotdeduplicated.
- Prompt injection:PR titles, descriptions, and commit messages are attacker-controlled. Malicious PRs could attempt to manipulate the agent's actions. Run the gateway in a sandboxed environment (Docker, VM) when exposed to the public internet.

`INSECURE_NO_AUTH`
`config.yaml`
`extra.rate_limit`
`429`
`X-GitHub-Delivery`
`X-Request-ID`

## Troubleshooting​

| Symptom | Check |
| --- | --- |
| 401 Invalid signature | Secret in config.yaml doesn't match GitHub webhook secret |
| 404 Unknown route | Route name in the URL doesn't match the key inroutes: |
| 429 Rate limit exceeded | 30 req/min per route exceeded — common when re-delivering test events from GitHub's UI; wait a minute or raiseextra.rate_limit |
| No comment posted | ghnot installed, not on PATH, or not authenticated (gh auth login) |
| Agent runs but no comment | Check the gateway log — if the agent output was empty or just "SKIP", delivery is still attempted |
| Port already in use | Changeextra.portin config.yaml |
| Agent runs but reviews only the PR description | The prompt isn't including thegh pr diffinstruction — the diff is not in the webhook payload |
| Can't see the ping event | Ignored events return{"status":"ignored","event":"ping"}at DEBUG log level only — check GitHub's delivery log (repo → Settings → Webhooks → your webhook → Recent Deliveries) |

`401 Invalid signature`
`404 Unknown route`
`routes:`
`429 Rate limit exceeded`
`extra.rate_limit`
`gh`
`gh auth login`
`extra.port`
`gh pr diff`
`{"status":"ignored","event":"ping"}`

GitHub's Recent Deliveries tab(repo → Settings → Webhooks → your webhook) shows the exact request headers, payload, HTTP status, and response body for every delivery. It is the fastest way to diagnose failures without touching your server logs.

## Full config reference​

```
platforms:  webhook:    enabled: true    extra:      host: "0.0.0.0"         # bind address (default: 0.0.0.0)      port: 8644               # listen port (default: 8644)      secret: ""               # optional global fallback secret      rate_limit: 30           # requests per minute per route      max_body_bytes: 1048576  # payload size limit in bytes (default: 1 MB)      routes:        <route-name>:          secret: "required-per-route"          events: []            # [] = accept all; otherwise list X-GitHub-Event values          prompt: ""            # {field} / {nested.field} resolved from payload          skills: []            # first matching skill is loaded (only one)          deliver: "log"        # log | github_comment | telegram | discord | slack | signal | sms          deliver_extra: {}     # repo + pr_number for github_comment; chat_id for others
```

## What's Next?​

- Cron-Based PR Reviews— poll for PRs on a schedule, no public endpoint needed
- Webhook Reference— full config reference for the webhook platform
- Build a Plugin— package review logic into a shareable plugin
- Profiles— run a dedicated reviewer profile with its own memory and config