- 
- Features
- Core
- Curator

# Curator

The curator is a background maintenance pass foragent-created skills. It tracks how often each skill is viewed, used, and patched, moves long-unused skills throughactive → stale → archivedstates, and periodically spawns a short auxiliary-model review that proposes consolidations or patches drift.

`active → stale → archived`

It exists so that skills created via theself-improvement loopdon't pile up forever. Every time the agent solves a novel problem and saves a skill, that skill lands in~/.hermes/skills/. Without maintenance, you end up with dozens of narrow near-duplicates that pollute the catalog and waste tokens.

`~/.hermes/skills/`

By default (prune_builtins: true) the curator can archiveunused bundled built-in skills(shipped with the repo) afterarchive_after_daysof non-use, alongside the agent-created skills it primarily manages. Hub-installed skills (fromagentskills.io) are always off-limits. Setcurator.prune_builtins: falseto restore the old agent-created-only behavior, where bundled skills are never touched. The curator alsonever auto-deletes— the worst outcome is archival into~/.hermes/skills/.archive/, which is recoverable.

`prune_builtins: true`
`archive_after_days`
`curator.prune_builtins: false`
`~/.hermes/skills/.archive/`

Tracksissue #7816.

## How it runs​

The curator is triggered by an inactivity check, not a cron daemon. On CLI session start, and on a recurring tick inside the gateway's cron-ticker thread, Hermes checks whether:

1. Enough time has passed since the last curator run (interval_hours, default7 days), and
2. The agent has been idle long enough (min_idle_hours, default2 hours).

`interval_hours`
`min_idle_hours`

If both are true, it spawns a background fork ofAIAgent— the same pattern used by the memory/skill self-improvement nudges. The fork runs in its own prompt cache and never touches the active conversation.

`AIAgent`

On a brand-new install (or the first time a pre-curator install ticks afterhermes update), the curatordoes not run immediately. The first observation seedslast_run_atto "now" and defers the first real pass by one fullinterval_hours. This gives you a full interval to review your skill library, pin anything important, or opt out entirely before the curator ever touches it.

`hermes update`
`last_run_at`
`interval_hours`

If you want to see what the curatorwoulddo before it runs for real, runhermes curator run --dry-run— it produces the same review report without mutating the library.

`hermes curator run --dry-run`

A run has two phases:

1. Automatic transitions(deterministic, no LLM). Skills unused forstale_after_days(30) becomestale; skills unused forarchive_after_days(90) are moved to~/.hermes/skills/.archive/. This is the always-on pruning behavior — it runs whenever the curator is enabled, with no aux-model cost.
2. LLM consolidation(single aux-model pass,max_iterations=8) —OFF by default. Whencurator.consolidate: true, the forked agent surveys the agent-created skills, can read any of them withskill_view, and decides per-skill whether to keep, patch (viaskill_manage), consolidate overlapping ones into class-level umbrellas, or archive via the terminal tool. Consolidation treats a skill as a full package: if a skill hasreferences/,templates/,scripts/,assets/, or relative links to those paths, the curator must either keep it standalone, re-home the needed support files and rewrite paths, or archive the entire package unchanged — not flatten onlySKILL.mdinto another skill'sreferences/file.

`stale_after_days`
`stale`
`archive_after_days`
`~/.hermes/skills/.archive/`
`max_iterations=8`
`curator.consolidate: true`
`skill_view`
`skill_manage`
`references/`
`templates/`
`scripts/`
`assets/`
`SKILL.md`
`references/`

By default the curator onlyprunes— the deterministic inactivity pass marks skills stale and archives long-unused ones. The opinionated LLMconsolidationpass (umbrella-building, merging overlapping skills) is off by default because it costs aux-model tokens on every run and makes broad structural changes to your library. Turn it on withcurator.consolidate: true, or run it once on demand withhermes curator run --consolidate.

`curator.consolidate: true`
`hermes curator run --consolidate`

Pinned skills are off-limits to both the curator's auto-transitions and the agent's ownskill_managetool. SeePinning a skillbelow.

`skill_manage`

## Configuration​

