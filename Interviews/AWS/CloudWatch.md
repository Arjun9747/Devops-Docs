Amazon CloudWatch is a monitoring and observability service by AWS that collects and tracks metrics, logs, and events for AWS resources, applications, and custom workloads. It enables you to monitor system performance, detect anomalies, set alarms, and automate responses.

It works by:

Collecting data from AWS services (like EC2, Lambda, RDS)

Accepting custom metrics and logs from applications or on-premise servers

Triggering alarms based on metric thresholds

Visualizing data through dashboards

Enabling event-driven automation using EventBridge or CloudWatch Alarms

🔁 Follow-up: What types of data does CloudWatch collect?
Answer:
CloudWatch collects three main types of observability data:


🔹 Optional: Traces & Alarms
CloudWatch also integrates with:

X-Ray traces (for distributed tracing)

CloudWatch Alarms (monitor thresholds and trigger notifications or actions)

| Data Type | Description                         | Example                                  |
| --------- | ----------------------------------- | ---------------------------------------- |
| Metrics   | Numeric, time-series                | `CPUUtilization`, `Latency`, `Errors`    |
| Logs      | Raw event logs                      | App logs, Lambda logs, VPC Flow Logs     |
| Events    | System-level activity notifications | EC2 state change, scheduled job triggers |
