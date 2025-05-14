# Kubernetes Core Concepts
## Overview of Key Kubernetes Objects

### Core Concepts

* **Pod**: Smallest deployable units of computing that can contain one or more containers.
* **Deployment**: Manages the deployment and scaling of Pods.
* **ReplicaSet**: Ensures the specified number of Pod replicas are running.
* **StatefulSet**: Manages stateful applications, providing stable identifiers for Pods.
* **DaemonSet**: Ensures a copy of a Pod runs on all (or some) Nodes.
* **Job**: Manages batch or one-time tasks.
* **CronJob**: Manages scheduled tasks, similar to Linux cron jobs.
* **Service**: Exposes Pods as a network service.
* **Ingress**: Manages external HTTP/S access to services within a cluster.
* **Namespace**: Virtual clusters within a Kubernetes cluster to logically isolate resources.
* **ConfigMap**: Provides configuration data to Pods.
* **Secret**: Stores sensitive information, such as passwords and API tokens.
* **PersistentVolume (PV)**: Storage resource in the cluster.
* **PersistentVolumeClaim (PVC)**: Requests storage resources from PVs.
* **ResourceQuota**: Manages resource usage across Namespaces.
* **Pod Disruption Budget (PDB)**: Ensures a minimum number of Pods are always running during disruptions.

### Advanced Concepts

* **Horizontal Pod Autoscaler (HPA)**: Automatically scales the number of Pods based on CPU utilization or custom metrics.
* **Vertical Pod Autoscaler (VPA)**: Adjusts resource requests and limits of Pods automatically.
* **Mutating & Validating Webhooks**: For custom admission control policies.
* **Custom Resource Definitions (CRDs)**: Extends Kubernetes API with custom objects.
* **Role & RoleBinding**: Manages RBAC permissions for Namespaces.
* **ClusterRole & ClusterRoleBinding**: Manages RBAC permissions cluster-wide.
* **ServiceAccount**: Associates Pods with permissions to communicate with the Kubernetes API.
* **Topology Spread Constraints**: Distributes Pods across zones/nodes for high availability.
* **Finalizers**: Executes clean-up logic before resource deletion.
* **Pod Anti-Affinity & Topology Spread**: Ensures Pods are spread across nodes for high availability.
* **Node Affinity**: Manages Pod scheduling based on node labels.
* **Taints and Tolerations**: Controls which nodes can run specific Pods.

### Networking

* **KubeProxy**: Manages networking for service discovery and load balancing.
* **KubeScheduler**: Determines which node a Pod runs on.
* **Kubelet**: Agent running on each node to ensure containers are running.
* **CNI (Container Network Interface)**: Manages pod networking.
* **Network Policies**: Controls communication between Pods at the network level.
* **Calico / Flannel / Weave**: Network plugins for Kubernetes.
* **Overlay Network vs Underlay Network**: Important for multi-cluster networking.
* **Headless Service**: Directly exposes Pod IPs without load balancing.

### Storage

* **StorageClass**: Defines the storage type and provisioner for dynamic volume provisioning.
* **Volume Snapshots**: Takes snapshots of PVs for backup and recovery.
* **EmptyDir**: Temporary storage for Pods.
* **Generic Ephemeral Volumes**: Flexible storage managed per Pod lifecycle.
* **CSI Ephemeral Volumes**: Ephemeral storage provided by a CSI driver.

### Monitoring & Observability

* **Prometheus/Grafana**: For metrics collection and visualization.
* **Fluentd / ELK Stack**: For centralized logging.
* **Jaeger / Zipkin**: For distributed tracing.

### Security & Compliance

* **Pod Security Policies (PSP)**: Controls security settings on Pods.
* **OPA/Gatekeeper**: Policy enforcement engine for custom policies.
* **Secrets Encryption**: Encrypts sensitive data in etcd.
* **Admission Controllers**: Enforce policies and validate objects during API requests.

### System Components

* **KubeProxy**: Manages networking for service discovery and load balancing.
* **KubeScheduler**: Determines which node a Pod runs on.
* **Kubelet**: Agent running on each node to ensure containers are running.
* **Ambassador**: API Gateway for microservices in Kubernetes.
* **Resource Quotas**: Limits the amount of resources a namespace can consume.
