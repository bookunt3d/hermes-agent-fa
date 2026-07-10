---
layout: docs
title: "پیام‌رسانی"
permalink: /docs/user-guide/messaging/
---

- 
- پلتفرم‌های پیام‌رسانی
- Gateway پیام‌رسانی

# Gateway پیام‌رسانی

با Hermes از Telegram، Discord، Slack، WhatsApp، Signal، SMS، Email، Home Assistant، Mattermost، Matrix، DingTalk، Feishu/Lark، WeCom، Weixin، BlueBubbles (iMessage)، QQ، Yuanbao، Microsoft Teams، LINE، ntfy یا مرورگر خود چت کنید. Gateway یک فرآیند پس‌زمینه واحد است که به همه پلتفرم‌های پیکربندی‌شده شما متصل می‌شود، sessionها را مدیریت می‌کند، cron jobها را اجرا می‌کند و پیام‌های صوتی را تحویل می‌دهد.

برای مجموعه کامل ویژگی‌های صوتی — شامل حالت میکروفن CLI، پاسخ‌های گفتاری در پیام‌رسانی و مکالمات صوتی Discord — [حالت صوتی](/docs/user-guide/features/voice-mode) و [استفاده از حالت صوتی با Hermes](/docs/guides/use-voice-mode-with-hermes) را ببینید.

[حالت صوتی](/docs/user-guide/features/voice-mode)
[استفاده از حالت صوتی با Hermes](/docs/guides/use-voice-mode-with-hermes)

بات‌ها به یک provider مدل و providerهای ابزار (TTS، وب) نیاز دارند. اشتراک [Nous Portal](/docs/integrations/nous-portal) همه آن‌ها را بسته‌بندی می‌کند.

[Nous Portal](/docs/integrations/nous-portal)

## مقایسه پلتفرم‌ها​

| پلتفرم | صوتی | تصاویر | فایل‌ها | threads | واکنش‌ها | تایپ کردن | streaming |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Telegram | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| Discord | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Slack | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Google Chat | — | ✅ | ✅ | ✅ | — | ✅ | — |
| WhatsApp | — | ✅ | ✅ | — | — | ✅ | ✅ |
| Signal | — | ✅ | ✅ | — | — | ✅ | ✅ |
| SMS | — | — | — | — | — | — | — |
| Email | — | ✅ | ✅ | ✅ | — | — | — |
| Home Assistant | — | — | — | — | — | — | — |
| Mattermost | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| Matrix | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DingTalk | — | ✅ | ✅ | — | ✅ | — | ✅ |
| Feishu/Lark | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| WeCom | ✅ | ✅ | ✅ | — | — | — | — |
| WeCom Callback | — | — | — | — | — | — | — |
| Weixin | ✅ | ✅ | ✅ | — | — | ✅ | ✅ |
| BlueBubbles | — | ✅ | ✅ | — | ✅ | ✅ | — |
| QQ | ✅ | ✅ | ✅ | — | — | ✅ | — |
| Yuanbao | ✅ | ✅ | ✅ | — | — | ✅ | ✅ |
| Microsoft Teams | — | ✅ | — | ✅ | — | ✅ | — |
| LINE | — | ✅ | ✅ | — | — | ✅ | — |
| ntfy | — | — | — | — | — | — | — |
| Raft | — | — | — | — | — | — | — |
| IRC | — | — | — | — | — | — | — |

**صوتی** = پاسخ‌های صوتی TTS و/یا رونویسی پیام صوتی. **تصاویر** = ارسال/دریافت تصاویر. **فایل‌ها** = ارسال/دریافت پیوست‌های فایل. **Threads** = مکالمات thread‌شده. **واکنش‌ها** = واکنش‌های emoji روی پیام‌ها. **تایپ کردن** = نشانگر تایپ هنگام پردازش. **Streaming** = به‌روزرسانی تدریجی پیام از طریق ویرایش.

## معماری​

هر adapter پلتفرم پیام‌ها را دریافت می‌کند، آن‌ها را از طریق یک فروشگاه session به ازای هر چت مسیریابی می‌کند و آن‌ها را به AI Agent برای پردازش ارسال می‌کند. Gateway همچنین زمان‌بند Cron را اجرا می‌کند، هر ۶۰ ثانیه tick می‌زند تا هر job سررسیدشده اجرا شود.

## توکن‌های سکوت عمدی​

برای چت‌های گروهی، hookها و جریان‌های اتوماسیون، Hermes از توکن‌های سکوت صریح پشتیبانی می‌کند. اگر پاسخ نهایی agent دقیقاً یک توکن پشتیبانی‌شده باشد، gateway ارسال outbound را سرکوب می‌کند و چیزی به چت ارسال نمی‌کند.

توکن‌های پشتیبانی‌شده:

- `[SILENT]`
- `SILENT`
- `NO_REPLY`
- `NO REPLY`

`[SILENT]`
`SILENT`
`NO_REPLY`
`NO REPLY`

فضای خالی و حروف بزرگ/کوچک نرمال‌سازی می‌شوند، اما کل پاسخ نهایی باید توکن باشد. جمله‌ای مانند "Use `[SILENT]` when nothing changed" به طور عادی تحویل داده می‌شود.

`[SILENT]`

سکوت فقط یک تصمیم تحویل است. Hermes نوبت سکوت assistant را در رونوشت session نگه می‌دارد، بنابراین مکالمه همچنان به طور عادی متناوب می‌شود:

```
user: side-channel chatterassistant: [SILENT]   # stored, not delivereduser: next message
```

نوبت‌های ناموفق همچنان به عنوان خطا ظاهر می‌شوند؛ Hermes فقط به این دلیل که متن شبیه توکن سکوت است شکست‌ها را پنهان نمی‌کند.

## تنظیم سریع​

ساده‌ترین راه پیکربندی پلتفرم‌های پیام‌رسانی جادوگر تعاملی است:

```
hermes gateway setup        # Interactive setup for all messaging platforms
```

