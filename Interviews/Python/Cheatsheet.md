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






