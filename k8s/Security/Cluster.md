```markdown
1. Authentication & Authorization
Authentication: Who are you?
→ Users, Service Accounts, Certificates, OIDC.

Authorization: What can you do?
→ Enforced via RBAC (Role-Based Access Control).

Best Practices:

Use OIDC with identity providers.

Rotate certificates/tokens periodically.

2. RBAC (Role-Based Access Control)
Role and RoleBinding: Namespaced permissions.

ClusterRole and ClusterRoleBinding: Cluster-wide.

Creating Tokens: Manual token creation for service accounts (used in CI/CD or external integrations).

Least Privilege Principle: Only grant what's necessary.

3. Service Accounts
Default account exists per namespace.

Attach service accounts explicitly to pods.

Best Practices:

Avoid using the default service account.

Use automountServiceAccountToken: false if not needed.

Rotate service account tokens.

Use Projected Service Account Tokens for secure and short-lived tokens (enhanced in v1.21+).

```
**Version Skew Policy**

Ensures compatibility between kubelet, kubeadm, and control plane.

Important during upgrades: kubelet must not lag behind API server by more than 1 minor version.

During upgrades, you don’t update everything at once. So Kubernetes must allow different versions of components to coexist temporarily.

| Component     | Version Skew Allowed                                     |
| ------------- | -------------------------------------------------------- |
| `kubelet`     | Up to **1 minor version behind** API server              |
| `kubeadm`     | Must be **same version as control plane**                |
| Control Plane | Components must be **same version**                      |
| `kubectl`     | Up to **1 minor version** older or newer than API server |

```makrdown
5. Cluster Upgrades
Use kubeadm for controlled upgrades.

Upgrade order:

Master (control plane)

kubelet & kube-proxy on workers

Verify compatibility using kubeadm upgrade plan.

6. Projected Volumes
Mechanism to inject secrets, configMaps, service account tokens into pods.

Supports:

Combining multiple sources.

Setting expiration and audience for tokens.
```
**Pod Security Standards (PSS)**

Successor to PodSecurityPolicy (deprecated).

Enforce baseline or restricted pod security modes.

Use PodSecurity admission controller.

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
```

```rst
1. Privileged Profile
The Privileged profile is the most permissive among the three Pod Security Standards (Privileged, Baseline, Restricted). It allows workloads to use powerful and potentially dangerous capabilities, which are typically restricted for security reasons.

✅ What It Allows
hostPath volumes
Grants direct access to the host filesystem.

Pods can read/write directories like /etc, /var, /dev, etc.

Risk: Compromised pod can tamper with host OS.

hostNetwork: true
Pod uses the host’s network stack.

Shares the host IP, interfaces, and port namespace.

Use Case: Apps that need to bind to specific ports (like node exporters).

hostPID: true
Pod shares the host’s PID namespace.

Can see and interact with all processes on the host.

Risk: Breaks isolation — possible to snoop or kill host processes.

Running as root (runAsUser: 0)
Containers can run as root user inside the pod.

Required by some legacy applications or system-level agents.

privileged: true in securityContext
Grants full access to host kernel capabilities (like CAP_SYS_ADMIN, CAP_NET_ADMIN).

Almost like having full host access.

Risk: High – attacker could break out of container jail.

🧪 Example Use Cases
These are legitimate scenarios where the privileged profile is necessary:

📦 Logging Agents
Tools like Fluentd, Logstash, or Filebeat often need access to:

/var/log

/var/lib/docker/containers

Use hostPath to collect logs directly from host.

📈 Monitoring DaemonSets
Node exporters (e.g., Prometheus Node Exporter) or metrics collectors need:

Host network access

Access to /proc, /sys

May run as privileged to gather CPU, memory, kernel metrics

🛠️ System Management Tools
Tools like nsenter, iptables, or eBPF tracers often run with elevated privileges.

“Only for critical system-level tools that require direct host interaction, and only in isolated namespaces with strict monitoring in place.”

```

2. Baseline Profile
Prevents known privilege escalations.

Disallows:

hostPath

hostPID / hostIPC

Privileged containers

capabilities: ALL

Allows:

Running as root (but no escalation)

Some volume types

Goal: Accept most apps with minor changes

3. Restricted Profile
Enforces strict security policies.

Requires:

runAsNonRoot: true

readOnlyRootFilesystem: true

seccompProfile, AppArmor, SELinux

Explicit capabilities (dropping defaults)

Goal: Strong isolation, secure-by-default

🔐 Advanced PSS Practices
🔹 4. Namespace-Based Enforcement
You can apply Pod Security Standards per namespace using Kubernetes labels:

kubectl label namespace dev \
  pod-security.kubernetes.io/enforce=baseline \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
enforce: Blocks non-compliant pods.

audit: Logs violations (no block).

warn: Shows warning in kubectl.

🔹 5. Enforcement Modes
You can define separate levels for:

enforce: Actual enforcement

audit: Log-only mode

warn: CLI warning

This helps in gradual adoption of stricter policies.

🔹 6. Using Custom Policy Engines
While PSS is good for standard hardening, OPA/Gatekeeper or Kyverno allow:

Custom policies (e.g., enforce image tags, labels)

Multi-tenant enforcement

JSON/YAML schema validation

🔹 7. Monitoring with Audit Logs
Use audit level to test impact before enforcing.

Integrate logs with SIEM tools.

🔹 8. Hardening Beyond PSS
PSS covers pod specs, not everything. Additional layers include:

Network Policies

Runtime protection (e.g., Falco)

Admission controllers (ValidatingWebhook, OPA)

🧠 Interview Tip
Expect questions like:

What's the difference between Baseline and Restricted?

How do you enforce PSS in production?

How do you apply PSS gradually to legacy workloads?

Can you customize PSS? (→ No, for customization use OPA/Kyverno)

✅ Summary Table
Level	Restricts	Allows Root	Allows Privileged	Use Case
Privileged	Nothing	Yes	Yes	Trusted system pods
Baseline	hostPath, escalations	Yes	No	General workloads
Restricted	Most risky features	No	No	Secure environments (prod)

```



