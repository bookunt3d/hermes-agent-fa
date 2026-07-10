---
layout: docs
title: "اتوماسیون با Cron"
permalink: /docs/guides/automate-with-cron/
---

- 
- Guides & Tutorials
- Automate Anything with Cron

# Automate Anything with Cron

Thedaily briefing bot tutorialcovers the basics. This guide goes further — five real-world automation patterns you can adapt for your own workflows.

For the full feature reference, seeScheduled Tasks (Cron).

Cron jobs run in fresh agent sessions with no memory of your current chat. Prompts must becompletely self-contained— include everything the agent needs to know.

- Recurring watchdogwhere the script already produces the exact message (memory alerts, disk alerts, heartbeats): usescript-only cron jobs. Same scheduler, no LLM. You can ask Hermes to set one up for you in chat — thecronjobtool knows when to pickno_agent=Trueand writes the script for you.
- One-shot from a script that's already running(CI step, post-commit hook, deploy script, externally-scheduled monitor): usehermes sendto pipe stdout or a file straight to Telegram / Discord / Slack / etc. without setting up a cron entry.

`cronjob`
`no_agent=True`
`hermes send`

## Pattern 1: Website Change Monitor​

Watch a URL for changes and get notified only when something is different.

Thescriptparameter is the secret weapon here. A Python script runs before each execution, and its stdout becomes context for the agent. The script handles the mechanical work (fetching, diffing); the agent handles the reasoning (is this change interesting?).

`script`

Create the monitoring script:

```
mkdir -p ~/.hermes/scripts
```

```
import hashlib, json, os, urllib.requestURL = "https://example.com/pricing"STATE_FILE = os.path.expanduser("~/.hermes/scripts/.watch-site-state.json")# Fetch current contentreq = urllib.request.Request(URL, headers={"User-Agent": "Hermes-Monitor/1.0"})content = urllib.request.urlopen(req, timeout=30).read().decode()current_hash = hashlib.sha256(content.encode()).hexdigest()# Load previous stateprev_hash = Noneif os.path.exists(STATE_FILE):    with open(STATE_FILE) as f:        prev_hash = json.load(f).get("hash")# Save current statewith open(STATE_FILE, "w") as f:    json.dump({"hash": current_hash, "url": URL}, f)# Output for the agentif prev_hash and prev_hash != current_hash:    print(f"CHANGE DETECTED on {URL}")    print(f"Previous hash: {prev_hash}")    print(f"Current hash: {current_hash}")    print(f"\nCurrent content (first 2000 chars):\n{content[:2000]}")else:    print("NO_CHANGE")
```

Set up the cron job:

```
/cron add "every 1h" "If the script output says CHANGE DETECTED, summarize what changed on the page and why it might matter. If it says NO_CHANGE, respond with just [SILENT]." --script ~/.hermes/scripts/watch-site.py --name "Pricing monitor" --deliver telegram
```

For cron monitoring jobs, instruct the agent to respond with only[SILENT]when nothing changed. Cron delivery treats[SILENT]as the quiet marker, so you only get notified when something actually happens — no spam on quiet hours.

`[SILENT]`
`[SILENT]`

## Pattern 2: Weekly Report​

Compile information from multiple sources into a formatted summary. This runs once a week and delivers to your home channel.

```
/cron add "0 9 * * 1" "Generate a weekly report covering:1. Search the web for the top 5 AI news stories from the past week2. Search GitHub for trending repositories in the 'machine-learning' topic3. Check Hacker News for the most discussed AI/ML postsFormat as a clean summary with sections for each source. Include links.Keep it under 500 words — highlight only what matters." --name "Weekly AI digest" --deliver telegram
```

From the CLI:

```
hermes cron create "0 9 * * 1" \  "Generate a weekly report covering the top AI news, trending ML GitHub repos, and most-discussed HN posts. Format with sections, include links, keep under 500 words." \  --name "Weekly AI digest" \  --deliver telegram
```

The0 9 * * 1is a standard cron expression: 9:00 AM every Monday.

`0 9 * * 1`

## Pattern 3: GitHub Repository Watcher​

Monitor a repository for new issues, PRs, or releases.

```
/cron add "every 6h" "Check the GitHub repository NousResearch/hermes-agent for:- New issues opened in the last 6 hours- New PRs opened or merged in the last 6 hours- Any new releasesUse the terminal to run gh commands:  gh issue list --repo NousResearch/hermes-agent --state open --json number,title,author,createdAt --limit 10  gh pr list --repo NousResearch/hermes-agent --state all --json number,title,author,createdAt,mergedAt --limit 10Filter to only items from the last 6 hours. If nothing new, respond with [SILENT].Otherwise, provide a concise summary of the activity." --name "Repo watcher" --deliver discord
```

Notice how the prompt includes the exactghcommands. The cron agent has no memory of previous runs or your preferences — spell everything out.

`gh`

## Pattern 4: Data Collection Pipeline​

Scrape data at regular intervals, save to files, and detect trends over time. This pattern combines a script (for collection) with the agent (for analysis).

