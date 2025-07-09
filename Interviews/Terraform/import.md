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



```
| Feature         | Timing               | Scope             | Purpose                                |
| --------------- | -------------------- | ----------------- | -------------------------------------- |
| `precondition`  | Before apply         | Inside resource   | Validate inputs or expressions         |
| `postcondition` | After resource apply | Inside resource   | Ensure real resource state correctness |
| `check`         | After apply          | Outside resources | Validate overall system state          |

