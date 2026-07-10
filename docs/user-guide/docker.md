---
layout: docs
title: "Docker"
permalink: /user-guide/docker/
---

- 
- استفاده از Hermes
- Docker

# Hermes Agent — Docker

دو روش متمایز وجود دارد که Docker با Hermes Agent تلاقی می‌کند:

1. اجرای Hermes در Docker — خود عامل در داخل یک container اجرا می‌شود (تمرکز اصلی این صفحه)
2. Docker به عنوان backend ترمینال — عامل روی میزبان شما اجرا می‌شود اما هر دستور را در داخل یک Docker sandbox container مستقل و پایدار که در طول زندگی فرآیند Hermes در برابر فراخوانی‌های ابزار، `/new` و زیرعاملان پایدار می‌ماند اجرا می‌کند (پیکربندی → Docker Backend را ببینید)

[پیکربندی → Docker Backend](/docs/user-guide/configuration#docker-backend)

این صفحه گزینه 1 را پوشش می‌دهد. Container تمام داده‌های کاربر (پیکربندی، کلیدهای API، نشست‌ها، مهارت‌ها، حافظه‌ها) را در یک پوشه واحد از میزبان در `/opt/data` نصب شده ذخیره می‌کند. خود image بی‌状态 است و با کشیدن نسخه جدید قابل ارتقا است بدون از دست دادن هیچ پیکربندی.

`/opt/data`

## شروع سریع

اگر اولین باری است که Hermes Agent اجرا می‌کنید، یک پوشه داده در میزبان ایجاد کنید و container را به صورت تعاملی شروع کنید تا wizard راه‌اندازی را اجرا کنید:

برخی ارائه‌دهندگان VPS (Hetzner Cloud و چندین مورد دیگر) یک کنسول مبتنی بر مرورگر برای مدیریت میزبان‌ها ارائه می‌دهند. این کنسول‌ها کاراکترهای خاص را به درستی ارسال نمی‌کنند — `:` ممکن است به صورت `;` برسد، `@` ممکن است اشتباه رندر شود، و چیدمان‌های صفحه‌کلید غیرانگلیسی بدتر عمل می‌کنند — که آرگومان‌های `docker run` مانند `-v ~/.hermes:/opt/data`، `-e KEY=value` و کلیدهای API/نشانه‌های چسبانده شده را به طور خاموش تخریب می‌کند.

از SSH استفاده کنید (`ssh root@<host>`) برای ورود امن کپی-چسباندن. اگر مجبورید از کنسول مرورگر استفاده کنید، دستورات را به جای چسباندن دستی تایپ کنید و هر `:`، `@`، `=` و `/` در نتیجه را قبل از فشردن Enter دوباره بررسی کنید.

`ssh root@<host>`

```
mkdir -p ~/.hermes
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent setup
```

شما را در wizard راه‌اندازی قرار می‌دهد، که کلیدهای API شما را درخواست می‌دهد و آن‌ها را در `~/.hermes/.env` می‌نویسد. فقط یک بار نیاز دارید این کار را انجام دهید. به شدت توصیه می‌شود در این مرحله یک سیستم چت برای کار gateway تنظیم کنید.

در داخل container، `hermes setup --portal` را یک بار اجرا کنید — نشانه refresh در volume نصب شده `~/.hermes` باقی می‌ماند. Nous Portal را ببینید.

`hermes setup --portal`
`~/.hermes`
[Nous Portal](/docs/integrations/nous-portal)

## اجرا در حالت gateway

پس از پیکربندی، container را به عنوان یک gateway پایدار (Telegram، Discord، Slack، WhatsApp و غیره) در پس‌زمینه اجرا کنید:

```
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  nousresearch/hermes-agent gateway run
```

پورت 8642 API server سازگار با OpenAI و endpoint سلامت را در معرض دید قرار می‌دهد. اگر فقط از پلتفرم‌های چت (Telegram، Discord و غیره) استفاده می‌کنید اختیاری است، اما اگر می‌خواهید داشبورد یا ابزارهای خارجی به gateway دسترسی داشته باشند ضروری است.

[API server سازگار با OpenAI](/docs/user-guide/features/api-server)

در داخل image رسمی Docker، `gateway run` توسط s6-overlay به طور خودکار نظارت می‌شود: اگر فرآیند gateway خراب شود در عرض چند ثانیه بدون از دست دادن container بازیابی می‌شود و داشبورد (وقتی `HERMES_DASHBOARD=1` تنظیم شده) در کنار آن نظارت می‌شود. فرآیند CMD خود `gateway run` یک `sleep infinity` heartbeat است که container را زنده نگه می‌دارد در حالی که s6 فرآیند gateway واقعی را مدیریت می‌کند — بنابراین `docker stop` همچنان همه چیز را تمیز متوقف می‌کند، اما `docker logs` خروجی gateway نظارت شده را نشان می‌دهد.

یک breadcrumb یک‌خطی در `docker logs` مشاهده خواهید کرد که ارتقا را تأیید می‌کند. برای انصراف — و به دست آوردن معنای تاریخی "gateway فرآیند اصلی container است، خروج container = خروج gateway" — `--no-supervise` را ارسال کنید یا `HERMES_GATEWAY_NO_SUPERVISE=1` را تنظیم کنید. انصراف برای تست‌های smoke CI مفید است که می‌خواهند container با کد وضعیت gateway خارج شود؛ برای استقرارهای تولیدی پیش‌فرض نظارت شده به طور قاطع بهتر است.

این رفتار فقط برای image مبتنی بر s6 اعمال می‌شود. تصاویر قدیمی‌تر (مبتنی بر tini) هنوز `gateway run` را به عنوان فرآیند اصلی foreground اجرا می‌کنند.

بخش "لاگ‌ها کجا می‌روند" در زیر را برای نقشه مسیریابی کامل (gateway‌ها به ازای هر پروفایل، داشبورد، آشتی‌دهنده boot، `docker logs` سراسر container) ببینید.

تنظیم `tool_loop_guardrails.hard_stop_enabled` به طور پیش‌فرض `false` است، که برای نشست‌های CLI و TUI تعاملی منطقی است جایی که انسان می‌تواند هشدارهای فراخوانی مکرر ابزار را ببیند. در استقرارهای gateway یا سرور بدون نظارت، فقط هشدارها ممکن است عاملی را که در حلقه فراخوانی مکرر ابزار گیر کرده متوقف نکنند. اپراتورهایی که رفتار قطع مدار می‌خواهند باید به طور صریح توقف‌های سخت را در `config.yaml` پروفایل فعال کنید:

```
tool_loop_guardrails:
  hard_stop_enabled: true
  hard_stop_after:
    exact_failure: 5
    idempotent_no_progress: 5
```

توجه: API server با `API_SERVER_ENABLED=true` مسدود شده. برای قرار دادن آن فراتر از `127.0.0.1` در داخل container، همچنین `API_SERVER_HOST=0.0.0.0` و یک `API_SERVER_KEY` (حداقل 8 کاراکتر — یکی با `openssl rand -hex 32` تولید کنید) تنظیم کنید. مثال:

```
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  -e API_SERVER_ENABLED=true \
  -e API_SERVER_HOST=0.0.0.0 \
  -e API_SERVER_KEY="$(openssl rand -hex 32)" \
  -e API_SERVER_CORS_ORIGINS='*' \
  nousresearch/hermes-agent gateway run
```

باز کردن هر پورتی روی یک ماشین متصل به اینترنت یک ریسک امنیتی است. نباید این کار را انجام دهید مگر اینکه ریسک‌ها را درک کنید.

## اجرای داشبورد

داشبورد وب داخلی به عنوان یک سرویس s6-rc نظارت شده در کنار gateway در همان container اجرا می‌شود. `HERMES_DASHBOARD=1` را تنظیم کنید تا آن را بالا بیاورید:

```
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  -p 9119:9119 \
  -e HERMES_DASHBOARD=1 \
  nousresearch/hermes-agent gateway run
```

داشبورد توسط s6 نظارت می‌شود — اگر خراب شود، `s6-supervise` آن را پس از یک backoff کوتاه به طور خودکار بازیابی می‌کند. stdout/stderr داشبورد به `docker logs <container>` (بدون پیشوند؛ خروجی خود gateway اکنون در یک فایل s6-log به ازای هر پروفایل زندگی می‌کند — بخش "لاگ‌ها کجا می‌روند" در زیر را ببینید — بنابراین دو جریان تداخل ندارند) ارسال می‌شود.

| متغیر محیطی | توضیح | پیش‌فرض |
| --- | --- | --- |
| HERMES_DASHBOARD | روی `1` (یا `true`/`yes`) تنظیم کنید تا سرویس داشبورد نظارت شده فعال شود | (تنظیم نشده — سرویس ثبت شده اما پایین باقی می‌ماند) |
| HERMES_DASHBOARD_HOST | آدرس اتصال سرور HTTP داشبورد | 0.0.0.0 |
| HERMES_DASHBOARD_PORT | پورت سرور HTTP داشبورد | 9119 |
| HERMES_DASHBOARD_INSECURE | منسوخ / بدون عمل. قبلاً دروازه احراز هویت را دور می‌زد؛ از زمان تقویت ژوئن 2026 دیگر احراز هویت را غیرفعال نمی‌کند. اتصال غیر-loopback همیشه به یک ارائه‌دهنده احراز هویت نیاز دارد | (نادیده گرفته شده — به جای آن یک ارائه‌دهنده پیکربندی کنید) |

داشبورد در داخل container به طور پیش‌فرض `0.0.0.0` را متصل می‌کند — بدون آن، پورت منتشر شده `-p 9119:9119` از میزبان قابل دسترس نخواهد بود. برای محدود کردن اتصال به loopback container (برای تنظیمات sidecar / reverse-proxy)، `HERMES_DASHBOARD_HOST=127.0.0.1` را تنظیم کنید.

دروازه احراز هویت داشبورد وقتی هر دو مورد زیر درست باشد به طور خودکار فعال می‌شود:

1. هاست اتصال غیر-loopback است (مثلاً پیش‌فرض `0.0.0.0` در داخل container)، و
2. یک پلاگین `DashboardAuthProvider` ثبت شده است.

سه روش bundled برای برآورده کردن شرط دوم وجود دارد:

- نام کاربری/رمز عبور — ساده‌ترین برای container میزبانی شده / روی سرور / homelab در یک شبکه مورد اعتماد یا پشت VPN: `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` + `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` (و `HERMES_DASHBOARD_BASIC_AUTH_SECRET` برای نشست‌های پایدار پس از راه‌اندازی مجدد) را تنظیم کنید. مناسب برای در معرض دید مستقیم اینترنت عمومی نیست.
- OAuth (Nous Portal) — برای استقرارهای میزبانی شده/عمومی: ارائه‌دهنده `dashboard_auth/nous` هر وقت `HERMES_DASHBOARD_OAUTH_CLIENT_ID` تنظیم شده باشد فعال می‌شود.
- OIDC میزبانی شده خودی — برای احراز هویت در برابر ارائه‌دهنده هویت خودتان از طریق OpenID Connect استاندارد: ارائه‌دهنده `dashboard_auth/self_hosted` وقتی `HERMES_DASHBOARD_OIDC_ISSUER` + `HERMES_DASHBOARD_OIDC_CLIENT_ID` تنظیم شده باشند فعال می‌شود.

صرف نظر از اینکه کدام را انتخاب کنید، دروازه تماس‌گیرندگان را قبل از اینکه به هر مسیر محافظت شده‌ای دسترسی پیدا کنند به یک صفحه ورود هدایت می‌کند. هر سه ارائه‌دهنده را در رابط وب داشبورد → احراز هویت ببینید.

[رابط وب داشبورد → احراز هویت](/docs/user-guide/features/web-dashboard#authentication-gated-mode)

اگر ارائه‌دهنده‌ای ثبت نشده باشد و اتصال غیر-loopback باشد، داشبورد در شروع با یک خطای خاص که به متغیر محیطی گمشده اشاره می‌کند **شکست خورده بسته** می‌شود. دیگر راه فراری وجود ندارد که داشبورد را بدون احراز هویت روی یک اتصال عمومی سرویس دهد: `HERMES_DASHBOARD_INSECURE=1` اکنون یک no-op منسوخ است (یک هشدار لاگ می‌کند و نادیده گرفته می‌شود). یک ارائه‌دهنده پیکربندی کنید، یا `HERMES_DASHBOARD_HOST=127.0.0.1` را متصل کنید و از طریق SSH tunnel / Tailscale به داشبورد دسترسی پیدا کنید.

`HERMES_DASHBOARD_INSECURE=1`
`HERMES_DASHBOARD_HOST=127.0.0.1`
`--insecure`

یک داشبورد عمومی بدون احراز هویت نقطه ورود کمپین ماندگاری پیکربندی MCP ژوئن 2026 بود: اسکنرهای اینترنت به داشبوردهای (و API serverهای OpenAI) در معرض دید رسیدند و عامل را به کاشتن یک backdoor کلید SSH سوق دادند. دروازه احراز هویت اکنون روی هر اتصال غیر-loopback اجباری است. برای جعبه LAN مورد اعتماد / homelab، ارائه‌دهنده bundled نام کاربری/رمز عبور (`HERMES_DASHBOARD_BASIC_AUTH_USERNAME` + `_PASSWORD`) راه zero-infra برای برآورده کردن آن است.

اجرای داشبورد به عنوان یک container جداگانه **پشتیبانی می‌شود** وقتی آن container فضای نام PID و شبکه میزبان را به اشتراک بگذارد (مثلاً `network_mode: host`، همانطور که فایل `docker-compose.yml` خود مخزن انجام می‌دهد — سرویس `dashboard` آن را ببینید). تشخیص سلامت gateway آن نیاز به فضای نام PID مشترک با فرآیند gateway دارد، بنابراین محدودیت فقط برای داشبوردهای اجرا شده در container‌های شبکه bridge جداگانه بدون فضای نام PID مشترک اعمال می‌شود.

## اجرا به صورت تعاملی (چت CLI)

برای باز کردن یک نشست چت تعاملی در برابر یک پوشه داده در حال اجرا:

```
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent
```

یا اگر قبلاً یک ترمینال در container در حال اجرای خود باز کرده‌اید (مثلاً از طریق Docker Desktop)، کافی است اجرا کنید:

```
/opt/hermes/.venv/bin/hermes
```

## volume‌های پایدار

volume `/opt/data` تنها منبع حقیقت برای تمام وضعیت Hermes است. به پوشه `~/.hermes/` میزبان شما نگاشت می‌شود و شامل:

| مسیر | محتوا |
| --- | --- |
| .env | کلیدهای API و رمزها |
| config.yaml | تمام پیکربندی Hermes |
| SOUL.md | شخصیت/هویت عامل |
| sessions/ | تاریخچه مکالمه |
| memories/ | فروشگاه حافظه پایدار |
| skills/ | مهارت‌های نصب شده |
| home/ | HOME به ازای هر پروفایل برای subprocess‌های ابزار Hermes (git، ssh، gh، npm و CLI‌های مهارت) |
| cron/ | تعریف‌های کار زمان‌بندی شده |
| hooks/ | هوک‌های رویداد |
| logs/ | لاگ‌های runtime |
| skins/ | اسکین‌های سفارشی CLI |

### درخت نصب تغییرناپذیر

در image‌های Docker میزبانی شده و منتشر شده، `/opt/hermes` درخت اپلیکیشن نصب شده است. مالک root است و برای کاربر runtime `hermes` فقط خواندنی است، بنابراین نوبت‌های عامل، نشست‌های gateway، اعمال داشبورد و دستورات عادی `docker exec hermes hermes ...` نمی‌توانند سورس اصلی، `.venv` bundled، `node_modules` یا بسته TUI را در جا ویرایش کنند.

تمام وضعیت متغیر Hermes زیر `/opt/data` تعلق دارد: پیکربندی، `.env`، پروفایل‌ها، مهارت‌ها، حافظه‌ها، نشست‌ها، لاگ‌ها، آپلودهای داشبورد، پلاگین‌ها و سایر فایل‌های مدیریت شده توسط کاربر. Image همچنین نوشتن runtime `.pyc` و نصب lazy وابستگی‌های Hermes در `/opt/hermes` را غیرفعال می‌کند؛ وابستگی‌های پلتفرم اختیاری که توسط image منتشر شده نیاز دارند باید در image پخته شوند یا از طریق یک ساخت image جدید نصب شوند.

در image‌های میزبانی شده/منتشر شده، بهبود خود عامل به مهارت‌ها، حافظه، پلاگین‌ها و پیکربندی زیر `/opt/data` محدود می‌شود. سورس اصلی نصب شده زیر `/opt/hermes` تغییرناپذیر است؛ تغییرات اصلی از طریق PR به مخزن ایجاد شده و با به‌روزرسانی image ارسال می‌شوند، نه با ویرایش زنده نصب در حال اجرا.

اگر اپراتور نیاز به تعمیر یا بازرسی فایل‌های خارج از `/opt/data` دارد، عمداً از یک shell root استفاده کنید. shim `hermes` معمولاً `docker exec hermes hermes ...` را به کاربر runtime برمی‌گرداند؛ `HERMES_DOCKER_EXEC_AS_ROOT=1` را برای یک فراخوانی root تکی وقتی به طور صریح به معنای root نیاز دارید تنظیم کنید.

CLI‌های مهارت که credentialها را زیر `~` ذخیره می‌کنند باید در برابر HOME subprocess مقداردهی اولیه شوند، نه فقط ریشه volume داده. به عنوان مثال، مهارت `xurl` وضعیت OAuth را در `~/.xurl` ذخهره می‌کند؛ در لایه‌بندی Docker رسمی، فراخوانی‌های ابزار Hermes آن را به عنوان `/opt/data/home/.xurl` می‌خوانند، بنابراین احراز هویت دستی xurl را با `HOME=/opt/data/home` اجرا کنید و با `HOME=/opt/data/home xurl auth status` تأیید کنید.

هرگز دو container `gateway` Hermes را به طور همزمان علیه همان پوشه داده اجرا نکنید — فایل‌های نشست و فروشگاه‌های حافظه برای دسترسی نوشتن همزمان طراحی نشده‌اند.

## پشتیبانی چند پروفایلی

Hermes از **چندین پروفایل** پشتیبانی می‌کند — پوشه‌های جداگانه `~/.hermes/` که به شما اجازه می‌دهند عاملان مستقل (SOUL، مهارت‌ها، حافظه، نشست‌ها، credentialهای متفاوت) از یک نصب واحد اجرا کنید. در داخل image رسمی Docker، درخت نظارت s6 هر پروفایل را به عنوان یک سرویس نظارت شده درجه یک رفتار می‌کند، بنابراین استقرار توصیه شده **یک container میزبان تمام پروفایل‌ها** است.

[چندین پروفایل](/docs/reference/profile-commands)

هر پروفایل که با `hermes profile create <name>` ایجاد می‌شود دریافت می‌کند:

- یک شکاف سرویس s6 اختصاصی در `/run/service/gateway-<name>/`، به طور پویا توسط runtime ثبت شده — بدون نیاز به بازساخت container.
- بازیابی خودکار هنگام خرابی، با backoff مدیریت شده توسط `s6-supervise`.
- لاگ‌های چرخشی به ازای هر پروفایل در `${HERMES_HOME}/logs/gateways/<name>/current` (10 آرشیو × 1 MB هر کدام).
- ماندگاری وضعیت در راه‌اندازی مجدد container: آشتی‌دهنده boot فایل `gateway_state.json` را از هر پوشه پروفایل می‌خواند و فقط برای پروفایل‌هایی که آخرین وضعیت ثبت شده `running` بود شکاف را دوباره بالا می‌آورد. فقط یک gateway که به طور صریح متوقف کرده‌اید (`hermes gateway stop`) در راه‌اندازی مجدد پایین باقی می‌ماند — راه‌اندازی مجدد container، ارتقای image یا خروج غیرمنتظره وضعیت ثبت شده را `running` باقی می‌گذارد، بنابراین gateway در راه‌اندازی بعدی به طور خودکار شروع می‌شود.

دستورات چرخه حیاتی که در میزبان اجرا می‌کنید از داخل container به همان شکل کار می‌کنند:

```
# ایجاد یک پروفایل — شکاف s6 gateway-<name> را ثبت می‌کند.
docker exec hermes hermes profile create coder
# شروع / توقف / بازیابی — s6-svc را ارسال می‌کند؛ چرخه حیات gateway در docker restart پایدار است.
docker exec hermes hermes -p coder gateway start
docker exec hermes hermes -p coder gateway stop
docker exec hermes hermes -p coder gateway restart
# وضعیت — `Manager: s6 (container supervisor)` را در داخل container گزارش می‌دهد.
docker exec hermes hermes -p coder gateway status
# حذف یک پروفایل — شکاف s6 را نیز فرو می‌ریزد.
docker exec hermes hermes profile delete coder
```

در زیر، `hermes gateway start/stop/restart` در داخل container رهگیری شده و به `s6-svc` علیه دایرکتوری سرویس صحیح مسیریابی می‌شود؛ نیازی به یادگیری مستقیم دستورات s6 ندارید. برای وضعیت خام ناظر، از `/command/s6-svstat /run/service/gateway-<name>` استفاده کنید (توجه `/command/` فقط در PATH برای فرآیندهای ایجاد شده توسط درخت نظارت است — هنگام فراخوانی از `docker exec`، مسیر مطلق را ارسال کنید).

### دسترسی به بیش از یک پروفایل از خارج container

دو سطح متفاوت از خارج به gateway یک پروفایل دسترسی دارند و رفتار متفاوتی دارند — آن‌ها را اشتباه نگیرید:

**Hermes Desktop (و رابط وب داشبورد).** اتصال "Remote Gateway" اپلیکیشن Desktop با backend `hermes dashboard` (پورت پیش‌فرض 9119، فعال شده با `HERMES_DASHBOARD=1`) ارتباط برقرار می‌کند — **نه** API server سازگار با OpenAI. یک backend داشبورد **هر** پروفایل co-located را سرویس می‌دهد: تعویض‌کننده پروفایل اپلیکیشن پروفایل هدف را با هر درخواست ارسال می‌کند و backend `HERMES_HOME` آن پروفایل را روی دیسک باز می‌کند. بنابراین **نیازی به پورت دوم** — یا اتصال دوم — به ازای هر پروفایل برای Desktop ندارید؛ یک اتصال `:9119` همه را از طریق تعویض‌کننده پوشش می‌دهد.

**کلاینت‌های API سازگار با OpenAI (Open WebUI، LobeChat، `/v1/...`).** این‌ها با API server هر پروفایل ارتباط برقرار می‌کنند، که **پورت 8642 را برای هر پروفایل متصل می‌کند** (از `API_SERVER_PORT` / `platforms.api_server.extra.port` حل می‌شود — هیچ تخصیص خودکار و کلید `gateway.port` در `config.yaml` وجود ندارد). اگر می‌خواهید یک کلاینت به پروفایل دوم خاصی دسترسی داشته باشد، به آن پروفایل یک `API_SERVER_PORT` متمایز در `.env` خودش بدهید، در غیر این صورت gateway آن سعی می‌کند 8642 را نیز متصل کند و با پروفایل پیش‌فرض تداخل می‌کند:

```
# ایجاد پروفایل (شکاف s6 gateway-<name> آن را ثبت می‌کند)
docker exec hermes hermes profile create work
# اتصال API server آن به یک پورت آزاد (در .env خود پروفایل بنویسید)
cat >> /opt/data/profiles/work/.env <<'EOF'
API_SERVER_ENABLED=true
API_SERVER_PORT=8643
EOF
docker exec hermes hermes -p work gateway restart
```

`API_SERVER_PORT` را در `.env` خود هر پروفایل نگه دارید، **هرگز** در بلوک `environment:` سراسر container — یک مقدار سراسری هر پروفایل را مجبور به استفاده از همان پورت می‌کند و با هم تداخل می‌کنند. با شبکه‌بندی bridge، پورت اضافی را در `docker-compose.yml` (`- "8643:8643"`) منتشر کنید؛ با `network_mode: host` از قبل در میزبان قابل دسترس است. اتصال 8642 پروفایل پیش‌فرض دست نخورده باقی می‌ماند.

### چرا یک container با پروفایل‌های متعدد، نه container‌های متعدد

قبل از مهاجرت s6، "یک container به ازای هر پروفایل" الگوی توصیه شده بود زیرا ناظری در داخل container برای مدیریت چندین gateway وجود نداشت. با s6 به عنوان PID 1، دیگر لازم نیست و لایه‌بندی container واحد در تقریباً هر بعد ساده‌تر است:

|  | یک container، پروفایل‌های متعدد | یک container به ازای هر پروفایل |
| --- | --- | --- |
| هزینه دیسک | یک image، یک venv bundled، یک کش Playwright | N image / N کش |
| هزینه حافظه | کش مفسر پایتون مشترک، `node_modules` مشترک | تکرار شده به ازای هر container |
| ایجاد پروفایل | `docker exec ... hermes profile create <name>` (ثانیه‌ها) | فراخوانی جدید `docker run` + تخصیص پورت + bind-mount پیکربندی |
| بازیابی خرابی به ازای هر پروفایل | بازیابی خودکار `s6-supervise` | `--restart unless-stopped` Docker (کندتر، کار خواهر و برادر را می‌کشد) |
| لاگ‌ها | فایل چرخشی به ازای هر پروفایل از طریق `s6-log`، به اضافه لاگ حسابرسی boot container | `docker logs <name>` به ازای هر container — بدون چرخش داخلی |
| پشتیبانی | یک پوشه `~/.hermes` | N پوشه برای هماهنگی |

پروفایل پیش‌فرض (`default`) همیشه در اولین راه‌اندازی ثبت می‌شود، بنابراین یک container تازه با یک gateway نظارت شده از جعبه خارج می‌شود. پروفایل‌های اضافی اضافه‌های خالص runtime هستند.

### زمانی که واقعاً یک container جداگانه می‌خواهید

پروفایل در container پیش‌فرض است. فقط وقتی دلیل خاصی دارید یک container جداگانه به ازای هر پروفایل اجرا کنید:

- جداسازی منابع به ازای هر بار کاری — مثلاً یک نشست ابزار مرورگر فرار در پروفایل A نباید بتواند پروفایل B را OOM کند. Container‌ها `--memory`/`--cpus` به ازای هر پروفایل به شما می‌دهند.
- تثبیت image مستقل — تگ‌های image upstream مختلف به ازای هر بار کاری.
- تقسیم شبکه — شبکه‌های Docker متمایز به ازای هر پروفایل (مثلاً یکی رو به مشتری، یکی داخلی).
- انطباق / شعاع انفجار — credentialهای متمایز هرگز درخت فرآیند سطح OS را به اشتراک نمی‌گذارند.

در آن موارد، یک سرویس به ازای هر پروفایل با `container_name`، `volumes` و `ports` متمایز اعلام کنید:

```
services:
  hermes-work:
    image: nousresearch/hermes-agent:latest
    container_name: hermes-work
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"
    volumes:
      - ~/.hermes-work:/opt/data
  hermes-personal:
    image: nousresearch/hermes-agent:latest
    container_name: hermes-personal
    restart: unless-stopped
    command: gateway run
    ports:
      - "8643:8642"
    volumes:
      - ~/.hermes-personal:/opt/data
```

هشدار از volume‌های پایدار همچنان اعمال می‌شود: هرگز دو container را به طور همزمان به همان پوشه `~/.hermes` اشاره ندهید. ناظر s6 داخل هر container مجموعه پروفایل خود را مدیریت می‌کند؛ به اشتراک گذاشتن volume داده بین container‌ها فایل‌های نشست و فروشگاه‌های حافظه را تخریب می‌کند.

## لاگ‌ها کجا می‌روند

container s6 چهار سطح لاگ متمایز دارد و "چرا gateway من در `docker logs` چیزی نشان نمی‌دهد" یک شگفتی رایج است. راهنمای سریع:

| منبع | کجا فرود می‌آید | چگونه بخوانیم |
| --- | --- | --- |
| Gateway به ازای هر پروفایل (`hermes gateway run` و gateway‌ها به ازای هر پروفایل تحت s6) | در دو مکان Tee'd: `docker logs <container>` (زمان واقعی، بدون پیشوند اضافی) و `${HERMES_HOME}/logs/gateways/<profile>/current` (چرخشی، با مهر زمانی ISO-8601، 10 آرشیو × 1 MB هر کدام) | `docker logs -f hermes` یا `tail -F ~/.hermes/logs/gateways/default/current` در میزبان |
| داشبورد (وقتی `HERMES_DASHBOARD=1`) | `docker logs <container>` (بدون پیشوند) | `docker logs -f hermes` — در هم تنیده با خطوط gateway |
| آشتی‌دهنده boot (ثبت می‌کند کدام gateway‌های پروفایل در هر شروع container بازیابی شدند) | `${HERMES_HOME}/logs/container-boot.log` (لاگ حسابرسی فقط-اضافه) | `tail -F ~/.hermes/logs/container-boot.log` |
| لاگ‌های عمومی Hermes (`agent.log`، `errors.log`) | `${HERMES_HOME}/logs/` (آگاه به پروفایل) | `docker exec hermes hermes logs --follow [--level WARNING] [--session <id>]` |

دو نتیجه عملی ارزش دانستن:

- کپی فایل در `logs/gateways/<profile>/current` چیزی است که راه‌اندازی مجدد container را تحمل می‌کند. `docker logs` فقط خروجی عمر container فعلی را حفظ می‌کند (و با `docker rm` پاک می‌شود)؛ فایل‌های چرخشی روی volume bind-mount شده باقی می‌مانند.
- شکل خط حسابرسی آشتی‌دهنده boot `<iso-timestamp> profile=<name> prior_state=<state> action=<registered|started>` است، بنابراین یک `grep profile=coder ~/.hermes/logs/container-boot.log` سریع نشان می‌دهد یک پروفایل خاص آخرین بار کی بازیابی شد و آیا s6 آن را به طور خودکار شروع کرد.

## ارسال متغیرهای محیطی

کلیدهای API از `/opt/data/.env` در داخل container خوانده می‌شوند. همچنین می‌توانید متغیرهای محیطی را مستقیماً ارسال کنید:

```
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  -e ANTHROPIC_API_KEY="sk-ant-..." \
  -e OPENAI_API_KEY="sk-..." \
  nousresearch/hermes-agent
```

پرچم‌های `-e` مستقیم مقادیر `.env` را override می‌کنند. این برای یکپارچه‌سازی‌های CI/CD یا secrets-manager مفید است جایی که نمی‌خواهید کلیدها روی دیسک باشند.

این صفحه اجرای خود Hermes در داخل Docker را پوشش می‌دهد. اگر می‌خواهید Hermes فراخوانی‌های `terminal`/`execute_code` عامل را در داخل یک Docker sandbox container (یک container بلندمدت مشترک بین فرآیندهای Hermes — issue #20561 را ببینید) اجرا کند، آن یک بلوک پیکربندی جداگانه است — `terminal.backend: docker` به اضافه `terminal.docker_image`، `terminal.docker_volumes`، `terminal.docker_forward_env`، `terminal.docker_env`، `terminal.docker_run_as_host_user`، `terminal.docker_extra_args`، `terminal.docker_persist_across_processes` و `terminal.docker_orphan_reaper`. مجموعه کامل شامل قوانین چرخه حیات container را در پیکربندی → Docker Backend ببینید.

## مثال Docker Compose

برای استقرار پایدار با هر دو gateway و داشبورد، `docker-compose.yaml` راحت است:

```
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"   # gateway API
      - "9119:9119"   # داشبورد (فقط وقتی HERMES_DASHBOARD=1 قابل دسترس است)
    volumes:
      - ~/.hermes:/opt/data
    environment:
      - HERMES_DASHBOARD=1
      # برای ارسال متغیرهای محیطی خاص به جای استفاده از فایل .env غیرفعال کنید:
      # - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      # - OPENAI_API_KEY=${OPENAI_API_KEY}
      # - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

با `docker compose up -d` شروع کنید و لاگ‌ها را با `docker compose logs -f` مشاهده کنید. stdout gateway نظارت شده همچنین به `${HERMES_HOME}/logs/gateways/<profile>/current` در volume tee'd می‌شود — نقشه مسیریابی کامل را در "لاگ‌ها کجا می‌روند" ببینید.

## اختیاری: bridge صوتی دسکتاپ Linux

حالت صدا در Docker به دو چیز مجزا نیاز دارد تا کار کند: Hermes باید اجازه کاوش دستگاه‌های صوتی در داخل container را داشته باشد و container باید بتواند به سرور صوتی میزبان شما دسترسی داشته باشد. راه‌اندازی زیر لوله‌کشی صوتی میزبان را برای دسکتاپ‌های Linux که یک سوکت سازگار با PulseAudio را افشا می‌کنند، شامل بسیاری از تنظیمات PipeWire، پوشش می‌دهد.

این یک راه‌حل دسکتاپ Linux است، نه یک ویژگی عمومی Docker Desktop. مفید است وقتی از قبل صوت میزبان کار می‌کند و حالت صدای CLI را در داخل container Hermes می‌خواهید. اگر Hermes همچنان `Running inside Docker container -- no audio devices` گزارش می‌کند، از یک ساخت که پشتیبانی کاوش صوتی Docker برای `PULSE_SERVER`/`PIPEWIRE_REMOTE` را شامل می‌شود استفاده کنید.

ابتدا یک پیکربندی ALSA در کنار فایل Compose خود ایجاد کنید:

```
pcm.!default {
    type pulse
    hint {
        show on
        description "Default ALSA Output (PulseAudio)"
    }
}
pcm.pulse {
    type pulse
}
ctl.!default {
    type pulse
}
```

سپد یک image کوچک مشتق شده با پلاگین ALSA PulseAudio نصب شده بسازید:

```
FROM nousresearch/hermes-agent:latest
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends libasound2-plugins \
    && rm -rf /var/lib/apt/lists/*
```

از آن image در Compose استفاده کنید و سوکت PulseAudio و cookie کاربر میزبان را عبور دهید:

```
services:
  hermes:
    build:
      context: .
      dockerfile: Dockerfile.audio
    image: hermes-agent-audio
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    volumes:
      - ~/.hermes:/opt/data
      - /run/user/${HERMES_UID}/pulse:/run/user/${HERMES_UID}/pulse
      - ~/.config/pulse/cookie:/tmp/pulse-cookie:ro
      - ./asound.conf:/etc/asound.conf:ro
    environment:
      - HERMES_UID=${HERMES_UID}
      - HERMES_GID=${HERMES_GID}
      - XDG_RUNTIME_DIR=/run/user/${HERMES_UID}
      - PULSE_SERVER=unix:/run/user/${HERMES_UID}/pulse/native
      - PULSE_COOKIE=/tmp/pulse-cookie
```

آن را با UID/GID میزبان خود شروع کنید تا فرآیند container بتواند به سوکت صوتی به ازای هر کاربر دسترسی داشته باشد:

```
export HERMES_UID="$(id -u)"
export HERMES_GID="$(id -g)"
docker compose up -d --build
```

برای تأیید آنچه PortAudio در داخل container می‌بیند:

```
docker exec hermes /opt/hermes/.venv/bin/python -c "import sounddevice as sd; print(sd.query_devices())"
```

## محدودیت‌های منابع

container Hermes به منابع متوسط نیاز دارد. حداقل‌های توصیه شده:

| منبع | حداقل | توصیه شده |
| --- | --- | --- |
| حافظه | 1 GB | 2–4 GB |
| CPU | 1 هسته | 2 هسته |
| دیسک (volume داده) | 500 MB | 2+ GB (با نشست‌ها/مهارت‌ها رشد می‌کند) |

اتوماسیون مرورگر (Playwright/Chromium) حریص‌ترین ویژگی حافظه است. اگر به ابزارهای مرورگر نیاز ندارید، 1 GB کافی است. با ابزارهای مرورگر فعال، حداقل 2 GB اختصاص دهید.

محدودیت‌ها را در Docker تنظیم کنید:

```
docker run -d \
  --name hermes \
  --restart unless-stopped \
  --memory=4g --cpus=2 \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

## کاری که Dockerfile انجام می‌دهد

image رسمی بر `debian:13.4` استوار است و شامل:

- Python 3.13 با وابستگی‌های هماهنگ شده از فایل قفل از طریق `uv sync --frozen --no-install-project` برای extras پخته شده (all، messaging، Anthropic/Bedrock/Azure identity، Hindsight، Matrix)، به دنبال یک نصب editable بدون وابستگی از خود Hermes.
- Node.js 22 + npm (برای اتوماسیون مرورگر، bridge WhatsApp، بسته‌های TUI/Desktop و ابزارهای ساخت workspace)
- Playwright با Chromium (`npx playwright install --with-deps chromium --only-shell`)
- ripgrep، ffmpeg، git و `xz-utils` به عنوان ابزارهای سیستمی
- `docker-cli` — تا عاملان در حال اجرا در container بتوانند daemon Docker میزبان را هدایت کنند (bind-mount `/var/run/docker.sock` برای فعال‌سازی) برای `docker build`، `docker run`، بازرسی container و غیره.
- `openssh-client` — امکان backend ترمینال SSH از داخل container را فراهم می‌کند. Backend SSH از باینری `ssh` سیستمی shell out می‌کند؛ بدون این، به طور خاموش در نصب‌های containerized شکست می‌خورد.
- Bridge WhatsApp (`scripts/whatsapp-bridge/`)
- `s6-overlay` v3 به عنوان PID 1 (jda تر `tini` قدیمی‌تر را جایگزین می‌کند) — داشبورد و gateway‌ها به ازای هر پروفایل را با بازیابی خودکار هنگام خرابی نظارت می‌کند، فرآیندهای فرعی zombie را جمع می‌کند و سیگنال‌ها را ارسال می‌کند.

image `/opt/hermes` را به عنوان یک درخت نصب تغییرناپذیر در runtime رفتار می‌کند. extras پایتونی اختیاری، workspace‌های Node و دارایی‌های TUI که باید در Docker در دسترس باشند باید در حین ساخت image پخته شوند؛ نصب‌های lazy runtime غیرفعال شده‌اند تا gateway‌های نظارت شده و دستورات `docker exec hermes …` سعی نکنند artifacts وابسته را به درخت سورس فقط-خواندنی برگردانند.

ENTRYPOINT container `/init` s6-overlay است. در راه‌اندازی:

1. `/etc/cont-init.d/01-hermes-setup` (= `docker/stage2-hook.sh`) را به عنوان root اجرا می‌کند: بازنویسی UID/GID اختیاری، تعمیر مالکیت volume، بذر `env`/`config.yaml`/`SOUL.md` در اولین راه‌اندازی، اجرای مهاجرت‌های config-schema غیرتعاملی مگر اینکه `HERMES_SKIP_CONFIG_MIGRATION=1` باشد، هماهنگ‌سازی مهارت‌های bundled.
2. `/etc/cont-init.d/02-reconcile-profiles` (= `hermes_cli.container_boot`) را اجرا می‌کند: `$HERMES_HOME/profiles/<name>/` را پیمایش می‌کند، شکاف سرویس s6 gateway به ازای هر پروفایل را در `/run/service/gateway-<profile>/` دوباره ایجاد می‌کند و فقط آن‌هایی را که آخرین وضعیت ثبت شده `running` بود خودکار شروع می‌کند (نظارت gateway به ازای هر پروفایل را ببینید).
3. سرویس‌های s6-rc ایستای `main-hermes` و `dashboard` را شروع می‌کند.
4. CMD container را به عنوان برنامه اصلی (`/opt/hermes/docker/main-wrapper.sh`) اجرا می‌کند، که آرگومان‌هایی که کاربر به `docker run` ارسال کرده را مسیریابی می‌کند: بدون آرگومان → `hermes` (پیش‌فرض) / اولین آرگومان یک اجرایی در PATH است (مثلاً `sleep`، `bash`) → مستقیماً اجرا کنید / هر چیز دیگری → `hermes <args>` (رد شدن زیردستور)
Container هنگامی که این برنامه اصلی خارج می‌شود، خارج می‌شود، با کد خروج آن.

ورودی container اکنون `/init` (s6-overlay) است، نه `/usr/bin/tini`. هر پنج الگوی فراخوانی `docker run` مستند شده (بدون آرگومان، `chat -q "…"`) رفتاری دقیقاً مانند image مبتنی بر tini دارند. اگر wrapper پایین‌تری دارید که به رفتار سیگنال خاص tini یا فراخوانی سخت‌کد شده `/usr/bin/tini --` وابسته بود، به تگ image قبلی ثابت کنید.

ورودی image را override نکنید مگر اینکه `/init` (یا معادل آن، shim قدیمی `docker/entrypoint.sh` که به hook stage2 ارسال می‌کند) را در زنجیره فرمان نگه دارید. `/init` s6-overlay به عنوان root اجرا می‌شود تا بتواند volume را در اولین راه‌اندازی chown کند، سپد از طریق `s6-setuidgid` برای هر سرویس نظارت شده **و** برای برنامه اصلی به کاربر `hermes` رها می‌کند. اجرای `hermes gateway run` به عنوان root در image رسمی به طور پیش‌فرض رد می‌شود زیرا می‌تواند فایل‌های مالک root در `/opt/data` ایجاد کند و راه‌اندازی‌های بعدی داشبورد یا gateway را خراب کند. فقط وقتی عمداً آن ریسک را می‌پذیرید `HERMES_ALLOW_ROOT_GATEWAY=1` را تنظیم کنید.

### `docker exec` به طور خودکار به کاربر `hermes` رها می‌کند

`docker exec hermes <cmd>` به طور پیش‌فرض به عنوان root در داخل container اجرا می‌شود، اما image یک shim سبک در `/opt/hermes/bin/hermes` (اولین در PATH) دارد که فراخوان‌های root را تشخیص می‌دهد و به طور شفاف از طریق `s6-setuidgid hermes` دوباره اجرا می‌کند. بنابراین `docker exec hermes login`، `docker exec hermes profile create …`، `docker exec hermes setup` و غیره همگی فایل‌هایی مالک UID 10000 می‌نویسند — یعنی توسط gateway نظارت شده خواندنی — بدون نیاز به پرچم `--user` اضافی. فراخوان‌های غیر-root (خود فرآیندهای نظارت شده، `docker exec --user hermes`، زیرعاملان kanban در داخل container) به یک میان‌بُر برخورد می‌کنند که باینری venv را مستقیماً اجرا می‌کند، بنابراین overhead در مسیرهای داغ وجود ندارد.

اگر به طور خاص به یک `docker exec` نیاز دارید که معنای root را حفظ کند (نشست‌های تشخیصی، بازرسی وضعیت فقط root، فایل‌های خارج از `/opt/data` که صاحب‌شان root است)، در هر فراخوانی خارج شوید:

```
docker exec -e HERMES_DOCKER_EXEC_AS_ROOT=1 hermes <cmd>
```

shim `1`/`true`/`yes` (حساس به حروف نیست) را می‌پذیرد. هر چیز دیگری — شامل اشتباهات تایپی مانند `=0` — به رها کردن عبور می‌کند، بنابراین انصراف‌های خاموش ممکن نیستند. اگر `s6-setuidgid` موجود نباشد (ساختهای سفارشی که s6-overlay را حذف کرده‌اند)، shim اجرای به عنوان root را رد می‌کند و 127 خارج می‌شود، مدل امتیاز شکسته را با صدای بلند سطح می‌کند به جای بازگشت به مشکل تاریخی جایی که `docker exec hermes login` `auth.json` را به عنوان `root:root` می‌نویسند و احراز هویت gateway نظارت شده را در هر پیام پلتفرم پیام‌رسانی خراب می‌کند.

### نظارت gateway به ازای هر پروفایل

هر پروفایل که با `hermes profile create <name>` ایجاد می‌شود به طور خودکار یک سرویس gateway نظارت شده s6 در `/run/service/gateway-<name>/` دریافت می‌کند، با بازیابی خودکار پایدار وضعیت در راه‌اندازی مجدد container. گردش کار کاربرمحور و دستورات چرخه حیات در بخش "پشتیبانی چند پروفایلی" در زیر را ببینید.

مزایای نظارت نسبت به image قبل s6:

- خرابی‌های gateway توسط `s6-supervise` پس از ~1s backoff بازیابی خودکار می‌شوند.
- داشبورد، وقتی با `HERMES_DASHBOARD=1` فعال شده، در همان درخت نظارت نظارت می‌شود و همان رفتار بازیابی خودکار را دریافت می‌کند.
- `docker restart`، ارتقاهای image (`docker compose up -d --force-recreate`) و خروج‌های غیرمنتظره gateway‌های در حال اجرا را حفظ می‌کنند: آشتی‌دهنده cont-init فایل `$HERMES_HOME/profiles/<name>/gateway_state.json` را می‌خواند و اگر آخرین وضعیت ثبت شده `running` بود شکاف را دوباره بالا می‌آورد. فقط یک `hermes gateway stop` صریح `stopped` ثبت می‌کند و gateway را در راه‌اندازی مجدد پایین نگه می‌دارد؛ SIGTERM ارسال شده توسط container/s6 در راه‌اندازی مجدد یا ارتقا به عنوان "هنوز در حال اجرا" رفتار می‌شود و به طور خودکار شروع می‌شود.
- لاگ‌های gateway به ازای هر پروفایل در `${HERMES_HOME}/logs/gateways/<profile>/current` (توسط `s6-log` چرخشی) باقی می‌مانند و اعمال آشتی‌دهنده در هر راه‌اندازی به `${HERMES_HOME}/logs/container-boot.log` اضافه می‌شوند. نقشه مسیریابی کامل را در "لاگ‌ها کجا می‌روند" ببینید.

`hermes status` در داخل container `Manager: s6 (container supervisor)` را گزارش می‌کند. از `/command/s6-svstat /run/service/gateway-<name>` برای نمای خام ناظر استفاده کنید (توجه `/command/` فقط در PATH برای فرآیندهای درخت نظارت است؛ هنگام فراخوانی از `docker exec` مسیر مطلق را ارسال کنید).

## ارتقا

آخرین image را بکشید و container را دوباره ایجاد کنید. پوشه داده شما حفظ می‌شود و container مهاجرت‌های config-schema غیرتعاملی را علیه `$HERMES_HOME/config.yaml` نصب شده قبل از شروع gateway اجرا می‌کند.
هنگامی که مهاجرت لازم است، Hermes ابتدا snapshot‌های با مهر زمانی در کنار `config.yaml` و `.env` می‌نویسد.

```
docker pull nousresearch/hermes-agent:latest
docker rm -f hermes
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

یا با Docker Compose:

```
docker compose pull
docker compose up -d
```

فقط اگر نیاز به بازرسی یا مهاجرت دستی پیکربندی ذخیره شده قبل از بازنویسی image جدید دارید `HERMES_SKIP_CONFIG_MIGRATION=1` را تنظیم کنید.

## مهارت‌ها و فایل‌های credential

وقتی از Docker به عنوان محیط اجرا استفاده می‌کنید (نه روش‌های بالا، بلکه وقتی عامل دستورات را در داخل یک Docker sandbox اجرا می‌کند — پیکربندی → Docker Backend را ببینید)، Hermes یک container بلندمدت واحد را برای تمام فراخوانی‌های ابزار دوباره استفاده می‌کند و پوشه مهارت‌ها (`~/.hermes/skills/`) و هر فایل credentialی که توسط مهارت‌ها اعلام شده را به طور خودکار به عنوان volume فقط-خواندنی به آن container bind-mount می‌کند. اسکریپت‌ها، قالب‌ها و مراجع مهارت در داخل sandbox بدون پیکربندی دستی در دسترس هستند و از آنجا که container در طول زندگی فرآیند Hermes پایدار می‌ماند، هر وابستگی که نصب می‌کنید یا فایلی که می‌نویسید برای فراخوانی ابزار بعدی باقی می‌ماند.

همان هماهنگ‌سازی برای backend‌های SSH و Modal اتفاق می‌افتد — مهارت‌ها و فایل‌های credential قبل از هر دستور از طریق rsync یا API نصب Modal آپلود می‌شوند.

## نصب ابزارهای بیشتر در container

image رسمی با مجموعه مراقبت شده‌ای از ابزارها ارسال می‌شود (کاری که Dockerfile انجام می‌دهد را ببینید)، اما هر ابزاری که عامل ممکن است بخواهد از قبل نصب نشده است. پنج رویکرد توصیه شده وجود دارد، به ترتیب تلاش و دوام رو به افزایش.

### ابزارهای npm یا Python — از `npx` یا `uvx` استفاده کنید

`npx`
`uvx`

برای هر ابزاری که در npm یا PyPI منتشر شده، به Hermes بگویید از طریق `npx` (npm) یا `uvx` (Python) آن را اجرا کند و آن دستور را در حافظه پایدار خود به خاطر بسپارد. اگر ابزار به فایل پیکربندی یا credential نیاز دارد، به آن بگویید آن‌ها را زیر `/opt/data` (مثلاً `/opt/data/<tool>/config.yaml`) قرار دهد.

وابستگی‌ها در صورت نیاز واکشی شده و برای عمر container کش می‌شوند. پیکربندی نوشته شده زیر `/opt/data` راه‌اندازی مجدد container را تحمل می‌کند زیرا در دایرکتوری bind-mount شده میزبان زندگی می‌کند. خود کش بسته پس از `docker rm` بازساخته می‌شود، اما `npx` و `uvx` دوباره واکشی شفاف می‌کنند دفعه بعدی که ابزار اجرا می‌شود.

### سایر ابزارها (بسته‌های apt، باینری‌ها) — نصب و به خاطر سپردن

برای هر چیزی خارج از npm یا PyPI — بسته‌های `apt`، باینری‌های از پیش ساخته شده، runtime‌های زبان که از قبل در image نیستند — به Hermes بگویید چگونه آن را نصب کند (مثلاً `apt-get update && apt-get install -y <package>`) و به آن بگویید دستور نصب را به خاطر بسپارد. ابزار برای بقیه عمر container باقی می‌ماند و Hermes دستور نصب را پس از راه‌اندازی مجدد container هنگامی که بعداً به ابزار نیاز دارد دوباره اجرا می‌کند.

این برای ابزارهایی که سریع نصب می‌شوند و گاهی استفاده می‌شوند مناسب است. برای ابزارهایی که مداوم استفاده می‌شوند، رویکرد بعدی را ترجیح دهید.

### نصب‌های پایدار — ساخت یک image مشتق شده

وقتی یک ابزار باید فوراً در هر شروع container بدون تأخیر نصب مجدد در دسترس باشد، یک image جدید بسازید که از `nousresearch/hermes-agent` ارث‌بری می‌کند و ابزار را در یک لایه نصب می‌کند:

```
FROM nousresearch/hermes-agent:latest
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends <your-package> \
    && rm -rf /var/lib/apt/lists/*
USER hermes
```

آن را بسازید و به جای image رسمی استفاده کنید:

```
docker build -t my-hermes:latest .
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  my-hermes:latest gateway run
```

ورودی و معنای `/opt/data` ارث‌بری شده بدون تغییر باقی می‌مانند، بنابراین بقیه این صفحه همچنان اعمال می‌شود. هنگام کشیدن `nousresearch/hermes-agent` جدیدتر upstream فراموش نکنید image را بازسازی کنید.

### ابزارهای پیچیده یا stack‌های multi-service — اجرای یک container sidecar

برای ابزارهایی که سرویس خودشان را می‌آورند (یک پایگاه داده، یک سرور وب، یک صف، یک مزرعه مرورگر بدون رابط) یا آنقدر سنگین هستند که در داخل container Hermes زندگی کنند، آن‌ها را به عنوان یک container جداگانه در یک شبکه Docker مشترک اجرا کنید. Hermes به sidecar از طریق نام container دسترسی پیدا می‌کند، به همان شکلی که به یک سرور استنتاج محلی دسترسی پیدا می‌کند (اتصال به سرورهای استنتاج محلی را ببینید).

```
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"
    volumes:
      - ~/.hermes:/opt/data
    networks:
      - hermes-net
  my-tool:
    image: example/my-tool:latest
    container_name: my-tool
    restart: unless-stopped
    networks:
      - hermes-net
networks:
  hermes-net:
    driver: bridge
```

از داخل container Hermes، sidecar در `http://my-tool:<port>` (یا هر پروتکلی که سرویس می‌دهد) قابل دسترس است. این الگو چرخه حیات، محدودیت‌های منابع و تقویم ارتقای هر سرویس را مستقل نگه می‌دارد و از حجیم کردن image Hermes با وابستگی‌هایی که فقط توسط یک ابزار نیاز دارند جلوگیری می‌کند.

### ابزارهای مفید به طور گسترده — ایجاد issue یا pull request

اگر یک ابزار احتمالاً برای اکثر کاربران Hermes Agent مفید باشد، مشارکت آن را در upstream به جای نگهداری در یک image مشتق شده خصوصی در نظر بگیرید. یک issue یا pull request در [مخزن hermes-agent](https://github.com/NousResearch/hermes-agent) ایجاد کنید که ابزار و مورد استفاده آن را توصیف کند. ابزارهایی که در image رسمی بسته‌بندی می‌شوند از هر کاربر بهره می‌برند و از هزینه نگهداری یک fork پایین‌تر جلوگیری می‌کنند.

## اتصال به سرورهای استنتاج محلی (vLLM، Ollama و غیره)

هنگام اجرای Hermes در Docker و سرور استنتاج شما (vLLM، Ollama، text-generation-inference و غیره) نیز روی میزبان یا در یک container دیگر اجرا می‌شود، شبکه‌بندی به توجه اضافی نیاز دارد.

### Docker Compose (توصیه شده)

هر دو سرویس را در یک شبکه Docker قرار دهید. این قابل اعتمادترین رویکرد است:

```
services:
  vllm:
    image: vllm/vllm-openai:latest
    container_name: vllm
    command: >
      --model Qwen/Qwen2.5-7B-Instruct
      --served-model-name my-model
      --host 0.0.0.0
      --port 8000
    ports:
      - "8000:8000"
    networks:
      - hermes-net
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"
    volumes:
      - ~/.hermes:/opt/data
    networks:
      - hermes-net
networks:
  hermes-net:
    driver: bridge
```

سپد در `~/.hermes/config.yaml` خود، **نام container** را به عنوان hostname استفاده کنید:

```
model:
  provider: custom
  model: my-model
  base_url: http://vllm:8000/v1
  api_key: "none"
```

- از **نام container** (`vllm`) به عنوان hostname استفاده کنید — نه `localhost` یا `127.0.0.1` که به خود container Hermes اشاره می‌کنند.
- مقدار `model` باید با `--served-model-name` که به vLLM ارسال کرده‌اید مطابقت داشته باشد.
- `api_key` را روی هر رشته غیرخالی تنظیم کنید (vLLM به هدر نیاز دارد اما به طور پیش‌فرض تأیید نمی‌کند).
- **شکسته** trailing slash در `base_url` قرار **ندهید**.

### Docker run مستقل (بدون Compose)

اگر سرور استنتاج شما مستقیماً روی میزبان اجرا می‌شود (نه در Docker)، در macOS/Windows از `host.docker.internal` یا در Linux از `--network host` استفاده کنید:

macOS / Windows:

```
docker run -d \
  --name hermes \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  nousresearch/hermes-agent gateway run
```

```
# config.yaml
model:
  provider: custom
  model: my-model
  base_url: http://host.docker.internal:8000/v1
  api_key: "none"
```

Linux (شبکه‌بندی میزبان):

```
docker run -d \
  --name hermes \
  --network host \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

```
# config.yaml
model:
  provider: custom
  model: my-model
  base_url: http://127.0.0.1:8000/v1
  api_key: "none"
```

### تأیید اتصال

از داخل container Hermes، تأیید کنید سرور استنتاج قابل دسترس است:

```
docker exec hermes curl -s http://vllm:8000/v1/models
```

باید یک پاسخ JSON شامل مدل سرویس داده شده خود ببینید. اگر این شکست خورد، بررسی کنید:

1. هر دو container در همان شبکه Docker هستند (`docker network inspect hermes-net`)
2. سرور استنتاج روی `0.0.0.0` گوش می‌دهد، نه `127.0.0.1`
3. شماره پورت مطابقت دارد

### Ollama

Ollama به همان شکل کار می‌کند. اگر Ollama روی میزبان اجرا می‌شود، از `host.docker.internal:11434` (macOS/Windows) یا `127.0.0.1:11434` (Linux با `--network host`) استفاده کنید. اگر Ollama در container خودش روی همان شبکه Docker اجرا می‌شود:

```
model:
  provider: custom
  model: llama3
  base_url: http://ollama:11434/v1
  api_key: "none"
```

## عیب‌یابی

### Container فوراً خارج می‌شود

لاگ‌ها را بررسی کنید: `docker logs hermes`. علل رایج:

- فایل `.env` گمشده یا نامعتبر — ابتدا به صورت تعاملی اجرا کنید تا راه‌اندازی را تکمیل کنید
- تداخل پورت‌ها اگر با پورت‌های در معرض دید اجرا می‌کنید

### خطاهای "Permission denied"

hook stage2 container امتیازات را به کاربر غیر-root `hermes` (UID 10000) از طریق `s6-setuidgid` در داخل هر سرویس نظارت شده رها می‌کند. اگر `~/.hermes/` میزبان شما مالک UID متفاوتی است، `HERMES_UID`/`HERMES_GID` — یا псевдонیم‌های `PUID`/`PGID` برای تطابق با LinuxServer.io و image‌های NAS — را تنظیم کنید تا با کاربر میزبان شما مطابقت داشته باشد، یا مطمئن شوید پوشه داده قابل نوشتن است:

```
chmod -R 755 ~/.hermes
```

در یک NAS (UGOS، Synology، unRAID) پوشه داده معمولاً یک bind mount مالک یک UID میزبان است که container نمی‌تواند `chown` کند. `PUID`/`PGID` (یا `HERMES_UID`/`HERMES_GID`) را روی آن کاربر میزبان تنظیم کنید تا runtime به جای UID 10000 به عنوان مالک نصب اجرا شود:

```
docker run -d \
  --name hermes \
  -e PUID=1000 -e PGID=10 \
  -v /volume1/docker/hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

### ابزارهای مرورگر کار نمی‌کنند

Playwright به حافظه مشترک نیاز دارد. `--shm-size=1g` را به دستور Docker run خود اضافه کنید:

```
docker run -d \
  --name hermes \
  --shm-size=1g \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

### Gateway پس از مشکلات شبکه مجدداً متصل نمی‌شود

پرچم `--restart unless-stopped` اکثر شکست‌های موقت را مدیریت می‌کند. اگر gateway گیر کرده، container را بازیابی کنید:

```
docker restart hermes
```

### بررسی سلامت container

```
docker logs --tail 50 hermes          # لاگ‌های اخیر
docker run -it --rm nousresearch/hermes-agent:latest version     # تأیید نسخه
docker stats hermes                    # استفاده منابع
```

[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/docker.md)
