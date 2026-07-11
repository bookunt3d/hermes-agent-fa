---
layout: docs
title: "پروفایل‌ها"
permalink: /docs/user-guide/profiles/
---

- 
- استفاده از Hermes
- پروفایل‌ها: اجرای عوامل متعدد

# پروفایل‌ها: اجرای عوامل متعدد

چندین عامل Hermes مستقل را روی یک ماشین اجرا کنید — هر کدام با پیکربندی، کلیدهای API، حافظه، جلسات، مهارت‌ها و وضعیت gateway خود.

## پروفایل‌ها چیست؟

یک پروفایل یک دایرکتوری خانه Hermes جداگانه است. هر پروفایل دایرکتوری خود را با `config.yaml`، `.env`، `SOUL.md`، حافظه‌ها، جلسات، مهارت‌ها، کارهای cron و پایگاه داده وضعیت خود دریافت می‌کند. پروفایل‌ها به شما اجازه می‌دهند عوامل جداگانه‌ای برای اهداف مختلف اجرا کنید — یک دستیار کدنویسی، یک ربات شخصی، یک عامل تحقیقاتی — بدون مخلوط کردن وضعیت Hermes.

`config.yaml`
`.env`
`SOUL.md`

وقتی یک پروفایل ایجاد می‌کنید، به طور خودکار به عنوان دستور خودش تبدیل می‌شود. یک پروفایل به نام `coder` ایجاد کنید و بلافاصله `coder chat`، `coder setup`، `coder gateway start` و غیره دارید.

`coder`
`coder chat`
`coder setup`
`coder gateway start`

## شروع سریع

```
hermes profile create coder       # creates profile + "coder" command alias
coder setup                       # configure API keys and model
coder chat                        # start chatting
```

همین است. `coder` اکنون پروفایل Hermes خودش با پیکربندی، حافظه و وضعیت خود است.

`coder`

## ایجاد پروفایل

سریع‌ترین راه‌اندازی: `hermes setup --portal` را داخل پروفایل جدید اجرا کنید تا مدل‌ها + ابزارها را یکجا راه‌اندازی کنید. به [Nous Portal](/docs/integrations/nous-portal/) مراجعه کنید.

`hermes setup --portal`
[Nous Portal](/docs/integrations/nous-portal/)

### پروفایل خالی

```
hermes profile create mybot
```

یک پروفایل جدید با مهارت‌های بسته‌شده ایجاد می‌کند. `mybot setup` را اجرا کنید تا کلیدهای API، مدل و توکن‌های gateway را پیکربندی کنید.

`mybot setup`

اگر قصد دارید این پروفایل را به عنوان کارگر kanban استفاده کنید (یا می‌خواهید orchestrator kanban کار را به آن مسیریابی کند)، `--description "<role>"` را در زمان ایجاد عبور دهید تا orchestrator بداند در چه چیزی خوب است:

`--description "<role>"`

```
hermes profile create researcher --description "Reads source code and external docs, writes findings."
```

