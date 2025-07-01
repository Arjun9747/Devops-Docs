**Check DNS POD health**

🔹 1. Check CoreDNS Pod Health

kubectl get pods -n kube-system

```bash
NAME                        READY   STATUS    RESTARTS   AGE
coredns-6955765f44-kgl7g    1/1     Running   0          2d
coredns-6955765f44-tbxf9    1/1     Running   0          2d
```
🔹 2. Verify CoreDNS Service

kubectl get svc -n kube-system

```bash
NAME       TYPE        CLUSTER-IP    PORT(S)         AGE
kube-dns   ClusterIP   10.96.0.10    53/UDP,53/TCP    2d
```

kubectl get configmap coredns -n kube-system 

```bash
cluster.local:53 {
    log
    any
    health {
        lameduck 5s
    }
    ready
    kubernetes
    prometheus :9153
    reload
    loop
    loadbalance
}

.:53 {
    log
    any
    prometheus :9153
    forward . /etc/resolv.conf
    cache
    loop
}
```

This config defines two separate server blocks:

cluster.local:53: Handles DNS queries within the Kubernetes cluster domain.

.:53: Handles all other (non-cluster) DNS queries (e.g., external lookups like google.com).

🔹 cluster.local:53 { ... }
This block is for in-cluster DNS resolution (e.g., myservice.default.svc.cluster.local).

👇 Internal DNS resolution example:
Query: nginx.default.svc.cluster.local

Handled by: cluster.local:53 block → resolved via kubernetes plugin

👇 External DNS resolution example:
Query: www.google.com

Handled by: .:53 block → forwarded to upstream DNS (like 8.8.8.8) via forward plugin





