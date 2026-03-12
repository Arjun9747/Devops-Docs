# CI/CD Pipeline – Follow-up Interview Questions

These are common **follow-up questions asked by interviewers** when discussing CI/CD pipelines and DevSecOps practices.

---

# 1. How do you secure secrets in your pipeline?

## Expected Discussion Points

- Store secrets in **GitHub Secrets**
- Use **OIDC authentication** to AWS
- Avoid hardcoding credentials
- Retrieve secrets from **AWS Secrets Manager**

## Good Answer

We avoid static credentials and use **GitHub OIDC** to assume IAM roles in AWS.  
Secrets like **database passwords** are stored in **AWS Secrets Manager** and injected into Kubernetes as secrets during deployment.

---

# 2. How do you prevent vulnerable dependencies from reaching production?

## Key Points

- Software Composition Analysis (SCA)
- CVE detection
- License checks

## Tools

- SonarQube Dependency Check
- Trivy
- Prisma Cloud

## Best Practice

The pipeline **fails automatically** if **critical vulnerabilities** are detected.

---

# 3. How do you handle versioning of artifacts and Docker images?

## Approach

Use **Semantic Versioning**

## Examples

```
app:1.2.0
app:1.2.1
app:commit-sha
```

## Best Practices

- Avoid using **latest** tag in production
- Use **immutable tags**
- Maintain proper version traceability

---

# 4. What happens if a deployment fails?

## Rollback Mechanisms

Use **Helm rollback**.

## Example

```bash
helm rollback app 3
```

## Rollback Triggers

- Failed health checks
- Pod crash loops
- Canary deployment failure

---

# 5. How do you ensure pipeline reliability?

## Key Techniques

- Retry mechanisms
- Parallel jobs
- Artifact caching
- Pipeline timeout controls

These techniques ensure **stable and resilient CI/CD pipelines**.

---

# 6. How do you optimize build time?

## Techniques

- Dependency caching
- Docker layer caching
- Parallel pipeline jobs
- Incremental builds

These optimizations significantly **reduce CI pipeline execution time**.

---

# 7. Why do you use Artifactory instead of storing artifacts in GitHub?

## Benefits of JFrog Artifactory

- Central artifact management
- Immutable builds
- Version control
- Security scanning
- Supports multiple package types (Docker, Maven, NPM, etc.)

---

# 8. What security checks do you perform in the pipeline?

This follows a **DevSecOps approach**.

## Security Stages

- **SAST** → SonarQube
- **Dependency Scanning**
- **Container Scanning** → Trivy
- **Runtime Security** → Prisma Cloud

---

# 9. How do you scale this pipeline for multiple microservices?

## Typical Architecture

- Shared CI templates
- Reusable workflows
- Helm chart templates
- Centralized pipeline standards

This allows multiple microservices to reuse **standardized CI/CD pipelines**.

---

# 10. How do you handle database schema changes in CI/CD?

This question tests **stateful deployments**.

## Good Answer

We manage database schema changes using **versioned migration tools** such as:

- Flyway
- Liquibase

## Deployment Flow

```
Run Database Migration
        ↓
Deploy Application
```

## Best Practices

- Ensure **backward compatibility**
- Maintain a **rollback strategy**

---

# 11. How do you roll back if a database migration breaks production?

This is a common **advanced interview question**.

## Key Concept

Application rollback is easy, but **database rollback is complex**.

## Best Approach

Use **backward-compatible migrations** following the **Expand and Contract pattern**.

## Example

```
Step 1: Add new column
Step 2: Deploy new application
Step 3: Remove old column later
```

This ensures safe rollbacks without breaking the application.

---

# 12. What happens if two deployments run simultaneously?

This tests **pipeline concurrency control**.

## Good Answer

We configure **deployment locks and environment protection rules** in GitHub Actions to ensure that **only one deployment runs per environment at a time**.

## Best Practices

- Deployment concurrency control
- Deployment queueing
- Environment locks
- Protected environments
