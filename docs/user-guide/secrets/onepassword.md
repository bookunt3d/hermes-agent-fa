---
layout: docs
title: "Secrets_Onepassword"
permalink: /docs/user-guide/secrets/onepassword/
---

- 
- Using Hermes
- Secrets
- 1Password

# 1Password

Resolve provider API keys from1Passwordat process startup instead of storing them in plaintext inside~/.hermes/.env. You keep your keys as 1Password items and reference them byop://vault/item/field; rotating a credential becomes a single change in 1Password.

`~/.hermes/.env`
`op://vault/item/field`

## How it works​

1. You install the official1Password CLI(op) and authenticate it — either with aservice-account token(headless servers) or aninteractive/desktop session(your laptop).
2. You map environment-variable names toop://references in~/.hermes/config.yaml.
3. Every timehermes(or the gateway, or a cron job) starts, after~/.hermes/.envhas loaded, Hermes runsop readfor each reference and sets the resolved values intoos.environ.
4. By default Hermesoverridesvalues already in your environment, so 1Password is the source of truth — rotate a credential once and every Hermes process picks it up on next start. Flipoverride_existing: falseif you want.envto win instead.

`op`
`op://`
`~/.hermes/config.yaml`
`hermes`
`~/.hermes/.env`
`op read`
`os.environ`
`override_existing: false`
`.env`

Hermes never authenticates on your behalf and never downloadsop: it shells out to your already-installed, already-trusted CLI. Ifopis missing, your session is locked, or a reference is wrong, Hermes prints a one-line warning and continues with whatever credentials.envalready had — it never blocks startup.

`op`
`op`
`.env`

## Authentication​

opsupports two non-interactive-friendly modes; Hermes works with either:

`op`
- Service accounts(recommended for servers/CI): create a service account in 1Password, grant it read access to the relevant vault, and export its token asOP_SERVICE_ACCOUNT_TOKENin~/.hermes/.env. The token is the credential — treat it like any other bearer token.
- Desktop / interactive sessions(laptops): runop signin(or enable CLI integration in the 1Password app). Hermes passes yourOP_SESSION_*variables through to theopchild process. The 1Password cache key includes those session variables, so signing into a different account never serves a value cached under the previous identity.

`OP_SERVICE_ACCOUNT_TOKEN`
`~/.hermes/.env`
`op signin`
`OP_SESSION_*`
`op`

## Bootstrap token​

When you authenticate with aservice-account token, that token is itself the bootstrap credential Hermes needsbeforeit can resolve anyop://reference. It must be present inos.environof every process that resolves secrets — including cron jobs (kanban.dispatch_in_gateway: false), subprocess invocations, CLI runs, macOS launchd agents, and Docker containers — not just the interactive gateway. There are three ways to make it available, in order of precedence:

`op://`
`os.environ`
`kanban.dispatch_in_gateway: false`
1. In~/.hermes/.env(recommended).hermes secrets onepassword setup --token <token>writes the token to~/.hermes/.env, exactly like Bitwarden'sBWS_ACCESS_TOKEN. Becauseload_hermes_dotenv()always loads.env, the token is available everywhere with zero extra setup. This is the simplest reliable option.
2. In~/.hermes/.op.env(gitignored).If you'd rather keep the service-account token out of.env— for example so.envcan be checked into a private dotfiles repo while the token stays out of version control — place it in~/.hermes/.op.env:echo'OP_SERVICE_ACCOUNT_TOKEN=ops_...'>~/.hermes/.op.envchmod600~/.hermes/.op.envHermes auto-loads.op.envat startup,after.env, andneveroverrides a token already present in the environment..op.envis gitignored so the token never enters a committed file.
3. Via systemdEnvironmentFile(Linux gateway).If you run the gateway under systemd, you can inject the token directly into the service environment:[Service]EnvironmentFile=-/home/youruser/.hermes/.op.envA token injected this way takes precedence — Hermes detects thatOP_SERVICE_ACCOUNT_TOKENis already set and skips loading.op.enventirely.

In~/.hermes/.env(recommended).hermes secrets onepassword setup --token <token>writes the token to~/.hermes/.env, exactly like Bitwarden'sBWS_ACCESS_TOKEN. Becauseload_hermes_dotenv()always loads.env, the token is available everywhere with zero extra setup. This is the simplest reliable option.

`~/.hermes/.env`
`hermes secrets onepassword setup --token <token>`
`~/.hermes/.env`
`BWS_ACCESS_TOKEN`
`load_hermes_dotenv()`
`.env`

