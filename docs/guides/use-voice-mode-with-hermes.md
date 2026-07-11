---
layout: docs
title: "استفاده از حالت صوتی"
permalink: /docs/guides/use-voice-mode-with-hermes/
---

- 
- Guides & Tutorials
- Use Voice Mode with Hermes

# استفاده از حالت صوتی با Hermes

این راهنما همراه عملی مرجع ویژگی حالت صوتی است.

[مرجع ویژگی حالت صوتی](/docs/user-guide/features/voice-mode/)

اگر صفحه ویژگی توضیح می‌دهد حالت صوتی چه کاری می‌تواند انجام دهد، این راهنما نشان می‌دهد چگونه واقعاً به خوبی از آن استفاده کنید.

Nous Portal هر دو LLM و TTS را از طریق یک OAuth بسته‌بندی می‌کند — حالت صوتی از ابتدا تا انتها بدون اعتبارنامه اضافی کار می‌کند.

[Nous Portal](/docs/integrations/nous-portal/)

## حالت صوتی برای چه چیزی خوب است

حالت صوتی به ویژه وقتی مفید است که:

- می‌خواهید یک workflow CLI بدون دست داشته باشید
- می‌خواهید پاسخ‌های گفتاری در Telegram یا Discord داشته باشید
- می‌خواهید Hermes در یک کانال صوتی Discord برای مکالمه زنده بنشیند
- می‌خواهید ایده‌گیری سریع، عیب‌یابی یا رفت و برگشت حین راه رفتن به جای تایپ کردن داشته باشید

## تنظیم حالت صوتی خود را انتخاب کنید

در واقع سه تجربه صوتی متفاوت در Hermes وجود دارد.

| حالت | بهترین برای | پلتفرم |
| --- | --- | --- |
| حلقه میکروفون تعاملی | استفاده شخصی بدون دست حین کدنویسی یا تحقیق | CLI |
| پاسخ‌های صوتی در چت | پاسخ‌های گفتاری در کنار پیام‌رسانی عادی | Telegram، Discord |
| ربات کانال صوتی زنده | مکالمه زنده گروهی یا شخصی در VC | کانال‌های صوتی Discord |

یک مسیر خوب:

1. ابتدا متن را کارآمد کنید
2. سپس پاسخ‌های صوتی را فعال کنید
3. در نهایت اگر تجربه کامل می‌خواهید به کانال‌های صوتی Discord بروید

## مرحله ۱: مطمئن شوید Hermes عادی ابتدا کار می‌کند

قبل از دست زدن به حالت صوتی، تأیید کنید که:

- Hermes شروع می‌شود
- ارائه‌دهنده شما پیکربندی شده
- agent می‌تواند به پرامپت‌های متنی به طور عادی پاسخ دهد

```
hermes
```

چیز ساده‌ای بپرسید:

```
What tools do you have available?
```

اگر هنوز محکم نیست، ابتدا حالت متن را تعمیر کن.

## مرحله ۲: extras درست را نصب کنید

### میکروفون CLI + پخش

```
cd ~/.hermes/hermes-agent && uv pip install -e ".[voice]"
```

### پلتفرم‌های پیام‌رسانی

```
cd ~/.hermes/hermes-agent && uv pip install -e ".[messaging]"
```

### ElevenLabs TTS پریمیوم

```
cd ~/.hermes/hermes-agent && uv pip install -e ".[tts-premium]"
```

### NeuTTS محلی (اختیاری)

```
python -m pip install -U neutts[all]
```

### همه چیز

```
cd ~/.hermes/hermes-agent && uv pip install -e ".[all]"
```

## مرحله ۳: وابستگی‌های سیستم را نصب کنید

### macOS

```
brew install portaudio ffmpeg opusbrew install espeak-ng
```

### Ubuntu / Debian

```
sudo apt install portaudio19-dev ffmpeg libopus0sudo apt install espeak-ng
```

چرا اینها مهم هستند:

