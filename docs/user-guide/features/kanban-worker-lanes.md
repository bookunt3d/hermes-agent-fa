---
layout: docs
title: "Features_Kanban Worker Lanes"
permalink: /docs/user-guide/features_kanban-worker-lanes/
---

- 
- Features
- Automation
- Kanban worker lanes

# Kanban worker lanes

Aworker laneis a class of process that the kanban dispatcher can route tasks to. Each lane has an identity (the assignee string), a spawn mechanism, and a contract for what it must do with the task once spawned.

This page is the contract. It exists for two audiences:

- Operatorspicking which lanes to wire into a board (which profiles to create, which assignees to use).
- Plugin / integration authorswanting to add a new lane shape (a CLI worker that wraps Codex / Claude Code / OpenCode, a containerised review worker, a non-Hermes service that pulls tasks via the API).

If you're writing the worker code itself — the agent that runsinsidea lane — the kanban lifecycle and reference details are injected into the worker's system prompt automatically (theKANBAN_GUIDANCEblock inagent/prompt_builder.py).

`KANBAN_GUIDANCE`
`agent/prompt_builder.py`

## The hierarchy​

```
Hermes Kanban  =  canonical task lifecycle + audit trailWorker lane    =  implementation executor for one assigned cardReviewer       =  human or human-proxy that gates "done"GitHub PR      =  upstreamable artifact (optional, for code lanes)
```

Hermes Kanban owns lifecycle truth —ready→running→blocked/done/archived. Worker lanes execute work but never own that truth; everything they do flows back through the kanban kernel via thekanban_*tools (or, for non-Hermes external workers, via the API). Reviewers gate the transition from "code change written" to "task done."

`ready`
`running`
`blocked`
`done`
`archived`
`kanban_*`

## What a lane provides​

To be a kanban worker lane, an integration must provide three things:

### 1. An assignee string​

The dispatcher matchestask.assigneeagainst either a Hermes profile name (the default lane shape) or a registered non-spawnable identifier (the plugin lane shape — seeAdding an external CLI worker lanebelow). Tasks whose assignee doesn't resolve are left onreadywith askipped_nonspawnableevent so a board operator can fix them; they are not silently dropped or executed by an arbitrary fallback.

`task.assignee`
`ready`
`skipped_nonspawnable`

### 2. A spawn mechanism​

For Hermes profile lanes, the dispatcher's_default_spawnrunshermes -p <assignee> chat -q <prompt>(or the equivalent module form when thehermesshim isn't on$PATH) inside the task's pinned workspace, with these env vars set:

`_default_spawn`
`hermes -p <assignee> chat -q <prompt>`
`hermes`
`$PATH`
| Variable | Carries |
| --- | --- |
| HERMES_KANBAN_TASK | the task id the worker is operating on |
| HERMES_KANBAN_DB | absolute path to the per-board SQLite file |
| HERMES_KANBAN_BOARD | board slug |
| HERMES_KANBAN_WORKSPACES_ROOT | root of the board's workspace tree |
| HERMES_KANBAN_WORKSPACE | absolute path tothistask's workspace |
| HERMES_KANBAN_RUN_ID | the current run's id (for the lifecycle gate) |
| HERMES_KANBAN_CLAIM_LOCK | the claim lock string (<host>:<pid>:<uuid>) |
| HERMES_PROFILE | the worker's own profile name (forkanban_commentauthor attribution) |
| HERMES_TENANT | tenant namespace, if the task has one |

`HERMES_KANBAN_TASK`
`HERMES_KANBAN_DB`
`HERMES_KANBAN_BOARD`
`HERMES_KANBAN_WORKSPACES_ROOT`
`HERMES_KANBAN_WORKSPACE`
`HERMES_KANBAN_RUN_ID`
`HERMES_KANBAN_CLAIM_LOCK`
`<host>:<pid>:<uuid>`
`HERMES_PROFILE`
`kanban_comment`
`HERMES_TENANT`

For non-Hermes lanes (registered via a plugin), the plugin supplies its ownspawn_fncallable that getstask,workspace, andboardand returns an optional pid for crash detection.

`spawn_fn`
`task`
`workspace`
`board`

### 3. A lifecycle terminator​

Every claim must end in exactly one of:

- kanban_complete(summary=..., metadata=...)— task succeeds, status flips todone.
- kanban_block(reason=...)— task waits for human input, status flips toblocked. The dispatcher respawns whenkanban_unblockruns.
- The worker process exits without a tool call. The kernel reaps it and emitscrashed(PID died) orgave_up(consecutive-failure breaker tripped) ortimed_out(max_runtime exceeded). This is the failure path; healthy workers don't end here.

`kanban_complete(summary=..., metadata=...)`
`done`
`kanban_block(reason=...)`
`blocked`
`kanban_unblock`
`crashed`
`gave_up`
`timed_out`

The kanban kernel enforces that exactly one of these terminates each run. A worker that calls neither and exits normally is treated as crashed.

## Outputs and the review-required convention​

For most code-changing tasks, the work isn't trulydonethe moment the worker finishes — it needs a human reviewer. The kanban kernel doesn't enforce this distinction (a "code-changing task" is fuzzy and forcing block-instead-of-complete on every code worker would break flows where no review is wanted). It's a convention layered on top:

- Block instead of complete, withreasonprefixedreview-required:so the dashboard /hermes kanban showsurfaces the row as awaiting review.
- Drop structured metadata into akanban_commentfirstsincekanban_blockonly carries the human-readablereason. Comments are the durable annotation channel — every audit-relevant field (changed_files, tests_run, diff_path or PR url, decisions) belongs there.
- Reviewer either approves and unblocks, which respawns the worker with the comment thread for follow-ups; or asks for changes via another comment, which the next worker run sees as part ofkanban_show's context.