همچنین می‌توانید توصیف را بعداً با `hermes profile describe` تنظیم یا به طور خودکار تولید کنید — به [راهنمای Kanban](/docs/user-guide/features/kanban#auto-vs-manual-orchestration) برای مدل مسیریابی کامل مراجعه کنید.

`hermes profile describe`
[راهنمای Kanban](/docs/user-guide/features/kanban#auto-vs-manual-orchestration)

### کلون فقط پیکربندی (--clone)

`--clone`

```
hermes profile create work --clone
```

`config.yaml`، `.env`، `SOUL.md` و مهارت‌های پروفایل فعلی شما را به پروفایل جدید کپی می‌کند. همان کلیدهای API، مدل و قابلیت‌ها، اما جلسات و حافظه جدید. `~/.hermes/profiles/work/.env` را برای کلیدهای API متفاوت یا `~/.hermes/profiles/work/SOUL.md` را برای شخصیت متفاوت ویرایش کنید.

`config.yaml`
`.env`
`SOUL.md`
`~/.hermes/profiles/work/.env`
`~/.hermes/profiles/work/SOUL.md`

### کلون همه چیز (--clone-all)

`--clone-all`

```
hermes profile create backup --clone-all
```

**همه چیز** را کپی می‌کند — پیکربندی، کلیدهای API، شخصیت، همه حافظه‌ها، مهارت‌ها، کارهای cron، پلاگین‌ها. یک اسکنپشت کاری کامل. تاریخچه به ازای پروفایل حذف شده (تاریخچه جلسات، `state.db`، `backups/`، `state-snapshots/`، `checkpoints/`) — این‌ها متعلق به پروفایل منبع هستند و می‌توانند ده‌ها GB باشند. برای پشتیبان کامل شامل تاریخچه، از `hermes profile export` یا `hermes backup` استفاده کنید.

`state.db`
`backups/`
`state-snapshots/`
`checkpoints/`
`hermes profile export`
`hermes backup`

### کلون از یک پروفایل خاص

```
hermes profile create work --clone-from coder
```

`--clone-from <source>` پروفایل منبع را مستقیماً انتخاب می‌کند و کلون پیکربندی/مهارت/SOUL را تلویحاً شامل می‌شود. آن را با `--clone-all` ترکیب کنید وقتی کپی کامل آن پروفایل منبع را می‌خواهید:

`--clone-from <source>`
`--clone-all`

```
hermes profile create work-backup --clone-from coder --clone-all
```

وقتی Honcho فعال است، عملیات کلون به طور خودکار یک AI peer اختصاصی برای پروفایل جدید ایجاد می‌کند در حالی که فضای کاری کاربر مشترک را به اشتراک می‌گذارد. هر پروفایل مشاهدات و هویت خود را می‌سازد. به [Honcho — Multi-agent / Profiles](/docs/user-guide/features/memory-providers#honcho) برای جزئیات مراجعه کنید.

[Honcho — Multi-agent / Profiles](/docs/user-guide/features/memory-providers#honcho)

## استفاده از پروفایل‌ها

### نام‌های مستعار دستوری

هر پروفایل به طور خودکار یک نام مستعار دستوری در `~/.local/bin/<name>` دریافت می‌کند:

`~/.local/bin/<name>`

```
coder chat                    # chat with the coder agent
coder setup                   # configure coder's settings
coder gateway start           # start coder's gateway
coder doctor                  # check coder's health
coder skills list             # list coder's skills
coder config set model.default anthropic/claude-sonnet-4
```

نام مستعار با هر زیردستور hermes کار می‌کند — فقط `hermes -p <name>` در پشت صحنه است.

`hermes -p <name>`

### پرچم `-p`

`-p`

همچنین می‌توانید به طور صریح با هر دستوری به یک پروفایل هدف بدهید:

```
hermes -p coder chat
hermes --profile=coder doctor
hermes chat -p coder -q "hello"    # works in any number
```

### پیش‌فرض چسبناک (hermes profile use)

`hermes profile use`

```
hermes profile use coder
hermes chat                   # now targets coder
hermes tools                  # configures coder's tools
hermes profile use default    # switch back
```

یک پیش‌فرض تنظیم می‌کند تا دستورات `hermes` ساده آن پروفایل را هدف بگیرند. مشابه `kubectl config use-context`.

`hermes`
`kubectl config use-context`

### دانستن موقعیت فعلی

CLI همیشه نشان می‌دهد کدام پروفایل فعال است:

- پرامپت: `coder ❯` به جای `❯`
- بنر: `Profile: coder` را در شروع نشان می‌دهد
- `hermes profile`: نام پروفایل فعلی، مسیر، مدل، وضعیت gateway را نشان می‌دهد

`coder ❯`
`❯`
`Profile: coder`
`hermes profile`

## پروفایل‌ها در مقابل workspace‌ها در مقابل sandboxing

پروفایل‌ها اغلب با workspace‌ها یا sandbox‌ها اشتباه گرفته می‌شوند، اما چیزهای متفاوتی هستند:

- یک **پروفایل** به Hermes دایرکتوری وضعیت جداگانه می‌دهد: `config.yaml`، `.env`، `SOUL.md`، جلسات، حافظه، لاگ‌ها، کارهای cron و وضعیت gateway.
- یک **workspace** یا **دایرکتوری کاری** جایی است که دستورات terminal شروع می‌شوند. این توسط `terminal.cwd` به صورت جداگانه کنترل می‌شود.
- یک **sandbox** چیزی است که دسترسی فایل‌سیستم را محدود می‌کند. پروفایل‌ها عامل را **sandbox نمی‌کنند**.

`config.yaml`
`.env`
`SOUL.md`
`terminal.cwd`

در backend `local` پیش‌فرض، عامل همچنان همان دسترسی فایل‌سیستم حساب کاربری شما را دارد. یک پروفایل مانع از دسترسی به پوشه‌های خارج از دایرکتوری پروفایل نمی‌شود.

`local`

اگر می‌خواهید یک پروفایل در یک پوشه پروژه خاص شروع شود، یک `terminal.cwd` مطلق صریح در `config.yaml` آن پروفایل تنظیم کنید:

`terminal.cwd`
`config.yaml`

```
terminal:
  backend: local
  cwd: /absolute/path/to/project
```

استفاده از `cwd: "."` در backend local به معنای «دایرکتوری که Hermes از آن راه‌اندازی شده» است، نه «دایرکتوری پروفایل».

`cwd: "."`

همچنین توجه کنید:

- `SOUL.md` می‌تواند مدل را راهنمایی کند، اما مرز workspace را اجرا نمی‌کند.
- تغییرات در `SOUL.md` در نشست جدید تمیز اعمال می‌شوند. نشست‌های موجود ممکن است هنوز از وضعیت پرامپت قدیمی استفاده کنند.
- پرسیدن از مدل «در چه دایرکتوری هستی؟» یک آزمون ایزوله قابل اعتماد نیست. اگر به دایرکتوری شروع قابل پیش‌بینی برای ابزارها نیاز دارید، `terminal.cwd` را به طور صریح تنظیم کنید.

`SOUL.md`
`SOUL.md`
`terminal.cwd`

## اجرای gateway‌ها

هر پروفایل gateway خود را به عنوان یک فرایند جداگانه با توکن bot خود اجرا می‌کند:

```
coder gateway start           # starts coder's gateway
assistant gateway start       # starts assistant's gateway (separate process)
```

### توکن‌های bot متفاوت

هر پروفایل فایل `.env` خود را دارد. یک توکن Telegram/Discord/Slack bot متفاوت در هر کدام پیکربندی کنید:

`.env`

```
# Edit coder's tokens
nano ~/.hermes/profiles/coder/.env

# Edit assistant's tokens
nano ~/.hermes/profiles/assistant/.env
```

### ایمنی: قفل‌های توکن

اگر دو پروفایل به طور تصادفی از همان توکن bot استفاده کنند، دومین gateway با خطای واضحی که پروفایل متعارض را نام می‌برد مسدود می‌شود. برای Telegram، Discord، Slack، WhatsApp و Signal پشتیبانی می‌شود.

### سرویس‌های ماندگار

```
coder gateway install         # creates hermes-gateway-coder systemd/launchd service
assistant gateway install     # creates hermes-gateway-assistant service
```

هر پروفایل نام سرویس جداگانه خود را دریافت می‌کند. مستقل اجرا می‌شوند.

gateway‌های به ازای پروفایل توسط **s6-overlay** (PID 1 در کانتینر) نظارت می‌شوند، بنابراین `hermes profile create <name>` به طور خودکار یک اسلات سرویس s6 در `/run/service/gateway-<name>/` ثبت می‌کند. `hermes -p <name> gateway start/stop/restart` به جای فرایند خام، به `s6-svc` ارسال می‌کند — خرابی‌ها به طور خودکار ری‌استارت می‌شوند و `docker restart` مجموعه gateway‌های قبلاً در حال اجرای حفظ شده را حفظ می‌کند. به [نظارت gateway به ازای پروفایل](/docs/user-guide/docker#per-profile-gateway-supervision) برای جزئیات مراجعه کنید.

[s6-overlay](https://github.com/just-containers/s6-overlay)
`hermes profile create <name>`
`/run/service/gateway-<name>/`
`hermes -p <name> gateway start/stop/restart`
`s6-svc`
`docker restart`
[نظارت gateway به ازای پروفایل](/docs/user-guide/docker#per-profile-gateway-supervision)

## پیکربندی پروفایل‌ها

هر پروفایل موارد زیر را دارد:

- `config.yaml` — مدل، ارائه‌دهنده، مجموعه‌ابزارها، همه تنظیمات
- `.env` — کلیدهای API، توکن‌های bot
- `SOUL.md` — شخصیت و دستورالعمل‌ها

`config.yaml`
`.env`
`SOUL.md`

```
coder config set model.default anthropic/claude-sonnet-4
echo "You are a focused coding assistant." > ~/.hermes/profiles/coder/SOUL.md
```

اگر می‌خواهید این پروفایل به طور پیش‌فرض در یک پروژه خاص کار کند، همچنین `terminal.cwd` خودش را تنظیم کنید:

`terminal.cwd`

```
coder config set terminal.cwd /absolute/path/to/project
```

### از داشبورد

[وب داشبورد](/docs/user-guide/features/web-dashboard#managing-multiple-profiles) یک سطح سطح-ماشین است که می‌تواند پیکربندی، کلیدهای API، مهارت‌ها، MCP‌ها و مدل **هر** پروفایلی را از طریق switcher در نوار کناری مدیریت کند — به داشبورد به ازای هر پروفایل نیاز نیست. `coder dashboard` به داشبورد ماشین با پروفایل `coder` از پیش انتخاب‌شده مسیریابی می‌کند. تب Chat داشبورد نیز از switcher پیروی می‌کند و مکالمه‌ای را تحت خانه پروفایل انتخابی راه‌اندازی می‌کند.

[وب داشبورد](/docs/user-guide/features/web-dashboard#managing-multiple-profiles)
`coder dashboard`
`coder`

توجه: «تنظیم به عنوان فعال» در صفحه Profile‌های داشبورد پیش‌فرض **چسبناک** برای اجرای‌های **آینده** CLI/gateway است (مشابه `hermes profile use`) — برای ویرایش پروفایل از داشبورد، به جای آن از switcher استفاده کنید.

`hermes profile use`

## به‌روزرسانی

`hermes update` کد را یک بار (مشترک) دریافت می‌کند و مهارت‌های بسته‌شده جدید را به **همه** پروفایل‌ها به طور خودکار همگام‌سازی می‌کند:

`hermes update`

```
hermes update
# → Code updated (12 commits)
# → Skills synced: default (up to date), coder (+2 new), assistant (+2 new)
```

مهارت‌های تغییریافته توسط کاربر هرگز بازنویسی نمی‌شوند.

## مدیریت پروفایل‌ها

```
hermes profile list           # show all profiles with status
hermes profile show coder     # detailed info for one profile
hermes profile rename coder dev-bot   # rename (updates alias + service)
hermes profile export coder   # export to coder.tar.gz
hermes profile import coder.tar.gz   # import from archive
```

## حذف پروفایل

```
hermes profile delete coder
```

پیام حذف اطلاعات پروفایل را قبل از درخواست تأیید نشان می‌دهد:

```
Profile: research-bot
Path:    ~/.hermes/profiles/research-bot
Model:   claude-opus-4 (anthropic)
Skills:  12
Distribution: research-bot@1.0.0
Installed from: https://github.com/you/research-bot
This will permanently delete:
  • All config, API keys, memories, sessions, skills, cron jobs
  • Command alias (~/.local/bin/research-bot)
Type 'research-bot' to confirm:
```

بنابراین هرگز به طور تصادفی یک عامل را بدون دانستن منشأ آن یا بدون توانایی نصب مجدد حذف نمی‌کنید.

از `--yes` برای رد کردن تأیید استفاده کنید: `hermes profile delete coder --yes`

`--yes`
`hermes profile delete coder --yes`

نمی‌توانید پروفایل پیش‌فرض (`~/.hermes`) را حذف کنید. برای حذف همه چیز، از `hermes uninstall` استفاده کنید.

`~/.hermes`
`hermes uninstall`

## تکمیل Tab

```
# Bash
eval "$(hermes completion bash)"

# Zsh
eval "$(hermes completion zsh)"
```

خط را به `~/.bashrc` یا `~/.zshrc` خود اضافه کنید برای تکمیل ماندگار. نام‌های پروفایل پس از `-p`، زیردستورهای پروفایل و دستورات سطح بالا را تکمیل می‌کند.

`~/.bashrc`
`~/.zshrc`
`-p`

## نحوه کار

پروفایل‌ها از متغیر محیطی `HERMES_HOME` استفاده می‌کنند. وقتی `coder chat` را اجرا می‌کنید، اسکریپت wrapper قبل از راه‌اندازی hermes `HERMES_HOME=~/.hermes/profiles/coder` را تنظیم می‌کند. از آنجا که 119+ فایل در پایگاه کد مسیرها را از طریق `get_hermes_home()` حل می‌کنند، وضعیت Hermes به طور خودکار به دایرکتوری پروفایل محدود می‌شود — پیکربندی، جلسات، حافظه، مهارت‌ها، پایگاه داده وضعیت، PID gateway، لاگ‌ها و کارهای cron.

`HERMES_HOME`
`coder chat`
`HERMES_HOME=~/.hermes/profiles/coder`
`get_hermes_home()`

این از دایرکتوری کاری terminal جداگانه است. اجرای ابزار از `terminal.cwd` (یا دایرکتوری راه‌اندازی وقتی `cwd: "."` در backend local) شروع می‌شود، نه به طور خودکار از `HERMES_HOME`.

`terminal.cwd`
`cwd: "."`
`HERMES_HOME`

در نصب‌های host، فرایندهای فرعی ابزار `HOME` واقعی OS-کاربر شما را به طور پیش‌فرض حفظ می‌کنند تا اعتبارات CLI موجود زیر `~` در پروفایل‌ها کار کنند. داده‌های پروفایل توسط `HERMES_HOME` ایزوله می‌شوند، نه با تغییر `HOME`. Backend‌های کانتینر همچنان از `{HERMES_HOME}/home` برای وضعیت ابزار ماندگار استفاده می‌کنند و کاربران host که به پیکربندی دقیق ابزار به ازای پروفایل نیاز دارند می‌توانند با `terminal.home_mode: profile` opted-in شوند.

`HOME`
`~`
`HERMES_HOME`
`HOME`
`{HERMES_HOME}/home`
`terminal.home_mode: profile`

این دو چیز را به همراه دارد که اشتباه گرفتن آن‌ها آسان است:

- `HERMES_HOME` مرز پروفایل است. پیکربندی Hermes، `.env`، حافظه، جلسات، مهارت‌ها، لاگ‌ها، کارهای cron، وضعیت gateway و سایر داده‌های Hermes را کنترل می‌کند.
- `HOME` سیستم‌عامل/خانه کاربری است که CLI‌های خارجی انتظار آن را دارند. در نصب‌های host، Hermes آن را به طور پیش‌فرض به عنوان خانه کاربر واقعی حفظ می‌کند تا ابزارهایی مانند `git`، `ssh`، `gh`، `az`، `npm`، Claude Code و Codex همان اعتباراتی را که در shell عادی شما استفاده می‌کنند پیدا کنند.

`HERMES_HOME`
`.env`
`HOME`
`git`
`ssh`
`gh`
`az`
`npm`

-tradeoff این است که پروفایل‌های host به طور پیش‌فرض وضعیت CLI سطح-کاربر عادی را به اشتراک می‌گذارند. اگر به هویت‌های CLI جداگانه به ازای هر پروفایل نیاز دارید، `terminal.home_mode: profile` را در `config.yaml` آن پروفایل تنظیم کنید. در آن حالت Hermes فرایندهای فرعی ابزار را با `HOME={HERMES_HOME}/home` راه‌اندازی می‌کند؛ سپس باید `~/.ssh`، `~/.gitconfig`، `~/.config/gh`، احراز هویت CLI ابری، احراز هویت Claude/Codex، وضعیت npm و فایل‌های مشابه را در آن خانه پروفایل مقداردهی اولیه یا لینک کنید.

`terminal.home_mode: profile`
`config.yaml`
`HOME={HERMES_HOME}/home`
`~/.ssh`
`~/.gitconfig`
`~/.config/gh`

Hermes همچنین `HERMES_REAL_HOME` را به فرایندهای فرعی نشان می‌دهد تا اسکریپت‌ها همچنان بتوانند خانه حساب واقعی را وقتی `home_mode: profile` فعال است پیدا کنند.

`HERMES_REAL_HOME`
`home_mode: profile`

پروفایل پیش‌فرض `~/.hermes` خودش است. نیازی به مهاجرت نیست — نصب‌های موجود به یک شکل کار می‌کنند.

`~/.hermes`

## به اشتراک گذاری پروفایل‌ها به عنوان توزیع‌ها

یک پروفایل که روی یک ماشین ساخته‌اید می‌تواند به عنوان یک **مخزن git** بسته‌بندی شود و با یک دستور روی ماشین دیگر نصب شود — ایستگاه کاری خودتان، لپ‌تاپ همکار یا محیط کاربر جامعه. بسته مشترک شامل SOUL، پیکربندی، مهارت‌ها، کارهای cron و اتصالات MCP است. اعتبارات، حافظه‌ها و جلسات به ازای ماشین باقی می‌مانند.

```
# Install a whole agent from a git repo
hermes profile install github.com/you/research-bot --alias

# Update later when the author ships a new version (keeps your memories + .env)
hermes profile update research-bot
```

به [توزیع‌های پروفایل: به اشتراک گذاری یک عامل کامل](/docs/user-guide/profile-distributions/) برای راهنمای کامل — نگارش، انتشار، معناشناسی به‌روزرسانی، مدل امنیتی و موارد استفاده مراجعه کنید.

[توزیع‌های پروفایل: به اشتراک گذاری یک عامل کامل](/docs/user-guide/profile-distributions/)
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/profiles.md)