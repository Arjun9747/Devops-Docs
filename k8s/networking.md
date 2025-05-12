
**Types of Networking**
1. Node
2. Pod
3. Cluster

<img width="470" alt="image" src="https://github.com/user-attachments/assets/5a4a7eef-41d5-40f3-bff9-499c12a07c60" />


**K8s N/w rules**
1. All pods can communicate with each other
2. Agents on one node can communicate with all the pods of the node
3. No NAT

**How Pods communicate with each other**

In the Node we create **Pod** .
This Pod has 2 **Containers**
Both Container share the same IP address (i.e the ip addr of the Pod) 
