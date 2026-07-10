---
layout: docs
title: "ویندوز (WSL2)"
permalink: /docs/user-guide/windows-wsl-quickstart/
---

- 
- استفاده از Hermes
- ویندوز (WSL2)

# راهنمای Windows (WSL2)

Hermes Agent اکنون هم از Windows بومی و هم از WSL2 پشتیبانی می‌کند. این صفحه مسیر WSL2 را پوشش می‌دهد؛ برای نصب PowerShell بومی به [راهنمای Windows (بومی)](/docs/user-guide/windows-native) مراجعه کنید.

[راهنمای Windows (بومی)](/docs/user-guide/windows-native)

چه زمانی WSL2 را به جای نصب بومی انتخاب کنید:

- می‌خواهید از ترمinal تعبیه‌شده داشبورد (تب `/chat`) استفاده کنید — آن پنل به POSIX PTY نیاز دارد و فقط در WSL2 موجود است.
- در حال انجام توسعه سنگین POSIX هستید و می‌خواهید sessionهای Hermes شما همان فایل‌سیستم / مسیرهای ابزارهای توسعه شما را به اشتراک بگذارند.
- از قبل یک محیط WSL2 دارید و نمی‌خواهید یک نصب دوم را مدیریت کنید.

`/chat`

چه زمانی نصب بومی خوب است (یا بهتر):

- چت تعاملی، gateway (Telegram/Discord/و غیره)، زمان‌بند Cron، ابزار مرورگر، سرورهای MCP و بیشتر ویژگی‌های Hermes همه به طور بومی روی Windows اجرا می‌شوند.
- نمی‌خواهید هر بار که به فایلی ارجاع می‌دهید یا URL را باز می‌کنید به عبور از مرز WSL↔Windows فکر کنید.

در WSL2 در واقع دو کامپیوتر در بازی هستند: هاست Windows شما، و یک Linux VM مدیریت‌شده توسط WSL. بیشتر سردرگمی‌ها از مطمئن نبودن اینکه در هر لحظه روی کدام هستید ناشی می‌شود.

این راهنمای بخش‌هایی از آن جداسازی را پوشش می‌دهد که به طور خاص بر Hermes تأثیر می‌گذارند: نصب WSL2، انتقال فایل‌ها بین Windows و Linux، شبکه‌سازی در هر دو جهت و دام‌هایی که افراد واقعاً با آن‌ها مواجه می‌شوند.

یک راهنمای چینی‌زبان از حداقل مسیر نصب در همین صفحه نگهداری می‌شود — از طریق منوی زبان (بالا سمت راست) سوئیچ کنید و 简体中文 را انتخاب کنید.

## چرا WSL2 (در مقابل Windows بومی)​

نصب Windows بومی مستقیماً در Windows اجرا می‌شود: ترمinal Windows شما (PowerShell، Windows Terminal و غیره)، مسیرهای فایل‌سیستم Windows (`C:\Users\…`) و فرآیندهای Windows. Hermes از Git Bash برای اجرای فرمان‌های shell استفاده می‌کند، که همان استراتژی‌ای است که Claude Code و سایر agentها امروزه برای Windows استفاده می‌کنند — این روش از شکاف POSIX-vs-Windows بدون بازنویسی کامل عبور می‌کند.

`C:\Users\…`

WSL2 یک کرنل واقعی Linux را در یک VM سبک اجرا می‌کند، بنابراین Hermes داخل آن اساساً مشابه اجرا روی Ubuntu است. این زمانی ارزشمند است که یک محیط POSIX واقعی می‌خواهید: `fork`، `/tmp`، سوکت‌های UNIX، معنای سیگنال‌ها، ترمینال‌های PTY-backed، shellهایی مانند `bash`/`zsh` و ابزارهایی مانند `rg`، `git`، `ffmpeg` که مانند Linux رفتار می‌کنند.

`fork`
`/tmp`
`bash`
`zsh`
`rg`
`git`
`ffmpeg`

پیامدهای عملی WSL2:

