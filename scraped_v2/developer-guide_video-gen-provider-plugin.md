- 
- Developer Guide
- Extending
- Plugins
- Video Generation Provider Plugins

# Building a Video Generation Provider Plugin

Video-gen provider plugins register a backend that services everyvideo_generatetool call. Built-in providers (xAI, FAL) ship as plugins. Add a new one, or override a bundled one, by dropping a directory intoplugins/video_gen/<name>/.

`video_generate`
`plugins/video_gen/<name>/`

Video-gen mirrorsImage Generation Provider Pluginsalmost line-for-line — if you've built an image-gen backend, you already know the shape. The main differences: acapabilities()method advertising modalities/aspect-ratios/durations, and a routing convention (passimage_urlto use image-to-video, omit it to use text-to-video — the provider picks the right endpoint internally).

`capabilities()`
`image_url`

## The unified surface (one tool, two modalities)​

Thevideo_generatetool exposes two modalities through one parameter:

`video_generate`
- Text-to-video— call withpromptonly. The provider routes to its text-to-video endpoint.
- Image-to-video— call withprompt+image_url. The provider routes to its image-to-video endpoint.

`prompt`
`prompt`
`image_url`

Edit and extend are intentionally out of scope. Most backends don't support them and the inconsistency would force per-backend prose into the agent's tool description.

## How discovery works​

Hermes scans for video-gen backends in three places:

1. Bundled—<repo>/plugins/video_gen/<name>/(auto-loaded withkind: backend)
2. User—~/.hermes/plugins/video_gen/<name>/(opt-in viaplugins.enabled)
3. Pip— packages declaring ahermes_agent.pluginsentry point

`<repo>/plugins/video_gen/<name>/`
`kind: backend`
`~/.hermes/plugins/video_gen/<name>/`
`plugins.enabled`
`hermes_agent.plugins`

Each plugin'sregister(ctx)function callsctx.register_video_gen_provider(...). The active provider is picked byvideo_gen.providerinconfig.yaml;hermes tools→ Video Generation walks users through selection. Unlikeimage_generate, there is no in-tree legacy backend — every provider is a plugin.

`register(ctx)`
`ctx.register_video_gen_provider(...)`
`video_gen.provider`
`config.yaml`
`hermes tools`
`image_generate`

## Directory structure​

```
plugins/video_gen/my-backend/├── __init__.py      # VideoGenProvider subclass + register()└── plugin.yaml      # Manifest with kind: backend
```

## The VideoGenProvider ABC​

Subclassagent.video_gen_provider.VideoGenProvider. Required:nameproperty andgenerate()method.

`agent.video_gen_provider.VideoGenProvider`
`name`
`generate()`

```
# plugins/video_gen/my-backend/__init__.pyfrom typing import Any, Dict, List, Optionalimport osfrom agent.video_gen_provider import (    VideoGenProvider,    error_response,    success_response,)class MyVideoGenProvider(VideoGenProvider):    @property    def name(self) -> str:        return "my-backend"    @property    def display_name(self) -> str:        return "My Backend"    def is_available(self) -> bool:        return bool(os.environ.get("MY_API_KEY"))    def list_models(self) -> List[Dict[str, Any]]:        # Each entry is a model FAMILY — a name the user picks once.        # Your provider's generate() routes within the family based on        # whether image_url was passed.        return [            {                "id": "fast",                "display": "Fast",                "speed": "~30s",                "strengths": "Cheapest tier",                "price": "$0.05/s",                "modalities": ["text", "image"],  # advisory            },        ]    def default_model(self) -> Optional[str]:        return "fast"    def capabilities(self) -> Dict[str, Any]:        return {            "modalities": ["text", "image"],            "aspect_ratios": ["16:9", "9:16"],            "resolutions": ["720p", "1080p"],            "min_duration": 1,            "max_duration": 10,            "supports_audio": False,            "supports_negative_prompt": True,            "max_reference_images": 0,        }    def get_setup_schema(self) -> Dict[str, Any]:        return {            "name": "My Backend",            "badge": "paid",            "tag": "Short description shown in `hermes tools`",            "env_vars": [                {                    "key": "MY_API_KEY",                    "prompt": "My Backend API key",                    "url": "https://mybackend.example.com/keys",                },            ],        }    def generate(        self,        prompt: str,        *,        model: Optional[str] = None,        image_url: Optional[str] = None,        reference_image_urls: Optional[List[str]] = None,        duration: Optional[int] = None,        aspect_ratio: str = "16:9",        resolution: str = "720p",        negative_prompt: Optional[str] = None,        audio: Optional[bool] = None,        seed: Optional[int] = None,        **kwargs: Any,  # always ignore unknown kwargs for forward-compat    ) -> Dict[str, Any]:        # ROUTE: image_url presence picks the endpoint.        if image_url:            endpoint = "my-backend/image-to-video"            modality_used = "image"        else:            endpoint = "my-backend/text-to-video"            modality_used = "text"        # ... call your API ...        return success_response(            video="https://your-cdn/output.mp4",            model=model or "fast",            prompt=prompt,            modality=modality_used,            aspect_ratio=aspect_ratio,            duration=duration or 5,            provider=self.name,        )def register(ctx) -> None:    ctx.register_video_gen_provider(MyVideoGenProvider())
```

