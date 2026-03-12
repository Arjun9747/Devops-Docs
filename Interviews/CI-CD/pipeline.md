🔥 COPY FROM BELOW
Shell# CI/CD Pipeline Overview## End-to-End Flow DiagramShow more lines
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

```md
## Technology Stack

- **SCM:** GitHub  
- **CI/CD Engine:** GitHub Actions  
- **Artifact Repository:** JFrog Artifactory  
- **Containerization:** Docker  
- **Container Registry:** Artifactory Docker Registry  
- **Orchestration:** Kubernetes on Amazon EKS  
- **Package Manager:** Helm  
- **Code Quality:** SonarQube  
- **Container Security:** Trivy, Prisma Cloud  

Markdown# 1. Developer Commit Stage (Trigger)### What happens- Developer commits/pushes code to GitHub repo.- GitHub Actions workflow triggers on:  - `push`  - `pull_request`  - `tag`Show more lines
Markdown# 2. Dependency Install Stage### Example```bashmvn clean install -DskipTestsShow more lines
What happens

Dependencies downloaded
Libraries resolved
Build structured prepared

Best Practices

Use dependency caching
Use private repo (Artifactory)


```md
# 3. Static Code Analysis (SonarQube)

### Pipeline Command
```bash
mvn sonar:sonar

Checks Performed

Code smells
Bugs
Vulnerabilities
Duplications
Technical debt

Quality Gate Rules

Coverage < 80% → FAIL
Critical vulnerabilities > 0 → FAIL


```md
# 4. License & Dependency Checks

### Tools Used
- Maven dependency-check  
- SCA scanners  

### Checks
- License validation  
- CVE detection  

### Sample Risks
- Log4j  
- GPL-restricted software  
- Outdated versions  

### Best Practice
Fail on **HIGH** CVEs.  

Markdown# 5. Unit Testing Stage### Example```bashmvn testShow more lines
Frameworks

JUnit
Mockito

Metrics

Coverage
Pass/Fail summary

Best Practice
Coverage ≥ 80%.

```md
# 6. Build Artifact Stage

### Build Command
```bash
mvn package

Output
target/app.jar

Storage

Pushed to JFrog Artifactory

Benefits

Versioning
Central repository
Reproducible builds


```md
# 7. Docker Image Build

### Example Dockerfile
```Dockerfile
FROM openjdk:17-jdk
COPY target/app.jar app.jar
ENTRYPOINT ["java","-jar","/app.jar"]

Build Command
Shelldocker build -t app:1.4.0 .Show more lines

```md
# 8. Container Security Scanning

### Tools
- Trivy  
- Prisma Cloud  

### Example Scan
```bash
trivy image app:1.4.0

Checks For

OS vulnerabilities
Library CVEs
Secrets

Rule
Critical CVEs > 0 → FAIL

```md
# 9. Push Docker Image to Registry

### Target
- Artifactory Docker Registry  

### Tags
- app:1.4.0  
- app:latest  
- app:${GIT_SHA}  

### Best Practice
Use immutable tags.  

Markdown# 10. Integration Testing### Types- API tests  - DB integration tests  - Service connectivity tests  ### Tools- Postman  - REST Assured  - TestContainers  Show more lines
Markdown# 11. Helm Packaging### Chart StructureShow more lines
charts/
deployment.yaml
service.yaml
values.yaml

### Example Values
```yaml
image:
  repository: artifactory/app
  tag: "1.4.0"


```md
# 12. Deployment to EKS

### Command
```bash
helm upgrade --install app ./chart

Deploys

Deployment
Service
ConfigMaps
Secrets
HPA


```md
# 13. Deployment Strategies

## Blue-Green Deployment
- Blue = Current  
- Green = New  
- Traffic switch after validation  

## Canary Deployment
Gradual rollout:
- 10% → 50% → 100%  

Tools:
- Istio  
- Argo Rollouts  

Markdown# 14. Health Checks### Liveness ProbeEnsures container is alive.### Readiness ProbeEnsures pod ready for traffic.``Show more lines
Markdown# 15. Rollback Strategy### Trigger on:- Failed health checks  - High error rate  - Canary failure  ### Command```bashhelm rollback app 3Show more lines

```md
# 16. Monitoring & Observability

### Tools
- Grafana  
- Prometheus  
- CloudWatch  

### Metrics
- CPU  
- Memory  
- Latency  
- Error rate  
- Pod restarts  

### Alerts
- Error rate > 5%  
- Crash loops  
- High latency  
