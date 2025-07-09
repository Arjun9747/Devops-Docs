```markdown
# File: import.tf

# Provider configuration
provider "aws" {
  region = "your-aws-region" # Replace with your AWS region
}

# Resource definition for the S3 bucket
resource "aws_s3_bucket" "state_bucket" {
  bucket = "deltastates3"
}

# Import block to import the existing S3 bucket
import {
  to = aws_s3_bucket.state_bucket
  id = "deltastates3"
}

# Workspace

Terraform workspaces allow you to use the same Terraform configuration to manage multiple environments or copies of infrastructure, like dev, staging, and prod.

Each workspace has its own state file (terraform.tfstate), so changes made in one workspace don’t affect the others.

terraform workspace new dev
terraform workspace new prod

terraform workspace list

terraform workspace select dev

# Pass as variable

variable "env" {
  type    = string
  default = terraform.workspace
}

# locals

locals in Terraform are used to define named values that you can reuse throughout your configuration.
They help reduce repetition and improve readability, maintainability, and logic abstraction

Locals are evaluated at plan time, and cannot change between applies.

Use for Tag Management

# dynamic blocks

Terraform's dynamic block is used to generate nested blocks programmatically based on loops or conditions—especially when the number or content of nested blocks isn't fixed.
Let’s say you want to define multiple ingress rules in a security group dynamically based on a list of CIDRs or ports.

Meta-arguments in Terraform are special arguments you can use in any resource block to change its behavior.
```

| Meta-Argument | Description                                         |
| ------------- | --------------------------------------------------- |
| `depends_on`  | Explicitly declare dependencies between resources   |
| `provider`    | Specify which provider configuration to use         |
| `count`       | Create multiple resource instances dynamically      |
| `for_each`    | Create multiple resources from a map or set         |
| `lifecycle`   | Control how Terraform creates, updates, and deletes |

```markdown

# Terraform Refresh

Terraform refreshes your working state by comparing the real infrastructure with what’s stored in your terraform.tfstate file.

✅ Refresh Happens When You:
Run terraform plan (automatically refreshes state)
Run terraform apply (also refreshes before making changes)
Explicitly run terraform refresh (prior to v1.6+, now removed)
Use terraform apply -refresh-only to only update state, not resources

# Provisoners

Provisioners in Terraform are used to execute scripts or commands on a local machine or on a remote resource after it's created. They're mainly used for bootstrapping, configuration, or custom post-deployment actions.
```

| Type            | Description                                          |
| --------------- | ---------------------------------------------------- |
| `local-exec`    | Runs a command **on your local machine**             |
| `remote-exec`   | Runs a command **on the provisioned remote machine** |
| `file`          | Copies files **from local to remote**                |
| `null_resource` | A meta-resource used **with provisioners**           |

```markdown

# Null Resources 

The null_resource is a meta-resource in Terraform that allows you to execute scripts or actions without managing actual infrastructure.

After creating an EC2 instance, run a script to register it in an external CMDB or monitoring tool.

 Trigger a rebuild script when the app version changes.

```

 # Modules

 | Module Type      | Description                                              |
| ---------------- | -------------------------------------------------------- |
| **Root Module**  | The main configuration directory where you run Terraform |
| **Child Module** | A reusable module called by the root or another module   |


```
| Feature         | Timing               | Scope             | Purpose                                |
| --------------- | -------------------- | ----------------- | -------------------------------------- |
| `precondition`  | Before apply         | Inside resource   | Validate inputs or expressions         |
| `postcondition` | After resource apply | Inside resource   | Ensure real resource state correctness |
| `check`         | After apply          | Outside resources | Validate overall system state          |