All settings live inconfig.yamlundercurator:(not.env— this isn't a secret). Defaults:

`config.yaml`
`curator:`
`.env`

```
curator:  enabled: true  interval_hours: 168          # 7 days  min_idle_hours: 2  stale_after_days: 30  archive_after_days: 90  consolidate: false           # LLM umbrella-building pass — opt-in (prune-only by default)  prune_builtins: true         # archive unused bundled built-in skills too (hub skills always exempt)
```

To disable entirely, setcurator.enabled: false. To keep the always-on pruning but opt into LLM consolidation, setcurator.consolidate: true.

`curator.enabled: false`
`curator.consolidate: true`

### Running the review on a cheaper aux model​

The curator's LLM review pass is a regular auxiliary task slot —auxiliary.curator— alongside Vision, Compression, Session Search, etc. "Auto" means "use my main chat model"; override the slot to pin a specific provider + model for the review pass instead.

`auxiliary.curator`

Easiest —hermes model:

`hermes model`

```
hermes model                   # → "Auxiliary models — side-task routing"                               # → pick "Curator" → pick provider → pick model
```

The same picker is available in the web dashboard under theModelstab.

Direct config.yaml (equivalent):

```
auxiliary:  curator:    provider: openrouter    model: google/gemini-3-flash-preview    timeout: 600               # generous — reviews can take several minutes
```

Leavingprovider: auto(the default) routes the review pass through whatever your main chat model is, matching the behavior of every other auxiliary task.

`provider: auto`

Earlier releases used a one-offcurator.auxiliary.{provider,model}block. That path still works but emits a deprecation log line — please migrate toauxiliary.curatorabove so the curator shares the same plumbing (hermes model, dashboard Models tab,base_url,api_key,timeout,extra_body) as every other aux task.

`curator.auxiliary.{provider,model}`
`auxiliary.curator`
`hermes model`
`base_url`
`api_key`
`timeout`
`extra_body`

## CLI​

```
hermes curator status         # last run, counts, pinned list, LRU top 5hermes curator run            # trigger a run now (blocks until done). Prune-only unless curator.consolidate: truehermes curator run --consolidate # force the LLM consolidation pass on for this run, overriding the config defaulthermes curator run --background  # fire-and-forget: start the run in a background threadhermes curator run --dry-run  # preview only — report without any mutationshermes curator backup         # take a manual snapshot of ~/.hermes/skills/hermes curator rollback       # restore from the newest snapshothermes curator rollback --list     # list available snapshotshermes curator rollback --id <ts>  # restore a specific snapshothermes curator rollback -y         # skip the confirmation prompthermes curator pause          # stop runs until resumedhermes curator resumehermes curator pin <skill>    # never auto-transition this skillhermes curator unpin <skill>hermes curator restore <skill>  # move an archived skill back to activehermes curator list-archived    # list skills currently in ~/.hermes/skills/.archive/hermes curator archive <skill>  # manually archive a single skill nowhermes curator prune [--days N] # bulk-archive agent-created skills idle >= N days (default 90)
```

## Backups and rollback​

Before every real curator pass, Hermes takes a tar.gz snapshot of~/.hermes/skills/at~/.hermes/skills/.curator_backups/<utc-iso>/skills.tar.gz. If a pass archives or consolidates something you didn't want touched, you can undo the whole run with one command:

`~/.hermes/skills/`
`~/.hermes/skills/.curator_backups/<utc-iso>/skills.tar.gz`

```
hermes curator rollback        # restore newest snapshot (with confirmation)hermes curator rollback -y     # skip the prompthermes curator rollback --list # see all snapshots with reason + size
```

The rollback itself is reversible: before replacing the skills tree, Hermes takes another snapshot taggedpre-rollback to <target-id>, so a mistaken rollback can be undone by rolling forward to that one with--id.

`pre-rollback to <target-id>`
`--id`

You can also take manual snapshots at any time withhermes curator backup --reason "before-refactor". The--reasonstring lands in the snapshot'smanifest.jsonand is shown in--list.

`hermes curator backup --reason "before-refactor"`
`--reason`
`manifest.json`
`--list`

Snapshots are pruned tocurator.backup.keep(default 5) to keep disk usage bounded:

`curator.backup.keep`

```
curator:  backup:    enabled: true    keep: 5
```

Setcurator.backup.enabled: falseto disable automatic snapshotting. The manualhermes curator backupcommand still works when backups are disabled only if you setenabled: truefirst — the flag gates both paths symmetrically so there's no way to accidentally skip the pre-run snapshot on mutating runs.

`curator.backup.enabled: false`
`hermes curator backup`
`enabled: true`

hermes curator statusalso lists the five least-recently-used skills — a quick way to see what's likely to become stale next.

`hermes curator status`

The same subcommands are available as the/curatorslash command inside a running session (CLI or gateway platforms).

`/curator`

## What "agent-created" means​

The curator only manages skills explicitly marked asagent-createdin~/.hermes/skills/.usage.json. A skill qualifies when ALL of the following
are true:

`~/.hermes/skills/.usage.json`
1. Its name isnotin~/.hermes/skills/.bundled_manifest(bundled skills shipped with the repo).
2. Its name isnotin~/.hermes/skills/.hub/lock.json(hub-installed skills).
3. Its.usage.jsonentry has"created_by": "agent"or"agent_created": true.

`~/.hermes/skills/.bundled_manifest`
`~/.hermes/skills/.hub/lock.json`
`.usage.json`
`"created_by": "agent"`
`"agent_created": true`

Currently, only thebackground self-improvement review forksets this marker
— when it creates a new umbrella skill during its periodic review pass (~every 10
agent turns). The background fork runs with a write origin of"background_review"(viatools/skill_provenance.py), which is the only path that triggers themark_agent_created()call inskill_manage.

`"background_review"`
`tools/skill_provenance.py`
`mark_agent_created()`
`skill_manage`

Skills the foreground agent creates viaskill_manage(action="create")during a
conversation arenotmarked as agent-created — they are considered
user-directed and the curator intentionally leaves them alone.

`skill_manage(action="create")`

If you manually created aSKILL.mdor pointed Hermes at an external skill
directory, that skill will have a.usage.jsonentry withcreated_by: null(or the field absent). The curator will not touch it. The same applies to
skills the foreground agent created at your request.

`SKILL.md`
`.usage.json`
`created_by: null`

To see which skills the curator actually manages, runhermes curator status.
If the agent-created count is 0, no skills are currently in the curator's
jurisdiction — the LLM review pass is skipped and the report will showModel: (not resolved) via (not resolved)withDuration: 0s.

`hermes curator status`
`Model: (not resolved) via (not resolved)`
`Duration: 0s`

Skills that ARE agent-created follow the full lifecycle:

- active→ (30d unused)stale→ (90d unused)archived
- Pinned skills bypass all auto-transitions
- Archives are recoverable viahermes curator restore <name>

`active`
`stale`
`archived`
`hermes curator restore <name>`

If you want to protect a specific skill from ever being touched — for example a
hand-authored skill you rely on — usehermes curator pin <name>. See the next
section.

`hermes curator pin <name>`

## Pinning a skill​

Pinning protects a skill from deletion — both the curator's automated archive passes and the agent'sskill_manage(action="delete")tool call. Once a skill is pinned:

`skill_manage(action="delete")`
- Thecuratorskips it during auto-transitions (active → stale → archived), and its LLM review pass is instructed to leave it alone.
- Theagent'sskill_managetoolrefusesdeleteon it, pointing the user athermes curator unpin <name>. Patches and edits still go through, so the agent can improve a pinned skill's content as pitfalls come up without a pin/unpin/re-pin dance.

`active → stale → archived`
`skill_manage`
`delete`
`hermes curator unpin <name>`

Pin and unpin with:

```
hermes curator pin <skill>hermes curator unpin <skill>
```

The flag is stored as"pinned": trueon the skill's entry in~/.hermes/skills/.usage.json, so it survives across sessions.

`"pinned": true`
`~/.hermes/skills/.usage.json`

Onlyagent-createdskills can be pinned —hermes curator pinrefuses on bundled and hub-installed skills with an explanatory message if you try. Hub-installed skills are never subject to curator mutation. Bundled built-in skills are only touched whencurator.prune_builtins: true(the default), and even then only archived afterarchive_after_daysof non-use — never patched, consolidated, or deleted. Setcurator.prune_builtins: falseto exempt bundled skills entirely.

`hermes curator pin`
`curator.prune_builtins: true`
`archive_after_days`
`curator.prune_builtins: false`

A small set ofprotected built-insis hardcoded as never-archivable and never-consolidatable, regardless ofcurator.prune_builtins, pin state, or LLM judgment. These back load-bearing UX — for example,planpowers the/planslash-command flow — so silently archiving one would turn its slash command into an "Unknown command" error with no signal to you. Protected built-ins are filtered out of the curator's candidate list entirely, so the consolidation pass never sees them.

`curator.prune_builtins`
`plan`
`/plan`

If you want a stronger guarantee than "no deletion" — for instance, freezing a skill's content entirely while the agent still reads it — edit~/.hermes/skills/<name>/SKILL.mddirectly with your editor. The pin guards tool-driven deletion, not your own filesystem access.

`~/.hermes/skills/<name>/SKILL.md`

## Usage telemetry​

The curator maintains a sidecar at~/.hermes/skills/.usage.jsonwith one entry per skill:

`~/.hermes/skills/.usage.json`

```
{  "my-skill": {    "use_count": 12,    "view_count": 34,    "last_used_at": "2026-04-24T18:12:03Z",    "last_viewed_at": "2026-04-23T09:44:17Z",    "patch_count": 3,    "last_patched_at": "2026-04-20T22:01:55Z",    "created_at": "2026-03-01T14:20:00Z",    "state": "active",    "pinned": false,    "archived_at": null  }}
```

Counters increment when:

- view_count: the agent callsskill_viewon the skill.
- use_count: the skill is loaded into a conversation's prompt.
- patch_count:skill_manage patch/edit/write_file/remove_fileruns on the skill.

`view_count`
`skill_view`
`use_count`
`patch_count`
`skill_manage patch/edit/write_file/remove_file`

Bundled and hub-installed skills are explicitly excluded from telemetry writes.

## Per-run reports​

Every curator run writes a timestamped directory under~/.hermes/logs/curator/:

`~/.hermes/logs/curator/`

```
~/.hermes/logs/curator/└── 20260429-111512/    ├── run.json      # machine-readable: full fidelity, stats, LLM output    └── REPORT.md     # human-readable summary
```

REPORT.mdis a quick way to see what a given run did — which skills transitioned, what the LLM reviewer said, which skills it patched. Good for auditing without having to grepagent.log.

`REPORT.md`
`agent.log`
`(not resolved)`

When the curator hasno agent-created skillsto review, the LLM review pass
is skipped entirely. The report header will showModel: (not resolved) via (not resolved)withDuration: 0s— this doesnotindicate a configuration error or model resolution failure. It simply means there
were no candidates, so no model was ever invoked. The auto-transition phase still
runs and reports its counts normally.

`Model: (not resolved) via (not resolved)`
`Duration: 0s`

### Rename map in the summary​

If a run consolidated multiple skills under an umbrella (or merged near-duplicates), the user-visible summary printed at the end of the run includes an explicit rename map showing everyold-name → new-namepair the curator applied. This is in addition to per-skill transition lines, so when a wave of renames lands you can spot them at a glance without diffing the JSON report. The hint also surfaces underhermes curator pinso you can pin the umbrella name immediately if you want to lock the new label in.

`old-name → new-name`
`hermes curator pin`

## Restoring an archived skill​

If the curator archived something you still want:

```
hermes curator restore <skill-name>
```

This moves the skill back from~/.hermes/skills/.archive/to the active tree and resets its state toactive. The restore refuses if a bundled or hub-installed skill has since been installed under the same name (would shadow upstream).

`~/.hermes/skills/.archive/`
`active`

## Disabling per environment​

The curator is on by default. To turn it off:

- For one profile only:edit~/.hermes/config.yaml(or the active profile's config) and setcurator.enabled: false.
- For just one run:hermes curator pause— the pause persists across sessions; useresumeto re-enable.

`~/.hermes/config.yaml`
`curator.enabled: false`
`hermes curator pause`
`resume`

The curator also refuses to run ifmin_idle_hourshasn't elapsed, so on an active dev machine it naturally only runs during quiet stretches.

`min_idle_hours`

## See also​

- Skills System— how skills work in general and the self-improvement loop that creates them
- Memory— a parallel background review that maintains long-term memory
- Bundled Skills Catalog
- Issue #7816— original proposal and design discussion