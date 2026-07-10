---
layout: docs
title: "Google Vertex"
permalink: /docs/guides/google-vertex/
---

- 
- Guides & Tutorials
- Google Vertex AI

# Google Vertex AI

Hermes Agent supportsGemini models on Google Cloud Vertex AIthrough Vertex's OpenAI-compatible endpoint. Unlike theGoogle AI Studio provider(which uses a static API key againstgenerativelanguage.googleapis.com), Vertex gives youenterprise-grade rate limits and GCP billing/credits, and is the right choice when you want Gemini usage to draw on your Google Cloud account rather than an AI Studio key.

`generativelanguage.googleapis.com`

Vertex hasno static API keyfor the standard endpoint. Every request needs a short-livedOAuth2 access token(≈1 hour TTL) minted from either a service-account JSON or Application Default Credentials (ADC). Hermes mints andauto-refreshesthese tokens for you — you never paste a token by hand. This is why pasting a temporary token into a custom provider'sapi_keyfield does not work: it expires mid-session.

`api_key`

## Prerequisites​

- A Google Cloud projectwith theVertex AI API enabledand billing active.
- Credentials, one of:aservice-account JSONkey file with theroles/aiplatform.userrole, orApplication Default Credentialsviagcloud auth application-default login(or the metadata server when running on a GCP VM).
- google-auth— installed automatically the first time you select Vertex (lazy install), or explicitly withpip install 'hermes-agent[vertex]'.

- aservice-account JSONkey file with theroles/aiplatform.userrole, or
- Application Default Credentialsviagcloud auth application-default login(or the metadata server when running on a GCP VM).

`roles/aiplatform.user`
`gcloud auth application-default login`
`google-auth`
`pip install 'hermes-agent[vertex]'`

## Quick Start​

```
# Option A — service account JSON (recommended for servers / gateways)echo "VERTEX_CREDENTIALS_PATH=/path/to/service-account.json" >> ~/.hermes/.env# Option B — Application Default Credentials (good for local dev)gcloud auth application-default login# Select Vertex as your providerhermes model# → Choose "More providers..." → "Google Vertex AI"# → Enter your GCP project ID (or leave blank to use the one in your credentials)# → Choose a region (default: global)# → Select a Gemini model# Start chattinghermes chat
```

## Configuration​

Vertex splits its settings by sensitivity:

- Thecredential pathis a pointer to a secret and lives in~/.hermes/.env.
- Project ID and regionare non-secret routing settings and live in~/.hermes/config.yaml.

`~/.hermes/.env`
`~/.hermes/config.yaml`

~/.hermes/.env:

`~/.hermes/.env`

```
# One of these (checked in this order); omit both to use ADC:VERTEX_CREDENTIALS_PATH=/path/to/service-account.jsonGOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

~/.hermes/config.yaml:

`~/.hermes/config.yaml`

```
model:  default: google/gemini-3-flash-preview  provider: vertexvertex:  project_id: my-gcp-project   # blank → use the project embedded in the credentials  region: global               # "global" is required for the Gemini 3.x previews
```

VERTEX_PROJECT_IDandVERTEX_REGIONoverride thevertex.project_id/vertex.regionvalues inconfig.yaml. Use them for per-shell overrides; keep the durable settings inconfig.yaml.

`VERTEX_PROJECT_ID`
`VERTEX_REGION`
`vertex.project_id`
`vertex.region`
`config.yaml`
`config.yaml`

### How authentication works​

1. Hermes resolves credentials in this order:VERTEX_CREDENTIALS_PATH→GOOGLE_APPLICATION_CREDENTIALS→ ADC.
2. It mints an OAuth2 access token (cloud-platformscope) and caches it, refreshing when the token is within 5 minutes of expiry.
3. The token is handed to a standard OpenAI client pointed at the Vertex endpoint:https://aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{region}/endpoints/openapiRegional locations use a{region}-aiplatform.googleapis.comhost instead.
4. If a session runs longer than the token lifetime and a request returns401, Hermes re-mints the token and retries automatically. On a long-running gateway, if ADC's refresh token has itself expired, Hermes falls back to the service-account JSON when one is configured.

`VERTEX_CREDENTIALS_PATH`
`GOOGLE_APPLICATION_CREDENTIALS`
`cloud-platform`

```
https://aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{region}/endpoints/openapi
```

`{region}-aiplatform.googleapis.com`
`401`

## Available Models​

Vertex requires thegoogle/vendor prefix on model IDs. Thehermes modelpicker offers:

`google/`
`hermes model`
| Model | ID |
| --- | --- |
| Gemini 3.1 Pro Preview | google/gemini-3.1-pro-preview |
| Gemini 3 Pro Preview | google/gemini-3-pro-preview |
| Gemini 3 Flash Preview | google/gemini-3-flash-preview |
| Gemini 3.1 Flash Lite Preview | google/gemini-3.1-flash-lite-preview |
| Gemini 2.5 Pro | google/gemini-2.5-pro |
| Gemini 2.5 Flash | google/gemini-2.5-flash |

`google/gemini-3.1-pro-preview`
`google/gemini-3-pro-preview`
`google/gemini-3-flash-preview`
`google/gemini-3.1-flash-lite-preview`
`google/gemini-2.5-pro`
`google/gemini-2.5-flash`
`global`

The Gemini 3.x preview models are served through theglobalendpoint. Regional endpoints (us-central1, etc.) may 404 them. Leaveregion: globalunless you have a specific reason to pin a region.

`global`
`us-central1`
`region: global`

## Switching Models Mid-Session​

```
/model google/gemini-3-pro-preview/model google/gemini-3-flash-preview
```

/modelswitches among already-configured providers and models; it does not collect new credentials. Configure Vertex withhermes modelfirst.

`/model`
`hermes model`

## Reasoning / Thinking​

Vertex exposes Gemini's thinking budget through the OpenAI-compatible surface. Hermes maps its reasoning-effort setting ontoextra_body.google.thinking_configautomatically, soreasoning_effortworks the same way it does on other Gemini surfaces.

`extra_body.google.thinking_config`
`reasoning_effort`

## Diagnostics​

```
hermes doctor
```

The doctor reports whether Vertex credentials can be resolved (service-account path or ADC) and whether the provider is configured.

## Troubleshooting​

### "Vertex AI credentials could not be resolved"​

Hermes found neither a service-account JSON nor working ADC. Either setVERTEX_CREDENTIALS_PATHin~/.hermes/.env, or rungcloud auth application-default login. If your project isn't embedded in the credentials, setvertex.project_idinconfig.yaml.

`VERTEX_CREDENTIALS_PATH`
`~/.hermes/.env`
`gcloud auth application-default login`
`vertex.project_id`
`config.yaml`

### google-authnot installed​

`google-auth`

Install the extra:pip install 'hermes-agent[vertex]'. Hermes also lazy-installs it the first time you select the Vertex provider.

`pip install 'hermes-agent[vertex]'`

### 404 on Gemini 3.x models​

You are probably on a regional endpoint. Setregion: globalin thevertex:section ofconfig.yaml(or unsetVERTEX_REGION).

`region: global`
`vertex:`
`config.yaml`
`VERTEX_REGION`

### 403 / permission denied​

The service account (or your ADC identity) needs theroles/aiplatform.userrole on the project, and the Vertex AI API must be enabled for that project.

`roles/aiplatform.user`

## Related​

- Google Gemini (AI Studio)— static-API-key Gemini without GCP
- AWS Bedrock— another native cloud-provider integration
- AI Providers
- Configuration