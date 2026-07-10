---
layout: docs
title: "به‌روزرسانی و حذف"
permalink: /getting-started/updating/
---

- 
- Getting Started
- Updating & Uninstalling

# Updating & Uninstalling

## Updating​

Update to the latest version with a single command:

```
hermes update
```

This pulls the latest code frommain, updates dependencies, and prompts you to configure any new options that were added since your last update.

`main`

hermes updateautomatically detects new configuration options and prompts you to add them. If you skipped that prompt, you can manually runhermes config checkto see missing options, thenhermes config migrateto interactively add them.

`hermes update`
`hermes config check`
`hermes config migrate`

### What happens during an update​

When you runhermes update, the following steps occur:

`hermes update`
1. Pairing-data snapshot— a lightweight pre-update state snapshot is saved (covers~/.hermes/pairing/, Feishu comment rules, and other state files that get modified at runtime). Recoverable via the snapshot restore flow described underSnapshots and rollback, or by extracting the most recent quick-snapshot zip Hermes wrote next to your~/.hermes/directory.
2. Git pull— pulls the latest code from themainbranch and updates submodules
3. Post-pull syntax validation + auto-rollback— after the pull, Hermes compiles the eight critical files everyhermesinvocation imports at startup. If any fails to parse (e.g. an orphan merge-conflict marker, an accidentally truncated file), Hermes runsgit reset --hard <pre-pull-sha>to roll the install back so your shell stays bootable. Re-runhermes updateonce the upstream fix lands.
4. Dependency install— runsuv pip install -e ".[all]"to pick up new or changed dependencies
5. Config migration— detects new config options added since your version and prompts you to set them
6. Gateway auto-restart— running gateways are refreshed after the update completes so the new code takes effect immediately. Service-managed gateways (systemd on Linux, launchd on macOS) are restarted through the service manager. Manual gateways are relaunched automatically when Hermes can map the running PID back to a profile.

`~/.hermes/pairing/`
[Snapshots and rollback](/docs/user-guide/checkpoints-and-rollback)
`~/.hermes/`
`main`
`hermes`
`git reset --hard <pre-pull-sha>`
`hermes update`
`uv pip install -e ".[all]"`

### Updating against a non-default branch:--branch​

`--branch`

By defaulthermes updatetracksorigin/main. Pass--branch <name>to update against a different branch — useful for QA channels, feature branches, or release-candidate testing:

`hermes update`
`origin/main`
`--branch <name>`

```
hermes update --branch release-candidatehermes update --check --branch experimental   # preview behindness only
```

If your local checkout is on a different branch, Hermes auto-stashes any uncommitted work, switches HEAD to the target branch, and then pulls. Branches that don't exist locally are auto-tracked fromorigin/<name>(git checkout -B <name> origin/<name>). Branches that don't exist anywhere fail cleanly — your stashed changes are restored before exit so you're never stranded in a weird state. Themain-only fork-upstream sync logic is automatically skipped on non-mainbranches.

`origin/<name>`
`git checkout -B <name> origin/<name>`
`main`
`main`

### Local changes on non-interactive updates​

When you runhermes updatein a terminal, Hermes stashes any uncommitted source-tree changes, pulls, thenaskswhether to restore them — exactly as it always has. Nothing changes for interactive updates.

`hermes update`

When the update runswithout a terminal— from the desktop/chat app's "Update" button or a gateway-triggered update — there's no prompt to answer. Theupdates.non_interactive_local_changessetting decides what happens to your stashed changes:

`updates.non_interactive_local_changes`

```
# ~/.hermes/config.yamlupdates:  non_interactive_local_changes: stash   # default: keep + auto-restore  # non_interactive_local_changes: discard  # throw local source edits away
```

- stash(default) — auto-stash, pull, then auto-restore your changes on top of the updated code. Nothing is lost; if a restore hits conflicts they're preserved in a git stash for manual recovery.
- discard— auto-stash and drop the stash after the pull, so the update always lands on a clean tree. Use this only on machines where you never intend to keep local edits to the Hermes source. It stash-drops (notgit reset --hard+git clean -fd), so ignored paths likenode_modules,venv, and build outputs are never touched.

