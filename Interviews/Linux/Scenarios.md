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


| Cause               | Symptom                         | Diagnostic                      |
| ------------------- | ------------------------------- | ------------------------------- |
| High CPU usage      | High load, `%us` or `%sy` high  | `top`, `perf top`, `ps`         |
| Disk I/O wait       | `%wa` high, `D` state processes | `iotop`, `iostat`, `dmesg`      |
| Memory pressure     | Swap usage, OOM kills           | `free -h`, `dmesg`, `vmstat`    |
| Network issues      | Slow responses, timeouts        | `netstat`, `ping`, `tcpdump`    |
| NFS or EBS problems | Hanging processes               | `dmesg`, `strace`, `mount` info |

```markdown
1. Basic System Checks (User Space)
Start from user-level tools to get an overview:

top / htop: Check CPU, memory, load average, process states.

uptime: Gives you load averages (1, 5, 15 minutes).

vmstat 1: See CPU, I/O, memory, swap every second.

iostat -xz 1: Shows disk I/O performance.

free -h: Check memory and swap usage.

df -h: Disk space usage.

dmesg | tail: Look for recent kernel errors.

journalctl -p err -b: Boot errors from the journal.

2. Understand Load Average
Load average > number of cores = system is busy
Check with nproc or lscpu how many CPUs are available.

High load can come from:

CPU-bound processes

I/O wait (disk/network bottlenecks)

Blocked processes

3. Identify CPU Bottlenecks
top or htop
Look for %us (user), %sy (system), %wa (I/O wait), %id (idle)

If %wa is high → Disk I/O problem

If %sy is high → Kernel or system call bottlenecks

perf top
Shows which kernel functions consume CPU (need perf installed)

4. Check for Disk I/O Issues
iostat -xz 1
await: High value → high latency

%util: Close to 100% → disk is fully used

tps and kB_read/s, kB_wrtn/s show load pattern

iotop
Real-time I/O usage by processes

blktrace, bpftrace (advanced)
For kernel-level block I/O tracing

5. Check for Memory/Swap Issues
free -h
Check available memory and swap usage

vmstat 1
Look for high si (swap in) / so (swap out)

High cs (context switches) could indicate thrashing

sar -B
Page faults and swapping metrics

cat /proc/meminfo
Deeper memory stats from kernel

6. Investigate Process Scheduling
top → Shift+H
Show threads; check if threads are blocked or consuming CPU

ps -eo pid,ppid,stat,ni,pri,cmd --sort=-pri
See process priorities

sched_debug (kernel scheduler)
bash
Copy
Edit
cat /proc/sched_debug
See CPU run queues, scheduling delays

7. Check for Blocked Processes (D State)
ps aux | awk '$8 ~ /D/ { print }'
D state = uninterruptible sleep, often due to I/O

If many processes are stuck in D, check:

Disk failure (dmesg)

NFS/network mounts

File system locks

8. Network Latency / Bottleneck
ss -tuan
See open sockets

netstat -s
TCP errors, retransmissions

sar -n DEV 1 or ifstat
Monitor NIC throughput

ping, traceroute, mtr
Latency and path issues

9. Advanced Kernel Tools
ftrace, bpftrace, ebpf, systemtap
Trace kernel functions, syscalls, events
```









   
