---
layout: docs
title: "مرجع مجموعه ابزارها"
permalink: /docs/reference/toolsets-reference/
---

- 
- Reference
- Tools & Skills Reference
- Toolsets Reference

# Toolsets Reference

Toolsets are named bundles of tools that control what the agent can do. They're the primary mechanism for configuring tool availability per platform, per session, or per task.

## How Toolsets Work​

Every tool belongs to exactly one toolset. When you enable a toolset, all tools in that bundle become available to the agent. Toolsets come in three kinds:

- Core— A single logical group of related tools (e.g.,filebundlesread_file,write_file,patch,search_files)
- Composite— Combines multiple core toolsets for a common scenario (e.g.,debuggingbundles file, terminal, and web tools)
- Platform— A complete tool configuration for a specific deployment context (e.g.,hermes-cliis the default for interactive CLI sessions)

`file`
`read_file`
`write_file`
`patch`
`search_files`
`debugging`
`hermes-cli`

## Configuring Toolsets​

### Per-session (CLI)​

```
hermes chat --toolsets web,file,terminalhermes chat --toolsets debugging        # composite — expands to file + terminal + webhermes chat --toolsets all              # everything
```

### Per-platform (config.yaml)​

```
toolsets:  - hermes-cli          # default for CLI  # - hermes-telegram   # override for Telegram gateway
```

### Interactive management​

```
hermes tools                            # curses UI to enable/disable per platform
```

Or in-session:

```
/tools list/tools disable browser/tools enable homeassistant
```

## Core Toolsets​

