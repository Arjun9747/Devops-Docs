Calico is a networking (security) solutions for K8s. It provides networking, n/w policy enforcement and IP addr mgmt using standard Linux networking tools. 

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

##Namespaces
Calico System namespace 
Calico API Server
tigeria Operator

Calico system namespace is the main namespace where calico components are run 














