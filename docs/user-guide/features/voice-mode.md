---
layout: docs
title: "حالت صوتی"
permalink: /docs/user-guide/features/voice-mode/
---

- 
- ویژگی‌ها
- رسانه و وب
- حالت صوتی

# حالت صوتی

Hermes Agent از تعامل کامل صوتی در CLI و پلتفرم‌های پیام‌رسانی پشتیبانی می‌کند. با عامل با میکروفون خود صحبت کنید، پاسخ‌های گفتاری بشنوید و مکالمات صوتی زنده در کانال‌های صوتی Discord داشته باشید.

اگر راهنمای عملی راه‌اندازی با پیکربندی‌های توصیه شده و الگوهای استفاده واقعی می‌خواهید، [Use Voice Mode with Hermes](/docs/guides/use-voice-mode-with-hermes) را ببینید.

## پیش‌نیازها

قبل از استفاده از ویژگی‌های صوتی، مطمئن شوید:

1. Hermes Agent نصب شده — از طریق اسکریپت نصب (به Installation مراجعه کنید)
2. یک ارائه‌دهنده LLM پیکربندی شده — hermes model را اجرا کنید یا اعتبارنامه ارائه‌دهنده ترجیحی خود را در ~/.hermes/.env تنظیم کنید
3. یک تنظیم پایه کاری — hermes را اجرا کنید تا مطمئن شوید عامل به متن پاسخ می‌دهد قبل از فعال کردن صدا

[Installation](/docs/getting-started/installation)
`hermes model`
`~/.hermes/.env`
`hermes`

پوشه ~/.hermes/ و config.yaml پیش‌فرض در اولین اجرای hermes به طور خودکار ایجاد می‌شوند. فقط برای کلیدهای API باید ~/.hermes/.env را به صورت دستی ایجاد کنید.

`~/.hermes/`
`config.yaml`
`hermes`
`~/.hermes/.env`

یک اشتراک [Nous Portal](/docs/user-guide/features/tool-gateway) پولی LLM (مرحله 2) و OpenAI TTS از طریق Tool Gateway را فراهم می‌کند — نیازی به کلید جداگانه OpenAI نیست. در یک نصب تازه، hermes setup --portal هر دو را به یکباره سیم‌بندی می‌کند.

`hermes setup --portal`

## نمای کلی

| ویژگی | پلتفرم | توضیح |
| --- | --- | --- |
| صدای تعاملی | CLI | کلید Ctrl+B را فشار دهید تا ضبط کنید، عامل سکوت را به طور خودکار تشخیص داده و پاسخ می‌دهد |
| پاسخ صوتی خودکار | Telegram, Discord | عامل پاسخ صوتی در کنار پاسخ‌های متنی ارسال می‌کند |
| کانال صوتی | Discord | ربات به VC می‌پیوندد، به کاربران صحبت کننده گوش می‌دهد و پاسخ‌ها را بازگو می‌کند |

## الزامات

### بسته‌های پایتون

```
# حالت صوتی CLI (میکروفون + پخش صدا)cd ~/.hermes/hermes-agent && uv pip install -e ".[voice]"# پیام‌رسانی Discord + Telegram (شامل discord.py[voice] برای پشتیبانی VC)cd ~/.hermes/hermes-agent && uv pip install -e ".[messaging]"# TTS پریمیوم (ElevenLabs)cd ~/.hermes/hermes-agent && uv pip install -e ".[tts-premium]"# TTS محلی (NeuTTS، اختیاری)python -m pip install -U neutts[all]# همه یکجاcd ~/.hermes/hermes-agent && uv pip install -e ".[all]"
```

| اضافی | بسته‌ها | نیاز برای |
| --- | --- | --- |
| voice | sounddevice,numpy | حالت صوتی CLI |
| messaging | discord.py[voice],python-telegram-bot,aiohttp | ربات‌های Discord & Telegram |
| tts-premium | elevenlabs | ارائه‌دهنده TTS ElevenLabs |

`voice`
`sounddevice`
`numpy`
`messaging`
`discord.py[voice]`
`python-telegram-bot`
`aiohttp`
`tts-premium`
`elevenlabs`

ارائه‌دهنده TTS محلی اختیاری: neutts را جداگانه با python -m pip install -U neutts[all] نصب کنید. در اولین استفاده مدل را به طور خودکار دانلود می‌کند.

