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
