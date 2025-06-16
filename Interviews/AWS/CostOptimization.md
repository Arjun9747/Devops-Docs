**Environment Rightsizing**

eliminate oversized instances 

**Log Retention and Duplication Optimization**

Remove redundant logs to lower storage cost 

**Operational Infra Cost Optimization**

Balance the use of Spot and on-demand instances

**Weekend Evening Cost Optimization**

Optimize off-peak hours by scaling down or shutting down unused workloads

for DEV only single AZ is required for RDS 

Resize idel EBS instance and remove it

****************************************

**Planning and assessment phase**

| **Phase**                | **Purpose**                                                               | **How the Calculator Helps**                                           |
| ------------------------ | ------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Assessment** ✅         | Understand current infrastructure and estimate future AWS costs           | Estimate costs for lift-and-shift, modernization, or hybrid strategies |
| **Planning** ✅           | Design target architecture, choose services, evaluate cost vs performance | Compare pricing models (e.g., On-Demand vs Reserved Instances)         |
| **Optimization** (Later) | Optimize running workloads                                                | Simulate savings with Reserved Instances or Savings Plans              |


**AWS Savings Plan**

A flexible pricing model that offers significant cost savings (up to 72%) in exchange for committing to a consistent usage (e.g., $/hour) over a 1 or 3-year term.

| Type                          | Description                                                                          | Flexibility |
| ----------------------------- | ------------------------------------------------------------------------------------ | ----------- |
| **Compute Savings Plan**      | Applies to EC2 (any instance type, family, region), Lambda, and Fargate              | Highest     |
| **EC2 Instance Savings Plan** | Applies to specific instance family in a specific region (e.g., `m5` in `us-east-1`) | Medium      |


**AWS Budgets**

A cost management and alerting tool that helps you:

Set budgets for cost or usage

Track actual vs projected spend

Trigger alerts when nearing thresholds

| Type                   | Purpose                                                         |
| ---------------------- | --------------------------------------------------------------- |
| **Cost Budget**        | Alert when spend exceeds budgeted amount                        |
| **Usage Budget**       | Alert when usage (e.g., GB, instance hours) exceeds a threshold |
| **Reservation Budget** | Track RIs or Savings Plans coverage & utilization               |


**Pillars of Cloud Cost Model**

| Pillar       | Goal                       | Tools/Methods                      |
| ------------ | -------------------------- | ---------------------------------- |
| Visibility   | Know where money goes      | Cost Explorer, CUR, tagging        |
| Allocation   | Assign costs properly      | Linked accounts, tag-based reports |
| Planning     | Forecast and budget wisely | Budgets, Pricing Calculator        |
| Optimization | Reduce waste               | Trusted Advisor, rightsizing, RIs  |
| Control      | Enforce guardrails         | IAM, Service Quotas, Budgets       |
| Measurement  | Track cost efficiency      | KPIs, unit cost metrics            |

**Use SCP to manage cost**

| Practice                                 | Why It Helps                                               |
| ---------------------------------------- | ---------------------------------------------------------- |
| Apply SCPs at the **OU level**           | Easy to manage for similar account types (e.g., Dev, Prod) |
| Use **“Deny” with conditions**           | More precise than full denies                              |
| Combine with **tags + budgets**          | SCP prevents, Budgets alert                                |
| Test with **AWS Access Analyzer**        | Validate your SCPs                                         |
| Start with **monitoring**, then restrict | Avoid breaking critical workflows                          |





