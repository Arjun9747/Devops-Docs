def char_occurence(s):
  freq = {}
  for char in s:
    if char in freq:
      freq[char] += 1
    else:
      freq[char] = 1

  return freq

s = "hhello"
result = char_occurence(s)

for char, count in result.items():
  print(f"{char} :{count}")
