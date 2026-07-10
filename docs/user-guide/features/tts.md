---
layout: docs
title: "Features_Tts"
permalink: /docs/user-guide/features_tts/
---

- 
- Features
- Media & Web
- Voice & TTS

# Voice & TTS

Hermes Agent supports both text-to-speech output and voice message transcription across all messaging platforms.

If you have a paidNous Portalsubscription, OpenAI TTS is available through theTool Gatewaywithout a separate OpenAI API key. New installs can runhermes setup --portalto log in and turn on every gateway tool at once; existing installs can pickNous Subscriptionfor just TTS viahermes modelorhermes tools.

`hermes setup --portal`
`hermes model`
`hermes tools`

## Text-to-Speech​

Convert text to speech with ten providers:

| Provider | Quality | Cost | API Key |
| --- | --- | --- | --- |
| Edge TTS(default) | Good | Free | None needed |
| ElevenLabs | Excellent | Paid | ELEVENLABS_API_KEY |
| OpenAI TTS | Good | Paid | VOICE_TOOLS_OPENAI_KEY |
| MiniMax TTS | Excellent | Paid | MINIMAX_API_KEY |
| Mistral (Voxtral TTS) | Excellent | Paid | MISTRAL_API_KEY |
| Google Gemini TTS | Excellent | Free tier | GEMINI_API_KEY |
| xAI TTS | Excellent | Paid | XAI_API_KEY |
| NeuTTS | Good | Free (local) | None needed |
| KittenTTS | Good | Free (local) | None needed |
| Piper | Good | Free (local) | None needed |

`ELEVENLABS_API_KEY`
`VOICE_TOOLS_OPENAI_KEY`
`MINIMAX_API_KEY`
`MISTRAL_API_KEY`
`GEMINI_API_KEY`
`XAI_API_KEY`

### Platform Delivery​

| Platform | Delivery | Format |
| --- | --- | --- |
| Telegram | Voice bubble (plays inline) | Opus.ogg |
| Discord | Voice bubble (Opus/OGG), falls back to file attachment | Opus/MP3 |
| WhatsApp | Audio file attachment | MP3 |
| CLI | Saved to~/.hermes/audio_cache/ | MP3 |

`.ogg`
`~/.hermes/audio_cache/`

### Configuration​

```
# In ~/.hermes/config.yamltts:  provider: "edge"              # "edge" | "elevenlabs" | "openai" | "minimax" | "mistral" | "gemini" | "xai" | "neutts" | "kittentts" | "piper"  speed: 1.0                    # Global speed multiplier (provider-specific settings override this)  edge:    voice: "en-US-AriaNeural"   # 322 voices, 74 languages    speed: 1.0                  # Converted to rate percentage (+/-%)  elevenlabs:    voice_id: "pNInz6obpgDQGcFmaJgB"  # Adam    model_id: "eleven_multilingual_v2"  openai:    model: "gpt-4o-mini-tts"    voice: "alloy"              # alloy, echo, fable, onyx, nova, shimmer    base_url: "https://api.openai.com/v1"  # Override for OpenAI-compatible TTS endpoints    speed: 1.0                  # 0.25 - 4.0  minimax:    model: "speech-2.8-hd"     # speech-2.8-hd (default), speech-2.8-turbo    voice_id: "English_Graceful_Lady"  # See https://platform.minimax.io/faq/system-voice-id    speed: 1                    # 0.5 - 2.0    vol: 1                      # 0 - 10    pitch: 0                    # -12 - 12  mistral:    model: "voxtral-mini-tts-2603"    voice_id: "c69964a6-ab8b-4f8a-9465-ec0925096ec8"  # Paul - Neutral (default)  gemini:    model: "gemini-2.5-flash-preview-tts"  # or gemini-3.1-flash-tts-preview    voice: "Kore"               # 30 prebuilt voices: Zephyr, Puck, Kore, Enceladus, Gacrux, etc.    audio_tags: false           # Enable hidden Gemini 3.1 TTS audio-tag insertion    persona_prompt_file: ""      # Optional Markdown/text file with Gemini voice direction  xai:    voice_id: "eve"             # or a custom voice ID — see docs below    language: "en"              # ISO 639-1 code    sample_rate: 24000          # 22050 / 24000 (default) / 44100 / 48000    bit_rate: 128000            # MP3 bitrate; only applies when codec=mp3    # base_url: "https://api.x.ai/v1"   # Override via XAI_BASE_URL env var  neutts:    ref_audio: ''    ref_text: ''    model: neuphonic/neutts-air-q4-gguf    device: cpu  kittentts:    model: KittenML/kitten-tts-nano-0.8-int8   # 25MB int8; also: kitten-tts-micro-0.8 (41MB), kitten-tts-mini-0.8 (80MB)    voice: Jasper                               # Jasper, Bella, Luna, Bruno, Rosie, Hugo, Kiki, Leo    speed: 1.0                                  # 0.5 - 2.0    clean_text: true                            # Expand numbers, currencies, units  piper:    voice: en_US-lessac-medium                  # voice name (auto-downloaded) OR absolute path to .onnx    # voices_dir: ''                            # default: ~/.hermes/cache/piper-voices/    # use_cuda: false                           # requires onnxruntime-gpu    # length_scale: 1.0                         # 2.0 = twice as slow    # noise_scale: 0.667    # noise_w_scale: 0.8    # volume: 1.0                               # 0.5 = half as loud    # normalize_audio: true
```

