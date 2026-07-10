---
layout: docs
title: "Features_Kanban"
permalink: /docs/user-guide/features/kanban/
---

- 
- Features
- Automation
- Kanban (Multi-Agent Board)

# Kanban — Multi-Agent Profile Collaboration

> Want a walkthrough?Read theKanban tutorial— four user stories (solo dev, fleet farming, role pipeline with retry, circuit breaker) with dashboard screenshots of each. This page is the reference; the tutorial is the narrative.

Want a walkthrough?Read theKanban tutorial— four user stories (solo dev, fleet farming, role pipeline with retry, circuit breaker) with dashboard screenshots of each. This page is the reference; the tutorial is the narrative.

Hermes Kanban is a durable task board, shared across all your Hermes profiles, that lets multiple named agents collaborate on work without fragile in-process subagent swarms. Every task is a row in~/.hermes/kanban.db; every handoff is a row anyone can read and write; every worker is a full OS process with its own identity.

`~/.hermes/kanban.db`

### Two surfaces: the model talks through tools, you talk through the CLI​

The board has two front doors, both backed by the same~/.hermes/kanban.db:

`~/.hermes/kanban.db`
- Agents drive the board through a dedicatedkanban_*toolset—kanban_show,kanban_list,kanban_complete,kanban_block,kanban_heartbeat,kanban_comment,kanban_create,kanban_link,kanban_unblock. The dispatcher spawns each worker with these tools already in its schema; orchestrator profiles can also enable thekanbantoolset explicitly. The model reads and routes tasks by calling tools directly,notby shelling out tohermes kanban. SeeHow workers interact with the boardbelow.
- You (and scripts, and cron) drive the board throughhermes kanban …on the CLI,/kanban …as a slash command, or the dashboard. These are for humans and automation — the places without a tool-calling model behind them.

`kanban_*`
`kanban_show`
`kanban_list`
`kanban_complete`
`kanban_block`
`kanban_heartbeat`
`kanban_comment`
`kanban_create`
`kanban_link`
`kanban_unblock`
`kanban`
`hermes kanban`
`hermes kanban …`
`/kanban …`

Both surfaces route through the samekanban_dblayer, so reads see a consistent view and writes can't drift. The rest of this page shows CLI examples because they're easy to copy-paste, but every CLI verb has a tool-call equivalent the model uses.

`kanban_db`

This is the shape that covers the workloadsdelegate_taskcan't:

`delegate_task`
- Research triage— parallel researchers + analyst + writer, human-in-the-loop.
- Scheduled ops— recurring daily briefs that build a journal over weeks.
- Digital twins— persistent named assistants (inbox-triage,ops-review) that accumulate memory over time.
- Engineering pipelines— decompose → implement in parallel worktrees → review → iterate → PR.
- Fleet work— one specialist managing N subjects (50 social accounts, 12 monitored services).

`inbox-triage`
`ops-review`

For the full design rationale, comparative analysis against Cline Kanban / Paperclip / NanoClaw / Google Gemini Enterprise, and the eight canonical collaboration patterns, seedocs/hermes-kanban-v1-spec.pdfin the repository.

`docs/hermes-kanban-v1-spec.pdf`

## Kanban vs.delegate_task​

`delegate_task`

They look similar; they are not the same primitive.

|  | delegate_task | Kanban |
| --- | --- | --- |
| Shape | RPC call (fork → join) | Durable message queue + state machine |
| Parent | Blocks until child returns | Fire-and-forget aftercreate |
| Child identity | Anonymous subagent | Named profile with persistent memory |
| Resumability | None — failed = failed | Block → unblock → re-run; crash → reclaim |
| Human in the loop | Not supported | Comment / unblock at any point |
| Agents per task | One call = one subagent | N agents over task's life (retry, review, follow-up) |
| Audit trail | Lost on context compression | Durable rows in SQLite forever |
| Coordination | Hierarchical (caller → callee) | Peer — any profile reads/writes any task |

`delegate_task`
`create`

One-sentence distinction:delegate_taskis a function call; Kanban is a work queue where every handoff is a row any profile (or human) can see and edit.

`delegate_task`

Usedelegate_taskwhenthe parent agent needs a short reasoning answer before continuing, no humans involved, result goes back into the parent's context.

`delegate_task`

Use Kanban whenwork crosses agent boundaries, needs to survive restarts, might need human input, might be picked up by a different role, or needs to be discoverable after the fact.

They coexist: a kanban worker may calldelegate_taskinternally during its run.

`delegate_task`

## Core concepts​

- Board— a standalone queue of tasks with its own SQLite DB, workspaces
directory, and dispatcher loop. A single install can have many boards
(e.g. one per project, repo, or domain); seeBoards (multi-project)below. Single-project users stay on thedefaultboard and never see the
word "board" outside this docs section.
- Task— a row with title, optional body, one assignee (a profile name), status (triage | todo | ready | running | blocked | done | archived), optional tenant namespace, optional idempotency key (dedup for retried automation).
- Link—task_linksrow recording a parent → child dependency. The dispatcher promotestodo → readywhen all parents aredone.
- Comment— the inter-agent protocol. Agents and humans append comments; when a worker is (re-)spawned it reads the full comment thread as part of its context.
- Workspace— the directory a worker operates in. Three kinds:scratch(default) — fresh tmp dir under~/.hermes/kanban/workspaces/<id>/(or~/.hermes/kanban/boards/<slug>/workspaces/<id>/on non-default boards).Deleted when the task completes— scratch is ephemeral by design, so the dir is wiped the moment the worker (orhermes kanban complete <id>) marks the task done. If you want to keep the worker's output, useworktree:ordir:<path>instead. The first time a scratch workspace is created on an install, the dispatcher logs a warning and emits atip_scratch_workspaceevent on the task (visible viahermes kanban show <id>).dir:<path>— an existing shared directory (Obsidian vault, mail ops dir, per-account folder).Must be an absolute path.Relative paths likedir:../tenants/foo/are rejected at dispatch because they'd resolve against whatever CWD the dispatcher happens to be in, which is ambiguous and a confused-deputy escape vector. The path is otherwise trusted — it's your box, your filesystem, the worker runs with your uid. This is the trusted-local-user threat model; kanban is single-host by design.Preserved on completion.worktree— a git worktree under.worktrees/<id>/for coding tasks. Useworktree:<path>to pin the exact target path. Worker-sidegit worktree addcreates it, using--branchwhen provided.Preserved on completion.
- Dispatcher— a long-lived loop that, every N seconds (default 60): reclaims stale claims, reclaims crashed workers (PID gone but TTL not yet expired), promotes ready tasks, atomically claims, spawns assigned profiles. Runsinside the gatewayby default (kanban.dispatch_in_gateway: true). One dispatcher sweeps all boards per tick; workers are spawned withHERMES_KANBAN_BOARDpinned so they can't see other boards. Afterkanban.failure_limitconsecutive spawn failures on the same task (default: 2) the dispatcher auto-blocks it with the last error as the reason — prevents thrashing on tasks whose profile doesn't exist, workspace can't mount, etc.
- Tenant— optional string namespacewithina board. One specialist fleet can serve multiple businesses (--tenant business-a) with data isolation by workspace path and memory key prefix. Tenants are a soft filter; boards are the hard isolation boundary.

`default`
`triage | todo | ready | running | blocked | done | archived`
`task_links`
`todo → ready`
`done`
- scratch(default) — fresh tmp dir under~/.hermes/kanban/workspaces/<id>/(or~/.hermes/kanban/boards/<slug>/workspaces/<id>/on non-default boards).Deleted when the task completes— scratch is ephemeral by design, so the dir is wiped the moment the worker (orhermes kanban complete <id>) marks the task done. If you want to keep the worker's output, useworktree:ordir:<path>instead. The first time a scratch workspace is created on an install, the dispatcher logs a warning and emits atip_scratch_workspaceevent on the task (visible viahermes kanban show <id>).
- dir:<path>— an existing shared directory (Obsidian vault, mail ops dir, per-account folder).Must be an absolute path.Relative paths likedir:../tenants/foo/are rejected at dispatch because they'd resolve against whatever CWD the dispatcher happens to be in, which is ambiguous and a confused-deputy escape vector. The path is otherwise trusted — it's your box, your filesystem, the worker runs with your uid. This is the trusted-local-user threat model; kanban is single-host by design.Preserved on completion.
- worktree— a git worktree under.worktrees/<id>/for coding tasks. Useworktree:<path>to pin the exact target path. Worker-sidegit worktree addcreates it, using--branchwhen provided.Preserved on completion.

`scratch`
`~/.hermes/kanban/workspaces/<id>/`
`~/.hermes/kanban/boards/<slug>/workspaces/<id>/`
`hermes kanban complete <id>`
`worktree:`
`dir:<path>`
`tip_scratch_workspace`
`hermes kanban show <id>`
`dir:<path>`
`dir:../tenants/foo/`
`worktree`
`.worktrees/<id>/`
`worktree:<path>`
`git worktree add`
`--branch`
`kanban.dispatch_in_gateway: true`
`HERMES_KANBAN_BOARD`
`kanban.failure_limit`
`--tenant business-a`

## Boards (multi-project)​

Boards let you separate unrelated streams of work — one per project, repo,
or domain — into isolated queues. A new install has exactly one board
calleddefault(DB at~/.hermes/kanban.dbfor back-compat). Users who
only want one stream of work never need to know about boards; the feature
is opt-in.

`default`
`~/.hermes/kanban.db`

Per-board isolation is absolute:

- Separate SQLite DB per board (~/.hermes/kanban/boards/<slug>/kanban.db).
- Separateworkspaces/andlogs/directories.
- Workers spawned for a task seeonlytheir board's tasks — the
dispatcher setsHERMES_KANBAN_BOARDin the child env and everykanban_*tool the worker has access to reads it.
- Linking tasks across boards is not allowed (keeps the schema simple; if
you really need cross-project refs, use free-text mentions and look
them up by id manually).

