---
layout: docs
title: "گیت‌وی‌های چند پروفایلی"
permalink: /docs/user-guide/multi-profile-gateways/
---

- 
- استفاده از Hermes
- اجرای همزمان چندین Gateway

# اجرای همزمان چندین Gateway

چندین **پروفایل** — هر کدام با توکن bot، جلسات و حافظه خود — را به عنوان سرویس‌های مدیریت‌شده روی یک ماشین واحد اجرا کنید. این صفحه نگرانی‌های عملیاتی را پوشش می‌دهد: شروع همه آن‌ها با هم، مشاهده لاگ‌ها در پروفایل‌ها، جلوگیری از خواب رفتن host و بازیابی از مشکلات رایج launchd/systemd.

[prefixes](/docs/user-guide/profiles/)

اگر فقط یک عامل Hermes اجرا می‌کنید، به این صفحه نیاز ندارید — به [پروفایل‌ها](/docs/user-guide/profiles/) برای مبانی مراجعه کنید.

[پروفایل‌ها](/docs/user-guide/profiles/)

## چه زمانی از این استفاده کنیم

وقتی دو یا چند عامل Hermes دارید که همه باید همزمان آنلاین باشند به این تنظیم نیاز دارید. دلایل رایج:

- یک دستیار شخصی روی یک bot Telegram و یک عامل کدنویسی روی دیگری
- یک عامل به ازای هر عضو خانواده یا یکی به ازای هر workspace Slack
- نمونه‌های sandbox + production از همان پیکربندی
- یک عامل تحقیقاتی + یک عامل نویسندگی + یک bot مبتنی بر cron — هر کدام با حافظه و مهارت‌های ایزوله

هر پروفایل در حال حاضر LaunchAgent به ازای هر پلتفرم (`ai.hermes.gateway-<name>.plist`) یا سرویس کاربر systemd (`hermes-gateway-<name>.service`) خود را دارد. این راهنما الگوهای مدیریت جمعی آن‌ها را اضافه می‌کند.

`ai.hermes.gateway-<name>.plist`
`hermes-gateway-<name>.service`

## شروع سریع

```
# Create profiles (once)
hermes profile create coder
hermes profile create personal-bot
hermes profile create research

# Configure each
coder setup
personal-bot setup
research setup

# Install each gateway as a managed service
coder gateway install
personal-bot gateway install
research gateway install

# Start them all
coder gateway start
personal-bot gateway start
research gateway start
```

همین است — سه عامل مستقل، هر کدام در فرایند خود، با ری‌استارت خودکار در صورت خرابی و ورود کاربر.

## جایگزین: یک gateway برای همه پروفایل‌ها (multiplexing)

مدل بالا **یک فرایند به ازای هر پروفایل** اجرا می‌کند. این پیش‌فرض است و برای بیشتر تنظیمات انتخاب درست است. اما روی host با پروفایل‌های زیاد — یا استقرار کانتینری که یک فرایند به ازای پروفایل از نظر عملیاتی سنگین است — می‌توانید به جای آن **یک gateway multiplexing واحد** اجرا کنید: gateway پروفایل پیش‌فرض به عنوان تنها فرایند ورودی تبدیل می‌شود و پیام‌ها را برای **هر** پروفایل روی ماشین سرویس می‌دهد.

این **اختیاری** و به طور پیش‌فرض **خاموش** است. وقتی خاموش است، هیچ چیز در این صفحه تغییر نمی‌کند — همه رفتارهای زیر غیرفعال هستند.

### چه زمانی multiplexing را ترجیح دهیم

- استقرار container/VPS که N واحد ناظر، N پورت و N فایل PID بار است.
- پروفایل‌های کم‌ترافیک زیاد که هر کدام یک فرایند کامل را توجیه نمی‌کنند.
- می‌خواهید یک چیز واحد برای شروع، نظارت و ری‌استارت داشته باشید.

وقتی ایزوله سخت سطح-فرایند بین پروفایل‌ها می‌خواهید ( ردپاهای حافظه جداگانه، دامنه‌های خرابی مستقل، توانایی ری‌استارت یک پروفایل بدون لمس دیگران) به یک فرایند-به-ازای-پروفایل بچسبید.

### نحوه فعال کردن

پرچم را روی **پروفایل پیش‌فرض** تنظیم کنید (مالک multiplexer) و gateway آن را ری‌استارت کنید:

