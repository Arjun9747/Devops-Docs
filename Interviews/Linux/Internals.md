*When we run `rm -rf` command, what happens in the backend*

**Traverses the Filesystem Tree:**

The rm command recursively walks through all subdirectories and files if -r is used.

It uses system calls like opendir(), readdir() to list directory contents.

**Unlinks Files and Directories:**

For each file, rm calls the unlink() system call:

This removes the directory entry (name) for the file.

**Decrements Inode Reference Count:**

Each file has an inode (data structure that stores file metadata).

The file's reference count is reduced.

When it reaches zero and no process is using it, the file data blocks are released back to the filesystem.

**Removes Directories:**

Uses the rmdir() or unlinkat() system call for directories.

Only empty directories can be deleted using rmdir(), but rm -r ensures subcontents are deleted first.

*While booting, the kernel is unable to load the file system. How will you troubleshoot*

**For AWS EC2 Instances**

Use EC2 Serial Console (for Amazon Linux 2 and Ubuntu).

Check System Logs from AWS Console.

Detach root volume → Attach to another instance → Mount → Fix.

| Check              | Command/Method                           |
| ------------------ | ---------------------------------------- |
| Boot Logs          | Watch boot screen / serial console       |
| fstab              | `cat /mnt/root/etc/fstab`                |
| Disk health        | `fsck /dev/sdX`                          |
| Initramfs contents | `lsinitrd`                               |
| Rebuild initramfs  | `dracut --force` / `update-initramfs -u` |
| Drivers            | Verify required drivers in kernel/initrd |

Initramfs (short for "initial RAM file system") is a temporary root file system that is loaded into memory during the Linux boot process. It's a crucial component of the boot process, especially in modern Linux systems.

Provides a temporary root file system

Loads necessary modules

Mounts the root file system

Handles early boot tasks

**How does Initramfs work?**

1. Boot loader loads the kernel and Initramfs:
2. Kernel initializes
3. Initramfs is mounted:
4. Initramfs loads necessary modules
5. Root file system is mounted
6. System transitions to real root file system


**Shared the screenshot of output of `top` command and asked me to explain the terms that I understand.**

