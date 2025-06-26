

**Check slow connected networks**

Monitor bandwidth 
$iftop -i 

$ uptime
13:35:03 up 103 days, 8 min, 5 users, load average: 2.03, 20.17, 15.09

The three numbers after load average—2.03, 20.17, and 15.09—represent the 1-, 5-, and 15-minute load averages on the machine

A single-CPU system with a load average of 1 means the single CPU is under constant load. If that single-CPU system has a load average of 4, there is four times the load on the system than it can handle, so three out of four processes are waiting for resources.

$top
```shell
top - 14:08:25 up 38 days,  8:02,  1 user,  load average: 1.70, 1.77, 1.68
Tasks: 107 total,   3 running, 104 sleeping,   0 stopped,   0 zombie
Cpu(s): 11.4%us, 29.6%sy, 0.0%ni, 58.3%id,  .7%wa, 0.0%hi, 0.0%si, 0.0%st
Mem:   1024176k total,   997408k used,    26768k free,    85520k buffers
Swap:  1004052k total,     4360k used,   999692k free,   286040k cached

  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM      TIME+  COMMAND
 9463 mysql     16   0  686m 111m 3328 S   53  5.5  569:17.64  mysqld
18749 nagios    16   0  140m 134m 1868 S   12  6.6    1345:01  nagios2db_status
24636 nagios    17   0 34660  10m  712 S    8  0.5    1195:15  nagios
22442 nagios    24   0  6048 2024 1452 S    8  0.1    0:00.04  check_time.pl
```

$iostat 
```shell
$ sudo iostat
Linux 2.6.24-19-server (hostname)   01/31/2009

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           5.73    0.07    2.03    0.53    0.00   91.64
Device:            tps   Blk_read/s   Blk_wrtn/s   Blk_read   Blk_wrtn
sda               9.82       417.96        27.53   30227262    1990625
sda1              6.55       219.10         7.12   15845129     515216
sda2              0.04         0.74         3.31      53506     239328
sda3              3.24       198.12        17.09   14328323    1236081
```

$iotop
```shell
$ sudo iotop
Total DISK READ: 189.52 K/s | Total DISK WRITE: 0.00 B/s

  TID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN     IO>     COMMAND

 8169  be/4  root    189.52 K/s    0.00 B/s  0.00 %  0.00 %     rsync --server --se

 4243  be/4  kyle      0.00 B/s    3.79 K/s  0.00 %  0.00 %     cli /usr/lib/gnome-

 4244  be/4  kyle      0.00 B/s    3.79 K/s  0.00 %  0.00 %     cli /usr/lib/gnome-

    1  be/4  root      0.00 B/s    0.00 B/s  0.00 %  0.00 %     init
```

tps--> transfer per second
blk-> number of blocks 
blk_wrtn--> block written 
When you have a system under heavy I/O load, the first step is to look at each of the partitions and identify which partition is getting the heaviest I/O load

sar -u 2 5
Reports CPU usage every 2 seconds for 5 samples

| Flag                          | Description                        |
| ----------------------------- | ---------------------------------- |
| `-u`                          | CPU usage                          |
| `-P ALL`                      | CPU usage for each core            |
| `-r`                          | Memory usage                       |
| `-B`                          | Paging and swapping stats          |
| `-b`                          | I/O transfer rates                 |
| `-d`                          | Block device usage                 |
| `-n DEV`                      | Network stats per interface        |
| `-n TCP,UDP`                  | Socket stats                       |
| `-q`                          | Run queue and load average         |
| `-W`                          | Swapping stats                     |
| `-A`                          | All stats (CPU, memory, I/O, etc.) |


**Disk Issues**
The df command lets you know how much space is used by each file system

Out of Inodes 
```shell
$ df -i
Filesystem Inodes IUsed IFree IUse% Mounted on
/dev/sda 520192 17539 502653 4% /
```
the file system is read only
```shell
$ sudo mount -o remount,rw /home
```
Repair corrupt file system
# fsck -y -C /dev/sda5

**Server A can't talk to Server B**
**Server is up or not**

Server is connected to network 
$sudo ethtool eth0 
to verify the link is up
Link detected: yes
for EC2 
$ ip a # list all interfaces
2: enX0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc fq_codel state UP group default qlen 1000
other than that it will have
flannel
docker 
cni0
veth1 and veth4
lo --> loopback 

