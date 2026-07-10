---
layout: docs
title: "Features_Spotify"
permalink: /docs/user-guide/features/spotify/
---

- 
- Features
- Media & Web
- Spotify

# Spotify

Hermes can control Spotify directly — playback, queue, search, playlists, saved tracks/albums, and listening history — using Spotify's official Web API with PKCE OAuth. Tokens are stored in~/.hermes/auth.jsonand refreshed automatically on 401; you only log in once per machine (refresh tokens expire after ~6 months; re-runhermes auth spotifywhen they do).

`~/.hermes/auth.json`
`hermes auth spotify`

Unlike Hermes' built-in OAuth integrations (Google, GitHub Copilot, Codex), Spotify requires every user to register their own lightweight developer app. Spotify does not let third parties ship a public OAuth app that anyone can use. It takes about two minutes andhermes auth spotifywalks you through it.

`hermes auth spotify`

## Prerequisites​

- A Spotify account.Freeworks for search, playlist, library, and activity tools.Premiumis required for playback control (play, pause, skip, seek, volume, queue add, transfer).
- Hermes Agent installed and running.
- For playback tools: anactive Spotify Connect device— the Spotify app must be open on at least one device (phone, desktop, web player, speaker) so the Web API has something to control. If nothing is active you'll get a403 Forbiddenwith a "no active device" message; open Spotify on any device and retry.

`403 Forbidden`

## Setup​

### One-shot:hermes toolsor first-run setup​

`hermes tools`

The fastest path. Run:

```
hermes tools
```

Scroll to🎵 Spotify, press space to toggle it on, thensto save. The same toggle is also available during the first-runhermes setup/hermes setup toolsflow. Spotify stays opt-in, so enabling it there runs the same provider-aware configuration ashermes tools.

`🎵 Spotify`
`s`
`hermes setup`
`hermes setup tools`
`hermes tools`

Hermes drops you straight into the OAuth flow — if you don't have a Spotify app yet, it walks you through creating one inline. Once you finish, the toolset is enabled AND authenticated in one pass.

