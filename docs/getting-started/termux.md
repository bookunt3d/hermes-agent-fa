---
layout: docs
title: "اندروید / Termux"
permalink: /getting-started/termux/
---

- 
- Getting Started
- Android / Termux

# Hermes on Android with Termux

Termux (Android) is aTier 2 platform. The installer script and documentation here are maintained on a best-effort basis only. Commits tomainmay break these packages at any point in time.

[Tier 2 platform](/docs/getting-started/platform-support#tier-2)
`main`

Hermes Agent can run directly on an Android phone throughTermux.

[Termux](https://termux.dev/)

It gives you a working local CLI on the phone, plus the core extras that are currently known to install cleanly on Android.

## What is supported in the tested path?​

The tested Termux bundle installs:

- the Hermes CLI
- cron support
- PTY/background terminal support
- Telegram gateway support (manual / best-effort background runs)
- MCP support
- Honcho memory support
- ACP support

Concretely, it maps to:

```
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

## What is not part of the tested path yet?​

A few features still need desktop/server-style dependencies that are not published for Android, or have not been validated on phones yet:

- .[all]is not supported on Android today
- thevoiceextra is blocked byfaster-whisper -> ctranslate2, andctranslate2does not publish Android wheels
- automatic browser / Playwright bootstrap is skipped in the Termux installer
- Docker-based terminal isolation is not available inside Termux
- Android may still suspend Termux background jobs, so gateway persistence is best-effort rather than a normal managed service

`.[all]`
`voice`
`faster-whisper -> ctranslate2`
`ctranslate2`

That does not stop Hermes from working well as a phone-native CLI agent — it just means the recommended mobile install is intentionally narrower than the desktop/server install.

## Option 1: One-line installer​

Hermes now ships a Termux-aware installer path:

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

On Termux, the installer automatically:

- usespkgfor system packages
- creates the venv withpython -m venv
- attempts the broad.[termux-all]extra first and falls back to the smaller.[termux]extra (then a base install) — the curl installer matches this order automatically
- linkshermesinto$PREFIX/binso it stays on your Termux PATH
- skips the untested browser / WhatsApp bootstrap

`pkg`
`python -m venv`
`.[termux-all]`
`.[termux]`
`hermes`
`$PREFIX/bin`

If you want the explicit commands or need to debug a failed install, use the manual path below.

## Option 2: Manual install (fully explicit)​

### 1. Update Termux and install system packages​

```
pkg updatepkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ffmpeg
```

Why these packages?

- python— runtime + venv support
- git— clone/update the repo
- clang,rust,make,pkg-config,libffi,openssl— needed to build a few Python dependencies on Android
- nodejs— optional Node runtime for experiments beyond the tested core path
- ripgrep— fast file search
- ffmpeg— media / TTS conversions

`python`
`git`
`clang`
`rust`
`make`
`pkg-config`
`libffi`
`openssl`
`nodejs`
`ripgrep`
`ffmpeg`

### 2. Clone Hermes​

```
git clone https://github.com/NousResearch/hermes-agent.gitcd hermes-agent
```

### 3. Create a virtual environment​

```
python -m venv venvsource venv/bin/activateexport ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"python -m pip install --upgrade pip setuptools wheel
```

ANDROID_API_LEVELis important for Rust / maturin-based packages such asjiter.

`ANDROID_API_LEVEL`
`jiter`

### 4. Install the tested Termux bundle​

```
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

If you only want the minimal core agent, this also works:

```
python -m pip install -e '.' -c constraints-termux.txt
```

### 5. Puthermeson your Termux PATH​

`hermes`

```
ln -sf "$PWD/venv/bin/hermes" "$PREFIX/bin/hermes"
```

$PREFIX/binis already on PATH in Termux, so this makes thehermescommand persist across new shells without re-activating the venv every time.

`$PREFIX/bin`
`hermes`

### 6. Verify the install​

```
hermes versionhermes doctor
```

### 7. Start Hermes​

```
hermes
```

## Recommended follow-up setup​

### Configure a model​

```
hermes model
```

Or set keys directly in~/.hermes/.env.

`~/.hermes/.env`

### Re-run the full interactive setup wizard later​

```
hermes setup
```

### Install optional Node dependencies manually​

The tested Termux path skips Node/browser bootstrap on purpose. If you want to experiment with browser tooling later:

```
pkg install nodejs-ltsnpm install
```

The browser tool automatically includes Termux directories (/data/data/com.termux/files/usr/bin) in its PATH search, soagent-browserandnpxare discovered without any extra PATH configuration.

`/data/data/com.termux/files/usr/bin`
`agent-browser`
`npx`

Treat browser / WhatsApp tooling on Android as experimental until documented otherwise.

## Troubleshooting​

### No solution foundwhen installing.[all]​

`No solution found`
`.[all]`

Use the tested Termux bundle instead:

```
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

The blocker is currently thevoiceextra:

`voice`
- voicepullsfaster-whisper
- faster-whisperdepends onctranslate2
- ctranslate2does not publish Android wheels

`voice`
`faster-whisper`
`faster-whisper`
`ctranslate2`
`ctranslate2`

### uv pip installfails on Android​

`uv pip install`

Use the Termux path with the stdlib venv +pipinstead:

`pip`

```
python -m venv venvsource venv/bin/activateexport ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"python -m pip install --upgrade pip setuptools wheelpython -m pip install -e '.[termux]' -c constraints-termux.txt
```

### jiter/maturincomplains aboutANDROID_API_LEVEL​

`jiter`
`maturin`
`ANDROID_API_LEVEL`

Set the API level explicitly before installing:

```
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"python -m pip install -e '.[termux]' -c constraints-termux.txt
```

### hermes doctorsays ripgrep or Node is missing​

`hermes doctor`

Install them with Termux packages:

```
pkg install ripgrep nodejs
```

### Build failures while installing Python packages​

Make sure the build toolchain is installed:

```
pkg install clang rust make pkg-config libffi openssl
```

Then retry:

```
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

## Known limitations on phones​

- Docker backend is unavailable
- local voice transcription viafaster-whisperis unavailable in the tested path
- browser automation setup is intentionally skipped by the installer
- some optional extras may work, but only.[termux]and.[termux-all]are currently documented as the tested Android bundles

`faster-whisper`
`.[termux]`
`.[termux-all]`

If you hit a new Android-specific issue, please open a GitHub issue with:

- your Android version
- termux-info
- python --version
- hermes doctor
- the exact install command and full error output

`termux-info`
`python --version`
`hermes doctor`
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/termux.md)