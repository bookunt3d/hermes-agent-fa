---
layout: docs
title: "سؤالات متداول"
permalink: /reference/faq/
---

- 
- مرجع
- سؤالات متداول و عیب‌یابی

# سؤالات متداول و عیب‌یابی

پاسخ‌ها و راه‌حل‌های سریع برای رایج‌ترین سؤالات و مشکلات.

## سؤالات متداول

### کدام ارائه‌دهندگان LLM با Hermes کار می‌کنند؟

Hermes Agent با هر API سازگار با OpenAI کار می‌کند. ارائه‌دهندگان پشتیبانی شده عبارتند از:

- [OpenRouter](https://openrouter.ai/) — دسترسی به صدها مدل از طریق یک API key (توصیه شده برای انعطاف‌پذیری)
- [Nous Portal](/docs/integrations/nous-portal) — دروازه اشتراک Nous Research — بیش از ۳۰۰ مدل به همراه وب/تصویر/TTS/مرورگر از طریق یک ورود OAuth (توصیه شده برای تازه‌کاران)
- OpenAI — GPT-5.4, GPT-5-codex, GPT-4.1, GPT-4o, و غیره
- Anthropic — مدل‌های Claude (API مستقیم، OAuth از طریق `hermes auth add anthropic`، OpenRouter، یا هر پروکسی سازگار)
- Google — مدل‌های Gemini (API مستقیم از طریق ارائه‌دهنده `gemini`، OpenRouter، یا پروکسی سازگار)
- z.ai / ZhipuAI — مدل‌های GLM
- Kimi / Moonshot AI — مدل‌های Kimi
- MiniMax — نقاط پایانی جهانی و چین
- مدل‌های محلی — از طریق [Ollama](https://ollama.com/)، [vLLM](https://docs.vllm.ai/)، [llama.cpp](https://github.com/ggerganov/llama.cpp)، [SGLang](https://github.com/sgl-project/sglang)، یا هر سرور سازگار با OpenAI

ارائه‌دهنده خود را با `hermes model` یا ویرایش `~/.hermes/.env` تنظیم کنید. برای کلیدهای تمام ارائه‌دهندگان به مرجع [Environment Variables](/docs/reference/environment-variables) مراجعه کنید.

### آیا روی Windows/Android/Termux/پلتفرم من کار می‌کند؟

برای ماتریکس کامل پشتیبانی پلتفرم به [Platform Support](/docs/getting-started/platform-support) مراجعه کنید.

### Hermes را در WSL2 اجرا می‌کنم. بهترین راه کنترل Chrome معمولی Windows من چیست؟

یک MCP bridge بر `/browser connect` ترجیح دهید.

الگوی توصیه شده:

- Hermes را داخل WSL2 اجرا کنید
- از Chrome معمولی وارد شده خود در Windows استفاده کنید
- `chrome-devtools-mcp` را به عنوان یک سرور MCP از طریق `cmd.exe` یا `powershell.exe` اضافه کنید
- اجازه دهید Hermes از ابزارهای مرورگر MCP حاصل استفاده کند

این مطمئن‌تر از تلاش برای اتصال مستقیم هسته مرورگر Hermes در مرز WSL2/Windows است.

ببینید:

- [Use MCP with Hermes](/docs/guides/use-mcp-with-hermes#wsl2-bridge-hermes-in-wsl-to-windows-chrome)
- [Browser Automation](/docs/user-guide/features/browser#wsl2--windows-chrome-prefer-mcp-over-browser-connect)

### آیا داده‌های من به جایی ارسال می‌شود؟

فراخوان‌های API فقط به ارائه‌دهنده LLM که شما پیکربندی کرده‌اید ارسال می‌شوند (مثلاً OpenRouter، نمونه محلی Ollama شما). Hermes Agent داده‌های telemetry، usage یا analytics جمع‌آوری نمی‌کند. مکالمات، حافظه و مهارت‌های شما به صورت محلی در `~/.hermes/` ذخیره می‌شوند.

### آیا می‌توانم آفلاین / با مدل‌های محلی استفاده کنم؟

بله. `hermes model` را اجرا کنید، `Custom endpoint` را انتخاب کنید و URL سرور خود را وارد کنید:

```
hermes model# Select: Custom endpoint (enter URL manually)# API base URL: http://localhost:11434/v1# API key: ollama# Model name: qwen3.5:27b# Context length: 64000   ← Hermes minimum; set this to match your server's actual context window
```

یا آن را مستقیماً در `config.yaml` پیکربندی کنید:

```
model:  default: qwen3.5:27b  provider: custom  base_url: http://localhost:11434/v1
```

Hermes نقطه پایانی، ارائه‌دهنده و base URL را در `config.yaml` ذخیره می‌کند تا پس از راه‌اندازی مجدد حفظ شود. اگر سرور محلی شما دقیقاً یک مدل بارگذاری کرده باشد، `/model custom` آن را به صورت خودکار تشخیص می‌دهد. همچنین می‌توانید `provider: custom` را در config.yaml تنظیم کنید — این یک ارائه‌دهنده درجه اول است، نه یک نام مستعار.

این با Ollama، vLLM، llama.cpp server، SGLang، LocalAI و سایرین کار می‌کند. برای جزئیات به [Configuration guide](/docs/user-guide/configuration) مراجعه کنید.

اگر `num_ctx` سفارشی در Ollama تنظیم کرده‌اید (مثلاً `ollama run --num_ctx 64000`)، مطمئن شوید طول context مطابق در Hermes تنظیم شده باشد — `/api/show` Ollama حداکثر context مدل را گزارش می‌دهد، نه `num_ctx` مؤثری که شما پیکربندی کرده‌اید.

Hermes نقاط پایانی محلی را به صورت خودکار تشخیص می‌دهد و timeoutهای streaming را کاهش می‌دهد (read timeout از 120s به 1800s افزایش یافته، تشخیص stream ناکارآمد غیرفعال). اگر هنوز در contextهای بسیار بزرگ با timeout مواجه می‌شوید، `HERMES_STREAM_READ_TIMEOUT=1800` را در `.env` خود تنظیم کنید. برای جزئیات به [Local LLM guide](/docs/guides/local-llm-on-mac#timeouts) مراجعه کنید.

### هزینه آن چقدر است؟

Hermes Agent خود رایگان و open-source است (مجوز MIT). شما فقط هزینه استفاده از API LLM از ارائه‌دهنده انتخابی خود را پرداخت می‌کنید. مدل‌های محلی کاملاً رایگان هستند.

### آیا چند نفر می‌توانند از یک نمونه استفاده کنند؟

بله. [messaging gateway](/docs/user-guide/messaging/) به چندین کاربر اجازه می‌دهد با همان نمونه Hermes Agent از طریق Telegram، Discord، Slack، WhatsApp یا Home Assistant تعامل کنند. دسترسی از طریق allowlistها (شناسه‌های کاربری خاص) و جفت‌سازی DM (اولین کاربری که پیام می‌دهد دسترسی را ادعا می‌کند) کنترل می‌شود.

### تفاوت memory و skills چیست؟

- [Memory](/docs/user-guide/features/memory) حقایق را ذخیره می‌کند — چیزهایی که agent درباره شما، پروژه‌های شما و ترجیحات می‌داند. خاطرات بر اساس ارتباط به صورت خودکار بازیابی می‌شوند.
- [Skills](/docs/user-guide/features/skills) رویه‌ها را ذخیره می‌کند — دستورالعمل‌های گام‌به‌گام برای نحوه انجام کارها. مهارت‌ها وقتی agent با یک کار مشابه مواجه می‌شود بازیابی می‌شوند.

هر دو در جلسات پایدار می‌مانند.

### آیا می‌توانم از آن در پروژه Python خود استفاده کنم؟

بله. کلاس `AIAgent` را import کنید و Hermes را به صورت برنامه‌ای استفاده کنید:

```
from run_agent import AIAgentagent = AIAgent(model="anthropic/claude-opus-4.7")response = agent.chat("Explain quantum computing briefly")
```

برای استفاده کامل API به [Python Library guide](/docs/user-guide/features/code-execution) مراجعه کنید.

## عیب‌یابی

### مشکلات نصب

#### پس از نصب `hermes: command not found`

علت: shell شما PATH به‌روز شده را مجدداً بارگذاری نکرده است.

راه‌حل:

```
# Reload your shell profilesource ~/.bashrc    # bashsource ~/.zshrc     # zsh# Or start a new terminal session
```

اگر هنوز کار نمی‌کند، مکان نصب را بررسی کنید:

```
which hermesls ~/.local/bin/hermes
```

installer `~/.local/bin` را به PATH شما اضافه می‌کند. اگر از پیکربندی shell غیراستاندارد استفاده می‌کنید، `export PATH="$HOME/.local/bin:$PATH"` را به صورت دستی اضافه کنید.

#### نسخه Python بسیار قدیمی است

علت: Hermes به Python 3.11 یا جدیدتر نیاز دارد.

راه‌حل:

```
python3 --version   # Check current version# Install a newer Pythonsudo apt install python3.12   # Ubuntu/Debianbrew install python@3.12      # macOS
```

installer این کار را به صورت خودکار انجام می‌دهد — اگر این خطا را در حین نصب دستی می‌بینید، ابتدا Python را ارتقا دهید.

#### دستورات terminal می‌گویند `node: command not found` (یا `nvm`، `pyenv`، `asdf`، ...)

علت: Hermes یک snapshot محیطی هر جلسه را با اجرای `bash -l` یک بار در راه‌اندازی ایجاد می‌کند. یک bash login shell فایل‌های `/etc/profile`، `~/.bash_profile` و `~/.profile` را می‌خواند اما `~/.bashrc` را source نمی‌کند — بنابراین ابزارهایی که خودشان را در آنجا نصب می‌کنند (nvm، asdf، pyenv، cargo، exportهای سفارشی PATH) از snapshot نامرئی می‌مانند. این معمولاً وقتی اتفاق می‌افتد که Hermes تحت systemd یا در یک shell حداقلی اجرا می‌شود که هیچ چیزی profile shell تعاملی را از پیش بارگذاری نکرده است.

راه‌حل: Hermes به صورت پیش‌فرض `~/.bashrc` را به صورت خودکار source می‌کند. اگر این کافی نیست — مثلاً کاربر zsh هستید که PATH شما در `~/.zshrc` است، یا nvm را از یک فایل مستقل init می‌کنید — فایل‌های اضافی را در `~/.hermes/config.yaml` فهرست کنید:

```
terminal:  shell_init_files:    - ~/.zshrc                     # zsh users: pulls zsh-managed PATH into the bash snapshot    - ~/.nvm/nvm.sh                # direct nvm init (works regardless of shell)    - /etc/profile.d/cargo.sh      # system-wide rc files  # When this list is set, the default ~/.bashrc auto-source is NOT added —  # include it explicitly if you want both:  #   - ~/.bashrc  #   - ~/.zshrc
```

فایل‌های گمشده به صورت بی‌صدا رد می‌شوند. Source کردن در bash اتفاق می‌افتد، بنابراین فایل‌هایی که به syntax اختصاصی zsh وابسته هستند ممکن است خطا بدهند — اگر این نگرانی است، فقط بخش تنظیم PATH (مثلاً `nvm.sh` از nvm) را source کنید، نه کل فایل rc.

برای غیرفعال کردن رفتار auto-source (فقط معنای strict login-shell):

```
terminal:  auto_source_bashrc: false
```

#### `uv: command not found`

علت: مدیر بسته `uv` نصب نشده یا در PATH نیست.

راه‌حل:

```
curl -LsSf https://astral.sh/uv/install.sh | shsource ~/.bashrc
```

#### خطاهای Permission denied در حین نصب

علت: مجوزهای ناکافی برای نوشتن در مکان نصب.

راه‌حل:

```
# Don't use sudo with the installer — it installs to ~/.local/bin# If you previously installed with sudo, clean up:sudo rm /usr/local/bin/hermes# Then re-run the standard installercurl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

### مشکلات ارائه‌دهنده و مدل

#### `/model` فقط یک ارائه‌دهنده نشان می‌دهد / نمی‌تواند ارائه‌دهندگان را تغییر دهد

علت: `/model` (داخل یک جلسه chat) فقط بین ارائه‌دهندگانی که قبلاً پیکربندی کرده‌اید جابجا می‌شود. اگر فقط OpenRouter را راه‌اندازی کرده‌اید، فقط همان را `/model` نشان می‌دهد.

راه‌حل: از جلسه خارج شوید و از terminal از `hermes model` برای اضافه کردن ارائه‌دهندگان جدید استفاده کنید:

```
# Exit the Hermes chat session first (Ctrl+C or /quit)# Run the full provider setup wizardhermes model# This lets you: add providers, run OAuth, enter API keys, configure endpoints
```

پس از اضافه کردن ارائه‌دهنده جدید از طریق `hermes model`، یک جلسه chat جدید شروع کنید — `/model` اکنون تمام ارائه‌دهندگان پیکربندی شده شما را نشان می‌دهد.

| می‌خواهید... | استفاده کنید از |
| --- | --- |
| یک ارائه‌دهنده جدید اضافه کنید | `hermes model` (از terminal) |
| API keys را وارد/تغییر دهید | `hermes model` (از terminal) |
| مدل را در حین جلسه تغییر دهید | `/model <name>` (داخل جلسه) |
| به ارائه‌دهنده متفاوت پیکربندی شده تغییر دهید | `/model provider:model` (داخل جلسه) |

#### API key کار نمی‌کند

علت: کلید گمشده، منقضی شده، اشتباه تنظیم شده، یا برای ارائه‌دهنده اشتباه است.

راه‌حل:

```
# Check your configurationhermes config show# Re-configure your providerhermes model# Or set directlyhermes config set OPENROUTER_API_KEY «redacted:sk-…»
```

مطمئن شوید کلید با ارائه‌دهنده مطابقت دارد. یک کلید OpenAI با OpenRouter کار نمی‌کند و بالعکس. `~/.hermes/.env` را برای ورودی‌های متناقض بررسی کنید.

#### مدل در دسترس نیست / مدل یافت نشد

علت: شناسه مدل نادرست یا در ارائه‌دهنده شما در دسترس نیست.

راه‌حل:

```
# List available models for your providerhermes model# Set a valid modelhermes config set HERMES_MODEL anthropic/claude-opus-4.7# Or specify per-sessionhermes chat --model openrouter/meta-llama/llama-3.1-70b-instruct
```

#### محدودیت نرخ (خطاهای 429)

علت: شما از محدودیت نرخ ارائه‌دهنده خود فراتر رفته‌اید.

راه‌حل: لحظه‌ای صبر کنید و دوباره تلاش کنید. برای استفاده مداوم، موارد زیر را در نظر بگیرید:

- ارتقای طرح ارائه‌دهنده خود
- تغییر به مدل یا ارائه‌دهنده متفاوت
- استفاده از `hermes chat --provider <alternative>` برای مسیریابی به backend متفاوت

#### طول context فراتر رفته

علت: مکالمه برای پنجره context مدل بسیار طولانی شده، یا Hermes طول context نادرستی برای مدل شما تشخیص داده است.

راه‌حل:

```
# Compress the current session/compress# Or start a fresh sessionhermes chat# Use a model with a larger context windowhermes chat --model openrouter/google/gemini-3-flash-preview
```

اگر این در اولین مکالمه طولانی اتفاق می‌افتد، Hermes ممکن است طول context نادرستی برای مدل شما داشته باشد. بررسی کنید چه چیزی تشخیص داده:

خط شروع CLI را ببینید — طول context تشخیص داده شده را نشان می‌دهد (مثلاً 📊 Context limit: 128000 tokens). همچنین می‌توانید با `/usage` در حین جلسه بررسی کنید.

برای اصلاح تشخیص context، آن را به صورت صریح تنظیم کنید:

```
# In ~/.hermes/config.yamlmodel:  default: your-model-name  context_length: 131072  # your model's actual context window
```

یا برای نقاط پایانی سفارشی، آن را به ازای هر مدل اضافه کنید:

```
custom_providers:  - name: "My Server"    base_url: "http://localhost:11434/v1"    models:      qwen3.5:27b:        context_length: 64000
```

برای نحوه کار تشخیص خودکار و تمام گزینه‌های override به [Context Length Detection](/docs/integrations/providers#context-length-detection) مراجعه کنید.

### مشکلات Terminal

#### دستور به عنوان خطرناک مسدود شد

علت: Hermes یک دستور بالقوه مخرب تشخیص داده (مثلاً `rm -rf`، `DROP TABLE`). این یک ویژگی ایمنی است.

راه‌حل: وقتی از شما خواسته شد، دستور را بررسی کنید و `y` تایپ کنید تا تأیید شود. همچنین می‌توانید:

- از agent بخواهید از یک جایگزین ایمن‌تر استفاده کند
- لیست کامل الگوهای خطرناک را در [Security docs](/docs/user-guide/security) ببینید

این طراحی شده است — Hermes هرگز دستورات مخرب را به صورت بی‌صدا اجرا نمی‌کند. پرامپت تأیید دقیقاً به شما نشان می‌دهد چه چیزی اجرا خواهد شد.

#### `sudo` از طریق messaging gateway کار نمی‌کند

علت: messaging gateway بدون terminal تعاملی اجرا می‌شود، بنابراین `sudo` نمی‌تواند برای رمز عبور پرامپت کند.

راه‌حل:

- از `sudo` در پیام‌رسانی اجتناب کنید — از agent بخواهید جایگزین‌ها را پیدا کند
- اگر باید از `sudo` استفاده کنید، sudo بدون رمز عبور را برای دستورات خاص در `/etc/sudoers` پیکربندی کنید
- یا برای کارهای مدیریتی به رابط terminal تغییر دهید: `hermes chat`

#### backend Docker متصل نمی‌شود

علت: daemon Docker اجرا نشده یا کاربر مجوز ندارد.

راه‌حل:

```
# Check Docker is runningdocker info# Add your user to the docker groupsudo usermod -aG docker $USERnewgrp docker# Verifydocker run hello-world
```

### مشکلات پیام‌رسانی

#### ربات به پیام‌ها پاسخ نمی‌دهد

علت: ربات اجرا نشده، مجاز نشده، یا کاربر شما در allowlist نیست.

راه‌حل:

```
# Check if the gateway is runninghermes gateway status# Start the gatewayhermes gateway start# Check logs for errorscat ~/.hermes/logs/gateway.log | tail -50
```

#### پیام‌ها تحویل داده نمی‌شوند

علت: مشکلات شبکه، توکن ربات منقضی شده، یا پیکربندی webhook پلتفرم نادرست.

راه‌حل:

- معتبر بودن توکن ربات خود را با `hermes gateway setup` تأیید کنید
- لاگ‌های gateway را بررسی کنید: `cat ~/.hermes/logs/gateway.log | tail -50`
- برای پلتفرم‌های مبتنی بر webhook (Slack، WhatsApp)، مطمئن شوید سرور شما عمومی قابل دسترس است

#### سردرگمی Allowlist — چه کسی می‌تواند با ربات صحبت کند؟

علت: حالت authorization تعیین می‌کند چه کسی دسترسی دارد.

راه‌حل:

| حالت | نحوه کار |
| --- | --- |
| Allowlist | فقط شناسه‌های کاربری فهرست شده در config می‌توانند تعامل کنند |
| DM pairing | اولین کاربری که در DM پیام می‌دهد دسترسی انحصاری را ادعا می‌کند |
| Open | هر کسی می‌تواند تعامل کند (توصیه نشده برای production) |

در `~/.hermes/config.yaml` تحت تنظیمات gateway خود پیکربندی کنید. به [Messaging docs](/docs/user-guide/messaging/) مراجعه کنید.

#### Gateway شروع نمی‌شود

علت: وابستگی‌های گمشده، تداخل پورت، یا توکن‌های نادرست پیکربندی شده.

راه‌حل:

```
# Install core messaging gateway dependenciescd ~/.hermes/hermes-agent && uv pip install -e ".[messaging]"  # Telegram, Discord, Slack, and shared gateway deps# Check for port conflictslsof -i :8080# Verify configurationhermes config show
```

#### WSL: Gateway مدام قطع می‌شود یا `hermes gateway start` ناموفق است

علت: پشتیبانی systemd در WSL غیرقابل اعتماد است. بسیاری از نصب‌های WSL2 systemd فعال ندارند و حتی وقتی فعال باشد، سرویس‌ها ممکن است پس از راه‌اندازی مجدد WSL یا خاموش شدن بیکار Windows باقی نمانند.

راه‌حل: به جای سرویس systemd از حالت foreground استفاده کنید:

```
# Option 1: Direct foreground (simplest)hermes gateway run# Option 2: Persistent via tmux (survives terminal close)tmux new -s hermes 'hermes gateway run'# Reattach later: tmux attach -t hermes# Option 3: Background via nohupnohup hermes gateway run > ~/.hermes/logs/gateway.log 2>&1 &
```

اگر می‌خواهید با systemd امتحان کنید، مطمئن شوید فعال است:

1. `/etc/wsl.conf` را باز کنید (اگر وجود ندارد ایجاد کنید)
2. اضافه کنید:
```
[boot]
systemd=true
```
3. از PowerShell: `wsl --shutdown`
4. ترمینال WSL خود را مجدداً باز کنید
5. تأیید کنید: `systemctl is-system-running` باید "running" یا "degraded" بگوید

برای راه‌اندازی خودکار قابل اعتماد، از Windows Task Scheduler برای راه‌اندازی WSL + gateway در ورود استفاده کنید:

1. یک تسک ایجاد کنید که `wsl -d Ubuntu -- bash -lc 'hermes gateway run'` را اجرا کند
2. آن را روی ورود کاربر تنظیم کنید

#### macOS: Node.js / ffmpeg / سایر ابزارها توسط gateway یافت نمی‌شوند

علت: سرویس‌های launchd یک PATH حداقلی (`/usr/bin:/bin:/usr/sbin:/sbin`) به ارث می‌برند که شامل Homebrew، nvm، cargo یا سایر ابزارهای نصب شده توسط کاربر نیست. این معمولاً WhatsApp bridge (node یافت نشد) یا transcription صوتی (ffmpeg یافت نشد) را خراب می‌کند.

راه‌حل: gateway در حین اجرای `hermes gateway install` PATH shell شما را ضبط می‌کند. اگر ابزارها را پس از راه‌اندازی gateway نصب کرده‌اید، نصب را مجدداً اجرا کنید تا PATH به‌روز شده ضبط شود:

```
hermes gateway install    # Re-snapshots your current PATHhermes gateway start      # Detects the updated plist and reloads
```

می‌توانید تأیید کنید plist PATH صحیح را دارد:

```
/usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:PATH" ~/Library/LaunchAgents/ai.hermes.gateway.plist
```

### مشکلات عملکرد

#### پاسخ‌های کند

علت: مدل بزرگ، سرور API دور، یا system prompt سنگین با ابزارهای زیاد.

راه‌حل:

- یک مدل سریع‌تر/کوچکتر امتحان کنید: `hermes chat --model openrouter/meta-llama/llama-3.1-8b-instruct`
- مجموعه ابزارهای فعال را کاهش دهید: `hermes chat -t "terminal"`
- تأخیر شبکه خود به ارائه‌دهنده را بررسی کنید
- برای مدل‌های محلی، مطمئن شوید VRAM GPU کافی دارید

#### استفاده بالا از token

علت: مکالمات طولانی، system promptهای verbose یا فراخوان‌های زیاد ابزار که context را تجمع می‌کنند.

راه‌حل:

```
# Compress the conversation to reduce tokens/compress# Check session token usage/usage
```

از `/compress` به طور منظم در جلسات طولانی استفاده کنید. این تاریخچه مکالمه را خلاصه می‌کند و استفاده از token را به طور قابل توجهی کاهش می‌دهد در حالی که context را حفظ می‌کند.

#### جلسه بیش از حد طولانی می‌شود

علت: مکالمات طولانی پیام‌ها و خروجی‌های ابزار را تجمع می‌کنند و به محدودیت‌های context نزدیک می‌شوند.

راه‌حل:

```
# Compress current session (preserves key context)/compress# Start a new session with a reference to the old onehermes chat# Resume a specific session later if neededhermes chat --continue
```

### مشکلات MCP

#### سرور MCP متصل نمی‌شود

علت: باینری سرور یافت نشد، مسیر دستور نادرست، یا runtime گمشده.

راه‌حل:

```
# Ensure MCP dependencies are installed (already included in standard install)cd ~/.hermes/hermes-agent && uv pip install -e ".[mcp]"# For npm-based servers, ensure Node.js is availablenode --versionnpx --version# Test the server manuallynpx -y @modelcontextprotocol/server-filesystem /tmp
```

پیکربندی MCP `~/.hermes/config.yaml` خود را تأیید کنید:

```
mcp_servers:  filesystem:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/docs"]
```

#### ابزارها از سرور MCP ظاهر نمی‌شوند

علت: سرور شروع شد اما کشف ابزار ناموفق بود، ابزارها توسط config فیلتر شدند، یا سرور از قابلیت MCP که انتظار داشتید پشتیبانی نمی‌کند.

راه‌حل:

- لاگ‌های gateway/agent را برای خطاهای اتصال MCP بررسی کنید
- مطمئن شوید سرور به متد RPC `tools/list` پاسخ می‌دهد
- هر تنظیم `tools.include`، `tools.exclude`، `tools.resources`، `tools.prompts` یا `enabled` زیر آن سرور را بررسی کنید
- به یاد داشته باشید ابزارهای کمکی resource/prompt فقط وقتی ثبت می‌شوند که جلسه واقعاً از آن قابلیت‌ها پشتیبانی کند
- پس از تغییر config از `/reload-mcp` استفاده کنید

```
# Verify MCP servers are configuredhermes config show | grep -A 12 mcp_servers# Restart Hermes or reload MCP after config changeshermes chat
```

همچنین ببینید:

- [MCP (Model Context Protocol)](/docs/user-guide/features/mcp)
- [Use MCP with Hermes](/docs/guides/use-mcp-with-hermes)
- [MCP Config Reference](/docs/reference/mcp-config-reference)

#### خطاهای timeout MCP

علت: سرور MCP برای پاسخ بیش از حد طولانی است، یا در حین اجرا خراب شده است.

راه‌حل:

- در صورت پشتیبانی، timeout را در پیکربندی سرور MCP خود افزایش دهید
- بررسی کنید آیا فرآیند سرور MCP هنوز در حال اجراست
- برای سرورهای HTTP MCP از راه دور، اتصال شبکه را بررسی کنید

اگر یک سرور MCP در حین درخواست خراب شود، Hermes timeout گزارش می‌دهد. لاگ‌های خود سرور (نه فقط لاگ‌های Hermes) را بررسی کنید تا علت اصلی را تشخیص دهید.

## Profileها

### profileها چگونه با تنظیم `HERMES_HOME` متفاوت هستند؟

Profileها یک لایه مدیریت شده روی `HERMES_HOME` هستند. شما می‌توانستید `HERMES_HOME=/some/path` را قبل از هر دستور به صورت دستی تنظیم کنید، اما profileها تمام لوله‌کشی را برای شما انجام می‌دهند: ایجاد ساختار دایرکتوری، تولید aliases shell (hermes-work)، ردیابی profile فعال در `~/.hermes/active_profile` و همگام‌سازی به‌روزرسانی‌های مهارت در تمام profileها به صورت خودکار. آنها همچنین با تکمیل tab ادغام می‌شوند تا مجبور نباشید مسیرها را به خاطر بسپارید.

### آیا دو profile می‌توانند توکن ربات مشترکی داشته باشند؟

خیر. هر پلتفرم پیام‌رسانی (Telegram، Discord و غیره) به دسترسی انحصاری به توکن ربات نیاز دارد. اگر دو profile تلاش کنند همزمان از توکن مشترک استفاده کنند، gateway دوم نمی‌تواند متصل شود. یک ربات جداگانه برای هر profile ایجاد کنید — برای Telegram، با [@BotFather](https://t.me/BotFather) صحبت کنید تا ربات‌های اضافی بسازید.

### آیا profileها حافظه یا sessionها را به اشتراک می‌گذارند؟

خیر. هر profile فروشگاه حافظه، پایگاه داده session و دایرکتوری مهارت خود را دارد. آنها کاملاً ایزوله هستند. اگر می‌خواهید یک profile جدید با خاطرات و sessionهای موجود شروع کنید، از `hermes profile create newname --clone-all` برای کپی کردن همه چیز از profile فعلی استفاده کنید، یا `--clone-from <profile>` را برای کپی از یک profile منبع خاص اضافه کنید.

### وقتی `hermes update` اجرا می‌کنم چه اتفاقی می‌افتد؟

`hermes update` آخرین کد را دریافت می‌کند و وابستگی‌ها را یک بار (نه به ازای هر profile) نصب مجدداً می‌کند. سپس مهارت‌های به‌روز شده را به طور خودکار به تمام profileها همگام‌سازی می‌کند. فقط یک بار نیاز به اجرای `hermes update` دارید — تمام profileهای ماشین را پوشش می‌دهد.

### چند profile می‌توانم اجرا کنم؟

هیچ محدودیت سختی وجود ندارد. هر profile فقط یک دایرکتوری زیر `~/.hermes/profiles/` است. محدودیت عملی به فضای دیسک و تعداد gatewayهای همزمانی بستگی دارد که سیستم شما می‌تواند مدیریت کند (هر gateway یک فرآیند Python سبک است). اجرای ده‌ها profile مشکلی ندارد؛ هر profile بیکار از منابع استفاده نمی‌کند.

## گردش کار و الگوها

### استفاده از مدل‌های مختلف برای کارهای مختلف (گردش کار multi-model)

سناریو: شما از GPT-5.4 به عنوان راننده روزانه استفاده می‌کنید، اما Gemini یا Grok محتوای بهتری برای رسانه‌های اجتماعی می‌نویسد. تغییر دستی مدل هر بار خسته‌کننده است.

راه‌حل: پیکربندی delegation. Hermes می‌تواند subagentها را به طور خودکار به مدل متفاوتی مسیریابی کند. این را در `~/.hermes/config.yaml` تنظیم کنید:

```
delegation:  model: "google/gemini-3-flash-preview"   # subagents use this model  provider: "openrouter"                    # provider for subagents
```

حالا وقتی به Hermes می‌گویید "یک thread درباره X برای من بنویس" و یک subagent `delegate_task` ایجاد می‌کند، آن subagent به جای مدل اصلی شما روی Gemini اجرا می‌شود. مکالمه اصلی شما روی GPT-5.4 باقی می‌ماند.

همچنین می‌توانید صریحاً در پرامپت خود بگویید: "یک کار برای نوشتن پست‌های رسانه اجتماعی درباره محصول ما واگذار کن. از subagent خود برای نوشتن واقعی استفاده کن." agent از `delegate_task` استفاده می‌کند که به طور خودکار پیکربندی delegation را دریافت می‌کند.

برای تغییر مدل یک‌باره بدون delegation، از `/model` در CLI استفاده کنید:

```
/model google/gemini-3-flash-preview    # switch for this session# ... write your content .../model openai/gpt-5.4                   # switch back
```

هر تغییر `/model` cache پرامپت را ریست می‌کند — کلید cache شامل مدل است، بنابراین اولین پیام پس از هر تغییر کل مکالمه را با قیمت کامل input دوباره می‌خواند. در جلسات طولانی، delegation (subagentها context تازه خود را دارند) یا session جدید را بر تغییر مکرر عقب و جلو ترجیح دهید.

برای جزئیات بیشتر درباره نحوه کار delegation به [Subagent Delegation](/docs/user-guide/features/delegation) مراجعه کنید.

### اجرای چند agent روی یک شماره WhatsApp (جفت‌سازی per-chat)

سناریو: در OpenClaw، شما چندین agent مستقل به چت‌های خاص WhatsApp متصل داشتید — یکی برای گروه لیست خرید خانواده، دیگری برای چت خصوصی شما. آیا Hermes می‌تواند این کار را انجام دهد؟

محدودیت فعلی: هر profile Hermes به شماره/session WhatsApp خود نیاز دارد. نمی‌توانید چندین profile را به چت‌های مختلف روی همان شماره WhatsApp متصل کنید — WhatsApp bridge (Baileys) از یک session احراز هویت شده به ازای هر شماره استفاده می‌کند.

راه‌حل‌ها:

1. **از یک profile با جابجایی شخصیت استفاده کنید.** فایل‌های متنی `AGENTS.md` متفاوت ایجاد کنید یا از دستور `/personality` برای تغییر رفتار به ازای هر chat استفاده کنید. agent می‌بیند در کدام chat است و می‌تواند تطبیق یابد.
2. **از cron jobs برای کارهای تخصصی استفاده کنید.** برای ردیاب لیست خرید، یک cron job راه‌اندازی کنید که یک chat خاص را نظارت کند و لیست را مدیریت کند — نیازی به agent جداگانه نیست.
3. **از شماره‌های جداگانه استفاده کنید.** اگر به agentهای واقعاً مستقل نیاز دارید، هر profile را با شماره WhatsApp خودش جفت کنید. شماره‌های مجازی از سرویس‌هایی مانند Google Voice برای این کار کار می‌کنند.
4. **به جای آن از Telegram یا Discord استفاده کنید.** این پلتفرم‌ها جفت‌سازی per-chat را طبیعی‌تر پشتیبانی می‌کنند — هر گروه Telegram یا کانال Discord session خودش را دارد و می‌توانید چندین توکن ربات (یکی به ازای هر profile) روی یک حساب اجرا کنید.

برای جزئیات بیشتر به [Profiles](/docs/user-guide/profiles) و [WhatsApp setup](/docs/user-guide/messaging/whatsapp) مراجعه کنید.

### کنترل نمایش در Telegram (مخفی کردن لاگ‌ها و استدلال)

سناریو: شما به جای فقط خروجی نهایی، لاگ‌های gateway exec، استدلال Hermes و جزئیات فراخوان ابزار را در Telegram می‌بینید.

راه‌حل: تنظیم `display.tool_progress` در `config.yaml` میزان نمایش فعالیت ابزار را کنترل می‌کند:

```
display:  tool_progress: "off"   # options: off, new, all, verbose
```

- `off` — فقط پاسخ نهایی. بدون فراخوان ابزار، بدون استدلال، بدون لاگ.
- `new` — فراخوان‌های جدید ابزار را هنگام وقوع نشان می‌دهد (یک خط کوتاه).
- `all` — تمام فعالیت ابزار شامل نتایج را نشان می‌دهد.
- `verbose` — جزئیات کامل شامل آرگومان‌ها و خروجی‌های ابزار.

برای پلتفرم‌های پیام‌رسانی، معمولاً `off` یا `new` همان چیزی است که می‌خواهید. پس از ویرایش `config.yaml`، gateway را برای اعمال تغییرات راه‌اندازی مجدد کنید.

همچنین می‌توانید این را به ازای جلسه با دستور `/verbose` تغییر دهید (اگر فعال باشد):

```
display:  tool_progress_command: true   # enables /verbose in the gateway
```

### مدیریت مهارت‌ها در Telegram (محدودیت دستور slash)

سناریو: Telegram محدودیت ۱۰۰ دستور slash دارد و مهارت‌های شما از آن فراتر رفته‌اند. می‌خواهید مهارت‌هایی که در Telegram نیاز ندارید را غیرفعال کنید، اما تنظیمات `hermes skills config` به نظر می‌رسد اثر نمی‌گذارد.

راه‌حل: از `hermes skills config` برای غیرفعال کردن مهارت‌ها به ازای هر پلتفرم استفاده کنید. این در `config.yaml` می‌نویسد:

```
skills:  disabled: []                    # globally disabled skills  platform_disabled:    telegram: [skill-a, skill-b]  # disabled only on telegram
```

پس از تغییر این، gateway را راه‌اندازی مجدد کنید (`hermes gateway restart` یا kill و relaunch). منوی دستور ربات Telegram در راه‌اندازی مجدد ساخته می‌شود.

مهارت‌هایی با توصیف‌های بسیار طولانی در منوی Telegram به ۴۰ کاراکتر بریده می‌شوند تا در محدودیت اندازه payload باقی بمانند. اگر مهارت‌ها ظاهر نمی‌شوند، ممکن است مشکل اندازه کل payload باشد نه محدودیت تعداد ۱۰۰ دستور — غیرفعال کردن مهارت‌های استفاده نشده به هر دو کمک می‌کند.

### Sessionهای thread مشترک (چند کاربر، یک مکالمه)

سناریو: شما یک thread Telegram یا Discord دارید که چندین نفر ربات را mention می‌کنند. می‌خواهید تمام mentionها در آن thread بخشی از یک مکالمه مشترک باشند، نه sessionهای جداگانه به ازای هر کاربر.

رفتار فعلی: Hermes sessionها را با کلید شناسه کاربر در اکثر پلتفرم‌ها ایجاد می‌کند، بنابراین هر نفر context مکالمه خود را دارد. این برای حریم خصوصی و ایزوله کردن context طراحی شده است.

راه‌حل‌ها:

1. **از Slack استفاده کنید.** sessionهای Slack با thread کلیدگذاری می‌شوند، نه با کاربر. چندین کاربر در یک thread یک مکالمه مشترک دارند — دقیقاً همان رفتاری که توصیف می‌کنید. این طبیعی‌ترین تناسب است.
2. **از یک چت گروهی با یک کاربر استفاده کنید.** اگر یک نفر "اپراتور" تعیین شده باشد که سؤالات را منتقل کند، session یکپارچه می‌ماند. سایرین می‌توانند بخوانند.
3. **از یک کانال Discord استفاده کنید.** sessionهای Discord با کانال کلیدگذاری می‌شوند، بنابراین تمام کاربران در یک کانال context مشترک دارند. از یک کانال اختصاصی برای مکالمه مشترک استفاده کنید.

### صادرات Hermes به یک ماشین دیگر

سناریو: شما مهارت‌ها، cron jobs و خاطرات را روی یک ماشین ساخته‌اید و می‌خواهید همه چیز را به یک باکس Linux اختصاصی جدید منتقل کنید.

راه‌حل:

1. Hermes Agent را روی ماشین جدید نصب کنید:
```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

2. در ماشین **منبع**، یک backup کامل ایجاد کنید:
```
hermes backup
```
این یک zip از کل دایرکتوری `~/.hermes/` شما ایجاد می‌کند — config، API keys، خاطرات، مهارت‌ها، sessionها و profileها — که در دایرکتوری خانه شما به عنوان `~/hermes-backup-<timestamp>.zip` ذخیره می‌شود.

3. فایل zip را به ماشین جدید کپی کنید و وارد کنید:
```
# On the source machinescp ~/hermes-backup-<timestamp>.zip newmachine:~/# On the new machinehermes import ~/hermes-backup-<timestamp>.zip
```

4. در ماشین جدید، `hermes setup` را اجرا کنید تا API keys و پیکربندی ارائه‌دهنده کار کنند.

### انتقال یک profile به ماشین دیگر

سناریو: می‌خواهید یک profile خاص را منتقل یا به اشتراک بگذارید — نه نصب کامل خود.

```
# On the source machinehermes profile export work ./work-backup.tar.gz# Copy the file to the target machine, then:hermes profile import ./work-backup.tar.gz work
```

profile وارد شده تمام config، خاطرات، sessionها و مهارت‌های export را خواهد داشت. ممکن است مسیرها را به‌روز کنید یا مجدد با ارائه‌دهندگان احراز هویت کنید اگر ماشین جدید تنظیم متفاوتی دارد.

### `hermes backup` در مقابل `hermes profile export`

| ویژگی | `hermes backup` | `hermes profile export` |
| --- | --- | --- |
| مورد استفاده | مهاجت کامل ماشین | انتقال/اشتراک یک profile خاص |
| محدوده | سراسری (کل دایرکتوری `~/.hermes`) | محلی (دایرکتوری یک profile) |
| شامل می‌شود | تمام profileها، config سراسری، API keys، sessionها | یک profile: SOUL.md، خاطرات، sessionها، مهارت‌ها |
| اعتبارنامه‌ها | شامل شده (`.env` و `auth.json`) | حذف شده (برای اشتراک ایمن) |
| فرمت | .zip | .tar.gz |

fallback دستی (rsync): اگر ترجیح می‌دهید فایل‌ها را مستقیماً کپی کنید، کد repository را مستثنی کنید:

```
rsync -av --exclude='hermes-agent' ~/.hermes/ newmachine:~/.hermes/
```

`hermes backup` حتی در حین اجرای فعال Hermes یک snapshot سازگار تولید می‌کند. آرشیو بازیابی شده فایل‌های runtime محلی ماشین مانند `gateway.pid` و `cron.pid` را حذف می‌کند.

### Permission denied پس از نصب هنگام بارگذاری مجدد shell

سناریو: پس از اجرای installer Hermes، `source ~/.zshrc` خطای permission denied می‌دهد.

علت: این معمولاً وقتی اتفاق می‌افتد که `~/.zshrc` (یا `~/.bashrc`) مجوزهای فایل نادرستی دارد، یا installer نتوانسته به طور تمیز در آن بنویسد. این مشکل اختصاصی Hermes نیست — مشکل مجوزهای پیکربندی shell است.

راه‌حل:

```
# Check permissionsls -la ~/.zshrc# Fix if needed (should be -rw-r--r-- or 644)chmod 644 ~/.zshrc# Then reloadsource ~/.zshrc# Or just open a new terminal window — it picks up PATH changes automatically
```

اگر installer خط PATH را اضافه کرده اما مجوزها نادرست هستند، می‌توانید آن را به صورت دستی اضافه کنید:

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

### خطای 400 در اولین اجرای agent

سناریو: نصب خوب انجام می‌شود، اما اولین تلاش chat با HTTP 400 ناموفق است.

علت: معمولاً عدم تطابق نام مدل — مدل پیکربندی شده در ارائه‌دهنده شما وجود ندارد، یا API key به آن دسترسی ندارد.

راه‌حل:

```
# Check what model and provider are configuredhermes config show | head -20# Re-run model selectionhermes model# Or test with a known-good modelhermes chat -q "hello" --model anthropic/claude-opus-4.7
```

اگر از OpenRouter استفاده می‌کنید، مطمئن شوید API key شما اعتبار دارد. خطای 400 از OpenRouter اغلب به این معنی است که مدل به طرح پولی نیاز دارد یا شناسه مدل املای اشتباه دارد.

## هنوز گیر کرده‌اید؟

اگر مشکل شما اینجا پوشش داده نشده:

1. issues موجود را جستجو کنید: [GitHub Issues](https://github.com/NousResearch/hermes-agent/issues)
2. از جامعه بپرسید: [Nous Research Discord](https://discord.gg/nousresearch)
3. یک گزارش باگ ثبت کنید: OS، نسخه Python (`python3 --version`)، نسخه Hermes (`hermes --version`) و پیام خطای کامل را درج کنید
