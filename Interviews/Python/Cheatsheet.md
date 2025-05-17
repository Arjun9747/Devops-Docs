## Reading a File

```python
with open('file.txt', 'r') as file:
    content = file.read()
    print(content)

##Writing a file

```python
with open('file.txt','w') as file:
    file.write('Hello, Devops')

