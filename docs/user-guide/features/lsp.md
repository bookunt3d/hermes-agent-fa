---
layout: docs
title: "Features_Lsp"
permalink: /docs/user-guide/features_lsp/
---

- 
- Features
- Core
- LSP — Semantic Diagnostics

# Language Server Protocol (LSP)

Hermes runs full language servers — pyright, gopls, rust-analyzer,
typescript-language-server, clangd, and ~20 more — as background
subprocesses and feeds their semantic diagnostics into the post-write
lint check used bywrite_fileandpatch. When the agent edits a
file, it sees exactly the errors that edit introduced — not just
syntax errors, buttype errors, undefined names, missing imports,
and project-wide semantic issuesthe language server detects.

`write_file`
`patch`

This is the same architecture top-tier coding agents use. Hermes
ships it self-contained: no editor host required, no plugins to
install, no separate daemon to manage.

## When LSP runs​

LSP is gated ongit workspace detection. When the agent's working
directory (or the file being edited) is inside a git repository, LSP
runs against that workspace. When neither is in a git repo, LSP
stays dormant — useful for messaging gateways where the cwd is the
user's home directory and there's no project to diagnose.

The check is layered: in-process syntax check first (microseconds),
then LSP diagnostics second when syntax is clean. A flaky or missing
language server can never break a write — every LSP failure path
falls back silently to the syntax-only result.

Concretely, on every successfulwrite_fileorpatch:

`write_file`
`patch`
1. Hermes captures a baseline of current diagnostics for the file.
2. Performs the write.
3. Re-queries the language server, filters out diagnostics that were
already in the baseline, and surfaces only the new ones.

The agent sees output like:

```
{  "bytes_written": 42,  "dirs_created": false,  "lint": {"status": "ok", "output": ""},  "lsp_diagnostics": "LSP diagnostics introduced by this edit:\n<diagnostics file=\"/path/to/foo.py\">\nERROR [42:5] Cannot find name 'foo' [reportUndefinedVariable] (Pyright)\nERROR [50:1] Argument of type \"str\" is not assignable to \"int\" [reportArgumentType] (Pyright)\n</diagnostics>"}
```

Thelintfield carries the syntax-check result (microsecond
in-process parse viaast.parse,json.loads, etc.); thelsp_diagnosticsfield carries the semantic diagnostics from the
real language server. Two channels, independent signals — the
agent sees a syntax-clean file with semantic problems aslint: okplus a populatedlsp_diagnostics.

`lint`
`ast.parse`
`json.loads`
`lsp_diagnostics`
`lint: ok`
`lsp_diagnostics`

## Supported languages​

| Language | Server | Auto-install |
| --- | --- | --- |
| Python | pyright-langserver | npm |
| TypeScript / JavaScript / JSX / TSX | typescript-language-server | npm |
| Vue | @vue/language-server | npm |
| Svelte | svelte-language-server | npm |
| Astro | @astrojs/language-server | npm |
| Go | gopls | go install |
| Rust | rust-analyzer | manual (rustup) |
| C / C++ | clangd | manual (LLVM) |
| Bash / Zsh | bash-language-server | npm |
| YAML | yaml-language-server | npm |
| Lua | lua-language-server | manual (GitHub releases) |
| PHP | intelephense | npm |
| OCaml | ocaml-lsp | manual (opam) |
| Dockerfile | dockerfile-language-server-nodejs | npm |
| Terraform | terraform-ls | manual |
| Dart | dart language-server | manual (dart sdk) |
| Haskell | haskell-language-server | manual (ghcup) |
| Julia | julia+ LanguageServer.jl | manual |
| Clojure | clojure-lsp | manual |
| Nix | nixd | manual |
| Zig | zls | manual |
| Gleam | gleam lsp | manual (gleam install) |
| Elixir | elixir-ls | manual |
| Prisma | prisma language-server | manual |
| Kotlin | kotlin-language-server | manual |
| Java | jdtls | manual |
| PowerShell | PowerShellEditorServices(pwshhost) | manual (release zip) |