Speed control: The globaltts.speedvalue applies to all providers by default. Each provider can override it with its ownspeedsetting (e.g.,tts.openai.speed: 1.5). Provider-specific speed takes precedence over the global value. Default is1.0(normal speed).

`tts.speed`
`speed`
`tts.openai.speed: 1.5`
`1.0`

### Gemini Persona Prompts​

Gemini TTS can follow natural-language performance direction. Settts.gemini.persona_prompt_fileto a local Markdown or text file that describes the voice persona. The file can include Gemini-style sections such asAUDIO PROFILE,SCENE,DIRECTOR'S NOTES,SAMPLE CONTEXT, andTRANSCRIPT.

`tts.gemini.persona_prompt_file`
`AUDIO PROFILE`
`SCENE`
`DIRECTOR'S NOTES`
`SAMPLE CONTEXT`
`TRANSCRIPT`

If the file contains{transcript}or{{ transcript }}, Hermes replaces that placeholder with the live TTS text. Otherwise, Hermes appends a labeledTRANSCRIPTsection automatically. The persona prompt stays local and is not shown in the chat reply.

`{transcript}`
`{{ transcript }}`
`TRANSCRIPT`

```
tts:  provider: gemini  gemini:    voice: Algieba    persona_prompt_file: ~/.hermes/tts/butler-voice.md
```

### Gemini Audio Tags​

Gemini 3.1 Flash TTS supports freeform square-bracket audio tags such as[whispers],[excitedly],[very slow],[laughs], and other expressive delivery notes. Enabletts.gemini.audio_tagsto have Hermes run a hidden rewrite pass before Gemini TTS. The rewrite inserts inline tags into the TTS script only; the visible chat reply stays unchanged.

`[whispers]`
`[excitedly]`
`[very slow]`
`[laughs]`
`tts.gemini.audio_tags`

```
tts:  provider: gemini  gemini:    model: gemini-3.1-flash-tts-preview    audio_tags: true
```

The rewrite usesauxiliary.tts_audio_tagsand defaults to your main chat model. Override that auxiliary task if you want tag insertion handled by a cheaper or faster model.

`auxiliary.tts_audio_tags`

### Input length limits​

Each provider has a documented per-request input-character cap. Hermes truncates text before calling the provider so requests never fail with a length error:

| Provider | Default cap (chars) |
| --- | --- |
| Edge TTS | 5000 |
| OpenAI | 4096 |
| xAI | 15000 |
| MiniMax | 10000 |
| Mistral | 4000 |
| Google Gemini | 32000 |
| ElevenLabs | Model-aware (see below) |
| NeuTTS | 2000 |
| KittenTTS | 2000 |
| Piper | 5000 |

ElevenLabspicks a cap from the configuredmodel_id:

`model_id`
| model_id | Cap (chars) |
| --- | --- |
| eleven_flash_v2_5 | 40000 |
| eleven_flash_v2 | 30000 |
| eleven_multilingual_v2(default),eleven_multilingual_v1,eleven_english_sts_v2,eleven_english_sts_v1 | 10000 |
| eleven_v3,eleven_ttv_v3 | 5000 |
| Unknown model | Falls back to provider default (10000) |

`model_id`
`eleven_flash_v2_5`
`eleven_flash_v2`
`eleven_multilingual_v2`
`eleven_multilingual_v1`
`eleven_english_sts_v2`
`eleven_english_sts_v1`
`eleven_v3`
`eleven_ttv_v3`

Override per providerwithmax_text_length:under the provider section of your TTS config:

`max_text_length:`

```
tts:  openai:    max_text_length: 8192   # raise or lower the provider cap
```

Only positive integers are honored. Zero, negative, non-numeric, or boolean values fall through to the provider default, so a broken config can't accidentally disable truncation.

### Telegram Voice Bubbles & ffmpeg​

Telegram voice bubbles require Opus/OGG audio format:

