- 
- Guides & Tutorials
- Run Nemotron 3 Ultra free in Hermes Agent

# Run Nemotron 3 Ultra free in Hermes Agent

Nous Research has been inducted into theNemotron Coalitionof leading AI labs working withNVIDIAto advance open frontier foundation models. In honor of this, we've partnered withNebiusto provideNemotron 3 Ultrafree onNous Portalfor two weeks (June 4th – June 18th). Follow the instructions below to try the model in your Hermes Agent today.

Thenvidia/nemotron-3-ultra:freetier is available fromJune 4th to June 18th. The:freetag is what keeps it on the no-cost plan — pick that exact variant.

`nvidia/nemotron-3-ultra:free`
`:free`

Pick whichever install fits you. Thedesktop appis the easiest — no terminal required. If you live in a terminal, thecommand-lineinstall is right below it.

## Option A — Desktop app (recommended)​

The simplest path: a one-click installer with a guided, point-and-click setup. No terminal needed.

### 1. Download and install​

Download the Hermes Desktop installerfor macOS or Windows, then open it. On first launch it finishes setting itself up (usually under a minute).

### 2. Connect Nous Portal​

When the app opens, you'll see a "Let's get you set up" screen. ClickNous Portal(markedRecommended). Your browser opens — create aNous Portalaccount (or sign in), choose theFreeplan, and authorize Hermes. The app connects automatically.

### 3. Pick the free Nemotron 3 Ultra model​

After connecting, the app shows aDefault modelcard. ClickChange, search fornemotron 3 ultra, and select the variant taggedFree tier:

```
nvidia/nemotron-3-ultra:free
```

The:freetag is what keeps it on the no-cost tier — pick that variant.

`:free`

### 4. Start chatting​

ClickStart chatting. That's it — you're talking to Nemotron 3 Ultra, free.

## Option B — Command line​

Prefer the terminal?

### 1. Install Hermes Agent​

On macOS/Linux/WSL2/Android, run

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

On Windows, run

```
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Prefer to review first? Downloadinstall.sh, inspect it, then run it.

`install.sh`

After it finishes, reload your shell:

```
source ~/.bashrc   # or source ~/.zshrc
```

### 2. Run Quick Setup​

```
hermes setup
```

SelectQuick Setup. Hermes opens a browser tab and waits for you to finish the next steps.

### 3. Create a Nous Portal account​

In the browser, create aNous Portalaccount (or sign in) and choose theFreeplan.

### 4. Connect your account​

When prompted to connect your account to Hermes Agent, clickConnect. You'll see a confirmation once it's linked.

### 5. Select the free Nemotron 3 Ultra model​

Return to your terminal. From the model list, select:

```
nvidia/nemotron-3-ultra:free
```

The:freetag is what keeps it on the no-cost tier, so make sure you pick that variant.

`:free`

### 6. Start chatting​

Complete the remaining Quick Setup prompts, then run:

```
hermes
```

That's it — you're talking to Nemotron 3 Ultra, free.

## Switching to it later​

Already set up with another model?

- Desktop app:open the model picker, search fornemotron 3 ultra, and select theFree tiervariant.
- CLI / TUI:switch any time from inside a session with/model nvidia/nemotron-3-ultra:free, or run/modelto open the picker and choose it from the list.

`/model nvidia/nemotron-3-ultra:free`
`/model`

## Troubleshooting​

- Don't see the model in the list?Make sure you finished the Nous Portal connection and that you're on theFreeplan. In the CLI,hermes portal infoconfirms you're logged in and routing through Nous.
- Picked the wrong variant?Re-selectnvidia/nemotron-3-ultra:free— the:freesuffix is required to stay on the no-cost tier.
- Browser didn't open / you're on a remote host (CLI)?SeeOAuth over SSH / Remote Hostsfor port-forwarding workarounds.

`hermes portal info`
`nvidia/nemotron-3-ultra:free`
`:free`

## See also​

- Desktop App— The native one-click app (macOS, Windows, Linux)
- Run Hermes Agent with Nous Portal— Full Portal walkthrough: models, Tool Gateway, and verification
- Nous Portal integration— What's in the subscription
- Quickstart— Install-to-chat in under 5 minutes