شما را از پیکربندی هر پلتفرم با انتخاب کلیدهای جهت‌نما راهنمایی می‌کند، نشان می‌دهد کدام پلتفرم‌ها از قبل پیکربندی شده‌اند و پیشنهاد شروع/بازنشانی gateway را پس از اتمام می‌دهد.

## دستورات Gateway​

```
hermes gateway              # Run in foregroundhermes gateway setup        # Configure messaging platforms interactivelyhermes gateway install      # Install as a user service (Linux) / launchd service (macOS)sudo hermes gateway install --system   # Linux only: install a boot-time system servicehermes gateway start        # Start the default servicehermes gateway stop         # Stop the default servicehermes gateway status       # Check default service statushermes gateway status --system         # Linux only: inspect the system service explicitly
```

## دستورات چت (داخل پیام‌رسانی)​

| دستور | توضیح |
| --- | --- |
| `/new` یا `/reset` | شروع یک مکالمه جدید |
| `/model [provider:model]` | نمایش یا تغییر مدل (از نحوه `provider:model` پشتیبانی می‌کند) |
| `/personality [name]` | تنظیم یک شخصیت |
| `/retry` | تلاش مجدد پیام آخر |
| `/undo` | حذف آخرین مبادله |
| `/status` | نمایش اطلاعات session |
| `/whoami` | نمایش دسترسی دستور اسلش شما در این scope (admin / user / unrestricted) |
| `/stop` | توقف agent در حال اجرا |
| `/approve` | تأیید فرمان خطرناک در انتظار |
| `/deny` | رد فرمان خطرناک در انتظار |
| `/sethome` | تنظیم این چت به عنوان کانال اصلی |
| `/compress` | فشرده‌سازی دستی context مکالمه |
| `/title [name]` | تنظیم یا نمایش عنوان session |
| `/resume [name]` | ادامه یک session قبلی نام‌گذاری شده |
| `/usage` | نمایش مصرف token برای این session |
| `/insights [days]` | نمایش بینش‌ها و تحلیل‌های استفاده |
| `/reasoning [level\|show\|hide]` | تغییر تلاش reasoning یا toggle نمایش reasoning |
| `/voice [on\|off\|tts\|join\|leave\|status]` | کنترل پاسخ‌های صوتی پیام‌رسانی و رفتار کانال صوتی Discord |
| `/rollback [number]` | لیست یا بازیابی checkpointهای فایل‌سیستم |
| `/background <prompt>` | اجرای یک prompt در یک session پس‌زمینه جداگانه |
| `/reload-mcp` | بارگذاری مجدد سرورهای MCP از پیکربندی |
| `/update` | به‌روزرسانی Hermes Agent به آخرین نسخه |
| `/help` | نمایش دستورات موجود |
| `/<skill-name>` | فراخوانی هر skill نصب‌شده |

`/new`
`/reset`
`/model [provider:model]`
`provider:model`
`/personality [name]`
`/retry`
`/undo`
`/status`
`/whoami`
`/stop`
`/approve`
`/deny`
`/sethome`
`/compress`
`/title [name]`
`/resume [name]`
`/usage`
`/insights [days]`
`/reasoning [level|show|hide]`
`/voice [on|off|tts|join|leave|status]`
`/rollback [number]`
`/background <prompt>`
`/reload-mcp`
`/update`
`/help`
`/<skill-name>`

## مدیریت Session​

### پایداری Session​

Sessionها تا زمانی که بازنشانی شوند در پیام‌ها پایدار می‌مانند. Agent context مکالمه شما را به یاد می‌آورد.

### سیاست‌های بازنشانی​

به طور پیش‌فرض sessionها **هرگز** به طور خودکار بازنشانی نمی‌شوند — context تا زمانی که دستی `/reset` کنید یا فشرده‌سازی context فعال شود زنده می‌ماند. اگر بازنشانی خودکار می‌خواهید، با بخش `session_reset` در `~/.hermes/config.yaml` opt-in کنید:

`/reset`
`session_reset`
`~/.hermes/config.yaml`

```
session_reset:  mode: idle        # "idle", "daily", "both", or "none" (default)  idle_minutes: 1440  # for idle/both: minutes of inactivity before reset  at_hour: 4          # for daily/both: hour of day (0-23, local time)
```

| حالت | توضیح |
| --- | --- |
| `none` | هرگز بازنشانی خودکار (پیش‌فرض) |
| `daily` | بازنشانی در ساعت مشخص هر روز |
| `idle` | بازنشانی پس از N دقیقه عدم فعالیت |
| `both` | هر کدام زودتر فعال شود |

یک فرآیند پس‌زمینه زنده (شروع شده با `terminal(background=true`) معمولاً
session خود را از بازنشانی محافظت می‌کند تا خروجی از دست نرود. برای جلوگیری از اینکه
یک فرآیند فراموش‌شده — مثلاً یک سرور پیش‌نمایش — session را برای همیشه باز نگه دارد، یک
فرآیند پس‌زمینه قدیمی‌تر از `bg_process_max_age_hours` (پیش‌فرض `24`) دیگر
بازنشانی را مسدود نمی‌کند. فرآیند کشته **نمی‌شود**، فقط توسط محافظ بازنشانی
نادیده گرفته می‌شود. آن را روی `0` تنظیم کنید تا قطع را غیرفعال کنید (هر فرآیند زنده بازنشانی را مسدود می‌کند، رفتار
قدیمی)، یا آن را اگر jobهای چندروزه قانونی اجرا می‌کنید که زنده بودن آن‌ها باید مکالمه را باز نگه دارد افزایش دهید.

`terminal(background=true)`
`bg_process_max_age_hours`
`0`

پیکربندی override به ازای هر پلتفرم در `~/.hermes/gateway.json`:

`~/.hermes/gateway.json`

```
{  "reset_by_platform": {    "telegram": { "mode": "idle", "idle_minutes": 240 },    "discord": { "mode": "idle", "idle_minutes": 60 }  }}
```

