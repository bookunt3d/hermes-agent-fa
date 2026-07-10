---
layout: docs
title: "دستورات پروفایل"
permalink: /docs/reference/profile-commands/
---

- 
- Reference
- Command Reference
- Profile Commands Reference

# Profile Commands Reference

This page covers all commands related toHermes profiles. For general CLI commands, seeCLI Commands Reference.

## hermes profile​

`hermes profile`

```
hermes profile <subcommand>
```

Top-level command for managing profiles. Runninghermes profilewithout a subcommand shows help.

`hermes profile`
| Subcommand | Description |
| --- | --- |
| list | List all profiles. |
| use | Set the active (default) profile. |
| create | Create a new profile. |
| describe | Read or set a profile's description (used by the kanban orchestrator for routing). |
| delete | Delete a profile. |
| show | Show details about a profile. |
| alias | Regenerate the shell alias for a profile. |
| rename | Rename a profile. |
| export | Export a profile to a tar.gz archive. |
| import | Import a profile from a tar.gz archive. |
| install | Install a profile distribution from a git URL or local directory. SeeProfile Distributions. |
| update | Re-pull a distribution-managed profile and re-apply its bundle. |
| info | Show distribution metadata for a profile (origin URL, commit, last update). |

`list`
`use`
`create`
`describe`
`delete`
`show`
`alias`
`rename`
`export`
`import`
`install`
`update`
`info`

## hermes profile list​

`hermes profile list`

```
hermes profile list
```

Lists all profiles. The currently active profile is marked with*.

`*`

Example:

```
$ hermes profile list  default* work  dev  personal
```

No options.

## hermes profile use​

`hermes profile use`

```
hermes profile use <name>
```

Sets<name>as the active profile. All subsequenthermescommands (without-p) will use this profile.

`<name>`
`hermes`
`-p`
| Argument | Description |
| --- | --- |
| <name> | Profile name to activate. Usedefaultto return to the base profile. |

`<name>`
`default`

Example:

```
hermes profile use workhermes profile use default
```

## hermes profile create​

`hermes profile create`

```
hermes profile create <name> [options]
```

Creates a new profile.

| Argument / Option | Description |
| --- | --- |
| <name> | Name for the new profile. Must be a valid directory name (alphanumeric, hyphens, underscores). |
| --clone | Copyconfig.yaml,.env,SOUL.md, and skills from the current profile. |
| --clone-all | Copy everything (config, memories, skills, cron, plugins) from the current profile. Excludes per-profile history: sessions,state.db, backups, state-snapshots, checkpoints. |
| --clone-from <profile> | Clone config/skills/SOUL from a specific profile instead of the current one. Implies--cloneunless paired with--clone-all. |
| --no-alias | Skip wrapper script creation. |
| --description "<text>" | One- or two-sentence description of what this profile is good at. Used by the kanban orchestrator to route tasks based on role instead of profile name alone. Skip and add later viahermes profile describe. Persisted in<profile_dir>/profile.yaml. |
| --no-skills | Create anemptyprofile with zero bundled skills enabled. Writes a.no-bundled-skillsmarker into the profile so futurehermes updateruns won't re-seed the bundled set, and refuses to combine with--clone,--clone-from, or--clone-all(which would copy skills in anyway). Useful for narrow orchestrator profiles or sandbox profiles that should not inherit the full skill catalog. To toggle this on an already-created profile (including the default~/.hermes), usehermes skills opt-out/hermes skills opt-in. |

`<name>`
`--clone`
`config.yaml`
`.env`
`SOUL.md`
`--clone-all`
`state.db`
`--clone-from <profile>`
`--clone`
`--clone-all`
`--no-alias`
`--description "<text>"`
`hermes profile describe`
`<profile_dir>/profile.yaml`
`--no-skills`
`.no-bundled-skills`
`hermes update`
`--clone`
`--clone-from`
`--clone-all`
`~/.hermes`
`hermes skills opt-out`
`hermes skills opt-in`

Creating a profile doesnotmake that profile directory the default project/workspace directory for terminal commands. If you want a profile to start in a specific project, setterminal.cwdin that profile'sconfig.yaml.

`terminal.cwd`
`config.yaml`

Examples:

```
# Blank profile — needs full setuphermes profile create mybot# Clone config only from current profilehermes profile create work --clone# Clone everything from current profilehermes profile create backup --clone-all# Clone config from a specific profilehermes profile create work2 --clone-from work# Clone everything from a specific profilehermes profile create work2-backup --clone-from work --clone-all
```

## hermes profile describe​

`hermes profile describe`

```
hermes profile describe [<name>] [options]
```

Read or set a profile's description. The description is consumed by the kanban orchestrator to route tasks based on what each profile is good at, rather than guessing from the profile name alone. Persisted in<profile_dir>/profile.yamlso it survives reboots and is shared with the gateway.

`<profile_dir>/profile.yaml`

With no flags, prints the current description (or(no description set for '<name>')if empty).

`(no description set for '<name>')`
| Argument / Option | Description |
| --- | --- |
| <name> | Profile to describe. Required unless--all --autois used. |
| --text "<text>" | Set the description to this exact text (user-authored). Overwrites any existing description. |
| --auto | Auto-generate a 1-2 sentence description via the auxiliary LLM, based on the profile's installed skills, configured model, and name. Configure the model underauxiliary.profile_describerinconfig.yaml. Auto-generated descriptions are markeddescription_auto: trueso the dashboard can flag them for review. |
| --overwrite | With--auto, replace user-authored descriptions too (default: skip profiles whose description was set explicitly). |
| --all | With--auto, sweep every profile missing a description. |

`<name>`
`--all --auto`
`--text "<text>"`
`--auto`
`auxiliary.profile_describer`
`config.yaml`
`description_auto: true`
`--overwrite`
`--auto`
`--all`
`--auto`

Examples:

```
# Read the current descriptionhermes profile describe researcher# Set it explicitlyhermes profile describe researcher --text "Reads source code and writes findings."# Let the LLM generate onehermes profile describe researcher --auto# Fill in descriptions for every profile that doesn't have onehermes profile describe --all --auto
```

## hermes profile delete​

`hermes profile delete`

```
hermes profile delete <name> [options]
```

Deletes a profile and removes its shell alias.

| Argument / Option | Description |
| --- | --- |
| <name> | Profile to delete. |
| --yes,-y | Skip confirmation prompt. |

`<name>`
`--yes`
`-y`

Example:

```
hermes profile delete mybothermes profile delete mybot --yes
```

This permanently deletes the profile's entire directory including all config, memories, sessions, and skills. Cannot delete the currently active profile.

## hermes profile show​

`hermes profile show`

```
hermes profile show <name>
```

Displays details about a profile including its home directory, configured model, gateway status, skills count, and configuration file status.

This shows the profile's Hermes home directory, not the terminal working directory. Terminal commands start fromterminal.cwd(or the launch directory on the local backend whencwd: ".").

`terminal.cwd`
`cwd: "."`
| Argument | Description |
| --- | --- |
| <name> | Profile to inspect. |

`<name>`

Example:

```
$ hermes profile show workProfile: workPath:    ~/.hermes/profiles/workModel:   anthropic/claude-sonnet-4 (anthropic)Gateway: stoppedSkills:  12.env:    existsSOUL.md: existsAlias:   ~/.local/bin/work
```

## hermes profile alias​

`hermes profile alias`

```
hermes profile alias <name> [options]
```

Regenerates the shell alias script at~/.local/bin/<name>. Useful if the alias was accidentally deleted or if you need to update it after moving your Hermes installation.

`~/.local/bin/<name>`
| Argument / Option | Description |
| --- | --- |
| <name> | Profile to create/update the alias for. |
| --remove | Remove the wrapper script instead of creating it. |
| --name <alias> | Custom alias name (default: profile name). |

`<name>`
`--remove`
`--name <alias>`

Example:

```
hermes profile alias work# Creates/updates ~/.local/bin/workhermes profile alias work --name mywork# Creates ~/.local/bin/myworkhermes profile alias work --remove# Removes the wrapper script
```

## hermes profile rename​

`hermes profile rename`

```
hermes profile rename <old-name> <new-name>
```

Renames a profile. Updates the directory and shell alias.

| Argument | Description |
| --- | --- |
| <old-name> | Current profile name. |
| <new-name> | New profile name. |

`<old-name>`
`<new-name>`

Example:

```
hermes profile rename mybot assistant# ~/.hermes/profiles/mybot → ~/.hermes/profiles/assistant# ~/.local/bin/mybot → ~/.local/bin/assistant
```

## hermes profile export​

`hermes profile export`

```
hermes profile export <name> [options]
```

Exports a profile as a compressed tar.gz archive.

| Argument / Option | Description |
| --- | --- |
| <name> | Profile to export. |
| -o,--output <path> | Output file path (default:<name>.tar.gz). |

`<name>`
`-o`
`--output <path>`
`<name>.tar.gz`

Example:

```
hermes profile export work# Creates work.tar.gz in the current directoryhermes profile export work -o ./work-2026-03-29.tar.gz
```

## hermes profile import​

`hermes profile import`

```
hermes profile import <archive> [options]
```

Imports a profile from a tar.gz archive.

| Argument / Option | Description |
| --- | --- |
| <archive> | Path to the tar.gz archive to import. |
| --name <name> | Name for the imported profile (default: inferred from archive). |

`<archive>`
`--name <name>`

Example:

```
hermes profile import ./work-2026-03-29.tar.gz# Infers profile name from the archivehermes profile import ./work-2026-03-29.tar.gz --name work-restored
```

## Distribution commands​

New to distributions?Start with theProfile Distributions user guide— it covers the why, when, and how with full examples. The sections below are a dry CLI reference for when you know what you want.

Distributions turn a profile into a shareable, versioned artifact published
as agit repository. A recipient installs the distribution with a single
command and can update it in place later without touching their local
memories, sessions, or credentials.

auth.jsonand.envare never part of a distribution — they stay on the
installing user's machine.

`auth.json`
`.env`

The recipient's user data (memories, sessions, auth, their own edits to.env) is always preserved across the initial install and subsequent
updates.

`.env`

hermes profile export/importare still the right commands forlocal backup and restoreof a profile on your own machine. Distribution
(install/update/info) is a separate concept: ship a profile via
git so someone else can install it.

`hermes profile export`
`import`
`install`
`update`
`info`

### hermes profile install​

`hermes profile install`

```
hermes profile install <source> [--name <name>] [--alias] [--force] [--yes]
```

Installs a profile distribution from a git URL or a local directory.

