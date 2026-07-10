---
layout: docs
title: "جلسات"
permalink: /docs/user-guide/sessions/
---

- 
- استفاده از Hermes
- جلسات

# جلسات

Hermes Agent به طور خودکار هر مکالمه را به عنوان یک جلسه ذخیره می‌کند. جلسات بازیابی مکالمه، جستجوی بین جلسه‌ای و مدیریت کامل تاریخچه مکالمه را ممکن می‌سازند.

## نحوه کار جلسات

هر مکالمه — چه از CLI، Telegram، Discord، Slack، WhatsApp، Signal، Matrix، Teams یا هر پلتفرم پیام‌رسان دیگر — به عنوان یک جلسه با تاریخچه کامل پیام ذخیره می‌شود. جلسات در مکان‌های زیر ردیابی می‌شوند:

1. دیتابیس SQLite (`~/.hermes/state.db`) — فراداده ساختاریافته جلسه با FTS5 full-text search، به علاوه تاریخچه کامل پیام

`~/.hermes/state.db`

دیتابیس SQLite ذخیره می‌کند:

- شناسه جلسه، پلتفرم منبع، شناسه کاربر
- عنوان جلسه (نام منحصربفرد و خوانا)
- نام مدل و پیکربندی
- اسنپشات system prompt
- تاریخچه کامل پیام (نقش، محتوا، فراخوانی‌های ابزار، نتایج ابزار)
- شمارش توکن (ورودی/خروجی)
- برچسب‌های زمانی (started_at, ended_at)
- شناسه جلسه والد (برای تقسیم جلسه ناشی از فشرده‌سازی)

### چه چیزی به سیاق اضافه می‌کند

Hermes تاریخچه جلسه را ذخیره می‌کند تا بتواند مکالمات را بازیابی کند، اما هر بایتی که تاکنون پردازش کرده را دوباره ارسال نمی‌کند. در هر نوبت، مدل system prompt انتخاب شده، پنجره مکالمه فعلی و هر محتوایی که Hermes به طور صریح برای آن نوبت تزریق می‌کند را می‌بیند.

پیوست‌های رسانه به عنوان ورودی‌های محدود به نوبت مدیریت می‌شوند:

- تصاویر ممکن است به طور بومی به فراخوانی مدل بعدی پیوست شوند، یا وقتی مدل فعال از vision بومی پشتیبانی نمی‌کند به یک توصیف متنی پیش‌تحلیل شوند.
- صدا وقتی speech-to-text پیکربندی شده باشد به متن تبدیل می‌شود.
- اسناد متنی می‌توانند متن استخراج شده خود را داشته باشند؛ سایر انواع اسناد معمولاً با یک مسیر محلی ذخیره شده و یک یادداشت کوتاه نمایش داده می‌شوند.
- مسیرهای پیوست و متن استخراج/مشتق شده می‌توانند در رونوشت ظاهر شوند، اما بایت‌های خام تصویر، صدا یا فایل باینری به طور مکرر به پرامپت‌های آینده کپی نمی‌شوند.

به عنوان مثال، اگر کاربری تصویری ارسال کند و از Hermes بخواهد از آن meme بسازد، Hermes ممکن است آن تصویر را یک بار با vision بررسی کند و یک اسکریپت پردازش تصویر اجرا کند. نوبت‌های آینده JPEG اصلی را به طور خودکار در سیاق حمل نمی‌کنند. فقط آنچه را که در مکالمه نوشته شده حمل می‌کنند، مانند درخواست کاربر، توصیف کوتاه تصویر، مسیر کش محلی یا پاسخ نهایی assistant.

شایع‌ترین دلیل رشد سیاق خود فایل رسانه نیست. متن مفصل است: رونوشتهای چسبانده شده، لاگ‌های کامل، خروجی‌های بزرگ ابزار، diff‌های طولانی، گزارش‌های وضعیت تکراری و اثبات‌های مفصل. خلاصه‌ها، مسیرهای فایل، قطعات متمرکز و جستجوهای مبتنی بر ابزار را بر کپی کردن artifact‌های بزرگ در چت ترجیح دهید.

از `/compress` وقتی یک جسله طولانی شود، `/new` برای یک رشته جدید و `hermes sessions prune` فقط وقتی می‌خواهید جلسات قدیمی پایان یافته را از فروشگاه حذف کنید استفاده کنید. فشرده‌سازی سیاق فعال را کاهش می‌دهد؛ حذف حریم خصوصی نیست.
یک نام به `/new` ارسال کنید (مثلاً `/new payments-refactor`) تا عنوان اولیه جسله جدید را از ابتدا تنظیم کنید — مفید برای پیدا کردن آن بعداً با `/resume <name>` یا در انتخابگر `/sessions`.

`/compress`
`/new`
`hermes sessions prune`
`/new`
`/new payments-refactor`
`/resume <name>`
`sessions`

### منابع جلسه

هر جلسه با پلتفرم منبع خود برچسب گذاری شده است:

| منبع | توضیحات |
| --- | --- |
| cli | CLI تعاملی (`hermes` یا `hermes chat`) |
| telegram | پیام‌رسان Telegram |
| discord | سرور/DM Discord |
| slack | workspace Slack |
| whatsapp | پیام‌رسان WhatsApp |
| signal | پیام‌رسان Signal |
| matrix | اتاق‌های Matrix و DMs |
| mattermost | کانال‌های Mattermost |
| email | ایمیل (IMAP/SMTP) |
| sms | SMS از طریق Twilio |
| dingtalk | پیام‌رسان DingTalk |
| feishu | پیام‌رسان Feishu/Lark |
| wecom | WeCom (WeChat Work) |
| weixin | Weixin (WeChat شخصی) |
| bluebubbles | Apple iMessage از طریق سرور macOS BlueBubbles |
| qqbot | QQ Bot (Tencent QQ) از طریق API رسمی v2 |
| homeassistant | مکالمه Home Assistant |
| webhook | webhook‌های ورودی |
| api-server | درخواست‌های سرور API |
| acp | یکپارچه‌سازی ویرایشگر ACP |
| cron | کارهای cron زمان‌بندی شده |
| batch | اجرای پردازش دسته‌ای |