- `portaudio` → ورودی میکروفون / پخش برای حالت صوتی CLI
- `ffmpeg` → تبدیل صدا برای TTS و تحویل پیام‌رسانی
- `opus` → پشتیبانی کدک صوتی Discord
- `espeak-ng` → پشتیبان Phonemizer برای NeuTTS

`portaudio`
`ffmpeg`
`opus`
`espeak-ng`

## مرحله ۴: ارائه‌دهندگان STT و TTS را انتخاب کنید

Hermes از هر دو پشته گفتار محلی و ابری پشتیبانی می‌کند.

### آسان‌ترین / ارزان‌ترین تنظیم

از STT محلی و Edge TTS رایگان استفاده کنید:

- ارائه‌دهنده STT: `local`
- ارائه‌دهنده TTS: `edge`

`local`
`edge`

این معمولاً بهترین نقطه شروع است.

### مثال فایل محیطی

به `~/.hermes/.env` اضافه کنید:

`~/.hermes/.env`

```
# گزینه‌های STT ابری (محلی نیازی به کلید ندارد)GROQ_API_KEY=***VOICE_TOOLS_OPENAI_KEY=***# TTS پریمیوم (اختیاری)ELEVENLABS_API_KEY=***
```

### توصیه‌های ارائه‌دهنده

#### گفتار به متن

- `local` → بهترین پیش‌فرض برای حریم خصوصی و استفاده بدون هزینه
- `groq` → رونویسی ابری بسیار سریع
- `openai` → بازگشت پولی خوب

`local`
`groq`
`openai`

#### متن به گفتار

- `edge` → رایگان و برای اکثر کاربران به اندازه کافی خوب
- `neutts` → TTS محلی/روی دستگاه رایگان
- `elevenlabs` → بهترین کیفیت
- `openai` → میانه خوب
- `mistral` → چند زبانه، Opus بومی

`edge`
`neutts`
`elevenlabs`
`openai`
`mistral`

### اگر از `hermes setup` استفاده می‌کنید

`hermes setup`

اگر NeuTTS را در جادوگر راه‌اندازی انتخاب کنید، Hermes بررسی می‌کند آیا `neutts` از قبل نصب شده است. اگر وجود نداشته باشد، جادوگر به شما می‌گوید NeuTTS به پکیج Python `neutts` و پکیج سیستم `espeak-ng` نیاز دارد، پیشنهاد می‌کند آنها را برای شما نصب کند، `espeak-ng` را با مدیر پکیج پلتفرم شما نصب می‌کند و سپس اجرا می‌کند:

`neutts`
`neutts`
`espeak-ng`
`espeak-ng`

```
python -m pip install -U neutts[all]
```

اگر آن نصب را رد کنید یا ناموفق باشد، جادوگر به Edge TTS بازمی‌گردد.

## مرحله ۵: config توصیه شده

```
voice:  record_key: "ctrl+b"  max_recording_seconds: 120  auto_tts: false  beep_enabled: true  silence_threshold: 200  silence_duration: 3.0stt:  provider: "local"  local:    model: "base"tts:  provider: "edge"  edge:    voice: "en-US-AriaNeural"
```

این یک پیش‌فرض خوب محافظه‌کارانه برای اکثر افراد است.

اگر TTS محلی به جای آن می‌خواهید، بلوک `tts` را به این سوئیچ کنید:

`tts`

```
tts:  provider: "neutts"  neutts:    ref_audio: ''    ref_text: ''    model: neuphonic/neutts-air-q4-gguf    device: cpu
```

## کاربرد ۱: حالت صوتی CLI

## آن را فعال کنید

Hermes را راه‌اندازی کنید:

```
hermes
```

در داخل CLI:

```
/voice on
```

### جریان ضبط

کلید پیش‌فرض:

- `Ctrl+B`

`Ctrl+B`

workflow:

1. `Ctrl+B` را فشار دهید
2. صحبت کنید
3. منتظر تشخیص سکوت باشید تا ضبط را به طور خودکار متوقف کند
4. Hermes رونویسی و پاسخ می‌دهد
5. اگر TTS فعال باشد، پاسخ را بیان می‌کند
6. حلقه می‌تواند برای استفاده پیوسته به طور خودکار شروع شود

