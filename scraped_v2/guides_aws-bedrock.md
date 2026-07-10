- 
- Guides & Tutorials
- AWS Bedrock

# AWS Bedrock

Hermes Agent supports Amazon Bedrock as a native provider using theConverse API— not the OpenAI-compatible endpoint. This gives you full access to the Bedrock ecosystem: IAM authentication, Guardrails, cross-region inference profiles, and all foundation models.

## Prerequisites​

- AWS credentials— any source supported by theboto3 credential chain:IAM instance role (EC2, ECS, Lambda — zero config)AWS_ACCESS_KEY_ID+AWS_SECRET_ACCESS_KEYenvironment variablesAWS_PROFILEfor SSO or named profilesaws configurefor local development
- boto3— install withcd ~/.hermes/hermes-agent && uv pip install -e ".[bedrock]"
- IAM permissions— at minimum:bedrock:InvokeModelandbedrock:InvokeModelWithResponseStream(for inference)bedrock:ListFoundationModelsandbedrock:ListInferenceProfiles(for model discovery)

- IAM instance role (EC2, ECS, Lambda — zero config)
- AWS_ACCESS_KEY_ID+AWS_SECRET_ACCESS_KEYenvironment variables
- AWS_PROFILEfor SSO or named profiles
- aws configurefor local development

`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`
`AWS_PROFILE`
`aws configure`
`cd ~/.hermes/hermes-agent && uv pip install -e ".[bedrock]"`
- bedrock:InvokeModelandbedrock:InvokeModelWithResponseStream(for inference)
- bedrock:ListFoundationModelsandbedrock:ListInferenceProfiles(for model discovery)

`bedrock:InvokeModel`
`bedrock:InvokeModelWithResponseStream`
`bedrock:ListFoundationModels`
`bedrock:ListInferenceProfiles`

On AWS compute, attach an IAM role withAmazonBedrockFullAccessand you're done. No API keys, no.envconfiguration — Hermes detects the instance role automatically.

`AmazonBedrockFullAccess`
`.env`

## Quick Start​

```
# Install with Bedrock supportcd ~/.hermes/hermes-agent && uv pip install -e ".[bedrock]"# Select Bedrock as your providerhermes model# → Choose "More providers..." → "AWS Bedrock"# → Select your region and model# Start chattinghermes chat
```

## Configuration​

After runninghermes model, your~/.hermes/config.yamlwill contain:

`hermes model`
`~/.hermes/config.yaml`

```
model:  default: us.anthropic.claude-sonnet-4-6  provider: bedrock  base_url: https://bedrock-runtime.us-east-2.amazonaws.combedrock:  region: us-east-2
```

### Region​

Set the AWS region in any of these ways (highest priority first):

1. bedrock.regioninconfig.yaml
2. AWS_REGIONenvironment variable
3. AWS_DEFAULT_REGIONenvironment variable
4. Default:us-east-1

`bedrock.region`
`config.yaml`
`AWS_REGION`
`AWS_DEFAULT_REGION`
`us-east-1`

### Guardrails​

To applyAmazon Bedrock Guardrailsto all model invocations:

```
bedrock:  region: us-east-2  guardrail:    guardrail_identifier: "abc123def456"  # From the Bedrock console    guardrail_version: "1"                # Version number or "DRAFT"    stream_processing_mode: "async"       # "sync" or "async"    trace: "disabled"                     # "enabled", "disabled", or "enabled_full"
```

### Model Discovery​

Hermes auto-discovers available models via the Bedrock control plane. You can customize discovery:

```
bedrock:  discovery:    enabled: true    provider_filter: ["anthropic", "amazon"]  # Only show these providers    refresh_interval: 3600                     # Cache for 1 hour
```

## Available Models​

Bedrock models useinference profile IDsfor on-demand invocation. Thehermes modelpicker shows these automatically, with recommended models at the top:

`hermes model`
| Model | ID | Notes |
| --- | --- | --- |
| Claude Sonnet 4.6 | us.anthropic.claude-sonnet-4-6 | Recommended — best balance of speed and capability |
| Claude Opus 4.6 | us.anthropic.claude-opus-4-6-v1 | Most capable |
| Claude Haiku 4.5 | us.anthropic.claude-haiku-4-5-20251001-v1:0 | Fastest Claude |
| Amazon Nova Pro | us.amazon.nova-pro-v1:0 | Amazon's flagship |
| Amazon Nova Micro | us.amazon.nova-micro-v1:0 | Fastest, cheapest |
| DeepSeek V3.2 | deepseek.v3.2 | Strong open model |
| Llama 4 Scout 17B | us.meta.llama4-scout-17b-instruct-v1:0 | Meta's latest |

`us.anthropic.claude-sonnet-4-6`
`us.anthropic.claude-opus-4-6-v1`
`us.anthropic.claude-haiku-4-5-20251001-v1:0`
`us.amazon.nova-pro-v1:0`
`us.amazon.nova-micro-v1:0`
`deepseek.v3.2`
`us.meta.llama4-scout-17b-instruct-v1:0`

Models prefixed withus.use cross-region inference profiles, which provide better capacity and automatic failover across AWS regions. Models prefixed withglobal.route across all available regions worldwide.

`us.`
`global.`

## Switching Models Mid-Session​

Use the/modelcommand during a conversation:

`/model`

```
/model us.amazon.nova-pro-v1:0/model deepseek.v3.2/model us.anthropic.claude-opus-4-6-v1
```

## Diagnostics​

```
hermes doctor
```

The doctor checks:

- Whether AWS credentials are available (env vars, IAM role, SSO)
- Whetherboto3is installed
- Whether the Bedrock API is reachable (ListFoundationModels)
- Number of available models in your region

`boto3`

## Gateway (Messaging Platforms)​

Bedrock works with all Hermes gateway platforms (Telegram, Discord, Slack, Feishu, etc.). Configure Bedrock as your provider, then start the gateway normally:

```
hermes gateway setuphermes gateway start
```

The gateway readsconfig.yamland uses the same Bedrock provider configuration.

`config.yaml`

## Troubleshooting​

### "No API key found" / "No AWS credentials"​

Hermes checks for credentials in this order:

1. AWS_BEARER_TOKEN_BEDROCK
2. AWS_ACCESS_KEY_ID+AWS_SECRET_ACCESS_KEY
3. AWS_PROFILE
4. EC2 instance metadata (IMDS)
5. ECS container credentials
6. Lambda execution role

`AWS_BEARER_TOKEN_BEDROCK`
`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`
`AWS_PROFILE`

If none are found, runaws configureor attach an IAM role to your compute instance.

`aws configure`

### "Invocation of model ID ... with on-demand throughput isn't supported"​

Use aninference profile ID(prefixed withus.orglobal.) instead of the bare foundation model ID. For example:

`us.`
`global.`
- ❌anthropic.claude-sonnet-4-6
- ✅us.anthropic.claude-sonnet-4-6

`anthropic.claude-sonnet-4-6`
`us.anthropic.claude-sonnet-4-6`

### "ThrottlingException"​

You've hit the Bedrock per-model rate limit. Hermes automatically retries with backoff. To increase limits, request a quota increase in theAWS Service Quotas console.

## One-Click AWS Deployment​

For a fully automated deployment on EC2 with CloudFormation:

sample-hermes-agent-on-aws-with-bedrock— creates VPC, IAM role, EC2 instance, and configures Bedrock automatically. Deploy in any region with one click.