- 
- Guides & Tutorials
- OAuth over SSH / Remote Hosts

# OAuth over SSH / Remote Hosts

Some Hermes providers —Spotifyandremote MCP servers(Linear, Sentry, Atlassian, Asana, Figma, …) — use aloopback redirectOAuth flow. The auth server redirects your browser tohttp://127.0.0.1:<port>/callbackso a tiny HTTP listener started by Hermes can grab the authorization code.

`http://127.0.0.1:<port>/callback`

This works perfectly when Hermes and your browser are on the same machine. It breaks the moment they aren't: your laptop's browser tries to reach127.0.0.1onyour laptop, but the listener is bound to127.0.0.1onthe remote server.

`127.0.0.1`
`127.0.0.1`

The fix is a one-line SSH local-forward. For MCP servers on an interactive terminal, you can often paste the redirect URL back instead (no tunnel).

xAI Grok OAuth (xai-oauth) uses OAuth device code, not a loopback callback — open the printed verification URL in any browser and Hermes polls until approval. No SSH tunnel is required. SeexAI Grok OAuth.

`xai-oauth`

## TL;DR​

```
# On your local machine (laptop), in a separate terminal:ssh -N -L 43827:127.0.0.1:43827 user@remote-host# In your existing SSH session on the remote machine:hermes auth add spotify --no-browser# → Hermes prints an authorize URL. Open it in a browser on your laptop.# → Your browser redirects to 127.0.0.1:43827/callback, the tunnel forwards#   the request to the remote listener, login completes.
```

Hermes prints the exact port it bound to on theWaiting for callback on ...line — copy it from there. Spotify defaults to port43827.

`Waiting for callback on ...`
`43827`

## Which Providers Need This​

| Provider | Loopback port | Tunnel needed? |
| --- | --- | --- |
| Spotify | 43827(default) | Yes, when Hermes is remote |
| MCP servers (auth: oauth) | auto-picked per server | Yes, when Hermes is remote (or paste redirect URL) |
| xai-oauth(Grok SuperGrok) | n/a | No — device code flow |
| anthropic(Claude Pro/Max) | n/a | No — paste-the-code flow |
| openai-codex(ChatGPT Plus/Pro) | n/a | No — device code flow |
| minimax,nous-portal | n/a | No — device code flow |

`43827`
`auth: oauth`
`xai-oauth`
`anthropic`
`openai-codex`
`minimax`
`nous-portal`

If your provider isn't in the table, you don't need a tunnel.

## MCP Servers​

Remote MCP servers (Linear, Sentry, Atlassian, Asana, Figma, etc.) use the same loopback redirect flow. Hermes auto-picks a free port per server and prints the authorize URL when the OAuth flow kicks off — either at startup (when a new server appears inmcp_servers:) or when you runhermes mcp login <server>.

`mcp_servers:`
`hermes mcp login <server>`

You have two ways to complete it from a remote host:

Option 1 — paste the redirect URL back (no setup, works anywhere).On an interactive terminal, Hermes prompts you to paste the redirect URL alongside running the local listener. After approving in your browser, the redirect tohttp://127.0.0.1:<port>/callbackwill show a connection error — that's expected. Copy thefull URL from the browser's address barand paste it at the Hermes prompt:

`http://127.0.0.1:<port>/callback`

```
  MCP OAuth: authorization required.  Open this URL in your browser:    https://mcp.linear.app/authorize?response_type=code&...  Or paste the redirect URL here (or the ?code=...&state=... portion) and press Enter:> https://mcp.linear.app/callback?code=abc123&state=xyz  Got authorization code from paste — completing flow.
```

A bare?code=...&state=...query string is accepted too. This works for any MCP server withauth: oauthand requires no SSH config changes.

`?code=...&state=...`
`auth: oauth`

Option 2 — SSH port forward (same as Spotify).Hermes prints the exact port it bound to in the SSH-session hint. Open a separate terminal on your laptop:

```
ssh -N -L <port>:127.0.0.1:<port> user@remote-host
```

