from typing import Collection, Optional
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry import trace

import logging

from opentelemetry.instrumentation.anthropic.package import _instruments
from opentelemetry.instrumentation.anthropic.version import __version__
import anthropic

logger = logging.getLogger(__name__)

TO_WRAP = [
    {
        "object": "Anthropic.completions",
        "method": "create",
        "span_name": "anthropic.completions.create",
    },
]


def no_none(value):
    """
    OTEL Attributes cannot be NoneType.
    If NoneType return string 'None'.
    """
    if value is None:
        return str(value)
    return value


class _InstrumentedAnthropic(anthropic.Anthropic):
    def __init__(
        self,
        tracer_provider: Optional[trace.TracerProvider] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._tracer_provider = tracer_provider
        self.completions.create = self._wrap_completions_create(
            self.completions.create
        )

    def _wrap_completions_create(self, original_func):
        """Wrap 'completions.create' to add telemetry."""

        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(
                __name__,
                __version__,
                self._tracer_provider,
            )
            try:
                with tracer.start_as_current_span(
                    "Anthropic.completions.create"
                ) as span:
                    span.set_attribute("model", kwargs.get("model", "unknown"))
                    span.set_attribute(
                        "max_tokens", kwargs.get("max_tokens_to_sample", 0)
                    )
                    return original_func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Failed to add span: {e}")
                return original_func(*args, **kwargs)

        return wrapper


class AnthropicInstrumentor(BaseInstrumentor):
    """Instrument Anthropic's client library in Python.

    This class adheres to OpenTelemetry's BaseInstrumentor interface and
    provides automatic instrumentation for Anthropic's Python library.
    """

    def __init__(self):
        self._original_anthropic = anthropic.Anthropic

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        self._replace_anthropic_class(tracer_provider)

    def _uninstrument(self, **kwargs):
        self._restore_original_anthropic_class()

    def _replace_anthropic_class(
        self, tracer_provider: Optional[trace.TracerProvider] = None
    ):
        """Replace the original Anthropic class with the instrumented one."""
        anthropic.Anthropic = _InstrumentedAnthropic

    def _restore_original_anthropic_class(self):
        """Restore the original Anthropic class."""
        anthropic.Anthropic = self._original_anthropic

    @staticmethod
    def instrument_instance(
        instance, tracer_provider: Optional[trace.TracerProvider] = None
    ):
        """Instrument a specific instance of the Anthropic class."""
        instance._tracer_provider = tracer_provider
        instance.completions.create = (
            _InstrumentedAnthropic._wrap_completions_create(
                instance.completions.create
            )
        )

    @staticmethod
    def uninstrument_instance(instance):
        """Uninstrument a specific instance of the Anthropic class."""
        instance.completions.create = instance._original_completions_create
