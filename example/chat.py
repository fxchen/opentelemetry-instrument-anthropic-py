from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from opentelemetry import trace

# If you don't want to use full autoinstrumentation, just add this:
# from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor
# AnthropicInstrumentor().instrument()

tracer = trace.get_tracer("chat.demo")

DEFAULT_ANTHROPIC_MODEL = "claude-instant-1.2"

client = Anthropic()


def prepare_anthropic_kwargs(model: str, prompt: str, max_tokens: int) -> dict:
    """
    Prepares the keyword arguments for the Claude API call.

    Args:
      prompt: str, the prompt to use for the API call
      model: str, the model to use for the API call
      max_tokens: int, the maximum number of tokens to use for the API call

    Returns:
      dict: The keyword arguments for the API call
    """
    kwargs = {
        "model": model,
        "max_tokens_to_sample": max_tokens,
        "prompt": f"{HUMAN_PROMPT}\n{prompt}\n{AI_PROMPT}",
    }
    return kwargs


with tracer.start_as_current_span("example") as span:
    client = Anthropic()
    span.set_attribute("attr1", 12)
    kwargs = prepare_anthropic_kwargs(
        DEFAULT_ANTHROPIC_MODEL, "hello world", 2048
    )

    response = client.completions.create(**kwargs)

    print(response.completion.strip())
