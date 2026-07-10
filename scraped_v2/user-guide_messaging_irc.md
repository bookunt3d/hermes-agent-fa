- 
- Messaging Platforms
- Other
- IRC

# IRC

The IRC adapter connects Hermes to any IRC server and relays messages between an IRC channel (or direct messages) and the agent. It speaks the IRC protocol over Python's stdlibasyncio—no external dependencies, no SDK, no daemon. It works with public networks likeLibera.Chatand any self-hosted ircd.

`asyncio`

IRC is plain text: there is no voice, image, file, thread, reaction, typing, or streaming support — replies are sent asPRIVMSGlines, with long messages split to fit the IRC line limit.

`PRIVMSG`

> Runhermes gateway setupand pickIRCfor a guided walk-through.

Runhermes gateway setupand pickIRCfor a guided walk-through.

`hermes gateway setup`

## Prerequisites​

- An IRC server to connect to (e.g.irc.libera.chat)
- A channel to join (e.g.#hermes) — comma-separate to join several
- A nickname for the bot (default:hermes-bot)
- Optional: a registered nick + NickServ password if your network requires identification

`irc.libera.chat`
`#hermes`
`hermes-bot`

## Configure Hermes​

You can configure IRC two ways — environment variables (for a quick env-only setup) or thegatewayblock in~/.hermes/gateway-config.yaml.

`gateway`
`~/.hermes/gateway-config.yaml`

### Option A — gateway-config.yaml​

```
gateway:  platforms:    irc:      enabled: true      extra:        server: irc.libera.chat        port: 6697        nickname: hermes-bot        channel: "#hermes"        use_tls: true        server_password: ""       # optional server password        nickserv_password: ""     # optional NickServ identification        allowed_users: []         # empty = allow all, or list of nicks        max_message_length: 450   # IRC line limit (safe default)
```

### Option B — environment variables​

| Variable | Required | Description |
| --- | --- | --- |
| IRC_SERVER | ✅ | IRC server hostname (e.g.irc.libera.chat) |
| IRC_CHANNEL | ✅ | Channel(s) to join — comma-separate for multiple |
| IRC_NICKNAME | ✅ | Bot nickname (default:hermes-bot) |
| IRC_PORT | — | Server port (default:6697with TLS,6667without) |
| IRC_USE_TLS | — | Use TLS (true/false; defaulttrueon port 6697) |
| IRC_SERVER_PASSWORD | — | Server password for thePASScommand |
| IRC_NICKSERV_PASSWORD | — | NickServ password for automatic IDENTIFY on connect |
| IRC_ALLOWED_USERS | — | Comma-separated nicks allowed to talk to the bot |
| IRC_ALLOW_ALL_USERS | — | Allow anyone in the channel to talk to the bot (dev only) |
| IRC_HOME_CHANNEL | — | Channel for cron / notification delivery (defaults toIRC_CHANNEL) |

`IRC_SERVER`
`irc.libera.chat`
`IRC_CHANNEL`
`IRC_NICKNAME`
`hermes-bot`
`IRC_PORT`
`6697`
`6667`
`IRC_USE_TLS`
`true`
`false`
`true`
`IRC_SERVER_PASSWORD`
`PASS`
`IRC_NICKSERV_PASSWORD`
`IRC_ALLOWED_USERS`
`IRC_ALLOW_ALL_USERS`
`IRC_HOME_CHANNEL`
`IRC_CHANNEL`

## Access control​

By default, only nicks listed inallowed_users(orIRC_ALLOWED_USERS) may talk to the bot. Leave the list emptyandsetIRC_ALLOW_ALL_USERS=trueto let anyone in the channel chat with Hermes — useful for testing, but not recommended on public networks since IRC nicks are not authenticated unless the network enforces NickServ.

`allowed_users`
`IRC_ALLOWED_USERS`
`IRC_ALLOW_ALL_USERS=true`

If your network registers nicks, setIRC_NICKSERV_PASSWORD(ornickserv_password) so the bot identifies to NickServ on connect and keeps its registered nick.

`IRC_NICKSERV_PASSWORD`
`nickserv_password`

## Channels vs. DMs​

- Messages in a joined channel are treated as agroupconversation.
- Private messages to the bot are treated asdirect messages.

Cron jobs and notifications are delivered to thehome channel—IRC_HOME_CHANNELif set, otherwise the firstIRC_CHANNEL.

`IRC_HOME_CHANNEL`
`IRC_CHANNEL`

## Run the gateway​

```
hermes gateway start
```

Check status withhermes gateway status— IRC connection state is reported there, including for env-only setups.

`hermes gateway status`

## Notes​

- Long agent replies are automatically split into multiplePRIVMSGlines to stay within the IRC line limit (max_message_length, default 450 bytes after protocol overhead).
- The adapter acquires a scoped credential lock per server+nick, so two Hermes profiles won't fight over the same IRC identity.

`PRIVMSG`
`max_message_length`