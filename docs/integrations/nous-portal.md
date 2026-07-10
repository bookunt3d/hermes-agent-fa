---
layout: docs
title: "Nous Portal"
permalink: /docs/integrations/nous-portal/
---

- 
- Integrations
- Nous Portal

# Nous Portal

Nous Portal دروازه اشتراک یکپارچه Nous Research و روش توصیه‌شده برای اجرای Hermes Agent است. یک ورود OAuth جایگزین مدیریت حساب‌ها، کلیدهای API و روابط صورتحساب جداگانه در هر آزمایشگاه مدل، API جستجو، مولد تصویر و ارائه‌دهنده مرورگر می‌شود که در غیر این صورت باید آنها را به صورت دستی پیکربندی کنید.

[Nous Portal](https://portal.nousresearch.com)

اگر فقط وقت راه‌اندازی یک چیز را دارید، این را راه‌اندازی کنید. سریع‌ترین مسیر:

```
hermes setup --portal
```

این دستور واحد، OAuth Portal را اجرا می‌کند، به شما امکان انتخاب یک مدل Nous را می‌دهد، Nous را به عنوان ارائه‌دهنده استنتاج در config.yaml تنظیم می‌کند و دروازه ابزار را فعال می‌کند. بلافاصله پس از آن آماده `hermes chat` هستید.

`config.yaml`
`hermes chat`

هنوز اشتراک ندارید؟ `portal.nousresearch.com/manage-subscription` — ثبت نام کنید، سپس برگردید و دستور بالا را اجرا کنید.

[portal.nousresearch.com/manage-subscription](https://portal.nousresearch.com/manage-subscription)

## چه چیزی در اشتراک وجود دارد

### ۳۰۰+ مدل پیشرو، یک صورتحساب

Portal یک کاتالوگ گزینش‌شده از مدل‌های agent محور از سراسر اکوسیستم را پراکسی می‌کند — صورتحساب بر اساس اشتراک Nous شما به جای یک موجودی اعتباری به ازای هر آزمایشگاه.

| خانواده | مدل‌ها |
| --- | --- |
| Anthropic Claude | Opus 4.7، Opus 4.6، Sonnet 4.6، Haiku 4.5 |
| OpenAI | GPT-5.5، GPT-5.5 Pro، GPT-5.4 Mini، GPT-5.4 Nano، GPT-5.3 Codex |
| Google Gemini | Gemini 3 Pro Preview، Gemini 3 Flash Preview، Gemini 3.1 Pro Preview، Gemini 3.1 Flash Lite Preview |
| DeepSeek | DeepSeek V4 Pro |
| Qwen | Qwen3.7-Max، Qwen3.6-35B-A3B |
| Kimi / Moonshot | Kimi K2.6 |
| GLM / Zhipu | GLM-5.1 |
| MiniMax | MiniMax M2.7 |
| xAI | Grok 4.3 |
| NVIDIA | Nemotron-3 Super 120B-A12B |
| Tencent | Hunyuan 3 Preview |
| Xiaomi | MiMo V2.5 Pro |
| StepFun | Step 3.5 Flash |
| Hermes | Hermes-4-70B، Hermes-4-405b (چت، به یادداشت زیر مراجعه کنید) |
| + همه موارد دیگر | ۲۰۰+ مدل اضافی — کامل‌ترین مرز agent محور |

مسیریابی از طریق OpenRouter در زیرساخت انجام می‌شود، بنابراین در دسترس بودن مدل و رفتار failover مشابه آنچه با یک کلید OpenRouter دریافت می‌کنید است — فقط به جای آن، بر اساس اشتراک Nous شما صورتحساب می‌شود. بین Claude Sonnet 4.6 برای کد و Gemini 3 Pro برای context طولانی با `/model` در وسط نشست سوئیچ کنید — بدون اعتبارنامه جدید، بدون شارژ مجدد، بدون خطای تعجب‌آور صفر موجودی.

`/model`

### دروازه ابزار Nous

همین اشتراک دروازه ابزار را باز می‌کند که فراخوانی‌های ابزار Hermes Agent را از طریق زیرساخت مدیریت‌شده Nous مسیریابی می‌کند. پنج پشتیبان، یک ورود:

[دروازه ابزار](/docs/user-guide/features/tool-gateway)

| ابزار | شریک | عملکرد |
| --- | --- | --- |
| جستجو و استخراج وب | Firecrawl | جستجو در سطح agent و استخراج صفحه کامل. بدون کلید API Firecrawl، بدون نظارت نرخ. |
| تولید تصویر | FAL | نه مدل در زیر یک endpoint: FLUX 2 Klein 9B، FLUX 2 Pro، Z-Image Turbo، Nano Banana Pro (Gemini 3 Pro Image)، GPT Image 1.5، GPT Image 2، Ideogram V3، Recraft V4 Pro، Qwen Image. |
| تبدیل متن به گفتار | OpenAI TTS | TTS با کیفیت بالا بدون کلید OpenAI جداگانه. حالت صوتی را در پلتفرم‌های پیام‌رسانی فعال می‌کند. |
| اتوماسیون مرورگر ابری | Browser Use | نشست‌های headless Chromium برای `browser_navigate`، `browser_click`، `browser_type`، `browser_vision`. بدون نیاز به حساب Browserbase. |
| sandbox ترمینال ابری | Modal | sandboxهای ترمینال بدون سرور برای اجرای کد (افزودنی اختیاری). |

[حالت صوتی](/docs/user-guide/features/voice-mode)
`browser_navigate`
`browser_click`
`browser_type`
`browser_vision`

بدون دروازه، راه‌اندازی هر یک از این موارد به معنای یک حساب Firecrawl، یک حساب FAL، یک حساب Browser Use، یک کلید OpenAI و یک حساب Modal است — پنج ثبت‌نام جداگانه، پنج داشبورد جداگانه، پنج فرآیند شارژ جداگانه. با دروازه، همه چیز از طریق یک اشتراک مسیریابی می‌شود.

همچنین می‌توانید فقط ابزارهای خاص دروازه را فعال کنید (مثلاً جستجوی وب اما نه تولید تصویر) — ترکیب دروازه با پشتیبان‌های خودتان را در زیر ببینید.

### Nous Chat

حساب Portal شما `chat.nousresearch.com` — رابط چت وب Nous Research با همان کاتالوگ مدل — را نمی‌پوشاند. هنگامی که از ترمینال دور هستید یا برای کار چت غیر agent مفید است.

[chat.nousresearch.com](https://chat.nousresearch.com)

### بدون اعتبارنامه در dotfiles شما

چون همه چیز از طریق یک نشست Portal احراز هویت‌شده با OAuth مسیریابی می‌شود، یک فایل `.env` با ده‌ها کلید API بلندمدت جمع نمی‌کنید. رفرش توکن در `~/.hermes/auth.json` تنها اعتبارنامه روی دیسک است و Hermes JWTهای کوتاه‌مدت را از آن به ازای هر درخوات ضرب می‌کند — مدیریت توکن در زیر را ببینید.

`.env`
`~/.hermes/auth.json`

### تطابق بین پلتفرمی

ویندوز بومی نصب کلید API به ازای هر ابزار را سخت‌ترین بخش راه‌اندازی یک agent مفید می‌داند — نصب حساب Firecrawl، حساب FAL، حساب Browser Use، کلید OpenAI از ویندوز بخش با اصطکاک زیاد دریافت یک agent کاربردی است. اشتراک Portal این مشکل را برطرف می‌کند: یک OAuth مدل و هر ابزار دروازه را پوشش می‌دهد، بنابراین کاربران ویندوز همان تجربه macOS/Linux را بدون پیکربندی دستی چهار پشتیبان دریافت می‌کنند.

[ویندوز بومی](/docs/user-guide/windows-native)

## یادداشتی درباره Hermes 4

خانواده Hermes 4 خود Nous Research (Hermes-4-70B، Hermes-4-405b) از طریق Portal با نرخ‌های تخفیف‌خورده در دسترس است. اینها مدل‌های چت ترکیبی پیشرو هستند — قوی در ریاضیات، علوم، پیگیری دستورات، پایبندی به schema، نقش‌آفرینی و نوشتار بلند.

با این حال، استفاده از آنها در داخل Hermes Agent توصیه نمی‌شود. Hermes 4 برای چت و استدلال بهینه شده است، نه حلقه فراخوانی ابزار سریعی که agent به آن وابسته است. از آنها برای Nous Chat، workflowهای تحقیقاتی یا از طریق پراکسی اشتراکی از ابزارهای دیگر استفاده کنید — اما برای کار agent، یک مدل پیشرو agent محور از کاتالوگ انتخاب کنید:

[Nous Chat](https://chat.nousresearch.com)
[پراکسی اشتراکی](/docs/user-guide/features/subscription-proxy)

```
/model anthropic/claude-sonnet-4.6     # بهترین مدل agent محور همه‌کاره/model openai/gpt-5.5-pro              # استدلال قوی + فراخوانی ابزار/model google/gemini-3-pro-preview     # پنجره context عظیم/model deepseek/deepseek-v4-pro        # برنامه‌نویس مقرون به صرفه
```

صفحه اطلاعات مدل خود Portal همین هشدار را دارد، بنابراین این یک نظر از سوی Hermes نیست — این رهنمود رسمی Nous Research است.

[صفحه اطلاعات مدل](https://portal.nousresearch.com/info)

## راه‌اندازی

### نصب تازه — یک دستور

```
hermes setup --portal
```

این راه‌اندازی کامل را در یک مرحله انجام می‌دهد:

1. مرورگر شما را به portal.nousresearch.com برای ورود OAuth باز می‌کند
2. رفرش توکن را در `~/.hermes/auth.json` ذخیره می‌کند
3. به شما امکان انتخاب یک مدل Nous از لیست گزینش‌شده را می‌دهد (یا رد شوید تا مدل فعلی خود را حفظ کنید)
4. Nous را به عنوان ارائه‌دهنده استنتاج در `~/.hermes/config.yaml` تنظیم می‌کند (وقتی مدل انتخاب می‌کنید)
5. دروازه ابزار را فعال می‌کند (وب، تصویر، TTS، مسیریابی مرورگر)
6. به ترمینال شما بازمی‌گرداند و آماده `hermes chat` هستید

`~/.hermes/auth.json`
`~/.hermes/config.yaml`
`hermes chat`

اگر هنوز اشتراک ندارید، ابتدا در portal.nousresearch.com/manage-subscription ثبت نام کنید.

[portal.nousresearch.com/manage-subscription](https://portal.nousresearch.com/manage-subscription)

### نصب موجود — اضافه کردن Portal در کنار ارائه‌دهندگان دیگر

اگر Hermes را قبلاً با OpenRouter، Anthropic یا هر ارائه‌دهنده دیگری پیکربندی کرده‌اید و می‌خواهید Portal را در کنار آنها اضافه کنید:

```
hermes model# «Nous Portal» را از لیست ارائه‌دهندگان انتخاب کنید# مرورگر باز می‌شود، وارد شوید، تمام
```

ارائه‌دهندگان موجود شما پیکربندی باقی می‌مانند. می‌توانید با `/model` در وسط نشست یا `hermes model` بین نشست‌ها بین آنها سوئیچ کنید — Portal یکی از ارائه‌دهندگان موجود شما می‌شود، نه تنها یکی.

`/model`
`hermes model`

### راه‌اندازی headless / SSH / راه دور

OAuth به یک مرورگر نیاز دارد، اما callback حلقه‌ای روی ماشینی اجرا می‌شود که Hermes روی آن اجرا می‌شود. برای میزبان‌های راه دور، به OAuth از طریق SSH / میزبان‌های راه دور مراجعه کنید — همان الگوها برای Portal و هر ارائه‌دهنده مبتنی بر OAuth دیگر کار می‌کنند (forwarding پورت `ssh -L`).

[OAuth از طریق SSH / میزبان‌های راه دور](/docs/guides/oauth-over-ssh)
`ssh -L`

### راه‌اندازی نشست (Profile)

اگر از نشست‌های Hermes استفاده می‌کنید، رفرش توکن Portal به صورت خودکار از طریق فروشگاه توکن مشترک در تمام نشست‌ها به اشتراک گذاشته می‌شود. یک بار در هر نشست وارد شوید و بقیه به صورت خودکار آن را دریافت می‌کنند — نیازی به تکرار فرآیند OAuth برای هر نشست نیست.

[نشست‌های Hermes](/docs/user-guide/profiles)

## استفاده روزمره از Portal

### بررسی اتصالات

```
hermes portal            # ورود به Nous Portal + راه‌اندازی (راه‌اندازی یک‌باره)hermes portal info       # وضعیت ورود، اطلاعات اشتراک، مسیریابی مدل + دروازهhermes portal status     # مستعار portal infohermes portal tools      # کاتالوگ کامل دروازه ابزار با مسیریابی به ازای هر ابزارhermes portal open       # باز کردن صفحه مدیریت اشتراک در مرورگر شما
```

`hermes portal` (بدون زیردستور) مستعار خوانا برای `hermes auth add nous --type oauth` است — شما را وارد می‌کند، به شما امکان انتخاب یک مدل Nous را می‌دهد، Nous را به عنوان ارائه‌دهنده استنتاج شما تنظیم می‌کند و دروازه ابزار را پیشنهاد می‌کند (مشابه `hermes setup --portal` و همان جریان Nous برای راه‌اندازی سریع اولیه).

`hermes portal`
`hermes auth add nous --type oauth`
`hermes setup --portal`

`hermes portal info` نمای کلی سطح بالا را به شما می‌دهد:

`hermes portal info`

```
  Nous Portal  ───────────  Auth:    ✓ logged in  Portal:  https://portal.nousresearch.com  Model:   ✓ using Nous as inference provider  Tool Gateway  ────────────  Web search & extract  via Nous Portal  Image generation      via Nous Portal  Text-to-speech        via Nous Portal  Browser automation    via Nous Portal  Cloud terminal        not configured
```

### سوئیچ مدل‌ها

در داخل یک نشست:

```
/model anthropic/claude-sonnet-4.6/model openai/gpt-5.5-pro/model google/gemini-3-pro-preview
```

یا انتخابگر را باز کنید:

```
/model# کلیدهای جهت‌دار، Enter برای انتخاب
```

خارج از نشست (Wizard راه‌اندازی کامل، مفید هنگام اضافه کردن ارائه‌دهنده جدید):

```
hermes model
```

### ترکیب دروازه با پشتیبان‌های خودتان

اگر مثلاً یک حساب Browserbase دارید و می‌خواهید به استفاده از آن ادامه دهید در حالی که جستجوی وب و تولید تصویر را از طریق Nous مسیریابی می‌کنید، این پشتیبانی می‌شود. از `hermes tools` برای انتخاب پشتیبان‌ها به ازای هر ابزار استفاده کنید:

`hermes tools`

```
hermes tools# → جستجوی وب       → «Nous Subscription»# → تولید تصویر   → «Nous Subscription»# → مرورگر          → «Browserbase»  (کلید موجود شما)# → TTS              → «Nous Subscription»
```

دروازه ابزار اختیاری به ازای هر ابزار است، نه همه یا هیچ. پشتیبان‌های مدیریت‌شده در `hermes tools` ظاهر می‌شوند چه به Nous Portal وارد شده باشید چه نه — اگر «Nous Subscription» را قبل از احراز هویت انتخاب کنید، Hermes ورود Portal را به صورت درون‌خطی اجرا می‌کند (ارائه‌دهنده استنتاج شما را تغییر نمی‌دهد یا به ابزارهای دیگر شما دست نمی‌زند). برای ماتریس پیکربندی کامل به ازای هر ابزار، به اسناد دروازه ابزار مراجعه کنید.

`hermes tools`
[اسناد دروازه ابزار](/docs/user-guide/features/tool-gateway)

### مدیریت اشتراک

طرح، مصرف یا ارتقا/لغو اشتراک خود را در هر زمان مدیریت کنید:

- وب: portal.nousresearch.com/manage-subscription
- میانبر CLI: `hermes portal open` (همان صفحه را در مرورگر پیش‌فرض شما باز می‌کند)

[portal.nousresearch.com/manage-subscription](https://portal.nousresearch.com/manage-subscription)
`hermes portal open`

## مرجع پیکربندی

پس از `hermes setup --portal`، `~/.hermes/config.yaml` به این شکل خواهد بود:

`hermes setup --portal`
`~/.hermes/config.yaml`

```
model:  provider: nous  default: anthropic/claude-sonnet-4.6     # یا هر مدلی که انتخاب کرده‌اید  base_url: https://inference-api.nousresearch.com/v1
```

تنظیمات دروازه ابزار در بخش‌های ابزار مربوطه زیر قرار دارد:

```
web:  backend: nous       # جستجو/استخراج وب از طریق دروازه ابزار مسیریابی می‌شودimage_gen:  provider: noustts:  provider: nousbrowser:  backend: nous
```

توکن رفرش OAuth به صورت جداگانه در `~/.hermes/auth.json` ذخیره می‌شود (نه در config.yaml — اعتبارنامه‌ها و پیکربندی طراحی‌شده جداگانه نگه داشته می‌شوند).

`~/.hermes/auth.json`
`config.yaml`

## مدیریت توکن

Hermes در هر فراخوانی استنتاج، یک JWT کوتاه‌مدت از توکن رفرش ذخیره‌شده Portal شما ضرب می‌کند به جای استفاده مجدد از یک کلید API بلندمدت. چرخه حیات توکن کاملاً خودکار است — رفرش، ضرب، تلاش مجدد در 401 گذرا — و شما هرگز آن را نمی‌بینید.

اگر Portal توکن رفرش را باطل کند (تغییر رمز عبور، لغو دستی، انقضای نشست)، توکن رفرش باطل به صورت محلی قرنطینه می‌شود تا Hermes از ارسال مجدد آن دست بردارد و شما جریانی از 401های یکسان نبینید. فراخوانی بعدی پیام واضح «احراز هویت مجدد لازم است» را نشان می‌دهد. `hermes auth add nous` را اجرا کنید تا دوباره وارد شوید؛ قرنطینه در اولین ورود موفق پاک می‌شود.

`hermes auth add nous`

## عیب‌یابی

### `hermes portal info` نشان می‌دهد «وارد نشده‌اید»

`hermes portal info`

شما فرآیند OAuth را تکمیل نکرده‌اید یا توکن رفرش شما پاک شده است. اجرا کنید:

```
hermes portal
```

یا از `hermes model` استفاده کنید و دوباره Nous Portal را انتخاب کنید.

`hermes model`

### پیام «احراز هویت مجدد لازم است» در وسط نشست دریافت کردید

توکن رفرش Portal شما باطل شده است (تغییر رمز عبور، لغو دستی یا انقضای نشست). `hermes auth add nous` را اجرا کنید و درخواست بعدی از اعتبارنامه‌های جدید استفاده می‌کند. هر قرنطینه روی توکن قدیمی به طور خودکار در ورود مجدد موفق پاک می‌شود.

`hermes auth add nous`

### می‌خواهید از یک مدل خاص ارائه‌دهنده استفاده کنید که Portal نمایش نمی‌دهد

Portal از طریق OpenRouter پراکسی می‌کند، بنابراین هر مدلی که OpenRouter پشتیبانی می‌کند به طور کلی در دسترس است. اگر یک مدل خاص در `/model` ظاهر نمی‌شود، slug سبک OpenRouter را مستقیماً امتحان کنید:

`/model`

```
/model anthropic/claude-opus-4.6
```

اگر واقعاً مدلی وجود ندارد، issue باز کنید — ما کاتالوگ Portal را برای Hermes باز می‌کنیم و شکاف‌ها معمولاً به معنای یک پیکربندی مسیریابی است که می‌توانیم به‌روزرسانی کنیم.

[issue باز کنید](https://github.com/NousResearch/hermes-agent/issues)

### صورتحساب‌ها در حساب Portal من ظاهر نمی‌شوند

ابتدا `hermes portal info` را بررسی کنید — اگر نشان دهد از ارائه‌دهنده دیگری استفاده می‌کنید (`Model: currently openrouter` به جای `using Nous as inference provider`)، پیکربندی محلی شما تغییر کرده است. `hermes model` را اجرا کنید، Nous Portal را انتخاب کنید و درخواست بعدی از طریق اشتراک شما مسیریابی می‌شود.

`hermes portal info`
`Model: currently openrouter`
`using Nous as inference provider`
`hermes model`

## مشاهده همچنین

- دروازه ابزار — جزئیات کامل درباره هر ابزار دروازه، پیکربندی به ازای هر ابزار و قیمت‌گذاری
- پراکسی اشتراکی — از اشتراک Portal خود در ابزارهای غیر Hermes استفاده کنید (agentهای دیگر، اسکریپت‌ها، کلاینت‌های شخص ثالث)
- حالت صوتی — مکالمات صوتی با استفاده از TTS OpenAI Portal
- ارائه‌دهندگان AI — کاتالوگ کامل ارائه‌دهندگان اگر می‌خواهید جایگزین‌ها را مقایسه کنید
- OAuth از طریق SSH — ورود از میزبان‌های راه دور یا محیط‌های فقط مرورگر
- نشست‌ها — پیکربندی‌های چند Hermes که یک ورود Portal را به اشتراک می‌گذارند

[دروازه ابزار](/docs/user-guide/features/tool-gateway)
[پراکسی اشتراکی](/docs/user-guide/features/subscription-proxy)
[حالت صوتی](/docs/user-guide/features/voice-mode)
[ارائه‌دهندگان AI](/docs/integrations/providers)
[OAuth از طریق SSH](/docs/guides/oauth-over-ssh)
[نشست‌ها](/docs/user-guide/profiles)
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/integrations/nous-portal.md)
