---
layout: docs
title: "مسیر یادگیری"
permalink: /docs/getting-started/learning-path/
---

- 
- Getting Started
- Learning Path

# مسیر یادگیری

Hermes Agent کارهای زیادی می‌تواند انجام دهد — دستیار خط فرمان، ربات Telegram/Discord، اتوماسیون وظایف، آموزش RL و موارد دیگر. این صفحه به شما کمک می‌کند بر اساس سطح تجربه و آنچه می‌خواهید انجام دهید، بفهمید از کجا شروع کنید و چه چیزی بخوانید.

اگر هنوز Hermes Agent را نصب نکرده‌اید، با [راهنمای نصب](/docs/getting-started/installation/) شروع کنید و سپس [شروع سریع](/docs/getting-started/quickstart/) را اجرا کنید. همه چیز در زیر فرض می‌کند نصب کاربردی دارید.

کاربران جدید تقریباً همیشه `hermes setup --portal` را می‌خواهند — یک OAuth یک مدل به علاوه چهار ابزار Tool Gateway (جستجو/تصویر/TTS/مرورگر) را پوشش می‌دهد. [Nous Portal](/docs/integrations/nous-portal/) را ببینید.

## چگونه از این صفحه استفاده کنیم

- سطح خود را می‌دانید؟ به [جدول سطح تجربه](#by-experience-level) بروید و ترتیب خواندن برای سطح خود را دنبال کنید.
- هدف مشخصی دارید؟ به [بر اساس مورد استفاده](#by-use-case) بروید و سناریوی متناظر را پیدا کنید.
- فقط مرور می‌کنید؟ [جدول ویژگی‌های کلیدی](#key-features-at-a-glance) را برای نمای کلی سریع همه کارهایی که Hermes Agent می‌تواند انجام دهد ببینید.

## بر اساس سطح تجربه

| سطح | هدف | مطالعه توصیه‌شده | تخمین زمان |
| --- | --- | --- | --- |
| مبتدی | راه‌اندازی، مکالمات پایه، استفاده از ابزارهای داخلی | نصب → شروع سریع → استفاده از CLI → پیکربندی | ~۱ ساعت |
| متوسط | راه‌اندازی ربات‌های پیام‌رسانی، استفاده از ویژگی‌های پیشرفته مانند حافظه، cron و skillها | Sessionها → پیام‌رسانی → ابزارها → Skillها → حافظه → Cron | ~۲-۳ ساعت |
| پیشرفته | ساخت ابزارهای سفارشی، ایجاد skillها، آموزش مدل‌ها با RL، مشارکت در پروژه | معماری → اضافه کردن ابزارها → ایجاد skillها → مشارکت | ~۴-۶ ساعت |

## بر اساس مورد استفاده

سناریویی را انتخاب کنید که با آنچه می‌خواهید انجام دهید مطابقت دارد. هر کدام شما را به مستندات مرتبط به ترتیبی که باید بخوانید لینک می‌کند.

### «یک دستیار کدنویسی CLI می‌خواهم»

از Hermes Agent به عنوان دستیار ترمینال تعاملی برای نوشتن، بررسی و اجرای کد استفاده کنید.

1. [نصب](/docs/getting-started/installation/)
2. [شروع سریع](/docs/getting-started/quickstart/)
3. [استفاده از CLI](/docs/user-guide/cli/)
4. [اجرای کد](/docs/user-guide/features/code-execution/)
5. [فایل‌های Context](/docs/user-guide/features/context-files/)
6. [نکات و ترفندها](/docs/guides/tips/)

فایل‌ها را مستقیماً با فایل‌های context به مکالمه خود وارد کنید. Hermes Agent می‌تواند کد در پروژه‌های شما را بخواند، ویرایش و اجرا کند.

### «یک ربات Telegram/Discord می‌خواهم»

Hermes Agent را به عنوان ربات در پلتفرم پیام‌رسانی مورد علاقه خود مستقر کنید.

1. [نصب](/docs/getting-started/installation/)
2. [پیکربندی](/docs/user-guide/configuration/)
3. [نمای کلی پیام‌رسانی](/docs/user-guide/messaging/)
4. [راه‌اندازی Telegram](/docs/user-guide/messaging/telegram/)
5. [راه‌اندازی Discord](/docs/user-guide/messaging/discord/)
6. [حالت صوتی](/docs/user-guide/features/voice-mode/)
7. [استفاده از حالت صوتی با Hermes](/docs/guides/use-voice-mode-with-hermes/)
8. [امنیت](/docs/user-guide/security/)

برای مثال‌های کامل پروژه، [Daily Briefing Bot](/docs/guides/daily-briefing-bot/) و [Team Telegram Assistant](/docs/guides/team-telegram-assistant/) را ببینید.

### «می‌خواهم وظایف را خودکار کنم']

وظایف تکرارشونده را زمان‌بندی کنید، کارهای دسته‌ای اجرا کنید یا اقدامات agent را به هم زنجیر کنید.

1. [شروع سریع](/docs/getting-started/quickstart/)
2. [زمان‌بندی Cron](/docs/user-guide/features/cron/)
3. [پردازش دسته‌ای](/docs/user-guide/features/batch-processing/)
4. [تفویض](/docs/user-guide/features/delegation/)
5. [ هوک‌ها](/docs/user-guide/features/hooks/)

Cron jobs به Hermes Agent اجازه می‌دهند وظایف را طبق زمان‌بندی اجرا کنند — خلاصه‌های روزانه، بررسی‌های دوره‌ای، گزارش‌های خودکار — بدون حضور شما.

### «می‌خواهم ابزارهای/skillهای سفارشی بسازم»

Hermes Agent را با ابزارها و بسته‌های skill قابل استفاده مجدد خودتان گسترش دهید.

1. [پلاگین‌ها](/docs/user-guide/features/plugins/)
2. [ساخت پلاگین Hermes](/docs/developer-guide/plugins/)
3. [نمای کلی ابزارها](/docs/user-guide/features/tools/)
4. [نمای کلی Skillها](/docs/user-guide/features/skills/)
5. [MCP (Model Context Protocol)](/docs/user-guide/features/mcp/)
6. [معماری](/docs/developer-guide/architecture/)
7. [اضافه کردن ابزارها](/docs/developer-guide/adding-tools/)
8. [ایجاد Skillها](/docs/developer-guide/creating-skills/)

برای بیشتر ساخت ابزارهای سفارشی، با پلاگین‌ها شروع کنید. صفحه [اضافه کردن ابزارها](/docs/developer-guide/adding-tools/) برای توسعه هسته داخلی Hermes است، نه مسیر معمول کاربر/ابزار سفارشی.

### «می‌خواهم مدل‌ها را آموزش دهم»

از یادگیری تقویتی برای تنظیم دقیق رفتار مدل با خط لوله آموزش Hermes Agent RL (قدرت‌گرفته از [Atropos](https://github.com/NousResearch/atropos)) استفاده کنید.

1. [شروع سریع](/docs/getting-started/quickstart/)
2. [پیکربندی](/docs/user-guide/configuration/)
3. [محیط‌های RL Atropos](https://github.com/NousResearch/atropos) (خارجی)
4. [مسیریابی ارائه‌دهنده](/docs/user-guide/features/provider-routing/)
5. [معماری](/docs/developer-guide/architecture/)

آموزش RL بهترین نتیجه را زمانی می‌دهد که قبلاً مبانی نحوه مدیریت مکالمات و فراخوانی ابزارها توسط Hermes Agent را درک کرده باشید. اگر تازه‌کار هستید، ابتدا مسیر مبتدی را طی کنید.

### «می‌خواهم آن را به عنوان کتابخانه Python استفاده کنم»

Hermes Agent را به طور برنامه‌نویسی در برنامه‌های Python خود ادغام کنید.

1. [نصب](/docs/getting-started/installation/)
2. [شروع سریع](/docs/getting-started/quickstart/)
3. [راهنمای کتابخانه Python](/docs/guides/python-library/)
4. [معماری](/docs/developer-guide/architecture/)
5. [ابزارها](/docs/user-guide/features/tools/)
6. [Sessionها](/docs/user-guide/sessions/)

## ویژگی‌های کلیدی در یک نگاه

مطمئن نیستید چه چیزی موجود است؟ این فهرست سریع ویژگی‌های اصلی است:

| ویژگی | چه کاری انجام می‌دهد | لینک |
| --- | --- | --- |
| ابزارها | ابزارهای داخلی که agent می‌تواند فراخوانی کند (ورودی/خروجی فایل، جستجو، shell و غیره) | [ابزارها](/docs/user-guide/features/tools/) |
| Skillها | بسته‌های پلاگین قابل نصب که قابلیت‌های جدید اضافه می‌کنند | [Skillها](/docs/user-guide/features/skills/) |
| حافظه | حافظه پایدار در سراسر sessionها | [حافظه](/docs/user-guide/features/memory/) |
| فایل‌های Context | وارد کردن فایل‌ها و دایرکتوری‌ها به مکالمات | [فایل‌های Context](/docs/user-guide/features/context-files/) |
| MCP | اتصال به سرورهای ابزار خارجی از طریق Model Context Protocol | [MCP](/docs/user-guide/features/mcp/) |
| Cron | زمان‌بندی وظایف تکرارشونده agent | [Cron](/docs/user-guide/features/cron/) |
| تفویض | ایجاد sub-agentها برای کار موازی | [تفویض](/docs/user-guide/features/delegation/) |
| اجرای کد | اجرای اسکریپت‌های Python که ابزارهای Hermes را به طور برنامه‌نویسی فراخوانی می‌کنند | [اجرای کد](/docs/user-guide/features/code-execution/) |
| مرورگر | جستجو و خزش وب | [مرورگر](/docs/user-guide/features/browser/) |
| هوک‌ها | کالبک‌های رویدادمحور و مiddleware | [هوک‌ها](/docs/user-guide/features/hooks/) |
| پردازش دسته‌ای | پردازش ورودی‌های متعدد به صورت دسته‌ای | [پردازش دسته‌ای](/docs/user-guide/features/batch-processing/) |
| مسیریابی ارائه‌دهنده | مسیریابی درخواست‌ها در ارائه‌دهندگان LLM متعدد | [مسیریابی ارائه‌دهنده](/docs/user-guide/features/provider-routing/) |

## قدم بعدی چیست

بر اساس جایی که الان هستید:

- تازه نصب کرده‌اید؟ → به [شروع سریع](/docs/getting-started/quickstart/) بروید تا اولین مکالمه خود را اجرا کنید.
- شروع سریع را تمام کرده‌اید؟ → [استفاده از CLI](/docs/user-guide/cli/) و [پیکربندی](/docs/user-guide/configuration/) را بخوانید تا تنظیمات خود را سفارشی کنید.
- با مبانی راحت هستید؟ → [ابزارها](/docs/user-guide/features/tools/)، [Skillها](/docs/user-guide/features/skills/) و [حافظه](/docs/user-guide/features/memory/) را کاوش کنید تا قدرت کامل agent را باز کنید.
- برای تیم راه‌اندازی می‌کنید؟ → [امنیت](/docs/user-guide/security/) و [Sessionها](/docs/user-guide/sessions/) را بخوانید تا کنترل دسترسی و مدیریت مکالمه را درک کنید.
- آماده ساخت هستید؟ → به [راهنمای توسعه‌دهنده](/docs/developer-guide/architecture/) بپرید تا ساختار داخلی را درک کنید و مشارکت را شروع کنید.
- مثال‌های عملی می‌خواهید؟ → بخش [راهنماها](/docs/guides/tips/) را برای پروژه‌های واقعی و نکات ببینید.

نیازی نیست همه چیز را بخوانید. مسیری را که با هدف شما مطابقت دارد انتخاب کنید، لینک‌ها را به ترتیب دنبال کنید و به سرعت بهره‌ور خواهید شد. همیشه می‌توانید به این صفحه برگردید تا قدم بعدی خود را پیدا کنید.

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/learning-path.md)
