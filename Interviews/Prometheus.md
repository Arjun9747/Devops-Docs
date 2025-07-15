# Prometheus 
```bash
NAME                                             READY   STATUS
alertmanager-kube-prometheus-alertmanager-0      2/2     Running
kube-prometheus-operator-xxx                     1/1     Running
kube-state-metrics-xxx                           1/1     Running
node-exporter-xxxxx                              1/1     Running
prometheus-kube-prometheus-prometheus-0          2/2     Running
grafana-xxxx                                     1/1     Running
```
✅ 1. prometheus-<name>-0
What it is: The Prometheus server pod that scrapes metrics.

Deployed by: Prometheus CR (Custom Resource)

Responsibilities:

Scrape metrics

Apply recording and alerting rules

Store time-series data

Storage: Persistent Volume Claim (PVC)

✅ 2. alertmanager-<name>-0
What it is: Handles alert routing and notifications (email, Slack, etc.).

Deployed by: Alertmanager CR

Responsibilities:

Deduplicates alerts

Groups alerts

Sends notifications via integrations

✅ 3. prometheus-operator-<hash>
What it is: The Kubernetes Operator that manages Prometheus and Alertmanager deployments using CRDs.

Responsibilities:

Watches Prometheus, ServiceMonitor, Alertmanager resources

Automates configuration

✅ 4. kube-state-metrics-<hash>
What it is: Exporter that exposes the state of Kubernetes objects (like Deployments, Pods, etc.) as Prometheus metrics.

Responsibilities:

Doesn't monitor resource usage (that's node_exporter)

Gives object-level visibility (e.g., desired replicas vs current replicas)

✅ 5. node-exporter-<hash>
What it is: A DaemonSet that runs on every node.

Responsibilities:

Collects host-level metrics (CPU, memory, disk, etc.)

✅ 6. grafana-<hash>
What it is: Grafana UI pod used to visualize metrics from Prometheus.

Responsibilities:

Dashboard rendering

Alerting UI (if enabled)

✅ 8. prometheus-node-exporter DaemonSet pods

✅ 10. blackbox-exporter or other exporters (optional)

For monitoring external endpoints (HTTP, TCP, etc.)

To install and integrate Grafana in EKS, the most common and production-ready method is using the Helm chart from the kube-prometheus-stack or standalone Grafana Helm chart.

Not default — added manually
What it is: One per node, exporting system metrics.
```

