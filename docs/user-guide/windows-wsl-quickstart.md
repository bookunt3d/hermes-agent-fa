---
layout: docs
title: "ویندوز (WSL2)"
permalink: /user-guide/windows-wsl-quickstart/
---

- 
- Using Hermes
- Windows (WSL2)

# Windows (WSL2) Guide

Hermes Agent now supportsbothnative Windows and WSL2.  This page covers the WSL2 path; for the native PowerShell install see the dedicatedWindows (Native) Guide.

[Windows (Native) Guide](/docs/user-guide/windows-native)

When to pick WSL2 over native:

- You want to use the dashboard's embedded terminal (/chattab) — that pane requires a POSIX PTY and is WSL2-only.
- You're doing POSIX-heavy development work and want your Hermes sessions to share the same filesystem / paths as your dev tools.
- You already have a WSL2 environment and don't want to maintain a second install.

`/chat`

When native is fine (or better):

- Interactive chat, gateway (Telegram/Discord/etc.), cron scheduler, browser tool, MCP servers, and most Hermes features all run natively on Windows.
- You don't want to think about crossing the WSL↔Windows boundary every time you reference a file or open a URL.

In WSL2 there are effectively two computers in play: your Windows host, and a Linux VM managed by WSL.  Most confusion comes from not being sure which one you're on at any moment.

This guide covers the parts of that split that specifically affect Hermes: installing WSL2, getting files back and forth between Windows and Linux, networking in both directions, and the pitfalls people actually hit.

A Chinese-language walkthrough of the minimum install path is maintained on this same page — switch via thelanguagemenu (top right) and select简体中文.

## Why WSL2 (vs. native Windows)​

The native Windows install runs in Windows directly: your Windows terminal (PowerShell, Windows Terminal, etc.), Windows filesystem paths (C:\Users\…), and Windows processes.  Hermes uses Git Bash to run shell commands, which is how Claude Code and other agents handle Windows today — it sidesteps the POSIX-vs-Windows gap without a full rewrite.

`C:\Users\…`

WSL2 runs a real Linux kernel in a lightweight VM, so Hermes inside it is essentially identical to running on Ubuntu.  That's valuable when you want a real POSIX environment:fork,/tmp, UNIX sockets, signal semantics, PTY-backed terminals, shells likebash/zsh, and tools likerg,git,ffmpegthat behave the way they do on Linux.

`fork`
`/tmp`
`bash`
`zsh`
`rg`
`git`
`ffmpeg`

Practical consequences of WSL2:

- The Hermes CLI, gateway, sessions, memory, skills, and tool runtimes all live inside the Linux VM.
- Windows programs (browsers, native apps, Chrome with your logged-in profile) live outside it.
- Every time you want the two to talk — share files, open URLs, control Chrome, hit a local model server, expose the Hermes gateway to your phone — you cross a boundary. Those boundaries are what this guide is about.

## Install WSL2​

From anAdmin PowerShellor Windows Terminal:

```
wsl --install
```

On a fresh Windows 10 22H2+ or Windows 11 box this installs the WSL2 kernel, the Virtual Machine Platform feature, and a default Ubuntu distro. Reboot when prompted. After reboot Ubuntu will open and ask for a Linux username + password — this is anew Linux user, unrelated to your Windows account.

Verify you're actually on WSL2 (not legacy WSL1):

```
wsl --list --verbose
```

You should seeVERSION  2. If a distro showsVERSION  1, convert it:

`VERSION  2`
`VERSION  1`

```
wsl --set-version Ubuntu 2wsl --set-default-version 2
```

Hermes does not work reliably on WSL1 — WSL1 translates Linux syscalls on the fly and some behaviors (procfs, signals, network) diverge from real Linux.

### Distro choice​

Ubuntu (LTS) is what we test against. Debian works. Arch and NixOS work for people who want them, but the one-line installer assumes a Debian-derivedaptsystem — see theNix setup guidefor that path.

`apt`
[Nix setup guide](/docs/getting-started/nix-setup)

### Enable systemd (recommended)​

