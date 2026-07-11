---
layout: docs
title: "Git Worktrees"
permalink: /docs/user-guide/git-worktrees/
---

- 
- استفاده از Hermes
- Git Worktrees

# Git Worktrees

Hermes Agent اغلب روی مخزن‌های بزرگ و طولانی‌مدت استفاده می‌شود. وقتی می‌خواهید:

- **عوامل متعدد را به صورت موازی** روی یک پروژه اجرا کنید، یا
- **بازآرایی‌های آزمایشی** را از شاخه اصلی خود جدا نگه دارید،

Git worktrees **امن‌ترین راه** برای دادن یک checkout جداگانه به هر عامل بدون تکرار کل مخزن هستند.

این صفحه نشان می‌دهد چگونه worktrees را با Hermes ترکیب کنید تا هر جلسه دایرکتوری کاری تمیز و ایزوله داشته باشد.

## چرا از Worktrees با Hermes استفاده کنیم؟

Hermes **دایرکتوری کاری فعلی** را به عنوان ریشه پروژه در نظر می‌گیرد:

- **CLI**: دایرکتوری که `hermes` یا `hermes chat` را در آن اجرا می‌کنید
- **Gateway‌های پیام‌رسانی**: دایرکتوری تنظیم‌شده توسط `terminal.cwd` در `~/.hermes/config.yaml`

`hermes`
`hermes chat`
`terminal.cwd`
`~/.hermes/config.yaml`

اگر چندین عامل را در **همان checkout** اجرا کنید، تغییرات آن‌ها می‌تواند با هم تداخل داشته باشد:

- یک عامل ممکن است فایل‌هایی را که عامل دیگر استفاده می‌کند حذف یا بازنویسی کند.
- درک اینکه کدام تغییرات مربوط به کدام آزمایش است دشوارتر می‌شود.

با worktrees، هر عامل دریافت می‌کند:

- **شاخه و دایرکتوری کاری خود**
- **تاریخچه Checkpoint Manager خود** برای `/rollback`

`/rollback`

همچنین ببینید: [نقاط بازیابی و /rollback](/docs/user-guide/checkpoints-and-rollback/).

## شروع سریع: ایجاد یک Worktree

از مخزن اصلی خود (حاوی `.git/`)، یک worktree جدید برای شاخه feature ایجاد کنید:

`.git/`

```
# From the main repo root
cd /path/to/your/repo

# Create a new branch and worktree in ../repo-feature
git worktree add ../repo-feature feature/hermes-experiment
```

این موارد زیر را ایجاد می‌کند:

- یک دایرکتوری جدید: `../repo-feature`
- یک شاخه جدید: `feature/hermes-experiment` که در آن دایرکتوری checkout شده

`../repo-feature`
`feature/hermes-experiment`

حالا می‌توانید `cd` به worktree جدید کنید و Hermes را در آن اجرا کنید:

`cd`

```
cd ../repo-feature
# Start Hermes in the worktree
hermes
```

Hermes:

- `../repo-feature` را به عنوان ریشه پروژه می‌بیند.
- از آن دایرکتوری برای فایل‌های زمینه، ویرایش‌های کد و ابزارها استفاده می‌کند.
- از یک **تاریخچه checkpoint جداگانه** برای `/rollback` محدود به این worktree استفاده می‌کند.

`../repo-feature`
`/rollback`

## اجرای عوامل متعدد به صورت موازی

می‌توانید چندین worktree ایجاد کنید، هر کدام با شاخه خود:

```
cd /path/to/your/repo
git worktree add ../repo-experiment-a feature/hermes-a
git worktree add ../repo-experiment-b feature/hermes-b
```

در ترمینال‌های جداگانه:

```
# Terminal 1
cd ../repo-experiment-a
hermes

# Terminal 2
cd ../repo-experiment-b
hermes
```

هر فرایند Hermes:

- روی شاخه خود کار می‌کند (`feature/hermes-a` در مقابل `feature/hermes-b`).
- checkpoints را تحت یک هش مخزن سایه‌ای متفاوت (مشتق از مسیر worktree) می‌نویسد.
- می‌تواند به طور مستقل از `/rollback` استفاده کند بدون تأثیر روی دیگری.

`feature/hermes-a`
`feature/hermes-b`
`/rollback`

این به ویژه مفید است وقتی:

- بازآرایی‌های دسته‌ای اجرا می‌کنید.
- رویکردهای مختلفی برای همان کار امتحان می‌کنید.
- نشست‌های CLI + gateway را علیه همان مخزن upstream جفت می‌کنید.

## پاک‌سازی ایمن Worktrees

وقتی آزمایشی تمام شد:

1. تصمیم بگیرید کار را نگه دارید یا دور بریزید.
2. اگر می‌خواهید نگه دارید: شاخه را مانند همیشه به شاخه اصلی خود ادغام کنید.
3. worktree را حذف کنید:

- شاخه را مانند همیشه به شاخه اصلی خود ادغام کنید.

```
cd /path/to/your/repo
# Remove the worktree directory and its reference
git worktree remove ../repo-feature
```

نکات:

- `git worktree remove` از حذف worktree با تغییرات commit نشده امتناع می‌کند مگر اینکه آن را مجبور کنید.
- حذف worktree **به طور خودکار شاخه را حذف نمی‌کند**؛ می‌توانید شاخه را با دستورات عادی `git branch` حذف یا نگه دارید.
- داده‌های checkpoint Hermes در `~/.hermes/checkpoints/` هنگام حذف worktree به طور خودکار پاک نمی‌شوند، اما معمولاً بسیار کوچک هستند.

`git worktree remove`
`git branch`
`~/.hermes/checkpoints/`

## بهترین شیوه‌ها

- **یک worktree برای هر آزمایش Hermes** — برای هر تغییر قابل توجه یک شاخه/worktree اختصاصی ایجاد کنید. این diff‌ها را متمرکز و PR‌ها را کوچک و قابل بررسی نگه می‌دارد.
- **شاخه‌ها را بر اساس آزمایش نام‌گذاری کنید** — مثلاً `feature/hermes-checkpoints-docs`، `feature/hermes-refactor-tests`.
- **مکرراً commit کنید** — از git commits برای نقاط عطف سطح بالا استفاده کنید. از checkpoints و `/rollback` به عنوان شبکه ایمنی برای ویرایش‌های ابزارمحور در بین آن‌ها استفاده کنید.
- **از اجرای Hermes از ریشه مخزن خام هنگام استفاده از worktrees اجتناب کنید** — به جای آن دایرکتوری‌های worktree را ترجیح دهید تا هر عامل دامنه مشخصی داشته باشد.

- برای هر تغییر قابل توجه یک شاخه/worktree اختصاصی ایجاد کنید.
- این diff‌ها را متمرکز و PR‌ها را کوچک و قابل بررسی نگه می‌دارد.

- مثلاً `feature/hermes-checkpoints-docs`، `feature/hermes-refactor-tests`.

`feature/hermes-checkpoints-docs`
`feature/hermes-refactor-tests`
- از git commits برای نقاط عطف سطح بالا استفاده کنید.
- از checkpoints و `/rollback` به عنوان شبکه ایمنی برای ویرایش‌های ابزارمحور در بین آن‌ها استفاده کنید.

[checkpoints و /rollback](/docs/user-guide/checkpoints-and-rollback/)
- دایرکتوری‌های worktree را ترجیح دهید تا هر عامل دامنه مشخصی داشته باشد.

## استفاده از `hermes -w` (حالت Worktree خودکار)

`hermes -w`

Hermes یک پرچم داخلی `-w` دارد که **به طور خودکار یک git worktree یکبار مصرف** با شاخه خود ایجاد می‌کند. نیازی به راه‌اندازی دستی worktrees نیست — فقط `cd` به مخزن خود کنید و اجرا کنید:

`-w`
`cd`

```
cd /path/to/your/repo
hermes -w
```

Hermes:

- یک worktree موقت در `.worktrees/` داخل مخزن شما ایجاد می‌کند.
- یک شاخه ایزوله (مثلاً `hermes/hermes-<hash>`) را checkout می‌کند.
- کل نشست CLI را در آن worktree اجرا می‌کند.

`.worktrees/`
`hermes/hermes-<hash>`

این آسان‌ترین راه برای دریافت ایزوله worktree است. همچنین می‌توانید آن را با یک پرسش واحد ترکیب کنید:

```
hermes -w -z "Fix issue #123"
```

برای عوامل موازی، چندین ترمینال باز کنید و `hermes -w` را در هر کدام اجرا کنید — هر فراخوانی به طور خودکار worktree و شاخه خود را دریافت می‌کند.

`hermes -w`

## ترکیب همه چیز

- از `git worktrees` استفاده کنید تا به هر جلسه Hermes checkout تمیز جداگانه بدهید.
- از `branch`‌ها استفاده کنید تا تاریخچه سطح بالای آزمایش‌های خود را ثبت کنید.
- از checkpoints + `/rollback` استفاده کنید تا از اشتباهات داخل هر worktree بازیابی کنید.

`/rollback`

این ترکیب به شما می‌دهد:

- تضمین‌های قوی که عوامل و آزمایش‌های مختلف روی هم قدم نگذارند.
- چرخه‌های تکرار سریع با بازیابی آسان از ویرایش‌های بد.
- Pull request‌های تمیز و قابل بررسی.

[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/git-worktrees.md)