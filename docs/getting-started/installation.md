---
layout: docs
title: "نصب"
permalink: /getting-started/installation/
---

- 
- Getting Started
- Installation

# Installation

Get Hermes Agent up and running in under two minutes!

For the full platform support matrix (which OSes, distribution methods, and
platform-gated features are supported), seePlatform Support.

[Platform Support](/docs/getting-started/platform-support)

## Quick Install​

### With the Hermes Desktop installer on macOS or Windows (recommended)​

To easily install the command-line and desktop applications,download the Hermes Desktop installerfrom our website and run it.

[download the Hermes Desktop installer](https://hermes-agent.nousresearch.com/)

### Without Hermes Desktop:​

For a command-line only install without Hermes Desktop, run:

#### Linux / macOS / WSL2 / Android (Termux)​

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

#### Windows (native)​

Run in powershell:

```
iex (irm https://hermes-agent.nousresearch.com/install.ps1) 
```

If you want to install & run Hermes Desktop after a command-line only install, simply run

```
hermes desktop
```

### What the Installer Does​

The installer handles everything automatically — all dependencies (Python, Node.js, ripgrep, ffmpeg), the repo clone, virtual environment, globalhermescommand setup, and LLM provider configuration. By the end, you're ready to chat.

`hermes`

#### Install Layout​

Where the installer puts things depends on whether you're installing as a normal user or as root:

| Installer | Code lives at | hermesbinary | Data directory |
| --- | --- | --- | --- |
| Per-user (git installer) | ~/.hermes/hermes-agent/ | ~/.local/bin/hermes(symlink) | ~/.hermes/ |
| Root-mode (sudo curl … | sudo bash) | /usr/local/lib/hermes-agent/ | /usr/local/bin/hermes | /root/.hermes/(or$HERMES_HOME) |

`hermes`
`~/.hermes/hermes-agent/`
`~/.local/bin/hermes`
`~/.hermes/`
`sudo curl … | sudo bash`
`/usr/local/lib/hermes-agent/`
`/usr/local/bin/hermes`
`/root/.hermes/`
`$HERMES_HOME`

The root-modeFHS layout(/usr/local/lib/…,/usr/local/bin/hermes) matches where other system-wide developer tools land on Linux. It's useful for shared-machine deployments where one system install should serve every user. Per-user config (auth, skills, sessions) still lives under each user's~/.hermes/or explicitHERMES_HOME.

`/usr/local/lib/…`
`/usr/local/bin/hermes`
`~/.hermes/`
`HERMES_HOME`

### After Installation​

Reload your shell and start chatting:

```
source ~/.bashrc   # or: source ~/.zshrchermes             # Start chatting!
```

To reconfigure individual settings later, use the dedicated commands:

```
hermes model          # Choose your LLM provider and modelhermes tools          # Configure which tools are enabledhermes gateway setup  # Set up messaging platformshermes config set     # Set individual config valueshermes setup          # Or run the full setup wizard to configure everything at once
```

One subscription covers 300+ models plus theTool Gateway(web search, image generation, TTS, cloud browser). Skip the per-tool key juggling:

[Tool Gateway](/docs/user-guide/features/tool-gateway)

```
hermes setup --portal
```

That logs you in, sets Nous as your provider, and turns on the Tool Gateway in one command.

## Prerequisites​

Installer:On non-Windows platforms, the only prerequisite isGit. On Linux, also make surecurlandxz-utilsare available (the installer downloads Node.js as a.tar.xzarchive). The desktop app additionally requiresg++(orbuild-essentialon Debian/Ubuntu) to compile native modules. The installer automatically handles everything else:

`curl`
`xz-utils`
`.tar.xz`
`g++`
`build-essential`
- uv(fast Python package manager)
- Python 3.11(via uv, no sudo needed)
- Node.js v22(for browser automation and WhatsApp bridge)
- ripgrep(fast file search)
- ffmpeg(audio format conversion for TTS)

You donotneed to install Python, Node.js, ripgrep, or ffmpeg manually. The installer detects what's missing and installs it for you. Just make suregitis available (git --version). On Linux, ensurecurlandxz-utilsare installed (sudo apt install curl xz-utilson Debian/Ubuntu). For the desktop app, also installbuild-essential(sudo apt install build-essential).

`git`
`git --version`
`curl`
`xz-utils`
`sudo apt install curl xz-utils`
`build-essential`
`sudo apt install build-essential`

Nix isno longer an explicitly supported install path(best-effort only). If you already use Nix (on NixOS, macOS, or Linux), there's a dedicated setup path with a Nix flake, declarative NixOS module, and optional container mode. See theNix & NixOS Setupguide.

[Nix & NixOS Setup](/docs/getting-started/nix-setup)

## Manual / Developer Installation​

If you want to clone the repo and install from source — for contributing, running from a specific branch, or having full control over the virtual environment — see theDevelopment Setupsection in the Contributing guide.

[Development Setup](/docs/developer-guide/contributing#development-setup)

## Non-Sudo / System Service User Installs​

Running Hermes as a dedicated unprivileged user (e.g. ahermessystemd service account, or any user withoutsudoaccess) is supported. The only thing on the install path that genuinely needs root is Playwright's--with-depsstep, whichapt-installs shared libraries (libnss3,libxkbcommon, etc.) used by Chromium. The installer detects whether sudo is available and gracefully degrades when it isn't — it will install the Chromium binary into the service user's own Playwright cache and print the exact command an administrator needs to run separately.

`hermes`
`sudo`
`--with-deps`
`apt`
`libnss3`
`libxkbcommon`

Recommended split (Debian/Ubuntu):

1. One time, as an admin user with sudo, install the system libraries Chromium needs:sudonpx playwright install-deps chromium(You can run this from anywhere —npxwill fetch Playwright on the fly.)
2. As the unprivileged service user, run the regular installer. It will detect the missing sudo, skip--with-deps, and install Chromium into the user's local Playwright cache:curl-fsSLhttps://hermes-agent.nousresearch.com/install.sh|bashIf you want to skip the Playwright step entirely — for example because you're running headless and don't need browser automation — pass--skip-browser:curl-fsSLhttps://hermes-agent.nousresearch.com/install.sh|bash-s-- --skip-browser
3. Makehermesavailable to the service user's shells.The installer writes the launcher to~/.local/bin/hermes. System service accounts often have a minimal PATH that doesn't include~/.local/bin. Either add it to the user's environment, or symlink the launcher into a system location:# Option A — add to the service user's profileecho'export PATH="$HOME/.local/bin:$PATH"'>>~/.bashrc# Option B — symlink system-wide (run as an admin)sudoln-s/home/hermes/.hermes/hermes-agent/venv/bin/hermes /usr/local/bin/hermes
4. Verify:hermes doctorshould now run cleanly. If you getModuleNotFoundError: No module named 'dotenv', you're invoking the repo sourcehermesfile (~/.hermes/hermes-agent/hermes) with system Python instead of the venv launcher (~/.hermes/hermes-agent/venv/bin/hermes) — fix step 3.

One time, as an admin user with sudo, install the system libraries Chromium needs:

```
sudo npx playwright install-deps chromium
```

(You can run this from anywhere —npxwill fetch Playwright on the fly.)

`npx`

As the unprivileged service user, run the regular installer. It will detect the missing sudo, skip--with-deps, and install Chromium into the user's local Playwright cache:

`--with-deps`

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

If you want to skip the Playwright step entirely — for example because you're running headless and don't need browser automation — pass--skip-browser:

`--skip-browser`

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-browser
```

Makehermesavailable to the service user's shells.The installer writes the launcher to~/.local/bin/hermes. System service accounts often have a minimal PATH that doesn't include~/.local/bin. Either add it to the user's environment, or symlink the launcher into a system location:

`hermes`
`~/.local/bin/hermes`
`~/.local/bin`

```
# Option A — add to the service user's profileecho 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc# Option B — symlink system-wide (run as an admin)sudo ln -s /home/hermes/.hermes/hermes-agent/venv/bin/hermes /usr/local/bin/hermes
```

Verify:hermes doctorshould now run cleanly. If you getModuleNotFoundError: No module named 'dotenv', you're invoking the repo sourcehermesfile (~/.hermes/hermes-agent/hermes) with system Python instead of the venv launcher (~/.hermes/hermes-agent/venv/bin/hermes) — fix step 3.

`hermes doctor`
`ModuleNotFoundError: No module named 'dotenv'`
`hermes`
`~/.hermes/hermes-agent/hermes`
`~/.hermes/hermes-agent/venv/bin/hermes`

The same pattern works on Arch (the installer uses pacman with the same sudo-detection logic), Fedora/RHEL, and openSUSE — those distros don't support--with-depsat all, so an administrator always installs the system libraries separately. The relevantdnf/zyppercommands are printed by the installer.

`--with-deps`
`dnf`
`zypper`

## Troubleshooting​

| Problem | Solution |
| --- | --- |
| hermes: command not found | Reload your shell (source ~/.bashrc) or check PATH |
| API key not set | Runhermes modelto configure your provider, orhermes config set OPENROUTER_API_KEY your_key |
| Missing config after update | Runhermes config checkthenhermes config migrate |

`hermes: command not found`
`source ~/.bashrc`
`API key not set`
`hermes model`
`hermes config set OPENROUTER_API_KEY your_key`
`hermes config check`
`hermes config migrate`

For more diagnostics, runhermes doctor— it will tell you exactly what's missing and how to fix it.

`hermes doctor`

## Install method auto-detection​

Hermes auto-detects whether it was installed viapip, the git installer, Homebrew, or NixOS, andhermes updateprints the matching update command for that path. There's no env var to set — the detection is based on the install layout (Python site-packages,~/.hermes/hermes-agent/, Homebrew prefix, or Nix store path).hermes doctoralso surfaces the detected method under its environment summary.

`pip`
`hermes update`
`~/.hermes/hermes-agent/`
`hermes doctor`
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/installation.md)