The hermes gateway (and anything else you want to keep running) is easier to manage with systemd. On modern WSL, enable it once inside your distro:

```
sudo tee /etc/wsl.conf >/dev/null <<'EOF'[boot]systemd=true[interop]enabled=trueappendWindowsPath=true[automount]options = "metadata,umask=22,fmask=11"EOF
```

Then from PowerShell:

```
wsl --shutdown
```

Reopen your WSL terminal.ps -p 1 -o comm=should printsystemd.

`ps -p 1 -o comm=`
`systemd`

Themetadatamount option above is important — without it, files on/mnt/c/...can't store real Linux permission bits, which breaks things likechmod +xon scripts under Windows paths.

`metadata`
`/mnt/c/...`
`chmod +x`

### Install Hermes inside WSL​

Once you have a WSL2 shell open:

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bashsource ~/.bashrchermes
```

The installer treats WSL2 as plain Linux — nothing WSL-specific is needed. SeeInstallationfor the full layout.

[Installation](/docs/getting-started/installation)

## Filesystem: crossing the Windows ↔ WSL2 boundary​

This is the part that trips up the most people. There aretwo filesystems, and where you put your files matters — for performance, correctness, and what tools can see.

### The two directions​

| Direction | Path inside | Path you use |
| --- | --- | --- |
| Windows disk, seen from WSL | C:\Users\you\Documents | /mnt/c/Users/you/Documents |
| WSL disk, seen from Windows | /home/you/code | \\wsl$\Ubuntu\home\you\code(or\\wsl.localhost\Ubuntu\...on newer builds) |

`C:\Users\you\Documents`
`/mnt/c/Users/you/Documents`
`/home/you/code`
`\\wsl$\Ubuntu\home\you\code`
`\\wsl.localhost\Ubuntu\...`

Both are real, both work, but they arenot the same filesystem— they're bridged by a 9P network protocol under the hood. That has real performance and semantic consequences.

### Where to put Hermes and your projects​

Rule of thumb: keep everything Linux-ish inside the Linux filesystem.

- Your Hermes install (~/.hermes/) — Linux side. The installer already does this.
- Your git repos that you work on from WSL — Linux side (~/code/...,~/projects/...).
- Your models, datasets, venvs — Linux side.

`~/.hermes/`
`~/code/...`
`~/projects/...`

What you get by following this rule:

- Fast I/O.Operations on/mnt/c/...go through 9P and are 10–100× slower than native ext4.git statuson a 10k-file repo that feels instant under~/codecan take 15+ seconds under/mnt/c.
- Correct permissions.Linux permission bits are a best-effort emulation on/mnt/c. Things likesshrefusing a key with "bad permissions" orchmod +xsilently failing are common.
- Reliable file watchers.inotify across 9P is flaky — file watchers (dev servers, test runners) routinely miss changes on/mnt/c.
- No case-sensitivity surprises.Windows paths are case-insensitive by default; Linux is case-sensitive. Projects with bothReadme.mdandREADME.mdbehave differently depending which side you're on.

`/mnt/c/...`
`git status`
`~/code`
`/mnt/c`
`/mnt/c`
`ssh`
`chmod +x`
`/mnt/c`
`Readme.md`
`README.md`

Put things on/mnt/conly when youneeda file to live on the Windows side — e.g., you want to open it from a Windows GUI app, or Windows Chrome's DevTools MCP needs the current directory to be a Windows-reachable path.

`/mnt/c`

### Getting files back and forth​

From Windows → into WSL:easiest is to open Explorer and type\\wsl.localhost\Ubuntuin the address bar. You can then drag-drop into\home\<you>\.... Or from PowerShell:

`\\wsl.localhost\Ubuntu`
`\home\<you>\...`

```
wsl cp /mnt/c/Users/you/Downloads/file.pdf ~/incoming/
```

From WSL → into Windows:copy to/mnt/c/Users/<you>/...and it shows up in Windows Explorer immediately:

`/mnt/c/Users/<you>/...`

```
cp ~/reports/output.pdf /mnt/c/Users/you/Desktop/
```

Open a WSL file in a Windows app(GUI editor, browser, etc.): useexplorer.exeorwslview:

`explorer.exe`
`wslview`

```
sudo apt install wslu     # once — gives you wslview, wslpath, wslopen, etc.wslview ~/reports/output.pdf    # opens with the Windows default handlerexplorer.exe .                  # opens the current WSL dir in Windows Explorer
```

Convert paths between the two universes:

```
wslpath -w ~/code/project        # → \\wsl.localhost\Ubuntu\home\you\code\projectwslpath -u 'C:\Users\you'        # → /mnt/c/Users/you
```

### Line endings, BOMs, and git​

If you edit files on the Windows side with a Windows editor, they may getCRLFline endings. Whenbashor Python on the Linux side reads them, shell scripts break withbad interpreter: /bin/bash^Mand Python can fail on BOM'd.envfiles.

`CRLF`
`bash`
`bad interpreter: /bin/bash^M`
`.env`

The fix is a sane git config inside WSL (not on Windows):

```
git config --global core.autocrlf inputgit config --global core.eol lf
```

For files that already have CRLF:

```
sudo apt install dos2unixdos2unix path/to/script.sh
```

### "Clone inside WSL or on/mnt/c?"​

`/mnt/c`

Clone inside WSL. Always, unless you have a specific reason not to. A typical Hermes workflow (hermes chat, tool calls thatrg/ripgrepthe repo, file watchers, background gateway) will be dramatically faster and more reliable against~/code/myrepothan/mnt/c/Users/you/myrepo.

`hermes chat`
`rg`
`ripgrep`
`~/code/myrepo`
`/mnt/c/Users/you/myrepo`

One exception:MCP bridges that launch Windows binaries.If you're usingchrome-devtools-mcpthroughcmd.exe(seeMCP guide: WSL → Windows Chrome), Windows may complain with aUNCwarning if Hermes's current working directory is~. In that case, start Hermes from somewhere under/mnt/c/so the Windows process has a drive-letter cwd.

`chrome-devtools-mcp`
`cmd.exe`
[MCP guide: WSL → Windows Chrome](/docs/guides/use-mcp-with-hermes#wsl2-bridge-hermes-in-wsl-to-windows-chrome)
`UNC`
`~`
`/mnt/c/`

## Networking: WSL ↔ Windows​

WSL2 runs in a lightweight VM with its own network stack. That meanslocalhostinside WSL isnot the same aslocalhoston Windows — they're two separate hosts from the network's point of view. You need to decide, for each service, which direction traffic flows and pick the right bridge.

`localhost`
`localhost`

Two cases come up constantly.

### Case 1 — Hermes in WSL talks to a service on Windows​

Most common: you're runningOllama, LM Studio, or a llama-server on Windows, and Hermes (inside WSL) needs to hit it.

The canonical how-to for this lives in the providers guide:WSL2 Networking for Local Models →

[WSL2 Networking for Local Models →](/docs/integrations/providers#wsl2-networking-windows-users)

Short version:

- Windows 11 22H2+:turn on mirrored networking mode (networkingMode=mirroredin%USERPROFILE%\.wslconfig, thenwsl --shutdown).localhostthen works in both directions.
- Windows 10 or older builds:use the Windows host IP (the default gateway of WSL's virtual network) and make sure the server on Windows binds to0.0.0.0, not just127.0.0.1. Windows Firewall usually also needs a rule for the port.

`networkingMode=mirrored`
`%USERPROFILE%\.wslconfig`
`wsl --shutdown`
`localhost`
`0.0.0.0`
`127.0.0.1`

For the full table (Ollama / LM Studio / vLLM / SGLang bind addresses, firewall rule one-liners, dynamic IP helpers, Hyper-V firewall workaround), follow the link above — don't duplicate it.

### Case 2 — Something on Windows (or your LAN) talks to Hermes in WSL​

This is the reverse direction and is less documented elsewhere, but it's what you need for:

- Using the Hermesweb dashboardfrom a Windows browser.
- Using theOpenAI-compatible API server(exposed byhermes gatewaywhenAPI_SERVER_ENABLED=true) from a Windows-side tool. See theAPI Server feature page.
- Testing amessaging gateway(Telegram, Discord, etc.) where the platform pings a local webhook URL — usually you'd usecloudflared/ngrokrather than raw port forwarding.

`hermes gateway`
`API_SERVER_ENABLED=true`
[API Server feature page](/docs/user-guide/features/api-server)
`cloudflared`
`ngrok`

#### Subcase 2a: from the Windows host itself​

OnWindows 11 22H2+ with mirrored mode enabled, there is nothing to do. A process in WSL that binds to0.0.0.0:8080(or even127.0.0.1:8080) is reachable from a Windows browser athttp://localhost:8080. WSL publishes the bind back to the host automatically.

`0.0.0.0:8080`
`127.0.0.1:8080`
`http://localhost:8080`

