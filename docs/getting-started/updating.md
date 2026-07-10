---
layout: docs
title: "به‌روزرسانی و حذف"
permalink: /docs/getting-started/updating/
---

- 
- Getting Started
- Updating & Uninstalling

# به‌روزرسانی و حذف

## به‌روزرسانی

با یک دستور به آخرین نسخه به‌روزرسانی کنید:

```
hermes update
```

این دستور آخرین کد را از main دریافت می‌کند، وابستگی‌ها را به‌روز می‌کند و از شما می‌خواهد گزینه‌های پیکربندی جدیدی که از آخرین به‌روزرسانی شما اضافه شده‌اند را پیکربندی کنید.

`hermes update` به طور خودکار گزینه‌های پیکربندی جدید را تشخیص می‌دهد و از شما می‌خواهد آن‌ها را اضافه کنید. اگر آن پرامپت را رد کردید، می‌توانید به صورت دستی `hermes config check` را اجرا کنید تا گزینه‌های موجود را ببینید، سپس `hermes config migrate` را اجرا کنید تا به صورت تعاملی آن‌ها را اضافه کنید.

### چه اتفاقی در طول به‌روزرسانی می‌افتد

وقتی `hermes update` را اجرا می‌کنید، مراحل زیر رخ می‌دهند:

1. اسکنپوت اطلاعات جفت‌شده — یک اسکنپوت سبک قبل از به‌روزرسانی ذخیره می‌شود (شامل `~/.hermes/pairing/`، قوانین نظرات Feishu و سایر فایل‌های وضعیتی که در حین اجرا تغییر می‌کنند). از طریق جریان بازیابی اسکنپوت که در بخش اسکنپوتها و بازگشت توضیح داده شده، یا با استخراج آخرین zip اسکنپوت سریع که Hermes در کنار دایرکتوری `~/.hermes/` شما نوشته است، قابل بازیابی است.
2. Git pull — آخرین کد را از شاخه main دریافت می‌کند و زیرمجموعه‌ها را به‌روز می‌کند
3. اعتبارسنجی نحو بعد از pull و بازگشت خودکار — بعد از pull، Hermes هشت فایل حیاتی را که هر فراخوانی `hermes` در شروع بارگذاری می‌کند کامپایل می‌کند. اگر هر کدام نتواند تجزیه شود (مثلاً یک نشانگر ادغام تعارضی یتیم، یا فایل تصادفاً بریده‌شده)، Hermes `git reset --hard <pre-pull-sha>` را اجرا می‌کند تا نصب را به حالت قبل برگرداند و shell شما قابل بوت باقی بماند. بعد از رفع مشکل از سمت upstream دوباره `hermes update` را اجرا کنید.
4. نصب وابستگی‌ها — `uv pip install -e ".[all]` را اجرا می‌کند تا وابستگی‌های جدید یا تغییر یافته را دریافت کند
5. مهاجرت پیکربندی — گزینه‌های پیکربندی جدیدی که از نسخه شما اضافه شده‌اند را تشخیص می‌دهد و از شما می‌خواهد آن‌ها را تنظیم کنید
6. بازراه‌اندازی خودکار gateway — gatewayهای در حال اجرا بعد از تکمیل به‌روزرسانی تازه‌سازی می‌شوند تا کد جدید فوراً اعمال شود. gatewayهای مدیریت‌شده توسط سرویس (systemd در Linux، launchd در macOS) از طریق مدیر سرویس بازراه‌اندازی می‌شوند. gatewayهای دستی زمانی که Hermes بتواند PID در حال اجرا را به یک پروفایل نگاشت کند، به طور خودکار دوباره راه‌اندازی می‌شوند.

### به‌روزرسانی با شاخه‌ای غیر از پیش‌فرض: --branch

به طور پیش‌فرض `hermes update` از `origin/main` پیروی می‌کند. `--branch <name>` را برای به‌روزرسانی با یک شاخه متفاوت پاس دهید — مفید برای کانال‌های QA، شاخه‌های ویژگی یا تست نامزد انتشار:

```
hermes update --branch release-candidate
hermes update --check --branch experimental   # فقط پیش‌نمایش عقب‌ماندگی
```

### تغییرات محلی در به‌روزرسانی‌های غیر تعاملی

وقتی `hermes update` را در یک ترمینال اجرا می‌کنید، Hermes هرگونه تغییرات کدsource تأیید نشده را stash می‌کند، pull می‌کند، سپس می‌پرسد آیا می‌خواهید آن‌ها را بازیابی کنید — دقیقاً مانند همیشه. برای به‌روزرسانی‌های تعاملی هیچ چیزی تغییر نمی‌کند.