`Ctrl+B`

### دستورات مفید

```
/voice/voice on/voice off/voice tts/voice status
```

### workflowهای خوب CLI

#### عیب‌یابی در حین راه رفتن

بگویید:

```
I keep getting a docker permission error. Help me debug it.
```

سپس بدون دست ادامه دهید:

- «خطا آخر را دوباره بخوان»
- «علت اصلی را به زبان ساده‌تر توضیح بده»
- «حالا دقیق تعمیر را به من بده»

#### تحقیق / طوفان فکری

عالی برای:

- راه رفتن حین فکر کردن
- رونویسی ایده‌های نیمه شکل‌گرفته
- از Hermes بخواهید افکار شما را در لحظه ساختار دهد

#### دسترسی / نشست‌های کم تایپ

اگر تایپ کردن ناراحت‌کننده است، حالت صوتی یکی از سریع‌ترین راه‌ها برای ماندن در حلقه کامل Hermes است.

## تنظیم رفتار CLI

### آستانه سکوت

اگر Hermes بیش از حد تهاجمی شروع/متوقف می‌شود، تنظیم کنید:

```
voice:  silence_threshold: 250
```

آستانه بالاتر = حساسیت کمتر.

### مدت سکوت

اگر بین جملات زیاد مکث می‌کنید، افزایش دهید:

```
voice:  silence_duration: 4.0
```

### کلید ضبط

اگر `Ctrl+B` با ترمینال یا عادت‌های tmux شما تداخل دارد:

`Ctrl+B`

```
voice:  record_key: "ctrl+space"
```

## کاربرد ۲: پاسخ‌های صوتی در Telegram یا Discord

این حالت ساده‌تر از کانال‌های صوتی کامل است.

Hermes یک ربات چت عادی باقی می‌ماند اما می‌تواند پاسخ‌ها را بیان کند.

### راه‌اندازی gateway

```
hermes gateway
```

### فعال کردن پاسخ‌های صوتی

در داخل Telegram یا Discord:

```
/voice on
```

یا

```
/voice tts
```

### حالت‌ها

| حالت | معنی |
| --- | --- |
| off | فقط متن |
| voice_only | فقط وقتی کاربر صدا فرستاده بیان کند |
| all | هر پاسخی را بیان کند |

`off`
`voice_only`
`all`

### چه زمانی از کدام حالت استفاده کنید

- `/voice on` اگر فقط برای پیام‌های صوتی پاسخ گفتاری می‌خواهید
- `/voice tts` اگر یک دستیار گفتاری کامل همیشه می‌خواهید

`/voice on`
`/voice tts`

### workflowهای خوب پیام‌رسانی

#### دستیار Telegram در گوشی شما

وقتی استفاده کنید:

- از ماشین خود دور هستید
- می‌خواهید یادداشت‌های صوتی ارسال کنید و پاسخ‌های گفتاری سریع دریافت کنید
- می‌خواهید Hermes مانند یک دستیار تحقیقاتی یا عملیاتی قابل حمل عمل کند

#### DMهای Discord با خروجی گفتاری

مفید وقتی تعامل خصوصی بدون رفتار mention کانال سرور می‌خواهید.

## کاربرد ۳: کانال‌های صوتی Discord

این پیشرفته‌ترین حالت است.

Hermes به یک VC Discord می‌پیوندد، به گفتار کاربران گوش می‌دهد، آن را رونویسی می‌کند، خط لول agent عادی را اجرا می‌کند و پاسخ‌ها را در کانال بیان می‌کند.

## دسترسی‌های مورد نیاز Discord

علاوه بر راه‌اندازی متنی عادت ربات، مطمئن شوید ربات دارد:

- Connect
- Speak
- ترجیحاً Use Voice Activity

همچنین intentهای特权‌دار را در Developer Portal فعال کنید:

- Presence Intent
- Server Members Intent
- Message Content Intent

