# CI/CD Pipeline Overview

## End-to-End Flow Diagram

```
Developer
↓
GitHub Commit
↓
GitHub Actions Pipeline
↓
Code Analysis (SonarQube)
↓
Unit Tests
↓
Build Artifact
↓
Artifactory
↓
Docker Build
↓
Trivy / Prisma Security Scan
↓
Push Image
↓
Integration Tests
↓
Helm Deployment
↓
EKS Cluster
↓
Grafana Monitoring
↓
Automatic Rollback (if needed)
```

---

# Technology Stack

- **SCM:** GitHub  
- **CI/CD Engine:** GitHub Actions  
- **Artifact Repository:** JFrog Artifactory  
- **Containerization:** Docker  
- **Container Registry:** Artifactory Docker Registry  
- **Orchestration:** Kubernetes on Amazon EKS  
- **Package Manager:** Helm  
- **Code Quality:** SonarQube  
- **Container Security:** Trivy, Prisma Cloud  

---

# 1. Developer Commit Stage (Trigger)

## What Happens

- Developer commits or pushes code to GitHub repository.
- GitHub Actions workflow triggers on:

```
push
pull_request
tag
```

---

# 2. Dependency Install Stage

## Example

```bash
mvn clean install -DskipTests
```

## What Happens

- Dependencies downloaded
- Libraries resolved
- Build structure prepared

## Best Practices

- Use dependency caching
- Use private repository (Artifactory)

---

# 3. Static Code Analysis (SonarQube)

## Pipeline Command

```bash
mvn sonar:sonar
```

## Checks Performed

- Code smells
- Bugs
- Vulnerabilities
- Duplications
- Technical debt

## Quality Gate Rules

- Coverage < 80% → **FAIL**
- Critical vulnerabilities > 0 → **FAIL**

---

# 4. License & Dependency Checks

## Tools Used

- Maven dependency-check
- SCA scanners

## Checks

- License validation
- CVE detection

## Sample Risks

- Log4j
- GPL restricted software
- Outdated versions

## Best Practice

Fail on **HIGH CVEs**

---

# 5. Unit Testing Stage

## Example

```bash
mvn test
```

## Frameworks

- JUnit
- Mockito

## Metrics

- Test coverage
- Pass / Fail summary

## Best Practice

Coverage ≥ **80%**

---

# 6. Build Artifact Stage

## Build Command

```bash
mvn package
```

## Output

```
target/app.jar
```

## Storage

Artifact pushed to **JFrog Artifactory**

## Benefits

- Versioning
- Central repository
- Reproducible builds

---

# 7. Docker Image Build

## Example Dockerfile

```dockerfile
FROM openjdk:17-jdk
COPY target/app.jar app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```

## Build Command

```bash
docker build -t app:1.4.0 .
```

---

# 8. Container Security Scanning

## Tools

- Trivy
- Prisma Cloud

## Example Scan

```bash
trivy image app:1.4.0
```

## Checks For

- OS vulnerabilities
- Library CVEs
- Secrets

## Rule

Critical CVEs > 0 → **FAIL**

---

# 9. Push Docker Image to Registry

## Target

- Artifactory Docker Registry

## Tags

```
app:1.4.0
app:latest
app:${GIT_SHA}
```

## Best Practice

Use **immutable tags**

---

# 10. Integration Testing

## Types

- API tests
- Database integration tests
- Service connectivity tests

## Tools

- Postman
- REST Assured
- TestContainers

---

# 11. Helm Packaging

## Chart Structure

```
charts/
  deployment.yaml
  service.yaml
  values.yaml
```

## Example Values

```yaml
image:
  repository: artifactory/app
  tag: "1.4.0"
```

---

# 12. Deployment to EKS

## Command

```bash
helm upgrade --install app ./chart
```

## Deploys

- Deployment
- Service
- ConfigMaps
- Secrets
- HPA

---

# 13. Deployment Strategies

## Blue-Green Deployment

- Blue = Current environment
- Green = New environment
- Traffic switched after validation

## Canary Deployment

Gradual rollout:

```
10% → 50% → 100%
```

## Tools

- Istio
- Argo Rollouts

---

# 14. Health Checks

## Liveness Probe

Ensures container is **alive**

## Readiness Probe

Ensures pod is **ready to receive traffic**

---

# 15. Rollback Strategy

## Trigger On

- Failed health checks
- High error rate
- Canary failure

## Command

```bash
helm rollback app 3
```

---

# 16. Monitoring & Observability

## Tools

- Grafana
- Prometheus
- CloudWatch

## Metrics

- CPU
- Memory
- Latency
- Error rate
- Pod restarts

## Alerts

- Error rate > 5%
- Crash loops
- High latency
