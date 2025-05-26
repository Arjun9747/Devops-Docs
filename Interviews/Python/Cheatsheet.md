**Reading a File**

```python
with open('file.txt', 'r') as file:
    content = file.read()
    print(content)
```

**Write to a File**

```python
with open('file.txt','w') as file:
    file.write('Hello, Devops')
```
**Import OS**

```python
import os

db_user = os.getenv('DB_USER')
print(db_user)
```
**Subprocess**

```python

import os

run = subprocess.run([ls-l]),capture_output=True, text = True)
print(result.stdout)
```
**API Request**

```python

import request

response= request.get("https://webpage.com")
print(response.json)
```

**json handling**

```python
import json 

with open('data.json','r') as file:
    data = json.load(file)
print (data)
```
**import logging**

```python

import logging

logging.basicConfig(level=logging.INFO)
logging.INFO("this is a info message")
```

#docker

```python

import docker

client=docker.from_env()
containers= client.container.list()

for containers in container:
    print(contianer.name)
```

**Monitor system**

```python
import psutil

print(psutil.cpu_time())
print(psutil.cpu_count())

```
**strip function**
```python
text = "---Hello, World!---"
result = text.strip("-")
print(f"'{result}'")
```

**json parser**

**json.load()**  --> Read from a file 

```python
import json

with open('data.json','r') as file:
    file = json.load(f)
```

**json.loads()** --> read from a string

```python
import json
json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)
```

**json.dumps()** --> convert python object to json

```python
import json
data = {"name": "Alice", "age": 30}
json_string = json.dumps(data)
```

**Configparser**

configparser is a built-in Python module used to handle configuration files (INI format). It's ideal for separating configuration from code—like database settings, file paths, or environment-specific variables.

```ini
[database]
host = localhost
port = 5432
username = admin
password = secret
```

```python
import configparser

# Create a config parser instance
config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')

# Access values
db_host = config['database']['host']
db_port = config.getint('database', 'port')

print(f"Connecting to DB at {db_host}:{db_port}")
print(f"Log Level: {log_level}")
```
HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
```

**for monitoring system performance**

```python
import psutil

print("CPU Usage:", psutil.cpu_percent(interval=1), "%")
print("Memory Usage:", psutil.virtual_memory().percent, "%")
```

**json loads**

```json
{"timestamp": "2025-05-26T10:00:00Z", "level": "ERROR", "message": "Failed to connect", "user": "alice"}
```
```python
import json

log_file = 'app.log'

with open(log_file, 'r') as f:
    for line in f:
        try:
            log_entry = json.loads(line)
            # Extract specific fields
            timestamp = log_entry.get('timestamp')
            level = log_entry.get('level')
            message = log_entry.get('message')

            # Filter only ERROR level logs
            if level == 'ERROR':
                print(f"[{timestamp}] ERROR: {message}")

        except json.JSONDecodeError:
            print("Skipping invalid JSON line")
```

**Extracting name and skipping first few lines**

```python
import panda as pd
import csv

df = pd.read_csv('yourfile.csv',skiprows=3)

with open('yourfile.sv','r') as file:
    csv_data = csv.reader(file)

next(csv.data)
next(csv.data)

```
csv.reader(file) --> print the output in a list
csv.readelines(file) --> return string 

**Regex**

for IP address
```python
\b(?:[0-9]{1,3}\.){3}\b
```
?: --> : not going to capture this grp
[0-9] --> 0-9 numbers
{1,3} --> 3 combinations
\. --> matches . 
{3} --> repeat the grp 3 times
\b boundary













