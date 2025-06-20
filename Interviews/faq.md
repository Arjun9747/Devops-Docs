```markdown
🔍 Monitoring:
Definition:
Monitoring is the act of collecting and analyzing predefined metrics to detect known problems or anomalies in a system.

Purpose:
To tell you what is wrong using dashboards, alerts, and logs.

Characteristics:

Uses predefined rules and thresholds.

Answers known questions like “Is the server CPU above 80%?”

Reactive in nature (detects issues after they occur).

Limited visibility into unknown or complex failures.

Tools: Prometheus, CloudWatch, Datadog (metrics/dashboards), Nagios.

🧠 Observability:
Definition:
Observability is a property of a system that allows you to understand its internal state from its external outputs (logs, metrics, traces).

Purpose:
To help you understand why something is wrong, especially in complex, distributed systems.

Characteristics:

Not limited to predefined metrics.

Helps debug unknown or novel issues.

Proactive and diagnostic in nature.

Built on the three pillars: Logs, Metrics, Traces.

Tools: Grafana, OpenTelemetry, Jaeger, Honeycomb, New Relic.
```
