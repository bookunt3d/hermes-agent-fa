---
layout: docs
title: "Messaging_Sms"
permalink: /docs/user-guide/messaging/sms/
---

- 
- Messaging Platforms
- Popular
- SMS (Twilio)

# SMS Setup (Twilio)

Hermes connects to SMS through theTwilioAPI. People text your Twilio phone number and get AI responses back — same conversational experience as Telegram or Discord, but over standard text messages.

The SMS gateway shares credentials with the optionaltelephony skill. If you've already set up Twilio for voice calls or one-off SMS, the gateway works with the sameTWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN, andTWILIO_PHONE_NUMBER.

`TWILIO_ACCOUNT_SID`
`TWILIO_AUTH_TOKEN`
`TWILIO_PHONE_NUMBER`

## Prerequisites​

- Twilio account—Sign up at twilio.com(free trial available)
- A Twilio phone numberwith SMS capability
- A publicly accessible server— Twilio sends webhooks to your server when SMS arrives
- aiohttp—cd ~/.hermes/hermes-agent && uv pip install -e ".[sms]"

`cd ~/.hermes/hermes-agent && uv pip install -e ".[sms]"`

## Step 1: Get Your Twilio Credentials​

1. Go to theTwilio Console
2. Copy yourAccount SIDandAuth Tokenfrom the dashboard
3. Go toPhone Numbers → Manage → Active Numbers— note your phone number in E.164 format (e.g.,+15551234567)

`+15551234567`

## Step 2: Configure Hermes​

### Interactive setup (recommended)​

```
hermes gateway setup
```

SelectSMS (Twilio)from the platform list. The wizard will prompt for your credentials.

### Manual setup​

Add to~/.hermes/.env:

`~/.hermes/.env`

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxTWILIO_AUTH_TOKEN=your_auth_token_hereTWILIO_PHONE_NUMBER=+15551234567# Security: restrict to specific phone numbers (recommended)SMS_ALLOWED_USERS=+15559876543,+15551112222# Optional: set a home channel for cron job deliverySMS_HOME_CHANNEL=+15559876543
```

## Step 3: Configure Twilio Webhook​

Twilio needs to know where to send incoming messages. In theTwilio Console:

1. Go toPhone Numbers → Manage → Active Numbers
2. Click your phone number
3. UnderMessaging → A MESSAGE COMES IN, set:Webhook:https://your-server:8080/webhooks/twilioHTTP Method:POST

- Webhook:https://your-server:8080/webhooks/twilio
- HTTP Method:POST

`https://your-server:8080/webhooks/twilio`
`POST`

If you're running Hermes locally, use a tunnel to expose the webhook:

```
# Using cloudflaredcloudflared tunnel --url http://localhost:8080# Using ngrokngrok http 8080
```

Set the resulting public URL as your Twilio webhook.

SetSMS_WEBHOOK_URLto the same URL you configured in Twilio.This is required for Twilio signature validation — the adapter will refuse to start without it:

`SMS_WEBHOOK_URL`

```
# Must match the webhook URL in your Twilio ConsoleSMS_WEBHOOK_URL=https://your-server:8080/webhooks/twilio
```

The webhook port defaults to8080. Override with:

`8080`

```
SMS_WEBHOOK_PORT=3000
```

## Step 4: Start the Gateway​

```
hermes gateway
```

You should see:

```
[sms] Twilio webhook server listening on 127.0.0.1:8080, from: +1555***4567
```

If you seeRefusing to start: SMS_WEBHOOK_URL is required, setSMS_WEBHOOK_URLto the public URL configured in your Twilio Console (see Step 3).

`Refusing to start: SMS_WEBHOOK_URL is required`
`SMS_WEBHOOK_URL`

Text your Twilio number — Hermes will respond via SMS.

## Environment Variables​

