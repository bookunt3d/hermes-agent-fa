---
layout: docs
title: "Features_Goals"
permalink: /docs/user-guide/features_goals/
---

- 
- Features
- Automation
- Persistent Goals

# Persistent Goals (/goal)

`/goal`

/goalgives Hermes a standing objective that survives across turns. After every turn a lightweight judge model checks whether the goal is satisfied by the assistant's last response. If not, Hermes automatically feeds a continuation prompt back into the same session and keeps working — until the goal is achieved, you pause or clear it, or the turn budget runs out.

`/goal`

It's our take on theRalph loop, directly inspired byCodex CLI 0.128.0's/goalby Eric Traut (OpenAI). The core idea — keep a goal alive across turns and don't stop until it's achieved — is theirs. The implementation here is independent and adapted to Hermes' architecture.

`/goal`

## When to use it​

Use/goalfor tasks where you want Hermes to iterate on its own without you re-prompting every turn:

`/goal`
- "Fix every lint error insrc/and verifyruff checkpasses"
- "Port feature X from repo Y, including tests, and get CI green"
- "Investigate why session IDs sometimes drift on mid-run compression and write up a report"
- "Build a small CLI to rename files by their EXIF dates, then test it against the photos/ folder"

`src/`
`ruff check`

Tasks where the agent does one turn and stops don't need/goal. Tasks whereyou'd otherwise have to say "keep going" three timesare where this shines.

`/goal`

## Quick start​

```
/goal Fix every failing test in tests/hermes_cli/ and make sure scripts/run_tests.sh passes for that directory
```

What you'll see:

1. Goal accepted—⊙ Goal set (20-turn budget): <your goal>
2. Turn 1 runs— Hermes starts working as if you'd sent the goal as a normal message.
3. Judge runs— after the turn, the judge model decidesdoneorcontinue.
4. Loop fires if needed— ifcontinue, you'll see↻ Continuing toward goal (1/20): <judge's reason>and Hermes takes the next step automatically.
5. Terminates— eventually you see either✓ Goal achieved: <reason>or⏸ Goal paused — N/20 turns used.

`⊙ Goal set (20-turn budget): <your goal>`
`done`
`continue`
`continue`
`↻ Continuing toward goal (1/20): <judge's reason>`
`✓ Goal achieved: <reason>`
`⏸ Goal paused — N/20 turns used`

## Commands​

| Command | What it does |
| --- | --- |
| /goal <text> | Set (or replace) the standing goal. Kicks off the first turn immediately so you don't need to send a separate message. |
| /goal draft <text> | Draft a structured completion contract from a plain-language objective, then set it. SeeCompletion contracts. |
| /goal show | Print the active goal's completion contract. |
| /goalor/goal status | Show the current goal, its status, and turns used. |
| /goal pause | Stop the auto-continuation loop without clearing the goal. |
| /goal resume | Resume the loop (resets the turn counter back to zero). |
| /goal clear | Drop the goal entirely. |
| /goal wait <pid> [reason] | Park the loop on a background process — it stops re-poking the agent every turn while the process runs, and auto-resumes when it exits. |
| /goal unwait | Drop the wait barrier and resume the loop immediately. |

`/goal <text>`
`/goal draft <text>`
`/goal show`
`/goal`
`/goal status`
`/goal pause`
`/goal resume`
`/goal clear`
`/goal wait <pid> [reason]`
`/goal unwait`

Works identically on the CLI and every gateway platform (Telegram, Discord, Slack, Matrix, Signal, WhatsApp, SMS, iMessage, Webhook, API server, and the web dashboard).

## Completion contracts​

A bare/goal <text>works fine, but avaguegoal makes for vague judging — the judge can only check what you told it to want. Codex's/goalguidance makes the same point: a durable objective works best when it nameswhat done means, how to prove it, what not to break, what's in scope, and when to stop. Hermes adapts this as an optionalcompletion contractlayered on top of the existing goal loop.

`/goal <text>`
`/goal`

A contract has five fields, all optional:

| Field | Meaning |
| --- | --- |
| outcome | The single end state that must be true when done. |
| verification | The specific test / command / artifact thatprovesthe outcome. |
| constraints | What must not change or regress. |
| boundaries | Which files, dirs, tools, or systems are in scope. |
| stop_when | The condition under which Hermes should stop and ask for input. |

