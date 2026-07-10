---
layout: docs
title: "Features_Extending The Dashboard"
permalink: /docs/user-guide/features/extending-the-dashboard/
---

- 
- Features
- Management
- Extending the Dashboard

# Extending the Dashboard

The Hermes web dashboard (hermes dashboard) is built to be reskinned and extended without forking the codebase. Three layers are exposed:

`hermes dashboard`
1. Themes— YAML files that repaint the dashboard's palette, typography, layout, and per-component chrome. Drop a file in~/.hermes/dashboard-themes/; it appears in the theme switcher.
2. UI plugins— a directory withmanifest.json+ a JavaScript bundle that registers a tab, replaces a built-in page, augments one via page-scoped slots, or injects components into named shell slots.
3. Backend plugins— a Python file inside that plugin directory that exposes a FastAPIrouter; routes are mounted under/api/plugins/<name>/and called from the plugin's UI.

`~/.hermes/dashboard-themes/`
`manifest.json`
`router`
`/api/plugins/<name>/`

All three aredrop-in at runtime: no repo clone, nonpm run build, no patching the dashboard source. This page is the canonical reference for all three.

`npm run build`

If you just want to use the dashboard, seeWeb Dashboard. If you want to reskin the terminal CLI (not the web dashboard), seeSkins & Themes— the CLI skin system is unrelated to dashboard themes.

Themes and plugins are independent but synergistic. A theme can stand alone (just a YAML file). A plugin can stand alone (just a tab). Together they let you build a complete visual reskin with custom HUDs — the examplestrike-freedom-cockpitdemo (lives in thehermes-example-pluginscompanion repo — seeCombined theme + plugin demofor install steps) does exactly that.

`strike-freedom-cockpit`
`hermes-example-plugins`

## Table of contents​

- ThemesQuick start — your first themePalette, typography, layoutLayout variantsTheme assets (images as CSS vars)Component chrome overridesColor overridesRawcustomCSSBuilt-in themesFull theme YAML reference
- PluginsQuick start — your first pluginDirectory layoutManifest referenceThe Plugin SDKShell slotsReplacing built-in pages (tab.override)Augmenting built-in pages (page-scoped slots)Slot-only plugins (tab.hidden)Backend API routesCustom CSS per pluginPlugin discovery & reload
- Combined theme + plugin demo
- API reference
- Troubleshooting

- Quick start — your first theme
- Palette, typography, layout
- Layout variants
- Theme assets (images as CSS vars)
- Component chrome overrides
- Color overrides
- RawcustomCSS
- Built-in themes
- Full theme YAML reference

`customCSS`
- Quick start — your first plugin
- Directory layout
- Manifest reference
- The Plugin SDK
- Shell slots
- Replacing built-in pages (tab.override)
- Augmenting built-in pages (page-scoped slots)
- Slot-only plugins (tab.hidden)
- Backend API routes
- Custom CSS per plugin
- Plugin discovery & reload

`tab.override`
`tab.hidden`

## Themes​

Themes are YAML files stored in~/.hermes/dashboard-themes/. The file name doesn't matter (the theme'sname:field is what the system uses), but convention is<name>.yaml. Every field is optional — missing keys fall back to the built-indefaulttheme, so a theme can be as small as one color.

`~/.hermes/dashboard-themes/`
`name:`
`<name>.yaml`
`default`

### Quick start — your first theme​

```
mkdir -p ~/.hermes/dashboard-themes
```

```
# ~/.hermes/dashboard-themes/neon.yamlname: neonlabel: Neondescription: Pure magenta on blackpalette:  background: "#000000"  midground: "#ff00ff"
```

Refresh the dashboard. Click the palette icon in the header and pickNeon. The background goes black, text and accents go magenta, and every derived color (card, border, muted, ring, etc.) is recomputed from that 2-color triplet viacolor-mix()in CSS.

`color-mix()`

That's the whole onboarding: one file, two colors. Everything below is optional refinement.

### Palette, typography, layout​

These three blocks are the heart of a theme. Each is independent — override one, leave the others.

#### Palette (3-layer)​

The palette is a triplet of color layers plus a warm-glow vignette color and a noise-grain multiplier. The dashboard's design-system cascade derives every shadcn-compatible token (card, popover, muted, border, primary, destructive, ring, etc.) from this triplet via CSScolor-mix(). Overriding three colors cascades into the whole UI.

`color-mix()`
| Key | Description |
| --- | --- |
| palette.background | Deepest canvas color — typically near-black. Drives the page background and card fill. |
| palette.midground | Primary text and accent. Most UI chrome reads this (foreground text, button outlines, focus rings). |
| palette.foreground | Top-layer highlight. The default theme sets this to white at alpha 0 (invisible); themes that want a bright accent on top can raise its alpha. |
| palette.warmGlow | rgba(...)string used as the vignette color by<Backdrop />. |
| palette.noiseOpacity | 0–1.2 multiplier on the grain overlay. Lower = softer, higher = grittier. |

`palette.background`
`palette.midground`
`palette.foreground`
`palette.warmGlow`
`rgba(...)`
`<Backdrop />`
`palette.noiseOpacity`

Each layer accepts either{hex: "#RRGGBB", alpha: 0.0–1.0}or a bare hex string (alpha defaults to 1.0).

`{hex: "#RRGGBB", alpha: 0.0–1.0}`

```
palette:  background:    hex: "#05091a"    alpha: 1.0  midground: "#d8f0ff"          # bare hex, alpha = 1.0  foreground:    hex: "#ffffff"    alpha: 0                    # invisible top layer  warmGlow: "rgba(255, 199, 55, 0.24)"  noiseOpacity: 0.7
```

#### Typography​

