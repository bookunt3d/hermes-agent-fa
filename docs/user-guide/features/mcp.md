---
layout: docs
title: "MCP"
permalink: /docs/user-guide/features/mcp/
---

- 
- یکپارچه‌سازی‌ها
- MCP (پروتکل زمینه مدل)

# MCP (پروتکل زمینه مدل)

MCP به Hermes Agent اجازه می‌دهد به سرورهای ابزار خارجی متصل شود تا agent بتواند از ابزارهایی استفاده کند که خارج از خود Hermes زندگی می‌کنند — GitHub، پایگاه‌های داده، سیستم‌های فایل، پشته‌های مرورگر، APIهای داخلی و موارد دیگر.

اگر تا به حال خواسته‌اید Hermes از ابزاری استفاده کند که در جای دیگری از قبل وجود دارد، MCP معمولاً تمیزترین راه برای انجام این کار است.

## چه چیزی MCP به شما می‌دهد

- دسترسی به اکوسیستم‌های ابزار خارجی بدون نیاز به نوشتن یک ابزار بومی Hermes ابتدا
- سرورهای stdio محلی و سرورهای MCP HTTP از راه دور در یک پیکربندی
- کشف و ثبت خودکار ابزار در راه‌اندازی
- بسته‌های کمکی برای منابع و پرامپت‌های MCP وقتی توسط سرور پشتیبانی می‌شود
- فیلتر کردن به ازای هر سرور تا فقط ابزارهای MCP را که واقعاً می‌خواهید Hermes ببیند نمایش دهید

## شروع سریع

1. پشتیبانی MCP با نصب استاندارد عرضه می‌شود — هیچ مرحله اضافی لازم نیست.
2. یک سرور MCP به `~/.hermes/config.yaml` اضافه کنید:

پشتیبانی MCP با نصب استاندارد عرضه می‌شود — هیچ مرحله اضافی لازم نیست.

یک سرور MCP به `~/.hermes/config.yaml` اضافه کنید:

`~/.hermes/config.yaml`

```
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```

3. Hermes را شروع کنید:

```
hermes chat
```

4. از Hermes بخواهید از قابلیت پشتیبانی شده توسط MCP استفاده کند.

به عنوان مثال:

```
فایل‌های /home/user/projects را فهرست کنید و ساختار مخزن را خلاصه کنید.
```

Hermes ابزارهای سرور MCP را کشف کرده و مانند هر ابزار دیگری از آنها استفاده می‌کند.

## کاتالوگ: نصب با یک کلیک برای MCP‌های تأیید شده توسط Nous

Hermes یک کاتالوگ گزینش شده از سرورهای MCP را عرضه می‌کند که توسط کارکنان Nous بررسی و ادغام شده‌اند. آنها به طور پیش‌فرض غیرفعال هستند — فقط آنچه واقعاً می‌خواهید نصب کنید.

```
hermes mcp                # انتخابگر تعاملی (پیش‌فرض)
hermes mcp catalog        # لیست متن ساده، قابل اسکریپت‌نویسی
hermes mcp install n8n    # نصب یک ورودی کاتالوگ با نام
```

انتخابگر هر ورودی را با وضعیت فعلی آن نشان می‌دهد:

```
n8n          available              مدیریت و بازرسی workflow‌های n8n از Hermes
linear       enabled                مدیریت issue/پروژه Linear (OAuth از راه دور)
github       installed (disabled)   ابزارهای repo + PR GitHub
```

بر روی `Enter` در یک ردیف فشار دهید تا نصب شود (و هر گونه اعتبارنامه لازم را طی کنید)، فعال، غیرفعال یا حذف شود. ورودی‌های کاتالوگ تحت `optional-mcps/` در مخزن hermes-agent ذخیره می‌شوند — حضور در آن دایرکتوری به این معنی است که تأیید شده توسط Nous است. هیچ سطح ارسال جامعه‌ای وجود ندارد؛ ورودی‌ها با ادغام یک PR اضافه می‌شوند.

`Enter`
`optional-mcps/`

ورودی‌های کاتالوگ می‌توانند نیاز داشته باشند:

- کلید API — Hermes در زمان نصب پرامپت می‌دهد و مقدار را در `~/.hermes/.env` می‌نویسد. مقادیر غیر رمز (base URLs) به همان فایل می‌روند.
- OAuth (سرور از راه دور) — به صورت `auth: oauth` در پیکربندی شما نوشته می‌شود؛ کلاینت MCP در اولین اتصال مرورگر را باز می‌کند.
- OAuth (ارائه‌دهنده شخص ثالث مانند Google/GitHub) — Hermes شما را به `hermes auth <provider>` هدایت می‌کند اگر هنوز احراز هویت نکرده‌اید.

`~/.hermes/.env`
`auth: oauth`
`hermes auth <provider>`

### انتخاب ابزار در زمان نصب

پس از پیکربندی اعتبارنامه‌ها، Hermes سرور MCP را برای فهرست کردن هر ابزاری که در معرض دید قرار می‌دهد آزمایش کرده و یک لیست بررسی ارائه می‌دهد:

```
انتخاب ابزارها برای 'linear' (SPACE برای تغییر، ENTER برای تأیید)
  [x] find_issues       یافتن issueهای مطابق با یک پرس‌وجو
  [x] get_issue         دریافت یک issue واحد
  [x] create_issue      ایجاد یک issue جدید
  [ ] delete_workspace  حذف یک فضای کاری Linear
  ...
```

ردیف‌های از پیش انتخاب شده از منابع زیر می‌آیند:

