```markdown
✅ So how can you access the EC2 instance if .pem is lost?
Connect using 🧩 Option 1: Use Systems Manager (SSM Session Manager)
💡 Option 2: Create a new key pair and replace the old one

Stop the EC2 instance (optional for safety)

Detach the root volume
Attach the volume to another EC2 instance where you have access
SSH into the second instance
Mount the attached volume, and edit ~/.ssh/authorized_keys of the original instance

sudo nano /mnt/home/ec2-user/.ssh/authorized_keys

Add your new public key from a newly created .pem
Detach the volume and re-attach to the original instance as /dev/xvda
Start the instance — now you can SSH using your new .pem
```

```markdown
clean up system logs
archive
set log rotation
```

```markdown
find log files older than 7 days

find /var/log/ -type f -mtime 7
```
