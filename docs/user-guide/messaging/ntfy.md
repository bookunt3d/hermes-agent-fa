---
layout: docs
title: "Messaging_Ntfy"
permalink: /docs/user-guide/messaging_ntfy/
---

- 
- Messaging Platforms
- Other
- ntfy

# ntfy

ntfyis a simple HTTP-based pub-sub notification service. It works with the free public server atntfy.shor any self-hosted instance, and supports any client that can make HTTP requests — phones, browsers, scripts, watches.

`ntfy.sh`

ntfy makes a great lightweight push channel for Hermes: subscribe to a topic from thentfy mobile app, send messages to the topic to talk to the agent, get the response back on your phone.

> Runhermes gateway setupand pickntfyfor a guided walk-through.

Runhermes gateway setupand pickntfyfor a guided walk-through.

`hermes gateway setup`

## Prerequisites​

- A topic name (any unique string —hermes-myname-2026works fine)
- Thentfy mobile appinstalled and subscribed to that topic
- Optional: a self-hosted ntfy server, or anntfy.shaccount token for private/reserved topics

`hermes-myname-2026`
`ntfy.sh`

That's it. No SDK, no daemon, no Node.js. The adapter useshttpxwhich is already a Hermes dependency.

`httpx`

## Configure Hermes​

### Via setup wizard​

```
hermes gateway setup
```

Selectntfyand follow the prompts.

### Via environment variables​

Add these to~/.hermes/.env:

`~/.hermes/.env`

```
NTFY_TOPIC=hermes-myname-2026NTFY_ALLOWED_USERS=hermes-myname-2026NTFY_HOME_CHANNEL=hermes-myname-2026
```

