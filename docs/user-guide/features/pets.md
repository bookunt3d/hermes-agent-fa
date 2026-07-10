---
layout: docs
title: "Features_Pets"
permalink: /docs/user-guide/features/pets/
---

- 
- Features
- Media & Web
- Pets (Petdex Mascots)

# Pets

Hermes can show an animatedpet— a small mascot sprite that reacts to what
the agent is doing (idle, running a tool, thinking, finishing, failing) across
theCLI,TUI, anddesktop app. Pets come from the publicpetdexgallery.

Pets are purely cosmetic. They haveno effect on prompt caching, tokens, or
the agent's behavior— the sprite is a display concern only. The feature isoff by defaultand stays dormant until you install and select a pet.

## How it works​

- Pets are installed into your profile'spets/directory
(<HERMES_HOME>/pets/<slug>/), so eachprofilekeeps its
own set.
- Selecting a pet writesdisplay.pet.sluganddisplay.pet.enabledtoconfig.yaml— nothing is stored as a secret or env var.
- Each surface watches the activity it already tracks and maps it to one of six
animation states. The mapping lives in one place so every surface behaves the
same:Agent activityPet stateA tool/turn just failedfailedA plan finished (all todos done)jump(celebrate)A turn finished cleanlywaveA tool is executingrunThe model is thinking/readingreviewTurn in flight (unspecified)runBlocked on you (a clarify/approval prompt is open)waiting(falls back toidleon legacy 8-row sheets)Nothing happeningidle

Pets are installed into your profile'spets/directory
(<HERMES_HOME>/pets/<slug>/), so eachprofilekeeps its
own set.

`pets/`
`<HERMES_HOME>/pets/<slug>/`

Selecting a pet writesdisplay.pet.sluganddisplay.pet.enabledtoconfig.yaml— nothing is stored as a secret or env var.

`display.pet.slug`
`display.pet.enabled`
`config.yaml`

Each surface watches the activity it already tracks and maps it to one of six
animation states. The mapping lives in one place so every surface behaves the
same:

| Agent activity | Pet state |
| --- | --- |
| A tool/turn just failed | failed |
| A plan finished (all todos done) | jump(celebrate) |
| A turn finished cleanly | wave |
| A tool is executing | run |
| The model is thinking/reading | review |
| Turn in flight (unspecified) | run |
| Blocked on you (a clarify/approval prompt is open) | waiting(falls back toidleon legacy 8-row sheets) |
| Nothing happening | idle |

`failed`
`jump`
`wave`
`run`
`review`
`run`
`waiting`
`idle`
`idle`

## Rendering​

In the terminal (CLI/TUI), Hermes renders the sprite at full fidelity when your
terminal supports a graphics protocol (kitty,Ghostty,WezTerm,iTerm2, orsixel). Otherwise it falls back automatically to a truecolor
Unicodehalf-blockrendering. Inside a pipe or redirect (no TTY), terminal
rendering is disabled by design.

The desktop app draws the pet as a floating sprite on a canvas and toggles it
fromSettings → Appearance.

## Quick start (CLI)​

```
# Browse the gallery (filter by substring)hermes pets listhermes pets list cat# Install a pet and make it active in one stephermes pets install boba --select# Preview / animate it in your terminal (Ctrl+C to stop)hermes pets show# Check your setuphermes pets doctor
```

## hermes petscommands​

`hermes pets`
| Goal | Command |
| --- | --- |
| Browse the gallery | hermes pets list [query] [--limit N] |
| List installed pets | hermes pets list --installed |
| Install a pet | hermes pets install <slug> [--select] [--force] |
| Set the active pet | hermes pets select [slug](omit slug for a picker) |
| Resize the pet everywhere | hermes pets scale <factor>(e.g.0.5, clamped 0.1–3.0) |
| Preview/animate | hermes pets show [slug] [--state <s>] [--cycle] [--once] [--mode <m>] [--scale <f>] |
| Disable the pet | hermes pets off |
| Remove an installed pet | hermes pets remove <slug> |
| Diagnose setup | hermes pets doctor |

`hermes pets list [query] [--limit N]`
`hermes pets list --installed`
`hermes pets install <slug> [--select] [--force]`
`hermes pets select [slug]`
`hermes pets scale <factor>`
`0.5`
`hermes pets show [slug] [--state <s>] [--cycle] [--once] [--mode <m>] [--scale <f>]`
`hermes pets off`
`hermes pets remove <slug>`
`hermes pets doctor`

hermes pets showflags:

`hermes pets show`
- --state— play a single state (idle,wave,run,failed,review,jump).
- --cycle— cycle through every state.
- --once— play once instead of looping.
- --mode— override the render protocol (kitty,iterm,sixel,unicode,auto).
- --scale— override the on-screen scale (0= use config).

`--state`
`idle`
`wave`
`run`
`failed`
`review`
`jump`
`--cycle`
`--once`
`--mode`
`kitty`
`iterm`
`sixel`
`unicode`
`auto`
`--scale`
`0`

## /petslash command​

`/pet`

Inside the CLI and TUI you can manage the pet without leaving the session:

- /pet— toggle the pet on/off (adopts the first installed pet if none is
active).
- /pet list— browse the gallery.
- /pet scale <factor>— resize the pet everywhere (e.g./pet scale 0.5).
- /pet <slug>— adopt a specific pet.
- /pet off— disable the pet.

`/pet`
`/pet list`
`/pet scale <factor>`
`/pet scale 0.5`
`/pet <slug>`
`/pet off`

In the TUI,/pet listopens an interactive picker overlay; in the desktop app
it opens the Cmd+K pet palette.

