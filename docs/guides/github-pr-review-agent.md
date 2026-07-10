---
layout: docs
title: "Agent بررسی PR گیتهاب"
permalink: /docs/guides/github-pr-review-agent/
---

- 
- Guides & Tutorials
- Tutorial: GitHub PR Review Agent

# Tutorial: Build a GitHub PR Review Agent

The problem:Your team opens PRs faster than you can review them. PRs sit for days waiting for eyeballs. Junior devs merge bugs because nobody had time to check. You spend your mornings catching up on diffs instead of building.

The solution:An AI agent that watches your repos around the clock, reviews every new PR for bugs, security issues, and code quality, and sends you a summary — so you only spend time on PRs that actually need human judgment.

What you'll build:

```
┌───────────────────────────────────────────────────────────────────┐│                                                                   ││   Cron Timer  ──▶  Hermes Agent  ──▶  GitHub API  ──▶  Review     ││   (every 2h)       + gh CLI           (PR diffs)       delivery   ││                    + skill                             (Telegram, ││                    + memory                            Discord,   ││                                                        local)     ││                                                                   │└───────────────────────────────────────────────────────────────────┘
```

This guide usescron jobsto poll for PRs on a schedule — no server or public endpoint needed. Works behind NAT and firewalls.

If you have a public endpoint available, check outAutomated GitHub PR Comments with Webhooks— GitHub pushes events to Hermes instantly when PRs are opened or updated.

## Prerequisites​

- Hermes Agent installed— see theInstallation guide
- Gateway runningfor cron jobs:hermes gatewayinstall# Install as a service# orhermes gateway# Run in foreground
- GitHub CLI (gh) installed and authenticated:# Installbrewinstallgh# macOSsudoaptinstallgh# Ubuntu/Debian# Authenticategh auth login
- Messaging configured(optional) —TelegramorDiscord

```
hermes gateway install   # Install as a service# orhermes gateway           # Run in foreground
```

`gh`

```
# Installbrew install gh        # macOSsudo apt install gh    # Ubuntu/Debian# Authenticategh auth login
```

Usedeliver: "local"to save reviews to~/.hermes/cron/output/. Great for testing before wiring up notifications.

`deliver: "local"`
`~/.hermes/cron/output/`

## Step 1: Verify the Setup​

Make sure Hermes can access GitHub. Start a chat:

```
hermes
```

Test with a simple command:

```
Run: gh pr list --repo NousResearch/hermes-agent --state open --limit 3
```

You should see a list of open PRs. If this works, you're ready.

## Step 2: Try a Manual Review​

Still in the chat, ask Hermes to review a real PR:

```
Review this pull request. Read the diff, check for bugs, security issues,and code quality. Be specific about line numbers and quote problematic code.Run: gh pr diff 3888 --repo NousResearch/hermes-agent
```

Hermes will:

1. Executegh pr diffto fetch the code changes
2. Read through the entire diff
3. Produce a structured review with specific findings

`gh pr diff`

If you're happy with the quality, time to automate it.

## Step 3: Create a Review Skill​

A skill gives Hermes consistent review guidelines that persist across sessions and cron runs. Without one, review quality varies.

```
mkdir -p ~/.hermes/skills/code-review
```

Create~/.hermes/skills/code-review/SKILL.md:

`~/.hermes/skills/code-review/SKILL.md`

```
---name: code-reviewdescription: Review pull requests for bugs, security issues, and code quality---# Code Review GuidelinesWhen reviewing a pull request:## What to Check1. **Bugs** — Logic errors, off-by-one, null/undefined handling2. **Security** — Injection, auth bypass, secrets in code, SSRF3. **Performance** — N+1 queries, unbounded loops, memory leaks4. **Style** — Naming conventions, dead code, missing error handling5. **Tests** — Are changes tested? Do tests cover edge cases?## Output FormatFor each finding:- **File:Line** — exact location- **Severity** — Critical / Warning / Suggestion- **What's wrong** — one sentence- **Fix** — how to fix it## Rules- Be specific. Quote the problematic code.- Don't flag style nitpicks unless they affect readability.- If the PR looks good, say so. Don't invent problems.- End with: APPROVE / REQUEST_CHANGES / COMMENT
```

Verify it loaded — starthermesand you should seecode-reviewin the skills list at startup.

`hermes`
`code-review`

