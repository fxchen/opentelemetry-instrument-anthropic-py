# opentelemetry-instrument-anthropic-py

Autoinstrumentation for Anthropic's client library.

Project site: https://github.com/fxchen/opentelemetry-instrument-anthropic-py

# Usage

**Installaion**

```
poetry add opentelemetry-instrument-anthropic
poetry run opentelemetry-bootstrap -a install
poetry run opentelemetry-instrument python your_app.py
```

**Using auto instrumentation agent**

```
poetry add opentelemetry-instrument-anthropic
poetry run opentelemetry-bootstrap -a install
poetry run opentelemetry-instrument python your_app.py
```

**Manually**

```
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor

AnthropicInstrumentor().instrument()

client = Anthropic()
client.completions.create(
    prompt=f"{HUMAN_PROMPT}\nHello world\n{AI_PROMPT}",
    )
```

## 🔗 Example ((chat.py)[./example])

In this folder there's a readme on how to:

- Execute a chat completion against Anthropic
- Send traces to your console or your OLTP provider!

# Acknowledgments

Thank you very much to (Philip Carter)[https://github.com/cartermp] and instrumentation by the OpenTelemetry Community! This instrumentation was heavily inspired by conversation and this (OpenAI library)[https://github.com/cartermp/opentelemetry-instrument-openai-py/tree/main].
