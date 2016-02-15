#!/usr/bin/env python2

# This is the final wordcount program.
# Job #1:
# the mapper outputs <word,1>
# the reducer receives <word,(1,1,1,...)> and outputs <word,COUNT>
# Job #2:
# The mapper outputs ("TopN",(word,COUNT))
# The reducer outputs the TopN

import mrjob,os
from mrjob.job import MRJob
from mrjob.step import MRStep
import heapq

TOPN=10
class WordCountTopN(MRJob):
    def mapper(self, _, line):
        for word in line.strip().lower().split():
            yield filter(str.isalpha,word),1
        
    def reducer(self, word, counts):
        yield word, sum(counts)

    def topN_mapper(self,word,count):
        yield "Top"+str(TOPN), (count,word)

    def topN_reducer(self,_,countsAndWords):
        for countAndWord in heapq.nlargest(TOPN,countsAndWords):
            yield _,countAndWord
        
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),

            MRStep(mapper=self.topN_mapper,
                   reducer=self.topN_reducer) ]



if __name__=="__main__":
    WordCountTopN.run()
