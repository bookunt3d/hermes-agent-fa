---
layout: docs
title: "توزیع پروفایل‌ها"
permalink: /docs/user-guide/profile-distributions/
---

- 
- استفاده از Hermes
- توزیع پروفایل‌ها: به اشتراک گذاشتن یک Agent کامل

# توزیع پروفایل‌ها: به اشتراک گذاشتن یک Agent کامل

یک **توزیع پروفایل** یک agent کامل Hermes را بسته‌بندی می‌کند — شخصیت، skillها، cron jobها، اتصالات MCP، پیکربندی — به عنوان یک مخزن git. هر کسی که به مخزن دسترسی دارد می‌تواند کل agent را با یک فرمان نصب کند، به طور محلی به‌روزرسانی کند و حافظه‌ها، sessionها و کلیدهای API خود را دست‌نخورده نگه دارد.

اگر **profile** یک agent محلی است، **distribution** آن agent قابل اشتراک‌گذاری شده است.

[profile](/docs/user-guide/profiles/)

## این یعنی چه​

قبل از distributionها، به اشتراک گذاشتن یک agent Hermes به معنای فرستادن چیزی به کسی بود:

1. SOUL.md شما
2. لیست skillهایی که نصب کنید
3. config.yaml شما، به جز رازها
4. توضیح اینکه کدام سرورهای MCP را وصل کرده‌اید
5. هر cron jobی که زمان‌بندی کرده‌اید
6. دستورالعمل‌هایی برای تنظیم متغیرهای env

...و امیدوار بودند که آن را به درستی مونتاژ کنند. هر افزایش نسخه یا رفع باگ به معنای تکرار تحویل بود.

با distributionها، همه اینها در یک مخزن git زندگی می‌کند:

```
my-research-agent/├── distribution.yaml    # manifest: name, version, env-var requirements├── SOUL.md              # the agent's personality / system prompt├── config.yaml          # model, temperature, reasoning, tool defaults├── skills/              # bundled skills that come with the agent├── cron/                # scheduled tasks the agent runs└── mcp.json             # MCP servers the agent connects to
```

گیرندگان اجرا می‌کنند:

```
hermes profile install github.com/you/my-research-agent --alias
```

...و اکنون کل agent را دارند. کلیدهای API خود را پر می‌کنند (`.env.EXAMPLE` → `.env`) و می‌توانند `my-research-agent chat` اجرا کنند یا از طریق Telegram / Discord / Slack / هر پلتفرم gateway به آن پاسخ دهند. وقتی نسخه جدید push می‌کنید، `hermes profile update my-research-agent` اجرا می‌کنند و تغییرات شما را pull می‌کنند — حافظه‌ها و sessionهای آن‌ها در جای خود باقی می‌ماند.

`.env.EXAMPLE`
`.env`
`my-research-agent chat`
`hermes profile update my-research-agent`

## چرا git؟​

tarballها، آرشیوهای HTTP، فرمت سفارشی را در نظر گرفتیم. هیچ‌کدام برتر از git نیستند:

- **بدون مرحله build برای نویسندگان.** به GitHub push کنید؛ مصرف‌کنندگان نصب می‌کنند. حلقه "این را pack کنید، آن را upload کنید، index را به‌روزرسانی کنید" وجود ندارد.
- **Tagها، branchها و commitها از قبل سیستم versioning هستند.** push یک tag برای ما همان کاری را می‌کند که "pack + upload یک release" برای ابزارهای دیگر انجام می‌دهد.
- **به‌روزرسانی‌ها یک fetch هستند.** نه دانلود مجدد کل آرشیو.
- **شفاف.** کاربران می‌توانند مخزن را مرور کنند، diffهای بین نسخه‌ها را بخوانند، issue علیه آن باز کنند، آن را برای سفارشی‌سازی fork کنند.
- **مخازن خصوصی رایگان کار می‌کنند.** کلیدهای SSH، credential helperهای `git`، اعتبارنامه‌های ذخیره‌شده GitHub CLI — هر احراز هویتی که ترمinal شما از قبل تنظیم کرده به طور شفاف اعمال می‌شود.
- **تکرارپذیری یک commit SHA است.** همان چیزی که pip و npm ثبت می‌کنند.

`git credential`

