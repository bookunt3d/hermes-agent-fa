---
layout: docs
title: "فایل‌های زمینه"
permalink: /docs/user-guide/features/context-files/
---

- 
- قابلیت‌ها
- هسته
- فایل‌های زمینه

# فایل‌های زمینه

Hermes Agent به طور خودکار فایل‌های زمینه‌ای را کشف و بارگذاری می‌کند که نحوه رفتارش را شکل می‌دهند. برخی پروژه‌محور هستند و از دایرکتوری کاری شما کشف می‌شوند. `SOUL.md` اکنون برای کل نمونه Hermes سراسری است و فقط از `HERMES_HOME` بارگذاری می‌شود.

`SOUL.md`
`HERMES_HOME`

## فایل‌های زمینه پشتیبانی‌شده

| فایل | هدف | کشف |
| --- | --- | --- |
| `.hermes.md`/`HERMES.md` | دستورالعمل‌های پروژه (بالاترین اولویت) | تا ریشه git پیمایش می‌کند |
| `AGENTS.md` | دستورالعمل‌های پروژه، قراردادها، معماری | CWD در شروع + زیرفهرست‌ها به تدریج |
| `CLAUDE.md` | فایل‌های زمینه Claude Code (همچنین تشخیص داده می‌شود) | CWD در شروع + زیرفهرست‌ها به تدریج |
| `SOUL.md` | شخصیت و لحن سراسری برای این نمونه Hermes | فقط `HERMES_HOME/SOUL.md` |
| `.cursorrules` | قراردادهای کدنویسی Cursor IDE | فقط CWD |
| `.cursor/rules/*.mdc` | ماژول‌های قانون Cursor IDE | فقط CWD |

`HERMES_HOME/SOUL.md`

