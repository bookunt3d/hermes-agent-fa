---
layout: docs
title: "Messaging_Homeassistant"
permalink: /docs/user-guide/messaging/homeassistant/
---

- 
- Messaging Platforms
- Other
- Home Assistant

# Home Assistant Integration

Hermes Agent integrates withHome Assistantin two ways:

1. Gateway platform— subscribes to real-time state changes via WebSocket and responds to events
2. Smart home tools— four LLM-callable tools for querying and controlling devices via the REST API

## Setup​

### 1. Create a Long-Lived Access Token​

1. Open your Home Assistant instance
2. Go to yourProfile(click your name in the sidebar)
3. Scroll toLong-Lived Access Tokens
4. ClickCreate Token, give it a name like "Hermes Agent"
5. Copy the token

### 2. Configure Environment Variables​

```
# Add to ~/.hermes/.env# Required: your Long-Lived Access TokenHASS_TOKEN=your-long-lived-access-token# Optional: HA URL (default: http://homeassistant.local:8123)HASS_URL=http://192.168.1.100:8123
```

Thehomeassistanttoolset is automatically enabled whenHASS_TOKENis set. Both the gateway platform and the device control tools activate from this single token.

`homeassistant`
`HASS_TOKEN`

### 3. Start the Gateway​

```
hermes gateway
```

Home Assistant will appear as a connected platform alongside any other messaging platforms (Telegram, Discord, etc.).

## Available Tools​

Hermes Agent registers four tools for smart home control:

### ha_list_entities​

`ha_list_entities`

List Home Assistant entities, optionally filtered by domain or area.

Parameters:

- domain(optional)— Filter by entity domain:light,switch,climate,sensor,binary_sensor,cover,fan,media_player, etc.
- area(optional)— Filter by area/room name (matches against friendly names):living room,kitchen,bedroom, etc.

`domain`
`light`
`switch`
`climate`
`sensor`
`binary_sensor`
`cover`
`fan`
`media_player`
`area`
`living room`
`kitchen`
`bedroom`

Example:

```
List all lights in the living room
```

Returns entity IDs, states, and friendly names.

### ha_get_state​

`ha_get_state`

Get detailed state of a single entity, including all attributes (brightness, color, temperature setpoint, sensor readings, etc.).

Parameters:

- entity_id(required)— The entity to query, e.g.,light.living_room,climate.thermostat,sensor.temperature

`entity_id`
`light.living_room`
`climate.thermostat`
`sensor.temperature`

Example:

```
What's the current state of climate.thermostat?
```

Returns: state, all attributes, last changed/updated timestamps.

### ha_list_services​

`ha_list_services`

List available services (actions) for device control. Shows what actions can be performed on each device type and what parameters they accept.

Parameters:

- domain(optional)— Filter by domain, e.g.,light,climate,switch

`domain`
`light`
`climate`
`switch`

Example:

```
What services are available for climate devices?
```

### ha_call_service​

`ha_call_service`

Call a Home Assistant service to control a device.

Parameters:

- domain(required)— Service domain:light,switch,climate,cover,media_player,fan,scene,script
- service(required)— Service name:turn_on,turn_off,toggle,set_temperature,set_hvac_mode,open_cover,close_cover,set_volume_level
- entity_id(optional)— Target entity, e.g.,light.living_room
- data(optional)— Additional parameters as a JSON object

`domain`
`light`
`switch`
`climate`
`cover`
`media_player`
`fan`
`scene`
`script`
`service`
`turn_on`
`turn_off`
`toggle`
`set_temperature`
`set_hvac_mode`
`open_cover`
`close_cover`
`set_volume_level`
`entity_id`
`light.living_room`
`data`

Examples:

```
Turn on the living room lights→ ha_call_service(domain="light", service="turn_on", entity_id="light.living_room")
```

```
Set the thermostat to 22 degrees in heat mode→ ha_call_service(domain="climate", service="set_temperature",    entity_id="climate.thermostat", data={"temperature": 22, "hvac_mode": "heat"})
```

```
Set living room lights to blue at 50% brightness→ ha_call_service(domain="light", service="turn_on",    entity_id="light.living_room", data={"brightness": 128, "color_name": "blue"})
```

## Gateway Platform: Real-Time Events​

The Home Assistant gateway adapter connects via WebSocket and subscribes tostate_changedevents. When a device state changes and matches your filters, it's forwarded to the agent as a message.

`state_changed`

### Event Filtering​

By default,no events are forwarded. You must configure at least one ofwatch_domains,watch_entities, orwatch_allto receive events. Without filters, a warning is logged at startup and all state changes are silently dropped.

`watch_domains`
`watch_entities`
`watch_all`

Configure which events the agent sees in~/.hermes/config.yamlunder the Home Assistant platform'sextrasection:

`~/.hermes/config.yaml`
`extra`

```
platforms:  homeassistant:    enabled: true    extra:      watch_domains:        - climate        - binary_sensor        - alarm_control_panel        - light      watch_entities:        - sensor.front_door_battery      ignore_entities:        - sensor.uptime        - sensor.cpu_usage        - sensor.memory_usage      cooldown_seconds: 30
```

