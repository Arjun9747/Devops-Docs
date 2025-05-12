
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

<img width="299" alt="image" src="https://github.com/user-attachments/assets/0e9dd1e0-078d-4b94-96a4-d4b337fbb9e4" />


In the Node we create **Pod** .
This Pod has 2 **Containers**
Both Container share the same IP address (i.e the ip addr of the Pod) 
If container 1 wants to talk to Container 2 , they will go through local host 
Pods of different container communicate each other through bridge 

**Node to Node Communication**
<img width="600" alt="image" src="https://github.com/user-attachments/assets/8193be1f-da93-4d9e-a8ea-5031e71d9e97" />
Happens thorugh CNI 

**Network Namespace**
Provide Network namespace isolation 
<img width="630" alt="image" src="https://github.com/user-attachments/assets/b821e223-ef58-44d2-bb60-c57efc937edf" />