- OpenAI, ElevenLabs, and Mistralproduce Opus natively — no extra setup
- Edge TTS(default) outputs MP3 and needsffmpegto convert:
- MiniMax TTSoutputs MP3 and needsffmpegto convert for Telegram voice bubbles
- Google Gemini TTSoutputs raw PCM and usesffmpegto encode Opus directly for Telegram voice bubbles
- xAI TTSoutputs MP3 and needsffmpegto convert for Telegram voice bubbles
- NeuTTSoutputs WAV and also needsffmpegto convert for Telegram voice bubbles
- KittenTTSoutputs WAV and also needsffmpegto convert for Telegram voice bubbles
- Piperoutputs WAV and also needsffmpegto convert for Telegram voice bubbles

```
# Ubuntu/Debiansudo apt install ffmpeg# macOSbrew install ffmpeg# Fedorasudo dnf install ffmpeg
```

Without ffmpeg, Edge TTS, MiniMax TTS, NeuTTS, KittenTTS, and Piper audio are sent as regular audio files (playable, but shown as a rectangular player instead of a voice bubble).

If you want voice bubbles without installing ffmpeg, switch to the OpenAI, ElevenLabs, or Mistral provider.

### xAI Custom Voices (voice cloning)​

xAI supports cloning your voice and using it with TTS. Create a custom voice in thexAI Console, then set the resultingvoice_idin your config:

`voice_id`

```
tts:  provider: xai  xai:    voice_id: "nlbqfwie"   # your custom voice ID
```

See thexAI Custom Voices docsfor details on recording, supported formats, and limits.

### Piper (local, 44 languages)​

Piper is a fast, local neural TTS engine from the Open Home Foundation (the Home Assistant maintainers). It runs entirely on CPU, supports44 languageswith pre-trained voices, and needs no API key.

Install viahermes tools→ Voice & TTS → Piper — Hermes runspip install piper-ttsfor you. Or install manually:pip install piper-tts.

`hermes tools`
`pip install piper-tts`
`pip install piper-tts`

Switch to Piper:

```
tts:  provider: piper  piper:    voice: en_US-lessac-medium
```

On the first TTS call for a voice that isn't cached locally, Hermes runspython -m piper.download_voices <name>and downloads the model (~20-90MB depending on quality tier) into~/.hermes/cache/piper-voices/. Subsequent calls reuse the cached model.

`python -m piper.download_voices <name>`
`~/.hermes/cache/piper-voices/`

Picking a voice.Thefull voice catalogcovers English, Spanish, French, German, Italian, Dutch, Portuguese, Russian, Polish, Turkish, Chinese, Arabic, Hindi, and more — each withx_low/low/medium/highquality tiers. Sample voices atrhasspy.github.io/piper-samples.

`x_low`
`low`
`medium`
`high`

Using a pre-downloaded voice.Settts.piper.voiceto an absolute path ending in.onnx:

`tts.piper.voice`
`.onnx`

```
tts:  piper:    voice: /path/to/my-custom-voice.onnx
```

Advanced knobs(tts.piper.length_scale/noise_scale/noise_w_scale/volume/normalize_audio,use_cuda) correspond 1:1 to Piper'sSynthesisConfig. They're ignored on olderpiper-ttsversions.

`tts.piper.length_scale`
`noise_scale`
`noise_w_scale`
`volume`
`normalize_audio`
`use_cuda`
`SynthesisConfig`
`piper-tts`

### Custom command providers​

If a TTS engine you want isn't natively supported (VoxCPM, MLX-Kokoro, XTTS CLI, a voice-cloning script, anything else that exposes a CLI), you can wire it in as acommand-type providerwithout writing any Python. Hermes writes the input text to a temp UTF-8 file, runs your shell command, and reads the audio file the command produced.

Declare one or more providers undertts.providers.<name>and switch between them withtts.provider: <name>— the same way you switch between built-ins likeedgeandopenai.

`tts.providers.<name>`
`tts.provider: <name>`
`edge`
`openai`

```
tts:  provider: voxcpm                 # pick any name under tts.providers  providers:    voxcpm:      type: command      command: "voxcpm --ref ~/voice.wav --text-file {input_path} --out {output_path}"      output_format: mp3      timeout: 180      voice_compatible: true       # try to deliver as a Telegram voice bubble    mlx-kokoro:      type: command      command: "python -m mlx_kokoro --in {input_path} --out {output_path} --voice {voice}"      voice: af_sky      output_format: wav    piper-custom:                  # native Piper also supports custom .onnx via tts.piper.voice      type: command      command: "piper -m /path/to/custom.onnx -f {output_path} < {input_path}"      output_format: wav
```

#### Example: Doubao (Chinese seed-tts-2.0)​

For high-quality Chinese TTS via ByteDance'sseed-tts-2.0bidirectional-streaming API, install thedoubao-speechPyPI package and wire it in as a command provider:

`doubao-speech`

```
pip install doubao-speechexport VOLCENGINE_APP_ID="your-app-id"export VOLCENGINE_ACCESS_TOKEN="your-access-token"
```

