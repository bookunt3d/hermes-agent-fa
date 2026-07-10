---
layout: docs
title: "شخصیت"
permalink: /user-guide/features/personality/
---

- 
- Features
- Core
- Personality & SOUL.md

# Personality & SOUL.md

Hermes Agent's personality is fully customizable.SOUL.mdis theprimary identity— it's the first thing in the system prompt and defines who the agent is.

`SOUL.md`
- SOUL.md— a durable persona file that lives inHERMES_HOMEand serves as the agent's identity (slot #1 in the system prompt)
- built-in or custom/personalitypresets — session-level system-prompt overlays

`SOUL.md`
`HERMES_HOME`
`/personality`

If you want to change who Hermes is — or replace it with an entirely different agent persona — editSOUL.md.

`SOUL.md`

## How SOUL.md works now​

Hermes now seeds a defaultSOUL.mdautomatically in:

`SOUL.md`

```
~/.hermes/SOUL.md
```

More precisely, it uses the current instance'sHERMES_HOME, so if you run Hermes with a custom home directory, it will use:

`HERMES_HOME`

```
$HERMES_HOME/SOUL.md
```

### Important behavior​

- SOUL.md is the agent's primary identity.It occupies slot #1 in the system prompt, replacing the hardcoded default identity.
- Hermes creates a starterSOUL.mdautomatically if one does not exist yet
- Existing userSOUL.mdfiles are never overwritten
- Hermes loadsSOUL.mdonly fromHERMES_HOME
- Hermes does not look in the current working directory forSOUL.md
- IfSOUL.mdexists but is empty, or cannot be loaded, Hermes falls back to a built-in default identity
- IfSOUL.mdhas content, that content is injected verbatim after security scanning and truncation
- SOUL.md isnotduplicated in the context files section — it appears only once, as the identity

`SOUL.md`
`SOUL.md`
`SOUL.md`
`HERMES_HOME`
`SOUL.md`
`SOUL.md`
`SOUL.md`

That makesSOUL.mda true per-user or per-instance identity, not just an additive layer.

`SOUL.md`

## Why this design​

This keeps personality predictable.

If Hermes loadedSOUL.mdfrom whatever directory you happened to launch it in, your personality could change unexpectedly between projects. By loading only fromHERMES_HOME, the personality belongs to the Hermes instance itself.

`SOUL.md`
`HERMES_HOME`

That also makes it easier to teach users:

- "Edit~/.hermes/SOUL.mdto change Hermes' default personality."

`~/.hermes/SOUL.md`

## Where to edit it​

For most users:

```
~/.hermes/SOUL.md
```

If you use a custom home:

```
$HERMES_HOME/SOUL.md
```

## What should go in SOUL.md?​

Use it for durable voice and personality guidance, such as:

- tone
- communication style
- level of directness
- default interaction style
- what to avoid stylistically
- how Hermes should handle uncertainty, disagreement, or ambiguity

Use it less for:

- one-off project instructions
- file paths
- repo conventions
- temporary workflow details

Those belong inAGENTS.md, notSOUL.md.

`AGENTS.md`
`SOUL.md`

## Good SOUL.md content​

A good SOUL file is:

- stable across contexts
- broad enough to apply in many conversations
- specific enough to materially shape the voice
- focused on communication and identity, not task-specific instructions

### Example​

```
# PersonalityYou are a pragmatic senior engineer with strong taste.You optimize for truth, clarity, and usefulness over politeness theater.## Style- Be direct without being cold- Prefer substance over filler- Push back when something is a bad idea- Admit uncertainty plainly- Keep explanations compact unless depth is useful## What to avoid- Sycophancy- Hype language- Repeating the user's framing if it's wrong- Overexplaining obvious things## Technical posture- Prefer simple systems over clever systems- Care about operational reality, not idealized architecture- Treat edge cases as part of the design, not cleanup
```

## What Hermes injects into the prompt​

SOUL.mdcontent goes directly into slot #1 of the system prompt — the agent identity position. No wrapper language is added around it.

`SOUL.md`

The content goes through:

- prompt-injection scanning
- truncation if it is too large

If the file is empty, whitespace-only, or cannot be read, Hermes falls back to a built-in default identity ("You are Hermes Agent, an intelligent AI assistant created by Nous Research..."). This fallback also applies whenskip_context_filesis set (e.g., in subagent/delegation contexts).

`skip_context_files`

## Security scanning​

SOUL.mdis scanned like other context-bearing files for prompt injection patterns before inclusion.

