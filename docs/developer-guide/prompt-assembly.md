---
layout: docs
title: "مونتاژ پرامپت"
permalink: /docs/developer-guide/prompt-assembly/
---

- 
- Developer Guide
- Architecture
- Prompt Assembly

# Prompt Assembly

Hermes deliberately separates:

- cached system prompt state
- ephemeral API-call-time additions

This is one of the most important design choices in the project because it affects:

- token usage
- prompt caching effectiveness
- session continuity
- memory correctness

Primary files:

- run_agent.py
- agent/prompt_builder.py
- tools/memory_tool.py

`run_agent.py`
`agent/prompt_builder.py`
`tools/memory_tool.py`

## Cached system prompt layers​

The cached system prompt is assembled as three ordered tiers (seeagent/system_prompt.py):

`agent/system_prompt.py`
1. stable— identity (SOUL.mdor fallback), tool/model guidance, skills prompt, environment hints, platform hints
2. context— caller-suppliedsystem_messageplus project context files (.hermes.md/AGENTS.md/CLAUDE.md/.cursorrules)
3. volatile— built-in memory snapshot (MEMORY.md), user profile snapshot (USER.md), external memory-provider block, timestamp/session/model/provider line

`SOUL.md`
`system_message`
`.hermes.md`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`
`MEMORY.md`
`USER.md`

The final system prompt is then joined as:stable→context→volatile.

`stable`
`context`
`volatile`

This ordering matters for precedence discussions:

- skills are part of thestabletier
- memory/profile snapshots are part of thevolatiletier
- both are still in the cached system prompt (they are not injected as ad-hoc mid-turn overlays)

Whenskip_context_filesis set (e.g., subagent delegation), SOUL.md is not loaded and the hardcodedDEFAULT_AGENT_IDENTITYis used instead.

`skip_context_files`
`DEFAULT_AGENT_IDENTITY`

### Concrete example: assembled system prompt​

Here is a simplified view of what the final system prompt looks like when all layers are present (comments show the source of each section):

```
# Layer 1: Agent Identity (from ~/.hermes/SOUL.md)You are Hermes, an AI assistant created by Nous Research.You are an expert software engineer and researcher.You value correctness, clarity, and efficiency....# Layer 2: Tool-aware behavior guidanceYou have persistent memory across sessions. Save durable facts usingthe memory tool: user preferences, environment details, tool quirks,and stable conventions. Memory is injected into every turn, so keepit compact and focused on facts that will still matter later....When the user references something from a past conversation or yoususpect relevant cross-session context exists, use session_searchto recall it before asking them to repeat themselves.# Tool-use enforcement (for GPT/Codex models only)You MUST use your tools to take action — do not describe what youwould do or plan to do without actually doing it....# Layer 3: Honcho static block (when active)[Honcho personality/context data]# Layer 4: Optional system message (from config or API)[User-configured system message override]# Layer 5: Frozen MEMORY snapshot## Persistent Memory- User prefers Python 3.12, uses pyproject.toml- Default editor is nvim- Working on project "atlas" in ~/code/atlas- Timezone: US/Pacific# Layer 6: Frozen USER profile snapshot## User Profile- Name: Alice- GitHub: alice-dev# Layer 7: Skills index## Skills (mandatory)Before replying, scan the skills below. If one clearly matchesyour task, load it with skill_view(name) and follow its instructions....<available_skills>  software-development:    - code-review: Structured code review workflow    - test-driven-development: TDD methodology  research:    - arxiv: Search and summarize arXiv papers</available_skills># Layer 8: Context files (from project directory)# Project ContextThe following project context files have been loaded and should be followed:## AGENTS.mdThis is the atlas project. Use pytest for testing. The mainentry point is src/atlas/main.py. Always run `make lint` beforecommitting.# Layer 9: Timestamp + sessionCurrent time: 2026-03-30T14:30:00-07:00Session: abc123# Layer 10: Platform hintYou are a CLI AI Agent. Try not to use markdown but simple textrenderable inside a terminal.
```

## Customizing platform hints​

The platform hint (Layer 10 above) is the per-surface guidance Hermes
injects for Telegram, WhatsApp, Slack, CLI, and other platforms — for
example "you are on a terminal, avoid Markdown." The built-in defaults
live inPLATFORM_HINTS(agent/system_prompt.py); plugin-provided
platforms supply theirs through the platform registry.

`PLATFORM_HINTS`
`agent/system_prompt.py`

An administrator can append to or replace a single platform's hint fromconfig.yamlvia the top-levelplatform_hintskey, without touching
any other platform:

`config.yaml`
`platform_hints`

```
platform_hints:  whatsapp:    append: >      When tabular output would be useful, invoke the table_formatting      skill instead of emitting a Markdown table.  slack:    replace: "You are on Slack. Keep responses tight and avoid wide tables."  telegram: "Prefer short messages; split long answers."   # shorthand = append
```

- append— keep the built-in hint and add the extra text after it.
- replace— substitute the built-in hint entirely.
- A bare string — shorthand forappend.
- replacewins overappendwhen both are present.
- A malformed entry is ignored defensively and falls back to the
unmodified default, so a bad config value can never break prompt
assembly or leak across platforms.

`append`
`replace`
`append`
`replace`
`append`

The override is resolved when the system prompt is built (session start,
and again on compaction since that rebuilds the prompt). It produces a
byte-stable hint for a fixed config, so it lives in thestabletier
alongside the built-in hint and does not break prompt caching — it is
not a live mid-session mutation of a frozen prompt.

## How SOUL.md appears in the prompt​

SOUL.mdlives at~/.hermes/SOUL.mdand serves as the agent's identity — the very first section of the system prompt. The loading logic inprompt_builder.pyworks as follows:

`SOUL.md`
`~/.hermes/SOUL.md`
`prompt_builder.py`

```
# From agent/prompt_builder.py (simplified)def load_soul_md() -> Optional[str]:    soul_path = get_hermes_home() / "SOUL.md"    if not soul_path.exists():        return None    content = soul_path.read_text(encoding="utf-8").strip()    content = _scan_context_content(content, "SOUL.md")  # Security scan    content = _truncate_content(content, "SOUL.md")       # Cap defaults to 20k chars, configurable    return content
```

Whenload_soul_md()returns content, it replaces the hardcodedDEFAULT_AGENT_IDENTITY. Thebuild_context_files_prompt()function is then called withskip_soul=Trueto prevent SOUL.md from appearing twice (once as identity, once as a context file).

`load_soul_md()`
`DEFAULT_AGENT_IDENTITY`
`build_context_files_prompt()`
`skip_soul=True`

IfSOUL.mddoesn't exist, the system falls back to:

`SOUL.md`

```
You are Hermes Agent, an intelligent AI assistant created by Nous Research.You are helpful, knowledgeable, and direct. You assist users with a widerange of tasks including answering questions, writing and editing code,analyzing information, creative work, and executing actions via your tools.You communicate clearly, admit uncertainty when appropriate, and prioritizebeing genuinely useful over being verbose unless otherwise directed below.Be targeted and efficient in your exploration and investigations.
```

## How context files are injected​

build_context_files_prompt()uses apriority system— only one project context type is loaded (first match wins):

`build_context_files_prompt()`

```
# From agent/prompt_builder.py (simplified)def build_context_files_prompt(cwd=None, skip_soul=False):    cwd_path = Path(cwd).resolve()    # Priority: first match wins — only ONE project context loaded    project_context = (        _load_hermes_md(cwd_path)       # 1. .hermes.md / HERMES.md (walks to git root)        or _load_agents_md(cwd_path)    # 2. AGENTS.md (cwd only)        or _load_claude_md(cwd_path)    # 3. CLAUDE.md (cwd only)        or _load_cursorrules(cwd_path)  # 4. .cursorrules / .cursor/rules/*.mdc    )    sections = []    if project_context:        sections.append(project_context)    # SOUL.md from HERMES_HOME (independent of project context)    if not skip_soul:        soul_content = load_soul_md()        if soul_content:            sections.append(soul_content)    if not sections:        return ""    return (        "# Project Context\n\n"        "The following project context files have been loaded "        "and should be followed:\n\n"        + "\n".join(sections)    )
```

### Context file discovery details​

| Priority | Files | Search scope | Notes |
| --- | --- | --- | --- |
| 1 | .hermes.md,HERMES.md | CWD up to git root | Hermes-native project config |
| 2 | AGENTS.md | CWD only | Common agent instruction file |
| 3 | CLAUDE.md | CWD only | Claude Code compatibility |
| 4 | .cursorrules,.cursor/rules/*.mdc | CWD only | Cursor compatibility |

`.hermes.md`
`HERMES.md`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`
`.cursor/rules/*.mdc`

