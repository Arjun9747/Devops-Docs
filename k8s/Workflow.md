**Liveness Probe and Readiness Probe**

**When liveness Probe fails**

• Purpose: To check if the Pod is alive or stuck in an unhealthy state.

• Trigger: If the application inside the container is not responding (e.g., deadlock, infinite loop).


• **Action Taken:*

  • Kubernetes kills the container and attempts to restart it based on the Pod's restartPolicy.
  
  * The Pod is not removed, only the container inside is restarted.

**When readiness Probe fails**

• Purpose: To check if the Pod is ready to serve traffic.

• Trigger: If the application inside the container is not ready (e.g., waiting for a database connection, initialization tasks).


• *Action Taken:*

	• The Pod is removed from the Service endpoints.
 
	• No traffic is sent to the Pod, but the container remains running.
 
	• Kubernetes continues to probe, and if it becomes healthy again, it is added back to the Service.

 ******************************************************************************************************

 **Deployments** are designed for stateless applications, where data persistence across pod restarts is typically not required.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: nginx-storage
          mountPath: /usr/share/nginx/html
      volumes:
      - name: nginx-storage
        persistentVolumeClaim:
          claimName: nginx-pvc
```
**StatefulSets** are for stateful applications where each pod needs its own independent storage.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-statefulset
spec:
  serviceName: "mysql"
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: mysql-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 5Gi
```


| Feature | Deployment | StatefulSet |
| --- | --- | --- |
| Pod Identity | All replicas are identical; pod names are dynamic (e.g., `my-app-xyz`). | Each pod gets a unique, persistent identity (e.g., `my-app-0`, `my-app-1`). |
| Storage Persistence | PVCs are shared across all pods if not managed correctly. | Each pod gets its own dedicated PVC, managed by its ordinal index. |
| Pod Order | All pods start and stop simultaneously, in any order. | Pods start and terminate sequentially (`0 → 1 → 2`). |
| Network Identity | Pods get random DNS names. | Each pod has a stable DNS identity: `pod-name.service-name.namespace.svc.cluster.local`. |
| Use Cases | Stateless apps (web servers, APIs). | Stateful apps (databases, Kafka, Zookeeper). |



| Aspect            | Deployment                               | StatefulSet                                                                |
| ----------------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| PVC Usage         | Shared among all pods                    | Each pod gets its own PVC (`app-storage-my-app-0`, `app-storage-my-app-1`) |
| PVC Configuration | Directly referenced in `volumes`         | Defined in `volumeClaimTemplates`                                          |
| Access Mode       | Usually `ReadWriteMany` (RWX) for shared | Typically `ReadWriteOnce` (RWO) for individual storage                     |

#You need to create a separate Persistent Volume Claim (PVC) object and reference it in the Deployment YAML.

## VolumeClaimTemplates vs PVC

**VolumeClaimTemplates** and **PersistentVolumeClaim (PVC)** are both used to provision storage resources in Kubernetes, but they serve different purposes and have different use cases.

### PersistentVolumeClaim (PVC):
- A PVC is a request for storage resources that can be fulfilled by a Persistent Volume (PV).
- A PVC is a separate object that needs to be created and managed independently.
- A PVC can be used by multiple pods, and all pods will share the same storage resources.
- PVCs are typically used in stateless applications where data is not critical or can be easily recreated.

### VolumeClaimTemplates:
- VolumeClaimTemplates is a field in StatefulSets that allows you to define a template for creating PVCs.
- When a StatefulSet is created, Kubernetes automatically creates a PVC for each replica based on the template.
- Each replica will have its own dedicated PVC, and the PVC name will be generated automatically based on the StatefulSet name and replica index.
- VolumeClaimTemplates are typically used in stateful applications where each replica needs its own dedicated storage resources.

### Key differences:
| Aspect               | PVC                                           | VolumeClaimTemplates                             |
|----------------------|-----------------------------------------------|-------------------------------------------------|
| **Management**       | PVCs need to be created and managed separately | Managed automatically by Kubernetes with StatefulSet |
| **Storage sharing**  | PVCs can be shared by multiple pods           | Creates a separate PVC for each replica          |
| **Use case**         | Suitable for stateless applications            | Suitable for stateful applications                |


**External Services**

External Service is a way to expose a service running outside of your Kubernetes cluster to be accessible within the cluster as if it were a native Kubernetes service. This allows internal applications to communicate with external databases, APIs, or legacy systems without complex networking configurations.

Use Case: Connecting to legacy systems, third-party APIs, or databases hosted outside of Kubernetes.

***************************************************************************************************
**External Service**

An External Service in Kubernetes is a way to expose applications running outside of your Kubernetes cluster to services running inside the cluster. It allows Kubernetes-managed applications to connect to external databases, third-party services, or APIs.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-rds-database
  namespace: default
spec:
  type: ExternalName
  externalName: mydb-instance.xxxxxxxxxx.us-east-1.rds.amazonaws.com
```
**type:** ExternalName — This allows you to map the service to an external DNS name.

**externalName** — This is the DNS name of your RDS instance. You get this from the RDS dashboard.


    
    


