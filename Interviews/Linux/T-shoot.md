
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




