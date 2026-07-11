---
layout: docs
title: "پیکربندی"
permalink: /docs/user-guide/configuration/
---

- 
- استفاده از Hermes
- پیکربندی

# پیکربندی

تمام تنظیمات در دایرکتوری `~/.hermes/` برای دسترسی آسان ذخیره می‌شوند.

`hermes setup --portal` را اجرا کنید — یک OAuth یک ارائه‌دهنده مدل و تمام چهار ابزار Tool Gateway را بدون ویرایش دستی YAML به شما می‌دهد. مشترکین Portal ۱۰٪ تخفیف در ارائه‌دهندگان پرداخت‌شده با توکن دارند. [Nous Portal](/docs/integrations/nous-portal/) را ببینید.

## ساختار دایرکتوری

```
~/.hermes/
├── config.yaml     # تنظیمات (مدل، ترمinal، TTS، فشرده‌سازی و غیره)
├── .env            # کلیدهای API و رمزها
├── auth.json       # اعتبارات ارائه‌دهنده OAuth (Nous Portal و غیره)
├── SOUL.md         # هویت اصلی agent (slot #1 در system prompt)
├── memories/       # حافظه پایدار (MEMORY.md، USER.md)
├── skills/         # skillهای ایجاد شده توسط agent (مدیریت شده از طریق ابزار skill_manage)
├── cron/           # jobهای زمان‌بندی شده
├── sessions/       # sessionهای gateway
└── logs/           # لاگ‌ها (errors.log، gateway.log — رمزها به طور خودکار redact می‌شوند)
```

## مدیریت پیکربندی

```bash
hermes config              # نمایش پیکربندی فعلی
hermes config edit         # باز کردن config.yaml در ویرایشگر شما
hermes config set KEY VAL  # تنظیم یک مقدار مشخص
hermes config check        # بررسی گزینه‌های موجود (بعد از به‌روزرسانی)
hermes config migrate      # اضافه کردن تعاملی گزینه‌های موجود
# مثال‌ها:
hermes config set model anthropic/claude-opus-4
hermes config set terminal.backend docker
hermes config set OPENROUTER_API_KEY sk-or-...  # در .env ذخیره می‌شود
```

فرمان `hermes config set` به طور خودکار مقادیر را به فایل صحیح هدایت می‌کند — کلیدهای API در `.env` و بقیه در `config.yaml` ذخیره می‌شوند.

## ترتیب اولویت پیکربندی

تنظیمات به این ترتیب حل می‌شوند (بالاترین اولویت اول):

1. **آرگومان‌های CLI** — مثلاً `hermes chat --model anthropic/claude-sonnet-4` (override به ازای هر فراخوانی)
2. `~/.hermes/config.yaml` — فایل پیکربندی اصلی برای تمام تنظیمات غیر رمز
3. `~/.hermes/.env` — fallback برای متغیرهای محیطی؛ **لازم** برای رمزها (کلیدهای API، توکن‌ها، رمزهای عبور)
4. **پیش‌فرض‌های داخلی** — پیش‌فرض‌های امن ثابت‌شده وقتی هیچ چیز دیگری تنظیم نشده

رمزها (کلیدهای API، توکن‌های ربات، رمزهای عبور) در `.env` قرار می‌گیرند. بقیه (مدل، بک‌اند ترمinal، تنظیمات فشرده‌سازی، محدودیت‌های حافظه، مجموعه ابزارها) در `config.yaml` قرار می‌گیرند. وقتی هر دو تنظیم شده باشند، `config.yaml` برای تنظیمات غیر رمز اولویت دارد.

یک مدیر سیستم می‌تواند مقادیر پیکربندی و رمز خاصی را که یک کاربر عادی نمی‌تواند override کند، از طریق یک دایرکتوری مدیریت‌شده سطح سیستمی ثابت کند. [Managed Scope](/docs/user-guide/managed-scope/) را ببینید.

## جایگزینی متغیر محیطی

می‌توانید به متغیرهای محیطی در `config.yaml` با فرمت `${VAR_NAME}` ارجاع دهید:

