```markdown
🚨 Monitoring – What is happening?
Definition: Monitoring is the process of collecting, processing, and analyzing data from systems to track their health and performance.

Goal: Detect known issues, anomalies, or predefined thresholds.

Approach: Reactive — you set alerts based on known failure modes.

Examples:

CPU usage > 90% alert

Memory leak detection

HTTP 500 errors rate exceeds threshold

Tools: Prometheus, Nagios, CloudWatch, Zabbix, New Relic, Dynatrace, Datadog (for traditional monitoring).

🔍 Observability – Why is it happening?
Definition: Observability is the ability to understand the internal state of a system based on external outputs (like logs, metrics, traces).

Goal: Investigate unknown issues, debug complex distributed systems, and find root causes.

Approach: Proactive — enables you to explore new, unpredictable failure modes.

Core Pillars:

Logs – Event details

Metrics – Time-series data (e.g., CPU, request count)

Traces – End-to-end journey of a request

Tools: OpenTelemetry, Grafana Tempo, Jaeger, Honeycomb, Lightstep, Datadog APM, Dynatrace (observability platforms).
```

**how to emit custom logs and metrics in your application ?**

```markdown
"In my recent application deployments, especially microservices running in containers on AWS, I implemented both custom logging and metrics to improve observability and debugging efficiency.

For logging, I used structured JSON logs with the standard logging module in Python. I ensured logs included contextual fields like timestamp, log level, service name, and correlation ID for traceability. These logs were emitted to stdout, captured by Fluent Bit, and sent to ELK (or CloudWatch Logs in AWS setups).

For custom metrics, I used the prometheus_client library in Python. I exposed an endpoint (/metrics) where we published custom metrics like:

request_count (Counter)

cpu_load (Gauge)

request_latency_seconds (Histogram)

This allowed Prometheus to scrape data regularly, and we visualized it using Grafana dashboards.**

The benefit was twofold:

We reduced MTTR during incidents because logs were searchable and metrics showed patterns over time.

Developers could proactively monitor new features with real-time metrics, improving feedback loops.**
```
