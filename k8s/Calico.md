Calico is a networking (security) solutions for K8s. It provides networking, n/w policy enforcement and IP addr mgmt using standard Linux networking tools. 

**Existing Policies**
Calico global Network Polciies 

allow communication between same namespace 
all workloads can dissolve dns name 
ensure dns queries to kube-system (where core dns runs) are always permitted regardless of their network polcies
all unmatched traffic will be logged 

**Gatekeeper Policies** 

Pull container images from private registry without manual interventions 

**How Calico Works?**

1. CNI Integration: Calico configures networking when pods starts using CNI specification. 
2. Routing: Pods gets a routable IP, and Calico sets up IP routes so that pods can communicate across nodes
3. Policy Enforcement: Enforces L3/L4 networking policies based on lables, namespace e.t.c.
4. Optional BGP : Can advertise pod routes across your data center or cloud network via BGP.

**Deployment Options:**
1. Calico with etcd (Self managed backend)
2. Calico with K8s API
3. Calico with BGP mode (for advanced n/w)

**When to use Calico**
1. You need fine grained networking policies
2. You want high performance scalable netwrorking
3. Need integration with cloud or on-prem routing via BGP

**Namespaces**
Calico System namespace 
Calico API Server
tigeria Operator

Calico system namespace is the main namespace where calico components are run 
1. Calico-node: Core Agent that runs on node. Handles pod networking , routing and enforce policies
2. Calico-Kube-Controllers: Syncs Calico specific resources (IP Pools Networking resources in k8s)

Calico uses dynamic subnet allocation scheme with either k8s API server or its own etcd cluster. When Calico installed it assigns each node blocks of ips to the pod of that node. 

The default encapsulation for Calico is IP-in-IP protocol. 
Refers to how calico enables cross node pod communication when native routing is not available.

Encapsulation in networking means wrapping one packet inside another . This is used when direct routing between source and destination is not possible or not efficent. 

**IP-in-IP protocol** that encapsulate and IP packet within another IP packet.
1. Outer IP header : used for routing between the nodes
2. Inner IP packet: the original pod to pod traffic

**Cross node pod Communication**  If k8s nodes are on different subnets and can't reach each other pod CIDR directly, IP-in-IP allows calico to route traffic directly.
**Overlay Networking** Acts like a light weight overlay when routes are not available.
Overlay networking is a virtual network layer built on top of an existing physical (underlay) network. It allows you to create isolated, software-defined networks (SDNs) that are independent of the underlying hardware.
**Simplifies Setup** No need to manually configure complex routing or BGP. 

**Real time Scenario**
1. Pod A on Node 1 (10.0.1.2) wants to talk to Pod B on Node 2(10.1.1.3)
2. Nodes don't have routes to each other pods
3. Calico wraps the packets from Pod A in another Packet with the outer header going to Node 2
4. Node 2 unwraps it and delivers to Pod B

                                            **Intial Configuration**

   **Pod Networking Namespace**
   1. K8s create new networking namespace for that pod
   2. It does not share host networking namespace unless specified (hostNetwork: true)
   3. The pod has its own loopback interface and its own virtual ethernet interface (eth0)
   4. The pod thinks as its own network
  
   **Host Network Namespace**
   1. Default networking namespace of the kubernets nodes
   2. Contains real n/w i/f
   3. Process like kubelet , containerd and os level services run here

   Calico creates veth one end goes to pod networking namespace as eth0 and other end stays in host networking namespace, connected to a calico bridge or device .

**Network Policies**
Each pod is a calico endpoint 
2 types of calico endpoints
1. Workdload endpoints (pods)
2. Host endpoints (interface on a host)

**Types**
1. Network Policies --> Applied to pods,vm, container
2. Global Network Policies --> Applied to any endpoint like pods/containers/vm/host interface

**Calico Resources**
1. Felix : Calico Agent that handles networking
2. IPAM : Manages IP block
3. Block Affinity : Track block affinity for ip addr mgmt
4. BGP Peers
5. IP Pools: Manages pool of ip address
6. Host Endpoints: Configure Host Specific Endpoints
7. Cluster Information
8. Global Network Policy: Represent sets of IP globally
9. Global Network Sets: Define namespace scoped network policy
10. Network Sets: Represent namespace scopes set of IPs

<img width="303" alt="image" src="https://github.com/user-attachments/assets/f20a807c-21da-470e-baff-2595cb9a4a7e" />






   
