OnNAT mode(Windows 10 / older Windows 11), the default "localhost forwarding" in WSL2 will generally forward Linux-side127.0.0.1binds to Windowslocalhost, so a Hermes service started with--host 127.0.0.1is usually reachable ashttp://localhost:PORTfrom Windows. If it isn't:

`127.0.0.1`
`localhost`
`--host 127.0.0.1`
`http://localhost:PORT`
- Bind to0.0.0.0explicitly inside WSL.
- Find the WSL VM's IP withip -4 addr show eth0 | grep inetand hit that from Windows.

`0.0.0.0`
`ip -4 addr show eth0 | grep inet`

#### Subcase 2b: from another device on your LAN (phone, tablet, another PC)​

This is the real pain. Traffic flowsLAN device → Windows host → WSL VM, and you have to set up both hops:

1. Bind on all interfaces inside WSL.A process listening on127.0.0.1will never be reachable from outside the VM. Use0.0.0.0.
2. Port-forward Windows → WSL VM.In mirrored mode this is automatic. In NAT mode you have to do it yourself, per port, in Admin PowerShell:# Grab the WSL VM's current IP (it changes on every WSL restart under NAT)$wslIp = (wsl hostname -I).Trim().Split(' ')[0]# Forward Windows port 8080 → WSL:8080netsh interface portproxy add v4tov4 `listenaddress=0.0.0.0 listenport=8080 `connectaddress=$wslIp connectport=8080# Allow it through Windows FirewallNew-NetFirewallRule -DisplayName "Hermes WSL 8080" `-Direction Inbound -Protocol TCP -LocalPort 8080 -Action AllowRemove later withnetsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8080.
3. Point the LAN device athttp://<windows-lan-ip>:8080.