```
tts:  provider: doubao  providers:    doubao:      type: command      command: "doubao-speech say --text-file {input_path} --out {output_path}"      output_format: mp3      max_text_length: 1024      timeout: 30
```

Credentials come from your shell environment (VOLCENGINE_APP_ID/VOLCENGINE_ACCESS_TOKEN) or~/.doubao-speech/config.yaml. Pick a voice by adding--voice zh-female-warm(or any other alias fromdoubao-speech list-voices) to the command.doubao-speechalso bundles streaming ASR — see theSTT section belowfor Hermes integration. Source and full docs:github.com/Hypnus-Yuan/doubao-speech.

`VOLCENGINE_APP_ID`
`VOLCENGINE_ACCESS_TOKEN`
`~/.doubao-speech/config.yaml`
`--voice zh-female-warm`
`doubao-speech list-voices`
`doubao-speech`

#### Placeholders​

Your command template can reference these placeholders. Hermes substitutes them at render time and shell-quotes each value for the surrounding context (bare / single-quoted / double-quoted), so paths with spaces and other shell-sensitive characters are safe.

| Placeholder | Meaning |
| --- | --- |
| {input_path} | Path to the temp UTF-8 text file Hermes wrote |
| {text_path} | Alias for{input_path} |
| {output_path} | Path the command must write audio to |
| {format} | mp3/wav/ogg/flac |
| {voice} | tts.providers.<name>.voice, empty when unset |
| {model} | tts.providers.<name>.model |
| {speed} | Resolved speed multiplier (provider or global) |

`{input_path}`
`{text_path}`
`{input_path}`
`{output_path}`
`{format}`
`mp3`
`wav`
`ogg`
`flac`
`{voice}`
`tts.providers.<name>.voice`
`{model}`
`tts.providers.<name>.model`
`{speed}`

Use{{and}}for literal braces.

`{{`
`}}`

#### Optional keys​

| Key | Default | Meaning |
| --- | --- | --- |
| timeout | 120 | Seconds; the process tree is killed on expiry (Unixkillpg, Windowstaskkill /T). |
| output_format | mp3 | One ofmp3/wav/ogg/flac. Auto-inferred from the output extension if Hermes picks a path. |
| voice_compatible | false | Whentrue, Hermes converts MP3/WAV output to Opus/OGG via ffmpeg so Telegram renders a voice bubble. |
| max_text_length | 5000 | Input is truncated to this length before rendering the command. |
| voice/model | empty | Passed to the command as placeholder values only. |

`timeout`
`120`
`killpg`
`taskkill /T`
`output_format`
`mp3`
`mp3`
`wav`
`ogg`
`flac`
`voice_compatible`
`false`
`true`
`max_text_length`
`5000`
`voice`
`model`

#### Behavior notes​

- Built-in names always win.Atts.providers.openaientry never shadows the native OpenAI provider, so no user config can silently replace a built-in.
- Default delivery is a document.Command providers deliver as regular audio attachments on every platform. Opt in to voice-bubble delivery per-provider withvoice_compatible: true.
- Command failures surface to the agent.Non-zero exit, empty output, or timeout all return an error with the command's stderr/stdout included so you can debug the provider from the conversation.
- type: commandis the default whencommand:is set.Writingtype: commandexplicitly is good practice but not required; an entry with a non-emptycommandstring is treated as a command provider.
- {input_path}/{text_path}are interchangeable.Use whichever reads better in your command.

`tts.providers.openai`
`voice_compatible: true`
`type: command`
`command:`
`type: command`
`command`
`{input_path}`
`{text_path}`

#### Security​

Command-type providers run whatever shell command you configure, with your user's permissions. Hermes quotes placeholder values and enforces the configured timeout, but the command template itself is trusted local input — treat it the same way you would a shell script on your PATH.

### Python plugin providers​

For TTS engines that can't be expressed as a single shell command — Python SDKs without a CLI, streaming engines, voice-listing APIs, OAuth-refreshing auth — register a Python plugin viactx.register_tts_provider(). The plugincoexists with(does not replace) theCustom command providersregistry; pick the surface that fits your engine.

`ctx.register_tts_provider()`

#### When to pick which​

| Your backend has… | Use |
| --- | --- |
| A single CLI reading text from a file/stdin and writing audio to a file/stdout | Command provider(no Python needed) |
| Two or three CLIs chained with shell pipes | Command provider |
| A Python SDK only — no CLI | Plugin |
| Streaming bytes you want to deliver chunked (mid-generation voice bubbles) | Plugin(overridestream()) |
| A voice-listing API used byhermes setup | Plugin(overridelist_voices()) |
| OAuth refresh flow (not a static bearer token) | Plugin |

`stream()`
`hermes setup`
`list_voices()`

