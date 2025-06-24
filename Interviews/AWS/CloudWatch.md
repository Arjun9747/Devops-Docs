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
***************************************************************************************

| Feature         | **Metrics**                             | **Logs**                                     | **Events** (CloudWatch Events / EventBridge)    |
| --------------- | --------------------------------------- | -------------------------------------------- | ----------------------------------------------- |
| **Definition**  | Time-series data (numbers over time)    | Raw, unstructured or structured textual data | Notifications about system/resource changes     |
| **Data Type**   | Numeric                                 | Text/String                                  | JSON-formatted event objects                    |
| **Purpose**     | Monitor performance, trends, SLAs       | Debug, audit, trace errors                   | Trigger automation, detect system state changes |
| **Granularity** | Aggregated, periodic (1m or 1s)         | Fine-grained, timestamped                    | Real-time or near real-time                     |
| **Retention**   | Up to 15 months                         | Configurable (based on log group settings)   | Logged only if routed (optional)                |
| **Examples**    | CPUUtilization, RequestCount, ErrorRate | “ERROR: Timeout connecting to DB”            | EC2 instance state change, Lambda invoked       |
| **Used for**    | Alarms, dashboards, SLOs, autoscaling   | Troubleshooting, forensic analysis           | Automation via rules (e.g., auto-remediation)   |
| **Sources**     | AWS services, custom apps               | CloudWatch Agent, Lambda, VPC Flow Logs      | AWS service actions or scheduled events         |


**Custom Metric**

```markdown
To set up a custom metric in Amazon CloudWatch, you publish your own numeric data points (e.g., queue size, request count, cache hits) using the PutMetricData API. This allows you to monitor application-specific or business-level KPIs not captured by AWS by default.

| Type                 | Granularity | Use Case                                  | Cost        |
| -------------------- | ----------- | ----------------------------------------- | ----------- |
| **Standard Metrics** | 1-minute    | General monitoring, dashboards, alarms    | Lower cost  |
| **High-Resolution**  | 1-second    | Real-time monitoring, low-latency systems | Higher cost |

🧠 When to Use High-Resolution Metrics:
Use high-resolution (1s) if:

You're monitoring real-time systems (e.g., gaming, trading)

You want fast alarm reaction times (e.g., failover, autoscaling)

You’re tracking short-lived spikes (e.g., bursty traffic)
```
********************************************************************************************************************

**Alarms**

```markdown
A CloudWatch Alarm is a monitoring feature in AWS CloudWatch that watches a single metric (or math expression of metrics) and performs actions based on thresholds you define. It continuously evaluates metric values and changes state when they cross thresholds, allowing for alerting, automation, or scaling actions

📌 Alarm States
OK – Metric is within defined limits
ALARM – Metric has crossed the threshold (e.g., high CPU, low free memory)
INSUFFICIENT_DATA – Not enough data to evaluate the threshold

✅ Follow-up 1: What happens when an alarm transitions from OK to ALARM?
Answer:
When the alarm transitions from OK to ALARM, CloudWatch:
Executes any configured actions:
Sends an SNS notification
Triggers a Lambda function or Auto Scaling policy
Logs the state change in CloudWatch Events
(Optional) Creates an entry in AWS Health Dashboard or incident tracking tools (via integration)
✅ Best practice: always test the action with simulated state changes.

Yes, you can create composite alarms in CloudWatch. These alarms evaluate the state of multiple other alarms using logical expressions (AND, OR, NOT) instead of watching a single metric.

| Scenario                               | Why Composite Alarm Helps                                                    |
| -------------------------------------- | ---------------------------------------------------------------------------- |
| Avoiding noise                         | Only alert when **multiple metrics fail** (e.g., latency **AND** error rate) |
| Creating critical alerts               | Alert only when **all regional alarms** are in `ALARM`                       |
| Combining infrastructure + app signals | Trigger alarm if **CPU is high AND API is slow**                             |
| Suppress flapping alerts               | Alert only on **sustained multiple alarm states**                            |

```
















