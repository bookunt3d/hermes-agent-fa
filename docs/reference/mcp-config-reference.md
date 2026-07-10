---
layout: docs
title: "مرجع پیکربندی MCP"
permalink: /docs/reference/mcp-config-reference/
---

- 
- Reference
- Configuration Reference
- MCP Config Reference

# MCP Config Reference

This page is the compact reference companion to the main MCP docs.

For conceptual guidance, see:

- MCP (Model Context Protocol)
- Use MCP with Hermes

## Root config shape​

```
mcp_servers:  <server_name>:    command: "..."      # stdio servers    args: []    env: {}    # OR    url: "..."          # HTTP servers    headers: {}    # Optional HTTP/SSE TLS settings:    ssl_verify: true                # bool or path to a CA bundle (PEM)    client_cert: "/path/to/cert.pem"  # mTLS client certificate (see below)    # client_key: "/path/to/key.pem"  # optional, when key lives in a separate file    enabled: true    timeout: 120    connect_timeout: 60    supports_parallel_tool_calls: false    tools:      include: []      exclude: []      resources: true      prompts: true
```

## Server keys​

| Key | Type | Applies to | Meaning |
| --- | --- | --- | --- |
| command | string | stdio | Executable to launch |
| args | list | stdio | Arguments for the subprocess |
| env | mapping | stdio | Environment passed to the subprocess |
| url | string | HTTP | Remote MCP endpoint |
| headers | mapping | HTTP | Headers for remote server requests |
| ssl_verify | bool or string | HTTP | TLS verification.true(default) uses system CAs,falsedisables verification (insecure), or a string path to a custom CA bundle (PEM) |
| client_cert | string or list | HTTP | mTLS client certificate. String = path to a PEM file containing cert + key. List[cert, key]= separate files. List[cert, key, password]= encrypted key |
| client_key | string | HTTP | Path to the client private key, whenclient_certis a string and the key is in a separate file |
| enabled | bool | both | Skip the server entirely when false |
| timeout | number | both | Tool call timeout in seconds (default:300) |
| connect_timeout | number | both | Initial connection timeout in seconds (default:60) |
| supports_parallel_tool_calls | bool | both | Allow tools from this server to run concurrently |
| skip_preflight | bool | HTTP | Bypass the fail-fast content-type probe for valid Streamable HTTP endpoints whose HEAD/GET answers a non-MCP content type (default:false) |
| tools | mapping | both | Filtering and utility-tool policy |
| auth | string | HTTP | Authentication method. Set tooauthto enable OAuth 2.1 with PKCE |
| sampling | mapping | both | Server-initiated LLM request policy (see MCP guide) |

`command`
`args`
`env`
`url`
`headers`
`ssl_verify`
`true`
`false`
`client_cert`
`[cert, key]`
`[cert, key, password]`
`client_key`
`client_cert`
`enabled`
`timeout`
`300`
`connect_timeout`
`60`
`supports_parallel_tool_calls`
`skip_preflight`
`false`
`tools`
`auth`
`oauth`
`sampling`

## toolspolicy keys​

`tools`
| Key | Type | Meaning |
| --- | --- | --- |
| include | string or list | Whitelist server-native MCP tools |
| exclude | string or list | Blacklist server-native MCP tools |
| resources | bool-like | Enable/disablelist_resources+read_resource |
| prompts | bool-like | Enable/disablelist_prompts+get_prompt |

`include`
`exclude`
`resources`
`list_resources`
`read_resource`
`prompts`
`list_prompts`
`get_prompt`

## Filtering semantics​

### include​

`include`

Ifincludeis set, only those server-native MCP tools are registered.

`include`

```
tools:  include: [create_issue, list_issues]
```

### exclude​

`exclude`

Ifexcludeis set andincludeis not, every server-native MCP tool except those names is registered.

`exclude`
`include`

```
tools:  exclude: [delete_customer]
```

### Precedence​

If both are set,includewins.

`include`

```
tools:  include: [create_issue]  exclude: [create_issue, delete_issue]
```

Result:

- create_issueis still allowed
- delete_issueis ignored becauseincludetakes precedence

`create_issue`
`delete_issue`
`include`

## Utility-tool policy​

Hermes may register these utility wrappers per MCP server:

Resources:

- list_resources
- read_resource

`list_resources`
`read_resource`

Prompts:

- list_prompts
- get_prompt

`list_prompts`
`get_prompt`

### Disable resources​

```
tools:  resources: false
```

### Disable prompts​

```
tools:  prompts: false
```

### Capability-aware registration​

