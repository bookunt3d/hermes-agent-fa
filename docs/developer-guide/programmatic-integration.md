---
layout: docs
title: "یکپارچه‌سازی برنامه‌نویسی"
permalink: /docs/developer-guide/programmatic-integration/
---

- 
- Developer Guide
- Architecture
- Programmatic Integration

# Programmatic Integration

Hermes ships three protocols for driving the agent from external programs — IDE plugins, custom UIs, CI pipelines, embedded sub-agents. Pick the one that matches your transport and consumer.

| Protocol | Transport | Best for | Defined by |
| --- | --- | --- | --- |
| ACP | JSON-RPC over stdio | IDE clients (VS Code, Zed, JetBrains) that already speak theAgent Client Protocol | acp_adapter/ |
| TUI gateway | JSON-RPC over stdio (or WebSocket) | Custom hosts that want fine-grained control of sessions, slash commands, approvals, and streaming events | tui_gateway/server.py |
| API server | HTTP + Server-Sent Events | OpenAI-compatible frontends (Open WebUI, LobeChat, LibreChat…) and language-agnostic web clients | gateway/platforms/api_server.py |

`acp_adapter/`
`tui_gateway/server.py`
`gateway/platforms/api_server.py`

All three drive the sameAIAgentcore. They differ only in wire format and which set of features they expose.

`AIAgent`

## ACP (Agent Client Protocol)​

hermes acpstarts a stdio JSON-RPC server speaking ACP. Used in production by VS Code (Zed Industries' ACP extension), Zed, and any JetBrains IDE with an ACP plugin.

`hermes acp`

Capabilities exposed: session creation, prompt submission, streaming agent message chunks, tool-call events, permission requests, session fork, cancel, and authentication. Tool output is rendered into ACPDiff/ToolCallcontent blocks the IDE understands.

`Diff`
`ToolCall`

Full lifecycle, event bridge, and approval flow:ACP Internals.

```
hermes acp                  # serve ACP on stdiohermes acp --bootstrap      # print install snippet for an ACP-capable IDE
```

## TUI Gateway JSON-RPC​

tui_gateway/server.pyis the protocol the Ink TUI (hermes --tui) and the embedded dashboard PTY bridge talk to. Any external host can speak the same protocol over stdio (or WebSocket viatui_gateway/ws.py).

`tui_gateway/server.py`
`hermes --tui`
`tui_gateway/ws.py`

### Method catalog (selected)​

```
prompt.submit           prompt.background       session.steersession.create          session.list            session.active_listsession.activate        session.close           session.interruptsession.history         session.compress        session.branchsession.title           session.usage           session.statusclarify.respond         sudo.respond            secret.respondapproval.respond        config.set / config.get commands.catalogcommand.resolve         command.dispatch        cli.execreload.mcp              reload.env              process.stopdelegation.status       subagent.interrupt      spawn_tree.save / list / loadterminal.resize         clipboard.paste         image.attach
```

session.active_list,session.activate, andsession.closeare the process-local live-session controls used by the TUI session switcher. Usesession.list//resumefor saved transcript discovery; use the active-session methods only for sessions that are currently open in the TUI gateway process.

`session.active_list`
`session.activate`
`session.close`
`session.list`
`/resume`

### Events streamed back​

message.delta,message.complete,tool.start,tool.progress,tool.complete,approval.request,clarify.request,sudo.request,secret.request,gateway.ready, plus session lifecycle and error events.

`message.delta`
`message.complete`
`tool.start`
`tool.progress`
`tool.complete`
`approval.request`
`clarify.request`
`sudo.request`
`secret.request`
`gateway.ready`

### Pi-style RPC mapping​

Every command in the Pi-mono RPC spec (issue #360) has a TUI-gateway equivalent:

| Pi command | Hermes equivalent |
| --- | --- |
| prompt | prompt.submit(or ACPsession/prompt) |
| steer | session.steer |
| follow_up | prompt.submitqueued after current turn |
| abort | session.interrupt |
| set_model | command.dispatchfor/model <provider:model>(mid-session, persistent) |
| compact | session.compress |
| get_state | session.status |
| get_messages | session.history |
| switch_session | session.resume |
| fork | session.branch |
| ui_request/ui_response | clarify.respond/sudo.respond/secret.respond/approval.respond |

`prompt`
`prompt.submit`
`session/prompt`
`steer`
`session.steer`
`follow_up`
`prompt.submit`
`abort`
`session.interrupt`
`set_model`
`command.dispatch`
`/model <provider:model>`
`compact`
`session.compress`
`get_state`
`session.status`
`get_messages`
`session.history`
`switch_session`
`session.resume`
`fork`
`session.branch`
`ui_request`
`ui_response`
`clarify.respond`
`sudo.respond`
`secret.respond`
`approval.respond`

## OpenAI-Compatible API Server​

gateway/platforms/api_server.pyexposes hermes over HTTP for any client that already speaks the OpenAI format. Useful when you want a web frontend, a curl-driven CI runner, or a non-Python consumer.

`gateway/platforms/api_server.py`

Endpoints:

```
POST /v1/chat/completions        OpenAI Chat Completions (streaming via SSE)POST /v1/responses               OpenAI Responses API (stateful)POST /v1/runs                    Start a run, returns run_id (202)GET  /v1/runs/{id}               Run statusGET  /v1/runs/{id}/events        SSE stream of lifecycle eventsPOST /v1/runs/{id}/approval      Resolve a pending approvalPOST /v1/runs/{id}/stop          Interrupt the runGET  /v1/capabilities            Machine-readable feature flagsGET  /v1/models                  Lists hermes-agentGET  /health, /health/detailed
```

Setup, headers (X-Hermes-Session-Id,X-Hermes-Session-Key), and frontend wiring:API Server.

`X-Hermes-Session-Id`
`X-Hermes-Session-Key`

## Which one should I use?​

- You're writing an IDE plugin and the IDE already speaks ACP→ ACP. Zero protocol work on the IDE side.
- You're writing a custom desktop / web / TUI host and want every Hermes feature(slash commands, approvals, clarify, multi-agent, session branching) → TUI gateway JSON-RPC.
- You want any OpenAI-compatible frontend, a language-agnostic HTTP client, or curl-driven automation→ API server.
- You want a Python in-process embed without a subprocess→ importrun_agent.AIAgentdirectly. SeeAgent Loop.

`run_agent.AIAgent`

## Model hot-swapping​

Mid-session model switching works on every surface — it's the/modelslash command under the hood.

`/model`
- CLI / TUI:/model claude-sonnet-4or/model openrouter:anthropic/claude-sonnet-4.6
- TUI gateway RPC:command.dispatchwith{"command": "/model claude-sonnet-4"}
- ACP:the IDE sends the slash command as a prompt; the agent dispatches it
- API server:include amodelfield in the request body or setX-Hermes-Model

`/model claude-sonnet-4`
`/model openrouter:anthropic/claude-sonnet-4.6`
`command.dispatch`
`{"command": "/model claude-sonnet-4"}`
`model`
`X-Hermes-Model`

Provider-aware resolution (the same model name picks the right format for whatever provider you're on) is built in. Seehermes_cli/model_switch.py.

`hermes_cli/model_switch.py`

## A note on--mode rpc​

`--mode rpc`

Hermes does not have a--mode rpcflag. The three protocols above already cover the use cases — ACP for IDE-protocol clients, the TUI gateway for stdio JSON-RPC hosts, and the API server for HTTP. If you find a real gap that none of them fill, open an issue with the concrete consumer you're building.

`--mode rpc`