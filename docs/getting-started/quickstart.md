---
layout: docs
title: "راهنمای شروع سریع"
permalink: /docs/getting-started/quickstart/
---

- 
- Getting Started
- Quickstart

# شروع سریع

این راهنما شما را از صفر به یک نصب کاربردی Hermes می‌رساند که در استفاده واقعی دوام می‌آورد. نصب کنید، یک ارائه‌دهنده انتخاب کنید، یک چت کاربردی را تأیید کنید و دقیقاً بدانید وقتی چیزی خراب می‌شود چه کاری انجام دهید.

## ترجیح می‌دهید تماشا کنید؟

Onchain AI Garage یک walkthrough جامع از نصب، تنظیم و فرمان‌های پایه تهیه کرده — یک همراه خوب برای این صفحه اگر ترجیح می‌دهید با ویدیو دنبال کنید. برای بیشتر، [پلی‌لیست آموزش‌ها و موارد استفاده Hermes Agent](https://www.youtube.com/playlist?list=PLmpUb_PWAkDxewld5ZYyKifuHxgIbiq2d) را ببینید.

## برای چه کسی است

- کاملاً جدید هستید و کوتاه‌ترین مسیر به یک نصب کاربردی می‌خواهید
- ارائه‌دهنده را عوض می‌کنید و نمی‌خواهید با اشتباهات پیکربندی وقت از دست دهید
- Hermes را برای یک تیم، ربات یا جریان کاری همیشه‌فعال راه‌اندازی می‌کنید
- از «نصب شد، ولی هنوز هیچ کاری نمی‌کند» خسته شده‌اید

## سریع‌ترین مسیر

 ردیفی که با هدف شما مطابقت دارد را انتخاب کنید:

| هدف | اول این کار را انجام دهید | سپس این کار را انجام دهید |
| --- | --- | --- |
| فقط می‌خواهم Hermes روی ماشین من کار کند | `hermes setup` | یک چت واقعی اجرا کنید و تأیید کنید پاسخ می‌دهد |
| ارائه‌دهنده خود را می‌دانم | `hermes model` | پیکربندی را ذخیره کنید، سپس شروع به چت کنید |
| یک ربات یا نصب همیشه‌فعال می‌خواهم | `hermes gateway setup` بعد از کار CLI | Telegram، Discord، Slack یا پلتفرم دیگری را وصل کنید |
| یک مدل محلی یا self-hosted می‌خواهم | `hermes model` → custom endpoint | endpoint، نام مدل و طول context را تأیید کنید |
| fallback چند ارائه‌دهنده می‌خواهم | `hermes model` اول | مسیریابی و fallback فقط بعد از کار چت پایه اضافه کنید |

قانون کلی: اگر Hermes نمی‌تواند یک چت عادی را تکمیل کند، هنوز ویژگی‌های بیشتری اضافه نکنید. ابتدا یک مکالمه تمیز را کار کنید، سپس gateway، cron، skillها، صدا یا مسیریابی را لایه‌بندی کنید.

## ۱. نصب Hermes Agent

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

اگر روی گوشی نصب می‌کنید، [راهنمای Termux](/docs/getting-started/termux/) را برای مسیر دستی تست‌شده، اکستراهای پشتیبانی‌شده و محدودیت‌های فعلی مختص اندروید ببینید.

بعد از اتمام، shell خود را مجدداً بارگذاری کنید:

```bash
source ~/.bashrc   # یا source ~/.zshrc
```

برای گزینه‌های نصب دقیق، پیش‌نیازها و عیب‌یابی، [راهنمای نصب](/docs/getting-started/installation/) را ببینید.

## ۲. انتخاب یک ارائه‌دهنده

مهم‌ترین قدم تنظیم. از `hermes model` برای راهنمایی تعاملی انتخاب استفاده کنید:

```
hermes model
```

یک اشتیاق ۳۰۰+ مدل به علاوه [Tool Gateway](/docs/user-guide/features/tool-gateway/) (جستجوی وب، تولید تصویر، TTS، مرورگر ابری) را پوشش می‌دهد. در یک نصب جدید:

```bash
hermes setup --portal
```

شما را وارد می‌کند، Nous را به عنوان ارائه‌دهنده شما تنظیم می‌کند و Tool Gateway را با یک فرمان فعال می‌کند.

در یک نصب جدید، `hermes setup` سه حالت ارائه می‌دهد:

- **Quick Setup (Nous Portal)** — ورود OAuth رایگان، بدون کلید API؛ یک مدل به علاوه ابزارهای Tool Gateway را تنظیم می‌کند. مسیر سریع توصیه‌شده.
- **Full Setup** — هر ارائه‌دهنده، ابزار و گزینه را خودتان طی کنید (کلیدهای خودتان را بیاورید).
- **Blank Slate** — همه چیز خاموش است به جز حداقل مورد نیاز برای اجرای یک agent: ارائه‌دهنده و مدل، مجموعه ابزار File Operations و مجموعه ابزار Terminal. بدون وب، مرورگر، اجرای کد، بینایی، حافظه، تفویض، cron، skillها، پلاگین‌ها یا سرورهای MCP — و فشرده‌سازی، checkpointها، مسیریابی هوشمند و ثبت حافظه همه غیرفعال هستند. بعد از اعمال حداقل پایه، یکی از دو مسیر را انتخاب می‌کنید: شروع با همه چیز غیرفعال (اکنون با agent حداقل تمام کنید) یا طی تمام پیکربندی‌ها (ابزارها، skillها، پلاگین‌ها، MCP و پیام‌رسانی را انتخاب کنید). این را وقتی انتخاب کنید که یک agent حداقلی و کاملاً کنترل‌شده می‌خواهید و فقط دقیقاً آنچه نیاز دارید را فعال می‌کنید.

### پیش‌فرض‌های خوب:

| ارائه‌دهنده | چیست | نحوه تنظیم |
| --- | --- | --- |
| Nous Portal | مبتنی بر اشتراک، بدون پیکربندی | ورود OAuth از طریق `hermes model` |
| OpenAI Codex | ChatGPT OAuth، از مدل‌های Codex استفاده می‌کند | احراز هویت device code از طریق `hermes model` |
| Anthropic | مدل‌های Claude مستقیماً — طرح Max + اعتبارات استفاده اضافی (OAuth) یا کلید API برای پرداخت به ازای توکن | `hermes model` → ورود OAuth (نیاز به Max + اعتبارات اضافی) یا کلید API Anthropic |
| OpenRouter | مسیریابی چند ارائه‌دهنده در مدل‌های متعدد | کلید API خود را وارد کنید |
| Z.AI | مدل‌های GLM / Zhipu-hosted | `GLM_API_KEY`/`ZAI_API_KEY` را تنظیم کنید (همچنین `Z_AI_API_KEY` را می‌پذیرد) |
| Kimi / Moonshot | مدل‌های کدنویسی و چت Moonshot-hosted | `KIMI_API_KEY` را تنظیم کنید |
| Kimi / Moonshot China | endpoint منطقه چین Moonshot | `KIMI_CN_API_KEY` را تنظیم کنید |
| Arcee AI | مدل‌های Trinity | `ARCEEAI_API_KEY` را تنظیم کنید |
| GMI Cloud | API مستقیم چند مدلی | `GMI_API_KEY` را تنظیم کنید |
| MiniMax (OAuth) | مدل پیشگام MiniMax از طریق OAuth مرورگر — نیاز به کلید API نیست | `hermes model` → MiniMax (OAuth) |
| MiniMax | endpoint بین‌المللی MiniMax | `MINIMAX_API_KEY` را تنظیم کنید |
| MiniMax China | endpoint منطقه چین MiniMax | `MINIMAX_CN_API_KEY` را تنظیم کنید |
| Alibaba Cloud | مدل‌های Qwen از طریق DashScope | `DASHSCOPE_API_KEY` را تنظیم کنید |
| Hugging Face | ۲۰+ مدل باز از طریق روتر یکپارچه | `HF_TOKEN` را تنظیم کنید |
| AWS Bedrock | Claude، Nova، Llama، DeepSeek از طریق API بومی Converse | نقش IAM یا `aws configure` |
| Azure Foundry | مدل‌های Azure AI Foundry-hosted | `AZURE_FOUNDRY_API_KEY` + `AZURE_FOUNDRY_BASE_URL` را تنظیم کنید |
| Google AI Studio | مدل‌های Gemini از طریق API مستقیم | `GOOGLE_API_KEY`/`GEMINI_API_KEY` را تنظیم کنید |
| xAI | مدل‌های Grok از طریق API مستقیم | `XAI_API_KEY` را تنظیم کنید |
| xAI Grok OAuth | اشتراک SuperGrok / Premium+، نیاز به کلید API نیست | `hermes model` → xAI Grok OAuth |
| NovitaAI | دروازه API چند مدلی | `NOVITA_API_KEY` را تنظیم کنید |
| StepFun | مدل‌های Step Plan | `STEPFUN_API_KEY` را تنظیم کنید |
| Xiaomi MiMo | مدل‌های Xiaomi-hosted | `XIAOMI_API_KEY` را تنظیم کنید |
| Tencent TokenHub | مدل‌های Tencent-hosted | `TOKENHUB_API_KEY` را تنظیم کنید |
| Ollama Cloud | مدل‌های Managed Ollama-hosted | `OLLAMA_API_KEY` را تنظیم کنید |
| LM Studio | اپلیکیشن دسکتاپ محلی با API سازگار با OpenAI | `LM_API_KEY` را تنظیم کنید (و `LM_BASE_URL` اگر پیش‌فرض نیست) |
| Qwen OAuth | ورود OAuth مرورگر Qwen Portal — نیاز به کلید API نیست | `hermes model` → Qwen OAuth |
| Kilo Code | مدل‌های KiloCode-hosted | `KILOCODE_API_KEY` را تنظیم کنید |
| OpenCode Zen | دسترسی پرداخت به ازای استفاده به مدل‌های گلچین | `OPENCODE_ZEN_API_KEY` را تنظیم کنید |
| OpenCode Go | اشتراک ۱۰ دلار در ماه برای مدل‌های باز | `OPENCODE_GO_API_KEY` را تنظیم کنید |
| DeepSeek | دسترسی مستقیم به API DeepSeek | `DEEPSEEK_API_KEY` را تنظیم کنید |
| NVIDIA NIM | مدل‌های Nemotron از طریق build.nvidia.com یا NIM محلی | `NVIDIA_API_KEY` را تنظیم کنید (اختیاری: `NVIDIA_BASE_URL`) |
| GitHub Copilot | اشتراک GitHub Copilot (GPT-5.x، Claude، Gemini و غیره) | OAuth از طریق `hermes model` یا `COPILOT_GITHUB_TOKEN`/`GH_TOKEN` |
| GitHub Copilot ACP | بک‌اند agent Copilot ACP (کپیتال CLI محلی) | `hermes model` (نیاز به `copilotCLI` + `copilot login`) |
| Custom Endpoint | VLLM، SGLang، Ollama یا هر API سازگار با OpenAI | آدرس URL پایه + کلید API را تنظیم کنید |

برای بیشتر کاربران اولین بار: یک ارائه‌دهنده انتخاب کنید، مقادیر پیش‌فرض را بپذیرید مگر اینکه بدانید چرا آن‌ها را تغییر می‌دهید. فهرست کامل ارائه‌دهندگان با متغیرهای محیطی و مراحل تنظیم در صفحه [ارائه‌دهندگان AI](/docs/integrations/providers/) است.

Hermes Agent به یک مدل با حداقل ۶۴,۰۰۰ توکن context نیاز دارد. مدل‌هایی با پنجره کوچکتر نمی‌توانند حافظه کاری کافی برای گردش‌های کاری فراخوانی ابزار چندمرحله‌ای حفظ کنند و در شروع رد خواهند شد. بیشتر مدل‌های میزبانی‌شده (Claude، GPT، Gemini، Qwen، DeepSeek) به راحتی این را برآورده می‌کنند. اگر یک مدل محلی اجرا می‌کنید، اندازه context آن را حداقل ۶۴K تنظیم کنید (مثلاً `--ctx-size 65536` برای llama.cpp یا `-c 65536` برای Ollama).

می‌توانید هر زمان با `hermes model` ارائه‌دهنده را عوض کنید — بدون قفل شدن. برای فهرست کامل همه ارائه‌دهندگان پشتیبانی‌شده و جزئیات تنظیم، [ارائه‌دهندگان AI](/docs/integrations/providers/) را ببینید.

### نحوه ذخیره تنظیمات

Hermes رمزها را از پیکربندی عادی جدا می‌کند:

- رمزها و توکن‌ها → `~/.hermes/.env`
- تنظیمات غیر رمز → `~/.hermes/config.yaml`

ساده‌ترین راه برای تنظیم مقادیر به طور صحیح از طریق CLI است:

```
hermes config set model anthropic/claude-opus-4.6
hermes config set terminal.backend docker
hermes config set OPENROUTER_API_KEY sk-or-...
```

مقدار صحیح به طور خودکار به فایل صحیح هدایت می‌شود.

## ۳. اولین چت خود را اجرا کنید

```bash
hermes            # CLI کلاسیک
hermes --tui      # TUI مدرن (توصیه‌شده)
```

یک بنر خوش‌آمدگویی با مدل، ابزارهای موجود و skillهای خود خواهید دید. از یک پرامپت خاص و آسان برای تأیید استفاده کنید:

Hermes با دو رابط ترمینال ارائه می‌شود: CLI `prompt_toolkit` کلاسیک و یک TUI جدیدتر با overlayهای modal، انتخاب با ماوس و ورودی non-blocking. هر دو sessionها، فرمان‌های اسلش و پیکربندی مشترکی دارند — هر کدام را با `hermes` در مقابل `hermes --tui` امتحان کنید.

```
Summarize this repo in 5 bullets and tell me what the main entrypoint is.
```

```
Check my current directory and tell me what looks like the main project file.
```

```
Help me set up a clean GitHub PR workflow for this codebase.
```

چه چیزی موفقیت است:

- بنر مدل/ارائه‌دهنده انتخابی شما را نشان می‌دهد
- Hermes بدون خطا پاسخ می‌دهد
- می‌تواند در صورت نیاز از یک ابزار استفاده کند (ترمینال، خواندن فایل، جستجوی وب)
- مکالمه به طور عادی بیش از یک نوبت ادامه می‌یابد

اگر این کار کرد، از سخت‌ترین قسمت عبور کرده‌اید.

## ۴. تأیید کار Sessionها

قبل از ادامه، مطمئن شوید از سرگیری کار می‌کند:

```bash
hermes --continue    # از سرگیری آخرین session
hermes -c            # فرم کوتاه
```

باید شما را به sessionی که تازه داشتید برگرداند. اگر این کار را نمی‌کند، بررسی کنید آیا در همان پروفایل هستید و آیا session واقعاً ذخیره شده. این بعداً وقتی چندین نصب یا ماشین را مدیریت می‌کنید مهم است.

## ۵. ویژگی‌های کلیدی را امتحان کنید

### استفاده از ترمینال

```
❯ What's my disk usage? Show the top 5 largest directories.
```

agent به نیابت شما فرمان‌های ترمینال را اجرا می‌کند و نتایج را نشان می‌دهد.

### فرمان‌های اسلش

`/` را تایپ کنید تا کشویی autocomplete تمام فرمان‌ها را ببینید:

| فرمان | چه کاری انجام می‌دهد |
| --- | --- |
| /help | نمایش تمام فرمان‌های موجود |
| /tools | فهرست ابزارهای موجود |
| /model | تعاملی عوض کردن مدل |
| /personality pirate | امتحان یک شخصیت سرگرم‌کننده |
| /save | ذخیره مکالمه |

### ورودی چند خطی

`Alt+Enter`، `Ctrl+J` یا `Shift+Enter` را فشار دهید تا یک خط جدید اضافه شود. `Shift+Enter` نیاز به ترمینالی دارد که آن را به عنوان توالی متمایز ارسال کند (Kitty / foot / WezTerm / Ghostty به طور پیش‌فرض؛ iTerm2 / Alacritty / ترمینال VS Code وقتی پروتکل کیبورد Kitty فعال باشد). `Alt+Enter` و `Ctrl+J` در هر ترمینالی کار می‌کنند.

### متوقف کردن agent

اگر agent خیلی طول می‌کشد، یک پیام جدید تایپ کنید و Enter را فشار دهید — وظیفه فعلی را قطع می‌کند و به دستورالعمل‌های جدید شما سوئیچ می‌کند. `Ctrl+C` هم کار می‌کند.

## ۶. لایه بعدی را اضافه کنید

فقط بعد از کار چت پایه. آنچه نیاز دارید را انتخاب کنید:

### ربات یا دستیار مشترک

```bash
hermes gateway setup    # پیکربندی تعاملی پلتفرم
```

[Telegram](/docs/user-guide/messaging/telegram/)، [Discord](/docs/user-guide/messaging/discord/)، [Slack](/docs/user-guide/messaging/slack/)، [WhatsApp](/docs/user-guide/messaging/whatsapp/)، [Signal](/docs/user-guide/messaging/signal/)، [Email](/docs/user-guide/messaging/email/)، [Home Assistant](/docs/user-guide/messaging/homeassistant/) یا [Microsoft Teams](/docs/user-guide/messaging/teams/) را وصل کنید.

### اتوماسیون و ابزارها

- `hermes tools` — دسترسی ابزار را به ازای هر پلتفرم تنظیم کنید
- `hermes skills` — workflowهای قابل استفاده مجدد را مرور و نصب کنید
- Cron — فقط بعد از پایداری نصب ربات یا CLI شما

### ترمینال sandboxed

برای ایمنی، agent را در یک کانتینر Docker یا روی یک سرور راه‌دور اجرا کنید:

```bash
hermes config set terminal.backend docker    # ایزولاسیون Docker
hermes config set terminal.backend ssh       # سرور راه‌دور
```

### حالت صوتی

```bash
# از دایرکتوری نصب Hermes (نصب‌کننده curl آن را در
# ~/.hermes/hermes-agent در Linux/macOS یا %LOCALAPPDATA%\hermes\hermes-agent در Windows قرار داده):
cd ~/.hermes/hermes-agent
uv pip install -e ".[voice]"
# شامل faster-whisper برای تبدیل رایگان گفتار به متن محلی
```

سپس در CLI: `/voice on`. `Ctrl+B` را برای ضبط فشار دهید. [حالت صوتی](/docs/user-guide/features/voice-mode/) را ببینید.

### Skillها

Skillها اسناد دستورالعمل on-demand هستند که به Hermes یاد می‌دهند چگونه یک کار خاص را انجام دهد — استقرار در Kubernetes، باز کردن یک PR GitHub، تنظیم دقیق مدل، جستجوی GIF. هر کدام یک فایل `SKILL.md` با نام، توضیح و روش گام‌به‌گام هستند. agent توضیحات کوتاه را به طور رایگان می‌خواند و فقط محتوای کامل skill را وقتی بارگذاری می‌کند که واقعاً یک کار به آن نیاز دارد، بنابراین اضافه کردن skillها هر درخواست را حجیم نمی‌کند.

Hermes با فهرستی از skillهای بسته‌بندی‌شده که قبلاً در `~/.hermes/skills/` نصب شده‌اند ارائه می‌شود. می‌توانید از Skills Hub بیشتر اضافه کنید یا خودتان بنویسید.

از hub مرور و نصب کنید:

```bash
hermes skills browse                      # لیست همه موجود
hermes skills search kubernetes           # جستجوی skillها با کلمه کلیدی
hermes skills install openai/skills/k8s   # نصب یکی (ابتدا اسکن امنیتی اجرا می‌کند)
```

هر skill نصب‌شده به طور خودکار به عنوان یک فرمان اسلش تبدیل می‌شود:

```bash
/k8s deploy the staging manifest          # اجرای skill با یک درخواست
/k8s                                       # بارگذاری آن و اجازه دهید Hermes بپرسد چه نیاز دارید
```

این در CLI و هر پلتفرم پیام‌رسانی متصل کار می‌کند. لازم نیست همه چیز را از قبل نصب کنید — agent در حین مکالمه عادی skill بسته‌بندی‌شده صحیح را وقتی یک کار با آن مطابقت دارد به طور خودکار انتخاب می‌کند.

[سیستم Skillها](/docs/user-guide/features/skills/) را برای نوشتن skillهای خود، دایرکتوری‌های skill خارجی و فهرست کامل منابع hub ببینید.

### سرورهای MCP

```yaml
# به ~/.hermes/config.yaml اضافه کنید
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
```

### ادغام ویرایشگر (ACP)

پشتیبانی ACP با اکستراهای استاندارد `[all]` ارائه می‌شود، بنابراین نصب‌کننده curl آن را از قبل شامل می‌شود. فقط اجرا کنید:

```
hermes acp
```

(اگر بدون `[all]` نصب کرده‌اید، ابتدا `cd ~/.hermes/hermes-agent && uv pip install -e ".[acp]"` را اجرا کنید.)

[ادغام ویرایشگر ACP](/docs/user-guide/features/acp/) را ببینید.

## حالت‌های خرابی رایج

این مشکلاتی هستند که بیشترین وقت را هدر می‌دهند:

| علت | علت احتمالی | راه‌حل |
| --- | --- | --- |
| Hermes باز می‌شود ولی پاسخ‌های خالی یا خراب می‌دهد | احراز هویت ارائه‌دهنده یا انتخاب مدل اشتباه است | `hermes model` را دوباره اجرا کنید و ارائه‌دهنده، مدل و احراز هویت را تأیید کنید |
| Custom endpoint «کار می‌کند» ولی خروجی بی‌معنی برمی‌گرداند | آدرس URL پایه، نام مدل یا واقعاً سازگار با OpenAI نیست | endpoint را ابتدا در یک کلاینت جداگانه تأیید کنید |
| Gateway شروع می‌شود ولی کسی نمی‌تواند به آن پیام دهد | توکن ربات، allowlist یا تنظیم پلتفرم ناقص است | `hermes gateway setup` را دوباره اجرا کنید و `hermes gateway status` را بررسی کنید |
| `hermes --continue` نمی‌تواند session قدیمی را پیدا کند | پروفایل‌ها را عوض کرده یا session هرگز ذخیره نشده | `hermes sessions list` را بررسی کنید و تأیید کنید در پروفایل صحیح هستید |
| مدل ناموجود یا رفتار عجیب fallback | مسیریابی یا تنظیمات fallback ارائه‌دهنده بیش از حد تهاجمی هستند | تا پایداری ارائه‌دهنده پایه، مسیریابی را خاموش نگه دارید |
| `hermes doctor` مشکلات پیکربندی را پیدا می‌کند | مقادیر پیکربندی موجود نیستند یا قدیمی هستند | پیکربندی را تعمیر کنید، قبل از اضافه کردن ویژگی‌ها یک چت ساده را دوباره تست کنید |

## کیت بازیابی

وقتی چیزی اشتباه به نظر می‌رسد، از این ترتیب استفاده کنید:

1. `hermes doctor`
2. `hermes model`
3. `hermes setup`
4. `hermes sessions list`
5. `hermes --continue`
6. `hermes gateway status`

آن ترتیب شما را از «حس خرابی» به یک وضعیت شناخته‌شده سریع برمی‌گرداند.

## مرجع سریع

| فرمان | توضیح |
| --- | --- |
| `hermes` | شروع چت |
| `hermes model` | انتخاب ارائه‌دهنده و مدل LLM |
| `hermes tools` | پیکربندی ابزارهای فعال به ازای هر پلتفرم |
| `hermes setup` | جادوگر پیکربندی کامل (همه چیز را یکجا پیکربندی می‌کند) |
| `hermes doctor` | تشخیص مشکلات |
| `hermes update` | به‌روزرسانی به آخرین نسخه |
| `hermes gateway` | شروع gateway پیام‌رسانی |
| `hermes --continue` | از سرگیری آخرین session |

## قدم‌های بعدی

- [راهنمای CLI](/docs/user-guide/cli/) — تسلط بر رابط ترمینال
- [پیکربندی](/docs/user-guide/configuration/) — سفارشی‌سازی تنظیمات
- [Gateway پیام‌رسانی](/docs/user-guide/messaging//) — اتصال Telegram، Discord، Slack، WhatsApp، Signal، Email، Home Assistant، Teams و بیشتر
- [ابزارها و مجموعه ابزارها](/docs/user-guide/features/tools/) — کاوش قابلیت‌های موجود
- [ارائه‌دهندگان AI](/docs/integrations/providers/) — فهرست کامل ارائه‌دهندگان و جزئیات تنظیم
- [سیستم Skillها](/docs/user-guide/features/skills/) — workflowها و دانش قابل استفاده مجدد
- [نکات و بهترین شیوه‌ها](/docs/guides/tips/) — نکات کاربر حرفه‌ای

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/quickstart.md)