In~/.hermes/.op.env(gitignored).If you'd rather keep the service-account token out of.env— for example so.envcan be checked into a private dotfiles repo while the token stays out of version control — place it in~/.hermes/.op.env:

`~/.hermes/.op.env`
`.env`
`.env`
`~/.hermes/.op.env`

```
echo 'OP_SERVICE_ACCOUNT_TOKEN=ops_...' > ~/.hermes/.op.envchmod 600 ~/.hermes/.op.env
```

Hermes auto-loads.op.envat startup,after.env, andneveroverrides a token already present in the environment..op.envis gitignored so the token never enters a committed file.

`.op.env`
`.env`
`.op.env`

Via systemdEnvironmentFile(Linux gateway).If you run the gateway under systemd, you can inject the token directly into the service environment:

`EnvironmentFile`

```
[Service]EnvironmentFile=-/home/youruser/.hermes/.op.env
```

A token injected this way takes precedence — Hermes detects thatOP_SERVICE_ACCOUNT_TOKENis already set and skips loading.op.enventirely.

`OP_SERVICE_ACCOUNT_TOKEN`
`.op.env`

If the token is reachable only through an interactive shell (op signin,OP_SESSION_*exports in.bashrc, etc.), it willnotbe inherited by cron jobs or freshly spawned subprocesses, and those contexts will log a warning and fall back to whatever credentials.envalready held. Use one of the three options above for any non-interactive workload.

`op signin`
`OP_SESSION_*`
`.bashrc`
`.env`

## Setup​

### 1. Install and sign in toop​

`op`

Follow the1Password CLI getting-started guide. Verify it works:

```
op whoami
```

### 2. Enable the integration​

```
hermes secrets onepassword setup
```

This verifiesopis onPATH(or use--binary-path), records your account/token settings, checks for an active session, and flipssecrets.onepassword.enabled: true. Non-interactive flags:

`op`
`PATH`
`--binary-path`
`secrets.onepassword.enabled: true`

```
hermes secrets onepassword setup \  --account my.1password.com \  --token-env OP_SERVICE_ACCOUNT_TOKEN \  --token "$OP_SERVICE_ACCOUNT_TOKEN"
```

### 3. Map your credentials​

The reference format isop://<vault>/<item>/<field>:

`op://<vault>/<item>/<field>`

```
hermes secrets onepassword set OPENAI_API_KEY    "op://Private/OpenAI/api key"hermes secrets onepassword set ANTHROPIC_API_KEY "op://Private/Anthropic/credential"
```

### 4. Preview and confirm​

```
hermes secrets onepassword sync     # dry-run: resolve now, show what would applyhermes secrets onepassword status   # config + binary + references + auth
```

From now on, everyhermesinvocation resolves the references at startup. You'll see a one-line summary in stderr the first time secrets are applied in a process.

`hermes`

## CLI​

| Command | What it does |
| --- | --- |
| hermes secrets onepassword setup | Verifyop, set account / token env var, enable |
| hermes secrets onepassword status | Show config, binary, auth, and configured references |
| hermes secrets onepassword set ENV_VAR "op://…" | Map an env var to a reference (stored stripped + validated) |
| hermes secrets onepassword remove ENV_VAR | Drop a mapping |
| hermes secrets onepassword sync | Dry-run: resolve references now and show what would apply |
| hermes secrets onepassword sync --apply | Resolve and export into the current shell's environment |
| hermes secrets onepassword disable | Flipenabled: false; leaves mappings in place |

`hermes secrets onepassword setup`
`op`
`hermes secrets onepassword status`
`hermes secrets onepassword set ENV_VAR "op://…"`
`hermes secrets onepassword remove ENV_VAR`
`hermes secrets onepassword sync`
`hermes secrets onepassword sync --apply`
`hermes secrets onepassword disable`
`enabled: false`

opand1passwordare accepted as aliases foronepassword.

`op`
`1password`
`onepassword`

## Configuration​

