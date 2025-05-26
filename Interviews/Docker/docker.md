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
