- 
- Developer Guide
- Architecture
- Session Storage

# Session Storage

Hermes Agent uses a SQLite database (~/.hermes/state.db) to persist session
metadata, full message history, and model configuration across CLI and gateway
sessions. This replaces the earlier per-session JSONL file approach.

`~/.hermes/state.db`

Source file:hermes_state.py

`hermes_state.py`

## Architecture Overview​

```
~/.hermes/state.db (SQLite, WAL mode)├── sessions              — Session metadata, token counts, billing├── messages              — Full message history per session├── messages_fts          — FTS5 virtual table (content + tool_name + tool_calls)├── messages_fts_trigram  — FTS5 virtual table with trigram tokenizer (CJK / substring search)├── state_meta            — Key/value metadata table└── schema_version        — Single-row table tracking migration state
```

Key design decisions:

- WAL modefor concurrent readers + one writer (gateway multi-platform)
- FTS5 virtual tablefor fast text search across all session messages
- Session lineageviaparent_session_idchains (compression-triggered splits)
- Source tagging(cli,telegram,discord, etc.) for platform filtering
- Batch runner and RL trajectories are NOT stored here (separate systems)

`parent_session_id`
`cli`
`telegram`
`discord`

## SQLite Schema​

### Sessions Table​

```
CREATE TABLE IF NOT EXISTS sessions (    id TEXT PRIMARY KEY,    source TEXT NOT NULL,    user_id TEXT,    model TEXT,    model_config TEXT,    system_prompt TEXT,    parent_session_id TEXT,    started_at REAL NOT NULL,    ended_at REAL,    end_reason TEXT,    message_count INTEGER DEFAULT 0,    tool_call_count INTEGER DEFAULT 0,    input_tokens INTEGER DEFAULT 0,    output_tokens INTEGER DEFAULT 0,    cache_read_tokens INTEGER DEFAULT 0,    cache_write_tokens INTEGER DEFAULT 0,    reasoning_tokens INTEGER DEFAULT 0,    billing_provider TEXT,    billing_base_url TEXT,    billing_mode TEXT,    estimated_cost_usd REAL,    actual_cost_usd REAL,    cost_status TEXT,    cost_source TEXT,    pricing_version TEXT,    title TEXT,    api_call_count INTEGER DEFAULT 0,    FOREIGN KEY (parent_session_id) REFERENCES sessions(id));CREATE INDEX IF NOT EXISTS idx_sessions_source ON sessions(source);CREATE INDEX IF NOT EXISTS idx_sessions_parent ON sessions(parent_session_id);CREATE INDEX IF NOT EXISTS idx_sessions_started ON sessions(started_at DESC);CREATE UNIQUE INDEX IF NOT EXISTS idx_sessions_title_unique    ON sessions(title) WHERE title IS NOT NULL;
```

### Messages Table​

```
CREATE TABLE IF NOT EXISTS messages (    id INTEGER PRIMARY KEY AUTOINCREMENT,    session_id TEXT NOT NULL REFERENCES sessions(id),    role TEXT NOT NULL,    content TEXT,    tool_call_id TEXT,    tool_calls TEXT,    tool_name TEXT,    timestamp REAL NOT NULL,    token_count INTEGER,    finish_reason TEXT,    reasoning TEXT,    reasoning_content TEXT,    reasoning_details TEXT,    codex_reasoning_items TEXT,    codex_message_items TEXT);CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, timestamp);
```

Notes:

- tool_callsis stored as a JSON string (serialized list of tool call objects)
- reasoning_details,codex_reasoning_items, andcodex_message_itemsare stored as JSON strings
- reasoningstores the raw reasoning text for providers that expose it
- Timestamps are Unix epoch floats (time.time())

`tool_calls`
`reasoning_details`
`codex_reasoning_items`
`codex_message_items`
`reasoning`
`time.time()`

### FTS5 Full-Text Search​

```
CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(    content,    content=messages,    content_rowid=id);
```

The FTS5 table is kept in sync via three triggers that fire on INSERT, UPDATE,
and DELETE of themessagestable:

`messages`

```
CREATE TRIGGER IF NOT EXISTS messages_fts_insert AFTER INSERT ON messages BEGIN    INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);END;CREATE TRIGGER IF NOT EXISTS messages_fts_delete AFTER DELETE ON messages BEGIN    INSERT INTO messages_fts(messages_fts, rowid, content)        VALUES('delete', old.id, old.content);END;CREATE TRIGGER IF NOT EXISTS messages_fts_update AFTER UPDATE ON messages BEGIN    INSERT INTO messages_fts(messages_fts, rowid, content)        VALUES('delete', old.id, old.content);    INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);END;
```

## Schema Version and Migrations​