Built-ins always win, and command providers win over a same-name plugin — so plugins are safe to register against any non-built-in name without worrying about shadowing your existing config.

#### Minimal plugin​

Drop this in~/.hermes/plugins/my-tts/:

`~/.hermes/plugins/my-tts/`

plugin.yaml:

`plugin.yaml`

```
name: my-ttsversion: 0.1.0description: "My custom Python TTS backend"
```

__init__.py:

`__init__.py`

```
from agent.tts_provider import TTSProviderclass MyTTSProvider(TTSProvider):    @property    def name(self) -> str:        return "my-tts"  # what tts.provider matches against    @property    def display_name(self) -> str:        return "My Custom TTS"    def is_available(self) -> bool:        # Return False when credentials/deps are missing — picker skips        # this row but the dispatcher still routes here on explicit config.        import os        return bool(os.environ.get("MY_TTS_API_KEY"))    def synthesize(self, text, output_path, *, voice=None, model=None,                   speed=None, format="mp3", **extra) -> str:        # Write audio bytes to output_path, return the path.        # Raise on failure — the dispatcher converts exceptions to a        # standard error envelope.        import my_tts_sdk        client = my_tts_sdk.Client()        audio_bytes = client.synthesize(text=text, voice=voice or "default")        with open(output_path, "wb") as f:            f.write(audio_bytes)        return output_pathdef register(ctx):    ctx.register_tts_provider(MyTTSProvider())
```

Enable it (hermes plugins enable my-tts), pointtts.providerat it (tts.provider: my-ttsinconfig.yaml), and thetext_to_speechtool will route through your plugin.

`hermes plugins enable my-tts`
`tts.provider`
`tts.provider: my-tts`
`config.yaml`
`text_to_speech`

#### Optional hooks​

Override these on your provider class for richer integration:

- list_voices()→ list of{id, display, language, gender, preview_url}dicts shown inhermes tools.
- list_models()→ list of{id, display, languages, max_text_length}dicts.
- get_setup_schema()→ return{name, badge, tag, env_vars: [{key, prompt, url}]}to power the picker row inhermes tools/hermes setup. Without this, the plugin still works but its row in the picker is minimal.
- stream(text, *, voice, model, format, **extra)→ iterator yielding audio bytes for streaming delivery (default raisesNotImplementedError).
- voice_compatibleproperty → setTrueif your output is Opus-compatible and the gateway should deliver it as a voice bubble (defaultFalse= regular audio attachment).

`list_voices()`
`{id, display, language, gender, preview_url}`
`hermes tools`
`list_models()`
`{id, display, languages, max_text_length}`
`get_setup_schema()`
`{name, badge, tag, env_vars: [{key, prompt, url}]}`
`hermes tools`
`hermes setup`
`stream(text, *, voice, model, format, **extra)`
`NotImplementedError`
`voice_compatible`
`True`
`False`

Seeagent/tts_provider.pyfor the full ABC including docstrings.

`agent/tts_provider.py`

## Voice Message Transcription (STT)​

Voice messages sent on Telegram, Discord, WhatsApp, Slack, or Signal are automatically transcribed and injected as text into the conversation. The agent sees the transcript as normal text.

| Provider | Quality | Cost | API Key |
| --- | --- | --- | --- |
| Local Whisper(default) | Good | Free | None needed |
| Groq Whisper API | Good–Best | Free tier | GROQ_API_KEY |
| OpenAI Whisper API | Good–Best | Paid | VOICE_TOOLS_OPENAI_KEYorOPENAI_API_KEY |

`GROQ_API_KEY`
`VOICE_TOOLS_OPENAI_KEY`
`OPENAI_API_KEY`

Local transcription works out of the box whenfaster-whisperis installed. If that's unavailable, Hermes can also use a localwhisperCLI from common install locations (like/opt/homebrew/bin) or a custom command viaHERMES_LOCAL_STT_COMMAND.

`faster-whisper`
`whisper`
`/opt/homebrew/bin`
`HERMES_LOCAL_STT_COMMAND`

### Configuration​

```
# In ~/.hermes/config.yamlstt:  provider: "local"           # "local" | "groq" | "openai" | "mistral" | "xai"  local:    model: "base"             # tiny, base, small, medium, large-v3  openai:    model: "whisper-1"        # whisper-1, gpt-4o-mini-transcribe, gpt-4o-transcribe  mistral:    model: "voxtral-mini-latest"  # voxtral-mini-latest, voxtral-mini-2602  xai:    model: "grok-stt"         # xAI Grok STT
```

### Provider Details​

Local (faster-whisper)— Runs Whisper locally viafaster-whisper. Uses CPU by default, GPU if available. Model sizes:

