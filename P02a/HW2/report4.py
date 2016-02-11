#!/usr/bin/env python2

# Output the number of URLs served on each day
# input is a weblog

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
from mrjob.step import MRStep
import heapq
import os

TOPN=10
class WeblogURLTop10(MRJob):
    def mapper(self, _, line):
	filename = mrjob.compat.jobconf_from_env("map.input.file")
	log = Weblog(line)
	yield (log.wikipage(),1)

        # add your code here to extract the wiki page from line and yield the <key,value>
        # where the key is the page name of the web log value and the value is 1


    def reducer(self, key, values):
	yield (key,sum(values))
        # Add your code here to sum the number of values for each key
        # and yield the results

    def top10_mapper(self, word, count):
        # notice that we put the counts first!
        yield "Top10", (count,word) 

    def top10_reducer(self, key, values):
	for values in heapq.nlargest(TOPN,values):
		yield values
        # put code here to select the top 10 values for the key and output them


    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),

            MRStep(mapper=self.top10_mapper,
                   reducer=self.top10_reducer) ]

if __name__=="__main__":
    WeblogURLTop10.run()