Even whenresources: trueorprompts: true, Hermes only registers those utility tools if the MCP session actually exposes the corresponding capability.

`resources: true`
`prompts: true`

So this is normal:

- you enable prompts
- but no prompt utilities appear
- because the server does not support prompts

## enabled: false​

`enabled: false`

```
mcp_servers:  legacy:    url: "https://mcp.legacy.internal"    enabled: false
```

Behavior:

- no connection attempt
- no discovery
- no tool registration
- config remains in place for later reuse

## Empty result behavior​

If filtering removes all server-native tools and no utility tools are registered, Hermes does not create an empty MCP runtime toolset for that server.

## Example configs​

### Safe GitHub allowlist​

```
mcp_servers:  github:    command: "npx"    args: ["-y", "@modelcontextprotocol/server-github"]    env:      GITHUB_PERSONAL_ACCESS_TOKEN: "***"    tools:      include: [list_issues, create_issue, update_issue, search_code]      resources: false      prompts: false
```

### Stripe blacklist​

```
mcp_servers:  stripe:    url: "https://mcp.stripe.com"    headers:      Authorization: "Bearer ***"    tools:      exclude: [delete_customer, refund_payment]
```

### Resource-only docs server​

```
mcp_servers:  docs:    url: "https://mcp.docs.example.com"    tools:      include: []      resources: true      prompts: false
```

### TLS client certificate (mTLS)​

For HTTP/SSE servers that require a client certificate, setclient_cert(and optionallyclient_key):

`client_cert`
`client_key`

```
mcp_servers:  # Combined cert + key in a single PEM file  internal_api:    url: "https://mcp.internal.example.com/mcp"    client_cert: "~/secrets/mcp-client.pem"  # Separate cert and key files  partner_api:    url: "https://mcp.partner.example.com/mcp"    client_cert: "~/secrets/client.crt"    client_key: "~/secrets/client.key"  # Encrypted key with a passphrase (3-element list form)  bank_api:    url: "https://mcp.bank.example.com/mcp"    client_cert: ["~/secrets/client.crt", "~/secrets/client.key", "my-passphrase"]  # Custom CA bundle (private CA / self-signed server)  lab_api:    url: "https://mcp.lab.local/mcp"    ssl_verify: "~/secrets/lab-ca.pem"    client_cert: "~/secrets/lab-client.pem"
```

Notes:

- Paths support~expansion. Missing files fail fast at connect time with a server-scoped error message.
- ssl_verify: falsedisables server certificate verification entirely. Don't use this with real services.
- Works on both Streamable HTTP and SSE transports.

`~`
`ssl_verify: false`

## Reloading config​

After changing MCP config, reload servers with:

```
/reload-mcp
```

## Tool naming​

Server-native MCP tools become:

```
mcp_<server>_<tool>
```

Examples:

- mcp_github_create_issue
- mcp_filesystem_read_file
- mcp_my_api_query_data

`mcp_github_create_issue`
`mcp_filesystem_read_file`
`mcp_my_api_query_data`

Utility tools follow the same prefixing pattern:

- mcp_<server>_list_resources
- mcp_<server>_read_resource
- mcp_<server>_list_prompts
- mcp_<server>_get_prompt

`mcp_<server>_list_resources`
`mcp_<server>_read_resource`
`mcp_<server>_list_prompts`
`mcp_<server>_get_prompt`

### Name sanitization​

Hyphens (-) and dots (.) in both server names and tool names are replaced with underscores before registration. This ensures tool names are valid identifiers for LLM function-calling APIs.

`-`
`.`

For example, a server namedmy-apiexposing a tool calledlist-items.v2becomes:

`my-api`
`list-items.v2`

```
mcp_my_api_list_items_v2
```

Keep this in mind when writinginclude/excludefilters — use theoriginalMCP tool name (with hyphens/dots), not the sanitized version.

`include`
`exclude`

## OAuth 2.1 authentication​

For HTTP servers that require OAuth, setauth: oauthon the server entry:

`auth: oauth`

```
mcp_servers:  protected_api:    url: "https://mcp.example.com/mcp"    auth: oauth
```

Behavior:

- Hermes uses the MCP SDK's OAuth 2.1 PKCE flow (metadata discovery, dynamic client registration, token exchange, and refresh)
- On first connect, a browser window opens for authorization
- Tokens are persisted to~/.hermes/mcp-tokens/<server>.jsonand reused across sessions
- Token refresh is automatic; re-authorization only happens when refresh fails
- Only applies to HTTP/StreamableHTTP transport (url-based servers)

`~/.hermes/mcp-tokens/<server>.json`
`url`