**معامله:** گیرندگان به git نصب‌شده نیاز دارند. در هر ماشینی که Hermes را در ۲۰۲۶ اجرا می‌کند، این از قبل صادق است.

## چه زمانی باید از distribution استفاده کنید؟​

**مناسب:**

- **در حال به اشتراک گذاشتن یک agent تخصصی هستید** — ناظر انطباق، بازبین کد، دستیار تحقیق، بات پشتیبانی مشتری — با یک تیم یا با جامعه.
- **در حال استقرار یک agent در چندین ماشین هستید** و نمی‌خواهید هر بار فایل‌ها را دستی کپی کنید.
- **در حال تکرار یک agent هستید** و می‌خواهید گیرندگان نسخه‌های جدید را با یک فرمان دریافت کنید.
- **در حال ساخت یک agent به عنوان محصول هستید** — پیش‌فرض‌های قاطع، skillهای گلچین‌شده، promptهای تنظیم‌شده — که دیگران باید به عنوان نقطه شروع استفاده کنند.

**مناسب نیست:**

- فقط می‌خواهید یک profile را در ماشین خود پشتیبان بگیرید. از `hermes profile export/import` استفاده کنید — برای همین هستند.
- می‌خواهید کلیدهای API را همراه agent به اشتراک بگذارید. `auth.json` و `.env` عمداً از distributionها حذف شده‌اند. هر نصب‌کننده اعتبارنامه‌های خود را می‌آورد.
- می‌خواهید حافظه‌ها / sessionها / تاریخچه مکالمه را به اشتراک بگذارید. آن‌ها داده کاربر هستند، نه محتوای distribution. هرگز ارسال نمی‌شوند.

