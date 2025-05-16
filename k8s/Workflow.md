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

<img width="483" alt="image" src="https://github.com/user-attachments/assets/36cff448-b2a0-4019-8ef3-f6b647d406b4" />



    
    