```
hermes config set gateway.multiplex_profiles true
hermes gateway restart
```

یا معادل آن، در `~/.hermes/config.yaml` پروفایل پیش‌فرض:

`~/.hermes/config.yaml`

```
gateway:
  multiplex_profiles: true
```

(پرچم همچنین به عنوان `multiplex_profiles: true` سطح بالا برای راحتی پذیرفته می‌شود.) در شروع بعدی، gateway پیش‌فرض هر پروفایل را شمارش می‌کند، هر پلتفرم فعال هر پروفایل را با اعتبارات خود آن پروفایل بالا می‌آورد و هر پیام ورودی را به پروفایلی که به آن تعلق دارد مسیریابی می‌کند. هر نوبت پیکربندی، مهارت‌ها، حافظه، SOUL و کلیدهای ارائه‌دهنده پروفایل مسیریابی‌شده را حل می‌کند — اعتبارات هرگز بین پروفایل‌ها به اشتراک گذاشته نمی‌شوند.

`multiplex_profiles: true`

شما `hermes gateway start` را برای پروفایل‌های فرعی **اجرا نمی‌کنید** — gateway پیش‌فرض آن‌ها را سرویس می‌دهد. به تغییرات قراردادی زیر مراجعه کنید.

`hermes gateway start`

### چه چیزی وقتی multiplexing فعال است تغییر می‌کند

فعال کردن پرچم نحوه رفتار چند چیز را تغییر می‌دهد. همه آن‌ها لحظه‌ای که پرچم خاموش شود بازمی‌گردند.

#### 1. پروفایل‌های فرعی نباید gateway خود را شروع کنند

با multiplexer در حال اجرا، `hermes gateway start/run` یک پروفایل نام‌گذاری‌شده **خطای سخت** است و شما را به multiplexer بازمی‌گرداند:

`hermes gateway start`
`run`

```
The default gateway is running as a profile multiplexer and already serves
profile 'coder'. ...
```

multiplexer تنها فرایند ورودی است؛ یک دومین gateway پروفایل آن پلتفرم‌های آن پروفایل را bind مضاعف می‌کند. فقط در صورتی `--force` عبور دهید که عمداً یک فرایند جداگانه برای آن پروفایل می‌خواهید (توصیه نمی‌شود در حالی که multiplexer در حال اجراست). بنابراین اسکریپت wrapper چرخه حیات بین-پروفایلی در بالای این صفحه در حالت multiplex **استفاده نمی‌شود** — فقط gateway پیش‌efault را مدیریت می‌کنید.

`--force`

#### 2. پلتفرم‌های HTTP-ورودی از طریق پیشوند URL `/p/<profile>/` قابل دسترسی هستند

`/p/<profile>/`

ترافیک webhook (و سایر HTTP-ورودی) برای یک پروفایل فرعی روی listener پیش‌فرض تحت یک پیشوند پروفایل وارد می‌شود، **نه** یک پورت دوم:

```
# default profile
POST http://host:8644/webhooks/<route>

# the "coder" profile, same listener
POST http://host:8644/p/coder/webhooks/<route>
```

یک پروفایل ناشناخته یا پیکربندی‌نشده در پیشوند `404` برمی‌گرداند. چون یک listener مشترک واحد از این طریق هر پروفایل را سرویس می‌دهد، یک **پروفایل فرعی نباید پلتفرم bind-پورتی خود را فعال کند** — انجام این کار خطای پیکربندی است و gateway از شروع امتناع می‌کند و پروفایل و پلتفرم را نام می‌برد:

`404`

```
Profile 'coder' enables the port-binding platform 'webhook', but
gateway.multiplex_profiles is on. ... Remove platforms.webhook from profile
'coder's config.yaml (configure it only on the default profile).
```

پلتفرم‌های bind-پورتی تحت این قانون: `webhook`، `api_server`، `msgraph_webhook`، `feishu`، `wecom_callback`، `bluebubbles`، `sms`. هر کدام از این‌ها را **فقط روی پروفایل پیش‌فرض** پیکربندی کنید؛ هر پروفایل از طریق پیشوند `/p/<profile>/` خود قابل دسترسی است.

`webhook`
`api_server`
`msgraph_webhook`
`feishu`
`wecom_callback`
`bluebubbles`
`sms`
`/p/<profile>/`

