**Convert list into string**

```python
a = ['Geek','for', 'Geeks']
res = ' '.join(a)
print(res)
```

**Reverse a list**

```python
my_list = [1,2,3,4,5]
my_list.reverse()
reversed_list = my_list[::-1]

list.insert(index, value)

def reversed_list(my_list):
  reversed_list = []
  for item in my_list:
      reversed_list.insert(0,item)
 return reversed_list
```
**Remove duplicate from list**

```python

my_list = [1,2,3,3,4,5,1]
unique_list = list(set(my_list))
```

**List conversion**

```python

s = "hello"
char_list = list(s)
print(char_list)
```

**String to list**

```python
words = ['apple', 'banana', 'cherry']
list1 = ''.join('words')
```
```python
word1 = "hello world"



print(word1)
print("After converting string to list")
w_list = list(word1)
print(w_list)

print("\nafter joining list with *")
list_word = '*'.join(w_list)
print(list_word)

print("\nAfter using split")
words = list_word.split('*')
print(words)
```
<img width="331" alt="image" src="https://github.com/user-attachments/assets/bca1d714-c805-4b86-90b2-0658d2a523db" />

Enumerate 

```python

colors = ['red', 'green', 'blue']
for index, color in enumerate(colors, start=1):
    print(f"{index}: {color}")
```

1: red
2: green
3: blue




