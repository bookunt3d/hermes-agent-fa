---
layout: docs
title: "Messaging_Email"
permalink: /docs/user-guide/messaging/email/
---

- 
- Messaging Platforms
- Popular
- Email

# Email Setup

Hermes can receive and reply to emails using standard IMAP and SMTP protocols. Send an email to the agent's address and it replies in-thread — no special client or bot API needed. Works with Gmail, Outlook, Yahoo, Fastmail, or any provider that supports IMAP/SMTP.

This page covers the Email gateway adapter, which uses Python's built-inimaplib,smtplib, andemailmodules. No additional packages or external services are required for this gateway path.

`imaplib`
`smtplib`
`email`

This is separate from the bundledHimalaya email skill, which lets the agent manage email through terminal commands and requires the externalhimalayaCLI plus a Himalaya config file.

`himalaya`
| Use case | What to configure | External dependency |
| --- | --- | --- |
| Let people email the Hermes agent and receive replies | Email gateway adapter on this page | None beyond an IMAP/SMTP email account |
| Let the agent inspect, compose, move, and manage mailbox messages from terminal tools | Himalaya email skill | himalayaCLI and~/.config/himalaya/config.toml |

`himalaya`
`~/.config/himalaya/config.toml`

## Prerequisites​

- A dedicated email accountfor your Hermes agent (don't use your personal email)
- IMAP enabledon the email account
- An app passwordif using Gmail or another provider with 2FA

### Gmail Setup​

1. Enable 2-Factor Authentication on your Google Account
2. Go toApp Passwords
3. Create a new App Password (select "Mail" or "Other")
4. Copy the 16-character password — you'll use this instead of your regular password

### Outlook / Microsoft 365​

1. Go toSecurity Settings
2. Enable 2FA if not already active
3. Create an App Password under "Additional security options"
4. IMAP host:outlook.office365.com, SMTP host:smtp.office365.com

`outlook.office365.com`
`smtp.office365.com`

### Other Providers​

Most email providers support IMAP/SMTP. Check your provider's documentation for:

- IMAP host and port (usually port 993 with SSL)
- SMTP host and port (usually port 587 with STARTTLS)
- Whether app passwords are required

## Step 1: Configure Hermes​

The easiest way:

```
hermes gateway setup
```

SelectEmailfrom the platform menu. The wizard prompts for your email address, password, IMAP/SMTP hosts, and allowed senders.

### Manual Configuration​

Add to~/.hermes/.env:

`~/.hermes/.env`

```
# RequiredEMAIL_ADDRESS=hermes@gmail.comEMAIL_PASSWORD=abcd efgh ijkl mnop    # App password (not your regular password)EMAIL_IMAP_HOST=imap.gmail.comEMAIL_SMTP_HOST=smtp.gmail.com# Security (recommended)EMAIL_ALLOWED_USERS=your@email.com,colleague@work.com# OptionalEMAIL_IMAP_PORT=993                    # Default: 993 (IMAP SSL)EMAIL_SMTP_PORT=587                    # Default: 587 (SMTP STARTTLS)EMAIL_POLL_INTERVAL=15                 # Seconds between inbox checks (default: 15)EMAIL_HOME_ADDRESS=your@email.com      # Default delivery target for cron jobs
```

## Step 2: Start the Gateway​

```
hermes gateway              # Run in foregroundhermes gateway install      # Install as a user servicesudo hermes gateway install --system   # Linux only: boot-time system service
```

On startup, the adapter:

1. Tests IMAP and SMTP connections
2. Marks all existing inbox messages as "seen" (only processes new emails)
3. Starts polling for new messages

## How It Works​

### Receiving Messages​

The adapter polls the IMAP inbox for UNSEEN messages at a configurable interval (default: 15 seconds). For each new email:

- Subject lineis included as context (e.g.,[Subject: Deploy to production])
- Reply emails(subject starting withRe:) skip the subject prefix — the thread context is already established
- Attachmentsare cached locally:Images (JPEG, PNG, GIF, WebP) → available to the vision toolDocuments (PDF, ZIP, etc.) → available for file access
- HTML-only emailshave tags stripped for plain text extraction
- Self-messagesare filtered out to prevent reply loops
- Automated/noreply sendersare silently ignored —noreply@,mailer-daemon@,bounce@,no-reply@, and emails withAuto-Submitted,Precedence: bulk, orList-Unsubscribeheaders

`[Subject: Deploy to production]`
`Re:`
- Images (JPEG, PNG, GIF, WebP) → available to the vision tool
- Documents (PDF, ZIP, etc.) → available for file access

`noreply@`
`mailer-daemon@`
`bounce@`
`no-reply@`
`Auto-Submitted`
`Precedence: bulk`
`List-Unsubscribe`

### Sending Replies​

Replies are sent via SMTP with proper email threading:

- In-Reply-ToandReferencesheaders maintain the thread
- Subject linepreserved withRe:prefix (no doubleRe: Re:)
- Message-IDgenerated with the agent's domain
- Responses are sent as plain text (UTF-8)

`Re:`
`Re: Re:`

### File Attachments​

The agent can send file attachments in replies. IncludeMEDIA:/path/to/filein the response and the file is attached to the outgoing email.

`MEDIA:/path/to/file`

### Skipping Attachments​

To ignore all incoming attachments (for malware protection or bandwidth savings), add to yourconfig.yaml:

`config.yaml`

```
platforms:  email:    skip_attachments: true
```

When enabled, attachment and inline parts are skipped before payload decoding. The email body text is still processed normally.

## Access Control​

Email access is stricter by default than chat-style platforms:

1. EMAIL_ALLOWED_USERSset→ only emails from those addresses are processed
2. No allowlist set→ unknown senders are ignored silently
3. EMAIL_ALLOW_ALL_USERS=true→ any sender is accepted (use with caution)
4. platforms.email.unauthorized_dm_behavior: pair→ unknown senders receive a pairing code

`EMAIL_ALLOWED_USERS`
`EMAIL_ALLOW_ALL_USERS=true`
`platforms.email.unauthorized_dm_behavior: pair`

Use a dedicated inbox and configureEMAIL_ALLOWED_USERSfor normal operation.Email pairing is opt-in because shared inboxes often contain unrelated unread messages, and Hermes should not reply to those contacts by default.

`EMAIL_ALLOWED_USERS`

## Troubleshooting​

| Problem | Solution |
| --- | --- |
| "IMAP connection failed"at startup | VerifyEMAIL_IMAP_HOSTandEMAIL_IMAP_PORT. Ensure IMAP is enabled on the account. For Gmail, enable it in Settings → Forwarding and POP/IMAP. |
| "SMTP connection failed"at startup | VerifyEMAIL_SMTP_HOSTandEMAIL_SMTP_PORT. Check that your password is correct (use App Password for Gmail). |
| Messages not received | CheckEMAIL_ALLOWED_USERSincludes the sender's email. Check spam folder — some providers flag automated replies. |
| "Authentication failed" | For Gmail, you must use an App Password, not your regular password. Ensure 2FA is enabled first. |
| Duplicate replies | Ensure only one gateway instance is running. Checkhermes gateway status. |
| Slow response | The default poll interval is 15 seconds. Reduce withEMAIL_POLL_INTERVAL=5for faster response (but more IMAP connections). |
| Replies not threading | The adapter uses In-Reply-To headers. Some email clients (especially web-based) may not thread correctly with automated messages. |

`EMAIL_IMAP_HOST`
`EMAIL_IMAP_PORT`
`EMAIL_SMTP_HOST`
`EMAIL_SMTP_PORT`
`EMAIL_ALLOWED_USERS`
`hermes gateway status`
`EMAIL_POLL_INTERVAL=5`

## Security​

Use a dedicated email account.Don't use your personal email — the agent stores the password in.envand has full inbox access via IMAP.

`.env`
- UseApp Passwordsinstead of your main password (required for Gmail with 2FA)
- SetEMAIL_ALLOWED_USERSto restrict who can interact with the agent
- The password is stored in~/.hermes/.env— protect this file (chmod 600)
- IMAP uses SSL (port 993) and SMTP uses STARTTLS (port 587) by default — connections are encrypted

`EMAIL_ALLOWED_USERS`
`~/.hermes/.env`
`chmod 600`

## Environment Variables Reference​

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| EMAIL_ADDRESS | Yes | — | Agent's email address |
| EMAIL_PASSWORD | Yes | — | Email password or app password |
| EMAIL_IMAP_HOST | Yes | — | IMAP server host (e.g.,imap.gmail.com) |
| EMAIL_SMTP_HOST | Yes | — | SMTP server host (e.g.,smtp.gmail.com) |
| EMAIL_IMAP_PORT | No | 993 | IMAP server port |
| EMAIL_SMTP_PORT | No | 587 | SMTP server port |
| EMAIL_POLL_INTERVAL | No | 15 | Seconds between inbox checks |
| EMAIL_ALLOWED_USERS | No | — | Comma-separated allowed sender addresses |
| EMAIL_HOME_ADDRESS | No | — | Default delivery target for cron jobs |
| EMAIL_ALLOW_ALL_USERS | No | false | Allow all senders (not recommended) |

`EMAIL_ADDRESS`
`EMAIL_PASSWORD`
`EMAIL_IMAP_HOST`
`imap.gmail.com`
`EMAIL_SMTP_HOST`
`smtp.gmail.com`
`EMAIL_IMAP_PORT`
`993`
`EMAIL_SMTP_PORT`
`587`
`EMAIL_POLL_INTERVAL`
`15`
`EMAIL_ALLOWED_USERS`
`EMAIL_HOME_ADDRESS`
`EMAIL_ALLOW_ALL_USERS`
`false`