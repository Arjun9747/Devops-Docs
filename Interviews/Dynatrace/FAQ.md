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
