---
layout: docs
title: "Features_Batch Processing"
permalink: /docs/user-guide/features_batch-processing/
---

- 
- Features
- Automation
- Batch Processing

# Batch Processing

Batch processing lets you run the Hermes agent across hundreds or thousands of prompts in parallel, generating structured trajectory data. This is primarily used fortraining data generation— producing ShareGPT-format trajectories with tool usage statistics that can be used for fine-tuning or evaluation.

## Overview​

The batch runner (batch_runner.py) processes a JSONL dataset of prompts, running each through a full agent session with tool access. Each prompt gets its own isolated environment. The output is structured trajectory data with full conversation history, tool call statistics, and reasoning coverage metrics.

`batch_runner.py`

## Quick Start​

```
# Basic batch runpython batch_runner.py \    --dataset_file=data/prompts.jsonl \    --batch_size=10 \    --run_name=my_first_run \    --model=anthropic/claude-sonnet-4.6 \    --num_workers=4# Resume an interrupted runpython batch_runner.py \    --dataset_file=data/prompts.jsonl \    --batch_size=10 \    --run_name=my_first_run \    --resume# List available toolset distributionspython batch_runner.py --list_distributions
```

Batch runs spin up many concurrent agent sessions, each making model calls and tool calls. ANous Portalsubscription bundles model access plus web search, image gen, TTS, and cloud browsers under one bill — useful when you want stable cost-per-trajectory without juggling rate limits across five vendor accounts. Set up withhermes setup --portal, then point--modelat a Nous model.

`hermes setup --portal`
`--model`

## Dataset Format​

The input dataset is a JSONL file (one JSON object per line). Each entry must have apromptfield:

`prompt`

```
{"prompt": "Write a Python function that finds the longest palindromic substring"}{"prompt": "Create a REST API endpoint for user authentication using Flask"}{"prompt": "Debug this error: TypeError: cannot unpack non-iterable NoneType object"}
```

Entries can optionally include:

- imageordocker_image: A container image to use for this prompt's sandbox (works with Docker, Modal, and Singularity backends)
- cwd: Working directory override for the task's terminal session

`image`
`docker_image`
`cwd`

## Configuration Options​

| Parameter | Default | Description |
| --- | --- | --- |
| --dataset_file | (required) | Path to JSONL dataset |
| --batch_size | (required) | Prompts per batch |
| --run_name | (required) | Name for this run (used for output dir and checkpointing) |
| --distribution | "default" | Toolset distribution to sample from |
| --model | claude-sonnet-4.6 | Model to use |
| --base_url | https://openrouter.ai/api/v1 | API base URL |
| --api_key | (env var) | API key for model |
| --max_turns | 10 | Maximum tool-calling iterations per prompt |
| --num_workers | 4 | Parallel worker processes |
| --resume | false | Resume from checkpoint |
| --verbose | false | Enable verbose logging |
| --max_samples | all | Only process first N samples from dataset |
| --max_tokens | model default | Maximum tokens per model response |

`--dataset_file`
`--batch_size`
`--run_name`
`--distribution`
`"default"`
`--model`
`claude-sonnet-4.6`
`--base_url`
`https://openrouter.ai/api/v1`
`--api_key`
`--max_turns`
`10`
`--num_workers`
`4`
`--resume`
`false`
`--verbose`
`false`
`--max_samples`
`--max_tokens`

### Provider Routing (OpenRouter)​

| Parameter | Description |
| --- | --- |
| --providers_allowed | Comma-separated providers to allow (e.g.,"anthropic,openai") |
| --providers_ignored | Comma-separated providers to ignore (e.g.,"together,deepinfra") |
| --providers_order | Comma-separated preferred provider order |
| --provider_sort | Sort by"price","throughput", or"latency" |

`--providers_allowed`
`"anthropic,openai"`
`--providers_ignored`
`"together,deepinfra"`
`--providers_order`
`--provider_sort`
`"price"`
`"throughput"`
`"latency"`

### Reasoning Control​

| Parameter | Description |
| --- | --- |
| --reasoning_effort | Effort level:none,minimal,low,medium,high,xhigh |
| --reasoning_disabled | Completely disable reasoning/thinking tokens |

`--reasoning_effort`
`none`
`minimal`
`low`
`medium`
`high`
`xhigh`
`--reasoning_disabled`

### Advanced Options​

| Parameter | Description |
| --- | --- |
| --ephemeral_system_prompt | System prompt used during execution but NOT saved to trajectories |
| --log_prefix_chars | Characters to show in log previews (default: 100) |
| --prefill_messages_file | Path to JSON file with prefill messages for few-shot priming |

`--ephemeral_system_prompt`
`--log_prefix_chars`
`--prefill_messages_file`