| Key | Type | Description |
| --- | --- | --- |
| fontSans | string | CSS font-family stack for body copy (applied tohtml,body). |
| fontMono | string | CSS font-family stack for code blocks,<code>,.font-monoutilities. |
| fontDisplay | string | Optional heading/display stack. Falls back tofontSans. |
| fontUrl | string | Optional external stylesheet URL. Injected as<link rel="stylesheet">in<head>on theme switch. Same URL is never injected twice. Works with Google Fonts, Bunny Fonts, self-hosted@font-facesheets — anything linkable. |
| baseSize | string | Root font size — controls the rem scale. E.g."14px","16px". |
| lineHeight | string | Default line-height. E.g."1.5","1.65". |
| letterSpacing | string | Default letter-spacing. E.g."0","0.01em","-0.01em". |

`fontSans`
`html`
`body`
`fontMono`
`<code>`
`.font-mono`
`fontDisplay`
`fontSans`
`fontUrl`
`<link rel="stylesheet">`
`<head>`
`@font-face`
`baseSize`
`"14px"`
`"16px"`
`lineHeight`
`"1.5"`
`"1.65"`
`letterSpacing`
`"0"`
`"0.01em"`
`"-0.01em"`

```
typography:  fontSans: '"Orbitron", "Eurostile", "Impact", sans-serif'  fontMono: '"Share Tech Mono", ui-monospace, monospace'  fontDisplay: '"Orbitron", "Eurostile", sans-serif'  fontUrl: "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Share+Tech+Mono&display=swap"  baseSize: "14px"  lineHeight: "1.5"  letterSpacing: "0.04em"
```

##### Changing the font from the UI (no YAML)​

The theme picker in the dashboard header has aFontsection below the
theme list. Pick any font there and it overrides the body font of whatever
theme is active — the choice is independent of the theme and persists across
theme switches (stored inconfig.yamlunderdashboard.font). ChooseTheme defaultto clear the override and fall back to the active theme's
ownfontSans.

`config.yaml`
`dashboard.font`
`fontSans`

The picker offers a curated catalog (system stacks plus a set of Google-Fonts
families across sans / serif / mono). It deliberately doesnotaccept a
free-text font URL — the font's stylesheet is injected as a<link>, so the
catalog keeps the injected origins fixed. For a fully custom face, setfontSans+fontUrlin a theme YAML as shown above. The theme'sfontMono(code blocks, terminal) is always left untouched by the UI override.

`<link>`
`fontSans`
`fontUrl`
`fontMono`

#### Layout​

| Key | Values | Description |
| --- | --- | --- |
| radius | any CSS length ("0","0.25rem","0.5rem","1rem", ...) | Corner-radius token. Maps to--radiusand cascades into--radius-sm/md/lg/xl— every rounded element shifts together. |
| density | compact|comfortable|spacious | Spacing multiplier applied as the--spacing-mulCSS var.compact = 0.85×,comfortable = 1.0×(default),spacious = 1.2×. Scales Tailwind's base spacing, so padding, gap, and space-between utilities all shift proportionally. |

`radius`
`"0"`
`"0.25rem"`
`"0.5rem"`
`"1rem"`
`--radius`
`--radius-sm/md/lg/xl`
`density`
`compact`
`comfortable`
`spacious`
`--spacing-mul`
`compact = 0.85×`
`comfortable = 1.0×`
`spacious = 1.2×`

```
layout:  radius: "0"  density: compact
```

### Layout variants​

layoutVariantpicks the overall shell layout. Defaults to"standard"when absent.

`layoutVariant`
`"standard"`
| Variant | Behaviour |
| --- | --- |
| standard | Single column, 1600px max-width (default). |
| cockpit | Left sidebar rail (260px) + main content. Populated by plugins via thesidebarslot — seeShell slots. Without a plugin the rail shows a placeholder. |
| tiled | Drops the max-width clamp so pages can use the full viewport width. |

`standard`
`cockpit`
`sidebar`
`tiled`

```
layoutVariant: cockpit
```

The current variant is exposed asdocument.documentElement.dataset.layoutVariant, so raw CSS incustomCSScan target it via:root[data-layout-variant="cockpit"] ....

`document.documentElement.dataset.layoutVariant`
`customCSS`
`:root[data-layout-variant="cockpit"] ...`

### Theme assets (images as CSS vars)​

Ship artwork URLs with a theme. Each named slot becomes a CSS var (--theme-asset-<name>) that the built-in shell and any plugin can read. Thebgslot is automatically wired into the backdrop; other slots are plugin-facing.

`--theme-asset-<name>`
`bg`

```
assets:  bg: "https://example.com/hero-bg.jpg"           # auto-wired into <Backdrop />  hero: "/my-images/strike-freedom.png"           # for plugin sidebars  crest: "/my-images/crest.svg"                   # for header-left plugins  logo: "/my-images/logo.png"  sidebar: "/my-images/rail.png"  header: "/my-images/header-art.png"  custom:    scanLines: "/my-images/scanlines.png"         # → --theme-asset-custom-scanLines
```

Values accept:

- Bare URLs — wrapped inurl(...)automatically.
- Pre-wrappedurl(...),linear-gradient(...),radial-gradient(...)expressions — used as-is.
- "none"— explicit opt-out.

`url(...)`
`url(...)`
`linear-gradient(...)`
`radial-gradient(...)`
`"none"`

Every asset is also emitted as--theme-asset-<name>-raw(the unwrapped URL), in case a plugin needs to pass it to<img src>instead ofbackground-image.

`--theme-asset-<name>-raw`
`<img src>`
`background-image`

Plugins read these with plain CSS or JS:

```
// In a plugin slotconst hero = getComputedStyle(document.documentElement)  .getPropertyValue("--theme-asset-hero").trim();
```

### Component chrome overrides​

componentStylesrestyles individual shell components without writing CSS selectors. Each bucket's entries become CSS vars (--component-<bucket>-<kebab-property>) that the shell's shared components read. Socard:overrides apply to every<Card>,header:to the app bar, etc.

`componentStyles`
`--component-<bucket>-<kebab-property>`
`card:`
`<Card>`
`header:`