`pyright-langserver`
`typescript-language-server`
`@vue/language-server`
`svelte-language-server`
`@astrojs/language-server`
`gopls`
`go install`
`rust-analyzer`
`clangd`
`bash-language-server`
`yaml-language-server`
`lua-language-server`
`intelephense`
`ocaml-lsp`
`dockerfile-language-server-nodejs`
`terraform-ls`
`dart language-server`
`haskell-language-server`
`julia`
`clojure-lsp`
`nixd`
`zls`
`gleam lsp`
`elixir-ls`
`prisma language-server`
`kotlin-language-server`
`jdtls`
`PowerShellEditorServices`
`pwsh`

For "manual" entries, install the server through whatever toolchain
manager makes sense for that language (rustup, ghcup, opam, brew,
…). Hermes auto-detects the binary on PATH or in<HERMES_HOME>/lsp/bin/.

`<HERMES_HOME>/lsp/bin/`

### PowerShell​

PowerShellEditorServices isn't a single binary — it's a PowerShell
module bundle launched by apwsh(PowerShell 7+) orpowershellhost. Setup:

`pwsh`
`powershell`
1. InstallPowerShellsopwsh(or Windowspowershell) is on PATH.
2. Download the latest release zip fromPowerShellEditorServices releasesand extract it.
3. Point Hermes at the extracted bundle — the directory that containsPowerShellEditorServices/Start-EditorServices.ps1. Either:setlsp.servers.powershell.command: ["/path/to/bundle"]inconfig.yaml, orextract it to<HERMES_HOME>/lsp/PowerShellEditorServices, orexportPSES_BUNDLE_PATH=/path/to/bundle.

`pwsh`
`powershell`
`PowerShellEditorServices/Start-EditorServices.ps1`
- setlsp.servers.powershell.command: ["/path/to/bundle"]inconfig.yaml, or
- extract it to<HERMES_HOME>/lsp/PowerShellEditorServices, or
- exportPSES_BUNDLE_PATH=/path/to/bundle.

`lsp.servers.powershell.command: ["/path/to/bundle"]`
`config.yaml`
`<HERMES_HOME>/lsp/PowerShellEditorServices`
`PSES_BUNDLE_PATH=/path/to/bundle`

hermes lsp statusreportsinstalledoncepwshis found; if the
bundle is missing you'll see a one-time warning in the logs with the
download link.

`hermes lsp status`
`installed`
`pwsh`

A few servers are installed alongside a peer dependency that npm
won't auto-pull. The current case istypescript-language-server,
which requires thetypescriptSDK importable from the samenode_modulestree — Hermes installs both packages together when you
runhermes lsp install typescriptor auto-install fires on first
use.

`typescript-language-server`
`typescript`
`node_modules`
`hermes lsp install typescript`

## CLI​

```
hermes lsp status          # service state + per-server install statushermes lsp list            # registry, optionally --installed-onlyhermes lsp install <id>    # eagerly install one serverhermes lsp install-all     # try every server with a known recipehermes lsp restart         # tear down running clientshermes lsp which <id>      # print resolved binary path
```

hermes lsp statusis the best starting point — it shows which
languages will get semantic diagnostics today and which need a
binary installed.

`hermes lsp status`

## Configuration​

The defaults work for typical setups; nothing to set if the binaries
are on PATH.

```
# config.yamllsp:  # Master toggle. Disabling skips the entire subsystem — no servers  # spawn, no background event loop runs.  enabled: true  # How long to wait for diagnostics after each write.  wait_mode: document      # "document" or "full"  wait_timeout: 5.0  # How to handle missing server binaries.  #   auto    — install via npm/pip/go install into <HERMES_HOME>/lsp/bin  #   manual  — only use binaries already on PATH  install_strategy: auto  # Per-server overrides (all optional).  servers:    pyright:      disabled: false      command: ["/abs/path/to/pyright-langserver", "--stdio"]      env: { PYRIGHT_LOG_LEVEL: "info" }      initialization_options:        python:          analysis:            typeCheckingMode: "strict"    typescript:      disabled: true       # skip TS even when its extensions match
```

### Per-server keys​