```yaml
auxiliary:
  vision:
    api_key: ${GOOGLE_API_KEY}
    base_url: ${CUSTOM_VISION_URL}
delegation:
  api_key: ${DELEGATION_KEY}
```

ارجاعات متعدد در یک مقدار واحد کار می‌کنند: `url: "${HOST}:${PORT}"`. اگر متغیر ارجاع‌شده تنظیم نشده باشد، placeholder بدون تغییر باقی می‌ماند. فقط فرمت `${_VAR}` پشتیبانی می‌شود — `$VAR` ساده گسترش نمی‌یابد.

برای پیکربندی ارائه‌دهنده AI، [ارائه‌دهندگان AI](/docs/integrations/providers/) را ببینید.

### timeout ارائه‌دهندگان

می‌توانید `providers.<id>.request_timeout_seconds` برای timeout درخواست در سطح ارائه‌دهنده و `providers.<id>.models.<model>.timeout_seconds` برای override مدل خاص تنظیم کنید. این بر کلاینت نوبت اصلی در هر انتقال (OpenAI-wire، Anthropic بومی، Anthropic-compatible)، زنجیره fallback و بازسازی‌ها بعد از چرخش اعتبار اعمال می‌شود.

می‌توانید `providers.<id>.stale_timeout_seconds` برای آشکارساز stale call غیر-streaming و `providers.<id>.models.<model>.stale_timeout_seconds` برای override مدل خاص تنظیم کنید.

## رفتار به‌روزرسانی

تنظیمات `hermes update` در `updates` در `config.yaml` قرار دارند:

```yaml
updates:
  pre_update_backup: false       # ایجاد یک zip کامل HERMES_HOME قبل از هر به‌روزرسانی
  backup_keep: 5                 # نگه‌داشتن این تعداد zip پشتیبان قبل از به‌روزرسانی
  non_interactive_local_changes: stash  # stash | discard
```

برای نصب‌های git، Hermes به طور خودکار فایل‌های tracked کثیف و فایل‌های tracked نشده را قبل از checkout شاخه به‌روزرسانی یا pull stash می‌کند.

قبل از آن مرحله stash، Hermes همچنین تفاوت‌های `package-lock.json` tracked باقی‌مانده از نوسانات `npm install`/build را بازیابی می‌کند. ویرایش‌های عمدی lockfile را قبل از به‌روزرسانی commit یا stash دستی کنید.

## پیکربندی بک‌اند ترمinal

Hermes شش بک‌اند ترمinal پشتیبانی می‌کند. هر کدام تعیین می‌کنند فرمان‌های shell agent واقعاً کجا اجرا می‌شوند.

```yaml
terminal:
  backend: local    # local | docker | ssh | modal | daytona | singularity
  cwd: "."          # دایرکتوری کاری gateway/cron
  timeout: 180      # timeout به ازای هر فرمان به ثانیه
  home_mode: auto   # auto | real | profile
  env_passthrough: []
  singularity_image: "docker://nikolaik/python-nodejs:python3.11-nodejs20"
  modal_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  daytona_image: "nikolaik/python-nodejs:python3.11-nodejs20"
```

برای sandboxهای ابری مانند Modal و Daytona، `container_persistent: true` به این معنی است که Hermes تلاش می‌کند وضعیت فایل‌سیستم را در بازسازی sandbox حفظ کند.

### نمای کلی بک‌اند

| بک‌اند | فرمان‌ها کجا اجرا می‌شوند | ایزولاسیون | بهترین برای |
| --- | --- | --- | --- |
| `local` | مستقیماً ماشین شما | هیچ | توسعه، استفاده شخصی |
| `docker` | کانتینر Docker پایدار مشترک | کامل (namespace، cap-drop) | sandbox ایمن، CI/CD |
| `ssh` | سرور راه‌دور از طریق SSH | مرز شبکه | توسعه راه‌دور |
| `modal` | sandbox ابری Modal | کامل (VM ابری) | محاسبات ابری موقت |
| `daytona` | workspace Daytona | کامل (کانتینر ابری) | محیط‌های توسعه ابری مدیریت‌شده |
| `singularity` | کانتینر Singularity/Apptainer | Namespace (`--containall`) | خوشه‌های HPC |

