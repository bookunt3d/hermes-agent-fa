#!/usr/bin/env python3
"""Map scraped_v2 files to Jekyll docs structure."""
import os
import re
from pathlib import Path

SCRAPED_DIR = Path("scraped_v2")
DOCS_DIR = Path("docs")

# Title translations for common pages
TITLES = {
    "acp-internals": "جزئیات داخلی ACP",
    "adding-platform-adapters": "افزودن تطبیق‌دهنده‌های پلتفرم",
    "adding-providers": "افزودن ارائه‌دهندگان",
    "adding-tools": "افزودن ابزارها",
    "agent-loop": "حلقه Agent",
    "browser-provider-plugin": "پلاگین ارائه‌دهنده مرورگر",
    "browser-supervisor": "نظارت‌گر مرورگر",
    "context-compression-and-caching": "فشرده‌سازی و کش زمینه",
    "context-engine-plugin": "پلاگین موتور زمینه",
    "contributing": "مشارکت در توسعه",
    "creating-skills": "ایجاد مهارت‌ها",
    "cron-internals": "جزئیات داخلی Cron",
    "extending-the-cli": "گسترش CLI",
    "gateway-internals": "جزئیات داخلی Gateway",
    "image-gen-provider-plugin": "پلاگین ارائه‌دهنده تولید تصویر",
    "memory-provider-plugin": "پلاگین ارائه‌دهنده حافظه",
    "model-provider-plugin": "پلاگین ارائه‌دهنده مدل",
    "plugin-llm-access": "دسترسی LLM پلاگین",
    "plugins": "پلاگین‌ها",
    "programmatic-integration": "یکپارچه‌سازی برنامه‌نویسی",
    "prompt-assembly": "مونتاژ پرامپت",
    "provider-runtime": "محیط اجرای ارائه‌دهنده",
    "secret-source-plugin": "پلاگین منبع رمز",
    "session-storage": "ذخیره‌سازی جلسه",
    "tools-runtime": "محیط اجرای ابزارها",
    "trajectory-format": "فرمت مسیر حرکت",
    "video-gen-provider-plugin": "پلاگین ارائه‌دهنده تولید ویدیو",
    "web-search-provider-plugin": "پلاگین ارائه‌دهنده جستجوی وب",
    "automate-with-cron": "اتوماسیون با Cron",
    "automation-blueprints": "نقشه‌های اتوماسیون",
    "aws-bedrock": "AWS Bedrock",
    "azure-foundry": "Azure Foundry",
    "cron-script-only": "فقط اسکریپت Cron",
    "cron-troubleshooting": "عیب‌یابی Cron",
    "daily-briefing-bot": "ربات گزارش روزانه",
    "delegation-patterns": "الگوهای واگذاری",
    "github-pr-review-agent": "Agent بررسی PR گیتهاب",
    "google-gemini": "Google Gemini",
    "google-vertex": "Google Vertex",
    "local-llm-on-mac": "LLM محلی روی مک",
    "local-ollama-setup": "تنظیم Ollama محلی",
    "microsoft-graph-app-registration": "ثبت برنامه Microsoft Graph",
    "migrate-from-openclaw": "مهاجرت از OpenClaw",
    "minimax-oauth": "OAuth MiniMax",
    "oauth-over-ssh": "OAuth از طریق SSH",
    "operate-teams-meeting-pipeline": "راه‌اندازی خط لوله جلسات Teams",
    "pipe-script-output": "خروجی اسکریپت لوله‌ای",
    "python-library": "کتابخانه پایتون",
    "run-hermes-with-nous-portal": "اجرای Hermes با Nous Portal",
    "run-nemotron-3-ultra-free": "اجرای رایگان Nemotron 3 Ultra",
    "team-telegram-assistant": "دستیار تلگرام تیمی",
    "use-soul-with-hermes": "استفاده از Soul با Hermes",
    "webhook-github-pr-review": "Webhook بررسی PR گیتهاب",
    "work-with-skills": "کار با مهارت‌ها",
    "xai-grok-oauth": "OAuth xAI Grok",
    "providers": "ارائه‌دهندگان",
    "automation-blueprints-catalog": "کاتالوگ نقشه‌های اتوماسیون",
    "environment-variables": "متغیرهای محیطی",
    "mcp-config-reference": "مرجع پیکربندی MCP",
    "model-catalog": "کاتالوگ مدل‌ها",
    "optional-skills-catalog": "کاتالوگ مهارت‌های اختیاری",
    "profile-commands": "دستورات پروفایل",
    "skills-catalog": "کاتالوگ مهارت‌ها",
    "slash-commands": "دستورات اسلش",
    "toolsets-reference": "مرجع مجموعه ابزارها",
    "tools-reference": "مرجع ابزارها",
    "acp": "ACP",
    "api-server": "سرور API",
    "batch-processing": "پردازش دسته‌ای",
    "browser": "مرورگر",
    "built-in-plugins": "پلاگین‌های داخلی",
    "code-execution": "اجرای کد",
    "codex-app-server-runtime": "محیط اجرای سرور برنامه Codex",
    "computer-use": "استفاده از کامپیوتر",
    "context-references": "مرجع‌های زمینه",
    "credential-pools": "استخر اعتبارنامه‌ها",
    "cron": "Cron",
    "curator": "Curator",
    "delegation": "واگذاری",
    "deliverable-mode": "حالت قابل تحویل",
    "extending-the-dashboard": "گسترش داشبورد",
    "fallback-providers": "ارائه‌دهندگان پشتیبان",
    "goals": "اهداف",
    "honcho": "Honcho",
    "hooks": "Hookها",
    "image-generation": "تولید تصویر",
    "kanban": "Kanban",
    "kanban-tutorial": "آموزش Kanban",
    "kanban-worker-lanes": "لاین‌های کاری Kanban",
    "lsp": "LSP",
    "memory-providers": "ارائه‌دهندگان حافظه",
    "mixture-of-agents": "ترکیب Agentها",
    "overview": "نمای کلی",
    "pets": "حیوانات خانگی",
    "plugins": "پلاگین‌ها",
    "provider-routing": "مسیریابی ارائه‌دهنده",
    "skins": "پوسته‌ها",
    "spotify": "Spotify",
    "subscription-proxy": "پروکسی اشتراک",
    "tool-gateway": "Tool Gateway",
    "tool-search": "جستجوی ابزار",
    "tts": "TTS",
    "vision": "بینایی",
    "web-dashboard": "دابورد وب",
    "web-search": "جستجوی وب",
    "x-search": "جستجوی X",
    "bluebubbles": "BlueBubbles",
    "dingtalk": "DingTalk",
    "discord": "Discord",
    "email": "ایمیل",
    "feishu": "Feishu",
    "google": "Google",
    "homeassistant": "Home Assistant",
    "irc": "IRC",
    "line": "LINE",
    "matrix": "Matrix",
    "mattermost": "Mattermost",
    "msgraph-webhook": "Webhook Microsoft Graph",
    "ntfy": "ntfy",
    "open-webui": "Open WebUI",
    "photon": "Photon",
    "qqbot": "QQ Bot",
    "raft": "Raft",
    "signal": "Signal",
    "simplex": "SimpleX",
    "slack": "Slack",
    "sms": "پیامک (Twilio)",
    "teams": "Microsoft Teams",
    "teams-meetings": "جلسات Microsoft Teams",
    "telegram": "تلگرام",
    "webhooks": "Webhookها",
    "wecom": "WeCom",
    "wecom-callback": "WeCom Callback",
    "weixin": "Weixin (WeChat)",
    "whatsapp": "WhatsApp",
    "whatsapp-cloud": "WhatsApp Business Cloud API",
    "yuanbao": "Yuanbao",
    "bitwarden": "Bitwarden",
    "onepassword": "1Password",
    "secrets": "رازها",
}

def make_title(slug):
    """Get Farsi title for a slug."""
    name = slug.split('/')[-1]
    return TITLES.get(name, name.replace('-', ' ').title())

def main():
    count = 0
    for scraped_file in sorted(SCRAPED_DIR.glob("*.md")):
        # Parse the slug from filename
        slug_raw = scraped_file.stem  # e.g. "developer-guide_acp-internals"
        # Convert back to path: developer-guide/acp-internals
        parts = slug_raw.split('_', 1)
        if len(parts) == 2:
            section, page = parts
            path = f"docs/{section}/{page}.md"
            permalink = f"/docs/{section}/{page}/"
            title = make_title(page)
        else:
            continue
        
        content = scraped_file.read_text(encoding='utf-8')
        if len(content) < 50:
            continue
        
        # Add front matter
        front = f"""---
layout: docs
title: "{title}"
permalink: {permalink}
---

"""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(front + content, encoding='utf-8')
        count += 1
        print(f"  {path} ({len(content)} chars)")
    
    print(f"\nWrote {count} files")

if __name__ == "__main__":
    main()
