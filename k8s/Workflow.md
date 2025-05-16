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


**Node Disk Pressure**

 ******************************************************************************************************

| Feature | Deployment | StatefulSet |
| --- | --- | --- |
| Pod Identity | All replicas are identical; pod names are dynamic (e.g., `my-app-xyz`). | Each pod gets a unique, persistent identity (e.g., `my-app-0`, `my-app-1`). |
| Storage Persistence | PVCs are shared across all pods if not managed correctly. | Each pod gets its own dedicated PVC, managed by its ordinal index. |
| Pod Order | All pods start and stop simultaneously, in any order. | Pods start and terminate sequentially (`0 → 1 → 2`). |
| Network Identity | Pods get random DNS names. | Each pod has a stable DNS identity: `pod-name.service-name.namespace.svc.cluster.local`. |
| Use Cases | Stateless apps (web servers, APIs). | Stateful apps (databases, Kafka, Zookeeper). |



    
    