## امنیت​

به طور پیش‌فرض، gateway همه کاربرانی که در allowlist نیستند یا از طریق DM جفت نشده‌اند را رد می‌کند. **این پیش‌فرض امن برای باتی با دسترسی ترمinal است.**

```
# Restrict to specific users (recommended):TELEGRAM_ALLOWED_USERS=123456789,987654321DISCORD_ALLOWED_USERS=123456789012345678SIGNAL_ALLOWED_USERS=+155****4567,+155****6543SMS_ALLOWED_USERS=+155****4567,+155****6543EMAIL_ALLOWED_USERS=trusted@example.com,colleague@work.comMATTERMOST_ALLOWED_USERS=3uo8dkh1p7g1mfk49ear5fzs5cMATRIX_ALLOWED_USERS=@alice:matrix.orgDINGTALK_ALLOWED_USERS=user-id-1FEISHU_ALLOWED_USERS=ou_xxxxxxxx,ou_yyyyyyyyWECOM_ALLOWED_USERS=user-id-1,user-id-2WECOM_CALLBACK_ALLOWED_USERS=user-id-1,user-id-2TEAMS_ALLOWED_USERS=aad-object-id-1,aad-object-id-2# Or allowGATEWAY_ALLOWED_USERS=123456789,987654321# Or explicitly allow all users (NOT recommended for bots with terminal access):GATEWAY_ALLOW_ALL_USERS=true
```

### جفت‌سازی DM (جایگزین Allowlistها)​

به جای پیکربندی دستی شناسه‌های کاربر، کاربران ناشناس یک کد جفت‌سازی یک‌باره هنگام DM به بات دریافت می‌کنند. Email استثناست: فرستندگان email ناشناس نادیده گرفته می‌شوند مگر اینکه جفت‌سازی email صریحاً فعال باشد.

```
# The user sees: "Pairing code: XKGH5N7P"# You approve them with:hermes pairing approve telegram XKGH5N7P# Other pairing commands:hermes pairing list          # View pending + approved usershermes pairing revoke telegram 123456789  # Remove access
```

کدهای جفت‌سازی پس از ۱ ساعت منقضی می‌شوند، rate-limited هستند و از تصادفی بودن رمزنگاری استفاده می‌کنند.

### Adminها در مقابل کاربران عادی​

Allowlistها به این پاسخ می‌دهند "آیا این شخص اصلاً می‌تواند به بات دسترسی پیدا کند؟" تقسیم **admin / user** به این پاسخ می‌دهد "حالا که وارد شد، چه کاری اجازه انجام دارد؟"

هر کاربر مجاز به یکی از دو سطح در هر scope (DM در مقابل گروه/کانال) تعلق دارد:

- **Admin** — دسترسی کامل. می‌تواند هر دستور اسلش ثبت‌شده (داخلی + plugin) را اجرا کند و از هر قابلیت gated استفاده کند.
- **کاربر عادی** — دسترسی محدود. می‌تواند به طور عادی با agent چت کند، اما فقط می‌تواند دستورات اسلشی را اجرا کند که شما صریحاً فعال کرده‌اید. سطح مجاز همیشگی `/help` و `/whoami` است.

`/help`
`/whoami`

سطوح به ازای هر پلتفرم و هر scope پیکربندی می‌شوند. وضعیت admin DM به معنای وضعیت admin گروه/کانال نیست — هر scope لیست admin خاص خود را دارد.

**چه چیزی امروز سطوح را کنترل می‌کند:** دستورات اسلش. تقسیم از رجیستری زنده دستورات عبور می‌کند، بنابراین دستورات داخلی و ثبت‌شده توسط plugin را بدون سیم‌کشی به ازای هر ویژگی پوشش می‌دهد. چت معمولی تحت تأثیر قرار نمی‌گیرد — non-adminها همچنان می‌توانند با agent صحبت کنند.

**چه چیزی ممکن است در آینده gated شود:** سطوح قابلیت بیشتری (دسترسی ابزار، تغییر مدل، عملیات سنگین) به همان تمایز admin / user آویزان خواهند شد. پیکربندی تقسیم در حال حاضر به این معنی است که آن محدودیت‌های آینده بدون نیاز به بازسازی اینکه کی admin است فرود می‌آیند.

#### پیکربندی​

```
gateway:  platforms:    discord:      extra:        allow_from: ["111", "222", "333"]        allow_admin_from: ["111"]                    # admins → all slash commands        user_allowed_commands: [status, model]       # what non-admins may run        # Optional: separate group/channel scope        group_allow_admin_from: ["111"]        group_user_allowed_commands: [status]
```

**سازگاری با عقب:** اگر `allow_admin_from` برای یک scope تنظیم نشده باشد، تقسیم سطح برای آن scope غیرفعال است و هر کاربر مجاز دسترسی کامل دارد. نصب‌های موجود بدون تغییر کار می‌کنند — وقتی تمایز می‌خواهید opt-in کنید.

`allow_admin_from`

#### بررسی دسترسی خود​

