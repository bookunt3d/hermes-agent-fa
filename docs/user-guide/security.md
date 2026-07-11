---
layout: docs
title: "امنیت"
permalink: /docs/user-guide/security/
---

- 
- استفاده از Hermes
- امنیت

# امنیت

Hermes Agent با مدل امنیتی دفاع در عمق طراحی شده است. این صفحه هر مرز امنیتی را پوشش می‌دهد — از تأیید دستور تا ایزوله کردن container تا مجوز کاربر در پلتفرم‌های پیام‌رسانی.

## نمای کلی

مدل امنیتی هفت لایه دارد:

1. مجوز کاربر — چه کسی می‌تواند با عامل صحبت کند (لیست‌های سفید، جفت‌سازی DM)
2. تأیید دستور خطرناک — حلقه انسانی برای عملیات مخرب
3. ایزوله کردن container — sandboxing Docker/Singularity/Modal با تنظیمات تقویت شده
4. فیلتر کردن اعتبارنامه MCP — ایزوله کردن متغیرهای محیطی برای فرایندهای فرعی MCP
5. اسکن فایل‌های زمینه — تشخیص تزریق پرامپت در فایل‌های پروژه
6. ایزوله کردن بین جلسه‌ای — جلسات نمی‌توانند به داده‌ها یا وضعیت یکدیگر دسترسی داشته باشند؛ مسیرهای ذخیره‌سازی cron job در برابر حملات traversal مسیر تقویت شده‌اند
7. پاکسازی ورودی — پارامترهای فهرست کاری در backendهای ابزار ترمینال در برابر یک لیست سفید اعتبارسنجی می‌شوند تا از تزریق shell جلوگیری شود

## تأیید دستور خطرناک

قبل از اجرای هر دستوری، Hermes آن را با فهرست گزینش شده‌ای از الگوهای خطرناک بررسی می‌کند. اگر تطابقی یافت شود، کاربر باید صریحاً آن را تأیید کند.

### حالت‌های تأیید

سیستم تأیید از سه حالت پشتیبانی می‌کند، از طریق approvals.mode در ~/.hermes/config.yaml پیکربندی می‌شود:

`approvals.mode`
`~/.hermes/config.yaml`

```
approvals:  mode: manual                    # manual | smart | off  timeout: 60                     # seconds to wait for user response (default: 60)  cron_mode: deny                 # deny | approve — what cron jobs do when they hit a dangerous command  mcp_reload_confirm: true        # /reload-mcp asks before invalidating the MCP tool cache  destructive_slash_confirm: true # /clear, /new, /reset, /undo prompt before discarding state
```

مجموعه کامل کلیدها:

| کلید | پیش‌فرض | چه چیزی را کنترل می‌کند |
| --- | --- | --- |
| mode | manual | سیاست تأیید برای دستورات خطرناک shell — جدول زیر را ببینید. |
| timeout | 60 | ثانیه‌هایی که Hermes منتظر پاسخ تأیید می‌ماند قبل از تایم‌اوت. |
| cron_mode | deny | نحوه رفتار cron jobs به صورت بی‌صفحه وقتی یک پرامپت دستور خطرناک را فعال می‌کنند. deny دستور را مسدود می‌کند (عامل باید مسیر دیگری پیدا کند)؛ approve همه چیز را در context cron تأیید خودکار می‌کند. |
| mcp_reload_confirm | true | وقتی true، /reload-mcp قبل از بازسازی مجموعه ابزار MCP سؤال می‌کند. بازسازی cache پرامپت ارائه‌دهنده را باطل می‌کند. کاربرانی که Always Approve کلیک می‌کنند این کلید را به false تغییر می‌دهند. |
| destructive_slash_confirm | true | وقتی true، دستورات اسلش مخرب جلسه (/clear، /new، /reset، /undo) قبل از رد کردن وضعیت مکالمه پرامپت می‌کنند. TUI از overlay modal خود استفاده می‌کند (HERMES_TUI_NO_CONFIRM=1 برای غیرفعال کردن). |

`mode`
`manual`
`timeout`
`60`
`cron_mode`
`deny`
[cron jobs](/docs/user-guide/features/cron/)
`deny`
`approve`
`mcp_reload_confirm`
`true`
`/reload-mcp`
`false`
`destructive_slash_confirm`
`true`
`/clear`
`/new`
`/reset`
`/undo`
`false`
`HERMES_TUI_NO_CONFIRM=1`

| حالت | رفتار |
| --- | --- |
| manual (پیش‌فرض) | همیشه از کاربر برای تأیید دستورات خطرناک پرامپت کند |
| smart | از یک LLM کمکی برای ارزیابی ریسک استفاده کند. دستورات کم‌ریسک (مثلاً python -c "print('hello')") تأیید خودکار می‌شوند. دستورات واقعاً خطرناک رد خودکار می‌شوند. موارد مبهم به پرامپت دستی ارتقا می‌یابند. |
| off | همه بررسی‌های تأیید را غیرفعال کند — معادل اجرا با --yolo. همه دستورات بدون پرامپت اجرا می‌شوند. |

`python -c "print('hello')"`
`--yolo`

تنظیم approvals.mode: off همه پرامپت‌های ایمنی را غیرفعال می‌کند. فقط در محیط‌های قابل اعتماد استفاده کنید (CI/CD، containerها و غیره).

`approvals.mode: off`

### حالت YOLO

حالت YOLO همه پرامپت‌های تأیید دستور خطرناک را برای جلسه فعلی دور می‌زند. به سه روش قابل فعال شدن است:

1. پرچم CLI: جلسه‌ای را با hermes --yolo یا hermes chat --yolo شروع کنید
2. دستور اسلش: /yolo را در حین جلسه تایپ کنید تا آن را روشن/خاموش کنید
3. متغیر محیطی: HERMES_YOLO_MODE=1 را تنظیم کنید

`hermes --yolo`
`hermes chat --yolo`
`/yolo`
`HERMES_YOLO_MODE=1`

دستور /yolo یک toggle است — هر استفاده حالت را روشن یا خاموش می‌کند:

`/yolo`

```
> /yolo  ⚡ YOLO mode ON — all commands auto-approved. Use with caution.> /yolo  ⚠ YOLO mode OFF — dangerous commands will require approval.
```

حالت YOLO در هر دو CLI و جلسات گیت‌وی در دسترس است. از نظر داخلی، متغیر محیطی HERMES_YOLO_MODE را تنظیم می‌کند که قبل از هر اجرای دستور بررسی می‌شود.

`HERMES_YOLO_MODE`

وقتی YOLO فعال است، Hermes دو یادآوری بصری پایدار نشان می‌دهد تا فراموش کردن اینکه پرامپت‌های تأیید دور زده شده‌اند سخت باشد:

- یک خط بنر قرمز در ابتدای جلسه وقتی YOLO از قبل فعال است: ⚠ YOLO mode — all approval prompts bypassed. وقتی YOLO خاموش است مخفی می‌شود تا بنر پیش‌فرض شلوغ نشود.
- یک قطعه ⚠ YOLO در نوار وضعیت در همه عرض‌ها، به صورت زنده به‌روز می‌شود وقتی YOLO را روشن یا خاموش می‌کنید.

`⚠ YOLO mode — all approval prompts bypassed`
`⚠ YOLO`

حالت YOLO همه بررسی‌های ایمنی دستور خطرناک را برای جلسه غیرفعال می‌کند — به جز لیست سیاه hardline (پایین را ببینید). فقط وقتی استفاده کنید که کاملاً به دستورات تولید شده اعتماد دارید.

برای دستورات اسلش مخرب جلسه (/clear، /new، /reset، /undo، /quit --delete — /exit --delete یک نام مستعار است)، CLI همچنین قبل از اجرا تأیید درخواست می‌کند. به Slash Commands — Confirmation prompts for destructive commands مراجعه کنید.

`/clear`
`/new`
`/reset`
`/undo`
`/quit --delete`
`/exit --delete`
[Slash Commands — Confirmation prompts for destructive commands](/docs/reference/slash-commands#confirmation-prompts-for-destructive-commands)

### لیست سیاه Hardline (کف همیشه روشن)

برخی دستورات آنقدر فاجعه‌بار هستند — پاک‌کردن غیرقابل بازگشت فایل‌سیستم، fork bombs، نوشتن مستقیم block device — که Hermes از اجرای آنها صرف نظر از شرایط زیر امتناع می‌کند:

- --yolo یا /yolo فعال شده
- approvals.mode: off
- Cron jobs در حالت headless approve در حال اجرا
- کاربر صریحاً «allow always» کلیک کرده

`--yolo`
`/yolo`
`approvals.mode: off`
`approve`

لیست سیاه کف زیر --yolo است. قبل از اینکه لایه تأیید حتی دستور را ببیند فعال می‌شود و هیچ پرچم override وجود ندارد. الگوهای فعلی (کامل نیست؛ با tools/approval.py::UNRECOVERABLE_BLOCKLIST همگام می‌شود):

`--yolo`
`tools/approval.py::UNRECOVERABLE_BLOCKLIST`

| الگو | چرا hardline است |
| --- | --- |
| rm -rf / و مشتقات واضح | ریشه فایل‌سیستم را پاک می‌کند |
| rm -rf --no-preserve-root / | نسخه صریح «بله منظورم root است» |
| :(){ :|:& };: (bash fork bomb) | host را تا ری‌استارت قفل می‌کند |
| mkfs.* روی یک root device متصل شده | سیستم زنده را format می‌کند |
| dd if=/dev/zero of=/dev/sd* | یک دیسک فیزیکی را صفر می‌کند |
| ارسال URLهای غیرقابل اعتماد به sh در سطح بالای rootfs | بردار حمله RCE بیش از حد گسترده برای تأیید |

`rm -rf /`
`rm -rf --no-preserve-root /`
`:(){ :|:& };:`
`mkfs.*`
`dd if=/dev/zero of=/dev/sd*`
`sh`

اگر به لیست سیاه برخورد کنید، فراخوان ابزار خطای توضیحی به عامل برمی‌گرداند و چیزی اجرا نمی‌شود. اگر یک جریان کار مشروع به یکی از این دستورات نیاز دارد (مثلاً شما اپراتور یک خط لوله wipe-and-reinstall هستید)، آن را خارج از عامل اجرا کنید.

### قوانین رد تعریف شده توسط کاربر (approvals.deny)

`approvals.deny`

لیست سیاه hardline ثابت و با کد ارائه می‌شود. approvals.deny معادل قابل ویرایش توسط کاربر آن است: فهرستی از الگوهای glob که دستورات ترمینال مطابق را بدون قید و شرط مسدود می‌کنند — قبل از مشورت با --yolo، /yolo و approvals.mode: off. از آن برای اجرا با استثنائات yolo استفاده کنید: «اجازه دهید عامل همه کارها را انجام دهد، به جز این چیزهای خاص، هرگز.»

`approvals.deny`
`--yolo`
`/yolo`
`approvals.mode: off`

```
approvals:  deny:    - "git push --force*"    - "*curl*|*sh*"    - "dd if=* of=/dev/*"
```

جزئیات:

- الگوها fnmatch globs (*,?,[...]) هستند که به صورت case-insensitive با کل متن دستور تطابق دارند. git push --force* با git push --force origin main مطابقت دارد اما با git push origin main نه.
- تطابق روی همان نسخه‌های نرمال شده/غیررمزنگاری شده دستوری که detector الگوی خطرناک استفاده می‌کند اجرا می‌شود، بنابراین ترفندهای نقل قول ساده (git pu""sh --force) از قاعده رد نمی‌شوند.
- نقل قول YAML: همیشه الگوها را نقل قول کنید. یک * ابتدایی برهنه یک YAML alias است و parse نمی‌شود؛ {، ! و : معانی YAML خودشان را دارند. نقل قول‌های تک برای محتوای shell-like ایمن‌ترین هستند.
- قوانین رد برای backendهای host-reaching (محلی، SSH، Docker متصل به host) اعمال می‌شوند. backendهای container ایزوله کل stack نگهبانی را رد می‌کنند، همانطور که همیشه بوده‌اند — هیچ چیزی که اجرا می‌کنند نمی‌تواند به host آسیب برساند.
- یک دستور رد شده خطای BLOCKED به عامل برمی‌گرداند که به آن می‌گوید دوباره تلاش یا بازنویسی نکند. چیزی اجرا نمی‌شود.

[fnmatch](https://docs.python.org/3/library/fnmatch.html)
`*`
`?`
`[...]`
`git push --force*`
`git push --force origin main`
`git push origin main`
`git pu""sh --force`
`*`
`{`
`!`
`: `

مانند بقیه پیکربندی تأیید، تغییرات بلافاصله اعمال می‌شوند (کش پیکربندی mtime-keyed است) — نیازی به ری‌استارت جلسه نیست.

قوانین رد یک نرده محافظتی در برابر عامل صادق-اما-اشتباه هستند، همان مدل تهدید detector الگوی خطرناک. آنها sandbox در برابر فرآیند عمداً مخرب نیستند — برای آن از backend ایزوله (Docker، Modal) یا محیط با egress محدود شده استفاده کنید.

### تایم‌اوت تأیید

وقتی یک پرامپت دستور خطرناک ظاهر می‌شود، کاربر زمان قابل پیکربندی برای پاسخ دادن دارد. اگر در تایم‌اوت پاسخی داده نشود، دستور به طور پیش‌فرض رد می‌شود (fail-closed).

تایم‌اوت را در ~/.hermes/config.yaml پیکربندی کنید:

`~/.hermes/config.yaml`

```
approvals:  timeout: 60  # seconds (default: 60)
```

### چه چیزی تأیید را فعال می‌کند

الگوهای زیر پرامپت‌های تأیید را فعال می‌کنند (تعریف شده در tools/approval.py):

`tools/approval.py`

| الگو | توضیح |
| --- | --- |
| rm -r / rm --recursive | حذف بازگشتی |
| rm ... / | حذف در مسیر root |
| chmod 777/666/o+w/a+w | مجوزهای world/other-writable |
| chmod --recursive با مجوزهای ناامن | بازگشتی world/other-writable (پرچم بلند) |
| chown -R root / chown --recursive root | بازگشتی chown به root |
| mkfs | فرمت فایل‌سیستم |
| dd if= | کپی دیسک |
| > /dev/sd | نوشتن در block device |
| DROP TABLE/DATABASE | SQL DROP |
| DELETE FROM (بدون WHERE) | SQL DELETE بدون WHERE |
| TRUNCATE TABLE | SQL TRUNCATE |
| > /etc/ | بازنویسی پیکربندی سیستم |
| systemctl stop/restart/disable/mask | توقف/راه‌اندازی مجدد/غیرفعال کردن/ماسک کردن سرویس‌های سیستم |
| kill -9 -1 | کشتن همه فرایندها |
| pkill -9 | کشتن اجباری فرایندها |
| الگوهای Fork bomb | Fork bombs |
| bash -c/sh -c/zsh -c/ksh -c | اجرای دستور shell از طریق پرچم -c |
| python -e/perl -e/ruby -e/node -c | اجرای اسکریپت از طریق پرچم -e/-c |
| curl ... \| sh / wget ... \| sh | ارسال محتوای از راه دور به shell |
| bash <(curl ...) / sh <(wget ...)> | اجرای اسکریپت از راه دور از طریق جایگزینی فرآیند |
| tee به /etc/، ~/.ssh/، ~/.hermes/.env | بازنویسی فایل حساس از طریق tee |
| > یا >> به /etc/، ~/.ssh/، ~/.hermes/.env | بازنویسی فایل حساس از طریق انتقال |
| xargs rm | xargs با rm |
| find -exec rm / find -delete | find با اقدامات مخرب |
| cp/mv/install به /etc/ | کپی/انتقال فایل به پیکربندی سیستم |
| sed -i / sed --in-place روی /etc/ | ویرایش در محل پیکربندی سیستم |
| pkill/killall hermes/gateway | جلوگیری از خودکشی |
| gateway run با &/disown/nohup/setsid | جلوگیری از شروع گیت‌وی خارج از مدیر سرویس |

`rm -r`
`rm --recursive`
`rm ... /`
`chmod 777/666`
`o+w`
`a+w`
`chmod --recursive`
`chown -R root`
`chown --recursive root`
`mkfs`
`dd if=`
`> /dev/sd`
`DROP TABLE/DATABASE`
`DELETE FROM`
`TRUNCATE TABLE`
`> /etc/`
`systemctl stop/restart/disable/mask`
`kill -9 -1`
`pkill -9`
`bash -c`
`sh -c`
`zsh -c`
`ksh -c`
`-c`
`-lc`
`python -e`
`perl -e`
`ruby -e`
`node -c`
`-e`
`-c`
`curl ... | sh`
`wget ... | sh`
`bash <(curl ...)`
`sh <(wget ...)>`
`tee`
`/etc/`
`~/.ssh/`
`~/.hermes/.env`
`>`
`>>`
`/etc/`
`~/.ssh/`
`~/.hermes/.env`
`xargs rm`
`find -exec rm`
`find -delete`
`cp`
`mv`
`install`
`/etc/`
`sed -i`
`sed --in-place`
`/etc/`
`pkill`
`killall`
`gateway run`
`&`
`disown`
`nohup`
`setsid`

عبور container: وقتی در backendهای docker، singularity، modal، یا daytona اجرا می‌شود، بررسی‌های دستور خطرناک رد می‌شوند زیرا خود container مرز امنیتی است. دستورات مخرب داخل container نمی‌توانند به host آسیب برسانند.

`docker`
`singularity`
`modal`
`daytona`

### جریان تأیید (CLI)

در CLI تعاملی، دستورات خطرناک یک پرامپت تأیید درون‌خطی نشان می‌دهند:

```
  ⚠️  DANGEROUS COMMAND: recursive delete      rm -rf /tmp/old-project      [o]nce  |  [s]ession  |  [a]lways  |  [d]eny      Choice [o/s/a/D]:
```

چهار گزینه:

- once — اجازه این اجرای واحد
- session — اجازه این الگو برای بقیه جلسه
- always — اضافه به لیست سفید دائمی (ذخیره شده در config.yaml)
- deny (پیش‌فرض) — مسدود کردن دستور

`config.yaml`

### جریان تأیید (گیت‌وی/پیام‌رسانی)

در پلتفرم‌های پیام‌رسانی، عامل جزئیات دستور خطرناک را به چت ارسال می‌کند و منتظر پاسخ کاربر می‌ماند:

- با yes، y، approve، ok، یا go پاسخ دهید تا تأیید شود
- با no، n، deny، یا cancel پاسخ دهید تا رد شود

متغیر محیطی HERMES_EXEC_ASK=1 هنگام اجرای گیت‌وی به طور خودکار تنظیم می‌شود.

`HERMES_EXEC_ASK=1`

### لیست سفید دائمی

دستورات تأیید شده با «always» در ~/.hermes/config.yaml ذخیره می‌شوند:

`~/.hermes/config.yaml`

```
# الگوهای دستور خطرناک دائمی مجازcommand_allowlist:  - rm  - systemctl
```

این الگوها در هنگام راه‌اندازی بارگذاری شده و در همه جلسات آینده بی‌صدا تأیید می‌شوند.

از hermes config edit برای بررسی یا حذف الگوها از لیست سفید دائمی استفاده کنید.

`hermes config edit`

## مجوز کاربر (گیت‌وی)

هنگام اجرای گیت‌وی پیام‌رسانی، Hermes کنترل می‌کند چه کسی می‌تواند از طریق سیستم مجوز لایه‌ای با ربات تعامل کند.

### ترتیب بررسی مجوز

متد _is_user_authorized() به این ترتیب بررسی می‌کند:

`_is_user_authorized()`
1. پرچم allow-all هر پلتفرم (مثلاً DISCORD_ALLOW_ALL_USERS=true)
2. لیست تأیید شده جفت‌سازی DM (کاربران تأیید شده از طریق کدهای جفت‌سازی)
3. لیست‌های سفید خاص پلتفرم (مثلاً TELEGRAM_ALLOWED_USERS=12345,67890)
4. لیست سفید سراسری (GATEWAY_ALLOWED_USERS=12345,67890)
5. اجازه سراسری (GATEWAY_ALLOW_ALL_USERS=true)
6. پیش‌فرض: رد

`DISCORD_ALLOW_ALL_USERS=true`
`TELEGRAM_ALLOWED_USERS=12345,67890`
`GATEWAY_ALLOWED_USERS=12345,67890`
`GATEWAY_ALLOW_ALL_USERS=true`

### لیست‌های سفید پلتفرم

شناسه‌های کاربر مجاز را به صورت مقادیر جدا شده با کاما در ~/.hermes/.env تنظیم کنید:

`~/.hermes/.env`

```
# لیست‌های سفید خاص پلتفرمTELEGRAM_ALLOWED_USERS=123456789,987654321DISCORD_ALLOWED_USERS=111222333444555666WHATSAPP_ALLOWED_USERS=15551234567SLACK_ALLOWED_USERS=U01ABC123# لیست سفید بین پلتفرمی (برای همه پلتفرم‌ها بررسی می‌شود)GATEWAY_ALLOWED_USERS=123456789# اجازه همه در هر پلتفرم (با احتیاط استفاده کنید)DISCORD_ALLOW_ALL_USERS=true# اجازه سراسری (با احتیاط شدید استفاده کنید)GATEWAY_ALLOW_ALL_USERS=true
```

اگر هیچ لیست سفیدی پیکربندی نشده باشد و GATEWAY_ALLOW_ALL_USERS تنظیم نشده باشد، همه کاربران رد می‌شوند. گیت‌وی در هنگام راه‌اندازی هشداری ثبت می‌کند:

`GATEWAY_ALLOW_ALL_USERS`

```
No user allowlists configured. All unauthorized users will be denied.Set GATEWAY_ALLOW_ALL_USERS=true in ~/.hermes/.env to allow open access,or configure platform allowlists (e.g., TELEGRAM_ALLOWED_USERS=your_id).
```

### سیستم جفت‌سازی DM

برای مجوز انعطاف‌پذیرتر، Hermes شامل یک سیستم جفت‌سازی مبتنی بر کد است. به جای نیاز به شناسه‌های کاربر از قبل، کاربران ناشناخته یک کد جفت‌سازی یک‌بار مصرف دریافت می‌کنند که مالک ربات از طریق CLI تأیید می‌کند.

نحوه کار:

1. یک کاربر ناشناخته DM به ربات ارسال می‌کند
2. ربات با یک کد جفت‌سازی 8 کاراکتری پاسخ می‌دهد
3. مالک ربات hermes pairing approve <platform> <code> را در CLI اجرا می‌کند
4. کاربر به طور دائمی برای آن پلتفرم تأیید می‌شود

`hermes pairing approve <platform> <code>`

کنترل کنید چگونه پیام‌های مستقیم غیرمجاز در ~/.hermes/config.yaml مدیریت می‌شوند:

`~/.hermes/config.yaml`

```
unauthorized_dm_behavior: pairwhatsapp:  unauthorized_dm_behavior: ignore
```

- pair پیش‌فرض برای پلتفرم‌های DM سبک چت است. DMهای غیرمجاز پاسخ کد جفت‌سازی دریافت می‌کنند.
- ignore DMهای غیرمجاز را بی‌صدا رد می‌کند.
- ایمیل به طور پیش‌فرض ignore است مگر اینکه platforms.email.unauthorized_dm_behavior: pair تنظیم شده باشد، زیرا صندوق‌های ورودی می‌توانند ایمیل‌های خوانده نشده نامرتبط داشته باشند.
- بخش‌های پلتفرم پیش‌فرض سراسری را بازنویسی می‌کنند، بنابراین می‌توانید جفت‌سازی را در Telegram نگه دارید در حالی که WhatsApp را بی‌صدا نگه می‌دارید.

`pair`
`ignore`
`ignore`
`platforms.email.unauthorized_dm_behavior: pair`

ویژگی‌های امنیتی (بر اساس راهنمای OWASP + NIST SP 800-63-4):

| ویژگی | جزئیات |
| --- | --- |
| قالب کد | 8 کاراکتر از الفبای 32 کاراکتری بدون ابهام (بدون 0/O/1/I) |
| تصادفی بودن | رمزنگاری (secrets.choice()) |
| TTL کد | انقضا 1 ساعت |
| محدودیت سرعت | 1 درخواست به ازای هر کاربر در هر 10 دقیقه |
| محدودیت در انتظار | حداکثر 3 کد در انتظار به ازای هر پلتفرم |
| قفل شدن | 5 تلاش ناموفق تأیید → قفل شدن 1 ساعته |
| امنیت فایل | chmod 0600 روی همه فایل‌های داده جفت‌سازی |
| ثبت گزارش | کدها هرگز در stdout ثبت نمی‌شوند |

`secrets.choice()`
`chmod 0600`

دستورات CLI جفت‌سازی:

```
# لیست کاربران در انتظار و تأیید شدهhermes pairing list# تأیید یک کد جفت‌سازیhermes pairing approve telegram ABC12DEF# لغو دسترسی یک کاربرhermes pairing revoke telegram 123456789# پاک کردن همه کدهای در انتظارhermes pairing clear-pending
```

`hermes`

تصویر رسمی Docker گیت‌وی را به عنوان کاربر غیرمجاز hermes (uid 10000) از طریق gosu اجرا می‌کند، اما docker exec به طور پیش‌فرض root است. فایل‌های تأیید ایجاد شده توسط root با حالت 0600 root:root نوشته می‌شوند و گیت‌وی نمی‌تواند آنها را بخواند — تأیید بی‌صدا نادیده گرفته می‌شود (#10270).

`hermes`
`gosu`
`docker exec`
`0600 root:root`
[#10270](https://github.com/NousResearch/hermes-agent/issues/10270)

همیشه -u hermes را پاس دهید:

`-u hermes`

```
docker exec -u hermes hermes-agent hermes pairing approve telegram ABC12DEF
```

اگر قبلاً دستور را به عنوان root اجرا کرده‌اید و کاربر هنوز غیرمجاز است، container را مجدداً راه‌اندازی کنید — entrypoint در اجرای بعدی مالکیت را تعمیر می‌کند.

ذخیره‌سازی: داده‌های جفت‌سازی در ~/.hermes/pairing/ با فایل‌های JSON به ازای هر پلتفرم ذخیره می‌شوند:

`~/.hermes/pairing/`
- {platform}-pending.json — درخواست‌های جفت‌سازی در انتظار
- {platform}-approved.json — کاربران تأیید شده
- _rate_limits.json — ردیابی محدودیت سرعت و قفل شدن

`{platform}-pending.json`
`{platform}-approved.json`
`_rate_limits.json`

## ایزوله کردن Container

هنگام استفاده از backend ترمینال docker، Hermes تقویت امنیتی سختی روی هر container اعمال می‌کند.

`docker`

### پرچم‌های امنیتی Docker

هر container با این پرچم‌ها اجرا می‌شود (تعریف شده در tools/environments/docker.py):

`tools/environments/docker.py`

```
_BASE_SECURITY_ARGS = [    "--cap-drop", "ALL",                          # Drop ALL Linux capabilities    "--cap-add", "DAC_OVERRIDE",                  # Root can write to bind-mounted dirs    "--cap-add", "CHOWN",                         # Package managers need file ownership    "--cap-add", "FOWNER",                        # Package managers need file ownership    "--security-opt", "no-new-privileges",         # Block privilege escalation    "--pids-limit", "256",                         # Limit process count    "--tmpfs", "/tmp:rw,nosuid,size=512m",         # Size-limited /tmp    "--tmpfs", "/var/tmp:rw,noexec,nosuid,size=256m",  # No-exec /var/tmp]
```

SETUID/SETGID در لیست پایه نیستند — به صورت شرطی اضافه می‌شوند وقتی container به عنوان root شروع می‌شود و یک init/entrypoint باید امتیازات را کاهش دهد (مسیر s6 privilege-drop). وقتی container قبلاً به عنوان non-root --user اجرا می‌شود رد می‌شوند. tmpfs /run نیز از لیست پایه جدا شده و به ازای هر تصویر mount می‌شود (به طور پیش‌فرض noexec تقویت شده، فقط exec برای تصویرهای s6-overlay که از /run اجرا می‌کنند).

`SETUID`
`SETGID`
`--user`
`/run`
`noexec`
`exec`
`/run`

### محدودیت‌های منابع

منابع container در ~/.hermes/config.yaml قابل پیکربندی هستند:

`~/.hermes/config.yaml`

```
terminal:  backend: docker  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"  docker_forward_env: []  # Explicit allowlist only; empty keeps secrets out of the container  container_cpu: 1        # CPU cores  container_memory: 5120  # MB (default 5GB)  container_disk: 51200   # MB (default 50GB, requires overlay2 on XFS)  container_persistent: true  # Persist filesystem across sessions
```

### پایداری فایل‌سیستم

- حالت پایدار (container_persistent: true): /workspace و /root را از ~/.hermes/sandboxes/docker/<task_id>/ bind-mount می‌کند
- حالت موقت (container_persistent: false): از tmpfs برای workspace استفاده می‌کند — همه چیز در پاکسازی از بین می‌رود

`container_persistent: true`
`/workspace`
`/root`
`~/.hermes/sandboxes/docker/<task_id>/`
`container_persistent: false`

برای استقرارهای گیت‌وی production، از backend docker، modal، یا daytona برای ایزوله کردن دستورات عامل از سیستم host خود استفاده کنید. این نیاز به تأیید دستور خطرناک را کاملاً حذف می‌کند.

`docker`
`modal`
`daytona`

اگر نام‌ها را به terminal.docker_forward_env اضافه کنید، آن متغیرها عمداً برای دستورات ترمینال به container تزریق می‌شوند. این برای اعتبارنامه‌های خاص کار مفید است مانند GITHUB_TOKEN، اما همچنین به این معنی است که کد اجرا شده در container می‌تواند آنها را بخواند و نشت دهد.

`terminal.docker_forward_env`
`GITHUB_TOKEN`

## مقایسه امنیتی Backend ترمینال

| Backend | ایزوله | بررسی دستور خطرناک | بهترین برای |
| --- | --- | --- | --- |
| local | هیچ — روی host اجرا می‌شود | ✅ بله | توسعه، کاربران قابل اعتماد |
| ssh | ماشین از راه دور | ✅ بله | اجرا روی سرور جداگانه |
| docker | Container | ❌ رد شده (container مرز است) | گیت‌وی production |
| singularity | Container | ❌ رد شده | محیط‌های HPC |
| modal | Sandbox ابری | ❌ رد شده | ایزوله ابری مقیاس پذیر |
| daytona | Sandbox ابری | ❌ رد شده | فضاهای کاری ابری پایدار |

## عبور متغیر محیطی

execute_code و terminal هر دو متغیرهای محیطی حساس را از فرایندهای فرعی حذف می‌کنند تا از نشت اعتبارنامه توسط کد تولید شده توسط LLM جلوگیری شود. با این حال، مهارت‌هایی که required_environment_variables اعلام می‌کنند به طور مشروع به آن متغیرها نیاز دارند.

`execute_code`
`terminal`
`required_environment_variables`

### نحوه کار

دو مکانیزم متغیرهای خاصی را از فیلترهای sandbox عبور می‌دهند:

1. عبور محدود به مهارت (خودکار)

وقتی یک مهارت بارگذاری می‌شود (از طریق skill_view یا دستور /skill) و required_environment_variables اعلام می‌کند، هر یک از آن متغیرها که واقعاً در محیط تنظیم شده‌اند به طور خودکار به عنوان عبور ثبت می‌شوند. متغیرهای گمشده (هنوز در حالت نیاز به راه‌اندازی) ثبت نمی‌شوند.

`skill_view`
`/skill`
`required_environment_variables`

```
# در frontmatter یک مهارت SKILL.mdrequired_environment_variables:  - name: TENOR_API_KEY    prompt: Tenor API key    help: Get a key from https://developers.google.com/tenor
```

پس از بارگذاری این مهارت، TENOR_API_KEY از execute_code، terminal (محلی)، و backendهای از راه دور (Docker، Modal) عبور می‌کند — نیازی به پیکربندی دستی نیست.

`TENOR_API_KEY`
`execute_code`
`terminal`

قبل از v0.5.1، forward_env Docker سیستمی جداگانه از عبور مهارت بود. اکنون ادغام شده‌اند — متغیرهای محیطی اعلام شده توسط مهارت به طور خودکار به containerهای Docker و sandboxهای Modal فوروارد می‌شوند بدون نیاز به اضافه کردن دستی به docker_forward_env.

`forward_env`
`docker_forward_env`

2. عبور مبتنی پیکربندی (دستی)

برای متغیرهای محیطی که توسط هیچ مهارتی اعلام نشده‌اند، آنها را به terminal.env_passthrough در config.yaml اضافه کنید:

`terminal.env_passthrough`
`config.yaml`

```
terminal:  env_passthrough:    - MY_CUSTOM_KEY    - ANOTHER_TOKEN
```

### عبور فایل اعتبارنامه (توکن‌های OAuth و غیره)

برخی مهارت‌ها به فایل‌ها (نه فقط متغیرهای محیطی) در sandbox نیاز دارند — مثلاً Google Workspace توکن‌های OAuth را به عنوان google_token.json در زیر HERMES_HOME پروفایل فعال ذخیره می‌کند. مهارت‌ها اینها را در frontmatter اعلام می‌کنند:

`google_token.json`
`HERMES_HOME`

```
required_credential_files:  - path: google_token.json    description: Google OAuth2 token (created by setup script)  - path: google_client_secret.json    description: Google OAuth2 client credentials
```

هنگام بارگذاری، Hermes بررسی می‌کند آیا این فایل‌ها در HERMES_HOME پروفایل فعال وجود دارند و آنها را برای mount ثبت می‌کند:

`HERMES_HOME`
- Docker: Mountهای bind فقط خواندنی (-v host:container:ro)
- Modal: هنگام ایجاد sandbox mount شده + قبل از هر دستور sync شده
- محلی: نیازی به اقدام نیست (فایل‌ها از قبل قابل دسترسی)

`-v host:container:ro`

همچنین می‌توانید فایل‌های اعتبارنامه را به صورت دستی در config.yaml فهرست کنید:

`config.yaml`

```
terminal:  credential_files:    - google_token.json    - my_custom_oauth_token.json
```

مسیرها نسبت به ~/.hermes/ هستند. فایل‌ها در /root/.hermes/ داخل container mount می‌شوند. این لیست توسط tools/credential_files.py (terminal.credential_files) خوانده می‌شود — در بلوک terminal زندگی می‌کند اما توسط ماژول credential_files بارگذاری می‌شود، نه backend ترمینال هسته، بنابراین بخشی از snapshot DEFAULT_CONFIG باندل نیست.

`~/.hermes/`
`/root/.hermes/`
`tools/credential_files.py`
`terminal.credential_files`
`terminal:`
`DEFAULT_CONFIG`

### هر sandbox چه چیزی را فیلتر می‌کند

| Sandbox | فیلتر پیش‌فرض | بازنویسی عبور |
| --- | --- | --- |
| execute_code | متغیرهایی با KEY، TOKEN، SECRET، PASSWORD، CREDENTIAL، PASSWD، AUTH در نام را مسدود می‌کند | ✅ متغیرهای عبور هر دو بررسی را دور می‌زنند |
| terminal (محلی) | متغیرهای صریح زیرساخت Hermes را مسدود می‌کند | ✅ متغیرهای عبور لیست سیاه را دور می‌زنند |
| terminal (Docker) | به طور پیش‌فرض متغیرهای محیطی host نیست | ✅ متغیرهای عبور + docker_forward_env از طریق -e فوروارد شده |
| terminal (Modal) | به طور پیش‌فرض فایل/متغیرهای host نیست | ✅ فایل‌های اعتبارنامه mount شده؛ عبور env از طریق sync |
| MCP | همه چیز را به جز متغیرهای ایمن سیستم + env صریحاً پیکربندی شده مسدود می‌کند | ❌ تحت تأثیر عبور نیست (از پیکربندی env MCP استفاده کنید) |

`KEY`
`TOKEN`
`SECRET`
`PASSWORD`
`CREDENTIAL`
`PASSWD`
`AUTH`
`docker_forward_env`
`-e`
`env`
`env`

### ملاحظات امنیتی

- عبور فقط متغیرهایی را تحت تأثیر قرار می‌دهد که شما یا مهارت‌هایتان صریحاً اعلام می‌کنید — وضعیت امنیتی پیش‌فرض برای کد دلخواه تولید شده توسط LLM تغییر نمی‌کند
- فایل‌های اعتبارنامه فقط خواندنی به containerهای Docker mount می‌شوند
- Skills Guard محتوای مهارت را برای الگوهای دسترسی مشکوک محیطی قبل از نصب اسکن می‌کند
- متغیرهای گمشده/تنظیم نشده هرگز ثبت نمی‌شوند (نمی‌توانید چیزی را که وجود ندارد نشت دهید)
- رمزهای زیرساخت Hermes (کلیدهای API ارائه‌دهنده، توکن‌های گیت‌وی) هرگز نباید به env_passthrough اضافه شوند — مکانیزم‌های اختصاصی خودشان را دارند

`env_passthrough`

## مدیریت اعتبارنامه MCP

فرایندهای فرعی سرور MCP (Model Context Protocol) یک محیط فیلتر شده دریافت می‌کنند تا از نشت تصادفی اعتبارنامه جلوگیری شود.

### متغیرهای محیطی ایمن

فقط این متغیرها از host به فرایندهای فرعی MCP stdio فوروارد می‌شوند:

```
PATH, HOME, USER, LANG, LC_ALL, TERM, SHELL, TMPDIR
```

به علاوه هر متغیر XDG_*. همه متغیرهای محیطی دیگر (کلیدهای API، توکن‌ها، رمزها) حذف می‌شوند.

`XDG_*`

متغیرهایی که به صورت صریح در پیکربندی env سرور MCP تعریف شده‌اند فوروارد می‌شوند:

`env`

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."  # Only this is passed
```

### حذف اعتبارنامه

پیام‌های خطا از ابزارهای MCP قبل از بازگشت به LLM پاکسازی می‌شوند. الگوهای زیر با [REDACTED] جایگزین می‌شوند:

`[REDACTED]`
- GitHub PATs (ghp_...)
- کلیدهای سبک OpenAI (sk-...)
- توکن‌های Bearer
- پارامترهای token=، key=، API_KEY=، password=، secret=

`ghp_...`
`sk-...`
`token=`
`key=`
`API_KEY=`
`password=`
`secret=`

### سیاست دسترسی به وب‌سایت

می‌توانید محدود کنید وب‌سایت‌هایی که عامل از طریق ابزارهای وب و مرورگر خود به آنها دسترسی دارد. این برای جلوگیری از دسترسی عامل به سرویس‌های داخلی، پنل‌های مدیریتی یا سایر URLهای حساس مفید است.

```
# در ~/.hermes/config.yamlsecurity:  website_blocklist:    enabled: true    domains:      - "*.internal.company.com"      - "admin.example.com"    shared_files:      - "/etc/hermes/blocked-sites.txt"
```

وقتی یک URL مسدود شده درخواست می‌شود، ابزار خطایی برمی‌گرداند که توضیح می‌دهد دامنه توسط سیاست مسدود شده است. لیست سیاه در web_search، web_extract، browser_navigate و همه ابزارهای URL-capable اعمال می‌شود.

`web_search`
`web_extract`
`browser_navigate`

[Website Blocklist](/docs/user-guide/configuration#website-blocklist) را برای جزئیات کامل در راهنمای پیکربندی ببینید.

### محافظت SSRF

همه ابزارهای URL-capable (جستجوی وب، استخراج وب، بینایی، مرورگر) URLها را قبل از واکشی اعتبارسنجی می‌کنند تا از حملات Server-Side Request Forgery (SSRF) جلوگیری شود. آدرس‌های مسدود شده شامل:

- شبکه‌های خصوصی (RFC 1918): 10.0.0.0/8، 172.16.0.0/12، 192.168.0.0/16
- Loopback: 127.0.0.0/8، ::1
- Link-local: 169.254.0.0/16 (شامل متاداده ابری در 169.254.169.254)
- CGNAT / فضای آدرس مشترک (RFC 6598): 100.64.0.0/10 (Tailscale، WireGuard VPNs)
- نام‌های میزبان متاداده ابری: metadata.google.internal، metadata.goog
- آدرس‌های رزرو شده، multicast و unspecified

`10.0.0.0/8`
`172.16.0.0/12`
`192.168.0.0/16`
`127.0.0.0/8`
`::1`
`169.254.0.0/16`
`169.254.169.254`
`100.64.0.0/10`
`metadata.google.internal`
`metadata.goog`

محافظت SSRF همیشه برای استفاده در اینترنت فعال است و خرابی‌های DNS به عنوان مسدود شده رفتار می‌شوند (fail-closed). زنجیره‌های انتقال در هر hop دوباره اعتبارسنجی می‌شوند تا از دور زدن‌های مبتنی بر انتقال جلوگیری شود.

#### اجازه عمدی به URLهای خصوصی

برخی تنظیمات به طور مشروع به دسترسی خصوصی/داخلی URL نیاز دارند — شبکه‌های خانگی که home.arpa را به فضای RFC 1918 حل می‌کنند، نقاط پایانی LAN-only Ollama/llama.cpp، ویکی‌های داخلی، اشکال‌زدایی متاداده ابری و غیره. برای این موارد یک غیرفعال کردن سراسری وجود دارد:

`home.arpa`

```
security:  allow_private_urls: true   # default: false
```

وقتی روشن است، ابزارهای وب، مرورگر، واکشی‌های URL بینایی و دانلودهای رسانه گیت‌وی دیگر مقصد RFC 1918 / loopback / link-local / CGNAT / متاداده ابری را رد نمی‌کنند. این یک مرز اعتماد عمدی است — فقط روی ماشین‌هایی فعال کنید که اجرای URLهای دلخواه تزریق شده توسط پرامپت علیه شبکه محلی یک ریسک قابل قبول است. گیت‌وی‌های عمومی آن را خاموش نگه دارند.

نگهبان host-substring (که ترفندهای دامنه Unicode مشابه را حتی وقتی IP زیرین عمومی است مسدود می‌کند) صرف نظر از این تنظیم روشن می‌ماند.

### اسکن امنیتی Tirith Pre-Exec

Hermes tirith را برای اسکن سطح محتوای دستور قبل از اجرا ادغام می‌کند. Tirith تهدیداتی را تشخیص می‌دهد که فقط تطابق الگو از دست می‌دهد:

[tirith](https://github.com/sheeki03/tirith)
- جعل URL Homograph (حملات دامنه بین‌المللی)
- الگوهای pipe-to-interpreter (curl | bash، wget | sh)
- حملات تزریق ترمینال

`curl | bash`
`wget | sh`

Tirith از GitHub releases در اولین استفاده به طور خودکار نصب می‌شود با بررسی checksum SHA-256 (و بررسی اصالت cosign اگر cosign موجود باشد).

```
# در ~/.hermes/config.yamlsecurity:  tirith_enabled: true       # Enable/disable tirith scanning (default: true)  tirith_path: "tirith"      # Path to tirith binary (default: PATH lookup)  tirith_timeout: 5          # Subprocess timeout in seconds  tirith_fail_open: true     # Allow execution when tirith is unavailable (default: true)
```

وقتی tirith_fail_open true باشد (پیش‌فرض)، دستورات اگر tirith نصب نباشد یا تایم‌اوت کند ادامه می‌یابند. در محیط‌های امنیتی بالا false تنظیم کنید تا دستورات وقتی tirith در دسترس نیست مسدود شوند.

`tirith_fail_open`
`true`
`false`

Tirith باینری‌های از پیش ساخته شده برای Linux (x86_64 / aarch64) و macOS (x86_64 / arm64) ارائه می‌دهد. در پلتفرم‌هایی بدون باینری از پیش ساخته شده (Windows و غیره)، tirith بی‌صدا رد می‌شود — نگهبان‌های تطابق الگو همچنان اجرا می‌شوند و CLI بنر «unavailable» نشان نمی‌دهد. برای استفاده از tirith در ویندوز، Hermes را در WSL اجرا کنید.

حکم tirith با جریان تأیید ادغام می‌شود: دستورات ایمن عبور می‌کنند، در حالی که دستورات مشکوک و مسدود شده تأیید کاربر را با یافته‌های کامل tirith (شدت، عنوان، توضیح، جایگزین‌های ایمن‌تر) فعال می‌کنند. کاربران می‌توانند تأیید یا رد کنند — گزینه پیش‌فرض رد است تا سناریوهای بدون نظارت ایمن بمانند.

### محافظت از تزریق فایل‌های زمینه

فایل‌های زمینه (AGENTS.md، .cursorrules، SOUL.md) قبل از گنجاندن در پرامپت سیستم برای تزریق پرامپت اسکن می‌شوند. اسکنر بررسی می‌کند:

- دستورات برای نادیده گرفتن/بی‌توجهی به دستورات قبلی
- نظرات HTML مخفی با کلمات کلیدی مشکوک
- تلاش‌ها برای خواندن رمزها (.env، credentials، .netrc)
- نشت اعتبارنامه از طریق curl
- کاراکترهای Unicode نامرئی (فاصله‌های با عرض صفر، بازنویسی‌های دوطرفه)

`.env`
`credentials`
`.netrc`
`curl`

فایل‌های مسدود شده هشداری نشان می‌دهند:

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

## بهترین شیوه‌ها برای استقرار Production

### چک‌لیست استقرار گیت‌وی

1. لیست‌های سفید صریح تنظیم کنید — هرگز در production از GATEWAY_ALLOW_ALL_USERS=true استفاده نکنید
2. از backend container استفاده کنید — terminal.backend: docker را در config.yaml تنظیم کنید
3. محدودیت‌های منابع را محدود کنید — CPU، حافظه و دیسک مناسب تنظیم کنید
4. رمزها را ایمن ذخیره کنید — کلیدهای API را در ~/.hermes/.env با مجوزهای فایل مناسب نگه دارید
5. جفت‌سازی DM را فعال کنید — از کدهای جفت‌سازی به جای کدگذاری سخت شناسه‌های کاربر استفاده کنید
6. لیست سفید دستورات را بررسی کنید — command_allowlist در config.yaml را دوره‌ای حسابرسی کنید
7. terminal.cwd را تنظیم کنید — نگذارید عامل از فهرست‌های حساس عمل کند
8. به عنوان non-root اجرا کنید — هرگز گیت‌وی را به عنوان root اجرا نکنید
9. لاگ‌ها را نظارت کنید — ~/.hermes/logs/ را برای تلاش‌های دسترسی غیرمجاز بررسی کنید
10. به‌روز نگه دارید — hermes update را به طور منظم برای وصله‌های امنیتی اجرا کنید

`GATEWAY_ALLOW_ALL_USERS=true`
`terminal.backend: docker`
`~/.hermes/.env`
`command_allowlist`
`terminal.cwd`
`~/.hermes/logs/`
`hermes update`

### ایمن‌سازی کلیدهای API

```
# تنظیم مجوزهای مناسب روی فایل .envchmod 600 ~/.hermes/.env# نگه داشتن کلیدهای جداگانه برای سرویس‌های مختلف# هرگز فایل‌های .env را به کنترل نسخه commit نکنید
```

### ایزوله کردن شبکه

برای حداکثر امنیت، گیت‌وی را روی ماشین یا VM جداگانه اجرا کنید. terminal.backend: ssh را در config.yaml تنظیم کنید، سپس جزئیات host را از طریق متغیرهای محیطی در ~/.hermes/.env فراهم کنید:

`terminal.backend: ssh`
`config.yaml`
`~/.hermes/.env`

```
# ~/.hermes/config.yamlterminal:  backend: ssh
```

```
# ~/.hermes/.envTERMINAL_SSH_HOST=agent-worker.localTERMINAL_SSH_USER=hermesTERMINAL_SSH_KEY=~/.ssh/hermes_agent_key
```

جزئیات اتصال SSH در .env (نه config.yaml) زندگی می‌کنند بنابراین check-in نمی‌شوند یا همراه exportهای پروفایل به اشتراک گذاشته نمی‌شوند. این اتصالات پیام‌رسانی گیت‌وی را از اجرای دستورات عامل جدا نگه می‌دارد.

`.env`
`config.yaml`

## بررسی advisory زنجیره تأمین

Hermes با یک اسکنر advisory داخلی ارائه می‌شود که بسته‌های پایتون در venv فعال را که با کاتالوگ گزینش شده نسخه‌های به خطر افتاده شناخته شده مطابقت دارند پرچم می‌زند (کرم‌های زنجیره تأمین مانند مسمومیت mistralai 2.4.6 مه 2026). پیاده‌سازی در hermes_cli/security_advisories.py زندگی می‌کند.

`mistralai 2.4.6`
`hermes_cli/security_advisories.py`

نحوه اجرا:

- بنر راه‌اندازی CLI. اگر هر advisory مطابقت داشته باشد یک خط هشدار چاپ می‌شود، با اشاره به hermes doctor برای اصلاح کامل.
- hermes doctor. هر advisory فعال را با جزئیات نسخه و دستورالعمل‌های اصلاح 2-4 مرحله‌ای نشان می‌دهد.
- راه‌اندازی گیت‌وی. در gateway.log ثبت می‌شود؛ اولین پیام تعاملی بنر کوتاه اپراتور دریافت می‌کند.

`hermes doctor`
`hermes doctor`
`gateway.log`

هر advisory یک id پایدار دارد. پس از خواندن و اقدام روی آن می‌توانید آن را برای همیشه رد کنید:

```
hermes doctor --ack <advisory-id>
```

ack در config.security.acked_advisories ذخیره شده و ری‌استارت را تحمل می‌کند. advisories قدیمی عمداً از کاتالوگ حذف نمی‌شوند — نگه داشتن آنها نصب‌های تازه را درباره نسخه‌های مسموم تاریخی که ممکن است هنوز در mirror خصوصی cache شده باشند هشدار می‌دهد.

`config.security.acked_advisories`

خود بررسی فقط stdlib است و از یک importlib.metadata.version() lookup به ازای هر advisory اجرا می‌شود، بنابراین اجرای آن در هر راه‌اندازی ایمن است.

`importlib.metadata.version()`

### نصب تنبل وابستگی‌های اختیاری

بسیاری از ویژگی‌ها (Mistral TTS، ElevenLabs، حافظه Honcho، Bedrock، Slack، Matrix و...) به بسته‌های پایتونی وابسته هستند که هر کاربری به آنها نیاز ندارد. Hermes اینها را به جای eager install تحت hermes-agent[all] در اولین استفاده به صورت lazy نصب می‌کند. پیاده‌سازی در tools/lazy_deps.py زندگی می‌کند.

`hermes-agent[all]`
`tools/lazy_deps.py`

 traded-off این:

- شکنندگی. وقتی وابستگی transitive یک extra روی PyPI در دسترس نباشد (برای بدافزار قرنطینه شده، حذف شده، آپلود خراب)، کل resolve [all] ناموفق می‌شود و نصب‌های تازه بی‌صدا به یک لایه حذف شده بازمی‌گردند — 10+ extra غیرمرتبط را یکجا از دست می‌دهند. نصب تنبل هر backend را ایزوله می‌کند بنابراین یک وابستگی مسموم نمی‌تواند ویژگی‌های غیرمرتبط را خراب کند.
- حجیم. کاربری که فقط با یک ارائه‌دهنده صحبت می‌کند دیگر صدها بسته‌ای را که هرگز import نمی‌کند نمی‌کشد.

`[all]`

نحوه کار:

1. یک ماژول backend ensure("feature.name") را در بالای مسیر import اول خود فراخوانی می‌کند.
2. اگر وابستگی‌ها گمشده باشند، ensure security.allow_lazy_installs در config.yaml (پیش‌فرض true) را بررسی می‌کند و pip install محدود به venv را برای مشخصات لیست سفید اجرا می‌کند.
3. اگر نصب ناموفق باشد یا کاربر نصب تنبل را غیرفعال کرده باشد، فراخوان FeatureUnavailable با stderr واقعی pip و اشاره به hermes tools برمی‌گرداند.

`ensure("feature.name")`
`ensure`
`security.allow_lazy_installs`
`config.yaml`
`true`
`pip install`
`FeatureUnavailable`
`hermes tools`

تضمین‌های امنیتی اعمال شده توسط tools/lazy_deps.py:

`tools/lazy_deps.py`

| تضمین | معنی |
| --- | --- |
| فقط محدود به venv | نصب‌ها sys.executable در venv فعال را هدف قرار می‌دهند — هرگز پایتون سیستم |
| فقط PyPI با نام | مشخصات سینتکس "package>=1.0,<2" را می‌پذیرند. بدون --index-url، git+https://، یا مسیرهای file: — config.yaml مخرب نمی‌تواند نصب را هدایت کند |
| لیست سفید | فقط مشخصاتی که در نقشه LAZY_DEPS موجود هستند می‌توانند از این مسیر نصب شوند. غلط املایی در نام feature معنای نصب هر چیزی نمی‌دهد |
| غیرفعال کردن | security.allow_lazy_installs: false تنظیم کنید تا نصب‌های runtime کاملاً غیرفعال شوند. مفید برای شبکه‌های محدود یا وضعیت‌های امنیتی سخت |
| بدون تلاش‌های مجدد بی‌صدا | خطاها به صورت FeatureUnavailable ظاهر می‌شوند — بدون کش حالت بد، بدون طوفان تلاش مجدد |

`sys.executable`
`"package>=1.0,<2"`
`--index-url`
`git+https://`
`config.yaml`
`LAZY_DEPS`
`security.allow_lazy_installs: false`
`FeatureUnavailable`

برای غیرفعال کردن نصب‌های runtime:

```
# ~/.hermes/config.yamlsecurity:  allow_lazy_installs: false
```

وقتی غیرفعال شود، backendهایی که به وابستگی‌های اختیاری نیاز دارند به کاربر می‌گویند نصب را به صورت دستی اجرا کند (pip install …) یا backend دیگری را از طریق hermes tools انتخاب کند.

`pip install …`
`hermes tools`
[ویرایش این صفحه](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/security.md)