| Model | Size | Speed | Quality |
| --- | --- | --- | --- |
| tiny | ~75 MB | Fastest | Basic |
| base | ~150 MB | Fast | Good (default) |
| small | ~500 MB | Medium | Better |
| medium | ~1.5 GB | Slower | Great |
| large-v3 | ~3 GB | Slowest | Best |

`tiny`
`base`
`small`
`medium`
`large-v3`

Groq API— RequiresGROQ_API_KEY. Good cloud fallback when you want a free hosted STT option.

`GROQ_API_KEY`

OpenAI API— AcceptsVOICE_TOOLS_OPENAI_KEYfirst and falls back toOPENAI_API_KEY. Supportswhisper-1,gpt-4o-mini-transcribe, andgpt-4o-transcribe.

`VOICE_TOOLS_OPENAI_KEY`
`OPENAI_API_KEY`
`whisper-1`
`gpt-4o-mini-transcribe`
`gpt-4o-transcribe`

Mistral API (Voxtral Transcribe)— RequiresMISTRAL_API_KEY. Uses Mistral'sVoxtral Transcribemodels. Supports 13 languages, speaker diarization, and word-level timestamps. Install withcd ~/.hermes/hermes-agent && uv pip install -e ".[mistral]".

`MISTRAL_API_KEY`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[mistral]"`

xAI Grok STT— RequiresXAI_API_KEY. Posts tohttps://api.x.ai/v1/sttas multipart/form-data. Good choice if you're already using xAI for chat or TTS and want one API key for everything. Auto-detection order puts it after Groq — explicitly setstt.provider: xaito force it.

`XAI_API_KEY`
`https://api.x.ai/v1/stt`
`stt.provider: xai`

Custom local CLI fallback— SetHERMES_LOCAL_STT_COMMANDif you want Hermes to call a local transcription command directly. The command template supports{input_path},{output_dir},{language}, and{model}placeholders. Your command must write a.txttranscript somewhere under{output_dir}.

`HERMES_LOCAL_STT_COMMAND`
`{input_path}`
`{output_dir}`
`{language}`
`{model}`
`.txt`
`{output_dir}`

#### Example: Doubao / Volcengine ASR​

If you usedoubao-speechfor Doubao TTS (seeabove), the same package handles speech-to-text via the local-command STT surface:

`doubao-speech`

```
pip install doubao-speechexport VOLCENGINE_APP_ID="your-app-id"export VOLCENGINE_ACCESS_TOKEN="your-access-token"export HERMES_LOCAL_STT_COMMAND='doubao-speech transcribe {input_path} --out {output_dir}/transcript.txt'
```

```
stt:  provider: local_command
```

Hermes writes the incoming voice message to{input_path}, runs the command, and reads the.txtfile produced under{output_dir}. Language is auto-detected by the Volcengine bigmodel endpoint.

`{input_path}`
`.txt`
`{output_dir}`

### Fallback Behavior​

If your configured provider isn't available, Hermes automatically falls back:

- Local faster-whisper unavailable→ Tries a localwhisperCLI orHERMES_LOCAL_STT_COMMANDbefore cloud providers
- Groq key not set→ Falls back to local transcription, then OpenAI
- OpenAI key not set→ Falls back to local transcription, then Groq
- Mistral key/SDK not set→ Skipped in auto-detect; falls through to next available provider
- Nothing available→ Voice messages pass through with an accurate note to the user

`whisper`
`HERMES_LOCAL_STT_COMMAND`

### STT custom command providers​

If the STT engine you want isn't natively supported (Doubao ASR, NVIDIA Parakeet, a whisper.cpp build, an open-source SenseVoice CLI, anything else that exposes a shell command), wire it in as acommand-type providerwithout writing any Python. Hermes runs your shell command against the audio file and reads back the transcript.

Declare one or more providers understt.providers.<name>and switch between them withstt.provider: <name>— same shape as the TTScommand-provider registry, adapted for the input=audio → output=transcript direction.

`stt.providers.<name>`
`stt.provider: <name>`

```
stt:  provider: parakeet                # pick any name under stt.providers  providers:    parakeet:      type: command      command: "parakeet-asr --model nvidia/parakeet-tdt-0.6b-v2 --in {input_path} --out {output_path}"      format: txt      language: en      timeout: 300    whispercpp:      type: command      command: "whisper-cli -m ~/models/ggml-large-v3.bin -f {input_path} -otxt -of {output_dir}/transcript"      format: txt    sensevoice:      type: command      command: "sensevoice-cli {input_path} --json | tee {output_path}"      format: json
```

This complements the legacyHERMES_LOCAL_STT_COMMANDescape hatch — that env var still works untouched via the built-inlocal_commandpath. Usestt.providers.<name>when you wantmultipleshell-driven STT engines, a name you can pick viastt.provider, or anything that needs per-providerlanguage/model/timeout.

