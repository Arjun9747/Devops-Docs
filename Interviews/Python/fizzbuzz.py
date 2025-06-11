def fizzbuzz(n):
    for i in range(1, n+1):
        if i%3 ==0 and i %5 ==0:
            print(f"fizzbuzz",i)
        elif i%3 == 0:
            print(f"fizz",i)
        elif i%5 == 0:
            print(f"buzz",i)
        else:
            print(i)

fizzbuzz(32)


#using dictionary

def fizzbuzz(n):
    for i in range(1,n+1):
        output =""
        rules = {3: "fizz", 5: "buzz"}

        for key in rules:
            if i % key == 0:
                output += rules[key]

        print(output or i)

fizzbuzz(32)
