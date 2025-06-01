**Pallindrome**

*Using method*

```python
def palindrome(s):
    temp = s[::-1]
    if s == temp:
        print("pallindrome")
    else:
        print("not a pallindrome")
s = "malayalam"    
palindrome(s)
```

*Using Index*

```python
def palindrome(s):
    n = len(s)
    for i in range(n):
        if s[i] != s[n-i-1]:
            print("not a pallindrome")
        else:
            print("pallindrome")
            break
            
s = "malayalam"
palindrome(s)
```
*While loop*
```python
def palindrome(s):
    n = len(s)
    first = 0
    last = n - 1
    while first <= last:
        if s[first] == s[last]:
            first += 1
            last -= 1
        else:
            return False
    return True

s = "malayalam"
print(palindrome(s))  # Output: True
```
