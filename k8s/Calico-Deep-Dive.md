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