- CLI Hermes، gateway، sessionها، حافظه، skillها و runtime ابزارها همه داخل Linux VM زندگی می‌کنند.
- برنامه‌های Windows (مرورگرها، اپلیکیشن‌های بومی، Chrome با پروفایل ورود شما) خارج از آن زندگی می‌کنند.
- هر بار که می‌خواهید این دو با هم صحبت کنند — فایل‌ها را به اشتراک بگذارند، URLها را باز کنند، Chrome را کنترل کنند، به سرور مدل محلی دسترسی پیدا کنند، gateway Hermes را در معرض تلفن خود قرار دهند — از یک مرز عبور می‌کنید. این مرزها دقیقاً موضوع این راهنما هستند.

## نصب WSL2​

از یک PowerShell با دسترسی Admin یا Windows Terminal:

```
wsl --install
```

در یک Windows 10 22H2+ یا Windows 11 تازه این کرنل WSL2، ویژگی Virtual Machine Platform و یک distro پیش‌فرض Ubuntu را نصب می‌کند. هنگام درخواست ری‌بوت کنید. پس از ری‌بوت Ubuntu باز می‌شود و نام کاربری + رمز عبور Linux می‌خواهد — این یک کاربر Linux جدید است و به حساب Windows شما ربطی ندارد.

مطمئن شوید واقعاً روی WSL2 هستید (نه WSL1 قدیمی):

```
wsl --list --verbose
```

باید `VERSION  2` را ببینید. اگر یک distro `VERSION  1` نشان می‌دهد، آن را تبدیل کنید:

`VERSION  2`
`VERSION  1`

```
wsl --set-version Ubuntu 2wsl --set-default-version 2
```

Hermes روی WSL1 به طور قابل اعتماد کار نمی‌کند — WSL1 syscalls لینوکس را به صورت بلادرنگ ترجمه می‌کند و برخی رفتارها (procfs، سیگنال‌ها، شبکه) از Linux واقعی منحرف می‌شوند.

### انتخاب Distro​

Ubuntu (LTS) همان چیزی است که ما روی آن تست می‌کنیم. Debian کار می‌کند. Arch و NixOS برای افرادی که می‌خواهند کار می‌کنند، اما نصب‌کننده یک‌خطی فرض سیستم `apt` مشتق‌شده از Debian را دارد — برای آن مسیر به [راهنمای تنظیم Nix](/docs/getting-started/nix-setup) مراجعه کنید.

`apt`
[راهنمای تنظیم Nix](/docs/getting-started/nix-setup)

### فعال‌سازی systemd (توصیه شده)​

gateway hermes (و هر چیز دیگری که می‌خواهید در حال اجرا باقی بماند) با systemd راحت‌تر مدیریت می‌شود. در WSL مدرن، آن را یک بار داخل distro خود فعال کنید:

```
sudo tee /etc/wsl.conf >/dev/null <<'EOF'[boot]systemd=true[interop]enabled=trueappendWindowsPath=true[automount]options = "metadata,umask=22,fmask=11"EOF
```

سپس از PowerShell:

```
wsl --shutdown
```

ترمinal WSL خود را دوباره باز کنید. `ps -p 1 -o comm=` باید `systemd` را چاپ کند.

`ps -p 1 -o comm=`
`systemd`

گزینه `metadata` mount در بالا مهم است — بدون آن، فایل‌ها روی `/mnt/c/...` نمی‌توانند بیت‌های مجوز Linux واقعی را ذخیره کنند، که چیزهایی مانند `chmod +x` روی اسکریپت‌ها در مسیرهای Windows را خراب می‌کند.

`metadata`
`/mnt/c/...`
`chmod +x`

### نصب Hermes داخل WSL​

