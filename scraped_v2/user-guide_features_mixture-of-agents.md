- 
- Features
- Core
- Mixture of Agents

# Mixture of Agents

Mixture of Agents is a virtual model provider. Each named MoA preset appears as a selectable model under themoaprovider.

`moa`

When you select a MoA preset, the preset's aggregator is the acting model. It is the model that writes the assistant response and emits tool calls. Reference models run first and provide analysis for the aggregator to use.

Use MoA when a hard task benefits from multiple model perspectives but still needs Hermes' normal agent loop: tool calls, follow-up iterations, interrupts, transcript persistence, and the same session context as any other message.

## Select a MoA preset as your model​

You can select a preset through the normal model picker surfaces:

```
/model default --provider moa/model review --provider moa
```

MoA presets are selectable onevery Hermes surface, because MoA is a normal provider in the model system:

- CLI / gateway / TUI/model—/model <preset> --provider moa, or/model --provider moafor the default preset. A bare/model <preset>also works when the name exactly matches a configured preset.
- hermes modeland theDashboard model picker— aMixture of Agentsprovider row appears with your preset names as its models.
- Desktop GUI app— the model dropdown shows anMoA presetssection; selecting one (MoA: <preset>) switches the active model to that preset. The Desktop settings panel also creates and edits presets.

`/model`
`/model <preset> --provider moa`
`/model --provider moa`
`/model <preset>`
`hermes model`
`Mixture of Agents`
`MoA presets`
`MoA: <preset>`

Configured presets therefore show up wherever you would pick any other model.

## Slash command shortcut​

/moais one-shot convenience sugar. It runs a single prompt through thedefaultMoA preset, then restores whatever model you were on:

`/moa`

```
/moa design and implement a migration plan for this flaky test cluster
```

Hermes temporarily switches to the default MoA preset for that one turn, sends the prompt, then restores your previous model afterward. The whole argument is the prompt —/moano longer interprets it as a preset name.

`/moa`

```
/moa
```

Bare/moa(no prompt) just prints usage.

`/moa`

Toswitchto a MoA preset for the rest of the session, select it from the model picker — MoA presets appear under aMixture of Agentsprovider in every model-selection surface (see above)./moais deliberately not a model switch, so a normal prompt can never accidentally change your model.

`Mixture of Agents`
`/moa`

## How it works in the agent loop​

For each main model call when providermoais selected, Hermes:

`moa`
1. resolves the selected preset by name;
2. runs the configured reference models without tool schemas (they receive only the conversation's user/assistant text — not the Hermes system prompt or tool-call transcript — so reference calls stay cheap and avoid strict-provider rejections);
3. appends the reference outputs as private context for the aggregator;
4. calls the configured aggregator with the normal Hermes tool schema;
5. treats the aggregator response as the real model response;
6. if the aggregator calls tools, Hermes executes those tools normally;
7. on the next model iteration, the same MoA process runs again over the updated conversation, including tool results.

Because MoA is selected through the normal model system, it composes automatically with/goal, gateway sessions, TUI sessions, and Desktop chat.

`/goal`

## Configure presets​

You can configure named MoA presets from:

- Dashboard → Models → Model Settings → Mixture of Agents
- Desktop app → Settings → Model → Mixture of Agents
- hermes moa configure [name]
- config.yaml

`hermes moa configure [name]`
`config.yaml`

The config stores explicit provider/model pairs, so you can mix providers and use multiple models from the same provider:

```
moa:  default_preset: default  presets:    default:      reference_models:        - provider: openai-codex          model: gpt-5.5        - provider: openrouter          model: deepseek/deepseek-v4-pro      aggregator:        provider: openrouter        model: anthropic/claude-opus-4.8      # Optional: pin sampling temperatures. When omitted (the default),      # temperature is NOT sent and each model uses its provider default —      # the same behavior as a single-model Hermes agent.      # reference_temperature: 0.6      # aggregator_temperature: 0.4      max_tokens: 4096      enabled: true
```

Default preset:

- reference:openai-codex:gpt-5.5
- reference:openrouter:deepseek/deepseek-v4-pro
- aggregator / acting model:openrouter:anthropic/claude-opus-4.8

`openai-codex:gpt-5.5`
`openrouter:deepseek/deepseek-v4-pro`
`openrouter:anthropic/claude-opus-4.8`

### Tuning advisor speed withreference_max_tokens​

`reference_max_tokens`

Each turn, MoA runs the reference models (advisors) in parallel and then the
aggregator acts. Advisor generation is the dominant per-turn latency — turn
wall time correlates strongly with how many tokens the advisors emit, because
the turn waits for the slowest advisor to finish writing. By default advisors
areuncapped(reference_max_tokensunset), so they may write long,
essay-length advice.

`reference_max_tokens`

Setreference_max_tokenson a preset to cap advisor output and give concise
advice instead. The aggregator only needs the gist of each advisor's
judgement, so a cap (e.g.600) measurably cuts per-turn wall time with little
quality impact. It capsadvisors only— the acting aggregator's output (the
user-visible answer) is never capped.

