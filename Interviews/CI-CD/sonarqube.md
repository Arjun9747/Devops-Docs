SonarQube 

# SonarQube Integration for Java (Gradle) Applications

This section explains how to integrate **SonarQube** static code analysis into a CI/CD pipeline for Java applications built using **Gradle**.

SonarQube helps ensure **code quality, maintainability, and security** before code is deployed.

---

# What is SonarQube?

SonarQube is a **static code analysis platform** that scans source code to detect:

- Bugs
- Security vulnerabilities
- Code smells
- Code duplication
- Code coverage issues

It integrates with CI/CD pipelines to automatically analyze code during builds.

Typical usage:

Developer Push
↓
CI/CD Pipeline
↓
SonarQube Scan
↓
Quality Gate Evaluation
↓
Pass → Deployment continues
Fail → Pipeline stops

Developer Push
↓
CI/CD Pipeline
↓
SonarQube Scan
↓
Quality Gate Evaluation
↓
Pass → Deployment continues
Fail → Pipeline stops

Coverage: 85% ✔
Bugs: 0 ✔
Vulnerabilities: 0 ✔

Quality Gate: PASSED

If any rule fails:

Coverage: 65% ❌

Quality Gate: FAILED
Pipeline stops



---

# What is a Quality Profile?

A **Quality Profile** defines the **set of coding rules used to analyze the code**.

Each programming language has its own quality profile.


Example Java rules:

| Rule | Description |
|----|-------------|
| Avoid NullPointerException | Prevent null dereference |
| Avoid unused variables | Remove unused code |
| Avoid duplicate code blocks | Improve maintainability |

Example:

Java Project → Uses "Sonar Way" Quality Profile


Companies often create **custom quality profiles**.

Example enterprise rule:


Companies often create **custom quality profiles**.

Example enterprise rule:


Use of System.out.println
Hardcoded values
Poor logging practices

private static final Logger logger = LoggerFactory.getLogger(Service.class);

public void processData() {

    logger.info("Processing started");

}

Step 1 – Generate SonarQube Authentication Token

Login to SonarQube.

Navigate to:


User Profile → Security → Generate Token


Example token:


Token Name: ci-pipeline-token


SonarQube generates a token like:


sqp_3d92fksl23jflsdf


This token allows CI/CD pipelines to authenticate with SonarQube.

Step 2 – Store Token in CI/CD Secret Manager

Never store tokens in source code.

Example using GitHub Secrets:


Settings → Secrets → Actions


Create secret:


SONAR_TOKEN

Step 3 – Configure Gradle SonarQube Plugin

Add the Sonar plugin in build.gradle.

plugins {
    id "org.sonarqube" version "4.4.1.3373"
}

sonarqube {

    properties {

        property "sonar.projectKey", "java-demo-app"
        property "sonar.host.url", "http://sonarqube.company.internal"
        property "sonar.login", System.getenv("SONAR_TOKEN")

    }

}
Step 4 – Run SonarQube Scan

Gradle command:


./gradlew sonar


Pipeline flow:


Build
↓
Unit Tests
↓
SonarQube Scan
↓
Quality Gate Evaluation
↓
Deploy

Step 5 – GitHub Actions Integration

Example pipeline:

name: Java CI with SonarQube

on:
  push:
    branches: [ main ]

jobs:

  build:

    runs-on: ubuntu-latest

    steps:

      - uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 17

      - name: Build Project
        run: ./gradlew build

      - name: SonarQube Scan
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: ./gradlew sonar
Example SonarQube Metrics

After scanning, SonarQube reports metrics such as:

Metric	Example Result
Bugs	0
Vulnerabilities	0
Code Smells	12
Coverage	82%
Duplications	1.5%
CI/CD Enforcement

Enterprise pipelines enforce:


Sonar Scan
      ↓
Quality Gate Check
      ↓
PASS → Continue pipeline
FAIL → Stop deployment
