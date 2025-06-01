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