`HERMES_LOCAL_STT_COMMAND`
`local_command`
`stt.providers.<name>`
`stt.provider`
`language`
`model`
`timeout`

#### STT placeholders​

Your command template can reference these placeholders. Hermes substitutes them at render time and shell-quotes each value for the surrounding context (bare / single-quoted / double-quoted), so paths with spaces are safe.

| Placeholder | Meaning |
| --- | --- |
| {input_path} | Absolute path to the input audio file (original location, read-only) |
| {output_path} | Absolute path the command should write the transcript to |
| {output_dir} | Parent directory of{output_path}(handy for whisper-style tools) |
| {format} | Configured output format:txt/json/srt/vtt |
| {language} | Configured language code (defaults toen) |
| {model} | stt.providers.<name>.model, empty when unset |

`{input_path}`
`{output_path}`
`{output_dir}`
`{output_path}`
`{format}`
`txt`
`json`
`srt`
`vtt`
`{language}`
`en`
`{model}`
`stt.providers.<name>.model`

Use{{and}}for literal braces (handy when embedding JSON snippets in the command).

`{{`
`}}`

#### How the transcript is read back​

After your command exits successfully:

1. If{output_path}exists and is non-empty → Hermes reads it as UTF-8 text.
2. Otherwise, if the command wrote to stdout → Hermes uses that.
3. Otherwise → error: "Command STT provider wrote no output file and produced no stdout".

`{output_path}`

This lets you use the registry for both file-writing CLIs (whisper-cli,parakeet-asr) and curl-style one-liners that emit transcript to stdout (curl … | jq -r .text).

`whisper-cli`
`parakeet-asr`
`curl … | jq -r .text`

Forformat: json/srt/vtt, Hermes returns the raw file content as thetranscriptfield. Extracting.textfrom JSON is out of scope for the runner — either configureformat: txt, or post-process JSON downstream.

`format: json`
`srt`
`vtt`
`transcript`
`.text`
`format: txt`

#### STT command-provider optional keys​

| Key | Default | Meaning |
| --- | --- | --- |
| timeout | 300 | Seconds; the process tree is killed on expiry (Unixstart_new_session, Windowstaskkill /T). |
| format | txt | One oftxt/json/srt/vtt. Sets the extension of{output_path}. |
| language | en | Forwarded to{language}. Defaults tostt.languagethenen. |
| model | empty | Forwarded to{model}. Themodel=argument totranscribe_audio()overrides this. |

`timeout`
`300`
`start_new_session`
`taskkill /T`
`format`
`txt`
`txt`
`json`
`srt`
`vtt`
`{output_path}`
`language`
`en`
`{language}`
`stt.language`
`en`
`model`
`{model}`
`model=`
`transcribe_audio()`

#### STT command-provider behavior notes​

- Built-ins always win.Declaringstt.providers.openai: type: commanddoes NOT override the real OpenAI Whisper handler. The built-in name is short-circuited before the command-provider resolver runs.
- Process-tree cleanup.A command running overtimeouthas its entire process tree killed, not just the shell wrapper. Long-running ASR pipelines that fork model-loading subprocesses are reaped reliably.
- Shell-quoting is automatic.Placeholders inside'…'get single-quote-safe escaping; inside"…"get$/`/"escaping; outside quotes getshlex.quote. Don't pre-quote placeholder values.

`stt.providers.openai: type: command`
`timeout`
`'…'`
`"…"`
`$`
```
`"`
`shlex.quote`

#### STT command-provider security​

The shell command runs under the same user as Hermes with full filesystem access — same trust model astts.providers.<name>: type: commandandHERMES_LOCAL_STT_COMMAND. Only declare command providers from sources you trust.

`tts.providers.<name>: type: command`
`HERMES_LOCAL_STT_COMMAND`

### Python plugin providers (STT)​

For STT engines that aren't built-in AND can't be expressed as a shell command (need a Python SDK, OAuth-refreshing auth, streaming chunks, etc.), register a Python plugin viactx.register_transcription_provider(). The plugincoexists withthe 6 built-in providers (local,local_command,groq,openai,mistral,xai) and thestt.providers.<name>: type: commandregistry — built-ins keep their native implementations and always win on name collision; command providers win over plugins of the same name (config is more local than plugin install).

`ctx.register_transcription_provider()`
`local`
`local_command`
`groq`
`openai`
`mistral`
`xai`
`stt.providers.<name>: type: command`

#### When to pick which (STT)​

| Backend has… | Use |
| --- | --- |
| A single shell command that takes an audio file and emits text | stt.providers.<name>: type: command(no Python needed) |
| Only the legacy single-command escape hatch is wanted | HERMES_LOCAL_STT_COMMANDenv var (preserved for back-compat) |
| A Python SDK with no CLI | register_transcription_provider()plugin |
| OAuth-refreshing auth, streaming chunks, voice-list metadata | register_transcription_provider()plugin |
| A built-in already covers it (local,groq,openai, …) | Setstt.provider: <name>— built-ins are inline |

