# Amazon EKS Architect Interview Preparation: End-to-End Application Design

## 1. Objective

Design, deploy, secure, expose, scale, and troubleshoot a production-grade application running on Amazon EKS.

This exercise covers both **high-level architecture and low-level implementation details**. The goal is to demonstrate practical understanding of the complete application lifecycle, including Kubernetes APIs, image pulls from Amazon ECR, scheduling, CNI networking, IAM, VPC endpoints, load balancing, autoscaling, and troubleshooting.

### What I should be able to demonstrate

- Explain the complete request lifecycle from a developer's deployment to a running application.
- Explain what happens internally when I run `kubectl apply`.
- Explain how EKS control plane components interact with worker nodes.
- Trace how a node pulls a private container image from ECR.
- Explain VPC CNI, pod IP allocation, ENIs, routing, and security groups.
- Explain Kubernetes scheduling, resource requests, affinity, taints, and tolerations.
- Explain the difference between the EKS API endpoint, Kubernetes API server, AWS service APIs, and application APIs.
- Explain ECR, S3, STS, EC2, and Elastic Load Balancing VPC endpoints.
- Explain endpoint policies versus IAM policies, repository policies, security groups, and Kubernetes RBAC.
- Troubleshoot Pending pods, ImagePullBackOff, CrashLoopBackOff, DNS failures, 503 errors, and inaccessible AWS services.

---

## 2. The interview question

### Scenario: Design a production application on EKS

You are the AWS EKS Architect for an enterprise application.

A development team has built a containerized REST API. The source code is stored in GitHub. The Docker image must be built, scanned, and pushed to a private Amazon ECR repository. The application must run on Amazon EKS and serve users globally.

Design the complete solution using the following requirements.

**Application requirements**

1. The application must run on an EKS cluster spanning three Availability Zones.
2. The application must have multiple replicas and survive a worker-node or Availability Zone failure.
3. Container images must be pulled from a private ECR repository.
4. Worker nodes must run in private subnets.
5. Users must access the application over HTTPS.
6. The application must connect to an S3 bucket, a database, and other internal services.
7. The application must scale when traffic increases.
8. Application pods must not receive unnecessary AWS permissions.
9. Kubernetes administrative access must be restricted.
10. The cluster must be observable, auditable, and recoverable.
11. The architecture must support deployment rollback and controlled production releases.

### Additional constraints

- The cluster should not depend on unrestricted outbound internet access.
- ECR access must be restricted as far as practical.
- Only authorized engineers and CI/CD pipelines may deploy workloads.
- The application must not run with privileged containers or unnecessary root access.
- The design must include monitoring, alerting, and incident troubleshooting.

### Interview deliverables

Explain and draw:

- High-level architecture.
- VPC and subnet design.
- EKS control plane and data plane.
- CI/CD and ECR image-pull flow.
- Kubernetes API and scheduling flow.
- Pod networking and service discovery.
- Application request lifecycle.
- IAM, endpoint policies, and network security.
- Scaling and high availability.
- Troubleshooting procedures.

---

## 3. High-level architecture

```text
                         DEVELOPERS
                             |
                         GitHub
                             |
                    GitHub Actions CI/CD
                             |
                Build -> Test -> Scan Image
                             |
                       Push to ECR
                             |
                     Private ECR Repository


 USERS / GLOBAL TRAFFIC
          |
          v
   Route 53 / DNS
          |
          v
   AWS Global Accelerator (optional)
          |
          v
   Application Load Balancer
       /       |       \
      AZ-A    AZ-B     AZ-C
          |
          v
      EKS Ingress / AWS Load Balancer Controller
          |
          v
       Kubernetes Service
          |
     +----+----------------+
     |                     |
   Pod A                 Pod B
     |                     |
   Node A                Node B
   AZ-A                  AZ-B
     |                     |
     +---------+-----------+
               |
        Private VPC Network
               |
       +-------+--------+
       |                |
      S3              Database
   Gateway VPCE      RDS/Aurora

 EKS CONTROL PLANE (AWS MANAGED)
          |
    Kubernetes API Server
          |
    Scheduler / Controllers
          |
    Worker Nodes / Kubelets

 PRIVATE AWS SERVICE CONNECTIVITY
          |
 ECR API + ECR DKR + S3
 STS / EC2 / ELB / CloudWatch
          |
     VPC Endpoints
```

The diagram is conceptual. In the final implementation, the AWS Load Balancer Controller normally provisions and manages the ALB from Kubernetes Ingress resources. The ALB forwards requests to the configured targets, commonly pod IPs when using IP target mode.

The control plane is AWS-managed; worker nodes and application pods run in the customer's AWS account. EKS control-plane components are not ordinary pods running on your worker nodes.

### Recommended infrastructure

