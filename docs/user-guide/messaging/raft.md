---
layout: docs
title: "Messaging_Raft"
permalink: /docs/user-guide/messaging_raft/
---

# Raft Setup

Hermes connects toRaftas an external agent through a local wake-channel bridge. The adapter starts a loopback HTTP endpoint that receives content-free wake hints from the bridge, then injects them into the Hermes gateway session pipeline. The agent reads and sends messages through the Raft CLI — the adapter never touches message bodies or delivery cursors.

- The bridgeowns: wake-hint consumption, dedup, backoff, reconnection, at-least-once delivery, and proof logging.
- The Hermes adapterowns: a localhost wake endpoint and injecting a short notice into the agent's context.
- The agentowns: pulling messages (raft message check), replying (raft message send), and all other Raft interactions via the CLI.

`raft message check`
`raft message send`

The adapter holds no Raft credentials — only a per-session shared token for localhost auth between the bridge and the endpoint.

## Prerequisites​

- ARaft workspacewhere you can create an External Agent
- TheRaft CLIinstalled and logged in to that External Agent profile
- aiohttp— Python package (included in Hermes[all]extras)

`[all]`

In Raft, open the Agents menu, create an External Agent, and follow the setup card to install the Raft CLI and log in the agent profile. Once the agent is created, Raft shows a Hermes setup guide with the environment variables and configuration needed to start the gateway.

## Setup​

Add to~/.hermes/.env:

`~/.hermes/.env`

```
RAFT_PROFILE=your-agent-profile
```

That's it — the adapter auto-enables whenRAFT_PROFILEis set. It generates a per-session bridge token, picks an ephemeral port, and spawns the bridge child process automatically when the gateway starts.

`RAFT_PROFILE`

## How It Works​

```
Raft Server → Bridge (wake-hints SSE) → POST /wake → Hermes Adapter → Agent contextAgent → raft message check → Raft Server (message bodies)Agent → raft message send → Raft Server (replies)
```

1. The Raft server sends wake hints to the bridge process via SSE.
2. The bridge forwards each hint as aPOST /waketo the adapter's loopback endpoint.
3. The adapter validates the bridge token, verifies the payload is content-free, and injects a wake notice into the Hermes session.
4. The agent sees the wake notice and uses the Raft CLI to read messages and reply.

`POST /wake`

Wake payloads arecontent-free by contract— they carry metadata (event ID, message ID, timestamps) but never message bodies, channel names, or sender identities. The adapter rejects any payload containing content-shaped fields (text,body,content,messages, etc.).

`text`
`body`
`content`
`messages`

## Bridge​

The adapter automatically spawnsraft agent bridgeas a child process, passing the endpoint URL and token. The bridge connects to the Raft server using the configured profile and begins forwarding wake hints. It is terminated when the gateway shuts down.

`raft agent bridge`

## Environment Variables​

| Variable | Description | Default |
| --- | --- | --- |
| RAFT_PROFILE | Raft agent profile slug — auto-enables the adapter when set | (required) |

`RAFT_PROFILE`