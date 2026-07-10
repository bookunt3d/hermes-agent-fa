---
layout: docs
title: "معماری"
permalink: /docs/developer-guide/architecture/
---

- 
- Developer Guide
- Architecture
- Architecture

# معماری

این صفحه نقشه سطح بالای ساختار داخلی Hermes Agent است. از آن برای جهت‌یابی در مخزن کد استفاده کنید، سپس برای جزئیات پیاده‌سازی به اسناد زیرسیستم‌های خاص بپردازید.

## نمای کلی سیستم

```
┌─────────────────────────────────────────────────────────────────────┐│                        Entry Points                                  ││                                                                      ││  CLI (cli.py)    Gateway (gateway/run.py)    ACP (acp_adapter/)     ││  Batch Runner    API Server                  Python Library          │└──────────┬──────────────┬───────────────────────┬───────────────────┘           │              │                       │           ▼              ▼                       ▼┌─────────────────────────────────────────────────────────────────────┐│                     AIAgent (run_agent.py)                          ││                                                                     ││  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               ││  │ Prompt       │  │ Provider     │  │ Tool         │               ││  │ Builder      │  │ Resolution   │  │ Dispatch     │               ││  │ (prompt_     │  │ (runtime_    │  │ (model_      │               ││  │  builder.py) │  │  provider.py)│  │  tools.py)   │               ││  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               ││         │                 │                 │                       ││  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐               ││  │ Compression  │  │ 3 API Modes  │  │ Tool Registry│               ││  │ & Caching    │  │ chat_compl.  │  │ (registry.py)│               ││  │              │  │ codex_resp.  │  │ 70+ tools    │               ││  │              │  │ anthropic    │  │ 28 toolsets  │               ││  └──────────────┘  └──────────────┘  └──────────────┘               │└─────────┴─────────────────┴─────────────────┴───────────────────────┘           │                                    │           ▼                                    ▼┌───────────────────┐              ┌──────────────────────┐│ Session Storage   │              │ Tool Backends         ││ (SQLite + FTS5)   │              │ Terminal / Docker / SSH││                   │              │ Modal / Singularity   ││                   │              │ Daytona               │└───────────────────┘              └──────────────────────┘
```

## ساختار دایرکتوری

```
hermes-agent/├── run_agent.py              # AIAgent — حلقه مکالمه اصلی (فایل بزرگ)├── cli.py                    # HermesCLI — رابط ترمینال تعاملی (فایل بزرگ)├── model_tools.py            # کشف ابزار، جمع‌آوری schema، مسیریابی├── toolsets.py               # گروه‌بندی ابزارها و پیش‌فرض‌های پلتفرم├── hermes_state.py           # پایگاه داده نشست/وضعیت SQLite با FTS5├── hermes_constants.py       # HERMES_HOME، مسیرهای آگاه نشست├── batch_runner.py           # تولید trajectory دسته‌ای│├── agent/                    # ساختار داخلی agent│   ├── prompt_builder.py     # مونتاژ system prompt│   ├── context_engine.py     # ABC ContextEngine (قابل اتصال)│   ├── context_compressor.py # موتور پیش‌فرض — خلاصه‌سازی با اتلاف│   ├── prompt_caching.py     # کش prompt Anthropic│   ├── auxiliary_client.py   # LLM کمکی برای تسک‌های جانبی (بینایی، خلاصه‌سازی)│   ├── model_metadata.py     # طول‌های context مدل، تخمین توکن│   ├── models_dev.py         # یکپارچه‌سازی ثبت‌نام models.dev│   ├── anthropic_adapter.py  # تبدیل فرمت Anthropic Messages API│   ├── display.py            # KawaiiSpinner، قالب‌بندی پیش‌نمایش ابزار│   ├── skill_commands.py     # دستورات اسلش مهارت│   ├── memory_manager.py    # ارکستراسیون مدیر حافظه│   ├── memory_provider.py   # ABC ارائه‌دهنده حافظه│   └── trajectory.py         # کمک‌کننده‌های ذخیره trajectory│├── hermes_cli/               # زیردستورها و راه‌اندازی CLI│   ├── main.py               # نقطه ورود — تمام زیردستورهای `hermes` (فایل بزرگ)│   ├── config.py             # DEFAULT_CONFIG، OPTIONAL_ENV_VARS، مهاجرت│   ├── commands.py           # COMMAND_REGISTRY — تعریفات مرکزی دستور اسلش│   ├── auth.py               # PROVIDER_REGISTRY، حل اعتبارنامه│   ├── runtime_provider.py   # ارائه‌دهنده → api_mode + اعتبارنامه│   ├── models.py             # کاتالوگ مدل، لیست مدل‌های ارائه‌دهنده│   ├── model_switch.py       # منطق دستور /model (مشترک CLI + gateway)│   ├── setup.py              # راه‌اندازی تعاملی... [برش یافته]
```

