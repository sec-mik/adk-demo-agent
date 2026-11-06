# ADK Demo Agent

A small customer support agent built with the
[Agent Development Kit (ADK)](https://github.com/google/adk-python). It checks
order status and opens refund requests for a demo online store.

The repository demonstrates an agent security scan on pull requests. The scan
comes from
[mik-sec/agent-security-guardrails](https://github.com/mik-sec/agent-security-guardrails)
and runs through [.github/workflows/agent-security.yml](.github/workflows/agent-security.yml).

## Security patterns in this agent

| Pattern | Where |
| --- | --- |
| The caller's identity comes from `tool_context.user_id`, never from a model-supplied argument | `support_agent/agent.py` |
| Every order lookup checks that the order belongs to that customer | `support_agent/orders.py` |
| Refund requests change state, so a person confirms each call (`require_confirmation=True`) | `support_agent/agent.py` |
| The instruction is a callable, so session state is never interpolated into it | `support_agent/agent.py` |
| Model Armor screens prompts and responses (`ModelArmorPlugin`) | `support_agent/agent.py` |
| Pinned model version and strict safety settings | `support_agent/agent.py` |
| Model calls are capped per invocation (`RunConfig(max_llm_calls=20)`) | `support_agent/agent.py` |

## Run it

```bash
pip install -r requirements.txt
export MODEL_ARMOR_TEMPLATE=projects/<project>/locations/<region>/templates/<template>
adk web .
```

## License

[Apache License 2.0](LICENSE)