```
componentStyles:  card:    clipPath: "polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px)"    background: "linear-gradient(180deg, rgba(10, 22, 52, 0.85), rgba(5, 9, 26, 0.92))"    boxShadow: "inset 0 0 0 1px rgba(64, 200, 255, 0.28)"  header:    background: "linear-gradient(180deg, rgba(16, 32, 72, 0.95), rgba(5, 9, 26, 0.9))"  tab:    clipPath: "polygon(6px 0, 100% 0, calc(100% - 6px) 100%, 0 100%)"  sidebar: {}  backdrop: {}  footer: {}  progress: {}  badge: {}  page: {}
```

Supported buckets:card,header,footer,sidebar,tab,progress,badge,backdrop,page.

`card`
`header`
`footer`
`sidebar`
`tab`
`progress`
`badge`
`backdrop`
`page`

Property names use camelCase (clipPath) and are emitted as kebab (clip-path). Values are plain CSS strings — anything CSS accepts (clip-path,border-image,background,box-shadow,animation, ...).

`clipPath`
`clip-path`
`clip-path`
`border-image`
`background`
`box-shadow`
`animation`

### Color overrides​

Most themes won't need this — the 3-layer palette derives every shadcn token. UsecolorOverrideswhen you want a specific accent the derivation won't produce (a softer destructive red for a pastel theme, a specific success green for a brand).

`colorOverrides`

```
colorOverrides:  primary: "#ffce3a"  primaryForeground: "#05091a"  accent: "#3fd3ff"  ring: "#3fd3ff"  destructive: "#ff3a5e"  border: "rgba(64, 200, 255, 0.28)"
```

Supported keys:card,cardForeground,popover,popoverForeground,primary,primaryForeground,secondary,secondaryForeground,muted,mutedForeground,accent,accentForeground,destructive,destructiveForeground,success,warning,border,input,ring.

`card`
`cardForeground`
`popover`
`popoverForeground`
`primary`
`primaryForeground`
`secondary`
`secondaryForeground`
`muted`
`mutedForeground`
`accent`
`accentForeground`
`destructive`
`destructiveForeground`
`success`
`warning`
`border`
`input`
`ring`

Each key maps 1:1 to the--color-<kebab>CSS var (e.g.primaryForeground→--color-primary-foreground). Any key set here wins over the palette cascade for the active theme only — switching to another theme clears the overrides.

`--color-<kebab>`
`primaryForeground`
`--color-primary-foreground`

### RawcustomCSS​

`customCSS`

For selector-level chrome thatcomponentStylescan't express — pseudo-elements, animations, media queries, theme-scoped overrides — drop raw CSS intocustomCSS:

`componentStyles`
`customCSS`

```
customCSS: |  /* Scanline overlay — only visible when cockpit variant is active. */  :root[data-layout-variant="cockpit"] body::before {    content: "";    position: fixed;    inset: 0;    pointer-events: none;    z-index: 100;    background: repeating-linear-gradient(to bottom,      transparent 0px, transparent 2px,      rgba(64, 200, 255, 0.035) 3px, rgba(64, 200, 255, 0.035) 4px);    mix-blend-mode: screen;  }
```

The CSS is injected as a single scoped<style data-hermes-theme-css>tag on theme apply and cleaned up on theme switch.Capped at 32 KiB per theme.

`<style data-hermes-theme-css>`

### Built-in themes​

Each built-in ships its own palette, typography, and layout — switching produces visible changes beyond color alone.

| Theme | Palette | Typography | Layout |
| --- | --- | --- | --- |
| Hermes Teal(default) | Dark teal + cream | System stack, 15px | 0.5rem radius, comfortable |
| Hermes Teal (Large)(default-large) | Same as default | System stack, 18px, line-height 1.65 | 0.5rem radius, spacious |
| Midnight(midnight) | Deep blue-violet | Inter + JetBrains Mono, 14px | 0.75rem radius, comfortable |
| Ember(ember) | Warm crimson + bronze | Spectral (serif) + IBM Plex Mono, 15px | 0.25rem radius, comfortable |
| Mono(mono) | Grayscale | IBM Plex Sans + IBM Plex Mono, 13px | 0 radius, compact |
| Cyberpunk(cyberpunk) | Neon green on black | Share Tech Mono everywhere, 14px | 0 radius, compact |
| Rosé(rose) | Pink + ivory | Fraunces (serif) + DM Mono, 16px | 1rem radius, spacious |

`default`
`default-large`
`midnight`
`ember`
`mono`
`cyberpunk`
`rose`

Themes that reference Google Fonts (all except Hermes Teal) load the stylesheet on demand — the first time you switch to them a<link>tag is injected into<head>.

`<link>`
`<head>`

### Full theme YAML reference​

Every knob in one file — copy and trim what you don't need:

```
# ~/.hermes/dashboard-themes/ocean.yamlname: oceanlabel: Ocean Deepdescription: Deep sea blues with coral accents# 3-layer palette (accepts {hex, alpha} or bare hex)palette:  background:    hex: "#0a1628"    alpha: 1.0  midground:    hex: "#a8d0ff"    alpha: 1.0  foreground:    hex: "#ffffff"    alpha: 0.0  warmGlow: "rgba(255, 107, 107, 0.35)"  noiseOpacity: 0.7typography:  fontSans: "Poppins, system-ui, sans-serif"  fontMono: "Fira Code, ui-monospace, monospace"  fontDisplay: "Poppins, system-ui, sans-serif"   # optional  fontUrl: "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap"  baseSize: "15px"  lineHeight: "1.6"  letterSpacing: "-0.003em"layout:  radius: "0.75rem"  density: comfortablelayoutVariant: standard        # standard | cockpit | tiledassets:  bg: "https://example.com/ocean-bg.jpg"  hero: "/my-images/kraken.png"  crest: "/my-images/anchor.svg"  logo: "/my-images/logo.png"  custom:    pattern: "/my-images/waves.svg"componentStyles:  card:    boxShadow: "inset 0 0 0 1px rgba(168, 208, 255, 0.18)"  header:    background: "linear-gradient(180deg, rgba(10, 22, 40, 0.95), rgba(5, 9, 26, 0.9))"colorOverrides:  destructive: "#ff6b6b"  ring: "#ff6b6b"customCSS: |  /* Any additional selector-level tweaks */
```