وقتی یک shell WSL2 باز دارید:

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bashsource ~/.bashrchermes
```

نصب‌کننده WSL2 را مانند Linux معمولی رفتار می‌کند — چیز خاصی برای WSL لازم نیست. برای چیدمان کامل به [نصب](/docs/getting-started/installation) مراجعه کنید.

[نصب](/docs/getting-started/installation)

## فایل‌سیستم: عبور از مرز Windows ↔ WSL2​

این بخشی است که بیشتر افراد را به دردسر می‌اندازد. دو فایل‌سیستم وجود دارد و اینکه فایل‌های خود را کجا قرار می‌دهید مهم است — برای عملکرد، صحت و اینکه چه ابزارهایی می‌توانند ببینند.

### دو جهت​

| جهت | مسیر داخلی | مسیری که استفاده می‌کنید |
| --- | --- | --- |
| دیسک Windows، دیده شده از WSL | `C:\Users\you\Documents` | `/mnt/c/Users/you/Documents` |
| دیسک WSL، دیده شده از Windows | `/home/you/code` | `\\wsl$\Ubuntu\home\you\code` (یا `\\wsl.localhost\Ubuntu\...` در بیلدهای جدیدتر) |

`C:\Users\you\Documents`
`/mnt/c/Users/you/Documents`
`/home/you/code`
`\\wsl$\Ubuntu\home\you\code`
`\\wsl.localhost\Ubuntu\...`

هر دو واقعی هستند، هر دو کار می‌کنند، اما یک فایل‌سیستم واحد نیستند — آن‌ها توسط یک پروتکل شبکه 9P در زیر پوشش پل زده شده‌اند. این پیامدهای عملکردی و معنایی واقعی دارد.

### کجا Hermes و پروژه‌های خود را قرار دهید​

قانون کلی: همه چیز Linux-مانند را داخل فایل‌سیستم Linux نگه دارید.

- نصب Hermes شما (`~/.hermes/`) — سمت Linux. نصب‌کننده این کار را انجام می‌دهد.
- مخازن git خود که از WSL کار می‌کنید — سمت Linux (`~/code/...`، `~/projects/...`).
- مدل‌ها، دیتاست‌ها، venvها — سمت Linux.

`~/.hermes/`
`~/code/...`
`~/projects/...`

چیزی که با پیروی از این قانون به دست می‌آورید:

- **I/O سریع.** عملیات روی `/mnt/c/...` از طریق 9P عبور می‌کنند و ۱۰-۱۰۰ برابر کندتر از ext4 بومی هستند. `git status` روی یک مخزن ۱۰k فایلی که در `~/code` فوری احساس می‌شود می‌تواند در `/mnt/c` بیش از ۱۵ ثانیه طول بکشد.
- **مجوزهای صحیح.** بیت‌های مجوز Linux تلاش بهترین شبیه‌سازی روی `/mnt/c` هستند. چیزهایی مانند `ssh` که کلیدی با "bad permissions" رد می‌کند یا `chmod +x` که بی‌صدا ناموفق می‌شود رایج هستند.
- **ناظران فایل قابل اعتماد.** inotify از طریق 9P ناپایدار است — ناظران فایل (سرورهای توسعه، اجرای تست‌ها) معمولاً تغییرات روی `/mnt/c` را از دست می‌دهند.
- **بدون شگفتی حساسیت به حروف.** مسیرهای Windows به طور پیش‌فرض حساس به حروف نیستند؛ Linux حساس به حروف است. پروژه‌هایی که هر دو `Readme.md` و `README.md` دارند بسته به اینکه کدام سمت هستید رفتار متفاوتی دارند.

`/mnt/c/...`
`git status`
`~/code`
`/mnt/c`
`/mnt/c`
`ssh`
`chmod +x`
`/mnt/c`
`Readme.md`
`README.md`

فایل‌ها را فقط زمانی روی `/mnt/c` قرار دهید که نیاز دارید فایلی در سمت Windows زندگی کند — مثلاً می‌خواهید آن را از یک اپلیکیشن GUI Windows باز کنید، یا DevTools MCP Chrome Windows نیاز دارد دایرکتوری فعلی مسیری قابل دسترس Windows باشد.

`/mnt/c`

### انتقال فایل‌ها به عقب و جلو​

**از Windows → به WSL:** ساده‌ترین راه باز کردن Explorer و تایپ `\\wsl.localhost\Ubuntu` در نوار آدرس است. سپس می‌توانید به `\home\<you>\....` درگ‌اپ کنید. یا از PowerShell:

`\\wsl.localhost\Ubuntu`
`\home\<you>\...`

```
wsl cp /mnt/c/Users/you/Downloads/file.pdf ~/incoming/
```

**از WSL → به Windows:** به `/mnt/c/Users/<you>/...` کپی کنید و فوراً در Windows Explorer ظاهر می‌شود:

`/mnt/c/Users/<you>/...`

```
cp ~/reports/output.pdf /mnt/c/Users/you/Desktop/
```

**باز کردن فایل WSL در یک برنامه Windows** (ویرایشگر GUI، مرورگر و غیره): از `explorer.exe` یا `wslview` استفاده کنید:

`explorer.exe`
`wslview`

```
sudo apt install wslu     # once — gives you wslview, wslpath, wslopen, etc.wslview ~/reports/output.pdf    # opens with the Windows default handlerexplorer.exe .                  # opens the current WSL dir in Windows Explorer
```

**تبدیل مسیرها بین دو دنیا:**

```
wslpath -w ~/code/project        # → \\wsl.localhost\Ubuntu\home\you\code\projectwslpath -u 'C:\Users\you'        # → /mnt/c/Users/you
```

### پایان خط‌ها، BOMها و git​

اگر فایل‌ها را در سمت Windows با یک ویرایشگر Windows ویرایش می‌کنید، ممکن است پایان خط `CRLF` بگیرند. وقتی `bash` یا Python در سمت Linux آن‌ها را می‌خواند، اسکریپت‌های shell با `bad interpreter: /bin/bash^M` خراب می‌شوند و Python ممکن است روی فایل‌های `.env` با BOM ناموفق شود.

`CRLF`
`bash`
`bad interpreter: /bin/bash^M`
`.env`

راه‌حل یک git config مناسب داخل WSL (نه در Windows) است:

```
git config --global core.autocrlf inputgit config --global core.eol lf
```

برای فایل‌هایی که از قبل CRLF دارند:

```
sudo apt install dos2unixdos2unix path/to/script.sh
```

### "Clone داخل WSL یا روی `/mnt/c`؟"​

`/mnt/c`

**Clone داخل WSL.** همیشه، مگر اینکه دلیل خاصی برای این کار نداشته باشید. یک گردش کار Hermes معمولی (`hermes chat`، فراخوانی‌های ابزاری که `rg`/`ripgrep` مخزن را می‌زنند، ناظران فایل، gateway پس‌زمینه) به طور چشمگیری سریع‌تر و قابل اعتمادتر روی `~/code/myrepo` نسبت به `/mnt/c/Users/you/myrepo` خواهد بود.

`hermes chat`
`rg`
`ripgrep`
`~/code/myrepo`
`/mnt/c/Users/you/myrepo`

یک استثنا: **پل‌های MCP که باینری‌های Windows را راه‌اندازی می‌کنند.** اگر از `chrome-devtools-mcp` از طریق `cmd.exe` استفاده می‌کنید (راهنمای MCP را ببینید: WSL → Windows Chrome)، Windows ممکن است با هشدار `UNC` شکایت کند اگر دایرکتوری کاری فعلی Hermes `~` باشد. در آن صورت، Hermes را از جایی زیر `/mnt/c/` شروع کنید تا فرآیند Windows یک cwd با حرف درایو داشته باشد.

`chrome-devtools-mcp`
`cmd.exe`
[راهنمای MCP: WSL → Windows Chrome](/docs/guides/use-mcp-with-hermes#wsl2-bridge-hermes-in-wsl-to-windows-chrome)
`UNC`
`~`
`/mnt/c/`

## شبکه‌سازی: WSL ↔ Windows​

WSL2 در یک VM سبک با پشته شبکه خاص خود اجرا می‌شود. این به این معنی است که `localhost` داخل WSL با `localhost` در Windows یکی نیست — از دیدگاه شبکه دو هاست جداگانه هستند. باید برای هر سرویس تصمیم بگیرید ترافیک در چه جهتی جریان دارد و پل مناسب را انتخاب کنید.

`localhost`
`localhost`

دو حالت مداوم پیش می‌آید.

### حالت ۱ — Hermes در WSL با یک سرویس در Windows صحبت می‌کند​

رایج‌ترین: دارید `Ollama`، `LM Studio` یا llama-server را در Windows اجرا می‌کنید و Hermes (داخل WSL) نیاز دارد به آن دسترسی پیدا کند.

نحوه استاندارد آن در راهنمای providerها زندگی می‌کند: [شبکه‌سازی WSL2 برای مدل‌های محلی →](/docs/integrations/providers#wsl2-networking-windows-users)

نسخه کوتاه:

- **Windows 11 22H2+:** حالت شبکه mirrored را فعال کنید (`networkingMode=mirrored` در `%USERPROFILE%\.wslconfig`، سپس `wsl --shutdown`). `localhost` سپس در هر دو جهت کار می‌کند.
- **Windows 10 یا بیلدهای قدیمی‌تر:** از IP هاست Windows (Gateway پیش‌فرض شبکه مجازی WSL) استفاده کنید و مطمئن شوید سرور در Windows به `0.0.0.0` bind شده، نه فقط `127.0.0.1`. Windows Firewall معمولاً برای پورت نیز به قاعده نیاز دارد.

`networkingMode=mirrored`
`%USERPROFILE%\.wslconfig`
`wsl --shutdown`
`localhost`
`0.0.0.0`
`127.0.0.1`

برای جدول کامل (آدرس‌های bind Ollama / LM Studio / vLLM / SGLang، یک‌خطی‌های قاعده firewall، کمک‌کننده‌های IP پویا، دور زدن Hyper-V firewall)، لینک بالا را دنبال کنید — آن را تکرار نکنید.

### حالت ۲ — چیزی در Windows (یا LAN شما) با Hermes در WSL صحبت می‌کند​

این جهت معکوس است و در جاهای دیگر کمتر مستند شده، اما چیزی است که برای این موارد نیاز دارید:

- استفاده از **داشبورد وب Hermes** از یک مرورگر Windows.
- استفاده از **سرور سازگار OpenAI API** (در معرض توسط `hermes gateway` وقتی `API_SERVER_ENABLED=true`) از یک ابزار سمت Windows. صفحه ویژگی API Server را ببینید.
- تست یک **gateway پیام‌رسانی** (Telegram، Discord و غیره) که پلتفرم یک URL webhook محلی را ping می‌کند — معمولاً از `cloudflared`/`ngrok` به جای port forwarding خام استفاده می‌کنید.

`hermes gateway`
`API_SERVER_ENABLED=true`
[صفحه ویژگی API Server](/docs/user-guide/features/api-server)
`cloudflared`
`ngrok`

#### زیرحالت ۲a: از هاست Windows خودش​

در **Windows 11 22H2+** با حالت mirrored فعال، کاری برای انجام دادن نیست. فرآیندی در WSL که به `0.0.0.0:8080` (یا حتی `127.0.0.1:8080`) bind شده از مرورگر Windows در `http://localhost:8080` قابل دسترسی است. WSL bind را به طور خودکار به هاست منتشر می‌کند.