8. Network Policies
Restrict pod-to-pod and pod-to-service communication.

Works only if CNI plugin supports it.

Example: Deny all egress traffic by default.

9. Runtime Security
Integrate tools like:

Falco – Monitors syscalls in real time.

AppArmor / SELinux / Seccomp – Linux kernel-level hardening.

KubeArmor – LSM-based workload protection.

10. Container Security Practices
Run containers as non-root.

Use minimal base images.

Read-only root file system.

Drop unnecessary Linux capabilities (capabilities.drop).

11. ETCD Protection
Store all cluster state.

Secure with:

TLS encryption

Authentication

Encryption at rest

Restrict access to API server only.

12. API Server Security
Disable anonymous access.

Enable audit logs.

Restrict API server via API Gateway or WAF.

13. Image and Supply Chain Security
Scan container images using Trivy, Grype, etc.

Enforce image signature verification using cosign or Notary v2.

Use a private registry with access control.

14. Audit Logs
Enable API server audit logging.

Export logs to SIEM (e.g., ELK, Datadog).

Define audit policies for alerting.

15. Policy Engines
OPA/Gatekeeper or Kyverno:

Enforce policies like: disallow hostPath, require resources, enforce labels.

📘 Final Tips for Interview
Know the difference between built-in vs external security features.

Be ready to explain real-world attack vectors like:

Privilege escalation

Token theft

Misconfigured RBAC or default service accounts

Know hardening tools: kube-bench, kubescape, kube-hunter, OPA, Kyverno

Practice hardening CIS Benchmarks using tools like kube-bench.

1. Disable Anonymous Access
Ensure --anonymous-auth=false in the API server.

Prevent unauthenticated access to cluster components.

2. Use Role-Based Access Control (RBAC)
Define Roles and ClusterRoles.

Bind them only to the necessary Users or ServiceAccounts.

Principle: Least Privilege

3. Secure Service Accounts
Don’t use default service accounts.

Use automountServiceAccountToken: false when not needed.

Rotate tokens periodically.

4. Use Network Policies
Define allowed ingress/egress per namespace or pod label.

Restrict pod-to-pod communication by default.

5. Pod Security Standards (PSS)
Enforce one of:

privileged

baseline

restricted

Ensure pods don’t run as root or use host resources.

6. Use Read-Only Root Filesystems
Prevent modifications inside containers by setting readOnlyRootFilesystem: true.

7. Restrict Host Access
Avoid using hostPath, hostNetwork, hostPID, and hostIPC unless explicitly required.

8. Resource Requests and Limits
Set CPU/memory limits to avoid DoS attacks due to resource starvation.

9. Use Liveness & Readiness Probes
Helps detect and recover from broken applications.

Also limits abuse via failing pods.

10. Secure ETCD
Use TLS for client/server communication.

Enable authentication.

Enable encryption at rest.

🔐 Advanced Kubernetes Cluster Hardening Techniques
These go beyond the basics and focus on runtime protection, admission control, compliance, and infrastructure hardening:

11. Enable Audit Logs
Set up audit-policy.yaml and enable it via API server flags.

Forward logs to a SIEM system.

12. Admission Controllers
Enable useful ones like:

NamespaceLifecycle

PodSecurity

NodeRestriction

LimitRanger

SecurityContextDeny (deprecated, replaced by PSS)

13. Use Pod Security Admission (PSA)
Kubernetes-native way to enforce PSS (baseline/restricted).

Replace legacy PodSecurityPolicy (PSP).

14. Use Policy Engines
OPA/Gatekeeper or Kyverno for fine-grained custom policy enforcement:

Disallow latest tags in images.

Require labels on resources.

Block privileged containers.

15. Implement Runtime Security Tools
Falco – Real-time syscall monitoring.

AppArmor / SELinux / Seccomp – Kernel-level isolation.

KubeArmor – LSM-based runtime enforcement.

16. Upgrade Kubernetes Regularly
Stay within the supported version skew.

Regularly apply security patches to Kubernetes and container runtimes.

17. Image and Supply Chain Security
Sign images with cosign.

Scan images using Trivy, Grype, or Aqua Microscanner.

Enforce image provenance and registries.

18. Encrypt Secrets at Rest
Use KMS providers for key management.

Encrypt Secrets and ConfigMaps using envelope encryption.

19. Use Projected Volumes for Service Account Tokens
Short-lived, audience-bound tokens reduce risk of token theft.

20. Monitor & Harden Node Infrastructure
Harden OS (CIS Benchmarks).

Use tools like kube-bench, kube-hunter to test cluster security.

Restrict SSH access, remove unnecessary packages.

✅ Summary Table
```
