---
layout: docs
title: "Features_X Search"
permalink: /docs/user-guide/features/x-search/
---

- 
- Features
- Media & Web
- X (Twitter) Search

# X (Twitter) Search

Thex_searchtool lets the agent search X (Twitter) posts, profiles, and threads directly. It's backed by xAI's built-inx_searchtool on the Responses API athttps://api.x.ai/v1/responses— Grok itself runs the search server-side and returns synthesized results with citations to the originating posts.

`x_search`
`x_search`
`https://api.x.ai/v1/responses`

Use this instead ofweb_searchwhen you specifically want current discussion, reactions, or claimson X. For general web pages, keep usingweb_search/web_extract.

`web_search`
`web_search`
`web_extract`

If you're paying Portal for an xAI model anyway, Live Search calls bill against the same xAI key configured for chat. SeeNous Portal.

## Authentication​

x_searchregisters wheneitherxAI credential path is available:

`x_search`
| Credential | Source | Setup |
| --- | --- | --- |
| SuperGrok / X Premium+ OAuth(preferred) | Browser login ataccounts.x.ai, refreshed automatically | hermes auth add xai-oauth— seexAI Grok OAuth (SuperGrok / X Premium+) |
| XAI_API_KEY | Paid xAI API key | Set in~/.hermes/.env |

`accounts.x.ai`
`hermes auth add xai-oauth`
`XAI_API_KEY`
`~/.hermes/.env`

Both hit the same endpoint with the same payload — the only difference is the bearer token.When both are configured, SuperGrok OAuth winsso x_search runs against your subscription quota instead of paid API spend.

The tool'scheck_fnruns the xAI credential resolver every time the model's tool list is rebuilt. ATruereturn means the bearer is fetchable AND non-empty AND (if it had expired) successfully refreshed. Revoked tokens with a failed refresh hide the tool from the schema; the model simply can't see it.

`check_fn`
`True`

## Enabling the tool​

Auto-enables when xAI credentials (OAuth token orXAI_API_KEY) are present. Disable explicitly viahermes tools→ Search → x_search if you don't want this.

`XAI_API_KEY`
`hermes tools`

```
hermes tools# → 🐦 X (Twitter) Search   (press space to toggle on)
```

The picker offers two credential choices:

1. xAI Grok OAuth (SuperGrok / Premium+)— opens the browser toaccounts.x.aiif you're not already logged in
2. xAI API key— prompts forXAI_API_KEY

`accounts.x.ai`
`XAI_API_KEY`

Either choice satisfies the gating. You can pick whichever credentials you already have; the tool works identically with both. If both end up configured, OAuth is preferred at call time.

## Configuration​

```
# ~/.hermes/config.yamlx_search:  # xAI model used for the Responses call.  # grok-4.20-reasoning is the recommended default; any Grok model  # with x_search tool access works.  model: grok-4.20-reasoning  # Request timeout in seconds. x_search can take 60–120s for  # complex queries — the default is generous. Minimum: 30.  timeout_seconds: 180  # Number of automatic retries on 5xx / ReadTimeout / ConnectionError.  # Each retry backs off (1.5x attempt seconds, capped at 5s).  retries: 2
```

## Tool parameters​

The agent callsx_searchwith these arguments:

`x_search`
| Parameter | Type | Description |
| --- | --- | --- |
| query | string (required) | What to look up on X. |
| allowed_x_handles | string array | Optional list of handles to includeexclusively(max 10). Leading@is stripped. |
| excluded_x_handles | string array | Optional list of handles to exclude (max 10). Mutually exclusive withallowed_x_handles. |
| from_date | string | OptionalYYYY-MM-DDstart date. |
| to_date | string | OptionalYYYY-MM-DDend date. |
| enable_image_understanding | boolean | Ask xAI to analyze images attached to matching posts. |
| enable_video_understanding | boolean | Ask xAI to analyze videos attached to matching posts. |

`query`
`allowed_x_handles`
`@`
`excluded_x_handles`
`allowed_x_handles`
`from_date`
`YYYY-MM-DD`
`to_date`
`YYYY-MM-DD`
`enable_image_understanding`
`enable_video_understanding`

The tool returns JSON with:

- answer— synthesized text response from Grok
- citations— citations returned by the Responses API top-level field
- inline_citations—url_citationannotations extracted from the message body (each withurl,title,start_index,end_index)
- degraded—truewhen any narrowing filter (allowed_x_handles,excluded_x_handles,from_date,to_date) was set AND both citation channels came back empty. In that case theanswerwas synthesized from the model's own knowledge rather than the X index, so treat it as unsourced.falseotherwise (including the "no filters set" case — a broad unsourced answer is just an answer, not a filter miss)
- degraded_reason— short string naming which filters were active, ornullwhendegradedisfalse
- credential_source—"xai-oauth"if OAuth resolved,"xai"if API key resolved
- model,query,provider,tool,success

`answer`
`citations`
`inline_citations`
`url_citation`
`url`
`title`
`start_index`
`end_index`
`degraded`
`true`
`allowed_x_handles`
`excluded_x_handles`
`from_date`
`to_date`
`answer`
`false`
`degraded_reason`
`null`
`degraded`
`false`
`credential_source`
`"xai-oauth"`
`"xai"`
`model`
`query`
`provider`
`tool`
`success`

### Date validation​

from_date/to_dateare validated client-side before the HTTP call:

`from_date`
`to_date`
- Both, if provided, must parse asYYYY-MM-DD.
- When both are set,from_datemust be on or beforeto_date.
- from_datemust not be later than today UTC — no posts can exist in a window that hasn't started yet, so the call would be guaranteed to return zero citations.
- to_datein the future is allowed (callers may legitimately request "from yesterday to tomorrow" to catch posts as they arrive).

`YYYY-MM-DD`
`from_date`
`to_date`
`from_date`
`to_date`

Validation failures surface as a structured{"error": "..."}tool result, never as an HTTP call to xAI.

`{"error": "..."}`

## Example​

Talking to the agent:

> What are people on X saying about the new Grok image features? Focus on responses from @xai.

What are people on X saying about the new Grok image features? Focus on responses from @xai.

The agent will:

1. Callx_searchwithquery="reactions to new Grok image features",allowed_x_handles=["xai"]
2. Get back a synthesized answer plus a list of citations linking to specific posts
3. Reply with the answer and references

`x_search`
`query="reactions to new Grok image features"`
`allowed_x_handles=["xai"]`

## Troubleshooting​

### "No xAI credentials available"​

The tool surfaces this when both auth paths fail. Either setXAI_API_KEYin~/.hermes/.envor runhermes auth add xai-oauthand complete the browser login. Then restart your session so the agent re-reads the tool registry.

`XAI_API_KEY`
`~/.hermes/.env`
`hermes auth add xai-oauth`

### "x_searchis not enabled for this model"​

`x_search`

The configuredx_search.modeldoesn't have access to the server-sidex_searchtool. Switch togrok-4.20-reasoning(the default) or another Grok model that supports it. Check thexAI documentationfor the current list.

`x_search.model`
`x_search`
`grok-4.20-reasoning`

### Tool doesn't appear in the schema​

Two possible causes:

1. Toolset not enabled.Runhermes toolsand confirm🐦 X (Twitter) Searchis checked.
2. No xAI credentials.The check_fn returns False, so the schema stays hidden. Runhermes auth statusto confirm xai-oauth login state, and check thatXAI_API_KEYis set (if you're using the API-key path).

`hermes tools`
`🐦 X (Twitter) Search`
`hermes auth status`
`XAI_API_KEY`

### degraded: true— answer with no citations​

`degraded: true`

When you usedallowed_x_handles,excluded_x_handles, or a date range and the response comes back withdegraded: true, xAI's X index returned no matching posts but Grok still produced a synthesized answer from its own training data. The answer is unsourced — do not treat it as a real X result.

`allowed_x_handles`
`excluded_x_handles`
`degraded: true`

Causes worth checking:

- Typo in the handle.Strip the@, double-check spelling, and confirm the account exists.
- Date range too narrowor sliding past today's posts; widen and retry.
- xAI index gap.Some active accounts intermittently fail to surface inx_searcheven when they post regularly. Retry after a few minutes, or use thexurlskill for direct X API reads when you need an exact handle's timeline.

`@`
`x_search`
`xurl`

## See Also​

- xAI Grok OAuth (SuperGrok / Premium+)— the OAuth setup guide
- Web Search & Extract— for general (non-X) web search
- Tools Reference— full tool catalog