`0.0.0.0:8080`
`127.0.0.1:8080`
`http://localhost:8080`

در **حالت NAT** (Windows 10 / Windows 11 قدیمی)، "localhost forwarding" پیش‌فرض در WSL2 معمولاً bindهای سمت Linux `127.0.0.1` را به `localhost` Windows فوروارد می‌کند، بنابراین سرویس Hermes که با `--host 127.0.0.1` شروع شده معمولاً به عنوان `http://localhost:PORT` از Windows قابل دسترسی است. اگر اینطور نیست:

`127.0.0.1`
`localhost`
`--host 127.0.0.1`
`http://localhost:PORT`
- صریحاً به `0.0.0.0` داخل WSL bind کنید.
- IP VM WSL را با `ip -4 addr show eth0 | grep inet` پیدا کنید و از Windows به آن بزنید.

`0.0.0.0`
`ip -4 addr show eth0 | grep inet`

#### زیرحالت ۲b: از دستگاه دیگری در LAN شما (تلفن، تبلت، PC دیگر)​

این درد واقعی است. ترافیک از **دستگاه LAN → هاست Windows → VM WSL** جریان دارد و باید هر دو hop را تنظیم کنید:

1. **در تمام interfaceها داخل WSL bind کنید.** فرآیندی که روی `127.0.0.1` گوش می‌دهد هرگز از خارج VM قابل دسترسی نخواهد بود. از `0.0.0.0` استفاده کنید.
2. **Port-forward Windows → VM WSL.** در حالت mirrored این خودکار است. در حالت NAT باید خودتان این کار را انجام دهید، به ازای هر پورت، در Admin PowerShell:

```
# Grab the WSL VM's current IP (it changes on every WSL restart under NAT)$wslIp = (wsl hostname -I).Trim().Split(' ')[0]# Forward Windows port 8080 → WSL:8080netsh interface portproxy add v4tov4 `  listenaddress=0.0.0.0 listenport=8080 `  connectaddress=$wslIp connectport=8080# Allow it through Windows FirewallNew-NetFirewallRule -DisplayName "Hermes WSL 8080" `  -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

بعداً با `netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8080` حذف کنید.

`netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8080`

3. **دستگاه LAN را به `http://<windows-lan-ip>:8080` اشاره دهید.**

`http://<windows-lan-ip>:8080`

از آنجا که IP VM WSL در حالت NAT در هر ری‌بوت جابجا می‌شود، یک قاعده یک‌باره فقط تا `wsl --shutdown` بعدی باقی می‌ماند. برای هر چیز پایدار، یا از حالت mirrored استفاده کنید یا مرحله port-proxy را در یک اسکریپتی قرار دهید که هنگام login Windows اجرا می‌شود.

`wsl --shutdown`

برای webhookهای از ارائه‌دهندگان پیام‌رسانی ابری (`setWebhook` Telegram، رویدادهای Slack و غیره)، با port fighting نجنگید — از تونل‌های `cloudflared` استفاده کنید. [راهنمای webhooks](/docs/user-guide/messaging/webhooks) را ببینید.

