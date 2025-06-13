**Operator**

Manages the lifecycle of Dynatrace OneAgent, ActiveGate, and DynaKube resources.

Automatically injects agents into pods or nodes depending on the deployment mode.

Acts as the main integration point between your EKS cluster and the Dynatrace platform.

**One Agent**

The core monitoring component installed on your cluster nodes.

Collects infrastructure, pod, container, application, process, and log metrics.

Modes of deployment:

classicFullStack: Full monitoring (app + infra).

cloudNativeFullStack: Uses CSI Driver & init containers for monitoring modern apps.

OneAgent runs as a DaemonSet, meaning one per node.

**Active Gate**

A gateway or relay service that:

Connects your cluster to Dynatrace SaaS (securely handles traffic).

Enables metrics ingestion, synthetic monitoring, and log forwarding.

Manages communication between Dynatrace and Kubernetes API server.

Can host extensions (e.g., cloud services, Prometheus integrations).

**Webhook**

Used for event ingestion (e.g., CI/CD tools, GitOps events).

External tools (e.g., ArgoCD, Jenkins, etc.) can send change events to Dynatrace for:

Deployment tracking

Release validation

Problem correlatio

```markdown
1. You install the Dynatrace Operator via Helm on EKS.
2. Operator deploys OneAgent to each node and configures ActiveGate.
3. OneAgent:
   - Monitors Node, Pod, Container, App, Logs.
   - Collects metrics & traces and sends them to ActiveGate (or directly to Dynatrace).
4. ActiveGate:
   - Relays data to Dynatrace SaaS.
   - Polls Kubernetes API for cluster state.
   - Connects to cloud APIs (e.g., AWS CloudWatch, ALB metrics).
5. Dynatrace platform:
   - Uses Davis AI to analyze telemetry.
   - Displays data via Smartscape, Dashboards, Problems.
6. Webhooks (optional):
   - Receive deployment info from CI/CD tools.
   - Send problem notifications to external systems.
```