`stash`
`discard`
`git reset --hard`
`git clean -fd`
`node_modules`
`venv`

In the desktop app this isSettings → Advanced → In-App Update Local Changes.

### Preview-only:hermes update --check​

`hermes update --check`

Want to know if an update is available before pulling? Runhermes update --check— it fetches and compares commits againstorigin/main. No files are modified, no gateway is restarted. Useful in scripts and cron jobs that gate on "is there an update".

`hermes update --check`
`origin/main`

### Full pre-update backup:--backup​

`--backup`

For high-value profiles (production gateways, shared team installs) you can opt into a full pre-pull backup ofHERMES_HOME(config, auth, sessions, skills, pairing):

`HERMES_HOME`

```
hermes update --backup
```

Or make it the default for every run:

```
# ~/.hermes/config.yamlupdates:  pre_update_backup: true
```

--backupwas the always-on behavior in earlier builds, but it was adding minutes to every update on large homes, so it's now opt-in. The lightweight pairing-data snapshot above still runs unconditionally.

`--backup`

### Windows: anotherhermes.exeis running​

`hermes.exe`

On Windows,hermes updatewill refuse to run if it detects anotherhermes.exeprocess holding the venv's entry-point executable open — most commonly the Hermes Desktop app's spawned backend, an openhermesREPL in another terminal, or a running gateway:

`hermes update`
`hermes.exe`
`hermes`

```
$ hermes update✗ Another hermes.exe is running:    PID 12345  hermes.exe  Updating now would fail to overwrite ...\venv\Scripts\hermes.exe because  Windows blocks REPLACE on a running executable.  Close Hermes Desktop, exit any open `hermes` REPLs, and  stop the gateway (`hermes gateway stop`) before retrying.  Override with `hermes update --force` if you've already  confirmed those processes will not write to the venv.
```

Close the listed processes and re-run. If you're sure the concurrent process won't interfere (rare — usually only useful when an antivirus shim is mis-attributed), pass--forceto skip the check. In that case the updater will still retry the.exerename with exponential backoff and, on stubborn locks, schedule the replacement for next reboot viaMoveFileEx(MOVEFILE_DELAY_UNTIL_REBOOT)so the update can complete.

`--force`
`.exe`
`MoveFileEx(MOVEFILE_DELAY_UNTIL_REBOOT)`