```
import json, os, urllib.requestfrom datetime import datetimeDATA_DIR = os.path.expanduser("~/.hermes/data/prices")os.makedirs(DATA_DIR, exist_ok=True)# Fetch current data (example: crypto prices)url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"data = json.loads(urllib.request.urlopen(url, timeout=30).read())# Append to history fileentry = {"timestamp": datetime.now().isoformat(), "prices": data}history_file = os.path.join(DATA_DIR, "history.jsonl")with open(history_file, "a") as f:    f.write(json.dumps(entry) + "\n")# Load recent history for analysislines = open(history_file).readlines()recent = [json.loads(l) for l in lines[-24:]]  # Last 24 data points# Output for the agentprint(f"Current: BTC=${data['bitcoin']['usd']}, ETH=${data['ethereum']['usd']}")print(f"Data points collected: {len(lines)} total, showing last {len(recent)}")print(f"\nRecent history:")for r in recent[-6:]:    print(f"  {r['timestamp']}: BTC=${r['prices']['bitcoin']['usd']}, ETH=${r['prices']['ethereum']['usd']}")
```

```
/cron add "every 1h" "Analyze the price data from the script output. Report:1. Current prices2. Trend direction over the last 6 data points (up/down/flat)3. Any notable movements (>5% change)If prices are flat and nothing notable, respond with [SILENT].If there's a significant move, explain what happened." \  --script ~/.hermes/scripts/collect-prices.py \  --name "Price tracker" \  --deliver telegram
```

The script does the mechanical collection; the agent adds the reasoning layer.

## Pattern 5: Multi-Skill Workflow​

Chain skills together for complex scheduled tasks. Skills are loaded in order before the prompt executes.

```
# Use the arxiv skill to find papers, then the obsidian skill to save notes/cron add "0 8 * * *" "Search arXiv for the 3 most interesting papers on 'language model reasoning' from the past day. For each paper, create an Obsidian note with the title, authors, abstract summary, and key contribution." \  --skill arxiv \  --skill obsidian \  --name "Paper digest"
```

From the tool directly:

```
cronjob(    action="create",    skills=["arxiv", "obsidian"],    prompt="Search arXiv for papers on 'language model reasoning' from the past day. Save the top 3 as Obsidian notes.",    schedule="0 8 * * *",    name="Paper digest",    deliver="local")
```

Skills are loaded in order —arxivfirst (teaches the agent how to search papers), thenobsidian(teaches how to write notes). The prompt ties them together.

`arxiv`
`obsidian`

## Managing Your Jobs​

```
# List all active jobs/cron list# Trigger a job immediately (for testing)/cron run <job_id># Pause a job without deleting it/cron pause <job_id># Edit a running job's schedule or prompt/cron edit <job_id> --schedule "every 4h"/cron edit <job_id> --prompt "Updated task description"# Add or remove skills from an existing job/cron edit <job_id> --skill arxiv --skill obsidian/cron edit <job_id> --clear-skills# Remove a job permanently/cron remove <job_id>
```

## Delivery Targets​

The--deliverflag controls where results go:

`--deliver`
| Target | Example | Use case |
| --- | --- | --- |
| origin | --deliver origin | Same chat that created the job (default) |
| local | --deliver local | Save to local file only |
| telegram | --deliver telegram | Your Telegram home channel |
| discord | --deliver discord | Your Discord home channel |
| slack | --deliver slack | Your Slack home channel |
| Specific chat | --deliver telegram:-1001234567890 | A specific Telegram group |
| Threaded | --deliver telegram:-1001234567890:17585 | A specific Telegram topic thread |

`origin`
`--deliver origin`
`local`
`--deliver local`
`telegram`
`--deliver telegram`
`discord`
`--deliver discord`
`slack`
`--deliver slack`
`--deliver telegram:-1001234567890`
`--deliver telegram:-1001234567890:17585`

## Tips​

Make prompts self-contained.The agent in a cron job has no memory of your conversations. Include URLs, repo names, format preferences, and delivery instructions directly in the prompt.

Use[SILENT]deliberately.For monitoring jobs, include instructions like "if nothing changed, respond with only[SILENT]." Do not ask the agent to explain the token in quiet cases — cron treats[SILENT]as the delivery-suppression marker.

`[SILENT]`
`[SILENT]`
`[SILENT]`

Use scripts for data collection.Thescriptparameter lets a Python script handle the boring parts (HTTP requests, file I/O, state tracking). The agent only sees the script's stdout and applies reasoning to it. This is cheaper and more reliable than having the agent do the fetching itself.

`script`

Test with/cron run.Before waiting for the schedule to trigger, use/cron run <job_id>to execute immediately and verify the output looks right.

`/cron run`
`/cron run <job_id>`

Schedule expressions.Supported formats: relative delays (30m), intervals (every 2h), standard cron expressions (0 9 * * *), and ISO timestamps (2025-06-15T09:00:00). Natural language likedaily at 9amis not supported — use0 9 * * *instead.

`30m`
`every 2h`
`0 9 * * *`
`2025-06-15T09:00:00`
`daily at 9am`
`0 9 * * *`

For the complete cron reference — all parameters, edge cases, and internals — seeScheduled Tasks (Cron).