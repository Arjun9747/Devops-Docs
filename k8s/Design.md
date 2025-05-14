**Stateful Sets**
![image](https://github.com/user-attachments/assets/0f5b6317-738a-46bb-8146-f7b5558f6b65)

| **Volume Type**              | **Details**                                                                                                                                                            |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Empty Dir**               | **Usage:** Temporary storage shared between containers in a Pod.  <br> **Lifecycle:** Created when Pod starts, deleted when Pod is removed.  <br> **Use Case:** Scratch space, shared cache between init and main containers. |
| **Generic Ephemeral Vols**  | **Type:** Ephemeral but more flexible than `emptyDir`. <br> **Usage:** Based on standard PVCs but automatically managed per Pod.  <br> **Use Case:** Use when you need storage class features but want automatic cleanup. |
| **CSI Ephemeral Vols**      | **Type:** Ephemeral. <br> **Usage:** Provided by a CSI (Container Storage Interface) driver without needing a PVC. <br> **Use Case:** When you need runtime-managed storage with CSI capabilities like encryption or snapshotting. |
| **Config Map**              | **Type:** Ephemeral (though tied to ConfigMap object). <br> **Usage:** Inject configuration data into containers as files. <br> **Use Case:** App settings, config files. |
| **Downward API**            | **Type:** Ephemeral. <br> **Usage:** Expose pod and container metadata (e.g., name, labels) to containers. <br> **Use Case:** Apps needing pod-specific info without hardcoding. |
| **Secret**                  | **Type:** Ephemeral (tied to Kubernetes Secret). <br> **Usage:** Store sensitive info like passwords, tokens, keys. <br> **Use Case:** Secure app configs. |


**Observability**

<img width="368" alt="image" src="https://github.com/user-attachments/assets/b611b011-f414-4fff-ac43-4d511f838777" />

