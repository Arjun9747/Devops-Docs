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
