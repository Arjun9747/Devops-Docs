| Feature         | List                                                                   | Tuple                                                              |
| --------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Mutability**  | **Mutable** — you can change, add, remove elements after creation      | **Immutable** — once created, you cannot change elements           |
| **Syntax**      | Square brackets: `[1, 2, 3]`                                           | Parentheses (usually): `(1, 2, 3)`                                 |
| **Performance** | Slightly slower due to mutability overhead                             | Faster and more memory efficient                                   |
| **Use cases**   | When you need a collection that can change                             | When data should remain constant and hashable (e.g., as dict keys) |
| **Methods**     | Many list methods: `.append()`, `.remove()`, `.pop()`, `.sort()`, etc. | Very few methods, mainly `.count()`, `.index()`                    |
| **Hashability** | Not hashable (cannot be dict keys or set elements)                     | Hashable if all elements are hashable (can be dict keys)           |


**Decorator**

A function that takes another function as a argument 

user logged in , the function is executed other display a message that user must be logged in 

```python
def login_required(func):
    def wrapper(user_logged_in):
        if user_logged_in:
            return func()
        else:
            print("You need to log in first.")
    return wrapper

@login_required
def access_secure_page():
    print("Welcome to the secure page!")

# Trying to access the secure page without logging in
access_secure_page(False)

# Logging in and accessing the secure page
access_secure_page(True)
```
**Memory Managment**

Python manages memory automatically through its memory manager.

When you create an object (like an int, list, dict), Python allocates memory for it in the heap

Python uses reference counting to keep track of how many references point to an object.

Python has a cyclic garbage collector (gc module) to detect and clean these cycles.

It runs periodically to free memory occupied by unreachable cycles.

**Generator and Iterators**

Generators are iterators which can execute only once . Uses yield keyword 

every generator is an iterator 

A Iterator is an object that contain countable number of values and its used to iterate over  objects like 
list tuples sets 

Uses Iter and next functions 

Every Iterator is not a generator 

```python
def count_to_five():
    num = 1
    while num <= 5:
        yield num
        num += 1

# Using the generator
gen = count_to_five()
for val in gen:
    print(val)
```

**__init__**

__init__.py --> its a python package or module directory . It can be blank 

__init__() --> Constructor to initilaize an object 

Module --> .py file , collection of functions and global variables 

Package --> Collection of module 

**Self**

Refer the current instance of the class and used to access variable that belong to the class

**Pickling**

Pickling is the process of serializing a Python object into a byte stream so it can be saved to a file or sent over a network.

Unpickling is the reverse — loading the object back from the byte stream to reconstruct the original Python object.