`~/.hermes/kanban/boards/<slug>/kanban.db`
`workspaces/`
`logs/`
`HERMES_KANBAN_BOARD`
`kanban_*`

### Managing boards from the CLI​

```
# See what's on disk. Fresh installs show only "default".hermes kanban boards list# Create a new board.hermes kanban boards create atm10-server \    --name "ATM10 Server" \    --description "Minecraft modded server ops" \    --icon 🎮 \    --switch                   # optional: make it the active board# Operate on a specific board without switching.hermes kanban --board atm10-server listhermes kanban --board atm10-server create "Restart ATM server" --assignee ops# Change which board is "current" for subsequent calls.hermes kanban boards switch atm10-serverhermes kanban boards show             # who's active right now?# Rename the display name (the slug is immutable — it's the directory name).hermes kanban boards rename atm10-server "ATM10 (Prod)"# Archive (default) — moves the board's dir to boards/_archived/<slug>-<ts>/.# Recoverable by moving the dir back.hermes kanban boards rm atm10-server# Hard delete — `rm -rf` the board dir. No recovery.hermes kanban boards rm atm10-server --delete
```

Board resolution order (highest precedence first):

1. Explicit--board <slug>on the CLI call.
2. HERMES_KANBAN_BOARDenv var (set by the dispatcher when spawning a
worker, so workers can't see other boards).
3. ~/.hermes/kanban/current— the slug persisted byhermes kanban boards switch.
4. default.

`--board <slug>`
`HERMES_KANBAN_BOARD`
`~/.hermes/kanban/current`
`hermes kanban boards switch`
`default`

Slugs are validated: lowercase alphanumerics + hyphens + underscores, 1-64
chars, must start with alphanumeric. Uppercase input is auto-downcased.
Anything else (slashes, spaces, dots,..) is rejected at the CLI layer
so path-traversal tricks can't name a board.

`..`

### Managing boards from the dashboard​

hermes dashboard→ Kanban tab shows a board switcher at the top as soon
as more than one board exists (or any board has tasks). Single-board users
see only a small+ New boardbutton; the switcher is hidden until it
matters.

`hermes dashboard`
`+ New board`
- Board dropdown— pick the active board. Your selection is saved to
the browser'slocalStorageso it persists across reloads without
shifting the CLI'scurrentpointer out from under a terminal you left
open.
- + New board— opens a modal asking for slug, display name,
description, and icon. Option to auto-switch to the new board.
- Archive— only shown on non-defaultboards. Confirms, then moves
the board dir toboards/_archived/.

`localStorage`
`current`
`default`
`boards/_archived/`

All dashboard API endpoints accept?board=<slug>for board scoping. The
events WebSocket is pinned to a board at connection time; switching in
the UI opens a fresh WS against the new board.

`?board=<slug>`

## File attachments​

Tasks can carry file attachments — PDFs, images, source documents — so a
worker has the source material it needs without you pasting paths into the
body and hoping it finds them.

- Upload— open a task in the dashboard drawer and use theAttachmentssection'sUpload filebutton (multiple files at once
are fine). Each upload is capped at 25 MB.
- Storage— files land under<hermes-home>/kanban/attachments/<task_id>/for the default board, or<hermes-home>/kanban/boards/<slug>/attachments/<task_id>/for a named
board. SetHERMES_KANBAN_ATTACHMENTS_ROOTto pin a custom location.
- What the worker sees— when the dispatcher hands a task to a worker,
the worker's context includes anAttachmentssection listing each
file's name and itsabsolute path. The worker has full file/terminal
tool access, so it reads attachments directly (read_file, or shell
tools likepdftotext).
- Download / remove— the drawer lists each attachment with a download
link and a remove (×) control. Removing an attachment deletes both the
metadata row and the on-disk file.

`<hermes-home>/kanban/attachments/<task_id>/`
`<hermes-home>/kanban/boards/<slug>/attachments/<task_id>/`
`HERMES_KANBAN_ATTACHMENTS_ROOT`
`read_file`
`pdftotext`

Attachment paths resolve directly on thelocalterminal backend, which
is the default for Kanban workers. If you run workers on a remote backend
(Docker, Modal), mount the board'sattachments/directory into the
sandbox so the absolute paths in the worker context are reachable.

`attachments/`

## Quick start​

The commands below areyou(the human) setting up the board and creating tasks. Once a task is assigned, the dispatcher spawns the assigned profile as a worker, and from therethe model drives the task throughkanban_*tool calls, not CLI commands— seeHow workers interact with the board.

`kanban_*`

```
# 1. Create the board (you)hermes kanban init# 2. Start the gateway (hosts the embedded dispatcher)hermes gateway start# 3. Create a task (you — or an orchestrator agent via kanban_create)hermes kanban create "research AI funding landscape" --assignee researcher# 4. Watch activity live (you)hermes kanban watch# 5. See the board (you)hermes kanban listhermes kanban stats
```

When the dispatcher picks upt_abcdand spawns theresearcherprofile, the very first thing that worker's model does is callkanban_show()to read its task. It doesn't runhermes kanban show t_abcd.

`t_abcd`
`researcher`
`kanban_show()`
`hermes kanban show t_abcd`

### Gateway-embedded dispatcher (default)​

The dispatcher runs inside the gateway process. Nothing to install, no
separate service to manage — if the gateway is up, ready tasks get picked
up on the next tick (60s by default).

```
# config.yamlkanban:  dispatch_in_gateway: true        # default  dispatch_interval_seconds: 60    # default
```

Override the config flag at runtime viaHERMES_KANBAN_DISPATCH_IN_GATEWAY=0for debugging. Standard gateway supervision applies: runhermes gateway startdirectly, or wire the gateway up as a systemd user unit (see the
gateway docs). Without a running gateway,readytasks stay where they are
until one comes up —hermes kanban createwarns about this at creation
time.

`HERMES_KANBAN_DISPATCH_IN_GATEWAY=0`
`hermes gateway start`
`ready`
`hermes kanban create`

Runninghermes kanban daemonas a separate process isdeprecated;
use the gateway. If you truly cannot run the gateway (headless host
policy forbids long-lived services, etc.) a--forceescape hatch keeps
the old standalone daemon alive for one release cycle, but running both
a gateway-embedded dispatcher AND a standalone daemon against the samekanban.dbcauses claim races and is not supported.

`hermes kanban daemon`
`--force`
`kanban.db`

### Idempotent create (for automation / webhooks)​

```
# First call creates the task. Any subsequent call with the same key# returns the existing task id instead of duplicating.hermes kanban create "nightly ops review" \    --assignee ops \    --idempotency-key "nightly-ops-$(date -u +%Y-%m-%d)" \    --json
```

### Bulk CLI verbs​

All the lifecycle verbs accept multiple ids so you can clean up a batch
in one command:

```
hermes kanban complete t_abc t_def t_hij --result "batch wrap"hermes kanban archive  t_abc t_def t_hijhermes kanban unblock  t_abc t_defhermes kanban block    t_abc "need input" --ids t_def t_hij
```

## How workers interact with the board​

Workers do not shell out tohermes kanban.When the dispatcher spawns a worker it setsHERMES_KANBAN_TASK=t_abcdin the child's env, and that env var flips on a dedicatedkanban toolsetin the model's schema. The same toolset is also available to orchestrator profiles that enablekanbanin their toolsets config. These tools read and mutate the board directly via the Pythonkanban_dblayer, same as the CLI does. A running worker calls these like any other tool; it never sees or needs thehermes kanbanCLI.

`hermes kanban`
`HERMES_KANBAN_TASK=t_abcd`
`kanban`
`kanban_db`
`hermes kanban`
| Tool | Purpose | Required params |
| --- | --- | --- |
| kanban_show | Read the current task (title, body, prior attempts, parent handoffs, comments, full pre-formattedworker_context). Defaults to the env's task id. | — |
| kanban_list | List task summaries with filters forassignee,status,tenant, archived visibility, and limit. Intended for orchestrators discovering board work. | — |
| kanban_complete | Finish withsummary+metadatastructured handoff. | at least one ofsummary/result |
| kanban_block | Stop work and route by why:kind=dependency(waits intodo, auto-resumes),needs_input/capability/transient(surface to a human). Repeated same-kind re-blocks auto-escalate totriage. | reason |
| kanban_heartbeat | Signal liveness during long operations. Pure side-effect. | — |
| kanban_comment | Append a durable note to the task thread. | task_id,body |
| kanban_create | (Orchestrators) fan out into child tasks with anassignee, optionalparents,skills, etc. | title,assignee |
| kanban_link | (Orchestrators) add aparent_id → child_iddependency edge after the fact. | parent_id,child_id |
| kanban_unblock | (Orchestrators) move a blocked task back toready. | task_id |

`kanban_show`
`worker_context`
`kanban_list`
`assignee`
`status`
`tenant`
`kanban_complete`
`summary`
`metadata`
`summary`
`result`
`kanban_block`
`kind=dependency`
`todo`
`needs_input`
`capability`
`transient`
`triage`
`reason`
`kanban_heartbeat`
`kanban_comment`
`task_id`
`body`
`kanban_create`
`assignee`
`parents`
`skills`
`title`
`assignee`
`kanban_link`
`parent_id → child_id`
`parent_id`
`child_id`
`kanban_unblock`
`ready`
`task_id`

A typical worker turn looks like:

```
# Model's tool calls, in order:kanban_show()                                     # no args — uses HERMES_KANBAN_TASK# (model reads the returned worker_context, does the work via terminal/file tools)kanban_heartbeat(note="halfway through — 4 of 8 files transformed")# (more work)kanban_complete(    summary="migrated limiter.py to token-bucket; added 14 tests, all pass",    metadata={"changed_files": ["limiter.py", "tests/test_limiter.py"], "tests_run": 14},)
```

Anorchestratorworker fans out instead:

```
kanban_show()kanban_create(    title="research ICP funding 2024-2026",    assignee="researcher-a",    body="focus on seed + series A, North America, AI-adjacent",)# → returns {"task_id": "t_r1", ...}kanban_create(title="research ICP funding — EU angle", assignee="researcher-b", body="…")# → returns {"task_id": "t_r2", ...}kanban_create(    title="synthesize findings into launch brief",    assignee="writer",    parents=["t_r1", "t_r2"],                     # promotes to ready when both complete    body="one-pager, 300 words, neutral tone",)kanban_complete(summary="decomposed into 2 research tasks + 1 writer; linked dependencies")
```

The "(Orchestrators)" tools —kanban_list,kanban_create,kanban_link,kanban_unblock, andkanban_commenton foreign tasks — are available through the same toolset; the convention (encoded in the auto-injected kanban guidance) is that worker profiles don't fan out or route unrelated work, and orchestrator profiles don't execute implementation work. Dispatcher-spawned workers are still task-scoped for destructive lifecycle operations and cannot mutate unrelated tasks.

`kanban_list`
`kanban_create`
`kanban_link`
`kanban_unblock`
`kanban_comment`

### Why tools instead of shelling tohermes kanban​

`hermes kanban`

Three reasons:

1. Backend portability.Workers whose terminal tool points at a remote backend (Docker / Modal / Singularity / SSH) would runhermes kanban completeinsidethe container, wherehermesisn't installed and~/.hermes/kanban.dbisn't mounted. The kanban tools run in the agent's own Python process and always reach~/.hermes/kanban.dbregardless of terminal backend.
2. No shell-quoting fragility.Passing--metadata '{"files": [...]}'through shlex + argparse is a latent footgun. Structured tool args skip it entirely.
3. Better errors.Tool results are structured JSON the model can reason about, not stderr strings it has to parse.

`hermes kanban complete`
`hermes`
`~/.hermes/kanban.db`
`~/.hermes/kanban.db`
`--metadata '{"files": [...]}'`

Zero schema footprint on normal sessions.A regularhermes chatsession has zerokanban_*tools in its schema unless the active profile explicitly enables thekanbantoolset for orchestrator work. Dispatcher-spawned task workers get task-scoped tools becauseHERMES_KANBAN_TASKis set; orchestrator profiles get the broader routing surface through config. No tool bloat for users who never touch kanban.

`hermes chat`
`kanban_*`
`kanban`
`HERMES_KANBAN_TASK`

The auto-injected kanban guidance teaches the model which tool to call when and in what order.

### Recommended handoff evidence​

kanban_complete(summary=..., metadata={...})is intentionally flexible:
the summary is the human-readable closeout, andmetadatais the
machine-readable handoff that downstream agents, reviewers, or dashboards can
reuse without scraping prose.

`kanban_complete(summary=..., metadata={...})`
`metadata`

For engineering and review tasks, prefer this optional metadata shape:

```
{  "changed_files": ["path/to/file.py"],  "verification": ["pytest tests/hermes_cli/test_kanban_db.py -q"],  "dependencies": ["parent task id or external issue, if any"],  "blocked_reason": null,  "retry_notes": "what failed before, if this was a retry",  "residual_risk": ["what was not tested or still needs human review"]}
```

These keys are a convention, not a schema requirement. The useful property is
that every worker leaves enough evidence for the next reader to answer four
questions quickly:

1. What changed?
2. How was it verified?
3. What can unblock or retry this if it fails?
4. What risk is still deliberately left open?

Keep secrets, raw logs, tokens, OAuth material, and unrelated transcripts out ofmetadata. Store pointers and summaries instead. If a task has no files or
tests, say so explicitly insummaryand usemetadatafor the evidence that
does exist, such as source URLs, issue ids, or manual review steps.

`metadata`
`summary`
`metadata`

### The worker lifecycle​

Every profile that works kanban tasks automatically gets the worker lifecycle — it's injected into the worker's system prompt at spawn (theKANBAN_GUIDANCEblock), so there isnothing to install or configure. It teaches the worker the full lifecycle intool calls, not CLI commands:

`KANBAN_GUIDANCE`
1. On spawn, callkanban_show()to read title + body + parent handoffs + prior attempts + full comment thread.
2. cd $HERMES_KANBAN_WORKSPACE(via the terminal tool) and do the work there.
3. Callkanban_heartbeat(note="...")every few minutes during long operations.If your work may run longer than 1 hour, callkanban_heartbeatat least once an hour— the dispatcher reclaims tasks that have been running pastkanban.dispatch_stale_timeout_seconds(default 4 h) with no heartbeat in the last hour, on the assumption the worker crashed without cleanup. A reclaim is benign (the task goes back toreadyfor re-dispatch without a failure-counter tick) but you lose your current run's progress.
4. Complete withkanban_complete(summary="...", metadata={...}), orkanban_block(reason="...")if stuck.

`kanban_show()`
`cd $HERMES_KANBAN_WORKSPACE`
`kanban_heartbeat(note="...")`
`kanban_heartbeat`
`kanban.dispatch_stale_timeout_seconds`
`ready`
`kanban_complete(summary="...", metadata={...})`
`kanban_block(reason="...")`

That finalkanban_complete/kanban_blockcall is part of the worker
protocol. If the worker process exits with status 0 while the task is stillrunning, the dispatcher treats that as a protocol violation, emits aprotocol_violationevent, and auto-blocks the task on the next tick instead
of respawning it into the same loop. This usually means the model wrote a
plain-text answer and exited without using the Kanban tool surface.

`kanban_complete`
`kanban_block`
`running`
`protocol_violation`

The lifecycle plus the load-bearing reference details (workspace kinds, deliverableartifacts, claiming created cards) ship in that system-prompt block, so every worker has them regardless of which profile it runs under — no per-profile skill setup required.

`artifacts`

### Pinning extra skills to a specific task​

Sometimes a single task needs specialist context the assignee profile doesn't carry by default — a translation job that needs thetranslationskill, a review task that needsgithub-code-review, a security audit that needssecurity-pr-audit. Rather than editing the assignee's profile every time, attach the skills directly to the task.

`translation`
`github-code-review`
`security-pr-audit`

From an orchestrator agent(the usual case — one agent routing work to another), use thekanban_createtool'sskillsarray:

`kanban_create`
`skills`

```
kanban_create(    title="translate README to Japanese",    assignee="linguist",    skills=["translation"],)kanban_create(    title="audit auth flow",    assignee="reviewer",    skills=["security-pr-audit", "github-code-review"],)
```

From a human (CLI / slash command), repeat--skillfor each one:

`--skill`

```
hermes kanban create "translate README to Japanese" \    --assignee linguist \    --skill translationhermes kanban create "audit auth flow" \    --assignee reviewer \    --skill security-pr-audit \    --skill github-code-review
```

From the dashboard, type the skills comma-separated into theskillsfield of the inline create form.

The dispatcher emits one--skills <name>flag per skill listed, so the worker spawns with all of them loaded on top of the auto-injected kanban guidance. The skill names must match skills that are actually installed on the assignee's profile (runhermes skills listto see what's available); there's no runtime install.

`--skills <name>`
`hermes skills list`

### Goal-mode cards (--goal)​

`--goal`

By default each worker getsone shotat its card — do the work, callkanban_complete/kanban_block, exit. Pass--goal(CLI) orgoal_mode=True(thekanban_createtool / dashboard) to instead run that worker in agoal loop, the same Ralph-style engine behind the/goalslash command: after every turn an auxiliary judge checks the worker's output against the card's title + body (treated as the acceptance criteria), and if the work isn't done — and the turn budget remains — the worker keeps goingin the same sessionuntil the judge agrees, the worker terminates the task itself, or the budget runs out (whichblocksthe card for human review rather than exiting silently).

`kanban_complete`
`kanban_block`
`--goal`
`goal_mode=True`
`kanban_create`
`/goal`

```
hermes kanban create "Translate the docs site to French" \    --body "Acceptance: every page translated, no English left, links intact." \    --assignee linguist \    --goal \    --goal-max-turns 15      # optional; default 20
```

Use it for open-ended, multi-step, or "keep going until X is true" cards. Skip it for cheap one-shot work — the per-turn judge overhead isn't worth it, and the dispatcher's existing retry/circuit-breaker already handles transient worker failures. The judge is only as good as your goal text, so write the body asexplicit acceptance criteria.

### How the orchestrator behaves​

Awell-behaved orchestrator does not do the work itself.It decomposes the user's goal into tasks, links them, assigns each to one of the profiles you've set up, and steps back. The orchestrator guidance — anti-temptation rules, a Step-0 profile-discovery prompt (the dispatcher silently fails on unknown assignee names, so the orchestrator must ground every card in profiles that actually exist on your machine), and a decomposition playbook keyed onkanban_create/kanban_link/kanban_comment— is injected into the worker's system prompt automatically; there is nothing to install.

`kanban_create`
`kanban_link`
`kanban_comment`

A canonical orchestrator turn (two parallel researchers handing off to a writer):

```
# Goal from user: "draft a launch post on the ICP funding landscape"kanban_create(title="research ICP funding, NA angle",  assignee="researcher-a", body="…")  # → t_r1kanban_create(title="research ICP funding, EU angle",  assignee="researcher-b", body="…")  # → t_r2kanban_create(    title="synthesize ICP funding research into launch post draft",    assignee="writer",    parents=["t_r1", "t_r2"],        # promoted to 'ready' when both researchers complete    body="one-pager, neutral tone, cite sources inline",)                                     # → t_w1# Optional: add cross-cutting deps discovered later without re-creating taskskanban_link(parent_id="t_r1", child_id="t_followup")kanban_complete(    summary="decomposed into 2 parallel research tasks → 1 synthesis task; writer starts when both researchers finish",)
```

The orchestrator guidance ships in the worker's system prompt automatically — there is nothing to install or sync per profile.

For best results, pair it with a profile whose toolsets are restricted to board operations (kanban,gateway,memory) so the orchestrator literally cannot execute implementation tasks even if it tries.

`kanban`
`gateway`
`memory`

## Dashboard (GUI)​

The/kanbanCLI and slash command are enough to run the board headlessly, but a visual board is often the right interface for humans-in-the-loop: triage, cross-profile supervision, reading comment threads, and dragging cards between columns. Hermes ships this as abundled dashboard pluginatplugins/kanban/— not a core feature, not a separate service — following the model laid out inExtending the Dashboard.