`SOUL.md`

That means you should still keep it focused on persona/voice rather than trying to sneak in strange meta-instructions.

## SOUL.md vs AGENTS.md​

This is the most important distinction.

### SOUL.md​

Use for:

- identity
- tone
- style
- communication defaults
- personality-level behavior

### AGENTS.md​

Use for:

- project architecture
- coding conventions
- tool preferences
- repo-specific workflows
- commands, ports, paths, deployment notes

A useful rule:

- if it should follow you everywhere, it belongs inSOUL.md
- if it belongs to a project, it belongs inAGENTS.md

`SOUL.md`
`AGENTS.md`

## SOUL.md vs/personality​

`/personality`

SOUL.mdis your durable default personality.

`SOUL.md`

/personalityis a session-level overlay that changes or supplements the current system prompt.

`/personality`

So:

- SOUL.md= baseline voice
- /personality= temporary mode switch

`SOUL.md`
`/personality`

Examples:

- keep a pragmatic default SOUL, then use/personality teacherfor a tutoring conversation
- keep a concise SOUL, then use/personality creativefor brainstorming

`/personality teacher`
`/personality creative`

## Built-in personalities​

Hermes ships with built-in personalities you can switch to with/personality.

`/personality`

| Name | Description |
| --- | --- |
| helpful | Friendly, general-purpose assistant |
| concise | Brief, to-the-point responses |
| technical | Detailed, accurate technical expert |
| creative | Innovative, outside-the-box thinking |
| teacher | Patient educator with clear examples |
| kawaii | Cute expressions, sparkles, and enthusiasm ★ |
| catgirl | Neko-chan with cat-like expressions, nya~ |
| pirate | Captain Hermes, tech-savvy buccaneer |
| shakespeare | Bardic prose with dramatic flair |
| surfer | Totally chill bro vibes |
| noir | Hard-boiled detective narration |
| uwu | Maximum cute with uwu-speak |
| philosopher | Deep contemplation on every query |
| hype | MAXIMUM ENERGY AND ENTHUSIASM!!! |

## Switching personalities with commands​

### CLI​

```
/personality/personality concise/personality technical
```

### Messaging platforms​

```
/personality teacher
```

These are convenient overlays, but your globalSOUL.mdstill gives Hermes its persistent default personality unless the overlay meaningfully changes it.

`SOUL.md`

## Custom personalities in config​

You can also define named custom personalities in~/.hermes/config.yamlunderagent.personalities.

`~/.hermes/config.yaml`
`agent.personalities`

```
agent:  personalities:    codereviewer: >      You are a meticulous code reviewer. Identify bugs, security issues,      performance concerns, and unclear design choices. Be precise and constructive.
```

Then switch to it with:

```
/personality codereviewer
```

## Recommended workflow​

A strong default setup is:

1. Keep a thoughtful globalSOUL.mdin~/.hermes/SOUL.md
2. Put project instructions inAGENTS.md
3. Use/personalityonly when you want a temporary mode shift

`SOUL.md`
`~/.hermes/SOUL.md`
`AGENTS.md`
`/personality`

That gives you:

- a stable voice
- project-specific behavior where it belongs
- temporary control when needed

## How personality interacts with the full prompt​

At a high level, the prompt stack includes:

1. SOUL.md(agent identity — or built-in fallback if SOUL.md is unavailable)
2. tool-aware behavior guidance
3. memory/user context
4. skills guidance
5. context files (AGENTS.md,.cursorrules)
6. timestamp
7. platform-specific formatting hints
8. optional system-prompt overlays such as/personality

`AGENTS.md`
`.cursorrules`
`/personality`

SOUL.mdis the foundation — everything else builds on top of it.

`SOUL.md`

## Related docs​

- Context Files
- Configuration
- Tips & Best Practices
- SOUL.md Guide

[Context Files](/docs/user-guide/features/context-files)
[Configuration](/docs/user-guide/configuration)
[Tips & Best Practices](/docs/guides/tips)
[SOUL.md Guide](/docs/guides/use-soul-with-hermes)

## CLI appearance vs conversational personality​

Conversational personality and CLI appearance are separate:

- SOUL.md,agent.system_prompt, and/personalityaffect how Hermes speaks
- display.skinand/skinaffect how Hermes looks in the terminal

`SOUL.md`
`agent.system_prompt`
`/personality`
`display.skin`
`/skin`

For terminal appearance, seeSkins & Themes.

[Skins & Themes](/docs/user-guide/features/skins)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/personality.md)