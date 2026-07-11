---
layout: docs
title: "دستورات CLI"
permalink: /docs/reference/cli-commands/
---

- 
- مرجع
- مرجع دستورات
- مرجع دستورات CLI

# مرجع دستورات CLI

این صفحه دستورات ترمینالی را پوشش می‌دهد که از shell خود اجرا می‌کنید.

برای دستورات اسلش داخل چت، به Slash Commands Reference مراجعه کنید.

[Slash Commands Reference](/docs/reference/slash-commands/)

## نقطه ورود جهانی​

```
hermes [global-options] <command> [subcommand/options]
```

### گزینه‌های جهانی​

| گزینه | توضیح |
| --- | --- |
| `--version`, `-V` | نمایش نسخه و خروج. |
| `--profile <name>`, `-p <name>` | انتخاب پروفایل Hermes برای این فراخوانی. مقدار پیش‌فرض چسبناک تعیین شده توسط `hermes profile use` را override می‌کند. |
| `--resume <session>`, `-r <session>` | از سرگیری نشست قبلی با ID یا عنوان. |
| `--continue [name]`, `-c [name]` | از سرگیری آخرین نشست، یا آخرین نشست مطابق با عنوان. |
| `--worktree`, `-w` | شروع در یک git worktree ایزوله برای workflowهای agent موازی. |
| `--yolo` | دور زدن درخواستهای تأیید دستور خطرناک. |
| `--pass-session-id` | شامل کردن session ID در system prompt agent. |
| `--ignore-user-config` | نادیده گرفتن `~/.hermes/config.yaml` و بازگشت به پیش‌فرض‌های داخلی. اعتبارنامه‌ها در `.env` همچنان بارگذاری می‌شوند. |
| `--ignore-rules` | رد شدن از تزریق خودکار `AGENTS.md`، `SOUL.md`، `.cursorrules`، حافظه و مهارت‌های پیش‌بارگذاری شده. |
| `--tui` | راه‌اندازی [TUI](/docs/user-guide/tui/) به جای CLI کلاسیک. معادل `HERMES_TUI=1`. همیشه بر `display.interface` ارجحیت دارد. |
| `--cli` | اجبار به REPL کلاسیک prompt_toolkit. از این برای override کردن `display.interface: tui` در یک فراخوانی استفاده کنید. |
| `--dev` | با `--tui`: اجرای منابع TypeScript مستقیماً از طریق `tsx` به جای bundle از پیش ساخته شده (برای مشارکت‌کنندگان TUI). |

`--version`
`-V`
`--profile <name>`
`-p <name>`
`hermes profile use`
`--resume <session>`
`-r <session>`
`--continue [name]`
`-c [name]`
`--worktree`
`-w`
`--yolo`
`--pass-session-id`
`--ignore-user-config`
`~/.hermes/config.yaml`
`.env`
`--ignore-rules`
`AGENTS.md`
`SOUL.md`
`.cursorrules`
`--tui`
[TUI](/docs/user-guide/tui/)
`HERMES_TUI=1`
`display.interface`
`--cli`
`display.interface: tui`
`--dev`
`--tui`
`tsx`

## دستورات سطح بالا​

