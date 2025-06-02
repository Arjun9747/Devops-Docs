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

*While loop palindrome number*

```python
def palindrome(num):
    temp = num #146
    rev = 0
    while (temp >0):
        digit = temp%10 #6
        rev = rev * 10 + digit 
        #rev = 0 * 10+ 6 = 6 
        temp = temp //10  # 14
    if num == rev:
        print("palindrome")
    else:
        print("not a palindomr")
palindrome(4540)
```
