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