| Variable | Required | Description |
| --- | --- | --- |
| TWILIO_ACCOUNT_SID | Yes | Twilio Account SID (starts withAC) |
| TWILIO_AUTH_TOKEN | Yes | Twilio Auth Token (also used for webhook signature validation) |
| TWILIO_PHONE_NUMBER | Yes | Your Twilio phone number (E.164 format) |
| SMS_WEBHOOK_URL | Yes | Public URL for Twilio signature validation — must match the webhook URL in your Twilio Console |
| SMS_WEBHOOK_PORT | No | Webhook listener port (default:8080) |
| SMS_WEBHOOK_HOST | No | Webhook bind address (default:127.0.0.1) |
| SMS_INSECURE_NO_SIGNATURE | No | Set totrueto disable signature validation (local dev only —not for production) |
| SMS_ALLOWED_USERS | No | Comma-separated E.164 phone numbers allowed to chat |
| SMS_ALLOW_ALL_USERS | No | Set totrueto allow anyone (not recommended) |
| SMS_HOME_CHANNEL | No | Phone number for cron job / notification delivery |
| SMS_HOME_CHANNEL_NAME | No | Display name for the home channel (default:Home) |

`TWILIO_ACCOUNT_SID`
`AC`
`TWILIO_AUTH_TOKEN`
`TWILIO_PHONE_NUMBER`
`SMS_WEBHOOK_URL`
`SMS_WEBHOOK_PORT`
`8080`
`SMS_WEBHOOK_HOST`
`127.0.0.1`
`SMS_INSECURE_NO_SIGNATURE`
`true`
`SMS_ALLOWED_USERS`
`SMS_ALLOW_ALL_USERS`
`true`
`SMS_HOME_CHANNEL`
`SMS_HOME_CHANNEL_NAME`
`Home`

## SMS-Specific Behavior​

- Plain text only— Markdown is automatically stripped since SMS renders it as literal characters
- 1600 character limit— Longer responses are split across multiple messages at natural boundaries (newlines, then spaces)
- Echo prevention— Messages from your own Twilio number are ignored to prevent loops
- Phone number redaction— Phone numbers are redacted in logs for privacy

## Security​

### Webhook signature validation​

Hermes validates that inbound webhooks genuinely originate from Twilio by verifying theX-Twilio-Signatureheader (HMAC-SHA1). This prevents attackers from injecting forged messages.

`X-Twilio-Signature`

SMS_WEBHOOK_URLis required.Set it to the public URL configured in your Twilio Console. The adapter will refuse to start without it.

`SMS_WEBHOOK_URL`

For local development without a public URL, you can disable validation:

```
# Local dev only — NOT for productionSMS_INSECURE_NO_SIGNATURE=true
```

### User allowlists​

The gateway denies all users by default.Configure an allowlist:

```
# Recommended: restrict to specific phone numbersSMS_ALLOWED_USERS=+15559876543,+15551112222# Or allow all (NOT recommended for bots with terminal access)SMS_ALLOW_ALL_USERS=true
```

SMS has no built-in encryption. Don't use SMS for sensitive operations unless you understand the security implications. For sensitive use cases, prefer Signal or Telegram.

## Troubleshooting​

### Messages not arriving​

1. Check your Twilio webhook URL is correct and publicly accessible
2. VerifyTWILIO_ACCOUNT_SIDandTWILIO_AUTH_TOKENare correct
3. Check the Twilio Console →Monitor → Logs → Messagingfor delivery errors
4. Ensure your phone number is inSMS_ALLOWED_USERS(orSMS_ALLOW_ALL_USERS=true)

`TWILIO_ACCOUNT_SID`
`TWILIO_AUTH_TOKEN`
`SMS_ALLOWED_USERS`
`SMS_ALLOW_ALL_USERS=true`

### Replies not sending​

1. CheckTWILIO_PHONE_NUMBERis set correctly (E.164 format with+)
2. Verify your Twilio account has SMS-capable numbers
3. Check Hermes gateway logs for Twilio API errors

`TWILIO_PHONE_NUMBER`
`+`

### Webhook port conflicts​

If port 8080 is already in use, change it:

```
SMS_WEBHOOK_PORT=3001
```

Update the webhook URL in Twilio Console to match.