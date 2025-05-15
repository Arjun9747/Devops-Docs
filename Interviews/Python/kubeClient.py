
#To fetch and display status of K8S

from kubernetes import client, config

# Load kubeconfig (default location: ~/.kube/config)
config.load_kube_config()

# Initialize the API client
v1 = client.CoreV1Api()

# Specify the namespace (default is 'default')
namespace = "default"

# Fetch all pods in the namespace
pods = v1.list_namespaced_pod(namespace)

print(f"{'Pod Name':<30} {'Status':<15} {'Node':<20}")
print("-" * 70)

# Display the status of each pod
for pod in pods.items:
    pod_name = pod.metadata.name
    pod_status = pod.status.phase
    node_name = pod.spec.node_name
    print(f"{pod_name:<30} {pod_status:<15} {node_name:<20}")