## جریان داده

### نشست CLI

```
ورودی کاربر → HermesCLI.process_input()  → AIAgent.run_conversation()    → prompt_builder.build_system_prompt()    → runtime_provider.resolve_runtime_provider()    → فراخوانی API (chat_completions / codex_responses / anthropic_messages)    → tool_calls? → model_tools.handle_function_call() → حلقه    → پاسخ نهایی → نمایش → ذخیره در SessionDB
```

### پیام Gateway

```
رویداد پلتفرم → Adapter.on_message() → MessageEvent  → GatewayRunner._handle_message()    → احراز هویت کاربر    → حل کلید نشست    → ایجاد AIAgent با تاریخچه نشست    → AIAgent.run_conversation()    → تحویل پاسخ از طریق adapter
```

### وظیفه Cron

```
تیک زمان‌بند → بارگذاری وظایف سررسید از jobs.json  → ایجاد AIAgent تازه (بدون تاریخچه)  → تزریق مهارت‌های پیوست‌شده به عنوان context  → اجرای prompt وظیفه  → تحویل پاسخ به پلتفرم هدف  → به‌روزرسانی وضعیت وظیفه و next_run
```

## ترتیب خواندن پیشنهادی

اگر با مخزن کد جدید هستید:

1. این صفحه — جهت‌یابی کنید
2. ساختار داخلی حلقه agent — نحوه کار AIAgent
3. مونتاژ prompt — ساخت system prompt
4. حل زمان‌بند runtime ارائه‌دهنده — نحوه انتخاب ارائه‌دهندگان
5. اضافه کردن ارائه‌دهندگان — راهنمای عملی برای اضافه کردن ارائه‌دهنده جدید
6. زمان‌بند ابزار — ثبت‌نام ابزار، مسیریابی، محیط‌ها
7. ذخیره‌سازی نشست — schema SQLite، FTS5، تاریخچه نشست
8. ساختار داخلی Gateway — دروازه پلتفرم پیام‌رسانی
9. فشرده‌سازی context و کش prompt — فشرده‌سازی و کشینگ
10. ساختار داخلی ACP — ادغام IDE

[ساختار داخلی حلقه agent](/docs/developer-guide/agent-loop)
[مونتاژ prompt](/docs/developer-guide/prompt-assembly)
[حل زمان‌بند runtime ارائه‌دهنده](/docs/developer-guide/provider-runtime)
[اضافه کردن ارائه‌دهندگان](/docs/developer-guide/adding-providers)
[زمان‌بند ابزار](/docs/developer-guide/tools-runtime)
[ذخیره‌سازی نشست](/docs/developer-guide/session-storage)
[ساختار داخلی Gateway](/docs/developer-guide/gateway-internals)
[فشرده‌سازی context و کش prompt](/docs/developer-guide/context-compression-and-caching)
[ساختار داخلی ACP](/docs/developer-guide/acp-internals)

## زیرسیستم‌های اصلی

### حلقه agent

موتور ارکستراسیون همزمان (`AIAgent` در `run_agent.py`). انتخاب ارائه‌دهنده، ساخت prompt، اجرای ابزار، تلاش‌های مجدد، بازگشت، callbackها، فشرده‌سازی و ماندگاری را مدیریت می‌کند. از سه حالت API برای پشتیبان‌های مختلف ارائه‌دهنده پشتیبانی می‌کند.

