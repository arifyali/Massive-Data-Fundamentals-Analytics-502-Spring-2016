#!/usr/bin/env python
# Demonstrate two ways to filter in python:

numbers = [1,2,3,4,5,6,7,8]

# print even numbers

# Procedural:
even_numbers = []
for i in numbers:
    if i%2==0:
        even_numbers.append(i)
print("Even numbers: %s" % even_numbers)

# Functional:
def iseven(x):
    return x%2==0
even_numbers = filter(iseven,numbers)
print("Even numbers: %s" % even_numbers)

# With Lambda:
even_numbers = filter(lambda x:x%2==0,numbers)
print("Even numbers: %s" % even_numbers)