#### 3. پلتفرم‌های به ازای اعتبار همچنان به توکن جداگانه به ازای هر پروفایل نیاز دارند

پلتفرم‌های polling/اتصال (Telegram, Discord, Slack, Matrix, Signal و ...) به صورت multiplexed خوب کار می‌کنند، اما هر پروفایلی که یکی را فعال می‌کند باید توکن bot **خود** را ارائه دهد — همان توکن نمی‌تواند توسط دو پروفایل همزمان polling شود. اگر دو پروفایل همان `(platform, token)` را پیکربندی کنند، شروع با سرعت بالا شکست می‌خورد و هر دو پروفایل را نام می‌برد (به [ایمنی تداخل توکن](#token-conflict-safety) مراجعه کنید — قانون تغییر نکرده، فقط اکنون داخل یک فرایند اجرا می‌شود).

`(platform, token)`

#### 4. کلیدهای جلسه بر اساس پروفایل namespace دارند

جلسات هر پروفایل تحت namespace `agent:<profile>:…` زندگی می‌کنند بنابراین دو پروفایل روی همان پلتفرم/چت هرگز در فروشگاه جلسه مشترک تداخل نمی‌کنند. پروفایل **پیش‌فرض** namespace تاریخی `agent:main:…` را byte-for-byte حفظ می‌کند، بنابراین جلسات پروفایل پیش‌فرض موجود تحت تأثیر قرار نمی‌گیرند — بدون مهاجرت، بدون تاریخچه یتیم.

`agent:<profile>:…`
`agent:main:…`

#### 5. یک PID/lock و یک سطح وضعیت واحد

یک PID و lock سطح-فرایند واحد وجود دارد (multiplexer، تحت خانه پیش‌فرض). `hermes status` multiplexer و پروفایل‌هایی که سرویس می‌دهد را گزارش می‌دهد؛ `hermes status -p <name>` روی یک پروفایل برش می‌زند. هر پروفایل همچنان `runtime_status.json` خود را تحت خانه خود می‌نویسد، بنابراین خوانندگان به ازای پروفایل موجود همچنان کار می‌کنند.

`hermes status`
`hermes status -p <name>`
`runtime_status.json`

#### چه چیزی **تغییر نمی‌کند**

ایزوله اعتبار `.env` به ازای پروفایل حفظ شده و در واقع **دقیق‌تر** است: کلیدهای یک پروفایل از دامنه خود حل می‌شوند و هرگونه unioned به محیط مشترک نمی‌شوند (این همچنین به این معنی است که فرایندهای فرعی مانند سرورهای MCP و کارگران Kanban فقط رمزهای عبور پروفایل خود را می‌بینند). Kanban، مهارت‌ها/حافظه/SOUL به ازای پروفایل و مسیریابی مدل همگی دقیقاً به ازای پروفایل رفتار می‌کنند مانند gateway‌های جداگانه.

`.env`

## شروع، توقف یا ری‌استارت همزمان همه gateway‌ها

CLI با دستورات چرخه حیات به ازای پروفایل واحد عرضه می‌شود. برای عمل در هر پروفایل، آن‌ها را در یک حلقه shell بپیچید. قطعه زیر را در `~/.local/bin/hermes-gateways` قرار دهید و `chmod +x` کنید:

`~/.local/bin/hermes-gateways`
`chmod +x`

```
#!/bin/sh
set -eu
# Add or remove profile names here as you create / delete profiles.
profiles="default coder personal-bot research"
usage() {  echo "Usage: hermes-gateways {start|stop|restart|status|list}"}
run_for_profile() {  profile="$1"  action="$2"
  if [ "$profile" = "default" ]; then
    hermes gateway "$action"
  else
    hermes -p "$profile" gateway "$action"
  fi
}
action="${1:-}"
case "$action" in
  start|stop|restart|status)
    for profile in $profiles; do
      echo "==> $action $profile"
      run_for_profile "$profile" "$action"
    done
    ;;
  list)    hermes gateway list    ;;
  *)    usage    exit 2    ;;
esac
```

سپس:

```
hermes-gateways start      # start every configured profile
hermes-gateways stop       # stop every configured profile
hermes-gateways restart    # restart all
hermes-gateways status     # status across all
hermes-gateways list       # delegates to `hermes gateway list`
```

پروفایل **پیش‌فرض** با `hermes gateway <action>` (بدون `-p`) هدف گرفته می‌شود، **نه** `hermes -p default gateway <action>`. wrapper بالا هر دو فرم را مدیریت می‌کند.

`default`
`hermes gateway <action>`
`-p`
`hermes -p default gateway <action>`

## مدیریت یک پروفایل

دستورات میانبری که هر پروفایل نصب می‌کند:

```
coder gateway run        # foreground (Ctrl-C to stop)
coder gateway start      # start the managed service
coder gateway stop       # stop the managed service
coder gateway restart    # restart
coder gateway status     # status
coder gateway install    # create the LaunchAgent / systemd unit
coder gateway uninstall  # remove the service file
```

این‌ها معادل `hermes -p coder gateway <action>` هستند — مفید وقتی نام مستعار پروفایل در `PATH` نیست یا پروفایل‌ها را به طور پویا از یک اسکریپت هدف می‌دهید.

`hermes -p coder gateway <action>`
`PATH`

## فایل‌های سرویس

هر پروفایل سرویس خود را با نام یکتا نصب می‌کند، بنابراین نصب‌ها هرگز تداخل ندارند:

| پلتفرم | مسیر |
| --- | --- |
| macOS | `~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist` |
| Linux | `~/.config/systemd/user/hermes-gateway-<profile>.service` |

`~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist`
`~/.config/systemd/user/hermes-gateway-<profile>.service`

پروفایل پیش‌فرض نام‌های تاریخی را حفظ می‌کند: `ai.hermes.gateway.plist` / `hermes-gateway.service`.

`ai.hermes.gateway.plist`
`hermes-gateway.service`

## مشاهده لاگ‌ها

هر پروفایل در فایل‌های لاگ خود می‌نویسد:

```
# Default profile
tail -f ~/.hermes/logs/gateway.log
tail -f ~/.hermes/logs/gateway.error.log

# Named profile
tail -f ~/.hermes/profiles/<name>/logs/gateway.log
tail -f ~/.hermes/profiles/<name>/logs/gateway.error.log
```

لاگ هر پروفایل را همزمان استریم کنید:

```
tail -f ~/.hermes/logs/gateway.log ~/.hermes/profiles/*/logs/gateway.log
```

CLI همچنین یک مشاهده‌گر لاگ ساختاریافته دارد:

```
hermes logs -f                  # follow default profile
hermes -p coder logs -f         # follow one profile
hermes logs --help              # filters, levels, JSON output
```

## شناسایی آنچه واقعاً در حال اجراست

```
hermes profile list             # profiles + model + gateway state
hermes-gateways status          # full status across every profile
launchctl list | grep hermes    # macOS — PIDs and labels
systemctl --user list-units 'hermes-gateway-*'   # Linux — units
```

## ویرایش پیکربندی

هر پروفایل پیکربندی خود را در دایرکتوری خود نگه می‌دارد:

```
~/.hermes/profiles/<name>/
├── .env              # API keys, bot tokens (chmod 600)
├── config.yaml       # model, provider, toolsets, gateway settings
└── SOUL.md           # personality / system prompt
```

پروفایل پیش‌فرض مستقیماً از `~/.hermes/` با همان سه فایل استفاده می‌کند.

`~/.hermes/`

آن‌ها را با هر ویرایشگر یا از طریق CLI ویرایش کنید:

```
hermes config set model.model anthropic/claude-sonnet-4    # default profile
coder config set model.model openai/gpt-5                  # named profile
```

پس از ویرایش `.env` یا `config.yaml`، gateway تحت تأثیر را ری‌استارت کنید:

`.env`
`config.yaml`

```
coder gateway restart
# or, for everything:
hermes-gateways restart
```

## بیدار نگه داشتن host

فرایند gateway می‌تواند تمام روز اجرا شود، اما سیستم‌عامل همچنان سعی می‌کند در حالت بیکاری بخوابد. دو الگو:

### macOS — `caffeinate`

`caffeinate`

`caffeinate` در macOS داخلی است و در حال اجرا از خواب جلوگیری می‌کند. نیازی به نصب نیست.

`caffeinate`

```
caffeinate -dis                    # block display, idle, and system sleep
caffeinate -dis -t 28800           # same, auto-exit after 8 hours
caffeinate -i -w $(cat ~/.hermes/gateway.pid) &   # awake while default gateway runs
# Persistent: run in background and forget
nohup caffeinate -dis >/dev/null 2>&1 &
disown
# Inspect / stop
pmset -g assertions | grep -iE 'caffeinate|prevent|user is active'
pkill caffeinate
```

| پرچم | اثر |
| --- | --- |
| `-d` | مسدود کردن خواب نمایشگر |
| `-i` | مسدود کردن خواب بیکار سیستم (پیش‌فرض) |
| `-m` | مسدود کردن خواب دیسک |
| `-s` | مسدود کردن خواب سیستم (فقط Macهای AC-powered) |
| `-u` | شبیه‌سازی فعالیت کاربر (از قفل صفحه جلوگیری می‌کند) |
| `-t N` | خروج خودکار پس از N ثانیه |
| `-w P` | خروج وقتی PID P خارج شود |

`-d`
`-i`
`-m`
`-s`
`-u`
`-t N`
`N`
`-w P`
`P`

`caffeinate` نمی‌تواند خواب بستن درب سخت‌افزاری را در MacBooks باطل کند. برای عملکرد با درب بسته، تنظیمات Energy Saver / Battery خود را تغییر دهید یا از ابزار شخص ثالث استفاده کنید.

`caffeinate`

### Linux — `systemd-inhibit` / `loginctl`

`systemd-inhibit`
`loginctl`

```
# Inhibit suspend while a command runs
systemd-inhibit --what=idle:sleep --who=hermes --why="gateways running" \
  sleep infinity &

# Allow user services to keep running after logout (recommended)
sudo loginctl enable-linger "$USER"
```

پس از فعال کردن lingering، واحدهای کاربر systemd شما (از جمله `hermes-gateway-<profile>.service`) در قطع اتصال SSH و ری‌استارت‌ها به اجرا ادامه می‌دهند.

`hermes-gateway-<profile>.service`

## ایمنی تداخل توکن

هر پروفایل باید توکن‌های bot یکتا برای هر پلتفرم استفاده کند. اگر دو پروفایل توکن Telegram، Discord، Slack، WhatsApp یا Signal را به اشتراک بگذارند، دومین gateway با خطایی که پروفایل متعارض را نام می‌برد از شروع امتناع می‌کند.

برای ممیزی:

```
grep -H 'TELEGRAM_BOT_TOKEN\|DISCORD_BOT_TOKEN' \
     ~/.hermes/.env ~/.hermes/profiles/*/.env
```

## به‌روزرسانی کد

`hermes update` آخرین کد را یک بار دریافت می‌کند و مهارت‌های بسته‌شده جدید را به هر پروفایل همگام‌سازی می‌کند:

`hermes update`

```
hermes update
hermes-gateways restart
```

مهارت‌های تغییریافته توسط کاربر هرگز بازنویسی نمی‌شوند.

## عیب‌یابی

### «Could not find service in domain for user gui: 501»

`hermes gateway start` را پس از `hermes gateway stop` قبلی اجرا کرده‌اید. `stop` CLI یک `launchctl unload` کامل انجام می‌دهد که سرویس را از رجیستری launchd حذف می‌کند. CLI این خطای خاص را در `start` می‌گیرد و به طور خودکار plist را دوباره بارگذاری می‌کند (↻ launchd job was unloaded; reloading service definition). سرویس به طور عادی شروع می‌شود. چیزی برای رفع نیست.

`hermes gateway start`
`hermes gateway stop`
`stop`
`launchctl unload`
`start`
`↻ launchd job was unloaded; reloading service definition`

### PID قدیمی پس از خرابی

اگر gateway پروفایلی `not running` نشان دهد اما فرایند هنوز زنده باشد:

`not running`

```
ps -ef | grep "hermes_cli.*-p <profile>"
cat ~/.hermes/profiles/<profile>/gateway.pid
kill -TERM <pid>          # graceful
kill -KILL <pid>          # if that fails after a few seconds
<profile> gateway start
```

### اجبار ریست سخت یک سرویس

```
# macOS
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist
launchctl load   ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist

# Linux
systemctl --user restart hermes-gateway-<profile>.service
```

### بررسی سلامت

```
hermes doctor                  # default profile
hermes -p <profile> doctor     # one profile
```

[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/multi-profile-gateways.md)