| دستور | هدف |
| --- | --- |
| `hermes chat` | چت تعاملی یا یکباره با agent. |
| `hermes model` | انتخاب تعاملی ارائه‌دهنده و مدل پیش‌فرض. |
| `hermes moa` | پیکربندی presetهای Mixture of Agents نام‌دار که از انتخابگر مدل قابل انتخاب هستند. |
| `hermes fallback` | مدیریت ارائه‌دهندگان fallback که هنگام خطای مدل اصلی امتحان می‌شوند. |
| `hermes gateway` | اجرا یا مدیریت سرویس گیت‌وی پیام‌رسانی. |
| `hermes proxy` | پروکسی محلی سازگار با OpenAI که اعتبارنامه‌های OAuth ارائه‌دهنده را متصل می‌کند. به [Subscription Proxy](/docs/user-guide/features/subscription-proxy/) مراجعه کنید. |
| `hermes lsp` | مدیریت ادغام Language Server Protocol (تشخیص‌های معنایی برای `write_file`/`patch`). |
| `hermes setup` | ویزار راه‌اندازی تعاملی برای همه یا بخشی از پیکربندی. |
| `hermes whatsapp` | پیکربندی و جفت‌سازی پل WhatsApp. |
| `hermes whatsapp-cloud` | پیکربندی آداپتور رسمی Meta WhatsApp Business Cloud API (حساب Business + webhook عمومی مورد نیاز). متمایز از `hermes whatsapp` (پل حساب شخصی Baileys). |
| `hermes slack` | ابزارهای کمکی Slack (در حال حاضر: تولید manifest برنامه با هر دستور به عنوان اسلش بومی). |
| `hermes auth` | مدیریت اعتبارنامه‌ها — اضافه کردن، فهرست کردن، حذف، بازنشانی، وضعیت، خروج از سیستم. مدیریت فلوهای OAuth برای Codex/Nous/Anthropic. |
| `hermes login`/`logout` | **منسوخ** — به جای آن از `hermes auth` استفاده کنید. |
| `hermes send` | ارسال یک پیام یکباره به یک پلتفرم پیام‌رسانی پیکربندی شده (Telegram، Discord، Slack، Signal، SMS، …). مفید از اسکریپت‌های shell، تسک‌های cron، هوک‌های CI و دیمن‌های پایش — بدون حلقه agent، بدون LLM. |
| `hermes secrets` | مدیریت منابع خارجی secret (در حال حاضر Bitwarden Secrets Manager) برای کشیدن کلیدهای API در شروع فرآیند به جای ذخیره در `~/.hermes/.env`. |
| `hermes migrate` | تشخیص و (اختیاری) بازنویسی `config.yaml` برای جایگزینی ارجاعات به مدل‌های بازنشسته یا تنظیمات منسوخ (مثلاً `migrate xai`). |
| `hermes status` | نمایش وضعیت agent، auth و پلتفرم. |
| `hermes cron` | بررسی و تیک زدن زمان‌بند cron. |
| `hermes kanban` | تخته همکاری چندپروفایلی (تسک‌ها، لینک‌ها، dispatcher). |
| `hermes project` | مدیریت فضاهای کاری نام‌دار چندپوشه (پروژه‌ها). گروه‌بندی نشست دسکتاپ را لنگر می‌اندازد و وقتی به تخته kanban متصل است، قرارداد worktree + branch تعیین‌شده به تسک‌ها می‌دهد. وضعیت به ازای هر پروفایل است. |
| `hermes webhook` | مدیریت اشتراک‌های webhook پویا برای فعال‌سازی مبتنی بر رویداد. |
| `hermes hooks` | بررسی، تأیید یا حذف هوک‌های اسکریپت shell اعلام شده در `config.yaml`. |
| `hermes doctor` | تشخیص مشکلات پیکربندی و وابستگی. |
| `hermes security audit` | ممیزی زنجیره تأمین on-demand (OSV.dev) برای venv، plugin requirements و سرورهای MCP ثابت شده. |
| `hermes dump` | خلاصه راه‌اندازی قابل کپی-پیست برای پشتیبانی/عیب‌یابی. |
| `hermes prompt-size` | نمایش تفکیک بایتی system prompt + اسکیماهای ابزار (ایندکس مهارت‌ها، حافظه، پروفایل). آفلاین اجرا می‌شود. |
| `hermes debug` | ابزارهای دیباگ — آپلود لاگ‌ها و اطلاعات سیستم برای پشتیبانی. |
| `hermes backup` | نسخه پشتیبان دایرکتوری Hermes home به فایل zip. |
| `hermes checkpoints` | بررسی / هرس / پاک کردن `~/.hermes/checkpoints/` (فروشگاه سایه‌ای که توسط `/rollback` استفاده می‌شود). بدون آرگومان اجرا کنید برای نمای کلی وضعیت. |
| `hermes import` | بازیابی نسخه پشتیبان Hermes از فایل zip. |
| `hermes logs` | مشاهده، دنبال کردن و فیلتر کردن فایل‌های لاگ agent/گیت‌وی/خطا. |
| `hermes config` | نمایش، ویرایش، مهاجرت و پرس‌وجو از فایل‌های پیکربندی. |
| `hermes pairing` | تأیید یا لغو کدهای جفت‌سازی پیام‌رسانی. |
| `hermes skills` | مرور، نصب، انتشار، ممیزی و پیکربندی مهارت‌ها. |
| `hermes bundles` | گروه‌بندی چند مهارت تحت یک دستور اسلش `/<name>`. به [Skill Bundles](/docs/user-guide/features/skills#skill-bundles) مراجعه کنید. |
| `hermes curator` | نگهداری پس‌زمینه مهارت‌ها — وضعیت، اجرا، توقف، pin. به [Curator](/docs/user-guide/features/curator/) مراجعه کنید. |
| `hermes memory` | پیکربندی ارائه‌دهنده حافظه خارجی. دستورات زیر سطح اختصاصی پلاگین (مثلاً `hermes honcho`) هنگام فعال بودن ارائه‌دهنده به طور خودکار ثبت می‌شوند. |
| `hermes acp` | اجرای Hermes به عنوان سرور ACP برای ادغام ویرایشگر. |
| `hermes mcp` | مدیریت پیکربندی سرورهای MCP و اجرای Hermes به عنوان سرور MCP. |
| `hermes plugins` | مدیریت pluginهای Hermes Agent (نصب، فعال کردن، غیرفعال کردن، حذف). |
| `hermes portal` | وضعیت Nous Portal، لینک اشتراک و مسیریابی Tool Gateway. به [Tool Gateway](/docs/user-guide/features/tool-gateway/) مراجعه کنید. |
| `hermes tools` | پیکربندی ابزارهای فعال به ازای هر پلتفرم. |
| `hermes computer-use` | نصب یا بررسی backend cua-driver (macOS Computer Use). |
| `hermes pets` | مرور، نصب و انتخاب حیوانات خانگی متحرک [petdex](/docs/user-guide/features/pets/) که در CLI، TUI و اپ دسکتاپ نمایش داده می‌شوند. دستورات زیر سطح: `list`, `install`, `select`, `show`, `off`, `scale`, `remove`, `doctor`. |
| `hermes sessions` | مرور، خروجی گرفتن، هرس، تغییر نام و حذف نشست‌ها. |
| `hermes insights` | نمایش تحلیل‌های توکن/هزینه/فعالیت. |
| `hermes claw` | ابزارهای کمکی مهاجرت OpenClaw. |
| `hermes dashboard` | راه‌اندازی داشبورد وب برای مدیریت پیکربندی، کلیدهای API و نشست‌ها. |
| `hermes desktop` (نام مستعار `gui`) | ساخت و راه‌اندازی اپ دسکتاپ بومی Electron. |
| `hermes profile` | مدیریت پروفایل‌ها — نمونه‌های ایزوله متعدد Hermes. |
| `hermes completion` | چاپ اسکریپت‌های تکمیل shell (bash/zsh/fish). |
| `hermes version` | نمایش اطلاعات نسخه. |
| `hermes update` | کشیدن آخرین کد و نصب مجدد وابستگی‌ها. `--check` بدون نصب پیش‌نمایش می‌دهد؛ `--backup` اسناپ‌شات `HERMES_HOME` قبل از کشیدن می‌گیرد. |
| `hermes uninstall` | حذف Hermes از سیستم. |

`hermes chat`
`hermes model`
`hermes moa`
`hermes fallback`
`hermes gateway`
`hermes proxy`
[Subscription Proxy](/docs/user-guide/features/subscription-proxy/)
`hermes lsp`
`hermes setup`
`hermes whatsapp`
`hermes whatsapp-cloud`
`hermes whatsapp`
`hermes slack`
`hermes auth`
`hermes login`
`logout`
`hermes auth`
`hermes send`
`hermes secrets`
`~/.hermes/.env`
`hermes migrate`
`config.yaml`
`migrate xai`
`hermes status`
`hermes cron`
`hermes kanban`
`hermes project`
`hermes webhook`
`hermes hooks`
`config.yaml`
`hermes doctor`
`hermes security audit`
`hermes dump`
`hermes prompt-size`
`hermes debug`
`hermes backup`
`hermes checkpoints`
`~/.hermes/checkpoints/`
`/rollback`
`hermes import`
`hermes logs`
`hermes config`
`hermes pairing`
`hermes skills`
`hermes bundles`
`/<name>`
[Skill Bundles](/docs/user-guide/features/skills#skill-bundles)
`hermes curator`
[Curator](/docs/user-guide/features/curator/)
`hermes memory`
`hermes honcho`
`hermes acp`
`hermes mcp`
`hermes plugins`
`hermes portal`
[Tool Gateway](/docs/user-guide/features/tool-gateway/)
`hermes tools`
`hermes computer-use`
`hermes pets`
[petdex](/docs/user-guide/features/pets/)
`list`
`install`
`select`
`show`
`off`
`scale`
`remove`
`doctor`
`hermes sessions`
`hermes insights`
`hermes claw`
`hermes dashboard`
`hermes desktop`
`gui`
`hermes profile`
`hermes completion`
`hermes version`
`hermes update`
`--check`
`--backup`
`HERMES_HOME`
`hermes uninstall`

## `hermes chat`​

`hermes chat`

```
hermes chat [options]
```

گزینه‌های رایج:

| گزینه | توضیح |
| --- | --- |
| `-q`, `--query "..."` | پرامپت یکباره، غیرتعاملی. |
| `-m`, `--model <model>` | Override کردن مدل برای این اجرا. |
| `-t`, `--toolsets <csv>` | فعال کردن مجموعه‌ای جداشده با کاما از toolsetها. |
| `--provider <provider>` | اجبار به یک ارائه‌دهنده: `auto`, `openrouter`, `nous`, `openai-codex`, `copilot-acp`, `copilot`, `anthropic`, `gemini`, `huggingface`, `novita` (نام مستعار `novita-ai`, `novitaai`), `openai-api`, `zai`, `kimi-coding`, `kimi-coding-cn`, `minimax`, `minimax-cn`, `minimax-oauth`, `kilocode`, `xiaomi`, `arcee`, `gmi`, `alibaba`, `alibaba-coding-plan` (نام مستعار `alibaba_coding`), `deepseek`, `nvidia`, `ollama-cloud`, `xai` (نام مستعار `grok`), `xai-oauth` (نام مستعار `grok-oauth`), `qwen-oauth`, `bedrock`, `opencode-zen`, `opencode-go`, `azure-foundry`, `lmstudio`, `stepfun`, `tencent-tokenhub` (نام مستعار `tencent`, `tokenhub`). |
| `-s`, `--skills <name>` | پیش‌بارگذاری یک یا چند مهارت برای نشست (قابل تکرار یا جداشده با کاما). |
| `-v`, `--verbose` | خروجی مفصل. |
| `-Q`, `--quiet` | حالت برنامه‌نویسی: سرکوب بنر/چرخنده/پیش‌نمایش ابزار. |
| `--image <path>` | متصل کردن یک تصویر محلی به یک پرامپت. |
| `--resume <session>`/`--continue [name]` | از سرگیری نشست مستقیماً از `chat`. |
| `--worktree` | ایجاد یک git worktree ایزوله برای این اجرا. |
| `--checkpoints` | فعال کردن checkpointهای فایل سیستم قبل از تغییرات فایلی مخرب. |
| `--yolo` | رد شدن از درخواستهای تأیید. |
| `--pass-session-id` | ارسال session ID به system prompt. |
| `--ignore-user-config` | نادیده گرفتن `~/.hermes/config.yaml` و استفاده از پیش‌فرض‌های داخلی. اعتبارنامه‌ها در `.env` همچنان بارگذاری می‌شوند. مفید برای اجراهای CI ایزوله، گزارش‌های خطای قابل تکرار و ادغام‌های شخص ثالث. |
| `--ignore-rules` | رد شدن از تزریق خودکار `AGENTS.md`، `SOUL.md`، `.cursorrules`، حافظه پایدار و مهارت‌های پیش‌بارگذاری شده. با `--ignore-user-config` ترکیب کنید برای اجرای کاملاً ایزوله. |
| `--safe-mode` | حالت عیب‌یابی: غیرفعال کردن همه سفارشی‌سازی‌ها — پیکربندی کاربر، تزریق قوانین/حافظه، pluginها، هوک‌های shell و سرورهای MCP (شامل `--ignore-user-config` و `--ignore-rules`). برای جدا کردن اینکه مشکل از راه‌اندازی شماست یا خود Hermes استفاده کنید. |
| `--source <tag>` | برچسب منبع نشست برای فیلتر کردن (پیش‌فرض: `cli`). از `tool` برای ادغام‌های شخص ثالث استفاده کنید که نباید در لیست نشست‌های کاربر ظاهر شوند. |
| `--max-turns <N>` | حداکثر تکرارهای فراخوانی ابزار به ازای هر نوبت مکالمه (پیش‌فرض: 90، یا `agent.max_turns` در پیکربندی). |

`-q`
`--query "..."`
`-m`
`--model <model>`
`-t`
`--toolsets <csv>`
`--provider <provider>`
`auto`
`openrouter`
`nous`
`openai-codex`
`copilot-acp`
`copilot`
`anthropic`
`gemini`
`huggingface`
`novita`
`novita-ai`
`novitaai`
`openai-api`
`zai`
`kimi-coding`
`kimi-coding-cn`
`minimax`
`minimax-cn`
`minimax-oauth`
`kilocode`
`xiaomi`
`arcee`
`gmi`
`alibaba`
`alibaba-coding-plan`
`alibaba_coding`
`deepseek`
`nvidia`
`ollama-cloud`
`xai`
`grok`
`xai-oauth`
`grok-oauth`
`qwen-oauth`
`bedrock`
`opencode-zen`
`opencode-go`
`azure-foundry`
`lmstudio`
`stepfun`
`tencent-tokenhub`
`tencent`
`tokenhub`
`-s`
`--skills <name>`
`-v`
`--verbose`
`-Q`
`--quiet`
`--image <path>`
`--resume <session>`
`--continue [name]`
`chat`
`--worktree`
`--checkpoints`
`--yolo`
`--pass-session-id`
`--ignore-user-config`
`~/.hermes/config.yaml`
`.env`
`--ignore-rules`
`AGENTS.md`
`SOUL.md`
`.cursorrules`
`--ignore-user-config`
`--safe-mode`
`--ignore-user-config`
`--ignore-rules`
`--source <tag>`
`cli`
`tool`
`--max-turns <N>`
`agent.max_turns`

مثال‌ها:

```
hermes
hermes chat -q "Summarize the latest PRs"
hermes chat --provider openrouter --model anthropic/claude-sonnet-4.6
hermes chat --toolsets web,terminal,skills
hermes chat --quiet -q "Return only JSON"
hermes chat --worktree -q "Review this repo and open a PR"
hermes chat --ignore-user-config --ignore-rules -q "Repro without my personal setup"
hermes chat --safe-mode -q "Is this bug mine or Hermes'?"
```

### `hermes -z <prompt>` — یکباره اسکریپتی​

`hermes -z <prompt>`

برای فراخوانندگان برنامه‌نویسی (اسکریپت‌های shell، CI، cron، فرآیندهای والد که پرامپت را لوله می‌کنند)، `hermes -z` خالص‌ترین نقطه ورود یکباره است: پرامپت واحد وارد، متن پاسخ نهایی خارج، چیز دیگری در stdout یا stderr نیست. بدون بنر، بدون چرخنده، بدون پیش‌نمایش ابزار، بدون خط `Session:` — فقط پاسخ نهایی agent به صورت متن ساده.

`hermes -z`
`Session:`

```
hermes -z "What's the capital of France?"
# → Paris.
# Parent scripts can cleanly capture the response:
answer=$(hermes -z "summarize this" < /path/to/file.txt)
```

بازنویسی‌های به ازای هر اجرا (بدون تغییر به `~/.hermes/config.yaml`):

`~/.hermes/config.yaml`

| پرچم | متغیر env معادل | هدف |
| --- | --- | --- |
| `-m`/`--model <model>` | `HERMES_INFERENCE_MODEL` | Override کردن مدل برای این اجرا |
| `--provider <provider>` | (هیچ) | Override کردن ارائه‌دهنده برای این اجرا |

`-m`
`--model <model>`
`HERMES_INFERENCE_MODEL`
`--provider <provider>`

```
hermes -z "…" --provider openrouter --model openai/gpt-5.5
# or:
HERMES_INFERENCE_MODEL=anthropic/claude-sonnet-4.6 hermes -z "…"
```

همان agent، همان ابزارها، همان مهارت‌ها — فقط همه لایه‌های تعاملی/زیبایی‌شناختی حذف شده‌اند. اگر خروجی ابزار را هم در رونویسی می‌خواهید، از `hermes chat -q` استفاده کنید؛ `-z` صریحاً برای «فقط پاسخ نهایی را می‌خواهم» است.

`hermes chat -q`
`-z`

## `hermes model`​

`hermes model`

انتخابگر تعاملی ارائه‌دهنده + مدل. این دستور برای اضافه کردن ارائه‌دهندگان جدید، تنظیم کلیدهای API و اجرای فلوهای OAuth است. آن را از ترمینال خود اجرا کنید — نه از داخل یک نشست چت فعال Hermes.

```
hermes model
```

از این استفاده کنید وقتی می‌خواهید:

- ارائه‌دهنده جدید اضافه کنید (OpenRouter، Anthropic، Copilot، DeepSeek، سفارشی و غیره)
- به ارائه‌دهندگان OAuth وارد شوید (Anthropic، Copilot، Codex، Nous Portal)
- کلیدهای API را وارد یا به‌روزرسانی کنید
- از لیست‌های مدل اختصاصی ارائه‌دهنده انتخاب کنید
- یک endpoint سفارشی/میزبانی‌شده پیکربندی کنید
- مقدار پیش‌فرض جدید را در پیکربندی ذخیره کنید

`hermes model` (از ترمینال خود، خارج از هر نشست Hermes) **ویزار کامل راه‌اندازی ارائه‌دهنده** است. می‌تواند ارائه‌دهندگان جدید اضافه کند، فلوهای OAuth اجرا کند، برای کلیدهای API درخواست کند و endpointها را پیکربندی کند.

`hermes model`

`/model` (تایپ شده داخل یک نشست چت فعال Hermes) فقط می‌تواند بین ارائه‌دهندگان و مدل‌هایی که قبلاً راه‌اندازی کرده‌اید جابجا شود. نمی‌تواند ارائه‌دهندگان جدید اضافه کند، OAuth اجرا کند یا برای کلیدهای API درخواست کند.

`/model`

اگر به اضافه کردن ارائه‌دهنده جدید نیاز دارید: ابتدا نشست Hermes خود را ترک کنید (`Ctrl+C` یا `/quit`)، سپس `hermes model` را از پرامپت ترمینال خود اجرا کنید.

`Ctrl+C`
`/quit`
`hermes model`

### دستور اسلش `/model` (وسط نشست)​

`/model`

بین مدل‌های قبلاً پیکربندی شده بدون ترک نشست جابجا شوید:

```
/model                              # Show current model and available options
/model claude-sonnet-4              # Switch model (auto-detects provider)
/model zai:glm-5                    # Switch provider and model
/model custom:qwen-2.5              # Use model on your custom endpoint
/model custom                       # Auto-detect model from custom endpoint
/model custom:local:qwen-2.5        # Use a named custom provider
/model openrouter:anthropic/claude-sonnet-4  # Switch back to cloud
```

به طور پیش‌فرض، تغییرات `/model` فقط روی **نشست فعلی** اعمال می‌شوند. `--global` را اضافه کنید تا تغییر را در `config.yaml` ذخیره کنید:

`/model`
`--global`
`config.yaml`

```
/model claude-sonnet-4 --global     # Switch and save as new default
```

اگر فقط OpenRouter را پیکربندی کرده‌اید، `/model` فقط مدل‌های OpenRouter را نشان خواهد داد. برای اضافه کردن ارائه‌دهنده دیگر (Anthropic، DeepSeek، Copilot و غیره)، نشست خود را ترک کنید و `hermes model` را از ترمینال اجرا کنید.

`/model`
`hermes model`

تغییرات ارائه‌دهنده و base URL به طور خودکار در `config.yaml` ذخیره می‌شوند. هنگام جابجایی از یک endpoint سفارشی، base URL منقضی شده پاک می‌شود تا از نشت آن به ارائه‌دهندگان دیگر جلوگیری شود.

`config.yaml`

## `hermes gateway`​

`hermes gateway`

```
hermes gateway <subcommand>
```

دستورات زیر سطح:

| دستور زیر سطح | توضیح |
| --- | --- |
| `run` | اجرای گیت‌وی در حالت foreground. توصیه شده برای WSL، Docker و Termux. |
| `start` | شروع سرویس پس‌زمینه systemd/launchd نصب شده. |
| `stop` | توقف سرویس (یا فرآیند foreground). |
| `restart` | راه‌اندازی مجدد سرویس. |
| `status` | نمایش وضعیت سرویس. |
| `list` | فهرست همه پروفایل‌ها و اینکه آیا گیت‌وی هر پروفایل در حال اجراست (با PID در صورت وجود). مفید وقتی چند پروفایل را کنار هم اجرا می‌کنید و یک نمای کلی می‌خواهید. |
| `install` | نصب به عنوان سرویس پس‌زمینه systemd (Linux) یا launchd (macOS). |
| `uninstall` | حذف سرویس نصب شده. |
| `setup` | راه‌اندازی تعاملی پلتفرم پیام‌رسانی. |
| `migrate-legacy` | حذف واحدهای `hermes.service` قدیمی باقی‌مانده از نصب‌های قبل از تغییر نام. واحدهای پروفایل (`hermes-gateway-<profile>.service`) و سرویس‌های نامرتبط هرگز لمس نمی‌شوند. پرچم‌ها: `--dry-run`، `-y`/`--yes`. |
| `enroll` | آزمایشی: ثبت این گیت‌وی با یک رله‌کننده و ذخیره اعتبارنامه‌های رله برای پلتفرم‌های پشتیبانی شده توسط رله‌کننده. |

`run`
`start`
`stop`
`restart`
`status`
`list`
`install`
`uninstall`
`setup`
`migrate-legacy`
`hermes.service`
`hermes-gateway-<profile>.service`
`--dry-run`
`-y`
`--yes`
`enroll`

گزینه‌ها:

| گزینه | توضیح |
| --- | --- |
| `--all` | در `start`/`restart`/`stop`: روی گیت‌وی **هر** پروفایل عمل کنید، نه فقط `HERMES_HOME` فعال. مفید وقتی چند پروفایل را کنار هم اجرا می‌کنید و می‌خواهید همه را پس از `hermes update` راه‌اندازی مجدد کنید. |
| `--no-supervise` | در `run`: در تصویر Docker s6-overlay، از نظارت خودکار انصراف دهید و از معنای foreground قبل از s6 استفاده کنید — گیت‌وی به عنوان فرآیند اصلی کانتینر بدون راه‌اندازی مجدد خودکار اجرا می‌شود. خارج از تصویر s6 بی‌اثر است. معادل تنظیم `HERMES_GATEWAY_NO_SUPERVISE=1`. |

`--all`
`start`
`restart`
`stop`
`HERMES_HOME`
`hermes update`
`--no-supervise`
`run`
`HERMES_GATEWAY_NO_SUPERVISE=1`

`hermes gateway enroll` پرچم‌های `--token`، `--connector-url`، `--gateway-id` و `--wake-url` را می‌پذیرد. توکن ثبت را با رله‌کننده مبادله می‌کند و مقادیر `GATEWAY_RELAY_ID`، `GATEWAY_RELAY_SECRET`، `GATEWAY_RELAY_DELIVERY_KEY`، اختیاری `GATEWAY_RELAY_URL` و (وقتی `--wake-url` داده شود) `GATEWAY_RELAY_WAKE_URL` را در `.env` پروفایل فعال می‌نویسد.

`hermes gateway enroll`
`--token`
`--connector-url`
`--gateway-id`
`--wake-url`
`GATEWAY_RELAY_ID`
`GATEWAY_RELAY_SECRET`
`GATEWAY_RELAY_DELIVERY_KEY`
`GATEWAY_RELAY_URL`
`--wake-url`
`GATEWAY_RELAY_WAKE_URL`
`.env`

از `hermes gateway run` به جای `hermes gateway start` استفاده کنید — پشتیبانی systemd WSL غیرقابل اعتماد است. آن را در tmux برای پایداری بپیچید: `tmux new -s hermes 'hermes gateway run'`. برای جزئیات به [WSL FAQ](/docs/reference/faq#wsl-gateway-keeps-disconnecting-or-hermes-gateway-start-fails) مراجعه کنید.

`hermes gateway run`
`hermes gateway start`
`tmux new -s hermes 'hermes gateway run'`

## `hermes lsp`​

`hermes lsp`

```
hermes lsp <subcommand>
```

مدیریت ادغام Language Server Protocol. LSP سرورهای واقعی زبان (pyright، gopls، rust-analyzer، …) را در پس‌زمینه اجرا می‌کند و تشخیص‌های آنها را به بررسی پس از نوشتن که توسط `write_file` و `patch` استفاده می‌شود تغذیه می‌کند. مبتنی بر تشخیص فضای کاری git است — LSP فقط وقتی اجرا می‌شود که cwd یا فایل ویرایش شده داخل یک git worktree باشد.

`write_file`
`patch`

دستورات زیر سطح:

| دستور زیر سطح | توضیح |
| --- | --- |
| `status` | نمایش وضعیت سرویس، سرورهای پیکربندی شده، وضعیت نصب. |
| `list` | چاپ رجیستری سرورهای پشتیبانی شده. `--installed-only` برای رد کردن گم‌شده‌ها. |
| `install <id>` | نصب اشتیاقی باینری یک سرور. |
| `install-all` | نصب هر سرور با دستورالعمل نصب خودکار شناخته شده. |
| `restart` | برچیدن کلاینت‌های در حال اجرا تا ویرایش بعدی دوباره ایجاد کند. |
| `which <id>` | چاپ مسیر باینری حل شده برای یک سرور. |

`status`
`list`
`--installed-only`
`install <id>`
`install-all`
`restart`
`which <id>`

برای راهنمای کامل، زبان‌های پشتیبانی شده و گزینه‌های پیکربندی به [LSP — Semantic Diagnostics](/docs/user-guide/features/lsp/) مراجعه کنید.

## `hermes setup`​

`hermes setup`

```
hermes setup [model|tts|terminal|gateway|tools|agent] [--non-interactive] [--reset] [--quick] [--reconfigure] [--portal]
```

آسان‌ترین مسیر: `hermes setup --portal` — ورود OAuth به Nous Portal و فعال کردن [Tool Gateway](/docs/user-guide/features/tool-gateway/) در یک ضربه.

`hermes setup --portal`

**اولین اجرا:** ویزار اولین بار راه‌اندازی می‌کند.

**کاربر بازگشتی (قبلاً پیکربندی شده):** مستقیماً به ویزار بازپیکربندی کامل می‌افتد — هر درخواست مقدار فعلی شما را به عنوان پیش‌فرض نشان می‌دهد، Enter را فشار دهید تا نگه دارید یا مقدار جدید تایپ کنید. بدون منو.

رفتن به یک بخش به جای ویزار کامل:

| بخش | توضیح |
| --- | --- |
| `model` | راه‌اندازی ارائه‌دهنده و مدل. |
| `terminal` | راه‌اندازی backend ترمینال و sandbox. |
| `gateway` | راه‌اندازی پلتفرم پیام‌رسانی. |
| `tools` | فعال/غیرفعال کردن ابزارها به ازای هر پلتفرم. |
| `agent` | تنظیمات رفتار agent. |

`model`
`terminal`
`gateway`
`tools`
`agent`

گزینه‌ها:

| گزینه | توضیح |
| --- | --- |
| `--quick` | در اجراهای کاربر بازگشتی: فقط برای آیتم‌هایی درخواست کنید که گم‌شده یا تنظیم نشده‌اند. آیتم‌هایی که قبلاً پیکربندی کرده‌اید را رد کنید. |
| `--non-interactive` | استفاده از پیش‌فرض‌ها/مقادیر محیطی بدون درخواست. |
| `--reset` | بازنشانی پیکربندی به پیش‌فرض‌ها قبل از راه‌اندازی. |
| `--reconfigure` | نام مستعار سازگاری معکوس — `hermes setup` بدون پرچم روی یک نصب موجود اکنون به طور پیش‌فرض این کار را انجام می‌دهد. |
| `--portal` | راه‌اندازی یکباره Nous Portal: ورود از طریق OAuth، تنظیم Nous به عنوان ارائه‌دهنده inference و فعال کردن Tool Gateway. بقیه ویزار را رد می‌کند. |

`--quick`
`--non-interactive`
`--reset`
`--reconfigure`
`hermes setup`
`--portal`

## `hermes portal`​

`hermes portal`

```
hermes portal [status|open|tools]
```

بررسی auth Nous Portal، مسیریابی Tool Gateway و دسترسی به صفحه اشتراک. فراخوانی بدون دستور زیر سطح `status` را اجرا می‌کند.

`status`

| دستور زیر سطح | توضیح |
| --- | --- |
| `status` (پیش‌فرض) | وضعیت auth Portal + خلاصه مسیریابی Tool Gateway به ازای هر ابزار. همچنین وقتی دستور زیر سطحی داده نشده نمایش داده می‌شود. |
| `open` | باز کردن `portal.nousresearch.com/manage-subscription` در مرورگر پیش‌فرض شما. |
| `tools` | فهرست همه شرکای Tool Gateway (Firecrawl، FAL، OpenAI TTS، Browser Use، Modal) و اینکه کدامها از طریق Nous مسیریابی می‌شوند. |

`status`
`open`
`portal.nousresearch.com/manage-subscription`
`tools`

برای پیکربندی خود گیت‌وی، به [Tool Gateway](/docs/user-guide/features/tool-gateway/) مراجعه کنید. برای مسیر راه‌اندازی یکباره، به `hermes setup --portal` بالا مراجعه کنید.

## `hermes whatsapp`​

`hermes whatsapp`

```
hermes whatsapp
```

اجرای فلوی جفت‌سازی/راه‌اندازی WhatsApp، شامل انتخاب حالت و جفت‌سازی QR code.

## `hermes slack`​

`hermes slack`

```
hermes slack manifest              # print manifest to stdout
hermes slack manifest --write      # write to ~/.hermes/slack-manifest.json
hermes slack manifest --slashes-only  # just the features.slash_commands array
```

یک manifest برنامه Slack تولید می‌کند که هر دستور گیت‌وی در `COMMAND_REGISTRY` (`/btw`، `/stop`، `/model`، …) را به عنوان یک دستور اسلش Slack درجه یک ثبت می‌کند — مطابقت با Discord و Telegram. خروجی را در پیکربندی برنامه Slack خود در [https://api.slack.com/apps](https://api.scalk.com/apps) → برنامه شما → Features → App Manifest → Edit و سپس Save بچسبانید. Slack اگر scopeها یا دستورات اسلش تغییر کرده باشند برای نصب مجدد درخواست می‌کند.

`COMMAND_REGISTRY`
`/btw`
`/stop`
`/model`
[https://api.slack.com/apps](https://api.slack.com/apps)

| پرچم | پیش‌فرض | هدف |
| --- | --- | --- |
| `--write [PATH]` | stdout | نوشتن در فایل به جای stdout. `--write` بدون مسیر `$HERMES_HOME/slack-manifest.json` می‌نویسد. |
| `--name NAME` | Hermes | نام نمایشی ربات در Slack. |
| `--description DESC` | توصیف پیش‌فرض | توصیف ربات نمایش داده شده در فهرست برنامه Slack. |
| `--slashes-only` | off | فقط `features.slash_commands` برای ادغام در manifest دستی خارج کردن. |

`--write [PATH]`
`--write`
`$HERMES_HOME/slack-manifest.json`
`--name NAME`
`Hermes`
`--description DESC`
`--slashes-only`
`features.slash_commands`

پس از `hermes update` مجدداً `hermes slack manifest --write` را اجرا کنید تا دستورات جدید انتخاب شوند.

`hermes slack manifest --write`
`hermes update`

## `hermes send`​

`hermes send`

```
hermes send --to <target> "message text"
hermes send --to <target> --file <path>
echo "message" | hermes send --to <target>
hermes send --list [platform]
```

ارسال یک پیام یکباره به یک پلتفرم پیام‌رسانی پیکربندی شده بدون راه‌اندازی حلقه agent یا گیت‌وی. از اعتبارنامه‌های قبلاً پیکربندی شده گیت‌وی (`~/.hermes/.env` + `~/.hermes/config.yaml`) استفاده مجدد می‌کند بنابراین اسکریپت‌های ops، تسک‌های cron، هوک‌های CI و دیمن‌های پایش می‌توانند به‌روزرسانی‌های وضعیت ارسال کنند بدون پیاده‌سازی مجدد REST client هر پلتفرم.

`~/.hermes/.env`
`~/.hermes/config.yaml`

برای پلتفرم‌های مبتنی بر توکن ربات (Telegram، Discord، Slack، Signal، SMS، WhatsApp-CloudAPI) نیازی به گیت‌وی در حال اجرا نیست — `hermes send` مستقیماً با endpoint REST پلتفرم صحبت می‌کند. پلتفرم‌های plugin که به آداپتور پایدار نیاز دارند همچنان به گیت‌وی زنده نیاز دارند.

`hermes send`

| گزینه | توضیح |
| --- | --- |
| `-t`, `--to <TARGET>` | هدف تحویل. قالب‌ها: `platform` (از کانال خانه استفاده می‌کند)، `platform:chat_id`، `platform:chat_id:thread_id` یا `platform:#channel-name`. مثال‌ها: `telegram`، `telegram:-1001234567890`، `discord:#ops`، `slack:C0123ABCD`، `signal:+155****4567`. |
| `-f`, `--file <PATH>` | خواندن بدنه پیام از `PATH` (فقط فایل‌های متنی — لاگ‌ها، گزارش‌ها، markdown). `-` برای اجبار خواندن از stdin. برای ارسال تصویر یا فایل باینری دیگر، از `MEDIA:<path>` استفاده کنید (پایین را ببینید). |
| `-s`, `--subject <LINE>` | اضافه کردن خط عنوان/موضوع قبل از بدنه پیام. |
| `-l`, `--list [platform]` | فهرست اهداف پیکربندی شده در همه پلتفرم‌ها (یا فقط پلتفرم داده شده). |
| `-q`, `--quiet` | سرکوب stdout در موفقیت — مفید در اسکریپت‌ها (فقط به کد خروجی اعتماد کنید). |
| `--json` | خروجی JSON خام به جای خروجی خوانا. |

`-t`
`--to <TARGET>`
`platform`
`platform:chat_id`
`platform:chat_id:thread_id`
`platform:#channel-name`
`telegram`
`telegram:-1001234567890`
`discord:#ops`
`slack:C0123ABCD`
`signal:+155****4567`
`-f`
`--file <PATH>`
`PATH`
`-`
`MEDIA:<path>`
`-s`
`--subject <LINE>`
`-l`
`--list [platform]`
`-q`
`--quiet`
`--json`

اگر نه آرگومان موقعیتی `message` و نه `--file` ارائه شود، `hermes send` وقتی TTY نیست از stdin می‌خواند. کدهای خروج: `0` در موفقیت، `1` در خرابی تحویل/backend، `2` در خطاهای استفاده.

`message`
`--file`
`hermes send`
`0`
`1`
`2`

### ارسال تصاویر و رسانه دیگر​

`--file` فقط برای بدنه‌های **متنی** است. برای تحویل یک تصویر، سند، ویدیو یا فایل صوتی به عنوان پیوست بومی پلتفرم، آن را در متن پیام با دستور `MEDIA:<local_path>` ارجاع دهید:

`--file`
`MEDIA:<local_path>`

```
hermes send --to telegram "MEDIA:/tmp/screenshot.png"
hermes send --to telegram "Build chart for today MEDIA:/tmp/chart.png"   # with caption
hermes send --to discord:#ops "MEDIA:/tmp/report.pdf"
```

به طور پیش‌فرض، فایل‌های تصویر به عنوان عکس ارسال می‌شوند (پلتفرم‌هایی مانند Telegram آنها را مجدداً فشرده می‌کنند). `[[as_document]]` را به پیام اضافه کنید تا به جای آن به عنوان پیوست فایل فشرده‌نشده تحویل داده شوند:

`[[as_document]]`

```
hermes send --to telegram "[[as_document]] MEDIA:/tmp/screenshot.png"
```

مثال‌ها:

```
hermes send --to telegram "deploy finished"
echo "RAM 92%" | hermes send --to telegram:-1001234567890
hermes send --to discord:#ops --file /tmp/report.md
hermes send --to slack:#eng --subject "[CI]" --file build.log
hermes send --list                  # all platforms
hermes send --list telegram         # filter by platform
```

## `hermes secrets`​

`hermes secrets`

```
hermes secrets bitwarden <subcommand>
hermes secrets bw <subcommand>          # short alias
```

کشیدن کلیدهای API از یک مدیر secret خارجی در شروع فرآیند به جای ذخیره آنها در `~/.hermes/.env`. در حال حاضر از [Bitwarden Secrets Manager](/docs/user-guide/secrets/bitwarden/) پشتیبانی می‌کند.

`~/.hermes/.env`

دستورات زیر سطح `bitwarden` (نام مستعار `bw`):

`bitwarden`
`bw`

| دستور زیر سطح | توضیح |
| --- | --- |
| `setup` | ویزار تعاملی: نصب باینری `bws` ثابت شده، ذخیره توکن دسترسی و انتخاب پروژه. `--project-id`، `--access-token` و `--server-url` برای استفاده غیرتعاملی می‌پذیرد. |
| `status` | نمایش پیکربندی فعلی، مسیر/نسخه باینری و اطلاعات آخرین کشیدن. |
| `sync` | کشیدن secretها اکنون و گزارش تغییرات. `--apply` برای خروجی واقعی secretها در محیط shell فعلی (پیش‌فرض dry-run است). |
| `install` | دانلود و بررسی باینری `bws` ثابت شده. `--force` حتی اگر نسخه مدیریت شده موجود است دوباره دانلود می‌کند. |
| `disable` | خاموش کردن ادغام Bitwarden. |

`setup`
`bws`
`--project-id`
`--access-token`
`--server-url`
`status`
`sync`
`--apply`
`install`
`bws`
`--force`
`disable`

## `hermes migrate`​

`hermes migrate`

```
hermes migrate <type>
```

تشخیص و (اختیاری) بازنویسی `config.yaml` فعال برای جایگزینی ارجاعات به مدل‌های بازنشسته یا تنظیمات منسوخ. یک نسخه پشتیبان با تمبر زمانی از `config.yaml` اصلی قبل از هر بازنویسی گرفته می‌شود (با `--no-backup` رد شوید).

`config.yaml`
`config.yaml`
`--no-backup`

| دستور زیر سطح | توضیح |
| --- | --- |
| `xai` | اسکن `config.yaml` برای ارجاعات به مدل‌های xAI برنامه‌ریزی شده برای بازنشستگی در ۱۵ مه ۲۰۲۶ و (با `--apply`) بازنویسی آنها در جا به جایگزین‌های رسمی طبق راهنمای مهاجرت xAI. پیش‌فرض dry-run. |

`xai`
`config.yaml`
`--apply`

پرچم‌های رایج برای دستورات زیر سطح مهاجرت:

| پرچم | توضیح |
| --- | --- |
| `--apply` | بازنویسی `config.yaml` در جا (پیش‌فرض: dry-run، بدون نوشتن). |
| `--no-backup` | رد کردن نسخه پشتیبان با تمبر زمانی `config.yaml` هنگام اعمال. |

`--apply`
`config.yaml`
`--no-backup`
`config.yaml`

> با `hermes claw migrate` اشتباه گرفته نشود (واردات یکباره پیکربندی OpenClaw به Hermes) — `hermes migrate` دستور بازنویسی پیکربندی سطح بالا است.

`hermes claw migrate`
`hermes migrate`

## `hermes proxy`​

`hermes proxy`

```
hermes proxy <subcommand>
```

اجرای یک سرور HTTP محلی سازگار با OpenAI که درخواست‌ها را به یک ارائه‌دهنده upstream احراز هویت شده با OAuth (مثلاً Nous Portal، xAI) ارسال می‌کند. برنامه‌های خارجی می‌توانند با هر bearer token به پروکسی اشاره کنند؛ پروکسی اعتبارنامه‌های واقعی OAuth شما را در خروجی متصل می‌کند. برای راهنمای کامل به [Subscription Proxy](/docs/user-guide/features/subscription-proxy/) مراجعه کنید.

| دستور زیر سطح | توضیح |
| --- | --- |
| `start` | اجرای پروکسی در حالت foreground. پرچم‌ها: `--provider <nous\|xai>` (پیش‌فرض `nous`)، `--host <addr>` (پیش‌فرض `127.0.0.1`؛ از `0.0.0.0` برای نمایانی در LAN استفاده کنید)، `--port <int>` (پیش‌فرض `8645`). |
| `status` | نمایش اینکه کدام upstreamهای پروکسی آماده هستند (اعتبارنامه‌ها موجود، OAuth معتبر). |
| `providers` | فهرست ارائه‌دهندگان upstream پروکسی موجود. |

`start`
`--provider <nous|xai>`
`nous`
`--host <addr>`
`127.0.0.1`
`0.0.0.0`
`--port <int>`
`8645`
`status`
`providers`

## `hermes security`​

`hermes security`

```
hermes security <subcommand>
```

اسکن آسیب‌پذیری on-demand علیه [OSV.dev](https://osv.dev). شامل venv Hermes (توزیع‌های نصب شده PyPI)، وابستگی‌های پایتونی اعلام شده توسط pluginها زیر `~/.hermes/plugins/` و سرورهای MCP `npx`/`uvx` ثابت شده در `config.yaml` است. بسته‌های نصب شده به صورت جهانی یا extensionهای ویرایشگر/مرورگر را اسکن **نمی‌کند**.

`~/.hermes/plugins/`
`npx`
`uvx`
`config.yaml`

| دستور زیر سطح | توضیح |
| --- | --- |
| `audit` | اجرای یک ممیزی زنجیره تأمین یکباره. |

پرچم‌های `audit`:

`audit`

| پرچم | پیش‌فرض | توضیح |
| --- | --- | --- |
| `--json` | off | خروجی JSON خوانا توسط ماشین به جای متن خوانا توسط انسان. |
| `--fail-on <level>` | critical | خروج با مقدار ناصفر وقتی هر یافته‌ای با این شدت مطابقت دارد (`low`، `moderate`، `high`، `critical`). |
| `--skip-venv` | off | رد کردن اسکن venv پایتونی Hermes. |
| `--skip-plugins` | off | رد کردن اسکن فایل‌های plugin requirements. |
| `--skip-mcp` | off | رد کردن اسکن سرورهای MCP ثابت شده در `config.yaml`. |

`--json`
`--fail-on <level>`
`critical`
`low`
`moderate`
`high`
`critical`
`--skip-venv`
`--skip-plugins`
`--skip-mcp`
`config.yaml`

## `hermes login`/`hermes logout` (منسوخ)​

`hermes login`
`hermes logout`

`hermes login` حذف شده است. از `hermes auth` برای مدیریت اعتبارنامه‌های OAuth، `hermes model` برای انتخاب ارائه‌دهنده یا `hermes setup` برای راه‌اندازی تعاملی کامل استفاده کنید.

`hermes login`
`hermes auth`
`hermes model`
`hermes setup`

## `hermes auth`​

`hermes auth`

مدیریت استخرهای اعتبارنامه برای چرخش کلید هم‌ارائه‌دهنده. برای مستندات کامل به [Credential Pools](/docs/user-guide/features/credential-pools/) مراجعه کنید.

```
hermes auth                                              # Interactive wizard
hermes auth list                                         # Show all pools
hermes auth list openrouter                              # Show specific provider
hermes auth add openrouter --api-key sk-or-v1-xxx        # Add API key
hermes auth add anthropic --type oauth                   # Add OAuth credential
hermes auth remove openrouter 2                          # Remove by index
hermes auth reset openrouter                             # Clear cooldowns
hermes auth status anthropic                             # Show auth status for a provider
hermes auth logout anthropic                             # Log out and clear stored auth state
hermes auth spotify                                      # Authenticate Hermes with Spotify via PKCE
```

دستورات زیر سطح: `add`، `list`، `remove`، `reset`، `status`، `logout`، `spotify`. هنگام فراخوانی بدون دستور زیر سطح، ویزار مدیریت تعاملی راه‌اندازی می‌شود.

`add`
`list`
`remove`
`reset`
`status`
`logout`
`spotify`

## `hermes status`​

`hermes status`

```
hermes status [--all] [--deep]
```

| گزینه | توضیح |
| --- | --- |
| `--all` | نمایش همه جزئیات در قالب قابل اشتراک‌گذاری ویرایش شده. |
| `--deep` | اجرای بررسی‌های عمیق‌تر که ممکن است بیشتر طول بکشد. |

`--all`
`--deep`

## `hermes cron`​

`hermes cron`

```
hermes cron <list|create|edit|pause|resume|run|remove|status|tick>
```

| دستور زیر سطح | توضیح |
| --- | --- |
| `list` | نمایش تسک‌های زمان‌بندی شده. |
| `create`/`add` | ایجاد یک تسک زمان‌بندی شده از پرامپت، با اختیار پیوست کردن یک یا چند مهارت از طریق `--skill` تکراری. |
| `edit` | به‌روزرسانی زمان‌بندی، پرامپت، نام، تحویل، تعداد تکرار یا مهارت‌های پیوست شده تسک. از `--clear-skills`، `--add-skill` و `--remove-skill` پشتیبانی می‌کند. |
| `pause` | توقف یک تسک بدون حذف آن. |
| `resume` | از سرگیری یک تسک متوقف شده و محاسبه اجرای آینده بعدی آن. |
| `run` | فعال کردن یک تسک در تیک بعدی زمان‌بند. |
| `remove` | حذف یک تسک زمان‌بندی شده. |
| `status` | بررسی اینکه آیا زمان‌بند cron در حال اجراست. |
| `tick` | اجرای تسک‌های سررسید یک بار و خروج. |

`list`
`create`
`add`
`--skill`
`edit`
`--clear-skills`
`--add-skill`
`--remove-skill`
`pause`
`resume`
`run`
`remove`
`status`
`tick`

trigger قابل اتصال از طریق کلید پیکربندی `cron.provider` است. خالی (پیش‌فرض) از ticker داخلی درون‌فرآیندی استفاده می‌کند. آن را روی `chronos` (ارائه‌دهنده مدیریت شده NAS برای دروازه‌های میزبانی شده scale-to-zero) تنظیم کنید — از طریق کلیدهای `cron.chronos.*` (`portal_url`، `callback_url`، `expected_audience`، `nas_jwks_url`) پیکربندی می‌شود — یا یک ارائه‌دهنده سفارشی تحت `plugins/cron/<name>/` یا `$HERMES_HOME/plugins/<name>/` نام ببرید. ارائه‌دهنده ناشناخته یا غیرموجود به داخلی بازمی‌گردد، بنابراین cron هرگز بدون trigger باقی نمی‌ماند. به مستندات [cron internals](/docs/developer-guide/cron-internals#gateway-integration) مراجعه کنید.

`cron.provider`
`chronos`
`cron.chronos.*`
`portal_url`
`callback_url`
`expected_audience`
`nas_jwks_url`
`plugins/cron/<name>/`
`$HERMES_HOME/plugins/<name>/`

## `hermes kanban`​

`hermes kanban`

```
hermes kanban [--board <slug>] <action> [options]
```

تخته همکاری چندپروفایلی، چندپروژه‌ای. هر نصب می‌تواند تخته‌های متعددی میزبانی کند (یکی به ازای هر پروژه، repo یا حوزه)؛ هر تخته یک صف مستقل با پایگاه داده SQLite و scope dispatcher خود است. نصب‌های جدید با یک تخته به نام `start` شروع می‌شوند که پایگاه داده آن برای سازگاری معکوس `~/.hermes/kanban.db` است؛ تخته‌های اضافی در `~/.hermes/kanban/boards/<slug>/kanban.db` زندگی می‌کنند. dispatcher تعبیه شده در گیت‌وی هر تخته را در هر تیک جاروب می‌کند.

`default`
`~/.hermes/kanban.db`
`~/.hermes/kanban/boards/<slug>/kanban.db`

پرچم‌های جهانی (در همه اعمال زیر اعمال می‌شوند):

| پرچم | هدف |
| --- | --- |
| `--board <slug>` | عمل روی یک تخته خاص. پیش‌فرض تخته فعلی (تعیین شده توسط `hermes kanban boards switch`، متغیر env `HERMES_KANBAN_BOARD` یا `default`). |

`--board <slug>`
`hermes kanban boards switch`
`HERMES_KANBAN_BOARD`
`default`

این سطح انسان/اسکریپت‌نویسی است. کارگران agent که توسط dispatcher ایجاد می‌شوند تخته را از طریق یک ابزار اختصاصی `kanban_*` (`kanban_show`، `kanban_complete`، `kanban_block`، `kanban_create`، `kanban_link`، `kanban_comment`، `kanban_heartbeat`؛ پروفایل‌های orchestrator همچنین `kanban_list` و `kanban_unblock` را دریافت می‌کنند) به جای shell کردن به `hermes kanban` هدایت می‌کنند. کارگران `HERMES_KANBAN_BOARD` را در env خود ثابت دارند بنابراین از نظر فیزیکی نمی‌توانند تخته‌های دیگر را ببینند.

`kanban_*`
[toolset](/docs/user-guide/features/kanban#how-workers-interact-with-the-board)
`kanban_show`
`kanban_complete`
`kanban_block`
`kanban_create`
`kanban_link`
`kanban_comment`
`kanban_heartbeat`
`kanban_list`
`kanban_unblock`
`hermes kanban`
`HERMES_KANBAN_BOARD`

| عمل | هدف |
| --- | --- |
| `init` | ایجاد `kanban.db` اگر وجود ندارد. Idempotent. |
| `boards list`/`boards ls` | فهرست همه تخته‌ها با تعداد تسک‌ها. `--json`، `--all` (شامل آرشیو شده‌ها). |
| `boards create <slug>` | ایجاد تخته جدید. پرچم‌ها: `--name`، `--description`، `--icon`، `--color`، `--switch` (فعال کردن). Slug kebab-case است، به طور خودکار به حروف کوچک تبدیل می‌شود. |
| `boards switch <slug>`/`boards use` | ذخیره `<slug>` به عنوان تخته فعال (در `~/.hermes/kanban/current` می‌نویسد). |
| `boards show`/`boards current` | چاپ نام، مسیر پایگاه داده و تعداد تسک‌های تخته فعال فعلی. |
| `boards rename <slug> "<name>"` | تغییر نام نمایشی تخته. Slug غیرقابل تغییر است. |
| `boards rm <slug>` | آرشیو (پیش‌فرض) یا حذف سخت تخته. `--delete` مرحله آرشیو را رد می‌کند. تخته‌های آرشیو شده به `boards/_archived/<slug>-<ts>/` منتقل می‌شوند. برای `default` رد می‌شود. |
| `create "<title>"` | ایجاد تسک جدید روی تخته فعال. پرچم‌ها: `--body`، `--assignee`، `--parent` (تکرارپذیر)، `--workspace scratch\|worktree\|dir:<path>`، `--tenant`، `--priority`، `--triage`، `--idempotency-key`، `--max-runtime`، `--max-retries`، `--skill` (تکرارپذیر). |
| `list`/`ls` | فهرست تسک‌های روی تخته فعال. فیلتر با `--mine`، `--assignee`، `--status`، `--tenant`، `--archived`، `--json`. |
| `show <id>` | نمایش تسک با نظرات و رویدادها. `--json` برای خروجی ماشین. |
| `assign <id> <profile>` | اختصاص یا اختصاص مجدد. از `none` برای لغو اختصاص استفاده کنید. در حین اجرا رد می‌شود. |
| `link <parent> <child>` | اضافه کردن وابستگی. تشخیص چرخه. هر دو تسک باید روی یک تخته باشند. |
| `unlink <parent> <child>` | حذف وابستگی. |
| `claim <id>` | به صورت اتمیک یک تسک آماده را مطالبه کنید. مسیر فضای کاری حل شده را چاپ می‌کند. |
| `comment <id> "<text>"` | اضافه کردن نظر. کارگر بعدی که تسک را مطالبه می‌کند آن را به عنوان بخشی از پاسخ `kanban_show()` خود می‌خواند. |
| `complete <id>` | نشانه‌گذاری تسک تمام شده. پرچم‌ها: `--result`، `--summary`، `--metadata`. |
| `block <id> "<reason>"` | نشانه‌گذاری تسک مسدود شده برای ورود انسان. همچنین دلیل را به عنوان نظر اضافه می‌کند. |
| `schedule <id> "<reason>"` | پارک کردن کار time-delay/پیگیری در `scheduled` تا به عنوان مسدودکننده انسانی نمایش داده نشود. |
| `unblock <id>` | بازگرداندن تسک مسدود یا زمان‌بندی شده به حالت آماده (یا `todo` اگر وابستگی‌ها هنوز باز هستند). |
| `archive <id>` | مخفی کردن از لیست پیش‌فرض. `gc` فضاهای کاری scratch را حذف می‌کند. |
| `tail <id>` | دنبال کردن جریان رویدادهای تسک. |
| `dispatch` | یک نوبت dispatcher روی تخته فعال. پرچم‌ها: `--dry-run`، `--max N`، `--failure-limit N`، `--json`. |
| `context <id>` | چاپ context کاملی که یک کارگر می‌بیند (عنوان + بدنه + نتایج والد + نظرات). |
| `specify <id>`/`specify --all` | تبدیل تسک ستون triage به یک مشخصات مشخص (عنوان + بدنه با هدف، رویکرد، معیارهای پذیرش) از طریق LLM کمکی، سپس ارتقا به `todo`. پرچم‌ها: `--tenant` (`--all` را به یک tenant محدود می‌کند)، `--author`، `--json`. مدل را تحت `auxiliary.triage_specifier` در `config.yaml` پیکربندی کنید. |
| `decompose <id>`/`decompose --all` | تبدیل تسک ستون triage به یک گراف از تسک‌های فرزند مسیریابی شده به پروفایل‌های متخصص بر اساس توصیف. وقتی LLM تصمیم می‌گیرد تسک از fan-out سود نمی‌برد، به ارتقای سبک specify تک‌تسک بازمی‌گردد. همان پرچم‌های `specify`. مدل decomposer را تحت `auxiliary.kanban_decomposer` در `config.yaml` پیکربندی کنید؛ `kanban.orchestrator_profile` فقط کنترل می‌کند چه کسی مالک تسک root/orchestration پس از fan-out است. همچنین به طور خودکار در هر تیک dispatcher وقتی `kanban.auto_decompose: true` (پیش‌فرض) اجرا می‌شود. [Auto vs Manual orchestration](/docs/user-guide/features/kanban#auto-vs-manual-orchestration) را ببینید. |
| `gc` | حذف فضاهای کاری scratch برای تسک‌های آرشیو شده. |

`init`
`kanban.db`
`boards list`
`boards ls`
`--json`
`--all`
`boards create <slug>`
`--name`
`--description`
`--icon`
`--color`
`--switch`
`boards switch <slug>`
`boards use`
`<slug>`
`~/.hermes/kanban/current`
`boards show`
`boards current`
`boards rename <slug> "<name>"`
`boards rm <slug>`
`--delete`
`boards/_archived/<slug>-<ts>/`
`default`
`create "<title>"`
`--body`
`--assignee`
`--parent`
`--workspace scratch|worktree|dir:<path>`
`--tenant`
`--priority`
`--triage`
`--idempotency-key`
`--max-runtime`
`--max-retries`
`--skill`
`list`
`ls`
`--mine`
`--assignee`
`--status`
`--tenant`
`--archived`
`--json`
`show <id>`
`--json`
`assign <id> <profile>`
`none`
`link <parent> <child>`
`unlink <parent> <child>`
`claim <id>`
`comment <id> "<text>"`
`kanban_show()`
`complete <id>`
`--result`
`--summary`
`--metadata`
`block <id> "<reason>"`
`schedule <id> "<reason>"`
`scheduled`
`unblock <id>`
`todo`
`archive <id>`
`gc`
`tail <id>`
`dispatch`
`--dry-run`
`--max N`
`--failure-limit N`
`--json`
`context <id>`
`specify <id>`
`specify --all`
`todo`
`--tenant`
`--all`
`--author`
`--json`
`auxiliary.triage_specifier`
`config.yaml`
`decompose <id>`
`decompose --all`
`specify`
`auxiliary.kanban_decomposer`
`config.yaml`
`kanban.orchestrator_profile`
`kanban.auto_decompose: true`
[Auto vs Manual orchestration](/docs/user-guide/features/kanban#auto-vs-manual-orchestration)
`gc`

مثال‌ها:

```
# Create a second board and put a task on it without switching away.
hermes kanban boards create atm10-server --name "ATM10 Server" --icon 🎮
hermes kanban --board atm10-server create "Restart server" --assignee ops
# Switch the active board for subsequent calls.
hermes kanban boards switch atm10-server
hermes kanban list                  # shows atm10-server tasks
# Archive a board (recoverable) or hard-delete it.
hermes kanban boards rm atm10-server
hermes kanban boards rm atm10-server --delete
```

ترتیب حل تخته (بالاترین اولویت اول): پرچم `--board <slug>` → متغیر env `HERMES_KANBAN_BOARD` → فایل `~/.hermes/kanban/current` → `default`.

`--board <slug>`
`HERMES_KANBAN_BOARD`
`~/.hermes/kanban/current`
`default`

همه اعمال همچنین به عنوان دستور اسلش در گیت‌وی (`/kanban …`) با همان سطح آرگومان در دسترس هستند — شامل دستورات زیر سطح `boards` و پرچم `--board`.

`/kanban …`
`boards`
`--board`

برای طراحی کامل — مقایسه با Cline Kanban / Paperclip / NanoClaw / Gemini Enterprise، هشت الگوی همکاری، چهار داستان کاربر، اثبات صحت همزمانی — به `docs/hermes-kanban-v1-spec.pdf` در مخزن یا [راهنمای کاربر Kanban](/docs/user-guide/features/kanban/) مراجعه کنید.

`docs/hermes-kanban-v1-spec.pdf`

## `hermes project`​

`hermes project`

```
hermes project <create|list|show|add-folder|remove-folder|rename|set-primary|use|archive|restore|bind-board>
```

پروژه‌ها فضاهای کاری نام‌گذاری شده توسط انسان هستند که می‌توانند چندین پوشه/rep را در بر بگیرند. گروه‌بندی نشست دسکتاپ را لنگر می‌اندازند و وقتی به تخته kanban متصل هستند، قرارداد worktree + branch تعیین‌شده به تسک‌ها می‌دهند. وضعیت به ازای هر پروفایل است.

| دستور زیر سطح | توضیح |
| --- | --- |
| `create` | ایجاد پروژه جدید. |
| `list` (نام مستعار `ls`) | فهرست پروژه‌ها. |
| `show` | نمایش جزئیات پروژه. |
| `add-folder` | اضافه کردن پوشه/rep به پروژه. |
| `remove-folder` | حذف پوشه از پروژه. |
| `rename` | تغییر نام پروژه. |
| `set-primary` | تنظیم پوشه اصلی. |
| `use` | تنظیم پروژه فعال. |
| `archive` | آرشیو کردن پروژه (قابل بازیابی). |
| `restore` | بازیابی پروژه آرشیو شده. |
| `bind-board` | متصل کردن تخته kanban به این پروژه. |

`create`
`list`
`ls`
`show`
`add-folder`
`remove-folder`
`rename`
`set-primary`
`use`
`archive`
`restore`
`bind-board`

## `hermes webhook`​

`hermes webhook`

```
hermes webhook <subscribe|list|remove|test>
```

مدیریت اشتراک‌های webhook پویا برای فعال‌سازی agent مبتنی بر رویداد. نیاز به فعال بودن پلتفرم webhook در پیکربندی دارد — اگر پیکربندی نشده، دستورالعمل راه‌اندازی چاپ می‌شود.

| دستور زیر سطح | توضیح |
| --- | --- |
| `subscribe`/`add` | ایجاد مسیر webhook. URL و secret HMAC برای پیکربندی در سرویس شما برمی‌گرداند. |
| `list`/`ls` | نمایش همه اشتراک‌های ایجاد شده توسط agent. |
| `remove`/`rm` | حذف یک اشتراک پویا. مسیرهای ثابت از `config.yaml` تحت تأثیر قرار نمی‌گیرند. |
| `test` | ارسال یک POST آزمایشی برای بررسی کارکرد اشتراک. |

`subscribe`
`add`
`list`
`ls`
`remove`
`rm`
`test`

### `hermes webhook subscribe`​

`hermes webhook subscribe`

```
hermes webhook subscribe <name> [options]
```

| گزینه | توضیح |
| --- | --- |
| `--prompt` | الگوی پرامپت با ارجاعات payload `{dot.notation}`. |
| `--events` | انواع رویداد جداشده با کاما برای پذیرش (مثلاً `issues`, `pull_request`). خالی = همه. |
| `--description` | توصیف خوانا توسط انسان. |
| `--skills` | نام مهارت‌های جداشده با کاما برای بارگذاری برای اجرای agent. |
| `--deliver` | هدف تحویل: `log` (پیش‌فرض)، `telegram`، `discord`، `slack`، `github_comment`. |
| `--deliver-chat-id` | شناسه چت/کانال هدف برای تحویل بین‌پلتفرمی. |
| `--secret` | secret HMAC سفارشی. اگر حذف شود به طور خودکار تولید می‌شود. |
| `--deliver-only` | رد کردن agent — تحویل `--prompt` رندر شده به عنوان پیام تحت الفظی. هزینه LLM صفر، تحویل زیر ثانیه. نیاز دارد `--deliver` یک هدف واقعی باشد (نه `log`). |
| `--script` | اسکریپت فیلتر/تبدیل تحت `~/.hermes/scripts/`. payload webhook به عنوان JSON در stdin ارسال می‌شود؛ stdout JSON payload را جایگزین می‌کند و stdout خالی، `[SILENT]` یا کد خروجی ناصفر webhook را نادیده می‌گیرد. به [Script Filters and Transforms](/docs/user-guide/messaging/webhooks#script-filters-and-transforms) مراجعه کنید. |

`--prompt`
`{dot.notation}`
`--events`
`issues,pull_request`
`--description`
`--skills`
`--deliver`
`log`
`telegram`
`discord`
`slack`
`github_comment`
`--deliver-chat-id`
`--secret`
`--deliver-only`
`--prompt`
`--deliver`
`log`
`--script`
`~/.hermes/scripts/`
`[SILENT]`

اشتراک‌ها در `~/.hermes/webhook_subscriptions.json` ذخیره می‌شوند و توسط آداپتور webhook بدون راه‌اندازی مجدد گیت‌وی بارگذاری مجدد داغ می‌شوند.

`~/.hermes/webhook_subscriptions.json`

## `hermes doctor`​

`hermes doctor`

```
hermes doctor [--fix]
```

| گزینه | توضیح |
| --- | --- |
| `--fix` | تلاش برای تعمیرات خودکار در صورت امکان. |

`--fix`

## `hermes dump`​

`hermes dump`

```
hermes dump [--show-keys]
```

خلاصه‌ای فشرده و متن ساده از کل راه‌اندازی Hermes شما خروجی می‌دهد. طراحی شده برای کپی-پیست در Discord، GitHub issues یا Telegram هنگام درخواست پشتیبانی — بدون رنگ ANSI، بدون قالب‌بندی خاص، فقط داده.

| گزینه | توضیح |
| --- | --- |
| `--show-keys` | نمایش پیشوندهای کلید API ویرایش شده (۴ کاراکتر اول و آخر) به جای فقط `set`/`not set`. |

`--show-keys`
`set`
`not set`

### چه چیزی شامل می‌شود​

| بخش | جزئیات |
| --- | --- |
| Header | نسخه Hermes، تاریخ انتشار، هش commit git |
| Environment | OS، نسخه Python، نسخه OpenAI SDK |
| Identity | نام پروفایل فعال، مسیر HERMES_HOME |
| Model | مدل و ارائه‌دهنده پیش‌فرض پیکربندی شده |
| Terminal | نوع backend (local, docker, ssh و غیره) |
| API keys | بررسی وجود برای همه ۲۲ کلید API ارائه‌دهنده/ابزار |
| Features | toolsetهای فعال، تعداد سرور MCP، ارائه‌دهنده حافظه |
| Services | وضعیت گیت‌وی، پلتفرم‌های پیام‌رسانی پیکربندی شده |
| Workload | تعداد تسک‌های cron، تعداد مهارت‌های نصب شده |
| Config overrides | هر مقدار پیکربندی که با پیش‌فرض‌ها متفاوت است |

### خروجی مثال​

```
--- hermes dump ---
version:          0.8.0 (2026.4.8) [af4abd2f]
os:               Linux 6.14.0-37-generic x86_64
python:           3.11.14
openai_sdk:       2.24.0
profile:          default
hermes_home:      ~/.hermes
model:            anthropic/claude-opus-4.6
provider:         openrouter
terminal:         local
api_keys:
  openrouter           set
  openai               not set
  anthropic            set
  nous                 not set
  firecrawl            set
  ...
features:
  toolsets:           all
  mcp_servers:        0
  memory_provider:    built-in
  gateway:            running (systemd)
  platforms:          telegram, discord
  cron_jobs:          3 active / 5 total
  skills:             42
config_overrides:
  agent.max_turns: 250
  compression.threshold: 0.85
  display.streaming: True
--- end dump ---
```

### چه زمانی استفاده کنید​

- گزارش خطا در GitHub — dump را در issue خود بچسبانید
- درخواست کمک در Discord — آن را در یک بلوک کد به اشتراک بگذارید
- مقایسه راه‌اندازی شما با راه‌اندازی شخص دیگر
- بررسی سریع وقتی چیزی کار نمی‌کند

`hermes dump` به طور خاص برای اشتراک‌گذاری طراحی شده. برای تشخیص‌های تعاملی، از `hermes doctor` استفاده کنید. برای نمای کلی بصری، از `hermes status` استفاده کنید.

`hermes dump`
`hermes doctor`
`hermes status`

## `hermes debug`​

`hermes debug`

```
hermes debug share [options]
```

آپلود یک گزارش دیباگ (اطلاعات سیستم + لاگ‌های اخیر) در یک سرویس paste و دریافت یک URL قابل اشتراک‌گذاری. مفید برای درخواست‌های پشتیبانی سریع — شامل همه چیزی است که یک کمک‌کننده برای تشخیص مشکل شما نیاز دارد.

| گزینه | توضیح |
| --- | --- |
| `--lines <N>` | تعداد خطوط لاگ برای شامل کردن به ازای هر فایل لاگ (پیش‌فرض: 200). |
| `--expire <days>` | انقضای paste به روز (پیش‌فرض: 7). |
| `--nous` | آپلود در ذخیره‌سازی تشخیص داخلی Nous به جای سرویس paste عمومی. وقتی پشتیبانی Nous باندل تشخیص خصوصی درخواست می‌کند استفاده کنید. |
| `--local` | چاپ گزارش به صورت محلی به جای آپلود. |
| `--no-redact` | غیرفعال کردن ویرایش secret هنگام آپلود. به طور پیش‌فرض، آپلودها ویرایش می‌شوند. |

`--lines <N>`
`--expire <days>`
`--nous`
`--local`
`--no-redact`

گزارش شامل اطلاعات سیستم (OS، نسخه Python، نسخه Hermes)، لاگ‌های اخیر agent، گیت‌وی، GUI/dashboard و دسکتاپ (محدودیت 512 KB به ازای هر فایل) و وضعیت کلید API ویرایش شده است. به طور پیش‌فرض، آپلودها ویرایش می‌شوند بنابراین secretها شامل نمی‌شوند.

آپلودهای پیش‌فرض از سرویس‌های paste عمومی به ترتیب استفاده می‌کنند: paste.rs، dpaste.com. `--nous` همان باندل دیباگ را در ذخیره‌سازی تشخیص خصوصی Nous آپلود می‌کند؛ لینک viewer برگشتی برای تیم Nous است و پس از ۱۴ روز به طور خودکار حذف می‌شود.

`--nous`

### مثال‌ها​

```
hermes debug share              # Upload debug report, print URL
hermes debug share --lines 500  # Include more log lines
hermes debug share --expire 30  # Keep paste for 30 days
hermes debug share --nous       # Upload a private diagnostics bundle for Nous support
hermes debug share --local      # Print report to terminal (no upload)
```

## `hermes backup`​

`hermes backup`

```
hermes backup [options]
```

ایجاد یک آرشیو zip از پیکربندی، مهارت‌ها، نشست‌ها و داده‌های Hermes شما. نسخه پشتیبان خود مخزن کد hermes-agent را حذف می‌کند.

| گزینه | توضیح |
| --- | --- |
| `-o`, `--output <path>` | مسیر خروجی برای فایل zip (پیش‌فرض: `~/hermes-backup-<timestamp>.zip`). |
| `-q`, `--quick` | اسناپ‌شات سریع: فقط فایل‌های وضعیت حیاتی (`config.yaml`، `state.db`، `.env`، auth، تسک‌های cron). بسیار سریع‌تر از نسخه پشتیبان کامل. |
| `-l`, `--label <name>` | برچسب برای اسناپ‌شات (فقط با `--quick` استفاده می‌شود). |

`-o`
`--output <path>`
`~/hermes-backup-<timestamp>.zip`
`-q`
`--quick`
`-l`
`--label <name>`
`--quick`

نسخه پشتیبان از API `backup()` SQLite برای کپی ایمن استفاده می‌کند، بنابراین حتی وقتی Hermes در حال اجراست به درستی کار می‌کند (امن در حالت WAL).

`backup()`

چه چیزی از zip حذف می‌شود:

- `*.db-wal`، `*.db-shm`، `*.db-journal` — sidecarهای WAL / shared-memory / journal SQLite. فایل `*.db` از قبل اسناپ‌شات سازگاری از طریق `sqlite3.backup()` دریافت کرده؛ ارسال sidecarهای زنده در کنار آن به بازیابی اجازه می‌دهد وضعیت نیمه-تایید شده را ببیند.
- `checkpoints/` — کش trajectory به ازای هر نشست. هش-کلیدی و بازتولید به ازای هر نشست؛ به هر حال به طور تمیز به نصب دیگر منتقل نمی‌شود.
- خود کد `hermes-agent` (این نسخه پشتیبان داده کاربر است، نه اسناپ‌شات مخزن).

`*.db-wal`
`*.db-shm`
`*.db-journal`
`*.db`
`sqlite3.backup()`
`checkpoints/`
`hermes-agent`

### مثال‌ها​

```
hermes backup                           # Full backup to ~/hermes-backup-*.zip
hermes backup -o /tmp/hermes.zip        # Full backup to specific path
hermes backup --quick                   # Quick state-only snapshot
hermes backup --quick --label "pre-upgrade"  # Quick snapshot with label
```

## `hermes checkpoints`​

`hermes checkpoints`

```
hermes checkpoints [COMMAND]
```

بررسی و مدیریت فروشگاه git سایه‌ای در `~/.hermes/checkpoints/` — لایه ذخیره‌سازی پشت دستور `/rollback` درون نشست. در هر زمان اجرا ایمن است؛ نیازی نیست agent در حال اجرا باشد.

`~/.hermes/checkpoints/`
`/rollback`

| دستور زیر سطح | توضیح |
| --- | --- |
| `status` (پیش‌فرض) | نمایش اندازه کل، تعداد پروژه‌ها و تفکیک به ازای هر پروژه. معادل `hermes checkpoints` بدون آرگومان. |
| `list` | نام مستعار `status`. |
| `prune` | اجرای جاروب پاکسازی اجباری — حذف پروژه‌های یتیم و منقضی، GC فروشگاه، اجرای محدودیت اندازه. نشانگر idempotency ۲۴ ساعته را نادیده می‌گیرد. |
| `clear` | حذف کل پایه checkpoints. غیرقابل بازگشت؛ مگر `-f` تأیید درخواست می‌کند. |
| `clear-legacy` | حذف فقط آرشیوهای `legacy-<timestamp>/` تولید شده توسط مهاجرت v1→v2. |

`status`
`hermes checkpoints`
`list`
`status`
`prune`
`clear`
`-f`
`clear-legacy`
`legacy-<timestamp>/`

### گزینه‌ها​

| گزینه | دستور زیر سطح | توضیح |
| --- | --- | --- |
| `--limit N` | `status`, `list` | حداکثر پروژه‌ها برای فهرست کردن (پیش‌فرض 20). |
| `--retention-days N` | `prune` | حذف پروژه‌هایی که `last_touch` قدیمی‌تر از N روز است (پیش‌فرض 7). |
| `--max-size-mb N` | `prune` | پس از عبور یتیم/منقضی، حذف قدیمی‌ترین commit به ازای هر پروژه تا اندازه کل فروشگاه ≤ N MB (پیش‌فرض 500). |
| `--keep-orphans` | `prune` | رد کردن حذف پروژه‌هایی که دایرکتوری کاری آنها دیگر وجود ندارد. |
| `-f`, `--force` | `clear`, `clear-legacy` | رد کردن درخواست تأیید. |

`--limit N`
`status`
`list`
`--retention-days N`
`prune`
`last_touch`
`--max-size-mb N`
`prune`
`--keep-orphans`
`prune`
`-f`
`--force`
`clear`
`clear-legacy`

### مثال‌ها​

```
hermes checkpoints                                  # status overview
hermes checkpoints prune --retention-days 3         # aggressive cleanup
hermes checkpoints prune --max-size-mb 200          # tighten size cap once
hermes checkpoints clear-legacy -f                  # drop v1 archive dirs
hermes checkpoints clear -f                         # wipe everything
```

برای معماری کامل و دستورات درون نشست به [Checkpoints and `/rollback`](/docs/user-guide/checkpoints-and-rollback/) مراجعه کنید.

`/rollback`

## `hermes import`​

`hermes import`

```
hermes import <zipfile> [options]
```

بازیابی یک نسخه پشتیبان Hermes ایجاد شده قبلی در دایرکتوری Hermes home شما. همه فایل‌ها در آرشیو فایل‌های موجود در Hermes home شما را بازنویسی می‌کنند؛ `--force` فقط درخواست تأییدی را که هنگام وجود نصب Hermes در هدف فعال می‌شود رد می‌کند.

`--force`

| گزینه | توضیح |
| --- | --- |
| `-f`, `--force` | رد کردن درخواست تأیید نصب موجود. |

`-f`
`--force`

قبل از import، گیت‌وی را متوقف کنید تا از تداخل با فرآیندهای در حال اجرا جلوگیری شود.

### مثال‌ها​

```
hermes import ~/hermes-backup-20260423.zip           # Prompts before overwriting existing config
hermes import ~/hermes-backup-20260423.zip --force   # Overwrite without prompting
```

## `hermes logs`​

`hermes logs`

```
hermes logs [log_name] [options]
```

مشاهده، دنبال کردن و فیلتر کردن فایل‌های لاگ Hermes. همه لاگ‌ها در `~/.hermes/logs/` (یا `<profile>/logs/` برای پروفایل‌های غیرپیش‌فرض) ذخیره می‌شوند.

`~/.hermes/logs/`
`<profile>/logs/`

### فایل‌های لاگ​

| نام | فایل | چه چیزی ثبت می‌کند |
| --- | --- | --- |
| `agent` (پیش‌فرض) | `agent.log` | همه فعالیت‌های agent — فراخوانی‌های API، ارسال ابزار، چرخه حیات نشست (INFO و بالاتر) |
| `errors` | `errors.log` | فقط هشدارها و خطاها — زیرمجموعه فیلتر شده agent.log |
| `gateway` | `gateway.log` | فعالیت گیت‌وی پیام‌رسانی — اتصالات پلتفرم، ارسال پیام، رویدادهای webhook |
| `gui` | `gui.log` | Dashboard / TUI-gateway / PTY-bridge / رویدادهای websocket |
| `desktop` | `desktop.log` | اپ دسکتاپ Electron — بوت، خروجی ایجاد backend و tracebackهای پایتون اخیر |

`agent`
`agent.log`
`errors`
`errors.log`
`gateway`
`gateway.log`
`gui`
`gui.log`
`desktop`
`desktop.log`

### گزینه‌ها​

| گزینه | توضیح |
| --- | --- |
| `log_name` | کدام لاگ را مشاهده کنید: `agent` (پیش‌فرض)، `errors`، `gateway` یا `list` برای نمایش فایل‌های موجود با اندازه‌ها. |
| `-n`, `--lines <N>` | تعداد خطوط برای نمایش (پیش‌فرض: 50). |
| `-f`, `--follow` | دنبال کردن لاگ در زمان واقعی، مانند `tail -f`. `Ctrl+C` برای توقف. |
| `--level <LEVEL>` | حداقل سطح لاگ برای نمایش: `DEBUG`، `INFO`، `WARNING`، `ERROR`، `CRITICAL`. |
| `--session <ID>` | فیلتر خطوط حاوی زیررشته session ID. |
| `--since <TIME>` | نمایش خطوط از یک زمان نسبی قبل: `30m`، `1h`، `2d` و غیره. از `s` (ثانیه)، `h` (ساعت)، `d` (روز) پشتیبانی می‌کند. |
| `--component <NAME>` | فیلتر بر اساس مولفه: `gateway`، `agent`، `tools`، `cli`، `cron`. |

`log_name`
`agent`
`errors`
`gateway`
`list`
`-n`
`--lines <N>`
`-f`
`--follow`
`tail -f`
`--level <LEVEL>`
`DEBUG`
`INFO`
`WARNING`
`ERROR`
`CRITICAL`
`--session <ID>`
`--since <TIME>`
`30m`
`1h`
`2d`
`s`
`m`
`h`
`d`
`--component <NAME>`
`gateway`
`agent`
`tools`
`cli`
`cron`

### مثال‌ها​

```
# View the last 50 lines of agent.log (default)
hermes logs
# Follow agent.log in real time
hermes logs -f
# View the last 100 lines of gateway.log
hermes logs gateway -n 100
# Show only warnings and errors from the last hour
hermes logs --level WARNING --since 1h
# Filter by a specific session
hermes logs --session abc123
# Follow errors.log, starting from 30 minutes ago
hermes logs errors --since 30m -f
# List all log files with their sizes
hermes logs list
```

### فیلتر کردن​

فیلترها قابل ترکیب هستند. وقتی چند فیلتر فعال باشند، یک خط لاگ باید **همه** آنها را رد کند تا نمایش داده شود:

```
# WARNING+ lines from the last 2 hours containing session "tg-12345"
hermes logs --level WARNING --since 2h --session tg-12345
```

خطوط بدون timestamp قابل تحلیل وقتی `--since` فعال است شامل می‌شوند (ممکن است خطوط ادامه‌دار از یک ورود لاگ چندخطی باشند). خطوط بدون سطح قابل تشخیص وقتی `--level` فعال است شامل می‌شوند.

`--since`
`--level`

### چرخش لاگ​

Hermes از `RotatingFileHandler` پایتون استفاده می‌کند. لاگ‌های قدیمی به طور خودکار چرخش می‌شوند — به دنبال `agent.log.1`، `agent.log.2` و غیره بگردید. دستور `hermes logs list` همه فایل‌های لاگ شامل چرخش شده‌ها را نشان می‌دهد.

`RotatingFileHandler`
`agent.log.1`
`agent.log.2`
`hermes logs list`

## `hermes prompt-size`​

`hermes prompt-size`

```
hermes prompt-size [--platform <name>] [--json]
```

بودجه prompt ثابت برای یک نشست جدید را گزارش می‌دهد — چه چیزی در هر فراخوانی API **قبل** از هر محتوای مکالمه ارسال می‌شود. مفید وقتی یک آداپتور یا پروکسی downstream بودجه prompt تنگ‌تری از پنجره context مدل دارد، یا وقتی می‌خواهید ببینید کدام بلوک (ایندکس مهارت‌ها، حافظه، پروفایل) غالب است.

همان system prompt را می‌سازد که agent می‌ساخت، سپس آن را تفکیک می‌کند:

- **کل system prompt** — prompt کامل مونتاژ شده (هویت، راهنمایی، ایندکس مهارت‌ها، فایل‌های context، حافظه، پروفایل، تمبر زمانی).
- **ایندکس مهارت‌ها** — بلوک `<available_skills>`. اغلب بزرگ‌ترین بلوک واحد وقتی مهارت‌های زیادی نصب شده.
- **حافظه و پروفایل کاربر** — اسناپ‌شات `MEMORY.md`/`USER.md` شما.
- **سطوح prompt** — پایدار / context / متغیر، مطابق نحوه لایه‌بندی prompt توسط Hermes برای سازگاری با کش.
- **اسکیماهای ابزار** — JSON برای همه ابزارهای فعال (نیمی دیگر از payload ثابت به ازای هر فراخوانی).

`<available_skills>`
`MEMORY.md`
`USER.md`

کاملاً آفلاین اجرا می‌شود — بدون فراخوانی API، بدون اعتبارنامه پیکربندی شده کار می‌کند.

```
# Human-readable breakdown for the CLI platform (default)
hermes prompt-size
# Simulate a messaging platform's prompt (different platform hint)
hermes prompt-size --platform telegram
# Machine-readable output for scripts
hermes prompt-size --json
```

ایندکس مهارت‌ها و اسکیماهای ابزار با تعداد مهارت‌ها و ابزارهای فعال شما مقیاس می‌گیرند. برای کوچک کردن prompt، ابزارهای غیرفعال toolset را غیرفعال کنید (`hermes tools`) یا مهارت‌هایی که نیاز ندارید را حذف کنید (`hermes skills`). فایل‌های context (`AGENTS.md`، `.cursorrules`) در دایرکتوری جاری شما نیز به کل محاسبه می‌شوند.

`hermes tools`
`hermes skills`

## `hermes config`​

`hermes config`

```
hermes config <subcommand>
```

دستورات زیر سطح:

| دستور زیر سطح | توضیح |
| --- | --- |
| `show` | نمایش مقادیر پیکربندی فعلی. |
| `edit` | باز کردن `config.yaml` در ویرایشگر شما. |
| `set <key> <value>` | تنظیم مقدار پیکربندی. |
| `path` | چاپ مسیر فایل پیکربندی. |
| `env-path` | چاپ مسیر فایل `.env`. |
| `check` | بررسی پیکربندی گم‌شده یا منقضی. |
| `migrate` | اضافه کردن گزینه‌های جدید به تازگی معرفی شده به صورت تعاملی. |

`show`
`edit`
`config.yaml`
`set <key> <value>`
`path`
`env-path`
`.env`
`check`
`migrate`

## `hermes pairing`​

`hermes pairing`

```
hermes pairing <list|approve|revoke|clear-pending>
```

| دستور زیر سطح | توضیح |
| --- | --- |
| `list` | نمایش کاربران در انتظار و تأیید شده. |
| `approve <platform> <code>` | تأیید کد جفت‌سازی. |
| `revoke <platform> <user-id>` | لغو دسترسی کاربر. |
| `clear-pending` | پاک کردن کدهای جفت‌سازی در انتظار. |

`list`
`approve <platform> <code>`
`revoke <platform> <user-id>`
`clear-pending`

## `hermes skills`​

`hermes skills`

```
hermes skills <subcommand>
```

دستورات زیر سطح:

| دستور زیر سطح | توضیح |
| --- | --- |
| `browse` | مرورگر صفحه‌بندی شده برای رجیستری مهارت‌ها. |
| `search` | جستجوی رجیستری مهارت‌ها. |
| `install` | نصب یک مهارت. |
| `inspect` | پیش‌نمایش یک مهارت بدون نصب. |
| `list` | فهرست مهارت‌های نصب شده. |
| `check` | بررسی مهارت‌های hub نصب شده برای به‌روزرسانی upstream. |
| `update` | نصب مجدد مهارت‌های hub با تغییرات upstream در صورت موجود بودن. |
| `audit` | اسکن مجدد مهارت‌های hub نصب شده. |
| `uninstall` | حذف یک مهارت نصب شده توسط hub. |
| `reset` | لغو چسبندگی یک مهارت bundle علامت‌گذاری شده به عنوان `user_modified` با پاک کردن ورودی manifest آن. با `--restore` همچنین نسخه کاربر را با نسخه bundle جایگزین می‌کند. |
| `opt-out` | جلوگیری از بذرپاشی مهارت‌های bundle در پروفایل فعال. یک نشانگر `.no-bundled-skills` می‌نویسد تا نصاب، `hermes update` و هر همگام‌سازی بذرپاشی مهارت‌های bundle را رد کنند. به طور پیش‌فرض ایمن — چیزی روی دیسک لمس نمی‌شود. با `--remove` همچنین مهارت‌های bundle از قبل موجود `unmodified` را حذف می‌کند (مهارت‌های ویرایش شده توسط کاربر، نصب شده توسط hub و دست‌نوشته هرگز حذف نمی‌شوند؛ ابتدا پیش‌نمایش و تأیید می‌کند، `--yes` برای رد کردن). |
| `opt-in` | برگرداندن `opt-out` با حذف نشانگر `.no-bundled-skills` تا مهارت‌های bundle در `hermes update` بعدی دوباره بذرپاشی شوند. با `--sync` بلافاصله دوباره بذرپاشی کنید. |
| `publish` | انتشار یک مهارت در رجیستری. |
| `snapshot` | خروجی/ورودی پیکربندی مهارت‌ها. |
| `tap` | مدیریت منابع مهارت سفارشی. |
| `config` | فعال/غیرفعال کردن تعاملی پیکربندی مهارت‌ها به ازای هر پلتفرم. |

`browse`
`search`
`install`
`inspect`
`list`
`check`
`update`
`audit`
`uninstall`
`reset`
`user_modified`
`--restore`
`opt-out`
`.no-bundled-skills`
`hermes update`
`--remove`
`--yes`
`opt-in`
`opt-out`
`.no-bundled-skills`
`hermes update`
`--sync`
`publish`
`snapshot`
`tap`
`config`

مثال‌های رایج:

```
hermes skills browse
hermes skills browse --source official
hermes skills search react --source skills-sh
hermes skills search https://mintlify.com/docs --source well-known
hermes skills inspect official/security/1password
hermes skills inspect skills-sh/vercel-labs/json-render/json-render-react
hermes skills install official/migration/openclaw-migration
hermes skills install skills-sh/anthropics/skills/pdf --force
hermes skills install https://sharethis.chat/SKILL.md                     # Direct URL (single-file SKILL.md)
hermes skills install https://example.com/SKILL.md --name my-skill        # Override name when frontmatter has none
hermes skills check
hermes skills update
hermes skills config
hermes skills reset google-workspace
hermes skills reset google-workspace --restore --yes
hermes skills opt-out                  # stop future bundled-skill seeding (nothing deleted)
hermes skills opt-out --remove --yes   # also delete UNMODIFIED bundled skills
hermes skills opt-in --sync            # undo: remove marker and re-seed now
```

یادداشت‌ها:

- `--force` می‌تواند بلوک‌های سیاست غیرخطرناک برای مهارت‌های شخص ثالث/جامعه را override کند.
- `--force` حکم اسکن `dangerous` را override نمی‌کند.
- `--source skills-sh` فهرست عمومی `skills.sh` را جستجو می‌کند.
- `--source well-known` به شما اجازه می‌دهد Hermes را به سایتی که `/.well-known/skills/index.json` را نمایان می‌کند اشاره کنید.
- `--source browse-sh` کاتالوگ ۲۰۰+ مهارت خودکارسازی مرورگر اختصاصی سایت `browse.sh` را جستجو می‌کند. شناسه‌ها شبیه `browse-sh/airbnb.com/search-listings-ddgioa` هستند.
- ارسال یک URL `http(s)://…/*.md` مستقیماً یک فایل تک SKILL.md نصب می‌کند. وقتی frontmatter `name:` ندارد و slug URL شناسه معتبری نیست، ترمینال تعاملی برای نام درخواست می‌کند؛ سطوح غیرتعاملی (`/skills install` در TUI، پلتفرم‌های گیت‌وی) به `--name <x>` نیاز دارند.

`--force`
`--force`
`dangerous`
`--source skills-sh`
`skills.sh`
`--source well-known`
`/.well-known/skills/index.json`
`--source browse-sh`
[browse.sh](https://browse.sh)
`browse-sh/airbnb.com/search-listings-ddgioa`
`http(s)://…/*.md`
`name:`
`/skills install`
`--name <x>`

## `hermes bundles`​

`hermes bundles`

```
hermes bundles <subcommand>
```

بسته‌های مهارت چندین مهارت را تحت یک دستور اسلش `/<bundle-name>` گروه‌بندی می‌کنند. فراخوانی بسته همه مهارت‌های ارجاع شده را در یک پیام کاربر ترکیبی واحد بارگذاری می‌کند. ذخیره‌سازی: `~/.hermes/skill-bundles/<slug>.yaml`. برای اسکیما YAML و رفتار به [Skill Bundles](/docs/user-guide/features/skills#skill-bundles) مراجعه کنید.

`/<bundle-name>`
`~/.hermes/skill-bundles/<slug>.yaml`

دستورات زیر سطح:

| دستور زیر سطح | توضیح |
| --- | --- |
| `list` | فهرست بسته‌های نصب شده (پیش‌فرض وقتی دستور زیر سطحی داده نشده) |
| `show <name>` | نمایش نام، توصیف، مهارت‌ها و مسیر فایل یک بسته |
| `create <name>` | ایجاد بسته جدید. `--skill <id>` (تکرار) ارسال کنید یا برای ورود تعاملی حذف کنید. `--description`، `--instruction`، `--force` موجود. |
| `delete <name>` | حذف فایل بسته |
| `reload` | اسکن مجدد `~/.hermes/skill-bundles/` و گزارش بسته‌های اضافه/حذف شده |

`list`
`show <name>`
`create <name>`
`--skill <id>`
`--description`
`--instruction`
`--force`
`delete <name>`
`reload`
`~/.hermes/skill-bundles/`

مثال‌ها:

```
hermes bundles create backend-dev \
  --skill github-code-review \
  --skill test-driven-development \
  --skill github-pr-workflow \
  -d "Backend feature work"
hermes bundles list
hermes bundles show backend-dev
hermes bundles delete backend-dev
```

در یک نشست چت، `/bundles` بسته‌های نصب شده را فهرست می‌کند و `/<bundle-name>` یکی را بارگذاری می‌کند.

`/bundles`
`/<bundle-name>`

## `hermes curator`​

`hermes curator`

```
hermes curator <subcommand>
```

curator یک تسک پس‌زمینه مدل کمکی است که دوره‌ای مهارت‌های ایجاد شده توسط agent را بررسی، مهارت‌های منقضی را هرس، همپوشانی‌ها را ادغام و مهارت‌های منسوخ را آرشیو می‌کند. مهارت‌های bundle و hub نصب شده هرگز لمس نمی‌شوند. آرشیوها قابل بازیابی هستند؛ حذف خودکار هرگز اتفاق نمی‌افتد.

| دستور زیر سطح | توضیح |
| --- | --- |
| `status` | نمایش وضعیت curator و آمار مهارت‌ها |
| `run` | فعال کردن بررسی curator اکنون (تا پایان عبور LLM بلاک می‌کند) |
| `run --background` | شروع عبور LLM در thread پس‌زمینه و برگشت فوری |
| `run --dry-run` | فقط پیش‌نمایش — تولید گزارش بررسی بدون تغییرات |
| `backup` | گرفتن اسناپ‌شات دستی tar.gz از `~/.hermes/skills/` (curator همچنین قبل از هر اجرای واقعی به طور خودکار اسناپ‌شات می‌گیرد) |
| `rollback` | بازیابی `~/.hermes/skills/` از اسناپ‌شات (پیش‌فرض جدیدترین) |
| `rollback --list` | فهرست اسناپ‌شات‌های موجود |
| `rollback --id <ts>` | بازیابی یک اسناپ‌شات خاص با id |
| `rollback -y` | رد کردن درخواست تأیید |
| `pause` | توقف curator تا از سر گرفته شود |
| `resume` | از سرگیری curator متوقف شده |
| `pin <skill>` | ثابت کردن مهارت تا curator هرگز آن را به طور خودکار transition ندهد |
| `unpin <skill>` | رفع ثبات مهارت |
| `restore <skill>` | بازیابی یک مهارت آرشیو شده |
| `archive <skill>` | آرشیو دستی یک مهارت |
| `prune` | هرس دستی مهارت‌هایی که curator معمولاً پاکسازی می‌کند |
| `list-archived` | فهرست مهارت‌های آرشیو شده (قابل بازیابی از طریق `restore`) |

`status`
`run`
`run --background`
`run --dry-run`
`backup`
`~/.hermes/skills/`
`rollback`
`~/.hermes/skills/`
`rollback --list`
`rollback --id <ts>`
`rollback -y`
`pause`
`resume`
`pin <skill>`
`unpin <skill>`
`restore <skill>`
`archive <skill>`
`prune`
`list-archived`
`restore`

در یک نصب جدید، اولین عبور زمان‌بندی شده به اندازه یک `interval_hours` کامل (به طور پیش‌فرض ۷ روز) به تعویق می‌افتد — گیت‌وی بلافاصله پس از اولین تیک پس از `hermes update` ممیزی نمی‌کند. قبل از آن از `hermes curator run --dry-run` برای پیش‌نمایش استفاده کنید.

`interval_hours`
`hermes update`
`hermes curator run --dry-run`

برای رفتار و پیکربندی به [Curator](/docs/user-guide/features/curator/) مراجعه کنید.

## `hermes moa`​

`hermes moa`

پیکربندی presetهای نام‌دار Mixture of Agents. presetها به عنوان مدل‌های قابل انتخاب تحت ارائه‌دهنده `Mixture of Agents` در هر انتخابگر مدل ظاهر می‌شوند؛ `/moa <prompt>` یک پرامپت را از طریق preset پیش‌فرض اجرا می‌کند.

`Mixture of Agents`
`/moa <prompt>`

```
hermes moa list
hermes moa configure [name]
hermes moa delete <name>
```

`hermes moa configure` از انتخابگر ارائه‌دهنده → مدل Hermes برای هر مدل مرجع و aggregator استفاده مجدد می‌کند. preset یک پیکربندی حالت اجرا است، نه یک مدل یا ارائه‌دهنده اصلی.

`hermes moa configure`

## `hermes fallback`​

`hermes fallback`

```
hermes fallback <subcommand>
```

مدیریت زنجیره ارائه‌دهنده fallback. ارائه‌دهندگان fallback به ترتیب وقتی مدل اصلی با خطای rate-limit، overload یا اتصال ناموفق باشد امتحان می‌شوند.

| دستور زیر سطح | توضیح |
| --- | --- |
| `list` (نام مستعار: `ls`) | نمایش زنجیره fallback فعلی (پیش‌فرض وقتی دستور زیر سطحی نیست) |
| `add` | انتخاب ارائه‌دهنده + مدل (همان انتخابگر `hermes model`) و اضافه کردن به انتهای زنجیره |
| `remove` (نام مستعار: `rm`) | انتخاب یک ورودی برای حذف از زنجیره |
| `clear` | حذف همه ورودی‌های fallback |

`list`
`ls`
`add`
`hermes model`
`remove`
`rm`
`clear`

به [Fallback Providers](/docs/user-guide/features/fallback-providers/) مراجعه کنید.

## `hermes hooks`​

`hermes hooks`

```
hermes hooks <subcommand>
```

بررسی هوک‌های اسکریپت shell اعلام شده در `~/.hermes/config.yaml`، آزمایش آنها با payloadهای مصنوعی و مدیریت لیست مجاز consent استفاده اول در `~/.hermes/shell-hooks-allowlist.json`.

`~/.hermes/config.yaml`
`~/.hermes/shell-hooks-allowlist.json`

| دستور زیر سطح | توضیح |
| --- | --- |
| `list` (نام مستعار: `ls`) | فهرست هوک‌های پیکربندی شده با matcher، timeout و وضعیت consent |
| `test <event>` | فعال کردن هر هوک مطابق `<event>` علیه یک payload مصنوعی |
| `revoke` (نام مستعارها: `remove`, `rm`) | حذف ورودی‌های لیست مجاز یک دستور (در راه‌اندازی مجدد بعدی اعمال می‌شود) |
| `doctor` | بررسی هر هوک پیکربندی شده: بیت exec، لیست مجاز، انحراف mtime، اعتبار JSON و زمان‌بندی اجرای مصنوعی |

`list`
`ls`
`test <event>`
`<event>`
`revoke`
`remove`
`rm`
`doctor`

برای امضاهای رویداد و اشکال payload به [Hooks](/docs/user-guide/features/hooks/) مراجعه کنید.

## `hermes memory`​

`hermes memory`

```
hermes memory <subcommand>
```

راه‌اندازی و مدیریت pluginهای ارائه‌دهنده حافظه خارجی. ارائه‌دهندگان موجود: honcho، openviking، mem0، hindsight، holographic، retaindb، byterover، supermemory. فقط یک ارائه‌دهنده خارجی می‌تواند در یک زمان فعال باشد. حافظه داخلی (`MEMORY.md`/`USER.md`) همیشه فعال است.

دستورات زیر سطح:

| دستور زیر سطح | توضیح |
| --- | --- |
| `setup` | انتخاب و پیکربندی تعاملی ارائه‌دهنده. |
| `status` | نمایش پیکربندی ارائه‌دهنده حافظه فعلی. |
| `off` | غیرفعال کردن ارائه‌دهنده خارجی (فقط داخلی). |

`setup`
`status`
`off`

وقتی یک ارائه‌دهنده حافظه خارجی فعال باشد، ممکن است دستور سطح بالای اختصاصی خود `hermes <provider>` را برای مدیریت اختصاصی ارائه‌دهنده ثبت کند (مثلاً `hermes honcho` وقتی Honcho فعال است). ارائه‌دهندگان غیرفعال دستورات زیر سطح خود را نمایان نمی‌کنند. `hermes --help` را اجرا کنید تا ببینید چه چیزی اکنون متصل است.

`hermes <provider>`
`hermes honcho`
`hermes --help`

## `hermes acp`​

`hermes acp`

```
hermes acp
```

Hermes را به عنوان سرور stdio ACP (Agent Client Protocol) برای ادغام ویرایشگر شروع می‌کند.

نقاط ورود مرتبط:

```
hermes-acp
python -m acp_adapter
```

ابتدا پشتیبانی نصب کنید:

```
cd ~/.hermes/hermes-agent && uv pip install -e '.[acp]'
```

به [ACP Editor Integration](/docs/user-guide/features/acp/) و [ACP Internals](/docs/developer-guide/acp-internals/) مراجعه کنید.

## `hermes mcp`​

`hermes mcp`

```
hermes mcp <subcommand>
```

مدیریت پیکربندی سرورهای MCP (Model Context Protocol) و اجرای Hermes به عنوان یک سرور MCP.

| دستور زیر سطح | توضیح |
| --- | --- |
| (هیچ) یا `picker` | انتخابگر تعاملی کاتالوگ — مرور MCPهای تأیید شده توسط Nous و نصب/فعال/غیرفعال. |
| `catalog` | فهرست MCPهای تأیید شده توسط Nous (متن ساده، قابل اسکریپت‌نویسی). |
| `install <name>` | نصب یک ورودی کاتالوگ (مثلاً `hermes mcp install n8n`). |
| `serve [-v\|--verbose]` | اجرای Hermes به عنوان سرور MCP — نمایان کردن مکالمات برای agentهای دیگر. |
| `add <name> [--url URL] [--command CMD] [--auth oauth\|header] [--args ...]` | اضافه کردن سرور MCP سفارشی با کشف خودکار ابزار. `--args` باقی argv را به دستور stdio ارسال می‌کند، بنابراین آن را آخر قرار دهید. |
| `remove <name>` (نام مستعار: `rm`) | حذف سرور MCP از پیکربندی. |
| `list` (نام مستعار: `ls`) | فهرست سرورهای MCP پیکربندی شده. |
| `test <name>` | آزمایش اتصال به یک سرور MCP. |
| `configure <name>` (نام مستعار: `config`) | جابجایی انتخاب ابزار برای یک سرور. |
| `login <name>` | اجبار به احراز هویت مجدد برای سرور MCP مبتنی بر OAuth. |

`picker`
`catalog`
`install <name>`
`hermes mcp install n8n`
`serve [-v|--verbose]`
`add <name> [--url URL] [--command CMD] [--auth oauth|header] [--args ...]`
`--args`
`remove <name>`
`rm`
`list`
`ls`
`test <name>`
`configure <name>`
`config`
`login <name>`

به [MCP Config Reference](/docs/reference/mcp-config-reference/)، [Use MCP with Hermes](/docs/guides/use-mcp-with-hermes/) و [MCP Server Mode](/docs/user-guide/features/mcp#running-hermes-as-an-mcp-server) مراجعه کنید.

## `hermes plugins`​

`hermes plugins`

```
hermes plugins [subcommand]
```

مدیریت یکپارچه plugin — pluginهای عمومی، ارائه‌دهندگان حافظه و موتورهای context در یک مکان. اجرای `hermes plugins` بدون دستور زیر سطح یک صفحه تعاملی ترکیبی با دو بخش باز می‌کند:

`hermes plugins`

- **Pluginهای عمومی** — چک‌باکسهای انتخاب چندگانه برای فعال/غیرفعال کردن pluginهای نصب شده
- **Pluginهای ارائه‌دهنده** — پیکربندی تک انتخابی برای ارائه‌دهنده حافظه و موتور context. ENTER را روی یک دسته فشار دهید تا انتخابگر رادیویی باز شود.

| دستور زیر سطح | توضیح |
| --- | --- |
| (هیچ) | UI تعاملی ترکیبی — کلیدهای toggle plugin عمومی + پیکربندی plugin ارائه‌دهنده. |
| `install <identifier> [--force]` | نصب plugin از یک URL Git یا `owner/repo`. |
| `update <name>` | کشیدن آخرین تغییرات برای plugin نصب شده. |
| `remove <name>` (نام مستعارها: `rm`, `uninstall`) | حذف plugin نصب شده. |
| `enable <name>` | فعال کردن plugin غیرفعال. |
| `disable <name>` | غیرفعال کردن plugin بدون حذف آن. |
| `list` (نام مستعار: `ls`) | فهرست pluginهای نصب شده با وضعیت فعال/غیرفعال. |

`install <identifier> [--force]`
`owner/repo`
`update <name>`
`remove <name>`
`rm`
`uninstall`
`enable <name>`
`disable <name>`
`list`
`ls`

انتخاب‌های plugin ارائه‌دهنده در `config.yaml` ذخیره می‌شوند:

`config.yaml`

- `memory.provider` — ارائه‌دهنده حافظه فعال (خالی = فقط داخلی)
- `context.engine` — موتور context فعال (`"compressor"` = پیش‌فرض داخلی)

`memory.provider`
`context.engine`
`"compressor"`

لیست غیرفعال plugin عمومی در `config.yaml` تحت `plugins.disabled` ذخیره می‌شود.

`config.yaml`
`plugins.disabled`

به [Plugins](/docs/user-guide/features/plugins/) و [Build a Hermes Plugin](/docs/developer-guide/plugins/) مراجعه کنید.

## `hermes tools`​

`hermes tools`

```
hermes tools [--summary]
```

| گزینه | توضیح |
| --- | --- |
| `--summary` | چاپ خلاصه ابزارهای فعال فعلی و خروج. |

`--summary`

بدون `--summary`، این UI پیکربندی ابزار به ازای هر پلتفرم تعاملی را راه‌اندازی می‌کند.

## `hermes computer-use`​

`hermes computer-use`

```
hermes computer-use <subcommand>
```

دستورات زیر سطح:

| دستور زیر سطح | توضیح |
| --- | --- |
| `install` | اجرای نصاب upstream cua-driver (macOS، Windows و Linux). |
| `install --upgrade` | اجرای مجدد نصاب حتی اگر cua-driver از قبل در PATH باشد. اسکریپت upstream همیشه آخرین انتشار را می‌کشد، بنابراین این ارتقای در جا انجام می‌دهد. |
| `status` | چاپ اینکه آیا cua-driver در `$PATH` است و کدام نسخه نصب شده. |

`install`
`install --upgrade`
`status`
`cua-driver`
`$PATH`

`hermes computer-use install` نقطه ورود پایدار برای نصب باینری `cua-driver` که توسط ابزار `computer_use` استفاده می‌شود. همان نصاب upstream را اجرا می‌کند که `hermes tools` هنگام اولین فعال کردن Computer Use فراخوانی می‌کند، بنابراین برای اجرای مجدد نصب در صورتی که toggle ابزار آن را فعال نکرده (مثلاً در راه‌اندازی‌های کاربر بازگشتی) ایمن است.

`hermes computer-use install`
[cua-driver](https://github.com/trycua/cua)
`computer_use`
`hermes tools`

`hermes update` به طور خودکار در پایان به‌روزرسانی نصب upstream را مجدداً اجرا می‌کند اگر `cua-driver` در PATH باشد، بنابراین اکثر کاربران نیازی به فراخوانی دستی `--upgrade` نخواهند داشت. از آن استفاده کنید وقتی upstream رفع خطایی را منتشر می‌کند که همین الان می‌خواهید بدون انتظار برای به‌روزرسانی بعدی Hermes.

`hermes update`
`--upgrade`

## `hermes pets`​

`hermes pets`

```
hermes pets <list|install|select|show|off|scale|remove|doctor>
```

[Petdex](https://github.com/crafter-ststation/petdex) یک گالری عمومی از حیوانات خانگی اسپرایت متحرک برای agentهای کدنویسی است. یکی را نصب کنید و Hermes آن را واکنش نشان داده به فعالیت agent در CLI، TUI و اپ دسکتاپ نمایش می‌دهد.

| دستور زیر سطح | توضیح |
| --- | --- |
| `list` | مرور گالری petdex. |
| `install` | نصب حیوان خانگی از گالری. |
| `select` | تنظیم حیوان خانگی فعال (در `display.pet.*` می‌نویسد). |
| `show` | متحرک کردن حیوان خانگی فعال در ترمینال. |
| `off` | غیرفعال کردن نمایش حیوان خانگی. |
| `scale` | تغییر اندازه حیوان خانگی در همه جا (`display.pet.scale`). |
| `remove` | حذف حیوان خانگی نصب شده. |
| `doctor` | بررسی راه‌اندازی حیوان خانگی + پشتیبانی گرافیک ترمینال. |

`list`
`install`
`select`
`display.pet.*`
`show`
`off`
`scale`
`display.pet.scale`
`remove`
`doctor`

همچنین می‌توانید یک حیوان خانگی کاملاً جدید از یک توصیف متنی با دستور اسلش `/hatch` تولید کنید. به [Pets](/docs/user-guide/features/pets/) مراجعه کنید.

`/hatch`

## `hermes sessions`​

`hermes sessions`

```
hermes sessions <subcommand>
```

دستورات زیر سطح:

| دستور زیر سطح | توضیح |
| --- | --- |
| `list` | فهرست نشست‌های اخیر. |
| `browse` | انتخابگر تعاملی نشست با جستجو و از سرگیری. |
| `export <output> [--session-id ID]` | خروجی نشست‌ها به JSONL. |
| `delete <session-id>` | حذف یک نشست. |
| `prune` | حذف نشست‌های مطابق فیلترها: محدودیت‌های زمانی `--older-than`/`--newer-than`/`--before`/`--after` (مانند `5h`/`2d`، روزهای ساده یا تمبرهای ISO)؛ ویژگی‌ها `--source`، `--title`، `--model`، `--provider`، `--branch`، `--end-reason`، `--user`، `--chat-id`، `--chat-type`، `--cwd`؛ محدودیت‌های عددی `--min`/`--max-messages`، `--min`/`--max-tokens`، `--min`/`--max-cost`، `--min`/`--max-tool-calls`؛ به علاوه `--include-archived`، `--dry-run`، `--yes`. پیش‌فرض: قدیمی‌تر از ۹۰ روز. |
| `archive` | آرشیو انبوه (مخفی کردن نرم، بدون حذف) نشست‌های مطابق همان فیلترهای `prune`. حداقل یک فیلتر نیاز دارد. |
| `stats` | نمایش آمار فروشگاه نشست. |
| `rename <session-id> <title>` | تنظیم یا تغییر عنوان نشست. |

`list`
`browse`
`export <output> [--session-id ID]`
`delete <session-id>`
`prune`
`--older-than`
`--newer-than`
`--before`
`--after`
`5h`
`2d`
`--source`
`--title`
`--model`
`--provider`
`--branch`
`--end-reason`
`--user`
`--chat-id`
`--chat-type`
`--cwd`
`--min/--max-messages`
`--min/--max-tokens`
`--min/--max-cost`
`--min/--max-tool-calls`
`--include-archived`
`--dry-run`
`--yes`
`archive`
`prune`
`stats`
`rename <session-id> <title>`

## `hermes insights`​

`hermes insights`

```
hermes insights [--days N] [--source platform]
```

| گزینه | توضیح |
| --- | --- |
| `--days <n>` | تحلیل n روز اخیر (پیش‌فرض: 30). |
| `--source <platform>` | فیلتر بر اساس منبع مانند `cli`، `telegram` یا `discord`. |

`--days <n>`
`n`
`--source <platform>`
`cli`
`telegram`
`discord`

## `hermes claw`​

`hermes claw`

```
hermes claw migrate [options]
```

راه‌اندازی OpenClaw خود را به Hermes مهاجرت دهید. از `~/.openclaw` (یا مسیر سفارشی) می‌خواند و در `~/.hermes` می‌نویسد. به طور خودکار نام‌های دایرکتوری قدیمی (`~/.clawdbot`، `~/.moltbot`) و نام‌های فایل پیکربندی (`clawdbot.json`، `moltbot.json`) را تشخیص می‌دهد.

`~/.openclaw`
`~/.hermes`
`~/.clawdbot`
`~/.moltbot`
`clawdbot.json`
`moltbot.json`

| گزینه | توضیح |
| --- | --- |
| `--dry-run` | پیش‌نمایش آنچه مهاجرت می‌شود بدون نوشتن چیزی. |
| `--preset <name>` | preset مهاجرت: `full` (همه تنظیمات سازگار) یا `user-data` (پیکربندی زیرساخت را حذف می‌کند). هیچ preset ای secret وارد نمی‌کند — `--migrate-secrets` را به صراحت ارسال کنید. |
| `--overwrite` | بازنویسی فایل‌های Hermes موجود در تعارضات (پیش‌فرض: رد کردن اعمال وقتی برنامه تعارض دارد). |
| `--migrate-secrets` | شامل کردن کلیدهای API در مهاجرت. حتی تحت `--preset full` مورد نیاز. |
| `--no-backup` | رد کردن اسناپ‌شات zip قبل از مهاجرت `~/.hermes/` (به طور پیش‌فرض یک آرشیو نقطه بازیابی واحد قبل از apply در `~/.hermes/backups/pre-migration-*.zip` نوشته می‌شود؛ قابل بازیابی با `hermes import`). |
| `--source <path>` | دایرکتوری OpenClaw سفارشی (پیش‌فرض: `~/.openclaw`). |
| `--workspace-target <path>` | دایرکتوری هدف برای دستورالعمل‌های فضای کاری (`AGENTS.md`). |
| `--skill-conflict <mode>` | مدیریت تداخل نام مهارت: `skip` (پیش‌فرض)، `overwrite` یا `rename`. |
| `--yes` | رد کردن درخواست تأیید. |

`--dry-run`
`--preset <name>`
`full`
`user-data`
`--migrate-secrets`
`--overwrite`
`--migrate-secrets`
`--preset full`
`--no-backup`
`~/.hermes/`
`~/.hermes/backups/pre-migration-*.zip`
`hermes import`
`--source <path>`
`~/.openclaw`
`--workspace-target <path>`
`--skill-conflict <mode>`
`skip`
`overwrite`
`rename`
`--yes`

### چه چیزی مهاجرت می‌شود​

مهاجرت بیش از ۳۰ دسته در شخصیت، حافظه، مهارت‌ها، ارائه‌دهندگان مدل، پلتفرم‌های پیام‌رسانی، رفتار agent، سیاست‌های نشست، سرورهای MCP، TTS و موارد دیگر را پوشش می‌دهد. آیتم‌ها یا مستقیماً به معادل‌های Hermes وارد می‌شوند یا برای بررسی دستی آرشیو می‌شوند.

**وارد شده مستقیماً:** `SOUL.md`، `MEMORY.md`، `USER.md`، `AGENTS.md`، مهارت‌ها (۴ دایرکتوری منبع)، مدل پیش‌فرض، ارائه‌دهندگان سفارشی، سرورهای MCP، توکن‌ها و لیست‌های مجاز پلتفرم پیام‌رسانی (Telegram، Discord، Slack، WhatsApp، Signal، Matrix، Mattermost)، پیش‌فرض‌های agent (تلاش استدلال، فشرده‌سازی، تأخیر انسان، منطقه زمانی، sandbox)، سیاست‌های بازنشانی نشست، قوانین تأیید، پیکربندی TTS، تنظیمات مرورگر، تنظیمات ابزار، timeout اجرا، لیست مجاز دستور، پیکربندی گیت‌وی و کلیدهای API از ۳ منبع.

**آرشیو شده برای بررسی دستی:** تسک‌های cron، pluginها، هوک‌ها/webhookها، backend حافظه (QMD)، پیکربندی رجیستری مهارت‌ها، UI/هویت، لاگ‌گیری، راه‌اندازی چندagent، اتصالات کانال، `IDENTITY.md`، `TOOLS.md`، `HEARTBEAT.md`، `BOOTSTRAP.md`.

** resolvesion کلید API** سه منبع را به ترتیب اولویت بررسی می‌کند: مقادیر پیکربندی → `~/.openclaw/.env` → `auth-profiles.json`. همه فیلدهای توکن رشته‌های ساده، الگوهای env (`${VAR}`) و اشیاء SecretRef را مدیریت می‌کنند.

`~/.openclaw/.env`
`auth-profiles.json`
`${VAR}`

برای نگاشت کامل کلید پیکربندی، جزئیات مدیریت SecretRef و چک‌لیست پس از مهاجرت، به [راهنمای کامل مهاجرت](/docs/guides/migrate-from-openclaw/) مراجعه کنید.

### مثال‌ها​

```
# Preview what would be migrated
hermes claw migrate --dry-run
# Full migration (all compatible settings, no secrets)
hermes claw migrate --preset full
# Full migration including API keys
hermes claw migrate --preset full --migrate-secrets
# Migrate user data only (no secrets), overwrite conflicts
hermes claw migrate --preset user-data --overwrite
# Migrate from a custom OpenClaw path
hermes claw migrate --source /home/user/old-openclaw
```

## `hermes serve`​

`hermes serve`

```
hermes serve [options]
```

سرور backend Hermes را شروع می‌کند — دروازه JSON-RPC/WebSocket که [اپ دسکتاپ](/docs/user-guide/desktop/) و کلاینت‌های راه دور به آن متصل می‌شوند. همان سروری است که `hermes dashboard` اجرا می‌کند اما **headless**: هرگز UI مرورگر را باز نمی‌کند. اپ دسکتاپ backend خود `hermes serve` را راه‌اندازی می‌کند؛ مستقیماً از این دستور استفاده کنید وقتی یک backend headless روی هاست راه دور می‌خواهید. همان گزینه‌های `--host`/`--port`/`--insecure`/`--skip-build`/`--stop`/`--status` را می‌پذیرد که `hermes dashboard` پایین (غیرloopback bind همان دروازه auth را فعال می‌کند). به extra `[web]` نیاز دارد؛ socket Chat تعبیه شده علاوه بر آن به `[pty]` در یک هاست POSIX نیاز دارد.

`hermes dashboard`
`hermes serve`

## `hermes dashboard`​

`hermes dashboard`

```
hermes dashboard [options]
```

داشبورد وب را راه‌اندازی می‌کند — UI مبتنی بر مرورگر برای مدیریت پیکربندی، کلیدهای API و نظارت نشست‌ها. (برای backend headless بدون UI مرورگر — مثلاً آنچه اپ دسکتاپ ایجاد می‌کند — از `hermes serve` بالا استفاده کنید.) به `cd ~/.hermes/hermes-agent && uv pip install -e ".[web]"` (FastAPI + Uvicorn) نیاز دارد. تب Chat مرورگر تعبیه شده همیشه موجود است و علاوه بر آن به extra `pty` نیاز دارد (`cd ~/.hermes/hermes-agent && uv pip install -e ".[web,pty]"`) به علاوه محیط POSIX PTY مانند Linux، macOS یا WSL2. برای مستندات کامل به [Web Dashboard](/docs/user-guide/features/web-dashboard/) مراجعه کنید.

`hermes serve`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[web]"`
`pty`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[web,pty]"`

| گزینه | پیش‌فرض | توضیح |
| --- | --- | --- |
| `--port` | 9119 | پورت برای اجرای سرور وب |
| `--host` | 127.0.0.1 | آدرس bind |
| `--no-open` | — | باز نکردن خودکار مرورگر |
| `--insecure` | off | منسوخ / بی‌اثر. قبلاً auth را در یک bind غیرloopback دور می‌زد. از ژوئن ۲۰۲۶ bind عمومی **همیشه** به یک ارائه‌دهنده auth (رمز عبور یا OAuth) نیاز دارد. `127.0.0.1` bind کنید و tunnel برای محلی نگه داشتن. |
| `--skip-build` | off | رد کردن مرحله ساخت UI وب و سرو کردن `dist` موجود مستقیماً. مفید برای زمینه‌های غیرتعاملی (Windows Scheduled Tasks، CI) که npm موجود نیست. از قبل با `cd web && npm run build` بسازید. |
| `--isolated` | off | وقتی از یک پروفایل نام‌دار راه‌اندازی می‌شود (dashboard کارگر)، یک سرور اختصاصی به ازای هر پروفایل به جای مسیریابی به dashboard ماشین اجرا کنید. |
| `--stop` | — | متوقف کردن فرآیندهای `hermes dashboard` در حال اجرا و خروج. |
| `--status` | — | فهرست فرآیندهای `hermes dashboard` در حال اجرا و خروج. |

`--port`
`9119`
`--host`
`127.0.0.1`
`--no-open`
`--insecure`
`127.0.0.1`
`--skip-build`
`dist`
`cd web && npm run build`
`--isolated`
`worker dashboard`
`--stop`
`hermes dashboard`
`--status`
`hermes dashboard`

### `hermes dashboard register`​

`hermes dashboard register`

این نصب را به عنوان dashboard خودمیزبان با حساب Nous Portal شما ثبت می‌کند. یک کلاینت OAuth ایجاد می‌کند، `HERMES_DASHBOARD_OAUTH_CLIENT_ID` را در `~/.hermes/.env` می‌نویسد و نحوه فعال کردن دروازه ورود را چاپ می‌کند. نیاز به ورود بودن (`hermes setup`) دارد.

`HERMES_DASHBOARD_OAUTH_CLIENT_ID`
`~/.hermes/.env`
`hermes setup`

| گزینه | توضیح |
| --- | --- |
| `--name` | برچسب خوانا توسط انسان برای dashboard (پیش‌فرض: به طور خودکار تولید شده). |
| `--redirect-uri` | URI بازگشت OAuth HTTPS عمومی (مثلاً `https://hermes.example.com/auth/callback`). برای استفاده localhost-only حذف کنید. |
| `--portal-url` | Override کردن base URL Nous Portal برای ثبت (پیش‌فرض: پورتالی که وارد شده‌اید). همچنین از طریق `HERMES_DASHBOARD_PORTAL_URL` قابل تنظیم. |

`--name`
`--redirect-uri`
`https://hermes.example.com/auth/callback`
`--portal-url`
`HERMES_DASHBOARD_PORTAL_URL`

```
# Default — opens browser to http://127.0.0.1:9119
hermes dashboard
# Custom port, no browser
hermes dashboard --port 8080 --no-open
# From a profile alias — routes to the machine dashboard with the
# profile preselected in the sidebar switcher (attach if running)
worker dashboard
```

## `hermes profile`​

`hermes profile`

```
hermes profile <subcommand>
```

مدیریت پروفایل‌ها — نمونه‌های ایزوله متعدد Hermes، هر کدام با پیکربندی، نشست‌ها، مهارت‌ها و دایرکتوری خانه خود.

| دستور زیر سطح | توضیح |
| --- | --- |
| `list` | فهرست همه پروفایل‌ها. |
| `use <name>` | تنظیم پروفایل پیش‌فرض چسبناک. |
| `create <name> [--clone] [--clone-all] [--clone-from <source>] [--no-alias]` | ایجاد پروفایل جدید. `--clone` پیکربندی، `.env`، `SOUL.md` و مهارت‌ها را از پروفایل فعال کپی می‌کند. `--clone-all` همه وضعیت را کپی می‌کند. `--clone-from` یک پروفایل منبع مشخص می‌کند و clone پیکربندی را شامل می‌مگر اینکه با `--clone-all` جفت شود. |
| `delete <name> [-y]` | حذف پروفایل. |
| `show <name>` | نمایش جزئیات پروفایل (دایرکتوری خانه، پیکربندی و غیره). |
| `alias <name> [--remove] [--name NAME]` | مدیریت اسکریپت‌های wrapper برای دسترسی سریع پروفایل. |
| `rename <old> <new>` | تغییر نام پروفایل. |
| `export <name> [-o FILE]` | خروجی پروفایل به آرشیو `.tar.gz` (نسخه پشتیبان محلی). |
| `import <archive> [--name NAME]` | وارد کردن پروفایل از آرشیو `.tar.gz` (بازیابی محلی). |
| `install <source> [--name N] [--alias] [--force] [-y]` | نصب توزیع پروفایل از URL Git یا دایرکتوری محلی. |
| `update <name> [--force-config] [-y]` | کشیدن مجدد توزیع؛ داده‌های کاربر (حافظه‌ها، نشست‌ها، auth) حفظ می‌شوند. |
| `info <name>` | نمایش manifest توزیع پروفایل (نسخه، وابستگی‌ها، منبع). |

`list`
`use <name>`
`create <name> [--clone] [--clone-all] [--clone-from <source>] [--no-alias]`
`--clone`
`.env`
`SOUL.md`
`--clone-all`
`--clone-from`
`--clone-all`
`delete <name> [-y]`
`show <name>`
`alias <name> [--remove] [--name NAME]`
`rename <old> <new>`
`export <name> [-o FILE]`
`.tar.gz`
`import <archive> [--name NAME]`
`.tar.gz`
`install <source> [--name N] [--alias] [--force] [-y]`
`update <name> [--force-config] [-y]`
`info <name>`

مثال‌ها:

```
hermes profile list
hermes profile create work --clone
hermes profile use work
hermes profile alias work --name h-work
hermes profile export work -o work-backup.tar.gz
hermes profile import work-backup.tar.gz --name restored
hermes profile install github.com/user/my-distro --alias
hermes profile update work
hermes -p work chat -q "Hello from work profile"
```

## `hermes completion`​

`hermes completion`

```
hermes completion [bash|zsh|fish]
```

یک اسکریپت تکمیل shell در stdout چاپ می‌کند. خروجی را در profile shell خود source کنید برای تکمیل tab دستورات Hermes، دستورات زیر سطح و نام‌های پروفایل.

مثال‌ها:

```
# Bash
hermes completion bash >> ~/.bashrc
# Zsh
hermes completion zsh >> ~/.zshrc
# Fish
hermes completion fish > ~/.config/fish/completions/hermes.fish
```

## `hermes update`​

`hermes update`

```
hermes update [--gateway] [--check] [--no-backup] [--backup] [--yes]
```

آخرین کد `hermes-agent` را می‌کشد و وابستگی‌ها را در venv مدیریت شده مجدداً نصب می‌کند، سپس هوک‌های پس از نصب را مجدداً اجرا می‌کند (سرورهای MCP، همگام‌سازی مهارت‌ها، نصب تکمیل). در یک نصب زنده اجرا ایمن است. از `--check` برای بررسی اینکه آیا checkout شما از `origin/main` عقب است بدون نصب استفاده کنید.

`hermes-agent`
`--check`
`origin/main`

`hermes update` شاخه به‌روزرسانی پیکربندی شده را می‌کشد (پیش‌فرض: `main`). اگر checkout شما روی شاخه دیگری است، Hermes ممکن است قبل از کشیدن شاخه به‌روزرسانی را checkout کند. کار شاخه را قبل از به‌روزرسانی commit کنید وقتی می‌خواهید آن را خارج از جریان autostash به‌روزرسانی نگه دارید.

`hermes update`
`main`

| گزینه | توضیح |
| --- | --- |
| `--gateway` | حالت داخلی استفاده شده توسط دستور پیام‌رسانی/`/update`. از IPC مبتنی فایل برای درخواست‌ها و پخش پیشرفت به جای خواندن از stdin ترمینال استفاده می‌کند. پرچم راه‌اندازی مجدد گیت‌وی نیست. |
| `--check` | بررسی اینکه آیا به‌روزرسانی موجود است بدون کشیدن، نصب وابستگی‌ها یا راه‌اندازی مجدد چیزی. |
| `--no-backup` | رد کردن نسخه پشتیبان قبل از به‌روزرسانی برای این اجرا، حتی اگر `updates.pre_update_backup` در `config.yaml` فعال باشد. |
| `--backup` | ایجاد یک اسناپ‌شات برچسب‌دار قبل از به‌روزرسانی از `HERMES_HOME` (پیکربندی، auth، نشست‌ها، مهارت‌ها، داده‌های جفت‌سازی) قبل از کشیدن. پیش‌فرض `off` است — رفتار همیشه-پشتیبان قبلی دقایقی به هر به‌روزرسانی در خانه‌های بزرگ اضافه می‌کرد. آن را به طور دائمی از طریق `updates.pre_update_backup: true` در `config.yaml` فعال کنید. |
| `--yes`, `-y` | فرض بله برای درخواست‌های تعاملی مانند مهاجرت پیکربندی و بازیابی stash. ورود کلید API رد می‌شود؛ `hermes config migrate` را جداگانه برای آنها اجرا کنید. |

`--gateway`
`/update`
`--check`
`--no-backup`
`updates.pre_update_backup`
`config.yaml`
`--backup`
`HERMES_HOME`
`updates.pre_update_backup: true`
`config.yaml`
`--yes`
`-y`
`hermes config migrate`

رفتار اضافی:

- **راه‌اندازی مجدد گیت‌وی.** پس از به‌روزرسانی موفق، Hermes تلاش می‌کند همه پروفایل‌های گیت‌وی در حال اجرا را به طور خودکار راه‌اندازی مجدد کند تا کد جدید را انتخاب کنند. از `hermes gateway restart` استفاده کنید وقتی می‌خواهید گیت‌وی را بدون اعمال به‌روزرسانی راه‌اندازی مجدد کنید.
- **تغییرات منبع محلی.** برای نصب‌های git، فایل‌های ردیابی شده کثیف و فایل‌های ردیابی نشده قبل از checkout یا pull شاخه به طور خودکار stash می‌شوند (`git stash push --include-untracked`). به‌روزرسانی‌های ترمینال تعاملی قبل از بازیابی stash سؤال می‌پرسند. به‌روزرسانی‌های غیرتعاملی به طور پیش‌فرض آن را بازمی‌گردانند؛ `updates.non_interactive_local_changes: discard` را فقط روی نصب‌های مدیریت شده تنظیم کنید که ویرایشهای منبع محلی باید پس از pull موفق دور ریخته شوند. اگر تعارض بازیابی stash یا pull ناموفق باشد، stash برای بازیابی دستی در جا باقی می‌ماند.
- **نوسان lockfile npm.** قبل از stash یا تعویض شاخه، Hermes تلاش بهینه برای پاک کردن تفاوت‌های `package-lock.json` ردیابی شده تولید شده توسط مراحل `npm install`/`build` انجام می‌دهد. ویرایشهای عمدی lockfile را قبل از اجرای `hermes update` commit یا stash دستی کنید.
- **اسناپ‌شات داده جفت‌سازی.** حتی وقتی `--backup` خاموش است، `hermes update` یک اسناپ‌شات سبک از `~/.hermes/pairing/` و قوانین نظر Feishu قبل از `git pull` می‌گیرد. می‌توانید آن را با `hermes backup restore --state pre-update` بازگردانید اگر pull فایلی را که در حال ویرایش آن بودید بازنویسی کند.
- **هشدار `hermes.service` قدیمی.** اگر Hermes واحد systemd `hermes.service` قدیمی را تشخیص دهد (به جای `hermes-gateway.service` فعلی)، یک نکته مهاجرت یکباره چاپ می‌کند تا از مشکلات حلقه نوسان جلوگیری کنید.
- **کدهای خروج.** `0` در موفقیت، `1` در خطاهای pull/install/post-install، `2` در تغییرات غیرمنتظره worktree که `git pull` را مسدود می‌کنند.

`hermes gateway restart`
`git stash push --include-untracked`
`updates.non_interactive_local_changes: discard`
`package-lock.json`
`hermes update`
`--backup`
`hermes update`
`~/.hermes/pairing/`
`git pull`
`hermes backup restore --state pre-update`
`hermes.service`
`hermes.service`
`hermes-gateway.service`
`0`
`1`
`2`
`git pull`

## دستورات نگهداری​

| دستور | توضیح |
| --- | --- |
| `hermes version` | چاپ اطلاعات نسخه. |
| `hermes update` | کشیدن آخرین تغییرات و نصب مجدد وابستگی‌ها. |
| `hermes postinstall` | راه‌اندازی داخلی. یک بار پس از اجرای اسکریپت نصب یا پس از `hermes update` اجرا می‌شود تا وابستگی‌های غیرپایتونی را که pip نمی‌تواند ارائه دهد نصب کند — runtime Node.js، مرورگر headless، ripgrep، ffmpeg — و سپس اگر پروفایل هنوز پیکربندی نشده `hermes setup` را فعال کند. اجرای مجدد idempotent ایمن است. |
| `hermes uninstall [--full] [--gui] [--yes]` | حذف Hermes، اختیاری حذف همه پیکربندی/داده. `--gui` فقط Chat GUI دسکتاپ را حذف می‌کند و agent را دست نخورده نگه می‌دارد؛ `--full` همچنین پیکربندی/داده را حذف می‌کند؛ `--yes` درخواستها را رد می‌کند. |

`hermes version`
`hermes update`
`hermes postinstall`
`hermes update`
`hermes setup`
`hermes uninstall [--full] [--gui] [--yes]`
`--gui`
`--full`
`--yes`

## همچنین ببینید​

- Slash Commands Reference
- CLI Interface
- Sessions
- Skills System
- Skins & Themes

[Slash Commands Reference](/docs/reference/slash-commands/)
[CLI Interface](/docs/user-guide/cli/)
[Sessions](/docs/user-guide/sessions/)
[Skills System](/docs/user-guide/features/skills/)
[Skins & Themes](/docs/user-guide/features/skins/)
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/reference/cli-commands.md)