## Toolset Distributions​

Each prompt gets a randomly sampled set of toolsets from adistribution. This ensures training data covers diverse tool combinations. Use--list_distributionsto see all available distributions.

`--list_distributions`

In the current implementation, distributions assign a probability toeach individual toolset. The sampler flips each toolset independently, then guarantees that at least one toolset is enabled. This is different from a hand-authored table of prebuilt combinations.

## Output Format​

All output goes todata/<run_name>/:

`data/<run_name>/`

```
data/my_run/├── trajectories.jsonl    # Combined final output (all batches merged)├── batch_0.jsonl         # Individual batch results├── batch_1.jsonl├── ...├── checkpoint.json       # Resume checkpoint└── statistics.json       # Aggregate tool usage stats
```

### Trajectory Format​

Each line intrajectories.jsonlis a JSON object:

`trajectories.jsonl`

```
{  "prompt_index": 42,  "conversations": [    {"from": "human", "value": "Write a function..."},    {"from": "gpt", "value": "I'll create that function...",     "tool_calls": [...]},    {"from": "tool", "value": "..."},    {"from": "gpt", "value": "Here's the completed function..."}  ],  "metadata": {    "batch_num": 2,    "timestamp": "2026-01-15T10:30:00",    "model": "anthropic/claude-sonnet-4.6"  },  "completed": true,  "partial": false,  "api_calls": 3,  "toolsets_used": ["terminal", "file"],  "tool_stats": {    "terminal": {"count": 2, "success": 2, "failure": 0},    "read_file": {"count": 1, "success": 1, "failure": 0}  },  "tool_error_counts": {    "terminal": 0,    "read_file": 0  }}
```

Theconversationsfield uses a ShareGPT-like format withfromandvaluefields. Tool stats are normalized to include all possible tools with zero defaults, ensuring consistent schema across entries for HuggingFace datasets compatibility.

`conversations`
`from`
`value`

## Checkpointing​

The batch runner has robust checkpointing for fault tolerance:

- Checkpoint file:Saved after each batch completes, tracking which prompt indices are done
- Content-based resume:On--resume, the runner scans existing batch files and matches completed prompts by their actual text content (not just indices), enabling recovery even if the dataset order changes
- Failed prompts:Only successfully completed prompts are marked as done — failed prompts will be retried on resume
- Batch merging:On completion, all batch files (including from previous runs) are merged into a singletrajectories.jsonl

`--resume`
`trajectories.jsonl`

### How Resume Works​

1. Scan allbatch_*.jsonlfiles for completed prompts (by content matching)
2. Filter the dataset to exclude already-completed prompts
3. Re-batch the remaining prompts
4. Process only the remaining prompts
5. Merge all batch files (old + new) into final output

`batch_*.jsonl`

## Quality Filtering​

The batch runner applies automatic quality filtering:

- No-reasoning filter:Samples where zero assistant turns contain reasoning (no<REASONING_SCRATCHPAD>or native thinking tokens) are discarded
- Corrupted entry filter:Entries with hallucinated tool names (not in the valid tool list) are filtered out during the final merge
- Reasoning statistics:Tracks percentage of turns with/without reasoning across the entire run

`<REASONING_SCRATCHPAD>`

## Statistics​

After completion, the runner prints comprehensive statistics:

- Tool usage:Call counts, success/failure rates per tool
- Reasoning coverage:Percentage of assistant turns with reasoning
- Samples discarded:Count of samples filtered for lacking reasoning
- Duration:Total processing time

Statistics are also saved tostatistics.jsonfor programmatic analysis.

`statistics.json`

## Use Cases​

### Training Data Generation​

Generate diverse tool-use trajectories for fine-tuning:

```
python batch_runner.py \    --dataset_file=data/coding_prompts.jsonl \    --batch_size=20 \    --run_name=coding_v1 \    --model=anthropic/claude-sonnet-4.6 \    --num_workers=8 \    --distribution=default \    --max_turns=15
```

### Model Evaluation​

Evaluate how well a model uses tools across standardized prompts:

```
python batch_runner.py \    --dataset_file=data/eval_suite.jsonl \    --batch_size=10 \    --run_name=eval_gpt4 \    --model=openai/gpt-4o \    --num_workers=4 \    --max_turns=10
```

### Per-Prompt Container Images​

For benchmarks requiring specific environments, each prompt can specify its own container image:

```
{"prompt": "Install numpy and compute eigenvalues of a 3x3 matrix", "image": "python:3.11-slim"}{"prompt": "Compile this Rust program and run it", "image": "rust:1.75"}{"prompt": "Set up a Node.js Express server", "image": "node:20-alpine", "cwd": "/app"}
```

The batch runner verifies Docker images are accessible before running each prompt.