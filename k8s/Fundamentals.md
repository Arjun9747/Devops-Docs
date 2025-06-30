**Containers**
1. Smallest Abstraction layer
2. Encapsulates its application and its dependancies
3. For eg: Docker containers, ContainerD, CRI-O

**Pod**
1. Smallest deployable unit.
2. Pod can encapsulates one more containers which share same
   * Network namespace (ip addr)
   * Storage Volumes
   * Process Namespace
3. Containers in the same namespace can communicate over local hosts
4. For eg: Pod

**Node**
1. Physical or VM in a cluster

**Application**
1.Deployment for Scalability
2.Statefulset for stateful apps
3. Ingress for external access 

Application
  └── Deployment / StatefulSet
      └── Pod
          └── Container(s)
              └── Application Code
  └── Service
  └── Ingress


  **************************************
  ```markdown
1. What CNI Really Does (and When It Fails)

The Container Network Interface is the first to act when a Pod is born. 
As soon as the kubelet spins up a Pod, the CNI plugin assigns an IP address 
to it and wires up its network namespace. In most setups—whether Calico, 
Weave, or AWS VPC CNI—this involves creating a veth pair, connecting it to a bridge, and ensuring routing is set.

If this wiring fails, the Pod may start, but it will be network-isolated. No inbound or outbound traffic. 
Worse, it might only partially fail, where DNS works but inter-Pod connectivity doesn’t.

And this plugin also implements NetworkPolicies—the Kubernetes-native firewall rules. 
If traffic seems blocked without reason, chances are your CNI is denying it.

2. CoreDNS: The Cluster's Oracle
Now, let’s say Pod A wants to call payments.default.svc.cluster.local. CoreDNS is the one who translates this to the Service’s ClusterIP.
 It runs as a Deployment in the kube-system namespace and usually exposes port 53.

If CoreDNS is misconfigured or overwhelmed, DNS queries time out. If your resolv.conf points to a wrong IP, even curl won’t help.

3. KubeProxy: The Silent Traffic Controller
Once DNS resolves the name to a ClusterIP, KubeProxy kicks in. It’s responsible for maintaining the routing rules (via iptables or IPVS)
 that direct traffic from Services to the right Pod IPs.

KubeProxy uses the Endpoints object, updated by the kube-controller-manager, to track which Pods are healthy (based on readiness probes). 
It then routes traffic accordingly.

If kube-proxy is misbehaving—or if the node is under network pressure—traffic can vanish silently, leading you down a rabbit hole.

The Balancing Act: A Full Lifecycle
Let’s map the lifecycle of a single network call within Kubernetes, putting each component into perspective:

Pod is created — The CNI plugin allocates a unique IP to the Pod and sets up its virtual network stack, wiring it into the node’s network.

Readiness probe passes — Once the Pod’s readiness probe succeeds, it is registered in the corresponding Endpoints object,
 signaling it's ready to serve traffic.

Service is created — The Kubernetes API server assigns a stable ClusterIP to the Service, abstracting the backend Pods behind it.

Another Pod calls the Service — The calling Pod performs a DNS lookup; CoreDNS resolves the fully qualified domain name (FQDN) to the ClusterIP.

CNI enforces ingress network policies — If any NetworkPolicy exists for the destination Pod, the CNI checks whether ingress from the calling Pod is
 allowed.

KubeProxy handles routing — Based on its iptables/ipvs rules and the Endpoints list, it forwards the traffic from the ClusterIP to one of
 the healthy Pod IPs.
 
 CNI enforces egress network policies — If the destination Pod tries to make an outbound call, the CNI again checks if egress is permitted by network policies.

External call resolution — When the Pod calls an external domain (like aws.amazon.com),
 CoreDNS identifies it's non-cluster and forwards the query to an external DNS resolver (e.g., 8.8.8.8).
 The response is used to establish an outbound connection.
 
 CNI brings Pods to life on the network.

CoreDNS is your in-cluster name oracle.

KubeProxy decides who gets the traffic.

***************************************************************************

kubectl operations

Step 1: Authentication — Who Are You?

Once the request is formed, it’s sent to the Kubernetes API Server (kube-apiserver). The first thing it asks is: Who is this?

Kubernetes supports several authentication methods, including:

Certificates: If using client certificates, kube-apiserver checks the validity of the certificate (client.crt) using its trusted CA.

Bearer Tokens: Often used by service accounts.

OIDC: If you’re using cloud-managed clusters, external identity providers like AWS Cognito or Azure AD authenticate you.

Step 2: Authorization — Can You Do This?
Next comes authorization. Kubernetes uses Role-Based Access Control (RBAC) to decide whether you have permission to perform the requested action.

A Role defines a set of permissions (e.g., read, write, delete) for specific Kubernetes resources within a namespace while a
 RoleBinding grants a user, group, or service account the permissions defined in a Role.
 
 
Even if authorization is granted, there’s one more checkpoint. Admission controllers enforce policies to ensure the request complies with organizational rules.

For example:

Pod Security Policies (PSP) ensure containers run with appropriate permissions.

ResourceQuotas prevent exceeding resource limits.

Mutating Webhooks may inject necessary sidecars or add environment variables.

Say, you add an annotation to a pod for monitoring (monitoring=true), an admission controller could automatically
 inject a sidecar container for metrics collection
 
 Once all checks pass, kube-apiserver forwards the request to the etcd for reading or writing data. In this case, it fetches the list of nodes from etcd.

The API server then generates a JSON response and sends it back to kubectl.

From a simple kubectl get nodes, Kubernetes has gone through multiple phases: authentication, authorization, admission control, data retrieval, and response. It’s a sophisticated dance that
 ensures security, compliance, and reliability.
 
 ************************************************************************
 
 Schedular 
 
 Imagine a Kubernetes cluster deployed in AWS, spanning three Availability Zones, with 500+ nodes. Now a Deployment kicks off 100 pods. These pods come with a set of non-negotiable constraints:

Pods must be distributed across different Availability Zones.

No two pods of the same deployment should land on the same worker node.

Each pod declares CPU, memory, and ephemeral storage requests.

Some pods tolerate specific node taints (think GPU nodes or spot instances).

A few pods can only run on a special pool of nodes reserved for system workloads—those nodes must remain untouched except for DaemonSets.


Filtering Phase: The scheduler evaluates all 500 nodes, but not entirely.

Kubernetes uses an intelligent mechanism controlled by percentageOfNodesToScore. For large clusters (say, 5000 nodes), it doesn’t score all of them. By default, it applies a linear formula that ensures it always scores at least 5% of the cluster (and up to 50% depending on cluster size).

So in our 500-node case, Kubernetes will attempt to filter most of them, but scoring might happen on a subset.


Scoring Phase: For each node that passed the filters, scoring plugins kick in. These plugins evaluate pods against nodes based on criteria like topology spread, taints/tolerations, resource availability, affinity/anti-affinity, and more.


Selection: Once scored, the node with the highest score is picked. If there's a tie, Kubernetes picks randomly among top-scored nodes.


**full Life Cycle**

A user or controller (like a Deployment) creates a pod.

That pod lands in the API server with no nodeName. It's in the Pending phase.

The scheduler watches the API server and picks this pod from its internal queue.

After filtering and scoring, it writes back the selected nodeName to the pod object in the API server.

The kubelet on that node watches for new pods assigned to it.

It picks up the pod, prepares the runtime, pulls images, sets up networking/storage, and finally spins up the containers.

The pod transitions to Running.
```