### بک‌اند محلی

پیش‌فرض. فرمان‌ها مستقیماً روی ماشین شما بدون ایزولاسیون اجرا می‌شوند. هیچ پیکربندی خاصی نیاز نیست.

```yaml
terminal:
  backend: local
```

به طور پیش‌فرض، subprocessهای ابزار محلی HOME واقعی کاربر OS شما را حفظ می‌کنند. این به CLIهای خارجی مانند `git`، `ssh`، `gh`، `az`، `npm`، Claude Code و Codex اجازه می‌دهد اعتبارات و پیکربندی‌ای که از قبل در shell عادی شما دارند را پیدا کنند.

#### terminal.home_mode

| حالت | نصب‌های هاست | Container | tradeoff |
| --- | --- | --- | --- |
| `auto` | HOME واقعی کاربر OS را نگه دارد | از `{HERMES_HOME}/home` استفاده کند | توصیه‌شده. CLIهای هاست کار می‌کنند؛ وضعیت container پایدار می‌ماند |
| `real` | HOME واقعی کاربر OS را اجبار کند | HOME واقعی کاربر OS را اجبار کند اگر قابل مشاهده باشد | مفید اگر فرآیند والد تصادفاً با HOME اشاره شده به home پروفایل شروع شده |
| `profile` | از `{HERMES_HOME}/home` وقتی وجود دارد استفاده کند | از `{HERMES_HOME}/home` وقتی وجود دارد استفاده کند | ایزوله CLI به ازای هر پروفایل |

### بک‌اند Docker

فرمان‌ها را درون یک کانتینر Docker با سخت‌سازی امنیتی اجرا می‌کند.

**کانتینر مشترک پایدار** — Hermes یک کانتینر طولانی‌مدت در اولین استفاده شروع و هر فراخوانی ترمinal، فایل و `execute_code` را از طریق `docker exec` در همان کانتینر مسیریابی می‌کند.

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  docker_mount_cwd_to_workspace: false
  docker_run_as_host_user: false
  docker_forward_env:
    - "GITHUB_TOKEN"
  docker_env:
    DEBUG: "1"
    PYTHONUNBUFFERED: "1"
  docker_volumes:
    - "/home/user/projects:/workspace/projects"
    - "/home/user/data:/data:ro"
  docker_extra_args:
    - "--gpus=all"
    - "--network=host"
  docker_network: true
  container_cpu: 1
  container_memory: 5120
  container_disk: 51200
  container_persistent: true
  docker_persist_across_processes: true
  docker_orphan_reaper: true
  timeout: 180
  lifetime_seconds: 300