Refresh the dashboard after creating the file. Switch themes live from the header bar — click the palette icon. Selection persists toconfig.yamlunderdashboard.themeand is restored on reload.

`config.yaml`
`dashboard.theme`

## Plugins​

A dashboard plugin is a directory with amanifest.json, a pre-built JS bundle, and optionally a CSS file and a Python file with FastAPI routes. Plugins live next to other Hermes plugins in~/.hermes/plugins/<name>/— the dashboard extension is adashboard/subfolder inside that plugin directory, so one plugin can extend both the CLI/gateway and the dashboard from a single install.

`manifest.json`
`~/.hermes/plugins/<name>/`
`dashboard/`

Plugins don't bundle React or UI components. They use thePlugin SDKexposed onwindow.__HERMES_PLUGIN_SDK__. This keeps plugin bundles tiny (typically a few KB) and avoids version conflicts.

`window.__HERMES_PLUGIN_SDK__`

### Quick start — your first plugin​

Create the directory structure:

```
mkdir -p ~/.hermes/plugins/my-plugin/dashboard/dist
```

Write the manifest:

```
// ~/.hermes/plugins/my-plugin/dashboard/manifest.json{  "name": "my-plugin",  "label": "My Plugin",  "icon": "Sparkles",  "version": "1.0.0",  "tab": {    "path": "/my-plugin",    "position": "after:skills"  },  "entry": "dist/index.js"}
```

Write the JS bundle (a plain IIFE — no build step needed):

```
// ~/.hermes/plugins/my-plugin/dashboard/dist/index.js(function () {  "use strict";  const SDK = window.__HERMES_PLUGIN_SDK__;  const { React } = SDK;  const { Card, CardHeader, CardTitle, CardContent } = SDK.components;  function MyPage() {    return React.createElement(Card, null,      React.createElement(CardHeader, null,        React.createElement(CardTitle, null, "My Plugin"),      ),      React.createElement(CardContent, null,        React.createElement("p", { className: "text-sm text-muted-foreground" },          "Hello from my custom dashboard tab.",        ),      ),    );  }  window.__HERMES_PLUGINS__.register("my-plugin", MyPage);})();
```

Refresh the dashboard — your tab appears in the nav bar, afterSkills.

If you prefer JSX, use any bundler (esbuild, Vite, rollup) with React as an external and IIFE output. The only hard requirement is that the final file is a single JS file loadable via<script>. React is never bundled; it comes fromSDK.React.

`<script>`
`SDK.React`

### Directory layout​

```
~/.hermes/plugins/my-plugin/├── plugin.yaml              # optional — existing CLI/gateway plugin manifest├── __init__.py              # optional — existing CLI/gateway hooks└── dashboard/               # dashboard extension    ├── manifest.json        # required — tab config, icon, entry point    ├── dist/    │   ├── index.js         # required — pre-built JS bundle (IIFE)    │   └── style.css        # optional — custom CSS    └── plugin_api.py        # optional — backend API routes (FastAPI)
```

A single plugin directory can carry three orthogonal extensions:

- plugin.yaml+__init__.py— CLI/gateway plugin (see plugins page).
- dashboard/manifest.json+dashboard/dist/index.js— dashboard UI plugin.
- dashboard/plugin_api.py— dashboard backend routes.

`plugin.yaml`
`__init__.py`
`dashboard/manifest.json`
`dashboard/dist/index.js`
`dashboard/plugin_api.py`

None of them are required; include only the layers you need.

### Manifest reference​

```
{  "name": "my-plugin",  "label": "My Plugin",  "description": "What this plugin does",  "icon": "Sparkles",  "version": "1.0.0",  "tab": {    "path": "/my-plugin",    "position": "after:skills",    "override": "/",    "hidden": false  },  "slots": ["sidebar", "header-left"],  "entry": "dist/index.js",  "css": "dist/style.css",  "api": "plugin_api.py"}
```

| Field | Required | Description |
| --- | --- | --- |
| name | Yes | Unique plugin identifier. Lowercase, hyphens ok. Used in URLs and registration. |
| label | Yes | Display name shown in the nav tab. |
| description | No | Short description (shown in dashboard admin surfaces). |
| icon | No | Lucide icon name. Defaults toPuzzle. Unknown names fall back toPuzzle. |
| version | No | Semver string. Defaults to0.0.0. |
| tab.path | Yes | URL path for the tab (e.g./my-plugin). |
| tab.position | No | Where to insert the tab."end"(default),"after:<path>", or"before:<path>"— value after the colon is thepath segmentof the target tab (no leading slash). Examples:"after:skills","before:config". |
| tab.override | No | Set to a built-in route path ("/","/sessions","/config", ...) toreplacethat page instead of adding a new tab. SeeReplacing built-in pages. |
| tab.hidden | No | When true, register the component and any slots without adding a tab to the nav. Used by slot-only plugins. SeeSlot-only plugins. |
| slots | No | Named shell slots this plugin populates.Documentation aid only— actual registration happens from the JS bundle viaregisterSlot(). Listing slots here makes discovery surfaces more informative. |
| entry | Yes | Path to the JS bundle relative todashboard/. Defaults todist/index.js. |
| css | No | Path to a CSS file to inject as a<link>tag. |
| api | No | Path to a Python file with FastAPI routes. Mounted at/api/plugins/<name>/. |