| Toolset | Tools | Purpose |
| --- | --- | --- |
| browser | browser_back,browser_cdp,browser_click,browser_console,browser_dialog,browser_get_images,browser_navigate,browser_press,browser_scroll,browser_snapshot,browser_type,browser_vision,web_search | Core browser automation. Includesweb_searchas a fallback for quick lookups.browser_cdpandbrowser_dialogare gated at runtime — registered only when a CDP endpoint is reachable at session start (via/browser connect,browser.cdp_urlconfig, Browserbase, or Camofox).browser_dialogworks together with thepending_dialogsandframe_treefields thatbrowser_snapshotadds when a CDP supervisor is attached. |
| clarify | clarify | Ask the user a question when the agent needs clarification. |
| code_execution | execute_code | Run Python scripts that call Hermes tools programmatically. |
| coding | composite (file+terminal+search+web+skills+browser+todo+memory+session_search+clarify+code_execution+delegation+vision) | Coding-focused bundle for software work: file editing, terminal, search, web docs, skills, browser, delegate, and code execution. |
| cronjob | cronjob | Schedule and manage recurring tasks. |
| debugging | composite (file+terminal+web) | Debug bundle — file, process/terminal, web extract/search. |
| delegation | delegate_task | Spawn isolated subagent instances for parallel work. |
| discord | discord | Core Discord text/embed/DM actions (gateway-only). Active on thehermes-discordtoolset. |
| discord_admin | discord_admin | Discord moderation (bans, role changes, channel management). Active on thehermes-discordtoolset; requires the bot to hold the relevant Discord permissions. |
| feishu_doc | feishu_doc_read | Read Feishu/Lark document content. Used by the Feishu document-comment intelligent-reply handler. |
| feishu_drive | feishu_drive_add_comment,feishu_drive_list_comments,feishu_drive_list_comment_replies,feishu_drive_reply_comment | Feishu/Lark drive comment operations. Scoped to the comment agent; not exposed onhermes-clior other messaging toolsets. |
| file | patch,read_file,search_files,write_file | File reading, writing, searching, and editing. |
| homeassistant | ha_call_service,ha_get_state,ha_list_entities,ha_list_services | Smart home control via Home Assistant. Only available whenHASS_TOKENis set. |
| computer_use | computer_use | Background desktop control via cua-driver — does not steal cursor/focus. Works with any tool-capable model. macOS, Windows, and Linux; requirescua-driveron$PATH. |
| context_engine | (varies) | Runtime tools exposed by the active context-engine plugin (empty until a plugin populates it). |
| image_gen | image_generate | Text-to-image generation via FAL.ai (with opt-in OpenAI / xAI backends). |
| video_gen | video_generate | Text-to-video and image-to-video via plugin-registered backends (xAI Grok-Imagine, FAL.ai Veo 3.1 / Pixverse v6 / Kling O3). Passimage_urlto animate an image; omit it for text-to-video. |
| kanban | kanban_block,kanban_comment,kanban_complete,kanban_create,kanban_heartbeat,kanban_link,kanban_list,kanban_show,kanban_unblock | Multi-agent coordination tools. Registered for dispatcher-spawned task workers (HERMES_KANBAN_TASK) and for profiles that explicitly list thekanbantoolset by name (theall/*wildcard doesnotenable it). Workers mark tasks done, block, heartbeat, comment, and create/link follow-up tasks; orchestrator profiles additionally get board-routing tools like list/unblock. |
| memory | memory | Persistent cross-session memory management. |
| project | project_create,project_list,project_switch | Create and switch desktopProjects(named, multi-folder workspaces). GUI / desktop sessions only. |
| safe | image_generate,vision_analyze,web_extract,web_search(viaincludes) | Read-only research + media generation. No file writes, no terminal, no code execution. |
| search | web_search | Web search only (without extract). |
| session_search | session_search | Search past conversation sessions. |
| skills | skill_manage,skill_view,skills_list | Skill CRUD and browsing. |
| spotify | spotify_albums,spotify_devices,spotify_library,spotify_playback,spotify_playlists,spotify_queue,spotify_search | Native Spotify control (playback, queue, search, playlists, albums, library). Registered by the bundledspotifyplugin. |
| terminal | process,terminal | Shell command execution and background process management. |
| todo | todo | Task list management within a session. |
| tts | text_to_speech | Text-to-speech audio generation. |
| vision | vision_analyze | Image analysis via vision-capable models. |
| video | video_analyze | Video analysis and understanding tools (opt-in, not in the default toolset — add explicitly via--toolsets). |
| web | web_extract,web_search | Web search and page content extraction. |
| x_search | x_search | Search X (Twitter) posts and threads via xAI's built-inx_searchResponses tool. Off by default; opt in viahermes tools. Schema only registered when xAI credentials (SuperGrok OAuth orXAI_API_KEY) are configured. |
| yuanbao | yb_query_group_info,yb_query_group_members,yb_search_sticker,yb_send_dm,yb_send_sticker | Yuanbao DM/group actions and sticker search. Registered only onhermes-yuanbao. |

`browser`
`browser_back`
`browser_cdp`
`browser_click`
`browser_console`
`browser_dialog`
`browser_get_images`
`browser_navigate`
`browser_press`
`browser_scroll`
`browser_snapshot`
`browser_type`
`browser_vision`
`web_search`
`web_search`
`browser_cdp`
`browser_dialog`
`/browser connect`
`browser.cdp_url`
`browser_dialog`
`pending_dialogs`
`frame_tree`
`browser_snapshot`
`clarify`
`clarify`
`code_execution`
`execute_code`
`coding`
`file`
`terminal`
`search`
`web`
`skills`
`browser`
`todo`
`memory`
`session_search`
`clarify`
`code_execution`
`delegation`
`vision`
`cronjob`
`cronjob`
`debugging`
`file`
`terminal`
`web`
`delegation`
`delegate_task`
`discord`
`discord`
`hermes-discord`
`discord_admin`
`discord_admin`
`hermes-discord`
`feishu_doc`
`feishu_doc_read`
`feishu_drive`
`feishu_drive_add_comment`
`feishu_drive_list_comments`
`feishu_drive_list_comment_replies`
`feishu_drive_reply_comment`
`hermes-cli`
`file`
`patch`
`read_file`
`search_files`
`write_file`
`homeassistant`
`ha_call_service`
`ha_get_state`
`ha_list_entities`
`ha_list_services`
`HASS_TOKEN`
`computer_use`
`computer_use`
`cua-driver`
`$PATH`
`context_engine`
`image_gen`
`image_generate`
`video_gen`
`video_generate`
`image_url`
`kanban`
`kanban_block`
`kanban_comment`
`kanban_complete`
`kanban_create`
`kanban_heartbeat`
`kanban_link`
`kanban_list`
`kanban_show`
`kanban_unblock`
`HERMES_KANBAN_TASK`
`kanban`
`all`
`*`
`memory`
`memory`
`project`
`project_create`
`project_list`
`project_switch`
`safe`
`image_generate`
`vision_analyze`
`web_extract`
`web_search`
`includes`
`search`
`web_search`
`session_search`
`session_search`
`skills`
`skill_manage`
`skill_view`
`skills_list`
`spotify`
`spotify_albums`
`spotify_devices`
`spotify_library`
`spotify_playback`
`spotify_playlists`
`spotify_queue`
`spotify_search`
`spotify`
`terminal`
`process`
`terminal`
`todo`
`todo`
`tts`
`text_to_speech`
`vision`
`vision_analyze`
`video`
`video_analyze`
`--toolsets`
`web`
`web_extract`
`web_search`
`x_search`
`x_search`
`x_search`
`hermes tools`
`XAI_API_KEY`
`yuanbao`
`yb_query_group_info`
`yb_query_group_members`
`yb_search_sticker`
`yb_send_dm`
`yb_send_sticker`
`hermes-yuanbao`

## Platform Toolsets​

Platform toolsets define the complete tool configuration for a deployment target. Most messaging platforms use the same set ashermes-cli:

`hermes-cli`
| Toolset | Differences fromhermes-cli |
| --- | --- |
| hermes-cli | Full toolset — the default for interactive CLI sessions. Includes file, terminal, web, browser, memory, skills, vision, image_gen, todo, tts, delegation, code_execution, cronjob, session_search, and clarify, plus thesafe(read-only) bundle. |
| hermes-acp | Dropsclarify,cronjob,image_generate,text_to_speech, and all four Home Assistant tools. Focused on coding tasks in IDE context. |
| hermes-api-server | Dropsclarifyandtext_to_speech. Keeps everything else — suitable for programmatic access where user interaction isn't possible. |
| hermes-cron | Same ashermes-cli. |
| hermes-telegram | Same ashermes-cli. |
| hermes-discord | Addsdiscordanddiscord_adminon top ofhermes-cli. |
| hermes-slack | Same ashermes-cli. |
| hermes-whatsapp | Same ashermes-cli. |
| hermes-signal | Same ashermes-cli. |
| hermes-matrix | Same ashermes-cli. |
| hermes-mattermost | Same ashermes-cli. |
| hermes-email | Same ashermes-cli. |
| hermes-sms | Same ashermes-cli. |
| hermes-bluebubbles | Same ashermes-cli. |
| hermes-dingtalk | Same ashermes-cli. |
| hermes-feishu | Adds the fivefeishu_doc_*/feishu_drive_*tools (only used by the document-comment handler, not the regular chat adapter). |
| hermes-qqbot | Same ashermes-cli. |
| hermes-wecom | Same ashermes-cli. |
| hermes-wecom-callback | Same ashermes-cli. |
| hermes-weixin | Same ashermes-cli. |
| hermes-yuanbao | Adds the fiveyb_*tools (DM/group/sticker) on top ofhermes-cli. |
| hermes-homeassistant | Same ashermes-cli(the Home Assistant tools are already present by default and activate whenHASS_TOKENis set). |
| hermes-webhook | Same ashermes-cli. |
| hermes-gateway | Internal gateway orchestrator toolset — union of everyhermes-<platform>toolset; used when the gateway needs to accept any message source. |

`hermes-cli`
`hermes-cli`
`safe`
`hermes-acp`
`clarify`
`cronjob`
`image_generate`
`text_to_speech`
`hermes-api-server`
`clarify`
`text_to_speech`
`hermes-cron`
`hermes-cli`
`hermes-telegram`
`hermes-cli`
`hermes-discord`
`discord`
`discord_admin`
`hermes-cli`
`hermes-slack`
`hermes-cli`
`hermes-whatsapp`
`hermes-cli`
`hermes-signal`
`hermes-cli`
`hermes-matrix`
`hermes-cli`
`hermes-mattermost`
`hermes-cli`
`hermes-email`
`hermes-cli`
`hermes-sms`
`hermes-cli`
`hermes-bluebubbles`
`hermes-cli`
`hermes-dingtalk`
`hermes-cli`
`hermes-feishu`
`feishu_doc_*`
`feishu_drive_*`
`hermes-qqbot`
`hermes-cli`
`hermes-wecom`
`hermes-cli`
`hermes-wecom-callback`
`hermes-cli`
`hermes-weixin`
`hermes-cli`
`hermes-yuanbao`
`yb_*`
`hermes-cli`
`hermes-homeassistant`
`hermes-cli`
`HASS_TOKEN`
`hermes-webhook`
`hermes-cli`
`hermes-gateway`
`hermes-<platform>`

## Dynamic Toolsets​

### MCP server toolsets​

Each configured MCP server generates amcp-<server>toolset at runtime. For example, if you configure agithubMCP server, amcp-githubtoolset is created containing all tools that server exposes.

`mcp-<server>`
`github`
`mcp-github`

```
# config.yamlmcp_servers:  github:    command: npx    args: ["-y", "@modelcontextprotocol/server-github"]
```

This creates amcp-githubtoolset you can reference in--toolsetsor platform configs.

`mcp-github`
`--toolsets`

### Plugin toolsets​

Plugins can register their own toolsets viactx.register_tool()during plugin initialization. These appear alongside built-in toolsets and can be enabled/disabled the same way.

`ctx.register_tool()`

### Custom toolsets​

Define custom toolsets inconfig.yamlto create project-specific bundles:

`config.yaml`

```
toolsets:  - hermes-clicustom_toolsets:  data-science:    - file    - terminal    - code_execution    - web    - vision
```

### Wildcards​

- allor*— expands to every registered toolset (built-in + dynamic + plugin)

`all`
`*`

A handful of tools have an additional availability check on top of toolset membership and arenotturned on byall/*alone:

`all`
`*`
- Capability-gatedtools (browser,computer_use,code_execution, Feishu, Home Assistant, cronjob) appear only when their backend/credential prerequisite is configured.
- Workflow-gatedtools — thekanbantoolset — are deliberately opt-in.all/*doesnotenable kanban; you must listkanbanexplicitly (or be a dispatcher-spawned worker withHERMES_KANBAN_TASKset). Kanban tools mutate shared board state, so they stay off by default even underall.

`computer_use`
`code_execution`
`kanban`
`all`
`*`
`kanban`
`HERMES_KANBAN_TASK`
`all`

## Relationship tohermes tools​

`hermes tools`

Thehermes toolscommand provides a curses-based UI for toggling individual tools on or off per platform. This operates at the tool level (finer than toolsets) and persists toconfig.yaml. Disabled tools are filtered out even if their toolset is enabled.

`hermes tools`
`config.yaml`

See also:Tools Referencefor the complete list of individual tools and their parameters.