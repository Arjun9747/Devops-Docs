✅ What is a False Positive in Dynatrace?
A false positive is when Dynatrace reports a problem (e.g., CPU spike, failed transactions, response time degradation), but:

It’s a known issue (like during a deployment).

It’s not user-impacting (e.g., running a load test).

It's a temporary fluctuation.


🔧 1. Use Deployment Annotations via GitHub Actions
You can inform Dynatrace about new deployments so that it can correlate anomalies to deployments, reducing false positives triggered by expected changes.

🏷️ 2. Tag Entities Programmatically Using Python
Use the Dynatrace API to tag entities during deployment or test runs (e.g., to indicate load test or staging environment).

🔧 Python Script Example:
```python
import requests

api_token = "<YOUR_DYNATRACE_API_TOKEN>"
environment_url = "<YOUR_ENVIRONMENT_URL>"  # e.g. https://<env>.live.dynatrace.com

headers = {
    "Authorization": f"Api-Token {api_token}",
    "Content-Type": "application/json"
}

entity_id = "<ENTITY-ID>"  # e.g. PROCESS_GROUP-123456
tag_payload = {
    "tags": [{"key": "LoadTest"}, {"key": "IgnoreAlerts"}]
}

response = requests.post(
    f"{environment_url}/api/v2/entities/{entity_id}/tags",
    headers=headers,
    json=tag_payload
)

print("Tag applied:", response.status_code)
✅ Now you can filter or suppress alerts from entities tagged IgnoreAlerts.
```


⚙️ 3. Use Dynatrace Maintenance Windows (via GitHub Actions or Python)
If you're doing deployments or tests, create maintenance windows to suppress alerts temporarily.

```python
import requests
from datetime import datetime, timedelta

api_token = "<YOUR_API_TOKEN>"
env_url = "<YOUR_ENVIRONMENT_URL>"

headers = {
    "Authorization": f"Api-Token {api_token}",
    "Content-Type": "application/json"
}

now = datetime.utcnow()
later = now + timedelta(minutes=30)

data = {
    "type": "PLANNED",
    "description": "CI Deployment Window",
    "suppression": "PROBLEMS",
    "enabled": True,
    "scope": {
        "entities": ["PROCESS_GROUP-123456"]
    },
    "schedule": {
        "start": now.isoformat() + "Z",
        "end": later.isoformat() + "Z"
    }
}

response = requests.post(
    f"{env_url}/api/v2/maintenanceWindows",
    headers=headers,
    json=data
)

print("Maintenance window created:", response.status_code)
```