فقط **یک** نوع زمینه پروژه در هر جسست بارگذاری می‌شود (اولین تطابق برنده است): `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`. `SOUL.md` همیشه به طور مستقل به عنوان هویت عامل (اسلات #1) بارگذاری می‌شود.

`.hermes.md`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`

## AGENTS.md

`AGENTS.md` فایل اصلی زمینه پروژه است. به عامل می‌گوید پروژه شما چگونه ساختار یافته، چه قراردادهایی را رعایت کند و هر دستورالعمل خاصی.

`AGENTS.md`

### کشف تدریجی زیرفهرست

در شروع نشست، Hermes `AGENTS.md` را از دایرکتوری کاری شما در پرامپت سیستم بارگذاری می‌کند. وقتی عامل در طول نشست به زیرفهرست‌ها ناوبری می‌کند (از طریق `read_file`، `terminal`، `search_files` و غیره)، فایل‌های زمینه در آن دایرکتوری‌ها را **به تدریج کشف** می‌کند و آن‌ها را در لحظه‌ای که مرتبط می‌شوند به مکالمه تزریق می‌کند.

`AGENTS.md`
`read_file`
`terminal`
`search_files`

```
my-project/
├── AGENTS.md              ← Loaded at startup (system prompt)
├── frontend/
│   └── AGENTS.md          ← Discovered when agent reads frontend/ files
├── backend/
│   └── AGENTS.md          ← Discovered when agent reads backend/ files
└── shared/
    └── AGENTS.md          ← Discovered when agent reads shared/ files
```

این رویکرد دو مزیت نسبت به بارگذاری همه چیز در شروع دارد:

- **بدون بزرگ شدن پرامپت سیستم** — نکات زیرفهرست فقط در صورت نیاز ظاهر می‌شوند
- **حفظ کش پرامپت** — پرامپت سیستم در نوبت‌ها پایدار باقی می‌ماند

هر زیرفهرست حداکثر یک بار در هر نشست بررسی می‌شود. کشف همچنین دایرکتوری‌های والد را پیمایش می‌کند، بنابراین خواندن `backend/src/main.py` فایل `backend/AGENTS.md` را کشف می‌کند حتی اگر `backend/src/` فایل زمینه خاص خود را نداشته باشد.

`backend/src/main.py`
`backend/AGENTS.md`
`backend/src/`

فایل‌های زمینه زیرفهرست از **اسکن امنیتی** یکسانی با فایل‌های زمینه شروع عبور می‌کنند. فایل‌های مخرب مسدود می‌شوند.

### نمونه AGENTS.md

```
# Project Context
This is a Next.js 14 web application with a Python FastAPI backend.

## Architecture
- Frontend: Next.js 14 with App Router in `/frontend`
- Backend: FastAPI in `/backend`, uses SQLAlchemy ORM
- Database: PostgreSQL 16
- Deployment: Docker Compose on a Hetzner VPS

## Conventions
- Use TypeScript strict mode for all frontend code
- Python code follows PEP 8, use type hints everywhere
- All API endpoints return JSON with `{data, error, meta}` shape
- Tests go in `__tests__/` directories (frontend) or `tests/` (backend)

## Important Notes
- Never modify migration files directly — use Alembic commands
- The `.env.local` file has real API keys, don't commit it
- Frontend port is 3000, backend is 8000, DB is 5432
```

## SOUL.md

`SOUL.md` شخصیت، لحن و سبک ارتباطی عامل را کنترل می‌کند. برای جزئیات کامل به صفحه [شخصیت](/docs/user-guide/features/personality) مراجعه کنید.

`SOUL.md`
[شخصیت](/docs/user-guide/features/personality)

محل قرارگیری:

- `~/.hermes/SOUL.md`
- یا `$HERMES_HOME/SOUL.md` اگر Hermes را با یک دایرکتوری خانه سفارشی اجرا می‌کنید

`~/.hermes/SOUL.md`
`$HERMES_HOME/SOUL.md`

نکات مهم:

- Hermes اگر هنوز `SOUL.md` وجود نداشته باشد یک `SOUL.md` پیش‌فرض به طور خودکار ایجاد می‌کند
- Hermes فقط از `HERMES_HOME` `SOUL.md` بارگذاری می‌کند
- Hermes دایرکتوری کاری را برای `SOUL.md` جستجو نمی‌کند
- اگر فایل خالی باشد، چیزی از `SOUL.md` به پرامپت اضافه نمی‌شود
- اگر فایل محتوا داشته باشد، محتوا پس از اسکن و برش‌خوردن word-for-word تزریق می‌شود

`SOUL.md`
`SOUL.md`
`HERMES_HOME`
`SOUL.md`
`SOUL.md`

## .cursorrules

Hermes با فایل `.cursorrules` و ماژول‌های قانون `.cursor/rules/*.mdc` Cursor IDE سازگار است. اگر این فایل‌ها در ریشه پروژه شما وجود داشته باشند و فایل زمینه با اولویت بالاتری (`.hermes.md`، `AGENTS.md` یا `CLAUDE.md`) یافت نشود، به عنوان زمینه پروژه بارگذاری می‌شوند.

`.cursorrules`
`.cursor/rules/*.mdc`
`.hermes.md`
`AGENTS.md`
`CLAUDE.md`

این به این معنی است که قراردادهای موجود Cursor شما هنگام استفاده از Hermes به طور خودکار اعمال می‌شوند.

## نحوه بارگذاری فایل‌های زمینه

### در شروع (پرامپت سیستم)

فایل‌های زمینه توسط `build_context_files_prompt()` در `agent/prompt_builder.py` بارگذاری می‌شوند:

`build_context_files_prompt()`
`agent/prompt_builder.py`

1. **اسکن دایرکتوری کاری** — `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` را بررسی می‌کند (اولین تطابق برنده است)
2. **خواندن محتوا** — هر فایل به عنوان متن UTF-8 خوانده می‌شود
3. **اسکن امنیتی** — محتوا برای الگوهای تزریق پرامپت بررسی می‌شود
4. **برش** — فایل‌هایی که از `context_file_max_chars` کاراکتر (پیش‌فرض 20,000) تجاوز می‌کنند از ابتدا و انتها برش می‌خورند (70% از ابتدا، 20% از انتها، با یک نشانگر در وسط)
5. **مونتاژ** — همه بخش‌ها تحت هدر `# Project Context` ترکیب می‌شوند
6. **تزریق** — محتوای مونتاژشده به پرامپت سیستم اضافه می‌شود

`.hermes.md`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`
`context_file_max_chars`
`# Project Context`

### در طول نشست (کشف تدریجی)

`SubdirectoryHintTracker` در `agent/subdirectory_hints.py` آرگومان‌های فراخوانی ابزار را برای مسیرهای فایل تماشا می‌کند:

`SubdirectoryHintTracker`
`agent/subdirectory_hints.py`

1. **استخراج مسیر** — پس از هر فراخوانی ابزار، مسیرهای فایل از آرگومان‌ها استخراج می‌شوند (`path`، `workdir`، دستورات shell)
2. **پیمایش نیاکان** — دایرکتوری و تا 5 دایرکتوری والد بررسی می‌شوند (در دایرکتوری‌های قبلاً بازدیدشده متوقف می‌شود)
3. **بارگذاری نکته** — اگر `AGENTS.md`، `CLAUDE.md` یا `.cursorrules` یافت شود، بارگذاری می‌شود (اولین تطابق به ازای هر دایرکتوری)
4. **اسکن امنیتی** — همان اسکن تزریق پرامپت فایل‌های شروع
5. **برش** — حداکثر 8,000 کاراکتر به ازای هر فایل
6. **تزریق** — به نتیجه ابزار اضافه می‌شود تا مدل آن را به طور طبیعی در زمینه ببیند

`path`
`workdir`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`

بخش پرامپت نهایی تقریباً این شکل را دارد:

```
# Project Context
The following project context files have been loaded and should be followed:

## AGENTS.md
[Your AGENTS.md content here]

## .cursorrules
[Your .cursorrules content here]

[Your SOUL.md content here]
```

توجه کنید که محتوای SOUL مستقیماً درج می‌شود، بدون متن wrapper اضافی.

## امنیت: محافظت در برابر تزریق پرامپت

همه فایل‌های زمینه قبل از درج برای تزریق بالقوه پرامپت اسکن می‌شوند. اسکنر بررسی می‌کند:

- **تلاش‌های بازنویسی دستورالعمل**: "ignore previous instructions"، "disregard your rules"
- **الگوهای فریبکاری**: "do not tell the user"
- **بازنویسی پرامپت سیستم**: "system prompt override"
- **نظرات HTML مخفی**: `<!-- ignore instructions -->`
- **عناصر div مخفی**: `<div style="display:none">`
- **سرقت اعتبارات**: `curl ... $API_KEY`
- **دسترسی به فایل‌های رمز**: `cat .env`، `cat credentials`
- **کاراکترهای نامرئی**: فاصله‌های عرض صفر، بازنویسی‌های دوجهته، word joiner‌ها

`<!-- ignore instructions -->`
`<div style="display:none">`
`curl ... $API_KEY`
`cat .env`
`cat credentials`

اگر هر الگوی تهدیدی تشخیص داده شود، فایل مسدود می‌شود:

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

این اسکنر در برابر الگوهای رایج تزریق محافظت می‌کند، اما جایگزینی برای بررسی فایل‌های زمینه در مخزن‌های مشترک نیست. همیشه محتوای AGENTS.md را در پروژه‌هایی که خودتان نویسنده آن نیستید تأیید کنید.

## محدودیت‌های اندازه

| محدودیت | مقدار |
| --- | --- |
| حداکثر کاراکتر به ازای هر فایل | `context_file_max_chars` (پیش‌فرض 20,000، ~7,000 توکن) |
| نسبت برش از ابتدا | 70% |
| نسبت برش از انتها | 20% |
| نشانگر برش | 10% (شمارش کاراکترها را نشان می‌دهد و استفاده از ابزارهای فایل را پیشنهاد می‌دهد) |

`context_file_max_chars`

وقتی فایل از محدودیت پیکربندی‌شده تجاوز کند، پیام برش به صورت زیر است:

```
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```

## نکاتی برای فایل‌های زمینه مؤثر

1. **مختصر باشید** — زیر `context_file_max_chars` پیکربندی‌شده خود بمانید؛ عامل آن را در هر نوبت می‌خواند
2. **با هدرها ساختار دهید** — از بخش‌های `##` برای معماری، قراردادها، نکات مهم استفاده کنید
3. **مثال‌های مشخص وارد کنید** — الگوهای کد ترجیحی، شکل‌های API، قراردادهای نام‌گذاری را نشان دهید
4. **ذکر کنید چه کاری نکنید** — "هرگز مستقیماً فایل‌های migration را ویرایش نکنید"
5. **مسیرها و پورت‌های کلیدی را فهرست کنید** — عامل از این‌ها برای دستورات terminal استفاده می‌کند
6. **با تکامل پروژه به‌روز کنید** — زمینه قدیمی بدتر از بدون زمینه است

`context_file_max_chars`
`##`

### زمینه به ازای هر زیرفهرست

برای monorepo‌ها، دستورالعمل‌های مخصوص زیرفهرست را در فایل‌های تو در تو `AGENTS.md` قرار دهید:

```
<!-- frontend/AGENTS.md -->
# Frontend Context
- Use `pnpm` not `npm` for package management
- Components go in `src/components/`, pages in `src/app/`
- Use Tailwind CSS, never inline styles
- Run tests with `pnpm test`
```

```
<!-- backend/AGENTS.md -->
# Backend Context
- Use `poetry` for dependency management
- Run the dev server with `poetry run uvicorn main:app --reload`
- All endpoints need OpenAPI docstrings
- Database models are in `models/`, schemas in `schemas/`
```

[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/context-files.md)