`stt.providers.<name>: type: command`
`HERMES_LOCAL_STT_COMMAND`
`register_transcription_provider()`
`register_transcription_provider()`
`local`
`groq`
`openai`
`stt.provider: <name>`

#### Resolution order​

1. stt.provideris a built-in name→ built-in dispatch.Always wins.
2. stt.providermatchesstt.providers.<name>withcommand:set→ command-provider runner (seeSTT custom command providers). Wins over a same-name plugin.
3. stt.providermatches a plugin-registeredTranscriptionProvider→ plugin dispatch:if the plugin'sis_available()returnsFalse(missing creds or SDK), the call surfaces an unavailability error envelope identifying the plugin —notthe generic "No STT provider available" message.otherwise the plugin'stranscribe()is called withmodel(from the publicmodel=arg, falling back tostt.<provider>.model) andlanguage(fromstt.<provider>.language).
4. No match→ "No STT provider available" error.

`stt.provider`
`stt.provider`
`stt.providers.<name>`
`command:`
`stt.provider`
`TranscriptionProvider`
- if the plugin'sis_available()returnsFalse(missing creds or SDK), the call surfaces an unavailability error envelope identifying the plugin —notthe generic "No STT provider available" message.
- otherwise the plugin'stranscribe()is called withmodel(from the publicmodel=arg, falling back tostt.<provider>.model) andlanguage(fromstt.<provider>.language).

`is_available()`
`False`
`transcribe()`
`model`
`model=`
`stt.<provider>.model`
`language`
`stt.<provider>.language`

#### Per-provider config namespace​

Plugins read their per-provider configuration fromstt.<provider>inconfig.yaml, mirroring how built-ins readstt.openai.model/stt.mistral.model:

`stt.<provider>`
`config.yaml`
`stt.openai.model`
`stt.mistral.model`

```
stt:  provider: my-stt  my-stt:    model: whisper-large-v3    language: ja          # forwarded as language= to transcribe()    # any other plugin-specific keys go here; read them via your    # own config.yaml access in __init__/is_available/transcribe
```

The dispatcher forwardsmodelandlanguagefrom this section; everything else, the plugin can read itself.

`model`
`language`

#### Minimal plugin​

Drop this in~/.hermes/plugins/my-stt/:

`~/.hermes/plugins/my-stt/`

plugin.yaml:

`plugin.yaml`

```
name: my-sttversion: 0.1.0description: "My custom Python STT backend"
```

__init__.py:

`__init__.py`

```
from agent.transcription_provider import TranscriptionProviderclass MySTTProvider(TranscriptionProvider):    @property    def name(self) -> str:        return "my-stt"  # what stt.provider matches against    @property    def display_name(self) -> str:        return "My Custom STT"    def is_available(self) -> bool:        # Return False when credentials/deps are missing — picker skips        # this row but the dispatcher still routes here on explicit config.        import os        return bool(os.environ.get("MY_STT_API_KEY"))    def transcribe(self, file_path, *, model=None, language=None, **extra):        # Return the standard transcribe envelope:        #   {"success": bool, "transcript": str, "provider": str, "error": str}        # Do NOT raise — convert exceptions to the error envelope so the        # gateway/CLI caller sees a consistent shape on failure.        try:            import my_stt_sdk            client = my_stt_sdk.Client()            text = client.transcribe(open(file_path, "rb"))            return {                "success": True,                "transcript": text,                "provider": "my-stt",            }        except Exception as exc:            return {                "success": False,                "transcript": "",                "error": f"my-stt failed: {exc}",                "provider": "my-stt",            }def register(ctx):    ctx.register_transcription_provider(MySTTProvider())
```

Enable it (hermes plugins enable my-stt), setstt.provider: my-sttinconfig.yaml, and voice-message transcription will route through your plugin.

`hermes plugins enable my-stt`
`stt.provider: my-stt`
`config.yaml`

#### Optional hooks​

Override these on your provider class for richer integration:

- list_models()→ list of{id, display, languages, max_audio_seconds}dicts.
- default_model()→ string returned when the user doesn't override the model.
- get_setup_schema()→ return{name, badge, tag, env_vars: [{key, prompt, url}]}to power picker rows inhermes tools/hermes setup(the picker category for STT is not yet shipped — this metadata is available to plugins for forward compatibility).

`list_models()`
`{id, display, languages, max_audio_seconds}`
`default_model()`
`get_setup_schema()`
`{name, badge, tag, env_vars: [{key, prompt, url}]}`
`hermes tools`
`hermes setup`

Seeagent/transcription_provider.pyfor the full ABC including docstrings.

`agent/transcription_provider.py`