`setWebhook`
`cloudflared`
[راهنمای webhooks](/docs/user-guide/messaging/webhooks)

## اجرای طولانی‌مدت سرویس‌های Hermes در Windows​

**Tool Gateway** و سرور API Hermes فرآیندهای طولانی‌مدت هستند. در WSL2 چند گزینه برای نگه داشتن آن‌ها دارید.

[Tool Gateway](/docs/user-guide/features/tool-gateway)

### میانبر دسکتاپ برای باز کردن سریع Hermes​

اگر فقط یک لانچر کلیک-دوگانه برای یک shell تعاملی Hermes می‌خواهید، آن را در سمت Windows بسازید و بگذارید شما را به WSL ببرد:

1. روی دسکتاپ Windows کلیک راست کرده و New -> Shortcut را انتخاب کنید.
2. برای target، از نام distro خود استفاده کنید (اگر لازم است Ubuntu را جایگزین کنید):

```
wt.exe -w 0 -p "Ubuntu" wsl.exe -d Ubuntu --cd ~ -- bash -ic "hermes"
```

3. نامی واضح مانند Hermes بگذارید.

روی دسکتاپ Windows کلیک راست کرده و New -> Shortcut را انتخاب کنید.

برای target، از نام distro خود استفاده کنید (اگر لازم است Ubuntu را جایگزین کنید):

`Ubuntu`

`Hermes`

این Windows Terminal را باز می‌کند، distro WSL شما را شروع می‌کند، شما را در دایرکتوری خانه Linux خود قرار می‌دهد و Hermes را راه‌اندازی می‌کند. اگر `hermes` هنوز در PATH نیست، یک بار WSL را دستی باز کنید و `source ~/.bashrc` را اجرا کنید، یا دستور را با `uv run hermes` داخل checkout پروژه خود جایگزین کنید.

`hermes`
`source ~/.bashrc`
`uv run hermes`

**تکمیل اختیاری:**

- آیکون سفارشی: Properties -> Change Icon را باز کنید و به یک فایل `.ico` اشاره کنید، مانند favicon Hermes از مخزن.
- لانچر pin شده: وقتی میانبر کار کرد، آن را در Start یا Taskbar pin کنید تا مجبور نباشید دوباره جستجو کنید.

`.ico`

### داخل WSL با systemd (توصیه شده)​

اگر طبق بخش تنظیمات بالا systemd را فعال کرده‌اید، `hermes gateway` و سرور API دقیقاً مانند هر ماشین Linux کار می‌کنند. از جادوگر تنظیم gateway استفاده کنید:

`hermes gateway`

```
hermes gateway setup
```

پیشنهاد نصب یک systemd user unit می‌دهد تا gateway هنگام شروع WSL به طور خودکار بالا بیاید.

### شروع خودکار WSL هنگام login Windows​

VM WSL فقط زمانی زنده می‌ماند که چیزی از آن استفاده کند. برای نگه داشتن gateway قابل دسترس بدون باز بودن پنجره ترمinal، یک فرآیند WSL را هنگام login Windows از طریق Task Scheduler راه‌اندازی کنید:

