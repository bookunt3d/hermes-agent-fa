- 
- Developer Guide
- Extending
- Plugins
- Image Generation Provider Plugins

# Building an Image Generation Provider Plugin

Image-gen provider plugins register a backend that services everyimage_generatetool call — DALL·E, gpt-image, Grok, Flux, Imagen, Stable Diffusion, fal, Replicate, a local ComfyUI rig, anything. Built-in providers (OpenAI, OpenAI-Codex, xAI) all ship as plugins. You can add a new one, or override a bundled one, by dropping a directory intoplugins/image_gen/<name>/.

`image_generate`
`plugins/image_gen/<name>/`

Image-gen is one of severalbackend pluginsHermes supports. The others (with more specialized ABCs) areMemory Provider Plugins,Context Engine Plugins, andModel Provider Plugins. General tool/hook/CLI plugins live inBuild a Hermes Plugin.

## How discovery works​

Hermes scans for image-gen backends in three places:

1. Bundled—<repo>/plugins/image_gen/<name>/(auto-loaded withkind: backend, always available)
2. User—~/.hermes/plugins/image_gen/<name>/(opt-in viaplugins.enabled)
3. Pip— packages declaring ahermes_agent.pluginsentry point

`<repo>/plugins/image_gen/<name>/`
`kind: backend`
`~/.hermes/plugins/image_gen/<name>/`
`plugins.enabled`
`hermes_agent.plugins`

Each plugin'sregister(ctx)function callsctx.register_image_gen_provider(...)— that puts it into the registry inagent/image_gen_registry.py. The active provider is picked byimage_gen.providerinconfig.yaml;hermes toolswalks users through selection.

`register(ctx)`
`ctx.register_image_gen_provider(...)`
`agent/image_gen_registry.py`
`image_gen.provider`
`config.yaml`
`hermes tools`

Theimage_generatetool wrapper asks the registry for the active provider and dispatches there. If no provider is registered, the tool surfaces a helpful error pointing athermes tools.

`image_generate`
`hermes tools`

## Directory structure​

```
plugins/image_gen/my-backend/├── __init__.py      # ImageGenProvider subclass + register()└── plugin.yaml      # Manifest with kind: backend
```

A bundled plugin is complete at this point. User plugins at~/.hermes/plugins/image_gen/<name>/need to be added toplugins.enabledinconfig.yaml(or runhermes plugins enable <name>).

`~/.hermes/plugins/image_gen/<name>/`
`plugins.enabled`
`config.yaml`
`hermes plugins enable <name>`

## The ImageGenProvider ABC​

Subclassagent.image_gen_provider.ImageGenProvider. The only required members are thenameproperty and thegenerate()method — everything else has sane defaults:

`agent.image_gen_provider.ImageGenProvider`
`name`
`generate()`

