---
layout: docs
title: "استفاده از MCP"
permalink: /docs/guides/use-mcp-with-hermes/
---

- 
- Guides & Tutorials
- Use MCP with Hermes

# استفاده از MCP با Hermes

این راهنما نشان می‌دهد چگونه واقعاً از MCP با Hermes Agent در workflowهای روزمره استفاده کنید.

اگر صفحه ویژگی توضیح می‌دهد MCP چیست، این راهنما درباره نحوه دریافت ارزش از آن به سرعت و به طور ایمن است.

## چه زمانی باید از MCP استفاده کنید؟

از MCP استفاده کنید وقتی:

- ابزاری از قبل به شکل MCP وجود دارد و نمی‌خواهید یک ابزار بومی Hermes بسازید
- می‌خواهید Hermes از طریق یک لایه RPC تمیز با یک سیستم محلی یا راه دور کار کند
- کنترل دقیق نمایش به ازای هر سرور می‌خواهید
- می‌خواهید Hermes را به APIهای داخلی، پایگاه‌های داده یا سیستم‌های شرکت متصل کنید بدون تغییر هسته Hermes

از MCP استفاده نکنید وقتی:

- یک ابزار داخلی Hermes از قبل کار را به خوبی انجام می‌دهد
- سرور یک سطح ابزار خطرناک عظیم را در معرض دید قرار می‌دهد و آماده فیلتر کردن آن نیستید
- فقط به یک ادغام بسیار باریک نیاز دارید و یک ابزار بومی ساده‌تر و ایمن‌تر خواهد بود

## مدل ذهنی

MCP را به عنوان یک لایه adapter در نظر بگیرید:

- Hermes agent باقی می‌ماند
- سرورهای MCP ابزارها را ارائه می‌دهند
- Hermes این ابزارها را در زمان راه‌اندازی یا بارگذاری مجدد کشف می‌کند
- مدل می‌تواند مانند ابزارهای عادی از آنها استفاده کند
- شما کنترل می‌کنید هر سرور چقدر قابل مشاهده باشد

آن بخش آخر مهم است. استفاده خوب MCP فقط «همه چیز را متصل کن» نیست. «درست را با کوچک‌ترین سطح مفید متصل کن» است.

## مرحله ۱: نصب پشتیبانی MCP

اگر Hermes را با اسکریپت نصب استاندارد نصب کرده‌اید، پشتیبانی MCP از قبل شامل شده است (نصب‌کننده `uv pip install -e ".[all]"` را اجرا می‌کند).

`uv pip install -e ".[all]"`

اگر بدون extras نصب کرده‌اید و نیاز دارید MCP را جداگانه اضافه کنید:

```
cd ~/.hermes/hermes-agentuv pip install -e ".[mcp]"
```

برای سرورهای مبتنی بر npm، مطمئن شوید Node.js و `npx` در دسترس هستند.

`npx`

برای بسیاری از سرورهای Python MCP، `uvx` یک گزینه خوب پیش‌فرض است.

`uvx`

## مرحله ۲: ابتدا یک سرور اضافه کنید

با یک سرور ایمن شروع کنید.

مثال: دسترسی فایل‌سیستم فقط به یک دایرکتوری پروژه.

```
mcp_servers:  project_fs:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]
```

سپس Hermes را راه‌اندازی کنید:

```
hermes chat
```

حالا چیز مشخصی بپرسید:

```
Inspect this project and summarize the repo layout.
```

## مرحله ۳: تأیید بارگذاری MCP

می‌توانید MCP را به چند روش تأیید کنید:

- بنر/وضعیت Hermes باید ادغام MCP را هنگام پیکربندی نشان دهد
- از Hermes بپرسید چه ابزارهایی در دسترس دارد
- پس از تغییرات config از `/reload-mcp` استفاده کنید
- اگر سرور نتوانست متصل شود، لاگ‌ها را بررسی کنید

`/reload-mcp`

یک پرامپت آزمایشی عملی:

```
Tell me which MCP-backed tools are available right now.
```

## مرحله ۴: بلافاصله شروع به فیلتر کردن کنید

اگر سرور ابزارهای زیادی را در معرض دید قرار می‌دهد، منتظر نمانید.