| Variable | Required | Description |
| --- | --- | --- |
| NTFY_TOPIC | Yes | Topic to subscribe to (incoming messages) |
| NTFY_SERVER_URL | Optional | Server URL (default:https://ntfy.sh) — point to a self-hosted ntfy for privacy |
| NTFY_TOKEN | Optional | Bearer token (e.g.tk_xyz) oruser:passfor Basic auth |
| NTFY_PUBLISH_TOPIC | Optional | Different topic for outgoing replies (defaults toNTFY_TOPIC) |
| NTFY_MARKDOWN | Optional | Settrueto send replies withX-Markdown: trueheader |
| NTFY_ALLOWED_USERS | Recommended | Comma-separated topic names allowed (treated as user IDs; see below) |
| NTFY_ALLOW_ALL_USERS | Optional | Settrueto allow every publisher — only safe for private topics with read tokens |
| NTFY_HOME_CHANNEL | Optional | Default topic for cron / notification delivery |
| NTFY_HOME_CHANNEL_NAME | Optional | Human label for the home channel |

`NTFY_TOPIC`
`NTFY_SERVER_URL`
`https://ntfy.sh`
`NTFY_TOKEN`
`tk_xyz`
`user:pass`
`NTFY_PUBLISH_TOPIC`
`NTFY_TOPIC`
`NTFY_MARKDOWN`
`true`
`X-Markdown: true`
`NTFY_ALLOWED_USERS`
`NTFY_ALLOW_ALL_USERS`
`true`
`NTFY_HOME_CHANNEL`
`NTFY_HOME_CHANNEL_NAME`

## Identity model — read this before deploying​

ntfy has no native authenticated user identity. Thetitlefield on a published message ispublisher-controlledand can be anything the sender wants. The Hermes adapter does NOT usetitlefor authorization — it would let any publisher who knows the topic spoof an allowed user.

`title`
`title`

Instead,the topic name itself is the identity. Every message published to the topic is treated as coming from the same logical user (the topic).NTFY_ALLOWED_USERSis therefore typically just the topic name itself — a single-entry allowlist that gates the whole channel.

`NTFY_ALLOWED_USERS`

This meansanyone who knows the topic can talk to the agent. To make that a real trust boundary:

- Self-host ntfyand lock the topic down withAccess Control. Only authorized clients with the read/write token can publish.
- Oruse a private topic on ntfy.sh(reserved topicsrequire an account) and protect it with aNTFY_TOKEN.
- Orpick a long, unguessable topic name(hermes-7d4f9c8b-2026) and treat it as the shared secret. This is the lightest setup but the topic name leaks via any logs or screenshots.

`NTFY_TOKEN`
`hermes-7d4f9c8b-2026`

In all cases, do not put sensitive data through ntfy unless the underlying topic is access-controlled.

## Quick start — talk to your agent from your phone​

1. Pick a topic name:hermes-myname-2026
2. On your phone: install thentfy app, tap+, enterhermes-myname-2026
3. On the host:echo'NTFY_TOPIC=hermes-myname-2026'>>~/.hermes/.envecho'NTFY_ALLOWED_USERS=hermes-myname-2026'>>~/.hermes/.envhermes gateway restart
4. From the ntfy app, send a message to the topic. The agent's reply lands as a push notification.

`hermes-myname-2026`
`hermes-myname-2026`

```
echo 'NTFY_TOPIC=hermes-myname-2026' >> ~/.hermes/.envecho 'NTFY_ALLOWED_USERS=hermes-myname-2026' >> ~/.hermes/.envhermes gateway restart
```

## Using ntfy with cron jobs​

OnceNTFY_HOME_CHANNELis set, cron jobs can deliver to ntfy:

`NTFY_HOME_CHANNEL`

```
cronjob(    action="create",    schedule="every 1h",    deliver="ntfy",          # uses NTFY_HOME_CHANNEL    prompt="Check for alerts and summarise.")
```

Or target a specific topic explicitly via the cron job'sdeliver:field, or from a shell script with thehermes sendCLI:

`deliver:`
`hermes send`

```
hermes send ntfy:alerts-channel "Done!"
```

This works even when the cron runs out-of-process from the gateway — the plugin registers astandalone_sender_fnthat opens its own HTTP connection.

`standalone_sender_fn`

## Self-hosting ntfy​

If you want full control:

```
# Dockerdocker run -p 80:80 -it binwiederhier/ntfy serve# Nativego install heckel.io/ntfy/v2@latestntfy serve
```

Then point Hermes at it:

```
NTFY_SERVER_URL=https://ntfy.mydomain.comNTFY_TOPIC=hermesNTFY_TOKEN=tk_abc123  # if you've set up access control
```

Self-hosting gives you topic access control, message persistence policies, attachments, and emoji tags. See thentfy server docs.

## Markdown formatting​

ntfy clients render markdown when the publisher sets theX-Markdown: trueheader. To enable for outgoing Hermes replies:

`X-Markdown: true`

```
NTFY_MARKDOWN=true
```

Or inconfig.yaml:

`config.yaml`

```
platforms:  ntfy:    extra:      markdown: true
```

The mobile app supports a subset of CommonMark — bold, italic, lists, links, fenced code blocks. Seentfy's markdown docsfor the exact set.

## Outgoing-only setup (notifications without inbound)​

If you only want Hermes topushnotifications to ntfy (cron summaries, alerts) and never accept messages back, set bothNTFY_TOPICandNTFY_PUBLISH_TOPICto the same value and skipNTFY_ALLOWED_USERSentirely. With no allowlist, the agent never responds to inbound messages — your phone gets the pushes, but the conversation is one-way.

`NTFY_TOPIC`
`NTFY_PUBLISH_TOPIC`
`NTFY_ALLOWED_USERS`

## Limits​

- Message size: ntfy caps message bodies at 4096 chars. Hermes truncates with a warning when this is exceeded.
- No typing indicators: the protocol doesn't expose one;send_typingis a no-op.
- No threads or attachments: ntfy is plain push notifications. Long replies stay in the message body, no thread fanout.
- No native user identity: see the identity-model section above.

`send_typing`

## Troubleshooting​

Auth failure / 401—NTFY_TOKENis wrong, or the token doesn't have publish/subscribe rights on this topic. The adapter halts its reconnect loop on 401 and the gateway runtime status will showfatal: ntfy_unauthorized. Fix the token and restart the gateway.

`NTFY_TOKEN`
`fatal: ntfy_unauthorized`

Topic not found / 404—NTFY_TOPICdoesn't exist on the configured server. For ntfy.sh, topics are auto-created on first publish, so a 404 means you're pointed at a self-hosted server that doesn't have the topic provisioned. The adapter halts its reconnect loop withfatal: ntfy_topic_not_found.

`NTFY_TOPIC`
`fatal: ntfy_topic_not_found`

Connected but no messages— Check thatNTFY_ALLOWED_USERSincludes the topic name itself. With ntfy's identity model, the topic IS the user; leaving the allowlist empty rejects everything.

`NTFY_ALLOWED_USERS`

Reconnects every 60s— The stream keepalive default is 55s; ntfy may have intermittent network issues. The adapter applies exponential backoff (2 → 5 → 10 → 30 → 60s) and resets to 0 once a stream stays alive ≥60s.