از `/whoami` از هر پلتفرم برای دیدن scope فعال، سطح شما (admin / user / unrestricted) و اینکه کدام دستورات اسلش می‌توانید اجرا کنید استفاده کنید. نمونه‌های مختص پلتفرم را در صفحات [Telegram](/docs/user-guide/messaging/telegram#slash-command-access-control) و [Discord](/docs/user-guide/messaging/discord#slash-command-access-control) ببینید.

`/whoami`
[Telegram](/docs/user-guide/messaging/telegram#slash-command-access-control)
[Discord](/docs/user-guide/messaging/discord#slash-command-access-control)

## قطع کردن Agent​

هنگام کار agent هر پیامی ارسال کنید تا آن را قطع کنید. رفتارهای کلیدی:

- فرمان‌های ترمinal در حال اجرا فوراً کشته می‌شوند (`SIGTERM`، سپس `SIGKILL` پس از ۱ ثانیه)
- فراخوانی‌های ابزار لغو می‌شوند — فقط آن‌که در حال حاضر در حال اجراست اجرا می‌شود، بقیه رد می‌شوند
- چندین پیام ترکیب می‌شوند — پیام‌های ارسال‌شده در حین قطع در یک prompt واحد ادغام می‌شوند
- دستور `/stop` — بدون صف‌بندی پیام پیگیری قطع می‌کند

`/stop`

### صف در مقابل قطع در مقابل هدایت (حالت busy-input)​

به طور پیش‌فرض، پیام‌رسانی به یک agent مشغول آن را قطع می‌کند. دو حالت دیگر موجود است:

- `queue` — پیام‌های پیگیری منتظر می‌مانند و به عنوان نوبت بعدی پس از اتمام task فعلی اجرا می‌شوند.
- `steer` — پیام‌های پیگیری از طریق `/steer` به اجرای فعلی تزریق می‌شوند، پس از فراخوانی ابزار بعدی به agent می‌رسند. بدون قطع، بدون نوبت جدید. اگر agent هنوز شروع نکرده باشد به رفتار `queue` برمی‌گردد.

`queue`
`steer`
`/steer`
`queue`

```
display:  busy_input_mode: steer   # or queue, or interrupt (default)  busy_ack_enabled: true   # set to false to suppress the ⚡/⏳/⏩ chat reply entirely
```

اولین باری که به یک agent مشغول در هر پلتفرم پیام می‌دهید، Hermes یک یادآوری یک‌خطی به busy-ack اضافه می‌کند که knob را توضیح می‌دهد ("💡 First-time tip — …"). یادآوری یک بار به ازای هر نصب شلیک می‌کند — یک flag زیر `onboarding.seen.busy_input_prompt` آن را latch می‌کند. آن کلید را حذف کنید تا نکته را دوباره ببینید.

`"💡 First-time tip — …"`
`onboarding.seen.busy_input_prompt`

اگر busy-ack را پرسروصدا می‌یابید — به خصوص با ورودی صوتی یا پیام‌های سریع — `display.busy_ack_enabled: false` را تنظیم کنید. ورودی شما همچنان به طور عادی صف‌بندی/هدایت/قطع می‌شود، فقط پاسخ چت ساکت می‌شود.

`display.busy_ack_enabled: false`

## اعلان‌های پیشرفت ابزار​

میزان نمایش فعالیت ابزار را در `~/.hermes/config.yaml` کنترل کنید:

`~/.hermes/config.yaml`

```
display:  tool_progress: all    # off | new | all | verbose  tool_progress_command: false  # set to true to enable /verbose in messaging  # How progress is grouped on platforms that support message editing:  #   accumulate (default) — edit one bubble in place as tools run  #   separate             — send one message per tool (pre-v0.9 style; noisier)  # Only applies where tool_progress is already enabled.  tool_progress_grouping: accumulate   # accumulate | separate
```

### مهرهای زمانی پیام در context مدل​

به طور پیش‌فرض خاموش. وقتی فعال می‌شود، Hermes یک مهر زمان خوانا
(مثلاً `[Tue 2026-04-28 13:40:53 CEST]`) را به هر پیام `user` در
context مدل اضافه می‌کند تا agent بداند پیام‌ها چه زمانی ارسال شده‌اند — مفید برای
استدلال زمانی ("شما امروز صبح پرسیدید…"، توجه به یک فاصله طولانی). به پیام‌های assistant
یا system prompt **اضافه نمی‌شود**.

`[Tue 2026-04-28 13:40:53 CEST]`

```
gateway:  message_timestamps:    enabled: false   # set true to show send-times to the model
```

رونوشتهای ذخیره‌شده همیشه تمیز باقی می‌مانند — مهر زمان به عنوان metadata پیام
ذخیره می‌شود صرف‌نظر از این toggle، بنابراین فعال کردن آن بعداً هم زمان‌های ارسال
پیام‌های گذشته را نشان می‌دهد و replay هرگز پیشوندهای تکراری تجمع نمی‌کند.

وقتی فعال می‌شود، بات هنگام کار پیام‌های وضعیت ارسال می‌کند:

```
💻 `ls -la`...🔍 web_search...📄 web_extract...🐍 execute_code...
```

## Sessionهای پس‌زمینه​

یک prompt را در یک session پس‌زمینه جداگانه اجرا کنید تا agent به طور مستقل روی آن کار کند در حالی که چت اصلی شما پاسخگو باقی می‌ماند:

```
/background Check all servers in the cluster and report any that are down
```

Hermes فوراً تأیید می‌کند:

```
🔄 Background task started: "Check all servers in the cluster..."   Task ID: bg_143022_a1b2c3
```

### نحوه عملکرد​

هر prompt `/background` یک **instance agent جداگانه** ایجاد می‌کند که به صورت ناهمگام اجرا می‌شود:

`/background`
- **Session ایزوله** — agent پس‌زمینه session خود با تاریخچه مکالمه خود را دارد. هیچ آگاهی از context چت فعلی شما ندارد و فقط promptی را که ارائه می‌دهید دریافت می‌کند.
- **پیکربندی یکسان** — مدل، provider، toolsetها، تنظیمات reasoning و مسیریابی provider را از تنظیم gateway فعلی به ارث می‌برد.
- **non-blocking** — چت اصلی شما کاملاً تعاملی باقی می‌ماند. پیام ارسال کنید، دستورات دیگر اجرا کنید یا taskهای پس‌زمینه بیشتری شروع کنید در حالی که کار می‌کند.
- **تحویل نتیجه** — وقتی task تمام می‌شود، نتیجه به همان چت یا کانالی که دستور را صادر کرده‌اید ارسال می‌شود، با پیشوند "✅ Background task complete". اگر ناموفق باشد، "❌ Background task failed" با خطا را خواهید دید.

### اعلان‌های فرآیند پس‌زمینه​

وقتی agent اجرای یک session پس‌زمینه از `terminal(background=true)` برای شروع فرآیندهای طولانی‌مدت (سرورها، buildها و غیره) استفاده می‌کند، gateway می‌تواند به‌روزرسانی‌های وضعیت را به چت شما ارسال کند. این را با `display.background_process_notifications` در `~/.hermes/config.yaml` کنترل کنید:

`terminal(background=true)`
`display.background_process_notifications`
`~/.hermes/config.yaml`

```
display:  background_process_notifications: all    # all | result | error | off
```

| حالت | چه چیزی دریافت می‌کنید |
| --- | --- |
| `all` | به‌روزرسانی‌های خروجی در حال اجرا **و** پیام تکمیل نهایی (پیش‌فرض) |
| `result` | فقط پیام تکمیل نهایی (صرف‌نظر از exit code) |
| `error` | فقط پیام نهایی وقتی exit code غیرصفر است |
| `off` | اصلاً پیام ناظر فرآیند نیست |

`all`
`result`
`error`
`off`

همچنین می‌توانید این را از طریق متغیر محیطی تنظیم کنید:

```
HERMES_BACKGROUND_NOTIFICATIONS=result
```

### موارد استفاده​

- **نظارت سرور** — "/background Check the health of all services and alert me if anything is down"
- **Buildهای طولانی** — "/background Build and deploy the staging environment" در حالی که به چت کردن ادامه می‌دهید
- **تکلیف تحقیق** — "/background Research competitor pricing and summarize in a table"
- **عملیات فایل** — "/background Organize the photos in ~/Downloads by date into folders"

Taskهای پس‌زمینه در پلتفرم‌های پیام‌رسانی fire-and-forget هستند — نیازی به انتظار یا بررسی نیست. نتایج به طور خودکار در همان چت وقتی task تمام می‌شود می‌رسند.

## مدیریت سرویس​

### Linux (systemd)​

```
hermes gateway install               # Install as user servicehermes gateway start                 # Start the servicehermes gateway stop                  # Stop the servicehermes gateway status                # Check statusjournalctl --user -u hermes-gateway -f  # View logs# Enable lingering (keeps running after logout)sudo loginctl enable-linger $USER# Or install a boot-time system service that still runs as your usersudo hermes gateway install --systemsudo hermes gateway start --systemsudo hermes gateway status --systemjournalctl -u hermes-gateway -f
```

از سرویس user در لپ‌تاپ‌ها و ماشین‌های توسعه استفاده کنید. از سرویس system در VPS یا هاستهای headless که باید بدون تکیه بر systemd linger در بوت بازگردند استفاده کنید.

`ExecStopPost`

Unit نصب‌شده توسط Hermes از قبل gateway را به طور تمیز با `KillMode=mixed` + `KillSignal=SIGTERM` خاموش می‌کند و از `Restart=always` با `RestartForceExitStatus` استفاده می‌کند تا به‌روزرسانی‌ها و `/restart` به درستی respawn شوند. **یک systemd drop-in مانند `ExecStopPost=/bin/kill -9 $MAINPID` اضافه نکنید** — `ExecStopPost` در **هر** توقفی شلیک می‌کند، شامل بازنشانی‌های تمیز، بنابراین instance تازه متولدشده را قبل از تثبیت SIGKILL می‌کند و `Restart=always` فوراً respawn می‌کند. نتیجه یک حلقه بازنشانی بی‌نهایت (و در Telegram، سیل پیام‌های بازنشانی) است. اگر چنین drop-inی اضافه کرده‌اید، آن را حذف کنید: `systemctl --user edit hermes-gateway` (یا `sudo systemctl edit hermes-gateway` برای سرویس system) و خط `ExecStopPost` را حذف کنید، سپس `systemctl --user daemon-reload`.

`KillMode=mixed`
`KillSignal=SIGTERM`
`Restart=always`
`RestartForceExitStatus`
`/restart`
`ExecStopPost=/bin/kill -9 $MAINPID`
`ExecStopPost`
`SIGKILL`
`Restart=always`
`systemctl --user edit hermes-gateway`
`sudo systemctl edit hermes-gateway`
`ExecStopPost`
`systemctl --user daemon-reload`

سرویس system برای هر بازنشانی به root نیاز دارد — شامل بازنشانی خودکار gateway در انتهای `hermes update`. وقتی `hermes update` به عنوان کاربر non-root اجرا می‌شود، سعی می‌کند `sudo systemctl` بدون رمز عبور؛ اگر موجود نباشد، بازنشانی را رد می‌کند و دستور دستی `sudo systemctl restart hermes-gateway` را چاپ می‌کند (هرگز در یک prompt رمز عبور تعاملی مسدود نمی‌شود).

`hermes update`
`hermes update`
`sudo systemctl`
`sudo systemctl restart hermes-gateway`

برای یک VM headless که هرگز وارد آن نمی‌شوید، سرویس user با linger فعال رفتار مشابه شروع در بوت با zero root involvement می‌دهد:

```
hermes gateway install          # user servicesudo loginctl enable-linger $USER   # one-time: start at boot, survive logout
```

پس از آن، `hermes update` می‌تواند بدون هیچ امتیازی gateway را بازنشانی کند. اگر ترجیح می‌دهید سرویس system را نگه دارید، یا به‌روزرسانی‌ها را با `sudo hermes update` اجرا کنید، یا به حساب سرویس sudo بدون رمز عبور برای systemctl بدهید، مثلاً در `sudo visudo -f /etc/sudoers.d/hermes-gateway`:

`hermes update`
`sudo hermes update`
`sudo visudo -f /etc/sudoers.d/hermes-gateway`

```
hermes ALL=(root) NOPASSWD: /usr/bin/systemctl --no-ask-password reset-failed hermes-gateway*, /usr/bin/systemctl --no-ask-password start hermes-gateway*, /usr/bin/systemctl --no-ask-password restart hermes-gateway*
```

از نگه داشتن همزمان unitهای gateway user و system خودداری کنید مگر واقعاً منظورتان باشد. Hermes هشدار می‌دهد اگر هر دو را تشخیص دهد زیرا رفتار start/stop/status مبهم می‌شود.

اگر چندین نصب Hermes روی یک ماشین (با دایرکتوری‌های مختلف `HERMES_HOME`) اجرا می‌کنید، هر کدام نام سرویس systemd خاص خود را دارد. پیش‌فرض `~/.hermes` از `hermes-gateway` استفاده می‌کند؛ نصب‌های دیگر از `hermes-gateway-<hash>` استفاده می‌کنند. دستورات `hermes gateway` به طور خودکار سرویس صحیح را برای `HERMES_HOME` فعلی شما هدف قرار می‌دهند.

`HERMES_HOME`
`~/.hermes`
`hermes-gateway`
`hermes-gateway-<hash>`
`hermes gateway`
`HERMES_HOME`

### macOS (launchd)​

```
hermes gateway install               # Install as launchd agenthermes gateway start                 # Start the servicehermes gateway stop                  # Stop the servicehermes gateway status                # Check statustail -f ~/.hermes/logs/gateway.log   # View logs
```

plist تولیدشده در `~/Library/LaunchAgents/ai.hermes.gateway.plist` زندگی می‌کند. سه متغیر محیطی شامل دارد:

`~/Library/LaunchAgents/ai.hermes.gateway.plist`
- `PATH` — کل PATH shell شما در زمان نصب، با `bin/` venv و `node_modules/.bin` در ابتدای آن. این تضمین می‌کند ابزارهای نصب‌شده توسط کاربر (Node.js، ffmpeg و غیره) برای subprocessهای gateway مانند WhatsApp bridge موجود هستند.
- `VIRTUAL_ENV` — به Python virtualenv اشاره می‌کند تا ابزارها بتوانند بسته‌ها را به درستی resolve کنند.
- `HERMES_HOME` — gateway را به نصب Hermes شما محدود می‌کند.

`bin/`
`node_modules/.bin`

plistهای launchd ایستا هستند — اگر پس از تنظیم gateway ابزارهای جدید نصب کنید (مثلاً نسخه Node.js جدید از طریق nvm، یا ffmpeg از طریق Homebrew)، دوباره `hermes gateway install` اجرا کنید تا PATH به‌روزشده را ثبت کند. Gateway plist منسوخ را تشخیص داده و به طور خودکار reload می‌کند.

`hermes gateway install`

مانند سرویس systemd Linux، هر دایرکتوری `HERMES_HOME` لیبل launchd خاص خود را دارد. پیش‌فرض `~/.hermes` از `ai.hermes.gateway` استفاده می‌کند؛ نصب‌های دیگر از `ai.hermes.gateway-<suffix>` استفاده می‌کنند.

`HERMES_HOME`
`~/.hermes`
`ai.hermes.gateway`
`ai.hermes.gateway-<suffix>`

## Toolsetهای مختص پلتفرم​

هر پلتفرم toolset خاص خود را دارد:

| پلتفرم | Toolset | قابلیت‌ها |
| --- | --- | --- |
| CLI | hermes-cli | دسترسی کامل |
| Telegram | hermes-telegram | ابزارهای کامل شامل ترمinal |
| Discord | hermes-discord | ابزارهای کامل شامل ترمinal |
| WhatsApp | hermes-whatsapp | ابزارهای کامل شامل ترمinal |
| WhatsApp Cloud API | hermes-whatsapp | ابزارهای کامل شامل ترمinal (toolset را با WhatsApp bridge به اشتراک می‌گذارد) |
| Slack | hermes-slack | ابزارهای کامل شامل ترمinal |
| Google Chat | hermes-google_chat | ابزارهای کامل شامل ترمinal |
| Signal | hermes-signal | ابزارهای کامل شامل ترمinal |
| SMS | hermes-sms | ابزارهای کامل شامل ترمinal |
| Email | hermes-email | ابزارهای کامل شامل ترمinal |
| Home Assistant | hermes-homeassistant | ابزارهای کامل + کنترل دستگاه HA (ha_list_entities، ha_get_state، ha_call_service، ha_list_services) |
| Mattermost | hermes-mattermost | ابزارهای کامل شامل ترمinal |
| Matrix | hermes-matrix | ابزارهای کامل شامل ترمinal |
| DingTalk | hermes-dingtalk | ابزارهای کامل شامل ترمinal |
| Feishu/Lark | hermes-feishu | ابزارهای کامل شامل ترمinal |
| WeCom | hermes-wecom | ابزارهای کامل شامل ترمinal |
| WeCom Callback | hermes-wecom-callback | ابزارهای کامل شامل ترمinal |
| Weixin | hermes-weixin | ابزارهای کامل شامل ترمinal |
| BlueBubbles | hermes-bluebubbles | ابزارهای کامل شامل ترمinal |
| QQBot | hermes-qqbot | ابزارهای کامل شامل ترمinal |
| Yuanbao | hermes-yuanbao | ابزارهای کامل شامل ترمinal |
| Microsoft Teams | hermes-teams | ابزارهای کامل شامل ترمinal |
| API Server | hermes-api-server | ابزارهای کامل (`clarify`، `text_to_speech` را حذف می‌کند — دسترسی برنامه‌ای کاربر تعاملی ندارد) |
| Webhooks | hermes-webhook | ابزارهای کامل شامل ترمinal |
| Raft | hermes-raft | کانال فقط wake؛ agent از Raft CLI برای I/O پیام استفاده می‌کند |

`hermes-cli`
`hermes-telegram`
`hermes-discord`
`hermes-whatsapp`
`hermes-whatsapp`
`hermes-slack`
`hermes-google_chat`
`hermes-signal`
`hermes-sms`
`hermes-email`
`hermes-homeassistant`
`hermes-mattermost`
`hermes-matrix`
`hermes-dingtalk`
`hermes-feishu`
`hermes-wecom`
`hermes-wecom-callback`
`hermes-weixin`
`hermes-bluebubbles`
`hermes-qqbot`
`hermes-yuanbao`
`hermes-teams`
`hermes-api-server`
`clarify`
`text_to_speech`
`hermes-webhook`
`hermes-raft`

## اجرای gateway چندپلتفرمی​

یک gateway معمولاً چندین adapter را همزمان اجرا می‌کند (Telegram + Discord + Slack و غیره). بخش‌های زیر عملیات day-2 را پوشش می‌دهند که همه پلتفرم‌ها را در بر می‌گیرد.

### دستور `/platform`​

`/platform`

وقتی gateway در حال اجرا است، از دستور اسلش `/platform` از هر session CLI متصل یا چت برای بررسی و هدایت adapterهای جداگانه بدون بازنشانی کل gateway استفاده کنید:

`/platform`

```
/platform list                  # show all adapters and their state/platform pause <name>          # stop dispatching new messages to one adapter/platform resume <name>         # re-enable a paused adapter
```

`/platform list` نشان می‌دهد هر adapter در حال `running`، `paused` (دستی) یا `paused-by-breaker` (به زیر مراجعه کنید) است. متوقف نگه داشتن adapter را load شده و loopهای پس‌زمینه آن زنده نگه می‌دارد — پیام‌های دریافتی drop می‌شوند، اما خود اتصال باز باقی می‌ماند تا resume فوری باشد.

`/platform list`
`running`
`paused`
`paused-by-breaker`

همچنین دستور خلاصه وضعیت گسترده‌تر `/platforms` را ببینید.

[/platforms](/docs/reference/slash-commands#info)
`/platforms`

### مدارک قطع خودکار​

هر adapter در یک مدارک قطع پیچیده شده. شکستهای قابل تلاش مجدد مکرر (قطعات شبکه، پاسخ‌های rate-limit، پاسخ‌های 5xx upstream، قطع websocket) باعث trip شدن مدارک می‌شود — adapter به طور خودکار متوقف می‌شود، یک اعلان operator به کانال اصلی پلتفرم زنده دیگر ارسال می‌شود وقتی یکی پیکربندی شده و یک خط log ساختاریافته منتشر می‌شود.

مدارک به طور خودکار **resume نمی‌شود** — تا زمانی که دستی `/platform resume <name>` اجرا کنید باز باقی می‌ماند. این عمدی است: اگر یک پلتفرم در یک قطع طولانی است، نمی‌خواهید gateway تلاش‌های reconnect را تکان دهد.

`/platform resume <name>`

### کجا نگاه کنید وقتی پلتفرم متوقف است​

وقتی یک adapter متوقف است، بررسی کنید:

1. **Log gateway** (`~/.hermes/logs/gateway.log` یا log unit systemd / launchd). نام پلتفرم و `circuit breaker`، `paused` یا `disabled` را جستجو کنید. رویداد trip شامل تعداد شکست و آخرین خطا است.
2. **خروجی `/platform list`** — وضعیت فعلی و آخرین دلیل را نشان می‌دهد.
3. **صفحه وضعیت provider** (وضعیت Telegram bot API، وضعیت Discord و غیره). مدارک trip شده زیرا پلتفرم ناسالم بود؛ تا قبل از بازگشت سعی نکنید resume کنید.

`~/.hermes/logs/gateway.log`
`circuit breaker`
`paused`
`disabled`
`/platform list`

وقتی upstream سالم است، `/platform resume <name>` مدارک را پاک و adapter را دوباره armed می‌کند.

`/platform resume <name>`

### اعلان‌های بازنشانی​

وقتی gateway بازنشانی می‌شود (یا با sessionهای در حال پرواز خاموش می‌شود)، می‌تواند یک پیام یک‌باره "agent بازگشت" / "agent قطع شد" به کانال اصلی هر پلتفرم ارسال کند. این توسط flag `gateway_restart_notification` در `gateway-config.yaml` به ازای هر پلتفرم کنترل می‌شود که پیش‌فرض `true` است:

`gateway_restart_notification`
`gateway-config.yaml`
`true`

```
gateway:  platforms:    telegram:      home_chat_id: "123456789"      gateway_restart_notification: false   # opt out for this platform    discord:      home_chat_id: "987654321"      # gateway_restart_notification omitted → defaults to true
```

آن را در پلتفرم‌های پرسروصدا یا کم‌اولویت غیرفعال کنید در حالی که برای چت اصلی خود فعال نگه دارید. اعلان یک بار در هر بازنشانی ارسال می‌شود، صرف‌نظر از اینکه چند session در حال پرواز بود.

### نشانگرهای تایپ​

وقتی agent در حال پردازش پیامی است، gateway یک وضعیت تایپ زنده در پلتفرم‌هایی که از آن پشتیبانی می‌کنند نشان می‌دهد — حباب "typing…" در Telegram/Discord/Signal، یا وضعیت assistant "is thinking…" در Slack. این توسط flag `typing_indicator` در `gateway-config.yaml` به ازای هر پلتفرم کنترل می‌شود که پیش‌فرض `true` است:

`typing_indicator`
`gateway-config.yaml`
`true`

```
gateway:  platforms:    slack:      typing_indicator: false   # don't show "is thinking…" on Slack    telegram:      # typing_indicator omitted → defaults to true
```

`typing_indicator: false` را در هر پلتفرمی که نشانگر ناخواسته است تنظیم کنید. برخی کاربران وضعیت "is thinking…" Slack را پرسروصدا می‌یابند (هنگام نمایش به طور مختصر compose box را نیز غیرفعال می‌کند، زیرا از Slack Assistant API استفاده می‌کند). غیرفعال کردن فقط نشانگر را سرکوب می‌کند — تحویل پیام و همه چیز دیگر تغییر نمی‌کند. Flag عمومی است، بنابراین همان کلید برای هر پلتفرم کار می‌کند.

`typing_indicator: false`

### ادامه Session در بازنشانی gateway​

وقتی gateway با یک فراخوانی ابزار در حال پرواز یا تولید خاموش می‌شود، sessionهای تحت تأثیر به عنوان `restart_interrupted` علامت‌گذاری می‌شوند. در شروع بعدی، gateway یک resume خودکار برای هر کدام زمان‌بندی می‌کند — کاربر یک اخطار کوتاه در چت دریافت می‌کند ("Send any message after restart and I'll try to resume where you left off.") و session از آخرین نوبت commit شده ادامه می‌یابد وقتی پاسخ دهند.

`restart_interrupted`

این رفتار به طور پیش‌فرض فعال است و هنگام شروع gateway لاگ می‌شود:

```
Scheduled auto-resume for N restart-interrupted session(s)
```

هیچ پیکربندی لازم نیست. اگر اخطار نمی‌خواهید، `gateway_restart_notification: false` را در پلتفرم تنظیم کنید.

`gateway_restart_notification: false`

### پیش‌فرض‌های پیشرفت سازگار با موبایل​

Telegram معمولاً یک inbox موبایل است، بنابراین پیش‌فرض‌ها برای آن سطح تنظیم شده‌اند:

- `tool_progress` پیش‌فرض `off` — جریان breadcrumb به ازای هر ابزار که چت را پر کند نیست.
- `busy_ack_detail` پیش‌فرض `off` — تأییدهای busy-state و heartbeatهای طولانی‌مدت مختصر باقی می‌مانند (بدون جزئیات دیباگ `iteration 21/60`).
- `interim_assistant_messages` **روشن** — تفسیر واقعی mid-turn assistant (مدل واقعاً به شما می‌گوید چه کاری قرار است انجام دهد) سیگنال است، نه نویز.
- `long_running_notifications` **روشن** — حباب edit-in-place "⏳ Working — N min" هر چند دقیقه به‌روزرسانی می‌شود تا heartbeat داشته باشید به جای نگاه کردن به `typing…` برای نیم ساعت.

`tool_progress`
`off`
`busy_ack_detail`
`off`
`iteration 21/60`
`interim_assistant_messages`
`long_running_notifications`
`typing…`

از هر یک از پیش‌فرض‌های روشن opt-out کنید یا دوباره به progress verbose به ازای هر پلتفرم opt-in کنید:

```
display:  platforms:    telegram:      # Re-enable the tool-progress stream      tool_progress: new      # Show "iteration N/M, running: tool" in heartbeats and busy acks      busy_ack_detail: true      # Or quiet them entirely      interim_assistant_messages: false      long_running_notifications: false
```

### پاک‌سازی حباب پیشرفت (opt-in)​

پیام‌های tool-progress، heartbeat "still working…" و حباب‌های status-callback همچنین می‌توانند پس از فرود پاسخ نهایی به طور خودکار حذف شوند. به ازای هر پلتفرم از طریق `display.platforms.<platform>.cleanup_progress` فعال کنید:

`display.platforms.<platform>.cleanup_progress`

```
display:  platforms:    telegram:      cleanup_progress: true    discord:      cleanup_progress: true
```

پیش‌فرض `false`. فقط پلتفرم‌هایی که adapter آن‌ها `delete_message` را پیاده‌سازی می‌کنند تنظیم را رعایت می‌کنند (در حال حاضر Telegram و Discord). اجرای ناموفق cleanup را رد می‌کند بنابراین حباب‌ها به عنوان breadcrumb باقی می‌مانند.

`false`
`delete_message`

## قدم بعدی​

- [راه‌اندازی Telegram](/docs/user-guide/messaging/telegram)
- [راه‌اندازی Discord](/docs/user-guide/messaging/discord)
- [راه‌اندازی Slack](/docs/user-guide/messaging/slack)
- [راه‌اندازی Google Chat](/docs/user-guide/messaging/google_chat)
- [راه‌اندازی WhatsApp](/docs/user-guide/messaging/whatsapp)
- [راه‌اندازی WhatsApp Business Cloud API](/docs/user-guide/messaging/whatsapp-cloud)
- [راه‌اندازی Signal](/docs/user-guide/messaging/signal)
- [راه‌اندازی SMS (Twilio)](/docs/user-guide/messaging/sms)
- [راه‌اندازی Email](/docs/user-guide/messaging/email)
- [یکپارچه‌سازی Home Assistant](/docs/user-guide/messaging/homeassistant)
- [راه‌اندازی Mattermost](/docs/user-guide/messaging/mattermost)
- [راه‌اندازی Matrix](/docs/user-guide/messaging/matrix)
- [راه‌اندازی DingTalk](/docs/user-guide/messaging/dingtalk)
- [راه‌اندازی Feishu/Lark](/docs/user-guide/messaging/feishu)
- [راه‌اندازی WeCom](/docs/user-guide/messaging/wecom)
- [راه‌اندازی WeCom Callback](/docs/user-guide/messaging/wecom-callback)
- [راه‌اندازی Weixin (WeChat)](/docs/user-guide/messaging/weixin)
- [راه‌اندازی BlueBubbles (iMessage)](/docs/user-guide/messaging/bluebubbles)
- [راه‌اندازی QQBot](/docs/user-guide/messaging/qqbot)
- [راه‌اندازی Yuanbao](/docs/user-guide/messaging/yuanbao)
- [راه‌اندازی Microsoft Teams](/docs/user-guide/messaging/teams)
- [Teams Meetings Pipeline](/docs/user-guide/messaging/teams-meetings)
- [Open WebUI + API Server](/docs/user-guide/messaging/open-webui)
- [راه‌اندازی Raft](/docs/user-guide/messaging/raft)
- [راه‌اندازی IRC](/docs/user-guide/messaging/irc)
- [Webhooks](/docs/user-guide/messaging/webhooks)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/messaging/index.md)