`neutts`
`python -m pip install -U neutts[all]`

discord.py[voice] به طور خودکار PyNaCl (برای رمزگذاری صدا) و opus bindings را نصب می‌کند. این برای پشتیبانی کانال صوتی Discord لازم است.

`discord.py[voice]`

### وابستگی‌های سیستم

```
# macOSbrew install portaudio ffmpeg opusbrew install espeak-ng   # برای NeuTTS# Ubuntu/Debiansudo apt install portaudio19-dev ffmpeg libopus0sudo apt install espeak-ng   # برای NeuTTS
```

| وابستگی | هدف | نیاز برای |
| --- | --- | --- |
| PortAudio | ورودی میکروفون و پخش صدا | حالت صوتی CLI |
| ffmpeg | تبدیل قالب صدا (MP3 → Opus، PCM → WAV) | همه پلتفرم‌ها |
| Opus | کدک صوتی Discord | کانال‌های صوتی Discord |
| espeak-ng | پشتیبان phonemizer | ارائه‌دهنده محلی NeuTTS |

### کلیدهای API

به ~/.hermes/.env اضافه کنید:

`~/.hermes/.env`

```
# گفتار به متن — ارائه‌دهنده محلی نیازی به کلید ندارد# pip install faster-whisper          # رایگان، محلی اجرا می‌شود، توصیه شدهGROQ_API_KEY=your-key                 # Groq Whisper — سریع، سطح رایگان (ابرهای)VOICE_TOOLS_OPENAI_KEY=your-key       # OpenAI Whisper — پولی (ابرهای)# متن به گفتار (اختیاری — Edge TTS و NeuTTS بدون هیچ کلیدی کار می‌کنند)ELEVENLABS_API_KEY=***           # ElevenLabs — کیفیت پریمیوم# VOICE_TOOLS_OPENAI_KEY بالا همچنین OpenAI TTS را فعال می‌کند
```

اگر faster-whisper نصب باشد، حالت صوتی بدون هیچ کلید API برای STT کار می‌کند. مدل (~150 مگابایت برای base) در اولین استفاده به طور خودکار دانلود می‌شود.

`faster-whisper`
`base`

## حالت صوتی CLI

حالت صوتی در [CLI کلاسیک](/docs/reference/cli-commands) (hermes chat) و [TUI](/docs/reference/cli-commands) (hermes --tui) در دسترس است. رفتار در هر دو یکسان است — دستورات اسلش یکسان، تشخیص سکوت VAD یکسان، TTS جریانی یکسان، فیلتر توهم یکسان. TUI علاوه بر این گزارش‌های اشکال‌زدایی crash را به ~/.hermes/logs/ ارسال می‌کند تا خرابی‌های push-to-talk در backendهای صوتی غیرمعمول با stack trace کامل قابل گزارش باشند.

`hermes chat`
`hermes --tui`
`~/.hermes/logs/`

### شروع سریع

CLI را شروع کنید و حالت صوتی را فعال کنید:

```
hermes                # شروع CLI تعاملی
```

سپس از این دستورات در CLI استفاده کنید:

```
/voice          حالت صوتی را روشن/خاموش کنید/voice on       حالت صوتی را فعال کنید/voice off      حالت صوتی را غیرفعال کنید/voice tts      خروجی TTS را روشن/خاموش کنید/voice status   وضعیت فعلی را نشان دهید
```

### نحوه کار

1. CLI را با hermes شروع کنید و حالت صوتی را با /voice on فعال کنید
2. کلید Ctrl+B را فشار دهید — بیپی پخش می‌شود (880Hz)، ضبط شروع می‌شود
3. صحبت کنید — یک نوار سطح صدای زنده ورودی شما را نشان می‌دهد:● [▁▂▃▅▇▇▅▂] ❯
4. صحبت کردن را متوقف کنید — پس از 3 ثانیه سکوت، ضبط به طور خودکار متوقف می‌شود
5. دو بیپ پخش می‌شود (660Hz) که پایان ضبط را تأیید می‌کند
6. صدا از طریق Whisper رونویسی شده و به عامل ارسال می‌شود
7. اگر TTS فعال باشد، پاسخ عامل با صدا بازگو می‌شود
8. ضبط به طور خودکار مجدداً شروع می‌شود — بدون فشار دادن هیچ کلیدی دوباره صحبت کنید