Then open the authorize URL in your browser as normal; the redirect tunnels through and the listener picks it up. Use this when you need the flow to complete unattended (e.g. scripted re-auth where you can't paste interactively).

Pitfall — the 30s config-reload race.If you edit~/.hermes/config.yamlto add an OAuth MCP server from inside a running Hermes session, the CLI auto-reloads MCP connections with a 30s timeout. That's not enough time to complete an interactive OAuth flow, and the reload will give up. Usehermes mcp login <server>from a fresh terminal instead — it has no such cap and waits the full 5 min for you to paste back.

`~/.hermes/config.yaml`
`hermes mcp login <server>`

## Why the listener can't just bind 0.0.0.0​

Spotify and most MCP OAuth servers validate theredirect_uriparameter against an allowlist. Both require the loopback form (http://127.0.0.1:<exact-port>/callback). Binding the listener to0.0.0.0or a different port would cause the auth server to reject the request as a redirect_uri mismatch. The SSH tunnel keeps the loopback URI intact end-to-end.

`redirect_uri`
`http://127.0.0.1:<exact-port>/callback`
`0.0.0.0`

## Step-by-step: single SSH hop​

### 1. Start the tunnel from your local machine​

```
# Spotify (port 43827)ssh -N -L 43827:127.0.0.1:43827 user@remote-host
```

-Nmeans "don't open a remote shell, just hold the tunnel open." Keep this terminal running for the duration of the login.

`-N`

### 2. In a separate SSH session, run the auth command​

```
ssh user@remote-hosthermes auth add spotify --no-browser
```

Hermes detects the SSH session, skips the browser auto-open, and prints an authorize URL plus aWaiting for callback on http://127.0.0.1:<port>/callbackline.

`Waiting for callback on http://127.0.0.1:<port>/callback`

### 3. Open the URL in your local browser​

Copy the authorize URL from the remote terminal and paste it into the browser on your laptop. Approve the consent screen. The auth server redirects tohttp://127.0.0.1:<port>/callback. Your browser hits the tunnel, the request is forwarded to the remote listener, and Hermes printsLogin successful!.

`http://127.0.0.1:<port>/callback`
`Login successful!`

You can tear down the tunnel (Ctrl+C in the first terminal) once you see the success line.

## Step-by-step: through a jump box​

If you reach Hermes through a bastion / jump host, use SSH's built-in-J(ProxyJump):

`-J`

```
ssh -N -L 43827:127.0.0.1:43827 -J jump-user@jump-host user@final-host
```

This chains a SSH connection through the jump host without putting the loopback port on the jump box itself. The local127.0.0.1:43827on your laptop tunnels straight through to127.0.0.1:43827on the final remote host.

`127.0.0.1:43827`
`127.0.0.1:43827`

For older OpenSSH that doesn't support-J, the long form is:

`-J`

```
ssh -N \    -o "ProxyCommand=ssh -W %h:%p jump-user@jump-host" \    -L 43827:127.0.0.1:43827 \    user@final-host
```

## Mosh, tmux, ssh ControlMaster​

The tunnel is a property of the underlying SSH connection. If you're running Hermes insidetmuxover a mosh session, the mosh roaming doesn't carry the-Lforwarding. Open aseparateplain SSH sessiononlyfor the-Ltunnel — that's the connection that has to stay alive during the auth flow. Your interactive mosh/tmux session can keep running Hermes normally.

`tmux`
`-L`
`-L`

If you usessh -o ControlMaster=auto, port forwards on a multiplexed connection share the master's lifetime. Restart the master if the tunnel doesn't come up:

`ssh -o ControlMaster=auto`

```
ssh -O exit user@remote-hostssh -N -L 43827:127.0.0.1:43827 user@remote-host
```

## Troubleshooting​

### bind [127.0.0.1]:43827: Address already in use​

`bind [127.0.0.1]:43827: Address already in use`

Something on your laptop is already using that port. Either the previous tunnel didn't shut down cleanly, or a local Hermes is also listening on it. Find and kill the offender:

```
# macOS / Linuxlsof -iTCP:43827 -sTCP:LISTENkill <PID>
```

Then retry thessh -Lcommand.

`ssh -L`

### Authorization timed out waiting for the local callback​

The redirect never made it back to the remote listener. Check the tunnel is still alive (ssh -Ndoesn't show output, so look at the terminal you started it from), confirm you used the port from the latestWaiting for callback on ...line (Hermes may auto-bump if the preferred port is busy), restart the tunnel if needed, and re-run the auth command.

`ssh -N`
`Waiting for callback on ...`

### Tokens land in the wrong~/.hermes​

`~/.hermes`

The tokens are written under the Linux user that ranhermes auth add .... If your gateway / systemd service runs as a different user (e.g.rootor a dedicatedhermesuser), authenticate asthatuser so the tokens land in their~/.hermes/auth.json.sudo -u hermes -ior equivalent.

`hermes auth add ...`
`root`
`hermes`
`~/.hermes/auth.json`
`sudo -u hermes -i`

## See Also​

- xAI Grok OAuth— device code; no SSH tunnel
- Spotify (Running over SSH)
- Native MCP client (OAuth section)
- SSH-J/ ProxyJump (man page)

`Running over SSH`
`-J`