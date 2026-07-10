---
layout: docs
title: "Features_Tool Search"
permalink: /docs/user-guide/features/tool-search/
---

- 
- Features
- Core
- Tool Search

# Tool Search

When you have many MCP servers or non-core plugin tools attached to a
session, their JSON schemas can consume a substantial fraction of the
context window on every turn — even when only a few of them are relevant
to what the user actually asked for.

Tool Searchis Hermes' opt-in progressive-disclosure layer for that
problem. When activated, MCP and plugin tools are replaced in the
model-visible tools array by three bridge tools, and the model loads each
specific tool's schema on demand.

The tools that make up Hermes' core capability set (terminal,read_file,write_file,patch,search_files,todo,memory,browser_*,web_search,web_extract,clarify,execute_code,delegate_task,session_search, and the rest of_HERMES_CORE_TOOLS) arealwaysloaded directly. Only MCP tools and
non-core plugin tools are eligible for deferral.

`terminal`
`read_file`
`write_file`
`patch`
`search_files`
`todo`
`memory`
`browser_*`
`web_search`
`web_extract`
`clarify`
`execute_code`
`delegate_task`
`session_search`
`_HERMES_CORE_TOOLS`

## How it works​

When Tool Search activates for a turn, the model sees three new tools in
place of the deferred ones:

```
tool_search(query, limit?)     — search the deferred-tool catalogtool_describe(name)            — load the full schema for one tooltool_call(name, arguments)     — invoke a deferred tool
```

A typical interaction looks like:

```
Model: tool_search("create a github issue")  → { matches: [{ name: "mcp_github_create_issue", ... }, ...] }Model: tool_describe("mcp_github_create_issue")  → { parameters: { type: "object", properties: { ... } } }Model: tool_call("mcp_github_create_issue", { title: "...", body: "..." })  → { ok: true, issue_number: 42 }
```

When the model invokestool_call, Hermesunwraps the bridgeand
dispatches the underlying tool exactly as if the model had called it
directly. Pre-tool-call hooks, guardrails, approval prompts, and
post-tool-call hooks all run against the real tool name — not againsttool_call. The activity feed in the CLI and gateway also unwraps so you
see the underlying tool, not the bridge.

`tool_call`
`tool_call`

## When does it activate?​

By default Tool Search runs inautomode: it activates only when the
deferrable tool schemas would consume at least 10% of the active model's
context window. Below that, the tools-array assembly is a pure
pass-through and you pay no overhead.

`auto`

This decision is re-evaluated every time the tools array is built, so:

- A session with just a few MCP tools and a long context model never
activates Tool Search.
- A session with many MCP servers attached (15+ tools typically) starts
activating it.
- Removing MCP servers mid-session correctly returns to direct exposure
on the next assembly.

## Configuration​

```
tools:  tool_search:    enabled: auto       # auto (default), on, or off    threshold_pct: 10   # percentage of context — only used in auto mode    search_default_limit: 5    max_search_limit: 20
```

| Key | Default | Meaning |
| --- | --- | --- |
| enabled | auto | autoactivates above threshold;onalways activates if there's at least one deferrable tool;offdisables entirely. |
| threshold_pct | 10 | Percentage of context length at whichautomode kicks in. Range 0–100. |
| search_default_limit | 5 | Hits returned when the model callstool_searchwithout alimit. |
| max_search_limit | 20 | Hard upper bound the model can request vialimit. Range 1–50. |

`enabled`
`auto`
`auto`
`on`
`off`
`threshold_pct`
`10`
`auto`
`search_default_limit`
`5`
`tool_search`
`limit`
`max_search_limit`
`20`
`limit`

You can also flip the legacy boolean shape:

```
tools:  tool_search: true   # equivalent to {enabled: auto}
```

## When NOT to use it​

Tool Search trades a fixed per-turn token cost (the three bridge tool
schemas, ~300 tokens) and at least one extra round trip (search →
describe → call) for the savings on the deferred schemas. It's a clear
win when you have many tools and use few per turn; it's overhead when
you have few tools total.

Theautodefault handles this for you. If you setenabled: onunconditionally, expect a slight per-turn cost on small toolsets.

`auto`
`enabled: on`

## Trade-offs that don't go away​

These come from the prompt-cache integrity invariant — they are inherent
to any progressive-disclosure design, not specific to this implementation:

- One extra round trip on cold tools.The first time the model needs
a deferred tool, it spends one or two extra model calls to find and
load the schema. The token savings on the static side are real, but a
portion is paid back at runtime.
- No cache benefit on deferred schemas.A loadedtool_describeresult enters the conversation history (so it does get cached on
subsequent turns) but it never benefits from the system-prompt cache
prefix.
- Model-quality dependence.Tool Search assumes the model can write a
reasonable search query for the tool it wants. Smaller models do this
less well; the published Anthropic numbers (49% → 74% on Opus 4 with
vs. without tool search) show the upside but also that ~26 points of
accuracy is still retrieval failure.
- Toolset edits invalidate cache.Adding or removing a tool mid-
session changes the bridge tools' descriptions (which include the
count of deferred tools) and the catalog, so the prompt cache is
invalidated. This is the same trade-off as any toolset edit.

`tool_describe`

## Implementation details​

- Retrieval:BM25 over tokenized tool name + description + parameter
names. Falls back to a literal substring match on the tool name when
BM25 returns no positive-score hits, which protects against
zero-IDF degenerate cases (e.g. searching"github"against a
catalog where every tool name contains "github").
- Catalog is stateless across turns.It rebuilds from the current
tool-defs list every assembly — no session-keyedMap. This avoids
the class of bug where a stored catalog drifts out of sync with the
live tool registry.
- The catalog is scoped to the session's toolsets.tool_search,tool_describe, andtool_callonly ever see and invoke tools the
session was actually granted. A subagent, kanban worker, or gateway
session restricted to a subset of toolsets cannot use the bridge to
discover or call a tool outside that subset — the deferred catalog is
the deferrable slice of the session's own enabled/disabled toolsets,
not the whole process registry.
- No JS sandbox.Hermes uses the simpler "structured tools" mode
(search / describe / call as plain functions). The JS-sandbox "code
mode" some other implementations offer is a large surface area; we
skip it.

`"github"`
`Map`
`tool_search`
`tool_describe`
`tool_call`

## See also​

- tools/tool_search.py— the implementation
- tests/tools/test_tool_search.py— the regression suite
- Theopenclaw-tool-search-reportPDF in the original implementation
PR for the research that shaped the design

`tools/tool_search.py`
`tests/tools/test_tool_search.py`
`openclaw-tool-search-report`