If you prefer to do the steps separately (or you're re-authing later), use the two-step flow below.

### Two-step flow​

#### 1. Enable the toolset​

```
hermes tools
```

Toggle🎵 Spotifyon, save, and when the inline wizard opens, dismiss it (Ctrl+C). The toolset stays on; only the auth step is deferred.

`🎵 Spotify`

#### 2. Run the login wizard​

```
hermes auth spotify
```

The 7 Spotify tools only appear in the agent's toolset after step 1 — they're off by default so users who don't want them don't ship extra tool schemas on every API call.

If noHERMES_SPOTIFY_CLIENT_IDis set, Hermes walks you through the app registration inline:

`HERMES_SPOTIFY_CLIENT_ID`
1. Openshttps://developer.spotify.com/dashboardin your browser
2. Prints the exact values to paste into Spotify's "Create app" form
3. Prompts you for the Client ID you get back
4. Saves it to~/.hermes/.envso future runs skip this step
5. Continues straight into the OAuth consent flow

`https://developer.spotify.com/dashboard`
`~/.hermes/.env`

After you approve, tokens are written underproviders.spotifyin~/.hermes/auth.json. The active inference provider is NOT changed — Spotify auth is independent of your LLM provider.

`providers.spotify`
`~/.hermes/auth.json`

### Creating the Spotify app (what the wizard asks for)​

When the dashboard opens, clickCreate appand fill in:

| Field | Value |
| --- | --- |
| App name | anything (e.g.hermes-agent) |
| App description | anything (e.g.personal Hermes integration) |
| Website | leave blank |
| Redirect URI | http://127.0.0.1:43827/spotify/callback |
| Which API/SDKs? | checkWeb API |

`hermes-agent`
`personal Hermes integration`
`http://127.0.0.1:43827/spotify/callback`

Agree to the terms and clickSave. On the next page clickSettings→ copy theClient IDand paste it into the Hermes prompt. That's the only value Hermes needs — PKCE doesn't use a client secret.

### Running over SSH / in a headless environment​

IfSSH_CLIENTorSSH_TTYis set, Hermes skips the automatic browser open during both the wizard and the OAuth step. Copy the dashboard URL and the authorization URL Hermes prints, open them in a browser on your local machine, and proceed normally — the local HTTP listener still runs on the remote host on port43827. Your laptop's browser can't reach the remote loopback without an SSH local-forward:

`SSH_CLIENT`
`SSH_TTY`
`43827`

```
ssh -N -L 43827:127.0.0.1:43827 user@remote-host
```

For jump-box / bastion setups and other gotchas (mosh, tmux, port conflicts), seeOAuth over SSH / Remote Hosts.

## Verify​

```
hermes auth status spotify
```

Shows whether tokens are present and when the access token expires. Refresh is automatic: when any Spotify API call returns 401, the client exchanges the refresh token and retries once. Refresh tokens persist across Hermes restarts, so you only re-auth if you revoke the app in your Spotify account settings or runhermes auth logout spotify.

`hermes auth logout spotify`

## Using it​

Once logged in, the agent has access to 7 Spotify tools. You talk to the agent naturally — it picks the right tool and action. For the best behavior, the agent loads a companion skill that teaches canonical usage patterns (single-search-then-play, when not to preflightget_state, etc.).

`get_state`

```
> play some miles davis> what am I listening to> add this track to my Late Night Jazz playlist> skip to the next song> make a new playlist called "Focus 2026" and add the last three songs I played> which of my saved albums are by Radiohead> search for acoustic covers of Blackbird> transfer playback to my kitchen speaker
```

### Tool reference​

All playback-mutating actions accept an optionaldevice_idto target a specific device. If omitted, Spotify uses the currently active device.

`device_id`

#### spotify_playback​

`spotify_playback`

Control and inspect playback, plus fetch recently played history.

| Action | Purpose | Premium? |
| --- | --- | --- |
| get_state | Full playback state (track, device, progress, shuffle/repeat) | No |
| get_currently_playing | Just the current track (returns empty on 204 — see below) | No |
| play | Start/resume playback. Optional:context_uri,uris,offset,position_ms | Yes |
| pause | Pause playback | Yes |
| next/previous | Skip track | Yes |
| seek | Jump toposition_ms | Yes |
| set_repeat | state=track/context/off | Yes |
| set_shuffle | state=true/false | Yes |
| set_volume | volume_percent= 0-100 | Yes |
| recently_played | Last played tracks. Optionallimit,before,after(Unix ms) | No |

`get_state`
`get_currently_playing`
`play`
`context_uri`
`uris`
`offset`
`position_ms`
`pause`
`next`
`previous`
`seek`
`position_ms`
`set_repeat`
`state`
`track`
`context`
`off`
`set_shuffle`
`state`
`true`
`false`
`set_volume`
`volume_percent`
`recently_played`
`limit`
`before`
`after`

#### spotify_devices​

`spotify_devices`
| Action | Purpose |
| --- | --- |
| list | Every Spotify Connect device visible to your account |
| transfer | Move playback todevice_id. Optionalplay: truestarts playback on transfer |

`list`
`transfer`
`device_id`
`play: true`

### Home Assistant-managed speakers​

If Home Assistant manages speakers that already support Spotify Connect (for example Sonos, Echo, Nest, or other Connect-capable speakers), they appear inspotify_devices listautomatically whenever Spotify can see them. Hermes does not need a Home Assistant ↔ Spotify bridge for this path — Spotify handles the device routing natively.

`spotify_devices list`

Ask Hermes to transfer playback by the speaker's display name (for example, “transfer Spotify to the kitchen speaker”), or callspotify_devices listand pass the exactdevice_idtospotify_devices transferwhen scripting. If the speaker is missing, open the Spotify app or the speaker's Spotify integration once so Spotify registers it as an active Connect target.

`spotify_devices list`
`device_id`
`spotify_devices transfer`

#### spotify_queue​

`spotify_queue`
| Action | Purpose | Premium? |
| --- | --- | --- |
| get | Currently queued tracks | No |
| add | Appendurito the queue | Yes |

`get`
`add`
`uri`

#### spotify_search​

`spotify_search`

Search the catalog.queryis required. Optional:types(array oftrack/album/artist/playlist/show/episode),limit,offset,market.

`query`
`types`
`track`
`album`
`artist`
`playlist`
`show`
`episode`
`limit`
`offset`
`market`

#### spotify_playlists​

`spotify_playlists`
| Action | Purpose | Required args |
| --- | --- | --- |
| list | User's playlists | — |
| get | One playlist + tracks | playlist_id |
| create | New playlist | name(+ optionaldescription,public,collaborative) |
| add_items | Add tracks | playlist_id,uris(optionalposition) |
| remove_items | Remove tracks | playlist_id,uris(+ optionalsnapshot_id) |
| update_details | Rename / edit | playlist_id+ any ofname,description,public,collaborative |

`list`
`get`
`playlist_id`
`create`
`name`
`description`
`public`
`collaborative`
`add_items`
`playlist_id`
`uris`
`position`
`remove_items`
`playlist_id`
`uris`
`snapshot_id`
`update_details`
`playlist_id`
`name`
`description`
`public`
`collaborative`

#### spotify_albums​

`spotify_albums`
| Action | Purpose | Required args |
| --- | --- | --- |
| get | Album metadata | album_id |
| tracks | Album track list | album_id |

`get`
`album_id`
`tracks`
`album_id`

#### spotify_library​

`spotify_library`

Unified access to saved tracks and saved albums. Pick the collection with thekindarg.

`kind`
| Action | Purpose |
| --- | --- |
| list | Paginated library listing |
| save | Addids/uristo library |
| remove | Removeids/urisfrom library |

`list`
`save`
`ids`
`uris`
`remove`
`ids`
`uris`

Required:kind=tracksoralbums, plusaction.

`kind`
`tracks`
`albums`
`action`

### Feature matrix: Free vs Premium​

Read-only tools work on Free accounts. Anything that mutates playback or the queue requires Premium.

| Works on Free | Premium required |
| --- | --- |
| spotify_search(all) | spotify_playback— play, pause, next, previous, seek, set_repeat, set_shuffle, set_volume |
| spotify_playback— get_state, get_currently_playing, recently_played | spotify_queue— add |
| spotify_devices— list | spotify_devices— transfer |
| spotify_queue— get |  |
| spotify_playlists(all) |  |
| spotify_albums(all) |  |
| spotify_library(all) |  |

`spotify_search`
`spotify_playback`
`spotify_playback`
`spotify_queue`
`spotify_devices`
`spotify_devices`
`spotify_queue`
`spotify_playlists`
`spotify_albums`
`spotify_library`

## Scheduling: Spotify + cron​

Because Spotify tools are regular Hermes tools, a cron job running in a Hermes session can trigger playback on any schedule. No new code needed.

### Morning wake-up playlist​

```
hermes cron add \  --name "morning-commute" \  "0 7 * * 1-5" \  "Transfer playback to my kitchen speaker and start my 'Morning Commute' playlist. Volume to 40. Shuffle on."
```

What happens at 7am every weekday:

1. Cron spins up a headless Hermes session.
2. Agent reads the prompt, callsspotify_devices listto find "kitchen speaker" by name, thenspotify_devices transfer→spotify_playback set_volume→spotify_playback set_shuffle→spotify_search+spotify_playback play.
3. Music starts on the target speaker. Total cost: one session, a few tool calls, no human input.

`spotify_devices list`
`spotify_devices transfer`
`spotify_playback set_volume`
`spotify_playback set_shuffle`
`spotify_search`
`spotify_playback play`

### Wind-down at night​

```
hermes cron add \  --name "wind-down" \  "30 22 * * *" \  "Pause Spotify. Then set volume to 20 so it's quiet when I start it again tomorrow."
```

### Gotchas​

- An active device must exist when the cron fires.If no Spotify client is running (phone/desktop/Connect speaker), playback actions return403 no active device. For morning playlists, the trick is to target a device that's always on (Sonos, Echo, a smart speaker) rather than your phone.
- Premium required for anything that mutates playback— play, pause, skip, volume, transfer. Read-only cron jobs (scheduled "email me my recently played tracks") work fine on Free.
- The cron agent inherits your active toolsets.Spotify must be enabled inhermes toolsfor the cron session to see the Spotify tools.
- Cron jobs run withskip_memory=Trueso they don't write to your memory store.

`403 no active device`
`hermes tools`
`skip_memory=True`

Full cron reference:Cron Jobs.

## Sign out​

```
hermes auth logout spotify
```

Removes tokens from~/.hermes/auth.json. To also clear the app config, deleteHERMES_SPOTIFY_CLIENT_ID(andHERMES_SPOTIFY_REDIRECT_URIif you set it) from~/.hermes/.env, or run the wizard again.

`~/.hermes/auth.json`
`HERMES_SPOTIFY_CLIENT_ID`
`HERMES_SPOTIFY_REDIRECT_URI`
`~/.hermes/.env`

To revoke the app on Spotify's side, visitApps connected to your accountand clickREMOVE ACCESS.

## Troubleshooting​

403 Forbidden — Player command failed: No active device found— You need Spotify running on at least one device. Open the Spotify app on your phone, desktop, or web player, start any track for a second to register it, and retry.spotify_devices listshows what's currently visible.

`403 Forbidden — Player command failed: No active device found`
`spotify_devices list`

403 Forbidden — Premium required— You're on a Free account trying to use a playback-mutating action. See the feature matrix above.

`403 Forbidden — Premium required`

204 No Contentonget_currently_playing— nothing is currently playing on any device. This is Spotify's normal response, not an error; Hermes surfaces it as an explanatory empty result (is_playing: false).

`204 No Content`
`get_currently_playing`
`is_playing: false`

INVALID_CLIENT: Invalid redirect URI— the redirect URI in your Spotify app settings doesn't match what Hermes is using. The default ishttp://127.0.0.1:43827/spotify/callback. Either add that to your app's allowed redirect URIs, or setHERMES_SPOTIFY_REDIRECT_URIin~/.hermes/.envto whatever you registered.

`INVALID_CLIENT: Invalid redirect URI`
`http://127.0.0.1:43827/spotify/callback`
`HERMES_SPOTIFY_REDIRECT_URI`
`~/.hermes/.env`

429 Too Many Requests— Spotify's rate limit. Hermes returns a friendly error; wait a minute and retry. If this persists, you're probably running a tight loop in a script — Spotify's quota resets roughly every 30 seconds.

`429 Too Many Requests`

401 Unauthorizedkeeps coming back— Your refresh token was revoked (usually because you removed the app from your account, or the app was deleted). Runhermes auth spotifyagain.

`401 Unauthorized`
`hermes auth spotify`

Wizard doesn't open the browser— If you're over SSH or in a container without a display, Hermes detects it and skips the auto-open. Copy the dashboard URL it prints and open it manually.

## Advanced: custom scopes​

By default Hermes requests the scopes needed for every shipped tool. Override if you want to restrict access:

```
hermes auth spotify --scope "user-read-playback-state user-modify-playback-state playlist-read-private"
```

Scope reference:Spotify Web API scopes. If you request fewer scopes than a tool needs, that tool's calls will fail with 403.

## Advanced: custom client ID / redirect URI​

```
hermes auth spotify --client-id <id> --redirect-uri http://localhost:3000/callback
```

Or set them permanently in~/.hermes/.env:

`~/.hermes/.env`

```
HERMES_SPOTIFY_CLIENT_ID=<your_id>HERMES_SPOTIFY_REDIRECT_URI=http://localhost:3000/callback
```

The redirect URI must be allow-listed in your Spotify app's settings. The default works for almost everyone — only change it if port 43827 is taken.

## Where things live​

| File | Contents |
| --- | --- |
| ~/.hermes/auth.json→providers.spotify | access token, refresh token, expiry, scope, redirect URI |
| ~/.hermes/.env | HERMES_SPOTIFY_CLIENT_ID, optionalHERMES_SPOTIFY_REDIRECT_URI |
| Spotify app | owned by you atdeveloper.spotify.com/dashboard; contains the Client ID and the redirect URI allow-list |

`~/.hermes/auth.json`
`providers.spotify`
`~/.hermes/.env`
`HERMES_SPOTIFY_CLIENT_ID`
`HERMES_SPOTIFY_REDIRECT_URI`