**Once the server is connected, check the route**

ip addr show

<img width="422" alt="image" src="https://github.com/user-attachments/assets/0398b00a-387a-48a9-bad3-c4028213488e" />

it will list 
Default Route
Pod network
docker
static host route enx0 with dhcp
vpc subnet route

**Check DNS**

nslookup or dig 
check nameserver configuration 

check traceroute 
once you see the "******" means the problem is in your network and ❌ No response was received from that hop within the timeout period.

check the port is open or not using Telnet 

$nmap -p 80 10.1.2.3
to detect firewalls 

Test for Listening ports
$netstat -lnp | grep 80

Check firewalls 
$/sbin/iptables -L 

**tcp dumps**
$ sudo tcpdump -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 96 bytes
19:01:51.133159 IP 208.115.111.75.60004 > 64.142.56.172.80: Flags [F.], seq 753858968, ack 1834304357, win 272, options [nop,nop,TS val 99314435 ecr 1766147273], length 0
19:01:51.133317 IP 64.142.56.172.80 > 208.115.111.75.60004: Flags [F.], seq 1, ack 1, win 54, options [nop,nop,TS val 1766147276 ecr 99314435], length 0

| Field                  | Meaning                                                      |
| ---------------------- | ------------------------------------------------------------ |
| `19:01:51.133159`      | Timestamp when the packet was captured                       |
| `IP`                   | IPv4 traffic                                                 |
| `208.115.111.75.60004` | **Source IP and source port** (60004)                        |
| `>`                    | Packet is **going to**                                       |
| `64.142.56.172.80`     | **Destination IP and port** (port 80 = HTTP)                 |
| `Flags [F.]`           | TCP flags: `F` = FIN (finish), `.` = ACK (acknowledgment)    |
| `seq 753858968`        | TCP sequence number (last data byte sent + 1)                |
| `ack 1834304357`       | TCP acknowledgment number (next expected seq from peer)      |
| `win 272`              | TCP window size (how much more data the receiver can accept) |
| `options [...]`        | TCP timestamp options (used for RTT estimation, PAWS)        |
| `length 0`             | No payload (this is a TCP control packet only)               |

Filter tcpdump output 
$ sudo tcpdump -n host web1

$ sudo tcpdump -n not host web1 # except host1

**DNS issue**

```shell
$ dig web1.example.net
; <<>> DiG 9.7.0-P1 <<>> example.net
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30750
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 2

;; QUESTION SECTION:
;web1.example.net.             IN      A

;; ANSWER SECTION:
web1.example.net.      300     IN      A       10.1.2.5

;; AUTHORITY SECTION:
example.net.           300     IN      NS      ns2.example.net.
example.net.           300     IN      NS      ns1.example.net.

;; ADDITIONAL SECTION:
ns1.example.net.       300     IN      A       10.1.1.3
ns2.example.net.       300     IN      A       10.1.1.4

;; Query time: 2 msec
;; SERVER: 192.168.0.1#53(192.168.0.1)
;; WHEN: Mon Mar 19 20:48:27 2012
;; MSG SIZE  rcvd: 118
```

Question section --> we asked for a A record and we got 10.1.2.5 
Authority Secton is Nameserver section 
Query details 

To trace dns query
$ dig web1.example.net +trace

Website accesible via Curl but not http

✅ 1. DNS resolution difference
curl might resolve a different IP (if using a different DNS resolver).

✅ 2. SSL/TLS Issues
curl may succeed with -k (ignores cert errors), but browsers block invalid/self-signed certs.

✅ 3. Redirects not handled
curl doesn't follow redirects unless you use -L.

A website may redirect HTTP → HTTPS → another domain.

curl -L http://example.com

✅ 4. Firewall/Proxy/Network filtering
A firewall may allow CLI tools (curl over port 443) but block GUI-based apps or certain user-agents.
Also, proxy settings in a browser may differ from the terminal.

✅ 6. JavaScript-heavy content
If the site relies on JavaScript to render or fetch content, curl will succeed in getting the raw HTML, but your browser may fail due to JS errors or CSP

✅ 7. Cookies/session issues
A browser might send stale cookies or be in an invalid session state, causing issues that curl doesn't face.

Use curl -v to see headers and TLS errors.
