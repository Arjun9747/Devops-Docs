**re.match() , search(),findall(),finditer()**

Matches pattern at the beginning of the string 

```python
match_string1 = "hello world"
match1 = re.match(r"^Hello",match_string1)

search1 = re.search(r"^abc","123abc456")
#match object

find1 = re.findall(r'^\d+' ',' 'abc123def456')
#123,456

matches= re.finditer(r"^hello","helloworld")

for i in matches:
  print(f"found {match.group()} at position {match.start()}"
#re.IGNORECASE

re.split(r'\d+', 'abc123def456')  # ['abc', 'def', '']

```







```