[hermes profile export/import](/docs/reference/profile-commands#hermes-profile-export)
`hermes profile export`
`import`
`auth.json`
`.env`

**Hermes git را کنترل نمی‌کند.** حذف‌های فایل توصیف‌شده در این صفحه توسط **نصب‌کننده** اعمال می‌شوند وقتی کسی `hermes profile install` یا `hermes profile update` اجرا می‌کند. هنگام اجرای `git add` یا `git commit` اعمال **نمی‌شوند**.

`hermes profile install`
`hermes profile update`
`git add`
`git commit`

## چرخه حیات: نویسنده تا نصب‌کننده تا به‌روزرسانی​

در زیر کل جریان end-to-end است. طرفی را که به آن اهمیت می‌دهید انتخاب کنید.

## برای نویسندگان: انتشار یک distribution​

### مرحله ۱ — شروع از یک profile کارکردی​

Agent را مانند هر profile دیگری بسازید و ظریف کنید:

```
hermes profile create research-botresearch-bot setup                    # configure model, API keys# Edit ~/.hermes/profiles/research-bot/SOUL.md# Install skills, wire up MCP servers, schedule cron jobs, etc.research-bot chat                     # dogfood until it feels right
```

### مرحله ۲ — اضافه کردن `distribution.yaml`​

`distribution.yaml`

`~/.hermes/profiles/research-bot/distribution.yaml` را ایجاد کنید:

`~/.hermes/profiles/research-bot/distribution.yaml`

```
name: research-botversion: 1.0.0description: "Autonomous research assistant with arXiv and web tools"hermes_requires: ">=0.12.0"author: "Your Name"license: "MIT"# Tell installers which env vars the agent needs. These are checked against# the installer's shell and existing .env file so they don't get nagged# about keys they already have configured.env_requires:  - name: OPENAI_API_KEY    description: "OpenAI API key (for model access)"    required: true  - name: SERPAPI_KEY    description: "SerpAPI key for web search"    required: false    default: ""
```

این کل manifest است. هر فیلد به جز `name` پیش‌فرض معقولی دارد.

`name`

### مرحله ۳ — ایجاد `.gitignore` قبل از اولین commit​

`.gitignore`

**قبل** از اجرای `git init` یا `git add` این کار را انجام دهید. اگر قبلاً با profile چت کرده‌اید، setup اجرا کرده‌اید یا به هر نحو دیگری از آن استفاده کرده‌اید، دایرکتوری اکنون حاوی فایل‌هایی است که نباید ارسال کنید: `.env`، `auth.json`، `memories/`، `sessions/`، `state.db*`، `logs/` و غیره.

`git init`
`git add`
`.env`
`auth.json`
`memories/`
`sessions/`
`state.db*`
`logs/`

`~/.hermes/profiles/research-bot/.gitignore` را با حداقل این‌ها ایجاد کنید:

`~/.hermes/profiles/research-bot/.gitignore`

```
# Credentials & secrets — NEVER commitauth.json.env.env.EXAMPLE    # generated by install, not authorship domain# Runtime databases & statestate.dbstate.db-shmstate.db-walhermes_state.dbresponse_store.dbresponse_store.db-shmresponse_store.db-walgateway.pidgateway_state.jsonprocesses.jsonauth.lockactive_profile.update_check# User data — NEVER commitmemories/sessions/logs/plans/workspace/home/# Caches & generated artifactsimage_cache/audio_cache/document_cache/browser_screenshots/cache/# Infrastructure (should not be in profile dir, but safe to exclude)hermes-agent/.worktrees/profiles/bin/node_modules/# User customization namespace — your local overrideslocal/# Checkpoints & backups (can be huge)checkpoints/sandboxes/backups/# Logserrors.log.hermes_history
```

این بازتاب مسیرهای **hard-excluded** است که نصب‌کننده در انتهای خود حذف می‌کند. هر چیز دیگری که می‌خواهید از مخزن خارج نگه دارید (فایل‌های موقت، دارایی‌های بزرگ، skillهای فقط محلی) باید اینجا نیز قرار بگیرد.

### مرحله ۴ — Push به یک مخزن git​

```
cd ~/.hermes/profiles/research-botgit initgit add .git commit -m "v1.0.0"git remote add origin git@github.com:you/research-bot.gitgit tag v1.0.0git push -u origin main --tags
```

مخزن اکنون یک distribution است. هر کسی که دسترسی دارد می‌تواند آن را نصب کند.

نصب‌کننده علاوه بر این مسیرهای hard-excluded را حتی اگر نویسنده به نحوی آن‌ها را ارسال کند حذف می‌کند — اما این فقط نصب‌کنندگان را محافظت می‌کند، نه نویسنده را.

### مرحله ۵ — Tag نسخه‌های versioned​

هر بار که agent به یک نقطه پایدار می‌رسد، نسخه را افزایش و tag کنید:

```
# Edit distribution.yaml: version: 1.1.0git add distribution.yaml SOUL.md skills/git commit -m "v1.1.0: tighter research SOUL, add arxiv skill"git tag v1.1.0git push --tags
```

گیرندگانی که `hermes profile update research-bot` اجرا می‌کنند آخرین نسخه را pull خواهند کرد.

`hermes profile update research-bot`

### ظاهر مخزن​

یک distribution نوشته‌شده کامل:

```
research-bot/├── .gitignore                   # excludes secrets & user data (see Step 3)├── distribution.yaml            # required├── SOUL.md                      # strongly recommended├── config.yaml                  # model, provider, tool defaults├── mcp.json                     # MCP server connections├── skills/│   ├── arxiv-search/SKILL.md│   ├── paper-summarization/SKILL.md│   └── citation-lookup/SKILL.md├── cron/│   └── weekly-digest.json       # scheduled tasks└── README.md                    # human-facing description (optional)
```

### Distribution-owned در مقابل User-owned​

وقتی نصب‌کننده به نسخه جدید به‌روزرسانی می‌کند، برخی چیزها جایگزین می‌شوند (دامنه نویسنده) و برخی در جای خود باقی می‌مانند (دامنه نصب‌کننده). پیش‌فرض‌ها:

| دسته | مسیرها | هنگام به‌روزرسانی |
| --- | --- | --- |
| Distribution-owned | `SOUL.md`، `config.yaml`، `mcp.json`، `skills/`، `cron/`، `distribution.yaml` | از clone جدید جایگزین می‌شوند |
| Config override | `config.yaml` | در واقع به طور پیش‌فرض حفظ می‌شود — نصب‌کننده ممکن است مدل یا provider را تنظیم کرده باشد. هنگام به‌روزرسانی `--force-config` برای بازنشانی پاس دهید. |
| User-owned | `memories/`، `sessions/`، `state.db*`، `auth.json`، `.env`، `logs/`، `workspace/`، `plans/`، `home/`، `*_cache/`، `local/` | هرگز دست‌کاری نمی‌شوند |

`SOUL.md`
`config.yaml`
`mcp.json`
`skills/`
`cron/`
`distribution.yaml`
`config.yaml`
`--force-config`
`memories/`
`sessions/`
`state.db*`
`auth.json`
`.env`
`logs/`
`workspace/`
`plans/`
`home/`
`*_cache/`
`local/`

می‌توانید لیست distribution-owned را در manifest override کنید:

```
distribution_owned:  - SOUL.md  - skills/research/            # only my research skills; other installed skills stay  - cron/digest.json
```

وقتی حذف می‌شود، پیش‌فرض‌های بالا اعمال می‌شوند — که همان چیزی است که بیشتر distributionها می‌خواهند.

## برای نصب‌کنندگان: استفاده از یک distribution​

### نصب​

```
hermes profile install github.com/you/research-bot --alias
```

**چه اتفاقی می‌افتد:**

1. مخزن را در یک دایرکتوری موقت clone می‌کند.
2. `distribution.yaml` را می‌خواند، manifest را (نام، نسخه، توضیحات، نویسنده، متغیرهای env مورد نیاز) نشان می‌دهد.
3. هر متغیر env مورد نیاز را با محیط shell شما و `.env` موجود profile هدف بررسی می‌کند. هر کدام را به عنوان `✓ set` یا `needs setting` علامت‌گذاری می‌کند تا دقیقاً بدانید چه چیزی پیکربندی کنید.
4. درخواست تأیید می‌کند. `-y`/`--yes` برای رد کردن پاس دهید.
5. فایل‌های distribution-owned را به `~/.hermes/profiles/research-bot/` (یا هر جا که `name` manifest حل می‌شود) کپی می‌کند. مسیرهای **hard-excluded** در حین این کپی حذف می‌شوند، حتی اگر نویسنده به طور تصادفی آن‌ها را در مخزن باقی گذاشته باشد.
6. `.env.EXAMPLE` با کلیدهای مورد نیاز کامنت‌شده می‌نویسد — به `.env` کپی کرده و پر کنید.
7. با `--alias`، یک wrapper ایجاد می‌کند تا بتوانید `research-bot chat` را مستقیماً اجرا کنید.

`distribution.yaml`
`.env`
`✓ set`
`needs setting`
`-y`
`--yes`
`~/.hermes/profiles/research-bot/`
`name`
`.env.EXAMPLE`
`.env`
`--alias`
`research-bot chat`

### انواع منبع​

هر git URL کار می‌کند:

```
# GitHub shorthandhermes profile install github.com/you/research-bot# Full HTTPShermes profile install https://github.com/you/research-bot.git# SSHhermes profile install git@github.com:you/research-bot.git# Self-hosted, GitLab, Gitea, Forgejo — any Git hosthermes profile install https://git.example.com/team/research-bot.git# Private repo using your configured git authhermes profile install git@github.com:your-org/internal-bot.git# Local directory during development (no git push needed)hermes profile install ~/my-profile-in-progress/
```

### Override نام profile​

دو کاربر که می‌خواهند همان distribution را با نام‌های profile مختلف داشته باشند:

```
# Alicehermes profile install github.com/acme/support-bot --name support-us --alias# Bob (same distribution, different local name)hermes profile install github.com/acme/support-bot --name support-eu --alias
```

### پر کردن متغیرهای env​

پس از نصب، profile agent حاوی یک `.env.EXAMPLE`:

`.env.EXAMPLE`

```
# Environment variables required by this Hermes distribution.# Copy to `.env` and fill in your own values before running.# OpenAI API key (for model access)# (required)OPENAI_API_KEY=# SerpAPI key for web search# (optional)# SERPAPI_KEY=
```

آن را کپی کنید:

```
cp ~/.hermes/profiles/research-bot/.env.EXAMPLE ~/.hermes/profiles/research-bot/.env# Edit .env, paste your real keys
```

کلیدهای مورد نیاز که قبلاً در محیط shell شما بودند (مثلاً `OPENAI_API_KEY` export شده در `~/.zshrc` شما) هنگام نصب به عنوان `✓ set` علامت‌گذاری می‌شوند — نیازی به تکرار آن‌ها در `.env` نیست.

`OPENAI_API_KEY`
`~/.zshrc`
`✓ set`
`.env`

### بررسی چه نصب کرده‌اید​

```
hermes profile info research-bot
```

**نمایش می‌دهد:**

```
Distribution: research-botVersion:      1.0.0Description:  Autonomous research assistant with arXiv and web toolsAuthor:       Your NameRequires:     Hermes >=0.12.0Source:       https://github.com/you/research-botInstalled:    2026-05-08T17:04:32+00:00Environment variables:  OPENAI_API_KEY (required) — OpenAI API key (for model access)  SERPAPI_KEY (optional) — SerpAPI key for web search
```

`hermes profile list` همچنین ستون `Distribution` نشان می‌دهد تا یک نگاه سریع ببینید کدام profileهای شما از مخازن آمده و کدام را دستی ساخته‌اید:

`hermes profile list`
`Distribution`

```
 Profile          Model                        Gateway      Alias        Distribution ───────────────    ───────────────────────────    ───────────    ───────────    ──────────────────── ◆default         claude-sonnet-4              stopped      —            —  coder           gpt-5                        stopped      coder        —  research-bot    claude-opus-4                stopped      research-bot research-bot@1.0.0  telemetry       claude-sonnet-4              running      telemetry    telemetry@2.3.1
```

### به‌روزرسانی​

```
hermes profile update research-bot
```

**چه اتفاقی می‌افتد:**

1. مخزن را از URL منبع ضبط‌شده دوباره clone می‌کند.
2. فایل‌های distribution-owned (SOUL، skillها، cron، `mcp.json`) را جایگزین می‌کند.
3. `config.yaml` **شما** را حفظ می‌کند — ممکن است مدل، temperature یا تنظیمات دیگر را تنظیم کرده باشید. `--force-config` برای بازنویسی پاس دهید.
4. **هرگز** به داده‌های کاربر دست نمی‌زند: حافظه‌ها، sessionها، احراز هویت، `.env`، لاگ‌ها، state.

`config.yaml`
`--force-config`
`.env`

**بدون دانلود مجدد کل آرشیو. بدون لگد زدن تغییرات محلی شما به config. بدون حذف تاریخچه مکالمه شما.**

### حذف​

```
hermes profile delete research-bot
```

پرامپت حذف اطلاعات distribution را قبل از درخواست تأیید نمایش می‌دهد:

```
Profile: research-botPath:    ~/.hermes/profiles/research-botModel:   claude-opus-4 (anthropic)Skills:  12Distribution: research-bot@1.0.0Installed from: https://github.com/you/research-botThis will permanently delete:  • All config, API keys, memories, sessions, skills, cron jobs  • Command alias (~/.local/bin/research-bot)Type 'research-bot' to confirm:
```

بنابراین هرگز تصادفاً agent را بدون دانستن اینکه از کجا آمده یا توانایی نصب مجدد حذف نمی‌کنید.

## موارد استفاده و الگوها​

### شخصی: همگام‌سازی یک agent بین ماشین‌ها​

یک دستیار تحقیق روی لپ‌تاپ خود ساخته‌اید. همان agent را روی workstation خود می‌خواهید.

```
# Laptop — create .gitignore first (see "For authors" Step 3), then:cd ~/.hermes/profiles/research-botgit init && git add . && git status   # confirm no secrets stagedgit commit -m "initial"git remote add origin git@github.com:you/research-bot.gitgit push -u origin main# Workstationhermes profile install github.com/you/research-bot --alias# Fill in .env. Done.
```

هر تکرار روی لپ‌تاپ (`git commit && push`) روی workstation با `hermes profile update research-bot` pull می‌شود. حافظه‌ها به ازای هر ماشین باقی می‌مانند — لپ‌تاپ مکالمات خود را به یاد می‌آورد، workstation خودش را، تداخل ندارند.

`git commit && push`
`hermes profile update research-bot`

### تیم: ارسال یک agent داخلی بازبینی‌شده​

تیم مهندسی شما یک بات بازبینی PR مشترک با SOUL خاص، skillهای خاص و cron می‌خواهد که هر PR را از طریق آن اجرا کند.

```
# Engineering lead — create .gitignore first (see "For authors" Step 3), then:cd ~/.hermes/profiles/pr-reviewer# ... build and tune ...git init && git add . && git status   # confirm no secrets stagedgit commit -m "v1.0 PR reviewer"git tag v1.0.0git push -u origin main --tags    # push to your company's internal Git host# Each engineerhermes profile install git@github.com:your-org/pr-reviewer.git --alias# Fill in .env with their own API key (billed to them), .env.EXAMPLE points at what's requiredpr-reviewer chat
```

وقتی lead نسخه ۱.۱ (SOUL بهتر، skill جدید) ارسال می‌کند، مهندسان `hermes profile update pr-reviewer` اجرا می‌کنند و همه ظرف چند دقیقه روی نسخه جدید هستند.

`hermes profile update pr-reviewer`

### جامعه: انتشار یک agent عمومی​

چیز نوآورانه‌ای ساخته‌اید — شاید یک "معامله‌گر Polymarket" یا "خلاصه‌ساز مقاله آکادمیک" یا "دستیار عملیات سرور Minecraft". می‌خواهید آن را به اشتراک بگذارید.

```
# You — create .gitignore first (see "For authors" Step 3), then:cd ~/.hermes/profiles/polymarket-trader# Write a solid README.md at the repo root — GitHub shows it on the repo pagegit init && git add . && git status   # confirm no secrets stagedgit commit -m "v1.0"git tag v1.0.0# Publish to a public GitHub repogit remote add origin https://github.com/you/hermes-polymarket-trader.gitgit push -u origin main --tags# Anyonehermes profile install github.com/you/hermes-polymarket-trader --alias
```

دستور نصب را توییت کنید. افرادی که آن را امتحان می‌کنند issue و PR برای شما ارسال می‌کنند. اگر کسی بخواهد سفارشی کند، fork می‌کند — همان گردش کار git که همه از قبل می‌شناسند.

### محصول: ارسال یک agent قاطع​

Hermes-on-top ساخته‌اید — شاید یک framework نظارت انطباق، یک stack پشتیبانی مشتری، یک پلتفرم تحقیق تخصصی. می‌خواهید آن را به عنوان محصول توزیع کنید.

```
# distribution.yamlname: telemetry-harnessversion: 2.3.1description: "Compliance telemetry harness — monitors and reviews regulated workflows"hermes_requires: ">=0.13.0"author: "Acme Compliance Inc."license: "Commercial"env_requires:  - name: ACME_API_KEY    description: "Your Acme Compliance license key (email support@acme.com)"    required: true  - name: OPENAI_API_KEY    description: "OpenAI API key for model access"    required: true  - name: GRAPHITI_MCP_URL    description: "URL for your Graphiti knowledge graph instance"    required: false    default: "http://127.0.0.1:8000/sse"
```

مشتریان شما با یک فرمان واحد نصب می‌کنند؛ پیش‌نمایش نصب دقیقاً به آن‌ها می‌گوید چه کلیدهایی آماده داشته باشند؛ به‌روزرسانی‌ها لحظه‌ای که نسخه جدید tag می‌کنید ارسال می‌شوند؛ داده‌های انطباق (`memories/`، `sessions/`) هرگز ماشین آن‌ها را ترک نمی‌کند.

`memories/`
`sessions/`

### موقت: اسکریپت‌های یک‌باره روی زیرساخت مشترک​

شما سرپرست ops هستید. یک agent موقت می‌خواهید که یک حادثه production را تشخیص دهد — SOUL آماده با ابزارها و اتصالات MCP مناسب — و روی لپ‌تاپ‌های سه مهندس on-call برای هفته آینده اجرا شود.

```
# You — create .gitignore first (see "For authors" Step 3), then:# Build the profile, commit, push a private repogit push -u origin main# Each on-callhermes profile install git@github.com:your-org/incident-2026-q2.git --alias# Incident resolved — tear it downhermes profile delete incident-2026-q2
```

چرخه نصب-حذف به اندازه کافی ارزان است که یکبار مصرف باشد.

## دستورالعمل‌ها​

### ثابت کردن به یک نسخه مشخص​

Git ref pinning (`#v1.2.0`) برنامه‌ریزی شده اما در انتشار اولیه موجود نیست — نصب در حال حاضر branch پیش‌فرض را ردیابی می‌کند. نسخه نصب‌شده را از طریق `hermes profile info <name>` ردیابی کنید و تا آماده شوید از به‌روزرسانی‌ها خودداری کنید.

`#v1.2.0`
`hermes profile info <name>`

### بررسی نسخه فعلی در مقابل آخرین​

```
# Your installed versionhermes profile info research-bot | grep Version# Latest upstream (without installing)git ls-remote --tags https://github.com/you/research-bot | tail -5
```

### حفظ سفارشی‌سازی‌های config محلی در به‌روزرسانی‌ها​

رفتار به‌روزرسانی پیش‌فرض این کار را انجام می‌دهد: `config.yaml` حفظ می‌شود. برای ایمنی، تنظیمات محلی خود را در فایلی بنویسید که distribution مالک آن نیست:

`config.yaml`

```
# ~/.hermes/profiles/research-bot/local/my-overrides.yaml# (distribution never touches local/)
```

...و در صورت نیاز از `config.yaml` یا SOUL خود به آن ارجاع دهید.

`config.yaml`

### اجبار یک نصب تمیز مجدد​

```
# Nuke and re-install from scratch (loses memories/sessions too)hermes profile delete research-bot --yeshermes profile install github.com/you/research-bot --alias# Update to current main but reset config.yaml to the distribution's defaulthermes profile update research-bot --force-config --yes
```

### Fork و سفارشی‌سازی​

گردش کار استاندارد git — distributionها فقط مخزن هستند:

```
# Fork the repo on GitHub, then install your forkhermes profile install github.com/yourname/forked-research-bot --alias# Iterate locally in ~/.hermes/profiles/forked-research-bot/# Edit SOUL.md, commit, push to your fork# Upstream changes: pull them into your fork the usual way
```

### تست یک distribution قبل از push​

از ماشین نویسنده:

```
# Install from a local directory (no git push needed)hermes profile install ~/.hermes/profiles/research-bot --name research-bot-test --alias# Tweak, delete, re-install until it's righthermes profile delete research-bot-test --yeshermes profile install ~/.hermes/profiles/research-bot --name research-bot-test
```

## چه چیزی در distribution نیست (هرگز)​

نصب‌کننده این مسیرها را **hard-exclude** می‌کند حتی اگر نویسنده به طور تصادفی آن‌ها را ارسال کند. هیچ گزینه پیکربندی اجازه override نمی‌دهد — محافظ ایمنی یک invariant با regression test است:

- `auth.json` — توکن‌های OAuth، اعتبارنامه‌های پلتفرم
- `.env` — کلیدهای API، رازها
- `memories/` — حافظه مکالمه
- `sessions/` — تاریخچه مکالمه
- `state.db`، `state.db-shm`، `state.db-wal` — metadata session
- `logs/` — لاگ‌های agent و خطا
- `workspace/` — فایل‌های کاری تولیدشده
- `plans/` — planهای موقت
- `home/` — mount خانه کاربر در backendهای Docker
- `*_cache/` — کش تصویر / صوت / سند
- `local/` — فضای نام سفارشی‌سازی رزرو شده توسط کاربر

`auth.json`
`.env`
`memories/`
`sessions/`
`state.db`
`state.db-shm`
`state.db-wal`
`logs/`
`workspace/`
`plans/`
`home/`
`*_cache/`
`local/`

وقتی distribution را به عنوان نصب‌کننده clone می‌کنید، اینها به طور ساده به دایرکتوری profile شما کپی **نمی‌شوند**. هنگام به‌روزرسانی، کپی‌های شما در جای خود باقی می‌مانند. اگر همان distribution را روی پنج ماشین نصب کرده باشید، پنج مجموعه ایزوله از این داده دارید — یکی به ازای هر ماشین.

این حذف در **زمان نصب / به‌روزرسانی** روی ماشین نصب‌کننده اجرا می‌شود. **جلوی نویسنده را از commit فایل‌های حساس/غیرضروری نمی‌گیرد.** نویسندگان باید از `.gitignore` برای خارج نگه داشتن رازها از مخزن استفاده کنند.

`.gitignore`

## امنیت و اعتماد​

Profile distributions به طور پیش‌فرض unsigned هستند. به این‌ها اعتماد می‌کنید:

- **میزبان git** (GitHub / GitLab / هر جا) برای سرو بایت‌هایی که نویسنده push کرده.
- **نویسنده** برای ارسال نکردن SOUL، skillها یا cron jobهای مخرب.

Cron jobهای از یک distribution **به طور خودکار زمان‌بندی نمی‌شوند** — نصب‌کننده `hermes -p <name> cron list` چاپ می‌کند و شما صریحاً آن‌ها را فعال می‌کنید. SOUL.md و skillها **محرک** هستند به محض شروع چت با profile، بنابراین قبل از اولین اجرا آن‌ها را بخوانید اگر از کسی که نمی‌شناسید نصب می‌کنید.

`hermes -p <name> cron list`

**تشبیه تقریبی:** نصب یک distribution مانند نصب یک افزونه مرورگر یا افزونه VS Code است. اصطکاک کم، قدرت بالا، به منبع اعتماد کنید. برای distributionهای داخلی شرکت، از مخزن خصوصی و احراز هویت git عادی خود استفاده کنید — چیز جدیدی برای پیکربندی نیست.

## آینده​

نسخه‌های آینده ممکن است امضا، lockfile (`.distribution-lock.yaml`) با یک commit SHA حل‌شده و flag `--dry-run` که diff را قبل از اعمال به‌روزرسانی چاپ می‌کند اضافه کنند. هیچ‌کدام هنوز ارسال نشده‌اند.

`.distribution-lock.yaml`
`--dry-run`

## زیر پوشش​

برای جزئیات پیاده‌سازی، رفتار دقیق CLI و همه flagها، [مرجع Profile Commands](/docs/reference/profile-commands#distribution-commands) را ببینید.

[مرجع Profile Commands](/docs/reference/profile-commands#distribution-commands)

نسخه کوتاه:

- `install`، `update`، `info` داخل `hermes profile` زندگی می‌کنند — نه یک درخت دستور موازی.
- فرمت manifest YAML با یک اسکوپا کوچک مورد نیاز است (فقط `name`).
- نصب‌کننده `git` محلی شما را برای clone استفاده می‌کند، بنابراین هر احراز هویتی که shell شما از قبل مدیریت می‌کند به طور شفاف کار می‌کند.
- پس از clone، `.git/` حذف می‌شود — profile نصب‌شده خودش یک git checkout نیست، از دام‌های "اوه، من تصادفاً `.env` خود را به تاریخچه git distribution commit کردم" جلوگیری می‌کند.
- نام‌های profile رزرو شده (`hermes`، `test`، `tmp`، `root`، `sudo`) هنگام نصب رد می‌شوند تا از تداخل با باینری‌های رایج جلوگیری شود.

`install`
`update`
`info`
`hermes profile`
`name`
`git`
`.git/`
`.env`
`hermes`
`test`
`tmp`
`root`
`sudo`

## همچنین ببینید​

- [Profileها: اجرای چندین Agent](/docs/user-guide/profiles/) — مفهوم پایه
- [مرجع Profile Commands](/docs/reference/profile-commands/) — هر flag، هر گزینه
- [hermes profile export/import](/docs/reference/profile-commands#hermes-profile-export) — پشتیبان / بازیابی محلی (نه distribution)
- [استفاده از SOUL با Hermes](/docs/guides/use-soul-with-hermes/) — نوشتن شخصیت‌ها
- [شخصیت و SOUL](/docs/user-guide/features/personality/) — چگونه SOUL در agent جا می‌شود
- [کاتالوگ Skillها](/docs/reference/skills-catalog/) — skillهایی که می‌توانید بسته‌بندی کنید

[Profileها: اجرای چندین Agent](/docs/user-guide/profiles/)
[مرجع Profile Commands](/docs/reference/profile-commands/)
[hermes profile export/import](/docs/reference/profile-commands#hermes-profile-export)
`hermes profile export`
`import`
[استفاده از SOUL با Hermes](/docs/guides/use-soul-with-hermes/)
[شخصیت و SOUL](/docs/user-guide/features/personality/)
[کاتالوگ Skillها](/docs/reference/skills-catalog/)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/profile-distributions.md)