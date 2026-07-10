---
layout: docs
title: "نقاط بازیابی"
permalink: /docs/user-guide/checkpoints-and-rollback/
---

- 
- استفاده از Hermes
- Checkpoints و Rollback

# Checkpoints و `/rollback`

`/rollback`

Hermes Agent می‌تواند به طور خودکار قبل از **عملیات مخرب** از پروژه شما اسکنپشت بگیرد و آن را با یک دستور واحد بازیابی کند. checkpoints از v2 به صورت **اختیاری** هستند — بیشتر کاربران هرگز از `/rollback` استفاده نمی‌کنند و ذخیره‌سازی shadow-store در طول زمان غیرعادی است، بنابراین پیش‌فرض خاموش است.

`/rollback`

checkpoints را در هر جلسه با `--checkpoints` فعال کنید:

`--checkpoints`

```
hermes chat --checkpoints
```

یا به طور کلی در `~/.hermes/config.yaml` فعال کنید:

`~/.hermes/config.yaml`

```
checkpoints:
  enabled: true
```

این شبکه ایمنی توسط یک **Checkpoint Manager** داخلی پشتیبانی می‌شود که یک مخزن git سایه‌ای مشترک را در `~/.hermes/checkpoints/store/` نگه می‌دارد — `.git` واقعی پروژه شما هرگز لمس نمی‌شود. هر پروژه‌ای که عامل در آن کار می‌کند همان فروشگاه را به اشتراک می‌گذارد، بنابراین DB اشیاء content-addressable git در پروژه‌ها و نوبت‌ها dedup می‌کند.

`~/.hermes/checkpoints/store/`
`.git`

## چه چیزی یک Checkpoint را فعال می‌کند

checkpoints قبل از موارد زیر به طور خودکار گرفته می‌شوند:

- **ابزارهای فایل** — `write_file` و `patch`
- **دستورات مخرب terminal** — `rm`، `rmdir`، `cp`، `install`، `mv`، `sed -i`، `truncate`، `dd`، `shred`، ریدایرکت‌های خروجی (`>`)، و `git reset`/`clean`/`checkout`

`write_file`
`patch`
`rm`
`rmdir`
`cp`
`install`
`mv`
`sed -i`
`truncate`
`dd`
`shred`
`>`
`git reset`
`clean`
`checkout`

عامل **حداکثر یک checkpoint به ازای هر دایرکتوری در هر نوبت** ایجاد می‌کند، بنابراین نشست‌های طولانی‌مدت اسکنپشت‌ها را اسپم نمی‌کنند.

## مرجع سریع

دستورات اسلش درون نشست:

| دستور | توضیح |
| --- | --- |
| `/rollback` | فهرست کردن همه checkpoints با آمار تغییرات |
| `/rollback <N>` | بازیابی به checkpoint N (همچنین آخرین نوبت چت را undo می‌کند) |
| `/rollback diff <N>` | پیش‌نمایش diff بین checkpoint N و وضعیت فعلی |
| `/rollback <N> <file>` | بازیابی یک فایل منفرد از checkpoint N |

`/rollback`
`/rollback <N>`
`/rollback diff <N>`
`/rollback <N> <file>`

CLI برای بررسی و مدیریت فروشگاه خارج از نشست:

| دستور | توضیح |
| --- | --- |
| `hermes checkpoints` | نمایش اندازه کل، تعداد پروژه، جزئیات به ازای هر پروژه |
| `hermes checkpoints status` | مشابه `checkpoints` ساده |
| `hermes checkpoints list` | نام مستعار برای `status` |
| `hermes checkpoints prune` | اجرای اجباری sweep: حذف orphan‌ها/قدیمی‌ها، GC، اجرای محدودیت اندازه |
| `hermes checkpoints clear` | حذف کل پایگاه checkpoint (اول تأیید می‌گیرد) |
| `hermes checkpoints clear-legacy` | حذف فقط آرشیوهای `legacy-*` از مهاجرت v1 |

`hermes checkpoints`
`hermes checkpoints status`
`checkpoints`
`hermes checkpoints list`
`status`
`hermes checkpoints prune`
`hermes checkpoints clear`
`hermes checkpoints clear-legacy`
`legacy-*`

## نحوه کار Checkpoints

در سطح بالا:

- Hermes تشخیص می‌دهد وقتی ابزارها در حال **ویرایش فایل‌ها** در درخت کاری شما هستند.
- یک بار در هر نوبت مکالمه (به ازای هر دایرکتوری):
  - یک ریشه پروژه معقول برای فایل حل می‌کند.
  - **فروشگاه سایه‌ای مشترک** در `~/.hermes/checkpoints/store/` را مقداردهی اولیه یا استفاده مجدد می‌کند.
  - در یک ایندکس به ازای پروژه staging می‌کند، یک درخت می‌سازد، و به یک ref به ازای پروژه (`refs/hermes/<project-hash>`) commit می‌کند.

- این ref‌های به ازای پروژه یک تاریخچه checkpoint تشکیل می‌دهند که می‌توانید از طریق `/rollback` آن را بررسی و بازیابی کنید.

