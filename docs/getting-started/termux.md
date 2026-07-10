---
layout: docs
title: "اندروید / Termux"
permalink: /docs/getting-started/termux/
---

- 
- Getting Started
- Android / Termux

# Hermes در اندروید با Termux

Termux (Android) یک [پلتفرم سطح ۲](/docs/getting-started/platform-support#tier-2) است. اسکریپت نصب و مستندات اینجا فقط به صورت بهترین تلاش نگهداری می‌شوند. commitها به main ممکن است در هر زمانی این بسته‌ها را خراب کنند.

Hermes Agent می‌تواند مستقیماً روی یک گوشی اندروید از طریق [Termux](https://termux.dev/) اجرا شود.

به شما یک CLI محلی کاربردی روی گوشی می‌دهد، به علاوه اکسترا‌های پایه‌ای که در حال حاضر می‌دانیم به طور تمیز در اندروید نصب می‌شوند.

## چه چیزی در مسیر تست‌شده پشتیبانی می‌شود؟

بسته Termux تست‌شده شامل می‌شود:

- CLI Hermes
- پشتیبانی cron
- پشتیبانی PTY/ترمینال پس‌زمینه
- پشتیبانی Telegram gateway (اجراهای پس‌زمینه دستی/بهترین تلاش)
- پشتیبانی MCP
- پشتیبانی حافظه Honcho
- پشتیبانی ACP

به طور مشخص، معادل این است:

```
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

## چه چیزی هنوز بخشی از مسیر تست‌شده نیست؟

تعداد کمی از ویژگی‌ها هنوز به وابستگی‌های سبک دسکتاپ/سرور نیاز دارند که برای اندروید منتشر نشده‌اند، یا هنوز روی گوشی‌ها اعتبارسنجی نشده‌اند:

- `.[all]` امروز در اندروید پشتیبانی نمی‌شود
- اکسترا `voice` توسط `faster-whisper -> ctranslate2` مسدود شده و `ctranslate2` چرخ‌های اندروید منتشر نمی‌کند
- راه‌اندازی خودکار مرورگر / Playwright در نصب‌کننده Termux رد می‌شود
- ایزولاسیون ترمینال مبتنی Docker در Termux موجود نیست
- اندروید همچنان ممکن است کارهای پس‌زمینه Termux را متوقف کند، بنابراین ماندگاری gateway بهترین تلاش است نه یک سرویس مدیریت‌شده عادی

این مانع از کار خوب Hermes به عنوان یک agent CLI بومی گوشی نمی‌شود — فقط به این معنی است که نصب موبایل توصیه‌شده عمداً از نصب دسکتاپ/سرور باریک‌تر است.

## گزینه ۱: نصب‌کننده یک‌خطی

Hermes اکنون یک مسیر نصب آگاه Termux ارائه می‌دهد:

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

در Termux، نصب‌کننده به طور خودکار:

- از `pkg` برای بسته‌های سیستمی استفاده می‌کند
- venv را با `python -m venv` ایجاد می‌کند
- ابتدا اکسترای گسترده `.[termux-all]` را تلاش می‌کند و به اکسترای کوچک‌تر `.[termux]` برمی‌گردد (سپس نصب پایه) — نصب‌کننده curl این ترتیب را به طور خودکار مطابقت می‌دهد
- `hermes` را در `$PREFIX/bin` لینک می‌کند تا در Termux PATH شما باقی بماند
- راه‌اندازی تست‌نشده مرورگر / WhatsApp را رد می‌کند

اگر فرمان‌های صریح می‌خواهید یا نیاز به عیب‌یابی یک نصب ناموفق دارید، از مسیر دستی زیر استفاده کنید.

## گزینه ۲: نصب دستی (کاملاً صریح)

### ۱. به‌روزرسانی Termux و نصب بسته‌های سیستمی

```
pkg update
pkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ffmpeg
```

چرا این بسته‌ها؟

- `python` — زمان اجرا + پشتیبانی venv
- `git` — clone/به‌روزرسانی مخزن
- `clang`، `rust`، `make`، `pkg-config`، `libffi`، `openssl` — برای ساخت چند وابستگی Python در اندروید لازم هستند
- `nodejs` — زمان اجرای Node اختیاری برای آزمایش‌های فراتر از مسیر پایه تست‌شده
- `ripgrep` — جستجوی سریع فایل
- `ffmpeg` — تبدیل رسانه / TTS

### ۲. Clone Hermes

```
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
```

### ۳. ایجاد محیط مجازی

```
python -m venv venv
source venv/bin/activate
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install --upgrade pip setuptools wheel
```

`ANDROID_API_LEVEL` برای بسته‌های مبتنی بر Rust / maturin مانند `jiter` مهم است.

### ۴. نصب بسته Termux تست‌شده

```
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

اگر فقط agent پایه حداقل می‌خواهید، این هم کار می‌کند:

```
python -m pip install -e '.' -c constraints-termux.txt
```

### ۵. `hermes` را در Termux PATH قرار دهید

```
ln -sf "$PWD/venv/bin/hermes" "$PREFIX/bin/hermes"
```

`$PREFIX/bin` در Termux از قبل در PATH است، بنابراین این کار فرمان `hermes` را بدون نیاز به فعال‌سازی مجدد venv در هر shell جدید پایدار می‌کند.

### ۶. اعتبارسنجی نصب

```
hermes version
hermes doctor
```

### ۷. Hermes را شروع کنید

```
hermes
```

## تنظیمات پیگیری توصیه‌شده

### پیکربندی یک مدل

```
hermes model
```

یا کلیدها را مستقیماً در `~/.hermes/.env` تنظیم کنید.

### اجرای مجدد جادوگر پیکربندی تعاملی کامل بعداً

```
hermes setup
```

### نصب دستی وابستگی‌های Node اختیاری

مسیر Termux تست‌شده عمداً راه‌اندازی Node/مرورگر را رد می‌کند. اگر می‌خواهید بعداً با ابزارهای مرورگر آزمایش کنید:

```
pkg install nodejs-lts
npm install
```

ابزار مرورگر به طور خودکار دایرکتوری‌های Termux (`/data/data/com.termux/files/usr/bin`) را در جستجوی PATH خود شامل می‌کند، بنابراین `agent-browser` و `npx` بدون هیچ پیکربندی PATH اضافی کشف می‌شوند.

تا زمانی که مستند نشده، ابزارهای مرورگر / WhatsApp در اندروید را به عنوان آزمایشی در نظر بگیرید.

## عیب‌یابی

### No solution found هنگام نصب `.[all]`

به جای آن از بسته Termux تست‌شده استفاده کنید:

```
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

انسدادکننده در حال حاضر اکسترا `voice` است:
- `voice` وابسته به `faster-whisper` است
- `faster-whisper` به `ctranslate2` وابسته است
- `ctranslate2` چرخ‌های اندروید منتشر نمی‌کند

### `uv pip install` در اندروید ناموفق است

به جای آن از مسیر Termux با stdlib venv + `pip` استفاده کنید:

```
python -m venv venv
source venv/bin/activate
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

### `jiter`/`maturin` درباره `ANDROID_API_LEVEL` شکایت می‌کند

سطح API را قبل از نصب به طور صریح تنظیم کنید:

```
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

### `hermes doctor` می‌گوید ripgrep یا Node وجود ندارد

آن‌ها را با بسته‌های Termux نصب کنید:

```
pkg install ripgrep nodejs
```

### خطاهای ساخت هنگام نصب بسته‌های Python

مطمئن شوید ابزار زنجیره ساخت نصب است:

```
pkg install clang rust make pkg-config libffi openssl
```

سپس دوباره تلاش کنید:

```
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

## محدودیت‌های شناخته‌شده در گوشی‌ها

- پشتیبان Docker ناموجود است
- تبدیل صوتی محلی از طریق `faster-whisper` در مسیر测试‌شده ناموجود است
- راه‌اندازی اتوماسیون مرورگر عمداً توسط نصب‌کننده رد می‌شود
- برخی اکستراهای اختیاری ممکن است کار کنند، اما فقط `.[termux]` و `.[termux-all]` در حال حاضر به عنوان بسته‌های تست‌شده اندروید مستند شده‌اند

اگر با یک مشکل جدید مختص اندروید مواجه شدید، لطفاً یک issue GitHub باز کنید و شامل موارد زیر باشید:

- نسخه اندروید شما
- `termux-info`
- `python --version`
- `hermes doctor`
- فرمان نصب دقیق و خروجی خطای کامل

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/termux.md)