`AIAgent`
`run_agent.py`

→ ساختار داخلی حلقه agent

[ساختار داخلی حلقه agent](/docs/developer-guide/agent-loop)

### سیستم Prompt

ساخت و نگهداری prompt در طول چرخه حیات مکالمه:

- `system_prompt.py` + `prompt_builder.py` — لایه‌های مرتب‌شده system prompt (پایدار → context → متغیر) را مونتاژ می‌کند: هویت/راهنمایی ابزار/مهارت‌ها، فایل‌های context، سپس بلوک‌های حافظه/نشست/برچسب زمانی
- `prompt_caching.py` — نقاط توقف کش Anthropic را برای کش prefix اعمال می‌کند
- `context_compressor.py` — گردش‌های میانی مکالمه را وقتی context از آستانه‌ها فراتر می‌رود خلاصه می‌کند

`system_prompt.py`
`prompt_builder.py`
`stable`
`context`
`volatile`
`prompt_caching.py`
`context_compressor.py`

→ مونتاژ prompt، فشرده‌سازی context و کش prompt

[مونتاژ prompt](/docs/developer-guide/prompt-assembly)
[فشرده‌سازی context و کش prompt](/docs/developer-guide/context-compression-and-caching)

### حل ارائه‌دهنده

یک حل‌کننده زمان‌بند مشترک که توسط CLI، gateway، cron، ACP و فراخوانی‌های کمکی استفاده می‌شود. tuples `(provider, model)` را به `(api_mode, api_key, base_url)` نگاشت می‌کند. بیش از ۱۸ ارائه‌دهنده، جریان‌های OAuth، استخرهای اعتبارنامه و حل نام مستعار را مدیریت می‌کند.

`(provider, model)`
`(api_mode, api_key, base_url)`

→ حل زمان‌بند runtime ارائه‌دهنده

[حل زمان‌بند runtime ارائه‌دهنده](/docs/developer-guide/provider-runtime)

### سیستم ابزار

ثبت‌نام مرکزی ابزار (`tools/registry.py`) با بیش از ۷۰ ابزار ثبت‌شده در حدود ۲۸ مجموعه ابزار. هر فایل ابزار در زمان import ثبت‌نام می‌کند. ثبت‌نام جمع‌آوری schema، مسیریابی، بررسی در دسترس بودن و بسته‌بندی خطا را مدیریت می‌کند. ابزارهای ترمینال از ۶ پشتیبان (local، Docker، SSH، Daytona، Modal، Singularity) پشتیبانی می‌کنند.

`tools/registry.py`

→ زمان‌بند ابزار

[زمان‌بند ابزار](/docs/developer-guide/tools-runtime)

### ماندگاری نشست

ذخیره‌سازی نشست مبتنی بر SQLite با جستجوی متن کامل FTS5. نشست‌ها دارای ردیابی تاریخچه (والد/فرزند در فشرده‌سازی‌ها)، ایزولاسیون به ازای هر پلتفرم و نوشتارهای اتمی با مدیریت رقابت هستند.

→ ذخیره‌سازی نشست

[ذخیره‌سازی نشست](/docs/developer-guide/session-storage)

### دروازه پیام‌رسانی

پروسه طولانی‌مدت با ۲۰ adapter پلتفرم، مسیریابی نشست یکپارچه، احراز هویت کاربر (لیست‌های مجاز + جفت‌سازی DM)، مسیریابی دستور اسلش، سیستم hook، تیک cron و نگهداری پس‌زمینه.

→ ساختار داخلی Gateway

[ساختار داخلی Gateway](/docs/developer-guide/gateway-internals)

### سیستم افزونه

