**Crashloopback**

CrashLoopBackOff means the pod is repeatedly crashing and Kubernetes is backing off (delaying) before restarting it again.

It usually happens when the container inside the pod exits with an error shortly after starting.

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous
kubectl get pods -n <namespace>
kubectl get events --sort-by='.lastTimestamp'
kubectl get pod <pod-name> -o yaml
```
 Application error -->Crashes due to bugs, missing files, config issues
 
🔢 Bad command/entrypoint-->	Incorrect CMD or ENTRYPOINT in Dockerfile

🔐 Missing secrets/configs-->	App fails due to missing env vars, configs, secrets

📄 Misconfigured volumes-->	App can't access mounted volume path

🛑 Probes fail-->	Liveness/readiness probes fail and restart the pod

🧵 Resource limits -->	OOMKilled if it uses more memory than allowed

**Pod in Pending state**

Pending state means Kubernetes has accepted the pod configuration but hasn’t scheduled it onto a node yet.

🧠 Insufficient resources -->	No node has enough CPU or memory

🛑 Node taints	-->All nodes are tainted and prevent pod scheduling

⚠️ Missing PVC	--> Pod requests a PersistentVolumeClaim that isn't bound

🚫 Wrong nodeSelector/affinity-->	Pod has constraints that no nodes satisfy

🔐 ServiceAccount/Secrets issues--->	Pod depends on secrets or accounts that don’t exist

```bash
kubectl get pods & nodes
kubectl get pvc
kubectl get nodes -o json | jq '.items[].spec.taints'
kubectl describe nodes | grep -A5 Taints
```

| Status               | When it Happens                        | What it Means                             |
| -------------------- | -------------------------------------- | ----------------------------------------- |
| **ErrImagePull**     | First failed attempt to pull the image | Initial error pulling the container image |
| **ImagePullBackOff** | After multiple failed attempts         | Kubernetes backing off and retrying pull  |

**Pod stuck in terminating state**

Finalizers blocking deletion  --> manually remove finalizers (force delete) if safe:

Pod stuck due to running processes  [ kubectl delete pod <pod-name> --grace-period=0 --force]

Node or kubelet issues --> unreachable nodes

Network/storage resources hanging --> Vols mounts blocking | unmount 


NodeNotReady means Kubernetes has detected that a node is not healthy or unreachable, 
so it marks the node as NotReady.
```bash
kubectl get nodes
kubectl describe node <node-name>
sudo systemctl status kubelet
sudo systemctl restart kubelet
top
df -h
free -m
sudo systemctl status docker    # or containerd
sudo journalctl -u kubelet -f
curl -k https://<api-server-ip>:6443/healthz
```

**PVC not bound**

PVC (PersistentVolumeClaim) not bound means your claim for storage has not been successfully matched to any PersistentVolume (PV).

```bash
kubectl get pvc
kubectl describe pvc <pvc-name>
kubectl get pv
kubectl describe pv <pv-name>
kubectl get storageclass
```
**Error syncing pod**

kubelet failed to synchronize the desired state of the pod with the actual state on the node.

```bash
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>                # If container has started
sudo journalctl -u kubelet -f          # On node
sudo systemctl status kubelet
sudo systemctl status docker           # Or containerd
top
df -h
free -m
```
**"Failed to create pod sandbox**

Failed to create pod sandbox" is an error message that typically occurs in Kubernetes when the container runtime (e.g., Docker, containerd) is unable to create the network namespace (sandbox) for a pod.

```bash
kubectl get pods -A
kubectl describe pod <pod-name> -n <namespace>
sudo systemctl status containerd     # or docker
sudo systemctl restart containerd
sudo journalctl -u kubelet -f
sudo journalctl -u containerd -f
ls /etc/cni/net.d/
ls /opt/cni/bin/
top
df -h
free -m
```

**FailedScheduling**

This error occurs when the Kubernetes scheduler is unable to find a suitable node to place a pod.

```bash
kubectl get pods -A
kubectl describe pod <pod-name> -n <namespace>
kubectl get nodes
kubectl describe node <node-name>
kubectl top nodes
kubectl uncordon <node-name>
kubectl describe node <node-name> | grep -i taints
```

**Pod Utilization**

```bash
kubectl top pods --all-namespaces
```
**Dynatrace**

Connect EKS cluster to Dynatrace via oneAgent 

Create Namespace 

Paste the dynatrace token

Enable Workload and Pod Resource Monitoring using Dynakube 

```yaml
# values.yaml (or --set parameters in helm)
dynakube:
  apiUrl: "https://<your-env>.live.dynatrace.com/api"
  oneAgent:
    classicFullStack:
      enabled: true
  kubeMon:
    enabled: true
    # Optional but recommended for resource metrics:
    resources:
      requests:
        cpu: 100m
        memory: 200Mi
```

Custom Queries

```text
builtin:kubernetes.pod.cpu.usage
builtin:kubernetes.pod.memory.usage
```