![image](https://github.com/user-attachments/assets/621601cb-759a-441b-be65-e6a7fe0af74e)


```bash
top - 12:45:27 up 5 days,  4:32,  2 users,  load average: 0.10, 0.08, 0.12
```
* 12:45:27 → Current time.
* up 5 days, 4:32 → System uptime (since last reboot).
* 2 users → Number of users currently logged in.
* load average: 0.10, 0.08, 0.12 → CPU load over 1, 5, and 15 minutes.

  ```arundio
  Tasks: 120 total, 1 running, 119 sleeping, 0 stopped, 0 zombie
```
* Total: Number of processes.
* Running: Actively using CPU.
* Sleeping: Idle, waiting for an event.
* Stopped: Manually stopped.
* Zombie: Dead processes not yet cleaned up.

```bash
%Cpu(s):  5.2 us,  1.0 sy,  0.0 ni, 93.0 id,  0.6 wa,  0.0 hi,  0.2 si,  0.0 st
```

* us (user): Time spent on user processes.
* sy (system): Time on kernel processes.
* ni (nice): Time on low-priority user processes.
* id (idle): Idle time.
* wa (wait): Time waiting on I/O.
* hi/si (hardware/software interrupts): Time handling interrupts.
* st (steal time): Time stolen by hypervisor in a virtual environment.


```bash
MiB Mem :  7984.4 total,  1200.0 free,  3450.0 used,  3334.4 buff/cache
```
* total: Total physical memory.
* free: Unused memory.
* used: In use (not including cache).
* buff/cache: Memory used for disk cache and buffers.

```bash
MiB Swap: 2048.0 total, 2048.0 free, 0.0 used, 600.0 avail Mem
```
* Shows swap space stats.
* If swap used is high → possible memory pressure.

```bash
PID USER  PR  NI  VIRT  RES  SHR  S  %CPU  %MEM  TIME+  COMMAND
```
* PID: Process ID.
* USER: Owner.
* PR/NI: Priority/Nice value.
* VIRT/RES/SHR: Virtual, resident, shared memory
* S: Process state (R = running, S = sleeping, Z = zombie).
* %CPU: CPU usage.
* %MEM: Memory usage.
* TIME+: Total CPU time used.
* COMMAND: Command name or path.

1. Top Header: System Overview
2.  Tasks Section
3.  CPU Usage
4.  Memory Usage
5.  Swap Usage
6.  Process List

**iostat**

![image](https://github.com/user-attachments/assets/0783589b-5ec3-4104-8ace-3f523e7437b1)

CPU statistics ,I/O statistics for devices and partitions

 1. CPU Utilization Section

```perl
avg-cpu:  %user  %nice %system %iowait  %steal  %idle
           5.10   0.00    1.23    2.01     0.00   91.66
```
* %user: Time CPU spends on user processes.
* %system: Time on kernel processes.
* %iowait: Time spent waiting for I/O. {🚨 If this is high (> 10–15%), it may indicate disk I/O bottlenecks}
* %idle: Idle time — should be high on healthy systems.

   2. Device Utilization Section

 
  Device            tps    kB_read/s  kB_wrtn/s  kB_read  kB_wrtn
  nvme0n1           55.0     1000.5     2048.3    504320   1034240


* Device: Disk or partition.
* tps (transfers per second): Number of I/O requests per second.
* kB_read/s / kB_wrtn/s: Throughput (in KB) per second.
* kB_read / kB_wrtn: Total data read/written (since boot or since stats reset)


**Your disk space is full. How will you boot into the OS?**

Boot into Rescue or Recovery Mode

On cloud (AWS EC2 / GCP / Azure):

Detach the root volume.

Attach it to another instance as a secondary volume.

Mount it and clean up space.

2. Mount the Root Filesystem (If Needed)
3. Find Large Files

```bash
du -h --max-depth=1 / | sort -hr | head -20
```
4. Clean up disk space

```bash
journalctl --vacuum-time=7d
rm -rf /var/log/*.gz /var/log/*.[0-9]
```

5. Set up logrotate.

Monitor with cron + alert if disk usage > threshold.

Move logs to external storage (e.g., S3).

Logrotate is a utility that helps manage log files by rotating, compressing, and removing them

🔁 Swap Memory

Definition: Swap is a portion of the hard drive used as virtual memory when RAM is full.

Purpose: Helps prevent out-of-memory (OOM) errors by temporarily moving inactive pages from RAM to disk.

Downside: Slower than RAM, can cause performance issues if overused.

📄 Paging

Definition: Paging is a memory management scheme that breaks physical memory into fixed-size blocks (pages).

Use Case: Allows the OS to use non-contiguous memory and supports virtual memory (including swap).

Mechanism: Pages can be swapped in/out of RAM and disk (swap).

🧟 Zombie Process

Definition: A process that has completed execution but still has an entry in the process table.

Why?: The parent process hasn't read its exit status using wait().

```bash
ps aux | grep 'Z'
```

🧒 Orphan Process

Definition: A process whose parent has exited before the child process.

Handling: Automatically adopted by init or systemd (PID 1).

No issue: Orphans are cleaned up properly unlike zombies.

📞 System Calls

Definition: System calls are the interface between a user-space application and the Linux kernel.

Purpose: To request kernel services like file operations, memory management, process control, etc.

Examples:

open(), read(), write(), fork(), exec(), exit()

⚙️ How System Calls Are Initiated

User process invokes a standard library function (e.g., read()).

Library wrapper triggers a software interrupt or special CPU instruction (e.g., int 0x80, syscall).

CPU switches to kernel mode, and jumps to the kernel’s system call handler.

The kernel executes the requested operation.

Control is returned to the user space with the result or an error code.

*Kernel Panic Error*

A kernel panic occurs when the Linux kernel detects a fatal error from which it cannot safely recover — often due to hardware failure, corrupt drivers, bad kernel updates, or critical file system issues.

Check Boot Logs

```bash
cat /var/log/kern.log
cat /var/log/syslog
journalctl -k -b -1   # Show kernel logs from last boot
```

 Use Recovery Mode / Rescue Mode

 Reboot the system.

In GRUB, select Advanced Options → choose a previous kernel version or recovery mode.

Use root shell to investigate.

🛠️ 4. Common Kernel Panic Causes & Fixes


Boot into recovery and run:

```bash
fsck /dev/sdX
```
 Invalid initramfs or grub config

 ```bash
sudo update-initramfs -u
```

| Task                 | Command                 |
| -------------------- | ----------------------- |
| Filesystem Check     | `fsck /dev/sdX`         |
| Regenerate Initramfs | `update-initramfs -u`   |
| Check RAM            | `memtest86+`            |
| View Last Boot Logs  | `journalctl -k -b -1`   |
| Boot Older Kernel    | Select via GRUB         |
| View GRUB config     | `cat /etc/default/grub` |

**inode**

An inode stores all the information about a file except its name and actual data. Specifically, it includes:

File type (regular file, directory, symlink, etc.)

Permissions (read/write/execute for owner, group, others)

Owner (UID) and group (GID)

File size

Timestamps:

ctime: inode change time

mtime: last modification time

atime: last access time

Link count (number of hard links)

Pointers to data blocks where the file's content is stored

Imagine you create a file:

echo "Hello" > myfile.txt

The system assigns an inode number (e.g., 12345) to the file.

myfile.txt is just an entry in the directory that points to inode 12345.

inode 12345 stores all metadata and block addresses where "Hello" is saved.

ls -i myfile.txt  --> To view 

1. Inodes and File System Performance
Access Speed:
When you access a file, the system looks up the directory entry (file name) to get the inode number, then uses the inode to find the file data blocks. This two-step lookup is efficient and allows fast metadata access without scanning file contents.

Metadata Operations:
Operations like checking permissions, timestamps, or ownership only involve reading the inode — no need to read the actual file data, which improves speed.

File System Limits:
The total number of inodes is fixed at filesystem creation. If you run out of inodes, you cannot create new files even if disk space is available, which can degrade performance or cause errors.

Fragmentation:
Because inode data is separate from file data, fragmentation affects data blocks but not inode storage. However, if metadata operations involve many files, inode locality can impact performance (e.g., many small files in one directory).

2. Inodes and File Deletion Behavior
Deleting a File:
When you delete (unlink) a file, the system removes the directory entry linking the file name to the inode and decreases the inode's link count.

When is the inode freed?
The inode (and its data blocks) is freed only when the link count reaches zero and no process is holding the file open.

Open File Handles:
Even after deletion, if a process still has the file open, the inode remains allocated until the file is closed. This is why deleted files can sometimes still be read by running processes.

3. Inodes and File System Corruption
Corrupted Inodes:
Damage to inode structures can cause files to become inaccessible or show incorrect metadata (wrong size, permissions, timestamps).

File System Check (fsck):
Tools like fsck scan and repair corrupted inodes, often recovering files or marking bad inodes so the system doesn’t use them.

Lost+Found:
Orphaned inodes (files without directory entries) found during checks may be moved to a lost+found directory for manual recovery.


1. How do inodes relate to file system performance?
Inodes store all the file metadata (permissions, timestamps, ownership) separately from file names and content, allowing fast access to file information without reading the data itself.

File operations that involve metadata (like permission checks or timestamp reads) are quick because the system accesses only the inode.

The total number of inodes is fixed at filesystem creation, so running out of inodes (even if disk space is available) prevents new files from being created and impacts system functionality.

Inode locality and how they are stored can affect performance, especially in directories with many files, since the system must read multiple inodes during directory traversal or metadata operations.














   









  

