#!/usr/bin/env python2

# Sum of squares


from mrjob.job import MRJob
import heapq

class SumOfSquares(MRJob):
    def mapper(self, _, line):
        (label,value) = line.strip().split(",")
        value = int(value)
        if value % 2 == 1:
            yield label,value**2

    def reducer(self, label, values):
        yield label, sum(values)


if __name__=="__main__":
    SumOfSquares.run()
