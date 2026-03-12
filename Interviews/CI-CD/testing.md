CI CD Test 

# Java Testing in CI/CD (Gradle Based Applications)

For Java applications built using **Gradle**, CI/CD pipelines must run automated tests before packaging or deployment.

Typical testing tools used:

- JUnit
- Spring Boot Test
- Flyway (database migrations)
- Gradle Test Tasks

DevOps engineers should understand how these tests run inside CI/CD pipelines.

---

# Types of Tests in Java CI/CD Pipelines

| Test Type | Purpose | Example |
|----------|--------|--------|
| Unit Test | Tests a single method or class | Service logic |
| Integration Test | Tests interaction with real systems | Service + Database |
| End-to-End Test | Tests full application workflow | API + DB + UI |

---

# Example Java Application

Simple service example:

```java
public class CalculatorService {

    public int add(int a, int b) {
        return a + b;
    }

}

Unit Test Example

Unit tests validate individual logic without external systems.

Example using JUnit:

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorServiceTest {

    @Test
    void testAddition() {
        CalculatorService service = new CalculatorService();

        int result = service.add(2, 3);

        assertEquals(5, result);
    }
}

This test verifies:

Input: 2 + 3
Expected Output: 5
Integration Test Using Flyway (Database Migration)

Instead of mocking the database, many enterprise projects use Flyway to run database migrations during integration testing.

This ensures the test database schema matches production.

Example workflow:

Test Environment Start
        ↓
Flyway Migration Runs
        ↓
Database Schema Created
        ↓
Application Starts
        ↓
Integration Tests Execute
Example Flyway Migration Script

Location:

src/main/resources/db/migration

Example migration file:

V1__create_users_table.sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);
Integration Test Example (Spring Boot + Flyway)
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.beans.factory.annotation.Autowired;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class UserServiceIntegrationTest {

    @Autowired
    UserService userService;

    @Test
    void testUserCreation() {

        User user = new User();
        user.setName("Arjun");

        User savedUser = userService.save(user);

        assertNotNull(savedUser.getId());
    }
}

Test flow:

Flyway migration runs
      ↓
Database schema created
      ↓
User saved to DB
      ↓
Test validates result
Gradle Configuration for Flyway

Example build.gradle configuration:

plugins {
    id 'java'
    id 'org.flywaydb.flyway' version '9.22.0'
}

dependencies {

    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
    implementation 'org.flywaydb:flyway-core'

}

test {
    useJUnitPlatform()
}
Running Tests in CI/CD

Gradle command used in pipelines:

./gradlew test

Pipeline flow:

Build
   ↓
Unit Tests
   ↓
Start Test Database
   ↓
Flyway Migration
   ↓
Integration Tests
   ↓
Package
   ↓
Deploy
Example GitHub Actions Pipeline
name: Java CI

on: [push]

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

      - name: Run Tests
        run: ./gradlew test
Test Reports in CI/CD

Gradle generates reports at:

build/reports/tests/test/index.html

Example:

Total tests: 120
Passed: 118
Failed: 2
Skipped: 0

These reports are commonly published in CI tools like Jenkins or GitHub Actions.

4. How do DevOps engineers run database tests in CI/CD?

Typical approach:

Start a temporary database container

Run Flyway migrations

Execute integration tests

Destroy database after pipeline