- یک ریشه پروژه معقول برای فایل حل می‌کند.
- فروشگاه سایه‌ای مشترک در `~/.hermes/checkpoints/store/` را مقداردهی اولیه یا استفاده مجدد می‌کند.
- در یک ایندکس به ازای پروژه staging می‌کند، یک درخت می‌سازد، و به یک ref به ازای پروژه commit می‌کند.

`~/.hermes/checkpoints/store/`
`refs/hermes/<project-hash>`
`/rollback`

## پیکربندی

در `~/.hermes/config.yaml` پیکربندی کنید:

`~/.hermes/config.yaml`

```
checkpoints:
  enabled: false              # master switch (default: false — opt-in)
  max_snapshots: 20           # max checkpoints per project (enforced via ref rewrite + gc)
  max_total_size_mb: 500      # hard cap on total store size; oldest commits dropped
  max_file_size_mb: 10        # skip any single file larger than this
  # Auto-maintenance (on by default): sweep ~/.hermes/checkpoints/ at startup
  # and delete project entries whose working directory no longer exists
  # (orphans) or whose last_touch is older than retention_days. Runs at most
  # once per min_interval_hours, tracked via a .last_prune marker.
  auto_prune: true
  retention_days: 7
  delete_orphans: true
  min_interval_hours: 24
```

برای غیرفعال کردن همه چیز:

```
checkpoints:
  enabled: false
  auto_prune: false
```

وقتی `enabled: false` باشد، Checkpoint Manager بی‌عمل است و هرگز عملیات git را انجام نمی‌دهد. وقتی `auto_prune: false` باشد، فروشگاه رشد می‌کند تا زمانی که `hermes checkpoints prune` را دستی اجرا کنید.

`enabled: false`
`auto_prune: false`
`hermes checkpoints prune`

## فهرست‌بندی Checkpoints

از یک نشست CLI:

```
/rollback
```

Hermes با یک فهرست قالب‌بندی‌شده نشان داده شده با آمار تغییرات پاسخ می‌دهد:

```
📸 Checkpoints for /path/to/project:
  1. 4270a8c  2026-03-16 04:36  before patch  (1 file, +1/-0)
  2. eaf4c1f  2026-03-16 04:35  before write_file
  3. b3f9d2e  2026-03-16 04:34  before terminal: sed -i s/old/new/ config.py  (1 file, +1/-1)
  /rollback <N>             restore to checkpoint N
  /rollback diff <N>        preview changes since checkpoint N
  /rollback <N> <file>      restore a single file from checkpoint N
```

## بررسی فروشگاه از Shell

```
hermes checkpoints
```

خروجی نمونه:

```
Checkpoint base: /home/you/.hermes/checkpoints
Total size:      142.3 MB
  store/         138.1 MB
  legacy-*       4.2 MB
Projects:        12
  WORKDIR                                                       COMMITS    LAST TOUCH  STATE
  /home/you/code/hermes-agent                                        20       2h ago  live
  /home/you/code/experiments/rl-runner                                8       1d ago  live
  /home/you/code/old-prototype                                        3       9d ago  orphan
  ...
Legacy archives (1):
  legacy-20260506-050616                           4.2 MB
Clear with: hermes checkpoints clear-legacy
```

اجرای اجباری sweep کامل (نادیده گرفتن نشانگر idempotency 24 ساعته):

```
hermes checkpoints prune --retention-days 3 --max-size-mb 200
```

## پیش‌نمایش تغییرات با `/rollback diff`

`/rollback diff`

قبل از تعهد به بازیابی، تغییراتی که از یک checkpoint ایجاد شده را پیش‌نمایش کنید:

```
/rollback diff 1
```

این یک خلاصه git diff stat و سپس diff واقعی را نشان می‌دهد.

## بازیابی با `/rollback`

`/rollback`

```
/rollback 1
```

در پشت صحنه، Hermes:

1. تأیید می‌کند که commit هدف در فروشگاه سایه‌ای وجود دارد.
2. یک **اسکنپشت قبل از بازیابی** از وضعیت فعلی می‌گیرد تا بعداً بتوانید «undo را undo کنید».
3. فایل‌های ردیابی‌شده در دایرکتوری کاری شما را بازیابی می‌کند.
4. **آخرین نوبت مکالمه را undo می‌کند** تا زمینه عامل با وضعیت فایل‌سیستم بازیابی‌شده مطابقت داشته باشد.

## بازیابی تک‌فایلی

فقط یک فایل از یک checkpoint بازیابی کنید بدون تأثیر روی بقیه دایرکتوری:

```
/rollback 1 src/broken_file.py
```

## محافظت‌های ایمنی و عملکردی