### مثال: فقط آنچه می‌خواهید را لیست سفید کنید

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, search_code]
```

این معمولاً بهترین پیش‌فرض برای سیستم‌های حساس است.

## WSL2: اتصال Hermes در WSL به Windows Chrome

این راه‌اندازی عملی وقتی است که:

- Hermes در WSL2 اجرا می‌شود
- مرورگری که می‌خواهید کنترل کنید Chrome معمولی شما در ویندوز است که وارد شده‌اید
- `/browser connect` از WSL ناخوشایند یا غیرقابل اعتماد است

`/browser connect`

در این راه‌اندازی، Hermes مستقیماً به Chrome متصل نمی‌شود. در عوض:

- Hermes در WSL اجرا می‌شود
- Hermes یک سرور stdio MCP محلی راه‌اندازی می‌کند
- آن سرور MCP از طریق windows interop (`cmd.exe` یا `powershell.exe`) راه‌اندازی می‌شود
- سرور MCP به نشست Chrome زنده ویندوز شما متصل می‌شود

`cmd.exe`
`powershell.exe`

مدل ذهنی:

```
Hermes (WSL) -> MCP stdio bridge -> Windows Chrome
```

### چرا این حالت مفید است

- پروفایل مرورگر واقعی ویندوز، کوکی‌ها و ورودهای خود را حفظ می‌کنید
- Hermes در محیط پشتیبانی‌شده Unix خود (WSL2) باقی می‌ماند
- کنترل مرورگر به عنوان ابزارهای MCP در معرض دید قرار می‌گیرد به جای تکیه بر انتقال مرورگر هسته Hermes

### سرور توصیه شده

از `chrome-devtools-mcp` استفاده کنید.

`chrome-devtools-mcp`

اگر Chrome ویندوز شما قبلاً از `chrome://inspect/#remote-debugging` debugging از راه دور زنده فعال دارد، آن را اینگونه از WSL اضافه کنید:

`chrome://inspect/#remote-debugging`

```
hermes mcp add chrome-devtools-win --command cmd.exe --args /c npx -y chrome-devtools-mcp@latest --autoConnect --no-usage-statistics
```

پس از ذخیره سرور:

```
hermes mcp test chrome-devtools-win
```

سپس یک نشست تازه Hermes شروع کنید یا اجرا کنید:

```
/reload-mcp
```

### پرامپت معمول

پس از بارگذاری، Hermes می‌تواند مستقیماً از ابزارهای مرورگر با پیشوند MCP استفاده کند. مثلاً:

```
调用 MCP 工具 mcp_chrome_devtools_win_list_pages，列出当前浏览器标签页。
```

### چه زمانی `/browser connect` ابزار اشتباهی است

`/browser connect`

اگر Hermes در WSL اجرا می‌شود و Chrome در ویندوز، `/browser connect` ممکن است ناموفق باشد حتی اگر Chrome باز و قابل debugging باشد.

`/browser connect`

دلایل رایج:

- WSL نمی‌تواند به همان endpoint host-local که Chrome در معرض ابزارهای ویندوز قرار می‌دهد برسد
- جریان‌های debugging زنده Chrome جدیدتر مشابه `ws://localhost:9222` کلاسیک نیستند
- مرورگر از یک helper سمت ویندوز مانند `chrome-devtools-mcp` آسان‌تر متصل می‌شود

`ws://localhost:9222`
`chrome-devtools-mcp`

در آن موارد، `/browser connect` را برای تنظیمات همان محیط نگه دارید و از MCP برای اتصال مرورگر WSL به ویندوز استفاده کنید.

`/browser connect`

### دام‌های شناخته‌شده

- Hermes را از یک مسیر mount شده در ویندوز مانند `/mnt/c/Users/<you>` یا `/mnt/c/workspace/...` هنگام استفاده از ابزارهای stdio ویندوز از طریق MCP راه‌اندازی کنید.
- اگر Hermes را از `/root` یا `/home/...` راه‌اندازی کنید، ویندوز ممکن است یک هشدار current-directory UNC قبل از شروع سرور MCP منتشر کند.
- اگر `chrome-devtools-mcp --autoConnect` هنگام فهرست کردن صفحات timeout شود، تب‌های پس‌زمینه/منجمد در Chrome را کاهش دهید و دوباره تلاش کنید.

`/mnt/c/Users/<you>`
`/mnt/c/workspace/...`
`/root`
`/home/...`
`UNC`
`chrome-devtools-mcp --autoConnect`

### مثال: لیست سیاه اقدامات خطرناک

```
mcp_servers:  stripe:    url: "https://mcp.stripe.com"    headers:      Authorization: "Bearer ***"    tools:      exclude: [delete_customer, refund_payment]
```

### مثال: غیرفعال کردن wrapperهای کمکی نیز

```
mcp_servers:  docs:    url: "https://mcp.docs.example.com"    tools:      prompts: false      resources: false
```

## فیلتر کردن واقعاً چه چیزی را تحت تأثیر قرار می‌دهد؟

دو دسته از عملکرد MCP در Hermes وجود دارد:

۱. ابزارهای بومی سرور MCP

- با `tools.include` / `tools.exclude` فیلتر می‌شوند

`tools.include`
`tools.exclude`

۲. wrapperهای کمکی اضافه‌شده توسط Hermes