Current schema version:11

Theschema_versiontable stores a single integer. Simple column additions are handled declaratively by_reconcile_columns()(which diffs live columns againstSCHEMA_SQLand ADDs any missing ones). The version-gated chain is reserved for data migrations and index/FTS changes that can't be expressed declaratively:

`schema_version`
`_reconcile_columns()`
`SCHEMA_SQL`
| Version | Change |
| --- | --- |
| 1 | Initial schema (sessions, messages, FTS5) |
| 2 | Addfinish_reasoncolumn to messages |
| 3 | Addtitlecolumn to sessions |
| 4 | Add unique index ontitle(NULLs allowed, non-NULL must be unique) |
| 5 | Add billing columns:cache_read_tokens,cache_write_tokens,reasoning_tokens,billing_provider,billing_base_url,billing_mode,estimated_cost_usd,actual_cost_usd,cost_status,cost_source,pricing_version |
| 6 | Add reasoning columns to messages:reasoning,reasoning_details,codex_reasoning_items |
| 7 | Addreasoning_contentcolumn to messages |
| 8 | Addapi_call_countcolumn to sessions |
| 9 | Addcodex_message_itemscolumn to messages for Codex Responses message id/phase replay |
| 10 | Addmessages_fts_trigramvirtual table (trigram tokenizer for CJK / substring search) and backfill existing rows |
| 11 | Re-indexmessages_ftsandmessages_fts_trigramto covertool_name+tool_callsand switch from external-content to inline mode; drop old triggers and backfill every message row |

`finish_reason`
`title`
`title`
`cache_read_tokens`
`cache_write_tokens`
`reasoning_tokens`
`billing_provider`
`billing_base_url`
`billing_mode`
`estimated_cost_usd`
`actual_cost_usd`
`cost_status`
`cost_source`
`pricing_version`
`reasoning`
`reasoning_details`
`codex_reasoning_items`
`reasoning_content`
`api_call_count`
`codex_message_items`
`messages_fts_trigram`
`messages_fts`
`messages_fts_trigram`
`tool_name`
`tool_calls`

Declarative column adds useALTER TABLE ADD COLUMNwrapped in try/except to handle the column-already-exists case (idempotent). The version number is bumped after each successful migration block.

`ALTER TABLE ADD COLUMN`

## Write Contention Handling​

Multiple hermes processes (gateway + CLI sessions + worktree agents) share onestate.db. TheSessionDBclass handles write contention with:

`state.db`
`SessionDB`
- Short SQLite timeout(1 second) instead of the default 30s
- Application-level retrywith random jitter (20-150ms, up to 15 retries)
- BEGIN IMMEDIATEtransactions to surface lock contention at transaction start
- Periodic WAL checkpointsevery 50 successful writes (PASSIVE mode)

This avoids the "convoy effect" where SQLite's deterministic internal backoff
causes all competing writers to retry at the same intervals.

```
_WRITE_MAX_RETRIES = 15_WRITE_RETRY_MIN_S = 0.020   # 20ms_WRITE_RETRY_MAX_S = 0.150   # 150ms_CHECKPOINT_EVERY_N_WRITES = 50
```

## Common Operations​

### Initialize​

```
from hermes_state import SessionDBdb = SessionDB()                           # Default: ~/.hermes/state.dbdb = SessionDB(db_path=Path("/tmp/test.db"))  # Custom path
```

### Create and Manage Sessions​

```
# Create a new sessiondb.create_session(    session_id="sess_abc123",    source="cli",    model="anthropic/claude-sonnet-4.6",    user_id="user_1",    parent_session_id=None,  # or previous session ID for lineage)# End a sessiondb.end_session("sess_abc123", end_reason="user_exit")# Reopen a session (clear ended_at/end_reason)db.reopen_session("sess_abc123")
```

### Store Messages​

```
msg_id = db.append_message(    session_id="sess_abc123",    role="assistant",    content="Here's the answer...",    tool_calls=[{"id": "call_1", "function": {"name": "terminal", "arguments": "{}"}}],    token_count=150,    finish_reason="stop",    reasoning="Let me think about this...",)
```

### Retrieve Messages​

```
# Raw messages with all metadatamessages = db.get_messages("sess_abc123")# OpenAI conversation format (for API replay)conversation = db.get_messages_as_conversation("sess_abc123")# Returns: [{"role": "user", "content": "..."}, {"role": "assistant", ...}]
```

### Session Titles​

```
# Set a title (must be unique among non-NULL titles)db.set_session_title("sess_abc123", "Fix Docker Build")# Resolve by title (returns most recent in lineage)session_id = db.resolve_session_by_title("Fix Docker Build")# Auto-generate next title in lineagenext_title = db.get_next_title_in_lineage("Fix Docker Build")# Returns: "Fix Docker Build #2"
```

