#!/usr/bin/env python2
#
# 
# Small program to display the first 50 lines of a web log
# Creates a single mapper that maps every line to the same key, with the values
# being the datetime and the original weblog line.
# The reducer counts 50

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
import os

class First50(MRJob):
    def mapper(self, _, line):
        o = Weblog(line)
        yield "first50",(o.datetime,line)

    def reducer_init(self):
        self.counter = 0

    def reducer(self, key, values):
        if self.counter<50:
            self.counter += 1
            yield CHANGEME

if __name__=="__main__":
    First50.run()
