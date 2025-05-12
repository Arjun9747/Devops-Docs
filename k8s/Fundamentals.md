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





