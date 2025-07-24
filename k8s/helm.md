Helm

Package manager for K8s 
Charts are easy to create , version , share , publish 

Make app deployments easy 

keep manifest file under templates, helm will take care of the order of deployment 

Helm2 - tiller--> client server architecture 

Helm3 - single command installers

apps/
  chart.yml --> metadata (name, appversion,helm version, dependency)
  LICENSE
  README.MD
  values.yml --> actual config values
  values.schema.json  --> validate 
  charts -->
  crds
  templates --> Kubernetes manifest files 
  
  templates/NOTES.txt 

-------------------------------------------------

helm create myapp
This creates a directory structure like this:

bash
Copy
Edit
myapp/
├── charts/                  # Dependency charts
├── templates/               # YAML templates for Kubernetes resources
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── _helpers.tpl         # Template helpers
│   └── ...
├── Chart.yaml               # Metadata about the chart
├── values.yaml              # Default configuration values

Chart.yaml defines metadata like chart name, version, etc.
values.yaml to Define Default Values

4. Modify templates/deployment.yaml with Template Syntax
Use Helm templating ({{ }}) to inject values from values.yaml:

yaml
Copy
Edit
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}



Use _helpers.tpl to define reusable name and label templates

Helm provides a set of built-in objects that you can use in your chart templates to dynamically generate Kubernetes manifests based on context (like release name, chart version, user-defined values, etc.).

| Object           | Description                                              | Example Usage                             |
| ---------------- | -------------------------------------------------------- | ----------------------------------------- |
| `.Values`        | User-defined values from `values.yaml`, `--set`, or `-f` | `{{ .Values.image.repository }}`          |
| `.Chart`         | Metadata from `Chart.yaml`                               | `{{ .Chart.Name }}` → `mychart`           |
| `.Release`       | Info about the current release                           | `{{ .Release.Name }}` → `myapp`           |
| `.Capabilities`  | Info about Kubernetes version and APIs                   | `{{ .Capabilities.KubeVersion.Version }}` |
| `.Template`      | Info about the current template file                     | `{{ .Template.Name }}`                    |
| `.Files`         | Access files in the chart (e.g., ConfigMap from file)    | `{{ .Files.Get "config.json" }}`          |
| `.Values.global` | Shared global values across charts                       | `{{ .Values.global.imageRegistry }}`      |
| `.Namespace`     | The namespace where the chart is being installed         | `{{ .Namespace }}`                        |


Functions in Helm templates are operations like string manipulation, conditionals, formatting, etc.

A pipeline lets you pass the output of one function as input to another using the | operator.

-------------------------------------------------------------------------------------------------------------

Helm Plugins 

| Plugin                   | Purpose                                               |
| ------------------------ | ----------------------------------------------------- |
| `helm diff`              | Show changes before upgrade or install                |
| `helm secrets`           | Encrypt/decrypt `values.yaml` using SOPS              |
| `helm push`              | Push chart to a chart repository (OCI or ChartMuseum) |
| `helm unittest`          | Run unit tests on chart templates                     |
| `helm template-validate` | Validate rendered templates using `kubeval`           |

-----------------------------------------------------------------------------------

Convert yaml to helm 

| Step | Action                                                    |
| ---- | --------------------------------------------------------- |
| 1️⃣  | Create Helm chart with `helm create`                      |
| 2️⃣  | Copy YAML files into `templates/`                         |
| 3️⃣  | Replace hardcoded values with `{{ .Values.* }}`           |
| 4️⃣  | Add those values in `values.yaml`                         |
| 5️⃣  | Use `helm install` to deploy or `helm template` to render |

---------------------------------------------------------------------------------------

Helm does not directly read environment variables into values.yaml or templates at runtime, but you can inject them during chart rendering using:

using --set 

export IMAGE_TAG=v1.2.3

helm install myapp ./mychart --set image.tag=$IMAGE_TAG

Use envsubst to Substitute Env Vars in a Template File

| Use Case                    | Method                                        |
| --------------------------- | --------------------------------------------- |
| Inject one value from shell | `--set key=$ENV_VAR`                          |
| Inject many from a file     | Use `envsubst` on a template values file      |
| Pass into Pod environment   | Use `env` section in your Deployment template |
| Dynamic rendering           | Use `helm template` with `--set` in CI/CD     |




