def is_prime(n):
  if n <= 1:
    print("Not a prime number")
  for i in range(2,n):
    if n%i == 0:
      print("Not a prime number")
      break
  else:
    print("Prime number")
    

is_prime(27)