```
# plugins/image_gen/my-backend/__init__.pyfrom typing import Any, Dict, List, Optionalimport osfrom agent.image_gen_provider import (    DEFAULT_ASPECT_RATIO,    ImageGenProvider,    error_response,    normalize_reference_images,    resolve_aspect_ratio,    save_b64_image,    success_response,)class MyBackendImageGenProvider(ImageGenProvider):    @property    def name(self) -> str:        # Stable id used in image_gen.provider config. Lowercase, no spaces.        return "my-backend"    @property    def display_name(self) -> str:        # Human label shown in `hermes tools`. Defaults to name.title() if omitted.        return "My Backend"    def is_available(self) -> bool:        # Return False if credentials or deps are missing.        # The tool's availability gate calls this before dispatch.        if not os.environ.get("MY_BACKEND_API_KEY"):            return False        try:            import my_backend_sdk  # noqa: F401        except ImportError:            return False        return True    def list_models(self) -> List[Dict[str, Any]]:        # Catalog shown in `hermes tools` model picker.        return [            {                "id": "my-model-fast",                "display": "My Model (Fast)",                "speed": "~5s",                "strengths": "Quick iteration",                "price": "$0.01/image",            },            {                "id": "my-model-hq",                "display": "My Model (HQ)",                "speed": "~30s",                "strengths": "Highest fidelity",                "price": "$0.04/image",            },        ]    def default_model(self) -> Optional[str]:        return "my-model-fast"    def get_setup_schema(self) -> Dict[str, Any]:        # Metadata for the `hermes tools` picker — keys to prompt for at setup.        return {            "name": "My Backend",            "badge": "paid",        # optional; shown as a short tag in the picker            "tag": "One-line description shown under the name",            "env_vars": [                {                    "key": "MY_BACKEND_API_KEY",                    "prompt": "My Backend API key",                    "url": "https://my-backend.example.com/api-keys",                },            ],        }    def capabilities(self) -> Dict[str, Any]:        # Declare whether this backend supports image-to-image / editing.        # The tool layer surfaces this in the dynamic schema so the model        # knows when `image_url` is honored. Default (if you omit this) is        # text-only: {"modalities": ["text"], "max_reference_images": 0}.        return {"modalities": ["text", "image"], "max_reference_images": 4}    def generate(        self,        prompt: str,        aspect_ratio: str = DEFAULT_ASPECT_RATIO,        *,        image_url: Optional[str] = None,        reference_image_urls: Optional[List[str]] = None,        **kwargs: Any,    ) -> Dict[str, Any]:        prompt = (prompt or "").strip()        aspect_ratio = resolve_aspect_ratio(aspect_ratio)        if not prompt:            return error_response(                error="Prompt is required",                error_type="invalid_input",                provider=self.name,                prompt="",                aspect_ratio=aspect_ratio,            )        # Routing: if image_url (or reference_image_urls) is set, the call is        # an image-to-image / edit request; otherwise text-to-image. Report        # which path you took via the `modality` field of success_response.        sources = []        if image_url:            sources.append(image_url)        sources.extend(normalize_reference_images(reference_image_urls) or [])        modality = "image" if sources else "text"        # Model selection precedence: env var → config → default. The helper        # _resolve_model() in the built-in openai plugin is a good reference.        model_id = kwargs.get("model") or self.default_model() or "my-model-fast"        try:            import my_backend_sdk            client = my_backend_sdk.Client(api_key=os.environ["MY_BACKEND_API_KEY"])            if modality == "image":                result = client.edit(                    prompt=prompt,                    model=model_id,                    image_urls=sources,                )            else:                result = client.generate(                    prompt=prompt,                    model=model_id,                    aspect_ratio=aspect_ratio,                )            # Two shapes supported:            #   - URL string: return it as `image`            #   - base64 data: save under $HERMES_HOME/cache/images/ via save_b64_image()            if result.get("image_b64"):                path = save_b64_image(                    result["image_b64"],                    prefix=self.name,                    extension="png",                )                image = str(path)            else:                image = result["image_url"]            return success_response(                image=image,                model=model_id,                prompt=prompt,                aspect_ratio=aspect_ratio,                provider=self.name,                modality=modality,            )        except Exception as exc:            return error_response(                error=str(exc),                error_type=type(exc).__name__,                provider=self.name,                model=model_id,                prompt=prompt,                aspect_ratio=aspect_ratio,            )def register(ctx) -> None:    """Plugin entry point — called once at load time."""    ctx.register_image_gen_provider(MyBackendImageGenProvider())
```

## plugin.yaml​

```
name: my-backendversion: 1.0.0description: My image backend — text-to-image via My Backend SDKauthor: Your Namekind: backendrequires_env:  - MY_BACKEND_API_KEY
```

kind: backendis what routes the plugin to the image-gen registration path.requires_envis prompted duringhermes plugins install.

`kind: backend`
`requires_env`
`hermes plugins install`

## ABC reference​

Full contract inagent/image_gen_provider.py. The methods you'll typically override:

`agent/image_gen_provider.py`
| Member | Required | Default | Purpose |
| --- | --- | --- | --- |
| name | ✅ | — | Stable id used inimage_gen.providerconfig |
| display_name | — | name.title() | Label shown inhermes tools |
| is_available() | — | True | Gate for missing creds/deps |
| list_models() | — | [] | Catalog forhermes toolsmodel picker |
| default_model() | — | first fromlist_models() | Fallback when no model is configured |
| get_setup_schema() | — | minimal | Picker metadata + env-var prompts |
| generate(prompt, aspect_ratio, **kwargs) | ✅ | — | The call |

