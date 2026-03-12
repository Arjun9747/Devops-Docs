OIDC configure in GitHub and AWS 

Configuring OIDC authentication between GitHub Actions and AWS is the recommended secure approach instead of storing long-lived AWS access keys in CI/CD pipelines.

The idea is:

➡ GitHub issues a temporary OIDC token
➡ AWS IAM trusts GitHub as an identity provider
➡ GitHub assumes an IAM Role
➡ Temporary AWS credentials are issued

This avoids storing static credentials in GitHub Actions while securely accessing Amazon Web Services.

1️⃣ High Level Architecture
GitHub Actions Workflow
        │
        │ (OIDC Token)
        ▼
GitHub OIDC Provider
        │
        ▼
AWS IAM Identity Provider
        │
        ▼
IAM Role with Trust Policy
        │
        ▼
Temporary AWS Credentials
        │
        ▼
Deploy to AWS (EKS, S3, Terraform, etc)
2️⃣ Step 1 — Create OIDC Provider in AWS

In AWS Identity and Access Management

Go to:

IAM → Identity Providers → Add provider

Provider type:

OIDC

Provider URL:

https://token.actions.githubusercontent.com

Audience:

sts.amazonaws.com

This registers GitHub as a trusted identity provider in AWS.

3️⃣ Step 2 — Create IAM Role for GitHub

Create an IAM Role that GitHub workflows can assume.

Example Trust Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:org-name/repo-name:*"
        }
      }
    }
  ]
}

This means:

Only workflows from:

org-name/repo-name

can assume this role.

4️⃣ Step 3 — Attach Permissions to IAM Role

Attach policies like:

Example:

AmazonEKSClusterPolicy
AmazonS3FullAccess

Or a custom policy.

Example:

{
  "Effect": "Allow",
  "Action": [
    "eks:DescribeCluster",
    "s3:*"
  ],
  "Resource": "*"
}
5️⃣ Step 4 — Configure GitHub Workflow

In GitHub workflow YAML:

name: Deploy

on:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-role
          aws-region: us-east-1

      - name: Deploy
        run: aws s3 ls

Key permission required:

id-token: write

This allows GitHub to generate an OIDC token.

6️⃣ Step 5 — Store Non-AWS Secrets in GitHub

You still store application secrets in GitHub Secrets.

Example:

DB_PASSWORD
API_KEY

Access them in workflow:

env:
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}

But AWS credentials are NOT stored.




