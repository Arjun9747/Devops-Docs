
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

<img width="422" alt="image" src="https://github.com/user-attachments/assets/0398b00a-387a-48a9-bad3-c4028213488e" />

it will list 
Default Route
Pod network
docker
static host route enx0 with dhcp
vpc subnet route


