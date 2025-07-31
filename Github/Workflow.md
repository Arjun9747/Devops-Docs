
# Devops DORA 

 DevOps Research and Assessment

 | Metric                             | What it Measures                        | Why it Matters                      |
| ---------------------------------- | --------------------------------------- | ----------------------------------- |
| **1. Deployment Frequency (DF)**   | How often you deploy to production      | Measures speed of delivery          |
| **2. Lead Time for Changes (LT)**  | Time from code commit to deploy         | Measures development efficiency     |
| **3. Change Failure Rate (CFR)**   | % of deployments that cause failures    | Measures quality and stability      |
| **4. Mean Time to Restore (MTTR)** | Time to recover from production failure | Measures reliability and resilience |

Github file

CI.yaml --> Continous Integration file 

Ensure Concurrency --> Ensure only one run of this workflow per branch or ref is active at a time 
if a new run is triggerred and previous run is cancelled. 

```yaml
concurrency:
  group: ${{github,workflow}}- {{github-ref}}
  cancel-in-progress: true
```

Workflow runs on 
Push ,  Schedule (cron job), workflow dispatch , pull request targets the main branch

Inputs :
 For manual trigger set an option for to run snyc scan, test 

For jobs: 

We will call a reuseble repository --> where we can pass parameters like app-name , chart path, component test , runners group 

the workflow will be called from other workflow using (workflow_call) to automate linting, versioning and provide release information 
