Terraform configuration 

Instead of using static AWS access keys, we configure OIDC authentication between GitHub Actions and Amazon Web Services so that workflows assume an IAM role and receive temporary credentials.

Architecture Overview
Developer Pushes Code to GitHub
        │
        ▼
GitHub Actions Pipeline
        │
        │ (OIDC Token)
        ▼
AWS IAM OIDC Provider
        │
        ▼
IAM Role for Terraform
        │
        ▼
Temporary AWS Credentials (STS)
        │
        ▼
Terraform Init → Plan → Apply
        │
        ▼
AWS Infrastructure Provisioned
Prerequisites

Before configuring the pipeline ensure the following:

AWS account

IAM permissions to create roles

Terraform code repository in GitHub

S3 bucket for Terraform state

DynamoDB table for Terraform state locking

Step 1 – Configure OIDC Provider in AWS

In AWS Identity and Access Management create an OIDC provider.

IAM → Identity Providers → Add Provider

Provider configuration:

Provider Type: OpenID Connect

Provider URL:
https://token.actions.githubusercontent.com

Audience:
sts.amazonaws.com

This allows GitHub workflows to authenticate with AWS.

Step 2 – Create IAM Role for GitHub Terraform Pipeline

Create an IAM role that GitHub can assume.

Example trust policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:ORG_NAME/REPO_NAME:*"
        }
      }
    }
  ]
}

Attach required policies such as:

AmazonEC2FullAccess
AmazonVPCFullAccess
AmazonS3FullAccess

For production environments, apply least privilege policies.

Step 3 – Configure Terraform Remote Backend

Terraform state must be stored remotely to support team collaboration.

Example backend configuration:

terraform {
  backend "s3" {
    bucket         = "terraform-state-prod"
    key            = "network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
  }
}

Purpose of components:

Component	Purpose
S3 Bucket	Stores Terraform state
DynamoDB Table	State locking
Backend Config	Prevents concurrent changes
Step 4 – GitHub Actions Workflow for Terraform

Create a workflow file:

.github/workflows/terraform.yml

Example pipeline:

name: Terraform Deployment

on:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  terraform:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Configure AWS Credentials using OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::<ACCOUNT_ID>:role/terraform-github-role
          aws-region: us-east-1

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        run: terraform plan

      - name: Terraform Apply
        run: terraform apply -auto-approve

Key permission required:

id-token: write

This allows GitHub to generate an OIDC token for AWS authentication.

Step 5 – Example Terraform Infrastructure

Example Terraform code to create an EC2 instance.

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web_server" {
  ami           = "ami-123456"
  instance_type = "t3.micro"

  tags = {
    Name = "terraform-demo-instance"
  }
}

Pipeline execution will perform:

terraform init
terraform plan
terraform apply
Step 6 – Handling Secrets

Application secrets can be stored in GitHub Secrets.

Example:

DB_PASSWORD
API_KEY

Usage in pipeline:

env:
  TF_VAR_db_password: ${{ secrets.DB_PASSWORD }}

Note:

AWS credentials are not stored in GitHub when using OIDC.

Security Best Practices

Recommended security practices:

Use OIDC authentication instead of static AWS keys

Restrict IAM role access to specific repositories

Restrict access to specific branches (e.g., main)

Apply least privilege IAM policies

Use remote Terraform state storage

Enable state locking with DynamoDB

Example repository restriction:

repo:ORG_NAME/REPO_NAME:ref:refs/heads/main
CI/CD Pipeline Stages

Typical Terraform pipeline flow:

Code Push
   │
   ▼
Terraform Format Check
   │
   ▼
Terraform Validate
   │
   ▼
Terraform Plan
   │
   ▼
Manual Approval
   │
   ▼
Terraform Apply

Many enterprise pipelines also include:

Security scanning

Infrastructure policy checks

Drift detection

Cost analysis
