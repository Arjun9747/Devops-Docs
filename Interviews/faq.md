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

```markdown
For logging, I used the standard logging library in Python and structured the logs in JSON format to make them easily parsable by log collectors. Logs included key contextual information like user ID, request ID, and error codes. These logs were emitted to stdout and collected using Fluent Bit, which then forwarded them to our centralized logging platform — in our case, CloudWatch or ELK Stack.

For metrics, I used the prometheus_client library to expose custom metrics like request count, latency, and error rate. These metrics were exposed via a /metrics endpoint and scraped by Prometheus at regular intervals. We then visualized them using Grafana dashboards and configured alerts for thresholds like high latency or increased error rates.
```

**Metrics to Collect**
```markdown
What kind of metrics do you scrape with prometheus in your current organization?

🔧 Infrastructure-level Metrics:
Node Exporter: For CPU usage, memory, disk I/O, and network traffic on EC2 instances or Kubernetes nodes.

Kube-State-Metrics: For Kubernetes object states like pod status, deployment replica count, and resource limits/requests.

cAdvisor: For container-level metrics like CPU/memory per container.

AWS CloudWatch Exporter: To ingest AWS-specific metrics like ELB latency, S3 bucket size, and Lambda invocation errors.

📦 Application-level Metrics:
HTTP Request Count (http_requests_total)

Request Latency (http_request_duration_seconds)

Error Rate (http_requests_total{status="5xx"})

Queue Lengths / Worker Status for background jobs

🧩 Custom Business Metrics:
Number of transactions processed per service

Successful vs failed payment attempts

File generation status (e.g., files_generated_total, files_failed_total)

Cron job execution time and outcome (success/failure)

📊 Visualization & Alerts:
These metrics are visualized in Grafana dashboards, and we configure alert rules using Alertmanager — for example:

Alert if pod restarts exceed a threshold

Alert if API error rate is above 5%

Alert if average response time crosses 2 seconds
```

```markdown
📄 Logs
Definition:
Logs are timestamped, unstructured or structured records of events that happen in your system.

Use Case:
To understand what happened in the system, especially during an error or unexpected behavior.

Examples:

"User login failed for user_id=123"

"Database connection timeout"

Stack traces, debug info, custom error messages

Tools:
CloudWatch Logs, ELK (Elasticsearch, Logstash, Kibana), Fluentd, Loki, Splunk

📊 Metrics
Definition:
Metrics are numeric values that represent the state of your system over time, usually aggregated and quantifiable.

Use Case:
To monitor system health and performance at a glance.

Examples:

CPU usage: 75%

Request count: http_requests_total = 1200

Error rate: 5xx_count = 5

Latency: request_duration_seconds = 0.5

Tools:
Prometheus, CloudWatch Metrics, Datadog, InfluxDB, New Relic

🧵 Traces
Definition:
Traces show the end-to-end flow of a single request through a distributed system, tracking how long each part took.

Use Case:
To pinpoint where latency or errors occur in a multi-service transaction.

Examples:

Trace of a payment request moving through frontend → auth → order service → payment gateway

Shows how much time each microservice took

Highlights bottlenecks or failures
```

**Push and Pull based Metrics**

```markdown
🔁 Pull-Based Monitoring
✅ Definition:
The monitoring system (e.g., Prometheus) pulls metrics by sending HTTP requests to targets (like applications, exporters, etc.) at regular intervals.

🧩 How it works:
The target exposes a /metrics endpoint.

The monitoring system periodically scrapes this endpoint.

📌 Example:
Prometheus scraping /metrics from a Node Exporter or Python app.

✅ Pros:
Easier to control scrape frequency.

Built-in service discovery (e.g., in Kubernetes).

Better suited for large dynamic environments.

❌ Cons:
Targets must be reachable by the monitoring server.

Not ideal for short-lived jobs or behind NAT/firewalls.

📤 Push-Based Monitoring
✅ Definition:
The application or agent pushes metrics to a central server (e.g., Pushgateway, Graphite, Datadog, CloudWatch).

🧩 How it works:
The app or agent sends metrics using HTTP APIs or agents at regular intervals or on-demand.

📌 Example:
A batch job pushes final metrics to Prometheus Pushgateway.

An application sends custom metrics to CloudWatch using PutMetricData.

✅ Pros:
Good for short-lived jobs or apps behind firewalls.

Easier to scale agents pushing data.

Common in cloud-native systems (e.g., AWS CloudWatch, Datadog, New Relic).

❌ Cons:
Less visibility/control from central system.

Harder to detect missing metrics (if push fails).

Risk of data duplication or loss if not handled properly.
```

```markdown
If users report slowness but logs show no errors and CPU is healthy, I follow a layered troubleshooting approach.
First, I check latency metrics and request durations in Prometheus or APM tools to confirm the issue.
I look for signs like slow DB queries, thread pool bottlenecks, or network latency.
If tracing is enabled, I trace a slow request end-to-end to identify which service or component is delaying.
I also check for external API latency, DNS resolution time, or recent deployments.
This helps me narrow down and isolate the root cause quickly.
```

```markdown
In our Kubernetes setup, we use distributed tracing with OpenTelemetry to trace requests across microservices.
Each service is instrumented to generate and propagate trace IDs using the traceparent header.
These spans are collected by the OpenTelemetry Collector, deployed as a sidecar or DaemonSet, and forwarded to Jaeger for visualization.
This allows us to trace a user request end-to-end — for example, from the ingress gateway → auth service → payment → database — and identify where latency or errors occur.
```

```markdown
I’d start by identifying the pod crash reason with kubectl describe pod and confirming it's OOMKilled.
Then, I’d check the memory limits set for the container, and use kubectl top or Prometheus to review actual memory usage.
If memory usage regularly exceeds the limit, I’d adjust the container's memory limits and requests.
If there’s a memory leak or inefficient code, I’d review logs, profile memory, and tune the application.
To prevent future issues, I’d add alerts and consider using VPA to automatically adjust memory based on usage patterns.
```

```markdown
I treat every false alarm as a signal to improve our alerting system.
When woken up unnecessarily, I first classify the alert and check if it was noisy due to poor thresholds or lack of context.
I then tune the alert with better duration, use percentiles, or suppress it during low-impact times.
I also reclassify alerts so that only actionable, high-priority issues page on-call, while lower-priority ones go to Slack or dashboards.
Lastly, I ensure we do a quick retro so we keep improving and reduce alert fatigue over time.
```