1. انتخاب قبلی شما — اگر قبلاً این ورودی را نصب کرده‌اید (نصب مجدد آنچه را داشتید حفظ می‌کند — پیش‌فرض‌های مانیفست آن را بازنویسی نمی‌کنند)
2. `tools.default_enabled` مانیفست اگر ورودی یکی اعلام کند (برخی ورودی‌های کاتالوگ ابزارهای جهشی یا به ندرت مفید را از پیش حذف می‌کنند)
3. همه — اگر هیچ‌کدام اعمال نشود

`tools.default_enabled`

لیست بررسی را با ENTER ارسال کنید. فقط ابزارهای بررسی شده در `mcp_servers.<name>.tools.include` قرار می‌گیرند. اگر همه چیز را انتخاب کنید، هیچ فیلتری نوشته نمی‌شود (شکل پیکربندی تمیزترین، رفتار یکسان).

`mcp_servers.<name>.tools.include`

اگر آزمایش ناموفق باشد (سرور در دسترس نیست، OAuth هنوز تکمیل نشده، سرویس پشتیبان در حال اجرا نیست)، نصب همچنان موفق است: `tools.default_enabled` مانیفست مستقیماً اعمال می‌شود (اگر اعلام شده)، یا هیچ فیلتری نوشته نمی‌شود (اگر نشده). پس از در دسترس شدن سرور، `hermes mcp configure <name>` را مجدداً اجرا کنید تا بهبود یابد.

`tools.default_enabled`
`hermes mcp configure <name>`

### مدل اعتماد

نصب یک ورودی کاتالوگ هر آنچه مانیفست مشخص می‌کند را اجرا می‌کند — `git clone`، دستورات `bootstrap` ورودی (`pip install`، `npm install` و غیره)، و در نهایت کد خود سرور MCP. مانیفست‌ها از طریق بررسی PR در مخزن hermes-agent فیلتر می‌شوند، بنابراین Nous هر ورودی را قبل از عرضه بررسی کرده است — اما هنوز باید قبل از نصب، مانیفست را بخوانید، به ویژه فیلد `source:` مخزن، دستورات `install.bootstrap:` و هر فراخوانی `transport.command:`.

`git clone`
`bootstrap`
`pip install`
`npm install`
`source:`
`install.bootstrap:`
`transport.command:`

مانیفست‌ها در `optional-mcps/<name>/manifest.yaml` روی GitHub زندگی می‌کنند. انتخابگر همچنین URL `source:` مانیفست را در زمان نصب چاپ می‌کند تا بتوانید به سرعت مخزن upstream را تأیید کنید. صفحه MCP داشبورد وب همان جزئیات را برای هر ورودی کاتالوگ نشان می‌دهد — حمل‌ونقل، نوع احراز هویت، URL نقطه پایانی (HTTP) یا دستور + آرگومان‌ها (stdio)، منبع/مرجع نصب git و دستورات bootstrap، و یادداشت‌های تنظیم — با `source:` به عنوان یک لینک کلیک‌پذیر رندر شده، تا بتوانید دقیقاً بررسی کنید یک ورودی به چه چیزی متصل می‌شود یا چه چیزی را قبل از کلیک روی Install اجرا می‌کند.

