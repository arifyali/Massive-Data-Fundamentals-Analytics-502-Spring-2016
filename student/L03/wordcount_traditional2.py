#!/usr/bin/env python2

# This is the final wordcount program.
# the mapper outputs <word,1>
# the reducer receives <word,(1,1,1,...)> and outputs <word,COUNT>

from mrjob.job import MRJob
import heapq

class WordCount(MRJob):
    def mapper(self, _, line):
        yield "lines", 1
        yield "words",len(line.split())
        yield "chars", len(line)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__=="__main__":
    WordCount.run()