```

**`docker_env` در مقابل `docker_forward_env`:** اولی جفت‌های لیترال `KEY=value` را تزریق می‌کند. دومی مقادیر از shell یا `~/.hermes/.env` شما را forward می‌کند. برای توکن‌ها از `docker_forward_env` و برای تنظیمات ایستا از `docker_env` استفاده کنید.

**`terminal.docker_extra_args`** (همچنین قابل override از طریق `TERMINAL_DOCKER_EXTRA_ARGS='["--gpus=all"]'`) به شما اجازه می‌دهد پرچم‌های دلخواه `docker run` را پاس دهید.

**`terminal.docker_network`** (پیش‌فرض `true`) — `false` برای اجرای sandbox با `--network=none`.

**الزامات:** Docker Desktop یا Docker Engine نصب و در حال اجرا. Hermes از `$PATH` و مکان‌های نصب رایج macOS کاوش می‌کند. Podman از جعبه پشتیبانی می‌شود: `HERMES_DOCKER_BINARY=podman` را تنظیم کنید.

#### چرخه حیات کانتینر

هر کانتینر مدیریت‌شده Hermes با سه برچسب برچسب‌گذاری می‌شود:
- `hermes-agent=1`
- `hermes-task-id=<sanitized task_id>`
- `hermes-profile=<sanitized profile name>`

در شروع، Hermes `docker ps --filter label=hermes-task-id=<id> --filter label=hermes-profile=<profile>` را اجرا و به کانتینر موجود وصل می‌شود.

وقتی فرآیند Hermes خارج می‌شود، مسیر پاکسازی برای کانتینر در حالت پیش‌فرض no-op است. کانتینر به اجرا ادامه می‌دهد.

کانتینر فقط در این موارد تخریب می‌شود (متوقف و `docker rm -f`):

| محرک | زمانی که فعال می‌شود |
| --- | --- |
| `docker_persist_across_processes: false` | ایزوله هر فرآیند |
| Idle reaper (`lifetime_seconds`) | فقط وقتی `persist_across_processes=false` |
| Orphan reaper در راه‌اندازی بعدی | containers `Exited` قدیمی‌تر از `2 × lifetime_seconds` |
| عمل مستقیم کاربر | `docker rm -f`، `docker system prune` |

**سخت‌سازی امنیتی:**
- `--cap-drop ALL` با فقط `DAC_OVERRIDE`، `CHOWN`، `FOWNER` اضافه شده
- `--security-opt no-new-privileges`
- `--pids-limit 256`
- tmpfs با اندازه محدود برای `/tmp` (512MB)، `/var/tmp` (256MB)، `/run` (64MB)

#### متغیرهای محیطی override

هر کلید در `terminal:` یک override متغیر محیطی به فرم `TERMINAL_<KEY_UPPERCASE>` دارد.

### بک‌اند SSH

فرمان‌ها را روی یک سرور راه‌دور از طریق SSH اجرا می‌کند.

```yaml
terminal:
  backend: ssh
  persistent_shell: true
```

متغیرهای محیطی لازم: `TERMINAL_SSH_HOST` و `TERMINAL_SSH_USER`.

اختیاری: `TERMINAL_SSH_PORT` (پیش‌فرض 22)، `TERMINAL_SSH_KEY`، `TERMINAL_SSH_PERSISTENT` (پیش‌فرض true).

### بک‌اند Modal

فرمان‌ها را در یک sandbox ابری [Modal](https://modal.com) اجرا می‌کند.

```yaml
terminal:
  backend: modal
  container_cpu: 1
  container_memory: 5120
  container_disk: 51200
  container_persistent: true
```

لزوم: متغیرهای `MODAL_TOKEN_ID` + `MODAL_TOKEN_SECRET` یا فایل پیکربندی `~/.modal.toml`.

### بک‌اند Daytona

فرمان‌ها را در یک [workspace مدیریت‌شده Daytona](https://daytona.io) اجرا می‌کند.

```yaml
terminal:
  backend: daytona
  container_cpu: 1
  container_memory: 5120
  container_disk: 10240
  container_persistent: true
```

لزوم: متغیر محیطی `DAYTONA_API_KEY`.

### بک‌اند Singularity/Apptainer

فرمان‌ها را در یک [کانتینر Singularity/Apptainer](https://apptainer.org) اجرا می‌کند.

```yaml
terminal:
  backend: singularity
  singularity_image: "docker://nikolaik/python-nodejs:python3.11-nodejs20"
  container_cpu: 1
  container_memory: 5120
  container_persistent: true
```

لزوم: باینری `apptainer` یا `singularity` در `$PATH`.

### مشکلات رایج بک‌اند ترمinal

- **local** — بدون پیش‌نیاز خاص
- **docker** — `docker version` را اجرا کنید
- **ssh** — `TERMINAL_SSH_HOST` و `TERMINAL_SSH_USER` لازم هستند
- **modal** — به `MODAL_TOKEN_ID` یا `~/.modal.toml` نیاز دارد
- **daytona** — به `DAYTONA_API_KEY` نیاز دارد
- **singularity** — به `apptainer` یا `singularity` در `$PATH` نیاز دارد

هنگام تردید، `terminal.backend` را به `local` برگردانید.

### همگام‌سازی فایل از راه‌دور به هاست در هنگام تخریب

برای بک‌اندهای SSH، Modal و Daytona، Hermes فایل‌هایی را که agent در sandbox راه‌دور لمس کرده در `~/.hermes/cache/remote-syncs/<session-id>/` به هاست sync می‌کند.

### Mount دایرکتوری‌های هاست

```yaml
terminal:
  backend: docker
  docker_volumes:
    - "/home/user/projects:/workspace/projects"
    - "/home/user/datasets:/data:ro"
    - "/home/user/.hermes/cache/documents:/output"