`/pet list`

## Generating a pet (/hatch)​

`/hatch`

Beyond installing pre-made pets from the gallery, Hermes cangenerate a brand-new petfrom a text description — its own AI sprite-generation pipeline.

- CLI/TUI:/hatch <description>(alias/generate-pet), orhermes pets→ the generate flow.
- Desktop app: the Pokédex-stylegenerateUI — an animated egg, hatch FX, and a draft picker.

`/hatch <description>`
`/generate-pet`
`hermes pets`

How generation works (a two-step, cost-bounded flow):

1. Base drafts— a handful of cheap, prompt-only "what should this pet look like" variants are generated. You pick one, or remix/retry for a fresh round.
2. Hatch— the chosen base is used as a reference image to generate one grounded animation row per Hermes state (idle, thinking, tool use, etc.), which are deterministically sliced into frames and packed into a standard petdex/Codex atlas (8×9 grid of 192×208 cells). The result is a valid spritesheet you keep — and couldpetdex submit.

`petdex submit`

### Image backend​

Generation uses the activeimage-generation provider, but it requiresreference-image groundingso each animation row stays the same character as the base. Reference-capable backends:Nous Portal,OpenRouter,OpenAI(gpt-image-2), andKrea. OpenRouter/Nous run a quality-first model chain by default.

`gpt-image-2`
- Resolution order prefers Nous Portal → OpenAI → OpenRouter.
- If no reference-capable backend is configured, generation surfaces an actionable error pointing you tohermes tools→ Image Generation. (Installing/adopting existing gallery pets needs no image backend.)
- Override the backend with theHERMES_PET_IMAGE_PROVIDERenv var (e.g.HERMES_PET_IMAGE_PROVIDER=openrouter).

`hermes tools`
`HERMES_PET_IMAGE_PROVIDER`
`HERMES_PET_IMAGE_PROVIDER=openrouter`

## Desktop app​

In the desktop app you can manage the pet two ways:

- Cmd+K → "Pets…"— browse, search, adopt, and toggle pets without leaving
the keyboard (mirrors the theme picker).
- Settings → Appearance— the same gallery plus asize sliderthat
resizes the floating mascot live as you drag.

Both adopt/toggle/resize the floating mascot in place — size changes apply
instantly; adopting a new pet lights it up within a moment.

### Pop-out overlay​

Shift-clickthe floating pet to pop it out into its own transparent,
always-on-top desktop window. Out there it stays visible while Hermes is
minimized (Codex-style), so a glance tells you what the agent is doing.

Gestures once it's popped out:

| Gesture | Action |
| --- | --- |
| Drag | Move the pet anywhere on screen, even outside the app. Its spot and in/out state persist across restarts. |
| Single-click | Open a mini composer to send a prompt to the most recent session — without surfacing the app. |
| Double-click | Toggle the app window: minimize it if it's up front, restore it if it's hidden. |
| Shift-click | Pop the pet back into the window. |
| Mail icon | Appears only when a turn finished while you were away; click to raise the app on the most recent thread (and mark it read). |

Only the popped-out pet shows aspeech bubble(working…,thinking…,your turn, …) — in-window the app itself is the surface, so the pet stays
quiet there.

`working…`
`thinking…`
`your turn`

The overlay is a pure puppet of the in-app pet — it carries no separate gateway
connection and never appears in the dock or app switcher.

## Configuration​

All settings live underdisplay.petinconfig.yaml:

`display.pet`
`config.yaml`

```
display:  pet:    enabled: false        # master on/off (true once you select a pet)    slug: ""              # active pet; empty = first installed    render_mode: auto      # auto | kitty | iterm | sixel | unicode | off    scale: 0.33           # master size knob (relative to native 192x208 frames)    unicode_cols: 0       # hard override for terminal width (0 = derive from scale)
```

- scaleis the single master size knob. One number shrinks every surface:
the desktop canvas scales its pixels by it, and the CLI/TUI derive their
terminal column width from it. The half-block fallback clamps to a legibility
floor — it can't shrink as far as true-pixel kitty/GUI rendering without
turning to mush, so the samescalelooks crisp under kitty but is floored in
half-blocks.
- render_mode: autodetects kitty/iTerm2/sixel and falls back to unicode
half-blocks. Set it explicitly to force a protocol oroffto disable
terminal rendering while keeping the pet on the desktop.
- unicode_colspins the terminal column width independently ofscale;
leave it at0to derive width fromscale.

`scale`
`scale`
`render_mode: auto`
`off`
`unicode_cols`
`scale`
`0`
`scale`

## Troubleshooting​

Runhermes pets doctor— it reports:

`hermes pets doctor`
- the pets directory and which pets are installed,
- display.pet.enabled,display.pet.slug, and the resolved active pet,
- the configuredrender_mode, the detected terminal graphics protocol, and the
effective mode for a TTY,
- whether Pillow (used for sprite decoding) is importable.

`display.pet.enabled`
`display.pet.slug`
`render_mode`

It prints✓ readyonce a pet is installed, selected, enabled, and Pillow is
available.

`✓ ready`

Common gotchas:

- A pet only shows once one isinstalled AND selected(enabled: true).
- Inside a pipe/redirect (no TTY), terminal rendering is disabled by design.
- The petdex npm CLI installs to~/.codex/pets; Hermes uses its own
profile-scoped<HERMES_HOME>/pets/instead — install throughhermes pets.

`enabled: true`
`~/.codex/pets`
`<HERMES_HOME>/pets/`
`hermes pets`

## See also​

- Thepetdexskilllets the agent install and switch pets for you on request.

`petdex`