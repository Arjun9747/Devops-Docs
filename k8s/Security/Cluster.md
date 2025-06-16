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

4. Version Skew Policy
Ensures compatibility between kubelet, kubeadm, and control plane.

Important during upgrades: kubelet must not lag behind API server by more than 1 minor version.

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

🔒 What’s Missing? (Advanced & Real-World Hardening)
7. Pod Security Standards (PSS)
Successor to PodSecurityPolicy (deprecated).

Enforce baseline or restricted pod security modes.

Use PodSecurity admission controller.

yaml
Copy
Edit
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
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