- disabled: true— skip this server entirely even when its
extensions match a file.
- command: [bin, ...args]— pin a custom binary path. Bypasses
auto-install.
- env: {KEY: value}— extra env vars passed to the spawned process.
- initialization_options: {...}— merged into the LSPinitializationOptionspayload sent in theinitializehandshake. Server-specific; consult the language server's docs.

`disabled: true`
`command: [bin, ...args]`
`env: {KEY: value}`
`initialization_options: {...}`
`initializationOptions`
`initialize`

## Installation locations​

Wheninstall_strategy: auto, Hermes installs binaries into<HERMES_HOME>/lsp/bin/. NPM packages land in<HERMES_HOME>/lsp/node_modules/with bin symlinks one level up.
Go binaries come fromgo installwithGOBINpointed at the
staging dir.

`install_strategy: auto`
`<HERMES_HOME>/lsp/bin/`
`<HERMES_HOME>/lsp/node_modules/`
`go install`
`GOBIN`

Nothing is ever installed to/usr/local/,~/.local/, or any other
shared location — the staging dir is fully Hermes-owned and is
removed when you reset the profile.

`/usr/local/`
`~/.local/`

## Performance characteristics​

LSP servers arelazy-spawnedon first use. Editing a Python file
in a project that's never seen.pytraffic spawns pyright; the
spawn takes 1-3 seconds for most servers (rust-analyzer can take 10+
on a cold project). Subsequent edits in the same workspace re-use
the running server.

`.py`

The LSP layer adds a few milliseconds to clean writes when no
diagnostics are emitted. When diagnostics are emitted, the wait
budget iswait_timeoutseconds — typically the server responds in
tens of milliseconds for pyright/tsserver and a few seconds for
rust-analyzer mid-indexing.

`wait_timeout`

Servers are kept alive for the life of the Hermes process. There's
no idle-timeout reaper — the cost of restarting the server's index
on every write would be far higher than holding the daemon.

## Disabling​

Setlsp.enabled: falseinconfig.yamlto disable the entire
subsystem. The post-write check falls back to the in-process syntax
check (ast.parsefor Python,json.loadsfor JSON, etc.) which
ships unchanged from earlier versions.

`lsp.enabled: false`
`config.yaml`
`ast.parse`
`json.loads`

To disable a single language without disabling the whole layer:

```
lsp:  servers:    rust-analyzer:      disabled: true
```

## Troubleshooting​

hermes lsp statusshows a server as "missing"

`hermes lsp status`

The binary isn't on PATH and isn't in<HERMES_HOME>/lsp/bin/. Runhermes lsp install <server_id>to attempt an auto-install, or
install the binary manually through the language's normal toolchain.

`<HERMES_HOME>/lsp/bin/`
`hermes lsp install <server_id>`

Backend warningssection inhermes lsp status

`Backend warnings`
`hermes lsp status`

Some servers ship as thin wrappers around an external CLI for actual
diagnostics — they spawn cleanly and accept requests but never emit
errors when the sidecar binary is missing. The most common case isbash-language-server, which delegates diagnostics toshellcheck.
Whenhermes lsp statusshows aBackend warningssection, install
the named tool through your OS package manager:

`bash-language-server`
`shellcheck`
`hermes lsp status`
`Backend warnings`

```
apt install shellcheck      # Debian / Ubuntubrew install shellcheck     # macOSscoop install shellcheck    # Windows
```

The same warning is logged once at server spawn time in~/.hermes/logs/agent.log.

`~/.hermes/logs/agent.log`

Server starts but never returns diagnostics

Check~/.hermes/logs/agent.logfor[agent.lsp.client]entries —
both stderr from the language server and protocol errors land
there. Some servers (rust-analyzer especially) need to finish a
project-wide index before they emit per-file diagnostics; the first
edit after server start may complete with no diagnostics, with
subsequent edits picking them up.

`~/.hermes/logs/agent.log`
`[agent.lsp.client]`

Server crashed

A crashed server is added to the broken-set and won't be retried for
the rest of the session. Runhermes lsp restartto clear the set;
the next edit re-spawns.

`hermes lsp restart`

Editing a file outside any git repo

By design, LSP only runs inside a git repository. If the project isn't
yet initialized, rungit initto enable LSP diagnostics. Otherwise the
in-process syntax-only fallback applies.

`git init`