| Component | Design |
|---|---|
| VPC | Dedicated VPC with non-overlapping CIDR ranges |
| Availability Zones | Three AZs where supported |
| Public subnets | Internet-facing ALB and NAT gateways, if required |
| Private subnets | EKS worker nodes |
| Pod networking | Amazon VPC CNI |
| EKS | Managed control plane and managed node groups |
| Container registry | Private Amazon ECR |
| Ingress | AWS Load Balancer Controller and ALB |
| Application | Kubernetes Deployment and ClusterIP Service |
| Database | Private RDS/Aurora subnets |
| S3 connectivity | S3 gateway VPC endpoint |
| Image pull connectivity | ECR API, ECR DKR and S3 endpoints |
| Workload identity | EKS Pod Identity or IRSA |
| Scaling | HPA plus Cluster Autoscaler or Karpenter |
| Observability | CloudWatch, Prometheus/Grafana, logs and alerts |
| Secrets | AWS Secrets Manager with narrowly scoped IAM permissions |

Official reference: [Amazon EKS documentation](https://aws.amazon.com/documentation-overview/eks/)

---

## 4. Understand the EKS internals

### 4.1 Control plane versus data plane

**Control plane**

The control plane manages the desired state of the Kubernetes cluster.

Important components include:

- **kube-apiserver:** Receives Kubernetes API requests, authenticates and authorizes them, and coordinates persistence and admission.
- **etcd:** Stores Kubernetes cluster state. In EKS, AWS manages the control-plane datastore.
- **kube-scheduler:** Selects an appropriate node for an unscheduled pod.
- **kube-controller-manager:** Runs controllers that reconcile actual state with desired state.

EKS manages the control plane, including its availability and underlying infrastructure.

**Data plane**

The data plane runs application workloads.

Important components include:

- **Worker nodes:** EC2 instances or Fargate compute.
- **kubelet:** Ensures pods assigned to a node are running.
- **Container runtime:** Typically containerd on Linux EKS nodes.
- **Amazon VPC CNI:** Configures pod networking and allocates VPC IP addresses.
- **kube-proxy:** Implements Service networking rules on common EKS configurations; alternative data-plane implementations can replace it.
- **Pods:** Run the application's containers.

### Interview question: Is the EKS control plane inside my VPC?

The EKS control plane is AWS-managed and runs in an AWS-managed environment. AWS creates networking interfaces in the cluster VPC to support communication between the control plane and customer-managed nodes.

Your worker nodes run in your AWS account. They communicate with the Kubernetes API server through the configured cluster endpoint.

Do not say that the Kubernetes API server is simply another pod running on your worker node.

Reference: [Amazon EKS CreateCluster API](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html)

---

## 5. Request lifecycle: From deployment to running pod

This is one of the most important topics to explain confidently.

Suppose I deploy a new application version using:

```bash
kubectl apply -f deployment.yaml
```

### Step 1: The client sends a request

The `kubectl` client uses the cluster endpoint and credentials configured in its kubeconfig.

Authentication can involve AWS IAM authentication, and Kubernetes authorization determines whether the caller is permitted to perform the requested operation.

The request reaches the Kubernetes API server.

### Step 2: The API server processes the request

The API server performs authentication, authorization, admission processing, validation, and persistence as applicable.

If the Deployment is accepted, its desired state is persisted in the Kubernetes datastore.

At this point, the API request can succeed even though no application pod is running yet.

### Step 3: The Deployment controller creates a ReplicaSet

The Deployment controller observes the desired Deployment state.

It creates or updates a ReplicaSet to maintain the desired number of replicas.

For example:

```yaml
replicas: 3
```

means Kubernetes should maintain three desired pod replicas.

### Step 4: The ReplicaSet controller creates pods

The ReplicaSet controller creates Pod objects.

Initially, these pods generally do not have an assigned node.

The controllers reconcile the desired state asynchronously; they do not wait for all containers to start before returning the original API response.

### Step 5: The scheduler selects nodes

The scheduler watches for unscheduled pods and evaluates candidate nodes.

It considers:

- CPU and memory requests.
- Node readiness and available resources.
- Node selectors and required affinity.
- Taints and tolerations.
- Pod affinity and anti-affinity.
- Topology spread constraints.
- Persistent-volume constraints and other scheduling requirements.

The scheduler selects a suitable node and records the binding.

If no node is suitable, the pod remains Pending and its events help explain why.

### Step 6: The kubelet receives the assigned pod

The kubelet on the selected worker node observes the pod assignment through the Kubernetes API.

It works with the container runtime to ensure that the pod's sandbox and containers are created.

### Step 7: Networking is configured

The container runtime invokes the configured CNI integration as part of pod sandbox setup.

With the Amazon VPC CNI, the plugin allocates or assigns a VPC-routable IP address to the pod and configures the node's networking.

The exact IP allocation mechanism depends on CNI configuration, available ENI addresses, prefix delegation, and IP family.

### Step 8: The image is pulled

The kubelet and container runtime obtain the image from the specified registry.

For a private ECR image, the node needs the necessary registry authentication, IAM permissions, and network connectivity.

If the image is already present and its pull policy permits reuse, a fresh download may not be necessary.

### Step 9: The container starts

The runtime starts the container.

The kubelet evaluates startup, readiness, and liveness probes as configured.

A running container is not necessarily a Ready pod.

### Step 10: The application becomes eligible for traffic

When the readiness probe succeeds, the pod becomes eligible to receive Service traffic, subject to the other Service and traffic-routing rules.

EndpointSlice controllers maintain the endpoints associated with Services.

If the AWS Load Balancer Controller manages the ALB, it also reconciles the corresponding AWS target configuration and health-check state.

### Step 11: Users reach the application

The ALB forwards traffic to healthy targets. The Kubernetes Service provides internal service discovery and routing according to the chosen target architecture.

The application processes the HTTP request and may communicate with S3, RDS, or other services.

**Key interview point:** Deployment acceptance, pod scheduling, image pulling, container startup, readiness, and successful user traffic are separate stages. A failure at any stage can produce a different symptom.

---

## 6. ECR image pull: The complete low-level flow

Suppose the Deployment contains:

```yaml
image: 123456789012.dkr.ecr.ap-south-1.amazonaws.com/orders-api:v1.2.0
```

What happens internally?

### Image pull sequence

1. The scheduler assigns the pod to a worker node.
2. The kubelet requests the required pod sandbox and containers through the container runtime.
3. The runtime checks whether the required image can be used locally.
4. If the image must be downloaded, the node's image credential provider obtains ECR credentials using the applicable IAM identity.
5. The node contacts the ECR API and registry endpoints.
6. ECR authorizes the image-pull operations.
7. The image manifest and layer download information are obtained.
8. The image layers are downloaded from the backing S3 infrastructure.
9. The runtime unpacks the image and creates the container.
10. The application starts.

### Which IAM role is used?

For conventional EC2-backed EKS nodes, the node IAM role normally supplies the permissions required for private ECR image pulls.

Common required actions include:

```text
ecr:GetAuthorizationToken
ecr:BatchCheckLayerAvailability
ecr:BatchGetImage
ecr:GetDownloadUrlForLayer
```

`ecr:GetAuthorizationToken` generally requires `Resource: "*"`. Repository-specific permissions can be scoped to the appropriate repository where supported.

For Fargate, the pod execution role has a different purpose and supplies the permissions needed to pull images.

Advanced per-pod ECR pull authorization is also possible with supported Kubernetes and EKS configurations. Do not confuse that feature with ordinary runtime application identity.

### Important distinction: Image pull versus application access

| Activity | Typical identity |
|---|---|
| Pull private ECR image on EC2 node | Node IAM role in the conventional configuration |
| Pull image on Fargate | Fargate pod execution role |
| Application reads S3 at runtime | EKS Pod Identity or IRSA role |
| Application accesses Secrets Manager | Pod workload identity with scoped IAM permissions |
| Engineer deploys to Kubernetes | IAM authentication plus Kubernetes authorization |

A pod's application IAM role is not automatically the identity used by the kubelet to pull its image.

### ECR troubleshooting commands

```bash
kubectl describe pod <pod-name> -n <namespace>

kubectl get events -n <namespace> \
  --sort-by=.metadata.creationTimestamp

kubectl get nodes -o wide

kubectl describe node <node-name>
```

Look for:

```text
ErrImagePull
ImagePullBackOff
AccessDeniedException
no basic auth credentials
manifest unknown
i/o timeout
no such host
```

Possible causes:

- Incorrect repository, image tag, or account ID.
- Missing ECR IAM permissions.
- Cross-account repository policy not permitting the pull.
- Missing ECR API or registry network connectivity.
- Missing S3 layer-download connectivity.
- Incorrect DNS or security group configuration.
- Registry authentication or image architecture mismatch.

Reference: [Using Amazon ECR images with EKS](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_EKS.html)

---

## 7. VPC endpoints, endpoint policies, and private clusters

This is a high-value interview area because the term "endpoint" can refer to several different things.

### 7.1 Different endpoints in an EKS architecture

| Endpoint | Purpose |
|---|---|
| EKS Kubernetes API endpoint | Used by kubectl, kubelet and Kubernetes components to communicate with the cluster API |
| AWS EKS service API endpoint | Used for AWS management operations such as DescribeCluster or UpdateClusterConfig |
| ECR API interface endpoint | Provides private connectivity to ECR API operations |
| ECR DKR interface endpoint | Provides private connectivity to the ECR registry |
| S3 gateway endpoint | Allows private access to S3 through associated VPC route tables |
| STS interface endpoint | Supports private STS API access where needed |
| EC2 interface endpoint | Supports private EC2 API access where needed |
| ELB interface endpoint | Supports private AWS Elastic Load Balancing API calls |
| Kubernetes Service ClusterIP | Internal virtual IP for a Kubernetes Service |
| Application ALB DNS endpoint | Client-facing entry point to the application |

**Critical distinction:** The AWS EKS service interface endpoint does not replace the Kubernetes API server endpoint. They are different endpoints serving different APIs.

Reference: [Access Amazon EKS using AWS PrivateLink](https://docs.aws.amazon.com/eks/latest/userguide/vpc-interface-endpoints.html)

### 7.2 Which VPC endpoints are required?

For an EC2-backed private EKS cluster with no unrestricted internet access, consider the following.

| AWS service | Endpoint | Reason |
|---|---|---|
| ECR API | Interface | Authentication and registry-related API operations |
| ECR DKR | Interface | Image registry operations |
| S3 | Gateway | Downloading ECR image layers and accessing S3 |
| STS | Interface, when required | AWS STS API calls |
| EC2 | Interface | EC2 API calls from components that need them |
| EKS Auth | Interface, when required | EKS Pod Identity credential flow |
| CloudWatch Logs | Interface, when required | Private log delivery |
| Elastic Load Balancing | Interface, when required | Controller access to AWS load-balancing APIs |
| Systems Manager | Interface, when required | Private node management |
| EKS service API | Interface, when required | Private AWS EKS management API access |

This is a planning list, not a claim that every endpoint is mandatory for every cluster. The exact requirements depend on the node bootstrap method, controllers, add-ons, deployment tools, logging, and workload integrations.

Also account for DNS resolution, security group rules, endpoint security groups, route tables, and any required external dependencies.

Reference: [Deploy private EKS clusters with limited internet access](https://docs.aws.amazon.com/eks/latest/userguide/private-clusters.html)

### 7.3 Can an endpoint policy restrict access to a specific S3 bucket?

Yes.

An S3 gateway endpoint policy can restrict which S3 resources and actions are allowed through that endpoint.

For example, the policy can permit access only to a specific application bucket, assuming no other required traffic is blocked.

However, there is an important complication with ECR.

**ECR stores image layers in AWS-managed S3 buckets.** When a node pulls a private ECR image, it needs access to the S3 bucket used for the ECR image layers.

Therefore, if the S3 endpoint policy permits only your application's bucket and omits the ECR layer bucket, ECR image pulls can fail.

The S3 gateway endpoint policy must account for the relevant regional ECR layer bucket, commonly represented as:

```text
arn:aws:s3:::prod-<region>-starport-layer-bucket/*
```

Use the exact regional resource from AWS documentation when implementing the policy.

### 7.4 Does an endpoint policy replace IAM?

No.

Think of authorization as a set of independent checks:

- IAM identity policy: What may this identity do?
- VPC endpoint policy: What may pass through this endpoint?
- ECR repository policy: Which principals may access this repository?
- S3 bucket policy: Which principals may access this bucket?
- Security groups and NACLs: Can the network connection pass?
- Kubernetes RBAC: What may this Kubernetes identity do in the cluster?

A successful request needs the required network path and authorization through all applicable controls.

An endpoint policy does not grant permissions that the identity otherwise lacks. It also does not replace the service's resource policy or identity policy.

Reference: [ECR VPC endpoints and endpoint policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html)

---

## 8. EKS Kubernetes API access and authorization

### 8.1 What is the EKS cluster endpoint?

The Kubernetes API server endpoint is the URL used to access the cluster's Kubernetes API.

You can inspect it using:

```bash
aws eks describe-cluster \
  --name my-cluster \
  --region ap-south-1 \
  --query cluster.endpoint \
  --output text
```

Configure access for an engineer's workstation:

```bash
aws eks update-kubeconfig \
  --name my-cluster \
  --region ap-south-1
```

The AWS CLI configures kubeconfig; it does not automatically grant the caller Kubernetes permissions.

### 8.2 Public versus private endpoint access

A production cluster can enable private access and disable public access to its Kubernetes API endpoint.

For a private-only endpoint, administrative access must originate from the cluster VPC or an appropriately connected network, such as corporate connectivity through VPN or Direct Connect.

A common design is:

```text
Engineer workstation
        |
Corporate VPN / Direct Connect
        |
Private VPC routing
        |
Private Kubernetes API endpoint
        |
EKS control plane
```

Public endpoint access can instead be restricted to approved source CIDRs where appropriate.

### 8.3 Authentication versus authorization

Authentication answers: **Who are you?**

Authorization answers: **What are you allowed to do?**

For example:

- AWS IAM authenticates an authorized identity.
- EKS access entries and access policies can associate identities with cluster access.
- Kubernetes RBAC controls permissions on Kubernetes resources.
- A Kubernetes ServiceAccount represents a workload identity within Kubernetes.

A user who can call AWS `eks:DescribeCluster` does not automatically have permission to create Deployments.

Likewise, access to the Kubernetes API does not automatically grant permission to delete AWS resources.

### 8.4 Kubernetes API troubleshooting

```bash
kubectl cluster-info

kubectl get nodes

kubectl auth can-i create deployments \
  --namespace production

kubectl auth can-i get secrets \
  --namespace production
```

Investigate:

- Incorrect AWS identity.
- Missing EKS access entry or authorization mapping.
- Missing Kubernetes RBAC binding.
- Incorrect kubeconfig context.
- Network access to the API endpoint.
- DNS resolution and certificate validation.
- Private endpoint routing or cluster security group rules.

Reference: [Configure EKS cluster API endpoint access](https://docs.aws.amazon.com/eks/latest/userguide/config-cluster-endpoint.html)

---

## 9. Kubernetes scheduling: How a pod finds a node

Suppose a Deployment requires three replicas.

```yaml
spec:
  replicas: 3
```

Kubernetes creates three desired pod replicas. The scheduler decides where they can run.

### 9.1 Scheduling inputs

The scheduler evaluates:

- CPU and memory requests.
- Node capacity and allocated resources.
- Node selectors and affinity.
- Taints and tolerations.
- Pod affinity and anti-affinity.
- Topology spread constraints.
- Persistent-volume topology.
- Other scheduling policies.

### 9.2 Requests versus limits

Example:

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "1000m"
    memory: "512Mi"
```

- **Requests** are used for scheduling and resource accounting.
- **Limits** constrain resource consumption.
- A container exceeding its memory limit can be terminated with an OOM-related failure.
- CPU limits can throttle a container.

A node may have free physical memory but still be unsuitable if its allocatable CPU or memory cannot satisfy the pod's requests.

### 9.3 Spread replicas across Availability Zones

Example:

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: orders-api
```

This helps distribute matching pods across zones, subject to the available nodes, labels, and other scheduling constraints.

It does not create additional worker nodes or guarantee placement if the required topology cannot be satisfied.

### 9.4 Node affinity versus taints and tolerations

- **Node affinity** expresses where a pod should or must run.
- **Taints** repel pods from nodes unless the pods tolerate those taints.
- **Tolerations** allow a pod to be considered for a tainted node; they do not force placement there.

### 9.5 What happens if there is insufficient capacity?

If no node can satisfy the pod's requirements, the pod remains Pending.

Possible responses:

1. Inspect pod events and scheduling constraints.
2. Check node allocatable resources.
3. Verify subnet and pod-IP capacity separately.
4. Add node capacity or adjust the workload's resource requests if justified.
5. Check whether autoscaling can provision a suitable node.
6. Review affinity, taints, topology spread, and storage constraints.

**Important:** A scheduler does not normally provision an EC2 instance by itself. A node autoscaler, managed node group scaling process, or Karpenter may provide additional capacity.

Reference: [Kubernetes scheduling and eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/)

---

## 10. Amazon VPC CNI: Pod IPs, ENIs, and routing

The Amazon VPC CNI plugin allows pods to receive IP addresses from the VPC's address space in the common IPv4 configuration.

### 10.1 How it works

At a high level:

1. Worker nodes have primary network interfaces and IP addresses.
2. The CNI manages additional networking capacity using ENIs and available IP addresses or delegated prefixes, depending on configuration.
3. When a pod is created, the CNI allocates networking and configures the pod sandbox.
4. The pod receives an IP address.
5. Traffic is routed according to the VPC, node, pod networking, and security configuration.

The exact allocation behavior varies with CNI version, prefix delegation, custom networking, and IPv4 or IPv6 mode.

### 10.2 Why do pods run out of IP addresses?

Possible causes:

- The subnet has insufficient free IP addresses.
- The node has reached its networking capacity.
- ENI or prefix allocation is constrained.
- Pod density exceeds the configured limits.
- Custom networking uses an exhausted subnet.
- A CNI permission or networking failure prevents allocation.

### 10.3 Troubleshooting CNI

```bash
kubectl get pods -n kube-system -o wide

kubectl logs -n kube-system \
  -l k8s-app=aws-node \
  --all-containers=true \
  --tail=100

kubectl describe node <node-name>

kubectl get events -A \
  --sort-by=.metadata.creationTimestamp
```

Also inspect:

- Available subnet IP addresses.
- EC2 ENI attachment and address capacity.
- CNI logs and add-on version.
- Node IAM permissions for CNI operations.
- Pod IP assignment failures.
- Security groups, NACLs, and VPC routes.

A pod that cannot obtain networking may fail before the application container starts.

### 10.4 Can a pod connect directly to S3?

Yes, assuming DNS, routing, security, and authorization are configured correctly.

For example:

```text
Pod
 |
Pod IP / Node networking
 |
VPC route table
 |
S3 gateway endpoint
 |
Amazon S3
```

The pod still requires an appropriate AWS identity and S3 permissions. A gateway endpoint provides connectivity, not automatic access to every bucket.

Reference: [Amazon VPC CNI for EKS](https://docs.aws.amazon.com/eks/latest/userguide/cni-iam-role.html)

---

## 11. Kubernetes Service, Ingress, ALB, and application APIs

These components solve different problems.

### Kubernetes Service

A Service provides a stable network abstraction for a set of matching pods.

Example:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders-api
spec:
  type: ClusterIP
  selector:
    app: orders-api
  ports:
    - port: 80
      targetPort: 8080
```

This Service forwards traffic to matching pod endpoints.

### Ingress

Ingress describes HTTP/HTTPS routing rules.

It requires an ingress controller to implement those rules. In AWS, the AWS Load Balancer Controller can provision an ALB from an Ingress resource.

### ALB

An Application Load Balancer operates at Layer 7 and supports HTTP/HTTPS routing, host-based routing, and path-based routing.

### Global traffic

A regional ALB does not become a globally distributed load balancer just because it has a public DNS name.

For global traffic, you can use:

- Route 53 routing policies for DNS-based traffic distribution.
- AWS Global Accelerator for static anycast IP addresses and routing to supported regional endpoints.
- Multiple regional application stacks for regional resilience and disaster recovery.

For cross-region active-active or active-passive designs, also address database consistency, replication lag, failover automation, session handling, and DNS or accelerator health checks.

### Request path

```text
User
 |
DNS / Global routing
 |
Regional ALB
 |
Target group
 |
Pod IP or node target
 |
Application container
 |
Database / S3 / downstream API
```

With ALB IP target mode, the ALB can route directly to pod IPs. With instance target mode, the traffic goes to worker-node targets and a NodePort path is used.

### Readiness matters

A healthy container is not necessarily ready for production traffic.

Use:

- Startup probes for slow-starting applications.
- Readiness probes to control traffic eligibility.
- Liveness probes to detect cases where restarting the container is appropriate.

Do not use an aggressive liveness probe that restarts a healthy application merely because a temporary downstream dependency is unavailable.

---

## 12. IAM for EKS workloads

There are separate identities for the cluster, nodes, Kubernetes users, and applications.

### Cluster IAM role

Used by the EKS control plane to perform required AWS operations.

### Node IAM role

Used by worker nodes for required AWS operations, including node-related permissions and conventional ECR image pulling.

### Kubernetes ServiceAccount

Identifies a workload inside Kubernetes.

### EKS Pod Identity

Provides an AWS IAM role to a Kubernetes workload using an EKS Pod Identity association and the Pod Identity Agent.

### IRSA

IAM Roles for Service Accounts uses a cluster's OIDC identity provider and AWS STS to provide temporary AWS credentials to a Kubernetes ServiceAccount.

Both EKS Pod Identity and IRSA support workload-specific AWS permissions.

### Example: Application reads one S3 bucket

The desired access pattern is:

```text
orders-api pod
      |
Kubernetes ServiceAccount
      |
EKS Pod Identity / IRSA
      |
Scoped IAM role
      |
S3 permissions for the required bucket
```

Do not give the application broad S3 access through the node role when workload-specific identity is appropriate.

Also avoid giving the CNI and unrelated workloads unnecessary privileges through a shared node role.

Reference: [Grant AWS permissions to EKS workloads](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html)

---

## 13. Autoscaling and high availability

### Horizontal Pod Autoscaler (HPA)

HPA changes the desired number of application replicas based on configured metrics.

Example:

```text
CPU utilization increases
        |
HPA evaluates metrics
        |
Replica count increases
        |
Scheduler places new pods
```

HPA does not create EC2 instances.

### Cluster Autoscaler or Karpenter

These mechanisms help provision additional worker capacity when pods cannot be scheduled or when scaling policies require more nodes.

```text
HPA increases replicas
        |
New pods cannot fit
        |
Node autoscaler provisions capacity
        |
New EC2 nodes join EKS
        |
Scheduler places pods
```

The exact timing depends on provisioning, node bootstrap, networking, and image startup.

### PodDisruptionBudget

A PodDisruptionBudget helps control voluntary disruptions such as certain node maintenance and drain operations. It does not guarantee protection from every involuntary failure, and it does not create capacity.

### Production resilience checklist

- Multiple replicas.
- Multiple Availability Zones.
- Topology spread constraints.
- Suitable pod resource requests.
- HPA and node autoscaling.
- Readiness probes.
- PodDisruptionBudget.
- Graceful termination.
- Load balancer health checks.
- Application and database recovery procedures.
- Tested rollback and disaster recovery plans.

---

## 14. Hands-on lab: Deploy a complete sample application

The following lab assumes you already have an EKS cluster, a reachable private ECR repository, and the necessary IAM and network configuration.

Replace all placeholders with your actual values.

### Step 1: Inspect the cluster

```bash
aws sts get-caller-identity

aws eks describe-cluster \
  --name my-cluster \
  --region ap-south-1

kubectl config current-context

kubectl get nodes -o wide

kubectl get pods -A
```

Explain what each command checks and which API or identity is involved.

### Step 2: Authenticate Docker to ECR

```bash
aws ecr get-login-password \
  --region ap-south-1 \
  | docker login \
      --username AWS \
      --password-stdin \
      123456789012.dkr.ecr.ap-south-1.amazonaws.com
```

This command authenticates the Docker client used to push the image. It does not configure worker-node image-pull permissions.

### Step 3: Build and push an image

```bash
docker build -t orders-api:v1.0.0 .

docker tag orders-api:v1.0.0 \
  123456789012.dkr.ecr.ap-south-1.amazonaws.com/orders-api:v1.0.0

docker push \
  123456789012.dkr.ecr.ap-south-1.amazonaws.com/orders-api:v1.0.0
```

In production, use an automated CI/CD pipeline, scan images, and prefer immutable digests for deployment traceability.

### Step 4: Create a namespace

```bash
kubectl create namespace production
```

### Step 5: Create a Deployment

Save the following as `deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orders-api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: orders-api
    spec:
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: orders-api
          image: 123456789012.dkr.ecr.ap-south-1.amazonaws.com/orders-api:v1.0.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          startupProbe:
            httpGet:
              path: /health
              port: 8080
            periodSeconds: 5
            failureThreshold: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
```

**Important:** This manifest assumes the application supports `/health`, listens on port 8080, and runs correctly as UID 10001 with a read-only root filesystem. Modify it to suit your image. The container may need writable temporary volumes.

The `automountServiceAccountToken: false` setting is appropriate for this sample if the application does not need to call the Kubernetes API. AWS workload identity can still be configured separately when required.

Apply it:

```bash
kubectl apply -f deployment.yaml

kubectl rollout status deployment/orders-api \
  -n production

kubectl get pods -n production -o wide
```

### Step 6: Create a Service

Save as `service.yaml`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders-api
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: orders-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

Apply it:

```bash
kubectl apply -f service.yaml

kubectl get service -n production

kubectl get endpointslices -n production
```

### Step 7: Test internal access

```bash
kubectl port-forward \
  -n production \
  service/orders-api 8080:80
```

In another terminal:

```bash
curl http://127.0.0.1:8080/health
```

This tests application access through the Kubernetes Service using port forwarding. It does not prove that the public ALB, external DNS, or all production network paths are working.

### Step 8: Test scaling

```bash
kubectl scale deployment/orders-api \
  -n production \
  --replicas=5

kubectl get pods -n production -o wide

kubectl describe deployment/orders-api \
  -n production
```

Observe how the scheduler assigns new pods and whether the existing nodes have sufficient resources.

### Step 9: Test rollout and rollback

```bash
kubectl set image deployment/orders-api \
  -n production \
  orders-api=123456789012.dkr.ecr.ap-south-1.amazonaws.com/orders-api:v1.1.0

kubectl rollout status deployment/orders-api \
  -n production

kubectl rollout history deployment/orders-api \
  -n production

kubectl rollout undo deployment/orders-api \
  -n production
```

The previous ReplicaSet must still be available, and its image must remain retrievable. Rolling back the Deployment does not reverse database schema changes or other external side effects.

---

## 15. Hands-on troubleshooting scenarios

For each scenario, explain the likely cause, the evidence you would collect, the fix, and how you would prevent recurrence.

### Scenario A: Pod remains Pending

Start with:

```bash
kubectl describe pod <pod-name> -n production

kubectl get events -n production \
  --sort-by=.metadata.creationTimestamp

kubectl describe nodes
```

Investigate:

- Insufficient CPU or memory.
- Untolerated taints.
- Node selector or affinity mismatch.
- Topology constraints.
- Unbound PVCs.
- IP capacity if networking setup is implicated.
- Autoscaler failures.

Do not immediately increase the node count without understanding the scheduling event.

### Scenario B: ImagePullBackOff

Start with:

```bash
kubectl describe pod <pod-name> -n production
```

Check the image URI, tag or digest, node IAM role, ECR repository permissions, ECR endpoints, S3 layer connectivity, DNS, and security groups.

### Scenario C: Pod is Running but Not Ready

```bash
kubectl describe pod <pod-name> -n production

kubectl logs <pod-name> -n production

kubectl logs <pod-name> -n production --previous
```

Check application startup, health-check paths, container port, dependencies, timeouts, and readiness probe configuration.

### Scenario D: Pod cannot access S3

Investigate:

1. Does DNS resolve?
2. Is the S3 gateway endpoint associated with the relevant route table?
3. Does the endpoint policy permit the request?
4. Does the workload IAM role allow the required S3 actions?
5. Does the bucket policy permit access?
6. Is the request using the expected role?
7. Are there explicit denies in applicable policies?
8. Is the application using the correct bucket and Region?

Network reachability and IAM authorization are different problems.

### Scenario E: ALB returns 503

Check:

```bash
kubectl get ingress -A

kubectl get service -n production

kubectl get endpointslices -n production

kubectl get pods -n production -o wide

kubectl describe ingress <ingress-name> -n production
```

Investigate:

- No healthy targets.
- Pods failing readiness.
- Incorrect target port.
- Incorrect Service selector.
- ALB target registration failures.
- Security group connectivity.
- Application health-check mismatch.

### Scenario F: Node cannot join the cluster

Check:

- Node IAM role and required permissions.
- Cluster API endpoint reachability.
- DNS resolution.
- Private endpoint configuration.
- Security group rules.
- Subnet routes.
- Node bootstrap and kubelet logs.
- Required endpoints for a private cluster.

### Scenario G: New pods cannot get IP addresses

Check VPC CNI logs, available subnet addresses, ENI capacity, prefix delegation configuration, custom networking, and node-level IP limits.

### Scenario H: Deployment is accepted but the application never starts

Explain the difference between API acceptance, ReplicaSet creation, scheduling, sandbox setup, image pulling, container startup, readiness, and external load-balancer health.

This question tests whether you understand the lifecycle rather than just memorizing Kubernetes commands.

---

## 16. Production security and governance

A production EKS architecture should include:

- Private worker nodes.
- Restricted Kubernetes API endpoint access.
- Least-privilege cluster, node, and workload IAM roles.
- Kubernetes RBAC and controlled EKS access entries.
- Restricted ECR repositories and image scanning.
- Approved image registries and immutable image digests.
- Secrets Manager or another approved secret-management mechanism.
- Pod security controls and non-root containers.
- Kubernetes NetworkPolicy where supported and configured.
- Security groups, VPC routing controls, and endpoint policies.
- Encryption in transit and at rest.
- Control-plane audit logging and workload observability.
- Terraform or another controlled infrastructure-as-code workflow.
- Version upgrade and add-on compatibility plans.
- Tested backups and disaster recovery procedures.

### NetworkPolicy versus security groups

Kubernetes NetworkPolicy controls pod traffic when an enforcing network policy implementation is installed and configured.

Security groups control traffic at the AWS network interface level.

They are complementary controls, not interchangeable ones.

### Endpoint policy versus security group

A VPC endpoint security group controls network connectivity to an interface endpoint.

The endpoint policy controls which service actions and resources are permitted through that endpoint.

Both may be required, along with IAM authorization.

---

## 17. Interview evaluation scorecard

Use this checklist to evaluate practical readiness.

| Topic | Points |
|---|---:|
| High-level architecture and AZ resilience | 10 |
| EKS control plane and Kubernetes APIs | 10 |
| Deployment request lifecycle | 10 |
| ECR image-pull flow and IAM | 10 |
| CNI, ENIs, pod IPs, and routing | 10 |
| Scheduler and resource management | 10 |
| VPC endpoints and endpoint policies | 10 |
| Services, Ingress, ALB, and request routing | 10 |
| IAM, RBAC, and workload identity | 5 |
| Autoscaling and high availability | 5 |
| Hands-on troubleshooting | 10 |
| **Total** | **100** |

Suggested interpretation:

- **85–100:** Strong architecture and troubleshooting readiness, assuming you can explain the design and demonstrate the commands.
- **70–84:** Good foundation; strengthen implementation details and failure diagnosis.
- **50–69:** Review the request lifecycle, networking, and IAM before attempting advanced design interviews.
- **Below 50:** Build and troubleshoot a working EKS lab before focusing on complex architectures.

This score is a preparation aid, not an industry certification or an objective measure of interview success.

---

## 18. Official documentation for revision

1. [Amazon EKS documentation](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
2. [EKS cluster API endpoint access](https://docs.aws.amazon.com/eks/latest/userguide/config-cluster-endpoint.html)
3. [Private EKS clusters](https://docs.aws.amazon.com/eks/latest/userguide/private-clusters.html)
4. [Amazon ECR image pulls from EKS](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_EKS.html)
5. [ECR VPC endpoints and policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html)
6. [Amazon VPC CNI](https://docs.aws.amazon.com/eks/latest/userguide/cni-iam-role.html)
7. [EKS workload identity](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html)
8. [Kubernetes scheduling](https://kubernetes.io/docs/concepts/scheduling-eviction/)
9. [Kubernetes cluster architecture](https://kubernetes.io/docs/concepts/architecture/)
10. [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
11. [EKS cluster creation API](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html)

---

## 19. How to prepare for the actual interview

Study these in order:

1. **Request lifecycle:** `kubectl apply` through API server, controllers, scheduler, kubelet, runtime, and readiness.
2. **ECR image pulls:** IAM identity, ECR API, registry endpoint, S3 image layers, and private networking.
3. **CNI networking:** Pod IP allocation, ENIs, subnet exhaustion, security groups, and routes.
4. **Scheduling:** Requests versus limits, affinity, taints, topology spread, and autoscaling.
5. **APIs and endpoint policies:** Kubernetes API versus AWS EKS API, S3 gateway endpoint, ECR interface endpoints, and authorization layers.
6. **Application traffic:** ALB, Ingress, Service, EndpointSlices, pod health, and response routing.
7. **Troubleshooting:** Practice identifying the cause from pod events, logs, node status, AWS IAM policies, and network configuration.

**Final test:** You should be able to draw the architecture from memory, trace one deployment and one user request hop by hop, and troubleshoot an intentionally broken deployment in a real EKS lab. That is a much stronger demonstration of EKS architecture capability than reciting Kubernetes definitions.