- با `tools.resources` / `tools.prompts` فیلتر می‌شوند

`tools.resources`
`tools.prompts`

### wrapperهای کمکی که ممکن است ببینید

منابع:

- `list_resources`
- `read_resource`

پرامپت‌ها:

- `list_prompts`
- `get_prompt`

این wrapperها فقط زمانی ظاهر می‌شوند که:

- config شما آنها را مجاز بداند، و
- جلسه سرور MCP واقعاً از آن قابلیت‌ها پشتیبانی کند

بنابراین Hermes وانمود نمی‌کند سرور منابع/پرامپت‌ها دارد اگر ندارد.

## الگوهای رایج

### الگو ۱: دستیار پروژه محلی

از MCP برای فایل‌سیستم یا سرور git محلی پروژه استفاده کنید وقتی می‌خواهید Hermes در یک فضای کاری محدود استدلال کند.

```
mcp_servers:  fs:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"]  git:    command: "uvx"    args: ["mcp-server-git", "--repository", "/home/user/project"]
```

پرامپت‌های خوب:

```
Review the project structure and identify where configuration lives.
```

```
Check the local git state and summarize what changed recently.
```

### الگو ۲: سوابق کاری بومی repo با Open Scaffold

از Open Scaffold استفاده کنید وقتی می‌خواهید Hermes سوابق کاری AI ماندگار یک مخزن را بخواند: مأموریت، برنامه‌ها، یادداشت‌های شواهد، بسته‌های handoff و نتایج review/gate. Hermes agent باقی می‌ماند؛ Open Scaffold سوابق محلی repo باقی می‌ماند.

[Open Scaffold](https://github.com/graphanov/open-scaffold)

سرور را برای یک مخزن scaffoldd شده اضافه کنید:

```
hermes mcp add open_scaffold --command npx --args -y open-scaffold@latest mcp serve --repo /absolute/path/to/repohermes mcp test open_scaffold
```

سپس سطح نمایش را خوانش-محور نگه دارید. `select` را در پرامپت `hermes mcp add` انتخاب کنید یا بعداً `config.yaml` را ویرایش کنید:

`select`
`hermes mcp add`
`config.yaml`

```
mcp_servers:  open_scaffold:    command: "npx"    args: ["-y", "open-scaffold@latest", "mcp", "serve", "--repo", "/absolute/path/to/repo"]    tools:      include:        - list_plans        - get_plan        - get_mission        - list_evidence        - get_evidence        - get_status        - search_plans        - list_amendments        - get_handoff        - analyze_loop        - gate_loop      prompts: false
```

پرامپت‌های خوب:

```
Use the Open Scaffold MCP tools to compile the current handoff packet and tell me the next legal action.
```

```
Inspect the active plans and evidence notes, then say whether this repo is ready for human review or needs another attempt.
```

یادداشت‌های مرزی:

- Open Scaffold MCP محلی-اول و فقط خواندنی به طور پیش‌فرض است.
- ابزارهای نوشتن آن نیاز دارند سرور با `--allow-write` شروع شود؛ آن را فعال نکنید تا زمانی که واقعاً بخواهید Hermes فایل‌های `.osc` را تغییر دهد.
- Open Scaffold سوابق و gateها را کار می‌کند؛ Hermes را برای ادغام، انتشار، استقرار یا ایجاد runtimeها مجاز نمی‌کند.
- `open-scaffold@<version>` را به جای `@latest` ثابت کنید اگر schemaهای ابزار قابل بازتولید نیاز دارید.

`--allow-write`
`.osc`
`open-scaffold@<version>`
`@latest`

### الگو ۳: دستیار triage GitHub

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, update_issue, search_code]      prompts: false      resources: false
```

پرامپت‌های خوب:

```
List open issues about MCP, cluster them by theme, and draft a high-quality issue for the most common bug.
```

```
Search the repo for uses of _discover_and_register_server and explain how MCP tools are registered.
```

### الگو ۴: دستیار API داخلی

```
mcp_servers:  internal_api:    url: "https://mcp.internal.example.com"    headers:      Authorization: "Bearer ***"    tools:      include: [list_customers, get_customer, list_invoices]      resources: false      prompts: false
```

پرامپت‌های خوب:

```
Look up customer ACME Corp and summarize recent invoice activity.
```

این نوع جایی است که لیست سفید سخت بسیار بهتر از لیست exclude است.

### الگو ۴: سرورهای مستندات / دانش

برخی سرورهای MCP پرامپت‌ها یا منابعی را در معرض دید قرار می‌دهند که بیشتر شبیه دارایی‌های دانش مشترک هستند تا اقدامات مستقیم.

```
mcp_servers:  docs:    url: "https://mcp.docs.example.com"    tools:      prompts: true      resources: true
```

پرامپت‌های خوب:

```
List available MCP resources from the docs server, then read the onboarding guide and summarize it.
```

```
List prompts exposed by the docs server and tell me which ones would help with incident response.
```

## آموزش: راه‌اندازی سرتاسری با فیلتر کردن

این یک پیشرفت عملی است.

### فاز ۱: اضافه کردن GitHub MCP با لیست سفید سخت

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, search_code]      prompts: false      resources: false
```