`name`
`label`
`description`
`icon`
`Puzzle`
`Puzzle`
`version`
`0.0.0`
`tab.path`
`/my-plugin`
`tab.position`
`"end"`
`"after:<path>"`
`"before:<path>"`
`"after:skills"`
`"before:config"`
`tab.override`
`"/"`
`"/sessions"`
`"/config"`
`tab.hidden`
`slots`
`registerSlot()`
`entry`
`dashboard/`
`dist/index.js`
`css`
`<link>`
`api`
`/api/plugins/<name>/`

#### Available icons​

Plugins use Lucide icon names. The dashboard maps these by name — unknown names silently fall back toPuzzle.

`Puzzle`

Currently mapped:Activity,BarChart3,Clock,Code,Database,Eye,FileText,Globe,Heart,KeyRound,MessageSquare,Package,Puzzle,Settings,Shield,Sparkles,Star,Terminal,Wrench,Zap.

`Activity`
`BarChart3`
`Clock`
`Code`
`Database`
`Eye`
`FileText`
`Globe`
`Heart`
`KeyRound`
`MessageSquare`
`Package`
`Puzzle`
`Settings`
`Shield`
`Sparkles`
`Star`
`Terminal`
`Wrench`
`Zap`

Need a different icon? Open a PR toweb/src/App.tsx'sICON_MAP— pure additive change.

`web/src/App.tsx`
`ICON_MAP`

### The Plugin SDK​

Everything a plugin needs is onwindow.__HERMES_PLUGIN_SDK__. Plugins should never import React directly.

`window.__HERMES_PLUGIN_SDK__`

```
const SDK = window.__HERMES_PLUGIN_SDK__;// React + hooksSDK.React                    // the React instanceSDK.hooks.useStateSDK.hooks.useEffectSDK.hooks.useCallbackSDK.hooks.useMemoSDK.hooks.useRefSDK.hooks.useContextSDK.hooks.createContext// UI components (shadcn/ui primitives)SDK.components.CardSDK.components.CardHeaderSDK.components.CardTitleSDK.components.CardContentSDK.components.BadgeSDK.components.ButtonSDK.components.InputSDK.components.LabelSDK.components.SelectSDK.components.SelectOptionSDK.components.SeparatorSDK.components.TabsSDK.components.TabsListSDK.components.TabsTriggerSDK.components.PluginSlot    // render a named slot (useful for nested plugin UIs)// Hermes API client + raw fetcherSDK.api                      // typed client — getStatus, getSessions, getConfig, ...SDK.fetchJSON                // raw fetch for custom endpoints (plugin-registered routes)// UtilitiesSDK.utils.cn                 // Tailwind class merger (clsx + twMerge)SDK.utils.timeAgo            // "5m ago" from unix timestampSDK.utils.isoTimeAgo         // "5m ago" from ISO string// HooksSDK.useI18n                  // i18n hook for multi-language plugins
```

#### Calling your plugin's backend​

```
SDK.fetchJSON("/api/plugins/my-plugin/data")  .then((data) => console.log(data))  .catch((err) => console.error("API call failed:", err));
```

fetchJSONinjects the session auth token, surfaces errors as thrown exceptions, and parses JSON automatically.

`fetchJSON`

#### Calling built-in Hermes endpoints​

```
// Agent statusSDK.api.getStatus().then((s) => console.log("Version:", s.version));// Recent sessionsSDK.api.getSessions(10).then((resp) => console.log(resp.sessions.length));
```

SeeWeb Dashboard → REST APIfor the full list.

### Shell slots​

Slots let a plugin inject components into named locations of the app shell — the cockpit sidebar, the header, the footer, an overlay layer — without claiming a whole tab. Multiple plugins can populate the same slot; they render stacked in registration order.

Register from inside the plugin bundle:

```
window.__HERMES_PLUGINS__.registerSlot("my-plugin", "sidebar", MySidebar);window.__HERMES_PLUGINS__.registerSlot("my-plugin", "header-left", MyCrest);
```

#### Slot catalogue​

Shell-wide slots(render anywhere in the app chrome):

| Slot | Location |
| --- | --- |
| backdrop | Inside the<Backdrop />layer stack, above the noise layer. |
| header-left | Before the Hermes brand in the top bar. |
| header-right | Before the theme/language switchers in the top bar. |
| header-banner | Full-width strip below the nav. |
| sidebar | Cockpit sidebar rail —only rendered whenlayoutVariant === "cockpit". |
| pre-main | Above the route outlet (inside<main>). |
| post-main | Below the route outlet (inside<main>). |
| footer-left | Footer cell content (replaces default). |
| footer-right | Footer cell content (replaces default). |
| overlay | Fixed-position layer above everything else. Useful for chrome (scanlines, vignettes)customCSScan't achieve alone. |

`backdrop`
`<Backdrop />`
`header-left`
`header-right`
`header-banner`
`sidebar`
`layoutVariant === "cockpit"`
`pre-main`
`<main>`
`post-main`
`<main>`
`footer-left`
`footer-right`
`overlay`
`customCSS`

Page-scoped slots(render only on the named built-in page — use these to inject widgets, cards, or toolbars into an existing page without overriding the whole route):

| Slot | Where it renders |
| --- | --- |
| sessions:top/sessions:bottom | Top / bottom of the/sessionspage. |
| analytics:top/analytics:bottom | Top / bottom of the/analyticspage. |
| logs:top/logs:bottom | Top (above filter toolbar) / bottom (below log viewer) of/logs. |
| cron:top/cron:bottom | Top / bottom of the/cronpage. |
| skills:top/skills:bottom | Top / bottom of the/skillspage. |
| config:top/config:bottom | Top / bottom of the/configpage. |
| env:top/env:bottom | Top / bottom of the/env(Keys) page. |
| docs:top/docs:bottom | Top (above the iframe) / bottom of/docs. |
| chat:top/chat:bottom | Top / bottom of/chat(only active when embedded chat is enabled). |