`hermes`
`/voice on`
`● [▁▂▃▅▇▇▅▂] ❯`

این حلقه تا زمانی ادامه می‌یابد که Ctrl+B را در حین ضبط فشار دهید (از حالت مداوم خارج شوید) یا 3 ضبط متوالی هیچ گفتاری تشخیص ندهند.

کلید ضبط از طریق voice.record_key در ~/.hermes/config.yaml قابل پیکربندی است (پیش‌فرض: ctrl+b).

`voice.record_key`
`~/.hermes/config.yaml`
`ctrl+b`

### تشخیص سکوت

الگوریتم دو مرحله‌ای تشخیص می‌دهد چه زمانی صحبت کردن را متوقف کرده‌اید:

1. تأیید گفتار — منتظر صدای بالای آستانه RMS (200) حداقل 0.3 ثانیه می‌ماند، کوتاهی بین هجاها را تحمل می‌کند
2. تشخیص پایان — وقتی گفتار تأیید شد، پس از 3.0 ثانیه سکوت متوالی فعال می‌شود

اگر اصلاً گفتاری تشخیص داده نشود، ضبط بعد از 15 ثانیه به طور خودکار متوقف می‌شود.

هر دو silence_threshold و silence_duration در config.yaml قابل پیکربندی هستند. همچنین می‌توانید بیپ‌های شروع/پایان ضبط را با voice.beep_enabled: false غیرفعال کنید.

`silence_threshold`
`silence_duration`
`config.yaml`
`voice.beep_enabled: false`

### TTS جریانی

وقتی TTS فعال باشد، عامل پاسخ خود را جمله به جمله در حین تولید متن بازگو می‌کند — منتظر پاسخ کامل نمی‌مانید:

1. دلتاهای متن را در جملات کامل بافر می‌کند (حداقل 20 کاراکتر)
2. قالب‌بندی markdown و بلوک‌های <think> را حذف می‌کند
3. برای هر جمله به صورت بلادرنگ صدا تولید و پخش می‌کند

`<think>`

### فیلتر توهم

Whisper گاهی متن توهمی از سکوت یا نویز پس‌زمینه تولید می‌کند ("Thank you for watching"، "Subscribe" و غیره). عامل اینها را با مجموعه‌ای از 26 عبارت توهم شناخته شده در چندین زبان به علاوه یک الگوی regex که تغییرات تکراری را می‌گیرد فیلتر می‌کند.

## پاسخ صوتی گیت‌وی (Telegram & Discord)

اگر هنوز ربات‌های پیام‌رسانی خود را راه‌اندازی نکرده‌اید، راهنماهای خاص پلتفرم را ببینید:

[Telegram Setup Guide](/docs/user-guide/messaging/telegram)
[Discord Setup Guide](/docs/user-guide/messaging/discord)

گیت‌وی را برای اتصال به پلتفرم‌های پیام‌رسانی خود شروع کنید:

```
hermes gateway        # شروع گیت‌وی (به پلتفرم‌های پیکربندی شده متصل می‌شود)hermes gateway setup  # جادوگر راه‌اندازی تعاملی برای پیکربندی اولیه
```

### Discord: کانال‌ها در مقابل DMها

ربات دو حالت تعاملی در Discord پشتیبانی می‌کند:

| حالت | نحوه صحبت کردن | نیاز به اشاره | راه‌اندازی |
| --- | --- | --- | --- |
| پیام مستقیم (DM) | پروفایل ربات → "Message" را باز کنید | خیر | بلافاصله کار می‌کند |
| کانال سرور | در یک کانال متنی که ربات در آن حضور دارد تایپ کنید | بله (@botname) | ربات باید به سرور دعوت شود |

`@botname`

DM (توصیه شده برای استفاده شخصی): فقط یک DM با ربات باز کنید و تایپ کنید — نیازی به @mention نیست. پاسخ‌های صوتی و همه دستورات دقیقاً مانند کانال‌ها کار می‌کنند.

کانال‌های سرور: ربات فقط وقتی به آن اشاره کنید (مثلاً @hermesbyt4 hello) پاسخ می‌دهد. مطمئن شوید که کاربر bot را از پاپ‌آپ mention انتخاب می‌کنید، نه نقشی با همان نام.

`@hermesbyt4 hello`

برای غیرفعال کردن الزام اشاره در کانال‌های سرور، به ~/.hermes/.env اضافه کنید:

`~/.hermes/.env`

```
DISCORD_REQUIRE_MENTION=false
```

یا کانال‌های خاصی را به عنوان پاسخ آزاد (بدون نیاز به اشاره) تنظیم کنید:

```
DISCORD_FREE_RESPONSE_CHANNELS=123456789,987654321
```

### دستورات

اینها در هر دو Telegram و Discord (DMs و کانال‌های متنی) کار می‌کنند:

```
/voice          حالت صوتی را روشن/خاموش کنید/voice on       فقط وقتی پیام صوتی ارسال می‌کنید پاسخ صوتی دهید/voice tts      پاسخ صوتی به همه پیام‌ها/voice off      پاسخ‌های صوتی را غیرفعال کنید/voice status   تنظیم فعلی را نشان دهید
```

### حالت‌ها

| حالت | دستور | رفتار |
| --- | --- | --- |
| off | /voice off | فقط متن (پیش‌فرض) |
| voice_only | /voice on | فقط وقتی پیام صوتی ارسال می‌کنید پاسخ می‌دهد |
| all | /voice tts | به هر پیامی پاسخ می‌دهد |

`off`
`/voice off`
`voice_only`
`/voice on`
`all`
`/voice tts`

تنظیم حالت صوتی در راه‌اندازی مجدد گیت‌وی پایدار می‌ماند.

### تحویل پلتفرم

| پلتفرم | قالب | یادداشت‌ها |
| --- | --- | --- |
| Telegram | حباب صوتی (Opus/OGG) | در چت به صورت درون‌خطی پخش می‌شود. ffmpeg در صورت نیاز MP3 → Opus تبدیل می‌کند |
| Discord | حباب صوتی بومی (Opus/OGG) | مانند پیام صوتی کاربر درون‌خطی پخش می‌شود. در صورت خرابی API حباب صوتی به پیوست فایل بازمی‌گردد |

## کانال‌های صوتی Discord

ویژگی صوتی غوطه‌ورتر: ربات به یک کانال صوتی Discord می‌پیوندد، به صحبت کردن کاربران گوش می‌دهد، گفتار آنها را رونویسی می‌کند، از طریق عامل پردازش می‌کند و پاسخ را در کانال صوتی بازگو می‌کند.

### راه‌اندازی

#### 1. مجوزهای ربات Discord

اگر قبلاً یک ربات Discord برای متن راه‌اندازی کرده‌اید (به Discord Setup Guide مراجعه کنید)، باید مجوزهای صوتی را اضافه کنید.

[Discord Setup Guide](/docs/user-guide/messaging/discord)