وقتی به‌روزرسانی بدون تerminal اجرا می‌شود — از دکمه «به‌روزرسانی» دسکتاپ/چت اپلیکیشن یا به‌روزرسانی فعال‌شده توسط gateway — هیچ پرامپتی برای پاسخ دادن وجود ندارد. تنظیم `updates.non_interactive_local_changes` تصمیم می‌گیرد با تغییرات stash شده شما چه اتفاقی بیفتد:

```yaml
# ~/.hermes/config.yaml
updates:
  non_interactive_local_changes: stash   # پیش‌فرض: نگه‌داشتن + بازیابی خودکار
  # non_interactive_local_changes: discard  # دور انداختن ویرایش‌های محلی کدsource
```

- `stash` (پیش‌فرض) — stash خودکار، pull، سپس بازیابی خودکار تغییرات شما روی کد به‌روزرسانی‌شده. هیچ چیزی از دست نمی‌رود؛ اگر بازیابی با تعارض مواجه شود، آن‌ها در git stash برای بازیابی دستی حفظ می‌شوند.
- `discard` — stash خودکار و حذف stash بعد از pull، بنابراین به‌روزرسانی همیشه روی یک درخت تمیز فرود می‌آید. فقط در ماشین‌هایی استفاده کنید که هرگز قصد حفظ ویرایش‌های محلی Hermes source را ندارید.

در اپلیکیشن دسکتاپ، این در Settings → Advanced → In-App Update Local Changes است.

### فقط پیش‌نمایش: hermes update --check

آیا می‌خواهید قبل از pull بدانید آیا به‌روزرسانی‌ای موجود است؟ `hermes update --check` را اجرا کنید — آخرین commitها را دریافت و با `origin/main` مقایسه می‌کند. هیچ فایلی تغییر نمی‌کند و gateway بازراه‌اندازی نمی‌شود.

### نسخه پشتیبان کامل قبل از به‌روزرسانی: --backup

برای پروفایل‌های با ارزش بالا (gatewayهای تولیدی، نصب‌های اشتراکی تیم) می‌توانید از نسخه پشتیبان کامل قبل از pull از `HERMES_HOME` (پیکربندی، احراز هویت، sessionها، skillها، جفت‌شده) استفاده کنید:

```
hermes update --backup
```

یا آن را به عنوان پیش‌فرض برای هر اجرا تنظیم کنید:

```yaml
# ~/.hermes/config.yaml
updates:
  pre_update_backup: true
```

`--backup` رفتار همیشه‌فعال در نسخه‌های قبلی بود، اما باعث اضافه شدن دقایقی به هر به‌روزرسانی در خانه‌های بزرگ می‌شد، بنابراین اکنون اختیاری است. اسکنپوت سبک اطلاعات جفت‌شده بالا همچنان بدون قید و شرط اجرا می‌شود.

### ویندوز: یک hermes.exe دیگر در حال اجراست

در ویندوز، `hermes update` از اجرا خودداری می‌کند اگر تشخیص دهد یک پروسه `hermes.exe` دیگر فایل اجرایی entry-point venv را باز نگه داشته است — بیشترین احتمال بک‌اند اسپاون‌شده توسط اپلیکیشن Hermes Desktop، یک REPL `hermes` باز در ترمینال دیگر، یا یک gateway در حال اجرا:

```console
$ hermes update
✗ Another hermes.exe is running:
    PID 12345  hermes.exe
  Updating now would fail to overwrite ...\venv\Scripts\hermes.exe because
  Windows blocks REPLACE on a running executable.
  Close Hermes Desktop, exit any open `hermes` REPLs, and
  stop the gateway (`hermes gateway stop`) before retrying.
  Override with `hermes update --force` if you've already
  confirmed those processes will not write to the venv.
```

پروسه‌های لیست‌شده را ببندید و دوباره اجرا کنید. اگر مطمئن هستید پروسه همزمان تداخل نمی‌کند، `--force` را برای رد کردن بررسی پاس دهید.

### اعتبارسنجی توصیه‌شده بعد از به‌روزرسانی

`hermes update` مسیر به‌روزرسانی اصلی را مدیریت می‌کند، اما یک اعتبارسنجی سریع تأیید می‌کند همه چیز به خوبی فرود آمده:

1. `git status --short` — اگر درخت به طور غیرمنتظره کثیف است، قبل از ادامه بررسی کنید
2. `hermes doctor` — پیکربندی، وابستگی‌ها و سلامت سرویس را بررسی می‌کند
3. `hermes --version` — تأیید کنید نسخه مطابق انتظار افزایش یافته
4. اگر از gateway استفاده می‌کنید: `hermes gateway status`
5. اگر doctor مشکلات npm audit را گزارش می‌کند: `npm audit fix` را در دایرکتوری مشخص‌شده اجرا کنید

### اگر تerminal شما در حین به‌روزرسانی قطع شود

`hermes update` در برابر از دست دادن تصادفی تerminal از خود محافظت می‌کند:

- به‌روزرسانی از SIGHUP چشم‌پوشی می‌کند، بنابراین بستن نشست SSH یا پنجره terminal دیگر آن را در حین نصب نمی‌کشد. فرآیندهای فرزند pip و git این محافظت را به ارث می‌برند، بنابراین محیط Python نمی‌تواند نیمه‌نصب باقی بماند.
- همه خروجی در حین اجرا در `~/.hermes/logs/update.log` آینه می‌شود. اگر terminal شما ناپدید شد، دوباره وصل شوید و لاگ را بررسی کنید تا ببینید آیا به‌روزرسانی تمام شده و آیا بازراه‌اندازی gateway موفق بوده:

```bash
tail -f ~/.hermes/logs/update.log
```

دیگر نیازی به بستن `hermes update` در screen یا tmux برای زنده ماندن قطع terminal نیست.

### بررسی نسخه فعلی

```bash
hermes version
```

با آخرین نسخه در [GitHub releases page](https://github.com/NousResearch/hermes-agent/releases) مقایسه کنید.

### به‌روزرسانی از پلتفرم‌های پیام‌رسانی

همچنین می‌توانید مستقیماً از Telegram، Discord، Slack، WhatsApp یا Teams با ارسال زیر به‌روزرسانی کنید:

```
/update
```

این دستور آخرین کد را دریافت می‌کند، وابستگی‌ها را به‌روز می‌کند و gatewayهای در حال اجرا را بازراه‌اندازی می‌کند. ربات در حین بازراه‌اندازی به طور خلاصه آفلاین می‌شود (معمولاً ۵ تا ۱۵ ثانیه) و سپس از سر گرفته می‌شود.

### به‌روزرسانی دستی

اگر به صورت دستی نصب کرده‌اید (نه از طریق نصب‌کننده سریع):

```bash
cd /path/to/hermes-agent
# فعال‌سازی venv که در حین نصب ایجاد کردید (خارج از درخت کدsource)
export VIRTUAL_ENV="$HOME/.hermes/venvs/hermes-dev"
export PATH="$VIRTUAL_ENV/bin:$PATH"
# دریافت آخرین کد
git pull origin main
# نصب مجدد (دریافت وابستگی‌های جدید)
uv pip install -e ".[all]"
# بررسی گزینه‌های پیکربندی جدید
hermes config check
hermes config migrate   # اضافه کردن تعاملی گزینه‌های موجود
```

### دستورالعمل‌های بازگشت

اگر یک به‌روزرسانی مشکلی ایجاد کرد، می‌توانید به نسخه قبلی بازگردید:

```bash
cd /path/to/hermes-agent
# لیست نسخ‌های اخیر
git log --oneline -10
# بازگشت به یک commit مشخص
git checkout <commit-hash>
uv pip install -e ".[all]"
# بازراه‌اندازی gateway اگر در حال اجراست
hermes gateway restart
```

بازگشت ممکن است اگر گزینه‌های جدیدی اضافه شده باشند، ناسازگاری پیکربندی ایجاد کند. بعد از بازگشت `hermes config check` را اجرا کنید و هر گزینه غیرقابل تشخیصی را از `config.yaml` حذف کنید.

### یادداشت برای کاربران Nix

Nix دیگر یک مسیر نصب پشتیبانی‌شده به طور رسمی نیست (فقط بهترین تلاش) — [Nix Setup](/docs/getting-started/nix-setup) را ببینید. اگر از طریق Nix flake نصب کرده‌اید، به‌روزرسانی‌ها از طریق مدیر بسته Nix مدیریت می‌شوند:

```bash
# به‌روزرسانی ورودی flake
nix flake update hermes-agent
# یا بازسازی با آخرین نسخه
nix profile upgrade hermes-agent
```

نصب‌های Nix تغییرناپذیر هستند — بازگشت توسط سیستم نسل Nix مدیریت می‌شود:

```bash
nix profile rollback
```

جزئیات بیشتر در [Nix Setup](/docs/getting-started/nix-setup).

## حذف

```bash
hermes uninstall
```

حذف‌کننده به شما گزینه نگه‌داشتن فایل‌های پیکربندی (`~/.hermes/`) برای نصب مجدد آینده را می‌دهد.

### حذف دستی

```bash
rm -f ~/.local/bin/hermes
rm -rf /path/to/hermes-agent
rm -rf ~/.hermes            # اختیاری — اگر قصد نصب مجدد دارید نگه‌دارید
```

اگر gateway را به عنوان سرویس سیستمی نصب کرده‌اید، ابتدا آن را متوقف و غیرفعال کنید:

```bash
hermes gateway stop
# Linux: systemctl --user disable hermes-gateway
# macOS: launchctl remove ai.hermes.gateway
```

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/updating.md)