Bind on all interfaces inside WSL.A process listening on127.0.0.1will never be reachable from outside the VM. Use0.0.0.0.

`127.0.0.1`
`0.0.0.0`

Port-forward Windows → WSL VM.In mirrored mode this is automatic. In NAT mode you have to do it yourself, per port, in Admin PowerShell:

```
# Grab the WSL VM's current IP (it changes on every WSL restart under NAT)$wslIp = (wsl hostname -I).Trim().Split(' ')[0]# Forward Windows port 8080 → WSL:8080netsh interface portproxy add v4tov4 `  listenaddress=0.0.0.0 listenport=8080 `  connectaddress=$wslIp connectport=8080# Allow it through Windows FirewallNew-NetFirewallRule -DisplayName "Hermes WSL 8080" `  -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

Remove later withnetsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8080.

`netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8080`

Point the LAN device athttp://<windows-lan-ip>:8080.

`http://<windows-lan-ip>:8080`

Because the WSL VM IP drifts on each restart in NAT mode, a one-shot rule survives only until the nextwsl --shutdown. For anything persistent, either use mirrored mode or put the port-proxy step in a script that runs at Windows login.

`wsl --shutdown`

For webhooks from cloud messaging providers (TelegramsetWebhook, Slack events, etc.), don't fight port-forwarding — usecloudflaredtunnels. See thewebhooks guide.

