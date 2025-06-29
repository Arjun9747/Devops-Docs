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