| Setting | Default | Description |
| --- | --- | --- |
| watch_domains | (none) | Only watch these entity domains (e.g.,climate,light,binary_sensor) |
| watch_entities | (none) | Only watch these specific entity IDs |
| watch_all | false | Set totrueto receiveallstate changes (not recommended for most setups) |
| ignore_entities | (none) | Always ignore these entities (applied before domain/entity filters) |
| cooldown_seconds | 30 | Minimum seconds between events for the same entity |

`watch_domains`
`climate`
`light`
`binary_sensor`
`watch_entities`
`watch_all`
`false`
`true`
`ignore_entities`
`cooldown_seconds`
`30`

Start with a focused set of domains —climate,binary_sensor, andalarm_control_panelcover the most useful automations. Add more as needed. Useignore_entitiesto suppress noisy sensors like CPU temperature or uptime counters.

`climate`
`binary_sensor`
`alarm_control_panel`
`ignore_entities`

### Event Formatting​

State changes are formatted as human-readable messages based on domain:

| Domain | Format |
| --- | --- |
| climate | "HVAC mode changed from 'off' to 'heat' (current: 21, target: 23)" |
| sensor | "changed from 21°C to 22°C" |
| binary_sensor | "triggered" / "cleared" |
| light,switch,fan | "turned on" / "turned off" |
| alarm_control_panel | "alarm state changed from 'armed_away' to 'triggered'" |
| (other) | "changed from 'old' to 'new'" |

`climate`
`sensor`
`binary_sensor`
`light`
`switch`
`fan`
`alarm_control_panel`

### Agent Responses​

Outbound messages from the agent are delivered asHome Assistant persistent notifications(viapersistent_notification.create). These appear in the HA notification panel with the title "Hermes Agent".

`persistent_notification.create`

### Connection Management​

- WebSocketwith 30-second heartbeat for real-time events
- Automatic reconnectionwith backoff: 5s → 10s → 30s → 60s
- REST APIfor outbound notifications (separate session to avoid WebSocket conflicts)
- Authorization— HA events are always authorized (no user allowlist needed, since theHASS_TOKENauthenticates the connection)

`HASS_TOKEN`

## Security​

The Home Assistant tools enforce security restrictions:

The following service domains areblockedto prevent arbitrary code execution on the HA host:

- shell_command— arbitrary shell commands
- command_line— sensors/switches that execute commands
- python_script— scripted Python execution
- pyscript— broader scripting integration
- hassio— addon control, host shutdown/reboot
- rest_command— HTTP requests from HA server (SSRF vector)

`shell_command`
`command_line`
`python_script`
`pyscript`
`hassio`
`rest_command`

Attempting to call services in these domains returns an error.

Entity IDs are validated against the pattern^[a-z_][a-z0-9_]*\.[a-z0-9_]+$to prevent injection attacks.

`^[a-z_][a-z0-9_]*\.[a-z0-9_]+$`

## Example Automations​

### Morning Routine​

```
User: Start my morning routineAgent:1. ha_call_service(domain="light", service="turn_on",     entity_id="light.bedroom", data={"brightness": 128})2. ha_call_service(domain="climate", service="set_temperature",     entity_id="climate.thermostat", data={"temperature": 22})3. ha_call_service(domain="media_player", service="turn_on",     entity_id="media_player.kitchen_speaker")
```

### Security Check​

```
User: Is the house secure?Agent:1. ha_list_entities(domain="binary_sensor")     → checks door/window sensors2. ha_get_state(entity_id="alarm_control_panel.home")     → checks alarm status3. ha_list_entities(domain="lock")     → checks lock states4. Reports: "All doors closed, alarm is armed_away, all locks engaged."
```

### Reactive Automation (via Gateway Events)​

When connected as a gateway platform, the agent can react to events:

```
[Home Assistant] Front Door: triggered (was cleared)Agent automatically:1. ha_get_state(entity_id="binary_sensor.front_door")2. ha_call_service(domain="light", service="turn_on",     entity_id="light.hallway")3. Sends notification: "Front door opened. Hallway lights turned on."
```

## Troubleshooting​

Environment variables not picked up.The adapter reads credentials from~/.hermes/.env(auto-merged at startup) or
fromconfig.yaml. Double-check the file lives under the active Hermes profile
home and that there's no stray quoting around the URL/token. Restart the gateway
after editing — env changes are only applied on process start.

`~/.hermes/.env`
`config.yaml`

REST auth failing (401 Unauthorized).The token must be aLong-Lived Access Tokencreated from your HA user profile
page (Profile → Security → Long-lived access tokens). Short-lived UI
session tokens won't work. Also verify the base URL includes the scheme and
port (e.g.http://homeassistant.local:8123) and is reachable from the host
running Hermes —curl -H "Authorization: Bearer <token>" <url>/api/should
return{"message": "API running."}.

`401 Unauthorized`
`http://homeassistant.local:8123`
`curl -H "Authorization: Bearer <token>" <url>/api/`
`{"message": "API running."}`