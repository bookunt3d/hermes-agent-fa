---
layout: docs
title: "Secrets_Bitwarden"
permalink: /docs/user-guide/secrets/bitwarden/
---

- 
- Using Hermes
- Secrets
- Bitwarden Secrets Manager

# Bitwarden Secrets Manager

Pull API keys fromBitwarden Secrets Managerat process startup instead of storing them in plaintext inside~/.hermes/.env. One bootstrap secret (a machine-account access token) replaces N per-provider keys, and rotating a credential becomes a single change in the Bitwarden web app.

`~/.hermes/.env`

## How it works​

1. You create amachine accountin Bitwarden Secrets Manager, give it read access to a project, and generate anaccess token.
2. Hermes stores that single token in~/.hermes/.envasBWS_ACCESS_TOKEN.
3. Every timehermes(or the gateway, or a cron job) starts, after~/.hermes/.envhas loaded, Hermes callsbws secret list <project_id>and sets the returned keys intoos.environ.
4. By default Hermesoverridesvalues already in your environment, so Bitwarden is the source of truth — rotate a key once in the web app and every Hermes process picks it up on next start. Flipoverride_existing: falsein config if you want.envto win instead.

`~/.hermes/.env`
`BWS_ACCESS_TOKEN`
`hermes`
`~/.hermes/.env`
`bws secret list <project_id>`
`os.environ`
`override_existing: false`
`.env`

Thebwsbinary is auto-downloaded into~/.hermes/bin/on first use — noapt, nobrew, nosudo.

`bws`
`~/.hermes/bin/`
`apt`
`brew`
`sudo`

## Why machine accounts (and why no 2FA prompt)​

Bitwarden Secrets Manager is designed for non-interactive workloads: machine accounts can't be 2FA-gated because there's no human in the loop. The access token is the credential. Anyone with it can read every secret the machine account has access to, so treat it like a high-value bearer token — store it in.env(notconfig.yaml), and revoke + regenerate from the Bitwarden web app if it ever leaks.

`.env`
`config.yaml`

You set up the machine accountin the web app, where your normal 2FA applies. After that the token is autonomous.

## Setup​

### 1. Create a machine account and access token​

In theBitwarden web app(orvault.bitwarden.eufor EU accounts):

1. Switch toSecrets Managerfrom the product switcher.
2. Create or pick aProject(e.g. "Hermes keys").
3. Add your provider keys as secrets. The secretNamebecomes the environment variable name — useOPENROUTER_API_KEY,ANTHROPIC_API_KEY, etc.
4. Machine accounts → New machine account → My Hermes machine→Projectstab → grant Read access to your project.
5. Access tokenstab →Create access token→Neverexpires (or pick a date) → copy the token (starts with0.). Bitwarden cannot retrieve it again — keep the copy.

`OPENROUTER_API_KEY`
`ANTHROPIC_API_KEY`
`0.`

Secrets Manager is included on the Bitwarden free tier with limits; no paid plan needed to try this.

### 2. Run the wizard​

```
hermes secrets bitwarden setup
```

It will:

1. Download and verifybws v2.0.0into~/.hermes/bin/bws.
2. Prompt you for the access token (input is hidden). Stored in~/.hermes/.envasBWS_ACCESS_TOKEN.
3. Ask which Bitwarden region your machine account belongs to —US Cloud,EU Cloud, orself-hosted / custom URL. Stored inconfig.yamlassecrets.bitwarden.server_urland passed tobwsasBWS_SERVER_URL.
4. List the projects the machine account can see; pick one. Stored inconfig.yamlassecrets.bitwarden.project_id.
5. Test-fetch the project's secrets and show you which env vars will resolve.
6. Flipsecrets.bitwarden.enabled: true.

`bws v2.0.0`
`~/.hermes/bin/bws`
`~/.hermes/.env`
`BWS_ACCESS_TOKEN`
`config.yaml`
`secrets.bitwarden.server_url`
`bws`
`BWS_SERVER_URL`
`config.yaml`
`secrets.bitwarden.project_id`
`secrets.bitwarden.enabled: true`

Non-interactive setup is also supported via flags:

```
hermes secrets bitwarden setup \  --access-token "$BWS_ACCESS_TOKEN" \  --server-url https://vault.bitwarden.eu \  --project-id <project-uuid>
```

### 3. Confirm​

```
hermes secrets bitwarden status
```

From now on, everyhermesinvocation pulls fresh secrets at startup. You'll see a one-line summary in stderr the first time secrets are applied in a process.

`hermes`

## CLI​

| Command | What it does |
| --- | --- |
| hermes secrets bitwarden setup | Interactive wizard (install binary, prompt for token, pick project, test fetch) |
| hermes secrets bitwarden status | Show config + binary version + token presence |
| hermes secrets bitwarden sync | Dry-run: pull secrets now and show what would be applied |
| hermes secrets bitwarden sync --apply | Pull and export into the current shell's environment |
| hermes secrets bitwarden install | Just download the pinnedbwsbinary (no auth required) |
| hermes secrets bitwarden disable | Flipenabled: false; leaves token + project id in place |

