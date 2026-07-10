---
layout: docs
title: "Features_Credential Pools"
permalink: /docs/user-guide/features/credential-pools/
---

- 
- Integrations
- Credential Pools

# Credential Pools

Credential pools let you register multiple API keys or OAuth tokens for the same provider. When one key hits a rate limit or billing quota, Hermes automatically rotates to the next healthy key — keeping your session alive without switching providers.

This is different fromfallback providers, which switch to adifferentprovider entirely. Credential pools are same-provider rotation; fallback providers are cross-provider failover. Pools are tried first — if all pool keys are exhausted,thenthe fallback provider activates.

Provider-side prompt caches (Anthropic, OpenAI, OpenRouter) are scoped to the account/API key that made the request. When the pool rotates to a different key mid-session, the new key has no cached prefix for your conversation — the next request re-reads the full history at undiscounted input price, and rotating back later is another full re-read unless the earlier key's cache TTL is still alive. Rotation keeps your session running, which is the point, but on long conversations each rotation costs one full-price pass over the context.

Credential pools are mainly for API-key providers (OpenRouter, Anthropic). A singleNous PortalOAuth covers 300+ models, so most users don't need a pool when on Portal.

## How It Works​

```
Your request  → Pick key from pool (round_robin / least_used / fill_first / random)  → Send to provider  → 429 rate limit?      → Plan/usage limit reached (e.g. ChatGPT/Codex "usage limit reached")?          → Rotate to next pool key immediately (no retry — the cap won't clear on retry)      → Generic / transient 429?          → Retry same key once (transient blip)          → Second 429 → rotate to next pool key      → All keys exhausted → fallback_model (different provider)  → 402 billing error?      → Immediately rotate to next pool key (24h cooldown)  → 401 auth expired?      → Try refreshing the token (OAuth)      → Refresh failed → rotate to next pool key  → Success → continue normally
```

## Quick Start​

If you already have an API key set in.env, Hermes auto-discovers it as a 1-key pool. To benefit from pooling, add more keys:

`.env`

```
# Add a second OpenRouter keyhermes auth add openrouter --api-key sk-or-v1-your-second-key# Add a second Anthropic keyhermes auth add anthropic --type api-key --api-key sk-ant-api03-your-second-key# Add an Anthropic OAuth credential (requires Claude Max plan + extra usage credits)hermes auth add anthropic --type oauth# Opens browser for OAuth login
```

Check your pools:

```
hermes auth list
```

Output:

```
openrouter (2 credentials):  #1  OPENROUTER_API_KEY   api_key env:OPENROUTER_API_KEY ←  #2  backup-key           api_key manualanthropic (3 credentials):  #1  hermes_pkce          oauth   hermes_pkce ←  #2  claude_code          oauth   claude_code  #3  ANTHROPIC_API_KEY    api_key env:ANTHROPIC_API_KEY
```

The←marks the currently selected credential.

`←`

## Interactive Management​

Runhermes authwith no subcommand for an interactive wizard:

`hermes auth`

```
hermes auth
```

This shows your full pool status and offers a menu:

```
What would you like to do?  1. Add a credential  2. Remove a credential  3. Reset cooldowns for a provider  4. Set rotation strategy for a provider  5. Exit
```

For providers that support both API keys and OAuth (Anthropic, Nous, Codex), the add flow asks which type:

```
anthropic supports both API keys and OAuth login.  1. API key (paste a key from the provider dashboard)  2. OAuth login (authenticate via browser)Type [1/2]:
```

## CLI Commands​

| Command | Description |
| --- | --- |
| hermes auth | Interactive pool management wizard |
| hermes auth list | Show all pools and credentials |
| hermes auth list <provider> | Show a specific provider's pool |
| hermes auth add <provider> | Add a credential (prompts for type and key) |
| hermes auth add <provider> --type api-key --api-key <key> | Add an API key non-interactively |
| hermes auth add <provider> --type oauth | Add an OAuth credential via browser login |
| hermes auth remove <provider> <index> | Remove credential by 1-based index |
| hermes auth reset <provider> | Clear all cooldowns/exhaustion status |

`hermes auth`
`hermes auth list`
`hermes auth list <provider>`
`hermes auth add <provider>`
`hermes auth add <provider> --type api-key --api-key <key>`
`hermes auth add <provider> --type oauth`
`hermes auth remove <provider> <index>`
`hermes auth reset <provider>`

## Rotation Strategies​

Configure viahermes auth→ "Set rotation strategy" or inconfig.yaml:

`hermes auth`
`config.yaml`

```
credential_pool_strategies:  openrouter: round_robin  anthropic: least_used
```

| Strategy | Behavior |
| --- | --- |
| fill_first(default) | Use the first healthy key until it's exhausted, then move to the next |
| round_robin | Cycle through keys evenly, rotating after each selection |
| least_used | Always pick the key with the lowest request count |
| random | Random selection among healthy keys |

`fill_first`
`round_robin`
`least_used`
`random`

## Error Recovery​

The pool handles different errors differently:

| Error | Behavior | Cooldown |
| --- | --- | --- |
| 429 Rate Limit | Retry same key once (transient). Second consecutive 429 rotates to next key | 1 hour |
| 402 Billing/Quota | Immediately rotate to next key | 24 hours |
| 401 Auth Expired | Try refreshing the OAuth token first. Rotate only if refresh fails | — |
| All keys exhausted | Fall through tofallback_modelif configured | — |

