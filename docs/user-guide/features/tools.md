---
layout: docs
title: "ابزارها"
permalink: /docs/user-guide/features/tools/
---

- 
- Features
- Core
- Tools & Toolsets

# ابزارها و مجموعه ابزارها

ابزارها توابعی هستند که قابلیت‌های agent را گسترش می‌دهند. آنها در مجموعه ابزارهای منطقی سازماندهی شده‌اند که می‌توانند برای هر پلتفرم فعال یا غیرفعال شوند.

## ابزارهای موجود

Hermes با یک ثبت‌نام گسترده ابزار داخلی ارائه می‌شود که جستجوی وب، اتوماسیون مرورگر، اجرای ترمینال، ویرایش فایل، حافظه، واگذاری، وظایف زمان‌بندی‌شده، Home Assistant و موارد دیگر را پوشش می‌دهد.

حافظه cross-session Honcho به عنوان یک افزونه ارائه‌دهنده حافظه (`plugins/memory/honcho/`) در دسترس است، نه به عنوان یک مجموعه ابزار داخلی. برای نصب به افزونه‌ها مراجعه کنید.

`plugins/memory/honcho/`
[افزونه‌ها](/docs/user-guide/features/plugins/)

دسته‌بندی‌های کلی:

| دسته‌بندی | مثال‌ها | توضیحات |
| --- | --- | --- |
| وب | `web_search`، `web_extract` | جستجو در وب و استخراج محتوای صفحه. |
| جستجوی X | `x_search` | جستجوی پست‌ها و تردهای X (Twitter) از طرقی ابزار داخلی `x_search` Responses xAI — وابسته به اعتبارنامه‌های xAI (SuperGrok OAuth یا `XAI_API_KEY`); به طور پیش‌فرض خاموش، از طریق `hermes tools` → 🐦 X (Twitter) Search فعال کنید. |
| ترمینال و فایل‌ها | `terminal`، `process`، `read_file`، `patch` | اجرای دستورات و مدیریت فایل‌ها. |
| مرورگر | `browser_navigate`، `browser_snapshot`، `browser_vision` | اتوماسیون تعاملی مرورگر با پشتیبانی متنی و بصری. |
| رسانه | `vision_analyze`، `image_generate`، `text_to_speech` | تولید و تحلیل چندوجهی. |
| ارکستراسیون agent | `todo`، `clarify`، `execute_code`، `delegate_task` | برنامه‌ریزی، شفاف‌سازی، اجرای کد و واگذاری subagent. |
| حافظه و بازیابی | `memory`، `session_search` | حافظه ماندگار و جستجوی نشست. |
| اتوماسیون | `cronjob` | وظایف زمان‌بندی‌شده با اقدامات create/list/update/pause/resume/run/remove. ارسال خروجی توسط سیستم تحویل خود cron، CLI `hermes send` و اعلان‌رسان gateway انجام می‌شود — نه توسط یک ابزار قابل فراخوانی agent. |
| ادغام‌ها | `ha_*`، ابزارهای سرور MCP | Home Assistant، MCP و سایر ادغام‌ها. |

`web_search`
`web_extract`
`x_search`
`x_search`
`XAI_API_KEY`
`hermes tools`
`terminal`
`process`
`read_file`
`patch`
`browser_navigate`
`browser_snapshot`
`browser_vision`
`vision_analyze`
`image_generate`
`text_to_speech`
`todo`
`clarify`
`execute_code`
`delegate_task`
`memory`
`session_search`
`cronjob`
`hermes send`
`ha_*`

برای ثبت‌نام معتبر مشتق از کد، به مرجع ابزارهای داخلی و مرجع مجموعه ابزارها مراجعه کنید.

[مرجع ابزارهای داخلی](/docs/reference/tools-reference/)
[مرجع مجموعه ابزارها](/docs/reference/toolsets-reference/)

مشترکان Nous Portal پولی می‌توانند از جستجوی وب، تولید تصویر، TTS و اتوماسیون مرورگر از طریق دروازه ابزار استفاده کنند — بدون نیاز به کلیدهای API جداگانه. `hermes model` را اجرا کنید تا آن را فعال کنید، یا ابزارهای جداگانه را با `hermes tools` پیکربندی کنید.