## Full-Text Search​

Thesearch_messages()method supports FTS5 query syntax with automatic
sanitization of user input.

`search_messages()`

### Basic Search​

```
results = db.search_messages("docker deployment")
```

### FTS5 Query Syntax​

| Syntax | Example | Meaning |
| --- | --- | --- |
| Keywords | docker deployment | Both terms (implicit AND) |
| Quoted phrase | "exact phrase" | Exact phrase match |
| Boolean OR | docker OR kubernetes | Either term |
| Boolean NOT | python NOT java | Exclude term |
| Prefix | deploy* | Prefix match |

`docker deployment`
`"exact phrase"`
`docker OR kubernetes`
`python NOT java`
`deploy*`

### Filtered Search​

```
# Search only CLI sessionsresults = db.search_messages("error", source_filter=["cli"])# Exclude gateway sessionsresults = db.search_messages("bug", exclude_sources=["telegram", "discord"])# Search only user messagesresults = db.search_messages("help", role_filter=["user"])
```

### Search Results Format​

Each result includes:

- id,session_id,role,timestamp
- snippet— FTS5-generated snippet with>>>match<<<markers
- context— 1 message before and after the match (content truncated to 200 chars)
- source,model,session_started— from the parent session

`id`
`session_id`
`role`
`timestamp`
`snippet`
`>>>match<<<`
`context`
`source`
`model`
`session_started`

The_sanitize_fts5_query()method handles edge cases:

`_sanitize_fts5_query()`
- Strips unmatched quotes and special characters
- Wraps hyphenated terms in quotes (chat-send→"chat-send")
- Removes dangling boolean operators (hello AND→hello)

`chat-send`
`"chat-send"`
`hello AND`
`hello`

## Session Lineage​

Sessions can form chains viaparent_session_id. This happens when context
compression triggers a session split in the gateway.

`parent_session_id`

### Query: Find Session Lineage​

```
-- Find all ancestors of a sessionWITH RECURSIVE lineage AS (    SELECT * FROM sessions WHERE id = ?    UNION ALL    SELECT s.* FROM sessions s    JOIN lineage l ON s.id = l.parent_session_id)SELECT id, title, started_at, parent_session_id FROM lineage;-- Find all descendants of a sessionWITH RECURSIVE descendants AS (    SELECT * FROM sessions WHERE id = ?    UNION ALL    SELECT s.* FROM sessions s    JOIN descendants d ON s.parent_session_id = d.id)SELECT id, title, started_at FROM descendants;
```

### Query: Recent Sessions with Preview​

```
SELECT s.*,    COALESCE(        (SELECT SUBSTR(m.content, 1, 63)         FROM messages m         WHERE m.session_id = s.id AND m.role = 'user' AND m.content IS NOT NULL         ORDER BY m.timestamp, m.id LIMIT 1),        ''    ) AS preview,    COALESCE(        (SELECT MAX(m2.timestamp) FROM messages m2 WHERE m2.session_id = s.id),        s.started_at    ) AS last_activeFROM sessions sORDER BY s.started_at DESCLIMIT 20;
```

### Query: Token Usage Statistics​

```
-- Total tokens by modelSELECT model,       COUNT(*) as session_count,       SUM(input_tokens) as total_input,       SUM(output_tokens) as total_output,       SUM(estimated_cost_usd) as total_costFROM sessionsWHERE model IS NOT NULLGROUP BY modelORDER BY total_cost DESC;-- Sessions with highest token usageSELECT id, title, model, input_tokens + output_tokens AS total_tokens,       estimated_cost_usdFROM sessionsORDER BY total_tokens DESCLIMIT 10;
```

## Export and Cleanup​

```
# Export a single session with messagesdata = db.export_session("sess_abc123")# Export all sessions (with messages) as list of dictsall_data = db.export_all(source="cli")# Delete old sessions (only ended sessions)deleted_count = db.prune_sessions(older_than_days=90)deleted_count = db.prune_sessions(older_than_days=30, source="telegram")# Clear messages but keep the session recorddb.clear_messages("sess_abc123")# Delete session and all messagesdb.delete_session("sess_abc123")
```

## Database Location​

Default path:~/.hermes/state.db

`~/.hermes/state.db`

This is derived fromhermes_constants.get_hermes_home()which resolves to~/.hermes/by default, or the value ofHERMES_HOMEenvironment variable.

`hermes_constants.get_hermes_home()`
`~/.hermes/`
`HERMES_HOME`

The database file, WAL file (state.db-wal), and shared-memory file
(state.db-shm) are all created in the same directory.

`state.db-wal`
`state.db-shm`