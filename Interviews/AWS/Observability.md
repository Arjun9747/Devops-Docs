Designed and implemented centralized observability using Grafana, Loki, Mimir, 
and Grafana Alloy for collecting and routing metrics and logs across multiple AWS accounts.

At the service level, Alloy is configured to scrape Prometheus exporters and collect application logs.
Both metrics and logs are forwarded using OTLP to a central Alloy endpoint, so applications don’t talk directly to Loki or Mimir.

“CloudWatch gives us AWS service metrics, but Alloy gives us application-level observability and a unified ingestion layer. We use Alloy to standardize, enrich, and route telemetry across services and accounts, 
which CloudWatch alone cannot do.”

Implemented team-scoped Grafana folders and permissions to support multi-tenant usage of a centralized observability platform.

Dataflow 


Application
  ↓
Prometheus Exporter
  ↓
Local Alloy (scrape)
  ↓
Central Alloy (OTLP / remote_write)
  ↓ (Transit Gateway)
Mimir (Central Account)
  ↓
S3 (long-term storage)
  ↓
Grafana (queries)

CloudWatch (ELB, ECS, RDS)
  ↓
Central Alloy (CloudWatch discovery)
  ↓
Mimir
  ↓
Grafana

Why this architecture is GOOD (sell it in interviews)
✅ Scalability
	• Mimir & Loki scale horizontally
	• Alloy is lightweight and elastic
	• No single Prometheus bottleneck
✅ Reliability
	• Failure in one app account does not affect others
	• Local buffering prevents data loss
	• Central account is isolated
✅ Cost control
	• Early filtering in Alloy
	• S3-based long-term storage
	• No per-team Grafana instances
✅ Governance
	• Centralized dashboards
	• Consistent labels
	• Controlled data egress



“Our observability platform follows a hub-and-spoke model. Each application runs on ECS Fargate and includes a local Alloy instance that collects logs and metrics from the application and Prometheus exporters.
These are forwarded to a central Alloy running in the same application account, which acts as an aggregation and policy layer. The central Alloy also discovers AWS service metrics via CloudWatch.
All telemetry is securely pushed through a Transit Gateway to a central observability account where Loki stores logs and Mimir stores metrics, both backed by S3 for long-term retention. Grafana runs in the same account and queries Loki and Mimir to provide a unified observability view across all environments.”

❓ Why not Prometheus everywhere?
	Prometheus does not scale well centrally; Mimir gives HA, multi-tenancy, and long-term storage.
❓ Why Alloy instead of Fluent Bit / OTEL Collector?
	Alloy unifies Prometheus, Loki, and OTEL pipelines with native Grafana ecosystem support.
❓ How do you handle noisy logs/metrics?
	Label filtering and drop rules in central Alloy before data leaves the account




