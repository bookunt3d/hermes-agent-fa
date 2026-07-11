---
layout: docs
title: "شخصیت"
permalink: /docs/user-guide/features/personality/
---

- 
- Features
- Core
- Personality & SOUL.md

# شخصیت و SOUL.md

شخصیت Hermes Agent کاملاً قابل سفارشی‌سازی است. `SOUL.md` هویت اصلی است — اولین چیزی که در system prompt قرار می‌گیرد و تعریف می‌کند agent کیست.

`SOUL.md`
- SOUL.md — یک فایل هویت پایدار که در `HERMES_HOME` زندگی می‌کند و به عنوان هویت agent عمل می‌کند (جایگاه شماره ۱ در system prompt)
- شخصیت‌های از پیش تعریف‌شده یا سفارشی (`/personality`) — overlayهای سطح نشست در system prompt

`SOUL.md`
`HERMES_HOME`
`/personality`

اگر می‌خواهید هویت Hermes را تغییر دهید — یا آن را با یک شخصیت کاملاً متفاوت جایگزین کنید — `SOUL.md` را ویرایش کنید.

`SOUL.md`

## نحوه کار SOUL.md در حال حاضر

Hermes در حال حاضر یک `SOUL.md` پیش‌فرض به صورت خودکار در مسیر زیر ایجاد می‌کند:

`SOUL.md`

```
~/.hermes/SOUL.md
```

دقیق‌تر، از `HERMES_HOME` نمونه فعلی استفاده می‌کند، بنابراین اگر Hermes را با یک دایرکتوری خانه سفارشی اجرا کنید، از مسیر زیر استفاده خواهد کرد:

`HERMES_HOME`

```
$HERMES_HOME/SOUL.md
```

### رفتار مهم

- SOUL.md هویت اصلی agent است. این فایل جایگاه شماره ۱ در system prompt را اشغال می‌کند و هویت پیش‌فرض سخت‌کد شده را جایگزین می‌کند.
- Hermes در صورت عدم وجود SOUL.md، به صورت خودکار یک فایل شروع ایجاد می‌کند
- فایل‌های SOUL.md موجود کاربر هرگز بازنویسی نمی‌شوند
- Hermes فقط از `HERMES_HOME` فایل SOUL.md را بارگذاری می‌کند
- Hermes در دایرکتوری کاری جاری به دنبال SOUL.md نمی‌گردد
- اگر SOUL.md وجود داشته باشد اما خالی باشد، یا قابل بارگذاری نباشد، Hermes به هویت پیش‌فرض داخلی بازمی‌گردد
- اگر SOUL.md دارای محتوا باشد، این محتوا پس از اسکن امنیتی و برش، عیناً تزریق می‌شود
- SOUL.md در بخش فایل‌های context تکرار نمی‌شود — فقط یک بار به عنوان هویت ظاهر می‌شود

`SOUL.md`
`SOUL.md`
`SOUL.md`
`HERMES_HOME`
`SOUL.md`
`SOUL.md`
`SOUL.md`

این باعث می‌شود SOUL.md یک هویت واقعی به ازای هر کاربر یا هر نمونه باشد، نه فقط یک لایه اضافی.

`SOUL.md`

## چرا این طراحی؟

این کار شخصیت را قابل پیش‌بینی نگه می‌دارد.

اگر Hermes فایل SOUL.md را از هر دایرکتوری‌ای که اتفاقاً آن را راه‌اندازی کنید بارگذاری کند، شخصیت شما ممکن است به طور غیرمنتظره بین پروژه‌ها تغییر کند. با بارگذاری فقط از `HERMES_HOME`، شخصیت متعلق به خود نمونه Hermes است.

`SOUL.md`
`HERMES_HOME`

این همچنین آموزش به کاربران را آسان‌تر می‌کند:

- "~/.hermes/SOUL.md را ویرایش کنید تا شخصیت پیش‌فرض Hermes را تغییر دهید."

`~/.hermes/SOUL.md`

## کجا آن را ویرایش کنیم

برای اکثر کاربران:

```
~/.hermes/SOUL.md
```

اگر از یک home سفارشی استفاده می‌کنید:

```
$HERMES_HOME/SOUL.md
```

## چه چیزی باید در SOUL.md قرار گیرد؟

از آن برای راهنمایی‌های دائمی صدا و شخصیت استفاده کنید، مانند:

