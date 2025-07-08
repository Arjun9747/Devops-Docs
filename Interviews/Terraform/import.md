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
```
