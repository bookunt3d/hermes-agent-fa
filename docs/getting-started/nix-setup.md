---
layout: docs
title: "تنظیم Nix و NixOS"
permalink: /docs/getting-started/nix-setup/
---

- 
- شروع کردن
- تنظیم Nix & NixOS

# تنظیم Nix & NixOS

Nix و NixOS پلتفرم‌های **Tier 2** هستند. Flake و ماژول NixOS مستند شده در اینجا فقط بر اساس بهترین تلاش نگهداری می‌شوند. Commitهای به `main` ممکن است در هر زمانی این بسته‌ها را خراب کنند.

[پلتفرم‌های Tier 2](/docs/getting-started/platform-support#tier-2)
`main`

برای نصب پشتیبانی‌شده، از یکی از مسیرهای [استاندارد نصب](/docs/getting-started/installation) استفاده کنید — Docker یا محیط FHS.

[نصب](/docs/getting-started/installation)

Hermes Agent یک Nix flake و یک ماژول NixOS ارسال می‌کند.

| سطح | برای چه کسی | چه چیزی دریافت می‌کنید |
| --- | --- | --- |
| `nix run` / `nix profile install` | هر کاربر Nix (macOS، Linux) | باینری از پیش ساخته‌شده با همه deps — سپس از گردش کار CLI استاندارد استفاده کنید |
| ماژول NixOS (بومی) | استقرارهای سرور NixOS | پیکربندی declarative، سرویس systemd hardened، رازهای مدیریت‌شده |
| ماژول NixOS (container) | Agentهایی که به self-modification نیاز دارند | همه موارد بالا، به علاوه یک container Ubuntu پایدار که agent می‌تواند `apt`/`pip`/`npm install` کند |

`nix run`
`nix profile install`
`apt`
`pip`
`npm install`

نصب‌کننده `curl | bash` خودش Python، Node و وابستگی‌ها را مدیریت می‌کند. Nix flake همه اینها را جایگزین می‌کند — هر وابستگی Python یک Nix derivation است که توسط [uv2nix](https://github.com/pyproject-nix/uv2nix) ساخته شده و ابزارهای runtime (Node.js، git، ripgrep، ffmpeg) در PATH باینری wrap شده‌اند. pip runtime، فعال‌سازی venv یا `npm install` وجود ندارد.

`curl | bash`
[uv2nix](https://github.com/pyproject-nix/uv2nix)
`npm install`

برای کاربران غیر-NixOS، این فقط مرحله نصب را تغییر می‌دهد. همه چیز پس از آن (`hermes setup`، `hermes gateway install`، ویرایش config) دقیقاً مانند نصب استاندارد کار می‌کند.

`hermes setup`
`hermes gateway install`

برای کاربران ماژول NixOS، کل چرخه حیات متفاوت است: پیکربندی در `configuration.nix` زندگی می‌کند، رازها از طریق sops-nix/agenix می‌روند، سرویس یک unit systemd است و دستورات CLI config مسدود هستند. Hermes را دقیقاً مانند هر سرویس NixOS دیگری مدیریت می‌کنید.

`configuration.nix`

## پیش‌نیازها​

- **Nix با flakes فعال** — [Determinate Nix](https://install.determinate.systems) توصیه می‌شود (flakes را به طور پیش‌فرض فعال می‌کند)
- **کلیدهای API** برای سرویس‌هایی که می‌خواهید استفاده کنید (حداقل: یک کلید OpenRouter یا Anthropic)

[Determinate Nix](https://install.determinate.systems)

## شروع سریع (هر کاربر Nix)​

Clone لازم نیست. Nix همه چیز را واکشی، build و اجرا می‌کند:

```
# Run the desktop appnix run github:NousResearch/hermes-agent#desktop# Or install persistentlynix profile install github:NousResearch/hermes-agent#desktop# run the tuinix run github:NousResearch/hermes-agent -- setupnix run github:NousResearch/hermes-agent -- --tui# or install it in your profilenix profile install github:NousResearch/hermes-agenthermes setuphermes --tui
```

پس از `nix profile install`، `hermes`، `hermes-agent` و `hermes-acp` در PATH شما هستند. از اینجا، گردش کار مشابه [نصب استاندارد](/docs/getting-started/installation) است — `hermes setup` شما را از انتخاب provider راهنمایی می‌کند، `hermes gateway install` یک سرویس launchd (macOS) یا systemd user راه‌اندازی می‌کند و پیکربندی در `~/.hermes/` زندگی می‌کند.

`nix profile install`
`hermes`
`hermes-agent`
`hermes-acp`
[نصب استاندارد](/docs/getting-started/installation)
`hermes setup`
`hermes gateway install`
`~/.hermes/`

بسته پیش‌فرض شامل **همه** کتابخانه‌هایی است که `hermes-agent` ممکن است به آن‌ها نیاز داشته باشد. اگر نسخه کوچک‌تری می‌خواهید، خروجی‌های دیگر flake را بررسی کنید.

بسته `default` حدود ۷۰۰ MB به closure اضافه می‌کند. اگر فقط به پلتفرم‌های پیام‌رسانی نیاز دارید، `#messaging` فقط حدود ۳۳ MB اضافه می‌کند.

`default`
`#messaging`

```
git clone https://github.com/NousResearch/hermes-agent.gitcd hermes-agentnix develophermes setup
```

## ماژول NixOS​

Flake خروجی `nixosModules.default` را صادر می‌کند — یک ماژول کامل سرویس NixOS که به طور declarative ایجاد کاربر، دایرکتوری‌ها، تولید پیکربندی، رازها، اسناد و چرخه حیات سرویس را مدیریت می‌کند.

`nixosModules.default`

این ماژول به NixOS نیاز دارد. برای سیستم‌های غیر-NixOS (macOS، distributionهای دیگر Linux)، از `nix profile install` و گردش کار CLI استاندارد بالا استفاده کنید.

`nix profile install`

### اضافه کردن Flake Input​

```
# /etc/nixos/flake.nix (or your system flake){  inputs = {    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";    hermes-agent.url = "github:NousResearch/hermes-agent";  };  outputs = { nixpkgs, hermes-agent, ... }: {    nixosConfigurations.your-host = nixpkgs.lib.nixosSystem {      system = "x86_64-linux";      modules = [        hermes-agent.nixosModules.default        ./configuration.nix      ];    };  };}
```

### پیکربندی حداقلی​

```
# configuration.nix{ config, ... }: {  services.hermes-agent = {    enable = true;    settings.model.default = "anthropic/claude-sonnet-4";    environmentFiles = [ config.sops.secrets."hermes-env".path ];    addToSystemPackages = true;  };}
```

همین. `nixos-rebuild switch` کاربر `hermes` را ایجاد، `config.yaml` را تولید، رازها را وصل و gateway را شروع می‌کند — یک سرویس طولانی‌مدت که agent را به پلتفرم‌های پیام‌رسانی (Telegram، Discord و غیره) متصل می‌کند و برای پیام‌های دریافتی گوش می‌دهد.

`nixos-rebuild switch`
`hermes`
`config.yaml`

خط `environmentFiles` بالا فرض می‌کند `sops-nix` یا `agenix` را پیکربندی کرده‌اید. فایل باید حداقل یک کلید provider LLM (مثلاً `OPENROUTER_API_KEY=sk-or-...`) داشته باشد. برای تنظیم کامل [مدیریت رازها](#secrets-management) را ببینید. اگر هنوز مدیر راز ندارید، می‌توانید از یک فایل معمولی به عنوان نقطه شروع استفاده کنید — فقط مطمئن شوید world-readable نیست:

`environmentFiles`
[sops-nix](https://github.com/Mic92/sops-nix)
[agenix](https://github.com/ryantm/agenix)
`OPENROUTER_API_KEY=sk-or-...`

```
echo "OPENROUTER_API_KEY=«redacted:sk-…»" | sudo install -m 0600 -o hermes /dev/stdin /var/lib/hermes/env
```

```
services.hermes-agent.environmentFiles = [ "/var/lib/hermes/env" ];
```

تنظیم `addToSystemPackages = true` دو کار انجام می‌دهد: CLI `hermes` را به PATH سیستم شما اضافه و `HERMES_HOME` را در سطح سیستم تنظیم می‌کند تا CLI تعاملی با سرویس gateway state (sessionها، skillها، cron) را به اشتراک بگذارد. بدون آن، اجرای `hermes` در shell شما یک دایرکتوری جداگانه `~/.hermes/` ایجاد می‌کند.

`addToSystemPackages = true`
`hermes`
`HERMES_HOME`
`hermes`
`~/.hermes/`

### CLI آگاه Container​

وقتی `container.enable = true` و `addToSystemPackages = true`، هر دستور `hermes` در هاست به طور خودکار به container مدیریت‌شده مسیریابی می‌شود. این به این معنی است که session CLI تعاملی شما دقیقاً در همان محیط سرویس gateway اجرا می‌شود — با دسترسی به همه بسته‌ها و ابزارهای نصب‌شده در container.

`container.enable = true`
`addToSystemPackages = true`
`hermes`
- مسیریابی شفاف است: `hermes chat`، `hermes sessions list`، `hermes version` و غیره همه در زیر پوشش exec به container می‌کنند
- همه flagهای CLI به همان شکل forward می‌شوند
- اگر container در حال اجرا نباشد، CLI به طور خلاصه تلاش می‌کند (۵ ثانیه با spinner برای استفاده تعاملی، ۱۰ ثانیه بی‌صدا برای اسکریپت‌ها) سپس با خطای واضح ناموفق می‌شود — بدون fallback بی‌صدا
- برای توسعه‌دهندگانی که روی کد `hermes` کار می‌کنند، `HERMES_DEV=1` را تنظیم کنید تا مسیریابی container را دور بزنید و checkout محلی را مستقیماً اجرا کنید

`hermes chat`
`hermes sessions list`
`hermes version`
`HERMES_DEV=1`

`container.hostUsers` را تنظیم کنید تا یک symlink `~/.hermes` به دایرکتوری state سرویس ایجاد شود، تا CLI هاست و container sessionها، پیکربندی و حافظه‌ها را به اشتراک بگذارند:

`container.hostUsers`
`~/.hermes`

```
services.hermes-agent = {  container.enable = true;  container.hostUsers = [ "your-username" ];  addToSystemPackages = true;};
```

کاربران فهرست‌شده در `hostUsers` به طور خودکار به گروه `hermes` برای دسترسی مجوز فایل اضافه می‌شوند.

`hostUsers`
`hermes`

**کاربران Podman:** سرویس NixOS container را به عنوان root اجرا می‌کند. کاربران Docker از طریق socket گروه `docker` دسترسی دارند، اما containerهای rootful Podman به sudo نیاز دارند. sudo بدون رمز عبور برای runtime container خود بدهید:

`docker`

```
security.sudo.extraRules = [{  users = [ "your-username" ];  commands = [{    command = "/run/current-system/sw/bin/podman";    options = [ "NOPASSWD" ];  }];}];
```

CLI به طور خودکار تشخیص می‌دهد چه زمانی sudo لازم است و به طور شفاف از آن استفاده می‌کند. بدون آن، باید `sudo hermes chat` را دستی اجرا کنید.

`sudo hermes chat`

### بررسی عملکرد​

پس از `nixos-rebuild switch`، بررسی کنید سرویس در حال اجراست:

`nixos-rebuild switch`

```
# Check service statussystemctl status hermes-agent# Watch logs (Ctrl+C to stop)journalctl -u hermes-agent -f# If addToSystemPackages is true, test the CLIhermes versionhermes config       # shows the generated config
```

### انتخاب حالت استقرار​

ماژول از دو حالت پشتیبانی می‌کند، کنترل شده توسط `container.enable`:

`container.enable`

|  | بومی (پیش‌فرض) | Container |
| --- | --- | --- |
| نحوه اجرا | سرویس systemd hardened در هاست | Container Ubuntu پایدار با bind-mount `/nix/store` |
| امنیت | `NoNewPrivileges`، `ProtectSystem=strict`، `PrivateTmp` | ایزوله container، اجرا به عنوان کاربر unprivileged داخل آن |
| Agent می‌تواند بسته‌ها را نصب کند | خیر — فقط ابزارها در PATH ارائه‌شده توسط Nix | بله — `apt`، `pip`، `npm` installها در ری‌بوت باقی می‌مانند |
| سطح پیکربندی | یکسان | یکسان |
| چه زمانی انتخاب کنید | استقرارهای استاندارد، حداکثر امنیت، تکرارپذیری | Agent به نصب بسته runtime، محیط mutable، ابزارهای تجربی نیاز دارد |

`/nix/store`
`NoNewPrivileges`
`ProtectSystem=strict`
`PrivateTmp`
`apt`
`pip`
`npm`

برای فعال‌سازی حالت container، یک خط اضافه کنید:

```
{  services.hermes-agent = {    enable = true;    container.enable = true;    # ... rest of config is identical  };}
```

حالت container به طور خودکار `virtualisation.docker.enable` را از طریق `mkDefault` فعال می‌کند. اگر به جای Podman استفاده می‌کنید، `container.backend = "podman"` و `virtualisation.docker.enable = false` را تنظیم کنید.

`virtualisation.docker.enable`
`mkDefault`
`container.backend = "podman"`
`virtualisation.docker.enable = false`

## پیکربندی​

### تنظیمات Declarative​

گزینه `settings` یک attrset دلخواه را می‌پذیرد که به عنوان `config.yaml` رندر می‌شود. از merge عمیق بین تعریف‌های ماژول متعدد (از طریق `lib.recursiveUpdate`) پشتیبانی می‌کند، بنابراین می‌توانید پیکربندی را بین فایل‌ها تقسیم کنید:

`settings`
`config.yaml`
`lib.recursiveUpdate`

```
# base.nixservices.hermes-agent.settings = {  model.default = "anthropic/claude-sonnet-4";  toolsets = [ "all" ];  terminal = { backend = "local"; timeout = 180; };};# personality.nixservices.hermes-agent.settings = {  display = { compact = false; personality = "kawaii"; };  memory = { memory_enabled = true; user_profile_enabled = true; };};
```

هر دو در زمان ارزیابی deep-merged می‌شوند. کلیدهای اعلام‌شده توسط Nix همیشه بر کلیدهای `config.yaml` موجود در دیسک اولویت دارند، اما کلیدهای اضافه‌شده توسط کاربر که Nix به آن‌ها دست نمی‌زند حفظ می‌شوند. این به این معنی است که اگر agent یا ویرایش دستی کلیدهایی مانند `skills.disabled` یا `streaming.enabled` اضافه کند، آن‌ها از `nixos-rebuild switch` زنده می‌مانند.

`config.yaml`
`skills.disabled`
`streaming.enabled`
`nixos-rebuild switch`

`settings.model.default` از شناسه مدلی استفاده می‌کند که provider شما انتظار دارد. با [OpenRouter](https://openrouter.ai) (پیش‌فرض)، اینها مانند `"anthropic/claude-sonnet-4"` یا `"google/gemini-3-flash"` به نظر می‌رسند. اگر مستقیماً از یک provider (Anthropic، OpenAI) استفاده می‌کنید، `settings.model.base_url` را به API آن‌ها اشاره دهید و از شناسه‌های مدل بومی آن‌ها استفاده کنید (مثلاً `"claude-sonnet-4-20250514"`). وقتی `base_url` تنظیم نشده، Hermes به OpenRouter پیش‌فرض می‌شود.

`settings.model.default`
[OpenRouter](https://openrouter.ai)
`"anthropic/claude-sonnet-4"`
`"google/gemini-3-flash"`
`settings.model.base_url`
`"claude-sonnet-4-20250514"`
`base_url`

`nix build .#configKeys && cat result` را اجرا کنید تا هر کلید config leaf استخراج‌شده از `DEFAULT_CONFIG` Python را ببینید. `config.yaml` موجود خود را می‌توانید در attrset `settings` paste کنید — ساختار ۱:۱ نقشه‌برداری می‌کند.

`nix build .#configKeys && cat result`
`DEFAULT_CONFIG`
`config.yaml`
`settings`

```
{ config, ... }: {  services.hermes-agent = {    enable = true;    container.enable = true;    # ── Model ──────────────────────────────────────────────────────────    settings = {      model = {        base_url = "https://openrouter.ai/api/v1";        default = "anthropic/claude-opus-4.6";      };      toolsets = [ "all" ];      max_turns = 100;      terminal = { backend = "local"; cwd = "."; timeout = 180; };      compression = {        enabled = true;        threshold = 0.85;        summary_model = "google/gemini-3-flash-preview";      };      memory = { memory_enabled = true; user_profile_enabled = true; };      display = { compact = false; personality = "kawaii"; };      agent = { max_turns = 60; verbose = false; };    };    # ── Secrets ────────────────────────────────────────────────────────    environmentFiles = [ config.sops.secrets."hermes-env".path ];    # ── Documents ──────────────────────────────────────────────────────    documents = {      "USER.md" = ./documents/USER.md;    };    # ── MCP Servers ────────────────────────────────────────────────────    mcpServers.filesystem = {      command = "npx";      args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];    };    # ── Container options ──────────────────────────────────────────────    container = {      image = "ubuntu:24.04";      backend = "docker";      hostUsers = [ "your-username" ];      extraVolumes = [ "/home/user/projects:/projects:rw" ];      extraOptions = [ "--gpus" "all" ];    };    # ── Service tuning ─────────────────────────────────────────────────    addToSystemPackages = true;    extraArgs = [ "--verbose" ];    restart = "always";    restartSec = 5;  };}
```

### فرار: پیکربندی خود را بیاورید​

اگر ترجیح می‌دهید `config.yaml` را کاملاً خارج از Nix مدیریت کنید، از `configFile` استفاده کنید:

`config.yaml`
`configFile`

```
services.hermes-agent.configFile = /etc/hermes/config.yaml;
```

این `settings` را کاملاً دور می‌زند — بدون merge، بدون تولید. فایل به همان شکل به `$HERMES_HOME/config.yaml` در هر فعال‌سازی کپی می‌شود.

`settings`
`$HERMES_HOME/config.yaml`

### مرجع سریع سفارشی‌سازی​

مرجع سریع رایج‌ترین چیزهایی که کاربران Nix می‌خواهند سفارشی کنند:

| می‌خواهم... | گزینه | مثال |
| --- | --- | --- |
| تغییر مدل LLM | `settings.model.default` | `"anthropic/claude-sonnet-4"` |
| استفاده از endpoint متفاوت provider | `settings.model.base_url` | `"https://openrouter.ai/api/v1"` |
| اضافه کردن کلیدهای API | `environmentFiles` | `[ config.sops.secrets."hermes-env".path ]` |
| دادن شخصیت به agent | `${services.hermes-agent.stateDir}/.hermes/SOUL.md` | فایل را مستقیماً مدیریت کنید |
| اضافه کردن سرورهای ابزار MCP | `mcpServers.<name>` | [سرورهای MCP](#mcp-servers) را ببینید |
| فعال‌سازی Discord/Telegram/Slack | `extraDependencyGroups` | `[ "messaging" ]` |
| Mount دایرکتوری‌های هاست به container | `container.extraVolumes` | `[ "/data:/data:rw" ]` |
| دسترسی GPU به container دادن | `container.extraOptions` | `[ "--gpus" "all" ]` |
| استفاده از Podman به جای Docker | `container.backend` | `"podman"` |
| به اشتراک گذاشتن state بین CLI هاست و container | `container.hostUsers` | `[ "sidbin" ]` |
| ابزارهای اضافی برای agent موجود کردن | `extraPackages` | `[ pkgs.pandoc pkgs.imagemagick ]` |
| استفاده از image پایه سفارشی | `container.image` | `"ubuntu:24.04"` |
| Override بسته hermes | `package` | `inputs.hermes-agent.packages.${system}.default.override { ... }` |
| تغییر دایرکتوری state | `stateDir` | `"/opt/hermes"` |
| تنظیم دایرکتوری کاری agent | `workingDirectory` | `"/home/user/projects"` |

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

## مدیریت رازها​

`settings`
`environment`

مقادیر در عبارات Nix در `/nix/store` قرار می‌گیرند که world-readable است. **همیشه** از `environmentFiles` با یک مدیر راز استفاده کنید.

`/nix/store`
`environmentFiles`

هر `environment` (متغیرهای غیرsecret) و `environmentFiles` (فایل‌های secret) در زمان فعال‌سازی (`nixos-rebuild switch`) در `$HERMES_HOME/.env` merge می‌شوند. Hermes این فایل را در هر شروع می‌خواند، بنابراین تغییرات با `systemctl restart hermes-agent` اعمال می‌شوند — نیازی به بازسازی container نیست.

`environment`
`environmentFiles`
`$HERMES_HOME/.env`
`nixos-rebuild switch`
`systemctl restart hermes-agent`

### sops-nix​

```
{  sops = {    defaultSopsFile = ./secrets/hermes.yaml;    age.keyFile = "/home/user/.config/sops/age/keys.txt";    secrets."hermes-env" = { format = "yaml"; };  };  services.hermes-agent.environmentFiles = [    config.sops.secrets."hermes-env".path  ];}
```

فایل رازها حاوی جفت‌های key-value است:

```
# secrets/hermes.yaml (encrypted with sops)hermes-env: |    OPENROUTER_API_KEY=sk-or-...    TELEGRAM_BOT_TOKEN=123456:ABC...    ANTHROPIC_API_KEY=sk-ant-...
```

### agenix​

```
{  age.secrets.hermes-env.file = ./secrets/hermes-env.age;  services.hermes-agent.environmentFiles = [    config.age.secrets.hermes-env.path  ];}
```

### OAuth / بذرگذاری Auth​

برای پلتفرم‌هایی که به OAuth نیاز دارند (مثلاً Discord)، از `authFile` برای بذرگذاری اعتبارنامه‌ها در اولین استقرار استفاده کنید:

`authFile`

```
{  services.hermes-agent = {    authFile = config.sops.secrets."hermes/auth.json".path;    # authFileForceOverwrite = true;  # overwrite on every activation  };}
```

فایل فقط اگر `auth.json` از قبل وجود نداشته باشد کپی می‌شود (مگر `authFileForceOverwrite = true`). تازه‌سازی‌های runtime OAuth token در دایرکتوری state نوشته می‌شوند و در rebuildها حفظ می‌شوند.

`auth.json`
`authFileForceOverwrite = true`

## اسناد​

گزینه `documents` فایل‌ها را در دایرکتوری کاری agent (`workingDirectory`، که agent آن را به عنوان workspace خود می‌خواند) نصب می‌کند. Hermes به طور قراردادی به نام‌های فایل خاص نگاه می‌کند:

`documents`
`workingDirectory`
- `USER.md` — context درباره کاربری که agent با او تعامل می‌کند.
- هر فایل دیگری که اینجا قرار می‌دهید به عنوان فایل workspace برای agent قابل مشاهده است.

`USER.md`

فایل هویت agent جداگانه است: Hermes فایل اصلی `SOUL.md` خود را از `$HERMES_HOME/SOUL.md` بارگذاری می‌کند، که در ماژول NixOS `${services.hermes-agent.stateDir}/.hermes/SOUL.md` است. قرار دادن `SOUL.md` در `documents` فقط یک فایل workspace ایجاد می‌کند و فایل شخصیت اصلی را جایگزین نمی‌کند.

`SOUL.md`
`$HERMES_HOME/SOUL.md`
`${services.hermes-agent.stateDir}/.hermes/SOUL.md`
`SOUL.md`
`documents`

```
{  services.hermes-agent.documents = {    "USER.md" = ./documents/USER.md;  # path reference, copied from Nix store  };}
```

مقادیر می‌توانند رشته‌های inline یا ارجاعات مسیر باشند. فایل‌ها در هر `nixos-rebuild switch` نصب می‌شوند.

`nixos-rebuild switch`

## سرورهای MCP​

گزینه `mcpServers` به طور declarative سرورهای **[MCP (Model Context Protocol)](https://modelcontextprotocol.io)** را پیکربندی می‌کند. هر سرور از حمل و نقل `stdio` (فرمان محلی) یا `HTTP` (URL از راه دور) استفاده می‌کند.

`mcpServers`
[MCP (Model Context Protocol)](https://modelcontextprotocol.io)

### حمل و نقل Stdio (سرورهای محلی)​

```
{  services.hermes-agent.mcpServers = {    filesystem = {      command = "npx";      args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];    };    github = {      command = "npx";      args = [ "-y" "@modelcontextprotocol/server-github" ];      env.GITHUB_PERSONAL_ACCESS_TOKEN = "\${GITHUB_TOKEN}"; # resolved from .env    };  };}
```

متغیرهای محیطی در مقادیر `env` در زمان runtime از `$HERMES_HOME/.env` resolve می‌شوند. از `environmentFiles` برای تزریق رازها استفاده کنید — **هرگز** توکن‌ها را مستقیماً در پیکربندی Nix قرار ندهید.

`env`
`$HERMES_HOME/.env`
`environmentFiles`

### حمل و نقل HTTP (سرورهای از راه دور)​

```
{  services.hermes-agent.mcpServers.remote-api = {    url = "https://mcp.example.com/v1/mcp";    headers.Authorization = "Bearer \${MCP_REMOTE_API_KEY}";    timeout = 180;  };}
```

### حمل و نقل HTTP با OAuth​

`auth = "oauth"` را برای سرورهایی که از OAuth 2.1 استفاده می‌کنند تنظیم کنید. Hermes کل flow PKCE را پیاده‌سازی می‌کند — کشف metadata، ثبت‌نام داینامیک client، تبادل token و تازه‌سازی خودکار.

`auth = "oauth"`

```
{  services.hermes-agent.mcpServers.my-oauth-server = {    url = "https://mcp.example.com/mcp";    auth = "oauth";  };}
```

توکن‌ها در `$HERMES_HOME/mcp-tokens/<server-name>.json` ذخیره می‌شوند و در ری‌بوت و rebuildها پایدار می‌مانند.

`$HERMES_HOME/mcp-tokens/<server-name>.json`

اولین مجوز OAuth به یک flow consent مبتنی بر مرورگر نیاز دارد. در یک استقرار headless، Hermes URL مجوز را به stdout/logs چاپ می‌کند به جای باز کردن مرورگر.

**گزینه A: bootstrap تعاملی** — flow را یک بار از طریق `docker exec` (container) یا `sudo -u hermes` (بومی) اجرا کنید:

`docker exec`
`sudo -u hermes`

```
# Container modedocker exec -it hermes-agent \  hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauth# Native modesudo -u hermes HERMES_HOME=/var/lib/hermes/.hermes \  hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauth
```

Container از `--network=host` استفاده می‌کند، بنابراین listener callback OAuth روی `127.0.0.1` از مرورگر هاست قابل دسترسی است.

`--network=host`
`127.0.0.1`

**گزینه B: بذرگذاری توکن‌ها از قبل** — flow را روی یک workstation کامل کنید، سپس توکن‌ها را کپی کنید:

```
hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauthscp ~/.hermes/mcp-tokens/my-oauth-server{,.client}.json \    server:/var/lib/hermes/.hermes/mcp-tokens/# Ensure: chown hermes:hermes, chmod 0600
```

### Sampling (درخواست‌های LLM آغاز شده توسط سرور)​

برخی سرورهای MCP می‌توانند completionهای LLM را از agent درخواست کنند:

```
{  services.hermes-agent.mcpServers.analysis = {    command = "npx";    args = [ "-y" "analysis-server" ];    sampling = {      enabled = true;      model = "google/gemini-3-flash";      max_tokens_cap = 4096;      timeout = 30;      max_rpm = 10;    };  };}
```

## حالت Managed​

وقتی Hermes از طریق ماژول NixOS اجرا می‌شود، دستورات CLI زیر با خطای توصیفی که به `configuration.nix` اشاره می‌کند **مسدود** هستند:

`configuration.nix`

| دستور مسدود | چرا |
| --- | --- |
| `hermes setup` | پیکربندی declarative است — `settings` را در پیکربندی Nix ویرایش کنید |
| `hermes config edit` | پیکربندی از `settings` تولید می‌شود |
| `hermes config set <key> <value>` | پیکربندی از `settings` تولید می‌شود |
| `hermes gateway install` | سرویس systemd توسط NixOS مدیریت می‌شود |
| `hermes gateway uninstall` | سرویس systemd توسط NixOS مدیریت می‌شود |

`hermes setup`
`settings`
`hermes config edit`
`settings`

`hermes config set <key> <value>`
`settings`
`hermes gateway install`
`hermes gateway uninstall`

این از انحراف بین آنچه Nix اعلام می‌کند و آنچه روی دیسک است جلوگیری می‌کند. تشخیص از دو سیگنال استفاده می‌کند:

1. متغیر محیطی `HERMES_MANAGED=true` — توسط سرویس systemd تنظیم شده، برای فرآیند gateway قابل مشاهده
2. فایل marker `.managed` در `HERMES_HOME` — توسط اسکریپت فعال‌سازی تنظیم شده، برای shellهای تعاملی قابل مشاهده (مثلاً `docker exec -it hermes-agent hermes config set ...` نیز مسدود است)

`HERMES_MANAGED=true`
`.managed`
`HERMES_HOME`
`docker exec -it hermes-agent hermes config set ...`

برای تغییر پیکربندی، پیکربندی Nix خود را ویرایش کنید و `sudo nixos-rebuild switch` اجرا کنید.

`sudo nixos-rebuild switch`

## معماری Container​

این بخش فقط زمانی مرتبط است که از `container.enable = true` استفاده می‌کنید. برای استقرارهای حالت بومی رد کنید.

`container.enable = true`

وقتی حالت container فعال می‌شود، Hermes داخل یک container Ubuntu پایدار با باینری ساخته‌شده توسط Nix که از هاست bind-mount شده فقط خواندنی اجرا می‌شود:

```
Host                                    Container────                                    ─────────/nix/store/...-hermes-agent-0.1.0  ──►  /nix/store/... (ro)~/.hermes -> /var/lib/hermes/.hermes       (symlink bridge, per hostUsers)/var/lib/hermes/                    ──►  /data/          (rw)  ├── current-package -> /nix/store/...    (symlink, updated each rebuild)  ├── .gc-root -> /nix/store/...           (prevents nix-collect-garbage)  ├── .container-identity                  (sha256 hash, triggers recreation)  ├── .hermes/                             (HERMES_HOME)  │   ├── .env                             (merged from environment + environmentFiles)  │   ├── config.yaml                      (Nix-generated, deep-merged by activation)  │   ├── .managed                         (marker file)  │   ├── .container-mode                  (routing metadata: backend, exec_user, etc.)  │   ├── state.db, sessions/, memories/   (runtime state)  │   └── mcp-tokens/                      (OAuth tokens for MCP servers)  ├── home/                                ──►  /home/hermes    (rw)  └── workspace/                           (agent working directory)      ├── SOUL.md                          (from documents option)      └── (agent-created files)Container writable layer (apt/pip/npm):   /usr, /usr/local, /tmp
```

باینری ساخته‌شده توسط Nix داخل container Ubuntu کار می‌کند زیرا `/nix/store` bind-mount شده — خودش interpreter و همه وابستگی‌ها را می‌آورد، بنابراین به کتابخانه‌های سیستم container وابسته نیست. Entry point container از طریق symlink `current-package` resolve می‌شود: `/data/current-package/bin/hermes gateway run --replace`. در `nixos-rebuild switch`، فقط symlink به‌روزرسانی می‌شود — container به اجرا ادامه می‌دهد.

`/nix/store`
`current-package`
`/data/current-package/bin/hermes gateway run --replace`
`nixos-rebuild switch`

### چه چیزی چه چیزی را حفظ می‌کند​

| رویداد | Container بازسازی می‌شود؟ | `/data` (state) | `/home/hermes` | لایه writable (`apt`/`pip`/`npm`) |
| --- | --- | --- | --- | --- |
| `systemctl restart hermes-agent` | خیر | پایدار | پایدار | پایدار |
| `nixos-rebuild switch` (تغییر کد) | خیر (symlink به‌روزرسانی) | پایدار | پایدار | پایدار |
| ری‌بوت هاست | خیر | پایدار | پایدار | پایدار |
| `nix-collect-garbage` | خیر (GC root) | پایدار | پایدار | پایدار |
| تغییر image (`container.image`) | بله | پایدار | پایدار | از دست رفته |
| تغییر volume/options | بله | پایدار | پایدار | از دست رفته |
| تغییر `environment`/`environmentFiles` | خیر | پایدار | پایدار | پایدار |

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

Container فقط وقتی بازسازی می‌شود که **hash identity** آن تغییر کند. Hash شامل: نسخه schema، image، `extraVolumes`، `extraOptions` و اسکریپت entry point است. تغییرات متغیرهای محیطی، settings، documents یا خود بسته hermes **بازسازی را trigger نمی‌کنند**.

`extraVolumes`
`extraOptions`

وقتی hash identity تغییر می‌کند (ارتقای image، volumeهای جدید، container options جدید)، container نابود و از pull تازه `container.image` بازسازی می‌شود. هر بسته `apt install`، `pip install` یا `npm install` در لایه writable از دست می‌رود. State در `/data` و `/home/hermes` حفظ می‌شود (اینها bind mount هستند).

`container.image`
`apt install`
`pip install`
`npm install`
`/data`
`/home/hermes`

اگر agent به بسته‌های خاصی وابسته است، آن‌ها را در یک image سفارشی (`container.image = "my-registry/hermes-base:latest"`) bake کنید یا نصب آن‌ها را در SOUL.md agent اسکریپت کنید.

`container.image = "my-registry/hermes-base:latest"`

### محافظت GC Root​

اسکریپت `preStart` یک GC root در `${stateDir}/.gc-root` ایجاد می‌کند که به بسته فعلی hermes اشاره می‌کند. این جلوگیری می‌کند `nix-collect-garbage` باینری در حال اجرا را حذف کند. اگر GC root به نحوی خراب شود، بازنشانی سرویس آن را بازسازی می‌کند.

`preStart`
`${stateDir}/.gc-root`
`nix-collect-garbage`

## پلاگین‌ها​

ماژول NixOS از نصب declarative پلاگین پشتیبانی می‌کند — نیازی به نصب امری `hermes plugins install` نیست.

`hermes plugins install`

### پلاگین‌های دایرکتوری (extraPlugins)​

`extraPlugins`

برای پلاگین‌هایی که فقط یک درخت منبع با `plugin.yaml` + `__init__.py` هستند (مثلاً [hermes-lcm](https://github.com/stephenschoettler/hermes-lcm)):

`plugin.yaml`
`__init__.py`

```
services.hermes-agent.extraPlugins = [  (pkgs.fetchFromGitHub {    owner = "stephenschoettler";    repo = "hermes-lcm";    rev = "v0.7.0";    hash = "sha256-...";  })];
```

پلاگین‌ها در زمان فعال‌سازی به `$HERMES_HOME/plugins/` symlink می‌شوند. Hermes آن‌ها را از طریق اسکان دایرکتوری عادی خود کشف می‌کند. حذف پلاگین از لیست و اجرای `nixos-rebuild switch` symlink را حذف می‌کند.

`$HERMES_HOME/plugins/`
`nixos-rebuild switch`

### پلاگین‌های Entry-Point (extraPythonPackages)​

`extraPythonPackages`

برای پلاگین‌های pip-packaged که از طریق `[project.entry-points."hermes_agent.plugins"]` ثبت‌نام می‌کنند (مثلاً [rtk-hermes](https://github.com/ogallotti/rtk-hermes)):

`[project.entry-points."hermes_agent.plugins"]`

```
services.hermes-agent.extraPythonPackages = [  (pkgs.python312Packages.buildPythonPackage {    pname = "rtk-hermes";    version = "1.0.0";    src = pkgs.fetchFromGitHub {      owner = "ogallotti";      repo = "rtk-hermes";      rev = "v1.0.0";      hash = "sha256-...";    };    format = "pyproject";    build-system = [ pkgs.python312Packages.setuptools ];  })];
```

`site-packages` بسته به PYTHONPATH در wrapper hermes اضافه می‌شود. `importlib.metadata` entry point را در شروع session کشف می‌کند.

`site-packages`
`importlib.metadata`

### گروه‌های وابستگی اختیاری (extraDependencyGroups)​

`extraDependencyGroups`

برای extras اختیاری اعلام‌شده در `pyproject.toml` hermes-agent، از `extraDependencyGroups` استفاده کنید تا آن‌ها را در venv sealed در زمان build وارد کنید. این برای هر extra که در مجموعه پیش‌فرض `[all]` نیست لازم است — در Nix، نصب runtime در store فقط خواندنی ممکن نیست.

`pyproject.toml`
`extraDependencyGroups`
`[all]`

```
# Enable Discord, Telegram, Slackservices.hermes-agent.extraDependencyGroups = [ "messaging" ];
```

```
# Enable a memory providerservices.hermes-agent = {  extraDependencyGroups = [ "hindsight" ];  settings.memory.provider = "hindsight";};
```

این توسط uv در کنار وابستگی‌های core resolve می‌شود — بدون patch کردن PYTHONPATH، بدون خطر تداخل. گروه‌های موجود:

| گروه | چه چیزی فعال می‌کند |
| --- | --- |
| `messaging` | Discord، Telegram، Slack |
| `matrix` | Matrix/Element (mautrix با رمزنگاری؛ فقط Linux) |
| `dingtalk` | DingTalk |
| `feishu` | Feishu/Lark |
| `voice` | speech-to-text محلی (faster-whisper) |
| `edge-tts` | ارائه‌دهنده Edge TTS |
| `tts-premium` | ElevenLabs TTS |
| `anthropic` | SDK بومی Anthropic (از طریق OpenRouter لازم نیست) |
| `bedrock` | AWS Bedrock (boto3) |
| `azure-identity` | احراز هویت Azure Entra ID |
| `honcho` | ارائه‌دهنده حافظه Honcho |
| `hindsight` | ارائه‌دهنده حافظه Hindsight |
| `modal` | backend ترمinal Modal |
| `daytona` | backend ترمinal Daytona |
| `exa` | جستجوی وب Exa |
| `firecrawl` | جستجوی وب Firecrawl |
| `fal` | تولید تصویر FAL |

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

یا از بسته‌های از پیش ساخته `#messaging` یا `#full` flake به جای پیکربندی به ازای هر extra استفاده کنید ([شروع سریع](#quick-start-any-nix-user)).

`#messaging`
`#full`

**چه زمانی از کدام استفاده کنید:**

| نیاز | گزینه |
| --- | --- |
| فعال‌سازی یک extra اختیاری pyproject.toml | `extraDependencyGroups` |
| اضافه کردن یک پلاگین Python خارجی که در pyproject.toml نیست | `extraPythonPackages` |
| اضافه کردن یک باینری سیستم (pandoc، jq و غیره) | `extraPackages` |
| اضافه کردن یک درخت منبع پلاگین مبتنی بر دایرکتوری | `extraPlugins` |

`extraDependencyGroups`
`extraPythonPackages`
`extraPackages`
`extraPlugins`

### ترکیب هر دو​

یک پلاگین دایرکتوری با وابستگی‌های Python شخص ثالث به هر دو گزینه نیاز دارد:

```
services.hermes-agent = {  extraPlugins = [ my-plugin-src ];          # plugin source  extraPythonPackages = [ pkgs.python312Packages.redis ];  # its Python dep  extraPackages = [ pkgs.redis ];            # system binary it needs};
```

### استفاده از Overlay​

Flakeهای خارجی می‌توانند بسته را مستقیماً override کنند:

```
{  inputs.hermes-agent.url = "github:NousResearch/hermes-agent";  outputs = { hermes-agent, nixpkgs, ... }: {    nixpkgs.overlays = [ hermes-agent.overlays.default ];    # Then:    #   pkgs.hermes-agent.override { extraPythonPackages = [...]; }    #   pkgs.hermes-agent.override { extraDependencyGroups = [ "hindsight" ]; }  };}
```

### پیکربندی پلاگین​

پلاگین‌ها همچنان باید در `config.yaml` فعال شوند. آن‌ها را از طریق تنظیمات declarative اضافه کنید:

`config.yaml`

```
services.hermes-agent.settings.plugins.enabled = [  "hermes-lcm"  "rtk-rewrite"];
```

یک بررسی تداخل زمان build جلوگیری می‌کند بسته‌های پلاگین وابستگی‌های core hermes را سایه نزنند. اگر پلاگینی بسته‌ای ارائه دهد که در venv sealed از قبل موجود است، `nixos-rebuild` با خطای واضح ناموفق می‌شود.

`nixos-rebuild`

## توسعه​

### Dev Shell​

Flake یک dev shell با Python 3.12، uv، Node.js و همه ابزارهای runtime فراهم می‌کند:

```
cd hermes-agentnix develop# Shell provides:#   - Python 3.12 + uv (deps installed into .venv on first entry)#   - Node.js 22, ripgrep, git, openssh, ffmpeg on PATH#   - Stamp-file optimization: re-entry is near-instant if deps haven't changedhermes setuphermes chat
```

### direnv (توصیه شده)​

`.envrc` موجود dev shell را به طور خودکار فعال می‌کند:

`.envrc`

```
cd hermes-agentdirenv allow    # one-time# Subsequent entries are near-instant (stamp file skips dep install)
```

### بررسی‌های Flake​

Flake شامل تأیید زمان build است که در CI و به طور محلی اجرا می‌شود:

```
# Run all checksnix flake check# Individual checksnix build .#checks.x86_64-linux.package-contents   # binaries exist + versionnix build .#checks.x86_64-linux.entry-points-sync  # pyproject.toml ↔ Nix package syncnix build .#checks.x86_64-linux.cli-commands        # gateway/config subcommandsnix build .#checks.x86_64-linux.managed-guard       # HERMES_MANAGED blocks mutationnix build .#checks.x86_64-linux.bundled-skills      # skills present in packagenix build .#checks.x86_64-linux.config-roundtrip    # merge script preserves user keys
```

| بررسی | چه چیزی تست می‌کند |
| --- | --- |
| `package-contents` | باینری‌های `hermes` و `hermes-agent` موجود هستند و `hermes version` اجرا می‌شود |
| `entry-points-sync` | هر entry `[project.scripts]` در `pyproject.toml` باینری wrap شده در بسته Nix دارد |
| `cli-commands` | `hermes --help` زیردستورات `gateway` و `config` را نشان می‌دهد |
| `managed-guard` | `HERMES_MANAGED=true hermes config set ...` خطای NixOS را چاپ می‌کند |
| `bundled-skills` | دایرکتوری skillها موجود است، فایل‌های SKILL.md دارد، `HERMES_BUNDLED_SKILLS` در wrapper تنظیم شده |
| `config-roundtrip` | ۷ سناریو merge: نصب تازه، override Nix، حفظ کلید کاربر، merge مختلط، merge افزایشی MCP، merge عمیق تو در تو، idempotency |

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

## مرجع گزینه‌ها​

### Core​

| گزینه | نوع | پیش‌فرض | توضیح |
| --- | --- | --- | --- |
| `enable` | bool | `false` | فعال‌سازی سرویس hermes-agent |
| `package` | package | `hermes-agent` | بسته hermes-agent مورد استفاده |
| `user` | str | `"hermes"` | کاربر سیستم |
| `group` | str | `"hermes"` | گروه سیستم |
| `createUser` | bool | `true` | ایجاد خودکار کاربر/گروه |
| `stateDir` | str | `"/var/lib/hermes"` | دایرکتوری state (والد `HERMES_HOME`) |
| `workingDirectory` | str | `"${stateDir}/workspace"` | دایرکتوری کاری agent |
| `addToSystemPackages` | bool | `false` | اضافه کردن CLI `hermes` به PATH سیستم و تنظیم `HERMES_HOME` در سطح سیستم |

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

### پیکربندی​

| گزینه | نوع | پیش‌فرض | توضیح |
| --- | --- | --- | --- |
| `settings` | attrs (deep-merged) | `{}` | پیکربندی declarative به عنوان `config.yaml` رندر می‌شود. از nesting دلخواه پشتیبانی می‌کند؛ تعریف‌های متعدد از طریق `lib.recursiveUpdate` merge می‌شوند |
| `configFile` | null یا path | `null` | مسیر به یک `config.yaml` موجود. اگر تنظیم شود `settings` را کاملاً override می‌کند |

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

### رازها و محیط​

| گزینه | نوع | پیش‌فرض | توضیح |
| --- | --- | --- | --- |
| `environmentFiles` | listOf str | `[]` | مسیرها به فایل‌های env با رازها. در زمان فعال‌سازی در `$HERMES_HOME/.env` merge می‌شوند |
| `environment` | attrsOf str | `{}` | متغیرهای env غیرsecret. **در Nix store قابل مشاهده** — رازها را اینجا قرار ندهید |
| `authFile` | null یا path | `null` | بذرگذاری اعتبارنامه‌های OAuth. فقط در اولین استقرار کپی می‌شود |
| `authFileForceOverwrite` | bool | `false` | همیشه `auth.json` از `authFile` در فعال‌سازی بازنویسی کنید |

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

### اسناد​

| گزینه | نوع | پیش‌فرض | توضیح |
| --- | --- | --- | --- |
| `documents` | attrsOf (either str path) | `{}` | فایل‌های workspace. کلیدها نام فایل‌ها، مقادیر رشته‌های inline یا مسیرها هستند. در `workingDirectory` در فعال‌سازی نصب می‌شوند |

`documents`
`attrsOf (either str path)`
`{}`
`workingDirectory`

### سرورهای MCP​

| گزینه | نوع | پیش‌فرض | توضیح |
| --- | --- | --- | --- |
| `mcpServers` | attrsOf submodule | `{}` | تعریف‌های سرور MCP، در `settings.mcp_servers` merge می‌شوند |
| `mcpServers.<name>.command` | null یا str | `null` | فرمان سرور (حمل و نقل stdio) |
| `mcpServers.<name>.args` | listOf str | `[]` | آرگومان‌های فرمان |
| `mcpServers.<name>.env` | attrsOf str | `{}` | متغیرهای محیطی برای فرآیند سرور |
| `mcpServers.<name>.url` | null یا str | `null` | URL endpoint سرور (حمل و نقل HTTP/StreamableHTTP) |
| `mcpServers.<name>.headers` | attrsOf str | `{}` | هدرهای HTTP، مثلاً `Authorization` |
| `mcpServers.<name>.auth` | null یا `"oauth"` | `null` | روش احراز هویت. `"oauth"` OAuth 2.1 PKCE را فعال می‌کند |
| `mcpServers.<name>.enabled` | bool | `true` | فعال یا غیرفعال کردن این سرور |
| `mcpServers.<name>.timeout` | null یا int | `null` | timeout فراخوانی ابزار به ثانیه (پیش‌فرض: ۱۲۰) |
| `mcpServers.<name>.connect_timeout` | null یا int | `null` | timeout اتصال به ثانیه (پیش‌فرض: ۶۰) |
| `mcpServers.<name>.tools` | null یا submodule | `null` | فیلتر کردن ابزار (لیست‌های include/exclude) |
| `mcpServers.<name>.sampling` | null یا submodule | `null` | پیکربندی sampling برای درخواست‌های LLM آغاز شده توسط سرور |

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

### رفتار سرویس​

| گزینه | نوع | پیش‌فرض | توضیح |
| --- | --- | --- | --- |
| `extraArgs` | listOf str | `[]` | آرگومان‌های اضافی برای `hermes gateway` |
| `extraPackages` | listOf package | `[]` | بسته‌های اضافی در دسترس agent. به پروفایل per-user کاربر hermes اضافه می‌شوند تا فرمان‌های ترمinal، skillها و cron jobها همه آن‌ها را ببینند |
| `extraPlugins` | listOf package | `[]` | بسته‌های پلاگین دایرکتوری برای symlink به `$HERMES_HOME/plugins/`. هر کدام باید `plugin.yaml` داشته باشند |
| `extraPythonPackages` | listOf package | `[]` | بسته‌های Python اضافه‌شده به PYTHONPATH برای کشف پلاگین entry-point. با `python312Packages` build کنید |
| `extraDependencyGroups` | listOf str | `[]` | extras اختیاری pyproject.toml برای وارد کردن در venv sealed (مثلاً `["hindsight"]`). توسط uv resolve می‌شود — بدون تداخل |
| `restart` | str | `"always"` | سیاست `Restart=` systemd |
| `restartSec` | int | `5` | مقدار `RestartSec=` systemd |

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

| گزینه | نوع | پیش‌فرض | توضیح |
| --- | --- | --- | --- |
| `container.enable` | bool | `false` | فعال‌سازی حالت container OCI |
| `container.backend` | enum `["docker" "podman"]` | `"docker"` | Runtime container |
| `container.image` | str | `"ubuntu:24.04"` | Image پایه (در runtime pull می‌شود) |
| `container.extraVolumes` | listOf str | `[]` | mount volume اضافی (host:container:mode) |
| `container.extraOptions` | listOf str | `[]` | آرگومان‌های اضافی ارسال‌شده به `docker create` |
| `container.hostUsers` | listOf str | `[]` | کاربران تعاملی که symlink `~/.hermes` به stateDir سرویس دریافت می‌کنند و به طور خودکار به گروه `hermes` اضافه می‌شوند |

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

## چیدمان دایرکتوری​

### حالت بومی​

```
/var/lib/hermes/                     # stateDir (owned by hermes:hermes, 0750)├── .hermes/                         # HERMES_HOME│   ├── config.yaml                  # Nix-generated (deep-merged each rebuild)│   ├── .managed                     # Marker: CLI config mutation blocked│   ├── .env                         # Merged from environment + environmentFiles│   ├── auth.json                    # OAuth credentials (seeded, then self-managed)│   ├── gateway.pid│   ├── state.db│   ├── mcp-tokens/                  # OAuth tokens for MCP servers│   ├── sessions/│   ├── memories/│   ├── skills/│   ├── cron/│   └── logs/├── home/                            # Agent HOME└── workspace/                       # Agent working directory    ├── SOUL.md                      # From documents option    └── (agent-created files)
```

### حالت Container​

چیدمان یکسان، mount شده به container:

| مسیر container | مسیر هاست | حالت | توضیحات |
| --- | --- | --- | --- |
| `/nix/store` | `/nix/store` | ro | باینری Hermes + همه deps Nix |
| `/data` | `/var/lib/hermes` | rw | همه state، پیکربندی، workspace |
| `/home/hermes` | `${stateDir}/home` | rw | خانه agent پایدار — `pip install --user`، کش ابزارها |
| `/usr`، `/usr/local`، `/tmp` | (لایه writable) | rw | installهای `apt`/`pip`/`npm` — در ری‌بوت پایدار، در بازسازی از دست رفته |

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

## به‌روزرسانی​

```
# Update the flake input (run from the directory containing flake.nix)cd /etc/nixos && nix flake update hermes-agent# Rebuildsudo nixos-rebuild switch
```

در حالت container، symlink `current-package` به‌روزرسانی می‌شود و agent باینری جدید را هنگام ری‌بوت دریافت می‌کند. بدون بازسازی container، بدون از دست دادن بسته‌های نصب‌شده.

`current-package`

## عیب‌یابی​

**همه** دستورات `docker` زیر با `podman` نیز کار می‌کنند. اگر `container.backend = "podman"` تنظیم کرده‌اید به ترتیب جایگزین کنید.

`docker`
`podman`
`container.backend = "podman"`

### لاگ‌های سرویس​

```
# Both modes use the same systemd unitjournalctl -u hermes-agent -f# Container mode: also available directlydocker logs -f hermes-agent
```

### بازرسی Container​

```
systemctl status hermes-agentdocker ps -a --filter name=hermes-agentdocker inspect hermes-agent --format='{{.State.Status}}'docker exec -it hermes-agent bashdocker exec hermes-agent readlink /data/current-packagedocker exec hermes-agent cat /data/.container-identity
```

### اجبار بازسازی Container​

اگر نیاز به بازنشانی لایمه writable (Ubuntu تازه) دارید:

```
sudo systemctl stop hermes-agentdocker rm -f hermes-agentsudo rm /var/lib/hermes/.container-identitysudo systemctl start hermes-agent
```

### بررسی بارگذاری رازها​

اگر agent شروع می‌شود اما نمی‌تواند با provider LLM احراز هویت کند، بررسی کنید فایل `.env` به درستی merge شده:

`.env`

```
# Native modesudo -u hermes cat /var/lib/hermes/.hermes/.env# Container modedocker exec hermes-agent cat /data/.hermes/.env
```

### بررسی GC Root​

```
nix-store --query --roots $(docker exec hermes-agent readlink /data/current-package)
```

### مشکلات رایج​

| علامت | علت | راه‌حل |
| --- | --- | --- |
| `Cannot save configuration: managed by NixOS` | محافظهای CLI فعال | `configuration.nix` را ویرایش و `nixos-rebuild switch` کنید |
| `No adapter available for discord` (یا telegram/slack) | وابستگی‌های messaging از venv sealed Nix موجود نیستند | بسته `#messaging` نصب کنید: `nix profile install ...#messaging`. برای ماژول NixOS: `extraDependencyGroups = [ "messaging" ].` `journalctl -u hermes-agent` را برای `FeatureUnavailable` یا `requirements not met` بررسی کنید. |
| Container به طور غیرمنتظره بازسازی شد | `extraVolumes`، `extraOptions` یا `image` تغییر کرد | عادی — لایمه writable بازنشانی می‌شود. بسته‌ها را دوباره نصب کنید یا از image سفارشی استفاده کنید |
| `hermes version` نسخه قدیمی نشان می‌دهد | Container ری‌بوت نشده | `systemctl restart hermes-agent` |
| Permission denied در `/var/lib/hermes` | دایرکتوری state `0750 hermes:hermes` است | از `docker exec` یا `sudo -u hermes` استفاده کنید |
| `nix-collect-garbage` hermes را حذف کرد | GC root موجود نیست | سرویس را بازنشانی کنید (`preStart` GC root را بازسازی می‌کند) |
| `no container with name or ID "hermes-agent"` (Podman) | container rootful Podman برای کاربر عادی قابل مشاهده نیست | sudo بدون رمز عبور برای podman اضافه کنید (بخش [حالت Container](#container-mode) را ببینید) |
| `unable to find user hermes` | Container هنوز در حال شروع است (entry point هنوز کاربر را ایجاد نکرده) | چند ثانیه صبر و دوباره تلاش کنید — CLI به طور خودکار تلاش می‌کند |
| ابزار اضافه‌شده از طریق `extraPackages` در ترمinal یافت نشد | نیاز به `nixos-rebuild switch` برای به‌روزرسانی پروفایل per-user | rebuild و restart: `nixos-rebuild switch && systemctl restart hermes-agent` |

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