`outcome`
`verification`
`constraints`
`boundaries`
`stop_when`

When a contract is set, both prompts change: thecontinuation prompttells the agent to target the verification surface and respect the constraints, and thejudge promptdecidesdoneonly when the verification criterion is met with concrete evidence(a command result, file excerpt, test output) — not a loose "looks done" claim. This directly tightens the most common/goalfailure mode (premature completion or endless over-continuation on an underspecified objective).

`done`
`/goal`

### Two ways to set a contract​

1. Let Hermes draft it(recommended — adapted from Codex's "let the agent draft the goal" tip):

```
/goal draft Migrate the auth service from session cookies to JWT
```

Hermes expands your one-liner into a full contract via thegoal_judgeauxiliary model, sets it, and shows you the result so you can review or tighten any field. If the aux model is unavailable, it falls back to a plain free-form goal — drafting never blocks setting a goal.

`goal_judge`

2. Write it inlinewithfield: valuelines:

`field: value`

```
/goal Migrate auth to JWTverify: pytest tests/auth passesconstraints: keep the /login response shape unchangedboundaries: only touch services/auth and its testsstop when: a DB schema migration is required
```

The first non-field line(s) are the goal headline; recognized field prefixes (verify:,verified by:,constraints:,preserve:,boundaries:,scope:,stop when:,blocked:, …) populate the contract. A plain goal with an incidental colon (Fix bug: the parser drops commas) isnotmangled — only known field prefixes are pulled out.

`verify:`
`verified by:`
`constraints:`
`preserve:`
`boundaries:`
`scope:`
`stop when:`
`blocked:`
`Fix bug: the parser drops commas`

Use/goal showto review the active contract. Contracts persist inSessionDB.state_metaalongside the goal, so they survive/resume. Old goals from before this feature load unchanged (no contract). Contracts and/subgoalcriteria compose: subgoals fold into the contract as extra criteria the judge must also satisfy.

`/goal show`
`SessionDB.state_meta`
`/resume`
`/subgoal`

## Adding criteria mid-goal:/subgoal​

`/subgoal`

While a goal is active you can append extra acceptance criteria with/subgoal <text>without resetting the loop. Each call adds one numbered item to the goal's subgoal list; thecontinuation promptthe agent sees on the next turn includes the original goal plus an "Additional criteria the user added mid-loop" block, and thejudge promptis rewritten so the verdict must consider every subgoal — the goal isn't marked done until the original objectiveandevery subgoal are met.

`/subgoal <text>`
| Command | What it does |
| --- | --- |
| /subgoal <text> | Append a new criterion to the active goal. Requires an active/goal. |
| /subgoal(no args) | Show the current numbered subgoal list. |
| /subgoal remove <N> | Remove the Nth subgoal (1-based). |
| /subgoal clear | Drop every subgoal but keep the original goal intact. |

`/subgoal <text>`
`/goal`
`/subgoal`
`/subgoal remove <N>`
`/subgoal clear`

Subgoals are persisted alongside the goal inSessionDB.state_meta, so they survive/resume. Setting a new/goal <text>replaces the goal and clears the subgoal list;/goal cleardoes the same.

`SessionDB.state_meta`
`/resume`
`/goal <text>`
`/goal clear`

Use this when you start a loop ("fix the failing tests") and notice partway through that you also want it to "and add a regression test for the bug you just patched" —/subgoal add a regression testtightens the success criteria without breaking the running loop.

`/subgoal add a regression test`

## Parking on a background process: automatic, with a manual override​

Some goals are gated on something that takes minutes and runs on its own — CI on a pushed PR, a long build, a test matrix, a deploy, a rate-limit cooldown. Without help, the goal loop would re-poke the agent every turn into "is it done yet?" busy-work while it waits.

This is handled automatically.Every turn, the judge is shown the agent's live background processes (theterminal(background=true)registry — pid, session id, command, uptime, recent output, and anywatch_patterns/notify_on_completetrigger) alongside the goal and the agent's response. When the agent's progress is genuinely gated on one of them, the judge returns awaitverdict instead ofcontinue, and the loopparks: the next turns are skipped (no judge call, no continuation, no turn consumed) until the wait is satisfied — then it resumes normally with the result in hand. The judge can also park on atimebasis (wait_for_seconds) for backoff/cooldown waits./goal statusshows⏳ Goal (parked …)while parked.

`terminal(background=true)`
`watch_patterns`
`notify_on_complete`
`wait`
`continue`
`wait_for_seconds`
`/goal status`
`⏳ Goal (parked …)`

The judge picks the right kind of wait from the process's own signal:

- wait_on_session <id>— releases when the process'sown triggerfires: it exits,or(if it was started withwatch_patterns) its pattern matches. This is the one for a long-lived watcher / server / poller that signalsmid-run(e.g. a build process that printsBUILD SUCCESSFULand keeps running, or anotify_on_completewatcher) and may never exit on its own.
- wait_on_pid <pid>— releases on process exit only.
- wait_for_seconds <n>— releases after a fixed delay.

`wait_on_session <id>`
`watch_patterns`
`BUILD SUCCESSFUL`
`notify_on_complete`
`wait_on_pid <pid>`
`wait_for_seconds <n>`

You don't type anything for this — it's the judge's decision, made from the process context the loop hands it. The manual commands exist as an override:

| Command | What it does |
| --- | --- |
| /goal wait <pid> [reason] | Manually park the loop until the process with that PID exits. |
| /goal unwait | Clear any wait barrier (judge- or manually-set) and resume immediately. |

`/goal wait <pid> [reason]`
`/goal unwait`

The barrier (pid- or time-based) is persisted with the goal inSessionDB.state_meta, so it survives/resume./goal pause,/goal resume, and/goal clearall drop it. If the PID is already dead when the barrier is set (or dies while parked), or the time deadline passes, the barrier clears on the next check — a stale barrier can never wedge the loop.

`SessionDB.state_meta`
`/resume`
`/goal pause`
`/goal resume`
`/goal clear`

Typical flow: the agent pushes a PR, starts a CI watcher withterminal(background=true, notify_on_complete=true), and reports "watching CI." The judge sees the watcher process still running, returnswaiton its pid, and the loop goes quiet — then picks back up the instant CI finishes and judges the goal against the actual result.

`terminal(background=true, notify_on_complete=true)`
`wait`

## Behavior details​

### The judge​

After every turn, Hermes calls an auxiliary model with:

- The standing goal text
- The agent's most recent final response (last ~4 KB of text)
- A system prompt telling the judge to reply with strict JSON:{"done": <bool>, "reason": "<one-sentence rationale>"}

`{"done": <bool>, "reason": "<one-sentence rationale>"}`

The judge is deliberately conservative: it marks a goaldoneonly when the responseexplicitlyconfirms the goal is complete, when the final deliverable is clearly produced, or when the goal is unachievable/blocked (treated as DONE with a block reason so we don't burn budget on impossible tasks).

`done`

### Fail-open semantics​

If the judge errors (network blip, malformed response, unavailable aux client), Hermes treats the verdict ascontinue— a broken judge never wedges progress. Theturn budgetis the real backstop.

`continue`

### Turn budget​

Default is 20 continuation turns (goals.max_turnsinconfig.yaml). When the budget is hit, Hermes auto-pauses and tells you exactly how to proceed:

`goals.max_turns`
`config.yaml`

```
⏸ Goal paused — 20/20 turns used. Use /goal resume to keep going, or /goal clear to stop.
```

/goal resumeresets the counter to zero, so you can keep going in measured chunks.

`/goal resume`

### User messages always preempt​

Any real message you send while a goal is active takes priority over the continuation loop. On the CLI your message lands in_pending_inputahead of the queued continuation; on the gateway it goes through the adapter FIFO the same way. The judge runs again after your turn — so if your message happens to complete the goal, the judge will catch it and stop.

`_pending_input`

### Mid-run safety (gateway)​

While an agent is already running,/goal status,/goal pause,/goal clear,/goal wait, and/goal unwaitare safe to run — they only touch control-plane state and don't interrupt the current turn. Setting anewgoal mid-run (/goal <new text>) is rejected with a message telling you to/stopfirst, so the old continuation can't race the new one.

`/goal status`
`/goal pause`
`/goal clear`
`/goal wait`
`/goal unwait`
`/goal <new text>`
`/stop`

### Persistence​

Goal state lives inSessionDB.state_metakeyed bygoal:<session_id>. That means/resumepicks up right where you left off — set a goal, close your laptop, come back tomorrow,/resume, and the goal is still standing exactly as you left it (active, paused, or done).

`SessionDB.state_meta`
`goal:<session_id>`
`/resume`
`/resume`

### Prompt cache​

The continuation prompt is a plain user-role message appended to history. It doesnotmutate the system prompt, swap toolsets, or touch the conversation in any way that invalidates Hermes' prompt cache. Running a 20-turn goal costs the same cache-wise as 20 turns of normal conversation.

## Configuration​

Add to~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
goals:  # Max continuation turns before Hermes auto-pauses and asks you to  # /goal resume. Default 20. Lower this if you want tighter loops;  # raise it for long-running refactors.  max_turns: 20
```

### Choosing the judge model​

The judge uses thegoal_judgeauxiliary task. By default it resolves to your main model (seeAuxiliary Models). If you want to route the judge to a cheap fast model to keep costs down, add an override:

`goal_judge`

```
auxiliary:  goal_judge:    provider: openrouter    model: google/gemini-3-flash-preview
```

The judge call is small (~200 output tokens) and runs once per turn, so a cheap fast model is usually the right call.

## Example walkthrough​

```
You: /goal Create four files /tmp/note_{1..4}.txt, one per turn, each containing its number as text  ⊙ Goal set (20-turn budget): Create four files /tmp/note_{1..4}.txt, one per turn, each containing its number as textHermes: Creating /tmp/note_1.txt now.  💻 echo "1" > /tmp/note_1.txt   (0.1s)  I've created /tmp/note_1.txt with the content "1". I'll continue with the remaining files on the next turn as you specified.  ↻ Continuing toward goal (1/20): Only 1 of 4 files has been created; 3 files remain.Hermes: [Continuing toward your standing goal]  💻 echo "2" > /tmp/note_2.txt   (0.1s)  Created /tmp/note_2.txt. Two more to go.  ↻ Continuing toward goal (2/20): 2 of 4 files created; 2 remain.Hermes: [Continuing toward your standing goal]  💻 echo "3" > /tmp/note_3.txt   (0.1s)  Created /tmp/note_3.txt.  ↻ Continuing toward goal (3/20): 3 of 4 files created; 1 remains.Hermes: [Continuing toward your standing goal]  💻 echo "4" > /tmp/note_4.txt   (0.1s)  All four files have been created: /tmp/note_1.txt through /tmp/note_4.txt, each containing its number.  ✓ Goal achieved: All four files were created with the specified content, completing the goal.You: _
```

Four turns, one/goalinvocation, zero "keep going" prompts from you.

`/goal`

## When the judge gets it wrong​

No judge is perfect. Two failure modes to watch for:

False negative — judge says continue when the goal is actually done.The turn budget catches this. You'll see⏸ Goal pausedand can/goal clearor just send a new message.

`⏸ Goal paused`
`/goal clear`

False positive — judge says done when work remains.You'll see✓ Goal achievedbut you know better. Send a follow-up message to continue, or re-set the goal more precisely:/goal <more specific text>. The judge's system prompt is deliberately conservative to make false positives rarer than false negatives.

`✓ Goal achieved`
`/goal <more specific text>`

If you find a judge verdict unconvincing, the reason text in the↻ Continuing toward goalor✓ Goal achievedline tells you exactly what the judge saw. That's usually enough to diagnose whether the goal text was ambiguous or the model's response was.

`↻ Continuing toward goal`
`✓ Goal achieved`

## Attribution​

/goalis Hermes' take on theRalph looppattern. The user-facing design — keep a goal alive across turns, don't stop until it's achieved, with create/pause/resume/clear controls — was popularised and shipped inCodex CLI 0.128.0by Eric Traut on OpenAI's Codex team. Our implementation is independent (centralCommandDefregistry,SessionDB.state_metapersistence, auxiliary-client judge, adapter-FIFO continuation on the gateway side) but the idea is theirs. Credit where credit's due.

`/goal`
`CommandDef`
`SessionDB.state_meta`