- **Trigger:** At log on (your user).
- **Action:** Start a program

**Program:** `C:\Windows\System32\wsl.exe`
**Arguments:** `-d Ubuntu --exec /bin/sh -c "sleep infinity"`

`C:\Windows\System32\wsl.exe`
`-d Ubuntu --exec /bin/sh -c "sleep infinity"`

این VM را زنده نگه می‌دارد تا gateway مدیریت‌شده توسط systemd در حال اجرا باقی بماند. در Windows 11، جریان‌های جدیدتر `wsl --install --no-launch` + auto-start نیز کار می‌کنند؛ ترفند `sleep infinity` نسخه قابل حمل است.

`wsl --install --no-launch`
`sleep infinity`

## GPU passthrough (مدل‌های محلی)​

WSL2 از GPUهای **NVIDIA** از WSL kernel 5.10.43+ به طور بومی پشتیبانی می‌کند — درایور استاندارد NVIDIA را در Windows نصب کنید (درایور Linux NVIDIA را **در** WSL نصب **نکنید**) و `nvidia-smi` داخل WSL GPU را خواهد دید. از آنجا، CUDA toolkits، `torch`، `vllm`، `sglang` و `llama-server` مانند معمول با GPU واقعی build می‌شوند.

`nvidia-smi`
`torch`
`vllm`
`sglang`
`llama-server`

پشتیبانی AMD ROCm و Intel Arc داخل WSL2 هنوز در حال تکامل است و خارج از ماتریس تست Hermes قرار دارد — ممکن است با درایورهای فعلی کار کند اما دستورالعملی برای توصیه نداریم.

اگر یک سرور مدل محلی **Windows-بومی** (Ollama for Windows، LM Studio) اجرا می‌کنید که از قبل از طریق درایورهای Windows از GPU شما استفاده می‌کند، اصلاً به GPU passthrough WSL نیاز ندارید — فقط حالت ۱ بالا را دنبال کنید و از WSL از طریق شبکه به آن بزنید.

## دام‌های رایج​