- **دسترسی git** — اگر `git` در `PATH` یافت نشود، checkpoints به طور شفاف غیرفعال می‌شوند.
- **دامنه دایرکتوری** — Hermes دایرکتوری‌های بیش از حد وسیع (`root/`، `home$HOME`) را رد می‌کند.
- **اندازه مخزن** — دایرکتوری‌های با بیش از 50,000 فایل رد می‌شوند.
- **محدودیت اندازه فایل** — فایل‌های بزرگتر از `max_file_size_mb` (پیش‌فرض 10 MB) از اسکنپشت حذف می‌شوند. از بلعیدن تصادفی مجموعه‌داده‌ها، وزن‌های مدل یا رسانه تولیدشده جلوگیری می‌کند.
- **محدودیت اندازه کل فروشگاه** — وقتی فروشگاه از `max_total_size_mb` (پیش‌فرض 500 MB) تجاوز کند، قدیمی‌ترین commit به ازای هر پروژه به صورت round-robin حذف می‌شود تا زیر محدودیت باشد.
- **Pruning واقعی** — `max_snapshots` با بازنویسی ref به ازای پروژه و اجرای `git gc --prune=now` بعد از آن اجرا می‌شود، بنابراین اشیای loose جمع نمی‌شوند.
- **اسکنپشت‌های بدون تغییر** — اگر از آخرین اسکنپشت تغییری وجود نداشته باشد، checkpoint رد می‌شود.
- **خطاهای غیرکشنده** — همه خطاها داخل Checkpoint Manager در سطح debug ثبت می‌شوند؛ ابزارهای شما به اجرای خود ادامه می‌دهند.

`git`
`PATH`
`/`
`$HOME`
`max_file_size_mb`
`max_total_size_mb`
`max_snapshots`
`git gc --prune=now`

## محل قرارگیری Checkpoints

```
~/.hermes/checkpoints/
  ├── store/                 # single shared bare git repo
  │   ├── HEAD, objects/     # git internals (shared across projects)
  │   ├── refs/hermes/<hash> # per-project branch tip
  │   ├── indexes/<hash>     # per-project git index
  │   ├── projects/<hash>.json  # workdir + created_at + last_touch
  │   └── info/exclude
  ├── .last_prune            # auto-prune idempotency marker
  └── legacy-<ts>/           # archived pre-v2 per-project shadow repos
```

هر `<hash>` از مسیر مطلق دایرکتوری کاری مشتق شده است. معمولاً هرگز نیازی به لمس دستی آن‌ها نیست — به جای آن از `hermes checkpoints status`/`prune`/`clear` استفاده کنید.

`<hash>`
`hermes checkpoints status`
`prune`
`clear`

### مهاجرت از v1

قبل از بازنویسی v2، هر دایرکتوری کاری یک مخزن git سایه‌ای کامل جداگانه مستقیماً زیر `~/.hermes/checkpoints/<hash>/` داشت. آن چیدمان نمی‌توانست object‌ها را بین پروژه‌ها dedup کند و یک pruner بی‌عمل مستند داشت — فروشگاه بدون محدودیت رشد می‌کرد.

`~/.hermes/checkpoints/<hash>/`

در اولین اجرای v2، هر مخزن سایه‌ای قبل از v2 به `~/.hermes/checkpoints/legacy-<timestamp>/` منتقل می‌شود تا چیدمان فروشگاه واحد جدید تمیز شروع شود. تاریخچه `/rollback` قدیمی همچنان با بررسی دستی آرشیو legacy از طریق `git` قابل دسترسی است؛ وقتی مطمئن شدید به آن نیاز ندارید، اجرا کنید:

`~/.hermes/checkpoints/legacy-<timestamp>/`
`/rollback`
`git`

```
hermes checkpoints clear-legacy
```

برای بازپس‌گیری فضا. آرشیوهای legacy همچنین توسط `auto_prune` پس از `retention_days` sweep می‌شوند.

`auto_prune`
`retention_days`

## بهترین شیوه‌ها

- **checkpoints را فقط وقتی فعال کنید که به آن‌ها نیاز دارید** — `hermes chat --checkpoints` یا `enabled: true` به ازای هر پروفایل.
- **قبل از بازیابی از `/rollback diff` استفاده کنید** — پیش‌نمایش کنید چه چیزی تغییر خواهد کرد تا checkpoint مناسب را انتخاب کنید.
- **از `/rollback` به جای `git reset` استفاده کنید** وقتی فقط می‌خواهید تغییرات عامل‌محور را undo کنید.
- **گاهی `hermes checkpoints status` را بررسی کنید** اگر منظماً از checkpoints استفاده می‌کنید — نشان می‌دهد کدام پروژه‌ها فعال هستند و فروشگاه چه هزینه‌ای برای شما دارد.
- **با Git worktrees ترکیب کنید** برای حداکثر ایمنی — هر جلسه Hermes را در worktree/branch خود نگه دارید، با checkpoints به عنوان یک لایه اضافی.

`hermes chat --checkpoints`
`enabled: true`
`/rollback diff`
`/rollback`
`git reset`
`hermes checkpoints status`

برای اجرای عوامل متعدد به صورت موازی روی همان مخزن، به راهنمای [Git worktrees](/docs/user-guide/git-worktrees) مراجعه کنید.

[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/checkpoints-and-rollback.md)