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


