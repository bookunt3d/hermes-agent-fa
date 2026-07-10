---
layout: docs
title: "فایل‌های زمینه"
permalink: /user-guide/features/context-files/
---

- 
- Features
- Core
- Context Files

# Context Files

Hermes Agent automatically discovers and loads context files that shape how it behaves. Some are project-local and discovered from your working directory.SOUL.mdis now global to the Hermes instance and is loaded fromHERMES_HOMEonly.

`SOUL.md`
`HERMES_HOME`

## Supported Context Files​

| File | Purpose | Discovery |
| --- | --- | --- |
| .hermes.md/HERMES.md | Project instructions (highest priority) | Walks to git root |
| AGENTS.md | Project instructions, conventions, architecture | CWD at startup + subdirectories progressively |
| CLAUDE.md | Claude Code context files (also detected) | CWD at startup + subdirectories progressively |
| SOUL.md | Global personality and tone customization for this Hermes instance | HERMES_HOME/SOUL.mdonly |
| .cursorrules | Cursor IDE coding conventions | CWD only |
| .cursor/rules/*.mdc | Cursor IDE rule modules | CWD only |

`HERMES_HOME/SOUL.md`

Onlyoneproject context type is loaded per session (first match wins):.hermes.md→AGENTS.md→CLAUDE.md→.cursorrules.SOUL.mdis always loaded independently as the agent identity (slot #1).

`.hermes.md`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`

## AGENTS.md​

AGENTS.mdis the primary project context file. It tells the agent how your project is structured, what conventions to follow, and any special instructions.

`AGENTS.md`

### Progressive Subdirectory Discovery​

At session start, Hermes loads theAGENTS.mdfrom your working directory into the system prompt. As the agent navigates into subdirectories during the session (viaread_file,terminal,search_files, etc.), itprogressively discoverscontext files in those directories and injects them into the conversation at the moment they become relevant.

`AGENTS.md`
`read_file`
`terminal`
`search_files`

```
my-project/├── AGENTS.md              ← Loaded at startup (system prompt)├── frontend/│   └── AGENTS.md          ← Discovered when agent reads frontend/ files├── backend/│   └── AGENTS.md          ← Discovered when agent reads backend/ files└── shared/    └── AGENTS.md          ← Discovered when agent reads shared/ files
```

This approach has two advantages over loading everything at startup:

- No system prompt bloat— subdirectory hints only appear when needed
- Prompt cache preservation— the system prompt stays stable across turns

Each subdirectory is checked at most once per session. The discovery also walks up parent directories, so readingbackend/src/main.pywill discoverbackend/AGENTS.mdeven ifbackend/src/has no context file of its own.

`backend/src/main.py`
`backend/AGENTS.md`
`backend/src/`

Subdirectory context files go through the samesecurity scanas startup context files. Malicious files are blocked.

### Example AGENTS.md​

```
# Project ContextThis is a Next.js 14 web application with a Python FastAPI backend.## Architecture- Frontend: Next.js 14 with App Router in `/frontend`- Backend: FastAPI in `/backend`, uses SQLAlchemy ORM- Database: PostgreSQL 16- Deployment: Docker Compose on a Hetzner VPS## Conventions- Use TypeScript strict mode for all frontend code- Python code follows PEP 8, use type hints everywhere- All API endpoints return JSON with `{data, error, meta}` shape- Tests go in `__tests__/` directories (frontend) or `tests/` (backend)## Important Notes- Never modify migration files directly — use Alembic commands- The `.env.local` file has real API keys, don't commit it- Frontend port is 3000, backend is 8000, DB is 5432
```

## SOUL.md​

SOUL.mdcontrols the agent's personality, tone, and communication style. See thePersonalitypage for full details.

`SOUL.md`
[Personality](/docs/user-guide/features/personality)

Location:

- ~/.hermes/SOUL.md
- or$HERMES_HOME/SOUL.mdif you run Hermes with a custom home directory

`~/.hermes/SOUL.md`
`$HERMES_HOME/SOUL.md`

Important details:

- Hermes seeds a defaultSOUL.mdautomatically if one does not exist yet
- Hermes loadsSOUL.mdonly fromHERMES_HOME
- Hermes does not probe the working directory forSOUL.md
- If the file is empty, nothing fromSOUL.mdis added to the prompt
- If the file has content, the content is injected verbatim after scanning and truncation

`SOUL.md`
`SOUL.md`
`HERMES_HOME`
`SOUL.md`
`SOUL.md`

## .cursorrules​

Hermes is compatible with Cursor IDE's.cursorrulesfile and.cursor/rules/*.mdcrule modules. If these files exist in your project root and no higher-priority context file (.hermes.md,AGENTS.md, orCLAUDE.md) is found, they're loaded as the project context.

`.cursorrules`
`.cursor/rules/*.mdc`
`.hermes.md`
`AGENTS.md`
`CLAUDE.md`

This means your existing Cursor conventions automatically apply when using Hermes.

## How Context Files Are Loaded​

### At startup (system prompt)​

Context files are loaded bybuild_context_files_prompt()inagent/prompt_builder.py:

`build_context_files_prompt()`
`agent/prompt_builder.py`
1. Scan working directory— checks for.hermes.md→AGENTS.md→CLAUDE.md→.cursorrules(first match wins)
2. Content is read— each file is read as UTF-8 text
3. Security scan— content is checked for prompt injection patterns
4. Truncation— files exceedingcontext_file_max_charscharacters (default 20,000) are head/tail truncated (70% head, 20% tail, with a marker in the middle)
5. Assembly— all sections are combined under a# Project Contextheader
6. Injection— the assembled content is added to the system prompt

`.hermes.md`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`
`context_file_max_chars`
`# Project Context`

### During the session (progressive discovery)​

SubdirectoryHintTrackerinagent/subdirectory_hints.pywatches tool call arguments for file paths:

`SubdirectoryHintTracker`
`agent/subdirectory_hints.py`
1. Path extraction— after each tool call, file paths are extracted from arguments (path,workdir, shell commands)
2. Ancestor walk— the directory and up to 5 parent directories are checked (stopping at already-visited directories)
3. Hint loading— if anAGENTS.md,CLAUDE.md, or.cursorrulesis found, it's loaded (first match per directory)
4. Security scan— same prompt injection scan as startup files
5. Truncation— capped at 8,000 characters per file
6. Injection— appended to the tool result, so the model sees it in context naturally

`path`
`workdir`
`AGENTS.md`
`CLAUDE.md`
`.cursorrules`

The final prompt section looks roughly like:

```
# Project ContextThe following project context files have been loaded and should be followed:## AGENTS.md[Your AGENTS.md content here]## .cursorrules[Your .cursorrules content here][Your SOUL.md content here]
```

Notice that SOUL content is inserted directly, without extra wrapper text.

## Security: Prompt Injection Protection​

All context files are scanned for potential prompt injection before being included. The scanner checks for:

- Instruction override attempts: "ignore previous instructions", "disregard your rules"
- Deception patterns: "do not tell the user"
- System prompt overrides: "system prompt override"
- Hidden HTML comments:<!-- ignore instructions -->
- Hidden div elements:<div style="display:none">
- Credential exfiltration:curl ... $API_KEY
- Secret file access:cat .env,cat credentials
- Invisible characters: zero-width spaces, bidirectional overrides, word joiners

`<!-- ignore instructions -->`
`<div style="display:none">`
`curl ... $API_KEY`
`cat .env`
`cat credentials`

If any threat pattern is detected, the file is blocked:

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

This scanner protects against common injection patterns, but it's not a substitute for reviewing context files in shared repositories. Always validate AGENTS.md content in projects you didn't author.

## Size Limits​

| Limit | Value |
| --- | --- |
| Max chars per file | context_file_max_chars(default 20,000, ~7,000 tokens) |
| Head truncation ratio | 70% |
| Tail truncation ratio | 20% |
| Truncation marker | 10% (shows char counts and suggests using file tools) |

`context_file_max_chars`

When a file exceeds the configured limit, the truncation message reads:

```
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```

## Tips for Effective Context Files​

1. Keep it concise— stay under your configuredcontext_file_max_chars; the agent reads it every turn
2. Structure with headers— use##sections for architecture, conventions, important notes
3. Include concrete examples— show preferred code patterns, API shapes, naming conventions
4. Mention what NOT to do— "never modify migration files directly"
5. List key paths and ports— the agent uses these for terminal commands
6. Update as the project evolves— stale context is worse than no context

`context_file_max_chars`
`##`

### Per-Subdirectory Context​

For monorepos, put subdirectory-specific instructions in nested AGENTS.md files:

```
<!-- frontend/AGENTS.md --># Frontend Context- Use `pnpm` not `npm` for package management- Components go in `src/components/`, pages in `src/app/`- Use Tailwind CSS, never inline styles- Run tests with `pnpm test`
```

```
<!-- backend/AGENTS.md --># Backend Context- Use `poetry` for dependency management- Run the dev server with `poetry run uvicorn main:app --reload`- All endpoints need OpenAPI docstrings- Database models are in `models/`, schemas in `schemas/`
```

[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/user-guide/features/context-files.md)