## پیوستن و ترک

در یک کانال متنی Discord که ربات در آن حضور دارد:

```
/voice join/voice leave/voice status
```

### وقتی می‌پیوندد چه اتفاقی می‌افتد

- کاربران در VC صحبت می‌کنند
- Hermes مرزهای گفتار را تشخیص می‌دهد
- رونویسی‌ها در کانال متنی مرتبط پست می‌شوند
- Hermes به صورت متنی و صوتی پاسخ می‌دهد
- کانال متنی همان است که `/voice join` در آن صادر شده

`/voice join`

### بهترین شیوه‌ها برای استفاده از VC Discord

- `DISCORD_ALLOWED_USERS` را باریک نگه دارید
- ابتدا از یک کانال اختصاصی ربات/تست استفاده کنید
- STT و TTS را در حالت چت متنی عادی قبل از امتحان حالت VC تأیید کنید

`DISCORD_ALLOWED_USERS`

## توصیه‌های کیفیت صدا

### بهترین تنظیم کیفیت

- STT: محلی `large-v3` یا Groq `whisper-large-v3`
- TTS: ElevenLabs

`large-v3`
`whisper-large-v3`

### بهترین تنظیم سرعت / راحتی

- STT: محلی `base` یا Groq
- TTS: Edge

`base`

### بهترین تنظیم بدون هزینه

- STT: محلی
- TTS: Edge

## حالت‌های خرابی رایج

### «No audio device found»

`portaudio` را نصب کنید.

`portaudio`

### «ربات می‌پیوندد اما چیزی نمی‌شنود»

بررسی کنید:

- شناسه کاربر Discord شما در `DISCORD_ALLOWED_USERS` باشد
- بی‌صدا نباشید
- intentهای特权‌دار فعال باشند
- ربات دسترسی‌های Connect/Speak داشته باشد

`DISCORD_ALLOWED_USERS`

### «رونویسی می‌کند اما بیان نمی‌کند»

بررسی کنید:

- پیکربندی ارائه‌دهنده TTS
- کلید API / سهمیه برای ElevenLabs یا OpenAI
- نصب `ffmpeg` برای مسیرهای تبدیل Edge

`ffmpeg`

### «Whisper متن زباله برمی‌گرداند»

امتحان کنید:

- محیط ساکت‌تر
- `silence_threshold` بالاتر در config
- مدل/ارائه‌دهنده STT متفاوت
- عبارات کوتاه‌تر و واضح‌تر

`silence_threshold`

### «در DMها کار می‌کند اما در کانال‌های سرور نه»

این اغلب سیاست mention است.

به طور پیش‌فرض، ربات در کانال‌های متنی سرور Discord به `@mention` نیاز دارد مگر اینکه پیکربندی شده باشد.

`@mention`

## تنظیم هفته اول پیشنهادی

اگر کوتاه‌ترین مسیر موفقیت را می‌خواهید:

1. Hermes متنی را کارآمد کنید
2. `hermes-agent[voice]` را نصب کنید
3. از حالت صوتی CLI با STT محلی + Edge TTS استفاده کنید
4. سپس `/voice on` را در Telegram یا Discord فعال کنید
5. فقط پس از آن، حالت VC Discord را امتحان کنید

`hermes-agent[voice]`
`/voice on`

این پیشرفت سطح عیب‌یابی را کوچک نگه می‌دارد.

## جایی که باید بعد بخوانید

- مرجع ویژگی حالت صوتی
- دروازه پیام‌رسانی
- راه‌اندازی Discord
- راه‌اندازی Telegram
- پیکربندی

[مرجع ویژگی حالت صوتی](/docs/user-guide/features/voice-mode/)
[دروازه پیام‌رسانی](/docs/user-guide/messaging/)
[راه‌اندازی Discord](/docs/user-guide/messaging/discord/)
[راه‌اندازی Telegram](/docs/user-guide/messaging/telegram/)
[پیکربندی](/docs/user-guide/configuration/)
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/guides/use-voice-mode-with-hermes.md)
