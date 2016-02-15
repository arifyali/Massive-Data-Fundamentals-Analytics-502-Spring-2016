#!/usr/bin/env python2
# 
# Demonstrate the yield


def get_one():
    yield 10
    yield 20
    yield 30
    yield 40


def get_two():
    yield 1,"the first value"
    yield 2,"the second value"

if __name__=="__main__":
    for x in get_one():
        print("get_more returned: {}".format(x))
    print("\n")
    for x,y in get_two():
        print("get_two returned: {},{}".format(x,y))

        