## بازیابی جلسه CLI

مکالمات قبلی را از CLI با استفاده از `--continue` یا `--resume` بازیابی کنید:

`--continue`
`--resume`

### ادامه آخرین جلسه

```
# بازیابی آخرین جلسه CLIhermes --continuehermes -c# یا با زیر دستور chathermes chat --continuehermes chat -c
```

این آخرین جلسه `cli` را از دیتابیس SQLite جستجو کرده و تاریخچه مکالمه کامل آن را بارگذاری می‌کند.

### بازیابی بر اساس نام

اگر به یک جلسه عنوان داده باشید (به Naming جلسه در زیر مراجعه کنید)، می‌توانید آن را بر اساس نام بازیابی کنید:

```
# بازیابی یک جلسه با نامhermes -c "my project"# اگر variant‌های lineage وجود دارند (my project, my project #2, my project #3),# این به طور خودکار آخرین را بازیابی می‌کندhermes -c "my project"   # → resumes "my project #3"
```

### بازیابی جلسه مشخص

```
# بازیابی یک جلسه مشخص بر اساس شناسهhermes --resume 20250305_091523_a1b2c3d4hermes -r 20250305_091523_a1b2c3d4# بازیابی بر اساس عنوانhermes --resume "refactoring auth"# یا با زیر دستور chathermes chat --resume 20250305_091523_a1b2c3d4
```

شناسه‌های جلسه هنگام خروج از جلسه CLI نمایش داده می‌شوند و با `hermes sessions list` قابل پیدا کردن هستند.

`hermes sessions list`

### بازبینی مکالمه هنگام بازیابی

وقتی یک جلسه را بازیابی می‌کنید، Hermes قبل از پرامپت ورودی یک بازبینی فشرده از مکالمه قبلی را در یک پنل استایل‌دار نمایش می‌دهد:

حالت بازیابی یک پنل بازبینی فشرده با نوبت‌های اخیر کاربر و assistant نمایش می‌دهد قبل از بازگرداندن شما به پرامپت زنده.

بازبینی:

- پیام‌های کاربر (طلایی ●) و پاسخ‌های assistant (سبز ◆) را نشان می‌دهد
- پیام‌های طولانی را کوتاه می‌کند (300 کاراکتر برای کاربر، 200 کاراکتر / 3 خط برای assistant)
- فراخوانی‌های ابزار را به یک شمارش با نام ابزارها فشرده می‌کند (مثلاً [3 tool calls: terminal, web_search])
- پیام‌های سیستم، نتایج ابزار و استدلال داخلی را پنهان می‌کند
- در 10 تبادل آخر با یک شاگر "... N earlier messages ..." محدود می‌شود
- از استایل کم‌رنگ برای تمایز از مکالمه فعال استفاده می‌کند

```
[3 tool calls: terminal, web_search]
```

برای غیرفعال کردن بازبینی و حفظ رفتار minimal one-liner، در `~/.hermes/config.yaml` تنظیم کنید:

`~/.hermes/config.yaml`

```
display:  resume_display: minimal   # default: full
```

شناسه‌های جلسه فرمت `YYYYMMDD_HHMMSS_<hex>` را دنبال می‌کنند — نشست‌های CLI/TUI از پسوند hex 6 کاراکتری (مثلاً `20250305_091523_a1b2c3`) و نشست‌های gateway از پسوند 8 کاراکتری (مثلاً `20250305_091523_a1b2c3d4`) استفاده می‌کنند. می‌توانید بر اساس شناسه (کامل یا پیشوند یکتا) یا عنوان بازیابی کنید — هر دو با `-c` و `-r` کار می‌کنند.

## انتقال بین پلتفرم‌ها

از `/handoff <platform>` در یک جلسه CLI استفاده کنید تا مکالمه زنده را به کانال اصلی یک پلتفرم پیام‌رسان منتقل کنید. ایجنت دقیقاً از جایی که CLI متوقف شده ادامه می‌دهد — همان شناسه جلسه، رونوشت کامل آگاه از نقش، فراخوانی‌های ابزار و همه چیز.

`/handoff <platform>`

```
# داخل یک جلسه CLI/handoff telegram
```

چه اتفاقی می‌افتد:

1. CLI تأیید می‌کند که `<platform>` فعال است و یک کانال اصلی تنظیم شده دارد (یک بار `/sethome` را از چت مقصد اجرا کنید تا آن را پیکربندی کنید).
2. CLI جلسه را به حالت pending علامت‌گذاری کرده و gateway را به طور مسدود کننده poll می‌کند. اگر ایجنت در وسط نوبت باشد امتناع می‌کند — منتظر باشید پاسخ فعلی تمام شود.
3. ناظر gateway انتقال را ادعا کرده و از آداپتور مقصد یک رشته جدید می‌خواهد: Telegram — یک topic فروم جدید باز می‌کند (topic‌های DM اگر Bot API 9.4+ فعال باشد، یا topic فروم supergroup). Discord — یک رشته با بایگانی خودکار 1440 دقیقه‌ای زیر کانال متنی اصلی ایجاد می‌کند. Slack — یک پیام seed ارسال کرده و `ts` آن را به عنوان anchor رشته استفاده می‌کند. WhatsApp / Signal / Matrix / SMS — رشته‌های بومی ندارند، مستقیماً به کانال اصلی بازمی‌گردند.
4. Gateway کلید مقصد را دوباره به شناسه جلسه CLI موجود شما bind می‌کند، سپس یک نوبت کاربر مصنوعی ایجاد می‌کند که از ایجنت می‌خواهد تأیید و خلاصه کند. پاسخ در رشته جدید فرود می‌آید.
5. وقتی gateway موفقیت را تأیید می‌کند، CLI یک راهنمای `/resume` چاپ کرده و به طور تمیز خارج می‌شود:

```
↻ Handoff complete. The session is now active on telegram.
  Resume it on this CLI later with: /resume my-session-title
```

