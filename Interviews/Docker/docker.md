| Feature | Containers | Virtual Machines (VMs) |
| --- | --- | --- |
| Definition | Lightweight, isolated processes sharing OS | Full OS instances running on virtualized hardware |
| Boot Time | ⚡️ Fast (seconds) | 🐢 Slow (minutes) |
| OS Layer | Shares host OS kernel | Includes full guest OS |
| Resource Usage | Efficient, minimal overhead | Heavy, includes OS per VM |
| Isolation | Process-level isolation | Full machine-level isolation |
| Portability | Highly portable via images (Docker) | Less portable, OS/image-specific |
| Use Case | Microservices, CI/CD, cloud-native apps | Legacy apps, full-stack testing, VM-based infra |


| Type | Description | Use Case |
| --- | --- | --- |
| bridge | Default network for containers | Local communication between containers |
| host | Shares the host's network stack | Performance, no network isolation |
| none | No network (container is isolated) | Debugging, security |
| overlay | Multi-host communication via Docker Swarm | Distributed apps, Swarm/Kubernetes |
| macvlan | Container gets a unique IP on the LAN | Legacy systems, low-level networking |
| custom bridge | User-defined bridge network | Better DNS and isolation for apps |

| Aspect | Docker Image | Docker Container |
| --- | --- | --- |
| **Definition** | A read-only template with instructions to create a container | A running instance of a Docker image |
| **State** | Static (never changes) | Dynamic (changes as app runs) |
| **Usage** | Used to build containers | Used to run applications |
| **Persistence** | Cannot save runtime data | Can store logs, state, and data while running |
| **Example** | Like a class blueprint in code | Like an object created from that class |

**Caching in Docker**

Docker builds images layer by layer based on instructions in the Dockerfile.

Each instruction (like RUN, COPY, etc.) creates a new image layer, and Docker caches these layers to speed up future builds.

🧠 How it works:

Docker checks if it has already built a layer with the same instruction and context.

If nothing has changed, Docker reuses the cached layer.

If something changes, Docker invalidates that layer and all following layers

```Dockerfile
# Stage 1: Build the application
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Stage 2: Create minimal runtime image
FROM alpine:latest
WORKDIR /
COPY --from=builder /app/myapp /myapp

# Add a basic healthcheck (adjust as needed for your app)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["/myapp"]
```

| Directive | Purpose                     | Best Use Case                    | Notes                            |
| --------- | --------------------------- | -------------------------------- | -------------------------------- |
| `COPY`    | Copy local files into image | App code, config files, assets   | Preferred over `ADD` for copying |
| `ADD`     | Copy with extra features    | Extracting local tarballs        | Avoid for URL downloads          |
| `RUN`     | Execute shell commands      | Installing packages, build steps | Combine steps to reduce layers   |

```markdown
🔸 CMD — Default Arguments
Sets default command or arguments for the container.
Can be overridden at runtime (docker run).
If both ENTRYPOINT and CMD are present, CMD acts as arguments to ENTRYPOINT.

🔸 ENTRYPOINT — Fixed Executable
Sets the main command that always runs.
Even if you pass arguments with docker run, the ENTRYPOINT is not overridden.
Useful when you want your image to behave like a CLI tool or have consistent startup behavior.

Volume vs BindMounts
Docker volumes are managed storage used for persisting container data and are ideal for production.
Bind mounts, on the other hand, are host paths mounted directly into containers, great for development where I need to sync files quickly. I usually use volumes for stability and isolation, and bind mounts when I need tight integration with the host during development."
```

```markdown

Optimization

Use Multi-stage builds
Slim Base Images
Minimize layers
Combine commands: RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*
Reduce docker context
Use .dockerignore to exclude unnecessary files (e.g., node_modules, .git).
Pin image version: Avoid latest; use specific versions to improve reproducibility.

Resource Requets and limits --> set CPU and memory properly
Use Liveness and readiness probe
USe configmaps and secrets
USe Init containers--> check dependancies before main containers runs

Use Cluster Auto-scaler
Managed Node Groups
Enable HPA
Pod Topology Spread constraints

Use Spot instances
Righsize node based on metrics
```

```
Security

Base Image
vulnerability scanning
Remove secrets
Avoid Root
USER root
RUN apt-get update && apt-get install -y nginx
Pin version
Multi-stage builds
sigining and verification

security context
securityContext:
  runAsNonRoot: true
PDP
Secret mgmnt
Livness and Readiness Probe
Network Policies
Admission controllers
use IRSA --

Private cluster
encryption
EKS optimized AMI
patch and upgrade regulary

Ingress
WAF/shield
block egress traffic
DNS filtering
```