Defaults in~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
secrets:  onepassword:    enabled: false    env:      OPENAI_API_KEY: "op://Private/OpenAI/api key"      ANTHROPIC_API_KEY: "op://Private/Anthropic/credential"    account: ""    service_account_token_env: OP_SERVICE_ACCOUNT_TOKEN    binary_path: ""    cache_ttl_seconds: 300    override_existing: true
```

| Key | Default | What it does |
| --- | --- | --- |
| enabled | false | Master switch. When false,opis never invoked. |
| env | {} | Mapping of env-var name →op://vault/item/fieldreference. Entries whose name isn't a valid env-var name, or whose value isn't anop://reference, are skipped with a warning. |
| account | "" | Account shorthand / sign-in address passed asop read --account. Empty usesop's default account. |
| service_account_token_env | OP_SERVICE_ACCOUNT_TOKEN | Env var Hermes reads the service-account token from. Its value is exported to theopchild asOP_SERVICE_ACCOUNT_TOKEN(the nameopexpects). Leave the var unset to use a desktop/interactive session. |
| binary_path | "" | Absolute path toop. When set, it is used verbatim andPATHisnotconsulted — pin this to avoid trusting whateveropappears first onPATH. |
| cache_ttl_seconds | 300 | How long resolved values are reused (in-process and on disk). Set to0to disablebothcache layers — no values are written to disk at all. |
| override_existing | true | When true, resolved values overwrite anything already in env (so rotation takes effect). Flip tofalseto let.env/ shell exports win; those references are then skippedbeforeopis invoked. |

`enabled`
`false`
`op`
`env`
`{}`
`op://vault/item/field`
`op://`
`account`
`""`
`op read --account`
`op`
`service_account_token_env`
`OP_SERVICE_ACCOUNT_TOKEN`
`op`
`OP_SERVICE_ACCOUNT_TOKEN`
`op`
`binary_path`
`""`
`op`
`PATH`
`op`
`PATH`
`cache_ttl_seconds`
`300`
`0`
`override_existing`
`true`
`false`
`.env`
`op`

## Failure modes​

1Password never blocks Hermes startup. If anything goes wrong you'll see a one-line warning in stderr and Hermes continues:

| Symptom | Cause | Fix |
| --- | --- | --- |
| the op CLI was not found on PATH | opnot installed / not on PATH | Install the CLI, or setsecrets.onepassword.binary_path |
| op read failed for 'op://…': … | Locked session, expired token, or no vault access | op signin, refresh the token, or grant the service account access |
| op read returned an empty value for 'op://…' | The referenced field exists but is empty | Fix the item/field in 1Password (an empty value is never applied — your existing env var is left intact) |
| … is not an op:// secret reference | A mapping value isn't anop://reference | Re-set it with the correctop://vault/item/fieldform |
| op read timed out | Network blocked or 1Password slow | Check connectivity / the desktop app integration |

`the op CLI was not found on PATH`
`op`
`secrets.onepassword.binary_path`
`op read failed for 'op://…': …`
`op signin`
`op read returned an empty value for 'op://…'`
`… is not an op:// secret reference`
`op://`
`op://vault/item/field`
`op read timed out`

## Caching​

Successful, complete pulls are cached in-process and on disk under<hermes_home>/cache/op_cache.json(written atomically, mode0600), so back-to-back short-livedhermesinvocations don't re-shellopfor every reference. The cache:

`<hermes_home>/cache/op_cache.json`
`0600`
`hermes`
`op`
- stores only resolved secretvalues— never the service-account token or any raw auth material (auth is fingerprinted into the cache key);
- is invalidated when the token, account,OP_SESSION_*variables, or the set of references change;
- isnotwritten when a pull had any per-reference error, so a transient auth failure isn't frozen in for the TTL;
- is fully disabled — readsandwrites — whencache_ttl_seconds: 0.

`OP_SESSION_*`
`cache_ttl_seconds: 0`

## Security notes​

- A 1Password service-account token can read every secret the account has access to. Store it in~/.hermes/.env(notconfig.yaml), and revoke + regenerate from 1Password if it leaks.
- Hermes refuses to let a resolved value overwrite the token env var itself, even withoverride_existing: true.
- Theopchild process gets a minimal allowlisted environment (auth/session vars +PATH/HOME), not a copy of the fullos.environ, so post-dotenv provider credentials aren't all inherited by the child.
- References are validated to start withop://, and the reference is passed after a--option terminator so a crafted value can't be parsed as anopflag.

`~/.hermes/.env`
`config.yaml`
`override_existing: true`
`op`
`PATH`
`HOME`
`os.environ`
`op://`
`--`
`op`

## When NOT to use this​

- Single-machine personal setupswhere~/.hermes/.envis fine.
- Air-gapped environmentsthat can't reach 1Password.
- CI/CDwhere an existing secrets-injection mechanism is already wired up — pick one path, not two.

`~/.hermes/.env`

The good case for this is multi-machine fleets, shared dev boxes, gateway VPSes, or anywhere you want centralized rotation and revocation across multiple Hermes installations.