`/kanban`
`plugins/kanban/`

Open it with:

```
hermes kanban init      # one-time: create kanban.db if not already presenthermes dashboard        # "Kanban" tab appears in the nav, after "Skills"
```

### What the plugin gives you​

- AKanbantab showing one column per status:triage,todo,ready,running,blocked,done(plusarchivedwhen the toggle is on).triageis the parking column for rough ideas. By default (kanban.auto_decompose: true), the dispatcher auto-runs thedecomposeron tasks that land here. The built-in decomposer uses theauxiliary.kanban_decomposermodel path, reads your profile roster (with descriptions), and fans the task out into a small graph of child tasks routed to the best-fit specialists. The original task stays alive as the parent of every child so its assignee (kanban.orchestrator_profile, or the active default profile when unset) wakes back up to judge completion when everything finishes. Flip theOrchestration: Auto/Manualpill at the top of the page (emerald = Auto, muted gray = Manual), or by editingconfig.yamldirectly. Both modes coexist withhermes kanban specify- that's still available as a single-task spec rewrite when you don't want fan-out.
- Cards show the task id, title, priority badge, tenant tag, assigned profile, comment/link counts, aprogress pill(N/Mchildren done when the task has dependents), and "created N ago". A per-card checkbox enables multi-select.
- Per-profile lanes inside Running— toolbar checkbox toggles sub-grouping of the Running column by assignee.
- Live updates via WebSocket— the plugin tails the append-onlytask_eventstable on a short poll interval; the board reflects changes the instant any profile (CLI, gateway, or another dashboard tab) acts. Reloads are debounced so a burst of events triggers a single refetch.
- Drag-dropcards between columns to change status. The drop sendsPATCH /api/plugins/kanban/tasks/:idwhich routes through the samekanban_dbcode the CLI uses — the three surfaces can never drift. Moves into destructive statuses (done,archived,blocked) prompt for confirmation. Touch devices use a pointer-based fallback so the board is usable from a tablet.
- Inline create— click+on any column header to type a title, assignee, priority, and (optionally) a parent task from a dropdown over every existing task. Press Enter to create the task, Shift+Enter to insert a newline in the title field, or Escape to cancel. Creating from the Triage column automatically parks the new task in triage.
- Multi-select with bulk actions— shift/ctrl-click a card or tick its checkbox to add it to the selection. A bulk action bar appears at the top with batch status transitions, archive, and reassign (by profile dropdown, or "(unassign)"). Destructive batches confirm first. Per-id partial failures are reported without aborting the rest.
- Click a card(without shift/ctrl) to open a side drawer (Escape or click-outside closes) with:Editable title— click the heading to rename.Editable assignee / priority— click the meta row to rewrite.Editable description— markdown-rendered by default (headings, bold, italic, inline code, fenced code,http(s)/mailto:links, bullet lists), with an "edit" button that swaps in a textarea. Markdown rendering is a tiny, XSS-safe renderer — every substitution runs on HTML-escaped input, onlyhttp(s)/mailto:links pass through, andtarget="_blank"+rel="noopener noreferrer"are always set.Dependency editor— chip list of parents and children, each with an×to unlink, plus dropdowns over every other task to add a new parent or child. Cycle attempts are rejected server-side with a clear message.Status action row(→ triage / → ready / → running / block / unblock / complete / archive) with confirm prompts for destructive transitions. For cards in theTriagecolumn the row also exposes two LLM-driven actions:⚗ Decomposefans the task out into a graph of child tasks routed to specialist profiles by description, and✨ Specifydoes a single-task spec rewrite. Decompose falls back to specify-style promotion when the LLM decides the task doesn't benefit from fan-out, so it's a strict superset. Both are reachable from the CLI (hermes kanban decompose <id>/specify <id>/--all), from any gateway platform (/kanban decompose <id>), and programmatically viaPOST /api/plugins/kanban/tasks/:id/decomposeand…/specify. Configure the models underauxiliary.kanban_decomposerandauxiliary.triage_specifierinconfig.yaml.Result section (also markdown-rendered), comment thread with Enter-to-submit, the last 20 events.
- Toolbar filters— free-text search, tenant dropdown (defaults todashboard.kanban.default_tenantfromconfig.yaml), assignee dropdown, "show archived" toggle, "lanes by profile" toggle, and aNudge dispatcherbutton so you don't have to wait for the next 60 s tick.

`triage`
`todo`
`ready`
`running`
`blocked`
`done`
`archived`
- triageis the parking column for rough ideas. By default (kanban.auto_decompose: true), the dispatcher auto-runs thedecomposeron tasks that land here. The built-in decomposer uses theauxiliary.kanban_decomposermodel path, reads your profile roster (with descriptions), and fans the task out into a small graph of child tasks routed to the best-fit specialists. The original task stays alive as the parent of every child so its assignee (kanban.orchestrator_profile, or the active default profile when unset) wakes back up to judge completion when everything finishes. Flip theOrchestration: Auto/Manualpill at the top of the page (emerald = Auto, muted gray = Manual), or by editingconfig.yamldirectly. Both modes coexist withhermes kanban specify- that's still available as a single-task spec rewrite when you don't want fan-out.

`triage`
`kanban.auto_decompose: true`
`auxiliary.kanban_decomposer`
`kanban.orchestrator_profile`
`config.yaml`
`hermes kanban specify`
`N/M`
`task_events`
`PATCH /api/plugins/kanban/tasks/:id`
`kanban_db`
`done`
`archived`
`blocked`
`+`
- Editable title— click the heading to rename.
- Editable assignee / priority— click the meta row to rewrite.
- Editable description— markdown-rendered by default (headings, bold, italic, inline code, fenced code,http(s)/mailto:links, bullet lists), with an "edit" button that swaps in a textarea. Markdown rendering is a tiny, XSS-safe renderer — every substitution runs on HTML-escaped input, onlyhttp(s)/mailto:links pass through, andtarget="_blank"+rel="noopener noreferrer"are always set.
- Dependency editor— chip list of parents and children, each with an×to unlink, plus dropdowns over every other task to add a new parent or child. Cycle attempts are rejected server-side with a clear message.
- Status action row(→ triage / → ready / → running / block / unblock / complete / archive) with confirm prompts for destructive transitions. For cards in theTriagecolumn the row also exposes two LLM-driven actions:⚗ Decomposefans the task out into a graph of child tasks routed to specialist profiles by description, and✨ Specifydoes a single-task spec rewrite. Decompose falls back to specify-style promotion when the LLM decides the task doesn't benefit from fan-out, so it's a strict superset. Both are reachable from the CLI (hermes kanban decompose <id>/specify <id>/--all), from any gateway platform (/kanban decompose <id>), and programmatically viaPOST /api/plugins/kanban/tasks/:id/decomposeand…/specify. Configure the models underauxiliary.kanban_decomposerandauxiliary.triage_specifierinconfig.yaml.
- Result section (also markdown-rendered), comment thread with Enter-to-submit, the last 20 events.

`http(s)`
`mailto:`
`http(s)`
`mailto:`
`target="_blank"`
`rel="noopener noreferrer"`
`×`
`hermes kanban decompose <id>`
`specify <id>`
`--all`
`/kanban decompose <id>`
`POST /api/plugins/kanban/tasks/:id/decompose`
`…/specify`
`auxiliary.kanban_decomposer`
`auxiliary.triage_specifier`
`config.yaml`
`dashboard.kanban.default_tenant`
`config.yaml`

Visually the target is the familiar Linear / Fusion layout: dark theme, column headers with counts, coloured status dots, pill chips for priority and tenant. The plugin reads only theme CSS vars (--color-*,--radius,--font-mono, ...), so it reskins automatically with whichever dashboard theme is active.

`--color-*`
`--radius`
`--font-mono`

### Auto vs Manual orchestration​

The kanban board has two ways to handle a task you drop into the Triage column:

Auto (default)—kanban.auto_decompose: true. The gateway-embedded dispatcher runs thedecomposeron each tick, capped bykanban.auto_decompose_per_tick(default 3 tasks per tick) so a bulk-load of triage tasks doesn't burst-spend the auxiliary LLM. The decomposer uses the built-in decomposition prompt plus theauxiliary.kanban_decomposermodel path, reads your installed profiles + their descriptions, and asks the LLM to produce a JSON task graph: which tasks to spawn, who they go to, and which depend on which. The original triage task becomes the parent of every leaf in the graph, so it stays alive until the whole graph completes - and then promotes back toreadyso its assignee (kanban.orchestrator_profile, or the active default profile when unset) can judge completion and add more tasks if the work isn't done. This is the "drop a one-liner, walk away" flow.

`kanban.auto_decompose: true`
`kanban.auto_decompose_per_tick`
`auxiliary.kanban_decomposer`
`ready`
`kanban.orchestrator_profile`

Manual—kanban.auto_decompose: false. Triage tasks stay in triage until you act. Click the⚗ Decomposebutton on a card, runhermes kanban decompose <id>(or--all), or use/kanban decompose <id>from a chat. This matches the pre-decomposer behavior of the board, useful when you want full control over what runs when.

`kanban.auto_decompose: false`
`hermes kanban decompose <id>`
`--all`
`/kanban decompose <id>`

Flip between the two modes from theOrchestration: Auto/Manualpill at the top of the kanban page (emerald = Auto, muted gray = Manual), or by editingconfig.yamldirectly. Both modes coexist withhermes kanban specify— that's still available as a single-task spec rewrite when you don't want fan-out.

`config.yaml`
`hermes kanban specify`