`setWebhook`
`cloudflared`
[webhooks guide](/docs/user-guide/messaging/webhooks)

## Running Hermes services long-term on Windows​

The HermesTool Gatewayand the API server are long-lived processes. In WSL2 you have a few options for keeping them up.

[Tool Gateway](/docs/user-guide/features/tool-gateway)

### Desktop shortcut for opening Hermes quickly​

If you just want a double-click launcher for an interactive Hermes shell, create
it on the Windows side and have it jump into WSL for you:

1. Right-click the Windows desktop and chooseNew -> Shortcut.
2. For the target, use your distro name (replaceUbuntuif needed):wt.exe -w 0 -p "Ubuntu" wsl.exe -d Ubuntu --cd ~ -- bash -ic "hermes"
3. Name it something obvious likeHermes.

Right-click the Windows desktop and chooseNew -> Shortcut.

For the target, use your distro name (replaceUbuntuif needed):

`Ubuntu`

```
wt.exe -w 0 -p "Ubuntu" wsl.exe -d Ubuntu --cd ~ -- bash -ic "hermes"
```

Name it something obvious likeHermes.

`Hermes`

That opens Windows Terminal, starts your WSL distro, drops you in your Linux
home directory, and launches Hermes. Ifhermesis not on PATH yet, open WSL
once manually and runsource ~/.bashrc, or replace the command withuv run hermesinside your project checkout.

`hermes`
`source ~/.bashrc`
`uv run hermes`

Optional polish:

- Custom icon:openProperties -> Change Iconand point it at an.icofile, such as the Hermes favicon from the repo.
- Pinned launcher:once the shortcut works, pin it to Start or Taskbar so
you do not have to browse for it again.

`.ico`

### Inside WSL with systemd (recommended)​

If you enabled systemd per the setup section above,hermes gatewayand the API server work the way they do on any Linux machine. Use the gateway setup wizard:

`hermes gateway`

```
hermes gateway setup
```

It will offer to install a systemd user unit so the gateway comes up automatically when WSL starts.

### Making WSL itself start on Windows login​

WSL's VM only stays alive while something is using it. To keep your gateway reachable without a terminal window open, boot a WSL process at Windows login via Task Scheduler:

- Trigger:At log on (your user).
- Action:Start a programProgram:C:\Windows\System32\wsl.exeArguments:-d Ubuntu --exec /bin/sh -c "sleep infinity"

- Program:C:\Windows\System32\wsl.exe
- Arguments:-d Ubuntu --exec /bin/sh -c "sleep infinity"

`C:\Windows\System32\wsl.exe`
`-d Ubuntu --exec /bin/sh -c "sleep infinity"`

That keeps the VM alive so the systemd-managed gateway stays running. On Windows 11, the newerwsl --install --no-launch+ auto-start flows also work; thesleep infinitytrick is the portable version.

`wsl --install --no-launch`
`sleep infinity`

## GPU passthrough (local models)​

WSL2 supportsNVIDIAGPUs natively since WSL kernel 5.10.43+ — install the standard NVIDIA driver on Windows (donotinstall a Linux NVIDIA driver inside WSL), andnvidia-smiinside WSL will see the GPU. From there, CUDA toolkits,torch,vllm,sglang, andllama-serverbuild against the real GPU as usual.

`nvidia-smi`
`torch`
`vllm`
`sglang`
`llama-server`

AMD ROCm and Intel Arc support inside WSL2 is still evolving and outside Hermes's test matrix — it may work with current drivers but we don't have a recipe to recommend.

If you're running aWindows-nativelocal-model server (Ollama for Windows, LM Studio) that already uses your GPU through Windows drivers, you don't need WSL GPU passthrough at all — just follow Case 1 above and hit it over the network from WSL.

## Common pitfalls​

"Connection refused" to my Windows-hosted Ollama / LM Studio.SeeWSL2 Networking. Ninety percent of the time the server is bound to127.0.0.1and needs0.0.0.0(Ollama:OLLAMA_HOST=0.0.0.0), or you're missing a firewall rule.