All context files are:

- Security scanned— checked for prompt injection patterns (invisible unicode, "ignore previous instructions", credential exfiltration attempts)
- Truncated— capped atcontext_file_max_charscharacters (default 20,000) using 70/20 head/tail ratio with a truncation marker
- YAML frontmatter stripped—.hermes.mdfrontmatter is removed (reserved for future config overrides)

`context_file_max_chars`
`.hermes.md`

## API-call-time-only layers​

These are intentionallynotpersisted as part of the cached system prompt:

- ephemeral_system_prompt
- prefill messages
- gateway-derived session context overlays
- later-turn Honcho/external recall injected into the current-turn user message

`ephemeral_system_prompt`

pre_llm_callplugin context also lands in this API-call-time path: it is appended to the current turn'suser message, not written into the cached system prompt. When multiple plugins return context, Hermes concatenates those context blocks (seeHooks →pre_llm_call).

`pre_llm_call`
`pre_llm_call`

This separation keeps the stable prefix stable for caching.

## Memory snapshots​

Local memory and user profile data are captured in the system prompt'svolatile tier. Mid-session writes update disk state but do not mutate the already-built cached system prompt until a rebuild path runs (new session, or explicit invalidation/rebuild flow such as compression-triggered rebuild).

## Context files​

agent/prompt_builder.pyscans and sanitizes project context files using apriority system— only one type is loaded (first match wins):