## The plugin manifest​

```
# plugins/video_gen/my-backend/plugin.yamlname: my-backendversion: 1.0.0description: "My video generation backend"author: Your Namekind: backendrequires_env:  - MY_API_KEY
```

## Thevideo_generateschema​

`video_generate`

The tool exposes one schema across every backend. Providers ignore parameters they don't support.

| Parameter | What it does |
| --- | --- |
| prompt | Text instruction (required) |
| image_url | When set → image-to-video; when omitted → text-to-video |
| reference_image_urls | Style/character refs (provider-dependent) |
| duration | Seconds — provider clamps |
| aspect_ratio | "16:9","9:16","1:1", ... — provider clamps |
| resolution | "480p"/"540p"/"720p"/"1080p"— provider clamps |
| negative_prompt | Content to avoid (Pixverse/Kling only) |
| audio | Native audio (Veo3 / Pixverse pricing tier) |
| seed | Reproducibility |
| model | Override the active model/family |

`prompt`
`image_url`
`reference_image_urls`
`duration`
`aspect_ratio`
`"16:9"`
`"9:16"`
`"1:1"`
`resolution`
`"480p"`
`"540p"`
`"720p"`
`"1080p"`
`negative_prompt`
`audio`
`seed`
`model`

The provider'scapabilities()advertises which of these are honored. The agent sees the active backend's capabilities in the tool description, dynamically rebuilt when the user changes backend viahermes tools.

`capabilities()`
`hermes tools`

## Model families and endpoint routing (the FAL pattern)​

When your backend has multiple endpoints per "model" — like FAL, where every family (Veo 3.1, Pixverse v6, Kling O3) has both a/text-to-videoand an/image-to-videoURL — represent eachfamilyas one catalog entry. Yourgenerate()picks the right endpoint based on whetherimage_urlwas passed:

`/text-to-video`
`/image-to-video`
`generate()`
`image_url`

```
FAMILIES = {    "veo3.1": {        "text_endpoint": "fal-ai/veo3.1",        "image_endpoint": "fal-ai/veo3.1/image-to-video",        # ... family-specific capability flags ...    },}def generate(self, prompt, *, image_url=None, model=None, **kwargs):    family_id, family = _resolve_family(model)    endpoint = family["image_endpoint"] if image_url else family["text_endpoint"]    # ... build payload from family's declared capability flags, call endpoint ...
```

The user picksveo3.1once inhermes tools. The agent never thinks about endpoints — it just passes (or doesn't pass)image_url.

`veo3.1`
`hermes tools`
`image_url`

## Selection precedence​

For per-instance model knobs (seeplugins/video_gen/fal/__init__.py):

`plugins/video_gen/fal/__init__.py`
1. model=keyword from the tool call
2. <PROVIDER>_VIDEO_MODELenv var
3. video_gen.<provider>.modelinconfig.yaml
4. video_gen.modelinconfig.yaml(when it's one of your IDs)
5. Provider'sdefault_model()

`model=`
`<PROVIDER>_VIDEO_MODEL`
`video_gen.<provider>.model`
`config.yaml`
`video_gen.model`
`config.yaml`
`default_model()`

## Response shape​

success_response()anderror_response()produce the dict shape every backend returns. Use them — don't hand-roll the dict.

`success_response()`
`error_response()`

Success keys:success,video(URL or absolute path),model,prompt,modality("text"or"image"),aspect_ratio,duration,provider, plusextra.

`success`
`video`
`model`
`prompt`
`modality`
`"text"`
`"image"`
`aspect_ratio`
`duration`
`provider`
`extra`

Error keys:success,video(None),error,error_type,model,prompt,aspect_ratio,provider.

`success`
`video`
`error`
`error_type`
`model`
`prompt`
`aspect_ratio`
`provider`

## Where to save artifacts​

If your backend returns base64, usesave_b64_video()to write under$HERMES_HOME/cache/videos/. For raw bytes from a follow-up HTTP fetch, usesave_bytes_video(). Otherwise return the upstream URL directly — the gateway resolves remote URLs on delivery.

`save_b64_video()`
`$HERMES_HOME/cache/videos/`
`save_bytes_video()`

## Testing​

Drop a smoke test undertests/plugins/video_gen/test_<name>_plugin.py. The xAI and FAL tests show the pattern — register, verify catalog, exercise routing both with and withoutimage_url, assert clean error responses on missing auth.

`tests/plugins/video_gen/test_<name>_plugin.py`
`image_url`