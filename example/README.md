# chat.py example

**Installation**

- Rename env.example to .env
- Set your Anthropic API key

**To run this locally**
```
poetry lock
poetry install
poetry run opentelemetry-instrument \
  --traces_exporter console \
  --metrics_exporter none \
  --logs_exporter none \
  python chat.py
```


**To export your traces to your OLTP provider**
```
OTEL_EXPORTER_OTLP_ENDPOINT="https://api.honeycomb.io" \
OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=YOUR_API_KEY" \
poetry run opentelemetry-instrument python chat.py
```