سه منبع کشف: `~/.hermes/plugins/` (کاربر)، `.hermes/plugins/` (پروژه) و نقاط ورود pip. افزونه‌ها ابزارها، hookها و دستورات CLI را از طریق یک API context ثبت‌نام می‌کنند. دو نوع افزونه تخصصی وجود دارد: ارائه‌دهندگان حافظه (`plugins/memory/`) و موتورهای context (`plugins/context_engine/`). هر دو تک‌انتخابی هستند — فقط یکی از هر کدام می‌تواند در یک زمان فعال باشد، از طریق `hermes plugins` یا `config.yaml` پیکربندی می‌شود.

`~/.hermes/plugins/`
`.hermes/plugins/`
`plugins/memory/`
`plugins/context_engine/`
`hermes plugins`
`config.yaml`

→ راهنمای افزونه، افزونه ارائه‌دهنده حافظه

[راهنمای افزونه](/docs/developer-guide/plugins)
[افزونه ارائه‌دهنده حافظه](/docs/developer-guide/memory-provider-plugin)

### Cron

وظایف agent درجه اول (نه وظایف shell). وظایف در JSON ذخیره می‌شوند، از قالب‌های زمان‌بندی متعدد پشتیبانی می‌کنند، می‌توانند مهارت‌ها و اسکریپت‌ها را پیوست کنند و به هر پلتفرم تحویل داده شوند.

→ ساختار داخلی Cron

[ساختار داخلی Cron](/docs/developer-guide/cron-internals)

### ادغام ACP

Hermes را به عنوان یک agent بومی ویرایشگر از طریق stdio/JSON-RPC برای VS Code، Zed و JetBrains در معرض دید قرار می‌دهد.

→ ساختار داخلی ACP

[ساختار داخلی ACP](/docs/developer-guide/acp-internals)

### Trajectoryها

Trajectoryهای قالب ShareGPT را از نشست‌های agent برای تولید داده آموزشی تولید می‌کند.

→ Trajectory و قالب آموزشی

[Trajectory و قالب آموزشی](/docs/developer-guide/trajectory-format)

## اصول طراحی

| اصل | معنای عملی |
| --- | --- |
| پایداری prompt | System prompt در وسط مکالمه تغییر نمی‌کند. بدون جهش‌های شکننده کش مگر اقدامات صریح کاربر (`/model`). |
| اجرای قابل مشاهده | هر فراخوانی ابزار از طریق callbackها برای کاربر قابل مشاهده است. به‌روزرسانی‌های پیشرفت در CLI (spiner) و gateway (پیام‌های چت). |
| قابل وقف | فراخوانی‌های API و اجرای ابزار می‌توانند در حین پرواز توسط ورودی کاربر یا سیگنال‌ها لغو شوند. |
| هسته بی‌تفاوت به پلتفرم | یک کلاس AIAgent از CLI، gateway، ACP، batch و API server خدمت می‌دهد. تفاوت‌های پلتفرم در نقطه ورود زندگی می‌کنند، نه در agent. |
| اتصال سست | زیرسیستم‌های اختیاری (MCP، افزونه‌ها، ارائه‌دهندگان حافظه، محیط‌های RL) از الگوهای ثبت‌نام و gating check_fn استفاده می‌کنند، نه وابستگی‌های سخت. |
| ایزولاسیون نشست | هر نشست (`hermes -p <name>`) HERMES_HOME، config، حافظه، نشست‌ها و PID gateway خود را دارد. چندین نشست به طور همزمان اجرا می‌شوند. |

`/model`
`hermes -p <name>`

## زنجیره وابستگی فایل

```
tools/registry.py  (بدون وابستگی — توسط تمام فایل‌های ابزار import می‌شود)       ↑tools/*.py  (هر کدام در زمان import registry.register() را فراخوانی می‌کنند)       ↑model_tools.py  (tools/registry را import + کشف ابزار را تحریک می‌کند)       ↑run_agent.py, cli.py, batch_runner.py, environments/
```

این زنجیره به این معنی است که ثبت‌نام ابزار در زمان import اتفاق می‌افتد، قبل از ایجاد هر نمونه agent. هر فایل `tools/*.py` با فراخوانی `registry.register()` در سطح بالا به طور خودکار کشف می‌شود — نیازی به لیست import دستی نیست.

`tools/*.py`
`registry.register()`
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/developer-guide/architecture.md)
