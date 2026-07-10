---
layout: docs
title: "تنظیم Nix و NixOS"
permalink: /getting-started/nix-setup/
---

- 
- Getting Started
- Nix & NixOS Setup

# Nix & NixOS Setup

Nix and NixOS areTier 2 platforms. The flake and NixOS module documented here are maintained on a best-effort basis only. Commits tomainmay break these packages at any point in time.

[Tier 2 platforms](/docs/getting-started/platform-support#tier-2)
`main`

For a supported setup, use one of the standardinstallationpaths - either Docker or an FHS environment.

[installation](/docs/getting-started/installation)

Hermes Agent ships a Nix flake & a NixOS module.

| Level | Who it's for | What you get |
| --- | --- | --- |
| nix run/nix profile install | Any Nix user (macOS, Linux) | Pre-built binary with all deps — then use the standard CLI workflow |
| NixOS module (native) | NixOS server deployments | Declarative config, hardened systemd service, managed secrets |
| NixOS module (container) | Agents that need self-modification | Everything above, plus a persistent Ubuntu container where the agent canapt/pip/npm install |

`nix run`
`nix profile install`
`apt`
`pip`
`npm install`

Thecurl | bashinstaller manages Python, Node, and dependencies itself. The Nix flake replaces all of that — every Python dependency is a Nix derivation built byuv2nix, and runtime tools (Node.js, git, ripgrep, ffmpeg) are wrapped into the binary's PATH. There is no runtime pip, no venv activation, nonpm install.

`curl | bash`
[uv2nix](https://github.com/pyproject-nix/uv2nix)
`npm install`

For non-NixOS users, this only changes the install step. Everything after (hermes setup,hermes gateway install, config editing) works identically to the standard install.

`hermes setup`
`hermes gateway install`

For NixOS module users, the entire lifecycle is different: configuration lives inconfiguration.nix, secrets go through sops-nix/agenix, the service is a systemd unit, and CLI config commands are blocked. You manage hermes the same way you manage any other NixOS service.

`configuration.nix`

## Prerequisites​

- Nix with flakes enabled—Determinate Nixrecommended (enables flakes by default)
- API keysfor the services you want to use (at minimum: an OpenRouter or Anthropic key)

[Determinate Nix](https://install.determinate.systems)

## Quick Start (Any Nix User)​

No clone needed. Nix fetches, builds, and runs everything:

```
# Run the desktop appnix run github:NousResearch/hermes-agent#desktop# Or install persistentlynix profile install github:NousResearch/hermes-agent#desktop# run the tuinix run github:NousResearch/hermes-agent -- setupnix run github:NousResearch/hermes-agent -- --tui# or install it in your profilenix profile install github:NousResearch/hermes-agenthermes setuphermes --tui
```

Afternix profile install,hermes,hermes-agent, andhermes-acpare on your PATH. From here, the workflow is identical to thestandard installation—hermes setupwalks you through provider selection,hermes gateway installsets up a launchd (macOS) or systemd user service, and config lives in~/.hermes/.

`nix profile install`
`hermes`
`hermes-agent`
`hermes-acp`
[standard installation](/docs/getting-started/installation)
`hermes setup`
`hermes gateway install`
`~/.hermes/`

The default package includes ALL libraries hermes-agent might need. if you want a smaller variant, check the other flake outputs.

Thedefaultpackage adds ~700 MB to the closure. If you only need messaging platforms,#messagingadds just ~33 MB.

`default`
`#messaging`

```
git clone https://github.com/NousResearch/hermes-agent.gitcd hermes-agentnix develophermes setup
```

## NixOS Module​

The flake exportsnixosModules.default— a full NixOS service module that declaratively manages user creation, directories, config generation, secrets, documents, and service lifecycle.

`nixosModules.default`

This module requires NixOS. For non-NixOS systems (macOS, other Linux distros), usenix profile installand the standard CLI workflow above.

`nix profile install`

### Add the Flake Input​

```
# /etc/nixos/flake.nix (or your system flake){  inputs = {    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";    hermes-agent.url = "github:NousResearch/hermes-agent";  };  outputs = { nixpkgs, hermes-agent, ... }: {    nixosConfigurations.your-host = nixpkgs.lib.nixosSystem {      system = "x86_64-linux";      modules = [        hermes-agent.nixosModules.default        ./configuration.nix      ];    };  };}
```

### Minimal Configuration​

```
# configuration.nix{ config, ... }: {  services.hermes-agent = {    enable = true;    settings.model.default = "anthropic/claude-sonnet-4";    environmentFiles = [ config.sops.secrets."hermes-env".path ];    addToSystemPackages = true;  };}
```

That's it.nixos-rebuild switchcreates thehermesuser, generatesconfig.yaml, wires up secrets, and starts the gateway — a long-running service that connects the agent to messaging platforms (Telegram, Discord, etc.) and listens for incoming messages.

`nixos-rebuild switch`
`hermes`
`config.yaml`

TheenvironmentFilesline above assumes you havesops-nixoragenixconfigured. The file should contain at least one LLM provider key (e.g.,OPENROUTER_API_KEY=sk-or-...). SeeSecrets Managementfor full setup. If you don't have a secrets manager yet, you can use a plain file as a starting point — just ensure it's not world-readable:

`environmentFiles`
[sops-nix](https://github.com/Mic92/sops-nix)
[agenix](https://github.com/ryantm/agenix)
`OPENROUTER_API_KEY=sk-or-...`

```
echo "OPENROUTER_API_KEY=sk-or-your-key" | sudo install -m 0600 -o hermes /dev/stdin /var/lib/hermes/env
```

```
services.hermes-agent.environmentFiles = [ "/var/lib/hermes/env" ];
```

SettingaddToSystemPackages = truedoes two things: puts thehermesCLI on your system PATHandsetsHERMES_HOMEsystem-wide so the interactive CLI shares state (sessions, skills, cron) with the gateway service. Without it, runninghermesin your shell creates a separate~/.hermes/directory.

`addToSystemPackages = true`
`hermes`
`HERMES_HOME`
`hermes`
`~/.hermes/`

### Container-aware CLI​

Whencontainer.enable = trueandaddToSystemPackages = true,everyhermescommand on the host automatically routes into the managed container. This means your interactive CLI session runs inside the same environment as the gateway service — with access to all container-installed packages and tools.

`container.enable = true`
`addToSystemPackages = true`
`hermes`
- The routing is transparent:hermes chat,hermes sessions list,hermes version, etc. all exec into the container under the hood
- All CLI flags are forwarded as-is
- If the container isn't running, the CLI retries briefly (5s with a spinner for interactive use, 10s silently for scripts) then fails with a clear error — no silent fallback
- For developers working on the hermes codebase, setHERMES_DEV=1to bypass container routing and run the local checkout directly

`hermes chat`
`hermes sessions list`
`hermes version`
`HERMES_DEV=1`

Setcontainer.hostUsersto create a~/.hermessymlink to the service state directory, so the host CLI and the container share sessions, config, and memories:

`container.hostUsers`
`~/.hermes`

```
services.hermes-agent = {  container.enable = true;  container.hostUsers = [ "your-username" ];  addToSystemPackages = true;};
```

Users listed inhostUsersare automatically added to thehermesgroup for file permission access.

`hostUsers`
`hermes`

Podman users:The NixOS service runs the container as root. Docker users get access via thedockergroup socket, but Podman's rootful containers require sudo. Grant passwordless sudo for your container runtime:

`docker`

```
security.sudo.extraRules = [{  users = [ "your-username" ];  commands = [{    command = "/run/current-system/sw/bin/podman";    options = [ "NOPASSWD" ];  }];}];
```

The CLI auto-detects when sudo is needed and uses it transparently. Without this, you'll need to runsudo hermes chatmanually.

`sudo hermes chat`

### Verify It Works​

Afternixos-rebuild switch, check that the service is running:

`nixos-rebuild switch`

```
# Check service statussystemctl status hermes-agent# Watch logs (Ctrl+C to stop)journalctl -u hermes-agent -f# If addToSystemPackages is true, test the CLIhermes versionhermes config       # shows the generated config
```

### Choosing a Deployment Mode​

The module supports two modes, controlled bycontainer.enable:

`container.enable`

|  | Native(default) | Container |
| --- | --- | --- |
| How it runs | Hardened systemd service on the host | Persistent Ubuntu container with/nix/storebind-mounted |
| Security | NoNewPrivileges,ProtectSystem=strict,PrivateTmp | Container isolation, runs as unprivileged user inside |
| Agent can self-install packages | No — only tools on the Nix-provided PATH | Yes —apt,pip,npminstalls persist across restarts |
| Config surface | Same | Same |
| When to choose | Standard deployments, maximum security, reproducibility | Agent needs runtime package installation, mutable environment, experimental tools |

`/nix/store`
`NoNewPrivileges`
`ProtectSystem=strict`
`PrivateTmp`
`apt`
`pip`
`npm`

To enable container mode, add one line:

```
{  services.hermes-agent = {    enable = true;    container.enable = true;    # ... rest of config is identical  };}
```

Container mode auto-enablesvirtualisation.docker.enableviamkDefault. If you use Podman instead, setcontainer.backend = "podman"andvirtualisation.docker.enable = false.

`virtualisation.docker.enable`
`mkDefault`
`container.backend = "podman"`
`virtualisation.docker.enable = false`

## Configuration​

### Declarative Settings​

Thesettingsoption accepts an arbitrary attrset that is rendered asconfig.yaml. It supports deep merging across multiple module definitions (vialib.recursiveUpdate), so you can split config across files:

`settings`
`config.yaml`
`lib.recursiveUpdate`

```
# base.nixservices.hermes-agent.settings = {  model.default = "anthropic/claude-sonnet-4";  toolsets = [ "all" ];  terminal = { backend = "local"; timeout = 180; };};# personality.nixservices.hermes-agent.settings = {  display = { compact = false; personality = "kawaii"; };  memory = { memory_enabled = true; user_profile_enabled = true; };};
```

Both are deep-merged at evaluation time. Nix-declared keys always win over keys in an existingconfig.yamlon disk, butuser-added keys that Nix doesn't touch are preserved. This means if the agent or a manual edit adds keys likeskills.disabledorstreaming.enabled, they survivenixos-rebuild switch.

`config.yaml`
`skills.disabled`
`streaming.enabled`
`nixos-rebuild switch`

settings.model.defaultuses the model identifier your provider expects. WithOpenRouter(the default), these look like"anthropic/claude-sonnet-4"or"google/gemini-3-flash". If you're using a provider directly (Anthropic, OpenAI), setsettings.model.base_urlto point at their API and use their native model IDs (e.g.,"claude-sonnet-4-20250514"). When nobase_urlis set, Hermes defaults to OpenRouter.

`settings.model.default`
[OpenRouter](https://openrouter.ai)
`"anthropic/claude-sonnet-4"`
`"google/gemini-3-flash"`
`settings.model.base_url`
`"claude-sonnet-4-20250514"`
`base_url`

Runnix build .#configKeys && cat resultto see every leaf config key extracted from Python'sDEFAULT_CONFIG. You can paste your existingconfig.yamlinto thesettingsattrset — the structure maps 1:1.

`nix build .#configKeys && cat result`
`DEFAULT_CONFIG`
`config.yaml`
`settings`

```
{ config, ... }: {  services.hermes-agent = {    enable = true;    container.enable = true;    # ── Model ──────────────────────────────────────────────────────────    settings = {      model = {        base_url = "https://openrouter.ai/api/v1";        default = "anthropic/claude-opus-4.6";      };      toolsets = [ "all" ];      max_turns = 100;      terminal = { backend = "local"; cwd = "."; timeout = 180; };      compression = {        enabled = true;        threshold = 0.85;        summary_model = "google/gemini-3-flash-preview";      };      memory = { memory_enabled = true; user_profile_enabled = true; };      display = { compact = false; personality = "kawaii"; };      agent = { max_turns = 60; verbose = false; };    };    # ── Secrets ────────────────────────────────────────────────────────    environmentFiles = [ config.sops.secrets."hermes-env".path ];    # ── Documents ──────────────────────────────────────────────────────    documents = {      "USER.md" = ./documents/USER.md;    };    # ── MCP Servers ────────────────────────────────────────────────────    mcpServers.filesystem = {      command = "npx";      args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];    };    # ── Container options ──────────────────────────────────────────────    container = {      image = "ubuntu:24.04";      backend = "docker";      hostUsers = [ "your-username" ];      extraVolumes = [ "/home/user/projects:/projects:rw" ];      extraOptions = [ "--gpus" "all" ];    };    # ── Service tuning ─────────────────────────────────────────────────    addToSystemPackages = true;    extraArgs = [ "--verbose" ];    restart = "always";    restartSec = 5;  };}
```

### Escape Hatch: Bring Your Own Config​

If you'd rather manageconfig.yamlentirely outside Nix, useconfigFile:

`config.yaml`
`configFile`

```
services.hermes-agent.configFile = /etc/hermes/config.yaml;
```

This bypassessettingsentirely — no merge, no generation. The file is copied as-is to$HERMES_HOME/config.yamlon each activation.

`settings`
`$HERMES_HOME/config.yaml`

### Customization Cheatsheet​

Quick reference for the most common things Nix users want to customize:

| I want to... | Option | Example |
| --- | --- | --- |
| Change the LLM model | settings.model.default | "anthropic/claude-sonnet-4" |
| Use a different provider endpoint | settings.model.base_url | "https://openrouter.ai/api/v1" |
| Add API keys | environmentFiles | [ config.sops.secrets."hermes-env".path ] |
| Give the agent a personality | ${services.hermes-agent.stateDir}/.hermes/SOUL.md | manage the file directly |
| Add MCP tool servers | mcpServers.<name> | SeeMCP Servers |
| Enable Discord/Telegram/Slack | extraDependencyGroups | [ "messaging" ] |
| Mount host directories into container | container.extraVolumes | [ "/data:/data:rw" ] |
| Pass GPU access to container | container.extraOptions | [ "--gpus" "all" ] |
| Use Podman instead of Docker | container.backend | "podman" |
| Share state between host CLI and container | container.hostUsers | [ "sidbin" ] |
| Make extra tools available to the agent | extraPackages | [ pkgs.pandoc pkgs.imagemagick ] |
| Use a custom base image | container.image | "ubuntu:24.04" |
| Override the hermes package | package | inputs.hermes-agent.packages.${system}.default.override { ... } |
| Change state directory | stateDir | "/opt/hermes" |
| Set the agent's working directory | workingDirectory | "/home/user/projects" |

`settings.model.default`
`"anthropic/claude-sonnet-4"`
`settings.model.base_url`
`"https://openrouter.ai/api/v1"`
`environmentFiles`
`[ config.sops.secrets."hermes-env".path ]`
`${services.hermes-agent.stateDir}/.hermes/SOUL.md`
`mcpServers.<name>`
`extraDependencyGroups`
`[ "messaging" ]`
`container.extraVolumes`
`[ "/data:/data:rw" ]`
`container.extraOptions`
`[ "--gpus" "all" ]`
`container.backend`
`"podman"`
`container.hostUsers`
`[ "sidbin" ]`
`extraPackages`
`[ pkgs.pandoc pkgs.imagemagick ]`
`container.image`
`"ubuntu:24.04"`
`package`
`inputs.hermes-agent.packages.${system}.default.override { ... }`
`stateDir`
`"/opt/hermes"`
`workingDirectory`
`"/home/user/projects"`

## Secrets Management​

`settings`
`environment`

Values in Nix expressions end up in/nix/store, which is world-readable. Always useenvironmentFileswith a secrets manager.

`/nix/store`
`environmentFiles`

Bothenvironment(non-secret vars) andenvironmentFiles(secret files) are merged into$HERMES_HOME/.envat activation time (nixos-rebuild switch). Hermes reads this file on every startup, so changes take effect with asystemctl restart hermes-agent— no container recreation needed.

`environment`
`environmentFiles`
`$HERMES_HOME/.env`
`nixos-rebuild switch`
`systemctl restart hermes-agent`

### sops-nix​

```
{  sops = {    defaultSopsFile = ./secrets/hermes.yaml;    age.keyFile = "/home/user/.config/sops/age/keys.txt";    secrets."hermes-env" = { format = "yaml"; };  };  services.hermes-agent.environmentFiles = [    config.sops.secrets."hermes-env".path  ];}
```

The secrets file contains key-value pairs:

```
# secrets/hermes.yaml (encrypted with sops)hermes-env: |    OPENROUTER_API_KEY=sk-or-...    TELEGRAM_BOT_TOKEN=123456:ABC...    ANTHROPIC_API_KEY=sk-ant-...
```

### agenix​

```
{  age.secrets.hermes-env.file = ./secrets/hermes-env.age;  services.hermes-agent.environmentFiles = [    config.age.secrets.hermes-env.path  ];}
```

### OAuth / Auth Seeding​

For platforms requiring OAuth (e.g., Discord), useauthFileto seed credentials on first deploy:

`authFile`

```
{  services.hermes-agent = {    authFile = config.sops.secrets."hermes/auth.json".path;    # authFileForceOverwrite = true;  # overwrite on every activation  };}
```

The file is only copied ifauth.jsondoesn't already exist (unlessauthFileForceOverwrite = true). Runtime OAuth token refreshes are written to the state directory and preserved across rebuilds.

`auth.json`
`authFileForceOverwrite = true`

## Documents​

Thedocumentsoption installs files into the agent's working directory (theworkingDirectory, which the agent reads as its workspace). Hermes looks for specific filenames by convention:

`documents`
`workingDirectory`
- USER.md— context about the user the agent is interacting with.
- Any other files you place here are visible to the agent as workspace files.

`USER.md`

The agent identity file is separate: Hermes loads its primarySOUL.mdfrom$HERMES_HOME/SOUL.md, which in the NixOS module is${services.hermes-agent.stateDir}/.hermes/SOUL.md. PuttingSOUL.mdindocumentsonly creates a workspace file and will not replace the main persona file.

`SOUL.md`
`$HERMES_HOME/SOUL.md`
`${services.hermes-agent.stateDir}/.hermes/SOUL.md`
`SOUL.md`
`documents`

```
{  services.hermes-agent.documents = {    "USER.md" = ./documents/USER.md;  # path reference, copied from Nix store  };}
```

Values can be inline strings or path references. Files are installed on everynixos-rebuild switch.

`nixos-rebuild switch`

## MCP Servers​

ThemcpServersoption declaratively configuresMCP (Model Context Protocol)servers. Each server uses eitherstdio(local command) orHTTP(remote URL) transport.

`mcpServers`
[MCP (Model Context Protocol)](https://modelcontextprotocol.io)

### Stdio Transport (Local Servers)​

```
{  services.hermes-agent.mcpServers = {    filesystem = {      command = "npx";      args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];    };    github = {      command = "npx";      args = [ "-y" "@modelcontextprotocol/server-github" ];      env.GITHUB_PERSONAL_ACCESS_TOKEN = "\${GITHUB_TOKEN}"; # resolved from .env    };  };}
```

Environment variables inenvvalues are resolved from$HERMES_HOME/.envat runtime. UseenvironmentFilesto inject secrets — never put tokens directly in Nix config.

`env`
`$HERMES_HOME/.env`
`environmentFiles`

### HTTP Transport (Remote Servers)​

```
{  services.hermes-agent.mcpServers.remote-api = {    url = "https://mcp.example.com/v1/mcp";    headers.Authorization = "Bearer \${MCP_REMOTE_API_KEY}";    timeout = 180;  };}
```

### HTTP Transport with OAuth​

Setauth = "oauth"for servers using OAuth 2.1. Hermes implements the full PKCE flow — metadata discovery, dynamic client registration, token exchange, and automatic refresh.

`auth = "oauth"`

```
{  services.hermes-agent.mcpServers.my-oauth-server = {    url = "https://mcp.example.com/mcp";    auth = "oauth";  };}
```

Tokens are stored in$HERMES_HOME/mcp-tokens/<server-name>.jsonand persist across restarts and rebuilds.

`$HERMES_HOME/mcp-tokens/<server-name>.json`

The first OAuth authorization requires a browser-based consent flow. In a headless deployment, Hermes prints the authorization URL to stdout/logs instead of opening a browser.

Option A: Interactive bootstrap— run the flow once viadocker exec(container) orsudo -u hermes(native):

`docker exec`
`sudo -u hermes`

```
# Container modedocker exec -it hermes-agent \  hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauth# Native modesudo -u hermes HERMES_HOME=/var/lib/hermes/.hermes \  hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauth
```

The container uses--network=host, so the OAuth callback listener on127.0.0.1is reachable from the host browser.

`--network=host`
`127.0.0.1`

Option B: Pre-seed tokens— complete the flow on a workstation, then copy tokens:

```
hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauthscp ~/.hermes/mcp-tokens/my-oauth-server{,.client}.json \    server:/var/lib/hermes/.hermes/mcp-tokens/# Ensure: chown hermes:hermes, chmod 0600
```

### Sampling (Server-Initiated LLM Requests)​

Some MCP servers can request LLM completions from the agent:

```
{  services.hermes-agent.mcpServers.analysis = {    command = "npx";    args = [ "-y" "analysis-server" ];    sampling = {      enabled = true;      model = "google/gemini-3-flash";      max_tokens_cap = 4096;      timeout = 30;      max_rpm = 10;    };  };}
```

## Managed Mode​

When hermes runs via the NixOS module, the following CLI commands areblockedwith a descriptive error pointing you toconfiguration.nix:

`configuration.nix`

| Blocked command | Why |
| --- | --- |
| hermes setup | Config is declarative — editsettingsin your Nix config |
| hermes config edit | Config is generated fromsettings |
| hermes config set <key> <value> | Config is generated fromsettings |
| hermes gateway install | The systemd service is managed by NixOS |
| hermes gateway uninstall | The systemd service is managed by NixOS |

`hermes setup`
`settings`
`hermes config edit`
`settings`
`hermes config set <key> <value>`
`settings`
`hermes gateway install`
`hermes gateway uninstall`

This prevents drift between what Nix declares and what's on disk. Detection uses two signals:

1. HERMES_MANAGED=trueenvironment variable — set by the systemd service, visible to the gateway process
2. .managedmarker fileinHERMES_HOME— set by the activation script, visible to interactive shells (e.g.,docker exec -it hermes-agent hermes config set ...is also blocked)

`HERMES_MANAGED=true`
`.managed`
`HERMES_HOME`
`docker exec -it hermes-agent hermes config set ...`

To change configuration, edit your Nix config and runsudo nixos-rebuild switch.

`sudo nixos-rebuild switch`

## Container Architecture​

This section is only relevant if you're usingcontainer.enable = true. Skip it for native mode deployments.

`container.enable = true`

When container mode is enabled, hermes runs inside a persistent Ubuntu container with the Nix-built binary bind-mounted read-only from the host:

```
Host                                    Container────                                    ─────────/nix/store/...-hermes-agent-0.1.0  ──►  /nix/store/... (ro)~/.hermes -> /var/lib/hermes/.hermes       (symlink bridge, per hostUsers)/var/lib/hermes/                    ──►  /data/          (rw)  ├── current-package -> /nix/store/...    (symlink, updated each rebuild)  ├── .gc-root -> /nix/store/...           (prevents nix-collect-garbage)  ├── .container-identity                  (sha256 hash, triggers recreation)  ├── .hermes/                             (HERMES_HOME)  │   ├── .env                             (merged from environment + environmentFiles)  │   ├── config.yaml                      (Nix-generated, deep-merged by activation)  │   ├── .managed                         (marker file)  │   ├── .container-mode                  (routing metadata: backend, exec_user, etc.)  │   ├── state.db, sessions/, memories/   (runtime state)  │   └── mcp-tokens/                      (OAuth tokens for MCP servers)  ├── home/                                ──►  /home/hermes    (rw)  └── workspace/                           (agent working directory)      ├── SOUL.md                          (from documents option)      └── (agent-created files)Container writable layer (apt/pip/npm):   /usr, /usr/local, /tmp
```

The Nix-built binary works inside the Ubuntu container because/nix/storeis bind-mounted — it brings its own interpreter and all dependencies, so there's no reliance on the container's system libraries. The container entrypoint resolves through acurrent-packagesymlink:/data/current-package/bin/hermes gateway run --replace. Onnixos-rebuild switch, only the symlink is updated — the container keeps running.

`/nix/store`
`current-package`
`/data/current-package/bin/hermes gateway run --replace`
`nixos-rebuild switch`

### What Persists Across What​

| Event | Container recreated? | /data(state) | /home/hermes | Writable layer (apt/pip/npm) |
| --- | --- | --- | --- | --- |
| systemctl restart hermes-agent | No | Persists | Persists | Persists |
| nixos-rebuild switch(code change) | No (symlink updated) | Persists | Persists | Persists |
| Host reboot | No | Persists | Persists | Persists |
| nix-collect-garbage | No (GC root) | Persists | Persists | Persists |
| Image change (container.image) | Yes | Persists | Persists | Lost |
| Volume/options change | Yes | Persists | Persists | Lost |
| environment/environmentFileschange | No | Persists | Persists | Persists |

`/data`
`/home/hermes`
`apt`
`pip`
`npm`
`systemctl restart hermes-agent`
`nixos-rebuild switch`
`nix-collect-garbage`
`container.image`
`environment`
`environmentFiles`

The container is only recreated when itsidentity hashchanges. The hash covers: schema version, image,extraVolumes,extraOptions, and the entrypoint script. Changes to environment variables, settings, documents, or the hermes package itself donottrigger recreation.

`extraVolumes`
`extraOptions`

When the identity hash changes (image upgrade, new volumes, new container options), the container is destroyed and recreated from a fresh pull ofcontainer.image. Anyapt install,pip install, ornpm installpackages in the writable layer are lost. State in/dataand/home/hermesis preserved (these are bind mounts).

`container.image`
`apt install`
`pip install`
`npm install`
`/data`
`/home/hermes`

If the agent relies on specific packages, consider baking them into a custom image (container.image = "my-registry/hermes-base:latest") or scripting their installation in the agent's SOUL.md.

`container.image = "my-registry/hermes-base:latest"`

### GC Root Protection​

ThepreStartscript creates a GC root at${stateDir}/.gc-rootpointing to the current hermes package. This preventsnix-collect-garbagefrom removing the running binary. If the GC root somehow breaks, restarting the service recreates it.

`preStart`
`${stateDir}/.gc-root`
`nix-collect-garbage`

## Plugins​

The NixOS module supports declarative plugin installation — no imperativehermes plugins installneeded.

`hermes plugins install`

### Directory Plugins (extraPlugins)​

`extraPlugins`

For plugins that are just a source tree withplugin.yaml+__init__.py(e.g.,hermes-lcm):

`plugin.yaml`
`__init__.py`
[hermes-lcm](https://github.com/stephenschoettler/hermes-lcm)

```
services.hermes-agent.extraPlugins = [  (pkgs.fetchFromGitHub {    owner = "stephenschoettler";    repo = "hermes-lcm";    rev = "v0.7.0";    hash = "sha256-...";  })];
```

Plugins are symlinked into$HERMES_HOME/plugins/at activation time. Hermes discovers them via its normal directory scan. Removing a plugin from the list and runningnixos-rebuild switchremoves the symlink.

`$HERMES_HOME/plugins/`
`nixos-rebuild switch`

### Entry-Point Plugins (extraPythonPackages)​

`extraPythonPackages`

For pip-packaged plugins that register via[project.entry-points."hermes_agent.plugins"](e.g.,rtk-hermes):

`[project.entry-points."hermes_agent.plugins"]`
[rtk-hermes](https://github.com/ogallotti/rtk-hermes)

```
services.hermes-agent.extraPythonPackages = [  (pkgs.python312Packages.buildPythonPackage {    pname = "rtk-hermes";    version = "1.0.0";    src = pkgs.fetchFromGitHub {      owner = "ogallotti";      repo = "rtk-hermes";      rev = "v1.0.0";      hash = "sha256-...";    };    format = "pyproject";    build-system = [ pkgs.python312Packages.setuptools ];  })];
```

The package'ssite-packagesis added to PYTHONPATH in the hermes wrapper.importlib.metadatadiscovers the entry point at session start.

`site-packages`
`importlib.metadata`

### Optional Dependency Groups (extraDependencyGroups)​

`extraDependencyGroups`

For optional extras declared in hermes-agent'spyproject.toml, useextraDependencyGroupsto include them in the sealed venv at build time. This is required for any extra not in the default[all]set — on Nix, runtime installation into the read-only store is not possible.

`pyproject.toml`
`extraDependencyGroups`
`[all]`

```
# Enable Discord, Telegram, Slackservices.hermes-agent.extraDependencyGroups = [ "messaging" ];
```

```
# Enable a memory providerservices.hermes-agent = {  extraDependencyGroups = [ "hindsight" ];  settings.memory.provider = "hindsight";};
```

This is resolved by uv alongside core dependencies — no PYTHONPATH patching, no collision risk. Available groups:

| Group | What it enables |
| --- | --- |
| messaging | Discord, Telegram, Slack |
| matrix | Matrix/Element (mautrix with encryption; Linux only) |
| dingtalk | DingTalk |
| feishu | Feishu/Lark |
| voice | Local speech-to-text (faster-whisper) |
| edge-tts | Edge TTS provider |
| tts-premium | ElevenLabs TTS |
| anthropic | Native Anthropic SDK (not needed via OpenRouter) |
| bedrock | AWS Bedrock (boto3) |
| azure-identity | Azure Entra ID auth |
| honcho | Honcho memory provider |
| hindsight | Hindsight memory provider |
| modal | Modal terminal backend |
| daytona | Daytona terminal backend |
| exa | Exa web search |
| firecrawl | Firecrawl web search |
| fal | FAL image generation |

`messaging`
`matrix`
`dingtalk`
`feishu`
`voice`
`edge-tts`
`tts-premium`
`anthropic`
`bedrock`
`azure-identity`
`honcho`
`hindsight`
`modal`
`daytona`
`exa`
`firecrawl`
`fal`

Or use the pre-built#messagingor#fullflake packages instead of per-extra configuration (seeQuick Start).

`#messaging`
`#full`

When to use which:

| Need | Option |
| --- | --- |
| Enable a pyproject.toml optional extra | extraDependencyGroups |
| Add an external Python plugin not in pyproject.toml | extraPythonPackages |
| Add a system binary (pandoc, jq, etc.) | extraPackages |
| Add a directory-based plugin source tree | extraPlugins |

`extraDependencyGroups`
`extraPythonPackages`
`extraPackages`
`extraPlugins`

### Combining Both​

A directory plugin with third-party Python dependencies needs both options:

```
services.hermes-agent = {  extraPlugins = [ my-plugin-src ];          # plugin source  extraPythonPackages = [ pkgs.python312Packages.redis ];  # its Python dep  extraPackages = [ pkgs.redis ];            # system binary it needs};
```

### Using the Overlay​

External flakes can override the package directly:

```
{  inputs.hermes-agent.url = "github:NousResearch/hermes-agent";  outputs = { hermes-agent, nixpkgs, ... }: {    nixpkgs.overlays = [ hermes-agent.overlays.default ];    # Then:    #   pkgs.hermes-agent.override { extraPythonPackages = [...]; }    #   pkgs.hermes-agent.override { extraDependencyGroups = [ "hindsight" ]; }  };}
```

### Plugin Configuration​

Plugins still need to be enabled inconfig.yaml. Add them via the declarative settings:

`config.yaml`

```
services.hermes-agent.settings.plugins.enabled = [  "hermes-lcm"  "rtk-rewrite"];
```

A build-time collision check prevents plugin packages from shadowing core hermes dependencies. If a plugin provides a package already in the sealed venv,nixos-rebuildfails with a clear error.

`nixos-rebuild`

## Development​

### Dev Shell​

The flake provides a development shell with Python 3.12, uv, Node.js, and all runtime tools:

```
cd hermes-agentnix develop# Shell provides:#   - Python 3.12 + uv (deps installed into .venv on first entry)#   - Node.js 22, ripgrep, git, openssh, ffmpeg on PATH#   - Stamp-file optimization: re-entry is near-instant if deps haven't changedhermes setuphermes chat
```

### direnv (Recommended)​

The included.envrcactivates the dev shell automatically:

`.envrc`

```
cd hermes-agentdirenv allow    # one-time# Subsequent entries are near-instant (stamp file skips dep install)
```

### Flake Checks​

The flake includes build-time verification that runs in CI and locally:

```
# Run all checksnix flake check# Individual checksnix build .#checks.x86_64-linux.package-contents   # binaries exist + versionnix build .#checks.x86_64-linux.entry-points-sync  # pyproject.toml ↔ Nix package syncnix build .#checks.x86_64-linux.cli-commands        # gateway/config subcommandsnix build .#checks.x86_64-linux.managed-guard       # HERMES_MANAGED blocks mutationnix build .#checks.x86_64-linux.bundled-skills      # skills present in packagenix build .#checks.x86_64-linux.config-roundtrip    # merge script preserves user keys
```

| Check | What it tests |
| --- | --- |
| package-contents | hermesandhermes-agentbinaries exist andhermes versionruns |
| entry-points-sync | Every[project.scripts]entry inpyproject.tomlhas a wrapped binary in the Nix package |
| cli-commands | hermes --helpexposesgatewayandconfigsubcommands |
| managed-guard | HERMES_MANAGED=true hermes config set ...prints the NixOS error |
| bundled-skills | Skills directory exists, contains SKILL.md files,HERMES_BUNDLED_SKILLSis set in wrapper |
| config-roundtrip | 7 merge scenarios: fresh install, Nix override, user key preservation, mixed merge, MCP additive merge, nested deep merge, idempotency |

`package-contents`
`hermes`
`hermes-agent`
`hermes version`
`entry-points-sync`
`[project.scripts]`
`pyproject.toml`
`cli-commands`
`hermes --help`
`gateway`
`config`
`managed-guard`
`HERMES_MANAGED=true hermes config set ...`
`bundled-skills`
`HERMES_BUNDLED_SKILLS`
`config-roundtrip`

## Options Reference​

### Core​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| enable | bool | false | Enable the hermes-agent service |
| package | package | hermes-agent | The hermes-agent package to use |
| user | str | "hermes" | System user |
| group | str | "hermes" | System group |
| createUser | bool | true | Auto-create user/group |
| stateDir | str | "/var/lib/hermes" | State directory (HERMES_HOMEparent) |
| workingDirectory | str | "${stateDir}/workspace" | Agent working directory |
| addToSystemPackages | bool | false | AddhermesCLI to system PATH and setHERMES_HOMEsystem-wide |

`enable`
`bool`
`false`
`package`
`package`
`hermes-agent`
`user`
`str`
`"hermes"`
`group`
`str`
`"hermes"`
`createUser`
`bool`
`true`
`stateDir`
`str`
`"/var/lib/hermes"`
`HERMES_HOME`
`workingDirectory`
`str`
`"${stateDir}/workspace"`
`addToSystemPackages`
`bool`
`false`
`hermes`
`HERMES_HOME`

### Configuration​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| settings | attrs(deep-merged) | {} | Declarative config rendered asconfig.yaml. Supports arbitrary nesting; multiple definitions are merged vialib.recursiveUpdate |
| configFile | nullorpath | null | Path to an existingconfig.yaml. Overridessettingsentirely if set |

`settings`
`attrs`
`{}`
`config.yaml`
`lib.recursiveUpdate`
`configFile`
`null`
`path`
`null`
`config.yaml`
`settings`

### Secrets & Environment​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| environmentFiles | listOf str | [] | Paths to env files with secrets. Merged into$HERMES_HOME/.envat activation time |
| environment | attrsOf str | {} | Non-secret env vars.Visible in Nix store— do not put secrets here |
| authFile | nullorpath | null | OAuth credentials seed. Only copied on first deploy |
| authFileForceOverwrite | bool | false | Always overwriteauth.jsonfromauthFileon activation |

`environmentFiles`
`listOf str`
`[]`
`$HERMES_HOME/.env`
`environment`
`attrsOf str`
`{}`
`authFile`
`null`
`path`
`null`
`authFileForceOverwrite`
`bool`
`false`
`auth.json`
`authFile`

### Documents​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| documents | attrsOf (either str path) | {} | Workspace files. Keys are filenames, values are inline strings or paths. Installed intoworkingDirectoryon activation |

`documents`
`attrsOf (either str path)`
`{}`
`workingDirectory`

### MCP Servers​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| mcpServers | attrsOf submodule | {} | MCP server definitions, merged intosettings.mcp_servers |
| mcpServers.<name>.command | nullorstr | null | Server command (stdio transport) |
| mcpServers.<name>.args | listOf str | [] | Command arguments |
| mcpServers.<name>.env | attrsOf str | {} | Environment variables for the server process |
| mcpServers.<name>.url | nullorstr | null | Server endpoint URL (HTTP/StreamableHTTP transport) |
| mcpServers.<name>.headers | attrsOf str | {} | HTTP headers, e.g.Authorization |
| mcpServers.<name>.auth | nullor"oauth" | null | Authentication method."oauth"enables OAuth 2.1 PKCE |
| mcpServers.<name>.enabled | bool | true | Enable or disable this server |
| mcpServers.<name>.timeout | nullorint | null | Tool call timeout in seconds (default: 120) |
| mcpServers.<name>.connect_timeout | nullorint | null | Connection timeout in seconds (default: 60) |
| mcpServers.<name>.tools | nullorsubmodule | null | Tool filtering (include/excludelists) |
| mcpServers.<name>.sampling | nullorsubmodule | null | Sampling config for server-initiated LLM requests |

`mcpServers`
`attrsOf submodule`
`{}`
`settings.mcp_servers`
`mcpServers.<name>.command`
`null`
`str`
`null`
`mcpServers.<name>.args`
`listOf str`
`[]`
`mcpServers.<name>.env`
`attrsOf str`
`{}`
`mcpServers.<name>.url`
`null`
`str`
`null`
`mcpServers.<name>.headers`
`attrsOf str`
`{}`
`Authorization`
`mcpServers.<name>.auth`
`null`
`"oauth"`
`null`
`"oauth"`
`mcpServers.<name>.enabled`
`bool`
`true`
`mcpServers.<name>.timeout`
`null`
`int`
`null`
`mcpServers.<name>.connect_timeout`
`null`
`int`
`null`
`mcpServers.<name>.tools`
`null`
`submodule`
`null`
`include`
`exclude`
`mcpServers.<name>.sampling`
`null`
`submodule`
`null`

### Service Behavior​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| extraArgs | listOf str | [] | Extra args forhermes gateway |
| extraPackages | listOf package | [] | Extra packages available to the agent. Added to the hermes user's per-user profile so terminal commands, skills, and cron jobs all see them |
| extraPlugins | listOf package | [] | Directory plugin packages to symlink into$HERMES_HOME/plugins/. Each must containplugin.yaml |
| extraPythonPackages | listOf package | [] | Python packages added to PYTHONPATH for entry-point plugin discovery. Build withpython312Packages |
| extraDependencyGroups | listOf str | [] | pyproject.toml optional extras to include in the sealed venv (e.g.["hindsight"]). Resolved by uv — no collisions |
| restart | str | "always" | systemdRestart=policy |
| restartSec | int | 5 | systemdRestartSec=value |

`extraArgs`
`listOf str`
`[]`
`hermes gateway`
`extraPackages`
`listOf package`
`[]`
`extraPlugins`
`listOf package`
`[]`
`$HERMES_HOME/plugins/`
`plugin.yaml`
`extraPythonPackages`
`listOf package`
`[]`
`python312Packages`
`extraDependencyGroups`
`listOf str`
`[]`
`["hindsight"]`
`restart`
`str`
`"always"`
`Restart=`
`restartSec`
`int`
`5`
`RestartSec=`

### Container​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| container.enable | bool | false | Enable OCI container mode |
| container.backend | enum ["docker" "podman"] | "docker" | Container runtime |
| container.image | str | "ubuntu:24.04" | Base image (pulled at runtime) |
| container.extraVolumes | listOf str | [] | Extra volume mounts (host:container:mode) |
| container.extraOptions | listOf str | [] | Extra args passed todocker create |
| container.hostUsers | listOf str | [] | Interactive users who get a~/.hermessymlink to the service stateDir and are auto-added to thehermesgroup |

`container.enable`
`bool`
`false`
`container.backend`
`enum ["docker" "podman"]`
`"docker"`
`container.image`
`str`
`"ubuntu:24.04"`
`container.extraVolumes`
`listOf str`
`[]`
`host:container:mode`
`container.extraOptions`
`listOf str`
`[]`
`docker create`
`container.hostUsers`
`listOf str`
`[]`
`~/.hermes`
`hermes`

## Directory Layout​

### Native Mode​

```
/var/lib/hermes/                     # stateDir (owned by hermes:hermes, 0750)├── .hermes/                         # HERMES_HOME│   ├── config.yaml                  # Nix-generated (deep-merged each rebuild)│   ├── .managed                     # Marker: CLI config mutation blocked│   ├── .env                         # Merged from environment + environmentFiles│   ├── auth.json                    # OAuth credentials (seeded, then self-managed)│   ├── gateway.pid│   ├── state.db│   ├── mcp-tokens/                  # OAuth tokens for MCP servers│   ├── sessions/│   ├── memories/│   ├── skills/│   ├── cron/│   └── logs/├── home/                            # Agent HOME└── workspace/                       # Agent working directory    ├── SOUL.md                      # From documents option    └── (agent-created files)
```

### Container Mode​

Same layout, mounted into the container:

| Container path | Host path | Mode | Notes |
| --- | --- | --- | --- |
| /nix/store | /nix/store | ro | Hermes binary + all Nix deps |
| /data | /var/lib/hermes | rw | All state, config, workspace |
| /home/hermes | ${stateDir}/home | rw | Persistent agent home —pip install --user, tool caches |
| /usr,/usr/local,/tmp | (writable layer) | rw | apt/pip/npminstalls — persists across restarts, lost on recreation |

`/nix/store`
`/nix/store`
`ro`
`/data`
`/var/lib/hermes`
`rw`
`/home/hermes`
`${stateDir}/home`
`rw`
`pip install --user`
`/usr`
`/usr/local`
`/tmp`
`rw`
`apt`
`pip`
`npm`

## Updating​

```
# Update the flake input (run from the directory containing flake.nix)cd /etc/nixos && nix flake update hermes-agent# Rebuildsudo nixos-rebuild switch
```

In container mode, thecurrent-packagesymlink is updated and the agent picks up the new binary on restart. No container recreation, no loss of installed packages.

`current-package`

## Troubleshooting​

Alldockercommands below work the same withpodman. Substitute accordingly if you setcontainer.backend = "podman".

`docker`
`podman`
`container.backend = "podman"`

### Service Logs​

```
# Both modes use the same systemd unitjournalctl -u hermes-agent -f# Container mode: also available directlydocker logs -f hermes-agent
```

### Container Inspection​

```
systemctl status hermes-agentdocker ps -a --filter name=hermes-agentdocker inspect hermes-agent --format='{{.State.Status}}'docker exec -it hermes-agent bashdocker exec hermes-agent readlink /data/current-packagedocker exec hermes-agent cat /data/.container-identity
```

### Force Container Recreation​

If you need to reset the writable layer (fresh Ubuntu):

```
sudo systemctl stop hermes-agentdocker rm -f hermes-agentsudo rm /var/lib/hermes/.container-identitysudo systemctl start hermes-agent
```

### Verify Secrets Are Loaded​

If the agent starts but can't authenticate with the LLM provider, check that the.envfile was merged correctly:

`.env`

```
# Native modesudo -u hermes cat /var/lib/hermes/.hermes/.env# Container modedocker exec hermes-agent cat /data/.hermes/.env
```

### GC Root Verification​

```
nix-store --query --roots $(docker exec hermes-agent readlink /data/current-package)
```

### Common Issues​

| Symptom | Cause | Fix |
| --- | --- | --- |
| Cannot save configuration: managed by NixOS | CLI guards active | Editconfiguration.nixandnixos-rebuild switch |
| No adapter available for discord(or telegram/slack) | Messaging deps missing from the sealed Nix venv | Install#messagingvariant:nix profile install ...#messaging. For NixOS module:extraDependencyGroups = [ "messaging" ]. Checkjournalctl -u hermes-agentforFeatureUnavailableorrequirements not metfor the underlying error. |
| Container recreated unexpectedly | extraVolumes,extraOptions, orimagechanged | Expected — writable layer resets. Reinstall packages or use a custom image |
| hermes versionshows old version | Container not restarted | systemctl restart hermes-agent |
| Permission denied on/var/lib/hermes | State dir is0750 hermes:hermes | Usedocker execorsudo -u hermes |
| nix-collect-garbageremoved hermes | GC root missing | Restart the service (preStart recreates the GC root) |
| no container with name or ID "hermes-agent"(Podman) | Podman rootful container not visible to regular user | Add passwordless sudo for podman (seeContainer Modesection) |
| unable to find user hermes | Container still starting (entrypoint hasn't created user yet) | Wait a few seconds and retry — the CLI retries automatically |
| Tool added viaextraPackagesnot found in terminal | Requiresnixos-rebuild switchto update the per-user profile | Rebuild and restart:nixos-rebuild switch && systemctl restart hermes-agent |

`Cannot save configuration: managed by NixOS`
`configuration.nix`
`nixos-rebuild switch`
`No adapter available for discord`
`#messaging`
`nix profile install ...#messaging`
`extraDependencyGroups = [ "messaging" ]`
`journalctl -u hermes-agent`
`FeatureUnavailable`
`requirements not met`
`extraVolumes`
`extraOptions`
`image`
`hermes version`
`systemctl restart hermes-agent`
`/var/lib/hermes`
`0750 hermes:hermes`
`docker exec`
`sudo -u hermes`
`nix-collect-garbage`
`no container with name or ID "hermes-agent"`
`unable to find user hermes`
`extraPackages`
`nixos-rebuild switch`
`nixos-rebuild switch && systemctl restart hermes-agent`
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/nix-setup.md)