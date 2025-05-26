**What are the RCA rule along with SRE 4 rules that you will apply while you create the alerts for your application**
1. Latency – How long does it take to serve a request?
2. Traffic – How much demand is your service receiving?
3. Errors – What fraction of requests are failing?
4. Saturation – How full is your system (CPU, memory, disk, etc.)?

**Port Mapping in Docker**

Port mapping in Docker is the mechanism that allows external access to services running inside Docker containers. It maps a port on the host machine to a port on the container, enabling communication between the outside world and the containerized application.

```bash
docker run -p <host_port>:<container_port> <image>
docker run -p 8080:80 nginx
```

**Workflow**

1. Docker sets up iptables rules or uses the userland proxy to forward traffic from the host port to the container port.
2. The container port is the one exposed by the application inside the container.
3. The host port is what users (or other services) use to access the container from outside.


**Paging and Segmentation**

Paging divides both logical memory (used by programs) and physical memory (RAM) into fixed-size blocks:

Pages: Fixed-size blocks of logical memory.

Frames: Fixed-size blocks of physical memory.

Segmentation divides memory based on logical divisions like functions, arrays, stacks, etc. Each segment has a variable length and a name/id.

Most modern systems (like x86) use a combination called segmented paging, where each segment is further divided into pages.

**Deadlock**

A deadlock is a situation where two or more processes are waiting for each other indefinitely to release resources, and none of them can proceed.

🛠️ How to Handle It:
Deadlock Prevention – Avoid one of the Coffman conditions.

Deadlock Avoidance – Use algorithms like Banker's Algorithm.

Deadlock Detection and Recovery – Periodically check for deadlocks and terminate/restart processes.

**Semaphores**
A semaphore is a synchronization primitive used to manage access to a shared resource in concurrent systems.









   
