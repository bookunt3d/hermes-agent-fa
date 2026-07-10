---
layout: docs
title: "پشتیبانی از پلتفرم‌ها"
permalink: /docs/getting-started/platform-support/
---

- 
- Getting Started
- Platform Support

# پشتیبانی از پلتفرم‌ها

Hermes Agent از پلتفرم‌ها و روش‌های توزیع متعددی پشتیبانی می‌کند، اما نمی‌توانیم از هر روش نصب ممکنی پشتیبانی کنیم.

## سطح ۱

تلاش ما این است که نصب و به‌روزرسانی‌ها برای این پلتفرم‌ها هرگز خراب نشوند. مشکلات و بازگشت‌ها در سطح ۱ اولویت اول ما هستند و بر پلتفرم‌های دیگر اولویت دارند.

| سیستم‌عامل / معماری | روش‌های نصب | توضیحات |
| --- | --- | --- |
| macOS(Apple Silicon) | Hermes Desktop، install.sh |  |
| Windows 10 / 11(x86_64، aarch64) | Hermes Desktop، install.ps1 | تعداد کمی از ویژگی‌ها موجود نیستند. |
| Linux / WSL2(x86_64، aarch64) | install.sh | ما روی آخرین نسخه Ubuntu و WSL2 تست می‌کنیم. اگر توزیع شما glibc، systemd دارد و از استاندارد سلسله‌مراتب فایل‌سیستم پیروی می‌کند، احتمالاً به خوبی کار می‌کند. |
| Docker Container(x86_64، aarch64) | docker pull | نصب‌های Docker از hermes update پشتیبانی نمی‌کنند. به‌روزرسانی با اجرای یک تصویر جدید انجام می‌شود. |

[Hermes Desktop](https://hermes-agent.nousresearch.com/)
[install.sh](/docs/getting-started/installation#linux--macos--wsl2--android-termux)
[Windows 10 / 11](/docs/user-guide/windows-native)
[Hermes Desktop](https://hermes-agent.nousresearch.com/)
[install.ps1](/docs/getting-started/installation#windows-native)
[موجود نیست](/docs/user-guide/windows-native#feature-matrix)
[WSL2](/docs/user-guide/windows-wsl-quickstart)
[install.sh](/docs/getting-started/installation#linux--macos--wsl2--android-termux)
[Docker Container](/docs/user-guide/docker#quick-start)
[docker pull](/docs/user-guide/docker#quick-start)

## سطح ۲

این پلتفرم‌ها فقط به صورت بهترین تلاش در درخت کد نگهداری می‌شوند.
انتشارها ممکن است آن‌ها را خراب کنند و نمی‌توانیم قول دهیم که به سرعت آن‌ها را تعمیر کنیم.

PRها برای تعمیر مشکلات آن‌ها پذیرفته می‌شوند، اما نسبت به تعمیر مشکلات پلتفرم‌های سطح ۱ اولویت کمتری دارند.

| سیستم‌عامل / معماری | روش‌های نصب | توضیحات |
| --- | --- | --- |
| Android (Termux)(aarch64) | install.sh | تعداد کمی از ویژگی‌ها موجود نیستند. |
| Nix(MacOS، Linux، NixOS) | install.sh | اغلب به دلیل مشکلات بسته‌بندی node.js خراب می‌شود. موفق باشید~! <3 |

[install.sh](/docs/getting-started/installation#linux--macos--wsl2--android-termux)
[موجود نیست](/docs/getting-started/termux#known-limitations-on-phones)
[install.sh](/docs/getting-started/nix-setup)

## پشتیبانی‌نشده

این پلتفرم‌ها و روش‌های توزیع پشتیبانی نمی‌شوند.
پیشنهاد می‌کنیم به یک روش توزیع یا پلتفرم پشتیبانی‌شده مهاجرت کنید.
ممکن است همین الان خراب باشند، ممکن است در آینده بیشتر خراب شوند.
PRهایی برای تعمیر آن‌ها پذیرفته نخواهند شد و هر کدی که سازگاری با آن‌ها را حفظ کند ممکن است در هر زمانی حذف شود.

- نصب‌ها از AUR (اگر مفید باشد ممکن است پچ‌ها را به صورت upstream ارسال کنیم <3)
- macOS روی پردازنده‌های x86 (Intel)
- نصب‌ها از pypi (مثلاً uv tool install hermes-agent، pip install hermse-agent، و غیره)
- نصب‌ها از brew (brew install hermes-agent)

اگر از یک روش توزیع پشتیبانی‌نشده استفاده می‌کنید، لطفاً [راهنمای نصب](/docs/getting-started/installation) را بخوانید تا یاد بگیرید چگونه به یک روش پشتیبانی‌شده سوئیچ کنید.
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/platform-support.md)
