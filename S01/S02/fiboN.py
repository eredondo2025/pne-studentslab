def fibon(n):
    a = 0
    b = 1
    for i in range(n):
        c = a + b
        a = b
        b = c
    return a
print("The 5th element is: ", fibon(5))
print("The 10th element is: ", fibon(10))
print("The 15th element is: ", fibon(15))