```

### انتقال اعتبار Docker

به طور پیش‌فرض، sessionهای ترمinal Docker credentialهای دلخواه هاست را به ارث نمی‌برند. اگر توکن خاصی در کانتینر نیاز دارید، آن را به `terminal.docker_forward_env` اضافه کنید.

### اجرای کانتینر به عنوان کاربر هاست شما

به طور پیش‌فرض کانتینرها به عنوان `root` (UID 0) اجرا می‌شوند. `terminal.docker_run_as_host_user` این را رفع می‌کند.

### shell پایدار

به طور پیش‌فرض هر فرمان ترمinal در subprocess خود اجرا می‌شود. وقتی shell پایدار فعال است، یک فرآیند bash طولانی‌مدت در سراسر فراخوانی‌های `execute()` نگه داشته می‌شود تا وضعیت بین فرمان‌ها پایدار بماند.

## تنظیمات Skill

Skillها می‌توانند تنظیمات پیکربندی خود را از طریق frontmatter SKILL.md اعلام کنید. این‌ها مقادیر غیر رمز هستند که در `skills.config` در `config.yaml` ذخیره می‌شوند.

```yaml
skills:
  config:
    myplugin:
      path: ~/myplugin-data
```

نحوه کار تنظیمات skill:
- `hermes config migrate` تمام skillهای فعال را اسکن و گزینه‌های پیکربندی‌نشده را پیشنهاد می‌کند
- `hermes config show` تمام تنظیمات skill را نشان می‌دهد
- وقتی skill بارگذاری می‌شود، مقادیر پیکربندی رفع‌شده به طور خودکار تزریق می‌شوند

### نگهبان نوشتن skill ایجاد شده توسط agent

وقتی agent از `skill_manage` برای ایجاد، ویرایش، patch یا حذف یک skill استفاده می‌کند، Hermes می‌تواند محتوا را برای الگوهای کلمه کلیدی خطرناک اسکن کند. اسکنر به طور پیش‌فرض **خاموش** است.

```yaml
skills:
  guard_agent_created: true   # پیش‌فرض: false
```

### تأیید نوشتن skill

`skills.write_approval` هر نوشتن skill agent را پشت تأیید صریح شما قفل می‌کند:

```yaml
skills:
  write_approval: false   # false = نوشتن آزاد (پیش‌فرض) | true = هر نوشتن برای بررسی staging شود
```

## پیکربندی حافظه

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200   # ~۸۰۰ توکن
  user_char_limit: 1375     # ~۵۰۰ توکن
  write_approval: false     # true = تأیید قبل از هر نوشتن حافظه لازم است
```

با `memory.write_approval: true`، نوشتن‌های حافظه قبل از اعمال به تأیید شما نیاز دارند.

## محدودیت بریدن فایل Context

کنترل می‌کند Hermes چه مقدار محتوا از هر فایل context خودکار قبل از اعمال بریدن head/tail بارگذاری کند. این روی فایل‌های تزریق شده به system prompt مانند `SOUL.md`، `.hermes.md`، `AGENTS.md`، `CLAUDE.md` و `.cursorrules` اعمال می‌شود.

```
context_file_max_chars: 20000  # پیش‌فرض
```

## ایمنی خواندن فایل

کنترل می‌کند یک فراخوانی `read_file` واحد چه مقدار محتوا می‌تواند برگرداند. خواندن‌هایی که از محدودیت فراتر روند با خطا رد می‌شوند.

```
file_read_max_chars: 100000  # پیش‌فرض — ~۲۵-۳۵K توکن
```

