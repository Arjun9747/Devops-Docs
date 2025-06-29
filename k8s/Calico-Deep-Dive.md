```markdown
🔹 1. Network Connectivity
Creates Pod-to-Pod networking across nodes using standard routing (no overlay by default).
Assigns IP addresses to pods and sets up routes.

 2. Network Policy Enforcement
Implements Kubernetes NetworkPolicy and extends it with its own Calico-specific policies.
Controls which pods/services can communicate, enforcing zero trust networking.

🔹 3. Network Security & Observability
Supports host endpoints, global policies, DNS policies, etc.
Offers logging and flow monitoring.

| Calico | CNI + Network Policy engine | Layer 3/4 | Routing, policy enforcement, IPAM |
| kube-proxy | Kubernetes Service routing | Layer 4 | Service-to-pod traffic via NAT rules |

🔸 Calico
Uses Linux routing tables / BGP (no overlays by default)
Simple, performant, and cloud-native
NetworkPolicy support via iptables or eBPF
Extends beyond Kubernetes (can be used in VMs)

🔸 kube-proxy
Handles Service abstraction (ClusterIP, NodePort, LoadBalancer)
Implements DNAT rules so traffic to a Service gets routed to the correct pod
Does not control pod-to-pod access or security
```

Calico Dataplanes 
```markdown
✅ 1. Linux iptables (default, most widely used)
Use when:
You want maximum compatibility (legacy systems, Windows nodes)
You prefer mature, well-documented stack
Your team is familiar with Linux networking
Pros: Stable, easy to debug, widely adopted

Cons: iptables scales poorly with many rules, performance degrades under load

✅ 2. eBPF
Use when:
You want higher performance and lower latency
You’re running Kubernetes on modern Linux (kernel ≥ 5.3)
You want to avoid iptables bottlenecks (e.g., in large clusters)
Pros: Fast connection tracking, inline NAT, reduced syscall overhead

Cons:
Not supported on Windows
Some advanced Calico features (like host endpoints) not fully available

✅ 3. VPP
Use when:

You need very high throughput (e.g., for NFV, telco-grade performance)
You run large-scale edge/cloud workloads
You’re OK with customization and tuning

Pros: Fastest dataplane, supports SR-IOV, hardware acceleration

Cons:
High complexity
Less community adoption
Requires dedicated, tuned NICs for DPDK
No Windows support
```

**Felix**

```markdown
Felix is the primary Calico agent that runs on every node in a Kubernetes cluster. It is responsible for programming the data plane — setting up routes, firewall rules, and policies based on the desired network state.

| Function                             | Description                                                                                                                          |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Policy Enforcement**               | Applies Kubernetes `NetworkPolicy` and Calico-specific policies by programming iptables rules or eBPF maps.                          |
| **Routing Setup**                    | Adds routes for pod-to-pod and pod-to-external communication, often by programming kernel routing tables (or BPF maps in eBPF mode). |
| **Interface Management**             | Monitors and programs veth pairs or other interfaces created for pods.                                                               |
| **Connection to Datastore**          | Watches Kubernetes API (or etcd in standalone mode) to stay updated on endpoints, policies, and configuration.                       |
| **Workload Endpoint Sync**           | Tracks which pods are on the node, and programs rules accordingly.                                                                   |
| **Sync with BGP Agent (e.g., BIRD)** | Works with BGP daemons to advertise routes for the pods on its node.                                                                 |
📉 How Do You Know Felix is Unhealthy?
✅ Health Checks:
Liveness & readiness probes (K8s-native)

kubectl get pods -n calico-system -l k8s-app=calico-node
kubectl describe pod <calico-node-pod>

Calico's node status
calicoctl node status

Look for:
State: up for Felix
Errors in BGP or Felix sections
```

**Pod to Pod Networking**

```markdown
🔹 No Overlay = Native Routing
Calico uses Layer 3 (L3) routing instead of overlays like VXLAN or IPIP. In pure L3 mode:

Each pod is assigned a real routable IP address (no NAT).

Calico programs static routes or uses BGP (Border Gateway Protocol) to share routes between nodes.

Traffic flows directly between nodes — pod-to-pod — using native IP routing, no encapsulation.

🔧 What Enables It?
Calico's BGP agent (calico/node) runs on each node.
It announces pod CIDRs for each node to the rest of the cluster.
These are installed as host routes in the kernel routing table.

🧠 Result:
No encapsulation → lower latency, better throughput, easier to debug
True end-to-end IP visibility

When Calico doesn't use an overlay, it avoids tunneling overhead, so you get the full MTU (Maximum Transmission Unit) of the network.

But…

⚠️ You must ensure:
Your pod-to-pod traffic stays within the underlying VPC MTU
Cloud VPC MTUs are often 1460–1500 bytes
AWS: 1500 (but jumbo frames not always supported)

When a Kubernetes cluster spans multiple Layer 2 (L2) domains (i.e., nodes aren't all in the same subnet or broadcast domain), Calico can still handle pod-to-pod communication by leveraging BGP (Border Gateway Protocol).

Kubernetes NetworkPolicy: Namespaced, additive, limited.

Calico GlobalNetworkPolicy: Cluster-wide, layered, prioritized, more expressive.

```
```markdown
🔍 What is a Service Account Selector in Calico?
A serviceAccountSelector is a field in Calico (NetworkPolicy or GlobalNetworkPolicy) that lets you match traffic based on the Kubernetes ServiceAccount attached to a pod, instead of or in addition to using podSelector or namespaceSelector.
```
```bash
spec:
  ingress:
  - action: Allow
    source:
      serviceAccounts:
        selector: name == 'frontend-sa'
```
```

```markdown
Typha is a horizontal scalability component in Calico, designed to reduce the load on the Kubernetes API server and the Calico felix agents on each node—especially in large-scale clusters.

```bash
calicoctl node status

Calico process is running.

IPv4 BGP status
+----------------+-------------------+-------+----------+-------------+
|  Peer address  |     Peer type     | State |  Since   |     Info    |
+----------------+-------------------+-------+----------+-------------+
| 192.168.1.1    | node-to-node mesh | up    | 00:10:12 | Established |
| 192.168.1.2    | node-to-node mesh | up    | 00:10:14 | Established |
+----------------+-------------------+-------+----------+-------------+

```