## Step 4: Teach It Your Conventions​

This is what makes the reviewer actually useful. Start a session and teach Hermes your team's standards:

```
Remember: In our backend repo, we use Python with FastAPI.All endpoints must have type annotations and Pydantic models.We don't allow raw SQL — only SQLAlchemy ORM.Test files go in tests/ and must use pytest fixtures.
```

```
Remember: In our frontend repo, we use TypeScript with React.No `any` types allowed. All components must have props interfaces.We use React Query for data fetching, never useEffect for API calls.
```

These memories persist forever — the reviewer will enforce your conventions without being told each time.

## Step 5: Create the Automated Cron Job​

Now wire it all together. Create a cron job that runs every 2 hours:

```
hermes cron create "0 */2 * * *" \  "Check for new open PRs and review them.Repos to monitor:- myorg/backend-api- myorg/frontend-appSteps:1. Run: gh pr list --repo REPO --state open --limit 5 --json number,title,author,createdAt2. For each PR created or updated in the last 4 hours:   - Run: gh pr diff NUMBER --repo REPO   - Review the diff using the code-review guidelines3. Format output as:## PR Reviews — today### [repo] #[number]: [title]**Author:** [name] | **Verdict:** APPROVE/REQUEST_CHANGES/COMMENT[findings]If no new PRs found, say: No new PRs to review." \  --name "pr-review" \  --deliver telegram \  --skill code-review
```

Verify it's scheduled:

```
hermes cron list
```

### Other useful schedules​

| Schedule | When |
| --- | --- |
| 0 */2 * * * | Every 2 hours |
| 0 9,13,17 * * 1-5 | Three times a day, weekdays only |
| 0 9 * * 1 | Weekly Monday morning roundup |
| 30m | Every 30 minutes (high-traffic repos) |

`0 */2 * * *`
`0 9,13,17 * * 1-5`
`0 9 * * 1`
`30m`

## Step 6: Run It On Demand​

Don't want to wait for the schedule? Trigger it manually:

```
hermes cron run pr-review
```

Or from within a chat session:

```
/cron run pr-review
```

## Going Further​

### Post Reviews Directly to GitHub​

Instead of delivering to Telegram, have the agent comment on the PR itself:

Add this to your cron prompt:

```
After reviewing, post your review:- For issues: gh pr review NUMBER --repo REPO --comment --body "YOUR_REVIEW"- For critical issues: gh pr review NUMBER --repo REPO --request-changes --body "YOUR_REVIEW"- For clean PRs: gh pr review NUMBER --repo REPO --approve --body "Looks good"
```

Make sureghhas a token withreposcope. Reviews are posted as whoeverghis authenticated as.

`gh`
`repo`
`gh`

### Weekly PR Dashboard​

Create a Monday morning overview of all your repos:

```
hermes cron create "0 9 * * 1" \  "Generate a weekly PR dashboard:- myorg/backend-api- myorg/frontend-app- myorg/infraFor each repo show:1. Open PR count and oldest PR age2. PRs merged this week3. Stale PRs (older than 5 days)4. PRs with no reviewer assignedFormat as a clean summary." \  --name "weekly-dashboard" \  --deliver telegram
```

### Multi-Repo Monitoring​

Scale up by adding more repos to the prompt. The agent processes them sequentially — no extra setup needed.

## Troubleshooting​

### "gh: command not found"​

The gateway runs in a minimal environment. Ensureghis in the system PATH and restart the gateway.

`gh`

### Reviews are too generic​

1. Add thecode-reviewskill (Step 3)
2. Teach Hermes your conventions via memory (Step 4)
3. The more context it has about your stack, the better the reviews

`code-review`

### Cron job doesn't run​

```
hermes gateway status    # Is the gateway running?hermes cron list         # Is the job enabled?
```

### Rate limits​

GitHub allows 5,000 API requests/hour for authenticated users. Each PR review uses ~3-5 requests (list + diff + optional comments). Even reviewing 100 PRs/day stays well within limits.

## What's Next?​

- Webhook-Based PR Reviews— get instant reviews when PRs are opened (requires a public endpoint)
- Daily Briefing Bot— combine PR reviews with your morning news digest
- Build a Plugin— wrap the review logic into a shareable plugin
- Profiles— run a dedicated reviewer profile with its own memory and config
- Fallback Providers— ensure reviews run even when one provider is down