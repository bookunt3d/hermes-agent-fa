---
layout: docs
title: "پیکربندی مدل‌ها"
permalink: /docs/user-guide/configuring-models/
---

- 
- استفاده از Hermes
- پیکربندی مدل‌ها

# پیکربندی مدل‌ها

Hermes از دو نوع اسلات مدل استفاده می‌کند:

- **مدل اصلی** — مدلی که عامل با آن فکر می‌کند. هر پیام کاربر، هر حلقه فراخوانی ابزار، هر پاسخ جریانی از این مدل عبور می‌کند.
- **مدل‌های کمکی** — کارهای جانبی کوچک‌تری که عامل آن‌ها را برون‌سپاری می‌کند. فشرده‌سازی زمینه، بینایی (تحلیل تصویر)، خلاصه‌سازی صفحه وب، امتیازدهی تأیید، مسیریابی ابزار MCP، تولید عنوان جلسه و جستجوی مهارت. هر کدام اسلات جداگانه خود را دارند و می‌توانند به طور مستقل بازنویسی شوند.

این صفحه پیکربندی هر دو از داشبورد را پوشش می‌دهد. اگر فایل‌های پیکربندی یا CLI را ترجیح می‌دهید، به **روش‌های جایگزین** در انتهای صفحه بروید.

**Nous Portal** بیش از 300 مدل را تحت یک اشتراک ارائه می‌دهد. در یک نصب جدید، `hermes setup --portal` را اجرا کنید تا وارد شوید و Nous را به عنوان ارائه‌دهنده خود با یک دستور تنظیم کنید. با `hermes portal info` بررسی کنید چه چیزی متصل است.

[Nous Portal](/docs/user-guide/features/tool-gateway)
`hermes setup --portal`
`hermes portal info`
- مشترکان Portal همچنین **10% تخفیف** برای ارائه‌دهندگان صورتحساب توکن دریافت می‌کنند.

`model:`

در یک نصب کاملاً جدید، پیکربندی پیش‌فرض بسته‌شده دارای `model: ""` (یک رشته خالی نشان‌دهنده «هنوز پیکربندی نشده») است. اولین باری که `hermes setup` یا `hermes model` را اجرا می‌کنید، این کلید به صورت درجا به یک نگاشت با زیرکلیدهای `provider`، `default`، `base_url` و `api_mode` ارتقا می‌یابد — شکلی که در این صفحه و در `profiles.md`/`configuration.md` نشان داده شده است. اگر هرگز رشته خالی در `config.yaml` دیدید، `hermes model` را اجرا کنید (یا در داشبورد روی **Change** کلیک کنید) و Hermes فرم دیکشنری را برای شما می‌نویسد.

`model: ""`
`hermes setup`
`hermes model`
`provider`
`default`
`base_url`
`api_mode`
[profiles.md](/docs/user-guide/profiles)
`profiles.md`
[configuration.md](/docs/user-guide/configuration)
`configuration.md`
`config.yaml`
`hermes model`

## صفحه مدل‌ها

داشبورد را باز کنید و روی **Models** در نوار کلیک کنید. دو بخش دریافت می‌کنید:

1. **تنظیمات مدل** — پنل بالا، جایی که مدل‌ها را به اسلات‌ها اختصاص می‌دهید.
2. **تحلیل مصرف** — کارت‌های رتبه‌بندی‌شده که هر مدلی را که در دوره انتخابی جلسه‌ای را اجرا کرده نشان می‌دهند، با شمارش توکن‌ها، هزینه و نشان‌های قابلیت.

کارت بالا پنل **تنظیمات مدل** است. ردیف اصلی همیشه نشان می‌دهد عامل چه چیزی را برای جلسات جدید راه‌اندازی می‌کند. روی **Change** کلیک کنید تا انتخابگر باز شود.

## تنظیم مدل اصلی

روی **Change** در ردیف مدل اصلی کلیک کنید:

انتخابگر دو ستون دارد:

- **چپ** — ارائه‌دهندگان احراز هویت‌شده. فقط ارائه‌دهندگانی که راه‌اندازی کرده‌اید (کلید API تنظیم‌شده، OAuth شده، یا به عنوان نقطه پایانی سفارشی تعریف شده) اینجا نمایش داده می‌شوند. اگر ارائه‌دهنده‌ای وجود ندارد، به **Keys** بروید و اعتبار آن را اضافه کنید.
- **راست** — فهرست مدل‌های گلچین‌شده برای ارائه‌دهنده انتخابی. این‌ها مدل‌های عاملی هستند که Hermes برای آن ارائه‌دهنده توصیه می‌کند، نه داده خام `/models` (که در OpenRouter شامل بیش از 400 مدل از جمله TTS، تولیدکنندگان تصویر و reranker‌ها است).

`/models`

در کادر فیلتر تایپ کنید تا بر اساس نام ارائه‌دهنده، slug یا شناسه مدل محدود شود.

یک مدل انتخاب کنید، روی **Switch** بزنید و Hermes آن را در `~/.hermes/config.yaml` تحت بخش `model` می‌نویسد. **این فقط برای جلسات جدید اعمال می‌شود** — هر تب چتی که قبلاً باز کرده‌اید با همان مدلی که شروع کرده ادامه می‌دهد. برای تعویض چت فعلی، از دستور اسلش `/model` داخل آن استفاده کنید.

`~/.hermes/config.yaml`
`model`
`/model`

### تعویض در حین جلسه و هشدارهای زمینه

وقتی مدل‌ها را **داخل یک جلسه فعال** تعویض می‌کنید (انتخابگر مدل TUI Herm، CLI `hermes`، یا `/model` در Telegram/Discord)، Hermes تخمین می‌زند آیا **پیام بعدی** شما **فشرده‌سازی زمینه پیش‌پرواز** را روی پنجره مدل جدید اجرا خواهد کرد یا خیر. اگر جلسه در حال حاضر نزدیک یا بالاتر از آستانه فشرده‌سازی آن مدل باشد (به فشرده‌سازی زمینه مراجعه کنید)، پاسخ تعویض شامل یک هشدار است — همان مسیر `warning_message` که برای اطلاعیه‌های مدل گران‌قیمت استفاده می‌شود. تعویض همچنان فوراً اعمال می‌شود؛ فشرده‌سازی روی **اولین پیام کاربر پس از تعویض** اجرا می‌شود، قبل از پاسخ مدل.