`hermes secrets bitwarden setup`
`hermes secrets bitwarden status`
`hermes secrets bitwarden sync`
`hermes secrets bitwarden sync --apply`
`hermes secrets bitwarden install`
`bws`
`hermes secrets bitwarden disable`
`enabled: false`

## Configuration​

Defaults in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
secrets:  bitwarden:    enabled: false    access_token_env: BWS_ACCESS_TOKEN    project_id: ""    server_url: ""    cache_ttl_seconds: 300    override_existing: true    auto_install: true
```

| Key | Default | What it does |
| --- | --- | --- |
| enabled | false | Master switch. When false, Bitwarden is never contacted. |
| access_token_env | BWS_ACCESS_TOKEN | Env var name that holds the bootstrap token. Change this if you already useBWS_ACCESS_TOKENfor something else. |
| project_id | "" | UUID of the project to sync from. |
| server_url | "" | Bitwarden region or self-hosted endpoint. Empty =bwsdefault (US Cloud,https://vault.bitwarden.com). Set tohttps://vault.bitwarden.eufor EU Cloud, or your own URL for self-hosted. Plumbed into thebwssubprocess asBWS_SERVER_URL. |
| cache_ttl_seconds | 300 | How long an in-process fetch result is reused. Set to0to disable caching. Cache is per-process; newhermesinvocations start fresh. |
| override_existing | true | When true, Bitwarden values overwrite anything already in env (so rotation in the web app actually takes effect). Flip tofalseif you want.env/ shell exports to win locally. |
| auto_install | true | When true,bwsis auto-downloaded into~/.hermes/bin/on first use. |

`enabled`
`false`
`access_token_env`
`BWS_ACCESS_TOKEN`
`BWS_ACCESS_TOKEN`
`project_id`
`""`
`server_url`
`""`
`bws`
`https://vault.bitwarden.com`
`https://vault.bitwarden.eu`
`bws`
`BWS_SERVER_URL`
`cache_ttl_seconds`
`300`
`0`
`hermes`
`override_existing`
`true`
`false`
`.env`
`auto_install`
`true`
`bws`
`~/.hermes/bin/`

## Failure modes​

Bitwarden never blocks Hermes startup. If anything goes wrong, you'll see a one-line warning in stderr and Hermes continues with whatever credentials.envalready had:

`.env`
| Symptom | Cause | Fix |
| --- | --- | --- |
| BWS_ACCESS_TOKEN is not set | Enabled in config but token cleared from.env | Re-runhermes secrets bitwarden setup |
| bws exited 1: invalid access token | Token revoked or wrong | Generate a new token, re-run setup |
| [400 Bad Request] {"error":"invalid_client"} | Token is for a Bitwarden region other than the onebwsis calling (e.g. EU token hitting the US identity endpoint) | Re-run setup and pick the right region, or setsecrets.bitwarden.server_urltohttps://vault.bitwarden.eu(or your self-hosted URL) |
| bws timed out | Network blocked or Bitwarden API slow | Check connectivity toapi.bitwarden.com(or yourserver_url) |
| bws binary not available | auto_install: falseandbwsnot on PATH | Install manually fromgithub.com/bitwarden/sdk-sm/releasesor flipauto_installback on |
| Checksum mismatch | Download corrupted or tampered | Re-run, will retry; if it persists, file an issue |

`BWS_ACCESS_TOKEN is not set`
`.env`
`hermes secrets bitwarden setup`
`bws exited 1: invalid access token`
`[400 Bad Request] {"error":"invalid_client"}`
`bws`
`secrets.bitwarden.server_url`
`https://vault.bitwarden.eu`
`bws timed out`
`api.bitwarden.com`
`server_url`
`bws binary not available`
`auto_install: false`
`bws`
`auto_install`
`Checksum mismatch`

## Security notes​

- The bootstrap token (BWS_ACCESS_TOKEN) is itself sensitive — anyone with it can read every secret the machine account has access to. Treat it the same as any other API key.
- Hermes will refuse to let Bitwarden overwrite the bootstrap token itself, even withoverride_existing: true. If you storeBWS_ACCESS_TOKENas a secret inside the project, it's silently skipped during apply.
- Thebwsbinary download is verified against the published SHA-256 checksum from the same GitHub release. Mismatch aborts the install.
- The pinned version (bws v2.0.0at time of writing) is updated through PRs to this repo — Hermes does not auto-upgradebwsto "latest" because upstream release shapes can change.

`BWS_ACCESS_TOKEN`
`override_existing: true`
`BWS_ACCESS_TOKEN`
`bws`
`bws v2.0.0`
`bws`

## When NOT to use this​

- Single-machine personal setupswhere~/.hermes/.envis fine. You're trading one credential for another and adding a network dependency at startup.
- Air-gapped environmentsthat can't reachapi.bitwarden.com.
- CI/CDwhere the existing secrets-injection mechanism (GitHub Actions secrets, Vault, etc.) is already set up — pick one path, not two.

`~/.hermes/.env`
`api.bitwarden.com`

The good case for this is multi-machine fleets, shared dev boxes, gateway VPSes, or any setup where you want centralized rotation and revocation across multiple Hermes installations.