`reason`
`review-required: `
`hermes kanban show`
`kanban_comment`
`kanban_block`
`reason`
`kanban_show`

The injectedKANBAN_GUIDANCEcovers bothkanban_complete(truly terminal tasks — typo fixes, docs changes, research writeups) and thereview-requiredblock pattern.

`KANBAN_GUIDANCE`
`kanban_complete`
`review-required`

## Logs and audit trail​

The dispatcher writes per-task worker stdout/stderr to<board-root>/logs/<task_id>.log. Logs are auditable from kanban metadata:

`<board-root>/logs/<task_id>.log`
- task_runsrows carry thelog_path, exit code (where available), summary, and metadata.
- task_eventsrows carry every state transition (promoted,claimed,heartbeat,completed,blocked,gave_up,crashed,timed_out,reclaimed,claim_extended).
- kanban_showreturns both, so a reviewer (or a follow-up worker) reading the task gets the full history without needing dashboard access.

`task_runs`
`log_path`
`task_events`
`promoted`
`claimed`
`heartbeat`
`completed`
`blocked`
`gave_up`
`crashed`
`timed_out`
`reclaimed`
`claim_extended`
`kanban_show`

The dashboard renders run history with summaries, metadata blocks, and exit-status badges. CLI users can runhermes kanban tail <task_id>to follow live, orhermes kanban runs <task_id>for the historical attempt list.

`hermes kanban tail <task_id>`
`hermes kanban runs <task_id>`

## Existing lane shapes​

### Hermes profile lane (default)​

The shape every kanban worker takes today: the assignee is a profile name, the dispatcher spawnshermes -p <profile>, the worker gets theKANBAN_GUIDANCEsystem-prompt block injected automatically, and uses thekanban_*tools to terminate the run. No setup beyond defining the profile.

`hermes -p <profile>`
`KANBAN_GUIDANCE`
`kanban_*`

When you create profiles for your fleet, choose names that match theroleyou want the orchestrator to route to. The orchestrator (when there is one) discovers your profile names viahermes profile list— there's no fixed roster the system assumes (the orchestrator side of the contract is part of the injectedKANBAN_GUIDANCE).

`hermes profile list`
`KANBAN_GUIDANCE`

### Orchestrator profile lane​

A specialisation of the profile lane: an orchestrator is a Hermes profile whose toolset includeskanbanbut excludesterminal/file/code/webfor implementation. Its job is decomposing a high-level goal into child tasks viakanban_create+kanban_linkand stepping back. The orchestrator skill encodes the anti-temptation rules.

`kanban`
`terminal`
`file`
`code`
`web`
`kanban_create`
`kanban_link`

## Adding an external CLI worker lane​

Wiring a non-Hermes CLI tool (Codex CLI, Claude Code CLI, OpenCode CLI, a local coding-model runner, etc.) as a kanban worker lane isnot yet a paved path. The dispatcher's spawn function is pluggable (spawn_fnis a parameter ondispatch_once), and a plugin could register its ownspawn_fnfor a non-Hermes assignee, but the surrounding integration work — wrapping the CLI's exit code intokanban_complete/kanban_blockcalls, mapping the CLI's workspace/sandbox conventions onto the dispatcher'sHERMES_KANBAN_WORKSPACEenv, handling auth and per-CLI policy — is still per-integration design work.

`spawn_fn`
`dispatch_once`
`spawn_fn`
`kanban_complete`
`kanban_block`
`HERMES_KANBAN_WORKSPACE`

If you're considering adding a CLI lane, open an issue describing the specific CLI and the workflow you're trying to enable. The contract above is the constraints any such lane must satisfy; the implementation shape (one plugin per CLI vs a generic CLI-runner plugin parameterised by config) is open.

The historical issue for this is#19931and the closed-not-merged Codex-specific PR#19924— those describe the original architecture proposal but didn't land a runner.

## Failure modes the dispatcher handles​

So lane authors don't have to reimplement these:

- Stale claim TTL— a worker that claims and then never heartbeats / completes / blocks gets reclaimed afterDEFAULT_CLAIM_TTL_SECONDS(15 min default) — but only if the worker process has actually died. A live worker (slow model spending 20+ min in one tool-free LLM call) gets the claimextendedinstead of killed; only a dead PID is reclaimed.
- Crashed worker— a worker whose host-local PID has vanished is detected bydetect_crashed_workersand reaped; the task incrementsconsecutive_failuresand may auto-block when the breaker trips.
- Run-level retry— when a task is retried (post-block, post-crash, post-reclaim), the worker can use theexpected_run_idparameter on terminating tools to fail fast if its own run was already superseded.
- Per-task max runtime—task.max_runtime_secondshard-caps wall-clock time per run, regardless of PID liveness. Catches genuinely-deadlocked workers that the live-PID extension would otherwise keep running.
- Stranded-task detection— a ready task whose assignee never produces a claim withinkanban.stranded_threshold_seconds(default 30 min) shows up inhermes kanban diagnosticsas astranded_in_readywarning. Severity escalates to error at 2x the threshold and critical at 6x. Catches typo'd assignees, deleted profiles, and down external worker pools in one signal — identity-agnostic, no per-board allowlist to curate.

`DEFAULT_CLAIM_TTL_SECONDS`
`detect_crashed_workers`
`consecutive_failures`
`expected_run_id`
`task.max_runtime_seconds`
`kanban.stranded_threshold_seconds`
`hermes kanban diagnostics`
`stranded_in_ready`

## Related​

- Kanban overview— the user-facing intro.
- Kanban tutorial— walkthrough with the dashboard open.
- KANBAN_GUIDANCE— the worker + orchestrator lifecycle injected into every kanban worker's system prompt.

`KANBAN_GUIDANCE`