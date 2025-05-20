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






   
