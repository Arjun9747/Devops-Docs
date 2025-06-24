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

**Terraform**

```markdown
What is the difference between for_each and for in Terraform?

for_each
Used to create multiple resources or modules dynamically from a map or set of strings.
📦 Used with:
Resources
Modules
Dynamic blocks

```hcl
resource "aws_security_group_rule" "egress" {
  for_each = {
    http  = 80
    https = 443
  }

  type        = "egress"
  from_port   = each.value
  to_port     = each.value
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}
```

for_
Used inside expressions (like variables, locals, outputs) to transform or generate lists or maps.
```hcl
locals {
  ports = [80, 443]
  port_map = { for p in local.ports : "port_${p}" => p }
}
```

```markdown
A module in Terraform is simply a container for multiple resources that are used together.
It’s like a reusable block of infrastructure code.
📁 A module typically consists of:
main.tf – resources
variables.tf – inputs
outputs.tf – outputs

Reusebale, consistency, seperation of functions.
```

**Docker**

```markdown
ERROR
docker ps -a
check the exit code
| Exit Code | Meaning                                        |
| --------- | ---------------------------------------------- |
| `0`       | Process completed successfully (nothing wrong) |
| `1`       | General error or app crash                     |
| `137`     | Killed (e.g., out of memory)                   |
| `139`     | Segmentation fault                             |

View container logs
docker logs <container_id>

check entrypoint or CMD
docker inspect <container_id> | grep -i entrypoint

EXPOSE --> command
EXPOSE does NOT publish the port.
It only serves as documentation and metadata inside the image.

To actually allow traffic from your host to the container:

docker run -p 3000:3000 my-app
```