- لحن
- سبک ارتباط
- سطح مستقیم بودن
- سبک تعامل پیش‌فرض
- آنچه باید از نظر سبک اجتناب شود
- نحوه مدیریت عدم قطعیت، اختلاف نظر یا ابهام توسط Hermes

از آن کمتر برای موارد زیر استفاده کنید:

- دستورالعمل‌های پروژه یک‌بار مصرف
- مسیرهای فایل
- قراردادهای repo
- جزئیات موقتی workflow

اینها به `AGENTS.md` تعلق دارند، نه `SOUL.md`.

`AGENTS.md`
`SOUL.md`

## محتوای خوب SOUL.md

یک فایل SOUL خوب:

- در سراسر contextها پایدار است
- به اندازه کافی گسترده است تا در بسیاری از مکالمات اعمال شود
- به اندازه کافی خاص است تا صدا را به طور مادی شکل دهد
- بر ارتباطات و هویت متمرکز است، نه دستورالعمل‌های مرتبط با تسک

### مثال

```
# PersonalityYou are a pragmatic senior engineer with strong taste.You optimize for truth, clarity, and usefulness over politeness theater.## Style- Be direct without being cold- Prefer substance over filler- Push back when something is a bad idea- Admit uncertainty plainly- Keep explanations compact unless depth is useful## What to avoid- Sycophancy- Hype language- Repeating the user's framing if it's wrong- Overexplaining obvious things## Technical posture- Prefer simple systems over clever systems- Care about operational reality, not idealized architecture- Treat edge cases as part of the design, not cleanup
```

## آنچه Hermes در prompt تزریق می‌کند

محتوای SOUL.md مستقیماً به جایگاه شماره ۱ system prompt — موقعیت هویت agent — می‌رود. هیچ زبان بسته‌بندی اطراف آن اضافه نمی‌شود.

`SOUL.md`

محتوا از مراحل زیر عبور می‌کند:

- اسکن prompt injection
- برش در صورت بزرگ بودن

اگر فایل خالی باشد، فقط شامل فاصله باشد، یا قابل خواندن نباشد، Hermes به هویت پیش‌فرض داخلی بازمی‌گردد («شما Hermes Agent، یک دستیار هوش مصنوعی هوشمند ساخته شده توسط Nous Research هستید...»). این بازگشت همچنین زمانی اعمال می‌شود که `skip_context_files` تنظیم شده باشد (مثلاً در contextهای subagent/delegation).

`skip_context_files`

## اسکن امنیتی

SOUL.md مانند سایر فایل‌های حاوی context قبل از درج برای الگوهای prompt injection اسکن می‌شود.

`SOUL.md`

این به این معنی است که همچنان باید آن را بر روی شخصیت/صدا متمرکز نگه دارید و سعی نکنید دستورالعمل‌های عجیب متا را در آن قرار دهید.

## SOUL.md در مقابل AGENTS.md

این مهم‌ترین تمایز است.

### SOUL.md

برای موارد زیر استفاده کنید:

- هویت
- لحن
- سبک
- پیش‌فرض‌های ارتباطی
- رفتار در سطح شخصیت

### AGENTS.md

برای موارد زیر استفاده کنید:

- معماری پروژه
- قراردادهای کدنویسی
- ترجیحات ابزار
- workflowهای خاص repo
- دستورات، پورت‌ها، مسیرها، یادداشت‌های استقرار

یک قانون مفید:

- اگر باید همه جا همراه شما باشد، به SOUL.md تعلق دارد
- اگر به یک پروژه تعلق دارد، به AGENTS.md تعلق دارد

`SOUL.md`
`AGENTS.md`

## SOUL.md در مقابل `/personality`

`/personality`

SOUL.md شخصیت پیش‌فرض پایدار شماست.

`SOUL.md`

`/personality` یک overlay سطح نشست است که system prompt فعلی را تغییر یا تکمیل می‌کند.

`/personality`

پس:

- SOUL.md = صدای پایه
- `/personality` = تغییر حالت موقت

`SOUL.md`
`/personality`

مثال‌ها:

- یک SOUL پیش‌فرض عملی نگه دارید، سپس از `/personality teacher` برای مکالمه آموزشی استفاده کنید
- یک SOUL مختصر نگه دارید، سپس از `/personality creative` برای طوفان فکری استفاده کنید

`/personality teacher`
`/personality creative`

## شخصیت‌های داخلی

Hermes با شخصیت‌های داخلی ارائه می‌شود که می‌توانید با `/personality` به آنها سوئیچ کنید.

