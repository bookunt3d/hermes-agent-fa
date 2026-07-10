- 
- Integrations
- Provider Routing

# Provider Routing

When usingOpenRouterorNous Portalas your LLM provider, Hermes Agent supportsprovider routing— fine-grained control over which underlying AI providers handle your requests and how they're prioritized.

OpenRouter routes requests to many providers (e.g., Anthropic, Google, AWS Bedrock, Together AI). Provider routing lets you optimize for cost, speed, quality, or enforce specific provider requirements.

Traffic routed through Nous Portal respects the same provider preferences — and Portal subscribers get 10% off token-billed providers.

## Configuration​

Add aprovider_routingsection to your~/.hermes/config.yaml:

`provider_routing`
`~/.hermes/config.yaml`

```
provider_routing:  sort: "price"           # How to rank providers  only: []                # Whitelist: only use these providers  ignore: []              # Blacklist: never use these providers  order: []               # Explicit provider priority order  require_parameters: false  # Only use providers that support all parameters  data_collection: null   # Control data collection ("allow" or "deny")
```

Provider routing only applies when using OpenRouter or Nous Portal. It has no effect with direct provider connections (e.g., connecting directly to the Anthropic API).

## Options​

### sort​

`sort`

Controls how OpenRouter ranks available providers for your request.

| Value | Description |
| --- | --- |
| "price" | Cheapest provider first |
| "throughput" | Fastest tokens-per-second first |
| "latency" | Lowest time-to-first-token first |

`"price"`
`"throughput"`
`"latency"`

```
provider_routing:  sort: "price"
```

### only​

`only`

Whitelist of provider slugs. When set,onlythese providers will be used. All others are excluded. Use the lowercase slug shown by OpenRouter for each provider.

```
provider_routing:  only:    - "anthropic"    - "google"
```

### ignore​

`ignore`

Blacklist of provider names. These providers willneverbe used, even if they offer the cheapest or fastest option.

```
provider_routing:  ignore:    - "together"    - "deepinfra"
```

### order​

`order`

Explicit priority order. Providers listed first are preferred. Unlisted providers are used as fallbacks.

```
provider_routing:  order:    - "anthropic"    - "google"    - "amazon-bedrock"
```

### require_parameters​

`require_parameters`

Whentrue, OpenRouter will only route to providers that supportallparameters in your request (liketemperature,top_p,tools, etc.). This avoids silent parameter drops.

`true`
`temperature`
`top_p`
`tools`

```
provider_routing:  require_parameters: true
```

### data_collection​

`data_collection`

Controls whether providers can use your prompts for training. Options are"allow"or"deny".

`"allow"`
`"deny"`

```
provider_routing:  data_collection: "deny"
```

## Practical Examples​

### Optimize for Cost​

Route to the cheapest available provider. Good for high-volume usage and development:

```
provider_routing:  sort: "price"
```

### Optimize for Speed​

Prioritize low-latency providers for interactive use:

```
provider_routing:  sort: "latency"
```

### Optimize for Throughput​

Best for long-form generation where tokens-per-second matters:

```
provider_routing:  sort: "throughput"
```

### Lock to Specific Providers​

Ensure all requests go through a specific provider for consistency:

```
provider_routing:  only:    - "anthropic"
```

### Avoid Specific Providers​

Exclude providers you don't want to use (e.g., for data privacy):

```
provider_routing:  ignore:    - "together"    - "lepton"  data_collection: "deny"
```

### Preferred Order with Fallbacks​

Try your preferred providers first, fall back to others if unavailable:

```
provider_routing:  order:    - "anthropic"    - "google"  require_parameters: true
```

## How It Works​

Provider routing preferences are passed to OpenRouter or Nous Portal on agent chat requests and iteration-limit summaries via theextra_body.providerfield. (extra_bodyis the OpenAI Python SDK argument; it becomes the top-levelproviderobject in the JSON request.) Auxiliary tasks such as compression and title generation are configured independently underauxiliary.<task>.extra_body.

`extra_body.provider`
`extra_body`
`provider`
`auxiliary.<task>.extra_body`
- CLI mode— configured in~/.hermes/config.yaml, loaded at startup
- Gateway mode— same config file, loaded when the gateway starts

`~/.hermes/config.yaml`

The routing config is read fromconfig.yamland passed as parameters when creating theAIAgent:

`config.yaml`
`AIAgent`

```
providers_allowed  ← from provider_routing.onlyproviders_ignored  ← from provider_routing.ignoreproviders_order    ← from provider_routing.orderprovider_sort      ← from provider_routing.sortprovider_require_parameters ← from provider_routing.require_parametersprovider_data_collection    ← from provider_routing.data_collection
```

You can combine multiple options. For example, sort by price but exclude certain providers and require parameter support:

```
provider_routing:  sort: "price"  ignore: ["together"]  require_parameters: true  data_collection: "deny"
```

## Default Behavior​

When noprovider_routingsection is configured (the default), the aggregator uses its own default routing logic, which generally balances cost and availability automatically.

`provider_routing`

Provider routing controls whichsub-providers behind OpenRouter or Nous Portalhandle your requests. For automatic failover to an entirely different provider when your primary model fails, seeFallback Providers.