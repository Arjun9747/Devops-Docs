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



   









  

