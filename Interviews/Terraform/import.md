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





```
| Feature         | Timing               | Scope             | Purpose                                |
| --------------- | -------------------- | ----------------- | -------------------------------------- |
| `precondition`  | Before apply         | Inside resource   | Validate inputs or expressions         |
| `postcondition` | After resource apply | Inside resource   | Ensure real resource state correctness |
| `check`         | After apply          | Outside resources | Validate overall system state          |