به [Discord Developer Portal](https://discord.com/developers/applications) → application شما → Installation → Default Install Settings → Guild Install بروید:

این مجوزها را به مجوزهای متنی موجود اضافه کنید:

| مجوز | هدف | لازم |
| --- | --- | --- |
| Connect | پیوستن به کانال‌های صوتی | بله |
| Speak | پخش صدا در کانال‌های صوتی | بله |
| Use Voice Activity | تشخیص صحبت کردن کاربران | توصیه شده |

عدد مجوز به‌روز شده:

| سطح | عدد | شامل چه چیزی |
| --- | --- | --- |
| فقط متن | 309237763136 | مشاهده کانال‌ها، ارسال پیام‌ها، خواندن تاریخچه، جاسازی‌ها، پیوست‌ها، رشته‌ها، واکنش‌ها، ایجاد رشته‌های عمومی |
| متن + صدا | 309240908864 | همه موارد بالا + Connect، Speak |

`309237763136`
`309240908864`

ربات را با URL مجوز به‌روز شده مجدداً دعوت کنید:

```
https://discord.com/oauth2/authorize?client_id=YOUR_APP_ID&scope=bot+applications.commands&permissions=309240908864
```

YOUR_APP_ID را با Application ID خود از Developer Portal جایگزین کنید.

`YOUR_APP_ID`

دعوت مجدد ربات به سروری که در آن حضور دارد، مجوزهایش را بدون حذف آن به‌روز می‌کند. هیچ داده یا پیکربندی‌ای را از دست نخواهید داد.

#### 2. Intentهای دروازه امتیازی

در [Developer Portal](https://discord.com/developers/applications) → application شما → Bot → Privileged Gateway Intents، هر سه را فعال کنید:

| Intent | هدف |
| --- | --- |
| Presence Intent | تشخیص وضعیت آنلاین/آفلاین کاربر |
| Server Members Intent | حل نام‌های کاربری در DISCORD_ALLOWED_USERS به شناسه‌های عددی (شرطی) |
| Message Content Intent | خواندن محتوای پیام متنی در کانال‌ها |

`DISCORD_ALLOWED_USERS`

Message Content Intent لازم است. Server Members Intent فقط در صورتی لازم است که لیست DISCORD_ALLOWED_USERS شما از نام‌های کاربری استفاده کند — اگر از شناسه‌های عددی کاربر استفاده می‌کنید، می‌توانید آن را OFF بگذارید. نگاشت SSRC → user_id کانال صوتی از کد opcode SPEAKING Discord در websocket صوتی می‌آید و به Server Members Intent نیاز ندارد.

`DISCORD_ALLOWED_USERS`

#### 3. کدک Opus

کتابخانه کدک Opus باید روی ماشینی که گیت‌وی را اجرا می‌کند نصب شده باشد:

```
# macOS (Homebrew)brew install opus# Ubuntu/Debiansudo apt install libopus0
```

ربات کدک را از اینجا بارگذاری می‌کند:

- macOS: /opt/homebrew/lib/libopus.dylib
- Linux: libopus.so.0

`/opt/homebrew/lib/libopus.dylib`
`libopus.so.0`

#### 4. متغیرهای محیطی

```
# ~/.hermes/.env# ربات Discord (از قبل برای متن پیکربندی شده)DISCORD_BOT_TOKEN=your-bot-tokenDISCORD_ALLOWED_USERS=your-user-id# STT — ارائه‌دهنده محلی نیازی به کلید ندارد (pip install faster-whisper)# GROQ_API_KEY=your-key            # جایگزین: مبتنی بر ابر، سریع، سطح رایگان# TTS — اختیاری. Edge TTS و NeuTTS نیازی به کلید ندارند.# ELEVENLABS_API_KEY=***      # کیفیت پریمیوم# VOICE_TOOLS_OPENAI_KEY=***  # OpenAI TTS / Whisper
```

### شروع گیت‌وی

```
hermes gateway        # شروع با پیکربندی موجود
```

ربات باید ظرف چند ثانیه در Discord آنلاین شود.

### دستورات

از اینها در کانال متنی Discord که ربات در آن حضور دارد استفاده کنید:

```
/voice join      ربات به کانال صوتی فعلی شما می‌پیوندد/voice channel   نام مستعار برای /voice join/voice leave     ربات از کانال صوتی قطع می‌شود/voice status    حالت صوتی و کانال متصل را نشان دهید
```

باید قبل از اجرای /voice join در یک کانال صوتی باشید. ربات به همان VC که شما در آن هستید می‌پیوندد.

`/voice join`

### نحوه کار

وقتی ربات به یک کانال صوتی می‌پیوندد:

1. به جریان صوتی هر کاربر به طور مستقل گوش می‌دهد
2. سکوت را تشخیص می‌دهد — 1.5 ثانیه سکوت پس از حداقل 0.5 ثانیه گفتار پردازش را فعال می‌کند
3. صدا را از طریق Whisper STT (محلی، Groq، یا OpenAI) رونویسی می‌کند
4. از طریق خط لوله کامل عامل (جلسه، ابزارها، حافظه) پردازش می‌کند
5. پاسخ را از طریق TTS در کانال صوتی بازگو می‌کند

### ادغام کانال متنی

وقتی ربات در یک کانال صوتی است:

- رونویسی‌ها در کانال متنی ظاهر می‌شوند: [Voice] @user: آنچه گفتید
- پاسخ‌های عامل به صورت متن در کانال و در VC بازگو می‌شوند
- کانال متنی همان است که /voice join در آن صادر شده

`[Voice] @user: what you said`
`/voice join`

### جلوگیری از اکو

ربات به طور خودکار شنونده صوتی خود را در حین پخش پاسخ‌های TTS متوقف می‌کند و از شنیدن و پردازش مجدد خروجی خود جلوگیری می‌کند.

### کنترل دسترسی

فقط کاربران فهرست شده در DISCORD_ALLOWED_USERS می‌توانند از طریق صدا تعامل کنند. صدای سایر کاربران بی‌صدا نادیده گرفته می‌شود.

`DISCORD_ALLOWED_USERS`

```
# ~/.hermes/.envDISCORD_ALLOWED_USERS=284102345871466496
```

## مرجع پیکربندی

### config.yaml

```
# ضبط صدا (CLI)voice:  record_key: "ctrl+b"            # کلید شروع/پایان ضبط  max_recording_seconds: 120       # حداکثر طول ضبط  auto_tts: false                  # فعال کردن خودکار TTS وقتی حالت صوتی شروع می‌شود  beep_enabled: true               # پخش بیپ شروع/پایان ضبط  silence_threshold: 200           # سطح RMS (0-32767) که زیر آن سکوت محسوب می‌شود  silence_duration: 3.0            # ثانیه سکوت قبل از توقف خودکار# گفتار به متنstt:  enabled: true                     # روی false تنظیم کنید تا رونویسی خودکار رد شود —                                    # گیت‌وی همچنان فایل صوتی را کش می‌کند و                                    # مسیر آن را به عنوان بخشی از پیام ورودی                                    # به عامل ارسال می‌کند، مفید برای خطوط لوله سفارشی                                    # (diarization، alignment، بایگانی و غیره)  provider: "local"                  # "local" (رایگان) | "groq" | "openai" | "mistral" | "xai"  local:    model: "base"                    # tiny، base، small، medium، large-v3  # model: "whisper-1"              # قدیمی: وقتی provider تنظیم نشده استفاده می‌شود# متن به گفتارtts:  provider: "edge"                 # "edge" (رایگان) | "elevenlabs" | "openai" | "neutts" | "minimax" | "mistral" | "gemini" | "xai" | "kittentts" | "piper"  edge:    voice: "en-US-AriaNeural"      # 322 صدا، 74 زبان  elevenlabs:    voice_id: "pNInz6obpgDQGcFmaJgB"    # Adam    model_id: "eleven_multilingual_v2"  openai:    model: "gpt-4o-mini-tts"    voice: "alloy"                 # alloy، echo، fable، onyx، nova، shimmer    base_url: "https://api.openai.com/v1"  # اختیاری: بازنویسی برای endpoints میزبانی شده خود  neutts:    ref_audio: ''    ref_text: ''    model: neuphonic/neutts-air-q4-gguf    device: cpu
```

### متغیرهای محیطی

```
# ارائه‌دهندگان گفتار به متن (محلی نیازی به کلید ندارد)# pip install faster-whisper        # STT محلی رایگان — نیازی به کلید API نیستGROQ_API_KEY=...                    # Groq Whisper (سریع، سطح رایگان)VOICE_TOOLS_OPENAI_KEY=...         # OpenAI Whisper (پولی)# بازنویسی‌های پیشرفته STT (اختیاری)STT_GROQ_MODEL=whisper-large-v3-turbo    # بازنویسی مدل پیش‌فرض Groq STTSTT_OPENAI_MODEL=whisper-1               # بازنویسی مدل پیش‌فرض OpenAI STTGROQ_BASE_URL=https://api.groq.com/openai/v1     # Endpoint سفارشی GroqSTT_OPENAI_BASE_URL=https://api.openai.com/v1    # Endpoint سفارشی OpenAI STT# ارائه‌دهندگان متن به گفتار (Edge TTS و NeuTTS نیازی به کلید ندارند)ELEVENLABS_API_KEY=***             # ElevenLabs (کیفیت پریمیوم)# VOICE_TOOLS_OPENAI_KEY بالا همچنین OpenAI TTS را فعال می‌کند# کانال صوتی DiscordDISCORD_BOT_TOKEN=...DISCORD_ALLOWED_USERS=...
```

### مقایسه ارائه‌دهندگان STT

| ارائه‌دهنده | مدل | سرعت | کیفیت | هزینه | کلید API |
| --- | --- | --- | --- | --- | --- |
| محلی | base | سریع (بستگی به CPU/GPU دارد) | خوب | رایگان | خیر |
| محلی | small | متوسط | بهتر | رایگان | خیر |
| محلی | large-v3 | کند | بهترین | رایگان | خیر |
| Groq | whisper-large-v3-turbo | بسیار سریع (~0.5s) | خوب | سطح رایگان | بله |
| Groq | whisper-large-v3 | سریع (~1s) | بهتر | سطح رایگان | بله |
| OpenAI | whisper-1 | سریع (~1s) | خوب | پولی | بله |
| OpenAI | gpt-4o-transcribe | متوسط (~2s) | بهترین | پولی | بله |
| Mistral | voxtral-mini-latest | سریع | خوب | پولی | بله |
| xAI | grok-stt | سریع | خوب | پولی | بله |

`base`
`small`
`large-v3`
`whisper-large-v3-turbo`
`whisper-large-v3`
`whisper-1`
`gpt-4o-transcribe`
`voxtral-mini-latest`
`grok-stt`

اولویت ارائه‌دهنده (بازگشت خودکار): local > groq > openai

### مقایسه ارائه‌دهندگان TTS

| ارائه‌دهنده | کیفیت | هزینه | تأخیر | نیاز به کلید |
| --- | --- | --- | --- | --- |
| Edge TTS | خوب | رایگان | ~1s | خیر |
| ElevenLabs | عالی | پولی | ~2s | بله |
| OpenAI TTS | خوب | پولی | ~1.5s | بله |
| NeuTTS | خوب | رایگان | بستگی به CPU/GPU دارد | خیر |

NeuTTS از بلوک پیکربندی tts.neutts بالا استفاده می‌کند.

`tts.neutts`

## عیب‌یابی

### "No audio device found" (CLI)

PortAudio نصب نشده:

```
brew install portaudio    # macOSsudo apt install portaudio19-dev  # Ubuntu
```

اگر Hermes را در Docker روی دسکتاپ Linux اجرا می‌کنید، container نیز به سوکت صوتی میزبان شما نیاز دارد. یادداشت‌های [Docker audio bridge](/docs/user-guide/docker#optional-linux-desktop-audio-bridge) را برای تنظیم سازگار با PulseAudio/PipeWire ببینید.

### ربات در کانال‌های سرور Discord پاسخ نمی‌دهد

ربات به طور پیش‌فرض در کانال‌های سرور به @mention نیاز دارد. مطمئن شوید:

1. @ تایپ کنید و کاربر bot (با #discriminator) را انتخاب کنید، نه نقشی با همان نام
2. یا به جای آن از DM استفاده کنید — نیازی به اشاره نیست
3. یا DISCORD_REQUIRE_MENTION=false را در ~/.hermes/.env تنظیم کنید

`@`
`DISCORD_REQUIRE_MENTION=false`
`~/.hermes/.env`

### ربات به VC می‌پیوندد اما صدای من را نمی‌شنود

- بررسی کنید شناسه کاربر Discord شما در DISCORD_ALLOWED_USERS باشد
- مطمئن شوید در Discord بی‌صدا نیستید
- ربات قبل از نگاشت صدای شما به یک رویداد SPEAKING از Discord نیاز دارد — چند ثانیه پس از پیوستن شروع به صحبت کردن کنید

`DISCORD_ALLOWED_USERS`

### ربات صدای من را می‌شنود اما پاسخ نمی‌دهد

- تأیید کنید STT در دسترس است: faster-whisper را نصب کنید (نیازی به کلید نیست) یا GROQ_API_KEY/VOICE_TOOLS_OPENAI_KEY را تنظیم کنید
- بررسی کنید مدل LLM پیکربندی شده و قابل دسترسی باشد
- گزارش‌های گیت‌وی را بررسی کنید: tail -f ~/.hermes/logs/gateway.log

`faster-whisper`
`GROQ_API_KEY`
`VOICE_TOOLS_OPENAI_KEY`
`tail -f ~/.hermes/logs/gateway.log`

### ربات در متن پاسخ می‌دهد اما در کانال صوتی نه

- ارائه‌دهنده TTS ممکن است خراب باشد — کلید API و سهمیه را بررسی کنید
- Edge TTS (رایگان، بدون کلید) بازگشت پیش‌فرض است
- گزارش‌ها را برای خطاهای TTS بررسی کنید

### Whisper متن زباله برمی‌گرداند

فیلتر توهم اکثر موارد را به طور خودکار می‌گیرد. اگر هنوز رونویسی‌های توهمی دریافت می‌کنید:

- از محیط آرام‌تر استفاده کنید
- silence_threshold در پیکربندی را تنظیم کنید (بالاتر = حساسیت کمتر)
- یک مدل STT متفاوت امتحان کنید

`silence_threshold`
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/voice-mode.md)