`hermes`
`/model`
[فشرده‌سازی زمینه](/docs/user-guide/configuration#context-compression)
`warning_message`

کش‌های Prompt به مدلی که درخواست را سرویس‌دهی می‌کند کلید خورده‌اند، بنابراین هر تغییر مدل در حین مکالمه — یک تغییر صریح `/model`، یک **فال‌بک خودکار**، یا چرخش **استخر اعتبار** روی حساب متفاوت — به این معنی است که پیام بعدی کل مکالمه را با قیمت کامل توکن ورودی (به جای نرخ تخفیف‌خورده کش (~75-90%)) بازخوانی می‌کند. در یک جلسه طولانی، این بازخوانی یک‌باره می‌تواند از تفاوت به ازای توکن بین دو مدل بزرگ‌تر باشد. در صورت نیاز تعویض کنید، اما ترجیحاً در ابتدای مکالمه یا بلافاصله پس از شروع یک جلسه جدید.

`/model`
[فال‌بک خودکار](/docs/user-guide/features/fallback-providers)
[استخر اعتبار](/docs/user-guide/features/credential-pools)

## تنظیم مدل‌های کمکی

روی **Show auxiliary** کلیک کنید تا 11 اسلات کاری نمایش داده شوند:

هر کار کمکی به صورت پیش‌فرض `auto` است — به این معنی که Hermes مدل اصلی شما را هم برای آن کار امتحان می‌کند. اگر آن مسیر در دسترس نباشد یا با خطای ظرفیتی مواجه شود، `auto` زنجیره `auxiliary.<task>.fallback_chain` مخصوص آن کار، سپس زنجیره اصلی `fallback_providers`/`fallback_model`، و سپس زنجیره کشف کمکی داخلی Hermes را دنبال می‌کند. یک کار خاص را بازنویسی کنید وقتی مدل ارزان‌تر یا سریع‌تری برای کار جانبی می‌خواهید.

`auto`
`auto`
`auxiliary.<task>.fallback_chain`
`fallback_providers`
`fallback_model`

### الگوهای رایج بازنویسی

| کار | چه زمانی بازنویسی کنید |
| --- | --- |
| تولید عنوان | تقریباً همیشه. یک مدل flash به قیمت $0.10/M عناوین جلسه را به خوبی Opus می‌نویسد. پیکربندی پیش‌فرض این را روی OpenRouter به `google/gemini-3-flash-preview` تنظیم می‌کند. |
| بینایی | وقتی مدل اصلی شما از بینایی پشتیبانی نمی‌کند. آن را به `google/gemini-2.5-flash` یا `gpt-4o-mini` اشاره دهید. |
| فشرده‌سازی | وقتی توکن‌های استدلال را روی Opus/M2.7 فقط برای خلاصه‌سازی زمینه می‌سوزانید. یک مدل چت سریع همان کار را با 1/50 هزینه انجام می‌دهد. |
| تأیید | برای `approval_mode: smart` — یک مدل سریع/ارزان (haiku, flash, gpt-5-mini) تصمیم می‌گیرد آیا دستورات کم‌خطر به صورت خودکار تأیید شوند. مدل‌های گران‌قیمت در اینجا هدر دادن منابع است. |
| استخراج وب | وقتی زیاد از `web_extract` استفاده می‌کنید. همان منطق فشرده‌سازی — خلاصه‌سازی نیاز به استدلال ندارد. |
| Hub مهارت‌ها | `hermes skills search` از این استفاده می‌کند. معمولاً با `auto` خوب است. |
| MCP | مسیریابی ابزار MCP. معمولاً با `auto` خوب است. |
| مشخص‌کننده تریاژ | مشخص‌کننده تریاژ Kanban (`hermes kanban specify`) را مسیریابی می‌کند که یک خط تقریبی را به یک مشخصات مشخص تبدیل می‌کند. یک مدل ارزان و توانمند خوب عمل می‌کند. |
| تجزیه‌کننده Kanban | تجزیه وظیفه Kanban را مسیریابی می‌کند — یک وظیفه تریاژ را به یک گراف از وظایع فرعی برای پروفایل‌های متخصص تقسیم می‌کند. |
| توصیف‌کننده پروفایل | تولید توصیف پروفایل (`hermes profile describe --auto` / دکمه تولید خودکار داشبورد) را مسیریابی می‌کند. فراخوانی کوتاه و ارزان. |
| Curator | مرور استفاده از مهارت curator را مسیریابی می‌کند. می‌تواند در مدل‌های استدلالی دقایقی طول بکشد، بنابراین یک مدل کمکی ارزان‌تر اغلب ارزشمند است. |

`google/gemini-3-flash-preview`
`google/gemini-2.5-flash`
`gpt-4o-mini`
`approval_mode: smart`
`web_extract`
`hermes skills search`
`auto`
`auto`
`hermes kanban specify`
`hermes profile describe --auto`

### بازنویسی به ازای هر کار

روی هر ردیف کمکی **Change** کلیک کنید. همان انتخابگر باز می‌شود، همان رفتار — ارائه‌دهنده + مدل را انتخاب کنید، **Switch** بزنید. ردیف به جای `auto (use main model)` نمایش `provider · model` را به‌روز می‌کند.

`provider · model`
`auto (use main model)`

### بازنشانی همه به auto

اگر بیش از حد تنظیم کرده‌اید و می‌خواهید از نو شروع کنید، روی **Reset all to auto** در بالای بخش کمکی کلیک کنید. هر اسلات به استفاده از مدل اصلی شما بازمی‌گردد.

## میانبر «استفاده به عنوان»

هر کارت مدل در صفحه یک کشویی **Use as** دارد. این مسیر سریع است — مدلی را که در تحلیل‌های خود می‌بینید انتخاب کنید، روی **Use as** کلیک کنید و آن را به اسلات اصلی یا هر کار کمکی خاصی با یک کلیک اختصاص دهید:

کشویی شامل موارد زیر است:

- **مدل اصلی** — مشابه کلیک کردن Change در ردیف اصلی.
- **همه کارهای کمکی** — این مدل را به هر 11 اسلات کمکی به طور همزمان اختصاص می‌دهد. مفید وقتی فقط می‌خواهید هر کار جانبی روی یک مدل flash ارزان باشد.
- **گزینه‌های کاری منفرد** — بینایی، استخراج وب، فشرده‌سازی و غیره. مدل فعلی هر کار با `current` مشخص شده است.

`current`

کارت‌ها وقتی در حال حاضر به چیزی اختصاص داده شده‌اند با `main` یا `aux · <task>` نشان‌دار می‌شوند — بنابراین می‌توانید در یک نگاه ببینید کدام مدل‌های تاریخی شما کجا متصل هستند.

`main`
`aux · <task>`

## چه چیزی در config.yaml نوشته می‌شود

`config.yaml`

وقتی از طریق داشبورد ذخیره می‌کنید، Hermes در `~/.hermes/config.yaml` می‌نویسد:

`~/.hermes/config.yaml`

مدل اصلی:

```
model:
  provider: openrouter
  default: anthropic/claude-opus-4.7
  base_url: ''        # cleared on provider switch
  api_mode: chat_completions
```

بازنویسی کمکی (مثال — بینایی روی gemini-flash):

```
auxiliary:
  vision:
    provider: openrouter
    model: google/gemini-2.5-flash
    base_url: ''
    api_key: ''
    timeout: 120
    extra_body: {}
    download_timeout: 30
```

کمکی روی auto (پیش‌فرض):

```
auxiliary:
  compression:
    provider: auto
    model: ''
    base_url: ''
    # ... other fields unchanged
```

`provider: auto` با `model: ''` به Hermes می‌گوید از مدل اصلی برای آن کار استفاده کند، در حالی که همچنان سیاست فال‌بک را اگر مسیر اصلی نتواند فراخوانی کمکی را سرویس دهد رعایت می‌کند.

`provider: auto`
`model: ''`

زنجیره‌های فال‌بک مخصوص کار اختیاری در همان زیربخش کار کمکی قرار دارند:

```
auxiliary:
  title_generation:
    provider: auto
    model: ''
    fallback_chain:
      - provider: openrouter
        model: inclusionai/ring-2.6-1t:free
```

وقتی `fallback_chain` وجود ندارد، `auto` از زنجیره `fallback_providers` سطح بالا قبل از زنجیره کشف کمکی داخلی استفاده می‌کند.

`fallback_chain`
`auto`
`fallback_providers`

## چه زمانی اعمال می‌شود؟

- **CLI** (`hermes chat`): فراخوانی بعدی `hermes chat`.
- **Gateway** (Telegram, Discord, Slack و غیره): جلسه **جدید** بعدی. جلسات موجود مدل خود را حفظ می‌کنند. Gateway را ری‌استارت کنید (`hermes gateway restart`) اگر می‌خواهید همه جلسات تغییر را دریافت کنند.
- **تب چت داشبورد** (`/chat`): PTY جدید بعدی. چت باز فعلی مدل خود را حفظ می‌کند — از `/model` داخل آن برای تعویض فوری استفاده کنید.

`hermes chat`
`hermes chat`
`hermes gateway restart`
`/chat`
`/model`

تغییرات هرگز کش‌های prompt را در جلسات در حال اجرا باطل نمی‌کنند. این عمدی است: تعویض مدل اصلی داخل یک جلسه نیازمند بازنشانی کش است (پرامپت سیستم حاوی محتوای مخصوص مدل است) و ما آن را برای دستور اسلش `/model` صریح داخل چت رزرو کرده‌ایم.

`/model`

## عیب‌یابی

### «ارائه‌دهندگان احراز هویت‌شده‌ای وجود ندارند» در انتخابگر

Hermes فقط ارائه‌دهنده‌ای را فهرست می‌کند که دارای اعتبار کاری باشد. **Keys** را در نوار کناری بررسی کنید — باید یکی از موارد زیر را ببینید: کلید API، OAuth موفق، یا آدرس endpoint سفارشی. اگر ارائه‌دهنده مورد نظر شما وجود ندارد، `hermes setup` را اجرا کنید یا به **Keys** بروید و متغیر env را اضافه کنید.

`hermes setup`

### مدل اصلی در چت در حال اجرای من تغییر نکرد

طبیعی است. داشبورد `config.yaml` را می‌نویسد که جلسات جدید آن را می‌خوانند. چت باز فعلی یک فرایند عامل زنده است — هر مدلی که با آن ایجاد شده حفظ می‌شود. از `/model <name>` داخل چت برای تعویض آن جلسه خاص استفاده کنید.

`config.yaml`
`/model <name>`

### بازنویسی کمکی «اعمال نشد»

سه مورد برای بررسی:

1. **آیا جلسه جدیدی شروع کردید؟** چت‌های موجود مجدداً پیکربندی را نمی‌خوانند.
2. **آیا `provider` روی چیزی غیر از `auto` تنظیم شده؟** اگر فیلد `auto` نشان می‌دهد، کار هنوز از مدل اصلی شما استفاده می‌کند. **Change** را کلیک کنید و یک ارائه‌دهنده واقعی انتخاب کنید.
3. **آیا ارائه‌دهنده احراز هویت شده؟** اگر `minimax` را به یک کار اختصاص داده‌اید اما کلید API MiniMax ندارید، آن کار به پیش‌فرض openrouter فال‌بک می‌کند و یک هشدار در `agent.log` ثبت می‌کند.

`provider`
`auto`
`auto`
`minimax`
`agent.log`

### مدلی انتخاب کردم اما Hermes ارائه‌دهنده را تغییر داد

در OpenRouter (یا هر aggregator)، نام‌های خالی مدل ابتدا **داخل** aggregator حل می‌شوند. بنابراین `claude-sonnet-4` در OpenRouter به `anthropic/claude-sonnet-4.6` تبدیل می‌شود و روی احراز هویت OpenRouter شما باقی می‌ماند. اما اگر `claude-sonnet-4` را روی احراز هویت بومی Anthropic تایپ کنید، به عنوان `claude-sonnet-4-6` باقی می‌ماند. اگر تغییر ارائه‌دهنده غیرمنتظره‌ای می‌بینید، بررسی کنید ارائه‌دهنده فعلی شما همانی باشد که انتظار دارید — انتخابگر همیشه مدل اصلی فعلی را در بالای محاوره نشان می‌دهد.

`claude-sonnet-4`
`anthropic/claude-sonnet-4.6`
`claude-sonnet-4`
`claude-sonnet-4-6`

## روش‌های جایگزین

### دستور اسلش CLI

داخل هر نشست `hermes chat`:

`hermes chat`

```
/model gpt-5.4 --provider openrouter             # session-only
/model gpt-5.4 --provider openrouter --global    # also persists to config.yaml
```

`--global` همان کاری را انجام می‌دهد که دکمه **Change** داشبورد انجام می‌دهد، به علاوه جلسه در حال اجرا را به صورت درجا تعویض می‌کند.

`--global`

### نام‌های مستعار سفارشی

نام‌های کوتاه خود را برای مدل‌هایی که زیاد استفاده می‌کنید تعریف کنید، سپس از `/model <alias>` در CLI یا هر پلتفرم پیام‌رسانی استفاده کنید. دو فرمت معادل وجود دارد — هر کدام که با گردش کار شما سازگارتر است را انتخاب کنید.

`/model <alias>`

فرمت استاندارد (سطح بالا `model_aliases:`) — کنترل کامل روی provider + base_url:

`model_aliases:`

```
# ~/.hermes/config.yaml
model_aliases:
  fav:
    model: claude-sonnet-4.6
    provider: anthropic
  grok:
    model: grok-4
    provider: x-ai
```

فرمت رشته کوتاه (`model.aliases.<name>: provider/model`) — راحت از shell چون `hermes config set` فقط مقادیر scalar می‌نویسد، اما نمی‌تواند `base_url` سفارشی را حمل کند:

`model.aliases.<name>: provider/model`
`hermes config set`
`base_url`

```
hermes config set model.aliases.fav anthropic/claude-opus-4.6
hermes config set model.aliases.grok x-ai/grok-4
```

هر دو مسیر به همان لودر (`hermes_cli/model_switch.py`) تغذیه می‌شوند. موارد اعلام‌شده در `model_aliases:` بر `model.aliases:` با همان نام اولویت دارند.

`hermes_cli/model_switch.py`
`model_aliases:`
`model.aliases:`

سپس `/model fav` یا `/model grok` در چت. نام‌های مستعار کاربر، نام‌های کوتاه داخلی (sonnet, kimi, opus و غیره) را سایه می‌زنند. به [نام‌های مستعار مدل سفارشی](/docs/reference/slash-commands#custom-model-aliases) برای مرجع کامل مراجعه کنید.

`/model fav`
`/model grok`
`sonnet`
`kimi`
`opus`
[نام‌های مستعار مدل سفارشی](/docs/reference/slash-commands#custom-model-aliases)

### زیردستور `hermes model`

`hermes model`

```
hermes model            # Interactive provider + model picker (the canonical way to switch defaults)
```

`hermes model` شما را در انتخاب ارائه‌دهنده، احراز هویت (جریان‌های OAuth مرورگر را باز می‌کنند؛ ارائه‌دهندگان کلید API کلید را درخواست می‌کنند) و سپس انتخاب یک مدل خاص از فهرست گلچین‌شده آن ارائه‌دهنده راهنمایی می‌کند. انتخاب در `model.provider` و `model.model` در `~/.hermes/config.yaml` نوشته می‌شود.

`hermes model`
`model.provider`
`model.model`
`~/.hermes/config.yaml`

برای فهرست کردن ارائه‌دهندگان/مدل‌ها بدون راه‌اندازی انتخابگر، از داشبورد یا endpoint‌های REST زیر استفاده کنید. برای بررسی اینکه CLI در حال حاضر چه چیزی واقعاً استفاده می‌کند: `hermes config show | grep '^model\.'` و `hermes status`.

`hermes config show | grep '^model\.'`
`hermes status`

### ویرایش مستقیم پیکربندی

`~/.hermes/config.yaml` را ویرایش کنید و هر چیزی که آن را می‌خواند ری‌استارت کنید. به [مرجع پیکربندی](/docs/user-guide/configuration) برای کل schema مراجعه کنید.

`~/.hermes/config.yaml`
[مرجع پیکربندی](/docs/user-guide/configuration)

### REST API

داشبورد از سه endpoint استفاده می‌کند. مفید برای اسکریپت‌نویسی:

```
# List authenticated providers + curated model lists
curl -H "X-Hermes-Session-Token: $TOKEN" http://localhost:PORT/api/model/options

# Read current main + auxiliary assignments
curl -H "X-Hermes-Session-Token: $TOKEN" http://localhost:PORT/api/model/auxiliary

# Set the main model
curl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \
  -d '{"scope":"main","provider":"openrouter","model":"anthropic/claude-opus-4.7"}' \
  http://localhost:PORT/api/model/set

# Override a single auxiliary task
curl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \
  -d '{"scope":"auxiliary","task":"vision","provider":"openrouter","model":"google/gemini-2.5-flash"}' \
  http://localhost:PORT/api/model/set

# Assign one model to every auxiliary task
curl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \
  -d '{"scope":"auxiliary","task":"","provider":"openrouter","model":"google/gemini-2.5-flash"}' \
  http://localhost:PORT/api/model/set

# Reset all auxiliary tasks to auto
curl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \
  -d '{"scope":"auxiliary","task":"__reset__","provider":"","model":""}' \
  http://localhost:PORT/api/model/set
```

توکن جلسه در HTML داشبورد در شروع تزریق می‌شود و با هر ری‌استارت سرور چرخش می‌کند. آن را از ابزارهای توسعه‌دهنده مرورگر (`window.__HERMES_SESSION_TOKEN__`) بگیرید اگر علیه داشبورد در حال اجرا اسکریپت می‌نویسید.

`window.__HERMES_SESSION_TOKEN__`
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/configuring-models.md)