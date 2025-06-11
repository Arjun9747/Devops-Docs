def fibannoci(n):
  a,b = 0,1
  series= []
  for _ in range(n):
    series.append(a)
    a,b = b, a+b
  return series

  #recursion 

  def fibannoci_recursion(n):
    if n<=0:
      return n
    elif n ==1:
      return 1
    else:
      return fibanoci_recursion(n-1)+ fibannoci_recursion(n-2)

#generate list

def generate_series(n):
  series = []
  for i in range(n):
    sereis.append(fibannoci_recrusive(i))
  return series

print(generate_sereis(10))



  
    