**"Connection refused" به Ollama / LM Studio میزبانی‌شده Windows من.** [شبکه‌سازی WSL2](/docs/integrations/providers#wsl2-networking-windows-users) را ببینید. نود درصد مواقع سرور به `127.0.0.1` bind شده و به `0.0.0.0` نیاز دارد (Ollama: `OLLAMA_HOST=0.0.0.0`)، یا قاعده firewall را از دست داده‌اید.

[شبکه‌سازی WSL2](/docs/integrations/providers#wsl2-networking-windows-users)
`127.0.0.1`
`0.0.0.0`
`OLLAMA_HOST=0.0.0.0`

**کندی شدید در `git status`/`hermes chat` در یک مخزن.** احتمالاً زیر `/mnt/c/...` کار می‌کنید. مخزن را به `~/code/...` (سمت Linux) منتقل کنید. سرعت به مراتب بیشتر.

`git status`
`hermes chat`
`/mnt/c/...`
`~/code/...`

**`bad interpreter: /bin/bash^M` در اسکریپت‌ها.** پایان خط CRLF از ویرایشگر Windows. `dos2unix script.sh` و `core.autocrlf input` را در git config WSL خود تنظیم کنید.

`bad interpreter: /bin/bash^M`
`dos2unix script.sh`
`core.autocrlf input`

**هشدار "UNC paths are not supported" از باینری‌های Windows راه‌اندازی‌شده از طریق MCP.** cwd Hermes داخل فایل‌سیستم Linux است و `cmd.exe` Windows نمی‌داند با آن چه کند. Hermes را از `/mnt/c/...` برای آن session شروع کنید، یا از یک wrapper استفاده کنید که قبل از فراخوانی اجرایی Windows به مسیر قابل دسترس Windows `cd` کند.

`cmd.exe`
`/mnt/c/...`
`cd`

**جابجایی ساعت پس از sleep/hibernate.** ساعت WSL2 ممکن است پس از بازیابی هاست از sleep چند دقیقه عقب بیفتد، که هر چیز مبتنی بر certificate (OAuth، APIهای HTTPS) را خراب می‌کند. درخواست رفع کنید:

```
sudo hwclock -s
```

یا `ntpdate` را نصب کرده و هنگام login اجرا کنید.

`ntpdate`

**DNS پس از فعال‌سازی حالت mirrored، یا هنگام اتصال VPN متوقف می‌شود.** حالت mirrored تنظیمات شبکه هاست را به WSL پروکسی می‌کند — اگر DNS Windows مشکل دارد (VPN split-tunnel، resolver سازمانی)، WSL آن را به ارث می‌برد. راه‌حل: `resolv.conf` را دستی override کنید (در `/etc/wsl.conf` `generateResolvConf=false` تنظیم کنید، سپس `/etc/resolv.conf` خود را با `1.1.1.1` یا DNS VPN خود بنویسید).

`resolv.conf`
`generateResolvConf=false`
`/etc/wsl.conf`
`/etc/resolv.conf`
`1.1.1.1`

**`hermes` پس از اجرای نصب‌کننده یافت نمی‌شود.** نصب‌کننده `~/.local/bin` را از طریق `~/.bashrc` به PATH shell شما اضافه می‌کند. برای اثرگذاری در session فعلی باید `source ~/.bashrc` (یا باز کردن ترمinal جدید) اجرا کنید.

`hermes`
`~/.local/bin`
`~/.bashrc`
`source ~/.bashrc`

**Windows Defender روی فایل‌های WSL کند است.** Defender فایل‌ها را از طریق پل 9P اسکن می‌کند وقتی از Windows دسترسی پیدا می‌کنند، که کندی دسترسی cross-boundary سبک `/mnt/c` را بزرگ‌نمایی می‌کند. اگر فقط از داخل WSL به فایل‌های WSL دسترسی پیدا می‌کنید، این مهم نیست. اگر از ابزارهای Windows علیه `\\wsl$\...` به طور مکرر استفاده می‌کنید، مسیر distro WSL را از اسکن real-time خارج کنید考虑考虑.

`/mnt/c`
`\\wsl$\...`

**تمام شدن فضای دیسک.** WSL2 دیسک VM خود را به عنوان یک VHDX پراکنده زیر `%LOCALAPPDATA%\Packages\...` ذخیره می‌کند. رشد می‌کند اما هنگام حذف فایل‌ها به طور خودکار کوچک نمی‌شود. برای بازپس‌گیری فضا: `wsl --shutdown`، سپس از Admin PowerShell `Optimize-VHD -Path <path-to-ext4.vhdx> -Mode Full` اجرا کنید (نیاز به ابزارهای Hyper-V) — یا مسیر ساده‌تر `diskpart` مستند شده در WSL docs.

`%LOCALAPPDATA%\Packages\...`
`wsl --shutdown`
`Optimize-VHD -Path <path-to-ext4.vhdx> -Mode Full`
`diskpart`

## قدم بعدی کجاست​

- [نصب](/docs/getting-started/installation) — مراحل نصب واقعی (Linux/WSL2/Termux همه از همان نصب‌کننده استفاده می‌کنند).
- [Integrations → Providers → WSL2 Networking](/docs/integrations/providers#wsl2-networking-windows-users) — بررسی عمیق شبکه‌سازی استاندارد برای سرورهای مدل محلی.
- [MCP guide → WSL → Windows Chrome](/docs/guides/use-mcp-with-hermes#wsl2-bridge-hermes-in-wsl-to-windows-chrome) — کنترل Chrome Windows ورود شده از Hermes در WSL.
- [Tool Gateway](/docs/user-guide/features/tool-gateway) و [Web Dashboard](/docs/user-guide/features/web-dashboard) — سرویس‌های طولانی‌مدتی که بیشتر می‌خواهید از WSL به بقیه شبکه خود در معرض بگذارید.

[نصب](/docs/getting-started/installation)
[Integrations → Providers → WSL2 Networking](/docs/integrations/providers#wsl2-networking-windows-users)
[MCP guide → WSL → Windows Chrome](/docs/guides/use-mcp-with-hermes#wsl2-bridge-hermes-in-wsl-to-windows-chrome)
[Tool Gateway](/docs/user-guide/features/tool-gateway)
[Web Dashboard](/docs/user-guide/features/web-dashboard)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/windows-wsl-quickstart.md)