[WSL2 Networking](/docs/integrations/providers#wsl2-networking-windows-users)
`127.0.0.1`
`0.0.0.0`
`OLLAMA_HOST=0.0.0.0`

Massive slowness ongit status/hermes chatin a repo.You're probably working under/mnt/c/.... Move the repo to~/code/...(Linux side). Order-of-magnitude faster.

`git status`
`hermes chat`
`/mnt/c/...`
`~/code/...`

bad interpreter: /bin/bash^Mon scripts.CRLF line endings from a Windows editor.dos2unix script.sh, and setcore.autocrlf inputin your WSL git config.

`bad interpreter: /bin/bash^M`
`dos2unix script.sh`
`core.autocrlf input`

"UNC paths are not supported" warning from Windows binaries launched via MCP.Hermes's cwd is inside the Linux filesystem, and Windowscmd.exedoesn't know what to do with it. Start Hermes from/mnt/c/...for that session, or use a wrapper thatcds to a Windows-reachable path before invoking the Windows executable.

`cmd.exe`
`/mnt/c/...`
`cd`

Clock drift after sleep/hibernate.WSL2's clock can lag by minutes after the host resumes from sleep, which breaks anything cert-based (OAuth, HTTPS APIs). Fix it on demand:

```
sudo hwclock -s
```

Or installntpdateand run it at login.

`ntpdate`

DNS stops working after enabling mirrored mode, or when a VPN is connected.Mirrored mode proxies host network settings into WSL — if Windows DNS is funky (VPN split-tunnel, corporate resolver), WSL inherits that. Workaround: overrideresolv.confmanually (setgenerateResolvConf=falsein/etc/wsl.conf, then write your own/etc/resolv.confwith1.1.1.1or your VPN's DNS).

`resolv.conf`
`generateResolvConf=false`
`/etc/wsl.conf`
`/etc/resolv.conf`
`1.1.1.1`

hermesnot found after running the installer.The installer adds~/.local/binto your shell's PATH via~/.bashrc. You need tosource ~/.bashrc(or open a new terminal) for it to take effect in the current session.

`hermes`
`~/.local/bin`
`~/.bashrc`
`source ~/.bashrc`

Windows Defender is slow on WSL files.Defender scans files via the 9P bridge when accessed from Windows, which magnifies the slowness of/mnt/c-style cross-boundary access. If you only touch WSL files from inside WSL, this doesn't matter. If you use Windows tools against\\wsl$\...frequently, consider excluding the WSL distro path from real-time scanning.

`/mnt/c`
`\\wsl$\...`

Running out of disk.WSL2 stores its VM disk as a sparse VHDX under%LOCALAPPDATA%\Packages\.... It grows but doesn't auto-shrink when you delete files. To reclaim space:wsl --shutdown, then from an Admin PowerShell runOptimize-VHD -Path <path-to-ext4.vhdx> -Mode Full(requires Hyper-V tools) — or the simplerdiskpartpath documented on the WSL docs.

`%LOCALAPPDATA%\Packages\...`
`wsl --shutdown`
`Optimize-VHD -Path <path-to-ext4.vhdx> -Mode Full`
`diskpart`

## Where to go next​

- Installation— actual install steps (Linux/WSL2/Termux all use the same installer).
- Integrations → Providers → WSL2 Networking— the canonical networking deep-dive for local model servers.
- MCP guide → WSL → Windows Chrome— controlling your signed-in Windows Chrome from Hermes in WSL.
- Tool GatewayandWeb Dashboard— the long-lived services you'll most often want to expose from WSL to the rest of your network.

[Installation](/docs/getting-started/installation)
[Integrations → Providers → WSL2 Networking](/docs/integrations/providers#wsl2-networking-windows-users)
[MCP guide → WSL → Windows Chrome](/docs/guides/use-mcp-with-hermes#wsl2-bridge-hermes-in-wsl-to-windows-chrome)
[Tool Gateway](/docs/user-guide/features/tool-gateway)
[Web Dashboard](/docs/user-guide/features/web-dashboard)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/windows-wsl-quickstart.md)