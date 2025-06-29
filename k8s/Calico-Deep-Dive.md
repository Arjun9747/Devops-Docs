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

| Feature / Aspect         | **Linux (iptables)**                   | **eBPF**                                   | **VPP (Vector Packet Processing)**             |
| ------------------------ | -------------------------------------- | ------------------------------------------ | ---------------------------------------------- |
| **Technology**           | Traditional Linux kernel with iptables | Kernel-bypass using extended BPF           | Userspace, DPDK-based fast packet processing   |
| **Performance**          | Moderate (iptables can scale poorly)   | High (lower latency, faster conn tracking) | Very high (optimized for throughput & latency) |
| **Complexity**           | Lowest (well-known tools, widespread)  | Moderate (requires kernel support)         | High (requires VPP expertise, tuning)          |
| **Compatibility**        | Broadest — works everywhere            | Requires kernel 5.3+                       | Requires DPDK-ready NICs, tuned environment    |
| **Network Policy**       | Fully supported (K8s + Calico policy)  | Fully supported (K8s + Calico policy)      | Fully supported                                |
| **Overlay Support**      | VXLAN, IPIP                            | VXLAN (no IPIP)                            | VXLAN, Geneve                                  |
| **Host Endpoint Policy** | Supported                              | Partially supported                        | Supported                                      |
| **Windows Support**      | Yes                                    | No                                         | No                                             |
| **TLS support (BGP)**    | Yes                                    | Yes                                        | Yes                                            |