6. از آن نقطه، مکالمه روی پلتفرم زندگی می‌کند. در رشته جدید پاسخ دهید — هر کسی که در آن کانال مجاز باشد همان جلسه را به اشتراک می‌گذارد و هر پیام کاربر واقعی بعدی در رشته به طور یکپارچه می‌پیوندد زیرا جلسات رشته بدون `user_id` کلید می‌خورند.

`<platform>`
`/sethome`
`ts`

بازیابی به CLI: وقتی می‌خواهید به دسکتاپ برگردید، فقط `/resume <title>` (یا `hermes -r "<title>"` از shell) اجرا کنید و از جایی که پلتفرم متوقف شده ادامه دهید.

`/resume <title>`
`hermes -r "<title>"`

حالت‌های شکست:

- کانال اصلی پیکربندی نشده → CLI با راهنمای `/sethome` امتناع می‌کند.
- پلتفرم فعال نیست / gateway در حال اجرا نیست → CLI با یک پیام واضح در 60 ثانیه timeout می‌دهد و جلسه CLI شما دست‌نخورده باقی می‌ماند.
- ایجاد رشته شکست می‌خورد (مجوزها، topics-mode خاموش) → مستقیماً به کانال اصلی بازمی‌گردد و هنوز تکمیل می‌شود؛ جداسازی رشته وجود ندارد اما خود انتقال کار می‌کند.
- `adapter.send` شکست می‌خورد (محدودیت rate، خطای گذرا API) → انتقال به عنوان شکست خورده با دلیل علامت‌گذاری می‌شود؛ ردیف پاک می‌شود تا بتوانید دوباره تلاش کنید.

`/sethome`
`adapter.send`

محدودیت ارزش دانستن: برای پلتفرم‌های بدون قابلیت رشته با کانال‌های اصلی گروهی چند کاربره، نوبت مصنوعی به عنوان یک جلسه DM-style کلید می‌خورد. این برای کانال‌های اصلی self-DM (تنظیم رایج) کار می‌کند اما برای چت‌های گروهی واقعاً مشترک ایده‌آل نیست. رشته‌بندی Telegram / Discord / Slack را پوشش می‌دهد — که قطعاً حالت رایج است — بنابراین اکثر تنظیمات هرگز به این مشکل نمی‌خورند.

## نام‌گذاری جلسه

جلسات را با عناوین خوانا نام‌گذاری کنید تا بتوانید به راحتی آنها را پیدا و بازیابی کنید.

### عناوین خودکار تولید شده

Hermes پس از اولین تبادل به طور خودکار یک عنوان توصیفی کوتاه (۳–۷ کلمه) برای هر جلسه تولید می‌کند. این در یک رشته پس‌زمینه با یک مدل کمکی سریع اجرا می‌شود، بنابراین latency اضافه نمی‌کند. عناوین خودکار تولید شده را هنگام مرور جلسات با `hermes sessions list` یا `hermes sessions browse` خواهید دید.

`hermes sessions list`
`hermes sessions browse`

نام‌گذاری خودکار فقط یک بار برای هر جلسه اجرا می‌شود و اگر قبلاً عنوانی را به صورت دستی تنظیم کرده باشید رد می‌شود.

### تنظیم عنوان به صورت دستی

از دستور اسلش `/title` در هر جلسه چت (CLI یا gateway) استفاده کنید:

`/title`

```
/title my research project
```

عنوان فوراً اعمال می‌شود. اگر جلسه هنوز در دیتابیس ایجاد نشده باشد (مثلاً قبل از ارسال اولین پیام `/title` اجرا کنید)، در صف قرار گرفته و وقتی جلسه شروع شد اعمال می‌شود.

همچنین می‌توانید جلسات موجود را از خط فرمان تغییر نام دهید:

```
hermes sessions rename 20250305_091523_a1b2c3d4 "refactoring auth module"
```

### قوانین عنوان

- منحصربفرد — دو جلسه نمی‌توانند عنوان مشترک داشته باشند
- حداکثر 100 کاراکتر — خروجی فهرست را تمیز نگه می‌دارد
- پاکسازی شده — کاراکترهای کنترلی، کاراکترهای عرض صفر و override‌های RTL به طور خودکار حذف می‌شوند
- یونیکد عادی مشکلی ندارد — emoji، CJK، کاراکترهای لهجه‌دار همه کار می‌کنند

### lineage خودکار هنگام فشرده‌سازی

وقتی سیاق یک جلسه فشرده شود (دستی از طریق `/compress` یا خودکار)، Hermes یک جلسه ادامه جدید ایجاد می‌کند. اگر اصلی عنوان داشته باشد، جلسه جدید به طور خودکار یک عنوان شماره‌گذاری شده دریافت می‌کند:

`/compress`

```
"my project" → "my project #2" → "my project #3"
```

وقتی بر اساس نام بازیابی می‌کنید (`hermes -c "my project"`)، به طور خودکار آخرین جلسه در lineage را انتخاب می‌کند.

### `/title` در پلتفرم‌های پیام‌رسان

دستور `/title` در تمام پلتفرم‌های gateway (Telegram، Discord، Slack، WhatsApp) کار می‌کند:

`/title`
- `/title My Research` — تنظیم عنوان جلسه
- `/title` — نمایش عنوان فعلی

## دستورات مدیریت جلسه

Hermes مجموعه کاملی از دستورات مدیریت جلسه را از طریق `hermes sessions` ارائه می‌دهد:

`hermes sessions`

### فهرست جلسات

```
# فهرست جلسات اخیر (پیش‌فرض: 20 مورد اخیر)hermes sessions list# فیلتر بر اساس پلتفرمhermes sessions list --source telegram# نمایش جلسات بیشترhermes sessions list --limit 50
```

وقتی جلسات عنوان دارند، خروجی عناوین، پیش‌نمایش‌ها و برچسب‌های زمانی نسبی را نمایش می‌دهد:

```
Title                  Preview                                  Last Active   ID────────────────────────────────────────────────────────────────────────────────────────────────refactoring auth       Help me refactor the auth module please   2h ago        20250305_091523_amy project #3          Can you check the test failures?          yesterday     20250304_143022_e—                      What's the weather in Las Vegas?          3d ago        20250303_101500_f
```

