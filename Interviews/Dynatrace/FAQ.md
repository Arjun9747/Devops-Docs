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

**Kind of metrics to scrape**

```markdown
"In my current organization, we use Dynatrace extensively for full-stack observability, and we collect a combination of infrastructure, application, and business-level metrics. Here's how it's structured:"

🔹 1. Infrastructure Metrics (via OneAgent or extensions)
CPU, Memory, Disk I/O, Network Usage per host and per container

Process-level metrics, like JVM heap size, garbage collection time

Kubernetes-specific metrics, like:

Pod restarts

Container CPU/Memory limits vs usage

Node pressure (memory/cpu)

Cluster health score

We use Dynatrace’s Kubernetes integration to get per-pod and per-node observability.

🔹 2. Application Metrics
Request count, failure rate, response time — automatically detected through Dynatrace’s Smartscape and PurePath.

Custom service metrics:

Number of active users

Payment success/failure ratio

Login attempts

These are pushed using Dynatrace’s OneAgent SDK or OpenTelemetry integration.

🔹 3. Custom Business Metrics
Tracked via custom events for alerting, such as:

High checkout drop-off rate

Surge in refund requests

In some services, we use the Dynatrace Metric API to push domain-specific metrics like order processing time or inventory sync delays.

🔹 4. Synthetic Monitoring Metrics
Page load times

Availability percentage from various geolocations

Error messages captured during synthetic tests

🔹 5. CI/CD & Deployment Observability
Deployment frequency and failure rates

Performance degradation post-deployment (automatically flagged by Dynatrace)

We integrate Dynatrace with GitHub Actions and ArgoCD to tag new releases and correlate performance issues with deployments.
```

**Logs Metrics and traces**

```markdown
🧱 1. Logs – What happened
Definition: Time-stamped, human-readable or structured records of events that happened in the system.

Used For: Debugging, auditing, investigating errors.
✅ Great for deep debugging and context
❌ Not ideal for real-time trend analysis

📈 2. Metrics – What is happening (quantitatively)
Definition: Numeric values representing the behavior or health of your system over time.
Used For: Alerting, dashboards, trend analysis, performance monitoring.

✅ Efficient, cheap to store, great for alerting
❌ Lacks rich context for root cause

🔍 3. Traces – Why and where it happened
Definition: A trace is the journey of a single request as it flows through various services/components in a distributed system.

Used For: Performance profiling, latency analysis, identifying bottlenecks.

✅ Excellent for debugging microservices and distributed systems
❌ More complex and heavier to instrument
```

**slowness in app but no logs**

```markdown
✅ Step 1: Verify and Scope the Slowness --> Region /AZ specific or any recent deployments

✅ Step 2: Check Application-Level Latency --> high response time/ increase queue

✅ Step 3: Check Downstream Dependencies --> check DB queries, API retires

Check Network/Load Balancer --> check packet drops

check client side--> CDN performance
```

**Trace request for multiple microservices**

```markdown
“To trace a request across multiple microservices in Kubernetes, I implement distributed tracing using standards like OpenTelemetry or tools like Dynatrace, Jaeger, or Datadog APM. Each microservice propagates a unique trace ID through HTTP headers (e.g., traceparent, x-b3-traceid). This allows us to follow the request from the frontend to backend, through service-to-service hops, and view the entire flow as a trace. We instrument the application code and collect telemetry using sidecars, agents, or SDKs, then visualize it in a tracing backend.”
```