`name`
`image_gen.provider`
`display_name`
`name.title()`
`hermes tools`
`is_available()`
`True`
`list_models()`
`[]`
`hermes tools`
`default_model()`
`list_models()`
`get_setup_schema()`
`generate(prompt, aspect_ratio, **kwargs)`

## Response format​

generate()must return a dict built viasuccess_response()orerror_response(). Both live inagent/image_gen_provider.py.

`generate()`
`success_response()`
`error_response()`
`agent/image_gen_provider.py`

Success:

```
success_response(    image=<url-or-absolute-path>,    model=<model-id>,    prompt=<echoed-prompt>,    aspect_ratio="landscape" | "square" | "portrait",    provider=<your-provider-name>,    extra={...},  # optional backend-specific fields)
```

Error:

```
error_response(    error="human-readable message",    error_type="provider_error" | "invalid_input" | "<exception class name>",    provider=<your-provider-name>,    model=<model-id>,    prompt=<prompt>,    aspect_ratio=<resolved aspect>,)
```

The tool wrapper JSON-serializes the dict and hands it to the LLM. Errors are surfaced as the tool result; the LLM decides how to explain them to the user.

## Handling base64 vs URL output​

Some backends return image URLs (fal, Replicate); others return base64 payloads (OpenAI gpt-image-2). For the base64 case, usesave_b64_image()— it writes to$HERMES_HOME/cache/images/<prefix>_<timestamp>_<uuid>.<ext>and returns the absolutePath. Pass that path (asstr) asimage=insuccess_response(). Gateway delivery (Telegram photo bubble, Discord attachment) recognizes both URLs and absolute paths.

`save_b64_image()`
`$HERMES_HOME/cache/images/<prefix>_<timestamp>_<uuid>.<ext>`
`Path`
`str`
`image=`
`success_response()`

## User overrides​

Drop a user plugin at~/.hermes/plugins/image_gen/<name>/with the samenameproperty as a bundled one and enable it viahermes plugins enable <name>— the registry is last-writer-wins, so your version replaces the built-in. Useful for pointing anopenaiplugin at a private proxy, or swapping in a custom model catalog.

`~/.hermes/plugins/image_gen/<name>/`
`name`
`hermes plugins enable <name>`
`openai`

## Testing​

```
export HERMES_HOME=/tmp/hermes-imggen-testmkdir -p $HERMES_HOME/plugins/image_gen/my-backend# …copy __init__.py + plugin.yaml into that dir…export MY_BACKEND_API_KEY=your-test-keyhermes plugins enable my-backend# Pick it as the active providerecho "image_gen:" >> $HERMES_HOME/config.yamlecho "  provider: my-backend" >> $HERMES_HOME/config.yaml# Exercise ithermes -z "Generate an image of a corgi in a spacesuit"
```

Or interactively:hermes tools→ "Image Generation" → selectmy-backend→ enter API key if prompted.

`hermes tools`
`my-backend`

## Reference implementations​

- plugins/image_gen/openai/__init__.py— gpt-image-2 at low/medium/high tiers as three virtual model IDs sharing one API model with differentqualityparams. Good example of tiered models under a single backend + config.yaml precedence chain.
- plugins/image_gen/xai/__init__.py— Grok Imagine via xAI. Different shape (URL output, simpler catalog).
- plugins/image_gen/openai-codex/__init__.py— Codex-style Responses API variant reusing the OpenAI SDK with a different routing base URL.

`plugins/image_gen/openai/__init__.py`
`quality`
`plugins/image_gen/xai/__init__.py`
`plugins/image_gen/openai-codex/__init__.py`

## Distribute via pip​

```
# pyproject.toml[project.entry-points."hermes_agent.plugins"]my-backend-imggen = "my_backend_imggen_package"
```

my_backend_imggen_packagemust expose a top-levelregisterfunction. SeeDistribute via pipin the general plugin guide for the full setup.

`my_backend_imggen_package`
`register`

## Related pages​

- Image Generation— user-facing feature documentation
- Plugins overview— all plugin types at a glance
- Build a Hermes Plugin— general tools/hooks/slash commands guide