`/personality`

| نام | توضیحات |
| --- | --- |
| helpful | دستیار دوستانه و همه‌کاره |
| concise | پاسخ‌های مختصر و مستقیم |
| technical | متخصص فنی دقیق و مفصل |
| creative | نوآورانه و خلاقانه |
| teacher | مربی صبور با مثال‌های واضح |
| kawaii | بیانات بامزه، درخشش و شور و شوق ★ |
| catgirl | Neko-chan با بیانات گربه‌ای، nya~ |
| pirate | کاپیتان هرمس، دزد دریایی فنی |
| shakespeare | نثر شاعرانه با جذابیت نمایشی |
| surfer | وibes خونسرد برادرانه |
| noir | روایت کارآگاه سرسخت |
| uwu | حداکثر بامزگی با uwu-speak |
| philosopher | تأمل عمیق در هر پرسش |
| hype | حداکثر انرژی و شور و شوق!!! |

## سوئیچ بین شخصیت‌ها با دستورات

### CLI

```
/personality/personality concise/personality technical
```

### پلتفرم‌های پیام‌رسانی

```
/personality teacher
```

اینها overlayهای راحتی هستند، اما SOUL.md جهانی شما همچنان به Hermes شخصیت پیش‌فرض ماندگار آن را می‌دهد مگر اینکه overlay آن را به طور معناداری تغییر دهد.

`SOUL.md`

## شخصیت‌های سفارشی در config

همچنین می‌توانید شخصیت‌های سفارشی نام‌دار را در `~/.hermes/config.yaml` تحت `agent.personalities` تعریف کنید.

`~/.hermes/config.yaml`
`agent.personalities`

```
agent:  personalities:    codereviewer: >      You are a meticulous code reviewer. Identify bugs, security issues,      performance concerns, and unclear design choices. Be precise and constructive.
```

سپس برای سوئیچ به آن:

```
/personality codereviewer
```

## workflow پیشنهادی

یک تنظیم قوی پیش‌فرض:

1. یک SOUL.md جهانی با دقت در `~/.hermes/SOUL.md` نگه دارید
2. دستورالعمل‌های پروژه را در AGENTS.md قرار دهید
3. فقط زمانی از `/personality` استفاده کنید که به یک تغییر حالت موقت نیاز دارید

`SOUL.md`
`~/.hermes/SOUL.md`
`AGENTS.md`
`/personality`

این به شما می‌دهد:

- یک صدای پایدار
- رفتار مختص پروژه در جای خود
- کنترل موقت در صورت نیاز

## نحوه تعامل شخصیت با prompt کامل

در سطح بالا، پشته prompt شامل موارد زیر است:

1. SOUL.md (هویت agent — یا بازگشت داخلی اگر SOUL.md در دسترس نباشد)
2. راهنمایی رفتار مبتنی بر ابزار
3. حافظه / context کاربر
4. راهنمایی مهارت‌ها
5. فایل‌های context (AGENTS.md، .cursorrules)
6. برچسب زمانی
7. نکات قالب‌بندی خاص پلتفرم
8. overlayهای اختیاری system prompt مانند `/personality`

`AGENTS.md`
`.cursorrules`
`/personality`

SOUL.md پایه است — همه چیزهای دیگر بر روی آن ساخته می‌شود.

`SOUL.md`

## اسناد مرتبط

- فایل‌های Context
- پیکربندی
- نکات و بهترین شیوه‌ها
- راهنمای SOUL.md

[فایل‌های Context](/docs/user-guide/features/context-files/)
[پیکربندی](/docs/user-guide/configuration/)
[نکات و بهترین شیوه‌ها](/docs/guides/tips/)
[راهنمای SOUL.md](/docs/guides/use-soul-with-hermes/)

## ظاهر CLI در مقابل شخصیت مکالمه‌ای

شخصیت مکالمه‌ای و ظاهر CLI از هم جدا هستند:

- SOUL.md، `agent.system_prompt` و `/personality` بر نحوه صحبت کردن Hermes تأثیر می‌گذارند
- `display.skin` و `/skin` بر نحوه ظاهر شدن Hermes در ترمینال تأثیر می‌گذارند

`SOUL.md`
`agent.system_prompt`
`/personality`
`display.skin`
`/skin`

برای ظاهر ترمینال، به پوسته‌ها و تم‌ها مراجعه کنید.

[پوسته‌ها و تم‌ها](/docs/user-guide/features/skins/)
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/personality.md)
