# Kubernetes Concepts Checklist

## Core Concepts

* **Pod**: Smallest deployable units of computing that can contain one or more containers.
	+ Use Case: Running containerized applications.
* **Deployment**: Manages the deployment and scaling of Pods.
	+ Use Case: Stateless applications and rolling updates.
* **ReplicaSet**: Ensures the specified number of Pod replicas are running.
	+ Use Case: High availability and redundancy.
* **StatefulSet**: Manages stateful applications, providing stable identifiers for Pods.
	+ Use Case: Databases and distributed applications requiring stable identity.
* **DaemonSet**: Ensures a copy of a Pod runs on all (or some) Nodes.
	+ Use Case: Log collection, monitoring agents.
* **Job**: Manages batch or one-time tasks.
	+ Use Case: Data processing jobs, image processing.
* **CronJob**: Manages scheduled tasks, similar to Linux cron jobs.
	+ Use Case: Database backups, report generation.
* **Service**: Exposes Pods as a network service.
	+ Use Case: Internal communication between microservices.
* **Ingress**: Manages external HTTP/S access to services within a cluster.
	+ Use Case: Routing traffic to backend services.
* **Namespace**: Virtual clusters within a Kubernetes cluster to logically isolate resources.
	+ Use Case: Multi-tenant environments.
* **ConfigMap**: Provides configuration data to Pods.
	+ Use Case: Application configuration without rebuilding images.
* **Secret**: Stores sensitive information, such as passwords and API tokens.
	+ Use Case: Securing database credentials, API keys.
* **PersistentVolume (PV)**: Storage resource in the cluster.
	+ Use Case: Long-term storage for databases or logs.
* **PersistentVolumeClaim (PVC)**: Requests storage resources from PVs.
	+ Use Case: Claiming storage for specific applications.
* **ResourceQuota**: Manages resource usage across Namespaces.
	+ Use Case: Controlling resource consumption.
* **Pod Disruption Budget (PDB)**: Ensures a minimum number of Pods are always running during disruptions.
	+ Use Case: Ensuring availability during upgrades.
* **Init Container**: Special containers that run before the main application containers start.
	+ Use Case: Initialization logic such as database migrations.

## Networking

* **KubeProxy**: Manages networking for service discovery and load balancing.
	+ Use Case: Distributing traffic within the cluster.
* **KubeScheduler**: Determines which node a Pod runs on.
	+ Use Case: Ensuring balanced resource utilization.
* **Kubelet**: Agent running on each node to ensure containers are running.
	+ Use Case: Managing pod lifecycle on worker nodes.
* **CNI (Container Network Interface)**: Manages pod networking.
	+ Use Case: Integrating different networking plugins.
* **Network Policies**: Controls communication between Pods at the network level.
	+ Use Case: Securing inter-Pod communication.
* **Calico / Flannel / Weave**: Network plugins for Kubernetes.
	+ Use Case: Overlay networking for multi-cluster communication.
* **Overlay Network vs Underlay Network**: Important for multi-cluster networking.
	+ Use Case: Traffic routing across nodes and regions.
* **Headless Service**: Directly exposes Pod IPs without load balancing.
	+ Use Case: Service discovery within StatefulSets.
* **ClusterIP**: Exposes the service on a cluster-internal IP.
	+ Use Case: Internal microservice communication.
* **NodePort**: Exposes the service on each Node's IP at a static port.
	+ Use Case: Directly accessing a service from outside the cluster.
* **LoadBalancer**: Exposes the service externally using a cloud provider's load balancer.
	+ Use Case: Publicly accessible web applications.

## Advanced Concepts

* **Custom Resource Definitions**

* **Mutating & Validating Webhooks**

* **Finalizers**: Ensures specific cleanup logic before the resource is removed.
	+ Use Case: Graceful deletion of dependent resources.
* **Horizontal Pod Autoscaler (HPA)**: Automatically scales the number of pods based on metrics.
	+ Use Case: Scaling applications based on CPU or memory usage.
* **Vertical Pod Autoscaler (VPA)**: Automatically adjusts the resource limits and requests of pods.
	+ Use Case: Optimizing resource allocation for cost and performance.
* **Pod Anti-Affinity / Topology Spread Constraints**: Controls pod distribution across nodes.
	+ Use Case: Avoiding single-point failures.
* **Node Affinity**: Controls which nodes a pod can be scheduled on.
	+ Use Case: Scheduling Pods on high-memory or GPU nodes.
* **Taints and Tolerations**: Restricts or allows pods to be scheduled on specific nodes.
	+ Use Case: Isolating critical workloads from general workloads.

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

**IRSA**
```markdown
 IAM Roles for Service Accounts
 IRSA allows EKS pods to assume AWS IAM roles securely, without needing to hardcode AWS credentials

You have a pod that needs to read from an S3 bucket. Instead of giving the entire EKS node IAM permissions (too broad), you use IRSA to assign a specific IAM role just to that pod's service account.

set IAM trust polcies conditions --> for S3 access to pod

For user

Use k8s RBAC

Create Role

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: my-namespace

Create Role-binding

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-binding
  namespace: my-namespace

Kubernetes doesn't have a user database. Instead, EKS integrates with AWS IAM for authentication. But you must explicitly map IAM users or roles to Kubernetes users or groups using a config file called aws-auth.

They authenticate using IAM credentials (via aws eks update-kubeconfig).
IAM Authenticator verifies the IAM identity (user/role).
The EKS cluster maps that IAM identity to a Kubernetes user or group (via aws-auth ConfigMap).
Kubernetes checks RBAC rules to see what the user is allowed to do.

map the user

kubectl edit configmap aws-auth -n kube-system

mapUsers: |
  - userarn: arn:aws:iam::111122223333:user/dev-user
    username: dev-user@example.com
    groups:
      - dev-group

Create an RBAC Role for That Group

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: dev-role
```

```markdown

Pod to S3

✅ Create an IAM Role with S3 permissions and trust policy for the service account

✅ Create a Kubernetes service account in the specific namespace

✅ Deploy your pod using that service account

✅ Your pod will now access S3 using AWS SDK (no secrets needed)

```





