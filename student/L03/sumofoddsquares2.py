#!/usr/bin/env python2

# Sum of odd squares
# Filtering in the reducer


from mrjob.job import MRJob
import heapq

def isodd(x):
    return x%2==1

class SumOfSquares(MRJob):
    def mapper(self, _, line):
        (label,value) = line.strip().split(",")
        value = int(value)
        yield label,value**2

    def reducer(self, label, values):
        yield label, sum(filter(isodd,values))


if __name__=="__main__":
    SumOfSquares.run()
