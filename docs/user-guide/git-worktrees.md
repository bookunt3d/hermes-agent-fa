---
layout: docs
title: "Git Worktrees"
permalink: /user-guide/git-worktrees/
---

- 
- Using Hermes
- Git Worktrees

# Git Worktrees

Hermes Agent is often used on large, long‑lived repositories. When you want to:

- Runmultiple agents in parallelon the same project, or
- Keep experimental refactors isolated from your main branch,

Gitworktreesare the safest way to give each agent its own checkout without duplicating the entire repository.

This page shows how to combine worktrees with Hermes so each session has a clean, isolated working directory.

## Why Use Worktrees with Hermes?​

Hermes treats thecurrent working directoryas the project root:

- CLI: the directory where you runhermesorhermes chat
- Messaging gateways: the directory set byterminal.cwdin~/.hermes/config.yaml

`hermes`
`hermes chat`
`terminal.cwd`
`~/.hermes/config.yaml`

If you run multiple agents in thesame checkout, their changes can interfere with each other:

- One agent may delete or rewrite files the other is using.
- It becomes harder to understand which changes belong to which experiment.

With worktrees, each agent gets:

- Itsown branch and working directory
- Itsown Checkpoint Manager historyfor/rollback

`/rollback`

See also:Checkpoints and /rollback.

[Checkpoints and /rollback](/docs/user-guide/checkpoints-and-rollback)

## Quick Start: Creating a Worktree​

From your main repository (containing.git/), create a new worktree for a feature branch:

`.git/`

```
# From the main repo rootcd /path/to/your/repo# Create a new branch and worktree in ../repo-featuregit worktree add ../repo-feature feature/hermes-experiment
```

This creates:

- A new directory:../repo-feature
- A new branch:feature/hermes-experimentchecked out in that directory

`../repo-feature`
`feature/hermes-experiment`

Now you cancdinto the new worktree and run Hermes there:

`cd`

```
cd ../repo-feature# Start Hermes in the worktreehermes
```

Hermes will:

- See../repo-featureas the project root.
- Use that directory for context files, code edits, and tools.
- Use aseparate checkpoint historyfor/rollbackscoped to this worktree.

`../repo-feature`
`/rollback`

## Running Multiple Agents in Parallel​

You can create multiple worktrees, each with its own branch:

```
cd /path/to/your/repogit worktree add ../repo-experiment-a feature/hermes-agit worktree add ../repo-experiment-b feature/hermes-b
```

In separate terminals:

```
# Terminal 1cd ../repo-experiment-ahermes# Terminal 2cd ../repo-experiment-bhermes
```

Each Hermes process:

- Works on its own branch (feature/hermes-avsfeature/hermes-b).
- Writes checkpoints under a different shadow repo hash (derived from the worktree path).
- Can use/rollbackindependently without affecting the other.

`feature/hermes-a`
`feature/hermes-b`
`/rollback`

This is especially useful when:

- Running batch refactors.
- Trying different approaches to the same task.
- Pairing CLI + gateway sessions against the same upstream repo.

## Cleaning Up Worktrees Safely​

When you are done with an experiment:

1. Decide whether to keep or discard the work.
2. If you want to keep it:Merge the branch into your main branch as usual.
3. Remove the worktree:

- Merge the branch into your main branch as usual.

```
cd /path/to/your/repo# Remove the worktree directory and its referencegit worktree remove ../repo-feature
```

Notes:

- git worktree removewill refuse to remove a worktree with uncommitted changes unless you force it.
- Removing a worktree doesnotautomatically delete the branch; you can delete or keep the branch using normalgit branchcommands.
- Hermes checkpoint data under~/.hermes/checkpoints/is not automatically pruned when you remove a worktree, but it is usually very small.

`git worktree remove`
`git branch`
`~/.hermes/checkpoints/`

## Best Practices​

- One worktree per Hermes experimentCreate a dedicated branch/worktree for each substantial change.This keeps diffs focused and PRs small and reviewable.
- Name branches after the experimente.g.feature/hermes-checkpoints-docs,feature/hermes-refactor-tests.
- Commit frequentlyUse git commits for high‑level milestones.Usecheckpoints and /rollbackas a safety net for tool‑driven edits in between.
- Avoid running Hermes from the bare repo root when using worktreesPrefer the worktree directories instead, so each agent has a clear scope.

- Create a dedicated branch/worktree for each substantial change.
- This keeps diffs focused and PRs small and reviewable.

- e.g.feature/hermes-checkpoints-docs,feature/hermes-refactor-tests.

`feature/hermes-checkpoints-docs`
`feature/hermes-refactor-tests`
- Use git commits for high‑level milestones.
- Usecheckpoints and /rollbackas a safety net for tool‑driven edits in between.

[checkpoints and /rollback](/docs/user-guide/checkpoints-and-rollback)
- Prefer the worktree directories instead, so each agent has a clear scope.

## Usinghermes -w(Automatic Worktree Mode)​

`hermes -w`

Hermes has a built‑in-wflag thatautomatically creates a disposable git worktreewith its own branch. You don't need to set up worktrees manually — justcdinto your repo and run:

`-w`
`cd`

```
cd /path/to/your/repohermes -w
```

Hermes will:

- Create a temporary worktree under.worktrees/inside your repo.
- Check out an isolated branch (e.g.hermes/hermes-<hash>).
- Run the full CLI session inside that worktree.

`.worktrees/`
`hermes/hermes-<hash>`

This is the easiest way to get worktree isolation. You can also combine it with a single query:

```
hermes -w -z "Fix issue #123"
```

For parallel agents, open multiple terminals and runhermes -win each — every invocation gets its own worktree and branch automatically.

`hermes -w`

## Putting It All Together​

- Usegit worktreesto give each Hermes session its own clean checkout.
- Usebranchesto capture the high‑level history of your experiments.
- Usecheckpoints +/rollbackto recover from mistakes inside each worktree.

`/rollback`

This combination gives you:

- Strong guarantees that different agents and experiments do not step on each other.
- Fast iteration cycles with easy recovery from bad edits.
- Clean, reviewable pull requests.

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/git-worktrees.md)