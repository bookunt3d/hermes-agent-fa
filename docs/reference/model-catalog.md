---
layout: docs
title: "کاتالوگ مدل‌ها"
permalink: /docs/reference/model-catalog/
---

- 
- Reference
- Configuration Reference
- Model Catalog

# Model Catalog

Hermes fetches curated model lists forOpenRouterandNous Portalfrom a JSON manifest hosted alongside the docs site. This lets maintainers update picker lists without shipping a newhermes-agentrelease.

`hermes-agent`

When the manifest is unreachable (offline, network blocked, hosting failure), Hermes silently falls back to the in-repo snapshot that ships with the CLI. The manifest never breaks the picker — worst case you see whatever list was bundled with your installed version.

## Live manifest URL​

```
https://hermes-agent.nousresearch.com/docs/api/model-catalog.json
```

Published on every merge tomainvia the existingdeploy-site.ymlGitHub Pages pipeline. The source of truth lives in the repo atwebsite/static/api/model-catalog.json.

`main`
`deploy-site.yml`
`website/static/api/model-catalog.json`

## Schema​

```
{  "version": 1,  "updated_at": "2026-04-25T22:00:00Z",  "metadata": {},  "providers": {    "openrouter": {      "metadata": {},      "models": [        {"id": "moonshotai/kimi-k2.6", "description": "recommended", "metadata": {}},        {"id": "openai/gpt-5.4",       "description": ""}      ]    },    "nous": {      "metadata": {},      "models": [        {"id": "anthropic/claude-opus-4.7"},        {"id": "moonshotai/kimi-k2.6"}      ]    }  }}
```

Field notes:

- version— integer schema version. Future schemas bump this; Hermes refuses manifests with versions it doesn't understand and falls back to the hardcoded snapshot.
- metadata— free-form dict at the manifest, provider, and model level. Any keys. Hermes ignores unknown fields, so you can annotate entries ("tier": "paid","tags": [...], etc.) without coordinating a schema change.
- description— OpenRouter-only. Drives picker badge text ("recommended","free", or empty). Nous Portal doesn't use this — free-tier gating is determined live from the Portal's pricing endpoint.
- Pricing and context lengthare NOT in the manifest. Those come from live provider APIs (/v1/modelsendpoints, models.dev) at fetch time.

`version`
`metadata`
`"tier": "paid"`
`"tags": [...]`
`description`
`"recommended"`
`"free"`
`/v1/models`

## Fetch behavior​

| When | What happens |
| --- | --- |
| /modelorhermes model | Fetches if disk cache is stale, else uses cache |
| Disk cache fresh (< TTL) | No network hit |
| Network failure with cache | Silent fallback to cache, one log line |
| Network failure, no cache | Silent fallback to in-repo snapshot |
| Manifest fails schema validation | Treated as unreachable |

`/model`
`hermes model`

Cache location:~/.hermes/cache/model_catalog.json.

`~/.hermes/cache/model_catalog.json`

## Config​

```
model_catalog:  enabled: true  url: https://hermes-agent.nousresearch.com/docs/api/model-catalog.json  ttl_hours: 1  providers: {}
```

Setenabled: falseto disable remote fetch entirely and always use the in-repo snapshot.

`enabled: false`

### Per-provider override URLs​

Third parties can self-host their own curation list using the same schema. Point a provider at a custom URL:

```
model_catalog:  providers:    openrouter:      url: https://example.com/my-openrouter-curation.json
```

The overriding manifest only needs to populate the provider block(s) it cares about. Other providers continue to resolve against the master URL.

## Updating the manifest​

Maintainers:

```
# Re-generate from the in-repo hardcoded lists (keeps manifest in sync after# editing OPENROUTER_MODELS or _PROVIDER_MODELS["nous"] in hermes_cli/models.py).python scripts/build_model_catalog.py
```

Then PR the resulting change towebsite/static/api/model-catalog.jsontomain. The docs site auto-deploys on merge and the new manifest is live within a few minutes.

`website/static/api/model-catalog.json`
`main`

You can also hand-edit the JSON directly for fine-grained metadata changes that don't belong in the in-repo snapshot — the generator script is a convenience, not the single source of truth.