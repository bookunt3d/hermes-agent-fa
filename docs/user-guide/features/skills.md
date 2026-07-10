---
layout: docs
title: "مهارت‌ها"
permalink: /docs/user-guide/features/skills/
---

- 
- امکانات
- هسته
- سیستم مهارت‌ها

# سیستم مهارت‌ها

مهارت‌ها اسناد دانشی هستند که agent می‌تواند در صورت نیاز بارگذاری کند. آنها از الگوی افشای تدریجی (progressive disclosure) پیروی می‌کنند تا مصرف توکن را به حداقل برسانند و با استاندارد باز agentskills.io سازگار هستند.

[agentskills.io](https://agentskills.io/specification)

همه مهارت‌ها در `~/.hermes/skills/` زندگی می‌کنند — دایرکتوری اصلی و منبع حقیقت. در نصب تازه، مهارت‌های bundled از مخزن کپی می‌شوند. مهارت‌های نصب‌شده از Hub و مهارت‌های ایجادشده توسط agent نیز اینجا قرار می‌گیرند. agent می‌تواند هر مهارتی را تغییر دهد یا حذف کند.

`~/.hermes/skills/`

همچنین می‌توانید Hermes را به **دایرکتوری‌های مهارت خارجی** اشاره دهید — پوشه‌های اضافی که در کنار پوشه محلی اسکن می‌شوند. بخش «دایرکتوری‌های مهارت خارجی» در زیر را ببینید.

همچنین ببینید:

- فهرست مهارت‌های Bundled
- فهرست رسمی مهارت‌های اختیاری

[فهرست مهارت‌های Bundled](/docs/reference/skills-catalog)
[فهرست رسمی مهارت‌های اختیاری](/docs/reference/optional-skills-catalog)

## شروع از صفحه خالی

به طور پیش‌فرض هر پروفایل با فهرست مهارت‌های bundled کاشته می‌شود و هر `hermes update` مهارت‌های bundled جدید را اضافه می‌کند. اگر می‌خواهید پروفایلی **بدون مهارت‌های bundled** داشته باشید — و در به‌روزرسانی‌ها خالی بماند — دو مسیر دارید:

`hermes update`

در زمان نصب (اعمال به پروفایل پیش‌فرض `~/.hermes`):

`~/.hermes`

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --no-skills
```

در زمان ایجاد پروفایل (پروفایل‌های نام‌گذاری‌شده):

```
hermes profile create research --no-skills
```

روی یک پروفایل از قبل نصب‌شده (پیش‌فرض یا نام‌گذاری‌شده)، در زمان اجرا تغییر دهید:

```
hermes skills opt-out            # stop future seeding — nothing on disk is touched
hermes skills opt-out --remove   # also delete UNMODIFIED bundled skills (confirms first)
hermes skills opt-in --sync      # undo: remove the marker and re-seed now
```

هر سه مسیر یک نشانگر `.no-bundled-skills` در دایرکتوری پروفایل می‌نویسند. تا زمانی که این نشانگر وجود دارد، نصب‌کننده، `hermes update` و هر همگام‌سازی مهارت، کاشت مهارت‌های bundled را برای آن پروفایل رد می‌کنند. نشانگر را حذف کنید (یا `hermes skills opt-in` اجرا کنید) تا دوباره فعال شود.

`.no-bundled-skills`
`hermes update`
`hermes skills opt-in`

`hermes skills opt-out` فقط کاشت **آینده** را متوقف می‌کند — هیچ چیز موجود روی دیسک را حذف نمی‌کند. پرچم اختیاری `--remove` فقط مهارت‌های bundled **تغییر نیافته** (بایت‌به‌بایت یکسان با نسخه‌ای که Hermes نصب کرده) را حذف می‌کند. مهارت‌هایی که ویرایش کرده‌اید، مهارت‌های نصب‌شده از Hub و مهارت‌هایی که خودتان نوشته‌اید همیشه حفظ می‌شوند.

`hermes skills opt-out`
`--remove`

## استفاده از مهارت‌ها

هر مهارت نصب‌شده به طور خودکار به عنوان یک دستور slash در دسترس است:

```
# In the CLI or any messaging platform:
/gif-search funny cats
/axolotl help me fine-tune Llama 3 on my dataset
/github-pr-workflow create a PR for the auth refactor
/plan design a rollout for migrating our auth provider

# Just the skill name loads it and lets the agent ask what you need:
/excalidraw
```

### انباشتن چندین مهارت در یک دستور

می‌توانید چندین مهارت را در یک پیام با زنجیره کردن دستورات slash در ابتدای آن فراخوانی کنید — هر توکن `/skill` پیشرو (حداکثر ۵ عدد) بارگذاری می‌شود و بقیه به عنوان دستورالعمل شما عمل می‌کند:

`/skill`

```
/github-pr-workflow /test-driven-development fix issue #123 and open a PR
```

تحلیل در اولین توکنی که مهارت نصب‌شده نیست متوقف می‌شود، بنابراین آرگومان‌هایی که اتفاقی با `/` شروع می‌شوند (مانند مسیر فایل) هرگز بلعیده نمی‌شوند:

`/`

```
/ocr-and-documents /tmp/scan.pdf extract the tables   # loads one skill; /tmp/scan.pdf is the argument
```

برای ترکیب‌هایی که مکرراً استفاده می‌کنید، یک **بسته مهارت (skill bundle)** ترجیح دهید —
همان اثر را با یک دستور کوتاه‌تر دارد.

مهارت bundled `plan` مثال خوبی است. اجرای `/plan [request]` دستورالعمل‌های مهارت را بارگذاری می‌کند و به Hermes می‌گوید در صورت نیاز زمینه را بررسی کند، به جای اجرای وظیفه یک طرح اجرایی markdown بنویسد و نتیجه را در `.hermes/plans/` نسبت به دایرکتوری کاری فعال/backend ذخیره کند.

`plan`
`/plan [request]`
`.hermes/plans/`

همچنین می‌توانید از طریق مکالمه طبیعی با مهارت‌ها تعامل کنید:

```
hermes chat --toolsets skills -q "What skills do you have?"
hermes chat --toolsets skills -q "Show me the axolotl skill"
```

## یادگیری یک مهارت از منابع (/learn)

`/learn`

`/learn` سریع‌ترین راه برای تبدیل چیزی که از قبل می‌دانید — یا انبوهی از مواد مرجع — به یک مهارت قابل استفاده مجدد، بدون نوشتن دستی `SKILL.md` است. این ابزار بی‌پایان است: هر چیزی که بتوانید توصیف کنید را به آن نشان دهید و agent مواد را با ابزارهایی که از قبل دارد جمع‌آوری می‌کند، سپس مهارتی می‌نویسد که از **استانداردهای تألیف خانگی** پیروی می‌کند (توصیف ≤۶۰ کاراکتر، ترتیب استاندارد بخش‌ها، چارچوب‌بندی ابزارهای Hermes، بدون دستورات اختراعی).

`/learn`
`SKILL.md`

```
# A local SDK or doc directory — read with read_file / search_files
/learn the REST client in ~/projects/acme-sdk, focus on auth + pagination

# An online doc page — fetched with web_extract
/learn https://docs.example.com/api/quickstart

# The workflow you just walked the agent through in this conversation
/learn how I just deployed the staging server

# Pasted notes / a described procedure
/learn filing an expense: open the portal, New > Expense, attach the receipt, submit
```

از آنجا که agent زنده خود منبع‌یابی را انجام می‌دهد، `/learn` به یک شکل در CLI، دروازه پیام‌رسانی، TUI و داشبورد کار می‌کند — و روی هر backend ترمینالی (محلی، Docker، راه دور)، زیرا موتور ingestion جداگانه‌ای وجود ندارد. در داشبورد، صفحه Skills دکمه‌ای «یادگیری یک مهارت» دارد که پنلی با فیلد دایرکتوری، فیلد URL و جعبه متن بی‌پایان باز می‌کند؛ درخواست `/learn` را ترکیب کرده و در چت اجرا می‌کند.

`/learn`
`/learn`

هیچ ردپای ابزار-مدلی وجود ندارد: `/learn` یک پرامپت راهنمای استاندارد می‌سازد و آن را به عنوان یک نوبت عادی به agent تحویل می‌دهد. agent نتیجه را با ابزار `skill_manage` ذخیره می‌کند، بنابراین **دروازه تأیید نوشتن** اعمال می‌شود اگر آن را فعال کرده باشید.

`/learn`
`skill_manage`

## افشای تدریجی (Progressive Disclosure)

مهارت‌ها از الگوی بارگذاری کارآمد توکن استفاده می‌کنند:

```
Level 0: skills_list()           → [{name, description, category}, ...]   (~3k tokens)
Level 1: skill_view(name)        → Full content + metadata       (varies)
Level 2: skill_view(name, path)  → Specific reference file       (varies)
```

agent فقط محتوای کامل مهارت را زمانی بارگذاری می‌کند که واقعاً به آن نیاز داشته باشد.

## فرمت SKILL.md

```
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
platforms: [macos, linux]     # Optional — restrict to specific OS platforms
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    fallback_for_toolsets: [web]    # Optional — conditional activation (see below)
    requires_toolsets: [terminal]   # Optional — conditional activation (see below)
    config:                          # Optional — config.yaml settings
      - key: my.setting
        description: "What this controls"
        default: "value"
        prompt: "Prompt for setup"
---
# Skill Title

## When to Use
Trigger conditions for this skill.

## Procedure
1. Step one
2. Step two

## Pitfalls
- Known failure modes and fixes

## Verification
How to confirm it worked.
```

### مهارت‌های خاص پلتفرم

مهارت‌ها می‌توانند خود را به سیستم‌عامل‌های خاصی محدود کنند با استفاده از فیلد `platforms`:

`platforms`

| مقدار | مطابقت |
| --- | --- |
| macos | macOS (Darwin) |
| linux | Linux |
| windows | Windows |

`macos`
`linux`
`windows`

```
platforms: [macos]            # macOS only (e.g., iMessage, Apple Reminders, FindMy)
platforms: [macos, linux]     # macOS and Linux
```

هنگام تنظیم، مهارت به طور خودکار از پرامپت سیستم، `skills_list()` و دستورات slash در پلتفرم‌های ناسازگار پنهان می‌شود. اگر حذف شود، مهارت روی همه پلتفرم‌ها بارگذاری می‌شود.

`skills_list()`

## خروجی مهارت و تحویل رسانه

هنگامی که پاسخ یک مهارت (یا هر پاسخ agent) یک مسیر مطلق رسانه خام را شامل می‌شود — برای مثال `/home/user/screenshots/digraph.png` — دروازه آن را به طور خودکار تشخیص می‌دهد، از متن قابل مشاهده حذف می‌کند و فایل را به صورت بومی به چت کاربر تحویل می‌دهد (عکس Telegram، پیوست Discord و غیره) به جای گذاشتن مسیر خام در پیام.

`/home/user/screenshots/digraph.png`

به طور خاص برای صدا، دستورالعمل `[[audio_as_voice]]` فایل‌های صوتی را به حباب‌های پیام صوتی بومی در پلتفرم‌هایی که از آن پشتیبانی می‌کنند (Telegram، WhatsApp) ارتقا می‌دهد.

`[[audio_as_voice]]`

### اجبار تحویل سند-مانند: [[as_document]]

`[[as_document]]`

گاهی اوقات می‌خواهید **عکس** پیش‌نمایش درون‌خطی باشد: فایل به جای حباب تصویری فشرده‌شده مجدد به عنوان یک پیوست قابل دانلود تحویل داده شود. مثال کلاسیک یک اسکرین‌شات یا نمودار با وضوح بالا است — `sendPhoto` در Telegram آن را به ~200 KB در 1280 px فشرده می‌کند و خوانایی را نابود می‌کند. یک PNG با حجم ۱-۲ MB که از طریق `sendDocument` ارسال شود بایت‌های اصلی را سالم نگه می‌دارد.

`sendPhoto`
`sendDocument`

اگر پاسخ (یا هر متنی درون آن — معمولاً آخرین خط) دستورالعمل تحت‌اللفظی `[[as_document]]` را شامل شود، هر مسیر رسانه استخراج‌شده از آن پاسخ به جای حباب تصویری به عنوان یک پیوست سند/فایل تحویل داده می‌شود:

`[[as_document]]`

```
Here is your rendered chart:
/home/user/.hermes/cache/chart-q4-2025.png
[[as_document]]
```

دستورالعمل قبل از تحویل حذف می‌شود، بنابراین کاربران هرگز آن را نمی‌بینند. جزئیات عمداً برای هر پاسخ یا همه‌یا-هیچ است: یک‌بار `[[as_document]]` صادر کنید و هر مسیر تصویری در همان پاسخ به عنوان سند تحویل داده می‌شود. این دقیقاً مانند دامنه `[[audio_as_voice]]` است.

`[[as_document]]`
`[[audio_as_voice]]`

از آن در یک مهارت استفاده کنید وقتی:

- اسکرین‌شات‌ها یا نمودارهایی تولید می‌کنید که کاربر به فایل نیاز دارد (برای ویرایش در ابزار دیگر، بایگانی، اشتراک‌گذاری سالم).
- پیش‌نمایش پیش‌فرض تخریب‌کننده جزئیات را پنهان می‌کند (متن ریز، نمودارهای پیکسل-دقیق، رندرهای حساس به رنگ).

پلتفرم‌های بدون مسیر سند جداگانه (مثلاً SMS) به هر مکانیزم پیوستی که دارند بازمی‌گردند.

### فعال‌سازی شرطی (مهارت‌های Fallback)

مهارت‌ها می‌توانند بر اساس ابزارهای موجود در نشست جاری به طور خودکار خود را نشان یا پنهان کنند. این بیشتر برای **مهارت‌های fallback** مفید است — جایگزین‌های رایگان یا محلی که فقط وقتی یک ابزار پولی در دسترس نیست باید ظاهر شوند.

```
metadata:
  hermes:
    fallback_for_toolsets: [web]      # Show ONLY when these toolsets are unavailable
    requires_toolsets: [terminal]     # Show ONLY when these toolsets are available
    fallback_for_tools: [web_search]  # Show ONLY when these specific tools are unavailable
    requires_tools: [terminal]        # Show ONLY when these specific tools are available
```

| فیلد | رفتار |
| --- | --- |
| fallback_for_toolsets | مهارت **پنهان** است وقتی مجموعه ابزارهای فهرست‌شده موجود باشند. وقتی غایب باشند نشان داده می‌شود. |
| fallback_for_tools | همان، اما ابزارهای منفرد به جای مجموعه ابزارها را بررسی می‌کند. |
| requires_toolsets | مهارت **پنهان** است وقتی مجموعه ابزارهای فهرست‌شده موجود نباشند. وقتی حاضر باشند نشان داده می‌شود. |
| requires_tools | همان، اما ابزارهای منفرد را بررسی می‌کند. |

`fallback_for_toolsets`
`fallback_for_tools`
`requires_toolsets`
`requires_tools`

**مثال:** مهارت داخلی `duckduckgo-search` از `fallback_for_toolsets: [web]` استفاده می‌کند. وقتی `FIRECRAWL_API_KEY` تنظیم شده باشد، مجموعه ابزار web موجود است و agent از `web_search` استفاده می‌کند — مهارت DuckDuckGo پنهان می‌ماند. اگر کلید API موجود نباشد، مجموعه ابزار web ناموجود است و مهارت DuckDuckGo به طور خودکار به عنوان fallback ظاهر می‌شود.

`duckduckgo-search`
`fallback_for_toolsets: [web]`
`FIRECRAWL_API_KEY`
`web_search`

مهارت‌هایی بدون هیچ فیلد شرطی دقیقاً مانند قبل رفتار می‌کنند — همیشه نشان داده می‌شوند.

## راه‌اندازی امن هنگام بارگذاری

مهارت‌ها می‌توانند متغیرهای محیطی مورد نیاز را بدون ناپدید شدن از کشف اعلام کنند:

```
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: Tenor API key
    help: Get a key from https://developers.google.com/tenor
    required_for: full functionality
```

هنگامی که مقداری موجود نباشد، Hermes فقط وقتی که مهارت واقعاً در CLI محلی بارگذاری شده از شما به طور امن درخواست می‌کند. می‌توانید راه‌اندازی را رد کرده و همچنان از مهارت استفاده کنید. سطوح پیام‌رسانی هرگز رازها را در چت درخواست نمی‌کنند — به شما می‌گویند به جای آن از `hermes setup` یا `~/.hermes/.env` به صورت محلی استفاده کنید.

`hermes setup`
`~/.hermes/.env`

پس از تنظیم، متغیرهای محیطی اعلام‌شده به طور خودکار به `execute_code` و جعبه‌های sandBox ترمینال **ارسال می‌شوند** — اسکریپت‌های مهارت می‌توانند مستقیماً از `$TENOR_API_KEY` استفاده کنند. برای متغیرهای محیطی غیرمهارت، از گزینه پیکربندی `terminal.env_passthrough` استفاده کنید. جزئیات بیشتر در «ارسال متغیرهای محیطی» را ببینید.

`execute_code`
`terminal`
`$TENOR_API_KEY`
`terminal.env_passthrough`
[ارسال متغیرهای محیطی](/docs/user-guide/security#environment-variable-passthrough)

### تنظیمات پیکربندی مهارت

مهارت‌ها همچنین می‌توانند تنظیمات پیکربندی غیرراز (مسیرها، ترجیحات) ذخیره‌شده در `config.yaml` را اعلام کنند:

`config.yaml`

```
metadata:
  hermes:
    config:
      - key: myplugin.path
        description: Path to the plugin data directory
        default: "~/myplugin-data"
        prompt: Plugin data directory path
```

تنظیمات در `skills.config` در `config.yaml` شما ذخیره می‌شوند. `hermes config migrate` برای تنظیمات پیکربندی‌نشده سؤال می‌کند و `hermes config show` آنها را نمایش می‌دهد. هنگامی که یک مهارت بارگذاری می‌شود، مقادیر پیکربندی حل‌شده آن در زمینه تزریق می‌شوند تا agent مقادیر پیکربندی‌شده را به طور خودکار بداند.

`skills.config`
`hermes config migrate`
`hermes config show`

جزئیات بیشتر در «تنظیمات مهارت» و «ایجاد مهارت‌ها — تنظیمات پیکربندی» را ببینید.

[تنظیمات مهارت](/docs/user-guide/configuration#skill-settings)
[ایجاد مهارت‌ها — تنظیمات پیکربندی](/docs/developer-guide/creating-skills#config-settings-configyaml)

## ساختار دایرکتوری مهارت

```
~/.hermes/skills/                  # Single source of truth
├── mlops/                         # Category directory
│   ├── axolotl/
│   │   ├── SKILL.md               # Main instructions (required)
│   │   ├── references/            # Additional docs
│   │   ├── templates/             # Output formats
│   │   ├── scripts/               # Helper scripts callable from the skill
│   │   └── assets/                # Supplementary files
│   └── vllm/
│       └── SKILL.md
├── devops/
│   └── deploy-k8s/                # Agent-created skill
│       ├── SKILL.md
│       └── references/
├── .hub/                          # Skills Hub state
│   ├── lock.json
│   ├── quarantine/
│   └── audit.log
└── .bundled_manifest              # Tracks seeded bundled skills
```

## دایرکتوری‌های مهارت خارجی

اگر مهارت‌هایی خارج از Hermes نگهداری می‌کنید — برای مثال یک دایرکتوری مشترک `~/.agents/skills/` که توسط چندین ابزار هوش مصنوعی استفاده می‌شود — می‌توانید به Hermes بگویید آن دایرکتوری‌ها را نیز اسکن کند.

`~/.agents/skills/`

`external_dirs` را در بخش `skills` در `~/.hermes/config.yaml` اضافه کنید:

`external_dirs`
`skills`
`~/.hermes/config.yaml`

```
skills:
  external_dirs:
    - ~/.agents/skills
    - /home/shared/team-skills
    - ${SKILLS_REPO}/skills
```

مسیرها از گسترش `~` و جایگزینی متغیر محیطی `${VAR}` پشتیبانی می‌کنند.

`~`
`${VAR}`

### نحوه کار

- ایجاد محلی، به‌روزرسانی در جا: مهارت‌های جدید ایجادشده توسط agent در `~/.hermes/skills/` نوشته می‌شوند. مهارت‌های موجود در جایی که یافت می‌شوند تغییر می‌کنند، از جمله مهارت‌های زیر `external_dirs`، وقتی agent اقدامات `skill_manage` مانند `patch`، `edit`، `write_file`، `remove_file` یا `delete` را استفاده می‌کند.
- دایرکتوری‌های خارجی مرز حفاظت از نوشتن نیستند: اگر دایرکتوری مهارت خارجی توسط فرآیند Hermes قابل نوشتن باشد، به‌روزرسانی‌های مهارت مدیریت‌شده توسط agent می‌توانند فایل‌های آن دایرکتوری را تغییر دهند. از مجوزهای فایل‌سیستم یا تنظیم پروفایل/مجموعه ابزار جداگانه استفاده کنید اگر مهارت‌های خارجی مشترک باید فقط-خواندنی باقی بمانند.
- اولویت محلی: اگر نام مهارت یکسان هم در دایرکتوری محلی و هم در دایرکتوری خارجی وجود داشته باشد، نسخه محلی برنده است.
- ادغام کامل: مهارت‌های خارجی در ایندکس پرامپت سیستم، `skills_list`، `skill_view` و به عنوان دستورات slash `/skill-name` ظاهر می‌شوند — تفاوتی با مهارت‌های محلی ندارند.
- مسیرهای موجود ناپدیدشده به طور خاموش رد می‌شوند: اگر دایرکتوری پیکربندی‌شده وجود نداشته باشد، Hermes بدون خطا آن را نادیده می‌گیرد. برای دایرکتوری‌های مشترک اختیاری که ممکن است در هر ماشینی موجود نباشند مفید است.

`~/.hermes/skills/`
`external_dirs`
`skill_manage`
`patch`
`edit`
`write_file`
`remove_file`
`delete`
`skills_list`
`skill_view`
`/skill-name`

### مثال

```
~/.hermes/skills/               # Local (primary, read-write)
├── devops/deploy-k8s/
│   └── SKILL.md
└── mlops/axolotl/
    └── SKILL.md

~/.agents/skills/               # External (shared, mutable if writable)
├── my-custom-workflow/
│   └── SKILL.md
└── team-conventions/
    └── SKILL.md
```

هر چهار مهارت در فهرست مهارت‌های شما ظاهر می‌شوند. اگر مهارت جدیدی به نام `my-custom-workflow` به صورت محلی ایجاد کنید، نسخه خارجی را سایه می‌زند.

`my-custom-workflow`

## بسته‌های مهارت (Skill Bundles)

بسته‌های مهارت فایل‌های YAML کوچکی هستند که چندین مهارت را در یک دستور slash واحد گروه‌بندی می‌کنند. هنگامی که `/<bundle-name>` را اجرا می‌کنید، هر مهارت فهرست‌شده در بسته همزمان بارگذاری می‌شود — مفید وقتی یک وظیفه خاص همیشه از مجموعه یکسانی مهارت با هم بهره می‌برد.

`/<bundle-name>`

### مثال سریع

```
# Create a bundle for backend feature work
hermes bundles create backend-dev \
  --skill github-code-review \
  --skill test-driven-development \
  --skill github-pr-workflow \
  -d "Backend feature work — review, test, PR workflow"
```

سپس در CLI یا هر پلتفرم دروازه‌ای:

```
/backend-dev refactor the auth middleware
```

agent هر سه مهارت را در یک پیام کاربر بارگذاری‌شده دریافت می‌کند و هر متن پس از دستور slash به عنوان دستورالعمل کاربر پیوست می‌شود.

### طرح YAML

بسته‌ها در `~/.hermes/skill-bundles/<slug>.yaml` زندگی می‌کنند و به این شکل هستند:

`~/.hermes/skill-bundles/<slug>.yaml`

```
name: backend-dev
description: Backend feature work — review, test, PR workflow.
skills:
  - github-code-review
  - test-driven-development
  - github-pr-workflow
instruction: |
  Always start by writing failing tests, then implement.
  Open the PR through the standard workflow with co-author tags.
```

فیلدها:

- `name` (اختیاری — به طور پیش‌فرض نام فایل) — نام نمایشی بسته. برای دستور slash به یک slug کوتاه نرمال‌سازی می‌شود (`Backend Dev` → `/backend-dev`).
- `description` (اختیاری) — متن کوتاه نمایش‌شده در `/bundles` و `hermes bundles list`.
- `skills` (الزامی، فهرست غیرخالی) — نام مهارت‌ها یا مسیرهای نسبی به دایرکتوری مهارت‌های شما. از همان شناسه‌ای استفاده کنید که به `/<skill-name>` منتقل می‌کنید.
- `instruction` (اختیاری) — راهنمای اضافی که قبل از محتوای مهارت بارگذاری‌شده اضافه می‌شود. برای مستندسازی «چگونه همیشه اینها را با هم استفاده می‌کنیم» مفید است.

`name`
`Backend Dev`
`/backend-dev`
`description`
`/bundles`
`hermes bundles list`
`skills`
`/<skill-name>`
`instruction`

### مدیریت بسته‌ها

```
# List all installed bundles
hermes bundles list

# Inspect one bundle
hermes bundles show backend-dev

# Create a bundle interactively (omit --skill flags to enter them one per line)
hermes bundles create research

# Overwrite an existing bundle
hermes bundles create backend-dev --skill ... --force

# Delete a bundle
hermes bundles delete backend-dev

# Re-scan ~/.hermes/skill-bundles/ and report changes
hermes bundles reload
```

از داخل یک نشست چت، `/bundles` هر بسته نصب‌شده و مهارت‌های آن را فهرست می‌کند.

`/bundles`

### رفتار

- بسته‌ها **اولویت بالاتری نسبت به مهارت‌های منفرد** دارند وقتی slugها تداخل پیدا می‌کنند. اگر بسته‌ای به نام `research` نام‌گذاری کنید و مهارتی به نام `research` نیز داشته باشید، `/research` بسته را فراخوانی می‌کند. این عمدی است — شما با نام‌گذاری آن بسته را انتخاب کردید.
- مهارت‌های موجود ناپدیدشده رد می‌شوند، کشنده نیستند. اگر بسته‌ای `skill-foo` را فهرست کند و آن را نصب نکرده باشید، بسته همچنان مهارت‌هایی که حل می‌شوند را بارگذاری می‌کند و agent یادداشتی با فهرست ردشدگان دریافت می‌کند.
- بسته‌ها در هر سطحی کار می‌کنند — CLI تعاملی، TUI، چت داشبورد و هر پلتفرم دروازه‌ای (Telegram، Discord، Slack، …) — زیرا dispatch در همان مکان دستورات مهارت منفرد متمرکز است.
- بسته‌ها کش پرامپت را باطل نمی‌کنند. آنها در زمان فراخوانی یک پیام کاربر تازه تولید می‌کنند، دقیقاً مانند `/<skill-name>` — بدون جهش پرامپت سیستم.

`research`
`research`
`/research`
`skill-foo`
`/<skill-name>`

### کی بسته‌ها بهتر از نصب دستی هر مهارت هستند

از بسته استفاده کنید وقتی:

- همیشه مهارت‌های یکسانی را برای یک وظیفه تکراری جفت می‌کنید (`/backend-dev`، `/release-prep`، `/incident-response`).
- مدل ذهنی کوتاه‌تر از تایپ کردن چندین فراخوانی `/skill` متوالی می‌خواهید.
- می‌خواهید یک «پروفایل وظیفه» سراسری تیم با چک کردن YAML بسته در یک مخزن dotfiles مشترک و symlink کردن آن به `~/.hermes/skill-bundles/` ارائه دهید.

`/backend-dev`
`/release-prep`
`/incident-response`
`/skill`
`~/.hermes/skill-bundles/`

بسته فقط یک نام مستعار YAML است — مهارت‌ها را برای شما نصب نمی‌کند. خود مهارت‌ها باید از قبل موجود باشند (در `~/.hermes/skills/` یا یک دایرکتوری مهارت خارجی). در غیر این صورت فراخوانی بسته فقط مهارت‌های موجود ناپدیدشده را رد می‌کند.

`~/.hermes/skills/`

## مهارت‌های مدیریت‌شده توسط Agent (ابزار skill_manage)

agent می‌تواند مهارت‌های خود را از طریق ابزار `skill_manage` ایجاد، به‌روزرسانی و حذف کند. این **حافظه رویه‌ای** agent است — وقتی یک گردش کار غیرساده را کشف می‌کند، رویکرد را به عنوان یک مهارت برای استفاده مجدد آینده ذخیره می‌کند.

`skill_manage`

مهارت‌ها و حافظه در حلقه بهبود خود با هم کار می‌کنند: حافظه حقایق کوچک ماندگاری را ذخیره می‌کند که همیشه باید در زمینه باشند، در حالی که مهارت‌ها رویه‌های طولانی‌تری را ذخیره می‌کنند که فقط وقتی مرتبط باشند باید بارگذاری شوند. بررسی پس‌زمینه می‌تواند پس از نشست پیشنهادات یا مرحله‌بندی تغییرات مهارت ارائه دهد، اما دروازه تأیید نوشتن در زیر به شما اجازه می‌دهد بررسی انسانی را قبل از اعمال آن تغییرات الزامی کنید.

### وقتی Agent مهارت ایجاد می‌کند

- پس از تکمیل موفقیت‌آمیز یک وظیفه پیچیده (۵+ فراخوانی ابزار)
- وقتی به خطاها یا بن‌بست‌ها برخورد کرد و مسیر کاری را پیدا کرد
- وقتی کاربر رویکرد آن را اصلاح کرد
- وقتی یک گردش کار غیرساده کشف کرد

### اقدامات

| اقدام | استفاده برای | پارامترهای کلیدی |
| --- | --- | --- |
| create | مهارت جدید از صفر | `name`، `content` (SKILL.md کامل)، `category` اختیاری |
| patch | اصلاحات هدفمند (ترجیحی) | `name`، `old_string`، `new_string` |
| edit | بازنویسی‌های ساختاری بزرگ | `name`، `content` (جایگزینی SKILL.md کامل) |
| delete | حذف کامل یک مهارت | `name` |
| write_file | اضافه/به‌روزرسانی فایل‌های پشتیبان | `name`، `file_path`، `file_content` |
| remove_file | حذف یک فایل پشتیبان | `name`، `file_path` |

`create`
`name`
`content`
`category`
`patch`
`name`
`old_string`
`new_string`
`edit`
`name`
`content`
`delete`
`name`
`write_file`
`name`
`file_path`
`file_content`
`remove_file`
`name`
`file_path`

اقدام `patch` برای به‌روزرسانی‌ها ترجیح داده می‌شود — نسبت به `edit` کارآمدتر از نظر توکن است زیرا فقط متن تغییر یافته در فراخوانی ابزار ظاهر می‌شود.

`patch`
`edit`

### مدیریت نوشتن مهارت‌های agent (skills.write_approval)

`skills.write_approval`

به طور پیش‌فرض agent آزادانه مهارت‌ها را می‌نویسد — از جمله از **بررسی بهبود خود پس‌زمینه** که پس از یک نوبت اجرا می‌شود. اگر ترجیح می‌دهید هر نوشتن مهارتی را ابتدا تأیید کنید (مدل‌های کوچکی که قضاوت اشتباهی درباره آموخته‌هایشان می‌کنند، محیط‌های امنیتی، یا فقط می‌خواهید چشم‌هایی روی حلقه بهبود خود داشته باشید)، دروازه تأیید نوشتن را فعال کنید:

[بررسی بهبود خود پس‌زمینه](/docs/user-guide/features/memory#controlling-memory-writes-write_approval)

```
skills:
  write_approval: false     # false = write freely (default) | true = require approval
```

وقتی `write_approval: true` باشد، هر نوشتن `skill_manage` (create / edit / patch / delete / write_file / remove_file) به جای commit **مرحله‌بندی** می‌شود — یک SKILL.md برای بررسی درون‌خطی بسیار بزرگ است، بنابراین مرحله‌بندی صرف‌نظر از اینکه نوشتن از یک نوبت پیش‌زمینه یا بررسی پس‌زمینه آمده باشد اعمال می‌شود.
نوشته‌های مرحله‌بندی‌شده پس از راه‌اندازی مجدد در `~/.hermes/pending/skills/` باقی می‌مانند و با همان جریان آشنای تأیید/رد کردن دستورات خطرناک بررسی می‌شوند:

`write_approval: true`
`skill_manage`
`~/.hermes/pending/skills/`

```
/skills pending             # list staged skill writes + a one-line gist each
/skills diff <id>           # full unified diff (best viewed in CLI or dashboard)
/skills approve <id>        # apply it (or 'all')
/skills reject <id>         # drop it (or 'all')
/skills approval on         # turn the gate on (or 'off') and persist it
```

سطح بررسی در CLI تعاملی و پلتفرم‌های پیام‌رسانی کار می‌کند (خروجی diff برای حباب‌های چت محدود شده است — diff کامل را در CLI یا فایل JSON pending بخوانید). نوشتن‌های حافظه همان دروازه را تحت `memory.write_approval` دارند — «کنترل نوشتن حافظه» را ببینید.

`memory.write_approval`
[کنترل نوشتن حافظه](/docs/user-guide/features/memory#controlling-memory-writes-write_approval)

> تنظیم جداگانه `skills.guard_agent_created` یک اسکنر محتوا (هوریستیک‌های الگوی خطرناک) است، نه یک دروازه تأیید — این دو مستقل هستند. «محافظت در برابر نوشتن مهارت‌های ایجادشده توسط agent» را ببینید.

تنظیم جداگانه `skills.guard_agent_created` یک اسکنر محتوا (هوریستیک‌های الگوی خطرناک) است، نه یک دروازه تأیید — این دو مستقل هستند. «محافظت در برابر نوشتن مهارت‌های ایجادشده توسط agent» را ببینید.

`skills.guard_agent_created`
[محافظت در برابر نوشتن مهارت‌های ایجادشده توسط agent](/docs/user-guide/configuration#guard-on-agent-created-skill-writes)

## هاب مهارت‌ها

مهارت‌ها را از ثبت‌نام‌های آنلاین، `skills.sh`، نقاط پایانی مهارت مستقیم شناخته‌شده و مهارت‌های رسمی اختیاری مرور، جستجو، نصب و مدیریت کنید.

`skills.sh`

### دستورات رایج

```
hermes skills browse                              # Browse all hub skills (official first)
hermes skills browse --source official            # Browse only official optional skills
hermes skills search kubernetes                   # Search all sources
hermes skills search react --source skills-sh     # Search the skills.sh directory
hermes skills search https://mintlify.com/docs --source well-known
hermes skills inspect openai/skills/k8s           # Preview before installing
hermes skills install openai/skills/k8s           # Install with security scan
hermes skills install official/security/1password
hermes skills install skills-sh/vercel-labs/json-render/json-render-react --force
hermes skills install well-known:https://mintlify.com/docs/.well-known/skills/mintlify
hermes skills install https://sharethis.chat/SKILL.md              # Direct URL (single-file SKILL.md)
hermes skills install https://example.com/SKILL.md --name my-skill # Override name when frontmatter has none
hermes skills list --source hub                   # List hub-installed skills
hermes skills check                               # Check installed hub skills for upstream updates
hermes skills update                              # Reinstall hub skills with upstream changes when needed
hermes skills audit                               # Re-scan all hub skills for security
hermes skills uninstall k8s                       # Remove a hub skill
hermes skills reset google-workspace              # Un-stick a bundled skill from "user-modified" (see below)
hermes skills reset google-workspace --restore    # Also restore the bundled version, deleting your local edits
hermes skills publish skills/my-skill --to github --repo owner/repo
hermes skills snapshot export setup.json          # Export skill config
hermes skills tap add myorg/skills-repo           # Add a custom GitHub source
```

### منابع Hub پشتیبانی‌شده

| منبع | مثال | توضیحات |
| --- | --- | --- |
| official | official/security/1password | مهارت‌های اختیاری همراه Hermes ارائه می‌شوند. |
| skills-sh | skills-sh/vercel-labs/agent-skills/vercel-react-best-practices | از طریق `hermes skills search <query> --source skills-sh` قابل جستجو. هنگامی که slug skills.sh با پوشه مخزن متفاوت است، Hermes مهارت‌های با نام مستعار را حل می‌کند. |
| well-known | well-known:https://mintlify.com/docs/.well-known/skills/mintlify | مهارت‌هایی که مستقیماً از `/.well-known/skills/index.json` در یک وب‌سایت ارائه می‌شوند. با استفاده از سایت یا URL اسناد جستجو کنید. |
| url | https://sharethis.chat/SKILL.md | URL HTTP(S) مستقیم به یک فایل `SKILL.md` تک‌فایلی. حل نام: frontmatter → URL slug → پرامپت تعاملی → پرچم `--name`. |
| github | openai/skills/k8s | نصب مستقیم از مخزن/مسیر GitHub و tapهای سفارشی. |
| clawhub، lobehub، browse-sh | شناسه‌های خاص منبع | ادغام‌های جامعه یا بازار. |

`official`
`official/security/1password`
`skills-sh`
`skills-sh/vercel-labs/agent-skills/vercel-react-best-practices`
`hermes skills search <query> --source skills-sh`
`well-known`
`well-known:https://mintlify.com/docs/.well-known/skills/mintlify`
`/.well-known/skills/index.json`
`url`
`https://sharethis.chat/SKILL.md`
`SKILL.md`
`--name`
`github`
`openai/skills/k8s`
`clawhub`
`lobehub`
`browse-sh`

### ادغام‌ها و ثبت‌نام‌های یکپارچه

Hermes در حال حاضر با این اکوسیستم‌های مهارت و منابع کشف ادغام شده است:

#### ۱. مهارت‌های رسمی اختیاری (official)

`official`

اینها در خود مخزن Hermes نگهداری می‌شوند و با اعتماد داخلی نصب می‌شوند.

- فهرست: فهرست رسمی مهارت‌های اختیاری
- منبع در مخزن: `optional-skills/`
- مثال:

[فهرست رسمی مهارت‌های اختیاری](/docs/reference/optional-skills-catalog)
`optional-skills/`

```
hermes skills browse --source official
hermes skills install official/security/1password
```

#### ۲. skills.sh (skills-sh)

`skills-sh`

این فهرست مهارت‌های عمومی Vercel است. Hermes می‌تواند مستقیماً آن را جستجو کند، صفحات جزئیات مهارت را بررسی کند، slugهای با نام مستعار را حل کند و از مخزن منبع زیربنایی نصب کند.

- فهرست: [skills.sh](https://skills.sh/)
- مخزن CLI/ابزار: [vercel-labs/skills](https://github.com/vercel-labs/skills)
- مخزن رسمی مهارت‌های Vercel: [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
- مثال:

[skills.sh](https://skills.sh/)
[vercel-labs/skills](https://github.com/vercel-labs/skills)
[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```
hermes skills search react --source skills-sh
hermes skills inspect skills-sh/vercel-labs/json-render/json-render-react
hermes skills install skills-sh/vercel-labs/json-render/json-render-react --force
```

#### ۳. نقاط پایانی مهارت شناخته‌شده (well-known)

`well-known`

این کشف مبتنی URL از سایت‌هایی است که `/.well-known/skills/index.json` را منتشر می‌کنند. یک hub متمرکز واحد نیست — یک قرارداد کشف وب است.

`/.well-known/skills/index.json`
- مثال نقطه پایانی زنده: [فهرست مهارت‌های Mintlify docs](https://mintlify.com/docs/.well-known/skills/index.json)
- پیاده‌سازی مرجع سرور: [vercel-labs/skills-handler](https://github.com/vercel-labs/skills-handler)
- مثال:

[فهرست مهارت‌های Mintlify docs](https://mintlify.com/docs/.well-known/skills/index.json)
[vercel-labs/skills-handler](https://github.com/vercel-labs/skills-handler)

```
hermes skills search https://mintlify.com/docs --source well-known
hermes skills inspect well-known:https://mintlify.com/docs/.well-known/skills/mintlify
hermes skills install well-known:https://mintlify.com/docs/.well-known/skills/mintlify
```

#### ۴. مهارت‌های مستقیم GitHub (github)

`github`

Hermes می‌تواند مستقیماً از مخزن‌های GitHub و tapهای مبتنی GitHub نصب کند. این وقتی مفید است که از قبل مخزن/مسیر را می‌شناسید یا می‌خواهید مخزن منبع سفارشی خود را اضافه کنید.

tapهای پیش‌فرض (قابل مرور بدون هیچ تنظیمی):

- [openai/skills](https://github.com/openai/skills)
- [anthropics/skills](https://github.com/anthropics/skills)
- [huggingface/skills](https://github.com/huggingface/skills)
- [NVIDIA/skills](https://github.com/NVIDIA/skills) — مهارت‌های تأییدشده توسط NVIDIA (امضاشده `skill.oms.sig` + حاکمیت `skill-card.md`)
- [garrytan/gstack](https://github.com/garrytan/gstack)
- مثال:

```
hermes skills install openai/skills/k8s
hermes skills tap add myorg/skills-repo
```

**گروه‌بندی‌های دسته‌بندی (skills.sh.json):** یک tap GitHub ممکن است فایل `skills.sh.json` را در ریشه مخزن خود طبق schema `skills.sh` ارائه دهد. `groupings` آن (هر کدام با `title` و لیستی از نام مهارت‌ها) در زمان ایندکس خوانده می‌شوند و به برچسب‌های دسته‌بندی نمایش‌شده در صفحه Skills Hub تبدیل می‌شوند — به جای حدس مبتنی بر tag. این عمومی است: هر tap که فایل را ارائه دهد دسته‌بندی واقعی دریافت می‌کند، بدون نیاز به تغییرات Hermes.

`skills.sh.json`
`skills.sh.json`
[skills.sh schema](https://skills.sh/schemas/skills.sh.schema.json)
`groupings`
`title`
[Skills Hub](https://hermes-agent.nousresearch.com/docs)

```
{
  "$schema": "https://skills.sh/schemas/skills.sh.schema.json",
  "groupings": [
    { "title": "Inference AI", "skills": ["dynamo-recipe-runner", "dynamo-router-sla"] },
    { "title": "Decision Optimization", "skills": ["cuopt-developer", "cuopt-install"] }
  ]
}
```

#### ۵. ClawHub (clawhub)

`clawhub`

بازار مهارت‌های طرف سوم که به عنوان یک منبع جامعه ادغام شده است.

- سایت: [clawhub.ai](https://clawhub.ai/)
- شناسه منبع Hermes: `clawhub`

[clawhub.ai](https://clawhub.ai/)
`clawhub`

#### ۶. مخزن‌های بازار-مانند Claude (claude-marketplace)

`claude-marketplace`

Hermes از مخزن‌های بازاری که مانیفیست‌های plugin/بازار سازگار با Claude را منتشر می‌کنند پشتیبانی می‌کند.

منابع ادغام‌شده شناخته‌شده شامل موارد زیر هستند:

- [anthropics/skills](https://github.com/anthropics/skills)
- [aiskillstore/marketplace](https://github.com/aiskillstore/marketplace)

شناسه منبع Hermes: `claude-marketplace`

`claude-marketplace`

#### ۷. LobeHub (lobehub)

`lobehub`

Hermes می‌تواند مدخل‌های agent از فهرست عمومی LobeHub را جستجو کرده و به مهارت‌های قابل نصب Hermes تبدیل کند.

- سایت: [LobeHub](https://lobehub.com/)
- ایندکس عمومی agentها: [chat-agents.lobehub.com](https://chat-agents.lobehub.com/)
- مخزن زیربنایی: [lobehub/lobe-chat-agents](https://github.com/lobehub/lobe-chat-agents)
- شناسه منبع Hermes: `lobehub`

[LobeHub](https://lobehub.com/)
[chat-agents.lobehub.com](https://chat-agents.lobehub.com/)
[lobehub/lobe-chat-agents](https://github.com/lobehub/lobe-chat-agents)
`lobehub`

#### ۸. browse.sh (browse-sh)

`browse-sh`

Hermes با `browse.sh` ادغام شده است، فهرست Browserbase بیش از ۲۰۰ فایل SKILL.md اتوماسیون مرورگر خاص-سایت (Airbnb، Amazon، arXiv، 12306.cn، Etsy، Xero و بسیاری دیگر). هر مهارت توضیح می‌دهد چگونه یک وب‌سایت را از ابتدا تا انتها هدایت کند و برای استفاده با ابزارهای مرورگر Hermes و هر مهارت اتوماسیون مرورگری که از قبل نصب کرده‌اید مناسب است.

[browse.sh](https://browse.sh/)
- سایت: [browse.sh](https://browse.sh/)
- API فهرست: `https://browse.sh/api/skills`
- شناسه منبع Hermes: `browse-sh`
- سطح اعتماد: community

[browse.sh](https://browse.sh/)
`https://browse.sh/api/skills`
`browse-sh`
`community`

```
hermes skills search airbnb --source browse-sh
hermes skills inspect browse-sh/airbnb.com/search-listings-ddgioa
hermes skills install browse-sh/airbnb.com/search-listings-ddgioa
```

شناسه‌ها از فرم `browse-sh/<hostname>/<task-id>` استفاده می‌کنند و با slug نمایش‌داده‌شده توسط فهرست browse.sh مطابقت دارند. محتوا از طریق نقطه پایانی جزئیات هر مهارت (`/api/skills/<slug>` → `skillMdUrl`) حل می‌شود، نه از طریق `sourceUrl` GitHub فهرست.

`browse-sh/<hostname>/<task-id>`
`/api/skills/<slug>`
`skillMdUrl`
`sourceUrl`

#### ۹. URL مستقیم (url)

`url`

یک فایل `SKILL.md` تک‌فایلی را مستقیماً از هر URL HTTP(S) نصب کنید — مفید وقتی یک نویسنده مهارتی را در سایت خود میزبانی می‌کند (بدون فهرست hub، بدون مسیر GitHub برای تایپ). Hermes URL را دریافت، YAML frontmatter را تجزیه، اسکن امنیتی انجام و نصب می‌کند.

`SKILL.md`
- شناسه منبع Hermes: `url`
- شناسه: خود URL (بدون نیاز به پیشوند)
- دامنه: فقط فایل `SKILL.md` تک‌فایلی. مهارت‌های چندفایلی با `references/` یا `scripts/` به یک مانیفست نیاز دارند و باید از طریق یکی از منابع دیگر بالا منتشر شوند.

`url`
`SKILL.md`
`references/`
`scripts/`

```
hermes skills install https://sharethis.chat/SKILL.md
hermes skills install https://example.com/my-skill/SKILL.md --category productivity
```

حل نام، به ترتیب:

1. فیلد `name:` در YAML frontmatter فایل `SKILL.md` (توصیه‌شده — هر مهارت خوبی یکی دارد).
2. نام دایرکتوری والد از مسیر URL (مثلاً `.../my-skill/SKILL.md` → `my-skill`، یا `.../my-skill.md` → `my-skill`)، وقتی یک شناسه معتبر باشد (`^[a-z][a-z0-9_-]*$`).
3. پرامپت تعاملی در یک ترمینال با TTY.
4. در سطوح غیرتعاملی (دستور slash `/skills install` در TUI، پلتفرم‌های دروازه، اسکریپت‌ها)، خطای تمیزی که به بازنویسی `--name` اشاره می‌کند.

`name:`
`.../my-skill/SKILL.md`
`my-skill`
`.../my-skill.md`
`my-skill`
`^[a-z][a-z0-9_-]*$`
`/skills install`
`--name`

```
# Frontmatter has no name and the URL slug is unhelpful — supply one:
hermes skills install https://example.com/SKILL.md --name sharethis-chat

# Or inside a chat session:
/skills install https://example.com/SKILL.md --name sharethis-chat
```

سطح اعتماد همیشه `community` است — همان اسکن امنیتی که برای هر منبع دیگر اجرا می‌شود. URL به عنوان شناسه نصب ذخیره می‌شود، بنابراین `hermes skills update` وقتی می‌خواهید تازه‌سازی کنید به طور خودکار از همان URL دوباره دریافت می‌کند.

`community`
`hermes skills update`

### اسکن امنیتی و `--force`

`--force`

همه مهارت‌های نصب‌شده از hub از یک **اسکنر امنیتی** عبور می‌کنند که نشت داده، تزریق پرامپت، دستورات مخرب، سیگنال‌های زنجیره تأمین و سایر تهدیدها را بررسی می‌کند.

`hermes skills inspect ...` اکنون هنگام موجود بودن متادیتای upstream را نیز نمایش می‌دهد:

`hermes skills inspect ...`
- URL مخزن
- URL صفحه جزئیات skills.sh
- دستور نصب
- نصب‌های هفتگی
- وضعیت‌های اسکن امنیتی upstream
- URLهای فهرست/نقطه پایانی well-known

از `--force` استفاده کنید وقتی مهارتی طرف سوم را بررسی کرده‌اید و می‌خواهید یک مسدودیت سیاست غیرخطرناک را بازنویسی کنید:

`--force`

```
hermes skills install skills-sh/anthropics/skills/pdf --force
```

رفتار مهم:

- `--force` می‌تواند مسدودیت‌های سیاست برای یافته‌های نوع caution/warn را بازنویسی کند.
- `--force` حکم اسکن `dangerous` را **بازنویسی نمی‌کند**.
- مهارت‌های رسمی اختیاری (`official/...`) به عنوان اعتماد داخلی رفتار شده و پنل هشدار طرف سوم را نشان نمی‌دهند.

`--force`
`--force`
`dangerous`
`official/...`

### سطوح اعتماد

| سطح | منبع | سیاست |
| --- | --- | --- |
| builtin | همراه Hermes ارائه می‌شود | همیشه مورد اعتماد |
| official | `optional-skills/` در مخزن | اعتماد داخلی، بدون هشدار طرف سوم |
| trusted | ثبت‌نام‌ها/مخزن‌های مورد اعتماد مانند `openai/skills`، `anthropics/skills`، `huggingface/skills`، `NVIDIA/skills` | سیاست آزادتر از منابع community |
| community | همه چیزهای دیگر (skills.sh، نقاط پایانی well-known، مخزن‌های GitHub سفارشی، بیشتر بازارها) | یافته‌های غیرخطرناک با `--force` قابل بازنویسی هستند؛ حکم `dangerous` همچنان مسدود باقی می‌ماند |

`builtin`
`official`
`optional-skills/`
`trusted`
`openai/skills`
`anthropics/skills`
`huggingface/skills`
`NVIDIA/skills`
`community`
`skills.sh`
`--force`
`dangerous`

### چرخه حیات به‌روزرسانی

Hub اکنون اطلاعات مبدأ کافی برای بازبررسی نسخه‌های upstream مهارت‌های نصب‌شده را ردیابی می‌کند:

```
hermes skills check          # Report which installed hub skills changed upstream
hermes skills update         # Reinstall only the skills with updates available
hermes skills update react   # Update one specific installed hub skill
```

این از شناسه منبع ذخیره‌شده به علاوه هش محتوای بسته upstream فعلی برای تشخیص انحراف استفاده می‌کند.

عملیات hub از GitHub API استفاده می‌کند که محدودیت نرخ ۶۰ درخواست/ساعت برای کاربران احراز هویت‌نشده دارد. اگر خطاهای محدودیت نرخ در حین نصب یا جستجو مشاهده کردید، `GITHUB_TOKEN` را در فایل `.env` خود تنظیم کنید تا محدودیت را به ۵,۰۰۰ درخواست/ساعت افزایش دهید. پیام خطا هنگام وقوع این اتفاق یک راهنمای عملی نشان می‌دهد.

`GITHUB_TOKEN`
`.env`

### انتشار یک tap مهارت سفارشی

اگر می‌خواهید مجموعه‌ای گزینش‌شده از مهارت‌ها را به اشتراک بگذارید — برای تیم، سازمان یا عموم — می‌توانید آنها را به عنوان یک tap منتشر کنید: یک مخزن GitHub که کاربران دیگر Hermes با `hermes skills tap add <owner/repo>` اضافه می‌کنند. بدون سرور، بدون ثبت‌نام در ثبت‌نام، بدون pipeline انتشار. فقط یک دایرکتوری از فایل‌های `SKILL.md`.

`hermes skills tap add <owner/repo>`
`SKILL.md`

#### چیدمان مخزن

tap هر مخزن GitHub (عمومی یا خصوصی — خصوصی به `GITHUB_TOKEN` نیاز دارد) است که به این شکل چیده شده:

`GITHUB_TOKEN`

```
owner/repo
├── skills/                       # default path; configurable per-tap
│   ├── my-workflow/
│   │   ├── SKILL.md              # required
│   │   ├── references/           # optional supporting files
│   │   ├── templates/
│   │   └── scripts/
│   ├── another-skill/
│   │   └── SKILL.md
│   └── third-skill/
│       └── SKILL.md
└── README.md                     # optional but helpful
```

قوانین:

- هر مهارت در دایرکتوری خود زیر مسیر ریشه tap (پیش‌فرض `skills/`) زندگی می‌کند.
- نام دایرکتوری به slug نصب مهارت تبدیل می‌شود.
- هر دایرکتوری مهارت باید یک `SKILL.md` با frontmatter استاندارد `SKILL.md` شامل `name`، `description` و اختیاری `metadata.hermes.tags`، `version`، `author`، `platforms`، `metadata.hermes.config` داشته باشد.
- زیردایرکتوری‌هایی مانند `references/`، `templates/`، `scripts/`، `assets/` در زمان نصب همراه `SKILL.md` دانلود می‌شوند.
- مهارت‌هایی که نام دایرکتوری آنها با `.` یا `_` شروع می‌شود نادیده گرفته می‌شوند.

`skills/`
`SKILL.md`
`name`
`description`
`metadata.hermes.tags`
`version`
`author`
`platforms`
`metadata.hermes.config`
`references/`
`templates/`
`scripts/`
`assets/`
`SKILL.md`
`.`
`_`

Hermes مهارت‌ها را با فهرست‌کردن هر زیردایرکتوری مسیر tap و بررسی هر کدام برای `SKILL.md` کشف می‌کند.

`SKILL.md`

#### مثال حداقلی tap

```
my-org/hermes-skills
└── skills/
    └── deploy-runbook/
        └── SKILL.md
```

`skills/deploy-runbook/SKILL.md`:

```
---
name: deploy-runbook
description: Our deployment runbook — services, rollback, Slack channels
version: 1.0.0
author: My Org Platform Team
metadata:
  hermes:
    tags: [deployment, runbook, internal]
---
# Deploy Runbook
Step 1: ...
```

پس از push کردن آن به GitHub، هر کاربر Hermes می‌تواند اشتراک و نصب کند:

```
hermes skills tap add my-org/hermes-skills
hermes skills search deploy
hermes skills install my-org/hermes-skills/deploy-runbook
```

### مسیرهای غیرپیش‌فرض

اگر مهارت‌های شما در `skills/` زندگی نمی‌کنند (رایج وقتی زیردایرکتوری `skills/` را به یک پروژه موجود اضافه می‌کنید)، ورودی tap در `~/.hermes/.hub/taps.json` را ویرایش کنید:

`skills/`
`skills/`
`~/.hermes/.hub/taps.json`

```
{
  "taps": [
    {"repo": "my-org/platform-docs", "path": "internal/skills/"}
  ]
}
```

CLI `hermes skills tap add` tapهای جدید را به طور پیش‌فرض به `path: "skills/"` اختصاص می‌دهد؛ فایل را مستقیماً ویرایش کنید اگر به مسیر متفاوتی نیاز دارید. `hermes skills tap list` مسیر مؤثر هر tap را نمایش می‌دهد.

`hermes skills tap add`
`path: "skills/"`
`hermes skills tap list`

### نصب مستقیم مهارت‌های منفرد (بدون اضافه کردن tap)

کاربران همچنین می‌توانند یک مهارت منفرد را از هر مخزن عمومی GitHub بدون اضافه کردن کل مخزن به عنوان tap نصب کنند:

```
hermes skills install owner/repo/skills/my-workflow
```

مفید وقتی می‌خواهید یک مهارت را بدون درخواست از کاربر برای اشتراک کل ثبت‌نام شما به اشتراک بگذارید.

### سطوح اعتماد برای tapها

tapهای جدید به طور پیش‌فرض سطح اعتماد `community` دریافت می‌کنند. مهارت‌های نصب‌شده از آنها از اسکن امنیتی استاندارد عبور می‌کنند و در اولین نصب پنل هشدار طرف سوم را نشان می‌دهند. اگر سازمان شما یا منبع مورد اعتماد گسترده باید اعتماد بالاتری دریافت کند، مخزن آن را به `TRUSTED_REPOS` در `tools/skills_hub.py` اضافه کنید (نیاز به PR هسته Hermes).

`community`
`TRUSTED_REPOS`
`tools/skills_hub.py`

### مدیریت tap

```
hermes skills tap list                                # show all configured taps
hermes skills tap add myorg/skills-repo               # add (default path: skills/)
hermes skills tap remove myorg/skills-repo            # remove
```

در داخل یک نشست در حال اجرا:

```
/skills tap list
/skills tap add myorg/skills-repo
/skills tap remove myorg/skills-repo
```

tapها در `~/.hermes/.hub/taps.json` ذخیره می‌شوند (در صورت نیاز ایجاد می‌شود).

`~/.hermes/.hub/taps.json`

## به‌روزرسانی مهارت‌های bundled (hermes skills reset)

`hermes skills reset`

Hermes با مجموعه‌ای از مهارت‌های bundled در `skills/` داخل مخزن ارائه می‌شود. در نصب و در هر `hermes update`، یک عبور همگام‌سازی آنها را به `~/.hermes/skills/` کپی می‌کند و یک مانیفست در `~/.hermes/skills/.bundled_manifest` ثبت می‌کند که هر نام مهارت را به هش محتوا در زمان همگام‌سازی (هش origin) نگاشت می‌کند.

`skills/`
`hermes update`
`~/.hermes/skills/`
`~/.hermes/skills/.bundled_manifest`

در هر همگام‌سازی، Hermes هش نسخه محلی شما را دوباره محاسبه و با هش origin مقایسه می‌کند:

- **تغییر نیافته** → ایمن برای کشیدن تغییرات upstream، کپی نسخه bundled جدید، ثبت هش origin جدید.
- **تغییر یافته** → به عنوان **تغییریافته توسط کاربر** در نظر گرفته شده و برای همیشه رد می‌شود، بنابراین ویرایش‌های شما هرگز له نمی‌شوند.

حفاظت خوب است، اما یک لبه تیز دارد. اگر یک مهارت bundled را ویرایش کنید و سپس بخواهید تغییرات خود را رها کرده و به نسخه bundled برگردید فقط با کپی-پیست از `~/.hermes/hermes-agent/skills/`، مانیفست همچنان هش origin قدیمی را از زمان آخرین همگام‌سازی موفق نگه می‌دارد. محتوای کپی-پیست تازه شما (هش bundled فعلی) با آن هش origin منقضی‌شده مطابقت نخواهد داشت، بنابراین همگام‌سازی همچنان آن را به عنوان تغییریافته توسط کاربر پرچم‌گذاری می‌کند.

`~/.hermes/hermes-agent/skills/`

`hermes skills reset` دریچه فرار است:

`hermes skills reset`

```
# Safe: clears the manifest entry for this skill. Your current copy is preserved,
# but the next sync re-baselines against it so future updates work normally.
hermes skills reset google-workspace

# Full restore: also deletes your local copy and re-copies the current bundled
# version. Use this when you want the pristine upstream skill back.
hermes skills reset google-workspace --restore

# Non-interactive (e.g. in scripts or TUI mode) — skip the --restore confirmation.
hermes skills reset google-workspace --restore --yes
```

همان دستور در چت به عنوان دستور slash کار می‌کند:

```
/skills reset google-workspace
/skills reset google-workspace --restore
```

هر پروفایل `bundled_manifest` خود را در `HERMES_HOME` خود دارد، بنابراین `hermes -p coder skills reset <name>` فقط بر آن پروفایل تأثیر می‌گذارد.

`.bundled_manifest`
`HERMES_HOME`
`hermes -p coder skills reset <name>`

### دستورات slash (داخل چت)

همه دستورات مشابه با `/skills` کار می‌کنند:

`/skills`

```
/skills browse
/skills search react --source skills-sh
/skills search https://mintlify.com/docs --source well-known
/skills inspect skills-sh/vercel-labs/json-render/json-render-react
/skills install openai/skills/skill-creator --force
/skills check
/skills update
/skills reset google-workspace
/skills list
```

مهارت‌های رسمی اختیاری همچنان از شناسه‌هایی مانند `official/security/1password` و `official/migration/openclaw-migration` استفاده می‌کنند.

`official/security/1password`
`official/migration/openclaw-migration`
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/skills.md)