`reference_max_tokens`
`600`

```
moa:  presets:    fast:      reference_models:        - provider: openrouter          model: anthropic/claude-opus-4.8        - provider: openrouter          model: openai/gpt-5.5      aggregator:        provider: openrouter        model: anthropic/claude-opus-4.8      reference_max_tokens: 600   # concise advice → faster turns
```

Leave it unset (or0/blank) to keep the prior uncapped behavior.

`0`

## Terminal preset management​

```
hermes moa listhermes moa configure              # update the default presethermes moa configure review       # create or update a named presethermes moa delete review
```

## Benchmarks​

On HermesBench, a two-model MoA preset —claude-opus-4.8aggregating over agpt-5.5reference — outscores either model run on its own:

`claude-opus-4.8`
`gpt-5.5`
| Model | HermesBench score |
| --- | --- |
| Opus aggregator (opus-4.8 + gpt-5.5 reference) — MoA | 0.8202 |
| anthropic/claude-opus-4.8 | 0.7607 |
| openai/gpt-5.5 | 0.7412 |

`anthropic/claude-opus-4.8`
`openai/gpt-5.5`

The MoA configuration beats its strongest component (opus-4.8) by ~6 points, confirming that aggregating a second perspective lifts quality on hard tasks rather than just averaging the two.

## Prompt caching​

MoA is built so themain conversation's prompt cache is never broken. Selecting a MoA preset is a normal model selection: it does not mutate past context, swap toolsets, or rebuild the system prompt mid-conversation. Your conversation history, system prompt, and tool schema stay byte-stable, so the cached prefix every other model relies on is preserved exactly as it would be for a plain model. Switching to or away from a MoA preset costs the same cache invalidation as any other/modelswitch — no more.

`/model`

Both internal call types cache normally:

- Reference modelsreceive a trimmed, deterministic view of the conversation (system prompt and tool transcript stripped — see the loop above). Because that view is a stable function of the stable history, a reference model's prompt prefix repeats across iterations and caches normally. References are short advisory calls with no tools.
- The aggregatoris the acting model. The reference outputs are appended to theendof the latest user turn as private guidance. Because that text sits at the tail — below the entire stable prefix (system prompt + prior history) — it does not invalidate any cached prefix: the aggregator gets a cache hit on everything above the injection, and only the freshly appended tail is new. That is exactly how every normal turn behaves, where each new user message is also uncached tail tokens.

So MoA does not sacrifice prompt caching on either call type. Its only real cost is the extra reference calls per iteration — you pay for multiple model perspectives, not for broken caches. The long-lived conversation prefix shared with the rest of Hermes is fully intact.

## Notes​

- MoA is no longer listed underhermes tools; there is nomoatoolset to enable.
- Settingenabled: falseon a preset disables the reference fan-out for that preset: the aggregator acts alone, exactly as if you selected it as a plain model. This is the per-preset off switch surfaced in the dashboard and desktop settings.
- A preset's aggregator cannot be another MoA preset. Recursive MoA trees are intentionally blocked.
- Credential failures on one reference model do not abort the turn. Hermes includes the failure in the reference context and continues with whatever models returned.
- MoA increases model-call count. A single model iteration can involve multiple reference calls plus the aggregator call.

`hermes tools`
`moa`
`enabled: false`