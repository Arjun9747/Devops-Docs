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



