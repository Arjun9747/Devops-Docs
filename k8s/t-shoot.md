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
