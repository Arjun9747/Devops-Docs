```markdown


Pod connection issues 

🔹 1. Verify Basic Connectivity

kubectl exec -it <src-pod> -n <namespace> --ping <destination-pod-ip>
kubectl exec -it <src-pod> -n <namespace> --curl -v <destination-pod-ip>:<port> 

Confirm if its pod specific or node specific 
Test pods within same nodes vs across nodes 

2.Check Calico health staus 

kubectl get pods -n calico-system
kubectl -n calico-system logs -l k8s-app=calico-node

Look for pod restarts / crash 
check felix logs for network faliures

verify BGP peering

calicoctl node status 

ensure all bgp are in established state 

kubectl -n kube-system logs -l k8s-app=kube-proxy 

Look for errors related to ip tables 

5. Check Routing 
ip a 
ip a | grep cali 

6. check ip tables or drop packets
sudo iptables -L -n -v |grep DROP

7.check ip conflict 
calicoctl ipam show 

**************************************************************
Q2: The issue only manifests when pods on Node A communicate with pods on Node B, while intra-node communication works fine. How would you proceed?


🔹 Step 1: Verify Node-to-Node Connectivity
ping <node-B-internal-IP>
traceroute <node-B-internal-IP>

🧠 If ping fails, it’s a host network or cloud-level issue

kubectl -n calico-system get pods -o wide
kubectl -n calico-system logs -l k8s-app=calico-node --tail=100

🚨 Crashes, restarts, or consistent errors in Felix logs may indicate IPAM or BGP route propagation issues.

calicoctl node status

*********************************************************
Q3: How would you troubleshoot a pod's inability to reach external services like AWS RDS databases?

kubectl exec -it <pod-name> -- nslookup <external-domain>

kubectl exec -it <pod-name> -- telnet <external-ip-or-domain> <port>

kubectl get networkpolicy -A
kubectl describe networkpolicy <policy-name>

calicoctl get globalnetworkpolicy
calicoctl get networkpolicy

inspect kube-proxy
kubectl -n kube-system get pods -l k8s-app=kube-proxy
kubectl logs <kube-proxy-pod> -n kube-system

*************************************************************************

Q4: Users report that a ClusterIP service is randomly dropping about 30% of requests. What's your investigation plan?

Packet Drops

1️⃣ Check for Node-Level Correlation

Determine if the packet drops are isolated to specific nodes by examining the distribution of endpoints and their health:

kubectl get endpoints -A -o wide
kubectl get pods -o wide -A
kubectl describe endpoints <svc-name> -n <namespace>


2️⃣ Inspect kube-proxy Logs for Sync Errors

Check for iptables sync delays or errors in kube-proxy logs:
kubectl -n kube-system get pods -l k8s-app=kube-proxy

3️⃣ Consider Switching kube-proxy to IPVS Mode
kubectl get configmap kube-proxy -n kube-system -o yaml | grep mode
# Look for: mode: "iptables" or "ipvs"

5️⃣ Tune nf_conntrack Parameters (if needed)

# Increase maximum number of tracked connections
sysctl -w net.netfilter.nf_conntrack_max=131072

# Optional: Persist in /etc/sysctl.conf or /etc/sysctl.d/99-custom.conf
echo "net.netfilter.nf_conntrack_max = 131072" >> /etc/sysctl.conf

# Tune GC intervals
sysctl -w net.netfilter.nf_conntrack_tcp_timeout_established=86400
sysctl -w net.netfilter.nf_conntrack_tcp_timeout_time_wait=30

We faced a large-scale drop incident where kube-proxy iptables performance degraded under >10K services.
 Switching to IPVS improved sync speed and throughput. However, lingering drops remained until we increased
 nf_conntrack_max from the default (65536) to 262144 and tuned GC parameters. This fully resolved the packet loss.
 
 **************************************************************************
 Q5: DNS resolution inside pods is intermittently failing. How would you diagnose this?
 
 1️⃣ Check CoreDNS Pod Health & Logs

kubectl -n kube-system get pods -l k8s-app=kube-dns
kubectl -n kube-system logs -l k8s-app=kube-dns

Check logs for DNS errors, plugin issues, timeouts:

Look for:

plugin/errors
timeout
unreachable backend
resource limit exceeded

2️⃣ Verify kube-dns Service and Endpoints

kubectl get svc kube-dns -n kube-system


3️⃣ Examine Pod's /etc/resolv.conf

kubectl exec -it <pod-name> -- cat /etc/resolv.conf

nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5

The ndots option controls how many dots must appear in a name before the resolver treats it as a fully qualified domain name (FQDN).

If a domain has fewer dots than this value, the resolver appends the search domains before attempting the actual name.

⚠️ Why ndots:5 Can Be Problematic
Suppose an application makes a DNS request for google.com, and ndots is set to 5.

google.com has only 1 dot → less than 5 → not treated as FQDN.

The resolver will try:

google.com.default.svc.cluster.local

google.com.svc.cluster.local

google.com.cluster.local

Finally: google.com

This causes:

Multiple failed DNS lookups

Increased latency (as each one waits to fail or timeout)

Extra load on CoreDNS

Set ndots:2 (or lower) unless you have a strong reason not to

5️⃣ Inspect NetworkPolicies for DNS Access
Make sure pods can access kube-dns (UDP/53, TCP/53):

kubectl get networkpolicy -A
kubectl describe networkpolicy <policy-name>

6️⃣ Detect Node-Level DNS Caching Conflicts

******************************************************************

Q6: Newly created pods can't get IP addresses assigned. What's your troubleshooting approach?

🔍 Step 1: Check kubelet logs for CNI errors
journalctl -u kubelet -f | grep -i cni
# or on systems using containerd:
journalctl -u containerd -f | grep -i 'ipam\|cni'

🔍 Step 2: Check Calico CNI logs on the node

kubectl logs -n kube-system -l k8s-app=calico-node
kubectl logs -n kube-system -l k8s-app=calico-node -c calico-node -o wide --tail=1000


🔍 Step 3: Inspect IP pool usage (Calico-specific)
# View all Calico IP pools
calicoctl get ippools -o wide

# Check for usage and allocated blocks
calicoctl get ipamblocks -o wide | less

# See current allocations by pod
calicoctl ipam show --show-blocks

🔍 Step 5: Validate connectivity to Calico control plane (e.g., Typha)

kubectl get pods -n kube-system -l k8s-app=calico-typha
kubectl logs -n kube-system -l k8s-app=calico-typha

******************************************************************************

Network Problems 

🔍 1. Start with Basic Connectivity Checks

✅ Check Pod-to-Service Connectivity:
kubectl exec -it <pod-name> -- curl http://<service-name>.<namespace>.svc.cluster.local:<port>

✅ Validate DNS resolution:
kubectl exec -it <pod-name> -- nslookup <service-name>

✅ Test raw TCP connectivity:
kubectl exec -it <pod-name> -- nc -vz <target-host> <port>

🐞 2. Real-Time Debug with Ephemeral Containers
kubectl debug -it <pod-name> --image=nicolaka/netshoot --target=<container-name> -- bash

```
