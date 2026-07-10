---
layout: docs
title: خانه
permalink: /docs/
---

# راهنمای فارسی Hermes Agent

Agent هوشمند خود بهبودی‌یافته ساخته‌شده توسط [Nous Research](https://nousresearch.com). تنها agentی که حلقه یادگیری داخلی دارد — از تجربه مهارت می‌سازد، در حین استفاده بهبودشان می‌دهد، دانش را ذخیره می‌کند و مدل عمیقی از هویت شما در طول جلسات می‌سازد.

---

## نصب

### ویندوز یا macOS

برای نصب آسان خط فرمان و اپلیکیشن دسکتاپ، [installer دسکتاپ Hermes](https://hermes-agent.nousresearch.com/) را از وب‌سایت ما دانلود و اجرا کنید.

### بدون Hermes Desktop:

برای نصب فقط خط فرمان بدون Hermes Desktop:

#### Linux / macOS / WSL2 / Android (Termux)

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

#### ویندوز (بومی)

در powershell اجرا کنید:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

راهنمای کامل [نصب](/docs/getting-started/installation) را ببینید. برای جدول پشتیبانی پلتفرم‌ها، [پشتیبانی از پلتفرم‌ها](/docs/getting-started/platform-support) را مشاهده کنید.

> **سریع‌ترین مسیر به یک agent کارا:** بعد از نصب، `hermes setup --portal` را اجرا کنید — یک OAuth هم مدل و هم چهار ابزار Tool Gateway (جستجوی وب، تولید تصویر، TTS، مرورگر) را پوشش می‌دهد. [Nous Portal](/docs/integrations/nous-portal) را ببینید.

---

## Hermes Agent چیست؟

یک copilot برنامه‌نویسی متصل به IDE یا یک chatbot ساده دور یک API نیست. یک **agent خودمختار** است که هرچه بیشتر اجرا شود، تواناتر می‌شود. هر جا بخواهید زندگی می‌کند — یک VPS ارزان، یک کلاستر GPU، یا زیرساخت serverless (Daytona, Modal) که تقریباً هیچ هزینه‌ای در حالت بیکاری ندارد. از تلگرام با آن صحبت کنید در حالی که روی یک VM ابری کار می‌کند که هرگز به آن SSH نمی‌زنید. به لپ‌تاپ شما وابسته نیست.

---

## لینک‌های سریع

| لینک | توضیح |
|------|-------|
| 🚀 [نصب](/docs/getting-started/installation) | نصب در ۶۰ ثانیه روی Linux، macOS، WSL2، ویندوز بومی یا اندروید |
| 📖 [راهنمای شروع سریع](/docs/getting-started/quickstart) | اولین مکالمه و ویژگی‌های کلیدی |
| 🗺️ [مسیر یادگیری](/docs/getting-started/learning-path) | مستندات مناسب سطح تجربه شما |
| ⚙️ [پیکربندی](/docs/user-guide/configuration) | تنظیم مدل‌ها، API keys و رفتار agent |
| 💡 [نکات و ترفندها](/docs/guides/tips) | ترفندها و بهترین شیوه‌ها |
| 🔧 [دستورات CLI](/docs/reference/cli-commands) | مرجع کامل دستورات |