Hermes را راه‌اندازی کنید و بپرسید:

```
Search the codebase for references to MCP and summarize the main integration points.
```

### فاز ۲: فقط در صورت نیاز گسترش دهید

اگر بعداً به به‌روزرسانی issues نیاز دارید:

```
tools:  include: [list_issues, create_issue, update_issue, search_code]
```

سپس بارگذاری مجدد کنید:

```
/reload-mcp
```

### فاز ۳: اضافه کردن سرور دوم با سیاست متفاوت

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, update_issue, search_code]      prompts: false      resources: false  filesystem:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"]
```

حالا Hermes می‌تواند آنها را ترکیب کند:

```
Inspect the local project files, then create a GitHub issue summarizing the bug you find.
```

اینجاست که MCP قدرتمند می‌شود: workflowهای چند سیستمی بدون تغییر هسته Hermes.

## توصیه‌های استفاده ایمن

### برای سیستم‌های خطرناک لیست سفید ترجیح دهید

برای هر چیز مالی، مربوط به مشتری یا مخرب:

- از `tools.include` استفاده کنید
- با کوچک‌ترین مجموعه ممکن شروع کنید

`tools.include`

### ابزارهای کمکی غیرفعال را غیرفعال کنید

اگر نمی‌خواهید مدل منابع/پرامپت‌های ارائه‌شده توسط سرور را مرور کند، آنها را خاموش کنید:

```
tools:  resources: false  prompts: false
```

### سرورها را باریک نگه دارید

مثال‌ها:

- سرور فایل‌سیستم در یک دایرکتوری پروژه ریشه‌دار شده، نه کل دایرکتوری خانه شما
- سرور git به یک مخزن اشاره شده
- سرور API داخلی با نمایش ابزارهای سنگین خوانش به طور پیش‌فرض

### پس از تغییرات config بارگذاری مجدد کنید

```
/reload-mcp
```

این کار را پس از تغییر انجام دهید:

- لیست‌های include/exclude
- پرچم‌های enabled
- کلیدهای resources/prompts
- هدرهای auth / env

## عیب‌یابی بر اساس علائم

### «سرور متصل می‌شود اما ابزارهایی که انتظار داشتم وجود ندارند»

علل احتمالی:

- توسط `tools.include` فیلتر شده
- توسط `tools.exclude` حذف شده
- wrapperهای کمکی از طریق `resources: false` یا `prompts: false` غیرفعال شده‌اند
- سرور واقعاً از resources/prompts پشتیبانی نمی‌کند

`tools.include`
`tools.exclude`
`resources: false`
`prompts: false`

### «سرور پیکربندی شده اما چیزی بارگذاری نمی‌شود»

بررسی کنید:

- `enabled: false` در config باقی نمانده باشد
- command/runtime وجود داشته باشد (npx، uvx و غیره)
- endpoint HTTP قابل دسترس باشد
- env یا هدرهای auth صحیح باشند

`enabled: false`
`npx`
`uvx`

### «چرا ابزارهای کمتری نسبت به آنچه سرور MCP تبلیغ می‌کند می‌بینم؟»

چون Hermes اکنون سیاست به ازای هر سرور شما و ثبت‌نام آگاه به قابلیت را رعایت می‌کند. این انتظار است و معمولاً مطلوب است.

### «چگونه یک سرور MCP را بدون حذف config حذف کنم؟`

از:

```
enabled: false
```

استفاده کنید. این config را حفظ می‌کند اما اتصال و ثبت‌نام را متوقف می‌کند.

## راه‌اندازی‌های اولیه MCP توصیه شده

سرورهای خوب اولیه برای اکثر کاربران:

- filesystem
- git
- GitHub
- سرورهای fetch / مستندات MCP
- یک API داخلی باریک

سرورهای اولیه نه چندان خوب:

- سیستم‌های تجاری عظیم با اقدامات مخرب زیاد و بدون فیلتر
- هر چیزی که به اندازه کافی درک نمی‌کنید تا محدود شود

## اسناد مرتبط

- MCP (Model Context Protocol)
- سؤالات متداول
- دستورات اسلش

[MCP (Model Context Protocol)](/docs/user-guide/features/mcp/)
[سؤالات متداول](/docs/reference/faq/)
[دستورات اسلش](/docs/reference/slash-commands/)
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/guides/use-mcp-with-hermes.md)
