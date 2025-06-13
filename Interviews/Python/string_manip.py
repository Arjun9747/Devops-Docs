
def string1(s):
  return s.split("-")

res = string1("Ar-j-un")
final_result = "".join(res)  # Joins list elements without spaces
print(final_result)
