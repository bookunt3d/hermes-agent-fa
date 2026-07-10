---
layout: docs
title: "نصب"
permalink: /docs/getting-started/installation/
---

- 
- Getting Started
- Installation

# نصب

Hermes Agent را در کمتر از دو دقیقه نصب و راه‌اندازی کنید!

برای جدول کامل پشتیبانی پلتفرم (کدام سیستم‌عامل‌ها، روش‌های توزیع و ویژگی‌های محدود به پلتفرم پشتیبانی می‌شوند)، [پشتیبانی از پلتفرم‌ها](/docs/getting-started/platform-support) را ببینید.

## نصب سریع

### با نصب‌کننده Hermes Desktop در macOS یا Windows (توصیه‌شده)

برای نصب آسان اپلیکیشن‌های خط فرمان و دسکتاپ، [نصب‌کننده Hermes Desktop](https://hermes-agent.nousresearch.com/) را از وب‌سایت ما دانلود و اجرا کنید.

### بدون Hermes Desktop:

برای نصب فقط خط فرمان بدون Hermes Desktop، دستور زیر را اجرا کنید:

#### Linux / macOS / WSL2 / Android (Termux)

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

#### Windows (بومی)

در powershell اجرا کنید:

```
iex (irm https://hermes-agent.nousresearch.com/install.ps1) 
```

اگر می‌خواهید بعد از نصب فقط خط فرمان، Hermes Desktop را نصب و اجرا کنید، کافی است اجرا کنید:

```
hermes desktop
```

### نصب‌کننده چه کاری انجام می‌دهد

نصب‌کننده همه چیز را به طور خودکار مدیریت می‌کند — تمام وابستگی‌ها (Python، Node.js، ripgrep، ffmpeg)، clone مخزن، محیط مجازی، تنظیم فرمان عمومی `hermes` و پیکربندی ارائه‌دهنده LLM. در پایان، آماده چت هستید.

#### چیدمان نصب

اینکه نصب‌کننده چیزها را کجا قرار می‌دهد بستگی دارد به اینکه به عنوان کاربر عادی یا root نصب می‌کنید:

| نصب‌کننده | کد در | باینری `hermes` | دایرکتوری داده |
| --- | --- | --- | --- |
| هر کاربر (git installer) | ~/.hermes/hermes-agent/ | ~/.local/bin/hermes (symlink) | ~/.hermes/ |
| حالت root (sudo curl … \| sudo bash) | /usr/local/lib/hermes-agent/ | /usr/local/bin/hermes | /root/.hermes/ (یا $HERMES_HOME) |

چیدمان FHS حالت root (`/usr/local/lib/…`، `/usr/local/bin/hermes`) با جایی که سایر ابزارهای توسعه سیستمی در Linux قرار می‌گیرند هماهنگ است. برای استقرارهای ماشین مشترک که یک نصب سیستمی باید هر کاربری را خدمت‌دهی کند مفید است. پیکربندی هر کاربر (احراز هویت، skillها، sessionها) همچنان در `~/.hermes/` یا `HERMES_HOME` صریح هر کاربر قرار دارد.

### بعد از نصب

Shell خود را مجدداً بارگذاری کنید و شروع به چت کنید:

```bash
source ~/.bashrc   # یا: source ~/.zshrc
hermes             # شروع چت!
```

برای پیکربندی مجدد تنظیمات خاص، از فرمان‌های اختصاصی استفاده کنید:

```bash
hermes model          # انتخاب ارائه‌دهنده و مدل LLM
hermes tools          # پیکربندی ابزارهای فعال
hermes gateway setup  # راه‌اندازی پلتفرم‌های پیام‌رسانی
hermes config set     # تنظیم مقادیر پیکربندی خاص
hermes setup          # یا اجرای جادوگر پیکربندی کامل برای پیکربندی همه چیز یکجا
```

یک اشتراک ۳۰۰+ مدل به علاوه [Tool Gateway](/docs/user-guide/features/tool-gateway) (جستجوی وب، تولید تصویر، TTS، مرورگر ابری) را پوشش می‌دهد. کلیدهای ابزار به ابزار را رد کنید:

```bash
hermes setup --portal
```

شما را وارد می‌کند، Nous را به عنوان ارائه‌دهنده شما تنظیم می‌کند و Tool Gateway را با یک فرمان فعال می‌کند.

## پیش‌نیازها

نصب‌کننده: در پلتفرم‌های غیر از Windows، تنها پیش‌نیاز Git است. در Linux همچنین مطمئن شوید `curl` و `xz-utils` موجود هستند (نصب‌کننده Node.js را به صورت آرشیو `.tar.xz` دانلود می‌کند). اپلیکیشن دسکتاپ علاوه بر این به `g++` (یا `build-essential` در Debian/Ubuntu) برای کامپایل ماژول‌های بومی نیاز دارد. نصب‌کننده بقیه را به طور خودکار مدیریت می‌کند:

- `uv` (مدیر بسته سریع Python)
- Python 3.11 (از طریق uv، نیاز به sudo نیست)
- Node.js v22 (برای اتوماسیون مرورگر و پل WhatsApp)
- `ripgrep` (جستجوی سریع فایل)
- `ffmpeg` (تبدیل فرمت صدا برای TTS)

نیازی نیست Python، Node.js، ripgrep یا ffmpeg را به صورت دستی نصب کنید. نصب‌کننده تشخیص می‌دهد چه چیزی وجود ندارد و آن را برای شما نصب می‌کند. فقط مطمئن شوید `git` موجود است (`git --version`). در Linux، اطمینان حاصل کنید `curl` و `xz-utils` نصب هستند (`sudo apt install curl xz-utils` در Debian/Ubuntu). برای اپلیکیشن دسکتاپ، `build-essential` را هم نصب کنید (`sudo apt install build-essential`).

Nix دیگر یک مسیر نصب پشتیبانی‌شده به طور رسمی نیست (فقط بهترین تلاش). اگر قبلاً از Nix استفاده می‌کنید (در NixOS، macOS یا Linux)، یک مسیر تنظیم اختصاصی با Nix flake، ماژول اعلامی NixOS و حالت container اختیاری وجود دارد. [راهنمای Nix & NixOS Setup](/docs/getting-started/nix-setup) را ببینید.

## نصب دستی / توسعه‌دهنده

اگر می‌خواهید مخزن را clone کرده و از source نصب کنید — برای مشارکت، اجرا از یک شاخه خاص یا کنترل کامل روی محیط مجازی — [بخش Development Setup](/docs/developer-guide/contributing#development-setup) در راهنمای Contributing را ببینید.

## نصب‌های بدون Sudo / کاربر سرویس سیستمی

اجرا کردن Hermes به عنوان یک کاربر غیرمجاز اختصاصی (مثلاً حساب سرویس systemd `hermes`، یا هر کاربری بدون دسترسی sudo) پشتیبانی می‌شود. تنها چیزی در مسیر نصب که واقعاً به root نیاز دارد، مرحله `--with-deps` Playwright است که کتابخانه‌های مشترک (`libnss3`، `libxkbcommon` و غیره) مورد استفاده Chromium را از طریق apt نصب می‌کند. نصب‌کننده تشخیص می‌دهد آیا sudo موجود است و وقتی نیست به طور محترمانه کاهش می‌یابد — باینری Chromium را در کش Playwright محلی کاربر سرویس نصب می‌کند و فرمان دقیقی که مدیر سیستم باید جداگانه اجرا کند را چاپ می‌کند.

تقسیم توصیه‌شده (Debian/Ubuntu):

1. یک بار، به عنوان کاربر مدیر با sudo، کتابخانه‌های سیستمی مورد نیاز Chromium را نصب کنید:
```bash
sudo npx playwright install-deps chromium
```
(می‌توانید این را از هر جایی اجرا کنید — npx Playwright را به صورت آنی دریافت می‌کند.)

2. به عنوان کاربر سرویس غیرمجاز، نصب‌کننده عادی را اجرا کنید. sudo موجود را تشخیص می‌دهد، `--with-deps` را رد می‌کند و Chromium را در کش Playwright محلی کاربر نصب می‌کند:
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```
اگر می‌خواهید مرحله Playwright را کلاً رد کنید — مثلاً چون headless اجرا می‌کنید و به اتوماسیون مرورگر نیاز ندارید — `--skip-browser` را پاس دهید:
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-browser
```

3. `hermes` را در shellهای کاربر سرویس در دسترس قرار دهید. نصب‌کننده launcher را در `~/.local/bin/hermes` می‌نویسد. حساب‌های سرویس سیستمی اغلب PATH حداقلی دارند که `~/.local/bin` را شامل نمی‌شود. یا آن را به محیط کاربر اضافه کنید، یا symlink launcher را در یک مکان سیستمی ایجاد کنید:
```bash
# گزینه A — اضافه کردن به پروفایل کاربر سرویس
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
# گزینه B — symlink سراسری (به عنوان مدیر اجرا کنید)
sudo ln -s /home/hermes/.hermes/hermes-agent/venv/bin/hermes /usr/local/bin/hermes
```

4. اعتبارسنجی: `hermes doctor` اکنون باید به طور تمیز اجرا شود. اگر `ModuleNotFoundError: No module named 'dotenv'` دریافت کردید، دارید فایل source `hermes` مخزن (`~/.hermes/hermes-agent/hermes`) را با Python سیستمی به جای launcher venv (`~/.hermes/hermes-agent/venv/bin/hermes`) فراخوانی می‌کنید — مرحله ۳ را تعمیر کنید.

همین الگو در Arch (نصب‌کننده از pacman با همان منطق تشخیص sudo استفاده می‌کند)، Fedora/RHEL و openSUSE کار می‌کند — آن توزیع‌ها از `--with-deps` اصلاً پشتیبانی نمی‌کنند، بنابراین مدیر سیستم همیشه کتابخانه‌های سیستمی را جداگانه نصب می‌کند. فرمان‌های مرتبط dnf/zypper توسط نصب‌کننده چاپ می‌شوند.

## عیب‌یابی

| مشکل | راه‌حل |
| --- | --- |
| hermes: command not found | Shell خود را مجدداً بارگذاری کنید (`source ~/.bashrc`) یا PATH را بررسی کنید |
| API key not set | `hermes model` را برای پیکربندی ارائه‌دهنده اجرا کنید، یا `hermes config set OPENROUTER_API_KEY your_key` |
| Missing config after update | `hermes config check` و سپس `hermes config migrate` را اجرا کنید |

برای عیب‌یابی بیشتر، `hermes doctor` را اجرا کنید — دقیقاً به شما می‌گوید چه چیزی وجود ندارد و چگونه آن را تعمیر کنید.

## تشخیص خودکار روش نصب

Hermes به طور خودکار تشخیص می‌دهد آیا از طریق pip، git installer، Homebrew یا NixOS نصب شده و `hermes update` فرمان به‌روزرسانی متناظر را برای آن مسیر چاپ می‌کند. نیازی به تنظیم متغیر محیطی نیست — تشخیص بر اساس چیدمان نصب است (Python site-packages، `~/.hermes/hermes-agent/`، پیشوند Homebrew یا مسیر Nix store). `hermes doctor` همچنین روش تشخیص داده شده را در خلاصه محیط خود نشان می‌دهد.

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/installation.md)