`agent/prompt_builder.py`
1. .hermes.md/HERMES.md(walks to git root)
2. AGENTS.md(CWD at startup; subdirectories discovered progressively during the session viaagent/subdirectory_hints.py)
3. CLAUDE.md(CWD only)
4. .cursorrules/.cursor/rules/*.mdc(CWD only)

`.hermes.md`
`HERMES.md`
`AGENTS.md`
`agent/subdirectory_hints.py`
`CLAUDE.md`
`.cursorrules`
`.cursor/rules/*.mdc`

SOUL.mdis loaded separately viaload_soul_md()for the identity slot. When it loads successfully,build_context_files_prompt(skip_soul=True)prevents it from appearing twice.

`SOUL.md`
`load_soul_md()`
`build_context_files_prompt(skip_soul=True)`

Long files are truncated before injection.

## Skills index​

The skills system contributes a compact skills index to the prompt when skills tooling is available.

## Supported prompt customization surfaces​

Most users should treatagent/prompt_builder.pyas implementation code, not a configuration surface. The supported customization path is to change the prompt inputs Hermes already loads, rather than editing Python templates in place.

`agent/prompt_builder.py`

### Use these surfaces first​

- ~/.hermes/SOUL.md— replace the built-in default identity block with your own agent persona and standing behavior.
- ~/.hermes/MEMORY.mdand~/.hermes/USER.md— provide durable cross-session facts and user profile data that should be snapshotted into new sessions.
- Project context files such as.hermes.md,HERMES.md,AGENTS.md,CLAUDE.md, or.cursorrules— inject repo-specific working rules.
- Skills — package reusable workflows and references without editing core prompt code.
- Optional system prompt config / API overrides — add deployment-specific instruction text without forking Hermes.
- Ephemeral overlays such asHERMES_EPHEMERAL_SYSTEM_PROMPTor prefill messages — add turn-scoped guidance that should not become part of the cached prompt prefix.

`~/.hermes/SOUL.md`
`~/.hermes/MEMORY.md`
`~/.hermes/USER.md`
`.hermes.md`
`HERMES.md`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`
`HERMES_EPHEMERAL_SYSTEM_PROMPT`

### When to edit code instead​

Editagent/prompt_builder.pyonly if you are intentionally maintaining a fork or contributing upstream behavior changes. That file assembles the prompt plumbing, cache boundaries, and injection order for every session. Direct edits there are global product changes, not per-user prompt customization.

`agent/prompt_builder.py`

In other words:

- if you want a different assistant identity, editSOUL.md
- if you want different repo rules, edit project context files
- if you want reusable operating procedures, add or modify skills
- if you want to change how Hermes assembles prompts for everyone, change Python and treat it as a code contribution

`SOUL.md`

## Why prompt assembly is split this way​

The architecture is intentionally optimized to:

- preserve provider-side prompt caching
- avoid mutating history unnecessarily
- keep memory semantics understandable
- let gateway/ACP/CLI add context without poisoning persistent prompt state

## Related docs​

- Context Compression & Prompt Caching
- Session Storage
- Gateway Internals