`sessions:top`
`sessions:bottom`
`/sessions`
`analytics:top`
`analytics:bottom`
`/analytics`
`logs:top`
`logs:bottom`
`/logs`
`cron:top`
`cron:bottom`
`/cron`
`skills:top`
`skills:bottom`
`/skills`
`config:top`
`config:bottom`
`/config`
`env:top`
`env:bottom`
`/env`
`docs:top`
`docs:bottom`
`/docs`
`chat:top`
`chat:bottom`
`/chat`

Example — add a banner card to the top of the Sessions page:

```
function PinnedSessionsBanner() {  return React.createElement(Card, null,    React.createElement(CardContent, { className: "py-2 text-xs" },      "Pinned note injected by my-plugin"),  );}window.__HERMES_PLUGINS__.registerSlot("my-plugin", "sessions:top", PinnedSessionsBanner);
```

Combine page-scoped slots withtab.hidden: trueif your plugin only augments existing pages and doesn't need a sidebar tab of its own.

`tab.hidden: true`

The shell only renders<PluginSlot name="..." />for the slots above. Additional names are accepted by the registry for nested plugin UIs — a plugin can expose its own slots viaSDK.components.PluginSlot.

`<PluginSlot name="..." />`
`SDK.components.PluginSlot`

#### Re-registration and HMR​

If the same(plugin, slot)pair is registered twice, the later call replaces the earlier one — this matches how React HMR expects plugin re-mounts to behave.

`(plugin, slot)`

### Replacing built-in pages (tab.override)​

`tab.override`

Settingtab.overrideto a built-in route path makes the plugin's component replace that page instead of adding a new tab. Useful when a theme wants a custom home page (/) but wants to keep the rest of the dashboard intact.

`tab.override`
`/`

```
{  "name": "my-home",  "label": "Home",  "tab": {    "path": "/my-home",    "override": "/",    "position": "end"  },  "entry": "dist/index.js"}
```

Withoverrideset:

`override`
- The original page component at/is removed from the router.
- Your plugin renders at/instead.
- No nav tab is added fortab.path(the override is the point).

`/`
`/`
`tab.path`

Only one plugin can override a given path. If two plugins claim the same override, the first wins and the second is ignored with a dev-mode warning.

If you only need to add a card or toolbar to an existing page without taking it over, usepage-scoped slotsinstead.

### Augmenting built-in pages (page-scoped slots)​

Full replacement viatab.overrideis heavy — your plugin now owns the entire page, including any future updates we ship to it. Most of the time you just want to add a banner, card, or toolbar to an existing page. That's whatpage-scoped slotsare for.

`tab.override`

Every built-in page exposes<page>:topand<page>:bottomslots rendered at the top and bottom of its content area. Your plugin populates one by callingregisterSlot()— the built-in page keeps working normally, and your component renders alongside it.

`<page>:top`
`<page>:bottom`
`registerSlot()`

Available slots:sessions:*,analytics:*,logs:*,cron:*,skills:*,config:*,env:*,docs:*,chat:*(each with:topand:bottom). See the full catalogue inShell slots → Slot catalogue.

`sessions:*`
`analytics:*`
`logs:*`
`cron:*`
`skills:*`
`config:*`
`env:*`
`docs:*`
`chat:*`
`:top`
`:bottom`

Minimal example — pin a banner to the top of the Sessions page:

```
// ~/.hermes/plugins/session-notes/dashboard/manifest.json{  "name": "session-notes",  "label": "Session Notes",  "tab": { "path": "/session-notes", "hidden": true },  "slots": ["sessions:top"],  "entry": "dist/index.js"}
```

```
// ~/.hermes/plugins/session-notes/dashboard/dist/index.js(function () {  const SDK = window.__HERMES_PLUGIN_SDK__;  const { React } = SDK;  const { Card, CardContent } = SDK.components;  function Banner() {    return React.createElement(Card, null,      React.createElement(CardContent, { className: "py-2 text-xs" },        "Remember to label important sessions before archiving."),    );  }  // Placeholder for the hidden tab.  window.__HERMES_PLUGINS__.register("session-notes", function () { return null; });  // The real work.  window.__HERMES_PLUGINS__.registerSlot("session-notes", "sessions:top", Banner);})();
```

Key points:

- tab.hidden: truekeeps the plugin out of the sidebar — it has no standalone page.
- Theslotsmanifest field is documentation only. The actual binding happens in the JS bundle viaregisterSlot().
- Multiple plugins can claim the same page-scoped slot. They render stacked in registration order.
- Zero footprint when no plugin registers: the built-in page renders exactly as before.

`tab.hidden: true`
`slots`
`registerSlot()`

A reference plugin (example-dashboardinhermes-example-plugins) ships a live demo that injects a banner intosessions:top— install it to see the pattern end-to-end.

`example-dashboard`
`hermes-example-plugins`
`sessions:top`

### Slot-only plugins (tab.hidden)​

`tab.hidden`

Whentab.hidden: true, the plugin registers its component (for direct URL visits) and any slots, but never adds a tab to the navigation. Used by plugins that only exist to inject into slots — a header crest, a sidebar HUD, an overlay.

`tab.hidden: true`

```
{  "name": "header-crest",  "label": "Header Crest",  "tab": {    "path": "/header-crest",    "position": "end",    "hidden": true  },  "slots": ["header-left"],  "entry": "dist/index.js"}
```

The bundle still callsregister()with a placeholder component (good practice in case someone hits the URL directly) and thenregisterSlot()to do the real work.

`register()`
`registerSlot()`

### Backend API routes​

Plugins can register FastAPI routes by settingapiin the manifest. Create the file and export arouter:

`api`
`router`

```
# ~/.hermes/plugins/my-plugin/dashboard/plugin_api.pyfrom fastapi import APIRouterrouter = APIRouter()@router.get("/data")async def get_data():    return {"items": ["one", "two", "three"]}@router.post("/action")async def do_action(body: dict):    return {"ok": True, "received": body}
```

Routes are mounted under/api/plugins/<name>/, so the above becomes:

`/api/plugins/<name>/`
- GET  /api/plugins/my-plugin/data
- POST /api/plugins/my-plugin/action

