---
layout: docs
title: "Messaging_Qqbot"
permalink: /docs/user-guide/messaging_qqbot/
---

- 
- Messaging Platforms
- Chinese platforms
- QQ Bot

# QQ Bot

Connect Hermes to QQ via theOfficial QQ Bot API (v2)— supporting private (C2C), group @-mentions, guild, and direct messages with voice transcription.

## Overview​

The QQ Bot adapter uses theOfficial QQ Bot APIto:

- Receive messages via a persistentWebSocketconnection to the QQ Gateway
- Send text and markdown replies via theREST API
- Download and process images, voice messages, and file attachments
- Transcribe voice messages using Tencent's built-in ASR or a configurable STT provider

## Prerequisites​

1. QQ Bot Application— Register atq.qq.com:Create a new application and note yourApp IDandApp SecretEnable the required intents: C2C messages, Group @-messages, Guild messagesConfigure your bot in sandbox mode for testing, or publish for production
2. Dependencies— The adapter requiresaiohttpandhttpx:pipinstallaiohttp httpx

QQ Bot Application— Register atq.qq.com:

- Create a new application and note yourApp IDandApp Secret
- Enable the required intents: C2C messages, Group @-messages, Guild messages
- Configure your bot in sandbox mode for testing, or publish for production

Dependencies— The adapter requiresaiohttpandhttpx:

`aiohttp`
`httpx`

```
pip install aiohttp httpx
```

## Configuration​

### Interactive setup​

```
hermes gateway setup
```

SelectQQ Botfrom the platform list and follow the prompts.

### Manual configuration​

Set the required environment variables in~/.hermes/.env:

`~/.hermes/.env`

```
QQ_APP_ID=your-app-idQQ_CLIENT_SECRET=your-app-secret
```

## Environment Variables​

| Variable | Description | Default |
| --- | --- | --- |
| QQ_APP_ID | QQ Bot App ID (required) | — |
| QQ_CLIENT_SECRET | QQ Bot App Secret (required) | — |
| QQBOT_HOME_CHANNEL | OpenID for cron/notification delivery | — |
| QQBOT_HOME_CHANNEL_NAME | Display name for home channel | Home |
| QQ_ALLOWED_USERS | Comma-separated user OpenIDs for DM access | open (all users) |
| QQ_GROUP_ALLOWED_USERS | Comma-separated group OpenIDs for group access | — |
| QQ_ALLOW_ALL_USERS | Set totrueto allow all DMs | false |
| QQ_PORTAL_HOST | Override the QQ portal host (set tosandbox.q.qq.comfor sandbox routing) | q.qq.com |
| QQ_STT_API_KEY | API key for voice-to-text provider | — |
| QQ_STT_BASE_URL | (Not read directly — setplatforms.qqbot.extra.stt.baseUrlinconfig.yamlinstead) | n/a |
| QQ_STT_MODEL | STT model name | glm-asr |

`QQ_APP_ID`
`QQ_CLIENT_SECRET`
`QQBOT_HOME_CHANNEL`
`QQBOT_HOME_CHANNEL_NAME`
`Home`
`QQ_ALLOWED_USERS`
`QQ_GROUP_ALLOWED_USERS`
`QQ_ALLOW_ALL_USERS`
`true`
`false`
`QQ_PORTAL_HOST`
`sandbox.q.qq.com`
`q.qq.com`
`QQ_STT_API_KEY`
`QQ_STT_BASE_URL`
`platforms.qqbot.extra.stt.baseUrl`
`config.yaml`
`QQ_STT_MODEL`
`glm-asr`

## Advanced Configuration​

For fine-grained control, add platform settings to~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
platforms:  qqbot:    enabled: true    extra:      app_id: "your-app-id"      client_secret: "your-secret"      markdown_support: true       # enable QQ markdown (msg_type 2). Config-only; no env-var equivalent.      dm_policy: "open"          # open | allowlist | disabled      allow_from:        - "user_openid_1"      group_policy: "open"       # open | allowlist | disabled      group_allow_from:        - "group_openid_1"      stt:        provider: "zai"          # zai (GLM-ASR), openai (Whisper), etc.        baseUrl: "https://open.bigmodel.cn/api/coding/paas/v4"        apiKey: "your-stt-key"        model: "glm-asr"
```

## Voice Messages (STT)​

Voice transcription works in two stages:

1. QQ built-in ASR(free, always tried first) — QQ providesasr_refer_textin voice message attachments, which uses Tencent's own speech recognition
2. Configured STT provider(fallback) — If QQ's ASR doesn't return text, the adapter calls an OpenAI-compatible STT API:Zhipu/GLM (zai): Default provider, usesglm-asrmodelOpenAI Whisper: SetQQ_STT_BASE_URLandQQ_STT_MODELAny OpenAI-compatible STT endpoint

QQ built-in ASR(free, always tried first) — QQ providesasr_refer_textin voice message attachments, which uses Tencent's own speech recognition

`asr_refer_text`

Configured STT provider(fallback) — If QQ's ASR doesn't return text, the adapter calls an OpenAI-compatible STT API:

- Zhipu/GLM (zai): Default provider, usesglm-asrmodel
- OpenAI Whisper: SetQQ_STT_BASE_URLandQQ_STT_MODEL
- Any OpenAI-compatible STT endpoint

`glm-asr`
`QQ_STT_BASE_URL`
`QQ_STT_MODEL`

## Troubleshooting​

### Bot disconnects immediately (quick disconnect)​

This usually means:

- Invalid App ID / Secret— Double-check your credentials at q.qq.com
- Missing permissions— Ensure the bot has the required intents enabled
- Sandbox-only bot— If the bot is in sandbox mode, it can only receive messages from QQ's sandbox test channel

### Voice messages not transcribed​

1. Check if QQ's built-inasr_refer_textis present in the attachment data
2. If using a custom STT provider, verifyQQ_STT_API_KEYis set correctly
3. Check gateway logs for STT error messages

`asr_refer_text`
`QQ_STT_API_KEY`

### Messages not delivered​

- Verify the bot'sintentsare enabled at q.qq.com
- CheckQQ_ALLOWED_USERSif DM access is restricted
- For group messages, ensure the bot is@mentioned(group policy may require allowlisting)
- CheckQQBOT_HOME_CHANNELfor cron/notification delivery

`QQ_ALLOWED_USERS`
`QQBOT_HOME_CHANNEL`

### Connection errors​

- Ensureaiohttpandhttpxare installed:pip install aiohttp httpx
- Check network connectivity toapi.sgroup.qq.comand the WebSocket gateway
- Review gateway logs for detailed error messages and reconnect behavior

`aiohttp`
`httpx`
`pip install aiohttp httpx`
`api.sgroup.qq.com`