[optional-mcps/<name>/manifest.yaml](https://github.com/NousResearch/hermes-agent/tree/main/optional-mcps)
`optional-mcps/<name>/manifest.yaml`
`source:`
`source:`

### سازگاری نسخه مانیفست

مانیفست‌ها یک `manifest_version` ثابت دارند. کاتالوگ رو به جلو سازگار است: اگر یک PR ورودی با `manifest_version` جدیدتر از آنچه Hermes نصب شده شما می‌فهمد اضافه کند، انتخابگر یک هشدار (`⚠ '<name>' requires a newer Hermes`) برای آن ورودی نشان می‌دهد به جای اینکه آن را به طور خاموش پنهان کند. وقتی این را دیدید `hermes update` را اجرا کنید تا آخرین Hermes را نصب کنید.

`manifest_version`
`manifest_version`
`⚠ '<name>' requires a newer Hermes`
`hermes update`

### جایگزینی Runtime `${ENV_VAR}`

`${ENV_VAR}`

در `transport.command`، `transport.args`، `transport.url` و `headers` یک ورودی، placeholdرهای `${VAR}` در زمان اتصال به سرور از متغیرهای محیطی (که شامل همه چیز در `~/.hermes/.env` است) حل می‌شوند. این زمانی مفید است که یک ورودی کاتالوگ بخواهد به مقداری که کاربر در جای دیگری پیکربندی کرده ارجاع دهد — مثلاً `${HOME}/foo` یا `${MY_PROVIDER_TOKEN}`.

`transport.command`
`transport.args`
`transport.url`
`headers`
`${VAR}`
`~/.hermes/.env`
`${HOME}/foo`
`${MY_PROVIDER_TOKEN}`

توجه داشته باشید این با `${INSTALL_DIR}` در مانیفست‌های کاتالوگ متفاوت است که در زمان نصب با مسیری که کاتالوگ مخزن ورودی را در آن کلون کرده جایگزین می‌شود.

`${INSTALL_DIR}`

### به‌روزرسانی انتخاب ابزار بعداً

```
hermes mcp configure linear
```

همان لیست بررسی را با انتخاب فعلی شما از پیش بررسی شده بازگشایی می‌کند. وقتی ابزارهای بیشتری می‌خواهید فعال شوند یا وقتی سرور ابزارهای جدیدی اضافه کرده که می‌خواهید در آنها شرکت کنید، از این استفاده کنید.

### به‌روزرسانی مانیفست کاتالوگ

MCP‌ها هرگز به طور خودکار به‌روزرسانی نمی‌شوند. پس از به‌روزرسانی Hermes اگر نسخه مانیفست تغییر کرده باشد، `hermes mcp install <name>` را مجدداً اجرا کنید تا تازه شود.

`hermes mcp install <name>`

برای افزودن یک MCP به کاتالوگ، یک PR علیه `optional-mcps/` باز کنید.

[optional-mcps/](https://github.com/NousResearch/hermes-agent/tree/main/optional-mcps)
`optional-mcps/`

## دو نوع سرور MCP

### سرورهای stdio

سرورهای stdio به عنوان زیرفرآیندهای محلی اجرا شده و از طریق stdin/stdout صحبت می‌کنند.

```
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

از سرورهای stdio استفاده کنید وقتی:

- سرور به صورت محلی نصب شده
- به دسترسی کم‌تأخیر به منابع محلی نیاز دارید
- از مستندات سرور MCP پیروی می‌کنید که `command`، `args` و `env` را نشان می‌دهد

`command`
`args`
`env`

### سرورهای HTTP

سرورهای MCP HTTP نقاط پایانی از راه دوری هستند که Hermes مستقیماً به آنها متصل می‌شود.

```
mcp_servers:
  remote_api:
    url: "https://mcp.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
```

از سرورهای HTTP استفاده کنید وقتی:

- سرور MCP در جای دیگری میزبانی می‌شود
- سازمان شما نقاط پایانی MCP داخلی در معرض دید قرار می‌دهد
- نمی‌خواهید Hermes یک زیرفرآیند محلی برای آن یکپارچه‌سازی ایجاد کند

### سرورهای HTTP احراز هویت شده با OAuth

اکثر سرورهای MCP میزبانی شده (Linear، Sentry، Atlassian، Asana، Figma، Stripe، …) به جای یک توکن bearer ثابت به OAuth 2.1 نیاز دارند. `auth: oauth` را تنظیم کنید و Hermes کشف، ثبت نام پویای کلاینت، PKCE، مبادله توکن، تازه‌سازی و احراز هویت step-up را از طریق SDK پایتون MCP مدیریت می‌کند.

`auth: oauth`

```
mcp_servers:
  linear:
    url: "https://mcp.linear.app/mcp"
    auth: oauth
```

در اولین اتصال، Hermes یک URL مجوز چاپ می‌کند، در صورت امکان مرورگر شما را باز می‌کند و منتظر callback OAuth روی یک پورت loopback محلی می‌ماند. توکن‌ها در `~/.hermes/mcp-tokens/<server>.json` با مجوزهای `0o600` کش می‌شوند؛ اجراهای بعدی آنها را به طور خاموش مجدداً استفاده می‌کنند تا زمانی که تازه‌سازی ناموفق باشد.

`~/.hermes/mcp-tokens/<server>.json`

**میزبان‌های از راه دور / headless.** وقتی Hermes روی ماشینی متفاوت از مرورگر شما اجرا می‌شود، callback loopback نمی‌تواند به لپ‌تاپ شما برسد. دو راه برای تکمیل جریان:

- **چسباندن مجدد (بدون تنظیم):** در یک ترمینال تعاملی Hermes URL مجوز را همراه با URL "Or paste the redirect URL here…" چاپ می‌کند. URL را در مرورگر خود باز کنید، تأیید کنید، URL کاملی که مرورگر در نهایت نشان می‌دهد را کپی کنید (redirect خطای اتصال نشان خواهد داد — این طبیعی است)، آن را در پرامپت بچسبانید. رشته‌های query `?code=…&state=…` خام هم کار می‌کنند.
- **forwarding پورت SSH:** `ssh -N -L <port>:127.0.0.1:<port> user@host` در یک ترمینال جداگانه، سپس اجازه دهید redirect به طور معمول اتفاق بیفتد.

`?code=…&state=…`
`ssh -N -L <port>:127.0.0.1:<port> user@host`

برای راهنمای کامل از جمله سرورهای بدون DCR (مثلاً Slack)، `client_id/client_secret` از پیش ثبت شده، سفارشی‌سازی scope و احراز هویت مجدد از طریق `hermes mcp login <server>` به [OAuth از طریق SSH / میزبان‌های از راه دور](/docs/guides/oauth-over-ssh#mcp-servers) مراجعه کنید.

[OAuth از طریق SSH / میزبان‌های از راه دور](/docs/guides/oauth-over-ssh#mcp-servers)
`client_id`
`client_secret`
`hermes mcp login <server>`

**تله — ارائه‌دهندگانی که از ثبت نام خودکار پشتیبانی نمی‌کنند (Google Drive، Atlassian).** برخی سرورها مرحله ثبت نام پویای کلاینت (RFC 7591) را که `auth: oauth` خام به آن وابسته است رد می‌کنند — سرور رسمی Google Drive (`https://drivemcp.googleapis.com/mcp/v1`) خطای `400 Bad Request` برمی‌گرداند، بنابراین کلاینت OAuth ایجاد نمی‌شود و توکنی دریافت نمی‌شود. نشانه ظریف است: این سرورها همچنین `tools/list` را بدون `auth` سرویس می‌دهند بنابراین `hermes mcp login` می‌تواند ابزارها را فهرست کند و به نظر کار می‌رسد، اما هر فراخوان ابزار واقعی بعداً تایم‌اوت می‌دهد. `hermes mcp login` حالا این را تشخیص می‌دهد (بررسی می‌کند آیا واقعاً توکنی روی دیسک نشسته) و به شما می‌گوید OAuth client خود را تهیه کنید. یکی در کنسول ارائه‌دهنده ایجاد کنید و به پیکربندی اضافه کنید:

`auth: oauth`
`https://drivemcp.googleapis.com/mcp/v1`
`400 Bad Request`
`tools/list`
`hermes mcp login`
`hermes mcp login`

```
mcp_servers:
  googledrive:
    url: "https://drivemcp.googleapis.com/mcp/v1"
    auth: oauth
    oauth:
      client_id: "<your-oauth-client-id>"
      client_secret: "<your-oauth-client-secret>"
```

سپس `hermes mcp login googledrive` را اجرا کنید — با کلاینت از پیش ثبت شده، Hermes ثبت نام را رد می‌کند و جریان مجوز مرورگر معمولی را اجرا می‌کند.

`hermes mcp login googledrive`

**تله — ریس بارگذاری خودکار پیکربندی.** وقتی `~/.hermes/config.yaml` را از داخل یک جلسه Hermes در حال اجرا ویرایش می‌کنید، CLI اتصالات MCP را با تایم‌اوت ۳۰ ثانیه بارگذاری مجدد خودکار می‌کند. این برای یک جریان OAuth تعاملی کافی نیست. ورودی را اضافه کنید، سپس `hermes mcp login <server>` را از یک ترمینال تازه اجرا کنید — این کل ۵ دقیقه منتظر می‌ماند تا احراز هویت را تکمیل کنید.

`~/.hermes/config.yaml`
`hermes mcp login <server>`

## mTLS / گواهی‌های کلاینت

سرورهای MCP HTTP از راه دور که به TLS متقابل (احراز هویت گواهی کلاینت) نیاز دارند از طریق `client_cert`/`client_key` پشتیبانی می‌شوند. Hermes گواهی حل شده را به کلاینت HTTP زیربنایی برای دستکشی TLS ارسال می‌کند.

`client_cert`
`client_key`

`client_cert` سه شکل می‌پذیرد:

`client_cert`

- **یک مسیر PEM ترکیبی واحد** — یک فایل حاوی هر دو گواهی و کلید خصوصی:

```
mcp_servers:
  internal_api:
    url: "https://mcp.internal.example.com/mcp"
    client_cert: "~/.certs/mcp-client.pem"
```

- **یک تاپل `[cert, key]`** — گواهی و کلید در فایل‌های جداگانه (معادل تنظیم `client_cert` + `client_key`):

`[cert, key]`
`client_cert`
`client_key`

```
mcp_servers:
  internal_api:
    url: "https://mcp.internal.example.com/mcp"
    client_cert: ["~/.certs/mcp-client.crt", "~/.certs/mcp-client.key"]
```

- **یک تاپل `[cert, key, password]`** — وقتی کلید خصوصی رمزگذاری شده، عنصر سوم رمز عبور کلید است:

`[cert, key, password]`

```
mcp_servers:
  internal_api:
    url: "https://mcp.internal.example.com/mcp"
    client_cert: ["~/.certs/mcp-client.crt", "~/.certs/mcp-client.key", "${MCP_KEY_PASSWORD}"]
```

همچنین می‌توانید گواهی و کلید را کاملاً جداگانه نگه دارید از طریق `client_cert` (PEM ترکیبی) به علاوه `client_key` صریح. مسیرها از گسترش `~` پشتیبانی می‌کنند؛ فایل گمشده خطای واضح و محدود به سرور ایجاد می‌کند به جای یک خطا دستکشی TLS نامفهوم.

`client_cert`
`client_key`
`~`

## مرجع پیکربندی پایه

Hermes پیکربندی MCP را از `~/.hermes/config.yaml` تحت `mcp_servers` می‌خواند.

`~/.hermes/config.yaml`
`mcp_servers`

### کلیدهای رایج

| کلید | نوع | معنی |
| --- | --- | --- |
| `command` | رشته | اجرایی برای سرور MCP stdio |
| `args` | لیست | آرگومان‌ها برای سرور stdio |
| `env** | نگاشت | متغیرهای محیطی ارسال شده به سرور stdio |
| `url` | رشته | نقطه پایانی HTTP MCP |
| `headers` | نگاشت | هدرهای HTTP برای سرورهای از راه دور |
| `client_cert` | رشته / لیست | گواهی کلاینت برای mTLS — مسیر PEM ترکیبی، یا `[cert, key]` / `[cert, key, password]` |
| `client_key` | رشته | مسیر PEM کلید خصوصی کلاینت (وقتی از `client_cert` جداگانه) |
| `timeout` | عدد | تایم‌اوت فراخوانی ابزار |
| `connect_timeout` | عدد | تایم‌اوت اتصال اولیه (همچنین دستکشی handshke `initialize` MCP را محدود می‌کند) |
| `idle_timeout_seconds` | عدد | بازیافت سرور stdio پس از این تعداد ثانیه بدون فراخوانی ابزار (0= هرگز، پیش‌فرض). سرور به طور شفاف در فراخوانی ابزار بعدی راه‌اندازی مجدد می‌شود. |
| `max_lifetime_seconds` | عدد | بازیافت سرور stdio پس از این عمر کل (0= هرگز، پیش‌فرض). در استفاده بعدی به طور شفاف راه‌اندازی مجدد می‌شود. |
| `enabled` | بولین | اگر `false`، Hermes سرور را کاملاً رد می‌کند |
| `supports_parallel_tool_calls` | بولین | اگر `true`، ابزارهای این سرور می‌توانند همزمان اجرا شوند |
| `tools` | نگاشت | فیلتر کردن ابزار و سیاست کمکی به ازای هر سرور |

`command`
`args`
`env`
`url`
`headers`
`client_cert`
`[cert, key]`
`[cert, key, password]`
`client_key`
`client_cert`
`timeout`
`connect_timeout`
`initialize`
`idle_timeout_seconds`
`0`
`max_lifetime_seconds`
`0`
`enabled`
`false`
`supports_parallel_tool_calls`
`true`
`tools`

### مثال stdio حداقلی

```
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
```

### بازیافت سرورهای stdio سنگین حافظه

سرورهای MCP مبتنی بر مرورگر (مثلاً `@playwright/mcp`) پس از اولین فراخوانی ابزار خود یک Chromium کامل را نگه می‌دارند — صدها مگابایت که هرگز آزاد نمی‌شوند. به بازیافت خودکار بپیوندید و سرور پس از محدودیت idle/lifetime برداشته شده و سپس در دفعه بعدی که یکی از ابزارهایش فراخوانی شود به طور شفاف راه‌اندازی مجدد می‌شود (ابزارهایش در تمام مدت ثبت مانده):

`@playwright/mcp`

```
mcp_servers:
  playwright:
    command: "npx"
    args: ["-y", "@playwright/mcp@latest", "--headless"]
    idle_timeout_seconds: 900     # بازیافت پس از ۱۵ دقیقه بدون فراخوانی ابزار
    max_lifetime_seconds: 86400   # و حداقل یک بار در روز صرف نظر از شرایط
```

### مثال HTTP حداقلی

```
mcp_servers:
  company_api:
    url: "https://mcp.internal.example.com"
    headers:
      Authorization: "Bearer ***"
```

## پیش‌فرض‌های داخلی

برای سرورهای MCP شناخته شده، `hermes mcp add` یک پرچم `--preset` می‌پذیرد که جزئیات حمل‌ونقل را پر می‌کند تا مجبور نباشید دستور و آرگومان‌ها را جستجو کنید. پیش‌فرض فقط پیش‌فرض‌ها را تأمین می‌کند — هر چیز دیگری (متغیرهای محیطی، هدرها، فیلتر کردن) که در همان خط فرمان ارسال می‌کنید همچنان اولویت دارد.

`hermes mcp add`
`--preset`

| پیش‌فرض | چه چیزی را متصل می‌کند |
| --- | --- |
| `codex` | سرور MCP Codex CLI (`codex mcp-server` از طریق stdio). به CLI `codex` در PATH نیاز دارد. |

`codex`
`codex mcp-server`
`codex`

```
# افزودن Codex CLI به عنوان سرور MCP در یک خط
hermes mcp add codex --preset codex
```

این معادل زیر را می‌نویسد:

```
mcp_servers:
  codex:
    command: "codex"
    args: ["mcp-server"]
```

می‌توانید هر نام محلی انتخاب کنید (`hermes mcp add my-codex --preset codex` درست است)؛ پیش‌فرض فقط پیش‌فرض‌های `command`/`args` را تأمین می‌کند.

`hermes mcp add my-codex --preset codex`
`command`
`args`

## چگونه Hermes ابزارهای MCP را ثبت می‌کند

Hermes پیشوندهای ابزارهای MCP را اضافه می‌کند تا با نام‌های داخلی تداخل نداشته باشند:

```
mcp_<server_name>_<tool_name>
```

مثال‌ها:

| سرور | ابزار MCP | نام ثبت شده |
| --- | --- | --- |
| `filesystem` | `read_file` | `mcp_filesystem_read_file` |
| `github` | `create-issue` | `mcp_github_create_issue` |
| `my-api` | `query.data` | `mcp_my_api_query_data` |

`filesystem`
`read_file`
`mcp_filesystem_read_file`
`github`
`create-issue`
`mcp_github_create_issue`
`my-api`
`query.data`
`mcp_my_api_query_data`

در عمل، معمولاً نیازی به فراخوانی دستی نام پیشوندی ندارید — Hermes ابزار را می‌بیند و در استدلال عادی آن را انتخاب می‌کند.

## ابزارهای کمکی MCP

وقتی پشتیبانی شود، Hermes همچنین ابزارهای کمکی اطراف منابع و پرامپت‌های MCP ثبت می‌کند:

- `list_resources`
- `read_resource`
- `list_prompts`
- `get_prompt`

`list_resources`
`read_resource`
`list_prompts`
`get_prompt`

اینها با همان الگوی پیشوند برای هر سرور ثبت می‌شوند، به عنوان مثال:

- `mcp_github_list_resources`
- `mcp_github_get_prompt`

`mcp_github_list_resources`
`mcp_github_get_prompt`

### مهم

این ابزارهای کمکی اکنون دارای آگاهی قابلیت هستند:

- Hermes فقط ابزارهای کمکی منبع را ثبت می‌کند اگر جلسه MCP واقعاً از عملیات منبع پشتیبانی کند
- Hermes فقط ابزارهای کمکی پرامپت را ثبت می‌کند اگر جلسه MCP واقعاً از عملیات پرامپت پشتیبانی کند

بنابراین سروری که ابزارهای فراخواندنی اما بدون منبع/پرامپت ارائه می‌دهد آن بسته‌های کمکی اضافی را دریافت نخواهد کرد.

## فیلتر کردن به ازای هر سرور

### فیلتر کردن ابزارهای کمکی نیز

همچنین می‌توانید بسته‌های کمکی اضافه شده توسط Hermes را جداگانه غیرفعال کنید:

```
mcp_servers:
  docs:
    url: "https://mcp.docs.example.com"
    tools:
      prompts: false
      resources: false
```

یعنی:

- `tools.resources: false` غیرفعال می‌کند `list_resources` و `read_resource`
- `tools.prompts: false` غیرفعال می‌کند `list_prompts` و `get_prompt`

`tools.resources: false`
`list_resources`
`read_resource`
`tools.prompts: false`
`list_prompts`
`get_prompt`

### مثال کامل

```
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [create_issue, list_issues, search_code]
      prompts: false
  stripe:
    url: "https://mcp.stripe.com"
    headers:
      Authorization: "Bearer ***"
    tools:
      exclude: [delete_customer]
      resources: false
  legacy:
    url: "https://mcp.legacy.internal"
    enabled: false
```

## چه اتفاقی می‌افتد اگر همه چیز فیلتر شود؟

اگر پیکربندی شما همه ابزارهای فراخواندنی را فیلتر کند و همه ابزارهای کمکی پشتیبانی شده را غیرفعال یا حذف کند، Hermes یک مجموعه ابزار runtime MCP خالی برای آن سرور ایجاد نمی‌کند.

این فهرست ابزار را تمیز نگه می‌دارد.

## رفتار Runtime

### زمان کشف

Hermes سرورهای MCP را در هنگام راه‌اندازی کشف می‌کند و ابزارهای آنها را در ثبت ابزار عادی ثبت می‌کند.

### کشف پویای ابزار

سرورهای MCP می‌توانند Hermes را زمانی که ابزارهای موجود آنها در runtime تغییر می‌کند با ارسال یک اعلان `notifications/tools/list_changed` مطلع کنند. وقتی Hermes این اعلان را دریافت می‌کند، به طور خودکار لیست ابزار سرور را مجدداً واکشی می‌کند و ثبت را به‌روز می‌کند — نیازی به `/reload-mcp` دستی نیست.

`notifications/tools/list_changed`
`/reload-mcp`

این برای سرورهای MCP مفید است که قابلیت‌هایشان به صورت پویا تغییر می‌کند (مثلاً سروری که ابزارها را وقتی یک طرحواره پایگاه داده جدید بارگذاری می‌شود اضافه می‌کند، یا ابزارها را وقتی یک سرویس آفلاین می‌شود حذف می‌کند).

بازیابی با قفل محافظت می‌شود بنابراین اعلان‌های پشت سر هم از یک سرور باعث بازیابی‌های همپوشان نمی‌شوند. اعلان‌های تغییر پرامپت و منبع (`prompts/list_changed`، `resources/list_changed`) دریافت می‌شوند اما هنوز عمل نمی‌شوند.

`prompts/list_changed`
`resources/list_changed`

### بازبارگذاری

اگر پیکربندی MCP را تغییر دهید، از این استفاده کنید:

```
/reload-mcp
```

این سرورهای MCP را از پیکربندی بازبارگذاری می‌کند و لیست ابزارهای موجود را تازه می‌کند. برای تغییرات ابزار runtime که توسط خود سرور ارسال می‌شوند، به کشف پویای ابزار بالا مراجعه کنید.

### مجموعه ابزارها

هر سرور MCP پیکربندی شده همچنین یک مجموعه ابزار runtime ایجاد می‌کند وقتی حداقل یک ابزار ثبت شده اضافه می‌کند:

```
mcp-<server>
```

این سرورهای MCP را در سطح مجموعه ابزار آسان‌تر می‌کند.

## مدل امنیتی

### فیلتر کردن محیط stdio

برای سرورهای stdio، Hermes محیط کامل پوسته شما را کورانه عبور نمی‌دهد.

فقط `env` صریحاً پیکربندی شده به علاوه یک پایه ایمن عبور داده می‌شود. این نشت تصادفی رمزها را کاهش می‌دهد.

`env`

### کنترل قرار گرفتن در معرض سطح پیکربندی

پشتیبانی فیلتر جدید همچنین یک کنترل امنیتی است:

- ابزارهای خطرناکی را که نمی‌خواهید مدل ببیند غیرفعال کنید
- فقط یک لیست سفید حداقلی برای یک سرور حساس نمایش دهید
- بسته‌های کمکی منبع/پرامپت را وقتی نمی‌خواهید آن سطح نمایش داده شود غیرفعال کنید

## مثال‌های استفاده

### سرور GitHub با سطح حداقلی مدیریت Issue

```
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [list_issues, create_issue, update_issue]
      prompts: false
      resources: false
```

مانند این استفاده کنید:

```
Show me open issues labeled bug, then draft a new issue for the flaky MCP reconnection behavior.
```

### سرور Stripe با حذف اقدامات خطرناک

```
mcp_servers:
  stripe:
    url: "https://mcp.stripe.com"
    headers:
      Authorization: "Bearer ***"
    tools:
      exclude: [delete_customer, refund_payment]
```

مانند این استفاده کنید:

```
Look up the last 10 failed payments and summarize common failure reasons.
```

### سرور فایل سیستم برای یک ریشه پروژه واحد

```
mcp_servers:
  project_fs:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]
```

مانند این استفاده کنید:

```
Inspect the project root and explain the directory layout.
```

## عیب‌یابی

### سرور MCP متصل نمی‌شود

بررسی کنید:

```
# تأیید وابستگی‌های MCP نصب شده‌اند (از قبل در نصب استاندارد گنجانده شده)
cd ~/.hermes/hermes-agent && uv pip install -e ".[mcp]"
node --version
npx --version
```

سپس پیکربندی خود را بررسی کنید و Hermes را مجدداً راه‌اندازی کنید.

### ابزارها ظاهر نمی‌شوند

علل احتمالی:

- سرور نتوانست متصل شود
- کشف ناموفق بود
- پیکربندی فیلتر شما ابزارها را حذف کرد
- قابلیت کمکی در آن سرور وجود ندارد
- سرور با `enabled: false` غیرفعال است

`enabled: false`

اگر عمداً فیلتر می‌کنید، این عادی است.

### چرا ابزارهای کمکی منبع یا پرامپت ظاهر نشدند؟

زیرا Hermes اکنون فقط آن بسته‌های کمکی را ثبت می‌کند وقتی هر دو شرط برقرار باشد:

1. پیکربندی شما آنها را مجاز می‌داند
2. جلسه سرور واقعاً از قابلیت پشتیبانی می‌کند

این عمدی است و فهرست ابزار را صادقانه نگه می‌دارد.

## فراخوان‌های موازی ابزار

به طور پیش‌فرض، ابزارهای MCP به صورت متوالی اجرا می‌شوند — یکی در یک زمان. اگر سرور MCP شما ابزارهایی ارائه می‌دهد که اجرای همزمان آنها بی‌خطر است (مثلاً پرس‌وجوهای فقط خواندنی، فراخوان‌های API مستقل)، می‌توانید اجرای موازی را فعال کنید:

```
mcp_servers:
  docs:
    command: "docs-server"
    supports_parallel_tool_calls: true
```

وقتی `supports_parallel_tool_calls` `true` باشد، Hermes ممکن است چندین ابزار از آن سرور را در یک دسته فراخوان ابزار واحد همزمان اجرا کند، دقیقاً مانند ابزارهای فقط خواندنی داخلی (`web_search`، `read_file` و غیره).

`supports_parallel_tool_calls`
`true`

فقط فراخوان‌های موازی را برای سرورهایی فعال کنید که اجرای همزمان ابزارهایشان بی‌خطر است. اگر ابزارها حالت مشترک، فایل‌ها، پایگاه‌های داده یا منابع خارجی را می‌خوانند و می‌نویسند، قبل از فعال کردن این تنظیم شرایط مسابقه خواندن/نوشتن را بررسی کنید.

## پشتیبانی MCP Sampling

سرورهای MCP می‌توانند از Hermes از طریق پروتکل `sampling/createMessage` استنتاج LLM درخواست کنند. این به یک سرور MCP اجازه می‌دهد از Hermes بخواهد متنی را از طرف آن تولید کند — مفید برای سرورهایی که به قابلیت‌های LLM نیاز دارند اما به مدل خودشان دسترسی ندارند.

`sampling/createMessage`

Sampling به طور پیش‌فرض برای همه سرورهای MCP فعال است (وقتی SDK MCP از آن پشتیبانی می‌کند). آن را برای هر سرور در کلید `sampling` پیکربندی کنید:

`sampling`

```
mcp_servers:
  my_server:
    command: "my-mcp-server"
    sampling:
      enabled: true            # فعال کردن sampling (پیش‌فرض: true)
      model: "openai/gpt-4o"  # بازنویسی مدل برای درخواست‌های sampling (اختیاری)
      max_tokens_cap: 4096     # حداکثر توکن‌ها برای هر پاسخ sampling (پیش‌فرض: 4096)
      timeout: 30              # تایم‌اوت به ثانیه برای هر درخواست (پیش‌فرض: 30)
      max_rpm: 10              # محدودیت سرعت: حداکثر درخواست‌ها در دقیقه (پیش‌فرض: 10)
      max_tool_rounds: 5       # حداکثر دورهای استفاده از ابزار در حلقه‌های sampling (پیش‌فرض: 5)
      allowed_models: []       # لیست سفید نام‌های مدلی که سرور می‌تواند درخواست کند (خالی = هر کدام)
      log_level: "info"        # سطح گزارش حسابرسی: debug، info، یا warning (پیش‌فرض: info)
```

هندلر sampling شامل یک محدودگر سرعت پنجره لغزان، تایم‌اوت‌های هر درخواست و محدودیت‌های عمق حلقه ابزار برای جلوگیری از استفاده بی‌رویه است. معیارها (تعداد درخواست‌ها، خطاها، توکن‌های استفاده شده) برای هر نمونه سرور ردیابی می‌شوند.

برای غیرفعال کردن sampling برای یک سرور خاص:

```
mcp_servers:
  untrusted_server:
    url: "https://mcp.example.com"
    sampling:
      enabled: false
```

## اجرای Hermes به عنوان یک سرور MCP

علاوه بر اتصال به سرورهای MCP، Hermes همچنین می‌تواند یک سرور MCP باشد. این به سایر عوامل سازگار با MCP (Claude Code، Cursor، Codex، یا هر کلاینت MCP) اجازه می‌دهد از قابلیت‌های پیام‌رسانی Hermes استفاده کنند — لیست مکالمات، خواندن تاریخچه پیام‌ها، و ارسال پیام در تمام پلتفرم‌های متصل شما.

### چه زمانی از این استفاده کنید

- می‌خواهید Claude Code، Cursor، یا یک کدگذار دیگر پیام‌های Telegram/Discord/Slack را از طریق Hermes ارسال و بخواند
- می‌خواهید یک سرور MCP واحد که به همه پلتفرم‌های متصل پیام‌رسانی Hermes به یکباره پل بزند
- قبلاً یک گیت‌وی Hermes در حال اجرا با پلتفرم‌های متصل شده دارید

### شروع سریع

```
hermes mcp serve
```

این یک سرور MCP stdio راه‌اندازی می‌کند. کلاینت MCP (نه شما) چرخه حیات فرآیند را مدیریت می‌کند.

### پیکربندی کلاینت MCP

Hermes را به پیکربندی کلاینت MCP خود اضافه کنید. به عنوان مثال، در `~/.claude/claude_desktop_config.json` Claude Code:

`~/.claude/claude_desktop_config.json`

```
{
  "mcpServers": {
    "hermes": {
      "command": "hermes",
      "args": ["mcp", "serve"]
    }
  }
}
```

یا اگر Hermes را در یک مکان خاص نصب کرده باشید:

```
{
  "mcpServers": {
    "hermes": {
      "command": "/home/user/.hermes/hermes-agent/venv/bin/hermes",
      "args": ["mcp", "serve"]
    }
  }
}
```

### ابزارهای موجود

سرور MCP ۱۰ ابزار ارائه می‌دهد، سطح ادغام کانال OpenClaw به علاوه یک مرورگر کانال خاص Hermes:

| ابزار | توضیح |
| --- | --- |
| `conversations_list` | لیست مکالمات پیام‌رسانی فعال. فیلتر بر اساس پلتفرم یا جستجو بر اساس نام. |
| `conversation_get` | دریافت اطلاعات دقیق درباره یک مکالمه با کلید جلسه. |
| `messages_read` | خواندن تاریخچه پیام‌های اخیر یک مکالمه. |
| `attachments_fetch` | استخراج پیوست‌های غیرمتنی (تصاویر، رسانه) از یک پیام خاص. |
| `events_poll` | بررسی رویدادهای مکالمه جدید از یک نقطه مکان‌نما. |
| `events_wait` | پولینگ بلند / بلاک کردن تا رویداد بعدی برسد (تقریباً بی‌درنگ). |
| `messages_send` | ارسال پیام از طریق یک پلتفرم (مثلاً `telegram:123456`، `discord:#general`). |
| `channels_list` | لیست اهداف پیام‌رسانی موجود در تمام پلتفرم‌ها. |
| `permissions_list_open` | لیست درخواست‌های تأیید در انتظار مشاهده شده در این جلسه پل. |
| `permissions_respond` | تأیید یا رد یک درخواست تأیید در انتظار. |

`conversations_list`
`conversation_get`
`messages_read`
`attachments_fetch`
`events_poll`
`events_wait`
`messages_send`
`telegram:123456`
`discord:#general`
`channels_list`
`permissions_list_open`
`permissions_respond`

### سیستم رویداد

سرور MCP شامل یک پل رویداد زنده است که پایگاه داده جلسه Hermes را برای پیام‌های جدید بررسی می‌کند. این آگاهی تقریباً بی‌درنگ کلاینت‌های MCP از مکالمات ورودی را فراهم می‌کند:

```
# بررسی رویدادهای جدید (غیرbloک)
events_poll(after_cursor=0)
# انتظار برای رویداد بعدی (bloک تا تایم‌اوت)
events_wait(after_cursor=42, timeout_ms=30000)
```

انواع رویداد: `message`، `approval_requested`، `approval_resolved`

`message`
`approval_requested`
`approval_resolved`

صف رویداد در حافظه است و وقتی پل متصل می‌شود شروع می‌شود. پیام‌های قدیمی‌تر از طریق `messages_read` در دسترس هستند.

`messages_read`

### گزینه‌ها

```
hermes mcp serve              # حالت عادی
hermes mcp serve --verbose    # گزارش اشکال‌زایی در stderr
```

### چگونه کار می‌کند

سرور MCP داده‌های مکالمه را مستقیماً از فروشگاه جلسه Hermes (`~/.hermes/sessions/sessions.json` و پایگاه داده SQLite) می‌خواند. یک رشته پس‌زمینه پایگاه داده را برای پیام‌های جدید بررسی می‌کند و یک صف رویداد در حافظه حفظ می‌کند. برای ارسال پیام‌ها، از همان موتور ارسال داخلی (`tools/send_message_tool.py`) استفاده می‌کند که تحویل cron و `hermes send` CLI را تقویت می‌کند.

`~/.hermes/sessions/sessions.json`
`tools/send_message_tool.py`
`hermes send`

گیت‌وی نیازی نیست برای عملیات خواندن (لیست مکالمات، خواندن تاریخچه، بررسی رویدادها) اجرا شود. باید برای عملیات ارسال اجرا شود، زیرا سازگارنده‌های پلتفرم به اتصالات فعال نیاز دارند.

### محدودیت‌های فعلی

- نمونه تعبیه شده `hermes mcp serve` امروز یک سرور MCP فقط stdio ارائه می‌دهد. اگر به یک سرور HTTP MCP نیاز دارید، یک سازگارنده جداگانه اجرا کنید — یا، بسیار رایج‌تر، از سمت کلاینت Hermes استفاده کنید که از قبل هم stdio و هم HTTP را صحبت می‌کند (`url` + `headers` در `mcp_servers.yaml`/`config.yaml`؛ به سرورهای HTTP بالا مراجعه کنید).
- بررسی رویداد با فواصل ~200ms از طریق بررسی پایگاه داده بهینه شده با mtime (وقتی فایل‌ها تغییر نکرده کار را رد می‌کند)
- هنوز هیچ پروتکل اعلان push `claude/channel` وجود ندارد
- ارسال‌های فقط متن (بدون ارسال رسانه/پیوست از طریق `messages_send`)

`hermes mcp serve`
`url`
`headers`
`mcp_servers.yaml`
`config.yaml`
`claude/channel`
`messages_send`

## مستندات مرتبط

- استفاده از MCP با Hermes
- دستورات CLI
- دستورات اسلش
- سؤالات متداول

[استفاده از MCP با Hermes](/docs/guides/use-mcp-with-hermes/)
[دستورات CLI](/docs/reference/cli-commands/)
[دستورات اسلش](/docs/reference/slash-commands/)
[سؤالات متداول](/docs/reference/faq/)
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/mcp.md)