`GET  /api/plugins/my-plugin/data`
`POST /api/plugins/my-plugin/action`

Plugin API routes bypass session-token authentication since the dashboard server binds to localhost by default.Don't expose the dashboard on a public interface with--host 0.0.0.0if you run untrusted plugins— their routes become reachable too.

`--host 0.0.0.0`

#### Accessing Hermes internals​

Backend routes run inside the dashboard process, so they can import from the hermes-agent codebase directly:

```
from fastapi import APIRouterfrom hermes_state import SessionDBfrom hermes_cli.config import load_configrouter = APIRouter()@router.get("/session-count")async def session_count():    db = SessionDB()    try:        count = len(db.list_sessions(limit=9999))        return {"count": count}    finally:        db.close()@router.get("/config-snapshot")async def config_snapshot():    cfg = load_config()    return {"model": cfg.get("model", {})}
```

### Custom CSS per plugin​

If your plugin needs styles beyond Tailwind classes and inlinestyle=, add a CSS file and reference it in the manifest:

`style=`

```
{  "css": "dist/style.css"}
```

The file is injected as a<link>tag on plugin load. Use specific class names to avoid conflicts with the dashboard's styles, and reference the dashboard's CSS vars to stay theme-aware:

`<link>`

```
/* dist/style.css */.my-plugin-chart {  border: 1px solid var(--color-border);  background: var(--color-card);  color: var(--color-card-foreground);  padding: 1rem;}.my-plugin-chart:hover {  border-color: var(--color-ring);}
```

The dashboard exposes every shadcn token as--color-*plus theme extras (--theme-asset-*,--component-<bucket>-*,--radius,--spacing-mul). Reference those and your plugin automatically reskins with the active theme.

`--color-*`
`--theme-asset-*`
`--component-<bucket>-*`
`--radius`
`--spacing-mul`

### Plugin discovery & reload​

The dashboard scans three directories fordashboard/manifest.json:

`dashboard/manifest.json`
| Priority | Directory | Source label |
| --- | --- | --- |
| 1 (wins on conflict) | ~/.hermes/plugins/<name>/dashboard/ | user |
| 2 | <repo>/plugins/memory/<name>/dashboard/ | bundled |
| 2 | <repo>/plugins/<name>/dashboard/ | bundled |
| 3 | ./.hermes/plugins/<name>/dashboard/ | project— only whenHERMES_ENABLE_PROJECT_PLUGINSis set |

`~/.hermes/plugins/<name>/dashboard/`
`user`
`<repo>/plugins/memory/<name>/dashboard/`
`bundled`
`<repo>/plugins/<name>/dashboard/`
`bundled`
`./.hermes/plugins/<name>/dashboard/`
`project`
`HERMES_ENABLE_PROJECT_PLUGINS`

Discovery results are cached per dashboard process. After adding a new plugin, either:

```
# Force a rescan without restartcurl http://127.0.0.1:9119/api/dashboard/plugins/rescan
```

…or restarthermes dashboard.

`hermes dashboard`

#### Plugin load lifecycle​

1. Dashboard loads.main.tsxexposes the SDK onwindow.__HERMES_PLUGIN_SDK__and the registry onwindow.__HERMES_PLUGINS__.
2. App.tsxcallsusePlugins()→ fetchesGET /api/dashboard/plugins.
3. For each manifest: CSS<link>is injected (if declared), then a<script>tag loads the JS bundle.
4. The plugin's IIFE runs and callswindow.__HERMES_PLUGINS__.register(name, Component)— and optionally.registerSlot(name, slot, Component)for each slot.
5. The dashboard resolves the registered component against the manifest, adds the tab to navigation (unlesshidden), and mounts the component as a route.

`main.tsx`
`window.__HERMES_PLUGIN_SDK__`
`window.__HERMES_PLUGINS__`
`App.tsx`
`usePlugins()`
`GET /api/dashboard/plugins`
`<link>`
`<script>`
`window.__HERMES_PLUGINS__.register(name, Component)`
`.registerSlot(name, slot, Component)`
`hidden`

Plugins have up to2 secondsafter their script loads to callregister(). After that the dashboard stops waiting and finishes initial render. If a plugin later registers, it still appears — the nav is reactive.

`register()`

If a plugin's script fails to load (404, syntax error, exception during IIFE), the dashboard logs a warning to the browser console and continues without it.

## Combined theme + plugin demo​

Thestrike-freedom-cockpitplugin (companion repohermes-example-plugins) is a complete reskin demo. It pairs a theme YAML with a slot-only plugin to produce a cockpit-style HUD without forking the dashboard.

`strike-freedom-cockpit`
`hermes-example-plugins`

What it demonstrates:

- A full theme using palette, typography,fontUrl,layoutVariant: cockpit,assets,componentStyles(notched card corners, gradient backgrounds),colorOverrides, andcustomCSS(scanline overlay).
- A slot-only plugin (tab.hidden: true) that registers into three slots:sidebar— an MS-STATUS panel with live telemetry bars driven bySDK.api.getStatus().header-left— a faction crest that reads--theme-asset-crestfrom the active theme.footer-right— a custom tagline replacing the default org line.
- The plugin reads theme-supplied artwork via CSS vars, so swapping themes changes the hero/crest without plugin code changes.

`fontUrl`
`layoutVariant: cockpit`
`assets`
`componentStyles`
`colorOverrides`
`customCSS`
`tab.hidden: true`
- sidebar— an MS-STATUS panel with live telemetry bars driven bySDK.api.getStatus().
- header-left— a faction crest that reads--theme-asset-crestfrom the active theme.
- footer-right— a custom tagline replacing the default org line.

`sidebar`
`SDK.api.getStatus()`
`header-left`
`--theme-asset-crest`
`footer-right`

Install:

```
git clone https://github.com/NousResearch/hermes-example-plugins.git# Themecp hermes-example-plugins/strike-freedom-cockpit/theme/strike-freedom.yaml \   ~/.hermes/dashboard-themes/# Plugincp -r hermes-example-plugins/strike-freedom-cockpit ~/.hermes/plugins/
```

Open the dashboard, pickStrike Freedomfrom the theme switcher. The cockpit sidebar appears, the crest shows in the header, the tagline replaces the footer. Switch back toHermes Tealand the plugin remains installed but invisible (thesidebarslot only renders under thecockpitlayout variant).

`sidebar`
`cockpit`

Read the plugin source (strike-freedom-cockpit/dashboard/dist/index.jsin the companion repo) to see how it reads CSS vars, guards against older dashboards without slot support, and registers three slots from one bundle.

`strike-freedom-cockpit/dashboard/dist/index.js`

## API reference​

### Theme endpoints​

| Endpoint | Method | Description |
| --- | --- | --- |
| /api/dashboard/themes | GET | List available themes + active name. Built-ins return{name, label, description}; user themes also include adefinitionfield with the full normalised theme object. |
| /api/dashboard/theme | PUT | Set active theme. Body:{"name": "midnight"}. Persists toconfig.yamlunderdashboard.theme. |

`/api/dashboard/themes`
`{name, label, description}`
`definition`
`/api/dashboard/theme`
`{"name": "midnight"}`
`config.yaml`
`dashboard.theme`

### Plugin endpoints​

| Endpoint | Method | Description |
| --- | --- | --- |
| /api/dashboard/plugins | GET | List discovered plugins (with manifests, minus internal fields). |
| /api/dashboard/plugins/rescan | GET | Force re-scan the plugin directories without restarting. |
| /dashboard-plugins/<name>/<path> | GET | Serve static assets from a plugin'sdashboard/directory. Path traversal is blocked. |
| /api/plugins/<name>/* | * | Plugin-registered backend routes. |

`/api/dashboard/plugins`
`/api/dashboard/plugins/rescan`
`/dashboard-plugins/<name>/<path>`
`dashboard/`
`/api/plugins/<name>/*`

### SDK onwindow​

`window`
| Global | Type | Provider |
| --- | --- | --- |
| window.__HERMES_PLUGIN_SDK__ | object | registry.ts— React, hooks, UI components, API client, utils. |
| window.__HERMES_PLUGINS__.register(name, Component) | function | Register a plugin's main component. |
| window.__HERMES_PLUGINS__.registerSlot(name, slot, Component) | function | Register into a named shell slot. |

`window.__HERMES_PLUGIN_SDK__`
`registry.ts`
`window.__HERMES_PLUGINS__.register(name, Component)`
`window.__HERMES_PLUGINS__.registerSlot(name, slot, Component)`

## Troubleshooting​

My theme doesn't appear in the picker.Check that the file is in~/.hermes/dashboard-themes/and ends in.yamlor.yml. Refresh the page. Runcurl http://127.0.0.1:9119/api/dashboard/themes— your theme should be in the response. If the YAML has a parse error, the dashboard logs toerrors.logunder~/.hermes/logs/.

`~/.hermes/dashboard-themes/`
`.yaml`
`.yml`
`curl http://127.0.0.1:9119/api/dashboard/themes`
`errors.log`
`~/.hermes/logs/`

My plugin's tab doesn't show up.

1. Check the manifest is at~/.hermes/plugins/<name>/dashboard/manifest.json(note thedashboard/subdirectory).
2. curl http://127.0.0.1:9119/api/dashboard/plugins/rescanto force re-discovery.
3. Open browser dev tools → Network — confirmmanifest.json,index.js, and any CSS loaded without 404s.
4. Open browser dev tools → Console — look for errors during the IIFE orwindow.__HERMES_PLUGINS__ is undefined(indicates the SDK didn't initialize, usually a React render crash earlier).
5. Verify your bundle callswindow.__HERMES_PLUGINS__.register(...)with thesame nameasmanifest.json:name.

`~/.hermes/plugins/<name>/dashboard/manifest.json`
`dashboard/`
`curl http://127.0.0.1:9119/api/dashboard/plugins/rescan`
`manifest.json`
`index.js`
`window.__HERMES_PLUGINS__ is undefined`
`window.__HERMES_PLUGINS__.register(...)`
`manifest.json:name`

Slot-registered components don't render.Thesidebarslot only renders when the active theme haslayoutVariant: cockpit. Other slots always render. If you're registering into a slot with no hits, addconsole.loginsideregisterSlotto confirm the plugin bundle ran at all.

`sidebar`
`layoutVariant: cockpit`
`console.log`
`registerSlot`

Plugin backend routes return 404.

1. Confirm the manifest has"api": "plugin_api.py"pointing to an existing file insidedashboard/.
2. Restarthermes dashboard— plugin API routes are mounted once at startup,noton rescan.
3. Check thatplugin_api.pyexports a module-levelrouter = APIRouter(). Other export names are not picked up.
4. Tail~/.hermes/logs/errors.logforFailed to load plugin <name> API routes— import errors are logged there.

`"api": "plugin_api.py"`
`dashboard/`
`hermes dashboard`
`plugin_api.py`
`router = APIRouter()`
`~/.hermes/logs/errors.log`
`Failed to load plugin <name> API routes`

Theme change drops my color overrides.colorOverridesare scoped to the active theme and cleared on theme switch — that's by design. If you want overrides that persist, put them in your theme's YAML, not in the live switcher.

`colorOverrides`

Theme customCSS gets truncated.ThecustomCSSblock is capped at 32 KiB per theme. Split large stylesheets across multiple themes, or switch to a plugin that injects a full stylesheet via itscssfield (no size cap).

`customCSS`
`css`

I want to ship a plugin on PyPI.Dashboard plugins are installed by directory layout, not by pip entry point. The cleanest distribution path today is a git repo the user clones into~/.hermes/plugins/. A pip-based installer for dashboard plugins is not currently wired up.

`~/.hermes/plugins/`