وقتی هیچ جلسه‌ای عنوان ندارد، فرمت ساده‌تری استفاده می‌شود:

```
Preview                                            Last Active   Src    ID──────────────────────────────────────────────────────────────────────────────────────Help me refactor the auth module please             2h ago        cli    20250305_091523_aWhat's the weather in Las Vegas?                    3d ago        tele   20250303_101500_f
```

### خروجی جلسات

`hermes sessions export` یک سطح برای هر فرمت خروجی است، با `--format` انتخاب شده:

`hermes sessions export`
`--format`

| فرمت | خروجی | استفاده |
| --- | --- | --- |
| jsonl (پیش‌فرض) | یک شیء JSON به ازای هر جلسه | پشتیبان‌گیری، بازگشت ماشینی |
| md/qmd | یک فایل Markdown/Quarto به ازای هر جلسه + manifest | آرشیوهای خوانا، یادداشت‌ها |
| html | یک صفحه خود-contained (sidebar برای جلسات متعدد) | اشتراک‌گذاری، مرور |
| trace | Claude Code JSONL | HF Agent Trace Viewer، `--upload` |

`jsonl`
`md`
`qmd`
`html`
`trace`
`--upload`

به علاوه `--only user-prompts` برای نمای فقط پرامپت‌ها (jsonl یا md).

`--only user-prompts`

تمام فرمت‌ها کنترل‌های انتخاب مشترک را به اشتراک می‌گذارند: `--session-id` برای یک جلسه، یا مجموعه فیلتر کامل `prune`/`archive` برای حجم — `--older-than`/`--newer-than`/`--before`/`--after` (مدت زمان مانند `5h`/`2d`/`1w`، روزهای خام، یا برچسب‌های زمانی ISO)، `--source`، `--title`، `--model`، `--provider`، `--cwd`، `--min`/`--max-messages`، `--min`/`--max-tokens`، `--min`/`--max-cost`، `--min`/`--max-tool-calls`، `--user`، `--chat-id`، `--chat-type`، `--branch`، `--end-reason`. `--dry-run` مجموعه تطابق را بدون نوشتن پیش‌نمایش می‌دهد. `--redact` رمزها (کلیدهای API، توکن‌ها، اعتبارنامه‌ها) را از محتوای خروجی در هر فرمت پاک می‌کند — برای هر چیزی که قصد اشتراک‌گذاری دارید توصیه می‌شود. توجه: فیلترهای حجم جلسات پایان یافته را تطابق می‌دهند؛ `export` بدون فیلتر همه چیز را خالی می‌کند، از جمله فعال‌ها.

`--session-id`
`prune`
`archive`
`--older-than`
`--newer-than`
`--before`
`--after`
`5h`
`2d`
`1w`
`--source`
`--title`
`--model`
`--provider`
`--cwd`
`--min/--max-messages`
`--min/--max-tokens`
`--min/--max-cost`
`--min/--max-tool-calls`
`--user`
`--chat-id`
`--chat-type`
`--branch`
`--end-reason`
`--dry-run`
`--redact`
`export`

#### JSONL (پیش‌فرض)

```
# خروجی تمام جلسات به یک فایل JSONLhermes sessions export backup.jsonl# خروجی جلسات از یک پلتفرم مشخصhermes sessions export telegram-history.jsonl --source telegram# خروجی یک جلسهhermes sessions export session.jsonl --session-id 20250305_091523_a1b2c3d4# پاک کردن کلیدهای API/توکن‌ها/اعتبارنامه‌ها از محتوای خروجیhermes sessions export backup.jsonl --redact
```

فایل‌های خروجی حاوی یک شیء JSON در هر خط با فراداده کامل جلسه و تمام پیام‌ها هستند.

#### HTML

`--format html` یک فایل HTML خود-contained واحد می‌نویسد — بدون dependency‌های دور — با حباب‌های پیام استایل‌دار، خروجی ابزار جمع‌شونده و (برای خروجی جلسات متعدد) یک sidebar برای سوئیچ بین جلسات:

`--format html`

```
# یک جلسه به عنوان یک صفحه HTML مستقلhermes sessions export --format html --session-id 20250305_091523_a1b2c3d4 transcript.html# تمام جلسات Telegram هفته اخیر در یک فایل، رمزها پاک شدهhermes sessions export --format html --newer-than 1w --source telegram --redact archive.html
```

#### فقط پرامپت‌ها

`--only user-prompts` فقط پرامپت‌هایی که نوشتید را خروجی می‌دهد — بدون پاسخ‌های assistant، خروجی ابزار یا سیاق سیستم. مفید برای ساخت کتابخانه پرامپت‌ها یا بازبینی آنچه پرسیدید:

`--only user-prompts`

```
# یک رکورد JSONL به ازای هر پرامپت (شناسه جلسه، ایندکس، برچسب زمانی، متن)hermes sessions export prompts.jsonl --session-id 20250305_091523_a1b2c3d4 --only user-prompts# Markdown، مستقیماً به stdouthermes sessions export - --session-id 20250305_091523_a1b2c3d4 --only user-prompts --format md
```

با `--format jsonl` (پیش‌فرض) یا `md` کار می‌کند، همان فیلترها برای خروجی حجم را رعایت می‌کند و با `--redact` ترکیب می‌شود.

#### Trace (HF Agent Trace Viewer)

`--format trace` Claude Code JSONL تولید می‌کند — شکل رونوشتی که Hugging Face Hub برای Agent Trace Viewer خود شناسایی خودکار می‌کند. آن را محلی بنویسید، یا `--upload` را اضافه کنید تا آن را به dataset خصوصی `hermes-traces` خودتان push کنید ( `HF_TOKEN` را می‌خواند):