## محدودیت بریدن خروجی ابزار

سه سقف مرتبط خروجی خامی را که ابزار می‌تواند قبل از بریدن Hermes برگرداند کنترل می‌کنند:

```yaml
tool_output:
  max_bytes: 50000        # سقف خروجی ترمinal (کاراکتر)
  max_lines: 2000         # سقف صفحه‌بندی read_file
  max_line_length: 2000   # سقف به ازای هر خط در نمای شماره‌خطی
```

## غیرفعال کردن سراسری مجموعه ابزار

```yaml
agent:
  disabled_toolsets:
    - memory       # پنهان کردن ابزارهای حافظه + تزریق MEMORY_GUIDANCE
    - web          # هیچ web_search / web_extract در هیچ جا
```

## ایزوله‌سازی Git Worktree

```yaml
worktree: true    # همیشه یک worktree ایجاد کنید (مشابه hermes -w)
```

## فشرده‌سازی Context

Hermes مکالمات طولانی را به طور خودکار فشرده می‌کند تا در پنجره context مدل شما باقی بماند.

```yaml
compression:
  enabled: true
  threshold: 0.50
  target_ratio: 0.20
  protect_last_n: 20
  protect_first_n: 3
  hygiene_hard_message_limit: 5000
```

`hygiene_hard_message_limit` یک سوپاپ ایمنی gateway-فقط قبل از فشرده‌سازی است. پیش‌فرض `5000`.

`protect_first_n` کنترل می‌کند چند پیام ابتدایی غیر-system در هر فشرده‌سازی pin شوند. پیش‌فرض `3`.

## موتور Context

`compressor` موتور داخلی خلاصه‌سازی lossy است. موتورهای پلاگین می‌توانند آن را با استراتژی‌های جایگزین جایگزین کنند.

```yaml
context:
  engine: "compressor"    # پیش‌فرض — خلاصه‌سازی داخلی lossy
```

## بودجه تکرار

وقتی agent روی یک کار پیچیده با فراخوانی‌های ابزار متعدد کار می‌کند، می‌تواند بودجه تکرار خود (پیش‌فرض: ۹۰ نوبت) را مصرف کند.

```yaml
agent:
  max_turns: 90                # حداکثر تکرار به ازای هر نوبت مکالمه (پیش‌فرض: ۹۰)
  api_max_retries: 3           # تلاش‌های مجدد به ازای هر ارائه‌دهنده قبل از فعال‌سازی fallback (پیش‌فرض: ۳)
```

## اهداف پایدار (/goal)

```yaml
goals:
  max_turns: 20   # حداکثر نوبت‌های ادامه قبل از توقف خودکار Hermes (پیش‌فرض: ۲۰)
```

## timeout API

Hermes لایه‌های timeout مجزایی برای streaming و یک آشکارساز stale برای فراخوانی‌های non-streaming دارد.

| Timeout | پیش‌فرض | ارائه‌دهندگان محلی | پیکربندی / env |
| --- | --- | --- | --- |
| Socket read timeout | 120s | خودکار به 1800s افزایش | `HERMES_STREAM_READ_TIMEOUT` |
| Stale stream detection | 180s | خودکار غیرفعال | `HERMES_STREAM_STALE_TIMEOUT` |
| Stale non-stream detection | 300s | خودکار غیرفعال | `providers.<id>.stale_timeout_seconds` یا `HERMES_API_CALL_STALE_TIMEOUT` |
| API call (non-streaming) | 1800s | بدون تغییر | `providers.<id>.request_timeout_seconds` یا `HERMES_API_TIMEOUT` |

## هشدارهای فشار Context

جدای از فشار بودجه تکرار، فشار context ردیابی می‌کند مکالمه چقدر به آستانه compaction نزدیک است.

| پیشرفت | سطح | چه اتفاقی می‌افتد |
| --- | --- | --- |
| ≥ ۶۰٪ تا آستانه | Info | CLI نوار پیشرفت فیروزه‌ای نشان می‌دهد |
| ≥ ۸۵٪ تا آستانه | Warning | CLI نوار زرد برجسته نشان می‌دهد |