`fallback_model`

Thehas_retried_429flag resets on every successful API call, so a single transient 429 doesn't trigger rotation.

`has_retried_429`

## Custom Endpoint Pools​

Custom OpenAI-compatible endpoints (Together.ai, RunPod, local servers) get their own pools, keyed by the endpoint name fromcustom_providersin config.yaml.

`custom_providers`

When you set up a custom endpoint viahermes model, it auto-generates a name like "Together.ai" or "Local (localhost:8080)". This name becomes the pool key.

`hermes model`

```
# After setting up a custom endpoint via hermes model:hermes auth list# Shows:#   Together.ai (1 credential):#     #1  config key    api_key config:Together.ai ←# Add a second key for the same endpoint:hermes auth add Together.ai --api-key sk-together-second-key
```

Custom endpoint pools are stored inauth.jsonundercredential_poolwith acustom:prefix:

`auth.json`
`credential_pool`
`custom:`

```
{  "credential_pool": {    "openrouter": [...],    "custom:together.ai": [...]  }}
```

## Auto-Discovery​

Hermes automatically discovers credentials from multiple sources and seeds the pool on startup:

| Source | Example | Auto-seeded? |
| --- | --- | --- |
| Environment variables | OPENROUTER_API_KEY,ANTHROPIC_API_KEY | Yes |
| OAuth tokens (auth.json) | Codex device code, Nous device code | Yes |
| Claude Code credentials | ~/.claude/.credentials.json | Yes (Anthropic) |
| Hermes PKCE OAuth | ~/.hermes/auth.json | Yes (Anthropic) |
| Custom endpoint config | model.api_keyin config.yaml | Yes (custom endpoints) |
| Manual entries | Added viahermes auth add | Persisted in auth.json |

`OPENROUTER_API_KEY`
`ANTHROPIC_API_KEY`
`~/.claude/.credentials.json`
`~/.hermes/auth.json`
`model.api_key`
`hermes auth add`

Auto-seeded entries are updated on each pool load — if you remove an env var, its pool entry is automatically pruned. Manual entries (added viahermes auth add) are never auto-pruned.

`hermes auth add`

Borrowed runtime secrets (for example env vars, Bitwarden/Vault/keyring/systemd references, and custom config values) are reference-only at theauth.jsonboundary. Hermes can use the resolved value in memory for the current run, but it persists only metadata such as the source ref, label, status, request counters, and a non-reversible fingerprint. Manual entries and Hermes-owned OAuth/device-code state keep the durable tokens they need to refresh.

`auth.json`

## Delegation & Subagent Sharing​

When the agent spawns subagents viadelegate_task, the parent's credential pool is automatically shared with children:

`delegate_task`
- Same provider— the child receives the parent's full pool, enabling key rotation on rate limits
- Different provider— the child loads that provider's own pool (if configured)
- No pool configured— the child falls back to the inherited single API key

This means subagents benefit from the same rate-limit resilience as the parent, with no extra configuration needed. Per-task credential leasing ensures children don't conflict with each other when rotating keys concurrently.

## Thread Safety​

The credential pool uses a threading lock for all state mutations (select(),mark_exhausted_and_rotate(),try_refresh_current(),mark_used()). This ensures safe concurrent access when the gateway handles multiple chat sessions simultaneously.

`select()`
`mark_exhausted_and_rotate()`
`try_refresh_current()`
`mark_used()`

## Architecture​

For the full data flow diagram, seedocs/credential-pool-flow.excalidrawin the repository.

`docs/credential-pool-flow.excalidraw`

The credential pool integrates at the provider resolution layer:

1. agent/credential_pool.py— Pool manager: storage, selection, rotation, cooldowns
2. hermes_cli/auth_commands.py— CLI commands and interactive wizard
3. hermes_cli/runtime_provider.py— Pool-aware credential resolution
4. run_agent.py— Error recovery: 429/402/401 → pool rotation → fallback

`agent/credential_pool.py`
`hermes_cli/auth_commands.py`
`hermes_cli/runtime_provider.py`
`run_agent.py`

## Storage​

Pool state is stored in~/.hermes/auth.jsonunder thecredential_poolkey:

`~/.hermes/auth.json`
`credential_pool`

```
{  "version": 1,  "credential_pool": {    "openrouter": [      {        "id": "abc123",        "label": "OPENROUTER_API_KEY",        "auth_type": "api_key",        "priority": 0,        "source": "env:OPENROUTER_API_KEY",        "secret_source": "bitwarden",        "secret_fingerprint": "sha256:12ab34cd56ef7890",        "last_status": "ok",        "request_count": 142      }    ],    "anthropic": [      {        "id": "manual1",        "label": "personal-api-key",        "auth_type": "api_key",        "priority": 0,        "source": "manual",        "access_token": "sk-ant-api03-..."      }    ]  }}
```

The OpenRouter entry above was borrowed from an external source, so the raw key is not stored inauth.json. The manual Anthropic entry was intentionally added to Hermes' credential store, so its token remains persistable.

`auth.json`

Strategies are stored inconfig.yaml(notauth.json):

`config.yaml`
`auth.json`

```
credential_pool_strategies:  openrouter: round_robin  anthropic: least_used
```