A second, separate guard refuses to touch the venv while any process is running from its Python interpreter (the Desktop app's backend, a gateway, a Python REPL). Those processes keep native extension files (.pyd) locked, and a dependency sync that dies partway on an access-denied error strands the install between versions. This guard isnotbypassed by--force; if you're certain the detected holders are false positives, use the explicithermes update --force-venv.

`.pyd`
`--force`
`hermes update --force-venv`

Expected output looks like:

```
$ hermes updateUpdating Hermes Agent...📥 Pulling latest code...Already up to date.  (or: Updating abc1234..def5678)📦 Updating dependencies...✅ Dependencies updated🔍 Checking for new config options...✅ Config is up to date  (or: Found 2 new options — running migration...)🔄 Restarting gateways...✅ Gateway restarted✅ Hermes Agent updated successfully!
```

### Recommended Post-Update Validation​

hermes updatehandles the main update path, but a quick validation confirms everything landed cleanly:

`hermes update`
1. git status --short— if the tree is unexpectedly dirty, inspect before continuing
2. hermes doctor— checks config, dependencies, and service health
3. hermes --version— confirm the version bumped as expected
4. If you use the gateway:hermes gateway status
5. Ifdoctorreports npm audit issues: runnpm audit fixin the flagged directory

`git status --short`
`hermes doctor`
`hermes --version`
`hermes gateway status`
`doctor`
`npm audit fix`

Ifgit status --shortshows unexpected changes afterhermes update, stop and inspect them before continuing. This usually means local modifications were reapplied on top of the updated code, or a dependency step refreshed lockfiles.

`git status --short`
`hermes update`

### If your terminal disconnects mid-update​

hermes updateprotects itself against accidental terminal loss:

`hermes update`
- The update ignoresSIGHUP, so closing your SSH session or terminal window no longer kills it mid-install.pipandgitchild processes inherit this protection, so the Python environment cannot be left half-installed by a dropped connection.
- All output is mirrored to~/.hermes/logs/update.logwhile the update runs. If your terminal disappears, reconnect and inspect the log to see whether the update finished and whether the gateway restart succeeded:

`SIGHUP`
`pip`
`git`
`~/.hermes/logs/update.log`

```
tail -f ~/.hermes/logs/update.log
```

- Ctrl-C(SIGINT) and system shutdown (SIGTERM) are still honored — those are deliberate cancellations, not accidents.

`Ctrl-C`

You no longer need to wraphermes updateinscreenortmuxto survive a terminal drop.

`hermes update`
`screen`
`tmux`

### Checking your current version​

```
hermes version
```

Compare against the latest release at theGitHub releases page.

[GitHub releases page](https://github.com/NousResearch/hermes-agent/releases)

### Updating from Messaging Platforms​

You can also update directly from Telegram, Discord, Slack, WhatsApp, or Teams by sending:

```
/update
```

This pulls the latest code, updates dependencies, and restarts running gateways. The bot will briefly go offline during the restart (typically 5–15 seconds) and then resume.

### Manual Update​

If you installed manually (not via the quick installer):

```
cd /path/to/hermes-agent# Activate the venv you created during install (outside the source tree)export VIRTUAL_ENV="$HOME/.hermes/venvs/hermes-dev"export PATH="$VIRTUAL_ENV/bin:$PATH"# Pull latest codegit pull origin main# Reinstall (picks up new dependencies)uv pip install -e ".[all]"# Check for new config optionshermes config checkhermes config migrate   # Interactively add any missing options
```

### Rollback instructions​

If an update introduces a problem, you can roll back to a previous version:

```
cd /path/to/hermes-agent# List recent versionsgit log --oneline -10# Roll back to a specific commitgit checkout <commit-hash>uv pip install -e ".[all]"# Restart the gateway if runninghermes gateway restart
```

To roll back to a specific release tag (substitute your previous tag — e.g. a recent release likev2026.5.16, or any earlier tag fromgit tag --sort=-version:refname):

`v2026.5.16`
`git tag --sort=-version:refname`

```
git checkout vX.Y.Zuv pip install -e ".[all]"
```

Rolling back may cause config incompatibilities if new options were added. Runhermes config checkafter rolling back and remove any unrecognized options fromconfig.yamlif you encounter errors.

`hermes config check`
`config.yaml`

### Note for Nix users​

Nix is no longer an explicitly supported install path (best-effort only) — seeNix Setup. If you installed via Nix flake, updates are managed through the Nix package manager:

[Nix Setup](/docs/getting-started/nix-setup)

```
# Update the flake inputnix flake update hermes-agent# Or rebuild with the latestnix profile upgrade hermes-agent
```

Nix installations are immutable — rollback is handled by Nix's generation system:

```
nix profile rollback
```

SeeNix Setupfor more details.

[Nix Setup](/docs/getting-started/nix-setup)

## Uninstalling​

```
hermes uninstall
```

The uninstaller gives you the option to keep your configuration files (~/.hermes/) for a future reinstall.

`~/.hermes/`

### Manual Uninstall​

```
rm -f ~/.local/bin/hermesrm -rf /path/to/hermes-agentrm -rf ~/.hermes            # Optional — keep if you plan to reinstall
```

If you installed the gateway as a system service, stop and disable it first:

```
hermes gateway stop# Linux: systemctl --user disable hermes-gateway# macOS: launchctl remove ai.hermes.gateway
```

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/updating.md)