## استراتژی‌های Pool اعتبار

وقتی چندین کلید API یا توکن OAuth برای یک ارائه‌دهنده دارید، استراتژی چرخش را پیکربندی کنید:

```yaml
credential_pool_strategies:
  openrouter: round_robin
  anthropic: least_used
```

گزینه‌ها: `fill_first` (پیش‌فرض)، `round_robin`، `least_used`، `random`.

## cache prompt

Hermes cache prompt بین session را وقتی ارائه‌دهنده فعال از آن پشتیبانی می‌کند به طور خودکار فعال می‌کند — نیازی به پیکربندی کاربر نیست.

## مدل‌های کمکی

Hermes از مدل‌های «کمکی» برای وظایف جانبی مانند تحلیل تصویر، خلاصه‌سازی صفحه وب، تحلیل اسکرین‌شات مرورگر، تولید عنوان session و فشرده‌سازی context استفاده می‌کند. به طور پیش‌فرض (`auxiliary.*.provider: "auto"`)، Hermes هر وظیفه کمکی را به مدل چت اصلی شما مسیریابی می‌کند.

### تنظیم تعاملی مدل‌های کمکی

به جای ویرایش دستی YAML، `hermes model` را اجرا کنید و «Configure auxiliary models» را از منو انتخاب کنید.

### الگوی پیکربندی همگانی

هر اسلات مدل در Hermes — وظایف کمکی، فشرده‌سازی، fallback — از سه دکمه یکسان استفاده می‌کند:

| کلید | چه کاری انجام می‌دهد | پیش‌فرض |
| --- | --- | --- |
| `provider` | کدام ارائه‌دهنده برای احراز هویت و مسیریابی | `"auto"` |
| `model` | کدام مدل درخواست شود | پیش‌فرض ارائه‌دهنده |
| `base_url` | endpoint سازگار با OpenAI دلخواه (provider را override می‌کند) | تنظیم نشده |

ارائه‌دهندگان موجود: `auto`، `main`، به علاوه هر ارائه‌دهنده در [فهرست ارائه‌دهندگان](/docs/reference/environment-variables/).

## تلاش استدلال

```yaml
agent:
  reasoning_effort: ""   # خالی = medium (پیش‌فرض). گزینه‌ها: none, minimal, low, medium, high, xhigh
```

همچنین می‌توانید با فرمان `/reasoning` در زمان اجرا تغییر دهید.

## اجبار استفاده از ابزار

برخی مدل‌ها گاهی اوقات اقدامات مورد نظر را به جای فراخوانی ابزار به صورت متن توصیف می‌کنند.

```yaml
agent:
  tool_use_enforcement: "auto"   # "auto" | true | false | ["model-substring", ...]
```

| مقدار | رفتار |
| --- | --- |
| `"auto"` (پیش‌فرض) | برای مدل‌های مطابق: `gpt`، `codex`، `gemini`، `gemma`، `grok` فعال |
| `true` | همیشه فعال |
| `false` | همیشه غیرفعال |
| `["gpt", "codex", "qwen", "llama"]` | فقط وقتی نام مدل شامل یکی از زیررشته‌های لیست‌شده باشد فعال |

## نگهبان‌های حلقه ابزار

Hermes تشخیص می‌دهد کی agent در یک حلقه فراخوانی ابướng غیرمولد گیر کرده.

```yaml
tool_loop_guardrails:
  warnings_enabled: true
  hard_stop_enabled: false
  warn_after:
    exact_failure: 2
    same_tool_failure: 3
    idempotent_no_progress: 2
  hard_stop_after:
    exact_failure: 5
    same_tool_failure: 8
    idempotent_no_progress: 5
```

## پیکربندی TTS