The decomposer's routing decisions depend on profile descriptions, which is a per-profile labeling primitive you set withhermes profile create --description "...",hermes profile describe <name> --text "...",hermes profile describe <name> --auto(LLM-generates from the profile's installed skills + model), or the dashboard's per-profile editor in the expandedOrchestration settingspanel. Profiles without a description still appear in the roster — they're routable by name, just less precisely. The decomposer NEVER lands a child task withassignee=None: when the LLM picks an unknown profile, the child gets routed tokanban.default_assignee(or the active default profile if that's unset).

`hermes profile create --description "..."`
`hermes profile describe <name> --text "..."`
`hermes profile describe <name> --auto`
`assignee=None`
`kanban.default_assignee`

kanban.orchestrator_profiledoes not load that profile's prompt, skills, or custom logic into the decomposition call. It controls who owns the root/orchestration task after fan-out. To change the decomposer's model/provider, configureauxiliary.kanban_decomposer. To use a profile's custom task-splitting logic instead of the built-in decomposer, switch to Manual mode and have that profile create or decompose tasks explicitly.

`kanban.orchestrator_profile`
`auxiliary.kanban_decomposer`

Config knobs (all underkanban:in~/.hermes/config.yaml):

`kanban:`
`~/.hermes/config.yaml`
| Key | Default | Purpose |
| --- | --- | --- |
| auto_decompose | true | Dispatcher auto-runs the decomposer every tick. |
| auto_decompose_per_tick | 3 | Cap on decompositions per dispatcher tick. Excess defers to the next tick. |
| orchestrator_profile | "" | Profile assigned to the root/orchestration task after decomposition. Empty = fall back to active default profile. |
| default_assignee | "" | Where a child task lands when the LLM picks an unknown profile. Empty = fall back to active default. |
| auto_subscribe_on_create | true | When a worker callskanban_createfrom inside a session with a persistent delivery channel (messaging gateway or TUI), the originating session is auto-subscribed to the new task's completion/block events. The dispatcher still drives the delivery — this only changes whether the caller's chat/key shows up in the notify-sub table. Set tofalseto require explicitkanban_notify-subscribecalls per task. |

`auto_decompose`
`true`
`auto_decompose_per_tick`
`3`
`orchestrator_profile`
`""`
`default_assignee`
`""`
`auto_subscribe_on_create`
`true`
`kanban_create`
`false`
`kanban_notify-subscribe`

And the two auxiliary LLM slots:

| Key | Purpose |
| --- | --- |
| auxiliary.kanban_decomposer | Model that produces the task graph (called by Decompose). Setprovider/modelto override the main chat model. |
| auxiliary.profile_describer | Model that auto-generates profile descriptions (called byhermes profile describe --auto). |

`auxiliary.kanban_decomposer`
`provider`
`model`
`auxiliary.profile_describer`
`hermes profile describe --auto`

### Architecture​

The GUI is strictly aread-through-the-DB + write-through-kanban_dblayer with no domain logic of its own:

```
┌────────────────────────┐      WebSocket (tails task_events)│   React SPA (plugin)   │ ◀──────────────────────────────────┐│   HTML5 drag-and-drop  │                                    │└──────────┬─────────────┘                                    │           │ REST over fetchJSON                              │           ▼                                                  │┌────────────────────────┐     writes call kanban_db.*        ││  FastAPI router        │     directly — same code path      ││  plugins/kanban/       │     the CLI /kanban verbs use      ││  dashboard/plugin_api.py                                    │└──────────┬─────────────┘                                    │           │                                                  │           ▼                                                  │┌────────────────────────┐                                    ││  ~/.hermes/kanban.db   │ ───── append task_events ──────────┘│  (WAL, shared)         │└────────────────────────┘
```

### REST surface​

All routes are mounted under/api/plugins/kanban/and protected by the dashboard's ephemeral session token:

`/api/plugins/kanban/`
| Method | Path | Purpose |
| --- | --- | --- |
| GET | /board?tenant=<name>&include_archived=… | Full board grouped by status column, plus tenants + assignees for filter dropdowns |
| GET | /tasks/:id | Task + comments + events + links |
| POST | /tasks | Create (wrapskanban_db.create_task, acceptstriage: boolandparents: [id, …]) |
| PATCH | /tasks/:id | Status / assignee / priority / title / body / result |
| POST | /tasks/bulk | Apply the same patch (status / archive / assignee / priority) to every id inids. Per-id failures reported without aborting siblings |
| POST | /tasks/:id/comments | Append a comment |
| POST | /tasks/:id/specify | Run the triage specifier — auxiliary LLM fleshes out the task body and promotes it fromtriagetotodo. Returns{ok, task_id, reason, new_title};ok=falsewith a human-readable reason on "not in triage" / no aux client / LLM error is a 200, not a 4xx |
| POST | /tasks/:id/decompose | Run the kanban decomposer — auxiliary LLM produces a task graph and the helper atomically creates the children + links the root + flipstriage → todo. Returns{ok, task_id, reason, fanout, child_ids, new_title}. Same 200-on-LLM-error convention as/specify. |
| GET | /profiles | List installed profiles with their descriptions (consumed by the dashboard's profile-description editor and the orchestrator picker). |
| PATCH | /profiles/:name | Set or clear a profile's description (user-authored —description_auto: false). Returns{ok, profile, description}. |
| POST | /profiles/:name/describe-auto | Generate a description for a profile viaauxiliary.profile_describer. Persists withdescription_auto: trueso the dashboard can surface a "review" badge. |
| GET | /orchestration | Read the kanban orchestration settings (orchestrator_profile,default_assignee,auto_decompose) plus theresolvedeffective values after fallbacks. |
| PUT | /orchestration | Update one or more of the three orchestration keys inconfig.yaml. Validates that non-empty profile names actually exist. |
| POST | /links | Add a dependency (parent_id→child_id) |
| DELETE | /links?parent_id=…&child_id=… | Remove a dependency |
| POST | /dispatch?max=…&dry_run=… | Nudge the dispatcher — skip the 60 s wait |
| GET | /config | Readdashboard.kanbanpreferences fromconfig.yaml—default_tenant,lane_by_profile,include_archived_by_default,render_markdown |
| WS | /events?since=<event_id> | Live stream oftask_eventsrows |

`GET`
`/board?tenant=<name>&include_archived=…`
`GET`
`/tasks/:id`
`POST`
`/tasks`
`kanban_db.create_task`
`triage: bool`
`parents: [id, …]`
`PATCH`
`/tasks/:id`
`POST`
`/tasks/bulk`
`ids`
`POST`
`/tasks/:id/comments`
`POST`
`/tasks/:id/specify`
`triage`
`todo`
`{ok, task_id, reason, new_title}`
`ok=false`
`POST`
`/tasks/:id/decompose`
`triage → todo`
`{ok, task_id, reason, fanout, child_ids, new_title}`
`/specify`
`GET`
`/profiles`
`PATCH`
`/profiles/:name`
`description_auto: false`
`{ok, profile, description}`
`POST`
`/profiles/:name/describe-auto`
`auxiliary.profile_describer`
`description_auto: true`
`GET`
`/orchestration`
`orchestrator_profile`
`default_assignee`
`auto_decompose`
`PUT`
`/orchestration`
`config.yaml`
`POST`
`/links`
`parent_id`
`child_id`
`DELETE`
`/links?parent_id=…&child_id=…`
`POST`
`/dispatch?max=…&dry_run=…`
`GET`
`/config`
`dashboard.kanban`
`config.yaml`
`default_tenant`
`lane_by_profile`
`include_archived_by_default`
`render_markdown`
`WS`
`/events?since=<event_id>`
`task_events`

Every handler is a thin wrapper — the plugin is ~700 lines of Python (router + WebSocket tail + bulk batcher + config reader) and adds no new business logic. A tiny_conn()helper auto-initializeskanban.dbon every read and write, so a fresh install works whether the user opened the dashboard first, hit the REST API directly, or ranhermes kanban init.

`_conn()`
`kanban.db`
`hermes kanban init`

### Dashboard config​

Any of these keys underdashboard.kanbanin~/.hermes/config.yamlchanges the tab's defaults — the plugin reads them at load time viaGET /config:

`dashboard.kanban`
`~/.hermes/config.yaml`
`GET /config`

```
dashboard:  kanban:    default_tenant: acme              # preselects the tenant filter    lane_by_profile: true             # default for the "lanes by profile" toggle    include_archived_by_default: false    render_markdown: true             # set false for plain <pre> rendering
```

Each key is optional and falls back to the shown default.

### Security model​

The dashboard's HTTP auth middlewareexplicitly skips/api/plugins/— plugin routes are unauthenticated by design because the dashboard binds to localhost by default. That means the kanban REST surface is reachable from any process on the host.

`/api/plugins/`

The WebSocket takes one additional step: it requires the dashboard's ephemeral session token as a?token=…query parameter (browsers can't setAuthorizationon an upgrade request), matching the pattern used by the in-browser PTY bridge.

`?token=…`
`Authorization`

If you runhermes dashboard --host 0.0.0.0, every plugin route — kanban included — becomes reachable from the network.Don't do that on a shared host.The board contains task bodies, comments, and workspace paths; an attacker reaching these routes gets read access to your entire collaboration surface and can also create / reassign / archive tasks.

`hermes dashboard --host 0.0.0.0`

Tasks in~/.hermes/kanban.dbare profile-agnostic on purpose (that's the coordination primitive). If you open the dashboard withhermes -p <profile> dashboard, the board still shows tasks created by any other profile on the host. Same user owns all profiles, but this is worth knowing if multiple personas coexist.

`~/.hermes/kanban.db`
`hermes -p <profile> dashboard`

### Live updates​

task_eventsis an append-only SQLite table with a monotonicid. The WebSocket endpoint holds each client's last-seen event id and pushes new rows as they land. When a burst of events arrives, the frontend reloads the (very cheap) board endpoint — simpler and more correct than trying to patch local state from every event kind. WAL mode means the read loop never blocks the dispatcher'sBEGIN IMMEDIATEclaim transactions.

`task_events`
`id`
`BEGIN IMMEDIATE`

### Extending it​

The plugin uses the standard Hermes dashboard plugin contract — seeExtending the Dashboardfor the full manifest reference, shell slots, page-scoped slots, and the Plugin SDK. Extra columns, custom card chrome, tenant-filtered layouts, or fulltab.overridereplacements are all expressible without forking this plugin.

`tab.override`

To disable without removing: adddashboard.plugins.kanban.enabled: falsetoconfig.yaml(or deleteplugins/kanban/dashboard/manifest.json).

`dashboard.plugins.kanban.enabled: false`
`config.yaml`
`plugins/kanban/dashboard/manifest.json`

### Scope boundary​

The GUI is deliberately thin. Everything the plugin does is reachable from the CLI; the plugin just makes it comfortable for humans. Auto-assignment, budgets, governance gates, and org-chart views remain user-space — a router profile, another plugin, or a reuse oftools/approval.py— exactly as listed in the out-of-scope section of the design spec.

`tools/approval.py`

## CLI command reference​

This is the surfaceyou(or scripts, cron, the dashboard) use to drive the board. Workers running inside the dispatcher use thekanban_*tool surfacefor the same operations — the CLI here and the tools there both route throughkanban_db, so the two surfaces agree by construction.

`kanban_*`
`kanban_db`

```
hermes kanban init                                     # create kanban.db + print daemon hinthermes kanban create "<title>" [--body ...] [--assignee <profile>]                                [--parent <id>]... [--tenant <name>]                                [--workspace scratch|worktree|worktree:<path>|dir:<path>]                                [--branch <name>]                                [--priority N] [--triage] [--idempotency-key KEY]                                [--max-runtime 30m|2h|1d|<seconds>]                                [--max-retries N]                                [--goal] [--goal-max-turns N]                                [--skill <name>]...                                [--json]hermes kanban list [--mine] [--assignee P] [--status S] [--tenant T] [--archived]        [--workflow-template-id <id>] [--current-step-key <key>]        [--sort created|created-desc|priority|priority-desc|status|assignee|title|updated]        [--json]hermes kanban show <id> [--json]hermes kanban assign <id> <profile>                    # or 'none' to unassignhermes kanban reassign <id>... <profile>               # bulk re-assign tasks to a profilehermes kanban edit <id> [--title ...] [--body ...]     # edit task title / body / priority in place        [--priority N]hermes kanban promote <id>...                          # move todo/blocked tasks to ready (recovery)hermes kanban schedule <id> --at <ISO8601>             # set/clear a task's scheduled_at start timehermes kanban diagnostics [--json]                     # board health snapshot (alias: diag)hermes kanban link <parent_id> <child_id>hermes kanban unlink <parent_id> <child_id>hermes kanban claim <id> [--ttl SECONDS]hermes kanban comment <id> "<text>" [--author NAME]# Bulk verbs — accept multiple ids:hermes kanban complete <id>... [--result "..."]hermes kanban block <id> "<reason>" [--ids <id>...]hermes kanban unblock <id>...hermes kanban archive <id>...hermes kanban tail <id>                                # follow a single task's event streamhermes kanban watch [--assignee P] [--tenant T]        # live stream ALL events to the terminal        [--kinds completed,blocked,…] [--interval SECS]hermes kanban heartbeat <id> [--note "..."]            # worker liveness signal for long opshermes kanban runs <id> [--json]                       # attempt history (one row per run)hermes kanban assignees [--json]                       # profiles on disk + per-assignee task countshermes kanban dispatch [--dry-run] [--max N]           # one-shot pass        [--failure-limit N] [--json]hermes kanban daemon --force                           # DEPRECATED — standalone dispatcher (use `hermes gateway start` instead)        [--failure-limit N] [--pidfile PATH] [-v]hermes kanban stats [--json]                           # per-status + per-assignee countshermes kanban log <id> [--tail BYTES]                  # worker log from ~/.hermes/kanban/logs/hermes kanban notify-subscribe <id>                    # gateway bridge hook (used by /kanban in the gateway)        --platform <name> --chat-id <id> [--thread-id <id>] [--user-id <id>]hermes kanban notify-list [<id>] [--json]hermes kanban notify-unsubscribe <id>        --platform <name> --chat-id <id> [--thread-id <id>]hermes kanban context <id>                             # what a worker seeshermes kanban specify [<id> | --all] [--tenant T]      # flesh out a triage-column idea        [--author NAME] [--json]                       #   into a full spec and promote to todohermes kanban gc [--event-retention-days N]            # workspaces + old events + old logs        [--log-retention-days N]
```

All commands are also available as a slash command in the interactive CLI and in the messaging gateway (see/kanbanslash commandbelow).

`/kanban`

--max-retriesis a per-task circuit-breaker override for the dispatcher.--max-retries 1blocks the task on the first non-successful attempt, while--max-retries 3allows two retries and blocks on the third failure. Omit it to usekanban.failure_limitfromconfig.yaml, then the built-in default.

`--max-retries`
`--max-retries 1`
`--max-retries 3`
`kanban.failure_limit`
`config.yaml`

### Concurrency, scheduling, and child promotion config​

| Config key | Default | What it does |
| --- | --- | --- |
| kanban.max_in_progress | unset (unlimited) | Caps the number of simultaneously running tasks. When the board already has N running, the dispatcher skips spawning more — useful for slow workers (local LLMs, resource-constrained hosts) so they finish what they have before more pile up and time out. Invalid or below-1 values log a warning and behave as unlimited. |
| kanban.max_in_progress_per_profile | unset (unlimited) | Per-profile variant ofmax_in_progress— caps how many tasks any single assignee profile may run concurrently. Useful when one profile is slow or rate-limited but others should keep flowing. Applies alongside the board-widemax_in_progress; both must allow a spawn for it to proceed. |
| kanban.auto_promote_children | true | Afterdecompose_triage_task()produces children with no parent-blocker dependencies, they're automatically promoted toreadyso the dispatcher can pick them up. Set tofalseto require manual review — children stay intodountil you promote them. |
| kanban.default_workdir | unset | Board-level default working directory applied to new tasks when neither--workspacenor the task itself overrides it. Per-taskworkspace:still wins. |

`kanban.max_in_progress`
`kanban.max_in_progress_per_profile`
`max_in_progress`
`max_in_progress`
`kanban.auto_promote_children`
`true`
`decompose_triage_task()`
`ready`
`false`
`todo`
`kanban.default_workdir`
`--workspace`
`workspace:`

```
kanban:  max_in_progress: 2  auto_promote_children: false  default_workdir: ~/work/active-project
```

### Scheduled task starts (scheduled_at)​

`scheduled_at`

Setscheduled_aton a task to delay dispatch until a specific time. The dispatcher skips ready tasks whosescheduled_atis in the future and picks them up on the first tick after that timestamp.

`scheduled_at`
`scheduled_at`

```
hermes kanban create "nightly backup audit" \  --assignee ops --scheduled-at "2026-06-01T03:00:00Z"
```

### Respawn guard​

The dispatcher refuses to re-spawn a ready task when it hit a quota/auth/429 error on the previous run (blocker_auth), or completed a run successfully within the guard window (recent_success), or a recent task comment links to a GitHub PR (active_pr). This prevents repeat worker storms on the same bug or task while a human catches up. See therespawn_guardedrow in theevent reference.

`blocker_auth`
`recent_success`
`active_pr`
`respawn_guarded`

### Drag-to-delete and bulk delete (dashboard)​

The dashboard exposes atrash drop zoneon the kanban page — drag any card into it to delete the task (cascades throughtask_events, child links, and subscriptions). A confirmation prompt protects against accidents. Bulk delete is also reachable viaDELETE /api/plugins/kanban/taskswith a JSON body{"ids": ["t_abc", "t_def", ...]}.

`task_events`
`DELETE /api/plugins/kanban/tasks`
`{"ids": ["t_abc", "t_def", ...]}`

### Worker visibility endpoints​

The dashboard plugin API now exposes these read-only endpoints (plus a run-control verb) for external monitors:

| Endpoint | Returns |
| --- | --- |
| GET /api/plugins/kanban/workers/active | Currently spawned workers with PID, profile, task id, started-at, last heartbeat |
| GET /api/plugins/kanban/runs/{id} | Single-run detail — task id, status, started/ended, exit code, log path |
| POST /api/plugins/kanban/runs/{run_id}/terminate | Terminate a reclaimable run — stops the worker and frees the task for re-dispatch |
| GET /api/plugins/kanban/inspect | Combined dispatcher snapshot — backlog, in-progress count vs.max_in_progress, recent events |

`GET /api/plugins/kanban/workers/active`
`GET /api/plugins/kanban/runs/{id}`
`POST /api/plugins/kanban/runs/{run_id}/terminate`
`GET /api/plugins/kanban/inspect`
`max_in_progress`

All of these are gated by the same dashboard plugin auth as the rest of the kanban plugin API.

### Kanban Swarm topology helper​

hermes kanban swarmcreates a durableKanban Swarm v1graph in one shot: a completed root/blackboard card, N parallel worker cards, a verifier card gated on all workers, and a synthesizer card gated on the verifier. Shared swarm context (the "blackboard") is stored as structured JSON comments on the root card so any worker can read it.

`hermes kanban swarm`

```
hermes kanban swarm "Design a multi-region failover plan" \  --workers researcher,architect,sre \  --verifier reviewer --synthesizer writer
```

The resulting graph dispatches normally — workers run in parallel, the verifier wakes after they all finish, the synthesizer wakes after the verifier marks the work clean.

## /kanbanslash command​

`/kanban`

Everyhermes kanban <action>verb is also reachable as/kanban <action>— from inside an interactivehermes chatsessionandfrom any gateway platform (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, email, SMS). Both surfaces call the exact samehermes_cli.kanban.run_slash()entry point that reuses thehermes kanbanargparse tree, so the argument surface, flags, and output format are identical across CLI,/kanban, andhermes kanban. You don't have to leave the chat to drive the board.

`hermes kanban <action>`
`/kanban <action>`
`hermes chat`
`hermes_cli.kanban.run_slash()`
`hermes kanban`
`/kanban`
`hermes kanban`

```
/kanban list/kanban show t_abcd/kanban create "write launch post" --assignee writer --parent t_research/kanban comment t_abcd "looks good, ship it"/kanban unblock t_abcd/kanban dispatch --max 3/kanban specify t_abcd                  # flesh out a triage one-liner into a real spec/kanban specify --all --tenant engineering  # sweep every triage task in one tenant
```

Quote multi-word arguments the same way you would on a shell —run_slashparses the rest of the line withshlex.split, so"..."and'...'both work.

`run_slash`
`shlex.split`
`"..."`
`'...'`

### Mid-run usage:/kanbanbypasses the running-agent guard​

`/kanban`

The gateway normally queues slash commands and user messages while an agent is still thinking — that's what stops you from accidentally starting a second turn while the first is in flight./kanbanis explicitly exempted from this guard.The board lives in~/.hermes/kanban.db, not in the running agent's state, so reads (list,show,context,tail,watch,stats,runs) and writes (comment,unblock,block,assign,archive,create,link, …) all go through immediately, even mid-turn.

`/kanban`
`~/.hermes/kanban.db`
`list`
`show`
`context`
`tail`
`watch`
`stats`
`runs`
`comment`
`unblock`
`block`
`assign`
`archive`
`create`
`link`

This is the whole point of the separation:

- A worker blocks waiting on a peer → you send/kanban unblock t_abcdfrom your phone and the dispatcher picks the peer up on its next tick. The blocked worker isn't interrupted — it just stops being blocked.
- You spot a card that needs human context →/kanban comment t_xyz "use the 2026 schema, not 2025"lands on the task thread and thenextrun of that task will read it inkanban_show().
- You want to know what your fleet is doing without stopping the orchestrator →/kanban list --mineor/kanban statsinspects the board without touching your main conversation.

`/kanban unblock t_abcd`
`/kanban comment t_xyz "use the 2026 schema, not 2025"`
`kanban_show()`
`/kanban list --mine`
`/kanban stats`

### Auto-subscribe on/kanban create(gateway only)​

`/kanban create`

When you create a task from the gateway with/kanban create "…", the originating chat (platform + chat id + thread id) is automatically subscribed to that task's terminal events (completed,blocked,gave_up,crashed,timed_out). You'll get one message back per terminal event — including the first line of the worker's result summary oncompleted— without having to poll or remember the task id.

`/kanban create "…"`
`completed`
`blocked`
`gave_up`
`crashed`
`timed_out`
`completed`

```
you> /kanban create "transcribe today's podcast" --assignee transcriberbot> Created t_9fc1a3  (ready, assignee=transcriber)     (subscribed — you'll be notified when t_9fc1a3 completes or blocks)… ~8 minutes later …bot> ✓ t_9fc1a3 completed by transcriber     transcribed 42 minutes, saved to podcast/2026-05-04.md
```

Subscriptions auto-remove themselves once the task reachesdoneorarchived. If you script a create with--json(machine output) the auto-subscribe is skipped — the assumption is that scripted callers want to manage subscriptions explicitly via/kanban notify-subscribe.

`done`
`archived`
`--json`
`/kanban notify-subscribe`

### Output truncation in messaging​

Gateway platforms have practical message-length caps. If/kanban list,/kanban show, or/kanban tailproduce more than ~3800 characters of output, the response is truncated with a… (truncated; use \hermes kanban …` in your terminal for full output)` footer. The CLI surface has no such cap.

`/kanban list`
`/kanban show`
`/kanban tail`
`… (truncated; use \`

### Autocomplete​

In the interactive CLI, typing/kanbanand hitting Tab cycles through the built-in subcommand list (list,ls,show,create,assign,link,unlink,claim,comment,complete,block,unblock,archive,tail,dispatch,context,init,gc). The remaining verbs listed in the CLI reference above (watch,stats,runs,log,assignees,heartbeat,notify-subscribe,notify-list,notify-unsubscribe,daemon) also work — they're just not in the autocomplete hint list yet.

`/kanban `
`list`
`ls`
`show`
`create`
`assign`
`link`
`unlink`
`claim`
`comment`
`complete`
`block`
`unblock`
`archive`
`tail`
`dispatch`
`context`
`init`
`gc`
`watch`
`stats`
`runs`
`log`
`assignees`
`heartbeat`
`notify-subscribe`
`notify-list`
`notify-unsubscribe`
`daemon`

## Collaboration patterns​

The board supports these eight patterns without any new primitives:

| Pattern | Shape | Example |
| --- | --- | --- |
| P1 Fan-out | N siblings, same role | "research 5 angles in parallel" |
| P2 Pipeline | role chain: scout → editor → writer | daily brief assembly |
| P3 Voting / quorum | N siblings + 1 aggregator | 3 researchers → 1 reviewer picks |
| P4 Long-running journal | same profile + shared dir + cron | Obsidian vault |
| P5 Human-in-the-loop | worker blocks → user comments → unblock | ambiguous decisions |
| P6@mention | inline routing from prose | @reviewer look at this |
| P7 Thread-scoped workspace | /kanban herein a thread | per-project gateway threads |
| P8 Fleet farming | one profile, N subjects | 50 social accounts |
| P9 Triage specifier | rough idea →triage→hermes kanban specifyexpands body →todo | "turn this one-liner into a spec'd task" |

`@mention`
`@reviewer look at this`
`/kanban here`
`triage`
`hermes kanban specify`
`todo`

For worked examples of each, seedocs/hermes-kanban-v1-spec.pdf.

`docs/hermes-kanban-v1-spec.pdf`

## Multi-tenant usage​

When one specialist fleet serves multiple businesses, tag each task with a tenant:

```
hermes kanban create "monthly report" \    --assignee researcher \    --tenant business-a \    --workspace dir:~/tenants/business-a/data/
```

Workers receive$HERMES_TENANTand namespace their memory writes by prefix. The board, the dispatcher, and the profile definitions are all shared; only the data is scoped.

`$HERMES_TENANT`

## Gateway notifications​

When you run/kanban create …from the gateway (Telegram, Discord, Slack, etc.), the originating chat is automatically subscribed to the new task. The gateway's background notifier pollstask_eventsevery few seconds and delivers one message per terminal event (completed,blocked,gave_up,crashed,timed_out) to that chat. Completed tasks also send the first line of the worker's--resultso you see the outcome without having to/kanban show.

`/kanban create …`
`task_events`
`completed`
`blocked`
`gave_up`
`crashed`
`timed_out`
`--result`
`/kanban show`

You can manage subscriptions explicitly from the CLI — useful when a script / cron job wants to notify a chat it didn't originate from:

```
hermes kanban notify-subscribe t_abcd \    --platform telegram --chat-id 12345678 --thread-id 7hermes kanban notify-listhermes kanban notify-unsubscribe t_abcd \    --platform telegram --chat-id 12345678 --thread-id 7
```

A subscription removes itself automatically once the task reachesdoneorarchived; no cleanup needed.

`done`
`archived`

## Runs — one row per attempt​

A task is a logical unit of work; arunis one attempt to execute it. When the dispatcher claims a ready task it creates a row intask_runsand pointstasks.current_run_idat it. When that attempt ends — completed, blocked, crashed, timed out, spawn-failed, reclaimed — the run row closes with anoutcomeand the task's pointer clears. A task that's been attempted three times has threetask_runsrows.

`task_runs`
`tasks.current_run_id`
`outcome`
`task_runs`

Why two tables instead of just mutating the task: you needfull attempt historyfor real-world postmortems ("the second reviewer attempt got to approve, the third merged"), and you need a clean place to hang per-attempt metadata — which files changed, which tests ran, which findings a reviewer noted. Those are run facts, not task facts.

Runs are also wherestructured handofflives. When a worker completes a task (viakanban_complete(...)) it can pass:

`kanban_complete(...)`
- summary(tool param) /--summary(CLI) — human handoff; goes on the run; downstream children see it in theirbuild_worker_context.
- metadata(tool param) /--metadata(CLI) — free-form JSON dict on the run; children see it serialized alongside the summary.
- result(tool param) /--result(CLI) — short log line that goes on the task row (legacy field, kept for back-compat).

`summary`
`--summary`
`build_worker_context`
`metadata`
`--metadata`
`result`
`--result`

Downstream children read the most recent completed run's summary + metadata for each parent. Retrying workers read the prior attempts on their own task (outcome, summary, error) so they don't repeat a path that already failed.

```
# What a worker actually does — a tool call, from inside the agent loop:kanban_complete(    summary="implemented token bucket, keys on user_id with IP fallback, all tests pass",    metadata={"changed_files": ["limiter.py", "tests/test_limiter.py"], "tests_run": 14},    result="rate limiter shipped",)
```

The same handoff is reachable from the CLI when you (the human) need to close out a task a worker can't — e.g. a task that was abandoned, or one you marked done manually from the dashboard:

```
hermes kanban complete t_abcd \    --result "rate limiter shipped" \    --summary "implemented token bucket, keys on user_id with IP fallback, all tests pass" \    --metadata '{"changed_files": ["limiter.py", "tests/test_limiter.py"], "tests_run": 14}'# Review the attempt history on a retried task:hermes kanban runs t_abcd#   #  OUTCOME       PROFILE           ELAPSED  STARTED#   1  blocked       worker               12s  2026-04-27 14:02#        → BLOCKED: need decision on rate-limit key#   2  completed     worker                8m   2026-04-27 15:18#        → implemented token bucket, keys on user_id with IP fallback
```

Runs are exposed on the dashboard (Run History section in the drawer, one coloured row per attempt) and on the REST API (GET /api/plugins/kanban/tasks/:idreturns aruns[]array).PATCH /api/plugins/kanban/tasks/:idwith{status: "done", summary, metadata}forwards both to the kernel, so the dashboard's "mark done" button is CLI-equivalent.task_eventsrows carry therun_idthey belong to so the UI can group them by attempt, and thecompletedevent embeds the first-line summary in its payload (capped at 400 chars) so gateway notifiers can render structured handoffs without a second SQL round-trip.

`GET /api/plugins/kanban/tasks/:id`
`runs[]`
`PATCH /api/plugins/kanban/tasks/:id`
`{status: "done", summary, metadata}`
`task_events`
`run_id`
`completed`

Bulk close caveat.hermes kanban complete a b c --summary Xis refused — structured handoff is per-run, so copy-pasting the same summary to N tasks is almost always wrong. Bulk closewithout--summary/--metadatastill works for the common "I finished a pile of admin tasks" case.

`hermes kanban complete a b c --summary X`
`--summary`
`--metadata`

Reclaimed runs from status changes.If you drag a running task offrunningin the dashboard (back toready, or straight totodo), or archive a task that was still running, the in-flight run closes withoutcome='reclaimed'rather than being orphaned. Thetask_runsrow is always in a terminal state whentasks.current_run_idisNULL, and vice versa — that invariant holds across CLI, dashboard, dispatcher, and notifier.

`running`
`ready`
`todo`
`outcome='reclaimed'`
`task_runs`
`tasks.current_run_id`
`NULL`

Synthetic runs for never-claimed completions.Completing or blocking a task that was never claimed (e.g. a human closes areadytask from the dashboard with a summary, or a CLI user runshermes kanban complete <ready-task> --summary X) would otherwise drop the handoff. Instead the kernel inserts a zero-duration run row (started_at == ended_at) carrying the summary / metadata / reason so attempt history stays complete. Thecompleted/blockedevent'srun_idpoints at that row.

`ready`
`hermes kanban complete <ready-task> --summary X`
`started_at == ended_at`
`completed`
`blocked`
`run_id`

Live drawer refresh.When the dashboard's WebSocket event stream reports new events for the task the user is currently viewing, the drawer reloads itself (via a per-task event counter threaded into itsuseEffectdependency list). Closing and reopening is no longer required to see a run's new row or updated outcome.

`useEffect`

### Forward compatibility​

Two nullable columns ontasksare reserved for v2 workflow routing:workflow_template_id(which template this task belongs to) andcurrent_step_key(which step in that template is active). The v1 kernel ignores them for routing but lets clients write them, so a v2 release can add the routing machinery without another schema migration.

`tasks`
`workflow_template_id`
`current_step_key`

## Event reference​

Every transition appends a row totask_events. Each row carries an optionalrun_idso UIs can group events by attempt. Kinds group into three clusters so filtering is easy (hermes kanban watch --kinds completed,gave_up,timed_out):

`task_events`
`run_id`
`hermes kanban watch --kinds completed,gave_up,timed_out`

Lifecycle(what changed about the task as a logical unit):

| Kind | Payload | When |
| --- | --- | --- |
| created | {assignee, status, parents, tenant} | Task inserted.run_idisNULL. |
| promoted | — | todo → readybecause all parents hitdone.run_idisNULL. |
| claimed | {lock, expires, run_id} | Dispatcher atomically claimed areadytask for spawn. |
| completed | {result_len, summary?} | Worker wrote--result/--summaryand task hitdone.summaryis the first-line handoff (400-char cap); full version lives on the run row. Ifcomplete_taskis called on a never-claimed task with handoff fields, a zero-duration run is synthesized sorun_idstill points at something. |
| blocked | {reason, kind, recurrences} | Worker or human flipped the task toblocked.kindis the typed block reason (needs_input,capability,transient, ornullfor a generic block);recurrencesis the unblock-loop counter. Synthesizes a zero-duration run when called on a never-claimed task with--reason. |
| dependency_wait | {reason, kind} | Worker blocked withkind=dependency— the task is only waiting on another task, so it routes totodo(parent-gated, auto-promoted) instead ofblocked. No human needed. |
| block_loop_detected | {reason, kind, recurrences, limit} | A task was unblocked and re-blocked for the same reasonBLOCK_RECURRENCE_LIMITtimes (default 2). Instead of landing inblockedagain — where a cron would keep unblocking it — it routes totriagefor a human decision, breaking the unblock↔re-block loop. |
| unblocked | — | blocked → ready(ortodoif parents are still open), either manually or via/unblock. Resets the dispatcher'sconsecutive_failuresbut deliberately preservesblock_recurrencesso the loop breaker keeps its memory.run_idisNULL. |
| archived | — | Hidden from the default board. If the task was still running, carries therun_idof the run that was reclaimed as a side effect. |

`created`
`{assignee, status, parents, tenant}`
`run_id`
`NULL`
`promoted`
`todo → ready`
`done`
`run_id`
`NULL`
`claimed`
`{lock, expires, run_id}`
`ready`
`completed`
`{result_len, summary?}`
`--result`
`--summary`
`done`
`summary`
`complete_task`
`run_id`
`blocked`
`{reason, kind, recurrences}`
`blocked`
`kind`
`needs_input`
`capability`
`transient`
`null`
`recurrences`
`--reason`
`dependency_wait`
`{reason, kind}`
`kind=dependency`
`todo`
`blocked`
`block_loop_detected`
`{reason, kind, recurrences, limit}`
`BLOCK_RECURRENCE_LIMIT`
`blocked`
`triage`
`unblocked`
`blocked → ready`
`todo`
`/unblock`
`consecutive_failures`
`block_recurrences`
`run_id`
`NULL`
`archived`
`run_id`

Edits(human-driven changes that aren't transitions):

| Kind | Payload | When |
| --- | --- | --- |
| assigned | {assignee} | Assignee changed (including unassignment). |
| edited | {fields} | Title or body updated. |
| reprioritized | {priority} | Priority changed. |
| status | {status} | Dashboard drag-drop wrote a status directly (e.g.todo → ready). Carries therun_idof the run that was reclaimed when dragging offrunning; otherwiserun_idis NULL. |

`assigned`
`{assignee}`
`edited`
`{fields}`
`reprioritized`
`{priority}`
`status`
`{status}`
`todo → ready`
`run_id`
`running`
`run_id`

Worker telemetry(about the execution process, not the logical task):

| Kind | Payload | When |
| --- | --- | --- |
| spawned | {pid} | Dispatcher successfully started a worker process. |
| heartbeat | {note?} | Worker calledhermes kanban heartbeat $TASKto signal liveness during long operations. |
| reclaimed | {stale_lock} | Claim TTL expired without a completion; task goes back toready. |
| crashed | {pid, claimer} | Worker PID no longer alive but TTL hadn't expired yet. |
| timed_out | {pid, elapsed_seconds, limit_seconds, sigkill} | max_runtime_secondsexceeded; dispatcher SIGTERM'd (then SIGKILL'd after 5 s grace) and re-queued. |
| stale | {elapsed_seconds, last_heartbeat_at, heartbeat_age_seconds, timeout_seconds, pid, terminated} | Task ran longer thankanban.dispatch_stale_timeout_seconds(default 4 h) AND nokanban_heartbeatarrived in the last hour. Dispatcher SIGTERM'd the host-local worker (if any), reset the task toreadyfor re-dispatch. Does NOT tick the failure counter (stale is dispatcher-side absence detection, not a worker fault). Workers running long operations should callkanban_heartbeatat least once an hour to avoid this. |
| respawn_guarded | {reason} | Dispatcher refused to re-spawn this ready task this tick. Reasons:blocker_auth(last failure was a quota/auth/429 error — wait for the rate window to reset),recent_success(a completed run happened in the last hour — wait for review before re-running),active_pr(a GitHub PR URL appears in a recent comment — a prior worker already opened a PR). The task stays inready; the next tick gets another chance to spawn. If the underlying condition persists, the normalconsecutive_failurescircuit breaker will auto-block viagave_upafterfailure_limitfailures. |
| spawn_failed | {error, failures} | One spawn attempt failed (missing PATH, workspace unmountable, …). Counter increments; task returns toreadyfor retry. |
| protocol_violation | {pid, claimer, exit_code} | Worker exited successfully while the task was stillrunning, usually because it answered without callingkanban_completeorkanban_block. The dispatcher also emitsgave_upand auto-blocks immediately instead of retrying. |
| gave_up | {failures, effective_limit, limit_source, error} | Circuit breaker fired after N consecutive non-successful attempts. Task auto-blocks with the last error. The effective limit resolves as taskmax_retries, then dispatcherfailure_limit/kanban.failure_limit, then the built-in default. |

`spawned`
`{pid}`
`heartbeat`
`{note?}`
`hermes kanban heartbeat $TASK`
`reclaimed`
`{stale_lock}`
`ready`
`crashed`
`{pid, claimer}`
`timed_out`
`{pid, elapsed_seconds, limit_seconds, sigkill}`
`max_runtime_seconds`
`stale`
`{elapsed_seconds, last_heartbeat_at, heartbeat_age_seconds, timeout_seconds, pid, terminated}`
`kanban.dispatch_stale_timeout_seconds`
`kanban_heartbeat`
`ready`
`kanban_heartbeat`
`respawn_guarded`
`{reason}`
`blocker_auth`
`recent_success`
`active_pr`
`ready`
`consecutive_failures`
`gave_up`
`failure_limit`
`spawn_failed`
`{error, failures}`
`ready`
`protocol_violation`
`{pid, claimer, exit_code}`
`running`
`kanban_complete`
`kanban_block`
`gave_up`
`gave_up`
`{failures, effective_limit, limit_source, error}`
`max_retries`
`failure_limit`
`kanban.failure_limit`

hermes kanban tail <id>shows these for a single task.hermes kanban watchstreams them board-wide.

`hermes kanban tail <id>`
`hermes kanban watch`

## Out of scope​

Kanban is deliberately single-host.~/.hermes/kanban.dbis a local SQLite file and the dispatcher spawns workers on the same machine. Running a shared board across two hosts is not supported — there's no coordination primitive for "worker X on host A, worker Y on host B," and the crash-detection path assumes PIDs are host-local. If you need multi-host, run an independent board per host and usedelegate_task/ a message queue to bridge them.

`~/.hermes/kanban.db`
`delegate_task`

## Design spec​

The complete design — architecture, concurrency correctness, comparison with other systems, implementation plan, risks, open questions — lives indocs/hermes-kanban-v1-spec.pdf. Read that before filing any behavior-change PR.

`docs/hermes-kanban-v1-spec.pdf`