[Nous Portal](https://portal.nousresearch.com)
[دروازه ابزار](/docs/user-guide/features/tool-gateway/)
`hermes model`
`hermes tools`

## استفاده از مجموعه ابزارها

```
# استفاده از مجموعه ابزارهای خاصhermes chat --toolsets "web,terminal"# مشاهده تمام ابزارهای موجودhermes tools# پیکربندی ابزارها به ازای هر پلتفرم (تعاملی)hermes tools
```

مجموعه ابزارهای رایج شامل `web`، `search`، `terminal`، `file`، `browser`، `vision`، `image_gen`، `skills`، `tts`، `todo`، `memory`، `session_search`، `cronjob`، `code_execution`، `delegation`، `clarify`، `homeassistant`، `messaging`، `spotify`، `discord`، `discord_admin`، `debugging` و `safe` است.

`web`
`search`
`terminal`
`file`
`browser`
`vision`
`image_gen`
`skills`
`tts`
`todo`
`memory`
`session_search`
`cronjob`
`code_execution`
`delegation`
`clarify`
`homeassistant`
`messaging`
`spotify`
`discord`
`discord_admin`
`debugging`
`safe`

برای مجموعه کامل، به مرجع مجموعه ابزارها مراجعه کنید، از جمله پیش‌فرض‌های پلتفرم مانند `hermes-cli`، `hermes-telegram` و مجموعه ابزارهای MCP پویا مانند `mcp-<server>`.

[مرجع مجموعه ابزارها](/docs/reference/toolsets-reference/)
`hermes-cli`
`hermes-telegram`
`mcp-<server>`

## پشتیبان‌های ترمینال

ابزار ترمینال می‌تواند دستورات را در محیط‌های مختلف اجرا کند:

| پشتیبان | توضیحات | مورد استفاده |
| --- | --- | --- |
| local | اجرا روی ماشین شما (پیش‌فرض) | توسعه، وظایف معتبر |
| docker | کانتینرهای ایزوله | امنیت، قابلیت بازتولید |
| ssh | سرور راه دور | sandboxing، دور نگه داشتن agent از کد خودش |
| singularity | کانتینرهای HPC | محاسبات خوشه‌ای، بدون root |
| modal | اجرای ابری | بدون سرور، مقیاس‌پذیری |
| daytona | فضای کاری sandbox ابری | محیط‌های توسعه راه دور ماندگار |

`local`
`docker`
`ssh`
`singularity`
`modal`
`daytona`

### پیکربندی

```
# در ~/.hermes/config.yamlterminal:  backend: local    # یا: docker, ssh, singularity, modal, daytona  cwd: "."          # دایرکتوری کاری  timeout: 180      # مهلت زمانی دستور بر حسب ثانیه
```

### پشتیبان Docker

```
terminal:  backend: docker  docker_image: python:3.11-slim
```

یک کانتینر ماندگار، به اشتراک گذاشته‌شده در سراسر فرآیند. Hermes یک کانتینر طولانی‌مدت در اولین استفاده راه‌اندازی می‌کند (`docker run -d ... sleep 2h`) و هر فراخوانی terminal، فایل و `execute_code` را از طریق `docker exec` به همان کانتینر مسیریابی می‌کند. تغییرات دایرکتوری کاری، پکیج‌های نصب‌شده، تنظیمات محیطی و فایل‌های نوشته‌شده در `/workspace` از یک فراخوانی ابزار به بعدی حمل می‌شوند، در سراسر subagentهای `/new`، `/reset` و `delegate_task`، در طول عمر فرآیند Hermes. کانتینر در هنگام خاموشی متوقف و حذف می‌شود.

`docker run -d ... sleep 2h`
`execute_code`
`docker exec`
`/workspace`
`/new`
`/reset`
`delegate_task`

این به این معنی است که پشتیبان Docker مانند یک VM sandbox ماندگار رفتار می‌کند، نه یک کانتینر تازه به ازای هر دستور. اگر یک بار `pip install foo` کنید، تا پایان نشست آنجا خواهد بود. اگر `cd /workspace/project` کنید، فراخوانی‌های `ls` بعدی آن دایرکتوری را می‌بینند. برای جزئیات کامل چرخه حیات و پرچم `container_persistent` که کنترل می‌کند آیا `/workspace` و `/root` از بازراه‌اندازی Hermes عبور می‌کنند یا نه، به پیکربندی → پشتیبان Docker مراجعه کنید.

`pip install foo`
`cd /workspace/project`
`ls`
[پیکربندی → پشتیبان Docker](/docs/user-guide/configuration#docker-backend)
`container_persistent`
`/workspace`
`/root`

### پشتیبان SSH

برای امنیت توصیه شده — agent نمی‌تواند کد خود را تغییر دهد:

```
terminal:  backend: ssh
```

```
# تنظیم اعتبارنامه‌ها در ~/.hermes/.envTERMINAL_SSH_HOST=my-server.example.comTERMINAL_SSH_USER=myuserTERMINAL_SSH_KEY=~/.ssh/id_rsa
```

### Singularity/Apptainer

```
# ساخت از پیش SIF برای کارگران موازیapptainer build ~/python.sif docker://python:3.11-slim# پیکربندیhermes config set terminal.backend singularityhermes config set terminal.singularity_image ~/python.sif
```

### Modal (سرور بدون سرور ابری)

```
uv pip install modalmodal setuphermes config set terminal.backend modal
```

### منابع کانتینر

پیکربندی CPU، حافظه، دیسک و ماندگاری برای تمام پشتیبان‌های کانتینر:

```
terminal:  backend: docker  # یا singularity, modal, daytona  container_cpu: 1              # هسته‌های CPU (پیش‌فرض: 1)  container_memory: 5120        # حافظه به مگابایت (پیش‌فرض: 5GB)  container_disk: 51200         # دیسک به مگابایت (پیش‌فرض: 50GB)  container_persistent: true    # ماندگاری فایل‌سیستم در نشست‌ها (پیش‌فرض: true)
```

هنگامی که `container_persistent: true` باشد، پکیج‌های نصب‌شده، فایل‌ها و پیکربندی در نشست‌ها باقی می‌مانند.

`container_persistent: true`

### امنیت کانتینر

تمام پشتیبان‌های کانتینر با تقویت امنیتی اجرا می‌شوند:

- فایل‌سیستم ریشه فقط خواندنی (Docker)
- تمام قابلیت‌های Linux حذف شده
- بدون ارتقای امتیاز
- محدودیت‌های PID (۲۵۶ پروسه)
- ایزولاسیون کامل فضای نام
- فضای کاری ماندگار از طریق volumeها، نه لایه ریشه نوشتنی

Docker به صورت اختیاری می‌تواند یک لیست مجاز صریح env از طریق `terminal.docker_forward_env` دریافت کند، اما متغیرهای forwarded برای دستورات داخل کانتینر قابل مشاهده هستند و باید به عنوان در معرض دید آن نشست در نظر گرفته شوند.

`terminal.docker_forward_env`

## مدیریت پروسه‌های پس‌زمینه

راه‌اندازی و مدیریت پروسه‌های پس‌زمینه:

```
terminal(command="pytest -v tests/", background=true)# برمی‌گرداند: {"session_id": "proc_abc123", "pid": 12345}# سپس با ابزار process مدیریت کنید:process(action="list")       # نمایش تمام پروسه‌های در حال اجرaprocess(action="poll", session_id="proc_abc123")   # بررسی وضعیتprocess(action="wait", session_id="proc_abc123")   # انتظار تا اتمامprocess(action="log", session_id="proc_abc123")    # خروجی کاملprocess(action="kill", session_id="proc_abc123")   # خاتمهprocess(action="write", session_id="proc_abc123", data="y")  # ارسال ورودی
```

حالت PTY (`pty=true`) ابزارهای CLI تعاملی مانند Codex و Claude Code را فعال می‌کند.

`pty=true`

## پشتیبانی Sudo

اگر یک دستور به sudo نیاز داشته باشد، از شما برای رمز عبور درخواست می‌شود (برای نشست کش شده). یا `SUDO_PASSWORD` را در `~/.hermes/.env` تنظیم کنید.

`SUDO_PASSWORD`
`~/.hermes/.env`

در پلتفرم‌های پیام‌رسانی، اگر sudo ناموفق باشد، خروجی شامل یک نکته برای اضافه کردن `SUDO_PASSWORD` به `~/.hermes/.env` است.

`SUDO_PASSWORD`
`~/.hermes/.env`
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/tools.md)
