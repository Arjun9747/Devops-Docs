```markdown
Ensure script file is executable in workflow 
name: Make script executable
        run: chmod +x scripts/deploy.sh

Github Token to access private repo, push the code , trigger workflows 

The matrix strategy in GitHub Actions is a powerful feature that allows you to run a job multiple times with different combinations of inputs, such as environment variables, operating systems, or language versions — automatically and in parallel.
    strategy:
      matrix:
        python: [3.8, 3.9, 3.10]


action.yml (or action.yaml)
This file is required for defining a custom action, and it contains key information about your action, such as:
	• Inputs: Parameters your action expects from the workflow
	• Outputs: Values your action provides to other steps or jobs
	• Runs: The configuration for how the action is executed, including the runtime environment

A branch protection rule in GitHub Actions (GHA) is a way to enforce specific workflows and settings for a particular branch in a repository. It allows you to define rules that govern how code changes are made to a branch, ensuring the integrity and quality of the codebase {Reviews , status checks, who can push and merge}

The primary purpose of caching dependencies in a GitHub Actions workflow is to speed up the execution time of your workflows by reusing previously downloaded dependencies or build outputs instead of downloading or rebuilding them from scratch on every run.

A composite action in GitHub Actions offers a way to combine multiple steps and actions into a single reusable unit. This functionality allows you to define a series of steps in a single action that can be reused across different workflows and repositories.

Cache Actions 
actions/checkout@v2 action is used to clone the repository to the runner
actions/cache@v2 action caches the node_modules directory.
The key defines the cache key based on the operating system (runner.os) and the hash of the package-lock.json file (hashFiles('**/package-lock.json')). This ensures that the cache is invalidated when the dependencies change.


- name: Checkout code
        uses: actions/checkout@v2

      - name: Cache Node.js modules
        uses: actions/cache@v2
        with:
          # Define the cache key based on the package-lock.json file
          key: ${{ runner.os }}-node-modules-${{ hashFiles('**/package-lock.json') }}
          path: node_modules

Strategies 
Sequential, Parallel, Conditonal, Matrixes 


When creating a GitHub Action, there are several important files to consider:
action.yml: This file defines the metadata for your action, including its name, description, and inputs.
workflow.yml: This file defines the workflow that uses your action, including the jobs, steps, and triggers.
Dockerfile: If your action uses a Docker container, this file defines the container's configuration.
package.json: If your action uses JavaScript, this file defines the dependencies and scripts for your action.

An event is what triggers the workflow to run. {push}
A workflow can contain multiple jobs, and it specifies what actions should be taken in response to a specific event {job for testing and deployment}
job is executed in isolation, meaning one job’s steps run on the same runner. {run test and reports}
A step is a single task within a job.{checkout


Triggers
• push: Triggered when code is pushed.
• pull_request: Triggered on PR events.
• schedule: Triggered on a scheduled basis.
• workflow_dispatch: Triggered manually.
• release: Triggered on release events.
• workflow_run: Triggered after the completion of another workflow.


The continue-on-error keyword allows you to tolerate failure in certain steps and continue with the workflow execution.

To validate that a self-hosted runner can access all required GitHub network services, your team can use the --check parameter with the config.sh script during runner setup.

workflow_call : Call one workflow from another 
Workflow_dispatch : manually trigger the workflow 
Repository_dispatch : cross repo automation 

matrix : parallel job excution
Needs : defines job dependies 
Councurreny: avoid duplicate runs 
Defaults:  define common work dirs
Env: set env 

Use workflow_call for reusable logic
Use needs: to run jobs in parallel
Use actions/cache smartly


- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: ${{ runner.os }}-npm-

Matrix Strategy Wisely
Don't run workflows on every event
Use Lightweight Base Images

SARIF (status analysis result interafece file) 

Codeql analysis engine 
  - CodeQL database is created 
 - Codeql queries are run against Codeql DB
 - show alerts 

Codeql uses relational data and uses object query language 

Types
 . .ql querues
  - alert and path queries

The cache feature in GitHub Actions is used to speed up workflows by reusing data from previous runs. This is particularly useful in CI/CD pipelines where you have dependencies or build artifacts that don’t change often.

```
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```
```markdown
path: Where pip stores downloaded packages.

key: Uniquely identifies the cache. If the hash of requirements.txt hasn’t changed, the cache will be reused.

restore-keys: Fallback keys if an exact match isn't found.
```


