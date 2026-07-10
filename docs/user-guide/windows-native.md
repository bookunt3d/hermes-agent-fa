---
layout: docs
title: "ویندوز (بومی)"
permalink: /user-guide/windows-native/
---

- 
- Using Hermes
- Windows (Native)

# راهنمای ویندوز (بومی)

Hermes به طور بومی روی Windows 10 و Windows 11 اجرا می‌شود — بدون WSL، بدون Cygwin، بدون Docker. این صفحه عمیق است: چه چیزی به طور بومی کار می‌کند، چه چیزی فقط WSL است، نصب‌کننده واقعاً چه کاری انجام می‌دهد و دکمه‌های مختص ویندوز که ممکن است نیاز به لمس داشته باشید.

اگر فقط می‌خواهید نصب کنید، یک‌خطی در [صفحه اصلی](/docs/) یا [صفحه نصب](/docs/getting-started/installation#windows-native-powershell) همه چیزی است که نیاز دارید. وقتی چیزی شما را شگفت‌زده کرد برگردید.

اگر ترجیح می‌دهید محیط POSIX واقعی داشته باشید (برای ترمinal تعبیه‌شده داشبورد، معنای `fork`، ناظران فایل سبک Linux و غیره)، [راهنمای Windows (WSL2)](/docs/user-guide/windows-wsl-quickstart) را ببینید. هر دو تمیز با هم همزیستی می‌کنند: داده‌های بومی در `%LOCALAPPDATA%\hermes` و داده‌های WSL در `~/.hermes` قرار دارند.

## نصب سریع

PowerShell (یا Windows Terminal) را باز کنید و اجرا کنید:

```powershell
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

نیازی به حقوق admin نیست. نصب‌کننده به `%LOCALAPPDATA%\hermes\` می‌رود و `hermes` را به User PATH اضافه می‌کند — بعد از اتمام یک ترمinal جدید باز کنید.

گزینه‌های نصب‌کننده (نیاز به فرم scriptblock برای ارسال پارامترها):

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1))) -NoVenv -SkipSetup -Branch main
```

| پارامتر | پیش‌فرض | هدف |
| --- | --- | --- |
| `-Branch` | main | Clone یک شاخه مشخص (مفید برای تست PR) |
| `-Commit` | تنظیم نشده | نصب را به یک commit SHA مشخص ثابت کنید (`-Branch` را override می‌کند) |
| `-Tag` | تنظیم نشده | نصب را به یک git tag مشخص ثابت کنید (مثلاً `v0.14.0`) |
| `-NoVenv` | خاموش | ایجاد venv را رد کنید (پیشرفته — خودتان Python را مدیریت می‌کنید) |
| `-SkipSetup` | خاموش | جادوگر post-install `hermes setup` را رد کنید |
| `-HermesHome` | %LOCALAPPDATA%\hermes | دایرکتوری داده را override کنید |
| `-InstallDir` | %LOCALAPPDATA%\hermes\hermes-agent | مکان کد را override کنید |

نصب‌کننده fetchهای git ناپایدار را به طور خودکار مجدداً تلاش می‌کند و BOM را از هر payload `install.ps1` دانلود شده حذف می‌کند، بنابراین UTF-8 BOM که در حین انتقال HTTP دریافت می‌شود دیگر فرم `[scriptblock]::Create((irm ...))` را خراب نمی‌کند.

### نصب‌کننده دسکتاپ (جایگزین)

یک نصب‌کننده GUI نازک نیز موجود است — مفید اگر ترجیح می‌دهید روی یک `.exe` دوبار کلیک کنید تا PowerShell را باز کنید. Hermes Desktop را دانلود کنید، نصب‌کننده را اجرا کنید و در اولین راه‌اندازی GUI در زیر پوشش `install.ps1` را برای تأمین Python (از طریق `uv`)، Node، PortableGit و بقیه راه‌اندازی وابستگی‌ها فراخوانی می‌کند.

## نصب‌کننده واقعاً چه کاری انجام می‌دهد

از بالا به پایین، به ترتیب:

1. **`uv` را راه‌اندازی می‌کند** — مدیر سریع Python Astral. در `%USERPROFILE%\.local\bin` نصب می‌شود.
2. **Python 3.11 را نصب می‌کند** از طریق `uv`. به Python موجود نیاز نیست.
3. **Node.js 22 را نصب می‌کند** (winget در صورت موجود بودن، در غیر این صورت بسته تار نصب پرتابل Node که در `%LOCALAPPDATA%\hermes\node` باز می‌شود). برای ابزار مرورگر و پل WhatsApp استفاده می‌شود.
4. **Git پرتابل نصب می‌کند** — اگر `git` از قبل در PATH باشد نصب‌کننده از آن استفاده می‌کند؛ در غیر این صورت یک `PortableGit` فشرده و خودمختار (~۴۵ MB، از انتشار رسمی `git-for-windows`) را در `%LOCALAPPDATA%\hermes\git` دانلود می‌کند.
5. **مخزن را در `%LOCALAPPDATA%\hermes\hermes-agent` clone می‌کند** و یک virtualenv در آن ایجاد می‌کند.
6. **`uv pip install` پلکانی** — ابتدا `.[all]` را تلاش می‌کند، به مجموعه‌های کوچک‌تر تدریجی برمی‌گردد.
7. **SDKهای پیام‌رسانی را به طور خودکار نصب می‌کند** — اگر `TELEGRAM_BOT_TOKEN`/`DISCORD_BOT_TOKEN`/`SLACK_BOT_TOKEN`/`SLACK_APP_TOKEN`/`WHATSAPP_ENABLED` موجود باشند.
8. **`HERMES_GIT_BASH_PATH` را تنظیم می‌کند** به `bash.exe` رفع‌شده.
9. **`%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts` را به User PATH اضافه می‌کند** و `HERMES_HOME=%LOCALAPPDATA%\hermes` را تنظیم می‌کند.
10. **`hermes setup` را اجرا می‌کند** — جادوگر اولین اجرای عادی. با `-SkipSetup` رد کنید.

در Windows، تنظیم کلید API به ازای هر ابزار بیشترین اصطکاک را در دریافت یک agent کاربردی دارد. یک اشتراک [Nous Portal](/docs/user-guide/features/tool-gateway) مدل و تمام آن ابزارها را از طریق یک ورود OAuth پوشش می‌دهد. بعد از اتمام نصب‌کننده، `hermes setup --portal` را اجرا کنید تا همه چیز را وصل کنید.

## ماتریس ویژگی‌ها

هر چیزی به جز ترمinal تعبیه‌شده داشبورد به طور بومی در Windows اجرا می‌شود.

| ویژگی | Windows بومی | WSL2 |
| --- | --- | --- |
| CLI (`hermes chat`، `hermes setup`، `hermes gateway` و غیره) | ✓ | ✓ |
| TUI تعاملی (`hermes --tui`) | ✓ | ✓ |
| Gateway پیام‌رسانی (Telegram، Discord، Slack، WhatsApp، ۱۵+ پلتفرم) | ✓ | ✓ |
| زمان‌بند Cron | ✓ | ✓ |
| ابزار مرورگر (Chromium از طریق Node) | ✓ | ✓ |
| سرورهای MCP (stdio و HTTP) | ✓ | ✓ |
| Ollama محلی / LM Studio / llama-server | ✓ | ✓ (از طریق شبکه WSL) |
| داشبورد وب (sessionها، jobها، معیارها، پیکربندی) | ✓ | ✓ |
| ترمinal تعبیه‌شده داشبورد/چت | ✗ (نیاز به POSIX PTY) | ✓ |
| شروع خودکار هنگام login | ✓ (schtasks) | ✓ (systemd) |

تب `/chat` داشبورد یک ترمinal واقعی از طریق POSIX PTY (ptyprocess) درج می‌کند. Windows بومی معادل بومی ندارد؛ `pywinpty`/Windows ConPTY Python کار می‌کند ولی پیاده‌سازی جداگانه است — به عنوان کار آینده در نظر بگیرید. بقیه داشبورد به طور بومی اجرا می‌شود — فقط آن یک تب بنر «برای این WSL2 استفاده کنید» نشان می‌دهد.

## نحوه اجرای فرمان‌های shell توسط Hermes در Windows

ابزار ترمinal Hermes فرمان‌ها را از طریق Git Bash اجرا می‌کند، همان استراتژی‌ای که Claude Code استفاده می‌کند.

ترتیب رفع `bash.exe`:

1. متغیر محیطی `HERMES_GIT_BASH_PATH` اگر تنظیم شده باشد.
2. `%LOCALAPPDATA%\hermes\git\usr\bin\bash.exe` (PortableGit مدیریت‌شده توسط نصب‌کننده).
3. `%LOCALAPPDATA%\hermes\git\bin\bash.exe` (چیدمان قدیمی‌تر Git-for-Windows).
4. نصب سیستمی Git-for-Windows (`%ProgramFiles%\Git\bin\bash.exe` و غیره).
5. MSYS2، Cygwin یا هر `bash.exe` در PATH به عنوان آخرین تلاش.

نصب‌کننده `HERMES_GIT_BASH_PATH` را به طور صریح تنظیم می‌کند تا sessionهای PowerShell جدید نیازی به کشف مجدد نداشته باشند.

**تله:** چیدمان MinGit با نصب‌کننده کامل Git-for-Windows متفاوت است — bash در `usr\bin\bash.exe` زندگی می‌کند، نه `bin\bash.exe`. Hermes هر دو را بررسی می‌کند. اگر آرشیو MinGit را به صورت دستی باز می‌کنید، مطمئن شوید نوع `non-busybox` (`MinGit-*-64-bit.zip`، نه `MinGit-*-busybox*.zip`) را انتخاب می‌کنید — بیلد‌های busybox به جای `bash`، `ash` ارائه می‌دهند و بیشتر coreutilsها موجود نیستند.

## کنسول UTF-8 در Windows

stdio پیش‌فرض Python در Windows از صفحه کد فعال کنسول (معمولاً `cp1252` یا `cp437`) استفاده می‌کند. بنر Hermes، لیست فرمان‌های اسلش، فید ابزار، پنل‌های Rich و توضیحات skill همه شامل Unicode هستند. بدون مداخله، هر کدام با `UnicodeEncodeError: 'charmap' codec can't encode character…` خراب می‌شوند.

راه‌حل در `hermes_cli/stdio.py::configure_windows_stdio()` است، که در هر entry point در ابتدای کار فراخوانی می‌شود.

## ویرایشگر (Ctrl-X Ctrl-E، /edit)

قبل از #21561، فشار `Ctrl-X Ctrl-E` یا تایپ `/edit` در Windows بی‌صدا هیچ کاری انجام نمی‌داد. prompt_toolkit یک لیست fallback مطلق POSIX ثابت‌شده دارد که در Windows هرگز حل نمی‌شود.

ویرایشگر stdio shim Windows Hermes اکنون `EDITOR=notepad` را به عنوان پیش‌فرض تنظیم می‌کند. Notepad در هر نصب Windows موجود است و به عنوان ویرایشگر blocking عمل می‌کند.

بازنویسی‌های کاربر همچنان اولویت دارند (قبل از `setdefault` بررسی می‌شوند):

| ویرایشگر | فرمان PowerShell |
| --- | --- |
| VS Code | `$env:EDITOR = "code --wait"` |
| Notepad++ | `$env:EDITOR = "'C:\Program Files\Notepad++\notepad++.exe' -multiInst -nosession"` |
| Neovim | `$env:EDITOR = "nvim"` |
| Helix | `$env:EDITOR = "hx"` |

پرچم `--wait` در VS Code حیاتی است — بدون آن ویرایشگر فوراً برمی‌گردد و Hermes یک بافر خالی دریافت می‌کند.

## Ctrl+Enter برای خط جدید در CLI

Windows Terminal `Ctrl+Enter` را به عنوان توالی کلید اختصاصی عبور می‌دهد. Hermes آن را به «درج خط جدید» bind می‌کند تا بتوانید پرامپت‌های چندخطی در CLI ترکیب کنید بدون بازگشت به Escape سپس Enter.

## اجرای gateway هنگام login Windows

`hermes gateway install` در Windows از Scheduled Tasks با fallback پوشه Startup استفاده می‌کند — نیازی به admin نیست.

### نصب

```bash
hermes gateway install
```

زیر پوشش چه اتفاقی می‌افتد:

1. `schtasks /Create /SC ONLOGON /RL LIMITED /TN HermesGateway` — یک task ثبت می‌کند که با مجوزهای استاندارد (غیر ارتقاء یافته) هنگام login شما اجرا می‌شود.
2. اگر `schtasks` توسط group policy مسدود شده باشد، یک میانبر `start /min cmd.exe /d /c <wrapper>` در `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` می‌نویسد.
3. gateway را جدا از طریق `pythonw.exe` ایجاد می‌کند — نه `python.exe`.

### مدیریت

```bash
hermes gateway status      # نمای ادغام‌شده
hermes gateway start       # task زمان‌بندی‌شده را الان شروع کنید
hermes gateway stop        # معادل SIGTERM مودبانه
hermes gateway restart
hermes gateway uninstall   # entry schtasks، میانبر Startup، فایل pid را حذف می‌کند
```

### چرا یک Windows Service نه؟

سرویس‌ها نیاز به حقوق admin برای نصب دارند و چرخه حیات gateway را به بوت ماشین متصل می‌کنند، نه login کاربر. کاربر معمولی Hermes می‌خواهد: login → gateway موجود، logout → gateway رفته. Scheduled Tasks دقیقاً همین کار را بدون ارتقاء انجام می‌دهند.

## چیدمان داده

| مسیر | محتوا |
| --- | --- |
| `%LOCALAPPDATA%\hermes\hermes-agent\` | Git checkout + venv. `venv\Scripts\hermes.exe` فرمان اضافه‌شده به User PATH است. |
| `%LOCALAPPDATA%\hermes\git\` | PortableGit (فقط اگر نصب‌کننده تأمین کرده باشد). |
| `%LOCALAPPDATA%\hermes\node\` | Node.js پرتابل (فقط اگر نصب‌کننده تأمین کرده باشد). |
| `%LOCALAPPDATA%\hermes\bin\` | `uv.exe` مدیریت‌شده Hermes. |
| `%LOCALAPPDATA%\hermes\` (ریشه) | پیکربندی، احراز هویت، skillها، sessionها، لاگ‌ها. از نصب‌های مجدد زنده می‌ماند. |

در Windows بومی نصب‌کننده `HERMES_HOME=%LOCALAPPDATA%\hermes` را تنظیم می‌کند. فقط زیردایرکتوری `hermes-agent\` را حذف کنید، نه کل `%LOCALAPPDATA%\hermes` را.

## ابزار مرورگر

ابزار مرورگر از `agent-browser` (یک کمک Node) برای هدایت Chromium استفاده می‌کند. Playwright Chromium در اولین اجرا به طور خودکار نصب می‌شود (`npx playwright install chromium`). اگر نصب ناموفق باشد، `hermes doctor` آن را با راهنمای تعمیر نشان می‌دهد.

## اجرا کردن Hermes در Windows — نکات عملی

### PATH بعد از نصب

نصب‌کننده `%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts` را از طریق `[Environment]::SetEnvironmentVariable` به User PATH اضافه می‌کند. ترمinal‌های موجود این را دریافت نمی‌کنند — بعد از نصب یک پنجره PowerShell جدید (یا تب Windows Terminal) باز کنید.

```powershell
Get-Command hermes        # باید C:\Users\<you>\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe را چاپ کند
hermes --version
```

### متغیرهای محیطی

Hermes هم `$env:X` (محدوده فرآیند) و هم متغیرهای محیطی User (دائمی) را رعایت می‌کند. تنظیم کلیدهای API در `%LOCALAPPDATA%\hermes\.env` (`HERMES_HOME` شما) مسیر عادی است — مانند Linux.

## حذف

از PowerShell:

```bash
hermes uninstall
```

مسیر تمیز است — entry schtasks، میانبر پوشه Startup، میانبر `hermes.cmd`، `%LOCALAPPDATA%\hermes\hermes-agent\` را حذف و User PATH را کوتاه می‌کند. بقیه `%LOCALAPPDATA%\hermes\` را دست نخورده باقی می‌گذارد (پیکربندی، احراز هویت، skillها، sessionها، لاگ‌ها).

برای حذف همه چیز:

```powershell
hermes uninstall
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\hermes"
# همچنین دایرکتوری داده CLI/WSL قدیمی را اگر قبلاً استفاده کرده‌اید حذف کنید:
Remove-Item -Recurse -Force "$env:USERPROFILE\.hermes"
```

## مدیریت فرآیند داخلی

این مطالب پس‌زمینه است — مگر اینکه در حال دیباگ یک عجیبی «خودش را می‌کشد» باشید، رد کنید.

در Linux و macOS، اصطلاح POSIX `os.kill(pid, 0)` یک بررسی مجوز بدون عمل است. در Windows، `os.kill` Python `sig=0` را به `CTRL_C_EVENT` نگاشت می‌کند — در مقدار عددی ۰ تداخل دارند — و آن را از طریق `GenerateConsoleCtrlEvent(0, pid)` مسیریابی می‌کند.

نتیجه: هر مسیر کدی که «بررسی کن آیا این PID زنده است» را از طریق `os.kill(pid, 0)` در Windows می‌گفت بی‌صدا هدف را می‌کشت. Hermes هر چنین سایتی را به `gateway.status._pid_exists()` مهاجرت داده که از `psutil.pid_exists()` استفاده می‌کند.

## مشکلات رایج

- **`hermes: command not found`** بعد از نصب — یک پنجره PowerShell جدید باز کنید.
- **`WinError 193: %1 is not a valid Win32 application`** — فراخوانی اسکریپت shebang از `.cmd` shim عبور کرد. از نسخه `.cmd` استفاده کنید (مثلاً `npx.cmd` نه `npx`).
- **`[scriptblock]::Create(...)` با `The assignment expression is not valid` ناموفق است** — دانلود `install.ps1` شما UTF-8 BOM دریافت کرد. با فرم ساده `irm | iex` دوباره اجرا کنید.
- **Gateway بعد از restart نمی‌ماند** — `hermes gateway status` را بررسی کنید. اگر `schtasks` ثبت شده ولی در حال اجرا نیست، group policy ممکن است triggerهای `ONLOGON` را مسدود کرده باشد.
- **ابزار مرورگر راه‌اندازی می‌شود ولی ابزارها timeout می‌خورند** — Chromium در اولین اجرا به طور خودکار نصب می‌شود. اگر نصب ناموفق بوده، `hermes doctor` را اجرا کنید.
- **کاراکترهای چینی/ژاپنی/عربی به صورت `?` در CLI نشان داده می‌شوند** — shim UTF-8 stdio فعال نشده. `HERMES_DISABLE_WINDOWS_UTF8` تنظیم نشده باشد.

## قدم بعدی

- [نصب](/docs/getting-started/installation) — صفحه نصب کامل
- [راهنمای Windows (WSL2)](/docs/user-guide/windows-wsl-quickstart) — اگر معنای POSIX یا ترمinal داشبورد می‌خواهید
- [مرجع CLI](/docs/reference/cli-commands) — هر زیرفرمان `hermes`
- [FAQ](/docs/reference/faq) — سوالات رایج غیرمختص Windows
- [Gateway پیام‌رسانی](/docs/user-guide/messaging/) — اجرای Telegram/Discord/Slack در Windows

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/windows-native.md)