```yaml
tts:
  provider: "edge"              # "edge" | "elevenlabs" | "openai" | "minimax" | "mistral" | "gemini" | "xai" | "neutts"
  speed: 1.0
  edge:
    voice: "en-US-AriaNeural"
    speed: 1.0
  elevenlabs:
    voice_id: "pNInz6obpgDQGcFmaJgB"
    model_id: "eleven_multilingual_v2"
  openai:
    model: "gpt-4o-mini-tts"
    voice: "alloy"
    speed: 1.0
    base_url: "https://api.openai.com/v1"
  minimax:
    speed: 1.0
  mistral:
    model: "voxtral-mini-tts-2603"
    voice_id: "c69964a6-ab8b-4f8a-9465-ec0925096ec8"
  gemini:
    model: "gemini-2.5-flash-preview-tts"
    voice: "Kore"
    audio_tags: false
    persona_prompt_file: ""
  xai:
    voice_id: "eve"
    language: "en"
    sample_rate: 24000
    bit_rate: 128000
  neutts:
    ref_audio: ''
    ref_text: ''
    model: neuphonic/neutts-air-q4-gguf
    device: cpu
```

## تنظیمات نمایش

```yaml
display:
  tool_progress: all      # off | new | all | verbose
  tool_progress_command: false
  platforms: {}
  skin: default
  personality: "kawaii"
  compact: false
  resume_display: full    # full | minimal
  bell_on_complete: false
  show_reasoning: false
  streaming: false
  show_cost: false
  timestamps: false
  tool_preview_length: 0
  runtime_footer:
    enabled: false
    fields: ["model", "context_pct", "cwd"]
  file_mutation_verifier: true
  credits_notices: true
  language: en            # en | zh | zh-hant | ja | de | es | fr | tr | uk | af | ko | it | ga | pt | ru | hu
```

### verifier تغییر فایل

وقتی `display.file_mutation_verifier` `true` است (پیش‌فرض)، Hermes هر زمان `write_file` یا `patch` در طول نوبت ناموفق بوده و هرگز با نوشتن موفق به همان مسیر جایگزین نشده، یک خط توصیه به پاسخ نهایی agent اضافه می‌کند.

### زبان UI برای پیام‌های ثابت

تنظیم `display.language` مجموعه کوچکی از پیام‌های ثابت کاربرمحور را ترجمه می‌کند — prompt تأیید CLI، تعدادی پاسخ فرمان اسلش gateway. پاسخ‌های agent، خطوط لاگ، خروجی ابزار یا tracebackها را ترجمه **نمی‌کند** — آن‌ها به انگلیسی باقی می‌مانند.

مقادیر پشتیبانی‌شده: `en` (پیش‌فرض)، `zh`، `zh-hant`، `ja`، `de`، `es`، `fr`، `tr`، `uk`، `af`، `ko`، `it`، `ga`، `pt`، `ru`، `hu`.

## ساختار پیکربندی CLI

```yaml
quick_commands:
  status:
    type: exec
    command: systemctl status hermes-agent
  gpu:
    type: exec
    command: nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader
  restart:
    type: alias
    target: /gateway restart
```

## رمزگذاری UTF-8 در Windows

Hermes در Windows کنسول را به CP_UTF8 (65001) تبدیل، `sys.stdout`/`sys.stderr`/`sys.stdin` را به UTF-8 با `errors='replace'` پیکربندی و `PYTHONIOENCODING=utf-8` + `PYTHONUTF8=1` را تنظیم می‌کند.

با `HERMES_DISABLE_WINDOWS_UTF8=1` غیرفعال کنید.

## رفتار gateway

```yaml
gateway:
  auto_start: true
  restart_on_config_change: true
  max_concurrent_sessions: 50
  session_timeout: 3600
  message_timeout: 300
```

## رفتار agent

```yaml
agent:
  max_turns: 90
  api_max_retries: 3
  reasoning_effort: ""
  tool_use_enforcement: "auto"
```

## امنیت

```yaml
security:
  require_approval_for_dangerous_commands: true
  blocked_commands: []
  sandbox_mode: "none"    # none | docker
```

## صفحه‌بندی CLI

```yaml
cli:
  pager: "auto"           # auto | less | cat | none
  history_size: 10000
```

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/configuration.md)