| Option | Description |
| --- | --- |
| <source> | Git URL (github.com/user/repo,https://...,git@...,ssh://,git://) or a local directory containingdistribution.yamlat its root. |
| --name NAME | Override the profile name from the manifest. |
| --alias | Also create a shell wrapper (e.g.telemetry→hermes -p telemetry). |
| --force | Overwrite an existing profile of the same name. User data is still preserved. |
| -y,--yes | Skip the manifest-preview confirmation prompt. |

`<source>`
`github.com/user/repo`
`https://...`
`git@...`
`ssh://`
`git://`
`distribution.yaml`
`--name NAME`
`--alias`
`telemetry`
`hermes -p telemetry`
`--force`
`-y`
`--yes`

The installer shows the manifest, lists required env vars, and warns about
cron jobs before asking for confirmation. Required env vars go into a.env.EXAMPLEfile you copy to.envand fill in.

`.env.EXAMPLE`
`.env`

Examples:

```
# Install from a GitHub repo (shorthand)hermes profile install github.com/kyle/telemetry-distribution --alias# Install from a full HTTPS git URLhermes profile install https://github.com/kyle/telemetry-distribution.git# Install from SSHhermes profile install git@github.com:kyle/telemetry-distribution.git# Install from a local directory during developmenthermes profile install ./telemetry/
```

### hermes profile update​

`hermes profile update`

```
hermes profile update <name> [--force-config] [--yes]
```

Re-clones the distribution from its recorded source and applies updates.
Distribution-owned files (SOUL.md, skills/, cron/, mcp.json) are
overwritten; user data (memories, sessions, auth, .env) is never touched.

config.yamlis preserved by default to keep your local overrides.
Pass--force-configto reset it to the distribution's shipped config.

`config.yaml`
`--force-config`

### hermes profile info​

`hermes profile info`

```
hermes profile info <name>
```

Prints the profile's distribution manifest — name, version, required
Hermes version, author, env var requirements, the source URL/path, and
theInstalled:timestamp recorded when the distribution was lastinstall-ed orupdate-d. Useful for checking what a shared profile
needs before installing it, and for spotting "this profile was installed
6 months ago and hasn't been updated."

`Installed:`
`install`
`update`

hermes profile listalso shows the distribution name and version in aDistributioncolumn, andhermes profile show <name>/delete <name>surface the source URL so you can tell at a glance which profiles came
from a git repo vs. were created locally.

`hermes profile list`
`Distribution`
`hermes profile show <name>`
`delete <name>`

### Private distributions​

A private git repository works as a distribution source with no extra
configuration — the install shells out to your normalgitbinary, so
whatever authentication your shell is already set up for (SSH key,git credentialhelper, GitHub CLI's stored HTTPS credentials) applies
transparently.

`git`
`git credential`

```
# Uses your SSH key, the same as any other `git clone`hermes profile install git@github.com:your-org/internal-assistant.git# Uses your git credential helperhermes profile install https://github.com/your-org/internal-assistant.git
```

If a clone prompts for credentials interactively in your terminal during
install, that prompt flows through. Set up your auth the way you'd
normally usegit cloneagainst the same repo first, then install.

`git clone`

### Distribution manifest (distribution.yaml)​

`distribution.yaml`

Every distribution has adistribution.yamlat the root of its repository:

`distribution.yaml`

```
name: telemetryversion: 0.1.0description: "Compliance monitoring harness"hermes_requires: ">=0.12.0"author: "Your Name"license: "MIT"env_requires:  - name: OPENAI_API_KEY    description: "OpenAI API key"    required: true  - name: GRAPHITI_MCP_URL    description: "Memory graph URL"    required: false    default: "http://127.0.0.1:8000/sse"distribution_owned:   # optional; defaults to SOUL.md, config.yaml,                      #   mcp.json, skills/, cron/, distribution.yaml  - SOUL.md  - skills/compliance/  - cron/
```

hermes_requiressupports>=,<=,==,!=,>,<, or a bare
version (treated as>=). Install fails with a clear error if the current
Hermes version doesn't satisfy the spec.

`hermes_requires`
`>=`
`<=`
`==`
`!=`
`>`
`<`
`>=`

distribution_ownedis optional. If set, only those paths are replaced on
update; anything else in the profile stays user-owned. If omitted, the
defaults above apply.

`distribution_owned`

### Publishing a distribution​

Authoring a distribution is just a git push:

1. In your profile directory, createdistribution.yamlwith at leastnameandversion.
2. Initialize a git repo (or use an existing one) and push to GitHub /
GitLab / any host Hermes can clone from.
3. Tell recipients to runhermes profile install <your-repo-url>.

`distribution.yaml`
`name`
`version`
`hermes profile install <your-repo-url>`

Use git tags for versioned releases — recipients who cloneHEADget your
latest state, and you can always bumpversion:in the manifest.

`HEAD`
`version:`

## hermes -p/hermes --profile​

`hermes -p`
`hermes --profile`

```
hermes -p <name> <command> [options]hermes --profile <name> <command> [options]
```

Global flag to run any Hermes command under a specific profile without changing the sticky default. This overrides the active profile for the duration of the command.

| Option | Description |
| --- | --- |
| -p <name>,--profile <name> | Profile to use for this command. |

`-p <name>`
`--profile <name>`

Examples:

```
hermes -p work chat -q "Check the server status"hermes --profile dev gateway starthermes -p personal skills listhermes -p work config edit
```

## hermes completion​

`hermes completion`

```
hermes completion <shell>
```

Generates shell completion scripts. Includes completions for profile names and profile subcommands.

| Argument | Description |
| --- | --- |
| <shell> | Shell to generate completions for:bash,zsh, orfish. |

`<shell>`
`bash`
`zsh`
`fish`

Examples:

```
# Install completionshermes completion bash >> ~/.bashrchermes completion zsh >> ~/.zshrchermes completion fish > ~/.config/fish/completions/hermes.fish# Reload shellsource ~/.bashrc
```

After installation, tab completion works for:

- hermes profile <TAB>— subcommands (list, use, create, etc.)
- hermes profile use <TAB>— profile names
- hermes -p <TAB>— profile names

`hermes profile <TAB>`
`hermes profile use <TAB>`
`hermes -p <TAB>`

## See also​

- Profiles User Guide
- CLI Commands Reference
- FAQ — Profiles section