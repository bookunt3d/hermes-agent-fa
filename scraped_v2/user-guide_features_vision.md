- 
- Features
- Media & Web
- Vision & Image Paste

# Vision & Image Paste

Hermes Agent supportsmultimodal vision— you can paste images from your clipboard directly into the CLI and ask the agent to analyze, describe, or work with them. Images are sent to the model as base64-encoded content blocks, so any vision-capable model can process them.

Portal subscribers get vision-capable models (Claude, GPT-5, Gemini) in the same catalog — no extra credentials needed. SeeNous Portal.

## How It Works​

1. Copy an image to your clipboard (screenshot, browser image, etc.)
2. Attach it using one of the methods below
3. Type your question and press Enter
4. The image appears as a[📎 Image #1]badge above the input
5. On submit, the image is sent to the model as a vision content block

`[📎 Image #1]`

You can attach multiple images before sending — each gets its own badge. PressCtrl+Cto clear all attached images.

`Ctrl+C`

Images are saved to~/.hermes/images/as PNG files with timestamped filenames.

`~/.hermes/images/`

## Paste Methods​

How you attach an image depends on your terminal environment. Not all methods work everywhere — here's the full breakdown:

### /pasteCommand​

`/paste`

The most reliable explicit image-attach fallback.

```
/paste
```

Type/pasteand press Enter. Hermes checks your clipboard for an image and attaches it. This is the safest option when your terminal rewritesCmd+V/Ctrl+V, or when you copied only an image and there is no bracketed-paste text payload to inspect.

`/paste`
`Cmd+V`
`Ctrl+V`

### Ctrl+V / Cmd+V​

Hermes now treats paste as a layered flow:

- normal text paste first
- native clipboard / OSC52 text fallback if the terminal did not deliver text cleanly
- image attach when the clipboard or pasted payload resolves to an image or image path

This means pasted macOS screenshot temp paths andfile://...image URIs can attach immediately instead of sitting in the composer as raw text.

`file://...`

If your clipboard hasonly an image(no text), terminals still cannot send binary image bytes directly. Use/pasteas the explicit image-attach fallback.

`/paste`

### /terminal-setupfor VS Code / Cursor / Windsurf​

`/terminal-setup`

If you run the TUI inside a local VS Code-family integrated terminal on macOS, Hermes can install the recommendedworkbench.action.terminal.sendSequencebindings for better multiline and undo/redo parity:

`workbench.action.terminal.sendSequence`

```
/terminal-setup
```

This is especially useful whenCmd+Enter,Cmd+Z, orShift+Cmd+Zare being intercepted by the IDE. Run it on the local machine only — not inside an SSH session.

`Cmd+Enter`
`Cmd+Z`
`Shift+Cmd+Z`

## Platform Compatibility​

| Environment | /paste | Cmd/Ctrl+V | /terminal-setup | Notes |
| --- | --- | --- | --- | --- |
| macOS Terminal / iTerm2 | ✅ | ✅ | n/a | Best experience — native clipboard + screenshot-path recovery |
| Apple Terminal | ✅ | ✅ | n/a | If Cmd+←/→/⌫ gets rewritten, use Ctrl+A / Ctrl+E / Ctrl+U fallbacks |
| Linux X11 desktop | ✅ | ✅ | n/a | Requiresxclip(apt install xclip) |
| Linux Wayland desktop | ✅ | ✅ | n/a | Requireswl-paste(apt install wl-clipboard) |
| WSL2 (Windows Terminal) | ✅ | ✅ | n/a | Usespowershell.exe— no extra install needed |
| VS Code / Cursor / Windsurf (local) | ✅ | ✅ | ✅ | Recommended for better Cmd+Enter / undo / redo parity |
| VS Code / Cursor / Windsurf (SSH) | ❌² | ❌² | ❌³ | Run/terminal-setupon the local machine instead |
| SSH terminal (any) | ❌² | ❌² | n/a | Remote clipboard not accessible |

`/paste`
`/terminal-setup`
`xclip`
`apt install xclip`
`wl-paste`
`apt install wl-clipboard`
`powershell.exe`
`/terminal-setup`

² SeeSSH & Remote Sessionsbelow
³ The command writes local IDE keybindings and should not be run from the remote host

## Platform-Specific Setup​

### macOS​

No setup required.Hermes usesosascript(built into macOS) to read the clipboard. For faster performance, optionally installpngpaste:

`osascript`
`pngpaste`

```
brew install pngpaste
```

### Linux (X11)​

Installxclip:

`xclip`

```
# Ubuntu/Debiansudo apt install xclip# Fedorasudo dnf install xclip# Archsudo pacman -S xclip
```

### Linux (Wayland)​

Modern Linux desktops (Ubuntu 22.04+, Fedora 34+) often use Wayland by default. Installwl-clipboard:

`wl-clipboard`

```
# Ubuntu/Debiansudo apt install wl-clipboard# Fedorasudo dnf install wl-clipboard# Archsudo pacman -S wl-clipboard
```

```
echo $XDG_SESSION_TYPE# "wayland" = Wayland, "x11" = X11, "tty" = no display server
```

### WSL2​

No extra setup required.Hermes detects WSL2 automatically (via/proc/version) and usespowershell.exeto access the Windows clipboard through .NET'sSystem.Windows.Forms.Clipboard. This is built into WSL2's Windows interop —powershell.exeis available by default.

`/proc/version`
`powershell.exe`
`System.Windows.Forms.Clipboard`
`powershell.exe`

The clipboard data is transferred as base64-encoded PNG over stdout, so no file path conversion or temp files are needed.

If you're running WSLg (WSL2 with GUI support), Hermes tries the PowerShell path first, then falls back towl-paste. WSLg's clipboard bridge only supports BMP format for images — Hermes auto-converts BMP to PNG using Pillow (if installed) or ImageMagick'sconvertcommand.

`wl-paste`
`convert`

#### Verify WSL2 clipboard access​

```
# 1. Check WSL detectiongrep -i microsoft /proc/version# 2. Check PowerShell is accessiblewhich powershell.exe# 3. Copy an image, then checkpowershell.exe -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::ContainsImage()"# Should print "True"
```

## SSH & Remote Sessions​

Clipboard image paste does not fully work over SSH.When you SSH into a remote machine, the Hermes CLI runs on the remote host. Clipboard tools (xclip,wl-paste,powershell.exe,osascript) read the clipboard of the machine they run on — which is the remote server, not your local machine. Your local clipboard image is therefore inaccessible from the remote side.

`xclip`
`wl-paste`
`powershell.exe`
`osascript`

Text can sometimes still bridge through terminal paste or OSC52, but image clipboard access and local screenshot temp paths remain tied to the machine running Hermes.

### Workarounds for SSH​

1. Upload the image file— Save the image locally, upload it to the remote server viascp, VSCode's file explorer (drag-and-drop), or any file transfer method. Then reference it by path.(A/attach <filepath>command is planned for a future release.)
2. Use a URL— If the image is accessible online, just paste the URL in your message. The agent can usevision_analyzeto look at any image URL directly.
3. X11 forwarding— Connect withssh -Xto forward X11. This letsxclipon the remote machine access your local X11 clipboard. Requires an X server running locally (XQuartz on macOS, built-in on Linux X11 desktops). Slow for large images.
4. Use a messaging platform— Send images to Hermes via Telegram, Discord, Slack, or WhatsApp. These platforms handle image upload natively and are not affected by clipboard/terminal limitations.

Upload the image file— Save the image locally, upload it to the remote server viascp, VSCode's file explorer (drag-and-drop), or any file transfer method. Then reference it by path.(A/attach <filepath>command is planned for a future release.)

`scp`
`/attach <filepath>`

Use a URL— If the image is accessible online, just paste the URL in your message. The agent can usevision_analyzeto look at any image URL directly.

`vision_analyze`

X11 forwarding— Connect withssh -Xto forward X11. This letsxclipon the remote machine access your local X11 clipboard. Requires an X server running locally (XQuartz on macOS, built-in on Linux X11 desktops). Slow for large images.

`ssh -X`
`xclip`

Use a messaging platform— Send images to Hermes via Telegram, Discord, Slack, or WhatsApp. These platforms handle image upload natively and are not affected by clipboard/terminal limitations.

## Why Terminals Can't Paste Images​

This is a common source of confusion, so here's the technical explanation:

Terminals aretext-basedinterfaces. When you press Ctrl+V (or Cmd+V), the terminal emulator:

1. Reads the clipboard fortext content
2. Wraps it inbracketed pasteescape sequences
3. Sends it to the application through the terminal's text stream

If the clipboard contains only an image (no text), the terminal has nothing to send. There is no standard terminal escape sequence for binary image data. The terminal simply does nothing.

This is why Hermes uses a separate clipboard check — instead of receiving image data through the terminal paste event, it calls OS-level tools (osascript,powershell.exe,xclip,wl-paste) directly via subprocess to read the clipboard independently.

`osascript`
`powershell.exe`
`xclip`
`wl-paste`

## Supported Models​

Image paste works with any vision-capable model. The image is sent as a base64-encoded data URL in the OpenAI vision content format:

```
{  "type": "image_url",  "image_url": {    "url": "data:image/png;base64,..."  }}
```

Most modern models support this format, including GPT-4 Vision, Claude (with vision), Gemini, and open-source multimodal models served through OpenRouter.

## Image Routing (Vision-Capable vs Text-Only Models)​

When a user attaches an image — from the CLI clipboard, the gateway (Telegram/Discord photo), or any other entry point — Hermes routes it based on whether your current model actually supports vision:

| Your model | What happens to the image |
| --- | --- |
| Vision-capable(GPT-4V, Claude with vision, Gemini, Qwen-VL, MiMo-VL, etc.) | Sent asreal pixelsusing the provider's native image content format above. No text summary layer. |
| Text-only(DeepSeek V3, smaller open-source models, older chat-only endpoints) | Routed through thevision_analyzeauxiliary tool — an auxiliary vision model describes the image, and the text description is injected into the conversation. |

`vision_analyze`

You don't configure this — Hermes looks up your current model's capability in the provider metadata and picks the right path automatically. The practical effect: you can switch between vision and non-vision models mid-session and image handling "just works" without changing your workflow. Text-only models get coherent context about the image rather than a broken multimodal payload they'd have to reject.

Which auxiliary model handles the text-description path is configurable underauxiliary.vision— seeAuxiliary Models.

`auxiliary.vision`

### vision_analyzehas the same dual behavior​

`vision_analyze`

Thevision_analyzetool itself follows the same routing. When the active main model is vision-capableandits provider supports image content inside tool results (currently the Anthropic, OpenAI, Azure-OpenAI, and Gemini 3.x stacks),vision_analyzeshort-circuits the auxiliary describer and returns the raw image pixels as a multimodal tool-result envelope. The main model sees the image natively on its next turn — no aux call, no text-summary information loss, no extra latency.

`vision_analyze`
`vision_analyze`

For text-only main models (or providers whose tool-result channel doesn't carry images),vision_analyzefalls back to the legacy path: it asks the configured auxiliary vision model to describe the image and returns the description as plain text. Either way the calling tool signature is the same — the tool decides which path to take at runtime based on the active model.

`vision_analyze`