`--format trace`
[Agent Trace Viewer](https://huggingface.co/docs/hub/agent-traces)
`--upload`
`hermes-traces`
`HF_TOKEN`

```
# Trace جلسه اخیر، به stdouthermes sessions export --format trace# یک جلسه به یک فایل trace محلیhermes sessions export --format trace --session-id 20250305_091523_a1b2c3d4 trace.jsonl# آپلود مستقیماً به dataset HF traces خصوصیhermes sessions export --format trace --session-id 20250305_091523_a1b2c3d4 --upload
```

خروجی‌های trace به طور پیش‌فرض رمزها را پاک می‌کنند (برای خروج از ماشین در نظر گرفته شده‌اند)؛ `--no-redact` پس از بازبینی دستی غیرفعال می‌کند. `--upload` خصوصی است مگر `--public`. خروجی حجم trace با فیلترها یک `<id>.trace.jsonl` به ازای هر جلسه می‌نویسد.

#### Markdown / QMD

`--format md` یا `--format qmd` را ارسال کنید وقتی می‌خواهید قبل از پنهان کردن یا حذف جلسات قدیمی یک آرشیو خوانا و مبتنی بر فایل داشته باشید. خروجی Markdown/QMD یک فایل به ازای هر جلسه در یک دایرکتوری می‌نویسد (پیش‌فرض: `~/.hermes/session-exports`).

`--format md`
`--format qmd`
`~/.hermes/session-exports`

```
# خروجی یک جلسه به Markdownhermes sessions export --format md --session-id 20250305_091523_a1b2c3d4# خروجی یک lineage فشرده‌سازی به عنوان یک سند منطقیhermes sessions export --format md --session-id 20250305_091523_a1b2c3d4 --lineage logical# پیش‌نمایش جلسات پایان یافته قدیمی‌تر از 90 روز بدون نوشتن فایلhermes sessions export --format md --older-than 90 --dry-run# خروجی جلسات پایان یافته Telegram قدیمی‌تر از 2 هفته به فایل‌های QMDhermes sessions export --format qmd --older-than 2w --source telegram# خروجی جلسات طولانی Claude، رمزها پاک شدهhermes sessions export --format md --model sonnet --min-messages 50 --redact# فقط پس از تأیید، خروجی و حذف یک جلسه با نام مشخصhermes sessions export --format md --session-id 20250305_091523_a1b2c3d4 --delete-after-verified --yes
```

خروجی Markdown/QMD یک فایل `.md` یا `.qmd` به ازای هر جلسه خروجی شده به علاوه یک `manifest.jsonl` با مسیر فایل، شمارش پیام، شناسه‌های lineage و SHA-256 می‌نویسد. خروجی حجم حداقل یک فیلتر می‌خواهد؛ یک خروجی حجم خام رد می‌شود. `--delete-after-verified` عمداً فقط به `--session-id` محدود شده و `--yes` نیاز دارد. `--redact` رمزها (کلیدهای API، توکن‌ها، اعتبارنامه‌ها) را از محتوای پیام و خروجی ابزار قبل از نوشتن پاک می‌کند — برای هر خروجی که قصد اشتراک‌گذاری دارید توصیه می‌شود.

### حذف جلسه

```
# حذف یک جلسه مشخص (با تأیید)hermes sessions delete 20250305_091523_a1b2c3d4# حذف بدون تأییدhermes sessions delete 20250305_091523_a1b2c3d4 --yes
```

### تغییر نام جلسه

```
# تنظیم یا تغییر عنوان جلسهhermes sessions rename 20250305_091523_a1b2c3d4 "debugging auth flow"# عناوین چند کلمه‌ای در CLI نیازی به نقل قول ندارندhermes sessions rename 20250305_091523_a1b2c3d4 debugging auth flow
```

اگر عنوان قبلاً توسط جلسه دیگری استفاده شده باشد، یک خطا نمایش داده می‌شود.

### حذف جلسات قدیمی

```
# حذف جلسات پایان یافته قدیمی‌تر از 90 روز (پیش‌فرض)hermes sessions prune# آستانه سن سفارشی — اعداد خام روزها هستندهermes sessions prune --older-than 30# مدت زمان هم کار می‌کند: 5h, 30m, 2d, 1whermes sessions prune --older-than 12h# حذف فقط یک بازه زمانی مشخص (مثلاً مجموعه‌ای از جلسات تست# ایجاد شده در 5 ساعت اخیر)hermes sessions prune --newer-than 5h# بازه صریح با برچسب‌های زمانی مطلقhermes sessions prune --after "2026-07-05 09:00" --before "2026-07-05 14:30"# فقط حذف جلسات از یک پلتفرم مشخص (همه سن‌ها — هر فیلتر# پیش‌فرض ضمنی 90 روز را غیرفعال می‌کند)hermes sessions prune --source telegramhermes sessions prune --source cron --older-than 60   # افزودن پرچم زمانی برای محدود کردن# فیلترهای بیشتر — همه AND با همhermes sessions prune --newer-than 5h --title "smoke test"   # زیررشته عنوانhermes sessions prune --older-than 30 --max-messages 3        # جلسات کوچکhermes sessions prune --cwd ~/scratch --end-reason done       # بر اساس cwd / دلیل پایانhermes sessions prune --model gpt-5 --older-than 1w           # بر اساس مدل (زیررشته)hermes sessions prune --provider openrouter --older-than 60   # بر اساس ارائه‌دهنده صورتحسابhermes sessions prune --branch feature/old-experiment         # بر اساس شاخه githermes sessions prune --user 12345678 --chat-type group       # بر اساس منبع پیام‌رسانhermes sessions prune --max-tokens 500 --older-than 7         # بر اساس استفاده توکنhermes sessions prune --max-cost 0.01 --max-tool-calls 0      # ارزان، بدون ابزار# پیش‌نمایش آنچه حذف می‌شد، بدون حذف هیچ چیزیhermes sessions prune --newer-than 5h --dry-run# رد کردن تأییدhermes sessions prune --older-than 30 --yes
```

مقادیر زمانی (`--older-than`، `--newer-than`، `--before`، `--after`) یک مدت زمان (`5h`، `30m`، `2d`، `1w`)، یک عدد خام روزها، یا یک برچسب زمانی ISO (`2026-07-05`، `2026-07-05 14:30`) می‌پذیرند. `--older-than` / `--before` مرز بالایی را تنظیم می‌کنند؛ `--newer-than` / `--after` مرز پایینی. هر دو را برای یک بازه ترکیب کنید.

فیلترهای ویژگی: `--source` (پلتفرم، دقیق)، `--title` / `--model` / `--branch` (زیررشته بدون حساسیت به حالت)، `--provider` (ارائه‌دهنده صورتحساب، دقیق)، `--end-reason`، `--user`، `--chat-id`، `--chat-type` (دقیق)، `--cwd` (پیشوند مسیر)، به علاوه محدودیت‌های عددی `--min`/`--max-messages`، `--min`/`--max-tokens` (ورودی+خروجی)، `--min`/`--max-cost` (USD، واقعی با fallback به تخمینی)، و `--min`/`--max-tool-calls`. استفاده از هر فیلتری پیش‌فرض ضمنی 90 روز را غیرفعال می‌کند، بنابراین `hermes sessions prune --source cron` یا `--model gpt-4o` همه سن‌ها را تطابق می‌دهد — یک پرچم زمانی اضافه کنید تا محدود شود. فقط `hermes sessions prune` کاملاً خام برش 90 روزه را حفظ می‌کند. هر اجرا غیر `--yes` شمارش تطابق به علاوه قدیمی‌ترین و جدیدترین جلسه تطابق را قبل از درخواست تأیید نمایش می‌دهد.

جلسات بایگانی شده به طور پیش‌فرض رد می‌شوند؛ `--include-archived` را ارسال کنید تا آنها را هم حذف کنید.

حذف فقط جلسات پایان یافته (جلساتی که به طور صریح پایان یافته یا بازنشانی خودکار شده‌اند) را حذف می‌کند. جلسات فعال هرگز حذف نمی‌شوند.

### بایگانی حجمی جلسات

اگر می‌خواهید جلسات از فهرست‌های شما خارج شوند بدون حذف هیچ چیزی، `hermes sessions archive` همان فیلترها را به عنوان `prune` می‌پذیرد اما جلسات تطابق را به جای آن soft-hide می‌کند (همان پرچم بایگانی شده را تنظیم می‌کند که بایگانی یک جلسه از UI Desktop/Dashboard — پیام‌ها و جستجو دست‌نخورده باقی می‌مانند):

`hermes sessions archive`
`prune`

```
# بایگانی همه چیز از 5 ساعت اخیر (مثلاً 75 جلسه smoke-test CI)hermes sessions archive --newer-than 5h# بایگانی بر اساس زیررشته عنوان، ابتدا پیش‌نمایشhermes sessions archive --title "dry run" --dry-runhermes sessions archive --title "dry run" --yes
```

حداقل یک فیلتر لازم است — `hermes sessions archive` خام کل تاریخچه شما را بایگانی نمی‌کند. جلسات بایگانی شده از `hermes sessions list` و `/resume` پنهان می‌شوند اما در دیتابیس باقی می‌مانند و از فهرست جلسات Desktop/Dashboard قابل بازیابی هستند.

### آمار جلسات

```
hermes sessions stats
```

خروجی:

```
Total sessions: 142Total messages: 3847  cli: 89 sessions  telegram: 38 sessions  discord: 15 sessionsDatabase size: 12.4 MB
```

برای تحلیل عمیق‌تر — استفاده توکن، تخمین هزینه، تفکیک ابزار و الگوهای فعالیت — از `hermes insights` استفاده کنید.

[hermes insights](/docs/reference/cli-commands#hermes-insights)
`hermes insights`

## ابزار جستجوی جلسه

ایجنت یک ابزار داخلی `session_search` دارد که full-text search در تمام مکالمات گذشته با استفاده از موتور FTS5 SQLite انجام می‌دهد — و به ایجنت اجازه می‌دهد در هر جلسه‌ای که پیدا می‌کند scroll کند. بدون فراخوانی‌های LLM، بدون خلاصه‌سازی، بدون کوتاه‌سازی. هر شکل پیام‌های واقعی از دیتابیس را برمی‌گرداند.

### سه شکل فراخوانی

ابزار از اینکه کدام آرگومان‌ها را تنظیم می‌کنید می‌فهمد چه می‌خواهید. پارامتر `mode` وجود ندارد.

1. کشف — `query` را ارسال کنید:

```
session_search(query="auth refactor", limit=3)
```

FTS5 را اجرا می‌کند، ضربه‌ها را بر اساس lineage جلسه dedupe می‌کند، N جلسه برتر را برمی‌گرداند. هر نتیجه شامل موارد زیر است:

- `session_id`، `title`، `when`، `source`
- `snippet` — قطعه تطابق با هایلایت FTS5
- `bookend_start` — اولین ۳ پیام کاربر+assistant جلسه (هدف/شروع)
- `messages` — ±۵ پیام اطراف تطابق FTS5، با پیام anchor علامت‌گذاری شده (تطابق در سیاق)
- `bookend_end` — آخرین ۳ پیام کاربر+assistant جلسه (حل/تصمیمات)
- `match_message_id`، `messages_before`، `messages_after`

bookend‌ها + پنجره با هم هدف → تطابق → حل را بدون پرداخت هزینه کل رونوشت بازسازی می‌کنند. زمان دیواری معمول: 15–50ms در یک دیتابیس جلسه واقعی.

2. scroll — `session_id` + `around_message_id` را ارسال کنید:

```
session_search(session_id="20260510_174648_805cc2", around_message_id=590803, window=10)
```

یک پنجره از ±`window` پیام مرکز شده روی anchor برمی‌گرداند. بدون FTS5، بدون bookend — فقط برش. بعد از فراخوانی کشف وقتی به سیاق بیشتری از پنجره پیش‌فرض ±۵ نیاز دارید استفاده کنید.

- برای scroll رو به جلو: `messages[-1].id` را به عنوان `around_message_id` پاس دهید
- برای scroll رو به عقب: `messages[0].id` را به عنوان `around_message_id` پاس دهید
- پیام مرزی در هر دو پنجره به عنوان شاگر جهت‌گیری ظاهر می‌شود
- وقتی `messages_before` یا `messages_after` کمتر از `window` باشد، در ابتدای یا انتهای جلسه هستید

زمان دیواری معمول: 1–2ms به ازای هر فراخوانی scroll.

3. مرور — بدون آرگومان:

```
session_search()
```

جلسات اخیر را به ترتیب زمانی برمی‌گرداند (عناوین، پیش‌نمایش‌ها، برچسب‌های زمانی). مفید وقتی کاربر می‌پرسد "مشغول چه کاری بودم" بدون نام بردن از یک موضوع.

### سntax پرس و جو FTS5

حالت کلمه کلیدی از سntax پرس و جو استاندارد FTS5 پشتیبانی می‌کند:

- کلمات کلیدی ساده: `docker deployment` (FTS5 به طور پیش‌فرض AND است)
- عبارات: `"exact phrase"`
- بولی: `docker OR kubernetes`، `python NOT java`
- پیشوند: `deploy*`

### پارامترهای اختیاری

- `sort` — `newest` یا `oldest`، علاوه بر رتبه‌بندی FTS5. برای مرتب‌سازی فقط بر اساس ارتباط (پیش‌فرض؛ مناسب برای یادآوری اکتشافی) حذف کنید. از `newest` برای سؤالات "X را کجا ترک کردیم" و `oldest` برای سؤالات "X چگونه شروع شد" استفاده کنید.
- `role_filter` — نقش‌های جدا شده با کاما. کشف به طور پیش‌فرض `user,assistant` (خروجی ابزار معمولاً نویز است). `user,assistant,tool` برای شامل کردن خروجی ابزار (ابزار debugging) یا `tool` برای فقط جستجوی خروجی ابزار ارسال کنید.

## ردیابی جلسه به ازای هر پلتفرم

### جلسات Gateway

در پلتفرم‌های پیام‌رسان، جلسات با یک کلید جلسه قطعی که از منبع پیام ساخته شده کلید می‌خورند:

| نوع چت | فرمت کلید پیش‌فرض | رفتار |
| --- | --- | --- |
| Telegram DM | `agent:main:telegram:dm:<chat_id>` | یک جلسه به ازای هر چت DM |
| Discord DM | `agent:main:discord:dm:<chat_id>` | یک جلسه به ازای هر چت DM |
| WhatsApp DM | `agent:main:whatsapp:dm:<canonical_identifier>` | یک جلسه به ازای هر کاربر DM ( псевдо‌نام‌های LID/تلفن به یک هویت فرو می‌ریزند وقتی نگاشت وجود دارد) |
| چت گروهی | `agent:main:<platform>:group:<chat_id>:<user_id>` | به ازای هر کاربر داخل گروه وقتی پلتفرم شناسه کاربر نمایان می‌کند |
| رشته/topic گروهی | `agent:main:<platform>:group:<chat_id>:<thread_id>` | جلسه مشترک برای تمام شرکت‌کنندگان رشته (پیش‌فرض). به ازای هر کاربر با `thread_sessions_per_user: true`. |
| کانال | `agent:main:<platform>:channel:<chat_id>:<user_id>` | به ازای هر کاربر داخل کانال وقتی پلتفرم شناسه کاربر نمایان می‌کند |

وقتی Hermes نمی‌تواند شناسه شرکت‌کننده‌ای برای چت مشترک پیدا کند، به یک جلسه مشترک برای آن اتاق بازمی‌گردد.

### جلسات گروهی مشترک در مقابل ایزوله

به طور پیش‌فرض، Hermes از `group_sessions_per_user: true` در `config.yaml` استفاده می‌کند. این بدان معناست:

`group_sessions_per_user: true`
`config.yaml`
- Alice و Bob هر دو می‌توانند در همان کانال Discord با Hermes صحبت کنند بدون به اشتراک گذاشتن تاریخچه رونوشت
- کار یک کاربر طولانی و ابزار-سنگین پنجره سیاق کاربر دیگر را آلوده نمی‌کند
- مدیریت وقفه هم به ازای هر کاربر باقی می‌ماند زیرا کلید ایجنت در حال اجرا با کلید جلسه ایزوله مطابقت دارد

اگر می‌خواهید به جای آن یک "mroom مشترک" داشته باشید، تنظیم کنید:

```
group_sessions_per_user: false
```

این گروه‌ها/کانال‌ها را به یک جلسه مشترک واحد به ازای هر اتاق برمی‌گرداند، که سیاق مکالمه مشترک را حفظ می‌کند اما هزینه‌های توکن، وضعیت وقفه و رشد سیاق را هم به اشتراک می‌گذارد.

### سیاست‌های بازنشانی جلسه

به طور پیش‌فرض جلسات gateway هرگز بازنشانی خودکار نمی‌دهند (`mode: none`). می‌توانید بازنشانی‌های خودکار را از طریق بخش `session_reset` در `config.yaml` فعال کنید:

`mode: none`
`session_reset`
`config.yaml`
- `none` — هرگز بازنشانی خودکار نکن (پیش‌فرض؛ سیاق توسط `/reset` و فشرده‌سازی مدیریت می‌شود)
- `idle` — پس از N دقیقه عدم فعالیت بازنشانی کن
- `daily` — در ساعت مشخصی هر روز بازنشانی کن
- `both` — در هر کدام که اول برسد بازنشانی کن (idle یا daily)

قبل از بازنشانی خودکار جلسه، به ایجنت یک نوبت داده می‌شود تا هر حافظه یا مهارت مهمی از مکالمه را ذخیره کند.

جلسات با فرآیندهای پس‌زمینه فعال هرگز بازنشانی خودکار نمی‌شوند، صرف نظر از سیاست.

## مکان‌های فروشگاه‌سازی

| چه چیزی | مسیر | توضیحات |
| --- | --- | --- |
| دیتابیس SQLite | `~/.hermes/state.db` | تمام فراداده جلسه + پیام‌ها با FTS5 |
| پیام‌های Gateway | `~/.hermes/state.db` | SQLite — فروشگاه اصلی برای تمام پیام‌های جلسه |
| ایندکس مسیریابی Gateway | `~/.hermes/sessions/sessions.json` | کلیدهای جلسه را به شناسه‌های جلسه فعال نگاشت می‌کند (فراداده منبع، پرچم‌های انقضا) |

دیتابیس SQLite از حالت WAL برای خوانندگان همزمان و یک نویسنده واحد استفاده می‌کند، که معماری چند پلتفرمی gateway را به خوبی تطبیق می‌دهد.

`~/.hermes/sessions/sessions.json` ایندکس مسیریابی gateway است — کلیدهای جلسه پیام‌رسان (`agent:main:<platform>:...`) را به شناسه‌های جلسه فعال نگاشت می‌کند. فقط حاوی ورودی‌های gateway/پیام‌رسان است، بنابراین اگر یک پلتفرم پیام‌رسان اجرا کنید فقط آنها را خواهید دید (مثلاً `agent:main:whatsapp:dm:...`).

`agent:main:<platform>:...`
`agent:main:whatsapp:dm:...`

این **عادی** است و **به این معنا نیست** که جلسات CLI شما ناپدید شده‌اند. `hermes sessions list`، `/sessions` و داشبورد همه `state.db` را می‌خوانند، که **هر** جلسه‌ای (CLI، TUI و gateway) را نگه می‌دارد. اسنپشات‌های `/save` در `~/.hermes/sessions/saved/*.json` خروجی‌های راحت هستند، نه ایندکس.

`hermes sessions list`
`sessions`
`state.db`
`/save`
`~/.hermes/sessions/saved/*.json`

اگر جلسات CLI واقعاً در `hermes sessions list` ظاهر نمی‌شوند، علت `state.db` است که آنها را دریافت نمی‌کند — `hermes sessions repair` را اجرا کنید و به دنبال هشدار `⚠ Session store unavailable` در شروع CLI بگردید، که به این معناست ماندگاری SQLite برای آن اجرا شکست خورده.

`hermes sessions list`
`state.db`
`hermes sessions repair`
`⚠ Session store unavailable`

جلسات ایجاد شده قبل از canonical شدن state.db ممکن است فایل‌های `*.jsonl` باقی‌مانده در `~/.hermes/sessions/` داشته باشند. آنها دیگر توسط Hermes نه نوشته و نه خوانده می‌شوند. پس از تأیید وجود جلسه مربوطه در state.db، حذف آنها بی‌خطر است.

### طرح دیتابیس

جداول کلیدی در `state.db`:

- `sessions` — فراداده جلسه (id, source, user_id, model, title, timestamps, token counts). عناوین ایندکس یکتا دارند (عناوین NULL مجاز هستند، فقط غیر-NULL باید یکتا باشند).
- `messages` — تاریخچه کامل پیام (role, content, tool_calls, tool_name, token_count)
- `messages_fts` — جدول مجازی FTS5 برای full-text search در محتوای پیام

## انقضای جلسه و پاکسازی

### پاکسازی خودکار

- جلسات gateway بر اساس سیاست بازنشانی پیکربندی شده بازنشانی خودکار می‌شوند
- قبل از بازنشانی، ایجنت حافظه‌ها و مهارت‌های جلسه منقضی شده را ذخیره می‌کند
- حذف خودکار اختیاری: وقتی `sessions.auto_prune` برابر `true` باشد، جلسات پایان یافته قدیمی‌تر از `sessions.retention_days` (پیش‌فرض 90) در شروع CLI/gateway حذف می‌شوند
- پس از حذفی که واقعاً ردیف‌ها را حذف کرده، `state.db` VACUUM می‌شود تا فضای دیسک بازیابی شود (SQLite با DELETE معمولی فایل را کوچک نمی‌کند)
- حذف حداکثر یک بار در هر `sessions.min_interval_hours` (پیش‌فرض 24) اجرا می‌شود؛ برچسب زمانی اجرای آخر در داخل خود `state.db` ردیابی می‌شود بنابراین در سراسر هر فرآیند Hermes در همان `HERMES_HOME` مشترک است

`sessions.auto_prune`
`true`
`sessions.retention_days`
`state.db`
`VACUUM`
`sessions.min_interval_hours`
`state.db`
`HERMES_HOME`

پیش‌فرض `off` است — تاریخچه جلسه برای یادآوری `session_search` ارزشمند است و حذف خاموش آن می‌تواند کاربران را شگفت‌زده کند. در `~/.hermes/config.yaml` فعال کنید:

`session_search`
`~/.hermes/config.yaml`

```
sessions:  auto_prune: true          # opt in — default is false  retention_days: 90        # keep ended sessions this many days  vacuum_after_prune: true  # reclaim disk space after a pruning sweep  min_interval_hours: 24    # don't re-run the sweep more often than this
```

جلسات فعال هرگز حذف خودکار نمی‌شوند، صرف نظر از سن.

### پاکسازی دستی

```
# حذف جلسات قدیمی‌تر از 90 روزhermes sessions prune# حذف یک جلسه مشخصhermes sessions delete <session_id># خروجی قبل از حذف (پشتیبان)hermes sessions export backup.jsonlhermes sessions prune --older-than 30 --yes
```

دیتابیس به آهستگی رشد می‌کند (معمول: 10-15 MB برای صدها جلسه) و تاریخچه جلسه یادآوری `session_search` در سراسر مکالمات گذشته را تقویت می‌کند، بنابراین حذف خودکار به طور پیش‌فرض غیرفعال است. اگر یک workload سنگین gateway/cron اجرا می‌کنید که `state.db` به طور معناداری بر عملکرد تأثیر می‌گذارد آن را فعال کنید (حالت شکست مشاهده شده: state.db با ~1000 جلسه 3848 MB که درج FTS5 و لیست `/resume` را کند می‌کند). از `hermes sessions prune` برای پاکسازی یک‌باره بدون فعال کردن جاروب خودکار استفاده کنید.

[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/sessions.md)
